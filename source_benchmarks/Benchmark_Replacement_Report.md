# Completed benchmark replacement

16 October 2026. The manuscript now uses seven source-traceable UCI benchmarks. The ten-dataset supplied pilot has been removed from the empirical tables, abstract claims and accompanying source package; its previous working bundle is retained separately for historical reference.

## Completed work

- Retained the earlier CTG/WDBC phase: 12 model–split vectors, 24 analyses.
- Added Climate, Seismic, Blood, Mammographic and Spambase: 30 new vectors, 60 analyses. Settings were frozen before downloads and fitting; all selected datasets were reported. No solver change was made.
- Included original UCI archives, target mappings, source/DOI/license attribution, checksums, split IDs, scores, protocol, CPU/dependency information, results and verification code.
- Updated abstract, experimental design, Tables 1, 2 and 6, discussion, conclusion, references and reproducibility appendix. Theory and computational comparison results were retained with their existing limitations.
- Replayed all 84 outcomes and independent one-edit verdicts. All 60 exact witnesses passed Fraction cutoff and edit-count verification. Split disjointness and array dimensions passed for all 42 score vectors (21 unique splits).

## Results

| Phase | Decision distance | Score vectors | Exactly one edit | Exactly two edits | At least three | Timeout |
|---|---:|---:|---:|---:|---:|---:|
| Earlier CTG/WDBC | 5% | 12 | 4 | 4 | 4 | 0 |
| New five datasets | 5% | 30 | 23 | 3 | 4 | 0 |
| Combined | 5% | 42 | 27 | 7 | 8 | 0 |
| Earlier CTG/WDBC | 10% | 12 | 0 | 4 | 8 | 0 |
| New five datasets | 10% | 30 | 15 | 7 | 8 | 0 |
| Combined | 10% | 42 | 15 | 11 | 16 | 0 |

The two distances reuse the same vectors. Repeats share datasets and splits, so these are descriptive counts, not 84 independent experiments. A lower bound of three is not an exact minimum of three.

## Material limitations retained

Blood retains 471/748 rows after removing 200 conflicting-label-group rows and 77 further duplicates. Mammographic retains 476/961 after removing 270 and 215 respectively. This label-dependent curation substantially changes the benchmark population; feature equality does not prove duplicate identity or label error. Cleaning is disclosed, not hidden or justified as medical validation.

Positive rates after cleaning range from approximately 6.6% to 43.1%. The suite does not establish extreme-imbalance behavior. The largest validation set is 1,051; the old 25,000-record real-data claim has been withdrawn. Random splitting of shifts/simulation designs does not establish temporal or unseen-condition generalization. No test predictions were evaluated.

Historical synthetic timing CPU information remains unavailable. New CPU records cannot repair that historical fact. The release supports source-to-score refitting and saved-score certification, but cross-platform bitwise score identity is not guaranteed. No public repository has been created and no code license has been chosen on the authors' behalf.

## Next concrete priorities

The unresolved-source barrier for the included empirical benchmarks is addressed. Before submission, obtain independent proof/method review, confirm author declarations, choose a code license and deposit the reproducibility package publicly. To strengthen empirical scale, the next research experiment should be a pre-specified larger source-traceable benchmark and a cleaning-sensitivity analysis, particularly for Blood/Mammographic. These remain future work; this report does not claim they were completed or guarantee journal acceptance.
