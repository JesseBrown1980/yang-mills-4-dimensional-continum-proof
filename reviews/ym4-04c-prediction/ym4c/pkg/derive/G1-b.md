## 4. Theorem G1: the step from scale k to scale k + 1 (route B)

**Status of this section.** Written by the G1 route-B lane on November 9, 2026, from main `830fd3f`, before any engine code. Route B argues through the Mayer expansion of a hard-core polymer gas, Penrose's tree-graph inequality and an explicit tree recursion, and only then compares with the Kotecký–Preiss form. DERIVED here: Lemmas 4.1 to 4.5, 4.6a, 4.7 to 4.9a, Theorem 4.10 (G1 with the proved constants c_♯ ≤ c_B) and Corollary 4.11 (the self-map). REPORTED: the Mayer identity and Penrose's inequality (Lemma 4.6). CONDITIONAL: every number in 4.13 that uses a step-0 output δ_1 rests on Theorem G0 (section 3). The numbers in 4.13 are exact enclosures from `pkg/derive/g1b/g1b_constants.py`, `g1b_derived.py` and `g1b_edges.py`, Fractions and dyadic outward rounding only. They are scratch checks, not engines. **The proof gives a different formula from the frozen one.** The proved closed-form constant is c_B(δ) = exp(δ + 16δ′ − 4κ), and the exact root bookkeeping gives c_♯(δ) ≤ c_B(δ), equal to e^{−4κ} for δ ≤ 0.0116995481. The frozen c(δ) is never smaller, so the frozen theorem is valid but weaker. The two agree exactly for δ ≤ δ_eq, with δ_eq in [0.0070256343, 0.0070256344].

### 4.0 Notation for this section

The renames of the freeze hold. The letter a is ½ Re Tr only. The letter b is the blocking factor 2 only. κ = 1/4 is the norm weight. The Kotecký–Preiss pair is (α, θ). The tree parameter is t.

- Λ_k is the scale-k lattice and Λ_{k+1} the next one. A link of Λ_k is a **line link** if it lies on a link of Λ_{k+1}, and an **off link** otherwise. Each link ℓ of Λ_{k+1} has two line links, at positions 0 and 1, joined at the midpoint m_ℓ (YM4-03C section 2).
- U is a configuration on Λ_k. V is a configuration on Λ_{k+1}. In the line gauge every line is at (U_0, U_1) = (1, V_ℓ).
- An **object** is a set Y of links of Λ_k with R_k(Y) not identically 0. For an object o, |o| is its number of links, off(o) its off links, line(o) its line links, and s(o) := |off(o)|. An object is **line-supported** if s(o) = 0.
- r(o) := sup_U |R_k(o; U)|. The input bound is δ ≥ ‖R_k‖_κ = sup_l Σ_{o∋l} e^{κ|o|} r(o). So r(o) ≤ δ e^{−κ|o|} for every object o.
- δ′ := δ e^{δ}. α := δ′, t := δ′. The certificate C_k is the inequality 2δ′ ≤ κ/2. On C_k, r_* := κ/2 − 2δ′ ≥ 0.
- For a set W of line links, S(W) is the set of links ℓ of Λ_{k+1} with both positions in W. For an object o, S(o) := S(line(o)).

### 4.1 Statements

**Theorem G1, as frozen in the draft.** Assume H_k(κ, δ). With δ′ = δe^δ, α = t = δ′ and θ = κ, if 2δ′ ≤ κ/2 then H_{k+1}(κ, c(δ)δ) holds with

```text
c(δ) = e^δ [ e^{−4κ} + max_{n≥4} ( e^{−(κ/2 − 2δ′)n} − e^{−κn/2} ) ].
```

**Theorem 4.10, as proved here.** Under the same hypothesis and on C_k, H_{k+1}(κ, c_B(δ)δ) holds with

```text
c_B(δ) = e^{δ} e^{−8(κ/2 − 2δ′)} = exp(δ + 16 δ e^{δ} − 4κ)          (κ = 1/4: exp(δ + 16δe^δ − 1)).
```

For every δ on C_k, c_B(δ) ≤ c(δ). Equality holds exactly when the integer maximiser of the bracket in c is n = 8, which is the case for δ ≤ δ_eq (section 4.10). A sharper constant c_♯ ≤ c_B, from the same proof, is stated in Theorem 4.10. So the frozen theorem follows from Theorem 4.10. The frozen formula is not what the proof gives.

Here H_k(κ, δ) means what the draft's row YM4_04C_HYPOTHESIS says: log ρ_k(U) = const_k + Σ_Y R_k(Y; U), each R_k(Y) real, invariant under every gauge transformation of Λ_k, a function of U|_Y only, with |Y| ≥ 4 and Y holding a closed loop, and ‖R_k‖_κ ≤ δ. The lattice Λ_{k+1} has every side at least L_K ≥ 4.

### 4.2 The blocked density in the line gauge

**Lemma 4.1 (iterated pushforward).** Let f be a bounded positive measurable function on configurations of Λ_k, invariant under every gauge transformation of Λ_k, with ∫ f dU = 1. Let ν_{k+1} be the pushforward of f dU under the line map B. Then ν_{k+1} has the density

```text
f′(V) = integral over the off links of f(U),   every line at (1, V_ℓ),
```

against product Haar on Λ_{k+1}. f′ is invariant under every gauge transformation of Λ_{k+1}.

*Proof.* YM4-03 Lemma 3 says that, given BU = V, the position-0 links are independent Haar and each position-1 link is fixed by the product. Fubini then gives f′(V) as the integral over the off links and the position-0 links, with each position-1 link set to U_0^{−1}V_ℓ. This is the proof of YM4-03 Theorem 4, item 2, with f in place of ∏_p w(U_p). The gauge transformation of Λ_k at m_ℓ by U_0 sends (U_0, U_1) to (1, U_0U_1) = (1, V_ℓ). It moves only off links besides the line of ℓ. Haar measure and f are invariant under it. So the position-0 integral drops out, which is the gauge step of YM4-03C section 2. For a gauge transformation g of Λ_{k+1}, extend it to g̃ on Λ_k by g̃ = g on the sites of Λ_{k+1}, g̃(m_ℓ) = g(x′) for ℓ = (x′, μ), and g̃ = 1 elsewhere. Then g̃ keeps every line in the form (1, ·) and sends V_ℓ to g(x′)V_ℓ g(x′ + μ)^{−1}. The change of variables U → U^{g̃} on the off links preserves Haar measure and f. This is the proof of YM4-03 Theorem 4, item 3. ∎

Apply Lemma 4.1 to f = ρ_k, which is bounded, positive and gauge invariant on a finite lattice. Write E_V for the expectation over the off links of Λ_k under product Haar, with every line at (1, V_ℓ). Split the objects into the line-supported set 𝒪_line and the rest, 𝒪. A line-supported object involves no off link. So, with a constant C_k that does not depend on V,

```text
ρ_{k+1}(V) = C_k · exp( Σ_{o in 𝒪_line} R_k(o; V) ) · Z(V),     Z(V) := E_V[ exp( Σ_{o in 𝒪} R_k(o) ) ].     (4.1)
```

Here R_k(o; V) means R_k(o) at the line-gauge configuration. Z(V) > 0, since the integrand is positive.

### 4.3 Lemma A for objects, and the both-positions rule

**Lemma 4.2.** Let F be a bounded measurable function of the links of Λ_k that is invariant under every gauge transformation of Λ_k at the midpoint m_ℓ. Let T(V) := E_V[F].

1. If F does not depend on position 0 of ℓ, then T is constant in V_ℓ.
2. If F does not depend on position 1 of ℓ, then T does not involve V_ℓ.
3. So T depends on V_ℓ only if F depends on both positions of ℓ.

*Proof.* Item 2 holds because V_ℓ enters the line gauge only through position 1. For item 1, let h be in SU(2). The gauge transformation at m_ℓ by h sends position 1 from V_ℓ to hV_ℓ, sends position 0 from 1 to h^{−1}, and moves the off links at m_ℓ. F does not see position 0. So F at the moved configuration equals F at the configuration with position 1 at hV_ℓ, position 0 at 1, and the off links at m_ℓ moved. E_V integrates those off links by Haar, which is invariant under the move. So T(V) = T(V with V_ℓ → hV_ℓ) for every h, and T equals its Haar average in V_ℓ. This is the proof of YM4-03C Lemma A, with F in place of a product of plaquette class functions. ∎

**Lemma 4.3 (forests).** Let S be a set of links of Λ_{k+1} that holds no closed loop. Let G be a function of V|_S that is invariant under every gauge transformation of Λ_{k+1}. Then G is constant.

*Proof.* S is a forest. Root each tree at one of its sites. Walking out from the root, a gauge transformation fixed at the root sets V_ℓ = 1 on each link of the tree, one link at a time, since each new link reaches a site not yet fixed. So G(V) = G(1). ∎

**The girth.** Every side of Λ_{k+1} is at least 4. A contractible closed loop holds at least 4 links. A winding loop holds at least the side length, so at least 4. So a set of links of Λ_{k+1} that holds a closed loop has at least 4 links.

**Corollary (both positions).** Let a function of V arise as E_V of a product of objects whose line links form the set W. By Lemma 4.2, it depends on V only through V|_{S(W)}. By Lemma 4.1 it is gauge invariant on Λ_{k+1}. By Lemma 4.3 it is constant unless S(W) holds a closed loop. So a V-dependent result has |S(W)| ≥ 4 and |W| ≥ 2|S(W)| ≥ 8. In particular, a V-dependent single object holds 8 or more line links.

### 4.4 Objects in L^∞

**Lemma 4.4.** For each object o, let ζ_o := e^{R_k(o)} − 1 and ρ̄(o) := r(o) e^{r(o)}. Then ζ_o is real, gauge invariant, a function of U|_o, and sup|ζ_o| ≤ ρ̄(o). For every link l of Λ_k,

```text
Σ_{o∋l} e^{κ|o|} ρ̄(o) ≤ δ e^{δ} = δ′.
```

*Proof.* For real x, |e^x − 1| = |Σ_{n≥1} x^n/n!| ≤ |x| Σ_{n≥0} |x|^n/n! = |x|e^{|x|}. So sup|ζ_o| ≤ r(o)e^{r(o)}. Since r(o) ≤ δ e^{−κ|o|} ≤ δ, ρ̄(o) ≤ r(o)e^{δ}. Sum with the weights e^{κ|o|}. ∎

No Hölder or Finner inequality is needed for k ≥ 1. Every bound below is a product of sup norms: |E_V[∏_{o∈Γ} ζ_o]| ≤ ∏_{o∈Γ} ρ̄(o). This is what "Y-objects in L^∞" means in the draft's G1.

*Remark (not used).* Since r(o) ≤ δe^{−κ|o|} ≤ δe^{−4κ}, the factor e^{δ} could be e^{δe^{−4κ}}. The theorem keeps δ′ = δe^{δ}, as the draft pins it.

### 4.5 The exact line channel

**Lemma 4.5.** For each line-supported object o, the term R_k(o; V) in (4.1) passes into log ρ_{k+1} with no integral. It is V-dependent only if |o| ≥ 8. It is then a gauge-invariant function of V|_{S(o)}, with |S(o)| ≤ |o|/2, and

```text
e^{κ|S(o)|} sup_V |R_k(o; V)| ≤ e^{−κ|o|/2} · e^{κ|o|} r(o) ≤ e^{−4κ} · e^{κ|o|} r(o).
```

*Proof.* The first clause is (4.1). By Lemma 4.2 with F = e^{R_k(o)}, read as a function on the lines, R_k(o; V) depends on V only through S(o). Gauge invariance on Λ_{k+1} follows from Lemma 4.1 applied to the single factor. By Lemma 4.3 and the girth it is constant unless |S(o)| ≥ 4, and then |o| ≥ 2|S(o)| ≥ 8. Each link of S(o) uses two links of o, so |S(o)| ≤ |o|/2. So e^{κ|S(o)|} ≤ e^{κ|o|/2} = e^{−κ|o|/2} e^{κ|o|}, and e^{−κ|o|/2} ≤ e^{−4κ} for |o| ≥ 8. ∎

This is the line channel of the draft, with the factor e^{−κ#Y/2} ≤ e^{−4κ}. It is exact, so no factor e^{δ} enters it. YM4-03 Proposition 2 is the special case of a Wilson loop: a coarse loop's holonomy is the fine holonomy along its lines. C10's input reads the bound with equality: |o| = 8, |S(o)| = 4.

### 4.6 The polymer gas of the other objects

Two objects o, o′ in 𝒪 are **linked** if off(o) ∩ off(o′) ≠ ∅. A **polymer** Γ is a nonempty finite set of objects of 𝒪 that is connected under linking. Write off(Γ) := ∪_{o∈Γ} off(o) and line(Γ) := ∪_{o∈Γ} line(o). Two polymers are **compatible** if off(Γ) ∩ off(Γ′) = ∅, and **incompatible**, Γ ≁ Γ′, otherwise. Every object of 𝒪 has an off link, so Γ ≁ Γ for every Γ. The activity of Γ is

```text
z_Γ(V) := E_V[ ∏_{o∈Γ} ζ_o ],      z̄_Γ := ∏_{o∈Γ} ρ̄(o) ≥ sup_V |z_Γ(V)|.
```

**Lemma 4.6a (the gas).** Z(V) = Σ ∏_i z_{Γ_i}(V), summed over all finite families {Γ_1, …, Γ_m} of pairwise compatible polymers, the empty family included with value 1.

*Proof.* ∏_{o∈𝒪}(1 + ζ_o) = Σ_{A⊂𝒪} ∏_{o∈A} ζ_o, a finite sum, since Λ_k is finite. Each A splits uniquely into its linking components, which are pairwise compatible polymers. Conversely a compatible family has a union whose components are its members, and its members are disjoint as sets of objects, since a shared object would share its off links. Components use disjoint sets of off links. The line links are fixed. So E_V factors over the components. ∎

**Lemma 4.6 (Mayer expansion and Penrose's bound; REPORTED).** For a finite hard-core polymer gas with activities z_Γ,

```text
log Σ_{compatible families} ∏ z_{Γ_i} = Σ_{m≥1} (1/m!) Σ_{(Γ_1,…,Γ_m)} φ^T(Γ_1,…,Γ_m) ∏_{i} z_{Γ_i}
```

as formal power series in the activities. Here φ^T(Γ_1,…,Γ_m) := Σ_G (−1)^{|E(G)|}, summed over the connected spanning subgraphs G of the incompatibility graph g(Γ_1,…,Γ_m) on {1,…,m}, in which i and j are joined when Γ_i ≁ Γ_j. φ^T(Γ) = 1 for m = 1. Penrose's inequality is

```text
|φ^T(Γ_1,…,Γ_m)| ≤ #{ trees τ on {1,…,m} with τ ⊂ g(Γ_1,…,Γ_m) }.
```

Sources: C. Gruber and H. Kunz, Commun. Math. Phys. 22 (1971) 133–161, for the expansion; O. Penrose, in *Statistical Mechanics: Foundations and Applications*, ed. T. A. Bak, Benjamin (1967) 101–109, for the inequality, by a partition of the connected subgraphs into Boolean intervals indexed by trees. The same bound follows from the forest formula of D. C. Brydges and T. Kennedy, J. Stat. Phys. 48 (1987) 19–49, and from G. A. Battle and P. Federbush, Lett. Math. Phys. 8 (1984) 55–57. A modern account is R. Fernández and A. Procacci, Commun. Math. Phys. 274 (2007) 123–140.

**Lemma 4.7 (tree recursion; DERIVED from Lemma 4.6).** Let u ≥ 0 be a weight on polymers. For a polymer Γ set

```text
T(Γ) := Σ_{m≥1} (1/(m−1)!) Σ_{(Γ_2,…,Γ_m)} Σ_{τ tree on {1..m}, τ ⊂ g(Γ,Γ_2,…,Γ_m)} ∏_{i=2}^{m} u(Γ_i),
```

with the m = 1 term equal to 1, and let T_n be the same sum over trees of depth at most n from the vertex 1. Then T_0 = 1, T_n(Γ) = exp(Σ_{Γ′≁Γ} u(Γ′) T_{n−1}(Γ′)), and T_n increases to T. If a function a ≥ 0 on polymers satisfies

```text
Σ_{Γ′≁Γ} u(Γ′) e^{a(Γ′)} ≤ a(Γ)   for every Γ,                                           (KP)
```

then T(Γ) ≤ e^{a(Γ)} for every Γ.

*Proof.* A tree on {1,…,m} rooted at 1 is fixed by the set C of the children of 1, |C| = j, a partition of {2,…,m} into j blocks each holding one child, and a tree on each block rooted at its child. Let the blocks have sizes m_1, …, m_j with Σ m_c = m − 1. The ordered lists of j blocks of these sizes, each with a chosen root, number (m − 1)!/∏ m_c! × ∏ m_c. An unordered set of children is counted j! times by the lists. So the weight 1/(m − 1)! becomes (1/j!) ∏_c 1/(m_c − 1)!, which is the weight of the subtrees in T_{n−1}. The edge from 1 to a child c needs Γ ≁ Γ_c, and the weight u(Γ_c) belongs to the child. So T_n(Γ) = Σ_{j≥0} (1/j!) (Σ_{Γ′≁Γ} u(Γ′) T_{n−1}(Γ′))^j, which is the exponential. All terms are nonnegative, so T_n increases with n, and its limit is T by monotone convergence. Under (KP), T_0 = 1 ≤ e^{a}, and if T_{n−1} ≤ e^{a} then T_n(Γ) ≤ exp(Σ_{Γ′≁Γ} u(Γ′)e^{a(Γ′)}) ≤ e^{a(Γ)}. ∎

**Corollary 4.7a (the per-polymer bound, with the single term split off).** Let d ≥ 0 be additive over tuples, d(Γ_1,…,Γ_m) := Σ_i d(Γ_i). Put u := z̄ e^{d}. Under (KP),

```text
Σ_{m≥1} (1/m!) Σ_{(Γ_1..Γ_m) ∋ Γ} |φ^T| ∏ z̄_{Γ_i} e^{d} ≤ z̄_Γ e^{d(Γ)} T(Γ) ≤ z̄_Γ e^{a(Γ)+d(Γ)},
```

where the tuples are those in which Γ occurs at least once. The m = 1 term, the tuple (Γ), equals z̄_Γ e^{d(Γ)}. So the tuples other than (Γ) sum to at most z̄_Γ e^{d(Γ)} (e^{a(Γ)} − 1).

*Proof.* A tuple holding Γ at least once is counted at most once for each position i with Γ_i = Γ. φ^T is symmetric in its arguments. So the left side is at most Σ_m (m/m!) Σ_{(Γ_2..Γ_m)} |φ^T(Γ, Γ_2, …)| z̄_Γ e^{d(Γ)} ∏_{i≥2} u(Γ_i). Penrose's inequality bounds |φ^T| by the number of trees, which gives z̄_Γe^{d(Γ)}T(Γ). The m = 1 term of T is 1, and Lemma 4.7 bounds T by e^{a}. ∎

This is the Kotecký–Preiss per-polymer corollary, Σ_{X∋γ}|Φ(X)|e^{d(X)} ≤ |z_γ|e^{a(γ)+d(γ)}, reached through the tree-graph inequality. R. Kotecký and D. Preiss, Commun. Math. Phys. 103 (1986) 491–498, state the same condition (KP) and prove it by induction without trees.

### 4.7 Connected sets of objects: the tree-graph bound

**Lemma 4.8.** Let ω ≥ 0 be a weight on the objects of 𝒪, and t > 0. Suppose that for every off link e,

```text
Σ_{o: e∈off(o)} ω_o e^{t s(o)} ≤ t.                                                       (*)
```

Then for every object o_0 and every off link e,

```text
Σ_{Γ∋o_0} ∏_{o∈Γ} ω_o ≤ ω_{o_0} e^{t s(o_0)},     Σ_{Γ∋o_0, Γ≠{o_0}} ∏_{o∈Γ} ω_o ≤ ω_{o_0} (e^{t s(o_0)} − 1),     Σ_{Γ: e∈off(Γ)} ∏_{o∈Γ} ω_o ≤ t,
```

the sums running over polymers.

*Proof.* Fix a total order on objects and on off links. To a polymer Γ ∋ o_0 attach its breadth-first spanning tree from o_0: each object o ≠ o_0 gets as parent the least object of the previous layer linked to it, and as attachment link the least off link it shares with that parent. Call a **decorated tree** at o a tree whose root is o, in which every node is an object, the children of a node p are grouped by an attachment link e ∈ off(p), and the children at e form a set of distinct objects that hold e. The map from Γ to its decorated tree is injective, since Γ is its set of nodes. Its weight is ∏_{o∈Γ} ω_o. Let G_n(o) be the total weight of all decorated trees at o of depth at most n, repeated objects allowed. Then G_0(o) = ω_o and

```text
G_n(o) = ω_o ∏_{e∈off(o)} ∏_{o′: e∈off(o′)} (1 + G_{n−1}(o′)) ≤ ω_o exp( Σ_{e∈off(o)} Σ_{o′∋e} G_{n−1}(o′) ).
```

By induction G_n(o) ≤ ω_o e^{t s(o)}: it holds at n = 0, and if it holds at n − 1 then each inner sum is at most t by (*), so the exponent is at most t·s(o). Every Γ has a finite depth, so the first claim follows as n grows. In the expanded product the term with no children is ω_{o_0}, and that is the image of Γ = {o_0} alone. So the polymers other than {o_0} sum to at most ω_{o_0}(e^{t s(o_0)} − 1), which is the second claim. For the third, a polymer with e ∈ off(Γ) holds an object o_0 with e ∈ off(o_0). So the sum is at most Σ_{o_0: e∈off(o_0)} ω_{o_0} e^{t s(o_0)} ≤ t. ∎

### 4.8 The certificate C_k gives (KP) and (*)

Choose

```text
a(Γ) := α |off(Γ)|,     d(Γ) := (κ/2) Σ_{o∈Γ} |o|,     ω_o := ρ̄(o) e^{α s(o) + (κ/2)|o|},     α = t = δ′.
```

**Lemma 4.9.** If 2δ′ ≤ κ/2, then (*) holds, and (KP) holds with u = z̄e^{d}.

*Proof.* For every object, ω_o e^{t s(o)} = ρ̄(o) e^{(α+t)s(o) + (κ/2)|o|} ≤ ρ̄(o) e^{κ|o|} e^{−(κ/2 − 2δ′)|o|}, since s(o) ≤ |o|. On C_k the last factor is at most 1. By Lemma 4.4 the sum over o ∋ e is at most δ′ = t. That is (*). For (KP): if Γ′ ≁ Γ then Γ′ holds an off link of Γ. So

```text
Σ_{Γ′≁Γ} z̄_{Γ′} e^{d(Γ′)+a(Γ′)} ≤ Σ_{e∈off(Γ)} Σ_{Γ′: e∈off(Γ′)} ∏_{o∈Γ′} ρ̄(o) e^{(κ/2)|o| + α s(o)} = Σ_{e∈off(Γ)} Σ_{Γ′: e∈off(Γ′)} ∏_{o∈Γ′} ω_o,
```

using |off(Γ′)| ≤ Σ_{o∈Γ′} s(o). Lemma 4.8 bounds each inner sum by t = α. So the left side is at most α|off(Γ)| = a(Γ). ∎

The proof uses C_k in exactly one place: the factor e^{−(κ/2−2δ′)|o|} ≤ 1. With α = t = δ′ and this d, the step (*) needs it. If 2δ′ > κ/2, the same factor exceeds 1 for every object, and an input with all its norm on 4-link objects breaks the majorant in (*). So C_k is the condition under which this proof closes. It is not shown to be necessary for H_{k+1}.

### 4.9 Convergence, and log Z as the cluster sum

**Lemma 4.9a.** On C_k the cluster series of Lemma 4.6 converges absolutely, uniformly in V, and its sum equals log Z(V), a real number.

*Proof.* By Corollary 4.7a with d = 0, the absolute series is at most Σ_Γ z̄_Γ e^{a(Γ)}, a finite sum. Replace each activity z_Γ by λ^{|Γ|} z_Γ with |λ| ≤ 1. The majorants do not grow, so the series converges absolutely and uniformly on the closed unit disc, to a function g(λ) analytic inside and continuous up to the boundary. Z(λ) := Σ ∏ λ^{|Γ_i|} z_{Γ_i} is a polynomial in λ with Z(0) = 1. Near λ = 0 the formal identity of Lemma 4.6 is an identity of convergent power series, so e^{g(λ)} = Z(λ) there. Both sides are analytic on the open disc, so they agree on it, and by continuity at λ = 1. So Z(V) = e^{g(1)}. Each activity is real, so g(1) is real, and log Z(V) = g(1) for the positive number Z(V). ∎

### 4.10 Assembly: the output, the root object, and the constant

For a tuple X = (Γ_1, …, Γ_m) put t_X(V) := (1/m!) φ^T(X) ∏_i z_{Γ_i}(V) and S_X := ∪_i S(line(Γ_i)). Each z_{Γ_i} is E_V of a product of gauge-invariant objects. By Lemma 4.2 it depends on V only through S(line(Γ_i)), and by Lemma 4.1 it is gauge invariant on Λ_{k+1}. So t_X is a real, gauge-invariant function of V|_{S_X}. Define, for each set Y″ of links of Λ_{k+1} that holds a closed loop,

```text
R_{k+1}(Y″) := Σ_{o in 𝒪_line, S(o) = Y″} R_k(o; ·)  +  Σ_{X: S_X = Y″} t_X.                          (4.2)
```

Terms whose support holds no closed loop are constant by Lemma 4.3 and go into const_{k+1}. By (4.1), Lemma 4.9a and absolute convergence, log ρ_{k+1} = const_{k+1} + Σ_{Y″} R_{k+1}(Y″). Each R_{k+1}(Y″) is real, gauge invariant on Λ_{k+1}, a function of V|_{Y″}, and |Y″| ≥ 4 by the girth. So H_{k+1} has the form H_k asks for, uniformly in N and K.

**Weights.** For a polymer, |S(line(Γ))| ≤ |line(Γ)|/2 ≤ (1/2)Σ_{o∈Γ}|o|. So e^{κ|S_X|} ≤ e^{d(X)}, with d as in 4.8.

**The root object.** Fix a link ℓ″ of Λ_{k+1}, and let l_0 be its position-0 link. A term of (4.2) with ℓ″ ∈ Y″ holds both positions of ℓ″, so one of its objects holds l_0. Call it the root o_0. Write w(o) := e^{κ|o|} r(o), so Σ_{o∋l_0} w(o) ≤ δ. Then

```text
Σ_{Y″∋ℓ″} e^{κ|Y″|} sup_V |R_{k+1}(Y″)| ≤ Σ_{o_0 in 𝒪_line, o_0∋l_0} L(o_0) + Σ_{o_0 in 𝒪, o_0∋l_0} [ M_1(o_0) + M_2(o_0) ],
```

where L is the line channel, M_1 the single-object term X = ({o_0}), and M_2 every other pair (Γ ∋ o_0, X ∋ Γ). A term may be counted under several roots. All terms are nonnegative, so that only adds.

- **L.** By Lemma 4.5, L(o_0) ≤ 1[|o_0| ≥ 8] e^{−κ|o_0|/2} w(o_0) ≤ e^{−4κ} w(o_0).
- **M_1.** t_X = E_V[ζ_{o_0}]. By the both-positions corollary it is V-dependent only if |line(o_0)| ≥ 8. A root in 𝒪 has s(o_0) ≥ 1, so then n := |o_0| ≥ 9, and |S(o_0)| ≤ (n − 1)/2. So M_1(o_0) ≤ 1[n ≥ 9] e^{−κ(n+1)/2} e^{κn} ρ̄(o_0).
- **M_2.** By Corollary 4.7a and Lemma 4.8, with z̄_Γ e^{d(Γ)+a(Γ)} ≤ ∏_{o∈Γ} ω_o,

```text
M_2(o_0) ≤ Σ_{Γ∋o_0} z̄_Γ e^{d(Γ)} (e^{a(Γ)} − 1) + Σ_{Γ∋o_0, Γ≠{o_0}} z̄_Γ e^{d(Γ)}
         ≤ Σ_{Γ∋o_0} ∏_{o∈Γ} ω_o − ρ̄(o_0) e^{(κ/2)n}
         ≤ ω_{o_0} e^{t s(o_0)} − ρ̄(o_0) e^{(κ/2)n} = e^{κn} ρ̄(o_0) e^{−κn/2} (e^{2δ′ s(o_0)} − 1)
         ≤ e^{κn} ρ̄(o_0) [ e^{−(κ/2 − 2δ′)n} − e^{−κn/2} ].
```

This is "the rooted sum minus the single-object term". Finally ρ̄(o_0) ≤ e^{δ} r(o_0) by Lemma 4.4, which is the e^{δ} prefactor.

**The per-root profile.** Write r_* := κ/2 − 2δ′ ≥ 0 and, for n ≥ 4,

```text
f(n) := e^{−r_* n} − e^{−κn/2},        g(n) := f(n) + 1[n ≥ 9] e^{−κ(n+1)/2}.
```

Then Σ_{Y″∋ℓ″} e^{κ|Y″|} sup|R_{k+1}(Y″)| ≤ Σ_{o_0∋l_0} w(o_0) · max{ e^{−4κ}, e^{δ} g(|o_0|) } ≤ c_♯(δ) δ.

**Theorem 4.10 (G1, as proved).** Assume H_k(κ, δ), k ≥ 1, and 2δ′ ≤ κ/2. Then H_{k+1}(κ, δ_{k+1}) holds with

```text
δ_{k+1} ≤ c_♯(δ) δ ≤ c_B(δ) δ ≤ c(δ) δ,
c_♯(δ) := max{ e^{−4κ}, e^{δ} max_{n≥4} g(n) },
c_B(δ) := e^{δ} e^{−8(κ/2 − 2δ′)} = exp(δ + 16δe^{δ} − 4κ),
c(δ)   := e^{δ} [ e^{−4κ} + max_{n≥4} f(n) ]      (the frozen formula).
```

*Proof.* The first inequality is the display above. For the second: f′(n) > 0 exactly when n < n_* := ln((κ/2)/r_*)/(2δ′), and n_* ≥ (2δ′/(κ/2))/(2δ′) = 2/κ = 8, since −ln(1 − y) ≥ y. So f increases on [4, 8] and g(n) = f(n) ≤ f(8) < e^{−8r_*} for 4 ≤ n ≤ 8. For n ≥ 9, g(n) = e^{−r_* n} − e^{−κn/2}(1 − e^{−κ/2}) ≤ e^{−r_* n} ≤ e^{−8r_*}. And e^{−4κ} ≤ e^{−8r_*}, since r_* ≤ κ/2. So c_♯ ≤ e^{δ}e^{−8r_*} = c_B. For the third: c(δ) ≥ e^{δ}[e^{−4κ} + f(8)] = e^{δ} e^{−8r_*} = c_B. ∎ (When r_* = 0, n_* = ∞ and the same steps hold with c_B = e^{δ} ≥ 1.)

**Exactly where the frozen formula equals what the proof gives.** c = c_B exactly when max_{n≥4} f(n) = f(8). Since f is unimodal with its peak at n_* ≥ 8, this holds iff f(8) ≥ f(9). The difference f(8) − f(9) = e^{−8r_*}(1 − e^{−r_*}) − e^{−4κ}(1 − e^{−κ/2}) is 0 at δ = 0, positive for 0 < δ < δ_eq and negative above, with

```text
δ_eq in [0.0070256343, 0.0070256344]   (g1b_derived.py).
```

c_♯ < c_B wherever the line channel or the n ≥ 9 single term binds. In particular c_♯(δ) = e^{−4κ} exactly for δ ≤ 0.0116995481 (g1b_sharp.py). By C10, no valid step bound on this class has c below e^{−4κ}. So on that range G1 as proved is optimal.

So: the frozen formula is a valid consequence of the proof. It adds the supremum of the single-object channel, e^{−4κ}, to the supremum of the multi-object channel, max_n f(n), and puts e^{δ} on both. The proof bounds the sum per root, takes the supremum once, and owes no e^{δ} to the exact line channel. The closed form c_B is the proof's bound with s(o_0) ≤ |o_0| and the single term bounded for every n ≥ 8. c_♯ keeps the root bookkeeping exact under those same choices.

### 4.11 The self-map, and why it propagates

**Corollary 4.11.** Let c_* be any of c_♯, c_B, c. Each is increasing in δ: δ′ = δe^{δ} increases, every f(n) and g(n) increases with δ′, and e^{δ} increases. Suppose C_k(δ_k) holds and c_*(δ_k) < 1. Put δ_{k+1} := c_*(δ_k)δ_k. Then δ_{k+1} < δ_k, so C_{k+1} holds, and c_*(δ_{k+1}) ≤ c_*(δ_k). By induction on j, H_{k+j}(κ, δ_{k+j}) holds with δ_{k+j} ≤ c_*(δ_k)^j δ_k, and Σ_{j≥0} δ_{k+j} ≤ δ_k/(1 − c_*(δ_k)). No bound involves N, K or the number of plaquettes. ∎

So δ_crit := sup{δ : C_k(δ) holds and c_*(δ) < 1} is the admissibility threshold of the self-map. Its value depends on which constant is pinned:

```text
frozen c :  δ_crit in [0.0496174910, 0.0496174911]   (reproduces C13's [0.0496174, 0.0496175])
c_B      :  δ_crit in [0.0558087801, 0.0558087802]   (set by c_B = 1; C_k holds there: 2δ′ = 0.118024 < 1/8)
c_♯      :  δ_crit in [0.0577661141, 0.0577661142]
C_k alone:  2δe^δ = κ/2 at δ in [0.0589236705, 0.0589236706]
```

### 4.12 Comparison with the Kotecký–Preiss form, and the Wilson term

**The KP form.** Route B used three inequalities: (KP) with a(Γ) = α|off(Γ)|, the per-polymer corollary 4.7a, and the tree bound (*) of Lemma 4.8. Kotecký and Preiss (1986) prove the corollary from (KP) by induction on the number of polymers. Route B proves it from Penrose's inequality and the tree recursion of Lemma 4.7. The hypotheses and the constants are the same. Route B also gives the split of the single term, M_1 versus M_2, as an exact first term of a series of nonnegative terms. The draft's pair reads α = t = δ′ and θ = κ. Here d(Γ) = (κ/2)Σ_{o∈Γ}|o| = κ · #Γ with #Γ := (1/2)Σ_{o∈Γ}|o|, the largest number of links of Λ_{k+1} that Γ can hold at both positions. With that reading θ = κ is what the proof uses. With the literal reading #Γ = Σ_{o∈Γ}|o|, θ = κ would need Σ_{o∋e} ρ̄(o) e^{(κ+2δ′)|o|} ≤ δ′, which the norm does not give, and the proof does not close.

**Carrying the coarse Wilson term inside R_k.** At scale k the term (β_k/2)χ_{1/2}(U_P) is the object R_k(∂P) on the 4 links of a plaquette P of Λ_k. A plaquette of Λ_k holds two parallel links (x, μ) and (x + ν, μ), and x_ν and x_ν + 1 are not both even, so every plaquette of Λ_k has at least 2 off links. So the Wilson objects lie in 𝒪, never in the line channel. What is forfeited is YM4-03C Lemma B. That lemma kills every cluster in which a plaquette class function has an off link held by no other factor, since that link makes U_P Haar and independent. A general object R_k(Y) is not a class function of one holonomy, so Lemma B does not hold for it, and the majorants of 4.7 to 4.10 count every linked polymer, closed or not. The cost is confined to the multi-object part M_2, since the line channel is exact and a lone Wilson object integrates to a constant. Restoring Lemma B for the Wilson objects could lower the bound by at most the multi-object share c_B(δ) − e^{−4κ} = e^{−4κ}(e^{δ+16δ′} − 1). That share is 5.9 × 10⁻⁵ at the refined δ_1 of C08, in [5.892 × 10⁻⁵, 5.912 × 10⁻⁵] over its bracket, and 0 for c_♯ wherever c_♯ = e^{−4κ}. No counting is needed at k ≥ 1: (KP) and (*) follow from the norm alone once 2δ′ ≤ κ/2. So the forfeit is harmless at these δ. It would matter only for an extension to larger coarse couplings, where Lemma B or a centering of the objects must be restored.

**The two exact controls.** C10 reads the line channel with equality: |o| = 8, |S(o)| = 4, ratio e^{−4κ}. Every constant here is at least e^{−4κ}, as C10 requires. C10b's rectangles are roots in 𝒪 with |o| = 6, s(o) = 2 and 4 line links. Alone each integrates to a constant, by the both-positions corollary, and the pair is V-dependent. That is the M_2 channel at a root of size 6. Its exact ratio, about 1.5 × 10⁻⁴, lies far below every constant here. The draft's test "projection bound at most 3 × 10⁻⁵ times c(δ_in)δ_in" reads 2.506 × 10⁻⁵ with the frozen c, 2.536 × 10⁻⁵ with c_B and 2.929 × 10⁻⁵ with c_♯, at s = 1/2000 (g1b_extra.out and 4.13). So C10b passes with every constant, with least slack under c_♯.

### 4.13 What the proved constants do to the frozen rows

Every value is an exact enclosure, from the δ_1 brackets the draft freezes (CONDITIONAL on G0). Outputs: `g1b_constants.out`, `g1b_derived.out`, `g1b_sharp.out`, `g1b_edges.out`, `g1b_edges_sharp.out`, `g1b_extra.out`, all in `pkg/derive/g1b/`. The frozen formula's own values are reproduced inside every frozen bracket, which checks the implementation.

- **C07, crude, β_0 = 1/100, δ_1 in [0.011044, 0.011045].** δ_1 > δ_eq, so the frozen c is strictly larger. c in [0.4450430, 0.4450509] (frozen); c_B in [0.4447292, 0.4447370]; c_♯ = e^{−1} = 0.3678794412. δ_2 ≤ 4.9156 × 10⁻³, 4.9122 × 10⁻³, 4.0633 × 10⁻³. Σ_k δ_k ≤ 0.0199028, 0.0198915, 0.0174730.
- **C08, refined, δ_1 in [9.42, 9.45] × 10⁻⁶.** δ_1 < δ_eq, so c = c_B exactly, in [0.3679383, 0.3679386]. c_♯ = e^{−1}, which lies below the frozen bracket [0.36793, 0.36795] by about 5.9 × 10⁻⁵. Σ_k δ_k ≤ 1.4951 × 10⁻⁵ (c, c_B), 1.4950 × 10⁻⁵ (c_♯).
- **C10b.** At s = 1/2000, δ_in in [0.026890, 0.026891]: c in [0.595095, 0.595107], c_B in [0.587932, 0.587943], c_♯ in [0.509131, 0.509143]. At s = 1/4096, δ_in in [0.013129, 0.013131]: c in [0.461734, 0.461752], c_B in [0.461150, 0.461167], c_♯ in [0.379284, 0.379301]. 2δ′_in and C_k are unchanged.
- **C11, C12.** These read C_k only, which is unchanged: 2δ′ ≥ 0.225052 at the crude 1/64 point and ≥ 0.156237 at the head-free 1/50 point, both above 1/8. NOT_MET as frozen.
- **C13.** c(49/1000) = 0.9824885 (frozen), c_B = 0.8801814, c_♯ = 0.8208979. c(1/20) = 1.0110668 (frozen), c_B = 0.8967456, c_♯ = 0.8389970. So the self-map holds at δ = 1/20 under both proved constants. The crude admissibility edge, read with the C_0 certificate at b = 1/4: 0.01369/0.01370 with the frozen δ_crit^- = 0.049617491 (reproduced), 0.01400/0.01401 with c_B (δ_crit^- = 0.055808780), and 0.01409/0.01410 with c_♯ (δ_crit^- = 0.057766114). β_ind^crude < β_crude = 0.01904 still holds.
- **C14.** The refined and head-free edges: 0.01959/0.01960 (frozen, reproduced), 0.01972/0.01973 (c_B), 0.01976/0.01977 (c_♯). So the frozen DERIVED clause "β_ind < 0.01960 for every count vector" is a fact about the frozen formula, not about G1: under c_B the head-free self-map is MET at 0.01960 through 0.01972. At β_0 = 1/64, δ_1 in [2.0347, 2.0348] × 10⁻³ < δ_eq, so c = c_B exactly, in [0.3808522, 0.3808529]; c_♯ = e^{−1}. The ordering β_ind < β_stop = 0.02075 < β_wall = 0.02247 holds under all three.
- **C16.** The oscillation step is DERIVED: Σ_Y sup|R(Y)| = Σ_l Σ_{Y∋l} sup|R(Y)|/|Y| ≤ #links · δ · max_{n≥4} e^{−κn}/n = #links · δ · e^{−1}/4, and osc ≤ 2Σ_Y sup|R(Y)|, which is (512/e)δ_m on 1024 links. δ_20 ≤ c^{19}δ_1: frozen in [2.3055, 2.3065] × 10⁻⁹, c_B in [2.2748, 2.2758] × 10⁻⁹, c_♯ in [6.1877, 6.1883] × 10⁻¹¹. osc ≤ 4.3443 × 10⁻⁷, 4.2865 × 10⁻⁷, 1.1656 × 10⁻⁸.

**What this means for the freeze.** If the frozen c stays the pinned certificate, every frozen row stays internally consistent and every bound it states stays true, since c ≥ c_B ≥ c_♯. But rows C13 and C14 then locate the edge of a weaker certificate, not the edge of G1 as proved. Two clean options: repin to c_B, a closed form, which moves C07, C10b, C13, C14 (edges) and C16 and leaves C08 and the C14 value at 1/64 unchanged; or keep c and say in C13 and C14 that the edge belongs to the frozen formula.

### 4.14 The table

"Equal" means the frozen constant or formula is exactly what this proof gives. "Weaker" means the frozen item is valid, follows from the proof, and the proof gives a smaller (better) bound. Proved values are c_B (closed form) and c_♯ (exact root bookkeeping under the same choices α = t = δ′ and d of 4.8).

| Frozen item (row) | Frozen value or formula | Proved here | Equal? |
|---|---|---|---|
| H_k form (HYPOTHESIS) | log ρ_k = const + Σ_Y R_k(Y), \|Y\| ≥ 4, closed loop, real, invariant, V\|_Y | reproduced at k + 1 by (4.2) | equal |
| norm (HYPOTHESIS) | sup_l Σ_{Y∋l} e^{κ#Y} sup\|R\| | used as is | equal |
| κ (HYPOTHESIS) | 1/4 | 1/4 | equal |
| Wilson term inside R_k (HYPOTHESIS) | carried as R_k(∂P) | carried; costs Lemma B in M_2 only (4.12) | equal |
| uniformity (HYPOTHESIS) | no N, K, N_p | none enters | equal |
| δ_crit (HYPOTHESIS, C13) | [0.0496174, 0.0496175] | c_B: [0.0558087801, 0.0558087802]; c_♯: [0.0577661141, 0.0577661142] | weaker (frozen smaller) |
| regime and window (HYPOTHESIS) | β_0 ≤ 0.0196, β_ind ≈ 0.01959 | edge 0.01972/0.01973 (c_B), 0.01976/0.01977 (c_♯) | weaker (frozen window narrower) |
| δ′ (CERTIFICATES) | δe^{δ} | δe^{δ}, from \|e^x − 1\| ≤ \|x\|e^{\|x\|} | equal |
| C_k (CERTIFICATES) | MET iff 2δ′ ≤ κ/2 | the condition under which (*) and (KP) close (Lemma 4.9); sufficiency proved | equal (as the certificate) |
| c(δ) (CERTIFICATES) | e^δ[e^{−4κ} + max_{n≥4}(e^{−(κ/2−2δ′)n} − e^{−κn/2})] | c_B = exp(δ + 16δ′ − 4κ); c_♯ = max{e^{−4κ}, e^δ max_n g(n)} | weaker; c = c_B iff δ ≤ δ_eq in [0.0070256343, 0.0070256344] |
| self-map and Σ (CERTIFICATES) | δ_{k+j} ≤ c^jδ_k, Σ ≤ δ_k/(1 − c), c increasing | Corollary 4.11, for each of c, c_B, c_♯ | equal (form) |
| e^δ prefactor (THEOREMS G1) | on both channels | on the M_1 and M_2 channels only; not on the exact line channel | weaker |
| line channel (THEOREMS G1, C10) | e^{−κ#Y/2} ≤ e^{−4κ} | Lemma 4.5, the same | equal |
| tree-graph bound (THEOREMS G1) | Σ_{Γ∋e}∏ω ≤ t from Σ_{o∋e}ω_o e^{t s(o)} ≤ t | Lemma 4.8, the same, plus the rooted form | equal |
| KP per-polymer corollary (THEOREMS G1) | Σ_{X∋γ}\|Φ\|e^d ≤ \|z_γ\|e^{a+d} | Corollary 4.7a, the same, plus the single-term split | equal |
| (α, θ, t) (C_k) | α = t = δ′, θ = κ | α = t = δ′; d = κ·(1/2)Σ\|o\| | equal under #Γ = (1/2)Σ\|o\|; fails under #Γ = Σ\|o\| |
| C07 2δ_1e^{δ_1} | [0.02233, 0.02234] | [0.0223333, 0.0223353] | equal |
| C07 c(δ_1) | [0.44504, 0.44505] | c_B [0.4447292, 0.4447370]; c_♯ = e^{−1} | weaker |
| C07 δ_2 | ≤ 4.92 × 10⁻³ | ≤ 4.9122 × 10⁻³ (c_B), 4.0633 × 10⁻³ (c_♯) | weaker |
| C07 Σ δ_k | ≤ 0.01991 | ≤ 0.0198915 (c_B), 0.0174730 (c_♯) | weaker |
| C08 c(δ_1) | [0.36793, 0.36795] | c_B equal, [0.3679383, 0.3679386]; c_♯ = e^{−1} = 0.3678794 | equal for c_B; weaker for c_♯ |
| C08 Σ δ_k | ≤ 1.50 × 10⁻⁵ | ≤ 1.4951 × 10⁻⁵ (c_B), 1.4950 × 10⁻⁵ (c_♯) | equal for c_B |
| C09 readout T | (8489/10000)·12a e^{−8b} | projection constant E\|χ_{1/2}\| = 8/(3π) ≤ 8489/10000 DERIVED; the factor 12a e^{−8b} is G0 and not derived here | not decided here |
| C10 ratio | e^{−4κ} = 0.3678794 at κ = 1/4, 1 at κ = 0 | every proved c ≥ e^{−4κ}; c_♯ = e^{−4κ} for δ ≤ 0.0116995481 | equal |
| C10b C_k(δ_in), 2δ′_in | MET, [0.05524, 0.05525] | [0.0552458, 0.0552479], MET | equal |
| C10b c(δ_in), s = 1/2000 | [0.5950, 0.5951] | c_B [0.587932, 0.587943]; c_♯ [0.509131, 0.509143] | weaker |
| C10b c(δ_in), s = 1/4096 | [0.4617, 0.4618] | c_B [0.461150, 0.461167]; c_♯ [0.379284, 0.379301] | weaker |
| C10b projection test | ≤ 3 × 10⁻⁵ · cδ_in | 2.536 × 10⁻⁵ (c_B), 2.929 × 10⁻⁵ (c_♯) | holds |
| C11 C_1 | NOT_MET, 2δ′ in [0.22505, 0.22507] | 2δ′ ≥ 0.225052, NOT_MET | equal |
| C12 C_1 | NOT_MET for every count vector | 2δ′ ≥ 0.156237, NOT_MET | equal |
| C13 c(49/1000) | [0.98248, 0.98249] | c_B 0.8801814; c_♯ 0.8208979 | weaker |
| C13 c(1/20) | [1.0110, 1.0111] | c_B 0.8967456; c_♯ 0.8389970, both < 1 | weaker (frozen > 1 only by slack) |
| C13 crude edge | MET 0.01369, NOT_MET 0.01370 | 0.01400/0.01401 (c_B), 0.01409/0.01410 (c_♯) | weaker |
| C14 refined and head-free edge | 0.01959/0.01960 | 0.01972/0.01973 (c_B), 0.01976/0.01977 (c_♯) | weaker |
| C14 c(δ_1) at 1/64 | [0.38085, 0.38086] | c_B equal, [0.3808522, 0.3808529]; c_♯ = e^{−1} | equal for c_B |
| C16 osc step | (512/e)δ_m on 1024 links | DERIVED, the same | equal |
| C16 δ_20 | [2.30, 2.31] × 10⁻⁹ | [2.2748, 2.2758] × 10⁻⁹ (c_B); [6.1877, 6.1883] × 10⁻¹¹ (c_♯) | weaker |
| C16 osc_20 | ≤ 4.35 × 10⁻⁷ | ≤ 4.2865 × 10⁻⁷ (c_B), 1.1656 × 10⁻⁸ (c_♯) | weaker |

all_equal: no. The frozen c(δ) is valid and weaker. It equals the closed-form proved c_B for δ ≤ δ_eq, which covers C08 and the 1/64 value of C14, and nowhere equals c_♯ except in the limit δ → 0.

### 4.15 Gaps: what this section does not close

1. **Lemma 4.6 is REPORTED.** The formal Mayer identity for a hard-core polymer gas and Penrose's tree-graph inequality are cited (Gruber–Kunz 1971; Penrose 1967; Brydges–Kennedy 1987; Battle–Federbush 1984; Fernández–Procacci 2007), not reproved here. Everything after them is DERIVED here.
2. **Every number in 4.13 is CONDITIONAL on G0.** The δ_1 brackets are frozen G0 outputs. The recomputed edges use the C_0 certificate at b = 1/4 only and rely on the G0 claim (note outline, section 5) that b = 1/4 decides existence and carries every δ_1 optimum. The refined edge also rests on the C03 counts, a CONJECTURE.
3. **The reading of θ = κ.** The draft does not say what #γ counts at k ≥ 1. The proof closes with #Γ = (1/2)Σ_{o∈Γ}|o| and does not close with #Γ = Σ_{o∈Γ}|o|. The freeze note should state the first.
4. **C_k is sufficient, not shown necessary.** "MET iff 2δ′ ≤ κ/2" is the definition of the certificate. The proof needs it at one step, and its failure breaks only the majorant, not H_{k+1} itself.
5. **C09.** Only the projection constant 8/(3π) ≤ 8489/10000 is checked here. The cluster factor 12a e^{−8b} belongs to G0.
6. **Which constant to pin is a freeze decision, not settled here.** c_B and c_♯ are both DERIVED. Neither is shown optimal, except that c_♯ = e^{−4κ}, the C10 floor, for δ ≤ 0.0116995481. Further slack remains in this proof (s(o_0) in place of |o_0| in M_2, e^{δe^{−4κ}} in place of e^{δ}, a t smaller than δ′, line-only weights in d), none of it used, since each would change a pinned parameter.
7. **No engine and no second seat has read this section.** The scripts in `pkg/derive/g1b/` are exact scratch checks, not engines. Gate G_attack still applies.
