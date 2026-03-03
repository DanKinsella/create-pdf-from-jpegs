# JPEG to PDF Converter

Converts all .jpg/.jpeg files in a folder into a single PDF file using img2pdf.

## Setup

python -m venv venv
venv\Scripts\activate   (Windows)
source venv/bin/activate (Mac/Linux)

pip install -r requirements.txt

## Usage

python main.py scans output.pdf

Files are processed in alphabetical order. 
Rename files with leading numbers (e.g., 01.jpg, 02.jpg) if page order matters.