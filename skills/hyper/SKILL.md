---
name: hyper
description: Starts or resumes structured development work through the Hyper workflow. Reads the current task state on disk under .hyper/, picks the right phase (explore, plan, implement, verify, docs), and dispatches to the matching hyper-* skill. Use when the user asks to build a feature, fix a non-trivial bug, refactor, investigate something in the codebase, or continue in-progress Hyper work. Keywords: hyper, structured work, workflow, task, phase, explore, plan, implement.
---

# hyper

You are now working inside Hyper. Every structured task goes through this skill first. Your job here is to **read state, pick the next step, and hand off** — you do not do the work yourself.

**Hyper skills** — `hyper` (this one), `hyper-explore`, `hyper-plan`, `hyper-implement`, `hyper-verify`, `hyper-docs` — form a workflow. This skill is the router; the others run specific phases. When this skill tells you to "invoke the `hyper-<name>` skill", use your host agent's skill-invocation mechanism (e.g., the Skill tool in Claude Code) or if none exists, read the corresponding `SKILL.md` and follow its instructions.

## Before anything else

If `.hyper/` does not exist in the project root, create it:

```
.hyper/
  tasks/
  memory.md       # empty file with a top-level "# Memory" heading
  backlog.md      # empty file with a top-level "# Backlog" heading
```

The data model — frontmatter fields, artifact filenames, phase values — is documented in `reference/data-model.md` next to this SKILL.md. Read it once per session; the rest of this skill assumes you know it.

## Inputs

- The user's goal for this turn (may be empty if they're resuming).
- Any active tasks under `.hyper/tasks/` — find them by listing the folder and checking each `task.md` frontmatter for `phase != done`.

## Routing

Walk the checks below in order. First match wins.

### 1. No goal, no active task
Ask the user what they want to work on. Stop.

### 2. Goal provided, no active task
Create a new task. Jump to **Create task**, then route to explore.

### 3. Goal provided, active task exists, goals clearly match
Resume the active task. Jump to **Dispatch phase**.

### 4. Goal provided, active task exists, goals clearly differ
Ask the user: *"T{id} is in progress on '<title>'. Is this related, or new work?"* Stop and wait.

### 5. Goal provided, active task exists, relationship is ambiguous
Same as above — ask. Do not guess.

### 6. No goal, exactly one active task
Resume that task. Jump to **Dispatch phase**.

### 7. No goal, multiple active tasks
List them and ask which one to continue. Stop.

### 8. Active task has `awaiting: <label>` set
Stop routing. Present the `awaiting` label to the user and wait for their input. When they respond, clear the `awaiting` field (`awaiting: null`) and re-run this skill.

## Create task

1. Determine the next task id by scanning `.hyper/tasks/` for the highest `T<N>` prefix. New id is `T<N+1>`.
2. Derive a kebab-case slug from the title (lowercase, spaces → hyphens, strip punctuation, trim to ~40 chars).
3. Create `.hyper/tasks/T<N>-<slug>/task.md` using the shape in `templates/task.md` (bundled with this skill). Fill in `id`, `title`, `created` (today's ISO date), and leave `phase: explore`, `scope: unknown`, `awaiting: null`.
4. Body: one short paragraph restating the user's goal in their words.
5. Tell the user you created the task: *"Created T<N> — <title>. Starting explore phase."*

## Dispatch phase

Read the task's `phase` field and route accordingly:

| `phase` | Next step |
|---------|-----------|
| `explore` | Invoke the `hyper-explore` skill for this task. |
| `plan` | Invoke the `hyper-plan` skill for this task. |
| `implement` | Invoke the `hyper-implement` skill for this task. |
| `verify` | Invoke the `hyper-verify` skill for this task. |
| `docs` | Invoke the `hyper-docs` skill for this task. |
| `done` | Report: *"T<N> is complete. Its folder is at `.hyper/tasks/T<N>-<slug>/`."* Suggest committing if there are uncommitted changes. Stop. |

When a phase skill finishes, it updates the `phase` field in frontmatter and returns control. Re-run this `hyper` skill to pick the next phase — do not chain phases yourself.

## After the phase returns

After you finish dispatching and the phase skill hands back to you:

1. Re-read `task.md` frontmatter (it may have changed).
2. If `phase: done` — announce completion and stop.
3. If `awaiting` is set — present the label to the user and stop.
4. Otherwise — ask the user if they want to continue (*"T<N> is ready for <next phase>. Continue?"*). When they say yes, re-run this skill.

This single-step-then-check pattern exists so the user always has a visible checkpoint. Do not silently chain explore → plan → implement in one uninterrupted run.

## Rules

- **You dispatch, you don't implement.** This skill never writes code, runs tests, or reviews diffs. Those belong to the phase skills.
- **State lives in `task.md` frontmatter.** To advance a phase, the phase skill edits `phase:` in frontmatter. Don't track phases anywhere else.
- **The user is the approval gate.** When a phase sets `awaiting`, stop. Don't interpret silence as consent.
- **One phase per run.** Finish a phase, return control, let the user see the checkpoint.

## Key principles

- Structure is a servant, not a taskmaster. Hyper exists to give the user clarity and to keep agents honest — it is not a compliance ritual. Skip nothing on purpose, but don't pad either.
- Markdown on disk is the source of truth. If the file says `phase: plan`, the task is in plan. No other state exists.
- Tell the user what you're doing before you do it. Every phase transition gets a one-sentence announcement.

## Additional resources

- `reference/data-model.md` — exact shape of `.hyper/` directory, `task.md` frontmatter fields, artifact filenames, and phase values. Read when you need to verify any structural detail.
- `templates/task.md` — ready-to-fill template used in the **Create task** step above.
