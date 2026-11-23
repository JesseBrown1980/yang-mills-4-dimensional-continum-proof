# YM4-VOL12 — physical-width bad-star crossing from the chessboard theorem

23 November 2026 — original continuous SU(2) Wilson, source-attested external Lean theorem with independent Lean kernel rebuild PASS; external human review OPEN. This is a geometric consequence of [VOL10](NOTE-YM4-VOL10-BAD-ISLAND-CRITERION-20261122.md) and the [VOL12 chessboard bridge](NOTE-YM4-VOL12-CHESSBOARD-BRIDGE-20261123.md).

## A. Precise external premise

The published upstream Lean archive was independently fetched with verified SHA-256 f8a444517b2f013a287ec20075977cb0afa71c019de2d3c3da577118c05aea62:

https://computoergosum.com/en/principia/lean/principia-ym-three-volumes-2026-11-13.tar.gz

The exact theorem FoldMix.rarity_orient occurs at FoldChess/MixAllV1.lean:66. Its inputs include N=2m, m>=2, beta>=0, cap r>0, one plane orientation mu<nu, and **every finite site set S**. Its inequality is:

\[
\int \prod_{x\in S}\mathrm{bigP}_{N,y}(U,(x,\mu),\nu)\,d\mu_W(U)
\le Z_W\left(\frac{\exp[\beta(48r^2-y)]}{h(r)^4}\right)^{|S|}.
\]

The downloaded upstream axioms.txt gives [propext, Classical.choice, Quot.sound] for this theorem and FoldWilson.wilson_chessboard_even. Its toolchain is Lean v4.33.1. The downloaded source and recorded axiom outputs have been inspected, and a separate independent Lean 4.33.1 kernel rebuild has passed ([hosted result](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/45174162871), 8,755 jobs, standard-three axioms only).

At epsilon=1/16, beta=9^6=531441, the chessboard implication from the previous VOL12 note gives rho<2^-663<18^-57. Then the VOL10 conditional cluster theorem yields, for any original positive-link root o and m>=1, under the even-sided untwisted periodic SU(2) Gibbs law,

\[
\Pr_{\beta,L}(|C(o)|\ge m)\le18^{-m-2}.
\tag{C1}
\]

The inference depends on the externally sourced FoldMix result.

## B. Original 4D box crossing lemma

Take 2<=b<=L/2, with L even, and the based-link vertex box Q_b={0,...,b-1}^4. Define Cross_nu(Q_b) as the event that a path of bad-star links in the **original plaquette-sharing link graph**, all based at sites in Q_b, touches both faces x_nu=0 and x_nu=b-1.

Two original links sharing a plaquette have base vertices differing by at most one site in every coordinate. Because b<=L/2, a path restricted to the box cannot jump between opposing faces by periodic wraparound. Every crossing path therefore has at least b distinct bad-link vertices, and a root on the first face. There are exactly 4b^3 positive links based at that face. Applying (C1) and a union bound yields

\[
\Pr(\mathrm{Cross}_{\nu}(Q_b))\le4b^3\,18^{-b-2}.
\]

Summing over four coordinate axes gives the **unconditional periodic-equilibrium bad-star crossing estimate**

\[
\boxed{\Pr(\mathrm{Cross}(Q_b))\le
\min\{1,16b^3\,18^{-b-2}\}.}
\tag{C2}
\]

The upper bound decreases strictly for b>=2, because ((b+1)/b)^3 <=27/8<18. Exact integer examples from the linked checker:

| based-link box side b | upper probability |
|---:|---:|
| 2 | less than 2^-9 |
| 3 | less than 2^-12 |
| 9 | less than 2^-32 |
| 27 | less than 2^-102 |
| 81 | less than 2^-323 |

## C. Physical-width limit — conditional geometric corollary

For any fixed positive physical width ell, choose lattice spacings a tending to zero, b(a)=ceil(ell/a), even periodic L(a)>=2b(a), and any coupling sequence beta_W(a)>=531441 for which the source chessboard activity bound persists. The same estimate gives

\[
\Pr(\mathrm{Cross}(Q_{b(a)}))\le16b(a)^3\,18^{-b(a)-2}\longrightarrow0.
\tag{C3}
\]

This is a volume-uniform, **one-scale periodic Gibbs probability** for geometrically connected bad-link islands crossing a physically large cube. It does not require independent plaquette defects.

## D. Acceptance and next mathematics

The physical-size Dobrushin-Shlosman cube needed by VOL07 is a much stronger object: it controls boundary-conditioned or appropriately averaged block distributions and all physical Gauss sectors. The periodic crossing bound supplies a quantitative bad-island component. To reach that cube, we still need good-region coupling, bounds on boundary frustration and the pushforward through blocking.

- External FoldMix source and bundled axiom record: SOURCE-PINNED/INSPECTED, independent Lean kernel rebuild PASS.
- Original even-torus joint bad-star and crossing implication: ANALYTIC, conditional on the external formal theorem; exact integer source check PASS.
- Arbitrary-boundary physical cube, multiscale blocked measure, full transfer rate and all 11 original continuum gates: OPEN.

[Original 4D integer checker](../../tests/ym4_su2_vol12_block_crossing.py) · [frozen HBP receipt](YM4-VOL12-BLOCK-CROSSING-20261123.hbp) · [hosted external source attestation](../../.github/workflows/ym4-vol12-external-chessboard-attest.yml).
