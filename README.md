# Daisy · Front desk assistant

An AI hotel front-desk assistant. Daisy helps with room availability, bookings,
reservations, payments, invoices, and other front-desk tasks through a simple
streaming chat interface. This is a test agent — the web surface is minimal so
you can try the underlying agent and observe its behavior.

## Prerequisites

- Python **3.12** and [uv](https://docs.astral.sh/uv/)
- Node.js (22+) and npm

## Setup

### 1. Environment variables
rate
Copy the template to the project root and fill in your values:

```bash
cp .env.example .env
```

Required variables:

| Variable             | Description                                  |
| -------------------- | -------------------------------------------- |
| `OPENAI_API_KEY`     | OpenAI API key for the agent's LLM calls.    |
| `MODEL`              | Model name, e.g. `gpt-4o-mini`.              |
| `NETRA_OTLP_ENDPOINT`| Netra OTLP telemetry endpoint.               |
| `NETRA_API_KEY`      | Netra API key for observability.             |

`.env` lives at the project root and is gitignored — never commit it.

### 2. Backend

```bash
cd backend
uv sync
uv run uvicorn backend.api:app --host 0.0.0.0 --port 8000
```

Run from the project root so the backend picks up the root `.env`.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

## Run with Docker

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

`docker-compose.yml` reads environment variables from the root `.env`.

## Docs

- [`DESIGN.md`](./DESIGN.md) — UI design intent.
- [`PRODUCT.md`](./PRODUCT.md) — product purpose and scope.