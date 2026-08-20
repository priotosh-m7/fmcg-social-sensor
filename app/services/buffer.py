import os
import httpx


BUFFER_API_URL = "https://api.buffer.com"
from dotenv import load_dotenv

load_dotenv()
from app.config import (
   BUFFER_API_KEY,
   BUFFER_CHANNEL_ID
)

async def publish_to_buffer(
    image_url: str,
    caption: str,
    scheduled_at: str | None = None
):
    api_key = BUFFER_API_KEY
    channel_id = BUFFER_CHANNEL_ID

    if not api_key:
        raise RuntimeError("BUFFER_API_KEY is not configured")

    if not channel_id:
        raise RuntimeError("BUFFER_CHANNEL_ID is not configured")

    if scheduled_at:
        scheduling_type = "automatic"
        mode = "customScheduled"
    else:
        scheduling_type = "automatic"
        mode = "shareNow"
    
    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
        createPost(input: $input) {
            ... on PostActionSuccess {
                post {
                    id
                    text
                    dueAt
                    status
                    assets {
                        id
                        mimeType
                    }
                }
            }

            ... on MutationError {
                message
            }
        }
    }
    """

    post_input = {
        "channelId": channel_id,
        "text": caption,
        "schedulingType": scheduling_type,
        "mode": mode,
        "assets": [
            {
                "image": {
                    "url": image_url
                }
            }
        ],
        "metadata": {
            "instagram": {
                "type": "post",
                "shouldShareToFeed": True
            }
        }
    }

    if scheduled_at:
        post_input["dueAt"] = scheduled_at

    variables = {
        "input": post_input
    }


    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            BUFFER_API_URL,
            headers=headers,
            json={
                "query": mutation,
                "variables": variables,
            },
            timeout=30,
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

    result = data.get("data", {}).get("createPost", {})

    if "message" in result:
        raise RuntimeError(
            f"Buffer publishing error: {result['message']}"
        )

    return result

async def test_buffer_channel():

    api_key = BUFFER_API_KEY
    channel_id = BUFFER_CHANNEL_ID

    query = """
    query GetChannel($input: ChannelInput!) {
        channel(input: $input) {
            id
            name
            service
        }
    }
    """

    variables = {
        "input": {
            "id": channel_id
        }
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
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

    print("CHANNEL TEST:", response.json())

    return response.json()