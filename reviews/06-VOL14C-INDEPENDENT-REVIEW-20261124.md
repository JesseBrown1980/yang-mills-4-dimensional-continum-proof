**Independent AI review (Claude), 24 Nov 2026. PR #123, VOL14-C, head `a9f3db2`.**

**Verdict: correct as stated.** I have two corrections to the derivative statement and one calibration issue against VOL12 that should be resolved before VOL14-D/E rely on the small-field domain.

## Replay

- The checker equals its receipt, and `-O` gives identical output (0.8 s).
- The 6 prediction rows match the receipt row for row.
- No-float gate: 188 files, 0 failures. Docs integrity: 96 files, 0 broken links.
- The prediction commit `abf6adc` precedes the checker commit `a9f3db2`, though only by 59 s. The ordering holds in history, but the independence of the prediction rests on the author's word.

## Mathematics

| § | Claim | Assessment |
|---|---|---|
| 1 | Measurable, gauge-equivariant group map | **Correct.** The equivariance is *local*: it holds under every fine gauge transformation g, with B(U^g)_e = g(x)B(U)_e g(y)⁻¹. That is stronger than "global". Numerical check: error 8×10⁻¹⁶. |
| 2 | Reflection covariance and open-half support | **Correct.** I re-derived the support. B_x ∪ B_y is the box [−h, b+h] in the μ direction and [−h, h] transversally, so the middle segment and both connectors stay inside it. At a mid-plane, the open halves are unions of whole blocks. The link-RP pullback then follows from Lemma 0004 Theorem 4. This supplies the group-valued realization that VOL14-B's corrected E07 calls for. |
| 3 | DB(I)A = QA − d_coarse c̄ | **Correct, sign included.** The first-order term is QA + c̄(x) − c̄(y). The coarse curl kills the gradient. |
| 4 | d(P, P₀) ≤ 15δ at b = 3 | **Correct, and sharp.** Over all 10,473 loops P·P₀⁻¹, the largest abelian projected area Σ_{i<j}\|A_ij\| is exactly 15, attained by 96 loops. So the constant field F_ij = ±δ reaches 15δ: no path-by-path argument can lower 15. The cosine step cos(1/2) ≥ 7/8 is right. Numerically, \|V\| ≥ 0.989 for all 64 sign patterns of constant abelian fields at δ = 1/30. |
| 4 | ‖DB‖ ≤ 22, ‖D²B‖ ≤ 1210 | **Correct as ambient bounds at base points in the domain.** Two clarifications follow. |

## Requested clarifications

1. **Lie-algebra coordinates.** For U_ℓ ↦ U_ℓ exp(X_ℓ) with sup‖X_ℓ‖ ≤ 1:
   - The first derivative is still ≤ 22.
   - The second derivative along exp-curves picks up a DB(U·X²) term, so it is ≤ 1210 + 22 = 1232.
   
   Please state which coordinates VOL14-D will use.
2. **Looseness.** The constants are loose. Random sup-norm-1 directions give \|DB η\| ≈ 1.0 and \|D²B(η,η)\| ≈ 1.4. I did not search for worst-case directions.

## Calibration issue: VOL14-C's small-field domain against VOL12

- δ ≤ 1/30 means 1 − W_p ≤ 1 − cos(1/30) ≈ 5.6×10⁻⁴. In VOL12's defect convention (a_p > ε/4), that is **ε ≈ 1/450**.
- At ε ≈ 1/450, VOL12's ρ⋆ ≤ 18⁻³ needs **β ≳ 1.1×10⁶ (about 9^6.35)**. At ε = 1/16 it needs only 35,069. This is a floating-point estimate.
- So at the β = 9⁵ fixture, VOL12 gives **no** information about VOL14-C's domain.

**Two fixes**
- **Option 1:** move the scale-0 fixture to β = 9⁷.
- **Option 2:** enlarge the domain. Because 15 is sharp, the gain has to come from the floor on the mean:
  - Requiring only \|V\| ≥ 1/2 allows δ ≤ π/45 ≈ 0.070, which is ε ≈ 1/103 and β ≳ 2.4×10⁵.
  - ‖DB‖ ≤ 22 is unchanged, because the note already uses ‖DN‖ ≤ 2 = 1/r.
  - ‖D²B‖ rises to ≤ 24·121 + 220 = 3124.

## Checker suggestions (non-blocking)

1. The `noncrossing_union` test is tautological: `sides == sides2` already forces the union to have size 1. The conclusion still follows from `block_one_half` and `path_in_endpoint_blocks`. Please replace the test with a direct check, on the L = 12 torus, that every site and link of every path of every non-crossing coarse link lies in one open half.
2. The swap count and the derivative constants are checked only as arithmetic on the constants. Two integer-only additions would make them concrete:
   - a per-word count of the two-stage swap construction, showing it is ≤ 15;
   - the projected-area witness showing 15 is attained, which is integer arithmetic.
3. The corner-offset negative control is a single hand-picked word. VOL14-B's E05 (4096/4096 failures) is the stronger control and could be cited.

## Relation to Bałaban (for the open comparison item)

For P_i = P₀ exp(X_i), the normalized quaternion mean equals P₀ exp(Σ w_i X_i) + O(\|X\|³). I checked this algebraically and numerically: the error falls by a factor of 8 per halving. So the candidate agrees with a log-mean about the straight reference path through second order in the deviations. Any difference from that kind of nonlinear average first appears at third order.

**Remaining OPEN:** the effective action, VOL14-D propagator locality, large-field control under the transformed measure, and human review.
