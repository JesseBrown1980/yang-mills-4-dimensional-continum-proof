# VOL14-D3G review: neutral curl certificate, stationary enclosure, and the non-Abelian fields on the 4⁴ torus

**Provenance:** written by Claude (AI) on 27 Nov 2026. This is AI verification, not human review. Floating-point numerics are exploratory; **none is a certificate.**

**State reviewed:**
- PR #138 at `219a15c` (base `claude/review-13-vol14d3f-20261127`, i.e. stacked on #137).
- Seal `EXPECTED-YM4-VOL14D3G-KEYED-NEUTRAL-20261127.hbp`; supplemental receipt `YM4-VOL14D3G-FULL-SECTOR-KEYS-20261127.hbp`.

The author's file `reviews/14-D3G-NONABELIAN-PILOT-INVENTORY-20261127.md` already uses the number 14 for an inventory; this review is named `14-VOL14D3G-REVIEW-…` to avoid a clash.

## 1. Verdicts

| Item | Verdict |
|---|---|
| Replay | The D3F prerequisite reproduces the first three D3F receipt lines. `ym4_vol14d3ga_neutral_curl.py` + `ym4_vol14d3gc_sector_keys.py` reproduce the receipt byte-identically under normal and `-O` Python, and the receipt equals the seal (lines 2–5). The full-sector key checker reproduces its receipt under both modes. Total about 71 s. |
| Gates and CI | No-float gate: 200 code files, `failed=0`. Docs integrity: 120 Markdown files, 0 control characters, 0 broken links. Hosted CI at `219a15c`: 15 workflow runs (16 check runs in total), all successful, including the new *YM4 VOL14D3G keyed neutral curl and stationary enclosure* workflow. |
| **D3G-A neutral signed-curl form** | **Correct.** Rederived below (§2). The identity L_U a = 0 ⇒ L₀a = −E f, the bound ‖dT₀z‖ ≤ (1 + 12‖E‖)‖f‖, the exact signed multiplier form Σ w_i b_i (r_i f)² − 2(A_e f)(F_e f), and the final arithmetic all check. |
| Integer checker vs note | **Matches.** The checker verifies every filling against the actual path incidence (an exact Stokes identity per path), computes the folded row and column sums before taking absolute values, and its fold is exact on any cover torus of side ≥ 6 fine sites (the filling span is 5). Block centres are at 0 mod 3, the same convention as review 09's blocking map. |
| Rounding budget (§3 of the note) | **Correct and generous.** Rederiving the fixed-point errors gives at most 384/S for a_i (budget 1024/S) and at most 4472/S for b_i (budget 65536/S; the note's own cruder count is 6777/S). |
| Neutral floor | (1799/1800 − 1/30)(247/250)² = 0.94306 and the weaker (1799/1800)(247/250)² − 1/30 = 0.94227, both > 15/16. Checked with exact fractions. |
| **Stationary enclosure (§4)** | **Correct**, with one premise worth replacing (below). Repair angle 11/(7/8 − 11r) = 12.57r ≤ 13r; θ_max < 1/δ − 10⁻⁵ from the pinned deficits (slack 3.2×10⁻⁶ and 6.2×10⁻⁶ beyond that), so the 56r = 5.6×10⁻⁶ ball stays below tolerance; ratio Lipschitz 377r < 400r; b Lipschitz 11168r < 12000r; ‖E‖ ≤ 0.00132 < 1/500; ‖M‖ ≤ 0.43269 < 13/30 = 0.43333; relative floor 636875/1179648 = 0.53989 > 1/2; gradient √648·16×10⁻¹² = 4.07×10⁻¹⁰ ≤ 26·16×10⁻¹² < r/210 = 4.76×10⁻¹⁰. The inward-gradient argument, the symmetric-criticality lift from the primitive cell to the repeated lattice, the U(1) argument for the charged first derivatives and the gauge argument for the tree directions are all valid. |
| Cantor keys | **Correct bookkeeping**: 200 representatives (72 neutral, 128 charged) covering 384 sectors; 384 distinct nine-digit addresses per fixture; conjugate mates distinct; 16 self-conjugate sectors. The keys are labels: they add no mathematical content and do not affect any spectral statement, as the note itself says. |
| Non-Abelian pilots (D3G-B) | Rebuilt independently on M = 4; see §3. |

## 2. The neutral argument, rederived

At an Abelian background with path holonomies P_i, V = Σ w_i P_i, and neutral variation a, write p_i = t_e + r_i d (the checker verifies this chain identity exactly for all 10,473 path pairs per face).

1. **Constraint.** L_U a = Σ w_i a_i p_i a with a_i = Re(P_i/V) and Σ w_i a_i = 1, so L_U a = t_e a + A_e f. Since Σ w_i(a_i − 1) = 0, (L_U − L₀)a = E f, hence L_U a = 0 ⇒ L₀a = −E f.
2. **Reference comparison.** T₀R = 0, so T₀z = T₀a = a + R E f and dT₀z = f + dR E f. The uniform face lift's curl is the coarse curl on 9 fine plaquettes, so ‖dR‖ ≤ 3·4 = 12.
3. **Multiplier form.** With μ = g_e/|V|², the second variation of −μ·Im(V̄V(U)) is Σ w_i b_i (p_i a)², b_i = g_e Im(P_i/V). Expanding (p_i a)², the (t_e a)² term vanishes because Σ w_i b_i = 0, and the cross term becomes −2(A_e f)(F_e f) after substituting t_e a = −A_e f.
4. **Nonstationary validity.** In the neutral face-correction chart the coordinate is z + Rψ(z), whose second derivative lies in range R, and R*(∇S − DG*μ) = 0 by the pointwise choice of μ. So the chart's scalar Hessian equals the augmented form at every point of the chart, not only at a stationary point.
5. **Neutral and charged sectors decouple exactly** at an Abelian background: the global U(1) rotation about i fixes U, C and μ and acts on charged directions by rotation, so every invariant bilinear form has zero neutral–charged block.

Small remarks:
- The note's premise |g_e| ≤ 2 (D3C) is far from tight at these fixtures: the measured maximum is **0.600 at δ = 1/30 and 0.500 at δ = 1/36** (charged components exactly 0). The checker already computes g_e in integers and could require |ĝ_e| + 3240/S ≤ 1 directly, which would remove the dependence on D3C and shrink ε_b.
- The 13/30 bound on the ball is only 0.0006 under its threshold, because ε_b = 12000r enters multiplied by 64·5. That is fine for an existence statement but leaves no room for a larger radius.

## 3. Independent numerics

### 3a. Is the global floor at the D3F fixture really charged?

D3G-A implies that the neutral sector's relative floor exceeds 15/16, so the 0.6116 floor at δ = 1/30 must come from the charged sector. Review 12's matrix-free G-chart operator was restricted to each colour sector on the tiled fixture (4⁴ coarse torus, full Z space in that sector, random start).

| δ = 1/30, 4⁴ coarse torus | dimension | lowest two relative eigenvalues | eigen-residual | leakage into the other sector |
|---|---|---|---|---|
| neutral sector (colour i) | 61,440 | **0.9989962**, 0.9990625 | 4.2×10⁻⁹ | 0 (exact) |
| charged sector (colours j, k) | 122,880 | **0.6116457**, 0.6177763 | 9.9×10⁻⁹ | 0 (exact) |
| full space (review 13) | 184,320 | 0.6116457 | 6.8×10⁻⁹ | — |

**Reading.**
- The decoupling is exact in floating point: applying the full operator to a neutral vector returns a purely neutral vector, and likewise for charged vectors.
- The global floor 0.6116457 is the charged floor to all 7 digits. The neutral floor is 0.99900, far above D3G-A's certified 15/16 = 0.9375. So the certificate is correct but loose by about 0.06, which is the cost of the Schur-test norms.
- At this fixture, the multiplier and constraint corrections barely move the neutral sector. The neutral floor 0.99900 is close to cos θ_max = 0.99944.

### 3b. Non-Abelian staggered fields on the 4⁴ coarse torus

D3G-B's coarse data were rebuilt independently, without the author's arrays (which are outside the repository):
- direction 0, colour i, staggered along coarse axis 1 (the D3F pattern);
- two colours: plus direction 2, colour j, staggered along axis 1;
- three colours: plus direction 3, colour k, staggered along axis 0;
- equal amplitudes (η = 1).

U₀ = exp(s·A_v) with A_v the flat constrained minimiser of review 10, followed by constrained minimisation with B(U) = B(U₀) held fixed, rescaled until θ_max is just below 1/30. The fields are exactly period 2 in coarse units, so the 4⁴ spectrum contains the M = 2 spectrum (the subspace invariant under translations by 2, 11,520 coordinates, the same count as the author's).

| δ = 1/30 | two colours (this review) | two colours (D3G-B, M = 2) | three colours (this review) | three colours (D3G-B, M = 2) |
|---|---|---|---|---|
| θ_max | 0.0333177 | 0.0333165 | 0.0333311 | 0.0333164 |
| relative stationarity residual | 7.5×10⁻⁸ | 1.8×10⁻⁹ | 6.9×10⁻⁸ | 2.0×10⁻⁹ |
| largest coarse commutator ‖PQ − QP‖ | 0.0296025 | 0.0296003 | 0.0296249 | 0.0295790 |
| largest \|j\|, \|k\| link component | 0.0830, 0.0034 | — | 0.0830, 0.0831 | — |
| max ‖λ‖ | 0.601 | — | 0.604 | — |
| **Wilson-only, full 4⁴ space** | **0.5686617** (resid 6×10⁻¹²) | — | **0.5502065** (resid 6×10⁻⁸) | — |
| **augmented, full 4⁴ space** (184,320 coordinates) | **0.5733726** (resid 5.4×10⁻⁹, 155 matvecs) | — | **0.5659541** (resid 8.9×10⁻⁹, 210 matvecs) | — |
| augmented, period-2 subspace (= the M = 2 problem, 11,520 coordinates) | **0.5733726** (resid 6.9×10⁻⁹) | 0.5733843 | **0.5659541** (resid 1.3×10⁻⁸) | 0.5662407 |
| second eigenvalue, full / period-2 | 0.5775723 / 0.5820027 | — | 0.5681758 / 0.5698042 | — |

**Reading.**
1. **The fields match the author's.** Without access to the author's arrays, the independent construction lands on the same fields: θ_max agrees to 10⁻⁶ (two colours) and 1.5×10⁻⁵ (three colours), and the commutator invariant agrees to 2×10⁻⁶ and 5×10⁻⁵.
2. **Two colours: cross-implementation agreement.** The floors differ by 1.17×10⁻⁵. The slope of the D3F floors in θ (−9.25 per radian, from 0.6116 at θ = 0.033317 and 0.6630 at θ = 0.027765) predicts 1.165×10⁻⁵ from the θ difference alone. After that correction (which borrows the Abelian slope) the two operators agree on this non-Abelian field to about 5×10⁻⁸, on par with review 13's agreement on the Abelian fixture.
3. **On M = 4 the two-colour floor does not drop.** The full 4⁴ floor equals the period-2 floor to 9 digits. The lowest mode lives at momenta already present on M = 2; the new 4⁴ momenta only lower the second eigenvalue (0.5820 → 0.5776).
4. **Three colours: the same picture, with a small field difference.**
   - The full 4⁴ floor 0.5659541 again equals the period-2 floor (to 8 digits), so the 4⁴ momenta do not lower it either.
   - The difference from the author's 0.5662407 is 2.9×10⁻⁴. The θ offset explains 1.4×10⁻⁴ of it. The rest reflects a slightly different field, not the larger torus: the commutator invariant differs by 0.15%, against 0.04% for θ.
   - An exact cross-check needs one operator run on the other's array. The arrays `nonab2_Ustar.npy` and `nonab3_Ustar.npy` (12⁴ fine torus, review 12 conventions) are available for that.
5. **The multiplier term no longer rescues the floor.** The augmented floor exceeds the Wilson-only floor by only +0.0047 (two colours) and +0.0157 (three colours), compared with +0.40 on review 11's Abelian adversary. The non-Abelian staggered fields lower the Wilson part itself, and the multiplier does not compensate.

## 4. Remarks

1. **The neutral certificate is the easy half, and it is now done properly.** It covers 72 of 200 representatives, and §3a confirms numerically that none of the low spectrum lives there. Everything that determines the 1/2 margin is charged.
2. **The non-Abelian fixtures break the 200-sector reduction.** With non-commuting colours there is no residual U(1), so the charged/neutral splitting and the conjugate pairing disappear. What survives is translation symmetry: a period-2 field on M = 4 splits into 16 real Bloch sectors (the characters ±1 of the translation group Z₂⁴), each of 11,520 coordinates. A certificate for D3G-B's fields therefore needs 16 sector inertia computations of that size, or the full space.
3. **Uniformity remains the main risk.**
   - Each added non-commuting colour lowers the floor at δ = 1/30: 0.6116 (Abelian) → 0.5734 (two colours) → 0.5660 (three colours, 4⁴). The margin above 1/2 falls from 22% to 13%.
   - These are three points of a hand-picked staggered ansatz at η = 1, not the result of an adversarial search. A search over general non-Abelian coarse data, using review 11's κ-maximisation with non-commuting colour components, is the obvious next numerical test. It should come before investing in charged-sector certificates for the two Abelian fixtures alone, which are no longer the hardest known cases.
   - With a 13% margin, review 13's gluing table needs amplification at most 1.13 for offset-2 couplings, which means patches of R ≥ 5 (9 blocks per side) unless the patch-local floors sit well above the global one.
   - The δ = 1/36 values of the non-Abelian fields were not computed here.
4. **On the sound / light / X-ray channels.** The note's own disclaimer is the right one. The SU(2) colour index labels a direction in the Lie algebra su(2); it is not a physical frequency or polarisation, and a laboratory probe at any wavelength cannot certify an inequality between two quadratic forms on a lattice. The Cantor keys are useful as replay bookkeeping, nothing more, and nothing in the certificate depends on them.

## 5. Paste-ready comment for PR #138

> AI review (Claude), 27 Nov 2026. VOL14-D3G at `219a15c`: both receipts replay byte-identically under normal and `-O` Python and equal the seal; no-float `failed=0` (200 files); docs 0/0; hosted CI 15/15 workflows successful, including the new D3G workflow.
>
> D3G-A is correct. I rederived L₀a = −E f, ‖dT₀z‖ ≤ (1 + 12‖E‖)‖f‖ and the signed multiplier form Σ w_i b_i (r_i f)² − 2(A_e f)(F_e f), and checked that the integer folds are exact on the 4⁴ cover and that the rounding budgets hold with room to spare. Final value 0.94306 > 15/16. The §4 enclosure arithmetic and logic check (the 13/30 bound has only 6×10⁻⁴ slack). Suggestion: |g_e| is measured at 0.60 / 0.50, so the checker could test |ĝ_e| directly instead of relying on D3C's |g| ≤ 2.
>
> Numerics on the tiled fixture, sector by sector (review 12 operator, 4⁴): neutral floor 0.99900 and charged floor 0.6116457 at 1/30, with exactly zero leakage between sectors. So the global floor is entirely charged, as D3G-A implies.
>
> Non-Abelian fields rebuilt independently on M = 4 (your arrays are not in the repo): the θ_max and commutator invariants match yours to 10⁻⁶–10⁻⁵. Full-space augmented floors: two colours 0.5733726 (equal to its period-2/M = 2 value to 9 digits; yours 0.5733843, a difference accounted for by the θ offset), three colours 0.5659541 (its period-2 value is also 0.5659541; yours 0.5662407). Wilson-only floors: 0.5687 and 0.5502. The multiplier now adds only +0.005 to +0.016, and the margin above 1/2 is down to 13%. The two Abelian fixtures are no longer the hardest known cases, so a non-Abelian adversarial search should precede the charged Abelian certificates. Floating point, not certificates.

## 6. Reproduction

The scripts are stored in the project as `reviews/14-*.py` and use the review 09–13 modules.

| Script | What it does |
|---|---|
| `14-sector_check.py` | Neutral and charged sector solves at the tiled D3F fixture. |
| `14-nonab_m4.py` | Builds the two- and three-colour staggered witnesses on M = 4 and runs the full-space Wilson-only and augmented solves. |
| `14-nonab_eig.py` | Re-runs a solve at a saved witness: augmented on the full space (`full`) or on the period-2 (M = 2) subspace (`per`), or Wilson-only (`wil`). |
| `14-nonab_diag.py` | θ_max, link components and the coarse commutator invariant of the saved witnesses. |
| `14-results.json` | All numbers in §3, with the author's D3G-B values for comparison. |

Run times on 2 cores, two jobs at a time:
- sector check: about 1 hour;
- each witness build: about 20–25 minutes;
- each full-space augmented solve: 65–90 minutes;
- each period-2 solve: 45–60 minutes.

The build stops when the relative stationarity residual stalls below 10⁻⁷, because below that the action decrease is lost in floating-point rounding (S ≈ 9–14). The first build's scale is the flat prediction times 0.9979, since the uncorrected two-colour run overshot to θ_max = 0.0333881.

The witness arrays `nonab2_Ustar.npy` and `nonab3_Ustar.npy` (2.6 MB each) are kept in the review workspace and can be supplied for a cross-run of D3E's operator.
