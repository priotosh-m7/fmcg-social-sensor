import httpx
from app.config import NEWS_API_KEY

BASE_URL = "https://newsapi.org/v2/everything"

async def search_news(query: str, days: int = 7, page_size: int = 50):
    if not NEWS_API_KEY:
        return [], {"enabled": False, "error": "NEWS_API_KEY not configured"}

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

    articles = []
    for item in data.get("articles", []):
        articles.append({
            "source": (item.get("source") or {}).get("name", ""),
            "title": item.get("title", "") or "",
            "description": item.get("description", "") or "",
            "url": item.get("url", "") or "",
            "published_at": item.get("publishedAt", "") or "",
        })

    return articles, {"enabled": True, "total_results": data.get("totalResults", 0)}
