# SINGLE_POWER, the one module-level memo the replay carries without a digest: which lines touch it, and which sections' recorded units hold its writer.
set -u
ROOT=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
T=$ROOT/repo/tests/test_one_scale_blocking.py
O=$ROOT/check/raw/lane-verify/MEMO.hbp
lines=$(grep -n "SINGLE_POWER" $T | cut -d: -f1 | tr '\n' ',')
callers=$(grep -n "single_power(" $T | cut -d: -f1 | tr '\n' ',')
sections=$(grep "^REPLAY_SECTION" $ROOT/work/runA/ym4-03-cache/REPLAY-INDEX.hbp | grep "single_power:" | sed 's/.*|section=\([a-z_0-9]*\)|.*/\1/' | tr '\n' ',')
echo "MEMO|name=SINGLE_POWER|lines=$lines|single_power_lines=$callers|sections_covering_single_power=$sections|json=0" > $O
cat $O
