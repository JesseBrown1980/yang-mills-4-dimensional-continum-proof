#!/bin/bash
# read-only: hash L3/L4 artifacts and scan lane outputs for failure markers
W=/mnt/c/tmp/opus55/ym4-04c-gattack/work
cd $W/L3-sec4-part1 && sha256sum *.py *.out
cd $W/L4-sec4-part2 && sha256sum *.py *.out pr45-read/*
cd $W
for f in L*/*.out; do
  n=$(grep -ciE 'fail|not_ok|ok=0|pass=0|all_ok=0|all_pass=0' "$f")
  echo "SCAN|file=$f|lines=$(wc -l <"$f")|flagged_lines=$n"
done
