# The second seat's attack on YM4-02b

Opus 5.5, acting as second seat for ACER-CLAUDE-FABLE5, attacked PR #11 at head `39bb57f` with the instruction to refute it. These are its receipts and tools as they ran, kept verbatim, with hard-coded paths from its scratch folder. `SHA256SUMS` pins each file.

**Its verdict:** refuted on one narrow point, with every computed number surviving. The corollary's "on any finite lattice" was false with side 1 in every direction. The lemma now states the hypothesis, and no row changed. **Correction, November 3:** its recheck at `61d49a2` found its own wording "a side of length 1" too broad: agreement runs through floor(t/2) where a plane has both sides 1, and it runs through t on the lattices and groups the lemma lists with exactly one side of 1. Its attack file stays as it ran, and the lemma carries the correction. `SHA256SUMS` is the working manifest, and it covers the second seat's files apart from this README. The histogram files came from its `t2brute` crate and were added here after that recheck, so that `first_diff_t2.py` reruns from this folder. The rows behind the measured side-1 sentences are in [`recheck/`](recheck/). [`confirm-last/`](confirm-last/) holds its last confirmation and its closed-form tools, and [`read-pr13/`](read-pr13/) holds its reading of PR #13: the forest bound and the 2O sums in d ≥ 3. `multiset_check.py` reads the rational part of each trace, so its Q8, 2T and Haar columns are the measured ones, and 2O and 2I come from `mixed_sides.py`.

| What it did | Result | Files |
|---|---|---|
| Built 2O and 2I explicitly, and averaged every monomial on S³ through degree t+1 | Exact through t, failing at t+1, for all four groups | `designs_explicit`, `grp.py` |
| Integrated the (ℤ/2ℤ)⁴ moments with no finite group and no gauge fixing | E[X²] = 24, E[X³] = 0, E[X⁴] = 6897/4, κ₄ = −15/4 | `moments_z2`, `haarpoly.py` |
| Enumerated closed surfaces by three other algorithms | The same 4 and 36 per site, and the same on periodic sides 4 and 5 through 10 faces | `surfaces*`, `classes_*` |
| Measured side 1 in every direction | Agreement runs through floor(t/2): the counterexample | `side1*` |
| Measured the first difference on the 2×2 torus for all four groups | N_p · dim(V^G) / 2^(t+1), and the same plaquette deltas | `first_diff_t2` |
| **Added what first enters log Z at β¹²** | **Reproduces the published β¹¹ coefficient, −264883/1486356480, exactly** | `stretch_b11`, `beta12_values` |
| **Added the 14-face spheres** | **Reproduces β¹³, 403651/5945425920, with residual 0** | `stretch_b13`, `b13_part.py`, `sphere_q8` |

The full row log is [`ATTACK-YM4-02b.hbp`](ATTACK-YM4-02b.hbp). Its findings are recorded in the lemma's text and in the prediction file's correction rows.
