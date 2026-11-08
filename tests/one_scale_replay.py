#!/usr/bin/env python3
"""YM4-03: the section replay for the sabotage step of .github/workflows/one-scale-blocking.yml.

usage = one_scale_replay.py record DIR [seeds=PATH]
        one_scale_replay.py replay DIR [sabotage=NAME] [cache_sabotage=NAME]

record runs every section of tests/test_one_scale_blocking.py in full, through its HOOKS, and prints exactly what the test prints; the workflow
compares that with the receipt byte for byte. Beside it, DIR/REPLAY-INDEX.hbp gets one row per section: its key, the receipt bytes it printed with
their sha256, its check count and misses, and the code it covers. It gets one row per level bracket of the flux section as well.

The key of a section is a sha256 over the source of every top-level function and class the section covers, the module's other top-level code, the
values of the module's data at the section's start, the sabotage, empty in the record, and the Python version. The coverage is the union of what
the section ran, read by sys.monitoring, and the static closure of the names it reaches, read from the tokens, so a shared helper counts in every
section that calls it. A sabotage reaches a section when its name is one of the literals compared with SABOTAGE in the covered code; every read of
SABOTAGE there is SABOTAGE == "literal", and any other read makes the unit reached by every sabotage. So does a string holding the word sabotage
in any case, and any of the names in DYNAMIC_READS, through which a unit could read the arguments or the module's names without the token SABOTAGE.

replay imports the test with the sabotage, then for each section: the recorded key must match the current code, the coverage must hold the static
closure, and then a section the sabotage reaches, or one whose data changed, runs in full. Any other section prints its recorded receipt bytes after
their sha256 is checked, and adds its recorded checks and misses. A level bracket whose key, a sha256 over the bracket code, the pencil, top,
wanted and shift, has a recorded row is certified again by count_above at its low and high ends before it is used; a pencil a sabotage changed has
another key, and bisect_level computes it.

A seed file for record holds level bracket rows. A seed is used when count_above certifies it, and the pair it certifies is the one bisect_level
returns, since count_above is non-increasing in the value (the pencil's G is a Gram matrix); bisect_level runs as well on every pencil of dimension at most
CROSSCHECK_DIMENSION, and a difference exits 1.

A failed replay check prints FAILED|check=replay_...|json=0 and exits 1. cache_sabotage names the controls for the replay itself. Three must fail here:
key_misses_helper drops block_map from section_covariance's coverage and rewrites its key to match; row_tampered changes one byte of the receipt
inside section_covariance's rows; stale_bracket moves every recorded level bracket up by one. reuse_reached reuses every section, those the
sabotage reaches too, so the run prints the passing receipt and exits 0, and the workflow's sabotage step, which needs exit 1 and the named line,
refuses it. An unknown name exits 2.
Python standard library, integers only, json=0.
"""
import hashlib
import io
import os
import sys
import time
import tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
MODULE_PATH = os.path.join(HERE, "test_one_scale_blocking.py")
RECEIPT_PATH = os.path.join(HERE, "ONE_SCALE_BLOCKING_RECEIPT.txt")
INDEX_NAME = "REPLAY-INDEX.hbp"
FORMAT = "1"
CACHE_SABOTAGE_NAMES = ("key_misses_helper", "row_tampered", "stale_bracket", "reuse_reached")
CROSSCHECK_DIMENSION = 12
# Names through which a unit could read the sabotage without the token SABOTAGE; any of them makes the unit reached by every sabotage.
DYNAMIC_READS = ("argv", "getattr", "globals", "vars", "locals", "eval", "exec", "__dict__", "__import__", "modules")
# The module's data, digested at each section's start, and its bookkeeping, which the replay carries by itself.
DATA_NAMES = ("SABOTAGE_NAMES", "Q_ONE", "MAT_ONE", "GROUPS", "Q8_ELEMENTS", "T2_ELEMENTS", "T2_QUATS", "BITS", "CENTER")
BOOK_NAMES = ("START_NS", "SABOTAGE", "FAILS", "MISSES", "CHECKS", "HOOKS", "SINGLE_POWER", "argument")


def usage():
    print("usage = one_scale_replay.py record DIR [seeds=PATH] | one_scale_replay.py replay DIR [sabotage=NAME] [cache_sabotage=NAME]")
    sys.exit(2)


ARGS = sys.argv[1:]
if len(ARGS) < 2 or ARGS[0] not in ("record", "replay"):
    usage()
MODE = ARGS[0]
CACHE_DIR = ARGS[1]
SEEDS_PATH = ""
PASSED = []
CACHE_SABOTAGE = ""
for given in ARGS[2:]:
    word, _, value = given.partition("=")
    if MODE == "record" and word == "seeds" and value and not SEEDS_PATH:
        SEEDS_PATH = value
    elif MODE == "replay" and word == "sabotage" and not PASSED:
        PASSED = [given]
    elif MODE == "replay" and word == "cache_sabotage" and value in CACHE_SABOTAGE_NAMES and not CACHE_SABOTAGE:
        CACHE_SABOTAGE = value
    else:
        usage()
# The test reads its sabotage from its own arguments, and exits 2 on an unknown name.
sys.argv[1:] = PASSED
sys.path.append(HERE)
import test_one_scale_blocking as blocking  # noqa: E402

PYTHON = "%s-%d.%d.%d" % (sys.implementation.name, sys.version_info[0], sys.version_info[1], sys.version_info[2])


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def note(text):
    print(text, file=sys.stderr, flush=True)


def refuse(check, reason):
    """A replay check that failed: the named line, the reason on stderr, and exit 1."""
    note("REPLAY_REFUSED|check=%s|reason=%s|json=0" % (check, reason))
    sys.stdout.write("FAILED|check=%s|json=0\n" % check)
    sys.stdout.flush()
    sys.exit(1)


# ---- The module read from its tokens: top-level units, the names each one reaches, and the sabotage literals in it.


def simple_literal(token):
    text = token.string
    if len(text) < 3 or text[0] not in "\"'" or text[-1] != text[0]:
        return None
    inner = text[1:-1]
    if not all(c in "abcdefghijklmnopqrstuvwxyz0123456789_" for c in inner):
        return None
    return inner


def read_module(path):
    with open(path, "rb") as handle:
        data = handle.read()
    source = data.decode("utf-8")
    lines = source.split("\n")
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    skip = (tokenize.NL, tokenize.COMMENT, tokenize.ENCODING, tokenize.ENDMARKER, tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE)
    starts = []
    depth = 0
    fresh = True
    for position, token in enumerate(tokens):
        if token.type == tokenize.INDENT:
            depth += 1
        elif token.type == tokenize.DEDENT:
            depth -= 1
        elif token.type == tokenize.NEWLINE:
            fresh = True
        if token.type in skip:
            continue
        if fresh and depth == 0:
            starts.append((token.start[0], position))
        fresh = False
    statements = []
    for k, (line, position) in enumerate(starts):
        last = starts[k + 1][0] - 1 if k + 1 < len(starts) else len(lines)
        while last > line and (not lines[last - 1].strip() or lines[last - 1].startswith("#")):
            last -= 1
        statements.append([line, last, position])
    # A decorator line joins the statement it decorates.
    merged = []
    for item in statements:
        if merged and tokens[merged[-1][2]].string == "@":
            merged[-1][1] = item[1]
            merged[-1].append(item[2])
        else:
            merged.append(item)
    units = {}
    order = []
    code_parts = []
    assigned = set()
    blockers = []
    for item in merged:
        line, last, position = item[0], item[1], item[-1]
        head = tokens[position]
        kind, name = "code", ""
        if head.string == "async" and tokens[position + 1].string == "def":
            position += 1
            head = tokens[position]
        if head.string in ("def", "class"):
            kind, name = head.string, tokens[position + 1].string
        text = "\n".join(lines[line - 1:last])
        if kind == "code":
            code_parts.append(text)
            assigned |= targets_of(tokens, line, last)
            # At the top level SABOTAGE is only assigned; a read there would set data by the sabotage, so the cache is then left unused.
            if module_reads_sabotage(tokens, line, last):
                blockers.append("SABOTAGE_read_at_top_level")
            continue
        if name in units:
            blockers.append("bound_twice_" + name)
        units[name] = {"kind": kind, "first": line, "last": last, "digest": sha(text)}
        order.append(name)
    significant = [t for t in tokens if t.type not in (tokenize.NL, tokenize.COMMENT, tokenize.ENCODING, tokenize.INDENT, tokenize.DEDENT)]
    for name in order:
        unit = units[name]
        own = [t for t in significant if unit["first"] <= t.start[0] <= unit["last"]]
        names, attributes, methods, literals = set(), set(), set(), set()
        opaque = False
        for k, t in enumerate(own):
            if t.type == tokenize.STRING and "sabotage" in t.string.lower():
                opaque = True
            if t.type == tokenize.NAME and t.string in DYNAMIC_READS:
                opaque = True
            if t.type != tokenize.NAME:
                continue
            before = own[k - 1] if k else None
            if before is not None and before.type == tokenize.OP and before.string == ".":
                attributes.add(t.string)
            else:
                names.add(t.string)
            if unit["kind"] == "class" and t.string == "def" and k + 1 < len(own):
                methods.add(own[k + 1].string)
            if t.string == "SABOTAGE":
                literal = sabotage_literal(own, k)
                if literal is None or literal not in blocking.SABOTAGE_NAMES:
                    opaque = True
                else:
                    literals.add(literal)
        unit.update(names=names, attributes=attributes, methods=methods, literals=literals, opaque=opaque)
    owner = [""] * (len(lines) + 2)
    for name in order:
        for line in range(units[name]["first"], units[name]["last"] + 1):
            owner[line] = name
    return {"units": units, "order": order, "code": sha("\n#\n".join(code_parts)), "assigned": assigned, "blockers": blockers, "owner": owner, "file": sha_bytes(data)}


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def module_reads_sabotage(tokens, first, last):
    """True when a top-level statement holds SABOTAGE anywhere but as the target of a plain =."""
    own = [t for t in tokens if first <= t.start[0] <= last and t.type not in (tokenize.NL, tokenize.COMMENT, tokenize.INDENT, tokenize.DEDENT)]
    for k, t in enumerate(own):
        if t.type == tokenize.NAME and t.string == "SABOTAGE":
            after = own[k + 1] if k + 1 < len(own) else None
            if after is None or after.type != tokenize.OP or after.string != "=":
                return True
    return False


def targets_of(tokens, first, last):
    """Names a module-level statement binds: those left of an = at bracket depth 0, and the target of a for."""
    out = set()
    line_tokens = []
    for t in tokens:
        if first <= t.start[0] <= last:
            if t.type == tokenize.NEWLINE:
                out |= line_targets(line_tokens)
                line_tokens = []
            elif t.type not in (tokenize.NL, tokenize.COMMENT, tokenize.INDENT, tokenize.DEDENT):
                line_tokens.append(t)
    out |= line_targets(line_tokens)
    return out


def line_targets(line_tokens):
    out = set()
    if line_tokens and line_tokens[0].string in ("import", "from"):
        return out
    if line_tokens and line_tokens[0].string == "for":
        for t in line_tokens[1:]:
            if t.string == "in":
                break
            if t.type == tokenize.NAME:
                out.add(t.string)
        return out
    depth = 0
    cut = None
    for k, t in enumerate(line_tokens):
        if t.string in ("(", "[", "{"):
            depth += 1
        elif t.string in (")", "]", "}"):
            depth -= 1
        elif depth == 0 and t.type == tokenize.OP and t.string in ("=", "+=", "-=", "*=", "|=", "&=", "^=", "//=", "%=", "<<=", ">>="):
            cut = k
    if cut is None:
        return out
    for k in range(cut):
        t = line_tokens[k]
        before = line_tokens[k - 1] if k else None
        if t.type == tokenize.NAME and not (before is not None and before.string == "."):
            out.add(t.string)
    return out


def sabotage_literal(own, k):
    """The literal in SABOTAGE == "literal" or "literal" == SABOTAGE around position k, or None for any other read."""
    stop = ("(", "[", ".", "+", "*", "%", "@")

    def at(j):
        return own[j] if 0 <= j < len(own) else None

    before, after = at(k - 1), at(k + 1)
    if before is not None and before.type == tokenize.OP and before.string == ".":
        return None
    if after is not None and after.type == tokenize.OP and after.string in ("==", "!="):
        value, follow = at(k + 2), at(k + 3)
        if value is None or value.type != tokenize.STRING:
            return None
        if follow is not None and (follow.type == tokenize.STRING or (follow.type == tokenize.OP and follow.string in stop)):
            return None
        return simple_literal(value)
    if before is not None and before.type == tokenize.OP and before.string in ("==", "!="):
        value, lead = at(k - 2), at(k - 3)
        if value is None or value.type != tokenize.STRING:
            return None
        if lead is not None and not ((lead.type == tokenize.OP and lead.string in ("(", ",", "=", ":", "[")) or (lead.type == tokenize.NAME and lead.string in ("if", "and", "or", "not", "return", "else", "elif", "while"))):
            return None
        if after is not None and after.type == tokenize.OP and after.string in stop:
            return None
        return simple_literal(value)
    return None


def closure(model, roots):
    """Every unit reachable from roots by a plain name, or by an attribute that names a method of a module class."""
    units = model["units"]
    method_owner = {}
    for name in model["order"]:
        for method in units[name]["methods"]:
            method_owner.setdefault(method, set()).add(name)
    seen = set()
    work = [r for r in roots if r in units]
    while work:
        name = work.pop()
        if name in seen:
            continue
        seen.add(name)
        unit = units[name]
        for other in unit["names"]:
            if other in units and other not in seen:
                work.append(other)
        for attribute in unit["attributes"]:
            for other in method_owner.get(attribute, ()):
                if other not in seen:
                    work.append(other)
    return seen


def reach(model, covered):
    """The sabotage names that reach a set of units, with every name when one of them reads SABOTAGE any other way."""
    out = set()
    for name in covered:
        unit = model["units"].get(name)
        if unit is None or unit["opaque"]:
            return set(blocking.SABOTAGE_NAMES)
        out |= unit["literals"]
    return out


# ---- The module's data, as one canonical string.


def canon(value, out):
    if value is None:
        out.append("N")
    elif isinstance(value, bool):
        out.append("B%d" % int(value))
    elif isinstance(value, int):
        out.append("I%x" % value)
    elif isinstance(value, str):
        out.append("S%d:%s" % (len(value), value))
    elif isinstance(value, (tuple, list)):
        out.append("T(" if isinstance(value, tuple) else "L(")
        for item in value:
            canon(item, out)
            out.append(",")
        out.append(")")
    elif isinstance(value, dict):
        parts = []
        for key, item in value.items():
            k_out, v_out = [], []
            canon(key, k_out)
            canon(item, v_out)
            parts.append(("".join(k_out), "".join(v_out)))
        out.append("D(")
        for k_text, v_text in sorted(parts):
            out.append(k_text + ":" + v_text + ",")
        out.append(")")
    elif isinstance(value, (set, frozenset)):
        parts = []
        for item in value:
            item_out = []
            canon(item, item_out)
            parts.append("".join(item_out))
        out.append("Z(" + ",".join(sorted(parts)) + ")")
    elif isinstance(value, blocking.Group):
        out.append("G")
        canon((value.name, value.n, value.table, value.identity, value.inverse, value.classes, value.class_of), out)
    else:
        raise ValueError("no canonical form for a value of the module's data")


def inputs_digest():
    out = []
    for value in (blocking.SABOTAGE_NAMES, blocking.Q_ONE, blocking.MAT_ONE, blocking.GROUPS, blocking.Q8_ELEMENTS, blocking.T2_ELEMENTS, blocking.T2_QUATS, blocking.BITS, blocking.CENTER):
        canon(value, out)
        out.append(";")
    return sha("".join(out))


# ---- Keys.


def unit_list(model, covered):
    return ",".join("%s:%s" % (name, model["units"][name]["digest"]) for name in sorted(covered))


def section_key(section, units_text, module_code, inputs, sabotage):
    return sha("YM4_03_REPLAY_KEY|format=%s|section=%s|units=%s|module_code=%s|inputs=%s|sabotage=%s|python=%s|json=0" % (FORMAT, section, units_text, module_code, inputs, sabotage, PYTHON))


MODEL = read_module(MODULE_PATH)
BRACKET_UNITS = closure(MODEL, ["bisect_level", "count_above"])
BRACKET_CODE = sha(unit_list(MODEL, BRACKET_UNITS))


def bracket_key(pencil, top, wanted, shift):
    h = hashlib.sha256()
    h.update(("YM4_03_BRACKET_KEY|format=%s|code=%s|top=%x|wanted=%x|shift=%x|" % (FORMAT, BRACKET_CODE, top, wanted, shift)).encode("utf-8"))
    for matrix in pencil:
        for row in matrix:
            h.update((",".join("%x" % x for x in row) + ";").encode("utf-8"))
        h.update(b"#")
    return h.hexdigest()


def certified(pencil, top, wanted, shift, low, high):
    """True when (low, high) is the pair bisect_level returns: read by count_above, which falls as the value rises. With top at most 1,
    bisect_level takes at most one count_above, and the pair is compared with its own."""
    if top <= 1:
        return (low, high) == blocking.bisect_level(pencil, top, wanted, shift)
    if low == 0 and high == 0:
        return blocking.count_above(pencil, 0, shift) < wanted
    if not (0 <= low and high == low + 1 and high <= top):
        return False
    if blocking.count_above(pencil, low, shift) < wanted:
        return False
    return high == top or blocking.count_above(pencil, high, shift) < wanted


def read_rows(path, tag):
    out = []
    with open(path, encoding="utf-8") as handle:
        for line in handle.read().split("\n"):
            if not line.startswith(tag + "|"):
                continue
            fields = {}
            for part in line.split("|")[1:]:
                k, _, v = part.partition("=")
                fields[k] = v
            out.append(fields)
    return out


def hex_names(names):
    return ",".join(name.encode("utf-8").hex() for name in names) if names else "none"


def names_of(text):
    return [] if text == "none" else [bytes.fromhex(part).decode("utf-8") for part in text.split(",")]


class Counted:
    """stdout, with every byte written counted and kept, so each section's rows are a slice of what the run printed."""

    def __init__(self, inner):
        self.inner = inner
        self.parts = []
        self.size = 0

    def write(self, text):
        self.inner.write(text)
        self.parts.append(text)
        self.size += len(text.encode("utf-8"))
        return len(text)

    def flush(self):
        self.inner.flush()


STATE = {"order": 0, "current": None, "seen": set(), "entries": [], "brackets": [], "seeded": 0, "bisected": 0, "crosschecked": 0, "frozen": 0, "reused": 0, "computed": 0}


# ---- record


def on_start(code, offset):
    if STATE["current"] is not None and code.co_filename == blocking.__file__:
        STATE["seen"].add(code.co_firstlineno)
    return sys.monitoring.DISABLE


def record_section(function):
    section = function.__name__
    STATE["order"] += 1
    out = sys.stdout
    begin_bytes = out.size
    begin_checks, begin_fails, begin_misses = blocking.CHECKS[0], len(blocking.FAILS), len(blocking.MISSES)
    inputs = inputs_digest()
    STATE["seen"] = set()
    STATE["current"] = section
    if MONITORING:
        sys.monitoring.restart_events()
    t0 = time.perf_counter_ns()
    try:
        returned = function()
    finally:
        STATE["current"] = None
    t1 = time.perf_counter_ns()
    inputs_after = inputs_digest()
    dynamic = {MODEL["owner"][line] for line in STATE["seen"] if 0 < line < len(MODEL["owner"])} - {""}
    static = closure(MODEL, [section])
    covered = dynamic | static
    data = "".join(out.parts).encode("utf-8")[begin_bytes:out.size]
    reusable = READY and inputs == inputs_after and (returned is None or (isinstance(returned, int) and not isinstance(returned, bool)))
    units_text = unit_list(MODEL, covered)
    entry = {
        "order": STATE["order"], "section": section, "key": section_key(section, units_text, MODEL["code"], inputs, ""), "reusable": int(reusable),
        "offset": begin_bytes, "bytes": len(data), "rows_sha256": sha_bytes(data), "checks": blocking.CHECKS[0] - begin_checks,
        "fails": hex_names(blocking.FAILS[begin_fails:]), "misses": hex_names(blocking.MISSES[begin_misses:]),
        "returned": "none" if returned is None else ("int:%d" % returned if isinstance(returned, int) else "other"), "inputs": inputs, "inputs_after": inputs_after,
        "ms": (t1 - t0) // 1000000, "dynamic": len(dynamic) if MONITORING else -1, "static": len(static), "dynamic_only": ",".join(sorted(dynamic - static)) or "none",
        "reach": ",".join(sorted(reach(MODEL, covered))) or "none", "units": units_text,
    }
    STATE["entries"].append(entry)
    note("REPLAY|order=%d|section=%s|mode=recorded|ms=%d|units=%d|dynamic=%d|reach=%s|reusable=%d|json=0" % (entry["order"], section, entry["ms"], len(covered), entry["dynamic"], entry["reach"], entry["reusable"]))
    return returned


def record_bracket(pencil, top, wanted, shift):
    key = bracket_key(pencil, top, wanted, shift)
    seed = SEEDS.get(key)
    dimension = len(pencil[0])
    result = None
    source = "bisect"
    if seed is not None and certified(pencil, top, wanted, shift, seed[0], seed[1]):
        result = seed
        source = "seed"
        STATE["seeded"] += 1
        if dimension <= CROSSCHECK_DIMENSION:
            STATE["crosschecked"] += 1
            if blocking.bisect_level(pencil, top, wanted, shift) != seed:
                refuse("replay_seed_differs_from_bisection", "key=%s" % key)
    else:
        result = blocking.bisect_level(pencil, top, wanted, shift)
        STATE["bisected"] += 1
    STATE["brackets"].append((len(STATE["brackets"]) + 1, key, result[0], result[1], dimension, source, STATE["current"] or "none"))
    return result


def write_index(exit_code, stdout_data):
    os.makedirs(CACHE_DIR, exist_ok=True)
    rows = []
    rows.append("REPLAY_INDEX|format=%s|module=tests/test_one_scale_blocking.py|module_sha256=%s|module_code=%s|stdout_sha256=%s|stdout_bytes=%d|exit=%d|python=%s|monitoring=%d|ready=%d|seeds=%s|seeds_sha256=%s|json=0" % (
        FORMAT, MODEL["file"], MODEL["code"], sha_bytes(stdout_data), len(stdout_data), exit_code, PYTHON, int(MONITORING), int(READY), SEEDS_NAME, SEEDS_SHA256))
    fields = ("order", "section", "key", "reusable", "offset", "bytes", "rows_sha256", "checks", "fails", "misses", "returned", "inputs", "inputs_after", "ms", "dynamic", "static", "dynamic_only", "reach", "units")
    for entry in STATE["entries"]:
        rows.append("REPLAY_SECTION|" + "|".join("%s=%s" % (f, entry[f]) for f in fields) + "|json=0")
    for order, key, low, high, dimension, source, section in STATE["brackets"]:
        rows.append("LEVEL_BRACKET|order=%d|key=%s|low=%d|high=%d|dimension=%d|source=%s|section=%s|json=0" % (order, key, low, high, dimension, source, section))
    rows.append("REPLAY_DONE|sections=%d|brackets=%d|seeded=%d|bisected=%d|crosschecked=%d|json=0" % (len(STATE["entries"]), len(STATE["brackets"]), STATE["seeded"], STATE["bisected"], STATE["crosschecked"]))
    text = "\n".join(rows) + "\n"
    path = os.path.join(CACHE_DIR, INDEX_NAME)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    with open(path + ".sha256", "w", encoding="utf-8", newline="\n") as handle:
        handle.write("%s  %s\n" % (sha(text), INDEX_NAME))
    note("REPLAY_INDEX|path=%s|sha256=%s|sections=%d|brackets=%d|seeded=%d|bisected=%d|crosschecked=%d|json=0" % (path, sha(text), len(STATE["entries"]), len(STATE["brackets"]), STATE["seeded"], STATE["bisected"], STATE["crosschecked"]))


# ---- replay


def replay_section(function):
    section = function.__name__
    k = STATE["order"]
    STATE["order"] += 1
    if k >= len(ENTRIES) or ENTRIES[k]["section"] != section:
        refuse("replay_order_%s" % section, "the recorded index holds another section at position %d" % (k + 1))
    entry = ENTRIES[k]
    recorded = {}
    for part in entry["units"].split(","):
        name, _, digest = part.partition(":")
        recorded[name] = digest
    for name, digest in sorted(recorded.items()):
        unit = MODEL["units"].get(name)
        if unit is None or unit["digest"] != digest:
            refuse("replay_key_stale_%s" % section, "unit=%s|recorded=%s|now=%s" % (name, digest, unit["digest"] if unit else "absent"))
    if INDEX["module_code"] != MODEL["code"] or INDEX["python"] != PYTHON or INDEX["format"] != FORMAT:
        refuse("replay_key_stale_%s" % section, "module_code_or_python_or_format")
    if section_key(section, entry["units"], INDEX["module_code"], entry["inputs"], "") != entry["key"]:
        refuse("replay_key_corrupt_%s" % section, "the key does not hash its own fields")
    missing = sorted(closure(MODEL, [section]) - set(recorded))
    if missing:
        refuse("replay_coverage_misses_helper_%s" % section, "missing=%s" % ",".join(missing))
    reached = reach(MODEL, set(recorded))
    inputs = inputs_digest()
    why = ""
    if entry["reusable"] != "1":
        why = "recorded_not_reusable"
    elif blocking.SABOTAGE and blocking.SABOTAGE in reached and CACHE_SABOTAGE != "reuse_reached":
        why = "reached_by_%s" % blocking.SABOTAGE
    elif inputs != entry["inputs"]:
        why = "inputs_changed"
    if why:
        STATE["computed"] += 1
        t0 = time.perf_counter_ns()
        returned = function()
        note("REPLAY|order=%d|section=%s|mode=computed|why=%s|ms=%d|json=0" % (k + 1, section, why, (time.perf_counter_ns() - t0) // 1000000))
        return returned
    offset, size = int(entry["offset"]), int(entry["bytes"])
    data = RECEIPT[offset:offset + size]
    if len(data) != size or sha_bytes(data) != entry["rows_sha256"]:
        refuse("replay_rows_sha256_%s" % section, "offset=%d|bytes=%d|recorded=%s|receipt=%s" % (offset, size, entry["rows_sha256"], sha_bytes(data)))
    text = data.decode("utf-8")
    fails = [line[len("FAILED|check="):-len("|json=0")] for line in text.split("\n") if line.startswith("FAILED|check=")]
    misses = [line.split("|row=", 1)[1].split("|", 1)[0] for line in text.split("\n") if line.startswith("YM4_03_READ|") and "|result=MISS|" in line]
    if fails != names_of(entry["fails"]) or misses != names_of(entry["misses"]):
        refuse("replay_rows_bookkeeping_%s" % section, "the rows' FAILED and MISS lines differ from the recorded lists")
    sys.stdout.write(text)
    sys.stdout.flush()
    blocking.CHECKS[0] += int(entry["checks"])
    blocking.FAILS.extend(fails)
    blocking.MISSES.extend(misses)
    STATE["reused"] += 1
    note("REPLAY|order=%d|section=%s|mode=reused|bytes=%d|checks=%s|json=0" % (k + 1, section, size, entry["checks"]))
    returned = entry["returned"]
    if returned == "none":
        return None
    if returned.startswith("int:"):
        return int(returned[4:])
    refuse("replay_returned_%s" % section, "returned=%s" % returned)
    return None


def replay_bracket(pencil, top, wanted, shift):
    if BRACKETS_REACHED:
        STATE["bisected"] += 1
        return blocking.bisect_level(pencil, top, wanted, shift)
    key = bracket_key(pencil, top, wanted, shift)
    row = FROZEN.get(key)
    if row is None:
        STATE["bisected"] += 1
        return blocking.bisect_level(pencil, top, wanted, shift)
    if not certified(pencil, top, wanted, shift, row[0], row[1]):
        refuse("replay_bracket_stale", "key=%s|low=%d|high=%d" % (key, row[0], row[1]))
    STATE["frozen"] += 1
    return row


def load_index():
    path = os.path.join(CACHE_DIR, INDEX_NAME)
    try:
        with open(path, "rb") as handle:
            data = handle.read()
        with open(path + ".sha256", encoding="utf-8") as handle:
            recorded = handle.read().split(" ", 1)[0]
    except OSError:
        refuse("replay_index_present", "path=%s" % path)
    if sha_bytes(data) != recorded:
        refuse("replay_index_sha256", "recorded=%s|now=%s" % (recorded, sha_bytes(data)))
    heads = read_rows(path, "REPLAY_INDEX")
    if len(heads) != 1:
        refuse("replay_index_sha256", "header rows=%d" % len(heads))
    return heads[0], read_rows(path, "REPLAY_SECTION"), read_rows(path, "LEVEL_BRACKET")


if os.path.abspath(blocking.__file__) != MODULE_PATH:
    usage()
MONITORING = MODE == "record" and sys.version_info >= (3, 12)
SEEDS = {}
SEEDS_NAME, SEEDS_SHA256 = "none", "none"
FROZEN = {}
ENTRIES = []
INDEX = {}
RECEIPT = b""
BRACKETS_REACHED = False
# The cache is usable when the module's top-level names are the ones listed above, none bound twice, and SABOTAGE only assigned at the top level.
READY = not MODEL["blockers"] and MODEL["assigned"] <= set(DATA_NAMES) | set(BOOK_NAMES) and set(DATA_NAMES) <= MODEL["assigned"]
if not READY:
    note("REPLAY_NOT_READY|blockers=%s|unlisted=%s|json=0" % (",".join(MODEL["blockers"]) or "none", ",".join(sorted(MODEL["assigned"] - set(DATA_NAMES) - set(BOOK_NAMES))) or "none"))
if MODE == "record":
    if SEEDS_PATH:
        with open(SEEDS_PATH, "rb") as handle:
            SEEDS_SHA256 = sha_bytes(handle.read())
        SEEDS_NAME = SEEDS_PATH.replace("|", "_")
        for row in read_rows(SEEDS_PATH, "LEVEL_BRACKET"):
            SEEDS[row["key"]] = (int(row["low"]), int(row["high"]))
    if MONITORING:
        sys.monitoring.use_tool_id(sys.monitoring.COVERAGE_ID, "ym4-03-replay")
        sys.monitoring.register_callback(sys.monitoring.COVERAGE_ID, sys.monitoring.events.PY_START, on_start)
        sys.monitoring.set_events(sys.monitoring.COVERAGE_ID, sys.monitoring.events.PY_START)
    blocking.HOOKS["section"] = record_section
    blocking.HOOKS["bracket"] = record_bracket
else:
    INDEX, ENTRIES, frozen_rows = load_index()
    with open(RECEIPT_PATH, "rb") as handle:
        RECEIPT = handle.read()
    if CACHE_SABOTAGE == "key_misses_helper":
        for entry in ENTRIES:
            if entry["section"] == "section_covariance":
                kept = [part for part in entry["units"].split(",") if part.partition(":")[0] != "block_map"]
                entry["units"] = ",".join(kept)
                entry["key"] = section_key(entry["section"], entry["units"], INDEX["module_code"], entry["inputs"], "")
    if CACHE_SABOTAGE == "row_tampered":
        for entry in ENTRIES:
            if entry["section"] == "section_covariance":
                at = int(entry["offset"]) + 8
                RECEIPT = RECEIPT[:at] + bytes([RECEIPT[at] ^ 1]) + RECEIPT[at + 1:]
    for row in frozen_rows:
        shift_up = 1 if CACHE_SABOTAGE == "stale_bracket" else 0
        FROZEN[row["key"]] = (int(row["low"]) + shift_up, int(row["high"]) + shift_up)
    BRACKETS_REACHED = blocking.SABOTAGE in reach(MODEL, BRACKET_UNITS)
    blocking.HOOKS["section"] = replay_section
    blocking.HOOKS["bracket"] = replay_bracket
    note("REPLAY_START|sabotage=%s|cache_sabotage=%s|sections=%d|brackets=%d|brackets_reached=%d|json=0" % (blocking.SABOTAGE or "none", CACHE_SABOTAGE or "none", len(ENTRIES), len(FROZEN), int(BRACKETS_REACHED)))

COUNTED = Counted(sys.stdout)
sys.stdout = COUNTED
EXIT = blocking.main()
sys.stdout = COUNTED.inner
if MODE == "record":
    write_index(EXIT, "".join(COUNTED.parts).encode("utf-8"))
else:
    note("REPLAY_DONE|sabotage=%s|reused=%d|computed=%d|brackets_certified=%d|brackets_bisected=%d|exit=%d|json=0" % (blocking.SABOTAGE or "none", STATE["reused"], STATE["computed"], STATE["frozen"], STATE["bisected"], EXIT))
sys.exit(EXIT)
