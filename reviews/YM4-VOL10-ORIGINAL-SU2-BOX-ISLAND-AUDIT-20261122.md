# YM4-VOL10 fresh mathematical audit: original Wilson defect packing, root animals and correlated countermodel

**Date 2026-11-22 · Analytical reconstruction, independent of the integer checker implementation.** This is a second mathematical derivation by the assistant, not an external human peer review. Reviewed source: [VOL10](../docs/certificate-atlas/NOTE-YM4-VOL10-BAD-ISLAND-CRITERION-20261122.md), building on [VOL09](../docs/certificate-atlas/NOTE-YM4-VOL09-PERIODIC-GOOD-STAR-FREQUENCY-20261122.md).

## 1. Independent finite-box Gibbs probability derivation

Let \(B_e\) denote the indicator that the original continuous SU2 link-star exterior fails the fifteen gauge-invariant double-staple Wilson inequalities. The exact VOL09 periodic Gibbs bound is \(\mathbb E B_e\le p_{\beta,\epsilon}\), uniformly in original periodic \(L^4\). A \(b^4\) collection of vertex sites has precisely \(4b^4\) *positively oriented original link bases*, even when an endpoint exits the collection. Define \(N_Q=\sum_{e\in Q}B_e\). By linearity of expectation,
\[
\mathbb E_{\beta,L}N_Q
=\sum_{e\in Q}\mathbb E_{\beta,L}B_e
\le4b^4p_{\beta,\epsilon}.
\]
Since \(N_Q\ge r\) implies \(N_Q/r\ge1\), directly averaging the **pointwise inequality**
\(\mathbf1_{\{N_Q\ge r\}}\le N_Q/r\)
gives \(\Pr(N_Q\ge r)\le4b^4p/r\). This derivation does not need independent Bernoulli labels, positive association, or an assumed Gibbs coupling. The connected-\(r\)-subset occupancy event is contained in \(\{N_Q\ge r\}\).

For \(\beta=9^k,\epsilon=1/2,b=3^j,r=1\), the upper envelope is \(64(35+18k)3^{4j}/9^k\). At \(k=12,j=3\) it is \(16064/531441\); at \(k=12,j=4\) the raw number is \(16064/6561>1\), so the correct probability ceiling is **1**; at \(k=16,j=5\) it is \(20672/531441\). These are exact rational computations.

## 2. Independent geometric defect budget

Fix a fully specified SU2 Wilson configuration and any original positive link \(e\), with quaternion \(u\) and six preferred three-edge staples \(s_i\). The full original Wilson plaquettes incident to \(e\) are \(W_i=u\cdot s_i\). For any pair,
\[
1-s_i\cdot s_j=\tfrac12\lVert s_i-s_j\rVert^2
\le\lVert s_i-u\rVert^2+\lVert u-s_j\rVert^2
=2[(1-W_i)+(1-W_j)].
\]
If every incident plaquette obeys \(W_i\ge1-\epsilon/4\), all fifteen pairwise loops obey \(s_i\cdot s_j\ge1-\epsilon\). Contrapositively, if \(B_e=1\), at least one of the original six incident plaquettes satisfies \(W_p<1-\epsilon/4\). Let \(D_p\) indicate such a plaquette defect. Then \(\boxed{B_e\le\sum_{p\ni e}D_p}\) **pointwise**, regardless of the gauge orbit or boundary condition. Since every original plaquette has four distinct positive link bases, reversing the sum yields
\[
\sum_e B_e\le\sum_p\underbrace{4}_{\text{incident links}} D_p
=4\sum_pD_p.
\]
A bad island of \(m\) original links forces at least \(\lceil m/4\rceil\) distinct high-action-defect plaquettes. This is a genuine original SU2 geometric constraint and a candidate starting point for a model-specific multidefect contour estimate. The integer checker separately confirms the 4-to-6 incidences at all original links on L3 and L4.

## 3. Rooted animal encoding and independent-set extraction

The graph \(\mathcal H_L\) has original positive links as vertices, with edge adjacency when sharing a Wilson plaquette. Every link lies in exactly six plaquettes with three other links on each, and for \(L\ge3\) these 18 neighbors are distinct; this is a **regular degree-18 graph**. In any graph of degree at most \(\Delta\), a connected rooted set \(A\) of size \(m\) has a deterministic lexicographically first rooted spanning tree and a deterministic ordered depth-first traversal of its edges, yielding a closed walk of length \(2(m-1)\). The visited vertices are exactly \(A\), so distinct \(A\) cannot produce the same walk. Therefore \(A_m\le\Delta^{2(m-1)}\). Greedy removal of each selected vertex and its at most \(\Delta\) neighbors yields at least \(\lceil m/(\Delta+1)\rceil\) independent vertices.

Set \(\Delta=18\). If an additional original SU2 **joint** inequality holds for every independent set \(S\), \(\Pr(\bigcap_{e\in S}B_e)\le\rho^{|S|}\), then the union of rooted connected \(m\)-animals has probability at most \(18^{2(m-1)}\rho^{\lceil m/19\rceil}\). The minimal rooted-cluster implication is exact: a cluster with at least \(m\) vertices contains a connected subset of exactly \(m\) containing its root. With \(\rho\le18^{-57}\), integer exponent inequalities give \(2(m-1)-57\lceil m/19\rceil\le-m-2\), and hence \(\Pr(|C(o)|\ge m)\le18^{-m-2}\).

This is a **conditional probability implication**, with a clearly unresolved premise. The exponential exponent is mathematically valid but deliberately conservative. It does not establish any actual original SU2 joint-decoupling estimate.

## 4. Anti-overclaim test and the model-specific open step

For independent sample-free labels \(B_e=Z\) everywhere, with a single shared Bernoulli random variable \(Z\) of parameter \(p\), the one-site probability equals \(p\) and the full connected island has size \(|\mathcal H_L|\) with probability \(p\). Therefore \(\Pr(B_eB_{e'})=p\), not \(p^2\). This abstract mathematical countermodel proves a logical **non-implication** from single-site marginals to a joint independent-set event; it is not a model of continuous SU2 Wilson physics.

Source-strength boundary:
- SU2 periodic finite-box count and the four-to-one Wilson defect budget: **analytic exact consequences of VOL09**, independently reconstructed here.
- Graph degree, connected-animal walk encoding, independent packing and exponential implication: **exact combinatorics**.
- Any SU2 uniform independent-set joint-badness bound, physical-size cube conditional Dobrushin–Shlosman estimate, nontrivial 4D continuum OS reconstruction and original eleven continuum gates: **OPEN**.

The constructive next calculation should focus on **two or more separated defective original Wilson plaquettes** with their full boundary-conditioned joint Gibbs law, or the corresponding gauge-invariant weighted block activities. The existing [one-cube research version 7](https://hexagonmath.org/2610.00341v7) explicitly identifies bad-block islands and the physical-size cube estimate as major components, but its uniform continuum-tuning cube input remains open. This audit does not import its conditional results as a completed proof.
