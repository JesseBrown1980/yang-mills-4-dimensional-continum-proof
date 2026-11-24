#!/usr/bin/env python3
"""Integrity gate for tracked Markdown files.

Checks on every tracked *.md file:

1. Control characters. Only the newline byte is allowed below 0x20, and 0x7f
   is refused. LaTeX source written through a non-raw string turns \\beta,
   \\rho and \\text into a backspace, a carriage return and a tab, and the
   rendered page then shows "eta", "ho" and "ext". This happened to
   README.md and BRIDGE-LEDGER.md on 22 November 2026.
2. Relative link targets. These are inline links [text](target), including
   <target> and an optional "title", and reference definitions
   [label]: target. Every target that is not a URL, a mailto or a pure
   #anchor must name an existing file or folder, resolved from the linking
   file's own folder.
3. Reference labels. Every full or collapsed reference link, [text][label]
   or [text][], must have a matching [label]: definition in the same file.
4. Section anchors. A #anchor on a link to a Markdown file (or a bare
   #anchor in the same file) must match a heading slug of that file, as
   GitHub generates it, or an explicit id or name attribute in that file.

Text inside fenced code blocks, inline code spans and $...$ math is ignored,
so examples written as code are not mistaken for links. Files under reviews/
are archived evidence that often copies a note together with its original
relative links, so they are checked for control characters only.

Usage:
    python3 -I -B scripts/check_docs_integrity.py            # check the repo
    python3 -I -B scripts/check_docs_integrity.py --selftest # planted faults

Exit status is 0 only when nothing is found.
"""
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse

EXTERNAL = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
ARCHIVE_PREFIX = "reviews/"
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"(`+)(?:(?!\1).)+?\1")
INLINE_MATH = re.compile(r"(?<![\\$])\$(?!\$)[^$\n]+?\$")
DEFINITION = re.compile(r"^ {0,3}\[([^\]]+)\]:[ \t]*(<[^>]*>|\S+)")
REFERENCE = re.compile(r"\[([^\[\]]+)\]\[([^\[\]]*)\]")
HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.*?)[ \t#]*$")
HTML_ID = re.compile(r"""\b(?:id|name)\s*=\s*["']([^"']+)["']""")
SLUG_KEEP = re.compile(r"[\w\- ]")


def blank(match):
    return " " * len(match.group(0))


def visible_lines(text):
    """Lines with fenced code, inline code and inline math blanked out."""
    out = []
    fence = None
    for line in text.split("\n"):
        opened = FENCE.match(line)
        if fence is not None:
            if opened and opened.group(1)[0] == fence[0] and len(opened.group(1)) >= len(fence):
                fence = None
            out.append("")
            continue
        if opened:
            fence = opened.group(1)
            out.append("")
            continue
        line = INLINE_CODE.sub(blank, line)
        line = INLINE_MATH.sub(blank, line)
        out.append(line)
    return out


def inline_targets(line):
    """Destinations of inline links [text](dest "title") on one line."""
    found = []
    start = 0
    while True:
        at = line.find("](", start)
        if at < 0:
            return found
        i = at + 2
        n = len(line)
        while i < n and line[i] in " \t":
            i += 1
        if i < n and line[i] == "<":
            close = line.find(">", i)
            if close < 0:
                start = at + 2
                continue
            dest = line[i + 1:close]
            i = close + 1
        else:
            depth = 0
            j = i
            while j < n:
                c = line[j]
                if c in " \t":
                    break
                if c == "(":
                    depth += 1
                elif c == ")":
                    if depth == 0:
                        break
                    depth -= 1
                j += 1
            dest = line[i:j]
            i = j
        while i < n and line[i] in " \t":
            i += 1
        if i < n and line[i] in "\"'(":
            closer = ")" if line[i] == "(" else line[i]
            end = line.find(closer, i + 1)
            if end < 0:
                start = at + 2
                continue
            i = end + 1
            while i < n and line[i] in " \t":
                i += 1
        if i < n and line[i] == ")" and dest:
            found.append(dest)
        start = at + 2


def slugify(text):
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "").replace("*", "").lower()
    return "".join(c for c in text if SLUG_KEEP.match(c)).replace(" ", "-")


def anchors_of(path, cache):
    if path not in cache:
        names = set()
        counts = {}
        try:
            text = open(path, "rb").read().decode("utf-8", errors="replace")
        except OSError:
            cache[path] = names
            return names
        fence = None
        for line in text.split("\n"):
            opened = FENCE.match(line)
            if fence is not None:
                if opened and opened.group(1)[0] == fence[0] and len(opened.group(1)) >= len(fence):
                    fence = None
                continue
            if opened:
                fence = opened.group(1)
                continue
            for found in HTML_ID.finditer(line):
                names.add(found.group(1).lower())
            head = HEADING.match(line)
            if head:
                slug = slugify(head.group(2))
                seen = counts.get(slug, 0)
                counts[slug] = seen + 1
                names.add(slug if seen == 0 else slug + "-" + str(seen))
        cache[path] = names
    return cache[path]


def target_findings(root, rel, target, cache):
    """Return a reason string if a link target is broken, else None."""
    target = target.strip()
    if not target or EXTERNAL.match(target):
        return None
    path, _, anchor = target.partition("#")
    path = path.split("?", 1)[0]
    here = os.path.join(root, rel)
    if path:
        resolved = os.path.normpath(os.path.join(os.path.dirname(here), urllib.parse.unquote(path)))
        if not os.path.exists(resolved):
            return "missing_target"
    else:
        resolved = here
    if anchor and resolved.endswith(".md") and os.path.isfile(resolved):
        wanted = urllib.parse.unquote(anchor).lower()
        if wanted not in anchors_of(resolved, cache):
            return "missing_anchor"
    return None


def normalize_label(label):
    return " ".join(label.split()).lower()


def control_findings(data):
    found = []
    line = 1
    for byte in data:
        if byte == 10:
            line += 1
        elif byte < 32 or byte == 127:
            found.append((line, byte))
    return found


def link_findings(root, rel, text, cache):
    found = []
    lines = visible_lines(text)
    labels = set()
    for line in lines:
        definition = DEFINITION.match(line)
        if definition:
            labels.add(normalize_label(definition.group(1)))
    for lineno, line in enumerate(lines, 1):
        definition = DEFINITION.match(line)
        if definition:
            dest = definition.group(2).strip("<>")
            reason = target_findings(root, rel, dest, cache)
            if reason:
                found.append((lineno, reason, dest))
            continue
        for dest in inline_targets(line):
            reason = target_findings(root, rel, dest, cache)
            if reason:
                found.append((lineno, reason, dest))
        for ref in REFERENCE.finditer(line):
            if line[ref.end():ref.end() + 1] == "(":
                continue
            label = normalize_label(ref.group(2) or ref.group(1))
            if label not in labels:
                found.append((lineno, "undefined_reference", "[" + label + "]"))
    return found


def check(root, files):
    controls = 0
    links = 0
    cache = {}
    for rel in files:
        data = open(os.path.join(root, rel), "rb").read()
        for lineno, byte in control_findings(data):
            controls += 1
            print("DOCS_CONTROL_CHAR|file=" + rel + "|line=" + str(lineno)
                  + "|byte=" + hex(byte) + "|json=0")
        if rel.startswith(ARCHIVE_PREFIX):
            continue
        text = data.decode("utf-8", errors="replace")
        for lineno, reason, target in link_findings(root, rel, text, cache):
            links += 1
            print("DOCS_BROKEN_LINK|file=" + rel + "|line=" + str(lineno)
                  + "|reason=" + reason + "|target=" + target + "|json=0")
    print("DOCS_INTEGRITY|markdown_files=" + str(len(files))
          + "|control_chars=" + str(controls)
          + "|broken_links=" + str(links) + "|json=0")
    return controls + links


GOOD_TEXT = (
    "# Fine page\n\n## Second heading, with `code`\n\n"
    "See [peer](peer.md), [titled](peer.md \"A title\"), [angle](<peer.md>),\n"
    "[up](../TOP.md#top-heading), [here](#second-heading-with-code),\n"
    "[web](https://x.y/z) and [ref][known].\n\n"
    "Code is not a link: `[x](nowhere.md)`, nor is math: $[a][b]$.\n\n"
    "```\n[y](also-nowhere.md)\n```\n\n"
    "[known]: peer.md#peer-heading\n"
)
BAD_TEXT = (
    "(\x08eta=81) and (\rho^{|S|}) and (\text{x})\n"
    "[gone](docs/missing.md)\n"
    "[titled gone](docs/missing2.md \"title\")\n"
    "[bad anchor](docs/peer.md#no-such-heading)\n"
    "[dangling][nolabel]\n\n"
    "[def]: docs/missing3.md\n"
)
PLANTED = 8


def selftest():
    with tempfile.TemporaryDirectory() as root:
        os.makedirs(os.path.join(root, "docs"))
        open(os.path.join(root, "docs", "ok.md"), "wb").write(GOOD_TEXT.encode("utf-8"))
        open(os.path.join(root, "docs", "peer.md"), "wb").write(b"# Peer heading\n")
        open(os.path.join(root, "TOP.md"), "wb").write(b"# Top heading\n")
        open(os.path.join(root, "bad.md"), "wb").write(BAD_TEXT.encode("utf-8"))
        clean = check(root, ["docs/ok.md", "docs/peer.md", "TOP.md"])
        planted = check(root, ["bad.md"])
    if clean != 0:
        print("DOCS_SELFTEST|clean_tree=FALSE_POSITIVE|findings=" + str(clean) + "|json=0")
        return 1
    if planted != PLANTED:
        print("DOCS_SELFTEST|planted_faults=" + str(PLANTED) + "|caught=" + str(planted) + "|json=0")
        return 1
    print("DOCS_SELFTEST|clean_tree=PASS|planted_faults=" + str(PLANTED)
          + "|caught=" + str(planted) + "|json=0")
    return 0


def tracked_markdown(root):
    out = subprocess.run(["git", "-C", root, "ls-files", "-z", "--", "*.md"],
                         check=True, capture_output=True).stdout
    return [p.decode("utf-8") for p in out.split(b"\0") if p]


def main(argv):
    if "--selftest" in argv:
        return selftest()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True,
                          capture_output=True).stdout.decode("utf-8").strip()
    return 1 if check(root, tracked_markdown(root)) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
