# Physics-first: user docs

Branch of [SKILL.md](SKILL.md). Start from its canonical script and gap list. Use the docs tooling already configured in the repo (`mkdocs.yml`, `conf.py`, notebook execution settings).

## Page types

Each user page is exactly one type. Code on every page is the means to a physical result.

- **Tutorial**: the canonical script, narrated through the physics. Each block answers a physical question, then shows the code that answers it, then the figure.
- **How-to**: one task the reader already knows they want (sweep a parameter, add a dispersive material, check convergence). Title is the task.
- **Theory**: formulation and governing equations, assumptions and approximations, conventions, validity regime, references. Code appears only to connect a symbol to its public name.
- **Validation**: package result vs. an analytic or published reference (Mie series, a known resonance, a benchmark), with an error plot and a convergence plot.
- **Reference**: generated from docstrings by the configured tool. Prose pages link to it; prose pages never restate it.

Tutorials and how-tos drift into each other. A tutorial has drifted when it assumes the reader already knows what they want, offers alternatives, or takes on real-world complexity. A how-to has drifted when it stops to teach basics. Move the stray material to a page of its own type and link it.

## Page skeleton (tutorial, how-to, theory)

1. **Question**: the physical problem in one or two sentences.
2. **Assumptions**: what is approximated and the regime where it holds.
3. **Conventions**: units and conventions in play, linked to the conventions page.
4. **Result**: the shortest code to the answer, then a figure with labelled axes and units.
5. **Trust**: how the reader checks the result (convergence knob, comparison, sanity limit).
6. **Limits**: where the method or package breaks, and what to use instead.
7. **Next**: links to the related theory, how-to and reference pages.

## Docstrings

NumPy style. Every parameter states its physical meaning and unit. Returns name their coordinates and units. An `Examples` section runs as a doctest. A `See Also` links the theory page.

## README

First two lines: what physics the package solves and for whom. Then the canonical script, its figure, install, and links to tutorial, theory and validation.

## Reviewing existing pages

Work on one piece at a time: pick a page, section or paragraph, name the reader's need and the page type that serves it, make the one improvement that helps most now, then repeat. Do not restructure a whole docs tree in one pass.

## Completion

Done when:
- every page is one type and every tutorial/how-to/theory page has all seven skeleton sections;
- every code block executes in the docs build;
- every figure has axis labels with units;
- every gap from the canonical script is either fixed or reported to the human.
