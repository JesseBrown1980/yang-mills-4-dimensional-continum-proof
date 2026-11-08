set -euo pipefail
rc=0
python3 -I -X utf8 tests/test_one_scale_blocking.py sabotage=no_such_name > /tmp/ym4ci2-B0/unknown.out 2>&1 || rc=$?
test "$rc" = 2
