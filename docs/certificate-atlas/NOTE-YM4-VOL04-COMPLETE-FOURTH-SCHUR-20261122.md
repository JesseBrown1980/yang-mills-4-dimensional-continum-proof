# YM4-VOL04 — complete fourth-order physical neutral plaquette coefficient at fixed spatial L>=3

**22 November 2026.** Exact rational SU(2) Haar/Schur coefficient calculation, source submitted to hosted independent replay. The quantitative error is \(O_L(\beta^5)\) for each fixed \(L\); its constant has not yet been proved independent of \(L\). Spatial-volume-uniform finite-\(\beta\) gap, 4D continuum and continuum mass gap remain **OPEN**.

Builds on [VOL01](NOTE-YM4-VOL01-VOLUME-SLOPE-OBSTRUCTION-20261122.md), [VOL02](NOTE-YM4-VOL02-THIRD-MAGNETIC-SELECTION-20261122.md) and [VOL03](NOTE-YM4-VOL03-CUBE-HAAR-NAVIER-CERTIFICATE-20261122.md). All formulas refer to the original physical Gauss-invariant **continuous SU(2)** 24-link-at-L2 / \(3L^3\)-link-at-L operator, all fundamental plaquette magnetic terms and the full Peter–Weyl space. No finite group truncation is used.

## 1. Operator and target

Let \(L\ge3\), \(N=3L^3\), \(\phi_i=\chi_{1/2}(U_i)\) for the \(N\) elementary spatial plaquettes, and \(W_i=\phi_i/2\). Set \(V=\sum_i W_i\). Let \(K\) be the exact normalized electric convolution with one-link Fourier eigenvalues \(\kappa_r(\beta)=I_{r+1}(\beta)/I_1(\beta)\), \(t=\kappa_1(\beta)^4\), and physical transfer \(J=K^{1/2}e^{\beta V}K^{1/2}\), suppressing the common scalar \(e^{-N\beta}\). Let \(P\) project onto the \(N\)-dimensional neutral four-fundamental plaquette band, \(P_0\) onto electric vacuum, \(R\) onto the remaining neutral electric spin networks.

For fixed finite \(L\), denote by \(\Lambda_{\rm vac}(\beta)\) the true physical vacuum transfer eigenvalue. Let \(F_P(\beta,\nu)\) be the \(P\)-space Feshbach effective operator at spectral parameter \(t\nu\), after eliminating \(P_0\) and \(R\). The **vacuum-normalized effective operator**, still energy-dependent but uniformly for \(\nu\) in its fixed-L plaquette spectral window, is

\[
\frac{F_P(\beta,\nu)}{\Lambda_{\rm vac}(\beta)}
 =\left(1-\frac{\beta^2}{8}\right)I_N+
 \beta^4 Q_L + O_L(\beta^5)
\]

where the fourth-order coefficient is the **explicit complete matrix**

\[
\boxed{Q_L=\frac{23}{384}I_N+
\frac{A_{\rm cube,L}+A_{\rm edge,L}}{256}.}
\]

Here \(A_{\rm cube,L}(i,j)=1\) for distinct faces of the same elementary cube and zero otherwise; \(A_{\rm edge,L}(i,j)=1\) for distinct elementary plaquettes that share one original spatial link and zero otherwise. Both have zero diagonal. The matrix \(Q_L\) includes vacuum subtraction and the **entire order-four contribution from the all-spin physical electric complement**; only the **finite-\(\beta\) remainder** remains to be bounded uniformly in \(L\).

This statement concerns the **effective plaquette-band transfer matrix** and its Taylor coefficient; it is not a spectral-gap proof for all spatial volumes or a finite-\(\beta\) volume-uniform theorem.

## 2. Haar identities and vacuum/disconnected cancellation

For every distinct plaquette pair \(i\ne j\), their supports overlap on at most one link. The SU(2) character identity \(\chi_{1/2}(U)^2=1+\chi_1(U)\), together with an exclusive link on each of any three distinct elementary plaquettes, gives

\[
\langle\phi_i^2\rangle=1,\quad
\langle\phi_i^4\rangle=2,\quad
\langle\phi_i^6\rangle=5,\quad
\langle\phi_i^2\phi_j^2\rangle=1,\quad
\langle\phi_i^4\phi_j^2\rangle=2,\quad
\langle\phi_i^2\phi_j^2\phi_k^2\rangle=1
\]

for mutually distinct \(i,j,k\). The even single-loop moments 1,2,5 follow independently from the exact SU(2) fundamental character fusion recurrence. More generally, products of five or fewer plaquette factors with nonzero net \(\mathbb Z_2\) edge parity vanish by Haar center invariance (VOL02).

Write \(a(\beta)=\langle0,e^{\beta V}0\rangle\), \(f_i(\beta)=\langle\phi_i,e^{\beta V}0\rangle\). Enumerating repeated-plaquette multisets gives, for \(N=3L^3\),

\[
\begin{aligned}
a(\beta)&=1+\frac N8\beta^2+\frac{3N^2-N}{384}\beta^4+O_L(\beta^6),\\
f_i(\beta)&=\frac{\beta}{2}+\frac{3N-1}{48}\beta^3+O_L(\beta^5).
\end{aligned}
\]

The exact vacuum Schur elimination at transfer eigenparameter \(\lambda=t\nu\) contributes \(-f f^*/(a-\lambda)\). Because \(t=O(\beta^4)\), replacing \(1/(a-\lambda)\) by \(1/a\) changes this order-four expansion only at order \(\beta^6\).

For \(i\ne j\), the **even-parity/disconnected** part of \( \langle\phi_i,V^4\phi_j\rangle/24\) is \((3N-2)/96\), exactly equal to the order-four coefficient of \(f_i f_j/a\). The only additional parity-compatible six-distinct-face contribution at this order is an elementary cube boundary (VOL02). VOL03's independently contracted continuous-SU2 six-face Haar integral is \(1/16\), giving \(1/256\) for each cube that contains both \(i\) and \(j\). Therefore

\[
\bigl[\tfrac1{24}PV^4P-f f^*/a\bigr]^{(4)}_{ij}
=\frac1{256}A_{\rm cube,L}(i,j),\qquad i\ne j.
\]

For the diagonal, the pair combinatorics give

\[
\frac1{24}\langle\phi_i,V^4\phi_i\rangle
=\frac{3N^2+5N-3}{384},\quad
\bigl[f_i^2/a\bigr]_{\beta^4}=\frac{3N-2}{96}.
\]

These values are **exact** for each finite \(L\ge3\).

At second order the same character moments yield
\[
\bigl[\tfrac12 PV^2P-f^{(1)}f^{(1)*}\bigr]_{ij}
=\frac{N-1}{8}\delta_{ij}.
\]
All first- and third-order band coefficients vanish by the previously certified parity argument.

## 3. Entire physical electric tail at fourth order

By the SU(2) Gauss constraint and center-neutral sector classification at spatial \(L\ge3\), every other nonvacuum neutral spin network has total twice-spin index \(S\ge6\). Relative to \(t=\kappa_1^4\), the only \(S=6\) states that can be reached by one magnetic insertion from a single \(S=4\) plaquette are **six-link fundamental Wilson loops** formed as the perimeter of two elementary plaquettes sharing one link.

Let \(i\ne j\) share exactly one link and \(\phi_{ij}\) be the normalized fundamental character of their exterior six-link perimeter. Exact SU(2) linkwise Haar orthogonality, also rechecked by an independently ordered integer quaternion contraction in the new test, yields

\[
\langle\phi_{ij},\phi_i\phi_j\rangle=\frac12,\qquad
\|\phi_{ij}\|^2=1.
\]

The spin-zero component of the two fundamental link factors on the shared edge is thus \(\phi_{ij}/2\), and all other components have total twice-spin index \(\ge8\). Consequently

\[
P_{S=6} V\phi_i
=\frac14\sum_{\substack{j\ne i\\ j\text{ shares an edge with }i}}\phi_{ij}.
\]

For \(L\ge3\), there are precisely 12 distinct edge-sharing \(j\) for every \(i\), and the six-link perimeter states obtained from two different pairs of elementary plaquettes are orthogonal (the VOL01 unique-symmetric-difference lemma). Each \(S=6\) perimeter eigenstate has \(K_{S=6}/t=\kappa_1(\beta)^2=\beta^2/16+O(\beta^4)\). In the complete physical Schur complement, the resulting fourth-order term is

\[
\boxed{\bigl[H_{4,\mathrm{tail}}\bigr]_{ij}
=\frac{12}{256}\delta_{ij}+
  \frac1{256}A_{\rm edge,L}(i,j).}
\]

States with \(S\ge8\) and all higher-spin electric mixing enter at order \(\beta^6\) or higher for each fixed finite \(L\); the vacuum modification of the \(E\)-to-tail coupling is also higher order. Therefore this formula **includes every physical electric-tail contribution at order four**.

The complete fourth-order diagonal before vacuum normalization is
\[
h_{4,\mathrm{diag}}(L)=
\frac{3N^2+5N-3}{384}
-\frac{3N-2}{96}+\frac{12}{256}
=\frac{3N^2-7N+23}{384}.
\]

## 4. Normalize by the genuine physical vacuum

The true vacuum transfer eigenvalue obeys \(\Lambda_{\rm vac}=a+O_L(\beta^6)\): its coupling to the \(S=4\) plaquette band has magnitude \(\sqrt t\,f=O_L(\beta^3)\), hence its first eigenvalue displacement appears at order \(\beta^6\). The neutral \(S\ge6\) sector contributes still higher orders.

Since the second-order plaquette coefficient is \((N-1)/8\) and the vacuum second-order coefficient is \(N/8\), their difference is \(-1/8\), independent of \(N\). At fourth order the diagonal coefficient after division by \(a\) is

\[
\begin{aligned}
&\frac{3N^2-7N+23}{384}
-\frac{3N^2-N}{384}
+\frac{N}{64}\\
&\hspace{25mm}=\boxed{\frac{23}{384}}.
\end{aligned}
\]

Thus all extensive \(N\) and \(N^2\) contributions cancel **algebraically**. Together with the off-diagonal terms, this establishes the announced \(Q_L\) formula. The cancellation is exact at the Taylor-coefficient level; control of the higher-order \(O_L\) terms uniformly as \(L\to\infty\) remains a separate gate.

## 5. Exact volume-independent operator norm of the complete fourth-order coefficient

Every elementary plaquette belongs to two cubes and has exactly **10 distinct cube-neighbor faces**. It shares one original link with exactly **12 other plaquettes**. Of those neighbors, 8 are also cube-neighbors, so the union contains 14; overlap receives the sum of the two genuine operator contributions. These statements hold at every \(L\ge3\) and were independently checked by [exact integer source](../../tests/ym4_su2_vol04_full_fourth_schur.py) at \(L=3,4,5\).

Both adjacency matrices are real symmetric, zero-diagonal and nonnegative. Hence \(Q_L\) has constant row sum
\[
\frac{23}{384}+\frac{10+12}{256}
=\boxed{\frac7{48}}.
\]
Its constant vector is an eigenvector; the maximum absolute row-sum bounds the operator norm. Therefore

\[
\boxed{\|Q_L\|_{\ell^2\to\ell^2}=\frac7{48}\quad
\text{for every }L\ge3.}
\]

This bounds the **complete vacuum-normalized fourth-order coefficient**, including the leading physical electric tail, uniformly in spatial volume. It is a stronger statement than VOL03's isolated cube-only \(\|B_{\rm cube,L}\|=5/128\). The finite-\(\beta\) physical-transfer remainder still requires a *uniform-in-L bound*.

## 6. Perron mode and a necessary distinction for the volume theorem

The combined cube/edge adjacency graph is connected for every \(L\ge3\); the 12 edge-neighbors permit translations and changes of plaquette orientation. Perron–Frobenius gives a unique constant top eigenvector of \(Q_L\), equal to \(N^{-1/2}(1,\ldots,1)\). A **single local plaquette basis source** has squared projection \(1/N=1/(3L^3)\) onto this top fourth-order mode.

More importantly, the *next* fourth-order band eigenvalue approaches the top as \(L\) grows. Take a plane-wave test vector \(x_{s,ab}=e^{2\pi i s_1/L}\), independent of plaquette orientation. It is orthogonal to the constant vector. Every cube- or edge-neighboring pair has at most one unit of displacement along the first coordinate, so its Rayleigh deficit is bounded by
\[
0<\mu_1(Q_L)-\mu_2(Q_L)
\le\frac{22}{256}\bigl(1-\cos(2\pi/L)\bigr)
<\frac{55}{32L^2},
\]
using \(1-\cos z\le z^2/2\) and \(\pi^2<10\).

**Acceptance implication:** a positive lower bound on the *spacing of the first two individual neutral-band momentum levels* cannot remain independent of \(L\) at this Taylor order. The appropriate target is instead a **vacuum-to-excitation mass gap / local Wilson spectral band or connected correlator estimate**, with the local spectral weight summed over the band, not concentrated on one translationally symmetric eigenvector. This does not preclude a positive Yang–Mills mass gap.

## 7. Acceptance and remaining work

- **VOL04-A, exact coefficient:** complete original SU2 fourth-order physical Schur coefficient \(Q_L\), including all disconnected-vacuum cancellation and \(S=6\) electric-tail terms — exact-rational producer and source audit provided, hosted replay pending.
- **VOL04-B, volume-independent coefficient norm:** \(\|Q_L\|=7/48\) for all \(L\ge3\) — exact geometry and row-sum theorem, hosted replay pending.
- **VOL04-C, fixed-volume finite-\(\beta\) remainder:** \(O_L(\beta^5)\), still requiring an explicit usable bound for each \(L\) — OPEN.
- **VOL04-D, uniform-volume remainder:** prove a normalized *connected/linked-cluster* estimate with constants independent of \(L\), including exact Wilson vacuum and all higher spins — OPEN.
- **VOL04-E, uniform physical vacuum gap and local connected Wilson two-point/spectral-band weight:** OPEN.
- **VOL04-F, weak-coupling and 4D continuum scaling with OS reconstruction:** OPEN.

The original eleven continuum construction obligations remain OPEN. The source-based verdict explicitly distinguishes exact fourth-order coefficient algebra from a complete finite-\(\beta\) or continuum spectral-gap theorem.
