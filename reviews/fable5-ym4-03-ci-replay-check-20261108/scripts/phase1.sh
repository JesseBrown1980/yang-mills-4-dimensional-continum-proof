set -u
cd /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
R=check/scripts/run_timed.py
for k in 1 2 3; do
  python3 -I -B -X utf8 $R one A-step-$k /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/repo /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/work/wfA/step-$k.sh work/T/phase1.hbp work/logs
  python3 -I -B -X utf8 $R one B-step-$k /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/main-tree /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/work/wfB/step-$k.sh work/T/phase1.hbp work/logs
done
python3 -I -B -X utf8 $R one A-step-4 /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/repo /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/work/wfA/step-4.sh work/T/phase1-main.hbp work/logs &
python3 -I -B -X utf8 $R one B-step-4 /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/main-tree /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/work/wfB/step-4.sh work/T/phase1-main.hbp work/logs &
wait
echo PHASE1_DONE
