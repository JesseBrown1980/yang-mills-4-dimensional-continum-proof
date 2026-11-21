# External certificate search — November 21, 2026 (second independent round)

This second search extends the [original 4D OPEN-gate ledger](BRIDGE-LEDGER.md). New sources remain **attributed CANDIDATES**, with their theorem scope checked against their original repository files or published articles. A compatible word or numerical graph is not sufficient to import a continuum Yang–Mills certificate.

## Nine source-matched candidates and concrete acceptance tests

| Atlas node | Verified original artifact | Best OPEN match | Certificate use and proof boundary |
|---|---|---|---|
| **EXT-LGT-DOB** | [Douglas–Rajasekaran, Lean strong-coupling gauge 2-point decay](https://github.com/mrdouglasny/lgt/blob/b8793ccf6a51e00e9e2b1685ba191b8626e37137/LGT/MassGap/StrongCoupling.lean) | YM4-Q07 | Lean statement for periodic lattice **U(n)** plaquette connected correlations at \(0<\beta<1/[32n(d-1)]\). At \(n=2,d=4\), window \(\beta<1/192\). The source reports only standard Lean axioms. SU(2) use needs a conforming `HasGaugeTrace` instance; physical full-Hamiltonian gap, \(\beta=64\) and continuum UV limit remain separate. |
| **EXT-LGT-RG** | [Same project, abstract RG scale-transfer](https://github.com/mrdouglasny/lgt/blob/b8793ccf6a51e00e9e2b1685ba191b8626e37137/LGT/Bridge/ScaleTransfer.lean) | YM4-Q08 | Abstract covariance/distance-compression transfer lemmas are useful; the source explicitly marks concrete RGBlockingData and blocking specifics incomplete. Require actual 4D gauge-covariant block source and uniform physical-unit rate before adoption. |
| **EXT-ERIKSSON-AREA** | [Eriksson, Lean volume-uniform exact Wilson activity area law](https://github.com/lluiseriksson/THE-ERIKSSON-PROGRAMME/blob/357ef54cc7fc3f2190fab7d2daa7357ded7a2edf/YangMills/L1_GibbsMeasure/RestrictedGate.lean) | YM4-Q07 | The `normalized_exp_wilson_loop_area_law` source is relevant to **volume-free finite strong-coupling** Wilson checks and polymer-gas machinery. Area-law bounds do **not** establish the lowest physical excitation or UV continuum gap. Project is AGPL-3.0; link rather than copying modules without license compliance. |
| **EXT-FUSION-6J** | [fusion-symbols, exact Rust SU(2) Wigner/CG/F-symbols](https://github.com/Ryo-wtnb11/fusion-symbols/blob/f56244fe1bcf6038043a2afa695ea3afb7ea072e/src/lie/su2.rs) | YM4-Q02 / Q01 | Exact signed-square-root-of-rational coefficient representation, doubled-integer spin labels, cached SU(2) recoupling; directly useful for character-sparse gauge-invariant basis building. Need exact vertex/edge orientation and phase normalization, tensor-network contraction and independent Racah-identity checks. MIT/Apache-2.0 options. |
| **EXT-LIBWIGNER** | [libwignernj exact intermediate Racah sums](https://github.com/susilehtola/libwignernj/blob/529ab42bdb31a34bb2bfa0a77a36f2a3a646202e/README.md) | YM4-Q02 | Independent Wigner 3j/6j/9j comparator, prime-factorized integer intermediates and arbitrary-precision output. The public API converts to floating-point at output: use only as an independent *exploratory cross-check* until a lossless certificate representation is obtained. |
| **EXT-CAUSAL-DUAL** | [Causal bootstrap, Phys. Rev. D 114, 074510 (2026)](https://doi.org/10.1103/m9kj-y6t3) | YM4-Q05 / Q04 | Published dual positive-kernel bounds from finite Euclidean spectral data. Provides mathematical architecture for finite polynomial/rational minors; requires explicit Wilson spectral measure, exact dual feasibility, interval-error budgets and **excited-state isolation**. We independently implemented a simple exact dual polynomial in [YM4-SW01](NOTE-SPECTRAL-WINDOW-DUAL-20261121.md); that is not a claimed reimplementation of the paper. |
| **EXT-KERNEL-TRANS** | [Kernel transformations and bounds for smeared spectral functions, Phys. Rev. D 114, 094510 (20 Nov 2026)](https://doi.org/10.1103/f4h2-pg8m) | YM4-Q05 | Target-smearing conversion between Euclidean/spectral kernels. Independent pointwise rational/interval dual inequality and normalization are required; today's discovery is a *method lead*, not an imported spectral certificate. |
| **EXT-U1-LEAN** | [Tomar, Lean 4 area-law formalization, Zenodo 23480809 (2026)](https://doi.org/10.5281/zenodo.23480809) | YM4-Q08 | Fully formal numerical-constant/area-law interface for **three-dimensional U(1)** Wilson theory across couplings. Useful as a proof engineering template for uniform estimates, but neither non-Abelian SU(2) nor the four-dimensional Wightman construction follows. |
| **EXT-LOCAL-QHAM** | [Scalet, certified equilibrium-state algorithms, Nat. Commun. 15 (2024)](https://doi.org/10.1038/s41467-024-51592-3) | YM4-Q06 | Certified local-Hamiltonian observable bounds and convex feasibility approach. Transfer via proof only after showing the original gauge-projected transfer/physical Hamiltonian meets the relevant locality, stability, thermodynamic and temperature hypotheses. Not an existing YM spectral gap certificate. |

## A new exact spectral-window certificate directly addressing Q05

We derived and froze [YM4-SW01](NOTE-SPECTRAL-WINDOW-DUAL-20261121.md), a **positive-measure dual minorant** for the *physical connected Wilson correlator*. Let
\(S=T_{\rm phys}/\lambda_0\), \(u=(W-\langle W\rangle)\Omega\), \(C_n=\langle u,S^nu\rangle\), and \(0<q<1\). The spectral measure \(\nu\) of \(u\) is positive on \([0,1]\). For \(n\ge1\),

\[
\nu((q,1])\ge\max\left(0,\frac{\underline C_n-q^n\overline C_0}{1-q^n}\right).
\]

The **exact integer-only polynomial witness** is \(p(t)=(t^n-q^n)/(1-q^n)\le 1_{(q,1]}(t)\). Its source values must be actual certified Wilson connected moments, with rigorous input intervals. It supplies **total low-energy spectral weight**, *not* the first eigenstate weight unless an independent spectrum-isolation certificate proves only one Wilson-coupled level in the window.

A deterministic rational toy fixture produces **HOLD at n=2, PASS at n=4**, with exact lower \(103/16384\) and robust interval lower \(53879/10240000\) when \(C_0,C_4\) have independent \(1/1000\) error envelopes. The fixture is not an original 4D measurement; its role is to certify the checker and prevent accidental first-weight promotion.

## Decision: what to reuse first

**Priority A:** exact SU(2) Wigner 6j/CG recoupling via fusion-symbols as a vetted algorithmic *coefficient provider*, tested against the independently proven quaternion/Wilson identities already in the atlas. This is immediately actionable for the sparse character evaluator, especially vertex singlet conditions.

**Priority B:** a physical Wilson spectral dual producer. Calculate actual \(C_0,C_2,C_4\) with strict intervals for a tractable original 4D SU(2) physical lattice; feed them to YM4-SW01 and only afterwards attempt a first-level isolation/weight certificate.

**Priority C:** cross-check strong-coupling and volume-uniform Wilson estimates against Douglas–Rajasekaran and Eriksson Lean theorems. Scope remains their certified strong-coupling range; no weak-\(\beta\to\infty\) conclusion.

**Priority D:** formal weak/UV and reconstruction source comparisons, including the 3D U(1) Lean engineering pattern and the already documented October Wilson construction. A 4D continuum certificate still requires the actual nontrivial physical reconstruction and uniform physical-energy bounds.

## Rejected shortcuts

Several other 2026 online claims describe a full Yang–Mills strong- or weak-coupling gap. I did not upgrade any claim without source-level checks on its action, physical sector, proof objects, uniformity and original source observable. In particular, numeric SDP solver output, 2D CFT certificates, 3D U(1) area laws and Gaussian free-field OS facts are distinct mathematical targets.

**Status:** finite/strong-coupling/formal and numerical-method certificates discovered; exact spectral-window algebra DERIVED with a checker; original 4D interacting Wilson spectral moment values and isolated first physical Wilson weight remain OPEN; 4D continuum mass gap remains OPEN.
