# Second seat's attack on YM4-02c at commit 1618199

Target: `1618199d51d722124bdb5ecc0ec28c5ba3f5a9ce`, the lemma, the prediction and the test of YM4-02c. The seat ran in its own folder, `C:/tmp/opus55/attack-4d-02c-20261103`, and shares a model family with the builder.

**Verdict, verbatim from its report.** "Refuted on one count, and it is the record of misses, not the mathematics. Every theorem and proposition held up when read step by step, and every number I recomputed reproduced by a different method, so no theorem statement or predicted value changes."

**How it was run.** Python 3.13.14, standard library, integers only, at below-normal priority. Rust 1.81 for the walkers, built with `rustc +1.81 -C opt-level=3 --edition=2021 brute.rs`. It reran the builder's script and workflow steps, wrote its own group tables and lattice code, ran 54 mutants of the script, and read the literature from page images. `REPORT.txt` holds its findings, each with its evidence and the commands to reproduce it, and its folder layout is kept here.

**What is here.**

- `REPORT.txt`: its report, verbatim.
- `SECOND_SEAT_FILES.hbp`: its own list of files, sizes and hashes.
- `src/`, `rust/brute.rs`, `mut/`, `run/`: the source its findings cite and its small outputs.
- `FILED.hbp`: one row per file, with the delivered hash, and one row for each file held outside this folder.
- `SHA256SUMS`: the bytes as filed.

**Bytes.** Python, Rust and shell files are byte for byte as delivered. Its `.out` files were written with CRLF on Windows, and they are filed with LF, so that every new text file in this repository has 0 CR. Their text is unchanged, and `FILED.hbp` carries each delivered hash: `sed 's/$/\r/' FILE | sha256sum` reproduces it, and the workflow `reflection-transfer.yml` checks this.

**Held outside, by hash in `FILED.hbp`.** Its compiled walkers, the PDFs it read, its 861,528-byte histogram `rust/gram12.hist` (`brute gram12` regenerates it), and its copies of the builder's files, which are the blobs at 1618199. `mut/mutate.py` regenerates its mutants, such as `mut/out/no_inverse_full_run.py`, from those blobs.

**Tags.** A value in `REPORT.txt` is MEASURED by the second seat on that host, and this folder records it. The owning gate for this repository's rows is the hosted workflow. What the builder did with each finding is in section 10 of [the lemma](../../docs/LEMMA-0004-REFLECTION-TRANSFER.md) and in the rows of [the prediction](../../docs/PREDICTION-YM4-02c.hbp). Review by a different model family, and against the body of Osterwalder–Seiler (1978), stays OPEN.

**The recheck.** The seat rechecked the branch at commit c32087a, and [`recheck/`](recheck/README.md) holds its report and files, with their rows in `SHA256SUMS` here. Its blocker, the scoped clause, and its retraction of the CONJECTURE in `REPORT.txt` are corrected in Remark 6.2 and section 10 of the lemma and in rows beside the prediction, and `REPORT.txt` stays as filed. GPT-6's assessment of this branch is at [`../gpt6-ym4-02c/`](../gpt6-ym4-02c/README.md).
