# VOL14-D3A — covariant crossing-face coordinates at the VOL14-C tolerance

**Status:** author-side exact suffix counts and analytic proof; hosted replay and independent review pending. Scope: b=3, every relevant fine plaquette angle at most delta=1/30, original VOL14-C map and Lie-algebra right exponential fluctuation coordinates. This is a uniform right-inverse and coordinate-section result, not a background Hessian coercivity theorem.

## 1. Why change coordinates

Independent review 09 validates the background derivative and Wilson Hessian numerically on a 4^4 coarse torus. Its fixed untransported face-zero-mean space is not gauge covariant: right fluctuation at a positive link transforms by the adjoint at its target site. Its almost identical observed eigenvalues under gauge changes do not imply exact spectral invariance in those fixed coordinates. Instead use parallel-transported face means. This construction does not require a global Landau-gauge existence theorem or small global holonomies.

Let e=(x,y=x+3 e_mu) be a positive coarse link. For each of its 27 crossing links ell let v be the fine target vertex in B_y. Let s0(v) be the holonomy of the inverse of the coordinate-ordered shortest tree path from y to v (thus v to y). Define the lift R_U by

    (R_U Y)_ell = Ad(s0(v)) Y_e

on the crossing links, zero on every internal link. These are right exponential link coordinates. Since each adjoint is orthogonal and faces are disjoint, R_U^* R_U=27 I. The tree-zero space intersected with ker R_U^* is Z_U, the transported face-zero-mean space, of dimension 240 per block per colour (720 real coordinates). It is gauge covariant by conjugation at fine endpoints. For an explicit block-local isometric identification with the identity coordinate space, use target-centre tree parallel transport for every fine link, including internal links; for crossing links use the target block. This identification is an isometry block by block when coordinates are grouped by positive anchors, and depends on the background.

## 2. Exact suffix counts

Each path in the VOL14-C average crosses the interface once. Write P for its holonomy and s for the suffix from the fine target vertex v of that crossing to y. In target-centred coordinates v_mu=-1 and v_i=z_i otherwise, where z is the uniformly sampled offset in {-1,0,1}^4. If p is the uniformly sampled target connector word from y to y+z, the suffix word is (positive mu) repeated 1+z_mu times followed by reverse(p) with signs reversed.

When z_mu=1, move the negative mu letter left until adjacent to the second positive mu letter and cancel the pair. The remaining letters are distinct axes. Sort into decreasing axis order to recover the canonical inverse tree word. The checker explicitly verifies every swapped path remains inside B_y and ends at y. A perpendicular swap inserts one conjugate elementary plaquette holonomy; an inverse cancellation is exact. Therefore the bi-invariant SU(2) geodesic distance d(s,s0) is bounded by n delta, with n the swap count. The uniform offset and uniform conditional connector weights have denominator 81*24=1944. The source connector distribution sums to one and has no effect on the suffix count.

| Axis | Maximum swaps | Weighted mean swaps |
|---|---:|---:|
| 0 | 9 | 8/3 |
| 1 | 8 | 20/9 |
| 2 | 7 | 16/9 |
| 3 | 6 | 4/3 |

All counts are integer enumeration, not a bound inferred from sampled gauge fields.

## 3. Uniform constraint derivative inverse

For an input R_U Y the path derivative at its sole crossing is

    delta P = P Ad(s^(-1) s0) Y_e.

For unit quaternions the adjoint acts by rotation through twice the geodesic angle, so ||Ad(s^(-1)s0)-I|| <= 2 d(s,s0) <= 2 n delta. Average over all paths. If V is the unnormalized quaternion mean, the error from V Y_e is at most 2 delta E[n] ||Y_e||. Normalizing the mean, the output right Lie derivative is Im(B^(-1) delta V)/||V||, B=V/||V||. The exact VY term gives Y. The imaginary projection is contractive. VOL14-C proves ||V||>=7/8 on this plaquette domain. Thus, on each face,

    ||L_U R_U - I|| <= (8/7) * 2 delta * (8/3)
                      = 64/315 < 1,
    ||(L_U R_U)^(-1)|| <= 315/251 < 4/3.

L_U R_U is block diagonal over coarse links: a path uses no other crossing interface, and the lift vanishes on all internal links. Hence the bounds hold simultaneously on every compatible periodic volume. Define J_U=R_U(L_U R_U)^(-1) and T_U=I-J_U L_U on Z_U. Then L_U J_U=I, L_U T_U=0, and the correction is in ran R_U, orthogonal to Z_U. Consequently

    ||T_U z||^2 = ||z||^2 + ||J_U L_U z||^2 >= ||z||^2.

The map is bijective from Z_U onto the tree-zero constrained tangent space: for any such A subtract its orthogonal projection onto ran R_U to obtain z, then solve the constraint using the invertible L_U R_U. The lift, inverse and coordinate changes are gauge covariant. The root-zero infinitesimal fine gauge subgroup can be fixed by the tree equations for any background: recursively solve the transported difference equation on the rooted tree. Coarse stabilizer directions, if present, still require separate treatment. This is a statement about the tangent section at a specified background, not a global nonlinear parametrization of the constraint manifold.

## 4. Curvature and the constrained-minimizer qualification

Review 09 measures H_U=T_U^* W_U T_U with W_U the ambient exponential-coordinate Wilson Hessian. At a constrained stationary point of the nonlinear blocking map the actual restricted second variation generally includes the Lagrange-multiplier term. Write a local constraint chart F(U)=log(B(U_*)^(-1) B(U)), and stationarity dS=lambda dF. Along a curve satisfying F=0, the intrinsic constrained Hessian on its tangent is

    H_phys = T_U^* [W_U - sum_e,a lambda_(e,a) D^2 F_(e,a)] T_U.

The multiplier term vanishes if the ambient first derivative vanishes, but that cannot be assumed at a constrained minimizer. Review 09's samples are not constrained minimizers. Both the curvature contribution in W_U and this constraint-curvature term need relative bounds.

For each plaquette, let a_i be its four signed, parallel-transported Lie insertions in the common plaquette base frame, and let U_p=cos(theta)+n sin(theta), with unit imaginary n. Moving insertions to the left gives the product exp(t a_1)...exp(t a_4) U_p. Quaternion multiplication gives the exact Hessian form

    cos(theta) |sum_i a_i|^2 + 2 sin(theta) n dot sum_(i<j) (a_i cross a_j).

The signed area has the identity

    sum_(i<j) a_i cross a_j
      = (a_1+a_2) cross (a_2+a_3) + (sum_i a_i) cross a_4.

The first term can survive zero total curl. A per-plaquette bound solely by |sum_i a_i| times the link norm is therefore invalid without additional conditions. Next reconstruct the two partial sums from local constrained curvature coordinates and retain their signed antisymmetric coefficients before any envelope. This is a route to a relative bound that avoids applying the global 105 to every link. The exact local form and its background perturbations remain to be estimated.

## 5. Weighted comparison and remaining gates

Use a single definition: E_W=H_0^(-1/2)(Re(W H_U W^(-1))-H_0)H_0^(-1/2). If E_W>=-alpha I, alpha<1, its inverse bound uses 105/(1-alpha). If instead alpha bounds only the weighted background difference, add the independently certified identity weighting cost beta_0. Do not count beta_0 twice. D2 certifies beta_0<=23/44 by its absolute envelope and the 105 floor; the reported 0.0096 is exploratory. The new background lift also needs its own weighted coordinate norm bound before transferring a covariance prefactor.

The 64/315 result is at the original VOL14-C plaquette tolerance and is uniform in volume. It supplies a well-conditioned constraint right inverse independent of global gauge choices. Curvature relative-form estimates, background-dependent Hessian positivity, multiplier control, coarse stabilizer handling, background locality, induced action and continuum construction remain OPEN.

[Sealed expectations](EXPECTED-YM4-VOL14D3A-COVARIANT-FACE-20261126.hbp) · [Integer checker](../../tests/ym4_vol14d3a_covariant_face.py) · [Expected replay](YM4-VOL14D3A-COVARIANT-FACE-20261126.hbp).
