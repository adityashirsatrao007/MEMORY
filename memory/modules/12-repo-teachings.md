# 12 — Research Notes: Cross-Repo Architectural Patterns

Personal research notes by Aditya Shirsatrao — architectural patterns extracted from studying 18 reference repositories. These are not dependencies or sources of MEMORY; they are studied references.

---

## 1. OpenBB (Financial Terminal & SDK)
- **Architecture**: Monorepo with an SDK engine that aggregates financial data providers and a visual CLI terminal wrapper.
- **Integration**: We can pull market metrics directly into quant tools by importing their python SDK.
- **Setup**:
  ```bash
  pip install openbb
  ```

## 2. Ruff (Rust-Based Python Toolchain)
- **Architecture**: A linter and formatter written in Rust, replacing Flake8, Black, and isort.
- **Integration**: Configured locally in `/tools/` to run checks on git commits.
- **Setup**:
  ```bash
  pipx install ruff
  ```

## 3. LangChain (LLM Orchestration)
- **Architecture**: Node-based chaining framework for models, memory, routing, and tool calling.
- **Integration**: Used when expanding our subagents into multi-step custom memory workflows.
- **Setup**:
  ```bash
  pip install langchain
  ```

## 4. Windmill (Developer Workflows & Script UI)
- **Architecture**: Postgres-backed workflow runner supporting Python, TypeScript, and Go scripts with auto-generated UIs.
- **Integration**: Alternative to Cron or PM2 for executing tasks on a distributed worker pool.
- **Setup**: Runs via Docker Compose (requires windmill postgres database).

## 5. SigNoz (Observability & APM)
- **Architecture**: OpenTelemetry native APM built in Go/React, using ClickHouse for storing traces and metrics.
- **Integration**: Integrated with local web applications to track latency, database queries, and errors.
- **Setup**: Deployed via SigNoz docker-compose stack.

## 6. Bottom (System Monitor)
- **Architecture**: A graphical process and system resource monitor built in Rust using `ratatui`.
- **Integration**: Executable via `btm` for monitoring system vitals in the terminal.
- **Setup**:
  ```bash
  cargo install bottom --locked
  ```

## 7. BuildKit (Docker Build Engine)
- **Architecture**: Concurrent, cache-efficient build engine powering modern `docker buildx`.
- **Integration**: Speeds up Vite/Next.js Docker image generation in CI/CD loops.

## 8. Novu (Notification Engine)
- **Architecture**: Microservice-based notifications manager handling Email, SMS, Slack, and Push templates.
- **Integration**: Replaces custom mailing scripts with a single unified API endpoint.

## 9. Zod (TypeScript Schema Validation)
- **Architecture**: TypeScript-first runtime schema parsing and type inference library.
- **Integration**: Used for input validation on all Next.js API endpoints to ensure type safety.
- **Setup**:
  ```bash
  npm install zod
  ```

## 10. Apache Kafka (Event Streaming)
- **Architecture**: Distributed commit-log messaging system built for high-throughput event queues.
- **Integration**: Used for logging traces or streaming telemetry events asynchronously between microservices.

## 11. Zitadel (Cloud-Native IAM)
- **Architecture**: OIDC/OAuth2 identity server written in Go, focused on multi-tenancy and audit logs.
- **Integration**: Replaces Clerk or Auth0 for enterprise sign-ins and user management.

## 12. Frappe HRMS (HR & Payroll Core)
- **Architecture**: Python-based extension built on the Frappe ERPNext framework, backed by MariaDB.
- **Integration**: Custom script integration for corporate accounting hooks.

## 13. Nextcloud AIO (Private Cloud Suite)
- **Architecture**: All-In-One Docker packaging for Nextcloud file sharing, office, and talk nodes.
- **Integration**: Used as the self-hosted storage vault for backups and agent logs.

## 14. Snipe-IT (Asset Management)
- **Architecture**: Laravel/PHP-based asset inventory manager.
- **Integration**: Accessible via REST API to query current server configurations and hardware assignments.

## 15. Infisical (Secrets Manager)
- **Architecture**: Vault alternative for developers, encrypting secrets end-to-end and syncing them to dev machines.
- **Integration**: Used to pull environment configs into local terminal runs automatically.
- **Setup**:
  ```bash
  curl -1sLf 'https://dl.cloudsmith.io/public/infisical/cli/setup.deb.sh' | sudo -E bash && sudo apt-get install -y infisical
  ```

## 16. MbedTLS (Cryptographic Core)
- **Architecture**: Lightweight C library providing TLS and basic cryptographic primitives.
- **Integration**: Referenced when building low-level secure sockets or encrypting local database blocks.

## 17. Devbox (Nix Environments)
- **Architecture**: Nix package manager wrapper allowing deterministic developer shells without writing Nix files.
- **Integration**: Run `devbox shell` to activate isolated software runtimes locally.
- **Setup**:
  ```bash
  curl -fsSL https://get.jetpack.io/devbox | bash -s -- -f
  ```

## 18. Reth (Rust Ethereum Client)
- **Architecture**: Optimized Ethereum execution layer node focusing on read-throughput and Rust modularity.
- **Integration**: Connects local web3 systems to the blockchain network.
