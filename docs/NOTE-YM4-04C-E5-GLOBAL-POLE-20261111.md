# YM4-04C E5+ — global uniqueness and monotonicity of the frozen C04/C15 tail pole

**11 November 2026 · independent proof extension, stacked on draft PR #62.** This result tightens the large-coupling *certificate obstruction*, not the physical Yang–Mills mass gap. It does not change either pre-code prediction freeze, any polymer count, G0/G1, a finite S3 run, or the base-branch gate.

## Theorem (monotonicity under exponential tilt)

Let (\mu) be any probability measure, let (A) be a bounded, nonconstant real observable, and write
[
 Z(\beta)=\mathbb E_\mu e^{\beta A},\quad
 X_\beta=\frac{e^{\beta A}}{Z(\beta)},\quad
 dP_\beta=X_\beta,d\mu,\qquad \beta\ge0.
]
For every differentiable convex (\Phi:(0,\infty)\to\mathbb R), the map
(D_\Phi(\beta)=\mathbb E_\mu\Phi(X_\beta)) is nondecreasing on ([0,\infty)).
It is strictly increasing for (\beta>0) if (\Phi') is strictly increasing on the image of (X_\beta).

**Proof.** Boundedness of (A) justifies differentiation under the integral on every compact (\beta)-interval. Set (m_\beta=\mathbb E_{P_\beta}A). Then
[
 \frac{dX_\beta}{d\beta}=X_\beta(A-m_\beta),\qquad
 D_\Phi'(\beta)
 =\operatorname{Cov}_{P_\beta}(\Phi'(X_\beta),A).
]
For (\beta>0), both (A\mapsto X_\beta(A)) and (\Phi') are nondecreasing. With independent (A,A'\sim P_\beta),
[
 2\operatorname{Cov}_{P_\beta}(\Phi'(X_\beta),A)
 =\mathbb E_{P_\beta\otimes P_\beta}
   [(\Phi'(X_\beta(A))-\Phi'(X_\beta(A')))(A-A')]\ge0.
]
If (A) is nonconstant and (\Phi') is strictly increasing on the image, the integrand is positive on a set of positive product measure. Continuity covers (\beta=0). QED.

For the actual normalized continuous-SU(2) Haar measure, (A(U)=\operatorname{ReTr}U/2\in[-1,1]) is nonconstant. Taking (\Phi(x)=(x-1)^6=|x-1|^6), whose derivative (6(x-1)^5) is strictly increasing, proves that
[
 \varepsilon_6(\beta)^6
 =\mathbb E_{\mathrm{Haar}}\left(\frac{e^{\beta A}}{c_0(\beta)}-1\right)^6
]
and hence (\varepsilon_6(\beta)) are **strictly increasing** for (\beta>0). This does not assume or infer monotonicity from a sampled grid.

## Corollary (single, globally bracketed fixed-tail pole)

Hold the **frozen C04/C15 parameterization** fixed: (κ=θ=1/4), the rooted-degree-(20) Fuss–Catalan geometric tail growth (\mu_{20}=20^{20}/19^{19}), and nonnegative polymer activity parameter (\alpha\). The mandatory geometric-majorant pole argument is
[
 W(\beta)=\mu_{20}e^{1/4}\varepsilon_6(\beta),\quad
 \mu_{20}\varepsilon_6(\beta)e^{2\alpha+1/4}\ge W(\beta).
]
The theorem implies (W) is continuous and strictly increasing on (\beta>0), with (W(0)=0).

The independently enclosed C04 endpoint values already in the stacked engine are reproduced by a **third, source-disjoint rational method** in `tests/test_ym4_04c_e5_global_pole.py`:
- (0.999913588125<W(2247/100000)<0.999913588128<1).
- (1<1.000358668021<W(2248/100000)<1.000358668024).
- (1.112522354464<W(1/40)<1.112522354467), also matching frozen C15.

Thus there exists **exactly one** (\beta_{\rm pole}) with (W(\beta_{\rm pole})=1), and
[
 \boxed{0.02247<\beta_{\rm pole}<0.02248.}
]
For **every** real (\beta\ge0.02248) and (\alpha\ge0) the mandatory pole condition (\mu_{20}\varepsilon_6(\beta)e^{2\alpha+1/4}<1) is impossible. This strictly strengthens PR #62's valid all-large-β bound at (\beta\ge36), without needing large-β asymptotics. The C05/C06 self-map and KP bounds can fail **before** the pole, so (\beta<\beta_{\rm pole}) means *only* that this particular necessary pole condition is satisfied, not that G0/G1 or the whole certificate is MET.

A different choice of norm, (\theta), resummation, optimized majorant, or physical RG flow is not ruled out; the statement concerns the **frozen fixed-θ, fixed-μ geometric Fuss–Catalan sufficient certificate only**. The underlying polymer series may converge where this conservative majorant fails. No continuum existence theorem, transfer spectral inequality, or physical mass gap follows.

## Third exact arithmetic route (separate from both E4/E5 checkers)

The standalone Python script uses **only integer arithmetic and reduced rational pairs** (no floats, Fraction, Decimal, Node or JSON). It independently evaluates
[
 c_0(t)=\sum_{m\ge0}\frac{(t/2)^{2m}}{m!(m+1)!},
 \quad\varepsilon_6^6=\sum_{j=0}^{6}(-1)^{6-j}{6\choose j}
\frac{c_0(j\beta)}{c_0(\beta)^j}.
]
It takes terms (m=0,\dots,24) in (c_0), bounds the positive tail by the first omitted term divided by (1-r) using
(r=(t/2)^2/((26)(27))<1/100) at each endpoint, and takes 81 positive terms for (e^{1/4}) with a geometric tail bound. All operations are outward interval arithmetic on rational endpoints. Integer sixth-root bisection at denominator (10^{24}) encloses the nonnegative sixth root. This is analytically different from both PR #62's 256-bit interval engine and the earlier 640-bit second-seat route. The monotonicity lemma, not these three finite arithmetic checks, supplies the **all-real-β conclusion**.

**Acceptance and release:** third route must pass on the final head; reject its intentionally false endpoint inversion; no changes to the old immutable receipts; keep this PR DRAFT and its parent #62 DRAFT while the inherited evidence-list human-review HOLD remains unresolved. Weak-coupling continuum Yang–Mills existence and the gap remain OPEN.
