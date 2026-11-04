# Which weights keep their sign on a fixed slice

**Status: DERIVED by the seat ACER-CLAUDE-FABLE5 on November 3, 2026. Independent review OPEN.** The operator asked that this be checked as a theorem, beyond finite samples. The prediction for its controls is [`PREDICTION-YM4-02c-SITE-SIGN.hbp`](PREDICTION-YM4-02c-SITE-SIGN.hbp).

It supports [Lemma 0004](LEMMA-0004-REFLECTION-TRANSFER.md), whose sharp form says that site reflection positivity holds for every bounded F exactly when f(C) ≥ 0 for almost every C at which the half-lattice weight is not almost everywhere zero. This note asks which single weights satisfy that. The Wilson weight is strictly positive, so its site reflection positivity does not depend on this note.

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

The argument uses no Lie structure, and it uses compactness only for the finite normalized Haar measure, its invariance on both sides, and L² continuity.

## What the hypotheses do

**Every side at least 2 is needed.** On Q8 with the spatial slice (ℤ/2) × (ℤ/1), MEASURED over its 4,096 configurations, the class pairs of the two plaquettes are (+1,+1) 320, (+1,−1) 192, (−1,+1) 192, (−1,−1) 320, and 1,024 each on (±i,±i), (±j,±j), (±k,±k). So S is constant exactly when s(1) = s(−1). DERIVED from that table: 16 of the 32 sign patterns keep one sign there, against the 8 the theorem gives at every side at least 2. The weight 3, 2, 1, −1, 2 keeps its sign on that slice and its sign is no homomorphism.

**w ≠ 0 almost everywhere is needed.** Let δ < 1/3 in the norm of ℍ, and on SU(2) let w = +1 within δ of 1, w = −1 within δ of −1, and w = 0 elsewhere. Take k = 3. If all plaquettes lie in the support then each is σ_p times an element within δ of 1, with σ_p = ±1. The six faces of a cube multiply, after conjugations, to 1, so the product of their σ_p is +1, since the remaining factor lies within 6δ < 2 of 1. So the faces with σ_p = −1 form a ℤ/2 cycle on the dual lattice. With every side even that lattice is bipartite, so the cycle has even length, and S = +1 wherever g ≠ 0. That w takes both signs on sets of positive measure, and f ≥ 0 everywhere, so site reflection positivity holds for it on these lattices. The sign is seen: with a = iσ₁ on the 1-links at x₁ = 0 and b = iσ₂ on the 2-links at x₂ = 0, and 1 elsewhere, exactly one 12-plaquette in each 3-layer is −1, and a neighbourhood of that configuration has positive measure. With an odd side L₃ the same configuration has S = −1, so f takes negative values. With k = 2 no cube constrains it, and one plaquette at −1 occurs at every side. **The characterization for weights with zeros is OPEN.**

## Scope

This is a statement about one weight used on every plaquette, on fixed finite lattices. It adds a condition on general weights and leaves the Wilson theorem as it stands. Uniformity in volume and spacing, and everything after reflection positivity, stay OPEN.
