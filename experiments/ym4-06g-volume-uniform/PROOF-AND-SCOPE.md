# YM4-06G — a volume-independent local Wilson bound, with the physical transfer kept separate

**Date: 2026-11-11. Status: prediction-first, exact-integer hosted verification, finite-spatial-lattice geometry with an all-volume analytic theorem.** This note does **not** claim the positive-magnetic-coupling, interacting SU(2) Wilson transfer mass is uniformly positive. It supplies two mathematically distinct, genuinely *volume-independent* controls and an explicit counterexample to substituting one for the other.

The original standalone frozen HBP is docs/PREDICTION-YM4-06G-VOLUME-UNIFORM-LOCAL-20261111.hbp at commit 19c9d0f78532e5b7bef1104fcbbcf89f1dd79940, written before the verifier code. The Rust 1.81 workflow checks that the prediction file has not changed. The 3×4 S₃ r=9 blind lane is not invoked.

## 1. Spatial Wilson geometry for all periodic L >= 2

For spatial (Z/LZ)^3 in three dimensions, there are V=L^3 sites, E=3L^3 positive oriented edges and P=3L^3 positive oriented plaquettes. On **every** periodic L>=2, each plaquette contains four distinct positive link variables, each edge belongs to exactly four plaquettes, and each face containing that edge involves three other distinct edges. Consequently the total directed incidence count of *other links* at any fixed edge is

\[
 \sum_{j\ne i}c_{ij}=4\cdot 3=12,
 \qquad c_{ij}=\#\{\text{spatial faces containing both }i,j\}.
\]

This is **exact independent of L**, not an approximation in which a global count P is replaced by 12 by fiat. Symmetry c_ij=c_ji gives equal row and column totals. The native program reconstructs every face and verifies four distinct edges, four plaquettes per edge, and 12 other-edge incidences per edge at L=2,3,4,5,9,27, including 59,049 edges and 59,049 plaquettes at L=27. It independently checks gauge invariance of all plaquette traces under nonuniform local quaternion gauge transformations and exhibits nonconstant spatial plaquette action.

## 2. Nonzero-coupling, volume-independent LOCAL classical Gibbs/heat-bath gap

On SU(2)^E with **continuous normalized SU(2) Haar** reference measure define the *spatial* Wilson Gibbs probability

\[
 d\mu_{L,\beta_s}(U)=Z^{-1}\prod_{p} e^{-\beta_s(1-\frac12\mathrm{Tr}\,U_p)}
 \prod_{\ell}dU_\ell,\qquad \beta_s=1/128>0.
\]

Given all other links, the conditional law of U_i is a von Mises–Fisher density on the unit quaternion S³:

\[
 \mu_i(dU_i\mid U_{\ne i})=
 \frac{e^{h_i\cdot U_i}}{\int_{SU(2)}e^{h_i\cdot X}\,dX}\,dU_i,\qquad
 h_i=\beta_s\sum_{p\ni i}v_{p,i},\quad\|v_{p,i}\|=1.
\]

If background configurations differ at exactly one other link j, only c_ij unit-vector summands can change; hence ||h_i−h_i'|| <= 2 beta_s c_ij.

**Total-variation influence lemma (explicit):** For p_h(X) proportional to exp(h·X) on the unit sphere S³, the one-parameter interpolation h(t)=h+t(h'−h) obeys, for any measurable 0<=f<=1,

\[
 \left|\frac{d}{dt}\mathbb E_{h(t)}f\right|
 =|\operatorname{Cov}_{h(t)}(f,(h'-h)\cdot X)|
 \le\frac12\|h'-h\|.
\]

Indeed, writing Y=(h'−h)·X, the covariance is bounded by (1/2) E|Y−EY|, and Cauchy–Schwarz with |Y|<=||h'−h|| bounds it by ||h'−h||/2. Integrating t=0..1 proves

\[
 d_{\rm TV}(\mu_i(\cdot|U),\mu_i(\cdot|U'))
 \le\frac12\|h_i-h_i'\|
 \le\beta_s c_{ij}.
\]

Therefore the Dobrushin interdependence sums satisfy, **for every L>=2**,

\[
 \boxed{\alpha\le\sup_i\sum_{j\ne i}\beta_s c_{ij}
   =12\beta_s=\frac3{32}<1.}
\]

This tests a genuine *nonzero* spatial plaquette interaction. The quantity 3/32 has no factor of L³.

**Classical heat-bath spectral-gap theorem, including clocks:** Let K_i be the exact conditional-resampling expectation operator at link i, acting on L²(mu), N=3L³, P=N^-1 sum_i K_i, and \(\mathcal L=\sum_i(K_i-I)=N(P-I)\). Both dynamics are reversible; each K_i is an L² orthogonal projection, and P is self-adjoint positive.

A path coupling in the Hamming metric couples the choice of updated edge, then maximally couples the continuous conditional SU(2) distributions. For states differing at exactly one edge j, updating j removes the disagreement, while updating i ≠j creates an additional disagreement with probability <= beta_s c_ij. Thus

\[
 \mathbb E[d(X_1,Y_1)]
 \le \left(1-\frac{1-\alpha}{N}\right)d(X_0,Y_0).
\]

The inequality extends to general pairs by changing their differing coordinates one at a time and using the triangle inequality for total variation. Therefore the t-step random-scan transition kernel converges uniformly to its stationary distribution in TV at rate at most \(N[1-(1-\alpha)/N]^t\). Reversibility plus the L¹/L∞ bounds and interpolation yields the same asymptotic L² spectral bound, so

\[
 \operatorname{gap}(P)\ge \frac{1-\alpha}{N}
 \ge\frac{29}{32N}.
\]

**For one independent rate-one update clock per link**, the continuous-time generator is N(P−I), whence

\[
 \boxed{\operatorname{gap}(-\mathcal L)\ge\frac{29}{32}
 \quad\text{for all periodic spatial } L\ge2.}
\]

This is the claimed **positive volume-uniform nonzero-interaction classical heat-bath bound**. The spatial Gibbs measure and heat-bath update rule are gauge-equivariant, so restriction to gauge-invariant functions cannot lower its spectral gap.

This is **not** the spectral gap of the 4D physical Wilson transfer T=A^(1/2)B_t P_G A^(1/2), even though both involve the same spatial Wilson plaquette weight. A physical time step is not a single-link Gibbs resampling operation.

The code checks the geometry, rational coefficient, stable update clock normalization and the beta_s=1/8 noncontractive negative control. The analytic covariance and coupling steps are written here for independent verification; the Rust code does not numerically approximate continuum Haar distributions.

## 3. A second, distinct uniform control: exact physical SU(2) transfer when beta_s = 0

At beta_s=0 the temporal Wilson convolution product B_t acts on all SU(2)^E link configurations and commutes with the full vertex gauge projector. At beta_t=1, one-link eigenvalue ratios are \(b_n/b_0\), where n is twice-spin and

\[
 b_n=e^{-1}\sum_{s\ge0}
 \frac{2^{-2s-n}}{s!(s+n+1)!},
 \qquad \rho=b_1/b_0\in
 \left(\frac{24019372}{10^8},\frac{24019373}{10^8}\right).
\]

Only closed spin networks survive all vertex gauge constraints. In the periodic cubic multigraph the shortest nontrivial support has cycle length

\[
 g(L)=\begin{cases}2,&L=2\\3,&L=3\\4,&L\ge4.\end{cases}
\]

The two-edge L=2 winding, three-edge L=3 winding, and four-edge spatial plaquette loops supply explicit physical fundamental trace eigenfunctions. No lower-support singlet exists because a nontrivial open edge carries a representation that cannot be invariant at a degree-one endpoint. By termwise monotonicity of b_n,

\[
 \frac{\lambda_2(B_t|_{\mathcal H_G})}
 {\lambda_1(B_t|_{\mathcal H_G})}
 =\rho^{g(L)}.
\]

The hosted program **independently encloses rho with positive rational Bessel-series tails**, verifies the exact cubic graph girths and these strict integer comparisons:

| Spatial side | First nontrivial physical beta_s=0 ratio |
|---|---|
| L=2 | rho² < 1/17 |
| L=3 | rho³ < 1/70 |
| All L>=4 | rho⁴ < 1/300 |

Thus, for **all L>=2 at beta_s=0**, the *physical gauge-invariant pure-temporal transfer* has

\[
 \boxed{\lambda_2/\lambda_1<1/17,\qquad
 m_{\rm first}(a_t=1)>\log 17.}
\]

This is a legitimate **volume-uniform finite-a quantum-transfer** bound at exactly **zero spatial interaction**, a strong-coupling baseline. It does not establish the same result for beta_s=1/128, where spatial plaquettes couple links.

## 4. Required falsifier: spatial mixing does not prove a temporal mass

Consider a product/uniform spatial measure with Dobrushin alpha=0, yet choose an independent positive reversible temporal operator

\[
 K_n=(1-1/n)I+(1/n)\Pi,\quad n=3^k,\quad a_t=1,
\]

where Pi is projection onto spatial constants. Its first ratio equals 1−1/n, so its normalized mass obeys

\[
 1/n\le -\log(1-1/n)\le1/(n-1)\to0.
\]

Thus even perfect **spatial** Dobrushin control (alpha=0) cannot, without a transfer-specific theorem, establish any positive mass uniformly over a family of **temporal** operators. YM4-06G freezes and checks this counterexample explicitly.

Five fault gates reject a missing face, a wrong incidence count, noncontractive beta_s=1/8, false classical-to-quantum inference, and a tampered HBP without resealing. The output records exact HBI/HBP/SHA/SH/HASH and a checksum manifest; SHA commitments are metadata and do not impose instantaneous physical effects.

## 5. What is still required to answer the user's FULL request

**Achieved:** a spatial-plaquette *nonzero coupling* bound with **no dependence on the total number of plaquettes** (alpha<=3/32, continuous-time classical heat-bath gap>=29/32), plus an exact beta_s=0 *physical Wilson transfer* gap that is uniform in spatial volume.

**Not achieved:** a positive lower first mass for the **interacting beta_s>0 gauge-invariant Wilson transfer** uniform in the number of plaquettes. To bridge this distinction, the next proof must use the temporal convolution plus spatial plaquette interaction together (for example, a controlled polymer/cluster expansion or a local block comparison with a certified error), rather than multiplying an extensive min–max bound or substituting classical Gibbs resampling for physical time evolution. It must then address the running couplings, physical a_t and a_s, and L*a_s->infinity.

Prior finite controls: YM4-06D one-link, YM4-06E side-one interacting, YM4-06F spatial 2×2×2 interacting. The YM4-06G result is a new *uniform-in-L* baseline, not a replacement or an assertion that those finite bounds solve the Clay Yang–Mills existence and mass-gap question.

**Independent proof review requested:** check the SU(2) conditional-field TV lemma, path-coupling-to-L² spectral-gap inference for compact continuous spins, and the spin-network shortest-loop first excitation theorem. Keep this research PR in DRAFT until those are accepted.
