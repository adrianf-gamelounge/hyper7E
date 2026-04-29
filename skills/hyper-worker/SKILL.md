---
name: hyper-worker
description: >
  Implements one Hyper subtask end-to-end inside a dispatched sub-agent. Reads the named subtask file, executes only that slice, runs tests, writes a completion record, and flips the subtask to done. Use when hyper-implement dispatches a worker. Keywords: hyper, worker, subtask, writes, completion.
user-invocable: false
---

# hyper-worker

Implement exactly one subtask.

Resolve the Hyper state root per `../hyper/reference/state-root.md` before
reading or writing `.hyper/` paths. Read
`../hyper/reference/worker-guardrails.md` before editing code.

## Inputs

- `task.md`
- `04-execution-plan.md`
- one `T<N>.<M>-<slug>.md` subtask file
- upstream artifacts referenced by the subtask

## Flow

1. Re-read the assigned subtask file.
2. Set its `status: in-progress`.
3. Work only inside the declared `writes` boundary.
4. If another file is required, stop, add or update `## Open questions`, set
   `awaiting: user-input`, and return to the orchestrator.
5. Implement the slice.
6. Run the smallest meaningful tests or checks for the slice.
7. Write `## Completion` with file-grouped notes and check results.
8. Set `status: done` and `awaiting: null`.

## Rules

- Do not change sibling subtask files.
- Do not change `task.md` phase or awaiting fields.
- Do not widen `writes`; block and ask instead.
- For `role: test`, write tests and record a red baseline.
- For `role: impl`, confirm the sibling test baseline now passes without
  editing the test files.
