# Provider Capability Matrix

Purpose: cross-provider quick reference for the one capability that varies in ways Step 5 of `SKILL.md` needs at prompt-build time — JSON schema output support. Per-provider CLI invocation, response extraction, multi-turn commands, and gotchas live in each provider file under `references/providers/<name>.md` (sections 4, 6, 8, and 10 respectively) and are intentionally not duplicated here.

## JSON Schema Support

| Provider | Supported | Flag |
|----------|-----------|------|
| Codex | Yes | `--output-schema <FILE>` (file path, not inline JSON) |
| Claude | Yes | `--json-schema '<inline JSON>'` (inline JSON, not a file path) |
| Gemini | Not verified | — |
| Copilot | No | — |

When a provider's row says "Yes", Step 5 may use structured output with that provider; otherwise the XML output contract in the prompt template enforces structure.
