# YM4 VOL12 — beta-uniform SU(2) good-star radial transport lemma

**23 November 2026. Original continuous SU(2) Wilson one-link conditional, analytic proof; independent exact integer and rational quaternion controls.** This lemma applies on every original four-dimensional periodic torus L>=3 and every beta>=0 whenever *both* compared one-link exteriors meet the gauge-invariant six-staple good-star condition. It does not depend on the externally imported chessboard theorem, even-side periodic reflections, or a finite-subgroup replacement of SU(2).

## Theorem: aligned single-link total variation <1/24

Fix a positively oriented original link e and any two exterior link assignments b,b'. Let their six original three-edge staple quaternions be (s_i) and (s'_i), each in SU(2), with every pairwise inner product satisfying
\[
\langle s_i,s_j\rangle\ge1-\epsilon,\qquad
\langle s'_i,s'_j\rangle\ge1-\epsilon,\qquad
\epsilon=\frac1{16}.
\]

Write \(H=\sum_{i=1}^6s_i\), \(t=\|H\|\), \(v=H/t\), and similarly \(H',t',v'\). The exact original link-conditional Wilson measure against normalized continuous Haar is
\[
\nu_H(du)=Z_H^{-1}\exp\big(\beta\langle u,H\rangle\big)\,dh(u).
\tag{T1}
\]

All staples are unit quaternions. Expanding the squared norm of the resultant gives
\[
\boxed{36-30\epsilon=\frac{273}{8}\le t^2,(t')^2\le36.}
\tag{T2}
\]
Thus the preferred quaternion orientations \(v,v'\in SU(2)\) are well-defined. Quaternion left multiplication by \(R=v'\bar v\) is Haar-preserving and sends \(v\) to \(v'\).

For \(\beta>0\), after the orientation alignment \(u\mapsto Ru\), the two conditional distributions have exactly the same preferred quaternion direction, and their difference is solely in the radial strengths t,t'. They satisfy
\[
\boxed{\|R_\#\nu_H-\nu_{H'}\|_{\rm TV}
\le \min\left\{1,\frac32\left|\log\frac{t'}{t}\right|\right\}
\le\min\left\{1,\frac32\frac{|t-t'|}{\min(t,t')}\right\}
<\frac1{24}.}
\tag{T3}
\]
At \(\beta=0\), both conditionals are Haar and the total variation distance is zero. The bound is independent of beta and the total lattice volume.

## Direct continuous SU(2) Haar radial proof

By Haar invariance, rotate a preferred direction to identity. SU(2) is the unit three-sphere, and for \(x=\mathrm{Re}(u)\in[-1,1]\) the normalized Haar pushforward has density proportional to \(\sqrt{1-x^2}\). Set \(z=1-x\in[0,2]\); the one-link Wilson density becomes
\[
p_\kappa(z)=\frac{\sqrt{z(2-z)}e^{-\kappa z}}{\int_0^2\sqrt{w(2-w)}e^{-\kappa w}\,dw},
\qquad \kappa=\beta t>0.
\tag{T4}
\]

For \(w(z)=\sqrt{z(2-z)}\), integrate the derivative of \(z w(z)e^{-\kappa z}\) over [0,2]. The boundary terms vanish. Since
\[
\frac{z w'(z)}{w(z)}=\frac{1-z}{2-z}\le\frac12,
\]
we obtain the *exact inequality*
\[
0=1+\mathbb E_\kappa\frac{1-z}{2-z}
-\kappa\mathbb E_\kappa z,
\qquad
\boxed{\kappa\mathbb E_\kappa z\le\frac32.}
\tag{T5}
\]

Differentiate the normalized density:
\[
\frac{\partial p_\kappa(z)}{\partial\kappa}
=-(z-\mathbb E_\kappa z)p_\kappa(z).
\]
Because z>=0,
\[
\frac12\int_0^2\left|\frac{\partial p_\kappa}{\partial\kappa}\right|dz
=\frac12\mathbb E_\kappa|z-\mathbb E_\kappa z|
\le\mathbb E_\kappa z\le\frac{3}{2\kappa}.
\]
Integrating between \(\beta t\) and \(\beta t'\) yields
\[
\|\nu_{\beta t}-\nu_{\beta t'}\|_{\rm TV}
\le\frac32\left|\log\frac{t'}t\right|.
\]
Both radial distributions are uniform over the SU(2) two-sphere directions conditional on z; the total-variation bound for z is therefore also the full SU(2) bound after orientation alignment. This proves the first two inequalities in T3 without Bessel asymptotics or floating-point approximations.

## Exact strict 1/24 constant

From T2, \(t,t'\in[\sqrt{273/8},6]\). An entirely integer comparison proves
\[
\frac{273}{8}>\left(\frac{216}{37}\right)^2
\Longleftrightarrow
273\cdot37^2=373737>373248=8\cdot216^2.
\tag{T6}
\]
Thus \(\min(t,t')>216/37\), and
\[
\frac32\frac{|t-t'|}{\min(t,t')}
\le\frac32\left(\frac{6}{\min(t,t')}-1\right)
<\frac32\left(\frac{37}{36}-1\right)
=\frac1{24}.
\tag{T7}
\]

The independent [integer/rational quaternion checker](../../tests/ym4_vol12_good_star_radial_transport.py) reproduces the strict 489-unit integer comparison in T6, all fifteen good pair tests for six genuine rational SU(2) quaternions, a concrete Haar-preserving left-quaternion rotation, and a frustrated zero-resultant control. The source is integer-only and [receipt](YM4-VOL12-GOOD-STAR-RADIAL-TRANSPORT-20261123.hbp) is frozen.

## Quantitative route to multi-link work, with exact boundary

Each original link has exactly 18 other original links sharing one of its six plaquettes. The formal count
\[
18\cdot\frac1{24}=\frac34<1
\]
creates a **conditional contraction budget**, but only after a genuinely gauge-covariant choice of preferred orientations has been made compatible from one link to all neighboring links and across boundary replicas. The alignment R may depend on the whole exterior and need not define a periodic gauge transformation or preserve Wilson plaquettes when applied separately to many links.

The [flat-holonomy independent control](../../reviews/YM4-VOL12-INDEPENDENT-SECTOR-AND-COVARIANCE-REVIEW-20261123.md) shows why this distinction is essential: two original periodic fields can have all plaquettes flat, every bad star absent, and opposite gauge-invariant winding-loop traces. The bad-island and aligned single-link estimates alone are sufficient only for their explicitly specified one-scale geometric/local objectives.

**Next acceptance target:** construct a coherent gauge-covariant multi-link alignment/transport on a good-star collar for *contractible local Wilson observables*, quantify the additional alignment defect across neighbors, and show a genuine averaged or physical-block delta_good(b) for insertion in the exact covariance bridge. Separately certify centre/winding-sector treatment for the full original physical Hilbert space. Untwisted periodic even-side rare-island probability, arbitrary boundary physical cube, blocked measure and all eleven continuum obligations remain separately scoped and open.

**Review status:** original SU(2) one-link aligned TV <1/24 ANALYTIC, numerical comparison and quaternion fixtures independently REPLAYED, external mathematical referee for this new lemma not yet recorded. Original all-physical-sector block contraction OPEN.
