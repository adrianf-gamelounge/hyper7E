---
name: hyper
description: Starts or resumes structured development work through the Hyper workflow. Reads the current task state on disk under .hyper/, picks the right phase (explore, plan, implement, verify, docs), and dispatches to the matching hyper-* skill. Use when the user asks to build a feature, fix a non-trivial bug, refactor, investigate something in the codebase, resume a specific task by id (e.g. "resume T3"), or continue in-progress Hyper work. Keywords: hyper, structured work, workflow, task, phase, explore, plan, implement, resume.
---

# hyper

Your job: **take the user's request, combine it with `.hyper/` state, decide whether to create, resume, or ask — then dispatch to the right phase skill.** Never implement, test, or review yourself; phase skills do that.

For task *management* operations (list, create-deferred, cancel, status) the user goes to `hyper-task`, not this skill.

## Before anything else

If `.hyper/` does not exist in the project root, create it:

```
.hyper/
  tasks/
  memory.md       # empty file with a top-level "# Memory" heading
  backlog.md      # empty file with a top-level "# Backlog" heading
```

The data model — frontmatter fields, artifact filenames, phase values — is in `reference/data-model.md` next to this SKILL.md. Read it once per session; the rest of this skill assumes you know it.

## Task categories

For routing, classify every task by its `phase`:

- **Active** — `explore`, `plan`, `implement`, `verify`, `docs`. Currently in flight.
- **Deferred** — `deferred`. Exists but not started. Created by `hyper-task` for later.
- **Terminal** — `done`, `cancelled`. Finished; don't resume.

When I say "active tasks" below, I mean tasks in one of the active phases only.

## Inputs

- The user's request for this turn. May be:
  - Empty (continuing previous work)
  - A task id like `T3` (resume a specific task)
  - A natural-language goal (new or ambiguous)
- The contents of `.hyper/tasks/` — list the folder and parse each `task.md` frontmatter.

## Routing

Walk the checks below in order. First match wins.

### 1. Request is a task id (e.g. `T3`, `t3`, "resume T3")
Jump to **Resume by id**.

### 2. No goal, no active task
If any deferred tasks exist, tell the user ("You have deferred tasks: T5, T7. Start one with `/hyper T5`, or give me a new goal."). Otherwise ask what they want to work on. Stop.

### 3. Goal provided, no active task
Create a new task. Jump to **Create task**, then route to explore.

### 4. Goal provided, active task, goals clearly match
Resume the active task. Jump to **Dispatch phase**.

### 5. Goal provided, active task, goals clearly differ
Ask: *"T{id} is in progress on '<title>'. Is this new work, or part of T{id}?"* Stop and wait.

### 6. Goal provided, active task, relationship is ambiguous
Same as above — ask. Do not guess.

### 7. No goal, exactly one active task
Resume that task. Jump to **Dispatch phase**.

### 8. No goal, multiple active tasks
List them with `id`, `phase`, and `title`, then ask which to continue. Stop.

### 9. Active task has `awaiting: <label>` set
(This is checked in **Dispatch phase**, not here — but if detected while routing, stop and present the `awaiting` label. When the user responds, clear `awaiting` and re-run.)

## Resume by id

Given task id `T<N>`:

1. Find the folder `.hyper/tasks/T<N>-*/`. If none, tell the user the id doesn't exist and suggest `/hyper-task list`. Stop.
2. Read `task.md` frontmatter.
3. If `phase: done` — report *"T<N> is already complete."* Stop.
4. If `phase: cancelled` — report *"T<N> was cancelled (<reason>)."* Stop.
5. If `phase: deferred` — set `phase: explore`, save, then continue to **Dispatch phase**. Announce: *"Starting T<N> — <title>."*
6. Otherwise — continue to **Dispatch phase**.

## Create task

1. Determine the next task id: scan `.hyper/tasks/` for the highest `T<N>` prefix, use `T<N+1>`.
2. Derive a kebab-case slug from the title (lowercase, spaces → hyphens, strip punctuation, ~40 chars).
3. Create `.hyper/tasks/T<N>-<slug>/task.md` using the shape in `templates/task.md`. Fill in `id`, `title`, `created` (today's ISO date), and set `phase: explore`, `scope: unknown`, `awaiting: null`.
4. Body: one short paragraph restating the user's goal in their words.
5. Announce: *"Created T<N> — <title>. Starting explore phase."*

## Dispatch phase

Before dispatching, check `awaiting`. If set, present the label to the user and stop — don't run a phase while a gate is open.

Read the task's `phase` field and route:

| `phase` | Next step |
|---------|-----------|
| `deferred` | Set `phase: explore`, then recurse through this table. |
| `explore` | Invoke the `hyper-explore` skill for this task. |
| `plan` | Invoke the `hyper-plan` skill for this task. |
| `implement` | Invoke the `hyper-implement` skill for this task. |
| `verify` | Invoke the `hyper-verify` skill for this task. |
| `docs` | Invoke the `hyper-docs` skill for this task. |
| `done` | Report completion and task folder path. Stop. |
| `cancelled` | Report the cancellation and reason. Stop. |

When a phase skill finishes, it updates `phase:` in frontmatter and returns control. Re-run this `hyper` skill to pick the next phase — do not chain phases yourself.

## After the phase returns

1. Re-read `task.md` frontmatter (it may have changed).
2. If `phase: done` — announce completion and stop.
3. If `phase: cancelled` — announce cancellation and stop.
4. If `awaiting` is set — present the label to the user and stop.
5. Otherwise — ask: *"T<N> is ready for <next phase>. Continue?"* When the user says yes, re-run this skill.

This step-then-check pattern exists so the user always has a visible checkpoint. Do not silently chain explore → plan → implement in one uninterrupted run.

## Rules

- **You dispatch, you don't implement.** This skill never writes code, runs tests, or reviews diffs.
- **State lives in `task.md` frontmatter.** The phase skill edits `phase:` to advance. Don't track phases anywhere else.
- **The user is the approval gate.** When a phase sets `awaiting`, stop. Silence is not consent.
- **One phase per run.** Finish a phase, return control, let the user see the checkpoint.
- **Terminal tasks stay terminal.** `done` and `cancelled` don't re-run from here. If the user wants to reopen a cancelled task, they clear the cancel fields manually.

## Key principles

- Structure is a servant, not a taskmaster. Skip nothing on purpose, but don't pad either.
- Markdown on disk is the source of truth. If the file says `phase: plan`, the task is in plan.
- Announce phase transitions. Every routing decision gets one clear sentence before any action.

## Additional resources

- `reference/data-model.md` — exact shape of `.hyper/`, `task.md` frontmatter, artifact filenames, and all phase values. Read when verifying structural details.
- `templates/task.md` — ready-to-fill template used in **Create task**.
