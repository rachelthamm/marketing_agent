from crewai import Agent


def build_publisher_agent(llm: str) -> Agent:
    """
    Publisher Agent.

    Pushes a single approved post to Postiz for scheduled publishing.

    IMPORTANT: This agent must NEVER be instantiated in a crew without
    confirming that post.approved == True. The human approval gate in
    cli.py is the only authorised trigger for this agent. No code path
    may bypass this check in v1.
    """
    return Agent(
        role="Social Media Publisher",
        goal=(
            "Schedule an approved post to the correct platform via Postiz "
            "and confirm successful scheduling back to the caller."
        ),
        backstory=(
            "You are responsible for the final, irreversible step of publishing "
            "content to a client's social accounts. You only ever act on posts "
            "that have been explicitly approved by a human reviewer. You confirm "
            "each scheduling action and surface any errors immediately."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
