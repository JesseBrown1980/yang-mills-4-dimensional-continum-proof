set -euo pipefail
read_sabotage() {
  rc=0
  python3 -I -X utf8 tests/test_one_scale_blocking.py "sabotage=$1" > "/tmp/ym4ci2-B2/sab-$1.out" 2>&1 || rc=$?
  test "$rc" = 1
  grep -qF "FAILED|check=$2|json=0" "/tmp/ym4ci2-B2/sab-$1.out"
  if grep -q 'Traceback' "/tmp/ym4ci2-B2/sab-$1.out"; then echo "sabotage=$1 crashed"; exit 1; fi
  echo "sabotage=$1 exit=$rc $(grep -c '^FAILED' "/tmp/ym4ci2-B2/sab-$1.out") failed checks, among them $2"
}
read_sabotage wrong_convolution_power 'two_dimensions_closes_S3_b=2_2x2'
read_sabotage wrong_first_coefficient 'first_dependence_(2,2,2,2)_position=0'
read_sabotage extra_plaquette_factor 'brute_equals_elimination_S3'
read_sabotage wrong_block_shell 'walls_Z2_4x2x2'
