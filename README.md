# Yang–Mills Four-Dimensional Continuum Proof

**Status: OPEN.** This repository works toward a rigorous four-dimensional pure Yang–Mills quantum field theory with a strictly positive *physical* mass gap. The first gauge group is **continuous SU(2)**, represented in small exact tests by rational unit quaternions. The official Clay problem covers every compact simple gauge group and asks for **both** a nontrivial quantum theory on four-dimensional spacetime **and** a mass gap.

**Official target:** [Clay Mathematics Institute — Yang–Mills and the Mass Gap](https://www.claymath.org/millennium/yang-mills-the-maths-gap/) and [Jaffe and Witten's problem description](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf).

## Where we stand, November 3, 2026

| Step | State | Where |
|---|---|---|
| YM4-00, the model | Defined | [PROBLEM.md](PROBLEM.md) |
| YM4-01, gauge covariance | Proved, with an exact test on the 2⁴ lattice. Independent review OPEN | [Lemma 0001](docs/LEMMA-0001-GAUGE-INVARIANCE.md) |
| YM4-02, finite Wilson measure, reflection positivity, transfer matrix | Partition function proved by compactness, and β = 0 moments derived, with their link geometry exact-tested and Haar orthogonality as input. YM4-02c, DERIVED at each fixed finite lattice and β, with exact controls MEASURED, attacked and rechecked by a second seat: exp(−βN_p) ≤ Z ≤ 1; site reflection positivity for every real β, with the sharp condition on the product of the weights over the fixed plaquettes; link reflection positivity for β ≥ 0, each for every F on the half; on an odd side at T ≥ 4, with 1/w bounded and c₀ ≠ 0, the form is PSD exactly when every c_ρ c₀ ≥ 0; T = A^(1/2) B A^(1/2) positive and trace class, Z = Tr(T^N_t P), top eigenvalue simple with a positive gauge-invariant eigenfunction. Lüscher (1977) matched against preprint DESY 76/54, Knowles' thesis matched including Z = Tr(P T^N), Jaffe–Janssens matched through its (V.5). Osterwalder–Seiler (1978) NAMED, body CANNOT_SEE. On an odd side at T ≥ 4, a weight with a zero goes either way. GPT-6 and the operator hold the PR as a draft. Uniformity in L and β, λ₁, a quantitative gap and review of this head by a different model family OPEN | [Lemma 0004](docs/LEMMA-0004-REFLECTION-TRANSFER.md), [Lemma 0002](docs/LEMMA-0002-HAAR-MOMENTS.md), [second seat](reviews/opus55-ym4-02c/README.md), [its recheck](reviews/opus55-ym4-02c/recheck/README.md), [GPT-6](reviews/gpt6-ym4-02c/README.md), [issue #2](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/2) |
| YM4-02b, finite subgroups of SU(2) against Haar | Q8, 2T, 2O and 2I average exactly as Haar through degree 3, 5, 7 and 11 per link, MEASURED from groups built here. So on a lattice whose plaquettes each hold four distinct links, a polynomial observable of degree at most t in each link agrees with SU(2), DERIVED, and the plaquette series matches the published table through β⁹, with 4 cubes and 36 ten-face surfaces per site. Side-1 limits are stated: both sides of a plane of length 1 gives floor(t/2), on periodic 1×L in two dimensions, L ≥ 2, agreement through t is DERIVED and checked independently by GPT-6, with exact controls on all four groups and a closed form for the Haar moments, and exactly one side of 1 in d ≥ 3 is measured through t on the lattices and groups the lemma lists. A second seat attacked and confirmed it, with [its files here](reviews/opus55-ym4-02b/README.md), and GPT-6 reported no mathematical blocker in the last two commits it read. A claim that agreement through t holds exactly when no plane has both sides 1 is CONJECTURE in the lemma, with two derivations and a falsifier. The remainder at β > 0 and a uniform bridge at large β are OPEN | [Lemma 0003](docs/LEMMA-0003-SUBGROUP-DESIGNS.md), [PR #11](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/11), [PR #13](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/13) |
| YM4-03, one-scale blocking | OPEN | [Issue #3](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/3) |
| YM4-04, uniform estimates across all scales | OPEN, the central bottleneck | [Issue #4](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/4) |
| YM4-05, continuum limits and Osterwalder–Schrader reconstruction | OPEN | [Issue #5](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/5) |
| YM4-06, the physical mass gap | OPEN | [Issue #6](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/6) |
| YM4-07, every compact simple group | OPEN | [The ledger](docs/PROOF_OBLIGATIONS.md) |
| YM4-08, independent audit of the whole chain | OPEN | [The ledger](docs/PROOF_OBLIGATIONS.md) |
| YM4-QNN-01, a harness for candidate generators | Draft, held on the seat's recommendation, which the operator agreed with on November 3. Its next gate is a pinned QNN adapter. It holds exact SU(2) arithmetic, receipts and four-shard CI, with synthetic input | [PR #9](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/9), [issue #8](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/8) |

[The ledger](docs/PROOF_OBLIGATIONS.md) says what rows YM4-00 to YM4-08 need before they can move. The computations here use integers only. On every pull request [a gate](scripts/no_float_gate.py) reads every tracked file and fails on what it finds outside [its list](scripts/FLOAT-EVIDENCE.txt), where each row holds a count, a hash pin and a reason: [`no_float.yml`](.github/workflows/no_float.yml) runs the change's own copy as `no-float`, the check `main` requires, [`no_float_base.yml`](.github/workflows/no_float_base.yml) runs the base commit's copy over the change as data, and [`no-float-compiled.yml`](.github/workflows/no-float-compiled.yml) reads what g++ and rustc produce from the C++ and Rust files.

**Its limits, in plain words.** A pass is evidence and no proof of integer-only execution: it means these checks found nothing in what they read. Written rules reached 6 of 20 on plants written afterwards, so the next plant may pass. The gate reads each file's source alone, with no types, values or view across files, and child processes, code written at run time, data files, third-party code and shell lines stay outside its reading. A float added in the same change as its own pinned row passes both scans, and only the job `no-float-list-unchanged` flags it for a person to read. The gate's docstring states its whole scope.

## The finite-lattice programs

The [Yang–Mills / HEB-C repository](https://github.com/JesseBrown1980/Finite-universe-Yang-mills-existence-and-mass-gap-using-HEB-C) develops finite S₃ lattice spectra, exact checks, 3×4 store-based certificates and a two-dimensional quantum-double stability track. The companion [SU(N) repository](https://github.com/JesseBrown1980/Finite-Universe-SU-N-solved) studies Q8, 2T, 2O, 2I and other finite models. Those results hold for finite groups in two spatial dimensions. Carrying any of them to continuous SU(2) in four dimensions needs its own proved argument.

This repository starts from a **four-dimensional Euclidean SU(2) Wilson lattice** and a ledger of every remaining mathematical step.

## First executable lemmas

The first control uses the periodic lattice `(Z/2Z)^4`, with 16 sites, 64 positively directed links and 96 oriented plaquettes. It represents SU(2) matrices by exact rational unit quaternions, including noncommuting elements. It checks gauge covariance and invariance of all Wilson plaquette traces and the Wilson action, with two deliberately failing controls.

```bash
python3 -I tests/test_exact_su2_4d.py
```

Expected receipt:

```text
EXACT_SU2_4D|sites=16|links=64|plaquettes=96|seeds=4|gauge_covariance=PASS|wilson_action=PASS|fault_controls=2/2|failures=0|json=0
EXACT_SU2_4D_VALUE|seed=20261103|S_W=449929987986/3508004825|json=0
EXACT_SU2_4D_VALUE|seed=1729|S_W=193195378719/1349232625|json=0
EXACT_SU2_4D_VALUE|seed=314159|S_W=185342826929127/1490902050625|json=0
EXACT_SU2_4D_VALUE|seed=271828|S_W=2969866827969/22936954625|json=0
EXACT_SU2_4D_CHECKER|one_link_fixture_S_W=18/5|wrong_plaquettes_detected=384/384|kept_the_trace=372|json=0
SCOPE|finite_periodic_lattice_only=1|continuum_existence=OPEN|physical_mass_gap=OPEN|json=0
```

This exact check is a **standard finite-lattice algebraic fact**, and its scope is that one lattice. The second, `python3 -I tests/test_haar_moments_4d.py`, checks the link geometry behind the first two plaquette cumulants at β = 0, with Haar orthogonality as input. Read [PROBLEM.md](PROBLEM.md), [the ledger](docs/PROOF_OBLIGATIONS.md), [Lemma 0001](docs/LEMMA-0001-GAUGE-INVARIANCE.md) and [Lemma 0002](docs/LEMMA-0002-HAAR-MOMENTS.md) for the proofs and their scope.

## Research program

The required chain is **Euclidean Wilson lattice SU(2) → gauge-covariant multiscale renormalization → uniform nonperturbative scale estimates → infinite-volume and zero-spacing limits → nontrivial Schwinger functions with OS axioms → Hilbert-space reconstruction → strictly positive physical spectral gap**.

Each arrow requires its own proof and independently reproducible evidence. A gap in lattice units or at finite volume is a statement at that cutoff and volume. Carrying one to a physical gap is YM4-06, which is OPEN. The ledger marks PROVED, EXACT-TEST, DERIVED, DERIVED-CONDITIONAL, CONJECTURE, OPEN, FAILED, INCONCLUSIVE and RETRACTED claims, and failed tests stay visible with their receipts.

Reference: Osterwalder and Seiler, *Gauge field theories on a lattice*, Annals of Physics 110 (1978), 440–471, [DOI:10.1016/0003-4916(78)90039-8](https://doi.org/10.1016/0003-4916(78)90039-8).
