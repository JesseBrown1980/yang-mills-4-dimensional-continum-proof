# YM4-WG06 — exact original SU(2) Wilson 42×42 Haar Gram and magnetic first-order connectivity

**21 November 2026.** New exact-rational original continuous SU(2) Wilson source calculation at periodic spatial L=2. This uses the accepted full-physical neutral 42-band [WG04](NOTE-YM4-WG04-NEUTRAL-42-WILSON-BAND-20261121.md) and positive true-vacuum Wilson spectral source [WG05](NOTE-YM4-WG05-POSITIVE-42BAND-WILSON-WEIGHT-20261121.md). **Status:** 42×42 *electric-band first magnetic derivative* and positive original fixed-L Wilson moment lower bounds, pending independent CI acceptance. A six-mode leading *perturbative* cluster is identified; its finite-β actual interacting Feshbach projection and individual first-neutral eigenweight are **OPEN**.

## Exact 42-state physical electric Gram

The original full continuous-SU2 Gauss-invariant spatial H=L²(SU(2)^24) supports 24 fundamental normalized trace χ₁(U_p) spin-network states from the 24 elementary spatial plaquettes, and 18 products χ₁(W_i)χ₁(W_j) of two parallel fundamental winding traces. The 42 basis functions have distinct original 24-link fundamental-representation supports. In each, each occupied vertex has degree two and a unique SU(2) invariant spin-half intertwiner. Original normalized product Haar measure therefore gives the **exact 42×42 Gram**

    G_ij = <phi_i,phi_j>_Haar = δ_ij.

The original local normalized spatial Wilson plaquette halftrace is W=phi_0/2, with exact Haar squared norm 1/4.

## Exact first magnetic derivative on the original 42-state electric band

Under the original full 24-spatial-plaquette Wilson normalization, the complete spatial magnetic multiplier has the form

    B(β)=exp[-24β] exp[β sum_p W_p],

where W_p=(1/2)ReTr U_p is the original continuous-SU(2) fundamental spatial plaquette halftrace. Restrict its **first magnetic derivative** to the 42-dimensional electric eigenspace:

    M_ij = <phi_i,(sum_p W_p)phi_j>_Haar.

The scalar derivative −24 times identity from exp(−24β) shifts all 42 slopes equally and therefore leaves the **relative** first-order eigenmode ordering unchanged. The source implementation constructs the exact integer matrix

    A = 8 M.

For each pair of distinct basis support sets E_i,E_j, every 3-trace integrand <phi_i W_p phi_j> has to contain an even number of fundamental factors on every spatial SU(2) link, because multiplication by the SU(2) center element −I on a single link leaves Haar measure invariant. Its only possible nonzero first-order coupling occurs when

    E_i XOR E_j = support(p)

for one of the 24 original elementary spatial plaquette support sets. This is a necessary support condition, and the exact SU(2) Haar integration gives **positive 1/8** for every one of the 48 permitted undirected pairs.

### Exact SU(2) Haar evaluation by finite quaternion cubature

On a single original continuous-SU(2) link, write U as a unit real quaternion q=(q0,q1,q2,q3) on S³. Normalized Haar has E[q_a]=0 and E[q_aq_b]=δ_ab/4. Uniform averaging over the eight quaternion group elements Q8={±1,±i,±j,±k} has **the identical first and second coordinate moments**. Every permitted triple trace product above is polynomial of quaternion-coordinate degree exactly two on each of its six occupied spatial links. Hence the eight-point cubature reproduces the **true continuous-SU2 normalized Haar integral exactly** for these integrands. Each occupied link occurs twice, so changing its quaternion sign leaves the integrand invariant; using only the four positive coordinate quaternion axes, with weight 1/4 each, gives the same exact result with 4^6=4096 integer-quaternion assignments. This is a mathematically exact low-degree SU(2) Haar quadrature, with no finite-group substitution of the Wilson lattice link fields.

All **48** permitted off-diagonal coefficients evaluate to

    <phi_i,(sum_p W_p)phi_j>_Haar = 1/8,

all diagonal first magnetic entries vanish by center parity on an individual edge, and every unpermitted off-diagonal entry vanishes. Thus A is precisely the original 42×42 integer 0–1 adjacency matrix of the allowed plaquette-flip support graph.

## Six exact K4,2 blocks, six isolates and magnetic slope spectrum

The exact full-original-SU2 basis adjacency graph has **48** undirected edges and components

    6 × K_(4,2)  plus  6 × isolated vertices.

Each K4,2 connects four elementary plaquette basis states to two double-winding-loop basis states. All 24 plaquette basis states have degree two. Twelve double-winding states have degree four; the other six have degree zero.

The integer matrix A satisfies

    trace(A²)=96,
    A³=8A.

For each connected K4,2 component the two nonzero eigenvalues of A are +√8 and −√8, with four zero eigenvalues. Consequently on all 42 basis states, the exact first magnetic derivative matrix M=A/8 has:

| Relative first magnetic-order eigenvalue | Multiplicity |
|---|---:|
| +√8/8 = +√2/4 | 6 |
| 0 | 30 |
| −√8/8 = −√2/4 | 6 |

For the original local W=phi_0/2, the squared Haar projection onto the first-order **six-dimensional positive-slope eigenspace** equals

    (1/4) × [(A²)_00 / 16] = (1/4) × (2/16) = 1/32.

Here the positive and negative slope spaces have equal diagonal projector weight by bipartiteness, and their union has projector A²/8. The **sixfold degeneracy is real at this derivative order**. It requires a second-order magnetic and complement/Feshbach correction to identify an actual finite-β first neutral eigenvalue, its possible further degeneracy and its source overlap. The computed 1/32 is an **electric-band perturbative slope-subspace projection**, not a certified spectral weight of the full interacting top-six physical projector at nonzero β.

## Strictly positive quantitative original physical Wilson C2 and C4 moments

WG05 establishes for every 0<β≤1/10000 that the **true interacting physical vacuum-centered** local Wilson source u has squared spectral weight >1/5 in the **actual interacting** isolated neutral rank42 physical band. WG04 proves each of these actual transfer eigenvalues >β⁴/500. Since the original normalized physical Wilson transfer T obeys 0<T≤I, its positive vacuum eigenvalue λ0≤1, and hence every **vacuum-normalized** band eigenratio t=λ/λ0 satisfies t>β⁴/500.

The original connected Wilson vacuum moments are C_n=<u,(T/λ0)^n u>. Their positive spectral expansion therefore gives strict lower bounds, for n=2 and n=4,

    C₂ > (1/5)(β⁴/500)² = β⁸/1,250,000,
    C₄ > (1/5)(β⁴/500)⁴ = β¹⁶/312,500,000,000.

These are the first **effective positive exact rational lower bounds for the original fixed-L full interacting-vacuum Wilson C2/C4** in this certificate chain, complementing WG01's previously accepted upper bounds. They are tiny at small β but mathematically nonzero and source-authenticated.

The independent test checks the original β=1/10000 and β=1/100000 numerators and denominators against separately computed integer products, rejects a wrong β or odd moment order, and preserves the all-physical-operator normalization.

## Reproduction and next mathematics

[Prediction frozen before code](certificate-atlas/PREDICT-YM4-WG06-42GRAM-MAGNETIC-SLOPE-20261121.hbp). The producer and independent test rebuild the original 24-link spatial geometry; verify the complete 42×42 first-order support matrix, exact Haar second moments, 48 identical rational SU2 Haar coefficients and integer cubic minimal polynomial; and check the new original fixed-L physical vacuum Wilson moment lower bounds.

    python3 -B tests/test_ym4_su2_wilson_first_magnetic_42gram.py -v
    python3 -B tests/ym4_su2_wilson_first_magnetic_42gram.py

**Next mathematical acceptance:** use the now explicit six disconnected K4,2 leading first-order blocks as the *first perturbative six-mode Feshbach trial space* and certify an actual finite-β interacting rank-six spectral projector with a nonzero true-vacuum Wilson-source overlap. The following stage can then split that six-state cluster to isolate a single leading neutral physical eigenspace. The original full Yang–Mills weak-coupling/volume-uniform continuum gap remains OPEN.
