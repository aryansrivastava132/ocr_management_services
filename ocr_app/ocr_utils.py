import os
# ensure names exist even if imports fail so static analyzers won't flag usage
pytesseract = None
Image = ImageFilter = ImageEnhance = None
try:
    import pytesseract
    from PIL import Image, ImageFilter, ImageEnhance
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

def extract_text(image_path):
    if not TESSERACT_AVAILABLE or Image is None or ImageFilter is None or pytesseract is None:
        return ""
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.filter(ImageFilter.SHARPEN)
        return pytesseract.image_to_string(img)
    except Exception as e:
        return f"Error: {str(e)}"

def parse_fields(text):
    import re
    fields = {'mfd': '', 'exp': '', 'batch': ''}
    mfd = re.search(r'MFD[:\s]*([A-Z0-9/\-]+)', text, re.IGNORECASE)
    exp = re.search(r'EXP[:\s]*([A-Z0-9/\-]+)', text, re.IGNORECASE)
    batch = re.search(r'BATCH[:\s]*([A-Z0-9/\-]+)', text, re.IGNORECASE)
    if mfd: fields['mfd'] = mfd.group(1).strip()
    if exp: fields['exp'] = exp.group(1).strip()
    if batch: fields['batch'] = batch.group(1).strip()
    return fields

def validate(fields):
    from .models import DateChart
    codes = list(DateChart.objects.values_list('code', flat=True))
    if fields['mfd'] in codes or fields['exp'] in codes:
        return 'PASS'
    return 'FAIL'