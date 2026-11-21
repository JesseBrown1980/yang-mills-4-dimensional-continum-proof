# YM4-07E — exact one-step SU(2) Wilson-source and physical spectral-projector transport

**20 November 2026.** Frozen targets: [prediction-first HBP](PREDICT-YM4-07E-EXACT-BLOCK-SOURCE-PROJECTOR-20261120.hbp), commit \`52215fa43f34772eb32dc9fdbaa30360ed176c1f\`. This note combines the already-defined, actual four-dimensional continuous-SU(2) factor-two block map of [YM4-03](NOTE-YM4-03-ONE-SCALE-BLOCKING.md) with the existing positive transfer representation of [YM4-02](LEMMA-0004-REFLECTION-TRANSFER.md). It gives **exact matched-source and cyclic physical-projector identities**, and a separate **quantitative lower bound on the loss of an unmatched source**. All statements concern the *exact induced coarse measure* at a single fixed finite lattice and coupling.

## 1. Genuine 4D SU(2) block: preserve the entire effective action

Let \(\Lambda_f=(\mathbb Z/(2L_i)\mathbb Z)^4\), with each \(L_i\ge3\), carry the genuine continuous \(\mathrm{SU}(2)\) Wilson Gibbs measure \(\mu_{\beta,f}\). Use any finite \(\beta\ge0\), including large bare weak-coupling values, and define for each coarse link
\[
(BU)_\mu(x')=U_\mu(2x')U_\mu(2x'+e_\mu).
\]
Its factors are **ordered**. Under a fine gauge transformation,
\(B(U^g)=(BU)^{g|_{\mathrm{coarse\ sites}}}\).
If \(C\) is a closed coarse path, then as a noncommutative ordered group product
\[
\mathrm{Hol}_C(BU)=\mathrm{Hol}_{2C}(U).
\]
For a coarse plaquette, \(2C\) is exactly the fine \(2\times2\) rectangle, never an individual fine elementary plaquette.

Define the **actual induced** coarse measure
\(\nu_{\beta,c}:=B_*\mu_{\beta,f}\). The conditional-Haar-fiber integral from YM4-03 is an explicit exact density \(\rho_\beta(V)\) for this measure. Its effective action is \(-\log\rho_\beta+\mathrm{constant}\). In \(d=4\), this generally contains a complete Wilson-network hierarchy: the one-link six-staple integral has **15 pair interactions, three coplanar and twelve mixed-plane** ([YM4-05A](NOTE-YM4-05A-CHARACTER-WEAK-COUPLING-20261107.md); [YM4-07D draft](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/75) on its branch). We retain the **full integral** rather than selecting a Wilson-only effective coupling \(\beta'\).

For every bounded gauge-invariant coarse observable \(F\), and every finite collection \(F_1,\dots,F_n\),
\[
\mathbb E_{\nu_{\beta,c}}\Big[\prod_i F_i(V)\Big]
=\mathbb E_{\mu_{\beta,f}}\Big[\prod_i F_i(BU)\Big].
\]
This equality is exact for any finite \(\beta\). It is the defining property of the pushforward, not an approximation or a cross-group comparison.

## 2. Matched Wilson-source amplitude defect: exactly zero

Define the Euclidean \(L^2\) pullback \(J_0F=F\circ B\). Since \(\nu=B_*\mu\),
\[
\|J_0F\|_{L^2(\mu)}=\|F\|_{L^2(\nu)},\qquad
\langle J_0F,J_0G\rangle_\mu=\langle F,G\rangle_\nu.
\]
Thus \(J_0\) is an **isometry**. For a coarse Wilson loop \(W_C\), take the matched fine observable \(W_{2C}=J_0W_C\), including its actual fine centering. Their normalized/centered source vectors coincide under \(J_0\); the exact Euclidean source comparison error is
\[
\boxed{\delta_{\mathrm{matched},L^2}=
\|W_{2C}-J_0W_C\|_{L^2(\mu)}=0.}
\]
The same holds for all gauge-invariant coarse Wilson networks. This is **at the same underlying cutoff**, with the exact induced coarse action.

## 3. Quantify the unmatched-source obstruction at every finite coupling

Take the ordinary fine plaquette \(p\) based at an even coordinate, in directions \(\mu\ne\nu\). Its four edges include two *off-line links*, which do not occur in \(B(U)\). Choose one such link \(\ell\). Let
\[
P_B f=\mathbb E_{\mu}[f\mid B(U)],\qquad
P_\ell f=\mathbb E_{\mu}[f\mid U_{\text{all links except }\ell}].
\]
These are **Euclidean conditional-expectation projectors**. Since \(\sigma(B)\subseteq\sigma(U_{\ne\ell})\), orthogonal projection onto nested subspaces gives
\[
\|(I-P_B)W_p\|_{L^2(\mu)}^2
\ge\|(I-P_\ell)W_p\|_{L^2(\mu)}^2
=\mathbb E_\mu[\mathrm{Var}(W_p\mid U_{\ne\ell})].
\]
The accepted continuous-SU(2) local conditional-density theorem [YM4-07C, merged PR #74](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/74) proves for all finite \(\beta\ge0\)
\[
\boxed{\quad\|(I-P_B)W_p\|_{L^2(\mu)}^2
\ \ge\ \frac14 e^{-12\beta}>0.\quad}
\]
This lower bound is *independent of volume* and is a **source-loss lower bound**, not the upper-bound \(\delta\) demanded by a continuum comparison. A stronger polynomial bound is available subject to acceptance of the analytic proof in the draft YM4-07D PR #75; the present theorem does not rely on that draft.

At \(\beta=0\), product Haar implies \(P_BW_p=0\) exactly because the selected off-line link is independent Haar. By exact SU(2) normalized-trace Haar moments, \(\mathbb E W_p=0\) and \(\mathbb E W_p^2=1/4\), hence
\[
\boxed{\quad\|(I-P_B)W_p\|_{L^2(\mu_{\beta=0})}^2=1/4.\quad}
\]
Thus **matched coarse loops have zero source defect; unmatched fine elementary plaquettes can have strictly positive defect**, even under the exact full-network induced action. The test uses exact 24-quaternion degree-two controls only as a check of the genuine Haar identity.

## 4. True physical-energy projector: exact on the induced cyclic sector

This paragraph uses the finite-\(\beta>0\) positive, self-adjoint gauge-invariant transfer framework and vacuum of [YM4-02/03](LEMMA-0004-REFLECTION-TRANSFER.md). Let \(T\ge0\) be the fine **physical** transfer operator on the gauge-invariant OS Hilbert space, with simple maximal eigenvalue \(\lambda_0>0\), normalized vacuum \(\Omega\), and fine physical time step \(a>0\). Write \(\widetilde T=T/\lambda_0\). Let \(Q\) be the **spatial** factor-two line map, and \(M(F\circ Q)\) multiplication by the pullback of a bounded coarse gauge-invariant slice observable \(F\).

Define the actual observable-generated cyclic subspace
\[
\mathcal K=\overline{\mathrm{span}}\big\{
M(F_n\circ Q)\widetilde T^2M(F_{n-1}\circ Q)\cdots
\widetilde T^2 M(F_1\circ Q)\Omega:\ n\ge0\big\}.
\]
It contains \(\Omega\), is invariant under \(\widetilde T^2\) and the matched coarse observable algebra. Since \(\widetilde T^2\) is self-adjoint, \(\mathcal K\) is *reducing* for \(\widetilde T^2\). Because \(\widetilde T\ge0\), it is the nonnegative spectral square root of \(\widetilde T^2\); hence \(\mathcal K\) also reduces \(\widetilde T\).

**Precise OS-algebra scope and temporal limit.** Take the **subalgebra generated by bounded gauge-invariant coarse spatial-slice functions \(F\)** inserted at integer coarse times, and its reflection-positive vacuum correlators. Those correlators are obtained from the exact induced coarse measure by the **infinite Euclidean-time/ground-state limit at fixed finite spatial lattice**, as in YM4-03, Theorem 7. They are exactly the fine-vacuum correlators of the pullbacks \(F\circ Q\) separated by two fine time steps.

The OS/GNS Hilbert space \(\mathcal H_c^{\rm slice}\) *reconstructed from this selected multi-time spatial-slice observable subalgebra* therefore has an isometric realization \(J:\mathcal H_c^{\rm slice}\to\mathcal H_f\) **onto \(\mathcal K\)**, with induced normalized transfer
\[
J\widetilde T_c=\widetilde T^2J.
\]
This \(T_c\) is the reconstructed **cyclic semigroup** on \(\mathcal H_c^{\rm slice}\), not an assertion that the coarse blocked action is Markovian in a single time slice. The exact induced measure may retain temporal memory and mixed-time Wilson-network observables. No generation theorem for the **entire** coarse OS Hilbert space from this chosen spatial-slice subalgebra is asserted. Any such additional states belong in a separately audited observable/sector-completeness gate.
Write \(H_f=-a^{-1}\log\widetilde T\) and \(H_c=-(2a)^{-1}\log\widetilde T_c\) on their positive-transfer supports; zero transfer eigenvalues correspond to infinite energy. By functional calculus, for every Borel *physical energy* interval \(I\subset [0,\infty)\),
\[
\boxed{\quad \mathbf1_I(H_f)J=J\mathbf1_I(H_c).\quad}
\]
This is an **exact physical spectral-projector intertwining theorem on the induced cyclic sector**; it is not the Euclidean conditional projector \(P_B\).

Let \(x_c=[M(W_C)-\langle\Omega_c,M(W_C)\Omega_c\rangle]\Omega_c\) be the **vacuum-centered** coarse Wilson time-zero source, and \(x_f=Jx_c\) its matched fine \(2C\) Wilson source. For \(P_c=\mathbf1_I(H_c)\), \(P_f=\mathbf1_I(H_f)\), the two same-group finite-step discrepancies are exactly
\[
\boxed{\quad \delta_{\mathrm{cyclic}}=\|x_f-Jx_c\|=0,\qquad
\epsilon_{\mathrm{cyclic}}=\|P_fJx_c-JP_cx_c\|=0.\quad}
\]
They hold at any finite \(\beta>0\) **for the exact induced action and the matched source**, without numerically diagonalizing the enormous fine SU(2) transfer operator. They are algebraic identities, not a fresh computed SU(2) first-excitation weight.

## 5. Dark-state obstruction and whole-spectrum gap

The induced cyclic spectrum can omit physical fine states. If \(\Delta_f\) denotes the first positive fine physical energy and \(\Delta_c\) the first positive induced cyclic energy, then \(\Delta_c\ge\Delta_f\). Equality requires the lowest fine excited eigenspace to intersect \(\mathcal K\) (with the corresponding spectral qualification for non-discrete spectra).

An adversarial positive rational transfer model illustrates the issue:
\[
\widetilde T_f=\mathrm{diag}(1,3/4,1/2),\quad
\mathcal K=\mathrm{span}(e_0,e_2),\quad
\widetilde T_c=\mathrm{diag}(1,1/4).
\]
Its projectors intertwine **exactly** for any common physical energy window. The dark fine level \(3/4\) nevertheless lies below the visible excited level \(1/2\): the fine first gap is \(\log(4/3)/a\), whereas the coarse cyclic first gap is \(\log 2/a\). Thus exact \(\delta=\epsilon=0\) is **insufficient by itself** to prove the full gap.

An all-scale mass-gap proof would additionally bound the spectrum of \(\mathcal K^\perp\) uniformly, or establish the required lowest-state visibility, while proving a nontrivial OS continuum limit along \(\beta(a)\to\infty\) and controlling physical/infinite-volume limits.

## 6. The whole-space projector error is a binary dark-sector gate

The reducing decomposition is actually stronger than a loose triangle inequality. Set \(P_{\mathcal K}=JJ^*\). For every physical-energy Borel window \(I\), exact functional calculus yields the **orthogonal projector decomposition**
\[
\boxed{\quad
\mathbf1_I(H_f)=J\mathbf1_I(H_c)J^*+
(I-P_{\mathcal K})\mathbf1_I(H_f)(I-P_{\mathcal K}).
\quad}
\]
Both summands are mutually orthogonal spectral projections. Define the *dark projector* \(D_I=(I-P_{\mathcal K})\mathbf1_I(H_f)(I-P_{\mathcal K})\). Therefore
\[
\boxed{\quad
\|\mathbf1_I(H_f)-J\mathbf1_I(H_c)J^*\|_{\mathrm{op}}
=\|D_I\|_{\mathrm{op}}\in\{0,1\}.
\quad}
\]
Here \(D_I=0\) precisely when the fine physical spectrum on \(\mathcal K^\perp\) has **no spectral weight in that energy window**. If any dark state contributes, this *whole-space* projector difference has norm exactly one. The successful cyclic projector identity of section 4 has zero defect because it restricts to \(\mathcal K\), not because all physical states were transferred.

In the section 5 rational model, take the physical-energy interval whose fine transfer ratios belong to \([2/3,4/5]\). Its fine spectral projector is the rank-one dark projector \(|e_1\rangle\langle e_1|\). The cyclic projector vanishes, and the difference has operator norm exactly **one**. The new integer test checks this interval without evaluating logarithms.

**A direct full-gap acceptance gate:** for a proposed physical \(\Delta_*>0\), it suffices to prove both (i) the cyclic sector has no excitation in \(I=(0,\Delta_*)\), and (ii) \(D_I=0\) (no dark excitation), uniformly along the ultraviolet/volume limits. Neither condition is claimed for the genuine weak-coupling SU(2) sequence. This binary decomposition identifies exactly what the next spectral producer must certify.

## 7. Scope and proof gate

- **Exact mathematical conclusions under the stated finite-lattice transfer hypotheses:** four-dimensional continuous-SU(2) factor-two pushforward; matched Wilson-source \(L^2\) isometry; exact cyclic physical-projector intertwining; strict unmatched fine-plaquette \(L^2\) loss by the merged YM4-07C bound.
- **Executables:** [prediction-first frozen HBP](PREDICT-YM4-07E-EXACT-BLOCK-SOURCE-PROJECTOR-20261120.hbp), [integer-only geometry/Haar/spectral checker](../tests/test_ym4_07e_exact_block_projector.py), nine active false-claim controls, and a dedicated hosted workflow.
- **Remaining OPEN:** generation of the full induced coarse OS algebra beyond the chosen spatial-slice cyclic subalgebra, quantitative full-space SU(2) physical spectral projector/lowest-state visibility, source maps between independently renormalized couplings, weak-coupling all-scale localized action bounds, nontrivial OS continuum reconstruction, uniform physical full-spectrum gap, and independent external proof review.

**Practical decision:** retain the source as a *blocked Wilson loop* under the exact induced action. Concentrate the next producer on dark-sector visibility and on bounding any subsequent approximation of the all-network induced action. The original finite \(S_3\) Wilson certificate remains a separate authenticated finite-model calibration anchor; no \(S_3\to SU(2)\) identification is made.
