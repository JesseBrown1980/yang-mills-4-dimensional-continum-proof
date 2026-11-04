# YM4-02d: an explicit gap at each fixed lattice

**Status: DERIVED by the seat ACER-CLAUDE-FABLE5 on November 4, 2026. GPT-6, a different model family, read the proof the same day, verified it, and added the full-space route in Step 4: [its report, verbatim](../reviews/gpt6-quantitative-gap/README.md). The exact tests are registered first in [`PREDICTION-YM4-02d.hbp`](PREDICTION-YM4-02d.hbp). The second seat's attack is OPEN.**

**Scope:** one finite periodic lattice and one β > 0. The objects are those of [section 7 of Lemma 0004](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/blob/ym4-02c-reflection-transfer/docs/LEMMA-0004-REFLECTION-TRANSFER.md), on draft PR #14 under the operator's HOLD, and they are written out here so this note reads alone. Theorem 5 there gives 0 < λ₁ < λ₀, and Proposition 6 there bounds λ₀. This note bounds the ratio. Zero spacing at fixed finite physical volume stays OPEN.

## The statement

Let G be a compact group and w a continuous class function on G with w(g⁻¹) = w(g) and 0 < m ≤ w ≤ M. Take a finite periodic spatial lattice with N_ℓ links and N_s plaquettes, and H = L²(G^{N_ℓ}) with normalized Haar measure. Define

- A(U), the product of w(U_p) over the spatial plaquettes,
- B(U,V), the product of w(U_ℓ V_ℓ⁻¹) over the spatial links,
- T = A^{1/2} B A^{1/2},
- P, the projector onto gauge-invariant functions.

T has a continuous, strictly positive kernel. By the argument of Theorem 5(d), its largest eigenvalue λ₀ is simple, with a strictly positive continuous eigenfunction Ω, which is gauge invariant.

**Proposition.** Every eigenvalue μ ≠ λ₀ of T on H, and so on PH, satisfies

```text
|mu| <= tau * lambda_0,    tau = ((M/m)^N_links - 1) / ((M/m)^N_links + 1).
```

For the Wilson weight w = exp(−β(1 − ½ Re Tr U)) on SU(2), m = exp(−2β) and M = 1, so τ = tanh(β N_ℓ):

```text
lambda_1 / lambda_0 <= tanh(beta N_links) < 1,
log(lambda_0 / lambda_1) >= -log tanh(beta N_links) > 0.
```

N_ℓ is the count of spatial links, 3L³ on (ℤ/L)³. The spatial weights A play no part in the bound.

## The proof

**Step 1, the cross-ratio.** Let K(U,V) = A(U)^{1/2} B(U,V) A(V)^{1/2} be the kernel of T. In the four-point ratio

```text
K(U,V) K(U',V') / ( K(U,V') K(U',V) ) = B(U,V) B(U',V') / ( B(U,V') B(U',V) )
```

every factor of A cancels. Each value of B lies in [m^{N_ℓ}, M^{N_ℓ}], so the ratio is at most R = (M/m)^{2N_ℓ}.

**Step 2, the contraction.** On the cone C of strictly positive continuous functions on G^{N_ℓ}, Hilbert's projective metric is d(f,g) = log( max(f/g) / min(f/g) ). T maps C into C. For f, g in C,

```text
(Tf)(U) (Tg)(U') / ( (Tg)(U) (Tf)(U') )
  = ∫∫ K(U,V) K(U',V') f(V) g(V') dV dV' / ∫∫ K(U,V') K(U',V) f(V) g(V') dV dV',
```

and the integrands have ratio at most R pointwise. So the image of C has projective diameter Δ ≤ log R = 2N_ℓ log(M/m). Birkhoff's theorem says T contracts d by the factor tanh(Δ/4). With x = (M/m)^{N_ℓ}, tanh((log x)/2) = (x − 1)/(x + 1), which is τ.

**Step 3, from the contraction to the eigenvalue.** T is self-adjoint and compact, so μ is real, and μ = 0 needs nothing. Let μ ≠ 0, λ₀ with real eigenfunction h, continuous because h = Th/μ and the kernel is continuous. h is orthogonal to Ω > 0, so it changes sign, and ρ = h/Ω is continuous and nonconstant. By Theorem 5(d)'s argument, |θ| < 1 for θ = μ/λ₀. Take ε > 0 small enough that f = Ω(1 + ερ) lies in C. Then

```text
T^n f = lambda_0^n Omega (1 + eps theta^n rho),
d(T^n f, T^n Omega) = log( max(1 + eps theta^n rho) / min(1 + eps theta^n rho) ) = eps |theta|^n osc(rho) (1 + o(1)).
```

Iterating Step 2, the left side is at most τⁿ d(f, Ω), a constant times τⁿ. Taking nth roots gives |θ| ≤ τ. ∎

**Step 4, the gauge-invariant sector, two routes.**

*Route 1, GPT-6's, on the full space.* The proof above runs on all of H, with no projection. Ω is gauge invariant and PH is invariant under T, so λ₀ is the top eigenvalue on PH and every other eigenvalue on PH is one of the μ above. So λ₁ on PH is at most τ λ₀.

*Route 2, on the orbits.* The projected kernel is (BP)(U,V) = ∫ B(U, V^g) dg. An average of values in [m^{N_ℓ}, M^{N_ℓ}] stays there, so Steps 1 to 3 run on the space of gauge orbits with the same R.

The two routes differ in one way: on H the first eigenvalue after λ₀ can belong to a gauge-noninvariant function, and it is at most τλ₀ too.

## Where it is sharp and where it is loose

**Sharp in this generality.** Z2 on one link, with w = 1 at the identity and q at the other element, has N_ℓ = 1, M/m = 1/q and T = ½[[1, q], [q, 1]], with eigenvalues (1 ± q)/2. So λ₁/λ₀ = (1 − q)/(1 + q) = τ, and no smaller constant holds for all such weights.

**Loose with many links.** The bound sees only the range of each weight and the number of links. GPT-6's float diagnostic on Z2 at N_ℓ = 8 reads 0.146 against 0.992.

**What it says as the lattice grows.** −log tanh x = 2 exp(−2x)(1 + O(exp(−4x))), so the bound in lattice units falls like 2 exp(−2βN_ℓ). At fixed physical size, L = L_phys/a grows as a → 0, and (1/a)(−log tanh(βN_ℓ)) goes to 0. So this result sizes the gap at each fixed lattice, and carrying a gap to zero spacing needs a dependence on N_ℓ far better than this. That is OPEN.

## What could fail

- **Step 2** rests on Birkhoff's theorem, NAMED: G. Birkhoff, *Extensions of Jentzsch's theorem*, Trans. AMS 85 (1957), in the form stated by [Lemmens and Nussbaum](https://arxiv.org/abs/1304.7921) and [Reeb, Kastoryano and Wolf](https://arxiv.org/abs/1102.5170). This seat read those statements and did not rework Birkhoff's own proof.
- **Step 3** needs ρ bounded and nonconstant, which continuity of h and Ω > 0 give, and |θ| < 1, which Theorem 5(d)'s argument gives for this strictly positive kernel.
- **The Wilson case** needs w > 0, so it holds for every real β in the bound's form, with m and M read off the weight. Theorem 5 and this statement are written for β > 0.

**Falsifier:** one positive symmetric class weight in [m, M], on one lattice, with a non-leading eigenvalue of modulus above τλ₀.

## What is measured

Nothing yet, at the commit that adds this note. [The prediction](PREDICTION-YM4-02d.hbp) lists exact spectra from characters, plaquette cases with their orbit counts, GPT-6's float values as already seen, both routes, broken-kernel controls and sabotages.
