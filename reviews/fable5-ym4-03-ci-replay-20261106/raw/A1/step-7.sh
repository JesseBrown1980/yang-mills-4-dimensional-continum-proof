set -euo pipefail
rc=0
python3 -I -X utf8 tests/test_one_scale_blocking.py sabotage=no_such_name > /tmp/ym4ci2-A1/unknown.out 2>&1 || rc=$?
test "$rc" = 2
rc=0
python3 -I -B -X utf8 tests/one_scale_replay.py replay /tmp/ym4ci2-A1/ym4-03-cache sabotage=no_such_name > /tmp/ym4ci2-A1/unknown-replay.out 2>&1 || rc=$?
test "$rc" = 2
rc=0
python3 -I -B -X utf8 tests/one_scale_replay.py replay /tmp/ym4ci2-A1/ym4-03-cache cache_sabotage=no_such_name > /tmp/ym4ci2-A1/unknown-cache.out 2>&1 || rc=$?
test "$rc" = 2
