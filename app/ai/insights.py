import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.schemas import SensorOutput

load_dotenv()
from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GOOGLE_SEARCH_ENABLED
)
async def generate_insight(context):
    key = GEMINI_API_KEY
    if not key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env.")

    prompt = f"""
You are an FMCG social trend intelligence engine.

Brand: {context["brand"]}
Category: {context["category"]}
Market: {context["market"]}
Lookback: approximately {context["lookback_days"]} days

Use current web information and identify the most relevant CURRENT
trends, events, cultural moments, consumer conversations, sports
moments, news and emerging topics that could create a legitimate
social opportunity for the brand.

Do NOT generate posts, captions, taglines or creative concepts.
Return exactly 5 distinct opportunities.

Prefer specific timely trends over generic statements. Do not force
brand connections. Do not invent sponsorships, partnerships or claims.
Lower confidence when evidence is weak. Rank opportunities strongest
to weakest. Evidence must contain concise factual observations.
"""

    client = genai.Client(api_key=key)
    response = await client.aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            response_mime_type="application/json",
            response_schema=SensorOutput,
            temperature=0.2,
        ),
    )

    print(response)

    parsed = response.parsed
    if parsed is None:
        parsed = SensorOutput.model_validate(json.loads(response.text))

    sources = []
    try:
        chunks = response.candidates[0].grounding_metadata.grounding_chunks or []
        for chunk in chunks:
            web = getattr(chunk, "web", None)
            if web and getattr(web, "uri", None):
                sources.append({
                    "title": getattr(web, "title", "") or "",
                    "url": web.uri
                })
    except Exception:
        pass

    return {"insights": parsed.model_dump(), "sources": sources}
