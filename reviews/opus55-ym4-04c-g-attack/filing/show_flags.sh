#!/bin/bash
W=/mnt/c/tmp/opus55/ym4-04c-gattack/work
cd $W
for f in L3-sec4-part1/tree_graph_exact.out L4-sec4-part2/l4p2_checks.out L5-numbers/n1_constants.out L5-numbers/n2_certs.out L5-numbers/n3_c09.out L5-numbers/n4_g1c.out L5-numbers/n5_w03.out; do
  echo "== $f"
  grep -iE 'fail|not_ok|ok=0|pass=0|all_ok=0|all_pass=0' "$f" | cut -c1-400
done
echo "== L1 summary"
grep -h -iE 'all_ok|SUMMARY' L1-sec3-part1/*.out | cut -c1-300
echo "== L2 summary"
grep -h -iE 'all_pass|SUMMARY' L2-sec3-part2/*.out | cut -c1-300
echo "== L3 summary"
grep -h -iE 'PASS|SUMMARY' L3-sec4-part1/*.out | cut -c1-200 | tail -15
echo "== L4 tail"
tail -3 L4-sec4-part2/l4p2_checks.out | cut -c1-300
