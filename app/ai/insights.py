import json
import httpx

from app.config import (
    OLLAMA_URL,
    OLLAMA_MODEL
)


def fallback_insight(payload):

    brand = payload.get(
        "brand",
        ""
    )

    category = payload.get(
        "category",
        ""
    )

    signals = payload.get(
        "signals",
        {}
    )

    score = signals.get(
        "opportunity_score",
        0
    )

    return {

        "summary":
            f"Monitoring signals for "
            f"{brand} in the {category} category.",

        "signals": [

            {
                "signal_type":
                    "consumer_conversation",

                "topic":
                    category,

                "opportunity_score":
                    score,

                "confidence":
                    "LOW",

                "insight":
                    "Insufficient AI analysis available."
            }
        ],

        "overall_assessment": {

            "opportunity_score":
                score,

            "urgency":
                "MEDIUM",

            "recommendation":
                "Continue monitoring emerging conversations."
        }
    }


async def generate_insight(
    payload
):

    # ==================================================
    # LLM PROMPT
    # ==================================================

    prompt = f"""
You are an FMCG social intelligence analyst.

Your job is to analyze online signals around a brand
and identify important consumer and cultural opportunities.

IMPORTANT:

The user has ONLY provided:

- Brand
- Category
- Market

You must DISCOVER potential signals from the evidence.

Do NOT assume that the user supplied an event.

Possible signal types include:

1. emerging_trend
2. real_time_moment
3. consumer_conversation
4. cultural_event
5. competitor_activity
6. product_conversation
7. brand_reputation
8. campaign_activity

A real-time moment could be something such as:

- sports event
- celebrity moment
- breaking news
- cultural event
- viral incident
- festival
- live broadcast moment

But ONLY classify something as a real-time moment
if the supplied evidence supports it.

Do NOT invent facts.

Do NOT create:

- captions
- social media posts
- image concepts
- ad copy
- creative briefs

We are ONLY generating intelligence.

Return ONLY valid JSON.

Use this structure:

{{
    "summary": "...",

    "signals": [

        {{
            "signal_type": "...",

            "topic": "...",

            "evidence": [
                "..."
            ],

            "consumer_reaction": "...",

            "brand_relevance": 0,

            "opportunity_score": 0,

            "confidence": "LOW|MEDIUM|HIGH",

            "insight": "..."
        }}
    ],

    "overall_assessment": {{

        "opportunity_score": 0,

        "urgency": "LOW|MEDIUM|HIGH",

        "recommendation": "..."
    }}
}}

DATA:

{json.dumps(
    payload,
    indent=2
)}
"""

    body = {

        "model":
            OLLAMA_MODEL,

        "prompt":
            prompt,

        "stream":
            False,

        "format":
            "json"
    }

    # ==================================================
    # CALL OLLAMA
    # ==================================================

    try:

        async with httpx.AsyncClient(
            timeout=120
        ) as client:

            response = await client.post(
                OLLAMA_URL,
                json=body
            )

            response.raise_for_status()

            result = response.json()

            return json.loads(
                result["response"]
            )

    except Exception as error:

        print(
            f"LLM unavailable: {error}"
        )

        return fallback_insight(
            payload
        )