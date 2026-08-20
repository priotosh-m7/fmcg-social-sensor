from datetime import datetime, timezone
from app.ai.insights import generate_insight

async def run_sensor(request):
    context = {
        "brand": request.brand,
        "category": request.category,
        "market": request.market,
        "language": request.language,
        "lookback_days": request.lookback_days,
    }
    result = await generate_insight(context)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "brand": request.brand,
        "category": request.category,
        "market": request.market,
        "lookback_days": request.lookback_days,
        "insights": result["insights"],
        "sources": result.get("sources", []),
    }
