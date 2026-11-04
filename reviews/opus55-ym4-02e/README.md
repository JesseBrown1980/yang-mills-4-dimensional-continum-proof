# The second seat on YM4-02e, at `09ff0f2`

**The records lane: HOLD at the commit, with every number it recomputed in agreement.** [Its report, verbatim](RECORDS-LANE-REPORT.md), [its findings](FINDINGS.txt) and [its holds](HOLDS.txt).

**The proof lane: FAILED, and it checked nothing.** Its reply passed the 128,000-token output limit after 7 tool calls, and it returned no result. So at this commit the second seat has run no proof review of Theorem 5, and the records lane says so too. It was relaunched in narrower lanes, whose reports are filed beside this one when they return.

| What the records lane did | Result |
|---|---|
| Prediction first | Rows pushed at 17:43:11Z, the test first written at 17:48:51Z. Rows 131 to 145 weaken no frozen number |
| Reran the test | Exit 0, stdout equal to the receipt with CRs removed |
| Separate code, sharing no lines | R_k on Q8 at 1×1 and Z2 at 2×2 digit for digit, Q8 at 2×1, the ratios on Z3 at 2×2 and Q8 at 1×1×1, ring rows and a locality row all agree. Not measured: Z2 at 2×2×1 by its own code |
| Mutants | 39 run or read: 23 killed, 5 survived, 11 stopped by its clock. A further 14 follow from coverage |
| Fuzz | 329 pencils, 0 mismatches. Theorem 5 on 52 random-weight cases, 0 violations, at most 32 orbits |
| The note's measured section | 42 of 44 claims hold, with the other two held |

## What was applied

All 20 holds, in its text, in the commit after `09ff0f2`, with two changes by FABLE5. H9 files the first version of the test under a `.py` name, so that the gate reads it, bytes unchanged. H17 to H19 are the pull request's body.

Past the holds, on its findings: a pencil that counts exactly 2 at the certifying step, for its mutant F2, and a second route on three lattices past L = 3, which it proposed and left unwritten, for its mutants C2 and C6. Those checks reading in the receipt are FABLE5's, unread by this seat.

## Its files

`rows/` holds its row files, with CRs removed and `.txt` added to the one script copy. Its scripts and mutants would add list rows here, so they are held on this machine at `D:/safety-backups/opus55-02e-records-20261104-tools.tar.gz`, 221 files, SHA-256 `45918716166a9971ccea64d8b7b2c98f6c3181cd56f95a3ec228da72ab9593e7`, and their upload to the Hugging Face dataset is OPEN.
