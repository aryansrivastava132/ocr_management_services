# OCR Barcode Verification System
### Django + HTML/CSS/JS + Tesseract OCR

---

## PROJECT STRUCTURE

```
ocr_django_project/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3              ← auto-created on first run
├── media/scans/            ← uploaded images (auto-created)
│
├── ocr_project/            ← Django project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── ocr_app/                ← Main Django app
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py           ← ScanRecord, DateChart
    ├── views.py            ← API endpoints
    ├── urls.py
    ├── ocr_utils.py        ← Tesseract + field parser
    └── templates/
        └── ocr_app/
            └── index.html  ← Full SPA (Scan, History, Date Chart)
```

---

## STEP 1 — Install Tesseract OCR

### Windows
1. Download installer: https://github.com/UB-Mannheim/tesseract/wiki
2. Run `tesseract-ocr-w64-setup-*.exe`
3. Default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
4. **Uncomment** this line in `ocr_app/ocr_utils.py`:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### Ubuntu / Debian Linux
```bash
sudo apt update && sudo apt install -y tesseract-ocr
```

### macOS
```bash
brew install tesseract
```

---

## STEP 2 — Install Python 3.10+

Download from https://python.org/downloads/
- ✅ Check "Add Python to PATH" during install (Windows)

---

## STEP 3 — Setup Virtual Environment

```bash
# Navigate to project folder
cd ocr_django_project

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux / Mac:
source venv/bin/activate
```

---

## STEP 4 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## STEP 5 — Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## STEP 6 — Create Admin User (Optional)

```bash
python manage.py createsuperuser
# Enter username, email, password when prompted
```

---

## STEP 7 — Start the Server

```bash
python manage.py runserver
```

Open your browser: **http://127.0.0.1:8000**

For **mobile / other devices on same WiFi**:
```bash
python manage.py runserver 0.0.0.0:8000
# Then open: http://<YOUR-PC-IP>:8000
```
To find your IP: `ipconfig` (Windows) or `hostname -I` (Linux)

---

## USING THE APP

### Tab 1: Scan
1. Click "Upload Photo" or drag & drop an image
2. Click "Scan & Verify"
3. See extracted MFD / EXP / Batch + PASS or FAIL result

### Tab 2: History
- View all past scans with thumbnails
- Export to Excel (color-coded PASS/FAIL)

### Tab 3: Date Chart
- Add valid MFD/EXP codes
- Any scan matching these codes → PASS
- Delete codes when they expire

---

## API ENDPOINTS

| Method | URL              | Description            |
|--------|-----------------|------------------------|
| GET    | `/`             | Main SPA page          |
| POST   | `/api/scan/`    | Upload photo, run OCR  |
| GET    | `/api/history/` | Get scan history (JSON)|
| GET    | `/api/datechart/` | List valid codes     |
| POST   | `/api/datechart/` | Add valid code       |
| DELETE | `/api/datechart/` | Remove a code        |
| GET    | `/api/report/`  | Download Excel report  |
| GET    | `/admin/`       | Django admin panel     |

---

## DEPLOYMENT (Free Hosting)

### Railway.app (Recommended)
```bash
# Add to requirements.txt:
gunicorn==21.2.0
whitenoise==6.6.0

# In settings.py add:
MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware', ...]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Procfile (create in root):
web: gunicorn ocr_project.wsgi --bind 0.0.0.0:$PORT

# Push to GitHub, connect at railway.app
```

### Render.com
```yaml
# render.yaml
services:
  - type: web
    name: ocr-verify
    env: python
    buildCommand: |
      apt-get install -y tesseract-ocr
      pip install -r requirements.txt
      python manage.py migrate
      python manage.py collectstatic --no-input
    startCommand: gunicorn ocr_project.wsgi
```

---

## TROUBLESHOOTING

| Problem | Fix |
|---------|-----|
| `TesseractNotFound` | Set path in `ocr_utils.py` (Windows) |
| `No module named 'PIL'` | `pip install Pillow` |
| `CSRF verification failed` | Clear cookies, retry |
| `Port already in use` | `python manage.py runserver 8001` |
| OCR returns empty text | Image too small/blurry — use 300dpi+ |
| MFD not found in text | Edit regex in `ocr_utils.py` `parse_fields()` |
