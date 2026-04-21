---
name: evaluate-hyper
description: >
  Evaluates the shipped Hyper skill suite under `skills/` as it exists on disk right now. Use when the user asks to evaluate Hyper, audit the Hyper skills, or check drift between Hyper skills and their bundled reference files. Not for reviewing diffs, pull requests, commits, or commit ranges — this skill judges current state, not changes. Supports drift audits and wider suite evaluations. Keywords: Hyper, evaluate, audit, drift, skills, data-model, gates, workflow, current state.
---

# evaluate-hyper

Use this skill for **Hyper-on-Hyper** evaluation of the shipped skill suite under `skills/`: `skills/hyper*`, companion skills that ship with Hyper, and their bundled `reference/` and `templates/` files. This is not a generic code-review skill.

## What this evaluates

**Current state on disk, not changes.** The target is whatever is in `skills/` right now — the files as a reader sees them. This skill does not evaluate diffs, pull requests, individual commits, commit ranges, or "what a recent change did." If the user wants a diff or PR reviewed, that is a different job and this skill is the wrong tool; redirect them rather than silently pivoting into a change review.

Concretely:

- Read files, not `git diff` / `git log`.
- Judge what exists, not what was added, removed, or rewritten.
- Do not map findings to commits or SHAs.
- Do not frame findings as "this commit introduced…" or "this PR regressed…".

The user handing you recent commit output or a branch name does not change the target. The target is still the current files.

## Authorities

Treat these as contract surface when judging drift:

- `skills/hyper/reference/gates.md` — phase transitions, verdicts, awaiting values.
- `skills/hyper/reference/data-model.md` — task.md fields, artifact filenames, subtask shape.
- `skills/hyper/SKILL.md` — orchestrator behavior.
- Each phase skill's own `SKILL.md` for its own phase.

**Not authorities** for shipped-skill behavior: `README.md`, `AGENTS.md`, operating/maintaining guides. They document the repo, not the contract. Only reach for them when the user explicitly asks for a repo-maintainer review.

`reference/*.md` is contract, not prose. `templates/` is bundled shape, not an alternate artifact name.

## Pick a mode

- **Drift audit** — one target contract against one axis (e.g. `data-model.md` vs live usage, `gates.md` vs `hyper/SKILL.md`, one phase skill vs its templates).
- **Suite evaluation** — broad review of the workflow or skill set as it stands. Use when the user explicitly asks for a wider pass across multiple skills.

Both modes operate on the current state of `skills/`. There is no "review the recent change" mode — that is intentionally outside this skill.

If the user says "review everything" with no axis, narrow it first. Pick the smallest honest scope and state it.

## Workflow

### 1. Lock the scope

State:

- the mode
- the target files
- the evaluation axis

Good axes:

- "drift between documented and live `task.md` fields"
- "duplicated contract surface between `gates.md` and `hyper/SKILL.md`"
- "dead surface in `hyper-verify/templates/checks.md` vs what the skill actually writes"

All axes are about the state of files today. An axis framed around a change, a commit, or a PR is out of scope — redirect rather than adopt it.

If the user drifts mid-pass, restate the locked axis out loud. Do not silently widen. If the new angle is worth pursuing, finish this pass first and queue the next.

### 2. Gather evidence before judging

Evidence comes from reading files on disk. Do not read commits, diffs, or `git log` for this skill's work — if those are relevant, the user is asking for something other than an evaluation of current state.

For **drift audits**:

- read the authoritative file first
- grep every producer and consumer across `skills/`
- classify each surface as `live`, `dead`, or `ambiguous`

For **suite evaluations**:

- start from the highest-authority or highest-friction surfaces (`gates.md`, `data-model.md`, `hyper/SKILL.md`)
- then the phase skill or doc touched by the concern
- read each skill end-to-end before judging; sampling causes false drift findings

### 3. Evaluate against Hyper's invariants

Default rubric:

- single source of truth
- no dead surface area
- no restatement sections ("Rules", "Key principles", "Additional resources" tails)
- one artifact name per concept
- scope sections only where they apply (e.g. quick vs feature branches)
- pure-producer phase skills; orchestrator owns phase/awaiting
- shared mechanics extracted to `reference/`
- portability: no accidental CLI or host-specific sprawl outside documented exceptions

### 4. Produce the output

Every finding must include:

- a **line-anchored citation** (`path/to/file.md:80`)
- a **severity** (load-bearing / drift / nit)
- a **smallest safe fix**
- a **route**: direct edit, new Hyper task, or backlog item

Cap findings at **3–8**. Beyond that, signal dilutes — fold nits into one aggregate line or drop them.

Mode-specific output:

- **Drift audit** — scope, findings, smallest fix per finding.
- **Suite evaluation** — "what works / what's drifting / what to do", ending with **top 3 fixes that would make the biggest difference**. This distillation is required.

Findings describe the current file, not a change to it. Phrase them as *"`gates.md:44` lists `review` in the phase-transition table but `hyper/SKILL.md:132` omits it from the dispatch table"*, not *"commit X introduced a mismatch"*.

### 5. Edit only if the user says apply

By default, evaluate and stop. If the user says apply:

- one finding per commit
- re-grep after each edit to confirm the drift or dead surface is actually gone
- never touch files outside the declared target ("while I'm here" edits are a known failure mode)
- never edit `reference/*.md` from a non-evaluation context masquerading as this skill

### 6. Handle pushback

When the user challenges a finding:

- if the defence fits in ~3 lines with concrete evidence, state it once
- otherwise drop the finding cleanly and move on
- if a false-duplication claim is being rejected, an orthogonal-axis table (skill × behavior) is the standard move

Do not mount long defences of weak findings.
