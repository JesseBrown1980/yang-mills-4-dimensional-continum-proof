# YM4-VOL15 — exact original SU(2) centered-collar boundary response and gauge-neutrality criterion

**23 November 2026.** A direct next mathematical acceptance interface following the [VOL14 centered source and joint Gibbs orbit coupling](NOTE-YM4-VOL14-CENTERED-SOURCE-COLLAR-20261123.md). This note uses original *continuous* SU(2) Wilson links, physical plaquettes, normalized Haar and Gibbs disintegration. Noncommuting Q8 original-link configurations are used solely as exact integer geometric falsifiers.

## 1. The exact Wilson boundary blanket in a centered original four-dimensional cube

Fix b=2h+1>=3, original periodic even L>=2b, and centered original site cube \(Q_h=\{-h,\ldots,h\}^4\). Let T be its complete set of **internal original positively oriented links** with both endpoints in Q_h. Every original plaquette falls into precisely one of three categories:

\[
\begin{array}{rll}
\mathcal P_{\mathrm{int}}:&4\text{ of its 4 links in T},&
\#\mathcal P_{\mathrm{int}}=6b^2(b-1)^2,\\
\mathcal P_\partial:&1\text{ of its 4 links in T},&
\#\mathcal P_\partial=24b^2(b-1),\\
\mathcal P_{\mathrm{ext}}:&0\text{ of its 4 links in T}.&
\end{array}
\tag{BR1}
\]
No original Wilson plaquette has 2 or 3 links in T. This count includes both lower/upper faces in all four axes and every original orientation; it holds in the periodic torus for every L>=2b.

The exact geometry follows by counting 6 plaquettes per original link: there are \(4(b-1)b^3\) internal links, so \(24(b-1)b^3\) link-plaquette incidences. Every one of \(6b^2(b-1)^2\) interior plaquettes consumes four incidences, leaving
\[
24(b-1)b^3-4\cdot6b^2(b-1)^2=24b^2(b-1)
\]
boundary plaquettes, each with one original internal link. The [full original plaquette enumerator](../../tests/ym4_vol15_boundary_response.py) replays the exact count on b=3/L=6 and b=5/L=10, using all six original plane orientations and all original positive links.

For a source supported at lattice distance at most r0 from the center, any boundary plaquette touching T lies at coordinate distance at least h in its internal-link base point. Thus the geometric source-to-boundary buffer is h-r0.

## 2. Original conditional Wilson action and an exact source-response derivative

Let \(U_T\) be the genuine original SU(2) internal link configuration and \(\eta\) the complement. The exact original conditional law under any exterior \(\eta\) is
\[
\mu_T^\eta(dU)=Z_\eta^{-1}
\exp\{\beta[A_{\mathrm{int}}(U)+A_\partial(U,\eta)]\}\,dH_T(U),
\tag{BR2}
\]
where
\[
A_{\mathrm{int}}(U)=\sum_{p\in\mathcal P_{\rm int}}\tfrac12\operatorname{Tr}U_p,\qquad
A_\partial(U,\eta)=\sum_{p\in\mathcal P_\partial}\tfrac12\operatorname{Tr}U_p(U,\eta).
\]
All plaquettes in \(\mathcal P_{\rm ext}\) cancel from the conditional normalization. Every original boundary plaquette has precisely **one** internal SU(2) link, making BR2 a concrete one-link-staple boundary source.

For two arbitrary exterior assignments \(\eta,\eta'\), define \(\Delta A(U):=A_\partial(U,\eta')-A_\partial(U,\eta)\) and the finite-dimensional positive interpolation
\[
\mu_t(dU)=
\frac{\exp\{\beta[A_{\mathrm{int}}(U)+A_\partial(U,\eta)+t\Delta A(U)]\}}
{\int\exp\{\beta[A_{\mathrm{int}}+A_\partial(\cdot,\eta)+t\Delta A]\}\,dH_T}\,dH_T(U),
\quad 0\le t\le1.
\tag{BR3}
\]
The end points are exactly the two original Wilson conditional laws. For every bounded internal gauge-invariant Wilson source F, differentiation under the finite-dimensional Haar integral (compact SU(2) and bounded action) yields the **exact boundary-response identity**
\[
\boxed{
\frac{d}{dt}\mathbb E_{\mu_t}F
=\beta\operatorname{Cov}_{\mu_t}(F,\Delta A)
=\beta\sum_{p\in\mathcal P_\partial}
\operatorname{Cov}_{\mu_t}
\left(F,W_p(U,\eta')-W_p(U,\eta)\right).
}
\tag{BR4}
\]
Consequently,
\[
\boxed{
\bigl|\mathbb E_{\mu_T^{\eta'}}F-\mathbb E_{\mu_T^\eta}F\bigr|
\le\beta
\sum_{p\in\mathcal P_\partial}\int_0^1
\left|\operatorname{Cov}_{\mu_t}
(F,W_p^{\eta'}-W_p^\eta)\right|\,dt.
}
\tag{BR5}
\]
BR5 identifies the **specific, physically located correlation term** whose decay with the source-to-boundary buffer h-r0 would certify actual one-cube influence decay.

A quantitative next theorem, with explicit constants depending on physical source normalization, would be a bound
\[
\sup_{\eta,\eta',\,0\le t\le1}
\left|\operatorname{Cov}_{\mu_t}
(F,W_p^{\eta'}-W_p^\eta)\right|
\le A_F(\beta,b)\,e^{-\kappa(\beta)(h-r_0)}
\tag{BR6-TARGET}
\]
for all boundary plaquettes, strong enough for
\[
\beta\,24b^2(b-1)\,A_F(\beta,b)e^{-\kappa(\beta)(h-r_0)}
\]
to contract along the required physical continuum scaling. BR6 is the **new explicit acceptance obligation**, not an accepted bound.

The measures \(\mu_t\) with 0<t<1 interpolate the boundary actions; they need not be the original single-exterior Wilson Gibbs laws. Therefore the previous periodic-equilibrium VOL09/VOL12 estimates cannot automatically be inserted under \(\mu_t\). A valid physical proof must control these interpolating measures or use a different comparison argument preserving its hypotheses.

## 3. Exact boundary gauge-neutrality positive control

Let \(g_x\in SU(2)\) be any periodic site gauge transformation that equals identity on **every site of Q_h**, and transforms the exterior field \(\eta\) into \(\eta^g\). All original internal links are unchanged. Every boundary plaquette transforms by conjugation, so its halftrace is unchanged for every choice of internal link configuration U:
\[
\boxed{A_\partial(U,\eta^g)=A_\partial(U,\eta),
\qquad\mu_T^{\eta^g}=\mu_T^\eta.}
\tag{BR7}
\]
In particular the source response BR4 is exactly zero for these gauge-equivalent boundary assignments, **at every beta and every b**. This is a rigorous gauge-covariant zero-response class, not just a small upper bound.

The [original noncommuting SU(2) checker](../../tests/ym4_vol15_boundary_response.py) explicitly builds a genuine Q8 original Wilson field on the full L=6 and L=10 periodic tori, changes exterior links by a site-varying noncommuting SU(2) gauge that fixes the centered cube, verifies every internal original link is unchanged, and checks each boundary and interior original Wilson halftrace is exactly preserved. Its [frozen HBP](YM4-VOL15-BOUNDARY-RESPONSE-20261123.hbp) includes the original plaquette classification and gauge-neutrality result.

## 4. The size of the raw boundary-oscillation certificate

Every original SU(2) halftrace lies in [-1,1], so the boundary-action difference in BR3 obeys \(|\Delta A(U)|\le2N_\partial\), where \(N_\partial=24b^2(b-1)\). Its oscillation as U varies is at most \(4N_\partial\). A standard bounded-density reweighting inequality gives the explicit boundary-uniform total-variation bound
\[
\boxed{
\|\mu_T^\eta-\mu_T^{\eta'}\|_{\rm TV}
\le\tanh\!\bigl(\beta N_\partial\bigr).
}
\tag{BR8}
\]
For \(\beta=9^{12}\) the right side is essentially 1 even at b=3; this exact certificate supplies the **baseline** that the spatial covariance cancellation in BR5–BR6 must improve upon. The bound holds for arbitrary original exterior assignments, including frustrated exteriors.

## 5. Acceptance status and immediate continuation

- Exact original 4D SU(2) internal/mixed/exterior plaquette split BR1: ANALYTIC; integer original incidence replay b=3/5.
- Original Wilson conditional density BR2 and positive interpolation BR3: ANALYTIC.
- Source response/covariance identity BR4–BR5: EXACT finite-dimensional Wilson/Haar differentiation.
- Gauge-covariant zero-response class BR7: ANALYTIC; noncommuting original SU(2) gauge falsifier.
- Baseline arbitrary-boundary TV BR8: ANALYTIC / general probability inequality.
- **Physical buffer-dependent conditional influence BR6, physically normalized source, full continuous winding/all Gauss sectors, blocked-measure pushforward and all 11 continuum obligations: OPEN.**

Immediate next proof requirement: bound the *signed or absolute* source-to-boundary covariances in BR5 **uniformly in the interpolating boundary law and in the physical tuning**, without substituting the already-completed weighted-metric contraction for genuine spatial mixing. [Tracking issue #115](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/115).


**Independent hosted exact checker PASS — [GitHub Actions #45207141748](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/45207141748).** Checked all original SU2 periodic Wilson plaquettes on centered b=3/L=6 and b=5/L=10, exact original boundary count 24b²(b−1), every mixed plaquette with exactly one internal link, noncommuting exterior site gauge preserving interior configurations and boundary Wilson traces, frozen HBP normal/optimized equality, SHA-256 and strict no-floating-point gate. BR4–BR5 are analytical differentiation of the original continuous Wilson conditional densities; BR6 physical separation decay remains the explicitly open next acceptance target.
