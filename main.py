import argparse
import tempfile
from pathlib import Path

import img2pdf
from PIL import Image


def collect_images(folder: Path) -> list[Path]:
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Input folder does not exist or is not a directory: {folder}")

    images = sorted([p for p in folder.iterdir() if p.suffix.lower() in (".jpg", ".jpeg")])
    if not images:
        raise ValueError(f"No .jpg/.jpeg files found in: {folder}")

    return images


def preprocess_images(
    images: list[Path],
    max_width_px: int,
    quality: int,
    grayscale: bool,
) -> tuple[Path, list[str]]:
    """
    Returns (temp_dir, list_of_preprocessed_image_paths_as_str).
    """
    temp_dir = Path(tempfile.mkdtemp(prefix="jpeg2pdf_"))
    out_paths: list[str] = []

    for src in images:
        with Image.open(src) as im:
            # Handle EXIF orientation (common with phone scans)
            im = ImageOps.exif_transpose(im) if hasattr(Image, "Ops") else im  # fallback

            if grayscale:
                im = im.convert("L")  # grayscale
                # img2pdf expects RGB/JPEG fine; keep grayscale JPEG for size
            else:
                im = im.convert("RGB")

            # Resize proportionally if needed
            if max_width_px and im.width > max_width_px:
                ratio = max_width_px / im.width
                new_size = (int(im.width * ratio), int(im.height * ratio))
                im = im.resize(new_size, Image.LANCZOS)

            dst = temp_dir / src.name
            save_kwargs = {
                "format": "JPEG",
                "quality": quality,
                "optimize": True,
                "progressive": True,
            }

            # If grayscale, ensure saving as JPEG still works fine
            if im.mode == "L":
                im.save(dst, **save_kwargs)
            else:
                im.save(dst, **save_kwargs)

            out_paths.append(str(dst))

    return temp_dir, out_paths


def make_pdf(image_paths: list[str], output_pdf: Path) -> None:
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(image_paths))


def main():
    parser = argparse.ArgumentParser(description="Create a single PDF from JPEG scans (with compression).")
    parser.add_argument("input_folder", help="Folder containing .jpg/.jpeg files")
    parser.add_argument("output_pdf", help="Output PDF path, e.g. output.pdf")

    # Sensible defaults for email-friendly docs:
    # A4 width at ~200 DPI ≈ 1654px. At 300 DPI ≈ 2480px.
    parser.add_argument("--max-width", type=int, default=1654, help="Max image width in pixels (default: 1654)")
    parser.add_argument("--quality", type=int, default=70, help="JPEG quality 1-95 (default: 70)")
    parser.add_argument("--grayscale", action="store_true", help="Convert images to grayscale for smaller PDFs")

    args = parser.parse_args()

    input_folder = Path(args.input_folder)
    output_pdf = Path(args.output_pdf)

    images = collect_images(input_folder)

    # Pillow EXIF transpose helper import (done here to keep top imports simple)
    global ImageOps
    from PIL import ImageOps  # noqa: E402

    temp_dir, processed = preprocess_images(
        images=images,
        max_width_px=args.max_width,
        quality=args.quality,
        grayscale=args.grayscale,
    )

    make_pdf(processed, output_pdf)

    print(f"Created PDF: {output_pdf}")
    print(f"Pages: {len(processed)}")
    print(f"Preprocessed images in: {temp_dir} (auto-temp; safe to delete after verifying)")


if __name__ == "__main__":
    main()