---
name: hyper-explore
description: Runs the explore phase of a Hyper task. Clarifies the user's goal, scans the codebase for relevant files and patterns, classifies scope (quick, feature, or research), and writes an approved exploration.md with findings and a proposed approach. Use when a Hyper task is in the 'explore' phase (check task.md frontmatter), or when the user wants to investigate a problem before implementing. Invoked by the `hyper` skill — not user-facing. Keywords: hyper, explore, investigate, clarify, approach, scope, exploration.md.
user-invocable: false
---

# hyper-explore

You are in the **explore** phase of a Hyper task. The goal: understand what the user actually wants, figure out what already exists, and agree on an approach — in one interactive session.

This phase runs first on every task. No code gets written until the user approves the approach.

## Inputs

- Task folder at `.hyper/tasks/T<N>-<slug>/` with `task.md` already created
- Any existing `exploration.md` (if resuming after revision requests)

## Outputs

- `exploration.md` with **Findings** + **Approach**
- `task.md` frontmatter updated: `scope: quick | feature | research` and `awaiting: user-approval`
- Phase stays at `explore` until the user approves — then you advance to the next phase

## Flow

```
read task.md
  │
  ├── clarify the goal (if needed)
  │
  ├── classify scope (quick / feature / research)
  │
  ├── scan the codebase — facts, not opinions
  │
  ├── (if research) produce findings; (otherwise) draft approach
  │
  ├── write exploration.md
  │
  └── set awaiting: user-approval and stop
```

## Step 1 — Clarify the goal

Read the task body. Does it unambiguously describe what to do?

- **Clear** → continue to scope classification.
- **One likely interpretation** → state it and ask one question: *"I read this as X. Sound right?"*
- **Multiple plausible interpretations** → ask *one* multiple-choice question with a default.
- **Vague / no goal** → summarize your understanding in 4 bullets and ask the user to correct.

Never ask more than one clarification question per message. Stop and wait for the answer. When you get it, continue.

## Step 2 — Classify scope

Pick one:

- **quick** — one file (or a few related lines), easily reversible, clear single change, no new abstractions. Examples: rename, typo fix, config tweak, one-line bug fix, small refactor inside one function.
- **feature** — anything else that produces code changes. Multiple files, new abstractions, test changes, non-trivial behavior.
- **research** — investigation, audit, comparison, feasibility study. No code changes expected. Terminates at `exploration.md` with findings + recommendation.

**Size is not the criterion.** A one-line change to auth, payments, or migrations is *not* quick. Quick means *impact is small enough that the plan phase adds no value*.

When in doubt, choose `feature`.

Write the scope into `task.md` frontmatter (`scope: quick | feature | research`).

## Step 3 — Scan the codebase

Use Grep/Glob/Read to find what matters for this task:

- Files the change will touch
- Existing patterns to follow (how similar things are done elsewhere)
- Conventions (naming, structure, where tests live)
- Related code that might break

Go as deep as the scope demands. For `quick`, a few targeted searches are enough. For `feature`, read the relevant modules end-to-end. For `research`, be thorough — this is the work.

**Facts only here.** No design decisions yet. If you find something surprising or undocumented, note it.

If the task is a bugfix or regression, ask the user for error output, logs, or a failing test case *before* diving into the code. They have context you don't.

## Step 4 — Draft the approach

For **quick** tasks: two or three sentences describing the change and the files involved.

For **feature** tasks: one or two paragraphs covering:
- What you'll change (files, modules)
- Why this approach over alternatives (name at least one alternative even if you immediately rule it out)
- Any new abstractions, dependencies, or test changes
- Trade-offs the user should know about

For **research** tasks: this section becomes **Findings & Recommendation**. Structured around the actual research question, with evidence from the code and external sources where relevant. End with a clear recommendation.

**YAGNI applies.** Remove scope you added for hypothetical needs. Tight > ambitious.

## Step 5 — Write `exploration.md`

Use the shape in `templates/exploration.md` (bundled with this skill). It has two sections — **Findings** and **Approach** — with subsections for files to change and out-of-scope. For research tasks, rename **Approach** to **Findings & Recommendation** and omit the "Files to change" subsection.

## Step 6 — Set approval gate and stop

Update `task.md` frontmatter: `awaiting: user-approval`.

Tell the user: *"Wrote `exploration.md`. Scope: <quick|feature|research>. Please read it and tell me to proceed, or what to change."*

**Stop.** Do not advance to the next phase. The user must read the file and respond.

## When the user responds

- **Approves** → clear `awaiting`, update `phase:` to the next value (`plan` for feature, `implement` for quick, `done` for research), write the approval decision into the body of `exploration.md` if useful, and return control to the `hyper` skill.
- **Requests changes** → clear `awaiting`, stay in `explore`, revise `exploration.md`, then re-set `awaiting: user-approval` and stop again.
- **Asks a question** → answer, stay in `explore`, don't clear `awaiting`.

## Rules

- **Scan before asking.** Many "ambiguous" goals become clear after reading the code for two minutes. Don't fire off questions the codebase would answer.
- **One question per message.** Always with a default or multiple choice.
- **Facts and design are separate.** Findings are what *is*. Approach is what we'll *do*. Don't mix them.
- **Approval is explicit.** Agent judgment is not a substitute for "yes, go".
- **Length proportional to scope.** A `quick` exploration.md fits on one screen. A `feature` one is a page or two. A `research` one is as long as the evidence demands.

## Key principles

- The user should be able to read `exploration.md` alone and know what's about to happen. That's the clarity Hyper promises.
- If you catch yourself writing scope you're not sure the user asked for, stop and ask.
- Unexamined assumptions are where wasted work comes from. Surface them as explicit questions, not as hidden defaults in the approach.

## Additional resources

- `templates/exploration.md` — ready-to-fill template for the artifact this skill produces.
