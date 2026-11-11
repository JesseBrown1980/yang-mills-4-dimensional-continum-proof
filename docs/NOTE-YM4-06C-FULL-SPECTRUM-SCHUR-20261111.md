# YM4-06C: a complete-physical-spectrum Schur certificate for the triadic gap budget

**Date:** November 11, 2026. **Status:** DERIVED **conditional operator theorem**, exact finite rational falsifier, actual 4D SU(2) operator estimates OPEN. This is not a claim of an interacting continuum or a physical Yang–Mills gap. It is not an optimization of the YM4-04C F20/Fuss–Catalan bound.

**Dependency and provenance.** The original 16 predictions were frozen in `docs/PREDICTION-YM4-06C-FULL-SPECTRUM-SCHUR-20261111.hbp` at `13bbb8bc33c4b89b46c787f75b985554a79d381b` before the present checker was written. This work is on its own branch from main `05de0ff7`; the original finite-lattice repo, r=9 launch and draft PRs #34/#64/#65 are unchanged.

## 1. The physical operators and the missing bridge

The Wilson transfer of [YM4-02c](LEMMA-0004-REFLECTION-TRANSFER.md) at finite spatial volume, positive bare beta and a specified reflection/temporal convention is a positive self-adjoint operator `T_a` on the gauge-invariant slice Hilbert space. Let its simple Perron vacuum be `Omega_a` with eigenvalue `lambda_0(a)>0`. Write

[
S_a:=T_a/\lambda_0(a),\qquad
S_a\Omega_a=\Omega_a,\qquad 0\le S_a\le I.
]

Define the **full** first excited ratio (all gauge-invariant sectors, not a chosen Wilson observable)

[
r_a:=\|S_a\vert_{\Omega_a^\perp}\|_{op}\in[0,1),\qquad
\gamma_a=-\ln r_a,\qquad m_a=\gamma_a/a.
]

At two adjacent scales `a_c=3a_f`, let `H_c,H_f` denote their gauge-invariant physical Hilbert spaces. We **require** a gauge-compatible isometry `J:H_c -> H_f` satisfying `J Omega_c=Omega_f`. This is a mathematical hypothesis requiring a construction from the *actual* four-dimensional interacting measure. Gauge covariance of a coarse-link configuration map `B` alone does **not** provide it.

One possible construction to investigate is the positive-ground-state Doob transform: the normalized Wilson transfer induces a reversible Markov operator on `L^2(dmu_a)`, `dmu_a=Omega_a^2 dHaar`, with vacuum `1`. If `mu_c=B_*mu_f` exactly, then `(Jf)(U)=f(BU)` is an isometry preserving the vacuum. But the **Euclidean** gauge-action pushforward in YM4-03 does not automatically imply `mu_c=B_*mu_f` for the time-slice ground-state measures, nor that the coarse Markov transfer is the compressed fine semigroup. Both are separately OPEN.

## 2. The direct block theorem: a full-spectrum, falsifiable bound

Let `P=J J^*` be the orthogonal projection onto the retained subspace (which includes the fine vacuum). Split the **entire** fine vacuum complement orthogonally:

[
H_f\ominus\mathbb C\Omega_f
=
U\oplus W,\qquad U=J(H_c\ominus\mathbb C\Omega_c),
\quad W=(I-P)H_f.
]

The fine positive transfer restricted to this complete vacuum complement has a self-adjoint 2-block form

[
M=
\begin{pmatrix}A & Z^*\\Z&D\end{pmatrix},
\quad
A=J^*S_fJ\vert_{\Omega_c^\perp},
\quad
Z=(I-P)S_fJ\vert_{\Omega_c^\perp},
\quad
D=(I-P)S_f(I-P)\vert_W.
]

Let `S_c` be the actual normalized coarse transfer, `r_c=||S_c|Omega_c^perp||`. The **three distinct nontrivial analytic obligations** are

[
\boxed{\|A-(S_c\vert_{\Omega_c^\perp})^{1/3}\|\le\alpha,\qquad
\|Z\|\le\zeta,\qquad
D\le\rho I_W.}
\tag{C1}
]

The second bound measures retained-to-discarded **memory leakage**; the last caps the **entire dark/fast physical complement**. None is implied by small Wilson-loop matching error or by the exact matrix-jump law.

Set `u=r_c^(1/3)+alpha`. Suppose a threshold `tau` satisfies

[
\boxed{\tau\ge u,\quad\tau\ge\rho,\quad
(\tau-u)(\tau-\rho)\ge\zeta^2.}
\tag{C2}
]

**Theorem (full-spectrum Schur step).** Under (C1)-(C2),

[
\boxed{
r_f=\|S_f\vert_{\Omega_f^\perp}\|\le\tau.}
\tag{C3}
]

**Proof.** For any `x in U`, `y in W`, use the operator bounds and Cauchy-Schwarz:

[
\langle(x,y),(\tau I-M)(x,y)\rangle
\ge(\tau-u)\|x\|^2+(\tau-\rho)\|y\|^2
-2\zeta\|x\|\|y\|.
]

The scalar 2×2 matrix with diagonal `tau-u,tau-rho` and offdiagonal `-zeta` is positive semidefinite precisely when (C2) holds. Therefore `tau I-M>=0` on the **complete** fine vacuum complement and (C3) follows. Neither the finite dimension nor an observable-overlap assumption enters this argument. QED.

For `rho<u`, the optimal scalar Schur threshold is

[
\tau_*=
\frac{u+\rho+\sqrt{(u-\rho)^2+4\zeta^2}}2
=u+\frac{2\zeta^2}{\sqrt{(u-\rho)^2+4\zeta^2}+(u-\rho)}
\le u+\frac{\zeta^2}{u-\rho}.
]

The last bound exhibits the useful **quadratic leakage penalty** when the discarded spectrum is separated from the retained block. If `rho` is near one, there is no such leverage and the theorem must report HOLD rather than hide the dark excitation.

## 3. Conversion into Law 70 with independently certified physical errors

Assume a 4D gauge-theory calculation supplies explicit `alpha_k,zeta_k,rho_k` and a threshold `tau_k` satisfying (C2) for the actual fine and coarse Wilson transfers, **without using the unknown fine first gap**. To obtain the desired positive physical gap, require for some explicit `x_k>=0`:

[
\tau_k\le r_k^{1/3}(1+x_k),\qquad
\sum_{k\ge0}\frac{x_k}{a_{k+1}}<m_0.
\tag{C4}
]

Then (C3) gives `r_(k+1)<=r_k^(1/3)(1+x_k)`; taking logs and using `ln(1+x)<=x` yields

[
m_K\ge m_0-\sum_{k=0}^{K-1}\frac{\ln(1+x_k)}{a_{k+1}}
\ge m_0-\sum_{k=0}^{K-1}\frac{x_k}{a_{k+1}}>0.
\tag{C5}
]

Thus **a full first-gap comparison follows from external, independently auditable operator bounds**. Unlike defining epsilon from the exact unknown gaps, (C1)-(C4) are concrete upper bounds on blocks of an explicitly specified physical transfer operator. The open work is obtaining such bounds for interacting 4D SU(2) at arbitrarily small spacing.

For an illustrative budget `a_0=1`, `a_(k+1)=3^(-k-1)`, `x_k=a_(k+1)^2/64`, one has the exact sum

[
\sum_{k\ge0}x_k/a_{k+1}=1/128.
]

Since `ln2>1/2>1/128`, a hypothetical family with `m_0=ln2` satisfying these actual operator inequalities would have `m_K>=ln2-1/128>0`. **This sequence is a target for independently verified errors, not a bound we have obtained from Yang–Mills dynamics.**

## 4. Exact compression does not provide the required direction

Let `P=JJ^*`, `B=J^*S_fJ`, `Z=(I-P)S_fJ`, `D=(I-P)S_f(I-P)|_W` where now W is the entire discarded subspace. For any bounded self-adjoint fine transfer `S_f`, direct matrix multiplication yields the **memory identities**

[
\boxed{J^*S_f^2J-B^2=Z^*Z\ge0,}
\tag{C6}
]

[
\boxed{J^*S_f^3J-B^3
=BZ^*Z+Z^*ZB+Z^*DZ.}
\tag{C7}
]

If `0<=S_f<=I`, then `||B||,||D||<=1`, hence `||J^*S_f^3J-B^3||<=3||Z||^2`.

**Exact coarse three-tick correlations do not imply Markov closure.** In fact, defining `S_c=J^*S_f^3J` yields, by a simple Rayleigh quotient over `J(H_c\ominus Omega_c)`,

[
\boxed{r_c\le r_f^3.}
\tag{C8}
]

This is an **upper** bound on the coarse excited ratio, hence a **lower** bound on the fine ratio: the reverse of (C3). This formula cannot prove the physical mass gap. For physical SU(2) it is also necessary to establish the relation between the exact induced coarse transfer and a chosen Wilson-network effective action; Euclidean coarse-link identities alone cannot do that.

The two-step identity (C6) identifies the missing information exactly: the memory operator `Z`, not a numerical time-jump discrepancy that can be assumed zero.

## 5. Frozen exact rational tests (no float)

**Positive mixed-mode control.** On an orthonormal basis `(vacuum, retained, discarded)`, let

[
S_f=\begin{pmatrix}
1&0&0\\0&1/2&1/16\\0&1/16&1/4
\end{pmatrix},\qquad
S_c=\operatorname{diag}(1,1/8),\quad
J(e_0)=e_0,\ J(e_1)=e_1.
]

Here `A=(1/2)`, `alpha=0`, `Z=1/16`, `D=1/4`. Thus `u=1/2`. The exact upper threshold `tau=33/64` passes:

[
(33/64-1/2)(33/64-1/4)=17/4096\ge 16/4096=(1/16)^2.
]

The tighter false `tau=65/128` fails: `33/16384<64/16384`. The actual fine first ratio is strictly greater than 1/2 because the characteristic polynomial of the 2×2 complement is negative at 1/2, yet the full Schur theorem certifies it **less than 33/64**.

The exact leakage readouts are `J^*S_f^2J-B^2=1/256` and `J^*S_f^3J-B^3=5/1024` on the excited retained component. The hypothetical `S_c=diag(1,1/8)` is **not** the exact three-tick compression in this mixed model: the latter has excited value `133/1024`. This difference is deliberately retained.

**Dark-mode negative control.** Replace the matrix with `S_f=diag(1,1/2,3/4)` and keep `J` as before. Exact compression yields `J^*S_f^3J=diag(1,1/8)`; nevertheless `r_f=3/4>1/2=r_c^(1/3)`. Here `Z=0` but `rho=3/4`. Any alleged theorem omitting the discarded spectrum falsely passes the dark mode, whereas (C2) correctly **rejects** `tau=1/2` because `tau<rho`.

Both are abstract positive-semidefinite transfer models in a vacuum/eigenobservable basis, **not** complete Wilson lattice Gibbs kernels or physical gauge-group constructions. They are counterexamples and controls for the operator inequality, not evidence that the 4D theorem has been achieved.

The exact-integer checker `tests/test_ym4_06c_full_spectrum_schur.py` checks the 2×2 determinant, rational 3×3 powers and leakages, the dark mode, the product bounds and the budget. Six named source mutations alter the computed matrices or threshold and must be rejected. Hosted final-head and independent human mathematical review are mandatory.

## 6. The actual 4D SU(2) proof obligations

1. **Fix the physical transfer and time spacing.** Use the positive self-adjoint Wilson transfer on the entire gauge-invariant slice Hilbert space, normalized by its *true* Perron eigenvalue. Its Doob ground-state measure must be specified; positivity and a finite-lattice Perron vacuum are already available in YM4-02c/d.
2. **Construct a genuine vacuum-preserving gauge-blocking isometry.** Show that the induced *ground-state* coarse measure matches the chosen coarse transfer's vacuum measure, or furnish an explicit change-of-measure correction with a quantitative vacuum-alignment error. The finite Euclidean pushforward YM4-03 proves a different identity.
3. **Bound the retained operator error `alpha_k`.** Compare `J^*S_fJ` against the positive cube root of the **actual coarse transfer**, with all chair, multiloop and higher-character interactions kept or certified in error.
4. **Bound both leakage `zeta_k` and complete dark spectrum `rho_k`.** A chosen Wilson-loop observable, selected character sector, finite Ritz subspace or magnetic high-cluster floor cannot replace the `D<=rho I` inequality. An anchored local Poincare/conditional variance estimate or complete Feshbach/inertia bound is a candidate method, not yet an achieved physical result.
5. **Prove all-scale geometry and a summable physical budget.** Compute certified `tau_k`, including the correct temporal spacing; require (C4) **for every k** and strict margin below `m_0`. A finitely sampled sequence does not certify induction.
6. **Keep existence separate.** Nontrivial continuum Euclidean correlators, the full OS axioms and infinite-volume uniformity remain independently open even if a fixed-physical-volume spectral bound were proved. SU(2) alone would not settle the all-compact-simple-groups Clay statement.

**Current status:** (C2)-(C8) are conditional operator algebra, independent of strong-coupling F20 and consistent with PR #34's failure; **none of `alpha,zeta,rho` is yet bounded for the actual 4D Wilson refinement family**. This is a testable theorem interface, not a solved mass-gap problem.

## Relevant previous work

- [YM4-02c: finite Wilson reflection-positive transfer](LEMMA-0004-REFLECTION-TRANSFER.md).
- [YM4-03: exact gauge-equivariant coarse-link map and Euclidean measure pushforward](NOTE-YM4-03-ONE-SCALE-BLOCKING.md).
- [YM4-03C: genuine chairs and higher SU(2) Wilson networks in the blocked effective action](NOTE-YM4-03C-BLOCKED-ACTION.md).
- [PR #34: collapsing-gap and dark-mode counterfamilies](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/34).
- [PR #65: exact strict-budget falsifier](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/65).
- Osterwalder–Seiler (1978), *Gauge field theories on a lattice*, Annals of Physics 110, 440-471, https://doi.org/10.1016/0003-4916(78)90039-8.
- Recent related published claims on reflection-positive spectral gap persistence: Faizal–Shabir, *Reflection-positive renormalization and the persistence of the mass gap in lattice SU(N) Yang–Mills: Part (2)*, IJGMMP 24 (2026), DOI https://doi.org/10.1142/S0219887826501136; its full proof is embargoed and not independently accepted or imported here.
