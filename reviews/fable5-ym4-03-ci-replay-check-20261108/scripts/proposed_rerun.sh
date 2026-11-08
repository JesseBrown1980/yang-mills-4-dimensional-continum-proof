# The proposal's step-5 control overwrites sab-reversed_order.out with its own run; this reruns the plain reversed_order replay beside it.
set -u
cd /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/prop
rc=0
python3 -I -B -X utf8 tests/one_scale_replay.py replay /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/work/runP/ym4-03-cache sabotage=reversed_order > /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/work/runP/sab-reversed_order-rerun.out 2>&1 || rc=$?
echo "RERUN|name=reversed_order|rc=$rc|json=0"
