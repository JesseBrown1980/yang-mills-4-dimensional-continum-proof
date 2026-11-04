# Four-dimensional continuum proof-obligation ledger

Updated 2026-11-03. Each row covers exactly its own statement, and the Clay problem is the whole chain. Every row is independently auditable. The IDs YM4-02 to YM4-06 match issues #2 to #6.

| ID | Issue | Obligation | Status | Required acceptance |
|---|---|---|---|---|
| YM4-00 | | State the four-dimensional Euclidean SU(2) Wilson model and conventions | PROVED: definition | Orientation, finite Haar measure and gauge law checked |
| YM4-01 | [PR #1](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/1) | Exact local gauge covariance of four-dimensional plaquettes and Wilson action | PROVED algebraically; EXACT-TEST on 2⁴ torus; independent review OPEN | Independent source audit; negative controls; CI |
| YM4-02 | [#2](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/2) | Finite Wilson measure, reflection positivity, correlation setup and transfer matrix | Partition-function existence and positivity PROVED by compactness, for β≥0 and finitely many links. YM4-02a: the β = 0 moments DERIVED, their incidence hypotheses EXACT-TEST. YM4-02b: finite subgroups average exactly as Haar through a fixed degree per link, in [Lemma 0003](LEMMA-0003-SUBGROUP-DESIGNS.md), with its side-1 limits stated. Reflection positivity, correlation setup and the transfer matrix OPEN for this construction | Issue #2's five tests, including matching precise conventions to the established Osterwalder–Seiler theorem |
| YM4-03 | [#3](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/3) | Explicit gauge-covariant one-scale blocking and exact measure pushforward | OPEN | Pin a one-scale identity and induced effective action |
| YM4-04 | [#4](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/4) | Uniform nonperturbative localized effective-action and cluster estimates across all scales | OPEN, the central bottleneck | Named summable constants and small- and large-field control |
| YM4-05 | [#5](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/5) | Nontrivial ultraviolet zero-spacing and infrared infinite-volume limits, Osterwalder–Schrader axioms and physical reconstruction | OPEN | Continuum correlations, control of scale, volume and order of limits, the precise reconstructed field algebra and Wightman properties |
| YM4-06 | [#6](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/6) | Physical mass gap Δ>0 in the reconstructed theory | OPEN | Rigorous positive bound in physical units across the limiting process |
| YM4-07 | | Extension to all compact simple gauge groups | OPEN | Proof for all G, or an explicit restricted scope |
| YM4-08 | | Independent mathematical audit of the entire proof chain | OPEN | Independent reproducible proofs and accepted assumptions |

**Numbering, corrected November 3 so that the ledger and the issues agree.** The old ledger rows map as follows: old YM4-02 and YM4-03 are now YM4-02, old YM4-04 is YM4-03, old YM4-05 is YM4-04, old YM4-06 and YM4-07 are YM4-05, old YM4-08 is YM4-06, old YM4-09 is YM4-07, and old YM4-10 is YM4-08.

## The scope of each kind of result

- The finite-lattice SU(2) Wilson action is the starting model. Continuum existence is the OPEN row YM4-05.
- A finite S₃ Hamiltonian result holds for S₃ in two spatial dimensions. This ledger's subject is continuous SU(2) in four dimensions.
- Q8, 2T, 2O and 2I are finite models inside SU(2). Anything carried from them to continuous SU(2) needs its own bounded argument.
- Four-dimensional Euclidean lattice gauge invariance is a baseline test. Its scope is covariance on the lattice, and evidence for a physical gap belongs to YM4-06.
- If a positive lattice gap is found, bounding it in physical units and proving its behavior under a→0 belongs to YM4-06.

## Next concrete proof task

Finish YM4-02: match the finite Wilson measure to reflection positivity and the transfer matrix, as issue #2 sets out. Then YM4-03: formulate an **exact gauge-covariant one-block renormalization identity** for D=4 SU(2), showing that integration over fine links induces an invariant effective action on coarse links. Pin the blocking map, Haar conventions and precise formula. Test tractable finite-volume controls, then state separate estimates needed for infinitely many scales, weak coupling, and the actual continuum limit.

### Starting primary sources

- Clay/Jaffe–Witten: https://www.claymath.org/millennium/yang-mills-the-maths-gap/ and https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf
- Osterwalder–Seiler (1978): https://doi.org/10.1016/0003-4916(78)90039-8
- Historical constructive RG direction: Balaban, four-dimensional lattice gauge fields; precise theorems to be matched before use.

**Gating rule:** a row can be promoted only with a pinned statement, hypotheses, proof or receipt, known limitations, and independent checking. FAIL, INCONCLUSIVE and RETRACTED results remain visible.
