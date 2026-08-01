#!/usr/bin/env python3
"""
Convert an image into ASCII art.

Usage:
    python img_to_ascii.py input.jpg
    python img_to_ascii.py input.jpg --width 120
    python img_to_ascii.py input.jpg --width 120 --output art.txt
    python img_to_ascii.py input.jpg --invert --charset detailed

Requires: pillow  ->  pip install pillow
"""

import argparse
from PIL import Image

# A few ramps from "empty" (dark) to "full" (light). You can invert with --invert.
CHARSETS = {
    "simple": "@%#*+=-:. ",
    "detailed": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    "blocks": "█▓▒░ ",
}

# Preset output widths (in characters) for quick resolution control.
RESOLUTIONS = {
    "low": 60,
    "medium": 120,
    "high": 250,
    "ultra": 400,
}


def resize_image(image, new_width=100):
    width, height = image.size
    # Characters are taller than they are wide, so we compress vertically
    # to keep the aspect ratio looking correct in a monospace font.
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)
    return image.resize((new_width, max(new_height, 1)))


def grayify(image):
    return image.convert("L")


def pixels_to_ascii(image, charset, invert=False):
    chars = charset[::-1] if invert else charset
    pixels = image.getdata()
    scale = len(chars) - 1
    ascii_str = "".join(chars[pixel * scale // 255] for pixel in pixels)
    return ascii_str


def image_to_ascii(path, width=300, charset_name="detailed", invert=False):
    """
    Convert an image file into an ASCII art string.

    Args:
        path: Path to the input image.
        width: Output width in characters.
        charset_name: One of "simple", "detailed", "blocks".
        invert: If True, invert the light/dark mapping.

    Returns:
        The ASCII art as a multi-line string.
    """
    image = Image.open(path)

    charset = CHARSETS.get(charset_name, CHARSETS["simple"])

    image = resize_image(image, width)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image, charset, invert)

    img_width = image.width
    ascii_lines = [
        ascii_str[i:i + img_width] for i in range(0, len(ascii_str), img_width)
    ]
    return "\n".join(ascii_lines)


def main():
    parser = argparse.ArgumentParser(description="Convert an image into ASCII art.")
    parser.add_argument("image", help="Path to the input image file")
    parser.add_argument("--width", type=int, help="Output width in characters (overrides --resolution if set)")
    parser.add_argument("--resolution", choices=RESOLUTIONS.keys(), default="high",
                         help=f"Resolution preset (default: high). Options: {', '.join(f'{k}={v}' for k, v in RESOLUTIONS.items())}")
    parser.add_argument("--output", help="Save output to a text file instead of printing to console")
    parser.add_argument("--charset", choices=CHARSETS.keys(), default="detailed", help="Character set to use")
    parser.add_argument("--invert", action="store_true", help="Invert light/dark mapping")

    args = parser.parse_args()

    width = args.width if args.width else RESOLUTIONS[args.resolution]
    ascii_art = image_to_ascii(args.image, width, args.charset, args.invert)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(ascii_art)
        print(f"ASCII art saved to {args.output}")
    else:
        print(ascii_art)


if __name__ == "__main__":
    main()