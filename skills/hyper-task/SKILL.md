---
name: hyper-task
description: Manages Hyper tasks outside the execution workflow. Lists active tasks, creates a deferred task (exists but not started), cancels an in-progress task with a reason, or shows the status of a specific task. Use when the user asks "what tasks do I have", "list my tasks", "show my tasks", "what am I working on", "create a task for later", "cancel T<N>", "drop T<N>", "status of T<N>", or similar. Do not use for starting or continuing work — that's the `hyper` skill. Keywords: hyper, task, list, status, cancel, create, manage, deferred.
---

# hyper-task

Manage tasks without running the workflow. This skill handles listing, status checks, deferred creation, and cancellation. It never writes code or advances a task through phases — that's what `hyper` is for.

Tasks live at `.hyper/tasks/T<N>-<slug>/task.md`. The frontmatter shape is documented in `skills/hyper/reference/data-model.md` (bundled with the `hyper` skill). Read it if you need to verify any field.

## Routing

Read the user's request and pick exactly one operation. When the intent is unclear, ask.

| User intent | Operation | Keywords |
|-------------|-----------|----------|
| See what's active / "what am I working on" / "list tasks" | **List** | list, show, what tasks |
| "Show status of T3" / "what's T3" | **Status** | status, info, show T |
| "Create a task for later" / "remind me to X later" | **Create (deferred)** | create, remind, later, deferred |
| "Cancel T3" / "drop T5" / "I'm not doing T4" | **Cancel** | cancel, drop, abort, scrap |

For intents outside this list (start work, continue, rerun a phase), tell the user and point them to `hyper`.

## Operation: List

Read all task folders under `.hyper/tasks/`. For each, parse the frontmatter and report a short line.

Default output: all non-terminal tasks (phase not `done` and not `cancelled`), sorted by `id` ascending.

```
T1  feature  plan       awaiting: user-approval   Add login page
T3  quick    implement                            Rename UserService to AccountService
T5  feature  deferred                             Migrate storage to Postgres
```

Columns: `id`, `scope`, `phase`, `awaiting` (if set), `title`.

If the user asks for all tasks including terminal ones, include `done` and `cancelled`. If they ask for a specific filter ("show me cancelled tasks"), apply it.

If there are no active tasks, say so explicitly — don't return an empty report without context.

## Operation: Status

Given a task id `T<N>`, read its `task.md` and report:

- Id and title
- `phase`, `scope`, `created`, `awaiting`
- Artifacts present in the folder (`exploration.md`, `spec.md`, `checks.md`, etc.)
- For `spec.md`: how many subtasks are checked vs total (scan the file for `- [x]` and `- [ ]`)
- For `phase: cancelled`: include `cancelled_at` and `cancelled_reason`

Keep it tight — this is a status line, not a transcript. One screen.

If the id doesn't exist, say so and offer to list active tasks.

## Operation: Create (deferred)

Create a task the user doesn't want to start right now — it queues up for later.

Steps:

1. Get the title from the user's request. If they said "create a task to migrate v2", the title is "Migrate to v2". Clean it up (trim filler, keep it under ~60 chars).
2. Determine the next task id: scan `.hyper/tasks/` for the highest `T<N>` prefix, use `T<N+1>`.
3. Derive a kebab-case slug from the title.
4. Create `.hyper/tasks/T<N>-<slug>/task.md` using the shape in `../hyper/templates/task.md`, with frontmatter:
   ```yaml
   ---
   id: T<N>
   title: <title>
   phase: deferred
   scope: unknown
   created: <today's ISO date>
   awaiting: null
   ---
   ```
5. Body: one paragraph capturing the user's intent in their words.
6. Report to the user: *"Created T<N> — <title> (deferred). Invoke `hyper T<N>` when you're ready to start it."*

Do not start the workflow. `phase: deferred` signals the task exists but is unscheduled. When the user later invokes `hyper T<N>`, `hyper` sees the deferred phase, transitions it to `explore`, and begins the normal flow.

## Operation: Cancel

Cancel a task the user has decided not to pursue.

Steps:

1. Confirm the target. If the user said "cancel T4" and T4 exists, use that id. If T4 doesn't exist, say so and stop.
2. If T4 is already `done` or `cancelled`, say so and stop — no-op.
3. Ask for a one-line reason. *"Why cancel T4? (one line — saved with the task for history)"* Wait for the answer.
4. Update the task's frontmatter:
   - `phase: cancelled`
   - `cancelled_at: <today's ISO date>`
   - `cancelled_reason: <user's reason>`
   - Clear `awaiting` if set (`awaiting: null`).
5. Do **not** delete the task folder. History stays on disk.
6. Report: *"Cancelled T<N> — <title>. Reason recorded in `task.md`."*

## Rules

- **One operation per invocation.** Don't chain list + cancel in one run. Each natural-language request maps to one thing.
- **Never start or run phases.** If the user's request is really about doing work ("start T5", "continue T3", "add X"), tell them and recommend `hyper` or `/hyper T<N>`.
- **Never delete files.** Cancellation is a status change, not a deletion. Terminal tasks stay on disk as history.
- **Ask for missing info.** Create without a clear title? Ask. Cancel without a reason? Ask. Don't fabricate.
- **Task state lives in `task.md` frontmatter.** That's the source of truth. Don't read or write status from anywhere else.

## Key principles

- This skill is optimization for the user. Everything it does could be accomplished by manually editing files under `.hyper/` — the skill just makes the common operations fast and consistent.
- The output is for a human to read. List output, status output, confirmation messages — all designed for at-a-glance parsing, not machine consumption.
- Deferred tasks are a planning tool, not a to-do list. If the user's "later" list is getting long, that's a sign to prune or move items to `.hyper/backlog.md` instead.
