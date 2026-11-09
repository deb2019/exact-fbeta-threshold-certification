# Revision following the baseline and presentation review

The revision adds a direct arbitrary-two-edit cutoff-scan baseline and a SciPy/HiGHS MILP reference. Both include the same objective tie policy and decision-disagreement requirement as the DP. The pair baseline includes same-direction edits, not only prevalence-preserving swaps. The MILP formulation, numerical-solver limitations and valid big-M bound are documented in README.md.

The initial cooperative-only timing attempt was superseded after a large MILP presolve overrun. All scheduled cases were rerun with the same process guard for all methods. Preliminary records are retained for transparency and are not the final benchmark. Unknown/timeout is never interpreted as infeasible; censored observations do not produce ordinary speedup ratios.

The manuscript's synthetic timing tables now use reruns with recorded CPU/software information. Table 4 and Table 5 retain distinct seeds and repetition counts, stated explicitly. The main-data CPU history is kept separate. Three new figures explain a verified label-edit witness, certificate/cleaning counts and computational performance. Figures derive from saved numerical results and are available as PNG, PDF and SVG.

Eleven display equations are converted to native editable Word math (OMML). The title now describes label-edit certificates for empirical F-measure threshold selection; no claim is made that the procedure itself makes a cutoff robust. Decimal subsection headings, first-citation reference ordering and table numbering are corrected. Revision subtitles, the working-draft footer and the embedded submission to-do appendix are removed. Internal pilot history is removed from the manuscript; historical data are not reintroduced. Author/funding/conflict declarations are not fabricated.

A 60-analysis descriptive F1/F2 sweep varies required decision fractions over 1%, 2.5%, 5%, 10% and 20% on six existing score vectors. Real g values are reported for the direct baselines. No new extreme-imbalance dataset is added; the paper retains its explicit limit on that empirical claim. The unchanged original source experiments and 204-analysis replay remain separate from the new baseline repetitions and parameter sweep.

The baseline comparisons assess these reference implementations and a limited design. The pair scan is faster in some cases; MILP timeouts do not establish that every possible MILP/CP-SAT formulation is slower. External proof review, author-confirmed declarations and licensing remain pending. The user controls GitHub upload; this revision performs no GitHub changes. If an older manuscript version has been publicly posted or submitted, the authors should record the version change in the appropriate revision history or cover letter.

Final validation: clean-archive replay passed all 204 core analyses and 142 witnesses. New checks passed for 85 completed timed outputs, with 23 censored outputs kept separate, and all 60 parameter analyses. The DP was faster in 9 of 11 comparable completed pair-scan cases; MILP had at least one timeout in 7 of 12 cases. The current revision machine is AMD EPYC 9V74, as recorded in the protocol; earlier Bank Marketing timings retain their separate Intel Xeon Platinum 8573C record. All 23 rendered manuscript pages were visually reviewed.

## Reconciliation with the supplied earlier Claude revision

Accepted: explicit four-part contribution list, Interpretation/Limitations subsections, Phase I/II labels in the main phase descriptions and Table 6, native inline subscripts for explicit mathematical underscore tokens, and corrected reference diacritics. The published Lipton et al. ECML PKDD 2014 citation was checked against the author manuscript at https://pmc.ncbi.nlm.nih.gov/articles/PMC4442797/ and replaces the arXiv-only entry.

Already present: certificate-focused title; three verified figures; eleven editable display equations; first-citation numbering; removal of draft furniture/internal pilot history; correct timing seed/repetition distinction; recorded-hardware reruns; direct arbitrary-pair and MILP references; F1/F2 distance sweep.

Retained from the current revision: current timing measurements and their CPU records, the CTG two-edit witness figure, the pair/MILP comparisons and all 60 parameter analyses. The older Seismic illustration was not substituted: the current two-edit example also illustrates the need to go beyond one-edit checks. The algorithm and saved experimental outcomes are unchanged by this editorial merge.

Not adopted as conclusions: an AI review is not an independent expert proof review or proof of novelty. No blanket claim that a 0.5 cutoff is rarely appropriate is added. No high-budget or extreme-imbalance performance claim is added without experiments. Author declarations and code licensing remain for author confirmation. The build script was updated with the merged text so that rebuilding does not restore the older manuscript.

## Subsequent below-5% benchmark addition

The previously pending point 6 now has a dedicated experiment (Section 7.8, Table 11): the unchanged UCI ozone one-hour task has 73/2536 positives (2.88%). All rows retained, group-disjoint approximately 50/25/25 allocations, LR/RF and three seeds, F2 and 5%/10% distances, cap two. All 12 analyses completed; three exact witnesses verified. At 5%: 1 exact-one, 2 exact-two, 3 at least three. At 10%: all 6 at least three. This is one naturally rare-positive benchmark, not universal extreme-imbalance evidence. See rare_benchmark/README.md for provenance and temporal limitations. The earlier statement that this experiment was not added is superseded by this section. A direct Section 6.2 cross-reference to cleaning sensitivity in Section 7.4 was also added.
