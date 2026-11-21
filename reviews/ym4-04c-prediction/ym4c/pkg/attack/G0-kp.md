# Attack on Theorem G0: the Kotecký–Preiss lens (second seat)

**Verdict: GAP.** I found no error in the Kotecký–Preiss step of G0, in either derivation. The criterion, the incompatibility relation, the test set and the per-polymer corollary all hold. I confirm each with my own argument below. Two items are blocking, and neither is a flaw in the proof. (B1) The proof's δ_1 and T are one half of the frozen 12-forms. v2's own gate G_attack then makes every row that rests on them read UNSUPPORTED. (B2) v2's THEOREMS row writes the corollary with the weight e^{d(γ)}. The weight must be e^{d(C)}. Section 7 lists the minor items.

Read: `derive/G0-a.md` (route A, KP as REPORTED plus a marker corollary), `derive/G0-b.md` (route B, the Penrose tree-graph route), the draft `ym4-04c/synth/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp`, `pkg/PREDICTION-v2.hbp`, `wf.json` (critic.blocking, critic.fixes), and NOTE-YM4-03C §2, §4, §6. Symbols are the binding renames. The KP pair is (α, θ), with a(γ) = α·#off(γ) and d(γ) = θ·#γ. a is ½ Re Tr. b = 2. κ = 1/4. For a cluster C, d(C) = Σ_{γ∈C} m_C(γ) d(γ) = θ·n(C).

No engine ran. The exact reads in section 6 come from the scratch files of section 8. Those files use integers and Fractions with outward dyadic rounding at 320 bits. They are not evidence. The engine recomputes every value.

## 1. (i) The per-polymer KP criterion holds with a(γ) = α#off(γ), d(γ) = θ#γ

DERIVED, in G0-a Lemma 3.15 and G0-b Corollary to Proposition 3.15. My argument follows.

1. Fix a closed polymer γ. A polymer γ′ is incompatible with γ exactly when off(γ′) ∩ off(γ) ≠ ∅. So γ′ holds some w ∈ off(γ).
2. Closure gives 2#off(γ′) ≤ Σ_{p∈γ′} #off(p) ≤ 4#γ′. So a(γ′) ≤ 2α#γ′.
3. Finner with exponent 6 gives sup_V |z_{γ′}| ≤ ε^{#γ′}, with ε = ε_6(β_0). So |z_{γ′}| e^{a(γ′)+d(γ′)} ≤ x^{#γ′}, with x = εe^{2α+θ}.
4. For one off link w, Σ_{γ′ ∋ w} x^{#γ′} = Σ_n N_w(n) xⁿ ≤ S(x) when the count vector is valid.
5. The union bound over w ∈ off(γ) gives LHS(KP at γ) ≤ #off(γ)·S(x). This is at most α#off(γ) = a(γ) when S(x) ≤ α.

The criterion is additive over off links. So checking it at every polymer is the same as checking the one scalar inequality S(x) ≤ α. The frozen certificate checks exactly that inequality. a(γ) ≥ 2α > 0, since every plaquette has at least 2 off links. Step 2 is sharp: the cube with fourth coordinate odd has #off = 12 = 2·6 (G0-b, after Lemma 3.4).

## 2. The incompatibility relation is right

DERIVED. The relation is "share an off link". It is reflexive and symmetric. My argument for why it is the right one:

- Every line link is fixed in the line gauge, at (1, V_ℓ). Every off link is integrated by product Haar measure. So two plaquette sets with no common off link are functions of disjoint sets of independent variables, and E_V factors over them.
- Expand Π_p (1 + K_p) over plaquette sets S. Split S into its components under "share an off link". The components are polymers, they are pairwise compatible, and E_V factors over them. Conversely, the components of the union of a compatible family are its members. Two compatible polymers share no plaquette, since every plaquette has 2 or 4 off links. So the map is a bijection.
- Lemma B (NOTE-YM4-03C §6, rule (a)) removes every non-closed component, since it integrates to 0. Removing it does not change the relation among the closed polymers.

Instance. Take the two fillings F_Q and F_{Q′} of two coarse plaquettes through ℓ. They share e_0(ℓ) and e_1(ℓ) and no off link, since internal links of distinct fillings are disjoint (G0-a Lemma 3.1 item 4). They are compatible, and E_V[K_{F_Q} K_{F_{Q′}}] = z_{F_Q} z_{F_{Q′}} exactly, because the line links are not integrated. NOTE-YM4-03C §7.5 says the same: "fillings of two coarse plaquettes share line links only and are compatible".

## 3. (ii) The per-polymer corollary follows

The corollary is Σ_{C ∋ γ} |Φ(C)| e^{d(C)} ≤ |z_γ| e^{a(γ)+d(γ)}. DERIVED. I check three routes.

**Reweighting reduces it to the d-free form.** Put z′(γ) := z(γ)e^{d(γ)}. Then Φ(C; z′) = Φ(C; z) e^{d(C)}, because d(C) is additive with multiplicity. The KP hypothesis with (a, d) at z is the KP hypothesis with (a, 0) at z′. So the d-form of every KP statement follows from the d-free form. In particular, Theorem 3.13 of G0-a does not need d in its hypothesis as a separate REPORTED feature.

**G0-a's marker proof (Corollary 3.14) is correct.** Adjoin γ̂ with z(γ̂) = 0, d(γ̂) = 0, a(γ̂) = Σ_{γ∈Γ_0} |z|e^{a+d} + η. Make it incompatible with itself and with Γ_0. KP at γ̂ holds by construction. KP at every γ ∈ Γ gains only the term |z(γ̂)|e^{…} = 0. A cluster that holds γ̂ has Φ = 0. Every other cluster is a cluster of Γ with the same Φ, because the incompatibility graph restricted to Γ is unchanged. The conclusion at γ̂ is the claim, up to η → 0.

**G0-b's route (Proposition 3.15) is correct and self-contained.** It needs no REPORTED KP theorem. I rechecked three steps:
- the rooted-tree recursion M_{h+1}(γ) = exp(Σ_{γ′≁γ} ω(γ′)M_h(γ′)), including the count (n−1)!/(k!Π(m_j−1)!);
- the induction M_h ≤ e^{α#off(γ)} through the union bound over off(γ);
- the step from Σ_{X∋e} to n·Σ_{γ_1∋e}.

It gives Σ_{X∋e} (1/n!)|φ^T| Π ω ≤ Σ_{γ∋e} ω(γ)e^{α#off(γ)} ≤ S(x), with ω = sup|z|e^{θ#γ}. That is the corollary summed over the polymers through e. The Penrose partition (Lemma 3.13) is right. The Boolean intervals [τ, R(τ)] partition the connected spanning subgraphs.

Instance (tightness of the shape). Take one self-incompatible polymer with u := |z|e^{d} and ue^{a} ≤ a. The clusters are {γ^m} with |Φ| e^{d(C)} = u^m/m, so the sum is −log(1−u). Put f(u) = ue^{a} + log(1−u). Then f(0) = 0 and f′(u) = e^{a} − 1/(1−u) ≥ 0 for u ≤ 1 − e^{−a}. Also ae^{−a} ≤ 1 − e^{−a}, since (1+a)e^{−a} ≤ 1. So −log(1−u) ≤ ue^{a} on the KP region. Equality holds only at u = 0.

## 4. (ii) The test set W(e_0) controls every Y through ℓ, with a factor 2 to spare

DERIVED. Fix a coarse link ℓ. Suppose ℓ ∈ Y(X). Then some γ ∈ X holds both positions of ℓ, so it holds a plaquette p through e_0(ℓ). p is a quarter. Its 2 off links both lie in W(e_0), and both lie in off(γ). So:

- X meets W(e_0) in at least 2 links. The union bound over the 12 links of W(e_0) counts X at least twice. That gives 12α as the frozen value and 6α as the honest output (G0-b Lemma 3.19).
- p has exactly one off link at m_ℓ. So X meets W′(ℓ), the 6 off links at m_ℓ, at least once. This also gives 6 (G0-a Lemma 3.16).
- No cover beats 6 for this method. The 6 fillings through ℓ hold ℓ and have pairwise disjoint off-link sets. So any fractional cover by test links has total weight at least 6.

Lemma A (NOTE-YM4-03C §2) is used per polymer. That is right, because Φ(X; V) is φ(X) times a product of activities. Take a cluster in which one polymer holds only e_0(ℓ) and another only e_1(ℓ). It has ℓ ∉ Y(X), and it is constant in V_ℓ. So "ℓ ∈ Y(X)" is the exact condition for a cluster to enter the norm at ℓ.

Exact checks (scratch `G0-kp-checks.py`, block A). On fine (ℤ/8)⁴, at all 1024 coarse links:
- #W(e_0) = 12, and both off links of each plaquette through e_0 lie in W(e_0);
- each of the 12 plaquettes through e_0 or e_1 has exactly one off link in W′(ℓ);
- the 6 off-link pairs through e_0 are pairwise disjoint;
- each of the 6 fillings through ℓ holds e_0 and e_1, exactly 2 links of W(e_0) and exactly 1 of W′(ℓ).

Exact instance (block B). In the gas of fillings alone, every cluster through ℓ is {F_Q^m} with Q ∋ ℓ. Each such cluster holds exactly 2 links of W(e_0). The ratio of the 12-link union bound to the true holding-cluster sum is exactly 2, at z = 1/1000 through m = 60 and in closed form at every z. So the frozen 12 is not a different valid method. It is the same method with every leading cluster counted twice.

## 5. The rest of the G0 chain inside the lens

- (C2). e^{κ#Y(X)} ≤ e^{κn(X)} uses #Y″(γ) ≤ #γ. The step e^{κn(X)} = e^{d(X)}e^{−(θ−κ)n(X)} ≤ e^{d(X)}e^{−4(θ−κ)} uses θ ≥ κ and n(X) ≥ 4. Both are right. G0-a's sharper form δ_1 = 6S(εe^{2α+κ}) ≤ 6e^{−4(θ−κ)}S(εe^{2α+θ}) is right, the tail term included. The tail term is Σ_j 6F(49)μ^j x^{49+j}, and every degree is at least 4.
- (C3). The readout bound uses the corollary with Γ_0 = Γ_ℓ at one ℓ ∈ ∂P. It uses the 8-plaquette exclusion for clusters, so e^{d(X)−8θ} ≥ 1. It uses E|χ½| = 8/(3π) < 8489/10000. The test set enters exactly as in (C2), so T also halves.
- Convergence and reality. G0-a uses Ξ(tz), t ∈ [0, 1]. G0-b uses absolute convergence on the closed polydisc |ζ_γ| ≤ sup_V|z_γ|. Both are right.
- Optimum and cap. θ = κ is optimal, and existence is decided there. The cap α ≤ 1/4 never binds, since α_− ≤ 1/8 (G0-b Lemmas 3.21 and 3.22). Both are right. The 1/8 proof uses xS′(x) ≥ 4S(x) at the minimizer of the convex g.

## 6. The constant tables against the draft

Every frozen value that the tables quote reproduces by my route. My route is a monotone lower iteration from α = 0 plus an exact upper certificate. NOT_MET of the admissibility test is certified by convexity: g(a_0) > 0 with a lower enclosure and g′(a_0) < 0 with an upper one. That gives α_− > a_0. The derivations' "not certified" reads are search reads. Mine are certified on both sides. The G1 quantities use G1's frozen c(δ) (CONDITIONAL G1).

| Quantity | Exact scratch read | Draft | Derivations |
|---|---|---|---|
| ε_6(1/100), (1/64), (1/50) | 6.538419569879e-3, 1.021654437372e-2, 1.307754186435e-2 | C02 brackets | agree |
| 1/100 crude: 12α_−, 6α_− | 0.0110444506776, 0.00552222533881 | C07 [0.011044, 0.011045] | agree |
| 1/100 C03 / head-free: 12α_− | 9.43197012859e-6 / 9.37230167871e-6 | C08 brackets | agree; halves 4.7159850643e-6, 4.68615083935e-6 |
| 1/64 crude: 12α_−, 2δ′(12) | 0.10165304414, ≥ 0.2250597 | C11 brackets | agree |
| 1/64 crude: 6α_−, 2δ′(6) | 0.0508265220701, 0.1069532699 ≤ 1/8 | — | G0-b writes "≤ 0.106953", which is false (minor m2) |
| 1/64 C03: 12α_− | 0.00203477114568 | C14 [2.0347e-3, 2.0348e-3] | agree |
| 1/50 crude | no root (lower iterates leave the domain or pass 1/8 ≥ α_−) | C12 NOT_MET | agree |
| 1/50 head-free: 12α_−, 2δ′(12) | 0.0726458243401, ≥ 0.1562393 | C12 [0.072645, 0.072646], ≥ 0.15623 | agree |
| 1/50 head-free / C03: 6α_−, 2δ′(6) | 0.0363229121701, ≤ 0.07533304 / 0.0363235365282, ≤ 0.07533438 | — | agree; C_1 MET with 6 |
| δ_crit (c(δ) = 1) | 0.0496174910308, so δ_crit⁻ = 0.049617491 on the 1e-9 grid | C13 [0.0496174, 0.0496175] | agree |
| c(49/1000), c(1/20) | 0.9824885, 1.011067 | C13 brackets | agree |
| factor-12 edges (crude, C03, head-free) | 0.01369/0.01370, 0.01959/0.01960, 0.01959/0.01960, both sides certified | C13, C14 | agree |
| factor-6 edges (crude, C03, head-free) | 0.01556/0.01557, 0.02029/0.02030, 0.02029/0.02030, both sides certified, with δ_crit⁻ read as 0.0496174 or as 0.049617491 | — | agree; now certified on the NOT_MET side |
| C19 delta_crit_surrogate (δ_1 ≤ 49/1000), crude | factor 12: MET 0.01365, NOT_MET 0.01366; factor 6: MET 0.01552, NOT_MET 0.01553 | C19 "MET lost at 0.01366–0.01369" | not listed by either derivation (minor m6) |

Each derivation's equality table matches the draft row by row. I checked every row of G0-a §3.12 and G0-b §3.12 against the draft's HYPOTHESIS, CERTIFICATES, THEOREMS and C01–C16 text. The "no" rows are exactly the factor-2 rows and their consequences, plus the ratio proof that holds for all n. One more check: halving the G0-b brackets for C08, C09 and C14 is exact, since T and δ_1 are linear in the prefactor at a fixed (α, θ). I also checked G0-a's new C09 claim, "lost between 1/700 and 1/600", by scaling. At the minimizing θ the point x stays at about 4.4e-3. So T/P_10 scales as β⁴ along the minimizing grid point: 5.2259e-4·(4000/700)⁴ = 0.557 and ·(4000/600)⁴ = 1.03. Both agree with G0-a's 0.55725 and 1.0323.

## 7. Findings

### Blocking

**B1. The proved δ_1 and T are not the frozen ones. Under v2's gate, that makes the dependent rows read UNSUPPORTED.**
- Claim. Both routes prove δ_1 = min 6αe^{−4(θ−κ)} and T = (8489/10000)·6αe^{−8θ}. The draft, and v2 (CERTIFICATES and C07), freeze the 12-forms. Sections 1 to 4 confirm that 6 is right, that 6 is the least the method gives, and that the frozen 12 is exactly a double count.
- Why it is blocking. v2's G_attack says each derivation must "end with an explicit check that the proved constants are exactly the frozen ones: … δ_1 = 12α e^{−4(θ−κ)}, T = (8489/10000)·12α e^{−8θ}". It also says "a proved constant that differs from a frozen one makes every row and clause that rests on it read UNSUPPORTED". Both derivations report all_equal = false. Frozen as written, these would read UNSUPPORTED: C07, C08, C09 (T), C11, C12, C13, C14, C16, C17's replacement clause, and C19's delta_crit_surrogate and readout_grid_128 values.
- Several frozen statements are artifacts of the factor 2:
  - C11's C_1 NOT_MET (it reads MET with 6: 2δ′ = 0.1069532699 ≤ 1/8);
  - C12's DERIVED "C_1 and the self-map NOT_MET under every count model" (with 6 the head-free lower limit is 0.0363229121701 and 2δ′ ≤ 0.07533304);
  - the regime and window values 0.01959 and 0.01369;
  - C09's "lost between 1/1000 and 1/700".
- Fix. Before the freeze commit, re-freeze with δ_1 := min over certified (α, θ) of 6αe^{−4(θ−κ)} and T := (8489/10000)·6αe^{−8θ}. Both routes prove these forms. Name the test set as W′(ℓ), the 6 off links at m_ℓ, or keep W(e_0) with "every holding cluster meets it twice". Then recompute the rows above. The edges with 6 are 0.01556/0.01557 (crude) and 0.02029/0.02030 (C03 and head-free), certified on both sides above. The alternative is to keep 12 and reword every listed clause as a property of the 12-certificate, and to drop the word "exactly" from G_attack. That alternative leaves the critic's blocking item 5 unmet.

**B2. v2's THEOREMS row writes the corollary with the wrong weight.**
- Claim. v2 line 4 reads "sum_{clusters_containing_gamma}_abs(Phi)e^{d(gamma)}<=abs(z_gamma)e^{a(gamma)+d(gamma)}". The draft reads "abs(Phi)e^d", which is ambiguous. The attack brief and both derivations use e^{d(C)}, with d(C) = θn(C).
- Why it is blocking. With e^{d(γ)}, both sides carry the same factor e^{d(γ)}. So the statement is equivalent to Σ_{C∋γ}|Φ(C)| ≤ |z_γ|e^{a(γ)}, which is true but weaker. It does not supply the weight e^{κn(C)} that (C2) needs to pay for e^{κ#Y(X)}. G0-a's proof uses e^{κn(X)} ≤ e^{d(X)}e^{−(θ−κ)#γ_0} on the left side. G1 needs the same weight with θ = κ. A frozen formula that does not support the theorem it names is a formula that must change.
- Fix. Write "sum_{clusters_C_containing_gamma}abs(Phi(C))e^{d(C)}<=abs(z_gamma)e^{a(gamma)+d(gamma)},d(C)=sum_{gamma'_in_C}m_C(gamma')d(gamma')". Make the same change in the draft's "e^d".

### Minor

- **m1. G0-a Lemma 3.19 says the coarse torus is "bipartite, since L is even". That premise is false under (H1).** N even with N ≥ 8 allows N = 10, so L = N/2 can be 5. The conclusion #Y ≥ 4 still holds. A 3-cycle in (ℤ/L)⁴ with L ≥ 4 would need three unit steps summing to 0 in ℤ⁴, which parity forbids. Fix: use G0-b's Lemma 3.3(h) argument: a loop is contractible, with even length at least 4, or it winds, with length at least L ≥ 4.
- **m2. G0-b row 43 and checks block F state "2δ_1e^{δ_1} ≤ 0.106953" at 1/64 crude with factor 6.** The exact value is 0.1069532699, which is above 0.106953. Fix: write ≤ 0.106954. The C_1 conclusion (≤ 1/8) is unaffected.
- **m3. Monotonicity in β, open in G0-a gap 5, is DERIVED here.**
  - Put L_β = e^{βa}/c_0(β). Then ∂_β L_β = L_β(a − E_β a), so (d/dβ) ε_6⁶ = Cov_{P_β}(6(L_β − 1)⁵, a).
  - For β ≥ 0, both 6(L_β − 1)⁵ and a are nondecreasing functions of a. The covariance of two nondecreasing functions of one variable is at least 0, since it equals ½E[(f(a) − f(a′))(g(a) − g(a′))] with a′ an independent copy.
  - So ε_6 is nondecreasing on β ≥ 0.
  - g(α) = S(εe^{2α+θ}) − α increases with ε. So C_0 MET is inherited downward in β, and α_− and δ_1 are nondecreasing in β.
  - So the pair checks at each edge decide the "largest β on the grid" reads of C05, C06, C13 and C14, and the bisection of C04.
  - Fix: add this as a lemma to note section 3.
- **m4. The two routes state different proved δ_1.** G0-a gives 6S(εe^{2α+κ}). G0-b gives 6αe^{−4(θ−κ)}. They coincide at θ = κ and the exact least root. At a certified dyadic α above the root, G0-a's value is smaller. Fix: freeze 6αe^{−4(θ−κ)}, which both routes prove and which the engine reads from its certified α. Name the other as a remark.
- **m5. The KP dependence is narrower than ledger L06 says.** G0-b §3.7 proves the per-link bound in full by Penrose trees. The reweighting of section 3 reduces the d-form to the d-free form. Fix: tag the G0 use of KP as DERIVED (G0-b Proposition 3.15), and keep Kotecký–Preiss (1986) as a REPORTED cross-reference. This also closes G0-a gap 1 for G0.
- **m6. Both affected-row lists are incomplete.** Neither lists C19's delta_crit_surrogate window. That window moves from 0.01366–0.01369 to 0.01553–0.01556 with 6 (section 6). Neither lists C11's predicts_NOT_MET entry "C_1". Neither lists PREDICTION_SUMMARY's rows_predicting_a_NOT_MET. Neither lists the G1-valued brackets that a re-freeze recomputes: c(δ_1), δ_2 and Σδ_k in C07 and C08, and c(δ_1) at 1/64 in C14. Fix: add them to the re-freeze list under B1.

## 8. Scratch files (pre-freeze disclosure; not engines, not evidence)

- `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/attack/G0-kp-checks.py`, with output `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/attack/G0-kp-checks.out`. Blocks A (test-set geometry on 8⁴), B (the fillings-only double count), C (ε_6 and α_− brackets), D (δ_crit from G1's frozen c(δ)) and E (edges with factors 12 and 6, certified on both sides). Run time is about 3 minutes.
- `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/attack/G0-kp-surrogate.py`, with output `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/attack/G0-kp-surrogate.out`. The C19 surrogate window with factors 12 and 6.

Both use integers and Fractions only, with outward rounding to dyadics at 320 bits. Floats appear only in display. Neither shares code with `G0-a-kp.py` or `G0-b-checks.py`.
