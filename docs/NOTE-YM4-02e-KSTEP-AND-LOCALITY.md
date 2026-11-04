# YM4-02e: bounds that use the structure of the weights

**Status: DERIVED by the seat ACER-CLAUDE-FABLE5 on November 4, 2026, on the operator's word, with the first theorem to test named by GPT-6. Its exact tests are registered first in [`PREDICTION-YM4-02e.hbp`](PREDICTION-YM4-02e.hbp), pushed before the test existed, and read below. GPT-6, a different model family, reviewed the argument with no contradiction identified, held it for final certification, and then read the final head `6322746`: it recognizes the base Theorem 5 and the k-step propositions as derived, an analytic result on a finite spatial lattice at strong coupling, and recommends lifting the proof and receipt HOLD: [its reviews, verbatim](../reviews/gpt6-ym4-02e/README.md). The second seat's records lane read the test and receipt, with [every number it recomputed in agreement](../reviews/opus55-ym4-02e/README.md). Its first proof lane failed on an output limit and checked nothing. Four narrower lanes then attacked the proofs at `a72a0c3`: [every proof step of Theorem 5 checks by hand and no falsifier was found](../reviews/opus55-ym4-02e/PROOF-LANES.md), with corrections to this text, one of them a formula in section 4, all applied here. The HOLD on the base result is lifted on GPT-6's reading and the operator's word, November 4, 2026. The SU(2) range β < 1/7 and section 4 stay flagged separately, with their acceptance criteria OPEN.**

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

**Proposition 2, NAMED.** τ_k ≥ |θ|^k, and τ_{2k} ≤ τ_k². The second is Birkhoff's: the contraction coefficient of a positive kernel is tanh(Δ/4), and it is submultiplicative, with the diagonal A an isometry of Hilbert's metric. In exact integers, with s_k = √R_k, it reads 4 R_k R_{2k} ≤ (R_k + 1)², and x ≤ τ_k reads R_k ≥ ((1 + x)/(1 − x))². So τ_k^{1/k} is non-increasing along k = 1, 2, 4, 8, and constant on Z2 with one link, where τ_k = |θ|^k, 600000 ppm at each k at q = 1/4.

**Proposition 3, the limit.** Let the eigenvalues of largest modulus after λ₀ share one positive value θλ₀, with orthonormal eigenfunctions h_j, Ω of unit norm, and ρ_j = h_j/Ω. Then τ_k/θ^k tends to

```text
C = (1/4) max over U, U', V, V' of  sum_j ( rho_j(U) - rho_j(U') ) ( rho_j(V) - rho_j(V') ).
```

*Derivation.* K_k(U,V) / (λ₀^k Ω(U) Ω(V)) = 1 + θ^k Σ_j ρ_j(U)ρ_j(V) + o(θ^k), uniformly, so log R_k = θ^k · 4C + o(θ^k), and τ_k = (log R_k)/4 + o(θ^k). ∎ With one eigenfunction, C = osc(h₁/Ω)²/4.

So **the k-th root overshoots by C^{1/k}**. On Z2 at L = 8, k = 8, C reads 6355 thousandths at q = 4/5, 2624 at q = 1/2 and 1000 at q = 1/5, so its size depends on the weight as well as on the lattice. Growth of C with the lattice is proved for independent copies, next. On the interacting ring the second seat derives linear growth as a lower bound, in section 4. On other interacting lattices it is a CONJECTURE, read in the rows below.

**Proposition 4, independent copies.** If T = T₁ ⊗ … ⊗ T₁ with n factors, the four-point ratio is a product, so Δ_k = nΔ_k(T₁), while |θ| stays that of T₁. For Z2 with x = |θ|^k, τ_k = tanh(n artanh x) = ((1+x)ⁿ − (1−x)ⁿ)/((1+x)ⁿ + (1−x)ⁿ), and C = n. The overshoot is at most n^{1/k} and tends to it as x → 0, since tanh(n artanh x)/x rises to n. So **at each fixed k the bound worsens with size, and k ≥ log n / log(1 + η) is enough to hold it to a factor 1 + η, sharp as n x → 0.** The exact condition at (1 + η)|θ| < 1 is n artanh(x) ≤ artanh(((1 + η)|θ|)^k): θ = 3/5, η = 3/5, n = 2 reads τ₁ = 15/17 ≤ 24/25 at k = 1, below that threshold. Z2 on 1×1 and on 1×1×1 are exactly this case, since their plaquette words are trivial.

## 2. Where A enters

At k = 2,

```text
C_2(U,V) = ∫ B(U,W) A(W) B(W,V) dW = prod_l w_2(U_l V_l^-1) * E_{U,V}[ A ],    w_2 = w * w,
```

with E_{U,V} the product over links of the bridge law ∝ w(u x⁻¹) w(x v⁻¹) dx. The four-point ratio factors into that of the convolved weight, whose range tightens, and that of E[A], which carries the plaquettes.

**The smallest case by hand.** Z2 on 2×1 has two self-loops v₁, v₂ and a holonomy W, with A = w(v₁v₂)², so T = T_v ⊗ T_W. With q = 1/2, T_v has, up to the scale 1/4 of Haar measure on the two self-loops, the blocks [[5/4, 1/2], [1/2, 5/16]] on even functions and 3/4, 3/16 on odd ones. So θ = 24/(25 + √481), about 0.51138, and √R_v(k) = (E_k + a^k)/(E_k − a^k), with a = 3/4 and E_k the (1,1) entry of the kth power of that block. At k = 2 the two self-loops read √R_v = 19/10 with A, against 25/16 with A set to 1. So on this lattice A raises the diameter, at q = 1/2, where it binds the self-loops together.

## 3. A bound from locality, with no dependence on the size of the lattice

Let ε = ((M/m) − 1)/((M/m) + 1), which is tanh β for the Wilson weight. Let s(ℓ, ℓ′) be the number of spatial plaquettes holding both of two different links, and σ = ε · max_ℓ Σ_{ℓ′≠ℓ} s(ℓ, ℓ′).

**Theorem 5.** If ε > 0 and 2ε + σ < 1, then every eigenvalue μ ≠ λ₀ of T on H, and so on PH, satisfies

```text
|mu| / lambda_0 <= r = ( (1 - sigma) - sqrt( (1 - sigma)^2 - 4 eps^2 ) ) / (2 eps),
```

the smaller root of ε(x + 1/x) + σ = 1. At ε = 0 the weight is constant and T has rank one, so every μ ≠ λ₀ is 0. On a hypercubic lattice with d spatial dimensions, a link lies in at most 2(d − 1) plaquettes, each holding at most 3 other links, so σ ≤ 6(d − 1)ε on every side, with equality when all sides are at least 2. r increases with σ, so the value at σ = 6(d − 1)ε bounds every lattice with 2ε + 6(d − 1)ε < 1. So **for the SU(2) Wilson weight on (ℤ/L)³ with tanh β < 1/14, about β < 0.07155, λ₁/λ₀ ≤ r(β) at every L**, and r(β) is about tanh β / (1 − 12 tanh β) at small β. The second seat derives a wider SU(2) range, β < 1/7, with ε′ = β/2 in place of tanh β on every step, using the GHS inequality, NAMED and applied by it. That range awaits a different family's review.

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

**What it is sized for.** Theorem 5 covers small β alone, as it must in general: on Z2 with sides L×1, T_v is the transfer matrix of the two-dimensional Ising model, with λ₁/λ₀ tending to ε/q above q_c = √2 − 1 and to 1 below it, by Onsager and Kaufman, NAMED. Small β here is strong coupling, and at fixed physical volume β grows as the spacing falls. So this result is an explicit form of a classical statement, the strong-coupling gap of Osterwalder and Seiler, NAMED, and its gain is the removal of N_ℓ at fixed small β. Dobrushin's condition is used for lattice gauge correlation decay by Chatterjee, arXiv:1811.09770, section 5, NAMED. The closed form for r appeared in none of the few sources the second seat opened, and that search stays open.

## 4. Fixed physical volume

With time step a, take k = t/a. Then, from Proposition 1, the mass in physical units satisfies

```text
m >= (1/a) log(lambda_0/lambda_1) >= (1/t) ( -log tanh( Delta_{t/a} / 4 ) ),
```

so **a bound on Δ_{t/a} uniform in a at one fixed t would give a physical gap, at fixed physical volume.** Whether Δ_{t/a} stays bounded is the question.

- **d = 1.** At fixed physical size with a correlation length fixed in that size, the Ising ring has a scaling limit. The all-up and all-down configurations give fixed boundary states, whose overlaps with the first states have a finite ratio, and at criticality C reads √2, from Cardy's states, NAMED. So C and Δ_{t/a} should stay bounded as L grows at fixed μ = m L_phys, in contrast with independent copies, where C = n is proved, and with fixed q on the interacting ring, where C growing linearly in L is a separate CONJECTURE, also registered. The second seat derives, from Kaufman's sectors, NAMED, that C ≥ L c(q) (1 + O(e^{−κL})) above q_c, with c(q) = (q² + 2q − 1)(1 + q²)/(4q²) and c(4/5) = 1271/1600, and the bound is met on all 13 ring cases it searched, with the maximizer unproved. That is a CONJECTURE, registered and measured here.
- **d ≥ 2, the Gaussian estimate.** For a free field on angles in [−π, π], the Mehler kernel at time t has log-ratio (θ₁ − θ₂)·𝔅·(θ₁′ − θ₂′), with 𝔅 = β sinh(Ω̃)/sinh(kΩ̃) in lattice units, cosh Ω̃ = 1 + κ/2, κ an eigenvalue of the spatial Laplacian. Its entries extend over t/a sites and are positive with row sum β/k at zero mass, so the maximum over the box sits at the constant mode and equals 4π²β (L/a)^d (a/t) = 4π²β L^d/(t a^{d−1}), with mass 4π²β (L/a)^d sinh(Ω̃₀)/sinh(kΩ̃₀). This is bounded in d = 1, and in d = 3 it grows like β L³/(t a²): smooth configurations of large field strength, far outside the typical set, drive it. For t beyond 1/m, the same estimate gives log C about 2 log(1/a), so the bound reads m − (c/t) log(1/a), and it needs t of order log(1/a)/m. That is a CONJECTURE for the interacting theory.

So **for the Gaussian on the box the supremum over all configurations is the obstruction in d ≥ 2, and for the interacting theory that is a CONJECTURE.** The Ising model on L×L at q = 6419/10000, near its critical point, at k = L reads log(K₊₊/K₊₋) of 1.120, 1.397 and 1.600 at L = 3, 4 and 5, with falling increments, where Gaussian scaling holds them constant; three sizes. On the other side, cutting all spatial couplings gives τ_k ≥ tanh(N artanh ε^k) on H for Z2 spin and gauge, by the Griffiths and Ginibre inequalities, NAMED, derived by the second seat. A uniform inequality, a norm that weighs configurations by their probability, or a block-spin argument that moves small β to the coarse lattice: all OPEN.

## What could fail

- **Proposition 3** assumes one positive top value after λ₀. With only a negative value at that modulus it holds at every k, read with |θ|^k, since the maximum is unchanged when U and U′ swap. With both signs at that modulus, τ_k/|θ|^k has one limit along even k, summing every j, and another along odd k, with each j carrying its sign: Z5 on one link with weights 2, 3, 1, 1, 3 has eigenvalues 10, √5 twice, −√5 twice, and reads 5/2 and √5.
- **Theorem 5** rests on the influence bound and the comparison. On small lattices a link can share several plaquettes with a neighbour, or appear twice in one plaquette, and s(ℓ, ℓ′) counts plaquettes for that reason: each plaquette is one factor of w whatever its word.
- **Section 4** is an estimate, tagged as such.

**Falsifiers:** one lattice with |θ| above τ_k^{1/k}, or above r with 2ε + σ < 1, or with 4R_kR_{2k} above (R_k + 1)².

## What is measured

[`tests/test_k_step_locality.py`](../tests/test_k_step_locality.py), in exact integers, against [the prediction](PREDICTION-YM4-02e.hbp), whose first 130 rows were pushed at commit `23cec81`, at 17:43:11Z, before that test was first written, at 17:48:51Z. Its closed forms came by characters and by hand blocks, from [a script with no lattice and no cross-ratio search](../reviews/fable5-ym4-02e-first-run/predict_02e.py). Its neighbours and r came from the same plaquette sum and the same bisection the test uses, and separate code confirms them on all 23 rows. Its rows are in [`tests/K_STEP_LOCALITY_RECEIPT.txt`](../tests/K_STEP_LOCALITY_RECEIPT.txt), and they are finite cases: the theorems' proofs stand or fall on their own.

**The runs.** The first run FAILED two rows and the fourth FAILED one, and those failures stay: [the record](../reviews/fable5-ym4-02e-first-run/README.md). The receipt is the sixth, 615 s on one machine, `failed=0`, which adds the second seat's checks to the fifth, 571 s, loses no row of it, and gains 3 rows, where the fast Z2 engines and the general orbit matrices agree on R_k and the ratio at L = 4 and 5 on L×1 and on 3×2. GPT-6's three conditions on it: all 208 rows of the first run reproduce, 206 identical and 2 changed by the documented correction of the Z3 check; the block solver gives the same characteristic polynomial as direct elimination on 7 small matrices, with exact multiplicities on 4 known spectra, and the same inertia at the listed thresholds on 10 cases, with that scope; and the run-time row reads 1, on the hosted runs as well, against 1,500 s: 403 s on the push and 597 s on the pull request for the fifth at `09ff0f2`, and 538 s and 467 s for the sixth at `52ceaa9`.

**The k-step bound on the actual Wilson form,** at r = 1/2, in parts per million, against the exact ratio on orbits.

| Group | Lattice | N_ℓ | Orbits | k = 1 | k = 2 | k = 4 | k = 8 | Exact |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Q8 | 1×1 | 2 | 28 | 992218 | 914270 | 733471 | 624178 | 529896 to 529897 |
| 2T | 1×1 | 2 | 76 | 992218 | 884002 | 655054 | 534509 | 435408 to 435409 |
| Q8 | 1×1×1 | 3 | 176 | 999512 | 980579 | 851540 | not run | 582784 to 582785 |
| Q8 | 2×1 | 4 | 176 | 997172 | 973463 | 936961 | not run | 874448 to 874449 |

All 199 rows with a sandwich field read 1, so θ_low^k stays at or below τ_k on each. The receipt prints no composition row: the 142 composition checks report only when they fail, and they stand inside `failed=0`. **Closed forms:** 32 of 32 rows match, by characters and by the hand block on Z2 at 2×1, including S3's R₂ = 4473/3025, Q8's √R₂ = 353/128, and 2T's √R₂ = 299/128. **The second seat's five values** on Z2 at 2×2, q = 1/2, agree: 467776, 273970, 200288, 171131 and 158185 at k = 1, 2, 4, 8 and 16, against 146218.

**The limit constant,** read at k = 8 against Proposition 3 and 4.

| Case | C predicted | τ₈/θ⁸, in thousandths |
|---|---:|---:|
| Z2, one link | 1 | 999 to 1001 |
| Z3, one link | 3/2 | 1499 to 1500 |
| S3, one link | 9/4 | 2249 to 2250 |
| Q8, one link | 4 | 3999 to 4000 |
| 2T, one link | 4 | 3999 to 4000 |
| Z2, 2 independent links | 2 | 1999 to 2000 |
| Z2, 3 independent links | 3 | 2997 to 2998 |
| Z2 at 2×1, q = 1/2 | 1 + t² = 1.18769 | 1187 to 1188 |

**Where A enters,** Z2 at 2×1, q = 1/2: √R₂ reads 779/400 with A and 205/128 with A set to 1, as derived by hand, and λ₁/λ₀ reads 511381 to 511382 ppm.

**Fixed q against fixed physical size,** on Z2 at L×1. Fixed q is the interacting case of the CONJECTURE in section 1. Fixed μ holds m L_phys near a chosen value, with q tuned by the Ising law.

| L | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|
| C at q = 4/5, k = 8, thousandths | 1633 | 2391 | 3178 | 3972 | 4766 | 5560 | 6355 |
| C at μ = 1, k = 2L, thousandths | 1213 | 1355 | 1449 | 1512 | 1558 | 1592 | 1615 |
| C at μ = 2, k = 2L, thousandths | 1356 | 1579 | 1731 | 1844 | 1928 | 1979 | 2037 |
| τ_L at μ = 1, ppm | 288373 | 321488 | 350863 | 371288 | 384117 | 393455 | 402412 |
| τ_L at μ = 2, ppm | 147675 | 172951 | 193329 | 205726 | 214322 | 225214 | 227937 |

So at fixed q, C rises by 0.79 per site from L = 4, inside the predicted 0.55 to 0.95. At μ = 1, C rises by 142, 94, 63, 46, 34 and 23 thousandths per site. At μ = 2 it rises by 223, 152, 113, 84, 51 and 58, and q, rounded to three digits, gives (ε/q)^L of 137078 ppm at L = 7 and 134227 ppm at L = 8, against e⁻² = 135335 ppm, a CONJECTURE for why the last step is the larger. The second seat reads it with q from the exact law: the steps fall at every L, 61678 then 48568 millionths at L = 7 and 8, MEASURED, so the larger last step is the rounding of q. τ at k = L, one unit of physical time, rises at each L to 402412 ppm at μ = 1 and 227937 ppm at μ = 2, at L = 8. That range is short, and whether either settles is OPEN. With q from the exact law, the second seat's closed form reads C = 1.822229 and 2.431210, and τ at k = L = 451699 and 274671 ppm, at L = 512, with deficits halving per doubling, toward C = 1.825727 and 2.438510 from a product formula in [its findings](../reviews/opus55-ym4-02e/proof-lanes/volume/FINDINGS.txt), a CONJECTURE checked to 5 digits.

**Conjectures read: 9 of 10 met,** in `YM4_02E_CONJ_READ` rows. **The miss:** C at μ = 2 passes the registered ceiling of 1.8, reaching 2.037 at L = 8. By the second seat's closed form, the limit at μ = 1 also passes 1.8, between L = 64 and L = 128, and reaches 1.8257. The Ising limits came out as registered: λ₁/λ₀ rises to 138889 ppm at q = 4/5, against 5/36, and to 652334 ppm at L = 6 at q = 1/2, below 2/3, and reaches 999666 ppm at q = 1/5, in the ordered phase.

**Theorem 5.** All 29 rows with 2ε + σ < 1 read within r, on orbits and on 6 all-configuration cases.

| Group, weight | Lattices | r, ppm | Largest ratio read, ppm | τ from the range, ppm, at the largest lattice |
|---|---|---:|---:|---:|
| Z2, q = 4/5 | 2×1 to 6×1 | 208713 | 138889 | 871399 |
| Z2, q = 4/5 | 2×2, 3×2 | 381967 | 12670 | 871399 |
| Z2, q = 7/8 | 2×2×1 | 145899 | 87018 | 664701 |
| Z3, 1, 8/9, 8/9 | 2×2 | 91674 | 1606 | 439114 |
| Q8, r = 19/20 | 1×1×1 | 130697 | 29470 | 298398 |

The first row is the point of the theorem: r stays fixed as L grows, while τ from the range climbs toward 1. These lattices are small, and the theorem's claim at every L stands on its proof.

**The controls.** Plaquette ratios on Z3, S3, Q8 and 2T are now pinned, including Q8 on 1×1×1 and Z3 on 2×2 at the second seat's values. The negative eigenvalue on Z2 with w = 1/4, 1 reads −3/8, with equality, and the certificate's negative side reads it. Seven sabotages each exit 1 on their named check.

**Seen after the run, in no prediction.** On Z2 at L×2, q = 4/5, C reads 3936, 2951 and 3935 thousandths at L = 2, 3 and 4, against 12665 to 12670 ppm for the ratio, near ε² = 12346. A reading, CONJECTURE: the lightest excitations are loops around the side of length 2, L of them when L ≥ 3 and 2 + 2 at L = 2, and C counts them.
