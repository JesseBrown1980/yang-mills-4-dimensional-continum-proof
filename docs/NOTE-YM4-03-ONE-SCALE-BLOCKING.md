# YM4-03: one-scale blocking, the exact pushforward, and what it induces

**Status: DERIVED by the seat ACER-CLAUDE-FABLE5 on November 5, 2026, on the operator's word: "Agreed. Go after that." Its exact tests are registered first in [`PREDICTION-YM4-03.hbp`](PREDICTION-YM4-03.hbp), pushed at `7e6b111` before the test existed, and read in section 9. MEASURED: 423 checks with 0 failed, and 7 reads missed on 3 rows of the prediction, kept below: the range in Corollary 10, a value I wrote by hand; the coefficient in Proposition 11, a row tagged DERIVED whose registered falsifier fired, with the proposition corrected after the run; and single insertions reaching the first excited state of e = 0 on four Z2 lattices, a row tagged CONJECTURE until read. DERIVED: the numbered statements of sections 2 to 7, with Amos's bound NAMED in Theorem 14. CONJECTURE: the statements so tagged in section 7. OPEN: the uniform bound in d ≥ 3, visibility along a family, and the mass gap and the continuum in d = 4. GPT-6 opened [PR #28](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/28) on the same issue from its own branch at 11:38:14Z, with its prediction `fae9a7f` at 11:31:28Z, both before `7e6b111` at 11:45Z: the same map at b = 2, the Haar pushforward for continuous SU(2) on even periodic 4D lattices with coarse sides at least 2, and a certified truncation for every β in [0, 1] on an isolated 2×2 tile, which is the one-block step in the proof of Theorem 8. [The second seat's attack at `6c87200`](../reviews/opus55-ym4-03/) confirmed Theorem 9 and the core of each theorem it read, and refuted two clauses of Theorem 7, item 3, and the reach of Theorem 13's proof, and those repairs and its other holds are applied here. GPT-6's reading of this head is OPEN.**

**Scope:** one finite periodic lattice, any compact group G and any bounded class weight with Z ≠ 0, with SU(2) and the Wilson weight as the case of interest: a positive weight with every character coefficient c_π ≥ 0 in Theorem 7, SU(2) in Theorems 9 and 14, Z2 in Proposition 11. Sections 5 and 7 read one family as the spacing falls in two dimensions. In three and four dimensions the uniform bound stays OPEN: section 7 states a hypothesis that gives it on H′, with the lowest state's visibility along the family OPEN. Issue #3 sets the mass gap and the continuum outside its target, and in d = 4 both stay OPEN here.

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

Now let T = A^{1/2} B A^{1/2} on H, with P the gauge projection and Ω the top eigenfunction, as in [YM4-02d](NOTE-YM4-02d-QUANTITATIVE-GAP.md). Here w is continuous with 0 < m ≤ w ≤ M, as there, and every character coefficient satisfies c_π ≥ 0, which gives T ≥ 0, and Theorem 7 uses this. Z2 with w = 1, 3 has c_1 = −1, and at b = 3 on a circle of 3 it reads T = 8, −1 on PH and T³ = 512, −1. On one slice the map is Q: G^{N_ℓ} → G^{N′_ℓ}, and Q* is an isometry by Lemma 3. For gauge-invariant bounded F, multiplication by Q*F acts on PH. Let **H′** be the closed span of the vectors

```text
M(F_n) T^b M(F_{n-1}) T^b ... T^b M(F_1) Omega,   n >= 0.
```

**Theorem 7.**

1. H′ contains Ω and is invariant under T^b. So T′ = T^b restricted to H′ is positive and trace class, with spec T′ ⊂ spec T^b and top eigenvalue λ₀^b, simple. Its next eigenvalue satisfies λ′₁ ≤ λ₁^b.
2. As the time side tends to infinity, every correlator of ν among gauge-invariant slice observables at coarse times t_1 ≤ … ≤ t_n tends to ⟨Ω, M(F_n) T^{b(t_n − t_{n−1})} ⋯ M(F_1) Ω⟩/λ₀^{b(t_n − t_1)}.
3. For an eigenvalue μ > 0 of T on PH, μ^b lies in spec T′ exactly when the eigenspace of μ in PH is not orthogonal to H′. An eigenfunction h in PH with E_Haar[hΩ | Q] ≠ 0 is not orthogonal to H′. Z2 on 2×2 at b = 2, w = 3, 1, has an eigenvalue with 6 dimensions in H′ and 12 orthogonal to it, and Q8 on a circle of 2 has an eigenfunction outside PH with E_Haar[hΩ | Q] ≠ 0.
4. In physical units with fine spacing a, m′ = (1/(ba)) log(λ₀^b/λ′₁) ≥ (1/a) log(λ₀/λ₁), with equality exactly when the lowest state is visible in H′.
5. If for each of the vectors v above ⟨v, T′^n v⟩/λ₀^{bn} − |⟨Ω, v⟩|² ≤ C_v e^{−κn}, then λ′₁ ≤ λ₀^b e^{−κ}.

*Proof.* Item 1 is the definition with the spectral theorem. Item 2: Z = Tr(T^{N_t} P) and the correlator is a trace with insertions, whose long segment tends in trace norm to λ₀^{…} times the projector on Ω. Item 3: H′ lies in PH by Theorem 1. T^b and the projector Π on H′ commute, and so do T and Π, since T ≥ 0 makes T a function of T^b, so Π maps the eigenspace E_μ of μ in PH into itself. If E_μ is not orthogonal to H′, some h in E_μ has Πh ≠ 0, and T′Πh = μ^bΠh. Conversely an eigenvector of T′ at μ^b lies in E_μ, since T ≥ 0 makes the μ^b-eigenspace of T^b that of μ for T. For h in PH, conditional expectation gives ⟨h, M(Q*F) Ω⟩ = E[G · F∘Q] with G = E_Haar[h̄Ω | Q], and G is coarse gauge invariant by the extension in Theorem 4, since h̄Ω is gauge invariant, so F = Ḡ is allowed and the pairing reads E|G|². The two cases named are MEASURED, by the second seat. Item 4 is item 1. Item 5: the left side is Σ (μ′/λ₀^b)^n |⟨e, v⟩|² over the other eigenvectors e of T′, and the v span a dense set. ∎

So a lower bound on m′ is a bound on H′, and by item 4 m′ = m, so it bounds the gap of the whole gauge-invariant space, when the lowest state is visible in H′, with m′ > m otherwise. By item 3 a state that H′ misses has a vanishing conditional expectation on the coarse variables. Visibility along a family as a falls is OPEN.

**Electric flux.** Let z ≠ 1 be a central element of G with z² = 1, so some irreducible π has π(z) = −1, and let Z_μ multiply U_μ(x) by z on the spatial links with x_μ = s. A plaquette holds both or neither of its μ-links on that plane, so Z_μ commutes with A and B, and two planes differ by a gauge transformation, so on PH it is one operator for all s. So PH splits into sectors labelled by e = (e_μ), e_μ = ±1, with P_e = 2^{−k} ∏_μ (I + e_μ Z_μ) over the k spatial directions, and e = 0 names the sector with every e_μ = 1. Let λ₀(e) be the top of T in sector e and λ₁(0) the second value in e = 0.

**Proposition 7a.** Let w > 0, with T ≥ 0 as above, so each logarithm below has a value, with log(λ₀/0) = ∞. Δ_full is the gap log(λ₀/λ₁) of T on PH, a times m.

1. Ω lies in e = 0, so λ₀ = λ₀(0), and Δ_full = min(Δ₀, Δ_flux), with Δ₀ = log(λ₀/λ₁(0)) and Δ_flux = min_{e ≠ 0} log(λ₀/λ₀(e)).
2. The holonomy of a coarse loop with winding number n in direction μ takes the factor zⁿ under Z_μ, from its net crossing of the plane, for every b and every s. So a character χ_π with π(z) = −1 changes sign on a loop winding once, and keeps it on one winding twice and on a contractible one, and a character with π(z) = 1, such as spin 1 for SU(2), keeps it on all of them.
3. For a gauge-invariant coarse F, P_e(FΩ) = P_e(F)Ω. So coarse winding loops reach every sector on a coarse lattice that holds one in each direction.

*Proof.* The kernel of T on gauge orbits is positive, so Ω is positive and simple, and Z_μ permutes orbits and fixes it. Item 2 is the count of crossings. Item 3 is item 1 with Z_μ multiplicative. ∎

Reaching a sector is a statement about a sector, and it leaves open how much of P_e(FΩ) lies in the lowest eigenspace of e. So the prediction's flux rows, pushed at `3db4313` before their controls ran, read three things per sector: commutation, access, and a certified overlap with the lowest eigenspace, the whole eigenspace when it is degenerate. Section 9 holds them. Each overlap is for that level on that lattice, and visibility along a family stays OPEN. By Theorem 7, items 4 and 5, Theorem 13's bound reaches Δ_full at a spacing a when the one level that sets Δ_full there is visible in H′ at that a, which on these five lattices is the top of e = (1, −1), with the top of e = (−1, 1) equal to it on 2×2: a positive overlap with one vector of H′ at that a is enough, and its size may vary with a.

## 5. Two dimensions: the blocking closes

Let w^(n) be the n-fold convolution, (f * h)(g) = ∫ f(g y⁻¹) h(y) dy.

**Theorem 8.** In d = 2, for every compact G, class weight w, b ≥ 2 and L_i ≥ 1,

```text
Z rho(V) = prod_{p'} w^(b^2)(V_{p'}).
```

With w = Σ_π d_π c_π χ_π, w^(n) = Σ_π d_π c_π^n χ_π. So the one-scale map is exactly c_π → c_π^{b²} on every π, and it iterates exactly.

*Proof.* The coarse lines cut the fine torus into b×b blocks, and each off link lies in exactly one block. Two facts do the work. For a class weight, ∫ f(Ax) h(x⁻¹B) dx = (f * h)(AB). And if two regions share the k links x_1, …, x_k in sequence, then y = x_1⋯x_k replaces x_k by Lemma 3, leaving x_1, …, x_{k−1} out of the integrand. So merging the b plaquettes of a row gives w^(b) of the row's boundary, and merging b rows gives w^(b²) of the block's boundary word, which by Proposition 2 is V_{p′}. The line links enter only through V, so their first b − 1 integrate to 1. Characters satisfy χ_π * χ_σ = δ_{πσ} χ_π/d_π. ∎

**SU(2) Wilson.** e^{β cos θ} = (2/β) Σ_{n≥1} n I_n(β) χ_n(θ), with n = 2j + 1, so c_n = e^{−β}(2/β) I_n(β), and with t_n = I_n(β)/I_1(β):

```text
w^(m) / c_1^m = sum_{n>=1} n t_n^m chi_n,      |chi_n| <= n.
```

So the truncation at n ≤ N has sup-norm error at most Σ_{n>N} n² t_n^m. That is an explicit effective action with a certified error, on every block in d = 2, DERIVED. The test brackets the tail in integers at β = 1, 4 and m = 4, 16, with the cut at n ≤ 3, and evaluates the series directly at m = 1, at five rational angles. GPT-6's isolated 2×2 tile in [PR #28](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/28), W(V) = Σ (n + 1)(f_n/f_0)⁴ χ_n, is this form at m = 4, with its f_n/f_0 = t_{n+1}. Its bound 25/671741424 on β ≤ 1 for the cut at its n ≤ 2 stands above the 8.8 × 10⁻⁹ read here at β = 1.

## 6. Three and four dimensions: what the blocking induces

For d ≥ 3 the coarse lines have codimension at least 2, so they leave the off links connected across the whole lattice, and the blocks of Theorem 8 join through those off links into one. What is held of ρ there: Theorem 9 for SU(2) at its first order in β, Proposition 11 for Z2 at its first nonlocal order. Its form at higher order for SU(2) is OPEN.

Let X = Σ_p a_p and let E_V be Haar conditioned on BU = V, so Z e^{βN_p} ρ(V) = E_V[e^{βX}].

**Theorem 9 (the first dependence on V).** Let G = SU(2), any d ≥ 2 and L_i ≥ 1.

1. For every b, E_V[X^n] is independent of V for n < b·min(b, 4).
2. For b = 2, 3, E_V[X^{b²}]/(b²)! = κ + 2^{1−2b²} Σ_{p′} χ_{1/2}(V_{p′}), with κ independent of V.

So at b = 2, 3, log(ρ(V)/ρ(V′)) = 2^{1−2b²} β^{b²} Σ_{p′}(χ_{1/2}(V_{p′}) − χ_{1/2}(V′_{p′})) + O(β^{b²+1}). In the Wilson form that is β′/4 = (β/4)^{b²}, the same leading flow as Theorem 8.

*Proof.* Expand X^n over multisets M of plaquettes, and expand each a_p^m in characters, so that a term carries spin j_p on each plaquette of M. Call p nontrivial if j_p ≠ 0. Take a term that depends on V_ℓ for a coarse link ℓ in direction μ.

(a) If a free link lies in exactly one nontrivial plaquette the term vanishes, since ∫χ_j(Ax) dx = 0 for j ≠ 0.

(b) Every fine link of the line ℓ lies in a nontrivial plaquette: if the one at position s does not, Lemma 3 with V_ℓ carried by that position shows the term is independent of V_ℓ.

(c) Fix s and take the graph Γ_s whose vertices are the μ-links crossing from x_μ = s to s + 1, and whose edges are the nontrivial plaquettes (μ, ν) in that slice. The vertex on ℓ has degree at least 1. By (a) a free vertex has degree 0 or at least 2, so the component of that vertex either holds a cycle or has at least two leaves, both on coarse μ-lines. Two distinct coarse μ-lines lie at transverse distance at least b. A cycle has length at least 4 if contractible and at least bL_ν ≥ b if it winds. So the slice holds at least min(b, 4) edges.

(d) The b slices are disjoint, so M holds at least b·min(b, 4) nontrivial plaquettes. That is item 1.

For item 2 take b = 2, 3 and |M| = b². Then every plaquette has multiplicity one and spin ½, and each slice is a straight segment between two μ-lines or a straight winding cycle of length b. The ν-links between consecutive slices are free unless they lie on a coarse line, so by (a) consecutive slices match and M is the flat b×b filling of one coarse plaquette. Then ∫χ_{1/2}(Ax) χ_{1/2}(x⁻¹B) dx = χ_{1/2}(AB)/2 applied b² − 1 times, with the remaining links cancelling as in Theorem 8, gives 2^{−(b²−1)} χ_{1/2}(V_{p′}), and the a_p = ½χ_{1/2} supply 2^{−b²}. ∎

**Lemma 9a (the four points that proof rests on).** Fine sides are bL_i ≥ 2.

1. *Free links and links on a line.* Carry V_ℓ on one position by Lemma 3, so the other positions of ℓ are free, and every link off the lines is free. A plaquette's word holds each of its four links once, since fine sides are at least 2. Expanding a_p^m in characters gives one spin per distinct plaquette per term, so a repeated plaquette is one edge, and the degree in (a) counts distinct nontrivial plaquettes, at any multiplicity and any spin. A vertex of Γ_s off every coarse μ-line has degree 0 or at least 2. A vertex on a coarse μ-line may have degree 1, since its integral also holds the carried link: at b = 2, U_1 = U_0⁻¹V puts U_0 into the plaquettes of both positions. So a leaf of Γ_s lies on a coarse μ-line.
2. *The graph on the torus, and L_i = 1.* Each edge of Γ_s joins two different vertices, since sides are at least 2. It has double edges exactly on fine side 2, where they form a cycle of length 2 = bL_ν that winds, at b = 2, L_ν = 1. Coarse μ-lines sit at transverse coordinates divisible by b, so two distinct ones lie at graph distance at least b. A tree component with an edge has two leaves on two distinct lines, so at least b edges. A contractible cycle has length at least 4, and a winding one at least bL_ν ≥ b. When every transverse L_ν = 1 there is one coarse μ-line, and the component holds a cycle. The b slices are the planes x_μ = start + s, distinct mod bL_μ, and a plaquette (μ, ν) lies in one of them through its base coordinate in μ.
3. *Equality at n = b², b = 2, 3.* Then b·min(b, 4) = b² = n, so every slice holds exactly b edges and every plaquette has multiplicity one and spin ½, and X^n/n! gives a product of n distinct plaquettes the coefficient 1. A path of b edges joins lines differing by b in one coordinate, so it is straight. A cycle of b edges winds with bL_ν = b, and at b = 3 every cycle has at least 3 edges, since its sides are multiples of 3. A ν-link at x_μ = s + 1 with s + 1 ≠ 0 mod b is free, so it needs a second plaquette, and every plaquette of M already lies in the b slices of the line, so slice s + 1 holds the same edge. So M is the flat filling of one coarse plaquette. Since χ_{1/2}(g⁻¹) = χ_{1/2}(g), orientation enters nowhere, and each coarse plaquette has one filling, so Σ_{p′} runs over coarse plaquettes with coefficient 1. In the merge, b² − 1 free links reduce b² characters to one, and the other (b − 1)² of the 2b(b − 1) interior links occur as x x⁻¹ and drop out. On L_μ = L_ν = 1 the boundary links are line links, each in two plaquettes, left unintegrated, and the word is the commutator, by Proposition 2.
4. *Continuous moments and the 2T read.* The 24 elements of 2T form a spherical design of degree 5 on S³: a polynomial of degree at most 5 in x's entries is a sum of matrix elements of spins at most 5/2, and for spin n/2, n = 1, …, 5, the average over 2T vanishes, since its character's does. The test reads Σ_{2T} χ_{n/2} = 0, 0, 0, 0, 0, 24 for n = 1, …, 6. Integrating one free link at a time, each integrand has degree at most n in that link, so at n = 4 the 2T average is the Haar average, term by term. The second seat's separate S³ moments read the same terms one by one.

**The thin tube.** The bound of item 1 is reached at b ≥ 4 for d ≥ 3 with a side L_μ = 1: the 4b plaquettes around a square cross-section holding the coarse μ-line read 2^{−8b} χ_{1/2}(V_μ)², a spin-1 winding line, MEASURED exactly by the second seat at b = 2 to 6. On L_μ = 2 the 8b plaquettes around the line of fine length 2b read 2^{−16b} χ_{1/2}(V_μ(x′)V_μ(x′ + μ))², MEASURED there at three lattices. At b = 4, n = 16 the tube enters beside the flat fillings, and at b ≥ 5 it comes first, at n = 4b: E_V[X^{4b}]/(4b)! = κ + 2^{−8b} · 2(d − 1)(d − 2) Σ_ℓ χ_{1/2}(V_ℓ)² over the coarse lines ℓ in directions with L_μ = 1. DERIVED from the count above: a slice of 4 edges is a square at b ≥ 5, free cross links keep one square along the line, it closes on L_μ = 1 alone, each line has 2(d − 1)(d − 2) squares, and all the terms have one sign. The second seat's search reads exactly those sets on (ℤ/5)³, (ℤ/6)³, (ℤ/7)³, (ℤ/5) × (ℤ/10)² and (ℤ/5)⁴, 4 per line at d = 3 and 12 at d = 4. So on a lattice with d ≥ 3 and a side L_μ = 1, item 2 and the flow β′/4 = (β/4)^{b²} stop at b = 3. With every L_i ≥ 2 a term that moves with V holds a closed coarse loop of coarse links whose fine links all lie in nontrivial plaquettes, since by (b) and the extension in Theorem 4 it is a coarse gauge-invariant function of those links, and on a forest that is a constant. A winding loop has at least two sets of slices, and two μ-links of a contractible loop share theirs, so E_V[X^n] is independent of V for n < min(b², 8b), and item 2 holds through b = 7, DERIVED by the second seat. Its search reads b² with the flat filling alone at b = 4, 5, 6 on (ℤ/2b)³, and the tube over one line's b slices with both ends capped, 4b + 2 plaquettes, reads 2^{2−n_p}, constant in V.

**Corollary 10 (a certified truncation in four dimensions).** Since |X| ≤ N_p, Taylor's remainder gives, for all V, V′ and b = 2, 3,

```text
| E_V[e^{beta X}] - E_{V'}[e^{beta X}] - 2^{1-2b^2} beta^{b^2} sum_{p'} ( chi(V_{p'}) - chi(V'_{p'}) ) |
   <= 2 (beta N_p)^{b^2+1} exp(beta N_p) / (b^2+1)!.
```

On the block (ℤ/2)⁴ → (ℤ/1)⁴, with N_p = 96 and six coarse plaquettes, this resolves the leading term at β = 10⁻¹²: the bound is 1.36 × 10⁻⁵², which the receipt floors to 135 × 10⁻⁵⁴, and the leading term's range over V is β⁴/6, or 1.67 × 10⁻⁴⁹. The remainder is crude: on this block the bound stays below β⁴/6 up to β = 1.2 × 10⁻⁹.

The range: for V_i = cos α_i + n_i sin α_i, χ_{1/2}(V_1 V_2 V_1⁻¹ V_2⁻¹) = 2 − 4 sin²α_1 sin²α_2 sin²φ_12, so Σ_{p′}(χ(1) − χ(V_{p′})) is at most 4 Σ_{i<j} sin²φ_ij. For four unit vectors in ℝ³ the frame bound Σ_{i,j} cos²φ_ij ≥ 16/3 gives Σ_{i<j} sin²φ_ij ≤ 16/3, reached at the tetrahedron, so the difference is at most 64/3 and the range is (β⁴/128)(64/3) = β⁴/6. The test reads 1.655 × 10⁻⁴⁹ at a rational V. **I wrote 1.9 × 10⁻⁴⁹ at first, from the count 6 × 4 = 24, and the row as pushed, at least 1.8 × 10⁻⁴⁹, stays a miss.**

**Proposition 11 (a nonlocal term, for Z2).** For Z2 with w = 1 + uσ, in d ≥ 3 at b = 2, ρ(V) ∝ Σ_M u^{|M|} ∏ V^{∂M} over plaquette sets M whose boundary is a union of whole coarse lines, with V^{∂M} the product of V_ℓ over those lines, since a line met on part of its fine links integrates to zero. Let P, Q be two coarse plaquettes with fillings of 4 plaquettes each. If they are perpendicular and share a coarse link, then in log ρ the coefficient of W_P W_Q is 3u¹⁰ + O(u¹²), from the two fine cubes at that link that hold one plaquette of each filling, taken alone or together, on a lattice with sides large enough that no surface wraps. If they are parallel at coarse distance 1, that coefficient vanishes through u¹². So for Z2 the blocked action leaves the Wilson form at order u¹⁰, and the pair at coarse distance 1 first reads at order u¹⁴, with coefficient 4 by the second seat's count: two points on how range grows with order. For SU(2) in d ≥ 3 the form of the next term is OPEN.

*Derivation.* A cube adds a closed surface, and M = P △ Q △ ∂C has 4 + 4 + 6 − 2·2 = 10 plaquettes, and with both cubes M = P △ Q △ ∂(C₁ ∪ C₂) has 4 + 4 + 10 − 2·4 = 10. Disjoint fillings give u⁸ and cancel in the logarithm against the square of the single term u⁴. The parallel pair needs a tube of two cubes: 4 + 4 + 10 − 2·2 = 14 plaquettes. ∎

The test enumerates every surface with that boundary, on 8³ and 8⁴: 1 at size 8 and 3 at size 10, and for the parallel pair on 12³, 1 at size 8 and 16 at size 12, against 8 bumps per filling, so the logarithm's coefficient reads 0 through u¹². **I wrote 2u¹⁰ at first, with the two cubes alone, and that row of the prediction stays a miss on both lattices.**

**Proposition 12 (walls).** Freeze instead every link on the codimension-one walls between blocks. Every plaquette holding an interior link then lies in one closed block, and for d ≥ 3 a plaquette with all four links on walls, 12 of 24 on (ℤ/2)³, is a function of the walls alone, so the density on the wall links is Z⁻¹ ∏_{wall p} w(U_p) ∏_{blocks} Z_block(walls), a finite-range form in every d, at the cost of many more coarse variables. In d = 2 the walls are the lines, and this is Theorem 8.

## 7. The bound as the spacing falls

**Theorem 13 (a coarse influence bound gives a gap on H′).** Let C_ij = sup TV(π_i(·|x), π_i(·|x′)) over x, x′ differing at the coarse link j, for the conditional laws π_i of ν, and let d(i, j) be the distance on the time circle between the time coordinates of i and j, a time link taking the coordinate of its base. If, uniformly in the time side,

```text
c_kappa = sup_i sum_j C_ij exp(kappa d(i,j)) < 1,
```

then for f and g products of gauge-invariant slice observables on finite sets of slices, at distance t on the time circle, the connected part of ⟨f g⟩_ν is at most a constant times e^{−κt}, with the constant free of the time side, and by Theorem 7, items 2 and 5, m′ ≥ κ/(ba). By item 4, m′ = m when the lowest state is visible in H′, where this is a bound on m, and m′ > m otherwise.

*Proof.* Tilt ν by a bounded positive f supported on finitely many slices, which the vectors of H′ need: two-slice correlators read the span of T′ⁿ M(F)Ω, of dimension 14 of 20 on Z2 at 2×2, 6 of 8 on Z2 at 2×1, 21 of 27 on Z3 at 2×1 and 29 of 33 on S3 at 2×1. By the comparison in [YM4-02e](NOTE-YM4-02e-KSTEP-AND-LOCALITY.md), |ν^f(g) − ν(g)| ≤ Σ_a Σ_j b_a D_ja δ_j(g), with b_a = 0 off the support of f and D = Σ_m C^m. The weight e^{κd} is submultiplicative along paths by the triangle inequality, so D_ja ≤ e^{−κ d(j,a)}/(1 − c_κ). With b_a ≤ 1, the sums over a in the support of f and j in the support of g give the constant, and Cov(f, g) = ν(f)(ν^f(g) − ν(g)) passes the bound to the correlators, with a constant added to a real f to make it positive, which leaves Cov(f, g) as it is, and a complex one split into real parts, at every time side and so in the limit of Theorem 7, item 2. ∎

**Theorem 14 (two dimensions, uniform along the trajectory).** Let d = 2, G = SU(2), w = w_β with β ≥ 1, and b ≥ 2√β. Then on PH, on every spatial circle of length L ∈ bℕ,

```text
lambda_1/lambda_0 <= (4 - sqrt 15)^(1/b).
```

With β = 4/(g²a²), at b = ⌈2√β⌉ one has 4 ≤ bag < 6, with bag = 4 when 2√β is an integer and bag → 4 as a → 0. So on circles with L ∈ bℕ, of physical length at least ba, m ≥ (log(1/(4 − √15))/(bag)) g: above 0.3439 g at every β ≥ 1, and tending to (log(1/(4 − √15))/4) g = 0.5158 g as a → 0. Along a = 4/(gb), b = 2, 3, …, where β = b²/4 and bag = 4, on circles of length 4k/g, k ∈ ℕ, it reads 0.5158 g at every b.

*Proof.* By Theorem 8 the coarse lattice carries the weight w^(b²), and with δ = Σ_{n≥2} n² t_n^{b²}, the bounds 1 − δ ≤ w^(b²)/c_1^{b²} ≤ 1 + δ give ε′ ≤ δ. Amos's bound I_{ν+1}(β)/I_ν(β) ≤ β/(ν + √(ν² + β²)), NAMED, gives t_n ≤ exp(−Σ_{ν<n} arcsinh(ν/β)). With b² ≥ 4β, β ≥ 1 and β arcsinh(ν/β) increasing in β, since arcsinh(y) ≥ y/√(1 + y²), we have b² arcsinh(ν/β) ≥ 4 arcsinh ν, so the term n = 2 is at most 4e^{−4 arcsinh 1} < 0.118, n = 3 at most 9 e^{−4(arcsinh 1 + arcsinh 2)} < 0.001, and n ≥ 4 sum below 0.001. So ε′ ≤ δ < 1/8. Theorem 5 of YM4-02e on the coarse circle has σ = 0, and its r at ε = 1/8 is 4 − √15. Theorem 8 gives eigenvalues c_π^{b²L/b} = (c_π^L)^b on the coarse lattice. ∎

The exact ratio is t₂^L, so m = 3g²ℓ/8 as a → 0 at ℓ = La. At ℓ = 4/g that is 1.5 g, above 0.516 g. On the fine circle Theorem 5 of YM4-02e needs 2 tanh β < 1, so β < 0.5493, and ε = tanh β → 1 as β grows. One blocking to the scale 4/g brings ε′ below 1/8 at every β ≥ 1, and its bound is proportional to g, as the exact value is at ℓ = 4/g.

**In three and four dimensions.** At fixed physical volume the coarse lattice can be held fixed, with L_phys/(ba) sites per side, so each slice's configuration space stays one fixed G^{N′_ℓ}, the time side grows with the limit of Theorem 7, item 2, and only the density ρ_a moves as a falls. Theorem 13 then reduces the uniform bound on H′ to this, with the lowest state's visibility in H′ at each a a separate OPEN item:

**Hypothesis UH(ℓ₀), OPEN.** There are a fixed length ℓ₀ = ba, a κ > 0 and a c < 1 with c_κ(ρ_a) ≤ c along the family (a → 0, β following a), uniformly in the time side.

UH holds in d = 2, at ℓ₀ ≥ 4/g along a = ℓ₀/b with β ≥ 1: the proof of Theorem 14 gives ε′ ≤ δ < 1/8 for the coarse weight, a coarse link lies in at most two coarse plaquettes, each with three other link slots and each one factor of w^(b²), and links of one plaquette lie at time distance at most 1, so c_κ ≤ 6ε′e^κ < 1 for κ < log(4/3). Theorem 13 then reads m′ ≥ log(4/3)/ℓ₀, and on a circle H′ = PH, since PH is the class functions of the holonomy, coarse by Proposition 2, and Ω > 0, so m ≥ log(4/3)/ℓ₀, below Theorem 14's value. For d ≥ 3 three things are recorded:

- **The obstruction moves.** Section 4 of YM4-02e has the supremum over fine configurations growing like βL³/(ta²) for the Gaussian. Here the supremum runs over the fixed coarse configurations with the fine fluctuations integrated.
- **Range.** C_ij at large time separation is a long-range term of ρ_a, and bounding it is a clustering estimate. So UH needs a localization of ρ_a, which is YM4-04.
- **Thin lines.** Lines have codimension d − 1. In d = 4 their capacity vanishes in the continuum, so conditioning on them leaves the off links' fluctuations long-ranged, and a Wilson line of fixed length loses its overlap as a falls, CONJECTURE. Block averages condition on a set that fills space. For an abelian gauge field in d = 3, Dimock states exponential decay of the conditional covariance at the block scale (arXiv:1712.10029, eq. 306, 308), crediting the method to Balaban, and for scalars likewise (arXiv:1108.1335). So the line map B here serves the exact identities, and YM4-04 will likely need an average in its place, CONJECTURE: which one, and with which positivity, is OPEN. The gauge-field sources the second seat opened keep a sharp constraint on an average, and Dimock's scalar case is soft, so the axis here is line against average.

## 7a. What the literature holds, as the second seat matched it

[Its report and sources are filed](../reviews/opus55-ym4-03-literature/). The bodies of Balaban's papers and of Lüscher 1983 are CANNOT_SEE from this seat, so what follows on them comes from abstracts and other authors, and from GPT-6's reading where named. On the report's tags, each quotation below is MEASURED as what the named source says, and NAMED as to any body it left unopened.

- **Balaban:** CMP 122, 355, abstract: "This allows us to complete the proof of the ultraviolet stability of four-dimensional pure gauge field theories, as formulated in Theorem 1." Magnen, Rivasseau and Sénéor, in preprint mp_arc 92-38, describe that result as the effective action on the unit lattice staying bounded in finite volume as the spacing falls, with the ultraviolet limit of gauge-invariant observables to follow through a subsequence and uniqueness open. Mitter's survey describes the free energy per unit volume bounded above and below. So, as those authors describe it, the theorem bears on partition functions and effective actions; the text of Theorem 1 and which paper states it are CANNOT_SEE from this seat. GPT-6 reports reading pp. 355–356 on PR #29: Theorem 1 assumes the effective couplings stay in (0, γ] and concludes χ_k exp(−g_k⁻²A(U_k) − E₋|T_η|) ≤ ρ_k ≤ exp(E₊|T_η|), with E± independent of k, T_η and U_k, and Theorem 2, removing the assumption, unpublished then, NAMED here.
- **Decimation:** van Enter, Fernández and Sokal, hep-lat/9210032, Theorem 4.2: decimation with b = 2 on the infinite-volume Ising model in d ≥ 2, for J above J_c of dimension d − 1, is non-quasilocal. Their Theorem 4.6 finds even-b block averaging pathological there too, at large J. Scope: infinite-volume spin systems, where the text's mentions of gauge are reference titles and two remarks. On a finite lattice the matching question is how the effective couplings' range and size behave uniformly as the spacing falls, the second seat's CONJECTURE.
- **Small volume:** the stated form at small physical volume is M(0⁺)L = 2.2696390 g^{2/3} − 0.7975278 g^{4/3} + O(g²), Koller and van Baal, NPB 273, eq. 29, for pure SU(2) on T³ with g renormalized at scale L, as an expansion of an effective Hamiltonian. Read here on the page: van Baal and Koller, Ann. Phys. 174, p. 352, eq. 9.1 with z = L·M_L(0⁺), and eq. 9.2, ΔE/M_L(0⁺) = 0.00767 z^{3/2} exp(−42.6169 z^{−3/2} + 34.2001 z^{−1/2}), valid to z ≈ 1.2, with the words "in no way require M_L(0⁺) to be the mass gap"; and Lüscher's 1988 lectures, pp. 507–513, eq. 4.36, M(A1++) ~ (1/L) Σ ε_k ḡ^{2k/3} in the sector e = 0 on 0 ≤ z ≤ 1, with the flux energy ΔE vanishing to all orders of perturbation theory. So that expansion is the lightest A₁⁺⁺ level of e = 0, and Δ₀ of section 4 lies at or below it: Lüscher's Table 4, p. 512, reads E⁺ and T₂⁺ at 0.86 of M(A₁⁺) at z = 1, with the ratios "practically independent of z" for z ≤ 1 (p. 511), and Koller and van Baal, NPB 273, p. 400, write "In weak coupling the smallest mass is a 2+ state". And ΔE is Δ_flux on the cubic T³, with log ΔE led by −S/g(L) as g(L) → 0, van Baal's review, eq. 12. So the expansion bounds Δ₀ from above, and with ΔE it bounds Δ_full = min(Δ₀, Δ_flux) from above. A value of Δ₀ needs the lowest level of e = 0 in every channel, and a value of Δ_full needs the lowest level of every sector, GPT-6's point on `b577fa8`. Rigorous theorems giving a positive physical gap at fixed small volume, uniform as the spacing falls, located on a small search: 0, so that stays OPEN. Among the sources the seats opened, this expansion is the nearest statement to target 2 of the README, in its sector e = 0 and its channel A₁⁺⁺.
- **Strong coupling:** Shen, Zhu and Zhu, arXiv:2204.12737, hold exponential decay at |β| < 1/(16(d − 1)) in their normalization, which the second seat converts, for SU(2) in d = 4, to β_W < 1/12. Theorem 5 of YM4-02e reads tanh β < 1/14, about β < 0.07155, on (ℤ/L)³.
- **Tomboulis,** arXiv:0707.2179, decimation with reflection positivity, listed by INSPIRE with no journal: Ito and Seiler dispute it at arXiv:0711.4930, 0803.3019, 0901.4246, Tomboulis replies at arXiv:0712.2620, and accepted repairs located on a small search: 0.
- **Finite groups:** on 8⁴ with the Wilson action, Hartung et al., arXiv:2201.09625, Table IV, read the freezing transition at β = 1.15(15), 2.15(15), 3.20(10) and 5.70(20) for Q8, 2T, 2O and 2I.

## 8. What could fail

- **Theorem 9** rests on (a) to (d). The count in (c) needs a free vertex's degree read in distinct nontrivial plaquettes, whatever their multiplicity. The test reads the first dependence at b = 2, on (ℤ/2)⁴ and (ℤ/4)×(ℤ/2)³, with SU(2) averages from 2T. Its row for b = 3 reads the flat filling on (ℤ/3)³. The second seat's separate S³ moments read the law at b = 2 on 13 shapes from 2² to 4×2³ and 6×4×2 over every even multiset, on 4³ and 4⁴ over every even set, and at b = 3 on 8 shapes from 3² to 3⁴ and 6×3³ over every even set, where the flat fillings alone move with V. Repeated plaquettes at b = 3 rest on the proof. At b = 4 on (ℤ/4)³ a tube around the line meets the same count and reads 2⁻³²χ(V_μ)², beside the flat filling's 2⁻³¹χ(V_p′).
- **Theorem 7, item 3** uses that T^b and the projector on H′ commute, which needs H′ invariant under T^b and T^b self-adjoint. The test's W starts from the constant 1, and H′ from Ω. Whether they agree beyond the cases the second seat read is OPEN.
- **Theorem 14** uses Amos's bound as NAMED. The test brackets t_n in integers on a grid of β, and that covers the grid alone.
- **Proposition 11** counts surfaces by hand, and the test enumerates them.
- **The flux rows** read the lowest state of each sector on five small lattices, at one weight each. What Theorem 13 needs along a family is that the level setting Δ_full keeps a positive overlap with one vector of H′ at each a, OPEN. On Q8 the share of e = 0's first excited state in the commutator's vector with Ω taken out is 0.0417, so that row's margin is the smallest: its certificate reads [0.041658959, 0.041658963], and the second seat's exact projection 0.041658961680944. At w = 3 + χ, T on e = 0 has rank 2 there, x⁷⁸ times one quadratic, so the other 0.95834 of that vector lies in T's kernel, and T of that vector, centered, is the first excited state alone.

## 9. The test

[`tests/test_one_scale_blocking.py`](../tests/test_one_scale_blocking.py) runs the rows named in the prediction, integers only, and its output is [`tests/ONE_SCALE_BLOCKING_RECEIPT.txt`](../tests/ONE_SCALE_BLOCKING_RECEIPT.txt). [`one-scale-blocking.yml`](../.github/workflows/one-scale-blocking.yml) is its owning gate. It reads:

| Law | Read |
|---|---|
| Covariance, 64 coarse links at each of b = 2, 3 | All equal, and reversed order, a shifted endpoint and a dropped inverse each differ on 40 or more links |
| Closed loops: plaquette, 1×2, hexagon, winding, at each b | 736 rows at each b equal as group elements. One walk of the path, read in quaternions and in 2×2 matrices, agrees on every row |
| Reflection map at c′ = 0, −1, each b | All equal, and the dropped inverse differs on at least 15 links |
| Two dimensions closes, on Z3, S3, Q8, 2T at b = 2, Z3, S3 at b = 3, on 4×2 and on 4×4 | Every V read equals the closed form. Distinct V read, of all V: 9 of 9 on Z3 at 2×2 and 3×3, 32 of 36 on S3, 32 of 64 on Q8, 12 of 576 on 2T, 7 of 36 on S3 at 3×3, 30 of 81 on Z3 and 6 of 1296 on S3 at 4×2, 12 of 6561 on Z3 and 6 of 1679616 on S3 at 4×4 |
| The first dependence at b = 2, on (ℤ/2)⁴ and (ℤ/4)×(ℤ/2)³, with V on either fine link | Independent of V at order 2, on 18 and 36 multisets, with orders 1 and 3 empty after the center-symmetry filter, and at order 4 equal to the law at two non-central V, by SU(2) averages from 2T. The terms that move with V are the flat fillings, with degree 2 on each free link, so these rows read the same with Q8 or the four points 1, i, j, k in place of 2T. The second seat's S³ moments equal the test's 2T terms one by one, degree 4 included, on all 1,599 and 6,330 terms at V = 1 and at its V_a. At b = 3 the coefficient reads on the flat filling on (ℤ/3)³, with the count of 9 |
| The count in Theorem 9, by search in d = 2, 3, 4, a read added after the prediction | 4 at b = 2 and 9 at b = 3 on every lattice read. b·min(b, 4) at b ≥ 4 stays DERIVED in this test, and the second seat's separate search reads it at b = 4, 5, 6, 7 on (ℤ/b)³ and at b = 4, 5 on (ℤ/b)⁴ |
| The coarse space W, which is H′ in the coordinates of S = BA built from the constant 1 by S^b and the coarse multiplications, on Z2 at 2×2 and at 2×1, S3 and Q8 at 2×1 with b_time = 2, and Z3 at 2×1 with b_time = 3, with the spatial block 2×1 on all but Z2 at 2×2 | W has dimension 20 of 32 on Z2 at 2×2, 33 of 49 on S3, 80 of 176 on Q8, and all of them on Z2 and Z3 at 2×1. Top value of W and of the whole space in one bracket 2 ppm wide, by exact inertia, on all five. Second value on W equal to the whole space's within the bisection's step on the four of at most 60 orbits, a read added after the first complete read and the prediction, and automatic on Z2 at 2×1 and Z3, where W is the whole. The second seat's separate code reads dim H′ = dim W on these five and on Z3 at 2×2, 162 of 243, with the constant 1 inside H′ at 2⁻²⁰⁰⁰ of its norm, and second over top equal on the whole space, W and H′ at 1 ppb: 0.588399, 0.201350, 0.168074, 0.057545, 0.054535 on Q8, and 0.023308 on Z3 at 2×2 |
| T^b against the coarse T on a circle, Z2, Z3, S3, Q8, 2T | Equal as matrices |
| SU(2) in d = 2 at β = 1, 4, 16, 64, 256, 1024, 4096, each a perfect square, so b = 2√β and bag = 4 on every row | δ from 0.0049 to 0.0133, below 1/8, and m/g at least 0.5158 on the bound's own terms, at these β. At b = ⌈2√β⌉ off the squares the same terms read 0.486 at β = 2, 0.447 at β = 3, 0.466 at β = 10 and 0.510 at β = 1000, and down to 0.3439 as β falls to 1, by the second seat |
| Electric flux on Z2 at spatial 2×1, 2×2, 3×1, 3×2 and Q8 at 2×1, with the spatial block equal to those sides, so coarse side 1 in each direction, off section 1's uniform b, and a fine side 1 on three of them, where a plaquette word holds a μ-link twice, with w = 3, 1 on Z2 and w = 3 + χ on Q8 | Z_μ commutes with A and B entry by entry, is one operator on every plane, and the sectors span PH. The top of T lies in e = 0, by exact inertia. A coarse loop winding once changes sign at b = 2, 3 on every plane, 160 of 160 rows on exact quaternions in d = 4, and on orbits in each model, and each flux sector holds a winding function |
| The lowest state of each sector, by a certified overlap from ⟨w, T^{2n} w⟩ with n up to 64 and exact inertia, the whole eigenspace when degenerate | Share of P_e(FΩ) in the lowest eigenspace, for e ≠ 0: 0.95596, 1.00000, 0.95596 on Z2 at 2×1; 0.80332, 0.80332, 0.70110 at 2×2; 0.93097, 1.00000, 0.93097 at 3×1; 0.63990, 0.66443, 0.50155 at 3×2; 0.65850, 0.99977, 0.65216 on Q8, the last of multiplicity 4. In e = 0, the first excited eigenspace's share of the vector with Ω taken out, of multiplicity 1 on all five: 1.00000, 0.78787, 0.75568, 0.61332 on those Z2 lattices, by two insertions F T^b F Ω at b = b_space[0], with F the winding in direction 1 on 2×1 and 3×1 and in direction 0 on 2×2 and 3×2, and 0.04166 on Q8, by one commutator. At 2×1 the 1.00000 follows from e = 0 having dimension 2. With a transverse side of 1 the winding in direction 0 has F T^b F = 2^{−bL₀} T^b on e = 0, exactly, so its vector is a multiple of Ω. The test's Ω is a rational vector u, with sin²(u, Ω) at most its residual squared over the gap squared and \|u\|². So in e = 0 the certificate takes off, at every power 2n, the most Ω's share of the centered vector can add, in place of a fixed slack, and every visibility row carries u's error to the vector built on the exact Ω: it reads MET only when the computed vector's certified part in the level exceeds the most that error can put there, with \|F T^b F\| at most max\|f\|² λ₀^b. On Z2 at 2×1 and 3×1 the winding in direction 0, whose exact vector has part 0 in the first excited level, reads not certified: that is the negative control, and the sabotage `visibility_ignores_omega_error`, which drops the error term, turns it red. That control stands at 2⁻⁹ of its error on 2×1 and 2⁻¹⁹ on 3×1, so it turns red when the error is dropped or cut by a factor above about 519 and 2¹⁹; with the factor 2 dropped, the \|u\|²\|O\|² term dropped, both, sin² read a quarter low, \|w\|² four times high, or the \|O\|² bound set low, every row reads byte for byte, as the second seat's mutation at `2184b54` read. On all five lattices a second exact zero stands near its line: O = 2^{shift+1} S − ⌊2^{shift} λ₀⌋ keeps Ω an eigenvector, so its part in the first excited level is 0, and its centered vector, u's own residual, stands at 0.87351, 0.81845, 0.76289, 0.74909 and 0.92949 of the error, (1 − λ₁/λ₀)² to five digits; it reads rejected, and the sabotage `visibility_error_halved` turns it red with the first control green. u after four steps of S reads its residual's certified share at most 1 with the ground's term taken off and above 1 read bare, and on all 12 calls \|O u\|² stays at or under the \|O\|² bound times \|u\|². The sabotages `visibility_error_inflated` and `overlap_one_power` turn the two-insertion rows and the narrow-bracket rows red. These two corrections are GPT-6's, from its review of `b577fa8`. With coarse side 1 on Z2 every even single coarse function is a constant, so the 4 rows asking for a single insertion read MISS and stay |
| λ₀(e ≠ 0)/λ₀ and λ₁(0)/λ₀, by the same brackets | 0.76707 and 0.06538 on Z2 at 2×1; 0.44872 and 0.09531 at 2×2; 0.88321 and 0.12656 at 3×1; 0.51319 and 0.13450 at 3×2; 0.23353 and 0.03590 on Q8. So Δ_flux < Δ₀ and Δ_full = Δ_flux on all five |
| 2T as a design | Σ_{2T} χ_{n/2} = 0, 0, 0, 0, 0, 24 for n = 1, …, 6, and every monomial of degree at most 5 in the four coordinates averages to its moment on S³, with 20 of the 84 of degree 6 apart |
| Walls, on Z2 at 2×2×2, 4×2×2, 2×4×2 and 2×2×4 and S3 at 2×2 and 4×2 | On the wall configurations read, 6, 4, 4, 4, 6 and 4 of them, each interior group lies in one block, and the whole sum equals the product over groups, with 1, 2, 2, 2, 1 and 2 blocks |

The first complete read, at 175 checks, had one failed check, the sum rule at β = 4: my tolerance missed the tail the sum cuts at n = 60, at 2⁻⁴⁰⁰ of the unit. [That read stays on file](../reviews/fable5-ym4-03-first-run/FIRST-COMPLETE-READ.hbp). The flux section's first read, at 142 checks with its brackets one integer wide, [stays on file too](../reviews/fable5-ym4-03-flux-first-run/FLUX-FIRST-READ.hbp): its lower bounds read 0.994 and 0.967 where the narrower brackets here read 1.00000, and its rows for e = 0 at 2×1 and 3×1, the 0.967 among them, read the winding in direction 0, whose vector the rows above replace.

The test runs narrower than the rows as pushed in these places. `two_dimensions_closes` names Q8 and 2T at b = 3, and they run at b = 2. `integral_identity` names a noncommuting family, and it reads one loop on Z3 and S3 at 2×2, with brute force against elimination carrying the read. `coarse_space` names pencil eigenvalues among those of T^b: it reads closure by rank, and the top and second value by inertia. `su2_character_truncation` names a direct evaluation, which stops at m = 1. `circle_spectrum` skips 2T at L′ = 2.

The second seat's mutation at `6c87200` ran 95 mutants: 42 killed on a named check, 16 caught only by the workflow's cmp, 32 survived, 3 crashed, 2 hit its time limit. The holds it filed against those survivors are in this test, and it read the patched copy at 199 checks with 0 failed, each sabotage on its named check. The rows above the flux section read here byte for byte as that copy reads them. The second seat's mutation of the flux section at `b577fa8` ran 72 mutants on the section alone: 38 killed on a named check, 15 caught only by the workflow's cmp, 13 left every row byte for byte, 4 crashed and 2 hit its time limit. With its holds, 12 of the 14 it aimed at turn a named check red; C03 moves one bracket by 13 units of 10⁻⁹ and stays with cmp, and D23, a change inside the loop of the character sums that keeps their real parts, stays byte for byte, while the monomial read catches the same change made to the 24 points. The second seat's mutation of the corrected certificate at `2184b54` ran 36 mutants of its new and changed lines, each through the test's full output, read with section_flux alone after that read equalled four full runs byte for byte, and through the sabotage `visibility_ignores_omega_error`: 8 killed on a named check, 1 caught only by cmp, 1 only by that sabotage line, and 26 left every row byte for byte with every line passing. Of the 26, 18 move a bound the certificate rests on: the leak term (5), the visibility error (7), the |O|² bound (3), and the two-insertion, narrow and bracket checks made vacuous (3); with its holds each of the 18 turns a named check or a sabotage line red. The other 8 leave every row byte for byte for a measured reason: three move the leak, which stands at most 2⁻⁹⁹⁵ units of 10⁻⁹; two run the same program on these inputs; one enlarges the error, and the accepted rows stand 2¹³⁷⁹ or more above it; two move the e ≠ 0 error, whose rows stand 2¹³⁹⁴ or more above it, and an exact zero for e ≠ 0 within this test stays OPEN.

The workflow runs the test through [`tests/one_scale_replay.py`](../tests/one_scale_replay.py). Its main step computes every section in full and compares the output with the receipt byte for byte. Each level bracket of the flux section comes from [`tests/ONE_SCALE_BLOCKING_BRACKETS.hbp`](../tests/ONE_SCALE_BLOCKING_BRACKETS.hbp) once count_above certifies it, which fixes the pair bisection returns. The record writes an index beside the receipt: for each section, a sha256 key over every function and class it runs, shared helpers included, the module's other code, its data at the section's start and the Python version, with the receipt bytes it printed and their sha256. Each sabotage then computes every section whose covered code compares SABOTAGE with its name and prints the other sections' receipt bytes after their sha256 is checked; covered code that reads the arguments or the module's names any other way, through argv, getattr, globals, vars, locals, eval, exec, `__dict__`, `__import__` or modules, or holds the word sabotage in a string, counts as reached by every sabotage. The sabotage step's read requires every section the index names as reached to have been computed, and a control that reuses section_loops under reversed_order is refused by that read; overlap_skips_next runs once for both its named checks. Five controls run on the replay itself: a stale entry, a key that misses a helper, a tampered row and a stale bracket each exit 1 on a named replay check, and a replay that reuses what reversed_order reaches prints the passing receipt with exit 0, the output the sabotage step refuses. Back to back on one machine, under a load from other work between 2 and 10, the sabotage step took 6,218 s at `bf58ab2` and 381 s and 784 s on the branch, with each sabotage's output byte-identical to the full run's. Projected onto hosted run 42138789854, whose sabotage step took 2,557 s, the branch's takes between 230 s and 265 s by five projections, and the branch's own hosted run measures it. The measurement, its predictions and its replay are in [`reviews/fable5-ym4-03-ci-replay-20261106/`](../reviews/fable5-ym4-03-ci-replay-20261106/). An independent check of that replay, with planted cache faults, the instrumented sections and its own back-to-back timing, is in [`reviews/fable5-ym4-03-ci-replay-check-20261108/`](../reviews/fable5-ym4-03-ci-replay-check-20261108/).
