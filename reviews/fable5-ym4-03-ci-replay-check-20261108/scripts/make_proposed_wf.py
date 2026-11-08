"""Write check/proposed/one-scale-blocking.yml: the branch workflow with a read that holds the replay to the index's reach, its control, and this
lane's folder in step 2 and the trigger paths.

usage = python3 -I -B -X utf8 make_proposed_wf.py BRANCH_WORKFLOW OUT
Every edit must match exactly once. Integers only, json=0.
"""
import sys

src, out = sys.argv[1], sys.argv[2]
with open(src, encoding="utf-8") as handle:
    text = handle.read()
GUARD = (
    "            for section in $(awk -F'|' -v n=\"$name\" '$1 == \"REPLAY_SECTION\" { s = \"\"; r = \"\"; for (i = 2; i <= NF; i++) { if (index($i, \"section=\") == 1) s = substr($i, 9); "
    "if (index($i, \"reach=\") == 1) r = \",\" substr($i, 7) \",\" } if (index(r, \",\" n \",\") > 0) print s }' /tmp/ym4-03-cache/REPLAY-INDEX.hbp); do\n"
    "              if ! grep -q \"^REPLAY|order=[0-9]*|section=$section|mode=computed|\" \"/tmp/sab-$name.out\"; then echo \"sabotage=$name reused $section, which the index says it reaches\"; exit 1; fi\n"
    "            done\n")
CONTROL = (
    "          # A reached section wrongly reused: the read above refuses it, by the reach the index recorded.\n"
    "          mkdir -p /tmp/unmark-tree\n"
    "          cp -r tests /tmp/unmark-tree/tests\n"
    "          sed -i 's/CACHE_SABOTAGE != \"reuse_reached\":$/CACHE_SABOTAGE != \"reuse_reached\" and section != \"section_loops\":/' /tmp/unmark-tree/tests/one_scale_replay.py\n"
    "          if cmp -s tests/one_scale_replay.py /tmp/unmark-tree/tests/one_scale_replay.py; then echo \"the edit changed nothing\"; exit 1; fi\n"
    "          rc=0\n"
    "          (cd /tmp/unmark-tree && read_sabotage reversed_order 'covariance_b=2') > /tmp/unmark.out 2>&1 || rc=$?\n"
    "          cat /tmp/unmark.out\n"
    "          test \"$rc\" = 1\n"
    "          grep -qF \"sabotage=reversed_order reused section_loops, which the index says it reaches\" /tmp/unmark.out\n"
    "          echo \"the read refuses reversed_order with section_loops reused\"\n")
LAST_CALL = "          read_sabotage overlap_one_power 'overlap_bracket_narrow_Z2_2x1_(1, -1)'\n"
REACHED = "            if [ \"$reached\" -lt 1 ]; then echo \"sabotage=$name computed no section it reaches\"; exit 1; fi\n"
STEP2 = "          (cd reviews/fable5-ym4-03-ci-replay-20261106 && sha256sum --strict -c --quiet SHA256SUMS)\n"
PATH = "      - 'reviews/fable5-ym4-03-ci-replay-20261106/**'\n"
edits = [
    (REACHED, REACHED + GUARD, 1),
    (LAST_CALL, LAST_CALL + CONTROL, 1),
    (STEP2, STEP2 + "          (cd reviews/fable5-ym4-03-ci-replay-check-20261108 && sha256sum --strict -c --quiet SHA256SUMS)\n", 1),
    (PATH, PATH + "      - 'reviews/fable5-ym4-03-ci-replay-check-20261108/**'\n", 2),
]
for old, new, count in edits:
    if text.count(old) != count:
        raise SystemExit("EDIT_COUNT|wanted=%d|found=%d|old=%s" % (count, text.count(old), old.strip()[:60]))
    text = text.replace(old, new)
with open(out, "w", encoding="utf-8", newline="\n") as handle:
    handle.write(text)
print("PROPOSED_WORKFLOW_WRITTEN|json=0")
