# The first run of YM4-02e's test: a failed run, kept

**FAILED, on two rows registered before the run.** The rows in [`FIRST-RUN.hbp`](FIRST-RUN.hbp) are its output as it stood, 208 complete lines, with the cut 209th line dropped. Rust is outside this test: Python 3.13 on Windows, at the commit after `23cec81`, as it first ran.

| Row | Registered | Read | Cause |
|---|---|---|---|
| `control_ratio_Z3_dims_3x1` | 428816..428818 ppm | 428817..428818 ppm, inside the interval | The check asked for the same floor and ceil |
| `runtime_within_1500_seconds` | 1,500 s | Stopped by FABLE5 at about 36 minutes, on Z2 at L×2 with L = 4, q = 1/2 | A fallback search on all symmetry blocks, with wide fractions |

Up to where it stopped, no row broke the k-step bound or the locality bound, every closed form matched, and the second seat's five values on Z2 at 2×2 agreed.

The corrected test keeps both as failures of this run, in `YM4_02E_MISS` rows beside the prediction, and a later pass leaves them as they are. It also reads every row here against its own output. Those rows are read by [`tests/test_k_step_locality.py`](../../tests/test_k_step_locality.py), in `section_first_run`.

**Two later attempts, stopped by FABLE5 for run time on one row,** the locality row of Z2 at 2×2×1, solved through the general pencil. Neither had a failed row. [`SECOND-ATTEMPT.hbp`](SECOND-ATTEMPT.hbp) and [`THIRD-ATTEMPT.hbp`](THIRD-ATTEMPT.hbp) hold the 47 rows each reached, recorded in `YM4_02E_ATTEMPT` rows beside the prediction. A start of a few seconds, launched outside the harness, was stopped before it reached any row of note.
