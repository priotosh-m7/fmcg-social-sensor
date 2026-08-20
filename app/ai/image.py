import base64
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GOOGLE_SEARCH_ENABLED,
    GEMINI_IMAGE_MODEL
)

async def generate_image(prompt: str):
    key = GEMINI_API_KEY

    if not key:
        raise RuntimeError("GEMINI_API_KEY is missing.")

    client = genai.Client(api_key=key)

    interaction = await client.aio.interactions.create(
        model=GEMINI_IMAGE_MODEL,
        input=prompt,
        response_format={
            "type": "image",
            "mime_type": "image/jpeg",
            "aspect_ratio": "1:1",
            "image_size": "1K"
        }
    )

    if not interaction.output_image:
        raise RuntimeError("Gemini did not return an image.")

    return base64.b64decode(
        interaction.output_image.data
    )