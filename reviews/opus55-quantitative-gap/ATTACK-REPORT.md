**VERDICT: HOLD at f7a3dbc.** The statement itself stands. I found no falsifier and no step that fails. The proof has one citation gap (H4), and the record and test claims need the corrections below.

## HOLDS

The exact old and new text is in `HOLDS.txt`. `write_holds.py` checked all 16 old strings at their stated lines: 16 of 16 match.

- **H1, "every row met" is false at this commit.** MEASURED.
  - Locations: `tests/test_quantitative_gap.py:556`, note:87, note:3, `README.md`:17, and new row(s) after the 36 pinned rows in the prediction (H2c).
  - The gate clause of prediction row 35 failed: `[sys_modules] .modules at line 556`, `failed=1`, locally and in hosted run 41840421497. That run skipped the test's own steps.
  - The required checks no-float and no-float-base are red here.
  - FABLE5's local "failed=0" read 28 files, before the test was tracked. Hosted read 29.
  - c64eed3 fixes it: run 41841734786 is green, with the receipt byte-equal and sabotage counts 21, 13, 22, 3.
- **H2, "GPT-6 read the proof, verified it" is overstated.** MEASURED from the session transcript. Locations: note:3, `README.md`:17, prediction beside row 1.
  - Sketch sent 12:17, relay received 12:39:44, note first written 12:48:42.
  - The sketch has no Step 3 and no [m, M] form. The report says "Independent proof", for SU(2) Wilson.
  - The general weight and Step 3 as written have no other-family reader yet.
- **H3, "Sharp in this generality" (note:71).** It is shown only at N_ℓ=1. DERIVED and MEASURED:
  - Equality holds exactly when N_ℓ=1 and G has a closed index-2 subgroup, with w two-valued on it. Either orientation works, and the reversed one gives μ=−τλ₀.
  - For N_ℓ≥2 the inequality is strict on every weight.
  - SU(2) is connected, so it is strict at every β>0.
- **H4, |θ|<1 (note:52, 80).** Theorem 5(d) as written uses λ₀=‖T‖ and "strictly below", at T≥0. Negative μ needs one line, supplied in the replacement. DERIVED.
- **H5, "This seat read those statements" (note:79).** MEASURED: FABLE5 ran one WebSearch and fetched neither paper. I opened both (see Attack 1).
- **H6, stale scope (note:5, `README.md`:17, `PROOF_OBLIGATIONS.md`:9).** MEASURED.
  - PR #14 merged at e7a12fc (15:00:20Z), after this commit.
  - PR #22 now reads CONFLICTING on `PROOF_OBLIGATIONS.md`.
- **H7, `A_cancels=1` cannot fail (note:119).** MEASURED: with a[i]=i²+7 in place of A, the rows stay byte-equal to the receipt.
- **H8, review README:3.** MEASURED: only the column's heading was lost. The values 0.2, 0.5, 0.8 came through, and "exactly" means six printed digits. FABLE5's reading q=exp(−2β) is right: τ rounds to 999995, 992218, 712663, and the 4×1 lattice reads 995106, 624404, 138840 ppm, so the lattice is 2×2.

## NOTES, by attack item

**1. Proof**
- Steps 1 to 4 hold, including loops, repeated links, μ=0, multiplicity, negative θ and both routes. DERIVED.
- Theorem 2.9 of Lemmens–Nussbaum (arXiv 1304.7921, p.9) applies with C taken together with 0, and it covers SU(2).
- Reeb–Kastoryano–Wolf (arXiv 1102.5170) Theorems 4 and 5 are finite-dimensional. Theorem 5 is the eigenvalue bound itself.
- A proof without Birkhoff, by total variation plus a small linear program, is in `DERIVATIONS.txt` §2. DERIVED.

**2. Hypotheses**
- The class-function hypothesis is unused on H and only gives gauge invariance. Symmetry only gives self-adjointness: the asymmetric Z3 kernel still satisfies ratio²=1/7≤9/25. MEASURED.
- "Every real β" is right in the τ form, τ=tanh(|β|N). The literal display fails at β<0: Z2 on 2 links with w=1,4 reads ratio 9/25 against a negative tanh. MEASURED.
- Wilson reduces correctly to m, M, tanh. DERIVED.

**3. Search**
- 38,367 exact cases: 0 violated, 0 undecided. 30,030 of them are tallied by verdict.
- 1,348 equal cases, all N=1, all in the H3 family.
- 12,892 tallied cases with N≥2: 0 equal.
- Closest approach is measured as n_eff, the n for which τ with exponent n equals the ratio:
  - S3 1×1, weights 1, 2, 2¹⁶⁰: n_eff=1.972 of 2, with (1−τ)/(1−ρ) steady at 0.045.
  - S3 1×1×1, weights 2, 1, 2¹²⁸: n_eff=2.946 of 3.
  - With T≥0: largest share 1/2, on Z2 L×1.
  - The Wilson form on Q8 and 2T, at r down to 1/256: at most 0.25.
  - SU(2) on one link, nine β: at most 0.249.
- τ is the exact supremum over arbitrary positive multipliers A. DERIVED, §7.

**4. Test**
- The pencil is correct. DERIVED §1, and matched by a separate route (characteristic polynomial plus Descartes):
  - 7 of 7 exact rows, including characters and H products.
  - 11 of 11 plaquette rows.
  - 3 of 3 full-space rows.
- New MEASURED values:
  - Q8 1×1×1: 582784..582785 ppm, which can fill the "certificate alone" cell.
  - Z3 2×2: 73035..73036 ppm.
- 26 mutants:
  - 10 killed by a predicted row.
  - 3 pass the script and only the receipt differs: A inverted, dropped fourth inverse, Route 1 run on orbits.
  - 13 survive: 12 weaken a checker, and 1 (wrong plaquette word order) is equivalent on the filed lattices.
- A inverted is invisible because the only pinned plaquette ratios are Z2 2×2, where a staggered flip makes T(A) and T(A⁻¹) isospectral. DERIVED §4.
- `drop_spatial_weight` fails only those 3 rows, so A on Z3, S3, Q8 and 2T is pinned by the self-recorded receipt alone. My engine confirms those values, so no real error is present.
- All filed rows have T≥0, so the certificate's negative side never reads anything. Suggested control: Z2 with w=1/4,1, which has μ=−3/8 and equality.
- On the three filed Route 1 lattices, H ratio equals PH ratio. Line 67 is true at other lattices: Z2 q=1/2 on 2×2 reads 0.345580 on H and 0.146218 on PH. MEASURED.
- No row has four distinct links in a word where order matters. Z3 2×2 is that case, and I ran it.

**5. Record**
- Prediction before test: true, by seconds. Branch created 12:50:43Z at 9d1c334. The test file reached disk about 3 s later and first ran at 12:52:19. The receipt equals that run.
- The report is verbatim except the first line "Worked for 4m 19s", table padding and the last newline.
- Note tables equal the receipt, 18 of 18 rows.
- "Seen after the run" is true on every case it names. The Z2 equality holds at every L, by formula.
- The workflow is not a required check: the required ones are the three no-float gates.

**6. Limit and diameter**
- 2exp(−2βN_ℓ) is right. The note leaves unstated the condition 2βN_ℓ−log(1/a)→∞, which holds for β bounded below. DERIVED §6.
- Law: largest cross-ratio=(Zmax/Zmin)² for abelian G. DERIVED, 27 of 27 against direct.
- For any G with a central W: Δ≥2log(Z(1)/Z(W)). DERIVED.
- On a circle Δ falls to 0: tanh(Δ/4) equals the exact ratio on Z2 to L=12, and Q8 reads 256, 7.6, 2.16, 1.33. MEASURED.
- With a side-1 direction, Δ is about half of log R. MEASURED.
- On the 2D torus Δ grows linearly in sites: log₂ lower bound 0.75, 1.81, 3.13, 5.09, 7.75 at L=2..10, q=1/2, and share 683 ppm flat at q=4/5. MEASURED.
- Q8 ladder lower bound also grows, about 5% of log R. MEASURED.
- So the true diameter improves the constant and keeps the exponential form in d≥2. For d≥3 and SU(2) that is CONJECTURE.
- Iterates do converge: tanh(Δ(T^k)/4)^(1/k) reads 467776, 273970, 200288, 171131, 158185 ppm at k=1, 2, 4, 8, 16, against 146218. MEASURED.

## WHAT I RAN

- The test at f7a3dbc: exit 0, receipt byte-equal, 351 s.
- The gate, 26 mutants, 4 sabotages plus the unknown name (21, 13, 22, 3, exit 2).
- Own engine: `recompute.py`, `search.py` stages A to E, `trend.py`, `diameter.py`.
- Hosted logs read with gh.
- Own code is integers only (scanned for floats and true division). The transcript readers use `json` to read only.
- WSL touched: no. Pushes: none.

## COULD NOT CHECK (CANNOT_SEE or NOT_MEASURED)

- What the operator actually pasted to GPT-6.
- Any model reasoning before the prediction, beyond tool calls. "By hand" stays NAMED.
- The bodies of Birkhoff 1957 and Eveson 1995.
- Q8 on 2×2 orbit matrix (8⁸ configurations): BUDGET.
- The own engine on hosted Linux: it ran on Windows Python 3.13.14 only.
- Fabric and recall: not queried.
- Stage D on abelian lattices was killed by its timeout and is uncounted. Its rows carried no alert.

## FILES

All under `C:/tmp/opus55/gap-02d-20261104/opus/`:
- `HOLDS.txt`
- `DERIVATIONS.txt`
- `SECOND-SEAT.hbp`
- `SHA256SUMS.txt`
- `out/` (all rows)
- `engine.py`, `search.py`, `recompute.py`, `trend.py`, `diameter.py`, `mutate.py`, `record_check.py`, `write_holds.py`, `h22.py`, `s3b.py`, `relay_diff.py`

Clone: `C:/tmp/opus55/gap-02d-20261104/repo`, at f7a3dbc, unchanged. Workspace is 5.0 MB.
