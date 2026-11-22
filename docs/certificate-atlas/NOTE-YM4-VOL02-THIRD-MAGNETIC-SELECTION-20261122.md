# YM4-VOL02 — exact five-plaquette parity obstruction at larger spatial L

**22 November 2026. Research scope:** original continuous SU(2) 3+1D Wilson model, spatial periodic \((\mathbb Z/L\mathbb Z)^3\), every integer \(L\ge3\), positive but sufficiently small finite \(\beta\). This exact support/Haar lemma advances [VOL01](NOTE-YM4-VOL01-VOLUME-SLOPE-OBSTRUCTION-20261122.md). The connected fourth-order physical transfer calculation and volume-uniform spectral estimates remain OPEN.

**Frozen preimplementation prediction:** [PREDICT-YM4-VOL02](PREDICT-YM4-VOL02-THIRD-MAGNETIC-SELECTION-20261122.hbp).

## Lemma: every nonempty mod-two closed plaquette 2-chain contains at least six faces

Let \(C\) be a set of distinct elementary spatial plaquettes with mod-two edge boundary \(\partial C=0\). The periodic cubic complex is a three-torus. If the \(H_2(T^3;\mathbb Z_2)\) class of \(C\) is nonzero, one of its three coordinate fluxes is nonzero. Intersect \(C\) with each of the \(L^2\) parallel coordinate winding cycles transverse to the corresponding face direction. The mod-two intersection is the same nonzero value for each such winding cycle, because any two parallel fibers are homologous. Therefore \(C\) needs at least one distinct face at each fiber: \(|C|\ge L^2\ge9\).

If the homology class is zero, \(C=\partial A\) for a mod-two 3-chain \(A\), i.e. a proper nonempty set of spatial elementary cubes (the empty/full subsets have zero boundary). Count boundary faces by their normal directions: \(b_1,b_2,b_3\). Each nonzero \(b_d\) is at least two, since a nonconstant periodic row of cube occupancies has at least two state changes. If all \(b_d>0\), \(|C|=\sum b_d\ge6\). If \(b_d=0\) for some direction, \(A\) is constant on every fiber parallel to that direction; since \(A\) is proper and nonempty, another direction has at least one nonconstant row, with its boundary crossings repeated along all \(L\) fibers. Thus some other \(b_e\ge2L\ge6\). Consequently every nonempty closed \(C\) has at least six faces.

In particular there are **no nonempty closed two-, three-, four- or five-plaquette mod-two surfaces** for any spatial \(L\ge3\). Repeated factors in a product cancel pairwise modulo two, leaving a chain with at most the original number of plaquettes and the same parity.

## Exact physical SU(2) consequences

Let \(E_L\) be the neutral four-fundamental, gauge-invariant electric plaquette span. It has one orthonormal trace spin network \(\phi_p=\chi_{1/2}(U_p)\) per elementary spatial plaquette, giving \(\dim E_L=3L^3\). At L=4, single four-edge axial winding loops carry center charge and lie in other sectors. At L=3, axial three-edge windings are likewise center charged. The L=2 exceptional double-winding sector of WG06 is absent.

Let \(V=\sum_pW_p\), \(W_p=\phi_p/2\), and \(P_{\rm vac}=|1\rangle\langle1|\). Linkwise SU(2) Haar invariance under \(U_e\mapsto-U_e\) kills every product whose total fundamental-link support has nonzero mod-two boundary. The five-face lemma therefore proves these exact matrix identities:

\[
E_LVE_L=0,\qquad E_LV^3E_L=0,\qquad E_LV^2P_{\rm vac}=0 .
\]

VOL01 established that for \(i\ne j\) the only ordered \((p,q)\) with \(m_p\oplus m_q=m_i\oplus m_j\) are \((p,q)=(i,j),(j,i)\), and the exact SU(2) Haar identity \(\chi_{1/2}^2=1+\chi_1\) makes their second-order contribution exactly cancel \(E_LVP_{\rm vac}VE_L\). Cubic translation and axis-permutation symmetry makes the diagonal entries equal. Thus

\[
E_L\left(\tfrac12V^2-VP_{\rm vac}V\right)E_L=d_L I_{3L^3}
\]

for a scalar \(d_L\) that requires no numerical evaluation to establish the identity.

For the true original full physical Wilson transfer \(J=K^{1/2}e^{\beta V}K^{1/2}\), \(t=\kappa_1(\beta)^4\), other neutral electric modes have total spin-representation index at least six and \(K_R/t=O(\beta^2)\) as \(\beta\to0\) **for each fixed finite L**. The vacuum Schur third-order term contains \(E_LV^2P_{\rm vac}\) and therefore vanishes. The all-spin tail Schur coupling is \(O(\beta^4)\) relative to \(t\). Hence the energy-dependent effective neutral plaquette-band operator has, at each fixed L,

\[
F_{E_L}(\beta,\nu)=
\left(1+d_L\beta^2\right) I_{3L^3}+O_L(\beta^4).
\]

The notation \(O_L\) is deliberate: **no volume-independent fourth-order constant or spectral-gap ordering** has been established. The first possible nonscalar plaquette-band correction is **fourth order**. In particular, the six-block third-order ordering certificate of L=2 cannot be transplanted as a larger-volume eigenvalue comparison.

## Independent finite tests and next proof

The integer-only independent code \`tests/ym4_su2_vol02_third_parity.py\` reconstructs all plaquette support masks at L=2,3,4,5 and independently counts ordered three-insertion parity possibilities for every diagonal and offdiagonal plaquette-pair matrix element. At L=3,4,5 all counts vanish exactly; L=2 is retained as a negative control for the four-face topological distinction. The source has no dependency on WG09's coefficient generator. Hosted duplicate replay and optimized replay are required.

**Next mathematical object:** the full vacuum-subtracted, higher-spin-corrected **fourth-order connected plaquette kernel**, with linked-cluster organization, exact Haar coefficients, real center sectors, and a uniform spatial-volume norm/correlator estimate. The eleven continuum construction obligations remain OPEN. These exact small-beta support identities form a fixed-lattice bridge, not a continuum mass-gap proof.

## Rebase-aware acceptance

This research branch is reviewed against the merged November 22 WG09/VOL01 92-node atlas baseline. The theorem inputs remain the original SU2 physical transfer and linkwise Haar parity; all continuum and uniform-volume spectral gates remain OPEN.
