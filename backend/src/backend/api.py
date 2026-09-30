from collections.abc import AsyncIterable
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.sse import EventSourceResponse, ServerSentEvent
from netra import Netra
from netra.decorators import agent
from pydantic import BaseModel, Field

from backend.agent import clear_thread, get_agent
from backend.db import get_db
from backend.observability import init_netra, shutdown_netra


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_netra()
    yield
    shutdown_netra()


app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    message: str = Field(description="The user message to send to the agent")
    thread_id: str = Field(default="default", description="Conversation thread identifier")


@agent(name="Daisy")
async def stream_tokens(request: ChatRequest) -> AsyncIterable[ServerSentEvent]:
    agent = get_agent()
    config = {"configurable": {"thread_id": request.thread_id}}
    Netra.set_root_input(request.message)
    Netra.set_session_id(request.thread_id)
    collected: list[str] = []
    async for event in agent.astream_events(
        {"messages": [{"role": "user", "content": request.message}]},
        config=config,
        version="v2",
    ):
        if event["event"] != "on_chat_model_stream":
            continue
        chunk = event["data"]["chunk"]
        content = getattr(chunk, "content", None)
        if not content:
            continue
        collected.append(content)
        yield ServerSentEvent(data={"token": content}, event="token")
    Netra.set_root_output("".join(collected))
    yield ServerSentEvent(data={"done": True}, event="done")


@app.post("/chat", response_class=EventSourceResponse)
async def chat(request: ChatRequest) -> AsyncIterable[ServerSentEvent]:
    async for event in stream_tokens(request):
        yield event


@app.delete("/chat/{thread_id}")
async def clear_chat(thread_id: str) -> dict:
    await clear_thread(thread_id)
    return {"cleared": True, "thread_id": thread_id}


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "db": get_db()}