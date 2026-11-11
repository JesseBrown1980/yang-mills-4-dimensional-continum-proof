# YM4-06F — multisite interacting SU(2) Wilson transfer

**Date: 2026-11-11.** Prediction-first, fixed-volume exact-integer research certificate. The full SU(2) gauge-invariant transfer operator is defined mathematically; **its spectrum is bounded analytically, not diagonalized numerically**. This is not a continuum Yang–Mills mass-gap proof.

Frozen prediction: docs/PREDICTION-YM4-06F-MULTISITE-WILSON-20261111.hbp, initial commit 955a997687d6220fa2ce60c36f97419934b4e06e, before any source code. The Rust 1.81 hosted verifier checks the unchanged prediction and all exact rational and finite-geometry controls.

## 1. Physical finite operator

Consider periodic spatial (Z/2)^3: 8 vertices, 24 oriented positive links, and 24 plaquettes. Every face uses four **different** link variables, and every link belongs to four faces. The code explicitly establishes these incidence facts, all 12 distinct two-link winding loops, nonconstant spatial plaquette values, and character invariance under independently assigned SU(2) quaternion gauge elements at the 8 vertices. The quaternion matrices are **finite geometry test witnesses only**, not an SU(2) quadrature.

For normalized Haar SU(2), Wilson plaquette weight w_beta(g)=exp[-beta(1−Tr(g)/2)], beta_s=1/128, beta_t=1, let

\[
 A(U)=\prod_{p=1}^{24}w_{\beta_s}(U_p),
 \quad (Bf)(U)=\int \prod_{\ell=1}^{24}w_{\beta_t}(U_\ell V_\ell^{-1})f(V)\,dV,
 \quad T=(A^{1/2}BP_GA^{1/2})\big|_{\mathcal H_G}.
\]

Here P_G projects under **all eight independent vertex gauge transformations** and H_G=L²(SU(2)^24)^{SU(2)^8}. The spatial multiplication A couples four-link plaquettes, and T is compact, self-adjoint and positive. No full Hamiltonian matrix is stored.

## 2. The two-link first excited state

The eigenvalue of the single-link SU(2) Wilson convolution on twice-spin n is b_n=e^(−1) ell_n(1), where

\[
 \ell_n(1)=\sum_{s=0}^{\infty}
 \frac{2^{-(2s+n)}}{s!(s+n+1)!}.
\]

Every coefficient is positive and b_(n+1)<b_n: termwise, the ratio is 1/[2(s+n+2)]<1. The independently validated YM4-06D rational series control gives

\[
 24019372/10^8 < \rho=b_1/b_0 < 24019373/10^8.
\]

A nontrivial irreducible representation on a **single open edge** cannot give a singlet under independent gauge transformations at its two endpoints. Therefore a nontrivial gauge-invariant spin-network support has at least two incident supported links at every active vertex and contains a cycle. The spatial (Z/2)^3 multigraph has girth two: a two-link Polyakov winding loop along each of the 12 axis-pairs, with fundamental trace as a gauge-invariant eigenfunction. It follows that the first two distinct physical B levels, including multiplicity ordering, are

\[
 \lambda_1(B)=b_0^{24},\qquad
 \lambda_2(B)=b_0^{22}b_1^2,\qquad
 \lambda_2(B)/\lambda_1(B)=\rho^2.
\]

The local geometry, gauge-invariance witnesses and exact inequalities are checked in Rust. The general spin-network selection theorem is an analytic argument that still merits independent mathematical review.

Each of 24 spatial plaquettes contributes Wilson action between 0 and 2, so e^(−3/8)I<=A<=I. Conjugation of the compact positive B and the min–max principle give e^(−3/8) lambda_i(B)<=lambda_i(T)<=lambda_i(B). Since 5/8<=e^(−3/8) and e^(3/8)<=8/5, exact integer comparisons imply

\[
 \boxed{\frac1{28}<\frac{\lambda_2(T)}{\lambda_1(T)}<\frac1{10}}.
\]

At an uncalibrated **reference** temporal spacing a_t=1, this implies log(10)<m_first<log(28). It does not determine the physical temporal spacing or a continuum mass.

## 3. Complete interacting-operator cutoff control

Let P_q retain complete SU(2) Peter–Weyl irrep blocks of twice-spin n<q on **each** link, restricted to the gauge-invariant subspace. The projector commutes with the full vertex gauge group. Its per-link dimension is q(q+1)(2q+1)/6, representable in 3, 6, 9 and 12 trits at q=3, 9, 27 and 81.

Write S=A^(1/2)=e^(−3/32)e^h with h=(1/256) sum_p Tr(U_p)/2 and |h|<=3/32. For a Taylor cutoff D, let S_D=e^(−3/32)sum_(j=0)^D h^j/j!. Its remainder satisfies

\[
 \|S-S_D\|\le\delta_D=(3/32)^{D+1}/(D+1)!.
\]

**New multisite algebra:** each plaquette contains a link **at most once**; the plaquette trace is degree one in that link's fundamental matrix coordinates. A product of D plaquettes can therefore raise its twice-spin by at most D, not 2D as the earlier side-one commutator-lattice bound conservatively allowed. With m=q−D,

\[
 (I-P_q)S_D P_m=0.
\]

For the exact SU(2) Wilson temporal spectrum, b_m/b_0 <= 4/[3*2^m*(m+1)!]. The factorization T=XX* with X=S B^(1/2) then proves the **full interacting** operator-norm inequality

\[
 \boxed{
 \|T-P_qTP_q\|/b_0^{24}
 \le2\left[
 \delta_D+\sqrt{4/[3\cdot2^m(m+1)!]}
 \right].
 }
\]

The native program proves the following strict, frozen rational bounds:

| q | D | m | Link dimension | Trits | Full-T relative norm error |
|---:|---:|---:|---:|---:|---|
| 3 | 0 | 3 | 14 | 3 | <3/8 |
| 9 | 2 | 7 | 285 | 6 | <1/700 |
| 27 | 6 | 21 | 6930 | 9 | <1/(30×10^9) |
| 81 | 20 | 61 | 180441 | 12 | <10^(−30) |

The q9 gate uses delta_2=9/65536<1/7000 and sqrt(b7/b0)<1/1900. The q27 gate uses delta_6<1/(70×10^9) and sqrt(b21/b0)<1/(40×10^12). At q81 a factorized factorial/tail comparison bounds delta_20 and the higher-spin tail separately, without evaluating a factorial that exceeds u128.

Weyl's bound for compact self-adjoint operators carries these full-T errors to the projected physical spectral ratios:

| q | Physical lambda2(T_q)/lambda1(T_q) |
|---:|---|
| 3 | NOT ENCLOSED by this coarse error |
| 9 | between 1/30 and 1/10 |
| 27, 81 | between 1/28 and 1/10 |

The q81 interval follows by monotonic tightening relative to q27; no arithmetic extrapolation of the q27 actual matrix is implied.

## 4. Cryptographic certificates and falsifiers

The Rust 1.81 native hosted gate enforces strict Clippy, exact integer comparisons, all eight-vertex geometry controls and direct representation-cutoff dimension tests. It rejects planted controls removing the spatial interaction, treating an open fundamental link as physical, deleting an irrep block, claiming an unjustifiably tight cutoff tail, or tampering with the final HBP. HBI stores ordered byte offsets, SHA hashes HBP/HBI/SH, SH identifies the three-phase provenance, and HASH commits to the resulting record. A one-trit mutation changes the tested Merkle root but leaves a distant physical trit unchanged.

The six output files (five ledgers plus SHA256SUMS) are filed under evidence/ and required to reproduce **byte for byte** from the source and frozen prediction. No work on the separate r=9 blind job is included.

## 5. Essential limits and next falsifier

This verifies spectral enclosures for the **specified finite** 2×2×2 Wilson transfer at the relatively small fixed coupling beta_s=1/128. It does not diagonalize the 24-link Hilbert space, prove a **volume-uniform** gap, determine a physical a_t or running coupling, reconstruct an infinite-volume continuum theory, or demonstrate instantaneous propagation from a SHA global root.

The next decisive experiment is to extend the graph-dependent loop selection and transfer estimates to L=3 and beyond **without allowing the crude e^(2 beta_s times number of plaquettes) factor to destroy the physical lower bound**, followed by controlled beta_s, beta_t, a_s, a_t scale matching. Independent review of the spin-network selection and Taylor irrep-bandwidth lemma is required before any external theorem claim.
