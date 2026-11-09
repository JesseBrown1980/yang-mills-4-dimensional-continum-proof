# Attack on Theorem G0: the polymers-and-counting lens (second seat)

**Verdict: GAP.** I tried to refute every counting claim of G0 in both derivations. I found no error in the counting lens. Each claim below is confirmed by my own argument and by exact small instances. One item is blocking, and it is carried, not new. Both constant tables report that the proved δ_1 and T are one half of the frozen 12-forms. The critic's blocking item 5 asks for proved constants equal to the frozen ones. That check fails (B1, shared with the Kotecký–Preiss lens). I also supply one repair: N_w(n) depends only on the class of w, and it does not depend on the lattice for n ≤ 2N − 1. Both derivations leave this open (G0-a gap 4, G0-b gap 4 and table row 13).

Read: `derive/G0-a.md` (route A), `derive/G0-b.md` (route B), the draft `ym4-04c/synth/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp` (40 lines), `pkg/PREDICTION-v2.hbp` and `pkg/engine_plan-v2.txt` where they bear on the lens, `wf.json` (critic.blocking, critic.fixes), `attack/G0-kp.md`, and NOTE-YM4-03C §2, §5, §6, §7.5.

Symbols are the binding renames. The Kotecký–Preiss pair is (α, θ), with a(γ) = α·#off(γ) and d(γ) = θ·#γ. The letter a is ½ Re Tr. b = 2. κ = 1/4. D = 20. F(n) := F_20(n) = C(20n, n)/(19n + 1). μ = 20²⁰/19¹⁹. N is the fine side.

No engine ran. The reads in this report come from the scratch files of section 10. They use integers and Fractions only. They are not engines and not evidence. The engine recomputes every value.

## 1. Lemma B closure, and #off(γ) ≤ 2#γ

**Claim.** If a plaquette set γ is not closed, z_γ(V) = 0 for every V. DERIVED (G0-a Lemma 3.4, G0-b Lemma 3.2). I confirm it.

1. Let e be an off link of p ∈ γ that no other plaquette of γ holds.
2. The four links of p are distinct when N ≥ 3. So U_p = A U_e^{±1} B, with A and B free of U_e.
3. Integrate U_e first. Haar invariance gives ∫ K(A u^{±1} B) du = ∫ K dg = 0.
4. No other factor of the integrand holds U_e. So z_γ = 0.

NOTE-YM4-03C §6 states Lemma B for cumulants of multisets, with the exception "supp(M) is one plaquette". That exception does not arise for activities. A one-plaquette activity is z_{p} = ∫ K = 0, by the same step. So the activity form needs only step 3. DERIVED.

**Claim.** #off(γ) ≤ 2#γ for a closed γ. DERIVED (G0-a Lemma 3.5, G0-b Lemma 3.4). I confirm it. Count pairs (e, p) with e ∈ off(γ), p ∈ γ, e ∈ p. Closure gives at least 2 pairs per off link. A plaquette has at most 4 off links. So 2#off(γ) ≤ 4#γ. The bound is sharp: a unit cube whose fourth coordinate is odd has 6 faces and 12 off edges, each edge in 2 faces.

**Small closed sets.** The closed off-link-connected sets of at most 4 plaquettes are exactly the fillings, and none has 3 or fewer. DERIVED in both routes. My closure-driven search reads N_c(1..4) = (0, 0, 0, 1) for class 1 and (0, 0, 0, 0) for classes 2 and 3 (section 6).

## 2. Finner's inequality with exponent 6

**Is 6 the right exponent?** Yes. In d = 4 a link lies in 2(d − 1) = 6 plaquettes. The census reads 6 for every link on fine (ℤ/8)⁴ and (ℤ/10)⁴. So Σ_{p∋e, p∈γ} 1/6 ≤ 1 at every off link e of every γ. DERIVED.

**Is 6 forced as a common exponent?** Yes. Take a class-1 off link e and three unit cubes that contain e, chosen so that each of the 6 plaquettes at e is a face of exactly one of them. The union is a closed, off-link-connected polymer of 18 plaquettes. Its link e lies in all 6 of them (scratch read, `G0-count-sixcube.out`). With a common exponent q < 6, the hypothesis Σ 1/q ≤ 1 fails at e. This confirms G0-a's remark after Lemma 3.8.

**Does the inequality apply to the Haar integral of a product of K over a polymer?** Yes. I check each hypothesis.

1. The measure is product Haar measure on the off links of γ. Each factor is a probability space. The other off links integrate to 1.
2. f_p := |K(U_p)|, with the line links held at (1, V_ℓ) as parameters, is a measurable function of the off links of p only.
3. |z_γ(V)| ≤ ∫ Π_p f_p. Finner gives ∫ Π_p f_p ≤ Π_p ‖f_p‖_{L⁶(off(p))}.
4. Fix all off links of p but one, u. Then U_p = A u^{±1} B is Haar distributed. By Fubini, U_p is Haar distributed under the product measure on off(p). So ‖f_p‖_6 = (∫ K⁶ dg)^{1/6} = ε_6.
5. The form with "≤ 1" follows from Finner's "= 1" by padding with constant factors 1 on single links, as both routes say.

So sup_V |z_γ(V)| ≤ ε_6^{#γ}. DERIVED, with Finner (1992) REPORTED.

**A note on the planted fault finner_exponent_2.** Take C19's 10-plaquette set: a filling F_P plus a unit cube that shares one internal link e of F_P. The census reads it closed and connected, with e in 4 of its plaquettes and every cube edge an off link. Its leading activity is DERIVED from the merge rule of NOTE-YM4-03C §7.5:

- every factor starts at n = 2, so the lowest order is β¹⁰, with spin ½ on all 10 plaquettes;
- three merges in F_P give (1/8)χ½ of a word in which e and e⁻¹ are adjacent, so the filling no longer depends on e;
- the closed cube then integrates to 2^{−4} = 1/16;
- so z_γ(V) = (2t_2)¹⁰ χ½(V_P)/128 plus terms of order β¹² and higher, and sup_V |z_γ| = (2t_2)¹⁰/64 at leading order.

Also ‖K‖_2² = Σ_{n≥2} n² t_n² ≥ 4t_2², so ‖K‖_2 ≥ 2t_2. So on this set the false L² product (2t_2)¹⁰ still bounds |z_γ| at leading order, with a factor 64 to spare. The fault cannot be caught here by comparing numbers. It can be caught only by a guard on the hypothesis: incidence 4 at e and 4·(1/2) = 2 > 1. C19 names exactly such a guard, G_finner_guard. The engine plan should say that the guard reads the incidence, not an inequality.

## 3. The BFS injection into the complete 20-ary tree

**Is D = 20 the right degree for off-link connectivity?** Yes. Join two plaquettes when they share an off link. Each off link of p lies in 5 other plaquettes. Two distinct plaquettes share at most one link. So distinct off links of p give distinct neighbours, and deg(p) = 5·#off(p). That is 20 for the plaquettes with 4 off links and 10 for the quarters. DERIVED (G0-a Lemma 3.1 item 7, G0-b Lemma 3.3(f)). The census on (ℤ/8)⁴ and (ℤ/10)⁴ reads minimum 10, maximum 20, all neighbours distinct, and deg = 5·#off at every plaquette.

**Is the injection right, and is the root counted correctly?** Yes. My argument:

1. At each vertex u fix an injective labelling of its neighbours by {1, …, 20}.
2. For a connected set A ∋ v, any deterministic spanning-tree rule from v works, BFS among them. Place each newly reached vertex u′ in the child slot of u labelled by u′.
3. The result is a subtree of the complete 20-ary tree that contains the root and has #A nodes.
4. The subtree alone rebuilds A: the root goes to v, and the child in slot i of a node that goes to u goes to the neighbour of u labelled i. So the map is injective.
5. The root has 20 slots, which covers deg(v) ≤ 20. A non-root vertex needs at most 19 slots, since one neighbour is its parent. Giving it 20 overcounts and keeps the bound valid.

So the connected sets of n plaquettes that contain a given plaquette number at most F_20(n). DERIVED.

**Does 6F_20(n) bound every off-link-connected set holding a given off link?** Yes. A set holds w exactly when it contains one of the 6 plaquettes through w. The union bound over these 6 roots gives at most 6F_20(n). It bounds all connected sets, closed or not, and so N_w(n) ≤ 6F_20(n). DERIVED. This is exactly C01's injection clause, which v2's G_attack lists as resting on G0(c).

**Exhaustive counts (critic fix 4).** On fine (ℤ/8)⁴, two routes (Redelmeier recursion, and brute-force extension with set dedup for class 1 through n = 5) give the same numbers. Scratch reads, not evidence:

| n | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| through a quarter | 1 | 10 | 167 | 3353 | 73082 | 1670630 |
| through a plaquette with 4 off links | 1 | 20 | 422 | 9434 | 218955 | 5212502 |
| F_20(n) | 1 | 20 | 590 | 20540 | 784245 | 31763004 |
| holding a class-1 off link | 6 | 85 | 1648 | 35478 | 805720 | 18911721 |
| holding a class-2 off link | 6 | 105 | 2138 | 47232 | 1090108 | 25860281 |
| holding a class-3 off link | 6 | 105 | 2282 | 52200 | 1229316 | 29531685 |
| 6F_20(n) | 6 | 120 | 3540 | 123240 | 4705470 | 190578024 |

Every count is at or below its bound. At n = 2 the per-root bound is attained (20 = F_20(2)). The per-link ratio to 6F_20(n) falls from 1 at n = 1 to 0.0992, 0.1357 and 0.1550 at n = 6 for classes 1, 2 and 3. The n ≤ 4 values agree with G0-b §3.14 block E. n = 2 checks by hand: class 1 gives 2·10 + 4·20 − C(6, 2) = 85, and classes 2 and 3 give 6·20 − 15 = 105.

**A note on the planted fault degree_19.** With D = 19, the per-link counts stay below 6F_19(n) = 6, 114, 3192, 105450, 3820254, 146803272 for n ≤ 6. So a per-link count comparison does not catch D = 19 in reach. The per-root count catches it at n = 2 (20 > F_19(2) = 19), and so does the degree census (maximum 20). C19 sends degree_19 to C01, whose degree clause fires. A count row added under critic fix 4 would not fire on that fault by itself.

## 4. The Fuss–Catalan count and the ratio, for all n

**The count.** The rooted subtrees of the complete D-ary tree with n nodes number F_D(n) = C(Dn, n)/((D − 1)n + 1) = C(Dn, n − 1)/n. DERIVED twice: G0-a by the cycle lemma, G0-b by Lagrange inversion of T = z(1 + T)^D. I rechecked G0-a's cycle-lemma step. A shift that starts after index r is valid exactly when P_m ≥ P_r for r < m ≤ n − 1 and P_m − 1 ≥ P_r for 0 ≤ m < r. That says r is the first minimizer of P over {0, …, n − 1}. A word with total −1 has no period shorter than n, so the shift map is a bijection. Hand check: F_20(3) = 590 = C(20, 2) + 20·20. Exact reads: F_20(4..12) equal the nine values frozen in C01, and C(Dn, n − 1)/n = F_D(n) for n ≤ 299.

**The ratio.** For every integer n ≥ 0,

```text
F(n+1)/F(n) = 20 * prod_{j=1}^{19} (20n + j)/(19n + j + 1).
```

Each factor f_j(n) is strictly increasing, since 20(19n + j + 1) − 19(20n + j) = j + 20 > 0. Each is strictly below 20/19, since 20/19 − f_j(n) = (j + 20)/(19(19n + j + 1)) > 0. So the ratio is strictly increasing and strictly below 20·(20/19)¹⁹ = μ, for every n. It tends to μ. DERIVED (G0-b Lemma 3.10). G0-a's real-variable proof is also correct: the offsets sort as i/D < (i + 1)/(D − 1) for i ≤ D − 2, (D − 1)/D < 1 and 1 < D/(D − 1). Exact reads: the product formula equals F(n + 1)/F(n) for n ≤ 200, and the ratio is strictly increasing and below μ for n ≤ 1500. The bracket μ ∈ [53.00068, 53.00069] is the integer inequality 5300068·19¹⁹ ≤ 100000·20²⁰ ≤ 5300069·19¹⁹, which holds.

C01 checks the ratio for n ≤ 59 only. Both proofs cover every n.

## 5. The tail bound 6F_20(49)x⁴⁹/(1 − μx)

**Claim.** For 0 ≤ x with μx < 1, Σ_{n≥49} 6F(n)xⁿ ≤ 6F(49)x⁴⁹/(1 − μx). DERIVED. Section 4 gives F(49 + j) ≤ F(49)μ^j. So 6F(49 + j)x^{49+j} ≤ 6F(49)x⁴⁹(μx)^j. Sum the geometric series. The frozen split, the explicit sum to n = 48 and the tail from n = 49, has no gap and no double count. Exact read: F(n)·19^{19(n−49)} ≤ F(49)·20^{20(n−49)} for n = 49..1200.

**The pole.** The tail formula is negative for μx > 1. An engine that evaluated it there could read a false MET. v2's engine plan already says that S is undefined, and the read NOT_MET, when μx ≥ 1. For the upper enclosure the test must be μ·x⁺ < 1 with the exact rational μ (or μ⁺ = 53.00069) and the upper enclosure x⁺, and the tail must use 1 − μx⁺ in its denominator. Minor pinning.

**C04 is right at equality.** C04 states x = ε_6 e^{2α+θ} > ε_6 e^{1/4} for every α > 0 and θ ≥ 1/4. So if μ e^{1/4} ε_6 ≥ 1, then μx > 1 strictly. The terms 6F(n)xⁿ = 6F(n)μ^{−n}(μx)ⁿ then grow without bound, since F(n)μ^{−n} decays only like n^{−3/2}. So the tail diverges at equality too. G0-b's remark after Corollary 3.11 and its gap 8 say C04 is wrong at equality. They miss the strict inequality x > ε_6 e^{1/4}. See finding M2.

## 6. The closed-set counts: class rule and locality (repair)

The refined head needs N(n) ≥ N_w(n) for every off link w, on every lattice in use. Both derivations leave two points open. I derive both.

**Lemma L1 (the class rule).** Let N be even. N_w(n) depends only on the class of w. DERIVED.

*Proof.* Consider the maps x ↦ σ(x) + t, with σ a signed permutation of the four coordinates and t ∈ (2ℤ/Nℤ)⁴. They are automorphisms of (ℤ/N)⁴ because N is even. They carry the parity of each coordinate to the parity of its image coordinate. So they map line links to line links and class-c off links to class-c off links. They map plaquettes to plaquettes and preserve "share an off link", closure and connectivity. So N_w(n) = N_{gw}(n) for every such g. They act transitively on the class-c links. Take a class-c link (x, λ) with odd transverse set O. A coordinate permutation moves λ and O to fixed positions. An even translation brings x to x_r = [r ∈ O] for r ≠ λ and x_λ ∈ {0, 1}. The reflection x_λ ↦ −x_λ, then translation by 2e_λ, maps the link with x_λ = 0 to the one with x_λ = 1. ∎

Scratch reads: 8 link types per class (types by direction, odd set and parity along the link; there are 24, 24 and 8 types in classes 1, 2 and 3) give one count vector per class through n = 8. The stabilizer of a class-1 link has order 16.

**Lemma L2 (winding costs 2N plaquettes).** Call [c, c + 1] the μ-range of a plaquette whose plane holds μ, and {c} the μ-range of any other plaquette. Let γ be a closed set of plaquettes, in ℤ⁴ or in (ℤ/N)⁴ with slabs read mod N. If the μ-ranges of γ cover N distinct slabs [c, c + 1], then #γ ≥ 2N. DERIVED.

*Proof.* Let p ∈ γ have μ-range [c, c + 1], in the plane (μ, ν). Its two μ-links sit at ν-coordinates of opposite parity. A line link needs every transverse coordinate even, so at most one of the two is a line link. The other, f, is an off link. Closure puts f in a second plaquette of γ. That plaquette holds a μ-link, so its μ-range is [c, c + 1] too. Plaquettes whose ranges are different slabs are different. So γ has at least 2 plaquettes per covered slab. ∎

**Lemma L3 (locality).** Let N be even with N ≥ 8, n ≤ 2N − 1, w an off link of (ℤ/N)⁴ and w̃ a lift of w to ℤ⁴. The projection π is a bijection from the closed off-link-connected sets of n plaquettes of ℤ⁴ that hold w̃ onto those of (ℤ/N)⁴ that hold w. So N_w(n) equals the ℤ⁴ count, for every such N. DERIVED.

*Proof.* Two plaquettes that share a link have intersecting μ-ranges. So along a path in the off-link graph the union of the μ-ranges is connected. A connected union of unit intervals and points that contains two points at distance at least N covers N consecutive slabs.

1. *π is injective on each ℤ⁴ set Ã.* If p̃′ = p̃ + Nv with v_μ ≠ 0, a path in Ã from p̃ to p̃′ covers N consecutive slabs. Lemma L2 in ℤ⁴ gives #Ã ≥ 2N > n. So π(Ã) has n plaquettes. It is closed, since each off link of π(Ã) lifts to an off link of Ã held by two plaquettes with distinct images. It is connected and holds w.
2. *Every torus set lifts.* Let γ hold w, with #γ = n. Lift γ along a spanning tree of its off-link graph, starting from a plaquette through w lifted to hold w̃. Let p, q ∈ γ share an off link f. Suppose their lifts hold lifts of f that differ by Nv with v ≠ 0, and pick μ with v_μ ≠ 0. The μ-range of p̃ contains that of f̃, and the μ-range of q̃ contains that of f̃ + Nv. So the tree path from p̃ to q̃ covers N consecutive slabs, and its image covers all N slabs mod N. Lemma L2 on the torus gives #γ ≥ 2N > n. So every shared off link lifts to a shared off link. The lift γ̃ is then closed and connected in ℤ⁴, holds w̃, and π(γ̃) = γ.
3. *The lift is unique.* Let Ã be any ℤ⁴ set of n plaquettes with π(Ã) = γ. The argument of step 2, run along a path inside Ã, shows that two plaquettes of Ã whose images share an off link f hold the same lift of f. So Ã is fixed by the lift of one of its plaquettes, and two such sets differ by a translation Nu. In each of them, all plaquettes whose images hold w hold one common lift of w. If both sets hold w̃, that common lift is w̃ in both, and u = 0. ∎

**Consequence.** For n ≤ 15 the counts are the same on every fine torus (ℤ/N)⁴ with N even and N ≥ 8. So the refined head n ≤ 10, and C03's growth readout n = 11, 12, are lattice independent. This closes G0-a gap 4, G0-a §3.9 ("lattice independent only through C03's locality claim") and G0-b gap 4 and table row 13, up to the counts themselves. The counts stay a CONJECTURE until the engine and the check read them. C03's parenthetical "DERIVED by locality: no set of fewer than 16 plaquettes winds at fine side 8" is Lemma L2. It also needs steps 1 to 3 of Lemma L3, which it does not state.

**Scratch cross-read of the C03 head.** Closure-driven growth seeded at the 6 plaquettes through one off link: a closed set may add any off-link neighbour, and an open set must close its lowest open off link. Visited sets are deduplicated as sets. Every closed connected set holding the link is reached, by induction on a growth order inside it. Reads on fine (ℤ/8)⁴ and on fine (ℤ/10)⁴, whose coarse side 5 is odd:

| class | N_c(4..10) here | C03 frozen N_c(4..10) |
|---|---|---|
| 1 | 1, 0, 12, 0, 32, 32, 304 | 1, 0, 12, 0, 32, 32, 304 |
| 2 | 0, 0, 12, 0, 12, 12, 240 | 0, 0, 12, 0, 12, 12, 240 |
| 3 | 0, 0, 12, 0, 0, 0, 216 | 0, 0, 12, 0, 0, 0, 216 |

The two lattices agree, as Lemma L3 says. In every class the 12 sets at n = 6 are the 12 unit cubes through the link (`G0-count-cubes.out`). This is a cross-read before the freeze, not a blind prediction.

**Sets, not orbits.** Under the 16-element stabilizer of a class-1 link, its 1, 12 and 32 closed sets at n = 4, 6 and 8 fall into 1, 2 and 4 orbits. So C03's numbers count sets. C03's method says "dedup by canonical form under coarse translations x the 384 signed permutations". Read literally, that counts symmetry classes, which would give a head below N_w(n) and an invalid S. See finding M4.

## 7. #Y″(γ) ≤ #γ, V-dependence at size ≥ 4, and the readout exclusion

**#Y″(γ) ≤ #γ.** DERIVED in both routes. Only quarters hold line links, 2 each. Each coarse link of Y″(γ) takes 2 distinct held line links. So 2#Y″(γ) ≤ 2·#(quarters of γ) ≤ 2#γ. I confirm it.

**#Y ≥ 4 for every Y that holds a closed loop.** True for coarse side L ≥ 4. A loop that does not wind has even length at least 4. A winding loop has length at least L. G0-b Lemma 3.3(h) argues it this way. G0-a Lemma 3.19 says the coarse torus is bipartite "since L is even". That is false when N ≡ 2 (mod 4). For example N = 10 is allowed by G0-a (H1), and its coarse torus (ℤ/5)⁴ has winding loops of length 5. The conclusion still holds. See finding M1.

**The readout exclusion.** A closed polymer γ ≠ F_P that holds all 8 line links of ∂P has #γ ≥ 8, and so does every cluster X ≠ {F_P} with ∂P ⊆ Y(X). DERIVED in both routes, by different case splits. I rechecked both. In G0-a case 1 ≤ k ≤ 3 the bound is #γ ≥ (8 − k) + 3 ≥ 8. G0-b's table gives 8, 10, 11, 12 and 12 for m = 3, 2 (adjacent), 2 (opposite), 1 and 0. Scratch read on (ℤ/8)⁴: closed sets of at most 8 plaquettes holding all of ∂P number 1 at n = 4 (F_P) and 16 at n = 8, none at 5, 6 or 7, as G0-b §3.14 block D reads.

## 8. The constant tables against the draft

Lens rows. "Frozen" is the 40-line draft. Every entry agrees.

| Item | Frozen | G0-a | G0-b | This attack |
|---|---|---|---|---|
| plaquettes per link, Finner exponent | 6, 6 | 6, 6 (yes) | 6, 6 (yes) | 6 on 8⁴ and 10⁴; 6 forced (18-plaquette polymer) |
| D, minimum degree | 20, 10 | 20, 10 (yes) | 20, 10 (yes) | 20, 10 on 8⁴ and 10⁴ |
| #W(e_0) | 12 | 12 (yes, as geometry) | 12 (yes) | 12 at every line link; 1 off link at m_ℓ per plaquette, so #W′(ℓ) = 6 |
| link classes on 8⁴ | 2048, 6144, 6144, 2048 | — | same | same |
| filling membership | class 1 in 1, classes 2, 3 in 0 | yes | yes | yes |
| closed sets ≤ 4 | fillings only | yes | yes | yes |
| injection bound | 6F_20(n) for all connected sets | yes | yes | yes; counts to n = 6 below it |
| F_20(4..12) | nine values | reproduce | reproduce | reproduce |
| μ | [53.00068, 53.00069] | yes | yes | yes |
| ratio | increasing, below μ, n ≤ 59 | "no: proof stronger" | "formula yes" | proved for all n; label differs (M8) |
| tail | 6F_20(49)x⁴⁹/(1 − μx) | yes | yes | yes |
| #off(γ) ≤ 2#γ | yes | yes | yes, sharp | yes, sharp |
| #Y″(γ) ≤ #γ | yes | yes | yes | yes |
| C03 head | CONJECTURE | n = 4 proved | CONJECTURE | n ≤ 10 reproduced in scratch; lattice independence DERIVED (L1–L3) |
| C03 counting gap n = 8, 10, 12 | [1.09e10, 1.10e10], [2.31e12, 2.33e12], [6.49e14, 6.50e14] | — | — | 1.0928e10, 2.3200e12, 6.4941e14 |
| C03 N(10)/N(8), N(12)/N(10) | 19/2; 1163/152 in [7.65, 7.66] | — | — | 19/2; 1163/152 = 7.6513 |
| C03 "F_20(n+2)/F_20(n) > 2000" | no n stated | — | — | true from n = 8 on only (M3) |
| E\|χ½\| | 8/(3π) ≤ 8489/10000 | π > 333/106 | π ≥ 1231847548/392109375 | both bounds exact; 848/999 < 8489/10000 |

Rows outside the lens. Both tables mark δ_1 and T as "no", with the draft weaker by exactly 2. Both mark the rows that inherit them (C07, C08, C09's T, C11 to C14, C16, the regime text) as "no". I found no row marked "yes" that should read "no". The halved readout brackets of G0-b row 40 contain G0-a's values (5.2259e-4, 8.3611e-3, 0.13383, 0.55725, 6.9352e3). The 12-form arithmetic reproduces in G0-a §3.11, in G0-b block F, in the critic's fix 10 and in the Kotecký–Preiss attack. I did not recompute it.

## 9. Findings

### Blocking

**B1 (carried; shared with the Kotecký–Preiss lens, its B1).** The proved δ_1 and T are one half of the frozen ones.

- Frozen: δ_1 := min 12α e^{−4(θ−κ)} and T := (8489/10000)·12α e^{−8θ}.
- Proved by both routes: δ_1 := min 6α e^{−4(θ−κ)} and T := (8489/10000)·6α e^{−8θ}.
- Source, confirmed by census at every line link of 8⁴ and 10⁴. Each of the 6 plaquettes through e_0 has its 2 off links in W(e_0). Exactly one of them ends at the midpoint m_ℓ. So a holding polymer meets W(e_0) at least twice, and W′(ℓ) at least once, with #W′(ℓ) = 6.
- Why it blocks. Critic blocking item 5 asks for an explicit check that the proved constants are exactly the frozen ones. v2's G_attack makes "a proved constant that differs from a frozen one" turn every row resting on it UNSUPPORTED. Both tables report all_equal = false.
- What it is not. It is not a validity error. The frozen 12-forms follow from the proved 6-forms.
- Fix. The owner chooses. (a) Re-freeze with 6 and recompute the inheriting rows (edges 0.01556/0.01557 crude and 0.02029/0.02030 refined, as both routes read). (b) Keep 12, and reword each NOT_MET clause that rests on it as a property of the 12-certificate, with C12's two DERIVED tags included.

### Minor

- **M1 (G0-a Lemma 3.19).** "Bipartite, since L is even" is false for N ≡ 2 (mod 4), which (H1) allows. Example: N = 10 has a coarse torus (ℤ/5)⁴ with winding loops of length 5. The conclusion #Y ≥ 4 holds. Fix: "a loop that does not wind has even length at least 4; a winding loop has length at least L ≥ 4", as in G0-b Lemma 3.3(h).
- **M2 (G0-b remark after Corollary 3.11, and gap 8).** The claim that C04 is wrong at equality is itself wrong. C04 has x > ε_6 e^{1/4} strictly for α > 0, so μx > 1 strictly whenever μ e^{1/4} ε_6 ≥ 1, and the tail diverges. Fix: drop the remark, or keep only the true part: the series Σ F(n)μ^{−n} converges, and its geometric bound does not.
- **M3 (C03 wording).** "Against F_20(n+2)/F_20(n) > 2000" holds only for n ≥ 8. The values are 1546.40, 1708.96, 1834.88, 1935.16 at n = 4 to 7 and 2016.84 at n = 8. Fix: "against F_20(10)/F_20(8) and F_20(12)/F_20(10), both above 2000".
- **M4 (C03 method wording).** The head must count the sets holding the seed link, not their classes under symmetry. The class-1 counts 1, 12, 32 at n = 4, 6, 8 are 1, 2, 4 orbits under the stabilizer of the link. Fix: say that canonical forms deduplicate search states only, and that each class is weighted by the number of its members holding the seed link. C03's own falsifier would catch an orbit count, so this is wording, not a hidden error.
- **M5 (repair, both routes).** Lemmas L1 to L3 (section 6) derive that N_w(n) depends only on the class of w, and that for n ≤ 2N − 1 it does not depend on N. Fix: add them to note section 3. Then the refined G0 is conditional on C03's counts only, not on their extension to every lattice. Add Lemma L3's injectivity steps to C03's DERIVED parenthetical.
- **M6 (C19 finner_exponent_2).** On the named 10-plaquette set the false L² product still bounds the activity at leading order: sup |z_γ| = (2t_2)¹⁰/64 against ‖K‖_2¹⁰ ≥ (2t_2)¹⁰. The fault is visible only to a hypothesis guard. Fix: state in the engine plan that G_finner_guard reads the maximal off-link incidence (4 on that set) and tests Σ 1/q ≤ 1.
- **M7 (C19 degree_19, and critic fix 4).** A per-link count row does not catch D = 19 for n ≤ 6, since every per-link count stays below 6F_19(n). The degree census and the per-root count at n = 2 do. Fix: if the count row of critic fix 4 is added, freeze the per-root counts too, or keep the degree clause as the named detector. The counts of section 3 can be frozen as cross-reads (prefreeze = CROSS_READ).
- **M8 (tables).** The ratio row is "no: the proof is stronger" in G0-a and "formula yes" in G0-b. Fix: one label, "yes; proved for every n".
- **M9 (G0-a notation).** S names both the count-vector power series of (H3) and the frozen closed form. They differ at μx = 1: the crude power series converges there, and the frozen form is +∞. Fix: name them S_N and S_frozen in (C2), (C3) and Corollary 3.12.
- **M10 (pole pinning).** The tail term needs the test μ·x⁺ < 1 with the exact μ (or μ⁺) and the upper enclosure x⁺, and 1 − μx⁺ in the denominator. v2's engine plan states the rule "undefined, NOT_MET, when μx ≥ 1" without the enclosure direction. Fix: state it.

## 10. Scratch files (not engines, not evidence)

All under `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/attack/`. Integers and Fractions only; floats appear in display only.

- `G0-count-checks.py`: blocks A (Fuss–Catalan, μ, ratio for n ≤ 1500, product formula, tail for n ≤ 1200, counting gaps), B (geometry on fine 8⁴ and 10⁴), C (connected-set counts), D (closed-set counts, both lattices), E (readout exclusion), F (filling-plus-cube set). Outputs `G0-count-checks.out` (arguments 5 8) and `G0-count-checks-6-10.out` (arguments 6 10, about 33 s).
- `G0-count-cross.py`, output `G0-count-cross.out`: brute-force class-1 connected counts for n ≤ 5, and closed counts at 8 link types per class.
- `G0-count-orbits.py`, output `G0-count-orbits.out`: the stabilizer of a class-1 link and the orbits of its closed sets at n = 4, 6, 8.
- `G0-count-sixcube.py`, output `G0-count-sixcube.out`: the 18-plaquette polymer with incidence 6.
- `G0-count-cubes.py`, output `G0-count-cubes.out`: the closed 6-sets holding an off link of each class are the 12 unit cubes through it.

### References

- H. Finner, A generalization of Hölder's inequality and some probability inequalities, Ann. Probab. 20 (1992) 1893–1901. REPORTED.
- A. Dvoretzky and Th. Motzkin, A problem of arrangements, Duke Math. J. 14 (1947) 305–313. Cycle lemma, cross-reference.
- R. P. Stanley, Enumerative Combinatorics, vol. 2, Cambridge University Press (1999), §5.4. Lagrange inversion, REPORTED.
- D. H. Redelmeier, Counting polyominoes: yet another attack, Discrete Math. 36 (1981) 191–203. The enumeration algorithm of the scratch check, cross-reference.
- Repo: NOTE-YM4-03C-BLOCKED-ACTION.md §2 (Lemma A), §5 (sides), §6 (Lemma B), §7.5 (the merge rule for disks); NOTE-YM4-03-ONE-SCALE-BLOCKING.md Theorem 8 (the merge rule).
