# YM4-VOL05 — a spatial-volume-uniform strong-coupling Wilson spectral-support certificate

**22 November 2026.** A spectral consequence of the previously accepted [original continuous-SU(2) YM4-04B Dobrushin local connected-correlation bound](../NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md), combined with the standard positive Wilson temporal transfer and an independently derived single-link conditional-variance estimate.

**Acceptance class:** rigorous analytic consequence of an explicitly identified published comparison theorem and the standard Wilson transfer construction; the new exact-integer code checks lattice incidence, temporal distance, rational constants and negative controls. Independently formalizing the external comparison and spectral transfer passage is a separate gate. The claim applies to the **local, center-neutral Wilson-visible spectral measure** at **fixed strong coupling**. The first excitation over every physical sector and the weak-coupling 4D continuum mass gap remain **OPEN**.

## 1. Original 4D continuous SU(2) Wilson model

Use the original normalized Wilson Euclidean gauge law on a \(T\times L^3\) periodic 3+1D lattice with \(T\ge3\), \(L\ge2\),
\[
d\mu_{\beta,L,T}=Z^{-1}\exp\!\left(\beta\sum_{p}\tfrac12\operatorname{Tr}(U_p)\right)\prod_e d\mathrm{Haar}(U_e).
\]
Select a **single normalized local spatial plaquette Wilson halftrace**
\(W(t)=\frac12\operatorname{Tr}(U_{\square,t})\in[-1,1]\).

One original spacetime link participates in exactly six plaquettes, each containing three other distinct original links. The influence multiplicity row sum is exactly \(18\), independently of \(L,T\); the integer verifier checks the original \(3^3\times7\) geometry and temporal separation 3. The general all-L/T incidence follows directly by enumerating axes in the cubical lattice.

As derived in YM4-04B using the named Rebeschini–van Handel *Comparison Theorems for Gibbs Measures*, Corollary 2.6, the single-link Dobrushin influence satisfies
\[
C_{ij}\le\tanh(\beta s_{ij})\le\beta s_{ij},\quad
\alpha=\sup_i\sum_{j\ne i}C_{ij}\le18\beta.
\]
For **every** \(0<\beta<1/18\), \(\alpha<1\). With two normalized spatial plaquette observables whose supports are separated by at least \(r\) steps in the link-sharing-plaquette graph,
\[
|\operatorname{Cov}(W_0,W_r)|
\le \frac{4(18\beta)^r}{1-18\beta}.
\]
Spatial Wilson plaquette supports at time 0 and time \(n\) in a temporal ring with \(T\ge2n+1\) have graph distance at least \(n\): each adjacency through an original spacetime plaquette changes the time coordinate by at most one. Therefore
\[
\boxed{|C_{\beta,L,T}(n)|
\le\frac{4(18\beta)^n}{1-18\beta}}
\quad(T\ge2n+1),
\]
with constants **independent of spatial size \(L\)**.

## 2. Uniform positive local Wilson variance

Condition on every original SU(2) link except one of the four links \(e\) belonging to the chosen spatial plaquette. The conditional density of \(U_e\) with respect to normalized Haar is
\[
p_e(U)=\frac{\exp(\beta\sum_{k=1}^6 a_k(U))}
{\int\exp(\beta\sum_{k=1}^6 a_k(V))dV},\quad -1\le a_k\le1.
\]
Thus the numerator is at least \(e^{-6\beta}\), the denominator is at most \(e^{6\beta}\), and \(p_e(U)\ge e^{-12\beta}\) for all SU(2) values.

With the three other links of the chosen plaquette fixed, multiplying a Haar \(U_e\) by the other fixed holonomies preserves Haar. The normalized fundamental Wilson halftrace satisfies exactly
\[
\int W\,dU_e=0,\qquad \int W^2\,dU_e=1/4.
\]
For any real constant \(c\),
\[
\int(W-c)^2 p_e\,dU_e
\ge e^{-12\beta}\int(W-c)^2dU_e
=e^{-12\beta}(1/4+c^2).
\]
Minimizing over \(c\) and applying the law of total variance gives the **full interacting 4D** uniform lower bound
\[
\boxed{
\operatorname{Var}_{\mu_{\beta,L,T}}(W)
\ge\frac{e^{-12\beta}}4\ge\frac{1-12\beta}{4}
}
\]
for \(0<\beta<1/18\). The lower bound is independent of **both spatial volume and temporal length**, and therefore survives the \(T\to\infty\) transfer-vacuum limit.

For the exact rational test coupling \(\beta=1/1000\),
\[
\boxed{\alpha\le9/500,\qquad
\operatorname{Var}(W)\ge247/1000.}
\]

## 3. Positive-transfer spectral representation and spectral support

For finite spatial \(L\), the original continuous-SU2 Wilson temporal kernel has strictly positive Peter–Weyl Fourier eigenvalues \(\kappa_r(\beta)=I_{r+1}(\beta)/I_1(\beta)\). On the full Gauss-invariant physical Hilbert space the transfer is
\[
J=K^{1/2}e^{\beta V_{\mathrm{spatial}}}K^{1/2},
\]
a positive self-adjoint, compact transfer operator with a unique strictly positive top eigenvector \(\Omega_{\beta,L}\) and eigenvalue \(\Lambda_0>0\). The original 4D Wilson cylinder and WG physical transfer certificates supply the original-model setting; the positivity is a standard Wilson Haar construction, not an axiom about a truncated Hamiltonian.

Let \(A=W-\langle\Omega,W\Omega\rangle\) and \(\psi=A\Omega\). The \(T\to\infty\) limit of the original finite-time connected Euclidean Wilson covariance is the nonnegative transfer correlation
\[
C_{\beta,L}(n)
=\langle\psi,(J/\Lambda_0)^n\psi\rangle
=\int_{[0,1)}r^n\,d\sigma_{\beta,L}(r),\qquad n\ge0.
\]
Here \(\sigma\) is a positive Wilson spectral measure on the neutral excited physical spectrum. The strong-coupling Dobrushin bound passes to the limit:
\[
0\le C_{\beta,L}(n)\le\frac{4(18\beta)^n}{1-18\beta}\quad(n\ge1).
\]

**Spectral-support lemma.** If a nonnegative finite measure \(\sigma\) on \([0,1)\) obeys \(\int r^n d\sigma(r)\le M\alpha^n\) for every positive integer \(n\), with \(0<\alpha<1\), then \(\sigma((\alpha,1))=0\). Indeed, any positive mass on \([\alpha+\epsilon,1)\) would force \(\int r^n d\sigma\ge c(\alpha+\epsilon)^n\), contradicting the upper bound as \(n\to\infty\).

It follows for **all** finite spatial sizes \(L\ge2\):
\[
\boxed{\operatorname{supp}\sigma_{\beta,L}\subset[0,18\beta]},
\qquad
\boxed{\sigma_{\beta,L}([0,18\beta])\ge\frac{1-12\beta}{4}.}
\]
In particular, for every positive-overlap *individual* original physical Wilson-visible eigenvector,
\[
\frac{\Lambda_{\mathrm{visible}}}{\Lambda_0}\le18\beta,
\qquad
m_{\mathrm{visible}}
:=-\log\frac{\Lambda_{\mathrm{visible}}}{\Lambda_0}
\ge\log\frac1{18\beta}.
\]

For \(\beta=1/1000\), the **uniform-in-spatial-volume, center-neutral local Wilson channel** acceptance is
\[
\boxed{
\frac{\Lambda_{\mathrm{visible}}}{\Lambda_0}\le\frac9{500},\quad
m_{\mathrm{visible}}\ge\log\frac{500}{9},\quad
\text{total centered Wilson weight}\ge\frac{247}{1000}.
}
\]

The positive-measure spectral support and mass bounds extend to subsequential spatial thermodynamic limits of the corresponding local Wilson spectral measures. Their positive total mass survives because the lower bound is uniform.

## 4. Relation to VOL04 and the next Yang–Mills requirement

VOL04's **complete fourth-order physical plaquette coefficient** has exact uniform matrix norm \(7/48\), while its top *individual momentum-mode* overlap with a local source is \(1/(3L^3)\). VOL05 explains how substantial **total local Wilson spectral mass** can persist while individual mode weights shrink: the uniform lower bound applies to the **entire local Wilson spectral measure**, not a single translation-invariant state.

The new result closes a **strong-coupling Wilson-visible spectral-support and total-weight criterion at all spatial volumes** by combining exact original 4D local bounds with standard transfer positivity. It does **not identify the first excitation across the full physical Hilbert space**, which can be center-charged or Wilson-dark. The finite-beta **complete Schur matrix remainder** of VOL04 remains open; VOL05 provides a complementary route to a Wilson-channel gap without requiring that matrix remainder to be completed first.

The next continuum construction still needs estimates along a **weak-coupling trajectory \(\beta(a)\to\infty\)**, physical lattice-spacing scaling, Osterwalder–Schrader reconstruction and full physical spectral control. The existing Dobrushin sufficient inequality \(\alpha<1\) applies at strong coupling, so its transfer to the scaling regime requires a new renormalized/block cluster estimate.

## 5. Reproducibility and acceptance

- [VOL05 exact integer source](../../tests/ym4_su2_vol05_wilson_spectral_support.py) independently rebuilds a \(T=7,L=3\) 4D link geometry, checks six-plaquette single-link incidence, 18-neighbor multiplicity, temporal distance 3, rational \(\beta=1/1000\) constants and covariance bounds, and rejects \(\beta=1/10\) as a negative control.
- [YM4-04B original accepted note](../NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md) documents the published Dobrushin comparison theorem and its exact SU2 4D application. Its original hosted checker and HBP are unchanged.
- The standard Wilson positive transfer and a positive-measure support lemma provide the spectral deduction. Those analytic steps are stated explicitly here, rather than represented as numerically formalized code.
- **Evidence boundary:** finite-volume original continuous SU2, all spatial sizes, \(0<\beta<1/18\), positive *local-Wilson-visible* spectral support and total weight. Quantitative full physical first-state ordering, weak-coupling continuum and the 4D Yang–Mills continuum mass gap remain OPEN.

The numerical ledger is frozen separately with SHA-256 replay, using exact integer numerator/denominator comparisons and no floating-point arithmetic.
