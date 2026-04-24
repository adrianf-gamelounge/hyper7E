# Hyper Authoring Invariants

Canonical list of drift invariants for **the shipped Hyper skills under `skills/**`** — the code that installs into other projects. Rules here govern `SKILL.md` bodies, `templates/`, and `reference/` files inside `skills/`. They do **not** cover this repo's maintainer surface (`AGENTS.md`, `README.md`, `.claude/skills/**`, `docs/`, `scripts/`) — that scope is owned by `review-hyper-skills` Mode 2 (`maintainer-drift`) and lives in the review skill's own body.

This file is cited by `AGENTS.md` (authoring-time guidance) and by `review-hyper-skills/SKILL.md` (review-time axis for Mode 1 and shipped-skill findings in Mode 3). Keep it as the single source for the shipped-skill scope — if a rule belongs here, it lives here and only here.

Each rule carries a short rationale and a quick test. A finding against any of these needs a smallest-safe-fix, not just a complaint.

## Content and structure

- **Single source of truth.** Every contract (table, enum, snippet, mechanic) has exactly one file that owns it. Every other mention is a pointer, not a copy. *Test: if you change the rule in one place, does another file silently disagree? If yes, one of them has to go.*
- **No dead surface area.** If no skill reads or writes a field, value, artifact, or code path, delete it. Unused options mislead more than they enable. *Test: grep the string across `skills/`. Zero producers or zero consumers → remove it.*
- **No restatement sections.** `SKILL.md` bodies don't carry "Key principles", "Additional resources", or "Rules" bullets that repeat the flow. `## Rules` lists only novel operational constraints a careful reader would otherwise miss. *Test: could a reader who scanned the body have inferred this bullet? If yes, drop it.*
- **No overengineered workflow.** Every step, section, guard, and abstraction must pay for itself. Collapse defensive machinery whose risk is not named, and merge numbered steps that could be one. *Test: if you removed this step or section, what concrete failure appears?*
- **Name-drop over re-explain.** When a concept has a standard name (SOLID, YAGNI, DRY, idempotency, Chesterton's fence, LRU, exponential backoff, etc.), cite the name rather than re-teaching it. Re-explanation is restatement wearing a different hat. *Test: is the explanation longer than the name plus one sentence of context?*

## Naming and scope

- **One artifact name per concept.** Branches live inside the artifact, not in the filename. `exploration.md` carries the bugfix body when needed; there is no `exploration-bugfix.md`. *Test: would a downstream skill need an OR-clause to find this file? If yes, collapse to one name.*
- **Scope every section to where it applies.** If a subsection is only meaningful in one scope or branch, state the condition and keep it out of the others. *Test: does this section exist on artifacts where nobody reads it? If yes, narrow the scope.*

## Skill responsibilities

- **Pure-producer phase skills.** Phase skills produce an artifact and return a verdict; they don't mutate `task.md` `phase:` / `awaiting:`, decide transitions, or patch state owned by another skill. `hyper` interprets the verdict and owns the transition. *Test: does this skill both produce output and decide where work goes next? If yes, split.*
- **Shared mechanics live in `reference/`.** Copy-pasted multi-line snippets across skills (archive moves, bootstrap blocks, validation recipes) go into a reference file; call sites become one-liners. *Test: is the same block in two `SKILL.md` files? If yes, extract.*

## Portability and provenance

- **Portability.** No accidental host-specific sprawl outside documented exceptions. No Claude-Code-only tool names in skill bodies (the one documented exception is `hyper-implement` naming the Task tool for sub-agent dispatch). *Test: would this skill body work on any agent implementing the Agent Skills spec?*
- **Provenance hygiene.** Nothing written into this repo — skill bodies, README, docs, code comments, any file the agent touches — carries provenance: no absolute local paths (`/Users/...`, `/home/...`, `~/Projects/...`), no external or predecessor repo names, no concrete historical task ids (`T39`, `T40.2`). Placeholder examples that teach a format (`T<N>`, `T1`, `T1.3`, `/path/to/thing`) are fine; concrete references that only mean something to the author are not. Enforced universally by `hyper-plan-review` and `hyper-code-review`. *Test: would a downstream reader with no access to this repo's history benefit from this reference? If no, it is provenance — move it out.*

## Cross-file agreement

- **Cross-file contract surfaces agree.** Filenames, enum values, verdict vocabularies, and required fields must agree across every producer and consumer inside `skills/`. *Test: does every consumer match the authority file's names and fields exactly?*

## When to apply

- At authoring time: when editing any file under `skills/**` — adding a skill, changing an enum, extending a reference — check whether the edit is enforcing one of these rules or violating one.
- At review time: `review-hyper-skills` uses this list as its evaluation axis for Mode 1 (`contract-drift`) and for shipped-skill findings in Mode 3 (`suite-evaluation`). Mode 2 (`maintainer-drift`) operates on this-repo surfaces and has its own criteria inside the review skill's body.
