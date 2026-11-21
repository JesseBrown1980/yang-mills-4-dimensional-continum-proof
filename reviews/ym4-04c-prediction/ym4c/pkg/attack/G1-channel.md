# G1 attack: bookkeeping and the line channel (second seat)

**Status.** Written on November 9, 2026, by a second-seat referee lane. Base: main `830fd3f`. No file in the repo was changed. Targets: `pkg/derive/G1-a.md` (route A) and `pkg/derive/G1-b.md` (route B), against the draft `synth/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp`. Lens: attack-brief questions (iii) and (iv). That covers the root-object bookkeeping behind c(δ), the e^δ prefactor, the max over n ≥ 4, the line-channel factor #Y″ ≤ #Y/2 with e^{−κ#Y/2} ≤ e^{−4κ}, Lemma A at both positions, and the map from a fine Y to its coarse support Y″.

**Verdict: HOLDS.** I found nothing blocking. Theorem G1 as frozen follows from each derivation. Every step in this lens checks by my own argument. Every constant in both tables reproduces under my own exact enclosures. I report seven minor findings. One of them is new and DERIVED here: the slice lower bound of section 3. It proves the draft's C10 claim for every representation. It also raises the power of C10b and C10c.

Symbols follow the binding renames. a is ½ Re Tr only. b is the blocking factor 2 only. κ = 1/4 is the norm weight. (α, θ) is the Kotecký–Preiss pair. δ′ = δe^δ. e_0(ℓ), e_1(ℓ) are the position-0 and position-1 line links of a coarse link ℓ. Y″(Y) is the set of coarse links with both positions in Y. Route A writes f = #off(o) and m = #line(o). Route B writes n = |o| and s = |off(o)|.

Arithmetic. All of it is exact. I used Fractions, with e^x enclosed by a Taylor sum plus a remainder bound, range reduction by halving, and outward rounding to 2⁻¹⁶⁰. Floats appear only in printing. The scripts are listed in section 9. They are scratch checks, not engines, and not evidence.

## 1. The coarse shadow and Lemma A at both positions (question iv)

**Claim.** An integral T(V) of a fine-gauge-invariant F over the off links, with every line at (1, V), depends on V only through V restricted to Y″(supp F). (Route A Lemma 4.3. Route B Lemma 4.2 and its corollary.)

**Own argument.** Fix ℓ. The gauge transformation at the midpoint m_ℓ by h moves e_0(ℓ) from 1 to h⁻¹. It moves e_1(ℓ) from V_ℓ to hV_ℓ. It moves the off links at m_ℓ by h on one side. No other line link meets m_ℓ. Suppose F does not see e_0(ℓ). Then F's value at the moved point equals F at (V_ℓ → hV_ℓ, off links moved). Haar measure on the off links absorbs the move. So T(V) = T(V with V_ℓ → hV_ℓ) for every h, and T is constant in V_ℓ. Now suppose F does not see e_1(ℓ). V_ℓ enters the line gauge only at e_1(ℓ), so T does not involve V_ℓ. A function that is constant in each V_ℓ with ℓ ∉ Y″ separately is a function of V restricted to Y″. This is YM4-03C §2 Lemma A. That proof never uses that F is a product of plaquette class functions. DERIVED. Both lanes are right.

**Coarse invariance.** Let g be a coarse gauge transformation. Extend it by g̃(2x′) = g(x′), g̃(m_ℓ) = g(x′) for ℓ = (x′, μ), and g̃ = 1 elsewhere. Then e_0(ℓ) goes from 1 to g(x′)·1·g(x′)⁻¹ = 1. And e_1(ℓ) goes from V_ℓ to g(x′)V_ℓg(x′ + e_μ)⁻¹ = (V^g)_ℓ. So the line gauge is preserved. This checks, and it is YM4-03 Theorem 4 item 3.

**Clusters.** In a cluster X = (Γ_1, Γ_2) with Γ_1 ≁ Γ_2, it can happen that e_0(ℓ) lies only in Γ_1 and e_1(ℓ) only in Γ_2. Then z_{Γ_1} is constant in V_ℓ and z_{Γ_2} does not involve V_ℓ, so the product does not involve V_ℓ either. So the right support is Y(X) = ∪_Γ Y″(Γ) (route A), or S_X = ∪_i S(line(Γ_i)) (route B). It is not Y″ of the union of the supports. Both lanes use the right one. Each z_Γ is a function of V restricted to Y″(Γ), so Φ(X) is a function of V restricted to Y(X).

**The factor.** Positions of distinct coarse links are distinct (route A Lemma 4.1 item 1). So 2#Y″(W) ≤ #line(W) for every set W of fine links. For a line-supported Y this gives #Y″ ≤ #Y/2. For an object with an off link it gives #Y″ ≤ (n − 1)/2. For a polymer it gives 2#Y″(Γ) ≤ #line(supp Γ) ≤ Σ_{o∈Γ} #line(o). DERIVED.

**Minor finding M6 (the loop condition does more than the lanes use).** No line link touches a fine site with two or more odd coordinates. A midpoint meets exactly the two line links of its own coarse link. I checked both facts on (ℤ/8)⁴ (instances script). So a closed fine loop made of line links is a subdivided closed coarse loop. Hence every line-supported Y in H_k already has Y″ holding a loop, and #Y ≥ 8. Route A's Lemma 4.5 item 2 ("if Y″(Y) holds no loop, R^L is constant") is vacuous for 𝒴_L. So is route B's clause "V-dependent only if |o| ≥ 8". Both are harmless. Presentational.

## 2. The exact line channel (question iv)

**Claim.** For Y ∈ 𝒴_L, the term R_k(Y; (1, V)) leaves the off-link integral exactly. Its weight passes to the coarse scale with e^{κ#Y″} ≤ e^{κ#Y}e^{−κ#Y/2} ≤ e^{κ#Y}e^{−4κ}, and with no e^δ.

**Own argument.** Y holds no off link, so exp(Σ_{𝒴_L} R) is a function of V alone and factors out of E_V (route A Lemma 4.7, route B (4.1)). Section 1 gives V-dependence through Y″ only. Every Y′ with ℓ ∈ Y″(Y′) contains e_0(ℓ). So the line-channel share of the coarse norm at ℓ is at most Σ_{Y′∋e_0(ℓ)} e^{κ#Y″(Y′)} sup|R_k(Y′)|. Section 1 and #Y′ ≥ 8 bound that by e^{−4κ} Σ_{Y′∋e_0} w(Y′). The fine norm at the one link e_0(ℓ) is shared by the line roots and the off roots, and it bounds their sum by δ. This is right in both lanes. DERIVED.

**The smallest instance, exactly (C10).** On fine (ℤ/8)⁴ I built one Y per coarse plaquette P″: its 8 line links. Checks:

- #Y = 8 for all 1536 of them.
- Every line link lies in exactly 6 of them, and no off link lies in any.
- Y″(Y) = ∂P″, so 2#Y″ = #Y.
- Every coarse link lies in 6 coarse plaquettes.
- The fine 2 × 2 loop in the line gauge equals V_{P″} as an exact quaternion, at 4 rational configurations.
- After a random rational fine gauge transformation, the trace of the fine loop equals the trace of (BU)_{P″}.

So the fine norm is 6 · 2|s|e^{8κ} and the coarse norm is 6 · 2|s|e^{4κ}. The ratio is e^{−4κ}. Route A's c* and route B's c_♯ both equal e^{−4κ} at small δ. So both are attained here. The frozen c is strictly larger.

## 3. New: every representation of the C10 output has norm at least e^{−4κ}δ (minor finding M3)

Route A (Proposition 4.23 and Gap 3) says that a different representation of log ρ_{k+1} "could have a smaller norm". So it calls the optimality of G1* a statement about the construction only. Route B claims optimality "by C10". The draft C10 says "every valid step bound on this class has c(δ) ≥ e^{−4κ}". Neither lane proves that claim for an arbitrary representation. The six-plaquette projection bound of C10c gives only (3π/16)e^{−4κ} ≈ 0.589e^{−4κ}. Here is a proof of the full claim.

**Lemma (slice bound), DERIVED here.** Let log ρ_{k+1} = const + Σ_Y R(Y) be any H_{k+1} representation, and fix a coarse link ℓ. Then

```text
sum_{Y containing l} sup |R(Y)|  >=  (1/2) osc_g [ log rho_{k+1}(V^g) ],   V^g := every coarse link at 1 except V_l = g.
```

*Proof.* On the slice V^g, each R(Y) with ℓ ∉ Y is a function of fixed links, so it is constant. So Σ_{Y∋ℓ} R(Y; V^g) = log ρ_{k+1}(V^g) + C. The oscillation of a sum is at most the sum of the oscillations. Each oscillation is at most 2 sup|R(Y)|. ∎

Since #Y ≥ 4, the norm at ℓ is then at least e^{4κ} times the right side. Take an output of the form const + Σ_{P″} f(χ½(V_{P″})), as in C10, C10b and C10c. On the slice, the 6 plaquettes through ℓ read χ½(g) and every other plaquette reads 2. I checked this exactly. So every representation has norm at least 3e^{4κ} osc_{[−2,2]}(f). That is exactly the norm of the natural decomposition, 6e^{4κ}osc(f)/2.

Consequences:

- **C10.** f = sχ½ and osc(f) = 4|s|. Every representation has norm at least 12|s|e^{4κ} = e^{−4κ}δ_in. So no valid step bound C(δ)δ has C(δ) < e^{−4κ}, at any δ > 0, for any representation. Route A's caveat can go. On 0 < δ ≤ 0.072094, G1* is optimal among all valid step bounds. Route B's optimality claim is true, and this is its missing proof.
- **C10b.** The every-decomposition bound becomes the natural δ_out ∈ [4.077422e-6, 4.077424e-6] at s = 1/2000, in place of the projection bound [4.00e-7, 4.01e-7]. The slack c(δ_in)δ_in/δ_out is then at least 3924.6 (frozen c), 2426.1 (route A c*) or 3357.7 (route B c_♯), in place of about 3 × 10⁴. At s = 1/4096 it is at least 6236.4, 4968.7 or 5122.8.
- **C10c (v2).** Every decomposition has norm at least δ_out^nat. The every-decomposition slack becomes at least 7.116 (frozen c), 6.594 (c*) or 6.594 (c_♯) at s = 1/65536, in place of [12.08, 12.09]. At s = 1/8192 it is at least 12.754, 6.592 or 11.023. The δ_out^nat bracket used here is the v2 row's own, 6e^{4κ}[s − 4s², s + 4s²].

None of this changes a frozen value. The frozen projection bounds stay true. They are weaker tests than the data allow. Recommendation: state the slice lemma in the note's C10 paragraph. Read C10b's and C10c's G1 tests against the slice bound, as appended rows.

## 4. Root-object bookkeeping (question iii)

### 4.1 Route A (§4.9): confirmed

Fix ℓ and put e_0 = e_0(ℓ). Let X enter the norm at ℓ. Some Γ ∈ X has ℓ ∈ Y″(Γ), so e_0 ∈ supp Γ. Let o be the least object of Γ that holds e_0. The three cases (i) Γ = {o} = X's only member, (ii) Γ = {o} with X ≠ {Γ}, and (iii) #Γ ≥ 2 cover every X. A cluster counted twice only adds nonnegative terms. Each step, checked:

- e^{κ#Y(X)} ≤ e^{d(X)}, since #Y(X) ≤ Σ m_X(Γ)#Y″(Γ) and κ#Y″(Γ) ≤ (κ/2)Σ_{o∈Γ}#line(o) = d(Γ).
- S_1 ≤ ω_o e^{κ⌊m/2⌋}1[m ≥ 8], since #Y″(o) ≤ ⌊m/2⌋ and a coarse loop has at least 4 links.
- S_2 ≤ ω_o e^{(κ/2)m}(e^{δ′f} − 1). This is Corollary 4.10(b) at Γ = {o}, with a({o}) = δ′f and d({o}) = (κ/2)m.
- S_3 ≤ ν̃_o[(1 + δ′)^f − 1]. Corollary 4.10(a) turns the inner sum into Π ν̃. Lemma 4.12 item 2 at the line link e_0 then gives this, because attachments happen only at the off links of the root (Lemma 4.11). Its hypothesis is needed only at off links, where Lemma 4.13 item 1 supplies it.
- (e^{δ′f} − 1)(1 + e^{δ′f}) = e^{2δ′f} − 1. So S_1 + S_2 + S_3 ≤ ω_o e^{κ#o} q(f, m).
- Lemma 4.16's closed form for Q agrees with a brute-force supremum of q over 1 ≤ f ≤ 80 and 0 ≤ m ≤ 80, at 8 values of δ from 0.001 to 0.10166. The maximiser is (f, m) = (1, 8) for small δ and (f, 0) above 0.072094.

### 4.2 Route B (§4.10): confirmed

Root o_0 ∋ l_0, terms L, M_1, M_2:

- M_1 needs #line(o_0) ≥ 8, so n ≥ 9 and #S ≤ (n − 1)/2.
- M_2 is "the rooted sum minus the single-object term". That is Σ_{Γ∋o_0} z̄e^{a+d} − ρ̄(o_0)e^{(κ/2)n} ≤ ω_{o_0}e^{ts} − ρ̄e^{(κ/2)n}, by Lemma 4.8.
- s ≤ n gives e^{κn}ρ̄[e^{−(κ/2−2δ′)n} − e^{−κn/2}].
- I checked the algebra of c_♯ ≤ c_B ≤ c line by line. The key identity is e^{δ}[e^{−4κ} + f(8)] = e^{δ}e^{−8(κ/2−2δ′)}.

### 4.3 Minor finding M1: the root holds a line link, and neither lane uses it

The root is chosen as an object that holds e_0 (route A) or l_0 (route B), which is a line link. So m ≥ 1 for every route-A root, and s(o_0) ≤ n − 1 for every route-B root. Route A's Q takes the supremum over m ≥ 0. Route A then describes its third entry as "a root with f off links and no line link together with its clusters" (§4.9, last paragraph). No such root exists. Route B uses s ≤ n.

Both bounds stay valid, since a supremum over a larger set is larger. But some of the lanes' thresholds are reads of their formulas, not limits of their proofs:

| Statement | As written | With m ≥ 1 (A) or s ≤ n − 1 (B) |
|---|---|---|
| route A, c* = e^{−1} up to | δ = 0.072094 | δ = 0.077320139 |
| route A, c* < 1 up to | δ_crit* ∈ [0.109530694, 0.109530695] | all of 2δ′ ≤ κ (δ ≤ 0.111780108); c* ≤ 0.98687 at the edge |
| route B, c_♯ = e^{−1} up to | δ = 0.0116995481 | δ = 0.0130676214 |

With m ≥ 1, route A's Q is max{e^{−5κ+2δ′}, e^{−κ/2} sup_{f≥4} g(f)}. I checked this by brute force at δ = 0.08, 0.09 and 0.10, where the maximiser is (f, m) = (7, 1), (8, 1) and (10, 1). So route A's self-map edges 0.01582/0.01583 and 0.02037/0.02038, its δ_crit*, and its readings of C11 and C12 would all move again.

Fix: state the restriction m ≥ 1 (or s ≤ n − 1), or say plainly that the formula drops it. Label the edges as properties of the stated formula. No frozen constant is affected.

### 4.4 The e^δ prefactor: confirmed

|e^x − 1| ≤ |x|e^{|x|} and |R_k(o)| ≤ δe^{−κ#o} ≤ δ give ω_o ≤ e^δ sup|R_k(o)|. So Σ_{o∋l} e^{κ#o}ω_o ≤ δe^δ = δ′. That is exactly why C_k is stated in δ′. The e^δ belongs only to the object channel. The line channel is exact and carries none. Both lanes agree on this. The frozen c puts e^δ on both channels, which is valid and loose. Both lanes note that e^{δe^{−4κ}} would also do; that is right and unused.

### 4.5 The max over n ≥ 4: confirmed, plus minor finding M2

**Confirmed.** The bracket f(n) = e^{−(κ/2−2δ′)n} − e^{−κn/2} has its real maximiser at n* = ln((κ/2)/u)/(2δ′), with u = κ/2 − 2δ′. And n* ≥ 2/κ = 8. This matches the engine plan's E4 formula. The certified integer maximisers at the rows' points are:

| Point | n |
|---|---|
| C08 | 8 |
| C14 at 1/64 | 8 |
| C07 | 9 |
| C10b at s = 1/4096 | 9 |
| C10b at s = 1/2000 | 11 |
| C13 at 49/1000 and 1/20 | 17 |

So the max over n ≥ 4 always sits at n ≥ 8, as both lanes say. The max equals f(8) exactly when δ ≤ δ_eq. I reproduce δ_eq ∈ [0.0070256343, 0.0070256344]: f(8) − f(9) encloses +9.03e-13 at the lower end and −3.75e-12 at the upper end.

**M2.** Route A's Remark 4.18 says the frozen c "is exactly the uniform bookkeeping". That is not right. Take uniform bookkeeping per root. Each root then gives, per unit e^δ w(o), at most e^{−κn/2}1[n ≥ 8] + g_fr(n). For n ≥ 8 that equals e^{−(κ/2−2δ′)n}. For n < 8 it is g_fr(n) ≤ g_fr(8). So the per-root maximum is e^{−8(κ/2−2δ′)}, and uniform bookkeeping gives route B's c_B = e^{δ−8(κ/2−2δ′)}. The frozen c adds two further relaxations. It puts e^δ on the exact line channel. And it adds the two channel suprema, where the proof needs only the supremum of their per-root sum. The two agree only for δ ≤ δ_eq. Route B has this right. Fix route A's wording: "the frozen formula is the uniform bookkeeping after two relaxations; it equals the per-root uniform bound c_B for δ ≤ δ_eq".

On the boundary 2δ′ = κ/2, the max is a supremum with value 1, and it is not attained. This cannot happen at a rational δ > 0, since δe^δ is then irrational. No action needed.

## 5. The two smallest instances, against the formulas

**One line-supported object (C10).** See section 2. The exact ratio is e^{−4κ}, and the route A and route B bounds equal it. By section 3 no representation does better.

**Two objects sharing a link (C10b).** On (ℤ/8)⁴, checked exactly:

- Each rectangle has 6 links: 4 line links and the 2 arm off links, which the pair shares.
- Each rectangle alone has Y″ equal to one coarse link, which holds no loop, so it integrates to a constant (Lemma A plus the forest lemma).
- The pair has Y″ = ∂P″.
- Every line link lies in 6 rectangles. Every off link lies in 0 or 2.

The moment identity follows in one line. In the line gauge, χ_b = 2⟨A, π⟩ and χ_t = 2⟨B̄, π⟩ in ℝ⁴, with π Haar on S³ and AB = V_{P″}. So X = χ_b + χ_t = ⟨c, π⟩ with |c|² = 4(2 + χ½(V_{P″})). Then E[X^{2m}] = |c|^{2m}(2m − 1)!!/(2^m(m + 1)!) = Cat_m(2 + χ½)^m. I checked m = 1 to 6 at 6 rational (A, B). The identity is DERIVED.

The root of each P″ term at e_0 is a rectangle with f = 2 and m = 4. Route A then bounds the ratio by e^{δ}e^{−4κ}(e^{4δ′} − 1). Route B uses n = 6 and e^{δ}f(6). The exact ratio is [1.516e-4, 1.517e-4], far below both. Two objects that share only a line link have disjoint off links. Their activities factor, and the gas makes them compatible, so no cross term arises. That is right.

## 6. The constant tables against the draft

Every number I recomputed agrees with both lanes to the digits they print:

- **Route A:** c and 2δ′ at C07, C08, C10b (both s), C13, C14 and C11; c* = e^{−1} through 0.072094, with third entry ≤ 0.36787107; its lower enclosure 0.36787984 at 0.072095; c* at C12 [0.3727262, 0.3727351] and at C11 [0.7717124, 0.7719305]; δ_crit* ∈ [0.109530694, 0.109530695] at f = 16.
- **Route B:** c_B and c_♯ at every point; δ_eq; c_♯ = e^{−1} through 0.0116995481; c_B = 1 at [0.0558087801, 0.0558087802]; c_♯ = 1 at [0.0577661141, 0.0577661142], n = 14.
- **Frozen:** δ_crit ∈ [0.049617491, 0.049617492], n = 17.
- **Ordering:** c*_A < c and c_♯ ≤ c_B ≤ c hold at all 58 points δ = i/1000, i = 1 to 58.

**Minor finding M4 (three draft brackets are narrower than the image of their own input brackets).** Both lanes write that every frozen value "reproduces inside its bracket", and both then print enclosures that leave the bracket:

| Row | Draft bracket | Image of the draft's δ bracket | The bracket is exceeded for |
|---|---|---|---|
| C07 c(δ_1) | [0.44504, 0.44505] | [0.44504299, 0.44505082] | δ_1 > 0.01104489552 |
| C10b c(δ_in), s = 1/2000 | [0.5950, 0.5951] | [0.59509519, 0.59510685] | δ > 0.02689041235 |
| C11 2δ_1e^{δ_1} | [0.22505, 0.22507] | [0.22505228, 0.22507667] | δ_1 > 0.10165726602 |

At the actual inputs the frozen values hold. At δ_1 = 0.0110444507 (the critic's read), c = 0.44504652. The exact δ_in = 12e^{3/2}/2000 = 0.02689013442 gives c ≤ 0.59509676. But C07's falsifier "c(δ_1) ≥ 0.44505" fires on part of C07's own δ_1 bracket, namely (0.01104489552, 0.011045]. Fix: the lanes should write "the frozen value at the frozen point reproduces; the image of the δ bracket is wider". The freeze should either widen these output brackets (for example C07 c to [0.44504, 0.44506] and C11 to [0.22505, 0.22508]) or narrow the input brackets. That is G_grids and C07 bookkeeping, not a G1 error.

## 7. Definitions the frozen text leaves open (minor finding M5)

The THEOREMS and CERTIFICATES rows say "Σ_{Γ∋e}Πω ≤ t from Σ_{o∋e}ω_o e^{t s(o)} ≤ t" and "α = t = δ′, θ = κ". They do not define s(o), ω, the range of e, or what #γ counts in d(γ) = θ#γ at k ≥ 1. The two lanes read them differently:

- **Route A:** attachments at off links, d = (κ/2)Σ#line(o). The frozen s(o) = #o is a special case.
- **Route B:** s(o) = #off(o), d = (κ/2)Σ|o|.

Both readings mean "weight κ per coarse link, paid by two fine links", and both close. The literal reading, d(γ) = κ times the number of links, does not close (KP) (route B §4.12). I agree. The note must state one reading. No frozen constant changes.

## 8. Pointer outside this lens (minor finding M7)

Both lanes prove the frozen implication C_k ⇒ H_{k+1}(κ, c(δ)δ). Both also prove strictly smaller constants (c* < c, and c_♯ ≤ c_B ≤ c). I reproduce every number. So the NOT_MET clauses of C11 and C12 are properties of the frozen formula, not limits of G1. So are the edges of C13 and C14, C14's head-free clause, and C10b's 3e-5 clause. With m ≥ 1 (M1) this is stronger still. Attack-brief question (vii) says "a differing constant makes every row resting on it read UNSUPPORTED". Whether that applies to a valid but weaker frozen constant is a gate decision for the owner and for the constants lens. Nothing in my lens makes a frozen constant wrong.

## 9. Findings

**Blocking: none.**

**Minor:**

- M1: roots hold a line link, so m ≥ 1 (A) and s ≤ n − 1 (B). Route A's third entry is an impossible root. The thresholds are reads of the formulas (section 4.3).
- M2: route A's Remark 4.18 "exactly" is wrong. The uniform per-root bound is c_B. The frozen c adds two relaxations and equals c_B only for δ ≤ δ_eq (section 4.5).
- M3: the slice lemma proves C10 for every representation. It removes route A's caveat, supplies route B's missing proof, and raises the power of C10b and C10c (section 3).
- M4: the C07, C10b (s = 1/2000) and C11 output brackets are narrower than the image of their own δ brackets. The lanes' "reproduces inside" is false as written (section 6).
- M5: s(o), ω, the range of e and d(γ) are undefined in the frozen rows, and the lanes read them differently (section 7).
- M6: the H_k loop condition already forces #Y ≥ 8 and a loop in Y″ for line-supported Y (section 1).
- M7: the constants question belongs to the (vii) lens (section 8).

## 10. Scratch files (pre-freeze disclosure)

All are in `/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/attack/`. None is an engine, and none is evidence.

- `G1-channel-checks.py` (`d226bf785aab73ffb82e6fbafabf70336a0d0b579b08536c6af87725c8fd3481`), output `G1-channel-checks.out` (`f178377929250b539d6959d3969a67ce5df8759756f15161984b619e1550a9e6`). Frozen c, route A c* in closed form and by brute force, route B c_B and c_♯, δ_eq, the thresholds, the δ_crit values, the M1 sharpening, the M4 images, and the ordering grid.
- `G1-channel-instances.py` (`b99f575629c125e0144a907576d8febbb09831641ff08a3363052be67e523d57`), output `G1-channel-instances.out` (`2c484fc9fd8cb0078392efbcf3e01518e8fa095f8c228173414fee3423a6bf90`). On (ℤ/8)⁴: the midpoint rule, C10's counts and exact holonomies, C10b's counts and shadows, the Catalan moments, and the slice.
- `G1-channel-slice.py` (`6c10a80ea931f6427aff65eae1bf0b74200c700903836086b89239343e18c61d`), output `G1-channel-slice.out` (`c9c9a74df2f181694cc2b76d57f38f836beacc5b16d6895cd4ab3c26046518b5`). The M1 edge read, and the C10b and C10c slack under the slice bound.
