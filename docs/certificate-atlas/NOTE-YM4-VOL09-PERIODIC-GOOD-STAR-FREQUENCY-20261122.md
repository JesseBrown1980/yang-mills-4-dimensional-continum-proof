# YM4-VOL09 — original continuous SU(2) Wilson volume-uniform good-star frequency from exact Haar caps

**2026-11-22 · New exact finite-periodic-lattice analytic bound.** This is a constructive next acceptance step after [VOL08](NOTE-YM4-VOL08-ORIGINAL-SU2-WILSON-STAR-20261122.md). It controls how frequently **gauge-invariant locally bad boundary stars** occur under the original *equilibrium* continuous-SU(2) Wilson Gibbs law, with a constant independent of spatial lattice size. The theorem holds on every isotropic periodic \(L^4\) torus, \(L\ge3\), for every real \(\beta\ge1\). Its integer checker provides exact-rational explicit values on the ternary sequence \(\beta=9^k\).

**Proof classification:** direct analytic derivation (Haar cap, compact Lie group geometry and free-energy convexity), with integer rational controls. The derivation is not machine-formalized and external peer review is OPEN. The finite-volume periodic **unconditional** star frequency is a separate proposition from a boundary-uniform physical-size Dobrushin–Shlosman cube coupling. The latter and the original eleven continuum gates remain OPEN.

## 1. Original normalized Wilson action and gauge-invariant star

Let \(V=L^4\), \(N_E=4V\) original oriented positive links and \(N_P=6V\) original plaquettes on the periodic 4D lattice \(L\ge3\). Put
\[
W_p=\frac12\operatorname{Tr}U_p,\quad
Z_L(\beta)=\int_{SU(2)^{N_E}}\exp\left(\beta\sum_pW_p\right)dU,\quad
\mu_{\beta,L}=\frac1{Z_L(\beta)}e^{\beta\sum_pW_p}dU.
\]
The Haar product is normalized. For each original oriented link \(e\), let \(s_1,\dots,s_6\in SU(2)\cong S^3\) be the six preferred three-edge staples of VOL08. These depend solely on the exterior links. The gauge-invariant \(\epsilon\)-good star is
\[
\mathcal G_\epsilon(e)=\{s_i\cdot s_j\ge1-\epsilon,\ \forall 1\le i<j\le6\},
\qquad 0<\epsilon<1.
\tag{1}
\]
The fifteen dot products are genuine double-staple closed Wilson traces.

## 2. Uniform Haar-cap lower bound for the partition function

For \(\beta\ge1\), set \(r=(4\sqrt\beta)^{-1}\le1/4\). Each link independently takes values in the closed SU(2) geodesic ball \(B_r(I)\) around identity. The normalized SU(2) Haar cap has mass
\[
h(r)=\frac2\pi\int_0^r\sin^2\theta\,d\theta
\ge\frac2\pi\int_0^r\frac{\theta^2}{4}\,d\theta
=\frac{r^3}{6\pi}\ge\frac{r^3}{24}
=\frac1{1536\,\beta^{3/2}}.
\tag{2}
\]
The inequality uses \(\sin\theta\ge\theta/2\) for \(0\le\theta\le1/4\), and \(\pi\le4\). The geodesic metric is bi-invariant, hence the holonomy of any four-link plaquette whose links lie in \(B_r(I)\) is at geodesic distance at most \(4r=1/\sqrt\beta\) from identity. Using \(\cos t\ge1-t^2/2\),
\[
W_p\ge1-\frac1{2\beta}
\tag{3}
\]
on the all-link cap event. Its product Haar mass is at least \(h(r)^{N_E}\), so
\[
\log Z_L(\beta)\ge\beta N_P-\frac{N_P}2-N_E\log(1536\beta^{3/2}).
\tag{4}
\]

## 3. Free-energy secant yields a volume-uniform plaquette deficit

Write \(F_L(\beta)=\log Z_L(\beta)\), which is smooth and convex because
\(F_L''(\beta)=\mathrm{Var}_{\beta,L}(\sum_pW_p)\ge0\). Then
\[
F_L'(\beta)\ge\frac{F_L(\beta)-F_L(\beta/2)}{\beta/2}.
\]
Use (4) and \(F_L(\beta/2)\le(\beta/2)N_P\) (since \(W_p\le1\)):
\[
F_L'(\beta)\ge N_P\Big(1-\frac1\beta\Big)
-\frac{2N_E}{\beta}\log(1536\beta^{3/2}).
\]
On the periodic isotropic torus, lattice rotations and translations give the same expected \(W_p\) for every plaquette orientation and position. With \(N_E/N_P=2/3\), the **exact continuum-group finite-volume theorem** is
\[
\boxed{
\mathbb E_{\mu_{\beta,L}}[1-W_p]
\le R(\beta):=
\frac1\beta+\frac4{3\beta}\log(1536\beta^{3/2}),
\qquad\beta\ge1,\ L\ge3.
}
\tag{5}
\]
The right side is independent of \(L\). This is a global equilibrium estimate under the original Wilson Gibbs law, rather than a perturbative small-field expansion or an assumption about good exteriors.

The same lower secant follows directly from positivity of relative entropy
\[
D_{\rm KL}(\mu_{\beta,L}\Vert\mu_{\beta/2,L})
=\frac\beta2F_L'(\beta)-[F_L(\beta)-F_L(\beta/2)]\ge0.
\]
This is a second derivation of the entropy/secant step, retaining the identical action normalization.

## 4. Pointwise plaquette-to-gauge-invariant-good-star conversion

For an original Wilson configuration and any link \(e\), let \(u=U_e\). Each of its six incident plaquettes is \(W_i=u\cdot s_i\) exactly. As unit quaternions,
\[
|s_i-s_j|^2
\le2(|s_i-u|^2+|u-s_j|^2)
=4[(1-W_i)+(1-W_j)].
\tag{6}
\]
If every \(W_i\ge1-\epsilon/4\), (6) yields
\(1-s_i\cdot s_j=|s_i-s_j|^2/2\le\epsilon\).
Thus the **pointwise, gauge-invariant implication** is
\[
\mathcal G_\epsilon(e)^c
\subseteq \bigcup_{i=1}^6\{W_i<1-\epsilon/4\}.
\tag{7}
\]
Using (5), Markov's inequality and a union bound:
\[
\boxed{
\mu_{\beta,L}[\mathcal G_\epsilon(e)^c]
\le \min\left\{1,\frac{24}{\epsilon}\,R(\beta)\right\},\qquad
\forall e,\ \beta\ge1,\ L\ge3.
}
\tag{8}
\]
For any fixed \(\epsilon>0\), the probability tends to zero as \(\beta\to\infty\), **uniformly across all finite periodic \(L^4\)**. Moreover, \(\epsilon=\beta^{-1/4}\) also gives a vanishing bound \(O((\log\beta)\beta^{-3/4})\). Thus a **shrinking Wilson-loop alignment tolerance** and an **increasingly high good-star equilibrium frequency** are obtained simultaneously.

## 5. Exact ternary / integer-only subcertificate

On the original ternary sequence \(n=3^k\), \(\beta=n^2=9^k\), \(k\ge1\), equations (5)–(8) have a rational upper envelope. The elementary strict inequalities
\[
e^8>\sum_{j=0}^{8}\frac{8^j}{j!}
=\frac{556403}{315}>1536,\qquad
e^{3/2}>1+\frac32+\frac98=\frac{29}{8}>3
\]
give \(\log1536<8\) and \(\log3<3/2\). Hence
\[
R(9^k)\le\frac{35+18k}{3\cdot9^k},
\qquad
\boxed{
\mu_{9^k,L}(\mathcal G_\epsilon(e)^c)
\le\min\left\{1,\frac{8(35+18k)}{\epsilon\,9^k}\right\}.
}
\tag{9}
\]
These are fully rational statements for each integer \(k\), with an elementary all-\(k\) proof from the logarithm inequalities.

Exact example fixtures:

| \(k\) | \(\beta=9^k\) | \(\epsilon\) | Certified bad-star probability ceiling |
|---|---|---|---|
| 5 | 59,049 | \(1/2\) | \(2000/59049\) |
| 6 | 531,441 | \(1/2\) | \(2288/531441\) |
| 8 | 43,046,721 | \(1/81=\beta^{-1/4}\) | \(1432/531441\) |
| 10 | 3,486,784,401 | \(1/59049=\beta^{-1/2}\) | \(1720/59049\) |

[Integer-only source checker](../../tests/ym4_su2_vol09_periodic_good_star.py), [frozen HBP](YM4-VOL09-PERIODIC-GOOD-STAR-20261122.hbp) and its hosted normal/optimized replay with SHA-256 verify these constants, \(N_E/N_P\), the 4D chordal triangle relation using quaternion-subgroup adversarial fixtures, and the exact partial-exponential series. They are **falsifiers for algebraic and integer steps**, not a numerical integral substitution for (2) or a formal proof of convexity.

## 6. Acceptance scope and targeted continuation

**Completed mathematical derivation (subject to independent external review):** (2)–(9) establish an **original continuous SU2**, nonperturbative, lattice-size-independent *periodic equilibrium* marginal good-star frequency bound, and the alignment tolerance may tend to zero.

**Next open bridge (VOL10):** Show that a high-probability good **single-star** event controls **connected islands of bad physical-size blocks**, with quantified mixing or Peierls-type tail under **arbitrary boundary conditioning** or an averaged Dobrushin–Shlosman condition. A uniform single-site probability alone permits strongly correlated rare events and supplies no block spectral contraction. Explicitly construct an appropriate coarse SU2 block metric, all-Gauss-sector comparison and source weights before invoking the [VOL07 block spectral-root theorem](NOTE-YM4-VOL07-PHYSICAL-BLOCK-GAP-CRITERION-20261122.md). This refines the same open inputs discussed in [Bhattacharjee et al., *One Cube Estimate Implies the Yang–Mills Mass Gap*, v7](https://hexagonmath.org/2610.00341v7) and the block analyses there.

**Status:** periodic unconditional good-star frequency = **ANALYTIC DERIVATION / exact integer replay**; full physical-size weak-coupling cube = **OPEN**; arbitrary exterior bad-block cluster frequency = **OPEN**; nontrivial 4D continuum source/OS construction and all eleven original continuum gates = **OPEN**.
