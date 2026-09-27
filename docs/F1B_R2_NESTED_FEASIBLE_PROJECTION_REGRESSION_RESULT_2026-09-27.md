# F1b R2 Nested-Feasible Projection Regression Result

Status: **PASS / NUMERICAL-INTEGRITY REGRESSION / HISTORICAL #171 IMMUTABLE**

Issue: #190  
Corrected projector source: `d25909a22f3adde313f59d372b58c139ce15ad1f`

## Purpose

Validate the two nested-feasible numerical-integrity corrections before resuming the complement KL envelope diagnostic:

- closure projector continuation from #187 / PR #188;
- finite-logit projector continuation from #195 / PR #196.

The corrected review was rerun with the exact historical #171 inputs and compared against the immutable exact #171 artifact.

No historical result is rewritten.

## Exact artifacts

Historical #171:

- source commit: `97a4ac6119709de8089032a21b97877a522dd04d`;
- Actions run: `36325580317`;
- artifact ID: `10933539813`;
- ZIP SHA-256: `7c947134279e816357bcc8b6d7966c44fc29e49bb536d974827628068e769f48`;
- exact JSON SHA-256: `55597e0f240b439531b872e99dfec9bafee73323e3c39d18943529069907537e`;
- exact JSON size: 2,757,195 bytes.

Corrected regression:

- source commit: `d25909a22f3adde313f59d372b58c139ce15ad1f`;
- temporary PR: #197;
- Actions run: `36333833072`;
- artifact ID: `10937041228`;
- ZIP SHA-256: `b8c92cc4e7a28e7a809a9254a6477178d574f4d27d22c335b26af290232b265f`;
- exact JSON SHA-256: `039e06da85a137f92d72b01defceb863605ed371597ed9f04a5240aebcfd2939`;
- exact JSON size: 3,563,220 bytes.

All non-source input hashes are identical between the two executions.

## Classification regression

No scientific classification changed.

For every D1 / D2 / D3 candidate:

- finite-interior: 7/12;
- closure-limit: 5/12;
- scientific-domain unresolved: 0/12.

Across all 36 case×candidate comparisons:

- attainment changes: 0;
- closure-boundary identity changes: 0;
- scientific-domain identity changes: 0;
- historical closure cases: 15;
- corrected closure cases: 15.

The same five target surfaces remain closure-limit for all three candidates:

- A1− / historical 0.25 → W1=1;
- A1− / historical 0.50 → W0=1;
- A2− / historical 0.10 → W1=1;
- A2− / historical 0.25 → W1=1;
- A2− / historical 0.50 → W0=1.

## Complete domain-level comparison

The comparison covered:

- 36 case×candidate combinations;
- 3 domain multipliers each;
- 108 finite-logit domain selections;
- 108 closure domain selections.

Only three of the 216 selected domain surfaces changed numerically.

No corrected selected objective is worse than its historical counterpart.

### Finite-logit change

A1+ / historical 0.25 / D3 Bernoulli KL / 32×:

- old objective: `0.003595362029283727`;
- corrected: `0.0035953619687837824`;
- improvement: `6.049994446394313e-11`;
- old/new response probability RMS: `7.126035805054217e-06`;
- old/new logit RMS: `4.2071537092034067e-05`;
- corrected selected source: exact previous-domain feasible candidate.

The response change is smaller than the same-candidate historical closure-versus-finite response scale already retained in #171 (`1.3091398573460358e-05` probability RMS).

### Closure changes

A2− / historical 0.50 / D1 stabilized utility RMS:

At both 16× and 32×:

- old objective: `0.11333333333465817`;
- corrected: `0.11333333333432018`;
- improvement: `3.379935220593211e-13`;
- old/new response probability RMS: `8.631549627505044e-09`;
- old/new logit RMS: `6.390065296345079e-07`.

At 16× the continuation optimizer selected the improved surface; at 32× the exact previous-domain feasible surface was selected.

The response change is about 0.12% of the same-candidate historical closure-versus-finite probability-RMS scale retained in #171.

## Optimizer-start regression

Historical execution:

- finite-logit successful optimizer starts across all domains: 972;
- closure successful optimizer starts: 972;
- failed optimizer starts: 0 for both paths.

Corrected execution:

- finite-logit successful optimizer starts: 1,044;
- closure successful optimizer starts: 1,044;
- failed optimizer starts: 0 for both paths.

The additional 72 successful starts per path are exactly the two widened domains × 36 case/candidate combinations.

The exact carry-forward candidate is not counted as an optimizer start.

In the corrected exact regression:

- finite-logit continuation was enabled in 72 widened domains;
- closure continuation was enabled in 72 widened domains;
- exact carry-forward was ultimately selected once in each projection path;
- the maximum raw apparent nested increase after adding continuation was 0 for both paths.

## Sign-comparison regression

Only the A1 / historical 0.25 / D3 plus value changes because of the finite-logit improvement:

- plus distance changes by `-6.049994446394313e-11`;
- plus-minus difference changes by the same amount;
- plus/minus ratio changes by `-8.174263044224972e-09`.

No sign classification or scientific interpretation changes.

## Verdict

The regression gate passes.

The nested-feasible corrections:

- preserve every attainment classification;
- preserve every closure identity;
- introduce no scientific-domain unresolved case;
- never worsen a selected domain objective;
- retain zero failed optimizer starts;
- alter response surfaces only below the numerical response scale already retained by #171.

The corrected finite-logit and closure projectors can therefore be used prospectively.

Historical #171 remains immutable.

## Next gate

Resume Issue #182 and complete the four complement KL envelopes using the corrected projectors.

The already observed complement-plus envelope result remains scientifically important, but #182 should retain one coherent corrected-projector result before any prospective KL-grid redesign.

## Boundary

`NUMERICAL-INTEGRITY REGRESSION = PASS`

`HISTORICAL #171 = IMMUTABLE`

`D1 / D2 / D3 / DOMAINS / NESTED TOLERANCE = UNCHANGED`

`CORRECTED PROJECTORS = PROSPECTIVE USE ALLOWED`

`KL V1 TARGET GRID = NOT REVISED BY THIS RESULT`

`#182 DETERMINISTIC ENVELOPE = NEXT`

`STOCHASTIC CHARACTERIZATION / PAIRED BOOTSTRAP = NOT AUTHORIZED`

`AUTHORITATIVE POWER / CORE GRID / HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
