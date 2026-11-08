"""Read every prediction of PREDICTION.hbp against the result rows: MET, MISS, or OBSERVED for a CONJECTURE row, each with the value read.

usage = python3 -I -B -X utf8 reads.py CHECK_FOLDER
Reads RESULTS.hbp, raw/plants/PLANTS.hbp, raw/instr/*.hbp, raw/main/A-REPLAY-INDEX.hbp, raw/negctl/NEG-CONTROLS.hbp, raw/lane-verify/*, raw/gates/*.
Writes READS.hbp. Integers only, json=0.
"""
import os
import sys

C = sys.argv[1]
NAMES = ["reversed_order", "shifted_endpoint", "dropped_inverse", "theta_no_inverse", "wrong_convolution_power", "wrong_first_coefficient",
         "extra_plaquette_factor", "wrong_block_shell", "twist_every_link", "flux_wrong_sign", "overlap_skips_next", "visibility_ignores_omega_error",
         "visibility_error_halved", "visibility_error_inflated", "overlap_one_power"]
NAMED = {
    "reversed_order": ["covariance_b=2"], "shifted_endpoint": ["covariance_b=2"], "dropped_inverse": ["covariance_b=2"],
    "theta_no_inverse": ["reflection_map_b=2_c=0"], "wrong_convolution_power": ["two_dimensions_closes_S3_b=2_2x2"],
    "wrong_first_coefficient": ["first_dependence_(2,2,2,2)_position=0"], "extra_plaquette_factor": ["brute_equals_elimination_S3"],
    "wrong_block_shell": ["walls_Z2_4x2x2"], "twist_every_link": ["winding_parity_b=2"], "flux_wrong_sign": ["flux_ground_in_e=0_Z2_2x1"],
    "overlap_skips_next": ["overlap_closed_form_Z2_2x1_(1, -1)", "overlap_bracket_Z2_2x1_(1, -1)"],
    "visibility_ignores_omega_error": ["flux_exact_zero_overlap_not_certified_Z2_2x1"], "visibility_error_halved": ["flux_exact_zero_residual_rejected_Z2_2x1"],
    "visibility_error_inflated": ["flux_two_insertions_above_the_residual_Z2_2x1"], "overlap_one_power": ["overlap_bracket_narrow_Z2_2x1_(1, -1)"],
}


def text(path):
    with open(os.path.join(C, path), encoding="utf-8") as handle:
        return handle.read()


def fields(line):
    return dict(part.split("=", 1) for part in line.split("|")[1:] if "=" in part)


def rows(path, tag):
    full = os.path.join(C, path)
    if not os.path.exists(full):
        return []
    return [fields(line) for line in text(path).split("\n") if line.startswith(tag + "|")]


OUT = []


def read(qid, ok, value, conjecture=False):
    result = "OBSERVED" if conjecture else ("MET" if ok else "MISS")
    OUT.append("READ|id=%s|result=%s|value=%s|json=0" % (qid, result, value.replace("|", "_")))


results = {}
for tag in ("MAIN_STEP", "MAIN_STEP_REPLAY_DONE", "INDEX_COMPARE", "SABOTAGE_READ", "SABOTAGE_READ_DONE", "SABOTAGE_STEP", "MAIN_STEP_TIME", "JOB_CPU", "HOSTED_PROJECTION", "PAIR"):
    results[tag] = rows("RESULTS.hbp", tag)
main_a = [r for r in results["MAIN_STEP"] if r["side"] == "A"][0]
done = text("RESULTS.hbp").split("MAIN_STEP_REPLAY_DONE|", 1)[1].split("\n", 1)[0]
read("Q01", main_a["equal_to_receipt"] == "1" and done.startswith("sections=16|brackets=44|seeded=44|bisected=0|crosschecked=26"), "equal_to_receipt=%s_%s" % (main_a["equal_to_receipt"], done.split("|json")[0]))
ic = results["INDEX_COMPARE"][0]
read("Q02", ic["rows_differing_without_ms"] == "0", "rows=%s_differing=%s" % (ic["mine_rows"], ic["rows_differing_without_ms"]))
sr = {r["name"]: r for r in results["SABOTAGE_READ"]}
passed = [n for n in NAMES if sr.get(n, {}).get("step_rc") == "0"]
read("Q03", len(passed) == 15, "workflow_read_passed=%d_of_15" % len(passed))
shape = []
ok = True
for n in NAMES:
    r = sr[n]
    comp = r["computed"].split(",")
    want = 3 if n == "reversed_order" else 1
    ok = ok and len(comp) == want and int(r["reused"]) == 16 - want and r["computed_outside_reach"] == "0" and r["computed_equals_reach"] == "1"
    shape.append("%s:%d/%s" % (n, len(comp), r["reused"]))
read("Q04", ok, ",".join(shape))
d = results["SABOTAGE_READ_DONE"][0]
read("Q05", d["replay_equals_full"] == "15", "replay_equals_full=%s_of_%s" % (d["replay_equals_full"], d["names"]))
# Q06 and Q08 from the instrumented replays.
inside, hit_names, named_ok = 0, 0, 0
detail = []
for n in NAMES:
    computed = set(sr[n]["computed"].split(","))
    lines = [r for r in rows("raw/instr/replay-%s.hbp" % n, "INSTR_LINE") if n in r["literal"].split(",")]
    sections_hit = sorted({r["section"] for r in lines})
    all_inside = all(s in computed for s in sections_hit)
    inside += int(all_inside and bool(lines))
    hit_names += int(bool(lines))
    added = rows("raw/instr/replay-%s.hbp" % n, "INSTR_SECTION")
    from_computed = set()
    for row in added:
        if row["names"] != "none" and row["section"] in computed:
            from_computed |= set(row["names"].split(";"))
    wanted = {x.replace("|", "_") for x in NAMED[n]}
    named_ok += int(wanted <= from_computed)
    detail.append("%s:%s" % (n, "+".join(sections_hit) or "none"))
read("Q06", inside == 15, "names_whose_literal_lines_ran_only_in_computed_sections=%d_of_15_ran_at_all=%d|%s" % (inside, hit_names, ",".join(detail)))
read("Q08", named_ok == 15, "named_checks_added_by_a_computed_section=%d_of_15" % named_ok)
# Q07 from the instrumented record.
reach = {}
for r in rows("raw/main/A-REPLAY-INDEX.hbp", "REPLAY_SECTION"):
    reach[r["section"]] = set() if r["reach"] == "none" else set(r["reach"].split(","))
rec = rows("raw/instr/record.hbp", "INSTR_LINE")
subset, equal = 0, 0
detail = []
for n in NAMES:
    evaluated = {r["section"] for r in rec if n in r["literal"].split(",")}
    by_index = {s for s, r in reach.items() if n in r}
    subset += int(evaluated <= by_index)
    equal += int(evaluated == by_index)
    detail.append("%s:%s" % (n, "+".join(sorted(evaluated)) or "none"))
read("Q07", subset == 15, "evaluated_within_index_reach=%d_of_15_equal=%d|%s" % (subset, equal, ",".join(detail)))
plants = {r["id"]: r for r in rows("raw/plants/PLANTS.hbp", "PLANT")}


def plant_read(qid, ids):
    got = [plants.get(i) for i in ids]
    ok = all(g is not None and g["refused_as_expected"] == "1" for g in got)
    read(qid, ok, ",".join("%s:%s" % (i, g["replay_failed"] if g else "missing") for i, g in zip(ids, got)))


plant_read("Q09", ["F01a", "F01b"])
plant_read("Q10", ["F02", "F02b"])
plant_read("Q11", ["F03"])
plant_read("Q12", ["F04"])
f05 = [plants.get("F05-" + n) for n in ("power", "inertia", "certify")]
read("Q13", all(g is not None and g["rc"] == "1" and g["replay_failed"].startswith("replay_key_stale_") for g in f05), ",".join("%s:%s" % (g["id"], g["replay_failed"]) for g in f05 if g))
plant_read("Q14", ["F06"])
plant_read("Q15", ["F07"])
f08 = [plants.get("F08-" + n) for n in NAMES]
refused = [g for g in f08 if g is not None and g["workflow_read_first_refusal"] == "exit_is_1"]
read("Q16", len(refused) == 15, "refused_at_the_exit_code_test=%d_of_15|first_refusals=%s" % (len(refused), ",".join(sorted({g["workflow_read_first_refusal"] for g in f08 if g}))))
f09 = [plants.get("F09-" + s) for s in ("section_covariance", "section_loops", "section_reflection")]
read("Q17", True, ",".join("%s:read_refusal=%s:stdout_vs_full=%s" % (g["id"], g["workflow_read_first_refusal"], g["stdout_against_full_run"]) for g in f09 if g), conjecture=True)
f10 = [plants.get(i) for i in ("F10", "F10-fixed")]
read("Q18", True, ",".join("%s:read_refusal=%s:computed=%s:stdout_vs_full=%s" % (g["id"], g["workflow_read_first_refusal"], g["computed"], g["stdout_against_full_run"]) for g in f10 if g), conjecture=True)
plant_read("Q19", ["F11a", "F11b"])
neg = rows("raw/negctl/NEG-CONTROLS.hbp", "NEG_CONTROLS_DONE")[0]
missing_paths = [r for r in rows("raw/negctl/NEG-CONTROLS.hbp", "TRIGGER") if r["missing"] != "none"]
read("Q20", neg["calls_kept"] == neg["main_calls"] == "16" and not missing_paths, "calls_kept=%s_of_%s_lines_same=%s_moved=%s_rewritten=%s" % (neg["calls_kept"], neg["main_calls"], neg["same"], neg["moved"], neg["rewritten"]))
st = results["SABOTAGE_STEP"][0]
cpu, wall = int(st["cpu_x1000"]), int(st["wall_x1000"])
read("Q21", 8700 <= cpu <= 14000, "cpu_x1000=%d" % cpu)
read("Q22", 7000 <= wall <= 15000, "wall_x1000=%d" % wall)
mt = results["MAIN_STEP_TIME"][0]
read("Q23", 600 <= int(mt["cpu_x1000"]) <= 1050, "record_over_plain_cpu_x1000=%s" % mt["cpu_x1000"])
gates = rows("raw/gates/e4a83d4-GATES.hbp", "GATE")
gdone = rows("raw/gates/e4a83d4-GATES.hbp", "GATES_DONE")
read("Q24", bool(gates) and bool(gdone) and gdone[0]["failed"] == "0", "steps=%d_failed=%s" % (len(gates), gdone[0]["failed"] if gdone else "missing"))
lane = {r_tag: rows("raw/lane-verify/LANE-CHECKS.hbp", r_tag) for r_tag in ("LANE_SUMS", "LANE_PREDICTION", "LANE_CR")}
verify_ok = "result=PASS" in text("raw/lane-verify/VERIFY-rerun.out")
lp = lane["LANE_PREDICTION"][0]
read("Q25", lane["LANE_SUMS"][0]["rc"] == "0" and verify_ok and lp["prediction_is_ancestor_of_change"] == "1" and lp["commits_touching"].count(",") == 1,
     "sums_rc=%s_verify_pass=%d_prediction_before_change=%s_commits_touching=%d" % (lane["LANE_SUMS"][0]["rc"], int(verify_ok), lp["prediction_is_ancestor_of_change"], lp["commits_touching"].count(",")))
lc = lane["LANE_CR"][0]
read("Q26", lc["carriage_returns"] == "0", "changed_files=%s_carriage_returns=%s" % (lc["changed_files"], lc["carriage_returns"]))
prop = rows("RESULTS.hbp", "PROPOSED_RUN")
if prop:
    p = prop[0]
    ok = all(part.endswith(":0") for part in p["steps"].split(",")) and p["main_equals_receipt"] == "1" and p["index_equals_branch"] == "1" and p["sabotage_stdout_equal_to_branch"] == "15_of_15" and p["control_refused"] == "1"
    read("X01", ok, "proposal_steps=%s_main=%s_index=%s_stdout=%s_control=%s" % (p["steps"], p["main_equals_receipt"], p["index_equals_branch"], p["sabotage_stdout_equal_to_branch"], p["control_refused"]), conjecture=True)
fixed = plants.get("F10-fixed")
if fixed:
    read("X02", True, "proposed_driver_on_the_planted_read:computed=%s:stdout_vs_full=%s" % (fixed["computed"], fixed["stdout_against_full_run"]), conjecture=True)
xs = rows("raw/steps/XCHECK.hbp", "XCHECK")
if xs:
    read("X03", True, "wfread_step_folders_equal_to_the_pyyaml_ones=%d_of_%d" % (sum(1 for x in xs if x["diff_rc"] == "0"), len(xs)), conjecture=True)
xi = rows("raw/instr/XCHECK-INSTRUMENT.hbp", "XCHECK_INSTRUMENT_DONE")
if xi:
    read("X04", True, "instrument_import_version_equal_to_runpy_version=%s_of_%s" % (xi[0]["same"], xi[0]["files"]), conjecture=True)
memo = rows("raw/lane-verify/MEMO.hbp", "MEMO")
if memo:
    read("X05", True, "SINGLE_POWER_lines=%s_writer_called_at=%s_sections=%s" % (memo[0]["lines"], memo[0]["single_power_lines"], memo[0]["sections_covering_single_power"]), conjecture=True)
with open(os.path.join(C, "READS.hbp"), "w", encoding="utf-8", newline="\n") as handle:
    handle.write("\n".join(OUT) + "\n")
print("\n".join(OUT))
