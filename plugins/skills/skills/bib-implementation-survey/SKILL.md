---
name: bib-implementation-survey
description: Use this skill whenever the user wants a literature/implementation survey of a numerical method, algorithm, or scientific computing topic — e.g. "find papers on X", "what's the state of the art for Y", "survey implementations of Z", "which papers have public code for this method", or any request to map out the papers + existing GitHub/Zenodo implementations + comparison of approaches for a computational method (FEM, FDTD, RCWA, BEM, optimization algorithms, ML architectures, etc). Trigger even if the user only asks for "papers" or "a github repo" for a method, since finding one usually means checking for the other. Also trigger for requests like "turn this into a literature review" or "build me a comparison table of approaches to X". Do NOT trigger for single, narrow factual lookups ("what's the time complexity of FFT") that don't need a multi-source survey.
---

# Bibliographic + Implementation Survey

A workflow for surveying a numerical method or algorithm topic: find the relevant papers, find working code for them, and produce a structured comparison — while aggressively guarding against fabricated citations, since this is the single biggest failure mode in this task.

## Core principle: never cite from parametric memory

Every paper, author, arXiv ID, GitHub repo, or claim about a paper's method that ends up in the final output MUST come from an actual tool call in *this* conversation (web_search, web_fetch, or reading an uploaded doc) — never from training-data recall alone. If you find yourself typing a citation without having just seen it in a tool result, stop and go verify it with a search first. This applies even when the topic is one you know well.

## Workflow

### Step 0 — Scope the query with the user (only if genuinely ambiguous)
If the method/topic is specific and the intent is clear (e.g. "RCWA implementations for anisotropic gratings"), proceed directly. Only ask a clarifying question if the topic is broad enough that the search strategy would differ wildly (e.g. "numerical methods" with no further context).

### Step 1 — Seed search (discovery layer)
Run several searches, not just one:
- `web_search`: `"<method name>" review paper` or `"<method name>" arxiv`
- `web_search`: `"<method name>" github` — for implementations directly
- `web_search`: `"<method name>" site:arxiv.org` for preprints
- If the topic has an obvious canonical review/survey paper, find and fetch it first — its reference list is a shortcut to the rest of the seed set.

Scale the number of searches to the breadth of the topic: a narrow method (~3-5 searches) vs. a broad survey (~10-15 searches, covering sub-variants).

### Step 2 — Expand via citation graph
For the 2-4 most central papers found in Step 1, search for:
- `"<paper title or key phrase>" cited by` or check Semantic Scholar / Google Scholar links surfaced in search results
- Follow-up searches for variants and follow-on work: `"<method>" improved` / `"<method>" faster` / `"<method>" GPU` etc., depending on what axis of comparison matters to the user (accuracy, speed, backend, license).

### Step 3 — Find implementations
For each paper that seems central to the comparison, actively search for code, don't assume it doesn't exist:
- `web_search`: `<method/author name> github implementation`
- `web_search`: `<method name> "papers with code"`
- Check for Zenodo/OSF archived code (`<method name> zenodo`) if GitHub search comes up empty — some solver code is archived there with a DOI instead.
- When a repo is found, `web_fetch` it briefly to check: is it actually the referenced method, is it maintained (recent commits/last release), what language/backend, what license.

### Step 4 — Verify, don't just collect
Before writing anything into the final table:
- Every claim about what a paper does (discretization scheme, complexity class, whether it has a stability proof, etc.) should be traceable to a passage you actually retrieved in this conversation, not inferred from the title alone. Use `web_fetch` on the abstract/full text when the claim matters.
- Flag anything you couldn't verify as "unverified" or "abstract-only" rather than guessing.
- Cross-check: if two sources disagree on something material (e.g. one repo claims to implement a method it doesn't fully match), note the discrepancy rather than silently picking one.

### Step 5 — Produce the structured output
Default to the comparison table format in `references/comparison_table_template.md`. Use it as a starting point, but adapt columns to what the user actually cares about (e.g. for a solver landscape survey: backend/language, complexity, license, is code public, is it maintained; for a pure literature review: year, venue, key contribution, follow-on work).

Output as a markdown table inline in chat for a normal-sized survey (this is analysis output, not a standalone document — see the file-creation guidance below). Only create an actual file (.md, or a spreadsheet if the comparison is large/many-columned) if the user asks to save/export it, or if the table has enough rows/columns that inline markdown would be unwieldy (rule of thumb: >15 rows or >6 columns — consider an .xlsx or .md file at that point).

### Step 6 — Report gaps honestly
End with an explicit note on what's still uncertain: papers you found but couldn't get full-text access to, methods with no discoverable public code, or claims that reviewers/practitioners dispute. This is more useful than a falsely-complete-looking table.

## Copyright note
Standard copyright limits apply: no verbatim reproduction of abstracts/paragraphs beyond short (<15 word) quotes, one quote max per source, paraphrase everything else. This is especially relevant here since academic papers are exactly the kind of source this constrains.

## Reference files
- `references/comparison_table_template.md` — default column layout for the implementation comparison table, with variants for pure-literature-review vs. solver/implementation-survey use cases.
