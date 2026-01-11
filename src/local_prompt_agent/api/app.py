# -*- coding: utf-8 -*-
"""
FastAPI application for Local Prompt Agent.

Simple REST API following Rule #1: Keep it simple.
"""

from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile, WebSocket, WebSocketDisconnect
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
                use_rag = data.get("use_rag", False)

                if not message:
                    continue

                # Enable/disable RAG based on request
                if use_rag:
                    try:
                        agent.enable_rag()
                    except Exception:
                        pass  # RAG dependencies not installed
                else:
                    agent.disable_rag()

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

    @app.post("/api/rag/query")
    async def rag_query(question: str, k: int = 5) -> dict[str, Any]:
        """
        Query RAG system.

        Args:
            question: User's question
            k: Number of chunks to retrieve
        """
        try:
            from local_prompt_agent.rag.simple_rag import SimpleRAG

            rag_system = SimpleRAG()
            result = rag_system.query(question, k=k)

            if not result["has_results"]:
                return {
                    "success": False,
                    "message": "No documents indexed yet",
                }

            # Generate answer with RAG context
            agent.enable_rag()
            answer = await agent.execute(question, use_history=False)

            return {
                "success": True,
                "question": question,
                "answer": answer,
                "sources": result["sources"],
                "num_chunks": result["num_results"],
            }

        except ImportError:
            raise HTTPException(
                status_code=501,
                detail="RAG dependencies not installed",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/rag/documents")
    async def rag_list_documents() -> dict[str, Any]:
        """List all indexed documents."""
        try:
            from local_prompt_agent.rag.simple_rag import SimpleRAG

            rag_system = SimpleRAG()
            docs = rag_system.list_documents()

            return {
                "success": True,
                "documents": docs,
                "count": len(docs),
            }

        except ImportError:
            raise HTTPException(
                status_code=501,
                detail="RAG dependencies not installed",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/rag/upload")
    async def rag_upload_pdf(file: UploadFile = File(...)) -> dict[str, Any]:
        """
        Upload and index a PDF document.

        Args:
            file: Uploaded PDF file

        Returns:
            Indexing result
        """
        try:
            from local_prompt_agent.rag import RAGSystem
            import tempfile
            import shutil
            import asyncio
            from concurrent.futures import ThreadPoolExecutor

            # Validate file type
            if not file.filename.endswith('.pdf'):
                raise HTTPException(
                    status_code=400,
                    detail="Only PDF files are supported"
                )

            # Save uploaded file to temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = Path(tmp.name)

            # Run indexing in thread pool to avoid blocking
            def index_in_thread():
                # Use SimpleRAG (fast, no heavy models!)
                from local_prompt_agent.rag.simple_rag import SimpleRAG
                rag_system = SimpleRAG()
                return rag_system.index_document(tmp_path)

            # Execute in thread pool
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                result = await loop.run_in_executor(executor, index_in_thread)

            # Clean up temp file
            try:
                tmp_path.unlink()
            except:
                pass

            return {
                "success": True,
                "message": "Document indexed successfully",
                "file_name": file.filename,
                "num_chunks": result["num_chunks"],
                "page_count": result["page_count"],
            }

        except ImportError:
            raise HTTPException(
                status_code=501,
                detail="RAG dependencies not installed. "
                "Install: pip install pdfplumber sentence-transformers chromadb"
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/rag/generate-prompts")
    async def rag_generate_prompts(doc_name: str, num_prompts: int = 5) -> dict[str, Any]:
        """
        Generate suggested prompts/questions for a document.

        Args:
            doc_name: Document file name
            num_prompts: Number of prompts to generate

        Returns:
            Generated prompts
        """
        try:
            from local_prompt_agent.rag.simple_rag import SimpleRAG

            rag_system = SimpleRAG()
            
            # Get document summary
            summary = rag_system.get_document_summary(doc_name, num_chunks=10)
            
            if not summary:
                return {
                    "success": False,
                    "message": f"Document not found: {doc_name}",
                }

            # Generate prompts using agent
            prompt = f"""Based on this document excerpt, generate {num_prompts} interesting and specific questions that someone might want to ask about the full document.

Document excerpt:
{summary[:3000]}

Generate exactly {num_prompts} questions. Format as a numbered list.
Make questions specific, useful, and diverse (cover different aspects).
"""
            
            response = await agent.execute(prompt, use_history=False)
            
            return {
                "success": True,
                "doc_name": doc_name,
                "prompts": response,
                "num_prompts": num_prompts,
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

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
