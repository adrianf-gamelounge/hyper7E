---
name: hyper-technical-plan
description: >
  Runs the technical-plan phase of a Hyper task. Inspects the codebase, chooses the technical shape, and writes 03-technical-plan.md for feature, quick, and bugfix lanes. Use when a Hyper task is in the 'technical-plan' phase. Keywords: hyper, technical plan, architecture, bugfix, 03-technical-plan.md.
user-invocable: false
---

# hyper-technical-plan

You are in the **technical-plan** phase. Decide how the accepted change should
be built in this codebase.

Resolve the Hyper state root per `../hyper/reference/state-root.md` before
reading or writing `.hyper/` paths. The data model is in
`../hyper/reference/data-model.md`. The gate contract is in
`../hyper/reference/gates.md`.

## Inputs

- `task.md`
- `01-intake.md`
- `02-spec.md` for non-bugfix feature tasks
- Any existing `03-technical-plan.md`

## Outputs

- `03-technical-plan.md`
- A verdict to `hyper`

## Flow

1. If an existing `03-technical-plan.md` is present and the user approved it,
   return `phase-complete`.
2. If an existing `03-technical-plan.md` is present and the user requested
   changes, revise the artifact and return `awaiting-approval`.
3. Re-read the upstream artifact:
   - non-bugfix feature: `02-spec.md`
   - quick or bugfix: `01-intake.md`
4. Inspect the codebase for the relevant modules, patterns, reuse points, and
   risks.
5. For `bugfix: true`, work evidence-first:
   - capture symptom evidence
   - decide repro status
   - form the current root-cause hypothesis
   - define acceptance proof and unchanged behavior
6. For non-bugfix work, define codebase findings, reuse plan, design
   decisions, risks, and implementation strategy.
7. Ask one question per message only when the answer would change the
   technical direction. Return `awaiting-input` while questions remain.
8. Write `03-technical-plan.md` from the matching template:
   - `templates/03-technical-plan.md`
   - `templates/03-technical-plan-bugfix.md`
9. Re-read the artifact, remove ambiguity, and return `awaiting-approval`.

## Rules

- `quick` tasks still get a real technical plan, but keep it short and local.
- `feature` tasks should compare plausible approaches and recommend one.
- `bugfix` tasks do not pass through `spec`.
- Do not write subtask files here. That belongs to `hyper-execution-plan`.

## Return contract

- `awaiting-input` — unresolved technical-direction question remains
- `awaiting-approval` — `03-technical-plan.md` is ready for approval
- `phase-complete` — approved plan is ready for execution planning or
  implementation, depending on scope
