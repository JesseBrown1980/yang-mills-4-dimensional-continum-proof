# Four-dimensional Yang–Mills Certificate Atlas

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
