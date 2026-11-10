cd /mnt/c/tmp/opus55/ym4-06a-refute/repo
python3 --version
/usr/bin/time -f "replay_seconds=%e" python3 -I -B -X utf8 tests/test_ym4_06a_global_lock.py > /mnt/c/tmp/opus55/ym4-06a-refute/replay.hbp
sha256sum /mnt/c/tmp/opus55/ym4-06a-refute/replay.hbp tests/YM4_06A_GLOBAL_LOCK_RECEIPT.hbp
cmp /mnt/c/tmp/opus55/ym4-06a-refute/replay.hbp tests/YM4_06A_GLOBAL_LOCK_RECEIPT.hbp && echo CMP_IDENTICAL
cd tests && sha256sum -c YM4_06A_GLOBAL_LOCK_RECEIPT.hbp.sha256; cd ..
for s in broken_transport noncommuting_triple wrong_chi dropped_face missing_gauge_orbit unreconstructible_flux twisted_as_periodic; do
  python3 -I -B -X utf8 tests/test_ym4_06a_global_lock.py sabotage=$s > /mnt/c/tmp/opus55/ym4-06a-refute/plant_$s.out 2>&1
  echo "PLANT|name=$s|rc=$?|last=$(tail -1 /mnt/c/tmp/opus55/ym4-06a-refute/plant_$s.out)|lines_before_fail=$(wc -l < /mnt/c/tmp/opus55/ym4-06a-refute/plant_$s.out)"
done
python3 -I -X utf8 scripts/no_float_gate.py . | tail -3
