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

**Reading:**
1. The nonlinear witness reproduces the flat-model curvature constant (16.27). The Wilson part alone therefore falls **below 1/2 at δ = 1/30**, and is 0.557 at δ = 1/36.
2. The multiplier term is large and positive exactly where the Wilson part is weakest. Its rms of 0.80 is far above the smooth witness's 0.51 at a larger θ, because high-frequency coarse fields need large multipliers.
3. The **full-space augmented minimum is not determined here.** The Ritz values only bound it from above, so D3E's full-space operator should be run on `adv_Ustar_30.npy` and `adv_Ustar_36.npy`.
   - If it stays above 1/2, the multiplier term is doing essential work, and the uniform argument must keep its sign, as D3D/D3E intend.
   - If it drops below 1/2, the fallback is δ = 1/36, where the Wilson part alone is already 0.557.

## 3. Comparison with the D3E pilot

D3E's transverse-staggered fixture gave a full-space augmented floor of 0.6116, with Wilson-only 0.6111, at δ = 1/30. There the multiplier term changed the floor by only 0.0006. On review 11's adversarial field the Wilson-only floor is lower (0.468) and the multiplier contribution on the low modes is three orders of magnitude larger. The two fixtures probe different regimes, so both belong in the D3 test set.

## 4. Limits

- One torus size (4⁴ coarse) and one adversarial field.
- The multiplier Hessian is from finite-difference polarization on a 6-dim subspace.
- The augmented values are Ritz upper bounds.
- Wilson-only eigen-residuals are at most 7×10⁻¹¹.

## 5. Reproduction

The package `review11-adversarial-fixture.zip` contains:
- the arrays `adv_v.npy`, `adv_Av.npy`, `adv_Ustar_30.npy` and `adv_Ustar_36.npy`;
- the JSON results;
- the generators `adv_fixture.py` and `build_adv_witness.py`;
- a README with every index and coordinate convention, and SHA256SUMS.

The generators depend on the review 07–10 modules in the project.
