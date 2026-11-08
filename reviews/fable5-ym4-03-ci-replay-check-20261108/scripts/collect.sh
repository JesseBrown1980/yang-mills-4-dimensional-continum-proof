# Copy this lane's raw runs from work/ into check/raw/, the folder the chain seals.
# usage = bash collect.sh
set -eu
ROOT=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
W=$ROOT/work
C=$ROOT/check/raw
mkdir -p $C/steps $C/T $C/main $C/sab/A $C/sab/B $C/logs $C/plants/out $C/instr $C/proposed/sab
cp $W/wfA/STEPS.hbp $C/steps/wfA-STEPS.hbp
cp $W/wfB/STEPS.hbp $C/steps/wfB-STEPS.hbp
if [ -f $W/wfP/STEPS.hbp ]; then cp $W/wfP/STEPS.hbp $C/steps/wfP-STEPS.hbp; fi
cp $W/T/*.hbp $C/T/
cp $W/runA/blocking.out $C/main/A-blocking.out
cp $W/runA/blocking.err $C/main/A-blocking.err
cp $W/runB/blocking.out $C/main/B-blocking.out
cp $W/runB/blocking.err $C/main/B-blocking.err
cp $W/runA/ym4-03-cache/REPLAY-INDEX.hbp $C/main/A-REPLAY-INDEX.hbp
cp $W/runA/ym4-03-cache/REPLAY-INDEX.hbp.sha256 $C/main/A-REPLAY-INDEX.hbp.sha256
cp $W/runA/sab-*.out $C/sab/A/
cp $W/runB/sab-*.out $C/sab/B/
for f in cache-control.out reuse.out reuse.err unknown.out unknown-replay.out unknown-cache.out; do
  if [ -f $W/runA/$f ]; then cp $W/runA/$f $C/main/A-$f; fi
done
if [ -f $W/runB/unknown.out ]; then cp $W/runB/unknown.out $C/main/B-unknown.out; fi
rm -rf $C/logs/lane1 $C/logs/lane2
cp -r $W/logs/lane1 $W/logs/lane2 $C/logs/
for f in $W/logs/A-step-* $W/logs/B-step-*; do cp $f $C/logs/; done
P=$W/plants
for f in PLANTS.hbp STAGE1.hbp RUNS.hbp stage2.log argv-record.err argv-full-twist.out; do
  if [ -f $P/$f ]; then cp $P/$f $C/plants/; fi
done
cp $P/out/*.out $C/plants/out/
cp $P/cache-argv-record/REPLAY-INDEX.hbp $C/plants/argv-record-REPLAY-INDEX.hbp
(cd $P && diff -u $ROOT/repo/tests/test_one_scale_blocking.py argv/tests/test_one_scale_blocking.py > $C/plants/planted-argv-module.diff || true)
for f in power inertia certify; do
  (cd $P && diff -u $ROOT/repo/tests/test_one_scale_blocking.py edit-$f/tests/test_one_scale_blocking.py > $C/plants/planted-edit-$f.diff || true)
done
for s in section_covariance section_loops section_reflection; do
  (cd $P && diff -u $ROOT/repo/tests/one_scale_replay.py unmark-$s/tests/one_scale_replay.py > $C/plants/planted-unmark-$s.diff || true)
done
sed -i "s#$ROOT/##g" $C/plants/*.diff
I=$W/instr
cp $I/*.hbp $C/instr/
cp $I/record.err $C/instr/
cp $I/replay-*.out $C/instr/
cp $I/record.out $C/instr/record.out
if [ -d $W/runP ]; then
  for f in $W/runP/sab-*.out; do cp $f $C/proposed/sab/; done
  for f in blocking.err unmark.out cache-control.out reuse.err; do
    if [ -f $W/runP/$f ]; then cp $W/runP/$f $C/proposed/P-$f; fi
  done
  cp $W/runP/ym4-03-cache/REPLAY-INDEX.hbp $C/proposed/P-REPLAY-INDEX.hbp
  for f in $W/logs/P-step-*; do cp $f $C/proposed/; done
fi
echo COLLECT_DONE
mkdir -p $C/gates
for g in $W/gates/*/; do
  label=$(basename $g)
  if [ -f $g/GATES.hbp ]; then
    cp $g/GATES.hbp $C/gates/$label-GATES.hbp
    for d in steps-nofloat steps-base steps-compiled; do
      for f in $g/$d/step-*.out; do
        if [ -f $f ]; then cp $f $C/gates/$label-$d-$(basename $f); fi
      done
    done
  fi
done
echo COLLECT_GATES_DONE
