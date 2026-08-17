import asyncio
import httpx


BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


async def search_gdelt(
    query: str,
    max_records: int = 50,
    retries: int = 2
):

    params = {
        "query": query,
        "mode": "artlist",
        "maxrecords": max_records,
        "format": "json",
        "sort": "datedesc",
    }

    for attempt in range(retries + 1):

        try:

            async with httpx.AsyncClient(
                timeout=20,
                headers={
                    "User-Agent": "FMCG-Social-Sensor/0.1"
                }
            ) as client:

                response = await client.get(
                    BASE_URL,
                    params=params
                )

                # ---------------------------------
                # Rate limited
                # ---------------------------------

                if response.status_code == 429:

                    if attempt < retries:

                        wait_time = 2 ** attempt

                        await asyncio.sleep(
                            wait_time
                        )

                        continue

                    # Don't crash the entire sensor
                    return []

                response.raise_for_status()

                data = response.json()

                articles = []

                for item in data.get(
                    "articles",
                    []
                ):

                    articles.append({

                        "source":
                            item.get(
                                "domain",
                                ""
                            ),

                        "title":
                            item.get(
                                "title",
                                ""
                            ),

                        "description":
                            "",

                        "url":
                            item.get(
                                "url",
                                ""
                            ),

                        "published_at":
                            item.get(
                                "seendate",
                                ""
                            )
                    })

                return articles

        except (
            httpx.HTTPError,
            ValueError
        ):

            if attempt < retries:

                await asyncio.sleep(
                    2 ** attempt
                )

            else:

                return []

    return []