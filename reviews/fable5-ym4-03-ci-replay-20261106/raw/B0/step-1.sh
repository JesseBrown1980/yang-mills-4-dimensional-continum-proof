set -euo pipefail
got=$(head -n 30 docs/PREDICTION-YM4-03.hbp | sha256sum | cut -d' ' -f1)
test "$got" = bcb1f24c0a6dd0e7942a9d4b5743145bf1536ec70854f65ff8e4854ff2c46a55
flux=$(sed -n 34,42p docs/PREDICTION-YM4-03.hbp | sha256sum | cut -d' ' -f1)
test "$flux" = 76e1d8f53e1519c82909004061c0587db59bf536902b6feb8610a2b2e7d82577
