from crewai import Agent


def build_intake_agent(llm: str) -> Agent:
    """
    Intake/Brand Agent.

    Interviews the F&B business owner via structured prompts and produces
    a validated BrandBrief. This is the pipeline entry point — all
    downstream agents depend on its output.
    """
    return Agent(
        role="Brand Intake Specialist",
        goal=(
            "Extract comprehensive brand information from the F&B business owner "
            "and produce a structured BrandBrief document."
        ),
        backstory=(
            "You are an expert brand strategist who has worked with hundreds of "
            "food and beverage businesses — from independent cafes and food trucks "
            "to regional restaurant chains and artisan producers. You know exactly "
            "what information is needed to build an effective marketing strategy "
            "for an F&B brand, and you ask the right questions to surface it."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
