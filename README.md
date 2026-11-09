# Results

Each table is given as `.xlsx` and `.csv` with the same content. All tables are generated from the JSON records by `python integration/export_results.py`; `python integration/check_public.py` confirms they match.

Common columns: `d` = decision-change distance, `status` = `exact` (minimum budget found and witness checked) or `lower_bound` (no flip set of size ≤ B exists, so the budget is larger than B), `minimum_budget` = exact minimum number of label edits, `witness_size` = size of the verified witness edit set, `stats_*` = solver counters (candidate cutoffs, envelope-pruned cutoffs, DP runs, DP stages).

| Folder | Table | Rows | Paper |
|---|---|---|---|
| `main_benchmarks/` | Source benchmark results | 84 | Tables 3 and 7, Figure 2A |
| | Cleaning sensitivity results | 72 | Table 8, Figure 2B |
| | Bank Marketing scalability results | 48 | Table 9, Figure 3D |
| | Ozone rare-event results | 12 | Table 12 |
| `revision_experiments/` | Pair-scan and MILP baseline comparison | 36 | Table 10, Figure 3C (median of 3 repeats per method) |
| | F-beta and distance sensitivity | 60 | Table 11 (F1/F2, distance fractions) |
| `synthetic_timing/` | Single-flip and swap timing | 16 | Table 4, Figure 3A–B |
| | Budget scaling | 6 | Table 5 |
| | Pruning ablation | 6 | Table 6 |
| `prepared_extension/` | All 71 tasks results | 852 | Prepared-data extension (one row per task × model × split × distance) |
| | Category summary | 12 | Table 13, Figure 4 |
| | Dataset catalogue | 83 | All candidate tables, exclusions and input hashes |
| | Data sources and licences | 71 | Source, licence and redistribution class per task |
| `verification/` | Verification summary | 8 | Recorded output of every verifier |

Timings were measured on the machines recorded in each folder's `environment.json` and are not comparable across folders.
