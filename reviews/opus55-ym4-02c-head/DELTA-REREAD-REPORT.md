**VERDICT: HOLD at 69dfdd9f46d1bff653def9ebb8c7da7c97d17599.** Five holds, all sentences: four from PR #23 or the builder's wording, one from my own N1. Math H1 to H12 and gate H1 to H3 are applied as written, and the list sentence the builder chose is true. No theorem, receipt, pin or count moved. MEASURED unless tagged. Paths are relative to C:/tmp/opus55/delta-02c-20261104/repo, lines at this commit.

**HOLDS**

**H1. README.md:7, also on main.** Old: `finite subgroups agree with SU(2) on plaquette monomials through their strength exactly when no plane has both sides 1`. New: `finite subgroups other than {1} agree with SU(2) on plaquette monomials through their strength, on periodic lattices, exactly when no plane has both sides 1`. {1} has t=0 and agrees through 0 on 1×1: my H7, carried at Lemma 0003:41 and dropped here.

**H2. README.md:9, also on main.** Old: `stated next as this repository first wrote it`. New: `stated next in this repository's text of November 3, unchanged since commit 9d8e678`. The first README, ecfd828, reads `ACTIVE RESEARCH`, with another Jaffe–Witten URL. Lines 13 and 15 are byte-identical to 9d8e678.

**H3, also on main.** docs/PROOF_OBLIGATIONS.md:3. Old: `and in this scope read as zero spacing at fixed finite physical volume.` New: `and on this seat's reading, at target 2 of the README, read as zero spacing at fixed finite physical volume.` README.md:70. Old: `In the operator's finite scope, the infinite-volume arrow`. New: `At target 2, on this seat's reading of the operator's scope, the infinite-volume arrow`. DERIVED: "this scope" now names target 1, at fixed spacing. README:7-8 and GPT-6's relayed decision keep zero spacing "a separate open target", and PROBLEM.md:36 marks the reading. My N2 missed both lines.

**H4, YM4-02d reads as settled.** PR #22 is OPEN and unmerged at c64eed3, and its body reads attack OPEN. docs/PROOF_OBLIGATIONS.md:9. Old: `with an explicit lower bound on the gap in [YM4-02d](URL).` New: `with an explicit lower bound on the gap in [YM4-02d](URL), DERIVED on PR #22, unmerged, with the second seat's attack OPEN.` docs/LEMMA-0004-REFLECTION-TRANSFER.md:306. Old: `[YM4-02d](URL) bounds the ratio.` New: `[YM4-02d](URL), on its own pull request with the second seat's attack OPEN, bounds λ₁/λ₀.` Line 304's "the ratio" is (T_op f)/f, which Proposition 6 already bounds.

**H5, my N1 wording is too wide.** Filed row reviews/opus55-ym4-02c-head/rows/math-gap_k1.hbp: `lambda_n_on_chi_n=(exp(-beta)*l_n)^L`, DERIVED. Lemma 0004:5. Old: `The value of λ₁ for SU(2): OPEN.` New: `The value of λ₁ for SU(2) at k ≥ 2: OPEN. At k = 1 it is (exp(−β) l₁(β))^L, DERIVED by the second seat.` Add `at k ≥ 2` after λ₁ or SU(2) in `the value of λ₁ and review` (README:23), `the value of λ₁ OPEN` (ledger:9), `The value of λ₁: OPEN.` (Lemma 0004:306), `The value of λ₁ for SU(2), and` (Lemma 0004:472).

**Falsifiers.** H1: {1} differing at degree 0. H2: ecfd828 holding lines 13 and 15. H3: zero spacing placed inside target 1. H4: PR #22 merged, attack closed. H5: another k=1 eigenvalue on χ₁.

**NOTES**

- **Head behind main.** aab6536 (#24) landed after this head, with `strict=true`, so a new head is needed. `git merge-tree` is clean.
- **Hugging Face.** reviews/opus55-ym4-02c-head/README.md:31 resolves: 169,309 bytes, sha256 `72bde97d…`, 230 files. Main's README:11 links the dataset, which this head gains by merging. The dataset card links back.
- **N2's substance is right, DERIVED:** at fixed L_phys, L and β both follow a. "This seat" names nobody at README:8, PROBLEM:36 and ledger:29. README:3's "set by the operator" is GPT-6's "primary achieved scope", relayed by him: NAMED.
- **That folder's README.** Line 19's "a dated row" holds a commit and no date. Its counts match my reports, byte-equal to my session text.
- **Wording table.** Sections 6 and 8 and both old texts are exact.
- reviews/opus55-ym4-02c-last/README.md:3, "has no reading of its own by this seat", is stale, like H11's.
- `rnd.sample` in reviews/opus55-ym4-02c-last/src has no list row: site_center.py:79 (k=4000), falsifier.py:63 (k≤4). GPT-6 asked for an exception or replacement.

**RAN**

- **List:** 3 reasons changed, each true against the bytes; 0 pins or counts moved; 28/28 blob pins. Lemma sentence: 25+2+1, 16 added against main, test findings=0, those four imports.
- **Gate, CI commands, 3.13.14:** selftest failed=0; scan 98/28/0/162 failed=0; plant step rc=0; main's gate gives the same row. Delta: 45 paths, 0 newly read; its one yml change is a comment.
- **Sums:** site-sign moved its README row only, `-c` 59/59.
- **Tests:** reflection and site-sign rc=0, each receipt `cmp` equal after CR removal.
- **Hosted, all 12 runs finished:** 11 success, 1 failure: 41842584881, job `no-float-list-unchanged`, flagging `scripts/FLOAT-EVIDENCE.txt` alone. The three required checks: success.

**COULD NOT CHECK**

Osterwalder–Seiler body: CANNOT_SEE. GPT-6's reading: NAMED. PR #22's proof: outside this read. Linux: hosted logs only.

**FITNESS**

**Not this SHA.** Five sentence holds, and `strict` blocks it now main moved. Mathematics, receipts, gate and list are fit; the changed lines then need a re-read.
