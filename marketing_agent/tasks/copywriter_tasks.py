from crewai import Agent, Task


def build_copywriter_task(
    agent: Agent, calendar_slot_json: str, brand_brief_json: str
) -> Task:
    """
    Draft post copy for a single calendar slot.
    Output: a JSON-serialisable Post dict.
    """
    return Task(
        description=(
            "Write post copy for the following calendar slot. Stay strictly within "
            "the brand tone defined in the BrandBrief. Use sensory, evocative "
            "language appropriate for F&B content. Include relevant hashtags "
            "(mix of niche, local, and broad). Provide a media prompt that "
            "describes exactly what visual (photo or video) should accompany "
            "this post.\n\n"
            f"Calendar Slot:\n{calendar_slot_json}\n\n"
            f"BrandBrief:\n{brand_brief_json}"
        ),
        expected_output=(
            "A JSON object matching the Post schema with these fields: "
            "slot_id (UUID string), copy (string, the full caption), "
            "hashtags (list of strings, without # prefix), "
            "media_prompt (string describing the visual to produce), "
            "approved (false)."
        ),
        agent=agent,
    )
