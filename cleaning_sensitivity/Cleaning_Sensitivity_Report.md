# Cleaning-sensitivity experiment: completed

16 October 2026

The certificate distribution depends on data curation. The earlier one-edit results for all Blood/Mammographic primary-distance runs must not be described as cleaning-independent. Nevertheless, small edit budgets also occur when every original row and conflicting label is retained.

## Design fixed before fitting

Two datasets, three new seeds (20261019–20261021), two unchanged models (LR and RF), three cleaning policies and two distances: 36 model–split–policy score vectors, 72 certificate analyses. These repeats are dependent.

1. **All rows:** retain original observations, multiplicities and conflicting labels.
2. **Deduplicate same label:** retain one row for each feature–label combination, including both labels in conflicting groups.
3. **Exclude conflicts:** the earlier strict policy, removing all conflicting-label groups then duplicate feature rows.

Feature-identical groups, including missing-value patterns, are formed from raw predictors without labels. GroupShuffleSplit allocates approximately 50/25/25% of groups to train/validation/test; observation counts need not have those proportions. The raw allocation is shared across policies. Groups never cross partitions. No split is reselected, and no test predictions are inspected. Group identity is feature equality, not verified patient identity. Numeric imputation/scaling and categorical encoding are fitted on training rows only. Settings otherwise match the preceding source-benchmark study: F2, budgets up to two, a five-second call allowance, distances ceil(0.05n) and ceil(0.10n).

The new group-disjoint strict-policy arm is a new experiment: it must not be confused with the previous row-stratified strict-policy results. Pairing group assignments reduces one source of variation, but cleaning changes training data, validation population, n, integer distance and scores simultaneously. The comparison therefore does not identify a causal effect of deletion alone.

## Complete results

Each row contains six model–split runs.

| Dataset | Distance | Policy | Exactly 1 | Exactly 2 | At least 3 | Timeout |
|---|---:|---|---:|---:|---:|---:|
| blood | 5% | all_rows | 5 | 1 | 0 | 0 |
| blood | 5% | deduplicate_same_label | 4 | 2 | 0 | 0 |
| blood | 5% | exclude_conflicts | 6 | 0 | 0 | 0 |
| blood | 10% | all_rows | 3 | 2 | 1 | 0 |
| blood | 10% | deduplicate_same_label | 3 | 3 | 0 | 0 |
| blood | 10% | exclude_conflicts | 3 | 3 | 0 | 0 |
| mammographic | 5% | all_rows | 4 | 2 | 0 | 0 |
| mammographic | 5% | deduplicate_same_label | 5 | 1 | 0 | 0 |
| mammographic | 5% | exclude_conflicts | 6 | 0 | 0 | 0 |
| mammographic | 10% | all_rows | 3 | 3 | 0 | 0 |
| mammographic | 10% | deduplicate_same_label | 5 | 1 | 0 | 0 |
| mammographic | 10% | exclude_conflicts | 4 | 2 | 0 | 0 |

At 5%, all-row retention yields nine exact-one and three exact-two certificates. Strict cleaning yields twelve exact-one certificates. At 10%, all-row retention yields six exact-one, five exact-two and one at-least-three certificate; strict cleaning yields seven exact-one and five exact-two certificates. A lower bound of three is not an exact minimum of three. Do not interpret these counts as predictive accuracy or uncertainty intervals.

## Verification and practical decision

All 72 solver outcomes and separate single-edit verdicts were replayed. All 71 exact witnesses passed independent Fraction-based cutoff selection and edit-count checks. All 36 arrays passed row/group disjointness, length and cross-policy assignment checks. The unchanged solver hash is recorded with CPU, package versions and raw-data hashes.

**Recommended manuscript interpretation:** retain the original curated tables as explicitly conditional computational results, add this sensitivity analysis, and remove any implication that the precise budget distribution is stable under preprocessing. For broader empirical evaluation, prefer original-row retention with feature-group-disjoint splits as the default, while treating deduplication as a sensitivity analysis. This avoids discarding genuine feature-identical observations on the assumption that conflicting labels are erroneous.

## Manuscript-ready paragraph

“We assessed cleaning sensitivity on Blood Transfusion and Mammographic Mass using shared feature-group-disjoint splits across three curation policies. The experiment comprised 36 score vectors and 72 bounded-budget analyses. At 5% decision disagreement, retaining all original rows produced nine exact-one and three exact-two certificates, whereas excluding conflicting-label groups and deduplicating produced twelve exact-one certificates. Thus the precise budget distribution depends on preprocessing, although small edit budgets remain observable without deleting conflicting labels. All 72 solver outcomes were replayed and all 71 exact witnesses passed rational-arithmetic verification. Because curation changes training and validation composition, sample size and required integer disagreement simultaneously, these comparisons are descriptive sensitivity checks rather than a causal estimate of cleaning effects.”

## Reproduce

Extract the accompanying ZIP; install `requirements.txt`; from its root run:

```
python cleaning_sensitivity/verify.py
```

For refitting, work in a separate copy, remove only `cleaning_sensitivity/completed.json`, `results.json` and generated `scores/*.npz`, preserve `protocol.json`, and run `python cleaning_sensitivity/run_sensitivity.py`. Original Blood/Mammographic UCI archives, source attributions and unchanged solver code are included. Saved scores define exact certificate replay; bitwise refitting across platforms is not promised. No public deposition or new code license is asserted.

This completes the cleaning-sensitivity step. Larger source-traceable scalability evaluation remains the next experiment. This supplement does not replace the existing manuscript or its seven-dataset main results automatically.
