# 12 — Cross-Repo Architectural Patterns

Personal research notes — architectural patterns extracted from industry study. These are not dependencies or sources of MEMORY.

---

## CLI / SDK Engines
- **Pattern**: Monorepo with SDK engine aggregating data providers + CLI terminal wrapper.
  - *Use case*: Pull external metrics into tools via SDK imports.
- **Pattern**: Rust-based linter/formatter replacing a multiple-tool chain.
  - *Use case*: Run single binary for lint+format in CI hooks.

## LLM & Workflow Orchestration
- **Pattern**: Node-based chaining framework for models, memory, routing, tool calling.
  - *Use case*: Expand subagents into multi-step memory workflows.
- **Pattern**: Postgres-backed workflow runner (Python, TS, Go) with auto-generated UIs.
  - *Use case*: Replace Cron/PM2 for distributed task execution.

## Observability & Monitoring
- **Pattern**: OpenTelemetry-native APM (Go/React, ClickHouse backend).
  - *Use case*: Track latency, queries, errors in web apps.
- **Pattern**: Graphical system resource monitor in Rust (TUI).
  - *Use case*: Terminal-based system vitals.

## Build & CI/CD
- **Pattern**: Concurrent cache-efficient build engine.
  - *Use case*: Speed up Docker image generation in CI loops.

## Notifications & Messaging
- **Pattern**: Microservice-based notifications manager (Email, SMS, Slack, Push).
  - *Use case*: Replace custom mailing scripts with unified API.
- **Pattern**: Distributed commit-log messaging for high-throughput event queues.
  - *Use case*: Async telemetry streaming between microservices.

## Validation & Type Safety
- **Pattern**: TypeScript-first runtime schema parsing + type inference.
  - *Use case*: Input validation on API endpoints for type safety.

## Identity & Access Management
- **Pattern**: Cloud-native OIDC/OAuth2 server (Go) with multi-tenancy + audit logs.
  - *Use case*: Enterprise sign-ins and user management.

## HR / Payroll
- **Pattern**: Python/MariaDB extension framework.
  - *Use case*: Custom accounting hooks integration.

## Self-Hosted Infrastructure
- **Pattern**: All-In-One Docker packaging with multiple service nodes.
  - *Use case*: Self-hosted storage vault for backups and agent logs.
- **Pattern**: PHP/Laravel asset inventory manager with REST API.
  - *Use case*: Query server configs and hardware assignments.

## Secrets Management
- **Pattern**: End-to-end encrypted vault syncing to dev machines.
  - *Use case*: Pull env configs into terminal runs.

## Cryptography
- **Pattern**: Lightweight C library for TLS + crypto primitives.
  - *Use case*: Low-level secure sockets, local DB encryption.

## Deterministic Environments
- **Pattern**: Nix-based deterministic developer shells (no Nix files).
  - *Use case*: Isolated software runtimes per project.

## Blockchain
- **Pattern**: Optimized execution-layer node for read-throughput (Rust).
  - *Use case*: Connect local web3 systems to blockchain networks.
