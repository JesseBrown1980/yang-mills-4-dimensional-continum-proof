# YM4-03C: the blocked SU(2) action at b = 2 in four dimensions, through β¹⁰

**Status: the prediction commit, on the operator's word of November 6, 2026: "GO. I approve the prediction-first computation for the four-dimensional SU(2) blocked action." Written for the seat ACER-CLAUDE-FABLE5 by the second seat's prediction lane, from main at `9e1cc06`. This commit holds the definitions (sections 1 to 6), the predictions in [`PREDICTION-YM4-03C.hbp`](PREDICTION-YM4-03C.hbp) with their derivations (section 7), the operator's three gates as acceptance criteria (section 8), the plan of the engine as text (section 9), and small exact checks of the facts the rows rest on, in [`reviews/fable5-ym4-03c-prediction/`](../reviews/fable5-ym4-03c-prediction/) (section 10). The engine, its receipt and the read of every row come in the next commit. DERIVED: P1, P3, P4, P5, P7 through β¹⁰, P8, P8c, P9, P10a, and the spin clause of P13. CONJECTURE: P6, the chair; P7 at β¹⁴; P10b; P11; P12; the rest of P13. MEASURED: 52 checks with 0 failed in `derive_checks.py`, with its two earlier runs kept beside it. OPEN: a local polymer bound uniform in the volume, the weak-coupling renormalization problem, and the mass gap and the continuum in d = 4.**

Numbering. P1 and P3 to P10 follow the attack lane's corrected list as relayed to this lane; the text of its P2 is CANNOT_SEE here. P8c, P11, P12 and P13 are this lane's rows, marked `origin=this_lane`, and P10 is split into P10a and P10b. The operator's second approval of the day, section-specific sabotage replay for CI, runs as its own pull request.

## 1. The target

```text
S_eff = constant + sum_{n=1}^{10} beta^n S_n + O(beta^11)
```

on the coarse lattice of the one-scale map B of [YM4-03](NOTE-YM4-03-ONE-SCALE-BLOCKING.md) at b = 2, for SU(2) with the Wilson weight w_β(g) = exp(−β(1 − a(g))), a(g) = ½ Re Tr g, in d = 4, with d = 3 as a second dimension for every row that depends on d. Each S_n is a finite sum over coarse translates and rotations of the named functionals of section 4, with exact rational coefficients. The rows predict this shape:

```text
S_1 = S_2 = S_3 = S_5 = S_7 = S_9 = 0                                    P3, and Theorem 9 below order 4
S_4  = -(1/128)       sum_P chi_1/2(V_P)                                 P1, DERIVED
S_6  = +(1/768)       sum_P chi_1/2(V_P)                                 P4, DERIVED
S_8  = -(1/1536)      sum_P chi_1/2(V_P) + (19/884736) sum_P chi_1(V_P)  P5, DERIVED
S_10 = +(467/2211840) sum_P chi_1/2(V_P) - (7/884736) sum_P chi_1(V_P)
       - (3/524288)   sum_chairs chi_1/2(V_chair)                        P11, P12, P6, P13: CONJECTURE
```

The first non-plaquette interaction, by these rows, is the chair at β¹⁰ (P6). The first plaquette term outside the fundamental Wilson form is χ₁(V_P) at β⁸ (P5).

## 2. The blocking map and the gauge

The fine lattice is Λ_f = ∏ ℤ/(2L_i), the coarse lattice Λ_c = ∏ ℤ/L_i, coarse sites at even fine coordinates, and (BU)_μ(x′) = U_μ(2x′) U_μ(2x′ + e_μ). The two fine links of a coarse link ℓ = (x′, μ) are its **line links**, at **positions** 0 and 1; every other fine link is an **off link**. ρ(V) is the density of Theorem 4 of YM4-03.

**The gauge.** The fine midpoint m_ℓ = 2x′ + e_μ has an odd coordinate, so it lies on one coarse line, and its only line links are the two positions of ℓ. The gauge transformation at m_ℓ by g = U_0 sends the line to (U_0, U_1) = (1, V_ℓ) with V_ℓ = U_0U_1, and moves the off links at m_ℓ. Haar measure and ∏_p w(U_p) are invariant under it, so

```text
rho(V) = (1/Z) integral over the off links of prod_p w(U_p),   every line at (1, V_l).
```

Every off link is integrated by product Haar, and every line link is fixed. With X = Σ_p a_p and E_V that conditional Haar expectation, Z e^{βN_p} ρ(V) = E_V[e^{βX}].

**Lemma A (one position).** Let T(V) be the integral over the off links of a product of class functions of plaquettes, lines at (1, V). If no plaquette of T holds position 0 of ℓ, then T is constant in V_ℓ and equals the same integral with position 1 integrated as an off link. If no plaquette holds position 1, T holds V_ℓ nowhere.

*Proof.* The gauge transformation at m_ℓ by h moves position 1 to hV_ℓ and the off links at m_ℓ by h, which T integrates by Haar, and it moves position 0, which T leaves out. So T(V) = T(V with V_ℓ → hV_ℓ) for every h, and T equals its Haar average in V_ℓ. ∎

## 3. The effective action and its sign

```text
S_eff(V) = -log rho(V) + const,   const chosen so that the coarse Haar mean of S_eff is 0,
log rho(V) = -log Z - beta N_p + sum_{n>=1} beta^n kappa_n(V) / n!,
S_n(V) = -(kappa_n(V) - integral kappa_n) / n!,
```

with κ_n(V) the n-th cumulant of X under E_V. A coefficient c of a basis function F in log ρ is −c in S_eff. The rows give each coefficient in log ρ and the note gives S_n with its sign.

## 4. The coarse spin-network basis, fixed

Functions of V ∈ SU(2)^{coarse links} that are invariant under coarse gauge transformations, as ρ is by Theorem 4. For each coarse link ℓ and spin j, the projection Π_ℓ^j onto the span of the spin-j matrix elements of V_ℓ is canonical; the projections of different links commute, and the joint components {j_ℓ} split every such function into orthogonal parts. A component holds intertwiners at coarse sites. Every functional named below has a one-dimensional component, with two- or three-valent coarse sites, so the named functionals fix the basis through β¹⁰. A four-valent coarse site takes the recoupling in which the two links of the lexicographically lower coarse plaquette couple first; this is fixed now so that an extension reads in the same basis, with coarse plaquettes ordered by base site lexicographically, then by direction pair; through β¹⁰ P13's zeros are statements about whole joint components {j_ℓ}, the same in every recoupling basis.

**Readout.** The coefficient of a basis function F in a function f is c_F = ⟨F, f⟩/⟨F, F⟩ in coarse Haar. ⟨χ_j(V_C), χ_j(V_C)⟩ = 1 for a simple coarse loop C.

| Functional | Definition |
|---|---|
| χ½(V_P) | the trace of V_P = V_μ(x′) V_ν(x′+μ) V_μ(x′+ν)⁻¹ V_ν(x′)⁻¹, the same for either orientation since χ½(g⁻¹) = χ½(g) |
| χ₁(V_P) | χ½(V_P)² − 1 |
| the chair | χ½ of the 6-link loop x′ → x′+ν → x′+ν+μ → x′+μ → x′+μ+λ → x′+λ → x′ around P = (μ, ν) and Q = (μ, λ) at x′, ν ≠ λ, which share ℓ = (x′, μ); spin 0 on ℓ |
| the 1×2 rectangle | χ½ of the 6-link loop around two coplanar coarse plaquettes sharing ℓ |
| N1_PQ | χ½(V_P)χ½(V_Q) − ½χ½(V_loop) for P, Q sharing ℓ, the spin-1 component on ℓ; ⟨N1, N1⟩ = 3/4 |
| a disjoint pair | χ½(V_P)χ½(V_Q) for P, Q with no common coarse link |
| the twisted hexagon | χ½ of x′ → +μ → +ν → +λ → −μ → −ν → −λ |
| a tube | χ₁(V_ℓ) for ℓ in a direction of coarse side 1 |

Per coarse site, by orbits under the group of section 5, MEASURED in `derive_checks.py`: 6 coarse plaquettes (stabilizer 64), 48 chairs (stabilizer 8, so 12 per coarse link), 12 rectangles (32), 16 twisted hexagons (24), 12 parallel pairs at coarse distance 1 (32).

## 5. Lattice-size conditions and symmetry

**Sides.** Every coarse side L_i ≥ 3, so fine sides ≥ 6. The smallest lattice is fine 6⁴, with 7776 plaquettes, where the multisets of 10 plaquettes number C(7785, 10) = 2.24 × 10³². A term that moves with V on a winding coarse loop of L coarse links holds 2L disjoint fine slices across that direction, each with at least min(b, 4) = 2 nontrivial plaquettes, by step (c) of Theorem 9, so at least 4L of them. At L = 3 nothing wraps through β¹¹. The bound 4L = 12 is met only by flat fillings of coarse plaquettes along the loop, joined on line links only, such as the strip of 12 plaquettes between two adjacent parallel winding coarse lines: it enters ρ at β¹² with 2⁻²¹ on χ½(V_{P₁})χ½(V_{P₂})χ½(V_{P₃}), and its joint cumulant is 0 by Lemma B, so log ρ holds no winding term through β¹³ at L = 3. An extension of G2's partition-function series to β¹² takes L ≥ 4. Closed fine surfaces that wrap hold at least 24 plaquettes at fine side 6.

**Symmetry.** The coarse-compatible group is the coarse translations, fine translations by 2ℤ⁴, times the 384 signed permutations about a coarse site; it maps coarse sites to coarse sites and lines to lines, and ρ is invariant under it; fine translations by a vector with an odd entry move coarse sites to midpoints and other fine sites. A class is an orbit; its canonical form is the lexicographically least image of its plaquette set, translated so that its least site is the origin, and keyed by the hash of that form.

## 6. The counting rule

**Moments and cumulants.** [βⁿ] log E_V e^{βX} = Σ_{|M|=n} κ(M)/∏_p m_p!, over multisets M of plaquettes with multiplicities m_p, where κ(M) is the joint cumulant of the a_p over the copies in M under E_V.

**Lemma B (rule (a), at the level of distinct plaquettes).** κ(M) = 0 unless supp(M) is one plaquette, or supp(M) is connected through off links and every off link of each of its plaquettes lies in at least two distinct plaquettes of supp(M).

*Proof.* If an off link e of p ∈ supp(M) lies in no other plaquette of supp(M), then given every other link, U_p = A e^{±1} B with e Haar and free of the rest, so U_p is Haar and independent of all the other plaquettes of M, and a joint cumulant whose variables split into two independent groups vanishes. If supp(M) splits into two parts sharing no off link, the parts are functions of disjoint sets of independent links. ∎ The multiplicities enter through 1/∏ m_p! and the cumulant alone; the pruning reads distinct plaquettes, as Lemma 9a of YM4-03 does.

**Lemma C (parity).** κ(M) = 0 when an off link has odd total multiplicity Σ_{p∋e} m_p, or when the two positions of a line have total multiplicities of different parity.

*Proof.* U_e → −U_e on one off link, or on both positions of one line, keeps Haar and BU and sends a_p → −a_p on the plaquettes holding it; the joint cumulant is multilinear. ∎ P3 is the same argument with the staggered sign of section 7.2 on every link at once.

**Recursion.** For a multiset M with a marked copy x, μ(M) = Σ_S c(S) κ(S) μ(M ∖ S) over sub-multisets S holding x, with c(S) = ∏_p C(m_p − [p = p_x], s_p − [p = p_x]) the ways to choose S's copies, and κ(M) = μ(M) − Σ_{S ≠ M} c(S) κ(S) μ(M ∖ S). μ factors over the parts that Lemma B separates.

**The fold through McKay powers.** a^m = 2^{−m} Σ_j N_m(2j) χ_j, with N_m(n) = (A^m)_{0,n} on the McKay graph of SU(2), n → n ± 1, the multiplicity of spin n/2 in (½)^{⊗m}. For a support S and spins (j_p), Φ_S(j; V) = E_V[∏_p χ_{j_p}(U_p)] serves every multiplicity vector on S:

```text
mu(m) = 2^{-|m|} sum_{(j_p)} prod_p N_{m_p}(2 j_p) Phi_S(j; V).
```

A spin j_p = 0 drops p, and Φ vanishes unless its nontrivial plaquettes satisfy Lemma B and the spins at each off link admit an invariant.

**The polymer form.** Equivalently, e^{βa(g)} = c₀(β)[1 + Σ_{j≥½}(2j+1) t_{2j+1}(β) χ_j(g)] with t_n = I_n/I_1, a series of parity n − 1 in β. A polymer γ is a support connected through off links with spins j_p ≥ ½, of activity z_γ(V) = ∏_p (2j_p+1)t_{2j_p+1} · Φ; two polymers are compatible when they share no off link, and ρ(V) is proportional to Σ ∏ z_γ over compatible families, since E_V factors over parts with no common off link. log ρ is the cluster expansion: z_γ, −z_γz_γ′ for each incompatible pair, −½z_γ² for γ with itself, and so on. Section 7 derives in this form, and it is route S of G3.

## 7. Derivations

### 7.1 P1, order 4

Theorem 9 of YM4-03: E_V[Xⁿ] is constant in V for n < 4, and E_V[X⁴]/4! = κ + 2⁻⁷ Σ_P χ½(V_P), so S_1 = S_2 = S_3 = 0 and S_4 = −(1/128) Σ_P χ½(V_P). The receipt's rows `YM4_03_FIRST_DEPENDENCE` read −24359/438048 on fine 2×2×2×2 and −5693581/33434856 on fine 4×2×2×2, at V_a of `quaternion_pool(2026, 40)` against V = 1, with V at position 0 and at position 1; the engine reads both lattices at order 4 as its first benchmark. DERIVED, and MEASURED in YM4-03.

### 7.2 P3, odd orders

U_μ(x) → (−1)^{s_μ(x)} U_μ(x) with s_μ(x) = Σ_{ν<μ} x_ν mod 2. Fine sides are even, so s is defined on the torus. A line link (x, μ) has every x_λ even for λ ≠ μ, so s = 0 on it, and BU is kept. On a plaquette with μ < ν, s_μ(x + e_ν) = s_μ(x) and s_ν(x + e_μ) = s_ν(x) + 1, so U_p → −U_p and a_p → −a_p for every p. Haar is kept, so X and −X have one law under E_V, and log E_V e^{βX} is even in β for every V. S_n = 0 for every odd n, for every functional. DERIVED.

### 7.3 The half-integer set

**Lemma D.** In a polymer, let H be its plaquettes of half-integer spin and I those of integer spin. (1) H holds every off link an even number of times, since a tensor product with an odd number of half-integer factors holds no invariant. (2) So the fine boundary of H lies on line links, and since m_ℓ meets only the two positions of ℓ, it is 2C′ for a coarse 1-cycle C′, both positions of each coarse link of C′. (3) By Lemma A the polymer's dependence on V_ℓ has half-integer spin exactly on the coarse links of C′. (4) Its order in β is Σ_p 2j_p plus an even number, at least |H| + 2|I|.

On coarse sides ≥ 3 through β¹¹ the sets that enter fit in a box, where every closed mod-2 surface bounds, so H = F ⊕ ∂C for a fixed filling F of C′ and a 3-chain C. A cube has 6 faces and shares at most one with a plane, so for C′ = ∂P, |F_P ⊕ ∂C| takes the values 4, 8, 10 and more. MEASURED in a window of ℤ⁴ (section 10): 1 set at size 4, 16 at 8, and at 10 the 16 domino disks, the 16 sets in which one cube shares one off link of F_P, and cube sets joined to F_P through line links or apart from it.

Every plaquette outside F_P that holds an off link of F_P (one of its four internal links, from the center to a side midpoint) leaves the plane of P, and its other three links have an odd coordinate in that plane, so they are off links outside F_P; and two distinct plaquettes share at most one link.

### 7.4 P4, order 6

Polymers with half-integer spin on ∂P at order 6: F_P at cost 4 with integer spin of total cost 2, so one spin-1 plaquette q, or F_P with spins (3/2, ½, ½, ½). A q through an internal link of F_P has three more off links in no other nontrivial plaquette; a q away from the internal links has at least two off links held by nothing else. Spin 3/2 beside spin ½ on an internal link needs a third plaquette there, as 3/2 ⊗ ½ holds no invariant. So F_P alone, 2t₂⁴χ½(V_P), whose β⁶ term is −1/768. Clusters: the smallest polymer that holds no V, a cube with 4t₂⁶, has order 6, so a cluster holding F_P has order at least 10. Other functionals: a half-integer set on the chair or the rectangle holds at least 8 plaquettes, and a spin-1 loop at least 4 spin-1 plaquettes, order 8. So S_6 = (1/768) Σ_P χ½(V_P), in d = 4 and d = 3. DERIVED.

### 7.5 P5, order 8

Half-integer sets on ∂P of size at most 8: F_P and the 8(d − 2) one-cube bumps, 16 in d = 4 and MEASURED as 16 disks. A disk of F spin-½ plaquettes, every off link in exactly two of them, integrates to 2t₂^F χ½ of its boundary: merging two plaquettes along a free link gives χ½(AB)/2, as in the proof of Theorem 8, and a disk has F − E_int + V_int = 1. A bump on a corner plaquette holds the corner cube's transverse link at the coarse site, a line link of another coarse link at one position, which Lemma A integrates. Decorations of F_P at cost 4, two spin-1 plaquettes or one of spin 2: a decoration through an internal link has three more off links and the other decoration holds at most one of them; a decoration away from the internal links has at least two off links that only the other could hold, and it holds at most one. Spin 3/2 on one face needs a decoration at each of its two internal links. Spin 1 on all of F_P gives 3t₃⁴χ₁(V_P), 1/110592 at β⁸. The cluster expansion at β⁸ adds the self-term −½z_{F_P}² = −2t₂⁸χ½(V_P)² = −2t₂⁸(1 + χ₁(V_P)), −1/32768 on χ₁; fillings of two coarse plaquettes share line links only and are compatible.

```text
chi_1/2(V_P):  1/6144 + 16 * 2^-15 = 1/1536        (d = 3: 1/6144 + 8 * 2^-15 = 5/12288)
chi_1(V_P):    1/110592 - 1/32768  = -19/884736    (both d)
```

Other functionals at β⁸: the chair's and the rectangle's half-integer sets of size 8 are F_P ∪ F_Q, which meet on line links only, so they are two compatible polymers, outside log ρ. So S_8 holds the two plaquette functionals alone. DERIVED.

### 7.6 P6, the chair

Half-integer sets with the chair's fine boundary, connected through off links, of size at most 10: F_P ⊕ F_Q ⊕ ∂C with C the corner cube at position 0 of ℓ, at position 1, or both. MEASURED: 3, each a disk of Euler characteristic 1, touching position 1 of ℓ, position 0, and neither; F_P ∪ F_Q at size 8 meets on line links only. Each disk gives 2t₂¹⁰χ½(V_chair), and since each holds at most one position of ℓ, Lemma A puts it wholly in the spin-0 component on ℓ. A spin-1 plaquette holding an off link of each filling meets them at m_ℓ, in the plane of their two transverse directions, and its two far links lie in no other plaquette. Clusters: F_P and F_Q are compatible. So

```text
[beta^10] chi_1/2(V_chair) in log rho = 3 * 2^-19 = 3/524288,   48 chairs per coarse site,
```

the Z2 count 3 of Proposition 11 times the SU(2) disk weight. N1_PQ needs both positions of ℓ held in one connected polymer, and the three disks hold one or none, so it needs a decoration too, order at least 12. CONJECTURE, as the operator's direction holds it, and kept in its own row apart from P4 and P5: the count ranges over the classes this lane listed, and the engine's classes read it exhaustively.

### 7.7 P7, the 1×2 rectangle

MEASURED in the window by both methods: the sets with the rectangle's fine boundary that are connected through off links number 0 at every size up to 12, and 8 at size 14, the domino disks across ℓ. A spin-1 plaquette holding an off link of each filling would hold the two links at m_ℓ along +ν and −ν, which no plaquette holds together, and for the same reason no cube shares an off link with both fillings. So the coefficient is 0 through β¹⁰, DERIVED. At β¹⁴ the 8 disks give 8 · 2⁻²⁷ = 1/16777216, plus whatever decorations and clusters of order 14 add: CONJECTURE, registered for a later extension.

### 7.8 P11, order 10 of χ½(V_P)

| Part | Count in d = 4 | Contribution |
|---|---|---|
| the planar series 2t₂⁴ at β¹⁰ | 1 | −79/4423680 |
| the bumps' 2t₂⁸ at β¹⁰ | 16 | −1/6144 |
| domino disks, 2t₂¹⁰ | 16 | +1/32768 |
| a cube on a face f: the polymer with f at spin 1, minus the cluster −z_{F_P}z_C | 16 | 16(2⁻¹⁸ − 2⁻¹⁷) = −1/16384 |
| a cube on one off link e of F_P, with no face of it | 16 | 0 |
| total | | **−467/2211840** |

The cube on a face: F_P's three other faces and the cube's five other faces at spin ½, f at spin 1. The cube's eight inner links integrate to 2t₂⁵χ½(U_f); the three faces of F_P to 2t₂³χ½(W); χ½(U_f)χ₁(U_f) = χ½(U_f) + χ_{3/2}(U_f), and along the two links U_f shares with W the 3/2 part integrates to 0 against χ½(W) and the ½ part to ½χ½(V_P). So the polymer is 3t₃ · 2t₂⁵ · 2t₂³ · ½ χ½(V_P) = 6t₃t₂⁸χ½(V_P), 2⁻¹⁸ at β¹⁰, against the cluster 8t₂¹⁰, 2⁻¹⁷.

**Lemma E (one shared off link).** If polymers γ, γ′ share only the off link e, and at an end s of e every other link of γ is an off link outside γ′, then the polymer γ ∪ γ′ has activity z_γz_γ′. *Proof.* Integrating γ's other links at s first leaves a function of e invariant under e → he by the gauge transformation at s, so a constant, equal to z_γ. ∎ The cube on one off link meets F_P at the center, where F_P's three other internal links are free, so its joint activity cancels the cluster term exactly.

In d dimensions the bumps, the domino disks and the cubes on a face hold 8(d − 2) each, and the cubes on one off link 16·C(d − 2, 2), 16 at d = 4 and 0 at d = 3, adding 0; the total is −79/4423680 − 19(d − 2)/196608, −1013/8847360 at d = 3. CONJECTURE: the table ranges over this lane's classes, with the decorations of cost 6 excluded by the argument of 7.5, and the engine's exhaustive classes read it, part by part where its classes match these.

### 7.9 P12, order 10 of χ₁(V_P)

The planar value of 3t₃⁴ − 2t₂⁸ at β¹⁰ is 7/884736. The four-dimensional polymers of order 10 above carry half-integer spin on ∂P, and spin 1 on all four coarse links of P needs every position held by an integer coupling, which the spin-1 filling gives at cost 8 and a decoration by one more spin-1 plaquette leaves dangling. So 7/884736, CONJECTURE.

### 7.10 P8 and P8c, the Z2 control

For Z2 with w = 1 + uσ, Proposition 11 as corrected in YM4-03: the perpendicular pair reads 3u¹⁰ and the parallel pair at coarse distance 1 reads 0 through u¹², MEASURED there by surface enumeration on 8³, 8⁴ and 12³. P8c: ρ ∝ Σ_M u^{|M|}V^{∂M}, and the coefficient of W_P in log ρ through u¹⁰ is r_P = u⁴⟨u^{−2k(Z)}⟩ over closed surfaces Z, k the number of faces Z shares with F_P. A cube on a face gives u⁸ − u¹⁰, a domino gives u¹⁰, a cube sharing no face cancels, so r_P = u⁴ + 8(d − 2)u⁸ + 0·u¹⁰ + O(u¹²). DERIVED. The engine runs these on its own cluster classes before any SU(2) row.

### 7.11 P10, winding and tubes

P10a is section 5's count, DERIVED. P10b, on fine 2×6×6×6, coarse 1×3×3×3: around each coarse link ℓ in direction 0, the 4 walls over a unit square with ℓ on a corner, along both fine positions, form a torus of 8 plaquettes; there are 2(d − 1)(d − 2) = 12 such squares; cut along ℓ the torus is an annulus, F − E_int + V_int = 0, so it integrates to t₂⁸χ½(V_ℓ)² = t₂⁸(1 + χ₁(V_ℓ)). So the coefficient of χ₁(V_ℓ), spin 0 elsewhere, is 12 · 2⁻¹⁶ = 3/16384 at β⁸, and 0 below, since the plaquette terms there carry spin ½ on ℓ. CONJECTURE: the formula 2(d − 1)(d − 2) was read on lattices with b ≥ 5.

### 7.12 P13, the β¹⁰ functionals

Through β¹⁰ the basis functions with a nonzero coefficient are χ½(V_P), χ₁(V_P) and the chair. Spin j ≥ 3/2 on a coarse link needs plaquettes of total spin at least j at each of its two positions, and a fine plaquette holds at most two line links, so the cost Σ2j_p is at least 2Σ_ℓ j_ℓ; a spin network with j ≥ 3/2 on ℓ carries spin ≥ 3/2 across each of the three disjoint cuts at graph distance 1, 2, 3 between ℓ's ends, so Σ_ℓ j_ℓ ≥ 6 and the cost is at least 12; a cluster reaches spin 3/2 on ℓ only from polymers costing at least 4 per spin ½ there, so at least 12: DERIVED. The rectangle is P7. N1_PQ is 7.6 and 7.7. A disjoint pair needs a cluster or a polymer joining two fillings that share no off link, order at least 14. A simple coarse loop of length at least 8 spans at least 3 coarse plaquettes, 12 fine ones. The twisted hexagon spans 3 coarse plaquettes and needs connections. CONJECTURE for the clauses without a derivation.

## 8. The three gates

**G1, Haar exactness.** Every average over the 120 elements of 2I runs link by link, and before each one the engine writes that link's degree: the sum of the multiplicities of the term's plaquettes on that link, with the boundary values and any inserted coarse functional counted. The average runs at degree ≤ 11; a term above goes to exact SU(2) integration. 2I is a spherical 11-design, Σ_{2I} χ_j = 0 for j = ½ to 11/2 and 120 at j = 6, MEASURED here in ℤ[φ]; so its average equals Haar on every polynomial of degree ≤ 11 in one link's entries, and integrating link by link keeps each remaining link's degree. The exactness of a row for continuous SU(2) rests on its written degrees, with the maximum on the row. The same for 2T at degree ≤ 5. Negative controls, P9: E[χ½⁶] reads 5 for SU(2) and 6 for 2T, and E[χ½¹²] reads 132 for SU(2) and 133 for 2I.

**G2, connected coefficients.** The engine files two series for each class: ρ(V)/∫ρ, the blocked partition function normalized, and log ρ, with each cancellation between them written. Rows to read: at β⁸, ρ/∫ρ holds 2⁻¹⁴ for each disjoint pair χ½(V_P)χ½(V_Q) and 1/110592 for χ₁(V_P), and log ρ holds 0 and −19/884736; the difference on χ₁ is the self-cluster −2t₂⁸ = −1/32768. Every class carries its orbit size under the group of section 5, its stabilizer and its multinomial 1/∏ m_p!, and the per-site counts of section 4 are the check on them.

**G3, an independent first non-plaquette term.** The chair's coefficient by two routes with separate code: the engine's cumulants, and a count of the surfaces with their character integrals (section 7.6). Operator: χ½ of the 6-link chair loop, spin 0 on the shared link. Sign: +c in log ρ, −c in S_10. Predicted: 3/524288. Lattice: coarse sides ≥ 3, in d = 4 and d = 3. Every failed prediction stays in the prediction file and in this note.

## 9. The engine, as a plan

| Part | It computes | The trick | The enumeration it replaces |
|---|---|---|---|
| E0 | the Z2 control, P8 and P8c | the same classes as E2 with Z2 integrals, which are parity counts | a separate Z2 code path |
| E1 | lattice, lines in the gauge (1, V), the group of section 5, canonical forms keyed by hash | coarse translations × 384 | every translate and rotation |
| E2 | supports connected through off links, closed under Lemma B, grown from a seed plaquette on the target's lines up to cost 10 | Lemmas B and C prune at the level of distinct plaquettes; a support whose open off links cannot close within the remaining cost stops | C(7785, 10) = 2.24 × 10³² multisets on fine 6⁴ |
| E3 | multiplicity vectors on each support, with 1/∏ m_p! | the McKay fold: one Φ_S(j; V) per support and spin pattern serves every vector | an integral per multiset |
| E4 | Φ_S(j; V) exactly, at rational V | link-by-link SU(2) integration, by the character merges of section 7 where a link has two plaquettes and exact recoupling where it has three or four; 2I averages in ℚ(√5) as the second route inside degree 11 under G1, where the √5 parts cancel, a check of its own | 120^k products over k free links |
| E5 | cumulants by the recursion, and the cluster expansion of the polymer form as route S | both series of G2 per class | a log taken on the whole partition function |
| E6 | the readout c_F in the basis of section 4, by exact solves at rational V with more sample points than unknowns and the residual filed as 0, or by the exact isotypic projection | the per-class functional list of section 7 | integration over V, which would raise G1's degrees |
| E7 | the chair by route S in separate code, for G3 | surfaces and disk weights | |
| E8 | receipts through HBI → HBP → SHA → SH → HASH | | |

Odd orders are skipped by P3, with β⁵ computed as its check. The planar corrections come from the t_n series. Every run stays under 20 minutes, with at most two heavy processes on the shared machine. The frozen blind runs stay untouched. The engine commit files the counts it reaches against those it replaces, measured, as the account of the computations avoided.

## 10. The checks of this commit

[`derive_checks.py`](../reviews/fable5-ym4-03c-prediction/derive_checks.py), integers and integer pairs only, writes [`DERIVE-CHECKS.hbp`](../reviews/fable5-ym4-03c-prediction/DERIVE-CHECKS.hbp): 52 checks, 0 failed, about 21 seconds (20540 ms in RECORDS.hbp) and 250 MB under WSL Python 3.12. MEASURED:

- **McKay route.** N_m(0) are the Catalan numbers. t₂ = β/4 − β³/96 + β⁵/1536 − β⁷/23040 + 13β⁹/4423680 and t₃ = β²/24 − β⁴/384 + β⁶/5760 − 13β⁸/1105920, from N_m alone. 2t₂⁴ and 3t₃⁴ − 2t₂⁸ through β¹² equal the decide and attack lanes' Bessel routes: 1/128, −1/768, 1/6144, −79/4423680, 769/424673280 and −19/884736, 7/884736, −373/212336640.
- **Designs.** In ℤ[φ], Σ_{2I} χ_j reads 120 at j = 0, 0 at j = ½ to 11/2, and 120 at j = 6; Σ_{2T} χ_j vanishes for j = ½ to 5/2 and reads 24 at j = 3. E[χ½^m] by closed walks on affine E8 and E6 equals the class sums, agrees with SU(2) through m = 11 and m = 5, and reads 133 against 132 at m = 12 and 6 against 5 at m = 6.
- **Surfaces**, in windows of ℤ⁴ from 352 to 672 cubes, every F ⊕ ∂C with at most three cubes, and the defect-repair walk of `count_surfaces` in the YM4-03 test as a second method. Plaquette, size ≤ 10: 1, 16 disks at 8, and at 10 16 disks, 16 one-off-link cube sets of Euler characteristic 2, and 320 sets in which a cube meets F_P at a line link (64), at one site (64) or nowhere (192). Chair, size ≤ 10: the two fillings at 8 and 3 disks at 10, touching positions (), (0), (1) of ℓ. Rectangle, size ≤ 14: no set connected through off links below 14, and 8 disks at 14. Every set the walk reaches lies among the chains, the two hold the same disks, and on the chair and the rectangle the same connected sets; on the plaquette the walk reaches 8 of the 16 one-off-link cube sets, since it adds plaquettes on the lowest odd edge only.
- **Arithmetic of the rows**: P4, P5 at d = 4 and d = 3, χ₁ at β⁸, P6, P7 at β¹⁴, P10b, P11 by parts at d = 4 and d = 3, P12, and G2's numbers.
- **Orbits** of section 4, with the 384 signed permutations.

The two earlier runs stay beside the script. [`FIRST-RUN.hbp`](../reviews/fable5-ym4-03c-prediction/FIRST-RUN.hbp) compared every set whose edge components all touch the boundary, and read 40 against 96 at size 10, since the walk reaches 8 of the 64 sets a cube joins along one line link. [`SECOND-RUN.hbp`](../reviews/fable5-ym4-03c-prediction/SECOND-RUN.hbp) compared all sets connected through off links and read 41 against 49 on the plaquette. Both are failed comparisons of the two methods, with the counts of each method unchanged in the third.

## 11. The evidence chain and the pin

In [`reviews/fable5-ym4-03c-prediction/`](../reviews/fable5-ym4-03c-prediction/): `INDEX.hbi`, one row per artifact with its bytes, sha256 and 16-hex SH; `RECORDS.hbp`, what each artifact is and how it was made; `SHA256SUMS` over the folder's files; and `SEAL.hbp`, the sha256 of `SHA256SUMS` and of `INDEX.hbi` and the sha256 of the two concatenated. The 26 rows of the prediction, as pushed in this commit, hash to `ddd7b779d60e04f2dca1f866ff56f1194107dd10a8470088dee4f0ab3336b881` by `head -n 26 docs/PREDICTION-YM4-03C.hbp | sha256sum`, and [`blocked-action-b10.yml`](../.github/workflows/blocked-action-b10.yml) holds that pin, as `one-scale-blocking.yml` holds YM4-03's. Later rows, attempts and corrections, go after row 26, so every earlier row stays a byte prefix.

## 12. OPEN

A local polymer bound that replaces the volume-dependent remainder of Corollary 10, the next target after this stage; the weak-coupling renormalization problem; the mass gap and the continuum in d = 4.
