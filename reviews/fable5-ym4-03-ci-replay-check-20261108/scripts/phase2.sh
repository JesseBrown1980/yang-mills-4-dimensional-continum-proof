set -u
cd /mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
R=check/scripts/run_timed.py
A=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/repo
B=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/main-clone
WA=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/work/wfA
WB=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/work/wfB
test -s work/runA/ym4-03-cache/REPLAY-INDEX.hbp
python3 -I -B -X utf8 $R pairs work/T/lane1.hbp work/logs/lane1 $A $WA $B $WB B reversed_order shifted_endpoint dropped_inverse theta_no_inverse wrong_convolution_power wrong_first_coefficient extra_plaquette_factor wrong_block_shell > work/lane1.log 2>&1 &
python3 -I -B -X utf8 $R pairs work/T/lane2.hbp work/logs/lane2 $A $WA $B $WB A twist_every_link flux_wrong_sign overlap_skips_next visibility_ignores_omega_error visibility_error_halved visibility_error_inflated overlap_one_power > work/lane2.log 2>&1 &
wait
python3 -I -B -X utf8 $R one A-step-6 $A $WA/step-6.sh work/T/phase2-tail.hbp work/logs
python3 -I -B -X utf8 $R one A-step-7 $A $WA/step-7.sh work/T/phase2-tail.hbp work/logs
python3 -I -B -X utf8 $R one B-step-6 $B $WB/step-6.sh work/T/phase2-tail.hbp work/logs
echo PHASE2_DONE
