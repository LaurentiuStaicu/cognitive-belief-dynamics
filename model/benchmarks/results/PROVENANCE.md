# Authoritative benchmark provenance index

This index centralizes retained execution provenance that was historically recorded across benchmark artifacts, pull-request audit records, checksum files, and later provenance sidecars.

It does **not** alter or reinterpret any benchmark result. Values below are transcribed only where the repository/GitHub history provides an explicit record. Missing historical metadata is left unfilled rather than reconstructed by inference.

## Phase F — candidate recovery

Persistent result:
`m1_e4_candidate_recovery_authoritative_2026-09-16.csv`

Historical audit source: PR #27, “Alpha 0.4.3a0 Phase F: publish authoritative M1.E4 recovery results”.

- benchmark-code commit: `8e291fd38c4f88ec7c0eb7c45a464dbd2914bd0e`
- authoritative workflow commit: `25cd4c9a93b1ada9a55bd6cc5a087f5e70136fb3`
- GitHub Actions run: `35064052116`
- artifact ID: `10433108423`
- authoritative JSON SHA-256 recorded by the historical audit: `c8aad7d5fcab17ddc114b0a0e1776e576e30056e21f0307fbb0a32722128cea7`
- Phase F merge commit: `71b643019f1ebeaa02d445fb09a373a8644cd2b8`

Current retained integrity file:
`m1_e4_candidate_recovery_authoritative_2026-09-16.sha256`

The original authoritative JSON itself is not retained as a current repository file; the persistent result surface is the retained CSV plus checksum and historical audit record.

## Phase G — targeted trial-count refinement

Persistent result:
`m1_e4_trial_count_refinement_authoritative_2026-09-16.csv`

Historical audit source: PR #28, “Alpha 0.4.3a0 Phase G: M1.E4 targeted trial-count refinement”.

- post-Phase-F main: `71b643019f1ebeaa02d445fb09a373a8644cd2b8`
- authoritative workflow commit: `5094b9fa90093ad695ddbef7a290843628f647eb`
- GitHub Actions run: `35065350252`
- artifact ID: `10433859156`
- authoritative JSON SHA-256 recorded by the historical audit: `80635b2e44eb0991fe8db446c163a0a2c3ff9dbab8396342098bdba6f72694b4`
- Phase G merge commit: `9c2225d608123f206c495ab1f945709195c92e22`

Current retained integrity file:
`m1_e4_trial_count_refinement_authoritative_2026-09-16.sha256`

As in Phase F, the historical authoritative JSON is not retained as a current repository file; the retained CSV/checksum plus the historical audit record preserve the available trace.

## Phase I — participant-aware screening

Persistent result:
`m1_e4_participant_screening_authoritative_2026-09-16.csv`

Historical audit source: PR #30, “Alpha 0.4.3a0 Phase I: publish participant-aware screening results”.

- Phase H main: `b725e14a8a226e67e1c2bc4f7c82b11dd15442a7`
- vectorized marginal-likelihood source commit: `f1123a4dce74c2b7c43917fd73d69080102d1799`
- loop/vectorized equivalence-test commit: `f5866784561b163f3a0c4b44ccff6bed146e4347`
- authoritative screening run: `35069251436`
- execution structure: 12 allocation × heterogeneity shards, each containing six generator × memory-regime cells
- Phase I merge commit: `c0dea407d55ca840dc00260834712d9225493768`

Current retained integrity file:
`m1_e4_participant_screening_authoritative_2026-09-16.sha256`

The historical PR records no artifact ID or single authoritative aggregate-JSON SHA in the audit text reviewed for v0.1.1. Those fields are intentionally **not invented** here.

## Phase K — participant-aware confirmation

Persistent result:
`m1_e4_participant_confirmation_authoritative_2026-09-16.json`

Historical audit source: PR #33, “Alpha 0.4.3a0 Phase K: publish authoritative participant confirmation result”.

- hardened main: `76aca60beb49a4e2ce5d96abaa564a67282ba811`
- workflow source: `faa8b4223960bb60dfa10654a7107d4158021f7f`
- GitHub Actions run: `35081097627`
- authoritative JSON SHA-256 recorded by the historical audit: `88c16c2143e7131a4ec8915dbb726ece7e859a797162df173b89743837335f89`
- Phase K merge commit: `f896b5dfe794c6f04fbc39ad4bf7be734a3c2269`

Current repository also retains:
- `m1_e4_participant_confirmation_authoritative_2026-09-16.provenance.json`
- `m1_e4_participant_confirmation_authoritative_2026-09-16.sha256`
- `m1_e4_participant_confirmation_authoritative_2026-09-16.shards.sha256`

The current provenance sidecar is the preferred machine-readable source.

## Phase M — protocol robustness

Persistent result:
`m1_e4_protocol_robustness_authoritative_2026-09-17.json`

The current repository retains a complete machine-readable provenance layer:

- contract/tooling commit: `2be27f09d054448abb9005ccf29c0017990a4ccc`
- executed commit: `af338ed1fe94cc8d59578e50471eb1ccc5886df2`
- GitHub Actions run: `35229760477`
- authoritative source aggregate SHA-256: `479767bc8f75a689060529c803d7796b2588340f7690915dd9fd481b2e6b9f80`
- retained verdict: `PROTOCOL_ROBUSTNESS_FAIL`

Current repository also retains:
- `m1_e4_protocol_robustness_authoritative_2026-09-17.provenance.json`
- `m1_e4_protocol_robustness_authoritative_2026-09-17.sha256`
- `m1_e4_protocol_robustness_authoritative_2026-09-17.shards.sha256`

The current provenance sidecar and authoritative result JSON are the preferred machine-readable sources.

## Provenance maturity

The benchmark history contains two provenance generations:

1. **historical audit-record provenance** — Phase F/G/I metadata is distributed between retained result/checksum files and GitHub PR/run history;
2. **repository-side machine-readable provenance** — Phase K/M retain dedicated provenance sidecars, with Phase M additionally covered by explicit result/provenance regression tests.

v0.1.1 centralizes the historical trace without rewriting old results. A future provenance-normalization task may introduce machine-readable sidecars for older phases only where every field can be copied from an explicit historical record. Unknown fields must remain unknown.

## Scientific boundary

Provenance records establish where retained synthetic results came from. They do not strengthen the scientific interpretation of those results. In particular, they do not convert synthetic model recovery into human validation, identify Pencode, select a human recognition architecture, or authorize participant recruitment.
