# VOL14-D3A/D3B review: covariant face lift, signed curvature ceiling, and a constrained-stationary witness

**Provenance:** written by Claude (AI) on 26 Nov 2026. This is AI verification, not human review. All floating-point numerics are exploratory; **none is a certificate.**

**State reviewed:**
- PR #128 at `5d98eff`, with D3A expectations sealed in `6f82da1`.
- PR #129 at `1b482ef`, with D3B expectations sealed in `8f061dc`.
- `main` at `6bb6873`.
- Read through anonymous git. Hosted CI was not visible to this session.

## 1. Verdicts

| Item | Verdict |
|---|---|
| Replays | D3A, D3B, D2 and D1 receipts are all byte-identical, also under `-O`. No-float gate 192 files, 0 failures; docs integrity 105 files, 0/0. PR #129 merges cleanly with `main`. |
| D3A suffix counts | **An independent enumeration matches exactly:** maximum swaps 9, 8, 7, 6 and weighted means 8/3, 20/9, 16/9, 4/3, with every swapped word ending at the canonical inverse tree word. |
| D3A argument | **Correct.** The transported face mean is gauge covariant; δP = P·Ad(s⁻¹s₀)Y; ‖L_U R_U − I‖ ≤ 64/315 at δ = 1/30; ‖T_U z‖ ≥ ‖z‖; the plaquette Hessian form and the signed-area identity hold; β₀ ≤ 23/44. It also repairs the covariance defect of the fixed Z used in review 09. |
| D3B Ward identity | **Correct**, and **confirmed numerically** at a constrained-stationary witness (§4): the multiplier term cancels the Wilson Hessian's gauge-direction leakage down to finite-difference noise. |
| D3B multiplier bound 1701/251 | **Correct, but about 10× loose:** at the witness, max‖λ_e‖ = 0.93, while the bound evaluated at its θ_max is 8.9. |
| D3B reference ceiling 658 | **Correct as a sufficient bound, about 14× above the worst case found.** More importantly, **the exact worst case of this reference model is at least 48**, and at least 28 even under the Bianchi identity, while the δ = 1/30 gate needs 15 (§3). Closing the gate requires stationarity, not a sharper envelope. |
| D3B seal | Minor: the sealed expectation omits the `multiplier_norm_le=1701/251` field that the receipt emits, so that value isn't covered by the seal. |
| Review 09 correction | Review 09's H_U omitted the multiplier term, as D3A §4 says. At the witness this term is **positive** on the low modes and raises the relative floor from 0.84 to 0.91 (§4). |

## 2. Remarks on D3A and D3B

- **Using section freedom.** The Ward identity makes the *background* augmented form invariant under root-zero gauge directions. The *comparison* form H₀∘ι, with ι the identification by parallel transport, is not exactly invariant under background gauge directions, because ι(G_U φ) is not a flat gauge direction. So the choice of section still enters the relative constant. Choose the section, for example the internal minimum-norm one, so that ι maps background gauge directions as close to flat ones as possible, and state the comparison in that section.
- **Multiplier.** λ = J_Uᵀ∇S is exact at stationarity because L_U J_U = I, so any right inverse gives the same λ. The face sum Σ₂₇ Ad(s₀)ᵀ∇S_ℓ cancels heavily in practice: the rms ‖λ_e‖ is 0.51 at θ_max = 0.044, about 12·θ, against 203·θ for the triangle-inequality bound.

## 3. How far the D3B reference model can go

**The quantity.** κ(n) = sup_A C_ref(A)/‖dA‖² for |n_p| ≤ 1, with A on the flat constrained tree-gauge slice. D3B certifies κ ≤ 658 for all n. I computed κ for structured n, and lower bounds on the supremum by alternating maximization: choose the top eigenvector A, then set n_p = w_p/|w_p|. Here w_p = Σ_{i<j} a_i × a_j, and the sanity check xᵀMx = C_ref holds to 9×10⁻¹³. The relative form uses the exact flat H₀^{−1/2}, applied by FFT on a 4⁴ coarse torus.

| Curvature coefficients n_p | κ found | Comment |
|---|---|---|
| D3B certificate (all n) | ≤ 658 | |
| Arbitrary, alternating from a staggered pattern | **48.1** (converged) | lower bound on sup_n κ |
| Arbitrary, alternating from random | 42.3 (still rising) | |
| Arbitrary, alternating from coherent | 29.6 (converged) | |
| Constant direction for every plaquette | 10.0 | before alternation |
| Bianchi-compatible: n = dB (abelianized), normalized to max\|n_p\| = 1 | **28.2** (best iterate) | lower bound for the constrained sup |
| Bianchi-compatible, from random curl | 7.6–8.3 | |
| **Constrained-stationary witness**, n_p = Im U_p / max\|Im U_p\| | **6.3** (both signs) | §4 |
| Needed for the 1/2 budget at δ = 1/30 | ≤ 15 | |

**Consequences:**
1. **No estimator that treats n_p as free coefficients bounded by δ can close the δ = 1/30 gate.** The exact supremum is at least 48, so this route needs δ ≤ 1/96.
2. **Adding the abelianized Bianchi identity is not enough either.** The supremum stays at or above 28, so δ ≤ 1/56 would be needed.
3. **Stationarity is the correlation that matters.** For the actual stationary background κ = 6.3, so the reference curvature term is about 0.21 at δ = 1/30, well inside the budget.

## 4. A constrained-stationary witness

**Construction.**
- Start from the smooth background of review 09 (ε = 0.03) on the 12⁴ fine torus, and fix V = B(U₀).
- Minimize S subject to B(U) = V. Each step is a preconditioned constrained descent, d = −T_U P H₀⁻¹ (T_U P)ᵀ∇S, using the exact flat inverse by FFT. After each step, B(U) = V is restored by Newton steps through R_U(L_U R_U)⁻¹.
- The gradient matches finite differences to 7×10⁻⁸.
- Convergence took 23 iterations: stationarity residual ‖∇S − L_Uᵀλ‖/‖∇S‖ = 4.5×10⁻¹⁰, constraint ‖F_c‖ = 3.5×10⁻¹⁷, S from 11.69 to 10.007.

| Quantity | Value |
|---|---|
| Max plaquette angle θ_max | 0.0438 (the minimizer concentrates curvature; it started at 0.0297) |
| Max link angle | 0.038 |
| max‖λ_e‖ / rms‖λ_e‖ | 0.933 / 0.510 |
| D3B bound at this θ: 27·6·(315/251)·θ | 8.91 |
| Ward check, ‖L_U Gφ‖ for random root-zero φ | 2.9×10⁻¹⁷ |
| D²J[Gφ, Gφ] / D²J[v, Gφ] | 2.5×10⁻⁸ / −2.7×10⁻⁹ (finite-difference noise) |
| D²S[Gφ, Gφ] / D²S[v, Gφ], Wilson part alone | −3.7×10⁻⁵ / 4.6×10⁻⁵ |
| D²J[v, v], for scale | 5.92 |

**The augmented Hessian D²S − λ·D²F_c on the 6 lowest modes of the Wilson-only H_U** (Ritz values, so upper bounds on the true minimum):

| | Values |
|---|---|
| Wilson-only eigenvalues | 0.0312, 0.0314, 0.0316, 0.0338, 0.0339, 0.0340 |
| Multiplier form −λ·D²F_c on that subspace | **+0.0019 … +0.0030** |
| Augmented Ritz values | 0.0335 … 0.0368 (flat λ_min is 0.0326) |
| Relative to H₀: Wilson only / augmented | 0.838–0.868 / **0.910–0.922** |

At this witness, whose θ_max of 0.044 is already above 1/30, the full augmented form keeps more than 90% of the flat form on the low modes. The multiplier term helps rather than hurts there, so a certificate should preserve its sign instead of bounding ‖λ‖·‖D²F‖.

## 5. Consequences for VOL14-D3

1. **Build the curvature estimate on stationarity.** At a constrained minimizer the curvature satisfies the lattice Yang–Mills equation with the multiplier source, so it is smooth below block scale. One route:
   - certify κ for **block-constant** n, which is a finite computation (the constant-direction value is 10.0 and the witness gives 6.3);
   - bound the deviation of the actual n_p from block-constant values using the stationarity equation;
   - absorb the remainder into the Bianchi-level constant (≥ 28) only on that deviation.
2. **Keep the multiplier term's sign:** it is positive on the low modes at the witness.
3. **Tighten λ through face cancellation:** measured about 12·θ rms and 21·θ max, against 203·θ.
4. **State relative comparisons in the chosen section,** for example the minimum-norm one, accounting for H₀∘ι not being gauge invariant (§2).
5. **Next numerical step:** witnesses at θ_max = 1/30 exactly, several seeds and coarse fields, a full-space relative form including the multiplier Hessian (a matvec via the second-order dexp correction), and a check of the minimum-norm section against the tree section.

## 6. Limits

- One witness (smooth start, a single seed) and one torus size.
- The low-mode results are Ritz values on 6 modes.
- The multiplier Hessian is from finite-difference polarization.
- The alternating maxima are lower bounds and heuristic, especially under the max-norm normalization.
- The Bianchi projection is abelianized, which is exact only to first order in the background.

## 7. Paste-ready PR comments

**PR #128 (D3A):**
> AI review (Claude), 26 Nov 2026, at `5d98eff`: the receipt replays byte-identically (also under `-O`). An independent enumeration reproduces every suffix count (maxima 9/8/7/6, means 8/3, 20/9, 16/9, 4/3) and every canonical endpoint. The argument checks: transported face-mean covariance, δP = P·Ad(s⁻¹s₀)Y, ‖L_U R_U − I‖ ≤ 64/315 at δ = 1/30, ‖T_U z‖ ≥ ‖z‖, the plaquette Hessian form, the signed-area identity, and β₀ ≤ 23/44. This fixes the covariance defect of review 09's fixed Z.

**PR #129 (D3B):**
> AI review (Claude), 26 Nov 2026, at `1b482ef`: the receipt replays byte-identically; no-float 192/0; docs 105/0/0; merges cleanly. The Ward identity is correct and is confirmed numerically at a constrained-stationary witness: D²J on root-zero gauge directions is about 10⁻⁸ against 5.9 for a generic direction, while the Wilson part alone leaks about 4×10⁻⁵. The 1701/251 arithmetic is correct; at the witness max‖λ‖ = 0.93 against the bound's 8.9.
>
> The 658 ceiling is a correct sufficient bound, but the exact supremum of this reference model over free |n_p| ≤ δ is at least 48, and at least 28 with Bianchi-compatible n. So no refinement of this model can reach the 1/2 budget at δ = 1/30, which needs at most 15. At the stationary witness κ = 6.3. Next: exploit stationarity. The augmented form there keeps more than 0.91 of H₀ on the low modes, with the multiplier term positive.
>
> Minor: the sealed expectation omits `multiplier_norm_le=1701/251`. Floating point, not certificates.

## 8. Reproduction

The scripts are stored in the project as `reviews/10-*.py`, with results in `reviews/10-*.json`. Save them without the `10-` prefix next to the review 09 modules `bgH.py` and `bg_gen.py`, together with `vol14d_bloch_crosscheck.py` (review 07) and `HZoff.npy` (from `08-d2_xcheck.py`).

| Script | What it produces | Time |
|---|---|---|
| `ref_adv.py` | the free-coefficient maxima | about 10 min |
| `ref_bianchi.py` | the Bianchi-compatible maxima | about 7 min |
| `stat.py 0.03` | the witness, multipliers, Ward check and low modes; writes `Ustar_0.03.npy` | about 30 min |
| `witness_kappa.py` | κ for the witness | about 3 min |
