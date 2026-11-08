set -e
cd /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
mkdir -p work/runA work/runB work/wfA work/wfB work/T work/logs
python3 -I -B -X utf8 check/scripts/wf_steps.py repo/.github/workflows/one-scale-blocking.yml /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/work/runA work/wfA
echo ====
python3 -I -B -X utf8 check/scripts/wf_steps.py main-tree/.github/workflows/one-scale-blocking.yml /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/work/runB work/wfB
