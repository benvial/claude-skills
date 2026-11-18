---
name: physics-first
description: Physics-first design for scientific Python packages. Use when designing, reviewing or refactoring a public Python API, or writing user-facing docs (README, tutorial, theory, how-to, docstrings) for a physics or simulation package.
---

# Physics-first

The **reader** is a physicist or engineer who knows the physics and has never opened the repo. They think in structures, materials, sources, frequencies and observables; the module layout is invisible to them. Judge everything this skill produces from the reader's seat.

## The canonical script

Both branches start here. The **canonical script** is the 5–15 lines of Python the reader writes to solve the package's canonical problem (Mie scattering from a sphere, the modes of a waveguide, a convergence sweep): import, physical setup, solve, labelled result, plot. It uses public names and physical quantities with stated units only.

1. State the canonical problem in one sentence of physics, with zero code words.
2. Write the canonical script as the reader would wish it to read. For API work, write it before reading the implementation. For docs work, write it against the current public API.
3. List every **gap** between that script and what the package runs today: a missing public name, a raw array where a physics noun belongs, a required numerical knob, an unlabelled return, a unit left implicit.

Done when the script runs as written (docs) or every line maps to a planned public name (API), and the gap list covers every line of the script.

## Branches

- Designing, reviewing or refactoring the public API → read [API.md](API.md). Gaps are design input.
- Writing user docs → read [DOCS.md](DOCS.md). Report gaps to the human before writing around them; a gap papered over in prose is an API bug hidden in the docs.
- A new package → API.md first; its canonical script becomes the first tutorial.

## Vocabulary

**Physics nouns** are what the reader would draw on a whiteboard: `Structure`, `Material`, `Source`, `Mode`, `Spectrum`. They are the public surface. **Numerics nouns** (matrices, bases, truncation orders, meshes, assemblers) live underneath and surface only through solver options.

**Conventions** are units, time dependence (e.g. `exp(-iωt)`), field normalisation, sign of loss, coordinate frames. Each convention has one source of truth (a `conventions` module plus one docs page), is stated where the reader meets it, and is checked at the API boundary.
