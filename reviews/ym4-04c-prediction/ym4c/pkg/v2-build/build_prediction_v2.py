#!/usr/bin/env python3
"""Builds PREDICTION-v2.hbp: one row per line, KIND|key=value|...|json=0, spaces written as underscores."""
import sys
OUT = "/tmp/claude-0/-home-user/b2fb539a-cb4d-5f0b-a22f-ca1a7fcb500d/scratchpad/ym4c/pkg/PREDICTION-v2.hbp"
DRAFT_SHA = "dbce1a28ff666f2a6a4706dd34ac7e4e59ab99637d887428525cc1f44f3d6140"
MAN1_SHA = sys.argv[1]; MAN2_SHA = sys.argv[2]
ROWS = []
def row(kind, *kv):
    parts = [kind]
    for k, v in kv:
        assert "|" not in v and "\n" not in v, (k, v)
        if k == "direction":   # the operator's words, byte for byte as in the draft
            parts.append(f"{k}={v}"); continue
        v = ' '.join(v.split())
        for a, b in ((", ", ","), ("; ", ";"), (": ", ":")):
            v = v.replace(a, b)
        parts.append(f"{k}={v.replace(' ', '_')}")
    parts.append("json=0")
    ROWS.append("|".join(parts))

row("YM4_04C_PREDICTION",
 ("written_before_any_engine_code_exists", "1"), ("step", "YM4-04C"),
 ("version", "v2, the draft of 2026-11-09 repaired under the final critic's FIX_FIRST verdict: blocking items 1 to 5 and fixes 1 to 10 applied here; blocking item 6, the derivations of G0 and G1, is carried by note sections 3 and 4 and gate G_attack"),
 ("supersedes", f"the uncommitted scratch draft synth/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp, 40 lines, sha256 {DRAFT_SHA}"),
 ("issue", "4"), ("base", "main_830fd3f"), ("date", "2026-11-09"),
 ("lane", "synthesis of the polymer-norm, small-large-field and coupling-flow design lanes under three judges, repaired after the final critic"),
 ("direction", "For_YM4-04,_I_agree_with_the_prediction-first_approach,_with_a_reachable_falsifier_per_row._The_successful_beta^10_calculation_is_a_strong_input,_but_it_does_not_establish_that_scale-to-scale_control.(operator,2026-11-08)"),
 ("statement_and_definitions", "docs/NOTE-YM4-04C-LOCAL-POLYMER-NORM-20261109.md, written in the freeze commit, with G0 and G1 derived in full in its sections 3 and 4"),
 ("symbols", "the Kotecky-Preiss pair is (alpha,theta): a(gamma)=alpha*#off(gamma), d(gamma)=theta*#gamma, theta in {1/4+i/64}; a is (1/2)Re Tr only; b is the blocking factor only; kappa is the norm weight 1/4 only; the fine lattice spacing is h_0; the W-lane momentum is q, with p=q*e_nu and t_W=tan(q/2); the W-lane small-field parameter is p_SF; the W06 twist is t_tw; the one-loop coupling step per halving is Delta_beta; t is G1's tree-graph parameter and t_n=I_n/I_1 the character ratios; bare mu is 20^20/19^19, and mu, nu as subscripts or polarizations are directions"),
 ("read_rule", "a row reads MET when the engine and the independent check both compute its predicted values; a row with predicts_NOT_MET names a certificate, self-map or hypothesis predicted to fail, and reads MET only when it fails where predicted; a row or clause tagged CONDITIONAL reads UNSUPPORTED when gate G_attack finds an unrepaired gap, or a proved constant that differs from a frozen one, in what it rests on; every failed read stays in this file and the note"),
 ("prefreeze_rule", "prefreeze=CROSS_READ: the engine's own target quantity (an enumeration, a census, an exact inertia, or a float run of the same quantity) was read before this freeze by a prototype; prefreeze=COMPUTED: the frozen value was fixed before this freeze by scratch arithmetic (Fractions or Decimal) of the closed form the row states; prefreeze=NONE: no script computed the value before this freeze; a CROSS_READ or COMPUTED value is a reproduction read, never a confirmed prediction, and is left out of every predictions-confirmed count; only NONE rows and NONE clauses enter that count"),
 ("tags", "DERIVED (proved here or in a cited repo note), CONJECTURE, OPEN, MEASURED (an exact count or integral actually computed), REPORTED (from the literature, with a citation); CONDITIONAL_G0, CONDITIONAL_G1 and CONDITIONAL_G0_G1 mark a row or clause whose frozen values are values of a G0 or G1 formula, or which states an H_k claim through them; role names CONTROL, NEGATIVE_CONTROL, G1_TEST or REPRODUCTION"),
 ("lanes", "S(strong-coupling certificate of H_k=>H_{k+1}, rows C01-C19, C10b and C10c), W(tree-level and Gaussian diagnostics, rows W01-W07, counted nowhere toward H_k=>H_{k+1})"))

row("YM4_04C_HYPOTHESIS",
 ("name", "H_k(kappa,delta_k), the localized polymer norm on the b=2 blocked SU(2) action"),
 ("lattices", "fine Lambda_0=(Z/N)^4, N=2^K*L_K, L_K>=4, spacing h_0; scale-k lattice Lambda_k=(Z/(N/2^k))^4, spacing 2^k*h_0"),
 ("map", "k applications of the YM4-03 line map at b=2, (BU)_mu(x')=U_mu(2x')U_mu(2x'+e_mu); rho_k=the exact Haar pushforward density, YM4-03 Theorem 4 iterated"),
 ("gauge", "at each step the line gauge (U_0,U_1)=(1,V_l) fixed at the coarse-link midpoint, a computational gauge only: every activity is coarse-gauge invariant and every norm is a sup norm of an invariant function"),
 ("H_0(beta_0)", "rho_0 is the SU(2) Wilson measure w=e^{beta_0*a}, a=(1/2)Re Tr, written as prod_p c_0(beta_0)(1+K_p), K=sum_{n>=2}n*t_n*chi_{(n-1)/2}, t_n=I_n/I_1, c_0(x)=sum_m(x/2)^{2m}/(m!(m+1)!)"),
 ("H_k(kappa,delta_k),k>=1", "log rho_k(V)=const_k+sum_Y R_k(Y;V), Y over finite sets of scale-k links with #Y>=4 that contain a closed loop, each R_k(Y;.) real, coarse-gauge invariant and a function of V restricted to Y; norm_kappa(R_k):=sup_l sum_{Y containing l} e^{kappa*#Y}*sup_V abs(R_k(Y;V))<=delta_k; the coarse Wilson term (beta_k/2)chi_1/2(V_P) is carried inside R_k(boundary of P)"),
 ("function_space", "the Banach space of such families {R(Y)} with finite norm_kappa"),
 ("admissible", "beta_0 with C_0 MET and delta_1<delta_crit^-, where delta_crit:=sup{delta: C_k(delta) MET and c(delta)<1} and delta_crit^- is its lower enclosure on the 10^-9 grid"),
 ("length_scales", "2^k*h_0, k=0..K; last-scale side L_K>=4; the exact counts need fine sides>=8, the Fuss-Catalan tail needs only adjacency degree 20"),
 ("constants", "kappa=1/4; D=20; 6 plaquettes per link (Finner exponent 6); #W(e_0)=12; F_20(n)=C(20n,n)/(19n+1); mu=20^20/19^19 in [53.00068,53.00069]; E_abs(chi_1/2)=8/(3pi)<=8489/10000; n_max=10"),
 ("uniformity", "no bound involves N, K or the number of plaquettes"),
 ("regime", "strong bare coupling, beta_0<=0.01959 on the 10^-5 grid: C14's edge with the C03 counts (CONJECTURE on C03), equivalently delta_1<delta_crit^-; beta_0=0.01960 lies outside, where C14 predicts the self-map NOT_MET; with the crude counts the boundary is beta_0<=0.01369 (C13); inside the window the certified flow runs to the trivial fixed point (Haar, beta=0)"))

row("YM4_04C_CERTIFICATES",
 ("C_0(beta_0)", "eps:=eps_6(beta_0), the L^6(SU(2)) norm of K; x:=eps*e^{2alpha+theta}; S(x):=sum_{n=4..10}N(n)x^n+sum_{n=11..48}6F_20(n)x^n+6F_20(49)x^49/(1-mu*x), defined for mu*x<1; crude: N(n):=6F_20(n); head-free: N(n):=0; refined: N(n):=the C03 counts; C_0 is MET iff for some grid theta there is a rational alpha with S^+(eps^+*e^{2alpha+theta})<=alpha<=1/4"),
 ("NOT_MET_read", "C_0 reads NOT_MET only on a proof that S(eps_6^-*e^{2alpha+1/4})>alpha for every alpha in [0,1/4]: the pole mu*x>=1 at alpha=0, or S^-(x^-(0))>1/4, or the convex tangent bound g^-(alpha_m)-abs(g')^+(alpha_m)*max(alpha_m,1/4-alpha_m)>0 at one rational alpha_m, with g'(alpha)=2x*S'(x)-1; theta=1/4 decides every grid theta, since S(eps*e^{2alpha+theta}) increases in theta (DERIVED)"),
 ("alpha_search", "g(alpha):=S(eps*e^{2alpha+theta})-alpha is convex in alpha (S has nonnegative coefficients); the engine finds its minimum by ternary search over dyadic alpha of denominator 2^48 in [0,1/4] and the least root alpha_- by bisection; the read is the exact inequality at the returned alpha, never a capped fixed-point iteration (C19 iteration_cap_400)"),
 ("outputs", "delta_1:=min over certified (alpha,theta) of 12alpha*e^{-4(theta-kappa)}; readout: c_1/2(P) in 2t_2(beta_0)^4+-T, T:=(8489/10000)*12alpha*e^{-8theta} minimized over certified (alpha,theta)"),
 ("C_k(delta_k),k>=1", "delta':=delta_k*e^{delta_k}; in C_k the Kotecky-Preiss pair is alpha=t=delta' and theta=kappa; MET iff 2delta'<=kappa/2; output delta_{k+1}<=c(delta_k)*delta_k, c(delta):=e^delta*[e^{-4kappa}+max_{n>=4}(e^{-(kappa/2-2delta')n}-e^{-kappa*n/2})]"),
 ("self_map", "MET iff C_k MET and c(delta_k)<1; then delta_{k+j}<=c(delta_k)^j*delta_k for every j and sum_k delta_k<=delta_k/(1-c(delta_k)), since c is increasing in delta"),
 ("grids", "theta in {1/4+i/64: 0<=i<=320}; beta on the 10^-5 grid; delta_crit^- on the 10^-9 grid; alpha on dyadics of denominator 2^48; upward rounding to 160 significant bits"),
 ("status", "the scalar inequality S(eps_6*e^{2alpha+theta})<=alpha with the 6F_20(n) counts, delta_1, T, the C_k test and c(delta) are the outputs G0 and G1 must prove with exactly these constants (gate G_attack)"))

row("YM4_04C_THEOREMS",
 ("G0", "step 0: YM4-03C Lemmas A and B; Finner's inequality with exponent 6, sup_V abs(z_gamma)<=eps_6^{#gamma}; the Kotecky-Preiss criterion with a(gamma)=alpha*#off(gamma)<=2alpha*#gamma, d(gamma)=theta*#gamma and the test set W(e_0); the BFS injection into the complete 20-ary tree and the Fuss-Catalan tail; gives #Y''(gamma)<=#gamma and V-dependence only at size>=4, hence C_0=>H_1 with delta_1"),
 ("G1", "step k: Y-objects in L^infinity; Lemma A; the tree-graph bound sum_{Gamma containing e} prod omega<=t, from sum_{o containing e} omega_o*e^{t*s(o)}<=t, with t=delta'; the Kotecky-Preiss per-polymer corollary sum_{clusters containing gamma} abs(Phi)e^{d(gamma)}<=abs(z_gamma)e^{a(gamma)+d(gamma)} with alpha=t and theta=kappa; gives an exact line channel (factor e^{-kappa*#Y/2}<=e^{-4kappa}) plus a multi-object term, hence C_k=>H_{k+1} with c(delta)"),
 ("status", "both TO_BE_DERIVED in note sections 3 and 4, in the same commit as these rows and before any engine code; each derivation ends with an explicit check that the proved constants are exactly the frozen ones of the certificates row; a second seat attacks both under gate G_attack"),
 ("ties_to_exact_data", "C09 (G0, low power); C10 (any valid G1, from below); C10b (G1's multi-object channel, slack 3x10^4); C10c (G1's single-object channel through off links, slack in [7.116,7.118] against the natural decomposition and in [12.08,12.09] against every decomposition at s=1/65536)"))

row("YM4_04C_W_HYPOTHESIS",
 ("name", "H_k^W(M), necessary conditions at tree level and Gaussian level for any weak-coupling induction built on a blocking map M"),
 ("maps", "M=B, the line map and its exact compositions B_{2^k} (B o B=B_4); M=A, the average of b-step transporters over the b^d offsets of a block, defined here only through its abelian linearization"),
 ("coupling", "r_k(p):=lim_{beta->infinity} beta_k(p)/beta, beta_k(p):=4*H_{log rho_k}(X_p)/sum_P phi_P(X_p)^2, X_p the abelian sigma_3 coarse plane wave of momentum p=q*e_nu with polarization perpendicular to p, phat^2:=4sin^2(q/2); slope A_k:=lim_{q->0}(1/r_k(p)-1)/phat^2, an exact limit (in d=3 with r_k replaced by b^{4-d}r_k)"),
 ("conditions", "(i) classical marginality, r_k(p)->1 as q->0; (ii) the irrelevant part bounded uniformly in k, sup_p abs(1/r_k(p)-1)/phat^2<=C with C independent of k; (iii) a plaquette small-field condition 1-a(V_P)<=2p_SF^2/beta_k with k-independent p_SF keeps a k-independent Gaussian large-field probability; (iv) the small-field threshold and a fine large-field bound pass one step without loss"),
 ("status", "these rows test necessary conditions only; no W row tests or promotes H_k=>H_{k+1}"))

row("YM4_04C_SCOPE",
 ("scope", "finite periodic 4D tori, fine sides>=8 for the exact counts, last-scale sides>=4, d=4, b=2, kappa=1/4; W lane on the lattices named in each row"),
 ("S_MET_means", "an exact rational inequality chain closes, or an exact enumeration or integral reads the predicted value; it means H_k=>H_{k+1} only through G0 and G1"),
 ("NOT_MET_above_the_windows", "a failure of this norm with these counts, set by the 6F_20(n) tail beyond the head: Fuss-Catalan growth mu in [53.00068,53.00069] per plaquette, against closed-set growth (N(10)/N(8))^{1/2}=(19/2)^{1/2} in [3.08,3.09] and (N(12)/N(10))^{1/2}=(1163/152)^{1/2} in [2.76,2.77] per plaquette (CONJECTURE on C03); not evidence of a phase transition, a vanishing gap or anything about the theory"),
 ("windows", "beta_ind^crude in [0.01369,0.01370), beta_crude in [0.01904,0.01905), beta_ind in [0.01959,0.01960), beta_stop in [0.02075,0.02076), beta_wall(1/4) in [0.02247,0.02248]; all below the YM4-04B Dobrushin reach 1/18, and below 9 percent of one one-loop step Delta_beta=(11/(3pi^2))ln2 in [0.2575118,0.2575119] per halving of the spacing"),
 ("not_claimed", "a renormalized trajectory with beta(h_0)->infinity as h_0->0; relevant counterterms (the certified plaquette coupling is irrelevant-like: its leading term 2*beta^4/128=beta^4/64 comes from the MEASURED series P_10); the crossover from beta_0 near 0.02 to the scaling region; Balaban's small-field and large-field estimates; an averaging map for SU(2); the coupling recursion or asymptotic freedom; a continuum or infrared limit; OS reconstruction; a mass gap; that the true contraction equals the certified one; that the certified class says anything about UV completeness of the theory; anything for other kappa, b or d"),
 ("OPEN_gates_not_promoted_by_any_row", "YM4-04 weak coupling, YM4-05, YM4-06"))

row("YM4_04C_DISCLOSURE",
 ("prefreeze_checks", "the numbers of this file were fixed by scratch scripts that are not engines and not evidence, listed below by directory under scratchpad/ym4-04c/ and scratchpad/ym4c/pkg/v2-checks/"),
 ("design_lanes", "polymer-norm/{contraction,delta_scan,delta_scan2,delta_scan3,derive_estimates,geometry_check,induction_window,readout,window2,window_scan}.py; smallfield-largefield/{ri,d1_chessboard,d2_fiber_k0,d3_atom,d4_tails,d5_rho,d6_misc}.py; coupling-trajectory/{d1_strong,d2_toy_split,d3_tree,d4_direct_float_sanity,d5_tree_exact,d6_two_d,d7_hessian_chairs,d8_misc,d8b_misc_top16,d9_window}.py"),
 ("judges", "judge-engineer/{closed_sets,ct_2d,kp_check,kp_edges,kp_edges2,slf_ct_sanity}.py and judge-engineer/n12.txt; referee/{check_headfree,check_ind,check_polymer,check_sl_ct}.py; judge-cft/{c05,c09_grid,eps6_exact,spot}.py"),
 ("synthesis", "synth/{verify_core,verify_extra,closed_sets_copy,r12_float_sanity}.py; their outputs synth/{c09,cs8,cs12,ind_crude,ind_free,ind_meas,points,stop_crude,stop_free,stop_meas}.txt; the draft synth/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp"),
 ("final_critic", "final-check/{s_lane,edges,margins,c09,c10b,faults,fault_judge,fault_dl,wlane,wlane_hp}.py, in Decimal at 50 and 90 digits, except wlane.py (floats) and fault_dl.py (window2's Fractions)"),
 ("v2_repair", "v2-checks/{w_lane_exact,kp_exact,c19_iteration_cap,c19_missing_tail_and_x3,c19_one_position,c10c_constants,c10c_brackets,c09_readout_tail}.py with their .out files, in Fractions with 160-bit outward dyadic rounding, floats only in display; they fixed W03's corrected bracket, W01's exact A_3, C19's pinned faults, C10c's constants and C09's P_10-2t_2^4"),
 ("float_runs", "floats enter arithmetic only in coupling-trajectory/d4_direct_float_sanity.py, judge-engineer/slf_ct_sanity.py and synth/r12_float_sanity.py (numpy sanity runs), judge-cft/spot.py and eps6_exact.py (float eps_6 spot checks), referee/check_sl_ct.py and final-check/wlane.py (float alias sums), and polymer-norm/contraction.py and coupling-trajectory/d9_window.py (a float only to choose a scan length or a rounding grid); everywhere else floats appear in display only"),
 ("cross_reads", "C03's counts (judge-engineer/closed_sets.py, rerun through n=10 on both lattices by synth/closed_sets_copy.py); C01's census (polymer-norm/geometry_check.py and the judge prototype); W06(b) (exact inertia, smallfield-largefield/d2_fiber_k0.py); W04 (float runs, so W04 is a reproduction row); these are reproduction reads, not blind predictions"),
 ("corrections_in_v2", "W03's second increment is 6529/60928, outside the draft's [0.10716,0.10717]; the regime boundary is beta_0<=0.01959; C15 is scoped to finite heads with the 6F_20(n) tail; C19's iteration_cap_400, missing_tail and one_position_support are pinned by exact runs; C10c and C01's A_c(n) clause are added; the symbols are renamed"),
 ("manifests", f"scratchpad/ym4c/pkg/MANIFEST-ym4-04c-scratch.sha256: 67 lines of path and sha256, every file of scratchpad/ym4-04c/ except bytecode caches, sha256 {MAN1_SHA}; scratchpad/ym4c/pkg/MANIFEST-ym4c-v2-checks.sha256: 19 lines, every file of scratchpad/ym4c/pkg/v2-checks/, sha256 {MAN2_SHA}; the scratchpad is ephemeral, so the freeze commit carries both manifests and every file they list under reviews/ym4-04c-prediction/"),
 ("engine_obligation", "the engine and the independent check recompute every value by their own routes under the no-float gate"))

row("PREDICT", ("id", "C01"), ("lane", "S"), ("origin", "polymer-norm C01, with the critic's exhaustive count added"),
 ("name", "geometry and counting constants"),
 ("statement", "on fine (Z/8)^4 and (Z/12)^4 with the b=2 lines (a line link has every coordinate other than its direction even): every link lies in 6 plaquettes; every plaquette has 2 or 4 off links; the off-link adjacency graph of fine plaquettes has maximum degree D=20 and minimum degree 10; for every line link e_0 the 6 plaquettes through it hold #W(e_0)=12 distinct off links; every off link lies in 0 or 1 coarse filling; the Lemma-B-closed off-link-connected sets of at most 4 plaquettes are exactly the coarse fillings; A_c(n):=the number of off-link-connected sets of n plaquettes, closed or not, that hold a given off link of class c (c=the number of its odd transverse coordinates); a BFS injection into the complete 20-ary tree gives A_c(n)<=6F_20(n)"),
 ("predicted", "6 plaquettes per link; off links per plaquette in {2,4}; D=20, minimum 10; #W=12 for every line link; on (Z/8)^4: 2048 line links, 6144 off links with one odd transverse coordinate (each in exactly one filling), 6144 with two and 2048 with three (in no filling), so 8192 in no filling and 6144 in one; closed sets of at most 4 plaquettes: the fillings only, none with 3 or fewer; A_c(n)<=6F_20(n) for n=1..5, c=1,2,3, on both lattices, with 6F_20(1..5)=6,120,3540,123240,4705470 and A_c(1)=6, an inequality only, no count frozen; F_20(4..12)=20540,784245,31763004,1340246340,58281448940,2593593086150,117544525178080,5406686759963586,251754316822792420; F_20(n+1)/F_20(n) strictly increasing and below mu, mu in [53.00068,53.00069], for n<=59"),
 ("tag", "DERIVED for the census, the F_20 values and the ratios; the injection inequality A_c(n)<=6F_20(n) rests on G0(c), TO_BE_DERIVED in note section 3: CONDITIONAL_G0 for that clause"),
 ("prefreeze", "CROSS_READ for the census (polymer-norm/geometry_check.py, judge-engineer/closed_sets.py); COMPUTED for F_20 and the ratios (polymer-norm/derive_estimates.py); NONE for the A_c(n) clause"),
 ("method", "integer lattice enumeration with sites, links and plaquettes as coordinate tuples; exhaustive closed-set search up to 4 plaquettes seeded at every off-link class; an exhaustive enumeration of all off-link-connected sets through n=5 grown from the 6 plaquettes through one seed off link per class, with no closure pruning and dedup by canonical form; Fuss-Catalan numbers as exact binomials; ratios compared as exact rationals"),
 ("falsifier", "any count different from the predicted one; a closed set of at most 4 plaquettes that is not a filling; an A_c(n)>6F_20(n) for some n<=5 on either lattice; a C03 count above 6F_20(n); a ratio F_20(n+1)/F_20(n)>=mu"),
 ("reach", "24576 and 124416 plaquettes; the census in seconds; at most 6F_20(5)=4705470 sets per class through n=5 if the inequality holds, minutes"))

row("PREDICT", ("id", "C02"), ("lane", "S"), ("origin", "polymer-norm C02"),
 ("name", "per-plaquette activity in the Finner norm"),
 ("statement", "eps_6(beta):=the L^6(SU(2)) norm of e^{beta*a}/c_0(beta)-1, with eps_6^6=sum_{k=0..6}C(6,k)(-1)^{6-k}c_0(k*beta)/c_0(beta)^k read as rational enclosures; by Finner's inequality every fine polymer gamma has sup_V abs(z_gamma(V))<=eps_6^{#gamma}, since an off link lies in at most 6 plaquettes"),
 ("predicted", "eps_6 in [6.53830e-4,6.53831e-4] at beta=1/1000; [6.538419e-3,6.538420e-3] at 1/100; [1.0216544e-2,1.0216545e-2] at 1/64; [1.3077541e-2,1.3077542e-2] at 1/50; [1.4530846e-2,1.4530847e-2] at 1/45; [1.6347585e-2,1.6347586e-2] at 1/40; [6.5499695e-2,6.5499696e-2] at 1/10; [0.740642074,0.740642075] at 1; [4.29699629,4.29699630] at 4; eps_6/beta->5^{1/6}/2 in [0.65383,0.65384] as beta->0, since E[chi_1/2^6]=5; for comparison sup abs(K)=e^beta/c_0-1 reads 1.0037542e-2 at 1/100, so the L^6 norm is smaller by a factor 0.6514"),
 ("tag", "DERIVED"), ("prefreeze", "COMPUTED (polymer-norm/derive_estimates.py, judge-cft/eps6_exact.py, final-check/s_lane.py)"),
 ("method", "exact rational partial sums of c_0 with geometric tail bounds; interval arithmetic through the alternating binomial sum; bisection for a rational sixth root to 10^-12"),
 ("falsifier", "an engine enclosure disjoint from a predicted one, or eps_6(beta)/beta outside [0.6538,0.6551] at any of the grid couplings<=1/10"),
 ("reach", "closed-form series; all nine enclosures in under a minute in scratch Fractions, reproduced by two judges"))

row("PREDICT", ("id", "C03"), ("lane", "S"), ("origin", "polymer-norm C03, sharpened by the judge-engineer's counts"),
 ("name", "exact closed-set counts and the counting gap"),
 ("statement", "N_c(n):=the number of Lemma-B-closed off-link-connected sets of n fine plaquettes holding a given off link of class c, c=the number of its odd transverse coordinates (1,2,3); N(n):=max_c N_c(n); read for n=4..12 on fine (Z/8)^4 and (Z/12)^4; the certificate uses n<=10, and n=11,12 are a growth readout; counting gap:=6F_20(n)/N(n)"),
 ("predicted", "class 1: N_1(4..12)=1,0,12,0,32,32,304,284,2326; class 2: N_2(4..12)=0,0,12,0,12,12,240,244,1640; class 3: N_3(4..12)=0,0,12,0,0,0,216,228,1242; so N(4..12)=1,0,12,0,32,32,304,284,2326; identical on the two lattices (DERIVED by locality: no set of fewer than 16 plaquettes winds at fine side 8); counting gap in [1.09e10,1.10e10] at n=8, [2.31e12,2.33e12] at n=10, [6.49e14,6.50e14] at n=12; N(10)/N(8)=19/2 and N(12)/N(10)=1163/152 in [7.65,7.66], against F_20(n+2)/F_20(n)>2000"),
 ("tag", "CONJECTURE"),
 ("prefreeze", "CROSS_READ: the judge prototype judge-engineer/closed_sets.py (Python integers) read these counts through n=12 before this freeze (judge-engineer/n12.txt), and synth/closed_sets_copy.py reran them through n=10 on both lattices; the engine's enumeration is separate code and the check's a third"),
 ("method", "closure-driven growth from the 6 plaquettes through a seed off link: a closed set may add any off-link neighbour, an open set must close its lowest open off link; prune when the open links exceed 4x(remaining size); dedup by canonical form under coarse translations x the 384 signed permutations; Fuss-Catalan values exact"),
 ("falsifier", "any count different from its predicted value on either lattice; any difference between the lattices; any N(n)>6F_20(n); a counting gap outside its bracket"),
 ("reach", "about 1s per class at n=10 (77k states) and 17s per class at n=12 (0.97M states) in the Python prototype"))

row("PREDICT", ("id", "C04"), ("lane", "S"), ("origin", "polymer-norm C04, restated for finite heads"),
 ("name", "the wall of the certificate"),
 ("statement", "for theta>=kappa=1/4 and every alpha>=0, x=eps_6*e^{2alpha+theta}>=eps_6*e^{1/4}; since F_20(n+1)/F_20(n) increases to mu (L08), the tail sum_{n>n_max}6F_20(n)x^n diverges whenever mu*x>1; so above the crossing mu*e^{1/4}*eps_6(beta)=1 the certificate fails for every finite head (any n_max>=4 and any counts N(4..n_max)>=0) with the 6F_20(n) tail beyond n_max; the wall belongs to this tail, not to the norm, and a closed-set growth bound below mu would move it (L14, OPEN); locate beta_wall(1/4) and the crossing mu*eps_6=1 (kappa->0) on a 10^-5 grid"),
 ("predicted", "beta_wall(1/4) in [0.02247,0.02248]; mu*eps_6=1 at beta in [0.02885,0.02886]; both below the YM4-04B Dobrushin reach 1/18, and below 0.088 and 0.113 of one one-loop step Delta_beta=(11/(3pi^2))ln2 in [0.2575118,0.2575119] per halving of the spacing; the engine's C04 guard reads the refined C_0 at 1/40 and at 0.02248 before any other row reads C_0, and both read NOT_MET by the pole, since mu*e^{1/4}*eps_6^- is at least 1.1125 at 1/40 and at least 1.00035 at 0.02248"),
 ("predicts_NOT_MET", "C_0 at every beta above beta_wall(1/4), for every alpha, every theta>=1/4 and every finite head with the 6F_20(n) tail beyond n_max"),
 ("tag", "DERIVED (the arithmetic); its meaning as a statement about H_1 runs through G0"), ("role", "NEGATIVE_CONTROL"),
 ("prefreeze", "COMPUTED (polymer-norm/derive_estimates.py, final-check/s_lane.py; the two guard reads by v2-checks/c19_missing_tail_and_x3.py)"),
 ("method", "C02 enclosures on a 10^-5 grid with rational bounds on e^{1/4}, mu, pi and ln2; bisection; the guard reads by the NOT_MET proof of the certificates row"),
 ("falsifier", "the crossing mu*e^{1/4}*eps_6=1 outside [0.02247,0.02248], or mu*eps_6=1 outside [0.02885,0.02886], or any C_0 read MET above beta_wall(1/4), the guard reads included"),
 ("reach", "closed form, about 10^3 enclosure evaluations, minutes"))

row("PREDICT", ("id", "C05"), ("lane", "S"), ("origin", "polymer-norm C05, certificate search repaired"),
 ("name", "the crude one-step window"),
 ("statement", "with N(n):=6F_20(n) for every n>=4, the pinned (alpha,theta) search and beta on the 10^-5 grid: the largest beta_0 at which C_0 is MET"),
 ("predicted", "MET at 0.01904 and NOT_MET at 0.01905, so beta_crude in [0.01904,0.01905); the certifying theta at the edge is 1/4; NOT_MET at beta_0=1/50"),
 ("predicts_NOT_MET", "C_0 crude at 0.01905 and at 1/50"),
 ("tag", "DERIVED (the arithmetic); its meaning as H_0=>H_1 runs through G0"),
 ("prefreeze", "COMPUTED (polymer-norm/window2.py, judge-cft/c05.py, synth/verify_core.py, final-check/edges.py and margins.py; the exact MET read at 0.01904 and the NOT_MET proof at 0.01905 by v2-checks/c19_missing_tail_and_x3.py)"),
 ("method", "exact rational KP sums: the series to n=48 plus the n=49 geometric tail using F_20(n+1)/F_20(n)<mu; the convex alpha-search of the certificates row, read as the exact inequality at the returned alpha; NOT_MET by the convex tangent bound of the certificates row"),
 ("falsifier", "the edge pair read otherwise, or C_0 crude read MET at 1/50"),
 ("reach", "closed form; one C_0 read takes seconds in scratch Decimal and minutes in exact rationals; the planted iteration_cap_400 of C19 reads the edge at 0.01901/0.01902"))

row("PREDICT", ("id", "C06"), ("lane", "S"), ("origin", "polymer-norm C06"),
 ("name", "the refined one-step window and what the counts buy"),
 ("statement", "with the C03 counts as the head (n<=10) and 6F_20(n) beyond: the largest beta_0 on the 10^-5 grid at which C_0 is MET; the head-free vector (N(n)=0, n<=10) bounds every count vector from above in reach"),
 ("predicted", "MET at 0.02075 and NOT_MET at 0.02076, the same edge as the head-free limit on this grid; DERIVED bracket: beta_crude<=beta_stop<=beta_stop(head-free), and the head-free certificate is NOT_MET at 0.02076; MET at beta_0=1/50, where the crude certificate is NOT_MET; so the exact counts move the edge from 0.01904 to within one grid step of the head-free limit, and the window is set by the Fuss-Catalan tail for n>=11, not by the head"),
 ("predicts_NOT_MET", "C_0 at 0.02076 for every count vector N(4..10)>=0"),
 ("tag", "CONJECTURE on C03, with the head-free clauses DERIVED; meaning as H_0=>H_1 through G0"),
 ("prefreeze", "COMPUTED (referee/check_headfree.py, synth/verify_core.py, final-check/edges.py and margins.py), on CROSS_READ counts"),
 ("method", "as C05, with the C03 counts as the head of S"),
 ("falsifier", "the refined edge pair read otherwise, an edge outside the DERIVED bracket, or NOT_MET at 1/50"),
 ("reach", "minutes once C03 has run"))

row("PREDICT", ("id", "C07"), ("lane", "S"), ("origin", "polymer-norm C07, retagged"),
 ("name", "the crude chain at beta_0=1/100"),
 ("statement", "C_0 crude MET, delta_1:=min 12alpha*e^{-4(theta-kappa)}, C_1(delta_1) MET, c(delta_1)<1, delta_2<=c(delta_1)delta_1 and sum_{k>=1}delta_k<=delta_1/(1-c(delta_1)); through G0 and G1 this maps H_0 into H_1 and H_1 into itself with a contraction"),
 ("predicted", "delta_1 in [0.011044,0.011045] (alpha=delta_1/12 at theta=1/4); 2delta_1*e^{delta_1} in [0.02233,0.02234]<=1/8; c(delta_1) in [0.44504,0.44505]; delta_2<=4.92e-3; sum_k delta_k<=0.01991; self-map MET"),
 ("tag", "CONDITIONAL_G0_G1, arithmetic DERIVED"),
 ("prefreeze", "COMPUTED (polymer-norm/delta_scan3.py and contraction.py, synth/verify_core.py, final-check/s_lane.py)"),
 ("method", "exact rationals through the pinned certificates; c(delta) by an exact maximum over integer n>=4, with upper and lower exponential enclosures"),
 ("falsifier", "C_0 or C_1 read NOT_MET at 1/100; delta_1 outside its bracket; c(delta_1)>=0.44505; sum_k delta_k above 0.01991; or gate G_attack finding an unrepaired gap or a differing constant in G0 or G1 (the row then reads UNSUPPORTED)"),
 ("reach", "closed form, minutes"))

row("PREDICT", ("id", "C08"), ("lane", "S"), ("origin", "polymer-norm C08, head-free value corrected"),
 ("name", "the refined chain at beta_0=1/100"),
 ("statement", "the quantities of C07 with the C03 counts; the head-free vector gives a lower limit on delta_1 valid for every count vector; the coarse Wilson term carried in R_1 is compared with delta_1"),
 ("predicted", "delta_1 in [9.42e-6,9.45e-6]; head-free lower limit in [9.372e-6,9.373e-6] (DERIVED arithmetic); c(delta_1) in [0.36793,0.36795]; sum_k delta_k<=1.50e-5; crude/refined delta_1 ratio in [1170,1172]; delta_1 is [3.6e3,3.8e3] times the norm 12e*c_1/2(1/100) in [2.548e-9,2.549e-9] of the coarse Wilson term it contains, where c_1/2(1/100) is read from the MEASURED series P_10 (YM4-03C receipt 76dc01b7) and is not certified here, since T/P_10 is in [1.38e4,1.40e4] at 1/100 (C09)"),
 ("tag", "CONJECTURE on C03 and CONDITIONAL_G0_G1"),
 ("prefreeze", "COMPUTED (polymer-norm/delta_scan3.py, synth/verify_core.py, final-check/s_lane.py), on CROSS_READ counts"),
 ("method", "as C07, with the C03 counts as the head of S; c_1/2(1/100) from the MEASURED series P_10 of YM4-03C"),
 ("falsifier", "delta_1 outside [9.42e-6,9.45e-6], the head-free limit outside its bracket, c outside [0.36793,0.36795], or C_1 NOT_MET"),
 ("reach", "minutes once C03 has run"))

row("PREDICT", ("id", "C09"), ("lane", "S"), ("origin", "polymer-norm C09, readout grid repaired, exclusion stated for clusters"),
 ("name", "the coarse plaquette coefficient tied to YM4-03C"),
 ("statement", "c_1/2(P) in [2t_2(beta)^4-T,2t_2(beta)^4+T], T:=(8489/10000)*12alpha*e^{-8theta} minimized over certified (alpha,theta) on the pinned grid theta<=21/4 with the C03 counts; every cluster other than {F_P} that holds both positions of all four links of P has at least 8 plaquettes, since no single polymer of 5, 6 or 7 plaquettes holds them and a cluster of two or more polymers holds at least 2x4 plaquettes (every polymer is Lemma-B-closed, and the smallest closed sets are the 4-plaquette fillings, C01); the interval is compared with the YM4-03C series P_10(beta)=beta^4/128-beta^6/768+beta^8/1536-467beta^10/2211840"),
 ("predicted", "no polymer of 5, 6 or 7 plaquettes holds all of the boundary of P at both positions; P_10 inside the certified interval at beta=1/4000, 1/2000, 1/1000; T/P_10 in [1.0e-3,1.1e-3] at 1/4000 (minimizing i=194), [1.6e-2,1.75e-2] at 1/2000 (i=150), [0.26,0.28] at 1/1000 (i=105), [1.10,1.13] at 1/700 (i=83), [1.38e4,1.40e4] at 1/100 (i=0); so the leading coarse coupling is resolved to within 0.11 percent at 1/4000 and lost between 1/1000 and 1/700, while C07 and C08 still certify H_1 at 1/100: the certificate controls the action there without resolving its leading coefficient"),
 ("tag", "CONDITIONAL_G0 (T is G0's readout); the T/P_10 values CONJECTURE on C03; the 5-7-plaquette exclusion CONJECTURE until the engine reads it"),
 ("low_power", "P_10-2t_2^4=(beta^8/2048)*(1-eta) with eta in [0,4e-7] at the three beta, and T exceeds it by a factor of at least 10^12, so containment can catch only a gross centering or sign error in G0"),
 ("prefreeze", "COMPUTED for T/P_10 and the minimizing i (polymer-norm/readout.py, judge-cft/c09_grid.py, synth/verify_core.py, final-check/c09.py) and for P_10-2t_2^4 (v2-checks/c09_readout_tail.py); NONE for the exclusion"),
 ("method", "t_2=I_2/I_1 enclosed by positive series; T in closed form over the grid; the 5-7-plaquette exclusion read off the C03 enumeration, split by held coarse links"),
 ("falsifier", "P_10 outside the certified interval at any of the three beta; a T/P_10 outside its bracket; a polymer of 5-7 plaquettes holding the whole boundary of P"),
 ("reach", "minutes once C03 has run; with the grid cut at i<=128 the read is grid-limited (planted fault readout_grid_128)"))

row("PREDICT", ("id", "C10"), ("lane", "S"), ("origin", "polymer-norm C10, reworded"),
 ("name", "the exact line channel, a lower bound on any valid contraction"),
 ("statement", "take a scale-k input with no Wilson term, R_k(Y)=s*chi_1/2 of the fine 2x2 loop on each next-coarse plaquette P'', Y its 8 line links (4 at position 0, 4 at position 1), every other R_k=0; it blocks with no integral to R_{k+1}(boundary of P'')=s*chi_1/2(V_P''); the fine norm reads 12*abs(s)*e^{8kappa} (6 next-coarse plaquettes through each line link, sup abs(chi_1/2)=2) and the coarse norm 12*abs(s)*e^{4kappa}; so every valid step bound on this class has c(delta)>=e^{-4kappa}, and in the kappa=0 norm no contraction is possible"),
 ("predicted", "delta_{k+1}/delta_k=e^{-1} in [0.3678794,0.3678795] at kappa=1/4, exactly, at 4 rational coarse configurations and s in {1/1000,1/100}; the ratio is unchanged under 4 rational coarse gauge transformations; ratio=1 at kappa=0"),
 ("predicts_NOT_MET", "a contraction in the kappa=0 norm"),
 ("tag", "DERIVED"), ("role", "NEGATIVE_CONTROL"),
 ("prefreeze", "COMPUTED for the norm counts (6 Y per line link, 6 P'' per coarse link, #Y=8, #Y''=4, by v2-checks/c19_one_position.py on (Z/8)^4); NONE for the holonomy reads"),
 ("method", "exact: the line-supported Y hold no off links, so E_V factors out and log rho_{k+1} gains R_k(Y) exactly (YM4-03 Proposition 2); exact quaternion holonomies and two rational norm sums"),
 ("falsifier", "an exact ratio other than e^{-4kappa} at kappa=1/4 or other than 1 at kappa=0, at any configuration, s or gauge"),
 ("reach", "a few exact quaternion holonomies, seconds"))

row("PREDICT", ("id", "C10b"), ("lane", "S"), ("origin", "new in the draft, judge requirement for a G1 falsifier beyond C10"),
 ("name", "an exact two-object instance of the multi-object channel"),
 ("statement", "at scale k split each next-coarse filling into two 1x2 rectangles along the lower of its two directions and set R_k(Y)=s*chi_1/2(rectangle loop) for each, Y its 6 links (4 line links and the 2 arm links the rectangles share), every other R_k=0; each object alone integrates to a constant, and the pair shares the arm path pi; exactly, to all orders in s, log rho_{k+1}(V)=const+sum_{P''}log c_0(2s*sqrt(2+chi_1/2(V_P''))); input norm delta_in=12*abs(s)*e^{6kappa}; the natural output norm delta_out=6e^{4kappa}*(1/2)log c_0(4s); every decomposition of the output has norm>=e^{4kappa}*abs(c_P)/E_abs(chi_1/2), c_P=E[f*chi_1/2] the chi_1/2(V_P'') coefficient of f=log c_0(2s*sqrt(2+chi_1/2)), with s^2/2-s^4/6 its first two Taylor terms"),
 ("predicted", "E_pi[(chi_b+chi_t)^{2m}]=Cat_m*(2+chi_1/2(V_P''))^m and odd moments 0, for m<=6 at 4 rational coarse configurations; at s=1/2000: delta_in in [0.026890,0.026891], C_k(delta_in) MET (2delta' in [0.05524,0.05525]), c(delta_in) in [0.5950,0.5951], delta_out in [4.077e-6,4.078e-6], delta_out/delta_in in [1.516e-4,1.517e-4], projection lower bound in [4.00e-7,4.01e-7], at most 3e-5 times c(delta_in)*delta_in; at s=1/4096: delta_in in [0.013129,0.013131], c(delta_in) in [0.4617,0.4618], delta_out/delta_in in [7.40e-5,7.41e-5]"),
 ("tag", "DERIVED; the c(delta_in) comparison CONDITIONAL_G1"),
 ("low_power", "G1 is refuted here only if it underestimates the multi-object term by more than 3x10^4"),
 ("prefreeze", "COMPUTED (synth/verify_extra.py, final-check/c10b.py); NONE for the moment reads"),
 ("method", "exact one-link integration of pi (degree<=12) by the engine's projector integrator at rational V, against the Catalan closed form; c_0 series with geometric tails; Haar projection of log c_0(2s*sqrt(2+chi)) onto chi_1/2 by its exact series"),
 ("falsifier", "an exact moment other than Cat_m(2+chi)^m; delta_out or the projection bound outside its bracket; the projection bound above c(delta_in)*delta_in (G1 refuted)"),
 ("reach", "24 one-link integrals of degree<=12 and closed-form series, seconds"))

row("PREDICT", ("id", "C10c"), ("lane", "S"), ("origin", "new in v2, the final critic's G1 power test"),
 ("name", "a single-object channel through off links: a G1 test with slack below 22"),
 ("statement", "at scale k, with rect_b and rect_t the two 1x2 rectangles of C10b in each next-coarse filling, set one object per P'': R_k(Y)=s*chi_1/2(rect_b)*chi_1/2(rect_t), Y the 10 links of the two loops (the 8 line links of the 2x2 boundary and the 2 arm links), every other R_k=0; sup abs(R_k(Y))=4abs(s), attained at U=1, so delta_in=24abs(s)*e^{10kappa}; each arm link lies in exactly one filling (C01), so log rho_{k+1}(V)=const+sum_{P''}f(chi_1/2(V_P'')), f:=log E_pi[e^{sX}], X:=chi_1/2(A*pi)*chi_1/2(pi^{-1}*B) with abs(X)<=4, pi the Haar arm path and AB the 2x2 boundary holonomy, which is V_P'' in the line gauge; leading order: E_pi[X]=chi_1/2(V_P'')/2 (Schur orthogonality: the Haar integral of tr(pi*G_1)tr(pi*G_2) is tr(G_1*G_2^{-1})/2), and sE_pi[X]<=f<=sE_pi[X]+8s^2 (Jensen and Hoeffding's lemma); the natural output R_{k+1}(boundary of P'')=f-(max f+min f)/2 has norm delta_out^nat=6e^{4kappa}*osc(f)/2 in 6e*[s-4s^2,s+4s^2]; every decomposition of the output has norm>=6e^{4kappa}*abs(c_P)/E_abs(chi_1/2), c_P:=E[f*chi_1/2] in [s/2-4s^2*E_abs(chi_1/2),s/2+4s^2*E_abs(chi_1/2)]"),
 ("engine_computes", "with its projector integrator, the exact rationals mu_m(V):=E_pi[X^m] for m=1..6 at 7 rational coarse configurations with distinct chi_1/2(V_P'') and at 4 more under rational coarse gauge transformations, integrating the two arm links one at a time (degree<=2m<=12 per link); mu_m depends on V only through chi_1/2(V_P'') and is a polynomial of degree<=m in it (conjugation invariance and the Clebsch-Gordan expansion of chi_1/2^m, DERIVED), so the 7 values fix it and the 4 more check it; from mu_1..mu_6 the cumulants and the s^1..s^6 Taylor polynomial of f, with the tail beyond s^6 at most (1/2)sum_{m>=7}(16s)^m by the YM4-04A Cauchy argument (abs(X)<=4, so f is analytic with abs(f)<1/2 on abs(s)<=1/16); then osc(f) over chi_1/2 in [-2,2], c_P, delta_out^nat and the every-decomposition bound"),
 ("predicted", "mu_1(V)=chi_1/2(V_P'')/2 exactly at all 11 configurations; delta_out^nat/delta_in in (e^{-3/2}/4)*[1-4s,1+4s], e^{-3/2}/4 in [0.05578254,0.05578255]; at s=1/8192: delta_in in [0.0356909,0.0356910], C_k(delta_in) MET (2delta' in [0.0739754,0.0739755]), c(delta_in) in [0.7118122,0.7118123], delta_out^nat/delta_in in [0.0557553,0.0558098], every-decomposition bound/delta_in in [0.0328285,0.0328860], bound/(c(delta_in)*delta_in) in [0.04611,0.04621]; at s=1/65536: delta_in in [0.0044613,0.0044614], 2delta' in [0.0089626,0.0089627], c(delta_in) in [0.3969925,0.3969926], delta_out^nat/delta_in in [0.0557791,0.0557860], bound/delta_in in [0.0328523,0.0328622], bound/(c(delta_in)*delta_in) in [0.08275,0.08278]; so G1 is not refuted at either s"),
 ("tag", "DERIVED (mu_1, the brackets, the six-plaquette bound); the c(delta_in) comparison CONDITIONAL_G1"), ("role", "G1_TEST"),
 ("power", "G1 is refuted here only if c(delta_in) underestimates the every-decomposition bound, which needs an error by a factor in [12.08,12.09] at s=1/65536 ([21.64,21.69] at s=1/8192); against the natural decomposition the slack is [7.116,7.118] ([12.754,12.767]); C10b's slack is 3x10^4"),
 ("prefreeze", "COMPUTED for e^{-3/2}/4, delta_in, 2delta', c(delta_in) and the brackets (v2-checks/c10c_constants.py and c10c_brackets.py); NONE for every mu_m; no SU(2) integral was computed before this freeze"),
 ("method", "the six-plaquette bound, DERIVED here: for a coarse link l of the boundary of P'', a Y containing l that holds the boundaries of j of the 6 coarse plaquettes through l has #Y>=3j+1, and e^{kappa(3j+1)}/j>=e^{4kappa} for j=1..6 at kappa=1/4; the chi_1/2(V_P) projection of R(Y) is at most E_abs(chi_1/2)*sup abs(R(Y)) and is 0 unless Y holds the boundary of P; so the 6 projections c_P through l add; E_abs(chi_1/2)=8/(3pi) enclosed by pi in [3.1415,3.1416]; c(delta) as in C07"),
 ("falsifier", "mu_1 other than chi_1/2(V_P'')/2 at any configuration; a mu_m that is not one polynomial of degree<=m in chi_1/2(V_P'') across the 11 configurations; delta_out^nat/delta_in or the bound/delta_in outside its bracket; the every-decomposition bound above c(delta_in)*delta_in (G1 refuted)"),
 ("reach", "11 configurations x 6 moments x 2 one-link integrals of degree<=12, seconds; closed-form series"))

row("PREDICT", ("id", "C11"), ("lane", "S"), ("origin", "polymer-norm C11"),
 ("name", "one crude step holds at 1/64 but the crude hypothesis does not map to itself"),
 ("statement", "at beta_0=1/64 with the crude counts: C_0, C_1(delta_1) and the self-map"),
 ("predicted", "C_0 crude MET with delta_1 in [0.10165,0.10166]; 2delta_1*e^{delta_1} in [0.22505,0.22507]>1/8, so C_1 NOT_MET and the crude self-map NOT_MET; the refined certificate is MET here (C14)"),
 ("predicts_NOT_MET", "C_1 and the crude self-map at 1/64"),
 ("tag", "CONDITIONAL_G0_G1: the delta_1 of the C_0 clause is G0's formula and the C_1 test is G1's; arithmetic DERIVED"), ("role", "NEGATIVE_CONTROL"),
 ("prefreeze", "COMPUTED (polymer-norm/window2.py, synth/verify_core.py, final-check/s_lane.py)"),
 ("method", "as C07, at beta_0=1/64"),
 ("falsifier", "C_1 read MET, or C_0 read NOT_MET, at 1/64 with the crude counts; delta_1 outside [0.10165,0.10166]"),
 ("reach", "closed form, minutes"))

row("PREDICT", ("id", "C12"), ("lane", "S"), ("origin", "polymer-norm C12, head-free value corrected"),
 ("name", "at 1/50 the self-map fails under every count model while one refined step holds"),
 ("statement", "at beta_0=1/50: the crude C_0, the head-free lower limit on delta_1 valid for every count vector, C_1 and the refined C_0"),
 ("predicted", "C_0 crude NOT_MET (DERIVED, since 1/50>beta_crude); head-free delta_1 in [0.072645,0.072646], so every count vector has delta_1>=0.072645 and 2delta_1*e^{delta_1}>=0.15623>1/8, and C_1 is NOT_MET (DERIVED arithmetic); C_0 refined MET with delta_1 in [0.072646,0.072648] (CONJECTURE on C03)"),
 ("predicts_NOT_MET", "C_0 crude, C_1 and the self-map under every count model, at 1/50"),
 ("tag", "CONDITIONAL_G0_G1: delta_1 is G0's formula and the C_1 test is G1's; arithmetic DERIVED, the refined clause CONJECTURE on C03"), ("role", "NEGATIVE_CONTROL"),
 ("prefreeze", "COMPUTED (referee/check_headfree.py, synth/verify_core.py, final-check/s_lane.py)"),
 ("method", "as C07 and C08, at 1/50, with the head-free bound as a lower limit for every count vector"),
 ("falsifier", "C_1 read MET at 1/50 under any counts, C_0 crude read MET, the head-free delta_1 outside its bracket; for the conjectured clause, C_0 refined read NOT_MET"),
 ("reach", "closed form, minutes; the refined clause needs C03"))

row("PREDICT", ("id", "C13"), ("lane", "S"), ("origin", "polymer-norm C13, admissibility test repaired"),
 ("name", "where the crude self-map stops"),
 ("statement", "delta_crit:=sup{delta: C_k(delta) MET and c(delta)<1}; beta_ind^crude:=the largest beta_0 on the 10^-5 grid with C_0 crude MET and delta_1<delta_crit^- (the pinned test; the design-lane surrogate delta_1<=49/1000 read the edge at 0.01365/0.01366)"),
 ("predicted", "c(49/1000) in [0.98248,0.98249]; c(1/20) in [1.0110,1.0111]; delta_crit in [0.0496174,0.0496175]; MET at 0.01369 (delta_1 in [0.049602,0.049603]) and NOT_MET at 0.01370 (delta_1 in [0.049788,0.049789]), so beta_ind^crude in [0.01369,0.01370); beta_ind^crude<beta_crude"),
 ("predicts_NOT_MET", "the crude self-map at 0.01370 and above"),
 ("tag", "CONDITIONAL_G0_G1, arithmetic DERIVED"),
 ("prefreeze", "COMPUTED (polymer-norm/induction_window.py, referee/check_ind.py, synth/verify_core.py, final-check/edges.py)"),
 ("method", "bisection on delta for c(delta)=1 with enclosures; C05's procedure with the extra test delta_1<delta_crit^-"),
 ("falsifier", "c(49/1000) or c(1/20) outside its bracket; delta_crit outside its bracket; the edge pair read otherwise; beta_ind^crude>=beta_crude"),
 ("reach", "closed form, under an hour"))

row("PREDICT", ("id", "C14"), ("lane", "S"), ("origin", "polymer-norm C14, admissibility test repaired"),
 ("name", "where the refined self-map stops"),
 ("statement", "as C13 with the C03 counts, and with the head-free vector as the bound for every count vector; this edge is the regime boundary of the hypothesis row"),
 ("predicted", "MET at 0.01959 (delta_1 in [0.049382,0.049383]) and NOT_MET at 0.01960, the same edge as the head-free limit; head-free NOT_MET at 0.01960, so beta_ind<0.01960 for every count vector N(4..10)>=0 (DERIVED arithmetic); at beta_0=1/64 the refined self-map is MET with delta_1 in [2.0347e-3,2.0348e-3] and c(delta_1) in [0.38085,0.38086]; ordering beta_ind<beta_stop<beta_wall(1/4), 0.01959<0.02075<0.02247"),
 ("predicts_NOT_MET", "the self-map at 0.01960 and above for every count vector N(4..10)>=0"),
 ("tag", "CONJECTURE on C03 and CONDITIONAL_G0_G1, the head-free clauses DERIVED arithmetic"),
 ("prefreeze", "COMPUTED (referee/check_ind.py, synth/verify_core.py, final-check/edges.py), on CROSS_READ counts"),
 ("method", "as C13, with the C03 counts"),
 ("falsifier", "the edge pair read otherwise, the refined self-map read NOT_MET at 1/64, a value outside its bracket, or the ordering violated"),
 ("reach", "under an hour once C03 has run"))

row("PREDICT", ("id", "C15"), ("lane", "S"), ("origin", "polymer-norm C15, scoped to finite heads"),
 ("name", "above the window the certificate is refuted under every count model it allows"),
 ("statement", "at beta_0=1/45, 1/40, 1/18 (the YM4-04B edge), 1/10, 1 and 4: the wall quantity mu*e^{1/4}*eps_6 and the C_0 read; a finite head is any n_max>=4 with any counts N(4..n_max)>=0, followed by the 6F_20(n) tail beyond n_max"),
 ("predicted", "1/45: mu*e^{1/4}*eps_6 in [0.9888,0.9889]<1, so the tail converges at small alpha, and the pinned certificate (n_max=10, every count vector N(4..10)>=0) is NOT_MET, since 1/45 is above the head-free edge 0.02076; a finite head with n_max>10 is not covered at 1/45 (OPEN); 1/40: [1.1125,1.1126]; 1/18: [2.473,2.474]; 1/10: [4.4575,4.4576]; 1: [50.40,50.41]; 4: [292.4,292.5]; each of these five is above 1, so at 1/40 and above C_0 is NOT_MET for every alpha in [0,1/4], every theta>=1/4 and every finite head with the 6F_20(n) tail beyond n_max, by a margin that grows with beta"),
 ("predicts_NOT_MET", "C_0 at all six couplings: for every finite head with the 6F_20(n) tail beyond n_max at the five couplings 1/40 and above, and for the pinned n_max=10 with every count vector at 1/45"),
 ("tag", "DERIVED (the C04 wall test above 1/40, the head-free arithmetic at 1/45); the wall belongs to the 6F_20(n) tail, not to the norm; meaning as a statement about H_1 through G0"), ("role", "NEGATIVE_CONTROL"),
 ("prefreeze", "COMPUTED (polymer-norm/derive_estimates.py, final-check/s_lane.py)"),
 ("method", "C02 enclosures and the C04 wall test; at 1/45 the head-free search with the NOT_MET proof of the certificates row"),
 ("falsifier", "any MET at these six couplings within the stated scope, or a wall quantity outside its bracket"),
 ("reach", "closed form, minutes"))

row("PREDICT", ("id", "C16"), ("lane", "S"), ("origin", "polymer-norm C16, first clause only"),
 ("name", "inside the window the certified class flows toward Haar"),
 ("statement", "from C07, delta_m<=c(delta_1)^{m-1}*delta_1 for m>=1, uniformly in N and K; on a final coarse 4^4 torus with 1024 links, osc_V log rho_m<=2*1024*e^{-4kappa}*delta_m/4=(512/e)delta_m; this is a statement about the certified class, which runs to the trivial fixed point, and not about UV completeness of the theory"),
 ("predicted", "at beta_0=1/100 with the crude constants: delta_20<=c(delta_1)^19*delta_1 in [2.30e-9,2.31e-9]; osc_V log rho_20<=4.35e-7 on the coarse 4^4 torus at spacing 2^20*h_0, within a factor e^{+-4.35e-7} of Haar"),
 ("tag", "CONDITIONAL_G0_G1, arithmetic DERIVED"),
 ("prefreeze", "COMPUTED (synth/verify_extra.py)"),
 ("method", "exact rational powers and products of the C07 outputs; the bound sum_Y sup abs(R(Y))<=#links*delta*max_{#Y>=4}e^{-kappa*#Y}/#Y"),
 ("falsifier", "the delta_20 bound outside its bracket, the oscillation bound above 4.35e-7, or c(delta_1)>=1"),
 ("reach", "arithmetic, seconds"))

row("PREDICT", ("id", "C17"), ("lane", "S"), ("origin", "polymer-norm C17, narrowed"),
 ("name", "the certificate is local and replaces the global remainder at strong coupling"),
 ("statement", "every input of C_0 and C_k (census, counts N(n), eps_6, KP sums, delta_1, c) reads byte-identical on fine (Z/8)^4 and (Z/12)^4; the YM4-04A global route needs beta<=1/(8N_p): YM4-04A proved it at b=3, and its Cauchy argument (abs(X)<=N_p for the fine plaquette sum X=sum_p(1/2)chi_1/2(U_p), on the disk abs(z)<=1/(4N_p)) does not use the blocking factor, so the same hypothesis stands at b=2"),
 ("predicted", "identical receipts on the two lattices; 1/(8N_p)=1/196608 on 8^4, 1/995328 on 12^4, 1/3145728 on 16^4, ->0 as N->infinity; at beta_0=1/100 the global route certifies nothing on any lattice with N_p>=13, while C07's local certificate holds on every fine torus with sides>=8; the replacement holds only for the effective-action norm at beta_0<=0.01959 (C14's edge)"),
 ("tag", "DERIVED (1/(8N_p) and the byte comparison as exact reads); the replacement clause CONDITIONAL_G0_G1"), ("role", "CONTROL"),
 ("prefreeze", "CROSS_READ for the counts on both lattices (synth/closed_sets_copy.py); COMPUTED for 1/(8N_p)"),
 ("method", "run the census, the enumeration and the certificate on both lattices and compare byte for byte; 1/(8N_p) exactly"),
 ("falsifier", "any difference between the two lattices' certificate rows, or any dependence on L in a bound"),
 ("reach", "doubles C03's cost; the 12^4 run reuses the same local classes"))

row("PREDICT", ("id", "C18"), ("lane", "S"), ("origin", "polymer-norm C18"),
 ("name", "the line gauge is a fixing artifact the readouts do not see"),
 ("statement", "for the classes F_P (spins 1/2 and 1), the 16 bumps and the 16 cubes on a face of YM4-03C, the exact SU(2) integrals Phi_S(j;V) at four rational coarse configurations read the same with V carried at position 1, gauge (1,V), as at position 0, gauge (V,1), and are unchanged under four rational coarse gauge transformations extended to the midpoints as in YM4-03 Theorem 4; the filling's chi_1/2 readout equals 2t_2^4 in both gauges"),
 ("predicted", "all equal as exact rationals: 0 differences"),
 ("tag", "DERIVED (gauge covariance, YM4-03 Theorem 4)"), ("role", "CONTROL"),
 ("prefreeze", "NONE"),
 ("method", "exact link-by-link SU(2) integration at rational unit quaternions (the engine's own projector integrator; the check uses the merged YM4-03C engine)"),
 ("falsifier", "any nonzero difference"),
 ("reach", "about 33 classes x 2 gauges x 8 configurations; the YM4-03C integrator ran 33,208 one-link integrals in 25-40s"))

row("PREDICT", ("id", "C19"), ("lane", "S+W"), ("origin", "polymer-norm C19, coupling-flow CT16, small-large-field R15; three faults pinned by exact runs in v2"),
 ("name", "planted faults and planted false claims"),
 ("statement", "each planted fault stops the engine on its named check with exit 1: finner_exponent_2 (eps_6 replaced by the L^2 norm)->G_finner_guard, on the 10-plaquette filling-plus-cube set whose shared off link lies in 4 plaquettes; degree_19 (D=19)->C01; missing_tail (S replaced by the head-only polynomial sum_{n=4..10}N(n)x^n with the C03 head: the terms n=11..48 and the n=49 tail removed)->C04, whose guard then reads the refined C_0 MET at 1/40 and at 0.02248 (alpha=2^-22 certifies, with S^+<=1.96e-7 and <=1.28e-7); one_position_support (the norm routine sets #Y to the number of links of Y at position 1, the links that carry V in the line gauge (1,V), in place of all links of Y)->C10, fine norm 12abs(s)e^{4kappa} and ratio 1 in place of e^{-1} at kappa=1/4; global_norm (sum over all Y in place of Y containing l)->C17, 8^4 and 12^4 differ; readout_without_tail (T:=0)->C09 containment, since P_10-2t_2^4=(beta^8/2048)*(1-eta) with eta in [0,4e-7] at the three beta; iteration_cap_400 (at every grid theta the convex search and the exact read are replaced by the iteration alpha_0=0, alpha_{j+1}=s_j:=S^+(up(eps_6^+*e^{2alpha_j+theta})), read MET at the first j with s_j<=alpha_j*(1+10^-40) and NOT_MET when s_j is undefined or above 1/4, or after 400 evaluations of S^+)->C05, MET lost at 0.01902, 0.01903 and 0.01904, so the faulted crude edge reads 0.01901/0.01902; delta_crit_surrogate (delta_1<=49/1000 in place of delta_1<delta_crit^-)->C13, MET lost at 0.01366-0.01369; readout_grid_128 (theta cut at i<=128)->C09, T/P_10 in [2.9e-2,3.0e-2] at 1/4000; drop_alias_terms (aliases with n_perp ne 0 dropped)->W01, corner r_1=2 in place of 15/28; longitudinal_read_unflagged->W05; float_literal in any engine file->G_nofloat; planted false claims, read by the same reader from a planted copy of this file: C_0 crude MET at 1/50; the head-free self-map MET at 1/50; the line-map corner k-independent (r_2=r_1); the averaged corner equal to the line corner"),
 ("variants_that_would_not_fire", "missing_tail cut at 10 with the crude head, or cut at 48 with any head: C_0 stays NOT_MET at 1/40 and 0.02248; one_position_support as drafted (a coarse link counted as held from one position): #Y''=4 on C10's input either way, ratio e^{-1}; iteration_cap_400 with alpha_{j+1}=up(s_j*10001/10000) and acceptance s_j<=alpha_j: MET through 0.01904; with alpha_{j+1}=s_j and acceptance s_j<=alpha_j it loses MET from 0.01901 on, so the stated edge would move; these are recorded so that the pinned variants are the ones the engine plants"),
 ("predicted", "12 of 12 faults stop on their named checks with exit 1; 4 of 4 planted claims read NOT_MET, with the misses at C12, C12, 25823/98640 ne 15/28 and 2 ne 15/28; the unplanted run exits 0 and its receipt is byte-identical across two runs"),
 ("tag", "DERIVED for the faulted values, by exact runs; the delta_crit_surrogate edge and the readout_grid_128 value are values of G1's and G0's formulas (CONDITIONAL_G1, CONDITIONAL_G0)"), ("role", "NEGATIVE_CONTROL"),
 ("prefreeze", "COMPUTED (final-check/faults.py, fault_judge.py, fault_dl.py; v2-checks/c19_iteration_cap.py, c19_missing_tail_and_x3.py, c19_one_position.py, c09_readout_tail.py; judge-cft/c09_grid.py; polymer-norm/window2.py); NONE for the engine's exits"),
 ("method", "SABOTAGE=<name> read once, as in the YM4-03C engine; each guard runs before the quantity it protects is used; each fault recomputes only the sections it reaches, the others replay from the receipt by sha256 (the YM4-03 replay of PR 43)"),
 ("falsifier", "a planted run that exits 0 or stops on another check; a planted claim read MET; the clean receipt differing between runs"),
 ("reach", "twelve reruns of minute-scale sections and four reader passes"))

row("PREDICT", ("id", "W01"), ("lane", "W"), ("origin", "coupling-flow CT12 merged with small-large-field R10"),
 ("name", "tree-level iterated line map: marginal, with an irrelevant part that grows like 2^k"),
 ("statement", "r_k(p) for the exact composition B_{2^k}, transverse polarization mu, p=q*e_nu, from the alias formula C'(p)=b^{2-d}sum_{n_perp in Z_b^{d-1},n_mu=0}1/khat^2((p+2pi*n)/b), r=C'_W/C', C'_W=1/phat^2, gauge independent since every contributing alias has k_mu=0; A_b=b^{-2}sum_{n ne 0}1/khat^2(2pi*n/b)-(1-1/b^2)/12, the exact limit of (1/r(p)-1)/phat^2 as q->0; G_3(0):=the integral of 1/khat^2(k) over [-pi,pi]^3 with measure d^3k/(2pi)^3; A_b/b->G_3(0) as b->infinity, since b^{-3}sum_{n ne 0}1/khat^2(2pi*n/b) is a Riemann sum of the integrable 1/khat^2 (DERIVED, proof in note section 10)"),
 ("predicted", "k=1 profile r_1 at t_W=tan(q/2)=1/16,1/8,1/4,1/2,1 and q=pi: 12689633/12736932, 813281/825252, 56033/59172, 4961/5892, 833/1212, 15/28, strictly decreasing, so the blocked Gaussian form is not Wilson-quadratic at any nonzero momentum; r_k(p)->1 as q->0 for k=1,2,3 (classical marginality, beta'_G=beta); A_1=23/96, A_2=1367/1920, A_3=113360987/66106880 in [1.7148137531,1.7148137532]; corners r_1=15/28, r_2=25823/98640, r_3 in [0.1274530942,0.1274530943]; A_k/2^k=23/192, 1367/7680, 113360987/528855040, in [0.1197916,0.1197917], [0.1779947,0.1779948], [0.2143517,0.2143518], strictly increasing and below G_3(0) in [0.2527310,0.2527311]; 2^k*r_k=15/14, 25823/24660 and [1.0196247,1.0196248], strictly decreasing and above 1/(4G_3(0)) in [0.989194,0.989195]"),
 ("predicts_NOT_MET", "H_k^W(ii) for M=B: the DERIVED limit A_{2^k}/2^k->G_3(0)>0 makes A_{2^k} grow like G_3(0)*2^k, so no k-uniform bound on the irrelevant part holds at tree level; the k=1..3 values are checks of that limit, and three scales alone do not show unboundedness"),
 ("tag", "DERIVED; the value of G_3(0) REPORTED (G. N. Watson, Quart. J. Math. Oxford 10 (1939) 266-276), used only for the stated inequalities"),
 ("prefreeze", "COMPUTED (coupling-trajectory/d3_tree.py and d5_tree_exact.py, judge-cft/spot.py, referee/check_sl_ct.py, final-check/wlane.py and wlane_hp.py, v2-checks/w_lane_exact.py)"),
 ("method", "route A: alias sums in exact rationals at b=2,4; at b=8 in Q(sqrt2) for A (the sqrt2 parts cancel under the permutation 1<->3, 5<->7 of Z_8, so A_3 is rational) and by dyadic interval enclosure in Q(sqrt2,sqrt(2+-sqrt2)) for the corner; route B: gauge-free constrained minimization of (1/2)sum_p F_p^2 on fine (Z/2b)^4 with the coarse data fixed, Bloch-reduced, exact KKT/Schur solve at b=2,4; the lattice sum in A_b also by an exact real-space pseudo-inverse Laplacian on (Z/b)^3"),
 ("falsifier", "any value differing between routes or from the prediction; r_k(p) not ->1; A_k/2^k not increasing; 2^k*r_k not decreasing"),
 ("reach", "route A at most 8^3 terms, seconds; route B 64 and 1024 unknowns per sector, minutes"),
 ("scope", "tree level, line map only; a MET here says nothing about the one-loop step Delta_beta"))

row("PREDICT", ("id", "W02"), ("lane", "W"), ("origin", "coupling-flow CT13, reworded"),
 ("name", "tree-level comparator: the linearized block average"),
 ("statement", "the abelian linearization of the average of b-step transporters over the b^d offsets of a block; transverse aliases with n_lambda ne 0 cancel exactly when p_lambda=0, so the normalized values r*b^{4-d} do not depend on d; this is a Gaussian fixed-point computation for a linearized map: the non-abelian averaged map (average plus projection to SU(2), covariance, positivity, reflection positivity) is not constructed"),
 ("predicted", "corner r_avg(pi;b)=3b^2/(b^2+2)=2, 8/3, 32/11 at b=2,4,8, tending to 3; slope A_avg(b)=-(1-1/b^2)/6=-1/8, -5/32, -21/128, tending to -1/6; r_avg(p)->1 as q->0; the deviations 6/(b^2+2)=1, 1/3, 1/11 and 1/(6b^2)=1/24, 1/96, 1/384 shrink per doubling of b by the factors 3 and 11/3 (corner) and 4 and 4 (slope), tending to 4; the same normalized values in d=2,3,4; so H_k^W(ii) holds at tree level for the linearized average, against its failure for B (W01)"),
 ("tag", "DERIVED"),
 ("prefreeze", "COMPUTED (coupling-trajectory/d3_tree.py and d5_tree_exact.py)"),
 ("method", "the closed form through sum_{n<b}csc^4((2n+1)pi/(2b))=b^2(b^2+2)/3; the alias formula in exact arithmetic; route B as in W01 at b=2,4"),
 ("falsifier", "any value differs, the deviations do not shrink, or the averaged corner equals the line map's"),
 ("reach", "seconds to minutes"))

row("PREDICT", ("id", "W03"), ("lane", "W"), ("origin", "coupling-flow CT14 with small-large-field R10 (d=2,3); increment bracket corrected in v2"),
 ("name", "dimension dependence of the line map's degradation"),
 ("statement", "the W01 quantities in d=2 and d=3, normalized by classical scaling b^{d-4}; d=2 is the tree-level image of YM4-03 Theorem 8's exact closure"),
 ("predicted", "d=2: r=1/b^2 exactly at q in {pi/2,2pi/3,pi} and A=0, b=2,4,8; d=3: unnormalized k=1 profile r_1 at the W01 points 2057/4120, 521/1048, 137/280, 41/88, 17/40, 3/8; corner b*r=3/4, 119/208, [0.4581134488,0.4581134489] at b=2,4,8; A=3/32, 73/384, 54335/182784 in [0.2972634366,0.2972634367]; increments 37/384 and 6529/60928 in [0.1071592,0.1071593], both inside [0.09,0.12] (logarithmic growth toward ln2/(2pi) in [0.1103,0.1104] per doubling, display only); d=4: linear growth (W01); so the degradation is absent (d=2), logarithmic (d=3) and linear (d=4) in b"),
 ("tag", "DERIVED"),
 ("prefreeze", "COMPUTED (coupling-trajectory/d3_tree.py and d6_two_d.py, final-check/wlane.py and wlane_hp.py, v2-checks/w_lane_exact.py, which found the draft's [0.10716,0.10717] excluding 6529/60928)"),
 ("method", "the alias formula exactly, with the 1D identity sum_{n<b}1/(4sin^2((x+2pi*n)/(2b)))=b^2/(4sin^2(x/2)) for d=2; A at b=8 in Q(sqrt2), rational by the cancellation of W01; route B at b=2,4 for d=2,3"),
 ("falsifier", "d=2 not exactly 1/b^2 at some momentum; any d=3 value differs; a d=3 increment outside [0.09,0.12]"),
 ("reach", "seconds to minutes"))

row("PREDICT", ("id", "W04"), ("lane", "W"), ("origin", "small-large-field R12, verdict narrowed; relabelled a reproduction row in v2"),
 ("name", "line-map coarse plaquettes roughen at the Gaussian level"),
 ("statement", "r_k:=V(2^k x 2^k)/V(1x1), V(C)=sum_{l,l' in C}o_l*o_l'*G_L(x_l-x_l') (o_l=+-1 the orientation of l in C), the flux variance of the scale-k line-map coarse plaquette (a fine 2^k x 2^k Wilson loop), gauge invariant, computed in Feynman gauge with the torus Green's function (Delta*G_L=delta-1/N_s, sum G_L=0); in infinite volume r_{k+1}/r_k->2 by the perimeter law (DERIVED)"),
 ("predicted", "on (Z/16)^4: r_1 in [2.65,2.85], r_2 in [6.2,6.8], r_2/r_1 in [2.2,2.5]; on (Z/8)^4: r_1 in [2.6,2.9], r_2 in [6.0,6.9]; consequence: at fixed p_SF the Gaussian large-field probability Q(3/2,4p_SF^2/r_k) of the scale-k coarse plaquette grows with k (at p_SF^2=2 near 0.0011, 0.12, 0.48 for k=0,1,2, display only)"),
 ("predicts_NOT_MET", "H_k^W(iii) for M=B, at the Gaussian level, for this plaquette small-field condition with k-independent p_SF; nothing is said about an averaging map or about finite beta"),
 ("tag", "DERIVED for the infinite-volume limit only; the finite-volume brackets carry no prediction tag: they were set around the float reads r_1=2.7349, r_2=6.4220 on 8^4 and 2.7384, 6.5187, ratio 2.3805 on 16^4, so the row is a reproduction, not a blind prediction"), ("role", "REPRODUCTION"),
 ("prefreeze", "CROSS_READ by float runs (judge-engineer/slf_ct_sanity.py, synth/r12_float_sanity.py); not evidence; the row is left out of every predictions-confirmed count"),
 ("method", "exact orbit-reduced Poisson solve under the hyperoctahedral symmetry (70 rational unknowns on 8^4, 495 on 16^4), then exact rational sums over loop link pairs; Q(3/2,y) by rational series"),
 ("falsifier", "any r outside its interval, or r_2/r_1 below 2.2 on 16^4"),
 ("reach", "a 495x495 sparse exact rational solve, minutes"))

row("PREDICT", ("id", "W05"), ("lane", "W"), ("origin", "coupling-flow CT15"),
 ("name", "gauge-fixing artifacts separated from invariant reads"),
 ("statement", "the transverse tree-level read does not depend on the gauge used as an intermediate; a coupling read from the longitudinal coarse mode (polarization nu along p=pi*e_nu) is a gauge-fixing artifact, and the engine's invariance check must refuse it"),
 ("predicted", "b=2, d=4: transverse corner ratio 15/28 in covariant gauges xi=1/2,1,3 and by the gauge-free route; longitudinal ratio (xi/4)/C'_nunu(xi)=3675/7372 (xi=1/2), 35/48 (xi=1), 11025/10456 (xi=3), pairwise unequal, so the longitudinal read is flagged and excluded"),
 ("predicts_NOT_MET", "gauge independence of the longitudinal read"),
 ("tag", "DERIVED"), ("role", "NEGATIVE_CONTROL"),
 ("prefreeze", "COMPUTED (the coupling-flow design lane, rechecked by the synthesis lane and the final critic)"),
 ("method", "alias sums with G_munu=(delta_munu-(1-xi)khat_mu*khat_nu/khat^2)/khat^2 in exact rationals; the gauge-free KKT route of W01; an invariance check that compares every read across xi and flags any read that differs"),
 ("falsifier", "the transverse ratio depends on xi or differs from the gauge-free value; the three longitudinal ratios coincide; or the check fails to flag them"),
 ("reach", "16 alias terms per read, seconds"))

row("PREDICT", ("id", "W06"), ("lane", "W"), ("origin", "small-large-field R11(a)(b), clause (c) dropped; twist arithmetic stated in v2"),
 ("name", "the Gaussian fluctuation operator of one line-map step is positive"),
 ("statement", "d^T*d, the Hessian of (1/2)sum F^2 per color, restricted to the fiber ker B intersected with the orthogonal complement of the fiber gauge directions (45 dimensions per coarse cell: 64 fine links, 4 constraints, 15 fiber gauge directions); (a) it is positive definite in every Bloch sector, since a closed fiber vector is a fiber gauge direction (DERIVED); (b) in the k'=0 sector its lowest eigenvalue lambda_0* is the smallest root of lambda^3-18lambda^2+80lambda-48, from the secular equation over the B-coupled transverse modes {4,4,4,8,8,8,12} of the 2^4 cell; a computed minimum over sectors is only an upper bound on the infinite-volume gap, and a whole-zone lower bound needs a covering certificate, OPEN"),
 ("predicted", "(a) no eigenvalue<=0 in the 16 sectors of fine 4^4, the 256 of fine 8^4, or the twisted sectors k'=2pi*t_tw*e_1 and 2pi*t_tw*(1,1,1,1) with t_tw in {1/2,1/4,1/8}; fiber dimension 45 per cell; (b) lambda_0* in [0.7084973778,0.7084973779], multiplicity 4; exact inertia: 0 eigenvalues below 7/10 and 4 below 71/100"),
 ("tag", "DERIVED"),
 ("prefreeze", "CROSS_READ for (b) (exact inertia, smallfield-largefield/d2_fiber_k0.py); NONE for (a)"),
 ("method", "an exact basis of the physical fiber per sector over Q (t_tw=1/2 and the untwisted sectors whose phases are +-1), Q(i) (t_tw=1/4 and sectors with phases +-i) or Q(zeta_8)=Q(i,sqrt2) (t_tw=1/8, phase e^{i*pi/4}); eigenvalue counts below lambda by exact LDL^* inertia of the Hermitian pencil K_fib-lambda*G_fib (fiber Hessian and Gram matrix), whose pivots lie in the real subfield Q, Q or Q(sqrt2), each sign decided exactly (u+v*sqrt2>0 with u,v rational, by comparing u^2 with 2v^2 when u and v differ in sign); bisection to 10^-10, shifting off exact rational eigenvalues to avoid zero pivots"),
 ("falsifier", "a nonpositive eigenvalue in any sector; a fiber dimension other than 45; a k'=0 value outside the bracket or with another multiplicity"),
 ("reach", "about 30 symmetry classes of sectors x 40 LDLs of 45x45 matrices, minutes"))

row("PREDICT", ("id", "W07"), ("lane", "W"), ("origin", "small-large-field R02 with the R04 consequence, wording repaired"),
 ("name", "the small-field threshold and an inherited large-field bound lose 16 per step"),
 ("statement", "for a fine 2x2 tile with plaquettes p_1..p_4 and boundary holonomy V' (the coarse plaquette): abs(1-V')<=sum_i abs(1-U_{p_i}) (lasso decomposition and conjugation invariance), so 1-a(V')<=4sum_i(1-a(U_{p_i}))<=16max_i(1-a(U_{p_i})); on the abelian aligned tile U_1=1, U_2(x)=g_T^{x_1}, g_T=cos(phi)+sin(phi)*e_3 a rational unit quaternion (e_3 the third quaternion unit), every fine plaquette has 1-a=eps and the ratio is exactly 16-40eps+32eps^2-8eps^3=8(1-eps)^2(2-eps), which tends to 16 as eps->0 and is below 16 at every eps>0; consequence (a surfaced error-growing recurrence): deterministic propagation of the plaquette small-field set {1-a(U_p)<=eps_k} into {1-a(V')<=eps_{k+1}} needs eps_{k+1}>=eps_k*(16-40eps_k+32eps_k^2-8eps_k^3) (the aligned tile), and eps_{k+1}=16eps_k suffices (the max inequality); a fine bound P(1-a(U_p)>eps)<=e^{-beta*eps+Phi} transfers by the union bound only as P(1-a(V')>eps')<=4e^{-beta*eps'/16+Phi}, a threshold 16(Phi+log4)/beta; after k steps the loss is 16^k, so LF_{k+1} must come from rho_{k+1}'s own effective action (OPEN); these are two routes, not a theorem that no inheritance exists"),
 ("predicted", "aligned-tile ratios 4064256/274625 (cos phi=63/65), 266342400/16974593 (255/257), 17146331136/1076890625 (1023/1025), each equal to 16-40eps+32eps^2-8eps^3 at eps=1-cos phi and each below 16; both inequalities hold on 10^4 seeded random rational tiles (Cayley-map quaternions)"),
 ("predicts_NOT_MET", "H_k^W(iv) for M=B: lossless inheritance across one step by either route"),
 ("tag", "DERIVED"),
 ("prefreeze", "COMPUTED for the aligned ratios (smallfield-largefield/d6_misc.py, v2-checks/w_lane_exact.py); NONE for the 10^4 random tiles"),
 ("method", "exact rational quaternion arithmetic on the tile's 12 links; 1-a(V') compared as a rational with 4sum(1-a_i) and 16max_i(1-a_i)"),
 ("falsifier", "a tile violating either inequality; an aligned ratio other than stated, or one>=16"),
 ("reach", "10^4 tiles of 16 quaternion products, seconds"))

row("YM4_04C_GATE", ("id", "G_attack"),
 ("criterion", "in the freeze commit, before any engine code, note sections 3 and 4 derive G0 and G1 in full (G0: Lemmas A and B, Finner with exponent 6, the KP test-set form with W(e_0), the BFS injection, the tail; G1: the line channel, the tree-graph bound, the KP per-polymer corollary, and the root-object bookkeeping behind c(delta)) and end with an explicit check that the proved constants are exactly the frozen ones: the scalar inequality S(eps_6*e^{2alpha+theta})<=alpha with the 6F_20(n) counts, delta_1=12alpha*e^{-4(theta-kappa)}, T=(8489/10000)*12alpha*e^{-8theta}, 2delta'<=kappa/2 with delta'=delta*e^delta, and c(delta); a second seat attacks both and files the attack; an unrepaired gap, or a proved constant that differs from a frozen one, makes every row and clause that rests on it read UNSUPPORTED, whatever its arithmetic; a repair or a corrected constant is filed as appended rows"),
 ("rests_on_G0_and_G1", "C07, C08, C11, C12, C13, C14, C16, and the replacement clause of C17"),
 ("rests_on_G0", "the injection clause of C01 (G0(c)), C09 (T), and the readout_grid_128 value of C19"),
 ("rests_on_G1", "the c(delta_in) comparisons of C10b and C10c, and the delta_crit_surrogate edge of C19"),
 ("meaning_only_through_G0", "C04, C05, C06, C15, and C19's iteration_cap_400 and missing_tail reads: their arithmetic is DERIVED whatever G0 says, and they speak about H_1 only through G0"),
 ("rests_on_neither", "C02, C03, C10 (a lower bound on any valid G1), C18, and the W lane"))

row("YM4_04C_GATE", ("id", "G_nofloat"),
 ("criterion", "every engine and check file passes scripts/no_float_gate.py and the compiled gate; rational enclosures with outward dyadic rounding; the scratch scripts of the disclosure row are not engines and are not evidence"))
row("YM4_04C_GATE", ("id", "G_grids"),
 ("criterion", "the engine and the check use exactly the pinned grids (theta, beta, delta_crit^-, alpha) and series lengths of the certificates row; a read on another grid, or a fallback such as a smaller n_max, is filed as a new appended row, never as an edit"))
row("YM4_04C_GATE", ("id", "G_replay"),
 ("criterion", "two runs write the same receipt byte for byte; CI pins the receipt sha256 and the frozen prefix, head -n 41 of this file piped to sha256sum, which covers lines 1-41 and so every frozen row; later rows, attempts and corrections go after line 41"))

row("YM4_04C_LEDGER",
 ("DERIVED_relied_on", "YM4-03 Theorem 4 and Proposition 2; YM4-03C Lemmas A, B, C and its polymer form of e^{beta*a} with t_n=I_n/I_1; YM4-04A global remainder (beta<=1/(8N_p), proved at b=3 by a Cauchy argument that does not use b)"),
 ("MEASURED_relied_on", "the YM4-03C coefficient table through beta^10 (receipt 76dc01b7), the source of P_10"),
 ("REPORTED_relied_on", "Kotecky-Preiss, Commun. Math. Phys. 103 (1986) 491-498 (G0, G1); Finner, Ann. Probab. 20 (1992) 1893-1901 (C02); Hoeffding's lemma, W. Hoeffding, J. Amer. Statist. Assoc. 58 (1963) 13-30 (C10c); Watson's G_3(0), Quart. J. Math. Oxford 10 (1939) 266-276 (W01); the Fuss-Catalan count F_D(n)=C(Dn,n)/((D-1)n+1) of n-node subtrees of the complete D-ary tree that contain the root, Graham, Knuth and Patashnik, Concrete Mathematics, 2nd ed. (1994), the generalized binomial series (G0(c))"),
 ("TO_BE_DERIVED_in_the_freeze_note", "G0 and G1 (sections 3 and 4); F_20(n+1)/F_20(n) increasing to mu for all n (L08); the limit A_b/b->G_3(0) (section 10)"),
 ("CONDITIONAL_here", "G0, G1, and every row or clause listed under gate G_attack"),
 ("OPEN_after_this_step", "an averaging map for SU(2); nonlinear small-field bounds at weak coupling; a renormalized large-field bound from rho_{k+1}; the effective-coupling recursion (Delta_beta=(11/(3pi^2))ln2 per halving); the crossover from beta_0 near 0.02; relevant counterterms; a growth bound for Lemma-B-closed sets below mu; W06's whole-zone covering certificate; uniformity over infinitely many weak-coupling steps; YM4-05; YM4-06"),
 ("full_ledger", "rows L01-L28 of note section 11"))

frozen_rows = [r for r in ROWS]
n_lines = len(frozen_rows) + 1
row("PREDICTION_SUMMARY",
 ("lines", f"{n_lines}"),
 ("rows", "28 PREDICT rows"), ("lane_S", "21 (C01-C19, C10b, C10c)"), ("lane_W", "7 (W01-W07)"), ("gates", "4"),
 ("other_rows", "9 (PREDICTION, HYPOTHESIS, CERTIFICATES, THEOREMS, W_HYPOTHESIS, SCOPE, DISCLOSURE, LEDGER, this SUMMARY)"),
 ("rows_predicting_a_NOT_MET", "14: C04, C05, C06, C10, C11, C12, C13, C14, C15, C19 (its 4 planted false claims: C_0 crude MET at 1/50; the head-free self-map MET at 1/50; r_2=r_1 for the line map; the averaged corner equal to the line corner), W01, W04 (a reproduction row), W05, W07"),
 ("conditional_on_G0_and_G1", "C07, C08, C11, C12, C13, C14, C16, C17's replacement clause"),
 ("conditional_on_G0", "C01's injection clause, C09, C19's readout_grid_128 value"),
 ("conditional_on_G1", "C10b's and C10c's c(delta_in) comparisons, C19's delta_crit_surrogate edge"),
 ("meaning_only_through_G0", "C04, C05, C06, C15, C19's iteration_cap_400 and missing_tail reads"),
 ("prefreeze_CROSS_READ", "C01 (census), C03, the C03 heads of C06, C08, C09, C12 and C14, C17 (counts), W04 (float, reproduction), W06 (b)"),
 ("prefreeze_COMPUTED", "C01 (F_20), C02, C04, C05, C06, C07, C08, C09, C10 (norm counts), C10b, C10c (constants), C11, C12, C13, C14, C15, C16, C17 (1/(8N_p)), C19 (faulted values), W01, W02, W03, W05, W07 (aligned ratios)"),
 ("prefreeze_NONE", "row C18; clauses: C01's A_c(n) count, C09's 5-7-plaquette exclusion, C10's holonomy reads, C10b's and C10c's moment reads, C19's engine exits, W06 (a), W07's random tiles"),
 ("predictions_confirmed_count", "may include only the prefreeze_NONE row and clauses; every CROSS_READ or COMPUTED value counts as a reproduction"),
 ("pin", f"head -n {n_lines} docs/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp piped to sha256sum covers lines 1-{n_lines}, every frozen row including this summary; appended rows start at line {n_lines + 1}"),
 ("frozen_before_engine", "YES, in the commit that also carries note sections 3 and 4 and the two manifests"))

assert len(ROWS) == n_lines
with open(OUT, "w") as fh:
    fh.write("\n".join(ROWS) + "\n")
print(OUT, len(ROWS), "lines")
