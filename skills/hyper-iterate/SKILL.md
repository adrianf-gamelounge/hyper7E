---
name: hyper-iterate
description: >
  Runs a lightweight probe-sense-respond loop for exploratory coding work. Creates or resumes loop files under `.hyper/loops/`, records the current bar, and works one small hypothesis-driven cycle at a time instead of forcing a full plan. Use when the user says to replicate first, try something inline, work by trial and error, or learn from live behavior before planning. Keywords: hyper, iterate, probe, loop, exploratory, trial and error, repro, inline.
---

# hyper-iterate

Run tracked exploratory work without entering the full Hyper phase workflow.

Resolve the Hyper state root per `../hyper/reference/state-root.md` before
reading or writing `.hyper/` paths. Ensure `.hyper/` is bootstrapped per
`../hyper/reference/bootstrap.md`, then create `<hyper-state-root>/.hyper/loops/`
if it does not exist.

This skill owns `<hyper-state-root>/.hyper/loops/`. It does not create task
folders, phase artifacts, backlog entries, or memory entries. When the Hyper
state root differs from the current working tree, use absolute paths for loop
artifacts so reads and writes still land in the main project directory.

## What this skill is for

Use this skill when the next useful answer should come from a live probe, not
from a long plan.

Good fits:

- reproducing a bug on a live system before designing the fix
- trying a small inline change, retesting, and adjusting
- improving agent-facing or user-facing behavior where quality must be observed
- exploratory work where the user explicitly wants trial and error
- small but important fixes where durable notes help and a full task would be overhead

Bad fits:

- broad multi-slice work with a stable design shape
- work that already needs execution-plan coordination
- pure research with no probes or code changes

When the work becomes stable enough that coordination matters more than
exploration, recommend switching to `hyper` or `hyper-task`. Do not migrate the
work automatically.

## Loop artifact

Store one file per loop at `<hyper-state-root>/.hyper/loops/L<N>-<slug>.md`.

Create new files from `templates/loop.md`.

A loop file is append-only except for:

- frontmatter `status` and `updated`
- `## Current bar`
- `## Outcome`

Done loops stay done. Extending the work means creating a new loop, not
rewriting the old one.

Everything else is evidence history. Do not rewrite old cycles to make the work
look cleaner than it was.

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
4. Determine the initial bar:
   - if the user named a concrete success condition, use it
   - otherwise write the narrowest useful bar you can justify from the request
   - ask once only if the bar is still unclear after that
5. Fill `## Constraints`:
   - list the user's explicit constraints when present
   - otherwise write `- None stated.`
6. Fill `## Starting point` with what is already known before cycle 1.
   - use concrete facts already established in the request when available
   - otherwise write `Unknown.`
7. Write `<hyper-state-root>/.hyper/loops/L<N>-<slug>.md` from `templates/loop.md`.
8. Announce: `Created L<N> — <title>. Starting probe loop.`

## Resume

Read the loop file before acting. Focus on:

- `## Goal`
- `## Current bar`
- latest `## Bar history` entry
- `## Constraints`
- `## Starting point`
- the last one or two cycles
- `## Outcome` when filled

If the loop is already `status: done`, report the outcome and stop. Do not
reopen done loops. If the user wants to continue from the same learning, create
a new loop and carry the old loop forward as context in `## Starting point`.

## Working cycle

Run one small cycle at a time unless the user explicitly asks for a batch.

For each cycle:

1. **Orient** — read only enough code, logs, docs, or prior cycles to choose the next probe.
2. **Hypothesis** — name what you expect and why.
3. **Probe** — make the smallest change or run the smallest test that can answer the question.
4. **Evidence** — capture the exact result: error text, command output, test result, tool response, screenshot note, or observed behavior.
5. **Learning** — say what the evidence changed in your understanding.
6. **Next** — choose one of: next probe, back up and rethink, or stop.
7. Append the cycle to the loop file and update frontmatter `updated`.

Use the cycle entry shape from `templates/loop.md`.

## Bar shifts

If the success criterion changes, do both before the next cycle:

1. update `## Current bar`
2. append one bullet to `## Bar history` with timestamp and the reason for the shift

A bar shift is normal. Log it explicitly instead of pretending the old bar was
never there.

## Stop conditions

Mark frontmatter `status: done` and fill `## Outcome` when:

- the current bar is met
- the user decides the current learning is enough
- the work should now move into a planned `hyper` task

If the user stops mid-stream without closing the work, leave `status: active`.
The loop file is the resume point.

## Rules

- Do not create `01-intake.md`, `02-spec.md`, `03-technical-plan.md`, `04-execution-plan.md`, or task folders from this skill.
- Prefer a live probe over more reading when the running system can answer faster.
- Keep changes and tests small enough that a bad probe is cheap to revert.
- Record evidence verbatim where practical. Do not paraphrase away the signal.
- Do not batch multiple unrelated probes into one cycle.
- Do not reopen a done loop; start a new one if the work continues.
- Do not write a long plan unless the user explicitly asks to promote the work out of iterate mode.
