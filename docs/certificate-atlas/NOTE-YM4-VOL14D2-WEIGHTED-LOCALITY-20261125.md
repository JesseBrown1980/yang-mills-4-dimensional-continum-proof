# VOL14-D2 — weighted local inverse and a certified complex strip

**Status:** AI-authored derivation and author-side exact integer reconstruction; hosted replay and independent mathematical review pending. Builds on VOL14-D1 (#125), including the supplied independent review 07. Scope: identity-background linearized SU(2) Wilson quadratic form, block side b=3, even periodic coarse side M>=4. No nonflat-background or physical mass-gap result.

The author-side values were sealed before the hosted checker replay at 3e3b0cdbff9657d129d1b914136425e98a58d2d2. They are not blind predictions. Numerical targets in that file are supplied independent exploratory measurements, not exact assertions.

## 1. Exact stencil construction

Use the D1 block-tree gauge and block-local independent subspace Z. Denote its orthogonal projector by P. Extend the D1 map T to the ambient 324 coordinates per block as T P. The checker constructs its rows with denominator D=1944, directly from the centred VOL14-C path derivative L. In the tree gauge the only crossing part of each L row is the uniform mean of 27 links on its own interface; that part vanishes on Z. Thus the ambient formula is P-R L P, exactly as in D1, with P eliminating tree entries and subtracting each crossing mean.

Define K=d T P. Every (mu,nu) plaquette row of K has coarse offsets contained in 0,e_mu,e_nu,e_mu+e_nu: each fine link is taken at its positive anchor, and a crossing link correction involves only its two endpoint blocks in its own direction. Differences of the four offsets have l1 norm at most two. The full ambient H=K* K has 33 nonzero offset matrices, each integral after scaling by D^2, and 525780 nonzero scalar entries across those offset matrices. The checker reconstructs the signed H coefficients, verifies adjoint symmetry and confirms this range. Restrict H to Z; on Z it is precisely the D1 Hessian. We do not invert the zero extension on Z-perp.

## 2. Sharper exact norm bounds

For a translation-invariant finite stencil A with integer coefficients scaled by D, fold the absolute values over translations into a nonnegative finite type matrix M. For each input type use the l2 norm over all coarse sites. The triangle inequality in that l2 space bounds the output type norms by M/D applied to the vector of input type norms. The same argument holds for periodic tori, even with wrapping. A strictly positive vector w satisfying M^T M w <= c D^2 w implies ||A||^2 <= c by the symmetric nonnegative weighted Schur test.

The checker builds positive integer weights by a fixed 12-step iteration and verifies the inequality by exact cross multiplication at each step. For T P the first bounds are 22,13,13; the final bound is 13. For K they are 76,59,57; the final bound is 57. Therefore, retaining the D1 lower bound,

    ||T||^2 <= 13,
    1/105 I_Z <= H|_Z <= 57 I_Z.

The condition number is at most 5985 (instead of 215040). With the corrected range two, the D1 Chebyshev ratio is now less than 39/40 because 5985 < 79^2. The covariance prefactor becomes 2*105*13=2730. For r>=1 the corresponding bound is 2730*(39/40)^floor((r-1)/2), with exponent zero at r=0.

## 3. Certified weighted inverse (real space)

Fix a target coarse block y and put W_x=(65/64)^dist(x,y), with periodic nearest-neighbour graph distance. Multiplication by this scalar on each block commutes with P. Consider H_W=W H W^(-1) on Z. It need not be self-adjoint. Its Hermitian part is H plus an error E whose (x,z) block is H_xz times (cosh(log(W_x/W_z))-1). For a stencil offset a of l1 length l, the distance triangle inequality gives |log(W_x/W_z)| <= l log(65/64). Thus E is absolutely dominated, after folding, by the symmetric nonnegative type matrix

    F_ij = sum_(a!=0) |H_a(i,j)| * (cosh(l log(65/64))-1).

Only l=1,2 occur. For general rational t=p/q>1 the exact factor is (p^l-q^l)^2/(2 p^l q^l). With denominator 2*p^2*q^2*D^2, the checker computes F and constructs a positive integer weight w with F w <= (23/4620) w. The fraction 23/4620 equals 1/105-1/220. The folded domination and weighted Schur inequality apply equally to position-dependent E because they use an entrywise envelope followed by the l2 triangle inequality. It follows that Re H_W >= (1/220) I_Z, hence ||H_W^(-1)|| <=220. This is an accretivity proof, not a small first-order perturbation in operator norm. The linear term cancels from the Hermitian part.

The range of T P is at most one. Its weighted norm and that of the adjoint are each bounded by (65/64)*sqrt(13), by the same folded domination used in section 2. Consequently the weighted covariance operator W C W^(-1), with C=T H^(-1) T*, has norm at most 220*13*(65/64)^2 <3000. Taking its (x,y) block gives the explicit volume-uniform bound

    ||C_xy|| <= 3000*(64/65)^r,  r=dist(x,y).

The normalization of the Gaussian action is (1/2)||dA||^2 as in D1. Multiply by the inverse quadratic prefactor for other normalizations. The bound holds on each compatible finite periodic torus without a periodization error. It is still loose, but the exponential rate is ln(65/64) per coarse step (about 0.0155), compared with the original ln(256/255)/4 (about 0.00098). The checker rejects 33/32 using this particular sufficient weighted test; that rejection is not proof of an actual singularity.

## 4. Certified complex strip at identity

The same estimate applies to the analytically continued Bloch symbol on the fixed Z space: H(k)=sum_a H_a exp(i k.a). Adjoint symmetry H_-a=H_a^T shows that the Hermitian part at k+i eta differs from H(k) by factors cosh(eta.a)-1. If each |eta_j| <= log(65/64), then |eta.a| <= l log(65/64). The exact F bound gives Re H(k+i eta)>=1/220 on Z for every real k, so the analytic inverse exists on this closed polystrip and has norm <=220. The real-axis floor used here holds at arbitrary real k: the D1 local curvature identities and folded norm estimates apply to Bloch phases of modulus one, or follow by density from compatible periodic momenta.

This is a full four-coordinate strip (not merely a sampled axis strip), with a rigorous though conservative width. The supplied independent numerical scan near 1.5 along axes is a different, exploratory statement. It gives a target for stronger relative form estimates or certified local inverses, but cannot be inserted as an all-coordinate strip theorem.

## 5. Multiscale implications and limits

The weighted real-space argument does not itself require translation invariance; if a nonflat-background constrained Hessian has a verified coercivity floor, a compatible local section and comparable entrywise envelopes, the same accretivity method applies. Those premises are presently OPEN. Next build background-field local Dirichlet inverses, verify uniform local nonlinear perturbation and boundary compatibility, and test a random-walk/gluing estimate. Keep the exact b=3 grouping but allow larger overlapping locality patches for the expansion. The polymer entropy issue needs its own activity bound: comparing a single propagator decay rate with a crude animal count does not settle convergence.

[Sealed expectations](EXPECTED-YM4-VOL14D2-WEIGHTED-LOCALITY-20261125.hbp) · [integer checker](../../tests/ym4_vol14d2_weighted_locality.py) · [expected replay](YM4-VOL14D2-WEIGHTED-LOCALITY-20261125.hbp) · [independent review 07](../../reviews/07-VOL14D-CALIBRATION-AND-COERCIVITY-2026-11-24.md). Sharp strip, nonflat background uniformity, induced action, per-scale large-field control and all continuum construction gates remain OPEN.
