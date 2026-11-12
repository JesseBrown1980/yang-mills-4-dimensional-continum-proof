# YM4-06I/J — actual isotropic SU(2) L=2 first physical gap AND center-charge selection

**Date:** November 11, 2026. **Status:** DERIVED analytic complete-physical-spectrum bounds for one **genuine isotropic continuous-SU(2) four-dimensional finite Wilson transfer**, with independently checked exact rational controls; **not** a diagonalized finite Wilson Gram matrix and **not** a continuum or Clay solution. This is a deliberately limited strong-coupling benchmark at spatial side L=2 and beta_s=beta_t=1/8. No first-gap claim is extended to beta=2, to infinite spatial volumes, or to lattice refinement.

**Predictions frozen before any new code:** 06I sixteen rows at commit cea436e6b399293493f308cf41c8f5bd1dac5677; new 06J center-charge predictions ten rows at 39504e4a9ca334d1e0184de8ea459de6a9a5b1e6. This branch is **stacked on draft PR #67**, and #67's original F/G/H predictions and the independent Opus reading remain unchanged.

## 1. Global spectral sandwich for the **actual isotropic Wilson transfer**

On the gauge-invariant spatial slice Hilbert space of the finite 3D periodic L=2 lattice, let M=N_s=3L^3=24. Take the continuous SU(2) isotropic Wilson weight
\[
A_\beta(U)=\prod_{p\ \mathrm{spatial}}
\exp[-\beta(1-\tfrac12\operatorname{ReTr}U_p)],
\qquad \beta=\tfrac18>0.
\]
The temporal kernel is the **actual** normalized product of 24 SU(2) central Wilson convolutions, \(\widehat B_\beta\), with complete Peter–Weyl link eigenvalues \(t_n=I_{n+1}(\beta)/I_1(\beta)>0\), \(t_0=1\). Its unique top vacuum is the constant Haar state.

Let
\[
\widehat T_\beta=A_\beta^{1/2}\widehat B_\beta A_\beta^{1/2},
\qquad
S_\beta=\widehat B_\beta^{1/2}A_\beta\widehat B_\beta^{1/2}.
\tag{I1}
\]
These are positive compact operators on the **entire** gauge-invariant physical slice. Put \(X=A^{1/2}\widehat B^{1/2}\). Then \(\widehat T=XX^*\) and \(S=X^*X\), so their **nonzero eigenvalues with multiplicities coincide**. Because each plaquette factor lies between \(e^{-2\beta}\) and 1,
\[
e^{-2\beta N_s}\widehat B
\preceq S \preceq \widehat B.
\tag{I2}
\]
Min–max therefore yields **for every physical eigenvalue index** \(j\) including dark or winding states
\[
\boxed{e^{-2\beta N_s}\lambda_j(\widehat B)
\le\lambda_j(\widehat T)
\le\lambda_j(\widehat B).}
\tag{I3}
\]
This is a **full-sector** comparison, not the Ritz spectrum of a selected Wilson-loop observable and not a truncated model. It proves a useful first-gap result if the true pure-electric first physical mode is identified and the top eigenvalue has an independent lower bound.

## 2. Correctly identify the first electric physical mode: a two-link winding loop

At L=2, periodic links along any axis give **two distinct links connecting the same pair of sites**, so the underlying spatial multigraph has a genuine winding two-edge cycle. A fundamental Wilson line around such a closed axis cycle (a Polyakov loop) is a gauge-invariant nonconstant eigenfunction of \(\widehat B\) with eigenvalue \(t_1^2\). This is **not** a four-link plaquette. The spatial multigraph has no self-loop and is bipartite, hence no nonzero gauge-invariant spin-network support can consist of one link or three links. A nonconstant gauge-invariant link representation network must have no degree-one vertex, hence its occupied edges include a cycle. Every other minimal support has four or more links, except possible two-link higher-irrep windings.

At \(\beta=1/8\), a completely elementary positive Bessel-series bound gives
\[
\frac{511}{16384}< t_1
=\frac{I_2(1/8)}{I_1(1/8)}
<\frac1{32}.
\tag{I4}
\]
The lower bound follows from \(I_2\ge(\beta/2)^2/2!\) and the geometric estimate \(I_1\le(\beta/2)/(1-\beta^2/8)\); upper bound follows from termwise factorial comparison. Likewise, **for all** \(n\ge2\),
\[
0<t_n\le\frac{(\beta/2)^n}{(n+1)!}
\le\frac1{1536}<t_1.
\tag{I5}
\]
Every occupied link contributes a temporal eigenvalue no greater than \(t_1\); each two-link gauge-invariant winding must have equal representations. Consequently
\[
\boxed{\lambda_0(\widehat B)=1,\qquad
\lambda_1(\widehat B)=t_1^2.}
\tag{I6}
\]
This statement already includes **all** physical lattice gauge sectors and every possible link irrep. Its multiplicity need not be computed to establish the eigenvalue enclosure.

## 3. True first excited ratio at nonzero isotropic spatial coupling

From (I3), since \(2\beta N_s=6\),
\[
e^{-6}\le\lambda_0(\widehat T)\le1,
\quad
e^{-6}t_1^2\le\lambda_1(\widehat T)\le t_1^2.
\tag{I7}
\]

But the actual isotropic spatial Haar moment bound 06H, **not an assumption about the vacuum**, strengthens the top eigenvalue:
\[
\lambda_0(\widehat T)\ge
e^{-\beta N_s}\left(1+\frac{\beta^2N_s}{4(2+\beta N_s)}\right)
=\frac{163}{160}e^{-3}.
\tag{I8}
\]

Using the certified rational inequality \(e<11/4\), and (I4), all without floating-point arithmetic, the **true full first excited ratio** obeys
\[
\begin{split}
r_{\rm phys}:=\frac{\lambda_1(\widehat T)}{\lambda_0(\widehat T)}
&<\frac{160}{163}\left(\frac{11}{4}\right)^3
\left(\frac1{32}\right)^2\\
&=\boxed{\frac{6655}{333824}<\frac1{50}}.
\end{split}
\tag{I9}
\]
The lower ratio bound similarly follows from \(\lambda_0\le1\), \(\lambda_1\ge e^{-6}t_1^2\), \(e^{-6}>(4/11)^6\) and \(t_1>511/16384\):
\[
\boxed{
\frac{261121}{116101021696}<r_{\rm phys}<\frac1{50}.
}
\tag{I10}
\]
Thus, in units of one fine Euclidean transfer tick,
\[
\boxed{\gamma=-\log r_{\rm phys}>\log50.}
\tag{I11}
\]
These are **certified bounds**, not numerical diagonalization or a novel continuum gap. The upper ratio is conservative, but by construction no hidden physical state is excluded.

## 4. Center one-form charge reveals *which* physical excitation is first

The spatial Wilson plaquette factor and temporal kernel are invariant under the \((\mathbb Z_2)^3\) **spatial center one-form symmetry**: multiply every oriented link crossing a chosen noncontractible dual spatial 2-torus by the central element \(-I\). Every spatial plaquette contains an even number of such crossing links; the temporal transition kernel is invariant under simultaneous central flips of its two time-slice arguments. Thus \(\widehat T\) and \(\widehat B\) preserve charge sectors. The unique positive vacuum is center neutral.

A two-link **fundamental** winding loop crosses the corresponding plane once, so it is **center charged** and exactly orthogonal to the vacuum. A contractible Wilson-loop observable is center neutral and has **zero overlap** with any charged eigenstate.

For the neutral non-vacuum sector, the smallest possible supports are:
- a two-link winding of **even** representation index \(n\ge2\), with pure-electric ratio \(t_n^2\); or
- at least four nontrivial links, giving pure-electric ratio at most \(t_1^4\).

At \(\beta=1/8\), exact inequalities give
\[
t_n^2\le(1/1536)^2<(511/16384)^4<t_1^4.
\tag{J1}
\]
Hence the complete neutral **vacuum-orthogonal** pure-electric transfer spectrum is bounded above by \(t_1^4\). The same \(S=\widehat B^{1/2}A\widehat B^{1/2}\) order comparison applies **inside each center sector** and, within the neutral sector, to the subspace orthogonal to its Perron vacuum. There is a subtlety: \(S\)'s vacuum vector is not the Haar constant when \(A\ne1\), so the bound on the neutral *second* eigenvalue uses min–max **index 2 in the neutral sector** rather than simply restricting \(S\) to the Haar-constant orthogonal complement. The bound is nevertheless \(\lambda_{\rm neutral,2}(\widehat T)\le t_1^4\).

In a charged winding sector, min–max (I3) gives a genuine eigenvalue at least \(e^{-6}t_1^2\). Because
\[
e^{-6}>(4/11)^6>(1/32)^2\ge t_1^2,
\]
we have
\[
\boxed{
\lambda_{\rm charged,top}(\widehat T)
\ge e^{-6}t_1^2
>t_1^4
\ge\lambda_{\rm neutral,second}(\widehat T).
}
\tag{J2}
\]
The same argument bounds other nontrivial charged sectors; the **true first excited eigenstate of this finite interacting isotropic Wilson system is in a nontrivial spatial center-flux sector**. We have not determined its degeneracy or which charged direction wins.

**Physical interpretation boundary:** a local, contractible glueball-type Wilson operator is center neutral and has zero overlap with this lowest finite-volume charged excitation. Therefore the **finite-volume first physical spectral gap** and the **first center-neutral/local-observable decay exponent** are distinct observables. This result is another reason not to equate an arbitrary finite torus first gap or one Wilson-loop correlator with the 4D continuum Yang–Mills mass-gap theorem.

## 5. Independent Fourier tail: extremely small at this controlled coupling

At the **same actual isotropic Wilson coupling** \(\beta=1/8\), 06F's all-irrep temporal cutoff N=3 has
\[
\delta_3=\frac{(\beta/2)^4}{5!}
=\frac1{7864320}.
\tag{I12}
\]
The rank per link is \(\sum_{n=0}^3(n+1)^2=30\); before gauge projection the full 24-link rank is \(30^{24}\), still computationally impractical. But the 06H lower bound (I8) yields the independent rigorous relative enclosure
\[
\frac{\delta_3}{\lambda_0(\widehat T_N)}
<
\frac{1331}{512753664}
<\frac1{380000}.
\tag{I13}
\]
This is a **truncation-error** result, not an actual \(N=3\) isotropic Gram diagonalization. The direct untruncated full-spectrum bound (I9) is independently nonvacuous and does not require diagonalizing the enormous retained space.

## 6. Exact verification, open work, and limits

The new checker \`tests/test_ym4_06i_isotropic_first_ratio.py\` independently verifies the side-2 multigraph and all noncontractible two-link winding paths, finite SU(2) fundamental endpoint gauge covariance via a separate Q8 **algebra-only** test, the rational Bessel-series enclosures, the strong-coupling *true* first-ratio bounds and complete sector comparison, the exact N=3 Fourier budget, and seven named false controls. It neither uses Q8 for the actual SU(2) spectral values nor substitutes a two-level selected-state diagonalization.

**Unsolved:** the actual isotropic transfer's sharper top and first spectral values at \(\beta=2\) or large bare \(\beta\), a scalable gauge-invariant Gram-matrix eigenvalue certification, the full \(\rho_k,\zeta_k\) all-scale transfer-block estimates of PR #66, the physical continuum-limit mass gap, and nontrivial OS reconstruction. This benchmark uses finite \(L=2\), fixed \(\beta=1/8\); its lower bound on \(\gamma\) is not uniform as \(\beta\) runs toward weak coupling or as the lattice is refined.

**Merge/review:** file in a **new stacked draft PR based on PR #67's branch**, keeping 06F/G/H reviewer scope intact. Dedicated hosted integer/no-float checks and an independent seat review are required; do not merge or change the finite floor-freeze/r=9 HOLD.
