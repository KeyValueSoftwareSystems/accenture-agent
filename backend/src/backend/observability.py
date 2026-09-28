import os

from dotenv import load_dotenv
from netra import Netra
from netra.instrumentation.instruments import InstrumentSet

APP_NAME = "daisy"
ENVIRONMENT = "development"


def init_netra() -> None:
    load_dotenv()
    Netra.init(
        app_name=APP_NAME,
        environment=ENVIRONMENT,
        headers=f"x-api-key={os.getenv('NETRA_API_KEY', '')}",
        trace_content=True,
        instruments={InstrumentSet.LANGCHAIN, InstrumentSet.OPENAI},
    )


def shutdown_netra() -> None:
    Netra.shutdown()