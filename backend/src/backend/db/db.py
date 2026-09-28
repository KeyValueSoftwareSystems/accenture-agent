import contextvars
import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data.json"

_db: dict | None = None
_db_cv: contextvars.ContextVar = contextvars.ContextVar("db", default=None)


def _load_global() -> dict:
    global _db
    _db = json.loads(DATA_PATH.read_text())
    return _db


def _current() -> dict:
    scoped = _db_cv.get()
    if scoped is not None:
        return scoped
    if _db is None:
        return _load_global()
    return _db


def load_db() -> dict:
    global _db
    _db = json.loads(DATA_PATH.read_text())
    return _db


def get_db() -> dict:
    return _current()


def save_db(data: dict) -> None:
    if _db_cv.get() is not None:
        _db_cv.set(data)
        return
    global _db
    _db = data
    DATA_PATH.write_text(json.dumps(data, indent=2))


def set_db(data: dict) -> None:
    _db_cv.set(data)


def clear_db() -> None:
    _db_cv.set(None)


def get_collection(name: str) -> list:
    return get_db()[name]


def next_id(prefix: str) -> str:
    max_n = 0
    for collection in get_db().values():
        if not isinstance(collection, list):
            continue
        for row in collection:
            if isinstance(row, dict) and row.get("id", "").startswith(f"{prefix}-"):
                try:
                    max_n = max(max_n, int(row["id"].split("-", 1)[1]))
                except ValueError:
                    continue
    return f"{prefix}-{max_n + 1}"