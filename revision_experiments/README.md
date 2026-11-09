# Direct arbitrary-edit baselines and presentation revision

The fixed protocol compares minimum label-edit budgets up to two at d=ceil(.05n), with smallest-cutoff objective ties. All models/scores are fixed. Six synthetic cases and the first-seed LR/RF arrays from CTG, WDBC and Spambase are included without outcome-based exclusions.

## Pair enumeration baseline

`scan` sorts once, compresses records by (score group, original label), and streams batches of 256 attack types. All one-edit types are checked first. All unordered two-type combinations follow, including two positive-to-negative edits, two negative-to-positive edits and mixed edits. A repeated type requires at least two records. An exact integer tournament reselects the cutoff for each attack. Returning the first successful positive budget gives its minimum; exhausting budget two gives a lower bound of three. This is a strong author-implemented reference, not a published competitor.

## Integer programming baseline

`integer_program` uses SciPy milp / HiGHS. It enumerates P' within P±B, with the P'=0 labeling treated separately. For fixed P', integer variables C_j represent cumulative edited positives; integer e_j bound |C_j-C_(j-1)-p_j|. Constraints impose 0<=C_j-C_(j-1)<=m_j, C_0=0, C_g=P', sum(e)<=B. Binary q_k selects exactly one admissible target with |K_k-K_base|>=d. For each selected target k and every competitor j, impose:

    (u P' + v K_k) C_j - (u P' + v K_j) C_k <= -1[j<k] + M_jk (1-q_k).

A valid deactivation bound is

    M_jk = max(0, (u P'+v K_k) min(K_j,P')
                    - (u P'+v K_j) max(0,P'-(n-K_k)) + 1[j<k]).

Minimize sum(e). An optimum is considered only if the solver returns optimal; an incumbent is independently realized and checked with integer cutoff comparisons. A one-edit witness establishes the minimum immediately because zero edits cannot change the deterministic cutoff. Otherwise every edited total must be resolved to certify the optimum/lower bound. Any unresolved solve is unknown, not infeasible. MILP numerical infeasibility/optimality is not advertised as an exact-arithmetic formal proof. All returned witnesses are checked exactly, and 120 tiny configurations agree with the pair scan and DP.

This formulation is an author-implemented MILP reference using an external general-purpose solver. It is not claimed to be the fastest possible MILP or an OR-Tools implementation. It has O(g^2) target-competitor rows, which can dominate runtime/memory.

## Timing and deviation record

The initial cooperative-limit run encountered a large HiGHS model/presolve overrun. Its protocol and partial results are retained as preliminary records, not used for final timing. Final `run_guarded.py` reruns every scheduled case with a common 10-second subprocess guard (including worker startup) and a 5-second cooperative solver allowance. Successful timings measure the method callable after imports, including sorting/model construction; hard-stop times include process overhead and are censored. Rotation order and three repetitions are fixed. No timeout is assigned an ordinary completed-runtime speedup. Raw repeated statuses/timings are retained. Numerical library thread environment is OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1; HiGHS uses its default configuration.

`synthetic_rerun/` reruns the previous flip/swap, reference-DP and pruning/deque timing experiments on the recorded current machine. Their separate seeds and three-versus-five repetitions are retained and explicitly distinguished in the manuscript. Old timing files remain historical; the manuscript uses the new files.

`parameter_protocol.json` separately fixes an F1/F2 distance sweep on six saved vectors. These are descriptive, dependent analyses, not independent confirmation.

Run `verify_new.py` to check the new result witnesses and reproduce DP/pair outcomes; full timing reruns and MILP require running the guarded benchmark in a new output copy. Preserve delivered protocols/results. The new SciPy dependency is already used by the supplied environment; versions are recorded.
