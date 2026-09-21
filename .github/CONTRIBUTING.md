# Contributing to Cognitive Belief Dynamics (CBD)

CBD is an **event-driven cognitive state-transition and agent-level stochastic dynamical model informed by systems thinking**. It is not currently a formal System Dynamics model.

## Before contributing

Read [README.md](../README.md), [STATUS.md](../STATUS.md), and the retained release notes under [releases/](../releases/).

## Paradigm and evidence invariants

Unless an explicit paradigm change is scientifically justified and reviewed:

- do not relabel CBD as System Dynamics merely for suite uniformity;
- persistent state, memory, saturation, decay, nonlinear transformations and stochastic decisions remain distinct from closed endogenous SD feedback;
- synthetic recovery/identifiability results are not human-participant validation;
- normative Bayesian reference operators are not claims that human cognition literally implements Bayes' rule;
- Pencode is not treated as identified or estimated;
- participant recruitment is not authorized by the current retained baseline.

## Contribution types

Useful work includes computational-engine fixes, schemas/contracts, synthetic benchmark reproduction, evidence/provenance corrections, documentation, recovery/validation methodology, prospective calibration proposals, and carefully justified model-structure proposals.

## Verification

Use Python 3.12+ and follow the same verification path as the public CI baseline:

```bash
python -m pytest
cemodel validate --root .
```

For an exact GitHub-hosted Ubuntu / CPython 3.12 reproduction, use the pinned installation commands in [README.md](../README.md) and `requirements/ci-py312-linux.lock.txt`.

For changes affecting retained M1.E4 results, rerun the relevant scripts under [scripts/](../scripts/) and document exactly which retained artifact changes.

## Release changes

Do not change the public version as part of an unrelated contribution. A version increment is not a substitute for a new validation statement.

## Security

Do not publish sensitive vulnerability details in a public issue.
