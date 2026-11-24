# YM4 VOL30 — spherical two-ended SU(2) Wilson measurement, Fischer freeze/replay and 3D atlas

**23 November 2026 · research-candidate finite-cutoff analytic certificate + exact integer spherical geometry.** Extends VOL26–29 without confusing a rendered lattice-point frame with an observed Gibbs expectation. The **original group variables are continuous SU(2)**; the *space-time lattice coordinates* remain four-dimensional integers at a fixed lattice cutoff. Spherical geometry and transfer bounds are certificates; neither point-cloud renderer nor Fischer transport supplies continuum-limit field measurements.

## 1. Original physical source, 4D Euclidean balls and two endpoints

Keep the untwisted even L^4 periodic original continuous SU(2) Wilson measure, transfer coordinate x2, and original same-orientation spatial 0–1 plaquette sources:
\[
 F=\tfrac12(1+\operatorname{Re}U_{p_0}),\quad p_0=(0,0,0,0;0,1),\qquad
 G=\tfrac12(1+\operatorname{Re}U_{p_d}),\quad p_d=(0,0,d,0;0,1).
\]
For the **frozen 3D demonstration** choose \(\beta=9^{12}\), \(L=128\), \(d=24\), original shell radii \(R=2,\dots,21\). These satisfy \(2R< L-d\); both radius-R chart balls are unambiguously embedded, including their overlap. The formulas below hold at any sufficiently large even L, fixed d>R>=2.

Use **Euclidean four-dimensional integer balls**
\[
 B_R(c)=\{x\in\mathbb Z^4:\sum_{j=0}^3(x_j-c_j)^2\le R^2\},\quad
 I_R(c)=\{(x,\mu):x,x+e_\mu\in B_R(c)\}.
\]
The centers are \(c=(0,0,0,0)\) and \(z=(0,0,24,0)\). The actual shell point clouds are \(\partial B_R(c)=\{x:\|x-c\|_2^2=R^2\}\) and \(\partial B_R(z)\) analogously. Every marker shown in the viewer has **four exactly specified integer coordinates**; the viewer projects them into three dimensions by the declared linear map
\[
 \pi(x_0,x_1,x_2,x_3)=
 (x_0+x_3/2,\ x_1-x_3/3,\ x_2+2x_3/5).
\]
Projection cannot preserve every 4D Euclidean distance or uniquely invert all 4D points. The point's original 4D tuple, not its projected screen position, is the canonical address.

The four source plaquette links lie in \(I_R(c)\) for every R>=2, since the largest vertex squared radius is 2. The four outer-source links lie in \(I_R(z)\) for every R>=2. For \(R<d\), each entire source remains outside the *other* endpoint's ball.

## 2. Separate true original-Wilson conditional measurement in each direction

Define the inward-link sigma-fields \(\mathcal I_R(c)=\sigma(U_e:e\in I_R(c))\) and \(\mathcal I_R(z)\) analogously. The **two ended-source predictors** are actual original continuous-SU(2) Gibbs conditional expectations
\[
 P_R^{c\to z}=E_\mu[G\mid\mathcal I_R(c)],\qquad
 P_R^{z\to c}=E_\mu[F\mid\mathcal I_R(z)].
\]
Put \(W_R^{c\to z}=\mathrm{Var}(P_R^{c\to z})\) and \(W_R^{z\to c}=\mathrm{Var}(P_R^{z\to c})\). Both fields increase with R, so both variances are **nondecreasing** under increasing radius; a rewind is a reversal of address order, *not a reversal of physical Euclidean time*.

The original Wilson action on the even periodic torus is invariant under the lattice reflection \(x_2\mapsto d-x_2\), which interchanges the two centers and maps each 0–1 spatial plaquette to the identical orientation. This measure-preserving symmetry yields the **exact reciprocity**
\[
 \boxed{W_R^{c\to z}=W_R^{z\to c}\quad\text{for every }R<d.} \tag{30.1}
\]
Let \(C_j=\mathrm{Cov}(F,G_j)\) be the original periodic spatial Wilson plaquette correlation and \(C_0=\mathrm{Var}(F)>0\). Because \(F\in\mathcal I_R(c)\) and \(G\in\mathcal I_R(z)\),
\[
 C_d=\mathrm{Cov}(F,P_R^{c\to z})
    =\mathrm{Cov}(P_R^{z\to c},G).
\]
Cauchy–Schwarz, conditional contraction and the exact time translation give
\[
 \boxed{
 \left(\frac{C_d}{C_0}\right)^2
 \le\frac{W_R^{c\to z}}{C_0}
 =\frac{W_R^{z\to c}}{C_0}
 \le1.} \tag{30.2}
\]
The equality between two directions is a mathematical symmetry; the *numerical value* of each true conditional variance has **not** been evaluated.

## 3. Two-sided native SU(2) nearest-slice interval: the opposite estimator

From VOL29's all-original-SU(2) source-local transfer inequality at any finite beta>0:
\[
 \frac{C_1}{C_0}\ge
 \ell_\beta:=\frac{[I_2(\beta)/I_1(\beta)]^8}{20e^{162\beta}}>0.
\]
Now derive a **new spatial-volume-independent nearest-slice upper bound**. Choose one true original positive link q of F's four-link plaquette. Conditional on every other original link, the translated F_1 uses none of q, while
\(F=(1+\langle U_q,c\rangle)/2\), \(\|c\|=1\). The VOL23 continuous-SU(2) six-staple variance bound gives
\(\mathrm{Var}(F-F_1\mid U_{\widehat q})
=\mathrm{Var}(F\mid U_{\widehat q})\ge B_\beta^{-1}\),
\(B_\beta=147456(1+6\beta)^2\).
Translation invariance gives \(\mathrm{Var}(F-F_1)=2(C_0-C_1)\) and the bounded source gives \(C_0\le1/4\). Consequently,
\[
 \boxed{0<\ell_\beta\le \frac{C_1}{C_0}
      \le 1-\frac{2}{B_\beta}<1.} \tag{30.3}
\]
At production beta=9^12, the exact integer-friendly strict lower is
\[
 \ell_\beta>\frac1{5120\,3^{45753584909922}},
\]
while the *upper* is the exact rational \(1-2/423433462692859012475599601664\). Neither endpoint was sampled by Monte Carlo or measured experimentally.

For all \(1\le d\le L/2\), the positive thermal Wilson transfer of VOL27 proves exact log-convex *lower propagation*, \((C_1/C_0)^d\le C_d/C_0\), and the paired spectral cosh identity proves exact **monotonicity** \(C_d\le C_1\). Thus for our d=24 at L=128:
\[
 \boxed{
 \bigl(5120\cdot3^{162\beta}\bigr)^{-24}
 < C_{24}/C_0
 \le1-2/B_\beta.} \tag{30.4}
\]
The lower predictor ratio in (30.2) is bounded by the **square** of the lower in (30.4). It is extraordinarily small yet uniform in total spatial volume at fixed beta and d. The upper \(1-2/B_\beta\) is **distance-independent**; it is *not* an exponential upper clustering rate and does not prove a mass gap.

## 4. Native 4D geometric dual intersection is exact and independently testable

At radius R, a site lies on **both** endpoint-centered spherical shells iff
\[
 |x-c|^2=R^2,\quad |x-z|^2=R^2.
\]
Subtracting gives \(x_2=12\) exactly (because d=24), with a separate three-square condition:
\[
 x_0^2+x_1^2+x_3^2=R^2-144. \tag{30.5}
\]
For R<12 there is no shared shell point. At R=12 the **only** shared lattice point is \((0,0,12,0)\); this is the exact 4D midpoint contact. At R=16 the continuous spheres geometrically intersect but the Diophantine three-square equation \(x_0^2+x_1^2+x_3^2=112\) has no integer solution (112=16·7, the classical three-square obstruction). The verifier enumerates and cross-checks exact integer shell points and all shared points at R=2..21, with no unverified fractional positions.

The contact is a **geometric event**, not a measured Yang–Mills correlation or signal velocity. Its appearance on the forward and backward display validates two-ended integer-geometry addressing; the actual Wilson expectation certificates remain (30.1)–(30.4).

## 5. Bobby Fischer deterministic freeze/play, 9 / 20 frames and third witness

The player supports **nine** R frames 2..10 or **twenty** R frames 2..21. The same source and outer endpoint are held fixed, while the user can play either list **forward (ascending R)** or **backward (descending R)**, pause, step, and freeze/restore an exact address.

A canonical frame receipt is the UTF-8 string:
\[
 \texttt{YM4-VOL30|L=128|d=24|R=<R>|shell_points=<N_R>|dual_intersection=<J_R>|source=0,0,0,0|outer=0,0,24,0}.
\]
The standalone [frame inventory](YM4-VOL30-SPHERE-FRAMES-20261123.json) pins the actual full SHA-256 for each of the 20 radii. For each reversible playback, the same radius must reconstruct identical 4D integer shell coordinates and frame receipt. The **third witness** independently checks all generated coordinates against both integer squared-distance equations and validates the display-independent symmetric reflection of the two endpoint sources. The viewer's numerical 3D canvas rotation is a **non-proof projection** and may use floating-point rendering; the certificate verifier uses strictly integer operations only. Browser-side SHA-256 is verified when a secure browser crypto API exists; otherwise the pinned hash is displayed with its verification status explicitly withheld. HBP stores counts and receipts; it does not imply measured spectral data.

This adapts the established *Bobby Fischer freeze-and-play/reverse replay* as a **deterministic certificate navigation procedure** (forward worker, reverse reflection, independent matrix/geometry witness). It does **not** claim reverse Euclidean dynamics, quantum cloning, information-theoretic inversion of SHA or recovery of unknown Wilson field variables.

## 6. Continuous-measurement conformity and next acceptance

**YES — model-level mathematical conformity.** The conditional expectation and transfer inequalities are statements for the genuine continuous-SU(2) Haar Gibbs measure on the original four-dimensional Wilson lattice; positive original link distributions, bounded Wilson observables and reflection symmetry are fully preserved. The two-ended reciprocity identity (30.1) and the two-sided inequalities can be checked against exact original-Wilson measurements in future Monte Carlo or formal interval quadrature.

**OPEN — physical continuum-measurement conformity.** The 3D points are lattice-site positions, not samples of the SU(2) gauge field. No per-shell field covariance or actual numerical measured \(W_R\) has been produced, and no \(a\to0\) renormalized continuum field limit has been certified. The 11 original continuum-construction obligations remain OPEN. The new upper \(C_1/C_0<1\) has no distance-dependent exponential factor, so the original physical mass-decay/shell-rate \(\kappa_r\ge1-e^{-2ma}\) remains OPEN.

**Supporting artifacts:** [strict integer 4D sphere and dual-link checker](../../tests/ym4_vol30_spherical_fischer.py); [frozen HBP](YM4-VOL30-SPHERICAL-FISCHER-20261123.hbp); [standalone playable 3D atlas](vol30-spherical-fischer.html); [exact 20-frame JSON inventory](YM4-VOL30-SPHERE-FRAMES-20261123.json). Candidate atlas link is integrated in the draft PR; no renumbering of the original accepted 115 proof nodes or silent mutation of main.
