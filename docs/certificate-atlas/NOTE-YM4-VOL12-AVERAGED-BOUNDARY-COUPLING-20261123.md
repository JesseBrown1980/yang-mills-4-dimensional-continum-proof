# YM4-VOL12 — averaged boundary-coupling interface from periodic bad-star crossing

23 November 2026. Rigorous conditional probability/coupling lemma in the original 4D continuous SU(2) finite-volume Gibbs model. Its geometric input is the [source-dependent periodic crossing theorem](NOTE-YM4-VOL12-PHYSICAL-BOX-CROSSING-20261123.md). The good-region coupling hypothesis is OPEN.

## 1. Original Gibbs disintegration and physically relevant observables

Fix an even periodic original Wilson torus L>=2b, beta_W>=531441, epsilon=1/16 and a b^4 based-link cube Q_b. Let T be the finite set of original links to be resampled in the cube with a sufficient collar to evaluate all six plaquette staples of the links based in Q_b; let Y=T^c be the remaining original links. Because the original continuous SU(2) finite-volume Gibbs measure is a strictly positive density relative to a finite Haar product, it disintegrates as

\[
\mu_{\beta,L}(dU_T,d\eta_Y)
=\lambda_{\beta,L}(d\eta)\,\mu^\eta_{\beta,L}(dU_T).
\tag{A1}
\]

Let A_b denote the event that the four-dimensional original bad-star link graph has a crossing of Q_b in at least one of four axes, interpreted as an event measurable in (U_T,eta). Conditional on the upstream chessboard theorem, the earlier exact probability bound gives

\[
p_b:=\mu_{\beta,L}(A_b)\le16b^3\,18^{-b-2}.
\tag{A2}
\]

This is **averaged over the actual Gibbs exterior marginal lambda**, not a supremum over adversarial eta.

Choose any bounded metric space (E,d) with 0<=d<=1 and any gauge-invariant physical observable F(U_T,eta) taking values in E (for a cylinder observable, its support and the collar are fixed). For each pair of boundary conditions (eta,eta'), suppose there is a coupling K_{eta,eta'} of the two original conditional Gibbs laws, measurable as a Markov kernel. Define its **good-region coupling cost** as

\[
g_b(\eta,\eta')=
\mathbb E_K\!\left[
d(F(U_T,\eta),F(V_T,\eta'))\,
\mathbf1_{A_b(U_T,\eta)^c\cap A_b(V_T,\eta')^c}
\right].
\tag{A3}
\]

It is enough to control the average of g_b, rather than the worst boundary pair. Let delta_good(b) be any valid bound on its lambda x lambda expectation.

## 2. Exact averaged coupling inequality

Split the coupling expectation of d into the event that neither replica has a bad-star crossing and its complement. Because d<=1,

\[
\mathbb E_K d(F(U_T,\eta),F(V_T,\eta'))
\le g_b(\eta,\eta')
+\mu^\eta(A_b)+\mu^{\eta'}(A_b).
\]

Taking independent boundaries eta,eta' from lambda and using (A1) twice gives

\[
\boxed{
\mathbb E_{\lambda\otimes\lambda}
W_1\!\left(F_\#\mu^\eta,F_\#\mu^{\eta'}\right)
\le
\delta_{\rm good}(b)+2\mu_{\beta,L}(A_b)
\le
\delta_{\rm good}(b)+32b^3\,18^{-b-2}.
}\tag{A4}
\]

Here W_1 is the Kantorovich distance with cost d, and F's dependence on the boundary is included in each pushforward. The only model-specific probability input beyond disintegration is (A2). This is a direct coupling and union-bound lemma; its proof is valid for every original continuous SU(2) Wilson finite-volume Gibbs law satisfying the cited input.

For a discrete observable F with distance d(x,y)=1_{x ne y}, W_1 is total variation and (A4) gives an averaged total-variation criterion, provided the stated good-region coupling exists. For continuous Wilson observables, bounded d may be a normalized Lipschitz metric.

## 3. Scale dependence and exact remaining target

For a physical width ell>0, b(a)=ceil(ell/a), even L(a)>=2b(a), and sufficiently large bare Wilson beta(a) satisfying the chessboard activity gate, the explicitly controlled bad-star contribution in (A4) tends to zero:

\[
32b(a)^3\,18^{-b(a)-2}\to0.
\]

If a new constructive good-region coupling theorem proves delta_good(b(a)) <= delta(a) with the contraction required by VOL07's physical all-sector transfer/covariance criterion, then (A4) becomes one **averaged physical-box input**. To use it, one must check that this averaged observable metric is the specific norm required in the physical transfer argument and that the conditioning/collar is compatible with the block map. Exponential bad-island rarity alone gives no estimate for delta_good.

At b=27 the exact island contribution 32b^3/18^(b+2) is less than 2^-101; at b=81 it is less than 2^-322. The good-region coupling is therefore the dominant unresolved term in this conservative high-beta regime.

## 4. Acceptance status

- Gibbs disintegration and averaged coupling inequality (A4): ANALYTIC / elementary measure-coupling theorem.
- Original periodic-even SU(2) p_b from source-attested FoldMix theorem and VOL10: CONDITIONAL ON INDEPENDENT LEAN KERNEL REBUILD / external human review.
- Constructive delta_good for physical Wilson observables, uniformly over physical scales and including all Gauss sectors: OPEN.
- Arbitrary-boundary Dobrushin-Shlosman cube or quantitatively adequate averaged replacement: OPEN.
- Renormalized block pushforward, nonzero continuum Wilson source, OS reconstruction, and eleven original continuum obligations: OPEN.

The immediate next analytic calculation is to derive an explicit gauge-invariant good-region coupling in the original SU(2) conditional law, including boundary orientation and Wilson source, with a quantitative delta_good(b) that can be inserted in (A4). Avoid replacing this with raw-link total-variation contraction, which VOL08's realizable frustrated-exterior witness already excludes uniformly at weak coupling.
