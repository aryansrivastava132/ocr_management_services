#!/bin/bash
apt-get update -y
apt-get install -y tesseract-ocr tesseract-ocr-eng
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate