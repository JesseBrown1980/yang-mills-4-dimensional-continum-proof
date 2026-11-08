set -u
cd /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/repo/reviews/fable5-ym4-03-ci-replay-20261106
rc=0
python3 -I -B -X utf8 VERIFY.py /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/repo/reviews/fable5-ym4-03-ci-replay-20261106 /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/repo > /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/check/raw/lane-verify/VERIFY-rerun.out 2>&1 || rc=$?
echo "LANE_VERIFY_RC|rc=$rc|json=0" >> /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/check/raw/lane-verify/VERIFY-rerun.out
tail -5 /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/check/raw/lane-verify/VERIFY-rerun.out
cmp /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/check/raw/lane-verify/VERIFY-rerun.out VERIFY.hbp && echo SAME_AS_COMMITTED_VERIFY || echo DIFFERS_FROM_COMMITTED_VERIFY
git -C /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/repo status --short | head -3
