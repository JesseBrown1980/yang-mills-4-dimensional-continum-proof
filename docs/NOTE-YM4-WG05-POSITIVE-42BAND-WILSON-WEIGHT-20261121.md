# YM4-WG05 — positive physical Wilson spectral weight in the original interacting 42-state neutral SU(2) band

**21 November 2026.** Exact-rational internal acceptance target, pending hosted independent checks. Continuous SU(2), original full 3+1D Wilson plaquette action, periodic spatial L=2, all 24 spatial magnetic plaquettes and all 24 temporal Wilson convolution links, full physical Gauss projection. **Theorem:** for every 0<β≤1/10000, the true interacting physical-vacuum centered local fundamental Wilson plaquette has squared spectral weight **greater than 1/5** in the isolated rank-42 center-neutral spectral band of [WG04](NOTE-YM4-WG04-NEUTRAL-42-WILSON-BAND-20261121.md). At least one genuine physical transfer eigenvector in that band consequently has squared Wilson overlap **greater than 1/210**. The first individual neutral eigenlevel weight and continuum gap remain OPEN.

## 1. Exact rank-one decomposition of the actual physical transfer

The same normalized original positive physical Wilson transfer from WG04 is

    T = B^(1/2) K B^(1/2),
    K = P_G K_24 P_G restricted to the original physical Hilbert space.

All original SU(2) Gauss constraints and magnetic/temporal plaquettes are included. Let |1> be the normalized constant function, P0=|1><1|, and K=P0+K_exc. A nontrivial gauge-invariant spin network on the original 24-link spatial graph must occupy at least two links. The original Wilson electric Peter–Weyl coefficients of every nontrivial representation are at most κ₁; therefore, on the **complete** physical Hilbert space,

    0<=K_exc,   ||K_exc||<=κ₁²<=h²,
    h=β/[4(1−y)],  y=β²/4.

With f=B^(1/2)1, c=||f||², b=1−48β, the original full magnetic multiplier satisfies b<=B<=1 and b<=c<=1. Consequently

    T=|f><f|+E,
    E=B^(1/2) K_exc B^(1/2)>=0,    ||E||<=h².

Let Ω be the unique strictly positive normalized physical Wilson transfer vacuum, λ₀ its eigenvalue, fhat=f/||f|| and Q_f=I−|fhat><fhat|. Rayleigh gives λ₀>=c>=b. Projecting TΩ=λ₀Ω with Q_f yields

    ||Q_f Ω||<=h²/b=:e.

Because Ω and fhat are positive unit vectors, their inner product has positive sign, and

    ||Ω−fhat||₂<=2e.

This controls the **true interacting vacuum** by a rank-one approximation, without assuming it equals the product-Haar constant.

## 2. Source-adapted rigorous L² and Rayleigh inequalities

The original local spatial fundamental Wilson source W=(1/2)ReTr U_p obeys Haar <W>=0, ||W||₂²=1/4, ||W||∞<=1. Let d=(1−b)/b=48β/b.

Pointwise B in [b,1] and c in [b,1] imply

    ||fhat−1||₂<=d,
    ||B^(1/2)fhat−1||₂<=d,

and hence

    ||Ω−1||₂<=2e+d,
    ||B^(1/2)Ω−1||₂<=2e+d.

With the **correct true-vacuum centering**

    m=<Ω,WΩ>,  u=(W−m)Ω,  z=B^(1/2)u,

Haar <W>=0 and Cauchy–Schwarz imply

    |m|<=2||Ω−1||₂<=4e+2d,
    ||z−W||₂<=6e+3d=:D,
    C₀=||u||²<=1/4+4e+2d=:C₀^up.

By WG04, W lies exactly in the original 42-dimensional *electric* center-neutral K eigenspace E42, with eigenvalue κ₁⁴ and ||W||₂=1/2. Thus

    ||E42 z||₂>=1/2−D.

The positive electric spectral theorem then gives a **source-sensitive lower bound** for the *original interacting physical transfer*

    <u,T u>=<z,K z>
       >=κ₁⁴ ||E42 z||²
       >=k⁴(1/2−D)²=:A,

where k=β(1−y)/4 is a strict rational lower bound on κ₁.

## 3. Isolated actual interacting band and Wilson spectral-weight dual

Let Π42 be the *true physical interacting* rank-42 spectral projection of WG04. Since the centered source u is orthogonal to the true physical vacuum and belongs to the neutral center sector, its full spectral measure consists of the 42 band eigenvalues and the remaining neutral tail.

Put w42=||Π42 u||². WG04's full-original-magnetic min–max theorem bounds every band eigenvalue by κ₁⁴<=h⁴ and every other nonvacuum neutral eigenvalue by

    δ=[β²/(24(1−y))]².

Therefore

    <u,T u> <=h⁴*w42 + δ(C₀−w42).

Combining this with the independently derived Rayleigh lower bound proves the exact source-adapted positive spectral-window dual

    w42 >= [ A−δ*C₀^up ]/[ h⁴−δ ].         (WG05)

All numerators and denominators are certified positive throughout the accepted β interval. Every estimate refers to the same original full SU(2) Wilson transfer, its actual physical positive vacuum and complete 24-plaquette spatial magnetic interaction.

## 4. Uniform integer-rational acceptance

For 0<β<=βmax=1/10000 freeze

    Y=βmax²/4=1/400000000,
    b_min=1−48βmax=622/625,
    d_max=3/622,
    e_max=[βmax/(4(1−Y))]²/b_min,
    D_max=6e_max+3d_max,
    C₀^max=1/4+4e_max+2d_max.

Exact monotonicity gives d<=d_max, e<=e_max, D<=D_max and C₀^up<=C₀^max over the entire interval. After factoring β⁴ from the numerator and denominator of (WG05), define the explicit rationals

    N_min=(1−Y)^4(1/2−D_max)²/256
           −C₀^max/[576(1−Y)²],

    H_max=1/[256(1−Y)^4]−1/576.

The exact comparison, independently checked with a separate exact integer numerator/denominator kernel rather than the producer's R class, gives

    N_min>0, H_max>0, N_min/H_max>1/5.

Hence for **all** 0<β<=1/10000,

    ||Π42 (W−<W>)Ω||² = w42 >1/5.

For the two original WV01 physical-vacuum benchmark couplings, the direct rational calculation gives stronger bounds:

| Original Wilson β | Entire interacting neutral 42-band Wilson weight | At least one individual physical eigenstate weight |
|---|---|---|
| 1/10000 | >21/100 | >1/200 |
| 1/100000 | >24/100 | >1/175 |

Since Π42 has exact rank 42, any orthonormal physical transfer eigenbasis of its range has 42 nonnegative individual squared Wilson overlaps summing to w42. Therefore at least one actual individual physical SU(2) eigenvector in the band obeys

    |<ψ_j,(W−<W>)Ω>|² > (1/5)/42 =1/210.

This is a **positive individual Wilson-visible physical excitation existence certificate** at fixed spatial L, inside the exact original interacting gauge-projected SU(2) transfer. WG03 simultaneously establishes that the **first full physical excited level is center charged and has zero local Wilson weight** at these β values. WG05 therefore identifies a genuinely higher neutral Wilson-visible physical eigenmode, and leaves identification of the **first individual eigenvalue within this neutral band** as an independent acceptance gate.

## 5. Independent reproduction and next Feshbach problem

[Prediction freeze](certificate-atlas/PREDICT-YM4-WG05-WILSON-42BAND-POSITIVE-20261121.hbp) predates the producer and independent tests. The verifier independently reconstructs the uniform exact rational inequality with its own integer numerator/denominator operations, checks true-vacuum L² and source centering, compares the accepted parent WV01 actual vacuum C₀ interval, confirms WG03's charged-first zero source weight, challenges parameter substitutions, and uses a separate 44-dimensional exact diagonal spectral fixture.

    python3 -B tests/test_ym4_su2_wilson_42band_positive_weight.py -v
    python3 -B tests/ym4_su2_wilson_42band_positive_weight.py

**Next proof:** compute the actual 42×42 gauge-invariant SU(2) neutral Wilson-network Gram/transfer and a source-sensitive Schur–Feshbach complement bound to isolate the *leading neutral interacting eigenprojection* or a smaller subcluster. The current whole-band weight certifies nonzero Wilson physics at fixed spatial lattice but does not assign it to that leading neutral eigenstate.

Larger-volume/weak-coupling uniformity, 4D continuum field reconstruction and a positive continuum Yang–Mills mass gap remain OPEN.
