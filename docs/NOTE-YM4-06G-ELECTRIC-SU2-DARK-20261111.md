# YM4-06G — continuous SU(2) gauge-invariant dark modes under exact tripling

**November 11, 2026. Status: exact spectral theorem in a special 3+1D continuous-SU(2) anisotropic Wilson model, with separate integer controls.** This is a **negative control for the proposed YM4-06E fast-discarded-sector hypothesis**, not an obstruction to the isotropic 4D Yang–Mills physical mass gap. It is also not a new general spin-network theorem.

Predictions frozen at `1cd8592f7f04c6b7e90ed63ddfdaa3e241b3f7fe` in `docs/PREDICTION-YM4-06G-ELECTRIC-SU2-DARK-20261111.hbp` **before** this note and its test were added.

## 1. The actual continuous SU(2) model under test

Take a periodic 3D spatial lattice of side `L_f=3L_c`, `L_c>=4`, with a Euclidean temporal direction. In an **anisotropic SU(2) Wilson action**, retain positive temporal plaquette coupling `beta_t=2` and set the *spatial plaquette coupling to zero*: `beta_s=0`. This is a legitimate 4D lattice gauge probability model, but **is not isotropic Wilson YM at beta_s=beta_t**.

Its positive spatial-slice transfer operator, restricted to the **gauge-invariant physical Hilbert space**, is the product of independent continuous-SU2 single-link central convolutions. Normalize it to a Markov operator `P_f` with Perron vacuum the constant 1 and stationary measure product Haar. Each link's complete SU2 matrix-coefficient irrep `n` is an eigenmode with eigenvalue

[
t_n(2)=\frac{I_{n+1}(2)}{I_1(2)}.
\tag{G1}
]

The independent exact rational positive-series enclosure in [YM4-06F](NOTE-YM4-06F-FULL-WILSON-FOURIER-20261111.md) proves `43/100<t_1<44/100`. The factorial termwise bound (F4) at beta=2 shows `0<t_n<=1/(n+1)!<=1/6<t_1` for all `n>=2`. Thus `t_1` is the **largest nontrivial** temporal-link eigenvalue, and no unexamined higher spin can overtake it.

## 2. Complete gauge-invariant physical fine first excitation

In a periodic nearest-neighbor cubic graph with side `L>=4`, there are **no spatial cycles of length 1, 2 or 3**; a plaquette is a length-4 cycle. In a Peter–Weyl/spin-network gauge-invariant basis, a nonconstant state cannot have a nontrivial link representation at a degree-one vertex, so the support of its nontrivial link representations must contain a closed graph cycle of at least four links.

Because each nontrivial link contributes an eigenvalue at most `t_1` and all other link eigenvalues lie in `(0,1]`, all nontrivial gauge-invariant transfer eigenvalues are at most `t_1^4`. The fundamental plaquette character `chi_1(U_p)`, which is gauge invariant, mean-zero under Haar and uses exactly four distinct links, **achieves** eigenvalue `t_1^4`. Hence

[
\boxed{r_f=t_1^4.}\tag{G2}
]

This is the first eigenvalue ratio for the **entire** physical gauge-invariant Hilbert space in this anisotropic model, not just a chosen Wilson-loop signal.

## 3. The genuinely induced coarse transfer, and why leakage is zero

Use the factor-three spatial link map `B_3` from YM4-06D and the exact product-Haar pullback `Jf=f\circ B_3`. The single-link transition noise in the temporal Markov convolution is central, so replacing three independent fine link variables by their product gives the *three-fold convolution* on each coarse link. This works despite noncommutativity: the intervening group rotations conjugate the independent noise variables, and central Haar densities are unchanged by those conjugations.

Therefore **the entire coarse pullback subspace is invariant under the fine time transfer**:

[
P_f J=J\widetilde P_c,\qquad
\widetilde P_c=J^*P_fJ.
\tag{G3}
]

On coarse irrep n on a given link, `Ptilde_c` has eigenvalue `t_n^3`. Since the coarse side is `L_c>=4`, the same spin-network minimum-cycle proof gives

[
\|\widetilde P_c\vert_{1^\perp}\|=t_1^{12}.
\]

At **three fine time ticks per coarse tick**, the actual induced transfer is

[
P_c^{ind}=J^*P_f^3J=\widetilde P_c^3,qquad
\boxed{r_c=t_1^{36},\quad r_c^{1/3}=t_1^{12}.}
\tag{G4}
]

The 06E leakage `Z=(I-JJ^*)P_fJ` is **exactly zero** here, hence `zeta=0` and the coarse transfer is an exact semigroup. That is not enough to control the full physical first gap.

## 4. An explicit discarded *physical* slow excitation

Choose an elementary fine plaquette in the (0,1) spatial plane based at `x=(1,1,1)`. All four links of this plaquette lie **outside every coarse straight three-link path**: their third coordinate is 1, whereas coarse (0,1) link paths have third coordinate divisible by 3. Thus its normalized character `h(U)=chi_1(U_p)` depends only on off-path Haar links and has conditional expectation zero given all coarse-link products:

[
\boxed{J^*h=\mathbb E[h\mid B_3U]=0.}
\tag{G5}
]

It is **gauge invariant** and, by (G2), is a fine eigenfunction of eigenvalue `t_1^4`. Therefore it belongs to the entire discarded physical vacuum complement `W=(I-JJ^*)H_{phys}`, and its discarded transfer norm satisfies

[
\boxed{\rho=\| (I-JJ^*)P_f(I-JJ^*)|_W\|
=t_1^4>t_1^{12}=r_c^{1/3}.}
\tag{G6}
]

The equality `rho=t_1^4` follows because the full physical spectrum itself is bounded by `t_1^4`, and h attains the bound in W. This *specific* real SU2 gauge example simultaneously has `zeta=0` and an explicitly **too-slow discarded mode**. Hence a small conditional-variance/leakage estimate alone, even *zero leakage*, can never suffice for the YM4-06E Schur physical-gap preservation target.

The required one-step multiplicative error in Law 70 is

[
1+x\ge\frac{r_f}{r_c^{1/3}}=t_1^{-8},
\qquad
\boxed{x\ge t_1^{-8}-1>(25/11)^8-1>710.}
\tag{G7}
]

The numeric lower bound is an **exact integer inequality** using `t_1<11/25`; it is not a floating-point estimate. This is a dramatic one-step failure of the proposed *small-error* criterion at beta_t=2. It says nothing about whether the anisotropic physical mass gap itself is nonzero: indeed its known fine physical gap is `-4 ln(t_1)/a>0`.

## 5. What this means for the isotropic 4D Wilson proof

It is invalid to conclude that `rho_k` is automatically small or dominated by the coarse first ratio just because the block is gauge-equivariant, the vacuum is preserved and the coarse time-jump is exact. In this countercontrol, **all those good properties hold**, yet the discarded gauge-invariant plaquette is the true slow excitation.

This is not an argument that the actual isotropic Wilson beta_s=beta_t theory has the same defect. Its spatial plaquette interaction is exactly what distinguishes it from the solvable electric-only model, and a proof of a uniform fast discarded spectrum must **quantify that effect**, rather than infer it from time-factorization.

The next accepted mathematical target is therefore **an isotropic four-dimensional SU2 Wilson conditional-fiber Dirichlet/Poincare estimate in physical units**, covering all discarded gauge-invariant modes, with a matched retained-spectrum bound and a positive all-scale error margin. YM4-06F's finite-rank full-spectrum Loewner enclosure is one non-circular way to attack that target on small finite spatial volumes; its dimension grows exponentially and does not itself furnish the continuum induction.

## 6. Exact checks and scientific holds

The independent checker `tests/test_ym4_06g_electric_su2_dark.py` verifies spatial graph girths and a four-link fine plaquette outside all coarse paths, exact beta=2 SU2 Bessel rational enclosure, the powers 4, 12 and 36, the strict `x>710` inequality, and a separate finite **Q8-only algebra control** of central-noise three-link pushforward under noncommutative multiplication. Q8 is an algebra falsifier, not the source of the SU2 spectral values.

**Status: a special solvable 4D continuous SU2 gauge countercontrol, not the physical isotropic SU2 gap.** Keep PR #67 draft; require hosted final-head CI and an independent paper-level audit of the spin-network and gauge-sector statements. No finite r9 launch, no upstream merge.
