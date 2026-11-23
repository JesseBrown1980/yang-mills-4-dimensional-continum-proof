# YM4 VOL13 — nonabelian SU(2) tree frames, chord holonomy, and a quantitative local Wilson transport interface

**23 November 2026 — genuine original continuous SU(2) gauge-group theorem, independently testable on a noncommuting exact quaternion subgroup.** This extends the original [centre-valued frame pilot](NOTE-YM4-VOL13-CENTER-FRAME-COCYCLE-20261123.md) and uses [VOL12's beta-uniform single-link Haar transport](NOTE-YM4-VOL12-GOOD-STAR-RADIAL-TRANSPORT-20261123.md).

## 1. Exact noncommutative gauge-frame criterion on the original 4D lattice

Let \(\Lambda_L=(\mathbb Z/L)^4\), \(L\ge3\), with the original positive oriented link set \(E\) consisting of four links per vertex: \(|E|=4L^4\). For any pair of genuine SU(2) link fields \(U=(U_{x,\mu})\), \(V=(V_{x,\mu})\), fix a connected spanning tree \(\mathsf T\) of the original nearest-neighbor site graph and a root \(o\). Let \(c\in SU(2)\) be a **specified root frame**. We seek periodic vertex frames \(g_x\in SU(2)\) satisfying
\[
V_{x,\mu}=g_x U_{x,\mu}g_{x+\hat\mu}^{-1},
\qquad g_o=c. \tag{G1}
\]

For any directed tree edge from x to y with corresponding directed link variables \(u_{xy},v_{xy}\), define the unique propagated frame
\[
\boxed{g_y=v_{xy}^{-1}g_xu_{xy}.}\tag{G2}
\]
For reversed edges use the inverses of the original positively oriented SU(2) variables. Every tree-edge equation (G1) then holds exactly, even with noncommuting variables.

Let \(P_U(x)\) and \(P_V(x)\) be ordered SU(2) products along the unique tree paths from o to x. For each non-tree positive link \(e=(x,y)\) define the **rooted fundamental cycle holonomy**
\[
C_U(e)=P_U(x)U_eP_U(y)^{-1},
\quad
C_V(e)=P_V(x)V_eP_V(y)^{-1}. \tag{G3}
\]

The propagated frames satisfy \(g_x=P_V(x)^{-1}cP_U(x)\), and their full-link compatibility obstruction is
\[
\boxed{
V_e=g_xU_eg_y^{-1}\ \Longleftrightarrow\
C_V(e)=cC_U(e)c^{-1}
\quad\text{for every non-tree }e.}\tag{G4}
\]
Tree links always satisfy G1. Consequently two arbitrary SU(2) link fields are periodic gauge-equivalent if and only if there exists **one common \(c\in SU(2)\)** that conjugates all rooted fundamental cycle holonomies simultaneously. Comparing only individual trace values or independently conjugating each cycle is insufficient. The cycle rank is exactly
\[
|E|-|V|+1=4L^4-L^4+1=3L^4+1. \tag{G5}
\]

## 2. Exact quantitative chord residual in a bi-invariant quaternion metric

Equip SU(2) with the quaternion chordal norm, which is left- and right-invariant:
\[
d_{\rm chord}(q,q')=\|q-q'\|_{\mathbb R^4}.
\]

For the unique tree frame determined by c, define the linkwise orientation mismatch
\[
\delta_e(c):=\|V_e-g_xU_eg_y^{-1}\|.
\]
For tree edges, \(\delta_e=0\). For any non-tree link, bi-invariance and G3 give the **exact identity**
\[
\boxed{\delta_e(c)=\|C_V(e)-cC_U(e)c^{-1}\|.}\tag{G6}
\]
This is a quantitative nonabelian frame-obstruction certificate, not merely a binary match test. In particular \(\delta_e(c)\in[0,2]\).

For the true original Wilson good-six-staple *preferred directions*
\[
v_e=H_e/\|H_e\|,\quad v'_e=H'_e/\|H'_e\|,
\]
apply the same tree construction with U=v and V=v'. On every link, let \(\nu_{H_e}\) and \(\nu_{H'_e}\) denote its original continuous SU(2) conditional law. Both can be compared after applying the corresponding endpoint gauge frame \(u\mapsto g_x u g_y^{-1}\). VOL12's radial theorem gives normalized Haar one-link **aligned** total variation \(<1/24\), independent of beta. A radial maximal coupling, plus Haar invariance of the angular distribution, then shows for the **bounded normalized chordal cost**
\[
d_*(u,u')=\tfrac12\|u-u'\|\in[0,1],
\]
the exact local inequality
\[
\boxed{
W_{1,d_*}\bigl((g_x\cdot g_y^{-1})_\#\nu_{H_e},\,\nu_{H'_e}\bigr)
<\frac1{24}+\frac12\delta_e(c).}
\tag{G7}
\]

**Proof of G7:** write \(u=v_eq\), with q radially distributed around the identity under an isotropic SU(2) density depending only on Re(q). The gauge-transformed sample is \((g_xv_eg_y^{-1})(g_yqg_y^{-1})\), and the matched second sample is \(v'_eq'\). The conjugate radial law of q is the same radial law since Re(q) and Haar are conjugation-invariant. Couple the two radial laws maximally: with probability at least \(1-\mathrm{TV}_{\rm radial}\), set \(q'=g_yqg_y^{-1}\), making their normalized chordal distance exactly \(\delta_e/2\); on the remaining event the cost is at most 1. Thus expected cost is at most \(\delta_e/2+\mathrm{TV}_{\rm radial}<\delta_e/2+1/24\). Infimize over all couplings to prove G7.

For tree links, G7 reduces to \(W_{1,d_*}<1/24\). For a chord it exposes **the actual orientation mismatch** as a rooted Wilson-loop discrepancy with a common root conjugator, rather than assuming that independently chosen one-link rotations compose into a gauge transformation.

This is a mathematical step toward a constructive **gauge-covariant** comparison, but a coupling of the *joint multi-link conditional laws* still requires controlling the distribution of the **endogenous** tree frames (which depend on all six staples), their chord residuals, and how their changes propagate as links are resampled. The original Dobrushin 18-neighbor threshold cannot be applied merely by summing independently aligned one-link costs.

## 3. Exact noncommuting original-SU(2) 4D controls

The [integer-only quaternion test](../../tests/ym4_vol13_nonabelian_tree_chord.py) uses the noncommuting unit quaternion subgroup \(Q_8=\{\pm1,\pm i,\pm j,\pm k\}\) as **exact genuine SU(2) test points**. It retains the complete original \(4L^4\)-link and \(6L^4\)-plaquette 4D torus incidence for L=4 and L=6.

- **Noncommuting curvature fixture:** use U_e=i on direction-0 links and U_e=j on direction-1 links, with the other directions +1. Then elementary 01-plaquettes have holonomy \(iji^{-1}j^{-1}=-1\).
- **Positive gauge reconstruction:** choose a site-varying noncommuting quaternion gauge g_x and define V_e=g_xU_eg_y^{-1}. With root c=g_o, tree frame propagation recovers every g_x exactly; all \(3L^4+1\) fundamental chord holonomy comparisons pass.
- **Global flat centre twist:** multiply V on the x_0=L−1 seam by −1 on direction-0 links, preserving *all* elementary SU(2) plaquette matrices while flipping the gauge-invariant direction-0 winding Wilson trace. The root-conjugacy chord test rejects a periodic matching gauge.
- **Local frustration red:** multiply one original V link by −1, changing at least one original plaquette Wilson trace; the chord holonomy criterion rejects it.

The code checks the equivalence of direct link mismatch and rooted cycle mismatch on **all non-tree edges**, a stronger guard than only observing one failing cycle. Its [frozen receipt](YM4-VOL13-NONABELIAN-CHORD-20261123.hbp) requires all three positive/negative results. These controls demonstrate genuine SU(2) noncommutativity in the implementation; the full general theorem G1–G7 is analytic group geometry and uses all continuous SU(2) quaternions, not a finite-group assumption.

## 4. New mathematical acceptance target

The immediate quantitative research gate is to obtain an **averaged bound** on the chord residual cost
\[
\mathbb E\bigg[\frac{1}{2}\sum_{e\in E_{\rm collar}}\delta_e(c)\bigg],
\]
under a *joint* coupling of two genuine original SU(2) Wilson interiors and an appropriate exterior-boundary law. A useful estimate must handle all \(O(b^4)\) original interior links without losing physical-size contraction, include source-sensitive gauge-invariant observables, and track winding loop holonomies and Gauss sectors.

The exact model-specific bad-star crossing term \(32b^3/18^{b+2}\) in [VOL12's covariance interface](NOTE-YM4-VOL12-AVERAGED-BOUNDARY-COUPLING-20261123.md) remains independently controlled on even periodic equilibrium tori at the cited beta threshold. The **good-collar chord residual and coherent coupling \(\delta_{\rm good}(b)\)** remain OPEN, as do the full physical-size Dobrushin–Shlosman cube, odd/twisted/arbitrary-boundary volumes, blocked pushforward, and all eleven continuum obligations.

[Next acceptance issue #115](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/115). Preserve source-linked branch status pending fresh mathematical referee and consistent 3D atlas reindexing.
