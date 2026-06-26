# Research Memory

## Storage
In-memory conversation store with session management. Each session contains:
- Messages (user + AI)
- Linked platform entities (regions, graph nodes, experiments, timeline snapshots)

## API
- `GET /api/reasoning/history?session_id=xxx` — Returns message history
- Sessions are auto-created on first message

## Future
- Persistent storage (SQLite/PostgreSQL)
- Vector embeddings for semantic search across sessions
- Cross-session knowledge linking
