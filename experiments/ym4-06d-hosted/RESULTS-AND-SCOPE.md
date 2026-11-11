# YM4-06D — hosted exact-integer SU(2) Wilson-link spectral pilot

Date: 2026-11-11. Status: verified finite controls; no 4D continuum mass-gap solution.

## Frozen predictions

- Pilot freeze: b63a2848fd23bc3a9cffc464c93036f2b92c3dbe (before verifier code).
- SU(2) Wilson link-ratio freeze: d426b0916f988084942433c71638f4485044059b (before spectral-ratio code).
- Both original HBP files are compared to their frozen bytes at the beginning of the hosted job. The r=9 one-shot is not used.

## Exact, executable results

1. S3 via affine maps on Z3: 2D 2×2 has 18 commuting pairs, 8 flat orbits and 1,393 physical gauge orbits. 3D 2×2×2 has 48 commuting triples, 21 flat orbits and 2,821,153,019,713 physical gauge orbits. This is a count, not an eigensolver.
2. Gauge-compatible SU(2) Peter–Weyl link cutoffs q=3,9,27,81 retain every irreducible block through twice-spin n=q−1. Per-link dimensions: 14, 285, 6,930, 180,441, exactly addressable with 3, 6, 9, 12 trits. Full SU(2) left/right covariance follows by keeping whole irreps; native tests explicitly check the noncommuting quaternion SU(2) subgroup generators I=diag(i,−i) and J on every monomial and its matrix-coefficient index. This does NOT certify the interacting transfer projection error.
3. For the SU(2) Wilson one-link convolution kernel at beta=1, the spin-n/2 coefficient is exp(−1) times l_n(1), where l_n(1)=sum over s≥0 of 2^(−2s−n)/(s!*(s+n+1)!). A positive rational partial sum through s=4 and geometric tail enclosures prove 0.24019372 < l_1(1)/l_0(1) < 0.24019373. Exact integer fractions stored in the HBP provide stronger intermediate bounds. This is a gauge-covariant LINK eigenratio, NOT the first gauge-invariant physical excitation of the 4D interacting Wilson transfer.
4. At beta=1, rigorous one-link trace-tail upper bounds: q3 32/243; q9 25/329204736; q27 and q81 less than 10^(−30). These bounds must not be substituted for an interacting 3D spatial-slice cutoff error without a separate theorem.
5. A noncommuting local S3 electric/magnetic pair has nonzero Strang BCH cubic correction. The formal unequal-clock ratio is 7/4 under a NONZERO leading observable mass-error coefficient. Neither the full 2D S3 spectral error nor its sign is measured.
6. Exact opposite scaling families: if n=3^k and a=1/n, second transfer ratio 1−1/n yields mass limit 1, while ratio 1−1/n² yields mass limit zero, even though every finite gap is positive.
7. Four triadic Merkle fixtures changed one trit and recomputed the global SHA root, while a distinct distant trit was unchanged. This is a commitment property and does not establish instantaneous physical influence.

## Replay and fault gates

Native Rust 1.81, strict Clippy, exact integers and numerator/denominator pairs, no JSON or Node/V8 in authored experiment. Six negative controls reject dropped SU(2) representations, wrong central parity, wrong Wilson bound, wrongly rounded Wilson spectral ratio, vanishing-mass misclassification, and a changed HBP. Five canonical HBI/HBP/SHA/SH/HASH files plus SHA256SUMS are committed under evidence/ and the hosted runner rebuilds and byte-compares them all. Existing no-float source and compiled gates are not weakened.

## Open physics obligations

The physical YM4-06D target is the lowest excitation of the GAUGE-INVARIANT, ANISOTROPIC 3+1D SU(2) Wilson transfer matrix, including the spatial-plaquette factor A, the gauge projector, multi-link correlations, the coupling/anisotropy matching, certified representation truncation errors, spatial and temporal continuum scaling, volume-uniform spectral bounds and Osterwalder–Schrader reconstruction. This pilot computes none of those full-spectrum eigenvalues. It does not solve the 4D continuum mass gap, and it leaves the original r=9 blind run untouched.

Reference: the revised prediction draft in docs/DRAFT-PREDICTION-YM4-06D-GLOBAL-LOCK-SLICE-SCALING-20261111.md and Wilson transfer in docs/LEMMA-0004-REFLECTION-TRANSFER.md.
