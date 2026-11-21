# YM4-WG04 — exact rank-42 neutral SU(2) Wilson band of the original interacting physical transfer

**21 November 2026.** **Scope:** continuous SU(2), original four-dimensional Wilson plaquette action, three-dimensional periodic spatial torus of side L=2, all 24 spatial magnetic plaquettes, all 24 temporal convolution links and the original local Gauss projector. **Strong-coupling interval:** 0<β≤1/100. **Certificate:** exact 42-dimensional *center-neutral physical spectral window*, derived from all-spin Peter–Weyl theory, exhaustive spatial-link incidence, and full magnetic-interaction min–max. The local contractible Wilson source is an **exact electric-band basis vector**, while the *interacting physical source projection onto this band* and individual first center-neutral eigenvalue weight remain OPEN.

This theorem extends the full-gauge [WG02 spatial-center selection](NOTE-YM4-WG02-SU2-CENTER-FLUX-WILSON-PROJECTORS-20261121.md) and the [WG03 charged-first spectral ordering](NOTE-YM4-WG03-FIRST-SU2-CENTER-CHARGED-ENERGY-ORDER-20261121.md) and sets up an explicit finite-rank Feshbach projector target.

## 1. Original 24-link spatial graph and neutral four-fundamental cycles

The 2×2×2 periodic cubic spatial lattice has eight sites and 24 positive oriented SU(2) spatial links, with two **distinct** parallel positive links between each adjacent pair of vertices in each direction. Its 24 spatial elementary plaquette loops and spatial winding loops are genuine original SU(2) gauge-invariant observables.

For any fixed set E of four occupied link *spin-1/2 Peter–Weyl representations*, gauge invariance requires an SU(2) singlet at each vertex. In particular, its number of incident fundamental edges must be even. Exhaustively enumerating the 24-choose-4 = **10,626** supports yields

- **162** supports with even fundamental incidence at all eight vertices;
- **42** center-neutral supports and **120** charged supports;
- of the charged supports, **16** in each of the three singly charged sectors and **24** in each of the three doubly charged sectors;
- **24** charged supports with a four-valent vertex, and **zero** such center-neutral supports.

Each of the 42 neutral supports has *degree 0 or 2* at every vertex, so the singlet intertwiner space at each occupied vertex is **one-dimensional**. The exact 42 original gauge-invariant spin-network basis functions can be written as:

1. the **24** fundamental spatial plaquette characters χ₁(U_p), and
2. **18** products χ₁(L_i)χ₁(L_j) of fundamental spatial winding-loop characters on two *distinct parallel circles in the same direction* (for each of three axes, select two of the four parallel winding loops, giving 3×6=18).

Their link-support sets are distinct. Peter–Weyl orthogonality (equivalently, Haar integration on an exclusive link) makes them mutually orthogonal, and each function has Haar squared norm **one**. Therefore the 42 functions form an orthonormal basis of the **entire center-neutral four-fundamental representation sector**. There is no finite character cutoff in the subsequent complement bound.

The original local Wilson half-trace observable W=(1/2)χ₁(U_(0,1)(0,0,0)) is **exactly one-half of one of these normalized electric-band basis functions**:

    ||W||²_Haar=1/4,
    K_phys W=κ₁^4 W.

This is an **electric** statement for the original Gauss-projected Wilson temporal Haar convolution K_phys. It is not yet a spectral overlap statement for the full interacting transfer and its true vacuum.

## 2. Exhaustive low-support spin-network classification

For any nontrivial SU(2) gauge-invariant spin-network component, a vertex incident to exactly one nontrivial representation is impossible: a single nontrivial irreducible representation has no invariant vector.

The 24-link spatial graph has **no supported nonvacuum configuration of three occupied links** with every occupied vertex of degree at least two. The independent full 24-choose-3 = **2,024** triple enumeration verifies this combinatorial fact. Similarly, no one-link source is gauge invariant.

With two occupied links, both edges must be the parallel pair with the same endpoints and the *same irreducible spin* r/2. If r is odd, the pair carries nontrivial center charge and is outside the neutral sector; if r is even, then r≥2. The 12 two-fundamental-link winding pairs from WG03 are all charged.

With four occupied fundamental links, the neutral space is precisely the 42-dimensional basis above. Every other neutral nonvacuum spin network has either two parallel links of representation r≥2; four occupied links with at least one representation r≥2; or at least five nontrivial occupied links. Because the electric Wilson convolution diagonalizes in all Peter–Weyl spin labels, these exhaustive cases suffice to estimate its full infinite-dimensional complement without discarding the higher-spin sectors.

## 3. Exact Wilson character and full neutral electric-tail bounds

The original normalized SU(2) one-link Wilson electric convolution K has r-th Peter–Weyl eigenvalue

    κ_r(β) = I_(r+1)(β)/I₁(β).

For 0<β≤1/100, put y=β²/4≤1/40000. The factorial-positive Bessel series gives the simultaneous **all-spin** rational bounds

    β(1−y)/4 < κ₁ < β/[4(1−y)],
    κ_r ≤ β²/[24(1−y)]  for all r≥2.

The latter follows by comparing consecutive representation majorants; the r≥2 sequence decreases at β≤1/100. Set

    a=β(1−y)/4,   A=β/[4(1−y)],
    d=β²/[24(1−y)].

The exact rational inequalities d<a² and A⁵<d² are valid over the entire specified β interval, and d<A<1. In consequence:

- every one of the **42** neutral four-fundamental electric states has **exact** eigenvalue κ₁⁴, greater than a⁴;
- a neutral two-link higher-spin state has eigenvalue at most d²;
- a four-link state containing at least one higher spin has eigenvalue at most d A³ ≤ A⁵ < d²;
- every state with at least five occupied links has eigenvalue at most A⁵ < d².

Hence the electric center-neutral eigenvalues, in decreasing order with multiplicity, satisfy

    λ₁(K_neutral) = 1,
    λ₂(K_neutral)=...=λ₄₃(K_neutral)=κ₁⁴,
    λ₄₄(K_neutral) ≤ d² = β⁴/[576(1−y)²].

These are rigorous statements about the **complete** physical SU(2) electric convolution and its complete higher-spin tail.

## 4. Transfer of the rank-42 band through every magnetic plaquette

The **full original physical Wilson transfer** is

    T_phys = B^(1/2) P_G K_24 P_G B^(1/2).

The magnetic multiplier B is the product of all 24 original spatial Wilson plaquette factors. With the same normalized Wilson convention as WG03, it satisfies the exact pointwise inequality

    exp(−48β) ≤ B ≤1.

Since B and K_phys commute with all spatial-center charge projectors, each physical sector is invariant. The nonzero spectra of B^(1/2)K_phys B^(1/2) and K_phys^(1/2) B K_phys^(1/2) coincide including multiplicities. Therefore min–max and the positive-operator sandwich

    (1−48β) K_neutral
       ≤ K_neutral^(1/2) B K_neutral^(1/2)
       ≤ K_neutral

give a true **all-magnetic-interactions, gauge-projected, infinite-dimensional** physical spectral comparison.

For every 0<β≤1/100, one can verify the following *universal rational comparisons*:

    (1−48β) [β(1−y)/4]^4 > β⁴/500,
    β⁴/[576(1−y)²] < β⁴/550,
    1−48β ≥ 13/25 > 1/2.

Consequently, after ordering the **full physical center-neutral eigenvalues** decreasingly, including the simple physical vacuum,

    λ₁(T_neutral) > 1/2,                 vacuum,
    λ₂,...,λ₄₃(T_neutral) > β⁴/500,      exactly 42 excited levels,
    λ₄₄(T_neutral) < β⁴/550,             complete remaining neutral spectrum.

The band's vacuum cutoff is unambiguous because λ₂≤κ₁⁴<1/2. The **actual interacting physical spectral projector**

    Π_42(β) = 1_( β⁴/550 , 1/2 )(T_phys | neutral)

therefore has **exact rank 42**, for every 0<β≤1/100. This spectral projector is defined by functional calculus on the *complete original physical transfer*. Its basis coefficients and Wilson-source overlaps still require calculation.

The certified unnormalized physical transfer band-to-tail ratio is strictly greater than

    (β⁴/500) / (β⁴/550) = 11/10.

At the two original vacuum-moment couplings, the simple rational band bounds are:

| β | Each of 42 physical neutral band eigenvalues | All remaining neutral excited eigenvalues |
|---|---|---|
| 1/10000 | >1/(500×10000⁴) | <1/(550×10000⁴) |
| 1/100000 | >1/(500×100000⁴) | <1/(550×100000⁴) |

This provides an exact **finite-rank target and certified spectral separation** for the forthcoming Wilson Feshbach projector, rather than an arbitrary representation cutoff.

## 5. Feshbach/Wilson source next acceptance obligation

The original local Wilson source is an exact **electric** basis element (Section 1). It is now known that the **full magnetic physical transfer** possesses an isolated 42-dimensional neutral band (Section 4). Yet B mixes electric spin-network basis vectors and shifts the physical vacuum; these two facts alone do **not** establish that the centered true-vacuum Wilson source has nonzero projection onto Π_42.

The next source-sensitive certificate must compute or bound

    w_42(β) = ||Π_42(β) (W−<Ω,WΩ>)Ω||²

and, for a *single* first Wilson-visible level, isolate a further eigenspace inside Π_42 with a source-adapted Feshbach/Schur residual and a positive weight lower bound. This is the correct next place to use a finite 42×42 spin-network Gram and a certified complement, with explicit higher-spin error control. The original WG03 charged-first physical spectral weight is exactly zero in the accepted parameter range; the neutral-band Wilson weight is separate and remains OPEN.

## 6. Reproduction and status

[Frozen predictions](certificate-atlas/PREDICT-YM4-WG04-NEUTRAL-42-BAND-20261121.hbp) precede the source and independent test implementation. The verifier recomputes all 10,626 four-link subsets, classifies the 162 Gauss-even supports and 42 neutral supports, cross-checks their exact 24+18 Wilson-loop basis, checks every three-link negative support, validates character bounds against independent rational Bessel intervals, challenges wrong geometry and β, and tests the magnetic spectral separation using a separate exact positive diagonal fixture.

    python3 -B tests/test_ym4_su2_neutral_42_band.py -v
    python3 -B tests/ym4_su2_neutral_42_band.py

**Acceptance target:** original-SU2 neutral **electric** rank-42 classification, original **interacting physical** isolated rank-42 neutral band for β≤1/100; physical band Wilson-overlap lower = OPEN; individual neutral first excited source weight = OPEN; larger-volume/weak-coupling continuum gap = OPEN.
