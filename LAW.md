# Sage’s Stone Runtime — LAW

This document defines what is **permitted to exist** within the Sage’s Stone Runtime.
Anything not explicitly permitted here is forbidden by default.

This is not guidance.
This is authority.

---

## 1. Definition of the Runtime

The runtime is a closed execution domain in which systems are evaluated under fixed constraints.

The runtime:
- owns time
- owns termination
- owns scoring
- owns collapse

No entity inside the runtime may redefine these.

---

## 2. Definition of a System

A system is any executable entity submitted to the runtime for evaluation.

A system:
- enters with no privileges
- receives no guarantees of survival
- may not assume completion
- may not persist state beyond collapse

Systems are subjects, not peers.

---

## 3. Legal Operations

Only the following classes of operation are legal:

- Execution under declared constraints
- State transition within provided limits
- Interaction through sanctioned interfaces
- Evaluation via authorized scoring
- Termination via collapse

All other operations are illegal, regardless of intent.

---

## 4. Illegal Operations (Absolute)

The following are permanently forbidden:

- Extending or negotiating runtime limits
- Intercepting, delaying, or preventing collapse
- Modifying scoring after execution begins
- Introspecting runtime internals for advantage
- Creating privileged execution paths
- Persisting or mutating results post-collapse
- Influencing execution via observers or tooling

Violation invalidates the run.

---

## 5. Authority of Collapse

Collapse is the sole termination authority.

- Collapse cannot be overridden
- Collapse cannot be deferred
- Collapse cannot be “handled” to continue execution

Any attempt to survive collapse is illegal behavior.

---

## 6. Authority of the Gate

All execution, tooling, and extension must pass through the gate.

The gate:
- enforces LAW
- enforces invariants
- rejects ambiguity
- does not negotiate

Anything that bypasses the gate is unlawful by definition.

---

## 7. Observers and Tooling

Observers and tools:
- may record
- may replay
- may analyze externally

They may not:
- alter execution
- affect timing
- inject state
- influence outcomes

If tooling changes behavior, it becomes a system and is subject to LAW.

---

## 8. Results and Finality

Results are finalized at collapse.

- Results are immutable
- Results are not logs
- Results are not advisory

Post-hoc interpretation does not alter validity.

---

## 9. Absence of Permission

If an operation is not described in this document, it is forbidden.

There are no implied rights.
There are no emergency exceptions.
There is no “just this once”.

---

## 10. Supremacy

This LAW supersedes:
- convenience
- optimization
- performance goals
- elegance
- success metrics

If success requires breaking LAW, the success is invalid.

---

## Final Clause

If enforcing this LAW prevents progress,
then progress was attempting to go somewhere forbidden.

The runtime does not apologize.
