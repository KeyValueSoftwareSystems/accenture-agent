import { useCallback, useRef, useState } from "react"

export type ChatRole = "user" | "assistant"

export interface ChatMessage {
  id: string
  role: ChatRole
  content: string
  status: "done" | "streaming"
}

const THREAD_ID = "web"

const RUNTIME_BACKEND_URL = (window as unknown as { DAISY_BACKEND_URL?: string }).DAISY_BACKEND_URL
const BACKEND_URL = (
  RUNTIME_BACKEND_URL ||
  (import.meta.env.VITE_BACKEND_URL as string | undefined) ||
  ""
).replace(/\/+$/, "")

function parseFrame(frame: string, onToken: (token: string) => void) {
  const lines = frame.split("\n")
  let event = ""
  let data = ""
  for (const line of lines) {
    if (line.startsWith("event:")) {
      event = line.slice(6).trim()
    } else if (line.startsWith("data:")) {
      data += line.slice(5).trim()
    }
  }
  if (event === "token") {
    try {
      const payload = JSON.parse(data)
      if (typeof payload.token === "string" && payload.token.length > 0) {
        onToken(payload.token)
      }
    } catch {
      // ignore malformed token frames
    }
  }
}

let counter = 0
function nextId(role: ChatRole) {
  counter += 1
  return `${role}-${counter}`
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isStreaming, setIsStreaming] = useState(false)
  const abortRef = useRef<AbortController | null>(null)

  const send = useCallback(async (text: string) => {
    const trimmed = text.trim()
    if (!trimmed || isStreaming) return

    const userMessage: ChatMessage = {
      id: nextId("user"),
      role: "user",
      content: trimmed,
      status: "done",
    }

    const assistantId = nextId("assistant")
    const assistantMessage: ChatMessage = {
      id: assistantId,
      role: "assistant",
      content: "",
      status: "streaming",
    }

    setMessages((prev) => [...prev, userMessage, assistantMessage])
    setIsStreaming(true)

    const controller = new AbortController()
    abortRef.current = controller

    try {
      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed, thread_id: THREAD_ID }),
        signal: controller.signal,
      })
      if (!response.ok || !response.body) {
        throw new Error(`Chat request failed (${response.status})`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ""

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        let separator = buffer.indexOf("\n\n")
        while (separator !== -1) {
          const frame = buffer.slice(0, separator)
          buffer = buffer.slice(separator + 2)
          parseFrame(frame, (token) => {
            setMessages((prev) =>
              prev.map((message) =>
                message.id === assistantId
                  ? { ...message, content: message.content + token }
                  : message,
              ),
            )
          })
          separator = buffer.indexOf("\n\n")
        }
      }

      setMessages((prev) =>
        prev.map((message) =>
          message.id === assistantId ? { ...message, status: "done" } : message,
        ),
      )
    } catch (error) {
      const message = error instanceof Error ? error.message : "Request failed"
      setMessages((prev) =>
        prev.map((item) =>
          item.id === assistantId
            ? {
                ...item,
                content: item.content || `Something went wrong: ${message}`,
                status: "done",
              }
            : item,
        ),
      )
    } finally {
      setIsStreaming(false)
      abortRef.current = null
    }
  }, [isStreaming])

  const reset = useCallback(async () => {
    abortRef.current?.abort()
    setMessages([])
    setIsStreaming(false)
    try {
      await fetch(`${BACKEND_URL}/chat/${encodeURIComponent(THREAD_ID)}`, { method: "DELETE" })
    } catch {
      // server thread may already be empty; local state is still cleared
    }
  }, [])

  return { messages, isStreaming, send, reset }
}