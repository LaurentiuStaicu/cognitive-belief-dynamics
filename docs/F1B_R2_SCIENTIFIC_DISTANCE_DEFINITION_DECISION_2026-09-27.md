# F1b R2 Scientific Distance-Definition Decision

Status: **DECISION COMPLETE / NEW FUTURE DEPARTURE DEFINITION / NO STOCHASTIC AUTHORIZATION**

Issue: #171  
Decision baseline: `d87a034589df725d33dcb18f6ca0a836508b47e5`

## Decision

For future prospectively versioned F1b R2 controlled-departure designs, use:

`D_KL = mean_j KL(Bern(p_general,j) || Bern(p_CBD,j))`

minimized over the **closure of the CBD response family on the explicitly declared design measure**.

The direction is:

`general generator -> CBD restricted family`

The primary reported quantity is **mean Bernoulli KL**.

`sqrt(2 × mean KL)` remains a scale diagnostic only.

Do not describe this quantity as a symmetric metric. It is a directed information divergence.

## Why D3 is selected

The decision is based only on the prospective scientific criteria frozen in #171.

It is not based on:
- historical #158 rejection rates;
- which sign was easier to detect;
- historical monotonicity;
- numerical convenience;
- preservation of the old 0.10 / 0.25 / 0.50 coefficient paths.

### 1. Direct relation to the observation model

R2 observations are binary and the fitted models use a Bernoulli/logistic likelihood.

For a fixed Bernoulli generator, the expected excess log-loss incurred by approximating it with another Bernoulli model is the directed KL divergence from the generator to the approximation.

Therefore D3 measures the information loss that is directly relevant when the CBD family approximates the declared data-generating response surface.

This is also the standard misspecification interpretation of the pseudo-true likelihood approximation.

### 2. Distribution-level rather than coordinate-level definition

D3 is defined by the Bernoulli response distributions on the frozen design cells.

Changing the parameter coordinates used to represent the same CBD response surface does not change the divergence.

That is the relevant invariance property for the scientific use here.

### 3. Operational fitter bounds are excluded from the scientific definition

The retained projection-bound audit showed that the historical bounded utility-RMS distance could change materially when inherited AP-A fitting bounds were widened.

Those operational bounds therefore cannot remain part of the scientific departure-strength definition.

The future D3 projection is to the response-family closure, not to the current fitter box.

The operational fitter and its bounds remain unchanged until a separate implementation gate says otherwise.

### 4. Closure handling gives the correct existence statement

The closure review found the same attainment structure for D1, D2 and D3:

- 7/12 retained complement surfaces: finite-interior nearest point attained;
- 5/12: the infimum lies at the finite-logit family closure;
- 0/12: scientific bias/reward domain unresolved.

The same five target surfaces reach closure under every candidate.

Therefore closure behavior is a property of the restricted response-family geometry, not a defect specific to D3.

For future D3 designs, projection must explicitly report whether the selected response surface is:
- finite-interior attained; or
- closure-limit / non-attained by finite logit coordinates.

A finite parameter vector must never be invented merely to hide non-attainment.

### 5. Saturation has the scientifically appropriate consequence

The deterministic sign-geometry audit showed that equal logit-RMS separation can correspond to very different probability and information separation near saturation.

D1 therefore treats departures as equally strong even when the Bernoulli observation model carries substantially different information.

D3 does not erase that asymmetry. It measures it as expected log-loss.

That is a feature for this scientific purpose, not a criterion failure.

At probability boundaries where an approximating CBD response assigns zero probability to an event generated with positive probability, directed KL may be infinite. Such behavior is scientifically meaningful and must be retained explicitly rather than clipped into an arbitrary finite distance.

### 6. Explicit design measure

The review used uniform weight over the frozen 18 B×A×R cells.

This weighting is part of the scientific definition.

Any future experimental design must declare its design measure explicitly. A change in weighting defines a different aggregate divergence and must be versioned prospectively.

## Why D1 is not selected as the primary future departure strength

Stabilized utility/logit RMS remains useful as a geometric diagnostic.

However:
- it is defined on latent logit displacement rather than expected observation-model loss;
- the same logit discrepancy is treated similarly across cells even when Bernoulli information differs greatly;
- the historical use of operational fitter bounds materially affected medium/large complement distances.

Removing the bounds fixes the second problem only partially; it does not make latent logit RMS the observation-model loss.

D1 therefore remains a retained diagnostic, not the primary scientific departure-strength definition.

## Why D2 is not selected as the primary future departure strength

Probability RMS is a distribution-level quantity and squared probability loss is associated with a proper binary scoring rule.

It is therefore scientifically legitimate as a diagnostic and is not rejected as an invalid measure.

However, the R2 observation/fitting model is Bernoulli likelihood based. For the specific task of measuring how much information is lost when a restricted CBD response family approximates a declared Bernoulli generator, directed KL corresponds directly to expected log-loss and to likelihood misspecification.

D2 therefore remains a retained diagnostic rather than the primary future definition.

## Fisher/information distance

The local information-weighted logit distance remains diagnostic only.

Fisher information describes local differential geometry. It is not automatically a global divergence for departures that can be large or approach saturation/closure.

No fourth global candidate is introduced by this decision.

## Historical-results rule

Nothing already retained is rewritten.

In particular:
- #158 remains a valid characterization of the historical bounded utility-RMS departure design that was actually frozen and run;
- #163/#166 remain the deterministic sign-geometry diagnosis of that historical design;
- #167/#170 remain the projection-bound sensitivity result;
- #171 deterministic D1/D2/D3 comparisons and closure review remain fixed evidence supporting this decision.

The selected D3 definition starts a **new prospectively versioned departure design**.

Historical labels `0.10 / 0.25 / 0.50` are not silently converted to KL values.

## Required next gate

Before any paired bootstrap, create a new deterministic KL-controlled departure design.

It must prospectively freeze:
- the scientific CBD response-family closure used for projection;
- the explicit design measure;
- multiple anchors;
- both departure signs;
- departure axes;
- a D3 target-strength grid chosen before stochastic recovery results;
- deterministic solving tolerances;
- finite-interior versus closure-limit status;
- D1/D2/Fisher diagnostics for transparency.

The new target-strength grid must not be selected to maximize historical or pilot power.

Only after that design is integrated may a paired same-dataset 49/99/199 bootstrap characterization be considered.

## Literature basis

- White, H. (1982). *Maximum Likelihood Estimation of Misspecified Models*. Econometrica 50(1), 1–25. DOI: 10.2307/1912526.
- Nielsen, F. (2020). *An Elementary Introduction to Information Geometry*. Entropy 22, 1100. DOI: 10.3390/e22101100.
- Gneiting, T. & Raftery, A. E. (2007). *Strictly Proper Scoring Rules, Prediction, and Estimation*. Journal of the American Statistical Association 102, 359–378.

These references justify the likelihood/information-projection interpretation and the distinction between global divergence and local Fisher geometry. They do not justify choosing D3 from historical CBD power results.

## Boundary

`FUTURE SCIENTIFIC DEPARTURE DIVERGENCE = D3 BERNOULLI KL GENERAL->CBD`

`SCIENTIFIC PROJECTION SET = CBD RESPONSE-FAMILY CLOSURE`

`HISTORICAL #158 DISTANCE = PRESERVED, NOT REWRITTEN`

`D1/D2/FISHER = RETAINED DIAGNOSTICS`

`NEW KL TARGET GRID = NOT YET FROZEN`

`PAIRED BOOTSTRAP = NOT AUTHORIZED`

`AUTHORITATIVE BOOTSTRAP DRAWS = NOT FROZEN`

`AUTHORITATIVE EVALUATION REPLICATES = NOT FROZEN`

`AUTHORITATIVE POWER = NOT VALIDATED`

`AUTHORITATIVE CORE GRID = NOT FROZEN`

`HUMAN N = NOT FROZEN`

`PARTICIPANT RECRUITMENT = NOT AUTHORIZED`

`RUNTIME F1B = NOT AUTHORIZED`
