# YM4-06I — SU(2) conditional covariance improves the volume-uniform 4D Wilson transfer window

**2026-11-11. Status: mathematical proof proposal with exact native Rust coefficients and 4D geometry.** Predicted *before* verifier implementation in \`docs/PREDICTION-YM4-06I-SHARP-VMF-20261111.hbp\`, commit \`7f4da6d135978453d7eeddfd2a8396c183814387\`. This work extends YM4-06H's fixed-spacing/strong-coupling criterion, **not** the continuum mass-gap theorem. Full reflection-positive transfer inference still uses published covariance and OS results; independent proof review is necessary.

## 1. A factor-two improvement valid at every SU(2) external field

Under the usual real unit-quaternion identification SU(2)=S³, the exact conditional distribution for one Wilson link has density relative to normalized Haar measure

\[
 p_h(X)=Z(h)^{-1}\exp(h\cdot X),\qquad X\in S^3,\quad h\in\mathbb R^4.
\]

Set r=||h||. Its normalized partition function is Z(r)=2I₁(r)/r, where Iₙ is the modified Bessel function. Let

\[
 A(r)=\frac{d}{dr}\log Z(r)=\frac{I_2(r)}{I_1(r)}.
\]

The mean is E_h X=A(r)h/r and the Hessian of logZ is the **full covariance matrix** of X. Its eigenvalues are
\[
 \operatorname{Var}_h(X_\parallel)=A'(r),\qquad
 \operatorname{Var}_h(X_\perp)=A(r)/r
\]
(the latter with multiplicity three). At r=0 all four covariance eigenvalues are 1/4.

**Tangential bound.** Compare the positive series for I₂(r) and (r/4)I₁(r) coefficient by coefficient. For every s>=0 the coefficient ratio equals 2/(s+2)<=1. Consequently

\[
 0<A(r)/r\le1/4\quad(r>0).
\]

**Radial bound, independently of numerical sampling.** The Bessel recurrence gives
\[
 A'(r)=1-A(r)^2-\frac{3A(r)}r,\qquad
 A(r)=r/4-r^3/96+O(r^5)\quad(r\to0).
\]
In particular A'(r)<1/4 sufficiently close to zero. At any hypothetical upward crossing A'(r)=1/4, differentiating the Riccati equation yields
\[
 A''(r)=\frac{A(r)(12-2r^2)-3r}{4r^2}<0.
\]
For r²<=6 use A(r)<=r/4, making the numerator at most -r³/2<0. For r²>6 the coefficient of A is negative and so is -3r. An upward crossing is impossible; hence A'(r)<=1/4 for all r>=0. This gives the global covariance matrix estimate
\[
 \boxed{\operatorname{Cov}_h(X)\preceq\frac14I_4,\quad \text{for every }h\in\mathbb R^4.}
\]

This argument is closely related to classical concavity results for Bessel-function ratios (Watson; see also Yang, 2022, *Convexity of ratios of the modified Bessel functions of the first kind with applications*). It is an explicit constant proved here for this conditional SU(2) family, not a claim that the underlying Bessel mathematics is new.

**Total-variation sensitivity.** For any bounded measurable 0<=f<=1, along h(t)=h+t(h'-h), we have
\[
 \left|\frac d{dt}E_{h(t)}f\right|
 =|\operatorname{Cov}_{h(t)}(f,(h'-h)\cdot X)|
 \le\frac12 E_{h(t)}|Y-EY|
 \le\frac12\sqrt{\operatorname{Var}_{h(t)}Y}
 \le\frac14\|h'-h\|
\]
with Y=(h'-h)·X. Integrating t from 0 to 1,
\[
 \boxed{\|\mu_h-\mu_{h'}\|_{\rm TV}\le\|h-h'\|/4.}
\]

A neighboring Wilson link j changed while link i is updated changes the conditional field by at most 2\sum_{p\ni i,j}\beta_p. It follows that

\[
 \boxed{c_{ij}\le \frac12\sum_{p\ni i,j}\beta_p.}
\]

This **halves the prior Dobrushin budget** from YM4-06H while keeping the same 4D Wilson model, physical time definition, and full SU(2) gauge group.

## 2. A stronger all-volume interacting 4D criterion

For periodic spatial cubic L>=2, every spatial edge lies in four spatial and two temporal Wilson faces; a temporal edge lies in six temporal faces. Every face has three other links. Hence the exact nonextensive influence estimate for ALL spatial L and temporal Nt is now

\[
 \boxed{\alpha\le \max(6\beta_s+3\beta_t,\ 9\beta_t).}
\]

At the new frozen, **both-couplings-positive** test point

\[
 \beta_s=1/128,\qquad \beta_t=1/10,
\]

we have
\[
 \alpha_{\rm spatial}\le111/320,\qquad
 \alpha_{\rm temporal}\le9/10,\qquad
 \boxed{\alpha\le9/10<1.}
\]

The bound depends only on local link–plaquette incidence; it does **not** contain L³ or the number of plaquettes. It improves the sufficient strong-coupling window from \(\beta_t<1/18\) to \(\beta_t<1/9\), assuming \(6\beta_s+3\beta_t<1\) too. For beta_s=1/128 the temporal inequality is the limiting one throughout this tested window.

The frozen exact-rational cross-checks also require:

| Couplings beta_s, beta_t | Spatial influence | Temporal influence | Alpha | Status |
|---|---|---|---|---|
| 1/128, 1/10 | 111/320 | 9/10 | 9/10 | PASS |
| 1/128, 1/16 | 15/64 | 9/16 | 9/16 | PASS |
| 1/128, 1/32 | 9/64 | 9/32 | 9/32 | PASS |
| 1/128, 1/9 | — | 1 | 1 | FAIL (not strictly contractive) |
| 1/128, 1/8 | — | 9/8 | 9/8 | FAIL |
| 1/128, 1 | — | 9 | 9 | FAIL |

At beta_t=1/10, a direct Dobrushin–Föllmer covariance expansion and **one-frame link influence graph locality** imply fixed-L connected Euclidean time correlations of bounded gauge-invariant spatial-slice observables decay as O((9/10)^t). The prefactor can depend on L, but not t; this is sufficient for a **spectral rate** bound. If the published Wilson/Osterwalder–Seiler reflection-positivity and transfer positivity hypotheses apply with the same normalization, the positive spectral measure of time-correlators implies, for each finite spatial L, the *entire first gauge-invariant transfer gap* satisfies

\[
 \boxed{\lambda_2(T)/\lambda_1(T)\le9/10,\quad
 m_{\rm first}\ge\log(10/9)/a_t.}
\]

The numerical verifier checks the exact local incidence, coefficient, frozen half-factor, time-anchor bound, specific finite geometry examples up to L=27, and explicit Dobrushin series factors. It **does not independently machine-prove** the cited general infinite-dimensional covariance theorem or Wilson transfer spectral representation. Those remain analytical ingredients and specific review targets. Nothing in this result calibrates the physical lattice spacing a_t.

## 3. Software, falsifiers, and independence

Native Rust1.81 with strict Clippy and no floats, unsafe, Node, V8, or JSON. The same full 4D geometry/gauge-covariance checker from YM4-06H verifies periodic (L,Nt)=(2,3),(3,3),(3,6),(5,3),(9,3),(27,2), including **236,196 plaquettes** in the L27,Nt2 test. The additional sharp-vMF checks encode the coefficient-wise positive Bessel comparison and analytic Riccati crossing sign, and regression-test exactly reduced anisotropic coupling fractions.

Intentionally rejected faults include removed 4D plaquette, wrong spatial/temporal link type, false time locality, \(\beta_t=1/9\) at the strict boundary, \(\beta_t=1/8\) beyond the threshold, illicit use at \(\beta_t=1\), a false 1/8 uniform directional variance claim, reversion to the prior per-face TV coefficient, and HBP tampering. All HBI/HBP/SHA/SH/HASH receipt files are hash-checked and replayed from source. SHA and SH remain separate from the physical transfer operator; changing a global cryptographic root cannot by itself propagate a quantum disturbance.

## 4. Remaining limits and immediate mathematical review

This is **an improved strong-coupling volume-uniform result**, not proof at \(\beta_t=1\) and not at the weak-coupling scaling regime. The continuum \(a_s,a_t\to0\), volume-to-infinity and running SU(2) coupling trajectory remain OPEN. Neither a better Dobrushin constant nor ternary representation resolution alone removes those obstructions.

Independent reviewers should verify (i) the Bessel ratio/Hessian proof at all r including r=0 and the TV factor 1/4, (ii) the SU(2) Wilson plaquette normalization h and its co-face field difference, (iii) the row/column influence matrix and Föllmer theorem assumptions, (iv) temporal infinite-cylinder limit and reflection-positive transfer spectral correspondence, and (v) whether a lower bound on the physical mass survives some continuation of beta_t **beyond 1/9** using a method not dependent on this single-link Dobrushin criterion.

This branch is kept as a DRAFT for independent review; do not merge based solely on green computational CI.
