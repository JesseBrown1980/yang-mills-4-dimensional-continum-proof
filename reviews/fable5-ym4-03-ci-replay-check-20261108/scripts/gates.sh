# The three checks main requires, run as their workflows run them, each in clones of its own inside this lane's folder.
# usage = bash gates.sh LABEL SOURCE_REPO HEAD_SHA
# no-float: the head's no_float.yml, every run step in a clone at HEAD_SHA. no-float-base and no-float-list-unchanged: the base's no_float_base.yml
# (pull_request_target runs the base branch's copy), with base/ at bf58ab2 and head/ at HEAD_SHA. no-float-compiled: the head's no-float-compiled.yml.
# GATE_DIR=scripts as the workflows set it. Each step is a GATE row with its exit code. Integers only, json=0.
set -u
LABEL=$1
SRC=$2
HEAD_SHA=$3
BASE_SHA=bf58ab272d2713c5e79d06005f6cfd1226763ed4
ROOT=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
G=$ROOT/work/gates/$LABEL
ROWS=$G/GATES.hbp
rm -rf "$G"
mkdir -p "$G"
export GATE_DIR=scripts
run_steps() {
  job=$1
  cwd=$2
  steps=$3
  shift 3
  for k in "$@"; do
    rc=0
    (cd "$cwd" && bash --noprofile --norc -eo pipefail "$steps/step-$k.sh") > "$steps/step-$k.out" 2>&1 || rc=$?
    name=$(sed -n "s/^STEP|k=$k|job=[^|]*|name=\([^|]*\)|.*/\1/p" "$steps/STEPS.hbp")
    echo "GATE|label=$LABEL|job=$job|k=$k|rc=$rc|name=$name|out_sha256=$(sha256sum "$steps/step-$k.out" | cut -d' ' -f1)|json=0" | tee -a "$ROWS"
  done
}
# no-float
git clone -q "$SRC" "$G/nofloat"
git -C "$G/nofloat" checkout -q "$HEAD_SHA"
python3 -I -B -X utf8 "$ROOT/check/scripts/wf_steps.py" "$G/nofloat/.github/workflows/no_float.yml" "$G/tmp-nofloat" "$G/steps-nofloat" > /dev/null
mkdir -p "$G/tmp-nofloat"
run_steps no-float "$G/nofloat" "$G/steps-nofloat" 1 2 3
# no-float-base, from the base commit's workflow
mkdir -p "$G/basejob"
git clone -q "$SRC" "$G/basejob/base"
git -C "$G/basejob/base" checkout -q "$BASE_SHA"
git clone -q "$SRC" "$G/basejob/head"
git -C "$G/basejob/head" checkout -q "$HEAD_SHA"
python3 -I -B -X utf8 "$ROOT/check/scripts/wf_steps.py" "$G/basejob/base/.github/workflows/no_float_base.yml" "$G/tmp-base" "$G/steps-base" > /dev/null
mkdir -p "$G/tmp-base"
run_steps no-float-base "$G/basejob" "$G/steps-base" 1 2 3
# no-float-list-unchanged, both with their history
mkdir -p "$G/listjob"
git clone -q "$SRC" "$G/listjob/base"
git -C "$G/listjob/base" checkout -q "$BASE_SHA"
git clone -q "$SRC" "$G/listjob/head"
git -C "$G/listjob/head" checkout -q "$HEAD_SHA"
run_steps no-float-list-unchanged "$G/listjob" "$G/steps-base" 4
# no-float-compiled
git clone -q "$SRC" "$G/compiled"
git -C "$G/compiled" checkout -q "$HEAD_SHA"
python3 -I -B -X utf8 "$ROOT/check/scripts/wf_steps.py" "$G/compiled/.github/workflows/no-float-compiled.yml" "$G/tmp-compiled" "$G/steps-compiled" > /dev/null
mkdir -p "$G/tmp-compiled"
run_steps no-float-compiled "$G/compiled" "$G/steps-compiled" 1 2 3 4 5 6 7
echo "GATES_DONE|label=$LABEL|head=$HEAD_SHA|failed=$(grep -c -v '|rc=0|' "$ROWS")|json=0" | tee -a "$ROWS"
