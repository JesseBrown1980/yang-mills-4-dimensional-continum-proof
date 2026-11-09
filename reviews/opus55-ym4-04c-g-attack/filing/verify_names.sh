#!/bin/bash
D=/mnt/c/tmp/opus55/ym4-04c-gattack
grep -o 'per_step_status=[^;]*' $D/G_ATTACK_ROW.txt | sed 's/per_step_status=//' | tr ',' '\n' | sed 's/:open$//' > /tmp/gattack_row_names.txt
grep -o 'target=[^|]*' $D/work/filing/GATTACK-ROWS.hbp | sed 's/target=//' | tail -n +8 > /tmp/gattack_filed_names.txt
echo "row_names=$(wc -l < /tmp/gattack_row_names.txt) filed_step_names=$(wc -l < /tmp/gattack_filed_names.txt)"
if diff /tmp/gattack_row_names.txt /tmp/gattack_filed_names.txt > /dev/null; then echo "NAMES|order_and_spelling=EXACT"; else echo "NAMES|DIFF"; diff /tmp/gattack_row_names.txt /tmp/gattack_filed_names.txt; fi
grep -o 'target=[^|]*' $D/work/filing/GATTACK-ROWS.hbp | head -7 | tr '\n' ' '; echo
grep -o '^check_[A-Za-z0-9]*' $D/G_ATTACK_ROW.txt | tr '\n' ' '; echo
