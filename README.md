# Four-dimensional SU(2) lattice Yang–Mills: exact finite-lattice and strong-coupling results

> **Scope.** This repository studies the four-dimensional Euclidean **SU(2) Wilson lattice gauge theory**. Its results hold on fixed finite lattices, at strong coupling, or at one lattice scale. Some are conditional implications. **The Clay Yang–Mills existence and mass-gap problem is OPEN here.** No continuum theory is constructed and no physical mass gap is proved; the repository name predates this scope statement. See [Review status](#review-status) for what has and has not been checked, and by whom.

Current status, corrections and the November 2026 external landscape: **[PROBLEM.md](PROBLEM.md)**. Prior work for every track: **[docs/REFERENCES.md](docs/REFERENCES.md)**. Full dated history and the previous README: **[CHANGELOG.md](CHANGELOG.md)**.

## Certificate atlases — live 3D viewers

**[▶ OPEN THE 4D SU(2) CERTIFICATE ATLAS — LIVE 3D VIEW](https://raw.githack.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/main/docs/certificate-atlas/index.html)** · [Alternative viewer](https://htmlpreview.github.io/?https://raw.githubusercontent.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/main/docs/certificate-atlas/index.html) · [Atlas guide](docs/certificate-atlas/README.md) · [Machine-readable inventory](docs/certificate-atlas/certificates.json) · [Proof obligation ledger](docs/certificate-atlas/BRIDGE-LEDGER.md).

![Four-panel 4D certificate atlas](docs/certificate-atlas/overview.svg)

Main inventory: **120 source-linked proof nodes, 558 evidence resources, 107 PR records, 12 camera views**, including merged VOL12-A–E. Eleven continuum obligations remain OPEN.

**[▶ OPEN THE COMPANION FINITE S₃ CERTIFICATE ATLAS](https://raw.githack.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C/main/docs/certificate-atlas/atlas-current-20261120.html)** · [Finite Yang–Mills repository](https://github.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C). The finite Wilson acceptance and 4D continuous SU(2) research are separately scoped.

**Research in review (November 24, 2026):** [spherical Wilson research atlas — pinned draft preview](https://raw.githack.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/672ce2ba84806029143368460423266ff9806568/docs/certificate-atlas/index.html) · [VOL30 spherical Fischer playback](https://raw.githack.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/672ce2ba84806029143368460423266ff9806568/docs/certificate-atlas/vol30-spherical-fischer.html) · [VOL32 exact Haar correlations](https://raw.githack.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/672ce2ba84806029143368460423266ff9806568/docs/certificate-atlas/vol32-exact-haar-correlations.html) · [VOL33 connected shell residuals](https://raw.githack.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/672ce2ba84806029143368460423266ff9806568/docs/certificate-atlas/vol33-connected-shell-residual.html) · [VOL34 independent Metropolis](https://raw.githack.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/672ce2ba84806029143368460423266ff9806568/docs/certificate-atlas/ym4-vol34-independent-metropolis.html) · [VOL35 L8/L10 comparison](https://raw.githack.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/672ce2ba84806029143368460423266ff9806568/docs/certificate-atlas/vol35-lattice-volume-comparison.html). These are separate, unmerged research views from [PR #113](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/113); the pinned draft's numerical measurements retain their exploratory status. The blocking research is staged in [VOL13 — PR #121](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/121), [VOL14-A — PR #122](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/122) and [VOL14-C — PR #123](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/123). VOL14-B supplied patches await publication. Research links are additional navigation; the main proof-node inventory retains its own source and review statuses.

## Review status

Three different kinds of review are easy to confuse. This page keeps them apart.

| Kind | What it means | Status here |
|---|---|---|
| **External human mathematical review** | A named mathematician, outside the project, reads a written proof and reports on it | **None recorded in this repository** (obligation YM4-08: OPEN). A human review that has taken place should be added here with the reviewer, the scope and the date. |
| **Independent AI verification** | Separate AI seats or sessions (for example GPT-6, Opus 5.5, Fable 5, Claude) reconstruct a derivation or rerun a checker without seeing the author's run | Done for many tracks; archived in `reviews/` and labelled "independent audit" or "seat review" in the notes. Useful internal checking, **not** human review. |
| **Formal peer review** | Refereeing by a journal or conference | **None.** |

Status labels on this page never count AI verification as acceptance.

## The model

On a periodic hypercubic lattice Λ, each positively oriented link carries $U_\ell\in SU(2)$, and

$$S_W(U;\beta)=\beta\sum_{p}\Big(1-\tfrac12\operatorname{Re}\operatorname{Tr}U_p\Big),\qquad Z_{\Lambda,\beta}=\int\prod_\ell dU_\ell\;e^{-S_W(U;\beta)},$$

with normalized Haar measure and $\beta=4/g^2$. The continuum limit needs $\beta(a)\to\infty$ as the lattice spacing $a\to0$, which is **weak coupling**. Strong coupling (small β) is where cluster and Dobrushin methods work, and it is far from the continuum. Definitions and targets: [PROBLEM.md](PROBLEM.md).

## Results

Status labels used on this page:
- **PROOF-WRITTEN:** a written derivation, not yet refereed.
- **COMPUTED:** an exact-arithmetic checker with a frozen receipt.
- **CONDITIONAL:** an implication whose hypothesis is open.
- **OPEN.**

Notes elsewhere in the repository use older labels: DERIVED, MEASURED, PASS, ACCEPTANCE and others.

| Track | Statement (short) | Regime | Status | Prior work | Note · checker |
|---|---|---|---|---|---|
| YM4-01 | Gauge covariance of plaquettes and the Wilson action | any finite lattice | PROOF-WRITTEN, COMPUTED on 2⁴ | Wilson 1974 | [Lemma 0001](docs/LEMMA-0001-GAUGE-INVARIANCE.md) · `tests/test_exact_su2_4d.py` |
| YM4-02a/b | β = 0 Haar moments; Q8, 2T, 2O, 2I match Haar through degree 3, 5, 7, 11 | finite | PROOF-WRITTEN, COMPUTED | classical designs | [Lemma 0002](docs/LEMMA-0002-HAAR-MOMENTS.md), [Lemma 0003](docs/LEMMA-0003-SUBGROUP-DESIGNS.md) |
| YM4-02c | Reflection positivity; positive transfer matrix with simple top eigenvalue; site-sign characterization | finite, β > 0 | PROOF-WRITTEN (sign theorem possibly new) | Osterwalder–Seiler 1978, Lüscher 1977 | [Lemma 0004](docs/LEMMA-0004-REFLECTION-TRANSFER.md), [sign note](docs/NOTE-YM4-02c-SITE-SIGN.md) |
| YM4-02d | λ₁/λ₀ ≤ tanh(βN_ℓ) | fixed lattice; tends to 1 with volume | PROOF-WRITTEN, COMPUTED | Birkhoff 1957, Bushell 1973 | [note](docs/NOTE-YM4-02d-QUANTITATIVE-GAP.md) |
| YM4-02e, 04B | Volume-uniform bounds for tanh β < 1/14 (transfer) and β < 1/18 (Dobrushin, 18β) | **strong coupling** | PROOF-WRITTEN, COMPUTED | Dobrushin 1968, Föllmer 1982, Seiler 1982 | [02e](docs/NOTE-YM4-02e-KSTEP-AND-LOCALITY.md), [04B](docs/NOTE-YM4-04B-LOCAL-CLUSTER-20261107.md) |
| YM4-03 | Exact gauge-equivariant one-scale decimation and Haar pushforward; 2D closure | finite | PROOF-WRITTEN, COMPUTED | Migdal 1975, Kadanoff 1976, Witten 1991 | [note](docs/NOTE-YM4-03-ONE-SCALE-BLOCKING.md) |
| **YM4-03C** | Exact rational b = 2 blocked action through β¹⁰ (χ₁ enters at β⁸, the chair at β¹⁰) | **strong coupling** | COMPUTED; Rust engine byte-reproducible | strong-coupling expansions (Drouffe–Zuber 1983) | [note](docs/NOTE-YM4-03C-BLOCKED-ACTION.md) · `reviews/fable5-ym4-03c-engine/` |
| YM4-04A | Two exact ternary blocks 18⁴ → 6⁴ → 2⁴ | strong coupling; flows toward β = 0 | COMPUTED | — | [note](docs/NOTE-YM4-04-TWO-TERNARY-BLOCKS-20261107.md) |
| YM4-05A | 2D heat-kernel semigroup; 4D one-link six-staple integral | exact controls | COMPUTED | character expansion | [note](docs/NOTE-YM4-05A-CHARACTER-WEAK-COUPLING-20261107.md) |
| YM4-07B / 07C / SW01 | Physical-unit bridge lemma; source-transfer gate; spectral-window bound | conditional | PROOF-WRITTEN. SW01 bounds the gap from **above**. 07C's S₃ input only sets a threshold. | — | [07B](docs/NOTE-YM4-07B-QUANTIFIED-CONTINUUM-BRIDGE-20261116.md), [07C](docs/NOTE-YM4-07C-WILSON-SOURCE-PROJECTION-BRIDGE-20261120.md), [SW01](docs/certificate-atlas/NOTE-SPECTRAL-WINDOW-DUAL-20261121.md) |
| WT01, WC01, WV01, WG01–WG09 | Exact one-link character transfer; C0/C2/C4 moments; centre sectors; first-excitation ordering; neutral 42-band | **spatial L = 2**, mostly 0 < β ≤ 1/100 | COMPUTED | 't Hooft flux sectors (1979) | [WT01](docs/NOTE-YM4-SU2-WILSON-LOCAL-TRANSFER-20261121.md), [WG03](docs/NOTE-YM4-WG03-FIRST-SU2-CENTER-CHARGED-ENERGY-ORDER-20261121.md), [WG09](docs/NOTE-YM4-WG09-FINITE-BETA-ORDER-CERT-20261121.md) and the other `docs/NOTE-YM4-W*` notes |
| VOL01–VOL05 | Selection rules; cube Haar integral 1/16; fourth-order Schur coefficient | strong coupling, L ≥ 3 | PROOF-WRITTEN, COMPUTED | character expansion | [VOL03](docs/certificate-atlas/NOTE-YM4-VOL03-CUBE-HAAR-NAVIER-CERTIFICATE-20261122.md), [VOL04](docs/certificate-atlas/NOTE-YM4-VOL04-COMPLETE-FOURTH-SCHUR-20261122.md) and the other VOL0x notes |
| VOL06 | Λ₁/Λ₀ ≤ 18β for β < 1/18, uniformly in spatial volume | **strong coupling** | PROOF-WRITTEN (classical theorem, explicit constant) | Osterwalder–Seiler 1978 | [note](docs/certificate-atlas/NOTE-YM4-VOL06-FULL-PHYSICAL-STRONG-COUPLING-GAP-20261122.md) |
| VOL07 | A uniform block covariance rate implies a uniform transfer gap | — | CONDITIONAL; the hypothesis is the open mass-gap rate (MG) | standard clustering ⇔ gap | [note](docs/certificate-atlas/NOTE-YM4-VOL07-PHYSICAL-BLOCK-GAP-CRITERION-20261122.md) |
| VOL08–VOL11 | Plaquette deficit ≤ R(β) = 1/β + (4/(3β)) log(1536 β^{3/2}) uniformly in volume; good- and bad-star bounds; factorization on plaquette-disjoint links | **weak coupling, one lattice scale** | PROOF-WRITTEN, COMPUTED arithmetic; joint bad-island bound OPEN | Bałaban (large fields), Chatterjee 2016 | [VOL09](docs/certificate-atlas/NOTE-YM4-VOL09-PERIODIC-GOOD-STAR-FREQUENCY-20261122.md), [VOL11](docs/certificate-atlas/NOTE-YM4-VOL11-SEPARATED-DEFECTS-20261122.md) |
| **VOL12** | Unconditional bounds for **every** set: μ(S ⊆ bad stars) ≤ ρ⋆^\|S\|, with ρ⋆ = 6·1536·e^{3/4}β^{3/2}e^{−βε/64}; island tail ≤ 72^{m−1}ρ⋆^m; ρ⋆ ≤ 18⁻³ gives 18^{−m−2} | **weak coupling, one lattice scale; even L ≥ 4** | PROOF-WRITTEN (AI-written, awaiting human review), COMPUTED geometry and fixtures | chessboard estimates (Fröhlich–Lieb 1978; Fröhlich–Israel–Lieb–Simon 1978) | [note](docs/certificate-atlas/NOTE-YM4-VOL12-CHESSBOARD-BAD-STAR-CLUSTERS-20261124.md) · `tests/ym4_su2_vol12_chessboard_clusters.py` |
| YM4-06A | S₃ flat sectors on the 3-torus (21 orbits); lock cost min(8, 3L_min) | finite group, structure only | PROOF-WRITTEN, COMPUTED | Burnside counting | [note](docs/NOTE-YM4-06A-GLOBAL-LOCK-20261110.md) |
| YM4-05B | Cantor-27 surrogate update | **not Yang–Mills** | computational experiment only | — | [note](docs/NOTE-YM4-05B-CANTOR27-20261107.md) |
| YM4-04 … 08 | Uniform multiscale control as β(a) → ∞; continuum limit and OS reconstruction; physical mass gap; all compact simple groups; external audit | — | **OPEN** | Bałaban 1984–89; Magnen–Rivasseau–Sénéor 1993 | [obligation ledger](docs/PROOF_OBLIGATIONS.md) |

**Where the real difficulty is.** Every volume-uniform estimate above, VOL12 included, holds either at strong coupling or at a single lattice scale. A physical mass gap needs control across the roughly β-many scales between the lattice spacing and the confinement length. That is the open uniform clustering rate (MG), which is also the hypothesis of VOL07.

## Reproduce

```bash
bash scripts/run_all_tests.sh                       # every tests/test_*.py, plus every VOL checker against its receipt
python3 -I -B scripts/no_float_gate.py .            # integer-only static gate
python3 -I -B scripts/check_docs_integrity.py       # Markdown control characters and relative links
python3 -B tests/test_exact_su2_4d.py               # one check, about 0.1 s
```

On two cores the full run took about 14 minutes (39 runs, 24 November 2026); `test_k_step_locality.py` alone takes about 6–10 minutes. CI runs the same suite unfiltered on every push to `main` and nightly (`.github/workflows/ym4-run-all-nightly.yml`). The other workflows are path-filtered per track.

## Repository map

| Path | Contents |
|---|---|
| [PROBLEM.md](PROBLEM.md) | Model, the three targets, current status and corrections |
| [docs/](docs/) | Lemmas 0001–0004 and the YM4-* notes |
| [docs/certificate-atlas/](docs/certificate-atlas/) | VOL notes, frozen `.hbp` receipts, the bridge ledger and the proof-node atlas |
| [docs/PROOF_OBLIGATIONS.md](docs/PROOF_OBLIGATIONS.md) | Ledger of the remaining obligations |
| [docs/REFERENCES.md](docs/REFERENCES.md) | Prior work by track |
| `tests/`, `scripts/` | Exact-arithmetic checkers, the no-float gate and the run-all script |
| `reviews/` | Archived AI-seat reviews and replays (internal checks, not refereeing) |
| [CHANGELOG.md](CHANGELOG.md) | Dated history and the previous README |

**Related.** A companion repository studies finite S₃ gauge Hamiltonians in 2+1 dimensions. S₃ is not a subgroup of SU(2), so its results are a separate model and are not inputs to the SU(2) estimates here.
