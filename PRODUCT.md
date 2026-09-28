# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

A person (developer or evaluator) testing the Daisy hotel front-desk agent by
conversing with it through a simple chat interface. The user's job is to try
agent behavior — checking availability, making reservations, handling payments
and invoices, and similar front-desk tasks — and observe the responses.

## Product Purpose

Daisy is a test agent: an AI hotel front-desk assistant used to evaluate and try
the underlying agent. The web surface is deliberately minimal — a simple chat UI
that streams conversations from the backend chat endpoint. There are no
dashboards, booking forms, or operations views; the chat is the whole interface.

## Positioning

Not a market claim. Daisy is a test/demo agent, not a guest-facing product. Its
distinctive quality is a single conversational agent that can act on the full
hotel front-desk workflow (availability, bookings, reservations, payments,
invoices, door access, group blocks) for evaluation purposes.

## Operating Context

The frontend chat UI sends guest messages to the backend and streams the agent's
token responses back. The agent exposes 23 tools over the hotel data store
(`backend/src/backend/db/data.json`), covering availability, room details, rate
plans, add-ons, reservation lookup/create/modify/cancel, discount codes, gift
certificates, payment links and amount-due, group blocks, invoice generation,
confirmation resends, and door lock info. Reservations use confirmation numbers
of the form `DC-####`.

## Capabilities and Constraints

Confirmed capabilities (agent): check availability, get room details, list rate
plans and add-ons, find/get/create reservations, add a room to a booking, set a
preferred room number, cancel, modify, add an add-on, apply discount codes and
gift certificates, send payment links, report amount due, create group blocks,
book under a block, generate/get invoices, resend confirmations, and read door
lock info.

Backend is FastAPI + LangChain with an OpenAI model (`openai:gpt-4.1-mini` via
`langchain-openai`); it requires an `OPENAI_API_KEY`. Chat is served over a
server-sent-events endpoint (`POST /chat` in `backend/src/backend/api.py`).

Frontend stack is established: React 19 + Vite + Tailwind CSS v4 + shadcn/ui
with TypeScript.

Undecided: hotel name and identity; production vs. throwaway demo intent; any
authentication/identity model. The LiveKit Agents dependency is present in the
backend but is not wired to the current web chat surface.

## Brand Commitments

The agent's name is "Daisy" (used as the front-desk assistant's voice in the
system prompt). No other binding brand assets exist; the hotel name and visual
identity are undecided and must not be invented.

## Evidence on Hand

- `backend/src/backend/db/data.json` — real rooms (Standard King, Deluxe Queen,
  Suite), six rate plans, add-ons, and sample guests/reservations.
- `backend/src/backend/agent/prompt.py` — the agent's system voice.
- `backend/src/backend/api.py` — the chat request/response contract.

No testimonials, customer case studies, pricing claims, or deployment claims
exist; none should be fabricated.

## Product Principles

1. Daisy is a test agent, not a shipped consumer product.
2. The chat surface stays minimal — one simple chat UI, nothing more.
3. Agent answers are concise and accurate about what it can and cannot do.
4. Reservation and financial data are handled honestly; no fabricated
   confirmations or invoices.
5. Reproducible and easy to run for evaluation.

## Accessibility & Inclusion

No product-specific accessibility requirement was established. The chat UI
applies baseline web accessibility.