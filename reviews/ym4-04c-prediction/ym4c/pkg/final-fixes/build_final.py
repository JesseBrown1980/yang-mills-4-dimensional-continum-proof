#!/usr/bin/env python3
# YM4-04C: apply the package critic's findings (pkg/critic3/, two blocking items and ten fixes) to the pre-critic
# package in pkg/, and write the deliverables of the freeze commit to ym4c/final/ under their repo-relative names.
# It also writes the three manifests (sha256, two spaces, path relative to the scratchpad directory, which is
# reviews/ym4-04c-prediction/ in the commit), fills their sha256 values and line counts into the prediction file,
# the note and the engine plan, computes the pin (head -n 41 | sha256sum) into note section 15, and reruns
# derive_checks.py. This file holds no hash of its own outputs, so the package manifest can list it.
# Scratch packaging, not an engine. Integers and strings only. Run: python3 -I -B build_final.py
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)                      # scratchpad/ym4c/pkg
YM4C = os.path.dirname(PKG)                      # scratchpad/ym4c
SCRATCH = os.path.dirname(YM4C)                  # the scratchpad directory = reviews/ym4-04c-prediction/ in the commit
FINAL = os.path.join(YM4C, 'final')
DOCS = os.path.join(FINAL, 'docs')
REV = os.path.join(FINAL, 'reviews', 'ym4-04c-prediction')
PRED_NAME = 'PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp'
NOTE_NAME = 'NOTE-YM4-04C-LOCAL-POLYMER-NORM-20261109.md'


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(path):
    with open(path, 'rb') as f:
        return sha_bytes(f.read())


def rep(text, old, new, count=1, tag=''):
    n = text.count(old)
    assert n == count, ('edit %s: expected %d occurrence(s), found %d: %r' % (tag, count, n, old[:120]))
    return text.replace(old, new)


def between(text, start, end, new, tag=''):
    """replace text[start_marker : end_marker) by new; both markers unique."""
    assert text.count(start) == 1 and text.count(end) == 1, ('markers', tag)
    i, j = text.index(start), text.index(end)
    assert i < j, ('marker order', tag)
    return text[:i] + new + text[j:]


def set_field(line, key, value):
    fields = line.split('|')
    hits = [k for k, f in enumerate(fields) if f.startswith(key + '=')]
    assert len(hits) == 1, ('field', key, len(hits))
    fields[hits[0]] = key + '=' + value
    return '|'.join(fields)


pred = read(os.path.join(PKG, PRED_NAME))
note = read(os.path.join(PKG, NOTE_NAME))
plan = read(os.path.join(PKG, 'engine_plan-final.txt'))
ledger = read(os.path.join(PKG, 'ledger_rows-final.txt'))
dchk = read(os.path.join(PKG, 'derive_checks.py'))
assert sha_bytes(pred.encode()) == 'f77c51568fdf9eaec81010d7f6cff12811ac2da65be56cd7cd3a74e37518ad61'

# ============================== the prediction file ==============================
P = pred
# header
P = rep(P, "neither_the_40-line_draft_nor_v2_was_committed,so_these_41_lines_carry_the_final_constants_in_their_own_rows_and_nothing_is_appended",
        "neither_the_40-line_draft_nor_v2_was_committed,so_these_41_lines_carry_the_final_constants_in_their_own_rows_and_nothing_is_appended;"
        "the_package_critic's_two_blocking_items_and_ten_fixes_(pkg/critic3/)_are_applied_in_these_rows,also_before_any_commit;"
        "they_move_tags,scopes,method_fields_and_one_fault_specification,and_no_predicted_value", tag='P1')
P = rep(P, "supersedes=the_uncommitted_scratch_file_scratchpad/ym4c/pkg/PREDICTION-v2.hbp,41_lines,sha256_b48e29d39f76eac50e54b285548ac4131b97ace05cab9e315463fcce4f20d30f,which_superseded",
        "supersedes=the_uncommitted_scratch_file_scratchpad/ym4c/pkg/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp,41_lines,"
        "sha256_f77c51568fdf9eaec81010d7f6cff12811ac2da65be56cd7cd3a74e37518ad61,the_final_as_the_package_critic_read_it,"
        "which_superseded_scratchpad/ym4c/pkg/PREDICTION-v2.hbp,41_lines,sha256_b48e29d39f76eac50e54b285548ac4131b97ace05cab9e315463fcce4f20d30f,which_superseded",
        tag='P2')
P = rep(P, "merged_into_canonical_sections;the_final_values_recomputed|",
        "merged_into_canonical_sections;the_final_values_recomputed;the_package_critic's_findings_applied|", tag='P3')
# THEOREMS (fix 8)
P = rep(P, "the_Kotecky-Preiss_per-polymer_corollary_sum_{X_containing_Gamma}_abs(Phi(X))e^{d(X)}<=abs(z_Gamma)e^{a(Gamma)+d(Gamma)},d(X)_summed_over_the_polymers_of_X,with_alpha=t=delta'_and_theta=kappa;",
        "the_per-polymer_corollary_sum_{X_containing_Gamma}_abs(Phi(X))e^{d(X)}<=abs(z_Gamma)e^{a(Gamma)+d(Gamma)},d(X)_summed_over_the_polymers_of_X,with_alpha=t=delta'_and_theta=kappa,"
        "from_note_Proposition_3.18_(the_abstract_cluster_bounds_of_section_3,under_the_per-link_condition_(KP_w),which_note_Lemma_4.13_gives_at_every_off_link)_and_note_Lemma_3.15,"
        "in_note_Theorem_4.9_and_Corollary_4.10_(Kotecky-Preiss_a_cross-reference);", tag='P4')
P = rep(P, "G1_on_the_REPORTED_Kotecky-Preiss_theorem_(Commun._Math._Phys._103,1986);",
        "G1_on_note_Proposition_3.18_and_Lemma_3.15,so_its_one_REPORTED_input_is_the_exponential_formula_for_connected_graphs,which_G0_also_uses,"
        "and_the_Kotecky-Preiss_theorem_(Commun._Math._Phys._103,1986)_is_a_cross-reference_for_both;", tag='P5')
# DISCLOSURE
P = rep(P, "|freeze_checks=reviews/ym4-04c-prediction/derive_checks.py",
        "|package_critic=pkg/critic3/{spot,kp,g1,wlane,c09}.py_and_pkg/critic3/derive_checks_rerun.out:the_package_critic's_own_reads_of_this_package,"
        "in_Fractions_with_outward_rounding_(wlane.py_in_exact_Q(sqrt2)),floats_only_in_display;they_re-read_values_already_tagged_COMPUTED_or_CROSS_READ"
        "_(the_constants,C02,C04,C15,the_chains_and_edges_of_C05-C08_and_C11-C14,C16,the_G1_constants,C09,C10b,C10c,W01,W03_and_W06(b)'s_cubic)"
        "_and_read_no_NONE_clause;only_derive_checks_rerun.out_is_saved_as_output"
        "|final_fixes=pkg/final-fixes/fix_checks.py_with_fix_checks.out,in_Fractions_with_256-bit_outward_rounding_through_the_helpers_of_pkg/recompute/final_s_lane.py:"
        "the_chain_bounds_of_C07,C08,C11,C12,C14_and_C16_at_the_certified_delta_1_and_at_the_ends_of_the_frozen_delta_1_brackets,"
        "the_missing_tail_guard_reads_with_and_without_the_pole_test,the_one_position_support_variant_that_also_counts_the_coarse_Y_by_its_position-1_links,"
        "and_W01's_2^k*r_k;pkg/final-fixes/build_final.py_applies_the_package_critic's_findings_to_the_pre-critic_package,"
        "writes_the_deliverables_of_the_freeze_commit_and_the_three_manifests,and_computes_the_pin;neither_reads_a_NONE_clause"
        "|freeze_checks=reviews/ym4-04c-prediction/derive_checks.py", tag='P6')
P = rep(P, "it_reads_C10b's_moment_identity_at_one_rational_configuration,so_that_clause_is_COMPUTED",
        "it_reads_C10b's_moment_identity_at_one_rational_configuration,and_pkg/attack/G1-channel-instances.py_read_it_at_6_rational_(A,B),"
        "so_that_clause_is_CROSS_READ", tag='P7')
P = rep(P, "C01's_census_(polymer-norm/geometry_check.py,the_judge_prototype_and_pkg/attack/G0-count-checks.py);W06(b)_(exact_inertia,smallfield-largefield/d2_fiber_k0.py);",
        "C01's_census_(polymer-norm/geometry_check.py,the_judge_prototype_and_pkg/attack/G0-count-checks.py);"
        "C01's_A_c(n)_clause_(pkg/attack/G0-count-checks.py,every_off-link-connected_set_holding_a_class-1,2_or_3_off_link_on_fine_(Z/8)^4_through_n=6,"
        "each_count_below_6F_20(n),and_pkg/derive/G0-b-checks.py_through_n=4);"
        "C09's_cluster-exclusion_read_(pkg/attack/G0-count-checks.py,section_E:the_closed_sets_holding_all_8_line_links_of_a_coarse_plaquette_through_n=8_are_{4:1,8:16});"
        "C10's_holonomy_reads_(pkg/attack/G1-channel-instances.py,at_4_random_rational_configurations);"
        "C10b's_moment_identity_(pkg/attack/G1-channel-instances.py_at_6_rational_(A,B),derive_checks.py_at_one);"
        "W06(b)_and_W06(a)_in_the_k'=0_sector_(exact_inertia,smallfield-largefield/d2_fiber_k0.py);", tag='P8')
P = rep(P, "|manifests=",
        "|corrections_after_the_package_critic=C01's_A_c(n)_clause,C09's_cluster-exclusion_read_and_C10's_holonomy_reads_were_read_before_this_freeze_by_the_attack_lenses,"
        "so_they_move_from_prefreeze=NONE_to_CROSS_READ;C10b's_moment_identity_moves_from_COMPUTED_to_CROSS_READ;W06(a)_is_NONE_only_in_the_sectors_other_than_k'=0;"
        "C19's_missing_tail_removes_the_pole_test_with_the_tail,as_the_exact_run_that_pinned_its_effect_did;one_position_support_acts_in_the_fine-norm_routine_only;"
        "C07,C12_and_C16_read_their_chains_from_the_certified_delta_1;G1_cites_note_Proposition_3.18_in_place_of_the_Kotecky-Preiss_theorem;"
        "the_manifests_are_regenerated_hash-first;no_predicted_value_moves"
        "|manifests=", tag='P10')
P = '\n'.join(set_field(l, 'manifests',
        "reviews/ym4-04c-prediction/MANIFEST-ym4-04c-scratch.sha256:@@N_SCRATCH@@_lines,every_file_of_the_design-lane_tree_ym4-04c/_except_bytecode_caches,sha256_@@SHA_SCRATCH@@;"
        "reviews/ym4-04c-prediction/MANIFEST-ym4c-v2-checks.sha256:@@N_V2@@_lines,every_file_of_ym4c/pkg/v2-checks/,sha256_@@SHA_V2@@;"
        "reviews/ym4-04c-prediction/MANIFEST-ym4c-pkg.sha256:@@N_PKG@@_lines,every_file_of_the_package_tree_ym4c/_except_bytecode_caches,"
        "the_workflow's_state_file_ym4c/pkg-wf.json,which_the_workflow_rewrites,and_ym4c/final/,which_holds_the_deliverables_of_the_freeze_commit"
        "_(this_file,the_note,derive_checks.py,DERIVE-CHECKS.hbp,engine_plan.txt,ledger_rows.txt,the_three_manifests);it_covers_pkg/critic3/,pkg/final-fixes/"
        "_and_the_pre-critic_package_in_pkg/_as_the_package_critic_read_it,its_three_path-first_manifests_included,sha256_@@SHA_PKG@@;"
        "each_line_is_a_sha256,two_spaces_and_a_path_relative_to_reviews/ym4-04c-prediction/_(in_scratch,the_scratchpad_directory),"
        "so_sha256sum_-c_<manifest>_run_there_verifies_it;the_scratchpad_is_ephemeral,so_the_freeze_commit_carries_the_three_manifests_and_every_file_they_list"
        "_under_reviews/ym4-04c-prediction/,the_design-lane_tree_as_ym4-04c/_and_the_package_tree_as_ym4c/")
        if l.startswith('YM4_04C_DISCLOSURE|') else l for l in P.split('\n'))
# B1: the three pre-read clauses
P = rep(P, ";NONE_for_the_A_c(n)_clause|",
        ";CROSS_READ_for_the_A_c(n)_clause_(pkg/attack/G0-count-checks.py_enumerated_every_off-link-connected_set_holding_a_class-1,2_or_3_off_link"
        "_on_fine_(Z/8)^4_through_n=6_and_found_each_count_below_6F_20(n);pkg/derive/G0-b-checks.py_read_the_same_counts_through_n=4)|", tag='B1a')
P = rep(P, ";NONE_for_the_exclusion_read|",
        ";CROSS_READ_for_the_exclusion_read_(pkg/attack/G0-count-checks.py,section_E:the_closed_sets_holding_all_8_line_links_of_a_coarse_plaquette"
        "_through_n=8_are_{4:1,8:16},the_filling_and_the_16_one-cube_bumps)|", tag='B1b')
P = rep(P, ";NONE_for_the_holonomy_reads|",
        ";CROSS_READ_for_the_holonomy_reads_(pkg/attack/G1-channel-instances.py:at_4_random_rational_configurations_the_fine_2x2_loop_in_the_line_gauge"
        "_equals_V_P''_and_its_trace_is_unchanged_under_a_rational_fine_gauge_transformation,through_BU)|", tag='B1c')
# fix 4: C10b
P = rep(P, "COMPUTED_for_the_moment_identity,which_derive_checks.py_read_at_one_rational_configuration_before_this_freeze,so_the_engine's_moment_reads_count_as_reproductions",
        "CROSS_READ_for_the_moment_identity,an_exact_integral_that_pkg/attack/G1-channel-instances.py_read_at_6_rational_(A,B)_for_m=1..6"
        "_and_derive_checks.py_read_at_one_rational_configuration_before_this_freeze,so_the_engine's_moment_reads_count_as_reproductions", tag='F4')
# fix 5: W06(a)
P = rep(P, "prefreeze=CROSS_READ_for_(b)_(exact_inertia,smallfield-largefield/d2_fiber_k0.py);NONE_for_(a)|",
        "prefreeze=CROSS_READ_for_(b)_and_for_(a)_in_the_k'=0_sector,one_of_the_16_sectors_of_fine_4^4_(exact_inertia,smallfield-largefield/d2_fiber_k0.py,"
        "which_read_that_sector's_positivity_as_part_of_(b));NONE_for_(a)_in_the_sectors_other_than_k'=0|", tag='F5')
# fix 6: the chain method of C07, C12 and C16
P = rep(P, "with_upper_and_lower_exponential_enclosures_and_ln(1+x)_by_alternating_partial_sums|falsifier=C_0_or_C_1_read_NOT_MET_at_1/100;",
        "with_upper_and_lower_exponential_enclosures_and_ln(1+x)_by_alternating_partial_sums;every_chain_value_(c_fin(delta_1),delta_2,sum_k_delta_k)"
        "_is_read_from_the_engine's_certified_delta_1^+=6*alpha^+,with_alpha^+_the_certified_upper_end_of_the_least_root,"
        "not_from_the_upper_end_of_the_delta_1_bracket_frozen_above|falsifier=C_0_or_C_1_read_NOT_MET_at_1/100;", tag='F6a')
P = rep(P, "method=as_C07_and_C08,at_1/50,with_the_head-free_bound_as_a_lower_limit_for_every_count_vector_N(4..10)>=0|",
        "method=as_C07_and_C08,at_1/50,with_the_head-free_bound_as_a_lower_limit_for_every_count_vector_N(4..10)>=0;"
        "the_chain_is_read_from_the_engine's_certified_delta_1^+,not_from_the_upper_end_of_the_delta_1_bracket:sum_k_delta_k<=5.7463e-2_holds_at_the_certified"
        "_delta_1_in_[0.0363235365,0.0363235366]_and_fails_at_the_bracket_end_0.0363236,where_delta_1/(1-e^{-1})_is_above_0.05746308|", tag='F6b')
P = rep(P, "method=exact_rational_powers_and_products_of_the_C07_outputs;the_bound_sum_Y_sup_abs(R(Y))<=#links*delta*max_{#Y>=4}e^{-kappa*#Y}/#Y|",
        "method=exact_rational_powers_and_products_of_the_C07_outputs;the_bound_sum_Y_sup_abs(R(Y))<=#links*delta*max_{#Y>=4}e^{-kappa*#Y}/#Y;"
        "delta_20_is_read_from_C07's_certified_delta_1^+,not_from_the_upper_end_of_C07's_delta_1_bracket:e^{-19}*delta_1^+<=3.093991e-11<=3.0940e-11,"
        "while_e^{-19}*0.0055223_is_above_3.094032e-11|", tag='F6c')
# B2 and fix 7: C19
P = rep(P, "the_terms_n=11..48_and_the_n=49_tail_removed)->C04",
        "the_terms_n=11..48_and_the_n=49_tail_removed,and_the_pole_test_mu^+x^+<1,which_belongs_to_the_tail,is_removed_with_it)->C04", tag='B2')
P = rep(P, "one_position_support_(the_norm_routine_sets_#Y_to_the_number_of_links_of_Y_at_position_1,the_links_that_carry_V_in_the_line_gauge_(1,V),in_place_of_all_links_of_Y)->C10",
        "one_position_support_(the_fine-norm_routine_sets_#Y_to_the_number_of_links_of_Y_at_position_1,the_links_that_carry_V_in_the_line_gauge_(1,V),"
        "in_place_of_all_links_of_Y;the_coarse_norm_keeps_#Y''=4_for_the_output_Y=boundary_of_P'')->C10", tag='F7a')
P = rep(P, ";these_are_recorded_so_that_the_pinned_variants_are_the_ones_the_engine_plants",
        ";missing_tail_with_the_pole_test_kept:both_guard_reads_stay_NOT_MET_by_the_pole_at_1/40_and_0.02248,and_the_head-only_S_makes_the_refined_C_0"
        "_read_MET_at_0.02076_(alpha=2^-22,S^+<=9.27e-8),so_the_run_would_pass_the_C04_guard_and_fail_at_a_later_row,C06's_NOT_MET_at_0.02076_among_them;"
        "one_position_support_applied_also_to_the_coarse_norm,with_the_output_Y=boundary_of_P''_counted_by_its_links_at_position_1_for_the_next_blocking"
        "_(0,1_or_2_per_coarse_plaquette):the_coarse_norm_reads_6abs(s)(e^{kappa}+e^{2kappa})_and_the_ratio_(e^{-3kappa}+e^{-2kappa})/2_in_[0.5394486,0.5394487]"
        "_at_kappa=1/4,1_at_kappa=0,so_that_variant_lands_strictly_between_e^{-1}_and_1_and_still_fires_at_C10"
        ";these_are_recorded_so_that_the_pinned_variants_are_the_ones_the_engine_plants", tag='F7b')
# LEDGER row (fix 8)
P = rep(P, "REPORTED_relied_on=Kotecky-Preiss,Commun._Math._Phys._103_(1986)_491-498_(G1;a_cross-reference_for_G0);Finner",
        "REPORTED_relied_on=Finner", tag='L1')
P = rep(P, "the_exponential_formula_for_connected_graphs,Stanley,Enumerative_Combinatorics_vol._2_(1999)_Corollary_5.1.6_(G0);",
        "the_exponential_formula_for_connected_graphs,Stanley,Enumerative_Combinatorics_vol._2_(1999)_Corollary_5.1.6_(G0,and_G1_through_note_Lemma_3.15);", tag='L2')
P = rep(P, "cross-references_only:Graham,",
        "cross-references_only:Kotecky-Preiss,Commun._Math._Phys._103_(1986)_491-498_(G0_and_G1,whose_cluster_bounds_note_Proposition_3.18_proves),Graham,", tag='L3')
P = rep(P, "with_Proposition_3.18_(the_cluster_bounds),",
        "with_Proposition_3.18_(the_cluster_bounds,used_by_G0_and,through_Theorem_4.9_and_Corollary_4.10,by_G1),", tag='L4')
# SUMMARY (B1, fixes 4 and 5)
P = rep(P, "prefreeze_CROSS_READ=C01_(census),C03,the_C03_heads_of_C06,C08,C09,C12_and_C14,C17_(counts),W04_(float,reproduction),W06_(b)|",
        "prefreeze_CROSS_READ=C01_(census_and_the_A_c(n)_clause),C03,the_C03_heads_of_C06,C08,C09,C12_and_C14,C09's_cluster-exclusion_read,"
        "C10's_holonomy_reads,C10b's_moment_identity,C17_(counts),W04_(float,reproduction),W06_(b,and_(a)_in_the_k'=0_sector)|", tag='S1')
P = rep(P, "C10b_(values_and_the_moment_identity)", "C10b_(values)", tag='S2')
P = rep(P, "prefreeze_NONE=row_C18;clauses:C01's_A_c(n)_count,C09's_cluster-exclusion_read,C10's_holonomy_reads,C10c's_moment_reads,C19's_engine_exits,W06_(a),W07's_random_tiles|",
        "prefreeze_NONE=row_C18;clauses:C10c's_moment_reads,C19's_engine_exits,W06_(a)_in_the_sectors_other_than_k'=0,W07's_random_tiles|", tag='S3')

# ============================== the engine plan ==============================
E = plan
E = rep(E, "the slice and per-root comparisons of C10b and C10c, and the recomputed fault values.",
        "the slice and per-root comparisons of C10b and C10c, and the recomputed fault values. The package critic's findings are applied: "
        "the missing_tail and one_position_support specifications, the chain reads at the certified delta_1, the prefreeze tallies and the manifest check.", tag='E1')
E = rep(E, "the three manifests (MANIFEST-ym4-04c-scratch.sha256, 67 files; MANIFEST-ym4c-v2-checks.sha256, 19 files; MANIFEST-ym4c-pkg.sha256, 116 files) and every file they list.",
        "the three manifests (MANIFEST-ym4-04c-scratch.sha256, @@N_SCRATCH@@ files; MANIFEST-ym4c-v2-checks.sha256, @@N_V2@@ files; "
        "MANIFEST-ym4c-pkg.sha256, @@N_PKG@@ files), engine_plan.txt, ledger_rows.txt and every file the manifests list.", tag='E2')
E = rep(E, "The fallback 2delta' <= kappa and its factor are read beside the final ones and filed as separate receipt rows for the TG values.",
        "The fallback 2delta' <= kappa and its factor are read beside the final ones and filed as separate receipt rows for the TG values. "
        "Every chain (c_fin(delta_1), delta_2, sum_k delta_k and C16's delta_20) is read from the certified delta_1^+ = 6 alpha^+, with alpha^+ the certified "
        "upper end of the least root, never from the upper end of a frozen delta_1 bracket: C12's sum and C16's delta_20 hold at the certified value "
        "and fail at the bracket end.", tag='E3')
E = rep(E, "The norm routine counts #Y as all links of Y; the planted one_position_support counts only its position-1 links.",
        "The norm routine counts #Y as all links of Y; the planted one_position_support counts only its position-1 links, in the fine-norm routine only, "
        "so the coarse norm keeps #Y''.", tag='E4')
E = rep(E, "the terms n = 11..48 and the n = 49 tail are removed. Effect:",
        "the terms n = 11..48 and the n = 49 tail are removed, and the pole test mu^+ x^+ < 1, which belongs to the tail, is removed with it. Effect:", tag='E5a')
E = rep(E, "Variants that would not fire: a cut at 10 with the crude head, or a cut at 48 with any head, leave both reads NOT_MET.",
        "Variants that would not fire: a cut at 10 with the crude head, or a cut at 48 with any head, leave both reads NOT_MET. "
        "A variant that keeps the pole test would not fire at C04 either: both guard reads stay NOT_MET by the pole, and the head-only S makes "
        "the refined C_0 read MET at 0.02076, so the run would pass the C04 guard and fail at a later row, C06's NOT_MET at 0.02076 among them.", tag='E5b')
E = rep(E, "The change: the norm routine sets #Y to the number of links of Y at position 1 (the links that carry V in the line gauge (1,V)) in place of all links of Y.",
        "The change: the fine-norm routine sets #Y to the number of links of Y at position 1 (the links that carry V in the line gauge (1,V)) "
        "in place of all links of Y. The coarse norm keeps #Y'' = 4 for the output Y = boundary of P''.", tag='E6a')
E = rep(E, "leaves #Y'' = 4 on C10's input and would not fire.",
        "leaves #Y'' = 4 on C10's input and would not fire. A variant that also counts the coarse Y by its links at position 1 for the next blocking "
        "(0, 1 or 2 per coarse plaquette) reads the coarse norm 6|s|(e^{kappa} + e^{2kappa}) and the ratio (e^{-3kappa} + e^{-2kappa})/2 "
        "in [0.5394486, 0.5394487] at kappa = 1/4. That is not 1, and not e^{-1}, so that variant would still fire at C10.", tag='E6b')
E = rep(E, "3. The manifest check: sha256sum -c over reviews/ym4-04c-prediction/ against the three manifests.",
        "3. The manifest check: cd reviews/ym4-04c-prediction && sha256sum -c MANIFEST-ym4-04c-scratch.sha256 MANIFEST-ym4c-v2-checks.sha256 "
        "MANIFEST-ym4c-pkg.sha256. Each manifest line is a sha256, two spaces and a path relative to reviews/ym4-04c-prediction/, so no column swap is needed.",
        tag='E7')

# ============================== the ledger ==============================
G = ledger
G = rep(G, "| REPORTED, relied on by G1 (Theorem 4.9), not reproved; for G0 a cross-reference only, since Proposition 3.18 proves the bound G0 uses | Commun. Math. Phys. 103 (1986) 491-498 | G1. Its text was not re-read in this session.",
        "| REPORTED, a cross-reference only for G0 and G1: Proposition 3.18 proves the bounds both use, G1 through Theorem 4.9 and Corollary 4.10 (note §4.5); "
        "the REPORTED input they share is the exponential formula for connected graphs (Lemma 3.15) | Commun. Math. Phys. 103 (1986) 491-498 | none.", tag='G1')
G = rep(G, "KP per-polymer corollary with alpha = t and theta = kappa", "the per-polymer corollary from Proposition 3.18 with alpha = t and theta = kappa", tag='G2')
G = rep(G, "(a Riemann sum, proved in note §10); corner halves per step |",
        "(a Riemann sum, proved in note §10); the corner obeys 2^k r_k = 15/14, 25823/24660 and [1.0196247, 1.0196248] at k = 1, 2, 3 |", tag='G3')
G = rep(G, "DERIVED; (b) cross-read by exact inertia before the freeze", "DERIVED; (b), and (a) in the k' = 0 sector, cross-read by exact inertia before the freeze", tag='G4')

# ============================== the note ==============================
N = note
N = rep(N, "**REPORTED:** Finner's inequality, the exponential formula for connected graphs, Weyl's integration formula with Schur orthogonality, the Kotecký–Preiss theorem (for G1), Hoeffding's lemma and Watson's G_3(0).",
        "**REPORTED:** Finner's inequality, the exponential formula for connected graphs (G0, and G1 through Lemma 3.15), Weyl's integration formula with Schur orthogonality, "
        "Hoeffding's lemma and Watson's G_3(0). The Kotecký–Preiss theorem is a cross-reference only: G0 and G1 both rest on Proposition 3.18 (sections 3.6 and 4.5).", tag='N1')
N = rep(N, "against v2's 0.01959.\n\n## 1. Target and why this shape",
        "against v2's 0.01959.\n\n**What changed after the package critic.** The final critic of this package (`ym4c/pkg/critic3/`) found two blocking items "
        "and ten fixes. No predicted value moved. Three clauses tagged prefreeze=NONE had been read before the freeze by the attack lenses: C01's A_c(n) count, "
        "C09's cluster-exclusion read and C10's holonomy reads. They are now CROSS_READ, and so is C10b's moment identity. W06(a) is NONE only in the sectors "
        "other than k′ = 0. C19's `missing_tail` now removes the pole test with the tail, and `one_position_support` acts in the fine-norm routine only. "
        "C07, C12 and C16 read their chains from the certified δ_1. G1 now cites Proposition 3.18 in place of the Kotecký–Preiss theorem (section 4.5). "
        "The manifests are regenerated so that `sha256sum -c` reads them (section 13). Sections 4.15 to 4.17 are marked superseded.\n\n"
        "## 1. Target and why this shape", tag='N2')
N = rep(N, "This step closes the gate only at strong coupling. With the C03 counts, the self-map holds for β_0 ≤ 0.02074 on the 10⁻⁵ grid. That is C14's edge, a CONJECTURE on C03 and CONDITIONAL on G0 and G1. β_0 = 0.02075 is outside: C14 predicts the self-map NOT_MET there for every count vector. Inside the window the certified flow runs to the trivial fixed point, Haar measure.",
        "This step would close the gate at strong coupling only, and only once gate G_attack is filed. With the C03 counts, the self-map holds for "
        "β_0 ≤ 0.02074 on the 10⁻⁵ grid. That is C14's edge, a CONJECTURE on C03 and CONDITIONAL on G0 and G1. β_0 = 0.02075 is outside: C14 predicts "
        "the self-map NOT_MET there for every count vector. With the crude counts, which are proved valid (Corollary 3.12), the window is β_0 ≤ 0.01767 "
        "(C13's edge, CONDITIONAL on G0 and G1; TG, fallback 0.01761). Inside the window the certified flow runs to the trivial fixed point, Haar measure.", tag='N3')
N = rep(N, "> **Assembly note (not part of the canonical text).** Sections 3 and 4 are the canonical repaired sections, verbatim except for file paths, which now name the committed copies under `reviews/ym4-04c-prediction/`.",
        "> **Assembly note (not part of the canonical text).** Sections 3 and 4 are the canonical repaired sections (`ym4c/pkg/repair/G0.md` and "
        "`ym4c/pkg/repair/G1.md`), verbatim except for file paths, which now name the committed copies under `reviews/ym4-04c-prediction/`. "
        "Section 4 also carries the changes of the package critic's fix 8, which its assembly note names.", tag='N4')
N = rep(N, "This section's own G1 values stand: c_fin and its flat range, δ_crit, the C10b and C10c slacks, and the fallback.",
        "This section's own G1 values stand: c_fin and its flat range, δ_crit, the C10b and C10c slacks, and the fallback.\n>\n"
        "> **Superseded: sections 4.15 to 4.17.** Section 6 and the prediction file supersede them. They are kept as the record of the repair. "
        "Sections 4.15 and 4.17 give factor-12 values: the edges 0.02040/0.02041 and 0.01595/0.01596, C11's c_fin ∈ [0.6374716724, 0.6376442579], "
        "and C19's surrogate range 0.01366–0.01595. With the factor 6 the edges are 0.02074/0.02075 and 0.01767/0.01768, C11's c_fin is e^{−1}, "
        "and the surrogate range is 0.01553–0.01767. Section 4.16 item 1 says that the edge rows read their pairs as two certified points until G0 proves "
        "monotonicity in β_0. Lemma 3.32 proves it. Section 4.16 item 3 lists C11's c value, the C13 and C14 edges and the regime clause among the values "
        "that depend on the (1 + t)^f step. With the factor 6, C11's c_fin is e^{−1}, and the C14 and regime edge 0.02074/0.02075 is the same under the "
        "fallback. The list that stands is the G_attack row's: δ_crit, C13's c_fin values above 0.078733761 and its crude edge, the scope row's crude "
        "window, and the upper end of C19's surrogate range.\n>\n"
        "> **Changed after the package critic (fix 8).** Theorem 4.9 is now derived from Proposition 3.18 and Lemma 3.15 of section 3. It was the "
        "Kotecký–Preiss theorem, REPORTED. The status paragraph, section 4.5, Lemma 4.13 item 4, the proof of Proposition 4.14, the opening of section 4.16 "
        "and the references change with it. Each change is marked **[CHANGED after the package critic]**. The rest of this section equals "
        "`ym4c/pkg/repair/G1.md` apart from paths and the three marks of superseded sections.", tag='N5')
for head, mark in (
        ("### 4.15 What changes in the rows\n\n",
         "> **Superseded (assembly note, not part of the canonical text).** Section 6 and the prediction file supersede this section. "
         "The section 4 assembly note names its stale values.\n\n"),
        ("### 4.16 OPEN and CONDITIONAL\n\n",
         "> **Superseded in part (assembly note, not part of the canonical text).** Section 6, the prediction file and the G_attack row supersede "
         "items 1 and 3. Items 2, 4, 5 and 6 still hold. The opening paragraph carries fix 8.\n\n"),
        ("### 4.17 The final constants table\n\n",
         "> **Superseded (assembly note, not part of the canonical text).** Section 6 and the prediction file supersede the factor-12 entries of this "
         "table. The section 4 assembly note names them.\n\n")):
    N = rep(N, head, head + mark, tag='N6')
N = rep(N, "REPORTED: the Kotecký–Preiss theorem (Theorem 4.9).",
        "Theorem 4.9 is DERIVED from Proposition 3.18 and Lemma 3.15 of section 3, and Kotecký and Preiss (1986) is a cross-reference "
        "**[CHANGED after the package critic: Theorem 4.9 was the Kotecký–Preiss theorem, REPORTED]**.", tag='N7')
N = rep(N, "### 4.5 Kotecký–Preiss, and the per-polymer corollary", "### 4.5 The cluster bounds, and the per-polymer corollary", tag='N8')
NEW45 = r"""**Theorem 4.9 (the cluster bounds, DERIVED from Proposition 3.18) [CHANGED after the package critic: this was the Kotecký–Preiss theorem, REPORTED].** Let 𝒫 be a finite set. Let each Γ ∈ 𝒫 carry a finite nonempty set off(Γ), and put Γ ≁ Γ′ iff off(Γ) ∩ off(Γ′) ≠ ∅. Let ω: 𝒫 → [0, ∞), d: 𝒫 → [0, ∞), α > 0 and a(Γ) := α#off(Γ). Suppose that for every w

```text
(KP_w)   sum_{Gamma : w in off(Gamma)}  omega(Gamma) e^{a(Gamma) + d(Gamma)}  <=  alpha.
```

Let z: 𝒫 → ℝ with |z| ≤ ω. Then Σ_X |Φ(X; z)|e^{d(X)} < ∞, Ξ(z) > 0, and log Ξ(z) = Σ_X Φ(X; z), an absolutely convergent real series.

*Proof.* This is the abstract setting of section 3.6, with the elements Γ, their sets off(Γ) and the weight ω_d(Γ) := ω(Γ)e^{d(Γ)}. (KP_w) is the hypothesis of Proposition 3.18 for ω_d. A multiset X with multiplicities m_X(Γ) and n members in all is realized by n!/Π_Γ m_X(Γ)! sequences in 𝒫ⁿ. They share one φ^T, since φ^T depends only on the incompatibility graph. So φ(X) = φ^T/Π_Γ m_X(Γ)!, and Π_i ω_d(Γ_i) = Π_Γ ω(Γ)^{m_X(Γ)} e^{d(X)}. Hence Σ_X |Φ(X; z)|e^{d(X)} equals Σ_{n≥1} (1/n!) Σ_{X∈𝒫ⁿ} |φ^T(X)| Π_i |z(Γ_i)|e^{d(Γ_i)}. Every off(Γ) is nonempty, so Proposition 3.18 item 3, summed over the finitely many w, bounds this by α times their number. The argument of Lemma 3.20 then applies word for word. The series L(ζ) of Lemma 3.15 converges absolutely on the polydisc |ζ| ≤ ω, so exp L(ζ) does too, and Lemma 3.15 gives exp L(ζ) = Ξ(ζ) as values. For real z, L(z) is real, so Ξ(z) = e^{L(z)} > 0 and log Ξ(z) = L(z) = Σ_X Φ(X; z). ∎

Kotecký and Preiss (1986) is a cross-reference. Their hypothesis, for every Γ ∈ 𝒫,

```text
(KP)   sum_{Gamma' ~/~ Gamma} |z(Gamma')| e^{a(Gamma') + d(Gamma')}  <=  a(Gamma),
```

follows from (KP_w) by the union bound over off(Γ) (Lemma 4.13 item 4). Their conclusion, Σ_{X≁Γ} |Φ(X; z)|e^{d(X)} ≤ a(Γ), gives the bounds below with the same constant α. G1 uses (KP_w) and Proposition 3.18 only.

**Corollary 4.10 (the per-polymer corollary, DERIVED from Proposition 3.18) [CHANGED after the package critic: it was derived from the REPORTED theorem].** Assume (KP_w) and let |z| ≤ ω. For every Γ ∈ 𝒫:

```text
(a)   sum_{X containing Gamma} |Phi(X;z)| e^{d(X)}                    <=  |z(Gamma)| e^{a(Gamma) + d(Gamma)},
(b)   sum_{X containing Gamma, X != {Gamma}} |Phi(X;z)| e^{d(X)}      <=  |z(Gamma)| e^{d(Gamma)} ( e^{a(Gamma)} - 1 ).
```

*Proof.* (a) Apply Proposition 3.18 item 2 to the weight ω_d, with Γ_0 := {Γ} and ω′ := |z|e^{d} ≤ ω_d. The sequences with some Γ_i = Γ are exactly the realizations of the multisets X ∋ Γ. So, as in the proof of Theorem 4.9, the left side of item 2 is Σ_{X∋Γ} |Φ(X; z)|e^{d(X)}, and its right side is ω′(Γ)e^{α#off(Γ)} = |z(Γ)|e^{a(Γ)+d(Γ)}. (b) The cluster {Γ} enters (a) with |z(Γ)|e^{d(Γ)}. Subtract it. ∎

"""
N = between(N, "**Theorem 4.9 (Kotecký and Preiss 1986, REPORTED).**", "The left side carries e^{d(X)}, not e^{d(Γ)}", NEW45, tag='N9')
N = rep(N, "4. (KP) holds on the set of polymers, for the activity ω(Γ), and for z_Γ(V) at every V.",
        "4. (KP_w) of Theorem 4.9 holds at every off link w, with α = δ′ and the weight ω(Γ): Σ_{Γ : w ∈ off(Γ)} ω(Γ)e^{a(Γ)+d(Γ)} ≤ δ′. "
        "Since |z_Γ(V)| ≤ ω(Γ), Theorem 4.9 and Corollary 4.10 apply to z(V) at every V. The Kotecký–Preiss form (KP) of section 4.5 holds too "
        "**[CHANGED after the package critic: (KP_w) is added, and G1 uses it in place of (KP)]**.", tag='N10a')
N = rep(N, "4. Every Γ′ ≁ Γ holds some e ∈ off(Γ). By item 3 the left side of (KP) is at most Σ_{e∈off(Γ)} T(e) ≤ δ′#off(Γ) = a(Γ). And a(Γ) ≥ δ′ > 0. Lemma 4.8 item 1 passes (KP) to z_Γ(V). ∎",
        "4. By item 3 the left side of (KP_w) is at most T(w), and T(w) ≤ δ′ by item 2. Every Γ′ ≁ Γ holds some e ∈ off(Γ), so the left side of (KP) "
        "is at most Σ_{e∈off(Γ)} T(e) ≤ δ′#off(Γ) = a(Γ), and a(Γ) ≥ δ′ > 0. Lemma 4.8 item 1 gives |z_Γ(V)| ≤ ω(Γ). ∎", tag='N10b')
N = rep(N, "Lemma 4.13 gives (KP) at every V. Theorem 4.9 gives log Ξ(V) = Σ_X Φ(X; V), real.",
        "Lemma 4.13 item 4 gives (KP_w) for the weight ω ≥ |z(V)|. Theorem 4.9 gives log Ξ(V) = Σ_X Φ(X; V), real, and its Ξ(V) > 0 agrees with "
        "Lemma 4.7 **[CHANGED after the package critic: through Proposition 3.18]**.", tag='N11')
N = rep(N, "No step of Theorem G1 is OPEN. It rests on Theorem 4.9, REPORTED from Kotecký and Preiss (1986). The paper's text was not re-read in this session. The rest is DERIVED here or in YM4-03 and YM4-03C.",
        "No step of Theorem G1 is OPEN. Its cluster bounds, Theorem 4.9 and Corollary 4.10, rest on Proposition 3.18 and Lemma 3.15 of section 3. "
        "So its one REPORTED input is the exponential formula for connected graphs, which G0 also uses. Kotecký and Preiss (1986) is a cross-reference. "
        "The rest is DERIVED here or in YM4-03 and YM4-03C **[CHANGED after the package critic: G1 rested on the REPORTED Kotecký–Preiss theorem, "
        "whose text was not re-read in this session]**.", tag='N12')
N = rep(N, "- R. Kotecký and D. Preiss, Cluster expansion for abstract polymer models, Comm. Math. Phys. 103 (1986) 491–498. REPORTED.",
        "- R. Kotecký and D. Preiss, Cluster expansion for abstract polymer models, Comm. Math. Phys. 103 (1986) 491–498. Cross-reference "
        "**[CHANGED after the package critic: it was REPORTED]**.", tag='N13')
N = rep(N, "e^{−1} ∈ [0.3678794, 0.3678795]. Every δ_1 in the table lies below 0.077320139, so the fallback gives the same factor. The crude C_0 is NOT_MET at 1/50 (C05, C12).",
        "e^{−1} ∈ [0.3678794, 0.3678795]. Every δ_1 in the table lies below 0.077320139, so the fallback gives the same factor. The crude C_0 is NOT_MET at "
        "1/50 (C05, C12). Each chain is read from the certified δ_1⁺, not from the upper end of its δ_1 bracket. C12's Σ_k δ_k ≤ 5.7463e-2 holds at the "
        "certified δ_1 ∈ [0.0363235365, 0.0363235366] and fails at the bracket end 0.0363236. C16's δ_20 ≤ 3.0940e-11 holds at C07's certified δ_1 and fails "
        "at 0.0055223. The other chains hold at their bracket ends too (`ym4c/pkg/final-fixes/fix_checks.out`).", tag='N14')
# section 11: ledger table
N = rep(N, "| REPORTED, relied on by G1 (Theorem 4.9), not reproved; for G0 a cross-reference only, since Proposition 3.18 proves the bound G0 uses | Commun. Math. Phys. 103 (1986) 491-498 | G1. Its text was not re-read in this session. |",
        "| REPORTED, a cross-reference only for G0 and G1: Proposition 3.18 proves the bounds both use, G1 through Theorem 4.9 and Corollary 4.10 (§4.5); "
        "the REPORTED input they share is the exponential formula for connected graphs (Lemma 3.15) | Commun. Math. Phys. 103 (1986) 491-498 | none. |", tag='N15a')
N = rep(N, "KP per-polymer corollary with alpha = t and theta = kappa", "the per-polymer corollary from Proposition 3.18 with alpha = t and theta = kappa", tag='N15b')
N = rep(N, "(a Riemann sum, proved in note §10); corner halves per step |",
        "(a Riemann sum, proved in note §10); the corner obeys 2^k r_k = 15/14, 25823/24660 and [1.0196247, 1.0196248] at k = 1, 2, 3 |", tag='N15c')
N = rep(N, "DERIVED; (b) cross-read by exact inertia before the freeze", "DERIVED; (b), and (a) in the k' = 0 sector, cross-read by exact inertia before the freeze", tag='N15d')
N = rep(N, "## 11. The theorem dependency ledger\n\n", "## 11. The theorem dependency ledger\n\nIt is also filed as `reviews/ym4-04c-prediction/ledger_rows.txt`.\n\n", tag='N15e')
# section 12: the engine plan, kept equal to engine_plan.txt
N = rep(N, "It is also filed as `engine_plan-final.txt`.", "It is also filed as `reviews/ym4-04c-prediction/engine_plan.txt`.", tag='N16')
assert plan.endswith('\n')
N = between(N, "```text\nENGINE PLAN, final", "\n```\n\n## 13. Pre-freeze disclosure", "```text\n" + E[:-1], tag='N17')
# section 13
NEW13 = """| Manifest | lines | covers | sha256 |
|---|---|---|---|
| `MANIFEST-ym4-04c-scratch.sha256` | @@N_SCRATCH@@ | every file of the design-lane tree `ym4-04c/`, except bytecode caches | `@@SHA_SCRATCH@@` |
| `MANIFEST-ym4c-v2-checks.sha256` | @@N_V2@@ | every file of `ym4c/pkg/v2-checks/` | `@@SHA_V2@@` |
| `MANIFEST-ym4c-pkg.sha256` | @@N_PKG@@ | every file of the package tree `ym4c/`, except bytecode caches, the workflow's state file `ym4c/pkg-wf.json`, which the workflow rewrites, and `ym4c/final/`, which holds this commit's deliverables. It covers the package critic's scripts in `pkg/critic3/`, this pass's `pkg/final-fixes/`, and the pre-critic package in `pkg/` as the package critic read it, its three path-first manifests included | `@@SHA_PKG@@` |

Each line is a sha256, two spaces and a path relative to `reviews/ym4-04c-prediction/` (in scratch, relative to the scratchpad directory). So `cd reviews/ym4-04c-prediction && sha256sum -c MANIFEST-ym4-04c-scratch.sha256 MANIFEST-ym4c-v2-checks.sha256 MANIFEST-ym4c-pkg.sha256` verifies all three. It did in scratch as of this note: @@N_SCRATCH@@, @@N_V2@@ and @@N_PKG@@ files OK. The pre-critic manifests in `ym4c/pkg/` put the path first, so `sha256sum -c` cannot read them. They are kept as records only. The design-lane tree is unchanged since the v2 repair, so its file list is the one v2 cited, now hash-first.

"""
N = between(N, "| Manifest | lines | covers | sha256 |", "**The lanes, by directory.**", NEW13, tag='N18a')
N = rep(N, "- The freeze checks: `derive_checks.py` (section 14).\n",
        "- The package critic's checks: `ym4c/pkg/critic3/` (`spot.py`, `kp.py`, `g1.py`, `wlane.py`, `c09.py`), in Fractions with outward rounding, with "
        "`wlane.py` in exact ℚ(√2); floats appear in display only. Only `derive_checks_rerun.out` is saved as output. They re-read values already tagged "
        "COMPUTED or CROSS_READ and read no NONE clause.\n"
        "- This pass: `ym4c/pkg/final-fixes/fix_checks.py` with `fix_checks.out`, in Fractions with 256-bit outward rounding through the helpers of "
        "`final_s_lane.py`. It reads the chains of C07, C08, C11, C12, C14 and C16 at the certified δ_1 and at the bracket ends, the `missing_tail` guard "
        "with and without the pole test, the `one_position_support` variant on the coarse norm, and W01's 2^k r_k. `build_final.py` applies the package "
        "critic's findings to the pre-critic package, writes this commit's deliverables and the three manifests, and computes the pin.\n"
        "- The freeze checks: `derive_checks.py` (section 14).\n", tag='N18b')
N = rep(N, "C01's census was read by `polymer-norm/geometry_check.py`, the judge prototype and the counting lens. W06(b) was read by exact inertia.",
        "C01's census was read by `polymer-norm/geometry_check.py`, the judge prototype and the counting lens. C01's A_c(n) clause was read by the counting "
        "lens, `ym4c/pkg/attack/G0-count-checks.py`, for every class through n = 6 on fine (ℤ/8)⁴, and by `ym4c/pkg/derive/G0-b-checks.py` through n = 4. "
        "C09's cluster exclusion was read by the same lens: through n = 8 the closed sets holding all 8 line links of a coarse plaquette are {4: 1, 8: 16}. "
        "C10's holonomy reads were read by `ym4c/pkg/attack/G1-channel-instances.py` at 4 random rational configurations, and C10b's moment identity by the "
        "same script at 6 rational (A, B). W06(b), and W06(a) in the k′ = 0 sector, were read by exact inertia.", tag='N18c')
N = rep(N, "They are row C18 and the clauses: C01's A_c(n) count, C09's cluster-exclusion read, C10's holonomy reads, C10c's moment reads, C19's engine exits, W06(a) and W07's random tiles. C10b's moment identity is COMPUTED, since `derive_checks.py` reads it at one rational configuration.",
        "They are row C18 and the clauses: C10c's moment reads, C19's engine exits, W06(a) in the sectors other than k′ = 0, and W07's random tiles. "
        "C01's A_c(n) count, C09's cluster-exclusion read and C10's holonomy reads were tagged NONE in the pre-critic package. The attack lenses read them "
        "before this freeze, so they are CROSS_READ. C10b's moment identity is CROSS_READ too: `G1-channel-instances.py` read it at 6 rational (A, B), and "
        "`derive_checks.py` reads it at one.", tag='N18d')
N = rep(N, "Since λ now names λ(δ), W02's direction index and W06's eigenvalue variable are renamed ρ and y.",
        "Since λ now names λ(δ), W02's direction index and W06's eigenvalue variable are renamed ρ and y. After the package critic, no predicted value "
        "moved. Three NONE clauses and C10b's moment identity became CROSS_READ, W06(a)'s NONE was scoped, C19's `missing_tail` and "
        "`one_position_support` were specified exactly, the chain method of C07, C12 and C16 was stated, G1 cites Proposition 3.18, and the manifests "
        "were regenerated.", tag='N18e')
N = rep(N, "The 41 rows of the prediction file hash to `f77c51568fdf9eaec81010d7f6cff12811ac2da65be56cd7cd3a74e37518ad61` by",
        "The 41 rows of the prediction file hash to `@@PIN@@` by", tag='N19')
N = rep(N, "10. Are the proved constants exactly the ones in the prediction file: the scalar inequality, δ_1 = 6α e^{−4(θ−κ)}, T = (8489/10000)·6α e^{−8θ}, λ(δ) ≤ κ and c_fin(δ)?",
        "10. Are the proved constants exactly the ones in the prediction file: the scalar inequality, δ_1 = 6α e^{−4(θ−κ)}, T = (8489/10000)·6α e^{−8θ}, λ(δ) ≤ κ and c_fin(δ)?\n"
        "11. Do Proposition 3.18 and Lemma 3.15 give Theorem 4.9 and Corollary 4.10 of G1 from Lemma 4.13 item 4, so that G1 needs no Kotecký–Preiss input (section 4.5)?",
        tag='N20')

# ============================== the manifests ==============================
def listing(root_rel, exclude):
    root = os.path.join(SCRATCH, root_rel)
    out = []
    for dp, dns, fns in os.walk(root):
        dns[:] = sorted(d for d in dns if d != '__pycache__' and not exclude(os.path.relpath(os.path.join(dp, d), SCRATCH) + '/'))
        for fn in fns:
            rel = os.path.relpath(os.path.join(dp, fn), SCRATCH)
            if exclude(rel) or fn.endswith('.pyc'):
                continue
            assert not os.path.islink(os.path.join(dp, fn)), rel
            assert all(c not in rel for c in ' \\\n'), rel
            out.append(rel)
    return sorted(out)


def manifest(paths):
    return ''.join('%s  %s\n' % (sha_file(os.path.join(SCRATCH, p)), p) for p in paths)


m_scratch = manifest(listing('ym4-04c', lambda r: False))
m_v2 = manifest(listing('ym4c/pkg/v2-checks', lambda r: False))
m_pkg = manifest(listing('ym4c', lambda r: r == 'ym4c/pkg-wf.json' or r.startswith('ym4c/final/')))
assert 'ym4c/pkg/critic3/spot.py' in m_pkg and 'ym4c/pkg/final-fixes/build_final.py' in m_pkg and 'ym4c/final/' not in m_pkg
MAN = {'MANIFEST-ym4-04c-scratch.sha256': m_scratch, 'MANIFEST-ym4c-v2-checks.sha256': m_v2, 'MANIFEST-ym4c-pkg.sha256': m_pkg}
for name, text in MAN.items():
    write(os.path.join(REV, name), text)
FILL = {
    '@@N_SCRATCH@@': str(m_scratch.count('\n')), '@@SHA_SCRATCH@@': sha_bytes(m_scratch.encode()),
    '@@N_V2@@': str(m_v2.count('\n')), '@@SHA_V2@@': sha_bytes(m_v2.encode()),
    '@@N_PKG@@': str(m_pkg.count('\n')), '@@SHA_PKG@@': sha_bytes(m_pkg.encode()),
}


def fill(text):
    for k, v in FILL.items():
        text = text.replace(k, v)
    return text


P, E, N = fill(P), fill(E), fill(N)
lines = P.split('\n')
assert P.endswith('\n') and len(lines) == 42 and lines[-1] == ''
PIN = sha_bytes(('\n'.join(lines[:41]) + '\n').encode())
N = N.replace('@@PIN@@', PIN)
for name, text in (('prediction', P), ('note', N), ('plan', E), ('ledger', G)):
    assert '@@' not in text, name

# ============================== checks of the written files ==============================
for k, l in enumerate(lines[:41], 1):
    assert ' ' not in l and l.endswith('|json=0'), ('row format', k)
    assert all('=' in f for f in l.split('|')[1:]), ('field without key', k)
    for bad in ('NAMED', 'O(', '~', 'final critic', 'engine_plan-final', 'ledger_rows-final'):
        assert bad not in l, ('forbidden text', bad, k)
assert sum(1 for l in lines if l.startswith('PREDICT|')) == 28
block = N.split("```text\nENGINE PLAN, final", 1)[1].split("\n```\n\n## 13.", 1)[0]
assert "ENGINE PLAN, final" + block + "\n" == E, 'note section 12 differs from engine_plan.txt'
assert 'engine_plan-final' not in N and 'ledger_rows-final' not in N

write(os.path.join(DOCS, PRED_NAME), P)
write(os.path.join(DOCS, NOTE_NAME), N)
write(os.path.join(REV, 'engine_plan.txt'), E)
write(os.path.join(REV, 'ledger_rows.txt'), G)
write(os.path.join(REV, 'derive_checks.py'), dchk)
assert sha_file(os.path.join(REV, 'derive_checks.py')) == sha_file(os.path.join(PKG, 'derive_checks.py'))
run = subprocess.run([sys.executable, '-I', '-B', os.path.join(REV, 'derive_checks.py')], capture_output=True, cwd=REV)
assert run.returncode == 0, run.stderr
write(os.path.join(REV, 'DERIVE-CHECKS.hbp'), run.stdout.decode('utf-8'))
assert run.stdout == open(os.path.join(PKG, 'DERIVE-CHECKS.hbp'), 'rb').read(), 'DERIVE-CHECKS.hbp differs from the pre-critic one'
run2 = subprocess.run([sys.executable, '-I', '-B', os.path.join(REV, 'derive_checks.py')], capture_output=True, cwd=REV)
assert run2.stdout == run.stdout

print('pin (head -n 41 | sha256sum):', PIN)
for name, text in MAN.items():
    print('%s: %d lines, sha256 %s' % (name, text.count('\n'), sha_bytes(text.encode())))
for rel in ('docs/' + PRED_NAME, 'docs/' + NOTE_NAME, 'reviews/ym4-04c-prediction/derive_checks.py',
            'reviews/ym4-04c-prediction/DERIVE-CHECKS.hbp', 'reviews/ym4-04c-prediction/engine_plan.txt',
            'reviews/ym4-04c-prediction/ledger_rows.txt'):
    print('%s  %s' % (sha_file(os.path.join(FINAL, rel)), rel))
print('derive_checks.py: exit 0, output byte-identical to DERIVE-CHECKS.hbp and to the pre-critic copy, twice')
