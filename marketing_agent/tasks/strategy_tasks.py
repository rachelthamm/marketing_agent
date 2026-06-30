from crewai import Agent, Task


def build_strategy_task(agent: Agent, brand_brief_json: str) -> Task:
    """
    Generate a marketing strategy from a BrandBrief.
    Output: a JSON-serialisable Strategy dict.
    """
    return Task(
        description=(
            "Using the following BrandBrief, develop a focused marketing strategy "
            "for this F&B business. For each decision — positioning statement, "
            "content pillar, channel choice, posting cadence, KPI — explain the "
            "reasoning so the client can review and correct it. Prioritise platforms "
            "that suit F&B visual content (Instagram, TikTok, Facebook) unless the "
            "brief indicates otherwise.\n\n"
            f"BrandBrief:\n{brand_brief_json}"
        ),
        expected_output=(
            "A JSON object matching the Strategy schema with these fields: "
            "brand_brief_id (UUID string), positioning (string), "
            "content_pillars (list of strings, each with a one-sentence rationale), "
            "channels (list of platform names), cadence (string, e.g. '3x per week'), "
            "kpis (list of strings)."
        ),
        agent=agent,
    )
