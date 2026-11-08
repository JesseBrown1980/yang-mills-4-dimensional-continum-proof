set -euo pipefail
read_sabotage() {
  rc=0
  python3 -I -X utf8 tests/test_one_scale_blocking.py "sabotage=$1" > "/tmp/ym4ci2-B1/sab-$1.out" 2>&1 || rc=$?
  test "$rc" = 1
  grep -qF "FAILED|check=$2|json=0" "/tmp/ym4ci2-B1/sab-$1.out"
  if grep -q 'Traceback' "/tmp/ym4ci2-B1/sab-$1.out"; then echo "sabotage=$1 crashed"; exit 1; fi
  echo "sabotage=$1 exit=$rc $(grep -c '^FAILED' "/tmp/ym4ci2-B1/sab-$1.out") failed checks, among them $2"
}
read_sabotage reversed_order 'covariance_b=2'
read_sabotage shifted_endpoint 'covariance_b=2'
read_sabotage dropped_inverse 'covariance_b=2'
read_sabotage theta_no_inverse 'reflection_map_b=2_c=0'
