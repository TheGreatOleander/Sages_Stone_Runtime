# Sage’s Stone Runtime — Failure Modes

This document defines how failure exists within the Sage’s Stone Runtime.
Failure is not an error to be hidden.
Failure is a legitimate outcome governed by LAW.

---

## 1. Definition of Failure

Failure is any condition in which execution does not achieve continued progression
within declared constraints.

Failure:
- is expected
- is allowed
- is final when it triggers collapse

Failure is not exceptional.
Failure is informative.

---

## 2. Classes of Failure

The runtime recognizes the following failure classes:

- Constraint exhaustion (time, steps, resources)
- Invalid state transition
- Illegal operation under LAW
- Gate rejection
- Runtime-detected inconsistency
- Explicit collapse condition met

All classes are equally authoritative.

---

## 3. Constraint Exhaustion

When any declared constraint is exhausted:

- execution collapses immediately
- no grace period is granted
- no recovery is attempted

Attempting to extend or soften constraints is illegal.

---

## 4. Illegal Operations

If a system performs an operation forbidden by LAW:

- execution collapses
- results are finalized as-is
- no corrective handling occurs

Illegal behavior is not corrected.
It is recorded and terminated.

---

## 5. Gate Failure

If the gate rejects an action:

- the action does not occur
- execution does not proceed or is terminated
- no partial execution is preserved

Gate failure is decisive.

---

## 6. Runtime Inconsistency

If the runtime detects an internal inconsistency:

- execution collapses
- results are marked invalid
- further execution is forbidden until resolved

Integrity supersedes continuity.

---

## 7. Observer or Tooling Interference

If observers or tooling influence execution:

- execution is invalid
- results are void
- collapse occurs immediately

Observation must remain passive or not exist.

---

## 8. Forbidden Failure Handling

The following are not permitted:

- retrying within the same execution
- masking failure states
- compensating for failure mid-run
- graceful degradation that extends execution
- post-hoc correction of results

Failure is not a negotiation.

---

## 9. Post-Failure State

After failure-induced collapse:

- execution is over
- state is frozen
- results are immutable

Analysis may occur only outside the runtime.

---

## 10. Failure as Signal

Failure communicates:

- boundary location
- constraint pressure
- system inadequacy
- runtime enforcement

Failure is not embarrassment.
Failure is data.

---

## Final Clause

If a failure is uncomfortable enough to want to hide,
then it is important enough to preserve.

The runtime does not rescue.
The runtime records and ends.
