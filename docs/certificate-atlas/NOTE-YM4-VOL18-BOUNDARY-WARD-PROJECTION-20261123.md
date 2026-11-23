# YM4 VOL18 — exact SU(2) boundary gauge-orbit Ward identity and high-beta projected source response

**23 November 2026.** A native continuous-SU(2) boundary-gauge projection for the original four-dimensional Wilson conditional laws of VOL15. It applies at **every beta>=0**, including the production beta=9^12. It is a finite-volume exact gauge-invariance and reweighting theorem, with noncommuting Q8 falsifiers. It is deliberately complementary to the [strict raw-link high-beta obstruction in VOL17](NOTE-YM4-VOL17-HIGH-BETA-DOBRUSHIN-OBSTRUCTION-20261123.md), rather than a claim of mass generation.

## 1. Boundary resultant fields transform exactly as original SU(2) links

Let Q_h={-h,...,h}^4 and T be its original internal positive links, as in [VOL15](NOTE-YM4-VOL15-BOUNDARY-SUFFICIENT-STATISTIC-20261123.md). The entire original conditional Wilson law is
\[
\mu_B(dU)\propto\exp\{\beta A_{\rm int}(U)+\beta\sum_{e=(x,y)\in T}\langle U_e,B_e\rangle\}\,dH_T(U).
\tag{W1}
\]
Each boundary B_e is the sum of up to three exactly cyclically ordered original SU(2) exterior Wilson staples. Under an arbitrary choice of **cube-site** gauges g=(g_x)∈SU(2)^{Q_h}, the internal link and boundary resultant transform by the same left-right quaternion action:
\[
(g\cdot U)_{(x,y)}=g_xU_{(x,y)}g_y^{-1},
\qquad
(g\cdot B)_{(x,y)}=g_xB_{(x,y)}g_y^{-1}.
\tag{W2}
\]
B_e is a real quaternion vector, not necessarily a unit quaternion. The norm-preserving real four-dimensional representation is nevertheless valid for all B_e.

Quaternion inner products and the entire original Wilson internal plaquette action are invariant under the simultaneous transformation. Product normalized SU(2) Haar measure is invariant too, proving the **complete conditional Gibbs covariance**
\[
\boxed{\mu_{g\cdot B}=g_\#\mu_B.}
\tag{W3}
\]
Consequently for every bounded gauge-invariant interior Wilson source F,
\[
\boxed{\Phi_F(g\cdot B)=\Phi_F(B),\qquad
\Phi_F(B):=\mathbb E_{\mu_B}F.}
\tag{W4}
\]
This holds for all beta and for all original boundary fields, including boundary resultants constructed from noncommuting exterior link configurations.

## 2. Exact Ward-null susceptibility at arbitrary beta

Take pure-imaginary quaternion generators \(\xi_x\in\mathfrak{su}(2)\) at arbitrary cube sites and let \(g_x(t)=\exp(t\xi_x)\). Differentiating W2 at t=0 gives
\[
\dot B_{(x,y)}=\xi_xB_{(x,y)}-B_{(x,y)}\xi_y.
\tag{W5}
\]
For any finite-volume Wilson conditional family μ_B, the original SU(2) Gibbs response identity is
\[
\left.\frac{d}{dt}\Phi_F(B+t\dot B)\right|_{t=0}
=\beta\sum_{e}\operatorname{Cov}_{\mu_B}
\left(F,\langle U_e,\dot B_e\rangle\right).
\]
But W4 makes \(\Phi_F(g(t)\cdot B)\) constant in t. Thus the **exact full SU(2) Ward-null identity**
\[
\boxed{
\sum_{e=(x,y)\in T}
\operatorname{Cov}_{\mu_B}
\left(F,\langle U_e,\xi_xB_e-B_e\xi_y\rangle\right)=0
\qquad(\beta>0).
}
\tag{W6}
\]
This is the precise local-gauge tangent null space of the VOL15 boundary susceptibility for **every original continuous SU(2) Wilson-source observable F**. It removes gauge-orbit directions without a high-beta Dobrushin assumption. W6 is an elementary consequence of finite-volume gauge invariance; it is recorded as a necessary engineering/proof constraint, not claimed as a newly discovered lattice-gauge principle.

## 3. Gauge-aligned boundary-resultant distance and a finite beta stability theorem

Define the SU(2) boundary-gauge-orbit pseudodistance on the original finite quaternion resultant fields:
\[
\boxed{
\mathcal D_\partial(B,B')=
\inf_{g\in SU(2)^{Q_h}}
\sum_{e\in T}\|B_e-g_xB'_eg_y^{-1}\|_{\mathbb R^4}.
}
\tag{W7}
\]
It is symmetric, obeys the triangle inequality and is zero for gauge-equivalent B,B'. Compactness of the cube-site gauge group makes the infimum attained.

For any fixed g, compare the conditional Wilson densities at B and g·B'. Write \(\Delta B_e=(g\cdot B')_e-B_e\) and interpolate \(B_t=B+t\Delta B\). Let \(A_\Delta(U)=\sum_e\langle U_e,\Delta B_e\rangle\). The original compact-SU(2) Gibbs derivative gives
\[
\left\|\frac{d\mu_{B_t}}{dt}\right\|_{\rm TV}
=\frac{\beta}{2}\mathbb E_{\mu_{B_t}}
|A_\Delta-\mathbb E A_\Delta|
\le\frac{\beta}{2}\sum_e\|\Delta B_e\|.
\tag{W8}
\]
For bounded gauge-invariant F∈[0,1], W3–W4 and integration of W8 prove the **gauge-optimized arbitrary-beta source stability bound**
\[
\boxed{
|\Phi_F(B')-\Phi_F(B)|
\le\min\left\{1,\frac{\beta}{2}\mathcal D_\partial(B,B')\right\}.
}
\tag{W9}
\]
This is an exact response bound in an **unweighted boundary resultant orbit metric**. At beta=9^12 it is strong only when the aligned boundary-resultant discrepancy is on the scale 1/beta; it has no source-to-boundary decay factor. Nonetheless, it vanishes **identically** for every gauge-equivalent pair of boundary fields, even if their raw componentwise difference is large.

A precise production-beta acceptance threshold follows: if one can show
\[
\mathcal D_\partial(B,B')\le\frac1{100\beta},
\quad\beta=9^{12},
\]
then W9 proves source expectation difference <=1/200. This closeness hypothesis remains a quantitative target, **not** an established property of arbitrary or Gibbs-typical independent exteriors.

## 4. Exact noncommuting original four-dimensional controls

The [integer-only original L6/L10 verifier](../../tests/ym4_vol18_boundary_ward.py) constructs noncommuting unit Q8 original Wilson link fields on centered b=3 and b=5 cubes and their ambient periodic tori. It applies a **nonconstant cube-site SU(2) gauge**, identity outside the cube, then checks:

1. Recompute each original mixed plaquette's correct cyclic exterior SU(2) staple from the transformed full configuration. Every boundary resultant satisfies the exact **noncommutative quaternion vector covariance** B'_e=g_xB_eg_y^-1, even when B_e is a sum of nonunit quaternions.
2. Replacing every original interior link by a different quaternion configuration, and simultaneously gauge-transforming it, preserves the whole original internal plaquette Wilson action and boundary resultant pairing \(\sum_e\langle U_e,B_e\rangle\) **term by term**. Consequently the full conditional Gibbs action is exactly equivariant, independent of beta.
3. A central contractible Wilson plaquette source has exactly the same trace before and after the gauge.
4. Raw B' differs from B while the gauge-orbit discrepancy W7 is exactly zero after choosing the inverse gauge. This is the negative control for treating raw boundary-vector differences as physical response.
5. An exact integer threshold fixture checks that \(\beta \mathcal D_\partial/2\le1/200\) when \(\mathcal D_\partial\le1/(100\beta)\), and records that no such closeness has been proved for the actual physical exteriors.

The infinitesimal W6 is an **analytic continuous-SU(2) Haar/Ward theorem**; the hosted exact Q8 checks are constructive group-algebra falsifiers, not a substitute for native Lean formalization.

## 5. Actual next acceptance

VOL16 rigorously constructs unweighted original SU(2) source-to-boundary decay for beta<=1/36; VOL17 gives a strict original-model obstruction to ordinary raw-link Dobrushin contraction at every beta>=36. VOL18 now **projects out exact gauge-null boundary response directions for every beta**, including beta=9^12.

The next mathematically meaningful high-beta goal is an *averaged, gauge-projected* version of the VOL15 source-to-boundary estimate under the actual interpolating Gibbs laws, controlling **physical transverse boundary-resultant perturbations**, and proving decay with the centered buffer h−r0. It must include full continuous winding holonomies, renormalized Wilson source normalization and the correct beta(a) path. No high-beta spatial mixing or continuum mass gap has yet been established by W9.

**Statuses:** SU(2) boundary gauge covariance, Ward-null identity and aligned-source stability ANALYTIC for all beta; original L6/L10 noncommutative quaternion controls pending dedicated hosted CI; production-beta expected projected-boundary discrepancy and physical conditional covariance decay OPEN; all eleven original continuum construction obligations OPEN. [Physical acceptance issue #116](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/116).


**Hosted acceptance PASS:** [Original SU2 boundary Ward and Lie-tangent verifier run #45214603906](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/45214603906). Complete L6/L10 original Wilson cyclic mixed-plaquette/resultant transformations, noncommuting Q8 gauge/orbit positive control, arbitrary changed internal SU2 links, exact first-order Lie-algebra Ward-null boundary pairing, central Wilson-source infinitesimal trace, byte-identical normal/optimized frozen HBP SHA-256 `6ecd72172e1d018022a5f94c1f04fc7223b6c4a509ad5232ed0201e04cef065d`, no-float gate and archived hosted artifact PASS. The general continuous SU2 Ward/source stability proof W3–W9 remains analytic and has not received an independent native Lean formalization.
