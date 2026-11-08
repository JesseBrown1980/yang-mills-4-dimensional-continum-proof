"""A reader for the shape of these GitHub workflow files, standard library only: the jobs, each step's name and run text, and the on: paths.

read_workflow(path) returns {"on": {event: {"paths": [...], "branches": [...]}}, "jobs": [(job, [{"name": ..., "run": ...}, ...])]}.
A run given as a literal block (run: |) is its lines less the block's indentation, with one final newline, as YAML's clip reads it; a run on one
line is that line's text. A step with no run has none. Only the forms these files use are read: a plain or single-quoted scalar, a block
sequence of scalars, a flow sequence [a, b], and a literal block. Integers only, json=0.
"""


def scalar(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == "'" and text[-1] == "'":
        return text[1:-1].replace("''", "'")
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        return text[1:-1]
    cut = text.find(" #")
    return (text[:cut] if cut >= 0 else text).rstrip()


def indent_of(line):
    return len(line) - len(line.lstrip(" "))


def literal_block(lines, start, parent):
    """The literal block after a key at indentation parent, from lines[start]; returns (text, next index)."""
    k = start
    body = []
    width = None
    while k < len(lines):
        line = lines[k]
        if line.strip() and indent_of(line) <= parent:
            break
        if line.strip() and width is None:
            width = indent_of(line)
        body.append(line)
        k += 1
    while body and not body[-1].strip():
        body.pop()
    width = width or 0
    return "".join(line[width:] + "\n" for line in body), k


def read_workflow(path):
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().split("\n")
    out = {"on": {}, "jobs": []}
    k = 0
    section = None
    event = None
    listing = None
    job = None
    step = None
    while k < len(lines):
        line = lines[k]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            k += 1
            continue
        level = indent_of(line)
        if level == 0:
            section = stripped.rstrip(":").split(":", 1)[0]
            event = listing = job = step = None
            k += 1
            continue
        if section == "on":
            if level == 2:
                event = stripped.rstrip(":")
                out["on"][event] = {}
                listing = None
            elif level == 4 and event is not None:
                key, _, rest = stripped.partition(":")
                rest = rest.strip()
                if rest.startswith("[") and rest.endswith("]"):
                    out["on"][event][key] = [scalar(x) for x in rest[1:-1].split(",") if x.strip()]
                    listing = None
                else:
                    out["on"][event][key] = []
                    listing = key
            elif level >= 6 and listing is not None and stripped.startswith("- "):
                out["on"][event][listing].append(scalar(stripped[2:]))
            k += 1
            continue
        if section == "jobs":
            if level == 2:
                job = (stripped.rstrip(":"), [])
                out["jobs"].append(job)
                step = None
                k += 1
                continue
            if job is not None and level == 6 and stripped.startswith("- "):
                step = {}
                job[1].append(step)
                stripped = stripped[2:]
                level = 8
            if step is not None and level == 8:
                key, _, rest = stripped.partition(":")
                rest = rest.strip()
                if key == "run" and rest == "|":
                    step["run"], k = literal_block(lines, k + 1, 8)
                    continue
                if key in ("name", "run", "uses"):
                    step[key] = scalar(rest)
            k += 1
            continue
        k += 1
    return out
