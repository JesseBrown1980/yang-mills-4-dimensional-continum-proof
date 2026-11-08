set -euo pipefail
python3 -I -X utf8 tests/test_one_scale_blocking.py > /tmp/ym4ci2-B0/blocking.out 2> /tmp/ym4ci2-B0/blocking.err
cat /tmp/ym4ci2-B0/blocking.err
cmp /tmp/ym4ci2-B0/blocking.out tests/ONE_SCALE_BLOCKING_RECEIPT.txt
grep -q '|failed=0|' /tmp/ym4ci2-B0/blocking.out
if grep -q '^FAILED' /tmp/ym4ci2-B0/blocking.out; then echo "a check failed"; exit 1; fi
