# Stone Interface (Runtime View)

This document defines the ONLY surface Runtime may rely on.

## Exposed Primitives

Stone MUST expose:

- Identity
- Constraint
- Evaluation
- Result

## Required Properties

All Stone primitives MUST be:

- Deterministic
- Explicit
- Side-effect free
- Serializable

## Prohibited Assumptions

Runtime MUST NOT assume:

- Internal representations
- Optimization strategies
- Storage formats
- Execution order beyond what is stated

## Versioning

Stone exposes a semantic version.
Runtime must refuse to run against incompatible versions.
