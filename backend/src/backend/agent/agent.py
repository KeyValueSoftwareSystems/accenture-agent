from functools import lru_cache

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from pydantic import SecretStr

from backend.agent.prompt import SYSTEM_PROMPT
from backend.agent.tools import TOOLS
from backend.settings import get_settings

_checkpointer = MemorySaver()


@lru_cache
def get_agent():
    settings = get_settings()
    model = ChatOpenAI(
        model=settings.model,
        api_key=SecretStr(settings.openai_api_key),
        base_url=settings.openai_base_url,
    )
    return create_agent(
        model=model,
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=_checkpointer,
    )


async def clear_thread(thread_id: str) -> None:
    await _checkpointer.adelete_thread(thread_id)