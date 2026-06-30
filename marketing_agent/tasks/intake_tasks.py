from crewai import Agent, Task


def build_intake_task(agent: Agent, company_name: str) -> Task:
    """
    Conduct a structured brand intake interview for an F&B business.
    Output: a JSON-serialisable BrandBrief dict.
    """
    return Task(
        description=(
            f"Conduct a structured brand intake for '{company_name}', an F&B business. "
            "Gather information about their products and menu offerings, target audience "
            "(dine-in, takeaway, delivery, events), brand tone and personality, "
            "marketing goals (e.g. increase foot traffic, build online following, "
            "launch a new menu), any constraints (budget, seasonal closures, "
            "platforms they want to avoid), and key local competitors. "
            "Return a complete BrandBrief as a JSON object."
        ),
        expected_output=(
            "A JSON object matching the BrandBrief schema with these fields: "
            "company_name (string), industry (string, default 'food_and_beverage'), "
            "products (list of strings), target_audience (string), tone (string), "
            "goals (list of strings), constraints (list of strings), "
            "competitors (list of strings)."
        ),
        agent=agent,
    )
