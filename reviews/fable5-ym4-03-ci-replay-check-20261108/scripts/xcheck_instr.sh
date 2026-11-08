# instrument.py ran the driver first through runpy with frame reads, then by a plain import (the version here); each output row file must match.
set -u
W=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/work
O=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/check/raw/instr/XCHECK-INSTRUMENT.hbp
: > $O
for f in $W/instr/*.hbp; do
  b=$(basename $f)
  if [ "$b" = RUNS.hbp ] || [ "$b" = XCHECK-INSTRUMENT.hbp ]; then continue; fi
  same=0
  cmp -s $f $W/instr-runpy/$b && same=1
  echo "XCHECK_INSTRUMENT|file=$b|sha256=$(sha256sum $f | cut -d' ' -f1)|first_version_sha256=$(sha256sum $W/instr-runpy/$b | cut -d' ' -f1)|same=$same|json=0" >> $O
done
echo "XCHECK_INSTRUMENT_DONE|files=$(grep -c '^XCHECK_INSTRUMENT|' $O)|same=$(grep -c '|same=1|' $O)|json=0" >> $O
tail -1 $O
