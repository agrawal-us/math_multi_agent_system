import Link from "next/link";

export default function HomePage() {
  return (
    <main style={{ padding: "2rem" }}>
      <h1>Math Multi-Agent</h1>
      <p>Scaffold-only migration to Next.js + FastAPI.</p>
      <ul>
        <li><Link href="/login">Login</Link></li>
        <li><Link href="/chat">Chat</Link></li>
      </ul>
    </main>
  );
}
