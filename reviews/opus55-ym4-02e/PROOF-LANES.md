# The second seat's four proof lanes on YM4-02e, at `a72a0c3`

**All four ran and none failed. Their reports follow verbatim.** Each lane's findings and holds are in [`proof-lanes/`](proof-lanes/). Their scripts would add list rows here, so they are held on this machine at `D:/safety-backups/opus55-02e-proof-lanes-20261104-tools.tar.gz`, 191 files, SHA-256 `83d95c4822d93e4e3c107ba9000125f63cc815ef436c2f24827bfe00e5f4930c`, and their upload to the Hugging Face dataset is OPEN.

## Theorem 5, the proof

VERDICT: HOLD at a72a0c3, on text only. Every proof step of Theorem 5 checks by hand (DERIVED). No falsifier found.

**Holds** (all in `docs/NOTE-YM4-02e-KSTEP-AND-LOCALITY.md`; exact old and new text in HOLDS.txt):
- **H1, line 58:** σ is derived for sides ≥3, but the bold claim says every L. Replacement: σ ≤ 6(d−1)ε on every side, equal when all sides ≥2, and r increases with σ.
- **H2, line 58:** 0.0716 → 0.07155. MEASURED artanh(1/14) = 0.071550421, so β = 0.0716 lies outside the hypothesis.
- **H3, line 52:** add ε > 0, since r reads 0/0 at M = m.

**Answers to the questions (DERIVED unless tagged):**
- r is the correct root.
- C against D, the sweep (potential-function proof), w ≤ δ + Cᵀw, wrapped paths, removing slice 0, the limit order, compact G and PH all hold.
- σ = 6(d−1)ε is right on sides ≥3, and 1/14 is right at d = 3.
- n = 3 and t = 1 show no failure (MEASURED).

**New results (MEASURED, integers only):**
- 69 lattices: Σs ≤ 6(d−1) on all, with equality whenever the minimum side ≥2.
- Influences from the definition, 22 runs: 0 violations. On Z2 with s = 2, C reads 312012 ppm, exactly the bound, against ε = 160000. So counting s is required.
- Sylvester inertia, 34 runs up to dim 256, all met. Largest θ/r is 599606 ppm.
- Walk inequality at n = 3..6, 1246 tests: 0 violations. Worst LHS/RHS is 131402 ppm.

**Ran:** `count_s.py`, `influence.py`, `inertia.py`, `cases.py`, `big2.py`, `walk.py`, `thresh.py`.

**Could not check:**
- SU(2) numerically; only the proof lines cover it.
- Dimensions above 256.
- `big.py` (S3, w = 31,25,19) hit its 570 s timeout with no reading; `big2.py` covered S3 1×1×1 with smaller weights.
- The Dobrushin and Föllmer sources are NAMED and unopened.
- Fabric and recall were not queried; this was a proof check.

**Files** (in `C:/tmp/opus55/02e-proof-thm5-20261104/`): `FINDINGS.txt`, `HOLDS.txt`, `OUTLINE.txt`, `code/`, output logs.

## Theorem 5, trying to break it

**VERDICT:** Theorem 5's inequality is CONFIRMED on everything reached, with no falsifier found. HOLD at a72a0c3 for two low-severity text items only.

**Holds** (`HOLDS.txt`):
1. Lines 52 and 58: at ε = 0, r is 0/0 and the hypothesis still holds. Add ε > 0 and the rank-one case.
2. Line 58: "β < 0.0716" should read 0.07155. artanh(1/14) = 0.0715504 (MEASURED).

**MEASURED, certified, 0 rows above r on lattices:**
- Dense: 3150 rows, 12 groups (non-abelian S3, D4, Q8, A4, D6, Dic3), dimensions to 1728, c from 0.002 to 0.9995.
- Random class weights: 1250 rows.
- Z2 blocks: 178 rows, including 2x2 (256), 2x2x1 (4096), 3x3 (262144), 5x2 (1048576; one row).
- Dense 4096: Q8 2x1, V4 3x1, and Z2 2x2x1 (first-pass engine, agrees with blocks).
- Exact Bareiss inertia: 15 cases pass.

**Largest θ/r:**
- One link, ε = 1/1000: 0.999999.
- With plaquettes, 1x1: 0.998999.
- Near c = 1: 0.357 (1x1), 0.250 (8x1), 0.160 (2x2x1).

**New results:**
- DERIVED: index-2 two-valued weights reduce exactly to Z2.
- MEASURED: σ = 6(d−1)ε also holds at sides 2.
- MEASURED, outside the note's lattice family: on K_n graph complexes at c = 1/2, θ/r rises from 0.9327 (n=3) to 0.9562 (n=12), still within r.
- CONJECTURE: θ/r → 1 on K_n.

**Ran:** own Rust 1.81 integer engine (verified fixed-point Cholesky, not clippy-gated) and Python exact checks. Early spurious rows above r came from an i64 overflow and from overshoot; both are fixed and the old rows are kept in `rows0/`.

**Could not check:**
- Z2 2x2x2: estimate only, 0.569, uncertified.
- 4x3: no row within its time limit (CANNOT_SEE).
- Non-abelian groups at sides 2x2 and up.
- Certificate entry-error bound exceeded by about 2x on rows with large A⁻¹; those rows have ratios at or below 0.36.

**Files:** `C:/tmp/opus55/02e-falsify-thm5-20261104/` (`FINDINGS.txt`, `HOLDS.txt`, `eng/`, `rows/`, `rows0/`)

## Propositions 1 to 4 and section 2

**VERDICT: HOLD at a72a0c3.** Propositions 1 to 4 and section 2 stand as mathematics. One word is false, and five scope corrections are filed.

**Holds**
1. Line 34, "needs": the bound k ≥ log n/log(1+η) is sufficient, and sharp only as n x → 0. Falsifier: θ=3/5, η=3/5, n=2, k=1 gives τ₁=15/17 ≤ 24/25 (MEASURED). 67 of 180 rows pass below the threshold.
2. Line 107: negative top value and mixed signs.
3. Line 24: Ω needs unit norm.
4. Line 22: q=1/4 is missing.
5. Line 34: ρ is undefined.
6. Line 46: Haar scale, optional.

**Confirmed**
- MEASURED, DERIVED: Proposition 1 including negative μ at odd k, and the Birkhoff predicate, 4800 rows each, bad=0.
- DERIVED: the isometry claim and the uniformity in Proposition 3.
- MEASURED: the Proposition 3 bracket on 800 rows, including degenerate top values.
- MEASURED from lattice geometry: √R_v formula, θ, 1+t², 19/10, 25/16, 779/400, 205/128.
- MEASURED: 6355, 2624 and 1000, by separate code.

**New results**
- Negative top value alone: the limit holds at every k (153/153).
- Both signs at one modulus give two limits. Z5, w=(2,3,1,1,3) reads √5 at odd k (2236 milli), and at even k 2499 milli by k=40, tending to 5/2 by hand.
- C ≥ 1 (DERIVED).
- A raises √R₂ by (1−q²)³/(4q²(1+q²)) (DERIVED). It rose at all 7 q run (MEASURED).
- τ_{j+k} ≤ τ_jτ_k (DERIVED).
- True C at L=8: 2625 milli at q=1/2, 1000 at q=1/5 (MEASURED).

**Own error, kept beside:** my first block had T₁₂=q instead of 2q², caught by my own run and corrected.

**Ran:** integer-only Python, scripts a1 to a9, with exact search on Householder kernels, Z2 lattices and Z5.

**Could not check:**
- The Birkhoff source was not opened (NAMED).
- Connected groups are derivation only.
- q>1 on the hand block.
- The repository's own test was not run.
- Fabric and recall were not asked.

**Files, in C:/tmp/opus55/02e-kstep-20261104/:**
- FINDINGS.txt
- HOLDS.txt
- DERIVATIONS.txt
- code/

## Section 4, fixed physical volume

**VERDICT: HOLD at a72a0c3.** Section 4's logic stands, including the reduction with k = t/a (DERIVED). All measured rows reproduce.

**Holds (`HOLDS.txt`, line 101 and 103 of the note):**
- H1: 𝔅 should be β sinh Ω̃/sinh kΩ̃, cosh Ω̃ = 1+κ/2. The old form fails at k = 1.
- H2: the box maximum is exact: 4π²βL^d/(t a^{d−1}), at the constant mode. MEASURED on 9 lattices.
- H3: the bold "obstruction" line is untagged and rests on the Gaussian alone.

**New results:**
- DERIVED, given Kaufman's diagonalization (NAMED): for q > q_c, C ≥ ρ(+)² = c(q)L(1+O(e^{−κL})), with c = (q²+2q−1)(1+q²)/(4q²). c(4/5) = 1271/1600.
- MEASURED: C(8, 4/5) = 6.355000. The closed form matches every receipt row compared, once the holonomy factor is included at L = 2, 3.
- C(L, q_c) reaches 1.413446 at L = 1024, toward √2.
- Fixed μ (CONJECTURE, limit formula matched to 4–5 digits): C → 1.8257 and 2.4385. τ at k = L → about 0.4526 and 0.2755. Both C limits pass the registered 1.8 ceiling.
- The larger last step is q's rounding (MEASURED).
- SU(2) ε′ = β/2 gives β < 1/7, against 0.0716 (DERIVED; the GHS step is NAMED).
- Ising on L×L, three sizes: increments fall (CONJECTURE: bounded).

**Prior art:** Dobrushin for lattice gauge correlation decay is in Chatterjee, arXiv:1811.09770. Theorem 5's closed-form eigenvalue version appeared in none of the few sources opened; the search was small, so this stays open.

**Ran:** closed-form engine, brute four-point search, integer Gaussian check, Rust Ising engine, integer TV quadrature.

**Could not check:**
- Texts of Chatterjee 2026, Osterwalder–Seiler, Föllmer and Künsch.
- Shen–Zhu–Zhu's normalization.
- Ising L ≥ 6.
- An interacting gauge family's growth at fixed t.
- A proof that (+,−) maximizes (13/13 ring cases).
- Fabric and recall were not queried.

**Files:** `C:/tmp/opus55/02e-volume-20261104/FINDINGS.txt`, `C:/tmp/opus55/02e-volume-20261104/HOLDS.txt`, scripts in `C:/tmp/opus55/02e-volume-20261104/work/`.
