# YM4-04C G_attack filing

- **Seat:** the local Opus 5.5 seat, pid `8467a937cba309f7` (the second seat named in the gate row).
- **Target:** `JesseBrown1980/yang-mills-4-dimensional-continum-proof`, commit `6ebf63272ae230bfb08ef48b3156cb4202c24627`, branch `cloud-seat-ym4-04c-freeze-20261109`.
- **Pin, re-measured:** `head -n 42 docs/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp | sha256sum` gives `c74e6388295a6309674268dd18deba3728a4eb627a1530c42054182b2fadc404`, which matches. The note has 1770 lines and sha256 `322284bd…0a40`.
- **Rows:** `GATTACK-ROWS.hbp` holds 75 rows: 69 status rows, 1 summary row and 5 notes rows. Its sidecar is `GATTACK-ROWS.hbp.sha256`.
- **Status:** the filing is local and nothing was written to GitHub. The gate reads these rows only after they are appended after line 42 on the frozen branch, by the seat that has write access.

## Counts

| | reproduced | refuted | open | total |
|---|---|---|---|---|
| Acceptance checks (T1–T4, G1a–G1c) | 7 | 0 | 0 | 7 |
| Per-step entries (`per_step_status`) | 62 | 0 | 0 | 62 |

Every target name and its order were checked against `G_ATTACK_ROW.txt` mechanically, and they match exactly. T3 combines its two halves: T3_step0 (lane L2) and T3_stepk (lane L4) are both reproduced, and this filing also covered the reviewers' edge files (see below). Every lane covered its entries, so no entry got the `not_attacked` status.

## Refuted items

None. No lane found:
- a false step;
- an unrepaired gap in a statement;
- a proved constant that differs from the frozen one.

The skeptic revision was null for every lane, so the lane statuses stand. This filing re-checked the borderline points itself (see "Text defects" below) and did not change any status.

## Open items

None.

## Consequences under the frozen rules

- **G0 (step_rule):** G0 needs T1–T4 and every section-3 entry reproduced, Remarks 3.19 and 3.34 included. All of them are, so G0's release condition is met.
- **G1 (G1_rule and step_rule):** G1 needs all of the following reproduced, and all of them are, so G1's release condition is met:
  - T1–T4, G1a, G1b and G1c;
  - every section-4 entry;
  - the section-3 entries G1 uses: Lemma 3.2 items 1 and 5, Lemmas 3.15–3.17, Proposition 3.18 and Lemma 3.20.
- **C19:** the first part of G1c is reproduced, so C19's `variant_that_fires_with_another_ratio` field stands as written.
- **No UNSUPPORTED rows.** Nothing is refuted, so no row or clause reads UNSUPPORTED and no repair row is required.
- **Clauses released from CONDITIONAL-on-G0/G1** once the rows land after line 42:
  - `rests_on_G0_and_G1`: C07, C08, C11, C12, C13, C14, C16, C17's replacement clause, the hypothesis row's regime clause, the scope windows β_ind and β_ind^crude, and C19's δ_crit surrogate edge and upper surrogate end;
  - `rests_on_G0`: C01's injection clause, C09's T, and C19's readout_grid_128;
  - `rests_on_G1`: C10b's and C10c's comparisons, C13's δ_crit and c_fin values, and C10's optimality clause;
  - `rests_on_the_(1+t)^f_step`: each clause with its fallback;
  - every clause of `rests_on_a_numbered_entry` and of `meaning_only_through_G0`.
- **Other tags stay as they are:**
  - CONJECTURE on C03 for the refined values: C08, C09, C12, C14 and the C14 window;
  - TG where a row carries it;
  - REPORTED for the exponential formula, Weyl, Schur, Finner and Hoeffding.
- **Scope:** weak-coupling scale-to-scale control and the continuum stay OPEN. They are separate, and this filing does not touch them. No engine code was written or run.

## What this filing added beyond the lane results

1. **The T3 reviewer edge files.**
   - The four scripts and three outputs that check_T3 names are not in the `6ebf632` tree; the lanes' contents fetch returned 404. That means CANNOT_SEE at that tree, not that the files are absent.
   - This filing fetched all seven read-only from PR #45 head `dfe0859` into `work/filing/pr45-edges/`. **All seven sha256 values equal the ones in check_T3** (MEASURED).
   - Their final-constant reads match the lanes:
     - the C14 edge 0.02074/0.02075, with δ_1 0.1088558 and 0.1158911;
     - C13 crude 6α at 0.114567562 and 0.115083068;
     - the factor-6 surrogate edge 0.01552/0.01553.
   - Their other reads use draft constants (dcrit 0.109530694, 0.0558, 0.0496, and the factor-12 forms). No final row rests on them.
2. **The C_0 reads of `final-check/edges.py`.** No lane had certified these. That file is Decimal and has no .out, so this filing certified the reads with `c05_c06_edges.py`. The script is integer-only and reuses the L5 library. It proves NOT_MET with the convex tangent bound at θ = κ, which is enough by Lemma 3.31 item 2.

   | Row | Head | Read | Result |
   |---|---|---|---|
   | C05 | crude | 0.01903, 0.01904 | MET |
   | C05 | crude | 0.01905 | NOT_MET, min g ≥ 1.4227943e-5 |
   | C05 | crude | 1/50 | NOT_MET, min g ≥ 2.4350135e-2 |
   | C06 | C03 | 0.02075 | MET, α_- = 1.9315184719e-2, so 6α equals C14's δ_1 |
   | C06 | C03 | 0.02076 | NOT_MET, min g ≥ 1.1235445e-4 |
   | C06 | head-free | 0.02075 | MET |
   | C06 | head-free | 0.02076 | NOT_MET, min g ≥ 1.1224485e-4 |
   | C06 | C03 | 1/50 | MET |

   This turns L2's "cross-read only" at 0.02076 into a proof.
3. **Lane evidence re-checked.**
   - L1's manifest: 14/14 files OK.
   - L5's manifest: 21/21 files OK.
   - L2's rows sidecar: OK.
   - Every L2, L3 and L4 script and output hash equals the one its lane reported.
   - Every lane summary reads pass with 0 failures.
   - The one `ok=0` row, L5's `two_dprime_at_edge`, records a display defect at note line 1081. It is not a failure of a frozen constant.

## Text defects recorded beside reproduced statuses

None of these changes a statement or a constant.

1. **#Γ is overloaded.**
   - The Symbols paragraph (line 685) makes #Γ the element count.
   - Section 4.7 (line 898) redefines #Γ := ½#line(Γ) for d.
   - Lemma 4.12 item 2 (line 881) and Proposition 4.15's case (iii) and S_3 (lines 958 and 964) need the object count. Under the line-898 meaning, the trichotomy at line 958 would not be exhaustive.
   - The proof's own S_3 bound goes through Lemma 4.12 item 2, which comes before line 898. That forces the object reading, and the critic's Checked 3 reads it the same way.
   - Suggested appended clarification: read "#Γ ≥ 2" as "Γ ≠ {o}" at lines 881, 958 and 964.
2. **Lemma 4.19, sentence 2** ("constant, equal to e^{−4κ}, on an initial interval") is true, but the proof text leaves out its argument.
   - Completion: c_fin ≥ e^{−4κ} always, entry 2 tends to e^{−5κ}, and entry 3 is at most e^{δ−κ/2}λ/(e(κ−λ)), which tends to 0.
   - The κ = 1/4 interval clause the rows use follows from sentence 1, the floor and the endpoint read at line 1081.
3. **Lemma 4.17:** the sentence at line 995 has a false middle step (e^{0.114846769−1/8} > 0.989898139). The assembly note at line 997, inside the frozen commit, repairs it.
4. **Lemma 4.22:** its constant 0.62454 is reached only through Lemma 3.2 item 5 (Machin), which the frozen assembly note at line 1037 supplies. The proof's printed π > 333/106 gives only < 0.6245481.
5. **Proposition 4.14's remark at line 932** says no step uses that an input Y holds a loop. Lemma 4.5 does use it, through Lemma 4.1 item 5.
6. **Lemma 3.2's remark at line 194:** the enclosure [0.8488263, 0.8488264] is true, but its upper end needs π ≥ 3.14159252, which item 5 alone does not give.
7. **Theorem 3.7:** the text of Finner's paper was CANNOT_SEE. The quoted form was re-derived (Hölder, Tonelli, Fubini), and the status rests on that.
8. **Line 1081** prints three values as "enclosures" that are rounded to nearest:
   - 2δ′ upper end 0.2576475964, where the true image reaches 0.257647596441;
   - 0.3678794375, where the true value is 0.36787943754;
   - 0.3678794463, where the true value is 0.36787944629.

   Every comparison they feed holds, and none of these values appears in the 42 frozen rows.

**Decision boundary (the falsifier for two statuses).** This filing reads "reproduced" as: re-derived from the stated inputs, with the statement and its constants holding as written.
- Under a stricter reading that requires the proof text itself to be complete:
  - point 2 would make Lemma 4.19 read refuted, with the repair already supplied;
  - point 1 would make Proposition 4.15 read refuted, with the one-word repair.
- The rows that cite them would still hold mathematically, through the κ = 1/4 reads and the object-count reading. If the gate's owner takes the stricter reading, those two rows flip to refuted. In that case the two clarifications above should be appended after line 42 as repair rows.

## Notes on the (1+t)^f step and the m ≥ 1 root restriction

- **The (1+t)^f step is reproduced.**
  - Lemma 4.11 makes the component map injective, so the tree factor is the product over off(o) of (1+T(e′)), which is at most (1+t)^{#off(o)}.
  - Condition (T) is needed only at off links, and Lemma 4.13 item 1 proves it there with λ = δ′ + ln(1+δ′) ≤ κ. The KP weight e^{δ′f} and the tree factor (1+δ′)^f multiply to e^{λf}, which is where the condition λ ≤ κ comes from.
  - 24 exact instances pass. The planted fault, with (1+t)^{s(o)} dropped, gives 28 violations, so the check does detect a failure.
  - Every fallback value is reproduced (2δ′ ≤ κ is implied):
    - edge [0.111780108, 0.111780109];
    - flat end 0.077320139;
    - crude edge 0.01761/0.01762.
- **The root restriction m ≥ 1 is reproduced.**
  - The root at e_0 contains a line link.
  - Objects with m = 0 enter only as attached components or inside clusters.
  - The restriction carries weight: the last δ with object entry ≤ e^{−1} is

    | Roots | Rate λ | Rate 2δ′ |
    |---|---|---|
    | m ≥ 1 | 0.078733761 | 0.077320139 |
    | m ≥ 0 | 0.073323362 | 0.072094954 |

  - These match the F5 record at line 1223.

## Numbers lane

- **Every named number reproduced:**
  - δ_crit and its fallback;
  - the c_fin flat range and the C13 brackets, including c_fin(δ_crit^-) ∈ [0.989898134029, 0.989898134030] at f = 90;
  - μ;
  - the C13 and C14 edges with their δ_1 brackets;
  - C09's T on all 321 θ points at six couplings, with unique minimizers;
  - the C10c slack;
  - C16;
  - W03, computed exactly in Q(√2);
  - the β_k bound;
  - δ_1 for C07, C08 and C11;
  - C19's missing_tail reads and their recorded variant.
- **derive_checks.py**, rerun in a copy, is byte-identical to DERIVE-CHECKS.hbp: 54 checks, 0 failed.
- **CHANGES.txt** pass 1 called 1.00035867 a lower end. Pass 2 already corrects this, and C04 says "at least 1.00035", which holds.
- Each NUM entry covers only the arithmetic at its row's read points.

## Evidence and files

- Lane folders: `/mnt/c/tmp/opus55/ym4-04c-gattack/work/L1-sec3-part1/`, `L2-sec3-part2/`, `L3-sec4-part1/`, `L4-sec4-part2/` and `L5-numbers/`.
- Filing folder: `/mnt/c/tmp/opus55/ym4-04c-gattack/work/filing/`. It contains:
  - `GATTACK-ROWS.hbp` and its `.sha256`;
  - `gen_filing.py`;
  - `c05_c06_edges.py` with `.out`;
  - `nf_scan_filing.py` with `.out` (0 float literals, 0 true divisions, 0 float, fraction or decimal names or imports);
  - `check_lanes.sh` and `verify_names.sh`;
  - `pr45-edges/` (the seven reviewer files, fetched read-only);
  - `MANIFEST-filing.sha256`.
- The evidence is Python integer arithmetic plus re-derivation, so it is SCOPED: it does not stand in for the repo's CI or for the no-float gate on the branch.
