# G1 second-seat attack: the expansion machinery

**Status.** Written by the second-seat referee for YM4-04C on November 9, 2026, from main `830fd3f`, before any engine code. Targets: `pkg/derive/G1-a.md` (route A) and `pkg/derive/G1-b.md` (route B). Frozen text checked: the draft `ym4-04c/synth/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp` and its repair `pkg/PREDICTION-v2.hbp` (rows CERTIFICATES, THEOREMS, C07 to C16, C10c), and the attack brief in `pkg/note_outline-v2.txt` section 16. Lens: the Mayer and cluster expansion of log ∫ exp(Σ_Y R_k(Y)) over the off links, the tree-graph bound with t = δ′, the Kotecký–Preiss per-polymer corollary, the incompatibility relation between Y-objects after blocking, and convergence (brief question (i)). Nothing in the repo was modified. No engine ran. Every number below is an exact rational enclosure with outward dyadic rounding at 2⁻²²⁰ from the scratch scripts of section 6; floats are display only. Tags: DERIVED, CONJECTURE, OPEN, REPORTED as in NOTE-YM4-03C.

Symbols as in the renames: a(g) = ½ Re Tr g; b = 2; κ = 1/4; the KP pair is (α, θ); δ′ = δe^δ; "fine" is scale k, "coarse" is scale k + 1; e_0(ℓ), e_1(ℓ) are the two positions of a coarse link ℓ; f = #off(o), m = #line(o) for an object o.

## 0. Verdict

**GAP.** I found no error in either proof. Every step of the expansion machinery in both routes holds, by my own argument (section 2). G1 as an implication, C_k ⇒ H_{k+1}(κ, c(δ)δ), is DERIVED twice. Route A's stronger G1* (2δ′ ≤ κ ⇒ H_{k+1}(κ, c*(δ)δ)) also holds.

Two findings block the freeze as written. Neither moves a frozen number of c(δ) or C_k.

- **F1.** Brief question (i) asks whether the KP per-polymer corollary holds "with these a(γ) and d(γ)". The frozen rows give d(γ) = θ#γ with θ = κ at step k. Both literal readings of #γ fail. With #γ = the number of fine links, the KP hypothesis fails on an explicit admissible input at δ = 1/100 (section 3, F1). With #γ = the number of objects, the weight bound e^{κ#Y(X)} ≤ e^{d(X)} fails on C10c's own object. Each route redefines d, and the two redefinitions differ.
- **F2.** Brief question (vii) and the v2 THEOREMS row demand that the proved constants be exactly the frozen ones. They are not, in either route. I confirm G1*. So the frozen NOT_MET clauses of C11 and C12, the C13 and C14 edges, C14's head-free clause and C10b's 3 × 10⁻⁵ clause are facts about the pinned formula, not about the method. The two derivations also disagree on whether C_k is "equal". The owner must decide what the rows pin before the freeze.

Six minor findings follow (F3 to F8). The constant tables of both derivations reproduce in my own enclosures (section 4), with one wording caveat (F6).

## 1. What was attacked

1. The gas: the expansion of ∏_{o∈𝒴_O}(1 + f_o) into compatible families, with polymers linked by shared off links (A Lemma 4.7; B Lemma 4.6a).
2. The activities: z_Γ(V) depends on V only through Y″(Γ), is real, and is coarse-gauge invariant (A Lemmas 4.3, 4.8; B Lemma 4.2 and the both-positions corollary).
3. The cluster expansion and its convergence (A Theorem 4.9, REPORTED; B Lemma 4.6, REPORTED, and Lemma 4.9a).
4. The tree-graph bound with t = δ′ (A Lemma 4.12; B Lemma 4.8).
5. The KP condition with α = t = δ′ and the route's d (A Lemma 4.13; B Lemma 4.9).
6. The per-polymer corollary and its "beyond one polymer" part (A Corollary 4.10; B Corollary 4.7a).
7. The root bookkeeping that turns these into the coarse norm (A Proposition 4.15, Lemma 4.16; B section 4.10).
8. The frozen formula's derivation from the proved one (A Lemma 4.17, Remark 4.18; B Theorem 4.10).

## 2. What I confirm, with my own argument

### 2.1 The gas and the incompatibility relation

In the line gauge every position-0 link is 1 and every position-1 link is V_ℓ. Only off links are integrated. Objects with no off link (𝒴_L) leave the integral as exp(Σ R^L). For the rest, ∏(1 + f_o) = Σ_{𝒮⊆𝒴_O} ∏_{o∈𝒮} f_o, a finite sum. Split 𝒮 into components of the graph "share an off link". Distinct components use disjoint sets of off links. Their line links are fixed numbers. So the off-link integral of the product factors over components. A family of pairwise compatible polymers has disjoint object sets, since every object holds an off link. Its union has exactly these polymers as components. So subsets and compatible families correspond one to one. The relation "off(Γ) ∩ off(Γ′) ≠ ∅" is reflexive and symmetric. **Confirmed (both routes).**

Objects that share only line links are compatible. That is correct: the shared links are not integrated. After blocking, an output Y(X) may be a disconnected set of coarse links, for example two loops whose polymers met through a fine off link. H_{k+1} allows that. At the next step such a Y is one object; the root decomposition never uses that an object is connected. **Confirmed.**

### 2.2 Activities: support and invariance

Let F = ∏_{o∈Γ} f_o. Each f_o is invariant under every fine gauge transformation, so F is. The gauge transformation at m_ℓ by h sends (U_0, U_1) = (1, V_ℓ) to (h⁻¹, hV_ℓ) and multiplies the 6 off links at m_ℓ by h on one side. If F does not see e_0(ℓ), Haar invariance of those 6 off links gives z_Γ(V) = z_Γ(V with V_ℓ → hV_ℓ). If F does not see e_1(ℓ), V_ℓ does not enter. So z_Γ depends on V only through Y″(Γ) = {ℓ : e_0(ℓ), e_1(ℓ) ∈ supp Γ}. The extension g̃ = g at 2x′ and at m_ℓ, g̃ = 1 elsewhere, keeps every line in the form (1, ·) and sends V to V^g. So z_Γ is coarse-gauge invariant. A gauge-invariant function on a coarse forest is constant. On a coarse torus of side ≥ 4 every cycle has ≥ 4 links. **Confirmed (both routes).**

A cluster X = {Γ_1, …} has Φ(X; V) = φ(X)∏ z_{Γ_i}(V). Each factor is a separate integral. So Φ depends only on Y(X) := ∪_i Y″(Γ_i), not on Y″(∪ supp Γ_i). If e_0(ℓ) ∈ Γ_1 and e_1(ℓ) ∈ Γ_2 only, Φ does not depend on V_ℓ. Route A's Y(X) and route B's S_X are this union. **Confirmed.**

### 2.3 The tree-graph bound with t = δ′

Route A, Lemma 4.12. Root a polymer Γ at e by its least object o ∋ e. The components C of Γ ∖ {o} each meet o at an off link; indexing C by the least such off link is injective, since two components holding a common off link would be adjacent. Each component has fewer objects. Dropping every constraint among components gives T_n(e) ≤ Σ_{o∋e} ν_o ∏_{e′∈off(o)}(1 + T_{n−1}(e′)). Under Σ_{o∋e} ν_o e^{t#off(o)} ≤ t at every off link, induction gives T(e) ≤ t, and the per-root form ν_o[(1 + t)^f − 1] for #Γ ≥ 2 at any link e, line or off. **Confirmed.**

Route B, Lemma 4.8. The breadth-first spanning tree from o_0, with each child attached at the least off link it shares with its parent, is an injection into decorated trees. The majorant G_n(o) = ω_o ∏_{e∈off(o)} ∏_{o′∋e}(1 + G_{n−1}(o′)) over-counts (it lets an object be its own child and repeat across branches), which only adds. Induction gives G_n(o) ≤ ω_o e^{t s(o)}. **Confirmed.**

Attachments happen only at off links in both, because polymers are linked only through off links. So t can be charged to off links alone. Route A uses this; route B does not.

### 2.4 The KP condition

Route A: ν̃_o := ω_o e^{δ′f + (κ/2)m}, a(Γ) := δ′Σ_{o∈Γ} f_o, d(Γ) := (κ/2)Σ_{o∈Γ} m_o. Then ν̃_o e^{δ′f} = ω_o e^{2δ′f + (κ/2)m} ≤ ω_o e^{κ(f+m)} iff 2δ′ ≤ κ (the line part needs only κ/2 ≤ κ). The norm and |e^x − 1| ≤ |x|e^{|x|} give Σ_{o∋e} ω_o e^{κ#o} ≤ δe^δ = δ′. So the tree hypothesis holds with t = δ′, and T(e) ≤ δ′. Every Γ′ ≁ Γ holds an off link of Γ. So the KP left side is at most δ′#off(Γ) ≤ a(Γ). **Confirmed under 2δ′ ≤ κ.**

Route B: ω_o := ρ̄(o)e^{αs(o) + (κ/2)|o|}, a(Γ) := α|off(Γ)|, d(Γ) := (κ/2)Σ|o|. Then ω_o e^{ts} ≤ ρ̄(o)e^{κ|o|}e^{−(κ/2 − 2δ′)|o|}, using s(o) ≤ |o|. This needs 2δ′ ≤ κ/2. **Confirmed under C_k.** Route B's remark that C_k is "the condition under which this proof closes" is true for route B's d only (see F2).

### 2.5 The per-polymer corollary

Route A, Corollary 4.10. The marker Γ̂ with z = 0, d = 0, a(Γ̂) = |z(Γ)|e^{a(Γ)+d(Γ)} + η, incompatible with itself and Γ only, satisfies KP. It adds 0 to every other left side. Every cluster that holds Γ̂ has Φ = 0. KP at Γ̂ bounds Σ_{X∋Γ}|Φ(X)|e^{d(X)}. Part (b) subtracts the term of {Γ}, which is |z(Γ)|e^{d(Γ)} since φ({Γ}) = 1. **Confirmed.** The KP statement used (Theorem 4.9) is the 1986 theorem with d in the hypothesis and e^{d(X)} in the conclusion. REPORTED, correctly cited.

Route B, Corollary 4.7a. Penrose's inequality |φ^T| ≤ #(spanning trees of g) is REPORTED and correctly cited. The tree recursion T_n(Γ) = exp(Σ_{Γ′≁Γ} u(Γ′)T_{n−1}(Γ′)) is right: a rooted tree on {1, …, m} is fixed by its j children, an unordered partition of {2, …, m} into j blocks each with a chosen root, and a tree on each block; the weight 1/(m − 1)! becomes (1/j!)∏_c 1/(m_c − 1)!. A tuple holding Γ is counted at most once per position of Γ, and φ^T is symmetric. **Confirmed.**

Both corollaries are used with e^{d(X)}, not e^{d(Γ)}, on the left. That form is needed (see F3).

### 2.6 The root bookkeeping

Fix ℓ. Every term with ℓ in its coarse support holds e_0(ℓ) in some object. Root it there.

Route A. With e^{κ#Y(X)} ≤ e^{d(X)} (since #Y(X) ≤ Σ m_X(Γ)#Y″(Γ) and 2#Y″(Γ) ≤ Σ_o m_o):

- S_1 ≤ ω_o e^{κ⌊m/2⌋}1[m ≥ 8]: a V-dependent single object needs #Y″ ≥ 4, so m ≥ 8.
- S_2 ≤ ω_o e^{(κ/2)m}(e^{δ′f} − 1): Corollary 4.10(b) at {o}.
- S_3 ≤ ν̃_o[(1 + δ′)^f − 1] ≤ ω_o e^{δ′f+(κ/2)m}(e^{δ′f} − 1): Corollary 4.10(a), then the per-root tree bound.
- S_2 + S_3 ≤ ω_o e^{(κ/2)m}(e^{2δ′f} − 1), since (x − 1) + x(x − 1) = x² − 1.
- The line channel is exact: e^{κ#Y″} ≤ e^{κ#Y/2} ≤ e^{−4κ}e^{κ#Y} for #Y ≥ 8.
- The line and object channels share the one budget Σ_{Y∋e_0} w(Y) ≤ δ, so the coarse norm is at most δ·max{e^{−4κ}, e^δ Q(δ′)}.

Lemma 4.16's closed form for Q is right. Case m ≥ 8 even: q = e^{−κm/2}e^{−(κ−2δ′)f}, largest at (f, m) = (1, 8). Case m ≥ 9 odd: smaller. Case m ≤ 7: q = e^{−κm/2}g(f) with g increasing on [0, 1/κ] ⊇ [0, 4]. **Confirmed.**

Route B. L ≤ e^{−4κ}w; M_1 ≤ 1[n ≥ 9]e^{−κ(n+1)/2}e^{κn}ρ̄; M_2 ≤ Σ_{Γ∋o_0} z̄e^{d+a} − z̄_{o_0}e^{d(o_0)} ≤ e^{κn}ρ̄[e^{−(κ/2−2δ′)n} − e^{−κn/2}]. The subtraction removes the exact single term and is in the safe direction. c_♯ ≤ c_B = exp(δ + 16δ′ − 4κ) ≤ c follows from n_* ≥ 2/κ = 8. **Confirmed.**

### 2.7 Convergence and the real logarithm

Route A: KP holds for the majorant ω, uniformly in V. Σ_X Φ̄(X) ≤ Σ_Γ a(Γ) < ∞ on the finite polymer set. KP holds for sz, s ∈ [0, 1], so Ξ(sz) never vanishes and Ξ(z) > 0; the real series is its logarithm. Route B: λ^{#Γ} scaling, a polynomial Z(λ) with Z(0) = 1, absolute convergence on the closed disc, analytic continuation, then λ = 1. Both give log Ξ(V) = Σ_X Φ(X; V), absolutely and uniformly in V, so regrouping by Y(X) is allowed. **Confirmed (both routes).** No bound depends on N, K or the number of plaquettes: every sum is rooted at one link.

### 2.8 The frozen theorem and G1*

Route A, Lemma 4.17: per root, the single part is ≤ e^{−5κ} and the multi part is ≤ g_fr(f + m), so Q ≤ e^{−5κ} + G_fr < e^{−4κ} + G_fr. Remark 4.18: the uniform bookkeeping (a, t and d all charged per fine link) needs 2δ′ + κ/2 ≤ κ, which is C_k, and returns c(δ) exactly. Route B: c ≥ e^δ[e^{−4κ} + f(8)] = c_B. **Confirmed.** So C_k ⇒ H_{k+1}(κ, c(δ)δ) is DERIVED, with c a valid but loose bound.

G1*: under 2δ′ ≤ κ, H_{k+1}(κ, c*(δ)δ). I checked every step of route A's split above. **Confirmed.**

## 3. Findings

### F1 (blocking). Brief question (i): the frozen d(γ) = θ#γ, θ = κ, does not close at step k

The frozen rows define d(γ) = θ#γ (THEOREMS, G0 clause; renames) and set θ = κ in C_k. They never say what #γ counts for a polymer of Y-objects.

*Reading 1: #γ = Σ_{o∈γ}|o|, the number of fine links.* Then KP needs Σ_{Γ′≁Γ} ω(Γ′)e^{δ′#off(Γ′) + κΣ|o′|} ≤ δ′#off(Γ). The norm gives only Σ_{o∋e} ω_o e^{κ|o|} ≤ δ′. The extra e^{δ′#off} has no room. An explicit admissible input (`g1tg_literal_d.py`), on fine (ℤ/8)⁴ at scale k:

- p_0 = the plaquette at 0 in plane (0, 1): 2 line links and 2 off links, ((0,1,0,0), 0) and ((1,0,0,0), 1).
- p_A = the plaquette at (1,0,0,0) in plane (1, 2), and p_B = the plaquette at (0,1,0,0) in plane (0, 3). Each has 4 off links. p_A holds ((1,0,0,0), 1), p_B holds ((0,1,0,0), 0), and p_A, p_B share no link.
- R_k(∂p_0) ≡ 10⁻⁶ and R_k(∂p_A) = R_k(∂p_B) ≡ 36787/10⁷ − 10⁻⁶. These are constant, real, gauge invariant, functions of U on 4 links that hold a loop. Every other R_k = 0.
- The norm at every fine link is ≤ 0.0099998 < δ = 1/100. C_k holds: 2δ′ = 0.0202010 ≤ 1/8.
- The six polymers incompatible with {p_0} give a KP left side of 0.0208596 (exact enclosure, width below 10⁻⁶⁰), against a({p_0}) = 2δ′ = 0.0202010. **KP fails.** The two single terms {p_A}, {p_B} alone already exceed a({p_0}).
- On the same input route A's d = (κ/2)#line gives 0.0076741 and route B's d = (κ/2)#links gives 0.0126752, both below a({p_0}).

The failure is first order in δ beyond the leading term. It persists for every small δ: at one off link of p_0 the left side is about δ(1 + δ/(2e))(1 + 4δ) against δ(1 + δ). So "the KP per-polymer corollary with α = t = δ′ and θ = κ" is not available under this reading.

*Reading 2: #γ = the number of objects of γ.* Then d({o}) = κ. C10c's object holds 8 line links and 2 off links, so #Y″ = 4 and e^{κ#Y″} = e^{4κ} > e^{d} = e^κ. The step e^{κ#Y(X)} ≤ e^{d(X)} of the assembly fails.

*What the proofs use.* Route A: d(Γ) = (κ/2)Σ_{o∈Γ}#line(o) and a(Γ) = δ′Σ_{o∈Γ}#off(o) (a sum, not the frozen union #off(γ)). Route B: d(Γ) = (κ/2)Σ_{o∈Γ}|o|, i.e. #γ := ½Σ|o|, and a(Γ) = α|off(Γ)|. Route B states the issue (its gap 3). Route A's table marks "θ = κ: yes" and "α = t = δ′: yes" although both formulas differ from the frozen ones. No number of C_k or c(δ) depends on the choice.

*Fix.* In THEOREMS and CERTIFICATES, define at step k: #γ := ½Σ_{o∈γ}|o| (route B, uniform; yields C_k and c(δ) exactly), or d(γ) := (θ/2)Σ_{o∈γ}#line(o) with a(γ) := αΣ_{o∈γ}#off(o) (route A, split; yields G1*). State in one line that θ = κ is a weight per coarse link, paid at κ/2 per fine link. Then brief question (i) reads "yes" for the stated d.

### F2 (blocking). Brief question (vii): the proved constants are not the frozen ones, and the two routes disagree on C_k

The v2 THEOREMS row requires "an explicit check that the proved constants are exactly the frozen ones". The note outline, section 16(vii), says "a differing constant makes every row resting on it read UNSUPPORTED". Both derivations end "all_equal: false".

- I confirm G1* (section 2.4, 2.6). It needs 2δ′ ≤ κ and gives c*(δ) = e^{−1} for δ ≤ 0.072094 at κ = 1/4. So the frozen C_k (2δ′ ≤ κ/2) is sufficient, not necessary for the method. Route B's table entries "C_k: equal (as the certificate)", "C11: equal", "C12: equal" are true only for route B's d. Route A's entries say "no". The note cannot carry both tables as written.
- Consequences, all CONDITIONAL on G0's δ_1, read with route A's c*:
  - C11, crude 1/64: δ_1 ∈ [0.10165, 0.10166] meets 2δ′ ≤ 1/4 and c* ≤ 0.7719306 < 1. So C11's name, "the crude hypothesis does not map to itself", is false for the method. The engine will still read the frozen test NOT_MET.
  - C12, 1/50: every count vector has δ_1 ≥ 0.072645, and c*(0.072646) ≤ 0.3727351 < 1. So C12's name, "the self-map fails under every count model", is false for the method.
  - C13, C14: the edges 0.01369/0.01370 and 0.01959/0.01960 locate the pinned formula, not G1. C14's clause "β_ind < 0.01960 for every count vector (DERIVED)" is DERIVED only for the pinned formula.
  - C10b: "at most 3 × 10⁻⁵ times c(δ_in)δ_in" holds for c ([2.4995e-5, 2.5060e-5]) and fails for c* ([4.0434e-5, 4.0537e-5]).
  - SCOPE: "NOT_MET above the windows = a failure of this norm and these counts" overclaims for the C_k and c clauses. They are failures of the pinned bookkeeping.
- "The proved constant" is itself not canonical (F5): route A's own c* has slack, and route B's c_♯ and c_B are two choices from one proof. So 16(vii) asks a question with no unique answer.

*Fix (owner decision).* Either (a) keep c and C_k as pinned, rewrite 16(vii) as "the pinned constants are implied by a written proof", and retitle C11, C12, C13, C14 and the SCOPE clause as statements about the pinned uniform bookkeeping (Remark 4.18 of route A); or (b) re-pin to route A's split (C_k: 2δ′ ≤ κ, c*), which moves C07, C08, C10b, C11 to C14, C16 and the regime clause, and needs its own attack. Under (a), the frozen rows stay true and none reads UNSUPPORTED. Under neither option can the freeze ship both tables unreconciled.

### F3 (minor). The v2 THEOREMS row states the corollary with e^{d(γ)}, not e^{d(X)}

v2 writes "Σ_{clusters ∋ γ} |Φ| e^{d(γ)} ≤ |z_γ| e^{a(γ)+d(γ)}". The assembly needs e^{d(X)} on the left. A cluster X = {{o}, {o′}} counted in S_2(o) has Y(X) = Y″(o) ∪ Y″(o′), and e^{κ#Y(X)} can exceed e^{d({o})}. The draft's "e^d" was ambiguous; v2 made it wrong for the use. Both derivations use e^{d(X)}. Fix: write |Φ(X)|e^{d(X)}, with d(X) := Σ_Γ m_X(Γ)d(Γ).

### F4 (minor). The frozen tree-graph clause does not define s(o), ω_o or the links e

"Σ_{Γ∋e}∏ω ≤ t, from Σ_{o∋e}ω_o e^{t s(o)} ≤ t" is read with s(o) = #o by route A and with s(o) = #off(o) by route B. With s(o) = #o and attachments at every link it is the uniform bookkeeping and returns C_k; with s(o) = #off(o) and attachments at off links it is the split and returns 2δ′ ≤ κ. ω_o must be the KP-weighted activity sup|f_o|·e^{a(o)+d(o)}, not the raw sup norm. Fix: define all three in the row, matched to the choice made under F2.

### F5 (minor). A root at e_0 always holds a line link; both bookkeepings keep impossible roots

The root of a term at ℓ contains e_0(ℓ), a line link, so m ≥ 1. Route A's Q takes the supremum over m ≥ 0, and its third entry of c* comes from m = 0. Route B bounds s(o_0) ≤ n where s(o_0) ≤ n − 1 holds. This is slack, not an error. Restricted to m ≥ 1, route A's third entry becomes e^{δ−κ/2}sup_{f≥3}g(f). Then (`g1tg_mge1.py`, search reads on the 10⁻⁹ grid):

- c* = e^{−1} up to δ = 0.077320139 (not 0.072094);
- c* < 1 on all of 2δ′ ≤ κ: at the condition edge 0.111780108, c* ≤ 0.9868670.

So route A's δ_crit* = 0.109530694 is a property of the m = 0 term, and route A's sentence "c*(δ) > e^{−1} for δ ≥ 0.072095" is a property of its formula. With m ≥ 1 the window under the split is set by 2δ′ ≤ κ alone. This feeds F2: no single "proved constant" exists to compare against. Fix: state in both derivations that their constants are one valid bookkeeping, and that m ≥ 1 (route A) and s(o_0) ≤ n − 1 (route B) were not used.

### F6 (minor). "Reproduces inside its bracket" is said of propagated enclosures that stick out

Both derivations propagate c and 2δ′ over the δ_1 bracket and say the frozen value "reproduces". Three propagated upper ends lie outside the frozen brackets:

- C07 c: 0.4450509 > 0.44505 (both routes);
- C11 2δ′: 0.2250767 > 0.22507 (route A);
- C10b, s = 1/2000, c: 0.5951069 > 0.5951 (route A).

At the actual points the frozen values are inside: c(0.0110444507) = 0.4450465; C11's δ_1 = 0.10165304 gives 2δ′ = 0.225060 (synthesis `points.txt`); δ_in = 12e^{3/2}/2000 = 0.0268901 gives c = 0.5950968; δ_in = 12e^{3/2}/4096 gives c = 0.4617425. No frozen row is wrong. Fix: say "reproduces at the row's point", and give the point.

### F7 (minor). C10b's power is stated against the wrong channel

C10b's low_power field says G1 is refuted "only if it underestimates the multi-object term by more than 3 × 10⁴". That ratio, [39905, 40008], is against the whole c(δ_in)δ_in. That includes e^{δ}e^{−4κ}δ_in for the line channel, which C10b's input never uses (its objects all hold off links). The frozen multi-object part at δ_in is e^δ max_n f(n) ≤ 0.2171908. Against it the slack is [1432.1, 1432.5] for the natural output and ≤ 14601 for the projection bound. Against route A's per-root factor for C10b's roots ((f, m) = (2, 4): e^{δ−4κ}(e^{4δ′} − 1) ≤ 0.0441499) it is ≤ 291.2 and ≤ 2968. C10c reproduces: slack ≥ 21.645 at s = 1/8192 and ≥ 12.081 at s = 1/65536 against c, ≥ 11.19 at both against c*, and ≥ 6.82 against route A's per-root factor e^{δ−6κ+4δ′}. Fix: reword C10b's field to the channel it tests. Optional: add the per-root comparison as a sharper falsifier.

### F8 (minor). Route A's table marks two non-identical formulas "yes"

Route A writes "α = t = δ′: yes" with a(Γ) = δ′Σ_o#off(o) (a sum over objects), against the frozen a(γ) = α#off(γ) (the off links of γ, a union). It also writes "θ = κ: yes, with d now explicit" for d = (κ/2)Σ#line. Both are valid choices and both are different formulas. Fix: mark them "valid, different" and resolve under F1.

## 4. The constant tables against the draft

"Mine" is my own enclosure (`g1tg_constants.py`); "pt" means the read at the row's point.

| Item (row) | Frozen | Route A | Route B | Mine |
|---|---|---|---|---|
| e^{−1} | — | [0.3678794411, 0.3678794412] | 0.3678794412 | 0.367879441171 |
| C07 2δ′ | [0.02233, 0.02234] | [0.0223332, 0.0223354] | [0.0223333, 0.0223353] | [0.02233329, 0.02233534]; pt 0.02233421 |
| C07 c(δ_1) | [0.44504, 0.44505] | [0.4450429, 0.4450509] | [0.4450430, 0.4450509] | ends 0.4450430, 0.4450508; pt 0.4450465 (F6) |
| C07 δ_2; Σδ_k | ≤ 4.92e-3; ≤ 0.01991 | 4.91559e-3; 0.0199028 | 4.9156e-3; 0.0199028 | 4.915586e-3; 0.01990272 |
| C08 c(δ_1) | [0.36793, 0.36795] | [0.3679383, 0.3679386] | same | 0.3679383586, 0.3679385463 |
| C10b c(δ_in), 1/2000 | [0.5950, 0.5951] | [0.5950951, 0.5951069] | [0.595095, 0.595107] | pt δ_in 0.02689013: 0.5950968 |
| C10b c(δ_in), 1/4096 | [0.4617, 0.4618] | [0.4617347, 0.4617511] | [0.461734, 0.461752] | pt δ_in 0.01312995: 0.4617425 |
| C10b c_B; c_♯, 1/2000 | — | — | [0.587932, 0.587943]; [0.509131, 0.509143] | pt 0.5879335; 0.5091330 |
| C10c 2δ′; c, 1/8192 (v2) | [0.0739754, 0.0739755]; [0.7118122, 0.7118123] | — | — | 0.07397549; 0.7118123 |
| C10c 2δ′; c, 1/65536 (v2) | [0.0089626, 0.0089627]; [0.3969925, 0.3969926] | — | — | 0.00896262; 0.3969926 |
| C13 c(49/1000); c(1/20) | [0.98248, 0.98249]; [1.0110, 1.0111] | 0.9824885; 1.0110668 | same | 0.9824885; 1.0110668 |
| δ_crit (frozen c) | [0.0496174, 0.0496175] | c⁺ < 1 at 0.049617491, c⁻ ≥ 1 at …492 | [0.0496174910, 0.0496174911] | same two grid reads |
| C14 c(δ_1), 1/64 | [0.38085, 0.38086] | [0.3808522, 0.3808529] | same | 0.3808522431, 0.3808528930 |
| C16 δ_20; osc_20 | [2.30e-9, 2.31e-9]; ≤ 4.35e-7 | 2.30648e-9; 4.34434e-7 | [2.3055, 2.3065]e-9; 4.3443e-7 | 2.306472e-9 (pt 2.305934e-9); 4.344339e-7 |
| C_k edge, 2δ′ ≤ 1/8 | — | 0.058923670 | [0.0589236705, 0.0589236706] | holds at …670, fails at …671 |
| 2δ′ ≤ 1/4 edge | — | 0.111780108 | — | holds at …108, fails at …109 |
| c* = e^{−1} edge | — | 0.072094 / 0.072095 | — | upper 0.3678711 at …094; lower 0.3678798 at …095; f = 6 |
| δ_crit* | — | [0.109530694, 0.109530695], f = 16 | — | same; f = 16 |
| δ_eq (c = c_B) | — | — | [0.0070256343, 0.0070256344] | sign change confirmed |
| c_♯ = e^{−1} edge | — | — | 0.0116995481 | confirmed, n = 9 |
| δ_crit(c_B); δ_crit(c_♯) | — | — | [0.0558087801, …802]; [0.0577661141, …142] | both confirmed |
| C10b ratio to c·δ_in | ≤ 3e-5 | [2.4995e-5, 2.5060e-5]; c*: [4.0434e-5, 4.0537e-5] | 2.506e-5; c_B 2.536e-5; c_♯ 2.929e-5 | frozen-c slack ≥ 39905.8 |

Every frozen G1 value I checked reproduces at its row's point. Every threshold and edge quoted by either route reproduces on its grid. The remaining issues are F2, F5 and F6.

## 5. Answers in this lens

- **(i) Does the KP per-polymer corollary hold with these a(γ) and d(γ)?** With the frozen d(γ) = θ#γ, θ = κ, read literally: no (F1, explicit instance). With route B's #γ := ½Σ|o| and a = α|off(γ)| under C_k: yes, DERIVED. With route A's d = (κ/2)Σ#line and a = δ′Σ#off under 2δ′ ≤ κ: yes, DERIVED. In every case the corollary must carry e^{d(X)} (F3).
- **Tree-graph bound with t = δ′.** Holds in both forms (section 2.3). The frozen form is a special case of route A's lemma once s(o) is defined (F4).
- **Incompatibility after blocking.** Linking through shared off links is correct. Shared line links do not link, and cannot, since lines are not integrated. Disconnected outputs Y(X) are allowed by H_{k+1} and harmless at the next step (section 2.1).
- **Convergence.** Absolute and uniform in V in both routes, with the real logarithm (section 2.7). Nothing depends on N, K or N_p.
- **(vii), in this lens.** The machinery gives a family of valid constants, not one. The pinned c is the uniform bookkeeping exactly (route A, Remark 4.18). The split gives c* < c and a weaker condition. This is an owner decision (F2).

## 6. Scratch files (pre-freeze disclosure)

All under `pkg/attack/g1tg/`. None is an engine and none is evidence.

- `g1tg_constants.py` (sha256 `073ddc129675c048cf085bf96bad27d4bb4cdbdaa64622eba7bacbd759c00b23`), output `g1tg_constants.out` (`efbe58c8348daf480f3a3c36c4c4fd6d07a44845e6b436375a728dbb87663996`): my own enclosures of c, c* (with and without m ≥ 1), c_B, c_♯, every threshold of both routes, and the row values of section 4.
- `g1tg_literal_d.py` (`fd8e082e5290da83df64e457aebe3cff8d548f22741468d5d75a9327f5b2983f`), output `g1tg_literal_d.out` (`12fbc28c5c51e8c7b075ea28e4f33ce4cb98a07912f3b9f0471b5ae056d5fd97`): the F1 instance, with the geometry asserted from coordinates on (ℤ/8)⁴.
- `g1tg_mge1.py` (`2151b8c666b860e02245e4b3c2deb635c6562c5fcc9ca8d3233614ca2ec3d7b9`), output `g1tg_mge1.out` (`ec3d5ec417a0a595551c7a57bff0b99dac230e8fb8cd4417b41ea85185b23208`): the F5 edges.
- `g1tg_power.py` (`e533feb20cbbac1e76c76ba7731b06446e4df45cdf747819619386868061cf2a`), output `g1tg_power.out` (`c9712d144f27f5d3fca2d4514ad228aeaab71435410f9f19d23f608c98a8620c`): the F7 ratios.

All eight hashes are also in `g1tg/SHA256SUMS`, written after the last edit.

### References

- R. Kotecký and D. Preiss, Cluster expansion for abstract polymer models, Comm. Math. Phys. 103 (1986) 491–498. REPORTED.
- O. Penrose, in *Statistical Mechanics: Foundations and Applications*, ed. T. A. Bak, Benjamin (1967) 101–109. REPORTED.
- Repo: NOTE-YM4-03-ONE-SCALE-BLOCKING.md (Lemma 3, Theorem 4, Proposition 2); NOTE-YM4-03C-BLOCKED-ACTION.md §2 (Lemma A), §6 (Lemma B).
