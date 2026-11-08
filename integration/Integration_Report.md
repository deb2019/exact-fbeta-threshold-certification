# Manuscript integration completed

17 October 2026

The manuscript now incorporates cleaning sensitivity in Section 7.4 / Table 7 and Bank Marketing scalability in Section 7.5 / Table 8. Abstract, introduction, limitations, conclusion, references, data availability and reproduction instructions have been updated. Appendix table numbering is now 9–11.

The combined package preserves three distinct experimental blocks: main benchmarks (84 analyses), cleaning sensitivity (72), and scalability (48). There are 102 saved score vectors and 142 exact witnesses across 204 analyses. These totals are not independent sample sizes. Eight distinct datasets are represented; sensitivity repeats two existing datasets, and nested scalability subsets reuse rows and scores.

The main seven-benchmark maximum n=1,051 remains explicitly scoped to that experiment. The separate Bank Marketing experiment reaches n=22,608; the old unaudited 25,000-record claim remains excluded. Cleaning-dependent budget counts and limitations of random feature-group splitting are disclosed. No new theory or speedup claim was introduced during integration.

The consolidated archive includes raw sources, frozen protocols, score arrays, split indices, solver/verification code, environments, hashes, synthetic checks and the manuscript builder. Its root README supersedes historical phase-report statements that integration is pending. Run `python integration/verify_all.py` after extraction to verify file hashes and replay all 204 certificate outcomes and 142 witnesses.

Remaining submission tasks: author-confirmed identities and declarations, independent expert proof review, public repository deposition, and an author-approved code license. This release is a consolidated research draft, not a guarantee of journal acceptance.


The subsequent baseline/presentation revision is documented in revision_experiments/Revision_Report.md and included in this archive. Core experiment totals remain unchanged; new baseline repetitions and parameter analyses are reported separately.


The rare-positive ozone extension adds six score vectors, 12 analyses and three exact witnesses. Updated consolidated totals are 108 vectors, 216 analyses and 145 witnesses across nine distinct datasets. Section 7.8/Table 11 reports this separate experiment; older core totals above describe the preceding release.
