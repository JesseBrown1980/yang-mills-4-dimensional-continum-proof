# YM4 VOL14 — centered SU(2) source collar and symmetric signed-coordinate gauge frame

**23 November 2026 · Original continuous SU(2) Wilson finite-volume Gibbs theory, symmetric source-rooted four-dimensional cube.** Constructive refinement of the earlier [corner-rooted joint gauge-orbit coupling](NOTE-YM4-VOL14-WEIGHTED-ORBIT-COUPLING-20261123.md). This version gives a nonzero physical lattice buffer between the source center and **every face** of the cube. Exact group geometry is checked by a noncommuting SU(2) quaternion-subgroup program; the probability theorem is analytic and uses the original continuous SU(2) Wilson measure.

## 1. Centered original physical cube and genuine boundary separation

For integer \(h\ge1\), define the centered original site cube
\[
Q_h=\{-h,-h+1,\ldots,h\}^4,\quad b=2h+1,
\]
embedded without overlap in a periodic original Wilson torus of even side \(L\ge2b\). Let \(T_h\) be its internal original positive links \(e=(x,\mu)\) with \(x_\mu<h\), including every edge fully inside \(Q_h\). The site source root \(o=(0,0,0,0)\) has **coordinate lattice distance h** from every site-boundary face.

An original Wilson plaquette touching both \(T_h\) and its exterior contains one internal link on a boundary face. That link is based at some site with \(\|x\|_1\ge h\). Consequently a contractible source supported within an \(\ell_1\) radius \(r_0<h\) has an explicit remaining source-to-boundary lattice collar of at least \(h-r_0\). This is the geometric feature absent from the prior corner-source pilot.

Set the symmetric root-distance weight
\[
w_e=3^{-\|x\|_1}.
\]
Each source-weight is positive. The original SU(2) gauge-orbit cost for all internal link fields is
\[
\boxed{
d_h([U_T],[V_T])=\frac1{64}\inf_{g\in SU(2)^{Q_h}}
\sum_{e=(x,\mu)\in T_h}
w_e\,\frac12\|V_e-g_xU_eg_{x+\hat\mu}^{-1}\|.
}\tag{C1}
\]
It is a metric on the internal SU(2) gauge orbit quotient and takes values in \([0,1]\). Because this is an interior-only quotient, it does not identify or contract distinct global torus winding holonomies.

## 2. Noncommutative signed-coordinate rooted strips

Choose the canonical root-to-x path that first traverses coordinate 0, then 1, 2, 3, using \(\operatorname{sign}(x_\mu)\) directed original steps for a negative or positive coordinate. This defines a spanning tree of the original undirected nearest-neighbor site graph.

For every **original positive link** \(e=(x,\mu)\in T_h\), including links in negative-coordinate directions, the fundamental rooted-cycle word differs from the canonical path to \(x+\hat\mu\) by exactly
\[
n_e=\sum_{\nu>\mu}|x_\nu|
\tag{C2}
\]
adjacent swaps of orthogonal signed original steps, followed when necessary by canceling one pair of inverse \(\mu\)-steps. Each adjacent swap contributes exactly one original elementary Wilson plaquette in a conjugated or inverted orientation. Bi-invariance and Cauchy–Schwarz give the same general continuous SU(2) plaquette-strip and preferred-direction estimates as [VOL13](NOTE-YM4-VOL13-GIBBS-AVERAGED-CHORD-20261123.md), with the signed \(n_e\) in C2.

The [exact signed-coordinate checker](../../tests/ym4_vol14_centered_orbit.py) constructs arbitrary noncommuting original Q8 link values in full b=3 and b=5 cubes and, for **every internal link**, verifies:

1. The signed word reaches the correct original endpoint, with exactly \(n_e\) swaps.
2. Each swap changes the SU(2) path product by a chord distance exactly equal to an original elementary plaquette chord distance, without assuming the plaquette matrix commutes with other links.
3. The final signed word is the canonical tree path to the endpoint, after exact inverse-step cancellation where needed.
4. The squared total noncommuting chord displacement obeys the plaquette-strip Cauchy bound.

This is a substantially stronger geometry falsifier than testing the abstract cycle rank alone.

## 3. Exact source-centered geometric generating functions

For \(|x|_1=\sum_\mu|x_\mu|\) and \(q\in(0,1)\),
\[
\sum_{x\in\mathbb Z^4}q^{|x|_1}
=\left(\frac{1+q}{1-q}\right)^4,\quad
\sum_{x\in\mathbb Z^4}q^{|x|_1}
\sum_{\mu<\nu}|x_\nu|
=6\frac{2q}{(1-q)^2}
\left(\frac{1+q}{1-q}\right)^3.
\]
At \(q=1/3\), the *exact*, volume-independent bounds for every centered finite cube are
\[
\boxed{
\sum_{e\in T_h} w_e\le64,\qquad
\sum_{e\in T_h} w_e n_e\le72.
}\tag{C3}
\]
All sums extend to the infinite signed orthant with positive terms, proving the bounds for arbitrary h. The coefficient 72 counts six ordered \(\mu<\nu\) coordinate pairs. The signed-coordinate verifier independently replays these finite sums using only integer cross-products.

For integer radius \(r\ge0\), \(3^{-|x|_1}\le2^{-r}(2/3)^{|x|_1}\) when \(|x|_1\ge r\). At \(q=2/3\) the corresponding exact full signed-lattice sums are \(\sum_e w'_e\le2500\), \(\sum_e w'_e n_e\le9000\). This yields
\[
\boxed{
\sum_{\lVert x\rVert_1\ge r}w_e\le2500\,2^{-r},\quad
\sum_{\lVert x\rVert_1\ge r}w_en_e\le9000\,2^{-r}.
}\tag{C4}
\]
The decay in C4 is **induced by the declared weight**. It is not a physical unweighted covariance-decay theorem.

## 4. Genuine averaged whole-interior Gibbs orbit coupling, with a source buffer

Fix \(\beta=9^{12}\), with even periodic \(L\ge2b\). Let \(\mu_{\beta,L}\) be the actual original SU(2) Wilson Gibbs measure. As in VOL13, write \(s=\sqrt{2R(\beta)}\) and
\[
m^2=\frac{37}{72\beta}+\frac4{2^{663}}.
\]
The original Haar/Peierls/chessboard input and VOL13 preferred six-staple chord result imply for **any two complete original Gibbs replicas, under any coupling with correct marginals** that
\[
\mathbb E\delta_e(v(U),v(V))\le(2s+4m)n_e+4m.
\]
Choose the single site-gauge frame propagated from their preferred-direction link fields on the signed-coordinate tree. It aligns every preferred tree link and determines the unique rooted-cycle mismatch on each chord. By the original link-to-preferred displacement estimate and triangle inequality,
\[
\boxed{
\mathbb E\sum_{e\in T_h}w_e
\frac12\|V_e-g_xU_eg_y^{-1}\|
\le72s+336m.
}\tag{C5}
\]
After the normalization (C1),
\[
\boxed{
\mathbb E\,d_h([U_T],[V_T])
\le\frac98s+\frac{21}{4}m.
}\tag{C6}
\]
The exact integer verifier checks \(s<1/41000\), \(m<1/740000\) from original SU(2) inputs and proves the strict numerical result
\[
\boxed{\mathbb E\,d_h([U_T],[V_T])<\frac1{28000}}
\tag{C7}
\]
**uniformly for every integer h>=1 and all even L>=2(2h+1)**.

For the actual conditional joint interior laws \(\mu_T^\eta\) and \(\mu_T^{\eta'}\), take their **explicit independent conditional coupling** and independently draw exteriors from the genuine Gibbs exterior marginal \(\lambda\). The resulting full Wilson replicas have exactly \(\mu_{\beta,L}\) marginals. If \(\pi\) denotes the internal site-gauge quotient, then by the coupling characterization of Wasserstein distance,
\[
\boxed{
\mathbb E_{\eta,\eta'\sim\lambda}
W_{1,d_h}(\pi_\#\mu_T^\eta,\pi_\#\mu_T^{\eta'})
<\frac1{28000}.}
\tag{C8}
\]
This is a genuine **joint conditional interior** averaged gauge-invariant coupling for a source located h original lattice steps away from every cube face. It is explicitly weaker than the target all-Gauss-sector and physically normalized one-cube coupling.

The geometry also gives a source-rooted weighted tail for the *same* coherent preferred-field tree gauge:
\[
\begin{aligned}
\mathbb E\sum_{\|x\|_1\ge r}w_e\,
  \frac12\|V_e-g_xU_eg_y^{-1}\|
&\le2^{-r}(9000s+25500m)
<\frac{2^{-r}}3,\\
\frac1{64}\mathbb E\sum_{\|x\|_1\ge r}w_e\,
  \frac12\|V_e-g_xU_eg_y^{-1}\|
&<\frac{2^{-r}}{192}.
\end{aligned}\tag{C9}
\]
The second inequality quantifies the **weighted discrepancy beyond the genuine buffer radius h** by substituting \(r=h\). It does not bound the unweighted influence of the exterior on an interior observable.

## 5. Centered winding adverse control and next source-to-boundary theorem

For b=3 and b=5, the exact checker constructs two original even periodic SU(2) flat fields: every internal link of the centered cube is identical, so the cube's gauge-orbit cost is exactly zero, while an exterior seam carries one -I factor around a noncontractible periodic loop and reverses the gauge-invariant Polyakov trace from +2 to -2. Thus C8 cannot establish all-sector winding transport.

**Next direct physics acceptance:** derive an explicit conditional covariance/source-response estimate for a bounded gauge-invariant Wilson source supported in a radius \(r_0<h\) and the \(24b^2(b-1)\) original plaquettes coupling the internal cube to arbitrary exterior links. Prove an actual bound that decreases in the **physical buffer h-r_0**, rather than merely the preselected source weight, with adequate \(\beta(a)\) and renormalized source normalization. This is the missing step toward a physically sized, all-Gauss-sector one-cube estimate.

**Status:** centered signed-coordinate SU(2) tree/chord geometry ANALYTIC with exact noncommuting Q8 original 4D tests; actual Wilson Gibbs averaged entire-interior source-centered gauge-orbit Wasserstein C8 ANALYTIC, source-dependent on VOL09/12/13 inputs; all numerical rational comparisons exact and integer-only. Boundary-uniform physical covariance decay, winding/all-sector transfer, block pushforward and all eleven continuum obligations OPEN. [Issue #115](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/115). Pending hosted status is determined by the dedicated Actions workflow, not assumed from the local checker.
