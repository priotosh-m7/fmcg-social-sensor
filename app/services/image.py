import os
import uuid

from app.ai.image import generate_image
from app.services.cloudinary import upload_image

async def create_image(
    brand: str,
    category: str,
    visual_prompt: str
):
    prompt = f"""
Create a professional FMCG social media advertisement.

Brand: {brand}
Category: {category}

Creative direction:
{visual_prompt}

Requirements:
- Premium commercial advertising quality
- Suitable for an Instagram post
- Clean composition
- Strong visual hierarchy
- Product-focused FMCG aesthetic
- Leave appropriate visual space for advertising copy
- Do not invent statistics or claims
- Do not create fake endorsements
- Do not include unrelated brands
"""

    image_bytes = await generate_image(prompt)

    output_dir = "generated"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.png"
        # Upload directly to Cloudinary
    cloudinary_result = upload_image(
        image_bytes=image_bytes,
        filename=filename
    )

    return {
        "filename": filename,
        "image_url": cloudinary_result["image_url"],
        "cloudinary_public_id": cloudinary_result["public_id"],
    }