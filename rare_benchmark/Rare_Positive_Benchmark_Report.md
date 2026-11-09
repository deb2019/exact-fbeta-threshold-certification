# Naturally rare-positive ozone extension

Source: Zhang K, Fan W, Yuan X (2008). Ozone Level Detection, UCI Machine Learning Repository. DOI: https://doi.org/10.24432/C5NG6W . Dataset page: https://archive.ics.uci.edu/dataset/172/ozone . License: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), as stated by UCI; attribution retained, no endorsement implied. The unchanged source ZIP is included in raw/ozone.zip. protocol.json records acquisition time and SHA-256; no upstream release number is invented.

Only onehr.data is evaluated. The source names file defines 1 as an ozone day, 0 as normal, and date as ignored. All 2,536 original rows and all 73 positives are retained (2.8785%; negative/positive ratio 2463/73 = 33.74). There are 72 numeric predictors; '?' is missing. Eight duplicate feature vectors are kept in the same partition through feature-group allocation. No label-dependent cleaning, resampling or class weights are used.

The protocol was frozen after source/schema/prevalence inspection and before fitting or looking at certificate outputs. Four-fold stratified group allocations give fold 0 validation, fold 1 reserved test, and folds 2+3 train. Three seeds and LR/RF give six saved vectors. Median imputation and LR scaling are fit on training only. Model settings match the main experiment. Every validation vector has 634 rows and 18 positives (2.84%). F2, distances 5%/10%, cap B=2 and five seconds per solver call give 12 analyses. Each solver call is timed once; timings include preparation, exclude fitting/verification, and are not speedup evidence.

Results: at 5%, one exact-one, two exact-two and three lower-bound-three results; at 10%, six lower-bound-three results. No timeout. All three exact witnesses pass Fraction-based cutoff verification; all 12 outcomes and single-edit verdicts replay. Lower bound three does not imply exact budget three. Counts are dependent repeats, not independent dataset samples. The source is temporal (1998–2004); random splits support a computational certificate experiment, not future forecasting accuracy or temporal generalization. No test predictions were evaluated. One 2.88%-positive dataset addresses the missing below-5% example, not universal performance at extreme ratios.

## Reproduce

Install ../threshold_validation/requirements.txt and run `python rare_benchmark/verify.py` from the archive root. This checks source/result hashes, all-row coverage, group-disjoint partitions, labels, scores, saved outcomes and witnesses. To refit, make a separate copy, remove completed.json/results.json/scores in that copy, retain protocol.json, then run `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python rare_benchmark/run.py`. Refitting across libraries/hardware may change floating-point scores; supplied arrays define replay.

Recorded CPU: AMD EPYC 9V74 80-Core Processor. Callable time range: 5.37–19.03 ms.

## Complete result table

| Seed | Model | n | Positives | g | Distance | Certificate | Time ms |
|---|---|---|---|---|---|---|---|
| 20261025 | LR | 634 | 18 | 626 | 5% | 1 | 5.592 |
| 20261025 | LR | 634 | 18 | 626 | 10% | at least 3 | 8.053 |
| 20261025 | RF | 634 | 18 | 414 | 5% | at least 3 | 5.750 |
| 20261025 | RF | 634 | 18 | 414 | 10% | at least 3 | 5.950 |
| 20261026 | LR | 634 | 18 | 626 | 5% | 2 | 19.030 |
| 20261026 | LR | 634 | 18 | 626 | 10% | at least 3 | 10.635 |
| 20261026 | RF | 634 | 18 | 452 | 5% | at least 3 | 6.872 |
| 20261026 | RF | 634 | 18 | 452 | 10% | at least 3 | 6.369 |
| 20261027 | LR | 634 | 18 | 626 | 5% | 2 | 12.140 |
| 20261027 | LR | 634 | 18 | 626 | 10% | at least 3 | 7.719 |
| 20261027 | RF | 634 | 18 | 418 | 5% | at least 3 | 5.521 |
| 20261027 | RF | 634 | 18 | 418 | 10% | at least 3 | 5.368 |
