B=/mnt/c/tmp/opus55/ym4-06a-refute
mkdir -p $B/probe
cp $B/repo/tests/test_exact_su2_4d.py $B/probe/
probe() { # name line
  sed "$2s/check(/(lambda *a: None)(/" $B/repo/tests/test_ym4_06a_global_lock.py > $B/probe/t_$1.py
  cd $B/probe; python3 -I -B -X utf8 t_$1.py sabotage=$1 > $B/probe/out_$1.txt 2>&1; rc=$?
  echo "PROBE|plant=$1|first_check_removed_line=$2|rc=$rc|next_catch=$(grep -o 'FAILED|check=[A-Za-z_]*' $B/probe/out_$1.txt | head -1)|error=$(grep -o '^[A-Za-z]*Error.*' $B/probe/out_$1.txt | head -1)"
}
probe wrong_chi 99
probe noncommuting_triple 777
probe dropped_face 234
probe broken_transport 281
probe missing_gauge_orbit 756
probe unreconstructible_flux 830
probe twisted_as_periodic 730
