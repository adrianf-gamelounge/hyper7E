# Hyper — Data Model

All Hyper state lives on disk under `.hyper/` in the project root. Plain markdown. No database, no CLI, no hidden state. A human can open any file and understand what's going on.

## Layout

```
.hyper/
  tasks/
    T1-add-login-page/
      task.md           # status + what the user asked for
      exploration.md    # what exists in the code + how we'll approach it
      spec.md           # acceptance criteria + subtask checklist
      checks.md         # test results, review findings, qa notes
      notes.md          # (optional) free-form working notes
  memory.md             # durable decisions across tasks
  backlog.md            # out-of-scope finds
```

- Task folders are named `T<N>-<kebab-slug>`. `N` is a simple incrementing integer. Slug is derived from the title.
- Artifact filenames are fixed. A skill that writes `spec.md` always writes to that path.
- A task with `phase: done` is complete. Nothing is ever "archived" — the folder stays.

## `task.md`

```markdown
---
id: T1
title: Add login page
phase: explore
scope: feature
created: 2026-04-17
awaiting: null
---

# Add login page

<The user's goal in their words, cleaned up after any clarification.
Two or three paragraphs max. This is what the task is about — the
artifacts below say how it gets done.>
```

### Frontmatter fields

| Field | Values | Meaning |
|-------|--------|---------|
| `id` | `T1`, `T2`, … | Sequential integer. First task is `T1`. |
| `title` | short string | Human-readable title, used in the folder name and headings. |
| `phase` | `deferred` · `explore` · `plan` · `implement` · `verify` · `docs` · `done` · `cancelled` | Current phase. The entry skill reads this to route. `done` and `cancelled` are terminal. `deferred` means the task exists but the user hasn't started it yet (created by `hyper-task`). |
| `scope` | `quick` · `feature` · `research` · `unknown` | Set during explore. Drives which phases run. `unknown` before explore classifies it. |
| `created` | ISO date | When the task was created. |
| `awaiting` | `null` · `user-approval` · `user-input` · `<custom label>` | When set, the entry skill stops and asks the user instead of running the phase. Cleared when the user responds. |
| `cancelled_at` | ISO date | Present only when `phase: cancelled`. Date the task was cancelled. |
| `cancelled_reason` | short string | Present only when `phase: cancelled`. One-line reason. |

### Phases by scope

| Scope | Flow |
|-------|------|
| `quick` | explore → implement → verify → done |
| `feature` | explore → plan → implement → verify → docs → done |
| `research` | explore → done (terminal artifact is `exploration.md`; no code changes) |

Phases are skipped by scope, not by agent judgment. If a feature task has no docs to update, `docs` phase still runs and writes `checks.md` recording "no docs changed, rationale: …".

A task in `phase: deferred` skips straight to `explore` the first time `hyper` is invoked on it — users "start" a deferred task the same way they continue any other task.

### Internal vs user-facing skills

Users invoke four skills directly: `hyper`, `hyper-task`, `hyper-handoff`, `hyper-retro`. The phase skills (`hyper-explore`, `hyper-plan`, `hyper-implement`, `hyper-verify`, `hyper-docs`) are internal — invoked only by `hyper`. They are marked `user-invocable: false` so they don't clutter the slash-command menu.

To manually re-run a phase on a task, edit `phase:` in the task's frontmatter and invoke `hyper`. The filesystem is the primary interface.

## `exploration.md`

Written by the `hyper-explore` skill. Two sections:

1. **Findings** — what exists in the code that matters for this task, bullet-point style. File paths + line numbers when relevant. Facts, not opinions.
2. **Approach** — how we'll do the work. For `quick`, two or three sentences. For `feature`, one or two paragraphs plus alternatives considered. For `research`, this is where the recommendation goes.

`exploration.md` is the approval artifact for the explore phase. Once the user approves, phase advances.

## `spec.md`

Written by the `hyper-plan` skill for `feature`-scope tasks. Contains:

1. **Acceptance criteria** — testable statements that define "done".
2. **Subtasks** — a markdown checklist. Each item is small enough to do in one sitting.
3. **Out of scope** — explicit list of things *not* being done.
4. **Edge cases** — known tricky scenarios the implementer must handle.

Subtasks live in this file as `- [ ] T1.1 — Install bcrypt`. The `hyper-implement` skill walks the list and checks boxes. No nested task folders.

## `checks.md`

Written during verify and docs phases. Three sections appended in order:

```markdown
## tests
<test runner output summary, pass/fail, command used>

## review
Verdict: pass | needs-changes | critical
<findings with file:line refs>

## qa
<functional checks against acceptance criteria — only for UI or user-facing work>

## docs
<which docs were updated or rationale for no update>
```

Each section gets written when its phase runs. Missing a section means the phase hasn't completed yet.

## `memory.md`

Durable notes that outlive a single task. Append-only in practice. Format:

```markdown
## 2026-04-17 — Pattern: service classes inject via constructor

Why: discussion during T3, user preference over static factories.
See: T3, src/services/user-service.ts
```

Each entry: date + category + title + one paragraph. Categories: `Decision`, `Pattern`, `Lesson`, `Constraint`.

## `backlog.md`

Out-of-scope things the agent notices but shouldn't fix inline. Format:

```markdown
- [ ] Pre-existing test failure in `auth.test.ts:42` — found during T5 verify
- [ ] README mentions deprecated CLI flag — found during T7 docs
```

Flat checklist. The user triages when they want.

## What's *not* here

- No `phases` array tracking every transition (the current `phase` field is enough)
- No separate task-status field (phase `done` = done; `awaiting` field handles pauses)
- No `clarification` field (the `awaiting` field serves this)
- No artifacts registry (artifacts are at known paths; file exists = artifact exists)
- No per-task memory (memory is project-scoped; task work lives in the task's files)
