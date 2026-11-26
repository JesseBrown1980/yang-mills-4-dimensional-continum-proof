# VOL14-D3C review: paired face cancellation, the stationary curvature source, and a D3D preview

**Provenance:** written by Claude (AI) on 26 Nov 2026. This is AI verification, not human review. All floating-point numerics are exploratory; **none is a certificate.**

**State reviewed:**
- PR #131 at `530368b`, with its seal in `b64cfe6`, stacked on #130 at `087f592`.
- Hosted CI, read through the REST API: #130 at `087f592` shows 12 of 12 check runs successful; #131 at `530368b` shows 16 of 16.

## 1. Verdicts

| Item | Verdict |
|---|---|
| Replay | Receipt byte-identical, also under `-O`. It matches the seal except for the δ = 1/22 row, which was added after sealing and is disclosed in the note. No-float gate 193 files, 0 failures; docs integrity 108 files, 0/0. |
| Paired face counts | **Independently reproduced in closed form:** n_V = #{a > ν : x_a ≠ 0}. Summing over the face gives 36, 54, 72, 90 for μ = 0…3; there are 54 two-link and 54 one-link plaquettes, and 2·54 + 54 = 27·6. |
| Face gradient bound 54δ + 180δ² | **Correct.** In target-tree gauge the lifted variation is Y at every face link, so a two-link plaquette has tangent Y − Ad(V)Y of norm at most 2n_Vδ‖Y‖, and the first variation is at most sin θ_p times the tangent norm. |
| Multiplier 630/251 | **Correct**, a 27/10 improvement on D3B. |
| δ = 1/22 extension | **Arithmetic correct:** 743/968, 704/2229, 2229/1525, 342/121, and the product is below 9/2. The swap counts are δ-independent and the cos floor is valid at 15/22 < π/2. |
| Stationarity identity | **Correct and exact:** ∇S = d_U*n with n_p = Im P_p, so K_U*n = T_U*L_U*λ = 0. Numerically at the witness: ∇S = d_U*n to 2×10⁻¹⁵, and ‖K_U*n‖/‖∇S‖ = 2.9×10⁻¹⁰. |
| Flat stationary reference A_v, n_v | **Correct:** L A_v = v to 5×10⁻¹⁶, K₀*n_v = 0 to 4×10⁻¹⁴, and N and Nᵀ are adjoint to 1×10⁻¹⁴. |
| D3D preview | On D3C's flat stationary subspace the reference constant is about 7.5 for generic coarse fields but **≥ 16.2 for an adversarial coarse field**, against 15 needed at δ = 1/30. This is down from ≥ 48 (free) and ≥ 28 (Bianchi), but not closed alone (§3, §4). |
| Correction to review 10 | Accepted. Review 10 evaluated the D3A constant 315/251 at θ = 0.0438, outside its domain δ ≤ 1/30. The witness is covered by D3C's 1/22 extension instead, which bounds ‖λ‖ below 9/2. |

## 2. The face gradient at real backgrounds

The transported face gradient (R_U*∇S)_e, computed with the D3A lift Ad(s₀(v)):

| Background | θ_max | max over faces | rms | D3C bound 54θ + 180θ² | D3B bound 162θ |
|---|---|---|---|---|---|
| Stationary witness | 0.0438 | 0.933 | 0.510 | 2.71 (2.9× slack) | 7.10 |
| Smooth, not stationary | 0.0297 | 0.589 | 0.325 | 1.76 (3.0× slack) | 4.81 |

At the witness, max‖λ_e‖ = 0.933 agrees with the face-gradient maximum, as expected since L_U R_U ≈ I. Against D3C's certified 1/22 constants (below 9/2, product 4.13) the slack is 4.4×.

## 3. D3D preview: the reference model on the stationary subspace

**Model.** The D3B reference form C_ref with flat transports, restricted to D3C's flat stationary curvature n_v = dA_v and normalized to max_p |n_p| = 1. As in review 10, κ = sup_A C_ref(A)/‖dA‖² on a 4⁴ coarse torus. Alternating maximization over the coarse data v (choose A, then v ← Nᵀw, n ← Nv / max) gives lower bounds on sup κ over this subspace.

| Start | κ (start → iterates) | best |
|---|---|---|
| Random v | 6.24 → 7.46, 7.21, 7.16, 7.13, 7.09, 7.11 | **7.46** |
| Witness coarse field, log B(U*) | 6.41 → 6.98, 7.26, 7.48, 7.43, 7.39, 7.36 | **7.48** |
| Staggered coarse field in one direction | 13.79 → 13.36, 13.34, 13.34, 13.33, 13.27, 12.68 | 13.79 |
| Free-coefficient worst case (κ ≥ 48) projected onto the subspace, v = Nᵀn_stag | 11.81 → **16.27**, 16.23, 16.23, 16.23, 16.23, 16.23 | **16.27** (converged) |

For comparison, from review 10 on the same model:

| Curvature class | κ |
|---|---|
| Free coefficients, adversarial | ≥ 48 |
| Bianchi-compatible, adversarial | ≥ 28 |
| Nonabelian stationary witness | 6.3 |
| **Flat stationary subspace, adversarial (this review)** | **≥ 16.2** |
| Gate: 1/2 budget at δ = 1/30 | ≤ 15 |

**Reading.**
- Generic (random) and witness-like coarse fields give about 7.5, half the gate value.
- Adversarial coarse fields push the stationary-subspace constant to **at least 16.2, just above the gate of 15**. They are high coarse-frequency fields, still admissible under the fine plaquette tolerance.
- So stationarity reduces the adversarial constant about 3× (48 → 16), but in this flat reference model it does **not** by itself close the 1/2 budget at δ = 1/30, where 16.2/30 ≈ 0.54. That is a lower bound; the true supremum could be higher.

**A structural note for D3D.** The stationary subspace is parametrized by coarse link data v, which is 3 real dimensions per coarse link per colour, minus coarse gauge: a staggered v in every direction is a coarse gradient and gives n_v = 0 identically. The random-start maximizers drive rms|n|/max|n| down to about 0.03, concentrating curvature at a few plaquettes, while the adversarial ones keep it near 0.2. A certificate can therefore work with a block-local family of v and the explicit flat solution operator, which is a finite computation per coarse neighbourhood, provided n_v decays away from the support of v (it inherits the decay of H₀⁻¹).

## 4. Consequences

1. **The gap at δ = 1/30 is now small but real.** The flat stationary-subspace worst case found is at least 16.2, against 15 needed. Three levers, not mutually exclusive:
   - **Keep the multiplier Hessian in the test.** At the review 10 witness the term −λ·D²F_c was positive on the low modes, raising the relative floor from 0.84 to 0.91. Adversarial coarse fields carry larger multipliers, so the signed augmented form, not the curvature term alone, should be optimized over the stationary subspace.
   - **Tighten the D3 background tolerance.** Under the VOL12 plan formula, β = 9⁷ keeps ρ⋆ ≤ 18⁻³ down to δ ≈ 1/60. At δ = 1/36, ε may be up to 1/648 and ln ρ⋆ ≈ −82, while the numerical reference term is 16.23/36 ≈ 0.45. This needs the integer VOL12 certificate rerun at the new ε, and the D3A and D3C constants only improve at smaller δ.
   - **A tighter estimator alone cannot close it.** No certificate on this subspace can beat the true supremum, which is at least 16.2, so one of the two levers above is needed at δ = 1/30.
2. **The background tolerance must be stated for the minimizer.** Constrained minimization raised θ_max from 0.030 at the start to 0.044 at the witness. The D3 small-field hypothesis concerns the background minimizer, so its relation to the scale-zero small-field event (VOL12/VOL14-C calibration) needs an explicit estimate.
3. **Certificate structure for D3D:**
   - write n_v = N v with N = d(I − T H₀⁻¹ Tᵀdᵀd)J;
   - bound sup_v κ(Nv/‖Nv‖_∞) through block-local v and the decay of H₀⁻¹;
   - this keeps the signed pairs and the max-norm constraint, as the D3C note asks.
4. **Then the nonlinear step:** the deviation of the true n_p = Im P_p from the flat n_v at U*, controlled through d_U*n = L_U*λ and D3C's multiplier bound, plus the full augmented Hessian W_U − λD²F_c in a fixed common section.
5. **Calibration:** the witness's θ_max of 0.0438 lies outside δ = 1/30, so future witnesses should be built at the chosen δ, or analyzed with the 1/22 constants.
6. **Next numerical step:** nonlinear stationary witnesses built from the adversarial coarse field (the projected free optimum), with the full augmented low-mode floor measured. This tests whether the multiplier term compensates where the curvature term is worst.

## 5. Limits

- The κ values are lower bounds from heuristic alternation on one torus size, using the flat abelian model.
- The face-gradient numbers come from two backgrounds.
- The low-mode results of review 10 are unchanged and remain Ritz upper bounds.

## 6. Paste-ready comment for PR #131

> AI review (Claude), 26 Nov 2026, at `530368b`: the receipt replays byte-identically (also under `-O`). It matches the seal except for the disclosed δ = 1/22 row. No-float 193/0; docs 108/0/0; hosted CI 16/16.
>
> The paired-face counts are reproduced in closed form, n_V = #{a > ν : x_a ≠ 0}, giving 36/54/72/90 with 54 + 54 plaquettes. The bound 54δ + 180δ², the multiplier 630/251, the 1/22 extension arithmetic and the identity K_U*n = 0 are all correct. Numerically ∇S = d_U*n to 2e-15, and K_U*n vanishes to 3e-10 at the stationary witness.
>
> Transported face gradient at the witness: 0.933 against a bound of 2.71 at its θ. On a non-stationary smooth background: 0.589 against 1.76.
>
> D3D preview: on the flat stationary subspace n_v = dA_v, alternating maximization of the D3B reference constant reaches about 7.5 from random and witness starts, but **≥ 16.2** from an adversarial coarse field, against 15 needed at δ = 1/30. Free coefficients gave ≥ 48 and Bianchi-compatible ≥ 28. Stationarity therefore cuts the gap about 3× but does not close it alone. Options: optimize the signed augmented form, including the multiplier Hessian, over the subspace; or tighten the D3 tolerance (β = 9⁷ appears to allow δ down to about 1/60 under the VOL12 criterion). Floating point, not certificates.

## 7. Reproduction

The scripts are stored in the project as `reviews/11-*.py` and use the review 09 and 10 modules.

| Script | What it produces |
|---|---|
| `d3c_check.py` | §2 and the identity checks; needs `Ustar_0.03.npy` from `10-stat.py`. |
| `d3d_preview.py` | §3. Run without arguments for the random and witness starts, or with `extra` for the adversarial starts. |
