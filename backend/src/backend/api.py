from collections.abc import AsyncIterable

from fastapi import FastAPI
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel, Field

from backend.agent import clear_thread, get_agent
from backend.db import get_db

app = FastAPI()


class ChatRequest(BaseModel):
    message: str = Field(description="The user message to send to the agent")
    thread_id: str = Field(default="default", description="Conversation thread identifier")


async def stream_tokens(request: ChatRequest) -> AsyncIterable[ServerSentEvent]:
    agent = get_agent()
    config = {"configurable": {"thread_id": request.thread_id}}
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
        yield ServerSentEvent(data={"token": content}, event="token")
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