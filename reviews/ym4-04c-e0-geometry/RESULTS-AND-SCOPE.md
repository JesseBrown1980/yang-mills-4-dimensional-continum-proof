# YM4-04C E0 — independent 4D b=2 geometry and four-plaquette polymer census

**2026-11-11. Scope: E0/C01 geometry and exact n=4 closed-polymer controls only.** The full YM4-04C engine, the refined C03 count through n=12, and weak-coupling control remain OPEN.

## Frozen inputs and release provenance

The unchanged first 42 rows of \`docs/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp\` retain the SHA256 digest
\`c74e6388295a6309674268dd18deba3728a4eb627a1530c42054182b2fadc404\`, from freeze commit \`6ebf63272ae230bfb08ef48b3156cb4202c24627\`. The branch is stacked on the C04 staged-engine draft PR #58 and, through it, the independently filed G-attack PR #46. It neither rewrites the freeze nor silently promotes the still separate evidence-list PR #45.

These E0 geometry and n=4 results have \`prefreeze=CROSS_READ\` because their values were already derived in the freeze and reviewed by the second seat. The current run is a reproduction with independent source routes, *not* a blind prediction.

## 4D b=2 definition used by both checkers

On the oriented positive links \((x,\mu)\) of the fine periodic \((\mathbb Z/N\mathbb Z)^4\), \(N\in\{8,10\}\), let

\[
 c(x,\mu)=|\{\nu\ne\mu:x_\nu \equiv1\pmod2\}|.
\]

A line link has \(c=0\); off-link classes have \(c=1,2,3\). For every positive oriented face \((x;\mu,\nu)\) with \(\mu<\nu\) construct its four distinct positive links and its off-link support. Two faces are adjacent when they share an off link. A closed polymer is a connected face set for which every off link appearing in its support has multiplicity at least two.

The Python route constructs all positive faces and indexed off-link incidence; finds face neighborhoods by union of co-incidences; and enumerates all connected, deduplicated sets of four faces containing a selected off link. It then checks closure by off-link multiplicity.

The native Rust 1.81 checker uses independently written indexed incidence and ordered-set augmentation for the same complete finite domain. It does not read the Python result to compute its own counts.

## Full-geometry census, with matching independent checks

| Exact observable | N=8 | N=10 |
|---|---:|---:|
| Sites | 4,096 | 10,000 |
| Positive links | 16,384 | 40,000 |
| Positive 4D plaquettes | 24,576 | 60,000 |
| Line links | 2,048 | 5,000 |
| Off-link classes c=1,2,3 | 6,144; 6,144; 2,048 | 15,000; 15,000; 5,000 |
| Faces with two off links | 6,144 | 15,000 |
| Faces with four off links | 18,432 | 45,000 |
| Off-link face-adjacency degrees | 10 and 20 | 10 and 20 |
| Other off links in six faces through the selected line link | 12 | 12 |
| Distinct off links at its midpoint | 6 | 6 |
| Closed connected four-face polymers holding a class-1,2,3 off link | **1,0,0** | **1,0,0** |

In the enumeration, the candidate connected four-face sets for a selected class-1, class-2 and class-3 off link were respectively 35,478; 47,232; and 52,200. Both implementations independently recovered one closed set only for class 1.

The exact degree identity is \(\deg_{\mathrm{off}}(p)=5\,\#\mathrm{off}(p)\). Because every face has two or four off links, its neighborhood degree is 10 or 20; the maximum degree \(D=20\) is the combinatorial input to YM4-04C's frozen Fuss–Catalan tail. This is a **local degree**, not the total lattice size.

## Reproducibility and deliberate failures

A hosted workflow checks the original frozen HBP pin, strict no-float source gate, native Rust 1.81 strict Clippy, independent Rust unit tests, and full Python/Rust agreement. Deliberate false controls reject (1) a fabricated degree-19 face, (2) a corrupted quarter-face count, and (3) the false assertion of a closed n=4 polymer in class 2.

Canonical source-generated receipts are in \`evidence/YM4_04C-E0-PY.hbp\`, \`evidence/YM4_04C-E0-RUST.hbp\`, and \`evidence/YM4_04C-E0-SHA256SUMS\`. The final-head workflow checks each file's SHA256 and compares all three against freshly rebuilt bytes. The checksum is an integrity commitment and not a physical Yang–Mills observable.

## Explicit open items

This does **not** enumerate the refined C03 closed-polymer coefficients through \(n=12\). The more difficult E1 closure-driven enumeration with verified canonical reductions is the next computational gate. E2 enclosure, E3 KP boundary search, G0/G1 all-\(k\) contraction, gauge-link integrals, W-lane diagnostics, the full independent Rust checker, twelve-stage sabotage matrix, and twice-clean complete receipt remain separate unfinished deliverables. The YM4-04C currently established strong-coupling norm controls neither provide a weak-coupling trajectory nor solve the continuum Clay problem.

PR #58's inherited \`no-float-list-unchanged\` fail remains an explicit human-review hold and must not be bypassed to merge this stack. No r=9 launch or unrelated GitRAM workload is made by this E0 workflow.
