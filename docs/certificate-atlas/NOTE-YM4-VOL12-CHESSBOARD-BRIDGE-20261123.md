# YM4-VOL12 — conditional-import chessboard bridge to unconditional even-volume bad-star islands

**23 November 2026 — mathematical implication from a published same-orientation chessboard estimate; external theorem source and independent peer review require acceptance.**

This note is the next direct mathematical step after [VOL10](NOTE-YM4-VOL10-BAD-ISLAND-CRITERION-20261122.md), [VOL11](NOTE-YM4-VOL11-SEPARATED-DEFECTS-20261122.md), and the two [VOL12](NOTE-YM4-VOL12-FINITE-PACKET-PILOT-20261123.md) [pilot results](NOTE-YM4-VOL12-REPAIR-DEFICIT-20261123.md). It combines their original continuous-SU(2) geometry with an **external, explicitly stated** reflection-positivity chessboard theorem, obtaining a volume-uniform **unconditional** joint bad-star rate on **even-sided periodic** lattices.

**Dependency classification:** the external same-orientation theorem (CB-ORIENT below) is **IMPORTED FROM LITERATURE / SOURCE AUDIT OPEN**; the transfer from CB-ORIENT to the VOL10 independent-star and cluster bound is proved below. Integer-only checks verify the constants, geometry, and scope, *not the imported reflection-positivity proof*. This is a source-dependent mathematical acceptance candidate rather than an independently closed all-volume certificate.

## A. Exact external input — CB-ORIENT(y,a,beta,L)

The public source [*Rarity of large plaquettes — the chessboard estimate*, §04–05](https://computoergosum.com/en/principia/yang-mills/22-01-rarity-by-chessboard.html) describes its Lean theorem \`FoldMix.rarity_orient\` as follows.

For the **original, untwisted, continuous SU(2) Wilson measure** with \`exp(beta sum_p halftrace(U_p))\` on the four-dimensional periodic torus of even side \`L=2m>=4\`, for any fixed plaquette orientation \`(mu,nu)\`, any set \`X\` of **distinct original plaquettes of that orientation**, any \`0<y<=2\`, and a positive Haar cap radius \`a\` with \`48 a^2<y\`, reflection positivity and the cap comparison yield
\[
\tag{CB-ORIENT}
\mu_{\beta,L}\bigl(\forall p\in X:\ 1-W_p>y\bigr)
\le Q_{\beta,y,a}^{|X|},\qquad
Q_{\beta,y,a}=
\frac{\exp[-\beta(y-48a^2)]}{h(a)^4},
\]
where \`h(a)\` is the normalized Haar probability of the SU(2) chordal cap \`|U-I|<a\`.

The article states the general-\`y\` same-orientation rate and the coefficient \`48a^2\` explicitly; it cites the Lean declaration. **Our repository has not reproduced the underlying reflection-positivity folding proof or independently retrieved the declaration from its original Lean source**. Its assumptions must be cross-checked against that source before independent signoff. Both orientation and even-side restrictions are essential.

The source's convention \`Re(U_p)\` is exactly \`halftrace(U_p)\` in the SU(2) defining representation. Thus there is **no coupling renormalization factor** in this import.

## B. Unconditional bad-star joint bound from original VOL10 geometry

Let \`epsilon=1/16\`, \`y=epsilon/4=1/64\`, and \`S\` be any independent set of \`r\` original positive links in the 18-degree original plaquette-sharing link graph.

The configuration-wise original-SU(2) lemma already checked in VOL09–VOL11 gives:
\[
B_e=1 \Rightarrow \bigcup_{p\ni e}\{1-W_p>y\}.
\]
There are exactly six incident original plaquettes for each original positive link. For every choice function \`e -> p(e)\`, the \`r\` selected plaquettes are distinct, because no two distinct links in \`S\` share a plaquette.

Therefore
\[
\{\forall e\in S:B_e=1\}
\subseteq\bigcup_{\text{at most }6^r\text{ choices}}
\{\forall e\in S:1-W_{p(e)}>y\}.
\]

Group the \`r\` selected plaquettes into their six unoriented lattice-plane orientations. One orientation contains at least \`ceil(r/6)\` plaquettes. On the event all selected defects occur, that entire orientation subset is defective; by CB-ORIENT, **provided \`Q<1\`**, each choice event has probability at most \`Q^ceil(r/6)<=Q^(r/6)\`.

Summing over choices produces the **genuine original Wilson Gibbs probability**
\[
\boxed{
\mu_{\beta,L}\bigl(\forall e\in S:\,B_e=1\bigr)
\le \left(6 Q_{\beta,y,a}^{1/6}\right)^r
=:\rho_{\beta,y,a}^{\,r}.
}\tag{VOL12.CB1}
\]
This is unconditional and **uniform in every even periodic \`L>=4\`**. It requires the imported same-orientation theorem rather than a product-independence assumption or a good-boundary factorization.

## C. Entirely integer conservative SU(2) rate

Choose the cap radius prescribed in the source's general-threshold discussion:
\[
y=1/64,\quad a=y/20=1/1280,\quad
d:=y-48a^2=1597/102400>0.
\]

By comparison with an SU(2) **geodesic cap** of angular radius \`a\`, which lies inside the chordal cap, VOL09's elementary Haar estimate gives
\[
h(a)\ge a^3/24=1/(24\cdot1280^3).
\]
The resulting cap comparison is
\[
Q_{\beta,y,a}\le A e^{-\beta d},
\qquad A=(24\cdot1280^3)^4.
\]

On the exact ternary integer sequence \`beta=9^k\`, \`e^2>2\` yields the rational upper envelope
\[
Q_{9^k,y,a}<\frac{A}{2^{N_k}},\qquad
N_k=\left\lfloor\frac{9^k\,1597}{204800}\right\rfloor.
\]
At \`k=6\`, \`beta=531441\`, \`N_6=4144\`, and \`A<2^143\`. Thus
\[
Q_{9^6}<2^{-4001},\quad
\rho_{9^6}=6 Q_{9^6}^{1/6}<2^{-663}<18^{-57}.
\]
The comparison \`2^{-663}<18^{-57}\` follows from \`18<32=2^5\`. An independent exact integer test verifies the sharper equivalent inequality \`6^6 A 18^342 < 2^4144\`; no floating-point exponentials or numerical Haar integrations occur.

## D. Transfer into the previously conditional VOL10 cluster theorem

Provided **CB-ORIENT** holds with the above scope, VOL12.CB1 supplies the missing \`VOL10-JOINT(rho,beta,epsilon,L)\` assumption for **every independent set** \`S\` and every **even side \`L>=4\`** at \`beta=9^6\`.

The already proved VOL10 combinatorial theorem therefore implies for every original positive root link \`o\` and integer \`m>=1\`,
\[
\boxed{
\mu_{9^6,L}\bigl(|C(o)|\ge m\bigr)
\le 18^{-m-2},\qquad
L\in2\mathbb N,\ L\ge4.
}\tag{VOL12.CB2}
\]

This is a **finite-lattice, bare-weak-coupling, untwisted periodic result**. It uses an external volume-uniform chessboard theorem and does not imply the required **physical-size cube**, boundary-conditioned all-sector transfer comparison, renormalized Wilson source, or continuum OS construction.

## E. Adversarial scope gates and originality

- **PASS conditional on CB-ORIENT:** authentic SU(2) continuous Haar, exact conventional Wilson coupling normalization, external chessboard input for **one orientation only**, six-choice and six-orientation union, independent star geometry, exact integer exponent.
- **REJECT:** generalize from even to odd side \`L=3,5,...\` by a change of notation; even-sided chessboard folds do not provide that.
- **REJECT:** infer a valid CB-ORIENT statement for fixed adversarial exterior boundary values, twisted sectors, the blocked measure at another scale, or the physical beta band \`~2-3\`.
- **REJECT:** label chessboard/Peierls reflection positivity or the strong-bare-coupling activity as first-in-literature; the import is prior work, and the source already addresses uniform plaquette rarity.
- **EXTERNAL SOURCE AUDIT OPEN:** independently retrieve and inspect \`FoldMix.rarity_orient\`, check its exact cap hypotheses and halftrace normalization, and seek a separate human mathematical review. Only then promote the imported theorem to independent acceptance.
- **11 original continuum obligations:** OPEN. **Original continuum Yang–Mills existence/mass gap:** OPEN.

The original [integer-only checker](../../tests/ym4_su2_vol12_chessboard_bridge.py) provides exact \`3^4\` negative and \`4^4,6^4\` positive geometry fixtures, six plane-orientation checks, arithmetic inequalities, and explicit red gates. The [receipt](YM4-VOL12-CHESSBOARD-BRIDGE-20261123.hbp) is stable across normal and optimized runs. The [external theorem scope report](../../reviews/YM4-VOL12-CHESSBOARD-IMPORT-AUDIT-20261123.md) records the provenance boundary.

**Next mathematical acceptance:** obtain a verifiable version-pinned formal source for CB-ORIENT, test the full conditional behavior for physical-size blocks, and establish the cross-scale transfer. At one even-lattice fixed-bare-coupling scale, the VOL10 cluster theorem's **numeric hypothesis is met if the imported published theorem is accepted**.
