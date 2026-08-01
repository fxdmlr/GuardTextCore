#!/usr/bin/env python3
"""
Decode a Base64 text string (produced by encode_image.py) back into an
image file.

Usage:
    python decode_image.py encoded.txt --output restored.webp
    python decode_image.py --text "UklGRi4A..." --output restored.webp
"""

import argparse
import base64


def decode_image_from_text(b64_string, output_path):
    """
    Decode a Base64 string back into the exact image bytes and save it.

    Args:
        b64_string: The Base64 text (as produced by encode_image_to_fit).
        output_path: Where to save the reconstructed image. The extension
            should match the format used during encoding (.webp or .jpg).
    """
    data = base64.b64decode(b64_string)
    with open(output_path, "wb") as f:
        f.write(data)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Decode a Base64 string back into an image file.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("input_file", nargs="?", help="Path to a text file containing the Base64 string")
    source.add_argument("--text", help="The Base64 string directly, instead of a file")
    parser.add_argument("--output", required=True, help="Output image path, e.g. restored.webp")

    args = parser.parse_args()

    if args.text:
        b64_string = args.text
    else:
        with open(args.input_file, "r", encoding="utf-8") as f:
            b64_string = f.read().strip()

    path = decode_image_from_text(b64_string, args.output)
    print(f"Image restored to {path}")


if __name__ == "__main__":
    main()
