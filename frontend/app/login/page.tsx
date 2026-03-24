import Link from "next/link";
import { LoginForm } from "@/components/login-form";

export default function LoginPage() {
  return (
    <main style={{ padding: "2rem" }}>
      <h1>Login</h1>
      <LoginForm />
      <p style={{ marginTop: "1rem" }}>
        <Link href="/chat">Go to Chat</Link>
      </p>
    </main>
  );
}
