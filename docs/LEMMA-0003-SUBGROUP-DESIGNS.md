# Lemma YM4-02b: finite subgroups of SU(2) and the Haar integral

**Status:** the statement is PROVED below, its strengths and consequences are MEASURED by an exact integer run, and independent review is OPEN. **Scope:** finite-lattice moments and the strong-coupling Taylor coefficients of the Wilson lattice. It is a subtask of [YM4-02](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/2).

## Statement

Let G be a finite subgroup of SU(2), and let t+1 be the first n ≥ 1 at which G has a nonzero invariant on the spin-n/2 representation V_{n/2}. Then for every polynomial f of degree at most t on the unit sphere S³ = SU(2),

```text
(1/|G|) sum_{g in G} f(g) = integral f(U) dHaar(U).
```

**Proof.** By Peter–Weyl, polynomials of degree at most t on S³ are spanned by the matrix coefficients of V_{n/2} with n ≤ t. For n = 0 both sides agree. For 1 ≤ n ≤ t the Haar integral of a matrix coefficient is 0, and the G-average of the representation is the projector onto its G-invariants, which is 0 by the choice of t. QED.

**Carrying it to a lattice.** Let F be a function of the link variables that is a polynomial of degree at most t in each link, with all others fixed. For SU(2), U⁻¹ is linear in the entries of U, so inverted links count the same. Integrating one link at a time then replaces every Haar integral by the G-average with no error. Since each power X^k of X = sum over plaquettes of a_p, with a_p = (1/2) Tr U_p, has degree at most k in each link, the Taylor coefficients of Z(β) on any finite lattice agree for SU(2) and for G through β^t.

## The four groups

| Group | Elements | Exact through degree t | First moment that differs: E[(Tr U)^(t+1)] vs Haar | Single-plaquette ⟨a⟩ first differs at | By |
|---|---:|---:|---|---|---|
| Q8 | 8 | 3 | 4 vs 2 | β³ | +1/48 |
| 2T | 24 | 5 | 6 vs 5 | β⁵ | +1/7680 |
| 2O | 48 | 7 | 15 vs 14 | β⁷ | +1/1290240 |
| 2I | 120 | 11 | 133 vs 132 | β¹¹ | +1/163499212800 |

The strengths come from exact character sums over ℤ, ℤ[√2] and ℤ[φ]. Haar moments of Tr U are the Catalan numbers. The value t = 11 for 2I agrees with the known fact that the 600-cell is a [spherical 11-design](https://errorcorrectionzoo.org/c/600cell).

## What it computes on the four-dimensional lattice

**On (ℤ/2ℤ)⁴, with 96 plaquettes.** [Lemma 0002](LEMMA-0002-HAAR-MOMENTS.md) takes Haar orthogonality as input. Here the moments are computed by group sums, Q8 where every link has degree at most 3 and 2T where it has degree at most 5:

```text
E[X²] = 24    E[X³] = 0    E[X⁴] = 6897/4    (log Z)''''(0) = E[X⁴] − 3 E[X²]² = −15/4
```

E[X⁴] splits into 12 from single plaquettes, 1710 from pairs, and 9/4 from the 24 two-dimensional tori that wrap this side-2 lattice. As a control, using Q8 past its strength gives 6945/4, off by exactly 12 = 96 (1/4 − 1/8).

**Closed surfaces on ℤᵈ through 10 faces,** enumerated as connected sets of distinct plaquettes with every link covered an even number of times:

| d | 6 faces, per site | 10 faces, per site | 10 faces spanning 3 directions | 10 faces spanning 4 directions |
|---:|---:|---:|---:|---:|
| 3 | 1 | 3 | 3 | 0 |
| 4 | 4 | 36 | 12 | 24 |

The 24 bent surfaces, two cubes in different three-dimensional subspaces sharing a face, are the first terms that need all four dimensions. The exact value of each surface is E[∏a_p] = 2^(−F) · 2^(χ−F): 1/1024 for the cube and 1/262144 for both ten-face shapes.

**The plaquette series.** In d = 4, through β⁹,

```text
⟨(1/2) Tr U⟩ = β/4 − β³/96 + 7β⁵/1536 − 31β⁷/23040 + 4451β⁹/8847360 + ...
```

This equals Table 1 of [Denbleyker, Du, Liu, Meurice and Velytsky, arXiv:0807.0185](https://ar5iv.arxiv.org/html/0807.0185), which lists P = 1 − ⟨(1/2) Tr U⟩ with the same β, so its signs are opposite. The β⁹ coefficient splits as 13/4423680 from one plaquette, 5/18432 from the cube and 15/65536 from the ten-face surfaces. Without the 24 bent surfaces the sum misses the table.

Through β¹⁰ in log Z only these surfaces enter, because a face with spin at least 1, or two overlapping surfaces, first appears at β¹². That step is DERIVED, and the match with the table is its check.

## Scope

The lemma is exact for its stated degree on any finite lattice, so it is a rigorous starting point for the bounded approximation that [YM4-03](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/3) asks of any use of Q8, 2T, 2O or 2I. It speaks to strong coupling. [Discrete subgroups of SU(2) have a freezing transition](https://www.arxiv.org/pdf/2201.09625) at larger β, which bounds how far a subgroup can follow SU(2), and the continuum limit needs β → ∞. Reflection positivity, the transfer matrix, the renormalization group, the continuum limit and the physical mass gap stay OPEN in the [ledger](PROOF_OBLIGATIONS.md).

## Reproduce

```bash
python3 -I -X utf8 tests/test_subgroup_designs_4d.py
```

It takes about 20 seconds, uses integers only, and prints the rows in [`tests/SUBGROUP_DESIGNS_RECEIPT.txt`](../tests/SUBGROUP_DESIGNS_RECEIPT.txt). The prediction, [`PREDICTION-YM4-02b.hbp`](PREDICTION-YM4-02b.hbp), was pushed before the code. It records that a scratch run had already seen the design strengths, the 2⁴ moments and the series through β⁵, and that the closed-surface counts, the ten-face values, β⁷, β⁹ and the first differences were new. Each of `sabotage=bad_group`, `wrong_class`, `wrong_table`, `drop_direction` and `q8_everywhere` must exit 1, and the [workflow](../.github/workflows/subgroup-designs.yml) checks that they do.
