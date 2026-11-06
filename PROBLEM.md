# Yang–Mills in four dimensions: problem, scope, and proof status

**Updated November 6, 2026. Official continuum existence and mass-gap claim: OPEN.**

This repository contains derived finite-lattice results, exact computational controls and a one-scale blocking construction. None of these alone constructs an interacting continuum four-dimensional quantum Yang–Mills theory or proves a positive *physical* mass gap. Read every claim under the hypotheses in its linked note.

## Three distinct targets

| Target | Scope | Status |
|---|---|---|
| **1. Primary — fixed finite lattice** | Continuous SU(2) Wilson gauge theory at fixed lattice spacing, volume and coupling. Prove gauge covariance, finite Wilson measure, reflection and transfer properties, and spectral estimates. | **Substantial fixed-lattice results DERIVED**, with finite tests MEASURED; see below. |
| **2. Finite physical volume, vanishing spacing** | Hold physical side length `L_phys` fixed while `a → 0`; site count `L = L_phys/a → ∞`, with a justified coupling trajectory. | **OPEN.** The estimates do not yet control this family uniformly. |
| **3. Clay problem on `ℝ⁴`** | Construct nontrivial continuum quantum Yang–Mills and establish a strictly positive physical mass gap for each compact simple gauge group. | **OPEN**, including the necessary infinite-volume limit. |

**Scope decision, November 4, 2026:** the operator said, "We're not doing physical volume becoming infinite. We're a finite system." The finite lattice is therefore the project's **primary scope**. That decision does not change the official Clay problem. A fixed finite lattice is also *not* the same as the vanishing-spacing limit at fixed physical volume.

## Official problem

For **every compact simple gauge group** `G`, construct a nontrivial quantum Yang–Mills theory on four-dimensional spacetime satisfying axiomatic quantum-field-theory requirements at least as strong as the Jaffe–Witten formulation, and prove a strictly positive mass gap `Δ > 0` above the vacuum in the physical spectrum.

**First group studied here:** continuous SU(2), pure gauge. An SU(2)-only theorem would cover one group; the official problem quantifies over all compact simple groups.

Sources: [Clay Mathematics Institute](https://www.claymath.org/millennium/yang-mills-the-maths-gap/) and the [Jaffe–Witten problem description](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf).

## Finite Euclidean starting point

For a finite periodic four-dimensional hypercubic lattice `Λ`, assign to each positively oriented link `U_μ(x) ∈ SU(2)`. For `μ < ν`, define

~~~text
U_{μν}(x) = U_μ(x) U_ν(x+μ) U_μ(x+ν)^(-1) U_ν(x)^(-1)
S_W(U; β) = β Σ_{x,μ<ν} [1 - (1/2) Re Tr U_{μν}(x)]
Z_{Λ,β} = ∫ (∏_links dHaar(U_ℓ)) exp(-S_W(U; β)).
~~~

With normalized Haar probability measure and `β ≥ 0`, the integrand is continuous, strictly positive and no larger than one. Thus `0 < Z_{Λ,β} ≤ 1` at fixed finite volume. If `N_p` is the number of plaquette terms, `Z_{Λ,β} ≥ exp(-2β N_p)` also follows from `0 ≤ S_W ≤ 2β N_p`. These are elementary **finite-lattice** bounds, not a continuum construction.

The local gauge action is `U_μ(x) → g(x) U_μ(x) g(x+μ)^{-1}`. Plaquette holonomies transform by conjugation, so their traces are invariant. [Lemma 0001](docs/LEMMA-0001-GAUGE-INVARIANCE.md) records the algebra and exact rational-quaternion tests on a `2×2×2×2` lattice.

## What has been established at finite scale

| Track | Result under its stated hypotheses | Evidence and boundary |
|---|---|---|
| **YM4-01** | Algebraic gauge covariance and exact small-lattice tests. | [Lemma 0001](docs/LEMMA-0001-GAUGE-INVARIANCE.md). Independent final audit remains a separate obligation. |
| **YM4-02a/b** | Finite Haar identities and bounded-degree moment matching for finite SU(2) subgroups. | [Lemmas 0002](docs/LEMMA-0002-HAAR-MOMENTS.md) and [0003](docs/LEMMA-0003-SUBGROUP-DESIGNS.md). Q8, 2T, 2O and 2I agree with continuous Haar only within stated degrees and link-incidence conditions; they are not interchangeable with SU(2) at arbitrary coupling. |
| **YM4-02c** | Finite Wilson measure, specified reflection-positivity results, and a positive transfer operator for Wilson SU(2) at `β > 0`, with a simple largest eigenvalue. | [Lemma 0004](docs/LEMMA-0004-REFLECTION-TRANSFER.md); [merged PR #14](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/14). Reflection-plane, slice and weight hypotheses matter. |
| **YM4-02d** | At each fixed spatial lattice with `N_ℓ` links, the non-leading transfer eigenvalues satisfy `|μ|/λ₀ ≤ tanh(β N_ℓ) < 1` for `β > 0`. Consequently the transfer energy gap in lattice units is at least `−log(tanh(β N_ℓ)) > 0`. | [Quantitative-gap note](docs/NOTE-YM4-02d-QUANTITATIVE-GAP.md); [merged PR #22](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/22). This bound worsens as `N_ℓ` or `β` increases. |
| **YM4-02e** | A k-step spectral bound and, at sufficiently small `β`, a bound independent of lattice size. The stated SU(2), three-spatial-dimensional sufficient range is `tanh β < 1/14`. | [K-step/locality note](docs/NOTE-YM4-02e-KSTEP-AND-LOCALITY.md); [merged PR #26](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/26). This strong-coupling regime does not prove uniformity on a weak-coupling continuum trajectory. |
| **YM4-03** | An exact gauge-equivariant one-scale coarse-link map, continuous-Haar pushforward, and induced-action identities. The note gives an exact two-dimensional blocking flow and leading four-dimensional coefficients, with certified small-block tests. | [One-scale blocking note](docs/NOTE-YM4-03-ONE-SCALE-BLOCKING.md); [merged PR #29](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/29). No controlled all-scale four-dimensional RG flow or continuum gap has been proved; registered missed reads remain recorded. |

A separate [independent GPT-6 one-block PR #28](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/28) is **draft/unmerged** as of this update. Its certified isolated planar tile is not a certified induced action for an entire four-dimensional lattice.

Finite S₃ spectral-gap certificates in a companion repository concern a different finite-group Hamiltonian. QNN, HTTP-0, GitRAM and related model/compute experiments can support candidate generation or verification, but do **not** replace the SU(2) continuum estimates or the physical-gap proof.

## Open proof obligations

These are requirements, **not completed results**.

1. **YM4-04 — All-scale control.** Specify a renormalized coupling trajectory and nonperturbative, scale-uniform bounds with explicit large-field, locality, ultraviolet/infrared and effective-action control. Show a rigorous induction through arbitrarily many blocking steps with summable errors. A successful single block does not imply this. [Issue #4](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/4).
2. **YM4-05 — Continuum existence.** Construct nontrivial gauge-invariant continuum correlations and prove the relevant Osterwalder–Schrader axioms; reconstruct the physical Hilbert space, vacuum, locality and positive-energy dynamics. The official Clay target also requires compatible infinite-volume limits. [Issue #5](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/5).
3. **YM4-06 — Physical mass gap.** Establish `Δ > 0` in the reconstructed physical spectrum, with sufficiently uniform estimates as `a → 0` (and the necessary volume limit for the Clay target). A finite lattice gap `m_latt = −log(λ₁/λ₀)` cannot be called a physical continuum gap without controlling `m_latt/a` and identifying the relevant physical states. [Issue #6](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/6).
4. **YM4-07 — All compact simple groups.** Extend from continuous SU(2) or retain the SU(2)-only label.
5. **YM4-08 — Independent mathematical audit.** Pin hypotheses, proofs, receipts and exclusions. Retain failures, inconclusive checks and corrected predictions in the evidence record.

For the project's target **2**, an appropriate subset of the continuum, uniform-estimate and physical-gap obligations remains OPEN even if the infinite-volume limit is intentionally outside scope. A theorem at fixed finite physical volume would not automatically prove the full Clay statement.

## Next mathematical boundary

The critical step is to go **from one exact four-dimensional blocking map to explicit summable bounds valid across an unbounded sequence of scales**, especially as the Wilson coupling follows a weak-coupling continuum trajectory. A candidate proof must state a precise normed inductive hypothesis and prove it is preserved with controlled errors. It cannot infer the continuum or physical gap from fixed-spacing positivity, a finite sequence of runs, or one blocked lattice.

For detailed gate status, see the [proof-obligation ledger](docs/PROOF_OBLIGATIONS.md), the [README](README.md), and the cited notes. Preserve each result at its demonstrated scope.
