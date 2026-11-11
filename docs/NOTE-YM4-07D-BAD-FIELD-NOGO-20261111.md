# YM4-07D: uniform bad-staple *lower* bound and no-go for globally good weak fields

**Date:** November 11, 2026. **Scope:** exact continuous-SU(2), four-dimensional finite periodic Wilson Gibbs measures. **New conclusion:** the demand that **every link** satisfy the YM4-07 six-staple good-field alignment is mathematically incompatible with thermodynamic volume at fixed beta, and also fails along any ternary bare-beta trajectory with slope below the explicit threshold. This does not obstruct local rare-defect/cluster RG, ultraviolet stability, or the physical Yang–Mills mass gap.

This is an independent *lower* complement to [YM4-07C's upper and density bounds](NOTE-YM4-07C-UNCONDITIONAL-BAD-FIELD-20261111.md). Original predictions 10 rows frozen at `fdc03eb61dbe98d0d2c05f60f8dfb688cb20645d`; adaptive sharpening 6 rows frozen at `72cb4a4f22cb34231a126fb49af9fdc0811a6b05`, both **before new D checker code**.

## 1. Exact geometrical fact: one controllable neighboring link

Let `ell=(x,mu)` be one oriented central link on a periodic four-dimensional hypercubic lattice of side `L>=3`. It has six incident plaquettes, one on each positive and negative side in each transverse direction. Their eighteen noncentral link variables are all distinct; the full local support has nineteen oriented links including `ell`.

Fix any transverse direction `nu != mu` and choose the oriented link `j=(x+e_mu,nu)`. It belongs to exactly **one** of the six plaquettes incident to `ell`. Consequently, among the six SU(2) staple vectors `v_1,...,v_6` seen by `ell`, changing `U_j` changes precisely one staple, say `v_1`. The remaining staple `v_2` can be fixed as a comparison target.

Conditional on all links except `j`, the **actual four-dimensional Wilson single-link conditional** has normalized density proportional to

[
\exp(\beta \sum_{i=1}^{6}\langle u_j,w_i\rangle)
=\exp(t\langle u_j,h\rangle),\quad t=\beta|\sum_i w_i|\in[0,6\beta].
]

The mapping `u_j -> v_1(u_j)` is an SU(2) left/right multiplication or inversion (possibly followed by multiplication), hence a Haar-preserving orthogonal isometry on the unit quaternion sphere `S^3`. Its pushforward conditional law remains `exp(t <v,h'>)/c_0(t)` for some unit direction `h'`. If `t=0`, choose `h'` arbitrarily. The target `n=v_2` does **not** depend on `U_j`.

The event `<v_1,n> <= 0` implies `G_ell^c` (since `0<1/2`), regardless of other staple values.

## 2. A uniform probability lower bound for *every external environment*

Let `h,n` be **arbitrary** unit vectors in real four-space. Choose a unit vector `z` orthogonal to both, possible because the orthogonal complement has dimension at least two. For `0<r<=1/8`, consider the geodesic ball `B(z,r)` on `S^3`.

Reflect in the hyperplane `n^perp`. Because `z perp n`, this is a Haar-preserving isometry of `B(z,r)`, swapping the halves `<v,n><=0` and `<v,n>>=0`. Thus the negative half-ball has exactly half the ball's Haar mass. The elementary Haar small-ball inequality from YM4-07C gives

[
\mathrm{Haar}(\{v\in B(z,r):\langle v,n\rangle\le0\})
\ge\frac{r^3}{48}.
]

For every `v` in the ball, `|<v,h>|=|<v-z,h>| <= |v-z| <=r`. The conditional numerator on the negative half-ball is at least `(r^3/48)*exp(-tr)`, and its normalization is at most `exp(t)`. Consequently, **for every external field**,

[
\boxed{\Pr(G_\ell^c\mid\text{all links other than }j)
\ge\frac{r^3}{48}\exp[-6\beta(1+r)].}
\tag{07D.1}
]

This is a finite-energy bound. No mixing, independence, strong-coupling condition or cluster estimate is assumed. In particular, choosing fixed `r=1/8` gives

[
\boxed{\Pr(G_\ell^c)\ge
\frac{\exp(-27\beta/4)}{24576}}
\qquad(\beta\ge0).
\tag{07D.2}
]

**Sharper adaptive-radius version (beta>=1):** choose `r=1/(6 beta)<=1/6`. The same argument, valid with `r<=1` in the small-ball bound, yields

[
\boxed{
\Pr(G_\ell^c\mid\mathrm{outside}, j)
\ge\frac{e^{-6\beta-1}}{10368\beta^3}
>\frac{e^{-6\beta}}{31104\beta^3}.}
\tag{07D.3}
]

The strict last inequality uses `e<3`, which follows from the factorial series. To avoid ambiguity, the small-ball and reflection argument holds for **all `r<=1`**, not only `r<=1/8` as initially chosen for the fixed-radius result.

## 3. Genuine many-link theorem without an independence assumption

The entire six-plaquette support of a central link `ell=(x,0)` lies among the oriented edges with basepoints `x+d` where every component of `d` is in `[-1,1]`. Consequently, choose central links only at `x=(3a,3b,3c,3d)`, with each coordinate in `{0,3,...,3(floor(L/3)-1)}`. Their local 19-link supports are pairwise disjoint, including across periodic boundaries because the wraparound separation is at least three.

There are exactly `M(L)=floor(L/3)^4` such links. Let `A_i=G_{ell_i}^c`. From (07D.1), **conditional on all links outside each target support**, `Pr(A_i|outside) >=p_beta`, where `p_beta` is the right-hand side of (07D.2) or (07D.3). Disjoint supports let us expose the supports in sequence. The tower property gives

[
\Pr\left(\bigcap_{i=1}^{M}A_i^c\right)
\le(1-p_\beta)^{M}
\le\exp(-Mp_\beta).
\]

Since the event that **every** link is good implies every selected link is good, we obtain

[
\boxed{\Pr_{\beta,L}(\forall\ell\ G_\ell)
\le\exp\left(-\lfloor L/3\rfloor^4
\frac{e^{-6\beta-1}}{10368\beta^3}\right)}
\quad(\beta\ge1).
\tag{07D.4}
]

At every fixed finite beta>=1 the right side tends to **zero** as `L->infinity`. This is a rigorous no-go for taking the global all-links-good event to have uniformly high probability at fixed Wilson beta.

## 4. The physically relevant bare-beta slope comparison

Take `L_k=L0*3^k`, `L0>=3`, and a **hypothesized** trajectory

[
\beta_k=\beta_0+c k+o(k),\quad c>0.
]

By (07D.4), `M(L_k) p_(beta_k)` grows exponentially up to polynomial factors precisely under the sufficient condition

[
\boxed{6c<4\ln3\quad\Longleftrightarrow\quad c<\tfrac23\ln3.}
\tag{07D.5}
]

Therefore, if (07D.5) holds, `Pr(all links good at scale k)->0`. This compares actual **marginal Gibbs probabilities at each scale** and does not require a joint coupling across scales.

For continuous SU(2) Wilson theory, the standard **one-loop asymptotic freedom** benchmark is `beta_W(a)=4/g0(a)^2` with slope `d beta_W / d ln(1/a) = 11/(3 pi^2)`. Under factor-three refinement the formal one-loop slope is `c_1loop = 11 ln3/(3 pi^2)`. It satisfies (07D.5) because `pi^2>11/2` (already implied by `pi>3`). Thus **the global all-links-good condition has vanishing probability on the one-loop benchmark trajectory**. This does **not** assert that the actual nonperturbative Wilson continuum bare-coupling trajectory is established.

The earlier fixed-radius bound (07D.2) also proves a weaker threshold `c<16 ln3/27`, itself sufficient for the one-loop benchmark. The adaptive bound strengthens it to (07D.5).

## 5. What this means for a replacement certificate

We now have both sides of the **one-link** estimate, rigorous for the interacting model and uniform in L:

[
\frac{e^{-6\beta-1}}{10368\beta^3}
\le\Pr_{\beta,L}(G_\ell^c)
\le\min\left(1,\frac{48}{\beta}
\left[\tfrac12+\tfrac23\ln1536+\ln\beta\right]\right),
\quad \beta\ge1.
]

Both bounds are weak and far apart, but they settle crucial logic:

- Bad alignments become sparse in **expected density** as `beta->infinity` (YM4-07C).
- You **cannot demand all links everywhere** satisfy the alignment condition at large volume along the benchmark weak-coupling slope (YM4-07D). This is not merely a missing proof: the global-good event has provably vanishing probability.
- The replacement RG norm must tolerate and quantify **bad-field islands and connected network clusters**, rather than union-bound them away. Its missing ingredient is a volume-independent **anchored cluster-probability decay** and a compatible exact-blocking map.
- These facts do not supply Wilson-loop area laws, a transfer-matrix spectral bound, nontrivial continuum Schwinger functions, or a physical gap. **The Clay problem remains OPEN.**

## Falsifiable verification

New code verifies the exact 4D incident-plaquette/link incidence for two periodic sizes, a unique control-neighbor link, the 19-link support, disjoint origin-spacing-three supports, `r^3/48` constants, and both exponents without floats. False mutations target the neighbor multiplicity, radius half-ball, local support overlap, and exponential constants. The analytic bound in (07D.1) still requires independent paper-level review; finite checker outputs do not substitute for the spherical geometry or Gibbs-conditioning proof.

**NO MERGE** before hosted final-head acceptance and independent mathematical review. No impact on #62/#63, finite #160, r9, or the original proof gate.
