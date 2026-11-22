# YM4-VOL06 independent analytic audit — finite-volume all-sector strong-coupling transfer bound

**Date 2026-11-22. Reviewer method:** fresh, direct reconstruction from the named published Dobrushin comparison theorem and the original positive Wilson transfer operator; independent of the numerical output of the VOL06 integer checker. **Verdict: mathematical derivation PASS, conditional on standard published comparison and physical transfer theorems; external peer review and continuum extension OPEN.**

This audit reviews [VOL06's theorem note](../docs/certificate-atlas/NOTE-YM4-VOL06-FULL-PHYSICAL-STRONG-COUPLING-GAP-20261122.md) and records the exact chain of assumptions rather than treating hosted tests as analytic proof. Its full-strength conclusion concerns the **original compact, continuous SU(2) Wilson lattice transfer at finite spatial L and fixed bare strong coupling**. It is consistent with standard strong-coupling lattice-gap theory: see Osterwalder–Seiler, *Ann. Phys.* 110 (1978) 440–471, [original article](https://doi.org/10.1016/0003-4916(78)90039-8), and Lüscher, *Commun. Math. Phys.* 54 (1977) 283–292, [original article](https://doi.org/10.1007/BF01614090). These historical results are prior work. Recent explicitly quantified strong-coupling treatments, such as [preprint 2610.00341v6](https://hexagonmath.org/pdf/2610.00341v6), provide a separate comparison lead and require scope/normalization checks before importing numerical bounds.

## A. Exact model and quantitative comparison

Use \(G=SU(2)\), periodic 4D lattice \(T\times L^3\) with \(L\ge3,T\ge3\), original normalized product Haar links, and action factor
\[
 \exp\left(\beta\sum_{p}W_p\right),\qquad W_p=\tfrac12\operatorname{Tr}(U_p)\in[-1,1].
\]
Every original spacetime link belongs to 6 oriented plaquettes; each such plaquette contains 3 other original link occurrences. Let \(s_{ij}\) count common plaquettes with multiplicity. Thus \(\sum_{j\ne i}s_{ij}=18\).

Fix boundary links except \(i\), and change only \(j\). The difference of the *unnormalized* conditional log potentials as a function of \(U_i\) has oscillation at most \(4\beta s_{ij}\). The bounded-log-tilt inequality between two probability densities gives
\[
C_{ij}=\sup_{\omega,\omega':\omega_{-j}=\omega'_{-j}}
\|\gamma_i(\cdot|\omega)-\gamma_i(\cdot|\omega')\|_{\mathrm{TV}}
\le\tanh(\beta s_{ij})\le\beta s_{ij}.
\]
Here total variation is \(\tfrac12\int|p-q|\), and no factor of 2 can be suppressed by changing conventions. Consequently \(\alpha=\sup_i\sum_j C_{ij}\le18\beta<1\). This verifies the finite-volume hypotheses in Rebeschini–van Handel, [*Comparison Theorems for Gibbs Measures*, Corollary 2.6, printed pp. 8–9](https://web.math.princeton.edu/~rvan/dobrushin130819.pdf): compact Polish link sites, continuous local specifications, discrete metric \(\eta=1_{x\ne y}\), and \(D=\sum_{k\ge0}C^k\) convergent under \(\|C\|_\infty<1\).

## B. Tilt gives a covariance bound with the correct factor

For bounded real spatial-slice functions \(F,G\), define \(d\widetilde\mu_t=e^{tG}d\mu/\langle e^{tG}\rangle_\mu\). The conditional-specification difference at link \(j\) is a log tilt with oscillation \(\le |t|\delta_jG\), so its TV distance is bounded by \(\tanh(|t|\delta_jG/4)\le |t|\delta_jG/4\).

Apply Corollary 2.6 to \(\mu,\widetilde\mu_t\), divide by \(|t|\), and use differentiation at \(t=0\):
\[
 |\operatorname{Cov}_{\mu}(F,G)|
 \le \frac14\sum_{i,j}\delta_iF\,D_{ij}\,\delta_jG.
 \tag{B.1}
\]
The \(\frac14\) follows from the log-tilt TV bound, and \(\delta_jG\) is the *full single-link oscillation* (not half the oscillation).

Let \(F=f(U_{\mathrm{spatial},0})\), \(G=f(U_{\mathrm{spatial},n})\), \(|f|\le B\), and \(S\le3L^3\) the number of spatial links in its support. For \(T\ge2n+1\), any path in the original plaquette-sharing-link graph connecting the two supports has length at least \(n\). Thus \((C^k)_{ij}=0\) for \(k<n\), while \(\sum_j(C^k)_{ij}\le\alpha^k\). Since \(\delta_iF,\delta_jG\le2B\),
\[
 |\operatorname{Cov}_{\beta,L,T}(f_0,f_n)|
 \le SB^2\frac{\alpha^n}{1-\alpha}
 \le\frac{3L^3B^2}{1-18\beta}(18\beta)^n.
 \tag{B.2}
\]
**Scope:** the prefactor is allowed to depend on \(L,\beta,f\); the exponential base is the same \(18\beta\) for all volumes and all bounded gauge-invariant slice observables.

## C. Positive transfer and the exact slice measure

Use the symmetric split
\[
 \widetilde J_L=M_{e^{\beta V/2}}K_LM_{e^{\beta V/2}}
\]
on the original Gauss-invariant spatial-link \(L^2\) space, where \(K_L\) is the temporal Wilson Haar-convolution with gauge projection. Its Peter–Weyl scalar coefficients are strictly positive for \(\beta>0\), and its integral kernel is a continuous positive function of the spatial link pairs (equivalently, integrate a product of strictly positive temporal one-link densities over all temporal gauge links). For finite \(L\), the operator is compact and self-adjoint positive; its kernel is positivity improving on the gauge-invariant space.

The Perron/Krein–Rutman argument therefore yields a simple maximal eigenvalue \(\Lambda_0>0\) and a continuous, strictly positive normalized vacuum \(\Omega_L\). The finite cylinder with \(T\) periodic time slices is represented by \(\operatorname{tr}(\widetilde J_L^T)\), with gauge-invariant spatial-slice multiplication insertions. Trace class follows from the summable SU(2) character coefficients for fixed finite \(L,\beta>0\), and the temporal connected covariance has the \(T\to\infty\) limit
\[
 C_{f,L}(n)=
 \langle (f-\langle f\rangle_{\Omega})\Omega_L,
       (\widetilde J_L/\Lambda_0)^n
       (f-\langle f\rangle_{\Omega})\Omega_L\rangle .
 \tag{C.1}
\]
Here \(M_{e^{\beta V/2}}\) is **half of the spatial magnetic multiplier on each side**: the quadratic form \(\widetilde J_L\) has the same nonzero spectrum as the electric-symmetric \(K_L^{1/2}e^{\beta V}K_L^{1/2}\) used in VOL04/VOL05. This is a unitary-equivalence-of-nonzero-spectra argument (via \(AB\) and \(BA\)), not an assertion that their eigenfunctions coincide as spatial functions.

## D. Density of bounded eigenvector observables and the spectral root

For every nonvacuum eigenfunction \(\psi\) with eigenvalue \(\lambda>0\), the continuous-kernel identity \(\psi=\widetilde J_L\psi/\lambda\) gives a continuous representative. Since \(\Omega_L\) is positive and continuous on compact \(G^{3L^3}\), the ratio \(f=\psi/\Omega_L\) is bounded, continuous and gauge invariant. For an eigenfunction chosen real (the kernel is real), \(\langle f\rangle_{\Omega}=\langle \Omega_L,\psi\rangle=0\). Normalize \(\|\psi\|_2=1\), so \(C_{f,L}(n)=(\lambda/\Lambda_0)^n\).

Taking \(T\to\infty\) in (B.2), and then \(n\to\infty\), yields
\[
 \left(\frac{\lambda}{\Lambda_0}\right)^n
 \le M_{L,\psi}(18\beta)^n,\quad
 M_{L,\psi}<\infty
 \quad\Longrightarrow\quad
 \boxed{\lambda/\Lambda_0\le18\beta}.
 \tag{D.1}
\]
The bound applies to every real eigenfunction in every Gauss-physical center sector. Complex eigenfunctions can be resolved into real and imaginary parts because the kernel is real and commutes with complex conjugation. Positivity handles the zero-eigenvalue case, and compactness excludes any additional positive continuous spectrum away from zero. Consequently the *entire* nonvacuum physical transfer spectrum lies in \([0,18\beta\Lambda_0]\), for every finite \(L\ge3\) at fixed \(0<\beta<1/18\).

At \(\beta=1/1000\), the exact ratio ceiling is \(9/500\) and the lattice-time energy floor is \(\log(500/9)\). The all-sector result includes states with zero overlap with a chosen local Wilson loop, which VOL05 could not identify.

## E. Adversarial acceptance and publication boundary

**Proof derivation PASS (under standard published analytic inputs):** the finite-TV normalization, correct \(1/4\) tilt derivative, geometry, volume-independent exponential rate, arbitrary bounded spatial-slice source, positive transfer, strict positive vacuum, ratio observable, spectral root and all-center-sector extension.

**Machine evidence:** [original integer checker](../tests/ym4_su2_vol06_full_spectrum.py), [frozen HBP](../docs/certificate-atlas/YM4-VOL06-FULL-PHYSICAL-GAP-20261122.hbp), [PR #105](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/105). These are finite consistency controls and reproducibility receipts. They do not formalize Rebeschini–van Handel or Lüscher.

**Historical scope:** exponential clustering and positive lattice transfer at strong coupling are established subjects in constructive gauge theory. This note contributes an explicit all-sector audit for this project's chosen normalization and acceptance chain; it does not assert priority over previous strong-coupling mass-gap results.

**Continuum status OPEN:** The coupling threshold \(\beta<1/18\) is a small fixed bare-coupling region; the required 4D continuum trajectory is \(\beta(a)\to\infty\). Dobrushin's single-link \(\alpha\le18\beta(a)\) ceases to be contractive long before this limit. The 11 original continuum gates, uniform physical-scale reconstruction and weak-coupling/nontrivial continuum spectral gap remain OPEN. An external independent peer review of the analytic transfer identification remains to be obtained.

**New next target (VOL07):** prove a **gauge-invariant block/renormalized comparison** whose contraction \(q(a)\) obeys a *physical-scale* estimate \(q(a)\le e^{-m_\star b(a)a}\) for a step of \(b(a)\) temporal lattice spacings, including reflection-positive transfer compatibility and nonzero normalized local source weight through refinement. A successful block inequality would give a physical gap \(m_\star\) after a separate continuum OS/compactness argument. No such block comparison has been derived here.
