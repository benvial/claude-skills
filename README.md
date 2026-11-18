# claude-skills

One Claude Code plugin marketplace holding all my skills: my own, plus pinned copies of external ones.

## Layout

- `plugins/skills/skills/<name>/` — every skill. Own skills are edited here directly.
- `plugins/skills/agents/` — subagents that come with external skills.
- `vendor.json` — external skills: upstream repo, pinned commit, and which paths to copy (or `plugin`: take every skill an upstream plugin.json lists).
- `LICENSES/<upstream>/` — each upstream's license and the exact commit copied.
- `scripts/sync.py` — copies the pinned external skills into the plugin.

## Install

Claude Code, on each machine:

```bash
claude plugin marketplace add benvial/claude-skills
claude plugin install skills@claude-skills
```

Then enable auto-update: `/plugin` → Marketplaces → claude-skills → Enable auto-update.

claude.ai: Customize → Plugins → Add → Add marketplace → Add from a repository → `benvial/claude-skills`, then install `skills`.

## Updating

- Own skill: edit it under `plugins/skills/skills/`, commit, push.
- External skills: a weekly workflow moves every pin to upstream HEAD and opens a PR. Review and merge it. To run it by hand: `python scripts/sync.py --bump`.
- Add or drop an external skill: edit `vendor.json`, run `python scripts/sync.py`, commit.

## External sources

| Upstream | Skills |
| --- | --- |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (Apache-2.0) | caveman, caveman-commit, caveman-review, caveman-compress |
| [mattpocock/skills](https://github.com/mattpocock/skills) (MIT) | every skill in the upstream plugin (27), read from its `plugin.json` |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0) | impeccable + 5 subagents |
| [wdm0006/python-skills](https://github.com/wdm0006/python-skills) (MIT) | designing-python-apis |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) (MIT) | avoid-ai-writing |
