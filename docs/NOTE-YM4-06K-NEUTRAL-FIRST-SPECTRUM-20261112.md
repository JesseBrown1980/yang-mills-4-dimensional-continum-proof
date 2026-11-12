# YM4-06K — actual isotropic continuous SU(2) center-neutral spectral gap and local Wilson correlator bound

**Date:** November 12, 2026. **Scientific claim:** at one explicitly specified *interacting, isotropic, continuous-SU(2) Wilson* point, periodic 3D spatial side \(L=2\) and both spatial/temporal Wilson couplings \(\beta=1/8\), a complete gauge-invariant **center-neutral first spectral gap** and a universal connected spatial Wilson-loop decay rate admit rigorous non-vacuous rational bounds. This goes beyond the total finite-torus first-gap estimate of YM4-06I/J, because the total first excitation is center-charged and therefore invisible to contractible Wilson-loop observables. **This is neither a lattice diagonalization nor a continuum/infinite-volume theorem or Clay solution.**

**Prediction-first gate:** twenty-two prediction rows at \`docs/PREDICTION-YM4-06K-NEUTRAL-FIRST-SPECTRUM-20261112.hbp\` committed as \`37d7253215f81394355a446e73824a4008920ca3\`, strictly before this note and its checker. Independent mathematical review must address the all-irrep physical-sector proof, not only the rational test rows.

## 1. The true complete neutral physical sector of the isotropic transfer

Let \(H_{\rm phys}\subset L^2(SU(2)^{24},dH)\) be the complete 3D spatial link gauge-invariant Hilbert space. The *real* isotropic Wilson transfer from 06F/06I reads
\[
T=A^{1/2}\widehat B A^{1/2},\qquad
A(U)=\exp\!\left[-\beta\sum_{p\in\mathcal P}(1-\tfrac12\operatorname{Tr}U_p)\right],
\quad\beta=\frac18,\quad |\mathcal P|=24.
\tag{K1}
\]
\(\widehat B\) is the normalized full temporal-link Wilson convolution (not a chosen Wilson-loop operator), with strictly positive single-link irrep eigenvalues
\[
t_n=\frac{I_{n+1}(\beta)}{I_1(\beta)},\quad n\ge0,\qquad t_0=1.
\tag{K2}
\]
The *whole* nonzero spectrum of \(T\), including all physical representations, equals that of
\(S=\widehat B^{1/2}A\widehat B^{1/2}\). Since \(e^{-6}\le A\le1\),
\[
e^{-6}\widehat B\preceq S\preceq \widehat B
\quad\text{on the entire }H_{\rm phys}.
\tag{K3}
\]

Both \(T\) and \(S\) commute with the \((\mathbb Z_2)^3\) spatial center one-form operators: multiply all links crossing a noncontractible dual spatial 2-torus by the SU(2) central \(-I\). Every contractible spatial plaquette crosses each such dual plane evenly, so both \(A\) and the central temporal kernel respect this symmetry. The positive Perron vacuum \(\Omega\) is unique and **neutral** (because \(T\) is a strictly positivity-improving continuous positive kernel).

**Important index rule:** the \(\widehat B\)-vacuum is Haar-constant 1, but the *interacting* vacuum of \(S\) or \(T\) need not be Haar-constant. All statements about the first **nonvacuum** neutral eigenvalue below are proved using the min–max **second eigenvalue inside the neutral sector**, not by incorrectly treating \(1^\perp\) as an invariant subspace of interacting \(S\).

## 2. Identify the first *neutral* electric excitation without missing dark states

Spatial side \(L=2\) forms a periodic cubic **multigraph**. The shortest gauge-invariant closed support is a **two-link noncontractible winding line**: two distinct parallel-oriented link variables join the same spatial vertices, giving a 2-cycle. A nonconstant spin-network basis component of \(H_{\rm phys}\) must have nontrivial irrep support with no degree-one vertex; a degree-one invariant with a single nontrivial SU(2) irrep cannot exist. On this bipartite graph there is no 1-cycle or 3-cycle. Any such support therefore contains either one of the twelve two-link winding cycles or at least four distinct links.

At \(\beta=1/8\), exact positive Bessel-series term bounds (YM4-06I) give
\[
\frac{511}{16384}<t_1<\frac1{32},\qquad
0<t_n\le\frac1{1536}\quad(n\ge2).
\tag{K4}
\]
A fundamental \(n=1\) representation on a two-link winding is **center-charged**, so it is excluded from \(H_{\rm neutral}\). A neutral two-link winding uses only **even** \(n\ge2\); its temporal eigenvalue obeys
\[
t_n^2\le\frac1{1536^2}
<\left(\frac{511}{16384}\right)^4
<t_1^4.
\tag{K5}
\]
Every other nontrivial neutral spin-network has at least four occupied links, whose normalized temporal eigenvalues multiply to at most \(t_1^4\). The actual *fundamental four-link plaquette character* is gauge-invariant, center-neutral and a \(\widehat B\) eigenfunction with eigenvalue exactly \(t_1^4\). Therefore this is a complete representation-theoretic result:
\[
\boxed{
\lambda_{0,\mathrm{neutral}}(\widehat B)=1,\qquad
\lambda_{1,\mathrm{neutral}}(\widehat B)=t_1^4,
}
\tag{K6}
\]
where index 1 is the **second** eigenvalue within the neutral sector. It includes dark, winding, higher-irrep and any other physical states. No assertion that the *interacting* first neutral eigenvector is a specific plaquette is needed.

## 3. Certified ratio of the *interacting* center-neutral first two levels

Sectorwise min–max (K3) gives
\[
\boxed{
e^{-6}t_1^4
\le \lambda_{1,\mathrm{neutral}}(T)
\le t_1^4.}
\tag{K7}
\]
The genuine interacting Perron vacuum is neutral and has the exact isotropic SU(2) 06H Haar-moment bound
\[
\frac{163}{160}e^{-3}
\le\lambda_0(T)\le1.
\tag{K8}
\]
Using \(e<11/4\) and (K4), with exact rational integer arithmetic,
\[
\boxed{
\left(\frac4{11}\right)^6\left(\frac{511}{16384}\right)^4
=
\frac{68184176641}{31165630701031653376}
<
\frac{\lambda_{1,\mathrm{neutral}}(T)}{\lambda_0(T)}
<
\frac{6655}{341835776}
<
\frac1{50000}.}
\tag{K9}
\]
Here the upper fraction is \((160/163)(11/4)^3(1/32)^4\). The lower is deliberately conservative and only proves the neutral eigenvalue is genuinely positive. It is not a numerical diagonalization.

Thus the center-neutral first gap per Euclidean fine time tick satisfies
\[
\boxed{\gamma_{\rm neutral}=-\log\!\left(\lambda_{1,\mathrm{neutral}}/\lambda_0\right)>\log50000.}
\tag{K10}
\]
This is *different* from the total physical first gap established by YM4-06I/J, since its first mode is a noncontractible one-form center-charged winding state. It does not require incorrectly calling winding loops "local glueball particles".

## 4. Universal *connected spatial Wilson-loop* correlation decay

Let \(O\) be any bounded gauge-invariant **center-neutral** spatial-link multiplication observable, in particular a real contractible spatial Wilson-loop character. Define the true interacting vacuum expectation \( \langle O\rangle_\Omega=\langle\Omega,O\Omega\rangle\), its connected state \(f=(O-\langle O\rangle_\Omega)\Omega\), and \(\mathsf P=T/\lambda_0(T)\), where \(\|\Omega\|=1\). Then \(f\) is simultaneously neutral and orthogonal to the interacting vacuum. For integer \(t\ge0\), its actual Euclidean connected vacuum correlation is
\[
C_O(t)=\langle f,\mathsf P^t f\rangle.
\tag{K11}
\]
The complete neutral spectral bound (K9), using positivity of \(T\), yields the rigorous **observable-independent temporal decay**
\[
\boxed{
0\le C_O(t)\le C_O(0)\!
\left(\frac{6655}{341835776}\right)^t
<C_O(0)\left(\frac1{50000}\right)^t
\quad\text{for every integer }t\ge1
}
\tag{K12}
\]
whenever \(C_O(0)>0\). For \(C_O(0)=0\), the connected correlator is identically zero. **There is no assumption that \(O\) overlaps with the very first center-neutral excitation.** If that overlap is zero, the true observed correlation decays faster than this bound.

Because all single-link temporal Fourier coefficients are strictly positive, the complete \(B\) operator is injective and strictly positive as a quadratic form (though has eigenvalues tending to zero). Since \(A^{1/2}\) is bounded above/below by positive constants on a finite lattice, \(T\) is also strictly positive as a quadratic form. For a nonconstant real spatial plaquette/Wilson operator \(O\) under the strictly positive continuous Perron vacuum, \(f\neq0\). Therefore
\[
\boxed{C_O(t)>0\quad\text{for every finite }t\ge0}
\tag{K13}
\]
for this **finite** model. This proves a nonzero neutral connected spectral response, not that the coefficient of \(\lambda_{1,\mathrm{neutral}}\) is nonzero.

In mass units with temporal lattice spacing \(a_t\), the rigorous lower rate is \(m_{\rm neutral}>\log(50000)/a_t\) **only for this finite L=2 strong-coupling lattice**. There is no uniform limit as \(a_t\to0\) or \(\beta\to\infty\).

## 5. Scope, verification and holds

The separately frozen checker tests exact L=2 link geometry, two-edge winding center parity, a neutral four-edge plaquette, the full-representation factorial bound including high-spin controls, exact rational bounds (K9), the no-selected-observable spectral inequality, and multiple falsifiers that must individually reject altered assertions. A finite Q8 or S3 model is **not** substituted for SU(2) Fourier or Haar data.

**Unproved and held:** exact interacting center-neutral first eigenvalue and a first-specific local spectral overlap, a gauge-reduced finite SU2 Haar-moment Gram-matrix diagonalization, the \(\beta=2\) strong/intermediate point, weak-coupling scaling, all-scale \(\zeta_k,\rho_k\) of YM4-06E, the 4D continuum and infinite-volume physical mass gap. The old finite floor-freeze Round 5 rehearsals and r=9 launch HOLD are not modified. **PR #67 and #68 remain draft; 06K requires its own hosted checks and independent seat mathematical review before merge.**
