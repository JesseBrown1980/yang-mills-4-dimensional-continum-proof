set -euo pipefail
read_sabotage() {
  name=$1
  shift
  rc=0
  python3 -I -B -X utf8 tests/one_scale_replay.py replay /tmp/ym4ci2-A1/ym4-03-cache "sabotage=$name" > "/tmp/ym4ci2-A1/sab-$name.out" 2>&1 || rc=$?
  test "$rc" = 1
  for named in "$@"; do
    grep -qF "FAILED|check=$named|json=0" "/tmp/ym4ci2-A1/sab-$name.out"
  done
  if grep -q 'Traceback' "/tmp/ym4ci2-A1/sab-$name.out"; then echo "sabotage=$name crashed"; exit 1; fi
  if grep -q '^FAILED|check=replay_' "/tmp/ym4ci2-A1/sab-$name.out"; then echo "sabotage=$name: a replay check failed"; exit 1; fi
  reached=$(grep -c "|mode=computed|why=reached_by_$name|" "/tmp/ym4ci2-A1/sab-$name.out" || true)
  if [ "$reached" -lt 1 ]; then echo "sabotage=$name computed no section it reaches"; exit 1; fi
  echo "sabotage=$name exit=$rc $(grep -c '^FAILED' "/tmp/ym4ci2-A1/sab-$name.out") failed checks, among them $*; computed=$(grep -c '|mode=computed|' "/tmp/ym4ci2-A1/sab-$name.out") reused=$(grep -c '|mode=reused|' "/tmp/ym4ci2-A1/sab-$name.out")"
}
read_sabotage reversed_order 'covariance_b=2'
read_sabotage shifted_endpoint 'covariance_b=2'
read_sabotage dropped_inverse 'covariance_b=2'
read_sabotage theta_no_inverse 'reflection_map_b=2_c=0'
read_sabotage wrong_convolution_power 'two_dimensions_closes_S3_b=2_2x2'
read_sabotage wrong_first_coefficient 'first_dependence_(2,2,2,2)_position=0'
read_sabotage extra_plaquette_factor 'brute_equals_elimination_S3'
read_sabotage wrong_block_shell 'walls_Z2_4x2x2'
read_sabotage twist_every_link 'winding_parity_b=2'
read_sabotage flux_wrong_sign 'flux_ground_in_e=0_Z2_2x1'
read_sabotage overlap_skips_next 'overlap_closed_form_Z2_2x1_(1, -1)' 'overlap_bracket_Z2_2x1_(1, -1)'
read_sabotage visibility_ignores_omega_error 'flux_exact_zero_overlap_not_certified_Z2_2x1'
read_sabotage visibility_error_halved 'flux_exact_zero_residual_rejected_Z2_2x1'
read_sabotage visibility_error_inflated 'flux_two_insertions_above_the_residual_Z2_2x1'
read_sabotage overlap_one_power 'overlap_bracket_narrow_Z2_2x1_(1, -1)'
