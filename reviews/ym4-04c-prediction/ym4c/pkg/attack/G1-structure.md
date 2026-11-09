# G1 second-seat attack: the structural hypotheses

**Status.** Written by a second-seat referee for YM4-04C on November 9, 2026, from main `830fd3f`, before any engine code. Targets: `pkg/derive/G1-a.md` (route A) and `pkg/derive/G1-b.md` (route B). Frozen text checked: the 40-line draft `ym4-04c/synth/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp`, its repair `pkg/PREDICTION-v2.hbp`, and the attack brief in `pkg/note_outline-v2.txt` section 16. Repo notes read: NOTE-YM4-03 (Lemma 3, Theorem 4, Proposition 2) and NOTE-YM4-03C (§2 Lemma A, §5, §6 Lemma B, §12 OPEN). Nothing in the repo was modified. No engine ran. Every number below is an exact rational enclosure with outward dyadic rounding at 2⁻²²⁰, from the scratch scripts of section 6. Floats are for display only. Tags: DERIVED, CONJECTURE, OPEN, REPORTED, as in NOTE-YM4-03C.

Symbols, as in the renames. a(g) = ½ Re Tr g. b = 2 is the blocking factor. κ = 1/4 is the norm weight. The Kotecký–Preiss pair is (α, θ). δ′ = δe^δ. "Fine" means scale k and "coarse" means scale k + 1. e_0(ℓ) and e_1(ℓ) are the two positions of a coarse link ℓ, and m_ℓ is its midpoint. For an object o, f := #off(o) and m := #line(o). Route A's proved constant is c*, route B's are c_♯ ≤ c_B, and the frozen one is c.

Lens: the structural hypotheses of H_k and whether G1 reproduces them at k + 1. Are the sup norms after integration finite? Does V-dependence stay at coarse size ≥ 4? Is the closed-loop condition kept? Are reality and coarse-gauge invariance kept? Does carrying the Wilson term (β_k/2)χ½(V_P) inside R_k(∂P) break any step, now that Lemma B is lost? Is c nondecreasing, so that the self-map propagates? Is everything uniform in N and K? These are brief questions (v) and (vi), plus the self-map and uniformity clauses.

## 0. Verdict

**HOLDS in this lens.** I tried to refute each structural claim. Every one survives, by my own argument (section 2), in both routes. G1 never uses Lemma B, so carrying the Wilson term inside R_k costs no step. Both constant tables reproduce in my own enclosures at every row point (section 4).

I found nothing blocking in this lens. There are eight minor findings, S1 to S8. One of them, S3, strengthens the package. It shows that C10's floor e^{−4κ} holds for every representation of the output, not only for the one G1 builds. The same argument raises the power of C10b by a factor of about 10 and of C10c by a factor of about 1.7.

The verdict is scoped to this lens. The tree-graph lane (`attack/G1-treegraph.md`) has two blocking findings in other lenses. F1 is the reading of d(γ) = θ#γ at step k. F2 is the "exactly the frozen constants" rule. I do not repeat them. My read on F2 is in section 5.

## 1. What was attacked

1. The pushforward in the line gauge, for a general gauge-invariant density at scale k. Route A Lemma 4.2; route B Lemma 4.1.
2. Lemma A for any integrand invariant at m_ℓ, and the both-positions support rule. Route A Lemma 4.3; route B Lemma 4.2 and its Corollary.
3. Forests and girth on the coarse torus. Route A Lemmas 4.1(4) and 4.4; route B Lemma 4.3 and "the girth".
4. The exact line channel. Route A Lemma 4.5; route B Lemma 4.5.
5. Finiteness, reality, invariance and support of every output term. Route A Proposition 4.14; route B (4.2).
6. The Wilson term inside R_k, with Lemma B lost. Route A §4.12; route B §4.12.
7. Monotonicity and the self-map. Route A Lemma 4.19 and Corollary 4.20; route B Corollary 4.11.
8. Uniformity in N, K and N_p. Route A (C3) and §4.1; route B §4.10 and §4.11.
9. The constant tables. Route A §§4.14–4.15; route B §§4.13–4.14.

## 2. What I confirm, with my own argument

### 2.1 The geometry used at scale k (DERIVED)

A link (y, μ) is a line link iff every coordinate of y other than μ is even. Write O for the set of odd coordinates of x. In a plaquette (x; μ, ν), the link (x, μ) is a line link iff O ⊆ {μ}, and (x + ν, μ) iff O Δ {ν} ⊆ {μ}. The two cannot both hold. The same is true for the two ν-links. So a plaquette holds at most 2 line links. Running through O = ∅, {μ}, {ν}, {μ, ν} gives exactly 2. Any other O gives 0. So every plaquette holds 0 or 2 line links. The Wilson objects therefore have (f, m) = (2, 2) or (4, 0), as route A states.

A midpoint m_ℓ has one odd coordinate, μ. Its two μ-links are e_0(ℓ) and e_1(ℓ), and its other 6 links are off links. A coarse site 2x′ has no odd coordinate, so all 8 of its links are line links. Each midpoint lies on exactly one coarse link, so the extension g̃ of a coarse gauge transformation, with g̃(m_ℓ) := g(x′), is well defined.

Sanity read (`g1st_geometry.py`) on fine (ℤ/8)⁴ with coarse (ℤ/4)⁴. The 2048 line links are the disjoint positions of the 1024 coarse links. Plaquettes split as 18432 with 0 line links and 6144 with 2. All 1024 midpoints have 2 line links and 6 off links. All 256 coarse sites have 8 line links. No coarse cycle of length 1, 2 or 3 exists. The fine side M = 2^{K−k}L_K is even and at least 8 for every k ≤ K − 1. The coarse side M/2 is at least L_K ≥ 4.

### 2.2 Sup norms after integration are finite (question v)

The input gives sup_U |R_k(Y; U)| ≤ δe^{−κ#Y} ≤ δ for every Y. So |e^{R_k(o)} − 1| ≤ δe^{δ} pointwise. Haar measure is a probability measure. So |z_Γ(V)| ≤ ∏_{o∈Γ} sup|f_o| for every V, with no Hölder or Finner step. Each cluster term obeys sup_V |Φ(X; V)| ≤ |φ(X)| ∏ ω(Γ)^{m_X(Γ)}. The Kotecký–Preiss sum of these majorants is finite and independent of V (route A Theorem 4.9, REPORTED; route B Lemma 4.9a). So each R_{k+1}(Y) is a uniformly convergent sum of bounded measurable functions. It is bounded and measurable, with sup_V |R_{k+1}(Y)| no larger than the sum of the sups. The lattice is finite, so the output norm is a finite sum over a finite set at each coarse link. **Confirmed (both routes).**

Pointwise, not almost everywhere. The pushforward formula ρ_{k+1}(V) = ∫ ρ_k((1, V), off) d off defines ρ_{k+1} at every V. Sections of a jointly measurable function are measurable. The gauge step uses invariance pointwise. So "for every V" in H_{k+1} is meaningful, and the next step can use it. **Confirmed.**

### 2.3 V-dependence only at coarse size ≥ 4 (question v)

*Both positions.* Let F be bounded, measurable and invariant at m_ℓ, and let T(V) := ∫F d off with every line at (1, V). The gauge transformation at m_ℓ by h sends e_0(ℓ) from 1 to h⁻¹ and e_1(ℓ) from V_ℓ to hV_ℓ. It multiplies the 6 off links at m_ℓ by a fixed element on one side, which Haar measure absorbs. If F does not see e_0(ℓ), then T(V) = T(V with V_ℓ → hV_ℓ) for every h and every V. If F does not see e_1(ℓ), then V_ℓ never enters. YM4-03C §2's proof of Lemma A uses only invariance at m_ℓ, never the plaquette-product form. So the extension to a general invariant F is the same proof. For each ℓ ∉ Y″(supp Γ), replace V_ℓ by 1 one link at a time. This shows that z_Γ is a function of V restricted to Y″(supp Γ). Each cluster term is a product of separate integrals, so it depends only on Y(X) = ∪_Γ Y″(Γ). **Confirmed.**

*Forests and girth.* Gauge-fix a coarse forest to 1 from a root. So a coarse-invariant function of V on a loop-free set is constant. On (ℤ/L)⁴ with L ≥ 4, a cycle of length 3 would need three signed unit steps that sum to 0 in ℤ⁴, which is impossible by parity. A 2-cycle needs a double link, and there is none for L ≥ 3. A winding cycle has net displacement ±L in some coordinate, so it has at least L ≥ 4 links. So every set holding a closed loop has at least 4 links. **Confirmed.**

*Line channel.* For a line-supported Y′, R^L(Y′) is a function of V on Y″(Y′), with no integral. A loop needs #Y″ ≥ 4, so #Y′ ≥ 2#Y″ ≥ 8, and e^{κ#Y″} ≤ e^{κ#Y′}e^{−κ#Y′/2} ≤ e^{κ#Y′}e^{−4κ}. A V-dependent single object with an off link holds at least 8 line links, so in route B it has n ≥ 9. **Confirmed.**

### 2.4 The closed loop is kept

Route A's Proposition 4.14 and route B's (4.2) assign a cluster X to R_{k+1}(Y(X)) only when Y(X) holds a closed loop. Every other cluster term is constant by 2.3 and goes into const_{k+1}. That constant is an absolutely convergent sum of V-independent terms. The output Y may be disconnected, which H_{k+1} allows. The tree-graph lane notes the same. G1 never uses that an input Y holds a loop or that #Y ≥ 4; it only reproduces these conditions. **Confirmed.**

### 2.5 Reality and coarse-gauge invariance are kept

f_o = e^{R_k(o)} − 1 is real. z_Γ is real, φ(X) is an integer combination, and Φ(X; V) is real. log Ξ(V) is real and equals the cluster sum, by route A's s-argument or route B's λ-argument. Both use Ξ(V) > 0, the integral of a positive function.

For a coarse gauge transformation g, take g̃ = g at the coarse sites, g̃(m_ℓ) = g(x′) for ℓ = (x′, μ), and g̃ = 1 elsewhere. Then e_0(ℓ) goes from 1 to g(x′)g(x′)⁻¹ = 1, and e_1(ℓ) goes from V_ℓ to g(x′)V_ℓ g(x′ + e_μ)⁻¹. On the off links g̃ acts by fixed left and right translations. So z_Γ(V^g) = z_Γ(V). This differs from the extension in YM4-03 Theorem 4 item 3, which sets g̃ = 1 at the midpoints. Route A's and route B's choice is the one that keeps the line gauge (1, ·). Both choices are valid. **Confirmed (both routes).**

*The line gauge is computational.* With lines at (V_ℓ, 1) in place of (1, V_ℓ), the gauge transformation at m_ℓ by h = V_ℓ maps one to the other and moves only off links at m_ℓ. So every z_Γ, every Φ(X) and every R_{k+1}(Y) is the same in the two gauges. C18 tests this. **Confirmed.**

### 2.6 The Wilson term inside R_k, and Lemma B lost (question vi)

At scale k the Wilson term is part of R_k(∂p) with #∂p = 4, and it holds a loop. Every plaquette holds 2 or 4 off links (2.1). So every Wilson object is in the polymer gas and never in the line channel.

Which steps could use Lemma B or closure? Only bounds that count closed polymers: G0's #off(γ) ≤ 2#γ and its Fuss–Catalan count. Neither route uses either at k ≥ 1. Route A's a(Γ) = δ′Σ_{o∈Γ}#off(o) counts every off link of every object. Route B's a(Γ) = α#off(Γ) does the same. Both tree bounds run on the norm alone, with Σ_{o∋e} ω_o e^{κ#o} ≤ δ′. Unclosed polymers, such as the single Wilson plaquette with activity c_0(β_k) − 1 > 0, are counted at their sup norm. So losing Lemma B changes no step and no constant. **Confirmed (both routes).**

The cost is real but first order. Route A's per-unit factors for the Wilson objects at C07's δ_1 ≤ 0.011045 are q(2, 2) = e^{−3κ}(e^{4δ′} − 1) ∈ [0.0215793, 0.0215794] and q(4, 0) = e^{−4κ}(e^{8δ′} − 1) ∈ [0.0343797, 0.0343798]. Both lie below route A's stated caps 0.0217 and 0.0345, and far below e^{−1}. Route B's "multi-object share" c_B − e^{−1} over C08's bracket is [5.89174e-5, 5.91052e-5] (see S6 for its lower end). Route A's Lemma 4.22 constant (16/(3π))e^{−1} reads 0.62453154 < 0.62454. **Confirmed.**

### 2.7 Monotonicity, so the self-map propagates

For fixed n, e^{−(κ/2−2δ′)n} − e^{−κn/2} increases with δ′, and δ′ = δe^δ increases with δ. A supremum of nondecreasing functions is nondecreasing. So the bracket of c is nondecreasing and positive. With e^δ strictly increasing, c is strictly increasing on C_k. Route A's c* and route B's c_♯ are maxima of nondecreasing entries, so they are nondecreasing. Both are constant at e^{−1} on an initial interval (S4).

Induction step: if H_j(κ, δ_j) holds with δ_j ≤ δ_k, then δ_j meets the condition, which is downward closed. G1 gives H_{j+1}(κ, c(δ_j)δ_j), with c(δ_j)δ_j ≤ c(δ_k)δ_j ≤ c(δ_k)^{j−k+1}δ_k. H is monotone in its second argument. Since c is increasing, {δ : C_k MET and c(δ) < 1} is an initial interval, so the admissibility test "δ_1 < δ_crit⁻" is meaningful. **Confirmed (both routes).**

### 2.8 Uniform in N and K

Every bound in G1 is local. It uses the norm budget at one fine link (e_0(ℓ), or one off link e), the geometry of 2.1, and the coarse girth. None of these depends on N, K or N_p. The only size conditions are fine side ≥ 8 and coarse side ≥ 4 at every scale. Both follow from L_K ≥ 4, for every 1 ≤ k ≤ K − 1. Kotecký–Preiss runs on a finite polymer set at each scale. **Confirmed (both routes).** One readout outside G1 is extensive in the volume (S8).

## 3. Findings

### S1 (minor, definitional). The Wilson-term clause of H_k is not reproduced literally at k + 1, and β_k is defined nowhere

The HYPOTHESIS row, in both the draft and v2, says: "the coarse Wilson term (β_k/2)χ½(V_P) is carried inside R_k(boundary of P)". No row defines β_k at k ≥ 1.

G1's output does not place the χ½(V_P) dependence in R_{k+1}(∂P) alone. Take two incompatible polymers Γ_1 and Γ_2 with Y″(Γ_1) = ∂P and Y″(Γ_2) = ∂Q. The cluster {Γ_1, Γ_2} contributes −z_1(V_P)z_2(V_Q) to R_{k+1}(∂P ∪ ∂Q). Its χ½(V_P) projection is −⟨χ½, z_1⟩·∫z_2 dV. That is nonzero unless ∫z_2 = 0. So, for a generic input, some χ½(V_P) dependence lands in an R_{k+1}(Y) with Y ⊋ ∂P.

Route A notices this and rewords its conclusion (C1): the Wilson term "lies inside the R_{k+1}(Y) with Y ⊇ ∂P". Route A's Lemma 4.22 defines β_m := 2c_½(P), the χ½(V_P) projection of log ρ_m. Route B's table checks only the input side ("carried as R_k(∂P) … equal"). Read as a constraint, "all of c_½(P) sits in R_{k+1}(∂P)" would need a re-decomposition. That moves each projection c_Yχ½(V_P) out of R(Y). It can raise sup|R(Y)| by up to 2|c_Y| ≤ (16/(3π))sup|R(Y)|, and it adds e^{4κ}·2|c_Y| at ∂P. G1 does not prove that this fits inside c(δ). Read as a placement rule, "no Wilson term is kept outside Σ_Y R_k(Y)", the clause constrains nothing and is reproduced. No constant depends on the choice.

*Fix.* Replace the clause with: "no Wilson term is kept outside Σ_Y R_k(Y); β_k := 2c_½(P), the χ½(V_P) projection of log ρ_k, which every R_k(Y) with Y ⊇ ∂P may carry (route A Lemma 4.22)". C08's v2 comparison already uses this reading.

### S2 (minor). The frozen H_k omits "measurable"

Every step integrates R_k(Y) over Haar measure. The frozen row says "real, coarse-gauge invariant and a function of V restricted to Y", and boundedness follows from the norm. Measurability is never stated. Route A adds "bounded and measurable" in (H2), and its table says "with bounded and measurable added". Route B uses both properties silently. The output is measurable (2.2), so the induction closes once the row says it.

*Fix.* Add "bounded, measurable" to the H_k clause.

The row also says "coarse-gauge invariant" for invariance under scale-k gauge transformations, while both routes call scale k "fine". *Fix:* write "invariant under every gauge transformation of Λ_k".

### S3 (minor, a strengthening). C10's floor e^{−4κ} holds for every representation, and the "every decomposition" bounds of C10b and C10c are the natural norms

Route A, after Proposition 4.23 and in its gap 3, says that a different representation of log ρ_{k+1} could have a smaller norm, so that its optimality holds only for the representation it builds. Route B §4.10 says "By C10, no valid step bound on this class has c below e^{−4κ}". That is stated, not proved. C10's frozen statement says "every valid step bound on this class has c(δ) ≥ e^{−4κ}". H_{k+1} is an existence statement, so these claims need a lower bound over all representations. Here is one.

**Lemma S3 (DERIVED here).** Let the coarse torus have side ≥ 4. Suppose log ρ(V) = C + Σ_P f_P(V_P), with each f_P a continuous class function. Write osc(f) := max f − min f. Let {R(Y)} be any family of bounded measurable functions, each a function of V restricted to Y, with log ρ = C′ + Σ_Y R(Y). Gauge invariance and the loop condition are not needed. Then for every coarse link ℓ, at κ = 1/4,

```text
sum_{Y containing l} e^{kappa #Y} sup|R(Y)|  >=  e^{4 kappa} sum_{P containing l} osc(f_P)/2.
```

*Proof.* Fix P ∋ ℓ. Let ψ be a bounded class function on SU(2) with Haar mean 0 and ∫|ψ| = 1. Then:

1. ∫ψ(V_P)·C dV = 0.
2. For Q ≠ P, take a link ℓ′ ∈ ∂Q ∖ ∂P; it exists because two plaquettes share at most one link. Integrate V_{ℓ′} first. f_Q(V_Q) averages to the constant ∫f_Q, so ∫ψ(V_P)f_Q(V_Q) dV = 0.
3. V_P is Haar distributed, so ∫ψ(V_P)f_P(V_P) dV = ⟨ψ, f_P⟩.
4. If ∂P ⊄ Y, take ℓ″ ∈ ∂P ∖ Y and integrate V_{ℓ″} first. ψ(V_P) averages to 0, so ∫ψ(V_P)R(Y) dV = 0.
5. If ∂P ⊆ Y, then |∫ψ(V_P)R(Y) dV| ≤ sup|R(Y)|.

The sum over Y is finite. So ⟨ψ, f_P⟩ ≤ Σ_{Y⊇∂P} sup|R(Y)|. Now take ψ = (1_A/|A| − 1_B/|B|)/2, with A and B small conjugation-invariant neighbourhoods of the maximum and the minimum of f_P. Then ⟨ψ, f_P⟩ tends to osc(f_P)/2.

Sum over the 6 plaquettes through ℓ. This gives Σ_{P∋ℓ} osc(f_P)/2 ≤ Σ_{Y∋ℓ} j(Y) sup|R(Y)|, where j(Y) := #{P ∋ ℓ : ∂P ⊆ Y}. The plaquettes through ℓ share only ℓ, so a Y with j(Y) = j ≥ 1 has #Y ≥ 3j + 1. At κ = 1/4, e^{κ(3j+1)} ≥ j e^{4κ}, that is e^{3(j−1)/4} ≥ j, for j = 1, …, 6. Lower enclosures from `g1st_duality.py`: 1, 2.117000, 4.481689, 9.487736, 20.085537 and 42.521082. ∎

Consequences:

- **C10.** f_P = sχ½ has osc/2 = 2|s|. So every representation of C10's output has norm ≥ 12|s|e^{4κ}, which is the natural norm. For every representation, the ratio is at least e^{−4κ} at κ = 1/4. This closes route A's gap 3 for C10's class, and it proves route B's sentence and C10's statement in the existence sense. Route A's Proposition 4.23 can say "for every representation".
- **The κ = 0 clause of C10** ("in the κ = 0 norm no contraction is possible") is not covered. At κ = 0 the same argument gives only j(Y) ≤ 6, so the ratio is ≥ 1/6 (DERIVED). Ratio ≥ 1 for every representation is OPEN; it is DERIVED only for the constructed representation.
- **Range of κ.** The j = 2 case needs κ ≥ (ln 2)/3 ≈ 0.2310, so the lemma holds at κ = 1/4 but not for every κ > 0. Route A's line "every statement holds for every κ > 0" does not extend to it.
- **C10b and C10c.** Both outputs have the lemma's form, and R(∂P) := f − (max f + min f)/2 attains the bound. So the every-decomposition lower bound equals the natural norm. The two rows' projection bounds with E|χ½| = 8/(3π) are valid but loose.
  - C10b at s = 1/2000: natural δ_out/δ_in ∈ [1.516e-4, 1.517e-4], against the projection bound [4.00e-7, 4.01e-7]/δ_in. The slack against c(δ_in)δ_in drops from [39905.8, 40005.6] to [3922.85, 3925.44] with the frozen c, to [2425.05, 2426.65] with c* and to [3356.18, 3358.40] with c_♯.
  - C10c: the every-decomposition slack drops from v2's [12.08, 12.09] to [7.11635, 7.11723] at s = 1/65536, and from [21.64, 21.69] to [12.7543, 12.7667] at s = 1/8192, with the frozen c. With c* it reads [6.59448, 6.59529] and [6.59166, 6.59811]. With c_♯ it reads [6.59448, 6.59529] and [11.0231, 11.0339].
  - No ratio reaches 1, so neither test refutes c, c*, c_♯ or c_B.

*Fix (optional, raises power at no cost).* In C10, say "for every representation, at κ = 1/4 (Lemma S3)". Keep the κ = 0 clause for the constructed representation only. In C10b and C10c, use the natural norm as the every-decomposition bound in the falsifier, and quote the new slacks. Put Lemma S3 in note section 4.

### S4 (minor). Route B calls c_♯ "increasing"; it is constant on an interval

Route B's Corollary 4.11 says that each of c_♯, c_B and c "is increasing in δ". c_♯ = e^{−1} exactly on (0, 0.0116995481]: the upper enclosure holds there and fails at 0.0116995482. Route A's c* = e^{−1} on (0, 0.072094]. The self-map needs only "nondecreasing", which route A says. The frozen clause "since c is increasing in δ" is correct for the frozen c, which is strictly increasing (2.7).

*Fix.* Route B: write "nondecreasing" for c_♯.

### S5 (minor). "max_{n≥4}" in the frozen c does not exist on the boundary 2δ′ = κ/2 that C_k includes

C_k is "MET iff 2δ′ ≤ κ/2". At 2δ′ = κ/2, the term e^{−(κ/2−2δ′)n} − e^{−κn/2} = 1 − e^{−κn/2} increases to 1 without reaching it. There c = e^δ(e^{−4κ} + 1) > 1, so the self-map fails anyway. The boundary point solves 2δe^δ = 1/8 and is irrational, so it is never on a grid. Route B treats r_* = 0 separately. Route A's Lemma 4.19 uses the strict inequality.

*Fix.* Write "sup_{n≥4}" in the CERTIFICATES row.

### S6 (minor). Four of route B's brackets are rounded to nearest, not outward

Route B states that every value in its §4.13 is an exact enclosure. Four displayed brackets exclude the exact enclosure over their own δ bracket (`g1st_brackets.py`):

| Item (route B) | Shown | Exact over the δ bracket |
|---|---|---|
| C07 c (frozen) | [0.4450430, 0.4450509] | [0.4450429880, 0.4450508181] |
| C07 2δ′ | [0.0223333, 0.0223353] | [0.0223332919, 0.0223353364] |
| C10b, s = 1/2000, 2δ′ | [0.0552458, 0.0552479] | [0.0552457631, 0.0552478728] |
| c_B − e^{−1} over C08 (§4.12) | [5.892e-5, 5.912e-5] | [5.89174535e-5, 5.91051054e-5] |

Route B's own script prints the correct 10-digit values; for example, `g1b_constants.out` reads c_frozen = 0.4450429880. So the error is in transcription. All 14 of route A's displayed brackets that I checked do contain the exact enclosure. No frozen row is affected. Copied into an appended row, such a bracket would read NOT_MET by arithmetic, as in the critic's W03 case.

*Fix.* Route B: round every displayed lower end down and every upper end up.

### S7 (minor). Both tables compare against the 40-line draft, not v2, and neither covers C10c

v2 changes the regime clause to "β_0 ≤ 0.01959 on the 10⁻⁵ grid". Route A's table quotes "β_0 ≤ 0.0196 (edge 0.01959)" and route B's quotes "β_0 ≤ 0.0196". v2 adds C10c, a G1 test whose c(δ_in) comparison G_attack lists under rests_on_G1. Neither table has a C10c row. My reads:

- s = 1/8192: 2δ′ = 0.073975492 ∈ [0.0739754, 0.0739755] and c = 0.71181228 ∈ [0.7118122, 0.7118123], both reproducing v2. c* = e^{−1}, c_♯ = 0.61519796 and c_B = 0.68900609.
- s = 1/65536: 2δ′ = 0.0089626215 ∈ [0.0089626, 0.0089627] and c = 0.39699259 ∈ [0.3969925, 0.3969926]. c* = c_♯ = e^{−1}, and c_B = c, since δ_in < δ_eq.

Route B's sentence on C08, "c_♯ = e^{−1}, which lies below the frozen bracket [0.36793, 0.36795] by about 5.9 × 10⁻⁵", is off. e^{−1} lies 5.06 × 10⁻⁵ below the bracket's lower end; 5.9 × 10⁻⁵ is its distance from c(δ_1).

*Fix.* Re-read both tables against v2, and add the C10c rows above.

### S8 (minor). Wording of the uniformity and self-map clauses

- The HYPOTHESIS uniformity clause says that no bound involves N, K or N_p. Route A's Lemma 4.21 (C16's oscillation readout) is extensive: osc_V log ρ_m ≤ 2·#links·e^{−4κ}δ_m/4. C16 states it on the 4⁴ torus, so it is uniform in K at fixed L_K = 4 only. *Fix:* say that the uniformity clause covers the step bounds, and that C16's readout is per final torus.
- The self_map clause "δ_{k+j} ≤ c(δ_k)^j δ_k for every j and sum_k δ_k ≤ δ_k/(1 − c(δ_k))" uses k both as the summation index and as the base scale, and "every j" means j ≤ K − k. *Fix:* write Σ_{j=k}^{K} δ_j ≤ δ_k/(1 − c(δ_k)) for 0 ≤ j − k ≤ K − k, as route A does.

## 4. The constant tables against the draft

Mine are from `g1st_constants.py`: exact Fractions, with e^x enclosed by Taylor series after halving and outward rounding at 2⁻²²⁰. The maximum over n or f is certified by a tail cap e^{−rate·n} below the best lower value. "pt" is the read at the row's point.

| Item (row) | Frozen | Mine, frozen c | Mine, c* (A) | Mine, c_♯ (B) | Mine, c_B (B) |
|---|---|---|---|---|---|
| e^{−1} | — | 0.367879441171 | | | |
| C07 2δ′ | [0.02233, 0.02234] | [0.0223332919, 0.0223353364] | | | |
| C07 c(δ_1) | [0.44504, 0.44505] | [0.4450429880, 0.4450508181]; pt 0.0110444507: 0.44504652 | e^{−1} | e^{−1} | [0.4447292251, 0.4447369440] |
| C08 c(δ_1) | [0.36793, 0.36795] | [0.3679383586, 0.3679385463] | e^{−1} | e^{−1} | equal to c |
| C10b c, s = 1/2000 | [0.5950, 0.5951] | pt δ_in = 0.0268901344: 0.59509676 | e^{−1} | 0.50913304 | 0.58793346 |
| C10b c, s = 1/4096 | [0.4617, 0.4618] | pt δ_in = 0.0131299484: 0.46174246 | e^{−1} | 0.37929233 | 0.46115809 |
| C10c c, s = 1/8192 (v2) | [0.7118122, 0.7118123] | 0.71181228 | e^{−1} | 0.61519796 | 0.68900609 |
| C10c c, s = 1/65536 (v2) | [0.3969925, 0.3969926] | 0.39699259 | e^{−1} | e^{−1} | equal to c |
| C13 c(49/1000) | [0.98248, 0.98249] | 0.98248848 | e^{−1} | 0.82089790 | 0.88018141 |
| C13 c(1/20) | [1.0110, 1.0111] | 1.0110668 | e^{−1} | 0.83899699 | 0.89674555 |
| C14 c(δ_1), 1/64 | [0.38085, 0.38086] | [0.38085224, 0.38085289] | e^{−1} | e^{−1} | equal to c |
| C11 2δ′; c* | [0.22505, 0.22507] | [0.22505228, 0.22507667] | [0.77171237, 0.77193051] | | |
| C12 2δ′; c* | ≥ 0.15623 | [0.15623742, 0.15623972] | [0.37272624, 0.37273509] | | |
| C16 δ_20; osc_20 | [2.30e-9, 2.31e-9]; ≤ 4.35e-7 | 2.306472e-9; 4.34434e-7 | | | |

Edges, each read on its stated grid:

- C_k, 2δ′ ≤ 1/8: holds at 0.058923670 and fails at 0.058923671.
- 2δ′ ≤ 1/4: holds at 0.111780108 and fails at 0.111780109.
- δ_crit (frozen c): c⁺ < 1 at 0.049617491 and c⁻ ≥ 1 at 0.049617492, inside the frozen [0.0496174, 0.0496175].
- δ_crit* (c*): c*⁺ < 1 at 0.109530694 and c*⁻ ≥ 1 at 0.109530695, with argmax f = 16.
- c* = e^{−1}: the off channel e^δQ ≤ 0.3678710667 < e^{−1} at 0.072094, and ≥ 0.367879837 > e^{−1} at 0.072095, with f = 6.
- δ_crit(c_B): holds at 0.0558087801 and fails at 0.0558087802.
- δ_crit(c_♯): holds at 0.0577661141 and fails at 0.0577661142.
- c_♯ = e^{−1}: holds through 0.0116995481 and fails at 0.0116995482.
- δ_eq: f(8) − f(9) = +9.03e-13 at 0.0070256343 and −3.75e-12 at 0.0070256344.

Every frozen G1 value reproduces at its row's point. Every edge and threshold quoted by either route reproduces on its grid. Some enclosures propagated over a δ bracket stick out of the frozen bracket: C07 c's upper end 0.4450508181 > 0.44505, C11 2δ′'s upper end 0.22507667 > 0.22507, and route A's C10b c over [0.026890, 0.026891], with upper end 0.5951068539 > 0.5951. At the row points they are inside. This confirms the tree-graph lane's F6. No other discrepancy was found except S6 and S7.

## 5. Answers in this lens

- **(v) Are the sup norms after integration finite, with V-dependence only at size ≥ 4?** Yes, in both routes (2.2, 2.3). Each output term is bounded, measurable and defined at every V. It depends on V only through Y(X) = ∪Y″(Γ). It is constant unless Y(X) holds a loop, and a loop has at least 4 coarse links.
- **(vi) Does carrying the Wilson term inside R_k break any step?** No (2.6). No step at k ≥ 1 uses Lemma B or closure, and no constant changes. The clause itself needs a definition (S1).
- **Closed loop, reality, coarse-gauge invariance.** Kept, in both routes (2.4, 2.5). The output does not depend on which line gauge is used.
- **Is c increasing, so the self-map propagates?** The frozen c is strictly increasing. c* and c_♯ are nondecreasing, which is enough (2.7, S4).
- **Uniform in N and K?** Yes, for every step bound (2.8). The C16 readout is per final torus (S8).
- **Cross-lane F2 (the "exactly the frozen constants" rule).** In this lens the frozen implication C_k ⇒ H_{k+1}(κ, c(δ)δ) is DERIVED twice, so no frozen constant is refuted. Both routes also prove sharper constants, and they disagree on which one is "the" proved constant. Whether 16(vii) means "equal to" or "implied by a written proof" is a decision for the owner before the freeze, as the tree-graph lane says.

## 6. Scratch files (pre-freeze disclosure)

All are under `pkg/attack/g1st/`. None is an engine, and none is evidence. The hashes are also in `g1st/SHA256SUMS`.

- `g1st_constants.py` (`a17234534a106b15b8564c8075f769754e35ebd0e005f877f669fb379e67b65b`), output `g1st_constants.out` (`e089966667563727f4cdbd7d95c6f155842eb6131b3452e778e061587304349d`): my enclosures of c, c*, c_B and c_♯ at the row points, every edge, δ_eq, C16, the Lemma 4.22 constant and the Wilson per-root factors.
- `g1st_geometry.py` (`6e8c86454ade6512c9963a1ee72fd8031c78cd9d4216351d152202a4ba670ef0`), output `g1st_geometry.out` (`9654dcc5aed7c048aa54cfc79424cdd6f1351924c57ea2fd25259b174633ea3b`): the b = 2 geometry sanity read on (ℤ/8)⁴ (2.1).
- `g1st_duality.py` (`3ab47c0efb6bb877caa8b8af53bb4efc7a71ddfd0a723c8f508a116ba84d8349`), output `g1st_duality.out` (`3701176dbf5ba9ceada505acbf5c796f205c758cbad5d963ee6249973ac2b1ea`): Lemma S3's inequality e^{3(j−1)/4} ≥ j, and the C10b and C10c slacks.
- `g1st_brackets.py` (`5313912cae37a373801648ea2f3e8420f110a1a4f04fb2cbbb113ee28ce64ed6`), output `g1st_brackets.out` (`6882fd2a9269990413255ccf9ed946ee43eff743173e01049d97598afa874133`): containment of each displayed bracket of both routes (S6).

### References

- R. Kotecký and D. Preiss, Cluster expansion for abstract polymer models, Comm. Math. Phys. 103 (1986) 491–498. REPORTED, as used by route A's Theorem 4.9.
- Repo: NOTE-YM4-03-ONE-SCALE-BLOCKING.md (Lemma 3, Theorem 4 items 2 and 3, Proposition 2); NOTE-YM4-03C-BLOCKED-ACTION.md (§2 Lemma A, §5 sides, §6 Lemma B and the polymer form, §12 OPEN).
- This package: `derive/G1-a.md`, `derive/G1-b.md`, `attack/G1-treegraph.md`, `PREDICTION-v2.hbp`, `note_outline-v2.txt` §16.
