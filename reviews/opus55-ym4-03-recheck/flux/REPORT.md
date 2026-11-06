**Head checked:** `b577fa83ac5a3e84f27709cbd73b3c54afe605c5`, at the start and at the end. The worktree is clean and holds no `__pycache__`. No process of this lane is still running.

**Verdict:** two of the five e = 0 rows certify a vector whose exact value is 0. The certificate itself survives. 30 holds, H1 to H30, are filed; they apply cleanly and the patched copy reads 399 checks with 0 failed.

## What I ran
- **The full test, on Python 3.13.14:** 306 s. Its output equals `tests/ONE_SCALE_BLOCKING_RECEIPT.txt` byte for byte: 362 checks, 0 failed, 7 misses. **MEASURED.** The owning gate also passed: `gh` reads `one-scale-blocking` as success at b577fa8 (run 42064092543, 28m32s). **MEASURED.**
- **A diagnostic copy of the flux section:** levels, Perron rounds, epsilon, the slack term at each n, and the size of each centered vector. Its 33 rows equal the receipt's.
- **Code of my own**, sharing nothing with the test:
  - Z2 in the basis of closed electric chains (no gauge orbits).
  - Q8 in invariant coordinates (A, P, Q), cross-checked against a per-link convolution over all 8⁴ configurations.
  - Spectra from exact characteristic polynomials (modular Hessenberg with CRT, Yun's factorization, Descartes on Taylor shifts).
  - Shares from E = g(S)/g(λ) applied to exact moments.
- **Exact quaternions** for the winding-parity rows.
- **A Rust 1.81 lattice sum** with no transfer matrix (clippy `-D warnings` exit 0).
- **72 mutants** of `section_flux`, then the holds applied to a copy and rerun.
- **The workflow's pin and sabotage lines** on a clone of the head and on the patched clone.
- **GPT-6's 2 comments on PR 29** were read; no token-like strings in them.

## Refuted
1. **Two e = 0 rows read the leftover error of u, not their named vector. HIGH.** Rows `first_excited_visible_Z2_2x1` and `_Z2_3x1`, and the note's §9 values "1.00000 … 1.00000".
   - DERIVED: with transverse side 1, the winding W₀ gives F S F = 2^(−L₀) S on e = 0, so F T^b F Ω is an exact multiple of Ω and its centered part is 0.
   - MEASURED: the ratio is exactly 1/4 on 2×1 and 1/8 on 3×1, both on my own matrices and on the test's own `Transfer`.
   - MEASURED: the squared relative size of the centered vector the test certifies equals the Perron error bound sin²θ: 2^−1895 and 2^−1435. It falls as the iteration count of u rises:

     | iterations of u | 60 | 120 | 240 | 480 |
     |---|---|---|---|---|
     | Z2 2×1 (log₂) | −479 | −950 | −1895 | −3784 |
     | Z2 3×1 (log₂) | −362 | −719 | −1435 | −2867 |

     On 2×2 and 3×2 it stays at −3 and −2 at every iteration count.
   - What stands: with W₁ the first excited state is reached. Shares are 1.000000000000000 on 2×1 (forced, since e = 0 has dimension 2) and 0.755676415560191 on 3×1.
2. **`of_multiplicity_2` on all five e = 0 rows counts the ground state.** The true multiplicity is 1 on all five (own polynomials). **MEASURED.**
3. **`flux_full_gap_is_the_min` compares a value with itself and cannot fail.** Mutants D03 and D04 move the printed flux ratios by 772812 and 883142 ppm while it stays green. **MEASURED.**
4. **Empty sectors are skipped with no check.** With z = identity, an identity orbit map, or a twist on every μ link (Z04, Z05, Z06), flux rows vanish with 0 checks red. `flux_sectors_span` reads only the sum of dimensions. **MEASURED.**
5. **`overlap_skips_next` fires on the low ≤ high consistency check alone.** It turns 14 of 20 rows red. A certificate that errs low passes it: C06, C07, C08, C10 and D08 all leave it green. **MEASURED.**
6. **The quaternion parity row compares against its own `minus`.** Setting minus = 1 (W01) leaves every row byte for byte. **MEASURED.**
7. **`t2_is_a_design_of_degree_5` reads only real parts.** D23 and D26 leave the rows byte for byte. The claim itself is true: 0 monomials of degree ≤ 5 differ from their S³ moments, and 20 of 84 differ at degree 6. **MEASURED.**
8. **Note §4, "Δ_full exactly when these levels stay visible":** only the level that sets Δ_full needs to stay visible. **DERIVED.**
9. **Prop. 7a item 2, "changes sign":** this holds in a representation where z acts as −1. **DERIVED.**
10. **A code comment cites a 2^−200 bound that no line of code uses.**

## Survives
- **The certificate.**
  - Each scale is right at 2^shift.
  - The inner product is the one under which S is self-adjoint; K is symmetric on all 20 sector pencils.
  - T ≥ 0 enters only through the bound on the other eigenvalues. next_high = 0 occurs on exactly two rows: on Z2 2×1 e = 0 no other eigenvalue exists (dimension 2); on Q8 e = 0 the other 78 eigenvalues are exactly 0 (factor x⁷⁸).
  - The degenerate top on Q8 e = (−1,−1) is exact: 19968 with multiplicity 4.
  - All 44 level brackets agree with my own exact root counts.
- **The slack.** At n = 64 the ground term is 2^−1392, 2^−1200, 2^−1054, 2^−1025 and 2^−1703, against one unit of 10⁻⁹. The step from the computed vector to the exact one moves a share by less than 2^−690 for one insertion.
- **The Perron vector.** Rounding ran only on Z2 3×2 (51 rounds), and it keeps the vector exactly even. Each model needs about 70 to 74 iterations; the test runs 240.
- **The Q8 sectors are 80/32/32/32**, by an F₂-symplectic count and by a second route. z is right for both groups.
- **Digits.** All 15 e ≠ 0 shares and the 3 genuine e = 0 shares lie inside their receipt brackets, and the note's 5-digit values agree. Δ_flux < Δ₀ on all five lattices.
- **The definitions.** Twisted 3D lattice sums equal the sector traces 20 of 20, exactly; this includes Q8 over 8¹⁰ configurations.
- **Winding parity.** 64/64 and 96/96 on exact quaternions, and in directions 1 to 3.
- **On the Z2 misses.** Every even single coarse function on coarse side 1 is constant, as the note says. At coarse side 2, a single even insertion does reach the first excited state: shares 0.6385 (2×2) and 0.2986 (3×2).
- **Workflow.** The pins pass, and they equal the rows at 3db4313. The three new sabotages fire 2, 41 and 14 checks, the same counts as the hosted log.
- **Mutation, 72 mutants.** 38 were killed on a named check, 15 were caught only by cmp, 13 left every row byte for byte, 4 crashed and 2 hit the time limit. With the holds, 12 of the 14 targeted mutants turn a named check red. The table is in `mutants/mutant_table.txt`.

## Holds (in `HOLDS.txt`)
- H1 (high) test: check that each two-insertion vector stands above u's error, take the next winding when it does not, and add a check that W₀ scales S on side 1.
- H2 (medium) test: subtract the ground from the e = 0 multiplicity.
- H3, H4 (medium) test: replace the tautology with cross-sector entries, the span, and the second value on the whole orbit space.
- H5 (medium) test: check that every sector is nonempty.
- H6 (medium) test: bracket width at most 2000 units of 10⁻⁹.
- H7 (medium) test: closed form on Z2 2×1, e = (1,−1).
- H8 (low) test: ground check at the falsifier's "at or above".
- H9 (low) test: the stale comment.
- H10 (low) test: 2T monomials against S³.
- H11 (low) test: the twist must change the holonomy.
- H12 (high) note: the e = 0 shares and which F gives each.
- H13 (medium) note: the flux row's block factors and weights.
- H14 (medium) note: Q8's margin and T's rank 2 on e = 0.
- H15 (medium) note: count to 399.
- H16 (medium) note: the mutation sentence.
- H17 (low) note: the first read's e = 0 rows.
- H18 (low) note: Prop. 7a, which representation.
- H19 (low) note: the level that sets Δ_full.
- H20 (medium) README: count to 399.
- H21 (medium) prediction: a correction row after row 45.
- H22 (medium) workflow: the sabotage's named check becomes `overlap_closed_form`.
- H23 (low) note: 2T as a design, in the table.
- H24 to H30 (medium) receipt: the seven lines the patched test prints.

Applying all 30 reproduces the patched test and its receipt byte for byte. On the patched clone: 399 checks, 0 failed, pins pass, gate exit 0, and each sabotage fires its named check.

## Could not check
- The hosted run's Python version; its log does not print it.
- The eight older sabotages on the patched copy. Flux code reads only its own three sabotage names, so they cannot reach the changed code.
- Larger Q8 or Z2 lattices, and other weights.
- Theorem 13, Theorem 14 and §7a beyond where the flux rows touch them.

Two method faults on record, neither touching a result: one bare-`python3` REPL, which I stopped; and a first clone that took CRLF from the system gitconfig and failed the pins. I re-cloned with `autocrlf=false`. The pins depend on LF bytes, and the repo has no `.gitattributes`.

Everything is in `C:/tmp/opus55/ym4-03-recheck-flux-20261105/`:
- `FINDINGS.txt`
- `HOLDS.txt`
- `runs/`
- `own/`
- `tools/`
- `mutants/`
