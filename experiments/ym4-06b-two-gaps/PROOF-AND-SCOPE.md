# YM4-06B — two **finite** S₃ spectral-gap bounds on the spatial 2×2×2 torus

**Date:** 2026-11-11. **Scope:** exact mathematics for one fixed finite 3D lattice, not a 4D continuum result. The first hosted computation is at r=27 and r=81 only. The blind 3×4 r=9 one-shot is not used and must not be executed by this experiment.

## Frozen prediction and model

The prediction file [PREDICT-YM4-06B-20261111.hbp](PREDICT-YM4-06B-20261111.hbp) was committed alone at \`3f397b14adeeef21960e8b00bdff58590e772292\`, before the Rust source or CI. It commits to both inequalities and their controls. All measurement files are separate.

On the periodic 2×2×2 cubic spatial lattice, there are 8 vertices, 24 directed positive links and 24 faces. Each link takes a value in S₃. The gauge-invariant Hilbert space consists of complex square-summable functions on link configurations invariant under vertex gauge transformations. Define

\[
 H(r)/J_E=\mathcal E+r\mathcal M,\qquad
 \mathcal E=\sum_{\ell}\Bigl(3I-\sum_{\tau\in\operatorname{Trans}(S_3)}L_{\ell,\tau}\Bigr),\qquad
 \mathcal M(U)=\sum_{p}(2-\chi_{\mathrm{std}}(U_p)).
\]

Here each single-link transposition operator is understood in the gauge-covariant sum over all three transpositions. Each local \(\mathcal E_\ell\) has spectrum \(\{0,3,6\}\), so \(0\le\mathcal E\le144I\). Each face contributes 0, 2 or 3, hence \(0\le\mathcal M\le72I\). The exact local polynomial \(\mathcal E_\ell(\mathcal E_\ell-3I)(\mathcal E_\ell-6I)=0\) is checked with a 6×6 integer matrix.

YM4-06A established 48 flat commuting triples and **21 gauge orbits** on the 3-torus, and \(\min\{\mathcal M(U):\mathcal M(U)>0\}=6\) for sides all 2. This calculation independently checks the 48/21 group count and all 1,512 one-link transitions of flat orbits; the independent YM4-06A proof of global \(\kappa=6\) is an input.

Write \(e_1(r)\le e_2(r)\le \cdots\) for eigenvalues of \(H(r)/J_E\), counted with multiplicity in the full gauge-invariant Hilbert space. **The two observables are different**:

- First-excitation gap: \(\delta_1=e_2-e_1\).
- Separation above the flat cluster: \(\delta_{\mathrm{flat}}=e_{22}-e_{21}\).

## Bound 1: flat-cluster gap

Let \(P\) project onto the 21 normalized gauge-invariant flat-configuration orbit vectors; \(Q=I-P\). Every single-link transposition from a flat configuration produces four nonflat transposition faces, with cost 8. In particular \(P\mathcal EP=72P\) and \(P\mathcal MP=0\). Thus \(PHP=72P\) and min-max gives \(e_{21}\le72\).

Since \(\mathcal E\ge0\), the operator inequality \(H/J_E\ge r\mathcal M\) holds. The first 21 eigenvalues of \(\mathcal M\) are zero, and its 22nd is 6 by YM4-06A. Min-max then gives \(e_{22}\ge6r\).

**Exact certified inequality from the model and the independent YM4-06A magnetic minimum:**

\[
 \boxed{(E_{22}-E_{21})/J_E\ \ge\ 6r-72.}
\]

For r=27 this is at least **90**. For r=81 it is at least **414**. These are lower bounds, **not measured spectral values** and not the first gap.

## Bound 2: strictly positive first gap (explicit, intentionally very weak)

Fix a rooted spanning tree containing 7 links, gauge-fix it to identity while keeping the root gauge free. The rooted gauge-fixed configuration space has \(N=6^{17}=16,926,659,444,736\) points. The residual global-conjugation-invariant subspace is the physical Hilbert space. Burnside gives 2,821,153,019,713 physical gauge orbits.

The rooted electric operator is a real symmetric nonnegative weighted graph Laplacian. The independent 17 non-tree links can be multiplied by any of the three transpositions without changing the tree-gauge condition. Every S₃ element is a product of at most two transpositions, so **every pair of rooted configurations is connected by a path of at most \(D=34\) unit-weight moves**. The operators on the tree links provide further nonnegative off-diagonal connections; they are not required for this path bound.

Set \(C=144+72r\) and \(A=CI-H/J_E\). Since \(0\le H/J_E\le CI\), \(A\) is positive semidefinite. It is also entrywise nonnegative in the rooted configuration basis: off-diagonal entries come from the positive transposition kernel, while each diagonal entry is at least \(C-(72+72r)=72\). Consequently, self-loop padding extends every path to exactly 34 steps, and
\[
 (A^{34})_{xy}\ge1\qquad \text{for all rooted }x,y.
\]
For \(B=A/C\), put \(q=C^{-34}\). Then \(B^{34}_{xy}\ge q\). Its top Perron eigenpair \((\mu_1,\phi)\), with \(\phi>0\), obeys \(\mu_1\le1\) and, from the 72-energy flat trial state, \(\mu_1\ge(C-72)/C\). From the positive matrix-power inequality, \(\min\phi/\max\phi\ge q\).

The Doob ground-state transform \(K=\mu_1^{-1}\operatorname{diag}(\phi)^{-1}B\operatorname{diag}(\phi)\) is stochastic. Every entry of \(K^{34}\) is at least \(q^2\). Thus its nontrivial eigenvalues have 34th powers of modulus at most \(1-Nq^2\) (uniform Doeblin minorization). All eigenvalues of \(B\) are nonnegative because \(B\ge0\) as an operator. The elementary inequality \(1-(1-x)^{1/34}\ge x/34\) now gives
\[
 \mu_1-\mu_2\ \ge\ \frac{\mu_1 N}{34C^{68}}
 \quad\Rightarrow\quad
 \boxed{(E_2-E_1)/J_E\ \ge\
 \frac{(C-72)\,6^{17}}{34\,C^{68}}>0.}
\]

The unique Perron eigenvector is invariant under residual global conjugation, since the electric graph is connected and its operator commutes with this action. Hence the lowest physical eigenvalue equals the lowest rooted eigenvalue, and the second physical eigenvalue cannot be lower than the rooted second eigenvalue. The same explicit bound holds for the **physical first gap**.

This bound is extremely small; its only intended role is to prove strict positivity at this fixed finite size and coupling by a checkable argument. It does **not** estimate the actual first gap accurately, establish uniformity in lattice size or spacing, or prove anything about a continuum mass gap.

At the two frozen couplings:

| r | \(C\) | Lower bound for \(\delta_1\) (in \(J_E\)) | Lower bound for \(\delta_{\mathrm{flat}}\) (in \(J_E\)) |
|---|---:|---|---:|
| 27 | 2088 | \((2088-72)\,6^{17}/(34\cdot2088^{68})\) | 90 |
| 81 | 5976 | \((5976-72)\,6^{17}/(34\cdot5976^{68})\) | 414 |

## Hosted computational gate

The Rust 1.81 runner checks the S₃ group law and 2-trit codec, all six elements generated by at most two transpositions, the 6×6 exact electric polynomial, 48 commuting triples, 21 conjugacy classes, all **1,512** one-link and **52,164** two-link transitions from the 21 representative flat configurations, and the factorized integer bounds for r=27 and r=81. It saves deterministic HBP/HBI/SHA/SH/HASH receipts and independently replays the stored bytes. Three planted mathematical faults and a forbidden-r=9 control must abort; a changed HBP receipt must fail verification. The HBP/HBI schema here is experiment-specific and is not claimed byte-equivalent to the physical Host8 time-slice schema.

The full 3D Hamiltonian has **not** been assembled, and no measured eigenvalue or transfer-matrix mass is produced by this gate.

## Next spectral work

The useful numerical target is now a sharper first-gap interval, preferably with two independently checked Ritz witnesses and a no-store \(QHQ\) floor. Exact resolvent/Feshbach work can exploit the 21-dimensional flat block and the fact that a single link mutation has cost 8 while the global magnetic minimum is 6. For the physical mass \(m_{\mathrm{phys}}=-\log(\lambda_1/\lambda_0)/a\), a specific transfer operator, lattice-spacing definition, coupling path and error-certified approximation are required; no such value is claimed by YM4-06B.

The **3×4 r=9** production launch retains its separate release gate and remains untouched.
