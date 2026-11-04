# The second seat's attack on YM4-02d, at `f7a3dbc`

**Its verdict, in [its report, verbatim](ATTACK-REPORT.md): HOLD at the commit, with the statement standing.** It found no falsifier and no step that fails. Its holds correct the record, add one line of proof for negative eigenvalues, and sharpen the statement on equality.

| What it did | Result |
|---|---|
| Searched for a falsifier | 38,367 exact cases, 0 violated, 0 undecided. Of those tallied by verdict, 1,348 are equal, all at N_ℓ = 1 on an index-2 subgroup, and 12,892 have N_ℓ ≥ 2, with 0 equal |
| Attacked the proof | Steps 1 to 4 hold, with loops, repeated links, μ = 0, multiplicity, negative θ and both routes. It opened Lemmens and Nussbaum, and Reeb, Kastoryano and Wolf |
| Gave a proof of its own | Total variation and a small linear program, with no citation: [`DERIVATIONS.txt`](DERIVATIONS.txt), section 2. FABLE5 read it step by step, and it is in [the note](../../docs/NOTE-YM4-02d-QUANTITATIVE-GAP.md) |
| Ran its own route through the test's rows | A characteristic polynomial and Descartes: 7 of 7 exact rows, 11 of 11 plaquette rows, 3 of 3 full-space rows |
| Ran the test at `f7a3dbc` | Exit 0, receipt byte-equal, 351 s |
| Ran mutants | 26: 10 killed by a predicted row, 3 changing the receipt alone, 13 surviving, of which 12 weaken a checker and 1 is equivalent on the filed lattices |

## What was applied

Every hold in [`HOLDS.txt`](HOLDS.txt), in its text, in the commit after `c64eed3`. H1a is `c64eed3` itself. H6c is the merge conflict, resolved as it wrote. FABLE5's two changes: H5 reads FABLE5 where it read "this seat", and H3 names the second seat beside its first DERIVED.

Its notes acted on, with FABLE5's wording, in the note: the second proof and the multipliers, the condition on the limit line, τ = tanh(|β|N_ℓ) for negative β, the test's reach, its two new ratios, and the true diameter.

## Open

- A different model family's reading of the general weight and of Step 3 as written.
- The controls it names: a plaquette ratio pinned on Z3, S3, Q8 and 2T, a row with a negative eigenvalue, and Z3 on 2×2.
- The bodies of Birkhoff 1957 and Eveson 1995: CANNOT_SEE. Q8's orbit matrix on 2×2, with 8⁸ configurations: BUDGET. Its engine on hosted Linux: it ran on Windows Python 3.13.14 alone.
- Stage D of its search on abelian lattices was killed by its timeout and is uncounted, and its rows carried no alert.

## Its files

`rows/` holds its row files, with CRs removed, and `SHA256SUMS` covers this folder. Its tools and transcript readers would add list rows here, since 14 of its 20 scripts carry gate findings, among them unproven exponents and `import json`. They are held on this machine at `D:/safety-backups/opus55-gap-02d-20261104-tools.tar.gz`, 91 files, SHA-256 `3fc462fbc72701df923df1b2749f1686dfc4dfa64aa412f417c1330dc3bf09d5`, and their upload to the Hugging Face dataset is OPEN.
