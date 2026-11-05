# The second seat's attack on the corrected certificate, at `2184b54`

Two opus55 lanes attacked the e = 0 overlap certificate and the visibility test as corrected on GPT-6's review of `b577fa8`. One worked by derivation and exact small matrices, and the other by mutation of the new code.

**The four claims survive, DERIVED by both lanes and MEASURED on exact projectors.** The claims are the sin² bound on the rational Ω, the ground weight of a centered vector, visibility carried past u's error, and the exact zero of the winding in direction 0 on side-1 lattices.
- On Z2 at 2×1 and 3×1 and Q8 at 2×1, every printed low end lies below the true share and every high end above it.
- Every MET row has a true part above 0.
- 9,000 exact worst cases through the test's own functions gave 0 false certifications.

**Refuted: the checks around it were too blunt.** The first exact-zero control sat at 2⁻⁹ to 2⁻¹⁹ of its error term, so 26 of 36 mutants passed every check, 18 of them real faults: a factor 2 dropped, a term dropped, the leak formula wrong. No printed read moved under any of them.

**What the holds add:**
- An exact-zero control on all five lattices, O = 2^(s+1)S minus its ground value, which sits at 0.75 to 0.93 of its error term.
- A control on the leak term.
- A check of the operator bound on all 12 calls.
- Three sabotages, `visibility_error_halved`, `visibility_error_inflated` and `overlap_one_power`, each read by the workflow.

With them, all 18 real faults turn a named check or a sabotage line red. The note's §9 row had unescaped pipes that cut it on GitHub's page; it is escaped.

**The disposition of every hold:** [`HOLDS-APPLIED.hbp`](HOLDS-APPLIED.hbp), 25 rows. The derivation lane's sharp control and sabotage are carried by the mutation lane's broader ones. **Each lane's own words:** `REPORT.md`, `FINDINGS.txt` and `HOLDS.txt` in [`derivation/`](derivation/) and [`mutation/`](mutation/). Their scripts are in the tools archive `D:/safety-backups/opus55-ym4-03-certificate-20261105-tools.tar.gz`.

**Limits, from the lanes.** Z2 at 3×2 exact truth ran past its time and stayed unread. Q8 at 3×1 or larger, and Z2 weights other than 3, 1, are open. An exact zero for e ≠ 0 lies outside this test's reach.
