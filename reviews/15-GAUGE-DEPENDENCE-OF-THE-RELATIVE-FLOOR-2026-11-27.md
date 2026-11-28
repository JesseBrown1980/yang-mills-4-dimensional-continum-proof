# Non-Abelian counterexamples to the D3 target at δ = 1/30, and the coarse gauge dependence of the relative floor

**Provenance:** written by Claude (AI) on 27 Nov 2026, as the follow-up to review 14 (VOL14-D3G, PR #138). This is AI verification, not human review. Floating-point numerics are exploratory; **none is a certificate.**

## 1. Summary

1. **The target H_aug ≥ ½H₀ fails at δ = 1/30 for non-Abelian backgrounds.**
   - An adversarial search over non-Abelian coarse data (§4) produced constrained-stationary fields with every fine plaquette angle at most 1/30 and full-space augmented relative floors of **0.461** and **0.260**.
   - Both are on the M = 2 torus, so they bound the tiled 4⁴ floors from above.
   - They are built and gauged exactly like the D3F, D3G and review 11 fixtures: co-exact coarse data, the flat-minimiser start, then constrained minimisation.
   - A local ascent over all block-constant gauges on M = 2 raises them only to **0.4635** and **0.288**. So they are not gauge artefacts.
   - At δ = 1/60 the same coarse data give 0.666 (step 1) and 0.489 (step 4) in the construction's gauge. In the best coarse gauge found, step 4 reaches 0.521. So 1/60 is borderline: it depends on the gauge convention, and no search has been run at that tolerance.
2. **The relative floor is not gauge invariant.** λ_min(H₀^(−1/2) H_aug(U) H₀^(−1/2)), measured against the fixed flat H₀ in tree-gauge Z coordinates, changes under block-constant (coarse) gauge transformations, which leave every plaquette angle and the stationarity unchanged.
   - A physically trivial pure gauge (θ = 0) has floor 0.372 when alternating blocks are rotated by a face-link angle of 0.1.
   - The same three-colour D3G field drops from 0.566 to 0.472 under a coarse rotation of 0.05.
   - The target therefore has to be stated in a fixed coarse gauge, or against a gauge-covariant reference.
3. **The first-order (linear in the background) model is not predictive at δ = 1/30.** For the three-colour field it predicts 0.42 against a nonlinear floor of 0.566. The positive second-order terms are large. They do not, however, stop the search's direction from lowering the true floor.
4. **New tools, both validated:**
   - a native M = 2 version of the review 09–14 operator;
   - a JAX implementation of the exact augmented form (14× faster per matvec, with exact background derivatives);
   - an exact gauge-gradient ascent for the floor.

## 2. Tools and validation

| Check | Result |
|---|---|
| Native M = 2 operator (review 09 module with the coarse size as a parameter) on the M = 2 restriction of the two-colour witness | augmented 0.5733725657, Wilson-only 0.5686617377; period-2 subspace of 4⁴ (review 14): 0.5733725652, 0.5686617377 |
| JAX augmented form vs review 12's operator, same field | quadratic forms agree to 3×10⁻⁹ (the central-difference error of the NumPy matvec); lowest eigenvalue 0.5733725643 vs 0.5733725657 |
| JAX three-colour floor on M = 2 | 0.5659541, identical to review 14's 4⁴ value |
| Speed (M = 2, 2 cores) | JAX matvec 0.4 s against 5.6 s for NumPy; a full augmented solve takes about 2 minutes |

The JAX module computes q(U, z) = d²/dt² J(U·exp(t·T_U P z)) at t = 0, where C = B(U), μ = λ/|V| and R_U are all treated as functions of U. Derivatives with respect to the background are therefore exact.

## 3. Coarse gauge dependence

**Mechanism.** In tree gauge the residual gauge freedom is one rotation g_X per block. Under it, every right fluctuation is rotated by Ad of its target block, so H_aug(U^g) = Γᵀ H_aug(U) Γ on Z. Γ preserves Z, because face links of one face share a target block.

The fixed flat H₀ does not commute with Γ. It couples links whose targets lie in different blocks, for example a crossing link (target in the next block) and an inner link of the same plaquette. So the *relative* spectrum changes, even though the absolute spectrum of H_aug does not.

D3A made the fine (within-block) gauge covariant through transported face means. The coarse rotations are untouched by that construction.

### 3a. Pure gauges (θ = 0, ∇S = 0, so the augmented and Wilson-only forms coincide)

For g = exp(φ_X i), the neutral colour is fixed and the charged pair is one complex scalar with phase e^(2iφ) at the target block. The relative spectrum is then a 3840-dimensional dense generalized eigenproblem on M = 2. Because the tiled pattern on 4⁴ contains these modes, any value below 1/2 carries over to 4⁴.

| face-link angle α on alternating blocks | 0.02 | 0.05 | 0.1 | 0.2 | 0.5 | π/4 | π/2 |
|---|---|---|---|---|---|---|---|
| checkerboard pattern (all four axes) | 0.814 | 0.600 | **0.372** | 0.166 | 0.038 | 0.018 | 0.009 |
| stripes along axis 0 | 0.879 | 0.726 | 0.532 | 0.300 | 0.088 | 0.044 | 0.023 |

Independent check: the explicit field U^g with α = 0.1 has θ_max = 0 and ∇S = 0 exactly. The NumPy constrained Hessian gives a Rayleigh quotient of 0.3717104896 on the dense eigenvector, equal to the dense value. The relative floor falls below 1/2 at α ≈ 0.07 (checkerboard) and α ≈ 0.11 (stripes).

### 3b. The same physical field in different coarse gauges

The M = 2 restriction of the three-colour D3G witness was rotated by g = exp(α i) on odd blocks. θ_max stays 0.0333311 throughout.

| α | 0 | ±0.01 | ±0.02 | 0.05 |
|---|---|---|---|---|
| augmented relative floor | 0.5659541 | 0.5611972 | 0.5479323 | **0.4722262** |

**Reading.**
- The floor is symmetric in ±α and the drop is quadratic, so the gauge produced by the review 10 construction (co-exact coarse data, close to coarse Landau gauge) is a local maximum of the floor along this direction.
- A coarse rotation of 0.05, smaller than the field's own link components (about 0.08), already takes the floor below 1/2.
- All floors reported so far (D3F 0.6116, D3G 0.573/0.566, review 11's 0.871) are measured in this one gauge.

### 3c. What the certificate needs

Any of the following would make the statement well posed.

1. **A coarse gauge condition**, for example coarse Landau gauge (minimal Σ_e |log C_e|²). The bound H_aug ≥ ½H₀ is then claimed only on that slice. On the torus, flat backgrounds with nontrivial holonomy cannot be gauged away and act locally like the stripe pattern of §3a. They therefore need a smallness condition on holonomies, or a patch-local formulation.
2. **A gauge-covariant reference** in place of H₀, for example H₀ conjugated by the block rotations of the coarse field, or the Hessian at D3D's canonical lift. Pure gauges then give exactly 1. D2's locality would have to be re-proved for that reference, uniformly in C.
3. **Patch-local gauges**, consistent with D3F's compensated gluing: each patch is gauge-fixed before its local floor is certified. The gluing must then absorb the gauge mismatch on overlaps. §3a shows that mismatch is not small: a relative rotation of 0.05 between overlapping gauges costs about 0.1 of floor.

The choice should be made before the charged-sector certificates are computed, because it changes the operator being certified.

### 3d. Why this is structural (an argument, not a computation)

- §3a shows that against the fixed flat H₀ the relative floor responds to the **coarse link values**, the relative rotations between neighbouring blocks, even when there is no curvature at all.
- No gauge keeps coarse links small over a region of sustained curvature. For an Abelian-like field with coarse plaquette angle Θ_c over an ℓ × ℓ square of blocks, the loop around it has angle ℓ²Θ_c, carried by 4ℓ links, so some link is at least ℓΘ_c/4.
- With Θ_c up to about 9θ_max = 0.3 at δ = 1/30, links of 0.1–0.15 appear within two or three blocks, which is the range where §3a's floors fall below 1/2.
- So under a plaquette-only small-field condition, a bound uniform in the volume, or in the gluing patch size, seems out of reach with the flat H₀ as reference. The finite M = 2 torus caps the effect, which is why the searches there stay bounded.
- A background-covariant reference is the standard remedy (Bałaban's averaging and propagators are covariant). For pure gauges it gives exactly 1 by construction.

This is a heuristic. It has not been checked on larger tori.

## 4. The first-order model and the adversarial search

The first-order operator W(v) is the exact derivative of the whitened augmented form at U = 1 in the direction of the flat minimiser A_v. It includes the curvature, multiplier and T_U variations together. With max_p |dA_v|_p = 1, the floor at θ = 1/30 is 1 − κ/30 + O(θ²), with κ = λ_max(−W(v)).
- W(v) is computed by central differences in the background amplitude (two exact JAX matvecs at exp(±10⁻³A_v)); the nonstationarity there is O(s²) and even, so it cancels.
- The coarse gradient comes from 135 directional differences of the exact form. Its consistency check reproduces κ to 6 digits.

| | κ (first order) | first-order floor at 1/30 | nonlinear floor at 1/30 |
|---|---|---|---|
| three-colour D3G data | 17.33 | 0.422 | **0.566** |
| search step 1 | 25.62 | 0.146 | **0.4611** (Wilson-only 0.4336) |
| search step 4 | 43.99 | −0.466 | **0.2604** (Wilson-only 0.2309; stationarity residual 10⁻⁵) |

- The search runs over the 135 co-exact coarse directions on M = 2 (192 − 45 gauge − 12 harmonic; the curvature map has exactly this rank). It alternates the top eigenvector of −W(v) with a second-order cone program for the coarse data, subject to max_p |dA_v|_p ≤ 1.
- **The first-order constant overstates the drop badly.** For the three-colour field the second-order coefficient in floor(θ) = 1 − κθ + cθ² is c ≈ 130. A plausible source is the ‖[A, a]‖² term of the covariant Laplacian: with link amplitudes near 0.08 against λ_min(H₀) = 1/105 at 4⁴, it is of order one on the lowest modes.
- The search increases κ by moving to coarse data that saturate the curvature bound on many plaquettes, with larger link amplitudes. Those are exactly the fields where both the first-order "gauge-like" term (§3) and the positive second-order term are largest. **The nonlinear floor nevertheless follows the first-order direction:** 0.566 → 0.461 → 0.260.

### 4a. Are the search candidates gauge artefacts?

§3 shows that a floor measured in one coarse gauge can be raised by choosing another. So each candidate's floor was maximised over all block-constant gauges.
- **Gradient.** For the generalized eigenvector z (Hz = λH₀z), the derivative along the rotation of block X about colour a is 2⟨Ωz, Hz⟩. One matvec gives all 48 components.
- **Ascent.** Steps along the normalized gradient with backtracking, trying both signs. Every trial is an exact recomputation of the floor.
- θ_max and stationarity do not change under these rotations.

| | floor in the construction's gauge | gauge-maximised floor (M = 2) | gauge gradient at the end |
|---|---|---|---|
| three-colour D3G data | 0.5660 | 0.5660 (symmetric ±α, §3b) | 0 by symmetry along the tested direction |
| search step 1 | 0.4611 | **0.4635** | 0.023 (from 0.116) |
| search step 4 | 0.2604 | **0.2882** after 8 steps, still rising by about 0.001 per step | 0.11 (the lowest two eigenvalues are nearly degenerate, so the gradient of the minimum is not smooth) |

**Reading.**
- The step-1 field gains only 0.0024 from the best coarse gauge, and stays at 0.4635. This is the M = 2 problem; the 4⁴ tiling contains these modes, so its floor in the tiled gauge is at most 0.461.
- The only freedom the M = 2 search does not cover is a gauge that is not period-2 on the 4⁴ torus. That is not expected to recover 0.04, but it is untested.
- The step-4 field also stays far below 1/2.

**Implication.** A certificate built from the linear-in-curvature model cannot reach 1/2, because κ > 15 already for the D3G data. Certificates must keep the second-order background terms, and a meaningful adversarial search must optimise the nonlinear floor in a fixed coarse gauge. With the JAX operator a nonlinear floor costs about 2 minutes on M = 2 plus the constrained minimisation. The gradient of the nonlinear floor needs implicit differentiation of the stationarity condition, which is the natural next tool.

## 5. Consequences for the D3 plan

1. **At δ = 1/30 the uniform target is false**, in the construction's gauge and in the best coarse gauge on M = 2. The floor 0.26 corresponds to ‖E‖ ≥ 0.74 in H_aug = H₀^(1/2)(1 + E)H₀^(1/2), so the Neumann-series step built on ‖E‖ ≤ 1/2 cannot work for these backgrounds at that tolerance.
2. **Smaller tolerance.** The two candidates were rebuilt at θ_max = 1/60, the smallest tolerance the current β = 9⁷ choice allows under the VOL12 ρ⋆ formula.

   | δ = 1/60 | Wilson-only | augmented, construction's gauge | augmented, best coarse gauge found |
   |---|---|---|---|
   | search step 1 | 0.6536 | 0.6656 | — |
   | search step 4 | 0.4766 | **0.4894** | **0.5208** (6 ascent steps, levelling off) |

   Halving δ lifts the step-4 field from 0.26 to 0.49 in the construction's gauge and 0.52 in the best gauge found, a 4% margin. These coarse data were optimised for 1/30, so a search run at 1/60 would probably find lower values. **At 1/60 the target is marginal at best**, and its truth depends on the gauge convention. A uniform statement with margin seems to need a covariant reference, a smaller δ (larger β), or a target constant below 1/2 with a correspondingly stronger locality estimate.
3. **Gauge convention.** Whatever tolerance is chosen, the statement must name the coarse gauge (§3c). The search here used the review 10 construction's gauge (co-exact coarse data) and confirmed the result by gauge maximisation.
4. **Priorities.** The two Abelian fixtures (D3F) and the D3G staggered fields are no longer near the worst case. Charged-sector certificates for them would certify fields that the search has already beaten. The next steps are:
   - settle the gauge convention and the tolerance;
   - rerun a nonlinear adversarial search at the new tolerance;
   - certify only the hardest fields found.
5. **Search coverage.** Only one search path, from the three-colour field, was run, for four first-order steps. Starting points, the nonlinear objective and M = 4 data with period 4 are all untested. The values here are upper bounds on the true worst case, not estimates of it.
6. **Admissibility.** The candidates are local constrained minimisers: they were found by descent from the flat-minimiser start, and their constrained Hessian is positive. Whether each is the *global* constrained minimiser for its coarse data was not checked. If the D3 statement is meant only for global minimisers, that check is needed before these count against it.

## 6. Reproduction

Scripts are stored in the project as `reviews/15-*.py`. They use the review 09–14 modules; `bgH.py` now reads the coarse size from `YM_MC` (default 4, so all earlier scripts are unchanged).

| Script | What it does |
|---|---|
| `15-bgH.py` | review 09's operator module with the one-line `YM_MC` change |
| `15-m2_check.py` | native M = 2 operator on the restricted two-colour witness |
| `15-jaug.py` | JAX augmented form (exact background derivatives) |
| `15-jaug_check.py` | JAX vs NumPy validation |
| `15-gauge_dense.py` | exact relative spectra at pure coarse gauges (dense, M = 2) |
| `15-gauge_verify.py` | NumPy Rayleigh-quotient check at the explicit gauge-transformed field |
| `15-gauge_on_field.py` | the three-colour field under coarse rotations |
| `15-search.py` | first-order alternating search (cone program over co-exact coarse data) |
| `15-nl_eval.py` | nonlinear floor of coarse data at θ_max = δ (default 1/30) |
| `15-gauge_opt.py` | maximisation of the floor over coarse gauges (exact gradient, backtracking) |
| `15-results.json` | all numbers above |
