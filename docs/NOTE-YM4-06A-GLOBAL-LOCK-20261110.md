# YM4-06A: global-lock structure in three spatial dimensions (finite S3 control, continuous SU(2) comparison)

**Scope: structure only.** This note studies which global constraints lock the flat sectors of a finite-group lattice gauge field in three spatial dimensions, and which of them survive for continuous SU(2). It computes no spectrum, no gap and no transfer-matrix eigenvalue of any Hamiltonian, makes no frozen 3+1D spectral prediction and runs no production lattice. It is separate from issue #6 (YM4-06, the physical mass gap), which stays **OPEN** and untouched. It awaits independent refutation.

Tags: **MEASURED** = a number in [`tests/YM4_06A_GLOBAL_LOCK_RECEIPT.hbp`](../tests/YM4_06A_GLOBAL_LOCK_RECEIPT.hbp) (sha256 `8507584c…1e97`, sidecar beside it), produced by [`tests/test_ym4_06a_global_lock.py`](../tests/test_ym4_06a_global_lock.py); **NAMED** = stated with a written argument or a literature citation, not machine-checked here; **CONJECTURE** = not established.

## Acceptance table

| Item | Status |
|---|---|
| 21 flat S3 sectors on the 3-torus | **Confirmed finite control.** MEASURED: 48 commuting triples, 21 conjugation orbits, by direct orbit count and by Burnside; reproduced on all five lattices from actual flat link configurations (48 tree-fixed flat configurations each, 21 gauge orbits). 2-torus: 18 / 8. |
| Four-face cost 8 | **Explicit periodic links on every lattice size** (MEASURED): one link `U0(000)=(01)`, all others e; four transposition faces, E = 8; Bianchi holds on every cube (rows `S3_FOUR_FACE`, `S3_KAPPA_WITNESS`). |
| Winding cost 3L | **Realized from explicit periodic links** (MEASURED) on all five lattices along all three axes, 15 rows `S3_TUBE`: corner holonomies a=(01), b=(12), one 3-cycle face per transverse slice, E = 3L exactly. The reviewer decides whether this lifts the HOLD. A transposition-flux tube, which passes the local Bianchi check, has **no** periodic link realization (row `FLUX_GATE`): a failed construction, recorded as a finding. |
| κ_3D(L) = min(8, 3·L_min) | MEASURED on 2×2×2, 2×2×3, 2×3×3 (κ = 6) and 3×3×3, 3×3×4 (κ = 8) by a complete search over all nonflat configurations with E < 8. For general L a written argument is given in section 4 (NAMED); the general formula stays **CONJECTURE** until that argument is independently checked. |
| A positive SU(2) lock cost | **Not applicable as a uniform bound.** MEASURED: explicit exact families with action → 0 above the flat set, local and winding (section 5). |
| The 4D physical mass gap | **OPEN** (issue #6). Nothing here bears on it. |

## 1. Set-up (finite S3 control)

Periodic Lx×Ly×Lz cubic lattice, link variables U_μ(x) ∈ S3. Every plaquette holonomy is derived from the links in the repository's convention `U_P = U_μ(x) U_ν(x+μ) U_μ(x+ν)⁻¹ U_ν(x)⁻¹`. Magnetic cost `E(U) = Σ_faces (2 − χ_std(U_P))`, χ_std the 2-dimensional irreducible character, so a face costs 0 (e), 2 (transposition) or 3 (3-cycle). MEASURED (row `S3_CHARACTER`): χ_std = 2, 0, −1 has norm 6/6 and is orthogonal to the trivial and sign characters; the commutator subgroup of S3 is A3 = {e, 3-cycles}.

Gauge fixing: a breadth-first maximal tree is set to e; the residual gauge group is global conjugation, which is identified in every orbit count.

**Bianchi identity, with the correct parallel transport.** For the cube at x with axes 0, 1, 2, loops based at x, a far face carried back to x by the link that leaves x towards it:

```text
B(x) = F01(x)⁻¹ · [U0 F12(x+0̂) U0⁻¹] · F02(x) · [U2 F01(x+2̂) U2⁻¹] · F12(x)⁻¹ · [U1 F02(x+1̂) U1⁻¹]⁻¹ = e
```

MEASURED (rows `S3_FLAT_LATTICE`, `cube_word_free_reduces_to_empty`): on every cube of every lattice this word reduces to the empty word in the free group on the links, so it is e for every configuration; it is also evaluated on pseudo-random configurations and on every witness and minimizer.

## 2. Flat sectors (MEASURED)

- Algebra: commuting pairs 18 → 8 orbits; commuting triples 48 → 21 orbits; Burnside gives 8 and 21 independently (row `S3_FLAT_ALGEBRA`).
- Lattice: the complete solver with every face constrained to e finds exactly 48 tree-fixed flat configurations on each of the five lattices; their axis windings are exactly the 48 commuting triples; 21 gauge orbits. Each algebraic triple is realized by an explicit flat link configuration (corner links).
- 2-torus control, brute force over all 6⁵ = 7,776 (2×2) and 6⁷ = 279,936 (2×3) tree-fixed configurations: 18 flat, 8 orbits, κ_2D = 3; the solver's flat set equals the brute-force set, and its single-face support search reproduces the 72 and 108 minimizers (rows `TWO_TORUS`).

## 3. κ_3D by complete search (MEASURED on the listed lattices)

**Completeness argument.** (i) Every nonflat face costs ≥ 2, so E < 8 forces a nonflat support F with 1 ≤ |F| ≤ 3. (ii) Energy is translation invariant, so it suffices to take one translate of each support (the lexicographically least, which holds a face at the origin). (iii) For each support the solver enumerates every tree-fixed link configuration with all faces outside F equal to e and all faces in F non-identity: an unknown link that is the last open link of a constrained face is fixed by solving the group equation `A·X^s·B = e` exactly; every other unknown is branched over all six elements. Pruning removes a partial assignment only if an already completed face violates its constraint, or if the completed faces of F already cost more than 7 (costs are nonnegative, so this is monotone). Hence every configuration with E < 8 is found. (iv) The search ran **without** any Bianchi prefilter on all five lattices, and again with the prefilter "no cube holds exactly one face of F" (a consequence of B(x) = e); both lists of solutions are identical (`solutions_below_8_equal=1`).

| Lattice | Supports searched (no prefilter) | Solver nodes | κ_3D | Minimizers (tree-fixed / gauge orbits) | min(8, 3·L_min) |
|---|---|---|---|---|---|
| 2×2×2 | 301 | 3,542 | **6** | 54 / 9 | 6 |
| 2×2×3 | 657 | 5,332 | **6** | 36 / 6 | 6 |
| 2×3×3 | 1,470 | 12,162 | **6** | 18 / 3 | 6 |
| 3×3×3 | 3,309 | 26,226 | **8** | — (none below 8) | 8 |
| 3×3×4 | 5,844 | 45,344 | **8** | — (none below 8) | 8 |

Attaining configurations (explicit links, rows `S3_KAPPA_WITNESS`): for κ = 6 a two-face 3-cycle tube along the axis of length 2, e.g. on 2×2×2 faces `P01(000)`, `P01(001)` both 3-cycles; for κ = 8 the one-link four-face configuration `U0(000)=(01)`. The whole receipt replays in about 11 s on one core.

**Reconstruction gate (MEASURED, row `FLUX_GATE`).** On 2×2×2 the arrangement "faces P01(000) and P01(001) both equal to the transposition (01)" passes the local cube check with trivial transport but has no periodic link realization (solver: 0 configurations). The same arrangement with a 3-cycle is realized. This is the global constraint: each transverse 2-torus slice holds one nonflat face, whose holonomy must be a commutator of the slice's windings, and S3's commutators are the 3-cycles. Every cost in this note comes from a link configuration, never from a flux pattern.

## 4. General L (NAMED written argument; the formula stays CONJECTURE)

Read cubes as vertices and faces as edges of the dual lattice, itself periodic cubic with the same sides. By the cube identity no cube holds exactly one nonflat face, so the support F of a configuration with E < 8 is a nonempty edge set with no vertex of degree 1, hence contains a cycle, of length ≤ 3. Between two adjacent dual vertices there are two edges only when that side is 2; a closed dual walk of length 3 with distinct edges must wind a side of length 3. So:

- L_min ≥ 4: no admissible support, κ = 8, attained by the four-face configuration;
- L_min = 3: the only admissible supports with |F| ≤ 3 are length-3 winding tubes, one face per slice, each face a commutator, i.e. a 3-cycle: E = 9 ≥ 8, so κ = 8;
- L_min = 2: admissible supports are two stacked faces along a side of length 2 (a 2-cycle plus an extra edge leaves degree-1 vertices); each slice face is a commutator, so E = 6, attained by the tube.

This gives κ_3D = min(8, 3·L_min) for every L. It is NAMED: written, consistent with every measured lattice, not machine-checked for all L. Per the acceptance rules the general formula is recorded as **CONJECTURE** until an independent reviewer checks or refutes this argument.

## 5. Continuous SU(2) comparison

Exact quaternions are reused from [`tests/test_exact_su2_4d.py`](../tests/test_exact_su2_4d.py) (`quat`, `multiply`, `inverse`, `half_trace`, `all_plaquettes`, `wilson_action`, `gauge_transform`, `covariance_holds`). Cost per face is the SU(2) analogue `2 − Tr U_P = 2(1 − half trace)`.

MEASURED:
- **The SU(2) infimum above the flat set is 0.** One link `U = ((n²−1) + 2n·i)/(n²+1)`, all others 1, on 3×3×3: four nonflat faces, `E_n = 16/(n²+1)` exactly (n = 2, 3, 10, 100, 1000, 10⁶ → 16/5, …, 16/1000000000001). On the repository's 2⁴ lattice with its own Wilson action, `S_W(β=1) = 12/(n²+1)`, unchanged under its gauge transform.
- **No positive winding cost either.** Corner holonomies a_n, b_n on the rational circle about i and j: one face per slice with holonomy [a_n, b_n] ≠ 1 and total E → 0 (n = 2: 3072/625; n = 1000: 1.92·10⁻¹⁰ as an exact ratio).
- **The flat set is a continuous family, not a finite set.** Six commuting triples inside one U(1) give flat configurations (every face exactly 1) with distinct half traces 3/5, 4/5, 15/17, 12/13, 24/25, 60/61, hence pairwise non-conjugate.
- **'t Hooft twisted sector, kept separate (label `TWISTED_n01=1`).** (a, b, c) = (i, j, ±1): ij = −ji, [i, j] = −1; the centralizer of {i, j} is R·1 (exact kernel of the commutator maps), so c = ±1. With twist z_P = −1 on one 01-face per slice these are twisted-flat; read as ordinary periodic configurations they are nonflat (E = 12 on 3×3×3) and are not counted among the periodic flat configurations.

NAMED (cited, not run here):
- Commuting pairs and triples in SU(n) lie in a common maximal torus, so the moduli space of flat SU(2) connections on T³ is (U(1)³)/Z₂, connected, with 8 orbifold points at the central holonomies (±1)³; extra components of commuting triples occur for groups such as Spin(n ≥ 7), not for SU(n). A. Borel, R. Friedman, J. W. Morgan, *Almost commuting elements in compact Lie groups*, Mem. AMS 157 (2002), arXiv:math/9907007; E. Witten, *Toroidal compactification without vector structure*, JHEP 02 (1998) 006, arXiv:hep-th/9712028; V. G. Kac, A. V. Smilga, *Vacuum structure in supersymmetric Yang–Mills theories with any gauge group*, arXiv:hep-th/9902029.
- Twisted boundary conditions and the Z₂ electric/magnetic flux sectors: G. 't Hooft, Nucl. Phys. B153 (1979) 141; Commun. Math. Phys. 81 (1981) 267; P. van Baal, Commun. Math. Phys. 85 (1982) 529.
- The untwisted periodic configuration space SU(2)^links is connected, so it has no discrete sectors.

**What survives for SU(2):** the center symmetry Z₂³ acting on the flat moduli, the topology of the flat moduli space (connected T³/Z₂), and the 't Hooft twisted sectors as separately labeled boundary conditions. **What does not survive:** a positive lock cost κ, and a finite set of flat sectors. The 21 S3 sectors are **not** identified with any SU(2) object (`S3_sectors_identified_with_SU2=0`).

## 6. Planted faults (MEASURED, each exits 1 by name)

| Plant | Fails as |
|---|---|
| the far face xy at x+2̂ used without transport in the cube word | `RED_broken_transport` |
| the a–c commutation condition dropped, so non-commuting triples count as flat | `RED_noncommuting_triple` |
| χ_std(transposition) read as 1 | `RED_wrong_chi` |
| one face dropped from the 2×2×2 lattice | `RED_dropped_face` |
| flat configurations counted without the conjugation identification (48 for 21, 18 for 8) | `RED_missing_gauge_orbit` |
| the transposition tube claimed as a cost-4 excitation from its flux pattern | `RED_unreconstructible_flux` |
| the twisted (i, j, 1) configuration put in the periodic flat list | `RED_twisted_as_periodic` |

## 7. Gate, CI, reproduction

- `python3 -I -X utf8 scripts/no_float_gate.py .` passes with the new file tracked; integers and reduced integer pairs only, no `fractions`.
- CI: [`.github/workflows/ym4-06a-global-lock.yml`](../.github/workflows/ym4-06a-global-lock.yml) runs the gate, checks the receipt sidecar, replays the receipt byte for byte, reads the key rows and runs the seven plants.
- Reproduce: `python3 -I -B -X utf8 tests/test_ym4_06a_global_lock.py | cmp - tests/YM4_06A_GLOBAL_LOCK_RECEIPT.hbp` (Linux line endings; measured byte-identical on WSL Python 3.12.3).

## 8. Open

- An independent check or refutation of the section 4 argument for all L.
- Lattices beyond 3×3×4 by the same search (cheap; not run here).
- Anything spectral: transfer-matrix gaps of the S3 or SU(2) Hamiltonians, uniformity in volume and spacing, and issue #6 all stay **OPEN**.
