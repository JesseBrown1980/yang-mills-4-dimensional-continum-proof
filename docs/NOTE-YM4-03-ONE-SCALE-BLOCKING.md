# YM4-03: one-scale blocking, the exact pushforward, and what it induces

**Status: DERIVED by the seat ACER-CLAUDE-FABLE5 on November 5, 2026, on the operator's word: "Agreed. Go after that." Its exact tests are registered first in [`PREDICTION-YM4-03.hbp`](PREDICTION-YM4-03.hbp), pushed before the test existed. The second seat's attack and GPT-6's reading are OPEN.**

**Scope:** one finite periodic lattice, any compact group G and any bounded class weight, with SU(2) and the Wilson weight as the case of interest. Sections 5 and 7 read one family as the spacing falls in two dimensions. In three and four dimensions the uniform bound stays OPEN: section 7 states the hypothesis that would give it.

[Issue #3](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/3) asks for five things: a proof of covariance and normalization, an exact closed-loop identity on a noncommuting family, independent checks with broken conventions, an explicit effective action or a certified truncation for one finite block, and a record of the nonlocal terms blocking induces. Sections 2 and 3 carry the first two, the test carries the third, section 5 and Corollary 10 carry the fourth, and section 6 carries the fifth.

## 1. Setting

Fine lattice Λ_f = ∏ ℤ/(bL_i), coarse lattice Λ_c = ∏ ℤ/L_i, in d dimensions, with b ≥ 2 and L_i ≥ 1. The issue names b = 2, and the tests also run b = 3. Coarse sites sit at b·x′ in Λ_f. As in [`PROBLEM.md`](../PROBLEM.md):

```text
U_{mu nu}(x) = U_mu(x) U_nu(x+mu) U_mu(x+nu)^-1 U_nu(x)^-1,   U_mu(x) -> g(x) U_mu(x) g(x+mu)^-1.
```

A weight is a bounded measurable class function w with w(g⁻¹) = w(g), and μ has density ∏_p w(U_p)/Z on product Haar measure. The Wilson weight is w_β(g) = exp(−β(1 − a(g))), a(g) = ½ Re Tr g.

## 2. The map

```text
(B U)_mu(x') = U_mu(b x') U_mu(b x' + e_mu) ... U_mu(b x' + (b-1) e_mu).
```

The fine links on these products are the **line links**, the rest the **off links**. Distinct coarse links use disjoint fine links.

**Theorem 1 (covariance).** For g: Λ_f → G, B(U^g)_μ(x′) = g(bx′) (BU)_μ(x′) g(bx′ + b e_μ)⁻¹, so B(U^g) = (BU)^{g∘ι} with ι(x′) = bx′. A g that equals 1 on the coarse sites leaves BU fixed.

*Proof.* The product telescopes: g(y + s e_μ)⁻¹ g(y + s e_μ) cancels at each inner site. ∎

**Proposition 2 (closed loops).** For a closed coarse path C′, the holonomy of BU along C′ equals, as a group element, the holonomy of U along the fine path bC′. So the coarse plaquette (BU)_{μν}(x′) is the fine b×b rectangle at bx′, and every coarse Wilson loop is a fine Wilson loop.

*Proof.* A forward coarse step is the ordered product along its b fine links, and a backward one its inverse, which is the same links reversed and inverted. ∎

**Lemma 3 (Haar).** Under product Haar on fine links, BU is product Haar on coarse links, independent of the off links. Given BU = V, the b − 1 first links of each line are independent Haar and the last is fixed by the product.

*Proof.* For one coarse link, (U_0, …, U_{b−1}) ↦ (U_0, …, U_{b−2}, U_0⋯U_{b−1}) is a homeomorphism. It preserves product Haar, since for fixed U_0, …, U_{b−2} the last coordinate is a left translate of U_{b−1}. ∎

## 3. The pushforward

**Theorem 4.** Define, on coarse configurations V,

```text
rho(V) = (1/Z) integral over the off links and the first b-1 links of each line of  prod_p w(U_p),
         with the last link of each line set to (U_0 ... U_{b-2})^-1 V.
```

Then:

1. ρ is bounded and measurable, and continuous if w is. If w ≥ m > 0 then ρ ≥ m^{N_p}/Z > 0.
2. ∫ρ dV = 1, and for every bounded measurable F, ∫F(V)ρ(V) dV = (1/Z) ∫F(BU) ∏_p w(U_p) dU. So ν = B_*μ has density ρ against product Haar.
3. ρ(V^g) = ρ(V) for every g: Λ_c → G.

*Proof.* Item 2 is Fubini with Lemma 3. Item 1 follows from dominated convergence and the integrand's bound. For item 3 extend g to g̃ on Λ_f by 1 off the coarse sites: the change of variables U ↦ U^{g̃} preserves Haar and ∏_p w, and sends the fiber over V to the fiber over V^g by Theorem 1. ∎

**Proposition 5 (the character table).** For unitary representations π_ℓ of G on the coarse links,

```text
integral prod_l pi_l(V_l) rho(V) dV = < prod_l pi_l((B U)_l) >_mu.
```

So the Peter–Weyl coefficients of ρ are exactly the fine expectations of Wilson networks along the coarse lines. In particular ⟨χ(V_{p′})⟩_ν = ⟨χ(U_{b×b})⟩_μ. A truncation of ρ in the character basis is a truncation of that table.

*Proof.* Theorem 4, item 2, entry by entry. ∎

## 4. Reflection positivity and the coarse space

Let the time side be b·N′ with N′ even, and take a coarse reflection t′ ↦ c′ − t′ with the fine reflection t ↦ bc′ − t. On the coarse lattice c′ = 0 is a site reflection. c′ = −1 is a link reflection, whose fine plane is a site plane for b even and a link plane for b odd.

**Theorem 6.** B(θU) = θ′(BU). So for bounded F on the coarse half, ⟨conj(θ′F) F⟩_ν = ⟨conj(θ(F∘B)) (F∘B)⟩_μ, and ν is reflection positive whenever μ is, by [Lemma 0004](LEMMA-0004-REFLECTION-TRANSFER.md).

*Proof.* A spatial coarse link at t′ is a product of spatial fine links at bt′, and θ moves them to b(c′ − t′). A coarse time link is an ordered product of fine time links: (θU)_0(x, t) = U_0(x, c − t − 1)⁻¹ makes B(θU)_0(x′, t′) the inverse of the ordered product of fine time links from b(c′ − t′ − 1) to b(c′ − t′), which is (θ′BU)_0(x′, t′). F∘B depends on the fine half alone, since a coarse link of the coarse half uses fine links of the fine half. ∎

Now let T = A^{1/2} B A^{1/2} on H, with P the gauge projection and Ω the top eigenfunction, as in [YM4-02d](NOTE-YM4-02d-QUANTITATIVE-GAP.md), with T positive for w of positive character coefficients. On one slice the map is Q: G^{N_ℓ} → G^{N′_ℓ}, and Q* is an isometry by Lemma 3. For gauge-invariant bounded F, multiplication by Q*F acts on PH. Let **H′** be the closed span of the vectors

```text
M(F_n) T^b M(F_{n-1}) T^b ... T^b M(F_1) Omega,   n >= 0.
```

**Theorem 7.**

1. H′ contains Ω and is invariant under T^b. So T′ = T^b restricted to H′ is positive and trace class, with spec T′ ⊂ spec T^b and top eigenvalue λ₀^b, simple. Its next eigenvalue satisfies λ′₁ ≤ λ₁^b.
2. As the time side tends to infinity, every correlator of ν among gauge-invariant slice observables at coarse times t_1 ≤ … ≤ t_n tends to ⟨Ω, M(F_n) T^{b(t_n − t_{n−1})} ⋯ M(F_1) Ω⟩/λ₀^{b(t_n − t_1)}.
3. An eigenfunction h of T with eigenvalue μ gives μ^b in spec T′ exactly when h is not orthogonal to H′, and a sufficient condition is E_Haar[hΩ | Q] ≠ 0.
4. In physical units with fine spacing a, m′ = (1/(ba)) log(λ₀^b/λ′₁) ≥ (1/a) log(λ₀/λ₁), with equality exactly when the lowest state is visible in H′.
5. If for each of the vectors v above ⟨v, T′^n v⟩/λ₀^{bn} − |⟨Ω, v⟩|² ≤ C_v e^{−κn}, then λ′₁ ≤ λ₀^b e^{−κ}.

*Proof.* Item 1 is the definition with the spectral theorem. Item 2: Z = Tr(T^{N_t} P) and the correlator is a trace with insertions, whose long segment tends in trace norm to λ₀^{…} times the projector on Ω. Item 3: T^b and the projector on H′ commute, so an eigenvector of T decomposes along H′ and its complement. Conditional expectation gives ⟨h, M(Q*F) Ω⟩ = E[hΩ · F∘Q], and F runs over gauge-invariant functions while hΩ is gauge invariant. Item 4 is item 1. Item 5: the left side is Σ (μ′/λ₀^b)^n |⟨e, v⟩|² over the other eigenvectors e of T′, and the v span a dense set. ∎

So a lower bound on the coarse gap bounds the physical gap on everything the coarse observables can see, and the only loss is a state whose conditional expectation on the coarse variables vanishes.

## 5. Two dimensions: the blocking closes

Let w^(n) be the n-fold convolution, (f * h)(g) = ∫ f(g y⁻¹) h(y) dy.

**Theorem 8.** In d = 2, for every compact G, class weight w, b ≥ 2 and L_i ≥ 1,

```text
Z rho(V) = prod_{p'} w^(b^2)(V_{p'}).
```

With w = Σ_π d_π c_π χ_π, w^(n) = Σ_π d_π c_π^n χ_π. So the one-scale map is c_π → c_π^{b²}, with no other term, and it iterates exactly.

*Proof.* The coarse lines cut the fine torus into b×b blocks, and each off link lies in exactly one block. Two facts do the work. For a class weight, ∫ f(Ax) h(x⁻¹B) dx = (f * h)(AB). And if two regions share the k links x_1, …, x_k in sequence, then y = x_1⋯x_k replaces x_k by Lemma 3, leaving x_1, …, x_{k−1} out of the integrand. So merging the b plaquettes of a row gives w^(b) of the row's boundary, and merging b rows gives w^(b²) of the block's boundary word, which by Proposition 2 is V_{p′}. The line links enter only through V, so their first b − 1 integrate to 1. Characters satisfy χ_π * χ_σ = δ_{πσ} χ_π/d_π. ∎

**SU(2) Wilson.** e^{β cos θ} = (2/β) Σ_{n≥1} n I_n(β) χ_n(θ), with n = 2j + 1, so c_n = e^{−β}(2/β) I_n(β), and with t_n = I_n(β)/I_1(β):

```text
w^(m) / c_1^m = sum_{n>=1} n t_n^m chi_n,      |chi_n| <= n.
```

So the truncation at n ≤ N has sup-norm error at most Σ_{n>N} n² t_n^m. That is an explicit effective action with a certified error, on every block in d = 2, and the test brackets it in integers.

## 6. Three and four dimensions: what the blocking induces

For d ≥ 3 the coarse lines have codimension at least 2, so they leave the off links connected across the whole lattice, and ρ is a product over no local cells.

Let X = Σ_p a_p and let E_V be Haar conditioned on BU = V, so Z e^{βN_p} ρ(V) = E_V[e^{βX}].

**Theorem 9 (the first dependence on V).** Let G = SU(2), any d ≥ 2 and L_i ≥ 1.

1. For every b, E_V[X^n] is independent of V for n < b·min(b, 4).
2. For b = 2, 3, E_V[X^{b²}]/(b²)! = κ + 2^{1−2b²} Σ_{p′} χ_{1/2}(V_{p′}), with κ independent of V.

So log(ρ(V)/ρ(V′)) = 2^{1−2b²} β^{b²} Σ_{p′}(χ_{1/2}(V_{p′}) − χ_{1/2}(V′_{p′})) + O(β^{b²+1}). In the Wilson form that is β′/4 = (β/4)^{b²}, the same leading flow as Theorem 8.

*Proof.* Expand X^n over multisets M of plaquettes, and expand each a_p^m in characters, so that a term carries spin j_p on each plaquette of M. Call p nontrivial if j_p ≠ 0. Take a term that depends on V_ℓ for a coarse link ℓ in direction μ.

(a) If a free link lies in exactly one nontrivial plaquette the term vanishes, since ∫χ_j(Ax) dx = 0 for j ≠ 0.

(b) Every fine link of the line ℓ lies in a nontrivial plaquette: if the one at position s does not, Lemma 3 with V_ℓ carried by that position shows the term is independent of V_ℓ.

(c) Fix s and take the graph Γ_s whose vertices are the μ-links crossing from x_μ = s to s + 1, and whose edges are the nontrivial plaquettes (μ, ν) in that slice. The vertex on ℓ has degree at least 1. By (a) a free vertex has degree 0 or at least 2, so the component of that vertex either holds a cycle or has at least two leaves, both on coarse μ-lines. Two distinct coarse μ-lines lie at transverse distance at least b. A cycle has length at least 4 if contractible and at least bL_ν ≥ b if it winds. So the slice holds at least min(b, 4) edges.

(d) The b slices are disjoint, so M holds at least b·min(b, 4) nontrivial plaquettes. That is item 1.

For item 2 take b = 2, 3 and |M| = b². Then every plaquette has multiplicity one and spin ½, and each slice is a straight segment between two μ-lines or a straight winding cycle of length b. The ν-links between consecutive slices are free unless they lie on a coarse line, so by (a) consecutive slices match and M is the flat b×b filling of one coarse plaquette. Then ∫χ_{1/2}(Ax) χ_{1/2}(x⁻¹B) dx = χ_{1/2}(AB)/2 applied b² − 1 times, with the remaining links cancelling as in Theorem 8, gives 2^{−(b²−1)} χ_{1/2}(V_{p′}), and the a_p = ½χ_{1/2} supply 2^{−b²}. ∎

**Corollary 10 (a certified truncation in four dimensions).** Since |X| ≤ N_p, Taylor's remainder gives, for all V, V′ and b = 2, 3,

```text
| E_V[e^{beta X}] - E_{V'}[e^{beta X}] - 2^{1-2b^2} beta^{b^2} sum_{p'} ( chi(V_{p'}) - chi(V'_{p'}) ) |
   <= 2 (beta N_p)^{b^2+1} exp(beta N_p) / (b^2+1)!.
```

On the block (ℤ/2)⁴ → (ℤ/1)⁴, with N_p = 96 and six coarse plaquettes, this resolves the leading term at β = 10⁻¹²: the bound is below 2 × 10⁻⁵² and the leading term's range reaches 1.9 × 10⁻⁴⁹. The remainder is crude, so the range of β is narrow.

**Proposition 11 (a nonlocal term, for Z2).** For Z2 with w = 1 + uσ, in d ≥ 3 at b = 2, ρ(V) ∝ Σ_M u^{|M|} ∏ V^{∂M} over plaquette sets M whose boundary lies on line links. Let P, Q be two coarse plaquettes with fillings of 4 plaquettes each. If they are perpendicular and share a coarse link, then in log ρ the coefficient of W_P W_Q is 2u¹⁰ + O(u¹²), from the two fine cubes at that link that hold one plaquette of each filling, on a lattice with sides large enough that no surface wraps. If they are parallel at coarse distance 1, that coefficient vanishes through u¹². So the blocked action leaves the Wilson form at finite order, and its range grows with the order.

*Derivation.* A cube adds a closed surface, and M = P △ Q △ ∂C has 4 + 4 + 6 − 2·2 = 10 plaquettes. Disjoint fillings give u⁸ and cancel in the logarithm against the square of the single term u⁴. The parallel pair needs a tube of two cubes: 4 + 4 + 10 − 2·2 = 14 plaquettes. ∎

**Proposition 12 (walls).** Freeze instead every link on the codimension-one walls between blocks. Every plaquette then lies in one closed block, so the density on the wall links is Z⁻¹ ∏_{blocks} Z_block(walls), a finite-range form in every d, at the cost of many more coarse variables. In d = 2 the walls are the lines, and this is Theorem 8.

## 7. The bound as the spacing falls

**Theorem 13 (a coarse influence bound gives a physical gap).** Let C_ij = sup TV(π_i(·|x), π_i(·|x′)) over x, x′ differing at the coarse link j, for the conditional laws π_i of ν, and let d(i, j) be the distance between the time coordinates of i and j. If, uniformly in the time side,

```text
c_kappa = sup_i sum_j C_ij exp(kappa d(i,j)) < 1,
```

then every gauge-invariant slice correlator of ν has connected part at most a constant times e^{−κ|t|}, and by Theorem 7, item 5, m ≥ κ/(ba) on H′.

*Proof.* Tilt ν by a bounded positive f supported on a slice. By the comparison in [YM4-02e](NOTE-YM4-02e-KSTEP-AND-LOCALITY.md), |ν^f(g) − ν(g)| ≤ Σ_a Σ_j b_a D_ja δ_j(g), with b_a = 0 off the support of f and D = Σ_m C^m. The weight e^{κd} is submultiplicative along paths by the triangle inequality, so D_ja ≤ e^{−κ d(j,a)}/(1 − c_κ). ∎

**Theorem 14 (two dimensions, uniform along the trajectory).** Let d = 2, G = SU(2), w = w_β with β ≥ 1, and b ≥ 2√β. Then on every spatial circle of length L ∈ bℕ,

```text
lambda_1/lambda_0 <= (4 - sqrt 15)^(1/b).
```

With β = 4/(g²a²) this reads, at b = ⌈2√β⌉ and ba → 4/g, m ≥ (log(1/(4 − √15))/4) g, about 0.516 g, uniformly as a → 0.

*Proof.* By Theorem 8 the coarse lattice carries the weight w^(b²), and with δ = Σ_{n≥2} n² t_n^{b²}, the bounds 1 − δ ≤ w^(b²)/c_1^{b²} ≤ 1 + δ give ε′ ≤ δ. Amos's bound I_{ν+1}(β)/I_ν(β) ≤ β/(ν + √(ν² + β²)), NAMED, gives t_n ≤ exp(−Σ_{ν<n} arcsinh(ν/β)). With b² ≥ 4β and arcsinh(y) ≥ y arcsinh(1) on [0, 1], the term n = 2 is at most 4e^{−4 arcsinh 1} < 0.118, n = 3 at most 9 e^{−4(arcsinh 1 + arcsinh 2)} < 0.001, and n ≥ 4 sum below 0.001. So ε′ ≤ δ < 1/8. Theorem 5 of YM4-02e on the coarse circle has σ = 0, and its r at ε = 1/8 is 4 − √15. Theorem 8 gives eigenvalues c_π^{b²L/b} = (c_π^L)^b on the coarse lattice. ∎

The exact ratio is t₂^L, so m = 3g²ℓ/8 as a → 0 at ℓ = La. At ℓ = 4/g that is 1.5 g, above 0.516 g. Here the fine-lattice bounds fail as β grows, with ε = tanh β → 1, and one blocking to the scale 4/g recovers a gap in physical units, of the right form in g.

**In three and four dimensions.** At fixed physical volume the coarse lattice can be held fixed, with L_phys/(ba) sites per side, so the configuration space stays one fixed G^{N′} and only the density ρ_a moves as a falls. Theorem 13 then reduces the uniform bound to this:

**Hypothesis UH(ℓ₀), OPEN.** There are a fixed length ℓ₀ = ba, a κ > 0 and a c < 1 with c_κ(ρ_a) ≤ c along the family (a → 0, β following a).

UH holds in d = 2, by Theorem 14. For d ≥ 3 three things are recorded:

- **The obstruction moves.** Section 4 of YM4-02e has the supremum over fine configurations growing like βL³/(ta²) for the Gaussian. Here the supremum runs over the fixed coarse configurations with the fine fluctuations integrated.
- **Range.** C_ij at large time separation is a long-range term of ρ_a, and bounding it is a clustering estimate. So UH needs a localization of ρ_a, which is YM4-04.
- **Thin lines.** Lines have codimension d − 1. In d = 4 their capacity vanishes in the continuum, so conditioning on them leaves the off links' fluctuations long-ranged, and a Wilson line of fixed length loses its overlap as a falls, CONJECTURE. Block averages, as in Balaban's work, NAMED, condition on a set that fills space, and their conditional fluctuations are expected to decay at the block scale, CONJECTURE. So the sharp map B here serves the exact identities, and YM4-04 will likely need an average in its place: which one, and with which positivity, is OPEN.

## 8. What could fail

- **Theorem 9** rests on (a) to (d). The count in (c) needs a free vertex's degree read in distinct nontrivial plaquettes, whatever their multiplicity. The test reads the first dependence on (ℤ/2)⁴, with SU(2) averages from 2T, within its design degree.
- **Theorem 7, item 3** uses that T^b and the projector on H′ commute, which needs H′ invariant under T^b and T^b self-adjoint.
- **Theorem 14** uses Amos's bound as NAMED. The test brackets t_n in integers on a grid of β, and that covers the grid alone.
- **Proposition 11** counts surfaces by hand, and the test enumerates them.

## 9. The test

[`tests/test_one_scale_blocking.py`](../tests/test_one_scale_blocking.py) runs the rows named in the prediction, integers only, and its output is [`tests/ONE_SCALE_BLOCKING_RECEIPT.txt`](../tests/ONE_SCALE_BLOCKING_RECEIPT.txt).
