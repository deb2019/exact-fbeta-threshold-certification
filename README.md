# Exact F-beta threshold certification

Research draft: **Exact Label Edit Budgets for Robust F Measure Threshold Selection in Imbalanced Classification**.

This repository studies fixed-score empirical F-beta cutoff reselection under bounded validation-label edits. It does not certify retraining, predictive accuracy or population robustness.

## Reproduce the complete experiments

Download [Manuscript_Source_Package.zip](Manuscript_Source_Package.zip), extract it into a separate directory, and run there:

```bash
python -m pip install -r threshold_validation/requirements.txt
python integration/verify_all.py
```

Use Python 3.12. The archive contains the algorithms, all eight UCI source snapshots, frozen protocols, 102 saved score vectors, split indices, environment records, manuscript builder and verification scripts. Expected replay: **204 analyses and 142 exact witnesses**. These are artifact counts, not independent statistical replications.

- Main source benchmarks: 84 analyses / 42 vectors.
- Cleaning sensitivity: 72 analyses / 36 vectors.
- Bank Marketing scalability: 48 analyses / 24 vectors, up to 22,608 certification records.

Read the extracted root README for phase-specific refitting. Saved scores define exact replay; floating-point refitting may differ across environments. No unaudited historical pilot data are included.

## Manuscript

[Download the working manuscript](Threshold_Robustness_Methods_Manuscript.docx). Author/declaration placeholders remain to be finalized. This is not a claim of acceptance or external expert approval. Historical statements inside phase reports that public upload/integration is pending are superseded by this repository README; experimental records are otherwise preserved.

## Attribution and license status

UCI source data retain their **CC BY 4.0** attribution terms. Source URLs, DOI and snapshot checksums are included in the archive's `source_benchmarks/DATA_SOURCES.md` and `scalability/Scalability_Report.md`. No endorsement is implied.

An author-approved code license is **pending**. Public availability alone is not an MIT license grant. Third-party data and dependencies retain their own licenses. No archival DOI or tagged release is claimed.

## Limits

Certificates condition on fixed floating-point scores and the specified deterministic tie rule. A lower bound of three is not an exact radius. Cleaning affects the distribution of budgets. Group-disjoint predictors do not establish patient/client independence. Budget-two scalability on one large benchmark is not a universal speedup or high-budget guarantee. Independent external proof review remains pending.
