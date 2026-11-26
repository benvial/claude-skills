---
name: wayfinder-autopilot
description: "Run a whole wayfinder effort in one session, from loose idea to implemented code: chart the map, resolve its tickets, write the spec and implementation tickets, then implement them, using parallel subagents and taking the recommended answer at every question."
disable-model-invocation: true
---

Wayfinder on **autopilot**. You are the main agent driving a whole effort in one session: a loose idea becomes a map of decisions, then a locked spec, then implementation tickets, then working code on an integration branch. The user has given a **standing answer**: every question any skill would put to them is answered with your own recommended answer, recorded, and the run continues.

## Base procedures

These skills are user-invoked, so read their `SKILL.md` files directly. They ship in the same plugin as this skill, at `../<skill>/SKILL.md` relative to this file:

- `wayfinder` before step 1. It defines the map, tickets, ticket types, fog of war, out of scope and refer-by-name, and it defers storage to the repo's tracker doc ("Wayfinding operations").
- `to-tickets` before step 4.
- `implement-spec` before step 5.

All of them hold, except for the overrides below.

## Overrides

- **Standing answer.** Every question resolves with your recommended answer, and the run never pauses for the user. This covers grilling questions, prototype reactions, wayfinder's "no fog: ask the user", to-spec seam checks, the to-tickets quiz, and any choice during implementation or code review. Ground each recommendation in evidence (code, tests, research notes, ADRs, `GLOSSARY.md`). Each recorded answer opens with `(standing answer: recommended answers accepted)`. A recommendation that rests on a guess about the user's intent, rather than on evidence, goes under an `### Assumptions` heading in its ticket; the final report lists them so the user can veto.
- **Whole effort, one session.** Wayfinder's one-ticket-per-session limit is lifted. Loop each frontier until it is empty.
- **Sole writer.** You alone write `map.md`, `GLOSSARY.md`, `docs/adr/`, and every `Status:` / `Blocked by:` line. A subagent writes only its own ticket's `## Answer` and the files that answer links to (and, in step 5, code in its own worktree). It returns glossary terms and ADR drafts in its final message for you to write.
- **Research notes** live where the tracker doc says. For the local-markdown tracker: `.scratch/<effort>/research/<name>.md`, linked from the ticket, never on a branch.
- **Destination.** Default: the spec implemented on an integration branch with the suite green. When the user's idea names a different destination, use theirs and trim the steps to it.
- **Decide, then build.** Map tickets (steps 1–2) produce decisions. A `task` ticket may change the local environment (venv, scratch files) to unblock a decision. Code changes start in step 5.

## Steps

### 1. Chart

Survey the repo; fan out parallel `Explore` subagents when the space is wide. Then, per wayfinder's "Chart the map", name the destination, write the map, create every ticket you can state precisely, wire blocking in a second pass, and sketch the rest into **Not yet specified**. Notes must carry: the standing answer, the sources of intent you found, and which skills each ticket type calls.

Add one closing `task` ticket, **Assemble the spec**, blocked by every decision ticket.

If charting surfaces no fog, skip the map and go straight to step 3 with what you know.

Done when every question you can state precisely is a ticket, and everything else sits in **Not yet specified** or **Out of scope**.

### 2. Work the map frontier in waves

1. Query the frontier. Claim every ticket on it.
2. Dispatch one background subagent per claimed ticket, all in one message. The prompt is context pointers only: the ticket path, `map.md`, `GLOSSARY.md`, `docs/adr/`, plus these rules:
   - resolve as the ticket's `Type:` line says: `grilling` calls the Skill tool for `grilling` and `domain-modeling` and plays both sides (ask, recommend, accept); `research` calls `research`; `prototype` calls `prototype` and judges the artifact against the destination; `task` does the work;
   - apply the standing answer and the Assumptions rule;
   - write `## Answer` into the ticket and leave its `Status:` line for you;
   - return a one-line gist, newly surfaced questions, out-of-scope findings, and any glossary terms or ADR drafts.
3. **Reconcile** each result as it lands, without waiting for the rest of the wave:
   - check the answer against **Decisions so far**; on a contradiction, amend the earlier ticket and note the amendment in both;
   - set `Status: resolved`, append the gist pointer to **Decisions so far**, write glossary and ADR changes;
   - graduate fog into new tickets (add each to the Assemble ticket's `Blocked by:`), rule out-of-scope work out;
   - claim and dispatch whatever just entered the frontier.

Keep your own context for coherence: hold the map and the gists, and open a full ticket only to reconcile a conflict.

Done when the only open ticket is **Assemble the spec** and **Not yet specified** reads "Nothing."

### 3. Assemble the spec

Resolve **Assemble the spec** yourself. Write `.scratch/<effort>/spec.md` from the resolved tickets:

1. **Target behaviour**, one section per decision area, each linking the ticket that holds the decision. When spec and ticket disagree, the ticket wins.
2. **Ordered fixes**: reviewable slices, each with file:line anchors and acceptance checks you could run.
3. **Deleted**: every public name, file, or behaviour removed.
4. **Definition of done.**

Small decisions taken while assembling go in their own subsection. A gap the assembly exposes is fixed by amending the owning ticket, then the spec.

Done when every resolved decision ticket is cited, and every slice has a runnable acceptance check.

### 4. Slice into implementation tickets

Follow to-tickets, answering its quiz with the standing answer. Write the tickets to `.scratch/<effort>/tickets/NN-<slug>.md`, apart from the map's decision tickets, and link the directory from the spec.

Done when every spec slice maps to at least one ticket, every ticket carries the slice's acceptance checks, and every `Blocked by:` names a real ticket file.

### 5. Implement

Follow implement-spec on the spec and the tickets from step 4, with the standing answer for every choice it or `code-review` raises.

Dispatch by **agent type**, so the expensive model only does the judgement work:

- implementation tickets, test and lint fixes, docs and tutorials: the `implementer` agent;
- lookups (finding files and usages, reading logs and job results, watching long jobs): the `scout` agent, or `Explore` for a wide search;
- decision tickets, the spec, `code-review` and hard numerical debugging: the default subagent, on your own model.

Redo an `implementer` ticket on the default subagent when it reports a loosened check, skips one, or fails the same ticket twice. Where these agents are not installed, fall back to the default subagent with `model: "sonnet"` for implementation and `"haiku"` for lookups. Record in the report which tickets ran on which agent.

Implementer worktrees are fresh checkouts, so local-only agent files (`.scratch/`, `GLOSSARY.md`, `docs/adr/`, anything in `.git/info/exclude`) are missing from them. Give every subagent **absolute paths into the main checkout** for the spec, its ticket, the glossary and the ADRs.

When an implementer finds the spec wrong or incomplete, it reports back instead of improvising. You amend the owning decision ticket, then the spec, then the affected implementation tickets, and redispatch.

Done when every implementation ticket is resolved, each ticket's acceptance checks pass on the integration branch, the full test suite and lint are green there, and every `code-review` finding is fixed or recorded as skipped with a reason.

### 6. Verify and report

Check that:

- every decision ticket is resolved or ruled out of scope;
- **Decisions so far** has one line per resolved ticket;
- every relative link in the map, tickets and spec resolves to a file;
- the spec's definition of done holds on the integration branch: rerun its checks and keep the output.

Report to the user, referring to tickets by name:

- the integration branch, with test and lint results;
- the decisions;
- every Assumption, with its ticket;
- anything skipped or failing, quoted exactly.

Merging into the main branch and pushing are left to the user.
