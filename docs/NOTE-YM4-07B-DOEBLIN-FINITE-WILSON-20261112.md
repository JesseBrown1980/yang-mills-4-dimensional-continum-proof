# YM4-07B — an actual interacting SU(2) Wilson β=2 finite-volume gap, and its precise continuum failure

**November 12, 2026.** This is a basic positive-kernel/Doeblin **finite-volume theorem**, not a new strong- or weak-coupling Yang–Mills theorem and **not a continuum mass-gap solution**. It uses the actual spatial Wilson multiplier and the actual continuous-SU(2) temporal Wilson kernel, with **no selected-observable gap substitution**. The bound is disastrously volume dependent; its own continuum scaling limit certifies **no positive physical mass**. It is useful because it closes the trivial β=2 finite-volume positivity question in our formalism while isolating exactly what stronger transfer estimate the real problem requires.

**Prediction-first:** 12 rows frozen before code in `docs/PREDICTION-YM4-07B-DOEBLIN-FINITE-WILSON-20261112.hbp` at `884d8fd9729c3fc806a734ceb974f75b4fce6939`. Five independent mutated-input controls plus rational operator-kernel checks are hosted separately. No 4D continuum theorem or numerical eigenvalue computation is claimed.

## 1. Setup with the *actual* nonzero isotropic spatial Wilson action

On a finite periodic spatial cubic SU(2) lattice of side L≥2, let M=3L³ be the number of oriented spatial links and N_s=3L³ the number of spatial plaquettes. Take **both** temporal and spatial Wilson couplings β>0. Let `dH` be normalized product Haar measure on all spatial links and let

    A(U)=prod_(p spatial) exp[-β(1 - (1/2)Tr(U_p))],
    k_β(g)= exp[-β(1-(1/2)Tr(g))] / b0,
    b0=∫ exp[-β(1-(1/2)Tr(g))] dH(g),
    K(U,V)=prod_(spatial links ℓ) k_β(U_ℓ V_ℓ^(-1)).

`Bf(U)=∫K(U,V)f(V)dH(V)` is the normalized genuine **continuous-SU2** temporal Wilson product convolution. It commutes with local spatial gauge transformations and preserves the full gauge-invariant physical Hilbert space (the gauge-average form is equivalent on invariant inputs). The positive temporal Peter–Weyl eigenvalues ensure B≥0 as an operator. The physical interacting transfer is

    T=A^(1/2) B A^(1/2).

Its integral kernel is strictly positive and continuous on the compact product SU2 configuration space. Its top Perron eigenvalue λ0>0 is simple with a normalized continuous strictly positive eigenvector Ω; Ω is gauge invariant, and all nontrivial physical eigenvectors are in its orthogonal complement. By positivity improving/compact positive-kernel theory this holds for every **finite** L and β>0, but it gives no uniform-in-L gap by itself.

## 2. Exact Doob transform eliminates the spatial factor from the transition ratio

Set F(U)=A(U)^(1/2)Ω(U)>0. The ground-state equation says

    λ0 Ω(U)=A(U)^(1/2) B F(U).

The Doob-normalized reversible Markov transfer `P` acting on the true physical vacuum measure `μ=Ω² dH` therefore has the exact identity

    (P f)(U) = (B(F f))(U)/(B F)(U)
             = ∫ K(U,V) F(V) f(V) dH(V) / ∫ K(U,W) F(W) dH(W).

Let `kmin` and `kmax` be the exact extrema of the single-link kβ. Since SU2 trace/2∈[-1,1],

    kmin/kmax = exp(-2β).

Thus the **complete M-link temporal kernel** satisfies for every U,V,

    Kmin/Kmax = exp(-2β M) =: ε(L,β)>0.

Crucially, the spatially interacting A multiplier is entirely inside the positive U-independent weight F(V). Let the probability measure `ν(dV)=F(V)dH(V)/∫F`. Then, **pointwise on the entire physical configuration space**,

    P(U,dV) >= ε(L,β) ν(dV).

This is an actual Doeblin minorization of the **interacting** ground-state-transformed SU(2) Wilson transfer. It does not assume A constant, β small, or a finite group model.

For a bounded function f, write `P=εν+(1-ε)Q`, with Q Markov. Hence the oscillation seminorm contracts:

    osc(Pf) <= (1-ε) osc(f).

Every nonzero-eigenvalue eigenfunction of P is bounded and continuous (because T has a continuous bounded kernel and Ω is positive continuous on a compact space). Applying the oscillation inequality to any nonconstant eigenvector `Pf=λ f` proves `|λ|<=1-ε`. The physical transfer is self-adjoint and positive, so its eigenratios are in `[0,1-ε]`. Consequently, **including every gauge-invariant dark/charged/center-neutral state**,

    λ1(T)/λ0(T) <= 1 - exp(-2βM),
    γ_lattice = -log[λ1(T)/λ0(T)] >= -log(1-ε) > ε.

No spectral weight of a selected Wilson loop is assumed. The analytic argument uses only standard compact positive-kernel and Doeblin mathematics. It does not compute λ1(T), and the bound is extremely weak.

## 3. Isotropic β=2, L=2: a mathematically nonvacuous but useless scaling bound

Here `M=24`, so `ε=e^-96` and the complete interacting physical transfer satisfies

    r_physical <= 1-e^-96 < 1-(32/87)^96 < 1,
    γ_lattice > (32/87)^96 > 0.

The strict exact-rational inequality uses the independently checked elementary bound `e<87/32` from the positive factorial expansion. Thus this is a **real full-sector finite isotropic β=2 gap certificate**, avoiding the vacuous ratio greater than 1 from the older global comparison, but the gap floor is astronomically small. It neither identifies the first neutral eigenstate nor produces a practical first excited spectral estimate.

**No novelty claim:** strictly positive finite-volume transfer integral kernels and Markov minorization are standard elementary techniques. The value lies in an independently replayable application to this actual SU(2) Wilson transfer and in honestly quantifying its failure to scale.

## 4. Explicit failure at β(a)→∞ and a→0 with spatial volume growth

For a deliberately simple **proxy sequence** (not a certified nonperturbative Wilson RG flow), put `a_k=3^-k`, `β_k=2+k`, `L_k=2*3^(2k)`, so `L_k a_k=2*3^k→∞`. The count of temporal spatial links is `M_k=24*3^(6k)`. The Doeblin certificate yields only

    ε_k = exp[-2β_k M_k] = exp[-48(2+k)3^(6k)],
    m_k^cert = ε_k/a_k = 3^k exp[-48(2+k)3^(6k)] -> 0.

For each k, the exponent increment exceeds 6, so the ratio `m_(k+1)^cert / m_k^cert =3 exp[-(exponent_(k+1)-exponent_k)]<1/2`, proving decay to zero without floats. This **does NOT imply that the true interacting mass gap goes to zero**: a vanishing lower *bound* is simply uninformative. It shows that positive-kernel global minorization cannot furnish the missing continuum constant, even if the finite β=2 theorem is correct for every L.

At weak coupling, the needed method must control **local time-slice dynamics** and discard the extensive kernel-range factor `exp(-2β M)` while excluding hidden low-energy center-neutral modes. This is exactly the nonextensive `ρ_k`, `ζ_k` and physical-time Schur/OS task in 07A and draft PR #66. All these analytic estimates are currently OPEN at weak coupling.

## 5. Evidence, limitations and independent review

The checker `tests/test_ym4_07b_doeblin_finite_wilson.py` recomputes exact L=2,3,5 link counts, the e<87/32 rational proof, the β=2 exponent 96, the monotone collapse of the *certified* scaling floor, and a separate nonconstant positive two-state Doob transform example with ε=1/3. This **two-state example is only an algebraic control**; it is not a substitute for continuous SU2 physics. Five corrupted computations must fail. The analytic kernel/oscillation argument, not a finite matrix measurement, supplies the true SU2 finite-volume result.

**Unsolved:** a physically useful interacting center-neutral β=2 first-eigenvalue enclosure, a volume-uniform (or continuum-scale controlled) weak-coupling full physical transfer comparison along actual Wilson β(a), nontrivial renormalized 4D Schwinger-function limits and OS reconstruction, and a finite strictly positive continuum mass gap. This file does not validate any of those claims. Keep #70 DRAFT; do not merge PRs #65–69, and leave finite Round 5 and r=9 launch HOLD untouched.