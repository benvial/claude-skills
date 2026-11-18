---
name: setup-local-dev
description: Prepare a cloned repo for local agent work — create AGENTS.md with a CLAUDE.md symlink and route every agent-generated file into .git/info/exclude so none reach commits. Use when the user says "setup local dev", starts agent work in a fresh clone, or wants agent files kept out of git.
---

# Setup local dev

Goal: agent tooling works in this repo while `git status` stays clean — every agent-generated file is invisible to git via `.git/info/exclude` (local-only, unlike `.gitignore`, which is itself a tracked file). Exclusion only hides *untracked* paths; anything the repo already tracks upstream is unaffected.

## Steps

1. **AGENTS.md + symlink.** If neither `AGENTS.md` nor `CLAUDE.md` exists at the repo root, create `AGENTS.md` seeded with the guardrail block below, then `ln -s AGENTS.md CLAUDE.md`. If exactly one exists as a regular file, symlink the other to it and append the guardrail block if missing. If both exist as regular files, stop and ask which is canonical before touching either.

2. **Exclude agent artifacts.** Append to `.git/info/exclude`, skipping any line already present:

   ```
   # local agent files — keep out of commits
   AGENTS.md
   CLAUDE.md
   CONTEXT.md
   CONTEXT-MAP.md
   .claude/
   .scratch/
   specs/
   docs/agents/
   docs/adr/
   src/*/docs/adr/
   ```

3. **Verify.** Done when both checks pass:
   - `git status --porcelain` lists none of the paths above.
   - `git check-ignore -v AGENTS.md CLAUDE.md .scratch/x docs/agents/x` attributes each to `.git/info/exclude`.

## Guardrail block for AGENTS.md

```markdown
## Local-only agent files

Agent-generated files (this file, CLAUDE.md, CONTEXT.md, .scratch/, docs/agents/, docs/adr/, specs/, .claude/) are local-only: they live in `.git/info/exclude`, never in commits or PRs. When a skill creates an artifact at a new path, add that path to `.git/info/exclude` before continuing.
```
