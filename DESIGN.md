# Design — Daisy chat UI

<!-- impeccable:design-schema 1 -->

## Platform

web

## World

A single conversational surface built from the shadcn chat primitives on the
project's existing neutral shadcn theme (Tailwind v4, `radix-mira` style, Inter
Variable). The interface is deliberately bare: one centered chat column on a
neutral ground. The brand is the composed shadcn chat surface itself — no
chrome, no decoration, nothing competing with the agent's replies.

## Color

Restrained. Inherits the shadcn semantic tokens verbatim:
`--background`/`--foreground` for the page, `bg-muted`/`bg-secondary`/`bg-primary`
for message surfaces. User bubbles use `Bubble variant="default"` (primary);
agent bubbles use `Bubble variant="outline"` (background, bordered) so the two
sides read distinctly without introducing a second accent. Header uses the
`test agent` `Badge variant="secondary"`. Dark mode follows the existing
`.dark` tokens — no custom palette.

## Type

Inter Variable (existing `@fontsource-variable/inter`). Default sizes from the
shadcn chat primitives: message text `text-xs/relaxed`, header/subtitle
`text-sm`/`text-xs`, inputs `text-sm`. No new faces; the test surface does not
warrant a display voice.

## Components

- `MessageScrollerProvider autoScroll` + `MessageScroller`/`Viewport`/`Content`/
  `Item` — streaming follow, anchoring (`scrollAnchor` on user turns),
  jump-to-latest.
- `Message` + `MessageAvatar` (Avatar with `D` fallback) + `MessageContent`.
- `Bubble`/`BubbleContent` — `variant="outline"` for agent, `variant="default"`
  for user.
- `Badge` for the "test agent" marker; `Input` + `Button` (icon, `ArrowUp`) for
  the composer.
- Thinking indicator: `shimmer` utility on "Daisy is thinking…" while a reply
  streams with no tokens yet.

## Surface states

- Empty: welcome message from Daisy greets the user.
- Streaming: "thinking…" shimmer, then tokens append live to the last agent
  bubble; send disabled while streaming.
- Error: if the request fails, the empty agent bubble falls back to a
  "Something went wrong: …" message and returns to `done`.
- Composer: send button disabled when input is empty or while streaming.

## Layout & spacing

Full-viewport flex column, `max-w-2xl` centered: header (border-b), scroller
(flex-1), composer (border-t). Chat content padded `px-4 py-5`; the scroll pane
uses `no-scrollbar` (scroll still works, bar hidden).

## Motion

One authored moment: the shimmer "thinking…" state and the scroller's built-in
streaming follow / jump-to-latest. No entrance animations; the surface is a
tool, not a showcase.