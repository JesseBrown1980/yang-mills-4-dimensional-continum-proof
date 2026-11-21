#!/usr/bin/env python3
"""Independent, integer-only source and scope check of the 4D certificate atlas.

The atlas is a sourced index, not a substitute for theorem/checker receipts.
The external Anaxia one-cube rational controls are recomputed from exact
integers, with no finite-to-continuum promotion.
"""
from pathlib import Path


def require(flag, name):
    if not flag:
        raise ValueError(name)


def rat(n, d=1):
    require(d > 0, "invalid_rational_denominator")
    return n, d


def radd(a, b):
    return rat(a[0] * b[1] + b[0] * a[1], a[1] * b[1])


def rneg(a):
    return rat(-a[0], a[1])


def rsub(a, b):
    return radd(a, rneg(b))


def rmul(a, b):
    return rat(a[0] * b[0], a[1] * b[1])


def rdiv(a, b):
    require(b[0] != 0, "zero_rational_divisor")
    require(b[0] > 0, "negative_rational_divisor")
    return rat(a[0] * b[1], a[1] * b[0])


def rlt(a, b):
    return a[0] * b[1] < b[0] * a[1]


def req(a, b):
    return a[0] * b[1] == b[0] * a[1]


def rpower(a, n):
    require(n >= 0, "negative_rational_power")
    out = rat(1)
    for _ in range(n):
        out = rmul(out, a)
    return out


def intfactorial(n):
    require(n >= 0, "negative_factorial")
    out = 1
    for k in range(1, n + 1):
        out *= k
    return out


def exp_envelope(y, degree):
    require(degree >= 0, "negative_series_degree")
    require(rlt(rat(0), y), "nonpositive_series_argument")
    require(rlt(y, rat(degree + 2)), "invalid_remainder_radius")
    series = rat(0)
    for k in range(degree + 1):
        series = radd(series, rdiv(rpower(y, k), rat(intfactorial(k))))
    nextterm = rdiv(rpower(y, degree + 1),
                    rat(intfactorial(degree + 1)))
    ratio = rdiv(y, rat(degree + 2))
    upper = radd(series, rdiv(nextterm, rsub(rat(1), ratio)))
    return series, upper


def external_one_cube_exact_rational():
    # Independent exact-rational reproduction of a PUBLIC finite-constants-only
    # script, source-pinned at anaxia-research/4Y-M main 2026-11-19.
    # This cannot establish a 4D Wilson physical first spectral weight.
    x = rat(1, 8192)
    purity = rsub(rsub(rmul(rat(2), x),
                       rmul(rat(3), rmul(x, x))), rat(1, 4097))
    require(req(purity, rat(4093, 274945015808)), "external_purity")
    require(64 * 252 < 127 * 127, "external_discriminant")
    require(not rlt(rat(127, 126), rat(252, 251)),
            "external_fraction_order")
    _, upper = exp_envelope(rat(64, 4160), 4)
    lower, _ = exp_envelope(rat(64, 4159), 4)
    require(rlt(rmul(rat(4160), rpower(rsub(upper, rat(1)), 2)),
                rat(99991, 100000)), "external_fixed_point_upper")
    require(rlt(rat(50007, 50000),
                rmul(rat(4159), rpower(rsub(lower, rat(1)), 2))),
            "external_fixed_point_lower")
    _, mass_upper = exp_envelope(rat(677, 1000), 8)
    require(rlt(mass_upper, rat(246, 125)),
            "external_mass_finite_constant")
    require(rlt(rat(246, 125), rat(63, 32)),
            "external_mass_comparison")
    print("ATLAS4D_EXTERNAL|source=ANAXIA_4Y_M_SINGLE_CUBE"
          "|mode=EXACT_INTEGER_REPLAY|finite_constants=PASS"
          "|4D_WILSON_WEIGHT=NOT_DERIVED|continuum_mass_gap=OPEN|json=0")


def hbp_nodes(text):
    rows = {}
    for line in text.splitlines():
        if not line.startswith("NODE|"):
            continue
        fields = {}
        for part in line.split("|")[1:]:
            if "=" in part:
                key, value = part.split("=", 1)
                fields[key] = value
        uid = fields.get("id", "")
        require(uid and uid not in rows, "duplicate_or_blank_node")
        require(fields.get("source", "").startswith("https://"),
                "unsourced_proof_node")
        require(fields.get("status", "") in (
            "FINITE_PASS", "DRAFT_CHECKED", "CONDITIONAL", "OPEN",
            "HOLD", "FINITE_S3", "EXTERNAL", "CANDIDATE"),
            "invalid_proof_status")
        rows[uid] = fields
    require(len(rows) == 55, "atlas_expected_nodes")
    for uid, row in rows.items():
        dependencies = row.get("dependencies", "NONE")
        for dep in dependencies.split(","):
            require(dep == "NONE" or dep in rows,
                    "unknown_dependency_" + uid)
        if uid.startswith("YM4-Q"):
            require(row["status"] == "OPEN", "missing_open_scope")
        if row["status"] == "FINITE_S3":
            require("Finite-universe-Yang-mills" in row["source"],
                    "wrong_group_for_finite_certificate")
        if row["status"] == "CANDIDATE":
            require("2610.00341v4" in row["source"]
                    or "2611.00492v1" in row["source"],
                    "unsupported_external_proof_promotion")
    require(sum(1 for uid in rows if uid.startswith("YM4-Q")) == 11,
            "open_subgates_missing")
    require(sum(1 for v in rows.values()
                if v["status"] == "CANDIDATE") == 2,
            "external_search_node_mismatch")
    require(rows["YM4-Q10"]["status"] == "OPEN",
            "continuum_gap_must_remain_open")
    return rows


def verify_no_runtime_code(page):
    lower = page.lower()
    require("<script" not in lower, "script_in_atlas")
    require("javascript:" not in lower, "javascript_scheme_in_atlas")
    require("onload=" not in lower, "runtime_handler_in_atlas")
    require("onerror=" not in lower, "runtime_handler_in_atlas")


def atlas_provenance():
    folder = Path("docs") / "certificate-atlas"
    hbp = (folder / "ATLAS-INDEX.hbp").read_text(encoding="utf-8")
    manifest = (folder / "certificates.json").read_text(encoding="utf-8")
    page = (folder / "index.html").read_text(encoding="utf-8")
    overview = (folder / "overview.svg").read_text(encoding="utf-8")
    ledger = (folder / "BRIDGE-LEDGER.md").read_text(encoding="utf-8")
    help_text = (folder / "OPEN-3D-VIEWER.md").read_text(encoding="utf-8")

    records = hbp_nodes(hbp)
    verify_no_runtime_code(page)
    require(page.count('<svg class="pane ') == 12,
            "four_views_times_three_cameras")
    require(page.count('<article class="entry" id="') == 55,
            "rendered_source_cards_mismatch")
    for view in ("proof", "wilson", "cutoff", "bridges"):
        for angle in ("0", "1", "2"):
            require('class="pane ' + view + ' a' + angle + '"' in page,
                    "missing_camera_" + view + angle)
    for uid, row in records.items():
        require('id="' + uid + '"' in page,
                "no_clickable_record_" + uid)
        require(row["source"] in manifest,
                "lost_source_in_machine_manifest_" + uid)
        require('"id": "' + uid + '"' in manifest,
                "lost_proof_node_in_json_" + uid)
    for uid in sorted(records):
        if uid.startswith("YM4-Q"):
            require('href="#' + uid + '"' in page,
                    "open_work_not_clickable_" + uid)
            require(uid in ledger, "open_gate_absent_from_ledger_" + uid)
    require("OPEN CERTIFICATES" in page, "no_open_certificates_section")
    require("Certificate" in page, "missing_header")
    require("Finite-universe-Yang-mills" in page,
            "finite_repository_link_missing")
    require("anaxia-research/4Y-M" in ledger,
            "attributed_external_certificates_missing")
    require("2611.00492v1" in ledger, "conditional_Lean_source_missing")
    require("continuum_mass_gap=OPEN" in hbp,
            "wrong_continuum_claim_status")
    require('"pr_events":' in manifest and '"resources":' in manifest,
            "source_audit_incomplete")
    require(overview.startswith("<svg ") and overview.count("<circle ") >= 50,
            "four_panel_overview_unavailable")
    require("raw.githack.com" in help_text,
            "live_viewer_instructions_missing")

    # Negative controls: reject a mathematical status mutation and a broken
    # graph mode; never convert the finite certificate into SU2 continuum.
    failures = 0
    for bad in (
        hbp.replace("id=YM4-Q10|status=OPEN",
                    "id=YM4-Q10|status=FINITE_PASS"),
        hbp.replace("id=YM4-Q11|status=OPEN",
                    "id=YM4-Q11|status=FINITE_S3"),
    ):
        try:
            hbp_nodes(bad)
        except ValueError:
            failures += 1
    for bad in (page + "<script></script>", page + " onload=bad"):
        try:
            verify_no_runtime_code(bad)
        except ValueError:
            failures += 1
    require(failures == 4, "negative_scope_controls_not_enforced")
    print("ATLAS4D_INDEX|nodes=55|open_gates=11|external_leads=2"
          "|crossrepo=3|json=0")
    print("ATLAS4D_VIEW|graph_modes=4|camera_positions=3"
          "|script_free=YES|source_cards=55|json=0")
    print("ATLAS4D_ADVERSARIES|negative_controls=4_REJECTED"
          "|physics_from_plot=NONE|json=0")


def main():
    external_one_cube_exact_rational()
    atlas_provenance()
    print("ATLAS4D_VERDICT|source_ledger=PASS|external_exact_constants=PASS"
          "|3D_graph=PASS|open_dependencies=VISIBLE"
          "|continuous_SU2_mass_gap=OPEN|json=0")


if __name__ == "__main__":
    main()
