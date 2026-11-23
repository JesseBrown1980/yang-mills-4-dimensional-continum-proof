# YM4 VOL22 — outer-cut cancellation and source-restricted shell Dirichlet Gram

**23 November 2026; candidate theorem for the original continuous-SU(2) Wilson measure.** This is an independent continuation of VOL15–VOL21. It improves the unconditional finite-beta shell-noise floor by cancellation against a *physical free-boundary Wilson Gibbs reference on the larger cube*. It also gives an exact two-replica and finite Gram-matrix acceptance interface for genuine gauge-invariant source predictors. The current finite-beta floor remains far below the physical continuum requirement.

## 1. Original finite lattice and two valid action cuts

Let Q_r=[-r,r]^4, b=2r+1>=3, T_r the original positive links with both endpoints in Q_r, and W=T_(r+1) the original links inside the larger cube Q_(r+1). Embed all in an untwisted original even periodic torus of side L>=2(b+2). Let Y=W^c denote the original outside links. All links are actual SU(2) variables integrated against normalized continuous Haar, with the Wilson action beta sum_p Re U_p and beta>=0 finite.

As proved in VOL15 and checked in VOL21, for any source F supported inside T_r, its conditional predictor M_r=E[F|E_r] is f_r(B_r), where the exact cyclic noncommuting boundary resultants B_r depend only on R_r subset W\T_r. VOL21 counts N_r=24b(3b²+b-3) plaquettes touching R_r and proves kappa_r(F)>=(exp(-4 beta N_r)) when V_r=Var(M_r)>0.

Now write c=b+2 for the side of Q_(r+1). The only original plaquettes with one link in W and some links outside W are the 24c²(c-1) **mixed outer plaquettes**. This exact original-lattice count is independently enumerated by the VOL22 integer checker, including its no-wrapping embedding. Set

    C_r := 24(b+2)²(b+1).                                     (22.1)

Define the *free-boundary* original SU(2) Wilson reference on **all** W links:

    nu_r(dw) = Z_free^-1 exp(beta A_internal(W)) dH_W(w),       (22.2)

where A_internal is the sum of plaquettes whose four links are in W. This is a positive, normalized continuous-Haar probability measure. For any actual outer-link configuration y, the original conditional law is

    mu(dw | Y=y) = [exp(beta A_mixed(w,y))/nu_r(exp(beta A_mixed(.,y)))] nu_r(dw),  (22.3)

where A_mixed is the sum of exactly C_r mixed outer plaquette traces. The complete interior Wilson action cancels from the likelihood ratio **exactly**. Each trace belongs to [-1,1], hence

    e^(-2 beta C_r) nu_r(dw) <= mu(dw | Y=y) <= e^(2 beta C_r) nu_r(dw).  (22.4)

These are measure inequalities, valid for arbitrary exterior y, with the unmodified original Wilson links and no gauge fixing. Let nu_B be the pushforward of nu_r by the actual B_r(W), and lambda_r the genuine periodic Gibbs law of B_r. Integrating (22.4) through W -> B_r and separately over the actual exterior marginal gives

    e^(-2 beta C_r) nu_B <= law(B_r | Y=y) <= e^(2 beta C_r) nu_B,
    e^(-2 beta C_r) nu_B <= lambda_r <= e^(2 beta C_r) nu_B.

Consequently, for almost every true exterior y,

    law(B_r | Y=y) >= e^(-4 beta C_r) lambda_r.               (22.5)

Conditioning further on the *outer boundary sufficient statistic* B_(r+1) preserves (22.5); the resulting K_r(b',db)=law(B_r|B_(r+1)=b') is exactly the original continuous-SU(2) boundary-resultant transfer kernel of VOL21, not an abstract proposed kernel.

## 2. Improved unconditional finite-beta shell contraction

For any real centered square-integrable boundary-resultant function f, the variational variance identity and (22.5) give

    E[Var(f(B_r)|B_(r+1))] >= e^(-4 beta C_r) Var_lambda_r(f). (22.6)

VOL21's independent reference directly on R_r gives the same estimate with N_r in place of C_r. Choose the better cut:

    s_r = min{24b(3b²+b-3), 24(b+2)²(b+1)}.

For *every* bounded gauge-invariant Wilson source F supported inside Q_r and V_r>0,

    kappa_r(F) := (V_r-V_(r+1))/V_r >= exp(-4 beta s_r)>0.   (22.7)

Equivalently, for every f in L²_0(lambda_r), the exact original-Wilson transfer obeys

    ||K_r f||²_(lambda_(r+1)) <= [1-exp(-4 beta s_r)] ||f||²_(lambda_r). (22.8)

Because both derivations hold for every boundary function, the bound also holds on the gauge-orbit quotient and the source-generated invariant subspace. No F-dependent weight is inserted. The upper bound on the true transfer norm remains far too weak for the continuum mass rate.

The exact original-geometry verifier reconstructs the original 4D inner shell support and **independently** enumerates every mixed outer plaquette. At beta=9^12 the conservative rational-free strict certificate (using e<3) is:

| r | b | N_r inner touching | C_r outer mixed | better cut | E=4 beta min(N_r,C_r) |
|---:|---:|---:|---:|---|---:|
| 1 | 3 | 1,944 | 2,400 | inner | 2,196,172,075,676,256 |
| 2 | 5 | 9,240 | 7,056 | outer | 7,971,291,237,639,744 |
| 3 | 7 | 25,368 | 15,552 | outer | 17,569,376,605,410,048 |
| 4 | 9 | 53,784 | 29,040 | outer | 32,807,014,957,632,960 |

Thus kappa_r(F)>3^(-E). The *leading* large-b action count improves from about 72b³ to 24b³, an asymptotic threefold exponent reduction; the exact small-b improvement is recorded in the table. The resulting loss still tends rapidly to zero as beta and physical box width rise, so this is not the high-beta physical acceptance bound.

## 3. Exact source-generated two-replica Dirichlet form

The stronger future target should control the actual shell loss for the relevant Wilson source, rather than the entire L² boundary algebra. For any genuine boundary-resultant function f at radius r, define

    G_r(f) := Var_lambda_r(f) = 1/2 E_{B,B' iid lambda_r}(f(B)-f(B'))²,
    D_r(f) := E_{b'~lambda_(r+1)} Var_{B~K_r(b',.)}(f(B)).

The latter has the exact conditional two-replica representation

    D_r(f) = 1/2 E_{b'} E_{B,B' iid K_r(b',.)}(f(B)-f(B'))². (22.9)

For the genuine original Gibbs source F, choose f=phi_r(B_r)=E[F|B_r] as in VOL21. Then

    kappa_r(F)=D_r(phi_r)/G_r(phi_r) whenever G_r(phi_r)>0. (22.10)

These replicas can be constructed from the original Wilson conditional measures; the formula integrates out physical inner and shell variables, with no artificial boundary interpolation. It is unchanged by an affine rescaling F -> aF+c (a nonzero).

For a finite family of gauge-invariant Wilson-source predictor functions f_1,...,f_d on the actual resultant orbit quotient, form the exact real matrices

    G_ij=Cov_lambda_r(f_i,f_j),
    D_ij=E_{b'} Cov_{K_r(b',.)}(f_i,f_j).                     (22.11)

Both are positive semidefinite and 0<=D<=G. Every source in their linear span obeys kappa_r>=k if and only if

    D - k G is positive semidefinite on that source span.   (22.12)

For an independent family, this is a generalized smallest-eigenvalue certificate; for dependent families, restrict to the quotient by ker G. This defines a precise finite-dimensional **source-restricted** acceptance target. An exact rational matrix certificate can use principal minors or a rational LDL decomposition; a complete physical proof must also bound the approximation tail if the desired source algebra is infinite-dimensional.

## 4. Integer-only adversarial fixture, acceptance status

The strict integer verifier `tests/ym4_vol22_free_boundary_gram.py` independently enumerates the original positive 4D links and both action cuts at r=1..4. A separately declared **abstract 32-atom** binary Gibbs example with beta=ln 2 (implemented by exact integer powers of 2) checks the free-boundary likelihood envelopes, original-mixture relative domination, both two-replica Dirichlet identities, and a three-dimensional **gauge-invariant analogue** under simultaneous binary sign inversion. In that abstract control, G_11=3/16, D_11=13/72, kappa=26/27; the full three-source exact Gram has smallest generalized eigenvalue 58/63, witnessed by the positive-semidefinite rational matrix D-(58/63)G (all principal minors exact).

The binary toy is an algebraic falsifier for probability and matrix identities, **not** a SU(2) Haar integral or a claim of high-beta physical contraction. The analytic parts of (22.2)–(22.8) concern the original continuous-SU(2) Wilson law and preserve its noncommutative staples and gauge covariance. The verifier has a frozen HBP and hosted no-float normal/optimized replay; each actual CI result must be checked separately.

**OPEN physical acceptance:** quantitative source-restricted kappa_r>=1-exp(-2ma) (or a sufficient summed version) uniformly along beta(a), with a nonzero renormalized Wilson source, all Gauss/winding-sector transfer and the eleven continuum-construction obligations. VOL22 establishes a sharper all-beta finite-cutoff baseline and a fully specified matrix certification interface. Keep the theorem in draft PR #113's candidate map; production 3D viewer and main unchanged.
