# Source-traceable scalability experiment

Completed 16 October 2026.

## Outcome

The unchanged exact solver completed all 48 scheduled analyses and all 144 timed executions at budget cap two. The largest certification set contains 22,608 records. Outcomes: seven exact-one certificates, four exact-two certificates, and 37 lower bounds of at least three. There were no timeouts and all three timing repetitions agreed for every analysis. These are finite-score computational results, not predictive performance or universal scalability guarantees.

## Source and fixed design

Moro S, Rita P, Cortez P (2014). Bank Marketing. UCI Machine Learning Repository. DOI: https://doi.org/10.24432/C5K306 . Official source: https://archive.ics.uci.edu/dataset/222/bank+marketing . Original snapshot: https://archive.ics.uci.edu/static/public/222/bank+marketing.zip . Access is public; UCI lists CC BY 4.0, https://creativecommons.org/licenses/by/4.0/ . No upstream release number is provided; the retained ZIP checksum pins the exact downloaded bytes.

The experiment uses `bank.zip/bank-full.csv` (45,211 rows), not the separate bank-additional variant. Positive class is y=yes (term-deposit subscription). All original rows and conflicting labels are retained. The last-contact duration predictor is excluded: the experiment therefore uses 15 predictors. Unknown category strings remain explicit categories. The raw archive and attribution are included unchanged; transformations and score generation are documented here and in code. No endorsement by the dataset creators is implied.

The protocol was saved before download, fitting and outcome inspection. Three seeds (20261022–20261024) allocate feature-identical groups to approximately equal training and certification partitions. No group crosses partitions. These groups are not verified client IDs; repeated client contacts and time dependence cannot be ruled out. Random splitting does not establish prospective validity. There is no separate predictive test evaluation because the target is computational certification.

LR (C=1, max_iter=2000) and RF (120 trees, min_samples_leaf=5, max_features=sqrt) use training-only preprocessing. Numeric median imputation and LR standardization accompany categorical imputation/one-hot encoding. No resampling or class weighting is used. Within each full certification set, a seeded permutation produces nested prefixes of 1,000, 5,000 and 10,000 records, plus the full set. Models are fitted once per split and model, not refitted at every certification size.

F2, d=ceil(0.05n) and ceil(0.10n), budget cap two and a five-second solver allowance are fixed. Each analysis has three timed executions; all samples and their median are retained. Timing includes solver preparation and excludes training, loading and independent verification. These measurements compare sizes within this experiment, not competing algorithms. No timing claim is made against an unrun baseline.

## Results by size

Each size has 12 analyses: three splits × two models × two distances. The timing range below is across the 12 per-analysis medians, not a confidence interval.

| Certification n | Analyses | Exactly 1 | Exactly 2 | At least 3 | Median-time range (s) |
|---|---:|---:|---:|---:|---:|
| 1000 | 12 | 5 | 3 | 4 | 0.0116–0.0707 |
| 5000 | 12 | 1 | 0 | 11 | 0.0612–0.0784 |
| 10000 | 12 | 0 | 1 | 11 | 0.1242–0.2216 |
| 22,606–22,608 | 12 | 1 | 0 | 11 | 0.1963–0.3122 |

Nested subsets share records, and their integer disagreement distances increase with n. Changing n also changes labels, score groups and target feasibility. Consequently these measurements are not a controlled asymptotic-complexity estimate, and the exact edit radius need not vary monotonically across subset sizes. Counts are descriptive, not independent replications or estimated population probabilities. Lower-bound-three outcomes are not exact radii of three.

## Verification

All 48 outcomes were independently replayed from saved scores; one-edit verdicts matched the separate single-flip implementation. All 11 exact witnesses passed Fraction-based cutoff enumeration and edit-count checks. All 24 arrays passed group/row-disjointness, dimensionality and nested-prefix checks. CPU, versions, raw/code hashes and protocol/result hashes are recorded. Saved score arrays define exact replay; bitwise model refitting across platforms is not guaranteed.

## Manuscript-ready addition

“To examine feasibility beyond the small source benchmarks, we evaluated the UCI Bank Marketing bank-full snapshot using feature-group-disjoint training/certification splits, retaining all original observations and excluding call duration. Two fixed scoring models and three splits generated nested certification vectors of 1,000, 5,000, 10,000 and approximately 22,607 records. Across two prescribed decision distances, all 48 budget-two analyses completed; three timed executions per analysis agreed throughout. At full size (22,606–22,608), per-analysis median solver times ranged from 0.1963 to 0.3122 seconds in the recorded environment. Independent replay confirmed all outcomes and all 11 exact witnesses. This supports low-budget computational feasibility at the tested scale on one additional dataset; it does not establish high-budget scalability, a universal speedup or clinical/population robustness.”

This is an additional scalability experiment, separate from the seven-benchmark main table. It does not restore the earlier unaudited 25,000-record claim. The newly measured maximum is 22,608. The main manuscript has not been overwritten by this supplement.

## Reproduce

Extract the accompanying ZIP and install `requirements.txt` in a Python 3.12 environment. Run:

```
python scalability/verify.py
```

To refit, use a separate copy and remove `scalability/completed.json`, `results.json` and generated files in `scores/`, retaining the frozen protocol and raw ZIP; then run `python scalability/run_scalability.py`. The raw archive, unchanged solvers and required helper are included. The original helper's model-fitting main function is never invoked by the scalability import. Source data are CC BY 4.0; public deposition and an author-approved code license remain pending.

## Remaining synthesis

The cleaning-sensitivity and larger-source scalability experiments are now completed. They should be integrated into the manuscript together, preserving their distinct protocols and avoiding pooling dependent analyses as independent datasets. Independent expert proof review and author-confirmed publication declarations remain separate requirements.

Recorded CPU: INTEL(R) XEON(R) PLATINUM 8573C. Python: 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]. NumPy 2.3.5; pandas 2.2.3; scikit-learn 1.8.0.

Raw snapshot SHA-256: `e0bf5f5de5b846e2f18e9d90606637267d46dfa260e0f17bb12e605db5efbeb4`.
