# YM4-07C — unconditional, volume-uniform estimate of the missing weak-field failure term

**Date:** 2026-11-11. **Status:** mathematical derivation plus integer-only finite constant checks. This settles an **unconditional one-link bad-field probability upper bound** for the exact Wilson Gibbs measure, not the all-link rare-cluster estimate needed for weak-coupling RG. The Clay continuum mass gap remains open.

The new predictions were frozen separately at commit `cc6e618499792ec0c352fdfb9e1532958802eb22` before any new 07C engine code. The earlier YM4-07 conditional lemma is in [NOTE-YM4-07-WEAK-CONDITIONAL-NETWORK-20261111.md](NOTE-YM4-07-WEAK-CONDITIONAL-NETWORK-20261111.md).

## Theorem 07C: probability that the six-staple alignment hypothesis fails

Let the 4D periodic hypercubic SU(2) Wilson lattice have side `L>=3`, `N=L^4` sites, `Nl=4N` positively oriented links and `Np=6N` plaquettes. Write

[
E(U)=\sum_p (1-a_p(U)),\quad a_p(U)=\tfrac12\operatorname{ReTr}U_p\in[-1,1],\quad
d\mu_{\beta,L}=\frac{e^{-\beta E(U)}}{\widetilde Z_{\beta,L}}\prod_\ell d\mathrm{Haar}(U_\ell).
]

For one link `ell`, write its six staple vectors `v_i` in the SU(2) unit-quaternion representation, in the convention `a_{p_i}=u_ell dot v_i`, and define the environment-only (gauge-invariant) event

[
G_\ell=\{\langle v_i,v_j\rangle\ge1/2\ \text{for all }1\le i<j\le6\}.
]

**Theorem.** For **every** real `beta>=1` and every finite `L>=3`,

[
\boxed{
\Pr_{\beta,L}(G_\ell^c)
\le \min\left\{1,\;
\frac{48}{\beta}\left(\frac12+\frac23\ln1536+\ln\beta\right)\right\}.}
\tag{07C.1}
]

The same upper bound controls the expected **fraction of bad links**. For any fraction `eta>0`, Markov's inequality gives

[
\Pr\left(\frac{\#\{\ell:G_\ell^c\}}{N_l}\ge\eta\right)
\le\min\{1,\;q_{\rm bad}(\beta)/\eta\},
\quad q_{\rm bad}(\beta):=
\frac{48}{\beta}\left(\frac12+\frac23\ln1536+\ln\beta\right).
\tag{07C.2}
]

In particular, at any fixed link the probability of failure tends to zero as beta tends to infinity **uniformly in L**, and the *density* of failing links tends to zero in probability even when the number of lattice links grows.

### Proof part A. An explicit lower bound on the Wilson partition function

For `beta>=1`, set `r=1/(4 sqrt(beta))<=1/4`. For one SU(2) Haar link `U`, identify its geodesic angle `theta in [0,pi]` from the identity, with `a(U)=cos(theta)`. Normalized Haar measure has polar radial density `(2/pi) sin(theta)^2 dtheta`. On `0<=theta<=r<=1`, `sin(theta)>=theta/2` and `pi<4`, so

[
\Pr_{\rm Haar}(\theta\le r)
\ge\frac2\pi\int_0^r\frac{\theta^2}{4}d\theta
=\frac{r^3}{6\pi}>\frac{r^3}{24}
=\frac1{1536\beta^{3/2}}.
\tag{07C.3}
]

Restrict **every** oriented link to that radius-`r` ball about identity. By the bi-invariant geodesic triangle inequality, any plaquette built from four such links has angle at most `4r`. Consequently,

[
1-a_p\le\frac{(4r)^2}{2}=\frac1{2\beta},
\qquad \beta E(U)\le\frac{N_p}{2}.
]

The restricted product Haar volume and the Boltzmann factor give, uniformly in L,

[
\boxed{
\widetilde Z_{\beta,L}
\ge e^{-N_p/2}\bigl(1536\beta^{3/2}\bigr)^{-N_l}.}
\tag{07C.4}
]

This uses the **full four-dimensional interacting Wilson partition function**, not an independent-plaquette product and not a strong-coupling expansion.

### Proof part B. Gibbs relative entropy bounds mean plaquette action

Let `H` denote the product of normalized link-Haar probability measures. The relative entropy of the Wilson probability `mu` with respect to `H` is nonnegative:

[
0\le D(\mu\|H)
=\int\log\left(\frac{d\mu}{dH}\right)d\mu
=-\beta\mathbb E_\mu E-\ln\widetilde Z.
]

Hence `beta E_mu[E] <= -ln Z`, and (07C.4) implies

[
\mathbb E_\mu E
\le\frac1\beta\left(\frac{N_p}{2}
 +N_l\left[\ln1536+\tfrac32\ln\beta\right]\right).
]

By translation and hypercubic-coordinate symmetry of the isotropic periodic torus, every oriented plaquette has the same one-plaquette expectation. Since `Nl/Np=2/3`,

[
\boxed{
\mathbb E_\mu(1-a_p)
\le\frac1\beta\left(\frac12+\frac23\ln1536+\ln\beta\right).}
\tag{07C.5}
]

The same inequality also bounds the spatial average on any symmetric periodic torus; the individual-plaquette statement is used here only for isotropic `L^4`.

### Proof part C. Plaquette quality implies the gauge-invariant six-staple condition

For one arbitrary configuration and any incident plaquette `p_i`, `a_{p_i}=u\cdot v_i`. Suppose all six incident plaquettes satisfy `a_{p_i}>=7/8`. For any pair, resolve `v_i=a_i u+w_i` with `w_i\perp u`; likewise for `v_j`. Then Cauchy–Schwarz shows

[
v_i\cdot v_j
\ge a_i a_j-\sqrt{1-a_i^2}\sqrt{1-a_j^2}
\ge 2(7/8)^2-1=17/32>1/2.
]

Therefore `G_ell^c` implies that **at least one** of those six plaquettes has `a_p<7/8`, equivalently `1-a_p>1/8`. Markov and a union bound yield

[
\Pr(G_\ell^c)
\le6\Pr(1-a_p>1/8)
\le48\,\mathbb E(1-a_p).
]

Substitution of (07C.5) proves (07C.1). Linearity of expectation and a second Markov inequality prove the density version (07C.2). **QED.**

There is no appeal to G0/G1, Kotecký–Preiss or the frozen F20 polymer coefficients. The only inputs are elementary Haar geometry, triangle inequality, probability relative entropy and Markov.

## Integer-only dyadic certificates

The positive Taylor polynomial `sum_{j=0}^8 8^j/j! = 556403/315 >1536` proves `ln1536<8`. From `e>2`, `ln2<1`. At `beta=2^m`, theorem 07C.1 therefore gives **strict**, entirely rational upper bounds

[
\Pr(G_\ell^c)<\min\left\{1,\frac{280+48m}{2^m}\right\}.
\tag{07C.6}
]

| beta | m | Certified strict upper bound on bad-link probability |
|---|---:|---:|
| `2^10 = 1024` | 10 | `760/1024 = 0.7421875` |
| `2^12 = 4096` | 12 | `856/4096 = 0.208984375` |
| `2^16 = 65536` | 16 | `1048/65536 = 0.0159912109375` |
| `2^20 = 1048576` | 20 | `1240/1048576 = 0.00118255615234375` |

These are **loose but rigorous unconditional estimates**. For beta 16, 32 and 64 this entropy method yields only the trivial cap 1, while the separate conditional estimate on G yields the much stronger values in YM4-07. Do not conflate the two.

The checker `tests/test_ym4_07c_bad_field.py` recomputes the exact positive exponential polynomial, lattice combinatorics, pair-angle threshold, dyadic rational bounds and density bounds. It also supplies an explicit `c=4/5` **counterexample**: `u=(1,0,0,0)`, `v_1=(4/5,3/5,0,0)`, `v_2=(4/5,-3/5,0,0)`, so the two plaquette alignments are both 4/5 while the staple pair product is only 7/25. Six controlled corruptions must fail closed. These finite checks support but do not replace the analytic proof.

## Consequence for all-scale Yang–Mills strategy

**What is genuinely resolved:** an explicitly quantified, volume-independent probability that *one specified link* violates the YM4-07 good-staple condition. This probability tends to zero in the large-beta limit, and the fraction of bad links tends to zero in probability uniformly as lattice volume grows.

**What is not resolved:** the probability that *any link anywhere* is bad, the size and mutual correlations of bad-link clusters, and their effect on induced Wilson networks. The union bound is

[
\Pr(\exists\,\ell\colon G_\ell^c)\le N_l\,q_{\rm bad}(\beta).
]

If the lattice refines by three in every direction, `Nl(k)=4L0^4 81^k`. For any **linearly growing** `beta_k=beta0+c k`, the right-hand upper bound grows without limit (before clipping at 1). The method gives a density result, not the globally simultaneous all-good event. Nor does the upper bound's growth prove that the true event becomes likely.

The physically relevant leading-order asymptotic-freedom relation for SU(2) Wilson `beta_W=4/g0^2` is `beta_W(a)=(11/(3pi^2)) ln(1/a)+lower-order terms`, so a factor-three refinement adds approximately `11 ln3/(3pi^2)` to beta. This is a **perturbative benchmark**, not a rigorously derived nonperturbative trajectory in this repository. Source: standard SU(N) beta-function coefficient `11N/(48pi^2)` and Wilson normalization `2N/g0^2`. The illustrative `16+3k` trajectory in YM4-07 is much faster than this benchmark.

**Next mathematical gate:** replace the global all-good-link union with a *local, gauge-invariant bad-field cluster norm*: quantify probabilities of connected simultaneous six-staple failures and their interactions under exact decimation, with a bound summable against cluster size and volume-uniform per anchored cluster. A one-point density estimate cannot establish clustering, RG contractivity, reflection-positive transfer spectra or a continuum physical mass gap.

**HOLD:** draft PR only. No merge, no changes to #62/#63, no finite PR #160 modification or r9 launch. Physical continuum mass gap OPEN.
