from crewai import Crew, LLM, Process

from marketing_agent.agents.calendar_agent import build_calendar_agent
from marketing_agent.agents.copywriter_agent import build_copywriter_agent
from marketing_agent.agents.intake_agent import build_intake_agent
from marketing_agent.agents.publisher_agent import build_publisher_agent
from marketing_agent.agents.strategy_agent import build_strategy_agent
from marketing_agent.config import settings
from marketing_agent.tasks.calendar_tasks import build_calendar_task
from marketing_agent.tasks.copywriter_tasks import build_copywriter_task
from marketing_agent.tasks.intake_tasks import build_intake_task
from marketing_agent.tasks.publisher_tasks import build_publisher_task
from marketing_agent.tasks.strategy_tasks import build_strategy_task


def _resolve_llm() -> LLM:
    """Return a CrewAI LLM instance based on LLM_PROVIDER env var."""
    if settings.llm_provider == "ollama":
        return LLM(
            model=f"ollama/{settings.ollama_model}",
            base_url=settings.ollama_base_url,
        )
    if settings.llm_provider == "gemini":
        return LLM(model="gemini/gemini-1.5-flash", api_key=settings.google_api_key)
    return LLM(model="claude-haiku-4-5-20251001", api_key=settings.anthropic_api_key)


def build_generation_crew(company_name: str) -> Crew:
    """
    The main content generation pipeline: Intake → Strategy → Calendar → Copywriter.

    Does NOT include the Publisher Agent. Publishing is a separate crew
    invoked only after explicit human approval via cli.py.
    """
    llm = _resolve_llm()

    intake = build_intake_agent(llm)
    strategy = build_strategy_agent(llm)
    calendar = build_calendar_agent(llm)
    copywriter = build_copywriter_agent(llm)

    intake_task = build_intake_task(intake, company_name)
    strategy_task = build_strategy_task(strategy, brand_brief_json="{intake_output}")
    calendar_task = build_calendar_task(calendar, strategy_json="{strategy_output}")
    copy_task = build_copywriter_task(
        copywriter,
        calendar_slot_json="{calendar_output}",
        brand_brief_json="{intake_output}",
    )

    return Crew(
        agents=[intake, strategy, calendar, copywriter],
        tasks=[intake_task, strategy_task, calendar_task, copy_task],
        process=Process.sequential,
        verbose=True,
    )


def build_publish_crew(post_json: str, slot_json: str) -> Crew:
    """
    Publishing crew for a single approved post.

    Only call this after confirming post.approved == True.
    The caller (cli.py publish command) is responsible for this check.
    """
    llm = _resolve_llm()
    publisher = build_publisher_agent(llm)
    publish_task = build_publisher_task(publisher, post_json=post_json, slot_json=slot_json)

    return Crew(
        agents=[publisher],
        tasks=[publish_task],
        process=Process.sequential,
        verbose=True,
    )
