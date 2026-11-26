# VOL14-D3C — paired face cancellation and the stationary curvature source

**Status:** author-side analytic derivation and integer face enumeration; independent review and hosted replay pending. Stacked on the independent review 10 (#130, 087f592). Scope: b=3, compatible periodic lattice, original nonlinear VOL14-C map, right exponential Lie coordinates and D3A covariant face lift. No augmented Hessian floor or nonflat locality claim.

## 1. Use signed face cancellation before absolute values

Review 10 confirms D3A and D3B and supplies an exploratory stationary witness. It also notes that D3B's old multiplier arithmetic was omitted from its sealed expectations. Preserve that original seal. The D3C expectation explicitly records the old value and the new comparison, after author-side derivation and before hosted replay; it is a supplemental seal, not a blind prediction or retrospective repair.

Let e=(x,y) be a positive coarse link in direction mu. Its face has 27 positive crossing fine links, with target vertices v on the mu=-1 plane of B_y. The covariant lift is (R_U Y)_ell=Ad(s0(v))Y on these crossing links, zero elsewhere, where s0(v) is the canonical inverse target-centre tree path. Gauge-transform the target block by its tree holonomies (identity at its centre), so tree links equal identity. The target-end adjoint transforms the lifted variation to the same Y at each of the 27 target vertices. This gauge choice is used only for the local calculation of the gauge-invariant Wilson first variation.

A plaquette containing two links of this face has holonomy P=U_a V U_b^(-1) S^(-1), oriented with the positive mu link first and a positive transverse link V inside B_y next. Under the simultaneous lifted variation,

    P(t)=U_a exp(tY) V exp(-tY) U_b^(-1) S^(-1).

Its right or left translated tangent has norm ||Y-Ad(V)Y||. This is at most 2 d(V,1)||Y||. For the target tree gauge, d(V,1)<=n_V delta: compare the coordinate-ordered tree path to the initial vertex followed by V with the tree path to its terminal vertex. Commute the appended transverse letter across later occupied coordinate axes and cancel the inverse letter if present. Each perpendicular swap stays within the target block and contributes a conjugate elementary plaquette of angle at most delta. The checker verifies these words and counts.

Since the action is S=sum_p(1-Re P_p), its first derivative on a plaquette tangent of norm q is bounded by sin(theta_p)*q <= delta*q. Thus each two-face-link plaquette contributes at most 2 n_V delta^2 ||Y||, rather than the previous sum of two independent bounds 2 delta ||Y||. Plaquettes with only one face link cost at most delta ||Y||. Other plaquettes contribute zero to this variation.

For each direction there are 54 two-face-link plaquettes and 54 one-face-link plaquettes. Their incidence count is 2*54+54=27*6. The sums of n_V over the interior plaquettes are respectively 36,54,72,90, exactly enumerated.

Therefore, simultaneously for every coarse link,

    ||(R_U^* grad S)_e|| <= 54 delta + 180 delta^2.

This is a bound on the transported face gradient for arbitrary backgrounds satisfying the plaquette tolerance, before any stationarity assumption. It uses only local plaquette control and works even for nontrivial global holonomies.

## 2. Sharper stationary multiplier

At a constrained stationary point grad S=L_U^* lambda, hence (L_U R_U)^* lambda=R_U^* grad S. The D3A right-inverse bound is block diagonal in e and is at most 315/251 for delta<=1/30. Combining,

    ||lambda_e|| <= (315/251)(54 delta+180 delta^2)
                  <= 630/251.

The previous D3B bound was 1701/251. The new maximum is smaller by the exact factor 1701/630=27/10. This bounds the multiplier itself, not its signed second-variation form.

Review 10's witness has measured maximum plaquette angle 0.0438, outside delta<=1/30. Its quoted extrapolation of the D3A inverse constant is therefore not justified by that certificate. For a separate analytic extension, if delta<=1/22, the same VOL14-C pathwise 15-swap estimate and cos(t)>=1-t^2/2 give ||V||>=743/968. The D3A weighted mean count 8/3 then gives ||L_U R_U-I||<=704/2229, hence inverse norm <=2229/1525. The face gradient estimate at 1/22 is 342/121. Their product is strictly below 9/2 by integer cross multiplication. This extension is conditional on the true plaquette maximum satisfying 1/22; the measured witness angle itself is exploratory. It does not change the original scale-zero calibration or the primary delta=1/30 target.

## 3. Exact correlation imposed by stationarity

For each oriented plaquette write n_p=Im P_p, in its left insertion frame. Let d_U A be the sum of its four signed transported Lie insertions. Differentiating 1-Re P gives exactly

    DS_U[A] = sum_p n_p dot (d_U A)_p.

Thus the constrained stationary equation is d_U^* n=L_U^* lambda. In particular with K_U=d_U T_U on the D3A tangent section,

    K_U^* n=0.

This is an exact orthogonality of the curvature coefficient to constrained curl variations. It is stronger than treating the plaquette coefficients as independent or merely imposing the abelianized Bianchi identity. It is a necessary condition, not by itself a proof that the signed curvature form satisfies a relative bound of 1/2.

A concrete flat linearized reference for the next signed test is as follows. Let J=R, L J=I, T the flat D1 constrained section, H=T^*d^*dT, and v prescribed coarse link Lie data. Define

    A_v=Jv - T H^(-1) T^*d^*d Jv,
    n_v=d A_v.

Then L A_v=v and K_0^* n_v=0, with K_0=dT. This is the flat constrained quadratic minimizer on the tree section, from the positive D1 Hessian, up to the gauge freedom already fixed. In particular n_v is both a fine curl and orthogonal to the entire constrained curl space. The next reference test should optimize only over this stationary curvature subspace, preserving the max-norm constraint and the signed pairs. Numerical lower-bound searches must be labeled exploratory until supported by rigorous witnesses. For the nonlinear problem retain the full augmented stationary Hessian W_U-lambda D^2 F_c; the background quotient Ward identity does not make the flat comparison form invariant under arbitrary background gauge directions.

## 4. Remaining acceptance gates

The supplied independent review's six low-mode Ritz estimates are exploratory upper bounds on the minimum, not lower bounds on the complete relative spectrum. The adversarial curvature tests are numerical lower-bound evidence, not certified exact extrema. The next goal is a signed relative bound on the stationary curvature subspace and then its nonlinear counterpart, including the multiplier Hessian, in an explicitly specified common fluctuation section. Background Hessian positivity, weighted locality, scale iteration, induced action and continuum remain OPEN.

[Expected rows](EXPECTED-YM4-VOL14D3C-FACE-CANCELLATION-20261126.hbp) · [integer geometry checker](../../tests/ym4_vol14d3c_face_cancellation.py) · [expected replay](YM4-VOL14D3C-FACE-CANCELLATION-20261126.hbp) · [Independent review 10](../../reviews/10-VOL14D3AB-REVIEW-AND-STATIONARY-WITNESS-2026-11-26.md).
