import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.schemas import CreativeOutput

load_dotenv()
from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GOOGLE_SEARCH_ENABLED
)

async def generate_creative(request, insight):

    key = GEMINI_API_KEY

    if not key:
        raise RuntimeError("GEMINI_API_KEY is missing.")

    prompt = f"""
You are an FMCG advertising strategist.

Create a social media advertisement concept based on the
following validated consumer opportunity.

Brand: {request.brand}
Category: {request.category}
Market: {request.market}
Format: {request.format}
Objective: {request.objective}

Opportunity rank: {insight["rank"]}
Trend: {insight["trend"]}

What is happening:
{insight["what_is_happening"]}

Consumer relevance:
{insight["consumer_relevance"]}

Brand connection:
{insight["brand_connection"]}

Opportunity score:
{insight["opportunity_score"]}

Urgency:
{insight["urgency"]}

Confidence:
{insight["confidence"]}

Timing:
{insight["timing"]}

Evidence:
{json.dumps(insight["evidence"])}

Generate:

1. A strong advertising headline
2. Short body copy
3. A clear CTA
4. 3-6 relevant hashtags
5. Creative direction
6. A detailed visual-generation prompt

The creative should be relevant to the identified trend
while remaining appropriate for the brand.

Do not invent statistics, partnerships, sponsorships,
product claims, or consumer research.

Do not generate the actual image.

Return only structured JSON.
"""

    client = genai.Client(api_key=key)

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=CreativeOutput
    )

    response = await client.aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=config
    )

    parsed = response.parsed

    if parsed is None:
        parsed = CreativeOutput.model_validate(
            json.loads(response.text)
        )

    return {
        "brand": request.brand,
        "category": request.category,
        "format": request.format,
        "creative": parsed.model_dump(),
        "source_insight": insight
    }