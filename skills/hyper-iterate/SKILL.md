---
name: hyper-iterate
description: >
  Runs Hyper's adaptive OODA-style lane for goal-led work where the destination is known or can be stated, but the route should evolve through contact with reality. Creates or resumes loop files under `.hyper/loops/`, keeps the current route, focus, bar, parts, decisions, and recent evidence on disk, and works one small cycle at a time so a new session can resume without re-deriving the whole task. Supports bounded delegated slices when the host agent can spawn sub-agents, while keeping one parent-owned loop as the source of truth. Use when the user asks to work iteratively, course-correct while implementing, try things in sequence, split a goal into adaptive slices, or learn from live behavior without committing to the full phase workflow. Keywords: hyper, iterate, adaptive, ooda, loop, course correct, probe, implement, slice, exploratory, delegate.
---

# hyper-iterate

Run tracked adaptive work without entering the full Hyper phase workflow.

This skill is Hyper's OODA-style lane: observe reality, orient on what it
means, decide the next move, act, then repeat. Use it when the goal is known or
can be stated, but the route should stay flexible while the work unfolds.

Resolve the Hyper state root per `../hyper/reference/state-root.md` before
reading or writing `.hyper/` paths. Ensure `.hyper/` is bootstrapped per
`../hyper/reference/bootstrap.md`, then create `<hyper-state-root>/.hyper/loops/`
if it does not exist.

If `<hyper-state-root>/.hyper/rules.md` exists, read it once before acting and
honor it as project-local standing guidance.

This skill owns `<hyper-state-root>/.hyper/loops/`. It does not create task
folders or phase artifacts. When the Hyper state root differs from the current
working tree, use absolute paths for loop artifacts so reads and writes still
land in the main project directory.

## What this skill is for

Use this skill when the work should move toward a destination, but the route
should emerge through contact with the codebase, the running system, and the
results of prior steps.

Good fits:

- implementing a feature or refactor in adaptive slices instead of freezing a
  full execution plan up front
- reproducing, debugging, and fixing a bug while the likely root cause is still
  moving
- improving agent-facing or user-facing behavior where quality must be observed
  in real behavior, not inferred from a plan alone
- integration work where each answer changes what the next useful move should be
- any tracked work where durable state matters but the full Hyper task workflow
  would be too stiff

Bad fits:

- work that already needs approval gates, worker-safe slicing, or explicit
  multi-phase coordination
- pure research with no direct system contact or implementation path
- tiny obvious edits that do not need durable state

When the route stabilizes and coordination matters more than adaptation,
recommend switching to `hyper` or `hyper-task`. Do not migrate the work
automatically.

## Loop artifact

Store one file per loop at `<hyper-state-root>/.hyper/loops/L<N>-<slug>.md`.
Create new files from `templates/loop.md`.

A loop is a durable navigation record, not just a probe log. It has two kinds
of content:

- **Living state** — frontmatter `status` and `updated`, plus `## Goal`,
  `## Why`, `## Constraints`, `## Non-negotiables`, `## Definition of done`,
  `## Current route`, `## Current focus`, `## Current bar`, `## Parts`,
  `## Handoff cues`, `## Memory candidates`, and `## Outcome`
- **Evidence history** — `## Bar history`, `## Route shifts`, `## Decisions`,
  `## Starting point`, and `## Cycles`

Update living state when reality changes. Append to evidence history; do not
rewrite old cycles to make the work look cleaner than it was.

Done loops stay done. Extending the work means creating a new loop, not
reopening the old one.

## Routing

Pick exactly one path:

1. **Resume by path** — if the user supplies an absolute path under `.hyper/loops/`; derive the Hyper state root from that path per `../hyper/reference/state-root.md`, then resume that loop.
2. **Resume by id** — if the user names `L<N>`.
3. **Resume by match** — if the user names an existing loop title clearly.
4. **Resume the only active loop** — if no id is given and exactly one active loop exists.
5. **Ask** — if multiple active loops exist and the target is ambiguous.
6. **Create** — otherwise.

Active means frontmatter `status: active`.

## Create

1. Scan `<hyper-state-root>/.hyper/loops/*.md` for the highest `L<N>` and allocate the next id.
2. Derive a short title and kebab-case slug.
3. Fill `## Goal` from the user's request in one or two tight sentences.
4. Fill `## Why` from the user's stated motivation when present; otherwise write `Not stated yet.`
5. Fill `## Constraints`:
   - list the user's explicit constraints when present
   - otherwise write `- None stated.`
6. Fill `## Non-negotiables`:
   - list invariants that must hold while the work evolves
   - otherwise write `- None stated.`
7. Fill `## Definition of done` from the user's stated end goal when present.
   - if the request implies the destination, write the clearest current end state you can justify
   - ask once only if the destination is still unclear after that
8. Fill `## Current route` with the best current route hypothesis in two or three sentences. This is a route, not a frozen plan.
9. Fill `## Current focus` with the first slice, question, or boundary to work on.
10. Determine the initial bar:
   - if the user named a concrete near-term stop point, use it
   - otherwise write the narrowest useful bar that moves the route forward now
11. Fill `## Parts`:
   - if the work naturally decomposes, list the first 2 to 5 meaningful slices as `P<N> — <title> — <todo|doing>`
   - otherwise write `- P1 — Whole goal — doing`
12. Fill `## Starting point` with what is already known before cycle 1.
   - use concrete facts already established in the request when available
   - otherwise write `Unknown.`
13. Write `<hyper-state-root>/.hyper/loops/L<N>-<slug>.md` from `templates/loop.md`.
14. Announce: `Created L<N> — <title>. Starting adaptive loop.`

## Resume

Read the loop file before acting. Focus on:

- `## Goal`
- `## Definition of done`
- `## Current route`
- `## Current focus`
- `## Current bar`
- `## Parts`
- latest `## Bar history` entry when present
- latest `## Route shifts` and `## Decisions` entries when present
- `## Handoff cues`
- the last one or two cycles
- `## Outcome` when filled

If the loop is already `status: done`, report the outcome and stop. Do not
reopen done loops. If the user wants to continue from the same learning, create
a new loop and carry the old loop forward as context in `## Starting point`.

## Working cycle

Run one adaptive cycle at a time unless the user explicitly asks for a batch.

For each cycle:

1. **Observe** — read or run only enough code, logs, docs, tests, or prior state to see the next useful move.
2. **Orient** — state what matters now: the active hypothesis, the current risk, the route question, or the reason this slice is next.
3. **Decide** — choose exactly one cycle intent: probe, implement, validate, split a part, reroute, or stop.
4. **Act** — make the smallest meaningful move that advances the chosen intent. This can be a probe, a code change, a validation pass, a decomposition step, or a route correction.
5. **Evidence** — capture the exact result: error text, command output, test result, tool response, screenshot note, diff summary, or observed behavior.
6. **Learning** — say what the evidence changed in your understanding of the goal, route, parts, or risks.
7. **Update living state** — update `## Current route`, `## Current focus`, `## Current bar`, `## Parts`, `## Handoff cues`, or `## Memory candidates` if the cycle changed them.
8. **Next** — choose one of: continue, back up, split further, validate, stop, or promote to full Hyper.
9. Append the cycle to the loop file and update frontmatter `updated`.

Use the cycle entry shape from `templates/loop.md`.

## Delegation inside long loops

If the host agent supports sub-agents, the parent session may delegate a
bounded slice when local recon, research, implementation, validation, or review
would otherwise overload the main session. The parent still owns the loop
artifact and all route decisions.

Use delegation for:

- local codebase recon on one part or boundary
- external research that would otherwise flood the main session
- implementation of one clearly bounded part
- focused validation or long-running checks
- adversarial review of a meaningful change

Do not delegate the whole loop. The parent session stays responsible for:

- `## Goal`, `## Definition of done`, `## Current route`, and `## Current focus`
- part selection and part-state updates
- `## Decisions`, `## Handoff cues`, and `## Memory candidates`
- deciding whether to continue, reroute, split further, stop, or promote to
  full Hyper

When delegating, give the child a compact contract derived from the loop:

- loop id and title
- overall goal
- relevant constraints and non-negotiables
- current route and current focus
- the exact part or question the child owns
- any recent decisions the child must preserve
- expected validation
- explicit stop rules and what the child must not decide alone

Prefer:

- fresh-context children for recon, research, and adversarial review
- one writer at a time for implementation
- parent-side synthesis after every child return before another route change

After a child finishes, the parent integrates only the durable result back into
the loop: update the relevant part, append a cycle entry with the evidence,
refresh handoff cues if needed, and log any load-bearing route decision.

## Bars, route shifts, and parts

If the near-term success criterion changes, do both before the next cycle:

1. update `## Current bar`
2. append one bullet to `## Bar history` with timestamp and the reason for the shift

If the route changes materially, do both before the next cycle:

1. update `## Current route`
2. append one bullet to `## Route shifts` with timestamp and the reason for the shift

If the work needs decomposition or a part changes state, update `## Parts` using
only these statuses: `todo`, `doing`, `done`, `blocked`, `dropped`.

Use `## Decisions` only for load-bearing choices a future session would need to
understand the route. Routine progress does not belong there.

## Handoffs and durable learnings

At useful pause points, sort new information into the right bucket:

- `## Handoff cues` — what a new session should know first that is not obvious
  from the rest of the file
- `## Memory candidates` — possible cross-task lessons that may deserve
  promotion later
- `## Decisions` — route-shaping choices already made
- `## Cycles` — detailed evidence history

Keep `## Handoff cues` current. Remove stale cues when they are no longer useful
for a restart.

Do not write `.hyper/memory.md` or `.hyper/rules.md` by default from this
skill. When the user explicitly asks to preserve a durable lesson beyond this
loop:

1. read `../hyper/reference/memory.md`
2. append only the truly cross-task learning to `.hyper/memory.md`
3. use `.hyper/rules.md` only for standing project rules the user wants to make normative

## Stop conditions

Mark frontmatter `status: done` and fill `## Outcome` when:

- the definition of done is met
- the user decides the current scope is complete enough
- the work should now move into a planned `hyper` task

If the current bar is met but the destination is not, raise or replace the bar
and continue later. If the user stops mid-stream without closing the work,
leave `status: active` and refresh `## Handoff cues`. The loop file is the
resume point.

## Rules

- Do not create `01-intake.md`, `02-spec.md`, `03-technical-plan.md`, `04-execution-plan.md`, or task folders from this skill.
- Prefer live system feedback over more reading when reality can answer faster.
- Use the smallest meaningful move, not necessarily the smallest possible probe.
- Keep `## Goal`, `## Current route`, and `## Parts` concise enough that a new session can rehydrate quickly.
- Record evidence verbatim where practical. Do not paraphrase away the signal.
- Do not batch multiple unrelated moves into one cycle.
- Do not reopen a done loop; start a new one if the work continues.
- Keep memory sparse. Not every local learning deserves promotion beyond the loop.
- When using sub-agents, keep one navigation authority: the parent loop owner.
- Do not let child sessions mutate the loop artifact directly; integrate their results in the parent session.
- Prefer one writer at a time unless the parts are truly isolated and the host provides safe isolation.
- When the work now needs approvals, worker-safe slicing, or broader coordination, recommend switching to `hyper`.
