#!/usr/bin/env python3
"""
YM4-03C, stage 2: the prediction commit's evidence chain, read against the prediction commit itself.

The engine commit adds a results section to docs/NOTE-YM4-03C-BLOCKED-ACTION.md, below its frozen sections, and steps to
.github/workflows/blocked-action-b10.yml, so those two files differ from the bytes that reviews/fable5-ym4-03c-prediction/INDEX.hbi
names. This file reads every INDEX.hbi row against the blob of that path at the prediction commit, recomputes the PID chain from the seat,
the folder's SHA256SUMS and the seal, and reads each artifact's current bytes: unchanged, or for the note a byte extension of the
prediction commit's note, so the frozen sections stay byte for byte. It needs the history (actions/checkout with fetch-depth: 0).

Run from the repository root as python3 -I -B -X utf8 reviews/fable5-ym4-03c-engine/check_prediction_chain.py. Integers only, json=0.
"""
import hashlib
import os
import subprocess
import sys

PREDICTION_COMMIT = "32486bd48f9137e0ebd5009e8f8ec4d347c18522"
FOLDER = "reviews/fable5-ym4-03c-prediction"
SEAT_PID = "8467a937cba309f7"
EXTENDED = {"docs/NOTE-YM4-03C-BLOCKED-ACTION.md": "extension", ".github/workflows/blocked-action-b10.yml": "edited"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(path):
    out = subprocess.run(["git", "cat-file", "blob", PREDICTION_COMMIT + ":" + path], capture_output=True, check=True, stdin=subprocess.DEVNULL)
    return out.stdout


def read(path):
    with open(path, "rb") as handle:
        return handle.read()


def say(text):
    sys.stdout.write(text + "\n")


def main():
    bad = 0
    pid = sha(("EMITTER-SEED|" + SEAT_PID).encode("utf-8"))[:16]
    rows = read(FOLDER + "/INDEX.hbi").decode("utf-8").splitlines()
    for row in rows:
        fields = dict(f.split("=", 1) for f in row.split("|")[1:] if "=" in f)
        path = fields["name"]
        old = blob(path)
        pid = sha((pid + "|" + path).encode("utf-8"))[:16]
        ok = fields["pid"] == pid and fields["bytes"] == str(len(old)) and fields["sha256"] == sha(old) and fields["sh"] == sha(old)[:16]
        now = read(path)
        kind = EXTENDED.get(path, "unchanged")
        if kind == "unchanged":
            now_ok = now == old
        elif kind == "extension":
            now_ok = now[: len(old)] == old
        else:
            now_ok = True
        if not (ok and now_ok):
            bad += 1
        say("PREDICTION_CHAIN_ROW|name=" + path + "|row_matches_the_prediction_commit=" + str(int(ok)) + "|now=" + kind + "|now_ok=" + str(int(now_ok)) + "|json=0")
    names = sorted(n for n in os.listdir(FOLDER) if n not in ("SHA256SUMS", "SEAL.hbp") and os.path.isfile(FOLDER + "/" + n))
    sums = "".join(sha(read(FOLDER + "/" + n)) + "  " + n + "\n" for n in names).encode("utf-8")
    sums_ok = sums == read(FOLDER + "/SHA256SUMS") == blob(FOLDER + "/SHA256SUMS")
    index_bytes = read(FOLDER + "/INDEX.hbi")
    seal = sha(read(FOLDER + "/SHA256SUMS") + index_bytes)
    seal_row = read(FOLDER + "/SEAL.hbp").decode("utf-8")
    seal_ok = ("|seal=" + seal + "|") in seal_row and ("|sh=" + seal[:16] + "|") in seal_row and ("|last_pid=" + pid + "|") in seal_row
    if not sums_ok:
        bad += 1
    if not seal_ok:
        bad += 1
    say("PREDICTION_CHAIN|commit=" + PREDICTION_COMMIT + "|index_rows=" + str(len(rows)) + "|sha256sums_ok=" + str(int(sums_ok)) + "|seal=" + seal + "|seal_ok=" + str(int(seal_ok)) + "|bad=" + str(bad) + "|json=0")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
