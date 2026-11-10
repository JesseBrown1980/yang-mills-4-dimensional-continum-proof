# REFUTE-YM4-06A: independent refutation attempt of PR #47 (head 19ecf72)

The refuter is opus55, the second seat of ACER-CLAUDE-FABLE5 (pid 8467a937cba309f7). Date: 2026-11-10. This is the narrative copy. The hot-path receipt is `REFUTE-YM4-06A.hbp`, sha256 `f285713d3848ea0879ad08152b5ef03173b846a9b8a222d4b17de39a50934eb3` (its sidecar sits beside it). Rule changes for exact-integer work beyond the remainder carry are out of scope.

Scope: structure only. No spectrum or gap was computed. No GitHub writes were made. Nothing was imported from the PR. Arithmetic is integer only: no float and no `fractions`.

Scripts (own code, sidecars beside them): `refute_s3.py`, `refute_aux.py`, `refute_support_lemma.py`.

## Verdicts

| # | Claim | Status |
|---|---|---|
| 1 | 21 flat S3 sectors on T³, 8 on T² | **CONFIRMED** (MEASURED) |
| 2 | κ_3D = 6, 6, 6, 8, 8; minimizers 54/9, 36/6, 18/3 | **CONFIRMED** (MEASURED), and extended to 8 more lattices |
| 3a | Flux gate: the transposition stack is not realizable, the 3-cycle stack is | **CONFIRMED** (MEASURED) |
| 3b | §4 general-L argument | **CONFIRMED_WITH_NOTE**. Every step is correct. I found no counterexample. Wording repairs are listed below. |
| 4 | SU(2) families, U(1) flat set, twisted sector kept separate | **CONFIRMED** (MEASURED) |
| 5 | 7 plants | **CONFIRMED_WITH_NOTE**: 7/7 exit rc=1 by name, and none is caught only incidentally. There are weak points (see below). |
| 6 | Receipt byte-identical, sha256 8507584c… | **CONFIRMED** (MEASURED). The replay matches byte for byte (`cmp` identical) on WSL Python 3.12. CI shows 10/10 required checks passing. |

## Method for κ (different from the PR)

The PR enumerates supports, takes them up to translation, and solves each one. I used a different method:

- **Gauge fixing:** a comb maximal tree, with spanning checked by union-find.
- **Search:** one global depth-first branch-and-bound over all 2N+1 free links of the whole lattice. The link order is greedy and static. Every completed face adds its exact cost, and a branch is cut when the running cost exceeds the budget.
- **What it leaves out:** support enumeration, translation reduction and the Bianchi prefilter.

**Completeness:** each face is completed exactly once and costs are at least 0, so the cut is monotone. Every free link is branched over all six values. Every solution is then re-evaluated from scratch. Only 3 branch positions are unconstrained (the windings).

Results (MEASURED):
- Budget 7: κ = 6 on 2×2×2, 2×2×3, 2×2×4, 2×3×3, 2×3×4, 2×4×4 and 2×5×5. No configuration with E ≤ 7 exists on 3×3×3, 3×3×4, 3×3×5, 3×4×4, 3×5×5 or 4×4×4.
- Budget 8: κ = 8 is attained only by four-transposition configurations. On 3×3×3 there are 81 supports (3N one-link excitations) and 432 tree-fixed configurations in 84 orbits per canonical support.
- The canonical-support counts match the PR: 54/9, 36/6, 18/3. The full-lattice gauge-orbit counts are 36, 36, 27.

## §4 general-L argument: every step checked

1. **No cube has exactly one nonflat face.** This follows from the cube identity. MEASURED on every solution with E ≤ 8 on 2×2×2, 2×3×3 and 3×3×3.
2. **The support has at most 3 faces and no vertex of degree 1, so it contains a cycle of length ≤ 3.** I machine-checked this by enumerating every face set with |F| ≤ 3 on all 20 side triples in {2,3,4,5}³. The admissible sets are exactly the straight 2-face stacks along sides of length 2 and the straight 3-face tubes along sides of length 3 (20/20 agree). Sides ≥ 4 add nothing: a closed walk of ≤ 3 steps lifts to Z³, which is bipartite.
3. **A slice with one nonflat face carries a conjugate of [a, b].** This is the punctured-torus lemma, and it is correct. The commutator subgroup of S3 is A3, so that face is a 3-cycle with cost 3.

Hence κ = min(8, 3·L_min) for every lattice with all sides ≥ 2, and κ = 8 is attained by the one-link configuration.

**Repairs needed before the tag moves to DERIVED:**
- (a) State the hypothesis that all sides are ≥ 2.
- (b) The L_min = 2 bullet omits the length-3 tubes (cost 9) that exist when another side is 3. This does not change κ.
- (c) Write out the punctured-torus commutator lemma.
- (d) Write out the bipartite-lift argument for "no triangle unless a side is 3".

**Promotion:** CONJECTURE → DERIVED is justified once (a) to (d) are in the note.

**Winding HOLD:** E = 3L comes from explicit links, 15 of 15 tubes, re-evaluated by my code. The HOLD can lift on realization. A lower bound of 3L for every winding configuration is NAMED here (one 3-cycle per slice, or at least 2 faces costing at least 4), not machine-checked.

## SU(2) (MEASURED, my own rational quaternions)

- 3×3×3 one-link family: E = 16/(n²+1) for n = 2, 3, 10, 100, 1000 and 10⁶.
- 2⁴ Wilson action at β = 1: 12/(n²+1). It is invariant under a rational gauge transform.
- Winding family: 3072/625 at n = 2, then 1920000/104060401 at n = 10, then 1.92·10¹⁴/(n²+1)⁴ at n = 1000. It strictly decreases.
- Six flat U(1) triples with all plaquettes exactly 1. Their half traces are distinct, so they are pairwise non-conjugate.
- Twisted sector: ij = −ji, [i, j] = −1, and the centralizer is R·1. Read as periodic, E = 12 for c = ±1. With the twist, the configuration is twisted-flat.
- Nothing identifies the 21 S3 sectors with SU(2) objects, and no gap or continuum claim is made (checked by grep). Note: my centralizer check is on basis elements only. It is valid here because the images of j and k under [·, i] and [·, j] are independent.

## Plants

All 7 exit rc=1 with the named check. To test each one, I removed its first-firing check in a local copy and reran:
- `wrong_chi`: the second wrong_chi check still fires.
- `broken_transport`: the Bianchi check on random configurations still fires.
- `missing_gauge_orbit`: the 3D comparison against Burnside still fires.
- `noncommuting_triple`: its catch by name is a literal check (48/18). Without it, the plant is caught as `RED_missing_gauge_orbit`.
- `dropped_face`: without the face-count check, it is caught as `RED_four_face`.
- `unreconstructible_flux`: without its check, the run crashes with an IndexError (rc=1, but not by name).
- `twisted_as_periodic`: this has a single detection point. Without it, rc=0.

Repairs:
- Name the independent backup checks.
- Add an eighth plant that breaks solver completeness. The 2D brute-force comparison would catch it.
