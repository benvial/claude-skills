# Physics-first: public API

Branch of [SKILL.md](SKILL.md). Start from its canonical script and gap list.

## Steps

1. **Two call styles.** Rewrite the canonical script in two genuinely different styles (e.g. object-with-methods vs. function-taking-objects, one `solve()` vs. separate setup and run). Give each a two-line trade-off from the reader's seat. The human picks.
2. **Public surface.** Design every public name the chosen script needs, applying every rule below. Write signatures, type hints and one-line docstrings before any body.
3. **Layering.** Where the solver allows, implement a pure functional core first (`solve(params) -> result`, arrays and pytrees), then the physics-noun layer as a thin wrapper over it. A wrapper over a compiled engine keeps the same split at its own boundary: physics nouns in, labelled results out, engine objects never public.
4. **Audit.** Run the canonical script. Then walk the rules below one by one and report each as pass or fail with the offending name or line.

Done when the canonical script runs unchanged and every rule is reported pass, or fail with a reason the human accepted.

## Rules

### Signatures
- Essentials positional, everything else keyword-only after `*`: `solve(structure, *, wavelength, options=None)`.
- Choices are `Literal[...]` or an `Enum`, validated at entry: `polarization: Literal["TE", "TM"]`.
- Interacting booleans become one `Literal` or a split into two functions.
- Numerical knobs (truncation order, mesh size, tolerances, quadrature) live in one frozen `@dataclass` (`SolverOptions`) with defaults that converge for the canonical problem. Where one knob dominates accuracy, a `precision` shortcut that builds the options may help; do not add one that hides which knob moved.

### Data in, data out
- Accept scalars, sequences and arrays for swept quantities, and broadcast. A wavelength sweep is an array argument.
- Return labelled data: an `xarray.DataArray`/`Dataset` with named, unit-carrying coordinates, or a frozen result dataclass with named fields, a `.plot()` and a convergence/validity flag.
- Units follow the package's conventions source of truth. Either accept `pint` quantities, or document one unit system and name parameters with it where ambiguity bites (`wavelength_um`).

### Progressive disclosure
- The common case is one call with physics arguments only. Power users reach more through `options` or a second, named function, never through extra required arguments on the first.
- One name per concept, no abbreviations, matching the glossary.

### Objects
- Physics nouns are classes; verbs are methods or top-level functions. Curate `__all__` so `dir(package)` reads like a physics glossary.
- Objects are immutable (`@dataclass(frozen=True)`) with `.replace(**changes)` for sweeps.
- Every public object has a `__repr__` showing its physical parameters, and a `_repr_html_` for Jupyter where a table or figure helps.
- One obvious import path per name: `from oslumen import Sphere, solve`.

### Errors and evolution
- Custom exceptions subclass `ValueError`/`RuntimeError` and speak physics, with a remedy: `"order=5 is too low for size parameter x=12; use order>=18 or precision='accurate'"`.
- Validate physical sanity at the boundary (negative radius, wavelength in wrong units by orders of magnitude, passive material with gain).
- Breaking changes go through `warnings.warn(..., DeprecationWarning, stacklevel=2)` naming the replacement call. Before 1.0, a break may land in one minor release if the release notes name the replacement.

### JAX packages
- The functional core is pure and jit-safe: static configuration in hashable dataclasses, arrays in pytrees.
- Physics-noun classes are registered pytrees (or `equinox.Module`), so `jax.grad` and `jax.vmap` work through the friendly layer as well as the core.
- The canonical script gets a differentiable twin: the same problem with `jax.grad` of one observable with respect to one physical parameter.
