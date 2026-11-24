# YM4 VOL13 — Gibbs-averaged SU(2) rooted-chord certificate and a contractible Wilson-source coupling

**23 November 2026. Original continuous SU(2) Wilson measure.** Analytical probability and group-geometry theorem with an exact integer/noncommutative-quaternion falsifier; any hosted verification status must be read from CI. Extends the general [VOL13 nonabelian tree-chord theorem](NOTE-YM4-VOL13-NONABELIAN-TREE-CHORD-20261123.md) and the [VOL12 single-link radial lemma](NOTE-YM4-VOL12-GOOD-STAR-RADIAL-TRANSPORT-20261123.md).

## 1. The canonical axial tree and an exact short plaquette strip

Take an original link-field configuration on the periodic four-dimensional torus of side L>=2b, with integer cube Q_b={0,...,b-1}^4 and b>=2. Include original **internal** positive links e=(x,mu) with x_mu<b-1. Use the coordinate-ordered site spanning tree T whose root-to-x path first moves x_0 steps in direction 0, then x_1 in direction 1, and so on through direction 3.

For any internal edge e=(x,mu), the rooted fundamental cycle P(x) e P(x+mu)^(-1) can be transformed to the trivial path with exactly
\[
\boxed{n_e=\sum_{\nu>\mu}x_\nu\le3(b-1)}
\tag{GC1}
\]
adjacent direction swaps. Each swap inserts one of the **original** elementary Wilson plaquette holonomies, conjugated by preceding path segments. It follows for *every* SU(2) link field U, using only the bi-invariant quaternion chordal norm and the triangle inequality,
\[
\boxed{\|C_U(e)-I\|\le\sum_{p\in\mathcal S_e}\|U_p-I\|,}
\tag{GC2}
\]
where S_e is the canonical strip of n_e original plaquettes. Tree edges have n_e=0 and C_U(e)=I exactly. The reduced cycle has length 2n_e+2 (including canceling double-back edges when n_e=0).

The cube has V=b^4 sites, E=4(b-1)b^3 internal original positive links, precisely
\[
N_{\mathrm{chord}}=E-V+1=3b^4-4b^3+1,
\quad
\sum_{e\in E}n_e=3b^3(b-1)^2.
\tag{GC3}
\]
These are *exact* four-dimensional lattice counts; no winding cycles occur inside this contractible box.

## 2. An unconditional Gibbs-averaged chord mismatch theorem for original Wilson links

Let mu_beta,L be the original continuous SU(2) periodic Wilson Gibbs measure at beta>=1. The previously accepted [VOL09 finite-volume bound](NOTE-YM4-VOL09-PERIODIC-GOOD-STAR-FREQUENCY-20261122.md) is
\[
\mathbb E(1-W_p)\le R(\beta)
=\frac1\beta+\frac4{3\beta}\log(1536\beta^{3/2}).
\]
For SU(2), \(\|U_p-I\|^2=2(1-W_p)\). Jensen and (GC2) therefore give
\[
\boxed{\mathbb E_{\mu}\|C_U(e)-I\|\le n_e\sqrt{2R(\beta)}.}
\tag{GC4}
\]
For any coupling of U,V **whose two full configurations each have the original mu_beta,L marginal**, and any fixed common root conjugator c, the nonabelian frame mismatch of [VOL13 G6](NOTE-YM4-VOL13-NONABELIAN-TREE-CHORD-20261123.md) consequently satisfies
\[
\boxed{\mathbb E\delta_e(U,V;c)\le2n_e\sqrt{2R(\beta)}.}
\tag{GC5}
\]
This is an actual **Gibbs-averaged rooted-cycle mismatch bound**; it uses genuine SU(2) Wilson equilibrium, not an independence or product-measure approximation. It even holds for an adversarial coupling, as long as the two marginals are correct, because the proof bounds each root cycle relative to identity separately.

## 3. Stronger model-specific input: preferred six-staple directions

For each original link e, let s_1,...,s_6 be its exterior-dependent SU(2) Wilson staples, let H_e=sum_i s_i, and define \(v_e=H_e/\|H_e\|\) whenever H_e is nonzero (a fixed measurable SU(2) fallback if H_e=0, which necessarily lies outside the good-star event). On a good star at epsilon=1/16,
\[
t_e^2=\|H_e\|^2\ge273/8>(216/37)^2.
\]
From [VOL12 radial Haar integration by parts](NOTE-YM4-VOL12-GOOD-STAR-RADIAL-TRANSPORT-20261123.md), conditional on the other original links,
\[
\mathbb E(\|U_e-v_e\|^2\mid U_{e^c})\le 3/(\beta t_e)
<37/(72\beta)
\quad\text{on a good star}.
\tag{GC6}
\]

For beta>=9^6, epsilon=1/16 and **even untwisted periodic L>=4**, the SHA-pinned and independently Lean-kernel-rebuilt external chessboard theorem and our VOL12 4D union argument yield \(\Pr(B_e)\le\rho<2^{-663}\). Since squared chordal distance between SU(2) quaternions is at most 4, integrating (GC6) across all original Gibbs exteriors proves
\[
\boxed{\mathbb E\|U_e-v_e\|^2
\le \frac{37}{72\beta}+4\cdot2^{-663}=:m_\beta^2.}
\tag{GC7}
\]
Here the fallback at H_e=0 is used only on the bad-star event; the preferred-direction map is gauge-covariant wherever H_e is nonzero.

The norm of a fundamental rooted loop is invariant under conjugation by its initial coordinate-prefix transport. Its shortened, 2n_e+2-edge representative therefore gives
\[
\mathbb E\|C_v(e)-I\|\le
n_e\sqrt{2R(\beta)}+(2n_e+2)m_\beta.
\tag{GC8}
\]
For a pair of original Wilson Gibbs replicas U,V under *any coupling with the two required marginal laws*, the corresponding random preferred fields v=v(U), v'=v(V), and a fixed common root c,
\[
\boxed{
\mathbb E\delta_e(v,v';c)
\le D_e(\beta):=
2n_e\sqrt{2R(\beta)}+2(2n_e+2)m_\beta.
}
\tag{GC9}
\]
The bound can always be capped at the maximum possible chordal mismatch 2. It is zero for tree links by the exact tree-frame construction. A global expected-residual budget follows, without an independence assumption:
\[
\sum_{e\in E}\mathbb E\delta_e(v,v';c)
\le(2\sqrt{2R}+4m_\beta)\,3b^3(b-1)^2
+4m_\beta(3b^4-4b^3+1).
\tag{GC10}
\]
GC10 remains extensive as b grows; it is not a uniform full-cube contraction theorem.

## 4. Strict integer-only milestones and the meaning of the 18-neighbor number

For beta=9^k, VOL09 gives \(R(9^k)<(35+18k)/(3\cdot9^k)\). Define s_beta=sqrt(2R). The [integer verifier](../../tests/ym4_vol13_averaged_gibbs_chord.py) proves strict rational upper bounds using cross-products with no floating-point calculations:

| k | beta | upper bound for s_beta | upper bound for m_beta |
|---|---:|---:|---:|
| 6 | 9^6 | 1/74 | 1/1000 |
| 9 | 9^9 | 1/1700 | 1/27000 |
| 12 | 9^12 | 1/40000 | 1/700000 |

For beta=9^12 and b=81, every chord has n_e<=240 and the conservative upper envelope is
\[
\boxed{
\mathbb E\delta_e(v,v')<
\frac{480}{40000}+\frac{964}{700000}
=\frac{11705}{875000}<\frac1{36}.
}
\tag{GC11}
\]
(The 11705/875000 fraction equals 0.013377142857... and is a convenience representation of the exact rational envelope.)

The VOL13 pointwise aligned *one-link* kernel bound on the good-good event was
\(W_{1,d_*}<1/24+\delta_e/2\). Off the good-good event we use its maximum 1 and \(\Pr(\text{one bad})\le2\rho\). Averaging the pointwise comparison over two original Wilson replicas yields the **numerical averaged single-link kernel budget**
\[
\boxed{
\mathbb E W_{1,d_*}(\text{tree-gauge-aligned single-link kernels})
<\frac1{24}+\frac12D_e+2\rho.
}
\tag{GC12}
\]
In particular, at k=12,b=81, the original 18-link-neighbor *arithmetic comparison* satisfies
\[
18\left(\frac1{24}+\frac{11705}{1750000}
+2\cdot2^{-663}\right)<1.
\tag{GC13}
\]
The quantity averaged in GC12 depends on random preferred-frame fields obtained from two **complete equilibrium samples**. It is **not** a sup-over-boundaries Dobrushin influence coefficient, nor a coupling of all *joint* conditional interior Gibbs measures. The candidate averaged local budget at beta=9^9,b=27 fails this stringent threshold under our conservative envelope; the integer verifier deliberately checks this negative case.

## 5. A separately completed source-specific averaged boundary coupling

A useful direct result for gauge-invariant *contractible Wilson loop sources* avoids any frame-selection ambiguity. Suppose a closed contractible loop gamma in the original interior has an explicit oriented filling by A elementary plaquettes, counted with multiplicity. Nonabelian lattice Stokes rewriting and Cauchy–Schwarz give, configuration by configuration,
\[
1-W_\gamma \le A\sum_{p\in\Sigma_\gamma}(1-W_p).
\]
Therefore under the original periodic Gibbs law
\[
\mathbb E(1-W_\gamma)\le A^2R(\beta).
\tag{GC14}
\]
For the bounded physical Wilson source \(f_\gamma=(1+W_\gamma)/2\in[0,1]\) and any actual Gibbs exterior marginal lambda with a collar containing the source links, choose the **independent** coupling of two conditional interiors mu^eta and mu^eta'. Averaging over independent eta,eta' gives two genuine complete Wilson Gibbs samples. By \(|f(U)-f(V)|\le(1-f(U))+(1-f(V))\),
\[
\boxed{
\mathbb E_{\eta,\eta'}W_1(f_{\gamma\#}\mu^\eta,f_{\gamma\#}\mu^{\eta'})
\le \min\{1,A^2R(\beta)\}.
}
\tag{GC15}
\]
The same independent coupling gives a valid **good-good restricted** term in VOL12's decomposition with \(\delta_{\rm good}(b)\le\min(1,A^2R(\beta))\) for this one named source. In fact GC15 gives the sharper full boundary-averaged inequality without adding the bad-island penalty. The covariance interface then yields
\[
8|\operatorname{Cov}(f_\gamma,g_{\rm ext})|^2\le A^2R(\beta)
\]
for any bounded exterior-measurable g_ext in [0,1].

**Crucial acceptance distinction:** GC15 is a rigorously obtained **fixed-source averaged boundary coupling**, uniform in finite periodic volume. Because the right side need not decay with source–boundary separation, because an extensive A can overwhelm R, and because the bound reflects near-identity concentration of unrenormalized Wilson traces, it does **not** yield a physical mass-gap/correlation-length bound or a full all-Gauss-sector coupling.

## 6. Scope, audit and next acceptance

- Actual original SU(2) equilibrium averaged link/chord bounds GC4–GC5: ANALYTIC, using the independently derived VOL09 periodic R(beta).
- Preferred six-staple chord bound GC6–GC10: ANALYTIC with the accepted external even-torus chessboard theorem as a stated input; the conditional Haar radial lemma is from VOL12.
- Coordinate-tree exact strip and 4D face counts: EXACT INTEGER / noncommuting quaternion local replay, hosted CI separately tracked.
- Source-specific averaged contractible Wilson loop boundary coupling GC14–GC15: ANALYTIC, uniform in periodic finite volume L>=3, with the original Gibbs disintegration.
- Quantified k=12,b=81 one-link **averaged** candidate 18-neighbor budget: RATIONAL CROSS-PRODUCT; no inference to the full Gibbs Dobrushin–Shlosman physical-cube criterion.
- Gauge-covariant **joint multi-link** collar transport, boundary-uniform contraction, physical-scaling trajectory, all Gauss sectors, blocked-measure pushforward, continuum Wilson field and all original 11 continuum obligations: OPEN.

**Next mathematical target:** replace the extensive GC10 sum by a spatially decaying, gauge-invariant, source-localized estimate for the actual joint Gibbs conditional coupling, with explicit behavior under \(\beta(a)\), \(b(a)\) and the block map. [Issue #115](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/115). Keep these source-linked candidates staged until final outside review and full static 3D atlas synchronization.
