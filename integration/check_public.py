"""Checks that need no score arrays.

1. Every file listed in SHA256_MANIFEST.json matches its hash.
2. The tables in results/ are exactly what integration/export_results.py
   produces from the JSON records.
3. The headline counts reported in the manuscript.

Full replay of every certificate (integration/verify_all.py) needs the score
arrays from the archived package; see README.md.
Run from the repository root:  python integration/check_public.py
"""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

import pandas as pd

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "integration"))
import export_results  # noqa: E402

for f, h in json.loads((R / "SHA256_MANIFEST.json").read_text()).items():
    assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f"hash mismatch: {f}"

with tempfile.TemporaryDirectory() as tmp:
    export_results.OUT = Path(tmp)
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        export_results.main()
    fresh = sorted(p.relative_to(tmp) for p in Path(tmp).rglob("*.csv"))
    kept = sorted(p.relative_to(R / "results") for p in (R / "results").rglob("*.csv"))
    assert fresh == kept, "results/ tables differ from the export list"
    for rel in fresh:
        a = pd.read_csv(Path(tmp) / rel)
        b = pd.read_csv(R / "results" / rel)
        pd.testing.assert_frame_equal(a, b)

o = export_results.load
rows = sum(len(o(f)) for f in ["source_benchmarks/combined_results.json", "cleaning_sensitivity/results.json",
                               "scalability/results.json", "rare_benchmark/results.json"])
wit = sum(sum(1 for r in o(f) if r.get("witness_verified")) for f in
          ["source_benchmarks/combined_results.json", "cleaning_sensitivity/results.json",
           "scalability/results.json", "rare_benchmark/results.json"])
ext = o("prepared_extension/all_results.json")
assert rows == 216 and wit == 145
assert len(ext) == 852 and len({r["dataset"] for r in ext}) == 71
assert sum(r["status"] == "exact" for r in ext) == 301
print(json.dumps({"status": "passed", "manifest_files": len(json.loads((R / "SHA256_MANIFEST.json").read_text())),
                  "tables": len(fresh), "original_analyses": rows, "original_witnesses": wit,
                  "extension_tasks": 71, "extension_analyses": len(ext), "extension_exact": 301}, indent=2))
