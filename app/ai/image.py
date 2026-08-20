import base64

from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, GEMINI_IMAGE_MODEL


async def generate_image(prompt: str):
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = await client.aio.models.generate_content(
        model=GEMINI_IMAGE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        ),
    )

    if not response.candidates:
        raise RuntimeError("Gemini returned no candidates.")

    for candidate in response.candidates:
        if not candidate.content:
            continue

        for part in candidate.content.parts:
            if part.inline_data and part.inline_data.data:
                return part.inline_data.data

    raise RuntimeError("Gemini did not return an image.")
