# The lane's evidence and branch, read: SHA256SUMS, the prediction's commit order, carriage returns in every changed file, and file identity at the hosted run's commit.
set -u
R=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/repo
O=/mnt/c/tmp/opus55/ym4d-ci-replay-check-20261108/check/raw/lane-verify/LANE-CHECKS.hbp
: > $O
cd $R/reviews/fable5-ym4-03-ci-replay-20261106
rc=0; sha256sum --strict -c --quiet SHA256SUMS > /dev/null 2>&1 || rc=$?
echo "LANE_SUMS|rc=$rc|files=$(wc -l < SHA256SUMS)|json=0" >> $O
cd $R
pc=$(git log --format=%H -- reviews/fable5-ym4-03-ci-replay-20261106/PREDICTION.hbp | tr '\n' ',')
echo "LANE_PREDICTION|commits_touching=$pc|first_change_commit=$(git rev-parse 0574ce9)|prediction_is_ancestor_of_change=$(git merge-base --is-ancestor 648b29f 0574ce9 && echo 1 || echo 0)|prediction_time=$(git log -1 --format=%ct 648b29f)|change_time=$(git log -1 --format=%ct 0574ce9)|json=0" >> $O
n=0; cr=0
for f in $(git diff --name-only bf58ab2 e4a83d4); do n=$((n+1)); c=$(tr -cd '\r' < "$f" | wc -c); cr=$((cr+c)); done
echo "LANE_CR|changed_files=$n|carriage_returns=$cr|json=0" >> $O
for f in .github/workflows/one-scale-blocking.yml tests/test_one_scale_blocking.py tests/ONE_SCALE_BLOCKING_RECEIPT.txt; do
  echo "LANE_SAME_BLOB|path=$f|at_5af7b7a=$(git rev-parse 5af7b7a:$f)|at_35b3f42=$(git rev-parse 35b3f42:$f)|at_bf58ab2=$(git rev-parse bf58ab2:$f)|json=0" >> $O
done
echo "LANE_HEAD|branch_head=$(git rev-parse HEAD)|parent_chain=$(git log --format=%h bf58ab2..HEAD | tr '\n' ',')|json=0" >> $O
cat $O
