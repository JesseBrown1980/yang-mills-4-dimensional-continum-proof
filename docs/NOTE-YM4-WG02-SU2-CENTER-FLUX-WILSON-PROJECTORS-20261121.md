# YM4-WG02 — exact spatial centre-flux projectors for the original continuous-SU(2) four-dimensional Wilson transfer

**21 November 2026.** Model: original four-dimensional continuous-SU(2) Wilson plaquette action with physical SU(2) Gauss projection on a 2×2×2 periodic spatial three-torus. The finite-periodic 2×2×2×10 source is the exact combinatorial verifier. The operator-level selection theorem holds for each fixed finite positive Wilson coupling on this same spatial torus. State: original SU(2) **eight centre-charge sector projectors and an exact Wilson-source selection rule**, pending hosted CI acceptance. The physical ordering of first nonvacuum eigenvalues between sectors is the next mathematical objective.

## 1. Three global spatial centre transformations of the actual 4D Wilson source

For each spatial direction i=0,1,2 define an operator Z_i on link configurations by multiplying each positive spatial SU(2) link in direction i with base point coordinate x_i=0 by the central element -I, on **all** time slices. Other links, including all timelike links, stay unchanged. Each Z_i is an involution, all three commute, and they preserve product normalized Haar measure.

On spatial size L=2, a time slice has 24 positive spatial links and exactly **four** selected links in any one direction. Over 10 time slices, the corresponding 4D transformation flips 40 of the total 320 links. A spatial plaquette containing i has two i-oriented link factors with the same x_i base coordinate, and therefore picks an even number of sign flips; so does each timelike plaquette containing i, because its two spatial links at adjacent times have the same base coordinate. Every original Wilson plaquette trace and the full interacting action are invariant.

The exact 480-plaquette checker counts, separately for each i:

    360 plaquettes with zero selected centre flips,
    120 plaquettes with two selected centre flips,
    zero plaquettes with an odd number of selected flips.

This is a direct group-theoretic SU(2) 1-form electric centre symmetry, with a canonical finite spatial three-torus realization, rather than a substitution by a discrete gauge group. We use a finite group only to **index its centre-symmetry operators**: the link variables themselves remain continuous SU(2).

## 2. Commutation with the full original physical Gauss-projected transfer

Use the exactly normalized original physical Wilson transfer from YM4-02c and WV01:

    T_phys = B^(1/2) P_G K_24 P_G B^(1/2).

Here B is the product of **all 24 spatial magnetic Wilson plaquette factors**, P_G averages over the eight original SU(2) lattice-site Gauss transformations, and K_24 is the product of 24 normalized SU(2) timelike Wilson convolution kernels.

Each Z_i commutes with each factor:

- B because all spatial plaquettes are centre-neutral.
- P_G because multiplication by a central element commutes with arbitrary SU(2) transformations at both link endpoints; hence it commutes with the local gauge action before Haar averaging.
- K_24 because its one-link kernel depends on U_l V_l^(-1), unchanged if both adjacent-time spatial configurations are multiplied by the same prescribed centre sign.

Thus Z_i T_phys = T_phys Z_i. The Z_i preserve the physical Gauss-invariant Hilbert space, are commuting unitary self-adjoint involutions, and supply three conserved binary quantum numbers. The fixed-volume positive transfer has a **simple strictly positive vacuum Omega**. Since centre transformations preserve the positive cone and commute with T_phys, uniqueness of the normalized positive eigenvector gives Z_i Omega = Omega.

## 3. Eight exact projectors and independent winding witnesses

Let s=(s0,s1,s2) in {0,1}^3, Z_s=Z0^s0 Z1^s1 Z2^s2, and let e=(e0,e1,e2) with each ei in {-1,+1}. Define the exact physical centre-charge projector

    P_e = (1/8) sum_s [ product_i ei^si ] Z_s.

The character orthogonality identity over (Z2)^3 proves

    P_e^2=P_e,          P_e^*=P_e,
    P_e P_f=0 if e!=f,
    sum_e P_e=I.

These identities hold on the whole original physical infinite-dimensional transfer Hilbert space. The producer independently enumerates all eight group elements, all eight characters and all 512 convolution coefficient identities in integer group algebra; the checker separately verifies the projector action on all eight charge characters.

All eight charge sectors are **nonzero**, witnessed by products of original SU(2) gauge-invariant fundamental Wilson lines winding around the spatial periodic directions. A one-direction winding loop contains two spatial links, exactly one of which crosses the corresponding selected centre cut. Therefore a line winding in direction i has charge -1 under Z_i and +1 under the other two, and their eight subsets realize all eight charge characters. Each such Wilson product is a nonzero function (for example, it equals one at the all-identity configuration).

The eight centre-charge sectors are a property of the original **continuous SU(2)** periodic lattice gauge symmetry. They are not identified with the eight topological/flat sectors of the separate finite S3 research model.

## 4. Exact original local Wilson first-state selection rule

The original normalized spatial plaquette half-trace W used in WC01, WV01 and WG01 is *contractible*. Every Z_i leaves it invariant. Because the true physical vacuum Omega is also Z_i-invariant, the centered original Wilson source

    u = (W - <Omega,W Omega>) Omega

belongs exactly to the **neutral** charge sector e=(+1,+1,+1). Hence

    P_e u=0 for every nontrivial e,

and its complete connected Wilson spectral weight in each centre-charged physical sector is identically zero:

    ||P_e u||² = 0,     e != (+++).

This holds at every original fixed-lattice beta>0 for which the original Wilson transfer theorem applies. In particular, **if the first physical excited eigenspace lies entirely in a charged sector, its Wilson overlap with this local contractible source is exactly zero**. If the first eigenspace has both charged and neutral parts, only its neutral part can contribute. The next acceptance gate is therefore **first neutral-sector eigenvalue isolation and comparison against the charged sectors**, rather than blindly targeting a full-spectrum eigenvector.

The centre projectors are exact symmetry-resolved spectral selectors, but **their sector ordering is not determined by the symmetry**. Establishing whether a centre-neutral or centre-charged mode comes first requires a physical operator energy comparison. A nonzero first-excited Wilson spectral weight requires an independent first-mode spectral projector plus positive source overlap in the appropriate sector.

## 5. Verification and scope

The prediction-first [YM4-WG02 frozen HBP](certificate-atlas/PREDICT-YM4-WG02-SU2-CENTER-SECTORS-20261121.hbp) precedes the producer and independent tests. The code verifies all 480 original SU(2) plaquette centre cuts, the time-slice spatial-link and full-circumference counts, all eight projector identities, three noncontractible fundamental Wilson winding charges, all eight winding-product charge witnesses and deliberately invalid plaquette or group inputs. The separate checker also constructs actual exact rational noncommuting SU(2) quaternion link fields, independently verifies complete action invariance under each Z_i, and verifies commutation between local SU(2) gauge transformations and centre transformations across all original 320 links.

    python3 -B tests/test_ym4_su2_center_flux_projectors.py -v
    python3 -B tests/ym4_su2_center_flux_projectors.py

**Next exact physical task:** build a centre-neutral Wilson-network basis, an explicitly complementary centre-charged spin-network energy test, and a source-sensitive Schur/Feshbach or exact variational/complement certificate. Combine that with WG01's positive spectral Gram bounds. All full weak-coupling continuum, volume-uniform energy and Clay mass-gap requirements remain OPEN.
