# YM4-06D: exact finite-Wilson vacuum-preserving spatial blocking isometry

**Date:** 2026-11-11. **Status:** DERIVED actual finite 3+1D continuous-SU(2) Wilson Hilbert-space construction, subject to independent mathematical review. **Not** a derived interscale spectral-gap bound, a local coarse Wilson action, a weak-coupling renormalization theorem, or the physical continuum mass gap.

This note sharpens [YM4-06C](NOTE-YM4-06C-FULL-SPECTRUM-SCHUR-20261111.md) by actually constructing its vacuum-preserving isometry **for the canonically induced coarse ground-state measure**. It does not claim that this induced measure equals the Perron measure of a separately prescribed Wilson coarse transfer.

**Prediction-first record:** twelve H-rows in `docs/PREDICTION-YM4-06D-WILSON-VACUUM-ISOMETRY-20261111.hbp` frozen at `dc9a7ff89c6ae2fd7a70e50a654f36439a779127` before the new code and before this proof addendum.

## 1. Genuine 4D Wilson input, one 3D spatial slice

Fix the **actual continuous SU(2)** Wilson transfer `T_f` with strictly positive coupling, the conventional positive temporal transfer, and a finite periodic three-dimensional spatial slice with fine side `L=3L_c>=6` in each direction. From [YM4-02c](LEMMA-0004-REFLECTION-TRANSFER.md), `T_f` is a compact positive self-adjoint operator with a **simple, strictly positive continuous gauge-invariant Perron eigenfunction** `Omega_f`, normalized by `integral Omega_f^2 dH_f=1`. Here `dH_f` denotes product Haar over the finitely many spatial links. Let `S_f=T_f/lambda_0(T_f)`.

The Doob-transformed physical transfer on `L^2(mu_f)` is

[
d\mu_f(U)=\Omega_f(U)^2,dH_f(U),\qquad
(P_f h)(U)=\frac{1}{\lambda_0\Omega_f(U)}
T_f(\Omega_f h)(U).
]

Then `P_f` is self-adjoint, a positive contraction, and a positivity-preserving **reversible Markov operator** with stationary measure `mu_f` and vacuum `1`. The gauge-invariant physical Hilbert space is its gauge-invariant subspace. All statements follow from the positive Wilson kernel, the Perron eigenvalue and the unitary multiplication by `Omega_f`.

## 2. Exact factor-three spatial Haar disintegration

Define the ordinary gauge-equivariant ordered line map on spatial links,

[
(B_3U)_\nu(x)
=U_\nu(3x),U_\nu(3x+e_\nu),U_\nu(3x+2e_\nu).
]

Distinct coarse links use disjoint fine oriented links. As in the already derived YM4-03 Haar disintegration (its general factor-b formula applies at `b=3`), under product fine Haar the image of `B_3` is exactly **product coarse Haar** `dH_c`. Given `B_3U=V`, two links of each three-link line are free Haar and the last is determined by their ordered product and V; other links remain independent Haar. Denote the resulting conditional fiber measure by `H_f(dU|V)`.

Define the **exact pushforward of the Wilson ground-state measure**

[
d\nu_c(V)=(B_3)_*d\mu_f(V)=\rho(V)dH_c(V),qquad
\rho(V)=\int_{B_3U=V}\Omega_f(U)^2,dH_f(U|V).
\tag{D1}
]

The bounded positive continuous `Omega_f`, compact fibers, and the explicit Haar disintegration show that `rho` is **strictly positive and continuous**. Product Haar plus gauge covariance and gauge invariance of `Omega_f` prove `rho(V^g)=rho(V)`. Moreover `integral rho,dH_c=1`.

**This is the required actual finite Wilson ground-state pushforward, not an assumed equality with the ground state of an independently chosen coarse Wilson action.**

## 3. Canonical vacuum-preserving gauge-compatible isometry

In Doob Hilbert spaces define

[
J:L^2(d\nu_c)\to L^2(d\mu_f),\qquad
(Jh)(U)=h(B_3U).
\tag{D2}
]

For all square-integrable gauge-invariant h and g,

[
\langle Jh,Jg\rangle_{\mu_f}
=\int\overline{h(B_3U)}g(B_3U)d\mu_f
=\int\overline{h(V)}g(V)d\nu_c
=\langle h,g\rangle_{\nu_c}.
\tag{D3}
]

Thus `J*J=I` and **`J1=1`**, while gauge covariance of B ensures gauge-invariant coarse functions pull back to gauge-invariant fine functions. This is a true vacuum-preserving isometry on the **full induced coarse physical Hilbert space** at each finite Wilson volume. No new asymptotic estimate is required for its existence.

Equivalently, in the original Haar Hilbert spaces, define

[
(J_{\rm raw}\psi)(U)=
\frac{\Omega_f(U)}{\sqrt{\rho(B_3U)}}\psi(B_3U).
\tag{D4}
]

For the induced coarse vacuum `Omega_c^ind(V)=sqrt(rho(V))`, one has
`J_raw Omega_c^ind=Omega_f`, and `J_raw*J_raw=I`. Formula (D4) is explicit but evaluating its operator estimates for general SU(2) at small spacing requires control of `Omega_f` and `rho`—these remain substantial mathematical obligations.

## 4. The induced three-tick transfer and its exact memory barrier

For the **real Wilson** `P_f`, define on the induced coarse space

[
P_c^{\mathrm{ind},3}=J^*P_f^3J.
\tag{D5}
]

This is a positive self-adjoint Markov contraction with vacuum 1 (or vacuum `sqrt(rho)` in raw Haar coordinates). Its coarse observables have exactly the right **single three-tick** time correlation:

[
\langle h,P_c^{\mathrm{ind},3}g\rangle_{\nu_c}
=\langle h\circ B_3,P_f^3(g\circ B_3)\rangle_{\mu_f}.
\tag{D6}
]

It generally does **not** reproduce correlations after two or more coarse ticks by simply taking powers of (D5). With `E=JJ*`, for **any positive integer n**, the exact identity

[
\boxed{
J^*P_f^{2n}J-(J^*P_f^nJ)^2
=
\bigl[(I-E)P_f^nJ\bigr]^*
\bigl[(I-E)P_f^nJ\bigr]\ge0.
}
\tag{D7}
]

follows by inserting `I=E+(I-E)` between the two powers. In particular at `n=3`, the error in matching **six fine ticks** to two coarse steps is the positive memory-Gram operator of leaked modes. Exact single-step pushed-forward Wilson correlations do not justify `(J*P_f^3J)^2=J*P_f^6J` unless that leakage is zero. No independence assumption enters.

If `r_f=\|P_f|_{1^\perp}\|` and `r_c^ind=\|P_c^ind,3|_{1^\perp}\|`, then

[
r_c^{\mathrm{ind}}\le r_f^3.
\tag{D8}
]

The inequality is **opposite** to the upper bound on `r_f` required for a physical first-gap lower bound. The full-Schur dark-mode and leakage norms in YM4-06C are therefore essential, and not optional refinements.

## 5. Exact finite-group computational stress control and its limits

The checker `tests/test_ym4_06d_wilson_vacuum_isometry.py` replays a **finite Q8 quaternion** three-link fiber disintegration as a *finite algebraic control of the general Haar mechanism*: all `8^3=512` source link triples map onto each coarse group element with 64 preimages, and an explicitly nonconstant **positive** test weight gives exact normalized pushforward densities, weighted norm equality and a vacuum identity in square-root-free rational form. It also verifies ordered product gauge covariance under multiple independent endpoint and internal gauge transformations. Three wrong-product/weight/ground-measure cases are rejected.

The Q8 weight is a **synthetic finite control**, not the continuous SU(2) Wilson vacuum probability and not evidence of a small-spacing spectral gap. The actual continuous-SU(2) statements in (D1)-(D8) are proven by the preceding Haar disintegration and Hilbert-space algebra, not by extrapolation from Q8.

## 6. Remaining mathematical target (unchanged, now narrower)

For the **induced** coarse `P_c^ind,3` we now have a canonical isometry, exact transfer bilinear forms, a positive compression-memory identity and full-spectrum reverse inequality. We do **not** have any inequality forcing `r_f<= (r_c^ind)^(1/3) e^{b}`.

To establish the wanted Law 70 inequality, one must independently prove:

1. The relation between `P_c^ind,3` and a physically justified renormalized coarse **local Wilson-network** transfer with the same effective ground-state measure, temporal normalization, and reflection positivity.
2. Quantitative retained-spectrum error `alpha_k`, off-diagonal memory leakage `zeta_k`, and **the supremum of the discarded physical spectrum** `rho_k` in YM4-06C, uniform over spatial volume and all successive spacing scales.
3. The exact Schur threshold `tau_k` and its strict summable physical error budget, for every k on the actual nonperturbative weak-coupling trajectory.
4. A nontrivial continuum OS reconstruction and independently verified physical spectrum.

**This addendum closes only existence of a canonical finite-volume vacuum-preserving block isometry for the *induced* measure. The hard spectral comparison remains OPEN.** No finite-universe repository changes or r9 launch.
