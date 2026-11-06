Head checked: `2184b54f44c39079f4873562c8874da3836736e1`, at the start and at the end. The checkout stayed clean, with no `__pycache__`, and none of this lane's processes is still running. The user line passed through the harness ("the TV got caught into the conversation") gave this lane no instruction, so I did only the assigned step.

**Main result: `refuted=true` for the target as asked.** The checks around the corrected code catch a certificate only when it is grossly wrong. 26 of my 36 mutants pass every check, match the receipt byte for byte, and pass the sabotage line. The four claims themselves stand (DERIVED, below), and no printed read at these five lattices changes under any surviving mutant. The faults those mutants plant are latent: the checks cannot see them.

**Method change you should know about.** Other lanes' jobs slowed full runs from 222 s to 450–630 s. These ran as full tests:
- the head;
- a diagnostic copy that writes extra rows to stderr only (its stdout equals the receipt);
- all 12 sabotages at the head;
- the patched copy and its 6 sabotages that reach the changed code.

The 36 mutants and 18 patched mutants did not run as full tests. They ran through `tools/flux_only.py`, which prints the head's first 117 receipt lines and then runs `section_flux` alone with the counters carried over. This is exact here because every edit sits in the flux helpers or `section_flux`, and nothing earlier calls them. Before relying on it I compared it with full runs: three byte-for-byte matches (head vs receipt, the new sabotage at the head, the patched copy's inflated sabotage) and two count matches (202 + 199 = 401, 224 + 199 = 423). Results are in `runs/VALIDATE.hbp`.

**What I ran (MEASURED)**
- **Workflow pin and gate lines** on a git clone of the head: all pass (gate: `code_files=104`, `failed=0`). On a plain archive copy the gate reads 0 files, because it reads blobs through git; that copy is CANNOT_SEE for it.
- **All 12 sabotage lines, plus the unknown name:** all pass, with FAILED counts equal to the hosted run 42101686287 (push, success). The PR run 42101699279 is also success.
- **The new sabotage line names its check correctly:** exit 1, 2 FAILED rows. It turns both the 2×1 and the 3×1 control red but names only the 2×1 one.
- **Margins (diagnostic copy, rows in `diag/`):**
  - The one exact-zero control sits at 1928 ppm of its error on 2×1 (2⁻⁹) and 2⁻¹⁹ on 3×1.
  - Every accepted candidate sits 2¹³⁷⁹ or more above its error.
  - The leak term is at most 2⁻⁹⁹⁵ units of 10⁻⁹, so it can never move a printed digit.
- **My own exact Z2 2×1 code** (in Q(√481), sharing nothing with the test) agrees:
  - share 955960752, inside the receipt bracket;
  - the direction-0 control at 1928 ppm;
  - with both the factor 2 and the |u|²|O|² term dropped, that control still reads 991469 ppm, so it still rejects and cannot see either drop.

**The 36 mutants**
| Outcome | Count | Mutants |
|---|---|---|
| Killed by a named check | 8 | C09, C15, C16, C19, C20, C21, C32, C34 |
| Caught only by the receipt comparison | 1 | C30 |
| Caught only by the sabotage line | 1 | C31 |
| Passed everything | 26 | see below |

Of the 26 that passed, 18 are real faults the checks miss:
- **Visibility error:** factor 2 dropped, |u|²|O|² term dropped, both, |v|² term dropped, reduced v's norm, |w|² counted 4×, sin² a quarter low (C11–C14, C17, C18, C23).
- **|O|² bound set low:** C24, C26, C27.
- **Leak formula:** dropped, sign flipped, 2n−1, no |w|², top_high in place of ground_high (C01, C02, C04, C05, C06).
- **Checks no line shows able to fail:** two-insertion, narrow-bracket and low ≤ high made vacuous (C33, C35, C36).

With the holds, all 18 turn a named check or a sabotage line red (`runs/PM.hbp`).

The other 8 change nothing true here, and I propose no hold for them:
- C03, C07, C08 move a leak of at most 2⁻⁹⁹⁵ units; DERIVED, `flux_rational_omega_close` keeps it under one unit.
- C10 (≥ for >) and C25 (max|f|² for max|f|⁴, with max|f| = 1) run the same program on these inputs.
- C22 only enlarges the error.
- C28 and C29 move the e ≠ 0 error, whose rows sit 2¹³⁹⁴ or more above it. No exact zero for e ≠ 0 is in reach in this test (DERIVED for F0 on side-1 lattices); that stays OPEN.

**What survives (DERIVED, my own algebra, in FINDINGS F4)**
- Claim 1, the sin² bound. S ≥ 0 is not needed for it.
- Claim 2, the leak bound.
- Claim 3, both visibility bounds, term by term.
- Claim 4: F0 S F0 = 2⁻ᴸ⁰ S on e = 0 for Z2 with w = 3, 1.

One side read, no hold: the scaling read and its control are Z2-only. When Q8 is forced into that branch, the scaling row turns red, as measured.

**A second, separate fault (MEASURED):** at this head, note §9 line 248 has 9 unescaped pipes; it had 3 at b577fa8, and the note escapes them elsewhere. GitHub's own renderer cuts the row after "over the gap squared and". That drops the leak correction, the negative control, its sabotage and GPT-6's attribution from the rendered page.

**Holds** (16 blocks, each applied cleanly to a fresh clone at the head; the patched clone passes every pin, 423 checks, 0 failed)
- H1 (medium): new exact-zero control on all five lattices, O = 2^(s+1)S − ground_low. It sits at 873518, 818455, 762892, 749097 and 929490 ppm of its error, which is (1 − λ₁/λ₀)².
- H2 (low): leak control at u after 4 steps of S. With the leak term the share is at most 1; without it the low runs to 112–179 digits.
- H3 (medium): checks |O u|² ≤ |O|² bound × |u|² on all 12 calls.
- H4, H5 (medium): sabotages `visibility_error_halved` and `visibility_error_inflated`.
- H6 (medium): their workflow lines, plus `overlap_one_power`.
- H7 (low): the `overlap_one_power` loop.
- H8 (low): restores the `overlap_bracket` line for `overlap_skips_next`.
- H9: receipt count 401 → 423.
- H10, H11: the note's and README's count 401 → 423.
- H12 (medium): note §9 text describing the new controls and their margins.
- H13 (low): a prediction ATTEMPT row for the new receipt.
- H14 (low): the mutation count in the note.
- H15, H16 (medium): escape the pipes in the §9 row.

**What I could not check**
- The 9 older sabotage lines on the patched copy were not run (NOT_MEASURED). DERIVED: their branches sit before the sectors, so they cannot reach the changed lines.
- The hosted runner's Python version; its log does not print it.
- Larger lattices.
- I wrote no memory file, because this lane's rule keeps every write in its folder; the parent seat may want to record these findings.

Method faults on record: once, Python read its script from stdin, which breaks this lane's rule; it touched only a draft file in my folder. I also stopped my own first queue by PID, which killed two C01 runs mid-way (set aside in `runs/PB_killed/`).

Files are in C:/tmp/opus55/ym4-03-cert-mutation-20261105/:
- FINDINGS.txt
- HOLDS.txt
- runs/TABLE.hbp
- runs/PM.hbp
- runs/VALIDATE.hbp
- diag/DIAG_HEAD.hbp
- diag/DIAG_PATCHED.hbp
- own/z2_2x1_own.py
- render/row248_head.html
- render/row248_patched.html
