set -u
cd /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
P=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/work/plants
python3 -I -B -X utf8 check/scripts/plants.py /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108 $P/STAGE1.hbp stage1
record_planted() {
  rc=0
  (cd $P/argv && python3 -I -B -X utf8 tests/one_scale_replay.py record $P/cache-argv-record seeds=tests/ONE_SCALE_BLOCKING_BRACKETS.hbp > $P/argv-record.out 2> $P/argv-record.err) || rc=$?
  echo "RUN|name=argv_record|rc=$rc|stdout_sha256=$(sha256sum $P/argv-record.out | cut -d' ' -f1)|json=0" >> $P/RUNS.hbp
}
full_planted_twist() {
  rc=0
  (cd $P/argv && python3 -I -X utf8 tests/test_one_scale_blocking.py sabotage=twist_every_link > $P/argv-full-twist.out 2>&1) || rc=$?
  echo "RUN|name=argv_full_twist|rc=$rc|out_sha256=$(sha256sum $P/argv-full-twist.out | cut -d' ' -f1)|json=0" >> $P/RUNS.hbp
}
record_planted &
full_planted_twist &
wait
cat $P/RUNS.hbp
echo PHASE3_DONE
