---
name: hyper-loops
description: Runs iterative loops for work where the goal is known but the route must evolve through contact with reality. Each loop persists so sessions can resume without losing context. Use when the user wants to iterate, course-correct mid-flight, probe before committing, or break a goal into adaptive slices. Keywords: hyper, iterate, loop, ooda, adaptive, probe, course correct.
argument-hint: "[L<N>|new]"
---

# Hyper Loops

Run tracked adaptive work: observe, orient, decide, act, repeat. Use it for iterative or exploratory work — when the path should stay flexible, when the goal itself is still forming, or when contact with reality is likely to shift the route.

## When to Use

Reach for hyper-loops when any of these match:

- The goal is clear but the path is not, and the path should stay flexible.
- The goal itself is still forming and needs probing before it can be committed.
- Reality is likely to reshape the plan once work starts.
- The work needs a throwaway probe or prototype before committing to a route.
- A big goal needs to be split into adaptive slices, not a rigid plan.
- The work will span multiple sessions and context must survive interrupts.
- The user uses verbs like "iterate", "explore", "probe", "experiment", "investigate", "prototype", "figure out", "pivot", or "course-correct".
- The user signals uncertainty about the path: "I'm not sure yet", "depends on what we find", "let me think through this", "this might change".

See `## Red Flags — STOP` for when not to use this.

## The Iron Law

**NO IMPLEMENTATION WITHOUT APPROVED ALIGNMENT. NO CLOSE WITHOUT PASSING VERIFY.**

Every loop runs two hard gates:

- **Alignment gate** — before the first implementation cycle, the user must approve the goal, the loop plan, and each part plan. Probes and reconnaissance can run before approval; production changes cannot.
- **Verify gate** — before `status: done`, tests must pass, code review must pass, user-facing docs must be updated, and every line in the definition of done must be met or marked `n/a`.

Skipping either gate is the loop failing, not progressing.

## The Process

Every loop moves through four phases:

1. **Load and Route** — read project rules and skill bindings. Decide: new loop or resume an existing one.
2. **Align** — restate the request, scan the codebase, report what exists and what's missing, agree on the loop plan and each part plan. **Hard gate.**
3. **Cycle** — for each part, repeat: observe → orient → decide → act → capture evidence → learn. One coherent move per cycle. Update living state, log decisions, refresh handoff cues.
4. **Verify and Close** — run tests, request code review, update docs, walk the definition of done. **Hard gate.** On pass, set `status: done`. On fail, run remediation cycles and re-enter the gate.

## The Loop Artifact

Each loop is a folder at `.hyper/loops/L<N>-<slug>/` containing:

- `loop.md` — the canonical state file. See `## Template — loop.md` for the full structure.
- Optional evidence files (logs, diffs, screenshots, console output) referenced from `## Relevant artifacts`. Use kebab-case names: `cycle3-build-log.txt`, `verify-2026-05-13.txt`.

The project root is the directory containing `.hyper/`, or the current working directory if `.hyper/` does not exist yet. Create `.hyper/loops/` if missing. Use absolute paths when the working directory differs from the project root.

Two kinds of content live in `loop.md`:

- **Living state** — overwrite as reality changes: `## Goal`, `## Why`, `## Constraints`, `## Non-negotiables`, `## Definition of done`, `## Task understanding`, `## Existing code and findings`, `## Loop plan`, `## Current route`, `## Current focus`, `## Current bar`, `## Parts`, `## Part alignment`, `## Evidence digest`, `## Relevant artifacts`, `## Handoff cues`, `## Outcome`.
- **History** — append-only, never rewrite: `## Bar history`, `## Route shifts`, `## Decisions`, `## Starting point`, `## Cycles`, `## Verified outcomes`.

Timestamps use `YYYY-MM-DDTHH:MM:SS`.

## Phase 1 — Load and Route

**Current time:**

!`date -u +%Y-%m-%dT%H:%M:%S`

**Existing loops:**

!`ls -1 .hyper/loops/ 2>/dev/null || echo "no loops yet"`

**Project rules and skill bindings.** Read both if they exist; treat as normative for the session.

- `.hyper/rules.md` — project-level rules that apply to every phase of every loop. If absent, no project rules are in force.
- `.hyper/skill-bindings.md` — per-project overrides for capability-to-skill bindings. See [`reference/default-bindings.md`](reference/default-bindings.md) for shipped defaults and resolution order.

Resolve bindings once per session. When a delegation point is reached and the bound skill is not installed, tell the user which capability needed it and ask whether to continue without it, swap for this loop, or stop. Never silently skip a delegation.

**Route.** Pick one:

1. **Resume by id or path** — user named `L<N>` or gave a path inside `.hyper/loops/`.
2. **Resume by title** — user named an existing loop clearly.
3. **Resume the only active loop** — exactly one loop has frontmatter `status: active`.
4. **Ask** — multiple active loops and the target is unclear.
5. **Create** — otherwise.

Done loops are not reopened. If the user wants to keep going from a done loop, create a new one and reference it in `## Starting point`.

**On create:**

1. Scan `.hyper/loops/` for `L<N>-*` folders, take the highest `N`, allocate the next.
2. Pick a short title and kebab-case slug.
3. Create `loop.md` from the template. Fill what is known; use `Not stated yet.`, `- None stated.`, or `Unknown.` for what is missing.
4. Initial bar: the next approval gate. Default to "reach an approved loop plan" if not stated.
5. Initial parts: 2–5 meaningful slices when the work decomposes naturally, or `P1 — Whole goal — doing` when it does not.
6. Announce: `Created L<N> — <title>. Starting adaptive loop.`

**On resume:** read `loop.md` in layers; do not reread the whole file by default.

- **Hot** (always): Goal, Definition of done, Task understanding, Existing code and findings, Loop plan, Current route, Current focus, Current bar, Parts, Part alignment, Evidence digest, Handoff cues.
- **Warm** (when the next move needs more): latest Decisions, Route shifts, Bar history, Relevant artifacts, last 1–3 cycles, latest Verified outcomes entry, Outcome.
- **Cold** (on demand only): older cycles, raw artifact files.

Promote durable signal upward as work progresses: route-shaping facts become `## Decisions`, still-relevant findings become `## Evidence digest`, restart-critical notes become `## Handoff cues`.

## Phase 2 — Align

Alignment is an interview pass before any implementation. Walk these steps in order:

1. **Restate your understanding** of the request from the user (or from the Linear issue, GitHub issue, etc.).
2. **Scan the project briefly** — relevant files, recent commits, README, related loops or tasks. Often the missing piece is already on disk.
3. **Report what already exists** in the codebase and what looks missing or unclear.
4. **Discuss the loop plan with the user** and agree how the work will be tackled.

Ask one question per message. Prefer multiple-choice when a structured-question tool is available; fall back to open-ended only when the choice space is genuinely open.

Only ask what changes the loop: goal, destination, hard constraints, non-negotiables, loop-plan shape, and the first part boundary. Skip details the loop will discover later.

**Grill the loop plan.** Before asking for approval, invoke `/grill-me` to walk the loop plan decision tree with the user. The grill-me skill interviews relentlessly, resolving each branch before moving on. Fold answers into `## Loop plan` and `## Decisions`. This is mandatory.

When the loop plan is non-trivial, also suggest a `cross-model-review` pass to get external model critique before approval. Suggested, not required. Fold the result into `## Loop plan` or `## Decisions`.

**Alignment gate.** Before the first implementation cycle, `loop.md` must show:

- `## Task understanding` — filled.
- `## Existing code and findings` — filled.
- `## Loop plan` — filled and grilled, plus:
  - `Status: awaiting approval | approved | needs rework`
  - `Approved by user: <timestamp or Not yet.>`

No implementation, validation, or production code mutation starts until the loop plan status is `approved`.

**Per-part alignment.** Repeat the same pattern for each part under `## Part alignment`:

- `### P<N> — <part name>`
- `#### Understanding`
- `#### Existing code and findings`
- `#### Plan`
- `Status: awaiting approval | approved | needs rework`
- `Approved by user: <timestamp or Not yet.>`

Run `/grill-me` on each part plan when it has its own non-trivial decisions; skip when the loop-level grill already covered the part. No work on part `P<N>` starts until that part plan is approved.

## Phase 3 — Cycle

_TBD._

## Phase 4 — Verify and Close

_TBD._

## Skill Bindings

_TBD._

## Delegation to Sub-Agents

_TBD._

## Red Flags — STOP

_TBD._

## Common Rationalizations

_TBD._

## Quick Reference

_TBD._

## Template — loop.md

_TBD._
