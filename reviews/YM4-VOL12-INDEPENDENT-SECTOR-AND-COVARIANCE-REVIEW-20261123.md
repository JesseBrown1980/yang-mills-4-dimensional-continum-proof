# VOL12 — independent mathematical review, winding sectors, and coupling target

**23 November 2026. Independent analytic reconstruction and original four-dimensional SU(2) exact-integer adversarial fixtures.** The user reports completing an external human mathematical review. No signed report or PR review submission was visible on PR #113 or issue #114 in the connector at the review checkpoint. That distinction affects archival provenance, not the tests below.

## 1. Independent verification of the exact source model

The published upstream archive was verified at SHA-256 f8a444517b2f013a287ec20075977cb0afa71c019de2d3c3da577118c05aea62. The [hosted independent Lean 4.33.1 rebuild](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/45174162871) completed 8,755 jobs and reported only the three standard axioms (propext, Classical.choice, Quot.sound) for FoldMix.rarity_orient.

An independent [native definition audit](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/45178898531) inspected the actual SHA-pinned Lean source:

- FoldChess/WilsonDataV1.lean:27: the configuration is a map from original positive links to norm-one quaternion QBall (SU(2)).
- FoldChess/RarityAllV1.lean:21: bigP is the strict original Wilson plaquette indicator **1 if y < 1 - Re(holonomy), else 0**.
- FoldChess/RarityEvenV1.lean:51: ballQ is the SU(2) quaternion chordal ball about identity.
- FoldChess/PeierlsEvenV1.lean:217: Zw is the total unnormalized Wilson-measure mass.
- FoldChess/MixAllV1.lean:66–71: FoldMix.rarity_orient bounds the Wilson integral of any finite set of plaquette-defect indicators of one orientation by Zw times q to the power of the set size. It requires even side L=2m, m>=2, beta>=0, and any positive Haar-cap radius.

The published [model chapter](https://computoergosum.com/en/principia/yang-mills/22-01-rarity-by-chessboard.html) identifies the original continuous SU(2) Wilson density as exp(beta sum Re U_p), with Re U_p = halftrace U_p and normalized Haar; the verified native definitions match this intended event and source model. This validates the substantive model-identification step, not merely the numerical checker.

## 2. Fresh reconstruction of the project-specific transfer

VOL10 and VOL11 prove that a bad original link star forces one of six incident original plaquette defects with y=epsilon/4. For an independent set of r original links, these forced plaquettes can be chosen to be distinct; at most 6^r choice assignments exist. Every assignment has at least ceil(r/6) plaquettes sharing one of the six plane orientations.

For a source chessboard rate q<1, probability for each assignment is at most q^ceil(r/6), and summation gives

\[
\boxed{P(\text{all }r\text{ chosen bad stars})\le (6q^{1/6})^r.}\tag{R1}
\]

With epsilon=1/16, y=1/64, cap radius 1/1280, and beta=9^6=531441, the exact Haar-cap comparison gives q<2^(-4001), hence rho=6q^(1/6)<2^(-663)<18^(-57). This satisfies VOL10's quantified independent-star input on untwisted even periodic L>=4. The original 18-degree graph and independent-set extraction then give the bound P(root bad cluster size >=m)<=18^(-m-2).

A based-link box of side b with 2<=b<=L/2 has 4b^3 roots on any coordinate boundary face. Any original graph path of bad links crossing to the opposite face has at least b bad-link vertices. Four-axis union yields P(any bad-star box crossing)<=16b^3/18^(b+2). The previously hosted original graph/crossing verifier passed; the derivation is consistent at the exact stated scope.

**Acceptance tier:** The upstream Lean result is independently kernel replayed. R1 and the box crossing are analytic original SU(2) implications supported by exact integer geometry; review of the combined proof by an outside referee is a separate provenance question. Arbitrary exterior, odd-sided, twisted and coarse pushforward measures require distinct certificates.

## 3. Independent deterministic all-sector falsifier: two flat holonomies

For any periodic even L>=4, define two true original SU(2) link fields, taking values in its centre {+I,-I}. Configuration A is +I on every positive link. Configuration B is -I on links in direction 0 based at x_0=L-1, and +I otherwise.

Every elementary plaquette is +I for both configurations; every one of the six three-edge staples of a link equals the original link. Thus **all fifteen double-staple pairs are aligned, every bad-star event is false and all plaquette deficits vanish**. However the ordinary SU(2) trace of the Polyakov loop winding once in direction 0 is +2 for A and -2 for B. This trace is invariant under periodic gauge transformations, establishing distinct flat-holonomy configurations.

The [independent exact centre-holonomy verifier](../../tests/ym4_vol12_independent_holonomy_audit.py) calculates all original plaquettes, all six staples and all fifteen pair comparisons for each positive link on L=4 and L=6; it confirms both winding traces. The frozen result is [here](../certificate-atlas/YM4-VOL12-INDEPENDENT-HOLONOMY-20261123.hbp).

This is a deterministic, gauge-invariant **scope control**, not a claim of positive Gibbs probability for a particular configuration. It demonstrates why the small periodic bad-island crossing probability alone cannot imply contraction of arbitrary winding observables. Local contractible Wilson observables and global centre/winding-sensitive observables must have separately identified coupling targets.

## 4. New exact boundary-to-Wilson covariance interface

Let eta denote the complement of an interior SU(2) link region T, and let lambda be its original Gibbs exterior marginal. Let f(U_T) in [0,1] be a gauge-invariant observable supported in the interior core of T, separated from the boundary by a collar, and g(eta) in [0,1] be exterior-measurable. Define m(eta)=E[f|eta].

Assume a conditional coupling produces the already derived bound, with the cost d(x,y)=|x-y|:

\[
D_b:=E_{\eta,\eta'} W_1(f_\#\mu^\eta,f_\#\mu^{\eta'})
\le \delta_{\rm good}(b)+32b^3\,18^{-b-2}.
\tag{R2}
\]

By coupling, |m(eta)-m(eta')|<=W1. Since m takes values in [0,1], the identity for two independent exterior copies gives

\[
2 Var_\lambda(m)=E_{\eta,\eta'}(m(eta)-m(eta'))^2\le D_b.
\]

Since g is exterior-measurable, Cov_mu(f,g)=Cov_lambda(m,g). Cauchy-Schwarz and Var(g)<=1/4 give the exact **conditional covariance bridge**

\[
\boxed{8\,|\operatorname{Cov}_\mu(f,g)|^2
\le \delta_{\rm good}(b)+32b^3\,18^{-b-2}.}
\tag{R3}
\]

This is a useful observable-specific physical-block acceptance interface. It requires a proof of delta_good(b) decaying at the correct physical scale and a mapping to the full VOL07 transfer norm before it can yield a continuum spectral gap.

The coefficient 8 is sharp for this chain of general inequalities: the independent checker replays an **abstract two-boundary control** in which the conditional inner state equals an equiprobable boundary bit, g equals the bit, D=1/2 and Cov=1/4, so 8Cov^2=D exactly. This control is abstract and is not offered as a Wilson Gibbs configuration.

## 5. Constructive next mathematical target: gauge-covariant staple transport

For an original link and its fixed six SU(2) staple quaternions s_1,...,s_6, define H=sum_i s_i. The one-link conditional density against Haar is proportional to exp(beta <u,H>) after the standard path-orientation identification.

On the good-star sector, every pairwise staple inner product is at least 1-epsilon. Therefore

\[
\boxed{|H|^2=6+2\sum_{i<j} s_i\cdot s_j\ge36-30\epsilon.}\tag{R4}
\]

At epsilon=1/16, |H|^2>=273/8. The preferred unit quaternion v=H/|H| is consequently well-defined.

For two local conditionals with equal staple-resultant norms |H|=|H'|, multiplication by R=v'v^(-1) transports one conditional law onto the other exactly: quaternion multiplication is orthogonal and normalized SU(2) Haar is left invariant.

**Subsequent stronger result:** [The beta-uniform SU(2) radial transport theorem](../docs/certificate-atlas/NOTE-YM4-VOL12-GOOD-STAR-RADIAL-TRANSPORT-20261123.md) uses the original S³ Haar density, the variable z=1-Re(U), and integration by parts to prove, for arbitrary two good-star exteriors,

\[
\boxed{\|R_\#\nu_H-\nu_{H'}\|_{\rm TV}
\le\frac32\left|\log\frac{t'}{t}\right|<\frac1{24}.}\tag{R5}
\]

The strict constant follows from |H|²,|H'|²>=273/8 and the purely integer test 273*37²=373737>373248=8*216² (margin 489). **The bound is uniform for every beta>0**, and at beta=0 the conditionals are identical Haar. It leaves an exact candidate neighbor budget 18/24=3/4, *provided multi-link gauge-frame alignments can be made coherent*. The next proof target is precisely that gauge/collar coherence and the handling of global centre/winding labels; the local radial mismatch is now quantitatively controlled.


**Next mathematical acceptance:** certify a quantitative good-region coupling for contractible local Wilson observables that yields delta_good(b) small enough in (R3), then separately certify physical all-sector transport including winding observables. Preserve the exact even periodic source scope; work on arbitrary exterior conditions and the coarse blocked law as separate gates.

**Reviewed scope:** upstream formal theorem and source mapping PASS, derived finite even-torus activity and crossing PASS at the stated imported-theorem scope, deterministic winding counterexample PASS, conditional covariance bridge DERIVED. External human report archived in PR: PENDING ARTIFACT. Constructive delta_good, physical-size cube, multiscale pushforward, and all eleven original continuum obligations: OPEN.
