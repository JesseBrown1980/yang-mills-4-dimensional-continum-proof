# Exact target: four-dimensional continuum Yang–Mills existence and mass gap

**Claim status: OPEN.** This repository works toward a proof.

## Official problem

For every compact simple gauge group G, construct a nontrivial quantum Yang–Mills theory in four spacetime dimensions, satisfying axiomatic quantum-field-theory requirements at least as strong as those in the Jaffe–Witten problem statement, and prove a strictly positive mass gap Δ > 0.

**Initial case:** continuous SU(2), pure gauge (no matter fields). An SU(2) theorem would cover one group, and the Clay statement quantifies over all compact simple groups.

## Finite Euclidean starting point

For a finite periodic hypercubic lattice Λ ⊂ ℤ⁴, give each positively oriented link U_μ(x) ∈ SU(2). For μ < ν define

```text
U_{μν}(x) = U_μ(x) U_ν(x+μ) U_μ(x+ν)^(-1) U_ν(x)^(-1)
S_W(U; β) = β sum_{x, μ<ν} [1 - (1/2) Re Tr U_{μν}(x)]
Z_{Λ,β} = integral (product_links dHaar(U_ℓ)) exp(-S_W(U; β)).
```

With β ≥ 0, the normalized Haar probability measure and compactness give `0 < Z_{Λ,β} ≤ 1` at **fixed finite volume**: the integrand is continuous and strictly positive, and the action is nonnegative. That is a standard finite-lattice existence fact.

The site gauge law is `U_μ(x) -> g(x) U_μ(x) g(x+μ)^(-1)`. Each plaquette transforms by conjugation and its trace is invariant. The first executable lemma tests this using exact rational SU(2) quaternions on a 2×2×2×2 lattice.

## Actual acceptance gates

1. Define a consistent renormalized weak-coupling trajectory as the lattice spacing a→0 and physical volume→∞, with controlled order/compatibility of limits.
2. Prove nonperturbative, volume- and scale-uniform estimates, with explicit control of large fields, localization, ultraviolet behavior and infrared behavior. Perturbative asymptotic freedom gives the trajectory its form, and these estimates have to hold beyond it.
3. Construct **nontrivial** continuum, gauge-invariant correlation functions and establish the required Osterwalder–Schrader axioms.
4. Reconstruct a physical quantum theory with a Hilbert space, vacuum, locality, energy positivity and suitable Wightman properties.
5. Prove that the **physical** excitation spectrum above the vacuum has `Δ > 0` in physical units. In transfer-matrix terms, a lattice-unit gap must be rescaled by 1/a and controlled uniformly through the limits.
6. Explain and prove the extension to every compact simple group, or preserve an explicit SU(2)-only scope.

The finite S₃ spectral bounds and the finite SU(2) subgroups Q8, 2T, 2O and 2I are separate finite models. Each result keeps its own scope, and anything carried to continuous SU(2) comes with its own argument.

Official source: https://www.claymath.org/millennium/yang-mills-the-maths-gap/
