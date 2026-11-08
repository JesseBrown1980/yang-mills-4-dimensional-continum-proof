# YM4-03C engine check: copy a file with each OLD text replaced by its NEW text, every occurrence, for a planted error.
# Usage: python3 -I -B -X utf8 edit_text.py SRC DST OLD1 NEW1 [OLD2 NEW2 ...]. Exits 1 if an OLD text is absent. json=0.
import sys


def main():
    src, dst = sys.argv[1], sys.argv[2]
    pairs = sys.argv[3:]
    if len(pairs) == 0 or len(pairs) % 2 != 0:
        sys.stdout.write("EDIT|failed=pairs|json=0\n")
        return 1
    with open(src, "r", encoding="utf-8", newline="") as f:
        t = f.read()
    for i in range(0, len(pairs), 2):
        n = t.count(pairs[i])
        sys.stdout.write("EDIT|occurrences=%d|json=0\n" % n)
        if n == 0:
            return 1
        t = t.replace(pairs[i], pairs[i + 1])
    with open(dst, "w", encoding="utf-8", newline="") as f:
        f.write(t)
    return 0


sys.exit(main())
