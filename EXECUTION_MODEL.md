# Sage’s Stone Runtime — Execution Model

This document defines what execution **is** within the Sage’s Stone Runtime.
Anything not defined here is not execution.

---

## 1. Definition of Execution

Execution is a bounded process initiated by the runtime in which a system
is evaluated under fixed constraints until collapse occurs.

Execution:
- has a single start
- proceeds forward only
- ends exclusively in collapse

Execution is not a dialogue.
Execution is not cooperative.
Execution is not guaranteed to complete.

---

## 2. Start of Execution

Execution begins only when:

- a system has passed the gate
- constraints have been fixed
- scoring has been declared
- collapse conditions have been armed

No system may observe or influence execution before this point.

---

## 3. During Execution

While execution is active:

- time advances under runtime control
- state transitions are permitted only within constraints
- scoring accumulates passively
- observers may record without agency

No entity may:
- alter constraints
- redefine scoring
- delay collapse
- introduce new capabilities

Execution does not negotiate.

---

## 4. Collapse

Collapse is the sole and mandatory termination of execution.

Collapse:
- is authoritative
- may occur at any time
- requires no system consent
- finalizes all results

Execution cannot continue past collapse.
There is no post-collapse execution state.

---

## 5. End of Execution

Execution ends exactly at collapse.

At that moment:
- results are finalized
- state is frozen
- scoring is sealed

Nothing occurring after collapse is part of execution.

---

## 6. Outside Execution

The following are explicitly outside execution:

- analysis
- visualization
- replay
- inspection
- interpretation

These activities:
- may not influence results
- may not alter records
- may not retroactively affect execution

Outside execution is not privileged.

---

## 7. Observers and Execution

Observers:
- exist only at runtime discretion
- have no agency
- cannot be detected by systems
- cannot affect timing or state

If an observer changes behavior, execution is invalid.

---

## 8. Tooling and Execution

Tooling may:
- initiate execution
- receive finalized results

Tooling may not:
- intervene during execution
- modify execution flow
- extend execution lifespan

Tooling is external by definition.

---

## 9. Determinism and Repeatability

Execution is deterministic with respect to:
- declared inputs
- declared constraints
- declared scoring

Any nondeterminism must be explicit and bounded.

Hidden nondeterminism is a violation.

---

## 10. Invalid Execution

Execution is invalid if:

- the gate was bypassed
- constraints were altered mid-run
- collapse was delayed or prevented
- observers influenced behavior
- results were modified post-collapse

Invalid execution produces no authoritative results.

---

## Final Statement

If execution feels cooperative, forgiving, or adaptable,
then execution is no longer occurring.

The runtime executes.
Systems endure.
Collapse decides.
