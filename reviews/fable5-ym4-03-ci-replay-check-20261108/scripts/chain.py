"""The HBI -> HBP -> SHA -> SH -> HASH chain over this lane's evidence folder.

usage = python3 -I -B -X utf8 chain.py FOLDER LABEL
INDEX.hbi gets one FILE row per file (path, bytes, sha256, its 16-hex SH, carriage returns), every file but INDEX.hbi, SHA256SUMS, SEAL.hbp and
VERIFY.hbp, which checks the rest. SHA256SUMS lists the same files and INDEX.hbi. SEAL.hbp holds the sha256 of the text
SEAL|label=LABEL|files=N|index_sha256=...|sha256sums_sha256=...|json=0 and its SH. A carriage return in any file exits 1. Integers only, json=0.
"""
import hashlib
import os
import sys

FOLDER, LABEL = sys.argv[1], sys.argv[2]
OUTSIDE = ("INDEX.hbi", "SHA256SUMS", "SEAL.hbp", "VERIFY.hbp")


def sha(data):
    return hashlib.sha256(data).hexdigest()


files = []
for top, dirs, names in os.walk(FOLDER):
    dirs.sort()
    for name in sorted(names):
        path = os.path.relpath(os.path.join(top, name), FOLDER).replace(os.sep, "/")
        if path in OUTSIDE or "__pycache__" in path or path.startswith(".git/"):
            continue
        files.append(path)
files.sort()
rows = ["HBI_HEAD|label=%s|files=%d|json=0" % (LABEL, len(files))]
sums = []
bad = 0
for path in files:
    with open(os.path.join(FOLDER, path), "rb") as handle:
        data = handle.read()
    digest = sha(data)
    cr = data.count(b"\r")
    bad += int(cr > 0)
    rows.append("FILE|path=%s|bytes=%d|sha256=%s|sh=%s|cr=%d|json=0" % (path, len(data), digest, digest[:16], cr))
    sums.append("%s  %s" % (digest, path))
index_text = ("\n".join(rows) + "\n").encode("utf-8")
with open(os.path.join(FOLDER, "INDEX.hbi"), "wb") as handle:
    handle.write(index_text)
sums.append("%s  %s" % (sha(index_text), "INDEX.hbi"))
sums_text = ("\n".join(sums) + "\n").encode("utf-8")
with open(os.path.join(FOLDER, "SHA256SUMS"), "wb") as handle:
    handle.write(sums_text)
seal_text = "SEAL|label=%s|files=%d|index_sha256=%s|sha256sums_sha256=%s|json=0" % (LABEL, len(files), sha(index_text), sha(sums_text))
seal = sha(seal_text.encode("utf-8"))
with open(os.path.join(FOLDER, "SEAL.hbp"), "wb") as handle:
    handle.write((seal_text + "\n" + "SEAL_HASH|seal=%s|seal_sh=%s|json=0\n" % (seal, seal[:16])).encode("utf-8"))
print("CHAIN|label=%s|files=%d|index_sha256=%s|sha256sums_sha256=%s|seal=%s|carriage_return_files=%d|json=0" % (LABEL, len(files), sha(index_text), sha(sums_text), seal, bad))
sys.exit(1 if bad else 0)
