"""Export the JSON result records into the summary tables under results/.

Run from the repository root:  python integration/export_results.py
Every table is written as .xlsx and as .csv. No score arrays are needed.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"


def load(rel):
    d = json.loads((ROOT / rel).read_text())
    return d["rows"] if isinstance(d, dict) and "rows" in d else d


def flat(rows, drop=("witness_indices", "repeat_statuses", "raw_seconds")):
    out = []
    for r in rows:
        r = dict(r)
        for k in drop:
            if k in r:
                v = r.pop(k)
                if k == "witness_indices" and v is not None:
                    r["witness_size"] = len(v)
        st = r.pop("stats", None) or {}
        for k, v in st.items():
            r["stats_" + k] = v
        for k, v in list(r.items()):
            if isinstance(v, (list, dict)):
                r[k] = json.dumps(v)
        out.append(r)
    return pd.DataFrame(out)


def save(df, folder, name, sheet="results"):
    p = OUT / folder
    p.mkdir(parents=True, exist_ok=True)
    df.to_csv(p / f"{name}.csv", index=False)
    with pd.ExcelWriter(p / f"{name}.xlsx") as w:
        df.to_excel(w, sheet_name=sheet[:31], index=False)
    print(f"{folder}/{name}: {len(df)} rows")


def baselines():
    rows = []
    for c in load("revision_experiments/results.json"):
        base = {k: c[k] for k in ("case", "n", "g", "positives", "d")}
        for m, reps in c["methods"].items():
            secs = [x["seconds"] for x in reps]
            rows.append({**base, "method": m, "repeats": len(reps),
                         "median_seconds": sorted(secs)[len(secs) // 2],
                         "status": ";".join(sorted({str(x.get("status")) for x in reps})),
                         "minimum_budget": ";".join(sorted({str(x.get("minimum_budget")) for x in reps}))})
    return pd.DataFrame(rows)


def verification():
    o = load("original_verification.json")
    rows = [{"part": "original study", "check": ph["script"], "status": ph["status"],
             "analyses": ph["analyses"], "witnesses": ph["witnesses"], "score_vectors": ph["score_vectors"]}
            for ph in o["phases"]]
    rv = o["revision_checks"]
    rows.append({"part": "original study", "check": "revision_experiments/verify_new.py", "status": rv["status"],
                 "analyses": rv["parameter_analyses"], "witnesses": rv["baseline_witness_checks"] + rv["parameter_witness_checks"]})
    e = load("prepared_extension/verification.json")
    rows.append({"part": "prepared extension (71 tasks)", "check": "prepared_extension/verify.py", "status": e["status"],
                 "analyses": e["analyses"], "witnesses": e["witnesses"], "score_vectors": e["vectors"]})
    for f, part in [("threshold_theory/budget_v2_verification.json", "theory (exhaustive n<=7)"),
                    ("theory_step2/audit_results.json", "theory audit")]:
        d = load(f)
        ok = d.get("all_passed", d.get("status") == "passed")
        rows.append({"part": part, "check": f, "status": "passed" if ok else "FAILED"})
    return pd.DataFrame(rows).convert_dtypes()


def main():
    save(verification(), "verification", "Verification summary")
    save(flat(load("source_benchmarks/combined_results.json")), "main_benchmarks", "Source benchmark results")
    save(flat(load("cleaning_sensitivity/results.json")), "main_benchmarks", "Cleaning sensitivity results")
    save(flat(load("scalability/results.json")), "main_benchmarks", "Bank Marketing scalability results")
    save(flat(load("rare_benchmark/results.json")), "main_benchmarks", "Ozone rare-event results")

    save(baselines(), "revision_experiments", "Pair-scan and MILP baseline comparison")
    save(flat(load("revision_experiments/parameter_results.json")), "revision_experiments", "F-beta and distance sensitivity")
    syn = "revision_experiments/synthetic_rerun/"
    save(flat(load(syn + "benchmark_results.json")), "synthetic_timing", "Single-flip and swap timing")
    save(flat(load(syn + "budget_scaling_results.json")), "synthetic_timing", "Budget scaling")
    save(flat(load(syn + "budget_ablation_results.json")), "synthetic_timing", "Pruning ablation")

    pe = ROOT / "prepared_extension"
    save(flat(load("prepared_extension/all_results.json"), drop=()), "prepared_extension", "All 71 tasks results")
    save(pd.read_csv(pe / "category_summary.csv"), "prepared_extension", "Category summary")
    save(pd.read_csv(pe / "dataset_catalog.csv"), "prepared_extension", "Dataset catalogue")
    save(pd.read_csv(pe / "DATA_SOURCES_PREPARED.csv"), "prepared_extension", "Data sources and licences")


if __name__ == "__main__":
    main()
