import os
import sys
import img2pdf
from pathlib import Path


def collect_images(folder: Path):
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Invalid folder: {folder}")

    images = sorted(
        [
            str(p)
            for p in folder.iterdir()
            if p.suffix.lower() in [".jpg", ".jpeg"]
        ]
    )

    if not images:
        raise ValueError("No JPEG files found in folder.")

    return images


def convert_folder_to_pdf(input_folder: str, output_file: str):
    folder = Path(input_folder)
    images = collect_images(folder)

    with open(output_file, "wb") as f:
        f.write(img2pdf.convert(images))

    print(f"Created PDF: {output_file}")
    print(f"Pages: {len(images)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_folder> <output_pdf>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_pdf = sys.argv[2]

    convert_folder_to_pdf(input_folder, output_pdf)