# wf_steps.py now reads the workflows with wfread.py; each step folder it writes must equal, byte for byte, the one written earlier with PyYAML.
set -u
ROOT=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
W=$ROOT/work
X=$W/xcheck
rm -rf $X
mkdir -p $X
OUT=$ROOT/check/raw/steps/XCHECK.hbp
: > $OUT
one() {
  name=$1; wf=$2; rundir=$3; old=$4
  python3 -I -B -X utf8 $ROOT/check/scripts/wf_steps.py $wf $rundir $X/$name > /dev/null
  rc=0
  diff -r -x "*.out" $old $X/$name > $X/$name.diff 2>&1 || rc=$?
  echo "XCHECK|name=$name|files=$(ls $X/$name | wc -l)|diff_rc=$rc|json=0" >> $OUT
}
one wfA $ROOT/repo/.github/workflows/one-scale-blocking.yml $W/runA $W/wfA
one wfB $ROOT/main-tree/.github/workflows/one-scale-blocking.yml $W/runB $W/wfB
one wfP $ROOT/prop/.github/workflows/one-scale-blocking.yml $W/runP $W/wfP
G=$W/gates/e4a83d4
one nofloat $G/nofloat/.github/workflows/no_float.yml $G/tmp-nofloat $G/steps-nofloat
one base $G/basejob/base/.github/workflows/no_float_base.yml $G/tmp-base $G/steps-base
one compiled $G/compiled/.github/workflows/no-float-compiled.yml $G/tmp-compiled $G/steps-compiled
cat $OUT
