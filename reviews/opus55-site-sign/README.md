# Second seat's attack on the site-sign note at commit 1078e6d

Target: `1078e6d11832449fa31a50066efcef5d8c6cd10f`, the note, its prediction, its test and the receipt. It read Lemma 0004 at `c32087a3f2c54412bb3028f7d0a53b8b63d6133c`, on the branch `ym4-02c-reflection-transfer`. The seat ran in its own folder, `C:/tmp/opus55/site-sign-attack-20261103`, and shares a model family with the builder.

**Verdict, verbatim from its report.** "I could not break the SU(2) sign characterization. Theorem and Corollary hold as stated, for w != 0 a.e., k >= 2 and every side >= 2."

**How it was run.** Python 3.13, standard library, integers only, at below-normal priority. It wrote its own groups from permutations and matrices mod p, its own lattice code and exact rational quaternions, sharing no code with the test, and it ran mutants of the test and tampered copies of the prediction. `REPORT.txt` holds its findings, each with its evidence and its fix.

**What is here.**

- `REPORT.txt`: its report, verbatim.
- `code/`: its scripts, with their hard-coded paths, and its own `SHA256SUMS`.
- `out/`: its rows and exit files, and its own `SHA256SUMS`.
- `FILED.hbp`: one row per file with the delivered hash, and one row for each file or folder held outside.
- `SHA256SUMS`: the bytes as filed.

**Bytes.** The report and the scripts are byte for byte as delivered. Its `.hbp` and `.exit` files were written with CRLF on Windows, and they are filed with LF, so that every new text file in this repository has 0 CR. Their text is unchanged, and `FILED.hbp` carries each delivered hash: `sed 's/$/\r/' FILE | sha256sum` reproduces it, and the workflow `site-sign.yml` checks this. In `out/repro.txt` the line `SITE_SIGN_RUNTIME` sits among the rows, since stdout and stderr shared that file.

**Held outside, by hash in `FILED.hbp`.** `code/gate_main.py`, the same bytes as `scripts/no_float_gate.py` at `96e19a2`. `out/repro.raw` and `out/repro.nort`, the text of `out/repro.txt`. `repl/`, the same bytes as the blobs at `1078e6d`. `mut/`, its mutated copies of the test, which `code/mutate.py` and `code/mutants_auto.py` regenerate from those blobs. `code/__pycache__/`, compiled Python.

**Three scripts in the gate's list.** `code/astscan.py`, `code/decode.py` and `code/run_gates.py` stay verbatim, with a row each in `scripts/FLOAT-EVIDENCE.txt`.

**What the builder did with its findings.** The four should-fix items and the notes are applied in [the note](../../docs/NOTE-YM4-02c-SITE-SIGN.md), in rows 16 to 41 of [the prediction](../../docs/PREDICTION-YM4-02c-SITE-SIGN.hbp), and in [the test](../../tests/test_site_sign_4d.py). Remark 4.2 of Lemma 0004 sits on the other branch and stays with that branch.

**Tags.** A value in `REPORT.txt` is MEASURED by the second seat on that host, and this folder records it. The owning gate for this repository's rows is the hosted workflow. The note's status stays DERIVED with independent review OPEN: GPT-6's review is preliminary, and the operator asked for its final check.
