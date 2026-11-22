# YM4-VOL07 — exact physical-scale block-gap criterion and weak-coupling acceptance interface

**2026-11-22 · Original continuous SU(2) lattice Wilson construction.** This is a proved *conditional spectral implication*, with an exact-integer arithmetic acceptance pilot and clearly enumerated physical inputs. The gauge-theory block hypothesis itself is OPEN. Every original continuum obligation remains OPEN.

## 1. Why VOL06 needs a new scale

[The VOL06 independent analytic review](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/105) reconstructs the original continuous-SU(2) full physical finite-volume transfer bound
\[
0\le\lambda_{\rm exc}/\Lambda_0\le18\beta
\quad(0<\beta<1/18,\ L\ge3).
\]
It uses the published Rebeschini–van Handel classical Dobrushin comparison theorem and the original positive Wilson transfer construction. The coefficient 18 is fixed by the original 4D six-plaquette-per-link incidence. Along a 4D continuum tuning with lattice spacing \(a\downarrow0\), the bare coupling satisfies \(\beta(a)\to\infty\), so the *single-link contraction certificate* \(\alpha\le18\beta(a)<1\) is unavailable.

The mathematical replacement must operate at a **physical time scale**, retaining Gauss projection, original group \(SU(2)\), full physical sectors, and reflection positivity.

## 2. Exact conditional theorem (all physical sectors)

For every spatial finite volume \(L\), bare spacing \(a>0\), let \(J_{a,L}\) be the positive trace-class Wilson temporal transfer with unique positive vacuum \(\Omega_{a,L}\), top eigenvalue \(\Lambda_0(a,L)\), and physical spectrum in \([0,\Lambda_0]\). Fix an integer block time \(b(a)\ge1\) and a contraction \(q(a)\in(0,1)\).

**Block covariance hypothesis \(H_{\rm block}\):** For **every** bounded real Gauss-invariant spatial-slice observable \(f\) there exists a finite prefactor \(M_{a,L,f}\) such that, for **all integers \(n\ge1\)**,
\[
\left|\operatorname{Cov}_{a,L}\big(f_0,f_{n\,b(a)}\big)\right|
\le M_{a,L,f}\,q(a)^n. \tag{2.1}
\]
The covariance is in the actual Wilson path-integral law, or equivalently the physical Gauss-projected transfer vacuum. Its prefactor may depend on \(a,L,f\); **the same \(q(a)\)** must work for every physical finite \(L\) and every bounded physical slice \(f\).

**Theorem VOL07-A (spectral root):** Under \(H_{\rm block}\), the physical nonvacuum transfer ratios obey
\[
\boxed{\sup\sigma(J_{a,L}/\Lambda_0)\big|_{\Omega^\perp}
\le q(a)^{1/b(a)}}\quad\text{for every finite }L.
\]
Proof: for any nonvacuum eigenstate \(\psi\) of positive eigenvalue \(\lambda\), write \(f=\psi/\Omega\). Continuity of the transfer kernel, compactness of configuration space and strict vacuum positivity ensure \(f\) is a bounded gauge-invariant slice observable. Its connected transfer covariance at block time \(n\,b(a)\) is \((\lambda/\Lambda_0)^{n b(a)}\); hence \((\lambda/\Lambda_0)^{b(a)}\le q(a)\) after taking \(n\)th roots. Extend to the full spectrum by compactness and nonnegative transfer. **This exact deduction is independent of the sizes of the prefactors.**

Define the *physical-unit* lattice transfer energy gap
\[
m_{a,L}:=-a^{-1}\log\left(\sup\sigma(J_{a,L}/\Lambda_0)\big|_{\Omega^\perp}\right).
\]
Then
\[
\boxed{m_{a,L}\ge\frac{-\log q(a)}{a\,b(a)}}. \tag{2.2}
\]

**Corollary VOL07-B (uniform physical mass floor):** If a constant \(m_\star>0\) is certified and
\[
q(a)\le e^{-m_\star a\,b(a)} \quad\text{uniformly along the tuned family}, \tag{2.3}
\]
then \(m_{a,L}\ge m_\star\) for all spatial volumes \(L\) and all spacings in that family.

Equivalent exact-rational sufficient form:
\[
q(a)\le1-m_\star a\,b(a)\in(0,1)
\quad\Longrightarrow\quad q(a)\le e^{-m_\star a\,b(a)}
\]
by \(1-x\le e^{-x}\) for \(x\ge0\).

**Important continuum boundary:** A lattice family with this spectral floor alone does not construct the nontrivial continuum theory. OS positivity, consistent limiting Schwinger functions, physical source normalization and a nonzero limiting state require their own certified inputs. If an OS limit exists, convergence of the chosen normalized connected correlators plus uniform mass floor passes the exponential spectral support ceiling to the limit. A nonzero continuum spectral sector additionally needs positive limiting source norm and nonzero appropriate finite-time correlation (or an equivalent spectral-weight witness).

## 3. Two distinct block-design regimes

**A. Fixed microscopic block count \(b(a)=1\).** A physical mass floor \(m_\star\) requires \(q(a)\le1-m_\star a+O(a^2)\), i.e. the contraction moves toward one as \(a\downarrow0\). A worked toy inequality (no SU2 claim): \(a=3^{-k}\), \(q=1-a/2\), gives \(m_{a,L}\ge1/2\) for every \(k\ge1\) from \(-\log(1-x)\ge x\).

**B. Fixed physical block time \(\ell(a)=a b(a)\) with \(0<\ell(a)\le\ell_{\max}\).** A contraction \(q(a)\le q_\star<1\) yields \(m_{a,L}\ge-\log(q_\star)/\ell_{\max}\). A ternary example \(a=3^{-k}\), \(b(a)=3^k\), \(q=1/2\) gives \(\ell=1\) and \(m\ge\log2>1/2\). This is the most natural interface for a gauge-invariant physical-size one-cube inequality.

**Negative control:** \(b=1\), \(q=1-a^2/2\) has \(-\log q/a\le a/(2-a^2)\to0\); the apparent contraction is insufficient for a positive **uniform physical-unit** mass floor. The original single-link factor \(18\beta(a)\) also fails to be a contraction when \(\beta(a)\ge1/18\). Exact integer code [ym4_su2_vol07_block_rate.py](../../tests/ym4_su2_vol07_block_rate.py) checks all these inequalities with explicit red controls; its toy numbers are never misidentified as SU2 block measurements.

## 4. Source-correlated next acceptance target: one cube plus spectral weight

The November 2026 preprint [*Yang–Mills Mass Gap on the Lattice and One Cube from the Continuum*, 2610.00341v6](https://hexagonmath.org/pdf/2610.00341v6), explicitly separates a physical-size Dobrushin–Shlosman cube criterion from the open inputs for a nontrivial continuum Yang–Mills theory. Its stated open items include: (O1) the cube estimate uniformly along the continuum tuning, (O2) a four-dimensional nonvanishing limiting slice/source ratio, and (O3) higher Schwinger-function tree estimates. Its fixed-lattice coupling normalization, forest-gauge map and conditional continuum theorems must be independently matched to this original physical SU2 Wilson transfer before importing quantitative constants.

This identifies a focused, model-specific next calculation:

1. **Gauge-covariant block specification:** define a physical-size cube map \(B_a\) from original SU2 link fields to center-neutral and center-charged physical boundary observables, including a normalized measure and exact Gauss gauge action.
2. **Quantitative block influence:** calculate or bound the *actual original Wilson conditional* block-to-block influence \(C_{XY}(a)\), all boundary conditions, all relevant physical sectors. Produce a finite \(\alpha_{\rm block}(a)\) and prove either \(q(a)\le1-m_\star a b(a)\) or \(q(a)\le q_\star<1\) for \(a b(a)\le\ell_{\max}\).
3. **Physical transfer passage:** verify the block covariance estimate for **arbitrary bounded Gauss-invariant slice observables**, not just one local Wilson loop; use VOL07-A to certify the complete transfer spectrum.
4. **Continuum visibility and OS closure:** independently bind nonzero normalized connected sources and limiting higher Schwinger functions so the physical mass gap survives in a nontrivial 4D reconstruction.

## 5. Exact reproducibility and verdict

[Integer-only rate checker](../../tests/ym4_su2_vol07_block_rate.py) and [frozen receipt](YM4-VOL07-PHYSICAL-BLOCK-RATE-20261122.hbp) validate the **logical rate interface and counterexamples**, including ternary scales \(3^{-k}\) at \(k=1,\dots,12\). The all-k inequalities follow from elementary proofs, with finite replay as an independent falsifier.

- **VOL07-A:** general positive-transfer block covariance \(\Rightarrow\) entire physical-spectrum bound — **CONDITIONAL THEOREM, PROOF RECONSTRUCTED**.
- **VOL07-B:** rational sufficient contraction \(q\le1-m_\star ab\) \(\Rightarrow\) uniform physical lattice gap — **EXACT ELEMENTARY LEMMA**.
- **VOL07-C:** original continuous SU2 gauge-invariant physical-size block influence inequality along \(\beta(a)\to\infty\) — **OPEN**.
- **VOL07-D:** positive renormalized 4D source weight, OS continuum reconstruction and full continuum mass gap — **OPEN**.

The original eleven continuum proof obligations remain OPEN. This stage supplies the exact acceptance target rather than asserting a weak-coupling calculation has already passed.
