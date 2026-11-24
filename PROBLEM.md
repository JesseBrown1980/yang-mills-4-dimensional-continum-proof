# Yang–Mills in four dimensions: problem, scope, and proof status

**Updated November 24, 2026: a status block for November 11–22 and corrections to two rows of the November 11 table. The rest of the November 11 text is unchanged. Official continuum existence and mass-gap claim: OPEN.**

This repository contains derived finite-lattice results, exact computational controls and a one-scale blocking construction. None of these alone constructs an interacting continuum four-dimensional quantum Yang–Mills theory or proves a positive *physical* mass gap. Read every claim under the hypotheses in its linked note.

## Status update, November 24, 2026

**Added since November 11.** Every item below is a fixed-lattice result, a strong-coupling result, a conditional implication or a single-scale estimate. None controls the weak-coupling limit β(a) → ∞ uniformly, and all eleven continuum obligations remain OPEN. Prior work for each track is listed in [docs/REFERENCES.md](docs/REFERENCES.md).

| Track | Result | Regime | Status |
|---|---|---|---|
| YM4-07B, YM4-07C, YM4-SW01 (Nov 16–21) | Physical-unit bridge lemma; Wilson-source transfer gate; spectral-window dual | Conditional or finite | Derivations. The 07C S₃ amplitude only fixes a threshold, since no S₃ → SU(2) isometry exists (S₃ is not a subgroup of SU(2)). SW01 lower-bounds spectral weight, so it bounds the gap from above. |
| WT01, WC01, WV01, WG01–WG09 (Nov 21) | Exact one-link character transfer; C0/C2/C4 moments; centre-flux projectors; first-excitation ordering; neutral 42-band | **Spatial L = 2** (2³ torus), mostly **0 < β ≤ 1/100** | Fixed-lattice computations with frozen receipts. On L = 2 the first excitation is a length-2 winding (centre-charged) state, which is a small-torus effect. |
| VOL01–VOL05 (Nov 22) | Selection rules for L ≥ 3; cube Haar integral 1/16; fourth-order Schur coefficient; Wilson spectral support | Strong coupling | Derivations with exact checkers |
| VOL06 | Λ₁/Λ₀ ≤ 18β for β < 1/18, uniformly in spatial volume | Strong coupling | The classical strong-coupling mass gap (Osterwalder–Seiler 1978; Seiler 1982), with an explicit SU(2) constant |
| VOL07 | A uniform covariance decay rate over a physical-size block implies a uniform transfer gap | Conditional | The hypothesis is equivalent to the open uniform clustering rate, (MG) |
| VOL08–VOL11 | Volume-uniform plaquette deficit ≤ R(β) = 1/β + (4/(3β))·log(1536 β^{3/2}); good- and bad-star bounds; conditional independence on plaquette-disjoint links | **Weak coupling, one lattice scale** | Analytic derivations, reconstructed by an AI assistant. The joint bad-island estimate ρ^{\|S\|} and every multiscale step are OPEN. |
| VOL12 (Nov 24) | For every set S of links, μ(S ⊆ bad stars) ≤ ρ⋆^{\|S\|} with ρ⋆ = 6·1536·e^{3/4}β^{3/2}e^{−βε/64}; rooted bad-island tail 72^{m−1}ρ⋆^m | **Weak coupling, one lattice scale; even L ≥ 4** | Written proof by an AI assistant (closed-cube chessboard estimate from Lemma 0004 plus VOL09 and VOL10), with integer checker and frozen prediction. It replaces VOL10's conditional joint input. Awaits human review; odd L and all multiscale steps remain OPEN. [Note](docs/certificate-atlas/NOTE-YM4-VOL12-CHESSBOARD-BAD-STAR-CLUSTERS-20261124.md) |

**Corrections to the November 11 table below.**
- **YM4-04C** is not on `main`. Its note sits on branch `cloud-seat-ym4-04c-freeze-20261109`, and PRs #58–#63 are drafts. Read it as an unmerged draft, not an established result.
- **YM4-05B** samples a deliberately defined surrogate update, not the Wilson measure. It is a computational experiment and is not evidence for any Yang–Mills statement.

**External landscape, as reported.** On 9–10 November 2026, a working group chaired by David Gross assessed OpenAI's Lean-formalized construction as establishing the *existence* half of the problem, with the mass gap not addressed. Hexagon preprint 2611.00492 reduces the gap to a uniform exponential clustering rate, (MG). Neither has been reviewed in this repository. For this repository, the open frontier is therefore the *mass gap*: uniform clustering at weak coupling. Sources are in [docs/REFERENCES.md](docs/REFERENCES.md).

**Review status.** "Independent audit" in notes since November 21 means a separate reconstruction by an AI assistant. No result here has had an external human referee (YM4-08: OPEN).

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
| **YM4-06A (global-lock structure, three spatial dimensions)** | Structure only. Finite S₃ control: 21 flat sectors on the 3-torus, and lock cost κ_3D(L) = min(8, 3·L_min) for every periodic lattice with all sides ≥ 2. Continuous SU(2): explicit exact families with action tending to 0 above the flat set. | [Note](docs/NOTE-YM4-06A-GLOBAL-LOCK-20261110.md); [merged PR #47](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/47). It computes no spectrum and no gap; the physical mass gap, issue #6, is **OPEN**. |
| **YM4-04C (localized polymer norm, frozen prediction)** | **[Correction, Nov 24: unmerged draft, not on `main`; see the status update above.]** A localized polymer norm for the b = 2 blocked SU(2) action, with the induction steps G0 and G1 proved in its note and 42 prediction rows frozen before any engine code. Predicted certificate windows at strong coupling, β near 0.019 to 0.021. | Commit `6ebf632` on the branch `cloud-seat-ym4-04c-freeze-20261109`, held there for review; second seat's G_attack, 7 of 7 checks and 62 of 62 steps reproduced, in [PR #46](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/46). Engine and measurement are next. The weak-coupling trajectory is **OPEN**. |
| **YM4-03C (blocked action through β¹⁰)** | On YM4-03's factor-two map in four dimensions, the blocked effective action of continuous SU(2) at strong coupling in exact rationals through β¹⁰: odd orders vanish through β⁹, χ₁(V_P) enters at β⁸ and the chair, the first non-plaquette term, at β¹⁰. Predictions frozen first, 92 of 92 met. | [Note](docs/NOTE-YM4-03C-BLOCKED-ACTION.md); [merged PR #41](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/41). A strong-coupling expansion on one blocking step; the all-scale flow is YM4-04, **OPEN**. |
| **YM4-01** | Algebraic gauge covariance and exact small-lattice tests. | [Lemma 0001](docs/LEMMA-0001-GAUGE-INVARIANCE.md). Independent final audit remains a separate obligation. |
| **YM4-02a/b** | Finite Haar identities and bounded-degree moment matching for finite SU(2) subgroups. | [Lemmas 0002](docs/LEMMA-0002-HAAR-MOMENTS.md) and [0003](docs/LEMMA-0003-SUBGROUP-DESIGNS.md). Q8, 2T, 2O and 2I agree with continuous Haar only within stated degrees and link-incidence conditions; they are not interchangeable with SU(2) at arbitrary coupling. |
| **YM4-02c** | Finite Wilson measure, specified reflection-positivity results, and a positive transfer operator for Wilson SU(2) at `β > 0`, with a simple largest eigenvalue. | [Lemma 0004](docs/LEMMA-0004-REFLECTION-TRANSFER.md); [merged PR #14](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/14). Reflection-plane, slice and weight hypotheses matter. |
| **YM4-02d** | At each fixed spatial lattice with `N_ℓ` links, the non-leading transfer eigenvalues satisfy `|μ|/λ₀ ≤ tanh(β N_ℓ) < 1` for `β > 0`. Consequently the transfer energy gap in lattice units is at least `−log(tanh(β N_ℓ)) > 0`. | [Quantitative-gap note](docs/NOTE-YM4-02d-QUANTITATIVE-GAP.md); [merged PR #22](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/22). This bound worsens as `N_ℓ` or `β` increases. |
| **YM4-02e** | A k-step spectral bound and, at sufficiently small `β`, a bound independent of lattice size. The stated SU(2), three-spatial-dimensional sufficient range is `tanh β < 1/14`. | [K-step/locality note](docs/NOTE-YM4-02e-KSTEP-AND-LOCALITY.md); [merged PR #26](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/26). This strong-coupling regime does not prove uniformity on a weak-coupling continuum trajectory. |
| **YM4-05B (Cantor 27 nonlinear 4D surrogate and matrix-law fast replay)** | **[Correction, Nov 24: surrogate experiment, not Yang–Mills; see the status update above.]** Sample a deliberately defined noncommuting **gauge-covariant plaquette update** on a (3^4) lattice with Q8-valued SU(2) link inputs at 27 fifth-generation Cantor points. Exact local Wilson 6-staple continuous SU(2) Haar integral is computed by a fast integer Horner kernel. **23 distinct (W,Q) outputs, 14 contradictions** to (Q_{t+1}=f(Q_t)), and independently certified **(U_{172}=U_4)** finite-orbit cycle permit a special-case jump (U_{3^{40}}=U_{81}). Core test measured 404 ms. | [Proof](docs/NOTE-YM4-05B-CANTOR27-20261107.md), [39-row receipt](tests/YM4_05B_CANTOR27-RECEIPT.hbp), [PR #40](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/40). **Not Yang–Mills dynamics**; generic scalar reduction **REFUTED** for this surrogate. General continuous-SU(2) physical reduction, actual weak-coupling RG, first excitation and mass gap **OPEN**. |
| **YM4-05A (weak-coupling controls, 2D vs 4D)** | Exactly test continuous-SU(2) 2D heat-kernel character semigroup through two ternary blocks and increasing inverse diffusion parameter; independently integrate the **4D Wilson one-link six-staple** Haar factor and certify 15 pair terms including 12 mixed-plane chair contours. For genuine Wilson `β=1,4,16,64`, mixed staple log interaction is strictly nonzero, with exact rational Taylor enclosures. | [Prediction-first exact note](docs/NOTE-YM4-05A-CHARACTER-WEAK-COUPLING-20261107.md); [PR #38](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/38). 2D weak heat-kernel blocking **EXACT**; 4D local Wilson integration **MEASURED**; full 4D weak-coupling RG, renormalized induced action, physical mass-gap induction and continuum **OPEN**. |
| **YM4-04B (local SU2 strong-coupling bound)** | On any finite 4D periodic SU(2) torus with sides at least 2, six plaquettes/link and 18 shared-link incidences bound Dobrushin influence by \(18\beta\). With the **named classical comparison theorem** and \(\beta_0=1/1000\), the actual connected spatial Wilson-loop time correlation at fine separation 9 has \(|C|<10^{-14}\), yielding a local absolute comparison to the twice-blocked Wilson-only proxy. A geometric-series proof gives all-\(k\) error sum \(<10^{-4}\) for a family of tori at **fixed strong coupling**. | [Local connected bound note](docs/NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md); [merged PR #37](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/37). **Weak-coupling \(\beta(a)\to\infty\) fails the sufficient Dobrushin contraction condition.** Full induced-action norm, first-state overlap, continuum and mass-gap proof are **OPEN**. |
| **YM4-04A (two ternary blocks)** | **Finite continuous-SU(2) four-dimensional 18⁴→6⁴→2⁴ map** preserves the actual Wilson-loop pullback; exact rational SU(2) controls pass. Conditional on the existing YM4-03 leading b=3 coefficient, a new global Cauchy bound gives a two-step Wilson-only **proxy** log-density error `δ₁=1/536,870,912`, `δ₂<2⁻¹²⁸` at `β₀=1/20,155,392`; finite periodic connected Wilson correlation `|C(9a)|<10⁻⁸`. Distinct infinite-time vacuum correlator `0≤C_Ω(9a)≤(1/1152)⁹` from the fixed-lattice transfer bound. | [Two-block note](docs/NOTE-YM4-04-TWO-TERNARY-BLOCKS-20261107.md), [merged PR #36](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/36). **Relative coupling precision FAIL/HOLD; first-state overlap, weak-coupling all-scale RG, continuum existence and physical mass gap remain OPEN.** |
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

**November 11, 2026.** YM4-04C is the first candidate of that kind in this repository: a normed inductive hypothesis H_k with the steps H_0 ⇒ H_1 (G0) and H_k ⇒ H_{k+1} (G1) proved at b = 2, at strong coupling. Carrying such an induction along a weak-coupling trajectory is the open boundary.

For detailed gate status, see the [proof-obligation ledger](docs/PROOF_OBLIGATIONS.md), the [README](README.md), and the cited notes. Preserve each result at its demonstrated scope.
