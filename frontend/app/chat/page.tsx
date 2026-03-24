import { ChatShell } from "@/components/chat-shell";

export default function ChatPage() {
  return (
    <main style={{ padding: "2rem" }}>
      <h1>Chat</h1>
      <p>Connected to FastAPI scaffold endpoints.</p>
      <ChatShell />
    </main>
  );
}
