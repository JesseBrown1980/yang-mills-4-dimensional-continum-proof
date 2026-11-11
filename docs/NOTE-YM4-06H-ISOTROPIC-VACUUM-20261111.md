# YM4-06H — improved isotropic SU(2) Wilson Perron floor from exact spatial Haar moments

**2026-11-11. Scope:** a rigorously proved finite-lattice **isotropic, interacting, continuous-SU(2) Wilson** lower bound on the leading temporal-transfer eigenvalue, valid for all `beta>=0` and periodic spatial sides `L>=2`. The correction addresses remark 3 of the independent reviewer on [PR #67](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/67#issuecomment-6809515886). This is *not* an independently evaluated full interacting 4D spectrum or a uniform physical gap.

The 16 prediction rows in `docs/PREDICTION-YM4-06H-ISOTROPIC-VACUUM-20261111.hbp` were frozen at `0326f97ec5e50e3f134dd7c59515689d35e68d37` **before** this note and the independent exact-int checker. The F/G predictions are unchanged.

## 1. Exact spatial Haar mean and covariance on the actual isotropic lattice

Let `L>=2` and let `N_s=3L^3` be the distinct spatial plaquettes of the periodic 3D cubic lattice, with normalized independent SU(2) Haar measure on all spatial links. Write

[
a_p(U)=\frac12\operatorname{ReTr}U_p,\quad X(U)=\sum_{p=1}^{N_s}a_p(U),\quad
A(U)=\prod_{p=1}^{N_s}e^{-\beta(1-a_p(U))}=e^{-\beta N_s}e^{\beta X(U)}.
]

Each plaquette uses four distinct oriented links for `L>=2`; conditioning on any one makes its holonomy Haar. Thus

[
\mathbb E_H a_p=0,\qquad
\mathbb E_H a_p^2=\frac14.
\tag{H1}
]

The second identity follows from SU(2) fundamental character orthogonality: `a_p=chi_(1/2)(U_p)/2` and `int chi_(1/2)^2 dHaar=1`.

For two **distinct** spatial plaquettes `p != q`, their underlying link supports are never identical; in fact, they overlap in at most two links for side 2 and at most one for side >=3 (on a cubic torus). Therefore there is at least one link appearing in precisely one of `p,q`; Haar integration of that unpaired fundamental matrix coefficient gives

[
\mathbb E_H[a_pa_q]=0\qquad(p\ne q).
\tag{H2}
]

Hence, exactly for all periodic `L>=2`,

[
\boxed{
\mathbb E_H X=0,\qquad \mathbb E_H X^2=N_s/4.
}\tag{H3}
]

This is **not a claim of probabilistic independence** of the plaquette traces; it is only the exact first two moment identities. The checker reproduces all plaquette incidence/cross-support cases at `L=2,3,4` with integer geometry. No finite subgroup is substituted for continuous-SU(2) Haar in (H1)-(H3).

## 2. Uniform elementary exponential lower bound for signed fluctuations

For every real `t`,

[
\boxed{e^t\ge1+t+\frac{t^2}{2+|t|}.}
\tag{H4}
]

For `t>=0`, use the nonnegative Taylor series and `2+t>=2`. For `t=-u<0`, this is equivalent to
`(u+2)e^{-u}>=2-u`. At `u=0` equality holds and the derivative of the difference equals `1-(1+u)e^{-u}>=0`, because `e^u>=1+u`. Thus (H4) holds globally, not just on positive field fluctuations.

Since `|X|<=N_s` and `beta>=0`, apply (H4) to `t=beta X`. The exact moments (H3) give

[
\begin{aligned}
\int A(U)dH(U)
&=e^{-\beta N_s}\mathbb E_H e^{\beta X}\\
&\ge e^{-\beta N_s}\left(1+\beta\mathbb E X+
\frac{\beta^2\mathbb E X^2}{2+\beta N_s}\right)\\
&=\boxed{
e^{-\beta N_s}\left(1+\frac{\beta^2N_s}{4(2+\beta N_s)}\right).}
\end{aligned}\tag{H5}
]

The earlier F11 bound was `exp(-2beta N_s)`; even ordinary Jensen gives `exp(-beta N_s)`. The positive variance correction above improves Jensen again with an explicit elementary rational factor.

The actual interacting normalized Wilson transfer `T_hat_N=A^(1/2) Pi_N B_hat Pi_N A^(1/2)` of 06F still satisfies `T_hat_N>=|sqrt(A)><sqrt(A)|`, because `Pi_N B_hat Pi_N` includes the normalized temporal Haar-constant mode with eigenvalue 1. The min-max principle therefore yields the *new actual transfer Perron floor*

[
\boxed{
\lambda_0(T_{N})\ge e^{-\beta N_s}\left(1+\frac{\beta^2N_s}{4(2+\beta N_s)}\right).
}\tag{H6}
]

**This does not assert that the top eigenvalue is attained on the constant mode.** It is a Rayleigh lower bound in a rank-one comparison.

## 3. Concrete isotropic point: L=2, beta=2

Here `N_s=3*(2^3)=24`, so the old F11 floor was `e^{-96}`; Jensen alone yields `e^{-48}`, and (H6) yields

[
\boxed{\lambda_0(T_N)\ge\frac{37}{25}e^{-48}.}\tag{H7}
]

The 06F Fourier-tail bound at this coupling is `delta_N=1/(N+2)!`. We can compare it **without using any floating point**. The positive series `e=sum_(k>=0)1/k!` and the tail ratio after the seventh term give

[
e<\sum_{k=0}^{6}\frac1{k!}+\frac{8}{7\cdot7!}<\frac{87}{32}.
\tag{H8}
]

Direct exact integer cross-products show

[
\frac1{22!}
<
\frac{37}{25}\left(\frac{32}{87}\right)^{48}
<
\frac{37}{25}e^{-48}
\le\lambda_0(T_{20}).
\tag{H9}
]

Thus **at Fourier cutoff `N=20`**, the absolute omitted temporal-transfer norm is already smaller than a proved lower bound on the true full-volume Perron normalization, at this **actual isotropic continuous-SU(2)** point.

It is emphatically **not enough to assert a positive spectral gap**: we have computed neither `lambda_1(T20)` nor a non-vacuous margin in `(lambda_1+delta)/lambda_0`.

For contrast, at `N=19`, the rational sufficient comparison with this deliberately elementary certified floor fails:

[
\frac1{21!}>
\frac{37}{25}\left(\frac{32}{87}\right)^{48}.
\tag{H10}
]

The `N=20` retained *per-link* matrix coefficient dimension is `sum_(m=1)^21 m²=3311`, and the full (before gauge-invariant projection) tensor rank is `3311^{24}` at `L=2`: the huge cost remains a blocker. **This is a sharper spectral normalization estimate, not a practical full-spectrum diagonalization.**

## 4. Accepted next target: actual interacting spectral matrix rather than only a floor

The mathematical next step is to construct the **isotropic** finite Wilson Gram matrix (F12) using a **complete orthonormal product-Haar Peter–Weyl basis**, first on a symmetry/gauge-reduced small spatial lattice, and to bound the first two spectral levels independently. A certified matrix enclosure must retain every physical gauge-invariant excitation, and the omitted Fourier tail must be compared against its certified leading eigenvalue and first-gap margin.

Once a true finite interacting spectral enclosure exists, combine it with the full-spectrum induced-Doob Schur construction in [PR #66](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/66) to attempt physical leakage and discarded-fiber spectral bounds. No all-scale weak-coupling error budget, nontrivial continuum OS reconstruction or Yang–Mills mass gap is proved.

## 5. Evidence and reviewer boundary

The separate exact integer checker `tests/test_ym4_06h_isotropic_vacuum.py` performs periodic spatial incidence for `L=2,3,4`, rational Haar moment coefficients, the precise `37/25` coefficient, factorial/exponential rational comparison, and rank, with five independent sabotage-style controls that must fail. The universal (H1)-(H6) results are analytic; finite incidence tests do not replace their proofs.

The independent Opus 5.5 review of 06F/06G was **reading and hand arithmetic** only; it did not independently execute the frozen test files or compute the isotropic spectrum. Its three remarks are recorded here and in F12. No promotion to merge approval. The original prediction files of 06F/06G remain unchanged. The floor-freeze round-four work, finite repo and r=9 launch HOLD are untouched.
