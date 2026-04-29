---
name: hyper-code-review
description: >
  Reviews a diff through contract-compliance, bug-finding, and standards-compliance passes, then writes a single review block with a pass, needs-changes, or blocked verdict. Works in embedded mode for hyper-verify and standalone mode for direct user review requests. Keywords: hyper, code review, review, bugs, standards, diff, PR review.
---

# hyper-code-review

Review code changes for bugs, regressions, contract violations, missing tests,
and standards problems.

Resolve the Hyper state root per `../hyper/reference/state-root.md` before
reading or writing `.hyper/` paths when working inside a Hyper task.

## Modes

### Embedded mode

Used by `hyper-verify`.

Inputs:

- current diff
- `task.md`
- feature scope: `02-spec.md`, `03-technical-plan.md`, `04-execution-plan.md`
- quick scope: `03-technical-plan.md`
- subtask completion records when present

Output:

- a review block for `checks.md`

### Standalone mode

Used when the user directly asks for a review.

1. Inspect the requested diff, branch, PR, or staged changes.
2. Create a `scope: code-review` task only when the user wants the review
   tracked under `.hyper/`.
3. Return findings first, ordered by severity, with file and line references.
4. If tracked, write `checks.md`, set `phase: done`, and archive the folder.

## Review passes

- Contract compliance: does the code match the accepted artifacts or user
  request?
- Bug finding: logic errors, edge cases, races, state leaks, security issues,
  data loss, and behavioral regressions.
- Test adequacy: missing or weak tests for changed behavior.
- Standards compliance: project conventions and maintainability issues.

## Verdicts

- `pass` — no blocking findings
- `needs-changes` — actionable issues must be fixed
- `blocked` — review cannot be completed with current information

Do not bury findings under a summary. Findings are the primary output.
