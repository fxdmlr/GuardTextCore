#!/usr/bin/env python3
"""
Convert an image to pure black & white by thresholding: every pixel becomes
either black or white depending on whether its brightness is above or below
a cutoff value.

Usage:
    python threshold_image.py photo.jpg
    python threshold_image.py photo.jpg --threshold 100
    python threshold_image.py photo.jpg --output bw.png
    python threshold_image.py photo.jpg --adaptive
    python threshold_image.py photo.jpg --invert

Requires: pillow  ->  pip install pillow
"""

import argparse

from PIL import Image, ImageOps


def threshold_image(path, threshold=128, invert=False, adaptive=False, output_path=None):
    """
    Convert an image to pure black & white by thresholding.

    Args:
        path: Path to the input image.
        threshold: Brightness cutoff (0-255). Pixels above this become
            white, pixels at or below become black. Ignored if adaptive=True.
        invert: If True, flip which side of the threshold is black vs white.
        adaptive: If True, use the image's own mean brightness as the
            threshold instead of a fixed value - handy when lighting
            varies a lot between images.
        output_path: If given, saves the result to this path.

    Returns:
        A PIL Image in mode "1" (1-bit black & white).
    """
    image = Image.open(path).convert("L")  # grayscale first

    if adaptive:
        # Use the image's own average brightness as the cutoff
        histogram = image.histogram()
        pixels = sum(histogram)
        brightness_sum = sum(i * count for i, count in enumerate(histogram))
        threshold = brightness_sum / pixels

    lut = [0 if i <= threshold else 255 for i in range(256)]
    if invert:
        lut = [255 - v for v in lut]

    bw_image = image.point(lut, mode="1")

    if output_path:
        bw_image.save(output_path)

    return bw_image


def main():
    parser = argparse.ArgumentParser(description="Convert an image to pure black & white via thresholding.")
    parser.add_argument("image", help="Path to the input image")
    parser.add_argument("--threshold", type=int, default=128, help="Brightness cutoff, 0-255 (default: 128)")
    parser.add_argument("--adaptive", action="store_true", help="Use the image's own mean brightness as the threshold")
    parser.add_argument("--invert", action="store_true", help="Invert black/white")
    parser.add_argument("--output", help="Output file path (default: <name>_threshold.png)")

    args = parser.parse_args()

    output_path = args.output
    if not output_path:
        stem = args.image.rsplit(".", 1)[0]
        output_path = f"{stem}_threshold.png"

    threshold_image(
        args.image,
        threshold=args.threshold,
        invert=args.invert,
        adaptive=args.adaptive,
        output_path=output_path,
    )

    print(f"Thresholded image saved to {output_path}")


if __name__ == "__main__":
    main()