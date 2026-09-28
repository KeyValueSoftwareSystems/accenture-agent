import uvicorn

from backend.api import app


def main() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8000)
