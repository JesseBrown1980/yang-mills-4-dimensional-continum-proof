#!/usr/bin/env python3
"""
YM4-03C prediction commit: the evidence chain HBI -> HBP -> SHA -> SH -> HASH for this folder. Run from the repository root as
python3 -I -B -X utf8 reviews/fable5-ym4-03c-prediction/make_chain.py. It writes, in this folder:
INDEX.hbi    one EMIT row per artifact: its path, a PID chained from the seat (pid[n] = sha16(pid[n-1]|name), seed sha16(EMITTER-SEED|8467a937cba309f7)),
             its bytes, its sha256 and its 16-hex SH.
SHA256SUMS   sha256 of every file of this folder apart from SHA256SUMS and SEAL.hbp, RECORDS.hbp and INDEX.hbi among them.
SEAL.hbp     the sha256 of SHA256SUMS, of INDEX.hbi, and of the two concatenated in that order, with its SH.
RECORDS.hbp, the HBP records, is written beside it by hand before this runs. Integers only, json=0.
"""
import hashlib
import os
import sys

FOLDER = "reviews/fable5-ym4-03c-prediction"
SEAT_PID = "8467a937cba309f7"
ARTIFACTS = [
    "docs/PREDICTION-YM4-03C.hbp",
    "docs/NOTE-YM4-03C-BLOCKED-ACTION.md",
    ".github/workflows/blocked-action-b10.yml",
    FOLDER + "/derive_checks.py",
    FOLDER + "/DERIVE-CHECKS.hbp",
    FOLDER + "/FIRST-RUN.hbp",
    FOLDER + "/SECOND-RUN.hbp",
    FOLDER + "/RECORDS.hbp",
    FOLDER + "/make_chain.py",
]


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha16(text):
    return sha256_bytes(text.encode("utf-8"))[:16]


def read(path):
    with open(path, "rb") as handle:
        return handle.read()


def write(path, text):
    with open(path, "wb") as handle:
        handle.write(text.encode("utf-8"))


def main():
    for path in ARTIFACTS:
        data = read(path)
        if b"\r" in data:
            sys.stdout.write("CHAIN|failed=1|cr_in=" + path + "|json=0\n")
            return 1
    pid = sha16("EMITTER-SEED|" + SEAT_PID)
    rows = []
    for path in ARTIFACTS:
        data = read(path)
        digest = sha256_bytes(data)
        pid = sha16(pid + "|" + path)
        rows.append("EMIT|family=ym4-03c-prediction|name=" + path + "|pid=" + pid + "|bytes=" + str(len(data)) + "|sha256=" + digest + "|sh=" + digest[:16] + "|json=0\n")
    write(FOLDER + "/INDEX.hbi", "".join(rows))
    names = sorted(n for n in os.listdir(FOLDER) if n not in ("SHA256SUMS", "SEAL.hbp") and os.path.isfile(FOLDER + "/" + n))
    sums = "".join(sha256_bytes(read(FOLDER + "/" + n)) + "  " + n + "\n" for n in names)
    write(FOLDER + "/SHA256SUMS", sums)
    sums_bytes = read(FOLDER + "/SHA256SUMS")
    index_bytes = read(FOLDER + "/INDEX.hbi")
    seal = sha256_bytes(sums_bytes + index_bytes)
    write(FOLDER + "/SEAL.hbp", "SEAL|family=ym4-03c-prediction|sha256_SHA256SUMS=" + sha256_bytes(sums_bytes) + "|sha256_INDEX.hbi=" + sha256_bytes(index_bytes) + "|seal=" + seal + "|sh=" + seal[:16] + "|order=SHA256SUMS_then_INDEX.hbi|seat=ACER-CLAUDE-FABLE5|seat_pid=" + SEAT_PID + "|last_pid=" + pid + "|files_summed=" + str(len(names)) + "|artifacts_indexed=" + str(len(ARTIFACTS)) + "|json=0\n")
    sys.stdout.write("CHAIN|artifacts=" + str(len(ARTIFACTS)) + "|files_summed=" + str(len(names)) + "|seal=" + seal + "|sh=" + seal[:16] + "|json=0\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
