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
    require(len(rows) == 112, "atlas_expected_nodes")
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
            require(uid.startswith("EXT-"), "external_source_id_required")
            require("github.com/" in row["source"]
                    or "arxiv.org/" in row["source"]
                    or "hexagonmath.org/" in row["source"]
                    or "doi.org/" in row["source"],
                    "unsupported_external_proof_promotion")
            if "/blob/" in row["source"]:
                require("/blob/main/" not in row["source"],
                        "external_candidate_must_pin_commit")
    require(sum(1 for uid in rows if uid.startswith("YM4-Q")) == 11,
            "open_subgates_missing")
    require(sum(1 for v in rows.values()
                if v["status"] == "CANDIDATE") == 22,
            "external_search_node_mismatch")
    require(rows["YM4-WG09-ORDER"]["status"] == "FINITE_PASS",
            "fixed_L2_WG09_order_not_accepted")
    require(rows["YM4-VOL01"]["status"] == "DRAFT_CHECKED",
            "volume_uniform_status_promoted_without_proof")
    require(rows["YM4-WG09-ORBIT"]["status"] == "FINITE_PASS"
            and rows["YM4-WG09-HAAR"]["status"] == "FINITE_PASS"
            and rows["YM4-WG09-SPIN"]["status"] == "FINITE_PASS",
            "missing_original_Haar_and_spin_evidence")
    require(rows["YM4-VOL03"]["status"] == "DRAFT_CHECKED",
            "local_cube_not_final_global_gap")
    require(rows["YM4-VOL05"]["status"] == "CONDITIONAL",
            "published_Dobrushin_and_transfer_not_independently_formalized")
    require(rows["YM4-VOL05-GEOM"]["status"] == "FINITE_PASS",
            "VOL05_rational_geometry_check_missing")
    require(rows["YM4-VOL06"]["status"] == "CONDITIONAL",
            "VOL06_external_analytic_acceptance_required")
    require(rows["YM4-VOL06-GEOM"]["status"] == "DRAFT_CHECKED",
            "VOL06_geometry_replay_not_full_analytic_signoff")
    require(rows["YM4-VOL06-AUDIT"]["status"] == "DRAFT_CHECKED",
            "VOL06_analytic_audit_premature_promotion")
    require(rows["YM4-VOL07"]["status"] == "CONDITIONAL",
            "VOL07_conditional_cube_gate_premature_promotion")
    require(rows["YM4-VOL07-RATE"]["status"] == "DRAFT_CHECKED",
            "VOL07_integer_rate_model_not_SU2_weak_coupling")
    for uid in ("YM4-VOL08", "YM4-VOL08-TV", "YM4-VOL08-AUDIT"):
        require(rows[uid]["status"] == "DRAFT_CHECKED",
                "VOL08_local_star_premature_continuum_promotion_" + uid)
    for uid in ("YM4-VOL09", "YM4-VOL09-AUDIT"):
        require(rows[uid]["status"] == "DRAFT_CHECKED",
                "VOL09_periodic_marginal_must_not_be_promoted_to_cube_" + uid)
    require(rows["YM4-VOL10-BOX"]["status"] == "DRAFT_CHECKED",
            "VOL10_finite_box_marginal_not_physical_cube")
    require(rows["YM4-VOL10-ISLAND"]["status"] == "CONDITIONAL",
            "VOL10_conditional_cluster_rho_unproved")
    require(rows["YM4-VOL10-AUDIT"]["status"] == "DRAFT_CHECKED",
            "VOL10_audit_not_external_peer_signoff")
    require(rows["YM4-VOL04"]["status"] == "DRAFT_CHECKED",
            "VOL04_fourth_coefficient_promoted_as_full_gap")
    require(rows["YM4-VOL04-AUDIT"]["status"] == "FINITE_PASS",
            "VOL04_independent_parity_audit_missing")
    require(rows["EXT-NS-CELL"]["status"] == "EXTERNAL",
            "external_fluid_not_original_SU2_proof")
    require(rows["YM4-Q10"]["status"] == "OPEN",
            "continuum_gap_must_remain_open")
    return rows


def verify_no_runtime_code(page):
    lower = page.lower()
    require("<script" not in lower, "script_in_atlas")
    require("javascript:" not in lower, "javascript_scheme_in_atlas")
    require("onload=" not in lower, "runtime_handler_in_atlas")
    require("onerror=" not in lower, "runtime_handler_in_atlas")


def quaternion_mul(a, b):
    w, x, y, z = a
    bw, bx, by, bz = b
    return (
        rsub(rsub(rsub(rmul(w, bw), rmul(x, bx)), rmul(y, by)),
             rmul(z, bz)),
        radd(rsub(radd(rmul(w, bx), rmul(x, bw)), rmul(z, by)),
             rmul(y, bz)),
        radd(radd(rsub(rmul(w, by), rmul(x, bz)), rmul(y, bw)),
             rmul(z, bx)),
        radd(rsub(radd(rmul(w, bz), rmul(x, by)), rmul(y, bx)),
             rmul(z, bw)),
    )


def quaternion_inverse(a):
    return a[0], rneg(a[1]), rneg(a[2]), rneg(a[3])


def quaternion_equal(a, b):
    return all(req(x, y) for x, y in zip(a, b))


def quaternion_product(items):
    result = rat(1), rat(0), rat(0), rat(0)
    for item in items:
        result = quaternion_mul(result, item)
    return result


def exact_jacobian_su2_fixture():
    # Reconstruct the source's fixed rational quaternion example, no remote
    # code executed, and prove Wilson trace algebra on the same inputs.
    links = (
        (rat(3, 5), rat(4, 5), rat(0), rat(0)),
        (rat(5, 13), rat(0), rat(12, 13), rat(0)),
        (rat(8, 17), rat(0), rat(0), rat(15, 17)),
        (rat(0), rat(1), rat(0), rat(0)),
    )
    gauges = (
        (rat(4, 5), rat(3, 5), rat(0), rat(0)),
        (rat(12, 13), rat(0), rat(5, 13), rat(0)),
        (rat(15, 17), rat(0), rat(0), rat(8, 17)),
        (rat(0), rat(0), rat(1), rat(0)),
    )
    for q in links + gauges:
        norm = rat(0)
        for t in q:
            norm = radd(norm, rmul(t, t))
        require(req(norm, rat(1)), "nonunit_SU2_quaternion")
    original = quaternion_product(links)
    transformed = quaternion_product(tuple(
        quaternion_mul(quaternion_mul(gauges[i], links[i]),
                       quaternion_inverse(gauges[(i + 1) % 4]))
        for i in range(4)))
    conjugate = quaternion_mul(
        quaternion_mul(gauges[0], original),
        quaternion_inverse(gauges[0]))
    require(quaternion_equal(transformed, conjugate),
            "finite_SU2_gauge_conjugacy")
    require(req(original[0], transformed[0]),
            "Wilson_scalar_conjugacy")
    # Tr(U)Tr(V) = Tr(UV) + Tr(U V^-1), unnormalized SU2 traces.
    u, v = links[0], links[1]
    tr_left = rmul(rmul(rat(2), u[0]), rmul(rat(2), v[0]))
    tr_right = radd(
        rmul(rat(2), quaternion_mul(u, v)[0]),
        rmul(rat(2), quaternion_mul(u, quaternion_inverse(v))[0]),
    )
    require(req(tr_left, tr_right), "SU2_single_trace_closure")
    wrong = quaternion_product((links[0], quaternion_inverse(links[1]),
                                links[2], links[3]))
    require(not quaternion_equal(wrong, original),
            "orientation_negative_control")
    print("ATLAS4D_SU2|source=JACOBIAN_EXACT_RATIONAL_FIXTURE"
          "|gauge_conjugacy=PASS|quaternion_and_traces=PASS"
          "|SU2_loop_identity=PASS|Haar_integral=NOT_CLAIMED|json=0")


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
    require(page.count('<article class="entry" id="') == 112,
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
    for uid in ("YM4-WT01", "YM4-WC01", "YM4-WV01",
                "YM4-WG01", "YM4-WG02", "YM4-WG03", "YM4-WG04",
                "YM4-WG05", "YM4-WG06", "YM4-WG07", "YM4-WG08",
                "YM4-WG09-ORBIT", "YM4-WG09-HAAR", "YM4-WG09-SPIN",
                "YM4-WG09-ORDER", "YM4-VOL01"):
        require('href="#' + uid + '"' in page,
                "missing_clickable_3d_node_" + uid)
        require(page.count('href="#' + uid + '"') >= 12,
                "missing_new_node_in_some_camera_" + uid)
    require(overview.count("index.html#YM4-WG09-ORDER") == 4
            and overview.count("index.html#YM4-VOL01") == 4,
            "four_overview_panels_not_reconciled")
    for artifact in (
        "YM4-WG09-FULL-OPERATOR-FINITE-BETA-20261121.hbp",
        "YM4-WG09-INDEPENDENT-SPIN-ENUM-20261121.hbp",
        "YM4-WG09-SECOND-THIRD-EXACT-LOCAL-RECEIPT-20261121.hbp",
        "YM4-WG09-STRUCTURAL-PILOT-20261121.hbp",
        "ym4_su2_wg09_full_operator_remainder.py",
        "ym4_su2_wg09_independent_spin_enumeration.py",
        "NOTE-YM4-VOL01-VOLUME-SLOPE-OBSTRUCTION-20261122.md",
    ):
        require(artifact in manifest, "missing_atlas_source_" + artifact)
    require('"curated_records": 112' in manifest
            and '"resource_files": 548' in manifest
            and '"pr_events": 103' in manifest,
            "machine_manifest_totals_mismatch")
    volume_note = (folder / "NOTE-YM4-VOL01-VOLUME-SLOPE-OBSTRUCTION-20261122.md").read_text(encoding="utf-8")
    require("volume_L_ge3_first_two_plaquette_coefficients=SCALAR" in hbp,
            "VOL01_second_order_not_in_proof_index")
    require("tfrac14" in volume_note
            and "third-order connected" in volume_note,
            "VOL01_exact_cancellation_note_unlinked")
    require("All L>=3 plaquette-band first variation zero and vacuum-reduced second-order matrix scalar" in manifest,
            "VOL01_manifest_not_reconciled")
    require("YM4-VOL02" in records and
            records["YM4-VOL02"]["status"] == "DRAFT_CHECKED",
            "VOL02_proof_status_missing")
    require(page.count('href="#YM4-VOL02"') >= 12,
            "VOL02_not_visible_in_all_3d_views")
    require(overview.count("index.html#YM4-VOL02") == 4,
            "VOL02_four_panel_link_missing")
    require("PREDICT-YM4-VOL02-THIRD-MAGNETIC-SELECTION-20261122.hbp"
            in manifest and "ym4_su2_vol02_third_parity.py" in manifest,
            "VOL02_prediction_and_independent_replay_missing")
    require("first_possible_nonscalar=FOURTH" in hbp
            and "volume_uniform_mass_gap=OPEN" in hbp,
            "VOL02_scope_boundary_missing")
    for uid in ("YM4-VOL03", "EXT-NS-CELL"):
        require(uid in records and page.count('href="#' + uid + '"') >= 12,
                "missing_new_pinned_3D_certificate_" + uid)
        require(overview.count('href="index.html#' + uid + '"') == 4,
                "new_external_or_cube_4panel_node_missing_" + uid)
    require("YM4-VOL03-CUBE-HAAR-TREE-20261122.hbp" in manifest
            and "ym4_su2_vol03_cube_haar_cell_tree.py" in manifest
            and "lean/comparator-cell-layer.json" in manifest,
            "VOL03_and_upstream_Lean_sources_not_pinned")
    require("six_face_Haar=1/16" in hbp and
            "isolated_cube_norm_all_L_ge3=5/128" in hbp and
            "raw_fourth_cube_W=1/256" in hbp and
            "numerical_certificate=UNAVAILABLE" in hbp and
            "global_physical_Feshbach=OPEN" in hbp,
            "VOL03_local_vs_external_scope_not_closed")
    require("cube_only_matrix_norm=5/128" in (folder / "YM4-VOL03-CUBE-HAAR-TREE-20261122.hbp").read_text(encoding="utf-8"),
            "cube_only_norm_missing_from_frozen_receipt")
    for uid in ("YM4-VOL04", "YM4-VOL04-AUDIT"):
        require(uid in records and page.count('href="#' + uid + '"') >= 12,
                "VOL04_missing_live_3d_node_" + uid)
        require(overview.count('href="index.html#' + uid + '"') == 4,
                "VOL04_missing_four_panel_card_" + uid)
    require("YM4-VOL04-COMPLETE-FOURTH-SCHUR-20261122.hbp" in manifest
            and "YM4-VOL04-INDEPENDENT-QUARTIC-PARITY-20261122.hbp" in manifest
            and "ym4_su2_vol04_full_fourth_schur.py" in manifest
            and "ym4_su2_vol04_independent_parity_audit.py" in manifest,
            "VOL04_exact_and_cleanroom_provenance_missing")
    require("Q4_uniform_L_ge3_norm=7/48" in hbp and
            "beta5_remainder_uniform_in_L=OPEN" in hbp and
            "within_band_splitting_upper=55/(32L2)" in hbp,
            "VOL04_full_coefficient_vs_uniform_beta_scope_error")
    for uid in ("YM4-VOL05", "YM4-VOL05-GEOM"):
        require(uid in records and page.count('href="#' + uid + '"') >= 12,
                "VOL05_missing_new_view_node_" + uid)
        require(overview.count('href="index.html#' + uid + '"') == 4,
                "VOL05_missing_exact_four_panel_href_" + uid)
    require("YM4-VOL05-WILSON-SPECTRAL-SUPPORT-20261122.hbp" in manifest
            and "ym4_su2_vol05_wilson_spectral_support.py" in manifest,
            "VOL05_source_and_HBP_not_pinned")
    require("Wilson_visible_ratio_le=9/500" in hbp
            and "total_local_Wilson_weight_ge=247/1000" in hbp
            and "external_Dobrushin_theorem=REQUIRED" in hbp
            and "weak_coupling_scaling=OPEN" in hbp,
            "strong_coupling_channel_promoted_as_continuum_proof")
    for uid in ("YM4-VOL06", "YM4-VOL06-GEOM", "YM4-VOL06-AUDIT"):
        require(uid in records and page.count('href="#' + uid + '"') >= 12,
                "VOL06_missing_one_of_twelve_graph_camera_nodes_" + uid)
        require(overview.count('href="index.html#' + uid + '"') == 4,
                "VOL06_missing_one_of_four_overview_links_" + uid)
    require("YM4-VOL06-FULL-PHYSICAL-GAP-20261122.hbp" in manifest
            and "ym4_su2_vol06_full_spectrum.py" in manifest
            and "NOTE-YM4-VOL06-FULL-PHYSICAL-STRONG-COUPLING-GAP-20261122.md" in manifest,
            "VOL06_original_frozen_sources_missing")
    require("YM4-VOL06-INDEPENDENT-ANALYTIC-AUDIT-20261122.md" in manifest
            and "finite_bare_strong_coupling=RECONSTRUCTION_PASS" in hbp,
            "VOL06_review_not_source_indexed")
    require("all_physical_transfer_ratio_le=9/500" in hbp
            and "external_Dobrushin_transfer_audit=REQUIRED" in hbp
            and "11_continuum_gates=OPEN" in hbp,
            "VOL06_conditional_strong_coupling_scope_missing")
    for uid in ("YM4-VOL07", "YM4-VOL07-RATE"):
        require(uid in records and page.count('href="#' + uid + '"') >= 12,
                "VOL07_missing_one_of_twelve_views_" + uid)
        require(overview.count('href="index.html#' + uid + '"') == 4,
                "VOL07_missing_one_of_four_overview_links_" + uid)
    require("YM4-VOL07-PHYSICAL-BLOCK-RATE-20261122.hbp" in manifest
            and "ym4_su2_vol07_block_rate.py" in manifest
            and "NOTE-YM4-VOL07-PHYSICAL-BLOCK-GAP-CRITERION-20261122.md" in manifest,
            "VOL07_exact_provenance_missing")
    require("mass_floor=-log_q_over_ab" in hbp
            and "SU2_weak_block_influence=OPEN" in hbp
            and "11_original_gates=OPEN" in hbp,
            "VOL07_conditional_rate_promoted_as_physics")
    for uid in ("YM4-VOL08", "YM4-VOL08-TV", "YM4-VOL08-AUDIT"):
        require(uid in records and page.count('href="#' + uid + '"') >= 12,
                "VOL08_missing_one_of_twelve_views_" + uid)
        require(overview.count('href="index.html#' + uid + '"') == 4,
                "VOL08_missing_one_of_four_overview_links_" + uid)
    require("YM4-VOL08-WILSON-STAR-20261122.hbp" in manifest
            and "ym4_su2_vol08_wilson_star.py" in manifest
            and "NOTE-YM4-VOL08-ORIGINAL-SU2-WILSON-STAR-20261122.md" in manifest
            and "YM4-VOL08-HAAR-BY-PARTS-INDEPENDENT-AUDIT-20261122.md" in manifest,
            "VOL08_original_SU2_Haar_provenance_missing")
    require("one_external_link_changed=YES" in hbp
            and "same_gauge_invariant_plaquette_TV_ge=29/36" in hbp
            and "weak_coupling_physical_cube=OPEN" in hbp
            and "11_original_gates=OPEN" in hbp,
            "VOL08_original_SU2_boundary_obstruction_promoted_as_cube")
    for uid in ("YM4-VOL09", "YM4-VOL09-AUDIT"):
        require(uid in records and page.count('href="#' + uid + '"') >= 12,
                "VOL09_missing_one_of_twelve_views_" + uid)
        require(overview.count('href="index.html#' + uid + '"') == 4,
                "VOL09_missing_one_of_four_overview_links_" + uid)
    require("YM4-VOL09-PERIODIC-GOOD-STAR-20261122.hbp" in manifest
            and "ym4_su2_vol09_periodic_good_star.py" in manifest
            and "NOTE-YM4-VOL09-PERIODIC-GOOD-STAR-FREQUENCY-20261122.md" in manifest
            and "YM4-VOL09-KL-PERIODIC-GOOD-STAR-AUDIT-20261122.md" in manifest,
            "VOL09_original_SU2_good_star_provenance_missing")
    require("volume_independent=YES" in hbp
            and "bad_star_probability_le=2000/59049" in hbp
            and "arbitrary_exterior_cube=OPEN" in hbp
            and "11_original_gates=OPEN" in hbp,
            "VOL09_periodic_equilibrium_promoted_as_all_boundary_cube")
    for uid in ("YM4-VOL10-BOX", "YM4-VOL10-ISLAND", "YM4-VOL10-AUDIT"):
        require(uid in records and page.count('href="#' + uid + '"') >= 12,
                "VOL10_missing_one_of_twelve_cameras_" + uid)
        require(overview.count('href="index.html#' + uid + '"') == 4,
                "VOL10_missing_one_of_four_overview_panels_" + uid)
    require("YM4-VOL10-BAD-ISLAND-20261122.hbp" in manifest
            and "ym4_su2_vol10_bad_island.py" in manifest
            and "NOTE-YM4-VOL10-BAD-ISLAND-CRITERION-20261122.md" in manifest
            and "YM4-VOL10-ORIGINAL-SU2-BOX-ISLAND-AUDIT-20261122.md" in manifest,
            "VOL10_original_SU2_box_and_island_sources_missing")
    require("any_bad_probability_le=16064/531441" in hbp
            and "number_bad_stars_le=4_times_number_defective_plaquettes" in hbp
            and "joint_independent_star_rho=OPEN" in hbp
            and "arbitrary_exterior_cube=OPEN" in hbp
            and "11_original_gates=OPEN" in hbp,
            "VOL10_false_independent_bad_island_or_continuum_promotion")
    require("first_neutral_Wilson_weight_fixed_L2=FINITE_PASS"
            in hbp and "uniform_volume_Wilson_weight=OPEN" in hbp,
            "fixed_volume_vs_continuum_scope_mismatch")
    require("EXT-FUSION-6J" in records and "YM4-SW01" in records,
            "new_exact_SU2_spectral_sources_missing")
    require(records["YM4-SW01"]["status"] == "DRAFT_CHECKED",
            "exact_dual_verification_tier")
    require("EXTERNAL-SEARCH-ROUND2-20261121.md" in manifest,
            "external_round2_references_missing")
    require("PREDICT-SPECTRAL-WINDOW-DUAL-20261121.hbp" in manifest,
            "spectral_prediction_not_indexed")
    require("source_cards=76" not in page,
            "runtime_receipts_must_not_be_claimed_in_viewer")
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
        hbp.replace("id=YM4-WG09-ORDER|status=FINITE_PASS",
                    "id=YM4-WG09-ORDER|status=CONDITIONAL"),
        hbp.replace("id=YM4-VOL01|status=DRAFT_CHECKED",
                    "id=YM4-VOL01|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL03|status=DRAFT_CHECKED",
                    "id=YM4-VOL03|status=FINITE_PASS"),
        hbp.replace("id=EXT-NS-CELL|status=EXTERNAL",
                    "id=EXT-NS-CELL|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL04|status=DRAFT_CHECKED",
                    "id=YM4-VOL04|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL04-AUDIT|status=FINITE_PASS",
                    "id=YM4-VOL04-AUDIT|status=OPEN"),
        hbp.replace("id=YM4-VOL05|status=CONDITIONAL",
                    "id=YM4-VOL05|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL05-GEOM|status=FINITE_PASS",
                    "id=YM4-VOL05-GEOM|status=OPEN"),
        hbp.replace("id=YM4-VOL06|status=CONDITIONAL",
                    "id=YM4-VOL06|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL06-GEOM|status=DRAFT_CHECKED",
                    "id=YM4-VOL06-GEOM|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL06-AUDIT|status=DRAFT_CHECKED",
                    "id=YM4-VOL06-AUDIT|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL07|status=CONDITIONAL",
                    "id=YM4-VOL07|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL07-RATE|status=DRAFT_CHECKED",
                    "id=YM4-VOL07-RATE|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL08|status=DRAFT_CHECKED",
                    "id=YM4-VOL08|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL08-TV|status=DRAFT_CHECKED",
                    "id=YM4-VOL08-TV|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL08-AUDIT|status=DRAFT_CHECKED",
                    "id=YM4-VOL08-AUDIT|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL09|status=DRAFT_CHECKED",
                    "id=YM4-VOL09|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL09-AUDIT|status=DRAFT_CHECKED",
                    "id=YM4-VOL09-AUDIT|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL10-BOX|status=DRAFT_CHECKED",
                    "id=YM4-VOL10-BOX|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL10-ISLAND|status=CONDITIONAL",
                    "id=YM4-VOL10-ISLAND|status=FINITE_PASS"),
        hbp.replace("id=YM4-VOL10-AUDIT|status=DRAFT_CHECKED",
                    "id=YM4-VOL10-AUDIT|status=FINITE_PASS"),
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
    require(failures == 25, "negative_scope_controls_not_enforced")
    print("ATLAS4D_INDEX|nodes=112|open_gates=11|external_leads=22"
          "|crossrepo=3|json=0")
    print("ATLAS4D_VIEW|graph_modes=4|camera_positions=3"
          "|script_free=YES|source_cards=112|json=0")
    print("ATLAS4D_ADVERSARIES|negative_controls=25_REJECTED"
          "|physics_from_plot=NONE|json=0")


def main():
    external_one_cube_exact_rational()
    exact_jacobian_su2_fixture()
    atlas_provenance()
    print("ATLAS4D_VERDICT|source_ledger=PASS|external_exact_constants=PASS"
          "|3D_graph=PASS|open_dependencies=VISIBLE"
          "|continuous_SU2_mass_gap=OPEN|json=0")


if __name__ == "__main__":
    main()
