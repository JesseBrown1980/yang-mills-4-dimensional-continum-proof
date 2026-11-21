## 3. Theorem G0 (step 0): from the Wilson measure to H_1, route A

**Status.** DERIVED in this section: Theorem G0 and every lemma below. They rest on [YM4-03](NOTE-YM4-03-ONE-SCALE-BLOCKING.md) (Theorem 4, Proposition 2, Theorem 9 (a)), on [YM4-03C](NOTE-YM4-03C-BLOCKED-ACTION.md) (§2 Lemma A, §6 Lemma B and the polymer form), and on two REPORTED theorems, Kotecký and Preiss (1986) and Finner (1992), stated as Theorems 3.13 and 3.7. CONJECTURE: the refined head of the count vector, that is the C03 counts at n = 5 to 10. With that head, G0 is conditional on C03. The proof gives better constants than the draft. The test set needs 6 off links, not 12. So δ_1 and the readout tail T are at most one half of their frozen values, at every certified (α, θ). The frozen values stay valid. Section 3.11 records what the factor 2 changes in rows C07 to C16. No engine ran. The numbers quoted from the two scratch scripts of section 3.14 are exact rational reads with upward rounding, not evidence.

Symbols, binding for this section. a(g) = ½ Re Tr g for g ∈ SU(2). With a polymer γ as argument, a(γ) = α·#off(γ) and d(γ) = θ·#γ are the Kotecký–Preiss functions. α > 0 and θ ≥ κ are the Kotecký–Preiss parameters; the certificate takes θ in {1/4 + i/64}. b = 2 is the blocking factor. κ = 1/4 is the norm weight. D = 20. μ = 20²⁰/19¹⁹. F_20(n) = C(20n, n)/(19n + 1). #A is the number of elements of a set A.

### 3.0 The statement

**Theorem G0.** Assume:

- (H1) Λ_0 = (ℤ/N)⁴ with N even and N ≥ 8, and Λ_1 = (ℤ/(N/2))⁴. B is the YM4-03 line map at b = 2, (BU)_μ(x′) = U_μ(2x′)U_μ(2x′ + e_μ). ρ_1 is its exact Haar pushforward density (YM4-03 §3, Theorem 4), written in the line gauge of YM4-03C §2.
- (H2) β_0 > 0, the Wilson weight is w = e^{β_0 a}, K := e^{β_0 a}/c_0(β_0) − 1, and ε := ε_6(β_0) = ‖K‖_{L⁶(SU(2))}.
- (H3) N(n) ≥ 0 for n ≥ 4 is a **valid count vector**: N(n) ≥ N_w(n) for every off link w and every n, where N_w(n) is the number of polymers (section 3.3) of n plaquettes that hold w. N(n) = 6F_20(n) is valid (Corollary 3.12). S(x) := Σ_{n≥4} N(n)xⁿ.
- (H4) α > 0 and θ ≥ κ satisfy S(εe^{2α+θ}) ≤ α, with the series convergent.

Then:

- (C1) log ρ_1(V) = const_1 + Σ_Y R_1(Y; V), with Y over the sets of coarse links that contain a closed loop. Every R_1(Y; ·) is real, coarse-gauge invariant, a function of V restricted to Y, and zero unless #Y ≥ 4. The coarse Wilson term lies inside R_1(∂P).
- (C2) The norm obeys
  ```text
  norm_kappa(R_1) := sup_l sum_{Y containing l} e^{kappa #Y} sup_V |R_1(Y;V)|
                   <= delta_1 := 6 S(eps e^{2 alpha + kappa})
                   <= 6 e^{-4(theta - kappa)} S(eps e^{2 alpha + theta})
                   <= 6 alpha e^{-4(theta - kappa)}  =  (1/2) * 12 alpha e^{-4(theta - kappa)}.
  ```
- (C3) For every coarse plaquette P, the coefficient c_½(P) of χ½(V_P) in log ρ_1 obeys
  ```text
  | c_1/2(P) - 2 t_2(beta_0)^4 |  <=  T := (8/(3 pi)) * 6 e^{-8 theta} S(eps e^{2 alpha + theta})
                                   <=  (8489/10000) * 6 alpha e^{-8 theta}  =  (1/2) * (8489/10000) * 12 alpha e^{-8 theta}.
  ```
- (C4) No constant in (C2) or (C3) depends on N, K or the number of plaquettes N_p.

So the frozen implication "C_0 MET ⇒ H_1(κ, δ_1) with δ_1 = min 12αe^{−4(θ−κ)}, and c_½(P) ∈ 2t_2⁴ ± (8489/10000)·12αe^{−8θ}" holds, with a factor 2 to spare. H_1(κ, δ) is monotone in δ, so the frozen δ_1 is an admissible but loose choice.

A frozen C_0 read meets (H4). The read checks S⁺(ε⁺e^{2α+θ}) ≤ α at a rational α, with ε⁺ ≥ ε and S⁺ an upper enclosure of the head plus the series to n = 48 plus the n = 49 tail. Corollary 3.12 shows that this S⁺ bounds S from above when the head is valid.

### 3.1 Parity classes, quarters and fillings

For a fine site x let O(x) = {λ : x_λ odd}. O(x) is well defined because N is even. Coarse sites are the x with O(x) = ∅. A fine link (x, μ) joins x to x + e_μ. Its **transverse odd set** is O_⊥(x, μ) = O(x) ∖ {μ}, the same at both ends. The link is a **line link** when O_⊥ = ∅, as in YM4-03C §2. Otherwise it is an **off link of class** c = #O_⊥ ∈ {1, 2, 3}.

A coarse link ℓ = (x′, μ) has position 0, the line link (2x′, μ), and position 1, the line link (2x′ + e_μ, μ). Its **midpoint** is m_ℓ = 2x′ + e_μ, with O(m_ℓ) = {μ}. The midpoint determines ℓ.

A fine plaquette p with base x in the plane {μ, ν} has the links (x, μ), (x + e_μ, ν), (x + e_ν, μ), (x, ν). Its **outer odd set** is T(p) = O(x) ∖ {μ, ν}. All four corners of p give the same T(p).

**Lemma 3.1 (the b = 2 geometry).** Let N be even and N ≥ 8.

1. Every link lies in exactly 6 plaquettes. A plaquette has 4 distinct links. Two distinct plaquettes share at most one link.
2. If T(p) = ∅, p has two line links, one in each direction of its plane, and two off links of class 1. Such a p is a **quarter**. If #T(p) = t ≥ 1, p has no line link and four off links: two of class t and two of class t + 1.
3. The two off links of a quarter p meet at its corner s(p), and O(s(p)) is the plane {μ, ν} of p. The 4 plaquettes of that plane with corner s(p) are quarters. They tile the 2 × 2 fine square centered at s(p), which is the **filling** F_Q of the coarse plaquette Q with center s(p). Every quarter lies in exactly one filling. The off links of the quarters of F_Q are the 4 **internal links** of F_Q, from its center to the midpoints of its 4 sides. Each internal link lies in exactly 2 quarters of F_Q, and the quarters of F_Q form a 4-cycle in which consecutive quarters share one internal link.
4. Every class-1 off link is an internal link of exactly one filling. It lies in 2 quarters, both of that filling, and in 4 plaquettes that are not quarters, each with #T = 1. An off link of class 2 or 3 lies in no quarter.
5. The quarters of F_Q hold exactly the 8 line links of ∂Q, both positions of its 4 coarse links. The quarter at a coarse corner c of Q holds the two line links of ∂Q at c. If Q ≠ P, a quarter of F_Q holds at most one line link of ∂P.
6. Let e_0 be position 0 of ℓ = (x′, μ). The 6 plaquettes through e_0 are the quarters at the corner 2x′ of the fillings of the 6 coarse plaquettes Q that contain ℓ. Their 12 off links are distinct. This set is W(e_0), and #W(e_0) = 12. Each of the 6 plaquettes has exactly one off link at m_ℓ. These are the 6 off links at m_ℓ. Call this set W′(ℓ), #W′(ℓ) = 6. The same holds for position 1 of ℓ, with the same W′(ℓ).
7. Join two distinct plaquettes when they share an off link. In this graph a quarter has degree 10 and every other plaquette has degree 20.

*Proof.* 1. Fine side N ≥ 3 makes the four corners of a plaquette distinct, so its 4 links are distinct. A link (y, μ) lies in the plaquettes of the planes {μ, ν}, ν ≠ μ, with base y or y − e_ν. These are 3 × 2 = 6 distinct plaquettes. Two links of one plaquette are either parallel at distance 1 or perpendicular with a common corner. In both cases they fix the plane and the base point, since the side is at least 3. So two distinct plaquettes cannot share two links.

2. The two μ-links of p sit at x and x + e_ν. Their transverse odd sets are T(p) together with ν or without it, and exactly one of the two holds ν. The same holds for the two ν-links with μ. So the classes are t, t + 1, t, t + 1 with t = #T(p), and class 0 is a line link.

3. Take T(p) = ∅. The off μ-link has O_⊥ = {ν} and the off ν-link has O_⊥ = {μ}. These two links are the ones at the corner whose μ- and ν-coordinates are both odd. That corner s has O(s) = {μ, ν}. The 4 plaquettes of the plane {μ, ν} with corner s have T = ∅ and corners with even coordinates at the far ends, so they tile the 2 × 2 square of the coarse plaquette with center s. Their off links are the 4 links from s to s ± e_μ and s ± e_ν. Each lies in the two of them on either side. A quarter p lies in the filling with center s(p) and in no other, since s(p) is determined by p.

4. A class-1 link of direction μ with O_⊥ = {ν} has one end s with O(s) = {μ, ν} and one end with odd set {ν}. So it is the internal link from s along ±e_μ of the filling with center s, and of no other filling, since only one end has two odd coordinates. A plaquette through it in the plane {μ, λ} has T = O(s) ∖ {μ, λ}. That is empty exactly when λ = ν. So 2 of its 6 plaquettes are quarters, both in that filling, and 4 have T = {ν}. A quarter's off links have class 1 by item 2, so a link of class 2 or 3 lies in no quarter.

5. A quarter's two line links meet at its corner with even coordinates, a coarse site c, one in each direction of its plane. For the quarter of F_Q at c these are the positions next to c of the two coarse links of ∂Q at c. If a quarter of F_Q holds two line links of ∂P, then P and Q both contain the two perpendicular coarse links at c that carry them. On a coarse side N/2 ≥ 3 two perpendicular coarse links at a common site lie in exactly one coarse plaquette. So Q = P.

6. A plaquette through e_0 holds a line link, so it is a quarter by item 2. Its line links meet at a coarse site, and that site is 2x′, since m_ℓ is not coarse. So it is the quarter at the corner 2x′ of a filling F_Q, and Q contains ℓ by item 5. Each of the 6 coarse plaquettes that contain ℓ has exactly one quarter at 2x′. So the 6 plaquettes through e_0 are these 6 quarters. Two of them share e_0, so by item 1 they share no other link, and their 12 off links are distinct. The quarter of F_Q at 2x′ holds the internal links from the center s_Q to the midpoints of the two sides of Q at 2x′, and one of these midpoints is m_ℓ. So each of the 6 quarters has exactly one off link at m_ℓ, the link from m_ℓ to s_Q. The 6 centers are s_Q = m_ℓ ± e_ν with ν ≠ μ, so these are the 6 off links at m_ℓ; the other 2 links at m_ℓ are e_0 and e_1. For position 1, the quarters at the corner 2x′ + 2e_μ of the same 6 fillings hold the same links from m_ℓ to s_Q.

7. Each off link of p lies in 5 other plaquettes. By item 1 distinct off links of p give distinct neighbors. So a plaquette with k off links has 5k neighbors: 10 for a quarter and 20 otherwise. ∎

The scratch check `G0-a-checks.py` reads items 1 to 7 on fine (ℤ/8)⁴, with 1536 fillings. It is a check, not the proof.

### 3.2 The polymer form of the Wilson measure

Haar measure on SU(2), restricted to class functions: write the eigenvalues of g as e^{±iφ}, φ ∈ [0, π]. The law of φ has density (2/π) sin²φ (Weyl's integration formula, REPORTED, standard). Then a(g) = cos φ and χ_j(g) = sin((2j + 1)φ)/sin φ.

**Lemma 3.2 (the plaquette weight).** Let β ≥ 0, c_0(β) := ∫ e^{βa(g)} dg and K := e^{βa}/c_0(β) − 1.

1. c_0(β) = Σ_{m≥0} (β/2)^{2m}/(m!(m + 1)!).
2. K is a real class function, K(g⁻¹) = K(g), and ∫ K dg = 0.
3. K = Σ_{n≥2} n t_n(β) χ_{(n−1)/2}, uniformly on SU(2), with t_n = I_n(β)/I_1(β). In particular ∫ K χ½ dg = 2t_2(β).
4. ε_6(β)⁶ := ∫ K⁶ dg = Σ_{k=0}^{6} C(6, k)(−1)^{6−k} c_0(kβ)/c_0(β)^k, with c_0(0) = 1.

*Proof.* 1. The map g → −g preserves Haar measure and sends a to −a, so the odd moments of a vanish. The even moments are E[a^{2m}] = 2^{−2m}E[χ½^{2m}] = 2^{−2m}(2m)!/(m!(m + 1)!), since E[χ½^{2m}] is the Catalan number, the number of closed walks of length 2m from 0 on the McKay graph of SU(2) (YM4-03C §6, the fold through McKay powers, and §10, where N_m(0) are the Catalan numbers). Summing β^{2m}E[a^{2m}]/(2m)! gives the series. The series converges absolutely, so summation and integration commute.

2. e^{βa} is a positive real class function and a(g⁻¹) = a(g). ∫ K dg = c_0/c_0 − 1 = 0.

3. Put n = 2j + 1. Then ∫ e^{βa}χ_j dg = (2/π)∫_0^π e^{β cos φ} sin(nφ) sin φ dφ. Since sin φ e^{β cos φ} = −β⁻¹ (d/dφ) e^{β cos φ}, integration by parts gives (2n/(πβ)) ∫_0^π e^{β cos φ} cos(nφ) dφ = 2nI_n(β)/β, by I_n(β) = π⁻¹∫_0^π e^{β cos φ} cos(nφ) dφ (REPORTED: Abramowitz and Stegun 1964, formula 9.6.19). At n = 1 this is 2I_1(β)/β, which is the series of item 1 by the power series of I_1 (Abramowitz and Stegun 1964, formula 9.6.10). Dividing by c_0 = 2I_1/β gives the coefficient n t_n of χ_{(n−1)/2} in K, and the coefficient at n = 1 is 0 by item 2. Uniform convergence: I_n(β) ≤ (β/2)ⁿe^{β²/4}/n! by the same power series, I_1(β) ≥ β/2 and |χ_{(n−1)/2}| ≤ n, so Σ_n n t_n · n < ∞. The characters are complete among class functions in L², and both K and the uniform limit are continuous, so the series equals K everywhere.

4. Expand (e^{βa}/c_0 − 1)⁶ by the binomial theorem and use ∫ e^{kβa} dg = c_0(kβ). ∎

**Lemma 3.3 (the polymer representation, YM4-03C §6, "The polymer form").** In the line gauge, with the lines of every coarse link ℓ at (U_0, U_1) = (1, V_ℓ),

```text
rho_1(V) = ( c_0(beta_0)^{N_p} / Z ) Xi(V),     Xi(V) = sum over compatible families {gamma_i} of prod_i z_{gamma_i}(V),
z_gamma(V) = E_V[ prod_{p in gamma} K(U_p) ].
```

Here a polymer is a nonempty set of fine plaquettes that is connected in the graph of Lemma 3.1 item 7. E_V is product Haar measure over the off links with the lines fixed. Two polymers are compatible when they share no off link. The empty family contributes 1. Ξ(V) > 0 for every V.

*Proof.* YM4-03C §2 gives ρ_1(V) = Z⁻¹ ∫ Π_{off links} dU Π_p w(U_p), with every line at (1, V_ℓ). It follows from YM4-03 Theorem 4 and the gauge transformation at m_ℓ by U_0. The weight e^{β_0 a} differs from YM4-03's e^{−β_0(1−a)} by the constant e^{−β_0} per plaquette, which goes into Z. Write e^{β_0 a(U_p)} = c_0(1 + K(U_p)) and expand the product over the sets S of plaquettes. Split S into its connected components. Two components share no off link. So their products are functions of disjoint sets of independent Haar links, the lines being fixed, and E_V factors over the components. Conversely, the components of the union of a compatible family are its members. Compatible polymers share no off link, so no plaquette, since every plaquette has at least 2 off links (Lemma 3.1 item 2). So the sets S correspond one to one to the compatible families. Ξ(V) > 0 because the integrand Π_p e^{β_0 a(U_p)} is positive. ∎

### 3.3 (a) Lemma B makes polymers closed

A set γ of plaquettes is **closed** when every off link of every plaquette of γ lies in at least two plaquettes of γ. off(γ) is the set of off links held by the plaquettes of γ.

**Lemma 3.4 (Lemma B for activities).** If γ is not closed, z_γ(V) = 0 for every V.

*Proof.* Let e be an off link of p ∈ γ that lies in no other plaquette of γ. Fix every other link. p holds each of its links once (Lemma 3.1 item 1), so U_p = A U_e^{±1} B with A and B free of U_e. By Haar invariance and Lemma 3.2 item 2, ∫ K(U_p) dU_e = ∫ K dg = 0. The other factors do not hold U_e. This is the first step of the proof of YM4-03C §6 Lemma B, and of YM4-03 Theorem 9 (a). ∎

From here on a **polymer** is a closed, connected plaquette set. Γ is the finite set of all polymers on Λ_0. γ ≁ γ′ (incompatible) when off(γ) ∩ off(γ′) ≠ ∅. The relation ≁ is reflexive and symmetric. By Lemma 3.4, Ξ(V) is the sum over the compatible families of polymers.

**Lemma 3.5.** For every polymer γ, #off(γ) ≤ 2#γ. So a(γ) = α#off(γ) ≤ 2α#γ.

*Proof.* Each off link of γ lies in at least 2 plaquettes of γ, so 2#off(γ) ≤ Σ_{p∈γ} #off(p) ≤ 4#γ. ∎

**Lemma 3.6 (small polymers).** Every polymer has at least 4 plaquettes. The polymers of exactly 4 plaquettes are the fillings F_Q. So N_w(n) = 0 for n ≤ 3, N_w(4) = 1 if w has class 1, and N_w(4) = 0 if w has class 2 or 3.

*Proof.* Let γ be closed. If γ holds a plaquette that is not a quarter, its 4 off links each lie in another plaquette of γ, and these are 4 distinct plaquettes by Lemma 3.1 item 1. So #γ ≥ 5. Otherwise every plaquette of γ is a quarter. Take p ∈ γ. Each of its two internal links lies in a second plaquette of γ. That plaquette is a quarter holding an internal link of F(p), the filling of p, so it lies in F(p) by Lemma 3.1 items 3 and 4. These are the two neighbors of p in the 4-cycle of F(p). Repeating along the cycle gives F(p) ⊆ γ. So #γ ≥ 4, and #γ = 4 forces γ = F(p). Each filling is closed and connected. A class-1 link lies in exactly one filling and a link of class 2 or 3 in none (Lemma 3.1 item 4). ∎

### 3.4 (b) Finner's inequality with exponent 6

**Theorem 3.7 (Finner 1992, REPORTED).** Let (Ω_e, μ_e), e ∈ E, be finitely many probability spaces and Ω = Π_e Ω_e with the product measure. For j = 1, …, m let S_j ⊆ E, let f_j ≥ 0 be measurable on Ω_{S_j}, and let q_j ∈ [1, ∞] with Σ_{j : e ∈ S_j} 1/q_j ≤ 1 for every e ∈ E. Then ∫ Π_j f_j dμ ≤ Π_j ‖f_j‖_{L^{q_j}(Ω_{S_j})}.

Finner states the inequality with the sum equal to 1. On probability spaces the form with "≤ 1" follows: for each e with slack s_e = 1 − Σ_{j : e ∈ S_j} 1/q_j > 0, add the factor 1 on Ω_{{e}} with exponent 1/s_e, whose norm is 1.

**Lemma 3.8.** For every polymer γ and every V, |z_γ(V)| ≤ ε_6(β_0)^{#γ}.

*Proof.* z_γ(V) = ∫ Π_{p∈γ} K(U_p) Π_{e ∈ off(γ)} dU_e, with the lines fixed. Take E = off(γ), S_p = off(p), f_p = |K(U_p)| as a function of the off links of p, and q_p = 6. The line links of p are fixed parameters. An off link lies in 6 plaquettes of Λ_0 (Lemma 3.1 item 1), so in at most 6 plaquettes of γ, and Σ_{p ∋ e} 1/6 ≤ 1. Theorem 3.7 gives |z_γ(V)| ≤ Π_p ‖K(U_p)‖_6. Integrate one off link of p first: U_p = A U_e^{±1} B, so U_p is Haar distributed whatever the other links are. Hence ‖K(U_p)‖_6⁶ = ∫ |K|⁶ dg = ε_6⁶. ∎

Exponent 6 is the smallest common exponent the hypothesis of Theorem 3.7 allows when a link lies in 6 plaquettes of γ. ‖K‖_q increases with q on a probability space, so 6 is also the best common exponent. The planted fault `finner_exponent_2` of C19 takes q = 2, which breaks the hypothesis at every off link held by 3 or more plaquettes of γ.

### 3.5 (c) Counting: the BFS injection and the Fuss–Catalan tail

Let 𝒯_D be the complete D-ary tree: every vertex has D child slots labeled 1, …, D. Let t_D(n) be the number of subtrees of 𝒯_D with n vertices that contain the root.

**Lemma 3.9 (the BFS injection).** Let G be a graph of maximum degree at most D and v a vertex of G. The number of connected vertex sets A ∋ v with #A = n is at most t_D(n). So for every off link w, the number of connected plaquette sets of n plaquettes that hold w is at most 6t_20(n), and N_w(n) ≤ 6t_20(n).

*Proof.* For each vertex u of G fix an injective labeling λ_u of its neighbors by {1, …, D}. Given A, run breadth-first search in A from v. Process the vertices in queue order. When u is processed, take its neighbors in A not yet discovered, in increasing order of λ_u. Mark them discovered, append them to the queue, and place each neighbor u′ in the child slot λ_u(u′) of the image of u in 𝒯_D. This builds a subtree τ(A) of 𝒯_D with n vertices containing the root, because A is connected and each vertex is discovered once. τ is injective. From τ(A) one rebuilds, by induction on depth, the map from tree vertices to G: the root goes to v, and the child in slot i of the image of u goes to λ_u⁻¹(i). A is the image of that map. For plaquettes take G as the graph of Lemma 3.1 item 7, of maximum degree D = 20. A set holds w if and only if it contains one of the 6 plaquettes through w (Lemma 3.1 item 1). Sum over these 6 roots. Polymers are connected sets, so N_w(n) ≤ 6t_20(n). ∎

**Lemma 3.10 (the Fuss–Catalan count).** t_D(n) = F_D(n) := C(Dn, n)/((D − 1)n + 1) = C(Dn, n − 1)/n.

*Proof.* List the vertices of a subtree in depth-first preorder, children in slot order: v_1 = root, …, v_n. Record for each v_i its set C_i ⊆ {1, …, D} of occupied slots, and k_i = #C_i. After j vertices, the number of discovered vertices not yet listed is 1 + Σ_{i≤j}(k_i − 1). So Σ_{i≤j}(k_i − 1) ≥ 0 for j < n and Σ_{i≤n}(k_i − 1) = −1. Conversely every word (C_1, …, C_n) with these partial sums is the record of exactly one subtree. Let 𝒜 be the set of all words (C_1, …, C_n) with Σ k_i = n − 1, and ℬ ⊆ 𝒜 the valid ones. Cycle lemma: for a word with Σ_{i≤n}(k_i − 1) = −1, exactly one cyclic shift is valid, namely the shift that starts after the first index r ∈ {0, …, n − 1} at which the partial sum P_r = Σ_{i≤r}(k_i − 1) attains its minimum over {0, …, n − 1}. Indeed, a shift starting after r is valid if and only if P_m ≥ P_r for r < m ≤ n − 1 and P_m − 1 ≥ P_r for 0 ≤ m < r, which says that r is the first minimizer. So w ↦ (its valid shift, the shift amount) is a bijection 𝒜 → ℬ × {0, …, n − 1}, and #ℬ = #𝒜/n. #𝒜 = [y^{n−1}] (1 + y)^{Dn} = C(Dn, n − 1), since a word chooses C_i with C(D, k_i) ways for each i. Finally C(Dn, n − 1)/n = (Dn)!/(n!((D − 1)n + 1)!) = C(Dn, n)/((D − 1)n + 1). ∎

The cycle lemma is Dvoretzky and Motzkin (1947); Raney's form and the Fuss–Catalan numbers are in Graham, Knuth and Patashnik (1994), §7.5. These are cross-references (REPORTED); the proof above is complete. F_20(4), …, F_20(12) read 20540, 784245, 31763004, 1340246340, 58281448940, 2593593086150, 117544525178080, 5406686759963586 and 251754316822792420 as exact binomials, the values frozen in C01.

**Lemma 3.11 (the ratio, for all n).** r(n) := F_D(n + 1)/F_D(n) is strictly increasing in n ≥ 0 and tends to μ_D := D^D/(D − 1)^{D−1}. So r(n) < μ_D for every n ≥ 0, and F_D(n + j) ≤ F_D(n) μ_D^j for all n, j ≥ 0. For D = 20, μ = 20²⁰/19¹⁹ ∈ [53.00068, 53.00069].

*Proof.* From F_D(n) = (Dn)!/(n!((D − 1)n + 1)!),

```text
r(n) = prod_{j=1}^{D} (Dn + j)  /  [ (n + 1) * prod_{j=2}^{D} ((D-1)n + j) ].
```

Read n as a real variable n ≥ 0. Then

```text
(d/dn) log r(n) = sum_{j=1}^{D} 1/(n + j/D)  -  [ 1/(n + 1) + sum_{j=2}^{D} 1/(n + j/(D-1)) ].
```

Both sums have D terms. Sort the offsets. The added ones are a_i = i/D, i = 1, …, D. The subtracted ones are b_i = (i + 1)/(D − 1) for i = 1, …, D − 2, then b_{D−1} = 1 and b_D = D/(D − 1). For i ≤ D − 2, a_i = i/D < (i + 1)/(D − 1) = b_i, since (D − 1)i < Di + D. Also a_{D−1} = (D − 1)/D < 1 = b_{D−1} and a_D = 1 < D/(D − 1) = b_D. So 1/(n + a_i) > 1/(n + b_i) for every i and every n ≥ 0, and the derivative is positive. Hence r is strictly increasing on [0, ∞). Dividing numerator and denominator by n^D, r(n) = Π_{j=1}^{D}(D + j/n) / [(1 + 1/n)Π_{j=2}^{D}(D − 1 + j/n)] → D^D/(D − 1)^{D−1} as n → ∞. An increasing sequence lies strictly below its limit. The bracket on μ is the integer inequality 5300068·19¹⁹ ≤ 100000·20²⁰ ≤ 5300069·19¹⁹. ∎

C01 checks the ratio for n ≤ 59 only. Lemma 3.11 holds for every n.

**Corollary 3.12 (the crude count and the tail).** N(n) := 6F_20(n), n ≥ 4, is a valid count vector on every Λ_0 with N even and N ≥ 8. For every n_1 ≥ 4 and 0 ≤ x < 1/μ,

```text
sum_{n >= n_1} 6 F_20(n) x^n  <=  6 F_20(n_1) x^{n_1} / (1 - mu x).
```

So for every valid head N(4), …, N(10), the frozen S(x) = Σ_{n=4}^{10} N(n)xⁿ + Σ_{n=11}^{48} 6F_20(n)xⁿ + 6F_20(49)x⁴⁹/(1 − μx) bounds Σ_{n≥4} N_w(n)xⁿ from above for every off link w, whenever μx < 1.

*Proof.* Lemmas 3.9 and 3.10 give validity. Lemma 3.11 gives F_20(n_1 + j)x^{n_1+j} ≤ F_20(n_1)x^{n_1}(μx)^j; sum the geometric series. ∎

### 3.6 (d) Kotecký–Preiss with a(γ), d(γ) and the test set

**Clusters.** A cluster X is a finite nonempty multiset of polymers, with multiplicities m_X(γ), whose incompatibility graph is connected. That graph has one vertex per element of X, counted with multiplicity, and an edge between two vertices whose polymers are incompatible. Two copies of one polymer are incompatible, since ≁ is reflexive. The Ursell coefficient is

```text
phi(X) = ( 1 / prod_gamma m_X(gamma)! ) * sum over connected spanning subgraphs G of the incompatibility graph of (-1)^{#edges(G)},
Phi(X; z) = phi(X) * prod_gamma z(gamma)^{m_X(gamma)}.
```

n(X) := Σ_γ m_X(γ)#γ is the number of plaquettes of X with multiplicity, and d(X) := Σ_γ m_X(γ)d(γ) = θ·n(X). X ∋ γ means m_X(γ) ≥ 1. X ≁ γ means some polymer of X is incompatible with γ.

**Theorem 3.13 (Kotecký and Preiss 1986, REPORTED).** Let Γ be a finite set with a reflexive, symmetric relation ≁. Let z: Γ → ℂ, a: Γ → (0, ∞) and d: Γ → [0, ∞). Suppose that for every γ ∈ Γ

```text
(KP)   sum_{gamma' ~/~ gamma} |z(gamma')| e^{a(gamma') + d(gamma')}  <=  a(gamma).
```

Then Ξ(z) := Σ over compatible families of Π z ≠ 0, Σ_X |Φ(X; z)| < ∞, log Ξ(z) = Σ_X Φ(X; z), and for every γ ∈ Γ

```text
sum_{X ~/~ gamma} |Phi(X; z)| e^{d(X)}  <=  a(gamma).
```

Kotecký and Preiss state it for countable Γ. A finite Γ is a special case. If z is real and (KP) holds, then (KP) holds for tz, t ∈ [0, 1], so Ξ(tz) is real, continuous in t and never 0, with Ξ(0) = 1. So Ξ(z) > 0 and the series is its real logarithm.

**Corollary 3.14 (marked sets, and the per-polymer corollary).** Assume (KP). For every Γ_0 ⊆ Γ,

```text
sum_{X : X contains a polymer of Gamma_0} |Phi(X; z)| e^{d(X)}  <=  sum_{gamma in Gamma_0} |z(gamma)| e^{a(gamma) + d(gamma)}.
```

With Γ_0 = {γ} this is the per-polymer corollary, Σ_{X ∋ γ} |Φ(X; z)| e^{d(X)} ≤ |z(γ)| e^{a(γ) + d(γ)}.

*Proof.* Let η > 0. Add to Γ a marker γ̂ with z(γ̂) = 0, d(γ̂) = 0 and a(γ̂) = Σ_{γ∈Γ_0}|z(γ)|e^{a(γ)+d(γ)} + η. Let γ̂ be incompatible with itself and with exactly the polymers of Γ_0. (KP) holds at γ̂: its left side is Σ_{γ∈Γ_0}|z(γ)|e^{a(γ)+d(γ)} + 0 < a(γ̂). (KP) still holds at every γ ∈ Γ: the left side gains at most the term of γ̂, which is 0. A cluster of the enlarged set that contains γ̂ has Φ = 0. The other clusters are the clusters of Γ, with the same Φ. Theorem 3.13 at γ̂ bounds the sum over the clusters of Γ that contain a polymer incompatible with γ̂, that is a polymer of Γ_0, by a(γ̂). Let η → 0. ∎

**Lemma 3.15 (the KP condition from the certificate).** Let N be a valid count vector. Put ζ(γ) := ε^{#γ}, a(γ) = α#off(γ), d(γ) = θ#γ and x := εe^{2α+θ}. For every y ≥ 0 and every off link w,

```text
(3.1)   sum_{gamma : w in off(gamma)} y^{#gamma}  =  sum_{n >= 4} N_w(n) y^n  <=  S(y),
(3.2)   sum_{gamma : w in off(gamma)} zeta(gamma) e^{a(gamma) + d(gamma)}  <=  S(x).
```

If S(x) ≤ α, then (KP) holds for ζ, and for z(V) = (z_γ(V))_γ at every V.

*Proof.* (3.1) groups the polymers by size and uses Lemma 3.6 (no polymer below 4 plaquettes). By Lemma 3.5, ζ(γ)e^{a(γ)+d(γ)} ≤ (εe^{2α+θ})^{#γ}, which gives (3.2). For (KP) at γ: every γ′ ≁ γ holds some w ∈ off(γ). So the left side of (KP) is at most Σ_{w∈off(γ)} S(x) ≤ α#off(γ) = a(γ). a(γ) ≥ 2α > 0 because every plaquette has at least 2 off links. By Lemma 3.8, |z_γ(V)| ≤ ζ(γ), so (KP) holds for z(V) too. ∎

**Lemma 3.16 (the test set at the midpoint).** Let ℓ be a coarse link and Γ_ℓ the set of polymers that hold both positions of ℓ. Every γ ∈ Γ_ℓ has off(γ) ∩ W′(ℓ) ≠ ∅. Hence, for every f ≥ 0 on polymers,

```text
sum_{gamma in Gamma_l} f(gamma)  <=  sum_{w in W'(l)} sum_{gamma : w in off(gamma)} f(gamma),   a sum over #W'(l) = 6 links.
```

*Proof.* γ holds position 0 of ℓ, so it contains one of the 6 plaquettes through e_0. By Lemma 3.1 item 6 that plaquette has an off link in W′(ℓ), and that link lies in off(γ). ∎

The draft's test set W(e_0) also works, with 12 terms. It counts each γ ∈ Γ_ℓ at least twice, through both off links of its quarter at e_0. Six is the least number for this argument: the 6 plaquettes through e_0 have pairwise disjoint pairs of off links, so a set of off links that meets each of them has at least 6 elements.

### 3.7 (e) Assembling R_1(Y)

For a polymer γ let Y″(γ) be the set of coarse links both of whose positions γ holds. For a cluster X let Y(X) := ∪_{γ ∈ X} Y″(γ). Put Φ(X; V) := Φ(X; z(V)).

**Lemma 3.17 (what the activities depend on).** z_γ(V) depends on V only through V restricted to Y″(γ), and it is real and coarse-gauge invariant. So Φ(X; V) depends on V only through V restricted to Y(X), and it is real and coarse-gauge invariant.

*Proof.* Dependence: YM4-03C §2 Lemma A applies to z_γ, an integral over the off links of a product of class functions of plaquettes, with the lines at (1, V). If γ holds no position 0 of ℓ, z_γ is constant in V_ℓ. If γ holds no position 1 of ℓ, z_γ does not hold V_ℓ. A function that is constant in each V_ℓ with ℓ ∉ Y″(γ) separately, the others held fixed, is a function of V restricted to Y″(γ).

Reality: K is real (Lemma 3.2 item 2), so z_γ and Φ are real.

Invariance: let g: Λ_1 → SU(2). Define g̃ on Λ_0 by g̃(2x′) = g(x′) at coarse sites, g̃(m_ℓ) = g(x′) at the midpoint of each ℓ = (x′, μ), and g̃ = 1 elsewhere. Under U ↦ U^{g̃}, position 0 of ℓ goes from 1 to g(x′)·1·g(x′)⁻¹ = 1, and position 1 goes from V_ℓ to g(x′)V_ℓ g(x′ + e_μ)⁻¹ = V^g_ℓ. So U ↦ U^{g̃} maps the fiber with lines at (1, V) onto the fiber with lines at (1, V^g). On off links it acts by left and right multiplications, which preserve product Haar measure. It conjugates every U_p ([LEMMA-0001](LEMMA-0001-GAUGE-INVARIANCE.md)), so K(U_p) is unchanged. Hence z_γ(V^g) = z_γ(V). This is the extension of YM4-03 Theorem 4 item 3, adapted to the line gauge. ∎

**Lemma 3.18.** #Y″(γ) ≤ #γ for every polymer γ. Hence #Y(X) ≤ n(X) for every cluster X.

*Proof.* A plaquette holds at most 2 line links (Lemma 3.1 item 2). The coarse links of Y″(γ) carry 2#Y″(γ) distinct line links, all held by γ. So 2#Y″(γ) ≤ 2#γ. Then #Y(X) ≤ Σ_{γ∈X} #Y″(γ) ≤ n(X). ∎

**Lemma 3.19 (forests, and loops of length at least 4).** If Y(X) contains no closed coarse loop, Φ(X; V) is constant in V. Every set of coarse links that contains a closed loop has at least 4 elements.

*Proof.* Let Y be a forest. In each tree of Y choose a root, and gauge every link of the tree to 1 along the tree paths from the root. A coarse-gauge-invariant function of V restricted to Y therefore equals its value at V = 1 on Y. The coarse torus (ℤ/L)⁴ with L = N/2 ≥ 4 is a simple graph, since L ≥ 3, and bipartite, since L is even. So every cycle has length at least 4. ∎

**Proposition 3.20 (the H_1 form, conclusion (C1)).** Assume (H1) to (H4). For every V,

```text
log rho_1(V) = const_1 + sum_Y R_1(Y; V),        R_1(Y; V) := sum_{X : Y(X) = Y} Phi(X; V),
const_1 = log( c_0^{N_p} / Z ) + sum_{X : Y(X) holds no closed loop} Phi(X; V),
```

with Y over the sets of coarse links that hold a closed loop. const_1 does not depend on V. Each R_1(Y; ·) is real, coarse-gauge invariant and a function of V restricted to Y, and #Y ≥ 4. R_1(∂P) holds the cluster {F_P}, so the coarse Wilson term lies inside R_1(∂P).

*Proof.* Lemma 3.3 gives log ρ_1 = log(c_0^{N_p}/Z) + log Ξ(V). Lemma 3.15 gives (KP) at every V. Theorem 3.13 gives log Ξ(V) = Σ_X Φ(X; V), absolutely convergent and real. Absolute convergence allows the regrouping by Y(X). Lemmas 3.17 to 3.19 give the properties. Y″(F_P) = ∂P, so {F_P} lies in R_1(∂P). ∎

### 3.8 (f) δ_1 and the readout

Write Φ̄(X) := |φ(X)| Π_γ ζ(γ)^{m_X(γ)}. By Lemma 3.8, sup_V |Φ(X; V)| ≤ Φ̄(X), and Φ̄(X) = |Φ(X; ζ)|, so Theorem 3.13 and Corollary 3.14 apply to Φ̄ with ζ.

**Proof of (C2).** Fix a coarse link ℓ. Each cluster enters at most one R_1(Y), so

```text
sum_{Y containing l} e^{kappa #Y} sup_V |R_1(Y;V)|  <=  sum_{X : l in Y(X)} e^{kappa #Y(X)} PhiBar(X)  <=  sum_{X : l in Y(X)} e^{kappa n(X)} PhiBar(X),
```

by Lemma 3.18 and κ > 0. If ℓ ∈ Y(X), X contains a polymer γ_0 ∈ Γ_ℓ. So the right side is at most Σ_{γ_0 ∈ Γ_ℓ} Σ_{X ∋ γ_0} e^{κ n(X)} Φ̄(X). For X ∋ γ_0 we have n(X) ≥ #γ_0, and θ ≥ κ, so e^{κ n(X)} = e^{d(X)} e^{−(θ−κ) n(X)} ≤ e^{d(X)} e^{−(θ−κ)#γ_0}. Corollary 3.14 with Γ_0 = {γ_0} and Lemma 3.5 give

```text
sum_{X containing gamma_0} e^{kappa n(X)} PhiBar(X)  <=  e^{-(theta-kappa) #gamma_0} zeta(gamma_0) e^{a(gamma_0) + d(gamma_0)}  <=  (eps e^{2 alpha + kappa})^{#gamma_0}.
```

Lemma 3.16 and (3.1) at y = εe^{2α+κ} give Σ_{γ_0 ∈ Γ_ℓ} y^{#γ_0} ≤ 6S(εe^{2α+κ}). Take the supremum over ℓ. Finally N(n) = 0 for n < 4 and e^{−n(θ−κ)} ≤ e^{−4(θ−κ)} for n ≥ 4, so S(εe^{2α+κ}) ≤ e^{−4(θ−κ)} S(εe^{2α+θ}) ≤ e^{−4(θ−κ)} α. ∎

**Lemma 3.21 (the filling).** z_{F_P}(V) = Σ_{n≥2} n t_n(β_0)⁴ χ_{(n−1)/2}(V_P). Its χ½(V_P) coefficient is 2t_2(β_0)⁴.

*Proof.* Expand each of the 4 factors K(U_p) by Lemma 3.2 item 3, and integrate term by term, which uniform convergence allows. Orient the 4 quarters the same way in the plane of P, so each internal link appears once in each of its two quarters, with opposite orientations. Integrate three internal links with ∫ χ_j(Ax) χ_{j′}(x⁻¹B) dx = δ_{jj′} χ_j(AB)/(2j + 1) (Schur orthogonality, as in YM4-03C §7.5 and YM4-03 Theorem 9). The fourth internal link then appears as x x⁻¹ next to the center and drops out. All four spins are equal, and the term with χ_{(n−1)/2} carries (n t_n)⁴/n³ = n t_n⁴. The remaining word runs along the 8 line links of ∂P. In the line gauge it is V_P, by YM4-03 Proposition 2. ∎

**Lemma 3.22 (the readout exclusion, for polymers).** Let P be a coarse plaquette and γ a polymer that holds all 8 line links of ∂P. If γ ≠ F_P, then #γ ≥ 8.

*Proof.* Let k = #(γ ∩ F_P), let n_q be the number of quarters in γ and n_r = #γ − n_q. Only quarters hold line links (Lemma 3.1 item 2). A quarter of F_P holds 2 line links of ∂P, and any other quarter at most 1 (Lemma 3.1 item 5). So 2k + (n_q − k) ≥ 8, that is n_q ≥ 8 − k.

Case k = 0. Then #γ ≥ n_q ≥ 8.

Case 1 ≤ k ≤ 3. γ ∩ F_P is a nonempty proper subset of the 4-cycle of quarters of F_P (Lemma 3.1 item 3). So some f ∈ γ ∩ F_P has a cycle neighbor f′ ∉ γ. Their common internal link e lies in no other quarter of F_P, so in exactly one plaquette of γ ∩ F_P. γ is closed, so some q ∈ γ, q ≠ f, holds e. The only quarters through e are f and f′ (Lemma 3.1 item 4), so q is not a quarter and #T(q) = 1. By Lemma 3.1 item 2, q has two off links g_1, g_2 of class 2. Closedness gives q_1 ∋ g_1 and q_2 ∋ g_2 in γ, both different from q. q_1 ≠ q_2, since otherwise q_1 shares two links with q (Lemma 3.1 item 1). q_1 and q_2 are not quarters, since links of class 2 lie in no quarter (Lemma 3.1 item 4). So n_r ≥ 3 and #γ ≥ (8 − k) + 3 ≥ 8.

Case k = 4. Then F_P ⊆ γ and γ ≠ F_P. γ is connected, so some q ∈ γ ∖ F_P shares an off link e with a quarter of F_P. The off links of the quarters of F_P are its internal links, so e is one of them, and q is not a quarter (Lemma 3.1 item 4). The quarters of F_P hold only the line links of ∂P and the internal links of F_P. A plaquette that is not a quarter of F_P holds at most one internal link of F_P: two internal links are either perpendicular at the center, and then lie together only in a quarter of F_P, or opposite, and then lie together in no plaquette. So the other three links of q, all off links, are links of no quarter of F_P. Closedness gives three plaquettes of γ that hold them. They are distinct from q and from each other (Lemma 3.1 item 1), and they lie outside F_P. So #(γ ∖ F_P) ≥ 4 and #γ ≥ 8. ∎

**Corollary 3.23 (the readout exclusion, for clusters).** Let {F_P} denote the cluster with m(F_P) = 1 and nothing else. Every cluster X ≠ {F_P} with ∂P ⊆ Y(X) has n(X) ≥ 8.

*Proof.* If X has 2 or more elements counted with multiplicity, n(X) ≥ 4 + 4 by Lemma 3.6. Otherwise X = {γ} and Y″(γ) ⊇ ∂P, so γ holds all 8 line links of ∂P, γ ≠ F_P, and Lemma 3.22 applies. ∎

This is the form the critic asked for: any cluster other than {F_P} that holds ∂P at both positions has at least 8 plaquettes. The multi-polymer clusters include the self-cluster {F_P, F_P}, with n = 8. The scratch enumeration of section 3.14 reads the closed connected sets of at most 8 plaquettes that hold all of ∂P on fine (ℤ/8)⁴: 1 at size 4, which is F_P, none at sizes 5, 6 and 7, and 16 at size 8, the same number as the 16 one-cube bumps of YM4-03C §7.5. That is a check of Lemma 3.22, not its proof. C09's clause "no polymer of 5, 6 or 7 plaquettes holds all of ∂P at both positions" is right for closed polymers. It is false for unclosed connected sets: F_P together with one plaquette through an internal link of F_P has 5 plaquettes and holds all of ∂P. Unclosed sets have activity 0 (Lemma 3.4), so C09's restriction to V-dependent polymers is the needed one.

**Proof of (C3).** The readout is c_½(P) := ∫ χ½(V_P) log ρ_1(V) dV in coarse Haar measure, as in YM4-03C §4, where ⟨χ½(V_P), χ½(V_P)⟩ = 1. V_P holds each of the 4 coarse links of ∂P once, so it is Haar distributed. Hence ∫ χ½(V_P) dV = 0, and const_1 contributes 0. If some ℓ ∈ ∂P lies outside Y(X), integrate V_ℓ first: Φ(X; V) does not hold V_ℓ (Lemma 3.17), and ∫ χ½(V_P) dV_ℓ = 0. Absolute and uniform convergence gives c_½(P) = Σ_{X : ∂P ⊆ Y(X)} ∫ χ½(V_P) Φ(X; V) dV. The cluster {F_P} gives exactly 2t_2⁴, by Lemma 3.21 and the orthonormality of the characters of V_P. Every other term obeys |∫ χ½(V_P) Φ(X; V) dV| ≤ E|χ½| Φ̄(X), with

```text
E|chi_1/2| = (2/pi) int_0^pi |2 cos phi| sin^2 phi dphi = (8/pi) int_0^{pi/2} cos phi sin^2 phi dphi = 8/(3 pi).
```

By Corollary 3.23 each such X has n(X) ≥ 8, so 1 ≤ e^{d(X) − 8θ}. Fix ℓ ∈ ∂P. Each such X holds a polymer of Γ_ℓ. Corollary 3.14 with Γ_0 = Γ_ℓ, then Lemma 3.16 and (3.2), give

```text
| c_1/2(P) - 2 t_2^4 |  <=  (8/(3 pi)) e^{-8 theta} sum_{X : X holds a polymer of Gamma_l} e^{d(X)} PhiBar(X)
                       <=  (8/(3 pi)) e^{-8 theta} * 6 S(eps e^{2 alpha + theta})  <=  (8/(3 pi)) * 6 alpha e^{-8 theta}.
```

Finally 8/(3π) < 8489/10000. Machin's formula with alternating partial sums gives π ≥ 16(1/5 − 1/375 + 1/15625 − 1/546875) − 4/239 > 333/106, and 8·106/(3·333) = 848/999 < 8489/10000. ∎

### 3.9 Uniformity, conclusion (C4)

The constants in (C2) and (C3) are built from ε_6(β_0), t_2(β_0), α, θ, κ, the count vector N(n), #W′(ℓ) = 6, the degree 20, μ and 8/(3π). None of them involves N, K or N_p. Every lemma above holds on every Λ_0 with N even and N ≥ 8. Lemma 3.1 uses fine side at least 3 and coarse side at least 3. Lemma 3.19 uses coarse side at least 4. Lemma 3.9 uses only the degree bound 20. Polymers may wrap around the torus. The crude counts 6F_20(n) bound them on every such torus, so the crude certificate is lattice independent. The refined head is lattice independent only through C03's locality claim, which is part of the CONJECTURE C03 and is read by C17. The hypothesis N = 2^K L_K with L_K ≥ 4 and K ≥ 1 gives N ≥ 8. Compare YM4-04A §2 ([NOTE-YM4-04-TWO-TERNARY-BLOCKS-20261107.md](NOTE-YM4-04-TWO-TERNARY-BLOCKS-20261107.md)), whose global Cauchy remainder needs β ≤ 1/(8N_p), and YM4-04B §1 ([NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md](NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md)), whose local Dobrushin bound controls correlations but not the effective action. YM4-03C §12 names the local bound as OPEN; Theorem G0 supplies it for step 0 at strong coupling, under (H4).

### 3.10 Remarks on the certificate

1. **θ = κ is optimal for (C2).** δ_1 = 6S(εe^{2α+κ}) increases with α. The set of α that meet S(εe^{2α+θ}) ≤ α shrinks as θ grows, since S is increasing. So the least admissible α, and the best δ_1, are at θ = κ. Existence of a certified pair is also decided at θ = κ. DERIVED.
2. **The frozen formula is also optimal at θ = κ, at exact least roots.** Let α(θ) be the least root of S(εe^{2α+θ}) = α, x = εe^{2α(θ)+θ} and u = xS′(x). At a root where g = S(εe^{2α+θ}) − α crosses from positive to negative, 1 − 2u > 0. Implicit differentiation gives dα/dθ = u/(1 − 2u). S holds only powers n ≥ 4, so u ≥ 4S(x) = 4α. Hence (d/dθ) log(α e^{−4θ}) = u/(α(1 − 2u)) − 4 > 0, and α(θ)e^{−4(θ−κ)} is least at θ = κ. On the rational grid this holds up to the search tolerance. DERIVED at exact roots. This proves outline item 5's claim that every δ_1 optimum sits at θ = 1/4.
3. **g is convex.** g(α) = S(εe^{2α+θ}) − α. Each term N(n)εⁿe^{nθ}e^{2nα} is convex in α. The tail 6F_20(49)x⁴⁹/(1 − μx) = Σ_{j≥0} 6F_20(49)μ^j x^{49+j} is a convergent sum of convex exponentials in α for μx < 1. DERIVED. The frozen search reads the exact inequality at the α it returns, which is sound whatever the search does.
4. **The cap α ≤ 1/4 in the frozen C_0 is not needed.** Theorem G0 needs only α > 0. The cap can only turn a MET into NOT_MET, never the reverse, so it is safe.
5. **The head-free vector is not a count vector.** N(n) = 0 for n ≤ 10 is below N_w(4) = 1 for class-1 links (Lemma 3.6). It is valid only as a lower limit: S_N ≥ S_head-free pointwise for every valid N, so the least root, and both the frozen and the proved δ_1, are at least their head-free values. The draft uses it only that way.

### 3.11 What the proved constants change in the frozen rows

Every number below comes from `G0-a-kp.py` (section 3.14) at θ = κ, the proved optimum. The MET side of each read is an exact upward-rounded certificate. A read marked "not certified" is a search read without lower enclosures, not a proof of NOT_MET. The self-map reads use G1's frozen c(δ) and δ_crit⁻ = 0.0496174 (C13) as given; G1 is not proved here. The frozen arithmetic reproduces in every case checked.

| Coupling and head | frozen 12α | proved 6S(εe^{2α+κ}) | 2δ′ with the proved δ_1 | C_1 (2δ′ ≤ 1/8) |
|---|---|---|---|---|
| 1/100, crude (α = 9.2037089e-4) | 0.0110444507 | 0.00552222534 | 0.011106 | MET |
| 1/100, C03 head | 9.43197e-6 | 4.71599e-6 | 9.4e-6 | MET |
| 1/100, head-free (lower limit) | 9.37230e-6 | 4.68615e-6 | 9.4e-6 | (limit) |
| 1/64, crude | 0.101653 | 0.0508265 | 0.106953 | MET, but δ_1 > δ_crit⁺ = 0.0496175, so the self-map stays NOT_MET |
| 1/64, C03 head | 2.03477e-3 | 1.01739e-3 | 0.002037 | MET |
| 1/50, head-free (lower limit) | 0.0726458 | 0.0363229 | 0.075333 | (limit) |
| 1/50, C03 head | 0.0726471 | 0.0363235 | 0.075334 | MET, and δ_1 < δ_crit⁻, so the self-map is MET |

- **Self-map edges** with the proved δ_1 and G1 as frozen: crude, certified at 0.01556 and not certified at 0.01557, against the frozen 0.01369/0.01370 (C13); C03 head and head-free, certified at 0.02029 and not certified at 0.02030, against the frozen 0.01959/0.01960 (C14). The order β_ind < β_stop ≈ 0.02075 < β_wall ≈ 0.02247 survives.
- **C12.** The frozen DERIVED NOT_MET of C_1 at 1/50 "under every count vector" rests on the head-free value 0.072645 of the frozen formula. With the proved constant the head-free limit is 0.0363229, and 2δ′ = 0.0753 < 1/8. With the C03 head both C_1 and the self-map read MET at 1/50, conditional on C03 and G1. So that NOT_MET is a property of the factor 12, not of the method. C_0 crude NOT_MET at 1/50 does not change, since the KP condition does not involve the test set.
- **C11.** At 1/64 crude, C_1 reads MET with the proved constant (2δ′ = 0.106953 ≤ 1/8). The self-map stays NOT_MET.
- **C09.** The proved T is exactly half of the frozen T at the same minimizing grid index. T/P_10 reads 5.2259e-4 (1/4000, i = 194), 8.3611e-3 (1/2000, i = 150), 0.13383 (1/1000, i = 105), 0.55725 (1/700, i = 83), 1.0323 (1/600, i = 73) and 6.9352e3 (1/100, i = 0). The frozen values reproduce: 1.0452e-3, 1.6722e-2, 0.26765, 1.1145, 2.0645 and 1.3870e4. So the leading coefficient is resolved to 0.05 percent at 1/4000 and is lost between 1/700 and 1/600, not between 1/1000 and 1/700.
- **C08.** δ_1/(12e·c_½(1/100)) is about 1.85e3 with the proved constant, against the frozen [3.6e3, 3.8e3]. The crude/refined ratio 1170.96 does not change. c_½(1/100) is the MEASURED series P_10, not a certified value: T/P_10 reads 6.9e3 there.
- **C07 and C16.** With the proved δ_1, every G1 output bound shrinks, since c is increasing in δ and H_1(κ, δ) is monotone in δ. The frozen values stay valid upper bounds. δ_20 ≤ c(δ_1)^{19}δ_1 is at most half of the frozen [2.30e-9, 2.31e-9], and the oscillation bound at most half of 4.35e-7.
- **The regime.** The text "β_0 ≤ 0.0196" (HYPOTHESIS, C17, L04, note section 1) would read β_0 ≤ 0.02029 with the proved constant, conditional on C03 and G1.

The frozen rows predict reads of the frozen certificate, with the factor 12. An engine that implements them as frozen should read them as frozen. Whether to re-freeze with 6 is the owner's decision.

### 3.12 The constants and formulas of G0: frozen against proved

"Equal" means exactly the same constant or formula. A frozen constant that the proof improves is marked not equal, with the direction.

| Row | Frozen in the draft | Proved here | Equal? |
|---|---|---|---|
| HYPOTHESIS | H_0: w = e^{β_0 a} = Π_p c_0(β_0)(1 + K_p) | Lemmas 3.2, 3.3 | yes |
| HYPOTHESIS | K = Σ_{n≥2} n t_n χ_{(n−1)/2}, t_n = I_n/I_1 | Lemma 3.2 item 3 | yes |
| HYPOTHESIS | c_0(x) = Σ_m (x/2)^{2m}/(m!(m+1)!) | Lemma 3.2 item 1 (= ∫e^{xa} = 2I_1(x)/x) | yes |
| HYPOTHESIS | H_k form: Y with #Y ≥ 4 holding a closed loop; R_k(Y) real, coarse-gauge invariant, local | Proposition 3.20 at k = 1 | yes |
| HYPOTHESIS | norm_κ(R) = sup_l Σ_{Y∋l} e^{κ#Y} sup_V \|R(Y;V)\| | used as frozen | yes |
| HYPOTHESIS | coarse Wilson term carried inside R_k(∂P) | {F_P} ⊂ R_1(∂P), Proposition 3.20 | yes |
| HYPOTHESIS | κ = 1/4 | used; the proof needs only 0 < κ ≤ θ | yes |
| HYPOTHESIS | D = 20 | Lemma 3.1 item 7 (maximum 20, minimum 10) | yes |
| HYPOTHESIS | 6 plaquettes per link, Finner exponent 6 | Lemma 3.1 item 1, Lemma 3.8 | yes |
| HYPOTHESIS | #W(e_0) = 12 | true as geometry (Lemma 3.1 item 6) | yes, as geometry |
| HYPOTHESIS, THEOREMS | test set W(e_0), 12 links, entering δ_1 and T | W′(ℓ), the 6 off links at the midpoint, suffices (Lemma 3.16); 6 is least for this argument | no: frozen 12 is weaker by a factor 2, valid |
| HYPOTHESIS | F_20(n) = C(20n, n)/(19n + 1) | Lemma 3.10; values n = 4..12 reproduce | yes |
| HYPOTHESIS | μ = 20²⁰/19¹⁹, in [53.00068, 53.00069] | Lemma 3.11 | yes |
| HYPOTHESIS, C01 | F_20(n+1)/F_20(n) increasing and below μ, checked for n ≤ 59 | proved for every n ≥ 0 (Lemma 3.11) | no: the proof is stronger (all n) |
| HYPOTHESIS | E\|χ½\| = 8/(3π) ≤ 8489/10000 | proof of (C3); π > 333/106 | yes |
| HYPOTHESIS | n_max = 10 | G0 holds for any head length | yes (a certificate choice) |
| HYPOTHESIS | exact counts need fine sides ≥ 8; the tail needs only degree 20 | G0 needs N even, N ≥ 8 (coarse side ≥ 4) throughout; tail needs only degree 20 | yes |
| HYPOTHESIS | uniformity: no bound involves N, K or N_p | (C4), section 3.9 | yes |
| HYPOTHESIS | regime β_0 ≤ 0.0196 (edge 0.01959) | 0.02029 with the proved constant (search read; conditional on C03 and G1) | no: frozen window narrower, conservative |
| HYPOTHESIS | admissible: C_0 MET and δ_1 < δ_crit⁻ | same structure, with the proved δ_1 | no, through δ_1 |
| CERTIFICATES | ε := ε_6(β_0) = ‖K‖_{L⁶(SU(2))} | Lemma 3.8; formula Lemma 3.2 item 4 | yes |
| CERTIFICATES | S(x) = head + Σ_{11}^{48} 6F_20(n)xⁿ + 6F_20(49)x⁴⁹/(1 − μx), μx < 1 | valid upper bound for every valid head (Corollary 3.12) | yes |
| CERTIFICATES | crude N(n) = 6F_20(n) | valid (Lemma 3.9) | yes |
| CERTIFICATES | head-free N(n) = 0 for n ≤ 10 | not a count vector; a lower limit only (remark 3.10.5) | yes, as the draft uses it |
| CERTIFICATES | refined N(n) = C03 counts | N_w(n) = 0 for n ≤ 3, N_1(4) = 1, N_2(4) = N_3(4) = 0 proved (Lemma 3.6); n = 5..10 not proved | yes at n = 4; n = 5..10 CONJECTURE |
| CERTIFICATES | C_0 MET iff, for a grid θ, a rational α has S⁺(ε⁺e^{2α+θ}) ≤ α ≤ 1/4 | sufficient: S(εe^{2α+θ}) ≤ α with α > 0, θ ≥ κ; the cap and the grid are not needed; existence is decided at θ = κ | no: frozen condition is stricter than needed, sound |
| CERTIFICATES | g(α) = S(εe^{2α+θ}) − α convex | remark 3.10.3, tail included | yes |
| CERTIFICATES | δ_1 = min over certified (α, θ) of 12αe^{−4(θ−κ)} | δ_1 = 6S(εe^{2α+κ}) ≤ 6αe^{−4(θ−κ)}, at most half of the frozen value at every certified pair; optimum at θ = κ for both | no: frozen weaker by a factor of at least 2, valid |
| CERTIFICATES | readout T = (8489/10000)·12αe^{−8θ}, minimized | T = (8/(3π))·6e^{−8θ}S(εe^{2α+θ}) ≤ (8489/10000)·6αe^{−8θ}, half | no: frozen weaker by a factor of at least 2, valid |
| THEOREMS | YM4-03C Lemmas A and B | Lemmas 3.4, 3.17 | yes |
| THEOREMS | Finner exponent 6: sup_V \|z_γ\| ≤ ε_6^{#γ} | Lemma 3.8 | yes |
| THEOREMS | a(γ) = α#off(γ) ≤ 2α#γ | Lemma 3.5 | yes |
| THEOREMS | d(γ) = θ#γ | used | yes |
| THEOREMS | BFS injection into the complete 20-ary tree; Fuss–Catalan tail | Lemmas 3.9, 3.10, Corollary 3.12 | yes |
| THEOREMS | #Y″(γ) ≤ #γ | Lemma 3.18 | yes |
| THEOREMS | V-dependence only at size ≥ 4 | Lemmas 3.6, 3.19 | yes |
| THEOREMS | C_0 ⇒ H_1 with δ_1 | Theorem G0, with δ_1 at most half | no: frozen weaker, valid |
| C07 | δ_1 ∈ [0.011044, 0.011045], α ≈ 9.2037e-4, θ = 1/4 | frozen arithmetic reproduces (0.0110444507); proved δ_1 ≤ 0.00552222534 | no: frozen weaker by a factor 2 |
| C07 | 2δ_1e^{δ_1}, c(δ_1), δ_2, Σδ_k | G1 outputs of δ_1; valid upper bounds if G1 holds; 2δ′ = 0.011106 with the proved δ_1 | no: frozen weaker |
| C08 | refined δ_1 ∈ [9.42e-6, 9.45e-6]; head-free [9.372e-6, 9.373e-6] | 4.71599e-6; head-free 4.68615e-6 | no: halved |
| C08 | crude/refined δ_1 ratio in [1170, 1172] | 1170.96 | yes |
| C08 | Wilson-term norm 12e·c_½ | 6 coarse plaquettes per coarse link, sup\|χ½\| = 2 and e^{4κ} = e give 12e\|c_½\| | yes |
| C08 | δ_1/(12e·c_½(1/100)) ∈ [3.6e3, 3.8e3] | about 1.85e3 | no: halved |
| C09 | c_½(P) ∈ 2t_2⁴ ± T | (C3), with T halved | no: frozen weaker, valid |
| C09 | every V-dependent polymer ≠ F_P holding ∂P at both positions has ≥ 8 plaquettes | Lemma 3.22 for every closed polymer; Corollary 3.23 for clusters | yes, now DERIVED, not read off C03 |
| C09 | no polymer of 5, 6 or 7 plaquettes holds all of ∂P at both positions | true for closed polymers; false for unclosed connected sets | yes, read for closed polymers |
| C09 | T/P_10 brackets at 1/4000, 1/2000, 1/1000, 1/700, 1/100 with i = 194, 150, 105, 83, 0 | 5.2259e-4, 8.3611e-3, 0.13383, 0.55725, 6.9352e3, same i | no: halved |
| C09 | resolved to 0.1 percent at 1/4000; lost between 1/1000 and 1/700 | 0.05 percent at 1/4000; lost between 1/700 and 1/600 | no |
| C09 | \|P_10 − 2t_2⁴\| ≈ β⁸/2048 | 1/1536 − 1/6144 = 1/2048 (YM4-03C §10) | yes |
| C10 | fine norm 12\|s\|e^{8κ}, coarse norm 12\|s\|e^{4κ}, ratio e^{−4κ} | follow from the frozen norm (6 coarse plaquettes per coarse link, sup\|χ½\| = 2) | yes; c ≥ e^{−4κ} is G1's claim |
| C10b | input norm 12\|s\|e^{6κ} | follows from the frozen norm | yes; the rest is G1 |
| C11 | δ_1 ∈ [0.10165, 0.10166]; 2δ′ > 1/8, so C_1 NOT_MET | 0.0508265; 2δ′ = 0.106953 ≤ 1/8, so C_1 MET; self-map still NOT_MET | no: the C_1 clause flips |
| C12 | head-free δ_1 ∈ [0.072645, 0.072646], so C_1 and the self-map NOT_MET for every count vector | head-free 0.0363229 (2δ′ = 0.075333); C03 head 0.0363235, C_1 and the self-map MET | no: the NOT_MET clauses do not survive the proved constant |
| C12 | C_0 crude NOT_MET at 1/50 | unchanged | yes |
| C13 | β_ind^crude ∈ [0.01369, 0.01370) | certified at 0.01556, not certified at 0.01557 | no |
| C14 | β_ind ∈ [0.01959, 0.01960); 1/64 refined δ_1 ∈ [2.0347e-3, 2.0348e-3] | certified at 0.02029, not certified at 0.02030; 1/64 refined δ_1 ≤ 1.01739e-3 | no |
| C16 | osc_V log ρ_m ≤ (512/e)δ_m, from Σ_Y sup\|R\| ≤ #links·δ·e^{−4κ}/4 | follows from the frozen norm and #Y ≥ 4 | yes |
| C16 | δ_20 ∈ [2.30e-9, 2.31e-9], osc ≤ 4.35e-7 at 1/100 crude | at most half of each | no: frozen weaker, valid |

all_equal: **false**. No frozen G0 constant is wrong as a bound. The test-set constant 12 and the two outputs built on it, δ_1 and T, are valid but loose by a factor 2. The interpretive NOT_MET clauses of C11 (C_1) and C12, and the edges of C13 and C14, are properties of that factor.

### 3.13 Gaps

1. Theorem 3.13 is REPORTED from Kotecký and Preiss (1986) and not reproved here, as ledger L06 says. I used it in the form stated, with d in the hypothesis, e^{d(X)} in the conclusion, clusters incompatible with γ, and zero activities allowed. The paper's text was not re-read in this session.
2. Theorem 3.7 is REPORTED from Finner (1992). The form with "≤ 1" is obtained here by padding with constant factors.
3. The integral and series representations of I_n are REPORTED from Abramowitz and Stegun (1964), formulas 9.6.19 and 9.6.10, and Weyl's integration formula is used as standard. They enter only through the identification t_n = I_n/I_1 and the uniform convergence of the character series.
4. The refined head, the C03 counts at n = 5 to 10, is a CONJECTURE. G0 with that head is conditional on C03, including C03's claim that the counts do not depend on the lattice at fine side ≥ 8.
5. The numbers of section 3.11 are scratch reads. Their MET sides are certified with upward rounding. Their "not certified" sides are search reads, not proofs of NOT_MET. They use G1's frozen c(δ) and δ_crit⁻, and G1 is not proved here. The bisection assumes that δ_1 increases with β_0, which is not proved. ε_6 was enclosed at 1/100, 1/64, 1/50 and the readout couplings only.
6. Remark 3.10.2 holds at exact least roots. On the rational grid it holds up to the search tolerance.
7. I did not check whether G1's bookkeeping, for C_k and c(δ), carries a similar factor-2 overcount. That is outside G0.
8. Whether rows C11 to C14, the regime text and the admissible window should be re-frozen with the proved constant is not settled here. As frozen, they predict reads of the frozen certificate.

### 3.14 Scratch files (pre-freeze disclosure)

- `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/derive/G0-a-checks.py`: integers and Fractions. Fuss–Catalan values and the ratio for n ≤ 399, the μ bracket, the π bound, Lemma 3.1 items 1 to 7 on fine (ℤ/8)⁴, and the closed sets of at most 8 plaquettes that hold all of ∂P (sizes 4: 1, 8: 16, none at 5 to 7).
- `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/derive/G0-a-kp.py`: Fractions with upward rounding to 160 significant bits. ε_6 enclosures, certified α at θ = κ, the frozen and proved δ_1, the C_1 test, the self-map edges with the proved constant, and the readout ratios on the grid i ≤ 320. Floats appear only in display.

Neither file is an engine, and neither is evidence. The engine and the independent check recompute what they need by their own routes.

### References

- R. Kotecký and D. Preiss, Cluster expansion for abstract polymer models, Comm. Math. Phys. 103 (1986) 491–498. REPORTED.
- H. Finner, A generalization of Hölder's inequality and some probability inequalities, Ann. Probab. 20 (1992) 1893–1901. REPORTED.
- A. Dvoretzky and Th. Motzkin, A problem of arrangements, Duke Math. J. 14 (1947) 305–313. Cycle lemma, cross-reference.
- R. L. Graham, D. E. Knuth and O. Patashnik, Concrete Mathematics, 2nd ed., Addison-Wesley (1994), §7.5. Raney's lemma and Fuss–Catalan numbers, cross-reference.
- M. Abramowitz and I. A. Stegun, Handbook of Mathematical Functions, National Bureau of Standards (1964), formulas 9.6.10 and 9.6.19. REPORTED.
- Repo: NOTE-YM4-03-ONE-SCALE-BLOCKING.md §2 (Theorem 1, Proposition 2, Lemma 3), §3 (Theorem 4), §6 (Theorem 9, Lemma 9a); NOTE-YM4-03C-BLOCKED-ACTION.md §2 (gauge, Lemma A), §4 (readout), §6 (Lemma B, the fold, the polymer form), §7.5 (disk merges, bumps), §10 (Catalan numbers, t_2 series), §12 (OPEN); NOTE-YM4-04-TWO-TERNARY-BLOCKS-20261107.md §2; NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md §1; LEMMA-0001-GAUGE-INVARIANCE.md.
