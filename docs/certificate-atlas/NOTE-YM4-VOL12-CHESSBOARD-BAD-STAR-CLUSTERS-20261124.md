# YM4-VOL12: an unconditional, volume-uniform bad-star cluster bound by closed-cube chessboard estimates

**Status:** PROOF-WRITTEN, not yet refereed.
- **Who wrote it:** Claude (an AI model, Anthropic) wrote this note on 24 November 2026.
- **Independent derivation:** a second AI seat derived the same route and the same constant independently on the same day. That is AI verification, not human review.
- **What is computed:** the finite, combinatorial and arithmetic parts are checked in exact integer arithmetic by [`tests/ym4_su2_vol12_chessboard_clusters.py`](../../tests/ym4_su2_vol12_chessboard_clusters.py). Its receipt is [`YM4-VOL12-CHESSBOARD-CLUSTERS-20261124.hbp`](YM4-VOL12-CHESSBOARD-CLUSTERS-20261124.hbp), against the prediction frozen first, [`PREDICT-YM4-VOL12-CHESSBOARD-CLUSTERS-20261124.hbp`](PREDICT-YM4-VOL12-CHESSBOARD-CLUSTERS-20261124.hbp).
- **Still OPEN:** external human mathematical review (YM4-08), odd side lengths, and every multiscale step.

## 0. Result

Take the four-dimensional SU(2) Wilson measure on the periodic torus (ℤ/L)⁴, with **L even and L ≥ 4**, coupling **β ≥ 1** and good-star tolerance **ε ∈ (0, 1)**. Put

$$A_\beta=1536\,e^{3/4}\beta^{3/2},\qquad \rho_D=A_\beta^4\,e^{-\beta\varepsilon/16},\qquad \rho_\star=6\,\rho_D^{1/4}=6\cdot1536\,e^{3/4}\beta^{3/2}e^{-\beta\varepsilon/64}.$$

Then, **uniformly in L**:

- **(C1)** For every finite set P of plaquettes, $\mu(D_p=1\ \forall p\in P)\le\rho_D^{|P|}$.
- **(C2)** For every finite set S of links, $\mu(S\subseteq\mathcal B_\varepsilon)\le\min\{1,\rho_\star^{|S|}\}$.
- **(D)** For every link o and every m ≥ 1, the bad cluster C(o) satisfies $\mu(|C(o)|\ge m)\le\min\{1,\,72^{m-1}\rho_\star^{m}\}\le\min\{1,\,18^{2(m-1)}\rho_\star^{m}\}$. In particular, **ρ⋆ ≤ 18⁻³ implies μ(|C(o)| ≥ m) ≤ 18^{−m−2}**.

(C2) is the joint input that VOL10 left OPEN, and it is stronger in three ways. It holds for **every** set S, with no independent-set extraction and no good-exterior conditioning, and the correlated bad-exterior case of VOL11 needs no separate treatment. VOL10's sufficient island threshold was ρ ≤ 18⁻⁵⁷. Here ρ⋆ ≤ 18⁻³ suffices.

This is a **single-lattice-scale** statement: large fields are rare. It is not a multiscale estimate and says nothing about the mass gap; see §8.

## 1. Setting and notation

- **The lattice.** Λ = (ℤ/L)⁴ with L even, L ≥ 4. A positively oriented link is e = (x, μ) from x to x + e_μ. A configuration assigns U_e ∈ SU(2) to each positively oriented link, with U of a reversed link equal to U_e⁻¹. A plaquette p = (x; μ < ν) has holonomy U_p, W_p = ½ tr U_p and a_p = 1 − W_p ∈ [0, 2]. The counts are N_E = 4L⁴ links and N_P = 6L⁴ plaquettes.
- **The measure** (deficit normalization). μ(dU) = (Z°)⁻¹ exp(−β Σ_p a_p) ∏_e dU_e, with normalized Haar measure. This equals VOL09's exp(β Σ W_p)/Z, since Z° = e^{−βN_P} Z.
- **Defects and bad stars.**
  - The defect indicator is D_p = 1{a_p > ε/4}, as in VOL10 §A.1.
  - The star of a link e has six staple vectors s_1,…,s_6. The link is **good** when all fifteen inequalities s_i·s_j ≥ 1 − ε hold (VOL08, 𝒢_ε(e)), and **bad** otherwise; write B_e = 1 for bad. 𝓑_ε is the set of bad links.
  - VOL10 (5a), from the VOL09 chordal inequality, gives pointwise **B_e ≤ Σ_{p∋e} D_p**.
- **Blocks.** For t ∈ Λ, the closed unit block is C_t = t + {0,1}⁴, with 16 sites, 32 links and 24 plaquettes.
- **Block transport.** τ_t maps C_0 onto C_t one coordinate at a time:
  - y_μ ↦ t_μ + y_μ if t_μ is even;
  - y_μ ↦ t_μ + 1 − y_μ if t_μ is odd (mod L).

  It is a composition of site reflections and is well defined because L is even (rows 04 and 06 of the checker). For a bounded function g of the links of C_0, (θ_t g)(U) := g(τ_t U), where (τ_t U)_e = U_{τ_t e}.
- **Site reflections.** ϑ = ϑ_{μ,k} is x_μ ↦ 2k − x_μ, acting by (ϑU)_e = U_{ϑe} and (ϑF)(U) = F(ϑU). Its closed halves are H⁺ = {x : (x_μ − k) mod L ≤ L/2} and H⁻ = ϑH⁺. They meet in the planes x_μ = k and x_μ = k + L/2.

## 2. VOL12-A: the chessboard estimate

**Lemma A.1 (reflection positivity through every site plane).** Fix μ and k. Let F and G be bounded real functions of the links with both endpoints in H⁺. Then E[F·ϑF] ≥ 0 and E[F·ϑG]² ≤ E[F·ϑF]·E[G·ϑG].

*Proof.* For μ = 4 and k = 0, this is [Lemma 0004](../LEMMA-0004-REFLECTION-TRANSFER.md), Theorem 2 (site reflection). The Wilson weights w_p = exp(−βa_p) are strictly positive, so f(C) > 0 there, every Gram matrix (N_w(F_a, F_b)) is positive semidefinite, and the Cauchy–Schwarz inequality follows. For general (μ, k), conjugate by the lattice automorphism that translates by k·e_μ and swaps coordinates μ and 4. It preserves the product Haar measure and the Wilson action, so it preserves μ, and it carries ϑ_{4,0} and its halves to ϑ_{μ,k} and its halves. ∎

**Lemma A.2 (blocks and reflections).** For every μ, k and s:
- **(a)** C_s lies in exactly one of H⁺ and H⁻.
- **(b)** ϑ(C_s) = C_{s′}, where s′ equals s except s′_μ = 2k − 1 − s_μ. Moreover ϑ∘τ_s = τ_{s′} on C_0, and hence ϑ(θ_s g) = θ_{s′} g.
- **(c)** s ↦ s′ is a bijection from the blocks in H⁺ to the blocks in H⁻, and it carries adjacent block pairs to adjacent block pairs.

*Proof.* Coordinatewise:
- If s_μ is even, ϑ(τ_s y)_μ = 2k − s_μ − y_μ. Here s′_μ is odd, so τ_{s′} gives s′_μ + 1 − y_μ = 2k − s_μ − y_μ.
- If s_μ is odd, ϑ(τ_s y)_μ = 2k − s_μ − 1 + y_μ. Here s′_μ is even, so τ_{s′} gives s′_μ + y_μ = 2k − s_μ − 1 + y_μ.

The other coordinates are untouched. Then ϑ(θ_s g)(U) = g(τ_s ϑU) = g(τ_{s′}U). A block occupies [s_μ, s_μ + 1] in direction μ, and the halves are the arcs [k, k + L/2] and [k + L/2, k + L], so each block lies in exactly one of them. The checker verifies (a) and (b) exhaustively for all μ, k and s on L = 4 and L = 6 (rows 04 and 05). ∎

**Theorem A (chessboard estimate).** For bounded measurable functions f_t ≥ 0 of the links of C_0, one for each t ∈ Λ,

$$\mathbb E\Big[\prod_{t\in\Lambda}\theta_t f_t\Big]\le\prod_{t\in\Lambda}\|f_t\|,\qquad \|f\|:=\mathbb E\Big[\prod_{t\in\Lambda}\theta_t f\Big]^{1/L^4}.$$

In particular, for events A_1,…,A_n on C_0 and distinct blocks t_1,…,t_n, μ(⋂_j θ_{t_j}A_j) ≤ ∏_j ‖1_{A_j}‖, because ‖1‖ = 1.

*Proof.*

**Step 0 (positive norms).** Apply the claim to f_t + δ with δ > 0. The left side can only grow. As δ ↓ 0, ‖f_t + δ‖ → ‖f_t‖, since ‖f + δ‖^{L⁴} is a polynomial in δ whose constant term is ‖f‖^{L⁴}. So we may assume f_t ≥ δ > 0, and then ‖f_t‖ ≥ δ.

**Step 1 (the extremal problem).** For a labelling a: Λ → Λ, let

$$\Phi(a)=\frac{\mathbb E[\prod_s\theta_s f_{a(s)}]}{\prod_s\|f_{a(s)}\|}>0.$$

There are finitely many labellings; let M be the largest value of Φ. A constant labelling a ≡ c has Φ = 1 by the definition of ‖f_c‖. The claim is Φ(identity) ≤ 1, so it suffices to show M = 1.

**Step 2 (reflection doubling).** Fix (μ, k), let Λ^± be the blocks in H^±, and write s′ for the mirror block from Lemma A.2. Define:
- a⁺ = a on Λ⁺, and a⁺(s) = a(s′) on Λ⁻;
- a⁻ = a on Λ⁻, and a⁻(s) = a(s′) on Λ⁺.

Put F = ∏_{s∈Λ⁺} θ_s f_{a(s)}, a function on H⁺. Lemma A.2(b) gives ∏_{s∈Λ⁻} θ_s f_{a(s)} = ϑG with G = ∏_{r∈Λ⁺} θ_r f_{a(r′)}, also a function on H⁺. Lemma A.1 gives E[F·ϑG]² ≤ E[F·ϑF]·E[G·ϑG]. Here F·ϑF is the product for a⁺ and G·ϑG is the product for a⁻. The normalizations multiply the same way, so

$$\Phi(a)^2\le\Phi(a^+)\,\Phi(a^-).$$

Hence, if Φ(a) = M, both a⁺ and a⁻ are maximizers too.

**Step 3 (agreement).** Let E(a) count the 4L⁴ nearest-neighbour block pairs {s, s + e_ν} with equal labels. Among the maximizers, choose one, a, with E(a) largest. Suppose a is not constant. Then some pair {s, s + e_μ} disagrees; take k = s_μ + 1, so the pair straddles the plane x_μ = k. Sort all pairs into three kinds:
- pairs inside Λ⁺ (E₊ of them agree);
- pairs inside Λ⁻ (E₋ of them agree);
- the 2L³ straddling pairs across x_μ = k and x_μ = k + L/2.

Each straddling pair is a mirror pair {r, r′}, so it agrees in both a⁺ and a⁻. Pairs inside Λ⁻ are mirror images of pairs inside Λ⁺. Hence

$$E(a^\pm)=2E_\pm(a)+2L^3,\qquad E(a^+)+E(a^-)=2(E_+ + E_-)+4L^3\ge 2E(a)+2,$$

since at least one straddling pair disagrees in a. So one of a^±, which is a maximizer by Step 2, has more agreement than a. That contradicts the choice of a. Therefore a is constant, and M = Φ(a) = 1. ∎

The checker tests the identities of Step 3, the count of 2L³ straddling pairs and the final inequality on 12 sampled three-label configurations of L = 4. That covers all 4 directions and all 4 planes, 192 cases with a disagreeing straddle in all (row 09).

## 3. VOL12-B: closed-cube geometry and energy–entropy

**Lemma B.1 (fourfold incidence).** The 24 two-faces F of C_0 are the six orientations (μ, ν) times four choices (a_ρ, a_σ) ∈ {0,1}² of the two transverse coordinates. Each orbit O_F = {τ_t F : t ∈ Λ} consists of the (μ, ν)-plaquettes whose transverse coordinates are ≡ (a_ρ, a_σ) mod 2, so |O_F| = L⁴/4. Every plaquette of O_F equals τ_t F for exactly four t. The 24 orbits are disjoint and cover all 6L⁴ plaquettes. Equivalently, every plaquette is a face of exactly **four closed unit cubes**.

*Proof.* τ_t preserves the parity of each transverse coordinate. A plaquette with base point (x_μ, x_ν) is reached exactly when t_μ = x_μ and t_ν = x_ν. In each transverse direction exactly two values of t_ρ work, one even and one odd. Rows 01–03 verify all of this on L = 4 and 6, with the four-cube incidence recounted independently from each block's 16 sites. ∎

**Lemma B.2 (partition function; VOL09).** For β ≥ 1 and L ≥ 2, Z° ≥ A_β^{−4L⁴}.

*Proof.* Let r = (4√β)⁻¹ ≤ 1/4. Normalized Haar measure in the geodesic angle is (2/π)sin²θ dθ, and sin θ ≥ θ/2 on [0, 1/4], so the cap of radius r has mass at least r³/(6π) ≥ r³/24 = (1536 β^{3/2})⁻¹. If every link lies in that cap, every plaquette angle is at most 4r, because the metric is bi-invariant. Then a_p ≤ (4r)²/2 = 1/(2β), so Σ_p a_p ≤ N_P/(2β). Therefore Z° ≥ (1536β^{3/2})^{−N_E} e^{−N_P/2} = (1536β^{3/2})^{−4L⁴} e^{−3L⁴} = A_β^{−4L⁴}. ∎

**Proposition B.3 (norm of a multi-face defect event).** For a set Φ of faces of C_0, let f_Φ = ∏_{F∈Φ} D_F. Then ‖f_Φ‖ ≤ A_β⁴ e^{−βε|Φ|/16}.

*Proof.* Lemma 3.1 of Lemma 0004 gives θ_t D_F = D_{τ_t F}, since W is invariant under inversion and conjugation in SU(2). So ∏_t θ_t f_Φ is the indicator that every plaquette in ⋃_{F∈Φ} O_F is defective. By Lemma B.1 that set has |Φ|L⁴/4 plaquettes, each with a_p > ε/4, so on this event Σ_p a_p > (ε/4)·(|Φ|L⁴/4) = ε|Φ|L⁴/16. Hence

$$\|f_\Phi\|^{L^4}\le (Z^\circ)^{-1}e^{-\beta\varepsilon|\Phi|L^4/16}\le A_\beta^{4L^4}e^{-\beta\varepsilon|\Phi|L^4/16}.$$

Take the L⁴-th root. ∎

## 4. VOL12-C: arbitrary sets

**Theorem C.1 (plaquettes).** For every finite set P of plaquettes, μ(D_p = 1 ∀p ∈ P) ≤ ρ_D^{|P|}.

*Proof.* Assign each p ∈ P to one block t(p) whose faces contain it; at least one exists by Lemma B.1. For each block t used, let Φ_t be the faces F with τ_t F assigned to t. Then 1{D ≡ 1 on P} = ∏_{t used} θ_t f_{Φ_t}. Theorem A and Proposition B.3 give a bound of ∏_t A_β⁴ e^{−βε|Φ_t|/16} = A_β^{4n} e^{−βε|P|/16}, where n ≤ |P| is the number of blocks used. Since A_β ≥ 1, this is at most ρ_D^{|P|}. ∎

**Theorem C.2 (bad stars).** For every finite set S of links, μ(B_e = 1 ∀e ∈ S) ≤ min{1, ρ⋆^{|S|}}.

*Proof.* If ρ_D > 1, then ρ⋆ > 6 and there is nothing to prove. Otherwise use VOL10 (5a): every bad e has a defective plaquette φ(e) ∋ e. Take a union bound over the at most 6^{|S|} such maps φ. Each plaquette contains 4 links, so φ is at most 4-to-1 and |φ(S)| ≥ |S|/4. Theorem C.1 then gives 6^{|S|} ρ_D^{|S|/4} = ρ⋆^{|S|}. ∎

## 5. VOL12-D: connected bad islands

The link graph joins two links when they share a plaquette. It is 18-regular for L ≥ 3 (row 03). C(o) is the connected component of o among bad links, and is empty if o is good.

**Lemma D.1 (rooted connected sets).** The number N_m of connected m-sets of links containing o satisfies N_m ≤ 72^{m−1} ≤ 18^{2(m−1)}.

*Proof.* Take a spanning tree of the set and a depth-first tour from o, of length 2(m − 1). The up/down pattern of the tour is a Dyck word, and there are C_{m−1} ≤ 4^{m−1} of those. Each up-step picks one of at most 18 neighbours, and each down-step is forced. The tour determines the set, so N_m ≤ 4^{m−1}·18^{m−1} = 72^{m−1}. VOL10's count 18^{2(m−1)} is the weaker form. ∎

Exact values on L = 6 are N₁ = 1, N₂ = 18, N₃ = 375 and N₄ = 8364 (row 07). **Negative control:** a count of 18^{m−1} would be too strong, since N₃ = 375 > 324 (row 08).

**Theorem D.2.** μ(|C(o)| ≥ m) ≤ min{1, N_m ρ⋆^m} ≤ min{1, 72^{m−1}ρ⋆^m}. If ρ⋆ ≤ 18⁻³, then μ(|C(o)| ≥ m) ≤ 18^{2m−2}·18^{−3m} = 18^{−m−2} for all m ≥ 1. If 72ρ⋆ < 1, then E|C(o)| ≤ ρ⋆/(1 − 72ρ⋆). All bounds are uniform in even L ≥ 4.

*Proof.* If |C(o)| ≥ m, then C(o) contains a connected m-set A ∋ o with A ⊆ 𝓑. Take the union bound over A, and use Theorem C.2 and Lemma D.1. ∎

## 6. VOL12-E: exact checks, fixtures and adversarial controls

The checker uses integers only and is no-float-gate clean. It is byte-identical under `python3 -I -B` and `python3 -O -I -B`. Its receipt SHA-256 is `ac95bc31…090d63b`.

| Row | What is checked | Result |
|---|---|---|
| 01–03 | Blocks, links, plaquettes, 24 orbits of size L⁴/4, disjoint and covering; four closed cubes per plaquette (recounted independently); 6 plaquettes per link, 4 links per plaquette, degree 18 | PASS on L = 4 and 6 |
| 04–05 | ϑ∘τ_s = τ_{s′} for every μ, k and s; each block in exactly one closed half | PASS on L = 4 and 6 |
| 06 | Odd side L = 5: t and t + L name the same block with opposite parity | 10,000 transport conflicts. **Rejected.** |
| 07–08 | N₁…N₄ = 1, 18, 375, 8364 under 72^{m−1} and 18^{2(m−1)}; 18^{m−1} falsified at m = 3 | PASS / falsifier fires |
| 09 | The agreement identities and inequality of Step 3 | 192 straddling cases, PASS |
| 10 | β = 9⁴, ε = 1/16 | ρ⋆ > 1 certified: **no information** |
| 11 | β = 9⁵, ε = 1/16 | ρ⋆ ≤ 18⁻³ certified, **and** ρ⋆ > 18⁻⁵⁷ certified. The VOL12 criterion passes where VOL10's fails. |
| 12 | β = 9⁶, ε = 1/16 | ρ⋆ ≤ 18⁻⁵⁷, with witness 6·1536·3¹⁹·18⁵⁷ < 2⁵¹⁸; ρ⋆ < 2⁻⁴⁷⁴; ρ_D < 2⁻¹⁹¹³ |
| 13 | β = 9⁵, ε = 1/2 | ρ⋆ ≤ 18⁻⁵⁷; ρ⋆ < 2⁻⁴²² |
| 14 | ε = 0 | ρ⋆ ≥ 6·1536: **no information** |

**How the certificates work.**
- Upper bounds use e^{3/4} < 3, β^{3/2} = 3^{3k} for β = 9^k, and e^{−x} ≤ 2^{−⌊x⌋}.
- Lower bounds use e^{3/4} ≥ 1 and e^{−x} ≥ 3^{−⌈x⌉}.

**Prediction against receipt.** All 14 rows are consistent with the prediction frozen before the checker existed. Rows 10 and 11 certify a stronger, two-sided statement than the one predicted.

**Approximate thresholds.** These are floating point and for orientation only; certified values exist only at the fixtures.

| ε | ρ⋆ < 1 for β > | ρ⋆ ≤ 18⁻³ for β > | ρ⋆ ≤ 18⁻⁵⁷ for β > |
|---|---|---|---|
| 1/16 | 25,714 | 35,069 | 197,551 |
| 1/4 | 5,861 | 8,210 | 48,851 |
| 1/2 | 2,788 | 3,965 | 24,291 |

## 7. Attribution

Chessboard estimates and their use in Peierls arguments are classical:
- J. Fröhlich and E. H. Lieb, *Commun. Math. Phys.* 60 (1978) 233–267.
- J. Fröhlich, R. Israel, E. H. Lieb and B. Simon, *Commun. Math. Phys.* 62 (1978) 1–34, and part II, *J. Stat. Phys.* 22 (1980) 297–347.
- Expositions: M. Biskup, *Reflection positivity and phase transitions in lattice spin models* (2009), §5.3, [arXiv:math-ph/0610025](https://arxiv.org/abs/math-ph/0610025); S. Friedli and Y. Velenik, *Statistical Mechanics of Lattice Systems*, Cambridge (2017), ch. 10.

Reflection positivity of lattice gauge theories goes back to K. Osterwalder and E. Seiler, *Ann. Phys.* 110 (1978) 440–471. Chessboard estimates are in current use for lattice gauge models, for example L. Goller and M. Porta, *J. Stat. Phys.* 193:60 (2026), for Z₂ gauge theory with fermions.

The proof of Theorem A follows the standard extremal-labelling argument. VOL12 claims no new method. Its contribution is an explicit-constant version for the 4D SU(2) Wilson measure, wired into the VOL08–VOL11 chain and checked in exact arithmetic.

## 8. Scope and open obligations

- **Odd L: OPEN.** Block transport by reflections is inconsistent when L is odd (row 06).
- **Single scale only.** The bound concerns lattice-scale plaquettes at very large β (fixtures β = 9⁵ to 9⁸). A physical-size block spans about e^{cβ} lattice spacings. Reflection positivity is generally not preserved by gauge-covariant block-spin maps, so this tool does not simply iterate under blocking. Uniform multiscale control and the uniform clustering rate (MG) remain **OPEN**.
- **External human review: OPEN (YM4-08).** The Theorem A proof (Lemmas A.1–A.2 and Steps 0–3) is the part a human should read first.
- **Atlas registration.** Nodes VOL12-A through VOL12-E are added to `certificates.json` in a follow-up commit after merge. Atlas sources pin immutable commit SHAs that exist on GitHub, so the merged commit must exist first. Dependencies: Lemma 0004, VOL08, VOL09 and VOL10.

## 9. Reproduce

```bash
python3 -I -B tests/ym4_su2_vol12_chessboard_clusters.py | cmp - docs/certificate-atlas/YM4-VOL12-CHESSBOARD-CLUSTERS-20261124.hbp
python3 -I -B scripts/no_float_gate.py .
```
