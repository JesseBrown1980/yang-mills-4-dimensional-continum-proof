set -euo pipefail
python3 -I -B -X utf8 tests/one_scale_replay.py record /tmp/ym4ci2-A2/ym4-03-cache seeds=tests/ONE_SCALE_BLOCKING_BRACKETS.hbp > /tmp/ym4ci2-A2/blocking.out 2> /tmp/ym4ci2-A2/blocking.err
cat /tmp/ym4ci2-A2/blocking.err
cmp /tmp/ym4ci2-A2/blocking.out tests/ONE_SCALE_BLOCKING_RECEIPT.txt
grep -q '|failed=0|' /tmp/ym4ci2-A2/blocking.out
if grep -q '^FAILED' /tmp/ym4ci2-A2/blocking.out; then echo "a check failed"; exit 1; fi
grep '^REPLAY_DONE|' /tmp/ym4ci2-A2/ym4-03-cache/REPLAY-INDEX.hbp
