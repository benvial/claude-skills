# Comparison Table Templates

Pick the variant that matches what the user is after, or blend columns as needed.

## Variant A — Implementation/solver survey
(best for: "what implementations exist for method X", numerical methods / scientific computing code surveys)

| Paper/Method | Year | Discretization / Approach | Complexity | Backend / Language | Public Code | Maintained? | License | Notes |
|---|---|---|---|---|---|---|---|---|

- **Public Code**: link if found, or "not found" (searched and confirmed absent) vs. "not checked"
- **Maintained?**: last commit/release date if checkable, or "unknown"
- **Notes**: anything unverifiable, disputed, or a caveat about how well the repo actually matches the paper's method

## Variant B — Pure literature review
(best for: "survey the literature on X", tracing how a research area developed)

| Paper | Year | Venue | Key Contribution | Builds On | Followed By | Verified? |
|---|---|---|---|---|---|---|

- **Verified?**: "read full text", "abstract only", or "title only, unverified" — be honest here, this column exists specifically to prevent silent overclaiming.

## Variant C — Algorithm/method comparison
(best for: "compare approaches A vs B vs C for problem Y")

| Method | Accuracy/Convergence | Computational Cost | Assumptions/Limitations | Reference Implementation | Source |
|---|---|---|---|---|---|

## General rules for filling these in
- Never leave a cell with a specific number or claim you didn't actually retrieve — write "unverified" or leave blank rather than estimate.
- Keep any quoted phrasing from a source under 15 words, one quote max per source (see main SKILL.md copyright note).
- If the table exceeds ~15 rows or ~6 columns, it's often clearer as a downloadable file (.md or .xlsx) rather than inline chat — ask the user or make the call based on how they intend to use it (e.g. sharing with a team → file; quick check → inline).
