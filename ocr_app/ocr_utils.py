"""
ocr_app/ocr_utils.py
────────────────────
Tesseract-based OCR + field extraction for barcode / label images.
"""
import re
try:
    import pytesseract
except ImportError:
    pytesseract = None
from PIL import Image, ImageFilter, ImageEnhance

# ── Windows users: uncomment and set your Tesseract path ──────────────────

if pytesseract is not None:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess(image_path: str) -> Image.Image:
    """Sharpen + upscale image for better OCR accuracy."""
    img = Image.open(image_path).convert('L')          # grayscale
    img = img.filter(ImageFilter.SHARPEN)
    img = ImageEnhance.Contrast(img).enhance(2.0)
    if hasattr(Image, 'Resampling'):
        resample_filter = Image.Resampling.LANCZOS
    else:
        resample_filter = getattr(Image, 'LANCZOS', 1)
    img = img.resize((img.width * 2, img.height * 2), resample_filter)
    return img


def extract_text(image_path: str) -> str:
    """Return raw OCR text from an image file."""
    if pytesseract is None:
        raise ImportError('pytesseract is required to extract text from images')

    img = preprocess(image_path)
    config = '--oem 3 --psm 6 -l eng'
    return pytesseract.image_to_string(img, config=config)


def parse_fields(text: str) -> dict:
    """
    Parse MFD, EXP, and BATCH from raw OCR text.
    Handles common OCR noise (0↔O, 1↔I, spaces, colons).
    """
    t = text.upper().replace('\n', ' ')

    # Normalise common OCR errors in label keywords
    t = re.sub(r'MF[O0]|MFB', 'MFD', t)
    t = re.sub(r'[EF][XK][RP]', 'EXP', t)

    mfd   = re.search(r'MFD\s*[:\-]?\s*([A-Z0-9/\-\.]{4,15})', t)
    exp   = re.search(r'EXP\s*[:\-]?\s*([A-Z0-9/\-\.]{4,15})', t)
    batch = re.search(r'BATCH\s*(?:NO\.?)?\s*[:\-]?\s*([A-Z0-9\-]{3,18})', t)

    return {
        'mfd'  : mfd.group(1).strip()   if mfd   else '',
        'exp'  : exp.group(1).strip()   if exp   else '',
        'batch': batch.group(1).strip() if batch else '',
    }


def validate(fields: dict) -> str:
    """
    Compare extracted codes against the DateChart table.
    Returns 'PASS' if any MFD or EXP code is in the valid chart.
    """
    from ocr_app.models import DateChart

    valid_codes = set(DateChart.objects.values_list('code', flat=True))
    mfd   = fields.get('mfd', '').upper().strip()
    exp   = fields.get('exp', '').upper().strip()

    if mfd and mfd in valid_codes:
        return 'PASS'
    if exp and exp in valid_codes:
        return 'PASS'
    return 'FAIL'
