# VOL14-D3B — signed curvature reconstruction test and stationary gauge identity

Status: author-side exact integer replay of the flat-reference curvature comparison; analytic stationary identity; hosted replay and independent review pending. D3A at 5d98eff passed all ten hosted workflows. This note deliberately records a failed quantitative acceptance target. The external VP/VNP arithmetic-circuit lower bounds were reviewed for relevance; no directly applicable curvature, constrained Hessian or background locality theorem was identified. They remain separate complexity references.

## 1. Signed reference form

Use D1's verified reconstruction A=S F on the flat tree-gauge constrained slice, with F=dA. The denominator of S is D=1944. On an oriented elementary plaquette p let a_1,...,a_4 be its four signed reference link variations, so a_i=sum_f s_if F_f/D, where s_if are integer rows of the translated reconstruction. Consider the frozen-frame curvature comparison form

    C_ref(A) = 2 sum_p n_p dot sum_(i<j) a_i cross a_j,

where the real three-vector n_p is arbitrary with ||n_p||<=delta. This is the algebraic curvature form with flat transports and flat constraint reconstruction and an independent bounded curvature coefficient. It is a reference model, not the actual nonflat Wilson Hessian. In the actual form n_p would be the imaginary plaquette part in a common frame and each a_i would involve the background transport and background constraint.

Before bounding absolute values, combine all contributions to the same ordered plaquette pair f<g:

    c_pfg=sum_(i<j)(s_if s_jg-s_ig s_jf).

Then C_ref(A)=2/D^2 sum_(p,f<g) c_pfg n_p dot(F_f cross F_g). This preserves all signed cancellations within one plaquette. The checker enumerates 486 anchored plaquette types; 72 have one nonzero link row, 132 have two, and 282 have four. There are 9530764 nonzero signed pair coefficients before folding. Folding |c_pfg| into a symmetric type matrix M means each pair contributes to both ordered entries (including twice to a diagonal type entry if both types coincide but the actual plaquettes are distinct). For the vector of l2 norms of F of each type over coarse blocks, Cauchy-Schwarz under translated shifts gives

    |C_ref(A)| <= delta/D^2 * v^T M v.

The proof applies to all compatible periodic volumes; coincident wrapped coordinates only further cancel. A positive integer vector w satisfying M w<=658 D^2 w proves

    |C_ref(A)| <= 658 delta ||F||^2.

The checker builds positive weights deterministically, verifies every component inequality and obtains the ceiling sequence 1929,715,661,659,659,658,658,658,658,658,658,658. The bound does not establish the target 1/2 relative budget at delta=1/30: 658/30 exceeds 1/2. It would require delta<=1/1316 for this reference contribution alone. No actual nonflat instability follows from this failed sufficient estimate. The experiment confirms that even combining local signed pairs before an entrywise envelope leaves substantial slack. The next method must exploit correlated curvature, stationarity and gauge structure rather than merely refining the same envelope.

## 2. The correct constrained stationary Hessian and its gauge radical

Let U_* be a constrained stationary background with B(U_*) fixed. In local coordinates let F_c(U)=log(B(U_*)^(-1) B(U)) (one Lie-algebra vector per coarse link), and let dS(U_*)=lambda dF_c(U_*). Define the augmented function J(U)=S(U)-lambda dot F_c(U), so dJ(U_*)=0. Its ambient second differential at U_* gives the intrinsic second variation on ker L_U. The formula follows by differentiating F_c(U(t))=0 twice and substituting the first-derivative multiplier identity. In particular the constraint-curvature correction is required in general.

For every fine gauge transformation g equal to the identity at coarse centres, both S and F_c are invariant in a neighbourhood of U_* by the local gauge covariance of the blocking map. Thus J is invariant. If G_U phi is the infinitesimal generator of such a gauge transformation, then dJ(U)[G_U phi]=0 for all U in that neighbourhood. Differentiating along an arbitrary variation a gives

    D^2 J(U_*)[a,G_(U_*) phi] + dJ(U_*)[D_a(G_U phi)] = 0.

The second term vanishes by stationarity. Therefore D^2 J(U_*)[a,G_(U_*) phi]=0 for every a, and the actual constrained Hessian descends to the quotient by the root-zero infinitesimal gauge subgroup. This is an exact identity at arbitrary constrained stationary backgrounds, independent of translation invariance and the small-field tolerance. It is an identity of quadratic forms; numerical eigenvalues in two nonisometric coordinate sections need not agree. Coarse stabilizers are separate.

In right exponential link coordinates,

    (G_U phi)_ell=Ad(U_ell^(-1)) phi_source - phi_target.

The D3A tree gauge is one section. An alternative section can minimize internal link variation norm within each block over phi zero at the centre. This minimization is local, strictly convex (the kernel of the internal covariant gradient with centre zero is trivial by propagation along the rooted tree), and unique. It preserves the constraint because L_U G_U phi=0. At constrained stationary backgrounds the augmented Hessian has identical quadratic values in these sections. This permits local Coulomb-type fluctuation gauges to improve curvature bounds without requiring a global Landau background gauge. A numerical test of the ambient Hessian alone at nonstationary backgrounds does not have this identity.

## 3. First explicit multiplier ceiling

At delta<=1/30, each positive link belongs to six plaquettes; a right unit Lie variation changes each Wilson term by at most sin(theta_p)<=delta. Hence every link component of the gradient, viewed as a three-vector, has norm <=6 delta. D3A's right inverse J_U=R_U (L_U R_U)^(-1) implies lambda=J_U^* grad S. Since R_U on each face consists of 27 orthogonal adjoint maps, the triangle inequality and inverse norm 315/251 yield

    ||lambda_e|| <= (315/251) * 27 * 6 delta
                 <= 1701/251.

This is a uniform coarse-link multiplier bound under the stated local plaquette condition and stationarity. It is deliberately loose; it is not a relative bound on the constraint-curvature term. To exploit the Ward identity quantitatively, estimate the full augmented Hessian in a local minimizing section rather than bounding W_U and lambda D^2 F_c independently on arbitrary gauge directions.

## 4. Next acceptance gate

Construct local, constrained-stationary background witnesses and compare signed augmented forms in the tree and internal-minimum-norm sections. Verify the Ward radical with exact rational quaternion backgrounds or rigorous enclosures, including the multiplier term. Then seek a local quadratic-form certificate for the augmented Hessian using shared plaquette energy and boundary constraints. Preserve the target delta=1/30 and lower relative floor 1/2 as OPEN; the test here demonstrates the present reference envelope does not close that gate. Background Hessian positivity, background locality, induced measure and continuum construction remain OPEN.

[Expected rows](EXPECTED-YM4-VOL14D3B-SIGNED-CURVATURE-20261126.hbp) · [integer checker](../../tests/ym4_vol14d3b_signed_curvature.py) · [receipt](YM4-VOL14D3B-SIGNED-CURVATURE-20261126.hbp).
