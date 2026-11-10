cd /mnt/c/tmp/opus55/ym4-06a-refute
for d in "2 3 4" "3 3 5" "2 5 5" "3 5 5"; do python3 -I -B refute_s3.py $d 7 > s3_$(echo $d | tr ' ' x).hbp; done
for d in "3 3 3" "3 3 4" "3 4 4" "4 4 4"; do python3 -I -B refute_s3.py $d 8 > s3b8_$(echo $d | tr ' ' x).hbp; done
