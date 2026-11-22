# YM4-VOL11 independent mathematical audit — conditional product and exact continuous Haar cap

**22 November 2026 · Separate analytical reconstruction by the assistant; external human referee status OPEN.** Reviewed original [VOL11 SU(2) separated-plaquette theorem](../docs/certificate-atlas/NOTE-YM4-VOL11-SEPARATED-DEFECTS-20261122.md). This audit checks the central potential failure modes: whether conditioning on selected links truly factors the **original 4D Wilson measure**, whether the gauge-invariant good-star conditions remain measurable after that conditioning, and whether the SU(2) cap tail is **continuous Haar rather than an eight-state truncation**.

## A. Direct Gibbs factorization from original four-link plaquettes

Let \(S\) be a set of positively oriented original links in a periodic \(L^4\) lattice, \(L\ge3\), with at most one member of \(S\) per original plaquette. Split the Wilson action
\[
A(U)=\sum_{p\cap S=\varnothing}W_p(U_{S^c})
+\sum_{e\in S}\;\sum_{p\ni e}W_p(U_e,U_{S^c}).
\]
Every term in the second sum is assigned to **exactly one** selected link, with no duplicate plaquette. For each fixed \(U_{S^c}\), normalized product Haar measure on \(S\) then makes
\[
\mu(dU_S\mid U_{S^c})
=\bigotimes_{e\in S}
\frac{\exp[\beta\sum_{p\ni e}W_p(U_e,U_{S^c})]}
{\int_{\mathrm{SU}(2)}\exp[\beta\sum_{p\ni e}W_p(v,U_{S^c})]\,dv}
\,dU_e.
\]
Using the six-staple SU(2) quaternion decomposition of VOL08, this is the factorization asserted in VOL11. **No Gibbs independence of the selected gauge-invariant plaquettes is asserted without fixing the complement.**

A good-star event \(G_e\) depends only on the six preferred path-products of **three links belonging to plaquettes incident to \(e\)**. Because no other selected link shares such a plaquette, every one of these path-products and all fifteen double-staple Wilson traces depend only on \(U_{S^c}\). This independently verifies good-exterior measurability; it would fail for adjacent selected links, an explicit red control in the checker.

## B. Original continuous SU2 Haar tilt by the geodesic polar measure

Write a unit quaternion \(u\) in polar form relative to any preferred axis \(h\), with \(\operatorname{Re}(u h^{-1})=\cos\theta\), \(\theta\in[0,\pi]\). The normalized Haar angular law has density \((2/\pi)\sin^2\theta\,d\theta\). Change variables \(t=1-\cos\theta\); the density becomes \((2/\pi)\sqrt{t(2-t)}\,dt\) on \([0,2]\). Thus a continuous SU2 Haar tilt by \(e^{\kappa u\cdot h}\) has a \(t\)-density proportional to \(e^{-\kappa t}\sqrt{t(2-t)}\).

For \(\kappa\ge1\), restrict its normalizer integral to \(t\in[0,1/\kappa]\). The exact inequalities \(e^{-1}>1/3\), \(2/\pi>1/2\), and \(\sqrt{2-t}\ge1\) imply
\[
\int e^{-\kappa t}\,d{\rm Haar}(t)
\ge\frac{1}{2}\frac13\int_0^{1/\kappa}\sqrt t\,dt
=\frac1{9\kappa^{3/2}}.
\]
For a tail \(t\ge z>0\), its unnormalized mass is \(\le e^{-\kappa z}\). The probability is therefore at most \(9\kappa^{3/2}e^{-\kappa z}\). This directly checks all constants, including normalized Haar.

## C. Independent numerical-factor check and joint probability

Under \(G_e(1/16)\), the six-staple resultant \(H\) satisfies
\(|H|\in[6(15/16),6]=[45/8,6]\), and each \(s_i\) is chordally at distance at most \(\sqrt{2/16}\) from \(h=H/|H|\). A plaquette defect \(u\cdot s_i\le1/2\) requires \(|u-s_i|\ge1\). By triangle inequality, \(|u-h|\ge1-\sqrt{1/8}>1/2\); hence \(1-u\cdot h\ge1/8\). With \(\kappa=\beta|H|\ge45\beta/8\), \(\kappa^{3/2}\le (6\beta)^2\) for \(\beta\ge1\), the conditional probability is
\[
\le 9(6\beta)^2e^{-(45\beta/8)(1/8)}
=324\beta^2e^{-45\beta/64}.
\]
This independently recovers the VOL11 coefficient and exponent, with a slightly different geometric comparison. The original inequality in the theorem uses the more general \(\delta\ge4\epsilon\) chordal relation.

On any simultaneous good exterior and independent set of \(r\) links, the conditional product density gives a product of \(r\) individual defect probabilities, each \(\le q_\beta\), so
\[
\mu_\beta\bigl(\forall e\in S:\; D_e\cap G_e\bigr)\le q_\beta^r.
\]
This is a **model-specific original Wilson many-plaquette estimate**, valid for all \(L\ge3\). Its scope is intentionally the good-exterior sector.

## D. Direct inspection of the unconditional contamination term

The number \(N_B=\sum_{e\in S}\mathbf1_{G_e^c}\) of bad-exterior labels is measurable given the complement. For each conditional factor at a good exterior, use \(q_\beta\); otherwise use the trivial factor 1. The conditional all-defect product is bounded by \(q_\beta^{r-N_B}\). For each \(t<r\),
\[
\mathbb E[q_\beta^{r-N_B}]
\le q_\beta^{r-t}+\Pr(N_B\ge t+1)
\le q_\beta^{r-t}+\frac{r p_\star(\beta)}{t+1}.
\]
This is the full unconditional result. The correlation of the bad-exterior indicators is entirely retained in the last term; **their joint activity is OPEN**. The VOL09 one-point ceiling at \(\beta=9^k\), \(\epsilon=1/16\), is exactly \(128(35+18k)/9^k\).

An adversarial all-correlated exterior-label distribution can satisfy a small marginal while having all labels bad simultaneously, which is consistent with this contaminated bound. It is only a logical counterexample; the actual Wilson Gibbs correlations remain a separate analysis.

## E. Acceptance and novelty scope

- Original SU(2) conditional product and 18-neighbor selection: **ANALYTIC DERIVATION / source graph replay**.
- Continuous Haar cap and Wilson plaquette conditional tail: **ANALYTIC DERIVATION**; twelve-term integer Taylor upper bound \(\beta=81\) is an independent arithmetic falsifier.
- Joint selected original plaquette **and** simultaneous gauge-invariant good exteriors: **ANALYTIC DERIVATION** with exponential \(r\)-dependence.
- Unconditional selected original plaquette joint probability with explicit bad-exterior contamination: **ANALYTIC DERIVATION**, **insufficient to infer VOL10-JOINT**.
- Unconditional independent bad-star activity, arbitrary-boundary physical-size cube, limiting Wilson source and eleven original continuum proof gates: **OPEN**.
- External referee and first-in-community originality review: **OPEN**.

**Prior-work placement:** Exact single-link Wilson heat-bath forms and Dobrushin/large-field block methods are established. See [Bhattacharjee et al., *One Cube Estimate Implies the Yang–Mills Mass Gap*, v7](https://hexagonmath.org/2610.00341v7), for extensive 4D block-island and large-field methods with a stronger, conditional continuum objective. VOL11 is a source-specific reproducibility and precise good/bad partition certificate, with its novelty status reserved for independent literature review.
