import json

import httpx
from crewai.tools import BaseTool

from marketing_agent.config import settings


class PostizScheduleTool(BaseTool):
    name: str = "postiz_schedule"
    description: str = (
        "Schedule a post to a social platform via the self-hosted Postiz API. "
        "Input must be a JSON string with: platform (string), content (string), "
        "scheduled_at (ISO 8601 datetime string), and optionally media_url (string)."
    )

    def _run(self, input_json: str) -> str:
        data = json.loads(input_json)
        payload = {
            "type": data["platform"],
            "content": data["content"],
            "date": data["scheduled_at"],
        }
        if "media_url" in data:
            payload["media"] = [{"url": data["media_url"]}]

        response = httpx.post(
            f"{settings.postiz_base_url}/api/posts",
            json=payload,
            headers={
                "Authorization": f"Bearer {settings.postiz_api_key}",
                "Content-Type": "application/json",
            },
            timeout=30,
        )
        response.raise_for_status()
        return json.dumps(response.json())
