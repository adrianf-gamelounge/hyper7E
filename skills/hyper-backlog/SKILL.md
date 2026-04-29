---
name: hyper-backlog
description: >
  Manages the Hyper backlog — an idea-triage inbox at .hyper/backlog.md where items live before they become formal tasks. Adds, lists, promotes (converts an idea to a task), and drops backlog entries. Use when the user says "add to backlog", "what's on the backlog", "show the backlog", "promote B3 to a task", "drop B5", "make this idea a task", or similar. Decides between idea→backlog and idea→task when the user's intent is ambiguous, using a triage heuristic. Keywords: hyper, backlog, idea, triage, promote, inbox, B1.
---

# hyper-backlog

Manage `.hyper/backlog.md`, the idea inbox before work becomes a task.

Resolve the Hyper state root per `../hyper/reference/state-root.md`. Apply the
shared triage heuristic in `../hyper/reference/intake-triage.md`.

## Backlog format

```markdown
# Hyper Backlog

## B1 — <title>

<idea body>
```

Allocate new backlog ids by scanning existing `B<N>` headings and adding 1.
Dropped ids are not reused.

## Add

1. If the request is task-shaped and the user did not explicitly ask for
   backlog, recommend `/hyper <goal>` instead.
2. Append a new `## B<N> — <title>` entry.
3. Preserve useful motivation or constraints in the body.
4. Report the new id.

## List

Show each backlog id and title, with a one-line summary when useful.

## Promote

Convert a backlog entry into a deferred task.

1. Resolve the requested `B<N>` or topic. Do not guess on ambiguous matches.
2. Allocate the next task id by scanning `.hyper/tasks/` and `.hyper/archive/`.
3. Create `.hyper/tasks/T<M>-<slug>/task.md` from the Hyper task template with:
   - `phase: deferred`
   - `scope: unknown`
   - `bugfix: false`
   - `awaiting: null`
4. Seed `dashboard.md` from `../hyper/templates/dashboard.md`.
5. Remove the backlog entry.
6. Report: `Promoted B<N> -> T<M> — <title> (deferred).`

Do not invoke `hyper` or start the intake phase yourself.

## Drop

Remove a backlog entry only after explicit confirmation. No undo is provided.
