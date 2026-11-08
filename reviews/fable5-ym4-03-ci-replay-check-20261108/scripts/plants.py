"""Faults a correct section cache must catch, planted in copies inside this lane's folder, and the check that catches each.

usage = python3 -I -B -X utf8 plants.py BASE OUT stage1|stage2
BASE is this lane's folder; BASE/repo is the branch at e4a83d4 (read only here), BASE/work/runA/ym4-03-cache the index its main step wrote.
stage1 builds the planted trees and the tampered caches that need no new record; stage2 runs every plant. Each run is read twice: as the
workflow's read_sabotage reads it (exit 1, every named line, no Traceback, no FAILED|check=replay_ line, one section or more computed as reached),
giving the first check that refuses it, and as the cache control's refused() reads it (exit 1 and the expected replay line). OUT gets one PLANT row
per run. Integers only, json=0.
"""
import hashlib
import os
import shutil
import subprocess
import sys

BASE, OUT, STAGE = sys.argv[1], sys.argv[2], sys.argv[3]
REPO = os.path.join(BASE, "repo")
CACHE = os.path.join(BASE, "work", "runA", "ym4-03-cache")
PW = os.path.join(BASE, "work", "plants")
INDEX = "REPLAY-INDEX.hbp"
STDERR_HEADS = ("SECTION|", "REPLAY|", "REPLAY_START|", "REPLAY_DONE|", "REPLAY_REFUSED|", "REPLAY_NOT_READY|", "REPLAY_INDEX|")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    with open(path, "rb") as handle:
        return handle.read()


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)


def tree(name):
    """A copy of tests/ under PW/name, the layout the driver needs: the module and the receipt beside it."""
    root = os.path.join(PW, name)
    if os.path.isdir(root):
        shutil.rmtree(root)
    shutil.copytree(os.path.join(REPO, "tests"), os.path.join(root, "tests"))
    return root


def cache_copy(name, source=CACHE):
    target = os.path.join(PW, "cache-" + name)
    if os.path.isdir(target):
        shutil.rmtree(target)
    shutil.copytree(source, target)
    return target


def reseal(cache):
    data = read(os.path.join(cache, INDEX))
    write(os.path.join(cache, INDEX + ".sha256"), ("%s  %s\n" % (sha(data), INDEX)).encode("utf-8"))


def edit_index(cache, edit):
    path = os.path.join(cache, INDEX)
    lines = read(path).decode("utf-8").split("\n")
    lines = [edit(line) for line in lines]
    write(path, "\n".join(lines).encode("utf-8"))
    reseal(cache)


def field_set(line, key, value):
    parts = line.split("|")
    for k, part in enumerate(parts):
        if part.startswith(key + "="):
            parts[k] = key + "=" + value
    return "|".join(parts)


def field(line, key):
    for part in line.split("|"):
        if part.startswith(key + "="):
            return part[len(key) + 1:]
    return None


def section_key(section, units, module_code, inputs, python):
    text = "YM4_03_REPLAY_KEY|format=1|section=%s|units=%s|module_code=%s|inputs=%s|sabotage=|python=%s|json=0" % (section, units, module_code, inputs, python)
    return sha(text.encode("utf-8"))


def header(cache):
    for line in read(os.path.join(cache, INDEX)).decode("utf-8").split("\n"):
        if line.startswith("REPLAY_INDEX|"):
            return line
    return ""


def replace_once(path, old, new):
    text = read(path).decode("utf-8")
    if text.count(old) != 1:
        raise SystemExit("PLANT_EDIT_NOT_UNIQUE|path=%s|count=%d" % (path, text.count(old)))
    write(path, text.replace(old, new).encode("utf-8"))


PLANTED_HAAR = '    if "sabotage=twist_every_link" in sys.argv:\n        say("YM4_03_PLANTED|section=haar|read=sys_argv_text|json=0")\n'


def stage1():
    os.makedirs(PW, exist_ok=True)
    # P_argv: a planted module, a different code version: section_haar reads the sabotage from sys.argv text, with no SABOTAGE token.
    root = tree("argv")
    path = os.path.join(root, "tests", "test_one_scale_blocking.py")
    text = read(path).decode("utf-8")
    head = "def section_haar():\n"
    at = text.index(head) + len(head)
    body_start = text.index("\n", text.index('"""', at) + 3) + 1 if text[at:].lstrip().startswith('"""') else at
    write(path, (text[:body_start] + PLANTED_HAAR + text[body_start:]).encode("utf-8"))
    # P_argv_fixed: the same module with the proposed driver.
    fixed = tree("argv-fixed")
    shutil.copy(path, os.path.join(fixed, "tests", "test_one_scale_blocking.py"))
    proposed = os.path.join(BASE, "check", "proposed", "one_scale_replay.py")
    if os.path.exists(proposed):
        shutil.copy(proposed, os.path.join(fixed, "tests", "one_scale_replay.py"))
    # Helper edits with the index left as recorded.
    for name, old, new in (
            ("power", "    out = 1\n    for _ in range(exponent):\n        out *= base\n    return out\n",
             "    out = 1\n    for _ in range(exponent):\n        out *= base\n    return out + 0 * exponent\n"),
            ("inertia", "def inertia_positive(rows):\n", "def inertia_positive(rows):\n    rows = [list(row) for row in rows]\n"),
            ("certify", "def certify_overlap(model, w, top_low, top_high, next_high, shift, label, leak=None, quiet=False):\n",
             "def certify_overlap(model, w, top_low, top_high, next_high, shift, label, leak=None, quiet=False):\n    shift = shift + 0\n")):
        root = tree("edit-" + name)
        replace_once(os.path.join(root, "tests", "test_one_scale_blocking.py"), old, new)
    # Driver copies that wrongly mark one reached section of reversed_order as unaffected.
    for section in ("section_covariance", "section_loops", "section_reflection"):
        root = tree("unmark-" + section)
        replace_once(os.path.join(root, "tests", "one_scale_replay.py"),
                     'CACHE_SABOTAGE != "reuse_reached":\n', 'CACHE_SABOTAGE != "reuse_reached" and section != "%s":\n' % section)
    print("STAGE1_DONE|json=0")


def run(cwd, driver, args):
    proc = subprocess.run(["python3", "-I", "-B", "-X", "utf8", driver] + args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout


def stdout_only(data):
    return b"".join(line for line in data.splitlines(keepends=True) if not line.decode("utf-8", "replace").startswith(STDERR_HEADS))


def workflow_read(rc, data, sabotage, named):
    text = data.decode("utf-8", "replace")
    checks = [("exit_is_1", rc == 1)]
    for item in named:
        checks.append(("named_" + item.replace("|", "_").replace(" ", "_"), ("FAILED|check=%s|json=0" % item) in text))
    checks.append(("no_traceback", "Traceback" not in text))
    checks.append(("no_replay_failed", not any(line.startswith("FAILED|check=replay_") for line in text.split("\n"))))
    reached = sum(1 for line in text.split("\n") if ("|mode=computed|why=reached_by_%s|" % sabotage) in line)
    checks.append(("reached_at_least_1", reached >= 1))
    first = next((name for name, ok in checks if not ok), "none")
    return first, reached


def refused_read(rc, data, expected):
    text = data.decode("utf-8", "replace")
    return rc == 1 and ("FAILED|check=%s|json=0" % expected) in text and "Traceback" not in text


ROWS = []
OUTS = {}


def plant(pid, quantity, cwd, cache, args, sabotage, named, expected, reference=None, save=None):
    driver = os.path.join(cwd, "tests", "one_scale_replay.py")
    rc, data = run(cwd, driver, ["replay", cache] + args)
    first, reached = workflow_read(rc, data, sabotage, named) if sabotage else ("not_a_sabotage_read", 0)
    text = data.decode("utf-8", "replace")
    replay_lines = sorted({line.split("|")[1][len("check="):] for line in text.split("\n") if line.startswith("FAILED|check=replay_")})
    computed = sum(1 for line in text.split("\n") if "|mode=computed|" in line)
    reused = sum(1 for line in text.split("\n") if "|mode=reused|" in line)
    ref = "none"
    if reference is not None:
        ref = "identical" if stdout_only(data) == reference else "differs"
    if save:
        write(os.path.join(PW, "out", save), data)
    row = "PLANT|id=%s|quantity=%s|rc=%d|replay_failed=%s|computed=%d|reused=%d|workflow_read_first_refusal=%s|reached=%d|expected=%s|refused_as_expected=%d|stdout_against_full_run=%s|out_sha256=%s|json=0" % (
        pid, quantity, rc, ",".join(replay_lines) or "none", computed, reused, first, reached, expected or "none", int(refused_read(rc, data, expected)) if expected else -1, ref, sha(data))
    ROWS.append(row)
    print(row, flush=True)
    return rc, data


def full_stdout(name):
    path = os.path.join(BASE, "work", "runB", "sab-%s.out" % name)
    return stdout_only(read(path)) if os.path.exists(path) else None


NAMED = {
    "reversed_order": ["covariance_b=2"], "shifted_endpoint": ["covariance_b=2"], "dropped_inverse": ["covariance_b=2"],
    "theta_no_inverse": ["reflection_map_b=2_c=0"], "wrong_convolution_power": ["two_dimensions_closes_S3_b=2_2x2"],
    "wrong_first_coefficient": ["first_dependence_(2,2,2,2)_position=0"], "extra_plaquette_factor": ["brute_equals_elimination_S3"],
    "wrong_block_shell": ["walls_Z2_4x2x2"], "twist_every_link": ["winding_parity_b=2"], "flux_wrong_sign": ["flux_ground_in_e=0_Z2_2x1"],
    "overlap_skips_next": ["overlap_closed_form_Z2_2x1_(1, -1)", "overlap_bracket_Z2_2x1_(1, -1)"],
    "visibility_ignores_omega_error": ["flux_exact_zero_overlap_not_certified_Z2_2x1"], "visibility_error_halved": ["flux_exact_zero_residual_rejected_Z2_2x1"],
    "visibility_error_inflated": ["flux_two_insertions_above_the_residual_Z2_2x1"], "overlap_one_power": ["overlap_bracket_narrow_Z2_2x1_(1, -1)"],
}


def stage2():
    head = header(CACHE)
    python, module_code = field(head, "python"), field(head, "module_code")
    argv_cache = os.path.join(PW, "cache-argv-record")
    # F01: the whole index recorded on the planted module (another code version), replayed by the current module.
    plant("F01a", "index_from_another_code_version_no_sabotage", REPO, argv_cache, [], "", [], "replay_key_stale_section_haar")
    plant("F01b", "index_from_another_code_version_under_wrong_block_shell", REPO, argv_cache, ["sabotage=wrong_block_shell"], "wrong_block_shell", NAMED["wrong_block_shell"], "replay_key_stale_section_haar")
    # F02/F03: header from another Python or another module-level code.
    c = cache_copy("python")
    edit_index(c, lambda line: field_set(line, "python", "cpython-3.12.4") if line.startswith("REPLAY_INDEX|") else line)
    plant("F02", "header_python_changed", REPO, c, [], "", [], "replay_key_stale_section_covariance")
    c = cache_copy("python-unsealed")
    path = os.path.join(c, INDEX)
    write(path, read(path).replace(("python=" + python).encode("utf-8"), b"python=cpython-3.12.4"))
    plant("F02b", "header_python_changed_sidecar_left", REPO, c, [], "", [], "replay_index_sha256")
    c = cache_copy("module-code")
    edit_index(c, lambda line: field_set(line, "module_code", "0" * 64) if line.startswith("REPLAY_INDEX|") else line)
    plant("F03", "header_module_code_changed", REPO, c, [], "", [], "replay_key_stale_section_covariance")
    # F04: one row spliced from the planted record into the current index.
    planted_rows = {field(line, "section"): line for line in read(os.path.join(argv_cache, INDEX)).decode("utf-8").split("\n") if line.startswith("REPLAY_SECTION|")}
    c = cache_copy("splice")
    edit_index(c, lambda line: planted_rows["section_haar"] if line.startswith("REPLAY_SECTION|") and field(line, "section") == "section_haar" else line)
    plant("F04", "one_row_spliced_from_another_code_version", REPO, c, ["sabotage=wrong_block_shell"], "wrong_block_shell", NAMED["wrong_block_shell"], "replay_key_stale_section_haar")
    # F05: a helper edited, the index as recorded.
    for name, sabotage in (("power", "overlap_one_power"), ("inertia", "overlap_one_power"), ("certify", "wrong_block_shell")):
        root = os.path.join(PW, "edit-" + name)
        rc, data = plant("F05-" + name, "helper_%s_edited_index_as_recorded" % name, root, CACHE, ["sabotage=" + sabotage], sabotage, NAMED[sabotage], "")
        OUTS[name] = data
    # F06: the helper edited, its digest rewritten in the units lists, the keys left. The edited unit's digest is the one the driver itself
    # prints when it refuses the stale entry in F05-certify.
    root = os.path.join(PW, "edit-certify")
    new_digest = refused_digest(OUTS["certify"], "certify_overlap")
    c = cache_copy("digest-rewritten")
    edit_index(c, lambda line: rewrite_unit(line, "certify_overlap", new_digest) if line.startswith("REPLAY_SECTION|") else line)
    plant("F06", "helper_edited_digest_rewritten_key_left", root, c, ["sabotage=wrong_block_shell"], "wrong_block_shell", NAMED["wrong_block_shell"], "replay_key_corrupt_section_flux")
    # F07: a flux unit holding sabotage literals dropped from the units, the key rewritten to match.
    c = cache_copy("drop-literal-unit")

    def drop(line):
        if not (line.startswith("REPLAY_SECTION|") and field(line, "section") == "section_flux"):
            return line
        kept = ",".join(part for part in field(line, "units").split(",") if part.partition(":")[0] != "certify_overlap")
        line = field_set(line, "units", kept)
        return field_set(line, "key", section_key("section_flux", kept, module_code, field(line, "inputs"), python))
    edit_index(c, drop)
    plant("F07", "flux_unit_with_literals_dropped_key_rewritten", REPO, c, ["sabotage=overlap_one_power"], "overlap_one_power", NAMED["overlap_one_power"], "replay_coverage_misses_helper_section_flux")
    # F08: every reached section reused, under each of the 15 names.
    for name in NAMED:
        plant("F08-" + name, "reuse_reached", REPO, CACHE, ["sabotage=" + name, "cache_sabotage=reuse_reached"], name, NAMED[name], "")
    # F09: one reached section of reversed_order wrongly marked unaffected.
    for section in ("section_covariance", "section_loops", "section_reflection"):
        root = os.path.join(PW, "unmark-" + section)
        plant("F09-" + section, "reversed_order_with_%s_marked_unaffected" % section, root, CACHE, ["sabotage=reversed_order"], "reversed_order", NAMED["reversed_order"], "",
              reference=full_stdout("reversed_order"), save="F09-%s.out" % section)
    plant("F09-control", "reversed_order_unpatched", REPO, CACHE, ["sabotage=reversed_order"], "reversed_order", NAMED["reversed_order"], "", reference=full_stdout("reversed_order"))
    # F10: the planted sys.argv read, on its own fresh record.
    argv_full = os.path.join(PW, "argv-full-twist.out")
    reference = stdout_only(read(argv_full)) if os.path.exists(argv_full) else None
    plant("F10", "sys_argv_read_on_its_own_record_current_driver", os.path.join(PW, "argv"), argv_cache, ["sabotage=twist_every_link"], "twist_every_link", NAMED["twist_every_link"], "", reference=reference, save="F10.out")
    plant("F10-fixed", "sys_argv_read_on_its_own_record_proposed_driver", os.path.join(PW, "argv-fixed"), argv_cache, ["sabotage=twist_every_link"], "twist_every_link", NAMED["twist_every_link"], "", reference=reference, save="F10-fixed.out")
    # F11: brackets: every one moved up by one (the workflow's control), and two rows' values swapped.
    plant("F11a", "stale_bracket", REPO, CACHE, ["sabotage=overlap_one_power", "cache_sabotage=stale_bracket"], "", [], "replay_bracket_stale")
    c = cache_copy("bracket-swap")
    rows = read(os.path.join(c, INDEX)).decode("utf-8").split("\n")
    brackets = [k for k, line in enumerate(rows) if line.startswith("LEVEL_BRACKET|")]
    pair = None
    for i in brackets:
        for j in brackets:
            if i < j and pair is None and (field(rows[i], "low"), field(rows[i], "high")) != (field(rows[j], "low"), field(rows[j], "high")) and field(rows[i], "low") != "0" and field(rows[j], "low") != "0":
                pair = (i, j)
    i, j = pair
    li, hi, lj, hj = field(rows[i], "low"), field(rows[i], "high"), field(rows[j], "low"), field(rows[j], "high")
    rows[i] = field_set(field_set(rows[i], "low", lj), "high", hj)
    rows[j] = field_set(field_set(rows[j], "low", li), "high", hi)
    write(os.path.join(c, INDEX), "\n".join(rows).encode("utf-8"))
    reseal(c)
    plant("F11b", "two_bracket_rows_values_swapped_orders_%s_%s" % (field(rows[i], "order"), field(rows[j], "order")), REPO, c, ["sabotage=overlap_one_power"], "", [], "replay_bracket_stale")
    with open(OUT, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(ROWS) + "\n")


def refused_digest(data, name):
    """The now= digest of unit name from the driver's REPLAY_REFUSED line."""
    for line in data.decode("utf-8", "replace").split("\n"):
        if line.startswith("REPLAY_REFUSED|") and ("|reason=unit=%s|" % name) in line:
            return field(line, "now")
    raise SystemExit("PLANT_NO_REFUSAL_FOR|name=%s" % name)


def rewrite_unit(line, name, digest):
    units = field(line, "units")
    if units is None:
        return line
    parts = []
    for part in units.split(","):
        unit, _, old = part.partition(":")
        parts.append("%s:%s" % (unit, digest) if unit == name else part)
    return field_set(line, "units", ",".join(parts))


if STAGE == "stage1":
    stage1()
elif STAGE == "stage2":
    stage2()
else:
    sys.exit(2)
