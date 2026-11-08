"""Write check/proposed/NOTE-YM4-03-ONE-SCALE-BLOCKING.md: the branch note with the sabotage read and the opacity rule as the proposal has them.

usage = python3 -I -B -X utf8 make_proposed_note.py BRANCH_NOTE OUT
Every edit must match exactly once. Integers only, json=0.
"""
import sys

src, out = sys.argv[1], sys.argv[2]
with open(src, encoding="utf-8") as handle:
    text = handle.read()
edits = [
    ("Each sabotage then computes every section whose covered code compares SABOTAGE with its name and prints the other sections' receipt bytes after their sha256 is checked; it must compute one or more sections it reaches, and overlap_skips_next runs once for both its named checks.",
     "Each sabotage then computes every section whose covered code compares SABOTAGE with its name and prints the other sections' receipt bytes after their sha256 is checked; covered code that reads the arguments or the module's names any other way, through argv, getattr, globals, vars, locals, eval, exec, `__dict__`, `__import__` or modules, or holds the word sabotage in a string, counts as reached by every sabotage. The sabotage step's read requires every section the index names as reached to have been computed, and a control that reuses section_loops under reversed_order is refused by that read; overlap_skips_next runs once for both its named checks."),
    ("The measurement, its predictions and its replay are in [`reviews/fable5-ym4-03-ci-replay-20261106/`](../reviews/fable5-ym4-03-ci-replay-20261106/).",
     "The measurement, its predictions and its replay are in [`reviews/fable5-ym4-03-ci-replay-20261106/`](../reviews/fable5-ym4-03-ci-replay-20261106/). An independent check of that replay, with planted cache faults, the instrumented sections and its own back-to-back timing, is in [`reviews/fable5-ym4-03-ci-replay-check-20261108/`](../reviews/fable5-ym4-03-ci-replay-check-20261108/)."),
]
for old, new in edits:
    if text.count(old) != 1:
        raise SystemExit("EDIT_COUNT|found=%d|old=%s" % (text.count(old), old[:60]))
    text = text.replace(old, new)
with open(out, "w", encoding="utf-8", newline="\n") as handle:
    handle.write(text)
print("PROPOSED_NOTE_WRITTEN|json=0")
