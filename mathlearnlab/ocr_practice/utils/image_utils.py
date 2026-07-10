"""
Image utility functions for OCR practice app.

Handles compression, encoding, and validation of uploaded images.
"""

import io
from PIL import Image


def compress_image(image_bytes: bytes, max_size: int = 5 * 1024 * 1024,
                   quality: int = 85) -> bytes:
    """Compress image to stay under max_size bytes.

    Parameters
    ----------
    image_bytes : bytes
        Raw image data (JPEG, PNG, etc.)
    max_size : int
        Maximum size in bytes.
    quality : int
        JPEG quality (1-100).

    Returns
    -------
    bytes — compressed JPEG image.
    """
    img = Image.open(io.BytesIO(image_bytes))

    # Convert RGBA to RGB if needed
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # If already small enough, return as JPEG
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    result = buf.getvalue()

    # Progressive quality reduction if still too large
    while len(result) > max_size and quality > 20:
        quality -= 15
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality)
        result = buf.getvalue()

    # If still too large, resize
    if len(result) > max_size:
        scale = (max_size / len(result)) ** 0.5
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size, Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality)
        result = buf.getvalue()

    return result


def validate_image(image_bytes: bytes) -> bool:
    """Check that uploaded bytes form a valid image."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()
        return True
    except Exception:
        return False


def get_image_dimensions(image_bytes: bytes) -> tuple[int, int]:
    """Get (width, height) of an image."""
    img = Image.open(io.BytesIO(image_bytes))
    return img.size
