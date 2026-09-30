from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from pydantic import SecretStr

from backend.agent.prompt import get_system_prompt
from backend.agent.tools import TOOLS
from backend.settings import get_settings

_checkpointer = MemorySaver()

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
        system_prompt=get_system_prompt(),
        checkpointer=_checkpointer,
    )


async def clear_thread(thread_id: str) -> None:
    await _checkpointer.adelete_thread(thread_id)