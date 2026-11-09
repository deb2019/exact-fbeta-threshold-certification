# Exact Label-Edit Certificates for Empirical F-Measure Threshold Selection

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24086450.svg)](https://doi.org/10.5281/zenodo.24086450)

Code, result tables and verification scripts for the paper *Exact Label-Edit Certificates for Empirical F-Measure Threshold Selection in Imbalanced Classification*.

The paper asks: if a decision threshold is chosen by maximizing the empirical F_β score on validation data, what is the smallest number of validation-label edits that would change a given number of thresholded decisions? The repository contains exact algorithms for this question (all single-label reversals, all prevalence-preserving swaps, and a grouped dynamic program for any bounded edit budget), together with the results of every experiment reported in the paper.

## Results at a glance

All results are in [`results/`](results/) as Excel and CSV tables (see [`results/README.md`](results/README.md)).

| Experiment | Analyses | Exact witnesses | Score vectors |
|---|---|---|---|
| Main UCI benchmarks, cleaning sensitivity, Bank Marketing, ozone | 216 | 145 | 108 |
| Prepared-data extension (71 tasks, 12 categories) | 852 | 301 | 426 |

## Quick start

Requires Python 3.12.

```bash
pip install -r requirements.txt
python integration/check_public.py              # manifest + result tables + headline counts (seconds)
python threshold_theory/verify_budget_v2.py     # exhaustive solver check, n = 1..7 (about 5 s)
python theory_step2/audit_checks.py             # tie-policy audit (about 1 s)
python integration/export_results.py            # rebuild results/ from the JSON records
```

Run `check_public.py` first: the two theory scripts rewrite their own JSON reports (with new timings), which changes those files' hashes.

## Full replay

The saved score arrays (`*/scores/*.npz`) and per-task folders of the prepared extension (`prepared_extension/results/`) are too many and too large for this repository, so they are kept in the full source package, available from the corresponding author on request. Folder READMEs that mention them refer to that package. With the package extracted:

```bash
python integration/verify_all.py
```

checks the SHA-256 manifest and replays every certificate from the stored score arrays, without refitting any model. Its recorded output is in `original_verification.json` and `prepared_extension/verification.json`, and summarized in `results/verification/`.

The raw UCI snapshots (`*/raw/*.zip`) are included, so the UCI experiments can also be refitted with each folder's `run*.py` script; refitted scores may differ slightly across software versions.

## Repository structure

| Folder | Contents |
|---|---|
| `results/` | Summary tables (xlsx and csv) of all experiments |
| `threshold_theory/`, `threshold_influence/`, `threshold_validation/` | Solvers: exact single-flip and swap algorithms, the bounded-budget dynamic program (`budget_v2.py`), and the reference implementation |
| `verification_step1/`, `theory_step2/` | Exhaustive small-instance verification and tie-policy audit |
| `source_benchmarks/` | Main experiment on seven UCI datasets: raw snapshots, protocol, certificates |
| `cleaning_sensitivity/` | Cleaning-policy sensitivity study (Blood, Mammographic) |
| `scalability/` | Bank Marketing experiment with up to 22,608 certification records |
| `rare_benchmark/` | UCI Ozone one-hour task (2.88% positives) |
| `revision_experiments/` | Synthetic timing reruns, pair-enumeration and MILP baselines, F1/F2 distance sensitivity, Figures 1–3 |
| `prepared_extension/` | Prepared-data tasks across medical, finance, fraud, cybersecurity and maintenance tables |
| `integration/` | `check_public.py`, `export_results.py`, `verify_all.py` and the package builder |

More detail on each phase is in `PACKAGE_DETAILS.md` and the README of each folder.

## Data and licences

- **UCI datasets** (main experiments): distributed by the UCI Machine Learning Repository under CC BY 4.0. Attribution, DOIs and SHA-256 hashes are in `source_benchmarks/DATA_SOURCES.md`, `scalability/` and `rare_benchmark/`.
- **Prepared-data extension**: the source and stated licence of each of the 71 tasks are listed in `prepared_extension/DATA_SOURCES_PREPARED.md` (47 open, 2 share-alike, 3 non-commercial, 2 AGPL-3.0, 17 unconfirmed). The prepared input tables and score arrays are not included in this repository; only outcomes and summary tables are.

## Licence

The code in this repository is released under the MIT Licence (see `LICENSE`). Data files keep their original licences, as listed above.

## Citation

If you use this code, please cite the paper (citation details will be added after publication). See `CITATION.cff`.
