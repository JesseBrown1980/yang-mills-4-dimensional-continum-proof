# YM4-06E — interacting SU(2) Wilson transfer: finite-volume physical gap and certified ternary cutoffs

**Date:** 2026-11-11. **Status:** exact-integer finite-volume spectral *enclosures*, prediction-first hosted verification. **NOT a 4D continuum mass-gap theorem.** This experiment extends the explicitly one-link YM4-06D pilot; it does not pretend that a noninteracting SU(2) transfer is the full interacting 4D spectrum.

Prediction-only freeze: docs/PREDICTION-YM4-06E-INTERACTING-WILSON-20261111.hbp, commit 89904ca89abc5962162e25509e5c20cf9588151e, before the executable. Runner: GitHub Actions 43048633445, originally PASS on correction head 67f4202122650315c7c02e9977da49caf5cc730d. Complete HBP/HBI/SHA/SH/HASH and SHA256SUMS are filed in evidence/.

## 1. The actual interacting finite spatial model

Let the spatial torus be (Z/1)^3: one spatial vertex with three oriented loop links U=(U_x,U_y,U_z) in SU(2)^3. The periodic spatial Wilson plaquettes are the three commutator loops [U_x,U_y], [U_x,U_z], [U_y,U_z]. These plaquettes are nonconstant and genuinely link-coupled: for unit quaternions i,j, [i,j]=−1 whereas [1,j]=1. They cannot be replaced by one-link factors.

Choose the **declared anisotropic couplings** beta_s=1/16 and beta_t=1, normalized SU(2) Haar measure and the exact Wilson weight w_beta(g)=exp[−beta(1−Tr(g)/2)]. Define

\[
 A(U)=\prod_{i<j}w_{\beta_s}([U_i,U_j]),\qquad
 (Bf)(U)=\int_{SU(2)^3}\prod_i w_{\beta_t}(U_i V_i^{-1})f(V)\,dV,
\]

and let P_G be the simultaneous-conjugation gauge projector. The transfer operator on physical gauge-invariant functions is

\[
 T=\left[A^{1/2} B P_G A^{1/2}\right]_{\mathcal H_{\rm gauge}},
 \quad \mathcal H_{\rm gauge}=L^2(SU(2)^3)^{SU(2)}.
\]

B is a positive compact convolution product, A is a bounded strictly positive gauge-invariant multiplication operator, and P_G commutes with both. Thus T is positive compact. This is an *interacting gauge-invariant* 3+1D Wilson transfer at **fixed** finite side-one spatial geometry. It is not the L>=2 lattice continuum sequence and has no spacing/coupling renormalization yet.

## 2. Full physical first transfer gap — no state-space diagonalization needed

By exact SU(2) character convolution, each matrix-coefficient block of twice-spin n has eigenvalue

\[
 b_n=e^{-1}\ell_n(1),\qquad
 \ell_n(1)=\sum_{s\ge0}\frac{2^{-2s-n}}{s!(s+n+1)!}.
\]

The positive series gives b_0>b_1>b_2>...>0. In the three-link gauge-invariant product, B has its largest eigenvalue b_0^3 on the constant function. Its next eigenvalue is b_0^2 b_1: at least one physical eigenfunction at that energy exists, namely the class function chi_1(U_x)=Tr U_x (and analogous y,z traces); every other product mode has eigenvalue at most this one. Gauge projection does **not** remove these closed spatial-loop trace functions.

Set S=A^(1/2). Because each of the three commutator plaquettes has −1<=Tr([U_i,U_j])/2<=1, the pointwise action obeys

\[
 e^{-6\beta_s} I\preceq S^2\preceq I,\quad\text{hence}\quad
 e^{-3/8}I\preceq S^2\preceq I.
\]

The positive operators SBS and B^(1/2)S²B^(1/2) have the same nonzero eigenvalues, and the latter lies between e^-3/8 B and B in operator order. Therefore **by min–max for every physical level**,

\[
 e^{-3/8}\lambda_i(B)\le\lambda_i(T)\le\lambda_i(B).
\]

At beta_t=1 the native code re-evaluates both exact positive-series partial sums and the monotone remainder bounds and proves

\[
 \frac{24019372}{10^8}<\frac{b_1}{b_0}<
 \frac{24019373}{10^8}.
\]

Using e^-x>=1−x and e^x<=1/(1−x) for 0<=x<1, we have e^-3/8>=5/8 and e^3/8<=8/5. Division of the eigenvalue intervals gives the **full interacting, physical first-excitation spectral ratio**

\[
 \boxed{\frac3{20}<\frac{\lambda_2(T)}{\lambda_1(T)}<\frac25}.
\]

The receipts also give the stronger lower and upper rational products. For a *chosen reference temporal spacing* a_t=1, this is a positive **finite-model** mass interval

\[
 -\log(2/5)<m_{\rm first}<-\log(3/20).
\]

The code certifies the ratio using rational arithmetic; it does not numerically evaluate transcendental logs. This interval is broad. In particular, it is **not** a measured exact eigenvalue or an SU(2) continuum limit.

## 3. Full interacting operator-norm errors at ternary Peter–Weyl cutoffs

On each spatial link let P_q retain the **whole** spin-n/2 representation blocks n=0,...,q−1. On three links, use the product of such projectors restricted to the gauge-invariant space. Whole blocks commute with the full left/right SU(2) action and consequently with simultaneous conjugation. Define T_q=P_q T P_q, extended by zero on its orthogonal complement.

The per-link dimensions q(q+1)(2q+1)/6, encoded with the fixed three storage digits, are 14, 285, 6930, 180441 for q=3,9,27,81.

Crucially, **the norm errors apply to this complete interacting T**, *including the spatial Wilson plaquette factor*. They are not the one-link trace-tail figures copied from YM4-06D.

Write h=(beta_s/2)Σ_{i<j}Tr([U_i,U_j])/2, with |h|<=3/32, and expand

\[
 S=e^{-3/32}e^h,\qquad
 S_D=e^{-3/32}\sum_{j=0}^{D}\frac{h^j}{j!}.
\]

The entire Taylor remainder obeys

\[
 \|S-S_D\|\le\delta_D:=\frac{(3/32)^{D+1}}{(D+1)!}.
\]

The commutator character on each plaquette is polynomial of degree at most 2 in the quaternion coordinates of each participating link. Therefore multiplication by S_D raises each link's **twice-spin** index by at most 2D. For m=q−2D we get (I−P_q) S_D P_m=0 exactly. This is the crucial gauge-preserving polynomial-bandwidth law; it would be false if one substituted a generic nonlinear jump without proving representation support.

Let b0 be the largest single-link Wilson temporal eigenvalue. The exact positive character series gives

\[
 \frac{b_m}{b_0}\le\frac{4}{3\cdot2^m(m+1)!}.
\]

Set X=S B^(1/2). Since T=XX*, ||X||<=sqrt(b0³), we have

\[
 \|(I-P_q)X\|
 \le \sqrt{b_0^3}\left[\delta_D+\sqrt{b_m/b_0}\right],
\]
\[
 \boxed{\|T-P_qTP_q\|\le
 2b_0^3\left[\delta_D+
 \sqrt{\frac4{3\cdot2^m(m+1)!}}\right].}
\]

The native Rust gate proves all following *strict* rational upper bounds with no floating-point operation:

| q | D | m | per-link dimension | trits per link | ||T−T_q||/b0³ |
|---:|---:|---:|---:|---:|---|
| 3 | 0 | 3 | 14 | 3 | <3/8 |
| 9 | 2 | 5 | 285 | 6 | <1/60 |
| 27 | 6 | 15 | 6930 | 9 | <1/300000000 |
| 81 | 20 | 41 | 180441 | 12 | <1/10^30 |

For q81 the exact comparisons split large factorials into two u128-safe products; no overflow or floating approximation is used. Because both D=floor((q−1)/4) and m=q−2D increase along q=3^k, the q81 bound extends to **all k>=4 for this same fixed finite spatial operator**. Increasing q **does not** change spatial lattice spacing here.

By the eigenvalue stability inequality for compact self-adjoint operators, |λ_i(T)−λ_i(T_q)|<=||T−T_q||. The native gate combines this with the full physical gap bounds to certify

| q | Certified physical λ2(T_q)/λ1(T_q) interval |
|---:|---|
| 3 | No positive first-gap interval from this coarse error estimate |
| 9 | (1/8, 1/2) |
| 27 | (3/20, 2/5) |
| 81 | (3/20, 2/5) |

These are **nontrivial full-interacting-operator spectral enclosures**, even though the gigantic cut-off matrices are never materialized or diagonalized. The result is obtained by min–max, exact character coefficients, polynomial representation support, and explicit operator norm inequalities.

## 4. Fault controls and integrity

The Rust 1.81 executable and the hosted workflow test the SU(2) exact Wilson beta_t=1 link ratio, spatial quaternion noncommutation, existence of a physical spin-1/2 trace excitation, every exact cutoff rational comparison, the refinement monotonicity, and four Merkle tree fixtures. Five planted controls reject: zero spatial coupling, removal of physical trace excitation, dropped representation block, falsely improved high-spin tail, and modified HBP. The precode HBP freeze is independently checked before running.

HBI gives exact offsets into HBP. SHA hashes HBP, HBI and SH. SH identifies gauge/sector lineage and the three-symbol representation. HASH seals the source and dependencies. These provenance records are *separate* from the transfer operator. A mutated Merkle root is not a physical instantaneous signal or proof of a continuum gap.

## 5. Mathematical and computational limits

1. Spatial side is only 1×1×1. Side-one Wilson plaquettes are commutators; they do interact, but this is **not** a multi-site spatial continuum simulation. No L=2 or larger interacting SU(2) transfer eigenvalues are computed.
2. Couplings beta_s=1/16 and beta_t=1 are **held fixed**. No physical a_s→0, a_t→0 trajectory or renormalized coupling has been established.
3. Error bounds cover representation truncation of this fixed compact transfer, **not** cutoff removal uniformly over spatial volume or changing coupling.
4. The root identity is a SHA-256 data commitment; no claim of quantum superselection, physically instantaneous propagation, or nonlocal mass generation follows.
5. A Clay Yang–Mills continuum positive mass gap remains **OPEN**; physical volume growth, reconstruction, and uniform physical spectral estimates are not addressed.
6. The separate frozen 3×4 S₃ r=9 one-shot remains untouched.

**Independent mathematical review remains required** before promoting the operator-bandwidth lemma or cutoff enclosures from hosted reproducibility to externally accepted theorems. The exact action and operator used here are already derived in [Lemma 0004](../../docs/LEMMA-0004-REFLECTION-TRANSFER.md), but this new finite spectral bound is a distinct result.
