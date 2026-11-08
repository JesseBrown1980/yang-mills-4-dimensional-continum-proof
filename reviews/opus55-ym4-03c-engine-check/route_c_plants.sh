#!/bin/bash
# YM4-03C engine check: route C's own planted errors, each run in d = 3 through beta^10. Each must exit 1 and write a MISS row.
# Run from the repository root: bash reviews/opus55-ym4-03c-engine-check/route_c_plants.sh > ROUTE-C-PLANTS.hbp
set -uo pipefail
d=reviews/opus55-ym4-03c-engine-check
for p in plant_no_multinomial plant_moment_for_cumulant plant_support_twice plant_recursion_sign; do
  rc=0
  out=$(python3 -I -B -X utf8 "$d/route_c_cumulants.py" 3 10 "$p") || rc=$?
  first=$(printf '%s\n' "$out" | grep -m1 '|result=MISS|' || true)
  last=$(printf '%s\n' "$out" | grep '^ROUTE_C_DONE' || true)
  echo "ROUTE_C_PLANT|option=$p|exit=$rc|first_miss=${first:-none}|done=${last:-none}"
done
