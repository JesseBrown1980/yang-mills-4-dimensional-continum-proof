set -euo pipefail
read_sabotage() {
  rc=0
  python3 -I -X utf8 tests/test_one_scale_blocking.py "sabotage=$1" > "/tmp/ym4ci2-B5/sab-$1.out" 2>&1 || rc=$?
  test "$rc" = 1
  grep -qF "FAILED|check=$2|json=0" "/tmp/ym4ci2-B5/sab-$1.out"
  if grep -q 'Traceback' "/tmp/ym4ci2-B5/sab-$1.out"; then echo "sabotage=$1 crashed"; exit 1; fi
  echo "sabotage=$1 exit=$rc $(grep -c '^FAILED' "/tmp/ym4ci2-B5/sab-$1.out") failed checks, among them $2"
}
read_sabotage twist_every_link 'winding_parity_b=2'
read_sabotage flux_wrong_sign 'flux_ground_in_e=0_Z2_2x1'
