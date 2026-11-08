set -u
cd /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
for k in 1 2; do
  python3 -I -B -X utf8 check/scripts/run_timed.py one P-final-step-$k /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/prop /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/work/wfP/step-$k.sh work/T/proposed-final.hbp work/logs
done
bash check/scripts/gates.sh prop-aa428ba /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/prop $(git -C prop rev-parse HEAD)
