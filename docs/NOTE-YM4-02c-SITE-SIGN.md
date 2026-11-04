# Which weights keep their sign on a fixed slice

**Status: DERIVED by the seat ACER-CLAUDE-FABLE5 on November 3, 2026. Independent review OPEN.** The operator asked that this be checked as a theorem, beyond finite samples. The prediction for its controls is [`PREDICTION-YM4-02c-SITE-SIGN.hbp`](PREDICTION-YM4-02c-SITE-SIGN.hbp), and the rows of its controls are in [`tests/SITE_SIGN_RECEIPT.txt`](../tests/SITE_SIGN_RECEIPT.txt). A second seat, sharing a model family with the builder, attacked this note at commit 1078e6d, and the theorem and every step of the proof held. Its files are in [`reviews/opus55-site-sign/`](../reviews/opus55-site-sign/README.md), and its findings are applied here. GPT-6's review is preliminary, and the operator asked for its final check.

It supports [Lemma 0004](LEMMA-0004-REFLECTION-TRANSFER.md), which holds its sharp form, and the lemma and this note land together, in one pull request. The sharp form says that site reflection positivity holds for every bounded F exactly when f(C) ≥ 0 for almost every C at which the half-lattice weight is not almost everywhere zero. This note asks which single weights satisfy that. The Wilson weight is strictly positive, so its site reflection positivity follows from the lemma alone.

## Setting

G is a compact second-countable group with normalized Haar measure. The spatial lattice is Λ = ∏ᵢ ℤ/Lᵢ with k ≥ 2 directions and every Lᵢ ≥ 2. A configuration C assigns one element of G to each positively oriented link, under the product Haar measure. Let w be a bounded measurable real class function with w(g⁻¹) = w(g) and w ≠ 0 almost everywhere, and let s = sign w, defined almost everywhere. Set

g(C) = ∏_p w(U_p), S(C) = ∏_p s(U_p).

Site reflection has two fixed slices, t = 0 and t = m, each a copy of Λ with its own independent links, so f(C₀, C_m) = g(C₀) g(C_m).

## Theorem

f ≥ 0 almost everywhere if and only if s = εκ almost everywhere, for some ε ∈ {+1, −1} and some continuous homomorphism κ: G → {+1, −1}.

**Corollary.** If G is connected, and in particular if G = SU(2), then f ≥ 0 almost everywhere if and only if w has one sign almost everywhere.

## Proof

Each step names what it uses, since those are the places it could fail.

**Step 0, g is nonzero.** Since every side is at least 2, each plaquette holds four distinct links, so U_p is Haar distributed. So w(U_p) ≠ 0 almost everywhere, there are finitely many plaquettes, and S is defined and equals sign g almost everywhere.

**Step 1, one sign of S.** C₀ and C_m are independent with one law. If S took both signs on sets of positive measure, then f < 0 on a set of positive measure. Conversely, if S ≡ ε almost everywhere then S(C₀) S(C_m) = 1 almost everywhere. So f ≥ 0 almost everywhere if and only if S is constant almost everywhere.

**Step 2, the "if" direction.** Let s = εκ. A homomorphism to {+1, −1} ignores order and inverses, so κ(U_p) is the product of κ(U_ℓ) over the links of p. Each link lies in exactly 2(k−1) plaquettes, once in each, which is an even number, so ∏_p κ(U_p) = 1. Hence S = ε^F is constant, with F the number of plaquettes.

**Step 3, one link at a time.** Let S ≡ ε almost everywhere. Fix a link ℓ = (x, μ) with value u. Since every side is at least 2, ℓ occurs once in each of its r = 2(k−1) ≥ 2 plaquettes. Orient and rotate each so that it reads u xᵢ, with xᵢ its staple. Here s(U_p) = s(u xᵢ) uses that w is a class function with w(g⁻¹) = w(g). The other plaquettes do not hold ℓ. So for almost every (u, rest),

∏ᵢ s(u xᵢ) = ε ∏_{p∌ℓ} s(U_p),

and the right side is free of u. By Fubini, for almost every value of the other links, u ↦ ∏ᵢ s(u xᵢ) is almost everywhere constant.

**Step 4, the staples are independent.** For the plaquette in direction σν from ℓ, with ν ≠ μ and σ = ±1, let eᵢ be its transverse link at the x+μ end: (x+μ, ν) for σ = +1, and (x+μ−ν, ν) for σ = −1. These are distinct for distinct (ν, σ), since L_ν ≥ 2. Each occurs in its own staple alone: the transverse links at the x end are (x, ν) and (x−ν, ν), which differ from these since L_μ ≥ 2, and the parallel links point along μ. Each staple is therefore a product holding one exclusive Haar link, so (x₁, …, x_r) is Haar distributed on Gʳ. **With a side of 1 this step fails.**

Hence for almost every (x₁, …, x_r) ∈ Gʳ, u ↦ ∏ᵢ s(u xᵢ) is almost everywhere constant.

**Step 5, from r points to two.** By Fubini, for almost every (x₂, …, x_r) and almost every pair (y, z), the statement holds both with x₁ = y and with x₁ = z. Multiply the two and use s² = 1: the factors with i ≥ 2 cancel. So for almost every (y, z) ∈ G², u ↦ s(uy) s(uz) is almost everywhere constant.

**Step 6, a continuous sign.** Let (R_h s)(v) = s(vh) and κ(h) = ∫ s(v) s(vh) dv = ⟨s, R_h s⟩ in L²(G). The right regular representation is strongly continuous, so κ is continuous, and |κ| ≤ 1 since ‖s‖₂ = 1. Substitute v = uy in Step 5, using invariance of Haar, and set h = y⁻¹z, the map (y, z) ↦ (y, h) preserving measure. So for almost every h, v ↦ s(v) s(vh) is almost everywhere constant, with value ±1, and that value must be κ(h). So |κ(h)| = 1 for almost every h. Haar measure has full support, so a set of full measure is dense, and by continuity |κ(h)| = 1 for every h. Equality in Cauchy–Schwarz gives R_h s = κ(h) s in L²(G), for every h.

**Step 7, a homomorphism.** R_{h₁} R_{h₂} = R_{h₁h₂} and s ≠ 0, so κ(h₁h₂) = κ(h₁) κ(h₂). So κ is a continuous homomorphism to {+1, −1}.

**Step 8, s is ±κ.** Let t = sκ. Then R_h t = t in L²(G) for every h: (R_h t)(v) = s(vh) κ(v) κ(h) = κ(h) s(v) κ(v) κ(h) = t(v). By Fubini, t(v) = ∫ t(vh) dh for almost every v, and this integral equals ∫ t by invariance of Haar. So t is almost everywhere a constant ε, and ε = ±1 since t = ±1. Hence s = εκ almost everywhere.

**Step 9, connected G.** The image of a connected group under a continuous map to {+1, −1} is one point, and a homomorphism takes 1 to 1, so κ ≡ 1 and s ≡ ε almost everywhere. ∎

The argument runs on every compact second-countable group, and it uses compactness for the finite normalized Haar measure, its invariance on both sides, and L² continuity.

## What the hypotheses do

**The side hypothesis.** The proof uses every side at least 2. The conclusion holds whenever two sides are at least 2 or one side is at least 3, given g ≠ 0 almost everywhere. Fix a link ℓ with value u, a plaquette p₁ holding ℓ once, and a link e held once by p₁ and by no other plaquette holding ℓ. With L_μ, L_ν ≥ 2, take ℓ = (x, μ), p₁ toward +ν and e = (x+μ, ν). With L₀ ≥ 3 and L₁ = 1, take ℓ = (x, 1), p₁ the plaquette of the plane (0, 1) at x and e = (x+0̂, 1), which stays out of the plaquette at x−0̂ because x+0̂ ≠ x−0̂. At fixed values of the other links, S = s(uy) A(u) B(e), with y Haar distributed in e, A free of e and B free of u. Read u ↦ s(uy) A(u) at two values y, z: since A² = 1, this is Step 5's conclusion, and Steps 6 to 9 run unchanged. Step 2 holds on every lattice, since each link is used an even number of times counted with multiplicity. The lattices left are (ℤ/2) × (ℤ/1)^{k−1} and (ℤ/1)^k, and there the answer depends on G. `SITE_SIGN_SIDES_LINK` reads on 13 lattices that such a link exists exactly where two sides are at least 2 or one side is at least 3.

On Q8 with the spatial slice (ℤ/2) × (ℤ/1), MEASURED over its 4,096 configurations, the class pairs of the two plaquettes are (+1,+1) 320, (+1,−1) 192, (−1,+1) 192, (−1,−1) 320, and 1,024 each on (±i,±i), (±j,±j), (±k,±k). So S is constant exactly when s(1) = s(−1). DERIVED from that table: 16 of the 32 sign patterns keep one sign there, against the 8 the theorem gives at every side at least 2. The weight 3, 2, 1, −1, 2 keeps its sign on that slice and its sign is no homomorphism.

MEASURED by `SITE_SIGN_SIDE_COUNT`: Q8 keeps 8 of 32 on (ℤ/3) × (ℤ/1) and (ℤ/2) × (ℤ/1) × (ℤ/2), the patterns of the theorem, and 16 of 32, those with s(1) = s(−1), on (ℤ/2) × (ℤ/1) × (ℤ/1) and (ℤ/1)³. On (ℤ/2) × (ℤ/1), S₃ keeps 4 of 8 and 2I keeps 2 of 512, the patterns of the theorem in both.

U(1) at (ℤ/2) × (ℤ/1) is the connected case: the second plaquette is the inverse of the first, so S = +1 for every sign with s(g⁻¹) = s(g), including signs that change on U(1). DERIVED, and `SITE_SIGN_U1` reads it on exact rational points of the circle, where a_p takes both signs, and on Z₃, Z₄ and Z₅, where every pattern stays constant.

On SU(2) at k = 2 the one-sign conclusion holds on both lattices left, DERIVED by the second seat and read through by this seat. On (ℤ/2) × (ℤ/1), with links a, b along direction 0 and c, d along direction 1, the plaquettes are a d a⁻¹ c⁻¹ and b c b⁻¹ d⁻¹. At fixed c and d, with real parts cos β and cos α, each plaquette's real part is uniform on [cos(α+β), cos(α−β)], and the two are independent, so a constant S makes s almost everywhere constant on that interval, and these intervals overlap across [−1, 1]. On (ℤ/1) × (ℤ/1), the commutator has density (π−θ)/(2 sin θ) against Haar measure at real part cos θ, positive for θ < π, with total mass 1 and mean real part 1/4, the value of the lemma's `COMMUTATOR` row, so a constant S makes s almost everywhere constant. **At k ≥ 3 on SU(2), the one-sign conclusion on (ℤ/2) × (ℤ/1)^{k−1} and (ℤ/1)^k is a CONJECTURE.** Its falsifier is a bounded class function on SU(2), nonzero almost everywhere and with both signs on sets of positive measure, whose S is almost everywhere constant on one of those lattices at some k ≥ 3. `SITE_SIGN_SU2_BANDS` reads 13 sign patterns of the real part, a_p among them, with both values of S on exact rational unit quaternions, on (ℤ/2) × (ℤ/1), (ℤ/1) × (ℤ/1), (ℤ/3) × (ℤ/1), (ℤ/2) × (ℤ/1) × (ℤ/1), (ℤ/1)³ and (ℤ/2) × (ℤ/1) × (ℤ/2).

**w ≠ 0 almost everywhere is needed.** Let δ < 1/3 in the norm of ℍ, and on SU(2) let w = +1 within δ of 1, w = −1 within δ of −1, and w = 0 elsewhere. Take k = 3. If all plaquettes lie in the support then each is σ_p times an element within δ of 1, with σ_p = ±1. The six faces of a cube multiply, after conjugations, to 1, as a word in the free group on its twelve edges, so the product of their σ_p is +1, since the remaining factor lies within 6δ < 2 of 1. So the faces with σ_p = −1 form a ℤ/2 cycle on the dual lattice. With every side even that lattice is bipartite, so the cycle has even length, and S = +1 wherever g ≠ 0. That w takes both signs on sets of positive measure, and with k = 3 and every side even, f ≥ 0 everywhere. The sign is seen: with a = iσ₁ on the 1-links at x₁ = 0 and b = iσ₂ on the 2-links at x₂ = 0, and 1 elsewhere, exactly one 12-plaquette in each 3-layer is −1, and a neighbourhood of that configuration has positive measure. With an odd side L₃ the same configuration has S = −1, so f takes negative values. With k = 2 no spatial cube constrains it, and one plaquette at −1 occurs at every side.

At each C with f(C) < 0 on the other lattices, W₊(C, ·) is zero: the cubes p × [t, t+1] carry S from each slice to the next, because the time-like faces cancel in pairs over all spatial p. In detail, if f(C) W₊(C, A) ≠ 0 then every plaquette of the closed half lies in the support, so the cube identity gives σ(p, t) σ(p, t+1) ∏_{ℓ∈∂p} σ(ℓ, t) = +1 for each spatial p, at any sides, since it is a word identity. Multiply over all spatial p: each spatial link lies in 2(k−1) spatial plaquettes, counted with multiplicity, so the time-like signs cancel, and S(C_t) = S(C_{t+1}). So f(C) = +1 wherever f(C) W₊(C, A) ≠ 0, and Theorem 2 of [the lemma](LEMMA-0004-REFLECTION-TRANSFER.md) gives site reflection positivity for this w on every lattice with T even, at every k and every side. f ≥ 0 is the sharp condition when w ≠ 0 almost everywhere, and W₊ enters when w has zeros. **The characterization for weights with zeros is OPEN.**

MEASURED on Q8 with w = 1, −1, 0, 0, 0 on the classes +1, −1, i, j, k, by `SITE_SIGN_ZEROS_T`. On (ℤ/1) × (ℤ/1) × (ℤ/2), of all 4,096 C, 1,920 have f(C) < 0 and W₊(C, ·) is zero on each of them, and the 256 C with W₊(C, ·) nonzero all have f(C) = +1. On (ℤ/1) × (ℤ/1) × (ℤ/4), all 1,024 paths through the middle slice keep g. On (ℤ/2) × (ℤ/2) × (ℤ/3) × (ℤ/2), the twist with the trivial slice has f = −1 and 0 V with every time-like plaquette central, and the twist with itself has 16,384 such V. MEASURED on SU(2) itself, on exact rational unit quaternions with δ = 8/25: `SITE_SIGN_SU2_TWIST`, `SITE_SIGN_SU2_NEIGHBOURHOOD`, `SITE_SIGN_SU2_CUBE` and `SITE_SIGN_CYCLE_PARITY`.

## Scope

This is a statement about one weight used on every plaquette, on fixed finite lattices. It adds a condition on general weights and leaves the Wilson theorem as it stands. Uniformity in volume and spacing, and everything after reflection positivity, stay OPEN.
