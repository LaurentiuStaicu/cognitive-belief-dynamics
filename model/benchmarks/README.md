# Benchmark configurations

This directory contains synthetic model-recovery configurations and retained authoritative outputs used to evaluate the identifiability and discrimination of the M1.E4 candidate families. These files are scientific calibration and validation artifacts; they are not active runtime state.

The retained configurations define candidate-recovery, trial-count refinement, participant-aware screening, participant confirmation and protocol-robustness analyses. Random seeds, replicate counts, operating points, candidate families and decision thresholds are frozen in the corresponding JSON contracts and configuration files.

The retained result files under `results/` provide the authoritative numerical summaries and integrity hashes. The participant-aware confirmation result uses 200 replicates per selected cell. All 18 primary P64_X10 cells meet the declared 0.80 recovery gate, with a minimum observed recovery of 0.92; the result remains a synthetic model-recovery finding and does not select EVSD or 2HT as human truth, identify Pencode or authorize participant recruitment.

The separate authoritative Phase M protocol-robustness stress result is `PROTOCOL_ROBUSTNESS_FAIL`. Three of 18 prospectively frozen stress cells fall below the 0.80 recovery gate (`ITEM_MODERATE__EVSD` = 0.780, `ITEM_HIGH__EVSD` = 0.560, `COMBINED_ADVERSE__EVSD` = 0.585), and the minimum recovery probability is 0.56. The participant-aware confirmation result and the Phase M stress result answer different questions and must be reported together rather than treating the earlier confirmation pass as evidence of general protocol robustness.

Interpretation of every benchmark is bounded by the corresponding files in `model/contracts/`. Failed or inconclusive cells are retained as scientific results rather than converted into model-selection claims.
