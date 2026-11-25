# VOL14-D1 — exact linearized constrained inverse in a block-tree gauge

**Status:** AI-authored mathematical derivation, locally reconstructed integer tables, independent review and hosted replay pending. Scope: free Lie-algebra fluctuation at the identity, b=3, even periodic coarse side M>=4. This addresses the two gauge-specific gaps raised in the independent VOL14-D calibration review: the gauge degeneracy and the actual constraint L=Q-d_coarse c. Background-field uniformity, a sharp complex Bloch strip and all physical continuum obligations remain OPEN.

The expectation file is sealed before hosted replay, after local reconstruction; it is not a blind prediction.

## 1. Gauge fixing and the exact constraint

Use one Lie-algebra component at a time, with positive fine links grouped by their anchors in centred 3^4 blocks. The linearized derivative of the nonlinear VOL14-C map is L=Q-d_coarse c, as established in the VOL14-C note. Its gauge identity is L d phi = d_coarse phi|centres, where d is the fine gradient. Impose L A=0. Residual gauge gradients preserving this constraint have phi constant on coarse centres; subtract the common constant so phi is zero there.

In each block use the rooted tree consisting of coordinate-ordered shortest paths from its centre to every fine site. The paths are prefix-closed, hence form an actual tree (80 edges per block). Choose phi uniquely with phi(root)=0 to set all these tree links to zero. This is a linear gauge section, preserves L A=0 and dA, and removes precisely the residual infinitesimal gauge directions. The gauge choice need not preserve lattice rotation symmetry; it is a choice of coordinates.

For a coarse positive link from x to y=x+3 e_mu, its constraint row has 459 nonzero fine-link coefficients, l2 norm squared 277/729 and l1 norm 205/27. The 27 crossing fine links in the common interface each carry coefficient 1/27, and connectors only use internal links. The proof uses the actual weighted VOL14-C path derivative, not componentwise Q.

## 2. Exact reconstruction of fine links from curvature

Write F=dA for the linearized elementary plaquette curl. Each internal edge in the tree gauge is a sum of plaquette curls: append that edge to the coordinate-ordered tree path to its initial vertex, commute it back to the correct coordinate position by perpendicular swaps and cancel any inverse step. The difference from the tree path to its terminal vertex is the signed sum of those plaquette curls.

For an interface edge e, compare it to the central crossing edge e0 by a transverse shortest path along the interface. Each transverse step expresses the difference of the crossing links as one signed interface plaquette curl plus the difference of the two adjacent internal links. Substitute the internal formulas. Denote this difference by H_e(F). Thus A_e=A_e0+H_e(F).

The actual L row has sum of its crossing weights equal to one. Substitute the internal and crossing formulas into L A=0 and solve for A_e0. This produces one local linear curvature reconstruction S, with A=S F on the tree-gauge constrained slice.

The checker builds all 324 link row types per block (216 internal and 108 crossing). For every row it expands the curl coefficients back to fine-link coefficients and verifies the resulting equality modulo the exact tree edges and (for crossing edges) the actual L row. There are 80 zero tree rows. The common integer coefficient denominator is 1944. The raw maximum absolute row sum is 1138/81 and the maximum absolute column sum over coarse translates is 37. Thus the ordinary Schur estimate already proves ||S||^2 <= 42106/81.

A stronger integer weighted estimate folds the absolute convolution coefficients by link/plaquette type modulo 3. Let M be this finite nonnegative integer matrix, so S is dominated in block-type l2 norms by M/1944 (triangle inequality over coarse translates, each a unitary permutation). The checker constructs a strictly positive integer vector w and verifies componentwise

    M^T M w <= 105 * 1944^2 * w.

For a symmetric nonnegative matrix G this inequality gives ||G|| <= 105*1944^2: use 2 v_i v_j <= (w_j/w_i)v_i^2+(w_i/w_j)v_j^2 in its quadratic form. Consequently ||S||^2 <= 105, independent of periodic volume. This gives

$$\|A\|^2\le105\|dA\|^2$$

on the actual constrained tree-gauge section. No divergence penalty was added to the Wilson Hessian.

## 3. Local unconstrained coordinates and Hessian

Let R map a coarse link value to the constant value on its 27 crossing fine links and zero elsewhere. Then L R=I, ||R||^2=27. Let Z be the block-local vector space of tree-zero fine fields whose crossing means vanish separately at every interface. Its orthogonal projector is block local when fine links are grouped by their positive anchors. For z in Z set Tz=z-RLz. Then Tz is tree-zero and L Tz=0. Conversely for a constrained tree-zero A, subtract its crossing means to obtain z, and Tz=A. The two terms z and R L z are orthogonal.

Each L row is supported on its two endpoint blocks. A fine anchor belongs to at most eight such patches, so Cauchy-Schwarz and the row norm give ||L||^2 <= 8*277/729 <4. Therefore ||T||^2 <= 1+27*4=109, while ||Tz||^2 >= ||z||^2. The Gaussian quadratic form in the independent coordinates is

$$H=T^*d^*dT,\qquad
\frac1{105}I_Z\preceq H\preceq2048 I_Z.$$

The upper bound uses ||d^*d||<=16 from the periodic discrete Hodge Laplacian, and 16*109<2048. The linear gauge section and T have field-independent Jacobians. Thus for the quadratic action (1/2)||dA||^2 and Lebesgue measure on the gauge-fixed fluctuation coordinates, the constrained covariance is C=T H^(-1) T^*. A different Wilson normalization or beta multiplies the covariance by the inverse quadratic prefactor.

This result is volume-uniform at b=3. The eigenvalue floor concerns the stated independent coordinates and gauge section, so it is not the scalar Bloch floor reported in the review.

## 4. First rigorous coarse-distance locality estimate

Use the coarse nearest-neighbour graph distance r between anchor blocks, with periodic distance on the torus. T has range at most one coarse step, d has range at most one, and H has range at most four in the block-local Z coordinates. For a positive operator with spectrum [a,B] the degree-n Chebyshev inverse polynomial has uniform error at most (2/a) q^(n+1), q=(sqrt(B/a)-1)/(sqrt(B/a)+1). For a=1/105 and B=2048, B/a=215040<511^2, so q<255/256. This follows directly from the normalized Chebyshev residual on the interval, divided by the spectral variable.

T p_n(H) T^* has range at most 4n+2. For r>=3 choose n=floor((r-3)/4); for r<=2 use the operator norm of C. The block-to-block covariance therefore obeys the explicit uniform estimate

$$\|C_{xy}\|\le22890(255/256)^{\lfloor(r+1)/4\rfloor}.$$

Here 22890=109*210. The rate is deliberately conservative; this is a rigorous first locality certificate for the actual gauge-fixed linearized candidate at b=3, not a sharp block-scale rate or the general-b b^(-2) prefactor.

## 5. Next acceptance targets

Use the 240 independent link coordinates per block per colour (324-80-4), with a well-conditioned basis for the crossing zero-sum spaces, to construct the Bloch symbol of H. A uniform complex strip estimate and improved covariance prefactor are the next numerical/analytic acceptance gate; the reported scalar tentative floor 4 sin^2(pi/(2b)) must not be transferred to this different operator. Extend the gauge section and estimates to a nonflat small-field background with a controlled nonlinear constraint and Jacobian. At every RG scale re-establish the small-field energy/entropy and large-field estimates on the actual induced measure, rather than iterating the scale-zero geometric angle bound. These steps are still OPEN.

[Local expected rows](EXPECTED-YM4-VOL14D1-TREE-GAUGE-20261124.hbp) · [integer checker](../../tests/ym4_vol14d1_tree_gauge.py). The checker verifies the curvature reconstruction and norm arithmetic, not all background-field or nonlinear assertions.
