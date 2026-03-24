# Next Phase TODOs (Post-Scaffold)

## Backend
1. Implement auth flows (register/login/refresh/logout) with real user persistence.
2. Add Alembic migrations for `users`, `chat_sessions`, `chat_messages`, `request_traces`.
3. Persist chat sessions/messages and connect request traces to chat requests.
4. Add dependency-injected current user auth guards on protected routes.
5. Add centralized error handling, request logging, and OpenTelemetry hooks.
6. Move copied orchestration toward adapter interfaces without changing solver logic.

## Frontend
1. Add proper auth state management and token storage strategy.
2. Replace inline styles with a design system (Tailwind/CSS modules).
3. Add streaming chat UX and session history retrieval.
4. Add route guards and login redirects.
5. Add API error boundaries and retry logic.

## Platform
1. Add docker-compose for local FastAPI + PostgreSQL + Next.js.
2. Add CI checks for lint, typecheck, and tests for both frontend and backend.
3. Add environment configuration strategy for dev/stage/prod.
4. Define modular monolith package boundaries and ownership.
