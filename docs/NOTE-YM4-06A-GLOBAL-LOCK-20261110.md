# YM4-06A: global-lock structure in three spatial dimensions (finite S3 control, continuous SU(2) comparison)

**Scope: structure only.** This note studies which global constraints lock the flat sectors of a finite-group lattice gauge field in three spatial dimensions, and which of them survive for continuous SU(2). It computes no spectrum, no gap and no transfer-matrix eigenvalue of any Hamiltonian, makes no frozen 3+1D spectral prediction and runs no production lattice. It is separate from issue #6 (YM4-06, the physical mass gap), which stays **OPEN** and untouched. An independent refutation attempt (opus55, `REFUTE-YM4-06A`, receipt sha256 `f285713d…4eb3`, on head `19ecf72`) refuted nothing; its wording and plant repairs are applied here.

Tags: **MEASURED** = a number in [`tests/YM4_06A_GLOBAL_LOCK_RECEIPT.hbp`](../tests/YM4_06A_GLOBAL_LOCK_RECEIPT.hbp) (sha256 `3752eeb1…00d8`, sidecar beside it), produced by [`tests/test_ym4_06a_global_lock.py`](../tests/test_ym4_06a_global_lock.py); **DERIVED** = proved by the written argument given here, each step either machine-checked on the listed lattices or a short lemma written out in full, and checked by the independent refuter; **NAMED** = stated with an argument or a literature citation, not machine-checked here; **CONJECTURE** = not established.

## Acceptance table

| Item | Status |
|---|---|
| 21 flat S3 sectors on the 3-torus | **Confirmed finite control.** MEASURED: 48 commuting triples, 21 conjugation orbits, by direct orbit count and by Burnside; reproduced on all 13 lattices from actual flat link configurations (48 tree-fixed flat configurations each, 21 gauge orbits). 2-torus: 18 / 8. |
| Four-face cost 8 | **Explicit periodic links on every lattice size** (MEASURED): one link `U0(000)=(01)`, all others e; four transposition faces, E = 8; Bianchi holds on every cube (rows `S3_FOUR_FACE`, `S3_KAPPA_WITNESS`). |
| Winding cost 3L | **Realized from explicit periodic links** (MEASURED) on all 13 lattices along all three axes, 39 rows `S3_TUBE`: corner holonomies a=(01), b=(12), one 3-cycle face per transverse slice, E = 3L exactly. The refuter re-evaluated the first 15 tubes with its own code and states the HOLD can lift on realization. That the minimum over **every** winding configuration is 3L is NAMED (section 4), not machine-checked. A transposition-flux tube, which passes the local Bianchi check, has **no** periodic link realization (row `FLUX_GATE`): a failed construction, recorded as a finding. |
| κ_3D(L) = min(8, 3·L_min) | **DERIVED for every periodic lattice with all sides ≥ 2** (section 4, with repairs (a)–(d) of the refutation). MEASURED here on 13 lattices by a complete search over all nonflat configurations with E < 8: κ = 6 on 2×2×2, 2×2×3, 2×3×3, 2×2×4, 2×3×4, 2×4×4, 2×5×5 and κ = 8 on 3×3×3, 3×3×4, 3×3×5, 3×4×4, 3×5×5, 4×4×4. The refuter's independent global branch-and-bound gives the same values on the same 13 lattices. |
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
- Lattice: the complete solver with every face constrained to e finds exactly 48 tree-fixed flat configurations on each of the 13 lattices; their axis windings are exactly the 48 commuting triples; 21 gauge orbits. Each algebraic triple is realized by an explicit flat link configuration (corner links).
- 2-torus control, brute force over all 6⁵ = 7,776 (2×2) and 6⁷ = 279,936 (2×3) tree-fixed configurations: 18 flat, 8 orbits, κ_2D = 3; the solver's flat set equals the brute-force set, and its single-face support search reproduces the 72 and 108 minimizers (rows `TWO_TORUS`).

## 3. κ_3D by complete search (MEASURED on the listed lattices)

**Completeness argument.** (i) Every nonflat face costs ≥ 2, so E < 8 forces a nonflat support F with 1 ≤ |F| ≤ 3. (ii) Energy is translation invariant, so it suffices to take one translate of each support (the lexicographically least, which holds a face at the origin). (iii) For each support the solver enumerates every tree-fixed link configuration with all faces outside F equal to e and all faces in F non-identity: an unknown link that is the last open link of a constrained face is fixed by solving the group equation `A·X^s·B = e` exactly; every other unknown is branched over all six elements. Pruning removes a partial assignment only if an already completed face violates its constraint, or if the completed faces of F already cost more than 7 (costs are nonnegative, so this is monotone). Hence every configuration with E < 8 is found. (iv) The search ran **without** any Bianchi prefilter on all 13 lattices, and again with the prefilter "no cube holds exactly one face of F" (a consequence of B(x) = e); both lists of solutions are identical (`solutions_below_8_equal=1`).

| Lattice | Supports searched (no prefilter) | Solver nodes | κ_3D | Minimizers (tree-fixed / gauge orbits) | min(8, 3·L_min) |
|---|---|---|---|---|---|
| 2×2×2 | 301 | 3,542 | **6** | 54 / 9 | 6 |
| 2×2×3 | 657 | 5,332 | **6** | 36 / 6 | 6 |
| 2×3×3 | 1,470 | 12,162 | **6** | 18 / 3 | 6 |
| 3×3×3 | 3,309 | 26,226 | **8** | — (none below 8) | 8 |
| 3×3×4 | 5,844 | 45,344 | **8** | — (none below 8) | 8 |
| 2×2×4 | 1,165 | 8,323 | **6** | 36 / 6 | 6 |
| 2×3×4 | 2,601 | 20,468 | **6** | 18 / 3 | 6 |
| 2×4×4 | 4,621 | 43,522 | **6** | 18 / 3 | 6 |
| 2×5×5 | 11,254 | 120,486 | **6** | 18 / 3 | 6 |
| 3×3×5 | 9,123 | 69,563 | **8** | — | 8 |
| 3×4×4 | 10,377 | 98,618 | **8** | — | 8 |
| 3×5×5 | 25,317 | 279,121 | **8** | — | 8 |
| 4×4×4 | 18,445 | 209,589 | **8** | — | 8 |

The last eight are the refuter's extra lattices. The refuter searched them first with a different method: one global depth-first branch-and-bound over every free link, a comb tree, no support enumeration, no translation reduction and no prefilter. It found κ = 6 on the four with a side 2 and no configuration with E ≤ 7 on the other four. This receipt reproduces those values with the support method. The two methods, written in codes that share nothing, agree on all 13 lattices (independent evidence, MEASURED).

The refuter's report, receipt (`REFUTE-YM4-06A.hbp`, sha256 `f285713d3848ea0879ad08152b5ef03173b846a9b8a222d4b17de39a50934eb3`), scripts with their sidecars, and run outputs are filed unedited in [`reviews/opus55-ym4-06a-refute-20261110/`](../reviews/opus55-ym4-06a-refute-20261110/). The refuter's manifest `REFUTER-MANIFEST.hbp` (sha256 `58353d3c172c86b5bd52bc769758dc56ca44fec8c0a224085ed87ea0067bbb15`) was filed alone, in commit `77062d8`, before any of its files. It lists all 44 top-level files with path, byte count and full sha256, and every filed file matches it. `aux.hbp` is filed as `aux_output.hbp` with its bytes unchanged, because AUX is a reserved device name on Windows (`FILED.hbp`). A CI wrapper (`tests/ym4_06a_verify_refuter_manifest.sh`) checks every file against the manifest and the manifest's own sha256 against the recorded value, and reruns the refuter's code against its own outputs (support lemma; budget 7 on 2×2×2, 2×2×3, 2×3×3, 3×3×3, 3×3×4) in wrapper steps. The refuter's three scripts pass the no-float gate as they are, without a pin.

Attaining configurations (explicit links, rows `S3_KAPPA_WITNESS`): for κ = 6 a two-face 3-cycle tube along the axis of length 2, e.g. on 2×2×2 faces `P01(000)`, `P01(001)` both 3-cycles; for κ = 8 the one-link four-face configuration `U0(000)=(01)`. The whole receipt replays in about 3 minutes on one core.

**Reconstruction gate (MEASURED, row `FLUX_GATE`).** On 2×2×2 the arrangement "faces P01(000) and P01(001) both equal to the transposition (01)" passes the local cube check with trivial transport but has no periodic link realization (solver: 0 configurations). The same arrangement with a 3-cycle is realized. This is the global constraint: each transverse 2-torus slice holds one nonflat face, whose holonomy must be a commutator of the slice's windings, and S3's commutators are the 3-cycles. Every cost in this note comes from a link configuration, never from a flux pattern.

## 4. General L (DERIVED for every side ≥ 2)

GPT-6's general argument (PR #47, comment 6768787639) covers every periodic cubic lattice with every side ≥ 2, in five steps:
1. A face costs ≥ 2, so E < 8 means at most 3 nonflat faces.
2. Bianchi forbids a cube with exactly one nonflat face, so the support contains a dual cycle.
3. A cycle of ≤ 3 dual edges is a winding 2-cycle along a side of length 2 or a winding 3-cycle along a side of length 3.
4. On each slice the single face is conjugate to a commutator, which in S3 is a 3-cycle, at cost 3.
5. So those costs are 6 and 9, and the one-link transposition attains 8.

The refuter's repairs (a)–(d) write out each step, as follows.


**(a) Hypothesis.** Every side satisfies L_x, L_y, L_z ≥ 2. A side of length 1 lets a face share links with itself and a cube hold the same face twice; that case is excluded and not treated. Under the hypothesis each face has four distinct links, each link lies on exactly four faces, and each face bounds exactly two distinct cubes (MEASURED by the geometry checks on every listed lattice).

**Step 1 (face cost).** 2 − χ_std ∈ {0, 2, 3}, and it is 0 only at e. So a nonflat configuration with E < 8 has a nonflat support F with 1 ≤ |F| ≤ 3.

**Step 2 (no cube holds exactly one nonflat face).** The based, transported cube word B(x) of section 1 reduces to the empty word, so B(x) = e for every configuration. If five of a cube's six faces are e, B(x) is a conjugate of the sixth face's holonomy or of its inverse, so the sixth is e too.

**Step 3 (dual graph).** Take cubes as vertices and faces as edges of the dual lattice, itself a periodic cubic lattice with the same sides. By Step 2, F is a nonempty edge set with no vertex of degree 1. Such an edge set contains a cycle, and this cycle has length ≤ |F| ≤ 3.

**(d) No short cycle unless a side is 2 or 3.** A cycle of length k ≤ 3 is a closed walk of k unit steps ±e_μ along distinct edges. Lift it to Z³ by summing the steps. It closes in the torus, so its displacement is (n_x L_x, n_y L_y, n_z L_z).
- **Zero displacement.** The lift is a closed walk in Z³. Z³ is bipartite (by the parity of x+y+z), so k is even, i.e. k = 2. A closed 2-step walk in Z³ goes out along one edge and back along the same edge, so it is not a cycle with distinct edges.
- **Nonzero displacement.** Some n_μ ≠ 0 needs at least L_μ steps along μ, so L_μ ≤ k ≤ 3.
  - k = 2: both steps go the same way along μ and L_μ = 2. This is the pair of stacked faces normal to μ at the same transverse position; they are distinct edges between the same two cubes exactly when L_μ = 2.
  - k = 3, all three steps along μ: L_μ = 3, a straight tube of three faces.
  - k = 3, two steps along μ covering L_μ = 2: the third step leaves a displacement of ±1 in another direction, which is not a multiple of a side ≥ 2, so the walk does not close.

So the admissible supports with |F| ≤ 3 are exactly the straight 2-face stacks along a side of length 2 and the straight 3-face tubes along a side of length 3. A 2-cycle plus one more edge leaves vertices of degree 1, and a triple edge cannot occur, since two cubes share at most two faces.

This census was machine-checked by the refuter on all 20 side triples in {2, 3, 4, 5}³, enumerating every face set with |F| ≤ 3. The admissible sets are exactly these, and 20/20 agree (`support_lemma.hbp` in `REFUTE-YM4-06A`). In this receipt the `supports_bianchi_admissible` counts (up to translation) are 3, 3, 3, 3, 2, 2, 2, 1, 1, 2, 1, 1, 0 on the 13 lattices, which is the number of sides equal to 2 or 3 in each case.

**(c) Punctured-torus commutator lemma.** Let a straight tube run along axis ρ, so each transverse 2-torus slice T (x_ρ fixed) contains exactly one nonflat face f, with holonomy h_f.
1. Restrict the field to the links of T.
2. T with f removed is a punctured torus. It deformation-retracts onto a wedge of two circles: the two winding loops, based at the corner of f. Its boundary loop is the commutator of those two loops.
3. Every face of T other than f is e, so the restricted field is flat on the punctured torus. Its holonomy around the boundary of f is therefore the commutator [a, b] of the two slice windings a, b.
4. The holonomy around the boundary of f is h_f up to conjugation (the choice of base point and orientation).

Hence h_f is conjugate to [a, b], which lies in [S3, S3] = A3 = {e, 3-cycles}. Since f is nonflat, h_f is a 3-cycle and costs 3. MEASURED consistency: in every 2-torus brute force a single nonflat face is always a 3-cycle (κ_2D = 3), and the transposition stack has no periodic link realization (row `FLUX_GATE`).

**Conclusion.** With every side ≥ 2:
- **L_min ≥ 4:** there is no admissible support, so no nonflat configuration has E < 8. κ = 8, attained by the one-link four-face configuration.
- **L_min = 3:** the only admissible supports are 3-face tubes along a side of length 3. Each slice face is a 3-cycle by (c), so E = 9 ≥ 8, and κ = 8.
- **(b) L_min = 2:** the admissible supports are the 2-face stacks along a side of length 2, each costing 2·3 = 6 by (c) and realized by the tube. When another side is 3 there are also the 3-face tubes along that side, costing 9. Nothing goes below 6, so κ = 6.

Hence **κ_3D = min(8, 3·L_min) for every periodic lattice with all sides ≥ 2 (DERIVED).**

A separate statement is **NAMED only**: that the minimum of E over every configuration with a nontrivial winding flux is 3L (one 3-cycle per slice by (c), or at least two nonflat faces in some slice, costing at least 4). It is not machine-checked and is not used for κ.

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

Each plant has a first check and an independent named backup. For each plant the first check was removed in a local copy and the run repeated: the backup still fails by the plant's own name (repair (e) of the refutation). MEASURED: 8 of 8, rows in [`tests/YM4_06A_BACKUP_PROBES.hbp`](../tests/YM4_06A_BACKUP_PROBES.hbp) with its sidecar.

| Plant | First check | Backup check (same name) |
|---|---|---|
| `broken_transport`: the far xy face used without transport in the cube word | the cube word does not reduce to the empty word | the cube product is not e on pseudo-random configurations |
| `noncommuting_triple`: the a–c commutation condition dropped | the count is not 48 / 18 | every counted tuple must commute pairwise, read straight from the permutations |
| `wrong_chi`: χ_std(transposition) read as 1 | norm and orthogonality of χ_std | face costs must be exactly 0, 2, 3 |
| `dropped_face`: one face dropped from the 2×2×2 lattice | face count, and four faces per link | every face of every cube is a lattice face and bounds exactly two cubes |
| `missing_gauge_orbit`: flat configurations counted without conjugation | the 2-torus orbits must be 8 | the 3D orbits must equal the Burnside count 21 |
| `unreconstructible_flux`: the transposition tube claimed as a cost-4 excitation | the reconstruction solver finds no periodic links | the claim must carry a link configuration whose derived faces equal its flux pattern |
| `twisted_as_periodic`: the twisted (i, j, 1) configuration put in the periodic flat list | every face of a periodic flat configuration is exactly 1 | the axis windings of a periodic flat configuration commute pairwise (here ij = −ji) |
| `incomplete_solver` (eighth plant, repair (f)): the solver never branches on the last group element | the 2-torus flat set against brute force over all tree-fixed configurations | the 2-torus single-face support search against the brute-force minimizer count |

## 7. Gate, CI, reproduction

- `python3 -I -X utf8 scripts/no_float_gate.py .` passes with the new file tracked; integers and reduced integer pairs only, no `fractions`.
- CI: [`.github/workflows/ym4-06a-global-lock.yml`](../.github/workflows/ym4-06a-global-lock.yml) runs the gate, checks the receipt sidecar, replays the receipt byte for byte, reads the key rows and runs the eight plants.
- Reproduce: `python3 -I -B -X utf8 tests/test_ym4_06a_global_lock.py | cmp - tests/YM4_06A_GLOBAL_LOCK_RECEIPT.hbp` (Linux line endings; measured byte-identical on WSL Python 3.12.3).

## 8. Open

- A machine check of the NAMED statement that every winding configuration costs at least 3L.
- Sides of length 1 (excluded by hypothesis (a)).
- Anything spectral: transfer-matrix gaps of the S3 or SU(2) Hamiltonians, uniformity in volume and spacing, and issue #6 all stay **OPEN**.
