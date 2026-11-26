# Physics-first: user docs

Branch of [SKILL.md](SKILL.md). Use the docs tooling already configured in the repo (`mkdocs.yml`, `conf.py`, notebook execution settings).

## Page types

Each user page is exactly one type. Code on every page is the means to a physical result.

- **Tutorial**: the canonical script, narrated through the physics. Each block answers a physical question, then shows the code that answers it, then the figure.
- **How-to**: one task the reader already knows they want (sweep a parameter, add a dispersive material, check convergence).
- **Theory**: formulation and governing equations, assumptions and approximations, conventions, validity regime, references. Code appears only to connect a symbol to its public name.
- **Validation**: package result vs. an analytic or published reference (Mie series, a known resonance, a benchmark), with an error plot and a convergence plot.
- **Reference**: generated from docstrings by the configured tool. Prose pages link to it; prose pages never restate it.

Tutorials and how-tos drift into each other. A tutorial has drifted when it assumes the reader already knows what they want, offers alternatives, or takes on real-world complexity. A how-to has drifted when it stops to teach basics. Move the stray material to a page of its own type and link it.

### Supporting pages

These are not narrative pages. Keep them in their shape:

- **Capabilities**: a table (problem × feature × differentiable × 2D/3D), one short note per cell at most. Prose bullets are a smell. No version number in the text; it goes stale.
- **Glossary**: a definition of one or two sentences, linked to the page that uses the term. No derivations, no option lists.
- **Release notes**: one line per change, naming the public call, plus a link to its page. No formulas, units or signatures.
- **Conventions**: one entry per convention: the rule, the symbol, the sign, one line of why. Long derivations go to a theory page.
- **Performance data** (scaling, benchmarks): one summary page with the headline figure and how to reproduce. Raw runs, per-commit figures and machine logs stay off the user site.

## Page skeletons

The **answer first**: the reader gets the result from the title, the first sentence and the first code block. Caveats come after, in an admonition or a short section.

The bold names below are roles, not headings: never print one as heading text or as a "Role: topic" prefix. A heading says what its section holds, in the reader's words.

**Checks** are how the reader verifies a result (convergence knob, comparison, sanity limit). Name each check by what it compares: "Power balance and reciprocity", "Against the Mie series", "A finer mesh". Put a check right after the result it checks; checks may be spread through the page. One list of checks at the end is headed "Check your results".

- **How-to**: **Question** (one sentence), then **Result** (shortest code, then the figure), then **Limits**. Add **Assumptions**, **Conventions** or **Checks** only when they change what the reader does; then keep each to three bullets or fewer and put them after Result.
- **Tutorial**: **Question**, **Assumptions**, **Conventions**, **Result** (narrated blocks), **Checks**, **Limits**, **Next**, in this order.
- **Theory**: **Question**, **Assumptions**, **Conventions**, formulation, validity regime, **Limits**, references, in this order.

A bullet holds one claim. A bullet longer than ~40 words or with nested parentheticals is two bullets, or detail for the docstring.

## Budgets

| Item | Budget |
|---|---|
| Sidebar / page title | ≤ ~35 characters, noun phrase (`Optomechanical coupling`); the task sentence goes in the first line |
| How-to | ≤ ~800 words of prose |
| Tutorial | ≤ ~2500 words of prose |
| Glossary entry | ≤ 2 sentences |
| Release-note entry | 1 line + link |
| Docs section (sidebar group) | ≤ ~10 pages |

Over budget? Cut, then split by page type. Do not raise the budget.

## Site structure

Run an IA pass when a sidebar section passes its budget, a new domain of physics arrives, or the human asks:

1. List every page with its type and the reader's need.
2. Group by the reader's physics domain (e.g. RF and ports, photonics, nonlinear optics, thermal, mechanics), then by infrastructure (meshes, solvers, scale-out, I/O). Never one "misc" or catch-all "Solving" section.
3. Tutorials get the same domain groups, so a reader finds their field in one look.
4. Conceptual pages (conventions, modes and ports) sit with theory, not under API reference.
5. The toctree is the only list of pages; no hand-maintained index that duplicates it.

Propose the new tree to the human before moving files. Keep redirects for moved pages.

## Docstrings

NumPy style. Every parameter states its physical meaning and unit. Returns name their coordinates and units. An `Examples` section runs as a doctest. A `See Also` links the theory page.

## README

First two lines: what physics the package solves and for whom. That pitch matches what the docs cover; when the docs outgrow it, update it. Then the canonical script, its figure, install, and links to tutorial, theory and validation.

## Reviewing existing pages

Work on one piece at a time: pick a page, section or paragraph, name the reader's need and the page type that serves it, make the one improvement that helps most now, then repeat. Structure problems across pages go to the IA pass above, not to page-by-page edits.

**Skim test** for each page: read only the title, the first sentence and the first code block. If they do not give the answer, fix that before anything else.

## Completion

Done when:
- every page is one type and covers its type's skeleton parts, under headings that name their content;
- every page passes the skim test and is within budget;
- every code block executes in the docs build;
- every figure has axis labels with units;
- every gap from the canonical script, when one was written, is either fixed or reported to the human.
