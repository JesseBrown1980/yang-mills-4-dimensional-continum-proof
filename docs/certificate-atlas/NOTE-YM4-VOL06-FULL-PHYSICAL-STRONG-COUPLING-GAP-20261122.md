# YM4-VOL06 — full physical finite-volume strong-coupling spectral-gap candidate

**2026-11-22. Research acceptance: exact integer geometry and spectral-root controls PASS; analytic application of external Dobrushin comparison and the physical transfer construction pending independent signoff.** This builds on [VOL05](NOTE-YM4-VOL05-WILSON-SPECTRAL-SUPPORT-20261122.md) and [YM4-04B](../NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md). All eleven continuum obligations remain OPEN.

## 1. The proposed extended theorem

For periodic spatial side L>=3, let H_L be the full original continuous-SU(2) Gauss-invariant Hilbert space of spatial links. At fixed 0<beta<1/18, let J_L be the original positive Wilson temporal transfer with simple vacuum eigenvalue Lambda_0. The candidate bound is

\[
\boxed{\sup(\operatorname{spec}(J_L/\Lambda_0)\setminus\{1\})\le 18\beta
\quad\text{for every finite integer }L\ge3.}
\]

The bound covers the entire physical spectrum, including center-charged and Wilson-dark states. In lattice-time energy units it gives \(\Delta_L\ge\log[1/(18\beta)]\), independent of L. At beta=1/1000 the bound is Lambda_1/Lambda_0 <=9/500 and energy separation >=log(500/9).

This is a strong-coupling finite-spacing statement. Establishing a mass gap for the interacting 4D continuum as beta(a)->infinity remains a distinct open mathematical task.

## 2. Generalized Dobrushin covariance step

Consider the original 4D Wilson measure on a periodic T x L^3 lattice, with T>=2n+1. The original linkwise Dobrushin influence matrix obeys \(\alpha=\sup_i\sum_j C_{ij}\le18\beta<1\) because each spacetime link belongs to six plaquettes with three other link occurrences each.

Take any **bounded real gauge-invariant function f of the spatial links on one time slice**, with \(\|f\|_\infty=B\), and let S<=3L^3 be the number of spatial links on which f depends. Its translates f_0 and f_n are separated by at least n steps in the link-sharing-plaquette graph. Applying Rebeschini–van Handel Corollary 2.6 to a bounded exponential tilt by f_n, then differentiating at zero, gives

\[
|\operatorname{Cov}_{\beta,L,T}(f_0,f_n)|
\le \frac14\sum_{i,j}\delta_i f_0\left(\sum_{k\ge0}C^k\right)_{ij}\delta_j f_n
\le \frac{SB^2}{1-18\beta}(18\beta)^n. \tag{2.1}
\]

Here \(\delta_i f\le2B\), \((C^k)_{ij}=0\) for k<n across the two time slices, and row sums obey \(\|C^k\|_\infty\le(18\beta)^k\). The prefactor **may depend on f and L**, while the exponential base does not. A spatial winding Wilson loop is among the permissible gauge-invariant bounded slice functions, even though it is spatially nonlocal.

The named comparison theorem is [Rebeschini–van Handel, Comparison Theorems for Gibbs Measures, Corollary 2.6](https://web.math.princeton.edu/~rvan/dobrushin130819.pdf). The SU(2) conditional-specification and tilt normalization appear in YM4-04B; independent acceptance of that transfer of the published theorem is a separate gate.

## 3. New step: completeness of bounded slice observables

Use the spatially symmetric Wilson transfer

\[
\widetilde J_L=e^{\beta V/2}K_L e^{\beta V/2}.
\]

Its nonzero spectrum agrees with the electric-symmetric convention \(K_L^{1/2}e^{\beta V}K_L^{1/2}\) used in VOL04/VOL05. This choice represents a spatial-link observable at a time slice by ordinary multiplication. The temporal-link-integrated Wilson kernel is continuous and strictly positive pointwise on the compact space of spatial SU(2) link configurations. Standard Wilson character positivity, reflection positivity, and Gauss projection make the transfer self-adjoint, positive and compact. Positivity improvement gives a simple top eigenvalue and a continuous, strictly positive, gauge-invariant vacuum eigenfunction \(\Omega_L(x)\). See [Lüscher (1977)](https://doi.org/10.1007/BF01614090) and [Osterwalder–Seiler (1978)](https://doi.org/10.1016/0003-4916(78)90039-8).

Take any real, normalized physical eigenvector \(\psi\perp\Omega_L\) with eigenvalue \(\lambda>0\). It is continuous because \(\psi=\widetilde J_L\psi/\lambda\). Compactness of configuration space and strict vacuum positivity make

\[
f_\psi=\psi/\Omega_L
\]

a bounded real **gauge-invariant spatial-slice observable**. It is centered in the physical vacuum, and \(f_\psi\Omega_L=\psi\). This is the essential new step: every nonvacuum eigenvector, regardless of its center/Wilson visibility, is tested by (2.1). It is unnecessary to confine the observable family to contractible plaquette halftraces.

For each fixed n and L, the standard finite-temporal-ring transfer trace with multiplication insertions converges as T->infinity to

\[
\lim_{T\to\infty}\operatorname{Cov}_{\beta,L,T}(f_{\psi,0},f_{\psi,n})
=\langle\psi,(\widetilde J_L/\Lambda_0)^n\psi\rangle
=(\lambda/\Lambda_0)^n . \tag{3.1}
\]

## 4. Spectral-root argument

Combining (2.1) and (3.1), for every integer n>=1,

\[
0\le(\lambda/\Lambda_0)^n
\le M_{L,\psi}(18\beta)^n,\qquad
M_{L,\psi}=\frac{3L^3\|f_\psi\|_\infty^2}{1-18\beta}<\infty.
\]

The n-th-root limit implies \(\lambda/\Lambda_0\le18\beta\). Although M may be large and volume dependent, it disappears under n-th roots. The same 18 beta holds for every eigenstate and every finite spatial L. Zero eigenvalues satisfy the bound automatically, and compactness excludes nonzero continuous spectral accumulation. This yields the candidate **full physical finite-volume, spatial-volume-uniform** transfer gap.

The exact integer checker [tests/ym4_su2_vol06_full_spectrum.py](../../tests/ym4_su2_vol06_full_spectrum.py) reconstructs 4D original link/plaquette geometry at (L,T)=(3,7),(4,9), confirms six incident plaquettes and 18 influence occurrences per link, spatial-slice graph distance n through n=3/4, and rejects a hypothetical transfer ratio r=1/50 exceeding alpha=9/500 using integer powers at n=200. The deterministic [HBP](YM4-VOL06-FULL-PHYSICAL-GAP-20261122.hbp) has SHA-256 **6a7d89f4b6e4b98a4528ac56a55ad97e808c798253dbd76ca00982789ae40cb6**. These finite tests check the geometry and rational logic, rather than claiming an executable proof of the full analytic operator theorem.

## 5. Acceptance gates

- **VOL06-A: exact geometry / rational falsifier — PASS locally**, pending hosted verification.
- **VOL06-B: published Dobrushin-to-covariance transfer for arbitrary bounded gauge-invariant slices — ANALYTIC REVIEW REQUIRED**, including total-variation constants.
- **VOL06-C: correct spatial-symmetric Wilson transfer, Gauss restriction, positivity-improving vacuum and time-slice insertions — ANALYTIC REVIEW REQUIRED**.
- **VOL06-D: real eigenfunction continuity and bounded quotient by the vacuum, including the spatial center sectors — ANALYTIC REVIEW REQUIRED**.
- **VOL06-E: weak-coupling scaling beta(a)->infinity, OS reconstruction and true continuum mass gap — OPEN**, with all eleven original atlas continuum gates still OPEN.

**Proposed atlas class: CONDITIONAL.** This is an explicit, reproducible analytic *candidate* for the complete strong-coupling finite-volume physical gap. Its external theorem and operator-theoretic dependencies should be independently signed off before stronger acceptance language is used.
