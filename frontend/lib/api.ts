const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

type LoginPayload = {
  email: string;
  password: string;
};

type ChatPayload = {
  session_id: number | null;
  message: string;
};

type ChatResponse = {
  session_id: number;
  response_type: string;
  content: string;
  metadata: Record<string, unknown>;
};

async function post<T>(path: string, body: object): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const apiClient = {
  login(payload: LoginPayload) {
    return post<{ access_token: string; token_type: string }>("/auth/login", payload);
  },
  sendMessage(payload: ChatPayload) {
    return post<ChatResponse>("/chat/message", payload);
  },
};
