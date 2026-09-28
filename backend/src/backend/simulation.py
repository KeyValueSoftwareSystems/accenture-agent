import argparse
import json
import os
from copy import deepcopy
from uuid import uuid4

from netra import Netra
from netra.simulation import BaseTask, TaskResult

from backend.agent import get_agent
from backend.db import DATA_PATH, clear_db, set_db
from backend.observability import init_netra, shutdown_netra

DEFAULT_DATASET_ID = os.getenv(
    "NETRA_SIM_DATASET_ID", "2a2a2d3c-0c46-469b-8c7b-7451a1f6d988"
)

_SEED: dict | None = None
_SCENARIO_DBS: dict[str, dict] = {}


def _load_seed() -> None:
    global _SEED
    _SEED = json.loads(DATA_PATH.read_text())


def _scenario_db(thread_id: str) -> dict:
    if thread_id not in _SCENARIO_DBS:
        _SCENARIO_DBS[thread_id] = deepcopy(_SEED)
    return _SCENARIO_DBS[thread_id]


class DaisyTask(BaseTask):
    """Drives the Daisy front-desk agent in-process for multi-turn simulation.

    Netra starts each scenario with ``session_id=None`` and reuses the session
    id the task returns on every subsequent turn of that scenario. The first
    turn therefore mints a unique thread id, giving every scenario its own
    in-memory copy of the pristine mock database (via ``_scenario_db``) and its
    own LangGraph conversation thread. Because Netra runs the
    before_each/after_each hooks in a context separate from the task's run()
    calls, the ContextVar scoping is established here in run() so it is always
    active while the agent's tools execute.
    """

    async def run(
        self,
        message: str,
        session_id: str | None = None,
        files=None,
        setup_context: dict | None = None,
    ) -> TaskResult:
        thread_id = session_id or f"scenario-{uuid4().hex}"
        set_db(_scenario_db(thread_id))
        Netra.set_root_input(message)
        Netra.set_session_id(thread_id)
        result = await get_agent().ainvoke(
            {"messages": [{"role": "user", "content": message}]},
            config={"configurable": {"thread_id": thread_id}},
        )
        last = result["messages"][-1]
        content = last.content
        if isinstance(content, list):
            content = "".join(
                str(part.get("text", ""))
                for part in content
                if isinstance(part, dict) and part.get("type") == "text"
            )
        text = content if isinstance(content, str) else str(content)
        Netra.set_root_output(text)
        return TaskResult(message=text, session_id=thread_id)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a multi-turn Daisy simulation")
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID, help="Netra dataset id")
    parser.add_argument("--name", default="Daisy Front-Desk Simulation", help="Run name")
    parser.add_argument("--max-concurrency", type=int, default=4)
    parser.add_argument("--max-turns", type=int, default=12)
    args = parser.parse_args()

    if not args.dataset_id:
        parser.error("--dataset-id is required (or set NETRA_SIM_DATASET_ID)")

    _load_seed()

    init_netra()
    try:
        result = Netra.simulation.run_simulation(
            name=args.name,
            dataset_id=args.dataset_id,
            task=DaisyTask(),
            max_concurrency=args.max_concurrency,
            max_turns=args.max_turns,
        )
        print(f"Simulation result: {result}")
    finally:
        _SCENARIO_DBS.clear()
        clear_db()
        shutdown_netra()


if __name__ == "__main__":
    main()