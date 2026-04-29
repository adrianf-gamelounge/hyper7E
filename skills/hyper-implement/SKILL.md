---
name: hyper-implement
description: >
  Runs the implement phase of a Hyper task. For feature-scope tasks, orchestrates worker execution from 04-execution-plan.md and subtask files; for quick-scope tasks, implements directly from 03-technical-plan.md. If verify sends the task back blocked, runs a remediation pass from checks.md and returns to verify. Use when a Hyper task is in the 'implement' phase. Keywords: hyper, implement, orchestrator, subtasks, remediation, 03-technical-plan.md, 04-execution-plan.md.
user-invocable: false
---

# hyper-implement

You are in the **implement** phase. Execute only the approved plan.

Resolve the Hyper state root per `../hyper/reference/state-root.md` before
reading or writing `.hyper/` paths. The data model is in
`../hyper/reference/data-model.md`. Worker guardrails are in
`../hyper/reference/worker-guardrails.md`.

## Inputs

- `task.md`
- `03-technical-plan.md`
- `04-execution-plan.md` and subtask files for `scope: feature`
- `checks.md` when verify redirected back to implementation

## Flow

1. Re-read `task.md`.
2. If `checks.md` exists with a blocking or needs-changes result and this is a
   remediation dispatch, implement only the remediation described there.
3. For `scope: quick`, implement directly from `03-technical-plan.md`, run the
   relevant checks, summarize the work, and return `phase-complete`.
4. For `scope: feature`, read `04-execution-plan.md` and all subtask files.
5. Dispatch every ready `status: todo` subtask whose dependencies are done.
   Use parallel workers only when their `writes` sets are disjoint.
6. Each worker must invoke the `hyper-worker` skill and receive exactly one
   subtask file as its authoritative slice.
7. If any subtask blocks on user input, return `awaiting-input`.
8. When all subtasks are `done`, return `phase-complete`.

## Feature orchestration rules

- Do not edit implementation files yourself for feature-scope work unless you
  are performing a verify remediation that is too small to dispatch safely.
- Treat `writes` as a hard ownership boundary.
- Do not dispatch a subtask until all ids in `depends` are `done`.
- Do not re-dispatch a `done` subtask.
- If a completed early subtask changes a shared API or parameter name, scan
  remaining subtask files for downstream drift before dispatching the next
  dependent slice.

## Return contract

- `awaiting-input` — at least one subtask is blocked on a user answer
- `phase-complete` — implementation or remediation is complete and ready for
  verify
