# Four-dimensional Yang–Mills Certificate Atlas

## November 22 — Complete original Wilson certificate reconciliation and volume bridge

The **[live clickable 4D atlas](https://raw.githack.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/main/docs/certificate-atlas/index.html)** now has **92 curated source-linked nodes**, **500 indexed resources**, **92 PR history entries**, and **11 explicitly OPEN continuum obligations**. The preceding November 21 survey of 76 nodes is preserved as historical context. The 16 new 3D graph points cover original SU2 local transfer WT01, original Wilson cylinder WC01, physical-vacuum WV01, WG01 through WG08, WG09 symmetry/Haar/spin/full-operator acceptance, and VOL01 larger-volume geometry.

For **fixed spatial L=2** and **0<beta<=10^-12**, [WG09 independently audited full-operator ordering](../NOTE-YM4-WG09-FINITE-BETA-ORDER-CERT-20261121.md) identifies the individual first *center-neutral* Wilson-visible eigenmode with true-vacuum squared spectral weight >1/289 and physical eigenvalue spacing greater than exp(-24 beta) kappa1(beta)^4 (21/320) beta^3. The first excitation across all physical center sectors is still charged and has zero local contractible Wilson weight. Hosted [exact independent audit and remainder verification](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/44956744803) passed; PRs #96, #97 and #98 are merged. All original source files and SHA receipts have pinned links in the machine manifest.

The new [YM4-VOL01 larger-volume structural result](NOTE-YM4-VOL01-VOLUME-SLOPE-OBSTRUCTION-20261122.md) proves that the fundamental plaquette-band first magnetic derivative vanishes for L>=3, unlike the exceptional L=2 double-winding six-block mechanism. The next mathematical objective is an exact third-order **connected plaquette kernel** with an **L-independent cluster error**. This is an uncompleted volume-uniform spectral theorem; higher-volume/weak-coupling/continuum obligations remain OPEN.

The graph is SVG/CSS only, with four modes and three camera views. Click the new green WG or blue VOL nodes to open their source cards. The older pinned records are preserved, and each new source is pinned to an exact repository commit.


## November 21 — Second certified-source survey

The live atlas now contains **76 source-linked graph nodes**, including **22 external candidate references** and the unchanged **11 OPEN proof tasks**. [The new cross-repository search ledger](EXTERNAL-SEARCH-ROUND2-20261121.md) records Lean strong-coupling correlations, exact SU(2) Racah/6j coefficients, Wilson cluster-area bounds, Euclidean spectral dual methods, and formal comparison targets; each source links to its exact original repository commit or published DOI. None is automatically promoted to a continuum SU(2) result.

We also added [YM4-SW01](NOTE-SPECTRAL-WINDOW-DUAL-20261121.md), a genuine *positive spectral measure* dual-polynomial inequality with an [exact-integer checker](../../tests/test_ym4_certificate_spectral_window_dual.py) and [frozen prediction](PREDICT-SPECTRAL-WINDOW-DUAL-20261121.hbp). It operates on **certified physically normalized connected Wilson moments**; its calibration test uses an explicitly labelled toy spectrum. A positive result proves **total window weight**, while the first excited Wilson state remains a distinct eigenvalue-isolation gate.



**Pinned audit: November 21, 2026.** Companion to the [finite 3D Yang–Mills certificate atlas](https://raw.githack.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C/main/docs/certificate-atlas/atlas-current-20261120.html) and its original-source finite S₃ Wilson weight acceptance.

## [▶ OPEN THE LIVE 4D CERTIFICATE ATLAS](https://raw.githack.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/main/docs/certificate-atlas/index.html)

[Alternate live HTML renderer](https://htmlpreview.github.io/?https://raw.githubusercontent.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/main/docs/certificate-atlas/index.html) · [Standalone graph](index.html) · [Four-panel SVG overview](overview.svg) · [Complete source and PR manifest](certificates.json) · [HBP proof-node index](ATLAS-INDEX.hbp) · [Open gate and external certificate search](BRIDGE-LEDGER.md) · [Viewer help](OPEN-3D-VIEWER.md).

**Use the rendered link, not the ordinary GitHub HTML file view.** The atlas is a standalone offline-capable **SVG/CSS-only** page. Four graph families, three camera positions, clickable 3D proof points and linked source records reproduce the existing finite atlas's interaction style. No JavaScript or remote graph libraries are required.

![4D proof graph overview](overview.svg)

## Inventory and scientific scope

The manifest is a source-linked **index, not a replacement for original certificates**. It records pinned 4D `main` notes and the examined PR #75–#80 stacked draft tree, exact HBP/HBI/SHA review receipts and checks, machine source hashes, and links to the finite and independent-public-research repositories.

All curated graph nodes carry **status, model group, physical assumptions, dependencies, proof stage, and an immutable source link**. The proof graph's 3D coordinates are intentionally categorical. They encode proof workflow, not measured energy eigenvalues, coupling values, gap sizes, performance or certificate rank.

The colors explicitly distinguish:
- **Accepted finite-scope internal result:** a mathematical claim with finite-lattice/Haar assumptions and an existing source.
- **Draft-checked:** hosted and independently audited code and derivation on an unmerged PR; the atlas does not silently promote it into `main`.
- **Conditional:** a proof implication with an unproved hypothesis.
- **Open / Hold:** a missing mathematical input, or a certificate gate failed by the current envelopes.
- **Finite S₃ / External candidate:** a separately sourced theorem, calculation or lead; no automatic transfer to SU(2) or continuum mass gap.

The **OPEN CERTIFICATES** map and [acceptance/search ledger](BRIDGE-LEDGER.md) mark our next proof obligations and record which outside certificates we have located, including their gauge group, normalization, level of formal proof, and missing transport.

## Ways to use the atlas

1. Select **Proof architecture** to see the sequence from Haar and transfer to Wilson and the continuum conditions.
2. Select **Wilson and spectrum** to find the original first-weight target, source Gram/moment inputs and physical-time normalization.
3. Select **Representation cutoffs** to compare the *verified inequalities* for powers of three, with HOLD/ PASS labels clearly separated from actual eigenvalues.
4. Select **Cross-repository** to see the bridge to the [finite atlas](https://raw.githack.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C/main/docs/certificate-atlas/atlas-current-20261120.html) and independently attributed Lean and analytical certificates.

Tap a colored point to scroll directly to its source card. The original 4D notes, immutable PR heads, raw HBP, checkers, CI and original companion links remain the evidence; the graph never generates new mathematical conclusions.

## Updating the atlas

The source of truth for the atlas is `certificates.json` plus `ATLAS-INDEX.hbp`. Run `python3 -I -B -X utf8 tests/test_ym4_certificate_atlas.py` after editing. The test enforces unique IDs, dependency consistency, immutable external sources, 12 selectable SVG panels, count consistency, visible OPEN nodes, reciprocal finite link, and fail-closed scope rules. The workflow produces a byte-identical HBP receipt and checks optimized replay.

To add evidence, preserve prior pinned records, add a dated node, update the linked proof obligations and statuses, and keep a distinct machine or theorem acceptance gate. If an external paper addresses an OPEN node, mark **CANDIDATE** until its mathematical object and proof checker are compatible. The known 4D continuum existence and full physical mass gap remain **OPEN**.

### Expanded external certificate audit (November 21)

**22 attributed external candidate nodes**, including the originally identified conditional proofs, are source-pinned in the 3D graph. [The external match ledger](BRIDGE-LEDGER.md) ranks the Lean Wilson construction, OS reconstruction, O(N) RG reference, exact rational quaternion code, SU(2) loop identity, statement anti-vacuity and dual spectral methods. We have incorporated a clean-room **integer-only SU(2) holonomy and normalized trace-closure check**, documented in [the exact algebra certificate](EXACT-SU2-WILSON-ALGEBRA.md). The eleven red OPEN mathematical requirements are preserved.
