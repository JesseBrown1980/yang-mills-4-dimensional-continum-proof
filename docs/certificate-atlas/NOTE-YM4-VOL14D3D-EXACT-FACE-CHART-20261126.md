# VOL14-D3D — exact nonlinear face chart and dual calibration

**Status:** author-side analytical derivation and exact integer arithmetic / synthetic quaternion-jet fixture. Independent review and hosted replay pending. Stacked on independent review 11 (#132, ce718f7). The stationary-subspace numerical lower bounds in that review motivate keeping the complete signed augmented Hessian. No uniform augmented relative floor or interacting locality theorem is claimed.

## 1. Alternative tolerances at the same coupling

Retain beta=9^7=4782969. For delta=1/36 choose epsilon=1/700, not the limiting approximation 1/648. The alternating cosine estimate gives

    1-cos(1/36) >= 15551/40310784 > 1/2800.

With the VOL12 prefactors bounded exactly as in VOL14-C section 4A, floor(beta/(64*700))=106 and floor(beta/(16*700))=427. Thus

    rho_star < 2^-57, rho_D < 2^-246,
    probability of a defective plaquette in a specified two-block support < 2^-236.

For a second diagnostic tolerance delta=1/58, epsilon=1/1700 passes the same cosine test. Since e>65/24>27/10 by the positive exponential series, exp(-x)<(10/27)^floor(x) for x>=1. The two floors are 43 and 175. Integer comparisons

    2^49 * 18^3 * 10^43 < 27^43,
    2^(181+69) * 10^175 < 27^175

give rho_star<18^-3, rho_D<2^-69 and the specified two-block defect probability <2^-59. Both calibrations concern the original periodic Wilson measure only. The 1/58 result is an additional conservative fixture, not a claim about the optimal admissible angle or a minimizer. The primary original delta=1/30 remains available; use 1/36 as the tighter fallback. A sampled reference constant of 16.2 is a numerical lower-bound estimate, not a certified upper bound, at either tolerance.

## 2. Exact finite face-orbit solution

Use the D3A covariant lift at a background U. For a fixed coarse link e and target vertex v of each crossing link, let s0(v) be the canonical target-tree suffix. Multiply each of the 27 crossing fine links on its right by s0(v) q s0(v)^(-1), with a common unit quaternion q. Every path contributing to the coarse mean crosses this face exactly once, and no other face. If P_i is its original holonomy and s_i the actual suffix to the target coarse centre, its new holonomy is exactly

    P_i(q)=P_i s_i^(-1) s0(v) q s0(v)^(-1) s_i.

In particular the unnormalized mean M_e q is a real-linear map on the four-dimensional quaternion vector space, with M_e 1=V_e. Each individual summand is an isometry, so ||M_e||<=1. The D3A swap bound gives ||s_i^(-1)s0 q s0^(-1)s_i - q||<=2 n_i delta ||q||, also for arbitrary quaternions q (their scalar parts cancel). Averaging the D3A suffix counts yields

    ||M_e - Left(V_e)|| <= 16 delta/3.

At delta<=1/30, ||V_e||>=7/8, hence the smallest singular value of M_e is at least 251/360. In particular M_e is invertible. The normalized VOL14-C mean along the *entire* face orbit is B_e(q)=M_e q/||M_e q|| and its exact inverse for any prescribed unit coarse link C_e is

    q = M_e^(-1) C_e / ||M_e^(-1) C_e||.

No Newton iteration is needed. This holds simultaneously for every face, because the path supports contain just one crossing face and all internal links are unchanged. Large q can leave the original small-field domain; the claim is invertibility of this particular orbit chart, not smallness of all resulting plaquettes or the global injectivity of the entire blocking map.

At delta<=1/36, cos(15 delta)>=263/288. Consequently

    ||V_e||>=263/288,
    sigma_min(M_e)>=661/864,
    ||(L_U R_U)^(-1)||<=789/661.

The last follows from the D3A differential error (16 delta/3)/||V_e||<=128/789. D3C's face gradient then improves the stationary multiplier estimate to

    ||lambda_e|| <= (789/661)*(59/36)=15517/7932.

The inverse sphere map is Lipschitz in geodesic distance with constant at most ||M_e^-1|| ||M_e||: its derivative is bounded by ||M_e^-1||/||M_e^-1 C_e||, and the denominator is at least 1/||M_e||. Integrate along a shortest arc. Therefore, if the starting fine field has plaquette angles <=1/36, and each new coarse target differs from its old coarse link by angle <=1/1000, the repaired field has plaquette angles <=1/36+4*(864/661)/1000 <1/30. This is an explicit feasible nearby field estimate. It does not say that a constrained minimizer chooses this feasible field.

## 3. Exact second derivative on the constraint surface

Fix B(U)=C. For a free fluctuation z, use the intermediate field U(t)=U exp(t z) linkwise and keep the original s0(v) fixed in the correction. The preceding single-face formula defines a differentiable real matrix M_e(t), without needing small-field control for more than a neighbourhood of t=0. Write q(t)=(1+u(t))/sqrt(1+|u(t)|^2), with u imaginary and u(0)=0. Define the 3-vector b(t)=Im(C^-1 M_e(t)1) and the 3x3 matrix A(t) with columns Im(C^-1 M_e(t)i_j) for the standard imaginary units i_j. Then b(0)=0 and A(0)=||V_e|| L_U R_U on that face. The constraint B_e(q(t))=C holds locally exactly if

    u(t)=-A(t)^(-1)b(t).

The sign of the scalar component is positive near the base. The derivative equations are

    u1=-A0^(-1)b'(0),
    u2=-A0^(-1)(b''(0)+2 A'(0)u1).

Each path derivative entering b and A can be obtained by the ordered quaternion product rule to second order. These formulas preserve the signed terms and avoid finite-difference polarization. For the repaired fine field, write the right exponential coordinates x(t) at U. On every crossing link,

    a=x'(0)=z+R_U u1,
    x''(0)=R_U u2+[z,R_U u1],

where the bracket is the quaternion commutator (twice the vector cross product). On internal links a=z and x''=0. If z is in the D3A free-coordinate section, then a=T_U z. The exact second derivative of the Wilson action along this feasible curve is

    W_U[a,a] + DS_U[R_U u2 + [z,R_U u1]].

The correction is supported on crossing links. At a constrained stationary point DS_U=lambda L_U, so this formula equals the augmented Hessian W_U[a,a]-lambda D^2F[a,a]. It retains the sign of the multiplier correction and does not require estimating its norm separately. Away from stationarity the same expression is a chart-specific second derivative, not an invariant quotient Hessian.

The checker includes a synthetic noncommuting two-path quaternion fixture with rational unit suffixes (9999, +/-200,0,0)/10001 and exponential product jets. It clears denominators, solves the 3x3 systems by integer Cramer's rule and verifies both derivative equations, the finite projective inverse, and the quaternion second jet. Omitting the mixed A' term or the commutator fails the fixture. This is an algebraic test of the formula, not a full nonflat lattice-background Hessian computation.

## 4. The scale-zero event versus the minimizer

For arbitrary prescribed coarse links C construct a canonical feasible fine field: all internal links identity, and every fine crossing link of a face equal to C_e. Every VOL14-C path then has holonomy C_e, so B(U_lift)=C exactly. An elementary fine plaquette with zero crossing directions is trivial, and with just one crossing direction its opposite crossing links cancel. With two crossing directions it is exactly a coarse plaquette holonomy (up to orientation). There are 3^2=9 transverse copies of each coarse plaquette. Thus for every global constrained minimizer U_*,

    S(U_*) <= S(U_lift)=9 S_coarse(C).

If C=B(U_in), also S(U_*)<=S(U_in). In particular the sufficient deterministic *total-action* criterion min(S(U_in),9 S_coarse(C)) < 1-cos(delta) puts every fine plaquette of every global minimizer below delta. This does not follow from the local VOL12 event: the total action is extensive. For a specified finite patch, if there exists a feasible competitor equal to U_* on every link outside the patch whose sum of all touched plaquette actions is below 1-cos(delta), minimality implies the same bound for the patch in U_*. The exact face repair above supplies a mechanism for building feasible patch competitors whenever the modified base field on the affected supports satisfies its chart hypotheses. A volume-uniform construction of such competitors from the original random small-field event and controlled exterior, or an appropriate local regularity theorem for constrained minimizers, is still required.

## 5. Next acceptance

Use the explicit repaired-curve jets to compute the *complete* signed augmented form for stationary witnesses, including the adversarial coarse field in review 11, at the stated minimizer tolerance. Compute the full relative spectral lower bound, not six Ritz values. Then seek a uniform estimate on the constrained-stationary fields in an explicitly fixed common section. Parallel priority: local minimizer regularity / feasible patch replacement, since calibration of the input does not calibrate the minimizer. The uniform augmented relative floor of 1/2, background locality and all continuum obligations remain OPEN.

[Expected rows](EXPECTED-YM4-VOL14D3D-EXACT-FACE-CHART-20261126.hbp) · [integer checker](../../tests/ym4_vol14d3d_exact_face_chart.py) · [expected replay](YM4-VOL14D3D-EXACT-FACE-CHART-20261126.hbp) · [review 11](../../reviews/11-VOL14D3C-REVIEW-AND-STATIONARY-SUBSPACE-2026-11-26.md).
