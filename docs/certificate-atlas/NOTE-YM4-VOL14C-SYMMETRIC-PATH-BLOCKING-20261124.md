# VOL14-C — a symmetric nonlinear SU(2) path-average candidate

**Status:** AI-written proof candidate, independent AI review PASS (Claude, 24 November 2026); hosted replay PASS (run 45512212398); external human review OPEN. Frozen prediction: abf6adc1d494d36b26699f57d63d72511f0d71a0. Builds on VOL14-A and the supplied, locally audited VOL14-B patches (original commits 15fd98c and f902ddd). This is a constructed candidate with the desired centred linearized curl, rather than an identification with Bałaban's full nonlinear averaging operation.

## 1. A globally measurable group-valued map

Let b=2h+1 be odd, L=bM with M even and at least four. Each coarse site x is a fine site multiple of b. Write B_x=x+[-h,h]^4. For a coarse oriented link e from x to y=x+b e_mu, and every offset z in [-h,h]^4, let C_x(z) range over all distinct monotone shortest fine paths from x to x+z, uniformly weighted; use the analogous independent C_y(z). Form the SU(2) path products

$$P_{z,a,c}=U(C_x(z,a))\,U[x+z,y+z]\,U(C_y(z,c))^{-1}.$$

Let V_e be their quaternion mean, with each z assigned weight b^(-4), and the two connector choices independently uniform conditional on z. Define B(U)_e=V_e/|V_e| when V_e is nonzero, and use the original straight product U[x,y] at V_e=0. The reverse coarse link is defined by inversion. Unit quaternions identify SU(2) with the sphere in R^4; multiplication by endpoint group elements acts orthogonally. Every path transforms by the same endpoint gauge action. Both normalization and the straight fallback commute with it. This gives a Borel measurable group-valued map on the whole configuration space, equivariant under every local fine gauge transformation at the coarse endpoints.

## 2. Symmetry and open-half support

All shortest connectors and their uniform weights are invariant under coordinate permutations and sign flips (with translated endpoints). Reversing an oriented link swaps the two connector choices and reverses the middle segment; the path product becomes its inverse. Quaternion conjugation is real-linear, so the mean and normalization respect inversion; the fallback respects it too. Hence the map intertwines all coarse translations, coordinate symmetries and aligned reflections with their fine versions.

Every connector stays within its endpoint block, and the straight middle segment stays inside the union of the two adjacent endpoint blocks. At a coarse link-reflection plane, the fine plane lies between two centered blocks; the two open fine halves are unions of these blocks, including the antipodal plane. A non-crossing coarse link has both blocks in one fine open half. The complete map, including fallback, therefore depends only on fine links within that half. Crossing coarse links are excluded from the half-observable algebra.

By Lemma 0004, Theorem 4, the fine SU(2) Wilson measure is link-reflection positive. If F is a bounded real function of non-crossing coarse links in the open half, F composed with B is a bounded fine open-half observable. Reflection covariance gives

$$E_{B_*\mu}[F\vartheta F]=E_\mu[(F\circ B)\theta(F\circ B)]\ge0.$$

This closes the nonlinear link-reflection pullback for the constructed map. Site reflection positivity remains OPEN. Coarse chessboard estimates still require a suitable separate dissemination argument.

## 3. Centred linearized curl

At the identity configuration, the derivative of the quaternion normalization acts as identity on imaginary tangent vectors. The first-order path product is the signed sum of its fine Lie-algebra links. Let Q be the centred block average of b-link straight line integrals, and let c(x) be the averaged connector line integral from x to x+z with the offset weights above. The derivative of B at identity is

$$DB(I) A=QA-d_{\rm coarse}c.$$

This is the centred linear map plus a coarse gauge-gradient correction, not literally Q on all link fields. The coarse curl annihilates the correction, so its Gaussian plaquette coefficient is exactly the centred average coefficient in VOL14-A/B. The point-gauge transformation law of the nonlinear group-valued map is consistent with this correction. For b=3, the exact checker compares the weighted fine-link tables for the derivative and for the coarse curl.

## 4. Gauge-invariant small-field regularity

Use the bi-invariant SU(2) geodesic metric with distance from identity equal to the angle in [0,pi]. Suppose every fine plaquette in the union of the two endpoint blocks has angle at most delta. For any offset and connectors, compare the path product to the straight product P0=U[x,y].

First replace the endpoint connector C_y by the translate of C_x: two monotone shortest paths with the same signed displacement differ by at most sum_(i<j)|z_i z_j| <= 6h^2 adjacent perpendicular step swaps. Next commute the b middle-direction steps past the transverse connector steps; at most 3bh swaps are needed. Parallel steps commute or cancel without plaquette cost. Each perpendicular swap changes a path holonomy by a conjugated elementary plaquette or its inverse, with the same geodesic distance. The intermediate paths stay in the union of endpoint blocks, which is a rectangular box. The triangle inequality therefore gives

$$d(P_{z,a,c},P_0)\le n_b\delta,\qquad n_b=3bh+6h^2.$$

For b>1 assume delta<=1/(2 n_b). Then the Euclidean quaternion dot product with P0 is at least cos(1/2)>=7/8, using cos(t)>=1-t^2/2. Taking the weighted mean gives |V_e|>=7/8. For b=1 the map is straight. For b=3, n_b=15 and delta<=1/30 suffices. This estimate requires no gauge fixing and holds even for large pure gauges; it is a sufficient small-plaquette condition, not an optimal domain.

The map is real analytic wherever the mean is nonzero. In ambient quaternion coordinates, use conjugation for reversed fine links, a polynomial extension that equals group inversion on unit quaternions. A path has at most ell=b+8h factors, each a unit quaternion at the base point. For perturbations in the sup of the Euclidean link norms, the first derivative of its product has norm at most ell and the second at most ell(ell-1). The weighted mean obeys the same bounds, counting repeated link occurrences separately.

For normalization N(v)=v/|v| at r=|v|>=7/8, the operator norm of DN is <=1/r<=2 and of D^2N is <=6/r^2<=8 by direct differentiation. Composition gives

$$\|DB\|\le2\ell,\qquad \|D^2B\|\le8\ell^2+2\ell(\ell-1)\le10\ell^2.$$

For b=3, ell=11, giving 22 and 1210. These are single-map ambient derivative bounds evaluated at group fields in the stated domain. In exponential Lie-algebra coordinates X -> U exp(X), the second derivative has the additional contribution from the second derivative of the exponential at zero, bounded by 22 in the sup norm. Thus for b=3 the first and second bounds in those coordinates are 22 and 1232, respectively. VOL14-D uses Lie-algebra fluctuation coordinates. They do not supply an iterated RG remainder estimate; uniform bounds along a specified perturbation segment require staying within a suitable nonzero-mean neighborhood.

## 4A. Exact scale-zero calibration with VOL12

Keep the floor 7/8 and set beta=9^7=4782969, epsilon=1/500. The VOL12 plaquette defect threshold is epsilon/4=1/2000. The alternating cosine series gives 1-cos(1/30) >= 1/(2*30^2)-1/(24*30^4) = 10799/19440000 > 1/2000. Since 1-cos(theta) increases on [0,pi], a nondefective plaquette has angle less than 1/30.

With A_beta=1536 exp(3/4) beta^(3/2), VOL12 gives rho_star=6 A_beta exp(-beta epsilon/64) and rho_D=A_beta^4 exp(-beta epsilon/16). Using exp(3/4)<3, exp(3)<27 and exp(-x)<=2^(-floor(x)), the exact integer witnesses are

    6*1536*3^22 < 2^49, floor(9^7/32000)=149,
    1536^4*27*3^84 < 2^181, floor(9^7/8000)=597.

Therefore rho_star < 2^-100 and rho_D < 2^-416. On an even periodic original Wilson lattice compatible with b=3, the union of the two endpoint blocks has 162 vertices and at most 972 internal plaquettes (six positive plaquette types per base). By the direct VOL12 plaquette estimate and union bound, failure of the sufficient local small-field condition has probability less than 972*2^-416 < 2^-406. This is a local periodic-equilibrium bound for a specified coarse link, not a uniform probability that the whole volume is small-field. Absence of bad stars alone is insufficient for the local small-plaquette hypothesis; use the original plaquette indicators directly. Transformed-measure and arbitrary-exterior estimates remain separate OPEN gates.

## 5. Evidence and next gates

At b=3 the 81 offsets contribute sum_(k=0)^4 binom(4,k)2^k(k!)^2=10473 full paths. Each connector multiplicity divides 24, so all path weights have common denominator 81*24^2=46656. The checker compares the entire weighted family under signed-coordinate generators and reversal, checks path support and the linearized curl, and verifies the integer bounds and a corner-offset reflection negative control.

[Prediction](PREDICT-YM4-VOL14C-SYMMETRIC-PATH-BLOCKING-20261124.hbp) · [checker](../../tests/ym4_su2_vol14c_symmetric_path_blocking.py) · [expected replay](YM4-VOL14C-SYMMETRIC-PATH-BLOCKING-20261124.hbp).

Remaining targets: prove gauge-fixed constrained propagator locality (VOL14-D), compare the candidate with the precise Bałaban nonlinear operation, study the effective action and nonlinear coupling recursion, and propagate large-field control under the transformed measure. All physical continuum obligations remain OPEN. The checker validates finite combinatorial and arithmetic identities; the group and analytic statements are established by the written arguments, subject to independent review.
