"use client";

import { FormEvent, useState } from "react";
import { apiClient } from "@/lib/api";

type ChatItem = { role: "user" | "assistant"; content: string };

export function ChatShell() {
  const [input, setInput] = useState("");
  const [items, setItems] = useState<ChatItem[]>([]);

  const send = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    setInput("");
    setItems((prev) => [...prev, { role: "user", content: userMessage }]);

    try {
      const response = await apiClient.sendMessage({ message: userMessage, session_id: null });
      setItems((prev) => [...prev, { role: "assistant", content: response.content }]);
    } catch {
      setItems((prev) => [...prev, { role: "assistant", content: "Backend scaffold is not fully implemented." }]);
    }
  };

  return (
    <section>
      <div style={{ border: "1px solid #555", borderRadius: 8, minHeight: 280, padding: 12, marginBottom: 12 }}>
        {items.map((item, idx) => (
          <p key={`${item.role}-${idx}`}>
            <strong>{item.role}:</strong> {item.content}
          </p>
        ))}
      </div>
      <form onSubmit={send} style={{ display: "flex", gap: 8 }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask a math question" style={{ flex: 1 }} />
        <button type="submit">Send</button>
      </form>
    </section>
  );
}
