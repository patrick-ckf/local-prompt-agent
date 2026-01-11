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
@click.option("--rag/--no-rag", default=False, help="Enable RAG mode for documents")
@click.pass_context
def chat(
    ctx: click.Context, model: Optional[str], stream: bool, rag: bool
) -> None:
    """
    Start interactive chat session.

    開始互動式對話 / 开始交互式对话
    """
    config_path = ctx.obj.get("config_path")
    asyncio.run(_chat(config_path, model, stream, rag))


async def _chat(
    config_path: Optional[Path],
    model: Optional[str],
    stream: bool,
    rag: bool = False,
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

    # Enable RAG if requested
    if rag:
        try:
            agent.enable_rag()
            console.print("[green]✓ RAG mode enabled[/green]")
        except ImportError as e:
            console.print(
                f"[red]RAG dependencies not installed.[/red]\n"
                "[yellow]Install with:[/yellow] pip install pdfplumber sentence-transformers chromadb"
            )
            return
        except Exception as e:
            console.print(f"[yellow]Warning: Could not enable RAG: {e}[/yellow]")

    # Welcome message
    rag_status = "[green]✓ RAG Enabled[/green]" if rag else ""
    console.print(
        Panel.fit(
            "[bold blue]Local Prompt Agent[/bold blue]\n"
            f"Model: {config.backend.model}\n"
            f"Backend: {config.backend.type}\n"
            f"{rag_status}\n\n"
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
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
@click.pass_context
def serve(ctx: click.Context, host: str, port: int, reload: bool) -> None:
    """
    Start REST API server with Web UI.

    啟動 REST API 伺服器 / 启动 REST API 服务器
    """
    import uvicorn

    from local_prompt_agent.api import create_app

    console.print(
        Panel.fit(
            f"[bold blue]Starting Local Prompt Agent API[/bold blue]\n\n"
            f"API:    http://{host}:{port}\n"
            f"Web UI: http://{host}:{port}\n"
            f"Docs:   http://{host}:{port}/docs\n\n"
            "[dim]Press Ctrl+C to stop[/dim]",
            title="Server",
        )
    )

    # Get config path
    config_path = ctx.obj.get("config_path")

    # Create app
    app = create_app(config_path)

    # Run server
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )


@main.group()
def rag() -> None:
    """
    RAG commands for document processing.

    文檔處理命令 / 文档处理命令
    """
    pass


@rag.command("index")
@click.argument("file_path", type=click.Path(exists=True, path_type=Path))
def rag_index(file_path: Path) -> None:
    """Index a PDF document for RAG."""
    try:
        from local_prompt_agent.rag import RAGSystem

        rag_system = RAGSystem()
        result = rag_system.index_document(file_path)

        console.print(
            Panel(
                f"[bold green]✓ Document indexed successfully[/bold green]\n\n"
                f"File: {result['file_name']}\n"
                f"Pages: {result['page_count']}\n"
                f"Chunks: {result['num_chunks']}",
                title="Indexing Complete",
            )
        )
    except ImportError as e:
        console.print(
            f"[red]Error: {e}[/red]\n"
            "[yellow]Install RAG dependencies:[/yellow]\n"
            "  pip install pdfplumber sentence-transformers chromadb"
        )
    except Exception as e:
        console.print(f"[red]Error indexing document: {e}[/red]")


@rag.command("query")
@click.argument("question")
@click.option("-k", "--top-k", default=5, help="Number of chunks to retrieve")
def rag_query(question: str, top_k: int) -> None:
    """Query indexed documents."""
    try:
        from local_prompt_agent.rag import RAGSystem

        rag_system = RAGSystem()
        result = rag_system.query(question, k=top_k)

        if not result["has_results"]:
            console.print(
                "[yellow]No documents indexed yet.[/yellow]\n"
                "Index a document first:\n"
                "  lpa rag index your_document.pdf"
            )
            return

        console.print(Panel.fit(f"[bold]Question:[/bold] {question}", title="Query"))

        console.print("\n[bold]Retrieved Context:[/bold]\n")
        console.print(result["context"])

        console.print("\n[bold]Sources:[/bold]")
        for source in result["sources"]:
            console.print(f"  • {source['file']} ({source['chunks']} chunks)")

    except ImportError as e:
        console.print(f"[red]Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@rag.command("list")
def rag_list() -> None:
    """List all indexed documents."""
    try:
        from local_prompt_agent.rag import RAGSystem

        rag_system = RAGSystem()
        docs = rag_system.list_documents()

        if not docs:
            console.print("[yellow]No documents indexed yet.[/yellow]")
            return

        console.print(Panel.fit("[bold]Indexed Documents[/bold]", title="RAG"))

        for doc in docs:
            console.print(
                f"\n[bold]{doc['file_name']}[/bold]\n"
                f"  Path: {doc['file_path']}\n"
                f"  Pages: {doc['pages']}\n"
                f"  Chunks: {doc['chunks']}"
            )

    except ImportError as e:
        console.print(f"[red]Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


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
