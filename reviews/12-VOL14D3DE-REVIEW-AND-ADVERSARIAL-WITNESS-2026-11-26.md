# VOL14-D3D/D3E review and review 11's adversarial field as a nonlinear stationary witness

**Provenance:** written by Claude (AI) on 26 Nov 2026. This is AI verification, not human review. Floating-point numerics are exploratory; **none is a certificate.**

**State reviewed:**
- PR #133 at `a371066` (seal `dcc6aab`).
- PR #134 at `a299a87` (seal `e60840b`).
- Hosted CI through the REST API: #133 shows 18 of 18 check runs successful, #134 shows 16 of 16.

## 1. Verdicts

| Item | Verdict |
|---|---|
| Replays | D3D and D3E receipts are byte-identical, also under `-O`. The D3E checker's SHA-256 `9c861d32…` matches the D3E source inventory. No-float gate 195 files, 0 failures; docs integrity 113 files, 0/0. |
| D3D calibration at 1/36 and 1/58 | **Correct.** 1 − cos(1/36) ≥ 15551/40310784 > 1/2800. The floors 106/427 and 43/175 hold, and so do 2⁴⁹·18³·10⁴³ < 27⁴³ and 2²⁵⁰·10¹⁷⁵ < 27¹⁷⁵. As the note says, these calibrate the input measure only. |
| D3D face-orbit chart | **Correct.** P_i(q) = P_i s_i⁻¹s₀qs₀⁻¹s_i; ‖M_e‖ ≤ 1; ‖M_e − Left(V_e)‖ ≤ 16δ/3; σ_min ≥ 251/360 at 1/30. At 1/36 the chain 263/288 → 661/864 → 128/789 → 789/661 holds, with 59/36 and λ ≤ 15517/7932. Repair: 1/36 + 4·(864/661)/1000 < 1/30. |
| D3D second jet | Structure correct: at stationarity the feasible-curve second derivative equals the augmented Hessian. Only the synthetic fixture is checked by the integer verifier, as stated. |
| D3D canonical lift | **Correct and useful:** S(U_lift) = 9·S_coarse(C), because only block-corner plaquettes carry curvature, 9 per coarse plaquette. The note correctly says the bound is extensive and does not settle minimizer regularity. |
| D3E G-chart | **Correct.** DG = diag(r)DF at U, and D²G = diag(r)D²F on the tangent space, so H_aug = T*(D²S − μ·D²G)T with μ = λ/r. |
| D3E prefix DAG | **Correct:** last-letter recurrence; counts 216, 2216 and 17728 = 4·2·2216. |
| D3E pilot | Plausible and internally consistent. It is a different fixture from review 11's, which the note says. |

## 2. Review 11's adversarial field as a nonlinear witness

**Fixture.** Delivered as `review11-adversarial-fixture.zip`, with a README and SHA256SUMS.
- The flat adversarial coarse data were regenerated exactly: κ history 11.806, **16.267**, 16.231, …
- A_v is the flat constrained minimizer, so U₀ = exp(scale·A_v) is nearly stationary.
- Constrained minimization converged in one round at the target scale.
- Tree links are exactly the identity, so the fields are in block-tree gauge and D3A's transported lift equals the constant lift.

| | δ = 1/30 | δ = 1/36 |
|---|---|---|
| θ_max of the stationary field | 0.033335 | 0.027779 |
| stationarity residual / constraint error | 2.6×10⁻¹² / 7×10⁻¹⁸ | 7.1×10⁻¹⁰ / 5×10⁻¹⁸ |
| ‖λ‖ max / rms | 0.907 / 0.804 | 0.755 / 0.670 |
| κ for the actual nonlinear curvature | 16.268 | 16.268 |
| **Wilson-only, full space: lowest eigenvalue of H₀^(−1/2)H_U H₀^(−1/2)** | **0.4685** | 0.5566 |
| −λ·D²F_c on the 6 lowest Wilson-only modes | +0.372 … +0.469 | +0.310 … +0.390 |
| augmented Ritz values on that subspace (upper bounds) | 0.9366 | 0.9465 |
| **augmented, full space (independent G-chart operator)** | **0.8714** (residual 1.7×10⁻⁷, 99 matvecs) | **0.8920** (residual 2.5×10⁻⁷, 86 matvecs) |
| Wilson part / multiplier part at the augmented minimizer | 0.830 / +0.041 | 0.858 / +0.034 |

**Reading:**
1. The nonlinear witness reproduces the flat-model curvature constant (16.27). The Wilson part alone therefore falls **below 1/2 at δ = 1/30**, and is 0.557 at δ = 1/36.
2. The multiplier term is large and positive exactly where the Wilson part is weakest. Its rms of 0.80 is far above the smooth witness's 0.51 at a larger θ, because high-frequency coarse fields need large multipliers.
3. **The full-space augmented minimum is 0.871 at δ = 1/30 and 0.892 at δ = 1/36,** well above 1/2. These come from an independent matrix-free operator in D3E's G-chart, with random start vectors and no subspace restriction (§2a). The minimizing direction is *not* a low Wilson mode: there the Wilson part is 0.83 and the multiplier adds about +0.04. The Wilson-low modes (0.468) are lifted by +0.37 or more.
4. The flat-curvature adversary of review 11 is therefore **not adversarial for the complete form.** The multiplier term comes from the same coarse field and largely cancels the curvature term where that term is worst, so a certificate has to treat the curvature and multiplier terms jointly.

## 2a. The independent full-space operator

- **Chart.** J = S − Σ_e μ_e·Im(C̄_e V_e(U)), with C = B(U*) and μ_e = λ_e/|V_e(U*)|, as in D3E §2.
- **Gradient.** The right-trivialized gradient of the multiplier term is contracted on the fly: an insertion (prefix pf, suffix sf, sign σ, weight w) contributes σ·w·Im(sf·μ·C̄·pf).
- **Matvec.** At a stationary U*, H_aug v = d/dt g_J(U* e^{tv}) exactly, because the exponential-chart correction multiplies ∇J = 0. It is evaluated by central differences with step 10⁻⁴/max|v|.
- **Checks at the 1/30 witness:**
  - G-chart stationarity ‖∇S − DGᵀμ‖/‖∇S‖ = 2.6×10⁻¹², equal to the F-chart residual;
  - the normalized means equal the VOL14-C map exactly;
  - the multiplier gradient matches a finite difference to 4×10⁻¹⁰;
  - aᵀH_aug a matches an independent second difference of the scalar μ·G to 2×10⁻⁹.
- **Solver.** ARPACK on the whitened operator H₀^(−1/2)T*H_aug T H₀^(−1/2), over all 184,320 Z coordinates.

## 3. Comparison with the D3E pilot

| Fixture at δ = 1/30 | Wilson-only floor | Augmented floor | Multiplier effect on the floor |
|---|---|---|---|
| D3E transverse-staggered | 0.6111 | **0.6116** | +0.0006 |
| Review 11 adversarial (this review) | 0.468 | **0.871** | +0.40 |

The two fixtures probe different weak directions. D3E's staggered field is currently the *lower* augmented floor and should be treated as the harder known case. Both belong in the D3 test set, together with the cross-implementation check below.

**Cross-implementation request.** Run D3E's operator on `adv_Ustar_30.npy` and `adv_Ustar_36.npy`, and run this review's operator (`12-aug.py`, `12-aug_eig.py`) on D3E's fixtures. Agreement on both pairs would validate the two implementations against each other.

## 4. Limits

- One torus size (4⁴ coarse) and one adversarial field.
- The full-space augmented minimum uses a central-difference matvec (validated to 2×10⁻⁹) and ARPACK with a random start; it is numerical evidence, not a certified minimum.
- Wilson-only eigen-residuals are at most 7×10⁻¹¹; augmented ones at most 9×10⁻⁷.

## 5. On using conditional decomposition for D3F

The Matrix Laws idea of conditioning on coupled boundary coordinates maps naturally onto the certificate problem, with three adjustments:
- **Ordering.** Its analogue is the elimination order in an exact LDLᵀ / Schur-complement certificate of H_aug − cH₀. Keeping each plaquette's links, and each face's crossing links with their multiplier, adjacent controls fill-in.
- **The constraint couples interiors.** In the Z coordinates the correction R L z sits on face links but depends on block interiors, so conditioning on face values does *not* decouple neighbouring interiors. The saddle-point (KKT) form [H_aug, Lᵀ; L, 0] keeps the coupling local per coarse link, which is the right object for interface Schur complements.
- **Uniformity, not size, is the hard part.** A per-background certificate is a finite computation. A uniform one needs a local positive decomposition H_aug − cH₀ = Σ_P Q_P with each Q_P ⪰ 0 for every admissible background patch. Gauge covariance gives exact equivalences between patches (local matrices at gauge-equivalent backgrounds are Ad-conjugate). Normalizing each patch to a local tree gauge before caching is the genuine analogue of the joint-shadow normalization. Whether such a decomposition exists at c = 1/2 is the main open risk. §2 shows it must keep the curvature and multiplier terms in the same local pieces.

## 6. Reproduction

The full-space cross-check scripts are `12-aug.py` (operator) and `12-aug_eig.py` (eigen-solve), in the project. Each solve takes about 30–35 minutes on 2 cores.

The package `review11-adversarial-fixture.zip` contains:
- the arrays `adv_v.npy`, `adv_Av.npy`, `adv_Ustar_30.npy` and `adv_Ustar_36.npy`;
- the JSON results;
- the generators `adv_fixture.py` and `build_adv_witness.py`;
- a README with every index and coordinate convention, and SHA256SUMS.

The generators depend on the review 07–10 modules in the project.
