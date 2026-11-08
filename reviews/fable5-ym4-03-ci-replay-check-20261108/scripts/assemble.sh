# Build the evidence folder: collect the raw runs, read them, seal the folder, replay it, and copy it into the proposal clone.
# usage = bash assemble.sh
set -eu
ROOT=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108
C=$ROOT/check
LABEL=fable5-ym4-03-ci-replay-check-20261108
bash $C/scripts/collect.sh
python3 -I -B -X utf8 $C/scripts/analyze.py $ROOT $C/RESULTS.hbp > /dev/null
python3 -I -B -X utf8 $C/scripts/reads.py $C > /dev/null
python3 -I -B -X utf8 $C/scripts/chain.py $C $LABEL
rc=0
python3 -I -B -X utf8 $C/VERIFY.py $C > $C/VERIFY.hbp || rc=$?
tail -3 $C/VERIFY.hbp
echo "VERIFY_RC|rc=$rc|json=0"
D=$ROOT/prop/reviews/$LABEL
rm -rf $D
mkdir -p $D
(cd $C && tar --exclude=.git -cf - .) | (cd $D && tar -xf -)
rc2=0
python3 -I -B -X utf8 $D/VERIFY.py $D > $ROOT/work/verify-in-prop.out || rc2=$?
cmp $ROOT/work/verify-in-prop.out $D/VERIFY.hbp && echo "VERIFY_IN_PROP_SAME|rc=$rc2|json=0"
(cd $D && sha256sum --strict -c --quiet SHA256SUMS) && echo "PROP_SUMS_CLEAN|json=0"
