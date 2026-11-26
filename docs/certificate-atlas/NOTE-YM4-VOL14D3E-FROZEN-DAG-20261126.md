# VOL14-D3E — frozen path DAG, exact augmented operator action and stationary pilot

**Status:** integer mixed-jet and generalized-pencil fixtures passed locally (normal and optimized Python, byte-identical); analytic reduction; separate exploratory floating-point stationary measurements. Hosted replay and independent review pending. Stacked on D3D (#133, a3710664, 10/10 hosted workflows). Uniform background floor, review 11's actual adversarial fixture reproduction, weighted interacting locality and continuum remain OPEN.

## 1. Matrix Laws source binding

The original Matrix Laws Essentials source was inspected at main commit e7c22188c83b59aae77cbaff142b86861e2db1d3:
- [Power-of-three jump and transposition memo](https://github.com/JesseBrown1980/The-matrix-law-essentials/blob/e7c22188c83b59aae77cbaff142b86861e2db1d3/docs/LAW-POWER-OF-THREE-JUMP.md), blob 37c2b86922c5ae5703ff12bf0996dfd5548bc246.
- [Frozen-trial parameter replay](https://github.com/JesseBrown1980/The-matrix-law-essentials/blob/e7c22188c83b59aae77cbaff142b86861e2db1d3/docs/LAW-FROZEN-TRIAL-PARAMETER-REPLAY-20261114.md), blob 8e2554466d3926c4e473501dc01ac50d056715b2.
- [Weighted target-spill and paired moments](https://github.com/JesseBrown1980/The-matrix-law-essentials/blob/e7c22188c83b59aae77cbaff142b86861e2db1d3/docs/LAW-WEIGHTED-TARGET-SPILL-PAIRED-MOMENTS-20261114.md), blob 19edabcc2a07e9ba5883d2bf96ccfe301bd965de.
- [Two-energy Schur Gram jump](https://github.com/JesseBrown1980/The-matrix-law-essentials/blob/e7c22188c83b59aae77cbaff142b86861e2db1d3/docs/LAW-SCHUR-GRAM-WILSON-CENTER-JUMP-20261120.md), blob a1420189b26152c47159c16f2732a9c8a5e6dacd.

The transferable ideas are exact path-state reuse, signed target reduction, a frozen operator pencil and paired Gram evaluation. The general nonflat operator has no established circulant NTT diagonalization. The flat reference does have the D1/D2 Bloch decomposition, so factor it once and reuse it at both amplitudes. No nonlinear time jump is assumed.

## 2. Exact simplification of the augmented form

Fix a feasible field U, coarse links C=B(U), V_e=r_e C_e with r_e>0. Use the local real constraint

    G_e(U')=Im(C_e^(-1) V_e(U')).

Near U this has the same zero locus as the normalized logarithmic constraint F=log(C^(-1) B(U')). Indeed G_e=r_e(U') Im exp(F_e), with the positive scalar sign fixed near U. At U, DG=diag(r_e) DF. If DS=lambda DF, set mu_e=lambda_e/r_e. Then DS=mu DG and the scalar augmented action J_G=S-mu dot G is stationary. On the constrained tangent, D^2G[a,b]=diag(r_e) D^2F[a,b] because both first derivatives DF[a],DF[b] vanish. Therefore

    H_aug=T_U^* [D^2 S - sum_e mu_e dot D^2 G_e] T_U.

This is exactly the D3D feasible-curve Hessian at stationarity. It uses a fixed linear contraction of the unnormalized mean, and avoids differentiating norms, logarithms or the face-repair solve for every direction. Solve mu from the 3x3 face derivative systems of DG using D3A's right inverse; then freeze U,C,mu,T_U and the flat comparison section. The gradient of J_G vanishes at a stationary field, ensuring the correct quotient Ward identity. At nonstationarity the ambient augmented form need not equal the second derivative along a repaired feasible curve.

Hessian-vector products can be formed by differentiating the gradient of this single scalar contraction in the fixed direction T_U z, then applying T_U^*. Forward and reverse differentiation traverse the same local graph. Do not form the dense global Hessian.

## 3. Ternary connector prefix DAG

For z in {-1,0,1}^4 let k be its number of occupied axes and A_X(z) the uniform average of all shortest ordered signed connectors from centre X to X+z. The disjoint last-letter partition proves

    A_X(0)=1
    A_X(z)=(1/k) sum_(j:z_j!=0) A_X(z-z_j e_j) U_(X+z-z_j e_j -> X+z).

The raw sum k! A_X(z) satisfies the same recurrence without division. This is a noncommuting ordered quaternion identity: it keeps each path multiplicity, rather than treating distinct holonomies as equal. For 81 nodes the number of predecessor transitions is sum k*binom(4,k)*2^k=216. Directly building each connector word requires sum k*k!*binom(4,k)*2^k=2216 quaternion products per centre (counting multiplication from identity). Reverse connectors are exact quaternion conjugates. The source and target connector means are shared among all incident coarse links. With the existing independent-connector factorization, the full mean is

    V_(X,mu)=(1/81) sum_z A_X(z) M_(X,mu,z) conj(A_(X+3e_mu)(z)).

The 10473 ordered pairs per coarse link become 81 factorized terms. Review 09 already exploited the latter factorization; the new improvement is the prefix DAG across offsets and sharing between faces. Compared with independently constructing source and target connector words for four outgoing faces, the connector product count is 17728 per centre versus 216 once, a factor 17728/216 (not a claim about total runtime).

The identity extends exactly to mixed quaternion jets (value, d1, d2, d12) by the product rule

    (ab)_12=a_12 b + a_1 b_2 + a_2 b_1 + a b_12.

Keep all signs through the common target sum. The checker uses rational unit links q/5 and integer Lie variations, five centres, all 405 endpoint jets, all four coarse-link directions and all 10473 independent connector pairs per direction. It compares the mixed jets from direct permutation enumeration with the DAG, clearing denominators by 81*24^2*5^11. Changing the quaternion multiplication order or removing a mixed product is rejected. This is an exact local algebra fixture, not a positivity proof for nonflat backgrounds.

## 4. Frozen generalized pencil

At a fixed background write H=H_aug and M=H_0 on the same independent coordinates. Freeze a trial matrix Y. The generalized threshold residual numerator at rational threshold n/d is

    R(n,d) = (d H - n M)Y = d A - n B,
    A=HY, B=MY.

Consequently R*R=d^2 A*A-d n(A*B+B*A)+n^2 B*B. The same Gram identity works in any fixed inner product. Only two anchor applications are needed for this fixed trial and six thresholds (or any other thresholds). The exact toy verifies the identity and rejects a flipped mixed-moment sign. This is the generalized-pencil version of the original frozen-trial replay law; it does not itself certify the full spectral floor, and it cannot reuse H-dependent moments after changing the nonlinear background. For a fixed Krylov basis or trial block the threshold tests can be replayed on the cached signed products.

## 5. Exploratory independent staggered fixture

Review 11's two scripts and saved adversarial coarse data are not in the proof tree; the source inventory lists their hashes and external dependencies. They were not available in the author workspace. Do not confuse the following independent high-frequency pilot with the original projected free optimum.

Start with coarse target C_(X,0)=exp(a (-1)^X_1 i), other coarse links identity. Use block-tree gauge (tree links exactly identity), so D3A transported R is the constant crossing-face lift in these coordinates. Minimize with the flat Bloch inverse preconditioner, restoring the exact normalized constraint at each step by D3D's 4x4 face solve. Warm-start the tighter-tolerance stationary field for the second amplitude. The actual measured maximum angles lie below their respective targets. All numerical work uses float64 outside the proof repository; a two-jet polynomial for the exponential has the exact derivatives at zero. The independent review 07 flat Bloch code supplies H0, and JAX differentiates the scalar J_G with the prefix DAG. ARPACK acts on the full whitened relative operator H0^(-1/2) H_aug H0^(-1/2). No six-mode restriction is used. A random full-space starting vector and small eigenpair residual are numerical evidence, not a proof of the global smallest eigenvalue.

| Target delta | 1/36 | 1/30 |
|---|---:|---:|
| Coarse target amplitude a | 0.05090003454623512 | 0.06107842456905684 |
| Fine plaquette max | 0.0277646238629059 | 0.03331717799296001 |
| M=2 relative stationarity residual | 2.9241733605650726e-10 | 1.6447320913856375e-10 |
| M=2 coarse constraint max error | 2.0816681711721685e-17 | 2.0816681711721685e-17 |
| M=2 all 11520 coordinates, augmented Ritz | 0.6629920348638614 | 0.61164573754213 |
| Eigenpair residual | 3.3190144187191077e-7 | 8.73792894905139e-7 |
| Wilson-only repeat Ritz | 0.6629196282865946 | 0.6110654085240713 |
| Augmented repeat Ritz | 0.6629920348637519 | 0.6116457375404647 |
| M=4 all 184320 coordinates, augmented Ritz | 0.6629920357590426 | 0.6116457375588242 |
| M=4 eigenpair residual | 8.814019085677644e-6 | 1.5320342635908563e-6 |
| M=4 matvec calls incl residual | 62 | 74 |

The M=2 fixture is exploratory below the existing M>=4 certificate scope. Its periodic repetition onto M=4 reuses the field without another minimization: every local equation sees the same translated field. The M=4 stationarity residuals are 2.9241737216301596e-10 and 1.644731222477135e-10, constraint maximum 2.0816681711721685e-17 at both. The larger eigensolver is unrestricted across all larger-torus fluctuation modes. These are two numerical witnesses, not a background-uniform bound or proof of minimization. The normalized flat comparison check on the smaller torus gave relative residual 9.837306452492494e-15. The augmented form's random-direction finite-difference checks on the repaired curve (step 1e-3) agree within 1.53e-7 absolute at both tolerances. An initial float32 cross-check was discarded for cancellation error; the logged check is float64. A separate experiment freezing JAX linearization closures timed out and was abandoned; the working implementation reuses compiled topology and flat Bloch factors, not a dense Hessian.

The full relative operator would have 33973862400 entries if dense, roughly 272 GB at float64. The measured larger-torus eigensolver uses only matrix-vector actions, flat 240x240 Bloch factors per momentum, and local graph data. The multiplier contribution modestly raises the measured lowest relative eigenvalue on the smaller torus at both tolerances; it is not asserted positive on every direction.

## 6. Acceptance status

The integer verifier certifies the local mixed-jet algebra and the fixed-trial generalized-pencil identities only. Its receipt reproduced byte-identically locally in normal and optimized mode; expectations were sealed after local calculation, not blind predictions. Floating-point scripts, frozen arrays and logs are kept outside the proof tree, authenticated in the source inventory. No no-float exemption is introduced.

Next use the same operator on review 11's actual adversarial coarse data when available, check further independent coarse patterns, then establish a certified all-background relative lower bound. The minimizer-angle transfer, uniform augmented floor >=1/2, background locality and continuum remain OPEN.

[Sealed expectations](EXPECTED-YM4-VOL14D3E-FROZEN-DAG-20261126.hbp) · [integer checker](../../tests/ym4_vol14d3e_frozen_dag.py) · [receipt](YM4-VOL14D3E-FROZEN-DAG-20261126.hbp) · [source inventory](../../reviews/12-D3E-PILOT-SOURCE-INVENTORY-20261126.md).
