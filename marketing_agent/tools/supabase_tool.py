import json
from typing import Any

from crewai.tools import BaseTool
from pydantic import Field

from marketing_agent.db import get_client


class SupabaseSaveTool(BaseTool):
    name: str = "supabase_save"
    description: str = (
        "Save a JSON record to a Supabase table. "
        "Input must be a JSON string with 'table' (string) and 'record' (object) keys."
    )

    def _run(self, input_json: str) -> str:
        data = json.loads(input_json)
        table: str = data["table"]
        record: dict[str, Any] = data["record"]
        result = get_client().table(table).insert(record).execute()
        return json.dumps(result.data)


class SupabaseReadTool(BaseTool):
    name: str = "supabase_read"
    description: str = (
        "Read records from a Supabase table with optional filters. "
        "Input must be a JSON string with 'table' (string) and optional "
        "'filters' (list of [column, operator, value] triples)."
    )

    def _run(self, input_json: str) -> str:
        data = json.loads(input_json)
        table: str = data["table"]
        filters: list[list[str]] = data.get("filters", [])
        query = get_client().table(table).select("*")
        for col, op, val in filters:
            query = query.filter(col, op, val)
        result = query.execute()
        return json.dumps(result.data)
