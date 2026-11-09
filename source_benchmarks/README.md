# Source-traceable benchmark replacement, 16 October 2026

This release replaces the unaudited ten-dataset pilot in the manuscript. That pilot is retained only in the separately delivered Historical_Pilot_Working_Archive.zip, not in this package or its empirical tables. The new evidence comprises seven original UCI datasets: CTG and WDBC (earlier phase) plus Climate Model Simulation Crashes, Seismic Bumps, Blood Transfusion, Mammographic Mass and Spambase (new phase).

## Reproduce certificates

From the extracted package root, install `threshold_validation/requirements.txt` in an isolated Python 3.12 environment, then run:

```
python source_benchmarks/verify_release.py
```

Expected: 84 solver outcomes and independent one-edit checks, 60 Fraction-verified witnesses, 42 score vectors with disjoint train/validation/test rows. The 42 model runs contain 21 unique splits. This command does not fit models or access the internet. A saved lower bound of three is not an exact radius.

`source_benchmarks/protocol.json` was written before the five new downloads and model fitting. Do not overwrite it. `environment.json` records the new phase CPU, package versions and solver hash. `threshold_validation/protocol.json` records the earlier phase. The solver is unchanged. `provenance.json` gives source URLs, download URLs, DOI, license and raw SHA-256 for the new five. `DATA_SOURCES.md` covers all seven. Raw archive hashes pin the exact bytes; UCI does not provide a distinct release number for these snapshots.

## Refit from original data

Work in a separate copy of the extracted package; preserve the delivered results. In that copy, delete `source_benchmarks/completed.json`, `source_benchmarks/results.json` and the generated files under `source_benchmarks/scores/`, then run `python source_benchmarks/run_benchmarks.py`. All required raw ZIP files are included. The frozen protocol remains in place. The run refuses to overwrite a completed experiment.

For the earlier CTG/WDBC phase, make another separate copy, remove `threshold_validation/protocol.json`, `results.json`, `completed.json` and generated scores, then run `python threshold_validation/run_validation.py`. Its settings are embedded in the runner and match the released protocol; its timestamp and environment fields will describe the new fit. Compare settings and results, not timestamp equality. Training is stochastic but seeded; floating-point score identity across dependency/hardware changes is not guaranteed. Saved arrays define exact certificate replay.

## Important interpretation

Cleaning removes feature-identical conflicting-label groups and then duplicates. This removes many Blood and Mammographic observations and uses labels before splitting. These are curated computational benchmarks, not unbiased clinical/donor population samples. Identical predictor rows need not be duplicate people. No claim is made that removed labels were incorrect. The source-row IDs are zero-based data-row offsets after headers, not person identifiers. Witness indices are positions within saved validation arrays; use `validation_id` to map them back.

No test predictions were evaluated. Labels were used for stratification. Random Seismic/Climate splits are not prospective or unseen-condition validation. Repeated models, seeds and distances are dependent; counts are descriptive. No extreme-imbalance claim is made. Maximum validation n is 1,051. The earlier 25,000-record pilot scale claim has been withdrawn.

`threshold_theory/` and `threshold_influence/` contain the exact solvers and synthetic timing scripts/results. `verification_step1/` and `theory_step2/` contain saved exhaustive checks. Historical synthetic timing CPU was not recorded; the new benchmark CPU does not retroactively identify it. Algorithms and narrow novelty scope are unchanged. Public deposition, author declarations, author-approved code licensing and independent proof review remain outstanding.
