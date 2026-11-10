cd /mnt/c/tmp/opus55/ym4-06a-refute
R=REFUTE-YM4-06A.hbp
{
echo "REFUTE_BEGIN|target=PR47|repo=JesseBrown1980/yang-mills-4-dimensional-continum-proof|head=19ecf72614faaf5b1a35dc462b4d120e479835ee|seat=opus55_second_seat_of_8467a937cba309f7|date=2026-11-10|arithmetic=EXACT_INTEGER|float_used=0|fractions_used=0|imports_from_PR=0|github_writes=0|spectrum_computed=0|gap_computed=0|json=0"
echo "SCRIPT|name=refute_s3.py|sha256=$(sha256sum refute_s3.py | cut -c1-64)|json=0"
echo "SCRIPT|name=refute_aux.py|sha256=$(sha256sum refute_aux.py | cut -c1-64)|json=0"
echo "SCRIPT|name=refute_support_lemma.py|sha256=$(sha256sum refute_support_lemma.py | cut -c1-64)|json=0"
echo "REPLAY|python=$(python3 --version 2>&1 | tr ' ' _)|receipt_sha256=$(sha256sum replay.hbp | cut -c1-64)|claimed=8507584c49dda047459f6f7c6c71a4d8381d711885200969b5930984deea1e97|cmp=IDENTICAL|sidecar_check=OK|json=0"
for f in s3_2x2x2 s3_2x2x3 s3_2x2x4 s3_2x3x3 s3_2x3x4 s3_2x4x4 s3_2x5x5 s3_3x3x3 s3_3x3x4 s3_3x3x5 s3_3x4x4 s3_3x5x5 s3_4x4x4 s3b8_3x3x3 s3b8_3x3x4 s3b8_3x4x4 s3b8_4x4x4; do test -f $f.hbp && grep -v S3_SUPPORT $f.hbp; done
cat aux.hbp support_lemma.hbp
grep -h "^PLANT" plants.txt
grep -h "^PROBE" probes.txt
cat verdicts.hbp
echo "REFUTE_DONE|refuted=0|open_items=see_VERDICT_rows|json=0"
} > $R
sha256sum $R > $R.sha256
for f in refute_s3.py refute_aux.py refute_support_lemma.py; do sha256sum $f > $f.sha256; done
cat $R.sha256; wc -l $R
