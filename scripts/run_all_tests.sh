#!/usr/bin/env bash
# Run every tests/test_*.py file and every VOL checker, unfiltered.
# The VOL checker outputs are compared byte for byte with their frozen receipts.
# Usage: bash scripts/run_all_tests.sh [OUTDIR]
set -uo pipefail
out="${1:-build/run-all}"
mkdir -p "$out"
fail=0
total=0

run() {
  local file="$1" log="$2"
  local start end
  start=$(date +%s)
  if python3 -B "$file" > "$log" 2>&1; then
    end=$(date +%s)
    echo "RUN_ALL|file=$file|status=PASS|seconds=$((end - start))|json=0"
  else
    end=$(date +%s)
    echo "RUN_ALL|file=$file|status=FAIL|seconds=$((end - start))|json=0"
    tail -5 "$log" | sed 's/^/    /'
    fail=$((fail + 1))
  fi
  total=$((total + 1))
}

for t in tests/test_*.py; do
  run "$t" "$out/$(basename "$t" .py).log"
done

# VOL checker -> frozen receipt (byte-identical output required).
pairs="
ym4_su2_vol03_cube_haar_cell_tree:YM4-VOL03-CUBE-HAAR-TREE-20261122
ym4_su2_vol04_full_fourth_schur:YM4-VOL04-COMPLETE-FOURTH-SCHUR-20261122
ym4_su2_vol04_independent_parity_audit:YM4-VOL04-INDEPENDENT-QUARTIC-PARITY-20261122
ym4_su2_vol05_wilson_spectral_support:YM4-VOL05-WILSON-SPECTRAL-SUPPORT-20261122
ym4_su2_vol06_full_spectrum:YM4-VOL06-FULL-PHYSICAL-GAP-20261122
ym4_su2_vol07_block_rate:YM4-VOL07-PHYSICAL-BLOCK-RATE-20261122
ym4_su2_vol08_wilson_star:YM4-VOL08-WILSON-STAR-20261122
ym4_su2_vol09_periodic_good_star:YM4-VOL09-PERIODIC-GOOD-STAR-20261122
ym4_su2_vol10_bad_island:YM4-VOL10-BAD-ISLAND-20261122
ym4_su2_vol11_separated_defects:YM4-VOL11-SEPARATED-DEFECTS-20261122
"
for pair in $pairs; do
  checker="tests/${pair%%:*}.py"
  receipt="docs/certificate-atlas/${pair##*:}.hbp"
  log="$out/${pair%%:*}.hbp"
  run "$checker" "$log"
  if cmp -s "$log" "$receipt"; then
    echo "RUN_ALL|receipt=$receipt|byte_identical=YES|json=0"
  else
    echo "RUN_ALL|receipt=$receipt|byte_identical=NO|json=0"
    fail=$((fail + 1))
  fi
done

echo "RUN_ALL_VERDICT|runs=$total|failures=$fail|json=0"
[ "$fail" -eq 0 ]
