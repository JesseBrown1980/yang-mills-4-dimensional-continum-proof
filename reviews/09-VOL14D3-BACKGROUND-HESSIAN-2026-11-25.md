# VOL14-D3 groundwork: the background-dependent constrained Hessian and which perturbation estimators survive

**Provenance:** written by Claude (AI) on 25 Nov 2026. Everything here is exploratory floating-point numerics on finite backgrounds. **No result in this review is a certificate.**

**Scope:**
- Fine torus 12⁴, which is a 4⁴ coarse torus at b = 3.
- SU(2), with fluctuations in Lie-algebra coordinates, U_ℓ → U_ℓ exp(x_ℓ).
- Constraint: the VOL14-C map. Gauge section: the D1 block tree. Coordinates: D2's fixed space Z.
- Eight backgrounds, one seed each, block row 0 only.

## 1. Summary

1. **Absolute perturbation of H fails twice over.** At link angle 0.01:
   - the entrywise envelope of δH is 1.18, and the block operator-norm sum is 1.22;
   - the true ‖δH‖ is 0.208, so the estimators lose about 6× to cancellation;
   - the D2 slack it must fit under is 1/220 ≈ 0.0045, so even the exact norm is 46× too large.

   δH is of order (link angle) × ‖H‖, while the budget is of order λ_min. So absolute comparison can only tolerate link angles of order 1/κ ≈ 10⁻⁴, whatever the estimator.
2. **The relative form works.** E = H₀^{−1/2}(H_U − H₀)H₀^{−1/2} is linear in the background, from ±0.086 to ±0.29 to ±0.87 at link angles 0.003, 0.01 and 0.03. The weighting at η = ln(65/64) adds only about 0.003. If ‖E_W‖ ≤ α < 1 can be certified, D2's weighted locality carries over with its rate unchanged and its prefactor multiplied by 1/(1 − α − β₀). Here β₀ ≈ 0.0096 is the weighting's own relative cost at the identity.
3. **The relative estimator depends strongly on the background gauge; λ_min does not.** The same smooth background gives:
   - largest E of 0.51 in its own gauge;
   - largest E of 6.4 in a block-tree plus coarse-axial gauge;
   - λ_min equal to 4 digits in both.

   A pure-gauge background leaves λ_min unchanged but gives E up to 0.92. **D3 needs a smooth (Landau-type) background gauge, not an axial or tree gauge,** for the comparison with H₀. Relaxing to a Landau gauge restores the good numbers: E −0.34/+0.48 and γ 0.39 for the smooth background, against 6.4 and 2.4 in the axial gauge. For the random background it is slightly better than the original gauge (γ 0.158 against 0.175).
4. **Tolerance in a good gauge is close to VOL14-C's δ.** Measured E_min ≈ −(7 to 12) × θ_p,max, where θ_p,max is the largest plaquette angle, for the random and smooth backgrounds in their own gauges and for random in the tree gauge. E_min ≥ −1/2 then holds up to θ_p of about 0.04–0.07, comparable to VOL14-C's δ = 1/30 ≈ 0.033. **This supersedes review 08 §5.3,** whose estimate of 10⁻⁴ came from the absolute budget.
5. **The certificate gap is concentrated in the curvature term.** Converting the measured norms into certified relative bounds through the floor loses:
   - about 7.5× on the curl part (γ);
   - about 70× on the curvature part, or about 20× with the true floor.

   Naive certified tolerance is θ_p ~ 10⁻³. Closing this means bounding the sin θ_p commutator term by ‖dx‖·‖x‖ or better, not by ‖x‖², and bounding δK locally.

## 2. What was built

| Piece | Definition |
|---|---|
| Wilson Hessian W_U | Exact second derivative of Σ_p(1 − Re U_p) at U in the coordinates U_ℓ exp(x_ℓ). Per plaquette, the diagonal blocks are δ_ab·Re U_p, and the (i < j) blocks are s_i s_j (h_j g_i e_a m_ij)_b. At U = 1 it equals dᵀd (one copy per colour), matching the D1/D2 normalization. |
| Covariant curl d_U | Rows s_i Ad(g_i) with transports g_i. **W_U = cos θ_p · d_Uᵀ d_U + C_U**, where C_U is the curvature (sin θ_p) part. |
| Constraint L_U | Derivative of B(U)_e = V_e/\|V_e\| in the coordinates B(U)_e exp(Y). Since V_e = (1/81) Σ_z Ā_z M_z C̄_z factorizes over the independent connector choices, Y = Im(B̄ δV)/\|V\|. |
| Section and coordinates | x = 0 on block trees (valid for every U). R_U = R(L_U R)⁻¹, so L_U R_U = I. T_U = I − R_U L_U on the fixed space Z. |
| Constrained Hessian | H_U = (T_U P)ᵀ W_U (T_U P) on Z. |

**A structural fact that transfers to every background:** R_U L_U z is constant on each face while z ∈ Z has mean zero there, so ‖T_U z‖ ≥ ‖z‖ for every U. The T-part of the D1 floor argument therefore needs no background estimate. Only the curvature reconstruction (the 105) does.

## 3. Validation (all pass)

| Check | Result |
|---|---|
| L₁ equals the D2 constraint rows (⊗ I₃) | 2.5×10⁻¹⁶ |
| Block row of H₁ vanishes beyond coarse distance 2 | 0 |
| Block row of H₁ equals the D2 integer stencil (⊗ I₃) | 4.4×10⁻¹⁵ |
| λ_min(H₁ on Z) on the torus, against the Bloch value 0.0326440 | 8×10⁻¹³ |
| xᵀW_U x against a finite-difference second derivative of the action (ε = 0.15) | 7×10⁻⁸ relative |
| L_U x against a finite difference of the nonlinear map B(U e^{tx}) | 2×10⁻¹¹ relative |
| L_U T_U P x = 0 | 4×10⁻¹⁷ |
| Gauge covariance of W_U, under a large random gauge transformation | 9×10⁻¹⁶ |
| Gauge covariance of L_U: Y′ = Ad(g at the coarse endpoint) Y | 3×10⁻¹⁵ |
| H₀^{−1/2} H₁ H₀^{−1/2} = I (FFT over coarse momenta) | 1.5×10⁻¹⁴ |

## 4. Backgrounds

| Family | Definition |
|---|---|
| random | U_ℓ = exp(ε n_ℓ) with random unit n_ℓ, so every link has angle ε. Plaquette angles reach about 4ε. |
| smooth | Long-wavelength fields, with link angle up to ε and plaquette angles about equal to ε. |
| gauge | A pure gauge g_x = exp(ε n_x): zero curvature, link angles up to 2ε. |
| canon / canonsmooth | random or smooth backgrounds put into the block-tree plus coarse-axial gauge radiating from block 0. Block row 0 depends only on the 3⁴ cube of blocks around block 0. |
| landau / landausmooth | the same backgrounds relaxed to the Landau gauge (maximize Σ Re U_ℓ). |

None of these is a constrained minimizer, which is the actual RG background. Minimizers are smooth, so the smooth families are the closer proxy.

## 5. Measurements

**Geometry and spectral floor**

| family | eps | max link angle (cube) | max plaquette angle | λ_min(H_U on Z) | change | weighted Re floor (η = ln 65/64) |
|---|---|---|---|---|---|---|
| random | 0.003 | 0.0030 | 0.0118 | 0.03248 | -0.49% | 0.03229 |
| random | 0.01 | 0.0100 | 0.0395 | 0.03085 | -5.50% | 0.03065 |
| random | 0.03 | 0.0300 | 0.118 | 0.01080 | -66.92% | 0.01053 |
| smooth | 0.03 | 0.0300 | 0.0297 | 0.03188 | -2.35% | 0.03168 |
| gauge | 0.03 | 0.0600 | 4.2e-17 | 0.03265 | +0.01% | 0.03245 |
| canon | 0.003 | 0.0223 | 0.0118 | 0.03248 | -0.49% | 0.03229 |
| canon | 0.01 | 0.0743 | 0.0395 | 0.03085 | -5.49% | 0.03065 |
| canonsmooth | 0.03 | 0.2490 | 0.0297 | 0.03189 | -2.30% | 0.03169 |
| landau | 0.01 | 0.0172 | 0.0395 | 0.03085 | -5.50% | 0.03065 |
| landausmooth | 0.03 | 0.0427 | 0.0297 | 0.03187 | -2.36% | 0.03168 |

**Perturbation estimators (absolute and relative)**

| family | eps | entrywise env_w(δH) | block-norm sum_w(δH) | E min / max | E_W min | γ | ‖δK‖ | curvature rel. min / max | ‖C‖ abs |
|---|---|---|---|---|---|---|---|---|---|
| random | 0.003 | 0.352 | 0.366 | -0.086 / +0.086 | -0.089 | 0.053 | 0.0384 | -0.087 / +0.085 | 0.0595 |
| random | 0.01 | 1.18 | 1.22 | -0.288 / +0.287 | -0.291 | 0.175 | 0.128 | -0.299 / +0.273 | 0.199 |
| random | 0.03 | 3.63 | 3.66 | -0.869 / +0.856 | -0.872 | 0.526 | 0.384 | -0.982 / +0.750 | 0.609 |
| smooth | 0.03 | 3.04 | 2.94 | -0.346 / +0.512 | -0.348 | 0.409 | 0.273 | -0.212 / +0.204 | 0.157 |
| gauge | 0.03 | 4.3 | 4.19 | -0.478 / +0.916 | -0.480 | 0.670 | 0.372 | -0.000 / +0.000 | 1.04e-14 |
| canon | 0.003 | 0.7 | 0.71 | -0.122 / +0.131 | -0.124 | 0.114 | 0.108 | -0.087 / +0.085 | 0.0594 |
| canon | 0.01 | 2.37 | 2.37 | -0.374 / +0.478 | -0.376 | 0.381 | 0.36 | -0.296 / +0.277 | 0.199 |
| canonsmooth | 0.03 | 3.95 | 4.52 | -0.866 / +6.383 | -0.866 | 2.407 | 2.02 | -0.243 / +0.215 | 0.157 |
| landau | 0.01 | 1.06 | 1.12 | -0.282 / +0.275 | -0.285 | 0.158 | 0.127 | -0.299 / +0.273 | 0.199 |
| landausmooth | 0.03 | 2.71 | 2.63 | -0.343 / +0.481 | -0.346 | 0.391 | 0.301 | -0.211 / +0.205 | 0.157 |

At the identity, the weighted part alone: E_W0 in [-0.0096, +0.0002]; block-norm sum of H_1 row = 56.021; sanity 1.5e-14; far 0.0e+00

The true operator norm of δH on Z for random, link angle 0.01, is **0.208** (extreme eigenvalues −0.2076 and +0.2064).

Notation:
- E and E_W are the relative forms, without and with weighting.
- γ = sup ‖δK z‖/‖K₀z‖, where δK = d_U T_U P − d T P.
- The curvature column is H₀-relative; the last column is the absolute norm of C on Z.

## 6. Analysis

**Absolute estimators.** Across all backgrounds the block operator-norm sum is within 15% of the entrywise envelope, so keeping block-internal signs gains little. The true ‖δH‖ (0.208 at random, link angle 0.01) is about 6× below both, so cancellation across blocks and directions is real. But even 0.208 exceeds the 1/220 budget by 46×. Reading the true norm through the floor gives 0.208/0.0326 = 6.4, while the relative form gives 0.29, a further 22×.

**Relative form: linear and weight-insensitive.**
- For random backgrounds, E grows at about 29 per radian of link angle, equivalently about 7.3 per radian of θ_p,max.
- E_W − E ≈ −0.003, and at the identity β₀ = 0.0096 at η = ln(65/64).
- λ_min itself falls only quadratically for random backgrounds (−0.49% and −5.5% at link angles 0.003 and 0.01) because first-order shifts average out. E is the right worst-direction quantity for a given background, but no sample measures the worst background.

**Gauge.** λ_min agrees to 4 digits between the original, tree and axial gauges of the same background (−5.50% against −5.49%, −2.35% against −2.30%), and is unchanged for a pure gauge. E does not agree: it follows link deviations, at about 11–18 per radian (γ), on top of curvature at about 7 per radian of θ_p. The tree and axial gauges multiply link deviations by about 7× for random backgrounds and about 8× for smooth ones across the dependence cube. A Landau-type gauge keeps them at about the plaquette scale.

**Decomposition and certificate losses at random, link angle 0.01:**

| Part | Measured relative | Certified by naive conversion | Loss |
|---|---|---|---|
| Curl, γ | 0.175 | √105·‖δK‖ = 1.31 | 7.5× |
| Curvature | 0.30 | 105·‖C‖ = 20.9 (or ‖C‖/0.0326 = 6.1 with the true floor) | 70× (20×) |

The curvature term is small relative to H₀ because it acts mainly on directions where H₀ is large. A bound of the form ‖C‖·‖x‖² throws that away.

## 7. Consequences for VOL14-D3

1. **Formulate D3 as relative-form coercivity:** Re(W H_U W⁻¹) ⪰ (1 − β₀ − α_W) H₀ on Z, in a fixed smooth background gauge. D2's rate then transfers unchanged. Certify β₀ separately; it is a statement about the identity only.
2. **Certify γ locally,** for example as a patch-wise inequality ‖δK z‖² ≤ Σ_patches c_P θ_P² ‖K₀ z‖²_{P′} using local Poincaré constants, instead of through the global 105.
3. **Bound the curvature term relative to H₀,** for example by ‖d_U x‖·‖x‖ with a √(floor) gain. This is where most of the certificate gap sits.
4. **Use a Landau-type background gauge,** and record the gauge-fixing estimate it needs: link deviation ≲ c·θ_p on the dependence cube.
5. **Target:** the measured E_min ≥ −1/2 window is θ_p ≲ 0.04–0.07 in good gauges, so a certified version at δ = 1/30 looks plausible but is unproven. This replaces review 08 §5.3's 10⁻⁴.

## 8. Limits

- One torus size (4⁴ coarse) and one seed per background.
- Envelope and block norms are from block row 0 only.
- Backgrounds are not constrained minimizers. At a minimizer the gradient of the action vanishes on the slice, but the sin θ_p curvature part of the Hessian remains. So the curvature measurements here indicate its size, not its exact form at RG backgrounds.
- LOBPCG residuals are about 10⁻⁷ on the lowest modes. eigsh runs used tol 10⁻⁶.
- No worst-case search over backgrounds.

## 9. Reproduction

The scripts are stored in the project as `reviews/09-*.py`; save them without the `09-` prefix. They need numpy and scipy, and use about 2 GB per run.
1. `vol14d_bloch_crosscheck.py` (review 07) and `HZoff.npy` (from `08-d2_xcheck.py`) must be in the working directory.
2. `python3 validate.py <path to PR #126 tests/ym4_vol14d2_weighted_locality.py>` runs §3 and writes `R1_block0.npy`.
3. `python3 full.py FAMILY EPS` runs one background, in about 12–15 minutes, and appends to `full_results.jsonl`.
4. `python3 tabulate_full.py` prints the §5 tables. `dH_abs.py` gives the true ‖δH‖.
