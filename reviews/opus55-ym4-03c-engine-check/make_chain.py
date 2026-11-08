#!/usr/bin/env python3
"""
YM4-03C engine check: the evidence chain HBI -> HBP -> SHA -> SH -> HASH for this folder. Run from the repository root as
python3 -I -B -X utf8 reviews/opus55-ym4-03c-engine-check/make_chain.py. It writes, in this folder:
INDEX.hbi    one EMIT row per artifact: its path, a PID chained from the seat (pid[n] = sha16(pid[n-1]|name), seed
             sha16(EMITTER-SEED|8467a937cba309f7)), its bytes, its sha256 and its 16-hex SH.
SHA256SUMS   sha256 of every file of this folder apart from SHA256SUMS and SEAL.hbp.
SEAL.hbp     the sha256 of SHA256SUMS, of INDEX.hbi, and of the two concatenated in that order, with its SH.
RECORDS.hbp, the HBP records, is written by hand before this runs. A CR in any artifact stops it. Integers only, json=0.
"""
import hashlib
import os
import sys

FOLDER = "reviews/opus55-ym4-03c-engine-check"
FAMILY = "ym4-03c-engine-check"
SEAT_PID = "8467a937cba309f7"
ARTIFACTS = [
    "docs/PREDICTION-YM4-03C.hbp",
    "docs/NOTE-YM4-03C-BLOCKED-ACTION.md",
    "reviews/fable5-ym4-03c-engine/blocked_action_engine.rs",
    "reviews/fable5-ym4-03c-engine/RECEIPT-YM4-03C.hbp",
    ".github/workflows/ym4-03c-engine-check.yml",
    FOLDER + "/route_c_cumulants.py",
    FOLDER + "/ROUTE-C-D4.hbp",
    FOLDER + "/ROUTE-C-D3.hbp",
    FOLDER + "/ROUTE-C-D3-GAUGE-1V.hbp",
    FOLDER + "/route_c_plants.sh",
    FOLDER + "/ROUTE-C-PLANTS.hbp",
    FOLDER + "/frozen_literals.py",
    FOLDER + "/FROZEN-LITERALS.hbp",
    FOLDER + "/edit_text.py",
    FOLDER + "/engine_plants.sh",
    FOLDER + "/ENGINE-PLANTS.hbp",
    FOLDER + "/RECORDS.hbp",
    FOLDER + "/make_chain.py",
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha16(text):
    return digest(text.encode("utf-8"))[:16]


def read(path):
    with open(path, "rb") as handle:
        return handle.read()


def write(path, text):
    with open(path, "wb") as handle:
        handle.write(text.encode("utf-8"))


def main():
    for path in ARTIFACTS:
        if b"\r" in read(path):
            sys.stdout.write("CHAIN|failed=1|cr_in=" + path + "|json=0\n")
            return 1
    pid = sha16("EMITTER-SEED|" + SEAT_PID)
    rows = []
    for path in ARTIFACTS:
        data = read(path)
        h = digest(data)
        pid = sha16(pid + "|" + path)
        rows.append("EMIT|family=" + FAMILY + "|name=" + path + "|pid=" + pid + "|bytes=" + str(len(data)) + "|sha256=" + h + "|sh=" + h[:16] + "|json=0\n")
    write(FOLDER + "/INDEX.hbi", "".join(rows))
    names = sorted(n for n in os.listdir(FOLDER) if n not in ("SHA256SUMS", "SEAL.hbp") and os.path.isfile(FOLDER + "/" + n))
    write(FOLDER + "/SHA256SUMS", "".join(digest(read(FOLDER + "/" + n)) + "  " + n + "\n" for n in names))
    sums = read(FOLDER + "/SHA256SUMS")
    index = read(FOLDER + "/INDEX.hbi")
    seal = digest(sums + index)
    write(FOLDER + "/SEAL.hbp", "SEAL|family=" + FAMILY + "|sha256_SHA256SUMS=" + digest(sums) + "|sha256_INDEX.hbi=" + digest(index) + "|seal=" + seal + "|sh=" + seal[:16] + "|order=SHA256SUMS_then_INDEX.hbi|seat=ACER-CLAUDE-FABLE5|seat_pid=" + SEAT_PID + "|last_pid=" + pid + "|files_summed=" + str(len(names)) + "|artifacts_indexed=" + str(len(ARTIFACTS)) + "|json=0\n")
    sys.stdout.write("CHAIN|family=" + FAMILY + "|artifacts=" + str(len(ARTIFACTS)) + "|files_summed=" + str(len(names)) + "|seal=" + seal + "|sh=" + seal[:16] + "|json=0\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
