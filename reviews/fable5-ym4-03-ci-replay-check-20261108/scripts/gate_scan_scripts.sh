# The no-float scan over a scratch tree: the proposal's first commit with this lane's scripts and VERIFY.py placed where the folder goes.
set -u
ROOT=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
S=$ROOT/work/scan-scratch
rm -rf $S
git clone -q $ROOT/prop $S
git -C $S checkout -q a5f8cab
mkdir -p $S/reviews/fable5-ym4-03-ci-replay-check-20261108
cp -r $ROOT/check/scripts $ROOT/check/VERIFY.py $S/reviews/fable5-ym4-03-ci-replay-check-20261108/
git -C $S add reviews
cd $S
rc=0
python3 -I -X utf8 scripts/no_float_gate.py . > $ROOT/work/scan-scratch.out 2>&1 || rc=$?
grep "^NO_FLOAT|file=\|NO_FLOAT_DONE" $ROOT/work/scan-scratch.out
echo "SCAN_RC|rc=$rc|json=0"
