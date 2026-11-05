# The second seat's attack on YM4-03, at `6c87200`

Three lanes, read and run only, each sharing no code with the test: [the proofs](proofs/REPORT.txt), [the test and its controls](test/REPORT.txt), and [the text against the rows](text/REPORT.txt). Each folder holds the lane's report, its findings and its holds, verbatim. [`HOLDS-APPLIED.hbp`](HOLDS-APPLIED.hbp) gives each of the 98 holds its disposition: applied as held, or merged where two lanes held the same text.

**What it read:** no theorem's core refuted. Theorem 9 confirmed, with b = 3 read on lattices for the first time, and a term the note did not state, the thin tube at b ≥ 4. Two clauses of Theorem 7, item 3, refuted as written, with an exact repair. Theorem 13's proof reached less than its conclusion, with an exact repair. 95 mutants of the test: 42 killed on a named check, 16 caught only by the workflow's cmp, 32 survived, 3 crashed, 2 hit the lane's time limit.

**Its code:** the lanes' scripts and their run outputs are in `opus55-ym4-03-attack-20261105-tools.tar.gz`, sha256 `21ac045d1f4dec2a4a8ea32c8660c5779ec36d0ef7255900be46239cf9b7fb2c`, on this seat's backup drive, for the second seat's store. Python here imports exact-rational modules that this repository's gate lists by name, so the code stays outside the tree and the reports stay in it.
