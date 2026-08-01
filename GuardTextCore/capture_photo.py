#!/usr/bin/env python3
"""
Silently open the default camera, capture a single photo, and save it to disk.
No preview window, no keypress needed - it just grabs a frame and exits.

Usage:
    python capture_photo.py
    python capture_photo.py --output photo.jpg
    python capture_photo.py --camera 1 --delay 3 --warmup 5

Requires: opencv-python  ->  pip install opencv-python
"""

import argparse
import time
from datetime import datetime

import cv2


def capture_photo(camera_index=0, output_path=None, min_delay=1.0):
    """
    Open a camera and immediately save a single captured frame, no UI.

    Args:
        camera_index: Which camera to use (0 is usually the default/built-in).
        output_path: Where to save the photo. Defaults to photo_<timestamp>.jpg.
        min_delay: Minimum seconds to keep the camera open and reading frames
            before capturing. Many webcams return dark/unfocused frames right
            after opening, so this gives the sensor time to adjust exposure
            and focus. The actual wait may be slightly longer depending on
            the camera's frame rate.

    Returns:
        The path the photo was saved to.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera at index {camera_index}")

    if not output_path:
        output_path = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

    try:
        start = time.time()
        frame = None

        # Keep reading frames until at least min_delay seconds have passed,
        # so the sensor has time to settle on exposure/focus.
        while True:
            ret, frame = cap.read()
            if not ret:
                raise RuntimeError("Failed to read from camera")
            if time.time() - start >= min_delay:
                break

        cv2.imwrite(output_path, frame)
    finally:
        cap.release()

    print(f"Photo saved to {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Automatically capture a photo from the webcam.")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--output", help="Output file path (default: photo_<timestamp>.jpg)")
    parser.add_argument("--min-delay", type=float, default=1.0, help="Minimum seconds to warm up the camera before capturing (default: 1.0)")

    args = parser.parse_args()
    capture_photo(camera_index=args.camera, output_path=args.output, min_delay=args.min_delay)


if __name__ == "__main__":
    main()
