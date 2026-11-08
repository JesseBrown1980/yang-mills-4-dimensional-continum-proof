set -euo pipefail
n=$(sed -n 's/^YM4_03_DONE|checks=\([0-9]*\)|.*/\1/p' tests/ONE_SCALE_BLOCKING_RECEIPT.txt)
grep -qF "$n checks" docs/NOTE-YM4-03-ONE-SCALE-BLOCKING.md
echo "618b4414384b76e8e66a5c5cc482f962bcdb9f1c1b00c81ed4a2aa4311cf458c  reviews/fable5-ym4-03-first-run/FIRST-COMPLETE-READ.hbp" | sha256sum -c -
echo "404cb4d79a5a77dbf26f9e50871ace546c0b80a5cd287dc950069ac6764d8c0a  reviews/fable5-ym4-03-flux-first-run/FLUX-FIRST-READ.hbp" | sha256sum -c -
(cd reviews/opus55-ym4-03 && sha256sum --strict -c --quiet SHA256SUMS)
(cd reviews/opus55-ym4-03-recheck && sha256sum --strict -c --quiet SHA256SUMS)
(cd reviews/fable5-ym4-03-ci-replay-20261106 && sha256sum --strict -c --quiet SHA256SUMS)
cd reviews/opus55-ym4-03-certificate && sha256sum --strict -c --quiet SHA256SUMS
