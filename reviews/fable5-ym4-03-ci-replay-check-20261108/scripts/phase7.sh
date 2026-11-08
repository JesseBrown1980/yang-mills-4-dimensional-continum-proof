# Rerun of the plants and the instrumented runs with the scripts as they go into the repository (no runpy, frames or yaml).
set -u
cd /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
ROOT=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
I=$ROOT/work/instr
mkdir -p $I
plants_lane() {
  python3 -I -B -X utf8 check/scripts/plants.py $ROOT $ROOT/work/plants/STAGE1.hbp stage1 > $ROOT/work/plants/stage1.log 2>&1
  python3 -I -B -X utf8 check/scripts/plants.py $ROOT $ROOT/work/plants/PLANTS.hbp stage2 > $ROOT/work/plants/stage2.log 2>&1
  echo "RUN|name=plants_stage2|rc=$?|json=0" >> $I/RUNS.hbp
}
instr_lane() {
  rc=0
  (cd $ROOT/repo && python3 -I -B -X utf8 $ROOT/check/scripts/instrument.py $I/record.hbp tests/one_scale_replay.py record $I/cache seeds=tests/ONE_SCALE_BLOCKING_BRACKETS.hbp > $I/record.out 2> $I/record.err) || rc=$?
  echo "RUN|name=instrumented_record|rc=$rc|stdout_sha256=$(sha256sum $I/record.out | cut -d' ' -f1)|json=0" >> $I/RUNS.hbp
  for name in reversed_order shifted_endpoint dropped_inverse theta_no_inverse wrong_convolution_power wrong_first_coefficient extra_plaquette_factor wrong_block_shell twist_every_link flux_wrong_sign overlap_skips_next visibility_ignores_omega_error visibility_error_halved visibility_error_inflated overlap_one_power; do
    rc=0
    (cd $ROOT/repo && python3 -I -B -X utf8 $ROOT/check/scripts/instrument.py $I/replay-$name.hbp tests/one_scale_replay.py replay $ROOT/work/runA/ym4-03-cache sabotage=$name > $I/replay-$name.out 2>&1) || rc=$?
    echo "RUN|name=instrumented_replay_$name|rc=$rc|out_sha256=$(sha256sum $I/replay-$name.out | cut -d' ' -f1)|json=0" >> $I/RUNS.hbp
  done
}
plants_lane &
instr_lane &
wait
echo PHASE7_DONE
