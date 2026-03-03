# Create PDF from JPEGs (compressed)

This tool:
1) Preprocesses .jpg/.jpeg scans (optional resize + recompress using Pillow)
2) Creates a single PDF (using img2pdf)

## Setup (PowerShell)

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

## Basic usage

python main.py scans output.pdf

## Email-friendly presets

A4-ish, readable, small:
python main.py scans output.pdf --max-width 1654 --quality 70 --grayscale

Higher quality (bigger file):
python main.py scans output.pdf --max-width 2480 --quality 80

## Ordering

Files are processed in alphabetical order.
Use names like 01.jpg, 02.jpg, ... for predictable paging.