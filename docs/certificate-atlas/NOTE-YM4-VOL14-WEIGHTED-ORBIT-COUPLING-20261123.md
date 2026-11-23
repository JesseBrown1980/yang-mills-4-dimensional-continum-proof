# YM4-VOL14 — source-anchored weighted SU(2) gauge-orbit coupling from genuine Wilson Gibbs disintegration

**23 November 2026 · Original continuous SU(2) four-dimensional Wilson gauge theory.** Mathematical analytic result, with a finite original-geometry and exact quaternion/integer falsifier. This advances the [VOL13 Gibbs-averaged chord estimates](NOTE-YM4-VOL13-GIBBS-AVERAGED-CHORD-20261123.md), which were previously extensive in box volume. The weight and the gauge-orbit quotient are explicit parts of the new result; physical unweighted correlation decay is a separate open obligation.

## 1. Entire joint interior law and a bounded gauge-invariant distance

Let the untwisted original periodic Wilson torus have even side \(L\ge2b\), \(b\ge2\), and \(\beta=9^{12}=282429536481\). Put \(Q_b=\{0,\ldots,b-1\}^4\) and let \(E_b\) contain precisely the **internal** original positive links \((x,\mu)\) with \(x_\mu<b-1\). Their endpoints are sites of \(Q_b\). Take \(T=E_b\) as the interior, and let \(\eta\) contain all other original links, including the original boundary collar. The exact Gibbs disintegration is
\[
\mu_{\beta,L}(dU_T,d\eta)=\lambda(d\eta)\,\mu_T^\eta(dU_T).
\tag{W1}
\]
The only assumption on \(\eta\) is that it is sampled from the **actual Gibbs exterior marginal**, not an adversarial boundary-uniform law.

For \(e=(x,\mu)\in E_b\), define the source-rooted weight \(w_e=3^{-\lVert x\rVert_1}\) and the SU(2)-bi-invariant normalized chordal cost \(d_*(u,v)=\tfrac12\lVert u-v\rVert_{\mathbb R^4}\in[0,1]\). Define the **full joint gauge-orbit distance**
\[
\boxed{
d_b([U_T],[V_T]):=\frac4{81}\inf_{g\in SU(2)^{Q_b}}
\sum_{(x,\mu)\in E_b}w_e\,
d_*\!\left(V_e,g_xU_eg_{x+\hat\mu}^{-1}\right).
}
\tag{W2}
\]
The group is compact, so the infimum is attained. This is a metric on the quotient of internal link fields by all cube-site SU(2) gauges (and hence a gauge-invariant pseudometric before quotient). It is symmetric and satisfies the triangle inequality by gauge-group composition and the bi-invariant chordal metric. Its range is \([0,1]\), since \(\sum_{e\in E_b}w_e\le81/4\).

The metric intentionally treats a source-corner neighborhood more strongly than links farther away. It ignores the exterior Wilson links and is therefore **not** the full physical all-Gauss-sector norm.

## 2. Exact four-dimensional geometric generating functions

Use the coordinate-ordered spanning tree rooted at \(o=(0,0,0,0)\) from [VOL13](NOTE-YM4-VOL13-GIBBS-AVERAGED-CHORD-20261123.md). For \(e=(x,\mu)\), its rooted fundamental cycle has a strip with \(n_e=\sum_{\nu>\mu}x_\nu\le3(b-1)\) original plaquettes. The finite sum can be bounded by the original positive orthant \(\mathbb N^4\), for which
\[
\sum_{x\in\mathbb N^4}q^{\lVert x\rVert_1}=(1-q)^{-4},\qquad
\sum_{x\in\mathbb N^4}q^{\lVert x\rVert_1}\sum_{\mu<\nu}x_\nu
=6q(1-q)^{-5}.
\]
At \(q=1/3\),
\[
\boxed{
\sum_{e\in E_b}w_e\le\frac{81}{4},\qquad
\sum_{e\in E_b}w_en_e\le\frac{243}{16}.}
\tag{W3}
\]
Both bounds are uniform over **all b**. Exact lattice checks for \(b=2,3,4,9\) verify the cycle rank \(3b^4-4b^3+1\), the unweighted strip area \(3b^3(b-1)^2\), and the finite generating-function inequalities.

Moreover, for any integer \(r\ge0\), on \(\lVert x\rVert_1\ge r\), \(3^{-\lVert x\rVert_1}\le2^{-r}(2/3)^{\lVert x\rVert_1}\). Substituting \(q=2/3\) gives the exact **weighted spatial tail**
\[
\boxed{
\sum_{e:\,\lVert x\rVert_1\ge r}w_en_e\le972\,2^{-r},\qquad
\sum_{e:\,\lVert x\rVert_1\ge r}w_e\le324\,2^{-r}.
}
\tag{W4}
\]
The decay in W4 is induced by the explicitly chosen metric weight. It is not an unweighted Gibbs mixing statement.

## 3. Genuine periodic Gibbs preferred-field and gauge-frame comparison

Let \(s:=\sqrt{2R(\beta)}\), with \(R\) the proven original continuous-SU(2) periodic mean plaquette deficit from VOL09. Let \(v_e(U)=H_e(U)/\lVert H_e(U)\rVert\) be the six-staple preferred direction on nonzero-resultant stars, with a fixed measurable unit-quaternion fallback for \(H_e=0\). VOL12's conditional Haar radial estimate and the independently rebuilt even-torus chessboard bad-star activity imply
\[
\mathbb E_\mu\lVert U_e-v_e(U)\rVert^2\le m^2,
\qquad
m^2:=\frac{37}{72\beta}+\frac4{2^{663}}.
\tag{W5}
\]
For **any** joint coupling of two complete original SU(2) Wilson configurations with each marginal \(\mu_{\beta,L}\), VOL13's nonabelian tree/chord theorem gives a definite site gauge frame \(g=g(v(U),v(V))\), constructed from the two preferred fields, with all tree links aligned exactly. Its chord residuals satisfy
\[
\mathbb E\delta_e(v(U),v(V))
\le(2s+4m)n_e+4m.
\tag{W6}
\]
A single gauge-frame comparison of the **actual original link fields**, with the *same* g on every link, gives the deterministic triangle estimate
\[
d_*\!\left(V_e,g_xU_eg_y^{-1}\right)
\le\tfrac12\bigl(\lVert V_e-v_e(V)\rVert
+\delta_e(v(U),v(V))
+\lVert U_e-v_e(U)\rVert\bigr).
\]
By Jensen/Cauchy–Schwarz, the two original fields have expected link-to-preferred displacement at most m. Summing W6 with W3 produces
\[
\boxed{\mathbb E\sum_{e\in E_b}w_ed_*(V_e,g_xU_eg_y^{-1})
\le\frac{243}{16}s+\frac{729}{8}m.}
\tag{W7}
\]
This is a bound on the **full joint internal link fields under one coherent gauge frame**, rather than a collection of unrelated single-link kernel couplings.

Since W2 takes the infimum over every site frame, and g from W7 is one admissible frame,
\[
\boxed{
\mathbb E\,d_b([U_T],[V_T])
\le\frac34s+\frac92m.
}
\tag{W8}
\]
This bound is independent of b and L in the stated periodic Wilson setup. An exact noncommuting Q8 gauge reconstruction is included only as a falsifier for the gauge-orbit and metric algebra; the analytic theorem uses the *continuous* original SU(2) Gibbs measure.

## 4. Strict integer acceptance, including a weighted distance tail

At \(\beta=9^{12}\), VOL09's exact rational envelope and W5 imply
\[
s<\frac1{41000},\qquad m<\frac1{740000}.
\tag{W9}
\]
The [integer-only exact verifier](../../tests/ym4_vol14_weighted_orbit.py) establishes both inequalities by cross-multiplication, including the full \(2^{-663}\) term, and then certifies
\[
\boxed{
\mathbb E\sum_e w_ed_*(V_e,g_xU_eg_y^{-1})<\frac1{2000},
\qquad
\mathbb E d_b([U_T],[V_T])<\frac1{40500}.
}
\tag{W10}
\]
The corresponding source-distance tails, for all integer \(r\ge0\), follow from W4:
\[
\begin{aligned}
\mathbb E\sum_{\lVert x\rVert_1\ge r}w_e\,\delta_e
&\le2^{-r}(1944s+5184m)<\frac{2^{-r}}{16},\\
\mathbb E\sum_{\lVert x\rVert_1\ge r}w_e\,
 d_*(V_e,g_xU_eg_y^{-1})
&\le2^{-r}(972s+2916m)<\frac{2^{-r}}{32}.
\end{aligned}
\tag{W11}
\]
These are weighted tail statements for the specific source-rooted metric and frame. They do not assert pointwise decay of the original link correlations with separation.

## 5. Completed averaged coupling of **entire conditional interior measures modulo gauge**

For **every** exterior pair \((\eta,\eta')\), choose the measurable independent coupling \(K_{\eta,\eta'}=\mu_T^\eta\otimes\mu_T^{\eta'}\) of all internal link variables, and let \(\pi\) be the quotient map to internal SU(2) gauge orbits. This is an actual, joint, measurable coupling of the full conditional interiors, without assuming probabilistic independence of the original link variables *within* either interior. It follows that
\[
W_{1,d_b}(\pi_\#\mu_T^\eta,\pi_\#\mu_T^{\eta'})
\le\mathbb E_{K_{\eta,\eta'}}d_b([U_T],[V_T]).
\]
Average over two independent actual exterior marginals \(\lambda\). Gibbs disintegration (W1) means each full configuration has exactly the original \(\mu_{\beta,L}\) marginal, so W8–W10 give
\[
\boxed{
\mathbb E_{\eta,\eta'\sim\lambda}
W_{1,d_b}(\pi_\#\mu_T^\eta,\pi_\#\mu_T^{\eta'})
<\frac1{40500},
\quad\beta=9^{12},\ L\text{ even},\ L\ge2b,\ b\ge2.
}
\tag{W12}
\]
This is a **genuine, box-uniform, gauge-invariant, joint-interior, averaged-boundary Wasserstein bound** in a precisely stated source-local metric. It requires no hypothetical good-good coupling kernel \(\delta_{\rm good}(b)\) to obtain W12, because the independent conditional coupling is constructed explicitly.

Consequently, for every bounded observable \(F\) on the interior gauge-orbit quotient with Lipschitz constant at most one for \(d_b\), its real-valued pushforward satisfies the same average W1 bound. For physical Wilson loop observables the Lipschitz constant depends on the loop's support and the source weights; it must be included explicitly before using W12.

## 6. Two exact adverse scope controls

The quaternion checker constructs a nonconstant local Q8 site gauge on each b=2 and b=3 original four-dimensional box, verifies that its transformed noncommuting SU(2) link configuration has **exactly zero** orbit distance, and verifies that flipping one original link by -I changes an original plaquette Wilson trace, hence cannot be removed by a cube-site gauge.

It also embeds the same internal cube in a periodic torus of side L=2b and compares two *flat* original SU(2) connections. They are identical on every internal cube link, so their **local orbit distance is zero**, yet a centre flip across the periodic exterior seam changes the gauge-invariant winding Polyakov trace from +2 to -2. Thus no implication from W12 to a global all-sector coupling is possible without an additional winding-holonomy estimate.

## 7. Mathematical status and immediate next physics task

**Completed at finite-periodic equilibrium scope:** explicit original Wilson interior disintegration; genuine independent conditional *joint* coupling; actual continuous-SU(2) Gibbs-averaged preferred chord control; box-uniform source-rooted gauge-orbit W1 bound W12; separately verified exact lattice/Q8 and no-float arithmetic; and an explicit induced spatial weight tail W11.

**Still OPEN:** source-to-boundary separation decay in a metric strong enough for **unweighted or physically normalized** Wilson covariance, arbitrary-boundary physical cube estimates, full winding/centre/all-Gauss-sector transport, uniform physical scaling \(\beta(a)\)/\(b(a)\), renormalized block pushforward, and all eleven original continuum obligations. W12 mostly measures near-flatness of the unrenormalized interior gauge orbit in a source-chosen metric; it is **not** an infrared mass gap or a physical correlation-length certificate.

**Next acceptance objective:** replace the imposed exponential weight by a quantitatively controlled **distance-to-boundary propagation/conditional influence estimate** for physically normalized Wilson observables, while tracking the noncommutative rooted-cycle and global winding terms. [Tracking issue #115](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/115). Keep VOL14 source-linked until formal independent mathematical audit and complete twelve-view 3D atlas consistency.
