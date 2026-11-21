# YM4-WG03 — first physical SU(2) excited level is centre-charged at fixed L=2 and small beta

**21 November 2026.** Status: exact full-original-SU(2) fixed-spatial-lattice theorem, frozen before implementation; hosted verification required. Original three-dimensional periodic spatial torus L=2, continuous SU(2), original 4D Wilson plaquette action and full Gauss-projected transfer. **Coupling range:** every rational or real 0<beta<=1/100. **Conclusion:** the largest nonvacuum physical eigenvalue lies in a nontrivial spatial-centre electric charge sector. Consequently the true local *contractible* spatial Wilson plaquette's **first physical excited eigenspace spectral weight equals zero** throughout that interval. The neutral-sector first Wilson-visible excitation, its individual positive weight, and all continuum mass-gap objectives retain their own gates.

This result uses [WG02](NOTE-YM4-WG02-SU2-CENTER-FLUX-WILSON-PROJECTORS-20261121.md)'s original centre projectors and selection theorem, [YM4-02c](LEMMA-0004-REFLECTION-TRANSFER.md)'s positive physical SU(2) transfer, [WT01](NOTE-YM4-SU2-WILSON-LOCAL-TRANSFER-20261121.md)'s normalized exact Wilson Haar characters, and [WV01](NOTE-YM4-WV01-WILSON-PHYSICAL-VACUUM-TRACE-20261121.md)'s complete original magnetic/temporal normalization.

## 1. Exact spectral comparison of the original physical transfer

On the original 2³ spatial lattice, H=L²(SU(2)^24, normalized Haar). The exact physical Wilson transfer, after the physically harmless common normalization of each timelike plaquette, is

    T_phys = B^(1/2) P_G K_24 P_G B^(1/2).

Here P_G projects onto the original local SU(2) gauge-invariant Hilbert space, K_24 is the tensor product of 24 original one-link Wilson Haar convolution operators, and B is the product over all 24 original spatial magnetic Wilson plaquette weights.

B is positive, gauge invariant and centre invariant, with

    exp(-48 beta) <= B <= 1.

On the physical Hilbert space, P_G commutes with K_24 and B. The nonzero eigenvalues of B^(1/2) K_phys B^(1/2) equal those of K_phys^(1/2) B K_phys^(1/2), where K_phys=P_G K_24 P_G restricted to physical states (as the two positive products AA* and A*A for A=B^(1/2)K_phys^(1/2)). The latter is bounded in positive-operator order:

    exp(-48 beta) K_phys
       <= K_phys^(1/2) B K_phys^(1/2)
       <= K_phys.

By the compact positive min–max principle, within **each centre-charge sector** the corresponding ordered positive eigenvalues obey

    exp(-48 beta)*lambda_j(K_phys)
       <= lambda_j(T_phys) <= lambda_j(K_phys).

This comparison includes all spatial magnetic interactions and Gauss constraints. It is an operator theorem on the original infinite-dimensional continuous-SU(2) physical Hilbert space; no discrete surrogate or finite character cutoff is inserted.

## 2. The exact Peter–Weyl eigenvalue upper bounds, uniform over all representations

For one SU(2) link, spin r/2 representation r=0,1,2,... has normalized Wilson convolution eigenvalue

    kappa_r = I_(r+1)(beta)/I_1(beta)
            = (beta/2)^r J_(r+1)(beta)/J_1(beta),

with the positive power series

    J_m(beta) = sum_(k>=0) (beta²/4)^k / [k! (k+m)!].

At 0<beta<=1/100, put y=beta²/4<=1/40000. The exact factorial estimates

    1/m! <= J_m(beta) <= exp(y)/m! <= 1/[m!(1-y)]

give **strict rational inequalities**

    beta/5 < kappa_1 < beta/3,
    0 < kappa_r < beta²/20  for every r>=2.

For r>=2 the majorant (beta/2)^r/(r+1)! decreases with r because each successive ratio is (beta/2)/(r+2)<=beta/8<1. Thus the r=2 majorant controls all larger spins, without a representation cutoff.

On the original spatial 2³ graph, K_24 is diagonal in the product Peter–Weyl matrix-coefficient representation labels r_l. The physical gauge projection retains only configurations admitting an intertwiner/singlet at every spatial site. A nonvacuum state supported on **one nontrivial link** cannot satisfy independent SU(2) Gauss invariance at its two distinct endpoints.

## 3. Exact classification of two-fundamental-link physical states

There are 24 original positive spatial links, and therefore exactly

    binomial(24,2) = 276

pairs of distinct links. For exactly two occupied spin-1/2 links, a Gauss singlet requires each endpoint to be incident to an even number of fundamentals. The original graph has precisely **12** such pairs, four spatial winding two-link cycles per direction. Each pair forms a gauge-invariant fundamental Wilson line winding around one of the three L=2 periodic spatial circles, with centre charge (-++), (+-+) or (++-). **Every one is centre charged; the neutral sector contains zero two-fundamental-link states.** The independent checker rebuilds the lattice graph from coordinates and re-enumerates the same 276 pairs and 12 winding cases without using the producer's geometry enumerator.

This covers the entire spin-network source classification needed for the following bound: any *nonvacuum centre-neutral* Peter–Weyl eigenstate has either at least three nontrivial representation-labeled links or exactly two with at least one representation r>=2. Its electric-transfer eigenvalue is therefore at most

    max[(beta/3)^3, (beta/3)*(beta²/20)]
       = beta³/27.

Consequently **the second centre-neutral physical eigenvalue of K_phys** lies strictly below beta³/27. The first centre-neutral eigenvector is its trivial constant vacuum.

## 4. Charged winding trial versus the whole neutral complement

An original two-link fundamental winding Wilson function is a genuine physical K_phys eigenfunction with eigenvalue kappa_1². It lives in a nontrivial centre-charge sector and is orthogonal to the constant vacuum. By the preceding full-transfer min–max comparison, the largest physical eigenvalue in one such charged sector is at least

    exp(-48 beta) kappa_1².

On 0<beta<=1/100, the rational elementary inequality exp(-48 beta)>=1-48 beta>=13/25 combines with kappa_1>beta/5 to give the **strict charged lower bound**

    lambda_charged > 13 beta²/625.

Meanwhile every centre-neutral nonvacuum physical eigenvalue is strictly below beta³/27, since B<=1. Their ratio is bounded strictly by

    lambda_charged/lambda_neutral_second
       > [13 beta²/625]/[beta³/27]
       = 351/(625 beta)
       >= 56.16 > 56.

Thus the charged sectors contain a physical eigenvalue strictly **higher** than every nonvacuum neutral-sector eigenvalue. The original positive full Wilson transfer has one simple centre-neutral vacuum (YM4-02c), so its next-highest eigenvalue — the **first physical nonvacuum eigenvalue** — belongs entirely to the charged sectors. Degeneracies between charged sectors are allowed and do not affect the selection rule.

WG02 proved that the normalized local *contractible* spatial Wilson plaquette has exactly zero physical source overlap with every charged sector. Hence throughout 0<beta<=1/100,

    ||P_first_nonvacuum (W - <W>) Omega||² = 0,

where P_first_nonvacuum is the complete spectral projector of the first nonvacuum eigenvalue, including all degeneracies.

This is a **zero-weight theorem for the original first physical state at the specified small couplings and fixed spatial size**. The same source still couples to higher neutral excited states by WG01's strict C2/C4 positivity. The first *Wilson-visible* excitation is therefore a separate, higher-level spectral objective.

## 5. Frozen acceptance and independent verification

The [prediction HBP](certificate-atlas/PREDICT-YM4-WG03-FIRST-EXCITED-CENTER-ORDER-20261121.hbp) was frozen at commit 3c4f01ea3360cdf39e1f830295e2f07aa0221430 before implementation and tests.

The exact integer checker verifies the graph's 276/12 pair classification, original WG02 full SU(2) centre-transfer source, uniform character majorants, exact SU(2) Bessel-ratio intervals independently at beta=1/10000 and beta=1/100000, the complete magnetic min–max comparison, and numeric rational strict gaps. The external independent test additionally reconstructs the 24-link graph and charge characters, checks sample values up to beta=1/100, uses a separate finite positive spectral min–max fixture, and rejects bad coupling, link and charge assumptions.

    python3 -B tests/test_ym4_su2_first_centre_energy_order.py -v
    python3 -B tests/ym4_su2_first_centre_energy_order.py

The hosted workflow will preserve a canonical HBP record and SHA-256 source receipt.

**Next physical objective:** isolate the first **centre-neutral Wilson-visible eigenstate** by a source-adapted spin-network Gram and Feshbach complement certificate; determine its actual first positive overlap, and then work toward larger spatial volumes and weak-coupling continuum scaling. All eleven continuum certificate obligations, including the uniform mass gap, remain OPEN.
