# YM4-04B: local connected SU(2) Wilson bounds through arbitrary ternary refinements

November 7, 2026. **Finite continuous SU(2) Wilson lattice theory: a strong-coupling local connected-correlation bound.** Verified with a prediction-first exact-integer lattice checker and the named classical Dobrushin comparison theorem. **Weak-coupling continuum induction, effective-action control, physical first gap and Clay result remain OPEN.**

This is [draft PR #37](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/37), stacked on [YM4-04A PR #36](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/36). All 19 predictions were frozen at commit ddfbbf44f539752769b6d8881a0e79fc6a119198, before the new checker. The older YM4-03 exact blocking and YM4-04A global Cauchy tests are not altered.

## 1. What is proved locally, using a named published theorem

Use the continuous SU(2) Wilson probability measure on a finite periodic four-dimensional torus of side \(L\ge2\):

\[
d\mu_{\beta,L}(U)=Z^{-1}\exp\Bigl(\beta\sum_p a_p(U)\Bigr)\prod_\ell d{\rm Haar}(U_\ell),
\qquad a_p=\tfrac12\operatorname{ReTr} U_p\in[-1,1].
\]

The standard Wilson-action constant cancels in the normalized measure. Every positively oriented link belongs to exactly **6 plaquettes**, and each such plaquette contains **3 other distinct link variables** even on size-two tori. If \(s_{ij}\) counts plaquettes involving both distinct links \(i,j\), with multiplicities, then \(\sum_{j\ne i}s_{ij}=18\).

The conditional Haar law of \(U_i\) is proportional to the exponential of its six plaquette contributions. Alter only neighboring link \(j\): the change in log conditional weight as a function of \(U_i\) has oscillation at most \(4\beta s_{ij}\), since each plaquette normalized trace is in \([-1,1]\). The elementary log-density/total-variation inequality gives

\[
C_{ij}:=\sup\|\gamma_i^\beta(\cdot|\omega)-\gamma_i^\beta(\cdot|\omega')\|_{\rm TV}
\le\tanh(\beta s_{ij})\le\beta s_{ij},
\qquad
\alpha:=\sup_i\sum_j C_{ij}\le18\beta.
\]

Here boundary conditions differ only at link \(j\). Thus the classical Dobrushin single-site comparison theorem applies whenever \(\beta<1/18\), **without depending on the total plaquette number \(N_p\)**.

**Named external theorem, not new computation:** [Rebeschini & van Handel, Comparison Theorems for Gibbs Measures, Corollary 2.6](https://web.math.princeton.edu/~rvan/dobrushin130819.pdf). For continuous compact SU(2) link spaces and local oscillations \(\delta_i(F)\), the theorem bounds a difference of Gibbs expectations by \(\sum_{i,j}\delta_i(F)D_{ij}b_j\), with \(D=\sum_{n\ge0}C^n\), provided \(\alpha<1\).

A short derivation turns this **comparison** result into a **connected covariance** result. Tilt the same finite Gibbs measure by \(e^{tG}\), where \(G\) is a bounded real local observable. The single-link conditional change has TV at most \(\tanh(|t|\delta_jG/4)\le|t|\delta_jG/4\). Divide the comparison bound by \(|t|\), send \(t\to0\), and use differentiation under the finite Wilson integral:
\[
|\operatorname{Cov}_{\mu_\beta}(F,G)|
\le\tfrac14\sum_{i,j}\delta_iF\, D_{ij}\,\delta_jG.
\]
If the positive-link supports are separated by at least \(r\) edges in the graph joining links that share plaquettes, then \((C^n)_{ij}=0\) for \(n<r\), while each remaining row sum is at most \(\alpha^n\). For normalized real Wilson loops \(|F|,|G|\le1\), the oscillations are at most 2, giving the explicit local estimate
\[
\boxed{|\operatorname{Cov}_{\mu_\beta}(F,G)|
\le |\operatorname{supp}F|\frac{\alpha^r}{1-\alpha}.}
\]
This is a genuine connected-correlation inequality for the **actual interacting SU(2) finite measure**, but it is **not** a proof of Wilson-only action closure, a complete polymer expansion or an excitation overlap.

## 2. Two factor-three blocks of the actual 4D field

Keep the exact YM4-03 map and the same geometries \(18^4\to6^4\to2^4\). Take two normalized spatial square Wilson characters at coarse temporal positions 0 and 1. Under the **actual** Haar pushforward, they are precisely the fine Wilson loops with square side \(3\) or \(9\) fine links and temporal separation \(3\) or \(9\) links. The first fine loop supports 12 positively oriented links and the second supports 36; the plaquette-link graph distances are respectively 3 and 9. A plaquette moves the base time coordinate by at most one, and a sequence of time-space plaquettes gives an explicit path achieving the bound.

Choose \(\beta_0=1/1000\), so \(\alpha_0=9/500\). This coupling is **strong**, but unlike the previous global condition, the new proof **does not require \(\beta_0 N_p\) to be small**. The integer checker confirms:

\[
|C_{\mathrm{actual},3}|
\le12\frac{(9/500)^3}{1-9/500}
=\frac{2187}{30687500}<10^{-4},
\]
\[
|C_{\mathrm{actual},9}|
\le36\frac{(9/500)^9}{1-9/500}
=\frac{3486784401}{479492187500000000000000}<10^{-14}.
\]

Define *separate Wilson-only proxies*, **not** the exact induced action, by the known leading YM4-03 coefficient:

\[
\beta_{\mathrm{proxy},1}=\beta_0^9/4^8,\qquad
\beta_{\mathrm{proxy},2}=\beta_0^{81}/4^{80}.
\]

At either proxy lattice, the one-step-separated normalized spatial plaquette pair has individual supports of four links. The same Dobrushin inequality gives
\[
|C_{\mathrm{proxy},k}|
\le\frac{4\alpha_k}{1-\alpha_k},
\qquad\alpha_k=18\beta_{\mathrm{proxy},k}.
\]
By the **exact YM4-03 pushforward equality** for the actual blocked correlations, followed by a triangle bound against these proxy correlations, we obtain the new **local absolute connected-observable comparisons**:

\[
\boxed{|C_{\mathrm{blocked},3}-C_{\mathrm{Wilson\,proxy},1}|<10^{-4},}
\quad
\boxed{|C_{\mathrm{blocked},9}-C_{\mathrm{Wilson\,proxy},2}|<10^{-14}.}
\]

The errors are on these *one specified connected Wilson-observable pair* and independent of \(N_p\). Because both individual correlations are tiny, **these absolute comparisons do not show relative accuracy of the leading Wilson coupling or the full induced action**. No full continuous SU(2) high-dimensional group integral was evaluated; these are analytic enclosures based on the named theorem.

## 3. Uniform all-k summability on a restricted, fixed-beta family

For each \(k\ge1\), set microscopic spacing \(a_k=3^{-k}\) and periodic four-dimensional site side \(2\cdot3^k\). The physical side is 2. **Keep the same fixed bare strong coupling \(\beta_0=1/1000\) at every refinement**, and take two normalized spatial Wilson loops with physical side 1, separated by physical Euclidean time 1. Each fine Wilson loop has perimeter \(4\cdot3^k\) links, and the two supports have graph distance \(3^k\).

For the actual interacting SU(2) lattice measure:
\[
A_k:=|C_{\rm actual,k}|\le
\frac{4\cdot3^k\alpha_0^{3^k}}{1-\alpha_0},
\qquad \alpha_0=9/500.
\]
Iterating only the **formal leading Wilson proxy** gives
\[
\beta_{\rm proxy,k}=\frac4{4000^{9^k}},\quad
\alpha_k=\frac{72}{4000^{9^k}},\quad
B_k:=|C_{\rm proxy,k}|\le\frac{4\alpha_k}{1-\alpha_k}.
\]
Consequently \(|C_{\rm blocked,actual,k}-C_{\rm Wilson\,proxy,k}|\le A_k+B_k\). The precise ratios obey
\[
\frac{A_{k+1}}{A_k}=3\alpha_0^{2\cdot3^k}
\le3\alpha_0^6<1/2,\qquad B_{k+1}/B_k<1/2.
\]
So **for all positive integers k**, not just the six tested examples:
\[
\boxed{\sum_{k=1}^\infty(A_k+B_k)
\le\frac{12\alpha_0^3}{(1-\alpha_0)(1-3\alpha_0^6)}
+\frac{8\alpha_1}{1-\alpha_1}<10^{-4}.}
\]
The finite integer program checks the exact rational constants and first six refinements. The infinite claim follows from the proved ratio bound, not numerical extrapolation.

**Interpretation:** this is a mathematical bound for an all-scale *fixed strong-coupling family of connected Wilson correlations*, with the same fixed physical loop size. It is **not** a normed induction for the full four-dimensional Wilson effective action. In this regime physical-size Wilson correlations are driven toward zero under refinement; nothing here constructs a nontrivial continuum theory.

## 4. Explicit failed weak-coupling gate and next obligation

At \(\beta=1/10\), the available bound is \(\alpha\le9/5>1\); at \(\beta=4\), it is \(\alpha\le72\). Therefore the **sufficient Dobrushin contraction proof no longer applies** along the physically relevant SU(2) continuum trajectory \(\beta(a)\to\infty\). That is a method failure, **not** evidence of a zero physical Yang–Mills mass gap or a phase transition.

For the actual continuum program we still need a local **gauge-invariant block specification or renormalized cluster/character expansion** with estimates valid at increasing bare coupling, including large-field control and induced nonlocal networks. We must also prove full-spectrum transfer control and the true first-state visibility, without confusing tiny observed Wilson correlations with a gap in the entire physical Hilbert space. These remain OPEN.

## Reproduction and limits

The [source checker](../tests/test_ym4_04b_local_cluster.py) verifies every plaquette incidence and shared-link multiplicity on \(2^4,3^4,6^4\), proves temporal graph distances 1,3,9 (the last by general time-coordinate argument plus explicit path), verifies all rational inequalities, tests \(k=1,\dots,6\), proves the infinite-sum comparison and runs eight deliberate red controls.

[Predictions](PREDICTION-YM4-04B-LOCAL-CLUSTER-20261107.hbp) were committed before code. [Measured hosted receipt](../tests/YM4_04B_LOCAL_CLUSTER_RECEIPT.txt) is compared byte-for-byte by [dedicated CI](../.github/workflows/ym4-04b-local-cluster.yml).

**Status:** local connected-observable estimates PASS under the stated strong-coupling and cited comparison-theorem hypotheses. The effective-action induction, weak-coupling regime, first excitation, nontrivial continuum existence and the Clay Millennium problem are not proved.
