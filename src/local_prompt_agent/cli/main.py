# -*- coding: utf-8 -*-
"""
CLI interface using Click and Rich.

Simple commands: chat, config, version
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from local_prompt_agent import __version__
from local_prompt_agent.agent import Agent
from local_prompt_agent.config import load_config

console = Console()


@click.group()
@click.version_option(version=__version__)
@click.option(
    "--config",
    type=click.Path(exists=True, path_type=Path),
    help="Config file path",
)
@click.pass_context
def main(ctx: click.Context, config: Optional[Path]) -> None:
    """
    Local Prompt Agent - Privacy-first AI assistant.

    本地提示代理 - 注重隐私的 AI 助手
    """
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config


@main.command()
@click.option("--model", help="Override model from config")
@click.option("--stream/--no-stream", default=True, help="Stream responses")
@click.pass_context
def chat(ctx: click.Context, model: Optional[str], stream: bool) -> None:
    """
    Start interactive chat session.

    開始互動式對話 / 开始交互式对话
    """
    config_path = ctx.obj.get("config_path")
    asyncio.run(_chat(config_path, model, stream))


async def _chat(
    config_path: Optional[Path],
    model: Optional[str],
    stream: bool,
) -> None:
    """Async chat implementation."""
    # Load config
    config = load_config(config_path)

    # Override model if specified
    if model:
        config.backend.model = model

    # Initialize agent
    try:
        agent = Agent(config)
    except Exception as e:
        console.print(f"[red]Error initializing agent: {e}[/red]")
        return

    # Welcome message
    console.print(
        Panel.fit(
            "[bold blue]Local Prompt Agent[/bold blue]\n"
            f"Model: {config.backend.model}\n"
            f"Backend: {config.backend.type}\n\n"
            "[dim]Type '/exit' to quit, '/clear' to clear history[/dim]",
            title="Welcome 歡迎 欢迎",
        )
    )

    # Check health
    console.print("[dim]Checking backend connection...[/dim]")
    if not await agent.health_check():
        console.print(
            "[red]Warning: Cannot connect to backend. "
            "Make sure Ollama is running![/red]"
        )
        return

    console.print("[green]✓ Connected to backend[/green]\n")

    # Chat loop
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]")

            if not user_input.strip():
                continue

            # Handle commands
            if user_input.startswith("/"):
                if user_input == "/exit" or user_input == "/quit":
                    console.print("[yellow]Goodbye! 再見! 再见![/yellow]")
                    break
                elif user_input == "/clear":
                    agent.clear_history()
                    console.print("[green]✓ History cleared[/green]")
                    continue
                elif user_input == "/help":
                    console.print(
                        "[bold]Commands:[/bold]\n"
                        "  /exit   - Quit\n"
                        "  /clear  - Clear history\n"
                        "  /help   - Show this help"
                    )
                    continue
                else:
                    console.print(f"[red]Unknown command: {user_input}[/red]")
                    continue

            # Get response
            console.print("[bold green]Assistant[/bold green]: ", end="")

            if stream:
                # Streaming response
                response_text = ""
                async for token in agent.stream(user_input):
                    console.print(token, end="")
                    response_text += token
                console.print()  # New line after streaming
            else:
                # Complete response
                response_text = await agent.execute(user_input)
                # Render as markdown
                md = Markdown(response_text)
                console.print(md)

            console.print()  # Empty line

        except KeyboardInterrupt:
            console.print("\n[yellow]Use /exit to quit[/yellow]")
            continue
        except EOFError:
            console.print("[yellow]Goodbye! 再見! 再见![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            continue


@main.command()
@click.pass_context
def config(ctx: click.Context) -> None:
    """Show current configuration."""
    config_path = ctx.obj.get("config_path")
    cfg = load_config(config_path)

    console.print(
        Panel(
            f"[bold]System:[/bold]\n"
            f"  Language: {cfg.system.language}\n"
            f"  Theme: {cfg.system.theme}\n"
            f"  Data Dir: {cfg.system.data_dir}\n\n"
            f"[bold]Backend:[/bold]\n"
            f"  Type: {cfg.backend.type}\n"
            f"  URL: {cfg.backend.base_url}\n"
            f"  Model: {cfg.backend.model}\n"
            f"  Temperature: {cfg.backend.temperature}\n"
            f"  Max Tokens: {cfg.backend.max_tokens}\n\n"
            f"[bold]Database:[/bold]\n"
            f"  URL: {cfg.database.url}",
            title="Configuration",
        )
    )


@main.command()
def version() -> None:
    """Show version information."""
    console.print(
        Panel.fit(
            f"[bold]Local Prompt Agent[/bold]\n"
            f"Version: {__version__}\n\n"
            "[dim]Privacy-first local AI assistant[/dim]\n"
            "[dim]本地提示代理 - 注重隐私的 AI 助手[/dim]",
            title="Version",
        )
    )


if __name__ == "__main__":
    main()
