#!/usr/bin/env bash
# The two new workflow steps, replayed on private copies, baseline and with one fault planted each time. Each step runs in its own strict shell. json=0.
export MSYS_NO_PATHCONV=1
R=C:/tmp/opus55/recheck-02c-20261103
W=$R/wf
rm -rf "$W"
mkdir -p "$W"
cat > "$W/step_pred.sh" <<'S'
set -euo pipefail
got=$(head -n 93 docs/PREDICTION-YM4-02c.hbp | sha256sum | cut -d' ' -f1)
test "$got" = 08db7d8135ba1ff945c79aefaafdc6661fa47c541561431de0e2ed73dcbe8210
S
cat > "$W/step_seat.sh" <<'S'
set -euo pipefail
cd reviews/opus55-ym4-02c
sha256sum -c --quiet SHA256SUMS
grep '^FILED|' FILED.hbp | while IFS='|' read -r _ p _ _ _ d c _; do
  p=${p#path=}; d=${d#sha256_as_delivered=}; c=${c#cr_removed=}
  if [ "$c" != 0 ]; then got=$(sed 's/$/\r/' "$p" | sha256sum | cut -d' ' -f1); else got=$(sha256sum "$p" | cut -d' ' -f1); fi
  test "$got" = "$d"
done
echo "delivered hashes all reproduced"
S
fresh() { rm -rf "$W/c"; mkdir -p "$W/c"; cp -r "$R/head/docs" "$R/head/reviews" "$W/c/"; cd "$W/c" || exit 9; }
run() { # label script
  if bash "$W/$2" > "$W/$1.out" 2>&1; then echo "STEP|case=$1|exit=0|json=0"; else echo "STEP|case=$1|exit=$?|json=0"; fi
}
fresh; run baseline_prediction step_pred.sh
fresh; sed -i '50s/found_by=this_run/found_by=that_run/' docs/PREDICTION-YM4-02c.hbp; run row_50_changed step_pred.sh
fresh; printf 'YM4_02C_EXTRA|json=0\n' >> docs/PREDICTION-YM4-02c.hbp; run row_appended_at_the_tail step_pred.sh
fresh; run baseline_seat step_seat.sh
fresh; sed -i '1s/^/x/' reviews/opus55-ym4-02c/src/geom.out; run out_file_changed step_seat.sh
fresh; sed -i 's/^FILED|path=src\/geom.py|\(.*\)|sha256_as_delivered=0/FILED|path=src\/geom.py|\1|sha256_as_delivered=1/; s/\(FILED|path=src\/geom.py|.*sha256_as_delivered=\)01f1/\1ffff/' reviews/opus55-ym4-02c/FILED.hbp; run delivered_hash_changed step_seat.sh
fresh; rm reviews/opus55-ym4-02c/src/cyl.py; run filed_file_removed step_seat.sh
cd "$R" || exit 9
find head/reviews/opus55-ym4-02c -type f | wc -l
find head/reviews/opus55-ym4-02c -type f -print0 | xargs -0 cat | wc -c
python3 -I -c "
import os
n=0
for d,_,fs in os.walk(r'C:/tmp/opus55/recheck-02c-20261103/head/reviews/opus55-ym4-02c'):
    for f in fs:
        n+=open(os.path.join(d,f),'rb').read().count(b'\r')
print('CR_bytes_in_the_filed_folder',n)"
grep -c 'gram12' head/reviews/opus55-ym4-02c/rust/brute.rs
