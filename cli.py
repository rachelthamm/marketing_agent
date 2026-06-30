import json

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(name="marketing-agent", help="F&B AI Marketing Agent CLI")
console = Console()


@app.command()
def run(
    company_name: str = typer.Argument(..., help="F&B business name to run intake for"),
    weeks: int = typer.Option(4, help="Number of weeks to generate the calendar for"),
) -> None:
    """Run the full content generation pipeline (Intake → Strategy → Calendar → Copy)."""
    from marketing_agent.crew import build_generation_crew

    console.print(f"\n[bold green]Starting pipeline for:[/bold green] {company_name}")
    console.print(f"Calendar length: {weeks} weeks\n")

    crew = build_generation_crew(company_name)
    result = crew.kickoff()

    console.print("\n[bold green]Pipeline complete.[/bold green]")
    console.print(result)


@app.command()
def review() -> None:
    """List all posts pending human approval."""
    from marketing_agent.db import get_client

    db = get_client()
    result = (
        db.table("posts")
        .select("id, slot_id, copy, hashtags, approved, created_at")
        .eq("approved", False)
        .order("created_at")
        .execute()
    )

    posts = result.data
    if not posts:
        console.print("[yellow]No posts pending approval.[/yellow]")
        raise typer.Exit()

    table = Table(title="Posts Pending Approval", show_lines=True)
    table.add_column("ID", style="dim", width=36)
    table.add_column("Copy", max_width=60)
    table.add_column("Hashtags", max_width=30)
    table.add_column("Created", width=20)

    for post in posts:
        hashtags = ", ".join(post.get("hashtags") or [])
        table.add_row(
            post["id"],
            post["copy"][:120] + ("…" if len(post["copy"]) > 120 else ""),
            hashtags[:80],
            post.get("created_at", "")[:19],
        )

    console.print(table)
    console.print(f"\n[bold]{len(posts)} post(s) awaiting approval.[/bold]")
    console.print("Run [cyan]marketing-agent publish <POST_ID>[/cyan] to approve and schedule.")


@app.command()
def publish(
    post_id: str = typer.Argument(..., help="UUID of the approved post to publish"),
) -> None:
    """Approve and publish a single post to Postiz."""
    from marketing_agent.db import get_client
    from marketing_agent.crew import build_publish_crew

    db = get_client()

    post_result = db.table("posts").select("*").eq("id", post_id).single().execute()
    if not post_result.data:
        console.print(f"[red]Post {post_id} not found.[/red]")
        raise typer.Exit(1)

    post = post_result.data
    if post.get("approved"):
        console.print(f"[yellow]Post {post_id} is already approved and scheduled.[/yellow]")
        raise typer.Exit()

    slot_result = (
        db.table("calendar_slots").select("*").eq("id", post["slot_id"]).single().execute()
    )
    if not slot_result.data:
        console.print(f"[red]Calendar slot for post {post_id} not found.[/red]")
        raise typer.Exit(1)

    console.print(f"\n[bold]Post copy:[/bold]\n{post['copy']}\n")
    console.print(f"[bold]Hashtags:[/bold] {', '.join(post.get('hashtags') or [])}")
    console.print(f"[bold]Media prompt:[/bold] {post.get('media_prompt', '')}\n")

    confirmed = typer.confirm("Approve and schedule this post?")
    if not confirmed:
        console.print("[yellow]Cancelled.[/yellow]")
        raise typer.Exit()

    db.table("posts").update({"approved": True}).eq("id", post_id).execute()

    crew = build_publish_crew(
        post_json=json.dumps(post),
        slot_json=json.dumps(slot_result.data),
    )
    result = crew.kickoff()

    console.print("\n[bold green]Post scheduled successfully.[/bold green]")
    console.print(result)


if __name__ == "__main__":
    app()
