from crewai import Agent, Task


def build_calendar_task(agent: Agent, strategy_json: str, weeks: int = 4) -> Task:
    """
    Generate a posting calendar from an approved Strategy.
    Output: a list of JSON-serialisable CalendarSlot dicts.
    """
    return Task(
        description=(
            f"Using the approved marketing strategy below, create a {weeks}-week "
            "posting calendar. Each slot must specify: the date and time to post, "
            "the platform, which content pillar it serves, the post format "
            "(carousel, reel, story, static, or text), and a one-sentence brief "
            "describing the post concept. Distribute pillars evenly across the "
            "schedule. Account for F&B-relevant timing (e.g. Friday posts for "
            "weekend specials, lunchtime posts for midweek offers).\n\n"
            f"Strategy:\n{strategy_json}"
        ),
        expected_output=(
            "A JSON array of CalendarSlot objects. Each object must have: "
            "strategy_id (UUID string), slot_date (ISO 8601 datetime string), "
            "platform (one of: instagram, facebook, tiktok, twitter, linkedin), "
            "pillar (string), format (one of: carousel, reel, story, static, text), "
            "brief (string), status ('pending')."
        ),
        agent=agent,
    )
