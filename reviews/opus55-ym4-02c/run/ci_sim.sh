#!/usr/bin/env bash
# Second seat: the workflow's steps replayed on a private clone, with one fault planted each time. Each step runs in its own shell with set -euo pipefail, as on the runner.
# The only change from the yml is tr -d CR, because this host writes CRLF to redirected stdout.
export MSYS_NO_PATHCONV=1
ROOT=C:/tmp/opus55/attack-4d-02c-20261103
CLONE=$ROOT/clone
OUT=$ROOT/run/ci
mkdir -p "$OUT"
cat > "$OUT/step3.sh" <<'S3'
set -euo pipefail
got=$(head -n 26 docs/PREDICTION-YM4-02c.hbp | sha256sum | cut -d' ' -f1)
test "$got" = 2448d8e6824b4f5197ee4d30aeb3612a7d5a8c3282e3737ddf5aeb5b5e6422d3
S3
cat > "$OUT/step4.sh" <<'S4'
set -euo pipefail
python3 -I -X utf8 tests/test_reflection_transfer_4d.py > "$OUT/r.raw"
tr -d '\r' < "$OUT/r.raw" > "$OUT/r.out"
cmp "$OUT/r.out" tests/REFLECTION_TRANSFER_RECEIPT.txt
grep -q '^REFLECTION_TRANSFER_DONE|failed=0|json=0$' "$OUT/r.out"
if grep -q '^FAILED' "$OUT/r.out"; then echo "a check failed"; exit 1; fi
S4
cat > "$OUT/step5.sh" <<'S5'
set -euo pipefail
for s in no_inverse_on_time_links wrong_plane wrong_multiplicity negative_weight_called_positive signed_site_weight_called_positive bad_projector; do
  rc=0
  python3 -I -X utf8 tests/test_reflection_transfer_4d.py "sabotage=$s" > "$OUT/sab.raw" 2>&1 || rc=$?
  tr -d '\r' < "$OUT/sab.raw" > "$OUT/sab.out"
  test "$rc" = 1
  grep -q '^FAILED|check=' "$OUT/sab.out"
  if grep -q 'Traceback' "$OUT/sab.out"; then echo "sabotage=$s crashed"; exit 1; fi
done
S5
cat > "$OUT/step6.sh" <<'S6'
set -euo pipefail
rc=0
python3 -I -X utf8 tests/test_reflection_transfer_4d.py sabotage=no_such_name > "$OUT/unk.raw" 2>&1 || rc=$?
test "$rc" = 2
S6
export OUT
cd "$CLONE" || exit 9
git config core.autocrlf false
git checkout -q -f 1618199d51d722124bdb5ecc0ec28c5ba3f5a9ce
one() { bash "$OUT/$1.sh" > /dev/null 2>&1; rc=$?; if [ "$rc" = 0 ]; then echo pass; else echo RED; fi; }
run_all() { printf 'CI_SIM|fault=%s|step3=%s|step4=%s|step5=%s|step6=%s|json=0\n' "$1" "$(one step3)" "$(one step4)" "$(one step5)" "$(one step6)"; }
reset_all() { git checkout -q -f 1618199d51d722124bdb5ecc0ec28c5ba3f5a9ce -- docs tests; }
run_all none
sed -i '12s/value=593\/4/value=594\/4/' docs/PREDICTION-YM4-02c.hbp; run_all prediction_row_12_value_changed; reset_all
sed -i 's/G_FF=593\/4|expected=593\/4/G_FF=591\/4|expected=593\/4/' tests/REFLECTION_TRANSFER_RECEIPT.txt; run_all receipt_value_changed; reset_all
sed -i 's/^    if not ok:$/    if False:/' tests/test_reflection_transfer_4d.py; run_all check_function_disabled; reset_all
sed -i 's/return \[sum(c\[rho\] \* Q8_CHI\[rho\]\[k\] for rho in range(5)) for k in range(Q8.nclasses)\]/return [sum(c[rho] * Q8_CHI[rho][k] for rho in range(4)) for k in range(Q8.nclasses)]/' tests/test_reflection_transfer_4d.py; run_all q8_weight_drops_the_two_dim_character; reset_all
sed -i 's/^    if SABOTAGE in ("no_inverse_on_time_links", "wrong_plane"):$/    if SABOTAGE in ("no_inverse_on_time_links", "wrong_plane") and False:/' tests/test_reflection_transfer_4d.py; run_all sabotage_dispatch_broken; reset_all
git status --short | head -5
