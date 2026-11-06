**Head checked.** The worktree reads `b577fa83ac5a3e84f27709cbd73b3c54afe605c5` and stayed clean through every run. It is also PR #29's head on GitHub.

Files are in `C:/tmp/opus55/ym4-03-recheck-proofs-20261105/`:
- `FINDINGS.txt`, sha256 `efb1899b…`
- `HOLDS.txt`, sha256 `c2773beb…`: 43 holds, 3 high, 11 medium, 29 low. Each OLD reads once at this head and all apply in turn on a copy (`scripts/s11_check_holds.py`).

**What I ran** (integers or exact rationals; no code shared with the test unless marked):
- **Owning gate, MEASURED:** the test at this head gives rc=0 and 362 checks, 0 failed, with stdout byte-equal to the receipt after removing CR. Hosted checks at this head read success, one-scale-blocking 16:24:26Z to 16:52:58Z, every step green.
- **`rust/cover`** (Rust 1.81, clippy -D warnings exit 0): exhaustive search on whole lattices for the fewest plaquettes covering a coarse line, with no slices and no count from the proof.
- **`s01`, `s01b`:** exact merge of words at rational V, for flat fillings, tubes and capped boxes.
- **`s03`:** separate flux code on all five lattices.
- **`s04`, `s04b`:** central and non-central z, T not ≥ 0, detoured loops, Theorem 7 item 3.
- **`s06`, `s07`:** Theorem 13 on an exact chain, Theorem 14's numbers.
- **`s05`, `s09`:** the test's own objects, imported with no bytecode, to read what its vectors and terms hold.
- **`s08`, `s08b`, `s10`:** the hold ledger, the pins, added sentences with negative words.
- **Private test copies** with the holds applied (`private/`, `s12`).
- **Page images** of Lüscher 1988 pp. 508–513, van Baal–Koller pp. 352–353, Koller–van Baal p. 400, van Baal's review p. 11.

**What survives:**
- **Lemma 9a, all four items, on every lattice in scope** (DERIVED):
  - Item 1: a line vertex of degree 1 does survive. It is the flat filling on every L_ν ≥ 2, read exactly on 45 of 45 rows (MEASURED).
  - Item 2: double edges, winding cycles and the single-line case hold by hand.
  - Item 3: classification, multiplicity, orientation and (b−1)² hold. The boundary links on L_μ = L_ν = 1 give the commutator.
  - Item 4: "one free link at a time" is right where links share plaquettes (Fubini). The largest degree in any term the 2T read uses is 4 on both lattices, MEASURED. No term goes above 5.
- **The b·min(b,4) count now reads by search** on these lattices (MEASURED):
  - (ℤ/4)³: 16, 6 sets (2 flat, 4 tubes)
  - (ℤ/4)⁴: 16, 15 sets
  - (ℤ/5)³: 20, 4 tubes
  - (ℤ/5)⁴: 20, 12 tubes
  - (ℤ/6)³: 24; (ℤ/7)³: 28
- **Thin tube values:** 2^{−8b}χ² at b = 2 to 7 and 2^{−16b} on L_μ = 2, MEASURED. "At b ≥ 5 it comes first" is DERIVED, and it does need the sum over tubes, see H9.
- **Proposition 7a at T ≥ 0:**
  - The kernel is positive on orbits.
  - Commutation reads on every configuration, including fine side 2 and the side 1 where a word holds a μ-link twice.
  - Non-central z fails.
  - Two planes differ by a band gauge transformation at any central z, read at order 3.
  - P_e fits z² = 1 and only that.
- **Theorem 13 as merged:** the proof reaches the statement, the constant is free of the time side, and it passes to items 2 and 5. The chain run read 0 violations on 276 pairs.
- **Theorem 14's reading:** 4 ≤ bag < 6, 0.3439, 0.5158 and the family a = 4/(gb) all hold, and the UH paragraph agrees with b ≥ 2√β (963 of 963 cases).
- **Theorem 7 item 3 as a statement:** 18 dimensions, 6 and 12, MEASURED on W and H′.
- **Every flux number in section 9 except the two e = 0 rows below,** read by separate code.
- **Literature:** eq. numbers, values, the quotation, e = 0 and the range all read on the page as the note has them.
- **Counts:** 362 checks and 7 reads on 3 rows. 98 ledger rows for 98 holds, each OLD once at 6c87200. Both pins hold.

**What is refuted or narrower than written:**
1. **e = 0 rows on Z2 at 2×1 and 3×1 (high, MEASURED).** On a spatial side 1, A leaves the winding along the long side alone. So F Ω is an exact eigenvector and F T^b F Ω an exact multiple of Ω.
   - The part off u reads 2⁻¹⁸⁹⁵, then 2⁻³⁷⁸⁴, as the walk goes from 240 to 480 steps, and likewise at 3×1. The rows' 1.00000 is the Perron walk's remainder, on the first excited state.
   - With F across the side 1, 2×1 reads 1.00000 (forced, since e = 0 has dimension 2) and 3×1 reads 0.75568. The level stays visible on all five.
   - The patched copy passes at 362 checks, 5 receipt lines change, and the sabotages I re-ran fire on their named checks.
   - The receipt's `of_multiplicity_2` is cumulative, and `flux_full_gap_is_the_min` cannot fail.
2. **"So that expansion is Δ₀ of section 4" (high, MEASURED on the page).** The expansion is the A₁⁺⁺ level of e = 0.
   - Lüscher's Table 4 reads E⁺ and T₂⁺ at 0.86 of it at z = 1, with ratios practically independent of z below that.
   - Koller–van Baal p. 400: "In weak coupling the smallest mass is a 2+ state."
   - "Of order exp(−S/g)" also reads wrong, because eq. 12 carries a growing factor beside it. "Led by" is right.
3. **"Exactly when these levels stay visible," and section 8's "stay away from zero" (medium, DERIVED).** Item 4 asks for one level, the one that sets Δ_full. Item 5 at each a takes any positive overlap.
4. **Proposition 7a (medium).**
   - At w > 0 alone the log has no value: Z2, w = 1, 3, on a circle of 3 has λ₀(e) = −1.
   - "Crosses once" fails for a loop with a detour, which crosses 3 times with net factor z (MEASURED).
   - "Changes sign" needs π(z) = −1. Spin 1 keeps its sign.
5. **Theorem 7 item 3's proof was left behind its statement (medium).** It gives one direction, uses T only through T^b, and omits the coarse gauge invariance of E[hΩ|Q]. Replacement in H7.
6. **"So item 2 and the flow are statements at b = 2, 3" (medium).** That holds with d ≥ 3 and a side L_μ = 1.
   - On every L_i ≥ 2, a term that moves with V holds a closed coarse loop of covered coarse links, since a gauge-invariant function on a forest is constant.
   - So first dependence sits at n ≥ min(b², 8b), and item 2 holds through b = 7, DERIVED here. This turns F04's CONJECTURE into a bound.
   - Read at b = 4, 5, 6: a coarse plaquette target gives b², one flat set.
   - The search's 22 at b = 5 on L_0 = 2 is a capped box, whose E_V is constant in V.
7. **Ledger.** Three `applied_as_held` rows carry more than held (text:H19, H20, H40). One sentence was lost: test:H18's "The spatial block is 2×1 on all but Z2 at 2×2." That matters now that three of the five flux lattices have fine side 1.
8. **Stale or scope points:**
   - The PR body says hosted checks are open; they read success.
   - The README lacks "on PH".
   - PROOF_OBLIGATIONS says "read at b = 2".
   - Section 7a's Balaban bullet stays NAMED: the local copy is a 919-byte 403 page, so the body is CANNOT_SEE.
9. **Operator's rule.** "Refuted no theorem's core" in three places, "no closed block", "no self-loops", "no 2-cycles", "in no row" twice, "cannot reach".

**Holds:**
- H1 high, test: e = 0 fallback takes the first winding with a real part off Ω.
- H1b low, test: multiplicity label.
- H1c low, test: real inertia check for Δ_full; a mutant fires on all five.
- H2 high, note §9: e = 0 row reads 1.00000, 0.78787, 0.75568, 0.61332.
- H2b low, note: 0.967 was on the replaced vector.
- H3 medium, note §4: "exactly when these levels" sentence.
- H4 medium, note §8: what Theorem 13 needs; "with Ω taken out".
- H5 medium, Prop 7a: T ≥ 0, Δ_full defined.
- H5b low: z ≠ 1, with π(z) = −1.
- H6 medium, Prop 7a item 2: factor zⁿ and characters.
- H7 medium, Theorem 7: proof paragraph of item 3.
- H7b low: μ > 0.
- H8 low, Theorem 13 proof: constant added to f.
- H8b low, Theorem 13: "exactly when" wording.
- H8c low, §4: same wording.
- H9 medium, thin tube: coefficient, its derivation, and the search reads.
- H10 medium, thin tube: "stop at b = 3" on a side 1, min(b², 8b) on L_i ≥ 2.
- H11 high, §7a: A₁⁺⁺ level, Table 4, p. 400, "led by".
- H11b low, §7a: channel A₁⁺⁺.
- H12 low, UH: m′, with H′ = PH on a circle.
- H13a low, §9: spatial block on the coarse row.
- H13b low, §9: block and fine side 1 on the flux row.
- H13c low, scope line: c_π ≥ 0.
- H13d low, §9: search reads of the count.
- H14a low, status line, positive form.
- H14b low, README, positive form.
- H14c low, PR body, positive form.
- H15a low: "blocks join".
- H15b low: "each edge joins two different vertices".
- H15c low: "every cycle at least 3 edges".
- H15d low: "a read added after".
- H15e low: same.
- H16 medium, prediction: correction row at the end, pins unaffected.
- H17 low, HOLDS-APPLIED: four correction rows beside.
- H17b low, SHA256SUMS: `3f9eb4ed…`.
- H18 low, README: "on PH".
- H19 low, PROOF_OBLIGATIONS: b = 3 on the flat filling.
- H20 medium, PR body: hosted checks success.
- H21 medium, PR body: flow scope, min(b², 8b).
- H22 low, test docstring: the four points carry homogeneous degree 2.
- H23 medium, PR body: e = 0 row.
- H24 low, PR body: "reads Ω alone".
- H25 low, PR body: "exactly when".

**What I could not check:**
- **Bodies:** Balaban CMP 122 and Lüscher 1983 are CANNOT_SEE. GPT-6's PDF links were not fetched, by the lane's rule.
- **Search, reason BUDGET:** the winding-loop target at b = 4, 5 is NOT_MEASURED, a limit of this lane and no finding on the lattice. The b = 8, 9 cases are NOT_MEASURED and stay DERIVED.
- **Equality at b = 4..7:** the classification is by hand. The search reads b = 4, 5, 6.
- **Mutation of `section_flux`:** not run here. Findings 1's walk remainder and the check that cannot fail came from reading by hand, so a mutation run would likely find more.
- **Not reopened:** first-lane literature.
- **Other private-copy sabotages:** `twist_every_link` returns before the changed lines, so I did not re-run it. The rest of the test's sabotages are not re-run on the private copy.
- **The gate after these holds:** nothing here is pushed. A new head reopens the hosted checks, and H1, H1b and H1c regenerate the receipt.
