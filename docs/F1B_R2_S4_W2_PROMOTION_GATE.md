# F1b R2 S4 W2 predecessor-driven promotion gate

Issue: #259

Status: **W2 PROMOTION / IMPLEMENTATION GATE**

W1 is retained on `main` by PR #312 and merge
`0885d465a56a435a173a0c6d0cde1d6e09c74255`.

The retained W1 predecessor is pinned by:
- path: `model/results/f1b_r2_s4_w1_combined_2026-09-30.json`;
- Git blob: `7302806c2630b8d24a84f20885a543274badcd33`;
- required status: `NON_AUTHORITATIVE_S4_W1_COMBINED_COMPLETE_RETAINED`.

## Frozen W2 identity

- evaluation replicates: 50..74;
- scientific runs: 3,750;
- method rows: 15,000;
- imported evidence: 0;
- shards: 250 / 250 non-empty;
- shard load range: 6..27;
- scientific-run IDs SHA-256:
  `a24dea39afdb03b91784248755d9ddad94466bbab8391044308eeeb8c9eff617`;
- method-row IDs SHA-256:
  `a338bd644ee62a474cf417aa0396a0ff2df4a310618e63ffb644c8f5f3cc8ba2`;
- shard-plan SHA-256:
  `399b4feecc51731f4691ca7168eb61625834cc1dc74e2fb66d3f6fe23ffe2475`.

The W2 identity was independently regenerated from retained S4 scientific-matrix
artifact `10988228984`, whose manifest SHA-256 remains
`f0691a0dc153f2ee1463f5115feeff448b49e7d2fb7accd6568a0fb8c43a5f01`.
The regenerated selection reproduced all three frozen W2 digests and the exact
6..27 non-empty shard range.

## Promotion rule

W2 reuses the already-qualified all-new-wave scientific path unchanged:
- the same four methods in the same order;
- the same shared broad executor blob;
- the same RNG namespaces carried by that executor;
- the same 199-draw prefix;
- the same sequential controller and n=10,000 cap;
- the same Haswell numerical lineage;
- zero imported evidence.

Unlike W1, W2 has no shard-11 or other scientific/method-selection preflight.
Its authorization is predecessor-driven: exact retained W1 is the gate.

The generic validator and plan builder remain W1-compatible while accepting W2
only when the retained predecessor path/blob/status and every frozen W2
identity are exact. W3 remains rejected.

## Boundary

This patch authorizes only the W2 execution configuration after merge. It does
not execute W2.

Observed W1 outcomes did not alter the promotion rule. Scientific
interpretation remains disabled, no method or hierarchical scale is selected,
power is not validated, human N is not frozen, participant recruitment and
runtime F1b activation remain forbidden, and the v0.2.0 blocker remains open.

A later temporary execution-only PR must run the exact 250-shard W2 workflow.
That PR must close unmerged after exact combine/evidence capture. W3 can become
eligible only after a separate retained W2 combined result is merged.
