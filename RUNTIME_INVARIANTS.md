# Sage’s Stone Runtime — Invariants & Build Law

This document defines what **must never change** without explicit, conscious, and justified violation.
If you break these invariants, you are no longer building Sage’s Stone — you are building something else.

---

## 1. The Runtime Is Law

The runtime defines the physics of the system.

It is not:
- an application layer
- a convenience wrapper
- an optimization target
- a place to “add features”

Any system that runs here must accept the runtime as-is.

---

## 2. Constraint-First Is Non-Negotiable

Every execution is bound by:
- time limits
- step limits
- resource limits
- explicit termination

No system may:
- extend its own limits
- introspect runtime internals to avoid collapse
- negotiate scoring rules at runtime

Survival must be earned, not assumed.

---

## 3. Collapse Is Authoritative

Collapse is not failure.
Collapse is resolution.

The collapse authority:
- decides when execution ends
- cannot be overridden by systems
- cannot be postponed for convenience
- cannot be “handled gracefully” to continue execution

Anything that bypasses collapse is invalid.

---

## 4. Scoring Judges Outcomes, Not Intent

Scoring evaluates **what happened**, not:
- what was attempted
- what was intended
- how clever the system was
- how complex the code looks

A system that performs well accidentally is more valid than one that fails intelligently.

---

## 5. Results Are Immutable

Runtime results:
- are objects, not logs
- are finalized at collapse
- must not be mutated after creation

Analysis happens *outside* the runtime.
Observers do not influence execution.

---

## 6. Observers Have No Agency

Observers, tracers, and lenses:
- may record
- may replay
- may analyze
- may visualize

They may not:
- alter execution
- affect timing
- inject state
- bias scoring

If an observer changes behavior, it is not an observer.

---

## 7. Pre-Stone Material Is Intent Only

Pre-Sage’s Stone material exists to explain:
- why the runtime exists
- what problems it refuses to fake solutions for

It must never be “implemented directly”.
The runtime is the only legitimate realization of that intent.

---

## 8. Building Rules (Read This Twice)

You MAY:
- add new systems that run under the runtime
- add new scoring functions that obey the same collapse rules
- add tooling that wraps execution externally
- add documentation that clarifies boundaries

You MAY NOT:
- weaken constraints
- add escape hatches
- create privileged systems
- special-case “important” runs
- optimize away collapse semantics

---

## 9. If You Are Unsure — Stop

If you are unsure whether a change violates an invariant:
- assume that it does
- do not guess
- ask for clarification

Silently breaking the runtime is worse than halting progress.

---

## 10. Final Warning

If your addition makes the system:
- easier to win
- harder to collapse
- more forgiving of bad behavior
- impressed with itself

You have broken the Stone.

Build accordingly.
