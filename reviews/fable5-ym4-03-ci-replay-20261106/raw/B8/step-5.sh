set -euo pipefail
read_sabotage() {
  rc=0
  python3 -I -X utf8 tests/test_one_scale_blocking.py "sabotage=$1" > "/tmp/ym4ci2-B8/sab-$1.out" 2>&1 || rc=$?
  test "$rc" = 1
  grep -qF "FAILED|check=$2|json=0" "/tmp/ym4ci2-B8/sab-$1.out"
  if grep -q 'Traceback' "/tmp/ym4ci2-B8/sab-$1.out"; then echo "sabotage=$1 crashed"; exit 1; fi
  echo "sabotage=$1 exit=$rc $(grep -c '^FAILED' "/tmp/ym4ci2-B8/sab-$1.out") failed checks, among them $2"
}
read_sabotage visibility_error_inflated 'flux_two_insertions_above_the_residual_Z2_2x1'
read_sabotage overlap_one_power 'overlap_bracket_narrow_Z2_2x1_(1, -1)'
