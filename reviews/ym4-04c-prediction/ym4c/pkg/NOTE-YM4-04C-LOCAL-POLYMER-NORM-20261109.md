# YM4-04C: a localized polymer norm on the b = 2 blocked SU(2) action

## 0. Status

**Status: the freeze package, prepared before any engine code, on the operator's word of November 8, 2026: "For YM4-04, I agree with the prediction-first approach, with a reachable falsifier per row. The successful beta^10 calculation is a strong input, but it does not establish that scale-to-scale control." Base: main `830fd3f`. Written by the YM4-04C freeze lane on November 9, 2026. This note holds the definitions (sections 1 and 2), the two theorems with full proofs (sections 3 and 4), the predictions in [`PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp`](PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp) (41 lines), the plan of the engine as text (section 12), and small exact checks in [`reviews/ym4-04c-prediction/`](../reviews/ym4-04c-prediction/) (section 14). Nothing is committed yet. The freeze commit is the owner's decision.**

**DERIVED here:** Theorem G0 (section 3) and Theorem G1 (section 4), with their constants. G0 gives δ_1 = 6α e^{−4(θ−κ)} and T = (8489/10000)·6α e^{−8θ}. G1 gives the test λ(δ) := δ′ + ln(1 + δ′) ≤ κ, with δ′ = δe^{δ}, and the factor c_fin(δ). Also DERIVED: the geometry, the enclosures, the wall, the edges as arithmetic, the exact line channel and its floor for every representation, the two-object instance, the leading order and brackets of C10c, and the tree-level and Gaussian rows.

**CONDITIONAL, on the formal second-seat attack (gate G_attack, OPEN):** on G0 and G1, rows C07, C08, C11, C12, C13, C14, C16, the replacement clause of C17, the regime clause of the hypothesis row and C19's `delta_crit_surrogate` edge; on G0 alone, the injection clause of C01, C09 and C19's `readout_grid_128` value; on G1 alone, the c_fin(δ_in) and per-root comparisons of C10b and C10c, and C13's δ_crit and c_fin values. Rows C04, C05, C06 and C15 have DERIVED arithmetic and speak about H_1 only through G0. Rows marked TG rest on G1's (1 + t)^f tree-graph step, which no second seat has read; each carries its fallback under 2δ′ ≤ κ.

**CONJECTURE:** the closed-set counts of C03, the refined edges built on them, and the readout ratios T/P_10. **REPORTED:** Finner's inequality, the exponential formula for connected graphs, Weyl's integration formula with Schur orthogonality, the Kotecký–Preiss theorem (for G1), Hoeffding's lemma and Watson's G_3(0). **Reproduction rows:** W04. **OPEN:** all weak-coupling scale-to-scale control (section 18).

**Pre-freeze values.** Every row carries a `prefreeze` field. Only prefreeze=NONE values can enter a count of confirmed predictions. Every CROSS_READ or COMPUTED value is a reproduction.

**What changed against the draft.** The proofs give constants that differ from the draft's. δ_1 and T carry the factor 6, not 12. C_k is λ(δ) ≤ κ, not 2δ′ ≤ κ/2, and the factor is c_fin(δ), not the draft's c(δ). c_fin(δ) = e^{−1} for 0 < δ ≤ 0.078733761. The draft and its repair v2 were never committed, so the prediction file carries the final constants in its own 41 rows. Every value that depends on them was recomputed in exact arithmetic before this freeze (section 6; `reviews/ym4-04c-prediction/ym4c/pkg/recompute/`). The window of the self-map is β_0 ≤ 0.02074 on the 10⁻⁵ grid, against v2's 0.01959.

## 1. Target and why this shape

Issue #4 sets the proof gate. It asks for an explicit hypothesis H_k, with its norm, gauge, couplings, scales and constants. It asks for H_k ⇒ H_{k+1} with errors that are summable and uniform in the volume. It asks for a ledger of theorem dependencies.

[YM4-03C](NOTE-YM4-03C-BLOCKED-ACTION.md) §12 and [YM4-04A](NOTE-YM4-04-TWO-TERNARY-BLOCKS-20261107.md) name the next obligation. It is a local polymer bound, uniform in the volume, in place of the global Cauchy remainder of YM4-04A. That remainder needs β ≤ 1/(8N_p), with N_p the number of fine plaquettes, so it vanishes as the volume grows.

The operator's word bounds what the β¹⁰ table means. The table is an input. It is not scale-to-scale control.

This step closes the gate only at strong coupling. With the C03 counts, the self-map holds for β_0 ≤ 0.02074 on the 10⁻⁵ grid. That is C14's edge, a CONJECTURE on C03 and CONDITIONAL on G0 and G1. β_0 = 0.02075 is outside: C14 predicts the self-map NOT_MET there for every count vector. Inside the window the certified flow runs to the trivial fixed point, Haar measure.

## 2. Definitions

**Lattices and the map.** The fine lattice is Λ_0 = (ℤ/N)⁴ with spacing h_0, N = 2^K L_K, L_K ≥ 4 and K ≥ 2. G0 needs only N even and N ≥ 8. The scale-k lattice is Λ_k = (ℤ/(N/2^k))⁴, with spacing 2^k h_0. B is the line map of [YM4-03](NOTE-YM4-03-ONE-SCALE-BLOCKING.md) at b = 2, (BU)_λ(x′) = U_λ(2x′)U_λ(2x′ + e_λ). ρ_k is the exact Haar pushforward density of k applications of B (YM4-03 Theorem 4, iterated).

**The line gauge.** At each step the line of a coarse link ℓ is fixed at (U_0, U_1) = (1, V_ℓ) by the gauge transformation at its midpoint m_ℓ (YM4-03C §2). It is a computational gauge only. Every activity is gauge invariant, and every norm is a sup norm of an invariant function. YM4-03C §2 Lemma A says which coarse links an off-link integral depends on. If the integrand does not hold position 0 of ℓ, the integral is constant in V_ℓ. If it does not hold position 1, the integral does not involve V_ℓ. So an activity depends only on the coarse links both of whose positions it holds (Lemma 3.21, Lemma 4.3).

**The polymer form of H_0.** H_0(β_0) is the SU(2) Wilson measure with weight e^{β_0 a}, a = ½ Re Tr. It is written ∏_p c_0(β_0)(1 + K(U_p)), with c_0(x) = Σ_m (x/2)^{2m}/(m!(m + 1)!), K = Σ_{n≥2} n t_n χ_{(n−1)/2} and t_n = I_n/I_1 (Lemma 3.2).

**H_k for k ≥ 1.** log ρ_k(V) = const_k + Σ_Y R_k(Y; V). Y runs over the finite sets of scale-k links with #Y ≥ 4 that contain a closed loop. Each R_k(Y; ·) is real, bounded, measurable, gauge invariant, and a function of V restricted to Y. The norm is

```text
norm_kappa(R_k) := sup_l sum_{Y containing l} e^{kappa #Y} sup_V |R_k(Y;V)|  <=  delta_k.
```

No Wilson term is kept outside Σ_Y R_k(Y). The plaquette coupling is β_k := 2c_{1/2}(P), with c_{1/2}(P) the χ_{1/2}(V_P) Haar projection of log ρ_k. By Lemma 4.22, |β_k| ≤ (16/(3π))e^{−4κ}δ_k < 0.62454 δ_k. The function space is the Banach space of families {R(Y)} with finite norm.

**Constants.** κ = 1/4. D = 20 is the maximal off-link degree of a plaquette. Every link lies in 6 plaquettes, so Finner's exponent is 6. #W(e_0) = 12 is the number of off links of the 6 plaquettes through a line link. #W′(ℓ) = 6 is the number of off links at the midpoint m_ℓ, the test set of G0. F_20(n) = C(20n, n)/(19n + 1). μ = 20²⁰/19¹⁹ ∈ [53.00068, 53.00069]. E|χ_{1/2}| = 8/(3π) ∈ [0.8488263, 0.8488264], below 8489/10000. The head length is n_max = 10.

**The step-k quantities.** δ′ := δe^{δ}. λ(δ) := δ′ + ln(1 + δ′). The factor is

```text
c_fin(delta) := max{ e^{-4 kappa},  e^{delta + lambda - 5 kappa},  e^{delta - kappa/2} sup_{f >= 4} ( e^{-(kappa - lambda) f} - e^{-kappa f} ) }.
```

The certificates are stated as exact inequalities in section 5. Sections 3 and 4 prove that they imply H_1 and H_{k+1}.

## 3. Theorem G0 (step 0): from the Wilson measure to H_1

> **Assembly note (not part of the canonical text).** Sections 3 and 4 are the canonical repaired sections, verbatim except for file paths, which now name the committed copies under `reviews/ym4-04c-prediction/`. In them "frozen" means the uncommitted 40-line draft, or its repair v2 (`PREDICTION-v2.hbp`). Neither was committed. The prediction file of this commit carries the final constants of both sections in its own 41 rows, and nothing is appended to it. Section 3.12 reads its G1-dependent values under G1 as drafted (2δ′ ≤ κ/2, the draft's c(δ), δ_crit ∈ [0.0496174, 0.0496175]). Section 4 replaces that G1. So the values of section 3.12 that rest on G1 are superseded by section 6 and the prediction file: the regime 0.02029, the edges 0.01556/0.01557 and 0.02029/0.02030, C11's crude self-map NOT_MET, C19's surrogate window 0.01553–0.01556, and each "recompute under G1". The final values are 0.02074/0.02075 (C14), 0.01767/0.01768 (C13), C11's crude self-map MET, and the surrogate window 0.01553–0.01767. The G0 values of section 3.12 stand: the factor 6, δ_1, T, the C08 ratios, the C09 ratios and the C_0 edges.

**Status.** This is the canonical section 3 of `docs/NOTE-YM4-04C-LOCAL-POLYMER-NORM-20261109.md`. It merges route A (`reviews/ym4-04c-prediction/ym4c/pkg/derive/G0-a.md`) and route B (`reviews/ym4-04c-prediction/ym4c/pkg/derive/G0-b.md`). It repairs both against the three second-seat attacks (`reviews/ym4-04c-prediction/ym4c/pkg/attack/G0-kp.md`, `reviews/ym4-04c-prediction/ym4c/pkg/attack/G0-count.md`, `reviews/ym4-04c-prediction/ym4c/pkg/attack/G0-assembly.md`), each of which read GAP. The base is main `830fd3f`. "Frozen" means the 40-line draft `reviews/ym4-04c-prediction/ym4-04c/synth/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp`. No engine ran.

DERIVED here: Theorem G0, Corollary G0.C, and every lemma and proposition of sections 3.2 to 3.11, unless a clause is tagged otherwise. They rest on [YM4-03](NOTE-YM4-03-ONE-SCALE-BLOCKING.md) (Theorem 4, Proposition 2, the proof of Theorem 8), on [YM4-03C](NOTE-YM4-03C-BLOCKED-ACTION.md) (§2 Lemma A and the line gauge, §4 the readout, §6 Lemma B and the polymer form) and on [LEMMA-0001](LEMMA-0001-GAUGE-INVARIANCE.md). REPORTED, with citations: Finner's inequality (Theorem 3.7); the exponential formula for connected graphs (Lemma 3.15); Weyl's integration formula on SU(2), completeness of the characters and Schur orthogonality (Lemmas 3.2 and 3.25). CONJECTURE: the refined head N(5), …, N(10), that is the values of row C03. OPEN inside G0: nothing. OPEN outside G0, and named in section 3.13: G1, and the re-freeze of the rows that rest on the changed constants.

**What changed against the frozen draft.** Each change is marked CHANGED where it appears.

1. δ_1. Frozen: min over certified (α, θ) of 12α e^{−4(θ−κ)}. Final: min over certified (α, θ) of **6**α e^{−4(θ−κ)}.
2. T. Frozen: (8489/10000)·12α e^{−8θ}. Final: (8489/10000)·**6**α e^{−8θ}.
3. The test set. Frozen: W(e_0), 12 links, each counted once. Final: W′(ℓ), the 6 off links at the midpoint m_ℓ. Equivalently W(e_0) with each holding polymer counted twice.
4. The per-polymer corollary. Frozen: "Σ_{clusters ∋ γ} |Φ| e^d ≤ |z_γ| e^{a(γ)+d(γ)}", with the weight unnamed (v2 wrote e^{d(γ)}). Final: the weight on the left is e^{d(X)}, with d(X) = θ·n(X) summed over the polymers of X with multiplicity.
5. The Kotecký–Preiss theorem is no longer a REPORTED input of G0. The bound it would supply is proved here (Proposition 3.18). Kotecký and Preiss (1986) stays a cross-reference.
6. Weaker hypotheses. The fine side need only be even and at least 8. The core hypothesis is the per-link inequality (KP_w). The cap α ≤ 1/4 and the θ grid are certificate choices, not hypotheses.

Changes 1 to 3 are one fact. Every polymer that holds both positions of a coarse link ℓ holds a plaquette through e_0(ℓ). Both off links of that plaquette lie in W(e_0). Exactly one of them ends at m_ℓ. So the union bound over W(e_0) counts every holding polymer at least twice. At leading order it counts the 6 fillings through ℓ exactly twice. The frozen 12-forms follow from the 6-forms, so every frozen 12-value stays a valid bound. They are not what the proof gives. Section 3.12 lists the rows that move.

**Symbols, binding for this section.** a(g) = ½ Re Tr g for g ∈ SU(2). The Kotecký–Preiss pair is (α, θ). With a polymer as argument, a(γ) = α·#off(γ) and d(γ) = θ·#γ; this section mostly writes these out. b = 2 is the blocking factor. κ = 1/4 is the norm weight. Directions are λ, ν, ρ, σ. μ := 20²⁰/19¹⁹ only. D = 20. F(n) := F_20(n) = C(20n, n)/(19n + 1). N is the fine side; N(n), always with its argument, is a count vector; N_p is the number of fine plaquettes. K is the plaquette function of Lemma 3.2; the number of blocking steps is written out in words. e_χ := E|χ_{1/2}|. #A is the number of elements of a set A.

### 3.1 The statement

**Theorem G0.** Assume:

- (H1) Λ_0 = (ℤ/N)⁴ with N even and N ≥ 8, and Λ_1 = (ℤ/(N/2))⁴. B is the YM4-03 line map at b = 2, (BU)_λ(x′) = U_λ(2x′) U_λ(2x′ + e_λ). ρ_1 is its exact Haar pushforward density (YM4-03 Theorem 4), written in the line gauge (1, V_ℓ) of YM4-03C §2.
- (H2) β_0 ≥ 0. The weight is w = e^{β_0 a}. K := e^{β_0 a}/c_0(β_0) − 1, and ε := ε_6(β_0) := ‖K‖_{L⁶(SU(2))}.
- (H3) 0 ≤ κ ≤ θ and α ≥ 0. For every off link w of Λ_0,

  ```text
  (KP_w)    sum_{gamma in Gamma : w in off(gamma)}  omega(gamma) e^{alpha #off(gamma)}  <=  alpha,      omega(gamma) := sup_V |z_gamma(V)| e^{theta #gamma}.
  ```

  Γ is the set of polymers and z_γ their activities (section 3.3).

Then:

- (C1) log ρ_1(V) = const_1 + Σ_Y R_1(Y; V). Y runs over the sets of coarse links that contain a closed loop. Every such Y has #Y ≥ 4. Each R_1(Y; ·) is real, coarse-gauge invariant and a function of V restricted to Y. The coarse Wilson term 2t_2(β_0)⁴ χ_{1/2}(V_P) lies inside R_1(∂P).
- (C2) **CHANGED.** The norm obeys

  ```text
  norm_kappa(R_1) := sup_l sum_{Y containing l} e^{kappa #Y} sup_V |R_1(Y;V)|  <=  delta_1(alpha, theta) := 6 alpha e^{-4(theta - kappa)}.
  ```

- (C3) **CHANGED.** For every coarse plaquette P, the coefficient c_{1/2}(P) of χ_{1/2}(V_P) in log ρ_1 obeys

  ```text
  | c_1/2(P) - 2 t_2(beta_0)^4 |  <=  T(alpha, theta) := e_chi * 6 alpha e^{-8 theta}  <=  (8489/10000) * 6 alpha e^{-8 theta},     e_chi = 8/(3 pi).
  ```

- (C4) **CHANGED (the weight).** For every polymer γ, the clusters rooted at γ obey Σ_{X: γ_1 = γ} (1/(n−1)!) |φ^T(X)| Π_{i≥2} ω(γ_i) ≤ e^{α#off(γ)}. In the multiset form of route A this gives Σ_{X ∋ γ} |Φ(X)| e^{d(X)} ≤ sup|z_γ| e^{a(γ)+d(γ)}, with d(X) = θ·n(X) (Remark 3.19). For every off link w, the clusters through w obey Σ_{X ∋ w} (1/n!) |φ^T(X)| Π_i ω(γ_i) ≤ α.
- (C5) No constant in (C2), (C3) or (C4) depends on N, on the number of blocking steps or on N_p.

**Corollary G0.C (the frozen certificate C_0).** Let the head N(4), …, N(10) be valid: N(n) ≥ N_w(n) for every off link w of Λ_0 and 4 ≤ n ≤ 10, where N_w(n) is the number of polymers of n plaquettes that hold w. The crude head N(n) = 6F(n) is valid (Corollary 3.12). By Lemma 3.14 validity can be checked on one lattice, by class. Let α > 0, κ ≤ θ, x := ε e^{2α+θ}, μx < 1, and S(x) ≤ α, with the frozen closed form

```text
S(x) := sum_{n=4}^{10} N(n) x^n  +  sum_{n=11}^{48} 6 F(n) x^n  +  6 F(49) x^49 / (1 - mu x).
```

Then (H3) holds. (C2) and (C3) hold in the sharper forms

```text
norm_kappa(R_1)  <=  6 S(eps e^{2 alpha + kappa})  <=  6 e^{-4(theta - kappa)} S(x)  <=  6 alpha e^{-4(theta - kappa)},
| c_1/2(P) - 2 t_2^4 |  <=  e_chi * 6 e^{-8 theta} S(x)  <=  (8489/10000) * 6 alpha e^{-8 theta}.
```

So a C_0 read that is MET gives H_1(κ, δ_1) with δ_1 := min over certified (α, θ) of 6α e^{−4(θ−κ)} (**CHANGED** from 12). The minimum sits at θ = κ and α = α_−(κ), the least root of S(εe^{2α+κ}) = α (Lemma 3.31).

The frozen 12-forms follow. They are weaker by exactly a factor 2 at every (α, θ).

### 3.2 The geometry of the b = 2 lines

For a fine site x let O(x) := {λ : x_λ odd}. N is even, so O(x) is well defined. Coarse sites are the x with O(x) = ∅. A fine link (x, λ) joins x to x + e_λ. Its **transverse odd set** is O_⊥(x, λ) := O(x) ∖ {λ}, the same at both ends. The link is a **line link** when O_⊥ = ∅, as in YM4-03C §2. Otherwise it is an **off link of class** c := #O_⊥ ∈ {1, 2, 3}.

A coarse link ℓ = (x′, λ) has position 0, the line link e_0(ℓ) = (2x′, λ), and position 1, the line link e_1(ℓ) = (2x′ + e_λ, λ). Its **midpoint** is m_ℓ = 2x′ + e_λ, with O(m_ℓ) = {λ}.

A fine plaquette p with base x in the plane {λ, ν} has the links (x, λ), (x + e_λ, ν), (x + e_ν, λ), (x, ν). Its **odd set** is O(p) := O(x) ∖ {λ, ν}, the same at all four corners. p is a **quarter** when O(p) = ∅.

W(e_0(ℓ)) is the set of off links of the plaquettes through e_0(ℓ). W′(ℓ) is the set of off links with an end at m_ℓ.

**Lemma 3.1 (the b = 2 geometry).** Let N be even and N ≥ 8.

1. Every fine link lies in exactly 6 plaquettes. A plaquette has 4 distinct links. Two distinct plaquettes share at most one link.
2. A quarter has 2 line links, one in each direction of its plane. They meet at a coarse site. It has 2 off links of class 1. They meet at a corner s(p) with O(s(p)) equal to the plane of p. A plaquette with #O(p) = t ≥ 1 has no line link and 4 off links: two of class t and two of class t + 1. So every plaquette has 2 or 4 off links.
3. Let s be a site with O(s) = {λ, ν}. The 4 plaquettes of the plane {λ, ν} with corner s are quarters. They tile the 2 × 2 fine square of the coarse plaquette Q with base (s − e_λ − e_ν)/2. This set is the **filling** F_Q, and s = s_Q is its **center**. Every quarter lies in exactly one filling. The off links of F_Q are its 4 **internal links**, from s_Q to the midpoints of the 4 sides of Q. Each internal link lies in exactly 2 quarters of F_Q, and the quarters form a 4-cycle in which consecutive quarters share one internal link. The 8 line links of F_Q are both positions of the 4 coarse links of ∂Q. The quarter at a coarse corner c of Q holds the two of them at c.
4. A class-1 off link is an internal link of exactly one filling. It lies in the 2 quarters of that filling beside it and in 4 plaquettes with #O(p) = 1. Off links of class 2 or 3 lie in no quarter. A plaquette with #O(p) = 1 holds exactly 2 class-1 links, internal to fillings of two different planes.
5. If Q ≠ P, a quarter of F_Q holds at most one line link of ∂P.
6. Let ℓ = (x′, λ). The 6 plaquettes through e_0(ℓ) are the quarters at the corner 2x′ of the 6 fillings F_Q with ℓ ∈ ∂Q. Their 12 off links are distinct. They form W(e_0(ℓ)), and each of the 6 fillings holds exactly 2 of them. Each of the 6 plaquettes has exactly one off link at m_ℓ. These are the 6 off links at m_ℓ, so #W′(ℓ) = 6. The same holds at e_1(ℓ), with the same W′(ℓ). Every link of W(e_0) and of W′(ℓ) has class 1.
7. Join two distinct plaquettes when they share an off link. A plaquette with k off links has exactly 5k neighbours: 10 for a quarter and 20 otherwise. So the maximal degree is D = 20 and the minimal degree is 10.
8. On Λ_1, with side L = N/2 ≥ 4: the 4 coarse links of a coarse plaquette are distinct; a coarse link lies in exactly 6 coarse plaquettes; two perpendicular coarse links at a common site lie in exactly one coarse plaquette; and every closed loop of coarse links has at least 4 links.

*Proof.* 1. The link (y, λ) lies in the plaquettes of the planes {λ, ν}, ν ≠ λ, with base y or y − e_ν. These are 3 × 2 = 6 plaquettes, distinct since N ≥ 3. The four corners of a plaquette are distinct since N ≥ 3, so its 4 links are distinct. Two links of one plaquette are perpendicular with a common corner or parallel at distance 1. Either pair fixes the plane and the base. So two distinct plaquettes share at most one link.

2. The two λ-links of p sit at x and x + e_ν. Their transverse odd sets are O(p) with ν added or not, and exactly one of them holds ν. The same holds for the two ν-links with λ. So the classes are t, t + 1, t, t + 1 with t = #O(p), and class 0 is a line link. If t = 0, the line links are the λ-link at even ν-coordinate and the ν-link at even λ-coordinate. They meet at the corner with even λ- and ν-coordinates, whose other coordinates are even too, a coarse site. The two class-1 links meet at the corner with odd λ- and ν-coordinates.

3. The coordinates of s outside {λ, ν} are even, so the 4 plaquettes have O(p) = ∅. Their far corners s ± e_λ ± e_ν are coarse sites. So they tile the 2 × 2 square of Q. A quarter fixes s(p) and its plane by item 2, so it lies in exactly one filling. By item 2 the off links of each quarter are its 2 links at s_Q. These are the 4 links at s_Q along ±λ and ±ν, each in the 2 quarters beside it. The boundary of the square is made of the 8 line links, two per side of Q. The quarter at c holds the two boundary links at c.

4. Let (x, λ) have O_⊥ = {ν}. Its ends have odd sets {ν} and {λ, ν}. The second end is the center of a filling of the plane {λ, ν}, and the link is one of its internal links. The first end is no center. So the filling is unique. The 6 plaquettes through the link lie in the planes {λ, ρ}, ρ ≠ λ. At the corner with odd set {λ, ν} their odd set is {ν} ∖ {ρ}. It is empty exactly when ρ = ν. That gives the 2 quarters, both of that filling, and 4 plaquettes with #O(p) = 1. Off links of quarters have class 1 by item 2. Let O(p) = {ρ} with p in the plane {λ, ν}. By item 2 its class-1 links are a λ-link and a ν-link, each with O_⊥ = {ρ}. By the first part they are internal to fillings of the planes {λ, ρ} and {ν, ρ}.

5. The two line links of a quarter of F_Q meet at a coarse corner c of Q. They are positions of the two coarse links of ∂Q at c. If both are line links of ∂P, then P contains these two perpendicular coarse links. By item 8, P = Q.

6. A plaquette through e_0(ℓ) holds a line link, so it is a quarter by item 2. Its line links meet at a coarse site, which is an end of e_0(ℓ). That end is 2x′, since m_ℓ is not coarse. So the plaquette is the quarter at 2x′ of a filling F_Q, and ℓ ∈ ∂Q by item 3. Each of the 6 coarse plaquettes through ℓ (item 8) has one quarter at 2x′. So the 6 plaquettes through e_0(ℓ) are these 6 quarters. They share e_0(ℓ), so by item 1 they share no other link, and their 12 off links are distinct. The off links of a quarter are internal links of its own filling, and distinct fillings have disjoint internal links by item 4. So each of the 6 fillings holds exactly 2 links of W(e_0). The quarter of F_Q at 2x′ holds the internal links from s_Q to the midpoints of the two sides of Q at 2x′. One of these midpoints is m_ℓ. So it has exactly one off link at m_ℓ, the link from m_ℓ to s_Q. The 6 centers are m_ℓ ± e_ν with ν ≠ λ. So these are the 6 links at m_ℓ along ±ν, ν ≠ λ. The other 2 links at m_ℓ are e_0(ℓ) and e_1(ℓ). At e_1(ℓ) the 6 plaquettes are the quarters at 2x′ + 2e_λ of the same 6 fillings, and each holds the same link from m_ℓ to s_Q. Internal links have class 1 by items 2 and 3.

7. Each off link of p lies in 5 other plaquettes by item 1. A plaquette other than p shares at most one link with p. So distinct off links of p give distinct neighbours.

8. The side is L ≥ 4. The first three claims follow as in item 1, with L ≥ 3 in place of N ≥ 3. A closed loop is a cycle of distinct coarse links, a sequence of k unit steps whose sum is 0 mod L. If the sum is 0 in ℤ⁴, the coordinate sum changes by ±1 at each step and returns to its start, so k is even. k = 2 would need two distinct links between the same two sites, which L ≥ 3 excludes. So k ≥ 4. Otherwise some coordinate of the sum is a nonzero multiple of L, which needs at least L ≥ 4 steps. ∎

The premise "the coarse torus is bipartite since L is even" of route A is false under (H1). N = 10 is allowed, and its coarse torus (ℤ/5)⁴ has a straight winding loop of length 5. Item 8 does not use bipartiteness.

### 3.3 Haar facts and the polymer gas

**Lemma 3.2 (one-link Haar facts).** Let g be Haar distributed on SU(2) and β ≥ 0.

1. (REPORTED: Weyl's integration formula, Bröcker and tom Dieck 1985, §IV.1.) Write the eigenvalues of g as e^{±iφ}, φ ∈ [0, π]. A class function f has E f = (2/π) ∫_0^π f(φ) sin²φ dφ. Here a = cos φ and χ_j = sin((2j + 1)φ)/sin φ, so |χ_j| ≤ 2j + 1. The characters are orthonormal and complete among class functions in L².
2. E[a^{2m}] = 4^{−m} (2m)!/(m!(m + 1)!) and the odd moments of a vanish. So c_0(β) := E e^{βa} = Σ_{m≥0} (β/2)^{2m}/(m!(m + 1)!).
3. Define t_n(β) by n t_n := E[χ_{(n−1)/2} e^{βa}]/c_0(β), so t_1 = 1. For β > 0, n t_n = n I_n(β)/I_1(β) with I_n(β) := (1/π) ∫_0^π e^{β cos φ} cos(nφ) dφ, and |n t_n| ≤ 2n β^{n−1} e^β/n!. So K = Σ_{n≥2} n t_n χ_{(n−1)/2}, absolutely and uniformly on SU(2). In particular E[K χ_{1/2}] = 2t_2.
4. K is a real class function, K(g⁻¹) = K(g), E K = 0, and ε_6(β)⁶ = E K⁶ = Σ_{k=0}^{6} C(6, k)(−1)^{6−k} c_0(kβ)/c_0(β)^k, with c_0(0) = 1.
5. e_χ := E|χ_{1/2}| = 8/(3π), and 8/(3π) < 848/999 < 8489/10000.

*Proof.* 2. g ↦ −g preserves Haar measure and sends a to −a. By item 1, E[a^{2m}] = (2/π)∫_0^π cos^{2m}φ sin²φ dφ. Wallis's integral ∫_0^π cos^{2m}φ dφ = π C(2m, m)/4^m and sin² = 1 − cos² give π C(2m, m)/(4^m (2m + 2)). Multiplying by 2/π gives the claim. This is the Catalan count of closed McKay walks of YM4-03C §10. Sum β^{2m}E[a^{2m}]/(2m)!; the series converges absolutely, so sum and integral commute.

3. By item 1, n t_n c_0 = (2/π)∫_0^π e^{β cos φ} sin(nφ) sin φ dφ. Integrate by parts with sin φ e^{β cos φ} = −β⁻¹ (d/dφ) e^{β cos φ}. The boundary term vanishes and the integral becomes (2n/β) I_n. At n = 1 this reads c_0 = 2I_1/β. Dividing gives n t_n = n I_n/I_1. Expand e^{β cos φ} = Σ_k β^k cos^kφ/k!. cos^kφ has Fourier modes of order at most k, so only k ≥ n contribute to I_n, each with |(1/π)∫_0^π cos^kφ cos(nφ) dφ| ≤ 1. So |I_n| ≤ β^n e^β/n!. With c_0 ≥ 1 this gives the bound on n t_n. Then Σ_n n|n t_n| < ∞, so the character series converges absolutely and uniformly. Its limit is continuous, and by completeness it equals e^{βa}/c_0. Subtract t_1 χ_0 = 1. The identification t_n = I_n/I_1 matches the frozen notation; no bound below uses it.

4. e^{βa} is a positive class function and a(g⁻¹) = a(g). E K = c_0/c_0 − 1 = 0. Expand (e^{βa}/c_0 − 1)⁶ and use E e^{kβa} = c_0(kβ).

5. By item 1, E|χ_{1/2}| = (2/π)∫_0^π 2|cos φ| sin²φ dφ = (8/π)∫_0^{π/2} cos φ sin²φ dφ = 8/(3π). Machin's formula π = 16 arctan(1/5) − 4 arctan(1/239) holds because (5 + i)⁴(239 − i) = 114244(1 + i). The alternating series give arctan(1/5) ≥ 1/5 − 1/375 + 1/15625 − 1/546875 and arctan(1/239) ≤ 1/239. So π ≥ 1231847548/392109375 > 333/106. Hence 8/(3π) < 8·106/(3·333) = 848/999 < 8489/10000. ∎

As an outward enclosure, 8/(3π) ∈ [0.8488263, 0.8488264]. Route B's display [0.8488264, 0.8488266] was rounded to nearest and missed the true value 0.84882636316.

**Lemma 3.3 (the polymer form).** Call a nonempty set of fine plaquettes **connected** when it is connected in the graph of Lemma 3.1 item 7. For such a set γ let z_γ(V) := E_V[Π_{p∈γ} K(U_p)], with E_V product Haar measure on the off links and every line at (1, V_ℓ). Two connected sets are **compatible** when they share no off link. Then, for every V,

```text
Z rho_1(V) = c_0(beta_0)^{N_p} Xi(V),      Xi(V) = sum over finite sets of pairwise compatible connected sets of  prod z_gamma(V),
```

with Z := ∫ Π_p e^{β_0 a(U_p)} dU and the empty set contributing 1. Each z_γ is real, and Ξ(V) > 0.

*Proof.* YM4-03C §2 gives ρ_1(V) = Z⁻¹ ∫ Π_{off} dU Π_p w(U_p), with every line at (1, V_ℓ). It follows from YM4-03 Theorem 4 and the gauge transformation at m_ℓ by U_0. YM4-03C writes w = e^{−β(1−a)}; the factor e^{−β_0} per plaquette cancels against Z. Write e^{β_0 a(U_p)} = c_0(1 + K(U_p)) and expand the product over the sets S of plaquettes. Split S into its components under "share an off link". Each component is a connected set. Distinct components are compatible. They are functions of disjoint sets of independent Haar links, the lines being fixed, so E_V factors over them. Conversely, the components of the union of a compatible family are its members: compatible sets share no off link, hence no plaquette, since every plaquette has an off link (Lemma 3.1 item 2). K is real, so each z_γ is real. w ≥ e^{−β_0} > 0, so ρ_1 > 0 (YM4-03 Theorem 4, item 1) and Ξ(V) > 0. ∎

A connected set γ is **closed** when every off link of every plaquette of γ lies in at least two plaquettes of γ. off(γ) is the set of off links held by γ.

**Lemma 3.4 (Lemma B for activities).** If a connected set γ is not closed, then z_γ(V) = 0 for every V.

*Proof.* Let w be an off link of p ∈ γ that no other plaquette of γ holds. p holds each of its links once (Lemma 3.1 item 1), so U_p = A U_w^{±1} B with A and B free of U_w. By Haar invariance and Lemma 3.2 item 4, ∫ K(A u^{±1} B) du = E K = 0. No other factor holds U_w. ∎

This is rule (a) of YM4-03C §6, Lemma B, in activity form. The exception "supp(M) is one plaquette" there does not arise here, since a one-plaquette activity is E K = 0. From here on a **polymer** is a closed connected set of plaquettes. Γ is the finite set of polymers of Λ_0. γ ≁ γ′ (incompatible) when off(γ) ∩ off(γ′) ≠ ∅. The relation is reflexive and symmetric. By Lemma 3.4, Ξ(V) is the sum over the compatible families of polymers.

**Lemma 3.5.** #off(γ) ≤ 2#γ for every polymer γ. The bound is attained.

*Proof.* Count the pairs (w, p) with w ∈ off(γ), p ∈ γ and w ∈ p. Closure gives at least 2 per off link. Lemma 3.1 item 2 gives at most 4 per plaquette. So 2#off(γ) ≤ 4#γ. The 6 faces of a unit cube whose fourth coordinate is odd form a polymer with 12 off links. ∎

**Lemma 3.6 (small polymers).** Every polymer has at least 4 plaquettes. The polymers of exactly 4 plaquettes are the fillings. So N_w(n) = 0 for n ≤ 3. N_w(4) = 1 when w has class 1, and N_w(4) = 0 when w has class 2 or 3.

*Proof.* Let γ be a polymer. Suppose γ holds a plaquette with 4 off links. Closure puts each of them in a second plaquette of γ. These 4 plaquettes are distinct by Lemma 3.1 item 1. So #γ ≥ 5. Otherwise every plaquette of γ is a quarter. Let p ∈ γ. Each of its two internal links lies in a second plaquette of γ. That plaquette is a quarter holding an internal link of the filling of p, so it lies in that filling (Lemma 3.1 items 3 and 4). These are the two cycle neighbours of p. Repeating along the 4-cycle gives F ⊆ γ for the filling F of p. A proper nonempty subset of the 4-cycle holds some internal link once and is not closed. Connectivity then gives γ = F. Each filling is closed and connected. A class-1 link lies in exactly one filling, and a link of class 2 or 3 in none (Lemma 3.1 item 4). ∎

### 3.4 Finner's inequality with exponent 6

**Theorem 3.7 (REPORTED: Finner 1992).** Let (Ω_i, ν_i), i ∈ I, be finitely many probability spaces, with product measure on Ω = Π_i Ω_i. For j in a finite set J let S_j ⊆ I, let f_j ≥ 0 be a measurable function of (ω_i)_{i∈S_j}, and let q_j ∈ [1, ∞]. If Σ_{j : i ∈ S_j} 1/q_j = 1 for every i ∈ I, then ∫ Π_j f_j ≤ Π_j ‖f_j‖_{L^{q_j}(Ω_{S_j})}.

The form with "≤ 1" follows. For each i with slack s_i = 1 − Σ_{j : i∈S_j} 1/q_j > 0, add the factor 1 on Ω_{{i}} with exponent 1/s_i. Its norm is 1.

**Lemma 3.8.** For every polymer γ, sup_V |z_γ(V)| ≤ ε^{#γ}, with ε = ε_6(β_0).

*Proof.* Take I = off(γ) with Haar measure on each link; the other off links integrate to 1. Take f_p = |K(U_p)| as a function of off(p), the lines fixed at V, and q_p = 6. An off link lies in 6 plaquettes of Λ_0 (Lemma 3.1 item 1), so in at most 6 of γ, and Σ_{p∋w} 1/6 ≤ 1. Theorem 3.7 gives |z_γ(V)| ≤ E_V Π_p |K(U_p)| ≤ Π_p ‖f_p‖_6. Fix all off links of p but one, u. Then U_p = A u^{±1} B is Haar distributed. By Fubini, U_p is Haar distributed under the product measure on off(p) (the exclusive-link argument of [LEMMA-0002](LEMMA-0002-HAAR-MOMENTS.md)). So ‖f_p‖_6 = ε. ∎

Exponent 6 is the least common exponent the hypothesis allows. Three unit cubes through a class-1 link w, chosen so that each of the 6 plaquettes at w is a face of exactly one of them, form a polymer of 18 plaquettes in which w lies in 6 (attack `G0-count.md` §2, scratch read). The planted fault `finner_exponent_2` of C19 cannot be caught by comparing numbers on C19's 10-plaquette filling-plus-cube set: there sup_V|z_γ| = (2t_2)¹⁰/64 at leading order (attack `G0-count.md` §2, by the merge rule of YM4-03C §7.5), below the false product ‖K‖_2¹⁰ ≥ (2t_2)¹⁰. It is caught only by a guard on the hypothesis. That guard reads the maximal off-link incidence of the set, which is 4, and tests Σ 1/q ≤ 1, which reads 2 > 1.

### 3.5 Counting: the injection, the Fuss–Catalan tail, and locality

N_w(n) is the number of polymers of n plaquettes that hold the off link w. It counts sets. It does not count classes under a symmetry. A search may deduplicate its states by canonical forms, but each class must then be weighted by the number of its members that hold w. The class-1 counts 1, 12 and 32 at n = 4, 6 and 8 are 1, 2 and 4 orbits under the 16-element stabilizer of the link (attack `G0-count.md` §6, scratch read). A head is **valid** when N(n) ≥ N_w(n) for every off link w and every 4 ≤ n ≤ 10.

Let 𝒯_D be the complete D-ary rooted tree, with D child slots labelled 1, …, D at every vertex. Let t_D(n) be the number of subtrees of 𝒯_D with n vertices that contain the root.

**Lemma 3.9 (the BFS injection).** Let G be a finite graph of maximal degree at most D and v a vertex. The number of connected vertex sets A ∋ v with #A = n is at most t_D(n). So for every off link w, the number of connected plaquette sets of n plaquettes that hold w is at most 6 t_20(n). This bounds closed and unclosed sets alike. In particular N_w(n) ≤ 6 t_20(n).

*Proof.* At each vertex u fix an injective labelling λ_u of its neighbours by {1, …, D}. For a connected A ∋ v, run breadth-first search inside A from v with a first-in first-out queue. When u leaves the queue, scan i = 1, …, D. If λ_u⁻¹(i) exists, lies in A and is not yet reached, mark it reached, queue it, and put it in child slot i of the image of u. A is connected, so every vertex of A is reached once. The result τ(A) is a subtree of 𝒯_D with #A vertices containing the root. τ(A) alone rebuilds the map onto A: the root goes to v, and the child in slot i of a node that goes to u goes to λ_u⁻¹(i). So A ↦ τ(A) is injective. For plaquettes take the graph of Lemma 3.1 item 7, of maximal degree 20. A set holds w exactly when it contains one of the 6 plaquettes through w. Sum over these 6 roots. ∎

**Lemma 3.10 (the Fuss–Catalan count).** t_D(n) = F_D(n) := C(Dn, n)/((D − 1)n + 1) = C(Dn, n − 1)/n for n ≥ 1.

*Proof.* List the vertices of a subtree in depth-first preorder, children in slot order: v_1, …, v_n. Record for each v_i its set C_i ⊆ {1, …, D} of occupied slots, with k_i = #C_i. After j vertices the number of discovered but unlisted vertices is 1 + Σ_{i≤j}(k_i − 1). So the partial sums P_j := Σ_{i≤j}(k_i − 1) satisfy P_j ≥ 0 for j < n and P_n = −1. Conversely each word (C_1, …, C_n) with these partial sums records exactly one subtree. Let 𝒜 be the set of words with Σ k_i = n − 1, and ℬ ⊆ 𝒜 the valid ones. A cyclic shift that starts after index r ∈ {0, …, n − 1} is valid exactly when P_m ≥ P_r for r < m ≤ n − 1 and P_m − 1 ≥ P_r for 0 ≤ m < r, that is, when r is the first minimizer of P over {0, …, n − 1}. So each word of 𝒜 has exactly one valid shift, and a word with total −1 has no period shorter than n. Hence #ℬ = #𝒜/n. #𝒜 = [y^{n−1}](1 + y)^{Dn} = C(Dn, n − 1). Finally C(Dn, n − 1)/n = (Dn)!/(n!((D − 1)n + 1)!) = C(Dn, n)/((D − 1)n + 1). ∎

The cycle lemma is due to Dvoretzky and Motzkin (1947), cross-reference only; the proof above is complete. F(4), …, F(12) read 20540, 784245, 31763004, 1340246340, 58281448940, 2593593086150, 117544525178080, 5406686759963586 and 251754316822792420 as exact binomials, the values frozen in C01.

**Lemma 3.11 (the ratios, for every n).** For every integer n ≥ 0,

```text
F(n+1)/F(n) = 20 * prod_{j=1}^{19} (20n + j)/(19n + j + 1).
```

Each factor is strictly increasing in n and strictly below 20/19. So F(n + 1)/F(n) is strictly increasing, strictly below μ = 20·(20/19)¹⁹ = 20²⁰/19¹⁹ for every n, and tends to μ. Moreover μ ∈ [53.00068, 53.00069].

*Proof.* F(n) = (20n)!/(n!(19n + 1)!), so F(n + 1)/F(n) = Π_{j=1}^{20}(20n + j)/[(n + 1)Π_{j=2}^{20}(19n + j)]. Use 20n + 20 = 20(n + 1) and shift j. For f_j(n) = (20n + j)/(19n + j + 1), the determinant 20(j + 1) − 19j = j + 20 is positive, so f_j increases. Also 20/19 − f_j(n) = (j + 20)/(19(19n + j + 1)) > 0, and it tends to 0. The bracket on μ is the integer inequality 5300068·19¹⁹ ≤ 100000·20²⁰ ≤ 5300069·19¹⁹. ∎

C01 checks the ratio for n ≤ 59. Lemma 3.11 holds for every n.

**Corollary 3.12 (the crude head and the tail).** The crude head N(n) = 6F(n) is valid on every Λ_0 with N even and N ≥ 8. For a valid head put S_N(y) := Σ_{n=4}^{10} N(n)yⁿ + Σ_{n≥11} 6F(n)yⁿ, a power series. For every off link w and every 0 ≤ y with μy < 1,

```text
sum_{n >= 4} N_w(n) y^n  <=  S_N(y)  <=  S(y),          and   S(y e^{-s}) <= e^{-4 s} S(y)  for every s >= 0.
```

*Proof.* Lemmas 3.9 and 3.10 give N_w(n) ≤ 6F(n), and Lemma 3.6 gives N_w(n) = 0 for n ≤ 3. Lemma 3.11 gives F(49 + j) ≤ F(49)μ^j, so Σ_{n≥49} 6F(n)yⁿ ≤ 6F(49)y⁴⁹/(1 − μy). Every term of S has degree at least 4, and 1/(1 − μye^{−s}) ≤ 1/(1 − μy). ∎

S_N and S are different objects. They differ where μy = 1: the series S_N can converge there, while the closed form S is +∞. Route A used the one letter S for both.

**Lemma 3.13 (two plaquettes per slab).** Fix a direction λ. The **λ-extent** of a plaquette p with base x is [x_λ, x_λ + 1] when λ lies in the plane of p, and the point {x_λ} otherwise. On Λ_0 read extents mod N. Let γ be a closed set of plaquettes, on Λ_0 or on ℤ⁴. If some p ∈ γ has λ-extent [c, c + 1], then at least two plaquettes of γ have λ-extent [c, c + 1].

*Proof.* p has two λ-links. Their transverse coordinates differ by 1 in the other direction of the plane of p. So their transverse odd sets differ, and at most one is empty. So one λ-link f of p is an off link. Closure puts f in a second plaquette q of γ. q holds a λ-link, so λ lies in its plane, and its λ-extent is that of f, [c, c + 1]. ∎

**Lemma 3.14 (locality and the class rule).** Let N be even with N ≥ 8, and 1 ≤ n ≤ 2N − 1. Let w be an off link of Λ_0 and w̃ a lift of w to ℤ⁴. On ℤ⁴ use the same parity definitions of line links, off links, classes and closure.

1. The projection π: ℤ⁴ → Λ_0 is a bijection from the closed connected sets of n plaquettes of ℤ⁴ that hold w̃ onto the polymers of n plaquettes of Λ_0 that hold w. So N_w(n) equals the ℤ⁴ count, on every such Λ_0.
2. N_w(n) depends only on the class of w.

So for n ≤ 15 the counts N_c(n) are the same on every fine torus with N even and N ≥ 8, including N ≡ 2 mod 4.

*Proof.* N is even, so π preserves the parity of every coordinate. So it maps line links to line links and class-c off links to class-c off links.

*Chains.* Let p̃_0, …, p̃_r be plaquettes of ℤ⁴ in which consecutive ones share an off link. Consecutive λ-extents intersect, since both contain the extent of the shared link. So the union J of the extents is an interval. Suppose J contains [m, m + N]. Each open slab (c, c + 1) ⊆ [m, m + N] meets a finite union of points and unit intervals with integer ends in an open set, so some extent equals [c, c + 1]. The chain then holds plaquettes of extent [c, c + 1] for N consecutive c, which project to all N slabs mod N.

*π is injective on every closed connected S̃ ⊂ ℤ⁴ with #S̃ ≤ 2N − 1.* Suppose p̃ and p̃ + Nv lie in S̃ with v_λ ≠ 0. A path in S̃ between them is a chain whose J contains the extent of p̃ and its shift by N v_λ. So J contains an interval [m, m + N]. By the chain step and Lemma 3.13 in ℤ⁴, S̃ holds at least 2 plaquettes of extent [c, c + 1] for each of N values of c. These are 2N distinct plaquettes, which is too many. So π(S̃) has #S̃ plaquettes. It is connected and holds w. It is closed: an off link f of π(p̃) lifts to an off link f̃ of p̃, f̃ lies in a second plaquette q̃ ∈ S̃, and π(q̃) ≠ π(p̃) holds f.

*Every polymer γ ∋ w of n plaquettes lifts.* Choose p_0 ∈ γ through w. Its lift that holds w̃ is unique, since p_0 holds w once. Fix a spanning tree of the off-link graph of γ and lift along it: when p is lifted and q shares the off link f with p, lift q so that it holds the lift of f held by the lift of p. Let p, q ∈ γ share any off link f. Suppose the lifts of p and q hold lifts of f that differ by Nv, v_λ ≠ 0. The lifted tree path from p to q is a chain whose J contains [m, m + N]. Its plaquettes project to plaquettes of γ in all N slabs mod N. Lemma 3.13 on Λ_0 gives #γ ≥ 2N, which is too many. So every shared off link lifts to a shared off link. The lift γ̃ is then closed, connected, holds w̃, and π(γ̃) = γ.

*The lift is unique.* Let S̃_1 and S̃_2 be closed connected sets of n plaquettes of ℤ⁴ that hold w̃ and project onto γ. π is injective on each, so it has an inverse L_i: γ → S̃_i. Let p, q ∈ γ share an off link f. A path in S̃_i from L_i(p) to L_i(q) is a chain. If L_i(p) and L_i(q) held different lifts of f, the chain step and Lemma 3.13 would give #S̃_i ≥ 2N. So L_i(p) and L_i(q) hold the same lift of f. Some plaquette of S̃_i holds w̃; its image p_i holds w. Every p ∈ γ through w shares w with p_i, so L_i(p) holds w̃. So L_1(p_0) = L_2(p_0), and both L_i follow the same unique lifting steps along a spanning tree. So S̃_1 = S̃_2.

*The class rule.* The maps x ↦ σ(x) + t, with σ a signed permutation of the four coordinates and t ∈ (2ℤ/Nℤ)⁴, are well defined on Λ_0 because N is even. They move coordinate parities with the coordinates. So they preserve line links, classes, plaquettes, "share an off link", closure and connectivity, and N_{g(w)}(n) = N_w(n). They act transitively on the off links of class c. Let (x, λ) have O_⊥ = O with #O = c. A coordinate permutation moves λ and O to a fixed pair. An even translation brings x_ρ to 1 for ρ ∈ O, to 0 for the other ρ ≠ λ, and x_λ into {0, 1}. If x_λ = 1, the reflection x_λ ↦ −x_λ followed by the translation by 2e_λ sends the link to the one with x_λ = 0, and it keeps every parity. ∎

C03's parenthetical "DERIVED by locality: no set of fewer than 16 plaquettes winds at fine side 8" is Lemma 3.13 with the chain step. The injectivity, lifting and uniqueness steps are also needed, and they are supplied here. The scratch cross-reads of the attacks read C03's values for n ≤ 10 on fine (ℤ/8)⁴ and fine (ℤ/10)⁴, and no set winds. That is a cross-read, not evidence. The values themselves stay a CONJECTURE until the engine and the check read them.

### 3.6 The cluster expansion and the tree-graph bound

This section is abstract. Γ is a finite set. Each γ ∈ Γ carries a finite nonempty set off(γ). γ ≁ γ′ when off(γ) ∩ off(γ′) ≠ ∅, so ≁ is reflexive and symmetric. G1 can use it with other supports.

A **cluster** is a sequence X = (γ_1, …, γ_n) ∈ Γⁿ with n ≥ 1. Every sum over clusters of length n carries the weight 1/n!. Its incompatibility graph I(X) on {1, …, n} has the edge {i, j} when γ_i ≁ γ_j. The Ursell function is φ^T(X) := Σ_G (−1)^{#edges(G)} over the connected spanning subgraphs G of I(X). It is 0 when I(X) is disconnected. For polymers, n(X) := Σ_i #γ_i is the number of plaquettes with multiplicity, and d(X) := θ·n(X). X ∋ w means w ∈ off(γ_i) for some i.

**Lemma 3.15 (the Mayer expansion).** For variables (ζ_γ)_{γ∈Γ} let Ξ(ζ) := Σ_A Π_{γ∈A} ζ_γ over the sets A ⊆ Γ of pairwise compatible elements. As formal power series,

```text
log Xi(zeta) = sum_{n >= 1} (1/n!) sum_{X in Gamma^n} phi^T(X) prod_i zeta_{gamma_i}.
```

*Proof.* Ξ(ζ) = Σ_{n≥0} (1/n!) Σ_{X∈Γⁿ} Π_i ζ_{γ_i} Π_{i<j}(1 + f_{ij}), with f_{ij} = −1 when γ_i ≁ γ_j and 0 otherwise. Repeated elements give 0, since γ ≁ γ, and each compatible set is counted n! times. Expand Π(1 + f_{ij}) over the graphs on {1, …, n} and split each graph into its connected components. The exponential formula for connected graphs (REPORTED: Stanley 1999, Corollary 5.1.6; Mayer and Mayer 1940) turns the sum over graphs into the exponential of the sum over connected graphs. For G ⊆ I(X), Π_{ij∈G} f_{ij} = (−1)^{#edges(G)}, and it is 0 otherwise. ∎

**Lemma 3.16 (the Penrose partition).** Let H be a connected graph on {1, …, n}. For a spanning tree τ ⊆ H let d_τ(i) be the tree distance from 1 and p_τ(j) the parent of j ≠ 1. Let

```text
R(tau) := tau  union  { {i,j} in H : d_tau(i) = d_tau(j) }  union  { {i,j} in H : d_tau(j) = d_tau(i) + 1 and i > p_tau(j) }.
```

Then Σ_{G ⊆ H connected spanning} (−1)^{#edges(G)} = (−1)^{n−1} #{τ : R(τ) = τ}. So |φ^T(X)| is at most the number of spanning trees of I(X), which is Σ_{τ tree on {1,…,n}} Π_{{i,j}∈τ} 1[γ_i ≁ γ_j].

*Proof.* For a connected spanning G ⊆ H let d_G be the graph distance from 1. Let T(G) join each j ≠ 1 to the least i with {i, j} ∈ G and d_G(i) = d_G(j) − 1. T(G) is a spanning tree of G with d_{T(G)} = d_G. Fix a spanning tree τ ⊆ H. If T(G) = τ, then τ ⊆ G and d_G = d_τ. Every edge of G joins levels that differ by at most 1. An edge between consecutive levels that is not a tree edge has i > p_τ(j), by the choice of the least i. So G ⊆ R(τ). Conversely let τ ⊆ G ⊆ R(τ). Then d_G ≤ d_τ since G ⊇ τ. Every edge of R(τ) changes d_τ by at most 1, so d_τ ≤ d_G along any path from 1. So d_G = d_τ. The neighbours of j at level d_τ(j) − 1 in G are p_τ(j) and vertices i > p_τ(j), so T(G) = τ. Hence the connected spanning subgraphs of H are the disjoint union of the Boolean intervals {G : τ ⊆ G ⊆ R(τ)}. On one interval the sum is (−1)^{n−1} Σ_{A ⊆ R(τ)∖τ} (−1)^{#A}. That is (−1)^{n−1} when R(τ) = τ and 0 otherwise. ∎

This is Penrose's partition (Penrose 1967, cross-reference only); the proof above is complete.

**Lemma 3.17 (the rooted-tree recursion).** Let ω: Γ → [0, ∞). For γ ∈ Γ and h ≥ 0 let

```text
M_h(gamma) := sum_{n>=1} (1/(n-1)!) sum_{tau tree on {1..n}, depth from 1 <= h} sum_{(gamma_2..gamma_n) in Gamma^{n-1}}  prod_{{i,j} in tau} 1[gamma_i ~/~ gamma_j]  prod_{i=2}^{n} omega(gamma_i),      gamma_1 := gamma.
```

Then M_0(γ) = 1 and M_{h+1}(γ) = exp(Σ_{γ′≁γ} ω(γ′) M_h(γ′)), as sums of nonnegative terms with values in [0, ∞].

*Proof.* A tree on {1, …, n} rooted at 1 with depth at most h + 1 is the same as three data: the set C of children of 1, with k = #C; a partition of {2, …, n} into k blocks, each holding exactly one element of C; and in each block a tree rooted at that element, of depth at most h. The weight factorizes over the blocks. The edge from 1 to the child c gives the factor 1[γ ≁ γ_c]. Ordered block tuples of sizes m_1, …, m_k with a root in each can be chosen in (n − 1)!/Π_j (m_j − 1)! ways. Unordered, divide by k!. Relabel each block onto {1, …, m_j} with its root as 1; this keeps the weights. Dividing by (n − 1)! leaves (1/k!) Π_j 1/(m_j − 1)!. Summing over n and the m_j gives Σ_k (1/k!) (Σ_{γ′≁γ} ω(γ′) M_h(γ′))^k. All terms are nonnegative, so the rearrangement is allowed. ∎

**Proposition 3.18 (the cluster bounds).** Let ω: Γ → [0, ∞) and α ≥ 0. Suppose that for every w,

```text
(KP_w)    sum_{gamma : w in off(gamma)}  omega(gamma) e^{alpha #off(gamma)}  <=  alpha.
```

Then:

1. (rooted) For every γ ∈ Γ, Σ_{n≥1} (1/(n−1)!) Σ_{(γ_2,…,γ_n)∈Γ^{n−1}} |φ^T(γ, γ_2, …, γ_n)| Π_{i=2}^n ω(γ_i) ≤ e^{α#off(γ)}.
2. (marked) For every Γ_0 ⊆ Γ and every ω′ ≤ ω pointwise, Σ_{n≥1} (1/n!) Σ_{X∈Γⁿ : some γ_i ∈ Γ_0} |φ^T(X)| Π_i ω′(γ_i) ≤ Σ_{γ∈Γ_0} ω′(γ) e^{α#off(γ)}.
3. (per link) For every w, Σ_{n≥1} (1/n!) Σ_{X ∋ w} |φ^T(X)| Π_i ω(γ_i) ≤ Σ_{γ ∋ w} ω(γ) e^{α#off(γ)} ≤ α.

*Proof.* 1. Let M(γ) := sup_h M_h(γ). Every tree has finite depth, so by monotone convergence M(γ) is the sum over all trees. By induction on h, M_h(γ) ≤ e^{α#off(γ)}. It holds at h = 0. If it holds at h, then

```text
sum_{gamma' ~/~ gamma} omega(gamma') M_h(gamma')  <=  sum_{w in off(gamma)} sum_{gamma' : w in off(gamma')} omega(gamma') e^{alpha #off(gamma')}  <=  alpha #off(gamma),
```

by the union bound over the links γ′ shares with γ and by (KP_w). Lemma 3.17 gives M_{h+1}(γ) ≤ e^{α#off(γ)}. Lemma 3.16 bounds |φ^T| by the sum over trees, so the left side of item 1 is at most M(γ).

2. φ^T and Π ω′ are symmetric under permutations of X. The union bound over the index i with γ_i ∈ Γ_0, and symmetry, bound the left side by Σ_n (1/(n − 1)!) Σ_{X: γ_1 ∈ Γ_0} |φ^T(X)| Π_i ω′(γ_i). Use ω′ ≤ ω for i ≥ 2 and item 1.

3. Item 2 with Γ_0 = {γ : w ∈ off(γ)} and ω′ = ω, then (KP_w). ∎

**Remark 3.19 (the Kotecký–Preiss form, and the weight).** Take Γ the polymers, ω(γ) = sup_V |z_γ| e^{d(γ)} with d(γ) = θ#γ, and a(γ) = α#off(γ). Item 1 multiplied by ω(γ) reads

```text
sum_{X : gamma_1 = gamma} (1/(n-1)!) |phi^T(X)| prod_i sup|z_{gamma_i}|  e^{d(X)}   <=   sup|z_gamma| e^{a(gamma) + d(gamma)},      d(X) = theta n(X).
```

In the multiset language of route A, a multiset cluster X ∋ γ with multiplicities m_X is realized by m_X(γ)(n − 1)!/Π m_X! sequences with γ_1 = γ, and Φ(X) = φ(X) Π z^{m_X} with φ(X) = φ^T/Π m_X!. So the display gives Σ_{X∋γ} m_X(γ) |Φ(X)| e^{d(X)} ≤ |z_γ| e^{a(γ)+d(γ)}, the per-polymer corollary with a factor m_X(γ) ≥ 1 to spare.

The weight on the left is e^{d(X)}, summed over all polymers of X. **CHANGED.** v2 writes e^{d(γ)} on the left. With e^{d(γ)} on both sides the statement reduces to Σ_{X∋γ} |Φ(X)| ≤ |z_γ| e^{a(γ)}. That is true but weaker. It cannot pay for e^{κ#Y(X)} in (C2), which needs the weight of the whole cluster. The draft's "e^d" must be read as e^{d(X)}.

(KP_w) for every w implies the hypothesis of Kotecký and Preiss (1986), Σ_{γ′≁γ} |z_{γ′}| e^{a(γ′)+d(γ′)} ≤ a(γ), by the union bound over off(γ). Their conclusion, Σ_{X≁γ} |Φ(X)| e^{d(X)} ≤ a(γ), and the per-link form of item 3 (adjoin a test element {w} with activity 0 and a({w}) = α) give the same bounds with the same constant α. That theorem is a cross-reference here (REPORTED), not an input. The reweighting z′ = z e^{d} reduces its d-form to its d-free form.

**Lemma 3.20 (the series is log ρ_1).** Assume (H1) to (H3). For every V,

```text
log rho_1(V) = log( c_0(beta_0)^{N_p} / Z ) + sum_{n>=1} (1/n!) sum_{X in Gamma^n} phi^T(X) z^X(V),      z^X := prod_i z_{gamma_i},
```

and the series converges absolutely.

*Proof.* Let r_γ := sup_V |z_γ(V)| ≤ ω(γ). Every polymer holds an off link. Summing Proposition 3.18 item 3 over the finitely many off links of Λ_0 bounds Σ_X (1/n!) |φ^T(X)| Π_i r_{γ_i} by α times the number of off links. That finite number enters no bound below. So the series L(ζ) of Lemma 3.15 converges absolutely on the polydisc |ζ_γ| ≤ r_γ. There exp L(ζ) is the formal composition, dominated by the exponential of the series with absolute values, so it converges absolutely. Lemma 3.15 then gives exp L(ζ) = Ξ(ζ) as values. At ζ = z(V), L is real (Lemma 3.3) and exp L = Ξ(V) > 0. So L(z(V)) = log Ξ(V). Lemma 3.3 converts log Ξ into log ρ_1. ∎

### 3.7 Assembling R_1

For a polymer γ let Y″(γ) be the set of coarse links ℓ such that γ holds both e_0(ℓ) and e_1(ℓ). For a cluster X let Y(X) := ∪_i Y″(γ_i). Γ_ℓ is the set of polymers with ℓ ∈ Y″(γ). So ℓ ∈ Y(X) exactly when some γ_i ∈ Γ_ℓ.

**Lemma 3.21 (what an activity depends on).** Let γ be a polymer.

1. z_γ(V) depends on V only through V restricted to Y″(γ).
2. z_γ is real and coarse-gauge invariant.
3. If Y″(γ) holds no closed loop, z_γ is constant.
4. #Y″(γ) is at most the number of quarters of γ, so #Y″(γ) ≤ #γ. Hence #Y(X) ≤ n(X) for every cluster X.

*Proof.* 1. z_γ is an integral over the off links of a product of class functions of plaquettes, with the lines at (1, V). YM4-03C §2 Lemma A applies. If γ holds no position 0 of ℓ, z_γ is constant in V_ℓ. If γ holds no position 1 of ℓ, z_γ does not hold V_ℓ. Change V one coarse link outside Y″(γ) at a time.

2. K is real, so z_γ is real. Let h: Λ_1 → SU(2). Define h̃ on Λ_0 by h̃(2x′) = h(x′) at coarse sites, h̃(m_ℓ) = h(x′) at the midpoint of each ℓ = (x′, λ), and h̃ = 1 elsewhere. A site with exactly one odd coordinate λ is the midpoint of exactly one coarse link, so h̃ is well defined. Under U ↦ h̃(x) U h̃(x + e)⁻¹, position 0 of ℓ goes from 1 to h(x′)·1·h(x′)⁻¹ = 1, and position 1 goes from V_ℓ to h(x′) V_ℓ h(x′ + e_λ)⁻¹ = (V^h)_ℓ. So the fiber over (1, V) maps onto the fiber over (1, V^h). Each off link is multiplied on the left and right by fixed elements, which preserves Haar measure. Each U_p is conjugated ([LEMMA-0001](LEMMA-0001-GAUGE-INVARIANCE.md)), so K(U_p) is unchanged. So z_γ(V^h) = z_γ(V). This is YM4-03 Theorem 4, item 3, in the line gauge.

3. Let Y″(γ) be a forest. In each tree choose a root with h = 1 there. Extend h along the tree so that h(x′) V_ℓ h(x′ + e_λ)⁻¹ = 1 on every edge, and set h = 1 elsewhere. Then V^h = 1 on Y″(γ). By items 1 and 2, z_γ(V) = z_γ(V^h), which is the value of z_γ at V = 1 on Y″(γ).

4. Only quarters hold line links, 2 each (Lemma 3.1 item 2). Each ℓ ∈ Y″(γ) takes 2 distinct held line links, and distinct coarse links have distinct line links. So 2#Y″(γ) ≤ 2·#(quarters of γ). Then #Y(X) ≤ Σ_i #Y″(γ_i) ≤ n(X). ∎

The decomposition does not depend on the line gauge. The gauge transformation at m_ℓ by V_ℓ⁻¹ sends the lines (1, V_ℓ) to (V_ℓ, 1). It moves only off links at m_ℓ, by Haar-preserving multiplications, and it keeps every K(U_p). So each z_γ, and each R_1(Y) below, is the same function of V in both gauges. Row C18 tests this.

**Proposition 3.22 (the H_1 form, conclusion (C1)).** Assume (H1) to (H3). For each set Y of coarse links that holds a closed loop let

```text
R_1(Y; V) := sum_{n>=1} (1/n!) sum_{X in Gamma^n : Y(X) = Y} phi^T(X) z^X(V),
const_1   := log( c_0^{N_p} / Z ) + sum over the clusters X whose Y(X) holds no closed loop of (1/n!) phi^T(X) z^X.
```

Then log ρ_1 = const_1 + Σ_Y R_1(Y), and const_1 does not depend on V. Every such Y has #Y ≥ 4. Each R_1(Y; ·) is real, coarse-gauge invariant and a function of V restricted to Y. Every cluster has n(X) ≥ 4 and n(X) ≥ #Y(X). R_1(∂P) holds the cluster (F_P), whose activity contains 2t_2⁴ χ_{1/2}(V_P) (Lemma 3.25).

*Proof.* Regroup the absolutely convergent series of Lemma 3.20 by Y(X). If Y(X) holds no closed loop, every Y″(γ_i) ⊆ Y(X) is a forest, so every z_{γ_i} is constant (Lemma 3.21 item 3). #Y ≥ 4 is Lemma 3.1 item 8. z^X depends on V only through V restricted to Y(X), and it is real and gauge invariant (Lemma 3.21). An absolutely convergent sum keeps these properties. n(X) ≥ 4 is Lemma 3.6, and n(X) ≥ #Y(X) is Lemma 3.21 item 4. Y″(F_P) = ∂P by Lemma 3.1 item 3. ∎

A cluster whose Y(X) holds a loop while every Y″(γ_i) is a forest is constant. It sits in R_1(Y(X)), which H_1 allows, and the norm counts it. Y need not be connected; the norm counts a disconnected Y at every link it holds.

### 3.8 The norm: conclusion (C2)

**Lemma 3.23 (the test set).** Let ℓ be a coarse link. Every polymer that holds e_0(ℓ), in particular every γ ∈ Γ_ℓ, holds at least one link of W′(ℓ) and at least two links of W(e_0(ℓ)). Hence for every f ≥ 0 on polymers,

```text
sum_{gamma in Gamma_l} f(gamma)  <=  sum_{w in W'(l)} sum_{gamma : w in off(gamma)} f(gamma),      #W'(l) = 6.
```

No set of test links does better for this argument. The 6 fillings F_Q with ℓ ∈ ∂Q lie in Γ_ℓ, and their off-link sets are pairwise disjoint. So any weights on test links that give each of them total weight at least 1 have total weight at least 6.

*Proof.* γ contains a plaquette p through e_0(ℓ). By Lemma 3.1 item 6, p has exactly one off link in W′(ℓ) and both its off links in W(e_0(ℓ)). They lie in off(γ). The fillings hold both positions of ℓ by Lemma 3.1 item 3, and they have disjoint internal links by item 4. ∎

**Proposition 3.24 (conclusion (C2)).** Assume (H1) to (H3). Then ‖R_1‖_κ ≤ 6α e^{−4(θ−κ)}. **CHANGED** from 12.

*Proof.* Fix a coarse link ℓ. Each cluster enters at most one R_1(Y), and ℓ ∈ Y(X) exactly when some γ_i ∈ Γ_ℓ. By Lemma 3.21 item 4 and κ ≥ 0, e^{κ#Y(X)} ≤ e^{κ n(X)} = Π_i e^{κ#γ_i}. So

```text
sum_{Y containing l} e^{kappa #Y} sup_V |R_1(Y;V)|  <=  sum_n (1/n!) sum_{X : some gamma_i in Gamma_l} |phi^T(X)| prod_i omega'(gamma_i),      omega'(gamma) := sup_V |z_gamma| e^{kappa #gamma}.
```

κ ≤ θ gives ω′ ≤ ω. Proposition 3.18 item 2 with Γ_0 = Γ_ℓ bounds the right side by Σ_{γ∈Γ_ℓ} ω′(γ) e^{α#off(γ)}. Every polymer has #γ ≥ 4, so ω′(γ) = ω(γ) e^{−(θ−κ)#γ} ≤ ω(γ) e^{−4(θ−κ)}. Lemma 3.23 and (KP_w) at each of the 6 links of W′(ℓ) give at most 6α e^{−4(θ−κ)}. Take the supremum over ℓ. ∎

The exponent is sharp, since the 6 fillings through ℓ have 4 plaquettes. The constant 6 is attained at leading order. The polymers of 4 plaquettes in Γ_ℓ are exactly the 6 fillings through ℓ (Lemma 3.6 and Lemma 3.1 items 3 and 8). So the order-y⁴ term of Σ_{γ∈Γ_ℓ} y^{#γ} is exactly 6y⁴. The union bound over the 12 links of W(e_0) gives 12y⁴ there, since each filling holds exactly 2 of them. The frozen 12 is this double count.

### 3.9 The readout: conclusion (C3)

The readout is c_{1/2}(P) := ⟨χ_{1/2}(V_P), log ρ_1⟩ in coarse Haar measure, as in YM4-03C §4, where ⟨χ_{1/2}(V_P), χ_{1/2}(V_P)⟩ = 1. The 4 coarse links of ∂P are distinct (Lemma 3.1 item 8), so V_P is Haar distributed.

**Lemma 3.25 (the filling).** z_{F_P}(V) = Σ_{n≥2} n t_n(β_0)⁴ χ_{(n−1)/2}(V_P). So ⟨χ_{1/2}(V_P), z_{F_P}⟩ = 2t_2(β_0)⁴.

*Proof.* Expand each of the 4 factors K(U_p) by Lemma 3.2 item 3. The expansion is absolutely and uniformly convergent, so integrate term by term. Orient the 4 quarters alike in the plane of P, so that each internal link appears as u in one word and as u⁻¹ in the other; χ_j(g⁻¹) = χ_j(g) allows this. Integrate three internal links in turn with ∫ χ_j(Au) χ_{j′}(u⁻¹B) du = δ_{jj′} χ_j(AB)/(2j + 1) (Schur orthogonality, REPORTED; the merge rule of the proof of YM4-03 Theorem 8 and of YM4-03C §7.5). Each merge forces equal spins and divides by the dimension n. After three merges the fourth internal link appears as u u⁻¹ next to the center and drops out. All four spins are equal, and the term with χ_{(n−1)/2} carries (n t_n)⁴/n³ = n t_n⁴. The remaining word runs along the 8 line links of ∂P. In the line gauge its holonomy is a conjugate of V_P (YM4-03 Proposition 2). The characters of V_P are orthonormal. ∎

**Lemma 3.26 (the readout exclusion, for polymers).** Let γ be a polymer that holds all 8 line links of ∂P, with γ ≠ F_P. Then #γ ≥ 8.

*Proof.* Let k := #(γ ∩ F_P), let n_q be the number of quarters in γ, and n_r := #γ − n_q. Only quarters hold line links (Lemma 3.1 item 2). A quarter of F_P holds 2 line links of ∂P, and any other quarter at most 1 (Lemma 3.1 item 5). So 2k + (n_q − k) ≥ 8, that is n_q ≥ 8 − k.

Case k = 0. Then #γ ≥ n_q ≥ 8.

Case 1 ≤ k ≤ 3. γ ∩ F_P is a nonempty proper subset of the 4-cycle of quarters of F_P. So some f ∈ γ ∩ F_P has a cycle neighbour f′ ∉ γ. Their common internal link e lies in no other quarter (Lemma 3.1 item 4), so f is the only plaquette of γ ∩ F_P that holds it. By closure some q ∈ γ, q ≠ f, holds e. q is not a quarter, so #O(q) = 1 (Lemma 3.1 item 4). By Lemma 3.1 item 2, q has two off links g_1, g_2 of class 2. Closure gives q_1 ∋ g_1 and q_2 ∋ g_2 in γ, both different from q. q_1 ≠ q_2, since otherwise q_1 would share two links with q (Lemma 3.1 item 1). q_1 and q_2 are not quarters, since class-2 links lie in no quarter. So n_r ≥ 3 and #γ ≥ (8 − k) + 3 = 11 − k ≥ 8.

Case k = 4. Then F_P ⊆ γ and γ ≠ F_P. γ is connected, so some q ∈ γ ∖ F_P shares an off link with a quarter of F_P. That link is an internal link of F_P, so q is not a quarter (Lemma 3.1 item 4). A plaquette that is not a quarter of F_P holds at most one internal link of F_P. Two internal links are either perpendicular at the center, and lie together only in a quarter of F_P, or opposite, and lie together in no plaquette. So the other three links of q, all off links, are links of no quarter of F_P. Closure gives three plaquettes of γ that hold them. They lie outside F_P, they differ from q, and they are pairwise distinct (Lemma 3.1 item 1). So #(γ ∖ F_P) ≥ 4 and #γ ≥ 8. ∎

**Corollary 3.27 (the readout exclusion, for clusters).** Every cluster X other than the one-term cluster (F_P) with ∂P ⊆ Y(X) has n(X) ≥ 8. The bound is attained.

*Proof.* If X has 2 or more terms, n(X) ≥ 4 + 4 by Lemma 3.6. This includes (F_P, F_P). Otherwise X = (γ) with Y″(γ) ⊇ ∂P, so γ holds all 8 line links of ∂P, γ ≠ F_P, and Lemma 3.26 applies. The 16 one-cube bumps F_P ⊕ ∂C of YM4-03C §7.5 keep 3 quarters of F_P and have 8 plaquettes. ∎

This is the form the critic asked for: the exclusion is stated for clusters. Row C09's clause "no polymer of 5, 6 or 7 plaquettes holds all of the boundary of P at both positions" holds for closed polymers. It is false for unclosed connected sets: F_P with one more plaquette through an internal link has 5 plaquettes and holds all of ∂P. Unclosed sets have activity 0 (Lemma 3.4), so C09's restriction to V-dependent polymers is the needed one. The clause is now DERIVED, not read off C03.

**Proposition 3.28 (conclusion (C3)).** Assume (H1) to (H3). Then |c_{1/2}(P) − 2t_2⁴| ≤ e_χ·6α e^{−8θ} ≤ (8489/10000)·6α e^{−8θ}. **CHANGED** from 12.

*Proof.* Absolute convergence (Lemma 3.20) lets the pairing pass through the sum over clusters. const_1 contributes 0, since ∫ χ_{1/2}(V_P) dV = 0. If some ℓ ∈ ∂P is not in Y(X), then z^X does not depend on V_ℓ (Lemma 3.21), and integrating V_ℓ first gives ∫ χ_{1/2}(A V_ℓ B) dV_ℓ = 0. So only the clusters with ∂P ⊆ Y(X) contribute. (F_P) contributes 2t_2⁴ (Lemma 3.25). Every other contributing cluster has |⟨χ_{1/2}(V_P), φ^T(X) z^X⟩| ≤ e_χ |φ^T(X)| Π_i sup|z_{γ_i}|, because V_P is Haar distributed. It has n(X) ≥ 8 (Corollary 3.27), so Π_i sup|z_{γ_i}| = e^{−θ n(X)} Π_i ω(γ_i) ≤ e^{−8θ} Π_i ω(γ_i). Fix ℓ ∈ ∂P. Each such cluster has some γ_i ∈ Γ_ℓ. Proposition 3.18 item 2 with Γ_0 = Γ_ℓ and ω′ = ω, then Lemma 3.23 and (KP_w), give

```text
| c_1/2(P) - 2 t_2^4 |  <=  e_chi e^{-8 theta} sum_{gamma in Gamma_l} omega(gamma) e^{alpha #off(gamma)}  <=  e_chi e^{-8 theta} * 6 alpha.
```

Lemma 3.2 item 5 gives e_χ < 8489/10000. ∎

At every (α, θ) the frozen T is exactly twice the final T when both use 8489/10000. So the minimizing grid index is the same for both. A sharper cover that uses all four links of ∂P gives 6 again: the four sets W′(ℓ), ℓ ∈ ∂P, are disjoint, have 24 links, and each contributing polymer meets each of them. No improvement is claimed.

The same argument bounds any decomposition from below, as row C10b uses. If f = Σ_Y R(Y) with #Y ≥ 4, then |c_P| ≤ e_χ Σ_{Y⊇∂P} sup|R(Y)| ≤ e_χ e^{−4κ} Σ_{Y∋ℓ} e^{κ#Y} sup|R(Y)|. So the norm is at least e^{4κ}|c_P|/e_χ.

### 3.10 The certificate C_0

**Lemma 3.29 (the certificate gives (H3)).** Let the head be valid, α > 0, κ ≤ θ, x = εe^{2α+θ}, μx < 1 and S(x) ≤ α. Then (KP_w) holds for every off link w, with ω(γ) = sup_V|z_γ| e^{θ#γ}. Moreover ‖R_1‖_κ ≤ 6S(εe^{2α+κ}) and |c_{1/2}(P) − 2t_2⁴| ≤ e_χ·6e^{−8θ}S(x).

*Proof.* By Lemmas 3.8 and 3.5, ω(γ)e^{α#off(γ)} ≤ ε^{#γ}e^{θ#γ}e^{2α#γ} = x^{#γ}. Corollary 3.12 gives Σ_{γ∋w} x^{#γ} = Σ_n N_w(n)xⁿ ≤ S(x) ≤ α. For the sharper norm bound, run the proof of Proposition 3.24 to Σ_{γ∈Γ_ℓ} ω′(γ)e^{α#off(γ)} ≤ Σ_{γ∈Γ_ℓ} y^{#γ} with y = εe^{2α+κ}. Lemma 3.23 and Corollary 3.12 bound this by 6S(y), and S(y) ≤ e^{−4(θ−κ)}S(x). For the readout, run the proof of Proposition 3.28 to Σ_{γ∈Γ_ℓ} x^{#γ} ≤ 6S(x). ∎

This proves Corollary G0.C. The two proved forms of δ_1 agree at θ = κ and an exact root: there 6S(εe^{2α+κ}) = 6α. At a certified dyadic α above the root, 6S(εe^{2α+κ}) is slightly smaller. The frozen structure, a prefactor times αe^{−4(θ−κ)}, is kept with the prefactor 6. Both routes prove it, and the engine reads it from its certified α.

**Lemma 3.30 (reading a certificate with enclosures).** A C_0 read at a rational α and a grid θ is sound when it uses ε⁺ ≥ ε, an upper enclosure x⁺ ≥ ε⁺e^{2α+θ}, μ⁺ ≥ μ (the exact μ or μ⁺ = 53.00069), checks μ⁺x⁺ < 1, puts 1 − μ⁺x⁺ in the tail denominator, rounds every other operation upward, and finds S⁺ ≤ α. Then μx < 1 and S(x) ≤ S⁺ ≤ α.

*Proof.* S has nonnegative coefficients and increases in x on [0, 1/μ). The tail term increases in x and in μ. ∎

The tail formula is negative for μx > 1. A read that evaluated it there could report a false MET. So the test μ⁺x⁺ < 1 comes first, and its failure reads NOT_MET.

**Lemma 3.31 (the α-search).** Fix a head with N(n) ≥ 0 and ε > 0. For θ ≥ κ let g_θ(α) := S(εe^{2α+θ}) − α on the domain {α ≥ 0 : μεe^{2α+θ} < 1}, and α_−(θ) := min{α : g_θ(α) ≤ 0} when that set is nonempty.

1. g_θ is convex in α and nondecreasing in θ.
2. If some (α, θ) is certified, then (α, κ) is certified. So θ = κ decides existence.
3. α_−(θ) and α_−(θ)e^{−4θ} are nondecreasing in θ. So the minimum over certified pairs of 6αe^{−4(θ−κ)} is 6α_−(κ), at θ = κ.
4. If any α is certified at θ, then α_−(θ) ≤ 1/8. So the frozen cap α ≤ 1/4 never binds.

*Proof.* 1. S is a power series in x with nonnegative coefficients, the tail included: 6F(49)x⁴⁹/(1 − μx) = Σ_{j≥0} 6F(49)μ^j x^{49+j}. Each term εⁿe^{n(2α+θ)} is convex in α and nondecreasing in θ. 2 follows from 1.

3. The set {α : g_θ(α) ≤ 0} shrinks as θ grows. It is closed, and g_θ → +∞ at the edge of the domain, so α_−(θ) exists when the set is nonempty, and it is nondecreasing. Every term of S has degree at least 4, so S(x) = x⁴Q(x) with Q a series with nonnegative coefficients. At the root, α_− = S(x_−) with x_− = εe^{2α_−+θ}. So α_−e^{−4θ} = ε⁴e^{8α_−}Q(x_−), and both factors are nondecreasing in θ. Every certified (α, θ) has α ≥ α_−(θ), so 6αe^{−4(θ−κ)} ≥ 6α_−(θ)e^{−4(θ−κ)} ≥ 6α_−(κ).

4. g_θ(0) = S(εe^θ) > 0. g_θ is convex and tends to +∞ at the edge of the domain. If g_θ′(0) ≥ 0, then g_θ > 0 everywhere, against the hypothesis. So g_θ has an interior minimum α* with g_θ′(α*) = 2x*S′(x*) − 1 = 0, where x* = εe^{2α*+θ}, and g_θ(α*) ≤ 0. Every term of S has degree at least 4, so xS′(x) ≥ 4S(x). So S(x*) ≤ x*S′(x*)/4 = 1/8. The least root satisfies α_− ≤ α*. So α_− = S(x(α_−)) ≤ S(x*) ≤ 1/8. ∎

The frozen condition "S⁺ ≤ α ≤ 1/4 for some grid θ" is therefore equal in effect to "S ≤ α for some α > 0 and θ ≥ κ". The same argument applies to α ↦ S(ε⁺e^{2α+θ}). The frozen read uses the exact inequality at the α its search returns, so it is sound whatever the search does. A plain fixed-point iteration from α = 0 gives lower iterates α_k ↑ α_− and never certifies by itself; that is why the frozen search does not use one.

**Lemma 3.32 (monotonicity in β_0).** ε_6(β) is nondecreasing on β ≥ 0. So a certified pair at β is certified at every β′ ∈ [0, β]. α_−(κ), and with it δ_1 = 6α_−(κ), is nondecreasing in β_0. Hence the reads "the largest β_0 on the grid with C_0 MET" (C05, C06), "the largest β_0 with C_0 MET and δ_1 < δ_crit⁻" (C13, C14) and the bisection of C04 are decided by their edge pairs.

*Proof.* Put L_β := e^{βa}/c_0(β). Then ∂_β L_β = L_β(a − E_β a), with E_β the expectation under the density L_β. So (d/dβ) ε_6⁶ = E[6(L_β − 1)⁵ L_β (a − E_β a)] = Cov_β(6(L_β − 1)⁵, a). The integrand is smooth on the compact group, so the derivative passes under the integral. For β ≥ 0 both 6(L_β − 1)⁵ and a are nondecreasing functions of a. For two nondecreasing functions f, h of one variable A, Cov(f(A), h(A)) = ½E[(f(A) − f(A′))(h(A) − h(A′))] ≥ 0, with A′ an independent copy. So ε_6⁶ is nondecreasing. g_θ is nondecreasing in ε, and the domain {α : μεe^{2α+θ} < 1} shrinks as ε grows. So a pair certified at some ε is certified at every smaller ε, and α_− is nondecreasing in ε. ∎

This closes route A's gap 5 ("the bisection assumes that δ_1 increases with β_0").

**Corollary 3.33 (the wall: a property of the Fuss–Catalan tail).** Let the counts be any finite head N(4), …, N(n_max), with any n_max ≥ 4, followed by 6F(n) for every n > n_max. If μe^κ ε ≥ 1, then no α > 0 and θ ≥ κ are certified: μx > 1 strictly, and Σ_{n>n_max} 6F(n)xⁿ = +∞.

*Proof.* For α > 0 and θ ≥ κ, x = εe^{2α+θ} > εe^κ, so μx > 1 strictly. By Lemma 3.11, x·F(n + 1)/F(n) → μx > 1, so the terms grow and the series diverges by the ratio test. α = 0 is excluded, since S > 0 when ε > 0. ∎

This is the correct quantifier for rows C04 and C15 and ledger L13 (critic blocking item 3). The wall holds for every finite head with the 6F_20(n) tail beyond it. It says nothing about a count vector with a smaller tail, such as a proved growth bound for closed sets. The wall belongs to the Fuss–Catalan tail, not to the norm. It holds at equality too. Route B's remark that C04 "is wrong at equality" is withdrawn: it missed the strict inequality x > εe^κ.

**Remark 3.34 (the head-free vector).** N(n) = 0 for n ≤ 10 is not a valid head, since N_w(4) = 1 for class-1 links (Lemma 3.6). For every valid head N, S_N ≥ S_headfree pointwise, so α_−^N(θ) ≥ α_−^{headfree}(θ). So the head-free 6α_−(κ) is a lower limit on δ_1 for every valid head. The frozen rows use it only that way.

### 3.11 Uniformity, and the proof of Theorem G0

**Uniformity, conclusion (C5).** The constants in (C2), (C3) and (C4) are built from α, θ, κ, the six links of W′(ℓ), and e_χ. Under the certificate they are built from ε_6(β_0), the head, 6F(n), D = 20, μ and 8/(3π). None involves N, the number of blocking steps or N_p. Every lemma holds on every Λ_0 with N even and N ≥ 8. Lemma 3.1 uses fine side at least 3 and coarse side at least 4. Lemma 3.9 uses only the degree bound 20. Polymers may wind around the torus; the crude counts bound them on every such torus. N_p enters only const_1 and the finiteness statement inside Lemma 3.20, which enters no bound. The refined head is lattice independent by Lemma 3.14, since 10 ≤ 2N − 1. So the refined certificate is uniform in N once the C03 values hold on one lattice. The hypothesis N = 2^K L_K with L_K ≥ 4 and at least one blocking step gives N ≥ 8. Compare YM4-04A §2 ([NOTE-YM4-04-TWO-TERNARY-BLOCKS-20261107.md](NOTE-YM4-04-TWO-TERNARY-BLOCKS-20261107.md)), whose global Cauchy remainder needs β ≤ 1/(8N_p), and YM4-04B §1 ([NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md](NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md)), whose Dobrushin bound controls correlations but not the effective action. YM4-03C §12 names the local bound as OPEN. Theorem G0 supplies it for step 0, at strong coupling, under (H3).

**Proof of Theorem G0.** (C1): Proposition 3.22, with Lemma 3.20. (C2): Proposition 3.24. (C3): Proposition 3.28. (C4): Proposition 3.18 items 1 and 3, with Remark 3.19. (C5): the uniformity paragraph. Corollary G0.C: Lemma 3.29, Corollary 3.12 and Lemma 3.31. ∎

### 3.12 What the change does to the frozen rows

The frozen 12-forms are true, since they follow from the 6-forms. They are not what the proof gives. Under gate G_attack, "a proved constant that differs from a frozen one makes every row and clause that rests on it read UNSUPPORTED". So the rows below must be re-frozen with the final constants before any engine code, or they read UNSUPPORTED. Every value below comes from exact scratch arithmetic (section 3.14), and every G1 value is CONDITIONAL on G1 as drafted, with δ_crit⁻ = 0.0496174 for MET and δ_crit⁺ = 0.0496175 for NOT_MET (C13's bracket), so either reading of δ_crit⁻ gives the same edges.

- **HYPOTHESIS.** constants: add "#W′(ℓ) = 6, the test set"; #W(e_0) = 12 stays as geometry. regime: "β_0 ≤ 0.0196" includes 0.01960, against C14 (critic blocking item 2), and the window moves. Replace with "C_0 MET and δ_1 < δ_crit⁻; on the 10⁻⁵ grid β_0 ≤ 0.02029 with the C03 head (CONJECTURE on C03, CONDITIONAL G1), and β_0 ≤ 0.01556 with the crude head (CONDITIONAL G1)". lattices: G0 needs only N even, N ≥ 8.
- **CERTIFICATES.** outputs: δ_1 := min over certified (α, θ) of 6αe^{−4(θ−κ)}; T := (8489/10000)·6αe^{−8θ} minimized over certified (α, θ). Add the reading rule of Lemma 3.30.
- **THEOREMS.** G0: the test set W′(ℓ), #W′(ℓ) = 6 (or W(e_0), met twice); the per-link condition (KP_w) with the Penrose tree-graph bound (DERIVED); "C_0 ⇒ H_1 with δ_1" with the 6-form. G1: the per-polymer corollary with e^{d(X)} on the left (Remark 3.19).
- **SCOPE.** "NOT_MET above the windows = a failure of this norm and these counts" is right for the C_0 reads. It is false for the C_1 clauses of C11 and C12, which were artifacts of the factor 12. windows: β_ind ∈ [0.02029, 0.02030) and β_ind^crude ∈ [0.01556, 0.01557), CONDITIONAL G1. The order β_ind < β_stop < β_wall(1/4) holds: 0.02029 < 0.02075 < 0.02247.
- **C01.** The injection clause covers every connected set, closed or not (Lemma 3.9). The ratio is proved for every n (Lemma 3.11); the n ≤ 59 read stays a check. If a count row is added under critic fix 4, freeze the per-root counts too, since per-link counts stay below 6F_19(n) for n ≤ 6 and would not catch `degree_19`. The per-root count at n = 2 is 20 = F(2) > F_19(2) = 19.
- **C03.** Its lattice clause is DERIVED for n ≤ 2N − 1 (Lemma 3.14). Its method counts sets holding the seed link, not symmetry classes. "Against F_20(n+2)/F_20(n) > 2000" holds only from n = 8: F(n + 2)/F(n) reads 1546.40, 1708.96, 1834.88 and 1935.16 at n = 4 to 7. Write "against F_20(10)/F_20(8) ∈ [2016.84, 2016.85] and F_20(12)/F_20(10) ∈ [2141.77, 2141.78]".
- **C04, C05, C06, C15.** Unchanged, since C_0 involves no prefactor. C04 is right at equality (Corollary 3.33). C15's "for every n_max and every count vector" becomes "for every finite head with the 6F_20(n) tail beyond n_max". At 1/45 the wall quantity is below 1, and the NOT_MET holds for the pinned certificate only.
- **C07.** δ_1 ∈ [0.0055222, 0.0055223] (frozen [0.011044, 0.011045]); 2δ_1e^{δ_1} ∈ [0.011105, 0.011106] (frozen [0.02233, 0.02234]). c(δ_1), δ_2 and Σδ_k: recompute under G1.
- **C08.** Refined δ_1 ∈ [4.7159e-6, 4.7160e-6] (frozen [9.42e-6, 9.45e-6]). Head-free limit ∈ [4.6861e-6, 4.6862e-6] (frozen [9.372e-6, 9.373e-6]). δ_1/(12e·P_10(1/100)) ∈ [1850, 1851] (frozen [3.6e3, 3.8e3]). The crude/refined ratio 1170.959 stays in [1170, 1172]. c(δ_1): recompute under G1. c_{1/2}(1/100) is the MEASURED series P_10, not a certified value: T/P_10 reads about 6.9e3 there.
- **C09.** T halves at every pair, so the minimizing indices i = 194, 150, 105, 83, 0 stay. T/P_10 reads 5.22588e-4 (1/4000), 8.36105e-3 (1/2000), 0.133825 (1/1000), 0.557254 (1/700) and 6935.17 (1/100). New brackets: [5.0e-4, 5.5e-4], [8.0e-3, 8.75e-3], [0.13, 0.14], [0.55, 0.565], [6.9e3, 7.0e3]. At 1/600 with i = 73 it reads 1.03226. So the leading coefficient is resolved to about 0.05 percent at 1/4000, and it is lost between 1/700 and 1/600, not between 1/1000 and 1/700. The low-power slack is still above 10¹²: about 2.1 × 10¹² at 1/4000. The exclusion clause is DERIVED for clusters (Corollary 3.27).
- **C10, C10b.** The norm arithmetic (12|s|e^{8κ}, 12|s|e^{4κ}, 12|s|e^{6κ}) is unchanged. C10b's c(δ_in) is G1.
- **C11.** δ_1 ∈ [0.0508265, 0.0508266] (frozen [0.10165, 0.10166]). 2δ_1e^{δ_1} ∈ [0.1069532, 0.1069533] ≤ 1/8, so C_1 reads MET (frozen NOT_MET). Remove "C_1" from predicts_NOT_MET. The crude self-map stays NOT_MET, since δ_1 > δ_crit⁺ = 0.0496175 (CONDITIONAL G1).
- **C12.** C_0 crude NOT_MET at 1/50 is unchanged. The head-free limit is δ_1 ∈ [0.0363229, 0.0363230] (frozen [0.072645, 0.072646]), with 2δ_1e^{δ_1} ∈ [0.0753330, 0.0753331] < 1/8. So the DERIVED clauses "C_1 and the self-map NOT_MET under every count model" are withdrawn. With the C03 head, δ_1 ∈ [0.0363235, 0.0363236], and C_1 and the self-map read MET (CONJECTURE on C03, CONDITIONAL G1). The row's name must change.
- **C13.** The crude self-map edge moves from 0.01369/0.01370 to 0.01556/0.01557: δ_1 ≤ 0.04961145 at 0.01556 and δ_1 ≥ 0.04979635 at 0.01557. c(49/1000), c(1/20) and δ_crit are pure G1 and unchanged.
- **C14.** The edge moves from 0.01959/0.01960 to 0.02029/0.02030: δ_1 ≤ 0.04959828 (C03) and ≤ 0.04959753 (head-free) at 0.02029; δ_1 ≥ 0.05018310 (C03) and ≥ 0.05018233 (head-free) at 0.02030. So β_ind < 0.02030 for every valid head (CONDITIONAL G1). At 1/64, refined δ_1 ∈ [1.01738e-3, 1.01739e-3] (frozen [2.0347e-3, 2.0348e-3]); c(δ_1) there: recompute under G1.
- **C16.** The formula osc ≤ (512/e)δ_m follows from the norm as frozen. δ_1 halves, and c is increasing in δ (a G1 claim), so δ_20 and the oscillation bound are at most half of the frozen [2.30e-9, 2.31e-9] and 4.35e-7. Recompute under G1.
- **C17.** The replacement clause's regime text follows HYPOTHESIS. The equality of counts on 8⁴ and 12⁴ for n ≤ 15 is DERIVED (Lemma 3.14), so its read now guards against code faults only. YM4-04A's β ≤ 1/(8N_p) was proved at b = 3, but its Cauchy argument does not depend on the blocking factor (critic fix).
- **C19.** `delta_crit_surrogate`: with δ_1 ≤ 49/1000 in place of δ_1 < δ_crit⁻, the crude read is MET at 0.01552 and NOT_MET at 0.01553, so MET is lost at 0.01553 to 0.01556 (frozen 0.01366 to 0.01369). `readout_grid_128`: T/P_10 at 1/4000 halves to [1.45e-2, 1.5e-2] (frozen [2.9e-2, 3.0e-2]). The planted false claim "the head-free self-map MET at 1/50" is no longer false under the proved constant: head-free δ_1 = 0.0363229 < δ_crit⁻ (CONDITIONAL G1). Replace it, for example by "C_0 head-free MET at 0.02076", whose miss is at C06 and rests on no prefactor. `iteration_cap_400` and `missing_tail` do not involve the prefactor. The `finner_exponent_2` guard reads the maximal off-link incidence (section 3.4).
- **PREDICTION_SUMMARY.** C11 keeps only its self-map NOT_MET, and C12 only its C_0 crude NOT_MET. List C11 and C12 among the rows conditional on G0 and G1.
- **LEDGER.** L06: a cross-reference, not relied on for G0. L08: DERIVED (Lemmas 3.9 to 3.11). L09: DERIVED in note §3 with the 6-forms. L11: the window as in HYPOTHESIS. L13: the wall belongs to the Fuss–Catalan tail (Corollary 3.33). Section 7 of the note: a growth bound for closed sets is one route to a wider window, not the only one.

The edges of C05 (0.01904/0.01905), C06 (0.02075/0.02076) and C04 (0.02247/0.02248) do not move.

### 3.13 OPEN steps, and the rows CONDITIONAL on them

1. Inside G0, no step is OPEN.
2. REPORTED inputs, not reproved: Finner (1992), Theorem 3.7; the exponential formula, Lemma 3.15; Weyl's integration formula, completeness of the characters and Schur orthogonality, Lemmas 3.2 and 3.25. Every row that rests on G0 rests on these. They are standard theorems with citations, not gaps.
3. CONJECTURE: the head values N(5), …, N(10) of C03. Lemma 3.14 removes the lattice dependence, so only the values remain. CONDITIONAL on C03: C06 (refined clauses), C08, C09 (the T/P_10 values), C12 (its refined clause), C14, and the HYPOTHESIS regime value 0.02029.
4. OPEN outside G0: G1, attacked separately. CONDITIONAL on G1: C07, C08, C10b and C10c (the c(δ_in) comparisons), C11 (C_1 and the self-map), C12, C13, C14, C16, C17 (the replacement clause) and C19 (`delta_crit_surrogate` and the planted self-map claim). The G1 values with the final δ_1 (c(δ_1), δ_2, Σδ_k, δ_20, the oscillation bound) are not recomputed here.
5. OPEN as an owner decision: the re-freeze with the final constants. Until it is filed, these rows read UNSUPPORTED under G_attack: C07, C08, C09 (T), C11, C12, C13, C14, C16, C17 (the replacement clause), and C19 (`delta_crit_surrogate` and `readout_grid_128`).

### 3.14 Scratch reads (pre-freeze disclosure)

`reviews/ym4-04c-prediction/ym4c/pkg/repair/G0-repair-checks.py` (sha256 `43a4199c2ab1785a17a25721b8f99530084b06307897f80ee405b6aa73583b54`), with output `G0-repair-checks.out` beside it (sha256 `644a81fca4dd69b3057388d77899c83d7086524d3db188f71141cd381b6aeec5`). It uses integers and Fractions only, with outward dyadic rounding at 288 bits and exact integer sixth roots. It runs in about 35 seconds. It shares no code with `G0-a-*.py`, `G0-b-checks.py` or the attack scripts. It reads:

- A. F(4..12) equal the frozen values; μ ∈ [53.00068, 53.00069]; the product formula of Lemma 3.11, strict increase and the bound below μ for n = 0 to 400; F(n + 2)/F(n) for n = 4 to 10.
- B. Machin's identity (5 + i)⁴(239 − i) = 114244(1 + i); π ≥ 1231847548/392109375 > 333/106; π enclosed to width 2e-35; 8/(3π) ∈ [0.8488263, 0.8488264]; 8489/10000 − 8/(3π) > 7.3e-5.
- C. ε_6 at 1/100, 1/64 and 1/50 inside the C02 brackets. α_− at θ = 1/4 for the crude, C03 and head-free heads at 1/100, 1/64 and 1/50, by lower iterates from α = 0 and an upper certificate, with 12α_−, 6α_− and 2δ′ at the factor 6. The crude head at 1/50 has no certificate.
- D. The edges with the factor 6 and with the factor 12, certified on both sides, and the surrogate edge.
- E. ε_6 increasing on nine grid points (a check of Lemma 3.32, not its proof).
- F. The C08 ratio and the C09 ratios T/P_10 at the frozen minimizing indices, with P_10 the MEASURED YM4-03C series.

These reads agree with the attacks' reads (`G0-kp-checks.out`, block C to E) and with the critic's fix 10. They are cross-reads before the freeze, not blind predictions, and not evidence. The engine and the independent check recompute every value by their own routes.

### 3.15 Final constants table

"Equal" means the final constant or formula is exactly the frozen one. Bracket values are pre-freeze cross-reads; the formulas are proved here.

| # | Constant or formula | Frozen | Final | Equal |
|---|---|---|---|---|
| 1 | κ | 1/4 | 1/4; the proof needs only 0 ≤ κ ≤ θ | yes |
| 2 | D, minimal degree | 20, 10 | 20, 10 (Lemma 3.1 item 7) | yes |
| 3 | plaquettes per link; Finner exponent | 6; 6 | 6; 6 (Lemma 3.1 item 1, Lemma 3.8) | yes |
| 4 | #W(e_0) | 12 | 12, as geometry | yes |
| 5 | test set in δ_1 and T | W(e_0), 12 links counted once | W′(ℓ), 6 links (W(e_0) met twice) | **no, CHANGED** |
| 6 | F_20(n) | C(20n, n)/(19n + 1) | the same (Lemma 3.10) | yes |
| 7 | μ | 20²⁰/19¹⁹ ∈ [53.00068, 53.00069] | the same (Lemma 3.11) | yes |
| 8 | F(n+1)/F(n) | increasing, below μ, checked n ≤ 59 | the same, proved for every n | yes; proved for every n |
| 9 | E\|χ_{1/2}\| | 8/(3π) ≤ 8489/10000 | the same; 8/(3π) ∈ [0.8488263, 0.8488264] | yes |
| 10 | n_max | 10 | 10; any head length gives a valid S | yes |
| 11 | S(x) | head + Σ_{11}^{48} 6F(n)xⁿ + 6F(49)x⁴⁹/(1 − μx), μx < 1 | the same; a valid bound for every valid head (Corollary 3.12) | yes |
| 12 | crude head | 6F_20(n) | valid (Corollary 3.12) | yes |
| 13 | head-free head | 0 | a lower limit only (Remark 3.34) | yes, in its role |
| 14 | ε | ε_6 = ‖K‖_{L⁶}, ε⁶ = Σ_k C(6,k)(−1)^{6−k} c_0(kβ)/c_0(β)^k | the same (Lemma 3.2) | yes |
| 15 | H_0, K, t_n, c_0 | Π_p c_0(1 + K_p), K = Σ n t_n χ, t_n = I_n/I_1, c_0 = Σ (x/2)^{2m}/(m!(m+1)!) | the same (Lemmas 3.2, 3.3) | yes |
| 16 | C_0 MET | ∃ grid θ, rational α: S⁺(ε⁺e^{2α+θ}) ≤ α ≤ 1/4 | sufficient; the cap never binds (α_− ≤ 1/8); θ = 1/4 decides; read by Lemma 3.30 | yes, equal in effect |
| 17 | KP functions | a(γ) = α#off(γ) ≤ 2α#γ, d(γ) = θ#γ | the same (Lemma 3.5, sharp) | yes |
| 18 | per-polymer corollary | Σ_{X∋γ}\|Φ\|e^{d} ≤ \|z_γ\|e^{a(γ)+d(γ)} (v2: e^{d(γ)} on the left) | the weight on the left is e^{d(X)}, d(X) = θ n(X) (Remark 3.19) | **no, CHANGED** |
| 19 | KP theorem | NAMED, relied on (L06) | not an input; Proposition 3.18 DERIVED | **no, CHANGED** (status) |
| 20 | δ_1 | min 12αe^{−4(θ−κ)} | min 6αe^{−4(θ−κ)}; sharper 6S(εe^{2α+κ}) | **no, CHANGED** |
| 21 | T | (8489/10000)·12αe^{−8θ} | (8489/10000)·6αe^{−8θ}; sharper (8/(3π))·6e^{−8θ}S(x) | **no, CHANGED** |
| 22 | θ at the δ_1 optimum | 1/4 | 1/4 (Lemma 3.31) | yes |
| 23 | lattice hypothesis | N = 2^K L_K, L_K ≥ 4; exact counts need fine sides ≥ 8 | N even, N ≥ 8; counts lattice independent for n ≤ 2N − 1 (Lemma 3.14) | yes, weakened |
| 24 | #Y″(γ) ≤ #γ; V-dependence only at size ≥ 4 | as frozen | the same (Lemma 3.21, Proposition 3.22) | yes |
| 25 | closed sets of ≤ 4 plaquettes | the fillings only | the same (Lemma 3.6) | yes |
| 26 | readout exclusion | polymers other than F_P holding ∂P: ≥ 8 plaquettes | the same for clusters, attained by the 16 bumps (Corollary 3.27) | yes, stated for clusters |
| 27 | regime | β_0 ≤ 0.0196 | C_0 MET and δ_1 < δ_crit⁻; β_0 ≤ 0.02029 (C03 head), ≤ 0.01556 (crude); CONDITIONAL G1 | **no, CHANGED** |
| 28 | C07 δ_1 at 1/100, crude | [0.011044, 0.011045] | [0.0055222, 0.0055223] | no |
| 29 | C07 2δ_1e^{δ_1} | [0.02233, 0.02234] | [0.011105, 0.011106] | no |
| 30 | C08 refined δ_1; head-free limit | [9.42e-6, 9.45e-6]; [9.372e-6, 9.373e-6] | [4.7159e-6, 4.7160e-6]; [4.6861e-6, 4.6862e-6] | no |
| 31 | C08 δ_1/(12e·c_{1/2}(1/100)) | [3.6e3, 3.8e3] | [1850, 1851] | no |
| 32 | C08 crude/refined δ_1 | [1170, 1172] | 1170.959 | yes |
| 33 | C09 T/P_10 at 1/4000, 1/2000, 1/1000, 1/700, 1/100 | [1.0e-3, 1.1e-3], [1.6e-2, 1.75e-2], [0.26, 0.28], [1.10, 1.13], [1.38e4, 1.40e4] | 5.22588e-4, 8.36105e-3, 0.133825, 0.557254, 6935.17 (same i) | no |
| 34 | C09 resolution | 0.1 % at 1/4000; lost between 1/1000 and 1/700 | 0.05 % at 1/4000; lost between 1/700 and 1/600 | no |
| 35 | C11 δ_1; 2δ_1e^{δ_1} at 1/64, crude | [0.10165, 0.10166]; [0.22505, 0.22507] > 1/8 | [0.0508265, 0.0508266]; [0.1069532, 0.1069533] ≤ 1/8 | no; C_1 flips to MET |
| 36 | C12 head-free δ_1 at 1/50 | [0.072645, 0.072646]; C_1 and self-map NOT_MET for every count model | [0.0363229, 0.0363230]; 2δ′ < 1/8; those NOT_MET clauses withdrawn | no |
| 37 | C12 refined δ_1 at 1/50 | [0.072646, 0.072648] | [0.0363235, 0.0363236] | no |
| 38 | C13 crude self-map edge | 0.01369/0.01370 | 0.01556/0.01557 | no |
| 39 | C14 refined and head-free edge | 0.01959/0.01960 | 0.02029/0.02030 | no |
| 40 | C14 refined δ_1 at 1/64 | [2.0347e-3, 2.0348e-3] | [1.01738e-3, 1.01739e-3] | no |
| 41 | C16 δ_20; oscillation | [2.30e-9, 2.31e-9]; 4.35e-7 | at most half of each; recompute under G1 | no |
| 42 | C19 surrogate window | MET lost at 0.01366–0.01369 | MET lost at 0.01553–0.01556 | no |
| 43 | C19 readout_grid_128 | [2.9e-2, 3.0e-2] | [1.45e-2, 1.5e-2] | no |
| 44 | C19 planted claim "head-free self-map MET at 1/50" | false | true under G1 as drafted; replace | no |
| 45 | C_0 edges and wall (C04, C05, C06, C15) | 0.02247/0.02248, 0.01904/0.01905, 0.02075/0.02076 | unchanged | yes |

### 3.16 Attack resolutions

The KP lens (`G0-kp.md`):

- **B1** (δ_1 and T are half the frozen values). The attack is right. The final constants are the 6-forms, marked CHANGED (Propositions 3.24 and 3.28). Section 3.12 lists every row that moves.
- **B2** (the corollary's weight). The attack is right. Remark 3.19 states and proves the corollary with e^{d(X)} on the left. The frozen formula changes.
- **m1** (bipartite premise). Right. Lemma 3.1 item 8 uses parity and winding instead.
- **m2** ("≤ 0.106953"). Right. The exact value is 0.106953269879, bracket [0.1069532, 0.1069533].
- **m3** (monotonicity in β). Right. Lemma 3.32 DERIVES it.
- **m4** (two forms of δ_1). Right. The final δ_1 is 6αe^{−4(θ−κ)}. The form 6S(εe^{2α+κ}) is a sharper corollary (Lemma 3.29).
- **m5** (the KP dependence is narrower). Right. Proposition 3.18 proves the bound. Kotecký–Preiss stays a cross-reference. The exponential formula stays REPORTED.
- **m6** (incomplete row lists). Right. Section 3.12 is complete. It adds a finding: the planted claim "head-free self-map MET at 1/50" becomes true and must be replaced.

The counting lens (`G0-count.md`):

- **B1.** As KP B1.
- **M1.** As KP m1.
- **M2** (route B's remark on C04 at equality). The attack is right, and route B was wrong. Corollary 3.33 uses x > εe^κ strictly and the ratio test.
- **M3** (C03's "> 2000"). Right. The ratio exceeds 2000 only from n = 8. C03 is reworded in section 3.12.
- **M4** (sets, not orbits). Right. N_w(n) counts sets (section 3.5).
- **M5** (class rule and locality). Right. Lemmas 3.13 and 3.14 DERIVE them. This closes gap 4 of both routes.
- **M6** (`finner_exponent_2`). Right. The guard reads the maximal incidence (section 3.4). The proof does not change.
- **M7** (`degree_19`). Right. The detector stays the degree census, plus the per-root count at n = 2 (section 3.12, C01).
- **M8** (ratio label). Right. The label is "yes; proved for every n".
- **M9** (S names two objects). Right. S_N and S are separated (Corollary 3.12).
- **M10** (pole pinning). Right. Lemma 3.30.

The assembly lens (`G0-assembly.md`):

- **B1.** As KP B1. The SCOPE sentence is also false for the C_1 clauses of C11 and C12. It is reworded in section 3.12.
- **m1.** As KP m1, with the N = 10 instance quoted after Lemma 3.1.
- **m2** (8/(3π) display). Right. The outward enclosure is [0.8488263, 0.8488264].
- **m3** (Lemma U). As counting M5.
- **m4** (the cap). Right. Lemma 3.31 item 4. The row reads "equal in effect".

No attack finding was wrong. Two claims of the derivations were wrong and are withdrawn: route A's "bipartite, since L is even", and route B's "C04 is wrong at equality". Route B's "≤ 0.106953" and its 8/(3π) display were rounding errors.

### References

- H. Finner, A generalization of Hölder's inequality and some probability inequalities, Ann. Probab. 20 (1992) 1893–1901. REPORTED.
- R. Kotecký and D. Preiss, Cluster expansion for abstract polymer models, Comm. Math. Phys. 103 (1986) 491–498. Cross-reference.
- O. Penrose, Convergence of fugacity expansions for classical systems, in T. A. Bak (ed.), Statistical Mechanics: Foundations and Applications, Benjamin (1967) 101–109. Cross-reference.
- R. P. Stanley, Enumerative Combinatorics, vol. 2, Cambridge University Press (1999), Corollary 5.1.6. REPORTED.
- J. E. Mayer and M. G. Mayer, Statistical Mechanics, Wiley (1940). Cross-reference.
- T. Bröcker and T. tom Dieck, Representations of Compact Lie Groups, Springer GTM 98 (1985), §IV.1. REPORTED.
- A. Dvoretzky and Th. Motzkin, A problem of arrangements, Duke Math. J. 14 (1947) 305–313. Cross-reference.
- M. Abramowitz and I. A. Stegun, Handbook of Mathematical Functions (1964), formula 9.6.19. Cross-reference for the name I_n.
- Repository: NOTE-YM4-03-ONE-SCALE-BLOCKING.md §2 (Proposition 2, Lemma 3), §3 (Theorem 4), §5 (the proof of Theorem 8); NOTE-YM4-03C-BLOCKED-ACTION.md §2 (the line gauge, Lemma A), §4 (the readout), §6 (Lemma B, the polymer form), §7.5 (the merge rule, the bumps), §10 (Catalan counts), §12 (OPEN); NOTE-YM4-04-TWO-TERNARY-BLOCKS-20261107.md §2; NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md §1; LEMMA-0001-GAUGE-INVARIANCE.md; LEMMA-0002-HAAR-MOMENTS.md.

## 4. Theorem G1: the step from scale k to scale k + 1 (k ≥ 1)

> **Assembly note (not part of the canonical text).** The row values of this section that use δ_1 were read with the draft's factor 12: the tables of sections 4.14 and 4.17, the chains, the C11 and C12 values, and the "about 2.7 × 10⁻⁴" of section 4.13. The final values combine G0's factor 6 with this section's λ(δ) ≤ κ and c_fin. On the β grid they are the rows "final, factor 6" and "fallback 2δ′ ≤ κ, factor 6" of the edge table in section 4.14. Section 6 and the prediction file give the rest; for example, with the factor 6 the coarse Wilson term of section 4.13 item 2 is about 5.4 × 10⁻⁴ of the refined δ_1 ∈ [4.7159e-6, 4.7160e-6]. Section 4.15 files the final values "in appended rows after line 41", a procedure for a committed v2; v2 was never committed, so the final values sit in the rows of this commit's prediction file. This section's own G1 values stand: c_fin and its flat range, δ_crit, the C10b and C10c slacks, and the fallback.

**Status.** This is the canonical section 4. It was written on November 9, 2026, from main `830fd3f`, before any engine code. It merges route A (`reviews/ym4-04c-prediction/ym4c/pkg/derive/G1-a.md`) and route B (`reviews/ym4-04c-prediction/ym4c/pkg/derive/G1-b.md`), and it resolves the three second-seat attacks (`reviews/ym4-04c-prediction/ym4c/pkg/attack/G1-treegraph.md`, verdict GAP; `reviews/ym4-04c-prediction/ym4c/pkg/attack/G1-channel.md`, HOLDS; `reviews/ym4-04c-prediction/ym4c/pkg/attack/G1-structure.md`, HOLDS). Tags: DERIVED, CONJECTURE, OPEN, REPORTED, as in NOTE-YM4-03C. DERIVED here: Theorem G1, Corollary G1-frozen, and every lemma below. REPORTED: the Kotecký–Preiss theorem (Theorem 4.9). The cited repo results are YM4-03 Lemma 3, Theorem 4 and Proposition 2, and YM4-03C §2 (the line gauge and Lemma A). No engine ran. The numbers of sections 4.14 to 4.17 are exact outward-rounded reads of the scratch scripts of section 4.19. They are not evidence.

**The result.** The frozen implication holds: C_k as frozen (2δ′ ≤ κ/2) gives H_{k+1}(κ, c(δ)δ) with the frozen c(δ). But the frozen C_k and c(δ) are not what the proof gives. The proof needs only λ(δ) := δ′ + ln(1 + δ′) ≤ κ. It gives the factor c_fin(δ) ≤ c(δ), with c_fin(δ) = e^{−4κ} exactly for 0 < δ ≤ 0.078733761 at κ = 1/4. Moreover c_fin(δ) < 1 on the whole domain λ(δ) ≤ κ. So the self-map test reduces to λ(δ_k) ≤ κ. Every frozen G1 constant and every row value built on one is replaced below, and each change is marked **[CHANGED]**. The frozen values stay true as bounds, since they follow from the final ones (Corollary G1-frozen). The NOT_MET clauses of C11 and C12, the C13 and C14 edges, C14's head-free clause, the regime clause and C10b's 3 × 10⁻⁵ clause describe the frozen formula, not the proof.

**Symbols.** These are binding for this section. a(g) = ½ Re Tr g only. b = 2 is the blocking factor only. κ = 1/4 is the norm weight. Every statement holds for 0 < κ ≤ 1/4 unless it quotes a number. The Kotecký–Preiss pair is (α, θ), and t is the tree-graph parameter. δ′ := δe^{δ}. #A is the number of elements of a set A. "Fine" means scale k, and "coarse" means scale k + 1. U is a fine configuration and V a coarse one. For a coarse link ℓ = (x′, μ), its two **positions** are the fine links e_0(ℓ) = (2x′, μ) and e_1(ℓ) = (2x′ + e_μ, μ), and its **midpoint** is m_ℓ = 2x′ + e_μ. The frozen factor is written c_frz(δ) := e^{δ}[e^{−4κ} + sup_{n≥4}(e^{−(κ/2−2δ′)n} − e^{−κn/2})]. The final one is c_fin(δ).

### 4.0 The statement

Fix N = 2^K L_K with L_K ≥ 4 and K ≥ 2, and 1 ≤ k ≤ K − 1. Put M := N/2^k.

- (H1) The fine lattice is Λ_k = (ℤ/M)⁴ and the coarse lattice is Λ_{k+1} = (ℤ/(M/2))⁴. B is the YM4-03 line map at b = 2, (BU)_μ(x′) = U_μ(2x′)U_μ(2x′ + e_μ). ν_k has the density ρ_k against product Haar measure on Λ_k. ρ_{k+1} is the density of ν_{k+1} = B_*ν_k against product Haar measure on Λ_{k+1}.
- (H2) H_k(κ, δ) holds with δ > 0. That is, log ρ_k(U) = const_k + Σ_{Y∈𝒴} R_k(Y; U) for every U. Here 𝒴 is the set of sets Y of fine links with #Y ≥ 4 that contain a closed loop. Each R_k(Y; ·) is real, bounded and measurable **[CHANGED: "bounded, measurable" added]**. It is invariant under every gauge transformation of Λ_k **[CHANGED: wording; the frozen row says "coarse-gauge invariant" for scale k]**. It is a function of U restricted to Y. The norm obeys

```text
norm_kappa(R_k) := sup_l sum_{Y containing l} e^{kappa #Y} sup_U |R_k(Y;U)|  <=  delta.
```

No Wilson term is kept outside Σ_Y R_k(Y). The coarse plaquette coupling is β_k := 2c_½(P), where c_½(P) is the χ½(V_P) Haar projection of log ρ_k. Any R_k(Y) with Y ⊇ ∂P may carry part of it (Lemma 4.22) **[CHANGED: the frozen clause "the Wilson term is carried inside R_k(∂P)" is not reproduced at k + 1; see S1]**.

With δ = 0 every R_k vanishes, ρ_k is constant, and so is ρ_{k+1}. So δ > 0 loses nothing.

Define

```text
lambda(delta) := delta' + ln(1 + delta'),                         delta' = delta e^delta,
c_fin(delta)  := max{ e^{-4 kappa},  e^{delta + lambda - 5 kappa},  e^{delta - kappa/2} sup_{f >= 4} ( e^{-(kappa - lambda) f} - e^{-kappa f} ) }.
```

The final certificate is **C_k MET iff λ(δ_k) ≤ κ**, equivalently e^{δ′}(1 + δ′) ≤ e^{κ} **[CHANGED from 2δ′ ≤ κ/2]**. The supremum over f is a maximum when λ < κ. It sits at ⌊f*⌋ or ⌈f*⌉, with f* := ln(κ/(κ − λ))/λ ≥ 4 (Lemma 4.16).

**Theorem G1 (DERIVED).** Assume (H1), (H2), 0 < κ ≤ 1/4 and λ(δ) ≤ κ. Then H_{k+1}(κ, c_fin(δ)δ) holds. In full:

- (C1) log ρ_{k+1}(V) = const_{k+1} + Σ_{Y∈𝒴′} R_{k+1}(Y; V) for every V. 𝒴′ is the set of coarse sets of at least 4 links that contain a closed loop. Each R_{k+1}(Y; ·) is real, bounded, measurable and invariant under every gauge transformation of Λ_{k+1}. It is a function of V restricted to Y.
- (C2) norm_κ(R_{k+1}) ≤ c_fin(δ)δ.
- (C3) No constant depends on N, K or the number of plaquettes.
- (C4) c_fin is nondecreasing, and c_fin(δ) ≤ max{e^{−4κ}, e^{δ−κ/2}} < 1 on the whole domain λ(δ) ≤ κ. So the self-map holds whenever C_k is MET (Corollary 4.20).

**Corollary G1-frozen (DERIVED).** Assume (H1), (H2) and the frozen C_k, 2δ′ ≤ κ/2. Then H_{k+1}(κ, c_frz(δ)δ) holds. *Proof.* ln(1 + δ′) ≤ δ′, so λ ≤ 2δ′ ≤ κ/2 ≤ κ. Theorem G1 applies. Lemma 4.18 gives c_fin(δ) ≤ c_frz(δ). H_{k+1}(κ, ·) is monotone in its second argument. ∎

The same argument gives route A's G1* (2δ′ ≤ κ, factor c*) and route B's Theorem 4.10 (2δ′ ≤ κ/2, factors c_♯ ≤ c_B) as corollaries. Section 4.10 states which bookkeeping each of them is.

### 4.1 The geometry at scale k

M = 2^{K−k}L_K is even and M ≥ 8. The coarse side M/2 is at least L_K ≥ 4. For a fine site x, write O(x) for the set of its odd coordinates.

**Lemma 4.1 (DERIVED).**

1. A fine link (y, μ) is a **line link** iff every coordinate of y other than μ is even. Then it is a position of exactly one coarse link. Every other fine link is an **off link**. Distinct coarse links have disjoint positions.
2. A fine plaquette holds 0 or 2 line links. So it holds 4 or 2 off links.
3. A line link touches only sites x with #O(x) ≤ 1. A site with O(x) = ∅ is a coarse site 2x′. A site with O(x) = {μ} is the midpoint m_ℓ of exactly one coarse link ℓ in direction μ. It touches exactly two line links, e_0(ℓ) and e_1(ℓ), and its other 6 links are off links.
4. Every closed loop of coarse links has at least 4 links.
5. Let Y be a set of line links that contains a closed loop C. Then the coarse links ℓ with e_0(ℓ), e_1(ℓ) ∈ C form a closed coarse loop. So Y″(Y) (defined below) contains a closed loop, #Y″(Y) ≥ 4 and #Y ≥ 8.

*Proof.* 1. A coarse link ℓ = (x′, μ) has positions with base 2x′ or 2x′ + e_μ, so their non-μ coordinates are even. Conversely a link (y, μ) with even non-μ coordinates is e_0 or e_1 of ((y − (y_μ mod 2)e_μ)/2, μ). Two coarse links with a common position share its base and direction, so they are equal. 2. In the plaquette (x; μ, ν), the link (x, μ) is a line link iff O(x) ⊆ {μ}, and (x + e_ν, μ) iff O(x) Δ {ν} ⊆ {μ}. These two cannot both hold. The same is true of the two ν-links. Running through O(x) = ∅, {μ}, {ν}, {μ, ν} gives exactly 2 line links, and every other O(x) gives 0. 3. The endpoints of a line link (y, μ) are y and y + e_μ, whose odd sets lie in {μ}. Let O(x) = {μ}. A link at x in direction ν ≠ μ has base x or x − e_ν, whose μ-coordinate is odd. So it is an off link. The two μ-links at x are (x − e_μ, μ) = e_0(ℓ) and (x, μ) = e_1(ℓ) for ℓ = ((x − e_μ)/2, μ). 4. The coarse torus (ℤ/L)⁴ with L ≥ 4 has no self-loops and no double links. A 3-cycle would be three signed unit steps with sum 0 mod L in every coordinate. Since L ≥ 4, the sum would be 0 in ℤ⁴, which needs an even number of steps. A winding cycle has at least L ≥ 4 links. 5. By item 3, C passes through each midpoint m_ℓ it meets along e_0(ℓ) and e_1(ℓ). Every link of C touches a midpoint, by item 3, since its two endpoints cannot both be coarse sites. So C is the subdivision of a closed coarse path through distinct coarse sites, that is, a closed coarse loop. Item 4 gives at least 4 coarse links, each with both positions in C. ∎

Item 5 is the attack's M6. For a set Y of fine links write line(Y) and off(Y) for its line links and off links. Its **coarse shadow** is

```text
Y''(Y) := { coarse links l : e_0(l) in Y and e_1(l) in Y }.
```

By item 1, 2#Y″(Y) ≤ #line(Y).

### 4.2 The pushforward in the line gauge, Lemma A, and forests

**Lemma 4.2 (the pushforward, DERIVED).** Let ρ be a bounded, positive, measurable density on fine configurations, invariant under every gauge transformation of Λ_k. Then B_*(ρ dU) has the density

```text
rho'(V) = integral over the off links of rho(U),   with every line at (U_0, U_1) = (1, V_l),
```

defined at every V. ρ′ is positive and invariant under every gauge transformation of Λ_{k+1}.

*Proof.* Let F be bounded and measurable on coarse configurations. For each coarse link, (U_0, U_1) ↦ (U_0, U_0U_1) preserves product Haar measure (YM4-03 Lemma 3). So ∫F(BU)ρ(U)dU = ∫dV F(V) ∫∏_ℓ dU_0(ℓ) ∫∏dU_off ρ(U_0, U_0⁻¹V, off). Fix one coarse link ℓ and every other variable. The gauge transformation at m_ℓ by h = U_0(ℓ) sends (U_0, U_1) to (1, U_0U_1) = (1, V_ℓ). By Lemma 4.1 item 3 it moves no other line link. It multiplies the 6 off links at m_ℓ by U_0 on one side, which preserves their Haar measure. ρ is unchanged. So the U_0(ℓ)-integrand does not depend on U_0(ℓ), and ∫dU_0(ℓ) = 1. Do this for one coarse link after another. Positivity is inherited. Invariance is Lemma 4.3 item 4 with F = ρ. ∎

By YM4-03 Theorem 4, iterated, ρ_k is such a density. Under (H2) each R_k(Y) is bounded, measurable and invariant, so ρ_k is too.

**Lemma 4.3 (Lemma A at scale k, for any invariant integrand; DERIVED).** Let F be a bounded measurable function of the fine configuration, invariant under the gauge transformations of Λ_k at the site m_ℓ. Put T(V) := ∫F ∏dU_off, with every line at (1, V).

1. If F does not depend on e_0(ℓ), then T is constant in V_ℓ.
2. If F does not depend on e_1(ℓ), then T does not involve V_ℓ.
3. Suppose F is invariant at every midpoint and depends on U only through U restricted to a set Y. Then T depends on V only through V restricted to Y″(Y).
4. If F is invariant under every gauge transformation of Λ_k, then T is invariant under every gauge transformation of Λ_{k+1}.

*Proof.* 1. The gauge transformation at m_ℓ by h sends e_0(ℓ) from 1 to h⁻¹, sends e_1(ℓ) from V_ℓ to hV_ℓ, and multiplies the off links at m_ℓ by h on one side. F is invariant and does not see e_0(ℓ). So F((1, V), off) = F((1, V with V_ℓ → hV_ℓ), h·off). Integrate over the off links, and let Haar measure absorb h. So T(V) = T(V with V_ℓ → hV_ℓ) for every h. 2. V_ℓ enters the line gauge only at e_1(ℓ). 3. If ℓ ∉ Y″(Y), one position of ℓ lies outside Y, and item 1 or 2 applies. A function that is constant in each V_ℓ with ℓ ∉ Y″(Y), the others held fixed, is a function of V restricted to Y″(Y). 4. Let g be a gauge transformation of Λ_{k+1}. Put g̃(2x′) := g(x′), g̃(m_ℓ) := g(x′) for ℓ = (x′, μ), and g̃ := 1 elsewhere. This is well defined, since coarse sites and midpoints are distinct fine sites. Under U ↦ U^{g̃}, e_0(ℓ) goes from 1 to g(x′)g(x′)⁻¹ = 1, and e_1(ℓ) goes from V_ℓ to g(x′)V_ℓ g(x′ + e_μ)⁻¹ = (V^g)_ℓ. On the off links g̃ acts by fixed left and right multiplications, which preserve Haar measure. So T(V^g) = T(V). ∎

Item 1 is the proof of YM4-03C §2 Lemma A. That proof never uses that F is a product of plaquette class functions. Item 4 uses a different extension from YM4-03 Theorem 4 item 3, which sets g̃ = 1 at the midpoints. This one keeps the line gauge (1, ·). Both are valid.

**Lemma 4.4 (forests, DERIVED).** Let S be a set of coarse links that holds no closed loop. A function of V restricted to S that is invariant under every gauge transformation of Λ_{k+1} is constant.

*Proof.* S is a forest. Root each tree at one site. Walking out from the root, a gauge transformation that is 1 at the root sets V_ℓ = 1 on each link of the tree, one link at a time, since each new link reaches a site not yet fixed. So the function equals its value at V = 1 on S. ∎

### 4.3 Y-objects in L^∞, and the exact line channel

Split 𝒴 = 𝒴_L ⊔ 𝒴_O. 𝒴_L holds the **line-supported** Y, with off(Y) = ∅. 𝒴_O holds the Y with at least one off link. Call the elements of 𝒴_O **objects**, and write o for them. For an object put f_o := #off(o) ≥ 1 and m_o := #line(o). Put

```text
w(Y) := e^{kappa #Y} sup_U |R_k(Y;U)|,        so   sum_{Y containing l} w(Y) <= delta   for every fine link l.
```

Every Y contains a link, so sup|R_k(Y)| ≤ δe^{−κ#Y} ≤ δe^{−4κ} ≤ δ.

**Lemma 4.5 (the exact line channel, DERIVED).** Let Y ∈ 𝒴_L and put R^L(Y; V) := R_k(Y; U) with every line at (1, V). Then R^L(Y; ·) is real, bounded, measurable and invariant under every gauge transformation of Λ_{k+1}. It is a function of V restricted to Y″(Y). Y″(Y) contains a closed loop, #Y ≥ 8, and

```text
e^{kappa #Y''(Y)} sup_V |R^L(Y;V)|  <=  e^{-kappa #Y/2} w(Y)  <=  e^{-4 kappa} w(Y).
```

*Proof.* Lemma 4.3 items 3 and 4 with F = R_k(Y), and no integral, since Y holds no off link. Lemma 4.1 item 5 gives the loop and #Y ≥ 8. Then 2#Y″(Y) ≤ #Y. ∎

These terms need no expansion. With the lines fixed, R_k(Y) for Y ∈ 𝒴_L is a function of V alone, and its exponential leaves the off-link integral (Lemma 4.7). So the line channel carries no e^{δ} and no cluster.

**Lemma 4.6 (objects in L^∞, DERIVED).** For o ∈ 𝒴_O put φ_o := e^{R_k(o)} − 1 and ω_o := sup_U |φ_o(U)|. Then φ_o is real, bounded, measurable, invariant under every gauge transformation of Λ_k, and a function of U restricted to o. Moreover

```text
omega_o <= e^{delta} sup_U |R_k(o;U)|,        sum_{o in Y_O, o containing l} e^{kappa #o} omega_o  <=  delta e^delta = delta'   for every fine link l.
```

*Proof.* For real x, |e^x − 1| ≤ |x|e^{|x|}. And |R_k(o)| ≤ δ. Sum over o ∋ l with the norm. ∎

No Hölder or Finner step is needed at k ≥ 1. Every bound below is a product of sup norms. This factor e^{δ} is the e^{δ} in c_fin, and δ′ is the parameter of C_k.

### 4.4 The polymer gas of the objects

A **polymer** Γ is a nonempty finite set of objects that is connected in the graph on 𝒴_O whose edges join two objects sharing an off link. Write supp Γ := ∪_{o∈Γ} o, off(Γ) := off(supp Γ) and line(Γ) := line(supp Γ). These are unions. Two polymers are **incompatible**, Γ ≁ Γ′, iff off(Γ) ∩ off(Γ′) ≠ ∅. Every object has an off link, so ≁ is reflexive and symmetric. The activity is

```text
z_Gamma(V) := integral over the off links of prod_{o in Gamma} phi_o(U),   every line at (1, V).
```

**Lemma 4.7 (the polymer representation, DERIVED).** For every V,

```text
rho_{k+1}(V) = e^{const_k} exp( sum_{Y in Y_L} R^L(Y;V) ) Xi(V),     Xi(V) = sum over compatible families {Gamma_i} of prod_i z_{Gamma_i}(V),
```

with the empty family giving 1. Ξ(V) > 0.

*Proof.* Lemma 4.2 and (H2) give ρ_{k+1}(V) = e^{const_k} ∫∏dU_off exp(Σ_{Y∈𝒴} R_k(Y; U)), lines at (1, V). The terms of 𝒴_L leave the integral. The lattice is finite, so ∏_{o∈𝒴_O}(1 + φ_o) = Σ_{𝒮⊆𝒴_O} ∏_{o∈𝒮} φ_o. Split 𝒮 into its components in the off-link graph. These are polymers that pairwise share no off link. The off links are independent Haar variables and the line links are fixed, so the integral factors over the components. Conversely, a family of pairwise compatible polymers has pairwise disjoint object sets, since a common object would give a common off link. So its union has exactly these polymers as components. So subsets and compatible families correspond one to one. Ξ(V) is the integral of exp(Σ_{o∈𝒴_O} R_k(o)) > 0. ∎

Objects that share only line links are compatible. That is correct, since line links are not integrated.

**Lemma 4.8 (the activities, DERIVED).** For every polymer Γ:

1. |z_Γ(V)| ≤ ω(Γ) := ∏_{o∈Γ} ω_o for every V.
2. z_Γ is real, bounded, measurable, and invariant under every gauge transformation of Λ_{k+1}.
3. z_Γ depends on V only through V restricted to Y″(Γ) := Y″(supp Γ). And 2#Y″(Γ) ≤ #line(Γ).

*Proof.* 1. Haar measure is a probability measure. 2. Each φ_o is real. Measurability is Fubini. Invariance is Lemma 4.3 item 4 with F = ∏_{o∈Γ} φ_o. 3. Lemma 4.3 item 3 with Y = supp Γ, and section 4.1. ∎

### 4.5 Kotecký–Preiss, and the per-polymer corollary

A **cluster** X is a finite nonempty multiset of polymers, with multiplicities m_X(Γ), whose incompatibility graph is connected. φ(X) is its Ursell coefficient, and Φ(X; z) := φ(X)∏_Γ z(Γ)^{m_X(Γ)}. For a function d on polymers put d(X) := Σ_Γ m_X(Γ)d(Γ). X ∋ Γ means m_X(Γ) ≥ 1. X ≁ Γ means that some polymer of X is incompatible with Γ. {Γ} is the cluster with one copy of Γ, and φ({Γ}) = 1.

**Theorem 4.9 (Kotecký and Preiss 1986, REPORTED).** Let 𝒫 be a finite set with a reflexive, symmetric relation ≁. Let z: 𝒫 → ℂ, a: 𝒫 → (0, ∞) and d: 𝒫 → [0, ∞). Suppose that for every Γ ∈ 𝒫

```text
(KP)   sum_{Gamma' ~/~ Gamma} |z(Gamma')| e^{a(Gamma') + d(Gamma')}  <=  a(Gamma).
```

Then Ξ(z) ≠ 0, Σ_X |Φ(X; z)| < ∞, log Ξ(z) = Σ_X Φ(X; z), and Σ_{X≁Γ} |Φ(X; z)|e^{d(X)} ≤ a(Γ) for every Γ ∈ 𝒫.

This is the theorem of section 3, used in the same form, with d in the hypothesis and e^{d(X)} in the conclusion. If z is real and (KP) holds, then (KP) holds for sz with s ∈ [0, 1]. So Ξ(sz) is real, continuous in s, never 0, and Ξ(0) = 1. So Ξ(z) > 0, and the series is its real logarithm.

**Corollary 4.10 (the per-polymer corollary, DERIVED from Theorem 4.9).** Assume (KP). For every Γ ∈ 𝒫:

```text
(a)   sum_{X containing Gamma} |Phi(X;z)| e^{d(X)}                    <=  |z(Gamma)| e^{a(Gamma) + d(Gamma)},
(b)   sum_{X containing Gamma, X != {Gamma}} |Phi(X;z)| e^{d(X)}      <=  |z(Gamma)| e^{d(Gamma)} ( e^{a(Gamma)} - 1 ).
```

*Proof.* (a) Let η > 0. Add a marker Γ̂ with z(Γ̂) = 0, d(Γ̂) = 0 and a(Γ̂) = |z(Γ)|e^{a(Γ)+d(Γ)} + η, incompatible with itself and with Γ only. (KP) holds at Γ̂, since its left side is |z(Γ)|e^{a(Γ)+d(Γ)}. At every other polymer the left side gains at most the term of Γ̂, which is 0. A cluster that holds Γ̂ has Φ = 0. Every other cluster of the enlarged set is a cluster of 𝒫 with the same Φ, since φ depends only on the incompatibility graph among its members. Theorem 4.9 at Γ̂ bounds the clusters of 𝒫 that hold Γ by a(Γ̂). Let η → 0. (b) The cluster {Γ} enters (a) with |z(Γ)|e^{d(Γ)}. Subtract it. ∎

The left side carries e^{d(X)}, not e^{d(Γ)} **[CHANGED: the v2 THEOREMS row writes e^{d(γ)}; F3]**. The assembly needs e^{d(X)}.

### 4.6 The tree-graph bound

Fix a total order on 𝒴_O. For a polymer Γ and a fine link e ∈ supp Γ, the **root** of Γ at e is the least object of Γ that contains e.

**Lemma 4.11 (the root decomposition, DERIVED).** Let e ∈ supp Γ, let o be the root of Γ at e, and let Γ ≠ {o}. Each component C of Γ ∖ {o} in the off-link graph has an object that shares an off link with o. Let e_C be the least off link of o held by an object of C. Then C ↦ e_C is injective. So Γ ↦ (o, (C_{e′})_{e′∈off(o)}), with C_{e′} the component indexed by e′ or ∅, is injective. Each nonempty C_{e′} is a polymer with e′ ∈ off(C_{e′}) and fewer objects than Γ.

*Proof.* Γ is connected. A path in Γ from an object of C to o leaves C only through o, since C is a component of Γ ∖ {o}. So its last object in C shares an off link with o. If e_C = e_{C′} with C ≠ C′, then objects of C and C′ share that off link, so they are adjacent in Γ ∖ {o}, and C = C′. Γ = {o} ∪ ⋃_C C, so the data determine Γ. ∎

**Lemma 4.12 (the tree-graph bound, DERIVED).** Let ν_o ≥ 0 for o ∈ 𝒴_O, put ν(Γ) := ∏_{o∈Γ} ν_o, and let t ≥ 0. Write s(o) := #off(o). Suppose

```text
(T)   sum_{o in Y_O, e in o} nu_o (1 + t)^{s(o)}  <=  t      for every off link e.
```

Then:

1. T_ν(e) := Σ_{Γ : e ∈ off(Γ)} ν(Γ) ≤ t for every off link e.
2. For every fine link e, line or off, and every object o ∋ e, Σ_{Γ with root o at e, #Γ ≥ 2} ν(Γ) ≤ ν_o[(1 + t)^{s(o)} − 1].

*Proof.* 1. Let T_n(e) be the same sum over polymers of at most n objects, and T_0 := 0. Root Γ at e. By Lemma 4.11, and dropping every constraint among the components,

```text
T_n(e)  <=  sum_{o containing e} nu_o prod_{e' in off(o)} (1 + T_{n-1}(e')).
```

If T_{n−1} ≤ t at every off link, the right side is at most Σ_{o∋e} ν_o(1 + t)^{s(o)} ≤ t, by (T). 𝒴_O is finite, so T_ν(e) = T_n(e) for large n. 2. The same decomposition, with at least one component nonempty, gives at most ν_o[∏_{e′∈off(o)}(1 + T_ν(e′)) − 1]. Item 1 bounds each T_ν(e′) by t. ∎

Attachments happen only at off links, because polymers are connected only through off links. So (T) is needed at off links only, and it counts off links only. Since (1 + t)^s ≤ e^{ts}, the frozen form "Σ_{o∋e} ω_o e^{t s(o)} ≤ t" implies (T) **[CHANGED: the frozen clause left s(o), ω and the range of e undefined (F4, M5); here s(o) = #off(o), ν is the KP-weighted activity of section 4.7, e runs over off links, and the hypothesis is the weaker (1 + t) form that the induction uses]**. A scratch read of item 1 and item 2 on 12 random hypergraphs, with (T) at equality, is in section 4.19. It checks examples; it is not the proof.

### 4.7 The Kotecký–Preiss pair at step k

At step k, take

```text
a(Gamma) := alpha #off(Gamma),     d(Gamma) := theta #Gamma,     #Gamma := (1/2) #line(Gamma),     alpha = t = delta',  theta = kappa,
nuTilde_o := omega_o e^{a({o}) + d({o})} = omega_o e^{delta' f_o + (kappa/2) m_o}.
```

So a(γ) = α#off(γ) is the frozen formula, with α = δ′. And d(γ) = θ#γ is the frozen formula with θ = κ, once #γ is defined at step k as half the number of line links of the support **[CHANGED: the frozen rows never define #γ at k ≥ 1 (F1)]**. With this definition #Y″(Γ) ≤ #Γ, by Lemma 4.8 item 3, as #Y″(γ) ≤ #γ at step 0. So θ is a weight per coarse link in both steps, paid here at κ/2 per fine line link.

**Lemma 4.13 (DERIVED).** Assume λ(δ) ≤ κ. Then:

1. Σ_{o∋e} ν̃_o (1 + δ′)^{f_o} ≤ δ′ for every off link e.
2. T(e) := Σ_{Γ : e ∈ off(Γ)} ∏_{o∈Γ} ν̃_o ≤ δ′ for every off link e.
3. ω(Γ)e^{a(Γ)+d(Γ)} ≤ ∏_{o∈Γ} ν̃_o for every polymer Γ.
4. (KP) holds on the set of polymers, for the activity ω(Γ), and for z_Γ(V) at every V.

*Proof.* 1. ν̃_o(1 + δ′)^{f_o} = ω_o e^{(δ′ + ln(1+δ′))f_o + (κ/2)m_o} = ω_o e^{λ f_o + (κ/2)m_o} ≤ ω_o e^{κ(f_o + m_o)} = ω_o e^{κ#o}, since λ ≤ κ. Lemma 4.6 bounds the sum by δ′. 2. Lemma 4.12 item 1 with ν = ν̃ and t = δ′. 3. #off(Γ) ≤ Σ_{o∈Γ} f_o and #line(Γ) ≤ Σ_{o∈Γ} m_o. 4. Every Γ′ ≁ Γ holds some e ∈ off(Γ). By item 3 the left side of (KP) is at most Σ_{e∈off(Γ)} T(e) ≤ δ′#off(Γ) = a(Γ). And a(Γ) ≥ δ′ > 0. Lemma 4.8 item 1 passes (KP) to z_Γ(V). ∎

**Why this is the weakest hypothesis of this proof.** With α = t = δ′ and θ = κ pinned, the proof uses λ ≤ κ at one place: item 1, for objects with m_o = 0 and many off links. If λ > κ, an input with its whole norm on such objects can make item 1 fail by the factor e^{(λ−κ)f_o}, which is unbounded in f_o. So λ ≤ κ is the condition under which this proof closes. It is not shown to be necessary for H_{k+1}. The frozen 2δ′ ≤ κ/2 is the uniform bookkeeping, which charges a, t and θ#γ to every fine link: then item 1 reads ω_o e^{(2δ′ + κ/2)#o} ≤ ω_o e^{κ#o} (Remark 4.18). Route A's 2δ′ ≤ κ is this proof with e^{δ′f} in place of (1 + δ′)^f in (T). Two further weakenings would change a pinned parameter, so they are not adopted: δe^{δe^{−4κ}} in place of δ′ (since |R_k(o)| ≤ δe^{−4κ}), and a t smaller than δ′.

**The literal readings fail (F1).** With #γ := the number of fine links of γ, the KP hypothesis fails on an explicit admissible input at δ = 1/100: the attack's instance on fine (ℤ/8)⁴ has a KP left side 0.0208596 at {p_0}, against a({p_0}) = 2δ′ = 0.0202010 (`reviews/ym4-04c-prediction/ym4c/pkg/attack/g1tg/g1tg_literal_d.py`). With #γ := the number of objects, the step e^{κ#Y(X)} ≤ e^{d(X)} of section 4.8 fails on C10c's object, which has #Y″ = 4 and one object. On the same instance, the d of this section gives a left side of at most 0.0076740784 < 2δ′ (section 4.19). So the reading matters, and it is fixed here.

### 4.8 Assembling H_{k+1}

For a cluster X put Y(X) := ∪_{Γ∈X} Y″(Γ), a union of coarse sets. Put Φ(X; V) := Φ(X; z(V)) and Φ̄(X) := |φ(X)|∏_Γ ω(Γ)^{m_X(Γ)}. By Lemma 4.8 item 1, sup_V |Φ(X; V)| ≤ Φ̄(X) = |Φ(X; ω)|. So Theorem 4.9 and Corollary 4.10 apply to Φ̄ with the activity ω. Each Φ(X; V) is a product of separate off-link integrals. So it depends on V only through Y(X), not through Y″ of the union of the supports. If e_0(ℓ) lies only in Γ_1 and e_1(ℓ) only in Γ_2, then Φ does not involve V_ℓ.

**Proposition 4.14 (conclusion (C1), DERIVED).** Assume (H1), (H2) and λ(δ) ≤ κ. For Y ∈ 𝒴′ put

```text
R_{k+1}(Y;V) := sum_{Y' in Y_L : Y''(Y') = Y} R^L(Y';V)  +  sum_{X : Y(X) = Y} Phi(X;V),
const_{k+1}  := const_k + sum_{X : Y(X) holds no closed loop} Phi(X;V).
```

Then const_{k+1} does not depend on V, log ρ_{k+1} = const_{k+1} + Σ_{Y∈𝒴′} R_{k+1}(Y), and each R_{k+1}(Y; ·) is real, bounded, measurable, invariant under every gauge transformation of Λ_{k+1}, and a function of V restricted to Y.

*Proof.* Lemma 4.7 gives log ρ_{k+1} = const_k + Σ_{𝒴_L} R^L + log Ξ. Lemma 4.13 gives (KP) at every V. Theorem 4.9 gives log Ξ(V) = Σ_X Φ(X; V), real. The majorant Σ_X Φ̄(X) ≤ Σ_Γ ω(Γ)e^{a(Γ)+d(Γ)} < ∞ (Corollary 4.10 (a), on a finite polymer set) does not depend on V. So the regrouping by Y(X) is allowed, and each R_{k+1}(Y; ·) is a uniform limit of bounded measurable functions. Each Φ(X; ·) is real and invariant (Lemma 4.8). Each R^L(Y′) has Y″(Y′) holding a loop (Lemma 4.5). A Φ(X) whose Y(X) holds no loop is a gauge-invariant function on a forest, so it is constant (Lemma 4.4). Every coarse set that holds a loop has at least 4 links (Lemma 4.1 item 4). ∎

The output Y may be disconnected, for example two coarse loops whose polymers met through a fine off link. H_{k+1} allows that. At the next step such a Y is one object. No step uses that an object is connected, that an input Y holds a loop, or that #Y ≥ 4. These conditions are only reproduced.

### 4.9 Root-object bookkeeping, and c_fin

For f ≥ 1, m ≥ 1 and f + m ≥ 4 define

```text
q(f,m) := e^{-kappa (f + m)} e^{kappa m / 2} [ e^{-kappa (m mod 2)/2} * 1[m >= 8]  +  e^{lambda f} - 1 ],      Q(lambda) := sup_{f,m} q(f,m).
```

**Proposition 4.15 (conclusion (C2), DERIVED).** Assume (H1), (H2) and λ(δ) ≤ κ. Then, for every coarse link ℓ with e_0 := e_0(ℓ),

```text
sum_{Y containing l} e^{kappa #Y} sup_V |R_{k+1}(Y;V)|  <=  e^{-4 kappa} sum_{Y' in Y_L, Y' containing e_0} w(Y')  +  e^{delta} sum_{o in Y_O, o containing e_0} q(f_o, m_o) w(o)
                                                         <=  max{ e^{-4 kappa}, e^{delta} Q(lambda) } delta.
```

*Proof.* Each Y′ ∈ 𝒴_L and each cluster X enters one R_{k+1}(Y) only. So the left side is at most A_L + A_O, with

```text
A_L := sum over Y' in Y_L with l in Y''(Y') of  e^{kappa #Y''(Y')} sup|R^L(Y')|,
A_O := sum over clusters X with l in Y(X) and Y(X) holding a loop of  e^{kappa #Y(X)} PhiBar(X).
```

*The line channel.* If ℓ ∈ Y″(Y′), then e_0 ∈ Y′. Lemma 4.5 gives A_L ≤ e^{−4κ}Σ_{Y′∈𝒴_L, Y′∋e_0} w(Y′).

*The objects.* Let X enter A_O. Some Γ ∈ X has ℓ ∈ Y″(Γ), so e_0 ∈ supp Γ. Let o be the root of Γ at e_0. Since e_0 is a line link, m_o ≥ 1 **[CHANGED: route A's Q took m ≥ 0 (F5, M1)]**. Exactly one of three cases holds. (i) Γ = {o} and X = {Γ}. (ii) Γ = {o} and X ≠ {Γ}. (iii) #Γ ≥ 2. So every X of A_O is counted at least once in

```text
A_O  <=  sum_{o in Y_O, o containing e_0} [ S_1(o) + S_2(o) + S_3(o) ],
S_1(o) := e^{kappa #Y''(o)} omega_o * 1[ Y''(o) holds a loop ],
S_2(o) := sum_{X containing {o}, X != {{o}}} e^{d(X)} PhiBar(X),
S_3(o) := sum over Gamma with root o at e_0 and #Gamma >= 2 of  sum_{X containing Gamma} e^{d(X)} PhiBar(X).
```

Here S_2 and S_3 use e^{κ#Y(X)} ≤ e^{d(X)}. That holds because #Y(X) ≤ Σ_Γ m_X(Γ)#Y″(Γ) ≤ Σ_Γ m_X(Γ)#Γ. Write f := f_o and m := m_o.

- S_1(o) ≤ ω_o e^{κ⌊m/2⌋} 1[m ≥ 8]. Indeed #Y″(o) ≤ ⌊m/2⌋, and a loop needs #Y″(o) ≥ 4 (Lemma 4.1 item 4). This is Lemma A's both-positions rule: a V-dependent single object holds 8 or more line links.
- S_2(o) ≤ ω_o e^{(κ/2)m}(e^{δ′f} − 1), by Corollary 4.10 (b) for ω at Γ = {o}, where a({o}) = δ′f and d({o}) = (κ/2)m.
- S_3(o) ≤ Σ_Γ ω(Γ)e^{a(Γ)+d(Γ)} ≤ Σ_Γ ∏ν̃ ≤ ν̃_o[(1 + δ′)^f − 1] = ω_o e^{(κ/2)m}(e^{λf} − e^{δ′f}), by Corollary 4.10 (a), Lemma 4.13 item 3, Lemma 4.12 item 2 with t = δ′ (whose hypothesis is Lemma 4.13 item 1), and e^{δ′f}(1 + δ′)^f = e^{λf}.

Adding, S_1 + S_2 + S_3 ≤ ω_o e^{(κ/2)m}[e^{−κ(m mod 2)/2}1[m ≥ 8] + e^{λf} − 1] = ω_o e^{κ#o}q(f, m). Lemma 4.6 gives ω_o e^{κ#o} ≤ e^{δ}w(o). This is the first line.

*Together.* The line roots and the object roots share the budget of the one fine link e_0: Σ_{Y′∈𝒴_L∋e_0} w + Σ_{o∈𝒴_O∋e_0} w = Σ_{Y∋e_0} w(Y) ≤ δ. This is the second line. Take the supremum over ℓ. ∎

The first line is the **per-root bound**. It is sharper than c_fin(δ)δ, and section 4.12 uses it as a falsifier. No test-set factor appears. In G0 a polymer holding both positions of ℓ had to be reached through the plaquettes at e_0. Here the root contains e_0 itself, and the fine norm at e_0 already sums over all roots.

**Lemma 4.16 (Q in closed form, DERIVED).** Let 0 < κ ≤ 1/4, 0 < λ ≤ κ and g(f) := e^{−(κ−λ)f} − e^{−κf}. Then

```text
Q(lambda) = max{ e^{-5 kappa + lambda},  e^{-kappa/2} sup_{f >= 4} g(f) }.
```

If λ < κ, the supremum over f is a maximum, taken at ⌊f*⌋ or ⌈f*⌉ with f* := ln(κ/(κ − λ))/λ ≥ 1/κ ≥ 4. If λ = κ, sup_f g(f) = 1, not attained.

*Proof.* On the real half-line g′(x) > 0 iff e^{λx} < κ/(κ − λ), that is x < f*. With u := λ/κ ∈ (0, 1), f* = ln(1/(1 − u))/(κu) ≥ 1/κ, since ln(1/(1 − u)) ≥ u. So g increases on [0, 1/κ] ⊇ [0, 4] and decreases after f*. Case m ≥ 8 even: q = e^{−κm/2}e^{−(κ−λ)f}, largest at (f, m) = (1, 8), where it is e^{−5κ+λ}. Case m ≥ 9 odd: q ≤ e^{−κ(f + m/2)}e^{λf} ≤ e^{−9κ/2}e^{−(κ−λ)} < e^{−5κ+λ}. Case 1 ≤ m ≤ 7: q = e^{−κm/2}g(f) with f ≥ max(1, 4 − m). For m = 1 this is e^{−κ/2}g(f) with f ≥ 3, and g(3) < g(4). For m ≥ 2 it is at most e^{−κ}g(f) ≤ e^{−κ}sup_{f≥4}g(f), since g increases on [0, 4]. Both values are attained, at (1, 8) and at (f, 1). At λ = κ, g(f) = 1 − e^{−κf} increases to 1. ∎

So c_fin(δ) = max{e^{−4κ}, e^{δ}Q(λ)} is the formula of section 4.0, and Propositions 4.14 and 4.15 with Lemma 4.16 prove Theorem G1 (C1) to (C3). The three entries of c_fin are the line channel; a single object with 1 off link and 8 line links, with its clusters; and a root with 1 line link and f off links, with its clusters. A brute-force supremum of q over 1 ≤ f ≤ 60, 1 ≤ m ≤ 40 agrees with the closed form at six values of δ from 0.01 to 0.11 (section 4.19). Its maximizer moves from (1, 8) to (f, 1) between δ = 0.07 and δ = 0.08.

**Lemma 4.17 (c_fin < 1 on the whole domain, DERIVED).** Let 0 < κ ≤ 1/4 and λ(δ) ≤ κ. Then δ < κ/2 and c_fin(δ) ≤ max{e^{−4κ}, e^{δ−κ/2}} < 1.

*Proof.* λ increases with δ. Put x := (κ/2)e^{κ/2}. Then ln(1 + x) ≥ x − x²/2, so λ(κ/2) ≥ x(2 − x/2) = κe^{κ/2}(1 − x/4). Since e^{1/8} < 8/7, x ≤ κ·(4/7), so 1 − x/4 ≥ 1 − κ/7. And e^{κ/2} ≥ 1 + κ/2. So λ(κ/2) ≥ κ(1 + κ/2)(1 − κ/7) > κ, since κ/2 − κ/7 − κ²/14 > 0 for κ < 5. So λ(δ) ≤ κ forces δ < κ/2. The second entry of c_fin is at most e^{δ−4κ}, since λ ≤ κ. The third is at most e^{δ−κ/2}, since g < 1. And e^{−4κ} < 1. ∎

At κ = 1/4 the domain is δ ≤ δ_crit,fin with δ_crit,fin ∈ [0.114846768, 0.114846769]. There c_fin ≤ e^{0.114846769 − 1/8} ≤ 0.989898139.

### 4.10 The frozen formula, and the other bookkeepings

**Lemma 4.18 (DERIVED).** On 2δ′ ≤ κ/2, c_fin(δ) ≤ c_*(δ) < c_frz(δ), where c_* is route A's c* (roots with m ≥ 0, rate κ − 2δ′).

*Proof.* λ ≤ 2δ′, and each entry of c_fin increases with λ. So c_fin is at most the same formula at λ = 2δ′ with m ≥ 1, which is at most route A's c*, a supremum over m ≥ 0. Route A's Lemma 4.17 compares root by root and gives c* < c_frz: the single-object part of q is at most e^{−5κ} < e^{−4κ}; the rest is at most e^{−κn/2}(e^{2δ′n} − 1) with n = f + m, which is the frozen bracket at n; and the line channel has no e^{δ}. ∎

**Remark 4.18a (what the frozen formula is; corrects route A's Remark 4.18, finding M2).** Charge a, t and θ#γ to every fine link: a_u(Γ) := δ′Σ_{o∈Γ}#o, d_u(Γ) := (κ/2)Σ_{o∈Γ}#o, attachments at every link. Then item 1 of Lemma 4.13 needs 2δ′ + κ/2 ≤ κ, which is the frozen C_k. Per root of n links, the bound per unit e^{δ}w(o) is e^{−κn/2}1[n ≥ 8] + g_fr(n), with g_fr(n) := e^{−(κ/2−2δ′)n} − e^{−κn/2}. Its maximum over n is e^{−8(κ/2−2δ′)}. So the uniform per-root bound is route B's c_B(δ) = exp(δ + 16δ′ − 4κ). The frozen c_frz makes two further relaxations. It puts e^{δ} on the exact line channel. And it adds the two channel suprema, where the proof needs only the supremum of their per-root sum. So c_frz = c_B exactly when the frozen maximizer is n = 8, which holds for δ ≤ δ_eq with δ_eq ∈ [0.0070256343, 0.0070256344]. That value is route B's read; the channel attack reproduces it. Route A's "exactly the uniform bookkeeping" was wrong. Route B's c_♯ ≤ c_B is this uniform bookkeeping with the root sum kept exact.

### 4.11 Monotonicity, the self-map, and two readouts

**Lemma 4.19 (DERIVED).** c_fin is nondecreasing on {δ > 0 : λ(δ) ≤ κ}. It is constant, equal to e^{−4κ}, on an initial interval **[CHANGED: the frozen self_map clause says "c is increasing"; S4]**.

*Proof.* δ′ and λ increase with δ. For fixed f, e^{−(κ−λ)f} − e^{−κf} increases with λ. A supremum of nondecreasing functions is nondecreasing, and so is a product of positive nondecreasing factors. The maximum of nondecreasing entries is nondecreasing. ∎

**Corollary 4.20 (the self-map, uniform in N and K; DERIVED).** Suppose H_k(κ, δ_k) holds and λ(δ_k) ≤ κ. Put δ_{j+1} := c_fin(δ_j)δ_j for k ≤ j ≤ K − 1. Then for every j with k ≤ j ≤ K, H_j(κ, δ_j) holds, and

```text
delta_j  <=  c_fin(delta_k)^{j-k} delta_k,          sum_{j=k}^{K} delta_j  <=  delta_k / (1 - c_fin(delta_k)).
```

*Proof.* Induction on j. If H_j(κ, δ_j) holds with δ_j ≤ δ_k, then λ(δ_j) ≤ κ, since λ is increasing. Theorem G1 gives H_{j+1}(κ, δ_{j+1}). Lemma 4.19 gives c_fin(δ_j) ≤ c_fin(δ_k). Lemma 4.17 gives c_fin(δ_k) < 1, so δ_{j+1} ≤ δ_j. Sum the geometric series. Nothing depends on N or K, beyond j ≤ K. ∎

So the final self_map clause reads: **MET iff λ(δ_k) ≤ κ** **[CHANGED from "C_k MET and c(δ_k) < 1"; the second test is now automatic]**, with the indices written as above **[CHANGED: S8]**. The admissibility test reads: β_0 with C_0 MET and λ(δ_1) ≤ κ, equivalently δ_1 ≤ δ_crit,fin **[CHANGED]**.

**Lemma 4.21 (the oscillation readout of C16, DERIVED).** Under H_m(κ, δ) on a torus with L_m links, Σ_Y sup_V|R_m(Y; V)| ≤ L_m δ e^{−4κ}/4, and osc_V log ρ_m ≤ L_m δ e^{−4κ}/2. On a coarse 4⁴ torus with 1024 links and κ = 1/4, osc_V log ρ_m ≤ (512/e)δ.

*Proof.* Σ_Y sup|R(Y)| = Σ_l Σ_{Y∋l} sup|R(Y)|/#Y ≤ Σ_l Σ_{Y∋l} w(Y) · max_{n≥4} e^{−κn}/n ≤ L_m δ e^{−4κ}/4, since e^{−κn}/n decreases. The oscillation of a sum is at most twice the sum of the suprema. ∎

This readout is extensive in the volume. The uniformity clause (C3) covers the step bounds. C16's readout is a bound per final torus **[CHANGED: wording; S8]**.

**Lemma 4.22 (the plaquette coefficient at every scale, DERIVED).** Let m ≥ 1 and H_m(κ, δ) hold. For a scale-m plaquette P put c_½(P) := ∫χ½(V_P) log ρ_m(V) dV in Haar measure, and β_m := 2c_½(P). Then

```text
| c_1/2(P) |  <=  (8/(3 pi)) e^{-4 kappa} delta  <  (8489/10000) e^{-4 kappa} delta,       | beta_m |  <=  (16/(3 pi)) e^{-4 kappa} delta.
```

At κ = 1/4, (16/(3π))e^{−1} < 0.62454.

*Proof.* V_P holds each link of ∂P once, so ∫χ½(V_P)dV = 0, and const_m contributes 0. If ∂P ⊄ Y, take ℓ ∈ ∂P ∖ Y. R_m(Y) does not involve V_ℓ, and ∫χ½(V_P)dV_ℓ = 0. So c_½(P) = Σ_{Y⊇∂P} ∫χ½(V_P)R_m(Y; V)dV. Each term is at most E|χ½| sup|R_m(Y)|. With χ½ = 2cos ψ and Haar density (2/π)sin²ψ on [0, π], E|χ½| = (8/π)∫_0^{π/2} cos ψ sin²ψ dψ = 8/(3π). Fix ℓ ∈ ∂P. Then Σ_{Y⊇∂P} sup|R_m(Y)| ≤ e^{−4κ}Σ_{Y∋ℓ} w(Y) ≤ e^{−4κ}δ, since #Y ≥ 4. Finally 8/(3π) < 8489/10000 iff π > 80000/25467, and π > 333/106 > 80000/25467. ∎

So the χ½(V_P) dependence of log ρ_m sits in the R_m(Y) with Y ⊇ ∂P, and in general not in R_m(∂P) alone. The attack's example: a cluster {Γ_1, Γ_2} of incompatible polymers with Y″(Γ_1) = ∂P and Y″(Γ_2) = ∂Q contributes −z_1(V_P)z_2(V_Q) to R(∂P ∪ ∂Q). Its χ½(V_P) projection is nonzero unless ∫z_2 dV = 0 (S1). This is why the hypothesis row now defines β_k as a projection. This readout ties to C09 only in form. C09's readout is a G0 statement at scale 1.

### 4.12 Lower bounds on any valid step bound, and the sharper G1 tests

**Lemma 4.23 (the slice bound, DERIVED; the channel attack's M3).** Let log ρ = C′ + Σ_Y R(Y) be any representation on Λ_{k+1}, with each R(Y) bounded and a function of V restricted to Y, and #Y ≥ 4. Neither gauge invariance nor the loop condition is needed. Fix a coarse link ℓ, and let V^g be the configuration with every coarse link at 1 except V_ℓ = g. Then, for every κ ≥ 0,

```text
sum_{Y containing l} e^{kappa #Y} sup|R(Y)|  >=  e^{4 kappa} sum_{Y containing l} sup|R(Y)|  >=  (e^{4 kappa}/2) osc_{g in SU(2)} log rho(V^g).
```

*Proof.* On the slice, each R(Y) with ℓ ∉ Y is a function of fixed links, so it is constant in g. So Σ_{Y∋ℓ}R(Y; V^g) = log ρ(V^g) + const. The oscillation of a sum is at most the sum of the oscillations, and each is at most 2 sup|R(Y)|. ∎

**Corollary 4.24 (C10 for every representation, DERIVED).** Take C10's input: at scale k, R_k(Y) = sχ½ of the fine 2 × 2 loop around each coarse plaquette P″, with Y its 8 line links, and every other R_k = 0. Its fine norm is 12|s|e^{8κ}. The output is log ρ_{k+1} = const + Σ_{P″} sχ½(V_{P″}) exactly (Lemma 4.7, with 𝒴_O = ∅, and YM4-03 Proposition 2). On the slice the 6 coarse plaquettes through ℓ read χ½(g), since χ½(g⁻¹) = χ½(g), and the others read 2. So osc_g = 24|s|, and every representation has norm at least 12|s|e^{4κ}. Hence no step bound C(δ)δ, valid for every input of norm δ, has C(δ) < e^{−4κ}, at any δ > 0 and any κ ≥ 0. At κ = 0 the ratio is at least 1 for every representation. At κ = 1/4, c_fin(δ) = e^{−1} for δ ≤ 0.078733761. So on that range Theorem G1 is optimal among all valid step bounds.

This removes route A's caveat (its gap 3). It supplies route B's missing proof. It is stronger than the structure attack's Lemma S3, which needs κ ≥ (ln 2)/3 and gives only 1/6 at κ = 0.

**The every-representation bounds of C10b and C10c.** Both outputs have the form const + Σ_{P″} F(χ½(V_{P″})), since the objects of distinct P″ share no off link (C01). On the slice, Lemma 4.23 gives every representation a norm of at least 3e^{4κ}osc_{[−2,2]}(F). That is the natural norm, attained by R(∂P″) := F − (max F + min F)/2. So the frozen projection bounds, built on E|χ½| = 8/(3π), are valid but loose. The natural norms are δ_out = 3e^{4κ}ln c_0(4s) for C10b and δ_out^nat ∈ 6e^{4κ}[s − 4s², s + 4s²] for C10c (the v2 row's DERIVED bracket).

**The per-root tests.** Proposition 4.15's first line bounds the norm of G1's own representation, which is at least the natural norm. For C10b every root at e_0 is a rectangle with (f, m) = (2, 4), so G1 claims δ_out ≤ e^{δ}q(2, 4)δ_in = e^{δ−4κ}(e^{2λ} − 1)δ_in. For C10c every root has (f, m) = (2, 8), so G1 claims δ_out^nat ≤ e^{δ}q(2, 8)δ_in = e^{δ−6κ+2λ}δ_in. These are sharper falsifiers of G1 than the c(δ_in) comparisons of the rows. Their slacks are in section 4.14.

### 4.13 The Wilson term inside R_k: what it costs, and why it is harmless

At scale k the plaquette coupling sits inside Σ_Y R_k(Y). A part of it may be an object R_k(∂p) on the 4 links of a fine plaquette. A fine plaquette holds 2 or 4 off links (Lemma 4.1 item 2). So ∂p is an object with (f, m) = (2, 2) or (4, 0), never a line-channel term. A gauge-invariant function of the 4 links of a plaquette is a class function of U_p.

**What is forfeited: Lemma B.** At step 0 the activities were products of K(U_p) with ∫K dg = 0. A polymer with an off link held by one plaquette only had activity 0 (YM4-03C §6 Lemma B). So polymers were closed, and #off(γ) ≤ 2#γ. At step k, ∫φ_{∂p} dU_e = ∫(e^{R_k(∂p)} − 1)dg for every off link e of p, by Haar invariance. For R_k(∂p) = β_k a this is c_0(β_k) − 1 = Σ_{m≥1}(β_k/2)^{2m}/(m!(m + 1)!) > 0. So the single-plaquette polymer has nonzero activity, unclosed polymers stay in the gas, and no closure bound is available. The same holds for every object at k ≥ 1, since nothing makes φ_o mean-zero.

**What G1 uses instead.** Nothing. No step of sections 4.2 to 4.11 uses a cancellation. a(Γ) counts every off link of the support, and every object pays at its sup norm. So the Wilson term changes no constant of G1 (structure attack, 2.6).

**What it costs in strength.** The multi-object factor is first order in δ′: q(f, m) holds e^{λf} − 1 ≥ λf. Centering the plaquette objects, e^{R_k(∂p)} = μ_p(1 + K_p) with μ_p := ∫e^{R_k(∂p)}dg and ∫K_p dg = 0, would restore Lemma B for them alone. That repair is not done. A plaquette object that is a root adds q(2, 2) = e^{−3κ}(e^{2λ} − 1) per unit e^{δ}w. At C07's δ_1 ≤ 0.011045 this is below 0.0216, against e^{−4κ} > 0.36787. A plaquette object with no line link is never a root at a line link. It enters only through the attachment factor e^{λf} − 1 of the roots it meets.

**Why it is harmless at these δ.**

1. For 0 < δ ≤ 0.078733761, c_fin(δ) = e^{−4κ}. The object channel, where every plaquette object lives, stays below the line channel there. By Corollary 4.24 no repair could lower the factor on that range.
2. By Lemma 4.22, |β_m| ≤ 0.62454δ_m at every scale m ≥ 1. At β_0 = 1/100 the term 12e·c_½(1/100) ∈ [2.548 × 10⁻⁹, 2.549 × 10⁻⁹] of C08 (from the MEASURED series P_10) is about 2.7 × 10⁻⁴ of the refined δ_1 ∈ [9.42 × 10⁻⁶, 9.45 × 10⁻⁶].
3. The same lemma marks the limit of H_k. A coupling |β_m| > 0.62454δ_m is incompatible with H_m(κ, δ_m). With δ_m < δ_crit,fin < 0.11485 this caps |β_m| below 0.07173. So H_k with the plaquette coupling inside Σ_Y R_k(Y) is a strong-coupling hypothesis at every scale. A weak-coupling H_k must carry the Wilson term outside the polymer norm.

### 4.14 The constants at the rows' points

Read by `reviews/ym4-04c-prediction/ym4c/pkg/repair/G1-repair-checks.py`: exact Fractions, e^y enclosed by a Taylor sum with a geometric remainder after range reduction by halving, ln(1 + x) by alternating partial sums, and outward rounding to 256 significant bits. The supremum over f is certified by a tail cut: the scan stops at the first f with e^{−(κ−λ⁺)f} below the best upper value so far. Floats appear only in printing. A bracket over a δ bracket uses that c_frz and c_fin are nondecreasing. "pt" is a read at the row's point.

e^{−1} ∈ [0.3678794411714, 0.3678794411715]. The final certificate's edge: λ(δ) ≤ 1/4 certified at δ = 0.114846768, and λ(δ) > 1/4 certified at 0.114846769. There 2δ′ ∈ [0.2576475939, 0.2576475964] > 1/4, so the final domain is wider than route A's 2δ′ ≤ κ, whose edge is at 0.111780108/0.111780109. The frozen C_k edge is 0.058923670/0.058923671. c_fin = e^{−1} through δ = 0.078733761: there the object channel's upper enclosure is 0.3678794375. At 0.078733762 its lower enclosure is 0.3678794463 > e^{−1}, at f = 7.

| Point (row) | δ | λ(δ) | frozen c_frz (reproduced) | final c_fin |
|---|---|---|---|---|
| C07, crude 1/100 | [0.011044, 0.011045] | [0.0222714052, 0.0222734384] | [0.4450429880, 0.4450508181]; pt 0.0110444507: 0.4450465170 | e^{−1} |
| C08, refined 1/100 | [9.42e-6, 9.45e-6] | [1.88401331e-5, 1.89001340e-5] | [0.3679383586, 0.3679385463] | e^{−1} |
| C10b, s = 1/2000 | [0.026890, 0.026891] | [0.0548711345, 0.0548732159] | [0.5950951906, 0.5951068539] | e^{−1} |
| C10b, s = 1/4096 | [0.013129, 0.013131] | [0.0265173128, 0.0265213920] | [0.4617347010, 0.4617510695] | e^{−1} |
| C10c, s = 1/8192 | [0.0356909, 0.0356910] | [0.0733078574, 0.0733080682] | [0.7118122718, 0.7118137902] | e^{−1} |
| C10c, s = 1/65536 | [0.0044613, 0.0044614] | [0.00895248443, 0.00895268577] | [0.3969921636, 0.3969928442] | e^{−1} |
| C13, 49/1000 | 0.049 | 0.10164123 | 0.9824884835 | e^{−1} |
| C13, 1/20 | 0.05 | 0.103792224 | 1.011066807 | e^{−1} |
| C14, refined 1/64 | [2.0347e-3, 2.0348e-3] | [0.00407561282, 0.00407581343] | [0.3808522431, 0.3808528930] | e^{−1} |
| C12, head-free 1/50 | [0.072645, 0.072646] | [0.153336293, 0.153338516] | undefined: 2δ′ ∈ [0.156237416, 0.156239723] > 1/8 | e^{−1} |
| C12, refined 1/50 | [0.072646, 0.072648] | [0.153338516, 0.153342963] | undefined: 2δ′ > 1/8 | e^{−1} |
| C11, crude 1/64 | [0.10165, 0.10166] | [0.219159369, 0.219182526] | undefined: 2δ′ ∈ [0.225052278, 0.225076668] > 1/8 | [0.6374716724, 0.6376442579], f = 10 |

Every frozen value of c_frz and 2δ′ reproduces at its row's point. Three frozen brackets are narrower than the image of their own δ bracket: C07's c (upper 0.4450508181 > 0.44505), C10b's c at s = 1/2000 (0.5951068539 > 0.5951), and C11's 2δ′ (0.225076668 > 0.22507). C10c's v2 c bracket at s = 1/8192 has the same issue (0.7118137902 > 0.7118123). At the row points the frozen values hold (F6, M4). Under the final constants this issue disappears for c, since c_fin is constant on each of these brackets.

**The chains** (upper ends of the δ_1 brackets):

| Row | quantity | frozen (reproduced) | final |
|---|---|---|---|
| C07 | c(δ_1); δ_2; Σ_k δ_k | 0.4450508181; 4.9155863e-3; 0.019902723 | 0.3678794412; 4.0632284e-3; 0.017472933 |
| C08 | c(δ_1); δ_2; Σ_k δ_k | 0.3679385463; 3.47702e-6 (route A); 1.49511e-5 (route A) | 0.3678794412; 3.4764607e-6; 1.494968e-5 |
| C14, 1/64 | c(δ_1); δ_2; Σ_k δ_k | 0.3808528930; 7.74960e-4 (route A); 3.28646e-3 (route A) | 0.3678794412; 7.4856109e-4; 3.2190062e-3 |
| C11 | c(δ_1); δ_2; Σ_k δ_k | NOT_MET as frozen | 0.6376442579; 0.064822915; 0.28055303 |
| C12, refined | c(δ_1); δ_2; Σ_k δ_k | NOT_MET as frozen | 0.3678794412; 0.026725706; 0.11492744 |
| C16 | δ_20 ≤ c^{19}δ_1; osc_V log ρ_20 ≤ (512/e)δ_20 | 2.306472e-9; 4.3443386e-7 | 6.1882887e-11; 1.1655906e-8 |

**C10b, C10c against the slice bound and the per-root bound** (c_fin = e^{−1} at every δ_in here):

| Row | natural δ_out = every-representation bound | δ_out/(c_fin δ_in); slack | per-root bound / natural δ_out |
|---|---|---|---|
| C10b, s = 1/2000 | [4.0774224e-6, 4.0774234e-6] | [4.121803e-4, 4.121804e-4]; [2426.122, 2426.123] | [289.0782, 289.0783] |
| C10b, s = 1/4096 | [9.7213332e-7, 9.7213338e-7] | [2.012599e-4, 2.012599e-4]; [4968.699, 4968.699] | [274.2232, 274.2232] |
| C10c, s = 1/8192 | [1.9899569e-3, 1.9919012e-3] | [0.1515586, 0.1517067]; [6.591666, 6.598107] | [4.797586, 4.802273] |
| C10c, s = 1/65536 | [2.4885094e-4, 2.4888132e-4] | [0.1516234, 0.1516419]; [6.594483, 6.595288] | [4.090225, 4.090724] |

The frozen C10b clause "projection bound at most 3 × 10⁻⁵ times c(δ_in)δ_in" reads [4.04354e-5, 4.05365e-5] with c_fin, so it fails as a clause. The G1 test it encodes still passes, with slack about 2.47 × 10⁴. C10c's per-root test at s = 1/65536 has the least slack, about 4.09. It is the strongest computed test of G1 in the package. No ratio reaches 1, so no test refutes c_frz, c_fin or the per-root bound.

**The self-map edges.** Each side is certified at its point. The MET read at β certifies S⁺(ε⁺e^{2α_c+1/4}) ≤ α_c at α_c := δ_crit⁻/factor, so δ_1 ≤ δ_crit⁻. The NOT_MET read at β certifies S⁻(ε⁻e^{2α_c+1/4}) > α_c and g′⁺(α_c) < 0 at α_c := δ_crit⁺/factor. By convexity of g the least root then exceeds α_c. Every read is at θ = 1/4. That every δ_1 optimum sits at θ = 1/4, and that δ_1 is nondecreasing in β_0, are G0 statements. "factor" is the prefactor of δ_1 = factor·α at θ = κ: 12 as frozen, and 6 in the G0 repair lane's checks (`reviews/ym4-04c-prediction/ym4c/pkg/repair/G0-repair-checks.out`). The frozen edges reproduce: 0.01369/0.01370 (crude) and 0.01959/0.01960 (C03 and head-free). Route A's c* edges reproduce: 0.01582/0.01583 and 0.02037/0.02038.

| Test | crude | C03 head (CONJECTURE on C03) | head-free (every count vector) |
|---|---|---|---|
| final, factor 12 | MET 0.01595 (δ_1 ∈ [0.1148019, 0.1148020]), NOT_MET 0.01596 (δ_1 ≥ 0.1152348) | MET 0.02040 (δ_1 ≤ 0.1134657), NOT_MET 0.02041 (δ_1 ≥ 0.1149395) | MET 0.02040, NOT_MET 0.02041 |
| final, factor 6 | MET 0.01767 (δ_1 ≤ 0.1145676), NOT_MET 0.01768 (δ_1 ≥ 0.1150830) | MET 0.02074 (δ_1 ≤ 0.1088559), NOT_MET 0.02075 (δ_1 ≥ 0.1158911) | MET 0.02074, NOT_MET 0.02075 |
| fallback 2δ′ ≤ κ, factor 12 | 0.01587/0.01588 | 0.02038/0.02039 | 0.02038/0.02039 |
| fallback 2δ′ ≤ κ, factor 6 | 0.01761/0.01762 | 0.02074/0.02075 | 0.02074/0.02075 |

The orderings survive: β_ind^crude < β_crude ∈ [0.01904, 0.01905), and β_ind < β_stop ∈ [0.02075, 0.02076) < β_wall ∈ [0.02247, 0.02248], under every row of the table. With factor 6 and the C03 head, β_ind sits one grid step below the refined C_0 stop. C19's δ_crit_surrogate fault (δ_1 ≤ 49/1000 in place of the final test) reads its edge at 0.01365/0.01366 with factor 12 and 0.01552/0.01553 with factor 6. So that fault loses MET on [0.01366, 0.01595] or on [0.01553, 0.01767].

### 4.15 What changes in the rows

Gate G_attack (v2) says that a proved constant differing from a frozen one makes every row and clause resting on it read UNSUPPORTED, and that a corrected constant is filed as appended rows. The final constants differ. So the frozen rows below read UNSUPPORTED as frozen. The final values go into appended rows after line 41. Every frozen value stays true as a bound, by Corollary G1-frozen and Lemma 4.18. What fails is only the claim that it is what the proof gives.

- CERTIFICATES: C_k becomes λ(δ_k) ≤ κ. c(δ) becomes c_fin(δ). self_map becomes "MET iff λ(δ_k) ≤ κ". The KP pair stays α = t = δ′, θ = κ, with #γ := ½#line(γ) at step k. "c is increasing" becomes "c_fin is nondecreasing". "max_{n≥4}" in the frozen formula becomes "sup_{n≥4}", since the maximum does not exist on 2δ′ = κ/2 (S5).
- HYPOTHESIS: "bounded, measurable" is added. "coarse-gauge invariant" becomes "invariant under every gauge transformation of Λ_k". The Wilson clause becomes the projection definition of section 4.0. admissible becomes "C_0 MET and λ(δ_1) ≤ κ". δ_crit becomes δ_crit,fin ∈ [0.114846768, 0.114846769]. The regime clause becomes β_0 ≤ 0.02040 (factor 12) or β_0 ≤ 0.02074 (factor 6), on the 10⁻⁵ grid.
- THEOREMS: the corollary carries e^{d(X)}. The tree-graph clause uses (1 + t)^{s(o)} with s(o) := #off(o), at off links. G1's status is DERIVED, here, on the REPORTED Theorem 4.9.
- C07, C08, C14 (value at 1/64), C16: c(δ_1) becomes e^{−1}, with the chains of section 4.14.
- C10: unchanged values. Its "every valid step bound" clause is now DERIVED for every representation and every κ ≥ 0 (Corollary 4.24).
- C10b, C10c: c(δ_in) becomes e^{−1}. C10b's 3 × 10⁻⁵ clause and low_power field are replaced by the slice slack and the per-root slack of section 4.14 (F7). C10c's power field is replaced likewise.
- C11: C_1 and the crude self-map become MET at 1/64. The row's name, "the crude hypothesis does not map to itself", is false for the final certificate.
- C12: the head-free lower limit δ_1 ≥ 0.072645 no longer forces a NOT_MET, since λ(0.072646) ≤ 0.153338516 < 1/4. So the clause "C_1 NOT_MET under every count vector" is dropped. With the C03 head, C_1 and the self-map are MET with c_fin = e^{−1} (CONJECTURE on C03). For a count vector between the C03 head and the crude one nothing is claimed: its δ_1 may exceed δ_crit,fin. C_0 crude stays NOT_MET at 1/50 (a G0 read).
- C13: c(49/1000) and c(1/20) become e^{−1}. δ_crit becomes δ_crit,fin. The crude edge becomes 0.01595/0.01596 (factor 12).
- C14: the edge becomes 0.02040/0.02041 (factor 12), the same for the head-free limit. The head-free clause becomes "β_ind < 0.02041 for every count vector".
- C17: the replacement clause stays true. It rests on C07's self-map, which stays MET.
- C19: the δ_crit_surrogate fault's expected range moves, as in section 4.14.
- SCOPE: "NOT_MET above the windows = a failure of this norm and these counts" is restated as a failure of this norm, these counts and this bookkeeping.

### 4.16 OPEN and CONDITIONAL

No step of Theorem G1 is OPEN. It rests on Theorem 4.9, REPORTED from Kotecký and Preiss (1986). The paper's text was not re-read in this session. The rest is DERIVED here or in YM4-03 and YM4-03C.

1. **CONDITIONAL on G0.** Every row value that uses δ_1 rests on section 3. That covers the δ_1 formula (factor 12 or 6), the claim that every δ_1 optimum sits at θ = 1/4, and, for every "largest β on the grid" read, that δ_1 is nondecreasing in β_0. Given ε_6 nondecreasing in β_0, the last follows from S increasing, so it reduces to a G0 statement about ε_6. Rows CONDITIONAL on G0: C07, C08, C11, C12, C13, C14, C16, C17's replacement clause and the regime clause. The edge reads of C13, C14 and the regime clause also rest on the monotonicity statement. Until G0 proves it, those rows read their edge pairs as two certified points only.
2. **CONJECTURE on C03.** C08, C12's refined clause and C14's refined values rest on the C03 counts.
3. **Not yet attacked.** Two changes of this section were not read by a second seat. The m ≥ 1 restriction was proposed by two attack lanes (F5, M1), and its numbers reproduce theirs. The (1 + t)^f form of (T), which gives λ ≤ κ in place of 2δ′ ≤ κ, is new. Gate G_attack should read Lemma 4.12, Lemma 4.13 and Proposition 4.15 as written here before the freeze. Rows whose final value depends on the (1 + t)^f step: C11's c value, the C13 and C14 edges, the regime clause, δ_crit,fin and C19's surrogate range. They are CONDITIONAL on that read. If it fails, the fallback rows of section 4.14 (2δ′ ≤ κ) apply, and their values are given. The rows where c_fin = e^{−1} (C07, C08, C10b, C10c, C12, C14 at 1/64, C16) do not depend on it, since the fallback gives e^{−1} there too, up to δ = 0.077320139.
4. **Not a gap.** G1 bounds one output representation. H_{k+1} asks for one. Corollary 4.24 shows that for C10's class no representation does better.
5. **Unused slack.** δe^{δe^{−4κ}} in place of δ′, a centered plaquette object with Lemma B restored, and line-only weights beyond d are not used. They could change c_fin only where c_fin > e^{−4κ}, that is for δ > 0.078733761, and the domain edge.
6. **Scope.** G1 says nothing about weak coupling. By Lemma 4.22 it is a statement about a class whose plaquette coupling is below 0.62454δ_m at every scale.

### 4.17 The final constants table

"Equal" means exactly the same constant or formula. Each "no" is marked [CHANGED] above.

| Item (row) | Frozen | Final | Equal? |
|---|---|---|---|
| H_k form (HYPOTHESIS) | real, coarse-gauge invariant, function of V on Y, #Y ≥ 4, closed loop | adds bounded and measurable; invariant under every gauge transformation of Λ_k | no (wording) |
| Wilson clause (HYPOTHESIS) | (β_k/2)χ½(V_P) carried inside R_k(∂P) | no Wilson term outside Σ_Y R_k(Y); β_k := 2c_½(P); \|β_k\| ≤ (16/(3π))e^{−4κ}δ_k | no |
| norm_κ (HYPOTHESIS) | sup_l Σ_{Y∋l} e^{κ#Y} sup\|R_k(Y)\| | the same | yes |
| κ | 1/4 | 1/4; the theorem holds for 0 < κ ≤ 1/4 | yes |
| uniformity | no bound involves N, K, N_p | step bounds only; C16's readout is per final torus | no (wording) |
| δ′ (CERTIFICATES) | δe^{δ} | δe^{δ} | yes |
| C_k (CERTIFICATES) | 2δ′ ≤ κ/2 | λ(δ) = δ′ + ln(1 + δ′) ≤ κ | no |
| KP pair | α = t = δ′, θ = κ; a(γ) = α#off(γ), d(γ) = θ#γ | the same, with #γ := ½#line(γ) at step k | yes, with #γ defined |
| tree-graph bound (THEOREMS) | Σ_{Γ∋e}Πω ≤ t from Σ_{o∋e}ω_o e^{t s(o)} ≤ t | Σ_{o∋e}ν_o(1 + t)^{s(o)} ≤ t at off links, s(o) = #off(o), ν = ω e^{a+d} | no (weaker hypothesis, defined) |
| KP corollary (THEOREMS v2) | Σ_{X∋γ}\|Φ\|e^{d(γ)} ≤ \|z_γ\|e^{a(γ)+d(γ)} | Σ_{X∋γ}\|Φ\|e^{d(X)} ≤ \|z_γ\|e^{a(γ)+d(γ)} | no |
| c(δ) (CERTIFICATES) | e^{δ}[e^{−4κ} + max_{n≥4}(e^{−(κ/2−2δ′)n} − e^{−κn/2})] | c_fin = max{e^{−4κ}, e^{δ+λ−5κ}, e^{δ−κ/2}sup_{f≥4}(e^{−(κ−λ)f} − e^{−κf})} | no |
| e^{δ} prefactor | on both channels | on the object channel only | no |
| line-channel factor | e^{−κ#Y/2} ≤ e^{−4κ} | the same; #Y ≥ 8 for every Y ∈ 𝒴_L | yes |
| root range | max over root size n ≥ 4 | off count f ≥ 4 at one line link, and (f, m) = (1, 8) | no |
| c_fin = e^{−4κ} range (κ = 1/4) | — | 0 < δ ≤ 0.078733761 | new |
| self_map | MET iff C_k MET and c(δ_k) < 1 | MET iff λ(δ_k) ≤ κ; c_fin < 1 automatic | no |
| monotonicity | c increasing | c_fin nondecreasing | no |
| δ_crit (HYPOTHESIS, C13) | [0.0496174, 0.0496175] | [0.114846768, 0.114846769] | no |
| regime (HYPOTHESIS) | β_0 ≤ 0.01959 | β_0 ≤ 0.02040 (factor 12) or 0.02074 (factor 6) | no |
| plaquette readout | — | \|c_½(P)\| ≤ (8/(3π))e^{−4κ}δ_m at every scale | new |
| C07 2δ_1′ | [0.02233, 0.02234] | reproduces; the final test reads λ ∈ [0.0222714, 0.0222735] | yes (value) |
| C07 c(δ_1) | [0.44504, 0.44505] | e^{−1} ∈ [0.3678794, 0.3678795] | no |
| C07 δ_2; Σδ_k | ≤ 4.92e-3; ≤ 0.01991 | ≤ 4.0632284e-3; ≤ 0.017472933 | no |
| C08 c(δ_1) | [0.36793, 0.36795] | e^{−1}, 5.06e-5 below the frozen lower end | no |
| C08 Σδ_k | ≤ 1.50e-5 | ≤ 1.494968e-5 | no |
| C10 ratio | e^{−4κ} exactly; ≥ e^{−4κ} for every valid c; 1 at κ = 0 | the same, for every representation and every κ ≥ 0 | yes (values) |
| C10b c(δ_in) | [0.5950, 0.5951]; [0.4617, 0.4618] | e^{−1} at both | no |
| C10b test | projection bound ≤ 3e-5·cδ_in; slack 3 × 10⁴ | slice slack [2426.122, 2426.123]; per-root slack [289.0782, 289.0783] | no |
| C10c c(δ_in) | [0.7118122, 0.7118123]; [0.3969925, 0.3969926] | e^{−1} at both | no |
| C10c test | slack [12.08, 12.09] (every decomposition) | slice slack [6.594483, 6.595288]; per-root slack [4.090225, 4.090724] at s = 1/65536 | no |
| C11 | C_1 NOT_MET, crude self-map NOT_MET at 1/64 | MET; c_fin ∈ [0.6374716724, 0.6376442579] | no |
| C12 | C_1 NOT_MET at 1/50 under every count vector | the head-free limit forces no NOT_MET; C03 head: C_1 and self-map MET, c_fin = e^{−1}; other count vectors: no claim | no |
| C13 c(49/1000); c(1/20) | [0.98248, 0.98249]; [1.0110, 1.0111] | e^{−1}; e^{−1} | no |
| C13 crude edge | 0.01369/0.01370 | 0.01595/0.01596 (factor 12); 0.01767/0.01768 (factor 6) | no |
| C14 edge, head-free clause | 0.01959/0.01960; β_ind < 0.01960 for every count vector | 0.02040/0.02041; β_ind < 0.02041 (factor 12); 0.02074/0.02075 (factor 6) | no |
| C14 c(δ_1) at 1/64 | [0.38085, 0.38086] | e^{−1} | no |
| C14 ordering | β_ind < β_stop < β_wall | holds | yes |
| C16 δ_20; osc_20 | [2.30e-9, 2.31e-9]; ≤ 4.35e-7 | ≤ 6.1882887e-11; ≤ 1.1655906e-8 | no |
| C16 osc step | (512/e)δ_m on 1024 links | the same | yes |
| C19 surrogate | MET lost at 0.01366–0.01369 | MET lost at 0.01366–0.01595 (factor 12) | no |

### 4.18 Attack resolutions

Tree-graph lane (verdict GAP):

- **F1 (blocking): d(γ) = θ#γ undefined at step k.** The attack is right. Both literal readings fail. Fixed: #γ := ½#line(supp γ), so a and d keep their frozen form with α = δ′ and θ = κ (section 4.7). On the attack's instance the final d gives 0.0076740784 < 2δ′.
- **F2 (blocking): the proved constants are not the frozen ones.** The attack is right. Resolved by using the proved constants, λ ≤ κ and c_fin, marked [CHANGED]. The frozen theorem is kept only as Corollary G1-frozen. The rows resting on it are re-pinned in appended rows (section 4.15). The two routes' disagreement on C_k is settled: route B's 2δ′ ≤ κ/2 is a property of its uniform d, and the weaker hypothesis wins.
- **F3: e^{d(γ)} in the v2 corollary.** Right. Fixed: e^{d(X)} (Corollary 4.10).
- **F4: s(o), ω and e undefined.** Right. Fixed: s(o) = #off(o), ν = ωe^{a+d}, e at off links, and the (1 + t) form (Lemma 4.12).
- **F5: roots hold a line link.** Right. Adopted: m ≥ 1. It moves c* = e^{−1} from 0.072094 to 0.077320139 under 2δ′ ≤ κ, and to 0.078733761 under λ ≤ κ.
- **F6: "reproduces inside" for propagated enclosures.** Right. Fixed: reads at the rows' points. C07's c, C10b's c, C11's 2δ′ and C10c's c brackets are flagged (section 4.14). Under c_fin the c brackets no longer arise.
- **F7: C10b's power against the wrong channel.** Right. Fixed: the per-root test for C10b's (2, 4) roots, slack [289.0782, 289.0783], and the slice slack.
- **F8: route A's table marks non-identical formulas "yes".** Right for route A's sum form of a. Fixed: the union form a(Γ) = α#off(Γ) is the frozen formula, and it closes (Lemma 4.13 item 3).

Channel lane (verdict HOLDS):

- **M1** = F5, adopted. **M2: route A's "exactly" in Remark 4.18 is wrong.** Right. Fixed in Remark 4.18a. **M3: the slice lemma.** Right. Adopted as Lemma 4.23 and Corollary 4.24. **M4** = F6. **M5** = F4 and F1. **M6: line-supported Y have #Y ≥ 8 and a loop in Y″.** Right. Adopted as Lemma 4.1 item 5. The vacuous clause of route A's Lemma 4.5 is dropped. **M7** = F2.

Structure lane (verdict HOLDS):

- **S1: the Wilson clause is not reproduced at k + 1, and β_k is undefined.** Right. Fixed: β_k := 2c_½(P), carried by any R_k(Y) with Y ⊇ ∂P (Lemma 4.22).
- **S2: "measurable" omitted, and "coarse" used for scale k.** Right. Fixed in (H2).
- **S3: C10's floor for every representation.** Right, and superseded by Lemma 4.23, which also covers κ < (ln 2)/3 and the κ = 0 clause, where S3 gives only 1/6.
- **S4: c_♯ called increasing.** Right. Fixed: c_fin is nondecreasing (Lemma 4.19).
- **S5: max on the boundary 2δ′ = κ/2.** Right. Fixed: sup in the frozen formula. c_fin uses sup, a maximum for λ < κ.
- **S6: four of route B's brackets rounded to nearest.** Right. Route B's brackets are not used. Every bracket here is outward.
- **S7: tables against the 40-line draft, no C10c row.** Right. Fixed: section 4.14 reads v2, C10c included. Route B's C08 sentence is corrected: e^{−1} lies 5.06 × 10⁻⁵ below the frozen lower end 0.36793.
- **S8: uniformity and self-map wording.** Right. Fixed in Lemma 4.21's remark and Corollary 4.20.

### 4.19 Scratch files (pre-freeze disclosure)

All are under `reviews/ym4-04c-prediction/ym4c/pkg/repair/`. None is an engine, and none is evidence.

- `G1-repair-checks.py` (sha256 `dc99c4b7cce35c1bfb01f4b99a47cdb509f83026ed9871afd451489c6245d2d8`), output `G1-repair-checks.out` (`e618049fef2b054a3f40a2cdcd5c01ed1e1acbd21996480a5c1ac39a703aede4`): e^{−1}; the edges of 2δ′ ≤ 1/8, 2δ′ ≤ 1/4 and λ ≤ 1/4; c_fin and the m ≥ 1 form of route A's c* at the row points; where each equals e^{−1}; the frozen c reproduced; the chains; C10b and C10c against the slice and per-root bounds; the F1 instance under the final d; the closed form of Q against a brute-force supremum; the β edges under the frozen, route A, fallback and final tests.
- `G1-repair-edges-extra.py` (`234fe9209a7ab21965b145fed7da46462df6476f80fb38c408789a6425b7ce18`), output `G1-repair-edges-extra.out` (`198271e9b9f1ed4b212e10b220ba43e247b9e44aebde29af83808702106cdb86`): δ_1 brackets at the final edge points, and C19's surrogate edges.
- `G1-repair-treegraph-toy.py` (`56aea72920f93904c92e5e78271f55cfcd2d91aa838e0fe2df7ca8d64b72a985`), output `G1-repair-treegraph-toy.out` (`adc7777edfc2d1843fa7b673e2447fdcda6e2762d415fb3a29069c93c711e273`): Lemma 4.12 in the (1 + t) form on 12 random hypergraphs of 14 links and 11 objects, with the hypothesis at equality. T(e)/t reads at most 0.8384, and item 2 holds at every link.

The ε_6 enclosure and the series S in `G1-repair-checks.py` follow the frozen closed forms and the G0 repair lane's routine. They are G0 inputs, re-read here only to place the edges.

### References

- R. Kotecký and D. Preiss, Cluster expansion for abstract polymer models, Comm. Math. Phys. 103 (1986) 491–498. REPORTED.
- Repo: NOTE-YM4-03-ONE-SCALE-BLOCKING.md (Proposition 2, Lemma 3, Theorem 4); NOTE-YM4-03C-BLOCKED-ACTION.md (§2 the line gauge and Lemma A, §6 Lemma B, §12 OPEN); NOTE-YM4-04-TWO-TERNARY-BLOCKS-20261107.md and NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md (the routes this step replaces); LEMMA-0001-GAUGE-INVARIANCE.md.
- This package, under `reviews/ym4-04c-prediction/ym4c/pkg/`: `derive/G1-a.md`, `derive/G1-b.md`, `attack/G1-treegraph.md`, `attack/G1-channel.md`, `attack/G1-structure.md`, `PREDICTION-v2.hbp`, `note_outline-v2.txt` §16, `repair/G0-repair-checks.out`.

## 5. The certificates as exact inequalities

**C_0.** Fix a head N(4), …, N(10) and put ε := ε_6(β_0) and x := ε e^{2α+θ}. The closed form is

```text
S(x) := sum_{n=4}^{10} N(n) x^n  +  sum_{n=11}^{48} 6 F_20(n) x^n  +  6 F_20(49) x^49 / (1 - mu x),      defined for mu x < 1.
```

A head is valid when N(n) ≥ N_w(n) for every off link w and 4 ≤ n ≤ 10. The crude head 6F_20(n) is valid (Corollary 3.12). The head-free vector N(n) = 0 is not valid; it gives a lower limit on δ_1 for every count vector N(4..10) ≥ 0 (Remark 3.34). The refined head is the C03 counts, a CONJECTURE until the engine and the check read them.

C_0 is MET when some grid θ and some rational α give S⁺(ε⁺e^{2α+θ}) ≤ α ≤ 1/4. The cap 1/4 never binds: a certified least root is at most 1/8 (Lemma 3.31 item 4).

**A MET read is one exact inequality.** g(α) := S(εe^{2α+θ}) − α is convex in α, since S has nonnegative coefficients (Lemma 3.31). The search only proposes α. The read is the inequality at that rational α. It uses ε⁺ ≥ ε, x⁺ ≥ ε⁺e^{2α+θ} and μ⁺ ≥ μ. It tests μ⁺x⁺ < 1 first, and reads NOT_MET when that fails. It puts 1 − μ⁺x⁺ in the tail denominator and rounds every other operation upward (Lemma 3.30). The tail formula is negative for μx > 1, so the pole test must come first.

**A NOT_MET read is a proof.** It is one of three: the pole μx ≥ 1 at α = 0; S⁻(x⁻(0)) > 1/4; or the convex tangent bound g⁻(α_m) − |g′|⁺(α_m)·max(α_m, 1/4 − α_m) > 0 at one rational α_m, with g′(α) = 2xS′(x) − 1. θ = 1/4 decides every grid θ, since S(εe^{2α+θ}) increases in θ. If no proof closes, the read is UNDECIDED and is filed as such.

**Why a capped fixed-point iteration is not used.** A plain iteration from α = 0 gives lower iterates that increase to the least root and never certify by themselves (Lemma 3.31). The planted variant `iteration_cap_400` pins one capped variant: α_0 = 0, α_{j+1} = s_j := S⁺(up(ε_6⁺e^{2α_j+θ})), MET at the first j with s_j ≤ α_j(1 + 10⁻⁴⁰), and at most 400 evaluations of S⁺. It reads the crude edge at 0.01901/0.01902 in place of 0.01904/0.01905. Two other variants behave differently. Inflation by 10001/10000 keeps MET through 0.01904. Acceptance without tolerance loses MET from 0.01901 on.

**Monotonicity.** In θ: θ = κ decides existence, and every δ_1 optimum sits at θ = 1/4 (Lemma 3.31 items 2 and 3). In β_0: ε_6 is nondecreasing, so a pair certified at β is certified at every smaller β, and δ_1 is nondecreasing in β_0 (Lemma 3.32). So every "largest β_0 on the grid" read is decided by its edge pair.

**The outputs.** δ_1 := min over certified (α, θ) of 6α e^{−4(θ−κ)}. The readout bound is T := (8489/10000)·6α e^{−8θ}, minimized over certified (α, θ). Both factors are 6, not the draft's 12 (section 3.12).

**The tail.** F_20(n + 1)/F_20(n) increases to μ for every n (Lemma 3.11). So F_20(49 + j) ≤ F_20(49)μ^j, and the closed form bounds the whole series for μx < 1 (Corollary 3.12).

**C_k, k ≥ 1.** δ′ := δ_k e^{δ_k} and λ(δ_k) := δ′ + ln(1 + δ′). C_k is MET when λ⁺ ≤ κ and NOT_MET when λ⁻ > κ. λ is read from an enclosure of e^{δ} and from alternating partial sums of ln(1 + x). The output is δ_{k+1} ≤ c_fin(δ_k)δ_k (Theorem G1). c_fin is the maximum of three entries. Its third entry is an exact maximum over integers f ≥ 4. The scan stops at the first f with e^{−(κ−λ⁺)f} at or below the best upper value so far, which bounds every later term. c_fin(δ) = e^{−1} exactly for 0 < δ ≤ 0.078733761 at κ = 1/4.

**The admissibility read on the β grid.** At a grid β_0, MET is the inequality S⁺(x⁺(α_c)) ≤ α_c at α_c := δ_crit⁻/6, so δ_1 ≤ δ_crit⁻. NOT_MET is the pair g⁻(α_c) > 0 and g′⁺(α_c) < 0 at α_c := δ_crit⁺/6. By convexity every α ≤ α_c then has g > 0, so the least root exceeds α_c and δ_1 > δ_crit⁺. A pole at x⁻(α_c) proves nothing here and reads UNDECIDED.

**The pinned grids.** θ ∈ {1/4 + i/64 : 0 ≤ i ≤ 320}, so θ ≤ 21/4. β_0 on the 10⁻⁵ grid. δ_crit⁻ on the 10⁻⁹ grid. α on dyadics of denominator 2⁴⁸. Upward rounding to 160 significant bits. A read on another grid is a new appended row (gate G_grids).

## 6. The self-map, summability and uniformity

**The domain of C_k.** δ_crit := sup{δ : λ(δ) ≤ κ} ∈ [0.114846768, 0.114846769] (TG). On the whole domain c_fin ≤ max{e^{−4κ}, e^{δ−κ/2}} < 1 (Lemma 4.17). At δ_crit⁻, c_fin ∈ [0.989898, 0.989899]. So the self-map test is λ(δ_1) ≤ κ alone (Corollary 4.20). Under the fallback 2δ′ ≤ κ the domain ends at δ ∈ [0.111780108, 0.111780109], and the factor is e^{−1} for δ ≤ 0.077320139.

**The window.** With the C03 head the self-map is MET at β_0 = 0.02074, with δ_1 ∈ [0.1088558, 0.1088559]. It is NOT_MET at 0.02075, with δ_1 ∈ [0.1158911, 0.1158912] > δ_crit⁺. The head-free vector reads the same pair, with δ_1 ∈ [0.1088527, 0.1088528] and [0.1158861, 0.1158862]. So β_ind ∈ [0.02074, 0.02075) with the C03 head, and β_ind < 0.02075 for every count vector N(4..10) ≥ 0. At 0.02075 the refined C_0 is still MET (C06), so β_ind sits one grid step below β_stop. With the crude head the self-map is MET at 0.01767 (δ_1 ∈ [0.1145675, 0.1145676]) and NOT_MET at 0.01768 (δ_1 ∈ [0.1150830, 0.1150831]), so β_ind^crude ∈ [0.01767, 0.01768) (TG; fallback 0.01761/0.01762). The fallback leaves the C03 and head-free edge at 0.02074/0.02075.

**Summability.** If λ(δ_1) ≤ κ, then δ_k ≤ c_fin(δ_1)^{k−1}δ_1 and Σ_k δ_k ≤ δ_1/(1 − c_fin(δ_1)), since c_fin is nondecreasing (Lemma 4.19, Corollary 4.20). The recomputed chains, all CONDITIONAL on G0 and G1:

| Row | β_0 | head | δ_1 | λ(δ_1) | c_fin(δ_1) | δ_2 ≤ | Σ_k δ_k ≤ |
|---|---|---|---|---|---|---|---|
| C07 | 1/100 | crude | [0.0055222, 0.0055223] | [0.0110902, 0.0110903] | e^{−1} | 2.0316e-3 | 8.737e-3 |
| C08 | 1/100 | C03 | [4.7159e-6, 4.7160e-6] | [9.4320e-6, 9.4321e-6] | e^{−1} | 1.7350e-6 | 7.461e-6 |
| C08 | 1/100 | head-free (lower limit) | [4.6861e-6, 4.6862e-6] | | | | |
| C11 | 1/64 | crude | [0.0508265, 0.0508266] | [0.1055724, 0.1055725] | e^{−1} | 1.8699e-2 | 8.041e-2 |
| C14 | 1/64 | C03 | [1.01738e-3, 1.01739e-3] | [2.0363e-3, 2.0364e-3] | e^{−1} | 3.7428e-4 | 1.6095e-3 |
| C12 | 1/50 | C03 | [0.0363235, 0.0363236] | [0.0746422, 0.0746423] | e^{−1} | 1.3363e-2 | 5.7463e-2 |
| C12 | 1/50 | head-free (lower limit) | [0.0363229, 0.0363230] | | | | |

e^{−1} ∈ [0.3678794, 0.3678795]. Every δ_1 in the table lies below 0.077320139, so the fallback gives the same factor. The crude C_0 is NOT_MET at 1/50 (C05, C12).

**Uniformity.** No constant of a step bound depends on N, K or the number of plaquettes (Theorem G0 (C5), Theorem G1 (C3)). G0 needs N even and N ≥ 8. The refined counts are lattice independent for n ≤ 2N − 1 (Lemma 3.14), so fine sides ≥ 8 cover the head n ≤ 10. The Fuss–Catalan tail needs only the degree bound 20 (Lemma 3.9).

**The flow to Haar (C16).** At β_0 = 1/100 with the crude constants, δ_20 ≤ e^{−19}δ_1 ≤ 3.0940e-11. On a final coarse 4⁴ torus with 1024 links, osc_V log ρ_m ≤ (512/e)δ_m (Lemma 4.21). So osc_V log ρ_20 ≤ 5.828e-9, and ρ_20 is within a factor e^{±5.828e-9} of Haar. This bound is per final torus. It is a statement about the certified class, whose only UV-complete member is the zero action. It says nothing about UV completeness of the theory.

**What moved against the draft and v2.** Every change comes from a proved constant (sections 3.12, 3.15, 4.15, 4.17).

| Quantity | draft and v2 | final |
|---|---|---|
| δ_1, T | 12α e^{−4(θ−κ)}, (8489/10000)·12α e^{−8θ} | 6α e^{−4(θ−κ)}, (8489/10000)·6α e^{−8θ} |
| C_k | 2δ′ ≤ κ/2 | λ(δ) ≤ κ |
| factor | c(δ) = e^{δ}[e^{−4κ} + max_n(…)] | c_fin(δ), = e^{−1} for δ ≤ 0.078733761 |
| δ_crit | [0.0496174, 0.0496175] | [0.114846768, 0.114846769] |
| regime | β_0 ≤ 0.01959 | β_0 ≤ 0.02074 |
| crude self-map edge | 0.01369/0.01370 | 0.01767/0.01768 |
| C07 c(δ_1) | [0.44504, 0.44505] | e^{−1} |
| C11 at 1/64 | C_1 and the crude self-map NOT_MET | both MET |
| C12 at 1/50 | C_1 NOT_MET for every count vector | refined chain MET; the head-free limit forces nothing |
| C16 δ_20; osc | [2.30e-9, 2.31e-9]; 4.35e-7 | ≤ 3.0940e-11; ≤ 5.828e-9 |
| C19 planted claim | "head-free self-map MET at 1/50" | "C_0 head-free MET at 0.02076" |

The C_0 edges do not move: 0.01904/0.01905 crude, 0.02075/0.02076 refined and head-free, and the wall 0.02247/0.02248.

## 7. Where the method stops

**The wall.** For θ ≥ κ and α > 0, x > εe^{κ}. If μe^{κ}ε_6 ≥ 1, the tail Σ_{n>n_max} 6F_20(n)xⁿ diverges for every finite head (Corollary 3.33, DERIVED, at equality too). The crossing μe^{1/4}ε_6 = 1 lies in β_wall(1/4) ∈ [0.02247, 0.02248]. The crossing μ ε_6 = 1, the limit κ → 0, lies in [0.02885, 0.02886]. The wall belongs to the Fuss–Catalan tail, not to the norm.

**At 1/45.** The wall quantity is in [0.9888, 0.9889] < 1, so the tail converges at small α. The NOT_MET at 1/45 is DERIVED only for the pinned certificate, n_max = 10 with every count vector, since 1/45 lies above the head-free edge 0.02076. A head with n_max > 10 is not covered there (OPEN).

**The C_0 edges.** Crude 0.01904/0.01905. Refined 0.02075/0.02076, the same pair as the head-free limit. So the exact counts move the edge from 0.01904 to within one grid step of the head-free limit, and the tail n ≥ 11 sets the window, not the head.

**The counting gap.** 6F_20(n)/N(n) lies in [1.09e10, 1.10e10] at n = 8, [2.31e12, 2.33e12] at n = 10 and [6.49e14, 6.50e14] at n = 12 (CONJECTURE on C03). Closed sets grow per plaquette by (19/2)^{1/2} ∈ [3.08, 3.09] and (1163/152)^{1/2} ∈ [2.76, 2.77], against μ ∈ [53.00068, 53.00069]. A growth bound on Lemma-B-closed sets below μ is one route to a wider window. No count bound reaches weak coupling with sup norms: ε_6(1) ∈ [0.740642074, 0.740642075] and ε_6(4) ∈ [4.29699629, 4.29699630] > 1 (C02).

**The Wilson term inside the norm.** At every scale |β_m| ≤ 0.62454δ_m (Lemma 4.22). On the domain δ_m < δ_crit⁺ this caps |β_m| below 0.07173. So H_k with the plaquette coupling inside Σ_Y R_k(Y) is a strong-coupling hypothesis at every scale. A weak-coupling H_k must carry the Wilson term outside the polymer norm.

**NOT_MET above the window is a method failure.** It is a failure of this norm, these counts and this bookkeeping. It is not evidence of a phase transition, a vanishing gap or anything about the theory.

**Comparisons.** The YM4-04B Dobrushin bound reaches β_0 < 1/18, for correlations only. One one-loop step per halving of the spacing is Δ_β = (11/(3π²))ln 2 ∈ [0.2575118, 0.2575119]. The wall is below 0.088 of one step, and the self-map window below 0.081 of one step.

## 8. Ties to exact data

**C09, the readout, low power.** The YM4-03C series P_10 must lie in 2t_2⁴ ± T at β_0 = 1/4000, 1/2000 and 1/1000. P_10 − 2t_2⁴ = (β⁸/2048)(1 − η) with η ∈ [0, 4e-7], and T exceeds it by a factor of at least 2.1 × 10¹². So containment can catch only a gross centering or sign error in G0. T/P_10 reads [5.2e-4, 5.3e-4] at 1/4000 (minimizing index i = 194), [8.3e-3, 8.4e-3] at 1/2000 (i = 150), [0.133, 0.134] at 1/1000 (i = 105), [0.557, 0.558] at 1/700 (i = 83), [1.032, 1.033] at 1/600 (i = 73) and [6.9e3, 7.0e3] at 1/100 (i = 0). The whole θ grid was scanned at each coupling, and each minimizing index beats its neighbours by a relative gap of at least 1.9e-5. That is four times the engine's dyadic resolution 2⁻⁴⁸/α_−, at most 4.7e-6. So the leading coarse coupling is resolved to 0.053 percent at 1/4000, and lost between 1/700 and 1/600. At 1/100 the certificate controls the action without resolving its leading coefficient. The exclusion is stated for clusters and DERIVED: every cluster other than (F_P) that holds ∂P in its coarse shadow has at least 8 plaquettes (Corollary 3.27).

**C10, the exact line channel.** A line-supported input blocks with no integral. The ratio of coarse to fine norm is e^{−4κ} exactly. By the slice bound every representation of the output has at least that norm (Lemma 4.23, Corollary 4.24). So no valid step bound has a factor below e^{−4κ}, and G1's c_fin = e^{−4κ} is optimal for 0 < δ ≤ 0.078733761.

**C10b, two objects.** log ρ_{k+1} = const + Σ_{P″} log c_0(2s√(2 + χ_{1/2}(V_{P″}))) exactly. The engine reads E_π[(χ_b + χ_t)^{2m}] = Cat_m(2 + χ_{1/2})^m for m ≤ 6. At s = 1/2000 the natural norm, which is the every-representation bound, is [4.077e-6, 4.078e-6]. It sits below c_fin(δ_in)δ_in by a factor in [2426.1, 2426.2], and below G1's per-root bound by a factor in [289.07, 289.08].

**C10c, one object through off links.** E_π[X] = χ_{1/2}(V_{P″})/2 by Schur orthogonality. Jensen and Hoeffding's lemma bracket the rest. At s = 1/65536 the natural norm sits below G1's per-root bound by a factor in [4.0902, 4.0908], and below c_fin(δ_in)δ_in by a factor in [6.5944, 6.5953]. This is the computed test of G1 with the most power. No SU(2) integral of X was computed before this freeze.

The substantive check of G0 and G1 is still the second-seat attack, gate G_attack (section 16). The computed tests above constrain G1 only through the channels they excite.

## 9. Gauge separation

**C18.** The line gauge is computational. The exact integrals Φ_S(j; V) of the YM4-03C classes read the same with V at position 1, gauge (1, V), as at position 0, gauge (V, 1). They are unchanged under coarse gauge transformations extended to the midpoints. prefreeze=NONE.

**W05.** The transverse tree-level corner ratio is 15/28 in the covariant gauges ξ = 1/2, 1 and 3, and by the gauge-free route. A coupling read from the longitudinal mode, (ξ/4)/C′_{νν}(ξ), gives 3675/7372, 35/48 and 11025/10456. They are pairwise unequal, so the read is a gauge artifact. The engine's invariance check must flag and refuse it.

**The rule.** No invariant statement of this note fixes a gauge. Every norm is a sup norm of an invariant function.

## 10. Lane W: tree-level and Gaussian diagnostics

These rows are counted nowhere toward H_k ⇒ H_{k+1}. They test necessary conditions for any weak-coupling induction built on a blocking map M.

**H_k^W(M).** r_k(p) := lim_{β→∞} β_k(p)/β for the abelian σ_3 coarse plane wave of momentum p = q e_ν, with polarization perpendicular to p, and p̂² := 4 sin²(q/2). A_k is the exact limit of (1/r_k(p) − 1)/p̂² as q → 0. The conditions are: (i) classical marginality, r_k(p) → 1 as q → 0; (ii) the irrelevant part is bounded uniformly in k; (iii) a plaquette small-field condition with k-independent p_SF keeps a k-independent Gaussian large-field probability; (iv) the small-field threshold and a fine large-field bound pass one step without loss.

**W01: the line map grows like 2^k.** For the composition B_{2^k} = B_b with b = 2^k, the alias formula gives

```text
A_b = b^{-2} sum_{n in Z_b^3, n != 0} 1/khat^2(2 pi n / b)  -  (1 - b^{-2})/12,        khat^2(k) = sum_{i=1}^{3} 4 sin^2(k_i/2).
```

*Claim (DERIVED).* A_b/b → G_3(0) := ∫_{[−π,π]³} d³k/((2π)³ k̂²(k)) as b → ∞.

*Proof.* The second term divided by b tends to 0. Put f(k) := 1/k̂²(k) on the torus [−π, π)³, with f(0) := +∞. Take the representatives n ∈ {−b/2 + 1, …, b/2}³ and k_n := 2πn/b. Then b⁻³Σ_{n≠0} f(k_n) = ∫ f_b dμ, with dμ = d³k/(2π)³ and f_b the step function equal to f(k_n) on the cube C_n of side 2π/b centred at k_n, and 0 on C_0. Write |k| for the distance from k to 2πℤ³. Since sin(x/2) ≥ x/π on [0, π], k̂²(k) ≥ (4/π²)|k|², so f(k) ≤ (π²/4)|k|⁻². For n ≠ 0, |k_n| ≥ 2π/b, and every k ∈ C_n has |k| ≤ |k_n| + √3π/b ≤ 2|k_n|. So f_b(k) ≤ (π²/4)|k_n|⁻² ≤ π²|k|⁻² on the whole torus. Fix r ∈ (0, 1). On the ball |k| < r, ∫ f_b dμ ≤ π²·4πr/(2π)³ = r/2 and ∫ f dμ ≤ r/8. Take b with 2√3π/b < r/2. Then every cube that meets {|k| ≥ r} lies in {|k| ≥ r/2}, where f is uniformly continuous. So sup_{|k|≥r} |f_b − f| → 0 as b → ∞. Hence lim sup_b |∫f_b dμ − ∫f dμ| ≤ 5r/8 for every r, and the limit is ∫f dμ = G_3(0). ∎

G_3(0) > 0, since the integrand is positive. So A_{2^k} grows like G_3(0)·2^k, and no k-uniform bound on the irrelevant part holds for the line map: H_k^W(ii) is NOT_MET. The k = 1, 2, 3 values are checks of this limit, not its proof. Three scales alone do not show unboundedness. A_1 = 23/96, A_2 = 1367/1920 and A_3 = 113360987/66106880 ∈ [1.7148137531, 1.7148137532]. A_3 is rational because the √2 parts cancel at b = 8. A_k/2^k = 23/192, 1367/7680, 113360987/528855040, strictly increasing and below G_3(0) ∈ [0.2527310, 0.2527311] (Watson, REPORTED, used only for these inequalities). The corners are r_1 = 15/28, r_2 = 25823/98640 and r_3 ∈ [0.1274530942, 0.1274530943].

**W02: the linearized average converges.** For the abelian linearization of the average of b-step transporters over the b^d offsets of a block, the corner is 3b²/(b² + 2) = 2, 8/3, 32/11 at b = 2, 4, 8, tending to 3. The slope is −(1 − 1/b²)/6 = −1/8, −5/32, −21/128, tending to −1/6. The deviations shrink per doubling of b by the factors 3 and 11/3 (corner) and 4 and 4 (slope). The non-abelian averaged map is not constructed (OPEN).

**W03: the dimension dependence.** In d = 2, r = 1/b² exactly and A = 0, the tree-level image of YM4-03 Theorem 8. In d = 3, A = 3/32, 73/384 and A(8) = 54335/182784 ∈ [0.2972634366, 0.2972634367]. The increments are 37/384 and 6529/60928 ∈ [0.1071592, 0.1071593], both inside [0.09, 0.12]. The draft's bracket [0.10716, 0.10717] excluded 6529/60928 and is corrected. In d = 4 the growth is linear (W01). So the degradation is absent, logarithmic and linear in d = 2, 3, 4.

**W04: roughening, a reproduction row.** The flux variance of the scale-k coarse plaquette grows like 2^k at the Gaussian level; the infinite-volume ratio r_{k+1}/r_k → 2 is DERIVED by the perimeter law. Its finite-volume brackets were set around float reads, so W04 is a reproduction and enters no count of confirmed predictions.

**W06: fiber positivity.** The Gaussian fluctuation operator of one line-map step is positive in every Bloch sector of fine 4⁴ and 8⁴ and in the twisted sectors t_tw ∈ {1/2, 1/4, 1/8}. The arithmetic is exact in ℚ, ℚ(i) and ℚ(ζ_8), with sign tests in ℚ(√2). The k′ = 0 gap is the smallest root of y³ − 18y² + 80y − 48, in [0.7084973778, 0.7084973779], multiplicity 4. A whole-zone lower bound needs a covering certificate (OPEN).

**W07: the 16-per-step threshold.** On a fine 2 × 2 tile, 1 − a(V′) ≤ 16 max_i(1 − a(U_{p_i})). On the aligned abelian tile the ratio is exactly 16 − 40ε + 32ε² − 8ε³ = 8(1 − ε)²(2 − ε), with ε = 1 − cos φ. It tends to 16 as ε → 0 and is below 16 at every ε > 0. So union-bound inheritance of a fine large-field bound loses 16 per step, and LF_{k+1} must come from ρ_{k+1}'s own effective action (OPEN).

**What these rows mean.** An averaging map is needed at least at tree level, and the large-field set at scale k + 1 must come from ρ_{k+1}'s own action. **What they do not mean.** Nothing about finite β, nothing about a non-abelian average, nothing about Δ_β.

## 11. The theorem dependency ledger

Symbols: the Kotecky-Preiss pair is (alpha, theta); a is (1/2)Re Tr only; b is the blocking factor only; kappa is the norm weight 1/4 only; delta' = delta e^delta and lambda(delta) = delta' + ln(1 + delta'); the one-loop step per halving is Delta_beta.

| id | statement | status | source | role in this step, and what would promote it |
|---|---|---|---|---|
| L01 | YM4-03 Theorem 4 (exact Haar pushforward rho = B_* mu, gauge covariance), Lemma 3 and Proposition 2 (line-supported loops block with no integral) | DERIVED, merged | PR #29, NOTE-YM4-03 | defines H_k; G0 (Lemma 3.3), G1 (Lemma 4.2), C10, C10c, C18. |
| L02 | YM4-03C Lemma A (one position), Lemma B (closure), Lemma C (parity) | DERIVED, merged | PR #41, NOTE-YM4-03C §2, §6 | G0 (Lemmas 3.4, 3.21), G1 (Lemma 4.3, which proves Lemma A for every invariant integrand), C01, C03, C09's cluster exclusion. |
| L03 | YM4-03C coefficient table through beta^10 (c_1/2 = beta^4/128 - beta^6/768 + beta^8/1536 - 467beta^10/2211840; chair 3/524288 in log rho) | MEASURED, 92/92 MET | receipt sha 76dc01b7 | control series for C09; the Wilson-term norm in C08, read from P_10 and not certified at 1/100, where T/P_10 is in [6.9e3, 7.0e3]. A finite series is never scale-to-scale control (operator, 2026-11-08). |
| L04 | YM4-04A global Cauchy remainder, valid at beta <= 1/(8N_p) | DERIVED, merged; proved at b = 3, and its Cauchy argument (abs(X) <= N_p for the fine plaquette sum) does not use the blocking factor, so the hypothesis stands at b = 2 | PR #36 | superseded locally at beta_0 <= 0.02074 (the 10^-5 grid; equivalently C_0 MET and lambda(delta_1) <= kappa) by L11 if G0 and G1 survive gate G_attack; compared in C17. |
| L05 | YM4-04B Dobrushin comparison, alpha_D <= 18beta, beta_0 < 1/18, correlations only | DERIVED with a REPORTED theorem | PR #37 | comparison point only (C04, C15); not an effective-action norm. |
| L06 | Kotecky-Preiss criterion: test-set form and per-polymer corollary with the weight e^{d(X)} | REPORTED, relied on by G1 (Theorem 4.9), not reproved; for G0 a cross-reference only, since Proposition 3.18 proves the bound G0 uses | Commun. Math. Phys. 103 (1986) 491-498 | G1. Its text was not re-read in this session. |
| L07 | Finner's generalized Holder inequality, exponent 6 | REPORTED | Ann. Probab. 20 (1992) 1893-1901 | G0 (Lemma 3.8), C02. |
| L08 | BFS injection of off-link-connected plaquette sets into the complete 20-ary tree; Fuss-Catalan count F_D(n) = C(Dn, n)/((D-1)n + 1); F(n+1)/F(n) increasing to mu for every n | DERIVED in note §3 (Lemmas 3.9, 3.10, 3.11), with full proofs; Graham, Knuth and Patashnik and Dvoretzky-Motzkin are cross-references | C01 checks the ratios for n <= 59 and A_c(n) <= 6F_20(n) for every off-link-connected set through n = 5 | G0's tail; the wall of C04 and C15. CONDITIONAL only through gate G_attack. |
| L09 | G0: C_0(beta_0) MET => H_1(1/4, delta_1), delta_1 = 6alpha e^{-4(theta-kappa)}, with the readout T = (8489/10000)6alpha e^{-8theta} | DERIVED in note §3, with its constants table; CONDITIONAL on gate G_attack, OPEN | note §3; three pre-freeze lenses (KP, counting, assembly), each GAP on the factor 6, repaired | values in C07, C08, C09, C11-C14, C16; meaning of C04-C06, C15. Promoted only by the filed second-seat attack of the final §3 plus engine and check agreement. |
| L10 | G1: lambda(delta_k) <= kappa => H_{k+1}(1/4, c_fin(delta_k)delta_k): line channel, tree-graph bound in the (1+t)^f form with t = delta', KP per-polymer corollary with alpha = t and theta = kappa, roots that hold a line link | DERIVED in note §4, with its constants table; CONDITIONAL on gate G_attack, OPEN; the (1+t)^f step and the root restriction m >= 1 were not read by a second seat (TG; fallback 2delta' <= kappa) | note §4; three pre-freeze lenses (tree-graph GAP, channel HOLDS, structure HOLDS), repaired | C07, C08, C10b and C10c (the c_fin(delta_in) and per-root comparisons), C11-C14, C16. Exact data constrain it from below for every representation (C10, Corollary 4.24: G1 is optimal for delta <= 0.078733761), and with slack [289.07, 289.08] per root (C10b, s = 1/2000) and [4.0902, 4.0908] per root (C10c, s = 1/65536). |
| L11 | Self-map and summability: lambda(delta_1) <= kappa, that is delta_1 <= delta_crit in [0.114846768, 0.114846769], => delta_k <= c_fin(delta_1)^{k-1}delta_1 and sum delta_k <= delta_1/(1-c_fin(delta_1)), uniform in N and K, with c_fin <= max{e^{-4kappa}, e^{delta-kappa/2}} < 1 on the whole domain | CONDITIONAL on L09, L10; the arithmetic was COMPUTED before the freeze and is read by the engine | C13, C14 | the issue-#4 shape (explicit H_k, norm, gauge, constants, summable volume-uniform errors), but only for beta_0 <= 0.02074 (beta_ind in [0.02074, 0.02075)), strong coupling; by Lemma 4.22 the class's plaquette coupling stays below 0.62454 delta_m at every scale. |
| L12 | The certified class flows toward Haar: osc log rho_20 <= 5.828e-9 at beta_0 = 1/100 on a coarse 4^4 torus | CONDITIONAL | C16 | a statement about the class (the only UV-complete member is the zero action); nothing about the theory. |
| L13 | Method wall: no certificate of this form (kappa = 1/4 sup norm, KP with theta >= 1/4, any finite head with the 6F_20(n) tail beyond n_max) at beta_0 above beta_wall in [0.02247, 0.02248]; the kappa -> 0 crossing is in [0.02885, 0.02886]. The wall belongs to the Fuss-Catalan tail, not to the norm: a closed-set growth bound below mu (L14) would move it | DERIVED (Corollary 3.33; it holds at equality) | C04, C15 | a limit of this method, not physics. At 1/45 (wall quantity in [0.9888, 0.9889]) the NOT_MET is derived only for n_max = 10. |
| L14 | Counting gap: Fuss-Catalan mu in [53.00068, 53.00069] per plaquette against closed-set growth (19/2)^{1/2} in [3.08, 3.09] and (1163/152)^{1/2} in [2.76, 2.77] per plaquette (n = 8-12); the refined C_0 edge equals the head-free edge | CONJECTURE (C03, C06), pre-freeze cross-read; the counts are lattice independent for n <= 2N-1 (Lemma 3.14, DERIVED) | C03, C06 | a growth bound for Lemma-B-closed sets would widen the window: OPEN. It is one route. No count bound reaches weak coupling with sup norms, since eps_6 exceeds 1 by beta = 4. |
| L15 | Gauge separation: the line gauge is computational; the longitudinal tree-level read is an artifact | DERIVED; read by C18 (CONTROL) and W05 (NEGATIVE_CONTROL) | C18, W05 | issue #4's separation of gauge-fixing artifacts from invariant statements. |
| L16 | Tree-level line map B_{2^k}: marginal (beta'_G = beta in d = 4); irrelevant part A_{2^k} with A_b/b -> G_3(0) > 0 (a Riemann sum, proved in note §10); corner halves per step | DERIVED; exact finite computations as checks (A_3 = 113360987/66106880); G_3(0) REPORTED (Watson, Quart. J. Math. Oxford 10 (1939) 266-276) | W01 | the line map cannot carry a k-uniform weak-coupling norm even at tree level. |
| L17 | Tree-level linearized block average: irrelevant part converges (corner -> 3, slope -> -1/6) | DERIVED for the abelian linearization only | W02 | a non-abelian averaged SU(2) map with covariance, positivity and RP is NOT CONSTRUCTED: OPEN. |
| L18 | Dimension dependence of the line map's degradation: none (d = 2), logarithmic (d = 3, increments 37/384 and 6529/60928), linear (d = 4) | DERIVED | W03 | d = 2 closure (YM4-03 Thm 8) transfers nothing to d = 4. |
| L19 | Gaussian line-map fluctuation operator positive in every Bloch sector; k' = 0 gap in [0.7084973778, 0.7084973779] (multiplicity 4) | DERIVED; (b) cross-read by exact inertia before the freeze | W06 | analog of Balaban's propagator bounds at Gaussian level only. A whole-zone lower bound (covering certificate) is OPEN. |
| L20 | Line-map coarse plaquette roughens: r_k grows like 2^k (Gaussian) | the infinite-volume limit DERIVED; the finite-volume intervals are a reproduction of float reads, not a prediction | W04 | a plaquette small-field condition with k-independent p_SF fails for B at Gaussian level. |
| L21 | Threshold recurrence: deterministic small-field propagation needs eps_{k+1} >= eps_k(16 - 40eps_k + 32eps_k^2 - 8eps_k^3), and union-bound large-field inheritance loses 16 per step | DERIVED | W07 | surfaced error-growing recurrence: LF_{k+1} must come from rho_{k+1}'s own effective action: OPEN. |
| L22 | Divergent recurrence surfaced: along beta_{k+1} = beta_k - Delta_beta (Delta_beta = (11/(3pi^2))ln2 in [0.2575118068, 0.2575118069]), sum_k 1/beta_k >= (1/Delta_beta)log(beta_0/16) -> infinity as h_0 -> 0 | DERIVED remark (from small-large-field R14; not a row, since no falsifier touches the measure) | ledger only | a weak-coupling H_k must move the marginal part of order 1/beta_k into beta_{k+1}, and carry a contraction factor below 1, or a remainder bounded by a stated constant times beta_k^-2, on the rest. By Lemma 4.22 it must also carry the Wilson term outside the polymer norm. No unquantified O(.) is admitted. |
| L23 | Balaban's small-field/large-field decomposition and large-field suppression exp(-c p(g)^2) with p(g) -> infinity | REPORTED (CMP 95-122, 1984-89), bodies CANNOT_SEE, NOT reached | NOTE-YM4-03 §7a | OPEN. |
| L24 | Balaban averaging operations with gauge fixing in blocks (CMP 98); Gaussian background-field integration; effective-coupling recursion g_{k+1}^-2 = g_k^-2 + beta_0 + r_k, with abs(r_k) bounded by a constant of Balaban's papers times g_k^2 (CMP 109; the constant is not reproduced here) | REPORTED, NOT reached | Dimock's expositions (arXiv:1108.1335, 1712.10029) REPORTED | OPEN. Delta_beta serves only as a scale: the certified window is under 9% of one step (0.02075/0.2575118 < 0.081). |
| L25 | CMP 122 Theorem 1 (effective-density bound with E± independent of k and volume, assuming the couplings stay in (0, gamma]); Theorem 2, which removes the assumption, unpublished per GPT-6's reading | REPORTED, CANNOT_SEE | PR #29 discussion | the S lane reproduces only its SHAPE (abs(log rho_k - const) <= (#links/(4e))delta_k) at g_k^-2 -> 0. That is no test of Balaban's estimate. |
| L26 | Crossover from beta_0 near 0.02 to the scaling region | no known rigorous method | — | OPEN. |
| L27 | Relevant counterterms (absent in the certified flow, where the plaquette coupling is irrelevant-like, with leading term beta^4/64 from the MEASURED P_10); possible non-quasilocality of the decimation at weak coupling (van Enter-Fernandez-Sokal analog) | untested / CONJECTURE undecided | — | OPEN. |
| L28 | Infrared limit, OS reconstruction (YM4-05), physical mass gap (YM4-06), other gauge groups (YM4-07), independent audit (YM4-08) | OPEN | PROOF_OBLIGATIONS.md | not touched by any row. No OPEN gate is promoted by finite examples. |

## 12. The engine, the independent check, planted faults and CI, as a plan

The plan is text only. No engine code exists. It is also filed as `engine_plan-final.txt`.

```text
ENGINE PLAN, final, for YM4-04C (text only; no engine code exists; note section 12). Carries the v2 plan to the constants proved in note sections 3 and 4: delta_1 and T with the factor 6, the C_k test lambda(delta) <= kappa, the factor c_fin(delta), the slice and per-root comparisons of C10b and C10c, and the recomputed fault values.

Symbols, binding: the Kotecky-Preiss pair is (alpha, theta), a(gamma) = alpha*#off(gamma), d(gamma) = theta*#gamma, theta in {1/4 + i/64 : 0 <= i <= 320}; at step k, #gamma := (1/2)#line(supp gamma). a is (1/2)Re Tr only. b is the blocking factor only. kappa is the norm weight 1/4 only. delta' = delta e^delta and lambda(delta) = delta' + ln(1 + delta'). The W-lane momentum is q, with p = q*e_nu and t_W = tan(q/2).

Freeze order:
1. One commit carries the prediction file (41 lines, pinned by head -n 41 | sha256sum), the note sections 0-18 with G0 and G1 proved in full in sections 3 and 4, and reviews/ym4-04c-prediction/ with derive_checks.py and DERIVE-CHECKS.hbp, the three manifests (MANIFEST-ym4-04c-scratch.sha256, 67 files; MANIFEST-ym4c-v2-checks.sha256, 19 files; MANIFEST-ym4c-pkg.sha256, 116 files) and every file they list. Sections 3 and 4 end with constants tables. The constants the rows carry are the proved ones: the scalar inequality S(eps_6 e^{2alpha+theta}) <= alpha with a valid head, delta_1 = 6alpha e^{-4(theta-kappa)}, T = (8489/10000) 6alpha e^{-8theta}, lambda(delta) <= kappa, and c_fin(delta).
2. A second seat of the owner's choosing attacks the final sections 3 and 4 as written, the (1+t)^f tree-graph step and the root restriction m >= 1 included, and files the attack (gate G_attack). No engine code before this filing.
3. Engine commit.
4. Independent check commit.
5. CI.

Arithmetic everywhere: Python ints and fractions.Fraction (engine) and Rust i128 with its own bigint (check). No floats, under scripts/no_float_gate.py and scripts/no_float_compiled.sh. Dyadic outward rounding helpers up(x) and down(x) at 160 significant bits. exp by Taylor series with a geometric remainder after range reduction; ln(1+x) by alternating partial sums (engine) and by the atanh series (check); pi by Machin with alternating tails; ln 2 by two series.

ENGINE: tests/test_ym4_04c_polymer_norm.py (S lane) and tests/test_ym4_04c_tree_gaussian.py (W lane). They write tests/YM4_04C_RECEIPT.hbp, one row per read. Every receipt row carries its tag and its prefreeze field (CROSS_READ, COMPUTED or NONE). The receipt's tally of confirmed predictions counts only prefreeze=NONE rows and clauses. Every CROSS_READ or COMPUTED read is tallied as a reproduction.

- E0 geometry (C01). Coordinate tuples on (Z/8)^4 and (Z/12)^4. Line and off links. Plaquette off-link lists. The adjacency census (D = 20, min 10), #W(e_0) = 12, #W'(l) = 6, the filling-membership histogram, and an exhaustive search of closed sets of at most 4 plaquettes. An exhaustive enumeration of all off-link-connected sets of n <= 5 plaquettes, closed or not, grown from the 6 plaquettes through one seed off link per class (c = 1, 2, 3), with no closure pruning and dedup by canonical form. It reads A_c(n) against 6F_20(n) = 6, 120, 3540, 123240, 4705470. The read is the inequality only; no count is frozen. The per-root count at n = 2 (20 = F_20(2) for a plaquette with 4 off links, against F_19(2) = 19). F_20 as exact binomials; F(n+1)/F(n) < mu checked for n <= 59 (the all-n statement is note Lemma 3.11).
- E1 counts (C03, C09 exclusion, Finner guard). Closure-driven DFS growth from the 6 plaquettes through a seed off link of each class. Pruning: open links <= 4 x remaining size. Canonical forms under coarse translations x 384 signed permutations, keyed by hash; each class weighted by the number of its members that hold the seed link, since N_w(n) counts sets. Runs to n = 12 on both lattices. Also emits the held-coarse-link split for n <= 7 (C09) and the maximum off-link incidence per set (G_finner_guard).
- E2 enclosures (C02, C04, C15). c_0 partial sums with geometric tails. eps_6^6 as an interval alternating sum, and its sixth root by dyadic bisection to 10^-12. Wall bisections on the 10^-5 grid.
- E2g the C04 guard. Before E3 serves any row, E3 reads the refined C_0 (the C03 head, the pinned S) at beta_0 = 1/40 and at 0.02248, the upper end of the wall bracket. Both must read NOT_MET by the pole: mu e^{1/4} eps_6^- >= 1.1125 at 1/40 and >= 1.00035 at 0.02248, so mu x >= 1 for every alpha >= 0 and theta >= 1/4. A MET at either point exits 1 at C04.
- E3 KP certificate (C05, C06, C09, C12, C15).
  - S^+(x): the head counts, the series to n = 48 and the n = 49 tail. The test mu^+ x^+ < 1 comes first; its failure reads NOT_MET. 1 - mu^+ x^+ goes in the tail denominator, and every other operation rounds upward (note Lemma 3.30).
  - For each theta on the grid i <= 320: ternary search for min g on dyadic alpha of denominator 2^48, then the least root by bisection. A MET read is the exact inequality S^+(eps^+ e^{2alpha+theta}) <= alpha <= 1/4 at that rational alpha.
  - A NOT_MET read is a proof. It is one of: the pole at alpha = 0; S^-(x^-(0)) > 1/4; or the convex tangent bound g^-(alpha_m) - |g'|^+(alpha_m) max(alpha_m, 1/4 - alpha_m) > 0 at the ternary minimizer alpha_m, with g'(alpha) = 2x S'(x) - 1 enclosed from both sides. g is convex because S has nonnegative coefficients. theta = 1/4 decides every grid theta, because S(eps e^{2alpha+theta}) increases in theta. If no proof closes, the read is UNDECIDED and is filed, never rounded to NOT_MET.
  - delta_1 = min 6alpha e^{-4(theta-kappa)}, read at theta = 1/4. T = (8489/10000) 6alpha e^{-8theta}, minimized over the whole grid.
- E4 C_k and c_fin (C07, C08, C10b, C10c, C11-C14, C16). lambda(delta) from enclosures of e^delta and ln(1 + delta'). The test lambda^+ <= 1/4 reads MET; lambda^- > 1/4 reads NOT_MET. c_fin as the maximum of its three entries. The third entry is an exact maximum over integers f >= 4, scanned from f = 4 and stopped at the first f with e^{-(kappa - lambda^+)f} at or below the best upper value so far, which bounds every later term; the real maximizer f* = ln(kappa/(kappa - lambda))/lambda is a check. delta_crit^- and delta_crit^+ by bisection of lambda = kappa on the 10^-9 grid. The fallback 2delta' <= kappa and its factor are read beside the final ones and filed as separate receipt rows for the TG values.
- E5 edges. At each predicted edge pair and listed point, read MET/NOT_MET on the 10^-5 grid. The admissibility read at beta: MET when S^+(x^+(alpha_c)) <= alpha_c at alpha_c = delta_crit^-/6; NOT_MET when g^-(alpha_c) > 0 and g'^+(alpha_c) < 0 at alpha_c = delta_crit^+/6, which by convexity puts the least root above alpha_c; a pole at x^-(alpha_c) is UNDECIDED. Bisection only locates; rows read the pair.
- E6 exact integrals (C10, C10b, C10c, C18).
  - Rational unit quaternions by the Cayley map, and exact holonomies.
  - The engine's own one-link projector integrator to degree 12 (Weingarten over non-crossing matchings).
  - C10: the line channel ratio at kappa = 1/4 and kappa = 0, under 4 coarse gauge transformations. The norm routine counts #Y as all links of Y; the planted one_position_support counts only its position-1 links.
  - C10b: E_pi[(chi_b+chi_t)^{2m}] = Cat_m (2+chi)^m for m <= 6 at 4 rational V. The natural norm 3e^{4kappa} log c_0(4s), which the slice bound makes the every-representation bound, the per-root bound e^{delta-4kappa}(e^{2lambda}-1) delta_in, and the projection bound.
  - C10c: mu_m(V) = E_pi[X^m], X = chi_1/2(A pi) chi_1/2(pi^{-1} B), for m = 1..6, at 7 rational coarse configurations with distinct chi_1/2(V_P'') and at 4 more under rational coarse gauge transformations. The two arm links are integrated one at a time, degree <= 2m <= 12 per link. Each mu_m is fixed as a polynomial of degree <= m in chi_1/2(V_P'') by the 7 values and checked at the 4 more. Then the cumulants, the s^1..s^6 Taylor polynomial of f = log E_pi[e^{sX}], the tail bound (1/2) sum_{m>=7} (16s)^m, osc(f) over chi_1/2 in [-2, 2], delta_out^nat = 6e osc(f)/2, the per-root bound e^{delta-6kappa+2lambda} delta_in, c_P = E[f chi_1/2] and the projection bound, at s = 1/8192 and 1/65536. The read compares them with the brackets, with the per-root bound and with c_fin(delta_in) delta_in.
  - C18: Phi_S(j;V) for the YM4-03C classes in gauges (1,V) and (V,1), and under coarse gauge transformations.
- E7 volume (C17). E0, E1 and E3 on both lattices, compared byte for byte. 1/(8N_p) exactly.
- E8 W lane.
  - W01-W03, W05: alias sums in exact rationals at b = 2, 4, with sqrt2 pairing. At b = 8, A in Q(sqrt2), where it is rational; the corner by dyadic intervals in Q(sqrt2, sqrt(2+-sqrt2)). Covariant-gauge G_munu(xi).
  - W06: exact LDL^* inertia on the 45-dimensional physical fiber over Q (t_tw = 1/2 and phases +-1), Q(i) (t_tw = 1/4 and phases +-i) and Q(zeta_8) = Q(i, sqrt2) (t_tw = 1/8, phase e^{i pi/4}). Pivots of the Hermitian pencil lie in Q, Q and Q(sqrt2). The sign of u + v sqrt2 is decided exactly: by the signs of u and v when they agree, and by comparing u^2 with 2v^2 when they differ. Bisection to 10^-10.
  - W04: orbit-reduced exact Poisson solve (70 and 495 unknowns), then loop sums. W04 is a reproduction row: its receipt row is tallied as a reproduction.
  - W07: 10^4 tiles from a seeded integer LCG and the aligned family.
- E9 receipts and sabotage. SABOTAGE=<name> is read once, and every guard runs before its quantity is used. Each fault recomputes only the sections it reaches; the others replay from the receipt by sha256 (the YM4-03 replay of PR 43). The evidence chain HBI -> HBP -> SHA -> SEAL follows YM4-03C.

INDEPENDENT CHECK: reviews/ym4-04c-check/ym4_04c_check.rs. Rust 1.81, std only, sharing no code with the engine; it may copy the generic bigint of the merged YM4-03C engine. Every module uses a different algorithm.
- X0: census through a link-plaquette incidence matrix and a union-find adjacency. A_c(n) for n <= 5 by breadth-first layered growth with a canonical deletion test.
- X1: counts by layer-by-layer canonical augmentation (BFS over n, canonical deletion test) instead of DFS closure growth, on both lattices.
- X2: c_0 also by the Bessel-ratio continued fraction; exp by binary splitting with range reduction; pi by two Machin formulas.
- X3: KP by monotone Newton from alpha = 0 on the convex g, a different route from the engine's ternary search. Newton from the left on a convex decreasing g stays below the least root alpha_- and converges to it. When an iterate has g' >= 0 before g reaches 0, g has no root and the check proposes NOT_MET. A MET proposal alpha_N is read as the exact inequality at alpha_N + 2^-30. A NOT_MET proposal is read by the convex tangent bound at an alpha_m found by bisection on the sign of g'. The certifying alpha-intervals at the C_0 edges are 3.7e-3 to 7.7e-3 wide, so 2^-30 lands inside them. Demonstrated in scratch at the crude edge (v2-checks/x3_newton_demo.out), and used for every root bracket of pkg/recompute/final_s_lane.py.
- X4: lambda(delta) through ln(1+x) = 2 atanh(x/(2+x)); c_fin through the closed-form maximizer f* and its two neighbouring integers; delta_crit by an independent bisection.
- X5: exact integrals through 2I averages in Q(sqrt5) inside degree 11 and a separate Weingarten table at degree 12; C10b's and C10c's moments; C18 through the merged YM4-03C engine.
- X6: W lane by the other route to E8's: route B Bloch KKT where E8 uses route A, and vice versa. Sturm sequences in place of LDL^* inertia, over Q(sqrt2) for the t_tw = 1/8 sectors (the characteristic polynomial of the Hermitian pencil has coefficients in the real subfield). A full 4096-unknown exact sparse solve on 8^4 against the orbit solve.

Both write receipts. CI requires every read to agree.

PLANTED FAULTS (C19), each to exit 1 on its named check.
- finner_exponent_2 -> G_finner_guard. The guard reads the maximal off-link incidence of the 10-plaquette filling-plus-cube set, 4, and tests sum 1/q <= 1, which reads 2 > 1. A comparison of numbers on that set would not catch it (note §3.4).
- degree_19 -> C01 (the degree census and the per-root count at n = 2).
- missing_tail -> C04. The change: S is replaced by the head-only polynomial sum_{n=4..10} N(n) x^n with the C03 head; the terms n = 11..48 and the n = 49 tail are removed. Effect: the C04 guard (E2g) reads the refined C_0 MET at 1/40 and at 0.02248, certified at alpha = 2^-22 with S^+ <= 1.96e-7 and <= 1.28e-7. Variants that would not fire: a cut at 10 with the crude head, or a cut at 48 with any head, leave both reads NOT_MET.
- one_position_support -> C10. The change: the norm routine sets #Y to the number of links of Y at position 1 (the links that carry V in the line gauge (1,V)) in place of all links of Y. Effect: C10's fine norm reads 12|s| e^{4kappa} and the ratio reads 1 in place of e^{-1} at kappa = 1/4. The drafted variant (a coarse link counted as held from one position) leaves #Y'' = 4 on C10's input and would not fire.
- global_norm -> C17.
- readout_without_tail -> C09. P_10 - 2t_2^4 = (beta^8/2048)(1 - eta), eta in [0, 4e-7], at the three containment couplings, so T := 0 fails containment at all three.
- iteration_cap_400 -> C05. The change: at every grid theta the convex search and the exact read are replaced by the iteration alpha_0 = 0, alpha_{j+1} = s_j := S^+(up(eps_6^+ e^{2alpha_j+theta})). It reads MET at the first j with s_j <= alpha_j (1 + 10^-40), and NOT_MET when s_j is undefined or above 1/4, or after 400 evaluations of S^+. Effect: MET at 0.01901 (step 352), NOT_MET at 0.01902, 0.01903 and 0.01904 at every grid theta, so C05's MET at 0.01904 is lost. Variants that differ: alpha_{j+1} = up(s_j 10001/10000) with acceptance s_j <= alpha_j reads MET through 0.01904 and would not fire; alpha_{j+1} = s_j with acceptance s_j <= alpha_j loses MET from 0.01901 on.
- delta_crit_surrogate -> C13. The change: delta_1 <= 49/1000 in place of delta_1 <= delta_crit^-. Effect: MET lost at 0.01553-0.01767, so the faulted crude edge reads 0.01552/0.01553 (TG; fallback range 0.01553-0.01761).
- readout_grid_128 -> C09. The change: theta cut at i <= 128. Effect: T/P_10 in [1.47e-2, 1.48e-2] at 1/4000 (minimizing i = 128), outside [5.2e-4, 5.3e-4].
- drop_alias_terms -> W01 (only the n = 0 alias kept: corner r_1 = 2).
- longitudinal_read_unflagged -> W05.
- float_literal -> G_nofloat.

Planted false claims, read from a planted copy of the prediction file, must read NOT_MET:
- C_0 crude MET at 1/50 (miss at C12)
- C_0 head-free MET at 0.02076 (miss at C06)
- r_2 = r_1 for the line map (25823/98640 ne 15/28)
- the averaged corner equal to the line corner (2 ne 15/28)

CI: .github/workflows/ym4-04c-polymer-norm.yml.
1. The no-float gates (Python and compiled).
2. The prediction pin: head -n 41 docs/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp | sha256sum against the pinned value. The 41 lines are every frozen row; appended rows start at line 42.
3. The manifest check: sha256sum -c over reviews/ym4-04c-prediction/ against the three manifests.
4. derive_checks.py, with its output compared byte for byte with DERIVE-CHECKS.hbp.
5. The engine run, with the receipt sha256 compared to its pin.
6. The check run, with its receipt and the cross-compare of reads.
7. 12 sabotage runs, each required to exit 1 naming its check, with replay of untouched sections.
8. 4 planted-claim passes.
9. Evidence-chain verification.
10. Two back-to-back clean runs, byte-identical.

BUDGET on 4 CPUs:
- C03 to n = 12 on both lattices: about 2 minutes in Python. A_c(n) through n = 5: at most 4705470 sets per class if the inequality holds, minutes.
- About 40 C_0 reads x 321 theta values in exact rationals: an estimated 20-40 minutes, split across row groups. The scratch recompute scanned the whole theta grid at six couplings in about 100 seconds at 256 bits. The C04 guard adds 2 pole tests. X3's Newton reads cost tens of S evaluations each.
- c_fin, integrals (C10c adds 11 configurations x 6 moments x 2 one-link integrals) and the W lane: minutes.
- The whole run is under 1 hour wall-clock, with memory under 2 GB and disk under 100 MB.

FAILURE HANDLING: any NOT_MET, UNDECIDED or UNSUPPORTED read stays in the receipt and the note. A fallback, a grid change or a repair is filed only as appended rows after line 41.
```

## 13. Pre-freeze disclosure

Every number of the prediction file was fixed by scratch scripts before this freeze. None is an engine, and none is evidence. They sit in an ephemeral scratchpad, so the freeze commit carries them and three sha256 manifests under `reviews/ym4-04c-prediction/`: the design-lane tree as `ym4-04c/` and the package tree as `ym4c/`.

| Manifest | lines | covers | sha256 |
|---|---|---|---|
| `MANIFEST-ym4-04c-scratch.sha256` | 67 | every file of the design-lane tree `ym4-04c/`, except bytecode caches | `0013abbb52fcc1dce351613afac5058ea07acb27a778db6856b439826df52873` |
| `MANIFEST-ym4c-v2-checks.sha256` | 19 | every file of `ym4c/pkg/v2-checks/` | `e1ace0fa52a8a529c02ca99ff00bf54f3047094469664e3cdbb629c7eb320a94` |
| `MANIFEST-ym4c-pkg.sha256` | 116 | every file of `ym4c/`, except bytecode caches, the three manifests, the packaging directory `pkg/assemble/` and the deliverables of this commit (the prediction file, this note, `derive_checks.py`, `DERIVE-CHECKS.hbp`, `ledger_rows-final.txt`, `engine_plan-final.txt`) | `9a906d15bd33f36fd0fec2776d89608ac2c7755bd01306b3d4d45a4a2c98647c` |

All three verify against their trees with `sha256sum -c` as of this note. The design-lane tree is unchanged since the v2 repair, so its manifest is the one v2 cited.

**The lanes, by directory.**

- Design lanes, under `ym4-04c/`: `polymer-norm/`, `smallfield-largefield/`, `coupling-trajectory/`.
- Judges: `judge-engineer/` (with `n12.txt`), `referee/`, `judge-cft/`.
- Synthesis: `synth/`, with its `.txt` outputs and the 40-line draft.
- The final critic: `final-check/`, in Decimal at 50 and 90 digits, except `wlane.py` (floats) and `fault_dl.py` (Fractions).
- The v2 repair: `ym4c/pkg/v2-checks/`, in Fractions with 160-bit outward rounding.
- The two derivation routes of G0 and G1: `ym4c/pkg/derive/` (`G0-a`, `G0-b`, `G1-a`, `G1-b`, with `g1a/` and `g1b/`).
- The six second-seat lenses: `ym4c/pkg/attack/` (with `g1st/` and `g1tg/`).
- The canonical sections and their reads: `ym4c/pkg/repair/`.
- The final recompute: `ym4c/pkg/recompute/final_s_lane.py` and `c09_neighbours.py`, in Fractions with 256-bit outward rounding. They recompute every value that depends on the factor 6, on λ(δ) ≤ κ or on c_fin, scan the whole θ grid at the six C09 couplings, and read the C09 index gaps against the engine's dyadic resolution.
- The freeze checks: `derive_checks.py` (section 14).

**Floats.** Floats enter arithmetic only in these places. Numpy sanity runs: `coupling-trajectory/d4_direct_float_sanity.py`, `judge-engineer/slf_ct_sanity.py`, `synth/r12_float_sanity.py`. Float ε_6 spot checks: `judge-cft/spot.py`, `eps6_exact.py`. Float alias sums: `referee/check_sl_ct.py`, `final-check/wlane.py`. A float only to choose a scan length or a rounding grid, then certified exactly: `polymer-norm/contraction.py`, `coupling-trajectory/d9_window.py`, `ym4c/pkg/derive/g1a/g1a_constants.py`. Machin's Gaussian-integer identity in Python complex numbers, exact for these integers: `ym4c/pkg/repair/G0-repair-checks.py`; `derive_checks.py` redoes it in integer pairs. Everywhere else floats appear in display only.

**Cross-reads.** C03's counts were read by the judge prototype `judge-engineer/closed_sets.py` through n = 12, rerun through n = 10 on both lattices by `synth/closed_sets_copy.py`, and through n = 10 on fine (ℤ/8)⁴ and (ℤ/10)⁴ by `ym4c/pkg/attack/G0-count-checks.py`. C01's census was read by `polymer-norm/geometry_check.py`, the judge prototype and the counting lens. W06(b) was read by exact inertia. W04 was read by float runs. These are reproduction reads, not blind predictions.

**The prefreeze field.** Every row carries one. Only prefreeze=NONE values can count as confirmed predictions. They are row C18 and the clauses: C01's A_c(n) count, C09's cluster-exclusion read, C10's holonomy reads, C10c's moment reads, C19's engine exits, W06(a) and W07's random tiles. C10b's moment identity is COMPUTED, since `derive_checks.py` reads it at one rational configuration.

**Recomputed in this package.** C07, C08, C09, C10b, C10c, C11, C12, C13, C14, C16, C17 and C19, and the hypothesis, certificates, theorems, scope, G_attack, ledger and summary rows. Each recomputed value carries prefreeze=COMPUTED with `pkg/recompute/final_s_lane.py` named.

**Corrections.** Against the design lanes: C08's head-free value, C12's value, the C13 and C14 edges under the δ_crit test, and the C09 grid (all from v2). Against the draft, from v2: W03's increment bracket; the regime boundary; C15's scope; C19's three pinned faults. Against v2, from the proofs: δ_1 and T halve; C_k becomes λ(δ) ≤ κ and the factor becomes c_fin; C11's C_1 and crude self-map become MET; C12's every-count-model NOT_MET clauses are withdrawn; the regime boundary moves to β_0 ≤ 0.02074 and the crude boundary to 0.01767; C19's planted claim "the head-free self-map MET at 1/50" became true and is replaced by "C_0 head-free MET at 0.02076"; the C09 resolution is lost between 1/700 and 1/600; C03's "> 2000" holds only from n = 8; C09's exclusion and C10's floor for every representation are DERIVED. Two field keys of the draft held "=" and are renamed `k_at_least_1`. Since λ now names λ(δ), W02's direction index and W06's eigenvalue variable are renamed ρ and y.

## 14. The checks of this commit

[`derive_checks.py`](../reviews/ym4-04c-prediction/derive_checks.py) uses integers and `fractions.Fraction` only. It holds no float literal, no true-division operator and no negative power, and it checks that of its own source before it runs; a planted `1.5 / 2` makes that check fail. It writes [`DERIVE-CHECKS.hbp`](../reviews/ym4-04c-prediction/DERIVE-CHECKS.hbp) on stdout, run as `python3 -I -B derive_checks.py`: 54 checks, 0 failed, under 1 second. MEASURED:

- **Fuss–Catalan.** F_20(4..12) and 6F_20(1..5) as exact binomials, F_20(2) = 20 against F_19(2) = 19, the product formula of Lemma 3.11 with strict increase below μ for n ≤ 59, μ ∈ [53.00068, 53.00069], F_20(10)/F_20(8) and F_20(12)/F_20(10), and the C03 counting-gap arithmetic.
- **The aligned tile.** The 12 links of a fine 2 × 2 tile as rational unit quaternions, its 4 plaquettes, its boundary holonomy, and the identity 16 − 40ε + 32ε² − 8ε³ = 8(1 − ε)²(2 − ε) at cos φ = 63/65, 255/257, 1023/1025.
- **The b = 2 and b = 4 alias rationals.** The alias formula as an exact rational function of σ = sin²(q/2): the W01 profile, r_2(π), A_1 and A_2 both from their lattice-sum definition and as the limit σ → 0; the W03 profile, corners and slopes; the d = 2 closure.
- **The b = 8 slopes.** A_3 = A(8, 4) and A(8, 3) in ℚ(√2), where the √2 parts cancel; the d = 3 increments; A_k/2^k.
- **W05.** The transverse corner 15/28 in three covariant gauges and the longitudinal ratios 3675/7372, 35/48, 11025/10456.
- **The Catalan moment identity at one rational V.** A = (1, 2, 2, 4)/5 and B = (2, 1, 0, 2)/3, χ_{1/2}(V) = −16/15. E_π[(χ_b + χ_t)^{2m}] = Cat_m(2 + χ)^m for m ≤ 6 and the odd moments 0, by exact monomial integration over the unit 3-sphere. The sphere moments are checked against Lemma 3.2 item 2.
- **Constants.** Machin's identity in integer pairs, π > 333/106 > 80000/25467, 8/(3π) < 848/999 < 8489/10000, and 1/(8N_p) on 8⁴, 12⁴ and 16⁴.

The output, byte for byte:

```text
YM4_04C_CHECKS_START|file=reviews/ym4-04c-prediction/derive_checks.py|rows=docs/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp|integers_and_fractions_only=1|json=0
YM4_04C_DC_NO_FLOAT|float_literals=0|true_division_ops=0|negative_powers=0|float_names=0|tag=MEASURED|json=0
YM4_04C_DC_FUSS_CATALAN|F_20(4..12)=20540,784245,31763004,1340246340,58281448940,2593593086150,117544525178080,5406686759963586,251754316822792420|6F_20(1..5)=6,120,3540,123240,4705470|F_20(2)=20|F_19(2)=19|mu_in_[53.00068,53.00069]=1|ratio=20*prod_j(20n+j)/(19n+j+1),increasing,below_mu_n=0..59|F(10)/F(8)=2016.8428|F(12)/F(10)=2141.7783|F(n+2)/F(n)>2000_from_n=8|tag=MEASURED|json=0
YM4_04C_DC_COUNTING_GAP|6F(8)/N(8)=43711086705/4|6F(10)/N(10)=44079196941780/19|6F(12)/N(12)=755262950468377260/1163|N(10)/N(8)=19/2|N(12)/N(10)=1163/152|sqrt_brackets=[3.08,3.09],[2.76,2.77]|counts=C03,CONJECTURE|tag=MEASURED_arithmetic_of_a_CONJECTURE|json=0
YM4_04C_DC_ALIGNED_TILE|cos=63/65:ratio=4064256/274625;cos=255/257:ratio=266342400/16974593;cos=1023/1025:ratio=17146331136/1076890625|each_equal_to_16-40e+32e^2-8e^3=8(1-e)^2(2-e)_at_e=1-cos|each_below_16|1-a(V')<=4sum(1-a(U_p))|tag=MEASURED|json=0
YM4_04C_DC_ALIAS_B2_B4|W01_r_1(t_W=1/16,1/8,1/4,1/2,1;q=pi)=12689633/12736932,813281/825252,56033/59172,4961/5892,833/1212,15/28|r_2(pi)=25823/98640|A_1=23/96|A_2=1367/1920|2r_1(pi)=15/14|4r_2(pi)=25823/24660|r->1_as_q->0=1|slopes_by_definition_and_by_the_alias_limit_agree=1|tag=MEASURED|json=0
YM4_04C_DC_ALIAS_D3_D2|W03_r_1_d=3=2057/4120,521/1048,137/280,41/88,17/40,3/8|b*r(pi)_b=2,4=3/4,119/208|A(2,3)=3/32|A(4,3)=73/384|d=2:r=1/b^2_at_q=pi/2,2pi/3,pi_and_A=0_at_b=2,4=1|tag=MEASURED|json=0
YM4_04C_DC_B8|A_3=A(8,4)=113360987/66106880|A(8,3)=54335/182784|sqrt2_parts=0,0|increments_d=3=37/384,6529/60928|A_k/2^k=23/192,1367/7680,113360987/528855040|A_3/8<0.2527310=1|tag=MEASURED|json=0
YM4_04C_DC_W05|transverse_corner_xi=1/2,1,3=15/28,15/28,15/28|longitudinal_(xi/4)/C'_nunu_xi=1/2,1,3=3675/7372,35/48,11025/10456|pairwise_unequal=1|tag=MEASURED|json=0
YM4_04C_DC_CATALAN_MOMENTS|A=(1,2,2,4)/5|B=(2,1,0,2)/3|chi_1/2(V)=tr(AB)=-16/15|E_pi[(chi_b+chi_t)^(2m)]_m=0..6=1,14/15,392/225,2744/675,537824/50625,7529536/253125,331299584/3796875|Cat_m(2+chi)^m=1,14/15,392/225,2744/675,537824/50625,7529536/253125,331299584/3796875|odd_moments_m<=11=0|route=exact_monomial_integration_on_S^3|tag=MEASURED|json=0
YM4_04C_DC_CONSTANTS|(5+i)^4(239-i)=114244(1+i)|pi>=1231847548/392109375>333/106>80000/25467|8/(3pi)<848/999<8489/10000|1/(8N_p)=1/196608(8^4),1/995328(12^4),1/3145728(16^4)|8N_p>100_iff_N_p>=13|tag=MEASURED|json=0
YM4_04C_CHECKS_END|checks=54|failed=0|tag=MEASURED|json=0
```

## 15. The evidence chain and the pin

In `reviews/ym4-04c-prediction/`, the freeze commit adds `INDEX.hbi`, one row per artifact with its bytes, sha256 and 16-hex SH; `RECORDS.hbp`, what each artifact is and how it was made; `SHA256SUMS` over the folder's files; and `SEAL.hbp`, the sha256 of `SHA256SUMS` and of `INDEX.hbi` and of the two concatenated. They follow YM4-03C §11.

**The pin.** The 41 rows of the prediction file hash to `f77c51568fdf9eaec81010d7f6cff12811ac2da65be56cd7cd3a74e37518ad61` by

```text
head -n 41 docs/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp | sha256sum
```

The 41 lines are every row of the file, the summary row included, so the pin covers the whole file as written. The workflow holds the pin. Later rows, attempts, fallbacks (such as a smaller n_max) and corrections go after line 41, so every earlier row stays a byte prefix.

## 16. The pre-freeze attack, and the gate it leaves open

**What was attacked.** Before the repair, two routes derived each theorem (`ym4c/pkg/derive/`). Three second-seat lenses attacked each theorem and filed a report with exact scratch reads (`ym4c/pkg/attack/`). The repair lane merged the routes into the canonical sections 3 and 4 and resolved every finding (sections 3.16 and 4.18).

| Theorem | Lens | File | Verdict | Blocking findings, and their resolution |
|---|---|---|---|---|
| G0 | Kotecký–Preiss | `attack/G0-kp.md` | GAP | B1: δ_1 and T carry 6, not 12; B2: the corollary's weight is e^{d(X)}. Both adopted (Propositions 3.24, 3.28, Remark 3.19). |
| G0 | polymers and counting | `attack/G0-count.md` | GAP | B1, carried. Lemmas 3.13 and 3.14 (locality, the class rule) supplied by this lens and adopted. |
| G0 | assembly and constants | `attack/G0-assembly.md` | GAP | B1, confirmed from the assembly side; the SCOPE reading of C11 and C12 corrected. |
| G1 | the expansion machinery | `attack/G1-treegraph.md` | GAP | F1: d(γ) = θ#γ undefined at step k, fixed by #γ := ½#line(supp γ); F2: the proved constants are not the draft's, resolved by using λ ≤ κ and c_fin. |
| G1 | the line and object channels | `attack/G1-channel.md` | HOLDS | Seven minor findings; the slice lower bound, adopted as Lemma 4.23 and Corollary 4.24. |
| G1 | the structural hypotheses | `attack/G1-structure.md` | HOLDS | Eight minor findings; β_k defined as a projection (Lemma 4.22), "measurable" added, c_fin nondecreasing. |

No attack finding was wrong. Two claims of the routes were withdrawn: route A's "bipartite, since L is even" and route B's "C04 is wrong at equality".

**The gate stays OPEN.** The lenses read the routes, not the canonical sections as written. Gate G_attack needs a second seat of the owner's choosing to attack the final sections 3 and 4 and file the attack. Until then every row that rests on G0 or G1 reads CONDITIONAL, and no engine code is written. An unrepaired gap, or a proved constant that differs from the one in the prediction file, makes every row and clause that rests on it read UNSUPPORTED, whatever its arithmetic. A repair or a corrected constant is filed as appended rows after line 41.

**The brief.** The second seat should answer these questions.

1. Does Proposition 3.18 give the cluster bounds used in (C2) and (C3) from (KP_w), with the weight e^{d(X)} on the left?
2. Does the test set W′(ℓ), with #W′(ℓ) = 6, control the cluster sums of every Y through ℓ, and is 6 the least constant for this argument (Lemma 3.23)?
3. Are #Y″(γ) ≤ #γ, V-dependence only at size ≥ 4, and the readout exclusion for clusters right (Lemmas 3.21, 3.26, Corollary 3.27)?
4. Do the locality and class rule of Lemma 3.14 hold for n ≤ 2N − 1, and does Lemma 3.32 give monotonicity in β_0?
5. Is the line-channel factor right, #Y″ ≤ #Y/2 with #Y ≥ 8 for every line-supported Y (Lemmas 4.1, 4.5)?
6. Does the tree-graph bound hold in the (1 + t)^f form at off links (Lemma 4.12), and does it give Lemma 4.13 item 1 under λ(δ) ≤ κ alone?
7. Is the root-object bookkeeping right, with roots that hold a line link (m ≥ 1), the e^{δ} prefactor on the object channel only, and the closed form of Lemma 4.16?
8. Are the sup norms after integration finite and the outputs gauge invariant, and does carrying the Wilson term inside R_k break any step (sections 4.8, 4.13)?
9. Is the slice bound of Lemma 4.23 right, so that C10's floor holds for every representation?
10. Are the proved constants exactly the ones in the prediction file: the scalar inequality, δ_1 = 6α e^{−4(θ−κ)}, T = (8489/10000)·6α e^{−8θ}, λ(δ) ≤ κ and c_fin(δ)?

**CONDITIONAL rows, listed.** On G0 and G1: C07, C08, C11, C12, C13, C14, C16, the replacement clause of C17, the regime clause of the hypothesis row, and C19's `delta_crit_surrogate` edge. On G0: the injection clause of C01, C09, and C19's `readout_grid_128` value. On G1: the c_fin(δ_in) and per-root comparisons of C10b and C10c, and C13's δ_crit and c_fin values. On the unread (1 + t)^f step (TG), each with its fallback: δ_crit (fallback [0.111780108, 0.111780109]), C13's c_fin values above 0.078733761 and its crude edge (fallback 0.01761/0.01762), the scope row's crude window, and the upper end of C19's surrogate range (fallback 0.01553–0.01761). CONJECTURE on C03, in addition: C08, C09's T/P_10 values, C12's and C14's refined clauses, and the regime value 0.02074.

## 17. Deferred to a separate diagnostic freeze (proposed YM4-04D)

- R03 with R05: a large-field bound from a REPORTED chessboard estimate with mixed reflections. It was tested only in 2D.
- R06 to R08: one-link atoms in a frozen environment.
- CT03 and CT04: scheme dependence. CT04 only with a built β¹² three-polymer engine, and with no NOT_RUN escape in a frozen row.
- R13: the 2D full step.

These are diagnostics. None of them bears on a row of this freeze.

## 18. OPEN

- Gate G_attack: the second-seat attack of the final sections 3 and 4, of the owner's choosing, G1's (1 + t)^f step and m ≥ 1 roots included.
- The freeze commit itself, an owner decision.
- The C03 counts, a CONJECTURE until the engine and the check read them.
- At β_0 = 1/45, a head with n_max > 10.
- A growth bound for Lemma-B-closed sets below μ (L14).
- An averaging map for SU(2) with covariance, positivity and reflection positivity (L17).
- Nonlinear small-field bounds at weak coupling, and a renormalized large-field bound from ρ_{k+1}'s own action (L21).
- A weak-coupling H_k that carries the Wilson term outside the polymer norm, moves the marginal part of order 1/β_k into β_{k+1}, and bounds the rest by stated constants (L22).
- The effective-coupling recursion, with Δ_β = (11/(3π²))ln 2 per halving, and uniformity over infinitely many weak-coupling steps (L24).
- The crossover from β_0 near 0.02 to the scaling region (L26). Relevant counterterms (L27).
- W06's whole-zone covering certificate (L19).
- The infrared limit, OS reconstruction (YM4-05), the mass gap (YM4-06), other gauge groups (YM4-07) and the independent audit (YM4-08) (L28).
