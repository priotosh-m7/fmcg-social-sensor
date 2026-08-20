from app.ai.creative import generate_creative as generate_ai_creative


async def generate_creative(request):
    insight = {
        "rank": request.rank,
        "trend": request.trend,
        "what_is_happening": request.what_is_happening,
        "consumer_relevance": request.consumer_relevance,
        "brand_connection": request.brand_connection,
        "opportunity_score": request.opportunity_score,
        "urgency": request.urgency,
        "confidence": request.confidence,
        "timing": request.timing,
        "evidence": request.evidence
    }

    return await generate_ai_creative(
        request,
        insight
    )