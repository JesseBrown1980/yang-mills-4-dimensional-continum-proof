# YM4-03 — exact factor-two SU(2) blocking and a certified one-tile Wilson effective action

**Scope / status (2026-11-05):** This is one exact finite-volume gauge-covariant blocking construction, plus an explicit continuous-SU(2) character truncation for an **isolated planar 2×2 fine-plaquette tile**. It addresses specified parts of [YM4-03 issue #3](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/3). The construction uses the genuine continuous SU(2) Haar measure. The exact Q8 arithmetic in its executable test is a *separate noncommutative control*, not a replacement for SU(2) Haar integration. Full D=4 uniform-Wilson induced-action locality, repeated scales, weak coupling and physical gaps are separate OPEN gates.

**Prediction-first record:** [PREDICTION-YM4-03-GPT6.hbp](PREDICTION-YM4-03-GPT6.hbp) was committed at `fae9a7f` **before the test was added**. The test and [receipt](../tests/YM4_03_ONE_SCALE_GPT6.hbp) are `../tests/test_one_scale_block_gpt6.py`. Both are exact-integer/rational arithmetic.

## 1. Finite 4D geometric blocking and a genuine pushforward

Let the fine periodic hypercubic lattice have even lengths `2M_mu`, where every `M_mu >= 2`. Fine spacing is `a`; coarse spacing `2a`, with coarse sites at coordinates whose four components are even. Use one positively oriented variable `U_mu(x) in SU(2)` per fine edge and **normalized Haar probability measure** on each variable. The standard Wilson law is

`S_W(U;beta) = beta sum_p (1 - (1/2) Re Tr U_p)`, `beta >= 0`, `dmu_f = Z_f^-1 exp(-S_W) prod_{fine edges} dU`.

For a coarse edge `e=(x,mu)` define its parallel transport

`B(U)_e := U_mu(x) U_mu(x+a e_mu)`.

Write a fine gauge transformation as `U_mu(x)^g = g(x) U_mu(x) g(x+a e_mu)^-1`. Exact matrix cancellation gives

`B(U^g)_e = g(x) B(U)_e g(x+2a e_mu)^-1`.

This proves gauge equivariance for **all** continuous-SU(2) link/gauge configurations, including noncommuting ones. The product around any coarse elementary `mu,nu` plaquette is the *ordered holonomy around its eight-edge fine 2×2 boundary*, so closed-loop traces are equal exactly.

Each chosen coarse edge consists of two **distinct fine oriented edges**; these pairs do not overlap with other chosen coarse paths. For a pair write `V=U_1 U_2`, `W=U_2`. Its inverse change of variables is `U_1=V W^-1`, `U_2=W`. Bi-invariance of Haar gives **`dU_1 dU_2 = dV dW`**, with unit normalization. All other fine links are `X`. Hence the strictly positive continuous density

`K_beta(V) = integral exp[-S_W(U(V,W,X);beta)] (prod_e dW_e) (prod_other dX)`

defines the **exact full-four-dimensional** pushforward with respect to product coarse Haar:

`Z_f = integral K_beta(V) dV`; `nu_beta(dV) = K_beta(V) dV/Z_f`;

`integral F(V) nu_beta(dV) = Z_f^-1 integral F(B(U)) exp[-S_W(U)] dU`

for **every bounded measurable** `F` (therefore, in particular, bounded gauge-invariant Wilson-loop observables). Gauge equivariance, gauge invariance of the fine Wilson law and Haar invariance give `K_beta(V^h)=K_beta(V)` for every coarse gauge transformation `h`. Define the exact coarse action `S_eff(V)=-log K_beta(V)`, up to an additive constant, or `-log(K_beta/Z_f)` when normalized.

**Important structure:** this exact pushforward produces an effective action on all coarse links. On a full uniform four-dimensional Wilson lattice it may contain larger loops, coupled loops, and interactions at different separations. It has not been shown to remain a pure plaquette Wilson action. The next obligation is a normed, localized expansion with uniform constants.

## 2. An isolated 2×2 tile: continuous SU(2) effective action in characters

Use a single open planar `2×2` patch of four fine plaquettes and four coarse boundary links. The weight is Wilson on **these four plaquettes**, with all other plaquette couplings set to zero; this is an inhomogeneous finite-volume *test block*, which can be embedded in a four-dimensional lattice. Its result is a single-coarse-plaquette computation rather than a formula for the complete uniform D=4 theory.

Let `chi_n(g)` be the SU(2) irreducible character of spin `n/2`, dimension `d_n=n+1`; `chi_1(g)=Tr_f(g)`. Normalize the central single-plaquette weight

`w_beta(g)=exp(beta chi_1(g)/2)/integral_SU2 exp(beta chi_1(h)/2) dh`.

The harmless `exp(-beta)` factor in the Wilson action cancels in normalization. Normalized character orthogonality and the class-angle Haar formula give

`w_beta(g)=sum_{n>=0} (n+1) b_n(beta) chi_n(g)`,

`b_n(beta)=f_n(beta)/f_0(beta)`,

`f_n(beta)=sum_{k>=0} (beta/2)^(n+2k)/(k! (n+k+1)!)`.

To derive it, write `chi_n(theta)=sin((n+1)theta)/sin(theta)` and Haar class measure `(2/pi)sin^2(theta)dtheta`. Orthogonality or the modified-Bessel integral yields the coefficient `I_n(beta)-I_{n+2}(beta)=2(n+1)I_{n+1}(beta)/beta=(n+1)f_n(beta)`; divide by `f_0`. At `beta=0`, use the continuous series limit.

A spanning-tree/axial-gauge change of variables on the open tile takes three plaquette holonomies as independent Haar variables; the fourth is fixed by their product and the boundary coarse holonomy `V`. Since each plaquette weight is central, this gives exactly the **fourfold group convolution** `W_beta(V)=w_beta*w_beta*w_beta*w_beta(V)`. For central class functions, `chi_n*chi_m=delta_nm chi_n/d_n`; therefore

`W_beta(V)=sum_{n>=0} (n+1) b_n(beta)^4 chi_n(V)`.

This is the induced normalized density on the single coarse plaquette. It is nonconstant for `beta>0`. Its spin-half character coefficient begins with

`(2)b_1(beta)^4 = beta^4/128 + higher even powers of beta`.

For `0<=beta<=1` set `q=beta/2<=1/2`. Positivity gives `f_0>=1`, and

`f_n<=q^n/(n+1)! sum_{k>=0} q^(2k)/k! <=(4/3) q^n/(n+1)!`

because `exp(q^2)<=1/(1-q^2)<=4/3`. Consequently

`|chi_n(V)|<=n+1` and `|(n+1)b_n^4 chi_n(V)| <= (4/3)^4 (n+1)^2 (1/2)^(4n)/((n+1)!)^4`.

For `n>=3`, successive majorants have ratio at most `1/6400`. Truncating through `n=2` (spin 0, spin 1/2, spin 1), a geometric sum gives the **exact rational uniform enclosure**

`sup_V |W_beta(V)-W_beta,<=2(V)| <= E = 25/671741424 < 1/25000000`.

The first two nonconstant-character majorants give

`W_beta,<=2(V) >= L = 1 - 4/81 - 1/11664 = 11087/11664 > 19/20`.

Since `E<L`, the exact and truncated actions `-log W` and `-log W_<=2` satisfy

`sup_V |S_eff(V)-S_<=2(V)| <= E/(L-E) = 25/638511392 < 1/20000000`.

The test recomputes these **exact rational numbers** and independently brackets `f_0,f_1,f_2` by factorial series and a geometric remainder. This is a certificate for every `beta in [0,1]` and every coarse holonomy, rather than a floating-point sample.

## 3. Independent executable controls and scope

The code checks 64 coarse gauge-covariant links and 96 coarse-versus-fine plaquette holonomies on the `4^4` periodic geometry using noncommuting **rational unit SU(2) quaternions** `(3,4,0,0)/5`, `(5,0,12,0)/13`, `(7,0,0,24)/25`. These are exact elements of the continuous group; no rounding is involved.

A separate exhaustive **Q8** check tries all `8^5=32768` choices of two fine links and three gauge vertices. For the separately defined positive weight `1+(1/4)chi_1`, convolution four times gives exactly `1+chi_1/2048`: value `1025/1024` at the identity, `1023/1024` at minus the identity, and `1` on the other six group elements. This tests noncommutative convolution algebra; Q8 does not approximate the continuous Wilson measure.

Four fail-closed controls perturb ordered links, a coarse endpoint, an inverse on the closed loop, and the convolution coefficient. All must be rejected. Compare stdout byte-for-byte to the pinned HBP receipt, and check that the prediction file predates the implementation commit.

## 4. Next independent mathematical tasks

1. Independent proof review of the disintegration/gauge-fixing lemma for the isolated tile (especially edge orientation and centrality).
2. Extend the character test to an **entire finite D=4 uniform-Wilson block**, explicitly recording additional induced loop terms and certified errors.
3. Define a gauge-invariant locality norm for the full induced action and demonstrate a one-scale bound with explicit constants; this supplies an input, **not** a solution, to YM4-04.
4. Only subsequently consider iterated blocking, growing beta and the zero-spacing limit. Every one of those claims remains OPEN.
