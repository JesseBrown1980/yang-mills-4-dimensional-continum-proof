# YM4-VOL08 — original continuous SU(2) Wilson weak-coupling link-star: gauge-invariant good/bad boundary certificate

**2026-11-22 · Mathematical derivation, direct original 4D Wilson model · analytic review and independent signoff outstanding.** This note introduces two complementary, exact local conclusions: a gauge-invariant **good-star conditional concentration bound**, and a **one-external-link frustrated-boundary witness** in the same continuous SU(2) theory. The latter is an explicit adversarial test for any attempted all-boundary weak-coupling single-link contraction. It establishes a boundary-control obligation for VOL07's physical-size block target. It does **not** establish that block estimate, a physical continuum gap, or the eleven original continuum gates.

## Model and normalization

Use normalized Haar measure on each original link of a 4D periodic lattice \(L^4\), \(L\ge3\). The original plaquette weight is
\[
\exp\bigl(\beta\sum_p W_p\bigr),\qquad W_p=\tfrac12\operatorname{Tr} U_p\in[-1,1],\quad \beta>0.
\]
This is the conventional \(\beta_W\) normalization, **not** the \(N\beta\operatorname{ReTr}\) normalization in [Bhattacharjee–Bhattacharya–Lockwood–Romanov, *One Cube Estimate Implies the Yang–Mills Mass Gap*, version 7, 4 Nov 2026](https://hexagonmath.org/2610.00341v7): in that paper, \(\beta_W=4\beta_{\rm paper}\) for SU(2). Their latest source, [creelie/4Y-M v4.37.0](https://github.com/creelie/4Y-M/tree/main/YangMills), and their explicit one-cube/bad-block decomposition are cited as prior work, not imported as proof of our local certificate.

Identify \(SU(2)\) with unit quaternions \(u\in S^3\). Let \(e=(x,\mu)\) be one positively oriented original link. For each of its six incident plaquettes write its ordered holonomy (possibly after reversal and cyclic trace invariance) as \(U_e S_i\), with \(S_i\) a path along the other three links from \(x+\hat\mu\) to \(x\). Set \(s_i=S_i^{-1}\), regarded as a unit quaternion parallel transporter from \(x\) to \(x+\hat\mu\). Then
\[
W(U_e S_i)=u\cdot s_i,\quad H=\sum_{i=1}^6s_i,\quad
d\mu_e(u\mid\mathrm{exterior})
=\frac{\exp(\beta\,u\cdot H)}{Z(\beta|H|)}\,du_{\rm Haar}.
\tag{1}
\]
This is the **exact** continuous-SU(2) conditional law, with arbitrary exterior links, including center-frustrated boundary data. No gauge fixing or small-field expansion has been used.

Under arbitrary endpoint gauge transformations, both \(u\) and every \(s_i\) transform as \(g_x(\cdot)g_{x+\hat\mu}^{-1}\); the six plaquette traces \(u\cdot s_i\) and the fifteen pairwise double-staple Wilson traces \(s_i\cdot s_j=\tfrac12\mathrm{Tr}(S_i^{-1}S_j)\) are gauge invariant.

## Lemma A: exact SU(2) Haar tilt concentration, all \(\kappa>0\)

Let \(X\) be the projection of a Haar unit quaternion onto any fixed unit quaternion axis, tilted by \(\exp(\kappa X)\). Since the un-tilted law has density \(\frac2\pi\sqrt{1-x^2}\,dx\) on \([-1,1]\), the tilted mean \(m(\kappa)=\mathbb E_\kappa X\) satisfies
\[
\boxed{m(\kappa)\ge 1-\frac{3}{2\kappa}}.
\tag{2}
\]
**Proof without special-function approximations.** The identity is also independently recovered by direct integration by parts in [VOL08 audit](../../reviews/YM4-VOL08-HAAR-BY-PARTS-INDEPENDENT-AUDIT-20261122.md). Set \(t=1-x\in[0,2]\). Its tilted density is proportional to
\[
t^{1/2}e^{-\kappa t}\,\underbrace{\sqrt{(2-t)_+}}_{v(t)\text{ nonincreasing}}.
\]
Compare it with an untruncated Gamma\((3/2,\mathrm{rate}\ \kappa)\) variable \(T\), which has \(\mathbb E T=3/(2\kappa)\). Since \(v(T)\) is nonnegative nonincreasing, \(\operatorname{Cov}(T,v(T))\le0\) by the independent-copy rearrangement identity; therefore
\(\mathbb E[T v(T)]/\mathbb E[v(T)]\le\mathbb ET\).
Thus \(\mathbb E_\kappa(1-X)\le3/(2\kappa)\), proving (2). The exact integral is continuous-Haar mathematics, not an eight-element quaternion-subgroup sum.

By rotational invariance of Haar \(S^3\), if \(H\ne0\),
\[
\mathbb E[u\mid\mathrm{exterior}]
=m(\beta|H|)\frac{H}{|H|}.
\tag{3}
\]

## Lemma B: a gauge-invariant good-star acceptance inequality

Fix \(0\le\epsilon<1\), and let \(\mathcal G_\epsilon(e)\) be the **fifteen gauge-invariant six-link Wilson inequalities**
\[
\mathcal G_\epsilon(e):
\qquad s_i\cdot s_j\ge 1-\epsilon\quad(1\le i<j\le6).
\tag{4}
\]
On this event,
\[
s_i\cdot H\ge6(1-\epsilon),\quad 6(1-\epsilon)\le|H|\le6,
\quad s_i\cdot H/|H|\ge1-\epsilon.
\]
Combining (2)–(3) gives the explicit **original SU(2) plaquette** conditional bound
\[
\boxed{\mathbb E[\,W(U_e S_i)\mid\mathrm{exterior}\,]
\ge 1-\epsilon-\frac1{4\beta(1-\epsilon)}}\quad\forall i.
\tag{5}
\]
For any \(0<\delta\le2\), Markov's inequality gives
\[
\boxed{\Pr[\,W(U_e S_i)\le1-\delta\mid\mathrm{exterior}\,]
\le\frac{\epsilon+[4\beta(1-\epsilon)]^{-1}}{\delta}}.
\tag{6}
\]
A union bound multiplies this by six to control all six plaquettes simultaneously.

**Exact rational fixture:** \(\beta=81,\epsilon=1/81,\delta=1/3\). Then
\[
1-\mathbb EW_i\le\frac{401}{25920},\quad
\Pr[W_i\le2/3\mid\mathcal G_\epsilon,\mathrm{exterior}]\le\frac{401}{8640},
\quad
\Pr[\exists i:W_i\le2/3\mid\mathcal G_\epsilon,\mathrm{exterior}]\le\frac{401}{1440}.
\tag{7}
\]
Here conditioning on \(\mathcal G_\epsilon\) is shorthand for **fixing any exterior configuration that satisfies it**. There is no claim that its probability under the full interacting Gibbs measure has yet been bounded.

## Lemma C: an original 4D Wilson one-external-link frustrated-boundary obstruction

Take the distinguished link \(e=((0,0,0,0),\mu=0)\) on the **actual original \(3^4\) lattice**. Choose all exterior links \(+I\) except selected lower-path \(\nu\)-links at positions \(x-\hat\nu+\hat\mu\), for \(\nu\in\{1,2,3\}\), which can be independently set to \(-I\) (the center of SU(2)). The six original staples, ordered as upper/lower for each \(\nu\), are:

- **Aligned boundary A:** \((+I,+I,+I,+I,+I,+I)\), resultant \(H_A=6I\).
- **Near-frustrated boundary B:** \((+I,-I,+I,-I,+I,+I)\), resultant \(H_B=2I\).
- **Frustrated boundary F:** \((+I,-I,+I,-I,+I,-I)\), resultant \(H_F=0\).

B and F differ in **exactly one external, positively oriented original link**, while the first upper plaquette's preferred transporter \(s_1=+I\) is unchanged. Consequently the **same gauge-invariant plaquette**
\(X=\tfrac12\operatorname{Tr}(U_e S_1)=\operatorname{Re}U_e\)
has conditional distributions \(\nu_A,\nu_B,\nu_F\) with tilts \(6\beta,2\beta,0\), respectively. \(\nu_F\) is the original continuous SU(2) Haar pushforward.

For any \(0<\delta\le1\), apply (2) to aligned A and near-frustrated B, and use Markov:
\[
\nu_A(X\ge1-\delta)\ge1-\frac1{4\beta\delta},\qquad
\nu_B(X\ge1-\delta)\ge1-\frac3{4\beta\delta}.
\tag{8}
\]
The Haar density \(\frac2\pi\sqrt{1-x^2}\) is everywhere at most one for \(x\in[0,1]\), hence
\(\nu_F(X\ge1-\delta)\le\delta\).
The variational definition of total variation therefore yields the **model-specific gauge-invariant lower bounds**
\[
\boxed{\operatorname{TV}(\nu_A,\nu_F)\ge
1-\delta-\frac1{4\beta\delta}},
\quad
\boxed{\operatorname{TV}(\nu_B,\nu_F)\ge
1-\delta-\frac3{4\beta\delta}}.
\tag{9}
\]
The second comparison changes **one original external link only**, not a three-link boundary packet.

For any integer \(k\ge3\), choose \(\beta=k^2,\delta=1/k\) to obtain
\[
\operatorname{TV}(\nu_A,\nu_F)\ge1-\frac5{4k},\qquad
\boxed{\operatorname{TV}(\nu_B,\nu_F)\ge1-\frac7{4k}}.
\tag{10}
\]
At \(k=9\), \(\beta=81\), these are \(31/36\) and \(29/36\), respectively; at \(k=27\), \(\beta=729\), the one-external-link bound is \(101/108\). In both cases the bounds tend to **one** along \(k\to\infty\).

This is a **gauge-invariant plaquette pushforward TV** lower bound under arbitrary exterior boundary choices. It confirms that a weak-coupling **worst-case, original single-link conditional total-variation contraction factor bounded away from one** is impossible along \(\beta\to\infty\). It is not a lower bound for a gauge-fixed Kantorovich metric, nor a disproof of the averaged finite-cube Dobrushin–Shlosman or gauge-invariant renormalized block conditions in [version 7](https://hexagonmath.org/2610.00341v7). Bad-boundary **probability**, scale separation, and coarse block reconstruction remain genuinely consequential.

A separate **anti-falsification** check shows flipping both the link and all six staples by center \(-I\) leaves every plaquette trace unchanged: a raw-link comparison between the all-plus and all-minus stars would be a gauge-sensitive false witness. The B-to-F witness holds the tested upper staple fixed and varies the actual physical plaquette law.

## Finite receipt and independent acceptance gates

The exact-integer checker [\`tests/ym4_su2_vol08_wilson_star.py\`](../../tests/ym4_su2_vol08_wilson_star.py) is deliberately a **finite algebra/replay checker**: it reconstructs six oriented original Wilson staple paths and all eighteen distinct neighboring links for each link on \(3^4\) (324 links) and \(4^4\) (1024 links); verifies exact quaternion noncommutative gauge covariance, plaquette and fifteen loop invariants; constructs B and F by changing one original exterior link; and checks all displayed rational fractions and adversarial center controls. It uses only the finite \(Q_8\) subgroup as **algebraic witness fixtures**, while analytic formulas (1)–(10) apply to the full original *continuous* SU(2) Haar measure.

[HBP receipt](YM4-VOL08-WILSON-STAR-20261122.hbp) and the hosted exact byte-for-byte replay workflow pin results. Neither the checker nor the workflow mechanizes the Gamma comparison or a 4D continuum existence proof; those analytic steps should receive an independent mathematical review before any promotion.

**Acceptance record:**
- VOL08 original six-staple **conditional law and gauge covariance**: exact analytic derivation; finite algebra checks PASS.
- VOL08 original SU2 **good-star plaquette expectation and probability bound**: exact analytic derivation; rational arithmetic PASS.
- VOL08 **one-external-link gauge-invariant worst-case boundary TV witness**: exact analytic derivation; boundary realization and rational controls PASS.
- **Original SU2 weak-coupling physical-size cube condition**: OPEN.
- **Uniform good/bad-block frequency and coarse scale coupling**: OPEN.
- **Nonzero limiting physical Wilson source, OS continuum, full mass gap, and all eleven original continuum gates**: OPEN.

**Next certificate VOL09:** compute, or rigorously upper-bound, the probability of the **gauge-invariant bad-star event** \(\mathcal G_\epsilon^c\) for a *physical-size* cube under original SU2 conditional Gibbs measures, with a volume-and-boundary-independent controlled estimate. This must accommodate gauge orbit degeneracy and bad-block islands rather than assuming good boundaries occur by fiat. Combine a proven bad-block control with the good-star local bounds through an explicit block coupling; then test it against the full-sector VOL07 spectral-root requirements.
