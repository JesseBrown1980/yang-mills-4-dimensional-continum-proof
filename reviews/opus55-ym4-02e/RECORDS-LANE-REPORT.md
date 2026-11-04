**VERDICT: HOLD at 09ff0f2.** All recomputed numbers agree; the holds are on records and test reach.

**Holds, 20 with exact text:**
- **H1:** "falling steps" fails at μ = 2 (steps 223, 152, 113, 84, 51, 58). MEASURED.
- **H2:** "every composition row holds", but the receipt has 0 such rows. There are 142 silent checks, DERIVED.
- **H3:** the general reading of C. At L = 8, C reads 6355 at q = 4/5 and 1000 at q = 1/5.
- **H4:** "falls" is constant on Z2 one-link.
- **H7/H8:** GPT-6's fifth message (18:57:33Z, the charpoly refinement row 141 credits) is missing from the "verbatim" file. The sixth arrived after the commit. The filed four match the relays, edit_ops=0.
- **H9:** the first-run code is on no ref. `f818bc5` already has containment; the transcript holds the original.
- **H5, H16–H19:** hosted text is stale. The PR's "Bounded… MEASURED" overstates.
- **H20:** `predict_02e.py` is on no ref.
- **H6:** the "is not" heading.
- **H10–H15:** test edits. With all six applied, stdout equals the receipt, MEASURED.

**Prediction:** MEASURED. Rows pushed 17:43:11Z with hash 7931f9bf…; test first written 17:48:51Z. Later rows 131–145 weaken no frozen number. KSTEP, PRODUCT, A_ENTERS and NO_A came by characters and hand blocks. LOCAL neighbours and r repeat the test's logic; separate code confirms 23/23.

**Surviving mutants:**
- Run whole: A1, A2 (first start row always decisive), B2, B3 (equivalent, DERIVED), B5 (non-symmetry accepted by `Z2Conv.commutes`, no row moves).
- D6: 266/266 rows read agree.
- DERIVED from coverage: F1–F5, D1, D4, D7, B4, I2, I7–I11. Lines 658–665 never run; `first_above`=1 on 99/99 calls.
- H10–H12 kill F1, F3, D6, F5; F2 still survives. A6 moves only row 101, Q8 2×1 k=4.
- 23 of 39 killed.
- Cap or my own stop, no FAILED row: C2 (42 rows changed), C6 (76), C4 (1), H1, G2, G7, I12 (rows read differ); E2, G1, I13 (rows agree). A check past L = 3 is proposed, unwritten.

**`top_two`:**
- The count is rigorous on every row: `same_cell`=0 and `lo1_is_zero`=0, 99/99.
- Wrong bracket found only at w = 1/4, 1 (λ₁ = −3/8, `lo1`=0). `free=0` flags it; no row reaches it.
- Fuzz: 329 pencils, 0 mismatches, fallback fired 26 times, Theorem 5 0 violations in 52 cases.
- BlockPencil's filter is exact. Starts are rigorous: 54/54 builds affine and full symmetries, 67 direct comparisons, 0 differ.

**Ran, MEASURED:**
- Local run equals the receipt with CRs removed (747 s under load).
- 7 sabotages exit 1 on their checks; unknown name exits 2.
- Hosted at the commit: push 403 s, PR 597 s, limit 1,500 s. `f818bc5`: 1207 s, failed at cmp with no receipt, as its message says.
- Gate: 28 rows, 162 findings, `scripts/` unchanged.
- Note: 42 of 44 claims hold.
- Independent code agrees: R_k on Q8 1×1 and Z2 2×2 exactly; Q8 2×1 at k = 1, 2, 4; ratios on Z3 2×2 and Q8 1×1×1; ring μ=2 at L=4 (τ, C, ratio) and L=6, k=6 (τ, ratio); locality row Q8 r=19/20 (ratio, τ).

**Could not check:**
- CANNOT_SEE: a test draft outside this session; GPT-6's original beside the relay; the 209th line.
- NOT_MEASURED, BUDGET: the Z2 2×2×1 ratio by my code (its r, c, τ agree); ring L=6, k=12; mutants never started.
- No proof review of Theorem 5.

**Files in `C:/tmp/opus55/02e-records-20261104/`:** `FINDINGS.txt` (`.txt` because the harness bars `.md` report files), `HOLDS.txt`, `rows/`, `scripts/`, `mutants/`. Repo untouched.
