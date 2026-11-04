# Lemma YM4-02b: finite subgroups of SU(2) and the Haar integral

**Status:** the statement is a standard fact, written out here for this repository's use with its own reproduction. Its strengths and lattice consequences are MEASURED by an exact integer run, the [second seat's attack](../reviews/opus55-ym4-02b/README.md) is recorded, and review of the whole lemma by a different model is OPEN. **Scope:** finite-lattice moments and the strong-coupling Taylor coefficients of the Wilson lattice. It is a subtask of [YM4-02](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/2).

## Statement

Let G be a finite subgroup of SU(2), and let t+1 be the first n ≥ 1 at which G has a nonzero invariant on the spin-n/2 representation V_{n/2}. Then for every polynomial f of degree at most t on the unit sphere S³ = SU(2),

```text
(1/|G|) sum_{g in G} f(g) = integral f(U) dHaar(U).
```

**Proof.** A monomial of degree k in the entries of U is a matrix coefficient of (ℂ²)^{⊗k}, which Clebsch–Gordan splits into V_{m/2} with m ≤ k. So polynomials of degree at most t on S³ are spanned by the matrix coefficients of V_{n/2} with n ≤ t, and the dimension count Σ_{n≤t}(n+1)² confirms it. For n = 0 both sides agree. For 1 ≤ n ≤ t the Haar integral of a matrix coefficient is 0, and the G-average of the representation is the projector onto its G-invariants, which is 0 by the choice of t. QED.

**Carrying it to a lattice.** Take a finite lattice whose plaquettes each hold four distinct links, which on a periodic lattice means every side is at least 2. Let F be a function of the link variables that is a polynomial of degree at most t in each link, with all others fixed. For SU(2), U⁻¹ is linear in the entries of U, so inverted links count the same. Integrating one link at a time then replaces every Haar integral by the G-average with no error. Each power X^k of X = sum over plaquettes of a_p, with a_p = (1/2) Tr U_p, has degree at most k in each link, so on such a lattice the Taylor coefficients of Z(β) agree for SU(2) and for G through β^t.

**A plane with both sides of length 1.** There a plaquette is U V U⁻¹ V⁻¹, degree 2 in each of its two links, and agreement runs through floor(t/2). The second seat measured this with side 1 in every direction (d = 2, all four groups; Q8 reads E[a²] = 1 against SU(2)'s 1/3) and on 1×1×2 (Q8, 2T) and 1×1×2×2 (Q8).

**Exactly one side of length 1.** A plaquette through that direction is A V B⁻¹ V⁻¹, degree 1 in A and B and 2 in V, and any other plaquette holds four distinct links. Agreement was measured through β^t on 1×2 (Q8, 2T, 2O), on 1×3 (Q8, 2T), and for Q8 on 1×2×2 and 1×2×2×2. Four distinct links is the hypothesis this proof uses, and the sharp condition stays OPEN.

**Beside this, November 4: the periodic 1×L lattice in two dimensions.** There the statement above is a theorem, and the sharp condition stays OPEN in d ≥ 3.

**Theorem (1×L, L ≥ 2).** Let G ⊂ SU(2) be finite, with its uniform average agreeing with Haar through degree t. On the periodic 1×L lattice write P_x = A_x V_x A_{x+1}⁻¹ V_x⁻¹ and a_x = (1/2) Tr P_x. For every monomial with k = Σ_x m_x ≤ t,

E_G[∏_x a_x^{m_x}] = E_{SU(2)}[∏_x a_x^{m_x}] = 2^{−k} Σ_{n=0}^{min_x m_x} ∏_x B(m_x, n) / (n+1)^L,

with B(m, n) = (n+1)/(m+1) · binom(m+1, (m−n)/2) when n ≤ m and m−n is even, and 0 otherwise. So the Taylor coefficients of the Wilson partition function agree with SU(2)'s through order t.

*Proof.* Each A_x has degree m_x + m_{x−1} ≤ k ≤ t, so its G average can be replaced by the Haar integral with every other link fixed. Expand a^m = 2^{−m} Σ_n B(m, n) χ_{n/2}. Schur orthogonality in the A_x gives 0 unless every n_x equals one n, and then

∫ ∏_x dA_x ∏_x χ_{n/2}(P_x) = χ_{n/2}(V_0 V_1 ⋯ V_{L−1})² / (n+1)^L.

So n ≤ min_x m_x, and what remains has degree 2n in each V_x, with 2n ≤ 2 min_x m_x ≤ 2k/L ≤ k ≤ t. So each V_x average is exact too, and the Haar integral of χ_{n/2}² is 1. ∎

The form also gives the Haar values at L = 1, E[a] = 1/4 and E[a²] = 1/3, where each link has degree 2k, the bound reads 2n ≤ 2k, and agreement stops at floor(t/2).

**Status.** DERIVED by the second seat at its recheck, and checked independently by GPT-6, which also derived the closed form: [its report, verbatim](../reviews/gpt6-one-by-l/README.md). MEASURED in [`tests/test_one_by_l_2d.py`](../tests/test_one_by_l_2d.py), by exact group sums on Q8 at L = 2 to 5, 2T at L = 2 to 4, 2O at L = 2 and 3, and 2I at L = 2: all 548 monomials through t equal the form, X^(t+1) differs from Haar in all 10 cases, and at L = 1 agreement stops at floor(t/2) on all four groups. [The prediction](PREDICTION-YM4-02b.hbp) went up first. Two of its sabotage rows missed, and they are recorded beside it.

**What these rows can see of orientation.** The test's two orientation sabotages act on the closing plaquette of its gauge-fixed sum, with V_0 … V_{L−2} = 1: A_{L−1} v A_0⁻¹ v, and A_{L−1} v A_0 v⁻¹. Those two words have one law, and each moves one row only, X⁶ on 1×2 for 2T, from 25/12 to 185/96. Every class of Q8, 2O, 2I and SU(2) is closed under inversion, so there they have the law of the plaquette, and through degree t 2T agrees with SU(2). Among the four groups, only 2T past its strength sees it, since its order-3 and order-6 classes are not inverse-closed. The test pins that value by name. The scope matters on V. The far-A word stays gauge covariant, so it gives 185/96 ungauged as well. With the V inverse dropped from the closing plaquette of the ungauged word, which is outside gauge covariance, SU(2) reads E[a_0 a_1] = −1/32 against 1/16 on 1×2, and Q8, 2T and 2O read the same.

**No plane with both sides of 1: two derivations to check, CONJECTURE.** From the second seat, unread by any seat outside this one. **The claim:** agreement through t holds for every finite G of strength t, on every lattice and every d, exactly when no plane has both sides 1. *Route 1, by characters.* Let A be the links along the side-1 direction and V the rest. A plaquette through that direction has degree 1 in each A, so for k ≤ t each A swaps from G to Haar with V fixed. Expand a_P^m in characters χ_{j_P}, with 2 j_P ≤ m_P. The Haar integral over an A vanishes unless each j_P is at most the sum of the other j at that A, the polygon condition for an invariant. So 4 j_P is at most the total power of the through-plaquettes at that A. Each V lies in exactly one through-plaquette, with degree 4 j_P there, plus other plaquettes that hold it once each. Those are different plaquettes from the through-plaquettes at that A, so their powers add to at most k, the surviving degree in V is at most k ≤ t, and V swaps too, term by term on fixed j_P. *Route 2, with no characters.* Take a maximum-weight spanning forest of the non-loop links, with weight the link's degree in the monomial, and gauge it to 1, which is exact for G and for Haar. A remaining non-loop link e closes a cycle in the forest, and any other link f on that cycle has deg f ≥ deg e. Each plaquette adds at most 2 per power to deg e + deg f, because a through-plaquette holds its one V twice and any other plaquette holds four distinct links. So deg e ≤ k. A loop link has degree at most k exactly when no plaquette holds it twice, which is no plane with both sides 1. Every free link then has degree at most k ≤ t, and the plain degree argument above finishes. *The other direction.* If a plane has both sides 1, the single-plaquette monomial a^k on it reads the 1×1 value, and it first differs at k = floor(t/2) + 1. **Falsifier:** one lattice with no plane of both sides 1 whose first difference comes at k ≤ t. MEASURED support, by the second seat, in [`confirm-last/`](../reviews/opus55-ym4-02b/confirm-last/) and [`read-pr13/`](../reviews/opus55-ym4-02b/read-pr13/): exact sums on the only multisets above the plain degree bound, one sum per pattern of link incidence, give differ = 0 for 2T (296 multisets in 40 patterns) and Q8 (62 multisets in 4 patterns) across 1×2×2, 1×2×3, 1×3×3 and 1×2×2×2, and for 2O (4,634 multisets in 386 patterns) across those and 1×2×4 and 1×3×4. Route 2's degree bound reads 0 violations over all 55,454,945 multisets on 1×2 through 1×5, 1×2×2, 1×2×3, 1×3×3, 1×2×4, 1×2×2×2 and 1×2×2×3, and over 4,526,931 more on 2×2, 3×3, 2×2×2 and 2×2×2×2, in [the rows FABLE5 reran from its source](../reviews/opus55-ym4-02b/read-pr13/FOREST-RERUN.hbp), and its controls fire on the loop links of 1×1, 1×1×1, 1×1×2 and 1×1×2×2. 2I in d ≥ 3 is unmeasured.

**Where a group first departs, on a lattice with four distinct links per plaquette.** For N_p plaquettes,

```text
E_G[X^(t+1)] − E_Haar[X^(t+1)] = N_p · dim(V_{(t+1)/2}^G) / 2^(t+1),
```

so the lattice plaquette series first differs from SU(2)'s at β^t, by the single-plaquette amount in the table below. **Proof.** Only a multiset of plaquettes with degree t+1 on some link can differ, and all its factors then pass through that link. If two or more distinct plaquettes occur, each holds a transverse link no other holds, so right-invariance makes them independent, and the product of their moments, each of order at most t, agrees. Only p^(t+1) differs. (Tr U)^(t+1) holds V_{(t+1)/2} once and lower spins that agree, so p^(t+1) differs by dim(V^G)/2^(t+1), and it enters X^(t+1) with coefficient 1. QED. This run measures it on (ℤ/2ℤ)⁴ for Q8, where the difference is 12 = 96·2/2⁴. The second seat measured it on the 2×2 torus for all four groups.

## The four groups

| Group | Elements | Conjugacy class sizes | Exact through degree t | E[(Tr U)^(t+1)] vs Haar | Single-plaquette ⟨a⟩ first differs at | By |
|---|---:|---|---:|---|---|---|
| Q8 | 8 | 1, 1, 2, 2, 2 | 3 | 4 vs 2 | β³ | +1/48 |
| 2T | 24 | 1, 1, 4, 4, 4, 4, 6 | 5 | 6 vs 5 | β⁵ | +1/7680 |
| 2O | 48 | 1, 1, 6, 6, 6, 8, 8, 12 | 7 | 15 vs 14 | β⁷ | +1/1290240 |
| 2I | 120 | 1, 1, 12, 12, 12, 12, 20, 20, 30 | 11 | 133 vs 132 | β¹¹ | +1/163499212800 |

The script builds each group from doubled unit quaternions over ℤ, ℤ[√2] and ℤ[φ], checks closure, associativity and norms, derives the classes, and sums characters exactly. Haar moments of Tr U are the Catalan numbers.

## What it computes on the four-dimensional lattice

**On (ℤ/2ℤ)⁴, with 96 plaquettes.** [Lemma 0002](LEMMA-0002-HAAR-MOMENTS.md) takes Haar orthogonality as input. Here the moments are computed by group sums, Q8 where every link has degree at most 3 and 2T where it has degree at most 5:

```text
E[X²] = 24    E[X³] = 0    E[X⁴] = 6897/4    (log Z)''''(0) = E[X⁴] − 3 E[X²]² = −15/4
```

E[X⁴] splits into 12 from single plaquettes, 1710 from pairs, and 9/4 from the 24 two-dimensional tori that wrap this side-2 lattice. As a control, using Q8 past its strength gives 6945/4, off by exactly 12. The second seat's group-free polynomial integration on S³ reproduces all three moments, and that is the form issue #2's acceptance test (2) names, since it reads "not substitution of a finite subgroup for Haar".

**Closed surfaces on ℤᵈ through 10 faces,** enumerated as connected sets of distinct plaquettes with every link covered an even number of times:

| d | 6 faces, per site | 10 faces, per site | 10 faces spanning 3 directions | 10 faces spanning 4 directions |
|---:|---:|---:|---:|---:|
| 3 | 1 | 3 | 3 | 0 |
| 4 | 4 | 36 | 12 | 24 |

The 24 bent surfaces, two cubes in different three-dimensional subspaces sharing a face, are the first terms that need all four dimensions. For a connected closed orientable surface with every link covered exactly twice, E[∏a_p] = 2^(−F) · 2^(χ−F): 1/1024 for the cube and 1/262144 for both ten-face shapes. The second seat confirmed the counts by three other algorithms.

**The plaquette series.** On ℤ⁴, and on periodic lattices of side at least 4 through this order,

```text
⟨(1/2) Tr U⟩ = β/4 − β³/96 + 7β⁵/1536 − 31β⁷/23040 + 4451β⁹/8847360 + ...
```

This equals Table 1 of [Denbleyker, Du, Liu, Meurice and Velytsky, arXiv:0807.0185](https://ar5iv.arxiv.org/html/0807.0185), which lists P = 1 − ⟨(1/2) Tr U⟩ with the same β, so its signs are opposite. The β⁹ coefficient splits as 13/4423680 from one plaquette, 5/18432 from the cube and 15/65536 from the ten-face surfaces. Keeping only the 12 flat surfaces gives 3101/8847360, which misses the table, so the coefficient measures the 24 four-dimensional surfaces.

Through β¹⁰ in log Z only these surfaces enter, because a face with spin at least 1, or two overlapping surfaces, first appears at β¹². That step is DERIVED. **The second seat then tested it:** adding what first enters at β¹² reproduces the published β¹¹ coefficient −264883/1486356480 exactly, and adding the 14-face spheres reproduces β¹³, 403651/5945425920, with residual 0. Its [receipts](../reviews/opus55-ym4-02b/README.md) are in this repository.

## Prior work

The statement is known. The values t = 3, 5, 7, 11 are the classical strengths of these groups as spherical designs: [the 600-cell is a spherical 11-design](https://errorcorrectionzoo.org/c/600cell), and [Goethals and Seidel](https://research.tue.nl/en/publications/cubature-formulae-polytopes-and-spherical-designs/) and [Sobolev](https://mathnet.ru/eng/dan26977) treat invariant cubature (these two read through summaries). [Bannai, Navarro, Rizo and Tiep, arXiv:1810.02507](https://arxiv.org/abs/1810.02507), Lemma 8, gives the same moment comparison for SL₂(5) = 2I, read in the PDF: M6 = 5, M8 = 14, M10 = 42, with M_{2k} agreeing for 1 ≤ k ≤ 5 and exceeding for k ≥ 6, which is t = 11 here. On the lattice side, [Petcher's 1981 thesis](https://www.osti.gov/biblio/6124817) compares the binary icosahedral group and SU(2) "to see at what order of inverse bare coupling constant squared their strong coupling expansions differ"; its body is CANNOT_SEE here, so the order it found is unread. [Denbleyker et al.](https://ar5iv.arxiv.org/html/0807.0185) take the series from Balian, Drouffe and Itzykson, Phys. Rev. D 11, 2104 (1975) and D 19, 2514 (1979), and only that citation was read here. A search found no paper stating the degree-per-link corollary itself, which is a limit of the search. The receipts here are this repository's own reproduction.

## Scope

- The lemma gives zero error on the Taylor coefficients through β^t for these lattices. It starts the bounded approximation that [YM4-03](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/3) asks of any use of Q8, 2T, 2O or 2I, and the remainder bound at β > 0 stays OPEN. A crude bound from |X| ≤ N_p depends on the volume.
- It concerns polynomial link averages and the Euclidean Wilson series at β = 0. The Hamiltonian series in the [SU(N) repository](https://github.com/JesseBrown1980/Finite-Universe-SU-N-solved) carry a group-specific electric term, and their relation to SU(2) stays OPEN. S₃ has three involutions and SU(2) has one, so S₃ sits outside this lemma.
- It speaks to strong coupling. [Discrete subgroups of SU(2) have a freezing transition](https://www.arxiv.org/pdf/2201.09625) at larger β, which bounds how far a subgroup can follow SU(2), and the continuum limit needs β → ∞. Reflection positivity, the transfer matrix, the renormalization group, the continuum limit and the physical mass gap stay OPEN in the [ledger](PROOF_OBLIGATIONS.md).

## Reproduce

```bash
python3 -I -X utf8 tests/test_subgroup_designs_4d.py
```

It takes about 20 seconds, uses integers only, and prints the rows in [`tests/SUBGROUP_DESIGNS_RECEIPT.txt`](../tests/SUBGROUP_DESIGNS_RECEIPT.txt). The prediction, [`PREDICTION-YM4-02b.hbp`](PREDICTION-YM4-02b.hbp), was pushed before the code. It records that a scratch run had already seen the design strengths, the 2⁴ moments, the torus and cube values and the series through β⁵, and that the closed-surface counts, the ten-face values, β⁷, β⁹, the first differences and the Q8 control were new to code. β⁷ and β⁹ were known from the published table beforehand. β⁷ tests the count 4 and the rule at the next order, and the count 36 is what makes β⁹ a test. Each of `sabotage=bad_group`, `wrong_class`, `wrong_table`, `drop_direction`, `drop_bent` and `q8_everywhere` must fail on its named check, and the [workflow](../.github/workflows/subgroup-designs.yml) checks that each one does.
