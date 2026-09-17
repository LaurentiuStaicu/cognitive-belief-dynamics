# Post-v1 calibration extension contract

Status: **architecture seam reserved; calibration module intentionally absent before v1.**

Cognitive Epistemic Model now has one simplified application surface. There is no separate Advanced application or Advanced mode. Scientific and data structures needed by later calibration remain in the repository, but no calibration control is mounted in the pre-v1 UI.

## Product boundary

Before v1:

- one application only;
- no Advanced-mode toggle;
- no calibration upload button;
- no population calibration claim;
- no activation of M1.E4 or `Pencode`;
- existing model registries, evidence provenance and workspace versioning remain intact.

After v1, calibration may be introduced as a module inside the same application. The planned entry control is a file-upload button within the relevant auxiliary/settings surface, not a switch to a separate application variant.

## Planned input classes

The typed extension seam reserves these appropriate source-file classes:

- `.txt` and `.md` for calibration notes, dictionaries, protocol descriptions or human-readable data specifications;
- `.csv` and `.tsv` for rectangular datasets;
- `.json` for structured records, manifests and machine-readable metadata;
- `.xlsx` and `.ods` for tabular workbooks when source data are delivered in spreadsheet form.

Supporting a filename extension in the contract does not imply that a parser is already implemented. Parser selection, schema detection, validation and security limits belong to the future post-v1 calibration module.

## Required future pipeline

The future module must preserve this order:

1. user selects one or more source files;
2. files are inspected and parsed without mutating the active model;
3. schema and required fields are validated;
4. validation errors and warnings are shown before calibration;
5. calibration runs only against an explicit model specification and evidence snapshot;
6. a result manifest records source files, parameter identifiers, diagnostics and provenance;
7. calibrated outputs remain distinguishable from demonstrative/default parameters.

## Architectural seam

`web/src/calibration-extension-contract.ts` defines the dormant typed port. It is intentionally not imported by the runtime entry point and exposes no mounted route or upload control before v1.

This contract preserves extensibility without creating a second application, an inactive Advanced shell, or premature calibration behavior.
