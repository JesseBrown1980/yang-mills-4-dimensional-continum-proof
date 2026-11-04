# Second seat's recheck of YM4-02c at commit c32087a

Target: `c32087a3f2c54412bb3028f7d0a53b8b63d6133c`, on the branch `ym4-02c-reflection-transfer`. The seat ran in its own folder, `C:/tmp/opus55/recheck-02c-20261103`, and shares a model family with the builder.

**Verdict, verbatim from its report.** "Not merge ready: one blocker remains, and it comes from my own suggested fix." And: "It is a one-line fix, and no theorem or predicted value moves." And: "Everything else the builder listed holds."

**How it was run.** Python, standard library, integers only, at below-normal priority, with its earlier helpers from `../src/exact.py`. Rust for the walker `rust/rp5.rs`, whose compiled file carries the commit of rustc 1.81.0, and its earlier `../rust/brute.rs` for `out/sitec.out`. It ran the script and the workflow's steps at this head, 85 mutants of the script, whose rows are in `mut/mut3.out`, `mut/mut3new.out` and `mut/mut3tail.out`, 4 more in `mut/mut4.out`, and the sabotages on 6 mutants in `out/sab_on_mut.out`.

**What is here.**

- `REPORT.txt`: its report, verbatim, with each finding's evidence, the commands to reproduce it, and its fix.
- `RECHECK_FILES.hbp`, with its sidecar `RECHECK_FILES.hbp.sha256`: its own list of 88 files, with sizes and hashes.
- `src/`, `rust/rp5.rs`, `mut/`, `run/`, `out/`: the source its findings cite and its small outputs, in its folder layout.
- `FILED.hbp`: one row per file, with the delivered hash, and one row for each file held outside this folder.

The bytes as filed are rows in [`../SHA256SUMS`](../SHA256SUMS), with the paths `recheck/...`.

**Bytes.** Its Python, Rust, shell and `.cmd` files are byte for byte as delivered. Its outputs that were written with CRLF on Windows are filed with LF, so that every new text file in this repository has 0 CR. Their text is unchanged, and `FILED.hbp` carries each delivered hash and where each CR stood. `cr_on=every_line` comes back through `sed 's/$/\r/' FILE | sha256sum`, and `cr_on=last_line`, which is `out/sitec.out` alone, through `sed '$ s/$/\r/' FILE | sha256sum`. The workflow `reflection-transfer.yml` checks this, and it checks that every row of its list is a row of `FILED.hbp`.

**Held outside, by hash in `FILED.hbp`.** Its compiled walker `rust/rp5.exe`, whose source is here. `run/t.py` and `run/receipt.txt`, which are the blobs at c32087a, and `run/base.out`, its run of that script, which equals that receipt after CR removal. `src/no_float_gate.py`, the same bytes as `scripts/no_float_gate.py` at 08f5361. `out/lemma.worddiff`, which `git diff --word-diff=porcelain 1618199 c32087a -- docs/LEMMA-0004-REFLECTION-TRANSFER.md` regenerates byte for byte.

**In its folder and outside its list.** `head/`, its copy of the branch at this head. `mut/out3/`, `mut/out4/`, `mut/out5/` and `mut/old/`, the mutants that `mut/mut3.py`, `mut/mut4.py`, `mut/sab_on_mut.py` and `mut/old_letters.py` generate. `wf/`, its simulation of the workflow's steps. `rust/rp5.pdb`, a debug file. `run/base.lf`, the same bytes as that receipt.

**Tags.** A value in `REPORT.txt` is MEASURED by the second seat on that host, and this folder records it. The owning gate for this repository's rows is the hosted workflow. What the builder did with each finding is in Remark 6.2 and sections 10 and 11 of [the lemma](../../../docs/LEMMA-0004-REFLECTION-TRANSFER.md) and in the rows of [the prediction](../../../docs/PREDICTION-YM4-02c.hbp). The report's retraction of its CONJECTURE concerns the wording in [`../REPORT.txt`](../REPORT.txt), which stays as filed.
