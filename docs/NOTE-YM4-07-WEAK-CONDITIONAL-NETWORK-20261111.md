# YM4-07: a replacement weak-coupling *conditional* certificate in 4D Wilson SU(2)

**Date:** 2026-11-11. **Status:** mathematically derived local and conditional all-scale estimates, pending hosted independent review. **Not** a physical weak-coupling renormalization group construction or a 4D mass-gap theorem.

This is a **new track based directly on the Wilson conditional Gibbs law**, separate from the failed-at-large-beta F20/Fuss-Catalan polymer majorant in draft #62/#63. It starts at main `05de0ff7` instead of stacking on those drafts. It does not modify their prediction files, the inherited no-float evidence guard, G0/G1, the finite lattice repository, or r9.

## Evidence and prediction order

The 10 local predictions in `docs/PREDICTION-YM4-07-WEAK-CONDITIONAL-NETWORK-20261111.hbp` were committed as **`4ef2b3cf99ad44b50354028ae21c41e48592c6a6` before** any new engine code. A separate six-row all-scale prediction was committed as **`85b67aa9893bb78fd749ff995d215ff0684ff48c` before** the trajectory code. Both files are immutable predictions; the test is evidence only when replayed against the frozen versions.

## 1. Exact four-dimensional conditional law

Consider a finite periodic hypercubic 4D lattice of side at least three, SU(2) link variables, and Wilson density proportional to
[
\exp\bigl(\beta\sum_p \tfrac12\operatorname{ReTr}(U_p)\bigr)\,d\mathrm{Haar}(U),\qquad \beta>0.
]
Fix all links except a positively oriented link `U`. In four dimensions `U` belongs to exactly six incident plaquettes. Each term can be written as `u dot v_i`, identifying SU(2) with unit quaternions `u,v_i` in real four-space, with all orientations absorbed into the staples. Put
[
H=\sum_{i=1}^{6}v_i,\quad Q=|H|^2=6+2\sum_{i<j}\langle v_i,v_j\rangle,\quad R=\sqrt Q.
]
These 15 pairwise scalar products are the gauge-invariant **two-staple Wilson-network variables** (12 involve different transverse planes). Under a gauge transformation at the endpoints of `U`, each staple transforms by the same left and right unit-quaternion multiplications. Their real four-space Gram matrix, and therefore `Q`, is invariant.

If `R>0`, put `h=H/R` and `t=beta R`. The exact conditional density of `u` with respect to normalized SU(2) Haar is
[
dP(u\mid\mathrm{environment})=
\frac{\exp(t\langle u,h\rangle)}{c_0(t)}d\mathrm{Haar}(u),
\qquad c_0(t)=\sum_{m=0}^{\infty}\frac{t^{2m}}{4^m m!(m+1)!}.
]
At `R=0`, the conditional distribution is precisely Haar for every beta. The integral and moment formula were already established in YM4-05A; **the contribution here is the gauge-invariant large-beta tail, its premise, and a trajectory test**, not discovery of this integral.

## 2. New local concentration theorem valid at arbitrarily large beta

For each link define the environment-only good-field condition
[
G_\ell:\quad\langle v_i,v_j\rangle\ge\tfrac12\qquad\text{for all }1\le i<j\le6.
]
Then `Q >= 6+2*15*(1/2)=21`, hence `R >= sqrt(21)>4` and `t >= 4 beta`. Always `R<=6`, hence `t<=6 beta`. Both are gauge invariant.

**Lemma (uniform conditional tail given G).** For `beta>=1`, for any `0<s<=2`,
[
P\bigl(1-\langle u,h\rangle\ge s\mid\mathrm{environment}\bigr)
\le 1728\,\beta^2\exp(-4\beta s)\quad\text{on }G_\ell.
]
(The less elementary but tighter bound is `24 exp(1/2)*(6 beta)^(3/2)*exp(-4 beta s)`.)

**Proof.** For `t>=1`, Haar on the unit three-sphere has angular element `(2/pi) sin(theta)^2 dtheta`. Put `r=t^(-1/2)<=1`. Since `sin(theta)>=theta/2` for `0<=theta<=1` and `pi<4`, the Haar mass of the ball `theta<=r` is at least `r^3/24`. On that ball, `cos(theta)>=1-r^2/2`; thus
[
c_0(t)\ge\frac{e^{t-1/2}}{24t^{3/2}}.
]
On `1-cos(theta)>=s`, the unnormalized integral is at most `e^{t(1-s)}`. Dividing yields
[
P(1-\cos\theta\ge s)\le24e^{1/2}t^{3/2}e^{-ts}.
]
Use `4 beta<=t<=6 beta`, `beta>=1`, `(6 beta)^(3/2)<=(6 beta)^2` and `e^(1/2)<2` (termwise comparison with the geometric series) to obtain the claimed bound. Nothing here uses the F20 coefficient or strong-coupling expansion. QED.

At `s=1/2`, this is at most `1728 beta^2 exp(-2 beta)`. Three independent exact-integer strict checks are frozen:
- `beta=16`: bound less than `10^-6`, by `e^32 > 32^20/20! > 1728*16^2*10^6`.
- `beta=32`: bound less than `10^-15`, by the positive `e^64` term `64^29/29!`.
- `beta=64`: bound less than `10^-24`, by the positive `e^128` term `128^31/31!`.

These are **conditional upper bounds**, not simulations of the full Gibbs measure.

## 3. Explicit true 4D link cancellation: good field is necessary

On a periodic 3^4 SU(2) lattice put all oriented links at identity except the three transverse links `U_nu(e0-e_nu)=-I` for `nu=1,2,3`. The six plaquettes incident to the central link `U_0(0)` are, in the three transverse planes, three `+I` and three `-I` staples. Their sum `H=0`, so `Q=0` and the central link's conditional distribution is **exactly Haar at every beta**.

This is a physically realizable link configuration, not an arbitrary list of incompatible plaquette data. It is usually atypical at large beta; this example does **not** establish that it has appreciable probability. It rules out a worst-environment conditional concentration bound without a good-field hypothesis.

## 4. All-scale *conditional* trajectory, and a negative scaling control

Let `L_k=L0*3^k` in each of the four directions, so `N_links(k)=4 L0^4 81^k`. For a given `k`, let `G_{ell,k}` be the above pair-network condition, and `B_{ell,k}` the event `1-<u_ell,h_ell>>=1/2`, with arbitrary definition of `h` off `G`. The good-field condition depends only on the other links. Therefore the tower property and a union bound prove, for every finite lattice and beta>=1,
[
\Pr\bigl(\cup_{\ell}B_{\ell,k}\bigr)
\le \Pr\bigl(\cup_{\ell}G_{\ell,k}^c\bigr)
+4L_0^4\,81^k\,1728\beta_k^2e^{-2\beta_k}.
\tag{*}
]

**Positive conditional control (illustrative, not a derived physical RG flow):** prescribe `beta_k=16+3k`. The last term of (*) has a consecutive-term ratio
[
81\Bigl(\frac{\beta_k+3}{\beta_k}\Bigr)^2e^{-6}
\le81\Bigl(\frac{19}{16}\Bigr)^2\frac5{899}
=\boxed{\frac{146205}{230144}<1},
]
because `e^6>sum_{j=0}^5 6^j/j! =899/5`. Thus the **good-field contribution alone** is uniformly summable through infinitely many ternary refinements:
[
\sum_{k\ge0}\Pr\bigl(\exists \ell: B_{\ell,k}\cap G_{\ell,k}\bigr)
\le\frac{4L_0^4\,1728(16)^2e^{-32}}{1-146205/230144}
<\frac{4L_0^4\,10^{-6}}{1-146205/230144}.
]
These are sums of marginal probabilities on potentially different probability spaces; no cross-scale joint law or almost-sure conclusion has been established.

**Negative control:** for `beta_k=16+k/2`, the *derived union upper bound* grows instead, its consecutive ratio exceeding `81/e>27`, using `e<3`. This demonstrates that this simple union certificate does not work at that slope. A growing **upper bound** is not a growing physical probability.

The chosen `beta_k=16+3k` is faster than the standard asymptotically free SU(2) bare-coupling growth and is **not** a claimed Yang–Mills scaling trajectory. It is an exact test of which required large-field/RG estimate could conceivably close.

## 5. The real unproved obligations

1. Bound `Pr(\cup G_{ell,k}^c)` along a **genuinely derived** Wilson weak-coupling/continuum trajectory, uniformly enough in four-dimensional volume. The local bound alone supplies no such estimate.
2. Control the full set of induced Wilson-network interactions (including the 12 cross-plane pairs and the chair/higher-character terms) under actual gauge-equivariant blocking; a one-link Gibbs conditional is not a block RG theorem.
3. Reconcile UV scaling with physical running beta; the illustrative 3k slope cannot be relabeled physical asymptotic freedom. Gauge-invariant observables and reflection/transfer positivity must be preserved.
4. Establish continuum Schwinger functions, OS axioms, a nontrivial limit, and a **gap in physical units** with controlled spectral overlap. The conditional tail does none of these.

**Release:** Mark the new local concentration lemma and illustrative conditional summability as DERIVED after independent verification; `bad_field_probability`, physical weak RG, and mass gap remain **OPEN**. No merge until review and original repository gates pass.

## Prior work and background

- Prior exact local Haar integral and nonplanar chairs: [YM4-05A](NOTE-YM4-05A-CHARACTER-WEAK-COUPLING-20261107.md).
- Earlier strong-coupling local estimates: [YM4-04B](NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md).
- Classical small-field RG background: T. Balaban, *Renormalization group approach to lattice gauge field theories I*, Communications in Mathematical Physics 109 (1987), 249–301, DOI 10.1007/BF01215223.
- The physical mass-gap problem remains unsolved: [Clay Mathematics Institute](https://www.claymath.org/millennium/yang-mills-the-maths-gap/).
