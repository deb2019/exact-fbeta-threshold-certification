# Consolidated research archive

This release integrates the cleaning-sensitivity and Bank Marketing scalability experiments into the methods manuscript, Sections 7.4–7.5 and Tables 7–8. The original seven-benchmark main table remains a separate experiment. There are nine distinct source datasets in total; Blood/Mammographic reappear in sensitivity experiments.

## Certificate replay

Install `threshold_validation/requirements.txt` in Python 3.12, then run from the extracted root:

```
python integration/verify_all.py
```

The command checks the SHA-256 manifest and runs all four replay scripts. Expected output: 216 analyses, 145 exact witnesses and 108 saved score vectors. These are artifact counts, not independent statistical replications. The 144 scalability timing executions repeat 48 analyses and are not additional observations. The suite checks saved-score solver outcomes, independent single-edit verdicts, Fraction witnesses, split disjointness and nested prefixes where applicable.

## Contents and phase-specific refitting

- `source_benchmarks/README.md`: seven-benchmark main experiment (84 analyses, 42 vectors, 60 witnesses); original CTG/WDBC phase in `threshold_validation/`.
- `cleaning_sensitivity/`: paired feature-group allocations across three policies (72 analyses, 36 vectors, 71 witnesses).
- `scalability/`: Bank Marketing nested certification sizes up to 22,608 (48 analyses, 24 vectors, 11 witnesses).
- `methods_manuscript/`: not included in the public repository. The manuscript will be linked here after publication.
- `threshold_theory/`, `threshold_influence/`, `verification_step1/`, `theory_step2/`: algorithms, synthetic timing results and exhaustive checks.

Preserve frozen protocols and delivered results. Refit only in a separate copy, following each phase report. Refitting may change floating-point scores across hardware/dependency versions; saved arrays define exact replay. The historical ten-dataset pilot and its unresolved source data are excluded. Earlier phase reports are historical records; their statements that integration is pending are superseded by this root README and the integrated manuscript.

## Sources and release status

Seven source attributions are in `source_benchmarks/DATA_SOURCES.md`. Bank Marketing attribution, DOI, license and raw hash are in `scalability/Scalability_Report.md`, `protocol.json` and `environment.json`. All nine source snapshots are included under UCI CC BY 4.0 attribution terms. No dataset version number is invented: raw hashes pin the snapshots. No public repository deposition or code license is asserted.

The planned source replacement, cleaning-sensitivity, larger-source scalability and manuscript integration are complete. Author identities/declarations, public repository deposition, an author-approved code license and independent expert proof review remain to be finalized. The revised synthetic tables use new runs on recorded AMD EPYC 9V74 hardware. Older timing files remain historical records. General high-budget scalability, clinical validity, performance across arbitrary extreme-imbalance settings and universal speed superiority are not established.

## Baseline and presentation revision

Sections 7.6–7.7 add arbitrary-two-edit pair enumeration, SciPy/HiGHS MILP, and a 60-analysis F1/F2 distance sweep. Three publication figures are included; the equations are listed in `revision_experiments/equations.md`. See `revision_experiments/README.md` for reproduction and timeout handling. Install SciPy 1.17.0 for the MILP experiment. The consolidated verifier also checks 85 completed timed outputs, 23 censored outputs and the 60 parameter analyses separately from the original 204 analyses. The 120-instance exhaustive baseline check is recorded separately. To rebuild the manuscript, pandoc is not needed: the editable equation document is included.

## Naturally rare-positive extension

Section 7.8 and Table 11 add UCI Ozone Level Detection (onehr.data): 73 positives among 2,536 original rows (2.88%), all rows retained. `rare_benchmark/` contains the source snapshot, pre-fitting protocol, six score vectors, 12 analyses, three witnesses and an independent replay script. Its README records provenance and the temporal/random-split limitation. Core totals now include this extension (216 analyses, 145 witnesses, 108 vectors); baseline repetitions and the 60 parameter analyses remain separate.


## Prepared-data extension added 5 November 2026

See prepared_extension/README.md. Additional 71 prepared tasks, 426 vectors and 852 analyses. UCI licensing and source-traceability statements above apply only to the original phases. The supplied prepared inputs have unverified upstream preprocessing and are not bundled; per-task sources and stated licences are listed in `prepared_extension/DATA_SOURCES_PREPARED.md`. The updated manuscript includes Sections 6.4 and 7.9, Table 12 and Figure 4. Integration replay reports original and extension counts separately.
