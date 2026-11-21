## 4. Theorem G1 (step k to k + 1, k ≥ 1), route A

**Status.** DERIVED in this section: Theorem G1 as frozen, Theorem G1* and every lemma below. They rest on [YM4-03](NOTE-YM4-03-ONE-SCALE-BLOCKING.md) (Lemma 3, Theorem 4, Proposition 2), on [YM4-03C](NOTE-YM4-03C-BLOCKED-ACTION.md) §2 (the line gauge and Lemma A), on section 3 of this note (Lemma 3.1, the b = 2 geometry; Lemma 3.19, forests; Corollary 3.14, the marker argument; §3.8, the bound 8/(3π) < 8489/10000), and on one REPORTED theorem, Kotecký and Preiss (1986), restated as Theorem 4.9. No engine ran. The numbers of section 4.14 are exact outward-rounded reads of a scratch script, not evidence.

The result, in four sentences. The frozen statement holds: C_k MET, that is 2δ′ ≤ κ/2, gives H_{k+1}(κ, c(δ_k)δ_k) with the frozen c(δ). The same route proves more. Only off links make polymers incompatible, and only line links make coarse support, so the Kotecký–Preiss weights split by link type; then the proof needs only 2δ′ ≤ κ and gives c*(δ) < c(δ), with c*(δ) = e^{−4κ} exactly for 0 < δ ≤ 0.072094. So the frozen C_k and c(δ) are valid but weaker, and every row value built on them is a valid bound that the proved constant improves; the NOT_MET clauses of C11 and C12, the edges of C13 and C14, and the 3 × 10⁻⁵ clause of C10b are properties of the frozen formula, not of the method.

Symbols, binding for this section. a(g) = ½ Re Tr g only. b = 2 is the blocking factor only. κ = 1/4 is the norm weight, and every statement below holds for every κ > 0 unless a number is quoted or the statement names a range of κ (Lemma 4.16 needs κ ≤ 1/4). The Kotecký–Preiss pair is (α, θ). In C_k the draft sets α = t = δ′ and θ = κ, with t the tree-graph parameter. δ′ := δe^{δ}. #A is the number of elements of a set A. "Fine" means scale k and "coarse" means scale k + 1 throughout this section. U is a fine configuration and V a coarse one.

### 4.0 The statement

Fix N = 2^K L_K with L_K ≥ 4 and K ≥ 2, and 1 ≤ k ≤ K − 1. Put M := N/2^k.

- (H1) The fine lattice is Λ_k = (ℤ/M)⁴ and the coarse lattice Λ_{k+1} = (ℤ/(M/2))⁴. B is the YM4-03 line map at b = 2, (BU)_μ(x′) = U_μ(2x′)U_μ(2x′ + e_μ). ν_k has density ρ_k against product Haar measure on Λ_k, and ρ_{k+1} is the density of ν_{k+1} = B_*ν_k.
- (H2) H_k(κ, δ) holds with δ > 0: log ρ_k(U) = const_k + Σ_{Y ∈ 𝒴} R_k(Y; U) for every U. 𝒴 is the set of sets Y of fine links with #Y ≥ 4 that contain a closed loop. Each R_k(Y; ·) is real, bounded and measurable, invariant under every fine gauge transformation, and a function of U restricted to Y. The norm obeys

```text
norm_kappa(R_k) := sup_l sum_{Y containing l} e^{kappa #Y} sup_U |R_k(Y;U)|  <=  delta.
```

With δ = 0 every R_k vanishes, ρ_k is constant, and so is ρ_{k+1}. So δ > 0 loses nothing.

**Theorem G1 (as frozen).** Assume (H1), (H2) and C_k: 2δ′ ≤ κ/2. Then H_{k+1}(κ, c(δ)δ) holds, with

```text
c(delta) := e^{delta} [ e^{-4 kappa} + max_{n >= 4} ( e^{-(kappa/2 - 2 delta') n} - e^{-kappa n / 2} ) ],     delta' = delta e^{delta}.
```

**Theorem G1* (what the proof gives).** Assume (H1), (H2), 0 < κ ≤ 1/4 and 2δ′ ≤ κ. Then H_{k+1}(κ, c*(δ)δ) holds, with

```text
c*(delta) := max{ e^{-4 kappa},  e^{delta + 2 delta' - 5 kappa},  e^{delta} sup_{f >= 4} ( e^{-(kappa - 2 delta') f} - e^{-kappa f} ) }.
```

For κ > 1/4 the same holds with c*(δ) := max{e^{−4κ}, e^{δ}Q(δ′)} and Q the supremum of section 4.9. On 2δ′ ≤ κ/2, c*(δ) < c(δ) (Lemma 4.17). For κ = 1/4, c*(δ) = e^{−1} exactly for 0 < δ ≤ 0.072094, and c*(δ) > e^{−1} for δ ≥ 0.072095 (section 4.14).

Both theorems give, in full:

- (C1) log ρ_{k+1}(V) = const_{k+1} + Σ_{Y ∈ 𝒴′} R_{k+1}(Y; V) for every V, with 𝒴′ the coarse sets of at least 4 links that contain a closed loop. Each R_{k+1}(Y; ·) is real, bounded, measurable, coarse-gauge invariant and a function of V restricted to Y. The coarse Wilson term, whatever it is, lies inside the R_{k+1}(Y) with Y ⊇ ∂P, since nothing else depends on all of V_P (Lemma 4.22).
- (C2) norm_κ(R_{k+1}) ≤ c*(δ)δ under 2δ′ ≤ κ, and ≤ c(δ)δ under C_k.
- (C3) No constant depends on N, K or the number of plaquettes.
- (C4) c and c* are nondecreasing, so the self-map propagates (Corollary 4.20).

### 4.1 The geometry at scale k

M = 2^{K−k}L_K is even and M ≥ 8, and the coarse side M/2 = 2^{K−k−1}L_K ≥ 4. Section 3.1 states the b = 2 geometry on (ℤ/N)⁴ with N even and N ≥ 8. Its proofs use only the parity of coordinates and those two size conditions. So it holds on Λ_k with N replaced by M. Four facts are used here.

**Lemma 4.1.**

1. A fine link is a **line link** when it is one of the two positions e_0(ℓ) = (2x′, μ) and e_1(ℓ) = (2x′ + e_μ, μ) of a coarse link ℓ = (x′, μ). Every other fine link is an **off link**. Distinct coarse links have disjoint positions.
2. The midpoint m_ℓ = 2x′ + e_μ meets exactly two line links, e_0(ℓ) and e_1(ℓ). Its other 6 links are off links.
3. A fine plaquette holds at most 2 line links. So it holds at least 2 off links.
4. Every closed loop of coarse links has at least 4 links.

*Proof.* Item 1 is the definition of section 3.1 read on (ℤ/M)⁴; two coarse links with a common position would share its base site and direction, so they are equal. Item 3 is Lemma 3.1 item 2. Item 2: O(m_ℓ) = {μ}. A link at m_ℓ in a direction ν ≠ μ has base m_ℓ or m_ℓ − e_ν, and its transverse odd set is {μ} in both cases, so it is an off link. The two links at m_ℓ in direction μ are e_0(ℓ) and e_1(ℓ). Item 4: the coarse torus (ℤ/L)⁴ with L = M/2 ≥ 4 has no self-loops and no double links, since L ≥ 3. A 3-cycle would be three signed unit steps with sum 0 mod L in every coordinate. With L ≥ 4 the sum would be 0 in ℤ⁴, which needs an even number of steps. So every cycle has length at least 4. ∎

For a set Y of fine links write line(Y) for its line links and off(Y) for its off links, so #Y = #line(Y) + #off(Y). Its **coarse shadow** is

```text
Y''(Y) := { coarse links l : e_0(l) in Y and e_1(l) in Y }.
```

Positions of distinct coarse links are distinct, so 2#Y″(Y) ≤ #line(Y).

### 4.2 The pushforward in the line gauge, and Lemma A at scale k

**Lemma 4.2 (the pushforward).** Let ρ be a bounded, positive, measurable density on the fine configurations, invariant under every fine gauge transformation. Then B_*(ρ dU) has the density

```text
rho'(V) = integral over the off links of rho(U),   with every line at (U_0, U_1) = (1, V_l).
```

ρ′ is positive, and invariant under every coarse gauge transformation.

*Proof.* Let F be bounded and measurable on the coarse configurations. For each coarse link, (U_0, U_1) ↦ (U_0, U_0U_1) preserves product Haar measure (YM4-03 Lemma 3). So ∫F(BU)ρ(U)dU = ∫dV F(V) ∫dU_0 ∫∏dU_off ρ(U_0, U_0⁻¹V, off), with one U_0 per coarse link. Fix one coarse link ℓ and every other variable. The gauge transformation at m_ℓ by h = U_0 sends (U_0, U_1) to (1, U_0U_1) = (1, V_ℓ). It multiplies the 6 off links at m_ℓ by U_0 on one side (Lemma 4.1 item 2). For fixed U_0 that preserves their Haar measure. ρ is unchanged. So the U_0-integrand no longer depends on U_0, and ∫dU_0 = 1. Do this for one coarse link after another. Positivity is inherited. Coarse invariance is YM4-03 Theorem 4 item 3, whose proof uses only the invariance of the integrand and Haar measure. ∎

By YM4-03 Theorem 4, iterated, ρ_k is such a density for every k. Under (H2) each R_k(Y) is fine-gauge invariant, so ρ_k is too.

**Lemma 4.3 (Lemma A at scale k, for any invariant integrand).** Let F be a bounded measurable function of the fine configuration that is invariant under the fine gauge transformations at the site m_ℓ. Put T(V) := ∫F ∏dU_off, with every line at (1, V).

1. If F does not depend on e_0(ℓ), T is constant in V_ℓ.
2. If F does not depend on e_1(ℓ), T does not involve V_ℓ.
3. Hence T depends on V only through V restricted to Y″(Y) for any set Y of fine links such that F depends on U only through U restricted to Y.
4. If F is invariant under every fine gauge transformation, T is invariant under every coarse gauge transformation.

*Proof.* 1. The gauge transformation at m_ℓ by h sends e_0(ℓ) from 1 to h⁻¹ and e_1(ℓ) from V_ℓ to hV_ℓ, and it multiplies the off links at m_ℓ by h. F is invariant and does not see e_0(ℓ). So F((1, V), off) = F((1, V with V_ℓ → hV_ℓ), h·off). Integrate over the off links; Haar measure absorbs h. So T(V) = T(V with V_ℓ → hV_ℓ) for every h, and T is constant in V_ℓ. This is the proof of YM4-03C §2 Lemma A, which never uses that F is a product of plaquette class functions. 2. V_ℓ enters only through e_1(ℓ). 3. If ℓ ∉ Y″(Y), one of the two positions lies outside Y, and items 1 or 2 apply. A function that is constant in each V_ℓ with ℓ ∉ Y″(Y) separately, the others held fixed, is a function of V restricted to Y″(Y). 4. Let g be a coarse gauge transformation. Define g̃ on Λ_k by g̃(2x′) = g(x′), g̃(m_ℓ) = g(x′) for ℓ = (x′, μ), and g̃ = 1 elsewhere. It is well defined, since the coarse sites and the midpoints are distinct fine sites. Under U ↦ U^{g̃}, e_0(ℓ) goes from 1 to g(x′)g(x′)⁻¹ = 1, and e_1(ℓ) from V_ℓ to g(x′)V_ℓ g(x′ + e_μ)⁻¹ = (V^g)_ℓ. On the off links g̃ acts by left and right multiplications, which preserve Haar measure. So T(V^g) = T(V). This is the argument of section 3, Lemma 3.17. ∎

**Lemma 4.4 (forests).** A coarse-gauge-invariant function of V restricted to a set Y of coarse links that holds no closed loop is constant. Every coarse set that holds a closed loop has at least 4 links.

*Proof.* Section 3, Lemma 3.19, with Lemma 4.1 item 4. ∎

### 4.3 Y-objects in L^∞, and the exact line channel

Split 𝒴 = 𝒴_L ⊔ 𝒴_O. 𝒴_L holds the **line-supported** Y, with off(Y) = ∅. 𝒴_O holds the Y with at least one off link. Call the elements of 𝒴_O **objects**, and write o for them. Put

```text
w(Y) := e^{kappa #Y} sup_U |R_k(Y;U)|,        so   sum_{Y containing l} w(Y) <= delta   for every fine link l.
```

Every Y contains some link, so sup|R_k(Y)| ≤ δe^{−κ#Y} ≤ δe^{−4κ} ≤ δ.

**Lemma 4.5 (the exact line channel).** Let Y ∈ 𝒴_L and put R^L(Y; V) := R_k(Y; U) with every line at (1, V). Then:

1. R^L(Y; ·) is real, coarse-gauge invariant and a function of V restricted to Y″(Y).
2. If Y″(Y) holds no closed loop, R^L(Y; ·) is constant.
3. If Y″(Y) holds a closed loop, then #Y ≥ #line(Y) ≥ 2#Y″(Y) ≥ 8, and e^{κ#Y″(Y)} ≤ e^{κ#Y}e^{−κ#Y/2} ≤ e^{κ#Y}e^{−4κ}.

So a V-dependent line-supported object holds 8 or more line links, and its weight passes to the coarse scale with the factor e^{−κ#Y/2} ≤ e^{−4κ}.

*Proof.* 1. Apply Lemma 4.3 items 3 and 4 to F = R_k(Y), with no integral, since Y holds no off link. 2. Lemma 4.4. 3. Lemma 4.4 gives #Y″ ≥ 4. Then 2#Y″ ≤ #line(Y) = #Y. ∎

These objects need no expansion. With the lines fixed, R_k(Y; U) for Y ∈ 𝒴_L is a function of V alone, and its exponential factors out of the off-link integral (Lemma 4.7). That is why the line channel is exact: it carries no e^{δ} and no cluster.

**Lemma 4.6 (objects in L^∞).** For o ∈ 𝒴_O put f_o := e^{R_k(o)} − 1 and ω_o := sup_U |f_o(U)|. Then f_o is real, bounded, fine-gauge invariant and a function of U restricted to o, and

```text
omega_o <= e^{delta} sup_U |R_k(o;U)|,        sum_{o in Y_O, o containing l} e^{kappa #o} omega_o  <=  e^{delta} delta = delta'   for every fine link l.
```

*Proof.* |e^x − 1| = |x Σ_{n≥0} xⁿ/(n + 1)!| ≤ |x|e^{|x|}, and |R_k(o)| ≤ δ. Sum over o ∋ l and use the norm. ∎

The factor e^{δ} is the e^{δ} prefactor of c(δ) and c*(δ), and δ′ = δe^{δ} is the parameter of C_k. Since |R_k(o)| ≤ δe^{−4κ}, the proof also allows e^{δe^{−4κ}} in place of e^{δ}. That sharpening is not used below.

### 4.4 The polymer gas of the objects

A **polymer** Γ is a nonempty finite set of objects that is connected in the graph on 𝒴_O whose edges join two objects sharing an off link. Write supp(Γ) := ∪_{o∈Γ} o, off(Γ) := off(supp Γ) and line(Γ) := line(supp Γ). Two polymers are **incompatible**, Γ ≁ Γ′, when off(Γ) ∩ off(Γ′) ≠ ∅. Every object has an off link, so Γ ≁ Γ, and ≁ is reflexive and symmetric. The activity is

```text
z_Gamma(V) := integral over the off links of prod_{o in Gamma} f_o(U),   every line at (1, V).
```

**Lemma 4.7 (the polymer representation).** For every V,

```text
rho_{k+1}(V) = e^{const_k} exp( sum_{Y in Y_L} R^L(Y;V) ) Xi(V),        Xi(V) = sum over compatible families {Gamma_i} of prod_i z_{Gamma_i}(V),
```

with the empty family giving 1, and Ξ(V) > 0.

*Proof.* Lemma 4.2 and (H2) give ρ_{k+1}(V) = e^{const_k} ∫∏dU_off exp(Σ_{Y∈𝒴} R_k(Y; U)), lines at (1, V). The terms of 𝒴_L do not involve off links, so they leave the integral as exp(Σ R^L(Y; V)). The lattice is finite, so 𝒴_O is finite and ∏_{o∈𝒴_O}(1 + f_o) = Σ_{𝒮⊆𝒴_O} ∏_{o∈𝒮} f_o. Split 𝒮 into its connected components in the off-link graph. These are polymers that pairwise share no off link. Their products are functions of disjoint sets of independent Haar off links, the lines being fixed, so the integral factors over them. Conversely, a family of pairwise compatible polymers has pairwise disjoint object sets, since a common object would give a common off link. So its union is a set 𝒮 whose components are exactly these polymers. Hence the subsets 𝒮 correspond one to one to the compatible families. Ξ(V) is the integral of exp(Σ_{o∈𝒴_O} R_k(o)) > 0. ∎

**Lemma 4.8 (the activities).** For every polymer Γ:

1. |z_Γ(V)| ≤ ω(Γ) := ∏_{o∈Γ} ω_o for every V.
2. z_Γ is real and coarse-gauge invariant.
3. z_Γ depends on V only through V restricted to Y″(Γ) := Y″(supp Γ), and 2#Y″(Γ) ≤ #line(Γ) ≤ Σ_{o∈Γ} #line(o).

*Proof.* 1. Haar measure is a probability measure. 2. Each f_o is real. Lemma 4.3 item 4 applies to F = ∏ f_o. 3. Lemma 4.3 item 3 with Y = supp Γ, and section 4.1. ∎

### 4.5 Kotecký–Preiss, and the per-polymer corollary

Clusters are as in section 3.6. A cluster X is a finite nonempty multiset of polymers with multiplicities m_X(Γ), whose incompatibility graph is connected. φ(X) is its Ursell coefficient, and Φ(X; z) := φ(X)∏_Γ z(Γ)^{m_X(Γ)}. For a function d on polymers, d(X) := Σ_Γ m_X(Γ)d(Γ). X ∋ Γ means m_X(Γ) ≥ 1, and X ≁ Γ means that some polymer of X is incompatible with Γ. {Γ} denotes the cluster with one copy of Γ. Its graph has one vertex, so φ({Γ}) = 1.

**Theorem 4.9 (Kotecký and Preiss 1986, REPORTED).** Let 𝒫 be a finite set with a reflexive, symmetric relation ≁. Let z: 𝒫 → ℂ, a: 𝒫 → (0, ∞) and d: 𝒫 → [0, ∞). Suppose that for every Γ ∈ 𝒫

```text
(KP)   sum_{Gamma' ~/~ Gamma} |z(Gamma')| e^{a(Gamma') + d(Gamma')}  <=  a(Gamma).
```

Then Ξ(z) ≠ 0, Σ_X |Φ(X; z)| < ∞, log Ξ(z) = Σ_X Φ(X; z), and for every Γ ∈ 𝒫, Σ_{X≁Γ} |Φ(X; z)|e^{d(X)} ≤ a(Γ).

This is section 3, Theorem 3.13. If z is real and (KP) holds, then (KP) holds for sz, s ∈ [0, 1]. So Ξ(sz) is real, continuous in s and never 0, with Ξ(0) = 1. So Ξ(z) > 0, and the series is its real logarithm.

**Corollary 4.10 (the per-polymer corollary, and the part beyond one polymer).** Assume (KP). For every Γ ∈ 𝒫:

```text
(a)   sum_{X containing Gamma} |Phi(X;z)| e^{d(X)}                      <=  |z(Gamma)| e^{a(Gamma) + d(Gamma)},
(b)   sum_{X containing Gamma, X != {Gamma}} |Phi(X;z)| e^{d(X)}        <=  |z(Gamma)| e^{d(Gamma)} ( e^{a(Gamma)} - 1 ).
```

*Proof.* (a) Let η > 0. Add a marker Γ̂ with z(Γ̂) = 0, d(Γ̂) = 0 and a(Γ̂) = |z(Γ)|e^{a(Γ)+d(Γ)} + η, incompatible with itself and with Γ only. (KP) holds at Γ̂, since its left side is |z(Γ)|e^{a(Γ)+d(Γ)} + 0. At every other polymer the left side gains at most the term of Γ̂, which is 0. A cluster that holds Γ̂ has Φ = 0. Every other cluster of the enlarged set is a cluster of 𝒫 with the same Φ. Theorem 4.9 at Γ̂ bounds the clusters of 𝒫 that hold Γ by a(Γ̂). Let η → 0. This is section 3, Corollary 3.14, with Γ_0 = {Γ}. (b) The cluster {Γ} enters (a) with |Φ({Γ}; z)|e^{d({Γ})} = |z(Γ)|e^{d(Γ)}. Subtract it from both sides. ∎

### 4.6 The tree-graph bound

Fix a total order on 𝒴_O. For a polymer Γ and a fine link e with e ∈ supp(Γ), the **root** of Γ at e is the least object of Γ that contains e.

**Lemma 4.11 (the root decomposition).** Let e ∈ supp(Γ), o the root of Γ at e, and Γ ≠ {o}. Each connected component C of Γ ∖ {o} in the off-link graph has an object that shares an off link with o. Let e_C be the least off link of o held by an object of C. Then C ↦ e_C is injective. So Γ ↦ (o, (C_{e′})_{e′ ∈ off(o)}), with C_{e′} the component indexed by e′ or ∅, is injective. Each nonempty C_{e′} is a polymer with e′ ∈ off(C_{e′}) and fewer objects than Γ.

*Proof.* Γ is connected. A path in Γ from an object of C to o leaves C only through o, since C is a component of Γ ∖ {o}. So its last object in C shares an off link with o. If e_C = e_{C′} with C ≠ C′, objects of C and C′ share that off link and are adjacent in Γ ∖ {o}, so C = C′. Γ = {o} ∪ ⋃_C C, so the data determine Γ. ∎

**Lemma 4.12 (the tree-graph bound).** Let ν_o ≥ 0 for o ∈ 𝒴_O, put ν(Γ) := ∏_{o∈Γ} ν_o, and let t ≥ 0. Suppose

```text
sum_{o in Y_O, e in o} nu_o e^{t #off(o)}  <=  t      for every off link e.
```

Then:

1. T_ν(e) := Σ_{Γ : e ∈ off(Γ)} ν(Γ) ≤ t for every off link e.
2. For every fine link e, line or off, Σ_{Γ : e ∈ supp Γ, #Γ ≥ 2} ν(Γ) ≤ Σ_{o∋e} ν_o[(1 + t)^{#off(o)} − 1], where o runs over the possible roots at e.

*Proof.* 1. Let T_n(e) be the same sum over polymers of at most n objects. T_0 = 0. By Lemma 4.11 with root o at e, and dropping every constraint among the components,

```text
T_n(e)  <=  sum_{o containing e} nu_o prod_{e' in off(o)} (1 + T_{n-1}(e')).
```

If T_{n−1} ≤ t everywhere, the right side is at most Σ_{o∋e} ν_o(1 + t)^{#off(o)} ≤ Σ_{o∋e} ν_o e^{t#off(o)} ≤ t. 𝒴_O is finite, so T_ν(e) = T_n(e) for large n. 2. The same decomposition, with at least one component nonempty, gives ν_o[∏_{e′∈off(o)}(1 + T_ν(e′)) − 1] for each root o, and item 1 bounds each T_ν(e′) by t. ∎

The draft's form, "Σ_{Γ∋e} Π ω ≤ t, from Σ_{o∋e} ω_o e^{t s(o)} ≤ t" with s(o) = #o, is a special case, since #off(o) ≤ #o. Attachments happen only at off links because polymers are connected only through off links. That is what lets the proof charge t to off links alone.

### 4.7 The Kotecký–Preiss condition from 2δ′ ≤ κ

Take

```text
a(Gamma) := delta' sum_{o in Gamma} #off(o),        d(Gamma) := (kappa/2) sum_{o in Gamma} #line(o),
nuTilde_o := omega_o e^{delta' #off(o) + (kappa/2) #line(o)},     so   omega(Gamma) e^{a(Gamma) + d(Gamma)} = prod_{o in Gamma} nuTilde_o.
```

So α = δ′ per off link of each object, and the tree-graph parameter is t = δ′. The function d charges κ/2 per line link of each object. By Lemma 4.8 item 3, d(Γ) ≥ κ#Y″(Γ). That is the draft's θ = κ: the output weight κ per coarse link, paid by two line links.

**Lemma 4.13.** Assume 2δ′ ≤ κ. Then:

1. Σ_{o∋e} ν̃_o e^{δ′#off(o)} ≤ δ′ for every off link e.
2. T(e) := Σ_{Γ : e ∈ off(Γ)} Π_{o∈Γ} ν̃_o ≤ δ′ for every off link e.
3. (KP) holds on the set of polymers for the activity ω(Γ), and for z_Γ(V) at every V, with these a and d.

*Proof.* 1. ν̃_o e^{δ′#off(o)} = ω_o e^{2δ′#off(o) + (κ/2)#line(o)} ≤ ω_o e^{κ#o}, since 2δ′ ≤ κ and κ/2 ≤ κ. Lemma 4.6 bounds the sum by δ′. 2. Lemma 4.12 item 1 with ν = ν̃ and t = δ′. 3. Every Γ′ ≁ Γ holds some e ∈ off(Γ). So the left side of (KP) is at most Σ_{e∈off(Γ)} T(e) ≤ δ′#off(Γ) ≤ δ′Σ_{o∈Γ}#off(o) = a(Γ). a(Γ) ≥ δ′ > 0. Lemma 4.8 item 1 passes the condition to z_Γ(V). ∎

The draft's C_k, 2δ′ ≤ κ/2, implies 2δ′ ≤ κ. So everything below holds under C_k.

### 4.8 Assembling H_{k+1}

For a cluster X put Y(X) := ∪_{Γ∈X} Y″(Γ), Φ(X; V) := Φ(X; z(V)) and Φ̄(X) := |φ(X)| Π_Γ ω(Γ)^{m_X(Γ)}. By Lemma 4.8 item 1, sup_V |Φ(X; V)| ≤ Φ̄(X), and Φ̄(X) = |Φ(X; ω)|. So Theorem 4.9 and Corollary 4.10 apply to Φ̄ with the activity ω.

**Proposition 4.14 (conclusion (C1)).** Assume (H1), (H2) and 2δ′ ≤ κ. For Y ∈ 𝒴′ put

```text
R_{k+1}(Y;V) := sum_{Y' in Y_L : Y''(Y') = Y} R^L(Y';V)  +  sum_{X : Y(X) = Y} Phi(X;V),
const_{k+1}  := const_k + sum_{Y' in Y_L : Y''(Y') holds no loop} R^L(Y';V) + sum_{X : Y(X) holds no loop} Phi(X;V).
```

Then const_{k+1} does not depend on V, log ρ_{k+1} = const_{k+1} + Σ_{Y∈𝒴′} R_{k+1}(Y), and each R_{k+1}(Y; ·) is real, bounded, measurable, coarse-gauge invariant and a function of V restricted to Y.

*Proof.* Lemma 4.7 gives log ρ_{k+1} = const_k + Σ R^L + log Ξ. Lemma 4.13 gives (KP) at every V, and Theorem 4.9 gives log Ξ(V) = Σ_X Φ(X; V), absolutely convergent and real. The bound Σ_X Φ̄(X) < ∞ from Theorem 4.9 with the activity ω is uniform in V. So the regrouping by Y(X) is allowed, and each R_{k+1}(Y; ·) is a uniform limit of bounded measurable functions. Each Φ(X; ·) is real and coarse-gauge invariant, and a function of V restricted to Y(X), by Lemma 4.8. Each R^L is the same with Y″, by Lemma 4.5. The terms whose support holds no loop are constant by Lemma 4.4 and Lemma 4.5 item 2. Every support that holds a loop has at least 4 links. ∎

### 4.9 Root-object bookkeeping, and c*(δ)

For f ≥ 1, m ≥ 0 and f + m ≥ 4 define

```text
q(f,m) := e^{-kappa (f + m)} e^{kappa m / 2} [ e^{-kappa (m mod 2)/2} * 1[m >= 8]  +  e^{2 delta' f} - 1 ],
Q(delta') := sup_{f, m} q(f,m).
```

**Proposition 4.15 (the norm, conclusion (C2)).** Assume (H1), (H2) and 2δ′ ≤ κ. Then

```text
norm_kappa(R_{k+1})  <=  delta * max{ e^{-4 kappa}, e^{delta} Q(delta') }.
```

*Proof.* Fix a coarse link ℓ and put e_0 := e_0(ℓ). Each Y′ ∈ 𝒴_L and each cluster X enters one R_{k+1}(Y) only. So Σ_{Y∋ℓ} e^{κ#Y} sup_V|R_{k+1}(Y; V)| ≤ A_L + A_O, with

```text
A_L := sum over Y' in Y_L with l in Y''(Y') and Y''(Y') holding a loop of  e^{kappa #Y''(Y')} sup|R^L(Y')|,
A_O := sum over clusters X with l in Y(X) and Y(X) holding a loop of  e^{kappa #Y(X)} PhiBar(X).
```

*The line channel.* If ℓ ∈ Y″(Y′), then e_0 ∈ Y′. By Lemma 4.5 item 3, A_L ≤ e^{−4κ} Σ_{Y′∈𝒴_L, Y′∋e_0} w(Y′).

*The objects.* Let X enter A_O. Some Γ ∈ X has ℓ ∈ Y″(Γ), so e_0 ∈ supp(Γ). Let o ∈ 𝒴_O be the root of Γ at e_0. Exactly one of three cases holds. (i) Γ = {o} and X = {Γ}. (ii) Γ = {o} and X ≠ {Γ}. (iii) #Γ ≥ 2. So every X of A_O is counted at least once in

```text
A_O  <=  sum_{o in Y_O, o containing e_0} [ S_1(o) + S_2(o) + S_3(o) ],
S_1(o) := e^{kappa #Y''(o)} omega_o * 1[ Y''(o) holds a loop ],
S_2(o) := sum_{X containing {o}, X != {{o}}} e^{d(X)} PhiBar(X),
S_3(o) := sum over Gamma with root o at e_0 and #Gamma >= 2 of  sum_{X containing Gamma} e^{d(X)} PhiBar(X).
```

Here e^{κ#Y(X)} ≤ e^{d(X)} was used in S_2 and S_3. It holds because #Y(X) ≤ Σ_Γ m_X(Γ)#Y″(Γ) and κ#Y″(Γ) ≤ d(Γ) (Lemma 4.8 item 3). Write f := #off(o) ≥ 1 and m := #line(o).

- S_1(o) ≤ ω_o e^{κ⌊m/2⌋} 1[m ≥ 8]. Indeed #Y″(o) ≤ ⌊m/2⌋, and a loop needs #Y″(o) ≥ 4 (Lemma 4.4), so m ≥ 8. This is Lemma A's both-positions rule: a V-dependent single object holds 8 or more line links.
- S_2(o) ≤ ω_o e^{(κ/2)m}(e^{δ′f} − 1), by Corollary 4.10 (b) for the activity ω at Γ = {o}, where a({o}) = δ′f and d({o}) = (κ/2)m.
- S_3(o) ≤ Σ_{Γ} ω(Γ)e^{a(Γ)+d(Γ)} = Σ_Γ Π ν̃ ≤ ν̃_o[(1 + δ′)^f − 1] ≤ ω_o e^{δ′f + (κ/2)m}(e^{δ′f} − 1), by Corollary 4.10 (a), Lemma 4.12 item 2 with ν = ν̃ and t = δ′, and Lemma 4.13 item 1.

Adding, S_1 + S_2 + S_3 ≤ ω_o e^{(κ/2)m}[e^{−κ(m mod 2)/2} 1[m ≥ 8] + e^{2δ′f} − 1] = ω_o e^{κ#o} q(f, m). Lemma 4.6 gives ω_o e^{κ#o} ≤ e^{δ}w(o). So A_O ≤ e^{δ}Q(δ′) Σ_{o∈𝒴_O, o∋e_0} w(o).

*Together.* The two sums share the budget of the single fine link e_0: Σ_{Y′∈𝒴_L∋e_0} w + Σ_{o∈𝒴_O∋e_0} w = Σ_{Y∋e_0} w(Y) ≤ δ. Hence A_L + A_O ≤ max{e^{−4κ}, e^{δ}Q(δ′)}δ. Take the supremum over ℓ. ∎

No test-set factor appears. In G0 a polymer holding both positions of ℓ had to be reached through the plaquettes at e_0 (section 3, Lemma 3.16). Here the root object contains e_0 itself, and the fine norm at e_0 already sums over all of them.

**Lemma 4.16 (Q in closed form).** Let 0 < κ ≤ 1/4, 2δ′ ≤ κ and g(f) := e^{−(κ−2δ′)f} − e^{−κf}. Then

```text
Q(delta') = max{ e^{-5 kappa + 2 delta'},  sup_{f >= 4} g(f) }.
```

If 2δ′ < κ, the supremum over f is a maximum, taken at ⌊f*⌋ or ⌈f*⌉ with f* := ln(κ/(κ − 2δ′))/(2δ′) ≥ 1/κ ≥ 4. If 2δ′ = κ, sup_f g(f) = 1.

*Proof.* Take m ≥ 8 even. Then q = e^{−κ(f + m/2)}e^{2δ′f} = e^{−κm/2}e^{−(κ−2δ′)f}. It is largest at m = 8, f = 1, where it equals e^{−5κ+2δ′}, since κ − 2δ′ ≥ 0. Take m ≥ 9 odd. Then q ≤ e^{−κ(f + m/2)}e^{2δ′f} ≤ e^{−9κ/2}e^{−(κ−2δ′)} < e^{−5κ+2δ′}. Take m ≤ 7. Then q = e^{−κm/2}g(f). On the real half-line g′(x) > 0 exactly when e^{2δ′x} < κ/(κ − 2δ′), that is x < f*. With u := 2δ′/κ ∈ (0, 1), f* = ln(1/(1 − u))/(κu) ≥ 1/κ, since ln(1/(1 − u)) ≥ u. So g increases on [0, 1/κ] ⊇ [0, 4]. If f ≥ 4, q ≤ g(f), with equality at m = 0. If f ≤ 3, then m ≥ 4 − f ≥ 1, and q < g(f) < g(4). g decreases after f*, so its maximum over integers f ≥ 4 is at ⌊f*⌋ or ⌈f*⌉. At 2δ′ = κ, g(f) = 1 − e^{−κf} increases to 1. ∎

For κ > 1/4, f* may lie below 4, and the roots with f ≤ 3 off links must be kept in Q. Define, for 0 < κ ≤ 1/4,

```text
c*(delta) := max{ e^{-4 kappa}, e^{delta} Q(delta') } = max{ e^{-4 kappa}, e^{delta + 2 delta' - 5 kappa}, e^{delta} sup_{f>=4} ( e^{-(kappa - 2 delta') f} - e^{-kappa f} ) }.
```

Proposition 4.14, Proposition 4.15 and Lemma 4.16 prove Theorem G1*. The three entries of c* are the line channel, a single object with 1 off link and 8 line links together with its clusters, and a root with f off links and no line link together with its clusters.

### 4.10 The frozen formula

**Lemma 4.17.** If 2δ′ ≤ κ/2, then c*(δ) < c(δ).

*Proof.* Put g_fr(n) := e^{−(κ/2−2δ′)n} − e^{−κn/2} and G_fr := max_{n≥4} g_fr(n) > 0. Compare root by root, for every κ > 0. Write n := f + m ≥ 4, and note e^{κm/2}e^{−κ(m mod 2)/2} = e^{κ⌊m/2⌋}. The single-object part of q(f, m) is e^{−κ(f+m)+κ⌊m/2⌋}1[m ≥ 8] ≤ e^{−κ(f + m/2)}1[m ≥ 8] ≤ e^{−5κ}, since f ≥ 1. The rest is e^{−κ(f + m/2)}(e^{2δ′f} − 1) ≤ e^{−κn/2}(e^{2δ′n} − 1) = g_fr(n) ≤ G_fr, since e^{−κf/2} ≤ 1 and f ≤ n. So Q(δ′) ≤ e^{−5κ} + G_fr < e^{−4κ} + G_fr, and e^{δ}Q(δ′) < c(δ). Also e^{−4κ} < e^{δ}e^{−4κ} ≤ c(δ). ∎

**Proof of Theorem G1.** C_k gives 2δ′ ≤ κ/2 ≤ κ. Theorem G1* gives H_{k+1}(κ, c*(δ)δ). By Lemma 4.17, c*(δ)δ < c(δ)δ, and H_{k+1}(κ, ·) is monotone in its second argument. ∎

**Remark 4.18 (the frozen formula is exactly the uniform bookkeeping).** Charge every link of an object alike: a_u(Γ) := δ′Σ_{o∈Γ}#o, d_u(Γ) := (κ/2)Σ_{o∈Γ}#o, and let attachments happen at every link. Then Lemma 4.13 item 1 reads Σ_{o∋e} ω_o e^{(2δ′+κ/2)#o} ≤ δ′, which needs 2δ′ + κ/2 ≤ κ, that is 2δ′ ≤ κ/2. That is C_k. A root o of n = #o links then gives S_1 ≤ ω_o e^{κn/2}1[n ≥ 8] and S_2 + S_3 ≤ ω_o e^{κn/2}(e^{2δ′n} − 1). Per unit e^{δ}w(o) that is e^{−κn/2}1[n ≥ 8] + g_fr(n) ≤ e^{−4κ} + G_fr. The line channel gives e^{−4κ} ≤ that. The result is δ·e^{δ}[e^{−4κ} + G_fr] = c(δ)δ, the frozen formula exactly. Its real maximizer n* = ln((κ/2)/(κ/2 − 2δ′))/(2δ′) obeys n* ≥ 2/κ = 8, by the argument of Lemma 4.16, so the frozen max over n ≥ 4 sits at n ≥ 8. This matches the engine plan's n*. The split of Lemma 4.13 improves on it for three reasons, each structural. Only off links make polymers incompatible, so a counts off links. Only off links carry attachments (Lemma 4.11), so t counts off links. Only line links make coarse support (Lemma 4.8 item 3), so d counts line links. Each link pays either α + t or κ/2 out of its κ, never both.

### 4.11 Monotonicity, and the self-map

**Lemma 4.19.** c is nondecreasing on {δ > 0 : 2δe^{δ} < κ/2}, and c* on {δ > 0 : 2δe^{δ} ≤ κ}.

*Proof.* δ′ = δe^{δ} increases with δ. For fixed n, e^{−(κ/2−2δ′)n} − e^{−κn/2} increases with δ′, and a maximum of nondecreasing functions is nondecreasing. So is a product of positive nondecreasing factors. The same holds for each entry of c*, and for their maximum. ∎

**Corollary 4.20 (the self-map, uniform in N and K).** Let C stand for c with the condition C_k, or for c* with the condition 2δ′ ≤ κ. Suppose H_k(κ, δ_k) holds, δ_k meets the condition and C(δ_k) < 1. Put δ_{j+1} := C(δ_j)δ_j for j ≥ k. Then for every j with k ≤ j ≤ K, H_j(κ, δ_j) holds and

```text
delta_j  <=  C(delta_k)^{j-k} delta_k,          sum_{j=k}^{K} delta_j  <=  delta_k / (1 - C(delta_k)).
```

*Proof.* Induction on j. If H_j(κ, δ_j) holds with δ_j ≤ δ_k, then δ_j meets the condition, since the conditions are downward closed. Theorem G1 or G1* gives H_{j+1}(κ, δ_{j+1}). Lemma 4.19 gives C(δ_j) ≤ C(δ_k), so δ_{j+1} ≤ C(δ_k)δ_j ≤ δ_j. Sum the geometric series. Nothing depends on N or K, beyond j ≤ K. ∎

This is the frozen self_map clause. With C = c it is the draft's statement. With C = c* the window is wider (section 4.14).

**Lemma 4.21 (the oscillation bound of C16).** Under H_m(κ, δ) on a torus with L_m links, Σ_Y sup_V|R_m(Y; V)| ≤ L_m δ e^{−4κ}/4, and osc_V log ρ_m ≤ L_m δ e^{−4κ}/2. On a coarse 4⁴ torus, with 1024 links and κ = 1/4, osc_V log ρ_m ≤ (512/e)δ.

*Proof.* Σ_Y sup|R(Y)| = Σ_l Σ_{Y∋l} sup|R(Y)|/#Y ≤ Σ_l Σ_{Y∋l} w(Y) · max_{n≥4} e^{−κn}/n ≤ L_m δ e^{−4κ}/4, since e^{−κn}/n decreases. The oscillation of a sum is at most twice the sum of the suprema. ∎

**Lemma 4.22 (the plaquette coefficient at every scale).** Let m ≥ 1 and H_m(κ, δ) hold. For a scale-m plaquette P, let c_½(P) := ∫χ½(V_P) log ρ_m(V) dV in Haar measure. Then

```text
| c_1/2(P) |  <=  (8/(3 pi)) e^{-4 kappa} delta  <  (8489/10000) e^{-4 kappa} delta.
```

So the plaquette coupling β_m := 2c_½(P) obeys |β_m| ≤ (16/(3π))e^{−4κ}δ, which at κ = 1/4 is below 0.6246δ.

*Proof.* V_P holds each link of ∂P once, so ∫χ½(V_P)dV = 0, and const_m contributes 0. If ∂P ⊄ Y, take ℓ ∈ ∂P ∖ Y. R_m(Y) does not involve V_ℓ, and ∫χ½(V_P)dV_ℓ = 0. So c_½(P) = Σ_{Y⊇∂P} ∫χ½(V_P)R_m(Y; V)dV. Each term is at most E|χ½| sup|R_m(Y)| = (8/(3π)) sup|R_m(Y)| (section 3.8). Fix ℓ ∈ ∂P. Then Σ_{Y⊇∂P} sup|R_m(Y)| ≤ e^{−4κ}Σ_{Y∋ℓ} w(Y) ≤ e^{−4κ}δ, since #Y ≥ 4. The rational bound is section 3.8. Numerically (16/(3π))e^{−1} < 0.62454. ∎

This is the step-m readout. It ties to C09 only in form. C09's readout, c_½(P) ∈ 2t_2⁴ ± T at scale 1, is a G0 statement, and nothing in this section changes it.

**Proposition 4.23 (the line channel is attained).** Take, at scale k, R_k(Y) = s χ½ of the fine 2 × 2 loop around each coarse plaquette P″, with Y its 8 line links, and every other R_k = 0, as in C10. Then G1's output representation has R_{k+1}(∂P″) = s χ½(V_{P″}) and nothing else. Its norm is 12|s|e^{4κ}, against the input norm 12|s|e^{8κ}. So, for the representation that Proposition 4.14 outputs, no bound of the form norm_κ(R_{k+1}) ≤ C(δ)δ, valid for every input with norm δ, can have C(δ) < e^{−4κ}, at any δ > 0. For κ = 1/4 and 0 < δ ≤ 0.072094, c*(δ) = e^{−4κ}. So there G1* is the best bound of this form for this representation.

*Proof.* Every Y is line-supported, so 𝒴_O = ∅, Ξ = 1 and log ρ_{k+1} = const + Σ R^L exactly (Lemma 4.7). With the lines at (1, V), the fine 2 × 2 loop along line links has holonomy V_{P″} (YM4-03 Proposition 2). A line link lies in the Y of the 6 coarse plaquettes through its coarse link, and sup|sχ½| = 2|s|. So the fine norm is 6 · 2|s|e^{8κ} and the coarse norm 6 · 2|s|e^{4κ}. Scale s to make the input norm δ. ∎

A different representation of the same log ρ_{k+1} could have a smaller norm. H_{k+1} asks only for one representation. So this optimality is a statement about the construction, as C10 is.

### 4.12 The coarse Wilson term inside R_k: what it costs, and why it is harmless

At scale k the Wilson term (β_k/2)χ½(U_p) = β_k a(U_p) sits inside R_k(∂p), with #∂p = 4. A fine plaquette holds at least 2 off links (Lemma 4.1 item 3). So ∂p is an object of 𝒴_O, never a line-channel term. A gauge-invariant function of the 4 links of a plaquette is a class function of U_p, so f_{∂p} = e^{R_k(∂p)} − 1 is a class function F of U_p.

**What is forfeited: Lemma B.** At step 0 the activities were products of K(U_p) with ∫K dg = 0 (section 3, Lemma 3.2 item 2). A polymer with an off link held by one plaquette only had activity 0 (Lemma 3.4, YM4-03C §6 Lemma B). So polymers were closed, and #off(γ) ≤ 2#γ (Lemma 3.5). At step k, ∫f_{∂p} dU_e = ∫F dg for every off link e of p, by Haar invariance. For R_k(∂p) = β_k a this is c_0(β_k) − 1 = Σ_{m≥1}(β_k/2)^{2m}/(m!(m + 1)!) > 0 (section 3, Lemma 3.2 item 1). So the single-plaquette polymer {∂p} has nonzero activity, unclosed polymers stay in the gas, and no closure bound is available. The same holds for every object at k ≥ 1, Wilson or not, since nothing makes f_o mean-zero.

**What G1 uses instead.** Nothing. No step of sections 4.2 to 4.11 uses a cancellation. a(Γ) counts every off link of every object, and every object pays at its sup norm. So the Wilson term changes no constant of G1 or G1*.

**What it costs in strength.** The multi-object factor is first order in δ′: q(f, m) holds e^{2δ′f} − 1 ≥ 2δ′f. A centered Wilson object, e^{R_k(∂p)} = μ_p(1 + K_p) with μ_p := ∫e^{R_k(∂p)} dg and ∫K_p dg = 0, would restore Lemma B for the plaquette objects alone. That repair is not done here. The Wilson objects have (f, m) = (2, 2) or (4, 0). They add q(2, 2) = e^{−3κ}(e^{4δ′} − 1) or q(4, 0) = e^{−4κ}(e^{8δ′} − 1) per unit e^{δ}w. At C07's δ_1 ≤ 0.011045 these are below 0.0217 and 0.0345, against e^{−4κ} = 0.36788.

**Why it is harmless at these δ.**

1. For 0 < δ ≤ 0.072094, c*(δ) = e^{−4κ}. The off channel e^{δ}Q(δ′), where every Wilson object lives, stays below the line channel there. Every certified δ_1 of the draft's window lies there: δ_1 < δ_crit⁻ = 0.0496174 (C13). So no repair of the Wilson objects could lower c* on that window. By Proposition 4.23 nothing could, for this representation.
2. The Wilson term's share of the norm is small at these couplings. By Lemma 4.22, |β_m| ≤ 0.6246δ_m at every scale m ≥ 1. At β_0 = 1/100 the draft's 12e·c_½(1/100) ∈ [2.548e-9, 2.549e-9] (C08, from the MEASURED series P_10) is about 2.7 × 10⁻⁴ of the refined δ_1 ∈ [9.42e-6, 9.45e-6].
3. The other side of the same lemma is the limit of H_k. A coarse plaquette coupling |β_m| > 0.6246δ_m is incompatible with H_m(κ, δ_m). With δ_m < δ_crit* < 0.10954 this caps |β_m| below 0.06842. So H_k with the Wilson term inside R_k is a strong-coupling hypothesis at every scale, as the draft's regime clause says. A weak-coupling H_k must carry the Wilson term outside the polymer norm.

### 4.13 Where the factor κ/2 in C_k comes from

C_k reads 2δ′ ≤ κ/2 because the uniform bookkeeping (Remark 4.18) spends α + t + κ/2 out of the budget κ of every link. The split (Lemma 4.13) spends α + t on off links and κ/2 on line links, so it needs only 2δ′ ≤ κ. For κ = 1/4 the frozen condition holds for δ ≤ 0.058923670, and the proved one for δ ≤ 0.111780108, on the 10⁻⁹ grid (section 4.14).

### 4.14 The constants at the rows' points

Read by `g1a/g1a_constants.py`: exact rationals, e^y enclosed by Taylor series with a geometric remainder, range reduction by halving and outward rounding to 2⁻²⁰⁰. The max over n or f is exact: the scan stops at an N certified to satisfy e^{(rate − r)N} ≥ rate/r, so N is past the real maximizer for every r in the enclosure. Floats only choose the scan start and print. Each bracket below is the outward-rounded enclosure over the draft's δ bracket, using that c and c* are nondecreasing. These are arithmetic of the closed forms, not evidence; the engine recomputes them.

e^{−1} ∈ [0.3678794411, 0.3678794412].

| Point (row) | δ | 2δ′ | frozen c(δ) | proved c*(δ) |
|---|---|---|---|---|
| C07, crude 1/100 | [0.011044, 0.011045] | [0.0223332, 0.0223354] | [0.4450429, 0.4450509] | e^{−1} |
| C08, refined 1/100 | [9.42e-6, 9.45e-6] | [1.88401e-5, 1.89002e-5] | [0.3679383, 0.3679386] | e^{−1} |
| C10b, s = 1/2000 | [0.026890, 0.026891] | [0.0552457, 0.0552479] | [0.5950951, 0.5951069] | e^{−1} |
| C10b, s = 1/4096 | [0.013129, 0.013131] | [0.0266050, 0.0266092] | [0.4617347, 0.4617511] | e^{−1} |
| C13, 49/1000 | 0.049 | [0.1029215, 0.1029216] | [0.9824884, 0.9824885] | e^{−1} |
| C13, 1/20 | 0.05 | [0.1051271, 0.1051272] | [1.0110668, 1.0110669] | e^{−1} |
| C13, δ_1 at 0.01369 | ≤ 0.049603 | ≤ 0.1042511 | ≤ 0.9995841 | e^{−1} |
| C13, δ_1 at 0.01370 | ≥ 0.049788 | ≥ 0.1046591 | ≥ 1.0049122 | e^{−1} |
| C14, δ_1 at 0.01959 | ≤ 0.049383 | ≤ 0.1037658 | ≤ 0.9932991 | e^{−1} |
| C14, refined 1/64 | [2.0347e-3, 2.0348e-3] | [4.07768e-3, 4.07789e-3] | [0.3808522, 0.3808529] | e^{−1} |
| C12, head-free 1/50 | [0.072645, 0.072646] | [0.1562374, 0.1562398] | undefined: 2δ′ > 1/8 | [0.3727262, 0.3727351] |
| C11, crude 1/64 | [0.10165, 0.10166] | [0.2250522, 0.2250767] | undefined: 2δ′ > 1/8 | [0.7717123, 0.7719306] |

Every frozen value of c in C07, C08, C10b, C13 and C14, and every frozen 2δ′, reproduces inside its bracket.

**The two critical points.** δ_crit := sup{δ : C_k(δ) MET and c(δ) < 1}: c⁺ < 1 at 0.049617491 and c⁻ ≥ 1 at 0.049617492, inside the frozen [0.0496174, 0.0496175]. δ_crit* := sup{δ : 2δ′ ≤ κ and c*(δ) < 1}: c*⁺ < 1 at 0.109530694 and c*⁻ ≥ 1 at 0.109530695, where 2δ′ = 0.24442 < 1/4 and the third entry of c* is binding, at f = 16. c*(δ) = e^{−1} for δ ≤ 0.072094: there e^{δ}Q(δ′) ≤ 0.36787107 < e^{−1}, read on the upper enclosure, and Lemma 4.19 extends it downward. At 0.072095 the lower enclosure of e^{δ}Q is 0.36787983 > e^{−1}, at f = 6.

**The chains** (upper ends of the δ_1 brackets):

| Row | quantity | frozen c | proved c* |
|---|---|---|---|
| C07 | c(δ_1); δ_2; Σ_k δ_k | 0.4450509; 4.91559e-3; 0.0199028 | 0.3678795; 4.06323e-3; 0.0174730 |
| C08 | c(δ_1); δ_2; Σ_k δ_k | 0.3679386; 3.47702e-6; 1.49511e-5 | 0.3678795; 3.47647e-6; 1.49497e-5 |
| C14, 1/64 | c(δ_1); δ_2; Σ_k δ_k | 0.3808529; 7.74960e-4; 3.28646e-3 | 0.3678795; 7.48562e-4; 3.21901e-3 |
| C16 | δ_20 ≤ c^{19}δ_1; osc_V log ρ_20 ≤ (512/e)δ_20 | 2.30648e-9; 4.34434e-7 | 6.18829e-11; 1.16560e-8 |

**C10b's falsifier clause.** The projection lower bound [4.00e-7, 4.01e-7] divided by c(δ_in)δ_in reads [2.4995e-5, 2.5060e-5] with the frozen c, so "at most 3e-5" holds. With c* it reads [4.0434e-5, 4.0537e-5], above 3e-5. The low-power slack becomes [24669, 24732] in place of [39905, 40008]. G1* is still not refuted there, since the ratio stays below 1.

**The self-map edges with c\*** (`g1a/g1a_edges.py`). δ_1(β) is the frozen 12α at θ = κ from the G0 lane's scratch `certify()` in `G0-a-kp.py`, and the test is δ_1 < δ_crit*⁻ = 0.109530694. These are search reads. The MET side is a certified δ_1 below δ_crit*⁻. The other side is a search read, not a proof of NOT_MET, and the bisection assumes δ_1 increases with β_0.

- Crude: MET at 0.01582 (δ_1 ≤ 0.1093334), not at 0.01583 (δ_1 = 0.1097438). Frozen C13: 0.01369/0.01370.
- C03 head and head-free: MET at 0.02037 (δ_1 ≤ 0.1092399 and 0.1092383), not at 0.02038 (0.1106172 and 0.1106156). Frozen C14: 0.01959/0.01960.
- With both proved constants, G0's 6S (section 3, (C2)) and c*: crude 0.01756/0.01757; C03 head 0.02074/0.02075, one grid step below the refined C_0 stop at 0.02075/0.02076.
- The orderings survive: 0.01582 < β_crude ≈ 0.01904, and 0.02037 < β_stop ≈ 0.02075 < β_wall ≈ 0.02247.

At C11's point, 1/64 crude, δ_1 ≤ 0.10166 meets 2δ′ ≤ 1/4, c* ≤ 0.7719306 < 1 and δ_1 < δ_crit*⁻. So with c* the crude self-map holds at 1/64. At C12's point, 1/50, the C03 head gives δ_1 ∈ [0.072646, 0.072648] (frozen C12, a CONJECTURE on C03). That lies above 0.072094 and below δ_crit*⁻. There 2δ′ ≤ 0.1562444 ≤ 1/4 and c* ≤ 0.3727528 < 1. So with c* both C_1 and the self-map hold at 1/50 for the C03 head, conditional on C03. The head-free lower limit, δ_1 ≥ 0.072645, no longer forces a NOT_MET, since c* stays below 1 up to δ_crit*.

The frozen rows predict reads of the frozen certificate. An engine that implements c and C_k as frozen will read them as frozen. Whether to re-freeze with c* is the owner's decision.

### 4.15 The constants and formulas of G1: frozen against proved

"Equal" means exactly the same constant or formula. A frozen constant that the proof improves is marked not equal, with the direction. "Reproduces" means the frozen arithmetic of the frozen formula reads inside its bracket.

| Row | Frozen in the draft | Proved here | Equal? |
|---|---|---|---|
| HYPOTHESIS | H_k form: Y finite sets of scale-k links, #Y ≥ 4, holding a closed loop; R_k(Y) real, coarse-gauge invariant, a function of V restricted to Y | reproduced at k + 1 (Proposition 4.14), with bounded and measurable added | yes |
| HYPOTHESIS | norm_κ(R_k) = sup_l Σ_{Y∋l} e^{κ#Y} sup_V \|R_k(Y; V)\| | used as frozen | yes |
| HYPOTHESIS | the coarse Wilson term (β_k/2)χ½(V_P) carried inside R_k(∂P) | used; it forfeits Lemma B and changes no constant (section 4.12); \|β_m\| ≤ 0.6246δ_m (Lemma 4.22) | yes |
| HYPOTHESIS | function space: the Banach space of such families | G1 uses only the norm | yes (not used) |
| HYPOTHESIS | κ = 1/4 | G1 and G1* hold for every κ > 0 | yes |
| HYPOTHESIS | length scales; last-scale side L_K ≥ 4 | used: fine side M ≥ 8, coarse side ≥ 4, loops ≥ 4 (Lemma 4.1) | yes |
| HYPOTHESIS | uniformity: no bound involves N, K or N_p | (C3), Corollary 4.20 | yes |
| HYPOTHESIS | admissible: C_0 MET and δ_1 < δ_crit⁻, δ_crit := sup{δ : C_k MET, c < 1} | same structure; δ_crit* ∈ [0.109530694, 0.109530695] | no: frozen window narrower, valid |
| HYPOTHESIS | regime β_0 ≤ 0.0196 (edge 0.01959) | 0.02037 with c* and the frozen δ_1 (search read) | no: frozen narrower, conservative |
| CERTIFICATES | δ′ := δ_k e^{δ_k} | used as frozen (Lemma 4.6); the proof also allows δe^{δe^{−4κ}} | yes, as used |
| CERTIFICATES | C_k MET iff 2δ′ ≤ κ/2 | the proof needs 2δ′ ≤ κ (Lemma 4.13); κ/2 is the uniform bookkeeping (Remark 4.18) | no: frozen stricter, sufficient |
| CERTIFICATES | α = t = δ′ | a(Γ) = δ′Σ#off(o), t = δ′ | yes |
| CERTIFICATES | θ = κ | d(Γ) = (κ/2)Σ#line(o) ≥ κ#Y″(Γ): weight κ per coarse link | yes, with d now explicit |
| CERTIFICATES | c(δ) = e^{δ}[e^{−4κ} + max_{n≥4}(e^{−(κ/2−2δ′)n} − e^{−κn/2})] | valid (Theorem G1); the proof gives c*(δ) = max{e^{−4κ}, e^{δ+2δ′−5κ}, e^{δ}max_{f≥4}(e^{−(κ−2δ′)f} − e^{−κf})} < c(δ) | no: frozen weaker, valid |
| CERTIFICATES | the e^{δ} prefactor on the whole bracket | e^{δ} only on the object channel; the line channel is exact | no: frozen weaker |
| CERTIFICATES | the term e^{−4κ} | the line channel, e^{−κ#Y/2} ≤ e^{−4κ} (Lemma 4.5) | yes |
| CERTIFICATES | max over n ≥ 4 of the root size | the max is over the off-link count f ≥ 4 of the root, rate κ − 2δ′, plus the separate e^{δ+2δ′−5κ}; the frozen n* ≥ 8 is proved (Remark 4.18) | no: frozen weaker |
| CERTIFICATES | self_map MET iff C_k MET and c(δ_k) < 1; δ_{k+j} ≤ c^jδ_k; Σδ_k ≤ δ_k/(1 − c); c increasing | Lemma 4.19, Corollary 4.20, for c and for c* | yes |
| CERTIFICATES | δ_crit⁻ on the 10⁻⁹ grid | frozen 0.049617491 reproduces; proved 0.109530694 | no |
| THEOREMS | Y-objects in L^∞ | Lemma 4.6 | yes |
| THEOREMS | Lemma A | Lemma 4.3, for any gauge-invariant integrand | yes |
| THEOREMS | tree-graph bound Σ_{Γ∋e}Πω ≤ t from Σ_{o∋e}ω_o e^{t s(o)} ≤ t | Lemma 4.12 with #off(o) in place of s(o); the frozen form is a special case | yes (valid); the proved hypothesis is weaker |
| THEOREMS | KP per-polymer corollary Σ_{X∋γ}\|Φ\|e^{d} ≤ \|z_γ\|e^{a(γ)+d(γ)} | Corollary 4.10 (a), plus (b) beyond the single polymer | yes |
| THEOREMS | exact line channel e^{−κ#Y/2} ≤ e^{−4κ}; a V-dependent single object holds ≥ 8 line links | Lemma 4.5; Proposition 4.15, S_1 | yes |
| THEOREMS | C_k ⇒ H_{k+1} with c(δ) | Theorem G1; Theorem G1* is stronger | yes as an implication; the proved constant is better |
| THEOREMS | status TO_BE_DERIVED | DERIVED here, route A, on the REPORTED Theorem 4.9 | — |
| C07 | 2δ_1e^{δ_1} ∈ [0.02233, 0.02234] ≤ 1/8 | [0.0223332, 0.0223354] reproduces | yes |
| C07 | c(δ_1) ∈ [0.44504, 0.44505] | reproduces [0.4450429, 0.4450509]; c* = e^{−1} ∈ [0.3678794, 0.3678795] | no: frozen weaker |
| C07 | δ_2 ≤ 4.92e-3 | reproduces 4.91559e-3; proved 4.06323e-3 | no: frozen weaker |
| C07 | Σ_k δ_k ≤ 0.01991 | reproduces 0.0199028; proved 0.0174730 | no: frozen weaker |
| C07 | self-map MET | MET under both | yes |
| C08 | c(δ_1) ∈ [0.36793, 0.36795] | reproduces [0.3679383, 0.3679386]; c* = e^{−1}, below the frozen bracket | no: frozen weaker |
| C08 | Σ_k δ_k ≤ 1.50e-5 | reproduces 1.49511e-5; proved 1.49497e-5 | no: frozen weaker |
| C10 | ratio e^{−4κ} exactly; every valid c ≥ e^{−4κ}; no contraction at κ = 0 | Proposition 4.23; c* = e^{−4κ} for δ ≤ 0.072094 attains the bound; at κ = 0, c* ≥ 1 | yes |
| C10b | C_k(δ_in) MET, 2δ′ ∈ [0.05524, 0.05525] | reproduces [0.0552457, 0.0552479] | yes |
| C10b | c(δ_in) ∈ [0.5950, 0.5951]; at s = 1/4096, [0.4617, 0.4618] | reproduce; c* = e^{−1} at both | no: frozen weaker |
| C10b | projection bound at most 3e-5 · c(δ_in)δ_in; slack 3 × 10⁴ | frozen ratio [2.4995e-5, 2.5060e-5]; with c*, [4.0434e-5, 4.0537e-5], slack about 2.47 × 10⁴ | no: the clause holds only for the frozen c |
| C11 | 2δ_1e^{δ_1} ∈ [0.22505, 0.22507] > 1/8, so C_1 and the crude self-map NOT_MET at 1/64 | value reproduces [0.2250522, 0.2250767]; it meets 2δ′ ≤ 1/4; c* ∈ [0.7717123, 0.7719306]; δ_1 < δ_crit*⁻; self-map MET | no: the NOT_MET is a property of the frozen formula |
| C12 | 2δ_1e^{δ_1} ≥ 0.15623 > 1/8, so C_1 NOT_MET at 1/50 under every count vector (DERIVED) | value reproduces 0.1562374; it meets 2δ′ ≤ 1/4; c* ≤ 0.3727351; with the C03 head the self-map is MET (conditional on C03) | no: the NOT_MET is a property of the frozen formula |
| C13 | c(49/1000) ∈ [0.98248, 0.98249]; c(1/20) ∈ [1.0110, 1.0111] | reproduce; c* = e^{−1} at both | no: frozen weaker |
| C13 | δ_crit ∈ [0.0496174, 0.0496175] | reproduces [0.049617491, 0.049617492]; δ_crit* ∈ [0.109530694, 0.109530695] | no: frozen narrower |
| C13 | edge MET at 0.01369, NOT_MET at 0.01370 | with c*: 0.01582/0.01583 (search read) | no |
| C13 | β_ind^crude < β_crude | 0.01582 < 0.01904 | yes |
| C14 | edge 0.01959/0.01960, the same for the head-free limit | with c*: 0.02037/0.02038 for both (search read) | no |
| C14 | head-free NOT_MET at 0.01960, so β_ind < 0.01960 for every count vector (DERIVED) | with c* the head-free limit is MET at 0.01960 | no: a property of the frozen formula |
| C14 | 1/64 refined: c(δ_1) ∈ [0.38085, 0.38086] | reproduces [0.3808522, 0.3808529]; c* = e^{−1} | no: frozen weaker |
| C14 | ordering β_ind < β_stop < β_wall | 0.02037 < 0.02075 < 0.02247 | yes |
| C16 | δ_m ≤ c(δ_1)^{m−1}δ_1, uniformly in N and K | Corollary 4.20 | yes |
| C16 | osc_V log ρ_m ≤ 2 · 1024 · e^{−4κ}δ_m/4 = (512/e)δ_m | Lemma 4.21 | yes |
| C16 | δ_20 ∈ [2.30e-9, 2.31e-9]; osc_20 ≤ 4.35e-7 | reproduce 2.30648e-9 and 4.34434e-7; proved 6.18829e-11 and 1.16560e-8 | no: frozen weaker |
| C09 | readout c_½(P) ∈ 2t_2⁴ ± T, T = (8489/10000)·12αe^{−8θ}, minimized | a G0 constant (section 3); G1 neither uses nor changes it | not a G1 constant: no G1 value to compare |
| C09 | E\|χ½\| = 8/(3π) ≤ 8489/10000 | used in Lemma 4.22, the step-m readout \|c_½(P)\| ≤ (8/(3π))e^{−4κ}δ_m (new, not frozen) | yes |
| C09 | every polymer other than F_P holding all of ∂P at both positions has ≥ 8 plaquettes | the step-k analog: a V-dependent single object holds ≥ 8 line links (Lemma 4.5, S_1) | yes, as an analog |

all_equal: **false**. No frozen G1 constant is wrong as a bound. The frozen C_k is a sufficient condition, and the frozen c(δ) is a valid but loose bound, exactly what the uniform bookkeeping of Remark 4.18 gives. The proved G1* needs only 2δ′ ≤ κ and gives c*(δ) < c(δ), equal to e^{−4κ} for δ ≤ 0.072094. Every frozen numerical value of c reproduces as arithmetic of the frozen formula. The NOT_MET clauses of C11 (C_1 and the self-map at 1/64) and C12 (C_1 at 1/50), the edges of C13 and C14 with C14's head-free clause, and C10b's 3e-5 clause are properties of the frozen formula and do not survive the proved constant.

### 4.16 Gaps

1. Theorem 4.9 is REPORTED from Kotecký and Preiss (1986) and not reproved, as ledger L06 says. It is used in the form stated, with d in the hypothesis, e^{d(X)} in the conclusion and zero activities allowed. The paper's text was not re-read in this session.
2. The edges of section 4.14 are scratch search reads. Their MET sides rest on certified upper bounds on δ_1. Their other sides are not proofs of NOT_MET, since `certify()` returns a certified root, not a lower enclosure of the least root, and the bisection assumes δ_1 increases with β_0, which is not proved. They rest on the G0 lane's scratch `certify()`, which I called and did not audit line by line.
3. G1 bounds one output representation. Whether log ρ_{k+1} has a representation of smaller norm is not addressed. Proposition 4.23's optimality holds for the representation of Proposition 4.14 only.
4. The sharper options noted in passing are not folded into c*: e^{δe^{−4κ}} in place of e^{δ}, (1 + δ′)^f in place of e^{δ′f}, a centered Wilson object with Lemma B restored. They could change c* only where c* > e^{−4κ}, that is δ ≥ 0.072095, and would move δ_crit* up. Not computed.
5. The numbers of section 4.14 come from one scratch script with its own exp enclosures. No independent check of them ran. The quoted frozen values of the draft reproduce in it.
6. Whether C_k, c(δ), δ_crit, the regime clause and the NOT_MET clauses of C11 to C14 and C10b should be re-frozen with the proved constants is not settled here. As frozen they predict reads of the frozen formula, and the row values stay valid bounds. Re-freezing with c* would also need the G0 lane's factor 2 settled, since the edges move again with both (0.01756 and 0.02074).
7. G1 says nothing about weak coupling. By Lemma 4.22 it is a statement about a class whose plaquette coupling is below 0.6246δ_m at every scale.
8. The combined G0 and G1 edges of section 4.14 use the G0 lane's proved output 6S without a check of my own.

### 4.17 Scratch files (pre-freeze disclosure)

- `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/derive/g1a/g1a_constants.py` (sha256 `3cc068cbcf113f3a0142751dbd6767cb45eae9a924cfb0f9ff99266e8635db95`), with its output `g1a_constants.out` (`22235b3586767082ec78c8733aa6458047c6b787c3a7b8bd6c9353b3ba438585`): the frozen c and the proved c* at the rows' points, the chains, δ_crit and δ_crit*, the point where c* leaves e^{−1}, C10b's ratio and the edges of the two conditions.
- `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/derive/g1a/g1a_edges.py` (`7d87ac222a73977baf192ed0a473d90bdec2a1ee75f66f895b659d96f45776a5`), with `g1a_edges.out` (`323b6a2c0fac09c7ec27f4e959a2f05af93acc75cecc6c64c62a8c106e210d10`): the self-map edges with c*, through the G0 lane's `G0-a-kp.py`.

- `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/derive/g1a/g1a_treegraph_toy.py` (`4053110e5f2709c7596be1fce31dc8ba0c46394f991be31b7e9bc0fff16796db`), with `g1a_treegraph_toy.out` (`af689312189f0b4838d9c7376759cf1b804da7dfa75fc7beeba6ddee5abaca5f`): a sanity read of Lemma 4.12 in exact Fractions on 12 random hypergraphs of 14 links (5 of them line links) and 11 objects, with weights scaled to meet the hypothesis. Every off-link-connected set was enumerated (786 to 2017 per seed). T(e)/t read at most 0.8301, and item 2 held at every link. It checks the lemma on examples; it is not its proof.

None of these files is an engine, and none is evidence.

### References

- R. Kotecký and D. Preiss, Cluster expansion for abstract polymer models, Comm. Math. Phys. 103 (1986) 491–498. REPORTED.
- Repo: NOTE-YM4-03-ONE-SCALE-BLOCKING.md §2 (Proposition 2, Lemma 3), §3 (Theorem 4); NOTE-YM4-03C-BLOCKED-ACTION.md §2 (the line gauge, Lemma A), §6 (Lemma B, the polymer form), §12 (OPEN: the local polymer bound); NOTE-YM4-04-TWO-TERNARY-BLOCKS-20261107.md and NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md (the global and correlation-only routes this step replaces); LEMMA-0001-GAUGE-INVARIANCE.md.
- This note, section 3: Lemma 3.1 (the b = 2 geometry), Lemma 3.2 (c_0 and K), Lemmas 3.4 and 3.5 (Lemma B and closure), Theorem 3.13 and Corollary 3.14 (Kotecký–Preiss and the marker), Lemma 3.17 (coarse invariance), Lemma 3.19 (forests), §3.8 (E|χ½| = 8/(3π) < 8489/10000).
