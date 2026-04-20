#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"
DATA_MODEL = ROOT / "skills" / "hyper" / "reference" / "data-model.md"

USER_FACING_HYPER = {
    "hyper",
    "hyper-task",
    "hyper-backlog",
    "hyper-handoff",
    "hyper-retro",
}
INTERNAL_HYPER = {
    "hyper-explore",
    "hyper-plan",
    "hyper-implement",
    "hyper-worker",
    "hyper-verify",
    "hyper-docs",
}

ERRORS: list[str] = []


def fail(msg: str) -> None:
    ERRORS.append(msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        fail(f"{path}: missing frontmatter block")
        return {}
    body = m.group(1)
    result: dict[str, str] = {}
    current_key = None
    current_value_lines: list[str] = []
    for raw_line in body.splitlines():
        if re.match(r"^[A-Za-z0-9_-]+:\s*", raw_line):
            if current_key is not None:
                result[current_key] = "\n".join(current_value_lines).strip()
            key, value = raw_line.split(":", 1)
            current_key = key.strip()
            current_value_lines = [value.strip()]
        else:
            if current_key is None:
                fail(f"{path}: could not parse frontmatter line: {raw_line!r}")
                return {}
            current_value_lines.append(raw_line)
    if current_key is not None:
        result[current_key] = "\n".join(current_value_lines).strip()
    return result


def extract_reference_paths(text: str) -> list[str]:
    return re.findall(r"`((?:\.\./)?(?:templates|reference)/[^`]+\.md)`", text)


def validate_skill_files() -> None:
    skill_dirs = sorted([p for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").exists()])
    names = {p.name for p in skill_dirs}
    expected = USER_FACING_HYPER | INTERNAL_HYPER | {"team"}
    if names != expected:
        missing = expected - names
        extra = names - expected
        if missing:
            fail(f"skills/: missing expected skill dirs: {sorted(missing)}")
        if extra:
            fail(f"skills/: unexpected skill dirs: {sorted(extra)}")

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        text = read(skill_file)
        line_count = text.count("\n") + 1
        if line_count > 500:
            fail(f"{skill_file}: exceeds 500 lines ({line_count})")

        fm = parse_frontmatter(text, skill_file)
        name = fm.get("name", "").strip().strip('"\'')
        desc = fm.get("description", "")
        desc_clean = re.sub(r"^>\s*", "", desc, flags=re.M).strip().strip('"\'')
        if name != skill_dir.name:
            fail(f"{skill_file}: frontmatter name {name!r} does not match dir {skill_dir.name!r}")
        if not desc_clean:
            fail(f"{skill_file}: missing description")
        if len(desc_clean) > 1024:
            fail(f"{skill_file}: description exceeds 1024 chars ({len(desc_clean)})")

        user_invocable = fm.get("user-invocable", "").strip().lower()
        if skill_dir.name in INTERNAL_HYPER and user_invocable != "false":
            fail(f"{skill_file}: internal Hyper skill must set user-invocable: false")
        if skill_dir.name in USER_FACING_HYPER and user_invocable == "false":
            fail(f"{skill_file}: user-facing Hyper skill must not set user-invocable: false")

        for rel in extract_reference_paths(text):
            ref_path = (skill_dir / rel).resolve() if not rel.startswith("../") else (skill_dir / rel).resolve()
            try:
                ref_path.relative_to(ROOT)
            except ValueError:
                fail(f"{skill_file}: reference escapes repo root: {rel}")
                continue
            if not ref_path.exists():
                fail(f"{skill_file}: referenced file does not exist: {rel}")

        for invoked in re.findall(r"Invoke the `([a-z0-9-]+)` skill", text):
            if invoked not in names:
                fail(f"{skill_file}: invokes missing skill {invoked!r}")
        for loaded in re.findall(r"Load the `([a-z0-9-]+)` skill", text):
            if loaded not in names:
                fail(f"{skill_file}: loads missing skill {loaded!r}")


def ensure_contains(path: Path, needle: str) -> None:
    text = read(path)
    if needle not in text:
        fail(f"{path}: missing expected text: {needle!r}")


def validate_readme_and_data_model() -> None:
    ensure_contains(README, "Five Hyper skills are user-facing.")
    ensure_contains(README, "Six internal Hyper skills run under the hood")
    for skill in sorted(USER_FACING_HYPER | INTERNAL_HYPER | {"team"}):
        ensure_contains(README, f"`{skill}`")

    ensure_contains(DATA_MODEL, "Users invoke five Hyper skills directly")
    ensure_contains(DATA_MODEL, "plus `hyper-worker` are internal")
    ensure_contains(DATA_MODEL, "`hyper-backlog promote B<N>` turns an idea into a task")
    ensure_contains(DATA_MODEL, "`phase: deferred`")
    ensure_contains(DATA_MODEL, "## `handoff.md`")
    ensure_contains(DATA_MODEL, "## `retro.md`")


def main() -> int:
    validate_skill_files()
    validate_readme_and_data_model()
    if ERRORS:
        print("Hyper validation failed:\n")
        for err in ERRORS:
            print(f"- {err}")
        return 1
    print("Hyper validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
