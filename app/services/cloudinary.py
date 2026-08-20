import os

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()
from app.config import (
   CLOUDINARY_CLOUD_NAME,
   CLOUDINARY_API_KEY,
   CLOUDINARY_API_SECRET
)


cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)


def upload_image(image_bytes: bytes, filename: str) -> dict:
    result = cloudinary.uploader.upload(
        image_bytes,
        folder="fmcg-social-sensor",
        public_id=os.path.splitext(filename)[0],
        resource_type="image",
    )

    return {
        "public_id": result["public_id"],
        "image_url": result["secure_url"],
        "width": result.get("width"),
        "height": result.get("height"),
        "format": result.get("format"),
    }