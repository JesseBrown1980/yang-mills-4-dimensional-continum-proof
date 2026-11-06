# The second seat's recheck of YM4-03, at `b577fa8`

Two opus55 lanes read what YM4-03 gained after [the first attack](../opus55-ym4-03/): the electric-flux section of the test and its certificate, Lemma 9a, the thin tube, Proposition 7a, and the merged repairs of Theorems 7, 13 and 14. They worked by code of their own, sharing nothing with the test, in exact integers and rationals, on page images of the sources, and by 72 mutants of the flux section.

**Refuted, high, read by both lanes.** On Z2 at spatial 2×1 and 3×1, the rows `first_excited_visible_Z2_2x1` and `_Z2_3x1` read the error of the rational Perron vector, and their 1.00000 came from that error. With a transverse side of 1, the winding along the long side gives F T^b F = 2^(−bL₀) T^b on e = 0, exactly, so F T^b F Ω is a multiple of Ω. The centered vector the test certified has squared relative size 2⁻¹⁸⁹⁵ and 2⁻¹⁴³⁵, the bound on that error, and it falls as the Perron walk runs longer: −1895, then −3784, in log₂ on 2×1, from 240 to 480 steps. With the winding across the side 1 the first excited state is reached: 1.00000 on 2×1, forced since e = 0 has dimension 2 there, and 0.75568 on 3×1. Both rows stay MET. The test now takes the first winding whose centered vector stands above the vector's own error, and checks the exact scaling on side 1.

**Refuted, high, on the page.** Section 7a called van Baal and Koller's and Lüscher's small-volume expansion Δ₀ of section 4. It is the lightest A₁⁺⁺ level of e = 0. Lüscher's Table 4, p. 512, reads E⁺ and T₂⁺ at 0.86 of it, and Koller and van Baal, p. 400, write *"In weak coupling the smallest mass is a 2+ state."* So Δ₀ sits at or below that expansion.

**Refuted, medium or low.**
- The e = 0 multiplicity printed 2, with the ground counted. It is 1 on all five lattices.
- `flux_full_gap_is_the_min` compared a value with itself. It now reads the cross entries, the span, and the second value on the whole orbit space.
- Empty sectors and deflated brackets passed unseen.
- Proposition 7a needs T ≥ 0 for its logarithms, and a character with π(z) = −1 to change sign.
- Theorem 7, item 3's proof had stayed behind its statement.
- The flow's reach stops at b = 3 on a lattice with a side 1. With every side at least 2, the first dependence on V sits at min(b², 8b), DERIVED, so item 2 holds through b = 7.

**Survives, MEASURED and DERIVED:**
- Lemma 9a, all four items, on every lattice in scope.
- The count b·min(b, 4), by exhaustive search at b = 4 to 7.
- The thin tube's value 2^{−8b}χ², at b = 2 to 7.
- Proposition 7a at T ≥ 0.
- Theorem 13 as merged, and Theorem 14's numbers.
- Every other flux number in section 9.
- The certificate itself: scales, inner product, brackets, slack.
- Winding parity, on exact quaternions.
- The literature's equation numbers, values and quotation.

**GPT-6's review of `b577fa8`,** [comment 6667904991](https://github.com/JesseBrown1980/yang-mills-4-dimensional-continum-proof/pull/29#issuecomment-6667904991), went past the lanes on the certificate itself. A vector orthogonal to the rational u still holds a little of the exact Ω, and its share grows with the power. So the e = 0 certificate now takes that share off at every power, from sin²(u, Ω) at most the residual squared over the gap squared and |u|², in place of a fixed slack. Every visibility row carries u's error to the vector built on the exact Ω. The winding in direction 0 on Z2 at 2×1 and 3×1, whose exact vector has part 0 in the first excited level, reads not certified, as a negative control, and the sabotage `visibility_ignores_omega_error` turns that control red. Its §7a point is in the note: the expansion bounds Δ₀ and Δ_full from above. MEASURED with all of it in: 401 checks, 0 failed, the 7 misses unchanged, and every e = 0 lower bound one unit of 10⁻⁹ higher than with the slack.

**The disposition of every hold:** [`HOLDS-APPLIED.hbp`](HOLDS-APPLIED.hbp), 73 rows. Where the two lanes held the same text, one merged text carries both. **Each lane's own words:** `REPORT.md`, `FINDINGS.txt` and `HOLDS.txt` in [`flux/`](flux/) and [`proofs/`](proofs/). Their scripts and tables are in the tools archive `D:/safety-backups/opus55-ym4-03-recheck-20261105-tools.tar.gz`.

**Limits, from the lanes.** Balaban's CMP 122 and Lüscher 1983 are CANNOT_SEE in body. The winding-loop target at b = 4, 5 and the cases b = 8, 9 stay DERIVED. Larger Q8 and Z2 lattices and other weights are open.
