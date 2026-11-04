**VERDICT: HOLD at 40cc40d226a54bf3362f2d8da7cc51009e69ad0f.** Three holds, all on text. Nothing is held on a float, pin, count or required check. MEASURED unless tagged.

## HOLDS

**H1.** `docs/LEMMA-0004-REFLECTION-TRANSFER.md:312`
- Old: "with six list rows, five for verbatim tools of the second seat, one of those added on this branch, and one for the gate itself."
- New: "with 28 list rows holding 162 findings at commit 40cc40d: 25 for verbatim tools of the second seat, 16 of those added on this branch, 2 for the tests of Lemma 0003 from main, and 1 for the gate itself. This lemma's test reads 0 findings and imports collections, itertools, math and sys."
- Row: hosted run 41825192994, `NO_FLOAT_DONE|code_files=98|listed_files=28|listed_findings=162|failed=0`. The sentence was true at 338e298.

**H2.** `.github/workflows/no-float-compiled.yml:2`
- Old: "one C++ review file and two Rust review files". New: "one C++ review file and four Rust review files".
- Row: hosted `COMPILED_DONE|cpp_files=1|rust_files=4|failed=0`. This PR adds `brute.rs` and `rp5.rs`.

**H3.** `scripts/FLOAT-EVIDENCE.txt`, reasons only, no pin moves.
- Line 3 old: "The tool counts float literals, true divisions and powers on that tree and prints them, and the tree is only walked". New: "The tool prints the line numbers of float literals and true divisions, the text of powers and of pow, float, complex and round calls, and the math attributes on that tree, and the tree is only walked and unparsed". Source: astscan lines 4-16.
- Line 5 old: "Those lines hold imports and three path strings, and". New: "Those lines hold two comments, imports, three path assignments and two calls of that lambda, the second with a fourth path string, and". The slice holds 4 string constants.
- Line 28 old: "line 221 calls it twice." New: "line 221 calls it once and passes it once to ring_power, which calls it at line 211."

With all five edits in a scratch clone, own gate and base gate both gave rc=0, 28 rows, 162 findings. list-unchanged still names the list alone.

## FLOAT LIST (recommendations; acceptance is the operator's)

- **Reconciled:** blob hash, the gate's reader and `--pins` match 28/28 rows.
- **Kinds:** 1 gate rule tables, 25 verbatim reviewer tools, 2 builder tests.
- **Authorship:** NAMED by FILED.hbp, READMEs and scratch paths. The hash lists match on all 25, and FILED delivered hash equals the blob on 14, CR 0.
- **Trace:** I ran every `**`, two-argument pow, `/`, exec and literal_eval through a checker. 22 runs, 117 power sites, 2,038,545 calls: 0 negative or non-int exponents, 0 float results, and every flagged power line ran. Where a tool's output feeds a Lemma 0003 or 0004 cell, or a test feeds a receipt, the path carries ints.

| path | findings | rec | reason |
|---|---|---|---|
| scripts/no_float_gate.py | 93 | ACCEPT | 86 strings; ast.parse 2; Formatter 1; imports 4; prints counts |
| reviews/opus55-site-sign/code/astscan.py | 1 | ACCEPT | test parsed as data; H3 |
| reviews/opus55-site-sign/code/cube_and_cycles.py | 2 | ACCEPT | exponents 2..10; byte-equal |
| reviews/opus55-site-sign/code/decode.py | 1 | ACCEPT | exec slice 0 findings; prints nothing; H3 |
| reviews/opus55-site-sign/code/mutants_auto.py | 3 | ACCEPT | test parsed as data; traced, not run |
| reviews/opus55-site-sign/code/run_gates.py | 3 | ACCEPT | prints counts; traced; third count reproduced |
| reviews/opus55-site-sign/code/side_one.py | 1 | ACCEPT | exponents 2..7, budget test; byte-equal |
| reviews/opus55-site-sign/code/zeros_srp.py | 4 | ACCEPT | exponents 1..81; byte-equal |
| reviews/opus55-ym4-02b/beta12_values.py | 1 | ACCEPT | 200 int lines; 2 filed rows reproduced |
| reviews/opus55-ym4-02b/confirm-last/filed_cells.py | 2 | ACCEPT | exponents 1..200; 47/48 rows filed, one reads my stub |
| reviews/opus55-ym4-02b/confirm-last/mckay_check.py | 2 | ACCEPT | exponents 1..12; 30/30 rows filed |
| reviews/opus55-ym4-02b/designs_explicit.py | 3 | ACCEPT | exponents 0..12; byte-equal |
| reviews/opus55-ym4-02b/first_diff_t2.py | 2 | ACCEPT | exponents 1..14; byte-equal |
| reviews/opus55-ym4-02b/haarpoly.py | 1 | ACCEPT | exponents 1..2; six importers through expect_words |
| reviews/opus55-ym4-02b/sphere_q8.py | 8 | ACCEPT | slices 0 findings; 200 int lines; byte-equal |
| reviews/opus55-ym4-02b/stretch_b11.py | 2 | ACCEPT | exponents 0..10; int lines; byte-equal |
| reviews/opus55-ym4-02b/stretch_b13.py | 2 | ACCEPT | exponents 0..10; int lines; byte-equal |
| reviews/opus55-ym4-02c-last/src/exps.py | 1 | ACCEPT | named file parsed; prints text |
| reviews/opus55-ym4-02c-last/src/recount.py | 2 | ACCEPT | exponents 1..5; byte-equal |
| reviews/opus55-ym4-02c/recheck/src/inertia_check.py | 3 | ACCEPT | function 0 findings; byte-equal |
| reviews/opus55-ym4-02c/src/cyl.py | 3 | ACCEPT | exponents 1..9; byte-equal |
| reviews/opus55-ym4-02c/src/exact.py | 1 | ACCEPT | n−k from n to 0; 66,012 calls |
| reviews/opus55-ym4-02c/src/gram12.py | 2 | ACCEPT | exponent 3; histogram hash reproduced; byte-equal |
| reviews/opus55-ym4-02c/src/rp4d.py | 1 | ACCEPT | exponents 6, 8; `single` rows inside filed |
| reviews/opus55-ym4-02c/src/su2num.py | 2 | ACCEPT | exponents 0..187; no filed output |
| reviews/opus55-ym4-02c/src/transfer.py | 9 | ACCEPT | exponents 1..11; both parts byte-equal |
| tests/test_one_by_l_2d.py | 3 | ACCEPT | integer closure `times`; receipt byte-equal; H3 |
| tests/test_subgroup_designs_4d.py | 4 | ACCEPT | exponents 0..10; receipt byte-equal |

## Main against this commit

Main's 12 rows become 28: 16 added, 0 changed, 0 removed. All 16 name files this PR adds, and each exists because gate 935bd77b reads findings there. Findings go 123+39=162: site-sign 15, 02c-last 3, recheck 3, src 18.

## Trusted gate

**Builder's claim holds.** Gate sha256 is 935bd77b at the head blob, the main blob and hosted `NO_FLOAT_BASE`. `no_float.yml`, `no_float_base.yml`, `no-float-compiled.yml` and `no_float_compiled.sh` are byte-equal to main.

**Head against main:** only `reflection-transfer.yml` and `site-sign.yml` are added. Both use path filters and `contents: read`, and their job names differ from every required name.

**All 9 workflows:** 0 `continue-on-error`, 0 `if:`, 0 `|| true`. Required workflows hold no path filter.

**Against b302549:**
- `no-float.yml` became `no_float.yml`: same job and `pull_request`, adds push to main, drops workflow_dispatch, moves to ubuntu-24.04, pins checkout (tag v4.2.2, read by API), widens plants. Clock and Fraction plants live in the selftest.
- New: `no_float_base.yml` (pull_request_target) and `no-float-compiled.yml`.
- Gate 86d779b7→935bd77b: old plants 85/85 flagged. On the tree, 0 files flagged by old only, 19 by new only. Loosened: `struct` by format rule, `math.prod`, ten `time` names.

DERIVED: nothing here weakens a required check after merge.

## list-unchanged

Job 126558014729 flags exactly `path=scripts/FLOAT-EVIDENCE.txt`, fork 762925b, reproduced locally. That change is the 16 added rows, with the header unchanged.

## Gate runs and plants

- **CI commands, on 3.13.14 and 3.12.12:** selftest 124/158/91/59/14 failed=0; scan 98/28/0/162 failed=0; workflow plant step rc=0. Hosted logs match.
- **Red:**
  - float in a listed file: count_moved and pin_moved
  - same-count swap and comment-only edit: pin_moved alone
  - copy at a new path, new .py, new .rs: file=
  - row removed, three kinds: file=
  - edited count or pin, missing file, emptied reason, deleted file, symlink: red
  - row twice: red on rerun; my first attempt was a harness failure, not a finding
  - fullwidth `float`, `2 ** ~0`, walrus exponent: red
- **Passed, own and base gate rc=0:** float with its row repinned; new file with its own row; a gate rule removed with its row repinned. Only the non-required list-unchanged flags these.
- **Passed, compiled script edited:** list-unchanged does not name it.
- **Passed, new files (own gate only):** child process, awk, `s % v`, Random.sample, assertAlmostEqual, decimals in data and markdown, unstaged file.

## Theorem receipts

- **Theorem 5:** `tests/test_reflection_transfer_4d.py` → `tests/REFLECTION_TRANSFER_RECEIPT.txt`. Imports collections, itertools, math, sys.
- **Sign theorem:** `tests/test_site_sign_4d.py` → `tests/SITE_SIGN_RECEIPT.txt`. Adds os, time, tokenize; reads prediction rows and its own tokens.

Neither file holds a row, and nothing they import does. Both read 0 findings. Both receipts are byte-equal under the checker, at 37 and 14 power sites, 0 bad. Listed tools feed second-seat table cells only.

## NOTES

- `README.md:26` reads as one required check; protection requires three. Replace "the check `main` requires," with nothing, and add "`main` requires all three."
- `docs/PREDICTION-YM4-02c.hbp` rows 135 and 170 stop at six rows. Append a dated row beside them with 28/162.
- list-unchanged is not required and protection holds no review rule. The PR reads MERGEABLE/UNSTABLE, so "a person must read" rests on the operator.
- `no-float-compiled` runs the change's own script, unwatched by list-unchanged. This is on main.
- The Actions policy in `no_float_base.yml`'s comment: CANNOT_SEE. `actions/permissions` shows no path list. DERIVED: a block leaves the required check pending.
- 0 workflows check `reviews/opus55-ym4-02c-last/SHA256SUMS`; local `sha256sum -c` passes.
- `integer_only_audit.py` reads 0 on the reflection test, as the lemma says. It hits 4 lines on the site-sign test, substrings `:f`/`:e` in `%d` row text. No doc claims that tool there.
- Filed `beta12_values.out` holds 2 rows and no DONE row; the tool prints more.
- `strict=true`: a move on main forces a new head, so approval binds a SHA.
- Gate docstring lines 99-100 still say hosted NOT_MEASURED; hosted rows exist. It is frozen with the pin.

**Falsifier:** any row's blob hash or gate count differing at this commit, or a run with a negative exponent at a flagged line.

## RAN

- Rust: `brute.rs` rebuilt on 1.81; `brute gram12` regenerated sha256 4bb408bd, equal to the held row.
- Also read: hosted logs, branch protection, a differential of the old and new gate, the import graph of all 93 Python files, and a decimal scan of 211 rows files (7 tokens, runner names and a citation; dot-joined witness lists excluded).

## COULD NOT CHECK

- Scratch copies named in rows are gone: CANNOT_SEE. Evidence is held hashes and reproduced outputs.
- `mutants_auto`, `run_gates`: traced, not run.
- `beta12_values`: stopped at my 281 s budget, rc=124.
- `rp4d`: `single` part only.
- Compiled check: hosted rows only.
- Linux lane: hosted logs only; local runs on Windows.

## FILES

Under `C:/tmp/opus55/head-02c-20261104/gate/`:
- `FLOAT-LIST-RECONCILE.hbp`, `FLOAT-LIST-RECONCILE.hbp.sha256`
- `out/plants.hbp`, `out/plants2.hbp`, `out/row_claims.hbp`, `out/row_findings.hbp`, `out/gate_diff.hbp`, `out/import_graph.hbp`, `out/sums_check.hbp`, `out/decimals.hbp`, `out/misc_measures.hbp`, `out/row_history.hbp`, `out/run/`
- `tools/`
- `repo/` (clone, clean)
