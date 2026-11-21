# YM4-07D — an all-finite-coupling polynomial Wilson-source floor for genuine 4D SU(2)

**November 20, 2026.** Prediction frozen before the new checker in [PREDICT-YM4-07D-ALLBETA-SU2-20261120.hbp](PREDICT-YM4-07D-ALLBETA-SU2-20261120.hbp), commit \`788de567557f1f28e97b187c8f2cbc3499f9e925\`. This note gives an analytic theorem for the original finite-volume **continuous SU(2)** 4D Wilson measure, an exact one-link nonplaquette-network comparison, and integer-only controls. The theorem is a local Gibbs-source result; spectral-projector and continuum-scale claims stay **OPEN**.

## 1. Quantitative improvement of YM4-07C

Let the four-dimensional periodic hypercubic lattice have side lengths at least three (this ensures six independently realizable staples around a selected link). Put normalized Haar SU(2) variables on links and the standard Wilson Gibbs density
\[
d\mu_{\Lambda,\beta}(U)=Z^{-1}\exp\{\beta\sum_{p}\tfrac12\operatorname{ReTr}U_p\}\prod_\ell dU_\ell,\qquad \beta\ge0.
\]
For any elementary plaquette \(p\), let \(W_p=\operatorname{ReTr}(U_p)/2\).

**Theorem.** At every finite bare coupling \(\beta\ge0\),
\[
\boxed{\operatorname{Var}_{\mu_{\Lambda,\beta}}(W_p)>
\frac{1}{2^{18}(1+6\beta)^2}.}
\]
The constant is **independent of lattice volume**. At \(\beta=0\) the true variance equals \(1/4\); the displayed floor is conservative. The earlier YM4-07C estimate \(\operatorname{Var}(W_p)\ge e^{-12\beta}/4\) remains valid, so their maximum can be used.

Unlike the earlier exponentially small bound, this explicit lower floor has polynomial \(\beta^{-2}\) behavior. It nevertheless tends to zero along a weak-coupling continuum trajectory \(\beta(a)\to\infty\). It is not a cutoff-uniform renormalized OS source norm.

## 2. Genuine six-staple one-link law and all network terms

Condition on every link except one selected link \(u\) of \(p\). In four dimensions, six plaquette terms involve \(u\); all other Boltzmann factors cancel in the conditional probability. Each staple can be represented by a unit quaternion \(v_j\in S^3\), with a consistent orientation, giving
\[
d\mu(u\mid U_{\mathrm{others}})
=\frac{\exp(\beta\,u\cdot q)}{Z_\beta(Q)}\,d\mathrm{Haar}(u),
\quad q=\sum_{j=1}^6v_j,\quad Q=|q|^2\le36.
\]
The selected plaquette observable has the form \(W_p=u\cdot h\) for a *unit* quaternion \(h\), including its possible reversed-link orientation.

The exact SU(2) Haar integral, already derived in [YM4-05A](NOTE-YM4-05A-CHARACTER-WEAK-COUPLING-20261107.md), is
\[
Z_\beta(Q)=\frac{2I_1(\beta\sqrt Q)}{\beta\sqrt Q}
=\sum_{m=0}^{\infty}\frac{(\beta^2Q)^m}{4^m m!(m+1)!},
\qquad Z_\beta(0)=1.
\]
The second equality supplies a positive real series at **every** \(\beta\), including large weak-coupling values. In particular
\[
Q=6+2\sum_{1\le j<k\le6}\!v_j\cdot v_k.
\]
The 15 pair terms are normalized traces of six-link closed networks (staple products), split into **3 same-plane rectangles and 12 mixed-plane chairs**. The \(\log Z_\beta(Q)\) interaction is nonlinear in their sum. The small-\(\beta\) exact coefficient control,
\[
Z_\beta=1+\beta^2Q/8+\beta^4Q^2/192+\cdots,\qquad
\log Z_\beta=\beta^2Q/8-\beta^4Q^2/384+\cdots,
\]
is only a series check; the integral and theorem work for all finite \(\beta\). This one-link integration is distinct from the whole-lattice \(b=2\) blocked-action calculation, where the first chair coefficient occurs at order \(\beta^{10}\) ([YM4-03C](NOTE-YM4-03C-BLOCKED-ACTION.md)).

## 3. Complete elementary proof of the polynomial variance floor

Write \(t=\beta|q|\), so \(0\le t\le6\beta\). If \(q\ne0\), rotate the quaternion coordinates so that \(u=(s,u_\perp)\in S^3\) and the conditional density is proportional to \(e^{ts}\). If \(q=0\), take any direction. At fixed \(s\), \(u_\perp\) is uniform on a two-sphere of radius \(\sqrt{1-s^2}\). Thus the covariance of \(u\) has one radial eigenvalue \(\operatorname{Var}(s)\) and three identical tangential eigenvalues
\[
\frac13\mathbb E(1-s^2).
\]
A lower bound on both eigenvalues bounds the variance of **every** unit projection \(u\cdot h\).

**Case \(0\le t\le1\).** The density relative to normalized Haar satisfies
\[
\frac{e^{t(s-1)}}{\mathbb E_{\mathrm{Haar}}e^{t(s-1)}}\ge e^{-2t}\ge e^{-2}>1/9.
\]
Haar has mean zero and variance \(1/4\) for any unit quaternion coordinate. For any real center \(b\), compare the squared deviations under conditional and Haar probability, then minimize over \(b\). It follows that
\[
\operatorname{Var}(u\cdot h)>1/36.
\]
Here \(e^2<9\) is elementary, and no numerical exponential approximation is required.

**Case \(t\ge1\).** Set \(c=(1+t)^{-1}\), so \(0<c\le1/2\), and \(y=1-s\in[0,2]\). Ignoring a common Haar normalization, the marginal density of \(y\) is
\[
e^{-ty}\sqrt{y(2-y)}\,dy,
\quad
D(t)=\int_0^2e^{-ty}\sqrt{y(2-y)}\,dy.
\]
Using \(\int_0^\infty e^{-ty}\sqrt{y}\,dy=\sqrt\pi/(2t^{3/2})<t^{-3/2}\) and \(t\ge(2c)^{-1}\), obtain
\[
D(t)<\sqrt2\,t^{-3/2}\le4c^{3/2}.
\]

Take two disjoint events \(A=\{0\le y\le c/4\}\) and \(B=\{c/2\le y\le3c/4\}\). Throughout them \(y\le1\), hence \(\sqrt{y(2-y)}\ge\sqrt y\). Also \(e^{-ty}\ge e^{-1}>1/3\) and \(\sqrt2<3/2\). Integrating the elementary lower estimates gives
\[
\Pr(A)>1/144,\qquad\Pr(B)>1/72.
\]
For two independent copies \(Y,Y'\), \(\operatorname{Var}(Y)=\frac12\mathbb E(Y-Y')^2\). The \(A\times B\) and \(B\times A\) pairs have \(|Y-Y'|\ge c/4\). Therefore
\[
\operatorname{Var}(s)=\operatorname{Var}(Y)>
\frac{c^2}{144\cdot72\cdot16}
=\frac{c^2}{165888}.
\]
Moreover \(1-s^2=y(2-y)\ge y\ge c/2\) on \(B\), so the tangential eigenvalue satisfies
\[
\frac13\mathbb E(1-s^2)>\frac{c}{432}
\ge\frac{c^2}{432}.
\]
Both bounds are greater than \(c^2/2^{18}\), since \(165888<262144\) and \(432<262144\).

Combining the two cases, every unit \(h\) and every six-staple configuration satisfy
\[
\operatorname{Var}(u\cdot h\mid U_{\mathrm{others}})
>\frac1{2^{18}(1+t)^2}
\ge\frac1{2^{18}(1+6\beta)^2}.
\]
The law of total variance,
\(\operatorname{Var}(W_p)\ge\mathbb E[\operatorname{Var}(W_p\mid U_{\mathrm{others}})]\),
proves the theorem for the genuine continuous SU(2) Wilson lattice measure.

**Boundary check:** the argument uses compact Haar, positivity of Wilson weight, genuine dimension-four incidence and the unit norm of a plaquette's selected-link quaternion coefficient; it contains no finite-group replacement or finite-volume count in the bound.

## 4. Explicit nonplaquette closure falsifier at large coupling

Take the selected link \(u=1\) and six staples, each of which has zero real part, so **all six individual plaquette traces are zero**.

* Configuration A: every staple is the quaternion \(i\). Then \(Q_A=36\).
* Configuration B: three staples are \(i\), three are \(-i\). Then \(Q_B=0\).

These data can be realized by assigning the six distinct shifted axial links \(U_\mu(x\pm\nu)\) (for \(\nu\ne\mu\)) and setting the other relevant links to identity, on a periodic lattice of side lengths at least three. The six individual plaquette traces agree between the configurations, while their 15 gauge-invariant staple-pair traces differ. For every \(\beta>0\),
\[
Z_\beta(Q_A)
=1+\frac{36\beta^2}{8}+\text{strictly positive higher terms}
>1+\frac92\beta^2,\qquad Z_\beta(Q_B)=1.
\]
Thus exact local link elimination cannot be represented by a function of the six individual plaquette traces alone. The mixed-plane Wilson-network data must be retained or their total effect bounded. At \(\beta=16,64\), the integer checker certifies \(Z_A>1153,18433\), respectively, versus \(Z_B=1\).

This is a **one-link conditional integration** and a network-basis obstruction. It is not a one-step whole-lattice weak-coupling renormalization map or a computed physical transfer spectrum.

## 5. Exact benchmarks and checkable limits

The polynomial bound, as rational numbers, reads:

| \(\beta\) | Certified strict variance floor |
|---|---|
| \(0\) | \(1/262144\) |
| \(1/8\) | \(1/802816\) |
| \(1\) | \(1/12845056\) |
| \(16\) | \(1/2466512896\) |
| \(64\) | \(1/38856294400\) |

The [integer-only independent control](../tests/test_ym4_07d_su2_allbeta_source.py) checks the cap-bound constants, two- and four-degree Haar moments using the 24 exact binary-tetrahedral quaternions as a *finite exact design control*, all 15 pair interactions, the distinct nonplaquette endpoint configurations, the rational benchmarks, and ten false claims. The continuous Haar integral and all-real-\(\beta\) inequalities are proven analytically above; finite design tests corroborate moments, rather than replacing the continuous measure.

## 6. Exact one-link Euclidean conditional-projection residual

There is also an **actual orthogonal projector** available at this local step, though it is **not the physical-energy spectral projector**. In the genuine finite-lattice Gibbs Hilbert space \(L^2(\mu_{\Lambda,\beta})\), let
\[
P_\ell f=\mathbb E_{\mu_{\Lambda,\beta}}[f\mid\text{all links except }\ell].
\]
This is the orthogonal conditional-expectation projector onto functions of the retained links. For \(\ell\) one of the four links of \(p\), the exact conditional-variance identity and section 3 give
\[
\boxed{\|(I-P_\ell)W_p\|_{L^2(\mu)}^2
=\mathbb E_\mu[\operatorname{Var}(W_p\mid U_{\ne\ell})]
>\frac1{2^{18}(1+6\beta)^2}.}
\]
Thus exact elimination of one link necessarily removes a nonzero \(L^2\) component of its plaquette source at every finite \(\beta\), even if all 15 induced staple-pair interactions are retained in the effective weight. This is a **measured mathematical source-defect floor** for one-link conditional projection; the projection is onto a link-variable sigma algebra, not onto a physical Hamiltonian energy window. It does not furnish either of the \(\delta,\epsilon\) *upper* bounds in YM4-07C, and it is not a lower bound on the error of every possible enriched RG map.

## 7. Research handoff: where the physical projector must enter

The following is now available: a genuine SU(2) finite-lattice source floor with volume-independent explicit polynomial dependence on \(\beta\), plus exact retention of nonplaquette interactions at the one-link level.

To complete the requested **weak-coupling source-and-projector RG step**, separately construct a gauge-invariant all-links blocking map at successive cutoffs, an OS time-zero Wilson source with physical units, the induced Wilson-network interaction norm including 12 mixed-plane pair sectors, and a true spectral projector onto the **same physical-energy window**. Then certify source and projector errors across the block, all large-field tails, and eventual summability. This local theorem does not supply these operators.

**Acceptance ledger:** local SU(2) source theorem **ANALYTIC DERIVATION + EXACT-INTEGER CONTROLS**; source full-RG transport **OPEN**; physical OS spectral projector **OPEN**; nontrivial four-dimensional continuum and full-spectrum mass gap **OPEN**.
