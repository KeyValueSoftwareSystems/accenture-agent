import { useState } from "react"
import { ArrowUpIcon, RotateCcwIcon } from "lucide-react"

import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import {
  Bubble,
  BubbleContent,
} from "@/components/ui/bubble"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Message,
  MessageAvatar,
  MessageContent,
} from "@/components/ui/message"
import {
  MessageScroller,
  MessageScrollerContent,
  MessageScrollerItem,
  MessageScrollerProvider,
  MessageScrollerViewport,
} from "@/components/ui/message-scroller"
import { useChat, type ChatMessage } from "@/hooks/useChat"

const WELCOME =
  "Hi, I'm front desk assistant here to help with room availability, bookings, reservations, payments, and more. How can I help?"

function AssistantBubble({ content, streaming }: { content: string; streaming: boolean }) {
  return (
    <Message align="start">
      <MessageAvatar>
        <Avatar>
          <AvatarFallback className="bg-primary text-primary-foreground">D</AvatarFallback>
        </Avatar>
      </MessageAvatar>
      <MessageContent>
        <Bubble variant="outline" align="start">
          <BubbleContent>
            {streaming ? (
              <span className="shimmer text-muted-foreground">Derek is thinking…</span>
            ) : (
              content
            )}
          </BubbleContent>
        </Bubble>
      </MessageContent>
    </Message>
  )
}

function UserBubble({ content }: { content: string }) {
  return (
    <Message align="end">
      <MessageContent>
        <Bubble variant="default" align="end">
          <BubbleContent>{content}</BubbleContent>
        </Bubble>
      </MessageContent>
    </Message>
  )
}

function MessageRow({ message }: { message: ChatMessage }) {
  if (message.role === "user") {
    return <UserBubble content={message.content} />
  }
  return (
    <AssistantBubble
      content={message.content}
      streaming={message.status === "streaming" && message.content.length === 0}
    />
  )
}

export function App() {
  const { messages, isStreaming, send, reset } = useChat()
  const [input, setInput] = useState("")

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault()
    if (!input.trim() || isStreaming) return
    void send(input)
    setInput("")
  }

  const handleReset = () => {
    if (isStreaming) return
    void reset()
  }

  return (
    <div className="mx-auto flex h-svh w-full max-w-2xl flex-col text">
      <header className="flex items-center gap-2 border-b px-4 py-3">
        <Avatar size="sm">
          <AvatarFallback className="bg-primary text-primary-foreground">D</AvatarFallback>
        </Avatar>
        <div className="flex min-w-0 flex-col">
          <span className="text-base font-semibold leading-tight">Derek</span>
          <span className="text-sm text-muted-foreground">Front desk assistant</span>
        </div>
        <Badge variant="secondary" className="ms-auto">
          test agent
        </Badge>
        <Button
          type="button"
          variant="ghost"
          size="icon-sm"
          onClick={handleReset}
          disabled={isStreaming}
          aria-label="Start a new conversation"
          title="Start a new conversation"
        >
          <RotateCcwIcon />
        </Button>
      </header>

      <MessageScrollerProvider autoScroll>
        <MessageScroller className="flex-1">
          <MessageScrollerViewport>
            <MessageScrollerContent className="px-4 py-5">
              <MessageScrollerItem>
                <AssistantBubble content={WELCOME} streaming={false} />
              </MessageScrollerItem>
              {messages.map((message) => (
                <MessageScrollerItem
                  key={message.id}
                  scrollAnchor={message.role === "user"}
                >
                  <MessageRow message={message} />
                </MessageScrollerItem>
              ))}
            </MessageScrollerContent>
          </MessageScrollerViewport>
        </MessageScroller>
      </MessageScrollerProvider>

      <form
        onSubmit={handleSubmit}
        className="flex items-center gap-2 border-t p-3"
      >
        <Input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Message Derek…"
          aria-label="Message Derek"
          autoFocus
          className="h-10 flex-1"
        />
        <Button
          type="submit"
          size="icon"
          disabled={!input.trim() || isStreaming}
          aria-label="Send message"
        >
          <ArrowUpIcon />
        </Button>
      </form>
    </div>
  )
}

export default App