# Team Sync Hub

Premium module — requires Enterprise license.

## Features
- Real-time memory sync across team members (WebSocket + CRDT)
- Conflict resolution with last-writer-wins + manual merge UI
- Per-namespace ACLs (who can read/write which modules)
- Activity feed with diff previews

## Setup
```bash
memory premium install team-sync
```

Start the sync daemon:
```bash
memory sync start --port 9090
```
