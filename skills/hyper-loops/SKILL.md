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

- **Alignment gate** — before any implementation cycle, the loop plan must be approved (including its goal and scope). Each part plan must be approved before that part's first implementation cycle. Probes and reconnaissance can run before approval; production changes cannot.
- **Verify gate** — before `status: done`, tests must pass, code review must pass, user-facing docs must be updated, and every line in the definition of done must be met or marked `n/a`.

Skipping either gate is the loop failing, not progressing.

## The Process

Every loop moves through four phases:

1. **Load and Route** — read project rules. Decide: new loop or resume an existing one.
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

**Project rules.** Read `.hyper/rules.md` if it exists; treat as normative for the session. If absent, no project rules are in force.

When the loop needs to call another skill (`/grill-me`, `/code-review`, `/technical-docs`, `/hyper-team`, etc.) and that skill is not installed, tell the user which capability is missing and offer: install it, swap to a substitute for this loop, or stop. Never silently skip a required skill call.

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

**Grill the loop plan.** Before asking for approval, invoke `/grill-me` to walk the loop plan decision tree with the user. The grill-me skill interviews relentlessly, resolving each branch before moving on. Fold answers into `## Loop plan` and `## Decisions`. This is mandatory; "continue without it" is **not** a valid choice when `/grill-me` is missing. If `/grill-me` is not installed, offer the user only: install it, swap to an equivalent pressure-test skill for this loop, or stop.

When the loop plan is non-trivial, also suggest invoking `/hyper-team` with codex to get an external model critique of the loop plan before approval. Suggested, not required. Fold the result into `## Loop plan` or `## Decisions`. If the external review changes the loop plan, re-run `/grill-me` on the changed plan before approval.

A loop plan is **non-trivial** when any of the following holds: it touches more than one part, it introduces a new external dependency, it changes a public contract, or it makes a decision the user cannot easily reverse.

**Post and ask.** Once the loop plan is filled and grilled (and re-grilled if external review changed it), post a concise loop-plan summary in chat — goal, approach, parts, key decisions, open risks. Then ask explicitly: `Approve this loop plan? (approve | needs rework)`. Do not set `Approved by user` unless the user replies with an explicit `approve`. The plan only exists in the agent's head until the user has seen it rendered.

**Alignment gate.** Before the first implementation cycle, `loop.md` must show:

- `## Task understanding` — filled.
- `## Existing code and findings` — filled.
- `## Loop plan` — filled, plus:
  - `Grilled at: <timestamp or Not yet.>`
  - `External review: completed by /hyper-team codex | skipped by user | n/a`
  - `Status: awaiting approval | approved | needs rework`
  - `Approved by user: <timestamp or Not yet.>`

"Filled" means no placeholder strings (`Not stated yet.`, `- None stated.`, `Unknown.`, `Not filled yet.`, `Not agreed yet.`) remain in the section.

The gate is cleared when, and only when: every "filled" section contains no placeholders, `Grilled at` is a timestamp, `External review` is set, and `Approved by user` is a timestamp. No implementation, validation, or production code mutation starts before this.

**On `needs rework`.** Return to step 4 (discuss the loop plan) for the disputed area. Update `## Loop plan` with the user's feedback, append the reason and decision to `## Decisions`, re-grill the branches the rework touched, refresh `Grilled at`, and re-post the plan summary. `External review` status carries over unless the rework changes a contract or dependency, in which case mark it `n/a` and re-suggest.

**Per-part alignment.** Repeat the same pattern (interview, grill where required, post and ask, gate, rework) for each part under `## Part alignment`:

- `### P<N> — <part name>`
- `#### Understanding`
- `#### Existing code and findings`
- `#### Part plan`
- `Part grill: completed at <timestamp> | covered by loop grill <timestamp> | n/a — no new decisions`
- `Status: awaiting approval | approved | needs rework`
- `Approved by user: <timestamp or Not yet.>`

Run `/grill-me` on a part plan when **any** of these hold: the part introduces a new external dependency, a new data shape, a new user-visible surface, or any decision not resolved in the loop-level grill. Otherwise record `covered by loop grill <timestamp>` and skip the part grill. No work on part `P<N>` starts until that part plan is approved.

## Phase 3 — Cycle

Cycles start only after the loop plan is approved and the current part plan is approved. One cycle = one coherent move. Run one cycle at a time unless the user asks for a batch.

Allocate the next cycle number by scanning existing `### Cycle N —` headings under `## Cycles`.

For each cycle:

1. **Observe** — read or run only enough to see the next useful move.
2. **Orient** — state what matters now: hypothesis, risk, or why this slice is next.
3. **Prior belief** — name what you expected to be true going into this cycle. `same as cycle N-1` is acceptable when nothing has shifted; the value is making the belief explicit, not forcing novelty.
4. **Decide** — pick one intent:
   - `probe` — throwaway experiment that answers a design, state, or UI question before committing.
   - `implement` — production change toward the current part. Requires the current part plan to be `approved`.
   - `validate` — run tests, manual checks, or external review against existing work.
   - `split` — the current part is too big; create new parts and re-enter Phase 2 for them.
   - `reroute` — same goal, different path through the loop plan.
   - `reframe` — evidence suggests the goal itself was wrong. Stop the cycle, update `## Goal` and `## Why`, and re-run the Phase 2 alignment gate (`## Task understanding`, `## Existing code and findings`, `## Loop plan`) before any further work. Distinct from `reroute`.
   - `stop` — goal reached, abandoned, or blocked; head to Phase 4 or close without verify.
5. **Act** — the smallest meaningful move that advances the chosen intent.
6. **Evidence** — capture the exact result. If raw output is large, save it inside the loop folder, keep the decisive excerpt in the cycle, and link the file from `## Relevant artifacts`.
7. **Learning** — what the evidence changed about the prior belief, the route, the parts, or the risks. Then explicitly ask: **is the goal still the right goal?** If no, the next intent must be `reframe`, not `reroute`.
8. **Route impact** — how this cycle changes the route or parts for the next cycle. `no change` is a valid finding and itself a useful signal.
9. **Update living state** — refresh whatever sections the cycle changed.
10. **If the next move opens a new part or changes a part plan, stop and refresh `## Part alignment` first.** Re-enter Phase 3 only after the user approves that part plan.
11. **Refresh handoff cues** — leave the next atomic move and the current risk visible in `## Handoff cues`.
12. **Next** — continue, back up, split, validate, or stop (then run Phase 4 — Verify and Close).
13. **Append** the cycle entry to `## Cycles` and bump frontmatter `updated`.

**TDD as a suggested implementation mode.** When an `implement` cycle's work is testable behavior (not pure refactoring, pure tooling, or pure prose), suggest `/tdd` to drive the slice red-green-refactor. Suggested, not required — the user can decline. When used, the failing test becomes the cycle's `Evidence`, the passing implementation becomes the next cycle's `Act` and `Evidence`, and the refactor (if any) becomes a third cycle.

If the bar or route changes, update the living value **and** append a one-line entry to `## Bar history` or `## Route shifts` with timestamp and reason. Use `## Decisions` only for load-bearing choices.

Part statuses: `todo | doing | done | blocked | dropped`.

## Phase 4 — Verify and Close

Phase 4 starts when Phase 3 ends with intent `stop` — either because the destination is reached, the user said stop, or the loop is blocked. It runs a single hard gate: the verify gate. The loop cannot close as `done` without a passing entry in `## Verified outcomes`, or an explicit user choice to close without verify.

**Run all four checks:**

1. **Tests.** Re-run the project's test suite. Capture the exact command, exit code, and a decisive excerpt. Link the full log under `## Relevant artifacts` if large.
2. **Code review.** Invoke `/code-review` on the loop's full diff. Capture the verdict (`pass | needs-changes | blocked`) and the top findings.
3. **Docs.** If the loop changed user-facing surface (CLI, UI, API, public functions, behavior advertised to users), invoke `/technical-docs`. Otherwise mark `n/a — no user-facing surface change` with a one-line justification.
4. **Definition of done.** Walk every line in `## Definition of done`. Mark each `met | not met | n/a` with the evidence that backs the mark (file:line, test name, screenshot, etc.).

Missing-skill handling matches Phase 2: if `/code-review` is required for this loop and is not installed, "continue without it" is **not** a valid choice. Same rule for `/technical-docs` when the loop changed user-facing surface. Offer install, swap for this loop, or stop.

**Record `### Verify N`** under `## Verified outcomes`:

```
### Verify N — <timestamp>

**Tests:** <command> → <exit code, decisive excerpt — link full log under Relevant artifacts if large>

**Code review:** </code-review verdict — pass | needs-changes | blocked — and top findings>

**Docs:** </technical-docs output summary, or `n/a — no user-facing surface change`>

**Definition of done:**
- <line 1> — met | not met | n/a — <evidence>
- <line 2> — met | not met | n/a — <evidence>

**Result:** pass | partial | fail

**Next:** <stop and close | remediation cycle to fix <what>>
```

**On `pass`** — set frontmatter `status: done`. Fill `## Outcome` with: what was achieved, what was traded away, link to this verify entry. Post a short closing summary in chat (result, what was verified, handoffs the next session needs). Stop.

**On `partial` or `fail`** — leave `status: active`. Run a remediation cycle (return to Phase 3) that fixes the specific failures named in this verify entry, then re-enter the verify gate. Do not edit `## Definition of done` to make a failure go away unless the user explicitly approves changing the scope.

**On user-explicit close without verify** — the user can close the loop before the verify gate passes ("I'm dropping this", "good enough", "abandon this loop"). When this happens: set `status: done`, write `Closed by user without verify gate` at the top of `## Outcome` along with the reason and any unfinished items. Skip the verify gate. This is a deliberate user choice, not a verify-gate pass.

## Delegation to Sub-Agents

When sub-agents are available, the parent may delegate a bounded slice within a cycle (recon, research, focused validation, adversarial review, one-part implementation). The parent still owns the loop and every route decision; the child returns a summary, the parent integrates it into the cycle's evidence and updates `loop.md`.

**Delegate when:**

- The task has a clear input, output, and stop condition.
- Fresh context will find different things than the parent's accumulated context (recon, second-opinion review).
- Multiple bounded slices can run in parallel without touching the same code path.

**Do not delegate:**

- The whole loop. Phase decisions, alignment, gate passes, and route changes stay with the parent.
- Anything that needs the loop's accumulated context.
- Approval moments — the user talks to the parent, not to children.

**Rules:**

- Children never mutate `loop.md` directly. They return text; the parent writes the cycle entry and refreshes living state.
- One writer at a time for implementation on the same code path. Two children racing on the same files produces incoherent diffs.
- Each delegation has a clear input, output, and stop condition. "Look at the codebase and figure things out" is too open; "find every call site of `Foo.bar` and report each as file:line with context" is bounded.

## Red Flags — STOP

When you catch yourself doing any of these, stop the current cycle, surface the pattern to the user, and back up to the phase that should have caught it.

- Starting an `implement` cycle before the loop plan is `approved`. → Back up to Phase 2.
- Starting work on a part before its part plan is `approved`. → Back up to Phase 2's per-part alignment.
- Asking for loop-plan approval without running `/grill-me` first. → Run the grill, then re-post and ask.
- Marking a section "filled" while it still contains `Not stated yet.`, `Unknown.`, or any other placeholder. → Fill it for real.
- Editing `## Definition of done` to make a verify check pass. → Run a remediation cycle that meets the original line, or ask the user to approve a scope change.
- Hearing a user pivot ("actually, what if we tried X", "I want to investigate something else") and folding it into a part plan without surfacing it. → Stop. The intent is `reframe`, not `reroute`. Re-run Phase 2.
- Running a cycle that batches unrelated changes. → Split into separate cycles.
- Continuing past a missing `/code-review`, `/grill-me`, or `/technical-docs` without offering install / swap / stop. → Stop and ask.
- Mutating `loop.md` from inside a delegated child agent. → Have the child return text; parent writes.
- Reopening a loop with `status: done`. → Create a new loop and reference the old one in `## Starting point`.

## Common Rationalizations

| You say | Reality |
|---------|---------|
| "Grilling would slow us down." | The grill is for both of you. The user finds gaps they didn't know they had; the agent finds branches that weren't named. The slow part is the part you didn't grill, found in implementation. |
| "This DoD line was too ambitious anyway." | The definition of done was approved up-front. Editing it to pass verify hides a failure as a success. Ask the user to approve a scope change; record the change in `## Decisions`. |
| "Small enough change to skip part approval." | The point of approval isn't change size; it's user awareness. A small unapproved change is a small unauditable change. |
| "User just wants a small variation, not a different goal." | If you're not sure, it's a `reframe`. Phase 2 is cheap; silent goal drift is expensive. Surface the pivot and let the user say. |
| "These changes are related, one cycle is fine." | One cycle = one move = one piece of evidence. Batching makes the evidence ambiguous and the route shift unauditable on resume. |
| "Code review on this diff would be overkill." | The verify gate is non-negotiable. If the change is too small for `/code-review`, it is still big enough to clear the gate — there is no exception. |
| "The grill already covered this branch." (after a rework) | If the rework touched it, the prior grill is stale. Re-grill, or record explicitly in `## Decisions` why the prior grill still holds. |

## Quick Reference

**Phase map**

| # | Phase | Gate |
|---|-------|------|
| 1 | Load and Route | — |
| 2 | Align | Alignment gate (hard) |
| 3 | Cycle | — |
| 4 | Verify and Close | Verify gate (hard) |

**Cycle intents** (Phase 3, step 4 — pick one)

- `probe` — throwaway experiment to answer a design, state, or UI question.
- `implement` — production change. Requires the current part plan to be `approved`.
- `validate` — tests, manual checks, external review on existing work.
- `split` — current part is too big; create new parts; re-enter Phase 2.
- `reroute` — same goal, different path.
- `reframe` — goal itself was wrong; re-run Phase 2 alignment gate.
- `stop` — head to Phase 4 or close without verify.

**Status enums**

- Plan status (loop plan and part plan): `awaiting approval | approved | needs rework`
- Part status (under `## Parts`): `todo | doing | done | blocked | dropped`
- Loop frontmatter `status`: `active | done`

**Required skill calls**

| Skill | Required in | When |
|-------|------------|------|
| `/grill-me` | Phase 2 | Mandatory before loop-plan approval |
| `/code-review` | Phase 4 | Mandatory when the loop changed code |
| `/technical-docs` | Phase 4 | Mandatory when user-facing surface changed |
| `/hyper-team` with codex | Phase 2 | Suggested for non-trivial loop plans |
| `/tdd` | Phase 3 | Suggested for `implement` cycles with testable behavior |

**Paths**

- Loop folder: `.hyper/loops/L<N>-<slug>/`
- State file: `.hyper/loops/L<N>-<slug>/loop.md`
- Evidence files: `.hyper/loops/L<N>-<slug>/<kebab-case>.<ext>`

**Timestamps:** `YYYY-MM-DDTHH:MM:SS`

## Template — loop.md

Use the template shipped at [`templates/loop.md`](templates/loop.md) when creating a new loop. Fill the living-state sections from the user's request and any clarifications. Keep the alignment sections (`## Task understanding`, `## Existing code and findings`, `## Loop plan`, `## Part alignment`) before `## Cycles`. Historical changes go to `## Route shifts` or `## Decisions`, not back into the living view.
