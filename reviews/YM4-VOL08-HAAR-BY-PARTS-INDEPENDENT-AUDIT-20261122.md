# Independent analytic route for YM4-VOL08 — exact integration-by-parts Haar check and worst-case gauge-invariant boundary witness

**2026-11-22 · Fresh mathematical reconstruction · no claim of an external human peer review.** Reviews [YM4-VOL08 original Wilson star note](../docs/certificate-atlas/NOTE-YM4-VOL08-ORIGINAL-SU2-WILSON-STAR-20261122.md) by a second calculation, distinct from its Gamma stochastic-order proof. The mathematical content concerns the **original continuous SU(2) 4D Wilson action**, while the accompanying Q8 test checks only finite algebra.

## 1. Independent continuous-Haar concentration proof

Fix \(\kappa>0\), a unit quaternion axis \(h\), and the SU2 Haar tilt \(d\nu_\kappa(u)\propto e^{\kappa u\cdot h}du\). For \(t=1-u\cdot h\in[0,2]\), the normalized density is proportional to \(w_\kappa(t)=t^{1/2}(2-t)^{1/2}e^{-\kappa t}\). Define
\[
F_\kappa(t)=t^{3/2}(2-t)^{1/2}e^{-\kappa t},
\]
which vanishes at both endpoints. Its derivative is
\[
F'_\kappa(t)=w_\kappa(t)
\Bigl(\tfrac32-\frac{t}{2(2-t)}-\kappa t\Bigr).
\]
Integrate from \(0\) to \(2\); endpoint singularities remain integrable. Dividing by \(\int_0^2w_\kappa(t)dt\) gives the **exact identity**
\[
\kappa\,\mathbb E_\kappa[t]
=\frac32-\frac12\mathbb E_\kappa\!\left[\frac{t}{2-t}\right]
\le\frac32.
\]
Therefore
\[
\boxed{\mathbb E_\kappa(u\cdot h)\ge1-\frac{3}{2\kappa}}.
\]
This independent integration-by-parts proof confirms the main note's Gamma/monotone-tilt result with the correct \(3/2\) constant. It uses the continuous \(S^3\) Haar density and no Bessel-series estimates or subgroup approximation.

## 2. The original star conditional is genuinely gauge covariant

For each original oriented link \(e=(x,\mu)\), use the two three-edge complementary paths for each \(\nu\ne\mu\):
\[
S_{\nu,+}=U_{x+\mu,\nu}\,U^{-1}_{x+\nu,\mu}\,U^{-1}_{x,\nu},
\qquad
S_{\nu,-}=U^{-1}_{x-\nu+\mu,\nu}\,U^{-1}_{x-\nu,\mu}\,U_{x-\nu,\nu}.
\]
Their inverses \(s_{\nu,\pm}=S_{\nu,\pm}^{-1}\) have the **same gauge endpoints** as \(U_{x,\mu}\). With \(H=\sum_{\nu,\pm}s_{\nu,\pm}\), the normalized conditional measure is exactly \(e^{\beta u\cdot H}du/Z(\beta|H|)\). The observable \(u\cdot s_{\nu,\pm}=\frac12\operatorname{Tr}(U_eS_{\nu,\pm})\) is a full Wilson plaquette; \(s_i\cdot s_j=\frac12\operatorname{Tr}(s_i^{-1}s_j)\) is a closed six-edge loop. It is therefore legitimate to compare these conditioned observables rather than raw gauge-dependent links.

The integer checker independently reconstructs all six oriented paths on every link of \(3^4\) and \(4^4\), checks the eighteen distinct other original links, and uses noncommuting quaternion rotations at every lattice vertex to verify gauge covariance and all 15 six-link loops. No physical center sector is identified solely from this local test.

## 3. Good-star and one-external-link bad-star independent bound reconstruction

Suppose \(s_i\cdot s_j\ge1-\epsilon\), \(0\le\epsilon<1\), for every pair. Then \(s_i\cdot H\ge6(1-\epsilon)\), \(|H|\in[6(1-\epsilon),6]\), and \(s_i\cdot H/|H|\ge1-\epsilon\). Haar-tilt integration-by-parts and the conditional mean vector give
\[
1-\mathbb E(W_i\mid\mathrm{exterior})\le
\epsilon+\frac1{4\beta(1-\epsilon)}.
\]
The probability of \(W_i\le1-\delta\) is bounded by this quantity divided by \(\delta\), and the union of six failure events is bounded sixfold. For the archived rational test \((\beta,\epsilon,\delta)=(81,1/81,1/3)\), a fresh common-denominator calculation gives \(1/81+1/320=401/25920\), hence \(401/8640\) per plaquette and \(401/1440\) for the six-plaquette union.

For the adversarial boundary, assign \(s=(+,-,+,-,+,+)\) and change only the last \((x-\nu+\mu,\nu)\) external link from \(+I\) to \(-I\). The preferred list becomes \((+,-,+,-,+,-)\). The distinguished upper staple is \(+I\) in both cases; the tested plaquette \(X=\operatorname{Re}U_e\) is the **same gauge-invariant loop**. The first exterior has \(|H|=2\), giving \(\mathbb E(1-X)\le3/(4\beta)\); the second has \(H=0\), giving SU2 Haar. For \(0<\delta\le1\), the Haar cap probability obeys
\[
\Pr_{\rm Haar}(X\ge1-\delta)
=\int_{1-\delta}^1\frac2\pi\sqrt{1-x^2}dx\le\delta
\]
because its density is at most \(2/\pi<1\) on \([0,1]\).
Hence the **one-external-link** gauge-invariant pushforward bound is
\[
\operatorname{TV}(\nu_{H=2I},\nu_{\rm Haar})
\ge1-\delta-\frac3{4\beta\delta}.
\]
At \(\beta=k^2,\delta=1/k\), its lower bound is \(1-\frac7{4k}\to1\); at \(k=9\), it is \(29/36\). The full aligned \(H=6I\) comparison yields \(1-\frac5{4k}\), or \(31/36\) at \(\beta=81\).

This audit verifies a **worst-case local conditional TV obstruction**, including a legitimate gauge-invariant observable and a single original neighbor change. It does not establish failure of a **multiscale averaged gauge-invariant cube** criterion; it also does not identify a pointwise sharp Kantorovich coefficient in a separately specified chordal or transported block metric.

## 4. Evidence and next mathematical target

- **SU2 Haar tilt**: exact integration-by-parts proof PASS, independently derived from the Gamma-weight argument.
- **Original Wilson action / gauge endpoints**: independent algebraic inspection PASS; actual \(3^4\) and \(4^4\) integer checker is an additional falsifier.
- **Good/bad gauge-invariant source and TV bounds**: rational inequalities and separate boundary fixtures PASS.
- **Machine checker**: [source](../tests/ym4_su2_vol08_wilson_star.py), [frozen HBP](../docs/certificate-atlas/YM4-VOL08-WILSON-STAR-20261122.hbp). Hosted workflow status is tracked by its PR; a green workflow is **not** a formal mechanization of the Haar integral.
- **External independent peer review**: OPEN.
- **A uniform volume / all-boundary weak-coupling physical-size one-cube condition and the eleven continuum gates**: OPEN.

**VOL09 acceptance:** a *gauge-invariant block* definition and a quantitative bound on its **bad-boundary frequency or weighted influence** under the original Wilson conditional Gibbs laws, stable as \(\beta(a)\to\infty\). The known [v7 one-cube work](https://hexagonmath.org/2610.00341v7) also distinguishes averaged DS conditions from single-link TV, and is a reference for the relevant proof architecture. Only after a source-conditioned local-to-block coupling and a uniform physical block rate should one apply the conditional VOL07 spectral-root theorem.
