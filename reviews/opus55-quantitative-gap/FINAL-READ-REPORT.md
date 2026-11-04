**VERDICT: HOLD at 27f9886.** The statement and the second proof stand. Five text holds, all in C:/tmp/opus55/final-02d-20261104/repo-lf/docs/NOTE-YM4-02d-QUANTITATIVE-GAP.md.

**H1, line 73.** Old: `for μ ≠ λ₀, ρ = h/Ω`. New: `for μ ≠ 0, λ₀, continuous as in Step 3 (μ = 0 needs nothing), ρ = h/Ω`. Reason: on the circle, a weight with vanishing even harmonics has an unbounded L² h at μ = 0, with no largest point.

**H2, line 89.**
- Old: `Equality holds exactly when`. New: `With M > m, equality holds exactly when`.
- Old: `strict on every weight,`. New: `strict on every weight with M > m,`.
- Reason: constant w gives |μ| = 0 = τλ₀. DERIVATIONS §2 carries M > m.

**H3, line 89.** Old: `Among weights with T ≥ 0 on the orbits the largest share measured is 1/2`. New: `Among weights with T ≥ 0 on the orbits at N_ℓ ≥ 2, the largest effective exponent measured reads N_ℓ/2`. Reason: search-A CLOSEST reads Z2 one link, negatives=0, share 1.

**H4, line 89.** Old: `at most 0.249`. New: `below 0.25`. Reason: row value 249 is a floor. Integers read 0.249979 at β = 1/16 and 0.249675 at β = 1/4.

**H5, line 93.** Old: `for β bounded below.`. New: `for β bounded below by a positive constant.`. Reason: β = a⁴ sends the limit to ∞.

**NOTES**
- The multipliers' last clause is true. The example keeps B whole, so on H the form of A is forced; B enters on PH through BP.
- The block omits |G|^{−N_ℓ}, with the ratio unaffected.
- opus55 README:24 reads CANNOT_SEE; SECOND-SEAT.hbp:11 reads reason=BUDGET.
- gpt6-quantitative-gap README:12, "on PR #14's branch": those files are also on main.
- ATTACK-REPORT:50 "at most 0.25"; trend-wilson reads Q8 one link 0.450.

**RAN (MEASURED)**
- Prediction hash met; report equals the attack's text; SHA256SUMS 36/36.
- Gate, local Python 3.13: 28 rows, 162 findings, failed=0.
- 84 relative links resolve; the numbers checked match their rows.
- Exact multiplier ratios reach τ from below on Z2, Z3, S3.
- Hosted: 12 of 12 success, required three pass.

**Not run:** the test locally, recomputing S3 rows, opening the cited papers.
