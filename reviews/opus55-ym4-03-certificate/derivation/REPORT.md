All four claims survive. My own exact computations on Z2 2×1, Z2 3×1 and Q8 2×1 found no false certification, and no printed low end above the truth or high end below it. The weak point is the negative control: it sits far enough below the error term that a version with the derivation's factor 2 dropped still passes every check. I filed 9 holds (8 medium, 1 low) that add a sharp control.

The relayed user line ("the TV got caught into the conversation") gave this lane no instruction, so I ran the computed task, read-only on the checkout.

**Head checked:** `2184b54f44c39079f4873562c8874da3836736e1`, at the start and at the end. The checkout stayed clean, with no `__pycache__`.

## What I ran (MEASURED)
- **Full test at the head:** 401 checks, 0 failed, 7 misses, exit 0. Its stdout equals the receipt byte for byte once Windows' CRLF line ends are turned into LF (sha256 `d89c17ca…` both). My first comparison dropped the CRs through sed; the correction is written beside that line in FINDINGS.
- **Sabotage `visibility_ignores_omega_error`:** exit 1, with exactly `flux_exact_zero_overlap_not_certified_Z2_2x1` and `_Z2_3x1` red.
- **Instrumented flux-only copy:** 202 checks, 0 failed, all 30 flux rows equal the receipt. It dumped u, S, the levels, sin² and every candidate vector.
- **Model and exact projectors of my own, sharing no code with the test.** My S, weights, twists and Perron vector u equal the test's on Z2 2×1, 3×1, 2×2, 4×1, 5×1 and Q8 2×1. W·S is exactly symmetric, so S is self-adjoint in the weighted inner product. Every level window holds exactly the eigenvalue it names.
- **Tests of the test's own functions:**
  - A constructed zero-part control run through `certify_overlap` and `exact_vector_visible`.
  - 9,000 exact worst cases through the same two functions.
  - 3 mutants of the error term.
  - The Z2 4×1 and 5×1 variants (86 checks) and an indefinite-weight variant.
  - The no-float gate on the patched tree.

## Survives
1. **Claim 1 (sin² bound).** DERIVED: it needs ρ > λ₁ (guaranteed by `gap > 0`), all other e = 0 values at or below `high_1`, u exactly in e = 0, and S self-adjoint. It does not need T ≥ 0, and every floor points the safe way. MEASURED: the true sin² is at or below the bound on 6 models, within a factor of 2 (2x1: 2⁻¹⁸⁹⁶..2⁻¹⁸⁹⁵). The test's gap is at or below the true scaled gap (12057086290172 ≤ 12057086290172.23).
2. **Claim 2 (ground weight of the centered vector).** DERIVED. MEASURED: every centered vector's true ground weight is at or below the bound. The 9,000 fuzz cases gave 0 low ends above the truth.
3. **Claim 3 (visibility past u's error).** DERIVED, e = 0 and e ≠ 0. It needs:
   - |F| = max|f|, which holds because the metric is diagonal and positive.
   - |S| = λ₀, by Perron–Frobenius.
   - O mapping e = 0 into e = 0. The test does not check this for the commutator; I measured it holds for Q8's.

   MEASURED: on all 19 rows, the true share lies inside the printed bracket and every MET row has a true part above 0. For example, Q8's commutator gives 0.041658961681 inside [41658960, 41658963], with |PΟΩ|² = 0.1456.
4. **Claim 4 (negative control).** DERIVED and MEASURED: F₀SF₀ = 2⁻ᴸ⁰S on e = 0 exactly, on 2×1, 3×1, 4×1 and 5×1. The control is rejected, and the sabotage turns it red.

## Refuted
No claim is refuted. The finding is about the control's sensitivity, all MEASURED:
- **The old control sits far below the error term.** Its |Pw|²/error is 2⁻¹⁰..2⁻⁹ on 2×1, 2⁻²⁰..2⁻¹⁹ on 3×1, and 2⁻⁵² on 5×1. It shrinks with lattice size because the bound uses the whole-space norm of O, not its norm on e = 0.
- **Mutants:** dropping the factor 2 (m1) passes all 202 flux checks with every row unchanged; dividing the error term by 512 (m2) also passes; dividing by 1024 (m3) turns only the 2×1 control red.
- **Constructed control.** I built a zero-part operator O'' = 2^(b·shift+1)S^b − (Gᵇ+Hᵇ), which is a polynomial in S. Through the test's own functions it reads 0.999999998 of the error term on 2×1 and 0.995945412 on 3×1. As derived, it is not certified; with the factor 2 dropped, it is certified.
- **Fuzz:** 9,000 worst cases, 0 false certifications, largest ratio 0.999999999997; all 9,000 are certified once the factor 2 is dropped.

The error term is the right one, and it is sharp.

## Holds (in HOLDS.txt)
- **H1** (medium, test): add the sharp control `flux_sharp_zero_overlap_not_certified` on Z2 2×1 and 3×1.
- **H2** (medium, test): add the sabotage name `visibility_error_halved`.
- **H3** (medium, test): that sabotage halves `error_num` in `exact_vector_visible`.
- **H4** (medium, workflow): add a `read_sabotage` line for it.
- **H5** (medium, receipt): checks 401 → 403.
- **H6** (medium, note): count 401 → 403, which the workflow's grep needs.
- **H7** (medium, README): count 401 → 403.
- **H8** (medium, note §9): add both controls' measured margins and the sharp control.
- **H9** (low, test): fix the stale comment at line 2397. It says "against 2^100 sin^2 theta", but no line of code compares against 2^100 at this head.

**On patched copies (MEASURED):**
- All 9 OLD texts occur exactly once.
- The full run gives 403 checks, 0 failed, and equals the patched receipt (sha256 `aae6735a…`).
- The new sabotage exits 1, with exactly the 2 sharp checks red.
- flux_wrong_sign, overlap_skips_next, visibility_ignores_omega_error and twist_every_link each keep their named check, with no Traceback.
- The no-float gate output is identical to the head's (failed=0).

## Could not check
- The hosted gate at `2184b54`: this lane is read-only.
- Z2 3×2 exact truth: my root refinement ran past 30 minutes and I stopped it.
- The patched copy under the 8 non-flux sabotages. These reach no changed line (DERIVED), but I did not run them.
- Q8 at 3×1 or larger.
- Z2 weights other than 3, 1 through the full section, because the test's scaling check hard-codes 2^L0.

## Method faults
- One stdin-heredoc Python run, a small patch to my own tool.
- One stray bare `python3 -`, stopped within 2 minutes; it read and wrote nothing.
- One git stash/pop in my own gate clone without `core.autocrlf=false`. The gate had already read the LF files.

Everything is in `C:/tmp/opus55/ym4-03-cert-derivation-20261105/`:
- FINDINGS.txt
- HOLDS.txt
- RESULTS.hbp (with its .sha256)
- SHA256SUMS
- patched/
- tools/
- runs/
- mutants/
- variants/
