# 3. Theorem G0: step 0, from the Wilson measure to H_1 (route B)

**Status.** This is note section 3 of `docs/NOTE-YM4-04C-LOCAL-POLYMER-NORM-20261109.md`, written from main `830fd3f` against the draft prediction file (40 rows, scratch copy `ym4-04c/synth/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp`). It is route B. It argues through the Mayer expansion and the Penrose tree-graph identity, and it compares with the Kotecký–Preiss form only after the bound is proved (Remark 3.17). It uses the binding renames: the Kotecký–Preiss pair is (α, θ); a stays ½ Re Tr; b stays the blocking factor 2; κ stays the norm weight 1/4.

DERIVED: every lemma, proposition and corollary of sections 3.3 to 3.11, unless a clause is tagged otherwise. REPORTED: Finner's inequality, the exponential formula for connected graphs and for rooted trees, Lagrange inversion, Weyl's integration formula on SU(2), Machin's formula, the Bessel series of I_1, and the Kotecký–Preiss theorem used only for comparison. CONJECTURE: the refined head N(4..10) of row C03. MEASURED: the scratch checks of section 3.14 only. No step of the proof rests on them. OPEN: section 3.15.

**What this route finds.** Every constant and formula of G0 in the draft is proved, with one exception. The proof gives

```text
delta_1 = 6 alpha e^{-4(theta - kappa)},        T = E|chi_1/2| * 6 alpha e^{-8 theta} <= (8489/10000) * 6 alpha e^{-8 theta}.
```

The draft froze 12α e^{−4(θ−κ)} and (8489/10000)·12α e^{−8θ}. Those are true, since they follow from the bounds above. They are weaker by exactly a factor 2. The factor comes from one step: every cluster that holds a line link e_0 meets the test set W(e_0) in at least 2 off links, not 1 (Lemma 3.19). Section 3.13 lists the frozen rows whose predicted NOT_MET rests on the factor 12.

## 3.1 Setting and notation

- **Lattices.** Λ_0 = (ℤ/N)⁴ with N even and N ≥ 8. Λ_1 = (ℤ/(N/2))⁴, with coarse side N/2 ≥ 4. The HYPOTHESIS row has N = 2^K L_K with L_K ≥ 4 and K ≥ 1, so N ≥ 8 holds.
- **The line map.** (BU)_μ(x′) = U_μ(2x′) U_μ(2x′ + e_μ), as in [NOTE-YM4-03](NOTE-YM4-03-ONE-SCALE-BLOCKING.md) §2. The coarse link ℓ = (x′, μ) has midpoint m_ℓ = 2x′ + e_μ. Its line links are e_0(ℓ) = (2x′, μ) at position 0 and e_1(ℓ) = (m_ℓ, μ) at position 1. Every other fine link is an off link. A fine link (x, μ) is a line link exactly when x_ν is even for every ν ≠ μ.
- **The line gauge.** By NOTE-YM4-03 Theorem 4 and the gauge of [NOTE-YM4-03C](NOTE-YM4-03C-BLOCKED-ACTION.md) §2, ρ_1(V) = (1/Z) ∫ ∏_{off links} dU ∏_p w(U_p), with every line at (U at e_0, U at e_1) = (1, V_ℓ). Here Z = ∫ ∏_p w(U_p) dU is the fine partition function. E_V is product Haar expectation over the off links, with the lines fixed in this way.
- **The weight.** w(g) = e^{β_0 a(g)} with a(g) = ½ Re Tr g and β_0 ≥ 0. By NOTE-YM4-03 §5, e^{β a(g)} = c_0(β)[1 + K(g)] with

```text
K = sum_{n>=2} n t_n chi_{(n-1)/2},   t_n = I_n(beta)/I_1(beta),   c_0(beta) = 2 I_1(beta)/beta = sum_{m>=0} (beta/2)^{2m} / (m! (m+1)!).
```

  The last equality is the Bessel series of I_1 (REPORTED: Abramowitz and Stegun 1964, 9.6.10). χ_j is the spin-j character, so χ_{(n−1)/2} has dimension n. K is real and a class function. Its Haar mean is 0, and ∫ e^{x a(g)} dg = c_0(x).
- **Constants.** κ = 1/4. ε := ε_6(β_0) := (∫ K(g)⁶ dg)^{1/6}. F(n) := F_20(n) = C(20n, n)/(19n + 1). μ := 20²⁰/19¹⁹. e_χ := ∫ |χ_{1/2}(g)| dg.
- **The Kotecký–Preiss pair.** α ≥ 0 and θ ≥ κ. Throughout, x := ε e^{2α+θ}. The function names a(γ) = α #off(γ) and d(γ) = θ #γ of the rename appear only in Remark 3.17. Elsewhere the two expressions are written out.
- **Polymers.** A polymer γ is a nonempty set of fine plaquettes that is connected through off links: the graph on γ that joins two plaquettes sharing an off link is connected. #γ is its number of plaquettes. off(γ) is the set of off links of its plaquettes. Two polymers are compatible when they share no off link. γ ≁ γ′ means they are not, and γ ≁ γ always. The activity is z_γ(V) := E_V[∏_{p∈γ} K(U_p)]. γ is closed when every off link of γ lies in at least two plaquettes of γ. 𝒫 is the set of closed polymers. It is finite.
- **Clusters.** A cluster is a sequence X = (γ_1, …, γ_n) ∈ 𝒫ⁿ with n ≥ 1. |X| := Σ_i #γ_i. z^X := ∏_i z_{γ_i}. X ∋ e means e ∈ off(γ_i) for some i. Every sum over clusters carries the weight 1/n!. The incompatibility graph I(X) on {1, …, n} has the edge {i, j} when γ_i ≁ γ_j. The Ursell function is φ^T(X) := Σ_G (−1)^{#edges(G)}, over the connected spanning subgraphs G of I(X).
- **Counts.** For an off link e, N_e(n) := #{γ ∈ 𝒫 : #γ = n, e ∈ off(γ)}. A head is a vector N(4), …, N(10) of nonnegative numbers. The certificate series is

```text
S(x) = sum_{n=4}^{10} N(n) x^n + sum_{n=11}^{48} 6 F(n) x^n + 6 F(49) x^49 / (1 - mu x),     0 < mu x < 1.
```

- **The target.** H_1(κ, δ) is the class of the HYPOTHESIS row: log ρ_1 = const_1 + Σ_Y R_1(Y; V), with Y over sets of coarse links with #Y ≥ 4 that contain a closed loop, each R_1(Y; ·) real, coarse-gauge invariant and a function of V|_Y, and ‖R_1‖_κ := sup_ℓ Σ_{Y∋ℓ} e^{κ#Y} sup_V |R_1(Y; V)| ≤ δ.

## 3.2 The statement

**Theorem G0 (step 0).** Let N ≥ 8 be even and β_0 ≥ 0. Let the head satisfy N(n) ≥ N_e(n) for every off link e and every 4 ≤ n ≤ 10. The crude head N(n) = 6F(n) always does (Corollary 3.11). Let α ≥ 0 and θ ≥ κ, with x = ε e^{2α+θ}, μx < 1 and S(x) ≤ α. Then:

1. For every off link e, Σ_{X∋e} |φ^T(X)| sup_V |z^X(V)| e^{θ|X|} ≤ S(x) ≤ α. The cluster expansion of log ρ_1 converges absolutely at every V.
2. log ρ_1 = const_1 + Σ_Y R_1(Y; ·), with the index set and the three properties of the class H_1.
3. ‖R_1‖_κ ≤ 6α e^{−4(θ−κ)}. So H_1(κ, 6α e^{−4(θ−κ)}) holds. The draft's H_1(κ, 12α e^{−4(θ−κ)}) follows.
4. For every coarse plaquette P, the coefficient c_{1/2}(P) of χ_{1/2}(V_P) in log ρ_1 satisfies |c_{1/2}(P) − 2t_2(β_0)⁴| ≤ e_χ · 6α e^{−8θ} ≤ (8489/10000) · 6α e^{−8θ}.
5. No bound in items 1 to 4 depends on N, on K or on the number of plaquettes.

Over the certified pairs, the minimum of 6α e^{−4(θ−κ)} is attained at θ = κ and α = α_−(κ), the least root of S(ε e^{2α+κ}) = α. That root is at most 1/8 (Lemmas 3.21 and 3.22).

The draft defines δ_1 := min 12α e^{−4(θ−κ)} and T := (8489/10000)·12α e^{−8θ}. Theorem G0 gives δ_1 = min 6α e^{−4(θ−κ)} and T = (8489/10000)·6α e^{−8θ} over the same certified pairs.

## 3.3 The polymer gas

**Lemma 3.1 (polymer form).** *Hypotheses:* the setting of 3.1. *Claim:* Z ρ_1(V) = c_0(β_0)^{N_p} Ξ(V), with N_p the number of fine plaquettes and

```text
Xi(V) = sum over finite sets Gamma of pairwise compatible polymers of  prod_{gamma in Gamma} z_gamma(V)      (Gamma empty gives 1).
```

Each z_γ(V) is real, and Ξ(V) > 0.

*Proof.* ∏_p w(U_p) = c_0^{N_p} ∏_p (1 + K_p) = c_0^{N_p} Σ_S ∏_{p∈S} K_p, over all sets S of plaquettes. Split S into its components under the relation "share an off link". Every plaquette has an off link (Lemma 3.3(b)). So each component is a polymer, and distinct components are compatible. Conversely, the components of the union of a compatible set Γ are exactly the elements of Γ. Under E_V the off links are independent and the line links are fixed. So E_V ∏_{p∈S} K_p is the product of the z_γ over the components. K is real, so z_γ is real. Ξ(V) = Z ρ_1(V) c_0^{−N_p} > 0, since w > 0 makes ρ_1 > 0 (NOTE-YM4-03 Theorem 4, item 1). ∎

**Lemma 3.2 (Lemma B, polymer form).** *Hypotheses:* fine side N ≥ 3. *Claim:* if a polymer γ is not closed, then z_γ(V) = 0 for every V.

*Proof.* Let e be an off link of p ∈ γ that no other plaquette of γ holds. The four links of p are distinct (Lemma 3.3(a)). So U_p = A e^{±1} B, with A and B free of e. Integrate e first. By invariance of Haar measure, ∫ K(A e^{±1} B) de = ∫ K(g) dg = 0. No other factor holds e. ∎

This is rule (a) of NOTE-YM4-03C §6, Lemma B, in the polymer form that §6 there states. From here on, Ξ(V) is the sum over compatible sets of closed polymers.

## 3.4 Local geometry of the b = 2 lines

For a fine link (x, μ) let O(x, μ) := {ν ≠ μ : x_ν odd}. It is the same at both ends. The link is a line link when O = ∅. Otherwise its **class** is #O ∈ {1, 2, 3}. For a plaquette p with base x in the plane (μ, ν), let T(p) := {λ ∉ {μ, ν} : x_λ odd}. It is the same at all four corners.

**Lemma 3.3 (local geometry).** *Hypotheses:* N even, N ≥ 8. *Claims:*

- (a) Every link lies in exactly 6 plaquettes. The four links of a plaquette are distinct. Two distinct plaquettes share at most one link.
- (b) If T(p) = ∅, p is a **line plaquette**. Exactly one corner x_c(p) of p has both its μ- and ν-coordinates odd. p has 2 line links, which meet at its corner with μ- and ν-coordinates even, a coarse site. p has 2 off links, both of class 1, both ending at x_c(p). If #T(p) = 1, p is of **type A**: its 4 off links have classes 1, 1, 2, 2. If #T(p) = 2, p is of **type B**: its 4 off links have classes 2, 2, 3, 3. So every plaquette has 2 or 4 off links.
- (c) Let y be a site with exactly two odd coordinates, μ < ν. The 4 plaquettes of the plane (μ, ν) with corner y form the filling F_P of the coarse plaquette P with base (y − e_μ − e_ν)/2 in the plane (μ, ν). y =: x_P is its **center**. Every line plaquette lies in exactly one filling, the one centered at x_c(p). The off links of F_P are the 4 links at x_P in the directions ±μ, ±ν, its **internal links**. Each lies in exactly 2 plaquettes of F_P. The plaquette of F_P at a corner y′ of P, its **quadrant** at y′, holds the two line links of ∂P at y′. So the 8 line links of F_P are the two positions of each of the 4 coarse links of ∂P.
- (d) Every class-1 link is an internal link of exactly one filling. Class-2 and class-3 links lie in no filling. A class-1 link lies in exactly 6 plaquettes: the 2 quadrants of its filling that hold it, and 4 type-A plaquettes.
- (e) A type-A plaquette holds exactly 2 class-1 links. They are internal links of two different fillings.
- (f) A plaquette with 4 off links has exactly 20 off-link neighbours. One with 2 has exactly 10. So the maximal off-link degree is D = 20.
- (g) Let e_0 be a line link of the coarse link ℓ. The 6 plaquettes through e_0 are line plaquettes, one in each of the 6 fillings F_{P′} with ℓ ∈ ∂P′. Their off links form a set W(e_0) of exactly 12 links. Each of these 6 fillings holds exactly 2 links of W(e_0).
- (h) On Λ_1, two distinct coarse plaquettes share at most one coarse link. The 4 coarse links of a coarse plaquette are distinct. Every closed loop of coarse links has at least 4 links.

*Proof.* (a) The link (x, μ) lies in the plaquettes of the planes (μ, ν), ν ≠ μ, based at x and at x − e_ν: 3 × 2 = 6. For N ≥ 3 the four corners of a plaquette are distinct. Two links of a plaquette that meet at a corner span its plane and fix it. Two opposite links fix it too when N ≥ 3. So distinct plaquettes share at most one link.

(b) The corners of p are x + s e_μ + t e_ν, s, t ∈ {0, 1}. The μ-link at t has O = T(p) ∪ ({ν} if x_ν + t is odd). The ν-link at s has O = T(p) ∪ ({μ} if x_μ + s is odd). So each pair of parallel links has classes #T and #T + 1. If T(p) = ∅, the two class-0 links are the μ-link at even ν and the ν-link at even μ. They meet at the corner with μ and ν even. All other coordinates are even there, so it is a coarse site. The two class-1 links are the μ-link at odd ν and the ν-link at odd μ. Both contain the corner with μ and ν odd, which is unique.

(c) The 4 quadrants at y have T = ∅, since the coordinates of y outside {μ, ν} are even. Their corners are y, y ± e_μ, y ± e_ν and the coarse sites y ± e_μ ± e_ν = 2x′ + {0, 2}e_μ + {0, 2}e_ν with x′ = (y − e_μ − e_ν)/2. So they form the 2 × 2 filling of P. A line plaquette fixes its center x_c(p) by (b), and its plane is spanned by the two odd directions of x_c(p). So it lies in exactly one filling. By (b), the off links of each quadrant are its two links at x_P. These are the 4 links at x_P in ±μ, ±ν, each in the 2 quadrants beside it. The quadrant at the coarse corner y′ holds the two boundary links of the square at y′. They are line links of the two coarse links of ∂P at y′.

(d) Let (x, λ) have O = {ν}. Its endpoints have odd sets {ν} and {ν, λ}. The second endpoint y is a center with odd directions λ and ν. The link is the internal link of F centered at y in direction ±λ. The first endpoint has one odd coordinate and is no center. So the filling is unique. A class-2 link (x, λ) with O = {ν, ρ} has an endpoint with odd set {ν, ρ}, a center whose odd directions do not include λ, and an endpoint with three odd coordinates. Internal links run in the odd directions of their center, so this link is internal to no filling. A class-3 link has no endpoint with exactly two odd coordinates. The 6 plaquettes through the class-1 link (x, λ) lie in the planes (λ, ρ), ρ ≠ λ. For ρ = ν they have T = ∅, and they are the 2 quadrants of its filling that hold it. For ρ ∉ {λ, ν} they have T = {ν}, so they are of type A: 4 plaquettes.

(e) Let p′ be of type A with T(p′) = {ρ} in the plane (μ, ν). By (b), its class-1 links are a μ-link and a ν-link, each with O = {ρ}. By (d), the first is internal to a filling of the plane (μ, ρ) and the second to one of the plane (ν, ρ). These planes differ.

(f) Each off link of p lies in 5 plaquettes other than p, by (a). A plaquette other than p shares at most one link with p, by (a). So the neighbours through different off links are distinct: 4 × 5 = 20 or 2 × 5 = 10.

(g) The coordinates of e_0 outside its direction are even, so every plaquette through e_0 has T = ∅ and is a line plaquette. Its filling holds e_0 among its 8 line links, so that filling belongs to a coarse plaquette P′ with ℓ ∈ ∂P′, by (c). The 6 plaquettes through e_0 have 6 distinct centers. If e_0 = (y, μ), they are y + e_μ ± e_ρ, ρ ≠ μ, when e_0 starts at the coarse site y, and y ± e_ρ when it ends at one. So the 6 fillings are distinct, and they are the 6 coarse plaquettes through ℓ, which are distinct by (h). Each plaquette's 2 off links are internal links of its own filling, by (b) and (c). Distinct fillings have disjoint internal links, by (d). So #W(e_0) = 6 × 2 = 12, and each of the 6 fillings holds exactly 2 of them.

(h) The coarse side is N/2 ≥ 4. Two coarse plaquettes that share two coarse links coincide when the side is at least 3. The 4 coarse links of a coarse plaquette are distinct when the side is at least 2. A closed loop either lifts to a closed loop of ℤ⁴, of length at least 4, or winds, with length at least the side, 4. ∎

**Lemma 3.4 (item (a): #off(γ) ≤ 2#γ).** *Hypotheses:* γ ∈ 𝒫 and N ≥ 8. *Claim:* #off(γ) ≤ 2#γ.

*Proof.* Count the pairs (e, p) with e ∈ off(γ), p ∈ γ and e ∈ p. Closure gives at least 2 pairs per off link. Lemma 3.3(b) gives at most 4 per plaquette. So 2#off(γ) ≤ 4#γ. ∎

The bound is sharp. Take a unit cube in three directions with the fourth coordinate odd. Its 6 faces are of type A or B, and its 12 edges are off links, each in 2 faces. It is closed, with #off = 12 = 2 × 6.

**Lemma 3.5 (small closed polymers).** *Hypotheses:* N ≥ 8, γ ∈ 𝒫. *Claims:* (i) If γ holds a plaquette of type A or B, then #γ ≥ 5. (ii) If every plaquette of γ is a line plaquette, then γ is a filling. (iii) So #γ ≥ 4 for every closed polymer, and #γ = 4 exactly for the fillings.

*Proof.* (i) Such a plaquette p has 4 off links, by Lemma 3.3(b). Closure puts each of them in a second plaquette of γ. These are distinct, since a plaquette other than p shares at most one link with p. So #γ ≥ 1 + 4.

(ii) Let p ∈ γ have center y. Let p″ ∈ γ be a line plaquette sharing an off link L with p. L is internal to exactly one filling, by Lemma 3.3(d). Since L is an off link of p, that filling is the one centered at y. Since L is an off link of p″, it is also the one centered at x_c(p″). So x_c(p″) = y, and p″ lies in the filling centered at y. By connectivity, γ lies in that filling. In a filling, quadrant i holds internal links i and i + 1 (mod 4). A nonempty proper set of quadrants holds some internal link once. It is not closed. So γ is the whole filling.

(iii) follows from (i) and (ii). ∎

So the Lemma-B-closed off-link-connected sets of at most 4 plaquettes are exactly the coarse fillings, and none has 3 or fewer. This is the claim of row C01.

**Lemma 3.6 (how z_γ depends on V).** *Hypotheses:* N ≥ 8, γ ∈ 𝒫. Let Y″(γ) be the set of coarse links ℓ such that γ holds both e_0(ℓ) and e_1(ℓ), that is, some plaquette of γ contains each. *Claims:*

- (i) z_γ(V) = z_γ(V′) whenever V and V′ agree on Y″(γ).
- (ii) z_γ(V^h) = z_γ(V) for every coarse gauge transformation h.
- (iii) If Y″(γ) contains no closed loop, z_γ is constant.
- (iv) #Y″(γ) is at most the number of line plaquettes of γ. So #Y″(γ) ≤ #γ.

*Proof.* (i) z_γ is an integral over the off links of a product of class functions of plaquettes, with the lines at (1, V). Lemma A of NOTE-YM4-03C §2 applies. If no plaquette of γ holds e_0(ℓ), then z_γ is constant in V_ℓ. If none holds e_1(ℓ), then z_γ holds V_ℓ nowhere. Change V into V′ one coarse link outside Y″(γ) at a time. Each change leaves z_γ fixed.

(ii) Define g̃ on Λ_0. Set g̃(2x′) = h(x′) at coarse sites. Set g̃(m_ℓ) = h(x′) at the midpoint of ℓ = (x′, μ). Each site with exactly one odd coordinate is the midpoint of exactly one coarse link, so this is well defined. Set g̃ = 1 at all other sites. Under U ↦ g̃(x) U g̃(x + e)⁻¹, the link at e_0(ℓ) goes from 1 to h(x′) · 1 · h(x′)⁻¹ = 1. The link at e_1(ℓ) goes from V_ℓ to h(x′) V_ℓ h(x′ + μ)⁻¹ = (V^h)_ℓ. Each off link is multiplied on the left and on the right by fixed elements, which preserves its Haar measure. Each plaquette holonomy is conjugated, so each K(U_p) is unchanged ([LEMMA-0001](LEMMA-0001-GAUGE-INVARIANCE.md)). This change of variables gives z_γ(V^h) = z_γ(V). It is the argument of NOTE-YM4-03 Theorem 4, item 3, in the line gauge.

(iii) Let Y″(γ) be a forest. Pick a root in each tree with h = 1 there. Extend h along each tree so that h(x′) V_ℓ h(x′ + μ)⁻¹ = 1 on every edge ℓ = (x′, μ). Set h = 1 off the forest. Then V^h = 1 on Y″(γ). By (i) and (ii), z_γ(V) = z_γ(V^h) equals the value of z_γ at V = 1 on Y″(γ).

(iv) Each line plaquette holds 2 line links, and other plaquettes hold none (Lemma 3.3(b)). Each ℓ ∈ Y″(γ) takes 2 distinct held line links. So 2#Y″(γ) ≤ 2 × (number of line plaquettes of γ). ∎

## 3.5 Item (b): Finner's inequality with exponent 6

**Finner's inequality (REPORTED: Finner 1992, Ann. Probab. 20, 1893–1901).** Let (Ω_i, μ_i), i ∈ I, be finitely many probability spaces. For j in a finite set J, let S_j ⊆ I, let f_j ≥ 0 be a measurable function of (ω_i)_{i∈S_j}, and let p_j ∈ [1, ∞]. If Σ_{j : i∈S_j} 1/p_j = 1 for every i, then ∫ ∏_j f_j d(⊗_i μ_i) ≤ ∏_j ‖f_j‖_{L^{p_j}(⊗_{i∈S_j} μ_i)}.

If the sum is below 1 at some i, add the factor f = 1 on {i} with the missing exponent. Its norm is 1. So the inequality also holds with "≤ 1".

**Lemma 3.7.** *Hypotheses:* N ≥ 8, γ a polymer, any V. *Claims:* |z_γ(V)| ≤ ε^{#γ}, with

```text
eps^6 = integral K^6 = sum_{k=0}^{6} C(6,k) (-1)^{6-k} c_0(k beta_0) / c_0(beta_0)^k.
```

*Proof.* Take I = off(γ), with Haar measure on each link; the other off links integrate to 1. Take f_p = |K(U_p)| as a function of the off links of p, with the lines fixed at V, and p_p = 6. Each off link lies in at most 6 plaquettes of γ (Lemma 3.3(a)), so Σ 1/6 ≤ 1. Fix every off link of p but one, u. Then U_p = A u^{±1} B is Haar distributed. By Fubini, U_p is Haar distributed under ⊗_{off(p)} Haar. (This is the exclusive-link argument of [LEMMA-0002](LEMMA-0002-HAAR-MOMENTS.md).) So ‖f_p‖_6 = (∫ |K|⁶)^{1/6} = ε. Finner's inequality gives |z_γ(V)| ≤ E_V ∏_p |K(U_p)| ≤ ε^{#γ}. The formula for ε⁶ is the binomial expansion of (e^{β_0 a}/c_0 − 1)⁶ with ∫ e^{kβ_0 a} = c_0(kβ_0). ∎

## 3.6 Item (c): the BFS injection and the Fuss–Catalan tail

**Lemma 3.8 (BFS injection).** *Hypotheses:* 𝔾 a finite graph of maximal degree at most D, and v a vertex. *Claim:* the number of connected vertex sets of size n that contain v is at most the number of subtrees with n nodes that contain the root of 𝕋_D, the complete rooted tree in which every node has D child slots labelled 1, …, D.

*Proof.* At each vertex u, label its neighbours injectively by {1, …, D}, and let u_i be the neighbour with label i. For a connected set A ∋ v, run breadth-first search from v inside A. Keep a first-in first-out queue. When u leaves the queue, scan i = 1, …, D. If u_i exists, lies in A and is not yet reached, mark it reached, put it in the queue, and make it the child of u in slot i. A is connected, so every vertex of A is reached. The result is a subtree τ(A) of 𝕋_D with #A nodes, with a map from its nodes onto A. τ(A) alone recovers the map: the root goes to v, and the child in slot i of a node that goes to u goes to u_i. So A, the image, is determined by τ(A). The map A ↦ τ(A) is injective. ∎

**Lemma 3.9 (Fuss–Catalan count).** *Claim:* the number of subtrees of 𝕋_D with n ≥ 1 nodes that contain the root is F_D(n) = C(Dn, n)/((D − 1)n + 1).

*Proof.* Let A(z) = Σ_{n≥0} F_D(n) zⁿ with F_D(0) = 1 for the empty tree. A subtree that contains the root is the root together with, in each of its D slots, an empty or a nonempty subtree. So A = 1 + z A^D. Write A = 1 + u, so u = z(1 + u)^D. Lagrange inversion (REPORTED: Stanley 1999, Enumerative Combinatorics vol. 2, Cambridge University Press, §5.4) gives [zⁿ]u = (1/n)[u^{n−1}](1 + u)^{Dn} = (1/n) C(Dn, n − 1) = C(Dn, n)/((D − 1)n + 1). ∎ So F_20(1), …, F_20(4) = 1, 20, 590, 20540. The same numbers count Raney's sequences (REPORTED: Raney 1960, Trans. Amer. Math. Soc. 94, 441–451).

**Lemma 3.10 (the ratios, for every n).** *Claim:* for every integer n ≥ 0,

```text
F(n+1)/F(n) = 20 * prod_{j=1}^{19} (20n + j) / (19n + j + 1).
```

Each factor is strictly increasing in n and strictly below 20/19. So F(n+1)/F(n) is strictly increasing, strictly below μ = 20²⁰/19¹⁹ for every n, and tends to μ as n → ∞.

*Proof.* F(n) = (20n)!/(n! (19n + 1)!). So

```text
F(n+1)/F(n) = [prod_{j=1}^{20} (20n+j)] / [(n+1) prod_{j=2}^{20} (19n+j)],
```

and 20n + 20 = 20(n + 1) gives the product formula. For f_j(n) = (20n + j)/(19n + j + 1), the determinant 20(j + 1) − 19j = j + 20 is positive, so f_j is strictly increasing. Also 20/19 − f_j(n) = (j + 20)/(19(19n + j + 1)) > 0, and it tends to 0. ∎

This holds for all n. Row C01 checks it for n ≤ 59 only. μ lies in [53.00068, 53.00069] (exact rational comparison, section 3.14, block A).

**Corollary 3.11 (the series S bounds the per-link sum).** *Hypotheses:* N ≥ 8, 0 < μx < 1, and a head with N(n) ≥ N_e(n) for 4 ≤ n ≤ 10. *Claims:* for every off link e, N_e(n) = 0 for n ≤ 3, N_e(n) ≤ 6F(n) for every n, and Σ_{n≥1} N_e(n) xⁿ ≤ S(x). The crude head N(n) = 6F(n) satisfies the hypothesis.

*Proof.* N_e(n) = 0 for n ≤ 3 by Lemma 3.5. A polymer γ with e ∈ off(γ) contains one of the 6 plaquettes through e (Lemma 3.3(a)). It is a connected vertex set of the off-link graph of plaquettes, of maximal degree 20 (Lemma 3.3(f)). Lemmas 3.8 and 3.9, with each of the 6 roots, give N_e(n) ≤ 6F(n). This bounds all off-link-connected sets through e, closed or not. Lemma 3.10 gives F(n) ≤ μ^{n−49} F(49) for n ≥ 49. So Σ_{n≥49} 6F(n) xⁿ ≤ 6F(49) x⁴⁹ Σ_{k≥0} (μx)^k = 6F(49) x⁴⁹/(1 − μx). ∎

*Remark.* At μx = 1 exactly, the Fuss–Catalan tail itself converges, since F(n) μ^{−n} decays like n^{−3/2} (REPORTED: Stirling's formula). Only its geometric bound diverges there. This touches the wording of row C04 ("diverges whenever μ e^{1/4} ε_6 ≥ 1") at equality only. It does not touch G0.

## 3.7 Item (d): the Mayer expansion and the tree-graph bound

Write ω(γ) := sup_V |z_γ(V)| e^{θ#γ} for γ ∈ 𝒫.

**Lemma 3.12 (Mayer expansion; REPORTED).** *Claim:* for variables (ζ_γ)_{γ∈𝒫}, let Ξ(ζ) = Σ_Γ ∏_{γ∈Γ} ζ_γ over the compatible subsets Γ ⊆ 𝒫. Then, as formal power series,

```text
log Xi(zeta) = sum_{n>=1} (1/n!) sum_{X in P^n} phi^T(X) prod_i zeta_{gamma_i}.
```

*Justification.* Ξ(ζ) = Σ_n (1/n!) Σ_{X∈𝒫ⁿ} ∏_i ζ_{γ_i} ∏_{i<j} (1 + f_ij), with f_ij = −1 when γ_i ≁ γ_j and 0 otherwise. Since γ ≁ γ, repeated polymers give 0, and each compatible set is counted once. Expand ∏(1 + f_ij) = Σ_G ∏_{ij∈G} f_ij over all graphs G on {1, …, n}. The exponential formula for graphs split into connected components gives the logarithm as the sum over connected G (REPORTED: Mayer and Mayer 1940, Statistical Mechanics, Wiley; Stanley 1999, §5.1; Brydges 1986, Les Houches 1984 lectures, North-Holland, 129–183). For G ⊆ I(X), ∏_{ij∈G} f_ij = (−1)^{#edges(G)}, and it is 0 otherwise.

**Lemma 3.13 (Penrose partition; DERIVED here, following Penrose 1967).** *Hypotheses:* H a connected graph on {1, …, n}. For a spanning tree τ ⊆ H, let d_τ(i) be the tree distance from 1 and p_τ(j) the parent of j ≠ 1. Let

```text
R(tau) = tau  union  { {i,j} in H : d_tau(i) = d_tau(j) }  union  { {i,j} in H : d_tau(j) = d_tau(i) + 1 and i > p_tau(j) }.
```

*Claim:* Σ_{G ⊆ H connected spanning} (−1)^{#edges(G)} = (−1)^{n−1} #{τ : R(τ) = τ}. So |φ^T(X)| ≤ #{spanning trees of I(X)} = Σ_{τ∈𝒯_n} ∏_{{i,j}∈τ} 1[γ_i ≁ γ_j], with 𝒯_n the trees on {1, …, n}.

*Proof.* For a connected spanning G ⊆ H, let d_G be graph distance from 1. Let T(G) join each j ≠ 1 to the least i with {i, j} ∈ G and d_G(i) = d_G(j) − 1. T(G) is a spanning tree of G with d_{T(G)} = d_G. Fix a spanning tree τ ⊆ H. If T(G) = τ, then τ ⊆ G. Every edge of G joins levels of d_G = d_τ that differ by at most 1. An edge between consecutive levels other than a tree edge has i > p_τ(j), by the choice of the least i. So G ⊆ R(τ). Conversely, let τ ⊆ G ⊆ R(τ). Then d_G ≤ d_τ, since G ⊇ τ. Every edge of R(τ) changes d_τ by at most 1, so d_τ ≤ d_G along any path from 1. So d_G = d_τ. The neighbours of j at level d_τ(j) − 1 are p_τ(j) and vertices i > p_τ(j). So T(G) = τ. The connected spanning subgraphs of H are therefore the disjoint union, over spanning trees τ, of the Boolean intervals {G : τ ⊆ G ⊆ R(τ)}. On one interval the sum is (−1)^{n−1} Σ_{A ⊆ R(τ)∖τ} (−1)^{#A}, which is (−1)^{n−1} when R(τ) = τ and 0 otherwise. If I(X) is disconnected, φ^T(X) = 0 and there is no spanning tree. ∎

**Lemma 3.14 (the rooted-tree recursion).** *Hypotheses:* γ ∈ 𝒫 and h ≥ 0. Let

```text
M_h(gamma) = sum_{n>=1} (1/(n-1)!) sum_{tau in T_n, depth from 1 <= h} sum_{(gamma_2..gamma_n) in P^{n-1}} prod_{{i,j} in tau} 1[gamma_i ~/~ gamma_j] prod_{i=2}^{n} omega(gamma_i),    gamma_1 := gamma.
```

*Claim:* M_0(γ) = 1 and M_{h+1}(γ) = exp(Σ_{γ′≁γ} ω(γ′) M_h(γ′)), as sums of nonnegative terms with values in [0, ∞].

*Proof.* A tree on {1, …, n} rooted at 1 with depth at most h + 1 is the same as three data: the set C of children of 1, with k = #C; a partition of {2, …, n} into k blocks, each holding one element of C; and in each block a tree rooted at that element, of depth at most h. The weight factorizes over the blocks. The edge from 1 to a child c gives the factor 1[γ ≁ γ_c]. Relabel each block onto {1, …, m_j} with its root as 1. The number of ways to form blocks of sizes m_1, …, m_k with a root in each is (n − 1)!/(k! ∏_j (m_j − 1)!). Dividing by (n − 1)! leaves (1/k!) ∏_j 1/(m_j − 1)!. Summing over n and the m_j gives Σ_k (1/k!) (Σ_{γ′≁γ} ω(γ′) M_h(γ′))^k. This is the exponential formula for rooted labelled trees, R = x e^R (REPORTED: Stanley 1999, §5.3). ∎

**Proposition 3.15 (the per-off-link cluster bound).** *Hypotheses:* N ≥ 8, θ ≥ 0, α ≥ 0, and for every off link e

```text
(KP_e)     sum_{gamma in P : e in off(gamma)} omega(gamma) e^{alpha #off(gamma)} <= alpha.
```

*Claim:* for every off link e,

```text
sum_{n>=1} (1/n!) sum_{X in P^n, X contains e} |phi^T(X)| prod_i omega(gamma_i)  <=  sum_{gamma contains e} omega(gamma) e^{alpha #off(gamma)}  <=  alpha.
```

*Proof.* Step 1. Let M(γ) := sup_h M_h(γ). Every tree has finite depth, so M(γ) is the sum over all trees. Induction on h gives M_h(γ) ≤ e^{α#off(γ)}. It holds at h = 0. If it holds at h, then

```text
sum_{gamma' ~/~ gamma} omega(gamma') M_h(gamma') <= sum_{e' in off(gamma)} sum_{gamma' contains e'} omega(gamma') e^{alpha #off(gamma')} <= alpha #off(gamma),
```

by the union bound over the off links that γ′ shares with γ and by (KP_e). Lemma 3.14 then gives M_{h+1}(γ) ≤ e^{α#off(γ)}.

Step 2. φ^T and ∏ω are symmetric under permutations of X. A cluster X ∋ e has some γ_i ∋ e. The union bound over i and symmetry give

```text
sum_{X in P^n, X contains e} (...) <= n * sum_{X in P^n, gamma_1 contains e} (...).
```

So the left side of the claim is at most Σ_n (1/(n − 1)!) Σ_{γ_1∋e} ω(γ_1) Σ_{γ_2..γ_n} |φ^T(X)| ∏_{i≥2} ω(γ_i). Lemma 3.13 bounds |φ^T| by the sum over trees, and the result is Σ_{γ_1∋e} ω(γ_1) M(γ_1). Step 1 and (KP_e) finish the proof. ∎

**Corollary (the certificate gives (KP_e)).** Under the hypotheses of Theorem G0, (KP_e) holds for every off link e, with the left side at most S(x). *Proof.* By Lemmas 3.4 and 3.7, ω(γ) e^{α#off(γ)} ≤ ε^{#γ} e^{θ#γ} e^{2α#γ} = x^{#γ}. Sum over γ ∋ e and use Corollary 3.11: the sum is at most Σ_n N_e(n) xⁿ ≤ S(x) ≤ α. ∎

**Lemma 3.16 (the series is log ρ_1).** *Hypotheses:* those of Theorem G0. *Claim:* for every V,

```text
log rho_1(V) = log(c_0^{N_p}/Z) + sum_{n>=1} (1/n!) sum_{X in P^n} phi^T(X) z^X(V),
```

and the series converges absolutely.

*Proof.* Every polymer holds an off link. Summing Proposition 3.15 over the finitely many off links of Λ_0 bounds Σ_X |φ^T(X)| ∏_i sup|z_{γ_i}| by a finite number. That number enters no estimate below. So the series L(ζ) of Lemma 3.12 converges absolutely on the closed polydisc |ζ_γ| ≤ sup_V |z_γ|. There exp(L(ζ)) is absolutely convergent too, since it is dominated by exp of the series with absolute values. A formal identity between two absolutely convergent power series holds as an identity of values, so exp L(ζ) = Ξ(ζ) on the polydisc. At ζ = z(V), L is real (Lemma 3.1) and exp L = Ξ(V) > 0. So L(z(V)) = log Ξ(V). Lemma 3.1 converts log Ξ into log ρ_1. ∎

**Remark 3.17 (comparison with the Kotecký–Preiss form).** *The theorem (REPORTED: Kotecký and Preiss 1986, Commun. Math. Phys. 103, 491–498).* For a polymer model with a symmetric, reflexive incompatibility relation, suppose there are functions a, d ≥ 0 on polymers with Σ_{γ′≁γ} |z_{γ′}| e^{a(γ′)+d(γ′)} ≤ a(γ) for every γ. Then the cluster expansion converges absolutely, and Σ_{X≁γ} |φ^T(X)| |z^X| e^{d(X)} ≤ a(γ) for every γ, with d(X) = Σ_i d(γ_i).

Take a(γ) = α #off(γ), d(γ) = θ #γ, and |z_γ| replaced by sup_V |z_γ|. Then:

- (KP_e) for every e implies the Kotecký–Preiss hypothesis, by the union bound over e ∈ off(γ). Its conclusion is Σ_{X≁γ} ≤ α #off(γ).
- The per-off-link form of Proposition 3.15 follows from Kotecký–Preiss as well. Adjoin, for each off link e, a test polymer {e} with activity 0, a({e}) = α and d({e}) = 0, incompatible exactly with the polymers that hold e. The hypothesis at {e} is (KP_e). Clusters that contain {e} vanish. The conclusion at {e} is Σ_{X∋e} ≤ α.

So the two routes prove the same inequality, with the same constant α. Route B also gives the identity with log ρ_1 (Lemma 3.16) and the sign rule (−1)^{n−1} of Lemma 3.13. A weaker hypothesis, a sum over pairwise compatible sets, is available (REPORTED: Fernández and Procacci 2007, Commun. Math. Phys. 274, 123–140; Battle and Federbush 1984, Lett. Math. Phys. 8, 55–57, for tree-graph bounds). It is not used. Neither route produces the factor 2 of section 3.9. That factor comes from the test-set step, after the cluster bound.

## 3.8 Item (e): assembling R_1

For a cluster X, let Y(X) := ∪_i Y″(γ_i).

**Proposition 3.18.** *Hypotheses:* those of Theorem G0. For each set Y of coarse links that contains a closed loop, let

```text
R_1(Y; V) := sum_{n>=1} (1/n!) sum_{X in P^n : Y(X) = Y} phi^T(X) z^X(V),
const_1   := log(c_0^{N_p}/Z) + sum over clusters X with no closed loop in Y(X) of (1/n!) phi^T(X) z^X.
```

*Claims:*

- (i) log ρ_1 = const_1 + Σ_Y R_1(Y), the sum over the sets Y that contain a closed loop. const_1 does not depend on V.
- (ii) Each such Y has #Y ≥ 4.
- (iii) Each R_1(Y; ·) is real, coarse-gauge invariant, and a function of V|_Y.
- (iv) Every cluster X in R_1(Y) has |X| ≥ #Y(X) ≥ 4. A term z^X can depend on V only if some γ_i has a closed loop in Y″(γ_i), and then #γ_i ≥ #Y″(γ_i) ≥ 4.

*Proof.* Regroup the absolutely convergent series of Lemma 3.16. If Y(X) has no closed loop, each Y″(γ_i) ⊆ Y(X) is a forest. So each z_{γ_i} is constant (Lemma 3.6(iii)), and so is z^X. That gives (i). (ii) is Lemma 3.3(h). For (iii): z^X depends on V only through V|_{Y(X)} (Lemma 3.6(i)). It is real (Lemma 3.1) and gauge invariant (Lemma 3.6(ii)). An absolutely convergent sum keeps all three properties. (iv) follows from Lemma 3.6(iv) and (ii), with Lemma 3.5. ∎

At k = 1 the coarse Wilson term lies inside R_1(∂P), as the HYPOTHESIS row asks. It is the χ_{1/2} part of z_{F_P}, which is 2t_2⁴ χ_{1/2}(V_P) (Lemma 3.23).

## 3.9 Item (f): δ_1

**Lemma 3.19 (every holding cluster meets W(e_0) twice).** *Hypotheses:* N ≥ 8, ℓ a coarse link, and X a cluster with ℓ ∈ Y(X). *Claim:* X holds at least 2 links of W(e_0(ℓ)). So, for every nonnegative function Φ on clusters,

```text
sum_{X : l in Y(X)} Phi(X)  <=  (1/2) sum_{e in W(e_0(l))} sum_{X contains e} Phi(X).
```

*Proof.* ℓ ∈ Y″(γ_i) for some i. So γ_i holds a plaquette p through e_0(ℓ). By Lemma 3.3(g), p has exactly 2 off links, both in W(e_0(ℓ)), and both lie in off(γ_i). So 1[ℓ ∈ Y(X)] ≤ (1/2) Σ_{e∈W(e_0)} 1[X ∋ e]. Multiply by Φ(X) and sum. ∎

**Proposition 3.20 (the norm bound).** *Hypotheses:* those of Theorem G0. *Claim:* ‖R_1‖_κ ≤ 6α e^{−4(θ−κ)}.

*Proof.* Fix a coarse link ℓ. Then

```text
sum_{Y contains l} e^{kappa #Y} sup_V |R_1(Y;V)|  <=  sum_{X : l in Y(X)} (1/n!) |phi^T(X)| prod_i sup|z_{gamma_i}| e^{kappa #Y(X)}.
```

By Proposition 3.18(iv), #Y(X) ≤ |X| and |X| ≥ 4. With θ ≥ κ,

```text
e^{kappa #Y(X)} <= e^{kappa |X|} = e^{theta |X|} e^{-(theta - kappa)|X|} <= e^{theta |X|} e^{-4(theta - kappa)}.
```

Since prod_i sup|z_{γ_i}| e^{θ|X|} = ∏_i ω(γ_i), Lemma 3.19 and Proposition 3.15 give

```text
<= e^{-4(theta-kappa)} * (1/2) * sum_{e in W(e_0(l))} sum_{X contains e} (1/n!) |phi^T(X)| prod_i omega(gamma_i)  <=  e^{-4(theta-kappa)} * (1/2) * 12 * alpha.
```

Here #W(e_0) = 12 (Lemma 3.3(g)). ∎

Without Lemma 3.19, the union bound over the 12 links of W(e_0) gives 12α e^{−4(θ−κ)}, the draft's constant. It counts every cluster twice.

*The constant 6 is the least this method gives.* The method bounds Σ_{X∋e} by α for each test link e and covers the clusters through ℓ fractionally by test links. The 6 fillings F_{P′} with ℓ ∈ ∂P′ are clusters through ℓ. Their off-link sets, the internal links, are pairwise disjoint (Lemma 3.3(d)). So any weights on test links that give each of them total weight at least 1 have total weight at least 6. At leading order in β_0 the clusters through ℓ are exactly these 6 fillings. The union bound over W(e_0) counts each of them twice, since each holds 2 links of W(e_0) (Lemma 3.3(g)).

**Lemma 3.21 (θ = κ is the optimum and decides existence).** *Hypotheses:* a head with N(n) ≥ 0, ε > 0. For θ ≥ κ let g_θ(α) := S(ε e^{2α+θ}) − α on the domain {α ≥ 0 : με e^{2α+θ} < 1}, and let α_−(θ) := min{α : g_θ(α) ≤ 0} when that set is nonempty. *Claims:*

- (i) g_θ is convex in α, and g_θ(α) is nondecreasing in θ.
- (ii) If g_θ(α) ≤ 0 for some α, then g_κ(α) ≤ 0.
- (iii) α_−(θ) and α_−(θ) e^{−4θ} are nondecreasing in θ.
- (iv) So min over certified pairs of 6α e^{−4(θ−κ)} equals 6α_−(κ), and the draft's minimizing θ = 1/4 is right.

*Proof.* (i) S is a power series in x with nonnegative coefficients, the tail term included: 6F(49)x⁴⁹/(1 − μx) = Σ_k 6F(49) μ^k x^{49+k}. Each term ε^n e^{n(2α+θ)} is convex in α and nondecreasing in θ. (ii) follows from (i). (iii) The set {α : g_θ(α) ≤ 0} shrinks as θ grows. It is closed, and it stays away from the edge of the domain, since g_θ → ∞ there. So α_−(θ) exists when the set is nonempty, and it is nondecreasing. Every term of S has degree at least 4, so S(x) = x⁴ Q(x) with Q a series with nonnegative coefficients. At the root, α_− = S(x_−) with x_− = ε e^{2α_−+θ}. So α_− e^{−4θ} = ε⁴ e^{8α_−} Q(x_−). Both factors are nondecreasing in θ. (iv) follows. ∎

**Lemma 3.22 (the cap α ≤ 1/4 never binds).** *Hypotheses:* as in Lemma 3.21, with g_θ(α) ≤ 0 for some α ≥ 0. *Claim:* α_−(θ) ≤ 1/8.

*Proof.* S(x) > 0 for x > 0, since the tail has positive coefficients. So g_θ(0) > 0. g_θ is convex and tends to +∞ at the edge of the domain. If g_θ′(0) ≥ 0, then g_θ ≥ g_θ(0) > 0 everywhere, against the hypothesis. So g_θ has an interior minimum α* with g_θ′(α*) = 2x* S′(x*) − 1 = 0, where x* = ε e^{2α*+θ}, and g_θ(α*) ≤ 0. Every term of S has degree at least 4, so x S′(x) ≥ 4S(x). So S(x*) ≤ x* S′(x*)/4 = 1/8. The least root satisfies α_− ≤ α*. So α_− = S(x(α_−)) ≤ S(x*) ≤ 1/8. ∎

So the frozen condition S ≤ α ≤ 1/4 is MET exactly when S ≤ α is MET for some α ≥ 0. Its least root is the one the draft's bisection returns.

## 3.10 Item (f): the readout

**Lemma 3.23 (the filling's term).** *Hypotheses:* N ≥ 8, P a coarse plaquette. *Claim:* z_{F_P}(V) = Σ_{n≥2} n t_n⁴ χ_{(n−1)/2}(V_P). So ⟨χ_{1/2}(V_P), z_{F_P}⟩ = 2t_2⁴ in coarse Haar.

*Proof.* Label the quadrants Q_1, …, Q_4 in cyclic order around x_P, with the internal link L_i between Q_i and Q_{i+1}. Orient the quadrants alike, so that each L_i occurs as u in one word and u⁻¹ in the other. This is allowed since χ_j(g⁻¹) = χ_j(g). Expand each K(U_{Q_i}) in characters, writing χ_n for the character of dimension n. Integrate L_1, L_2, L_3 in turn with ∫ χ_n(A u) χ_{n′}(u⁻¹ B) du = δ_{nn′} χ_n(AB)/n. Each merge forces equal labels and divides by n. After three merges, L_4 occurs as u … u⁻¹, adjacent in the cyclic word, and drops out. The word left is the boundary of the 2 × 2 square. With the lines at (1, V) its holonomy is a conjugate of V_P (NOTE-YM4-03 Proposition 2). So z_{F_P} = Σ_n (n t_n)⁴ n^{−3} χ_n(V_P). This is the disk rule of NOTE-YM4-03 Theorem 8's proof and NOTE-YM4-03C §7.5. Under coarse Haar measure V_P is Haar distributed, since its 4 coarse links are distinct (Lemma 3.3(h)). The characters are orthonormal, and n = 2 gives 2t_2⁴. ∎

**Lemma 3.24 (the 8-plaquette gap, for polymers and for clusters).** *Hypotheses:* N ≥ 8, P a coarse plaquette. *Claims:*

- (i) A closed polymer γ that holds all 8 line links of ∂P is F_P, or has #γ ≥ 8.
- (ii) A cluster X ≠ (F_P) with Y(X) ⊇ ∂P has |X| ≥ 8.

*Proof of (i).* Let m := #(γ ∩ F_P). For P′ ≠ P let g(P′) := #(γ ∩ F_{P′}). A filling is **partial** when 1 ≤ #(γ ∩ F) ≤ 3. Let n_A be the number of type-A plaquettes in γ.

*Fact 1: n_A ≥ the number of partial fillings, F_P included.* In a filling, quadrant i holds internal links i and i + 1 (mod 4). A partial filling leaves at least 2 internal links held by exactly one plaquette of γ. By closure, each lies in a second plaquette of γ. That plaquette is not a line plaquette, since the only line plaquettes holding the link are its 2 quadrants, and one of them is outside γ (Lemma 3.3(d)). So it is of type A (Lemma 3.3(d)). Internal links of distinct fillings are distinct, and a type-A plaquette holds exactly 2 class-1 links (Lemma 3.3(e)). Count the pairs (type-A plaquette of γ, singly held internal link in it): at least 2 per partial filling, at most 2 per type-A plaquette.

*Fact 2.* Line plaquettes of F_P, line plaquettes of the other fillings, and type-A plaquettes are disjoint classes. So #γ ≥ m + Σ_{P′≠P} g(P′) + n_A.

*Fact 3.* Call a corner of P missing when the quadrant of F_P there is not in γ. There are 4 − m missing corners. A line link of ∂P at a missing corner is held by a line plaquette of γ in a filling F_{P′} with P′ ≠ P and P′ containing that coarse link (Lemma 3.3(c), (g)). Such a P′ meets ∂P in at most one coarse link (Lemma 3.3(h)). Call it ℓ(P′). The line plaquettes of F_{P′} hold at most the two positions of ℓ(P′) among the line links of ∂P, one each.

*Fact 4.* For ℓ ∈ ∂P, let u(ℓ) ∈ {0, 1, 2} be the number of its positions at missing corners. Let c(ℓ) := Σ_{P′≠P : ℓ(P′)=ℓ} (g(P′) + [F_{P′} partial]). If u(ℓ) ≥ 1, some P′ with ℓ(P′) = ℓ has g(P′) ≥ 1, and it contributes at least 2: g + 1 when partial, 4 when full. So c(ℓ) ≥ 2. If u(ℓ) = 2, either one P′ holds both positions, with g(P′) ≥ 2 and a contribution of at least 3, or two contribute at least 2 each. So c(ℓ) ≥ 3.

Fillings with different ℓ(P′) are different. Facts 1 and 2 give

```text
#gamma  >=  m + [F_P partial] + sum_{l in dP} c(l).
```

The cases:

| m | missing corners | u over the 4 links of ∂P | lower bound on #γ |
|---|---|---|---|
| 3 | one | 1, 1, 0, 0 | 3 + 1 + 2 + 2 = 8 |
| 2 | two adjacent, along ℓ | 2 on ℓ; 1, 1 on the two links at its ends; 0 | 2 + 1 + 3 + 2 + 2 = 10 |
| 2 | two opposite | 1, 1, 1, 1 | 2 + 1 + 8 = 11 |
| 1 | three | 2, 2, 1, 1 | 1 + 1 + 6 + 4 = 12 |
| 0 | four | 2, 2, 2, 2 | 0 + 0 + 12 = 12 |

For m = 4, let γ ≠ F_P. Off-link connectivity gives p′ ∈ γ ∖ F_P that holds an internal link L of F_P. p′ is not a line plaquette, since the line plaquettes holding L lie in F_P. So p′ is of type A (Lemma 3.3(d)). Its 3 other off links are not internal links of F_P: its other class-1 link is internal to a different filling (Lemma 3.3(e)), and its class-2 links lie in no filling. By closure, each lies in a second plaquette of γ. These plaquettes are outside F_P, whose off links are its internal links. They differ from p′, and they are pairwise distinct, since a plaquette other than p′ shares at most one link with p′. So #γ ≥ 4 + 1 + 3 = 8.

*Proof of (ii).* If X has n ≥ 2 polymers, |X| ≥ 8 by Lemma 3.5. If X = (γ) with γ ≠ F_P, then Y″(γ) ⊇ ∂P, so γ holds all 8 line links of ∂P, and (i) applies. ∎

The bound 8 is attained. The 16 one-cube bumps F_P ⊕ ∂C of NOTE-YM4-03C §7.5 keep 3 quadrants of F_P and have 8 plaquettes. This is the case m = 3 above. The closure hypothesis cannot be dropped. F_P together with one more plaquette through an internal link is a polymer of 5 plaquettes that holds ∂P. It is not closed, so its activity is 0 (Lemma 3.2). So row C09's clause "no polymer of 5, 6 or 7 plaquettes holds all of the boundary of P at both positions" holds for closed polymers. Its frozen form "every V-dependent polymer" already implies closure.

**Lemma 3.25 (E|χ_{1/2}|).** *Claim:* e_χ = 8/(3π), and 8/(3π) < 8489/10000.

*Proof.* By Weyl's integration formula on SU(2) (REPORTED: Bröcker and tom Dieck 1985, Representations of Compact Lie Groups, Springer GTM 98, §IV.1), a class function f integrates as (2/π) ∫_0^π f(θ) sin²θ dθ. With χ_{1/2} = 2 cos θ,

```text
e_chi = (2/pi) int_0^pi 2|cos t| sin^2 t dt = (8/pi) int_0^{pi/2} cos t sin^2 t dt = 8/(3 pi).
```

Machin's formula π = 16 arctan(1/5) − 4 arctan(1/239) (REPORTED). For 0 < y < 1 the alternating series gives arctan y ≥ y − y³/3 + y⁵/5 − y⁷/7 and arctan y ≤ y. So π ≥ 1231847548/392109375 > 3.1414. And 8/(3 × 3.1414) < 0.848880 < 0.8489. ∎

**Proposition 3.26 (the readout).** *Hypotheses:* those of Theorem G0. *Claim:* for every coarse plaquette P,

```text
| c_1/2(P) - 2 t_2(beta_0)^4 |  <=  e_chi * 6 alpha e^{-8 theta}  <=  (8489/10000) * 6 alpha e^{-8 theta}.
```

*Proof.* c_{1/2}(P) = ⟨χ_{1/2}(V_P), log ρ_1⟩ in coarse Haar, since ⟨χ_{1/2}(V_P), χ_{1/2}(V_P)⟩ = 1 (NOTE-YM4-03C §4, the readout). Absolute convergence (Lemma 3.16) allows the sum over clusters to pass through the pairing. If Y(X) ⊉ ∂P, then z^X does not depend on some V_ℓ with ℓ ∈ ∂P, and ∫ χ_{1/2}(V_P) dV_ℓ = 0. So only clusters with Y(X) ⊇ ∂P contribute. The constant contributes 0 too. X = (F_P) contributes 2t_2⁴ (Lemma 3.23). Every other contributing cluster has |⟨χ_{1/2}(V_P), z^X⟩| ≤ e_χ sup_V |z^X|, since V_P is Haar distributed. It has |X| ≥ 8 (Lemma 3.24(ii)), so sup|z^X| ≤ e^{−8θ} ∏_i ω(γ_i). It holds ℓ for each ℓ ∈ ∂P. Lemma 3.19 at one ℓ ∈ ∂P and Proposition 3.15 bound the sum of ∏ω over these clusters by (1/2) × 12 × α. Lemma 3.25 gives the last inequality. ∎

The draft's T = (8489/10000)·12α e^{−8θ} follows, and is weaker by the factor 2. For any pair (α, θ), the ratio T_draft/T_here is exactly 2 when both use 8489/10000. The minimizing θ over the grid is therefore the same for both.

The same argument gives row C10b's projection bound. Any decomposition of a function into terms R(Y) with #Y ≥ 4 has |c_P| ≤ e_χ Σ_{Y⊇∂P} sup|R(Y)| ≤ e_χ e^{−4κ} Σ_{Y∋ℓ} e^{κ#Y} sup|R(Y)|. So its norm is at least e^{4κ} |c_P|/e_χ.

## 3.11 Uniformity, and the proof of Theorem G0

**Uniformity.** The inputs of every bound are ε, a function of β_0 alone; the head N(n) or 6F(n); #W(e_0) = 12; D = 20; the factors e^{−4(θ−κ)} and e^{−8θ}; and e_χ. Each lemma uses only that N is even with N ≥ 8. Lemma 3.3(a) needs fine side at least 3. Lemma 3.3(h) needs coarse side at least 4. No step uses N, K or the number of plaquettes, except the finiteness statement inside Lemma 3.16, which enters no bound. The tail needs only the degree bound 20. For the refined head, the hypothesis N(n) ≥ N_e(n) must hold on the lattice in use. Row C03 reads the counts on fine 8⁴ and 12⁴ only. Its extension to every N ≥ 8 is not derived here (section 3.15).

**Proof of Theorem G0.** Item 1: Corollary 3.11, the Corollary to Proposition 3.15, Proposition 3.15 and Lemma 3.16. Item 2: Proposition 3.18. Item 3: Proposition 3.20. Item 4: Proposition 3.26. Item 5: the uniformity paragraph. The closing statement: Lemmas 3.21 and 3.22. ∎

## 3.12 The frozen constants and formulas against the proved ones

"Equal" means the proved statement is exactly the frozen one. "No" with "draft weaker" means the frozen statement is true but follows from a sharper proved one.

| # | Item (row) | Frozen in the draft | Proved here | Equal |
|---|---|---|---|---|
| 1 | H_0 (HYPOTHESIS) | ρ_0 = ∏_p c_0(β_0)(1 + K_p), K = Σ_{n≥2} n t_n χ_{(n−1)/2}, t_n = I_n/I_1, c_0(x) = Σ_m (x/2)^{2m}/(m!(m+1)!) | the same (§3.1, Lemma 3.1) | yes |
| 2 | H_k class at k = 1 (HYPOTHESIS) | Y with #Y ≥ 4 containing a closed loop; R real, coarse-gauge invariant, a function of V\|_Y | the same (Proposition 3.18) | yes |
| 3 | norm (HYPOTHESIS) | sup_ℓ Σ_{Y∋ℓ} e^{κ#Y} sup_V \|R(Y;V)\| | used as frozen | yes |
| 4 | Wilson term inside R_k(∂P) (HYPOTHESIS) | carried inside R_k(∂P) | at k = 1, R_1(∂P) holds z_{F_P} = Σ n t_n⁴ χ_{(n−1)/2}(V_P) (Lemma 3.23) | yes |
| 5 | κ (HYPOTHESIS) | 1/4 | used; G0 needs only θ ≥ κ | yes |
| 6 | D (HYPOTHESIS, C01) | 20, minimum 10 | 20 and 10 (Lemma 3.3(f)) | yes |
| 7 | plaquettes per link; Finner exponent (HYPOTHESIS, THEOREMS) | 6; 6 | 6; 6 (Lemma 3.3(a), Lemma 3.7) | yes |
| 8 | #W(e_0) (HYPOTHESIS) | 12 | 12, with 2 links in each of the 6 fillings through ℓ (Lemma 3.3(g)) | yes |
| 9 | F_20(n) (HYPOTHESIS) | C(20n, n)/(19n + 1) | the number of rooted 20-ary subtrees (Lemma 3.9) | yes |
| 10 | μ (HYPOTHESIS, C01) | 20²⁰/19¹⁹ ∈ [53.00068, 53.00069] | the same; sup and limit of F(n+1)/F(n) (Lemma 3.10) | yes |
| 11 | E\|χ_{1/2}\| (HYPOTHESIS) | 8/(3π) ≤ 8489/10000 | the same (Lemma 3.25) | yes |
| 12 | n_max (HYPOTHESIS) | 10 | any n_max ≥ 4 gives a valid S | yes |
| 13 | uniformity (HYPOTHESIS) | no bound involves N, K or the number of plaquettes | proved for G0 (§3.11); the refined head needs C03's counts on every N ≥ 8 | yes (crude); conditional (refined) |
| 14 | lattice conditions (HYPOTHESIS) | exact counts need fine sides ≥ 8; tail needs only degree 20 | G0 needs N even, N ≥ 8 (coarse side ≥ 4); the tail needs degree ≤ 20 | yes |
| 15 | ε (CERTIFICATES) | ε_6 = ‖K‖_{L⁶}, ε⁶ = Σ_k C(6,k)(−1)^{6−k} c_0(kβ)/c_0(β)^k | the same (Lemma 3.7) | yes |
| 16 | S(x) (CERTIFICATES) | head n = 4..10, 6F_20(n) for n = 11..48, tail 6F_20(49)x⁴⁹/(1 − μx), μx < 1 | a valid bound on Σ_n N_e(n)xⁿ when N(n) ≥ N_e(n) (Corollary 3.11) | yes |
| 17 | crude head (CERTIFICATES) | N(n) = 6F_20(n) | valid for every off link (Corollary 3.11) | yes |
| 18 | head-free head (CERTIFICATES) | N(n) = 0 | not a certificate, since N_e(4) = 1 for class-1 e; valid as the lower limit of δ_1 over count vectors, the role C06, C08, C12, C14 give it | yes (in its role) |
| 19 | refined head (CERTIFICATES) | N(n) = the C03 counts | valid exactly when the counts bound N_e(n) on the lattice used | yes, CONJECTURE |
| 20 | C_0 MET (CERTIFICATES) | ∃ grid θ, rational α with S⁺(ε⁺e^{2α+θ}) ≤ α ≤ 1/4 | sufficient for H_1; the cap never binds, since α_− ≤ 1/8 (Lemma 3.22) | yes (in effect) |
| 21 | a-search (CERTIFICATES) | g(α) = S(εe^{2α+θ}) − α convex | convex (Lemma 3.21(i)) | yes |
| 22 | δ_1 (CERTIFICATES outputs) | min over certified pairs of 12α e^{−4(θ−κ)} | min of 6α e^{−4(θ−κ)} (Proposition 3.20); 6 is the least the method gives | **no**: draft weaker by exactly 2 |
| 23 | readout T (CERTIFICATES outputs) | (8489/10000)·12α e^{−8θ}, minimized over certified pairs | e_χ·6α e^{−8θ} ≤ (8489/10000)·6α e^{−8θ} (Proposition 3.26) | **no**: draft weaker by exactly 2 (by 2.0002 against e_χ) |
| 24 | θ at the δ_1 optimum; existence at θ = 1/4 (CERTIFICATES, outline §5) | every δ_1 optimum at θ = 1/4; θ = 1/4 decides existence | the same (Lemma 3.21) | yes |
| 25 | Lemmas A and B (THEOREMS) | used | A as in NOTE-YM4-03C §2; B in polymer form (Lemma 3.2) | yes |
| 26 | Finner bound (THEOREMS) | sup_V \|z_γ\| ≤ ε_6^{#γ} | the same (Lemma 3.7) | yes |
| 27 | a(γ) (THEOREMS) | α #off(γ) ≤ 2α #γ | the same, sharp (Lemma 3.4) | yes |
| 28 | d(γ) (THEOREMS) | θ #γ | used | yes |
| 29 | the KP criterion (THEOREMS) | Kotecký–Preiss with a(γ), d(γ) | per-link bound Σ_{X∋e} ≤ α, by Penrose trees (Proposition 3.15); the same bound as KP (Remark 3.17) | yes |
| 30 | test set (THEOREMS) | W(e_0) | W(e_0), with every holding cluster meeting it twice (Lemma 3.19) | the set: yes; its constant: row 22 |
| 31 | BFS injection (THEOREMS, C01) | at most 6F_20(n) off-link-connected sets of n plaquettes through a given off link | the same, for all such sets, closed or not (Lemmas 3.8, 3.9, Corollary 3.11) | yes |
| 32 | ratio monotonicity (C01, ledger L08) | F(n+1)/F(n) strictly increasing and below μ, checked for n ≤ 59 | for every n ≥ 0, with limit μ (Lemma 3.10) | formula yes; the proof covers all n, stronger than the n ≤ 59 check |
| 33 | #Y″ (THEOREMS) | #Y″(γ) ≤ #γ | the same; also ≤ the number of line plaquettes (Lemma 3.6(iv)) | yes |
| 34 | size of V-dependence (THEOREMS) | only at size ≥ 4 | the same (Lemma 3.5, Proposition 3.18(iv)) | yes |
| 35 | small closed sets (C01) | the closed sets of ≤ 4 plaquettes are the fillings; none of ≤ 3 | the same (Lemma 3.5) | yes |
| 36 | filling membership (C01) | every off link in 0 or 1 filling | class 1 in exactly 1, classes 2 and 3 in none (Lemma 3.3(d)) | yes |
| 37 | G0 itself (THEOREMS) | C_0 ⇒ H_1 with δ_1 = min 12α e^{−4(θ−κ)} | C_0 ⇒ H_1 with min 6α e^{−4(θ−κ)} (Theorem G0) | **no**: draft weaker by exactly 2 |
| 38 | C07 | δ_1 ∈ [0.011044, 0.011045], α ≈ 9.2037e-4, θ = 1/4; 2δ_1e^{δ_1} ∈ [0.02233, 0.02234] | α_− ∈ [9.2037088980e-4, 9.2037089080e-4] (MEASURED, exact); δ_1 = 6α_− ∈ [0.00552222533, 0.00552222535]; 2δ_1e^{δ_1} ≤ 0.011106 | **no** (half). c(δ_1), δ_2, Σδ_k are G1 values, not recomputed |
| 39 | C08 | δ_1 ∈ [9.42e-6, 9.45e-6]; head-free limit [9.372e-6, 9.373e-6]; δ_1/(12e·c_{1/2}) ∈ [3.6e3, 3.8e3]; crude/refined ∈ [1170, 1172] | [4.71e-6, 4.725e-6]; [4.686e-6, 4.6865e-6]; [1.8e3, 1.9e3]; ratio unchanged (draft brackets halved, not rechecked) | **no** (half); ratio yes |
| 40 | C09 | T as row 23; T/P_10 ∈ [1.0e-3, 1.1e-3] (1/4000), [1.6e-2, 1.75e-2] (1/2000), [0.26, 0.28] (1/1000), [1.10, 1.13] (1/700), [1.38e4, 1.40e4] (1/100), same i = 194, 150, 105, 83, 0; no polymer of 5–7 plaquettes holds ∂P | T halves: [5.0e-4, 5.5e-4], [8.0e-3, 8.75e-3], [0.13, 0.14], [0.55, 0.565], [6.9e3, 7.0e3], the same i; the exclusion holds for closed polymers and for clusters (Lemma 3.24), and the bound 8 is attained by the 16 bumps | T and brackets **no** (half); exclusion yes |
| 41 | C10 | fine norm 12\|s\|e^{8κ}, coarse norm 12\|s\|e^{4κ} (6 coarse plaquettes per line link) | the same norm arithmetic | yes |
| 42 | C10b | δ_in = 12\|s\|e^{6κ}; norm ≥ e^{4κ}\|c_P\|/E\|χ_{1/2}\| | the same; the projection bound by the argument of Proposition 3.26 | yes; c(δ_in) is G1 |
| 43 | C11 | crude 1/64: δ_1 ∈ [0.10165, 0.10166], 2δ_1e^{δ_1} ∈ [0.22505, 0.22507] > 1/8, so C_1 NOT_MET | α_− ∈ [8.4710870117e-3, 8.4710870127e-3] (MEASURED); δ_1 ∈ [0.05082652207, 0.05082652208]; 2δ_1e^{δ_1} ≤ 0.106953 ≤ 1/8, so C_1 MET; δ_1 > 0.0496175, so the self-map stays NOT_MET under G1 as drafted | **no** |
| 44 | C12 | 1/50: head-free δ_1 ∈ [0.072645, 0.072646]; C_1 and the self-map NOT_MET under every count model (DERIVED) | head-free 6α_− ≤ 0.03632291, C03 head 6α_− ≤ 0.03632354 (MEASURED); 2δ_1e^{δ_1} ≤ 0.0754 ≤ 1/8 and δ_1 < δ_crit^−: under G1 as drafted, C_1 and the self-map are MET at 1/50 with the C03 head | **no**: the NOT_MET clauses rest on the factor 12 |
| 45 | C13 | crude self-map edge MET 0.01369, NOT_MET 0.01370 | reproduced with 12 (MEASURED); with 6: MET 0.01556, NOT_MET 0.01557 (MEASURED, under G1 as drafted, δ_crit^− = 0.0496174) | **no** |
| 46 | C14 | refined edge 0.01959/0.01960; head-free NOT_MET at 0.01960, so β_ind < 0.01960 for every count vector; 1/64: δ_1 ∈ [2.0347e-3, 2.0348e-3] | reproduced with 12; with 6: 0.02029/0.02030 for the C03 head and the head-free vector, so β_ind < 0.02030 for every count vector; 1/64: [1.01735e-3, 1.0174e-3]; the ordering 0.02029 < 0.02075 < 0.02247 holds | **no** |
| 47 | C16 | δ_20 ≤ c(δ_1)^{19}δ_1 ∈ [2.30e-9, 2.31e-9]; osc ≤ (512/e)δ_m ≤ 4.35e-7 | the formula (512/e)δ_m follows from the norm as frozen; δ_1 halves, so with c increasing (a G1 claim) δ_20 ≤ 1.155e-9 and osc ≤ 2.18e-7 | formula yes; values **no** |

**all_equal = false.** Rows 22, 23 and 37 differ in the constant, with the draft weaker by exactly a factor 2. Rows 38 to 40 and 43 to 47 inherit it. Row 32 is proved in a stronger form than the draft checks. Every other row is proved exactly as frozen.

## 3.13 What the factor 2 does to the frozen rows

- The frozen 12-forms are true statements, since they follow from the 6-forms. Each frozen value computed with 12 is a valid bound.
- They are not what the proof gives. Every NOT_MET that rests on 12 is a NOT_MET of the weaker constant, not of the method. These are: C11's C_1 clause; C12's C_1 and self-map clauses, including their DERIVED tags; the C13 and C14 edges and the DERIVED clause "β_ind < 0.01960 for every count vector"; the HYPOTHESIS regime "β_0 ≤ 0.0196", the SCOPE windows "β_ind ≈ 0.01959" and ledger L11; and C09's "lost between 1/1000 and 1/700", since T/P_10 ≤ 0.565 at 1/700 with the proved T.
- These do not change: the C_0 edges of C04, C05 and C06, which do not involve the prefactor; C15; C10 and the norm arithmetic of C10b; C01 to C03.
- Two ways to freeze. (a) Freeze 6 and recompute the affected rows. Under G1 as drafted, the windows move to 0.01556 (crude) and 0.02029 (C03 head and head-free), section 3.14, block G. (b) Keep 12, and reword every NOT_MET above as a property of the 12-certificate. Option (a) matches the critic's demand (blocking item 5) that the proved constants equal the frozen ones.

## 3.14 Scratch checks (MEASURED; not evidence; no step of the proof rests on them)

[`G0-b-checks.py`](G0-b-checks.py) uses integers and Fractions only. Its output is [`G0-b-checks.out`](G0-b-checks.out). It runs in about 15 seconds.

- **A.** F_20(4..12) equal the draft's nine values. μ ∈ [53.00068, 53.00069]. The product formula of Lemma 3.10 equals F(n+1)/F(n) for n = 0..120, and the ratios are strictly increasing and below μ there. F_20(1..3) = 1, 20, 590.
- **B.** π ∈ [1231847548/392109375, 5277328977275528/1679825970703125], and 8/(3π) ∈ [0.8488264, 0.8488266] < 8489/10000.
- **C.** On fine (ℤ/8)⁴: 24576 plaquettes, 16384 links, each link in 6 plaquettes; off links per plaquette 2 or 4; off-link degree from 10 to 20; distinct neighbours share exactly one link; link classes 0, 1, 2, 3 number 2048, 6144, 6144, 2048; plaquette class patterns (0,0,1,1) × 6144, (1,1,2,2) × 12288, (2,2,3,3) × 6144; each line plaquette has one center and both its off links end there; 1536 fillings of 4; class-1 links in exactly 1 filling, classes 2 and 3 in none; #W(e_0) = 12 at every line link, with 2 links in each of the 6 fillings through ℓ.
- **D.** Closure-driven growth from the 6 plaquettes through e_0 of one coarse link of P, up to 8 plaquettes: 72624 states and 126 closed sets. Those holding all 8 line links of ∂P: 1 of size 4, which is F_P, and 16 of size 8, each keeping 3 quadrants of F_P. None of size 5, 6 or 7. This agrees with Lemma 3.24 and its equality case.
- **E.** Off-link-connected sets through one off link of each class, n = 1..4: (6, 85, 1648, 35478), (6, 105, 2138, 47232), (6, 105, 2282, 52200), each below 6F_20(n) = (6, 120, 3540, 123240).
- **F.** The crude certificate at θ = 1/4, with exact rational ε enclosures and exact series: at β_0 = 1/100, α_− ∈ [9.2037088980e-4, 9.2037089080e-4], so 12α_− lies in C07's bracket and 6α_− ∈ [0.00552222533, 0.00552222535]; at 1/64, α_− ∈ [8.4710870117e-3, 8.4710870127e-3], so 12α_− lies in C11's bracket and 6α_− ≈ 0.05082652. The lower ends come from the monotone iteration from α = 0, whose iterates stay below α_−. The upper ends are values where S(x⁺) ≤ α.
- **G.** Conditional on G1 as drafted, with δ_crit^− = 0.0496174 taken from C13's bracket. With the factor 12 the reads give the frozen edges 0.01369/0.01370 (crude) and 0.01959/0.01960 (C03 head). With the factor 6 they give 0.01556/0.01557 (crude) and 0.02029/0.02030 (C03 head and head-free). At 1/50, 6α_− ≤ 0.03632291 (head-free) and ≤ 0.03632354 (C03 head), both admissible.

## 3.15 Gaps (OPEN)

1. Finner's inequality is REPORTED and is not reproved here.
2. The exponential formulas of Lemmas 3.12 and 3.14 are REPORTED standard combinatorics, given with a sketch. The analytic passage from the formal identity to log ρ_1 (Lemma 3.16) is written out.
3. Lagrange inversion, Weyl's integration formula, Machin's formula and the Bessel series of I_1 are REPORTED.
4. The refined head rests on C03's counts, a CONJECTURE. G0 with that head also needs N(n) ≥ N_e(n) on every fine torus with N ≥ 8, not only on 8⁴ and 12⁴. That needs a proof that no closed set of at most 10 plaquettes winds at fine side 8, and that N_e(n) depends only on the class of e. Neither is derived here. The crude certificate needs neither.
5. Exact arithmetic was redone here only for the crude certificate at 1/100 and 1/64, the head-free and C03 heads at 1/50, and the C13/C14 edges. The proved values listed for C08, C09 and C14 at 1/64 are the draft's brackets halved, not rechecked.
6. The G1 quantities c(δ), δ_crit, δ_2, Σδ_k, δ_20 and the oscillation bound are not derived here. Block G and rows 43 to 47 use G1 as drafted. δ_crit^− = 0.0496174 is the lower end of C13's bracket. The critic's value 0.049617491 could move an edge only if 6α_− fell between the two numbers at an edge point.
7. The constant 6 is optimal for δ_1 within this method (section 3.9). For the readout, a sharper fractional cover using all of ∂P may exist. It is not explored.
8. Row C04's phrase "the tail diverges whenever μ e^{1/4} ε_6 ≥ 1" is wrong at equality, where the Fuss–Catalan tail converges (Corollary 3.11, remark). This is outside G0, and no frozen read sits at equality.

## References

- Abramowitz, M., Stegun, I. A. (1964). Handbook of Mathematical Functions. National Bureau of Standards, Applied Mathematics Series 55. Formula 9.6.10.
- Battle, G. A., Federbush, P. (1984). A note on cluster expansions, tree graph identities, extra 1/N! factors!!! Lett. Math. Phys. 8, 55–57.
- Bröcker, T., tom Dieck, T. (1985). Representations of Compact Lie Groups. Springer, Graduate Texts in Mathematics 98.
- Brydges, D. C. (1986). A short course on cluster expansions. In: Osterwalder, K., Stora, R. (eds.), Phénomènes critiques, systèmes aléatoires, théories de jauge (Les Houches 1984). North-Holland, 129–183.
- Fernández, R., Procacci, A. (2007). Cluster expansion for abstract polymer models. New bounds from an old approach. Commun. Math. Phys. 274, 123–140.
- Finner, H. (1992). A generalization of Hölder's inequality and some probability inequalities. Ann. Probab. 20, 1893–1901.
- Kotecký, R., Preiss, D. (1986). Cluster expansion for abstract polymer models. Commun. Math. Phys. 103, 491–498.
- Mayer, J. E., Mayer, M. G. (1940). Statistical Mechanics. Wiley, New York.
- Penrose, O. (1967). Convergence of fugacity expansions for classical systems. In: Bak, T. A. (ed.), Statistical Mechanics: Foundations and Applications. Benjamin, New York, 101–109.
- Raney, G. N. (1960). Functional composition patterns and power series reversion. Trans. Amer. Math. Soc. 94, 441–451.
- Stanley, R. P. (1999). Enumerative Combinatorics, vol. 2. Cambridge University Press. §5.1, §5.3, §5.4.
- Repository: NOTE-YM4-03-ONE-SCALE-BLOCKING.md §2 (the map, Proposition 2, Lemma 3), §3 (Theorem 4), §5 (Theorem 8 and the SU(2) character expansion); NOTE-YM4-03C-BLOCKED-ACTION.md §2 (the line gauge, Lemma A), §4 (the readout), §6 (Lemma B, the polymer form), §7.5 (the disk rule, the bumps), §12 (OPEN: the local bound this section supplies at strong coupling); NOTE-YM4-04-TWO-TERNARY-BLOCKS-20261107.md §2 and §6 (the global Cauchy remainder this replaces); NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md §1 (6 plaquettes per link); LEMMA-0001-GAUGE-INVARIANCE.md; LEMMA-0002-HAAR-MOMENTS.md.
