from datetime import datetime, timezone

from app.collectors.news import search_news
from app.collectors.gdelt import search_gdelt

from app.analytics.signals import (
    sentiment_score,
    growth_pct,
    opportunity_score
)

from app.ai.insights import generate_insight


async def run_sensor(request):

    # ==================================================
    # 1. USER INPUT
    # ==================================================

    brand = request.brand
    category = request.category
    market = request.market
    language = request.language

    print(
        f"\nStarting Social Sensor for "
        f"{brand} | {category}"
    )

    # ==================================================
    # 2. BUILD A BROAD SEARCH QUERY
    #
    # We intentionally DON'T ask the user for:
    # - FIFA
    # - substitutions
    # - campaigns
    # - viral moments
    #
    # Those should be discovered by the sensor.
    # ==================================================

    query = (
        f'"{brand}" OR '
        f'"{category}"'
    )

    print(
        f"Search query: {query}"
    )

    # ==================================================
    # 3. NEWSAPI
    # ==================================================

    print(
        "Fetching NewsAPI..."
    )

    try:

        news, news_meta = await search_news(
            query,
            request.lookback_days
        )

        print(news)

    except Exception as error:

        print(
            f"NewsAPI failed: {error}"
        )

        news = []

        news_meta = {
            "enabled": False,
            "error": str(error),
            "total_results": 0
        }

    print(
        f"NewsAPI complete: "
        f"{len(news)} articles"
    )

    # ==================================================
    # 4. GDELT
    # ==================================================

    print(
        "Fetching GDELT..."
    )

    gdelt = await search_gdelt(
        query,
        max_records=30
    )

    print(
        f"GDELT complete: "
        f"{len(gdelt)} articles"
    )

    # ==================================================
    # 5. SOURCE STATUS
    # ==================================================

    gdelt_status = {

        "enabled": True,

        "articles": len(
            gdelt
        )
    }

    # ==================================================
    # 6. COMBINE DATA
    # ==================================================

    combined = (
        news +
        gdelt
    )

    # ==================================================
    # 7. REMOVE DUPLICATES
    # ==================================================

    unique_articles = []

    seen = set()

    for article in combined:

        url = article.get(
            "url",
            ""
        )

        title = article.get(
            "title",
            ""
        )

        identifier = (
            url or title
        )

        if not identifier:
            continue

        if identifier in seen:
            continue

        seen.add(
            identifier
        )

        unique_articles.append(
            article
        )

    combined = unique_articles

    # ==================================================
    # 8. SENTIMENT
    # ==================================================

    texts = [

        (
            article.get(
                "title",
                ""
            )
            + " "
            +
            article.get(
                "description",
                ""
            )
        )

        for article in combined

        if article.get(
            "title"
        )
    ]

    mentions = len(
        combined
    )

    sentiment = sentiment_score(
        texts
    )

    # ==================================================
    # 9. TEMPORARY VELOCITY
    #
    # This will eventually be replaced by a database
    # containing historical observations.
    # ==================================================

    baseline = max(
        mentions // 4,
        1
    )

    velocity = growth_pct(
        mentions,
        baseline
    )

    # ==================================================
    # 10. INITIAL RELEVANCE SCORES
    #
    # LLM will perform deeper interpretation.
    # ==================================================

    brand_relevance = 80

    event_relevance = 70

    score = opportunity_score(
        velocity,
        sentiment,
        brand_relevance,
        event_relevance
    )

    # ==================================================
    # 11. PREPARE LLM CONTEXT
    # ==================================================

    context = {

        "brand": brand,

        "category": category,

        "market": market,

        "language": language,

        "signals": {

            "mention_volume":
                mentions,

            "mention_velocity_pct":
                velocity,

            "sentiment":
                sentiment,

            "opportunity_score":
                score,

            "news": news_meta,

            "gdelt": gdelt_status
        },

        "source_distribution": {

            "newsapi":
                len(news),

            "gdelt":
                len(gdelt)
        },

        "recent_evidence":
            combined[:30]
    }

    # ==================================================
    # 12. LLM ANALYSIS
    # ==================================================

    print(
        "Sending signals to LLM..."
    )

    insight = await generate_insight(
        context
    )

    print(
        "LLM analysis complete."
    )

    # ==================================================
    # 13. FINAL API RESPONSE
    # ==================================================

    return {

        "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "brand":
            brand,

        "category":
            category,

        "market":
            market,

        "signal": {

            "mention_volume":
                mentions,

            "mention_velocity_pct":
                velocity,

            "sentiment":
                sentiment,

            "opportunity_score":
                score
        },

        "sources": {

            "newsapi":
                len(news),

            "gdelt":
                len(gdelt)
        },

        "insights":
            insight
    }