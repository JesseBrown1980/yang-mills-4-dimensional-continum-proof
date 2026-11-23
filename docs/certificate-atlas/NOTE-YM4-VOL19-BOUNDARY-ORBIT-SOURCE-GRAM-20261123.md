# YM4 VOL19 — complete boundary-resultant orbit coordinates and source-conditioned Ward Gram

**Research draft, 23 November 2026.** Independent mathematical continuation of VOL15–VOL18, for the original continuous SU(2) Wilson model on a finite four-dimensional cube. This note establishes exact finite-dimensional reductions at every finite beta. It does not establish high-beta spatial mixing or a continuum mass gap.

## 1. Complete gauge-orbit coordinates for arbitrary boundary resultants

Let `J` be the original boundary-affected internal-link graph of VOL15. Each oriented edge `e=(x,y)` has a quaternion resultant `B_e` (a sum of at most three original staples), transforming by `B_e -> g_x B_e g_y^{-1}`. Define `r_e = ||B_e||`. On the nonzero-edge graph `J_+={e:r_e>0}`, write `q_e=B_e/r_e` in SU(2); zero edges remain zero. Pick a rooted spanning forest, one tree in each connected component of `J_+`. Let `P_x` be the ordered product of the `q_e` along the tree path from the component root to `x`, using inverse factors when traversing against the orientation, with `P_root=1`. On each non-tree edge, define the rooted chord holonomy

`H_e = P_x q_e P_y^{-1}`.

**Exact classification.** Two resultant fields `B,B'` lie on the same cube-site SU(2) gauge orbit if and only if (i) all edge radii `r_e` agree, so their zero supports agree, and (ii) for each connected component there exists *one common* `c` in SU(2) with `H'_e=c H_e c^{-1}` for **all** its non-tree edges. Components can use independent `c`. Proof: any site gauge transforms `P_x` to `g_root P_x g_x^{-1}` and each `H_e` by common root conjugation. Conversely, with `c` fixed, `g_x=(P'_x)^{-1} c P_x` aligns every tree edge and chord, and hence every nonzero resultant. Isolated vertices have free gauges.

Thus every gauge-invariant interior Wilson expectation `Phi_F(B)=E_{mu_B}[F]` depends on boundary-resultant radii and the **simultaneous** rooted-cycle conjugacy classes. No unit-resultant or commuting-staple approximation is involved. Individual cycle traces alone are insufficient: the pairs `(i,i)` and `(i,-i)` have the same individual real traces, but `Re(H_1^{-1}H_2)` is respectively `+1` and `-1`; they cannot be simultaneously conjugate. This safeguard retains noncommutative relative-cycle information. These are cycle coordinates on a finite cube, distinct from full periodic winding-sector data.

## 2. An exactly Ward-null *source-conditioned* covariance kernel

At any boundary field `B`, including a linear interpolation of original resultant fields, let `mu_B` denote the positive original continuous-SU(2) conditional Wilson law from VOL15. Let `X=(U_e)_{e in J}` be the real `4|J|` vector of original boundary-affected interior links. Let `A_S` be the sigma-algebra of gauge-invariant Wilson observables supported on a fixed interior source region `S`. Define

`Y_B=E_{mu_B}[X | A_S]`,

`K_{B,S}=Cov_{mu_B}(Y_B,Y_B)` (a positive-semidefinite real matrix).

For the genuine original Wilson source `F in [0,1]`, measurable with respect to `A_S`, and any real boundary-resultant perturbation `D`, conditional expectation and Cauchy–Schwarz give

`Cov_B(F, <X,D>) = Cov_B(F, <Y_B,D>)`,

`|Cov_B(F, <X,D>)| <= (1/2) sqrt(D^T K_{B,S} D)`.

More precisely, `D^T K_{B,S} D` equals the square of the optimal covariance with `<X,D>` over all centered, variance-one, square-integrable `A_S`-measurable functions. This follows from orthogonal projection in L2(mu_B); it is an exact observable-algebra sensitivity, not a chosen spatial weighting.

For any cube-site Lie algebra field `xi`, define the boundary gauge tangent

`(J_B xi)_e = xi_x B_e - B_e xi_y`.

For beta>0, VOL18's Ward identity applies to **every** bounded `A_S`-measurable gauge-invariant function. At beta=0, the product Haar law has the same null consequence directly: an independent central site gauge `-I` at one endpoint reverses each selected link while fixing every gauge-invariant source, so its source-conditioned link expectation vanishes. Consequently, for all beta>=0, the conditional expectation of `<X,J_B xi>` given `A_S` is constant almost surely. Equivalently,

`K_{B,S} J_B=0`.

This is an exact null-space theorem at **every beta** for all original continuous SU(2) interpolating conditional laws. In contrast to the unconditioned boundary-link covariance, `K_{B,S}` explicitly retains the source region and can be tested for source-to-boundary decay. It obeys `0 <= K_{B,S} <= Cov_B(X,X)` in positive-semidefinite order.

## 3. Gauge-invariant finite-difference response bound

Let `B,B'` be two original Wilson boundary resultant fields. For a cube-site gauge `g`, put `D_g=g.B'-B` and `B_{t,g}=B+t D_g` for `t in [0,1]`. The exact VOL15 response derivative, gauge covariance of VOL18, and the source-conditioned bound above give

`|Phi_F(B')-Phi_F(B)| <= (beta/2) inf_g integral_0^1 sqrt(D_g^T K_{B_{t,g},S} D_g) dt`.   **(V19)**

The integral is finite and well defined in each finite cube. Every comparison uses the original continuous SU(2) Haar Gibbs law, even when an intermediate linear resultant is not realized by a single physical exterior configuration. For gauge-equivalent `B,B'`, some `g` makes `D_g=0` and the right side vanishes identically. There is no assumption that an independently sampled pair of Gibbs exteriors is gauge-equivalent.

**A sufficient acceptance target for issue #116:** for a source centered at buffer `d=h-r0`, prove with suitable physical constants and beta(a) that the expected or uniform (as required by VOL07) right-hand integral satisfies

`inf_g integral_0^1 sqrt(D_g^T K_{B_{t,g},S} D_g) dt <= (2 A / beta) exp(-m d)`.

Then the physical source response is at most `A exp(-m d)` without inserting a distance weight into its definition. The uniformity in lattice spacing, all Gauss sectors, physical source normalization, and continuous winding-holonomy transfer remain distinct proof obligations. **No such decay bound is proved here.**

The kernel can be evaluated as the variance of the conditional expected *single boundary score* `E[<X,D_g> | A_S]`; one need not materialize the full `4|J|`-square matrix. This is a source-specific, matrix-free route to the next numerical or analytic acceptance test.

## 4. Independently checked exact algebraic controls and limitations

The strict integer/Fraction checker [tests/ym4_vol19_orbit_source_gram.py](../../tests/ym4_vol19_orbit_source_gram.py) verifies quaternion multiplication, noncommutative two-square-cycle common-root conjugacy, full gauge reconstruction with nonunit resultants, and a red control where individual cycle traces agree but the simultaneous conjugacy class differs. It also tests the source-conditioned covariance projection on an explicitly **abstract** four-outcome rational model: the raw score variance is `53`, while the source-projected variance is `4`; the tangent-score variance projects to zero and source Cauchy–Schwarz is attained exactly. This rational example checks the algebra and is not a Wilson Gibbs or continuous Haar integration.

The exact expected-output [HBP](YM4-VOL19-ORBIT-SOURCE-GRAM-20261123.hbp) and [hosted-workflow definition](../../.github/workflows/ym4-vol19-orbit-source-gram.yml) are committed. The dedicated hosted acceptance result is pending.

**Review status:** finite graph-orbit classification, continuous-Haar Gibbs response identity, L2 projection and Ward-null Gram theorem have analytic proofs above; exact toy controls pass locally. No Lean kernel formalization or hosted run is claimed. High-beta spatial decay of the source-conditioned Gram, all-sector transport, and the eleven continuum construction gates remain OPEN. Keep in draft PR #113's candidate atlas map pending full audit and hosted acceptance; production 3D viewer and `main` should remain unchanged.