# Sage’s Stone — Runtime

This repository contains the **Runtime implementation** for Sage’s Stone.

Runtime is responsible for executing, orchestrating, and interfacing with the Sage’s Stone core.
It does **not** define or modify the core itself.

## Structure

- `CONTRACT.md` — Normative contract between Runtime and Stone
- `runtime/` — Execution logic, adapters, and orchestration
- `interfaces/` — Human or machine-facing surfaces (CLI, API, UI)
- `experiments/` — Non-canonical explorations (may be deleted at any time)

## Design Principles

- Stone is authoritative
- Runtime adapts to reality, not theory
- Execution must not redefine meaning
- Failure modes must be explicit

## Status

Early Runtime construction.
The core interface is intentionally minimal and stable.
