set -u
cd /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
ROOT=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
I=$ROOT/work/instr
mkdir -p $I
instr_record() {
  rc=0
  (cd $ROOT/repo && python3 -I -B -X utf8 $ROOT/check/scripts/instrument.py $I/record.hbp tests/one_scale_replay.py record $I/cache seeds=tests/ONE_SCALE_BLOCKING_BRACKETS.hbp > $I/record.out 2> $I/record.err) || rc=$?
  echo "RUN|name=instrumented_record|rc=$rc|stdout_sha256=$(sha256sum $I/record.out | cut -d' ' -f1)|json=0" >> $I/RUNS.hbp
}
plants_stage2() {
  python3 -I -B -X utf8 check/scripts/plants.py $ROOT $ROOT/work/plants/PLANTS.hbp stage2 > $ROOT/work/plants/stage2.log 2>&1
  echo "RUN|name=plants_stage2|rc=$?|json=0" >> $I/RUNS.hbp
}
instr_record &
plants_stage2 &
wait
cat $I/RUNS.hbp
echo PHASE4_DONE
