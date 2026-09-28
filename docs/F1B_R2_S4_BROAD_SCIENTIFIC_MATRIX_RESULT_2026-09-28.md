# F1b R2 S4 broad scientific matrix result — 2026-09-28

Issue: #259

Status: **MATRIX COMPLETE / 15,000 SCIENTIFIC RUN IDENTITIES / METHODS NOT YET BOUND**

The method-independent S4 matrix gate was merged in PR #272 and executed in temporary PR #273, which was closed unmerged.

Execution evidence:
- workflow run: `36463026247`;
- artifact ID: `10988228984`;
- artifact ZIP SHA-256: `25f9a07a928678f90861d1d01f21fbc4bd75949f2238837e71f3fa9eb72c3471`;
- manifest JSON SHA-256: `f0691a0dc153f2ee1463f5115feeff448b49e7d2fb7accd6568a0fb8c43a5f01`;
- manifest JSON size: 16,787,637 bytes.

Verified matrix:
- 75 restriction cells;
- 150 cell × missingness strata;
- 15,000 unique scientific-run IDs;
- 14,400 departure runs;
- 600 null runs;
- 7,500 runs at missingness 0.00;
- 7,500 runs at missingness 0.15;
- exact evaluation-replicate indices 0..99;
- exactly 100 replicates per stratum.

Canonical SHA-256 of the sorted 15,000 scientific-run IDs:

`851e7336387901ca15d2486ed8efc19cd090ffac869b760352106a3f455f2b43`

The precision target remains worst-case component MCSE <= 0.05. This is a Monte Carlo precision requirement and is not a power result.

No scientific dataset was simulated in this manifest stage and no inference method, fitter, bootstrap, or sequential continuation was executed.

The next gate must bind the method list exactly to the retained M2 `eligible_methods` result. M2 remains independent of this manifest and may not be reinterpreted to fit the broad matrix.

Boundary:
- S4 scientific matrix: complete;
- M2 method binding: pending;
- power: not validated;
- core-grid / human-N freeze: not authorized.
