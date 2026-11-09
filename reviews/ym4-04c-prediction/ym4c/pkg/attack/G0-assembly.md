# Attack on Theorem G0: assembly and constants (second seat)

**Verdict: GAP.** Every assembly step of G0 holds in both derivations. Sections 1 to 8 confirm each one with my own argument. One item is blocking (B1). The proved δ_1 and T carry the factor 6, not the frozen 12, so two frozen formulas change. B1 also makes the SCOPE row's reading of the C_1 clauses of C11 and C12 false. Those NOT_MET reads come from the factor 12, not from the norm or the counts. The KP lens filed the same constant as its B1. This lens confirms it from the assembly side, with an exact leading-order instance. Section 10 lists four minor items. One of them is a repair. Both derivations leave the lattice independence of the refined head OPEN. Section 8.2 DERIVES it for every even N ≥ 8.

Read: `derive/G0-a.md` (route A), `derive/G0-b.md` (route B), the draft `ym4-04c/synth/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp` (40 lines), `pkg/PREDICTION-v2.hbp` (for G_attack and SCOPE), `wf.json` (critic.blocking, critic.fixes), `note_outline-v2.txt` §16 (the attack brief), `attack/G0-kp.md` (the KP lens), and NOTE-YM4-03 §2 and §3, NOTE-YM4-03C §2, §4, §5 and §6.

Symbols follow the binding renames. a = ½ Re Tr. b = 2. κ = 1/4. The Kotecký–Preiss pair is (α, θ), with a(γ) = α·#off(γ) and d(γ) = θ·#γ. x := εe^{2α+θ}, with ε = ε_6(β_0). n(X) is the number of plaquettes of a cluster X, with multiplicity; G0-b writes |X|. Y″(γ) is the set of coarse links both of whose positions γ holds, and Y(X) is the union over the polymers of X. W(e_0) is the set of the 12 off links of the 6 plaquettes through e_0(ℓ). W′(ℓ) is the set of the 6 off links at the midpoint m_ℓ.

No engine ran. The exact reads below come from the scratch file of section 11, which uses integers and Fractions only. They are MEASURED scratch reads, not evidence.

## 1. V-dependence only at size ≥ 4 (attack brief (v))

Claim, in both derivations: every R_1(Y) has #Y ≥ 4, every cluster has n(X) ≥ 4, and a polymer depends on V only if Y″(γ) holds a closed coarse loop. DERIVED. My argument:

1. Every closed polymer has at least 4 plaquettes. Take a plaquette with 4 off links. It needs one more plaquette through each of them. These 4 are distinct, since two plaquettes share at most one link. So the polymer has at least 5. A polymer made only of quarters lies in one filling, since distinct fillings share no off link. A proper subset of the 4-cycle of quarters leaves some internal link held once. So that polymer is the filling, with 4.
2. z_γ is a function of V restricted to Y″(γ). This is Lemma A of NOTE-YM4-03C §2, applied one coarse link at a time. z_γ is coarse-gauge invariant (section 3). If Y″(γ) is a forest, there is a gauge transformation h with V^h = 1 on Y″(γ), built root by root along each tree. Then z_γ(V) = z_γ(V^h), which is the value of z_γ at V = 1 on Y″(γ), a constant.
3. The same holds for a cluster, with Y(X) in place of Y″(γ), since Φ(X; V) is φ(X) times a product of activities.
4. On (ℤ/L)⁴ with L ≥ 4, a closed loop of coarse links has at least 4 links. Two distinct links cannot close a loop. Three unit steps cannot sum to 0 in ℤ⁴, since the sum of their coordinates is odd. A sum that is 0 mod L but not 0 in ℤ⁴ needs a coordinate of absolute value at least L ≥ 4, and three steps reach at most 3.

Exact instance (scratch block B). At N = 10 the coarse side is L = 5. The coarse torus has no 3-cycle and no double edge. It does have a 5-cycle, the straight winding loop. So its girth is 4, but it is not bipartite. This is a counterexample to the premise "bipartite, since L is even" in G0-a Lemma 3.19. (H1) allows N = 10. The conclusion of Lemma 3.19 still holds by item 4. Minor finding m1, the same as the KP lens's m1.

Exact instance (scratch block C). On fine (ℤ/8)⁴ and (ℤ/10)⁴ I enumerate every closed off-link-connected set of at most 10 plaquettes through one off link of each class. None has fewer than 4 plaquettes. Here are the sizes of the sets whose Y″ holds a closed loop:
- class 1: size 4 (1 set, the filling), and sizes 8, 9 and 10;
- class 2: sizes 8, 9 and 10;
- class 3: size 10.

None of them has #Y″ < 4. In this range, V-dependence starts at size 4 and skips sizes 5 to 7.

Second half of brief (v): the sup norms after integration are finite. sup_V |z_γ(V)| ≤ ε^{#γ} by Finner's inequality (G0-a Lemma 3.8, G0-b Lemma 3.7). The cluster sum through any off link is at most S(x) ≤ α (G0-a Lemma 3.15 with Theorem 3.13 and Corollary 3.14; G0-b Proposition 3.15). DERIVED.

## 2. #Y″(γ) ≤ #γ

DERIVED in G0-a Lemma 3.18 and G0-b Lemma 3.6(iv). My argument follows.
- Only quarters hold line links. A quarter holds exactly 2, one in each direction of its plane.
- A coarse link in Y″(γ) needs both of its line links held. Distinct coarse links have distinct line links.
- So 2#Y″(γ) ≤ 2·#(quarters of γ) ≤ 2#γ.
- For a cluster, #Y(X) ≤ Σ_i #Y″(γ_i) ≤ n(X).

The bound is sharp: the filling F_P has #Y″ = #γ = 4. Scratch block C checks #Y″ ≤ #(quarters) ≤ #γ for every closed set of at most 10 plaquettes through the three seed links, on both lattices.

The bound enters in one place only: e^{κ#Y(X)} ≤ e^{κ n(X)}, which also needs κ > 0. Both derivations use it there and nowhere else in G0.

## 3. Gauge invariance of every activity and every sup norm

DERIVED in G0-a Lemma 3.17 and G0-b Lemma 3.6(ii). The step that could fail is the extension g̃ of a coarse gauge transformation g. I check it here.
- A fine site with exactly one odd coordinate μ equals 2x′ + e_μ for exactly one coarse link ℓ = (x′, μ). So g̃(m_ℓ) := g(x′) is well defined.
- Position 0 runs from 2x′ to m_ℓ. It goes to g(x′)·1·g(x′)⁻¹ = 1.
- Position 1 runs from m_ℓ to 2(x′ + e_μ). It goes to g(x′)V_ℓ g(x′ + e_μ)⁻¹ = (V^g)_ℓ.
- So the fiber with lines at (1, V) maps onto the fiber with lines at (1, V^g).
- Each off link is multiplied on the left and on the right by fixed elements, so product Haar is kept. Each U_p is conjugated, so each K(U_p) is kept.

The decomposition does not depend on which line gauge is used. The gauge transformation at m_ℓ by h = V_ℓ⁻¹ sends the lines (1, V_ℓ) to (V_ℓ, 1). It moves only the off links at m_ℓ, by Haar-preserving multiplications. It keeps every K(U_p). The set of off links, the polymers and every Y″(γ) are the same in both gauges. So each z_γ, and hence each R_1(Y), is the same function of V in both gauges. This is the content C18 tests.

Sup norms: sup_V |R_1(Y; V)| is the supremum of a gauge-invariant function, so it depends only on gauge orbits. Nothing more is needed. DERIVED.

## 4. Locality

DERIVED. R_1(Y; ·) := Σ_{X : Y(X) = Y} Φ(X; ·), and each Φ(X; ·) is a function of V restricted to Y(X). On a finite lattice the sum converges absolutely and uniformly in V, since sup_V |Φ(X; V)| ≤ |φ(X)| Π_i ε^{#γ_i} and these bounds have a finite sum. So R_1(Y; ·) is real, gauge invariant and a function of V restricted to Y. Two remarks, neither a defect:
- Suppose Y(X) holds a loop while every Y″(γ_i) is a forest. Then Φ(X; ·) is constant. Both derivations put it into R_1(Y(X)), not into const_1. H_1 allows a constant R_1(Y), and the norm bound counts it.
- Y(X) need not be connected. H_1 does not ask for that. The norm counts a disconnected Y at every link that Y holds.

## 5. The constant 12 and the exponent −4(θ − κ) in δ_1

### 5.1 The exponent

DERIVED, and sharp. Let X be a cluster in R_1(Y) with ℓ ∈ Y. Then:
- e^{κ#Y(X)} ≤ e^{κ n(X)} (section 2);
- e^{κ n(X)} = e^{d(X)} e^{−(θ−κ) n(X)} ≤ e^{d(X)} e^{−4(θ−κ)}, since θ ≥ κ and n(X) ≥ 4 (section 1).

The 6 fillings through ℓ have n = 4, so the 4 in the exponent is attained. G0-a also gives the sharper factor e^{−(θ−κ)#γ_0}, where γ_0 is the polymer that holds ℓ. With the tail included, S(xe^{−t}) ≤ e^{−4t} S(x) for every t ≥ 0. Every term of S has degree at least 4, and 1/(1 − μxe^{−t}) ≤ 1/(1 − μx).

### 5.2 The constant

The draft freezes δ_1 := min over certified (α, θ) of 12αe^{−4(θ−κ)}. Both derivations prove the same bound with 6. My argument for 6:
1. If ℓ ∈ Y(X), some γ ∈ X holds e_0(ℓ). So γ holds a plaquette p through e_0(ℓ).
2. p is a quarter, at the corner 2x′ of the filling F_Q of some coarse plaquette Q ∋ ℓ. Its two off links are internal links of F_Q, and both lie in W(e_0). Exactly one of them ends at m_ℓ, so exactly one lies in W′(ℓ). Both lie in off(γ).
3. So X meets W(e_0) in at least 2 links and W′(ℓ) in at least 1.
4. For every off link e, the cluster sum through e is at most S(x) ≤ α. This is Σ_{X∋e} |Φ(X)| e^{d(X)} ≤ S(x): G0-a Corollary 3.14 summed over the polymers through e, or G0-b Proposition 3.15.
5. The union bound over W′(ℓ) gives 6α. Half of the union bound over W(e_0) gives 12α/2 = 6α.

The union bound over W(e_0) without the factor ½ gives the frozen 12. It is valid, but it counts every cluster through ℓ at least twice. 6 is the least this method gives, since the 6 fillings through ℓ have pairwise disjoint off-link sets.

Exact instance (scratch blocks B and C). The following hold at every coarse link of fine (ℤ/8)⁴ and of fine (ℤ/10)⁴:
- #W(e_0) = 12 and #W′(ℓ) = 6. Every plaquette through e_0 or e_1 has exactly one off link in W′(ℓ).
- Each of the 6 fillings through ℓ holds e_0 and e_1, exactly 2 links of W(e_0) and exactly 1 link of W′(ℓ).
- N_w(4) = 1 for a class-1 link w. Every link of W(e_0) and of W′(ℓ) has class 1.

So at order x⁴ the polymer sum over the polymers that hold ℓ is exactly 6x⁴, from the 6 fillings. The 12-link union bound gives 12x⁴, and the 6-link bound gives 6x⁴. So the factor 2 is exact at leading order, and 6 is attained there. This is the polymer-level version of the KP lens's block B, which works at the cluster level.

So the frozen 12 is not the proved constant. G0-b states the theorem with 6αe^{−4(θ−κ)}. G0-a states it with 6S(εe^{2α+κ}) ≤ 6αe^{−4(θ−κ)}. Both report all_equal = false. See B1.

## 6. The readout interval T and the cluster exclusion

The statement is (C3) of G0-a and Proposition 3.26 of G0-b: |c_½(P) − 2t_2⁴| ≤ e_χ·6e^{−8θ}S(x) ≤ (8489/10000)·6αe^{−8θ}, with e_χ := E|χ½|. DERIVED. My check, step by step:
1. c_½(P) = ⟨χ½(V_P), log ρ_1⟩ in coarse Haar measure. The 4 coarse links of ∂P are distinct, so V_P is Haar distributed. Hence const_1 contributes 0.
2. If some ℓ ∈ ∂P is not in Y(X), then Φ(X; ·) is constant in V_ℓ, and ∫ χ½(V_P) dV_ℓ = 0. So only the clusters with ∂P ⊆ Y(X) contribute.
3. The cluster {F_P} contributes ⟨χ½(V_P), z_{F_P}⟩ = 2t_2⁴, from z_{F_P} = Σ_{n≥2} n t_n⁴ χ_{(n−1)/2}(V_P). I rechecked the disk count. There are 4 faces, 4 internal links and 1 internal site. Three Schur merges give (nt_n)⁴/n³. The fourth internal link then appears as u u⁻¹ next to the center and drops out.
4. The exclusion. Every other cluster with ∂P ⊆ Y(X) has n(X) ≥ 8.
   - A cluster with 2 or more polymers, counted with multiplicity, has n ≥ 4 + 4. This includes {F_P, F_P}, with n = 8.
   - A single polymer γ ≠ F_P with Y″(γ) ⊇ ∂P holds all 8 line links of ∂P. G0-a Lemma 3.22 and G0-b Lemma 3.24 show #γ ≥ 8. I checked both proofs case by case. In G0-a, a quarter of F_P holds 2 line links of ∂P and any other quarter at most 1, so n_q ≥ 8 − k, where k is the number of quarters of F_P in γ. Its cases k = 0, k = 1 to 3 and k = 4 give 8, 11 − k and 8. In G0-b, the rows of the table give 8, 10, 11, 12 and 12, and the case m = 4 gives 8. Both proofs are right.
   - The 16 one-cube bumps attain 8.
5. Each such X has |⟨χ½(V_P), Φ(X)⟩| ≤ e_χ sup_V |Φ(X)| ≤ e_χ e^{−8θ} e^{d(X)} Φ̄(X), with Φ̄(X) as in G0-a §3.8.
6. Fix ℓ ∈ ∂P. Each such X holds ℓ. By section 5.2, the sum of e^{d(X)}Φ̄(X) over the clusters that hold ℓ is at most 6S(x). That sum also contains {F_P}. This overestimates the bound but does not break it.

So T carries 6, as δ_1 does. At every (α, θ), the frozen T = (8489/10000)·12αe^{−8θ} is weaker by exactly 2 when both forms use 8489/10000, and by 2.000174 against e_χ. So the minimizing grid index is the same for both. See B1.

The exclusion is for clusters, as the critic's C09 fix asked. C09's polymer clause, "no polymer of 5, 6 or 7 plaquettes holds all of ∂P at both positions", is right for closed polymers. It is false for unclosed sets, for example F_P with one more plaquette through an internal link. Both derivations say so.

## 7. E|χ½| = 8/(3π) ≤ 8489/10000

DERIVED. Weyl's formula gives class functions on SU(2) the density (2/π) sin²φ on [0, π], with χ½ = 2cos φ. ∫_0^π |cos φ| sin²φ dφ = 2∫_0^{π/2} cos φ sin²φ dφ = 2/3. So E|χ½| = (2/π)·2·(2/3) = 8/(3π). As a check on the normalization, E[χ½²] = (2/π)∫_0^π 4cos²φ sin²φ dφ = 1.

The bound needs π > 8/(3·0.8489) = 3.14135…. Both derivations use the Machin lower bound 16(1/5 − 1/375 + 1/15625 − 1/546875) − 4/239. Scratch block A reads:
- this number equals 1231847548/392109375, the value G0-b quotes;
- it exceeds G0-a's 333/106, and 848/999 < 8489/10000;
- with 12 terms of the arctan(1/5) series, π is enclosed to width 1.5e-17, and 8/(3π) = 0.84882636316 to 11 digits;
- the margin 8489/10000 − 8/(3π) is 7.3637e-5.

One display is wrong. G0-b §3.14 block B and `G0-b-checks.out` write "8/(3π) ∈ [0.8488264, 0.8488266]". The true value 0.84882636316 lies below 0.8488264. The script rounds the lower end to nearest, not outward. The inequality 8/(3π) < 8489/10000 is unaffected. This is minor finding m2.

## 8. Uniformity in N and K

### 8.1 The crude certificate

DERIVED. Every constant in (C2) and (C3) is built from these inputs only:
- ε_6(β_0), t_2(β_0), α, θ and κ;
- the count vector;
- #W′(ℓ) = 6 or #W(e_0) = 12, and D = 20;
- μ and 8/(3π).

The geometry (G0-a Lemma 3.1, G0-b Lemma 3.3) is local, and it holds for every even N ≥ 8. The BFS injection needs only the degree bound 20, so the crude count 6F_20(n) is valid on every such torus, winding polymers included. K enters only through N = 2^K L_K, and G0 is a single step. N_p enters only in const_1 and in finiteness, never in a bound. Scratch block B confirms the local facts at N = 8 and at N = 10.

### 8.2 The refined head: lattice independence is DERIVED here

Both derivations leave open whether the C03 counts hold on every even N ≥ 8 (G0-a gap 4, G0-b gap 4). C03 writes "(DERIVED by locality: no set of fewer than 16 plaquettes winds at fine side 8)", but neither section derives it. Here is a derivation.

**Lemma U (lattice independence).** Let N ≥ 8 be even and n < 2N. Let w be an off link of Λ_0 = (ℤ/N)⁴, and w̃ a lift of w to ℤ⁴. Then N_w(n) equals the number of closed off-link-connected sets of n plaquettes of ℤ⁴ that hold w̃. Moreover, N_w(n) depends only on the class of w.

*Proof.*
1. Extents. For a plaquette p and a direction μ, the μ-extent of p is [x_μ, x_μ + 1] if μ lies in the plane of p, and {x_μ} otherwise. Two plaquettes that share a link have intersecting extents, since the extent of the link lies in both.
2. Two plaquettes per slab. A plaquette with μ in its plane has two μ-links. At most one of them is a line link, since line links occur only in quarters, one in each direction (G0-a Lemma 3.1 item 2). Let S be closed. If S holds a plaquette with μ-extent [c, c + 1], then that plaquette's off μ-link lies in a second plaquette of S. The second plaquette also has μ-extent [c, c + 1]. So S holds at least 2 plaquettes with extent [c, c + 1].
3. Chains cover slabs. Let p_0, …, p_r be plaquettes of S in which consecutive ones share an off link, lifted to ℤ⁴ step by step. Their lifted μ-extents form a chain of intersecting intervals, so their union is an interval J. Every unit slab (c, c + 1) ⊂ J lies inside the extent of some p_i, and that p_i has extent [c, c + 1].
4. Winding needs 2N plaquettes. Lift a closed polymer S on Λ_0 along its off-link adjacency. Start from a plaquette through w and its lift through w̃. Suppose two paths lift one plaquette differently. Then a closed walk in S lifts to a chain from some p̃ to p̃ + v, with v ∈ Nℤ⁴ and v ≠ 0. Take μ with v_μ ≠ 0. By item 3, the chain covers at least N consecutive unit slabs in direction μ, so it covers all N slabs of the torus. By item 2, S holds at least 2 plaquettes in each slab, and plaquettes in different slabs are different. So #S ≥ 2N. Hence for #S < 2N the lift is well defined and injective. The lift is connected. It is closed, because the second holder of each off link is adjacent to the first and lifts consistently. It holds w̃.
5. The projection is injective. Let S̃ ⊂ ℤ⁴ be closed and connected, and suppose p̃ and p̃ + v both lie in S̃, with v ∈ Nℤ⁴ and v ≠ 0. A chain from p̃ to p̃ + v covers at least N unit slabs in a direction μ with v_μ ≠ 0. So #S̃ ≥ 2N. Hence for #S̃ < 2N the projection of S̃ to Λ_0 has #S̃ distinct plaquettes. The projection is connected and closed, and it holds w. By item 4 its lift is S̃, because S̃ is a consistent lift along a spanning tree of its own adjacency graph, and that tree is a subgraph of the adjacency graph of the projection.
6. So for n < 2N the lift and the projection are inverse bijections. Since 2N ≥ 16 > 10, this covers the whole head.
7. Class. The fine translations by 2ℤ⁴ and the 384 signed permutations about a coarse site keep lines, off links, plaquettes, closure and connectivity. They are well defined on Λ_0, since N is even. They act transitively on the off links of each class. Let λ be the direction of the link, and z its endpoint with even λ-coordinate. An even translation moves z to the indicator vector of O_⊥. The reflection x_λ ↦ −x_λ fixes z and swaps the two possible other endpoints, z + e_λ and z − e_λ. A permutation then moves O_⊥ and λ to a fixed normal form. ∎

Consequences:
- C03's lattice clause becomes DERIVED for every even N ≥ 8, not only for N = 8: a closed polymer that winds has at least 2N plaquettes.
- Once the C03 values hold on one lattice, the refined certificate is uniform in N. So (C4) for the refined head is conditional on the C03 values only. Those values remain CONJECTURE until the engine reads them.
- For n ≤ 10, C17's byte-identical counts on 8⁴ and 12⁴ are now a derived consequence, not an independent prediction. Their power is against code faults only.
- The same lemma covers n ≤ 15, so C03's n = 11 and n = 12 growth readouts are lattice independent too.

Cross-read (scratch block C; MEASURED, not evidence). My own closure-driven enumeration, separate code from the C03 prototype, reads these counts for n = 4 to 10 on fine (ℤ/8)⁴ and on fine (ℤ/10)⁴:
- class 1: 1, 0, 12, 0, 32, 32, 304;
- class 2: 0, 0, 12, 0, 12, 12, 240;
- class 3: 0, 0, 12, 0, 0, 0, 216.

These are C03's predicted values for n = 4 to 10, on both lattices. Both lattices need the same number of search states: 456873, 356901 and 378071 for classes 1, 2 and 3. No set winds. The frozen file never reads N = 10, whose coarse side 5 is odd. This is minor finding m3, a repair rather than an error.

### 8.3 K

G0 is a single step, and K enters only through N. The HYPOTHESIS condition L_K ≥ 4 matters only from G1 on. In G0 there is nothing more to attack.

## 9. The constant tables against the draft

I read every row of G0-a §3.12 and G0-b §3.12 against the draft's HYPOTHESIS, CERTIFICATES and THEOREMS rows and rows C01 to C16.
- The "yes" rows match the draft text: κ; D = 20 with minimum 10; 6 plaquettes per link; Finner exponent 6; #W(e_0) = 12; F_20(n); μ; 8/(3π) ≤ 8489/10000; n_max; the series S(x); the crude head; the role of the head-free vector; Lemmas A and B; a(γ) ≤ 2α#γ; d(γ); the BFS bound; #Y″ ≤ #γ; V-dependence only at size ≥ 4; the closed-set facts of C01; and the norm arithmetic of C08 (12e|c_½|), C10 (12|s|e^{8κ} and 12|s|e^{4κ}), C10b (12|s|e^{6κ}) and C16 ((512/e)δ_m). I rederived each norm count: 6 coarse plaquettes per coarse link, sup|χ½| = 2, and for C16 the bound max_{#Y≥4} e^{−κ#Y}/#Y = e^{−4κ}/4.
- The "no" rows are the factor-2 rows and their consequences. They are δ_1; T; G0 itself; C07; C08's δ_1 and its ratio to the Wilson norm; C09's T, its T/P_10 values and "lost between 1/1000 and 1/700"; C11's C_1 clause; C12's C_1 and self-map clauses; the C13 and C14 edges; the C16 values; and the regime text. The ratio monotonicity of F_20 is also marked "no", since it is proved for every n, not only for n ≤ 59.
- Halving checks, all correct:
  - C08: [9.42e-6, 9.45e-6] → [4.71e-6, 4.725e-6]; [9.372e-6, 9.373e-6] → [4.686e-6, 4.6865e-6]; [3.6e3, 3.8e3] → [1.8e3, 1.9e3].
  - C09: [1.0e-3, 1.1e-3], [1.6e-2, 1.75e-2], [0.26, 0.28], [1.10, 1.13] and [1.38e4, 1.40e4] → [5.0e-4, 5.5e-4], [8.0e-3, 8.75e-3], [0.13, 0.14], [0.55, 0.565] and [6.9e3, 7.0e3].
  - C14: [2.0347e-3, 2.0348e-3] → [1.01735e-3, 1.0174e-3].
  - C16: 2.31e-9/2 = 1.155e-9, and (512/e)·1.155e-9 = 2.1755e-7 ≤ 2.18e-7.
  
  G0-b says these values were not rechecked. At fixed (α, θ), δ_1 and T are linear in the prefactor, so the halvings are exact.
- C09's |P_10 − 2t_2⁴| at order β⁸ is 1/1536 − 1/6144 = 1/2048. F_P gives 1/6144 and the 16 bumps give 16·2⁻¹⁵ (NOTE-YM4-03C §7.5). The low-power clause survives with the proved T. At 1/4000 the slack is T/(β⁸/2048) = 5.2259e-4·(β⁴/128)·2048/β⁸, about 2.1e12, still at least 10¹².

The two tables disagree in two places:
- CERTIFICATES, "C_0 MET". G0-a writes "no: frozen condition is stricter than needed". Its remark 3.10.4 says the cap α ≤ 1/4 "can only turn a MET into NOT_MET". But G0-b Lemma 3.22 proves α_−(θ) ≤ 1/8 whenever any α is certified, so the cap never binds. Both derivations show that θ = 1/4 decides existence, and θ = 1/4 is grid point i = 0. So the frozen condition is equivalent in effect. G0-a's "no" should read "equal in effect". This is minor finding m4.
- The two proved δ_1 differ in form: 6S(εe^{2α+κ}) in G0-a, and 6αe^{−4(θ−κ)} in G0-b. This is the KP lens's m4 and is not repeated here.

## 10. Findings

### Blocking

**B1. δ_1 and T: the proved constant is 6, the frozen one is 12.** The KP lens's B1 names the same constant. This lens confirms it from the assembly side.
- Claim. Both derivations prove δ_1 ≤ 6αe^{−4(θ−κ)} and |c_½(P) − 2t_2⁴| ≤ (8489/10000)·6αe^{−8θ}, at every certified (α, θ). The draft's CERTIFICATES row freezes 12αe^{−4(θ−κ)} and (8489/10000)·12αe^{−8θ}, and its THEOREMS row says that G0 gives "C_0 ⇒ H_1 with δ_1". The 12-forms follow from the 6-forms, so they are valid but loose.
- Instance. At order x⁴ the sum over the polymers that hold ℓ is exactly 6x⁴. The bound through the 12 links of W(e_0) is 12x⁴, and the bound through the 6 links of W′(ℓ) is 6x⁴ (section 5.2, scratch blocks B and C, on 8⁴ and 10⁴). So the factor 2 is exact at leading order.
- Why it is blocking.
  - The critic's blocking item 6 requires "an explicit check that the proved constants are exactly these".
  - v2's G_attack makes a differing proved constant turn every row and clause that rests on it UNSUPPORTED.
  - Both derivations report all_equal = false.
  - The proofs change two frozen formulas.
- What is false as worded. The draft's SCOPE row says "NOT_MET above the windows = a failure of this norm and these counts (Fuss–Catalan growth …)", and v2 keeps that sentence. With the same norm and the same counts, the proved constant gives:
  - C_1 MET at 1/64 with the crude counts, since 2δ′ = 0.10695327 ≤ 1/8;
  - at 1/50, a head-free lower limit 6α_− = 0.03632291 with 2δ′ ≤ 0.07534 ≤ 1/8, which no longer forces NOT_MET. With the C03 head, C_1 and the self-map read MET. This is conditional on C03 and on G1 as drafted.
  - self-map edges at 0.02029/0.02030 (C03 head and head-free) and 0.01556/0.01557 (crude), conditional on G1 as drafted.

  The values come from the KP lens's block E, certified on both sides, and from G0-a §3.11 and G0-b block G. So C11's C_1 clause and C12's C_1 and self-map clauses are artifacts of the factor 12, not of the norm or the counts. For them the SCOPE attribution is false.
- Fix. Re-freeze δ_1 := min over certified (α, θ) of 6αe^{−4(θ−κ)} and T := (8489/10000)·6αe^{−8θ}. Name the test set as W′(ℓ), or as "W(e_0), met at least twice". Recompute the rows listed in the KP lens's B1 and m6, and reword the SCOPE sentence. The alternative is to keep 12 and reword every listed clause, SCOPE included, as a property of the 12-certificate. That alternative leaves the critic's blocking item 6 unmet.

### Minor

- **m1. G0-a Lemma 3.19: "bipartite, since L is even" is false under (H1).**
  - Instance: N = 10 gives L = 5, and the straight winding coarse loop is a 5-cycle (scratch block B).
  - The conclusion, girth at least 4, still holds.
  - Fix: use G0-b's Lemma 3.3(h), or the parity argument of section 1, item 4.
  - The KP lens filed this as its m1. The explicit instance is added here.
- **m2. G0-b §3.14 block B and `G0-b-checks.out`: "8/(3π) ∈ [0.8488264, 0.8488266]" is not an enclosure.**
  - The true value 0.84882636316 lies below 0.8488264.
  - Fix: round outward, to [0.8488263, 0.8488266].
- **m3. Repair: Lemma U closes the lattice independence of the refined head.**
  - Both derivations leave it OPEN (G0-a gap 4, G0-b gap 4), and C03's "DERIVED by locality" has no derivation in either.
  - Lemma U (section 8.2) proves N_w(n) = N_{w̃}^{ℤ⁴}(n) for every even N ≥ 8 and n < 2N, and that N_w(n) depends only on the class of w. The cross-read at N = 10 reproduces C03 through n = 10.
  - Fix: add Lemma U to note section 3. Tag C03's lattice clause DERIVED. State (C4) for the refined head as conditional on the C03 values only. Say that C17's equality of counts for n ≤ 10 follows from the lemma.
- **m4. G0-a §3.12, the CERTIFICATES "C_0 MET" row, and remark 3.10.4.**
  - The cap α ≤ 1/4 never binds, since α_− ≤ 1/8 (G0-b Lemma 3.22). Existence is decided at θ = 1/4, which is on the grid.
  - Fix: cite α_− ≤ 1/8, and mark the row "equal in effect".

The other minor items in this lens are already filed by the KP lens: m2, the false "≤ 0.106953", where the exact value is 0.1069532699; m4, the two forms of the proved δ_1; and m6, the incomplete lists of affected rows. I confirm m2 and m4 and do not repeat them.

## 11. Scratch files (pre-freeze disclosure; not engines, not evidence)

- `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/attack/G0-assembly-checks.py`, with its output at `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/attack/G0-assembly-checks.out`. The blocks are:
  - A: Machin enclosures of π, the G0-a and G0-b lower bounds, 8/(3π), and the 8489/10000 margin;
  - B: the geometry on fine 8⁴ and 10⁴, namely 6 plaquettes per link, W(e_0), W′(ℓ), and the 6 fillings through each coarse link with their meets with W(e_0) and W′(ℓ), together with the coarse girth facts at L = 4 and L = 5;
  - C: the closed sets through one off link of each class up to n = 8, on both lattices, with a winding test by lifting along the adjacency graph, the check #Y″ ≤ #(quarters) ≤ #γ, and the sizes at which Y″ holds a loop.
  
  Run it as `python3 -I G0-assembly-checks.py`. It takes about 2 seconds.
- `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/attack/G0-assembly-checks-n10.out` is the same script run as `python3 -I G0-assembly-checks.py 10`, with block C through n = 10. It takes about a minute.
- sha256: script 42aa29d42e32ba4c04deee2ca652126961c688951e9c28480d4b73a863cb2fe9, n ≤ 8 output 63697af5f99d2893add66ceb3012fab7485717c388de328f992ca858e504390e, n ≤ 10 output f0aa9d0251c3f0c7a577597374fdf372e8fb311f437da7796b764e9b017da811.

Both files use integers and Fractions only. Floats appear only in display. Neither file shares code with `G0-a-checks.py`, `G0-a-kp.py`, `G0-b-checks.py`, `G0-kp-checks.py` or the C03 prototype `closed_sets.py`.
