# YM4-07B — quantified lattice-to-continuum mass-gap bridge (conditional theorem)

**Date:** November 16, 2026 · **Status:** CONDITIONAL PROOF PLAN, no continuum mass-gap certificate.
**Scope:** genuine continuous \(\mathrm{SU}(2)\) Euclidean 4D Wilson theory along a cutoff-removal sequence. The 3×4 finite \(S_3\) certificates are calibration/provenance controls; no group-independent transfer theorem has been certified.

This note records exact quantifiers and two elementary falsifiers for proposed finite-size/step-scaling shortcuts. It does not infer a mass gap from finite S3 eigenvalues, finite strong-coupling clustering, or an unverified continuum limit. See [PROOF_OBLIGATIONS.md](PROOF_OBLIGATIONS.md), YM4-04/05/06, and [the Clay problem statement](https://www.claymath.org/millennium/yang-mills-the-maths-gap/).

## 1. State the physical gap and the quantifiers

Let \(a_k=a_0 2^{-k}\). Let \(\ell\) count lattice sites on a spatial torus, \(R=\ell a_k\) its *physical* spatial side, and \(\beta_k\) the SU2 bare coupling on a specified renormalization-group trajectory. If \(T_{k,\ell}\) is a positive gauge-invariant transfer operator with simple vacuum top eigenvalue \(\lambda_0(k,\ell)>0\), define the *lattice-unit* gap

\[
 d_{k,\ell}=-\log\!\left(\frac{\lambda_1(k,\ell)}{\lambda_0(k,\ell)}\right).
\]

Define the *physical* gap

\[
 \Delta_{k,\ell}=\frac{d_{k,\ell}}{a_k},\qquad
 \Delta_{k,\infty}=\lim_{\ell\to\infty}\Delta_{k,\ell}
\]

only after existence of that limit has been established (or use a spectral infimum in a defined infinite-volume GNS/transfer representation). In statements with a finite fixed physical side, \(\ell=R/a_k\) must tend to infinity as \(a_k\to0\). Every bound must specify whether it concerns \(d\) or \(\Delta\).

A sufficiently strong **target inequality** is

\[
 \exists \Delta_*>0,\ k_0,\ R_0>0:\quad
 \forall k\ge k_0,\ \forall R\ge R_0
 \ \Delta_{k,R/a_k}\ge \Delta_*.
\]

This target has to be combined with a controlled, **nontrivial** limit of gauge-invariant Schwinger functions (reflection positivity, Euclidean invariance, regularity, clustering, and the other reconstruction requirements). A gap lower bound in a numerical family alone is no substitute for construction of the continuum field algebra.

## 2. Correct finite-volume extrapolation direction

A sufficient certified comparison is

\[
 |\Delta_{k,\ell}-\Delta_{k,\infty}|\le \varepsilon_{k,\ell},
 \qquad \varepsilon_{k,\ell}\ge0,
\]

which implies

\[
 \Delta_{k,\infty}\ge\Delta_{k,\ell}-\varepsilon_{k,\ell}.
\]

The one-sided inequality \(\Delta_{k,\ell}\ge\Delta_{k,\infty}-\varepsilon\) **does not imply** this desired lower bound: it implies \(\Delta_{k,\infty}\le\Delta_{k,\ell}+\varepsilon\). This is a sign/direction falsifier for any proposed finite-volume-to-infinite-volume acceptance gate.

A candidate \(\varepsilon_{k,\ell}=C_k e^{-\mu_k\ell}\) becomes a theorem only when \(C_k\), \(\mu_k\), the spatial geometry, the boundary conditions, and all hypotheses are proved for the **same** Hamiltonian. In a cutoff-removal proof, \(C_k\) and \(\mu_k\) must combine with \(a_k\) so that the bound stays useful in **physical units**. A gap/correlation-length hypothesis must not be used circularly to prove the very gap it assumes.

## 3. Correct the step-scaling induction

If a comparison controls physical gaps directly,

\[
 \Delta_{k+1,\infty}\ge \Delta_{k,\infty}-\eta_k
\]

and \(\eta_k\ge0,\ \sum_{k=k_0}^\infty\eta_k<\Delta_{k_0,\infty}\), then induction yields the explicit uniform bound

\[
 \boxed{\inf_{k\ge k_0}\Delta_{k,\infty}
       \ge \Delta_{k_0,\infty}-\sum_{j=k_0}^\infty\eta_j>0.}
\]

This is a **conditional arithmetic lemma**. The difficult work is finding **actual** \(\eta_k\) valid along \(\beta_k\to\infty\) for continuous SU2, with uniform large-field and Wilson-network remainders.

If a relative step comparison instead gives \(d_{k+1,\infty}\ge\rho_k d_{k,\infty}\), then because \(a_{k+1}=a_k/2\),

\[
 \Delta_{k+1,\infty}\ge (2\rho_k)\Delta_{k,\infty},\qquad
 \inf_k\prod_{j=k_0}^{k-1}(2\rho_j)>0
\]

is needed to retain a positive lower bound by that induction. Merely proving every \(\rho_k>0\), or even \(\rho_k\ge c>0\) for a fixed \(c<1/2\), is insufficient.

**Exact falsifier:** \(d_{k,\infty}=4^{-k}d_{0,\infty}\) satisfies every step ratio \(d_{k+1}/d_k=1/4>0\), while \(\Delta_{k,\infty}=(1/2)^k\Delta_{0,\infty}\to0\).

Finite \(S_3\) coupling parameters \(r\) are not automatically the running \(\beta_k\) of continuous four-dimensional \(\mathrm{SU}(2)\); an explicit operator/measure comparison would be needed.

## 4. What a uniform spectral theorem would imply

**Conditional transfer lemma.** Suppose compatible physical Hilbert-space representations admit self-adjoint nonnegative Hamiltonians \(H_k\), rank-one vacuum projections \(P_k\), and contraction semigroups \(S_k(t)=e^{-tH_k}\). Assume a common identification/embedding and **strong convergence**

\[
 S_k(t)\to S(t),\qquad P_k\to P
 \quad\text{for each fixed }t>0,
\]

with \(P\) the vacuum projection of the reconstructed nontrivial continuum theory. Suppose the **entire** vacuum-orthogonal sector, not only a chosen Wilson observable, has a uniform physical bound

\[
 \|S_k(t)(I-P_k)\|\le e^{-t\Delta_*}
 \quad\text{for every }t>0,\ k\ge k_0,\quad \Delta_*>0.
\]

Then for every \(\psi\), strong convergence gives

\[
 \|S(t)(I-P)\psi\|
 =\lim_k\|S_k(t)(I-P_k)\psi\|
 \le e^{-t\Delta_*}\|\psi\|.
\]

By the spectral theorem the continuum generator has no vacuum-orthogonal spectrum below \(\Delta_*\). This is a genuine **conditional spectral bridge**, with OS reconstruction and strong convergence explicit hypotheses.

**Visible-observable caution:** exponential decay of a particular Wilson-loop connected correlator bounds only its supported spectral measure. A lower unseen state can make the first physical gap arbitrarily small. A full-spectrum transfer inequality (as above), or a proved complete family of observable bounds plus quantitative density/visibility control, is needed.

## 5. Topology, string tension and the finite \(S_3\) control

Positive topological susceptibility alone does not imply a universal positive first Hamiltonian gap. A decoupled gapless/diminishing-gap sector can coexist with a topological observable whose variance remains positive. A proposed positive universal relation must be established as a theorem on the same measure, with constants and assumptions; center-vortex model equalities are not universal mass-gap inequalities.

Similarly a finite-volume string-tension lower bound derived from an area-law observable cannot be converted into a bound on **every** physical excitation without a separately proved spectral relation.

The continuous \(\mathrm{SU}(2)\) Wilson theory in 4D is not a cutoff limit of a fixed \(S_3\) gauge-group model simply because both have finite exact certificate engines. The 3×4 \(S_3\) data are trustworthy tests of arithmetic, provenance, finite spectral/graph algorithms, and counterexample generation. The continuum target needs a separate, quantified SU2 bridge.

## 6. Executable acceptance ledger for the next theorem

1. Specify **one SU2 Wilson RG trajectory** \(\beta_k\), normalized physical time \(a_k\), and compatible finite/infinite-volume transfer operators.
2. Prove explicit finite-volume \(\varepsilon_{k,\ell}\) with **both sides** or the correct lower-bound direction; certify the required physical-unit error and infinite-volume existence.
3. Prove additive summable \(\eta_k\), or a positive infinite product of physical multiplicative step factors, uniformly in volume along \(\beta_k\to\infty\). Track all induced non-Wilson loops/characters, large fields, and polymer tails.
4. Establish nontrivial OS/transfer convergence with compatible vacuum projections, then pass a **full-spectrum** gap inequality through the limit.
5. Only after those exact hypotheses are accepted: state a continuum gap \(\Delta_*>0\). Retain clear \`HOLD\` labels until then.

**Status:** equations in sections 2–4 are correct conditional lemmas and an exact counterexample. The hypotheses required to apply them to 4D continuous SU2 remain **OPEN** in YM4-04/05/06. No Clay mass-gap claim.
