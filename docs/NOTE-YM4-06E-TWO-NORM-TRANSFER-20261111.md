# YM4-06E: two-norm full-spectrum certificate for the *actual induced* 4D Wilson transfer

**Date:** 2026-11-11. **Status:** DERIVED abstract-operator and actual finite-Wilson conditional-variance identities; **no uniform all-scale SU(2) leakage or dark-sector norm established**. Independent mathematical review and hosted final-head checks required. This does not prove continuum Yang–Mills or the Clay mass gap.

This note is a sharpening of [YM4-06C](NOTE-YM4-06C-FULL-SPECTRUM-SCHUR-20261111.md) and its actual finite-SU(2) isometry construction [YM4-06D](NOTE-YM4-06D-WILSON-VACUUM-ISOMETRY-20261111.md). **It eliminates the separate retained-spectrum matching error alpha** when the coarse transfer is defined by the *exact three-tick induced Wilson transfer*, instead of a separately assumed single-coupling Wilson operator.

**Prediction-first freeze:** fourteen E-rows in `docs/PREDICTION-YM4-06E-TWO-NORM-TRANSFER-20261111.hbp`, commit `98764e26125efdd1e6363ffc827686d024ed0e1e`, precede the independent E-checking code.

## 1. Actual finite-Wilson objects

Work on the finite 4D continuous SU(2) Wilson lattice, with the *normalized positive and reversible Perron/Doob transfer* `P_f` and the canonical vacuum-preserving spatial factor-three isometry `J` constructed analytically in YM4-06D. Thus `J1=1`, `J*J=I`, and `E=JJ*` is orthogonal conditional expectation on the fine vacuum measure onto functions of the coarse spatial links `B3U`.

Define

[
B=J^*P_fJ,\qquad
Z=(I-E)P_fJ,\qquad
D=(I-E)P_f(I-E)\vert_{(I-E)\mathcal H_f}.
]

The induced three-fine-tick coarse transfer is

[
\boxed{P_c=J^*P_f^3J.}\tag{E1}
]

This is a positive self-adjoint Markov contraction with top eigenvalue 1 and Perron vector 1. Let `r_c` be the **whole gauge-invariant vacuum-orthogonal spectral ratio** of this actual induced coarse operator, and `r_f` that of `P_f`.

Two **open** scale-dependent norms remain:

[
\boxed{
\zeta=\|Z\|_{op},\qquad
\rho=\|D\|_{op}.
}\tag{E2}
]

The norms are restricted to the gauge-invariant physical space and its complete non-vacuum complement. `rho` is not a high-cluster floor or a chosen Wilson-loop eigenvalue.

## 2. Exact positive two-tick memory is a conditional variance

The general identity already established in YM4-06D at n=1 gives

[
J^*P_f^2J-B^2=Z^*Z\ge0,\qquad
\boxed{\zeta^2=\|J^*P_f^2J-B^2\|_{op}.}\tag{E3}
]

In the Doob ground-state `L^2(\mu_f)` representation, `E=JJ*` is the conditional expectation given the coarse gauge links `B_3U`. For a normalized coarse physical observable `h\perp1` and `g=h\circ B_3`,

[
\|Z h\|^2
=\int \operatorname{Var}_{\mu_f}\bigl((P_f g)(U)\mid B_3U\bigr)\,d\nu_c.
\tag{E4}
]

Therefore the **operator norm over all gauge-invariant coarse observables** of this conditional-variance functional is exactly `zeta^2`. This is a genuine all-observable Wilson definition, not a selected correlation function.

The discarded-space estimate `D\le\rho I` is equivalently the exact conditional-fiber Poincare/Dirichlet target

[
\langle h,P_f h\rangle\le\rho\|h\|^2
\quad\text{for all gauge-invariant }h\text{ with }
\mathbb E_{\mu_f}[h\mid B_3U]=0.
\tag{E5}
]

These are now **specific mathematical quantities** for the actual Wilson path/block construction. Their independent scale-uniform bounds are still not proved.

## 3. Eliminate alpha using the exact three-tick memory identity

From [YM4-06C](NOTE-YM4-06C-FULL-SPECTRUM-SCHUR-20261111.md) with `||B||,||D||<=1`,

[
P_c=B^3+BZ^*Z+Z^*ZB+Z^*DZ
quad\Longrightarrow\quad
\|P_c-B^3\|\le3\zeta^2.
\tag{E6}
]

All operators preserve the vacuum, and the error annihilates it, so restrict to the coarse vacuum complement. Since `B\ge0`, its spectral norm obeys `||B_0^3||=||B_0||^3`. Hence

[
\boxed{
\|B_0\|^3\le r_c+3\zeta^2.}
\tag{E7}
]

Thus there is **no need to independently certify an operator-norm error between B and the cube root of P_c**. A certified nonnegative `u` satisfying

[
\boxed{u^3\ge r_c+3\zeta^2}
\tag{E8}
]

already bounds the retained excited spectrum.

**Theorem (two-norm true-first-gap Schur certificate).** If for a fine and induced-coarse Wilson pair, `u,tau` satisfy

[
u^3\ge r_c+3\zeta^2,\quad
\tau\ge u,\quad\tau\ge\rho,\quad
(\tau-u)(\tau-\rho)\ge\zeta^2,
\tag{E9}
]

then the complete fine physical excited spectrum obeys

[
\boxed{r_f\le\tau.}\tag{E10}
]

**Proof.** (E6)-(E8) bound the retained block `B_0\le uI`. The full vacuum complement is the orthogonal sum of `J\mathcal H_c^0` and the discarded space. Its transfer blocks have retained cap u, discarded cap rho, and coupling norm zeta. The 2×2 Schur quadratic-form estimate of YM4-06C implies `tau I-P_f|_{1^perp}\ge0` under the final three tests of (E9). Therefore `r_f\le tau`. **No low-mode observability or finite-dimensional truncation is assumed.** QED.

If `\zeta=0`, the retained coarse range is invariant, `P_c=B^3` and the exact equality is `r_f=max(r_c^{1/3},\rho)`. This shows why a separate discarded-space estimate remains mandatory even with perfect coarse three-tick correlators.

## 4. Exact rational controls

**Mixed-mode positive control** from YM4-06C:

[
P_f=
\begin{pmatrix}1&0&0\\0&1/2&1/16\\0&1/16&1/4\end{pmatrix},
\quad J(e_0)=e_0,\ J(e_1)=e_1.
]

Its genuinely **induced** three-tick coarse excited ratio is `r_c=133/1024`, and `zeta^2=1/256`, `rho=1/4`. Thus `r_c+3 zeta^2=145/1024=4640/32768`. Choose `u=17/32`, whose cube is `4913/32768`, and `tau=35/64`. Then

[
(\tau-u)(\tau-\rho)
=\frac1{64}\frac{19}{64}
=\frac{19}{4096}
\ge\frac{16}{4096}=\zeta^2.
]

So (E9) independently certifies the **entire** fine first excited eigenvalue ratio at most `35/64`, without using the exact 2×2 eigenvalue and without assuming the coarse operator is a Wilson single-coupling family. It is a *conservative* bound; YM4-06C's separate hypothetical-coarse comparison gives the sharper `33/64`.

**Dark negative control:** `P_f=diag(1,1/2,3/4)` with the same J has `r_c=1/8`, `zeta=0`, `rho=3/4`. Choosing `u=1/2` is admissible but `tau=1/2` violates `tau>=rho`. The criterion correctly refuses a false global physical first-gap preservation, even when coarse three-tick blocking matches perfectly.

**Exact positivity controls:** a too-small u with `u^3<r_c+3 zeta^2` or an omitted discarded spectral block must be rejected. The E-specific independent rational checker tests these as altered-input failures, not simply text comparisons.

## 5. What is next on actual 4D Wilson, not another toy optimization

1. **Prove a uniform upper bound on zeta** by estimating the conditional variance (E4) of the *time-evolved coarse Wilson-network algebra* given the exact coarse spatial links. This has to hold for all coarse gauge-invariant `L^2` observables with norm one, not a finite list of Wilson loops.
2. **Prove a uniform upper bound on rho** as a conditional-fiber Poincare/spectral theorem (E5) for *every discarded gauge-invariant excitation*. A single dark slow mode falsifies the gate. A candidate proof may use a gauge-covariant block conditional spectral inequality with explicit constants; no such inequality has yet been established in this repo.
3. **Control r_c** of the full induced coarse transfer (or compare it rigorously with a physical reflection-positive local coarse network action), then find `u_k,tau_k` satisfying (E9) and the strict physical Law 70 budget:
[
\tau_k\le r_{c,k}^{1/3}(1+x_k),\qquad
\sum_k x_k/a_{k+1}<m_0.
]
4. Keep the full continuum existence and OS reconstruction proof separate. Fixed finite Wilson isometry and transfer bounds alone do not settle the problem.

**Status:** the proposed RG spectral theorem interface is now reduced to **two independently bounded physical operator norms plus the induced coarse spectrum**, and is proved *conditionally* for every finite 4D Wilson lattice. Uniform estimates for the actual weak-coupling refinement family, all-scale spectral preservation and Clay existence/mass gap remain OPEN. No unrelated PRs or finite r9 operations are touched.

## Research context

This is the full-spectrum operator version of Law 70 with explicit leakage and dark-state controls. It is based on standard Hilbert-space/Schur complement arguments and existing finite-Wilson transfer positivity, not a claim of novel resolution of the Millennium problem. Related 2026 published discussions of reflection-positive renormalization and spectral persistence exist (e.g. DOI 10.1142/S0219887826501136), but their detailed hypotheses were not imported or audited because the available full text is restricted.
