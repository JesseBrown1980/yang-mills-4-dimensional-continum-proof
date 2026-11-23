# YM4 VOL17 — exact high-beta obstruction to ordinary single-link Dobrushin contraction in original 4D SU(2)

**23 November 2026.** A constructive adversarial-control theorem on the *original continuous SU(2)* Wilson link heat bath, with six explicitly realizable rational quaternion staples and one-link neighbor changes. It complements [VOL16's rigorous unweighted low-beta comparison theorem](NOTE-YM4-VOL16-UNWEIGHTED-DOBRUSHIN-20261123.md) and sharpens why the physical high-beta acceptance of [issue #116](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/116) needs gauge-covariant, typical-environment or block-level control.

## 1. Six genuine SU(2) staples with exactly zero five-staple resultant

Work on an original untwisted even periodic four-dimensional torus L>=6. Fix the original positive link \(e=(x,0)\), x=(0,0,0,0), and use the six original Wilson three-edge staples (in ±nu directions, nu=1,2,3). Their *opposite 0-direction links*
\[
f_{\nu,+}=(x+\hat\nu,0),\qquad
f_{\nu,-}=(x-\hat\nu,0)
\]
are six distinct original positive links, and each belongs to the centered b=3 internal cube. Set every transverse-direction link to identity. Then each original three-edge staple of e is **exactly** the corresponding opposite-direction link variable U_f; changing only one U_f changes precisely one of the six staples of e.

Use the following five exact **norm-one rational SU(2) quaternions**:
\[
\begin{aligned}
q_1&=(1,0,0,0),\\
q_2&=(-1,1,1,1)/2,\\
q_3&=(-1,-1,-1,-1)/2,\\
q_4&=(0,1,0,0),\\
q_5&=(0,-1,0,0).
\end{aligned}
\tag{O1}
\]
They obey \(\sum_{i=1}^5q_i=0\) **exactly**. Each has quaternion Euclidean norm one and represents a genuine original continuous SU(2) link value. Some do not commute (for example q_2 and q_4). For any one of the six opposite links f, place q_1,...,q_5 as the other five staples and set the selected sixth staple to +I or -I. These two complete original link environments differ **only on f**, and their original SU(2) Wilson single-link conditional resultants are
\[
\boxed{H_e^+=I,\qquad H_e^-=-I.}\tag{O2}
\]

Thus each of six distinct actual interior neighboring links f produces two **legal** exterior-of-e environments where one changed link reverses the preferred direction of the complete one-link Gibbs conditional. These environments contain strongly frustrated/bad stars; this is a worst-boundary counterexample, not an estimate of their probability under the high-beta Gibbs law.

## 2. Certified total-variation separation from genuine continuous SU(2) Haar

For a Wilson coupling beta>0, define the true original one-link conditional SU(2) Haar laws
\[
\nu_\pm(du)=Z_\beta^{-1}e^{\pm\beta\,\operatorname{Re}u}\,dh(u),
\tag{O3}
\]
where h is normalized Haar on the full SU(2) three-sphere (not a finite quaternion-subgroup counting measure). The Haar marginal x=Re u has density
\[
p_0(x)=\frac2\pi\sqrt{1-x^2},\qquad-1\le x\le1.
\tag{O4}
\]
The Haar cap x∈[1/2,3/4] has mass greater than 1/16: its width is 1/4, \(\sqrt{1-x^2}>1/2\) throughout, and \(\pi<4\). Hence
\[
Z_\beta>\frac1{16}e^{\beta/2}.
\tag{O5}
\]
The \(\nu_+\) probability of x<=0 is at most \(8e^{-\beta/2}\) (its unnormalized numerator is at most 1/2). By symmetry, \(\nu_-\) probability of x>0 obeys the same bound. Taking x>0 as the total-variation test event gives
\[
\boxed{
\|\nu_+-\nu_-\|_{\rm TV}
>1-16e^{-\beta/2}.}
\tag{O6}
\]

For **all beta>=36**, the elementary positive exponential Taylor series gives \(e^{\beta/2}\ge e^{18}>1+18+18^2/2=181\). Therefore
\[
\boxed{
\|\nu_+-\nu_-\|_{\rm TV}>\frac{165}{181}.
}
\tag{O7}
\]

Let c_{ef} be the ordinary single-link total-variation Dobrushin influence coefficient for the original Wilson conditional law, optimized over all allowed assignments to the other internal links and a fixed exterior that permits the above configuration. Each of the six f_{\nu,\pm} has \(c_{ef}>165/181\), so the corresponding original interior graph row sum satisfies
\[
\boxed{
\sum_{f\ne e}c_{ef}
>6\frac{165}{181}=\frac{990}{181}>1.
}\tag{O8}
\]

This is a **strict lower bound on the true worst-environment Dobrushin row**, not just the failure of the upper envelope \(18\beta\) to be below one. It applies at the production \(\beta=9^{12}\), since \(9^{12}>36\), and even at every beta>=36. It therefore rules out proving that the unprojected **single-link, boundary-uniform, total-variation Dobrushin row sum** is less than one at production coupling.

## 3. What the obstruction establishes and how to proceed

The construction uses exactly six independent original Wilson staples at one link, and the full SU(2) Haar conditional variation. The [strict integer/Q8-rational verifier](../../tests/ym4_vol17_high_beta_obstruction.py) checks complete L=6 original positive-link geometry, the five-unit-quaternion zero sum, all six one-neighbor flip pairs, exactly one differing original link for each pair, noncommutativity, and the purely rational inequality 990>181. The exponential and Haar-cap steps O4–O7 are analytic, explicitly recorded for independent review.

**Mathematical conclusion:** a uniform-in-all-interior-configurations **raw linkwise total-variation Dobrushin** route to the high-beta physical boundary covariance is genuinely obstructed. It does **not** rule out gauge-invariant Wilson-source correlation decay, a gauge-orbit or block Dobrushin–Shlosman contraction, nor a typical-good-star coupling.

At the high-beta even periodic equilibrium, VOL12's chessboard activity shows the probability of an *individual* bad star is tiny. The obstruction fixtures are strongly frustrated and are therefore natural **negative controls** for a typical-good-star strategy. But the VOL15 interpolation laws with mixed boundary resultants are not automatically covered by that periodic-equilibrium rate. The next mathematical acceptance should therefore either (a) certify bad-star activity under **all relevant interpolating conditional boundary laws** with proper covariance/gauge projection; or (b) work through a conditional **Gibbs-exterior averaged**, gauge-covariant physical-source comparison that never requires worst-environment single-link total variation contraction.

## 4. Review/novelty status

The O1–O8 adversarial construction is independently checkable on the original model. It is a concrete high-beta diagnostic for this project's coupling architecture, **not** a claim that previously known strong-coupling or Yang–Mills mathematical results are new. Any statement about the project's 4D physical continuum mass gap still requires the original eleven continuum construction obligations.

**Accepted source scope:** exact original 4D rational SU(2) staple realizability and row-sum geometry, integer-only test pending hosted verification; true continuous SU(2) Haar total-variation lower bound analytical. **High-beta good-region interpolated covariance, physical all-sector gap and all continuum gates OPEN.** [Issue #116](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/116).


**Hosted acceptance PASS:** [Original L6 rational SU2 six-neighbor obstruction run #45212928702](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/45212928702). The complete six distinct real original link pairs, genuine noncommuting rational SU2 staples, exact H=±I resultants, full link-environment one-neighbor changes, frozen HBP, optimized/normal replay and no-float gate succeeded. The true full SU2 Haar total-variation lower bound O4–O8 is analytic and separately subject to independent referee review.
