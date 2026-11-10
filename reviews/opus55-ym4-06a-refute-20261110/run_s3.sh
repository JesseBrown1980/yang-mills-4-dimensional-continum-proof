cd /mnt/c/tmp/opus55/ym4-06a-refute
for d in "2 2 3" "2 3 3" "3 3 3" "3 3 4" "2 4 4" "3 4 4" "2 2 4" "4 4 4"; do
  s=$(date +%s); python3 -I -B refute_s3.py $d 7 > s3_$(echo $d | tr ' ' x).hbp; echo "TIMING|dims=$d|seconds=$(( $(date +%s) - s ))"
done
