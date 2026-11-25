# VOL14-D: scale-zero calibration, Bloch-fibre numerics, and review of VOL14-D1 (PR #125)

**Provenance:** written by Claude (AI) on 24 Nov 2026. This is AI verification, not human review. All floating-point numerics below are exploratory and are not certificates.

**State reviewed:**
- `main` at `6bb6873` (#124 merged).
- PR #125 at `4f1f9ec`. It is stacked on #122 (`e1a0ffe`) and #123 (`a9f3db2`), plus `32d8674` (VOL14-C calibration), `77c9907` (archived VOL14-C review), `5d5455c` (tolerance clarification) and `027f1c8` (sealed expectations).
- Read through anonymous git. PR metadata and hosted CI were not visible to this session.

## 1. Verdicts

| Item | Verdict |
|---|---|
| Scale-zero calibration (VOL14-C §4A) | **Correct.** All integer witnesses re-verified (§2). |
| My earlier statement that ε = 1/500 is "required" | **Wrong; withdrawn.** ε = 1/451 also works (§2). |
| Scalar Bloch floor reported earlier this evening | **Reproduced**, but it concerns a different, scalar operator (§3). |
| PR #125 replay | Receipt byte-identical, also under `-O`; equals the sealed expectations 6/6; no-float gate 189 files, 0 failures; docs integrity 98 files, 0/0. Merges cleanly with `main`. |
| VOL14-D1 constants (105, 2048, 22890, 255/256) | **Correct as bounds.** An independent Bloch reconstruction of the same operator confirms each, with margin (§4.2). |
| VOL14-D1 locality estimate | **Valid but quantitatively vacuous below about 10⁴ coarse spacings.** The measured decay is roughly 1,500× faster (§4.3). |

## 2. Scale-zero calibration

**Verified exactly:**
- 1 − cos(1/30) ≥ 10799/19440000 > 1/2000, so a nondefective plaquette at ε = 1/500 has angle below δ = 1/30.
- cos(15δ) = cos(1/2) ≥ 40439/46080 > 7/8.
- 6·1536·3²² < 2⁴⁹ (bit length 49) and ⌊9⁷/32000⌋ = 149, so ρ⋆ < 2⁻¹⁰⁰.
- 1536⁴·27·3⁸⁴ < 2¹⁸¹ (bit length 181) and ⌊9⁷/8000⌋ = 597, so ρ_D < 2⁻⁴¹⁶.
- 972 < 2¹⁰, so the local small-field failure probability is below 2⁻⁴⁰⁶.
- For k ≤ 6 the lower bound 9216·3^(3k − ⌈9ᵏ/32000⌉) exceeds 18⁻³, so 9⁷ is the first power of nine that passes the sufficient criterion.

**Reconciling two sets of numbers.** My previous reply quoted ln ρ_D ≈ −473 (about 2⁻⁶⁸³) and ln ρ⋆ ≈ −117 (about 2⁻¹⁶⁸) from the same VOL12 formulas. The certified values in the note are weaker because they use e^{3/4} < 3 and e^{−x} ≤ 2^{−⌊x⌋}, which gives up roughly a factor ln 2 in the exponent. Both are valid. The note's values are the certified ones, and the difference is slack in the safe direction.

**Correction.** I said ε = 1/500 was "required, not just conservative". That was wrong.
- The admissible tolerances are those with ε/4 ≤ 1 − cos(1/30), that is ε ≤ 0.00222202.
- 1/450 fails by about one part in 10⁴.
- 1/451 passes, with the same two-term witness: 19440000 < 10799·1804.
- So 1/451 is the largest admissible reciprocal integer, and 1/500 is a choice for round witnesses. At 1/451 the activity threshold is β ≈ 1.14×10⁶ instead of 1.27×10⁶, so 9⁷ is still the smallest power of nine.

**Scope.** The calibration covers the original measure at scale 0 only. The requirement to re-establish small-field and large-field estimates on the induced measure at every scale is now stated in VOL14-C §4A. Nothing further to add.

## 3. Scalar Bloch-fibre findings (earlier this evening)

**Operator.** A scalar field u on the fine lattice ℤ⁴, constrained so that its centred tent-weighted block mean vanishes at every coarse site. The weights are 1, 2, 3, 2, 1 along one axis times uniform b³ transversally, which is the μ-component of the VOL14-B average. Bloch decomposition over coarse momenta gives b⁴-dimensional fibres for the compressed Laplacian.

**Results** (reproduced tonight with the script in §7):

| b | λ_min | at k | 4 sin²(π/2b) | momenta scanned |
|---|---|---|---|---|
| 3 | 1.00000 | (0, 0, 0, π) | 1.00000 | 9⁴ grid + 2,000 random |
| 5 | 0.38197 | (0, π, 0, 0) | 0.38197 | 3⁴ grid only |

The preliminary bound λ_min ≥ 1/(32b²) = 1/288 at b = 3 holds, about 288× below the measured value.

**Limitations:**
1. **Different operator.** It is componentwise and scalar, uses the gradient ∇ rather than the curl d, has no gauge fixing and no d c̄ term. The D1 note is right not to transfer it.
2. **The formula 4 sin²(π/2b) is a fit to two values,** and the b = 5 value rests on 81 momenta.
3. **Grid search, not a certified minimum.** The minimizers sit at symmetric points, which makes a missed interior minimum less likely but does not exclude it.
4. **A pitfall for D2.** In Bloch form the constraint a·φ = 0 is bilinear, so the constrained space is the orthogonal complement of conj(a), not of a. Dropping the conjugate gives a wrong floor (0.683 at b = 3); I hit this when consolidating the script. The numbers above use the correct form.

## 4. Review of VOL14-D1 (PR #125, `4f1f9ec`)

### 4.1 Replay and the written argument

- **Replay.** The checker runs in 0.3 s and reproduces `YM4-VOL14D1-TREE-GAUGE-20261124.hbp` byte for byte, including under `-O`. Its rows equal the sealed expectation file. The expectations were sealed after local computation (`027f1c8` precedes `4f1f9ec`), and the note says so.
- **Gauge section.** Coordinate-ordered shortest paths are prefix-closed, so they form a tree with 80 edges. Residual gauge gradients preserving L A = 0 are constant on coarse centres, so the section is unique. Correct.
- **L R = I.** Connectors use only internal links, and each middle segment crosses only its own interface. Correct, and confirmed numerically.
- **‖L‖² ≤ 8·277/729 < 4.** Each fine link lies in at most eight two-block patches. Correct.
- **T.** A = z + RLz is an orthogonal decomposition, so ‖Tz‖² ≥ ‖z‖² and ‖T‖² ≤ 1 + 27·4 = 109. Correct.
- **Schur domination.** The absolute kernel of S is nonnegative and invariant under coarse translations, so its norm is attained at zero momentum. Folding to the finite matrix M is therefore valid, and the weighted Schur test is valid for the symmetric nonnegative MᵀM. Correct.
- **Chebyshev.** The normalized residual is bounded by 2q^{n+1}/(1 + q^{2n+2}) ≤ 2q^{n+1}, which gives the stated (2/a)q^{n+1}. 215040 < 511² gives q < 255/256. Correct.
- **Covariance.** The gauge section and T have constant Jacobians, so C = T H⁻¹ T* for the quadratic action. This holds at the identity background only, as the note says.

I found no gaps in the construction. One bound can be sharpened (§4.2): H has coarse ℓ¹ range 2, not 4.

### 4.2 Independent Bloch reconstruction of the D1 operator

I rebuilt the operator from the written definitions (VOL14-C map, coordinate-ordered tree, the space Z, T = I − RL) without importing repository code.
- **Construction checks:** 459 nonzeros per L row, squared norm 277/729, ℓ¹ norm 205/27, 80 tree links, dim Z = 240, LR = I, L dφ = d_coarse φ, and dd = 0.
- **Scan:** a 6⁴ grid of coarse momenta, 500 random momenta and the symmetric points, with local refinement around each extremum.

| Quantity | D1 bound | Measured | Slack |
|---|---|---|---|
| sup ‖A‖²/‖dA‖² on the constrained tree-gauge slice | ≤ 105 | 36.5 (minimum ratio 0.02738 at k = (0, π, π, π)) | 2.9× |
| λ_min(H) on Z | ≥ 1/105 = 0.00952 | 0.03264 at (π, π, π, π) | 3.4× |
| λ_max(H) | ≤ 2048 | 16.23 at (0, π, π, π) | 126× |
| max ‖T(k)‖² | ≤ 109 | 7.30 | 15× |
| Condition number | 215,040 | 497 | 430× |
| Coarse ℓ¹ range of H | ≤ 4 | exactly 2 (33 offset blocks, every \|X_j\| ≤ 1) | — |

**Why the range is 2.** A plaquette of type (μ, ν) reaches only blocks 0, e_μ, e_ν and e_μ + e_ν through d and T. Differences of those offsets have ℓ¹ norm at most 2.

### 4.3 Decay: the bound against measurement

**Real-space covariance** on an 8⁴ coarse torus (finite volume; r = 4 is the antipodal point):

| Coarse offset X | ‖C₀ₓ‖ | | Coarse offset X | ‖C₀ₓ‖ |
|---|---|---|---|---|
| (0,0,0,0) | 17.4 | | (0,0,0,1) | 5.07 |
| (1,0,0,0) | 6.56 | | (0,0,0,2) | 0.0381 |
| (2,0,0,0) | 0.0999 | | (0,0,0,3) | 0.00553 |
| (3,0,0,0) | 0.0207 | | (0,0,0,4) | 0.00164 |
| (4,0,0,0) | 0.00722 | | (1,1,1,1) | 0.0168 |
| (1,1,0,0) | 0.397 | | (2,2,2,2) | 2.1×10⁻⁵ |

The D1 bound is 22,890 for r ≤ 2 and about 22,800 for r = 3 to 6. At r = 3 it exceeds the measured value by about 10⁶.

**Complex strip.** Minimum over a 6⁴ real grid of σ_min of the analytically continued symbol H(k + iη e₁):

| η | 0.25 | 0.5 | 0.75 | 1.0 | 1.25 |
|---|---|---|---|---|---|
| min σ_min | 0.0325 | 0.0321 | 0.0312 | 0.0293 | 0.0251 |

The first near-singularities appear near η ≈ 1.51–1.52: along e₁ at real parts (π, 0, 0, 0) and (π, π, π, π), and along e₄ at (0, 0, 0, π). The real-space ratio between r = 2 and r = 3 along e₁ is 4.83, and ln 4.83 ≈ 1.57, which is consistent.

So the measured decay rate is about **1.5 per coarse step**, an e-folding length of about 0.66 coarse or 2 fine spacings. The D1 rate is ln(256/255)/4 ≈ 0.00098 per coarse step, an e-folding length of about 1,022 coarse spacings, and the bound drops below 1 only at r ≈ 10,260.

**How far generic methods can go,** each evaluated with the measured sharp constants:

| Route | Rate per coarse step |
|---|---|
| D1 as written (condition number 215,040, range 4) | 0.00098 |
| The same Chebyshev argument with condition number 497 and range 2 | ≈ 0.045 |
| Combes–Thomas with the exact offset blocks and λ_min = 0.0326 | ≈ 0.002 (along an axis) |
| Complex strip (numerical) | ≈ 1.5 |

Sharpening the constants alone gains at most about 45×. The remaining factor of about 30 needs a method that uses the structure of the operator.

### 4.4 An open question for the multiscale plan

A Bałaban-style polymer expansion needs propagator decay per block to beat combinatorial entropy. For scale: the animal count VOL10 uses for link sets grows by a factor of about 324 per added element (entropy ≈ 5.8), while the measured decay per coarse step at b = 3 is about 1.5. Bałaban takes the block side large, which is one way to make decay dominate. Whether b = 3 can stay fixed depends on how the expansion is organised. I have not analysed this; it belongs in the multiscale plan.

## 5. Paste-ready comment for PR #125

> AI review (Claude), 24 Nov 2026. VOL14-D1 at `4f1f9ec`: the checker replays byte-identically (also under `-O`) and equals the sealed expectations 6/6; no-float gate 189/0; docs integrity 98/0/0; the branch merges cleanly with `main`. The written argument checks: the gauge section, LR = I, ‖L‖² ≤ 8·277/729, the orthogonal T decomposition, Schur domination at zero momentum, and the Chebyshev residual.
>
> An independent floating-point Bloch reconstruction of the same operator (no repository code) gives sup ‖A‖²/‖dA‖² ≈ 36.5 (bound 105), λ_min(H) ≈ 0.0326 (bound 1/105), λ_max(H) ≈ 16.2 (bound 2048) and max ‖T‖² ≈ 7.3 (bound 109). All bounds hold.
>
> Suggested edits:
> (1) H has coarse ℓ¹ range 2, not 4: a (μ, ν) plaquette row reaches only blocks 0, e_μ, e_ν and e_μ + e_ν. Then T p_n(H) T* has range 2n + 2, and the exponent improves to ⌊(r − 1)/2⌋.
> (2) State beside the estimate that the bound exceeds 1 until r ≈ 10⁴ coarse spacings, so it is a qualitative volume-uniformity statement.
> (3) Numerically the true decay is about e^{−1.5r} in coarse units: the first complex singularity of the symbol is near Im k ≈ 1.51, and the real-space ratio from r = 2 to r = 3 on an 8⁴ torus is 4.8. Floating point, not a certificate.

## 6. Recommendations for VOL14-D2

1. **Freeze the numerical targets above as predictions:** λ_min(H) ≈ 0.0326, λ_max(H) ≈ 16.2, condition number ≈ 500, strip width ≈ 1.5.
2. **Correction to my earlier suggestion.** I proposed certifying the strip with interval arithmetic on a grid plus a Lipschitz bound in k. As stated, that is not feasible: ‖∂H/∂k_j‖ ≈ 4.4 on real momenta, so certifying λ_min ≥ 0.016 to first order needs a spacing of about 2×10⁻³ per coordinate, roughly 10¹⁴ fibres in four dimensions. Realistic versions are:
   - adaptive branch-and-bound with interval arithmetic and second-order bounds, refined only near the few minimizing corners;
   - a sum-of-squares certificate for the matrix trigonometric polynomial H(k) − cI ⪰ 0 (a finite semidefinite program, rounded to rationals), for the real-axis floor.
3. **Plan for nonflat backgrounds now.** Bloch fibres need translation invariance and will not survive a nonflat small-field background. Bałaban's random-walk expansion builds the propagator from local Dirichlet inverses on overlapping cubes (CMP 95 and 96, 1984). It needs only finitely many local problems, which suits exact certification, and it extends to small-field backgrounds by perturbation. A reasonable split: compute the strip numerically as the target, and build the certificate locally.
4. **Cheap improvements to D1:** use range 2, and replace ‖T‖² ≤ 109 and λ_max ≤ 2048 with sharper certified values.
5. **Bloch pitfall:** take the complex conjugate when forming the complement of a bilinear constraint (§3, item 4).

## 7. Reproduction

The script is stored beside this review as `reviews/07-vol14d_bloch_crosscheck.py` (numpy only). Each subcommand runs the construction checks first.

| Subcommand | What it produces | Time (2 cores) |
|---|---|---|
| `floor 6` | the §4.2 extremes | about 90 s |
| `strip 6 0 0.25,0.5,0.75,1.0,1.25` | the §4.3 strip table | about 50 s per η |
| `line` | the first singularities near η ≈ 1.51 | a few minutes |
| `real 8` | the real-space table | about 2.5 min |
| `ct` | range of H and the Combes–Thomas rate | under 1 min |
| `scalar 3 9`, `scalar 5 3` | the §3 scalar floors (grid only; the original b = 3 scan added 2,000 random momenta) | a few minutes |

The local refinement in §4.2 used random perturbations from the grid extremes and moved none of them.

Not done: certified versions of any §4 numbers, the b = 4 tail from doc 05, and any check of PR #125's hosted CI.
