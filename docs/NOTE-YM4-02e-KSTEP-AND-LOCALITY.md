# YM4-02e: bounds that use the structure of the weights

**Status: DERIVED by the seat ACER-CLAUDE-FABLE5 on November 4, 2026, on the operator's word, with the first theorem to test named by GPT-6. Its exact tests are registered first in [`PREDICTION-YM4-02e.hbp`](PREDICTION-YM4-02e.hbp), pushed before the test existed. The second seat's attack and a different model family's reading are OPEN.**

**Scope:** one finite periodic lattice and one β, except section 3, which holds on every periodic lattice at small β. The objects are those of [YM4-02d](NOTE-YM4-02d-QUANTITATIVE-GAP.md): T = A^{1/2} B A^{1/2} on H = L²(G^{N_ℓ}), with θ = μ/λ₀ for an eigenvalue μ ≠ λ₀. Zero spacing at fixed finite physical volume stays OPEN.

YM4-02d gives |θ| ≤ τ from the range of w and the number of links, and its second proof shows τ is the exact supremum over positive multipliers. So a better dependence on N_ℓ has to use the form of A or B. This note uses two forms: T^k, where A enters from k = 2, and locality, where each factor of A and B touches few links.

## 1. The k-step bound

T^k has the kernel K_k(U,V) = A(U)^{1/2} C_k(U,V) A(V)^{1/2}, with C_1 = B and C_{j+k} = C_j A C_k. The outer factors cancel from every four-point ratio, so define

```text
R_k = the largest of C_k(U,V) C_k(U',V') / ( C_k(U,V') C_k(U',V) ),
Delta_k = log R_k,    tau_k = tanh(Delta_k / 4) = (sqrt(R_k) - 1) / (sqrt(R_k) + 1).
```

**Proposition 1.** Every eigenvalue μ ≠ λ₀ satisfies |μ|/λ₀ ≤ τ_k^{1/k}, on H with the kernel on H and on PH with the kernel on orbits.

*Proof.* T^k has a continuous, strictly positive, symmetric kernel, with top eigenvalue λ₀^k, eigenfunction Ω, and μ^k on the same eigenfunction as μ. The second proof of YM4-02d, which uses only those properties and the bound on the four-point ratio, gives |μ|^k/λ₀^k ≤ τ_k. ∎

**Proposition 2, NAMED.** τ_k ≥ |θ|^k, and τ_{2k} ≤ τ_k². The second is Birkhoff's: the contraction coefficient of a positive kernel is tanh(Δ/4), and it is submultiplicative, with the diagonal A an isometry of Hilbert's metric. In exact integers, with s_k = √R_k, it reads 4 R_k R_{2k} ≤ (R_k + 1)², and x ≤ τ_k reads R_k ≥ ((1 + x)/(1 − x))². So τ_k^{1/k} falls along k = 1, 2, 4, 8.

**Proposition 3, the limit.** Let the eigenvalues of largest modulus after λ₀ share one positive value θλ₀, with orthonormal eigenfunctions h_j and ρ_j = h_j/Ω. Then τ_k/θ^k tends to

```text
C = (1/4) max over U, U', V, V' of  sum_j ( rho_j(U) - rho_j(U') ) ( rho_j(V) - rho_j(V') ).
```

*Derivation.* K_k(U,V) / (λ₀^k Ω(U) Ω(V)) = 1 + θ^k Σ_j ρ_j(U)ρ_j(V) + o(θ^k), uniformly, so log R_k = θ^k · 4C + o(θ^k), and τ_k = (log R_k)/4 + o(θ^k). ∎ With one eigenfunction, C = osc(h₁/Ω)²/4.

So **the k-th root overshoots by C^{1/k}**, and the size of C says how much of the lattice the worst pair of configurations can read. Growth of C with the lattice is proved for independent copies, next. On interacting lattices it is a CONJECTURE, read in the rows below.

**Proposition 4, independent copies.** If T = T₁ ⊗ … ⊗ T₁ with n factors, the four-point ratio is a product, so Δ_k = nΔ_k(T₁), while |θ| stays that of T₁. For Z2 with x = ρ^k, τ_k = tanh(n artanh x) = ((1+x)ⁿ − (1−x)ⁿ)/((1+x)ⁿ + (1−x)ⁿ), and C = n. The overshoot is n^{1/k}, so **at each fixed k the bound worsens with size, and holding it to a factor 1 + η needs k ≥ log n / log(1 + η).** Z2 on 1×1 and on 1×1×1 are exactly this case, since their plaquette words are trivial.

## 2. Where A enters

At k = 2,

```text
C_2(U,V) = ∫ B(U,W) A(W) B(W,V) dW = prod_l w_2(U_l V_l^-1) * E_{U,V}[ A ],    w_2 = w * w,
```

with E_{U,V} the product over links of the bridge law ∝ w(u x⁻¹) w(x v⁻¹) dx. The four-point ratio factors into that of the convolved weight, whose range tightens, and that of E[A], which carries the plaquettes.

**The smallest case by hand.** Z2 on 2×1 has two self-loops v₁, v₂ and a holonomy W, with A = w(v₁v₂)², so T = T_v ⊗ T_W. With q = 1/2, T_v has the blocks [[5/4, 1/2], [1/2, 5/16]] on even functions and 3/4, 3/16 on odd ones. So θ = 24/(25 + √481), about 0.51138, and √R_v(k) = (E_k + a^k)/(E_k − a^k), with a = 3/4 and E_k the (1,1) entry of the kth power of that block. At k = 2 the two self-loops read √R_v = 19/10 with A, against 25/16 with A set to 1. So on this lattice A raises the diameter, at q = 1/2, where it binds the self-loops together.

## 3. A bound from locality, with no dependence on the size of the lattice

Let ε = ((M/m) − 1)/((M/m) + 1), which is tanh β for the Wilson weight. Let s(ℓ, ℓ′) be the number of spatial plaquettes holding both of two different links, and σ = ε · max_ℓ Σ_{ℓ′≠ℓ} s(ℓ, ℓ′).

**Theorem 5.** If 2ε + σ < 1, then every eigenvalue μ ≠ λ₀ of T on H, and so on PH, satisfies

```text
|mu| / lambda_0 <= r = ( (1 - sigma) - sqrt( (1 - sigma)^2 - 4 eps^2 ) ) / (2 eps),
```

the smaller root of ε(x + 1/x) + σ = 1. On a hypercubic lattice with d spatial dimensions and sides at least 3, σ = 6(d − 1)ε. So **for the SU(2) Wilson weight on (ℤ/L)³ with tanh β < 1/14, about β < 0.0716, λ₁/λ₀ ≤ r(β) at every L**, and r(β) is about tanh β / (1 − 12 tanh β) at small β.

*Proof, on H.* The chain of Gibbs measures. For n ≥ 3 let μ_n be the measure on (G^{N_ℓ})^n with density ∝ Π_t A(x_t) B(x_t, x_{t+1}), t in ℤ/n, so its normalization is tr Tⁿ. With n ≥ 3 each link has two different time neighbours, and slices 1 and n − 1 are the two neighbours of slice 0. Let h be a real unit eigenfunction for μ ≠ 0, λ₀, and f = h/Ω, bounded and continuous. T is compact and self-adjoint with λ₀ simple and |θ| < 1 for the rest, by Step 3 of YM4-02d, and T² is trace class. So at fixed t, as n → ∞, Tⁿ⁻ᵗ/λ₀ⁿ⁻ᵗ tends in trace norm to the projector on Ω, and tr Tⁿ/λ₀ⁿ tends to 1. So E_{μ_n}[f(x₀)] → ⟨Ω, fΩ⟩ = ⟨Ω, h⟩ = 0 and

```text
E_{mu_n}[ f(x_0) f(x_t) ] -> <h, T^t h> / lambda_0^t = theta^t.
```

*Local influences.* The conditional law π_i of one link i = (ℓ, t) given the rest has a density that is a product of w over the two time neighbours and the plaquettes holding ℓ. One plaquette is one factor of w, however many times a link appears in its word, which is what matters on sides 1 and 2. So changing one neighbour multiplies that density by a factor in [(m/M)^s, (M/m)^s], where s is the number of factors it enters: 1 for a time neighbour, and s(ℓ, ℓ′) within the slice. For two probability laws whose density ratio has largest over smallest at most S, the total variation is at most (√S − 1)/(√S + 1): with E = {p > q}, a = q(E), b = p(E), and r₊, r₋ the extremes of p/q, TV = b − a ≤ min((r₊ − 1)a, (1 − r₋)(1 − a)) ≤ (r₊ − 1)(1 − r₋)/(r₊ − r₋), which is largest at r₊ = √S. So the influence C_ij = sup TV(π_i(·|x), π_i(·|x′)), over x, x′ differing at j, is at most ε for each time neighbour and at most tanh(s(ℓ, ℓ′) artanh ε) ≤ s(ℓ, ℓ′) ε within the slice, since tanh is subadditive on the positive half-line. The density and the bound are the same at every slice of ℤ/n. The paths that wrap around the periodic boundary are counted in the walk below, and they vanish in the limit taken there. Each row of C sums to at most c = 2ε + σ < 1.

*Comparison.* Let δ_j(g) be the largest change of g at site j. Let μ, μ′ be two laws on the sites with conditional laws π_i, π′_i, with b_i = sup TV(π_i, π′_i). Then for a function g,

```text
|mu(g) - mu'(g)| <= sum_a sum_j b_a D_ja delta_j(g),    D = sum over m >= 0 of C^m.
```

Indeed δ_i(π_i g) = 0 and δ_j(π_i g) ≤ δ_j(g) + C_ij δ_i(g), and (μ − μ′)(g) = (μ − μ′)(π_i g) + μ′(π_i g − π′_i g), with the last term at most δ_i(g) b_i. Sweep the sites cyclically with g₀ = g and g_s = π_{i_s} g_{s−1}. Each visit moves the mass δ_{i_s} to the other sites with total factor at most c, so one full sweep multiplies Σ_j δ_j by at most c, and g_s tends to a constant. Let w_a be the sum of δ_a(g_{s−1}) over the visits to a. Mass reaching a is either initial or arrives from a visit to some b with factor C_ba, so w ≤ δ(g) + Cᵀ w, and w_a ≤ Σ_j D_ja δ_j(g). Summing the visits gives the inequality. This is Dobrushin's comparison theorem, NAMED: Dobrushin 1968, Föllmer 1982. The proof here stands alone.

*The walk.* Fix x₀ and x₀′ differing at one link ℓ of slice 0, and take the laws of μ_n given each. Only (ℓ, ±1) have b ≠ 0, with b ≤ ε. Let g = f(x_t). Summing over the links changed from x₀ to x₀′, one at a time, gives

```text
| E[f(x_t) | x_0] - E[f(x_t) | x_0'] | <= eps * ( sum_j delta_j(f) ) * ( G(t -> 1) + G(t -> -1) ),
```

where G(x → y) bounds the sum over slices of D: from a site, a path moves one slice up or down with weight at most ε and stays in the slice with total weight at most σ. Removing slice 0 removes paths, so G is at most the Green's function of a walk on ℤ/n. On ℤ, 1/(1 − σ − ε(z + 1/z)) has coefficients r^{|m|}/√((1−σ)² − 4ε²). On ℤ/n the paths wrap and are counted. With D = √((1−σ)² − 4ε²) and 0 ≤ d < n, the Green's function at separation d is G_n(d) = Σ_{w in ℤ} r^{|d+wn|}/D = (r^d + r^{n−d})/(D(1 − r^n)), the closed form GPT-6 wrote out in its review. Since r < 1, at fixed d it tends to r^d/D as n → ∞.

*The end, with the limits in this order.* At fixed N_ℓ, h and t, let n → ∞: |θ|^t = lim |Cov_{μ_n}(f(x₀), f(x_t))| ≤ ‖f‖_∞ · ε · (Σ_j δ_j(f)) · (r^{t−1} + r^{t+1}) / √((1−σ)² − 4ε²). The constant depends on N_ℓ and h and holds at every t. Now let t → ∞: |θ| ≤ r. ∎

*On PH.* T commutes with the gauge projection P, and Ω, the unique positive top eigenfunction, is gauge invariant. So every eigenvalue of T on PH other than λ₀ is an eigenvalue on H other than λ₀, and the bound carries over.

**What it is and is not sized for.** Theorem 5 covers small β alone, as it must in general: on Z2 with sides L×1, T_v is the transfer matrix of the two-dimensional Ising model, with λ₁/λ₀ tending to ε/q above q_c = √2 − 1 and to 1 below it, by Onsager and Kaufman, NAMED. Small β here is strong coupling, and at fixed physical volume β grows as the spacing falls. So this result is an explicit form of a classical statement, the strong-coupling gap of Osterwalder and Seiler, NAMED, and its gain is the removal of N_ℓ at fixed small β.

## 4. Fixed physical volume

With time step a, take k = t/a. Then, from Proposition 1, the mass in physical units satisfies

```text
m >= (1/a) log(lambda_0/lambda_1) >= (1/t) ( -log tanh( Delta_{t/a} / 4 ) ),
```

so **a bound on Δ_{t/a} uniform in a at one fixed t would give a physical gap, at fixed physical volume.** Whether Δ_{t/a} stays bounded is the question.

- **d = 1.** At fixed physical size with a correlation length fixed in that size, the Ising ring has a scaling limit. The all-up and all-down configurations give fixed boundary states, whose overlaps with the first states have a finite ratio, and at criticality C reads √2, from Cardy's states, NAMED. So C and Δ_{t/a} should stay bounded as L grows at fixed μ = m L_phys, in contrast with independent copies, where C = n is proved, and with fixed q on the interacting ring, where C growing linearly in L is a separate CONJECTURE, also registered. That is a CONJECTURE, registered and measured here.
- **d ≥ 2, the Gaussian estimate.** For a free field on angles in [−π, π], the Mehler kernel at time t has log-ratio (θ₁ − θ₂)·𝔅·(θ₁′ − θ₂′), with 𝔅 = β Ω̃/sinh(kΩ̃) in lattice units. Its entries extend over t/a sites, and the maximum over the box is about β (L/a)^d (a/t) = β L^d/(t a^{d−1}). This is bounded in d = 1, and in d = 3 it grows like β L³/(t a²): smooth configurations of large field strength, far outside the typical set, drive it. For t beyond 1/m, the same estimate gives log C about 2 log(1/a), so the bound reads m − (c/t) log(1/a), and it needs t of order log(1/a)/m. That is a CONJECTURE for the interacting theory.

So **the supremum over all configurations looks like the obstruction in d ≥ 2.** A uniform inequality, a norm that weighs configurations by their probability, or a block-spin argument that moves small β to the coarse lattice: all OPEN.

## What could fail

- **Proposition 3** assumes one positive top value after λ₀. With a negative top value it holds along even k.
- **Theorem 5** rests on the influence bound and the comparison. On small lattices a link can share several plaquettes with a neighbour, or appear twice in one plaquette, and s(ℓ, ℓ′) counts plaquettes for that reason: each plaquette is one factor of w whatever its word.
- **Section 4** is an estimate, tagged as such.

**Falsifiers:** one lattice with |θ| above τ_k^{1/k}, or above r with 2ε + σ < 1, or with 4R_kR_{2k} above (R_k + 1)².

## What is measured

Filled from the receipt after the run, against [the prediction](PREDICTION-YM4-02e.hbp).
