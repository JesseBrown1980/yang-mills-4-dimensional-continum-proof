#!/bin/bash
F=/mnt/c/tmp/opus55/ym4-04c-gattack/frozen
N=$F/NOTE-YM4-04C-LOCAL-POLYMER-NORM-20261109.md
P=$F/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp
echo "== grep 0.2576475 / 0.3678794375 / 0.3678794463 in prediction (line numbers only, 300 chars)"
grep -n -o '.\{0,120\}0\.257647.\{0,80\}' $P | cut -c1-300
grep -n -o '.\{0,120\}0\.36787943.\{0,80\}' $P | cut -c1-300
grep -n -o '.\{0,120\}0\.36787944.\{0,80\}' $P | cut -c1-300
for r in "$@"; do
  echo "== note lines $r"
  sed -n "${r}p" $N | cut -c1-2500
done
