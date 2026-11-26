# VOL14-D3A — covariant crossing lift on the calibrated small-field domain

**Status:** AI-authored derivation with exact combinatorial and rational checker; independent mathematical review and hosted replay pending. Builds on VOL14-C and D1/D2. Scope: original b=3 SU(2) group-valued map, all fine plaquettes in the two endpoint blocks and their interface have angle <=1/30. No background minimizer or Hessian coercivity claim.

## 1. A gauge-covariant right inverse

For coarse edge e=(x,y=x+3e_mu), every path P in VOL14-C crosses the same interface exactly once, at one of 27 fine crossing links l with endpoint t in the y block. Write P=A U_l S, with suffix S the transport from t to y. Let J_l be the reference transport t->y obtained by reversing the shortest path y->t that orders all transverse coordinates first and the mu coordinate last. Define the face lift R^cov by X_l=Ad(J_l) v_e on those 27 links and zero on internal links. Here v_e is a right Lie-algebra variation at the coarse endpoint y and X_l is a right variation at t. All transforms are in their stated endpoint frames. The lift is gauge covariant and ||R^cov v||^2=27||v||^2, since SU(2) adjoint maps are orthogonal.

The reversed suffix S^-1 is the y connector c followed by z_mu+1 negative mu steps, where z in {-1,0,1}^4 is the path offset. Sort the connector steps into transverse-first, mu-last order by perpendicular adjacent swaps, then cancel any inverse mu steps. The appended steps are already last in this order. At most 6 swaps are needed, all inside the y block, because c has at most 4 steps with distinct axes. The resulting path is J_l^-1. Each swap contributes a conjugated elementary plaquette of angle <=delta. Thus d(S,J_l)<=6 delta, and

    ||Ad(S^-1 J_l)-I|| <= 12 delta.

The checker enumerates all 2532 choices of direction, z and target connector, verifies endpoints and internal support, and records the swap histogram. This is a support count, not a floating-point simulation.

Let V be the quaternion average of P, B=V/|V|, and w_P their normalized positive weights. In the right coarse coordinates, differentiation of normalization gives

    L_U R^cov v = (1/|V|) sum_P w_P Im(B^-1 P Ad(S^-1 J_l) v).

For unit quaternion q=a+b (b imaginary), the real-linear map M(q):v->Im(qv) has norm <=1. Moreover sum_P w_P M(B^-1 P)=|V| I exactly, since B^-1 V=|V|. Subtract this identity BEFORE estimating absolute values. Consequently

    ||L_U R^cov-I|| <= 12 delta / |V|
                    <= (12/30)*(8/7)=16/35.

Use the already established VOL14-C normalization floor |V|>=7/8. The crossing supports for different coarse edges are disjoint, and each path uses only its own crossing face. Therefore this is a block-diagonal coarse-link estimate, valid uniformly in volume. Every 3x3 diagonal block has minimum singular value >=19/35 and inverse norm <=35/19.

Define J_U=R^cov (L_U R^cov)^(-1). Then L_U J_U=I, with

    ||J_U|| <= sqrt(27)*35/19.

This establishes solvability of the tangent constraint, not positivity of the Wilson quadratic form. It also avoids assuming a uniform global Landau link-angle estimate or trivial holonomy.

## 2. Covariant coordinates

Replace the fixed ordinary face mean by the transported mean: on each crossing face require sum_l Ad(J_l)^* z_l=0; tree variations remain zero. The complement is exactly orthogonal to the range of R^cov. With T_U=I-J_U L_U, the two terms are orthogonal, giving ||T_U z||^2=||z||^2+||J_U L_U z||^2. T_U maps these coordinates bijectively onto tree-zero ker L_U by subtraction of the transported mean. All constructions are local and covariant. Fix gauge transformations at the coarse centres when defining the residual gauge section; handle any coarse stabilizer separately. A transported-mean coordinate spectrum is gauge invariant under the induced orthogonal change of coordinates, unlike a fixed ordinary face-mean coordinate spectrum in general.

## 3. Correct Hessian for the constrained minimizer

Review 09 computes T_U^* S'' T_U in exponential link coordinates. It is an ambient Hessian restricted to the tangent constraint. For a fixed coarse target B(U_*), define local constraint coordinates F(X)=log(B(U_*)^-1 B(U_* exp X)) edge by edge, near X=0. On the gauge-fixed slice, if the background is a constrained stationary point and S'=L_U^* lambda, the Hessian of the restricted action is

    T_U^* (S'' - sum_e lambda_e . F_e'') T_U.

This follows by twice differentiating F(X(t))=0. The sign corresponds to the stated multiplier convention. The second term must be bounded; at an unconstrained stationary point lambda=0. A pointwise inverse for L_U supplies the local submersion, but does not yet give a volume-uniform nonlinear chart radius or a multiplier estimate.

In addition the plaquette curvature term cannot be bounded pointwise solely by the plaquette curl times the fluctuation norm: transported signed insertions a,b,-a,-b have zero first-order sum but nonzero second-order commutator (2[a,b] in the second derivative of the product). In a nonzero curvature background that term can contribute to the Hessian. A successful relative bound must exploit summed covariant identities, constraints, or stationary-background structure. Do not assume the cancellation holds separately on every plaquette.

## 4. Relative weighted acceptance criterion

For a positive reference Hessian H0 on the same identified coordinates, if the FULL relative form H0^(-1/2)(Re(W H_U W^-1)-H0)H0^(-1/2) >= -alpha I, then Re(W H_U W^-1)>= (1-alpha) H0. No second subtraction of the identity weighting cost is needed because it is already included in the full relative form. If bounding only the weighted difference H_U-H0, subtract the separate identity weighting cost. From D2's exact absolute comparison its certified relative cost is <=105*(23/4620)=23/44; review 09's 0.0096 is exploratory. For the physical constrained Hessian use the full multiplier-corrected operator. A new bound on weighted T_U is also needed for the covariance prefactor.

## 5. Evidence and next target

Reviews 08 and 09 are archived as supplied AI reviews. Review 09's scope header says eight backgrounds, while its tables contain ten. Row-zero envelopes are not global suprema. Its eigenvalue gauge comparison is a numerical observation; its own validation script explicitly notes the noncovariant fixed Z. All sampled backgrounds are exploratory; none is a constrained minimizer. The source scripts are retained as external supplied attachments, not executed by the integer-only proof repository; see the source hash manifest.

Next target: construct actual constrained stationary backgrounds with coarse target and fixed centre gauge, derive a quantitative multiplier estimate and a local energy-relative curvature bound, and prove the weighted lower bound including the constraint Hessian. A uniform nonlinear chart, admissible nonflat background locality, induced measure and all continuum gates remain OPEN.
