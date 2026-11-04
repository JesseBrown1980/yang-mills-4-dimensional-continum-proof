# YM4-02d: an explicit gap at each fixed lattice

**Status: DERIVED by the seat ACER-CLAUDE-FABLE5 on November 4, 2026. GPT-6, a different model family, read FABLE5's sketch of Steps 1 and 2 the same day, for the Wilson weight, tagged CONJECTURE, and returned a proof of its own for SU(2) at the proof level, with the full-space route in Step 4: [its report, verbatim](../reviews/gpt6-quantitative-gap/README.md). Its report came before this note was written, so the general weight and Step 3 as written here await a different model family. Its exact tests, registered first in [`PREDICTION-YM4-02d.hbp`](PREDICTION-YM4-02d.hbp), are MEASURED below: every row the test reads was met, and the gate clause of the limits row was met at the next commit, as stated below. The second seat's attack at `f7a3dbc` found no falsifier in 38,367 exact cases and no step that fails, and it gave a second proof with no citation. Its corrections are applied: [its report](../reviews/opus55-quantitative-gap/README.md).**

**Scope:** one finite periodic lattice and one β > 0. The objects are those of [section 7 of Lemma 0004](LEMMA-0004-REFLECTION-TRANSFER.md), on main since PR #14 merged at `e7a12fc`, and they are written out here so this note reads alone. Theorem 5 there gives 0 < λ₁ < λ₀, and Proposition 6 there bounds λ₀. This note bounds the ratio. Zero spacing at fixed finite physical volume stays OPEN.

## The statement

Let G be a compact group and w a continuous class function on G with w(g⁻¹) = w(g) and 0 < m ≤ w ≤ M. Take a finite periodic spatial lattice with N_ℓ links and N_s plaquettes, and H = L²(G^{N_ℓ}) with normalized Haar measure. Define

- A(U), the product of w(U_p) over the spatial plaquettes,
- B(U,V), the product of w(U_ℓ V_ℓ⁻¹) over the spatial links,
- T = A^{1/2} B A^{1/2},
- P, the projector onto gauge-invariant functions.

T has a continuous, strictly positive kernel. By the argument of Theorem 5(d), its largest eigenvalue λ₀ is simple, with a strictly positive continuous eigenfunction Ω, which is gauge invariant.

**Proposition.** Every eigenvalue μ ≠ λ₀ of T on H, and so on PH, satisfies

```text
|mu| <= tau * lambda_0,    tau = ((M/m)^N_links - 1) / ((M/m)^N_links + 1).
```

For the Wilson weight w = exp(−β(1 − ½ Re Tr U)) on SU(2), m = exp(−2β) and M = 1, so τ = tanh(β N_ℓ):

```text
lambda_1 / lambda_0 <= tanh(beta N_links) < 1,
log(lambda_0 / lambda_1) >= -log tanh(beta N_links) > 0.
```

N_ℓ is the count of spatial links, 3L³ on (ℤ/L)³. The spatial weights A play no part in the bound.

## The proof

**Step 1, the cross-ratio.** Let K(U,V) = A(U)^{1/2} B(U,V) A(V)^{1/2} be the kernel of T. In the four-point ratio

```text
K(U,V) K(U',V') / ( K(U,V') K(U',V) ) = B(U,V) B(U',V') / ( B(U,V') B(U',V) )
```

every factor of A cancels. Each value of B lies in [m^{N_ℓ}, M^{N_ℓ}], so the ratio is at most R = (M/m)^{2N_ℓ}.

**Step 2, the contraction.** On the cone C of strictly positive continuous functions on G^{N_ℓ}, Hilbert's projective metric is d(f,g) = log( max(f/g) / min(f/g) ). T maps C into C. For f, g in C,

```text
(Tf)(U) (Tg)(U') / ( (Tg)(U) (Tf)(U') )
  = ∫∫ K(U,V) K(U',V') f(V) g(V') dV dV' / ∫∫ K(U,V') K(U',V) f(V) g(V') dV dV',
```

and the integrands have ratio at most R pointwise. So the image of C has projective diameter Δ ≤ log R = 2N_ℓ log(M/m). Birkhoff's theorem says T contracts d by the factor tanh(Δ/4). With x = (M/m)^{N_ℓ}, tanh((log x)/2) = (x − 1)/(x + 1), which is τ.

**Step 3, from the contraction to the eigenvalue.** T is self-adjoint and compact, so μ is real, and μ = 0 needs nothing. Let μ ≠ 0, λ₀ with real eigenfunction h, continuous because h = Th/μ and the kernel is continuous. h is orthogonal to Ω > 0, so it changes sign, and ρ = h/Ω is continuous and nonconstant. With θ = μ/λ₀, |θ| < 1: for real unit h, |μ| = |⟨h, Th⟩| < ⟨|h|, T|h|⟩ ≤ λ₀, the first step strict because the kernel is strictly positive and h changes sign, the second because λ₀ is the largest eigenvalue of the compact self-adjoint T. Theorem 5(d) reads μ < λ₀ at β > 0, where T ≥ 0, and this line also covers the negative μ of a general weight. Take ε > 0 small enough that f = Ω(1 + ερ) lies in C. Then

```text
T^n f = lambda_0^n Omega (1 + eps theta^n rho),
d(T^n f, T^n Omega) = log( max(1 + eps theta^n rho) / min(1 + eps theta^n rho) ) = eps |theta|^n osc(rho) (1 + o(1)).
```

Iterating Step 2, the left side is at most τⁿ d(f, Ω), a constant times τⁿ. Taking nth roots gives |θ| ≤ τ. ∎

**Step 4, the gauge-invariant sector, two routes.**

*Route 1, GPT-6's, on the full space.* The proof above runs on all of H, with no projection. Ω is gauge invariant and PH is invariant under T, so λ₀ is the top eigenvalue on PH and every other eigenvalue on PH is one of the μ above. So λ₁ on PH is at most τ λ₀.

*Route 2, on the orbits.* The projected kernel is (BP)(U,V) = ∫ B(U, V^g) dg. An average of values in [m^{N_ℓ}, M^{N_ℓ}] stays there, so Steps 1 to 3 run on the space of gauge orbits with the same R.

The two routes differ in one way: on H the first eigenvalue after λ₀ can belong to a gauge-noninvariant function, and it is at most τλ₀ too.

## A second proof, with no citation

By the second seat, DERIVED, in [its derivations](../reviews/opus55-quantitative-gap/DERIVATIONS.txt), section 2. FABLE5 read it step by step. It replaces Steps 2 and 3 whole, and it uses Ω > 0, continuity and Step 1.

Let h be a real eigenfunction for μ ≠ 0, λ₀, continuous as in Step 3 (μ = 0 needs nothing), ρ = h/Ω, and x₁, x₂ the points of largest and smallest ρ. P(x, dy) = K(x,y) Ω(y) / (λ₀ Ω(x)) dy is a probability kernel, and Pρ = θρ with θ = μ/λ₀. With p = P(x₁, ·) and q = P(x₂, ·), θ osc(ρ) = ∫(p − q)ρ, so |θ| ≤ TV(p, q).

Let r = p/q, with range [r₋, r₊], r₋ ≤ 1 ≤ r₊. With E = {r > 1}, a = q(E) and b = p(E), we have b ≤ r₊a and 1 − b ≥ r₋(1 − a), so

```text
TV(p, q) = b - a <= min( (r+ - 1) a, (1 - r-)(1 - a) ) <= (r+ - 1)(1 - r-) / (r+ - r-).
```

With r₊/r₋ = S fixed, this is largest at r₊ = √S, where it equals (√S − 1)/(√S + 1). S is the largest of K(x₁,y) K(x₂,y′) / (K(x₁,y′) K(x₂,y)), since Ω cancels, so S ≤ R by Step 1. And √R = (M/m)^{N_ℓ}, so |θ| ≤ τ. ∎

**Where equality lives.** |θ| = τ > 0 forces r to take only the values (M/m)^{N_ℓ} on E and (M/m)^{−N_ℓ} off E, so every link carries M at x₁ and m at x₂ for y in E, and the reverse off E. Take y in E and y′ off E, and splice the first link of y into y′. The ratio there is (M/m)^{2−N_ℓ}, which is neither value when N_ℓ ≥ 2. On PH the same holds of every gauge image, since an average of values at most M^{N_ℓ} equals M^{N_ℓ} only when each equals it. On connected G, r is continuous on a connected space and takes one value, so the inequality is strict at every N_ℓ.

**The multipliers.** The proof uses A only through positivity. For finite G with w(1) = M and w(g₀) = m, take A = 1 on (1, …, 1) and (g₀, …, g₀) and ε elsewhere, on H. As ε → 0, T tends, up to the scale |G|^{−N_ℓ}, to the block [[M^{N_ℓ}, m^{N_ℓ}], [m^{N_ℓ}, M^{N_ℓ}]], with ratio τ. So τ is the exact supremum over positive multipliers at every N_ℓ, DERIVED by the second seat, section 7, and a better dependence on N_ℓ has to use the form of A or B beyond positivity.

## Where it is sharp and where it is loose

**Sharp at N_ℓ = 1.** Z2 on one link, with w = 1 at the identity and q at the other element, has N_ℓ = 1, M/m = 1/q and T = ½[[1, q], [q, 1]], with eigenvalues (1 ± q)/2. So λ₁/λ₀ = (1 − q)/(1 + q) = τ, the least constant at N_ℓ = 1. With M > m, equality holds exactly when N_ℓ = 1 and G has a closed subgroup of index 2, with w = M on it and m off it, where μ = τλ₀, or w = m on it and M off it, where μ = −τλ₀: DERIVED by the second seat, and MEASURED on 25 finite groups, 1,348 equal cases, all in this family. For N_ℓ ≥ 2 the inequality is strict on every weight with M > m, DERIVED, with 12,892 exact cases all strict, and the exponent N_ℓ is approached as M/m grows: S3 on 1×1 with weights 1, 2, 2¹⁶⁰ on the identity, the 3-cycles and the transpositions reads an effective exponent, the n with ((M/m)^n − 1)/((M/m)^n + 1) equal to the ratio, of 1.972 of 2, and S3 on 1×1×1 with 2, 1, 2¹²⁸ reads 2.946 of 3. Among weights with T ≥ 0 on the orbits at N_ℓ ≥ 2, the largest effective exponent measured reads N_ℓ/2, on Z2 on L×1. SU(2) is connected, so its inequality is strict at every β > 0, and on one link it reads I₂(β)/I₁(β), an effective exponent below 0.25 at the nine β measured.

**Loose with many links.** The bound sees only the range of each weight and the number of links. GPT-6's float diagnostic on Z2 at N_ℓ = 8 reads 0.146 against 0.992.

**What it says as the lattice grows.** −log tanh x = 2 exp(−2x)(1 + O(exp(−4x))), so the bound in lattice units falls like 2 exp(−2βN_ℓ). At fixed physical size, L = L_phys/a grows as a → 0, and (1/a)(−log tanh(βN_ℓ)) goes to 0 as long as 2βN_ℓ − log(1/a) goes to infinity, which holds with N_ℓ = 3(L_phys/a)³ for β bounded below by a positive constant. So this result sizes the gap at each fixed lattice, and carrying a gap to zero spacing needs a dependence on N_ℓ far better than this. That is OPEN.

## What could fail

- **Step 2** rests on Birkhoff's theorem, NAMED: G. Birkhoff, *Extensions of Jentzsch's theorem*, Trans. AMS 85 (1957), in the form stated by [Lemmens and Nussbaum](https://arxiv.org/abs/1304.7921) and [Reeb, Kastoryano and Wolf](https://arxiv.org/abs/1102.5170). FABLE5 read a search summary quoting those statements and left Birkhoff's own proof unreworked. The second seat opened both papers on November 4, 2026: Lemmens and Nussbaum, equation (2.2) and Theorem 2.9, for cones in any real vector space, with C taken together with 0, which covers SU(2); Reeb, Kastoryano and Wolf, Theorems 4 and 5, for proper cones in finite dimension, where Theorem 5 is the eigenvalue bound itself. The second proof above stands on none of them.
- **Step 3** needs ρ bounded and nonconstant, which continuity of h and Ω > 0 give, and |θ| < 1, which the line in Step 3 gives for this strictly positive kernel.
- **The Wilson case** needs w > 0, so it holds for every real β in the bound's form, with m and M read off the weight and τ = tanh(|β|N_ℓ). Theorem 5 and this statement are written for β > 0.

**Falsifier:** one positive symmetric class weight in [m, M], on one lattice, with a non-leading eigenvalue of modulus above τλ₀.

## What is measured

[`tests/test_quantitative_gap.py`](../tests/test_quantitative_gap.py), in exact integers, against [the prediction](PREDICTION-YM4-02d.hbp), pushed at commit `9d1c334` before that test existed. Every row the test reads was met on its first run, `failed=0`, and the receipt is byte-equal to that run. The clause `integers_only_under_scripts/no_float_gate.py=1` of the limits row was missed at commit `f7a3dbc`: the gate refused `.modules` at line 556, `failed=1`, in hosted run 41840421497, which skipped the test's own steps, and an earlier local read held 28 code files, before the test was tracked. Commit `c64eed3` reads the imports from the source with the same row, and hosted run 41841734786 reads `failed=0`, the receipt byte-equal and each sabotage exit 1. The rows are in [`tests/QUANTITATIVE_GAP_RECEIPT.txt`](../tests/QUANTITATIVE_GAP_RECEIPT.txt).

**Exact spectra, one link direction, no spatial plaquettes.** The values were worked out by hand from characters, as (c_ρ/d_ρ)^L, and the test reads them through the orbit matrix, a separate route, with the nullity at each value and the multiplicities summing to the number of orbits.

| Group | Weight | Links | Spectrum on PH | λ₁/λ₀ | τ |
|---|---|---:|---|---:|---:|
| Z2 | q = 1/4 | 1 | 5/8, 3/8 | **3/5** | **3/5**, equal |
| Z2 | q = 1/4 | 2 | 25/64, 9/64 | 9/25 | 15/17 |
| Z2 | q = 1/4 | 3 | 125/512, 27/512 | 27/125 | 63/65 |
| S3 | 1, 1/2, 1/3 | 1 | 19/36, 1/9, 1/36 | 4/19 | 1/2 |
| Q8 | r = 1/2 | 1 | 41/128, 15/128, 9/128 three times | 15/41 | 15/17 |
| Q8 | r = 1/2 | 2 | 1681/16384, 225/16384, 81/16384 three times | 225/1681 | 255/257 |
| 2T | r = 1/2 | 1 | 121/384, 13/128, 3/128, 1/128 twice, 1/384 twice | 39/121 | 15/17 |

**With spatial plaquettes.** The ratio is an exact bracket in parts per million. The certificate reads: at least one eigenvalue above a rational lo, at most one above τ·lo, and none below −τ·lo, so every other eigenvalue has modulus at most τ·lo < τλ₀.

| Group | Weight | Lattice | N_ℓ | N_s | Orbits | λ₁/λ₀, ppm | τ |
|---|---|---|---:|---:|---:|---:|---:|
| Z2 | q = 1/5 | 2×2 | 8 | 4 | 32 | 812023 to 812024 | 195312/195313 |
| Z2 | q = 1/2 | 2×2 | 8 | 4 | 32 | 146218 to 146219 | 255/257 |
| Z2 | q = 4/5 | 2×2 | 8 | 4 | 32 | 12665 to 12666 | 325089/456161 |
| Z2 | q = 1/2 | 2×1×1 | 6 | 6 | 32 | 511381 to 511382 | 63/65 |
| Z2 | q = 1/2 | 1×1×1 | 3 | 3 | 8 | 333333 to 333334 | 7/9 |
| Z3 | 1, 1/2, 1/2 | 2×1 | 4 | 2 | 27 | 385446 to 385447 | 15/17 |
| Z3 | 1, 1/2, 1/2 | 3×1 | 6 | 3 | 81 | 428816 to 428818 | 63/65 |
| S3 | 1, 1/2, 1/3 | 1×1 | 2 | 1 | 11 | 279835 to 279836 | 4/5 |
| Q8 | r = 1/2 | 1×1 | 2 | 1 | 28 | 529896 to 529897 | 255/257 |
| Q8 | r = 1/2 | 1×1×1 | 3 | 3 | 176 | certificate alone | 4095/4097 |
| 2T | r = 1/2 | 1×1 | 2 | 1 | 76 | 435408 to 435409 | 255/257 |

GPT-6's float diagnostic, recorded in the prediction as already seen, falls in the first three brackets: 0.812023, 0.146218 and 0.012666. Q8 on 1×1×1 is the spatial slice of a four-dimensional lattice.

**Both routes.** Route 1 on all configurations, Z2 on 2×1×1 (dimension 64), Z3 on 2×1 (81) and Q8 on 1×1 (64): the top eigenvalue lies in the bracket from the orbits, and the certificate holds. Route 2 is every row above. On each case of at most 32 orbits, each averaged entry lies in [m^{N_ℓ}, M^{N_ℓ}], and the largest cross-ratio is at most (M/m)^{2N_ℓ}. The field `A_cancels=1` is an identity of the code's multiplication, reading 1 for any array in place of A, and the cancellation of A stands on Step 1, DERIVED.

**Broken kernels, each named in the prediction.**

| Kernel | Reading |
|---|---|
| Z3, weight 1, −1/2, −1/2 | The hypothesis refuses it. Spectrum 1/2 twice, 0, so the ratio is 1, above the 1/3 that the range of \|w\| would give. The bound is false here |
| Z3, weight 1, 0, 0 | The hypothesis refuses it. Spectrum 1/3 three times, with no finite range |
| Z3, weight 1, 1/2, 1/4 | The hypothesis refuses it, and the inertia reports an asymmetric matrix |
| Half the exponent, on Z2 with q = 1/4 | That constant reads 1/3 against an exact ratio of 3/5, so it is false here |

**The sabotages.** `drop_gauge_average`, `drop_orbit_measure`, `half_the_exponent` and `drop_spatial_weight` each exit 1 on the check the prediction named, with no crash, and an unknown name exits 2.

**The test's reach, from the second seat.** 26 mutants: 10 killed by a predicted row, 3 passing the script with only the receipt differing (A inverted, a dropped fourth inverse, and Route 1 run on the orbits), and 13 surviving, of which 12 weaken a checker and 1 is equivalent on the filed lattices. Its own integer route, a characteristic polynomial and Descartes, met 7 of 7 exact rows, 11 of 11 plaquette rows and 3 of 3 full-space rows. Controls to add, OPEN: a plaquette ratio pinned in the prediction on Z3, S3, Q8 and 2T, since Z2 at 2×2 reads A and 1/A alike; a row with a negative eigenvalue, such as Z2 with w = 1/4, 1, where μ = −3/8; and Z3 on 2×2, with four distinct links in a word whose order matters. Its engine reads Q8 on 1×1×1 at 582784 to 582785 ppm and Z3 on 2×2 at 73035 to 73036 ppm.

**Scope.** Finite groups at rational weights. SU(2) itself is covered by the proof, and read here through Q8 and 2T at rational r. 2O and 2I have irrational Wilson weights at rational r and are left out.

**Seen after the run, in no prediction.** On some lattices the gauge-averaged kernel's largest cross-ratio sits far below R. Z2 at q = 1/4 on 2 links reads 289/64 against R = 256, and at q = 1/2 on 2×2 it reads 124609/16384 against 65536. On those two-orbit cases of Z2, tanh(Δ/4) from the actual cross-ratio equals the exact ratio: 9/25 at 2 links and 27/125 at 3. On others it reaches R: 256 on Q8 and 2T with one link, 65536 on Q8 at 1×1, 64 on Z2 at 1×1×1. So the bound from the true diameter of BP is tighter than τ on some lattices and equal on others. How that diameter grows is the next paragraph.

**The true diameter, from the second seat** ([derivations](../reviews/opus55-quantitative-gap/DERIVATIONS.txt), section 5). For abelian G the largest cross-ratio of BP is (Z_max/Z_min)², where Z(W) is the gauge average of the product of w with holonomy W, DERIVED, and 27 of 27 cases equal the direct orbit matrix. For any compact G with a central element W, SU(2) included, Δ ≥ 2 log(Z(1)/Z(W)), DERIVED. On a circle Δ falls to 0, and on Z2 tanh(Δ/4) equals the exact ratio to L = 12, MEASURED. On the 2D torus with Z2 at q = 1/2, a lower bound on log₂ of the largest cross-ratio reads 0.752, 1.810, 3.133, 5.094 and 7.747 at L = 2, 4, 6, 8 and 10, growing linearly in the sites, MEASURED. So the true diameter improves the constant in the exponent and keeps the exponential form in d ≥ 2 on those cases, and for d ≥ 3 and SU(2) that is CONJECTURE. Iterates do converge: on Z2 at 2×2 with q = 1/2, tanh(Δ(T^k)/4)^{1/k} reads 467776, 273970, 200288, 171131 and 158185 ppm at k = 1, 2, 4, 8 and 16, against an exact ratio of 146218, MEASURED, and A enters from k = 2. A dependence on N_ℓ good enough for zero spacing is OPEN.
