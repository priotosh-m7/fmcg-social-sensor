import httpx

from app.config import BUFFER_API_KEY

BUFFER_API_URL = "https://api.buffer.com"


async def get_post_metrics(post_id: str):

    query = """
    query GetPostMetrics($input: PostInput!) {
        post(input: $input) {
            id
            text
            channelId
            status
            sentAt
            metrics {
                type
                name
                value
                unit
            }
            metricsUpdatedAt
        }
    }
    """

    variables = {
        "input": {
            "id": post_id
        }
    }

    headers = {
        "Authorization": f"Bearer {BUFFER_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            BUFFER_API_URL,
            headers=headers,
            json={
                "query": query,
                "variables": variables
            },
            timeout=30
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"Buffer HTTP error {response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    if "errors" in data:
        raise RuntimeError(
            f"Buffer GraphQL error: {data['errors']}"
        )

    return data["data"]["post"]