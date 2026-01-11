# -*- coding: utf-8 -*-
"""
FastAPI application for Local Prompt Agent.

Simple REST API following Rule #1: Keep it simple.
"""

from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from local_prompt_agent import __version__
from local_prompt_agent.agent import Agent
from local_prompt_agent.config import load_config


class ChatRequest(BaseModel):
    """Chat request model."""

    message: str
    agent: str = "default"
    stream: bool = False


class ChatResponse(BaseModel):
    """Chat response model."""

    response: str
    model: str
    agent: str = "default"


def create_app(config_path: Optional[Path] = None) -> FastAPI:
    """
    Create FastAPI application.

    Args:
        config_path: Path to config file

    Returns:
        FastAPI app instance
    """
    app = FastAPI(
        title="Local Prompt Agent",
        description="Privacy-first local AI assistant API",
        version=__version__,
    )

    # CORS middleware (allow all for local development)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Load config
    config = load_config(config_path)

    # Initialize agent
    agent = Agent(config)

    # Serve static files
    static_dir = Path(__file__).parent.parent / "web" / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def root() -> str:
        """Serve web UI."""
        html_file = Path(__file__).parent.parent / "web" / "index.html"
        if html_file.exists():
            with open(html_file, "r", encoding="utf-8") as f:
                return f.read()
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Local Prompt Agent</title>
        </head>
        <body>
            <h1>Local Prompt Agent API</h1>
            <p>Visit <a href="/docs">/docs</a> for API documentation</p>
        </body>
        </html>
        """

    @app.get("/health")
    async def health() -> dict[str, Any]:
        """Health check endpoint."""
        backend_healthy = await agent.health_check()
        return {
            "status": "healthy" if backend_healthy else "unhealthy",
            "backend": config.backend.type,
            "model": config.backend.model,
            "version": __version__,
        }

    @app.post("/api/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest) -> ChatResponse:
        """
        Chat endpoint.

        Execute a prompt and return response.
        """
        try:
            response = await agent.execute(request.message)
            return ChatResponse(
                response=response,
                model=config.backend.model,
                agent=request.agent,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.websocket("/ws/chat")
    async def websocket_chat(websocket: WebSocket) -> None:
        """
        WebSocket endpoint for streaming chat.

        Streams responses token by token.
        """
        await websocket.accept()

        try:
            while True:
                # Receive message
                data = await websocket.receive_json()
                message = data.get("message", "")

                if not message:
                    continue

                # Stream response
                try:
                    async for token in agent.stream(message):
                        await websocket.send_json({"type": "token", "token": token})

                    # Send done signal
                    await websocket.send_json({"type": "done"})

                except Exception as e:
                    await websocket.send_json({"type": "error", "error": str(e)})

        except WebSocketDisconnect:
            pass

    @app.post("/api/clear")
    async def clear_history() -> dict[str, str]:
        """Clear conversation history."""
        agent.clear_history()
        return {"status": "ok", "message": "History cleared"}

    @app.get("/api/config")
    async def get_config() -> dict[str, Any]:
        """Get current configuration."""
        return {
            "backend": {
                "type": config.backend.type,
                "model": config.backend.model,
                "temperature": config.backend.temperature,
                "max_tokens": config.backend.max_tokens,
            },
            "system": {
                "language": config.system.language,
                "theme": config.system.theme,
            },
        }

    return app


# For running with uvicorn
app = create_app()

# Add middleware for UTF-8 (critical for Chinese)
@app.middleware("http")
async def add_charset_middleware(request, call_next):
    """Ensure UTF-8 in all responses."""
    response = await call_next(request)

    # Add charset to Content-Type if not present
    content_type = response.headers.get("content-type", "")
    if content_type and "charset" not in content_type.lower():
        if "application/json" in content_type:
            response.headers["content-type"] = "application/json; charset=utf-8"
        elif "text/html" in content_type:
            response.headers["content-type"] = "text/html; charset=utf-8"

    return response
