# YM4-04A — two ternary SU(2) blocks: correlation, spectral comparison and the failed relative-precision gate

**Status (November 7, 2026):** finite four-dimensional continuous-SU(2) Wilson theory. Exact algebra and finite-measure correlation bounds **DERIVED conditional on the existing YM4-03 Theorems 1–9 and YM4-02c/d positive-transfer results**; independent small algebraic checks **MEASURED**. A relative-precision requirement **FAILS BY DESIGN** and is retained. All-scale RG control, weak-coupling trajectory, nontrivial continuum reconstruction and Clay gap **OPEN**.

The new 19-row [prediction](PREDICTION-YM4-04-TWO-TERNARY-BLOCKS-20261107.hbp) was frozen at commit \`ad79b029\` before the verifier \`tests/test_ym4_04_two_ternary_blocks.py\` existed. Two *separately pre-frozen* extensions establish (1) an absolute bound on a true **finite periodic-time** connected Wilson correlation and (2) a different **infinite-time interacting-vacuum** transfer bound: [six-row prediction](PREDICTION-YM4-04-TWO-BLOCK-CORRELATION-SUPPLEMENT-20261107.hbp) and [four-row prediction](PREDICTION-YM4-04-VACUUM-CORRELATION-SUPPLEMENT-20261107.hbp). They were frozen before their respective code changes, so neither result was retrospectively inserted into the prediction.

**Source dependency:** [YM4-03 Theorems 1–9](NOTE-YM4-03-ONE-SCALE-BLOCKING.md) in immutable Git blob \`88b441ce39c3867d4635c0ac3f3475ea5ac621dc\`; its Theorem 9 is invoked, **not reproved** by this test. [YM4-02c](LEMMA-0004-REFLECTION-TRANSFER.md) supplies positivity of the Wilson transfer, and [YM4-02d](NOTE-YM4-02d-QUANTITATIVE-GAP.md) its fixed finite-lattice ratio bound. These remain upstream hypotheses of the new spectral claims.

## 1. The actual map and our geometry

The fine periodic Euclidean lattice is \((\mathbb Z/18)^4\), the intermediate one is \((\mathbb Z/6)^4\), and the coarse lattice is \((\mathbb Z/2)^4\). Every fine positively oriented link carries an element of **continuous SU(2)**; rational unit quaternions are used to check exact algebra, *not as a finite subgroup replacement for Haar SU(2)*.

The existing YM4-03 block, for direction \(\mu\), is the ordered nonabelian product

\[
(B_3U)_\mu(x)=U_\mu(3x)U_\mu(3x+\hat\mu)U_\mu(3x+2\hat\mu).
\]

Because group multiplication is associative,

\[
B_3\circ B_3=B_9
\]

for configurations of the actual noncommutative gauge field. Gauge transformations telescope, and the coarse Wilson plaquette equals the fine \(9\times9\) rectangular Wilson loop on its boundary.

The checker constructs a sparse but nontrivial configuration of 576 exactly represented SU(2) fine links (the other fine links are the group identity), evaluates **64 coarse links and all 96 coarse plaquettes**, checks every \(\mathrm{SU}(2)\) quaternion norm and gauge covariance, and compares two \(B_3\) blocks with the direct 9-link and 36-link paths. A spatial Wilson-loop pair at **two different temporal slices** is checked as the same fine pullback. This is an exact *algebraic* test, not a numerical integral over \(18^4\) gauge configurations.

YM4-03's Haar pushforward identity applies to the **actual Wilson measure**, not only to the sparse test: for bounded gauge-invariant \(F,G\), with \(\nu_2=(B_3\circ B_3)_*\mu_{\beta_0}\),

\[
C_{\nu_2}(F,G)=C_{\mu_{\beta_0}}(F\circ B_9,G\circ B_9)
\]

*exactly*, with the same finite periodic-time expectations on both sides. This equality, valid at any Wilson coupling, uses a theorem, not a Monte Carlo estimate.

## 2. Explicit coupling proxy and a rigorous 4D error

Write \(X(U)=\sum_{p\text{ fine}}\frac12\chi_{1/2}(U_p)\), and \(N_p\) for the number of fine plaquettes. With normalized product Haar, condition on \(B_3U=V\):

\[
F_V(z)=\mathbb E_{\mathrm{Haar}}[\exp(zX)\mid B_3U=V].
\]

The normalized blocked probability density is proportional to \(F_V(\beta)\). Theorem 9 of YM4-03 (for \(b=3\)) says that all Taylor coefficients of \(F_V\) with order below 9 are independent of \(V\), and the first nonconstant coefficient is

\[
[z^9] F_V(z)=\kappa+2^{-17}\sum_{p'}\chi_{1/2}(V_{p'}).
\]

**New explicit remainder proof.** For complex \(|z|\le (4N_p)^{-1}\), the bound \(|X|\le N_p\) gives
\[
|F_V(z)-1|\le e^{1/4}-1<1/3.
\]
The analytic branch \(\log F_V(z)\) therefore exists on this disk and obeys
\[
|\log F_V(z)|\le-\log(2/3)<1/2.
\]
By Cauchy's coefficient bound, for each \(n\), the difference between the \(n\)th coefficients of \(\log F_V\) and \(\log F_{V'}\) is bounded by \((4N_p)^n\). The first configuration-dependent term still occurs at order 9 with coefficient \(2^{-17}\sum\chi\). Thus for \(0\le\beta\le(8N_p)^{-1}\),

\[
\left|\log\frac{F_V(\beta)}{F_{V'}(\beta)}
-\frac{\beta^9}{2^{17}}\left(\sum_{p'}\chi(V_{p'})-\sum_{p'}\chi(V'_{p'})\right)\right|
\le\delta,\qquad \delta=2(4N_p\beta)^{10}.
\]

This is a **global absolute log-density bound**, not a local cluster expansion. Its hypotheses include the full **finite-volume** \(N_p\). Define the **Wilson-only proxy coupling**
\[
\beta_{\mathrm{proxy},1}=\frac{\beta_0^9}{4^8}.
\]
The actual blocked four-dimensional measure has higher-order terms, potentially nonlocal. There is **no claim** that its effective action is exactly Wilson.

Our numerical choice (exact rationals throughout) is

| Quantity | Value |
|---|---:|
| Fine plaquettes | \(N_{p,0}=6\cdot18^4=629,856\) |
| Intermediate plaquettes | \(N_{p,1}=6\cdot6^4=7,776\) |
| Final plaquettes | \(N_{p,2}=6\cdot2^4=96\) |
| Bare Wilson coupling | \(\beta_0=1/20,155,392\) |
| First Wilson proxy | \(\beta_{\mathrm{proxy},1}=\beta_0^9/4^8\) |
| Second Wilson proxy | \(\beta_{\mathrm{proxy},2}=\beta_0^{81}/4^{80}\) |
| First uniform log-density oscillation bound | \(\delta_1=1/536,870,912\) |
| Second such bound, applied to the **Wilson proxy** | \(\delta_2<2^{-128}\) |

**Two blocks without assuming action closure.** Since a pointwise relative density bound is preserved under pushforward (conditional expectation of a bounded density ratio), applying the second \(B_3\) to the **actual** first blocked measure stays within a factor \(e^{\pm\delta_1}\) of blocking the first Wilson proxy. Applying the one-step Cauchy bound to that proxy gives an additional \(e^{\pm\delta_2}\) relative to the second Wilson proxy. Therefore, for \(\delta=\delta_1+\delta_2\),

\[
e^{-\delta}\le\frac{d\nu_2}{d\mu^W_{\beta_{\mathrm{proxy},2}}}\le e^\delta.
\]

For any bounded normalized Wilson observables \(|F|,|G|\le1\), this implies

\[
|C_{\nu_2}(F,G)-C_{\mu^W_{\beta_{\mathrm{proxy},2}}}(F,G)|
\le3(e^\delta-1)
\le\frac{3\delta}{1-\delta}<10^{-8}.
\]

The last two bounds are checked using **exact rational integers**; no floating point, JSON, numerical quadrature or multi-million-state matrix is used. This is a genuine quantitative finite-volume certificate, but only at this **extremely small**, strong-coupling \(\beta_0\).

## 3. Direct bounded connected Wilson correlation — two distinct time limits

Choose normalized *spatial* \(F=\chi_{1/2}(V_{12}(t=0))/2\) and \(G=\chi_{1/2}(V_{12}(t=1))/2\), at identical coarse spatial position but at **different coarse times**. Their spatial coarse links are disjoint, so with product Haar both means and their two-point expectation are zero. The final Wilson proxy differs pointwise from Haar by at most \(e^{\pm z}\), with \(z=2N_{p,2}\beta_{\mathrm{proxy},2}<2^{-128}\). Let \(\eta=z/(1-z)\). Then
\[
|C_{\mu^W_{\beta_{\mathrm{proxy},2}}}(F,G)|\le\eta+\eta^2,
\quad
|C_{\nu_2}(F,G)|
\le\frac{3\delta}{1-\delta}+\eta+\eta^2
<10^{-8}.
\]

Hence the **actual interacting, finite periodic-time Euclidean Wilson correlation**, at temporal separation \(9a\), has the certified enclosure
\[
\boxed{-10^{-8}<C_{\mathrm{periodic}}(9a)<10^{-8}}.
\]
The sign and spectral weight are not determined. This is a bound, **not** the numerical integral's evaluated value. The source Euclidean time side has only 18 sites; a periodic thermal-type correlator is **not automatically an infinite-temporal-extent vacuum correlator**.

**Separate interacting vacuum bound.** Take the temporal extent to infinity at fixed 3D spatial side 18 and fixed \(\beta_0\), and use the original normalized positive Wilson transfer operator \(\mathcal T=T/\lambda_0\). The same normalized **\(9\times9\) spatial Wilson rectangle**, centered in the true interacting vacuum \(\Omega\), yields \(v=(F-\langle\Omega,F\Omega\rangle)\Omega\) with \(\|v\|^2=\mathrm{Var}_\Omega(F)\le1\). The YM4-02d transfer bound gives
\[
q_0=\frac{\lambda_1}{\lambda_0}\le\tanh(\beta_0 N_\ell)
\le\beta_0N_\ell=\frac1{1152},\quad N_\ell=3(18)^3=17,496.
\]
Since \(\mathcal T\) is positive, the true-vacuum connected *self*-correlator satisfies
\[
\boxed{0\le C_\Omega(9a)=\langle v,\mathcal T^9v\rangle
\le\left(\frac1{1152}\right)^9
=\frac1{3573323304747203265520730112}.}
\]
This **does concern the interacting vacuum**, but it is a *very loose one-sided upper bound*, not an independently measured overlap with the first excited state. It applies to the strong-coupling example, not automatically to the weak-coupling continuum.

## 4. Transfer-spectrum comparison and the visibility issue

YM4-03 Theorem 7 defines the subspace \(\mathcal H_3'\) generated by gauge-invariant coarse-slice Wilson multiplications acting around the fine interacting vacuum, evolved by \(T^3\); likewise \(\mathcal H_9'\) after two blocks. The original theorem implies
\[
T'_3=T^3|_{\mathcal H'_3},\qquad
T'_9=T^9|_{\mathcal H'_9},\qquad
\mathcal H'_9\subseteq\mathcal H'_3.
\]
Therefore, if \(q_j\) are normalized *subleading* spectral ratios,
\[
q_3\le q_0^3,\qquad q_9\le q_3^3\le q_0^9.
\]
The test reads the exact upper bounds
\[
q_0\le\frac1{1152},\quad
q_3\le\frac1{1528823808},\quad
q_9\le\frac1{3573323304747203265520730112}.
\]
In physical units, \(m_{\rm fine}\ge\log(1152)/a\), and the observable-generated restrictions cannot have a smaller mass. **But a blocked channel may omit the true first excited eigenstate**, making its *observed* gap larger; no positive first-state overlap is certified. Nor does total-variation closeness of measures alone imply a comparably tight spectral gap for the *proxy Wilson transfer operator*. These two distinct facts prevent unjustified transfer of a gap.

## 5. The explicit physical-gap counterexample

Take the **toy** positive two-state transfer family
\[
T_k=\operatorname{diag}\left(1,\frac{3^{2k}}{3^{2k}+1}\right),
\quad a_k=3^{-k},\quad k\ge1.
\]
Every finite model has a positive first lattice gap
\[
\Delta_k=\log(1+3^{-2k})>0.
\]
Blocking time by factors of 3 and 9 exactly raises the second eigenvalue to its third and ninth power, preserving the normalized transfer correlation of the **visible** off-diagonal observable \(O\). But its mass in physical units obeys
\[
0<m_{\rm phys}(k)
=3^k\log(1+3^{-2k})
<3^{-k}\longrightarrow0.
\]
At fixed physical time \(t=1\), the connected correlation is
\[
C_k(1)=\left(\frac{3^{2k}}{3^{2k}+1}\right)^{3^k}
\ge1-3^{-k}\longrightarrow1.
\]
The new checker verifies six exact rational cases \(k=1,\ldots,6\), the two time-block powers, the strict positive fine gap, the exact physical upper bound and the correlation limit argument. This is deliberately **not** an SU(2) Wilson transfer operator. Its purpose is to reject the invalid inference “finite positive gaps + perfect two-scale blocking + visible correlation imply a positive continuum mass.”

## 6. Fail-closed decision and next mathematical step

**Finite 4D SU(2) two-block algebra and absolute error:** PASS under the pinned YM4-03/02c/02d hypotheses. **Two-step Wilson-only *relative* coupling accuracy:** FAIL/HOLD because the global error \(\delta_1\) is **larger** than the very small leading coarse Wilson signal \(2N_{p,1}\beta_{\mathrm{proxy},1}\). The bound is also extensive in \(N_p\) and requires \(\beta N_p\) tiny. In the required weak-coupling continuum trajectory \(\beta(a)\to\infty\), its hypothesis \(\beta\le1/(8N_p)\) cannot persist. This is an identified **mathematical obstruction to using this particular bound for the all-scale induction**, not a counterexample to the existence of Yang–Mills theory.

**The estimate to replace** is the global \(|X|\le N_p\) Cauchy remainder. A serious YM4-04 next certificate must bound **connected, localized polymer/character clusters per coarse block**, summable across scales and sufficiently stable under the actual induced nonlocal interactions, with a norm controlled along \(\beta(a)\to\infty\). In parallel it must certify overlap of the true first excited state under every blocking map, or provide an independent *full-spectrum* lower bound. A proposed induction must specify \(\epsilon_k\) with \(\sum_{k\ge0}\epsilon_k<\infty\), uniform physical-volume bounds, and a renormalized coupling trajectory. Until those are proved, do not promote this two-scale finite test to an infinite-universe or Clay theorem.

**Reproduce:**
\`\`\`sh
python3 -I -X utf8 tests/test_ym4_04_two_ternary_blocks.py
\`\`\`
The [dedicated workflow](../.github/workflows/ym4-04-two-ternary-blocks.yml) also checks the repo's strict no-float gate, exact byte-for-byte receipt replay and **ten deliberate false claims**. Prediction misses or a weakened bound must be filed rather than hidden. All source/proof scopes remain distinct.
