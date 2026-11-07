# YM4-03b: Three S₃ spatial slices, ternary transfer jumps, and excitation visibility

**Dated 2026-11-06. Status:** predictions FROZEN at `5341070050a57192bcd1019bd7792193f154887b` *before* the test implementation; algebraic results MEASURED in the exact integer reference run and subject to independent hosted replay. **This is a 1+1-dimensional finite-group S₃ gauge-transfer verification, not the 3×4 S₃ Hamiltonian eigensystem, 4D SU(2), or a continuum proof.**

## What was tested

Start with S₃ and the same standard-character magnetic penalty used by the 2D finite Hamiltonian project, `m(g)=2−chi_std(g)`, but in a **separate Euclidean 1+1D Wilson transfer model**, with `beta=ln 2`. The local weight is `w(g)=exp(−beta*m(g))`: on the six group elements its integer-normalized values are `8` at the identity, `2` at each transposition, and `1` at each 3-cycle, summing to 16. This normalization gives a symmetric, positive, row-stochastic convolution transfer kernel
[
K(g,h)=\frac{w(gh^{-1})}{\sum_{u\in S_3}w(u)}.
]
The spatial holonomy is gauge-covariant by conjugation. The character observables `chi_std` and `sign` are gauge invariant. The operator on their 3D gauge-invariant class-function subspace has the trivial eigenvalue `1` and the nontrivial eigenvalues `7/16` and `1/4`. Both are positive.

For a spatial ring with `L` fine plaquettes, integrating the intermediate links gives `T_L=K^L`. For `L_f=9`, block spatial and temporal lengths by `b=3`, using the **exact induced** local weight `K_3=K^(3×3)=K^9` and `L_3=3`. Block once more to `b=9` with `K_9=K^81` and `L_9=1`. The induced transfers are therefore
[
T_1=K^9,\quad T_3=(K^9)^3=K^{27}=T_1^3,\quad
T_9=(K^{81})^1=K^{81}=T_1^9=T_3^3.
]
Every comparison is equality of **all 36 exact rational kernel entries**, not merely a plotted spectrum.

### Independent calculation paths

1. Direct exact-integer multiplication of the 6×6 integer numerator `A=16K` for small exponents.
2. Base-three matrix exponentiation by repeated cubing, valid for this **noncommutative S₃ group**; the ring-NTT shortcut of Matrix Law Essentials is not assumed to apply.
3. An independently derived S₃ character formula for every `n>=1`:
[
(16K)^n_{g,h}=\frac{16^n+4^n\operatorname{sgn}(gh^{-1})+
2\cdot 7^n\chi_{\rm std}(gh^{-1})}{6}.
]
The right-hand side has integer entries. The test compares it with the ternary route through the `n=2187` underlying plaquette-transfer power.

### Gauge-invariant excitation and mass-gap comparison

For the standard-character Wilson holonomy observable, `C_std(t)=<(chi_std)_t (chi_std)_0> = (7/16)^(9t)`, where `t` is the number of *fine* temporal ticks. The sign character gives `C_sign(t)=(1/4)^(9t)`. These are connected correlations with zero one-point means. For physical time `t_phys=t*a` and coarse time steps `3a` and `9a`, exact triple-scale agreement holds for fine `t=9,27,81,243` and the corresponding coarse times `t/3,t/9`.

The first nontrivial eigenvalue ratio is `(7/16)^(9b)` for the `b`-coarsened spatial ring; the **physical transfer gap** is therefore exactly
[
\Delta_b=-\frac{\log[(7/16)^{9b}]}{ba}
=\frac9a\log\frac{16}{7}
\approx\frac{7.440107158660211}{a}.
]
The `a` here is a declared lattice time interval; no Planck-time or SI calibration is inferred. Exact equality of ratios at these three scales is a **solvable blocking identity**, not evidence that the 4D theory has a nonzero continuum mass gap.

### A crucial failed closure test

A one-parameter Wilson class factor of the form `w(g)=C*(1,z²,z³)` for `(e,transposition,3-cycle)` satisfies
[
w(\mathrm{transposition})^3=w(e)\,w(\mathrm{3cycle})^2.
]
The original weights `(8,2,1)` satisfy that equation. The induced local weight at the first 3×3 block is `K^9`; its three independent class values **violate** the equation, with an exactly **negative** residual. Thus the exact coarse effective action does not belong to the original one-coupling Wilson family. Keeping only the original Wilson coupling destroys the three-scale match. This is a concrete demonstration of why **all induced couplings and correlation visibility** must be controlled in higher-dimensional Yang–Mills constructions.

Four deliberately wrong operations are rejected by the test: 3 instead of 9 microscopic plaquettes per blocked plaquette, retaining the unblocked coupling, corrupting one transfer entry, and treating the coarse step as the fine time unit.

## Results ledger

- Frozen predictions: [PREDICTION-YM4-THREESCALE-S3-20261106.hbp](PREDICTION-YM4-THREESCALE-S3-20261106.hbp), commit `5341070` (first on branch).
- Executable: [test_s3_three_scale_triadic.py](../tests/test_s3_three_scale_triadic.py), added *after* frozen prediction.
- Committed exact result: [MEASURED-YM4-THREESCALE-S3-20261106.hbp](../tests/MEASURED-YM4-THREESCALE-S3-20261106.hbp), SHA256 pinned by the CI.
- Hosted CI: [ym4-s3-three-scale.yml](../.github/workflows/ym4-s3-three-scale.yml) executes the exact code on Ubuntu and checks the receipt and predictions before publishing an artifact.

## Boundary of inference

This calculation is a **real gauge-invariant correlation test in a finite-group 1+1D gauge-transfer model**, but it does **not** evolve the 45,508,080-row S₃ Hamiltonian. Nor does it establish an equivalence between that Hamiltonian and the 4D SU(2) Wilson transfer, a physical Planck lattice, a quantum-vacuum measurement, or Yang–Mills on R⁴. The scale sequence here **coarsens** a finite lattice (`a→3a→9a`), whereas a continuum proof requires a controlled **refinement** `a→0` with the proper coupling trajectory, uniform bounds, and nonvanishing excitation overlap. See [PROBLEM.md](../PROBLEM.md) and [YM4-03](NOTE-YM4-03-ONE-SCALE-BLOCKING.md).

**Research implication:** this validates the operator algebra `coarse ∘ time-jump = time-jump ∘ fine` when the exact induced gauge action is preserved. It also provides a concrete, automatic red control for truncated effective actions. Scaling equality alone cannot distinguish continuous fundamental spacetime from a discrete model; independent predictions about nature would be needed.
