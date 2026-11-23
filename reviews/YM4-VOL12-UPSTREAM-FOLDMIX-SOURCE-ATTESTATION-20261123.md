# YM4 VOL12 upstream FoldMix source attestation — independently retrieved archive

**23 November 2026. Hosted SHA-256 source verification PASS. Original Lean kernel rebuild OPEN until separately measured.**

## Evidence and exact provenance

The [upstream SU(2) chessboard chapter](https://computoergosum.com/en/principia/yang-mills/22-01-rarity-by-chessboard.html) identifies FoldMix.rarity_orient and FoldWilson.wilson_chessboard_even.

A hosted GitHub Actions run downloaded the actual published source archive at https://computoergosum.com/en/principia/lean/principia-ym-three-volumes-2026-11-13.tar.gz and verified SHA-256 **f8a444517b2f013a287ec20075977cb0afa71c019de2d3c3da577118c05aea62**.

- [Hosted source attestation run #45173527653](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/45173527653): PASS; actual source archive and declaration/proof lines were inspected, not inferred from the book's prose.
- [Upstream theorem and supporting declaration](https://computoergosum.com/en/principia/yang-mills/22-01-rarity-by-chessboard.html): FoldChess/MixAllV1.lean:66–71. Its proof invokes rarity_orient_tau and an orientation permutation.
- Named prerequisite: FoldWilson.wilson_chessboard_even in FoldChess/WilsonChessV1.lean:118.
- Companion general-threshold wrapper: FoldMix.rarity_uniform_all_mix in FoldChess/MixAllUniformV1.lean:15–30.
- Upstream toolchain: leanprover/lean4:v4.33.1.
- Upstream DECLS.tsv maps FoldMix.rarity_orient to FoldChess.MixAllV1:66.
- Upstream axioms.txt line 235 lists FoldMix.rarity_orient [propext, Classical.choice, Quot.sound]; line 244 similarly lists FoldWilson.wilson_chessboard_even. These are **published output records** and not a substitute for our own independent Lean kernel run.

## Exact imported theorem quantifiers

The declaration has arguments N,m with N=2m and 2<=m, real beta>=0, real threshold y and cap r with r>0, any plane orientation mu<nu in Fin 4, and **every finite set S of original sites**. It bounds the UNNORMALIZED original Wilson integral

\[
\int \prod_{x\in S}\mathrm{bigP}(N,y,U,(x,\mu),\nu)\,d(\mathrm{wilsonMeasure}(N,\beta))
\le
\mathrm{Zw}(N,\beta)\left(\frac{e^{\beta(48r^2-y)}}{h(r)^4}\right)^{|S|}.
\]

Here bigP is the indicator of the original gauge-invariant plaquette defect. Dividing by Zw yields the simultaneous same-plane probability inequality used in VOL12. The source makes no assumption that the sites of S are nonadjacent; distinct site labels already correspond to distinct plaquettes of one fixed orientation.

The upstream mixed reflection argument is specific to **untwisted even-sided periodic Wilson SU(2)**. The original VOL12 packet proof retains this scope. The conditional local repair calculation and the original periodic crossing lemma are separate results with their own hypotheses.

## Acceptance status

- SOURCE ARCHIVE SHA-256 / location / complete FoldMix signature: PASS.
- INDEPENDENT ARITHMETIC of q, rho and VOL10 18-degree link graph: PASS through prior VOL12 hosted jobs.
- UPSTREAM PUBLISHED AXIOM RECORD: LOCATED, standard-three-only as recorded by upstream.
- INDEPENDENT LEAN KERNEL REBUILD of this exact archive: STARTED as separate read-only hosted CI workflow; verdict must be read from its hosted run, not assumed.
- EXTERNAL HUMAN REFEREE SIGNOFF and physical-width boundary-conditioned SU(2) cube: OPEN.
- All 11 original continuum construction obligations: OPEN.

The current source attestation supports a **source-dependent theorem**; independent kernel acceptance and external mathematical review remain explicit future gates.
