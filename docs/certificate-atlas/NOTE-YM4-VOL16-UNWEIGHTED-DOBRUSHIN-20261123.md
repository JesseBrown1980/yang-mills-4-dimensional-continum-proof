# YM4 VOL16 — original continuous SU(2) unweighted Wilson boundary-decay control under interpolating laws

**23 November 2026.** A strong-coupling (small Wilson parameter) calibration theorem for the exact original four-dimensional SU(2) Wilson cube and the arbitrary-exterior, positive interpolating boundary laws of [VOL15](NOTE-YM4-VOL15-BOUNDARY-SUFFICIENT-STATISTIC-20261123.md). This is **unweighted spatial influence decay**: the distance exponent comes from the original local interaction graph, rather than choosing a source-weighted metric. The derivation is a model-specific quantitative instance of the established Dobrushin comparison method; analogous strong-coupling results are known in the mathematical lattice-gauge literature. The continuum tuning and production beta=9^12 remain separate OPEN gates.

## 1. Exact original physical setting

Let Q_h={-h,...,h}^4, h>=1, b=2h+1, embedded in an original periodic L^4 torus with even L>=2b. The interior variables are **all original positive SU(2) links** e with both endpoints in Q_h; there are 4(b-1)b^3. The genuine conditional SU(2) Wilson law for any exterior eta is
\[
\mu_T^\eta(dU)\propto
\exp\left\{\beta A_{\rm int}(U)+\beta\sum_{e\in T}
\langle U_e,B_e(\eta)\rangle\right\}dH_T(U).
\tag{D1}
\]
VOL15 proved the complete exterior boundary statistic: B_e=0 except on the J-set of
\[
|J|=4(b-1)[b^3-(b-2)^3]
\tag{D2}
\]
boundary-affected internal links, each with at most three true noncommutative exterior staples. Hence \(\|B_e(\eta)\|\le3\), and \(\|B_e(\eta')-B_e(\eta)\|\le6\).

For arbitrary eta,eta', let B_e(t)=(1-t)B_e(eta)+tB_e(eta'), t∈[0,1], and denote by mu_t the positive normalized Gibbs density D1 with B(t). This includes all the **interpolating laws** which VOL15 identified as the missing physical influence target. The proof requires no periodic equilibrium estimate or good-star event under mu_t.

## 2. Original link interaction graph and single-site SU(2) influence

Define the original interior link-interaction graph G_T: two distinct internal links are adjacent if they belong to a common all-internal original Wilson plaquette. For L>=2b>=6, any two original distinct links share at most one original elementary plaquette. Each link occurs in at most six all-internal plaquettes, with three other links in each, and therefore
\[
\boxed{\deg_{G_T}(e)\le18.}\tag{D3}
\]
This includes all original orientations and noncommuting SU(2) link factors.

Conditioning on every other internal link, the single-link conditional has exact original normalized Haar density
\[
\gamma_e^t(du\mid U_{T\setminus e})
=Z_e^{-1}\exp\{\beta\langle u,H_e^t\rangle\}dh(u),
\tag{D4}
\]
where H_e^t consists of at most six unit-quaternion **interior plaquette staples** and the real-quaternion boundary field B_e(t). Replacing any one other internal link f changes at most one original plaquette staple of e, and two unit SU(2) staples differ by Euclidean norm at most 2. Thus \(\|H_e-H_e'\|\le2\) if (e,f) is a graph edge; otherwise it is zero. In addition, comparing the same U_{T\setminus e} at two boundary fields changes H_e exactly by B_e−B_e'.

For any two quaternion resultants H,H', interpolate H_s=(1-s)H+sH'. Differentiating D4 and applying the variance bound of the scalar variable \(\langle u,H'-H\rangle\in[-\|H'-H\|,\|H'-H\|]\) gives
\[
\begin{split}
\left\|\gamma_H-\gamma_{H'}\right\|_{\rm TV}
&\le \int_0^1\frac{\beta}{2}
\sqrt{\operatorname{Var}_{\gamma_{H_s}}\langle u,H'-H\rangle}\,ds\\
&\le\frac{\beta}{2}\|H'-H\|.
\end{split}\tag{D5}
\]
This is a true continuous SU(2) Haar inequality, uniform over *all* H including zero and all interpolating original SU(2) boundary actions.

Consequently each Dobrushin influence coefficient satisfies c_{ef}<=beta if e~f and zero otherwise, and the absolute row sum is bounded by
\[
\boxed{\alpha=\sup_e\sum_f c_{ef}\le18\beta.}\tag{D6}
\]

## 3. A fully physical unweighted boundary-response theorem for beta<=1/36

Assume 0<beta<=1/36, giving alpha<=1/2<1. Let \(C=(c_{ef})\) and \(D=(I-C)^{-1}=\sum_{n\ge0}C^n\). All entries are nonnegative, and \(\sup_e\sum_fD_{ef}\le(1-\alpha)^{-1}\).

Let F(U)∈[0,1] be any bounded original Wilson observable supported on a finite set of internal links \(S\), with s=|S|. Write the single-site oscillation δ_e(F)=sup_{U,U': same off e}|F(U)-F(U')|≤1, and define its true original link-graph distance from the boundary-statistic set J as
\[
d=\operatorname{dist}_{G_T}(S,J).
\tag{D7}
\]
Changing an exterior resultant B_e only affects the **one-site** conditional at e and, by D5, the direct TV discrepancy is b_e<=beta\|B_e(eta')-B_e(eta)\|/2<=3beta on J, zero elsewhere.

By Dobrushin's comparison theorem, or by a coupled single-site Gibbs heat-bath construction with maximal SU(2) couplings, the two genuine conditional original SU(2) Gibbs measures satisfy
\[
\left|\mathbb E_{\mu_T^\eta}F-\mathbb E_{\mu_T^{\eta'}}F\right|
\le\sum_{i\in S}\delta_i(F)\sum_{j\in J}D_{ij}b_j.
\]
Every graph walk connecting i to J has length at least d, so \(\sum_{j\in J}D_{ij}\le\sum_{n\ge d}\alpha^n=\alpha^d/(1-\alpha)\). This proves the **unweighted, boundary-uniform, finite-volume Wilson-source decay**
\[
\boxed{
\left|\mathbb E_{\mu_T^\eta}F-
\mathbb E_{\mu_T^{\eta'}}F\right|
\le s\frac{3\beta}{1-18\beta}(18\beta)^d
\le\frac{s}{6}\,2^{-d},
\qquad0<\beta\le1/36.
}
\tag{D8}
\]
The second inequality uses monotonicity in beta and evaluates at beta=1/36. The result holds for **arbitrary eta,eta'**, independent of periodic equilibrium probabilities. It also holds uniformly in t for the actual interpolating SU(2) Wilson family mu_t.

Each adjacency in the original link-interaction graph changes the link base coordinate by Manhattan distance at most 2. The boundary-affected links have base coordinate \(\ell_1\) distance at least h. Thus when the source links have base coordinates with \(\|x\|_1\le r_0<h\),
\[
\boxed{d\ge\left\lceil\frac{h-r_0}{2}\right\rceil.}\tag{D9}
\]
This makes the **physical lattice buffer explicit** without an artificially imposed spatial weight:
\[
\left|\mathbb E_{\mu_T^\eta}F-
\mathbb E_{\mu_T^{\eta'}}F\right|
\le \frac{s}{6}\;2^{-\lceil(h-r_0)/2\rceil}.
\tag{D10}
\]
D9 is a safe coordinate-to-interaction-distance lower bound, not necessarily the sharp graph distance.

## 4. Exact interpolating-law covariance susceptibility

More strongly, for the interpolation B(t), the one-site direct discrepancy under B(t+dt)−B(t) is <=(beta/2)\|\Delta B_j\||dt|. The Dobrushin comparison formula, divided by |dt|, gives
\[
\left|\frac{d}{dt}\mathbb E_{\mu_t}F\right|
\le\frac{\beta}{2}\sum_{i\in S}\delta_i(F)\sum_{j\in J}D_{ij}\|\Delta B_j\|.
\tag{D11}
\]
Because \(\|\Delta B_j\|\le6\), the full source-boundary susceptibility satisfies
\[
\boxed{
\left|\beta\sum_{j\in J}
\operatorname{Cov}_{\mu_t}
\left(F,\langle U_j,\Delta B_j\rangle\right)\right|
\le\frac{3\beta s}{1-18\beta}(18\beta)^d
\le\frac{s}{6}\,2^{-d}.
}
\tag{D12}
\]
This is an actual **uniform-in-interpolation** bound on the *signed aggregate* physically located response. It avoids the otherwise extensive O(b^3) term count by using the Dobrushin resolvent row sums. By varying only one B_j at a time, the same comparison also bounds each individual covariance by
\[
\left|\operatorname{Cov}_{\mu_t}(F,\langle U_j,\Delta B_j\rangle)\right|
\le\frac{\|\Delta B_j\|}{2}\sum_{i\in S}\delta_i(F)D_{ij}.
\tag{D13}
\]
D12 does **not** claim the sum of absolute individual covariances is small for arbitrary sign choices; each actual direction vector \(\Delta B_j\) is part of the bound. The integrated response D8 is the main physical source statement.

## 5. Exact integer original 4D controls, positive and negative

The [strict integer-only original-link checker](../../tests/ym4_vol16_dobrushin_control.py) computes the original internal link interaction graph by enumerating **every one of the 6b²(b−1)² original all-internal plaquettes** for b=3,5,7. It verifies:

- Every original link has graph degree<=18; every distinct pair of internal links shares at most one original Wilson plaquette. The checker counts the complete original 4-link plaquette cliques, not a generic abstract 18-regular graph.
- The exact original boundary affected set J has \(4(b-1)[b^3-(b-2)^3]\) links. Multi-source graph BFS computes the *actual* distance to J, and central original link sources satisfy D9.
- At beta=1/36, the exact Dobrushin arithmetic is α<=1/2, b_max<=1/12 and b_max/(1−α)<=1/6; all integer cross-products pass.
- At beta=9^12, the same raw uniform influence row bound is **far greater than one** and must fail the Dobrushin acceptance gate. This negative control prevents any false promotion of the strong-coupling theorem to the production beta.

The analytic SU(2) single-link Haar step D5 and the Dobrushin comparison theorem are stated and sourced separately from the integer graph checker.

## 6. Status, novelty, and the actual continuum research gate

This establishes a **genuine, physically unweighted, arbitrary-boundary, uniform-in-interpolation original SU(2) Wilson-source influence theorem** at beta<=1/36. The result is a *model-specific exact numerical calibration* of established strong-coupling Dobrushin comparison theory, not a discovery of a new strong-coupling mechanism. Historical strong-coupling gauge work includes Osterwalder–Seiler (Ann. Phys. 110, 1978, pp. 440–471), and comparison estimates for Gibbs measures are classical.

At the production research beta=9^12 the hypothesis α<1 is not certified: the coarse uniform 18beta influence bound is enormous. The previous VOL12–15 low-curvature/multi-link frame calculations and source-weighted gauge-orbit bounds still provide a separate possible path to *typical-environment* contraction, but they do not supply the boundary-uniform high-beta covariance statement D12. A physically relevant next result must control the **interpolated laws** and a real beta(a) continuum trajectory in a stronger, gauge-covariant norm, or build a renormalized block comparison that survives the very large bare Wilson beta.

**Acceptance:** D1–D13 analytic original SU(2) finite-volume theorem at 0<beta<=1/36, independent original 4D graph/geometry and exact rational verifier pending hosted workflow. All-Gauss-sector high-beta mass gap and original 11 continuum construction obligations OPEN. [Physical next acceptance issue #116](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/116).
