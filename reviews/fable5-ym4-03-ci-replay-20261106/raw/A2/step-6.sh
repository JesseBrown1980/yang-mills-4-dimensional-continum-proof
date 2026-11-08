set -euo pipefail
refused() {
  script=$1
  named=$2
  shift 2
  rc=0
  python3 -I -B -X utf8 "$script" replay /tmp/ym4ci2-A2/ym4-03-cache "$@" > /tmp/ym4ci2-A2/cache-control.out 2>&1 || rc=$?
  test "$rc" = 1
  grep -qF "FAILED|check=$named|json=0" /tmp/ym4ci2-A2/cache-control.out
  if grep -q 'Traceback' /tmp/ym4ci2-A2/cache-control.out; then echo "the cache control on $named crashed"; exit 1; fi
  echo "cache control exit=$rc on $named"
}
# A stale entry: the helper block_map edited after the index was recorded.
mkdir -p /tmp/ym4ci2-A2/stale-tree
cp -r tests /tmp/ym4ci2-A2/stale-tree/tests
sed -i 's/^def block_map(U, x_c, mu, b, sides, mul, one):$/&\n    # edited after the index was recorded/' /tmp/ym4ci2-A2/stale-tree/tests/test_one_scale_blocking.py
if cmp -s tests/test_one_scale_blocking.py /tmp/ym4ci2-A2/stale-tree/tests/test_one_scale_blocking.py; then echo "the edit changed nothing"; exit 1; fi
refused /tmp/ym4ci2-A2/stale-tree/tests/one_scale_replay.py replay_key_stale_section_covariance
refused tests/one_scale_replay.py replay_coverage_misses_helper_section_covariance sabotage=reversed_order cache_sabotage=key_misses_helper
refused tests/one_scale_replay.py replay_rows_sha256_section_covariance cache_sabotage=row_tampered
refused tests/one_scale_replay.py replay_bracket_stale sabotage=overlap_one_power cache_sabotage=stale_bracket
# Every section reused, those reversed_order reaches too: the passing receipt and exit 0, which the sabotage step's read refuses.
rc=0
python3 -I -B -X utf8 tests/one_scale_replay.py replay /tmp/ym4ci2-A2/ym4-03-cache sabotage=reversed_order cache_sabotage=reuse_reached > /tmp/ym4ci2-A2/reuse.out 2> /tmp/ym4ci2-A2/reuse.err || rc=$?
test "$rc" = 0
cmp /tmp/ym4ci2-A2/reuse.out tests/ONE_SCALE_BLOCKING_RECEIPT.txt
if grep -qF 'FAILED|check=covariance_b=2|json=0' /tmp/ym4ci2-A2/reuse.out; then echo "the reused rows hold the named check"; exit 1; fi
grep -q '|reused=16|computed=0|' /tmp/ym4ci2-A2/reuse.err
echo "cache control: every section reused under reversed_order gives exit 0 and the receipt, which the sabotage step refuses"
