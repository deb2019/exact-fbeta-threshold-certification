# Prepared data extension

Completed: 71 prepared tasks, 426 model-split vectors, 852 F2 distance-specific analyses, 301 independently checked witnesses. This extension is separate from the source-traceable UCI experiments. Collection categories are not verified domain labels. Related sources and repeated splits are not independent observations.

## Read first

- `dataset_catalog.csv`: all 83 candidate tables, 11 exclusions, one unsplittable task, raw counts, feature exclusions and input hashes.
- `category_summary.csv` and `summary.json`: full completed outcomes. A budget ≥3 is a lower bound; timeout is unknown.
- `selection.json` and `protocol.json`: decisions recorded before fitting and certification outcomes.
- `results/`: per-task audits, score/label arrays, split row indices, outcomes and witnesses. D016 has an error record because no rows remain after prescribed conflict removal; no model or certificate was fitted for it.
- `supplied_source_notes/`: user-supplied provenance leads, NOT independently verified source records or licences.
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

In the public repository, the saved score arrays and `completed.json` records of 17 tasks without a confirmed licence are withheld (D010 D011 D019 D020 D023 D024 D025 D026 D027 D028 D029 D031 D032 D036 D038 D040 D054). Their outcomes remain in `results/<ID>/results.json`, `all_results.json`, `summary.json` and `category_summary.csv`. Here `verify.py` replays the remaining 54 tasks (648 analyses, 196 exact witnesses on 324 score vectors); `verification.json` records the full private verification of all 71 tasks. `summarize.py` needs all 71 tasks and runs only on the full private archive.
