# VOL14-A — Gaussian screening of straight and translated-path blocking

Status: GPT-6.2 AI-written derivation; independent mathematical review and hosted replay pending. Prediction frozen at f368055dbf8e787e95254e31474915f8141ee52f. Motivation: Claude's independent VOL13 review (24 November 2026, PR #121). All nonlinear, continuum and physical-gap obligations remain OPEN.

## 1. Model and scope

Work on a four-dimensional periodic cubic lattice, side L >= 2b, integer b >= 1, with the usual unit-spacing cochain inner products (one positive orientation per cell). Let d be the forward lattice exterior derivative, delta its adjoint, and Delta = d delta + delta d the Hodge Laplacian, componentwise the nearest-neighbor lattice Laplacian. Its nonzero eigenvalues lie in (0,16]. Delta^+ denotes its inverse on the orthogonal complement of the constant modes and zero on constants.

For the linearized free gauge field in Feynman gauge, define S(J)=<J,Delta^+ J> for a conserved zero-mean link current J. For the usual SU(2) generator normalization the Gaussian leading Wilson deficit is 3 S(J)/(2 beta). This is a coefficient of the weak-field expansion at fixed geometry, not a bound on the full Wilson expectation or its remainder. The unit plaquette coefficient is S=(1-L^(-4))/2 by coordinate symmetry of the lattice momentum sum; it tends to 1/2. No continuum limit is assumed here.

## 2. Straight-link obstruction

Let K be the oriented b by b square of unit plaquettes in one coordinate plane, and J=delta K its boundary current. There are 4b distinct boundary links, each with coefficient plus or minus one, so ||J||^2=4b. Since the positive Laplacian eigenvalues are at most 16,

$$S_{\mathrm{straight}}(b)\ge \|J\|^2/16=b/4.$$

This proves unavoidable linear growth of the Gaussian coefficient at least, uniformly in L. It implies the plaquette-matched leading proxy beta_eff/beta=1/(2 S) is at most 2/b. This proxy does not identify the coefficient in the induced action, nor prove nonlocality, strong-coupling convergence or a nonlinear flow. The exploratory values from the independent review support a perimeter asymptotic, but do not constitute a remainder bound. In particular a first-step factor near 4.6 is not a universal factor at later scales; successive quoted ratios approach 3 if S is asymptotically linear.

## 3. A translated-path averaging candidate

For a coarse site x and offset z in {0,...,b-1}^4 choose a fixed connector C_x(z) from x to x+z (coordinate order fixed, same choice at each site). For each positive coarse link from x to y=x+b e_mu, form

$$P_z(x,y)=C_x(z)\,U[x+z,y+z]\,C_y(z)^{-1}.$$

Here U is the ordered straight fine-link product. Each P_z transforms by the same endpoint gauge actions, independently of z. Average the SU(2) quaternions P_z and normalize the resulting quaternion to unit norm; at zero sum use the z=0 straight product. This is gauge covariant and measurable; the map is analytic in a neighborhood of the identity. It need not be reflection compatible or regular on arbitrary fields.

At identity the derivative of quaternion normalization in the imaginary tangent direction is the arithmetic average. To first order the connectors telescope around the coarse plaquette for each offset, and linearity permits averaging before summing. Thus the linearized plaquette current is J_avg=delta K_avg with K_avg=b^(-4) sum_z T_z K. This exact linearized identity involves a single map of span b; it does not identify the iterated ternary map with this direct average.

## 4. Uniform Gaussian bound

The cochain Hodge identity, or its Fourier symbol, gives

$$\langle\delta H,\Delta^+\delta H\rangle\le\|H\|^2$$

for any two-cochain H: the operator d Delta^+ delta on two-cochains is an orthogonal projection (use commutation with Delta and d delta + delta d = Delta). The zero modes contribute zero. Apply this with H=K_avg.

In each of the two in-plane directions the convolution of two b-point interval indicators has multiplicities 1,2,...,b,...,2,1. The sum of squares is T_b=b(2b^2+1)/3. In each of the two transverse directions there are b positions with coefficient one. Since L >= 2b there is no aliasing of the support. Consequently

$$\|K_{\mathrm{avg}}\|^2=b^2 T_b^2/b^8=(2b^2+1)^2/(9b^4).$$

Thus

$$S_{\mathrm{avg}}(b)\le (2b^2+1)^2/(9b^4)\le1.$$

For every b >= 3 the upper bound is strictly less than b/4: (2+1/b^2)^2/9 <= (2+1/9)^2/9 = 361/729 < 3/4 <= b/4. This is a scale-uniform separation of two Gaussian coefficients. The averaged upper bound tends to 4/9; the actual coefficient need not attain that bound. The statement neither proves the expected logarithmic nonlinear beta flow nor identifies a unique blocking map.

## 5. Acceptance plan and multiscale gates

- A: exact Gaussian comparison (this note). Verify the cochain projection identity and integer multiplicity formulas, then independently reconstruct.
- B: compare actual Gaussian coefficients and covariance locality for straight, translated-path, and a faithfully specified Bałaban-style block average; include transverse/longitudinal projectors and finite-volume zero modes. Do not identify a plaquette proxy with a renormalized action coefficient.
- C: prove smoothness, gauge covariance, appropriate small-field domain and derivative/remainder bounds for the selected nonlinear map; address zero normalization, reflection support and locality separately.
- D: define the scale-dependent effective action, separate relevant/marginal terms and irrelevant polymer interactions, control the background-field Hessian and the small-field Gaussian covariance uniformly. Establish coupling recursion with controlled error, not merely the one-loop prediction.
- E: propagate the large-field estimate at every scale with compatible conditioning and a summable error budget. VOL12 and VOL13 supply original-scale periodic geometry only.
- F: prove or supply the required nonperturbative physical-scale clustering input and connect to VOL07 and OS reconstruction. All eleven continuum obligations remain OPEN.

Prior work: Bałaban, Averaging operations for lattice gauge theories, CMP 98 (1985), 17–51, [DOI](https://doi.org/10.1007/BF01211042); RG I, CMP 109 (1987), 249–301 (small-field effective actions and coupling renormalization); RG II, CMP 116 (1988), 1–22 (cluster expansions); Convergent renormalization expansions, CMP 119 (1988), 243–285, [DOI](https://doi.org/10.1007/BF01217741). These are methodological inputs, with their own hypotheses and scope. The candidate above is explicitly a separate simple path-average, not a reconstruction of Bałaban's map.

[Prediction](PREDICT-YM4-VOL14-GAUSSIAN-BLOCKING-20261124.hbp) · [integer checker](../../tests/ym4_su2_vol14_gaussian_blocking.py) · [expected replay](YM4-VOL14-GAUSSIAN-BLOCKING-20261124.hbp). Checker measures convolution identities and separation arithmetic, not the full analytic Gaussian theorem or the nonlinear gauge theory.
