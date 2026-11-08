#!/bin/bash
# YM4-03C engine check: planted errors in the engine itself, each a text edit of a copy, built with Rust 1.81 and run once.
# Each must stop the run with exit 1 and a FAILED row naming its check. Run from the repository root:
#   bash reviews/opus55-ym4-03c-engine-check/engine_plants.sh OUT_DIR > ENGINE-PLANTS.hbp
set -uo pipefail
F=reviews/fable5-ym4-03c-engine/blocked_action_engine.rs
E=reviews/opus55-ym4-03c-engine-check/edit_text.py
O=$1
mkdir -p "$O"
plant() {
  name=$1
  shift
  if ! python3 -I -B -X utf8 "$E" "$F" "$O/$name.rs" "$@" > "$O/$name.edit" 2>&1; then
    echo "PLANT|name=$name|edit=not_applied|json=0"
    return
  fi
  if ! rustc +1.81.0 -O --edition 2021 -o "$O/$name" "$O/$name.rs" > "$O/$name.build" 2>&1; then
    echo "PLANT|name=$name|build=failed|json=0"
    return
  fi
  rc=0
  "$O/$name" > "$O/$name.out" 2> "$O/$name.err" || rc=$?
  first=$(grep -m1 '^FAILED' "$O/$name.out" || true)
  echo "PLANT|name=$name|exit=$rc|first=${first:-none|json=0}"
}
# the orbit factor of the one class of 8 plaquettes (the bumps) dropped
plant one_class_orbit_dropped $'Q::frac(pg, (c.nmatch * c.tstab) as i128)\n        }' $'if c.plaqs.len() == 8 { Q::one() } else { Q::frac(pg, (c.nmatch * c.tstab) as i128) }\n        }'
# a wrong orbit count: the classes of 10 plaquettes with stabilizer 8 counted twice
plant chair_class_orbit_doubled $'Q::frac(pg, (c.nmatch * c.tstab) as i128)\n        }' $'Q::frac(if c.plaqs.len() == 10 && c.nmatch * c.tstab == 8 { 2 * pg } else { pg }, (c.nmatch * c.tstab) as i128)\n        }'
# a sign flip: each incompatible pair entered with +1/2 in place of -1/2
plant cluster_sign_flipped 'let half = Q::frac(-1, 2);' 'let half = Q::frac(1, 2);'
# a 2I average past degree 11: the term-by-term check and its guards lifted to degree 13
plant twoi_average_past_degree_11 '    for target in 7..=11usize {' '    for target in 7..=13usize {' 'if d0 > 11 || d1 > 11 {' 'if d0 > 13 || d1 > 13 {'
