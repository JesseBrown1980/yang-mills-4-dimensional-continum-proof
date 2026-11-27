# VOL14-D3G — keyed neutral curl certificate, local stationary enclosure and non-Abelian pilots

**Status:** author-derived neutral-sector estimate and stationary existence enclosure; integer checkers locally replayed with normal and optimized Python; independent mathematical review and hosted replay pending. D3F's rational fixture and D1/D2 premises must remain pinned. The charged-sector spectral floor, full local minimum, uniform non-Abelian coercivity, minimizer-angle transfer and continuum remain OPEN. Stacked on review 13 (#137).

## 1. Keep the sector key and the whole graded matrix

The operator requested the earlier Cantor/wave architecture and a separate key for each sector. The original [YM4-05B Cantor27 experiment](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/40) used 27 selected Cantor endpoints, proved a finite Q8 full-state cycle and rejected a scalar Q-only closure. Its nonlinear update was not physical Wilson evolution. The new key scheme preserves that distinction: a measurement address is not a proof of spectral reduction.

For the D3F exactly periodic Abelian rational fields on M=4, let k in C4 x C2 x C4 x C4 and c in {0,+1,-1} specify the translation character and neutral/charged color representation. Conjugation sends (c,k) to (-c,-k). Use the lexicographic representative for neutral pairs and all plus-charged characters. There are exactly 200 representatives for 384 complex character/color sectors, including 72 neutral representatives and 128 charged ones. Assign representative i (0..199) the eight-digit middle-thirds Cantor address obtained by replacing each of its eight binary digits by 0 or 2. This gives 200 distinct positions in the 3^8=6561 grid, drawn from the 256 possible Cantor words.

The full key includes source digest, tolerance/fixture row, basis/section, color representation, translation character and Cantor address. Threshold is a separate parameter: the three trial grades 1/3,1/2,2/3 give 600 keys per fixture and 1200 across both. These grades are chosen rational spectral test thresholds, not claimed as physical sound, light or X-ray frequencies. Those modalities may be supplied as independent external probe/readout schedules with their own calibrated operators. They must not be equated to the SU(2) color directions or used to discard an unmeasured sector. This is an explicit computational realization of the sector-key request, not a recovered definition of the original all-wave architecture.

### Full-sector identity versus representative reuse (operator clarification)

Every individual sector must have its own key. The eight-digit representative schedule above is for computation reuse only. The supplemental checker assigns all 384 sectors distinct nine-digit Cantor addresses in a 3^9=19683 grid (512 possible Cantor words). Conjugate sectors retain distinct identities unless self-conjugate, and point to the same computation representative via the explicit mate map. There are 384 keys per fixture, 768 for two fixtures and 2304 when the three independent threshold grades are included. This does not increase the 200 representative computation count or assume the graded thresholds are physical wave frequencies. Original seal and receipt remain unchanged; supplemental integer check replays its separate locally measured receipt. See [full-sector checker](../../tests/ym4_vol14d3gc_full_sector_keys.py) and [supplemental receipt](YM4-VOL14D3G-FULL-SECTOR-KEYS-20261127.hbp).

## 2. Neutral signed curl factorization

Fix one of the D3F rational backgrounds and let variations be in its common Abelian i direction. Work in the tree-zero, face-zero-mean section Z. For every path i of coarse face e, let p_i be its signed fine-link incidence, t_e the incidence of the straight centre path, and w_i its positive normalized weight. Sorting the signed axis letters gives an integer plaquette filling r_i with p_i-t_e=r_i d. The checker independently reconstructs the boundary of each filling; 10473 path pairs per face, sum of integer weights W=81*24^2. This is valid for real neutral Lie variations even on a torus: the fillings are retained on the covering lattice before periodic identification.

Let P_i be the Abelian path holonomy, V=sum_i w_i P_i, g_e=(R*grad S)_e, and define real coefficients

    a_i=Re(P_i/V), b_i=g_e Im(P_i/V).

Then sum w_i a_i=1 and sum w_i b_i=0. The normalized neutral derivative is sum w_i a_i p_i. The neutral face multiplier for G=Im(conj(V) V(U')) is g_e/|V|^2. Put f=d a for a tangent variation a=T_U z and define the weighted filling map C_fill from f to all r_i f, with the path weights in its target metric. Write

    A_e=sum w_i a_i r_i,
    F_e=sum w_i b_i r_i,
    E_e=sum w_i (a_i-1) r_i.

The neutral constraint says t_e a=-A_e f. The flat constraint on the same a is L_0 a=-E f. Since T_0 z=a+R E f and the flat curl of a uniform crossing-face lift is the coarse curl copied nine times, ||d R||<=12 (coarse curl norm<=4 by the discrete Fourier symbol, or the elementary exterior gradient bound). Therefore

    ||d T_0 z|| <= (1+12||E||) ||f||.

The Wilson part is sum cos(theta_p) f_p^2. The signed multiplier part is exactly

    sum_e sum_i w_i b_i (r_i f)^2 - 2 sum_e (A_e f)(F_e f).

This follows from the second derivative of Im(conj(V) P_i exp(i p_i a t)), with the sign of the augmented action S-mu G retained. In particular the term in (t_e a)^2 vanishes because sum w_i b_i=0. Denote the symmetric plaquette matrix of this signed form by M. The checker accumulates both terms by actual displacement and primitive source row *before* absolute values. At a neutral field, R is the fixed uniform face lift in tree gauge; at each point choose mu as above. On a neutral feasible curve built by D3D's face correction, its acceleration in right exponential coordinates lies in the range of R (all commutators vanish). Because R*(grad S-DG*mu)=0, the curve's exact scalar second derivative equals this augmented form even before stationarity is established. This fact is specific to neutral curves and the face correction chart.

## 3. Integer coefficient bounds with explicit rounding budget

The two frozen rational fields use S=2^40 for their source stereographic coordinates. For computational coefficients use fixed point denominator S and round each real and imaginary component down after each product; this is integer arithmetic, not binary floating point. The source unit quaternion error in Euclidean norm is <=2/S. For a product of length k<=11 the error satisfies e_(k+1)<=(1+2/S)e_k+4/S, so e_k<=5k/S by induction, in particular <64/S. The path mean error is <=66/S including its final two floors. A four-link plaquette product error is <=20/S, and the face-gradient error is <=162*20/S, counting all 27*6 incidences. The D3A mean norm is >=7/8 and the checker verifies that the approximate squared mean denominator is >=3/4. The error in the squared mean and the real or imaginary contracted path numerator is <134/S, by the triangle inequality and the product bounds. For the exact ratio P_i/V, norm <=8/7, so the error in each fixed-point component of a_i or Im(P_i/V) after division is bounded by

    (134 + (8/7)*134)/(3/4)/S + 1/S <1024/S.

D3C gives |g_e|<=2, and the checker requires the approximate |g_e|<3. Thus the exact |b_i|<=16/7<3, and the product/division error of b_i is <65536/S (indeed the bound 3*1024 + (8/7)*3240 + 2 suffices in units 1/S). Exact and approximate |a_i|<=2.

The integer weighted absolute row witness for C_fill*C_fill gives ||C_fill||^2<=64. Fold by primitive plaquette row and displacement, preserving the correct support including periodic images. For the rounded E the product of maximum absolute row and column sums is <=(3/4000)^2. For the rounded symmetric M the maximum absolute row sum is <=28/1000. With coefficient errors eps_a=1024/S, eps_b=65536/S, Cauchy-Schwarz in the weighted path space gives

    ||E-Ehat||<=8 eps_a,
    ||M-Mhat||<=64[(1+2*2) eps_b + 2*3 eps_a].

For the second estimate use Ahat*Fhat-A*F=Ahat*(Fhat-F)+(Ahat-A)*F, and its adjoint. The checker tests the final exact integer inequalities

    ||E||<=1/1000,
    ||M||<=1/30.

For every compatible periodic repetition of each rational fixture, the complete neutral form therefore exceeds (1799/1800-1/30)*(247/250)^2 times H0; indeed 1/(1+12/1000)>247/250. Even the weaker (1799/1800)*(247/250)^2-1/30 exceeds 15/16. All 72 neutral representatives are covered analytically by this one curl inequality, without performing 72 separate dense inertia calculations. The 128 charged representatives per fixture remain OPEN. This proves a bound for the neutral chart Hessian at the rational fixture, not the full Hessian at an exact stationary point.

## 4. Exact nearby stationary existence in the Abelian chart

Use the 648-link primitive cell, neutral free variables z in the real tree-zero, face-zero-mean space with Euclidean norm <=r=1/10^7. The base rational field U0 fixes C=B(U0). Vary U0 by exp(i z), then repair each coarse mean using the common face phase arg(C_e)-arg(V_e(z)); choose the continuous branch near zero. Every path has length <=11, so the pre-repair V changes by at most 11r. The derivative of its argument along this segment is bounded by 11/(7/8-11r); the checker verifies the resulting phase correction <=13r. Every fine link changes by angle <=14r, every plaquette by <=56r. From the pinned D3F max-deficit upper bounds (385412410 and 554965836 parts per trillion), the checker proves each initial plaquette angle <1/delta_denominator-1/100000 using the lower Taylor bound on 1-cos. Thus the entire repaired ball remains below its respective tolerance and retains mean norm >=7/8.

For the repaired field, |P-P0| and |V-V0| <=154r by the path length. Both mean norms >=7/8, hence |P/V-P0/V0| <=154r*(8/7+64/49)<400r. Each g_e changes by <=162*56r by the sine Lipschitz inequality and its complete incidence count. With |g_e|<=2 this gives |b_i-b_i0|<12000r. The same weighted map bound in section 3 gives

    ||E|| <=1/1000 +8*400r <1/500,
    ||M|| <=1/30 +64*(5*12000+6*400)r <13/30.

The exact scalar Hessian of the neutral repaired chart throughout the ball is therefore bounded below relative to H0 by (1799/1800-13/30)*(125/128)^2>1/2. This uses the nonstationary neutral chart equality of section 2, not an assumption of exact stationarity. The D1 flat reference H0>=I/105 also holds on the primitive periodic quotient by lifting fields to M=4 and dividing both quadratic forms by the identical number of copies. Thus the scalar chart Hessian is >=I/210.

At the centre the gradient equals the orthogonal projection of the neutral residual grad S-DG*mu, since its face sum is zero. D3F's exact componentwise defect <=16/10^12 implies ||grad f(0)||<26*16/10^12 < r/210. Integrating the Hessian along each radial segment gives grad f(z) dot z>0 on the radius-r boundary. The continuous action attains its minimum on the closed ball; a boundary minimum is excluded by the inward radial direction, so there is an interior stationary point. Strict convexity gives uniqueness within this neutral chart ball. This is an existence enclosure, not a numerically solved exact quaternion array.

The resulting field is periodic and Abelian, and the coarse target remains the original fixed C. Translational invariance lifts stationarity from the primitive cell to the full repeated lattice. A global U(1) conjugation fixes U,C and neutral multipliers, so the charged first derivatives vanish exactly (conjugation rotating j,k by pi reverses their sign). Tree-zero stationarity extends to the root-zero fine gauge directions by the gauge invariance identity. Consequently there exists an **exact constrained-stationary SU(2) background** in each chart ball. At it the full neutral Hessian still exceeds H0/2. This does not establish local minimization in the charged directions, and the charged floor at the rational anchor still needs a separate bound and continuity transfer. The local small-field event for arbitrary random minimizers is also unresolved.

## 5. Non-Abelian pilot (exploratory only)

The author used the existing D3E JAX matrix-free implementation, shared flat reference factors, exact face repair in floating-point arithmetic and warm starts. For M=2 (exploratory below the formal M>=4 proof domain), the original coarse field in direction 0, color i, staggered along axis 1, was supplemented by direction 2, color j, staggered along axis 1, and for the three-color family by direction 3, color k, staggered along axis 0. Ratios eta=1/4,1/2,1 were tested. Amplitudes were tuned to remain below 1/30. The two indicated coarse plaquettes have nonzero quaternion product commutator (P Q-Q P), an invariant obstruction to simultaneous conjugation into the same U(1) at their basepoint. This is a genuinely non-Abelian coarse field test, not merely a rotation of the prior Abelian field.

| Candidate, eta=1 | max fine plaquette angle | relative stationarity residual | commutator norm | full-space augmented Ritz (11520 coordinates) | eigenpair residual |
|---|---:|---:|---:|---:|---:|
| Two colors | 0.03331648669 | 1.78046e-9 | 0.02960028306 | 0.57338426475 | 1.07565e-6 |
| Three colors | 0.03331639950 | 2.03814e-9 | 0.02957899234 | 0.56624065120 | 3.33635e-6 |

Both lower the measured relative eigenvalue relative to D3E's 0.6116457. These are approximate stationary witnesses and Ritz estimates, not certified lower bounds. They have not yet been replayed on M=4 or independently cross-checked. Neither a universal worst case nor a full-space local minimum is certified. Floating-point source, arrays and logs are kept outside the proof tree with the SHA inventory. The original review 12 adversarial array cross-implementation on the author operator remains pending.

## 6. Acceptance

The next expensive calculation is the 128 charged representatives per Abelian fixture, not the 72 already covered neutral representatives. Use each sector's independently keyed fixed pencil and retain conjugate coverage. Extend the numerical non-Abelian search to M=4 and tighter tolerance, then establish a proof of all-background coercivity. The Cantor key schedule provides complete bookkeeping and replay, not a physical wave unification or a general fast solver. Global constrained-minimizer regularity, interacting locality and continuum remain OPEN.

[Neutral checker](../../tests/ym4_vol14d3ga_neutral_curl.py) · [Key and enclosure checker](../../tests/ym4_vol14d3gc_sector_keys.py) · [Expected](EXPECTED-YM4-VOL14D3G-KEYED-NEUTRAL-20261127.hbp) · [Receipt](YM4-VOL14D3G-KEYED-NEUTRAL-20261127.hbp) · [Pilot inventory](../../reviews/14-D3G-NONABELIAN-PILOT-INVENTORY-20261127.md).
