"""Run the replay driver or the test under sys.monitoring and record, per section, which lines comparing SABOTAGE with a literal ran.

usage = python3 -I -B -X utf8 instrument.py OUTFILE DRIVER [ARG...]
DRIVER is a tests/one_scale_replay.py; it runs by a plain import, as its own top level runs it, with ARG as its arguments, and its stdout and
stderr are left as they are. The literal lines are read here from the tokens of tests/test_one_scale_blocking.py, independently of the driver: a NAME token
SABOTAGE next to == or != with a string literal on its other side. A section is a top-level function of the test whose name starts with section_,
from its PY_START to its PY_RETURN; FAILED names added to the module's FAILS while it runs are kept with it. OUTFILE gets INSTR_LINE rows (section,
line, literal, hits), INSTR_SECTION rows (order, section, failed names added) and INSTR_DONE with the exit code. Integers only, json=0.
"""
import io
import os
import sys
import tokenize

OUT, SCRIPT, ARGS = sys.argv[1], os.path.abspath(sys.argv[2]), sys.argv[3:]
TEST = os.path.join(os.path.dirname(SCRIPT), "test_one_scale_blocking.py")


def literal_lines(path):
    with open(path, encoding="utf-8") as handle:
        source = handle.read()
    tokens = [t for t in tokenize.generate_tokens(io.StringIO(source).readline) if t.type not in (tokenize.NL, tokenize.COMMENT, tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE)]
    found, other = {}, set()
    for k, t in enumerate(tokens):
        if t.type != tokenize.NAME or t.string != "SABOTAGE":
            continue
        got = None
        for op_at, value_at in ((k + 1, k + 2), (k - 1, k - 2)):
            if 0 <= value_at < len(tokens) and tokens[op_at].string in ("==", "!=") and tokens[value_at].type == tokenize.STRING:
                got = tokens[value_at].string[1:-1]
        if got is None:
            other.add(t.start[0])
        else:
            found.setdefault(t.start[0], set()).add(got)
    return found, other


LITERAL, OTHER = literal_lines(TEST)
M = sys.monitoring
TOOL = M.DEBUGGER_ID
HITS = {}
STACK = []
SECTIONS = []


if os.path.basename(SCRIPT) != "one_scale_replay.py":
    sys.exit(2)
# The test is imported here first, with the sabotage argument alone, as the driver passes it; the driver's own import then finds this module.
sys.argv = [SCRIPT] + [given for given in ARGS[2:] if given.startswith("sabotage=")][:1]
sys.path.insert(0, os.path.dirname(SCRIPT))
import test_one_scale_blocking as BLOCKING  # noqa: E402


def fails_now():
    value = BLOCKING.FAILS
    return value if isinstance(value, list) else []


def is_section(code):
    return code.co_filename == TEST and code.co_name.startswith("section_") and code.co_qualname == code.co_name


def on_start(code, offset):
    if not is_section(code):
        return M.DISABLE
    STACK.append((code.co_name, len(fails_now())))
    return None


def on_return(code, offset, value):
    if not is_section(code):
        return M.DISABLE
    name, before = STACK.pop()
    SECTIONS.append((len(SECTIONS) + 1, name, list(fails_now()[before:])))
    return None


def on_line(code, line):
    if code.co_filename != TEST or line not in LITERAL:
        return M.DISABLE
    key = (STACK[-1][0] if STACK else "none", line)
    HITS[key] = HITS.get(key, 0) + 1
    return None


M.use_tool_id(TOOL, "ym4-03-check-instrument")
M.register_callback(TOOL, M.events.PY_START, on_start)
M.register_callback(TOOL, M.events.PY_RETURN, on_return)
M.register_callback(TOOL, M.events.LINE, on_line)
M.set_events(TOOL, M.events.PY_START | M.events.PY_RETURN | M.events.LINE)
sys.argv = [SCRIPT] + ARGS
code = 0
try:
    import one_scale_replay  # noqa: F401,E402
except SystemExit as stop:
    code = stop.code if isinstance(stop.code, int) else (0 if stop.code is None else 1)
M.set_events(TOOL, 0)
rows = ["INSTR_HEAD|script=%s|args=%s|test=%s|literal_lines=%d|other_reads=%s|json=0" % (os.path.basename(SCRIPT), " ".join(ARGS).replace("|", "_"), TEST, len(LITERAL), ",".join(str(x) for x in sorted(OTHER)) or "none")]
for (section, line), hits in sorted(HITS.items(), key=lambda item: (item[0][1], item[0][0])):
    rows.append("INSTR_LINE|section=%s|line=%d|literal=%s|hits=%d|json=0" % (section, line, ",".join(sorted(LITERAL[line])), hits))
for order, name, added in SECTIONS:
    rows.append("INSTR_SECTION|order=%d|section=%s|failed_added=%d|names=%s|json=0" % (order, name, len(added), ";".join(added).replace("|", "_") or "none"))
rows.append("INSTR_DONE|exit=%d|sections_run=%d|json=0" % (code, len(SECTIONS)))
with open(OUT, "w", encoding="utf-8", newline="\n") as handle:
    handle.write("\n".join(rows) + "\n")
sys.exit(code)
