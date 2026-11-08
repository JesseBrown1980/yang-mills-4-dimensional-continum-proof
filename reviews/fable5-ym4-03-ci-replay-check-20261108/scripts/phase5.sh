set -u
cd /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
ROOT=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
I=$ROOT/work/instr
R=$ROOT/check/scripts/run_timed.py
instr_replays() {
  for name in reversed_order shifted_endpoint dropped_inverse theta_no_inverse wrong_convolution_power wrong_first_coefficient extra_plaquette_factor wrong_block_shell twist_every_link flux_wrong_sign overlap_skips_next visibility_ignores_omega_error visibility_error_halved visibility_error_inflated overlap_one_power; do
    rc=0
    (cd $ROOT/repo && python3 -I -B -X utf8 $ROOT/check/scripts/instrument.py $I/replay-$name.hbp tests/one_scale_replay.py replay $ROOT/work/runA/ym4-03-cache sabotage=$name > $I/replay-$name.out 2>&1) || rc=$?
    echo "RUN|name=instrumented_replay_$name|rc=$rc|out_sha256=$(sha256sum $I/replay-$name.out | cut -d' ' -f1)|json=0" >> $I/RUNS.hbp
  done
}
proposed_workflow() {
  python3 -I -B -X utf8 check/scripts/wf_steps.py prop/.github/workflows/one-scale-blocking.yml $ROOT/work/runP work/wfP > /dev/null
  mkdir -p work/runP
  for k in 1 3 4 5 6 7; do
    python3 -I -B -X utf8 $R one P-step-$k $ROOT/prop $ROOT/work/wfP/step-$k.sh work/T/proposed.hbp work/logs
  done
}
instr_replays &
proposed_workflow &
wait
echo PHASE5_DONE
