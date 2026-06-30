from crewai import Agent, Task


def build_publisher_task(agent: Agent, post_json: str, slot_json: str) -> Task:
    """
    Publish a single approved post to Postiz.

    This task must only be created for posts where approved == True.
    The caller (cli.py) is responsible for enforcing this precondition.

    Output: a confirmation dict containing postiz_post_id and scheduled time.
    """
    return Task(
        description=(
            "Schedule the following approved post to its target platform via "
            "the Postiz API. Confirm successful scheduling and return the "
            "Postiz post ID and scheduled publish time.\n\n"
            f"Post:\n{post_json}\n\n"
            f"Calendar Slot (for platform and slot_date):\n{slot_json}"
        ),
        expected_output=(
            "A JSON object with: postiz_post_id (string), "
            "scheduled_at (ISO 8601 datetime string), "
            "platform (string), status ('scheduled')."
        ),
        agent=agent,
    )
