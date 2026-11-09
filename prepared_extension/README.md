# Prepared data extension

Completed: 71 prepared tasks, 426 model-split vectors, 852 F2 distance-specific analyses, 301 independently checked witnesses. This extension is separate from the source-traceable UCI experiments. Collection categories are not verified domain labels. Related sources and repeated splits are not independent observations.

## Read first

- `dataset_catalog.csv`: all 83 candidate tables, 11 exclusions, one unsplittable task, raw counts, feature exclusions and input hashes.
- `category_summary.csv` and `summary.json`: full completed outcomes. A budget ≥3 is a lower bound; timeout is unknown.
- `selection.json` and `protocol.json`: decisions recorded before fitting and certification outcomes.
- `all_results.json`: outcome of every one of the 852 analyses (also exported as `results/prepared_extension/All 71 tasks results.xlsx` at the repository root). D016 has no analyses because no rows remain after prescribed conflict removal; no model or certificate was fitted for it.
- `DATA_SOURCES_PREPARED.md` and `DATA_SOURCES_PREPARED.csv`: source, stated licence, licence basis and redistribution class for each of the 71 completed tasks, plus data-quality notes. Licences come from the author's dataset description sheet or the UCI repository policy; 12 tasks have no licence information yet.
- `environment.json`: execution host and dependencies. Concurrent timing is diagnostic, not a baseline comparison.
- `verify.py`: independent rational winner rescans, split checks, single-edit checks and replay of all completed budget verdicts.
- `summarize.py`: rebuilds numerical summaries and Figure 4 from saved outcomes.
- `update_manuscript.py`: not included in the public repository (it edits the private manuscript file).

## Replay

From the package root:

```
python prepared_extension/verify.py
python integration/verify_all.py
```

## Refit

Use a fresh copy. Extract the five supplied RAR archives into a directory preserving the relative paths in `selection.json` (archive stem / original contained directories). Set `PREPARED_DATA_ROOT` to that directory. Remove the copied `prepared_extension/results` directory and run `python prepared_extension/run.py`. The script refuses changed input bytes through SHA-256 assertions. Refit scores may vary across software versions. Seeds are integer split identifiers, not experiment dates.

## Scope and publication limits

Prepared inputs may contain earlier scaling, sampling or engineered outcomes. Known outcome-derived columns and identifiers are removed as listed, but this is not a complete leakage/semantic audit. Positive means encoded 1, except climate outcome=0. Label semantics must not be inferred from folder names. The extension measures exact conditional threshold sensitivity, not predictive accuracy, subject independence or natural prevalence. Upstream versions remain unresolved. Stated licences are recorded per task in `DATA_SOURCES_PREPARED.md`: 47 tasks carry open licences permitting redistribution with attribution, 2 share-alike, 3 non-commercial, 2 AGPL-3.0, and 17 are unconfirmed (12 without licence information and 5 with unspecified or restrictive terms). Prepared raw tables are not included in this release; refitting requires the author's supplied inputs. Saved derived arrays are included for verification; arrays from the 17 unconfirmed tasks should not be publicly redistributed until permission is confirmed. The UCI CC BY attribution does not apply automatically to this extension.

Original source-traceable experiments, theory, algorithms and baseline timings are retained. The extension does not replace or relabel them.


## Public repository note

This GitHub repository keeps the code, protocols, outcome records and summary tables only. The per-task folder `results/` (audits, score/label arrays, split row indices, witnesses) and `supplied_source_notes/` are kept in the archived full package, so `verify.py`, `summarize.py` and the Replay commands above need that package. `verification.json` records the full verification of all 71 tasks (852 analyses, 301 exact witnesses, 426 score vectors). Score arrays of 17 tasks without a confirmed licence (D010 D011 D019 D020 D023 D024 D025 D026 D027 D028 D029 D031 D032 D036 D038 D040 D054) should not be deposited publicly until permission is confirmed.
