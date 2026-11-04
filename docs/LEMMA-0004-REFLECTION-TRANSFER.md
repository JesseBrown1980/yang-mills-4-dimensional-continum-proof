# Lemma YM4-02c: reflection positivity and the transfer operator of the finite SU(2) Wilson lattice

**Status.** Theorems 1, 2, 4 and 5 and Propositions 3, 4.1 and 6 are DERIVED, with full proofs below. Their exact controls are MEASURED by [`tests/test_reflection_transfer_4d.py`](../tests/test_reflection_transfer_4d.py), whose rows are in [`tests/REFLECTION_TRANSFER_RECEIPT.txt`](../tests/REFLECTION_TRANSFER_RECEIPT.txt). The owning gate is [`reflection-transfer.yml`](../.github/workflows/reflection-transfer.yml). Lüscher's transfer-matrix proposition is matched in writing in section 9. The body of Osterwalder–Seiler (1978) is CANNOT_SEE from this seat, so the match to it stays NAMED. A second seat attacked this lemma at commit 1618199: every theorem and every computed value held, and it refuted the record of misses. Its evidence is in [`reviews/opus55-ym4-02c/`](../reviews/opus55-ym4-02c/), and section 10 carries the corrections. Review by a different model family: OPEN.

**Scope.** Each statement holds at one fixed finite lattice and one fixed β. Uniformity in volume and spacing: OPEN. λ₁ and a quantitative gap for SU(2): OPEN. S₃ numbers carried here: 0. This is a subtask of [YM4-02](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/2).

## 1. Setting

Let Λ = (ℤ/L₁) × … × (ℤ/L_k) × (ℤ/T), with T = 2m even and periodic in every direction. The four-dimensional lattice has k = 3 and every L_i = L. The theorems hold for any k and any sides. The rows `REFLECTION`, `EXCLUSIVE_LINK`, `STAGGERED_FLIP` and `PLAQUETTE_ORIENTATION` on (ℤ/L)³ × (ℤ/T), the scan in `CYLINDER` on (ℤ/3)³ × (ℤ/4), and `FOUR_D_LINK`, `FOUR_D_TRANSFER` and the (ℤ/1)³ rows of `SINGLE_W_SITE` run at k = 3, and every other Gram, PSD and transfer row runs at k = 1 or k = 2, so at general L the four-dimensional statements are carried by the proofs.

A positive link is a spatial U_i(x,t), from (x,t) to (x+i,t), or a time link V(x,t), from (x,t) to (x,t+1). A plaquette is written in the repository's convention:

```text
U_p = U_mu(y) U_nu(y+mu) U_mu(y+nu)^-1 U_nu(y)^-1,  mu < nu.
```

So a spatial plaquette is U_i(x,t) U_j(x+i,t) U_i(x+j,t)⁻¹ U_j(x,t)⁻¹, and a time-like plaquette is U_i(x,t) V(x+i,t) U_i(x,t+1)⁻¹ V(x,t)⁻¹.

Let G be a compact group with normalized Haar measure. A **weight** is a bounded measurable class function w on G with w(g⁻¹) = w(g), real-valued. On SU(2) and on Q8 every element is conjugate to its inverse, so a class function has the second property automatically. The **Wilson weight** on SU(2) is

```text
w_beta(g) = exp(-beta (1 - a(g))),  a(g) = (1/2) Re Tr g,
```

so ∏_p w_β(U_p) = exp(−S) with S = β Σ_p (1 − a_p). For a reflection θ, defined in section 3, and bounded measurable functions F₁, F₂ on the relevant half of the lattice,

```text
N_w(F1, F2) = integral prod dU  conj(F1(theta U)) F2(U) prod_p w(U_p),
N_w(F) = N_w(F, F),   Z_w = N_w(1),   <theta(F) F> = N_w(F) / Z_w  when Z_w > 0.
```

Q8 and 2T with counting measure are instances of G in their own right. They stand in for Haar measure on SU(2) only in parts B and C of section 8, within their exact degree, as those rows state.

## 2. Bounds

**Theorem 1.** On every such lattice with G = SU(2), Z > 0 for every real β. For β ≥ 0, exp(−β N_p) ≤ Z ≤ 1, where N_p is the number of plaquettes.

*Proof.* The integrand is continuous and strictly positive on a compact space, so Z > 0. For β ≥ 0, a_p ≤ 1 gives S ≥ 0, so exp(−S) ≤ 1 and Z ≤ 1. Jensen's inequality for the probability measure gives Z ≥ exp(−E[S]) = exp(−β Σ_p (1 − E[a_p])). It remains to see E[a_p] ≥ 0. If a plaquette holds a link that appears once in its word, integrating that link makes U_p Haar distributed and E[a_p] = 0. A plaquette in the plane (μ,ν) holds one as soon as one of its two sides is at least 2, since then U_μ(y) and U_μ(y+ν), or U_ν(y+μ) and U_ν(y), are distinct links. On a lattice with every side at least 2 all four links are distinct, which the test counts on all three lattices of part A. The remaining case has both sides equal to 1, with both directions spatial since T ≥ 2, and the plaquette is a commutator U V U⁻¹ V⁻¹. Integrating U gives Tr(U V U⁻¹ V⁻¹) → (Tr V)²/2, so E[a_p] = E[(Tr V)²]/4 = 1/4 > 0. So E[a_p] ≥ 0 in every case, and the bound follows. ∎

The prediction's row names S ≥ 0 and Jensen. E[a_p] = 0 holds for L ≥ 2, and the form above also covers the side-1 lattices of parts F and G. The value 1/4 is measured as `COMMUTATOR`.

## 3. The two reflections

Let c = 0 for **site reflection** and c = −1 for **link reflection**. On sites, θ(x,t) = (x, c−t). On an oriented edge e from a to b, θe runs from θa to θb, and (θU)(e) = U(θe), with U of a reversed edge the inverse. A time edge from t to t+1 goes to the edge from c−t to c−t−1, which is the positive link at c−t−1 run backward. So exactly:

```text
(theta U)_i(x, t) = U_i(x, c - t),
(theta V)(x, t)   = V(x, c - t - 1)^-1.
```

Both are involutions, since c − (c−t−1) − 1 = t and the inverse is applied twice. On plaquettes, θ(x,t,i,j) = (x, c−t, i, j), and θ(x,t,i,time) = (x, c−t−1, i, time).

**Lemma 3.1.** For a spatial plaquette, U_p(θU) = U_{θp}(U). For a time-like plaquette, U_p(θU) is conjugate to U_{θp}(U)⁻¹. Hence w(U_p(θU)) = w(U_{θp}(U)) for every weight, and a_{θp}(θU) = a_p(U).

*Proof.* The spatial case is the definition. For the time-like case put s = c − t − 1, so that c − t = s + 1:

```text
U_p(theta U) = U_i(x, s+1) V(x+i, s)^-1 U_i(x, s)^-1 V(x, s),
U_(theta p)(U)^-1 = V(x, s) U_i(x, s+1) V(x+i, s)^-1 U_i(x, s)^-1.
```

The first is a cyclic rotation of the second, so they are conjugate. A class function with w(g⁻¹) = w(g) takes the same value on both. ∎

The inverse on time links is what makes this true. Dropping it is the sabotage `no_inverse_on_time_links`, which fails on noncommuting configurations.

**The property w(g⁻¹) = w(g) has a control.** 2T has conjugacy classes that inversion swaps, and `W_INVERSE_CONTROL` gives them a real positive weight, with values 9, 7, 5, 8, 2, 3, 6 on the classes. On (ℤ/1) × (ℤ/2), with F a point function of V(0), 384 of the 576 blocks at fixed spatial links lose symmetry and the form reaches −144.

**Gauge covariance.** With (U^g)_ℓ = g(s) U_ℓ g(r)⁻¹ for a link from s to r, one has θ(U^g) = (θU)^{g∘θ}, so θ carries gauge-invariant functions to gauge-invariant functions. This is checked on exact configurations.

**Lemma 3.2 (the split).**

*Site reflection.* The fixed slices are t = 0 and t = m. The fixed plaquettes are the spatial ones in those slices. The upper plaquettes are the spatial ones with 0 < t < m and the time-like ones with base 0 ≤ t ≤ m−1. The lower plaquettes are their mirror images. Each plaquette lies in exactly one of the three sets. The links of the upper and fixed plaquettes together, and the links of the lower and fixed plaquettes together, share exactly the spatial links of the two fixed slices. The **closed half** is the set of spatial links with 0 ≤ t ≤ m and time links with base 0 ≤ t ≤ m−1.

*Link reflection.* The crossing planes lie between t = −1 and t = 0 and between t = m−1 and t = m. The crossing links are V(x,−1) and V(x,m−1), and each maps to its own inverse. The crossing plaquettes are the time-like ones based at t = −1 and t = m−1, and each maps to itself reversed. The upper plaquettes are the spatial ones with 0 ≤ t ≤ m−1 and the time-like ones with 0 ≤ t ≤ m−2. The **open half** is the set of spatial links with 0 ≤ t ≤ m−1 and time links with base 0 ≤ t ≤ m−2. It is disjoint from its mirror image and from the crossing links.

The counts on (ℤ/L)³ × (ℤ/T) are N_p = 6L³T, crossing or fixed 6L³, each half 3L³(T−1). Writing S₊ for the upper sum, with weight 1/2 on fixed plaquettes in the site case,

```text
site:  S(U) = S_plus(U) + S_plus(theta U),
link:  S(U) = S_plus(U) + S_plus(theta U) + S_crossing(U).
```

| L | T | plaquettes | crossing or fixed | each half | exact configurations, per reflection |
|---:|---:|---:|---:|---:|---:|
| 2 | 2 | 96 | 48 | 24 | 2 |
| 2 | 4 | 192 | 48 | 72 | 2 |
| 3 | 4 | 648 | 162 | 243 | 2 |

Every row is MEASURED for both reflections: involution on links, plaquettes to plaquettes as oriented cycles, the mirror split and link supports, a_{θp}(θU) = a_p(U), the action split and gauge covariance, on exact rational SU(2) fields built from (3,4,0,0)/5, (5,0,12,0)/13 and (8,0,0,15)/17.

**Plaquette orientation.** The `REFLECTION` rows compare words up to rotation and inversion. So they catch a dropped inverse on the third letter of U_p, and a dropped inverse on the fourth letter leaves them unchanged, as mutants of commit 1618199 measured. The replay of GPT-6's checker records the third-letter mutation surviving on its lattice through the relabelling b → b⁻¹, and the `GRAM_LINK` rows here stay unchanged under it as well. `PLAQUETTE_ORIENTATION` reads each word against the path it traces and against the gauge action. On all three lattices of the table, every word is a closed path based at y, each link appears once forward and once backward in each of its planes, and U_p(U^g) = g(y) U_p(U) g(y)⁻¹ holds exactly on 2 configurations. These checks read the word itself, so a relabelling of link variables leaves them red: the sabotages `dropped_inverse_third_letter` and `dropped_inverse_fourth_letter` each exit 1 on the check `plaquette_orientation`.

## 4. Site reflection

**Theorem 2.** Give each plaquette p a weight w_p with w_{θp} = w_p, so that N_w carries ∏_p w_p(U_p). Let C be the spatial links of the fixed slices and A the remaining links of the closed half, and put

```text
f(C) = prod_(p fixed) w_p(U_p),    W_plus(C, A) = prod_(p upper) w_p(U_p).
```

For every bounded measurable function F on the closed half under site reflection,

```text
N_w(F) = integral dC  f(C) | integral dA  F(C, A) W_plus(C, A) |^2.
```

So N_w(F) ≥ 0 for every such F if and only if f(C) ≥ 0 for almost every C at which W₊(C, ·) is not almost everywhere zero, and then every Gram matrix (N_w(F_a, F_b)) is positive semidefinite. A sufficient condition is w_p ≥ 0 on the values taken by each fixed plaquette, the form first stated here. The Wilson weight is strictly positive for every real β, so site reflection positivity holds for every real β.

*Proof.*

1. *Variables.* Write U = (C, A, A⁻), with A⁻ the rest. θ fixes C pointwise and maps A⁻ onto A, with an inverse on time links. Let A′ be the image of A⁻. By inversion invariance of Haar measure, (C, A, A⁻) → (C, A, A′) preserves the measure.
2. *The fixed plaquettes.* f depends on C alone and θ fixes C, so f stays whole as a factor. Writing f = f^{1/2} f^{1/2} and carrying one root with each half, as the first version of this proof did, is a convenience, real only where f ≥ 0. A signed weight on a fixed slice acts through the sign of f(C) in the display above.
3. *Factorization.* By Lemma 3.1 and w_{θp} = w_p, w_{θp}(U_{θp}(U)) = w_p(U_p(θU)). So the lower plaquettes multiply to W₊(θU), and ∏_p w_p(U_p) = f(C) W₊(U) W₊(θU).
4. *Conjugation.* Since W₊ is real, conj(F(θU)) W₊(θU) = conj(Φ(θU)) with Φ = F W₊, a function of (C, A). And θU restricted to the closed half is (C, A′).
5. *Independence.* Conditioned on C, the variables A and A′ are independent, so integrating them gives the display, with G(C) = ∫dA Φ(C, A) inside the square.
6. *Both directions.* If f(C) ≥ 0 for almost every C at which W₊(C, ·) is not almost everywhere zero, the integrand is non-negative, since G(C) = 0 at every other C. Conversely, let E be the set of C with f(C) < 0 and ∫dA W₊(C, A)² > 0. If E has positive measure, F = 1_E(C) W₊(C, A) gives N_w(F) = ∫_E dC f(C) (∫dA W₊(C, A)²)² < 0.

The Gram statement follows because Σ conj(x_a) x_b N_w(F_a, F_b) = N_w(Σ x_b F_b). ∎

The hypotheses are exactly these. The upper and lower weights may take either sign and may differ from one mirror pair to the next. Positivity of characters plays no part. F ranges over all bounded measurable functions on the closed half, gauge-invariant or moved by gauge transformations.

**What the pointwise form reads on SU(2) at k ≥ 2.** With one w on every plaquette, every group element is a value of a fixed plaquette, so it reads w ≥ 0 almost everywhere on SU(2) (sides ≥ 2: an exclusive link makes the plaquette Haar distributed, DERIVED; side 1: Goto's commutator theorem, NAMED). With plaquette-dependent weights the mirror pairs stay free in sign, and the fixed plaquettes carry the condition.

**Remark 4.2 (the sharp form with one weight).** Take one w with w ≠ 0 almost everywhere, k ≥ 2 and every spatial side ≥ 2. Then f ≥ 0 almost everywhere if and only if sign w is, almost everywhere, plus or minus a homomorphism χ: G → {±1}. On SU(2), and on any connected G, this reads: w has one sign almost everywhere. Here W₊(C, ·) is almost everywhere nonzero, so this is the condition of Theorem 2.

*Proof.* If sign w = εχ, each link appears in each plane of a slice once forward and once backward, so ∏ χ(U_p) = 1 over a slice, and the two slices give ε^{2N_s} = 1. Conversely, f ≥ 0 makes the product over one slice one-signed, since the two slices are independent. Fix every link of a slice except g = U_ℓ. Then that product is a nonzero constant times ∏_j w(g X_j), over the 2(k−1) staples X_j of ℓ, and the staples are jointly Haar distributed, since each holds an exclusive link U_ν(x) or U_ν(x−ν). So with s = sign w, ∏_j s(g X_j) does not depend on g, for almost every staple tuple. Put ε(h) = ∫ s(hY) s(Y) dY, continuous in h. For almost every h, the product of s(hY_j) s(Y_j) over independent Y_j is 1, so s(hY) s(Y) is almost everywhere constant in Y. That constant is ε(h), so |ε| = 1 on a dense set, hence everywhere, and s(hY) = ε(h) s(Y). So ε is a continuous homomorphism, and s ε is invariant under translation, hence constant. ∎

Q8 has three nontrivial homomorphisms, which is where a signed weight can stay green. `SITE_CHARACTER` reads the slice (ℤ/2) × (ℤ/2) over its 32,768 gauge-fixed configurations: w = 3, 2, 1, −1, −2, whose sign is a homomorphism, has a negative product on 0 of them, and w = 3, 2, 1, −1, 2 and 1, −1, 1, 1, 1 have one on 12,288 and 10,944.

**The sign of f(C) has teeth.** On (ℤ/1) × (ℤ/1) × (ℤ/2) with Q8, both slices are fixed, and s₀, s₁ are commutators taking only the values ±1, with P(s = −1) = 3/8. With time-like weight 1 and F the indicator of s₀ = −1, s₁ = +1:

| fixed-slice weight w(+1), w(−1) | numerator N(F) | Z | Gram matrix |
|---|---:|---:|---|
| 1, −1 | −15/64 | 1/16 | negative pivot: positivity fails, with Z > 0 |
| 3, 1 | 45/64 | 81/16 | PSD, rank 7 on 7 functions of the fixed-slice links |
| 3, 1, with time-like values 3, −2, 1, −1, 2 on the classes | | | PSD, rank 9 on 10 functions of the closed half, some moved by gauge transformations |

An independent seat, GPT-6, found this hypothesis on review of the prediction, and the row `YM4_02C_CORRECTION` records it beside `YM4_02C_GRAM_SITE`. These rows are instances of the plaquette-dependent form, and −15/64 stays a control on its own lattice. With one w on every plaquette, `SINGLE_W_SITE` keeps the same teeth at k = 2 and k = 3: w = 1, −1, 1, 1, 1 gives a lowest N(δ_C) of −64 over 8⁶ and −64 over 8⁸, and w = 3, 1, −2, 1, −1 gives +64 and +192.

The second seat found that w ≥ 0 on the fixed plaquettes is sufficient and the sign of the product is what acts. On (ℤ/2) × (ℤ/1) × (ℤ/2) with Q8, a slice has 4096 configurations and two plaquettes, and with w on the classes of +1, −1, i, j, k:

| w | fixed-plaquette evaluations with w < 0, of 8192 | slices with a negative product | C with N(δ_C) < 0, of 8⁸ | lowest N(δ_C) × 8¹² | Z × 8¹² |
|---|---:|---:|---:|---:|---:|
| 3, 2, 1, −1, −2 | 4096 | 0 | 0 | 20736 | 53321326354432 |
| 1, 1, 1, −1, −1 | 4096 | 0 | 0 | 4096 | 68719476736 |
| 3, 2, 1, −1, 2 | 2048 | 0 | 0 | 256 | 25274644652032 |
| 1, −1, 1, 1, 1 | 1024 | 384 | 1572864 | −2304 | 10989076480 |

The formula of Theorem 2 is DERIVED here. MEASURED by the second seat, in Rust: for w = 3, 2, 1, −1, −2, all 8¹⁰ = 1,073,741,824 point functions of the closed half, with mirror mismatches 0 and negative prefactors 0, so every Gram block is PSD of rank at most 1, and the lowest numerator and Z above; for w = 1, −1, 1, 1, 1, the last three entries of its row; and the two other green weights, in its words, "behave the same". MEASURED here by `SITE_SHARP`: every row above, from pairs of the 176 gauge orbits of a slice, since N(δ_C) = A(C₀) A(C₁) T(C₀, C₁) T(C₁, C₀) depends on C through its orbits, with 0 mirror mismatches of 4096 on one plaquette with its four links free. `SITE_SHARP_BLOCK` reads one Gram block from the words: rank 1 at a C whose four fixed plaquettes all carry w = −1, and a negative pivot at a C with f(C) = −1. A side-1 direction explains w = 3, 2, 1, −1, 2 on this lattice: the two plaquettes of a slice lie in one class up to the center, so their weights multiply to a square or to w(+1) w(−1).

## 5. The character expansion

Let τ = Tr U = 2 cos θ. The character of spin n/2 is χ_n, with χ₀ = 1, χ₁ = τ and χ_{n+1} = τχ_n − χ_{n−1}.

**Proposition 3.** For m ≥ 0,

```text
tau^m = sum_n B(m, n) chi_n,   B(m, n) = (n+1)/(m+1) * binom(m+1, (m-n)/2)  for m >= n, m-n even, else 0,
```

so E[τ^m χ_n] = B(m,n) under Haar. Further, for every real β,

```text
exp(beta cos theta) = sum_n (n+1) l_n(beta) chi_n(theta),
l_n(beta) = sum_k (beta/2)^(2k+n) / (k! (k+n+1)!) = 2 I_(n+1)(beta) / beta,
```

with Σ_n (n+1)² |l_n(β)| = exp(|β|) and l_n(−β) = (−1)ⁿ l_n(β). The Wilson coefficients are c_n(β) = exp(−β)(n+1) l_n(β). They are strictly positive for β > 0. For β < 0 the coefficients with n odd are negative.

*Proof.* From τχ_n = χ_{n+1} + χ_{n−1} follows B(m+1,n) = B(m,n−1) + B(m,n+1) with B(0,n) = δ_{n0}. So B(m,n) counts walks of m steps ±1 on the non-negative integers from 0 to n, and the reflection principle gives binom(m,j) − binom(m,j−1) with j = (m−n)/2, which equals the stated form. E[τ^m χ_n] = B(m,n) is Schur orthogonality. Next, exp(βτ/2) = Σ_m (β/2)^m τ^m / m!, and with m = 2k+n one has B(m,n)/m! = (n+1)/(k!(k+n+1)!). At τ = 2 every term is positive and the sum is exp(β) for β ≥ 0, which gives the absolute convergence. The identification with I_{n+1} is the power series of the Bessel function. ∎

For a compact group, K(U,U′) = w(U U′⁻¹), acting by (Kf)(U) = ∫dU′ K(U,U′) f(U′), is diagonal on matrix coefficients: if w = Σ_ρ c_ρ χ_ρ then K D^ρ_{ab} = (c_ρ/d_ρ) D^ρ_{ab}, by Schur orthogonality, and the D^ρ_{ab} are a complete orthogonal basis by Peter–Weyl. For the Wilson weight the eigenvalue on spin j is exp(−β) l_{2j}(β), with multiplicity (2j+1)², and the trace of K is Σ (2j+1)² exp(−β) l_{2j}(β) = w(1) = 1.

**The rule on a two-dimensional torus.** On (ℤ/L) × (ℤ/T) with F = LT plaquettes, every link appears once forward and once backward. With w = Σ_ρ c_ρ χ_ρ, Schur orthogonality gives ∫dU χ_ρ(XU) χ_σ(U⁻¹Y) = δ_{ρσ} χ_ρ(XY)/d_ρ, so all faces carry one ρ, each link contributes 1/d_ρ and each site d_ρ. With V = F sites and E = 2F links,

```text
Z_direct = sum_rho c_rho^F d_rho^(V-E) = sum_rho c_rho^F d_rho^(-F).
```

For the Wilson weight on SU(2) this reads Z = Σ_n (exp(−β) l_n(β))^F. Part D checks the rule on Q8 and on 2T with a complex weight, since the rule needs only that each link appears once forward and once backward.

## 6. Link reflection

**Theorem 4.** Let w be a continuous weight with every character coefficient c_ρ = ∫ w conj(χ_ρ) ≥ 0. On a finite group every function is continuous. Then N_w(F) ≥ 0 for every bounded measurable function F on the open half under link reflection, and every Gram matrix is positive semidefinite. The characters of G may be complex: `LINK_2T` on (ℤ/1) × (ℤ/2) with 2T and c = 7, 2, 2, 4, 3, 1, 1 on 1, ω, ω², 3, 2, 2ω, 2ω² is PSD of rank 7 on all 24 point functions, and c = 7, 2, 2, 4, −1, 1, 1 has 6 positive and 1 negative. So for the Wilson weight on SU(2), link reflection positivity holds for every β ≥ 0.

*Proof.*

1. *Variables.* Write U = (U₊, U⁻, V), with U₊ the links of the open half, U⁻ their mirror links and V the crossing links. Let U′ be the image of U⁻ under θ. As in Theorem 2 this preserves the measure.
2. *The halves.* Put W₊ = ∏_{upper} w(U_p), real. By Lemma 3.1 the lower plaquettes give W₊(θU). So the integrand is conj(Φ(U′)) Φ(U₊) ∏_{crossing} w(U_p), with Φ = F W₊.
3. *One plane.* Let A be U₊ on the slice t = 0 and A′ be U′ on that slice, so A′_i(x) = U_i(x,−1). With V(x) = V(x,−1), a crossing plaquette is

```text
A'_i(x) V(x+i) A_i(x)^-1 V(x)^-1 = A'_i(x) [ (A^V)_i(x) ]^-1,   (A^V)_i(x) = V(x) A_i(x) V(x+i)^-1.
```

So V acts on the slice exactly as a gauge transformation, the product of w over the plane is B(A′, A^V) with B the product over spatial links of K, and integrating V gives

```text
(B P)(A', A) = integral dg  B(A', A^g),      (P psi)(U) = integral dg  psi(U^g).
```

The second plane gives (BP)(C, C′) in the same way, with C on the slice t = m−1 and C′ its mirror.

4. *Positivity of BP.* K(g₁Ug₂⁻¹, g₁U′g₂⁻¹) = K(U,U′), since w is a class function. So B commutes with the gauge action and BP = PB = PBP. And K = Σ_ρ (c_ρ/d_ρ) Π_ρ with Π_ρ the projection onto matrix coefficients of ρ, so K ≥ 0 when every c_ρ ≥ 0, hence B ≥ 0, hence ⟨ψ, BPψ⟩ = ⟨Pψ, B Pψ⟩ ≥ 0 for every ψ in L². Also (BP)(U,U′) is real and symmetric, because w is real with w(g⁻¹) = w(g).
5. *T ≥ 4.* Let H(A,C) be the integral of Φ over the links of the open half outside the slices t = 0 and t = m−1. Then

```text
N_w(F) = integral conj(H(A', C')) H(A, C) (BP)(A', A) (BP)(C', C),
```

and the kernel is the tensor product BP ⊗ BP on two different slices, which is positive semidefinite.

6. *T = 2.* The two planes act on the same pair of slices, and H = Φ is a function of A alone. The kernel is the pointwise product (BP)(A′,A)². When w is continuous, BP has a continuous kernel and Mercer's theorem gives BP = Σ_k λ_k φ_k φ̄_k with λ_k ≥ 0, uniformly convergent. Then N_w(F) = Σ_{k,l} λ_k λ_l |∫ H̄ φ_k φ_l|² ≥ 0, which is the Schur product theorem for kernels. On a finite group this is the matrix form. ∎

**Does it need F gauge-invariant? It holds for every F, and the numerator sees only the gauge projection.**

**Proposition 4.1.** Let g be a gauge transformation supported on the sites of Λ₊, the half t = 0, …, m−1. Then F ↦ F^g leaves θF, the product of weights and the measure unchanged, because the crossing links absorb g. So N_w(F₁,F₂) = N_w(F₁, F₂^g). Averaging over g, and doing the same on the mirror half, gives N_w(F) = N_w(ΠF), where Π averages F over gauge transformations on Λ₊. ∎

The steps above use no gauge invariance of F, and this proposition says why that costs nothing. The test enumerates every point function of the slice at T = 2, which spans all F there: on (ℤ/1) × (ℤ/2), 8 of them, and on (ℤ/2) × (ℤ/2), 64. The Gram matrix is PSD of rank 5, which is the number of gauge orbits, and the kernel does not move under gauge transformations of either slice. At T = 4 on (ℤ/1) × (ℤ/4), the 64 point functions of (U(0), U(1)) give PSD of rank 25, which is 5 × 5, one factor per slice. The open half also holds V(0), and all 512 point functions of (U(0), U(1), V(0)) give the same rank, `EVERY_FUNCTION_T4_OPEN_HALF`: 25 positive and 0 negative, and 17 and 8 at c_{2dim} = −1.

**A pointwise positive weight can fail.** On (ℤ/3) × (ℤ/2) with Q8, write w = Σ c_ρ χ_ρ on the five irreducible characters, with c = (8; 3, 3, 3; ±1) on the trivial, the three signs and the 2-dimensional character. Both weights are pointwise positive, with values 19, 15, 5, 5, 5 and 15, 19, 5, 5, 5 on the classes. With W the holonomy of the slice t = 0, integrating each plane over V gives Σ_ρ t_ρ χ_ρ(W′) χ_ρ(W) with t_ρ = (c_ρ/d_ρ)³, so

```text
G_FF = N_w(chi_2dim(W)) = sum_(rho, tau) t_rho t_tau (E[chi_2dim chi_rho chi_tau])^2 = 2 t_2dim (t_0 + 3 t_s) = +-593/4.
```

Both are measured by a pass over all 8⁷ = 2,097,152 gauge-fixed assignments.

**Remark 6.2 (a negative coefficient).** The coefficient condition in Theorem 4 is sufficient on every lattice. What a negative coefficient does depends on the lattice, on T and on the weight.

*T ≥ 4, a side L odd, w > 0 pointwise, some c_ρ < 0.* Red, for every such weight. Let W be the holonomy of a line of length L around that side, in the slice t = 0. Since w > 0, F = χ_ρ(W)/W₊ is bounded on the open half, Φ = χ_ρ(W), and steps 3 and 5 of Theorem 4 give

```text
N_w(F) = <chi_rho(W), BP chi_rho(W)> <1, BP 1> = (c_rho/d_rho)^L  c_0^(2 N_links - L) < 0.
```

DERIVED. `T4_RED_WITNESS` measures −8 at c = 8, −1, 3, 3, 2 and −4 at c = 8, 3, 3, 3, −1 on (ℤ/1) × (ℤ/4). For the Wilson weight on SU(2) this reads N_β(F) = (exp(−β) l₁(β))^L (exp(−β) l₀(β))^{2N_ℓ−L} < 0 for every β < 0. For weights that take other values the statement stays the second seat's CONJECTURE, and every sample agrees: c = 8, −3, 3, 3, 1, with values 13, 9, −1, 11, 11, has 17 positive and 8 negative on (ℤ/1) × (ℤ/4), MEASURED by the second seat.

*T = 2, L odd.* The kernel is the pointwise square of BP, and that square can be PSD when BP is not. On (ℤ/3) × (ℤ/2) with Q8, c_{2dim} < 0 is red: −593/4. A negative coefficient of a sign character depends on the weight. `NEGATIVE_COEFFICIENT` reads the five characters of W, which by Proposition 4.1 span the gauge-invariant F there: c = 8, −1, 3, 3, 2 has 5 positive and 0 negative, and c = 8, −1, 2, 2, 1 has 4 positive and 1 negative, with G_{s₁s₁} = 2t₀t₁ + 2t₂t₃ + t_E² = 435 and −57343/64. On (ℤ/1) × (ℤ/2) the same pair has 5, 0 and 4, 1, on all 8 point functions, and on (ℤ/1) × (ℤ/4) each has 17, 8, on all 64. Both are pointwise positive. The second seat measured the same inertias, from the literal 8¹² histogram with characteristic polynomial and Descartes.

*L odd, the Wilson weight, small β.* Let W be the Wilson line of length L in direction 1. Each plaquette holds at most 2 of the 2L links of W and its mirror, so the lowest contributing order in β is L, from the L side plaquettes of a plane joining them, and each link is covered exactly twice. The closed surface formed by the sides and the two lines is a sphere, which gives E[a_W a_{θW} ∏ a_side] = 4^{−(L+1)}. For L = 3 this is 1/256, and the scan and the exact sums confirm it at T = 4. So at T ≥ 4, N_β(a_W) exp(βN_p) = β^L/4^{L+1} + O(β^{L+1}), negative for small β < 0. At T = 2 both planes join them and the coefficient doubles. On the two-dimensional lattice (ℤ/L) × (ℤ/2) with the Wilson weight the same computation is exact for every β: N_β(a_W) = (1/2) Σ_n t_n t_{n+1} with t_n = (exp(−β) l_n(β))^L, and for β < 0 and L odd every term is negative. The test measures this at L = 3, β = ±1.

*L even.* Put η_μ(x) = (−1)^{x₁+…+x_{μ−1}} with time last, and (ηU)_μ(x) = η_μ(x) U_μ(x). This is periodic when every spatial side is even. Then a_p(ηU) = −a_p(U) for every plaquette, the map preserves Haar measure, and it commutes with both reflections because η does not depend on t. So for β < 0, N_β(F) = exp(−2βN_p) N_{−β}(F∘η) ≥ 0, and on a lattice with every spatial side even, link reflection positivity holds for every real β. The test measures the flip on 96 of 96 plaquettes at (2,2), 192 of 192 at (2,4) and 432 of 648 at (3,4), and on (ℤ/2) × (ℤ/2) with Q8 the weight with c_{2dim} = −1 gives the same PSD kernel as its positive twin.

**Remark 6.3 (the gauge used in the literature).** At T ≥ 4 the crossing links form a forest, so for gauge-invariant F they can be set to 1, and the plane kernel becomes B alone. At T = 2 the links V(x,0) and V(x,1) close a loop at each x whose class is gauge invariant, so that gauge is unavailable. Step 6 and the link-splitting proof in Knowles' thesis cover T = 2.

## 7. The transfer operator

Let the spatial lattice have N_ℓ links and N_s plaquettes, 3L³ each in four dimensions. Let H = L²(SU(2)^{N_ℓ}), with normalized Haar measure. Define A, multiplication by exp(−S_spatial); B, the product over spatial links of K(U,U′) = exp(−β(1 − (1/2) Re Tr(U U′⁻¹))); P, the gauge projector; and T_op = A^{1/2} B A^{1/2}.

**Theorem 5.** Let β > 0 and N_t ≥ 1.

(a) *Operator positivity.* B is strictly positive and trace class, with eigenvalues ∏_ℓ exp(−β) l_{2j_ℓ}(β) on products of matrix coefficients and Tr B = 1. T_op is self-adjoint, injective, positive and trace class, with Tr T_op = ∫A.

(b) *Gauge symmetry.* A and B commute with the gauge action, so T_op commutes with P.

(c) *The trace identity.* On the lattice with N_t time steps, Z = Tr(T_op^{N_t} P) = Tr over PH of T_op^{N_t}.

(d) *The top eigenvalue.* T_op has a continuous, strictly positive kernel. Its largest eigenvalue λ₀ on H is simple, with a strictly positive continuous eigenfunction Ω, and every other eigenvalue is strictly smaller. Ω is gauge-invariant.

(e) *The gap at fixed L and β.* On the gauge-invariant subspace the next eigenvalue satisfies 0 < λ₁ < λ₀, so log(λ₀/λ₁) ∈ (0, ∞), in lattice units.

*Proof.* The steps are kept separate, as GPT-6 asked. Operator positivity (a) comes from the character expansion. Simplicity and isolation (d) come from compactness and positivity of the kernel. For β < 0, K is pointwise positive and has negative eigenvalues, which is why these are two steps.

(a) By section 5, K has the complete eigenbasis D^j_{ab} with eigenvalues exp(−β) l_{2j}(β) > 0 and trace 1, and B is the tensor product over finitely many links. A^{1/2} is real, continuous and bounded with a bounded inverse, since w_β > 0. So ⟨f, T_op f⟩ = ⟨A^{1/2} f, B A^{1/2} f⟩ > 0 for f ≠ 0, and T_op is trace class as a product of bounded and trace class operators. Since T_op has a continuous kernel and is positive, Mercer's theorem gives Tr T_op = ∫ A(U) B(U,U) dU = ∫A, because K(U,U) = w(1) = 1.

(b) S_spatial is gauge invariant by Lemma 0001. B is by section 6, step 4. (R_g f)(U) = f(U^g) is unitary because Haar measure is invariant, and P = ∫R_g dg is an orthogonal projection, since Haar measure on the gauge group is bi-invariant.

(c) Let U_t be the spatial links at time t and V_t the time links from t to t+1. By section 6, step 3, the time-like plaquettes between t and t+1 give B(U_t, U_{t+1}^{V_t}), and the V_t integral gives (BP)(U_t, U_{t+1}), the kernel of BP. The spatial plaquettes at t give A(U_t). So Z = Tr((A BP)^{N_t}). Cyclicity, and the fact that P commutes with A^{1/2} and B and P² = P, turn this into Tr((T_op P)^{N_t}) = Tr(T_op^{N_t} P). The kernel of (A BP)^{N_t} and the kernel of (T_op P)^{N_t} agree on the diagonal, and (T_op P)^{N_t} is positive with a continuous kernel, so Mercer's theorem makes its trace the integral of that diagonal, which is the lattice integral.

(d) T_op(U,U′) = A^{1/2}(U) B(U,U′) A^{1/2}(U′) is continuous and strictly positive, since w_β > 0. T_op is compact and self-adjoint, so λ₀ = ‖T_op‖ > 0 is an eigenvalue, with real eigenfunctions since the kernel is real. Let f be one, normalized. Then ⟨|f|, T_op |f|⟩ ≥ ⟨f, T_op f⟩ = λ₀, and the variational bound gives equality. Strict positivity of the kernel then forces f to have one sign almost everywhere, and T_op|f| = λ₀|f| > 0 everywhere, so |f| is continuous and strictly positive. Two orthogonal functions cannot both have one sign, so λ₀ is simple. Call the positive eigenfunction Ω. Eigenvalues of a compact operator accumulate only at 0, so the rest lie strictly below λ₀. R_gΩ is a positive eigenfunction of the same norm for the same eigenvalue, so R_gΩ = Ω and PΩ = Ω.

(e) By (d), λ₀ is the top eigenvalue on PH, simple there, and the next one is strictly smaller. PH is infinite-dimensional, since it holds every function of a Wilson loop holonomy, and T_op is injective, so the next eigenvalue is positive. ∎

**Proposition 6 (Collatz–Wielandt).** For every continuous f > 0, min_U (T_op f)(U)/f(U) ≤ λ₀ ≤ max_U (T_op f)(U)/f(U). With f = A^{−1/2} this gives the explicit bound

```text
(exp(-beta) l_0(beta))^N_links exp(-2 beta N_s)  <=  lambda_0  <=  (exp(-beta) l_0(beta))^N_links.
```

*Proof.* λ₀⟨Ω,f⟩ = ⟨Ω,T_op f⟩ = ⟨Ω f, (T_op f)/f⟩, so λ₀ is a weighted average of (T_op f)/f with positive weights Ωf. For f = A^{−1/2}, T_op f = A^{1/2} B 1 = A^{1/2}(exp(−β) l₀(β))^{N_ℓ}, since K acts on constants by the spin-0 eigenvalue, so the ratio is A(U)(exp(−β) l₀(β))^{N_ℓ}, with A between exp(−2βN_s) and 1. ∎

This controls the leading eigenvalue only. Certifying λ₁ and a quantitative gap needs further spectral bounds: OPEN.

**Remark 7.1 (the two reflections through T_op).** Let F be gauge-invariant and act by multiplication on one slice. For link reflection, with F at t = 0 and θF at t = −1, N(F) = Tr(P F̄ T F T^{2m−1}) = Σ_{ij} λ_i λ_j^{2m−1} |⟨i|F|j⟩|², which uses T ≥ 0. For site reflection, with F at t = s and θF at t = −s, N(F) = Tr(P F̄ T^{2s} F T^{2m−2s}) = Σ_{ij} λ_i^{2s} λ_j^{2m−2s} |⟨i|F|j⟩|², which uses only that T is self-adjoint, and that is where A ≥ 0 enters, through the real root A^{1/2}. For β < 0 the operator T_op stays self-adjoint, and B on PH has eigenvalue signs (−1)^{number of half-odd links}. Half-odd links form closed cycles on PH, so on a lattice with even sides these signs are +1, and on an odd L the winding loop gives −1 and, by Sylvester's law of inertia, T_op has a negative eigenvalue on PH.

## 8. Exact tests

`python3 -I -X utf8 tests/test_reflection_transfer_4d.py`. Python standard library, integers only, with exact rationals as pairs of plain ints. [`integer_only_audit.py`](https://github.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C/blob/main/native/scripts/integer_only_audit.py) reads 0 violations, and the stricter draft `no_float_gate` reads 0 findings, since every exponent is a literal or goes through an integer power that refuses a negative exponent. Local run with the second-round rows: 40 s wall at below-normal priority, Python 3.13.14, against the prediction's limit of 900 s. The first round measured 30 s. The hosted run [41727758077](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/41727758077) on commit c31a033, on ubuntu-24.04, read the same bytes as the receipt, and each sabotage exited 1 there. The hosted run [41748399166](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/41748399166) on commit d382636, on ubuntu-24.04, did the same for the second-round rows, with a job of 40 s, and each of the twelve sabotages exited 1 there on the check that names it. All values are MEASURED unless a row says otherwise.

| Part, prediction row | Measured | Met |
|---|---|---|
| A, `YM4_02C_GEOMETRY` | The table of section 3, for both reflections | yes |
| A, `YM4_02C_ACTION_SPLIT` | Exact on two configurations per lattice and reflection | yes |
| B, `YM4_02C_CHARACTER` | 105 identities through β²⁰ at traces 2, 1, 0, −1, −2, 0 failures. 121 coefficients of (n+1) l_n read by a separate route, E[τ^m χ_n]/(2^m m!) with the moments from the S³ measure: each equals the formula, all positive, and zero off parity. (n+1) l_n = I_n − I_{n+2} and Σ(n+1)² l_n = exp β, through β²⁰ | yes |
| B, `YM4_02C_BALLOT` | Against quadrature: Q8 10 pairs through m+n = 3, 2T 21 through 5, 2O 36 through 7, 2I 78 through 11. Next degree differs: E[τ⁴] 4 vs 2, E[τ⁶] 6 vs 5, E[τ⁸] 15 vs 14, E[τ¹²] 133 vs 132. Haar directly, from the S³ moments: 325 pairs through m+n = 24 | yes |
| C, `YM4_02C_CYLINDER` | Lattice (ℤ/3)³ × (ℤ/4), 9 links, 6 sites, 4 free, degree 2 per link. Q8 = 1/256, 2T = 1/256. Without the sides 0, with two sides 0. Scan of 648 plaquettes: at most 2 W-links per plaquette, exactly 3 plaquettes with 2, which are the sides, so the β³ coefficient is 1/256 and lower orders vanish | yes |
| D, `YM4_02C_TORUS_2D` | Q8 at (2,2): 69425/16. Q8 at (3,2): 16917185/64. 2T at (2,2), c = 7, 2, 1, 4, 3, 1, 2 on 1, ω, ω², 3, 2, 2ω, 2ω², a complex weight: 1572881/648, imaginary part 0. Each direct sum equals Σ c_ρ^F d_ρ^{−F} | yes |
| E, `YM4_02C_GRAM_LINK` | G_FF = 593/4, PSD rank 5, all principal minors non-negative, Z = 16917185/64 | yes |
| E, `YM4_02C_GRAM_LINK_RED` | G_FF = −593/4, negative pivot, Z = 16917185/64, weight pointwise positive | yes on the value, see section 10 on its `meaning` |
| E, `YM4_02C_GRAM_SITE` | PSD rank 15 on 15 functions for both weights, and for values 3, −2, 1, −1, 2 on the classes | yes, see section 10 on its `meaning` |
| G, `YM4_02C_SIGNED_SITE` | −15/64, Z = 1/16, negative pivot. P(s = −1) = 3/8 from 24 of 64 pairs | yes on the value, see section 10 on its `meaning` |
| G, `YM4_02C_SIGNED_SITE_CONTROL` | 45/64, Z = 81/16, PSD rank 7 | yes |
| F, `YM4_02C_TRANSFER_TEST` | Spatial (ℤ/2) × (ℤ/1), one step, 262,144 terms over links and gauge group: Tr(ABP) = 2571382 = direct sum on (ℤ/2) × (ℤ/1) × (ℤ/1), with and without a forest fixed, and = the trace over the 176 gauge orbits. c_{2dim} = −1: 2283606 | yes |
| Sabotage, `YM4_02C_TEETH` | `no_inverse_on_time_links`, `wrong_plane`, `wrong_multiplicity`, `negative_weight_called_positive`, `signed_site_weight_called_positive`, `bad_projector`, and from the second round `no_inverse_in_gram`, `wrong_plane_in_gram`, `dropped_inverse_third_letter`, `dropped_inverse_fourth_letter`, `every_function_one_plane`, `t4_half_weights_dropped`: each exits 1 on a named check, with no traceback | yes |
| `YM4_02C_COST` | 30 s at c31a033, 40 s with the second-round rows, limit 900 s | yes |

**N_t = 2.** Spatial (ℤ/1) × (ℤ/1) on (ℤ/1) × (ℤ/1) × (ℤ/2), 8⁶ assignments: Tr(T²P) over 28 orbits = direct sum = 2571382, and 2283606 at c_{2dim} = −1. That lattice is (ℤ/2) × (ℤ/1) × (ℤ/1) with its axes renamed, so the row `TWO_SLICINGS` compares one step on one slicing with two steps on the other, and they agree. On spatial (ℤ/2) × (ℤ/1) the direct sum has 8⁹ gauge-fixed leaves, minutes in pure Python, so its row reads `NOT_MEASURED`, reason `BUDGET`, and the smaller case above stands in, with the 176-orbit trace 8835582291457/16 recorded. The second seat ran that direct sum over the 8⁹ leaves in Rust, in 7 s wall at below-normal priority, and read 74118236294774521856/8⁹ = 8835582291457/16 at both signs of c_{2dim}. The row `TRANSFER_DIRECT_SECOND_SEAT`, beside the `NOT_MEASURED` row, compares the orbit trace here with that value, tagged as its measurement.

**Further rows beyond the prediction.**

| Row | Measured |
|---|---|
| `TORUS_SU2_ENCLOSURE`, SU(2) itself, Z = Σ_n (exp(−β) l_n(β))^F on the 2D torus at β = 1, enclosed by exact rationals | (2,2): 0.029996399843 ≤ Z ≤ 0.029996399844, exp(−4) ≤ 0.018315638889. (3,2): 0.005170360694 ≤ Z ≤ 0.005170360695, exp(−6) ≤ 0.002478752177 |
| `SU2_GRAM_2D`, SU(2) on (ℤ/3) × (ℤ/2), F = a_W | At β = +1 the numerator over exp(−6) lies in 0.014450588093 to 0.014450588094. At β = −1 the numerator over exp(+6) reads −0.014450588094 on the partial sum, every term negative. The series of (1/2) Σ_n (l_n l_{n+1})³ multiplied out from the l_n coefficients reads 0, 0, 0, 1/128, 0, 5/1024, 0, 71/49152, 0, 133/491520 through β⁹, so the β³ coefficient is 1/128, twice the value of the `CYLINDER` row, one strip per plane |
| `GRAM_LINK_T4`, (ℤ/1) × (ℤ/4), Q8 | ±2389/8 = ±(t³_E (t₀ + 3t_s) + t_E (t₀³ + 3t³_s)), with t = c/d. PSD rank 9, and a negative pivot for the minus sign |
| `EVERY_FUNCTION`, T = 2 | (ℤ/1) × (ℤ/2): PSD rank 5 for c_{2dim} = +1, negative pivot for −1. (ℤ/2) × (ℤ/2): PSD rank 5 for both signs. The sum of all entries is 8^links Z: 373760 and 72797388800. The entry at (1, 1) is the square of one plane's sum: 23104 and 14400, and 34668544 at both signs. A dropped plane turns the row red |
| `EVERY_FUNCTION_T4` | (ℤ/1) × (ℤ/4): PSD rank 25 for +1, negative pivot for −1. The sum of all entries is 72797388800, and the entry at all 1 is (8 w(1))⁴: 533794816 and 207360000. A dropped half weight turns the row red |
| `EVERY_FUNCTION_SITE`, (ℤ/1) × (ℤ/2) | All 512 point functions of the closed half with values 3, −2, 1, −1, 2 on the classes: 64 blocks, each PSD of rank at most 1 |
| `LINK_SPECTRUM`, Q8 | Eigenvalues 8, 3, 3, 3, 1/2 with multiplicities 1, 1, 1, 1, 4 on the four signs and four quaternion coordinates. Trace 19 = w(1) |
| `BP_FORM`, (ℤ/1) × (ℤ/1) | BP on the 28-dimensional gauge-invariant space: rank 28 for +1, negative pivot for −1 |
| `NO_PROJECTOR` | Tr(AB) = 47567165/4 = the direct sum with every time link set to 1. Z = Tr(ABP) = 2571382 |
| `COLLATZ_WIELANDT`, Q8, 176 orbits | M = ABP has positive entries. f = 1 gives exactly A(U) c₀⁴, so 102400 ≤ λ₀ ≤ 1478656. After 24 power steps, 466057.523684 ≤ λ₀ ≤ 466058.045586. λ₀ and λ₀² lie below the traces at N_t = 1, 2. λ₁: OPEN |

**Rows from the second seat's findings.** Each was predicted in `docs/PREDICTION-YM4-02c.hbp` before it ran, in commits df6ff5c and c46cb4c, with the value the second seat had seen where it had one. Every predicted value was met. The rank 17 of `GRAM_SITE_MOVED` and the counts 12,288 and 10,944 in `SITE_CHARACTER` were printed here first. `SITE_SHARP_BLOCK` ran with no prediction row of its own, and it reads the formula of `YM4_02C_SITE_SHARP_FORM` on one block; a row beside the prediction records this.

| Row | Measured here | The second seat, its own MEASURED |
|---|---|---|
| `SITE_SHARP`, `SITE_SHARP_BLOCK` | The table of section 4, on pairs of the 176 orbits | The literal walks over 8⁸ C and 8¹⁰ point functions |
| `SITE_CHARACTER` | Remark 4.2 | |
| `SINGLE_W_SITE` | (ℤ/1)² × (ℤ/2), lowest N(δ_C) over 8⁶ and Z: w = 1, −1, 1, 1, 1: −64, 7/64. w = 3, 1, 1, 1, 1: 64, 1179/64. w = 3, 1, −2, 1, −1: 64, 2253/64. w = −1: 64, 1. (ℤ/1)³ × (ℤ/2), over 8⁸: −64, 11/128. 64, 170535/128. 192, 423723/128. 64, 1 | The same values |
| `NEGATIVE_COEFFICIENT` | Remark 6.2. G_EE = 1130 and 527/4, Z = 263604 and 16785473/64, each equal to the rule | The inertias, from its literal 8¹² histogram |
| `T4_RED_WITNESS` | −8 and −4, each equal to the rule of Remark 6.2 | |
| `GRAM_SITE_MOVED_BLOCKS`, `GRAM_SITE_MOVED`, `GRAM_SITE_MOVED_RED` | Section 11 | 3648 and −6351452416 |
| `EVERY_FUNCTION_T4_OPEN_HALF` | 25 positive, 0 negative, and 17, 8 at c_{2dim} = −1, on all 512 functions | The same values |
| `FOUR_D_LINK` | (ℤ/1)³ × (ℤ/2), every point function of the slice reduced to 176 orbits. c_{2dim} = +1: 176 positive, 0 negative, G_FF = 5696786251574 for F = χ_{2dim}(U₁), Z = 366894732506723/16. c_{2dim} = −1: 112, 64, G_FF = −1965328413750, Z = 257883799138323/16. Each Z equals Tr(T²P) and the direct sum over 8⁷ gauge-fixed leaves | The same values, with the direct sum also over 8⁸ with no gauge fixing, and one step over 8960 orbits on spatial (ℤ/2) × (ℤ/1) × (ℤ/1) |
| `FOUR_D_TRANSFER` | N_t = 3 on spatial (ℤ/1)³: 559775981543075516869/16 and 333366012807212569335/16 | The direct sums, equal to those traces |
| `TRANSFER_DIRECT_SECOND_SEAT` | The orbit trace 8835582291457/16 at both signs | The direct sum over 8⁹ leaves |
| `W_INVERSE_CONTROL`, `LINK_2T` | Sections 3 and 6 | The same values |
| `PLAQUETTE_ORIENTATION` | Section 3 | A separate check: geometry from the universal cover, on 16 lattices |

**An independent reading.** The independent seat GPT-6 reported a C++17 enumeration of all 2,097,152 gauge-fixed assignments on the part E lattice, reading 593/4 and −593/4 with both weights pointwise positive and Z = 16917185/64. When the row `YM4_02C_EXTERNAL` was written its checker was held outside this repository. It has since entered main through [PR #12](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/12), at [`reviews/gpt6-q8-0e9bcff/`](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/tree/main/reviews/gpt6-q8-0e9bcff), with a replay. This branch forked before that merge. This run is separate Python code and reads the same values. The second seat ran a literal 8¹² = 68,719,476,736 pass with no gauge fixing on that lattice, in Rust, and reads them too.

## 9. Match against the literature

Peter–Weyl, Schur orthogonality and Mercer's theorem are used with their hypotheses matched in writing where they appear: compact group; continuous, symmetric, positive semidefinite kernel on a compact space with Haar measure of full support. The Jentzsch step is proved in Theorem 5(d) rather than imported.

| Statement here | Source | What was read | Result |
|---|---|---|---|
| Theorem 5(a), (b): T self-adjoint, bounded, gauge invariant, strictly positive | Lüscher, Commun. Math. Phys. 54 (1977) 283–292, Proposition 1(a), (b), (c), with (17), (20), (21) | The full preprint DESY 76/54, [KEK scan](https://lib-extopc.kek.jp/preprints/PDF/1976/7611/7611148.pdf), sha256 `2093c746…4e8d11`, and the journal abstract. The journal body is paywalled: CANNOT_SEE | MATCHED against the preprint. His pure-gauge part is T_G⁺ S T_G, with β = 2/g₀². He takes SU(N) with fermions and 0 < K < 1/6, and states that strict positivity reduces to the integral operator S on the gauge Hilbert space, which is the part used here. His box has odd sides 2L+1 and 2M+1, and his proof makes no use of that |
| Theorem 5(a), (b) | Knowles, [ETH diploma thesis](https://www.unige.ch/~knowles/diploma.pdf), (2.105)–(2.108), Lemma 2.1, Lemma 2.2 | Page images, PDF pages 27–30, sha256 `00e2ff42…be4e0e` | MATCHED. T = MTM, with M multiplication by exp[(1/2) Σ_p J_M (Re χ(g_p) − χ(1))] and T convolution with exp[Σ_b J_E (Re χ(g_b) − χ(1))], which is A^{1/2} B A^{1/2} at J_M = J_E = β/2 on SU(2). Lemma 2.1: strictly positive, from the eigenvalues (2.115) and the multiplicities (2.116). Lemma 2.2: [T, P_α] = 0 |
| Section 5, positive coefficients | Lüscher (22), (23) | Same | MATCHED. He writes the kernel as Σ_ν c_ν χ^{(ν)}(V), says (22) holds if and only if the c_ν are all positive, and gets positivity from the tensor-product multiplicities c_ν(n,m). For SU(2), c_ν(n,m) = B(n+m, ν) |
| Theorem 5(c), Z = Tr(T^{N_t} P) | Lüscher (25), (30), footnote 3 | Same | DIFFERENCE, recorded. His trace formula has no projector and is written for the gauge-fixed expectation, with all time links set to 1. Footnote 3 says that for cyclic boundary conditions his (7) holds only in the infinite volume limit, provided the color symmetry is unbroken. Here the time links are integrated at fixed volume and P appears, and `NO_PROJECTOR` measures the difference |
| Theorem 5(c), Z = Tr(T^{N_t} P) | Knowles, Lemma 2.3, (2.135), (2.137), proof (2.138)–(2.140), and Lemma 3.14, (3.184) | Page images, PDF pages 31 and 66 | MATCHED. (2.135) Z_α = tr[P_α T^{N₀}], (2.137) Z₀ = Z_Λ for periodic time, and the links between two layers are the gauge variable h in the trace. The second seat found this match. The difference from Lüscher in the row above stays |
| Theorem 5(d), simple top eigenvalue | Lüscher after (26): "If the largest eigenvalue of T is not degenerate, (26) becomes (27) … I do not know wether this happens for lattice gauge theories." Knowles §2.8, note 3: unique by Perron–Frobenius | Same; thesis, page image, PDF page 36 | The proof here holds at finite L for pure gauge, where the kernel is positive. Lüscher's sentence concerns the theory with fermions |
| Theorem 2, site reflection | Menotti–Pelissetto, Commun. Math. Phys. 113 (1987) 369–373, DOI 10.1007/BF01221251 | Abstract only, via Springer and OSTI: "We extend the proof by Osterwalder and Seiler … to the case in which the reflection is performed with respect to planes containing sites". Body: CANNOT_SEE, a bot wall and a paywall | NAMED. The hypothesis on the fixed slices could not be compared with theirs. Knowles §2.4.1 and §2.4.2 give the same split and keep exp(−S₀) ≥ 0 as a factor: MATCHED against the thesis. His (2.92), page image, PDF page 24, keeps that factor whole, which is the formula of Theorem 2 here |
| Theorem 4, link reflection | Osterwalder–Seiler, Annals of Physics 110 (1978) 440–471, DOI 10.1016/0003-4916(78)90039-8 | Abstract only, the Elsevier text through INSPIRE: "we verify physical positivity for the Schwinger functions of these approximations. This implies the existence of a positive self-adjoint transfer matrix." Body: CANNOT_SEE, a captcha page from ScienceDirect and no open copy found | NAMED. Statements unmatched against their text: the class of observables, the boundary conditions, and the case T = 2. Secondary, each opened: Menotti–Pelissetto place their planes as containing sites, as an extension; Jaffe–Janssens write that those proofs "fix the gauge on bonds that cross the reflection plane" |
| Theorem 4 and Proposition 4.1, every F | Jaffe–Janssens, arXiv:1607.07126, Corollary IX.2 | Section IX, full text | MATCHED. Compact Lie group, hypercubic lattice in ℝ^d or T^d, reflection plane halfway between lattice points, reflection positive for all values of g₀. "since our derivation does not use gauge invariance, we get reflection positivity of the full algebra" |
| Beside the row above, the printed sign | Jaffe–Janssens (V.5), Proposition V.6, (VII.2), (VII.3), Theorem VII.3, (IX.6), Theorem IX.1, Corollary IX.2, (IX.7) | Page images, PDF pages 26, 27, 32, 33, 43–45, sha256 `9df0224f…e5456ac9` | (V.5) and (VII.3) read −H = Σ J_IJ Θ(C_I) C_J, with Boltzmann factor exp(−βH), so a PSD J gives exp(+β Σ J_IJ Θ(C_I) C_J). Section IX prints S = Σ J_IJ Θ(U_I) U_J in (IX.6), exp(−βS) in Theorem IX.1, whose proof cites Theorem VII.3, and exp(−(1/(2g₀²)) S_YM) in Corollary IX.2, with S_YM the plus sum of traces over oriented plaquettes. Read literally, that is β = −2/g₀² in this lemma's parametrisation, the case measured red at L = 3 in `SU2_GRAM_2D`. This lemma reads section IX through (V.5), with weight exp(+(1/(2g₀²)) S_YM), which is Lüscher's (1), (2) and β = 2/g₀², and with that sign the row above stands. The second seat found this, and it was checked here on the page images |
| Proposition 4.1 | Jaffe–Janssens, section IX, introduction | Page image, PDF page 41: "any two elements of 𝔄₊ that differ by a gauge transformation that does not involve the reflection plane yield the same state in ℋ_Θ" | MATCHED. The second seat found this match. The difference from Lüscher in the last row of this table stays |
| Remark 6.3 | Knowles, [ETH diploma thesis](https://www.unige.ch/~knowles/diploma.pdf), 2005, §2.4.2, §2.4.3, sha256 `00e2ff42…be4e0e` | Read | For periodic time and even N₀ he uses a gauge with all crossing links 1, and §2.4.3 gives link splitting with no gauge fixing. The gauge is available from T = 4 up, and T = 2 takes the Schur step or the splitting |
| Eq. (4) of Lüscher for all F | Lüscher, section I: "we should not expect eq.(4) to be true for all quantities" | Preprint | DIFFERENCE, recorded. Proposition 4.1 gives N_w(F) = N_w(ΠF) for pure gauge, so it holds for all F, and for F outside the invariant sector it reads through the projection |

## 10. The prediction: what was met, and the misses

Every predicted value was met. Three clauses of the prediction need a correction, recorded here and as rows beside the originals in [`docs/PREDICTION-YM4-02c.hbp`](PREDICTION-YM4-02c.hbp). The original rows stay.

**Correction beside that count, found by the second seat.** The count is five: items 1 to 3 and items 4 and 5 below. The row `YM4_02C_CORRECTION` beside `YM4_02C_RESULT` keeps what `clauses_corrected_beside=3` said and adds this. No predicted value moved.

1. **MISS, found by this run.** `YM4_02C_GRAM_LINK_RED` says `meaning=reflection_positivity_fails_when_a_character_coefficient_is_negative`. On its own lattice, L = 3, the value and the failure are right. As a general statement it is wrong. The rule is t_ρ = (c_ρ/d_ρ)^L, so at L = 2 the sign of c_{2dim} cancels: `EVERY_FUNCTION` on (ℤ/2) × (ℤ/2) with c_{2dim} = −1 is PSD of rank 5. Corrected: non-negative coefficients are sufficient on every lattice, and Remark 6.2 gives the odd and even cases for the Wilson weight.
2. **MISS, the same clause.** `YM4_02C_GRAM_SITE` says `link_reflection_needs_positive_character_coefficients`. Corrected the same way, sufficient rather than necessary. Its first half, `site_reflection_needs_only_a_real_weight`, is the miss GPT-6 already found, corrected in `YM4_02C_CORRECTION`.
3. **Stale fact.** `YM4_02C_EXTERNAL` says `checker_held_outside_this_repository=1`. That was true when written. PR #12 has since brought the checker into main.
4. **MISS, found by the second seat.** `YM4_02C_SIGNED_SITE` says `meaning=site_reflection_positivity_fails_for_a_signed_weight_on_fixed_slice_plaquettes`. On its own lattice the value −15/64 and the failure are right. As a general statement it fails the test item 1 applied: on (ℤ/2) × (ℤ/1) × (ℤ/2), w = 3, 2, 1, −1, −2 is negative on half of the fixed-plaquette evaluations and PSD on all 8¹⁰ point functions. Corrected: the sign that acts is that of f(C), Theorem 2.
5. **MISS, found by the second seat.** `YM4_02C_CORRECTION` beside `YM4_02C_GRAM_SITE` says `corrected=the_weight_must_be_real_and_non_negative_on_plaquettes_of_the_fixed_slices_since_each_is_split_in_half`. Corrected: that condition is sufficient, and the split in half is a convenience. Its `Wilson_action=positive_so_all_real_beta_hold` stands.
6. **Scope, found by the second seat.** The clause `a_negative_one_fails_on_odd_L_here` in the `YM4_02C_MISS` row beside `YM4_02C_GRAM_LINK_RED` holds for c_{2dim} < 0. On (ℤ/3) × (ℤ/2), c = 8, −1, 3, 3, 2 has 5 positive and 0 negative, so at T = 2 the sign of a sign-character coefficient depends on the weight, Remark 6.2.

Two hypotheses are made more exact, with no predicted value moved. The weight needs w(g⁻¹) = w(g), automatic on SU(2) and Q8, because a time-like plaquette maps to itself reversed. And the Jensen step uses E[a_p] ≥ 0, with E[a_p] = 0 for L ≥ 2 and E[a_p] = 1/4 on a commutator.

**Wording changed after the attack at 1618199.** The commit holds the earlier text.

| Where | Earlier | Now |
|---|---|---|
| Section 1, Theorems 2 and 4 | bounded function | bounded measurable function |
| Section 1 | the controls use k = 1 and k = 2 as well | a sentence naming the rows at k = 3 and those at k = 1, 2 |
| Section 2 | The prediction's route used E[a_p] = 0 | The prediction's row names S ≥ 0 and Jensen |
| Theorem 2 | one weight w, with w ≥ 0 on the values taken by plaquettes of the fixed slices | weights w_p with w_{θp} = w_p, the formula with f(C), and that pointwise form named sufficient |
| Theorem 2, step 2 | Square root. This is the step that a signed weight on a fixed slice breaks | The root is a convenience. A signed weight on a fixed slice acts through the sign of f(C) |
| Section 4 | On plaquettes of the upper and lower sets w may take either sign | The upper and lower weights may take either sign and may differ from one mirror pair to the next |
| Theorem 4 | on a group whose characters are real | clause dropped, with the `LINK_2T` rows |
| Remark 6.2 | Whether a negative coefficient breaks positivity depends on the lattice | It depends on the lattice, on T and on the weight |
| Section 9 | For SU(2) those multiplicities are B(m,n) | c_ν(n,m) = B(n+m, ν) |
| References | Knowles, sections 2.4 and 2.5 read | The list that section 9 cites |

The row name `EVERY_FUNCTION_T4` covers the 64 functions of (U(0), U(1)), and `EVERY_FUNCTION_T4_OPEN_HALF` now covers the open half. The commit title of c31a033 says "proved in full". The status of these proofs is DERIVED, with review by a different model family OPEN, and that title stays as pushed.

## 11. Issue #2's acceptance tests

| Test | Where |
|---|---|
| (1) Z > 0 and Z ≤ 1 | Theorem 1, with the SU(2) enclosures of section 8 |
| (2) Character and Haar identities with enclosures | Section 5 and part B: exact identities directly for SU(2), with the Catalan moments from the S³ measure, and `TORUS_SU2_ENCLOSURE`, `SU2_GRAM_2D` with explicit rational enclosures |
| (3) The reflection and boundary links | Section 3, with `PLAQUETTE_ORIENTATION` for the words |
| (4) PSD Gram matrices with red controls | Parts E and G, the `EVERY_FUNCTION` rows, `FOUR_D_LINK` and `GRAM_SITE_MOVED`, with the sabotage controls. An invalid weight goes red at `GRAM_LINK_RED`, `SIGNED_SITE`, `SITE_SHARP`, `FOUR_D_LINK` and `W_INVERSE_CONTROL`. An invalid reflection goes red at `GRAM_SITE_MOVED_RED`, see below |
| (5) Independent review against Osterwalder–Seiler and the transfer-matrix literature | OPEN. Section 9 is this seat's match. The body of Osterwalder–Seiler remains to be read, and GPT-6's review covered the prediction. A second seat of the same model family attacked this lemma and read Lüscher, Knowles and Jaffe–Janssens, [`reviews/opus55-ym4-02c/`](../reviews/opus55-ym4-02c/), with the same CANNOT_SEE list |

**What an invalid reflection reaches.** The sabotages `no_inverse_on_time_links` and `wrong_plane` run part A alone, so they reach the six `REFLECTION` rows, and each exits 1 there. At commit 1618199 no Gram, PSD or transfer row reacted to an invalid reflection, as the second seat measured: with the inverse dropped in a full run, only the six `REFLECTION` rows and `EVERY_FUNCTION_SITE` changed, the last through its literal mirror check. The reason is side 1: a side-1 plaquette of Q8 holds v twice and v⁻¹ = ±v, so its weight is equal with or without the inverse, and the mutants `no_inverse_only_part_G` and `every_site_block_mirror_no_inverse` still change no row. So the Gram control sits on (ℤ/2) × (ℤ/2), with c = 8, 3, 3, 3, 1, site reflection, and the mirror taken from `Reflection.link`. With the correct mirror, all 4096 fixed (A, B) give a rank-one square on the 64 point functions of (V(0,0), V(1,0)). On 1 and the 16 products of a coordinate of V(0,0) and a coordinate of V(1,0), which gauge transformations move, the Gram matrix is PSD of rank 17, with G_FF = 91/128 for F = e₁(V(0,0)) e₀(V(1,0)) and Z = 69425/16. With the inverse dropped, `GRAM_SITE_MOVED_RED` reads: 3648 of 4096 lose symmetry, the form reaches −6351452416 at (A, B) = (0, 0, 2, 3) in element indices, and G_FF = −91/128. The sabotages `no_inverse_in_gram` and `wrong_plane_in_gram` run this row alone, through `Reflection.link`, and exit 1 on the check `gauge-moved site Gram`. In a full run of this script with the inverse dropped, a mutant measured here, 11 named checks fail: the six `REFLECTION` rows, `EVERY_FUNCTION_SITE`, the two rows of `EVERY_FUNCTION_T4_OPEN_HALF`, and the two gauge-moved rows. With the plane moved, 22 named checks fail, among them `the mirror of W`, `cylinder`, the part G rows and the site blocks.

## 12. Open items

- Uniformity of anything here in L, T or β.
- λ₁ and a quantitative gap for SU(2), and the gap in physical units (YM4-06).
- Reading the bodies of Osterwalder–Seiler (1978) and Menotti–Pelissetto (1987) against Theorems 2 and 4.
- The direct sum at N_t = 2 on spatial (ℤ/2) × (ℤ/1) in Python: `NOT_MEASURED`, reason `BUDGET`. MEASURED by the second seat in Rust, 8835582291457/16, equal to the orbit trace here. The literal 8¹² pass on that lattice with no gauge fixing: `NOT_MEASURED` by that seat, reason `BUDGET`.
- On odd L at T ≥ 4, a negative coefficient for a weight that is not pointwise positive: the second seat's CONJECTURE, red on every sample.
- Odd T, where the reflection has one fixed slice and one crossing plane, as in Lüscher's box.
- Independent review of this lemma by a different model family.

## References

- K. Osterwalder, E. Seiler, Gauge field theories on a lattice, Annals of Physics 110 (1978) 440–471, [DOI](https://doi.org/10.1016/0003-4916(78)90039-8). Abstract read.
- M. Lüscher, Construction of a selfadjoint, strictly positive transfer matrix for Euclidean lattice gauge theories, Commun. Math. Phys. 54 (1977) 283–292, [DOI](https://doi.org/10.1007/BF01614090). Preprint DESY 76/54 read in full.
- P. Menotti, A. Pelissetto, General proof of Osterwalder–Schrader positivity for the Wilson action, Commun. Math. Phys. 113 (1987) 369–373, [DOI](https://doi.org/10.1007/BF01221251). Abstract read.
- A. Jaffe, B. Janssens, Reflection positive doubles, [arXiv:1607.07126](https://arxiv.org/abs/1607.07126). (V.5), Proposition V.6, (VII.2), (VII.3), Theorem VII.3 and section IX read, on page images.
- A. Knowles, Lattice Yang–Mills theory and the confinement problem, diploma thesis, ETH Zürich, 2005, [PDF](https://www.unige.ch/~knowles/diploma.pdf). Sections 2.4, 2.5, 2.6 and 2.7.1, note 3 of section 2.8, and Lemma 3.14 of section 3.3.3 read.
