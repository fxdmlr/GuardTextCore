#!/usr/bin/env python3
"""
Encode an image into a Base64 text string that fits within a maximum
character budget, by shrinking and compressing it until it fits.

Since the output must be pure text, this is lossy on the image itself
(it gets downscaled/compressed to fit) but the Base64 -> bytes step
is lossless: decode_image.py reconstructs the exact compressed image
bytes that were encoded.

Usage:
    python encode_image.py photo.jpg
    python encode_image.py photo.jpg --limit 1748
    python encode_image.py photo.jpg --limit 1748 --output encoded.txt

Requires: pillow  ->  pip install pillow
"""

import argparse
import base64
import io

from PIL import Image


def encode_image_to_fit(path, char_limit=1748, format="WEBP", verbose=False):
    """
    Shrink/compress an image until its Base64 encoding fits within
    char_limit characters.

    Args:
        path: Path to the input image.
        char_limit: Maximum length of the Base64 output string.
        format: Image format to re-encode as ("WEBP" is most efficient;
            "JPEG" is more universally supported).
        verbose: If True, print the resolution/quality/length it landed on.

    Returns:
        The Base64-encoded string (fits within char_limit characters).
        The image's own format header carries its width/height, so no
        extra metadata needs to travel alongside the string.

    Raises:
        ValueError if no combination of size/quality fits the budget.
    """
    image = Image.open(path).convert("RGB")
    orig_w, orig_h = image.size

    # Try progressively smaller scales, and within each scale, progressively
    # lower quality, until the Base64 output fits the budget.
    scale = 1.0
    for _ in range(40):
        w = max(1, int(orig_w * scale))
        h = max(1, int(orig_h * scale))
        resized = image.resize((w, h), Image.LANCZOS)

        for quality in (80, 60, 40, 25, 15, 8, 3):
            buf = io.BytesIO()
            save_kwargs = {"quality": quality}
            if format.upper() == "WEBP":
                save_kwargs["method"] = 6
            resized.save(buf, format=format, **save_kwargs)
            b64 = base64.b64encode(buf.getvalue()).decode("ascii")

            if len(b64) <= char_limit:
                if verbose:
                    print(f"Fit at {w}x{h}, quality={quality}, {len(b64)} chars (limit {char_limit})")
                return b64

        scale *= 0.8  # shrink further and try again

    raise ValueError(
        f"Could not fit image under {char_limit} characters even at "
        f"1x1 resolution. Try a smaller format or a higher char_limit."
    )


def main():
    parser = argparse.ArgumentParser(description="Encode an image to Base64 text within a character budget.")
    parser.add_argument("image", help="Path to the input image")
    parser.add_argument("--limit", type=int, default=1748, help="Max characters for the Base64 output (default: 1748)")
    parser.add_argument("--format", choices=["WEBP", "JPEG"], default="WEBP", help="Re-encoding format (default: WEBP)")
    parser.add_argument("--output", help="Save the Base64 string to a text file instead of printing it")

    args = parser.parse_args()

    b64 = encode_image_to_fit(args.image, args.limit, args.format, verbose=True)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(b64)
        print(f"Saved to {args.output}")
    else:
        print(b64)


if __name__ == "__main__":
    main()
