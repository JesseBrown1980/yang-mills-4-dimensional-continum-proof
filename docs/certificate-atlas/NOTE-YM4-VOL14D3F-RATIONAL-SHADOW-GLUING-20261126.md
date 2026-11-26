# VOL14-D3F — rational primitive-cell replay and signed local-to-global gluing

**Status:** two source-derived rational near-stationary witnesses and analytic certificate reductions; integer fixture calculations and stencil radius explored locally; hosted replay and independent review pending. Uniform nonlinear augmented relative floor remains OPEN. Stack: review 12 (#135, ea135f0d). No quantum gravity claim is imported as a premise.

## 1. Review 12 changes the target

Review 12's original adversarial field has Wilson-only relative Ritz 0.4685 and augmented Ritz 0.8714 at a measured maximum angle 0.033335, slightly above 1/30; at angle 0.027779 the figures are 0.5566 and 0.8920 (also slightly above 1/36). These are exploratory full-space eigensolver estimates, not spectral lower bounds. The previous D3E transverse-staggered field remains the harder known augmented test (0.6116457 at measured angle below 1/30). Do not bound the multiplier and curvature terms independently. Their correlations are essential. Review 12 requests cross-implementation checks on the original adversarial arrays; those arrays are not accessible in this author workspace.

## 2. Freeze an exact rational primitive cell before spectral certification

The prior D3E archive supplied both staggered fields, with quaternion order (real,i,j,k), fine lattice shape 6^4, positive directions last. Inspection shows exactly zero j,k components and translational differences less than 4e-16 under a fine shift of 3 in axes 0,2,3. The source arrays are exploratory and are not exactly periodic with that smaller period. Select the fine slice [:3,:,:3,:3,:,:], retain the full length 6 of axis 1, and round each stereographic coordinate t=b/(1+a) to n/2^40 (nearest integer). The exact rational representative is

    U_l=(D^2-n_l^2+2 D n_l i)/(D^2+n_l^2), D=2^40.

The maximum measured component change on the selected cell is below 9e-13 for either amplitude. Freeze the 648 integer indices as a 33-value table plus a base-36 address string; both amplitudes share the same string. The fixture file SHA-256 is 305b5acbac5f7636908a2081754122fb79b4b7661fde44cb4fb5f4bfc028ec54. Its sources are the two npz inputs whose SHA-256 values are recorded in the D3E inventory: ba72ff2426b776efab7010ba74d162903ca032d4fbf9643a776e5e3cc763e818 and a6a0e65d3bc5776d93e334667fab793ef967c1d14e3f9f93f6a3ead913016953. The rational fixture is a new exactly periodic input, not an enclosure proving that the old floating-point background is exactly stationary.

The integer checker verifies unit norm, all 160 tree links identity, all 972 positive elementary plaquettes, the strict angle inequalities by 1-cos(1/d)>=1/(2d^2)-1/(24d^4), all eight coarse means of norm >=7/8, and a rational bound on stationarity defect. It uses the unnormalized rational constraint G_e(U')=Im(conj(V_e(U)) V_e(U')), which is D3E's constraint with an extra positive scale r_e. Its zero locus locally equals the prescribed normalized mean. Since the field is Abelian, the first variation of S and the multiplier contraction both vanish exactly in the two charged directions by conjugation symmetry. For the neutral direction each path derivative is i times its signed link incidence times the path product. Use the D3E last-letter DAG, shared denominator Q (LCM of all link denominators), and denominator 81*24^2*Q^11 for the eight means and their sparse first derivatives. The checker verifies (DG_e R)_neutral=|V_e|^2 exactly; choose the neutral multiplier by dividing the transported face gradient by |V_e|^2. Interval integer floor/ceiling bounds on each signed term certify the full neutral gradient defect.

| Target | Exact upper bound on max plaquette action (ppt) | Exact max stationarity defect per link component (ppt) |
|---|---:|---:|
| 1/36 | 385412410 | 16 |
| 1/30 | 554965836 | 12 |

ppt = parts per 10^12. These statements lift to every compatible periodic repetition by locality (each primitive link derivative collects all corresponding incident factors, including repeated occurrences). The original M>=4 proof domain is retained for applications; the primitive cell is a periodic quotient for computing those local sums. No exact stationarity, minimization or positivity claim follows from a small defect. The full charged derivative and second jet are not reconstructed here.

## 3. Exact symmetry reduction of the new rational fixture

On the 4^4 coarse torus, the translations by one coarse block along axes 0,2,3 and two along axis 1 generate G=C4 x C2 x C4 x C4 of order 128. In tree gauge the face lift is constant, and Z has 720 real dimensions per block. All ingredients of the frozen pencil H_aug-cH0 for this rational representative commute with G, by the actual background and multiplier periodicity. The common global U(1) color conjugation also commutes with the pencil; it fixes the neutral i color and rotates j,k. Thus complexify and split into neutral and two charged eigenspaces of a quarter-turn in the j,k plane. Each translation-character/color sector has dimension 2*240=480. Since the phase factors on this torus are exactly Gaussian units, there is no trigonometric approximation in the character transform. Conjugacy pairs neutral sectors (16 self-conjugate, 72 representatives total); charged minus sectors are the complex conjugates of charged plus at opposite character (128 representatives suffice). Therefore 200 complex matrices of dimension at most 480 suffice for the entire 184320-dimensional fixed-background pencil; the integer checker verifies character orthogonality and dimension coverage. This is an exact algebraic decomposition, not a report of having assembled or factored these matrices. There is no such symmetry assumption for general nonflat backgrounds.

## 4. Signed compensated patch assembly

Let A be the *complete* reduced threshold pencil H_aug-cH0 on the direct sum of independent Z_U block coordinates, identified block-locally with Z at identity by D3A's isometry. For the Wilson term after the tangent pullback each plaquette sees the four coarse blocks 0,e_mu,e_nu,e_mu+e_nu at most. For the constraint term each coarse mean and its second derivatives see just its two endpoint blocks; the tangent map on its links stays in those blocks. Thus every reduced matrix offset is in {-1,0,1}^4 with l1 length <=2 (33 possible offsets). These local range statements use the actual VOL14-C path support and face-wise lift, not translation invariance.

On the infinite covering lattice use the integer tent w_R(x)=product_j max(0,R-|x_j|). Its squared norm is N=S^4 with S=(2R^3+R)/3. For an allowed offset a of l1 length k, the overlap sum g(a)=sum_x w_R(x)w_R(x+a)=S^(4-k)(S-R)^k. All are positive for R>=2. Define the compensated pencil by A_sharp(x,x+a)=N A(x,x+a)/g(a). Both H_aug and H0 must carry the same compensation; retain signed entries. Then for periodic fields (with period lifted coefficients and vectors) the finite sum over one fundamental set of window centres satisfies the exact equality

    A quadratic form = (1/N) sum_centres <w_R z,A_sharp w_R z>.

Indeed reindex the finite support offsets modulo the period and sum over window positions; each original oriented edge coefficient is multiplied by g(a)/N, canceling its compensation exactly. This also works for periods shorter than the window if repeated images are retained as separate entries in the lifted local form. If every lifted patch compression of A_sharp is positive semidefinite, the global relative floor follows without a boundary-error subtraction. A single patch or a finite sample of backgrounds is insufficient. The proof gives a useful exact criterion; no claim is made that practical small patches at c=1/2 satisfy it.

As a flat-reference calibration, the D2 signed stencil is rebuilt once. Reuse its folded positive Schur witness w, formed by 12 power-weight iterations using 4160 times the length-one absolute fold plus 16641 times the length-two fold. For radius R the coefficient excesses are R/(S-R) and (S^2-(S-R)^2)/(S-R)^2. With R=99 the integer checker tests the weighted row inequality for the excess envelope against 23/4620. R=98 fails this particular frozen witness (not a necessary threshold). Therefore the compensated flat H0 has floor >=1/220, including on its Dirichlet patches. The calibration window side 197 is far too large to factor densely; do not allocate it. It demonstrates exact consistency of the local-to-global rule with D2 and gives an analytic flat calibration. Search smaller patch-specific signed certificates, use sparse boundary elimination and exact symmetry before any large computation. A signed scalar wrapped-period fixture verifies the gluing identity and refuses omitted compensation.

## 5. Joint boundary Schur certificate

Review 12 correctly notes that fixing face coordinates alone need not decouple interiors after the tangent correction. Use the actual sparse constrained pencil before elimination. On tree-zero variables a, let B_c be D^2J_G-c P_U^* H0 P_U (with the block-local transported identification understood); let L be the actual linear constraint. P_U is the orthogonal projection onto the transported zero-face-mean space. Then P_U T_U=I on that space. With a right inverse J of L and T_U the tangent map, the map [T_U,J] is invertible on tree-zero variables. The bordered KKT matrix

    [ B_c   L* ]
    [ L      0 ]

is congruent in these coordinates to

    [ A_c   C    0 ]
    [ C*    D    I ]
    [ 0     I    0 ],

where A_c=T_U^* B_c T_U=H_aug-cH0. The lower two-by-two block is invertible with inverse [0,I; I,-D] and inertia (m,m,0) for m constraints. The Schur correction on A_c vanishes, hence the bordered inertia is exactly inertia(A_c)+(m,m,0). This remains true even if the ambient B_c is indefinite; a direct test that demands its positivity is too strong. The exact integer synthetic checker verifies the inertia shift and rejects a negative tangent mutation. In a conditional elimination keep all crossing primal variables and all interface multiplier coordinates until the graph actually splits. Eliminate independent nonsingular interiors, add their signed Schur contributions on the common boundary, and account for each eliminated inertia. Singular pivots require pivot blocks or a different ordering. Do not use the KKT inertia rule on naively truncated constraints in a compensated window; the window test is on the reduced A, or an exact local representation of it including all required halo inputs.

This is the signed-matrix counterpart of the new Matrix Laws primitive and adaptive shadow replay ([PR #19, pinned source](https://github.com/JesseBrown1980/The-matrix-law-essentials/blob/07d960bbb82e54526a41ab89365791105914afb3/docs/LAW-CONDITIONAL-SHADOW-COMPONENT-REPLAY-20261126.md)). Cache only exactly equivalent joint boundary matrices, preserving their sign, scale, source and basis. The finite nonnegative counting law does not establish an automatic polynomial-size representation of these signed operators.

## 6. External null-cone research: scope decision

Reviewed the original [arXiv:2611.34924v1](https://arxiv.org/html/2611.34924v1), section 3.6 and appendix E.1-E.2, and the public [NULLCONE-QG-CERT-1.0](https://github.com/lluiseriksson/null-cone-quantum-gravity-certificates) Lean and Python sources. Section 3.6 explicitly matches overlap frames and cancels opposite boundary charges; appendix E assumes invariance under changing cuts, positivity, factorization and finite energy-band amplitudes. These are useful design parallels, not proven SU(2) gluing bounds. Lean theorem 18 checks a two-component Gram kernel quadratic identity, and theorem 16 cancels a positive scale under supplied spectral premises. Neither supplies our needed nonflat positivity or locality estimate. The external Python source uses fractions.Fraction and JSON, which violate our stricter proof-tree language gate; no source is imported and its suite was not executed. Our compensated assembly and KKT congruence above are independently derived finite algebraic facts, not consequences of the proposed gravitational quantization.

## 7. Next gate

Construct the full signed rational mixed second-jet stencil on the primitive cell, certify the charged and neutral tangent charts, and perform threshold inertia tests at c=1/2 in the 200 symmetry representatives with exact or outward integer arithmetic. The finite fixture is not yet a true minimizer; prove or enclose a nearby stationary solution separately. Then address all-background local patch positivity, minimizer-angle transfer, weighted background locality, scale iteration and continuum. Original review 12 cross-implementation remains pending on receipt of its adversarial arrays. No claim of uniform coercivity or continuum mass gap.

[Fixture](FIXTURE-YM4-VOL14D3F-RATIONAL-STAGGERED-20261126.txt) · [Sealed expectations](EXPECTED-YM4-VOL14D3F-RATIONAL-SHADOW-GLUING-20261126.hbp) · [Rational checker](../../tests/ym4_vol14d3f_rational_fixture.py) · [Gluing checker](../../tests/ym4_vol14d3f_signed_gluing.py) · [Expected receipt](YM4-VOL14D3F-RATIONAL-SHADOW-GLUING-20261126.hbp).
