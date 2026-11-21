# YM4-WG08 — exact original SU(2) symmetry-resolved individual physical Wilson eigenvector

**21 November 2026.** Original complete continuous-SU(2), 3+1D Wilson lattice transfer at periodic spatial L=2; full SU(2) Gauss projection, all 24 spatial magnetic plaquettes, all 24 original SU2 temporal convolution factors, all electric higher-spin representations. Builds from the accepted [WG06 first magnetic 42×42 Gram](NOTE-YM4-WG06-FIRST-MAGNETIC-42GRAM-20261121.md) and [WG07 interacting physical rank-six Feshbach projector](NOTE-YM4-WG07-SU2-SIX-FESHBACH-20261121.md).

**New exact fixed-L statement, pending hosted independent checks:** for every \(0<\beta\leq1/1000000\), the true interacting physical six-state center-neutral spectral cluster contains a **one-dimensional fully spatial-symmetric invariant subspace**, and hence a genuine **individual physical SU(2) Wilson transfer eigenvector**. Its **true interacting-vacuum centered local Wilson squared overlap is strictly greater than \(1/289\)**. The energy of this symmetry-selected eigenmode relative to the other five cluster eigenvalues, and whether it is the very first neutral excited level, remain OPEN.

## 1. Forty-eight original spatial Wilson symmetries

On the original spatial three-torus of side length two, take the eight translations \(x_i\mapsto x_i+s_i\pmod2\), and the six coordinate-axis permutations. Together these give the finite spatial symmetry group

\[
G=(\mathbb Z_2)^3\rtimes S_3,\qquad |G|=48.
\]

Every element acts unitarily on the **original continuous-SU(2) link-field Hilbert space** by relabeling the 24 spatial links (preserving their positive orientation under coordinate permutations). The full 24-plaquette Wilson magnetic action, the identical Wilson temporal Haar convolution on every link and the original local Gauss projection are invariant under these spatial relabelings. Hence every group element commutes with the true original physical transfer. Spatial-center neutrality is also preserved.

Let

\[
P_G=\frac1{48}\sum_{g\in G}U_g
\]

be the orthogonal projector onto fully translation- and axis-permutation-invariant physical wavefunctions. We use \(P_G\) here for the finite **spatial-symmetry** average; the original SU2 Gauss projector is a separate factor of the physical transfer.

## 2. Exact action on the previous 42-dimensional spin-network basis

WG06 supplied 24 fundamental spatial plaquette spin-network states and 18 products of two parallel winding traces, with distinct original 24-link supports. Every spatial group element maps each of those 42 normalized SU2 Haar functions to another one with a **positive unit coefficient**: if a plaquette's winding orientation reverses, the fundamental SU2 trace still obeys \(\operatorname{Tr}(U^{-1})=\operatorname{Tr}U\).

The independent integer-link support checker constructs all 48 permutations of the 42 original spin-network masks. Each permutation preserves WG06's exact magnetic derivative adjacency matrix \(A=8M\), which has six \(K_{4,2}\) blocks and six isolates. The six connected blocks form **one transitive orbit** under the full spatial group, with each original block appearing exactly eight times among the images of a fixed block.

Each \(K_{4,2}\) block has a single strictly positive normalized eigenvector at its largest magnetic derivative eigenvalue \(+\sqrt8\). The group maps these six positive-slope eigenvectors to one another, with positive sign, so the six-dimensional electric positive-slope projector \(P_+\) decomposes as a six-point permutation representation of \(G\). Its fully invariant subspace therefore has **exact rank one**:

\[
\operatorname{rank}(P_G P_+)=1.
\]

The normalized common sum of those six block Perron vectors is the uniquely identified electric fully spatial-symmetric first-slope state.

## 3. Exact electric local Wilson source projection: \(1/192\)

The original local fundamental Wilson halftrace is \(W=\phi_0/2\). Its orbit under the 48 spatial symmetries consists of **all 24 elementary spatial plaquette basis states**, each reached exactly twice, so

\[
P_G W=\frac1{48}\sum_{p=1}^{24}\phi_p.
\]

By WG06 the positive-slope projector is

\[
P_+=\frac{A^2+\sqrt8 A}{16},\qquad A^3=8A.
\]

The symmetric source \(P_GW\) has only plaquette components, while the original magnetic matrix \(A\) joins plaquettes to double-winding states. Hence \(\langle P_GW,A P_GW\rangle=0\). The independent integer matrix product yields

\[
\sum_{p,q=1}^{24}(A^2)_{pq}=192.
\]

Therefore the exact squared projection of the original local Wilson halftrace on the fully symmetric first-slope state is

\[
\boxed{\|P_G P_+ W\|^2
=\frac{192}{48^2\cdot16}
=\frac1{192}}.
\]

This original SU2 Haar relation uses exact integer matrix coefficients; it does not require an approximate eigenvector or finite group replacement of SU2 link variables.

## 4. Transfer to one actual interacting physical eigenvector

The accepted WG07 Feshbach theorem constructs an **actual** interacting center-neutral physical rank-six spectral projector \(\Pi_6(\beta)\) for every \(0<\beta\leq1/10000\). It commutes with each spatial symmetry because the true full physical transfer does. WG07 also established the operator-norm estimate

\[
\|\Pi_6(\beta)-P_+\|\leq23250\beta
\]

in the stated small-coupling range needed here.

Since \(P_G\) commutes with both orthogonal projectors, \(P_G P_+\) and \(P_G\Pi_6\) are orthogonal projections. Their difference in norm is at most \(23250\beta<1\) for \(0<\beta\leq1/1000000\). Orthogonal projections at distance strictly below one have the **same rank**, so

\[
\boxed{\operatorname{rank}(P_G\Pi_6)=1}.
\]

This is a statement about the **actual full interacting infinite-dimensional original continuous-SU2 physical transfer**. Because its rank-one range is invariant under that self-adjoint transfer, it consists of a genuine physical eigenvector \(\psi_{\mathrm{sym}}(\beta)\). Its eigenvalue is one of the six actual center-neutral levels 2–7.

Let \(\Omega\) be the true normalized positive interacting physical vacuum, and let \(u=(W-\langle\Omega,W\Omega\rangle)\Omega\) be the correctly centered local Wilson source. WG05–WG07 give

\[
\|u-W\|\leq148\beta,\qquad
\|W\|=\frac12,\qquad
\|\Pi_6-P_+\|\leq23250\beta.
\]

Combining the exact electric source norm with the invariant projector estimate,

\[
\begin{aligned}
\|P_G\Pi_6u\|
&\geq\|P_G P_+W\|
-\|\Pi_6-P_+\|\|W\|-\|u-W\|\\
&>\sqrt{\frac1{192}}-11773\beta\\
&>\frac1{14}-11773\beta
>\frac1{17}
\qquad (0<\beta\leq1/1000000).
\end{aligned}
\]

The final strict inequality is an independent exact rational endpoint check. Because the physical invariant cluster range has **rank one**, this is already a certified squared Wilson weight for an **identified individual physical eigenvector**:

\[
\boxed{|\langle\psi_{\mathrm{sym}},u\rangle|^2>\frac1{289}}.
\]

The eigenmode is identified by its finite spatial symmetry character (fully translation- and axis-permutation-invariant) and its membership in the isolated six-state interacting neutral cluster. Its energy can still coincide with that of other symmetry sectors; the rank-one statement is with the additional commuting spatial-symmetry projector.

## 5. Independent controls, status and next spectral order

The source prediction is frozen in [WG08 prediction HBP](certificate-atlas/PREDICT-YM4-WG08-SYMMETRIC-WILSON-EIGENMODE-20261121.hbp) before the producer and independent tests. The verifier reconstructs all 48 original spatial link relabelings independently, tests 42-network closure, checks original magnetic adjacency equivariance for all 48×42² matrix entries, verifies the exact 24-plaquette local-Wilson orbit and its multiplicities, the transitive six-component action, integer sum \(\sum(A^2)_{pq}=192\), and the true source rational lower bound. Wrong symmetry, missing orbit, wrong \(\beta\) and premature first-neutral-level promotion are treated as falsifiers.

    python3 -B tests/test_ym4_su2_wilson_symmetric_rankone.py -v
    python3 -B tests/ym4_su2_wilson_symmetric_rankone.py

**Next exact mathematical question:** use the 24-point fourth-Haar SU2 integration of WG07 and the symmetry-decomposed six-mode sector to compare the **energy of this fully symmetric rank-one eigenvector** with the other five first-neutral cluster levels. A certified ordering would determine whether it is the leading neutral excitation and would attach the already certified positive Wilson overlap to that first neutral eigenspace. Full larger-volume/weak-coupling continuum Yang–Mills mass gap remains OPEN.
