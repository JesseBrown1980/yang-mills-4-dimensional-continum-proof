# YM4-VOL03 — exact continuous-SU(2) six-face fourth-order cube term and hierarchical certificate pilot

**2026-11-22. Evidence status: LOCAL_HAAR_PASS; conditional tree-interface test PASS; full fourth-order Feshbach, volume-uniform spectral inequality and continuum gap OPEN.**

This continuation of [YM4-VOL02](NOTE-YM4-VOL02-THIRD-MAGNETIC-SELECTION-20261122.md) examines the first parity-allowed six-plaquette closed surface and adopts proof-engineering ideas, with attribution and strict scope separation, from Alpöge–Buckmaster's new [unforced Navier–Stokes research repository](https://github.com/tristanbuckmaster/navier-stokes/tree/ad53419de079eb8f95f60313473374624a348546). No Navier–Stokes fluid-specific theorem or missing numerical data is imported into SU(2) Yang–Mills.

## 1. Exact original continuous-SU(2) cube Haar integral

On the original periodic spatial lattice, for L>=3, take one elementary cube c with its six faces and twelve distinct oriented SU(2) links. With the fundamental SU(2) character χ(U)=tr(U) and each face holonomy U_f, the genuine product Haar expectation is

    I_cube = ∫ ∏_{f∈∂c} χ(U_f) dHaar(U_edges) = 1/16.

The independent integer-only calculation in [tests/ym4_su2_vol03_cube_haar_cell_tree.py](../../tests/ym4_su2_vol03_cube_haar_cell_tree.py) represents every SU(2) link as a unit quaternion q0 + q1 i + q2 j + q3 k. Since each edge occurs exactly twice, only exact Haar second moments E[q_a q_b]=δ_ab/4 enter. The six oriented face-trace tensors have integer coefficients. Repeated sparse exact tensor contractions produce numerator **1,048,576** over denominator **16,777,216**, hence **1/16**. The same result independently holds for the local cube embedding at spatial L=3 and L=4.

An analytic cross-check uses Schur orthogonality of the fundamental representation: link integration supplies a factor 2^(-E), and closed-surface index contractions a factor 2^V, with cube E=12 and V=8; this yields 2^(8−12)=1/16. This is an original continuous-Haar calculation, not a finite group substitution.

For any two **distinct** designated cube faces i,j, insert the other four faces as normalized Wilson halftraces W_f=χ(U_f)/2. Their 4! ordered permutations cancel the 1/4! exponential coefficient. The corresponding particular **cube-surface term** in the raw fourth-order band entry

    <φ_i, V^4 φ_j>/24,   φ_i=χ(U_i),  V=Σ_p χ(U_p)/2

is exactly **1/256 per cube containing that pair**. This is one connected cube contribution only. Other order-four support patterns, vacuum normalization/counterterms, intermediately excited electric states, and the full higher-spin Schur/Feshbach correction must be included before obtaining the actual physical effective matrix. No sign or gap claim is inferred from this one positive term.

## 1A. An exact L-independent norm for the cube-only fourth-order submatrix

Every elementary plaquette of a periodic spatial cubic lattice L>=3 is a face of exactly **two** elementary cubes. In either cube it meets five other faces. The two cubes share only the original face, and each unordered pair of distinct cube faces lies in exactly one cube. Thus the symmetric nonnegative cube-face adjacency \(A_{\rm cube,L}\) is **10-regular** on the \(3L^3\) plaquette states. The additional exact integer enumerator independently verifies these claims at L=3,4,5, including unique cube ownership of each face-pair.

Define the **isolated raw cube-surface contribution**, explicitly excluding all other fourth-order connected diagrams and all physical Schur corrections,

\[
B_{\rm cube,L}(i,j)=
\begin{cases}
\#\{\text{cubes containing both faces }i,j\}/256,&i\ne j,\\
0,&i=j.
\end{cases}
\]

Since this nonnegative symmetric matrix has uniform row sum 10/256, the constant vector is a positive eigenvector with eigenvalue 10/256. The row-sum bound gives the reverse operator-norm inequality. Therefore

\[
\boxed{\|B_{\rm cube,L}\|_{\ell^2\to\ell^2}=\frac{10}{256}=\frac5{128}
\quad\text{for every integer }L\ge3.}
\]

This is an **exact volume-independent local contribution norm**, providing an input to a future hierarchical cell proof. It is **not** a norm bound on the full vacuum-subtracted fourth-order effective operator, whose additional contributions may change both its entries and spectrum. The full all-volume mass gap and even the first nonscalar physical effective coefficient remain OPEN.

## 2. Conditional hierarchical two-block certificate, inspired by a pinned Lean proof interface

Let a real symmetric/Hermitian operator A be partitioned into two local blocks, A_U and A_V, with cross-block B. If independently checked lower bounds satisfy A_U≥g_U I, A_V≥g_V I and an independently checked upper bound satisfies ||B||≤ε, then

    A ≥ (min(g_U,g_V)−ε) I.

Proof: for any x=(u,v),
    <x,Ax>≥g_U||u||²+g_V||v||²−2ε||u||||v||
        ≥(min(g_U,g_V)−ε)(||u||²+||v||²).

The inequality can be composed along a binary tree of cell clusters; each parent receipt must authenticate its two children, their direct-sum decomposition, and a bound on all cross-child interactions. A uniform-in-volume spectral lower bound will require that the **sum of cross-norm debits along each root-to-leaf path remains bounded independently of the tree size**. A raw tree with growing debits does not establish such a bound.

The original VOL03 test checks a synthetic integer fixture: eight leaf lower bounds 12, four cross bounds 1, two cross bounds 2, and one root cross bound 4 yield global lower bound 5, while deliberately invalid inputs yield a negative bound. **These fixture numbers are not SU(2) operator bounds.** This exercise checks the assembly formula, rather than proving physical volume-uniform positivity.

## 3. External Navier–Stokes proof artifacts: exact compatibility map

Upstream pin: `ad53419de079eb8f95f60313473374624a348546` (2026-11-20).

| Original pinned artifact | What the source provides | Valid use in YM4 | Acceptance |
|---|---|---|---|
| [Upstream README](https://github.com/tristanbuckmaster/navier-stokes/blob/ad53419de079eb8f95f60313473374624a348546/README.md) | Formalization scope, release status | Provenance and missing-input gate | SOURCE_LINKED |
| [Lean README](https://github.com/tristanbuckmaster/navier-stokes/blob/ad53419de079eb8f95f60313473374624a348546/lean/README.md) | Challenge/solution structure; Appendix B fifteen condition families | Design a declarative SU2 certificate interface | METHODOLOGY |
| [CellLayerChallenge.lean](https://github.com/tristanbuckmaster/navier-stokes/blob/ad53419de079eb8f95f60313473374624a348546/lean/CellLayerChallenge.lean) | Fluid-specific cell and positivity statement objects | Pattern for local-cell input contracts | METHODOLOGY |
| [CellCalculusStatements.lean](https://github.com/tristanbuckmaster/navier-stokes/blob/ad53419de079eb8f95f60313473374624a348546/lean/Breakdown/CertCell/CellCalculusStatements.lean) | Fluid-specific local cell-form conditions | Organize auditable local quadratic forms | METHODOLOGY |
| [Cell-layer comparator](https://github.com/tristanbuckmaster/navier-stokes/blob/ad53419de079eb8f95f60313473374624a348546/lean/comparator-cell-layer.json) | Lists three statement names and the permitted axioms propext, Quot.sound, Classical.choice | Independent theorem-statement and permitted-axiom audit concept | SOURCE_LINKED |
| [Certificate assembly](https://github.com/tristanbuckmaster/navier-stokes/blob/ad53419de079eb8f95f60313473374624a348546/lean/Breakdown/Cert/Assembly.lean) | Conditional proof assembly from prerequisite claims | Predeclare all SU2 physical operator dependencies | METHODOLOGY |

The publicly posted repository **does not contain the numerical Navier–Stokes certificate data**, and its 128-bit Arb/FLINT interval verification is **not part of the Lean formalization or repository**. The upstream README also states that the November 20 patched Lean package was not rebuilt at publication. Those are explicit acceptance holds for upstream full numerical validation. Even a successful fluid proof would not provide a direct YM4 volume-uniform spectral theorem. The linked Lean code is preserved as attributed external methodology, not copied or claimed to be formally imported.

## 4. Original SU2 next gates

**VOL03-A (now):** genuine continuous-SU2 exact Haar cube contribution and integer replay: PASS at local test, hosted gate pending.

**VOL03-B:** reconstruct the complete fourth-order *connected, vacuum-subtracted physical* effective kernel on the neutral plaquette band, including all parity-compatible diagrams, electric-state mixing, centre-sector selection and higher-spin tail with exact rational error bounds: OPEN.

**VOL03-C:** produce authenticated cell operators and all cross-cell norm bounds, including infinite-spin tail and physical projection, and prove the tree debit is **volume-independent**: OPEN.

**VOL03-D:** identify the relevant nonvacuum Wilson-coupled eigenmode and first connected spectral weight at every spatial L, with an actual quantitative uniform spectral gap in the appropriate transfer/energy normalization: OPEN.

**VOL03-E:** connect this strong-coupling regime to the lattice-spacing/weak-coupling scaling and the 4D continuum OS reconstruction: OPEN.

The atlas's original eleven continuum obligations remain OPEN. The machine HBP is [YM4-VOL03-CUBE-HAAR-TREE-20261122.hbp](YM4-VOL03-CUBE-HAAR-TREE-20261122.hbp), replay SHA-256 `5457698b6e59a0aec208d3b5d17d8aeaf4b048fd01f920348206d0602040e168`. This pilot can be independently recomputed with Python 3 and integer arithmetic; its source and receipt belong to the 4D atlas, alongside original upstream evidence pointers.
