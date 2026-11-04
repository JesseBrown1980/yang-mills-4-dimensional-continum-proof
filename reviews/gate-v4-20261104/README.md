# Gate v4, November 4, 2026

[`scripts/no_float_gate.py`](../../scripts/no_float_gate.py) reads the blob of every tracked file and fails on what it finds apart from [`scripts/FLOAT-EVIDENCE.txt`](../../scripts/FLOAT-EVIDENCE.txt). Its docstring states what it reads and its limits. A pass is evidence, and no proof of integer-only execution.

| File | What it holds |
|---|---|
| `GATE-V4-PREDICTION.hbp` | What was expected, pushed at commit 08d23b3 before the integrated run, and kept as pushed |
| `GATE-V4-RESULTS.hbp` | Each predicted row with MET, MISS or NOT_MEASURED, the totals on the frozen gate and on the gate as it now stands, the holes found in its own merge, and findings by kind per tree |
| `raw/` | The rows behind those totals, one file per section and lane |
| `INTEGRATED-20261104.hbp` | The tree after #10, #11, #13 and the compiled small form came in: the selftest, the scan, the list by rule, the workflows' run blocks and the simulated pull requests, with what stays NOT_MEASURED |

Two workflows run it. [`no_float.yml`](../../.github/workflows/no_float.yml) runs the change's own copies, on pull requests and on pushes to `main`. [`no_float_base.yml`](../../.github/workflows/no_float_base.yml) runs the base commit's gate over the pull request's list and files as data, and flags any change to the gate, the list or either workflow for a person to read. Their steps were run locally under `bash -e`. Hosted runs are NOT_MEASURED until a pull request runs them.

## After it reached main, November 4

**Hosted, MEASURED,** in [`HOSTED-EXPERIMENTS.hbp`](HOSTED-EXPERIMENTS.hbp), on this repository with `no-float` and `no-float-base` required, `strict` on and admins enforced. Four throwaway pull requests, #16 to #19, closed unmerged:

| Pull request | `no-float` | `no-float-base` | `no-float-list-unchanged` | GitHub's merge state |
|---|---|---|---|---|
| #16, a float with no row | red | red | green | BLOCKED |
| #17, a float, with the pull request's gate edited to exit 0 | red | red | red | BLOCKED |
| #18, a float, with new jobs carrying the required names and exiting 0 | red and green | red and green | green and green | BLOCKED |
| #19, a clean integer change | green | green | green | CLEAN |

#18 was read with the same-named jobs finishing before the real ones and again finishing about 3 minutes after them, and it read BLOCKED both times.

**The second seat's last attack,** in [`last-attack/`](last-attack/LAST-ROUND.hbp), on the final file, sha256 935bd77b. All the builder's tallies stand: 9 Python survivors of 395 on Linux and 7 of 392 on Windows, 135 native closed of 152, 6 of 20 held-out, and 5 file-level survivors. Of 40 fresh plants written after reading the rules, each executed first to show a float, 39 pass. So this measures an attacker who has read the gate.

**What a green check says.** The gate on the default branch at that event read the blobs of the tracked files at the pull request's head, with the list that pull request carries, and found nothing outside that list. It is evidence, and no proof of integer-only execution.

**What stays open.** A float with its own pinned row passes both required checks, and only `no-float-list-unchanged` shows it, on that one pull request. A softened gate that merges once makes later checks green, flag included, so read `NO_FLOAT_BASE|gate_sha256=` in the job log against a hash kept elsewhere, and read every change to the gate, list and workflows. `scripts/no_float_compiled.sh` runs from the pull request, outside the flag. Child processes, data files, third-party code and inline shell sit outside the reading.

