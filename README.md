# Stone Runtime

This repository is the **runtime**.

It is the execution layer that enforces law. Nothing here exists to explain ideas, complete theories, or make systems comfortable. It exists to **run them**, constrain them, collapse them, and record what happened.

If you are looking for meaning, philosophy, or invention: you are upstream.
If you are looking for mercy, optimization, or help: you are in the wrong place.

---

## What This Is

* A **deterministic execution environment** for Stone-compliant systems
* The **authority on execution**, not interpretation
* A system that:

  * enforces constraints
  * performs collapse
  * assigns outcomes
  * preserves immutability of results
* A hostile environment by design

The runtime treats Stone as law and everything else as untrusted.

---

## What This Is Not

* Not a theory engine
* Not a simulator for ideas
* Not an application framework
* Not a place to evolve or "finish" concepts
* Not a convenience layer
* Not a sandbox

This repository does **not** exist to make things work.
It exists to reveal when they do not.

---

## Runtime Authority

The runtime is final.

* Outcomes are not negotiable
* Collapse is irreversible
* Results are immutable
* Observers do not interfere
* Constraints are enforced, not suggested

If a system fails here, the system failed — not the runtime.

---

## What Cannot Be Touched

Unless explicitly stated otherwise:

* Runtime invariants
* Collapse authority and semantics
* Scoring semantics (outcomes only)
* Observer passivity
* Constraint enforcement
* The Stone interface surface
* Contracts between Stone and the runtime

Do **not** modify runtime behavior to save a system.
Anything that requires runtime changes does not belong inside it.

---

## Pre-Runtime Material

Material that predates this runtime:

* Defines **intent**, not implementation
* Provides context, not instructions
* Is not to be "completed" or "cleaned up" here

The runtime does not resolve ambiguity upstream.
It only enforces downstream consequences.

---

## What Can Be Built on Top

Allowed and expected:

* Stone implementations that strictly conform to the interface
* Systems that accept collapse, scoring, and limits as facts
* Adapters that translate external inputs into Stone-legal primitives
* Observers, tracers, analyzers, and visualizers that **do not interfere**
* Tooling outside the runtime for:

  * analysis
  * replay
  * reporting
  * comparison

Anything built on top must be willing to fail honestly.

---

## Design Ethos

* The runtime does not explain itself
* The runtime does not optimize for survival
* The runtime does not care about intent
* The runtime records what happened and moves on

Comfort is a bug.

---

## Read Before You Build

If you intend to extend, integrate, or depend on this runtime:

* Read everything
* Assume nothing
* Do not guess intent
* Do not soften constraints

When something is unclear, stop.
Guessing is a violation.

---

## Installation & Execution (Linux)

This section exists because people will ask.
It does **not** soften the runtime.

The runtime has no GUI, no wizard, and no safety rails.
If it fails to run on your system, that fact is itself informative.

### Supported Systems

* Ubuntu 22.04 LTS
* Ubuntu 24.04 LTS

Other Linux distributions may work, but are not guaranteed.

---

### Dependencies

This runtime intentionally declares **no external Python dependencies**.

If you are looking for a `requirements.txt` or `pyproject.toml`, their absence is deliberate.

At minimum, you need:

* Python 3.10 or newer
* Standard system build tools (for Python itself)

Install system prerequisites:

```bash
sudo apt update
sudo apt install -y python3 build-essential
```

If the runtime ever gains external dependencies, they will be explicit, minimal, and justified.

---

### Setup

There is no installation step beyond cloning the repository.

Do **not** invent dependency files.
Do **not** add package managers.
Do **not** wrap the runtime for convenience.

If your system Python cannot execute the runtime as-is, that is a valid failure signal.

---

### Running the Runtime

The runtime does nothing on its own.

Running it without an external Stone-compliant subject should result in:

* immediate termination, or
* a clear refusal to execute

This is correct behavior.

Execution is only meaningful when invoked by, or against, an external system.

---

### Important Notes

* There is no "hello world"
* There is no demo mode
* There is no interactive prompt

If you are expecting visible output without collapse, you are upstream.

---

## Status

This runtime is foundational.

Everything else builds **on top of it**, never inside it, unless explicitly authorized.
