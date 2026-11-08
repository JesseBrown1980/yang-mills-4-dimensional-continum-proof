"""Write check/proposed/one_scale_replay.py: the branch driver with a wider opacity rule. Integers only, json=0."""
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
with open(src_path, encoding="utf-8") as handle:
    text = handle.read()
edits = [
    ('SABOTAGE there is SABOTAGE == "literal", and any other read makes the unit reached by every sabotage.\n',
     'SABOTAGE there is SABOTAGE == "literal", and any other read makes the unit reached by every sabotage. So does a string holding the word sabotage\n'
     'in any case, and any of the names in DYNAMIC_READS, through which a unit could read the arguments or the module\'s names without the token SABOTAGE.\n'),
    ('CROSSCHECK_DIMENSION = 12\n',
     'CROSSCHECK_DIMENSION = 12\n'
     '# Names through which a unit could read the sabotage without the token SABOTAGE; any of them makes the unit reached by every sabotage.\n'
     'DYNAMIC_READS = ("argv", "getattr", "globals", "vars", "locals", "eval", "exec", "__dict__", "__import__", "modules")\n'),
    ('            if t.type == tokenize.STRING and "SABOTAGE" in t.string:\n',
     '            if t.type == tokenize.STRING and "sabotage" in t.string.lower():\n                opaque = True\n'
     '            if t.type == tokenize.NAME and t.string in DYNAMIC_READS:\n'),
]
for old, new in edits:
    if text.count(old) != 1:
        raise SystemExit("EDIT_NOT_UNIQUE|old=%r" % old[:60])
    text = text.replace(old, new)
with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
    handle.write(text)
print("PROPOSED_WRITTEN|json=0")
