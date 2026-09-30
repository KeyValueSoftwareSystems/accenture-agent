# AGENTS.md

Guidance for AI coding agents working in this repository. Run everything with
Docker — the stack is a `docker compose` project.

## Stack overview

Two services (see `docker-compose.yml`):

| Service    | What it is                          | Host port |
| ---------- | ----------------------------------- | --------- |
| `backend`  | FastAPI + LangChain agent (Netra)   | `8000`    |
| `frontend` | React/Vite UI served by `vite preview` | `5173` |

The frontend calls the backend directly via `VITE_BACKEND_URL` (baked at build
time) or the runtime `frontend/public/config.js` — there is no reverse proxy.
The backend enables CORS for this.

**Important:** neither Dockerfile mounts your source as a volume — both images
`COPY` the code at build time. There is **no hot reload**. To apply code edits
you must rebuild the image and recreate the container.

## First run

1. Create the environment file from the template:

   ```bash
   cp .env.example .env
   ```

2. Fill in the required values in `.env`:
   - `OPENAI_API_KEY`
   - `MODEL`
   - `NETRA_OTLP_ENDPOINT`
   - `NETRA_API_KEY`

   `.env` is gitignored — never commit it.

3. Build the images and start the stack detached:

   ```bash
   docker compose up --build -d
   ```

4. Verify:
   - UI: open http://localhost:5173
   - Backend: `curl http://localhost:8000/health`

## Applying edits

Because source is copied into the image at build time, edit → rebuild → recreate:

```bash
docker compose up -d --build
```

`--build` rebuilds the image; `up -d` recreates the container from it. If the
build layer cache is stale, add `--no-cache`.

## `.env` changes

Env vars are injected at container start. To apply `.env` edits, recreate the
containers so they re-read `env_file`:

```bash
docker compose up -d
```

Prefer `up -d` over `docker compose restart`, which may reuse the old env in
some compose versions.

## Logs and teardown

- Stream backend logs: `docker compose logs -f backend`
- Stream frontend logs: `docker compose logs -f frontend`
- Stop and remove containers: `docker compose down`

There are no named volumes; app data lives in a JSON file inside the backend
source (`backend/src/backend/db/data.json`), so `docker compose down` does not
wipe data.

## Troubleshooting

- **Backend fails to start with a pydantic Settings validation error** — a
  required variable is missing or empty in `.env` (e.g. `OPENAI_API_KEY`,
  `MODEL`). Fix `.env`, then `docker compose up -d`.
- **Port already in use** — `8000` or `5173` is taken. Check with
  `docker compose ps` and stop the conflicting process.
- **`docker compose` command not found** — the Docker Compose v2 plugin is not
  installed; install it for your Docker distribution.