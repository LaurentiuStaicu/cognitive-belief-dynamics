# F1b R2 Distance-Definition Review — Closure/Attainment Result

Status: **COMPLETED COMPARISON / NON-AUTHORITATIVE / METRIC DECISION PENDING**

Issue: #171  
Scientific source: `97a4ac6119709de8089032a21b97877a522dd04d`  
Temporary execution PR: #175  
Actions run: `36325580317`

## Scope

This result completes the deterministic existence/attainment diagnostic for the three prospectively declared nearest-CBD distance candidates:

1. stabilized utility/logit RMS;
2. probability RMS;
3. directed mean Bernoulli KL from the general generator to the CBD family.

The 12 fixed complement-relation target surfaces and the uniform 18-cell design measure are unchanged.

No historical #158 departure is regenerated or reinterpreted.

## Execution integrity

The run completed successfully with:

- 12/12 retained target surfaces;
- 3/3 candidate objectives;
- finite-logit and direct closed-surface projections;
- nested 8× / 16× / 32× bias/reward diagnostic domains;
- zero failed closure optimizer starts;
- zero `SCIENTIFIC_DOMAIN_UNRESOLVED` cases.

Exact execution provenance is retained in the compact JSON result.

The exact execution artifact is identified by:

- artifact ID: `10933539813`;
- artifact ZIP SHA-256: `7c947134279e816357bcc8b6d7966c44fc29e49bb536d974827628068e769f48`;
- exact JSON SHA-256: `55597e0f240b439531b872e99dfec9bafee73323e3c39d18943529069907537e`;
- exact JSON size: 2,757,195 bytes.

## Attainment result

Every candidate shows the same count:

| Candidate | Finite interior | Closure limit | Scientific domain unresolved |
|---|---:|---:|---:|
| Stabilized utility RMS | 7/12 | 5/12 | 0/12 |
| Probability RMS | 7/12 | 5/12 | 0/12 |
| Bernoulli KL general→CBD | 7/12 | 5/12 | 0/12 |

The same five retained target surfaces hit a `W0/W1` closure boundary under all three candidates.

Therefore non-attainment is not evidence against one candidate relative to the others. It is a property of the retained target geometry relative to the finite-logit CBD family.

## Which targets reach the closure

For all three candidates, closure-limit behavior occurs for:

- CBD_ANCHOR_1 / complement-minus / historical 0.25;
- CBD_ANCHOR_1 / complement-minus / historical 0.50;
- CBD_ANCHOR_2 / complement-minus / historical 0.10;
- CBD_ANCHOR_2 / complement-minus / historical 0.25;
- CBD_ANCHOR_2 / complement-minus / historical 0.50.

The medium-distance minus cases reach `W1=1`; the large-distance minus cases reach `W0=1`.

No sharing-bias or reward coordinate remains active at the widest scientific diagnostic domain.

## Finite-logit versus closure surfaces

The direct closure projection and widest finite-logit projection are extremely close as response surfaces.

Maximum probability-RMS difference across all retained targets:

- stabilized utility RMS: approximately `7.0e-6`;
- probability RMS: approximately `6.1e-5`;
- Bernoulli KL: approximately `1.31e-5`.

Maximum absolute objective difference is approximately:

- stabilized utility RMS: `1.23e-8`;
- probability RMS: `4.65e-9`;
- Bernoulli KL: `1.91e-9`.

This supports interpreting the finite-logit sequences as approaching the identified boundary surfaces, rather than as unresolved optimizer-domain failures.

## Consequence for distance definition

The comparison is now numerically and geometrically characterized sufficiently to support a separate scientific decision.

The closure result does not itself choose among D1/D2/D3 because all three face the same finite-family attainment issue on the same targets.

Any subsequent metric choice must be based on the prospective scientific criteria in #171:

- relationship to the Bernoulli observation model;
- parameterization invariance;
- independence from arbitrary operational bounds;
- existence/stability when the response-family closure is handled explicitly;
- explicit design weighting;
- behavior near saturation;
- suitability for controlled distance from a restricted response family.

It must not use historical #158 rejection rates, historical monotonicity, sign symmetry, optimizer convenience, or preservation of old coefficient values.

## Boundary

`DISTANCE CANDIDATE COMPARISON = COMPLETED`

`CLOSURE / ATTAINMENT DIAGNOSTIC = COMPLETED`

`METRIC SELECTION = PENDING SEPARATE SCIENTIFIC DECISION`

`PAIRED BOOTSTRAP = NOT AUTHORIZED`

`AUTHORITATIVE BOOTSTRAP DRAWS = NOT FROZEN`

`AUTHORITATIVE EVALUATION REPLICATES = NOT FROZEN`

`AUTHORITATIVE CORE GRID = NOT FROZEN`

`HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
