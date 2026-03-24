"use client";

import { FormEvent, useState } from "react";
import { apiClient } from "@/lib/api";

export function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState<string>("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setStatus("Calling auth scaffold endpoint...");

    try {
      await apiClient.login({ email, password });
      setStatus("Auth endpoint connected (implementation pending).");
    } catch {
      setStatus("Auth scaffold not implemented yet.");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "grid", gap: "0.75rem", maxWidth: 420 }}>
      <label>
        Email
        <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
      </label>
      <label>
        Password
        <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
      </label>
      <button type="submit">Login</button>
      <small>{status}</small>
    </form>
  );
}
