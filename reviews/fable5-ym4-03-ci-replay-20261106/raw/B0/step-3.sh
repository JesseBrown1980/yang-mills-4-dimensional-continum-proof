set -euo pipefail
python3 -I -X utf8 scripts/no_float_gate.py --selftest
python3 -I -X utf8 scripts/no_float_gate.py .
