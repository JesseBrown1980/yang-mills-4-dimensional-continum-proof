# The first run of YM4-02e's test: a failed run, kept

**FAILED, on two rows registered before the run.** The rows in [`FIRST-RUN.hbp`](FIRST-RUN.hbp) are its output as it stood, 208 complete lines, with the cut 209th line dropped. Rust is outside this test: Python 3.13 on Windows, on the test as it first ran, written at 17:48:51Z after `23cec81` and started at 17:49:08Z. That version stayed uncommitted: the first commit holding the test, `f818bc5`, already reads the interval as a containment. [The version as first written](test_k_step_locality_as_first_written.py), recovered from the session transcript, has the check that asked for the same floor and ceil.

| Row | Registered | Read | Cause |
|---|---|---|---|
| `control_ratio_Z3_dims_3x1` | 428816..428818 ppm | 428817..428818 ppm, inside the interval | The check asked for the same floor and ceil |
| `runtime_within_1500_seconds` | 1,500 s | Stopped by FABLE5 at about 36 minutes, on Z2 at L×2 with L = 4, q = 1/2 | A fallback search on all symmetry blocks, with wide fractions |

Up to where it stopped, no row broke the k-step bound or the locality bound, every closed form matched, and the second seat's five values on Z2 at 2×2 agreed.

The corrected test keeps both as failures of this run, in `YM4_02E_MISS` rows beside the prediction, and a later pass leaves them as they are. It also reads every row here against its own output. Those rows are read by [`tests/test_k_step_locality.py`](../../tests/test_k_step_locality.py), in `section_first_run`.

**Two later attempts, stopped by FABLE5 for run time on one row,** the locality row of Z2 at 2×2×1, solved through the general pencil. Neither had a failed row. [`SECOND-ATTEMPT.hbp`](SECOND-ATTEMPT.hbp) and [`THIRD-ATTEMPT.hbp`](THIRD-ATTEMPT.hbp) hold the 47 rows each reached, recorded in `YM4_02E_ATTEMPT` rows beside the prediction. A start of a few seconds, launched outside the harness, was stopped before it reached any row of note.

**A fourth attempt ran to the end and FAILED its run-time row,** at 1,863 s against 1,500 s, with every other check passing: [`FOURTH-ATTEMPT.hbp`](FOURTH-ATTEMPT.hbp). The fifth, [`FIFTH-RUN.hbp`](FIFTH-RUN.hbp), with each search seeded by an integer estimate and each bracket still decided by exact inertia, finished at 571 s on the same machine with no failed row. The sixth, with the second seat's checks added, is [the receipt](../../tests/K_STEP_LOCALITY_RECEIPT.txt), at 615 s, losing no row of the fifth and gaining 3. Between the fourth and the fifth, the rows differ by the added scope fields and characteristic-polynomial rows, and the run-time and closing rows.
