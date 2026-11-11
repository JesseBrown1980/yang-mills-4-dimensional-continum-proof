# YM4-06F: complete finite 4D SU(2) Wilson transfer spectrum by a certified temporal character cutoff

**November 11, 2026.** Theorem: an **actual interacting finite-volume 4D continuous-SU(2) Wilson transfer** admits a gauge-invariant finite-rank approximation with an explicit, all-discarded-modes operator-norm error. This is a standard Peter–Weyl/Bessel method applied to this transfer kernel, **not** a claim of a new general Fourier theorem, a completed large-volume calculation, or a continuum mass gap. This branch is independent of #66 and of the finite S₃/r=9 campaign.

Twenty-two falsifiable predictions were frozen in `docs/PREDICTION-YM4-06F-FULL-WILSON-FOURIER-20261111.hbp` at `16224bc38cd21d67817539be407ca92b691949ad` **before the checker was created**.

## 1. Actual finite Wilson transfer and its exact temporal harmonic spectrum

Fix a periodic 3D spatial lattice of side `L>=2`, with `M=3L^3` spatial oriented links and `N_s=3L^3` spatial plaquettes, and positive Wilson temporal coupling `beta>0`. Work on the gauge-invariant slice Hilbert space `H_phys=L²(SU(2)^M,Haar)^gauge`. From [YM4-02c](LEMMA-0004-REFLECTION-TRANSFER.md), the positive compact temporal transfer is

[
T=A^{1/2}BA^{1/2},\quad
A(U)=\prod_{p\ \mathrm{spatial}}w_\beta(U_p),\quad
B(U,V)=\prod_{\ell=1}^{M}w_\beta(U_\ell V_\ell^{-1}),\quad
w_\beta(g)=e^{-\beta(1-\frac12\operatorname{ReTr}g)}.
]

For SU(2) spin label `n/2` (integer n>=0), its representation dimension is `d_n=n+1`; the temporal central convolution has eigenvalue

[
b_n(\beta)=e^{-\beta}\frac{2I_{n+1}(\beta)}{\beta},
\qquad
t_n(\beta):=\frac{b_n}{b_0}
=\frac{I_{n+1}(\beta)}{I_1(\beta)}.
\tag{F1}
]

Every `t_n>0`, `t_0=1`, `t_n<=1` (the normalized positive convolution is a Markov contraction). The full tensor convolution has eigenvalues `prod_l b_(n_l)` with multiplicities `prod_l(n_l+1)^2`. We normalize the **entire** temporal transfer by `b_0^M`, leaving its physical spectral ratios unchanged:

[
\widehat B=B/b_0^M,\qquad
\widehat T=A^{1/2}\widehat B A^{1/2}.
\tag{F2}
]

The character coefficient (F1), including the factor of representation dimension, agrees with standard SU(2) Wilson character expansions. Its justification is the Haar identity `∫e^(beta cos theta)chi_n=(2(n+1)/beta) I_(n+1)(beta)`, followed by Schur orthogonality. The Bessel series and character expansion are classical; **the finite-volume gauge-sector spectral enclosure below is the contribution being checked**.

## 2. An elementary uniform absolute tail bound from positive factorial terms

For integer `m>=1` and real `beta>0`,

[
I_m(\beta)=\sum_{k\ge0}
\frac{(\beta/2)^{m+2k}}{k!(m+k)!}.
\tag{F3}
]

Comparing the **k-th summand** of `I_(n+1)` with that of `I_1` gives, for all n>=0,

[
\frac{I_{n+1}(\beta)}{I_1(\beta)}
\le\frac{(\beta/2)^n}{(n+1)!}.
\tag{F4}
]

Indeed `(k+1)!/(n+k+1)!<=1/(n+1)!` term by term. No floating-point ratio theorem or asymptotic estimate is imported.

Let `Pi_N` be the product of full single-link Peter–Weyl projections on **all matrix coefficients** of irreps `0<=n<=N`, not only class functions or Wilson-loop observables. This is a finite-rank projection, commuting with independent left and right SU(2) endpoint transformations on every link and therefore with all 3D local gauge transformations. The per-link retained rank is

[
d(N)=\sum_{n=0}^{N}(n+1)^2
=\frac{(N+1)(N+2)(2N+3)}6.
\tag{F5}
]

If `N+3>=beta/2`, the factorial envelope in (F4) is nonincreasing for all `n>=N+1`; hence

[
\boxed{
\|\widehat B-\Pi_N\widehat B\Pi_N\|
\le\delta_N(\beta):=
\frac{(\beta/2)^{N+1}}{(N+2)!}.}
\tag{F6}
]

**Crucially, there is no factor M on the right.** On any omitted multi-link tensor eigenvector, *at least one* link has `n>N`, and all remaining normalized factors satisfy `0<t_n<=1`. Thus the spectral norm of the entire tensor-product tail is controlled by one omitted factor. This is an **absolute** normalized temporal-kernel bound, not a bound relative to the finite-volume Perron eigenvalue.

## 3. One-sided full physical spectral enclosure (the dark-state protection)

Define

[
\widehat T_N=A^{1/2}\Pi_N\widehat B\Pi_N A^{1/2}.
\tag{F7}
]

Because `0<A<=1` and the omitted temporal Fourier eigenvalues are all nonnegative,

[
\boxed{
0\le \widehat T-\widehat T_N\le\delta_N(\beta)I
}
\quad\text{on the entire }H_{phys}.
\tag{F8}
]

In particular this is a **Loewner order**, stronger than a mere two-sided norm error. Label eigenvalues in decreasing order `Lambda_0>=Lambda_1>=...`, counting multiplicity and remaining in the **full gauge-invariant** Hilbert space. The min-max principle gives, for **every** eigenvalue index j,

[
\boxed{
\Lambda_j(\widehat T_N)
\le\Lambda_j(\widehat T)
\le\Lambda_j(\widehat T_N)+\delta_N.
}
\tag{F9}
]

No selected observable, subspace visibility or *assumed* discarded-mode Poincare gap appears. In particular, if the finite-rank top eigenvalue `L0_N>0`, then the actual first excited ratio satisfies

[
\boxed{
\frac{L1_N}{L0_N+\delta_N}
\le r_{\mathrm{phys}}
\le\min\left\{1,\frac{L1_N+\delta_N}{L0_N}\right\}.
}
\tag{F10}
]

At finite positive beta, Perron simplicity of the **true** Wilson transfer and a strict upper bound below one give a certified physical fixed-volume first gap. A nonpositive or vacuous upper bound is **NOT MET**, not a gap certificate.

The rank-one constant-temporal component is included in `Pi_N Bhat Pi_N`. Therefore `T_N>=|sqrt A><sqrt A|`, and

[
\boxed{L0_N\ge\int A(U)\,dHaar(U)
\ge e^{-2\beta N_s}>0.}\tag{F11}
]

This elementary lower bound is exponentially bad in volume. It makes the finite theorem effective, but does **not** establish a uniform relative truncation error along a growing lattice family.

**Independent finite matrix formulation.** If `phi_i` are **orthonormal in the full product-Haar inner product** and form the complete retained Peter–Weyl matrix-coefficient basis of `Pi_N` (before optional gauge-invariant projection), and `t_i=prod_l t_(n_l)`, the nonzero eigenvalues of `T_N` equal those of the finite Gram matrix

[
G_{ij}=\sqrt{t_i t_j}\int\overline{\phi_i(U)}A(U)\phi_j(U)\,dHaar(U).
\tag{F12}
]

One can restrict this matrix to gauge-invariant combinations after forming the representation coupling, **without discarding any gauge-invariant sector**. Certified Haar moment or interval arithmetic can bound these entries and their eigenvalues independently; the formulas do **not** pretend the resulting matrix size is computationally manageable at realistic 3D L.

**Vacuum approximation if its spectral separation is certified.** Let `v_N` be a normalized top eigenvector of `T_N` in the physical sector, with `g_N=L0_N-L1_N>0`. For the normalized positive true Perron vacuum `Omega`,

[
\boxed{
\|(I-|v_N\rangle\langle v_N|)\Omega\|
\le\delta_N/g_N.}\tag{F13}
]

Project `(T_N-\Lambda_0(T))\Omega=-(T-T_N)\Omega` onto `v_N^perp`; there the distance from `\Lambda_0(T)>=L0_N` to the rest of `T_N` is at least `g_N`. Thus the exact ground-state probability measure and its coarse pushforward become approximable from a certified finite-rank Perron vector when `delta/g_N` is small. This is **conditional** on a genuinely certified finite-rank top separation, not an all-scale proof.

## 4. Exact small controls and scale limits

The independent integer/rational checker (no floats) verifies factorial cutoffs and exact positive Bessel interval ratios. Frozen cutoff rows include:

| beta | N | Exact/strict tail certificate |
|---:|---:|---|
| 2 | 8 | `1/3628800 < 10^-6` |
| 4 | 12 | `4/42567525 < 10^-7` |
| 8 | 20 | `8388608/2143861251406875 < 10^-8` |
| 16 | 40 | `delta_N < 10^-13` |

The Bessel ratio `t_1=I_2/I_1` is independently enclosed by positive rational power series at beta 2 (between 43/100 and 44/100), beta 4 (between 65/100 and 66/100), and beta 8 (between 81/100 and 83/100).

An exact **two-link Z2 finite control only** (not SU2) checks the Loewner/minmax logic with a nonconstant spatial multiplier. One-link normalized convolution has eigenvalues `1,q`, `q=1/8`; the two-link tensor has `1,q,q,q²`. Retaining the product Haar constant mode leaves a positive omitted operator with norm `q`. With rational spatial square-root weights `1,1/2,1/3,1/4`, the retained one-dimensional transfer has exact `L0_N=205/576`, while the true complete first excited eigenvalue is bounded by `1/8`. Thus `r_phys<=72/205<1`, including every omitted state. This is a control of the spectral logic, **not** a positive-gap numerical result for 4D SU2.

The checker includes exact Q8 left/right endpoint-gauge transformations of SU2 fundamental matrix-coefficient coordinates as an independent algebra control. General n gauge invariance follows from Peter–Weyl representation transformation, not from Q8 enumeration.

### Computational and proof limitations

- The global finite-rank dimension scales like `d(N)^(3L^3)`, not seconds or even remotely feasible on nontrivial spatial volumes without symmetry/reduction. No runtime claims are made.
- Although the absolute temporal tail `delta_N` is independent of M, the relative ratio `delta_N/L0_N` can be disastrous as the spatial volume increases because `L0_N` can be exponentially small. **This is not a volume-uniform physical spectral gap**.
- The actual weak-coupling SU2 trajectory and induced chair/higher Wilson-network action are not controlled by this harmonic cutoff. Neither `zeta` nor `rho` of YM4-06E has been numerically or analytically bounded for an all-scale 4D family.
- The spectrum of finite S3/HEB-C 3×4 has not been identified with continuous SU2. The r=9 launch gate and finite repo remain unchanged.

## 5. Next exact action toward 06E

The finite-rank approximation provides a **non-circular independent full-spectrum enclosure** of `r_f` and the fine Perron vacuum on each fixed finite 4D lattice. The next accepted calculation is an explicitly specified **tiny gauge-invariant continuous-SU2 spatial lattice**, evaluated from its *actual Wilson spatial Haar moment Gram matrix* with a separate rational interval checker and verified variational full-spectrum enclosures. Do not substitute Q8 or a selected Wilson observable as if it were the continuous model.

For the 06E block-error route, once the true vacuum/coarse pullback is enclosed, compute
[
\zeta=\|(I-E)S_fJ\|,qquad
\rho=\| (I-E)S_f(I-E)|_W\|,
]
and bound the remaining Fourier tail using (F8). Without these complete-physical-sector bounds, the Law 70 all-scale inequality stays OPEN.

### Prior work and references

- [YM4-02c](LEMMA-0004-REFLECTION-TRANSFER.md), finite Wilson positive transfer.
- [YM4-06C/D/E](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/66), full-spectrum two-block comparison, exact induced Wilson vacuum isometry and memory norm.
- Classical transfer positivity: M. Lüscher (1977), *Construction of a selfadjoint, strictly positive transfer matrix for Euclidean lattice gauge theories*, Communications in Mathematical Physics 54, 283–292, DOI 10.1007/BF01614090.
- Classical SU2 character coefficients: `exp(-S_p)=sum_r d_r c_r(beta) chi_r(U_p)`, `c_r=e^-beta 2I_(2r+1)(beta)/beta` (e.g. standard lattice gauge representation theory).
- Bessel factorial series: DLMF, `I_m(beta)=sum_(k>=0) (beta/2)^(m+2k)/(k!(m+k)!)`.

**Status: actual finite Wilson all-spectrum harmonic approximation theorem DERIVED under standard SU2 harmonic facts, finite exact checker pending hosted and independent review; physical continuum mass gap OPEN.**
