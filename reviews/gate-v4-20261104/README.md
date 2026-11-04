# Gate v4, November 4, 2026

[`scripts/no_float_gate.py`](../../scripts/no_float_gate.py) reads the blob of every tracked file and fails on what it finds apart from [`scripts/FLOAT-EVIDENCE.txt`](../../scripts/FLOAT-EVIDENCE.txt). Its docstring states what it reads and its limits. A pass is evidence, and no proof of integer-only execution.

| File | What it holds |
|---|---|
| `GATE-V4-PREDICTION.hbp` | What was expected, pushed at commit 08d23b3 before the integrated run, and kept as pushed |
| `GATE-V4-RESULTS.hbp` | Each predicted row with MET, MISS or NOT_MEASURED, the totals on the frozen gate and on the gate as it now stands, the holes found in its own merge, and findings by kind per tree |
| `raw/` | The rows behind those totals, one file per section and lane |
| `INTEGRATED-20261104.hbp` | The tree after #10, #11, #13 and the compiled small form came in: the selftest, the scan, the list by rule, the workflows' run blocks and the simulated pull requests, with what stays NOT_MEASURED |

Two workflows run it. [`no_float.yml`](../../.github/workflows/no_float.yml) runs the change's own copies, on pull requests and on pushes to `main`. [`no_float_base.yml`](../../.github/workflows/no_float_base.yml) runs the base commit's gate over the pull request's list and files as data, and flags any change to the gate, the list or either workflow for a person to read. Their steps were run locally under `bash -e`. Hosted runs are NOT_MEASURED until a pull request runs them.
