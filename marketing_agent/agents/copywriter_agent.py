from crewai import Agent


def build_copywriter_agent(llm: str) -> Agent:
    """
    Copywriter Agent.

    Drafts post copy and hashtags for each calendar slot, staying strictly
    within the brand voice and tone defined in the BrandBrief.
    """
    return Agent(
        role="F&B Copywriter",
        goal=(
            "Write compelling, on-brand post copy and hashtags for each calendar "
            "slot that reflect the F&B brand's voice and drive engagement."
        ),
        backstory=(
            "You are a specialist F&B copywriter who understands that food "
            "content lives and dies on sensory language, authenticity, and "
            "community. You write captions that make people hungry, curious, "
            "or proud to be a regular. You never stray from the brand tone "
            "in the BrandBrief — if it says 'warm and approachable', you don't "
            "write corporate. You always provide a media prompt alongside copy "
            "so the client knows what visual to pair with each post."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
