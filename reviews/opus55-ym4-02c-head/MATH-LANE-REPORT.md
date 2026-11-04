**VERDICT: HOLD at 40cc40d226a54bf3362f2d8da7cc51009e69ad0f.** Every theorem, computed value and receipt held. The holds are sentences. H1 to H3 were added by the six-corrections commit 338e298.

**HOLDS** (old → new, with evidence)

- **H1, README.md:15.** `exp(−βN_p) ≤ Z ≤ 1; site` → `exp(−βN_p) ≤ Z ≤ 1 for β ≥ 0; site`. DERIVED: at β<0 the left side exceeds 1. Theorem 1 states β≥0.
- **H2, README.md:15.** `T = A^(1/2) B A^(1/2) positive and trace class,` → `for β > 0, T = A^(1/2) B A^(1/2) positive and trace class,`. Theorem 5 assumes β>0. Remark 7.1 gives a negative eigenvalue at β<0 on odd L.
- **H3, docs/PROOF_OBLIGATIONS.md:9.** `and the transfer operator with Z` → `and, for β > 0, the transfer operator with Z`. Same evidence as H2.
- **H4, docs/LEMMA-0004-REFLECTION-TRANSFER.md:312.** `with six list rows, five for verbatim tools of the second seat, one of those added on this branch, and one for the gate itself.` → `with 28 file rows and 162 listed findings: one for the gate itself, 25 for verbatim tools of the second seat, and two for tests.` MEASURED, locally and hosted: `listed_files=28|listed_findings=162|failed=0`. The old text was true at 338e298 (6 rows).
- **H5, the same file:128.** `GPT-6 asks that a different model family check it as a theorem: OPEN.` → `GPT-6 asked that a different model family check it as a theorem, and verified it on November 4, 2026, under the note's hypotheses: [its report](../reviews/gpt6-sign-and-bridge/README.md).` Evidence: the note's line 3 and comment 6628841208.
- **H6, docs/LEMMA-0003-SUBGROUP-DESIGNS.md.** Its line 41 reads DERIVED.
  - Line 19: `the sharp condition stays OPEN.` → `the sharp condition is the paragraph below on no plane with both sides of 1.`
  - Line 21: `the sharp condition stays OPEN in d ≥ 3.` → `the sharp condition in d ≥ 3 is the paragraph below on no plane with both sides of 1.`
- **H7, the same file:41.** `agreement through t holds for every finite G of strength t, on every lattice and every d,` → `for plaquette monomials of total degree k ≤ t, agreement through t holds for every finite G ≠ {1} of strength t, on every periodic lattice and every d,`. MEASURED: G={1} has t=0, first difference k=1>t, so agreement through 0 holds on 1×1.
- **H8, the same file:99.** `Reflection positivity, the transfer matrix, the renormalization group, the continuum limit and the physical mass gap stay OPEN in the [ledger](PROOF_OBLIGATIONS.md).` → `The renormalization group, the continuum limit and the physical mass gap stay OPEN in the [ledger](PROOF_OBLIGATIONS.md), which holds reflection positivity and the transfer operator at each fixed finite lattice as DERIVED.` Evidence: ledger line 9.
- **H9, README.md:16.** `The conclusion also holds at two sides ≥ 2 or one side ≥ 3.` → `The conclusion also holds at two sides ≥ 2 or one side ≥ 3, given ∏_p w(U_p) ≠ 0 almost everywhere.` DERIVED: take U(1) on (ℤ/3)×(ℤ/1)×(ℤ/1), w = cos θ with w(1) set to 0. The commutator plaquette is 1, so g≡0 and f≡0, while sign w is no ±κ. The note's line 55 carries this hypothesis.
- **H10, reviews/gpt6-sign-and-bridge/README.md:8.** `The counts of 55 million multisets and the 2I replay are the second seat's and FABLE5's, not rerun by GPT-6` → `The counts of 55 million multisets are the second seat's and FABLE5's, which GPT-6 left unrun, and the 2I replay it names is outstanding`. The quote says "outstanding 2I replay", and Lemma 0003 says 2I in d≥3 is unmeasured.
- **H11.**
  - reviews/opus55-site-sign/README.md:27: `The note's status stays DERIVED with independent review OPEN: GPT-6's review is preliminary, and the operator asked for its final check.` → `At this filing the note's status was DERIVED with independent review OPEN, and GPT-6 verified it later on November 4: [its report](../gpt6-sign-and-bridge/README.md).`
  - reviews/fable5-q8-slice-count/README.md:15: `is preliminary, and the operator asked for its final check.` → `was preliminary at this filing, and its final check is [its report](../gpt6-sign-and-bridge/README.md).`
- **H12, reviews/opus55-ym4-02c-last/README.md:5.** `repository, is left out here,` → ``repository, and its 21 files under `run/`, are left out here, each with its hash in `LAST_FILES.hbp`,``. MEASURED: of 100 rows, 78 filed (27 with CRs removed), 22 unfiled.

**WHAT I RAN**

1. **Six corrections.** That folder gives the count of six and omits their text, so I took them from the diff of 338e298.
   - Lemma 0004:260 (row reproduces), :312 list rows (H4), :312 exponents, :473 with :450, README:15 (H1, H2), ledger:9 (H3).
   - Exponents, by my AST scan: 48 literals, 3 len lines, 0 true divisions, 0 float literals.
   - Seven filed scripts rerun, byte-identical to their filed outputs.
2. **My own integer recount, all MEASURED.**
   - Q8 w=0,1,0,0,0: 6 and 0 at T=4 (36,864 literal entries, 0 mismatches), T=6, and T=8 to 14 reduced. DERIVED for every even T≥4, since reachable end pairs stay at 96.
   - Z/6: 18 and 0, with c₃=−1/6.
   - Moved Gram: 3648 blocks, −6351452416 at (0,0,2,3), G_FF=−91/128. Twin: 91/128, 17 positive and 0 negative, Z=69425/16.
   - Patterns, exhaustive on (ℤ/2)²: Q8 8/32, 2T 2/32, 2O 4/256, 2I 2/512 (24,883,200,000 configurations), each equal to the ±homomorphisms.
   - Note lines 57 to 61 reproduce on 29 lattice-group pairs. Its side-link statement agrees on 117 of 117 lattices.
3. **Tests.**
   - All receipts `cmp` identical on LF under Python 3.12.3, and identical after CR removal on Windows 3.13.14: exact, designs, one-by-L, reflection, site-sign.
   - All sabotages exit as named, with 0 tracebacks.
   - Gate scan, compiled check and plants pass. GPT-6's Q8 checker and its 3 mutants behave as filed.
   - Pins and SHA256SUMS: 0 bad.
   - Hosted, all 10 finished: 9 success and 1 failure. The failure is run 41825190517, job `no-float-list-unchanged`, flagging `scripts/FLOAT-EVIDENCE.txt`. `no-float-base` passed in that run. Path filters gave `subgroup-designs` and `gpt6-q8-audit` no run at this commit.
4. **New sentences.**
   - (a) Theorem 5(e) carries the operator's sentence, DERIVED. Sector: the gauge-invariant subspace PH. Hypotheses: β>0, SU(2) Wilson weight, any finite periodic spatial lattice with k≥1. The gap is a property of T_op, independent of N_t, and the theorem gives no size. Exact control at k=1: gap = L·log(l₀/l₁).
   - (b) True as arithmetic, DERIVED. See N2.
   - (c) Route 2 and the other direction re-derived, and I could not break them.
     - Incidence on 73 lattices: m(e)+m(f)≤2 and m(loop)≤1 on all 29 with no such plane; a loop link held twice on all 44 with one.
     - My own forest bound: 0 violations over 381,614 multisets on one-side-1 lattices, with controls firing on the side-1 pairs.
     - First difference: k=2, 3, 4, 6 for Q8, 2T, 2O, 2I; also Dic₃, Dic₆ and Z₂ to Z₆. DERIVED generally, from E_G[χ_n([U,V])] = Σ m_i/d_i.
     - **Exact scope.** Lattices: finite periodic, any d, at most one side equal to 1. Monomials: ∏a_P^{m_P} with Σm_P≤t. Groups: every finite subgroup of SU(2) except {1}, with t=1 (cyclic), 3 (binary dihedral), 5, 7, 11.
     - New evidence: through-plaquette monomials on 1×2×2 with V above the plain bound, 10,296 for 2I, differ=0, while K_m differs from Haar on 49 class pairs at m=6.
   - (d) Table rows 1, 3, 4 and the second note state the quotes. Row 2: H10. First note: N2. Comment section byte-identical to the API (2805 bytes, 10:53:03Z).
5. **Osterwalder–Seiler.** No file at this commit represents the proof as read. MEASURED by grep of tracked text: citations, NAMED, CANNOT_SEE or OPEN throughout. PR #14's body agrees.
6. **Diff reading.** Whole diff read: docs/ (six files), README, PROBLEM, and the new review READMEs. I sampled `reviews/gate-v4` raw rows and `opus55-site-sign/out`, and left the gate code to the other lane.

**NOTES**

- **N1.** `λ₁ OPEN` (README:15, ledger:9, Lemma:5 and :470) sits beside DERIVED 0<λ₁<λ₀. Suggested: "the value of λ₁". Ledger:25's "If a positive lattice gap is found" is now Theorem 5(e).
- **N2.** The family L = L_phys/a omits β(a) (README:7, PROBLEM:34, ledger:29). Neither quote in the GPT-6 report states L_phys/a; it is the builder's gloss on the operator's words. Exact k=1 row along L=n, β=n²: exp(Δ) reads 4.16, 5.33, 4.88, 4.70, 4.58, 4.53 at n=1, 2, 3, 4, 6, 8. Gates 3 to 5 have no finite-scope reading.
- **N3.** The note's CONJECTURE at k≥3 on SU(2) has a pencil proof, DERIVED by this seat with review OPEN, in the derivation file below.
- **N4.** Older status locked by `cmp`: SITE_SIGN_RECEIPT:79-80, ONE_BY_L:20, SUBGROUP_DESIGNS:28, test_haar_moments:120.
- **N5.** Section 10's wording table has no rows for the L=3 sentence or the exponent sentence. Line 1506 is a sum of two len(...).
- **N6.** −6351452416 is the lowest value on a family of two-coordinate test vectors with large coefficients. On e_i±e_j the lowest is −18496.
- **N7.** Z/6's weight reads 25 and 5 at T=6. The lemma scopes it to T=4 correctly.
- **N8, for the float lane.**
  - `reviews/opus55-ym4-02c-last/src/site_center.py:79`, my tool, calls `rnd.sample(slices, 4000)`. CPython's source takes the float log path for k>5, read and not traced. The tool has no list row.
  - README:28 cites 6 of 20, and the last attack read 1 of 40.
  - README:26 names one required check, and live protection requires `no-float`, `no-float-base` and `no-float-compiled`.

**COULD NOT CHECK**

- My original message listing the six holds: CANNOT_SEE.
- Osterwalder–Seiler body: CANNOT_SEE.
- 2I on monomials with plane plaquettes: NOT_MEASURED, BUDGET.
- Q8, 2T and 2O filed multiset rows: totals read only for FOREST, not rerun.
- λ₁ at k≥2: NOT_MEASURED.
- GPT-6's reading: NAMED.
- Float-list acceptance: another lane.

**FILES** under C:/tmp/opus55/head-02c-20261104/math/

- C:/tmp/opus55/head-02c-20261104/math/SHA256SUMS
- C:/tmp/opus55/head-02c-20261104/math/mine/SU2-K3-DERIVATION.txt
- `mine/`: ylib.py, step2_gram.py, step2_moved.py, lemma3_incidence.py, lemma3_first_difference.py, lemma3_through_2i.py, gap_k1.py, note_links.py, records.py, exps_scan.py, compare_comment.py, export_tables.py, export_more.py, forest_sum.py, walk_list.txt, integrity.sh, wsl_run.sh, wsl_compiled.sh, wsl_plants.sh, filed_last.sh, filed_last2.sh, integer_only_audit_fetched.py, rs/walk22.rs, rs/walk_any.rs, tables/
- `runs/`: LOCAL_RUN_ROWS.hbp, step2_gram.hbp, step2_moved.hbp, sign_walk.hbp, sign_walk_any.hbp, lemma3_incidence.hbp, lemma3_first.hbp, lemma3_through.hbp, gap_k1.hbp, note_links.hbp, filed_last.hbp, wsl_run.hbp, wsl_compiled.hbp, wsl_plants.hbp, and each raw test output.
- `repo/` is the clone at the pinned commit, `lf/` its LF export. Build output deleted; workspace 9.3 MB.
