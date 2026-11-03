# YM4-QNN-01: QNN × HEB-C HTTP0 × GitRAM bridge

**Status: DESIGN / INTEGRATION — not a four-dimensional continuum existence or mass-gap theorem.**
Related issue: [YM4-QNN-01](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/8). All upstream refs below are pinned at the time of this initial design.

## Exact source contracts

| Role | Source and frozen commit | Reuse |
|---|---|---|
| Qutrit QNN physics/variational trials | [GGUF trained quantum neural models](https://github.com/JesseBrown1980/GGUF-files-operating-as-trained-quantum-neural-network-models/tree/44946f21b2d63cc1943ce92c3d98435da2ac0efc) at `44946f21b2d63cc1943ce92c3d98435da2ac0efc` | Candidate states, rational/integer arithmetic, honest PASS/FAIL records; currently Z3 finite groups, not continuous SU(2) |
| Nested ternary proposals | [Neural network inside a neural network](https://github.com/JesseBrown1980/Neural-network-inside-a-neural-network-using-trits-to-resolve-Finiteness/tree/8cbca4356121f3bb3fb14fd927b6719cb35eb4ae) at `8cbca4356121f3bb3fb14fd927b6719cb35eb4ae` | Deterministic candidate/source generator, not a physical quantum-field model by itself |
| Mixed GGUF / trit transport | [Mixed-GGUFs](https://github.com/JesseBrown1980/Mixed-GGUFs-as-the-neural-networks-using-asolaria-star-and-mythos-and-kimi/tree/06951ae9f059f6d6eb039a97fdc995cf35668ea6) at `06951ae9f059f6d6eb039a97fdc995cf35668ea6` | Named 27-channel upstream interface; use actual pinned weight bytes before claiming real GGUF inference |
| HEB-C native receipt implementation | [HEB-C HTTP0](https://github.com/JesseBrown1980/qoled-internet-HEB-C-revisted-HTTP---free-0-hbi-hbp-sha-sh-hash/tree/1ac7f00e744c08aa7f95c2a1df89af2abd579e19) at `1ac7f00e744c08aa7f95c2a1df89af2abd579e19` | SHA-256 hashes, HBP/HBI records, native receipt verification, source-address catalog |
| Stateless compute | [GitRAM](https://github.com/JesseBrown1980/GitRAM/tree/e01425204b58dc680d1f3106410ff9ce71260b0d) at `e01425204b58dc680d1f3106410ff9ce71260b0d` | Matrix shards, immutable artifacts, all-or-nothing fan-in and sealed results |

These repository source commits are **source-identification pins**, not automatic evidence of matching data weights. A GGUF file requires its exact revision, byte size, actual bytes, loader, and SHA-256 digest. An address/hash alone cannot regenerate missing weights.

## Binding implementation constraints

**Compute/evidence hot path:**
- Rust **1.81.0**, pinned toolchain; `cargo fmt --all -- --check`; `cargo clippy --all-targets -- -D warnings`; `cargo test --all-targets`.
- Exact integer/rational, finite-field and algebraic-number arithmetic only, with **zero f32/f64** and no unbounded silent overflow.
- **Zero native JSON serialization; zero Node/V8 in the authored compute and verification code**. Every HBP/HBI record ends `json=0`. GitHub Actions checkout/artifact wrappers and GitHub's hosting API may internally use JavaScript and JSON; those external platform internals are not the native computation.
- `#![forbid(unsafe_code)]`; cryptographic digest and provenance checks fail closed on missing, duplicate, tampered, stale or mismatched shard artifacts.
- Use `HBP` for rows, `HBI` for byte offsets and lengths, `SHA` for SHA-256 over exact original bytes, `SH` for a short locator that **does not replace** SHA-256, and `HASH` for chained records. Pin the ultimate digest outside the bundle; a self-signed/unkeyed anchor verifies consistency, not who authored it.
- No live HTTP0 server required for CI, and no physical Host8 300GB volume required for a bounded fixture. HTTP0 is a **registry/address interface**, not a physics proof engine.

## First limited scientific contract

**Start with four-dimensional finite Euclidean SU(2), not Z3 substitutes.** Each of the 64 positive links on `(Z/2Z)^4` gets a signed trit `−1,0,+1` proposed by a synthetic deterministic source. Map each trit **by a documented exact rational embedding** to a unit quaternion in continuous `SU(2)`, allowing noncommuting links. Check all 96 plaquettes and their trace invariance under arbitrary independent site gauges. This is a **finite-lattice gauge-covariance regression**, not a sampled Haar integral, a transfer-matrix bound, or a continuum theorem.

The `QNN_CANDIDATE` input record must identify `kind=SYNTHETIC_CONTROL` or `kind=REAL_QNN`. `REAL_QNN` is rejected until a pinned GGUF loader and verified model weights are actually present. Otherwise the bridge is a **test of the adapter**, not evidence that a QNN has learned Yang–Mills physics.

Minimum evidence per shard:
```text
QNN_CANDIDATE|kind=SYNTHETIC_CONTROL|model_sha256=NONE|source_commit=...|trits64=<64 balanced trits>|json=0
YM4_SHARD|lattice=2x2x2x2|group=SU2_RATIONAL|plaquettes=96|gauge_covariance=PASS|trace=PASS|source_sha256=<digest>|candidate_sha256=<digest>|scope=FINITE_CHECK_ONLY|json=0
HBI|record_offset=<integer>|record_len=<integer>|hbp_sha256=<digest>|sh=<short-locator>|json=0
HASH|prev_hash=<digest>|record_sha256=<digest>|chain_hash=<digest>|json=0
```

The native verifier independently recomputes file digests and checks exact line encoding, expected shard IDs, complete shard count and all source refs. A missing/mismatched byte is a hard FAIL.

**Next physics step:** real QNN outputs may parameterize a gauge-projected variational trial state or a learned effective action, with exact arithmetic and independently checked constraints. Its variational energy can yield an **upper bound** for an operator's lowest energy when the Hilbert space, Hamiltonian and normalization are correct. It does **not** by itself establish a positive gap lower bound or continuum existence.

## GitRAM execution and benchmark

Use 4 independent shards first, then scale to 27 only after the 4-shard integrity and resource baseline passes. No inter-cell shared state. Every shard compiles its source from pinned commit and writes artifacts, a checksum manifest and a scoped PASS/FAIL. Fan-in checks **all expected shards**, rejects any missing/duplicate ID, verifies SHA-256 and chained rows, then seals one result; it never silently redoes shard training.

Benchmark an **identical deterministic workload** (same inputs, source, verifier) in two modes: single-runner sequential baseline versus GitRAM shards. Record **wall time, total CPU time, peak RAM, artifact bytes, runner minutes, and validated-bound quality**. The gain in wall time may cost more aggregate compute and storage. A plain HBP/HBI format and short SH locator reduce some serialization overhead but do not themselves guarantee memory compression or a mathematical speedup. Any saving must be measured.

## Verification gates

1. **Design/pins**: pinned upstream source commits and full GGUF bytes or explicitly synthetic input.
2. **Engine**: Rust 1.81/Clippy, integer-only, fail-closed encoding/checksums.
3. **Geometry**: exact 4D SU(2) finite-lattice gauge covariance with corruption controls.
4. **Parallel transport**: 4/4 independent GitRAM cells plus authenticated integrity of inputs and a complete fan-in.
5. **Measured comparison**: precise baseline versus GitRAM performance and negative controls.
6. **Mathematics**: any claimed nonperturbative bound must have an independent analytic/interval certificate. Physical 4D mass gap and existence stay **OPEN**.

Reference finite SU(2) work: [the four-dimensional continuum repository's issue #2](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/2), [#3](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/3), and [#4](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/issues/4).


## Executable v0 and first hosted comparison — November 3, 2026

The source and workflow are now implemented on draft PR #9, not merged:

- src/physics.rs: deterministic 64-slot balanced-trit candidate, exact rational SU(2) unit quaternions, 4D periodic lattice with 16 sites, 64 positive links and 96 plaquettes, exact Wilson-action sum, and local gauge-covariance checks including two negative controls.
- src/receipts.rs: SHA-256, HBP/HBI, 16-hex SH locators, HASH chains, source-commit pinning, exact regeneration on verification, strict shard file counts, and an all-or-nothing four-shard fan-in.
- src/sha256.rs: integer-only SHA-256 reused from the pinned HEB-C HTTP0 implementation, with known-answer tests.
- src/main.rs: single-shard computation, four-shard verification and sequential baseline.
- .github/workflows/ym4-gitram.yml: pinned Rust 1.81.0, Clippy -D warnings, formatting, unit and corruption tests, four independent GitRAM cells, sequential baseline, sealed fan-in and OS-level time/RSS measurements. The final seal requires the prerequisite jobs to succeed.

Commands: run cargo +1.81.0 fmt --all -- --check; cargo +1.81.0 clippy --locked --all-targets -- -D warnings; cargo +1.81.0 test --locked --all-targets; cargo +1.81.0 build --release --locked. Then use target/release/ym4-gitram baseline SOURCE_SHA OUTPUT_ROOT or target/release/ym4-gitram shard ID SOURCE_SHA SHARD_DIR, followed by target/release/ym4-gitram fan-in SOURCE_SHA SHARDS_DIR SEAL_DIR. SOURCE_SHA must be the full lowercase 40-hex source commit. Keep baseline output separate from the four shard subdirectories named shard-0 through shard-3.

### Hosted results and historical failed controls

The first run, https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/41689538266 , passed baseline, all four shards and fan-in, but retained a FAIL on source formatting. A subsequent run, https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/actions/runs/41690101300 , passed all seven jobs (formatting, Clippy, tests, baseline, 4 shards, fan-in). The first PR merge checkout was 152b2c03572c25ebf697b495ae2b5974384eca5c; its exact finite-lattice Wilson-action sums at beta=1 were:

| Shard | Wilson-action sum |
|---|---:|
| 0 | 45956/625 |
| 1 | 7888/125 |
| 2 | 44212/625 |
| 3 | 40124/625 |
| Four-shard sum | 169732/625 |

Sequential and distributed fan-in agreed exactly, including a recorded anchor root SHA-256 of a375d0afa2c143d1146d4e351b262edc18289580773bf7c4ab11ceaf61d06f5a. The sequential process took 6 ms on that tiny four-shard test. The baseline artifact tree held 8,441 bytes and the four downloaded shard artifacts 7,403 bytes. This is not an end-to-end GitRAM speedup result: GitHub runner, toolchain, compilation and artifact overhead dominate such a small task, and the runner RESOURCE.txt artifacts retain those costs.

### Explicit remaining gates

- The candidate is SYNTHETIC_CONTROL from reproducible trits, NOT actual GGUF inference. No QNN weights are loaded or reconstructed from hashes. The pinned upstream source refs are references only.
- This uses exact rational matrices belonging to continuous SU(2), but evaluates only finitely many link configurations. It does NOT integrate continuous SU(2) Haar measure or establish continuum existence.
- The HEB-C integer-only SHA-256 algorithm is reused, but the native bridge defines its own ym4.qnn.gitram.v0 HBP/HBI schema. The live HTTP0 service and physical 300GB Host8 store are not used.
- SHA/HBP/HBI validate checked data relative to the pinned source and deterministic expectations. An unsigned anchor is NOT an author signature.
- There is NO new mass-gap lower bound. Exact SU(2) finite lattice covariance, a candidate generator and integrity verification cannot substitute for reflection positivity, RG estimates across all scales, Osterwalder-Schrader reconstruction or a positive physical continuum gap.

Next scientific experiment: obtain pinned real QNN weights, a byte-validated model loader, a proof of output-to-link representation validity, and independent controls; then compare QNN candidates with a non-QNN baseline on a correctly defined 4D SU(2) variational problem. Any rigorous lower bound requires a separate mathematical certificate.
