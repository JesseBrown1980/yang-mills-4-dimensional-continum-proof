#!/usr/bin/env python3
"""Builds the final PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp from the v2 builder's rows plus the overrides below.
One row per line, KIND|key=value|...|json=0, spaces written as underscores (the v2 normalization). Packaging only: every
number below comes from pkg/recompute/final_s_lane.out, pkg/recompute/c09_neighbours.out or an earlier lane's output.
Run: python3 -I build_prediction_final.py"""
import hashlib
import os

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(PKG, "PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp")
V2_SHA = "b48e29d39f76eac50e54b285548ac4131b97ace05cab9e315463fcce4f20d30f"
DRAFT_SHA = "dbce1a28ff666f2a6a4706dd34ac7e4e59ab99637d887428525cc1f44f3d6140"
MAN1_SHA = "0013abbb52fcc1dce351613afac5058ea07acb27a778db6856b439826df52873"
MAN2_SHA = "e1ace0fa52a8a529c02ca99ff00bf54f3047094469664e3cdbb629c7eb320a94"
man3 = os.path.join(PKG, "MANIFEST-ym4c-pkg.sha256")
MAN3_SHA = hashlib.sha256(open(man3, "rb").read()).hexdigest()
MAN3_LINES = sum(1 for _ in open(man3))
assert hashlib.sha256(open(os.path.join(PKG, "PREDICTION-v2.hbp"), "rb").read()).hexdigest() == V2_SHA


def norm(k, v):
    assert "|" not in v and "\n" not in v, (k, v)
    if k == "direction":
        return v
    v = " ".join(v.split())
    for a, b in ((", ", ","), ("; ", ";"), (": ", ":")):
        v = v.replace(a, b)
    return v.replace(" ", "_")


# ---- the v2 rows, as structured data
V2 = []


def row(kind, *kv):
    V2.append([kind, [list(x) for x in kv]])


src = open(os.path.join(PKG, "v2-build", "build_prediction_v2.py")).read()
body = src.split('row("YM4_04C_PREDICTION",', 1)[1].split("frozen_rows = [r for r in ROWS]")[0]
ns = {"row": row, "DRAFT_SHA": DRAFT_SHA, "MAN1_SHA": MAN1_SHA, "MAN2_SHA": MAN2_SHA}
exec('row("YM4_04C_PREDICTION",' + body, ns)


def key_of(r):
    kind, kv = r
    for k, v in kv:
        if k == "id":
            return kind + ":" + v
    return kind


ROWS = {key_of(r): r for r in V2}
ORDER = [key_of(r) for r in V2]


def setf(rk, k, v, after=None):
    kv = ROWS[rk][1]
    for x in kv:
        if x[0] == k:
            x[1] = v
            return
    assert after is not None, (rk, k)
    i = [x[0] for x in kv].index(after)
    kv.insert(i + 1, [k, v])


def delf(rk, k):
    kv = ROWS[rk][1]
    n = len(kv)
    kv[:] = [x for x in kv if x[0] != k]
    assert len(kv) == n - 1, (rk, k)


# ======================= row 1: PREDICTION =======================
R = "YM4_04C_PREDICTION"
setf(R, "version", "final, the v2 draft of 2026-11-09 carried to the constants proved in note sections 3 and 4: delta_1 and T carry the factor 6 (G0), C_k is lambda(delta)<=kappa with the factor c_fin(delta) (G1), and every value that depends on them is recomputed in exact arithmetic; neither the 40-line draft nor v2 was committed, so these 41 lines carry the final constants in their own rows and nothing is appended")
setf(R, "supersedes", f"the uncommitted scratch file scratchpad/ym4c/pkg/PREDICTION-v2.hbp, 41 lines, sha256 {V2_SHA}, which superseded the uncommitted draft synth/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp, 40 lines, sha256 {DRAFT_SHA}")
setf(R, "lane", "synthesis of the polymer-norm, small-large-field and coupling-flow design lanes under three judges, repaired after the final critic; G0 and G1 derived by two routes each, attacked by three second-seat lenses each, and merged into canonical sections; the final values recomputed")
setf(R, "symbols", "the Kotecky-Preiss pair is (alpha,theta): a(gamma)=alpha*#off(gamma), d(gamma)=theta*#gamma, d(X)=theta*n(X) for a cluster X, theta in {1/4+i/64}; at step k>=1, #gamma:=(1/2)#line(supp gamma); a is (1/2)Re Tr only; b is the blocking factor only; kappa is the norm weight 1/4 only; delta'=delta*e^delta and lambda(delta)=delta'+ln(1+delta'); c_fin is G1's final factor; lambda means lambda(delta) only, so W02's direction index is rho and W06's eigenvalue variable is y; the fine lattice spacing is h_0; the W-lane momentum is q, with p=q*e_nu and t_W=tan(q/2); the W-lane small-field parameter is p_SF; the W06 twist is t_tw; the one-loop coupling step per halving is Delta_beta; t is G1's tree-graph parameter and t_n=I_n/I_1 the character ratios; bare mu is 20^20/19^19, and mu, nu as subscripts or polarizations are directions")
setf(R, "read_rule", "a row reads MET when the engine and the independent check both compute its predicted values; a row with predicts_NOT_MET names a certificate, self-map or hypothesis predicted to fail, and reads MET only when it fails where predicted; a row or clause tagged CONDITIONAL reads UNSUPPORTED when gate G_attack finds an unrepaired gap in what it rests on, or a proved constant that differs from the one in this file; every failed read stays in this file and the note")
setf(R, "tags", "DERIVED (proved here or in a cited repo note), CONJECTURE, OPEN, MEASURED (an exact count or integral actually computed), REPORTED (from the literature, with a citation); CONDITIONAL_G0, CONDITIONAL_G1 and CONDITIONAL_G0_G1 mark a row or clause whose values are values of a G0 or G1 formula, or which states an H_k claim through them; a value marked TG rests on G1's (1+t)^f tree-graph step, which no second seat has read, and carries its fallback under 2delta'<=kappa; role names CONTROL, NEGATIVE_CONTROL, G1_TEST or REPRODUCTION")

# ======================= row 2: HYPOTHESIS =======================
R = "YM4_04C_HYPOTHESIS"
setf(R, "lattices", "fine Lambda_0=(Z/N)^4, N=2^K*L_K, L_K>=4, K>=2, spacing h_0 (G0 needs only N even and N>=8); scale-k lattice Lambda_k=(Z/(N/2^k))^4, spacing 2^k*h_0")
setf(R, "H_k(kappa,delta_k),k>=1", "log rho_k(V)=const_k+sum_Y R_k(Y;V), Y over finite sets of scale-k links with #Y>=4 that contain a closed loop, each R_k(Y;.) real, bounded, measurable, invariant under every gauge transformation of Lambda_k and a function of V restricted to Y; norm_kappa(R_k):=sup_l sum_{Y containing l} e^{kappa*#Y}*sup_V abs(R_k(Y;V))<=delta_k; no Wilson term is kept outside sum_Y R_k(Y): the plaquette coupling beta_k:=2c_1/2(P), with c_1/2(P) the chi_1/2(V_P) Haar projection of log rho_k, is carried by the R_k(Y) with Y containing the boundary of P, and abs(beta_k)<=(16/(3pi))e^{-4kappa}delta_k<0.62454delta_k (note Lemma 4.22); at k=1 the filling cluster puts 2t_2(beta_0)^4 chi_1/2(V_P) inside R_1(boundary of P)")
setf(R, "admissible", "beta_0 with C_0 MET and lambda(delta_1)<=kappa, equivalently delta_1<=delta_crit:=sup{delta: lambda(delta)<=kappa} in [0.114846768,0.114846769] (TG; fallback 2delta'<=kappa, delta_crit in [0.111780108,0.111780109]); the read is MET when delta_1^+<=delta_crit^-=0.114846768 and NOT_MET when delta_1^->delta_crit^+=0.114846769; c_fin<1 holds on the whole domain (note Lemma 4.17)")
setf(R, "constants", "kappa=1/4; D=20; 6 plaquettes per link (Finner exponent 6); #W(e_0)=12 (geometry); the test set W'(l), the 6 off links at the midpoint m_l, #W'(l)=6; F_20(n)=C(20n,n)/(19n+1); mu=20^20/19^19 in [53.00068,53.00069]; E_abs(chi_1/2)=8/(3pi) in [0.8488263,0.8488264], <=8489/10000; n_max=10")
setf(R, "uniformity", "no step bound involves N, K or the number of plaquettes; C16's oscillation readout is a bound per final torus")
setf(R, "regime", "strong bare coupling, beta_0<=0.02074 on the 10^-5 grid: C14's edge with the C03 counts (CONJECTURE on C03, CONDITIONAL_G0_G1), equivalently C_0 MET and lambda(delta_1)<=kappa; beta_0=0.02075 lies outside, where C14 predicts the self-map NOT_MET for every count vector N(4..10)>=0 while the refined C_0 is still MET (C06); with the crude counts the boundary is beta_0<=0.01767 (C13, TG, fallback 0.01761); inside the window the certified flow runs to the trivial fixed point (Haar, beta=0)")

# ======================= row 3: CERTIFICATES =======================
R = "YM4_04C_CERTIFICATES"
setf(R, "C_0(beta_0)", "eps:=eps_6(beta_0), the L^6(SU(2)) norm of K; x:=eps*e^{2alpha+theta}; S(x):=sum_{n=4..10}N(n)x^n+sum_{n=11..48}6F_20(n)x^n+6F_20(49)x^49/(1-mu*x), defined for mu*x<1; a head is valid when N(n)>=N_w(n) for every off link w and 4<=n<=10, N_w(n) the number of polymers of n plaquettes that hold w; crude: N(n):=6F_20(n), valid (note Corollary 3.12); head-free: N(n):=0, not valid, a lower limit on delta_1 for every valid head (note Remark 3.34); refined: N(n):=the C03 counts; C_0 is MET iff for some grid theta there is a rational alpha with S^+(eps^+*e^{2alpha+theta})<=alpha<=1/4; the cap 1/4 never binds, since a certified root is at most 1/8 (note Lemma 3.31)")
setf(R, "reading_rule", "a C_0 read uses eps^+>=eps, x^+>=eps^+*e^{2alpha+theta} and mu^+>=mu, tests mu^+*x^+<1 first and reads NOT_MET when it fails, puts 1-mu^+*x^+ in the tail denominator and rounds every other operation upward (note Lemma 3.30)", after="alpha_search")
setf(R, "outputs", "delta_1:=min over certified (alpha,theta) of 6alpha*e^{-4(theta-kappa)}, attained at theta=kappa=1/4 (note Lemma 3.31); readout: c_1/2(P) in 2t_2(beta_0)^4+-T, T:=(8489/10000)*6alpha*e^{-8theta} minimized over certified (alpha,theta)")
setf(R, "C_k(delta_k),k>=1", "delta':=delta_k*e^{delta_k} and lambda(delta_k):=delta'+ln(1+delta'); in C_k the Kotecky-Preiss pair is alpha=t=delta' and theta=kappa, with #gamma:=(1/2)#line(supp gamma); MET iff lambda(delta_k)<=kappa; output delta_{k+1}<=c_fin(delta_k)*delta_k, c_fin(delta):=max{e^{-4kappa}, e^{delta+lambda-5kappa}, e^{delta-kappa/2}*sup_{f>=4}(e^{-(kappa-lambda)f}-e^{-kappa*f})}, the sup a maximum at floor(f*) or ceil(f*), f*=ln(kappa/(kappa-lambda))/lambda, when lambda<kappa; c_fin(delta)=e^{-4kappa} for 0<delta<=0.078733761")
setf(R, "self_map", "MET iff lambda(delta_k)<=kappa; then c_fin(delta_k)<=max{e^{-4kappa}, e^{delta_k-kappa/2}}<1 (note Lemma 4.17), and delta_{k+j}<=c_fin(delta_k)^j*delta_k for every j and sum_j delta_{k+j}<=delta_k/(1-c_fin(delta_k)), since c_fin is nondecreasing (note Lemma 4.19, Corollary 4.20)")
setf(R, "fallback", "if the second seat rejects G1's (1+t)^f tree-graph step, route A's bookkeeping with 2delta'<=kappa applies: domain delta<=0.111780108, factor e^{-4kappa} for delta<=0.077320139; the rows marked TG give their fallback values", after="grids")
setf(R, "status", "the scalar inequality S(eps_6*e^{2alpha+theta})<=alpha with a valid head, delta_1=6alpha*e^{-4(theta-kappa)}, T=(8489/10000)*6alpha*e^{-8theta}, lambda(delta)<=kappa and c_fin(delta) are the constants proved in note sections 3 and 4, each of which ends with a constants table against the draft; gate G_attack, a second seat on the final sections, is OPEN")

# ======================= row 4: THEOREMS =======================
R = "YM4_04C_THEOREMS"
setf(R, "G0", "step 0: YM4-03C Lemmas A and B; Finner's inequality with exponent 6, sup_V abs(z_gamma)<=eps_6^{#gamma}; the per-link condition (KP_w): sum_{gamma: w in off(gamma)} omega(gamma)e^{alpha*#off(gamma)}<=alpha, omega(gamma)=sup_V abs(z_gamma)e^{theta*#gamma}, with a(gamma)=alpha*#off(gamma)<=2alpha*#gamma and d(gamma)=theta*#gamma; the cluster bounds through the Penrose partition and the rooted-tree recursion (note Proposition 3.18, DERIVED; Kotecky-Preiss a cross-reference); the test set W'(l), #W'(l)=6 (W(e_0) meets every holding polymer at least twice); the BFS injection into the complete 20-ary tree and the Fuss-Catalan tail; #Y''(gamma)<=#gamma and V-dependence only at size>=4; hence C_0=>H_1(kappa,delta_1) with delta_1=6alpha*e^{-4(theta-kappa)} and the readout T")
setf(R, "G1", "step k: Y-objects in L^infinity; Lemma A for every invariant integrand; the exact line channel (factor e^{-kappa*#Y/2}<=e^{-4kappa}, #Y>=8); the tree-graph bound T(e)<=t from sum_{o containing e} nu_o(1+t)^{s(o)}<=t at off links, s(o)=#off(o), t=delta'; the Kotecky-Preiss per-polymer corollary sum_{X containing Gamma} abs(Phi(X))e^{d(X)}<=abs(z_Gamma)e^{a(Gamma)+d(Gamma)}, d(X) summed over the polymers of X, with alpha=t=delta' and theta=kappa; root-object bookkeeping with roots that hold a line link; hence lambda(delta)<=kappa=>H_{k+1}(kappa,c_fin(delta)delta)")
setf(R, "status", "both DERIVED in note sections 3 and 4, in the freeze commit and before any engine code; G0 rests on REPORTED Finner, the exponential formula for connected graphs, Weyl's integration formula, completeness of the characters and Schur orthogonality; G1 on the REPORTED Kotecky-Preiss theorem (Commun. Math. Phys. 103, 1986); each section ends with a constants table against the draft; three second-seat lenses per theorem read the two derivation routes before the repair (note section 16); gate G_attack, a second seat on the final sections, is OPEN")
setf(R, "ties_to_exact_data", "C09 (G0, low power); C10 (every representation, from below; G1's c_fin=e^{-4kappa} is optimal for delta<=0.078733761); C10b (G1's multi-object channel: per-root slack in [289.07,289.08], slice slack in [2426.1,2426.2] at s=1/2000); C10c (G1's single-object channel through off links: per-root slack in [4.0902,4.0908], slice slack in [6.5944,6.5953] at s=1/65536)")

# ======================= row 6: SCOPE =======================
R = "YM4_04C_SCOPE"
setf(R, "NOT_MET_above_the_windows", "a failure of this norm, these counts and this bookkeeping: the C_0 reads are set by the 6F_20(n) tail beyond the head, Fuss-Catalan growth mu in [53.00068,53.00069] per plaquette, against closed-set growth (N(10)/N(8))^{1/2}=(19/2)^{1/2} in [3.08,3.09] and (N(12)/N(10))^{1/2}=(1163/152)^{1/2} in [2.76,2.77] per plaquette (CONJECTURE on C03), and the self-map reads by G1's bookkeeping; not evidence of a phase transition, a vanishing gap or anything about the theory")
setf(R, "windows", "beta_ind^crude in [0.01767,0.01768) (TG; fallback [0.01761,0.01762)), beta_crude in [0.01904,0.01905), beta_ind in [0.02074,0.02075), beta_stop in [0.02075,0.02076), beta_wall(1/4) in [0.02247,0.02248]; all below the YM4-04B Dobrushin reach 1/18, and below 9 percent of one one-loop step Delta_beta=(11/(3pi^2))ln2 in [0.2575118,0.2575119] per halving of the spacing")
setf(R, "not_claimed", "a renormalized trajectory with beta(h_0)->infinity as h_0->0; relevant counterterms (the certified plaquette coupling is irrelevant-like: its leading term 2*beta^4/128=beta^4/64 comes from the MEASURED series P_10); the crossover from beta_0 near 0.02 to the scaling region; Balaban's small-field and large-field estimates; an averaging map for SU(2); the coupling recursion or asymptotic freedom; a continuum or infrared limit; OS reconstruction; a mass gap; that the true contraction equals the certified one; that the certified class says anything about UV completeness of the theory; a weak-coupling H_k, which must carry the Wilson term outside the polymer norm (note Lemma 4.22); anything for other kappa, b or d")

# ======================= row 7: DISCLOSURE =======================
R = "YM4_04C_DISCLOSURE"
setf(R, "prefreeze_checks", "the numbers of this file were fixed by scratch scripts that are not engines and not evidence, listed below by directory; a path that starts with pkg/ is under scratchpad/ym4c/, a path that starts with v2-checks/ is under scratchpad/ym4c/pkg/, derive_checks.py is the freeze commit's reviews/ym4-04c-prediction/derive_checks.py, and every other script path is under scratchpad/ym4-04c/")
setf(R, "derive_lanes", "pkg/derive/{G0-a-checks,G0-a-kp,G0-b-checks}.py, pkg/derive/g1a/{g1a_constants,g1a_edges,g1a_treegraph_toy}.py and pkg/derive/g1b/{g1b_constants,g1b_derived,g1b_edges,g1b_sharp}.py with their .out files: the two routes of G0 and of G1", after="v2_repair")
setf(R, "attack_lanes", "pkg/attack/{G0-kp-checks,G0-kp-surrogate,G0-count-checks,G0-count-cross,G0-count-cubes,G0-count-orbits,G0-count-sixcube,G0-assembly-checks,G1-channel-checks,G1-channel-instances,G1-channel-slice}.py, pkg/attack/g1st/{g1st_brackets,g1st_constants,g1st_duality,g1st_geometry}.py and pkg/attack/g1tg/{g1tg_constants,g1tg_literal_d,g1tg_mge1,g1tg_power}.py with their .out files: the six second-seat lenses", after="derive_lanes")
setf(R, "repair_lanes", "pkg/repair/{G0-repair-checks,G1-repair-checks,G1-repair-edges-extra,G1-repair-treegraph-toy}.py with their .out files: the canonical sections' reads", after="attack_lanes")
setf(R, "final_recompute", "pkg/recompute/final_s_lane.py and c09_neighbours.py with their .out files, in Fractions with 256-bit outward dyadic rounding: every value that depends on the factor 6, on lambda(delta)<=kappa or on c_fin, the theta grid scanned in full at the six C09 couplings, and the C09 index gaps against the engine's dyadic resolution", after="repair_lanes")
setf(R, "freeze_checks", "reviews/ym4-04c-prediction/derive_checks.py (note section 14), integers and Fractions only, 54 checks, 0 failed; it reads C10b's moment identity at one rational configuration, so that clause is COMPUTED", after="final_recompute")
setf(R, "float_runs", "floats enter arithmetic only in coupling-trajectory/d4_direct_float_sanity.py, judge-engineer/slf_ct_sanity.py and synth/r12_float_sanity.py (numpy sanity runs), judge-cft/spot.py and eps6_exact.py (float eps_6 spot checks), referee/check_sl_ct.py and final-check/wlane.py (float alias sums), polymer-norm/contraction.py, coupling-trajectory/d9_window.py and pkg/derive/g1a/g1a_constants.py (a float only to choose a scan length or a rounding grid, then certified exactly), and pkg/repair/G0-repair-checks.py (Machin's Gaussian-integer identity in Python complex numbers, exact for these integers, redone in integer pairs by derive_checks.py); everywhere else floats appear in display only")
setf(R, "cross_reads", "C03's counts (judge-engineer/closed_sets.py, rerun through n=10 on both lattices by synth/closed_sets_copy.py, and through n=10 on fine (Z/8)^4 and (Z/10)^4 by pkg/attack/G0-count-checks.py); C01's census (polymer-norm/geometry_check.py, the judge prototype and pkg/attack/G0-count-checks.py); W06(b) (exact inertia, smallfield-largefield/d2_fiber_k0.py); W04 (float runs, so W04 is a reproduction row); these are reproduction reads, not blind predictions")
for x in ROWS[R][1]:
    if x[0] == "corrections_in_v2":
        assert x[1].count("the regime boundary is beta_0<=0.01959") == 1
        x[1] = x[1].replace("the regime boundary is beta_0<=0.01959", "the regime boundary is beta_0<=0.01959 (superseded below)")
setf(R, "corrections_in_final", "delta_1 and T halve (the factor 6 of G0); C_k becomes lambda(delta)<=kappa and c becomes c_fin (G1); C11's C_1 and crude self-map become MET; C12's every-count-model NOT_MET clauses are withdrawn; the regime boundary moves to beta_0<=0.02074 and the crude boundary to 0.01767; C19's planted claim 'the head-free self-map MET at 1/50' became true and is replaced by 'C_0 head-free MET at 0.02076'; the C09 resolution is lost between 1/700 and 1/600; C03's '>2000' holds only from n=8; C09's exclusion and C10's every-representation floor are DERIVED in the note; the two field keys that held '=' are renamed k_at_least_1; W02's direction index lambda and W06's eigenvalue variable lambda are renamed rho and y", after="corrections_in_v2")
setf(R, "manifests", f"scratchpad/ym4c/pkg/MANIFEST-ym4-04c-scratch.sha256: 67 lines of path and sha256, every file of scratchpad/ym4-04c/ except bytecode caches, sha256 {MAN1_SHA}; scratchpad/ym4c/pkg/MANIFEST-ym4c-v2-checks.sha256: 19 lines, every file of scratchpad/ym4c/pkg/v2-checks/, sha256 {MAN2_SHA}; scratchpad/ym4c/pkg/MANIFEST-ym4c-pkg.sha256: {MAN3_LINES} lines, every file of scratchpad/ym4c/ except bytecode caches, the three manifests, the packaging directory pkg/assemble/ and the deliverables of the freeze commit (this file, the note, derive_checks.py, DERIVE-CHECKS.hbp, ledger_rows-final.txt, engine_plan-final.txt), sha256 {MAN3_SHA}; the scratchpad is ephemeral, so the freeze commit carries the three manifests and every file they list under reviews/ym4-04c-prediction/, the design-lane tree as ym4-04c/ and the package tree as ym4c/")
setf(R, "recomputed", "C07, C08, C09, C10b, C10c, C11, C12, C13, C14, C16, C17 and C19, and the HYPOTHESIS, CERTIFICATES, THEOREMS, SCOPE, GATE G_attack, LEDGER and SUMMARY rows; every recomputed value carries prefreeze=COMPUTED with pkg/recompute/final_s_lane.py named", after="manifests")

# ======================= PREDICT rows =======================
P_ = "PREDICT:"
R = P_ + "C01"
setf(R, "statement", "on fine (Z/8)^4 and (Z/12)^4 with the b=2 lines (a line link has every coordinate other than its direction even): every link lies in 6 plaquettes; every plaquette has 2 or 4 off links; the off-link adjacency graph of fine plaquettes has maximum degree D=20 and minimum degree 10; for every line link e_0 the 6 plaquettes through it hold #W(e_0)=12 distinct off links, and exactly 6 of them, one per plaquette, end at the midpoint m_l (the test set W'(l)); every off link lies in 0 or 1 coarse filling; the Lemma-B-closed off-link-connected sets of at most 4 plaquettes are exactly the coarse fillings; A_c(n):=the number of off-link-connected sets of n plaquettes, closed or not, that hold a given off link of class c (c=the number of its odd transverse coordinates); a BFS injection into the complete 20-ary tree gives A_c(n)<=6F_20(n) (note Lemma 3.9); a plaquette with 4 off links has 20=F_20(2) neighbours, against F_19(2)=19, the per-root count at n=2 that catches degree_19")
setf(R, "predicted", "6 plaquettes per link; off links per plaquette in {2,4}; D=20, minimum 10; #W=12 and #W'=6 for every line link; on (Z/8)^4: 2048 line links, 6144 off links with one odd transverse coordinate (each in exactly one filling), 6144 with two and 2048 with three (in no filling), so 8192 in no filling and 6144 in one; closed sets of at most 4 plaquettes: the fillings only, none with 3 or fewer; A_c(n)<=6F_20(n) for n=1..5, c=1,2,3, on both lattices, with 6F_20(1..5)=6,120,3540,123240,4705470 and A_c(1)=6, an inequality only, no count frozen; F_20(4..12)=20540,784245,31763004,1340246340,58281448940,2593593086150,117544525178080,5406686759963586,251754316822792420; F_20(n+1)/F_20(n) strictly increasing and below mu, mu in [53.00068,53.00069], read for n<=59 and proved for every n (note Lemma 3.11)")
setf(R, "tag", "DERIVED for the census, the F_20 values and the ratios (note Lemmas 3.1, 3.10, 3.11); the injection inequality A_c(n)<=6F_20(n) is note Lemma 3.9, a step of G0: CONDITIONAL_G0 for that clause")
setf(R, "prefreeze", "CROSS_READ for the census (polymer-norm/geometry_check.py, judge-engineer/closed_sets.py, pkg/attack/G0-count-checks.py); COMPUTED for F_20 and the ratios (polymer-norm/derive_estimates.py, pkg/repair/G0-repair-checks.py, derive_checks.py); NONE for the A_c(n) clause")

R = P_ + "C02"
setf(R, "prefreeze", "COMPUTED (polymer-norm/derive_estimates.py, judge-cft/eps6_exact.py, final-check/s_lane.py, pkg/repair/G0-repair-checks.py and pkg/recompute/final_s_lane.py at 1/100, 1/64 and 1/50)")

R = P_ + "C03"
setf(R, "statement", "N_c(n):=the number of Lemma-B-closed off-link-connected sets of n fine plaquettes that hold a given off link of class c, c=the number of its odd transverse coordinates (1,2,3), counted as sets, not symmetry classes: a search that deduplicates by canonical form weights each class by the number of its members that hold the link; N(n):=max_c N_c(n); read for n=4..12 on fine (Z/8)^4 and (Z/12)^4; the certificate uses n<=10, and n=11,12 are a growth readout; counting gap:=6F_20(n)/N(n)")
setf(R, "predicted", "class 1: N_1(4..12)=1,0,12,0,32,32,304,284,2326; class 2: N_2(4..12)=0,0,12,0,12,12,240,244,1640; class 3: N_3(4..12)=0,0,12,0,0,0,216,228,1242; so N(4..12)=1,0,12,0,32,32,304,284,2326; identical on the two lattices (DERIVED for n<=2N-1=15 by note Lemma 3.14, locality and the class rule); counting gap in [1.09e10,1.10e10] at n=8, [2.31e12,2.33e12] at n=10, [6.49e14,6.50e14] at n=12; N(10)/N(8)=19/2 and N(12)/N(10)=1163/152 in [7.65,7.66], against F_20(10)/F_20(8) in [2016.84,2016.85] and F_20(12)/F_20(10) in [2141.77,2141.78]")
setf(R, "tag", "CONJECTURE for the counts; the lattice identity DERIVED (note Lemma 3.14), so its read guards against code faults")
setf(R, "prefreeze", "CROSS_READ: the judge prototype judge-engineer/closed_sets.py (Python integers) read these counts through n=12 before this freeze (judge-engineer/n12.txt), synth/closed_sets_copy.py reran them through n=10 on both lattices, and pkg/attack/G0-count-checks.py through n=10 on fine (Z/8)^4 and (Z/10)^4; the engine's enumeration is separate code and the check's a third")
setf(R, "method", "closure-driven growth from the 6 plaquettes through a seed off link: a closed set may add any off-link neighbour, an open set must close its lowest open off link; prune when the open links exceed 4x(remaining size); dedup by canonical form under coarse translations x the 384 signed permutations, each class weighted by the number of its members that hold the seed link; Fuss-Catalan values exact")

R = P_ + "C04"
setf(R, "tag", "DERIVED (the arithmetic; the wall is note Corollary 3.33, and it holds at equality too); its meaning as a statement about H_1 runs through G0")
setf(R, "prefreeze", "COMPUTED (polymer-norm/derive_estimates.py, final-check/s_lane.py; the two guard reads by v2-checks/c19_missing_tail_and_x3.py and pkg/recompute/final_s_lane.py)")

R = P_ + "C06"
setf(R, "statement", "with the C03 counts as the head (n<=10) and 6F_20(n) beyond: the largest beta_0 on the 10^-5 grid at which C_0 is MET; the head-free vector (N(n)=0, n<=10) is not a valid head, and its edge bounds the edge of every valid head from above (note Remark 3.34)")

R = P_ + "C07"
setf(R, "origin", "polymer-norm C07, retagged; values carried to the final constants")
setf(R, "statement", "C_0 crude MET, delta_1:=min 6alpha*e^{-4(theta-kappa)}, C_1(delta_1) MET (lambda(delta_1)<=kappa), delta_2<=c_fin(delta_1)delta_1 and sum_{k>=1}delta_k<=delta_1/(1-c_fin(delta_1)); through G0 and G1 this maps H_0 into H_1 and H_1 into itself with a contraction")
setf(R, "predicted", "delta_1 in [0.0055222,0.0055223] (alpha=delta_1/6 at theta=1/4); lambda(delta_1) in [0.0110902,0.0110903]<=1/4; 2delta_1*e^{delta_1} in [0.0111056,0.0111057] (display); c_fin(delta_1)=e^{-1} in [0.3678794,0.3678795]; delta_2<=2.0316e-3; sum_k delta_k<=8.737e-3; self-map MET; the fallback 2delta'<=kappa gives the same values")
setf(R, "prefreeze", "COMPUTED (pkg/recompute/final_s_lane.py; pkg/repair/G0-repair-checks.py and G1-repair-checks.py; the draft's factor-12 values by polymer-norm/delta_scan3.py and contraction.py, synth/verify_core.py, final-check/s_lane.py)")
setf(R, "method", "exact rationals through the pinned certificates; c_fin(delta) by an exact maximum over integer f>=4 with a certified tail cut, with upper and lower exponential enclosures and ln(1+x) by alternating partial sums")
setf(R, "falsifier", "C_0 or C_1 read NOT_MET at 1/100; delta_1 outside its bracket; c_fin(delta_1) outside [0.3678794,0.3678795]; delta_2 above 2.0316e-3; sum_k delta_k above 8.737e-3; or gate G_attack finding an unrepaired gap or a differing constant in G0 or G1 (the row then reads UNSUPPORTED)")

R = P_ + "C08"
setf(R, "origin", "polymer-norm C08, head-free value corrected; values carried to the final constants")
setf(R, "statement", "the quantities of C07 with the C03 counts; the head-free vector gives a lower limit on delta_1 valid for every count vector N(4..10)>=0; the coarse Wilson term carried in R_1 is compared with delta_1")
setf(R, "predicted", "delta_1 in [4.7159e-6,4.7160e-6]; head-free lower limit in [4.6861e-6,4.6862e-6] (DERIVED arithmetic); lambda(delta_1) in [9.4320e-6,9.4321e-6]; c_fin(delta_1)=e^{-1}; delta_2<=1.7350e-6; sum_k delta_k<=7.461e-6; crude/refined delta_1 ratio in [1170,1172]; delta_1 is [1850,1851] times the norm 12e*c_1/2(1/100) in [2.548e-9,2.549e-9] of the coarse Wilson term it contains, where c_1/2(1/100) is read from the MEASURED series P_10 (YM4-03C receipt 76dc01b7) and is not certified here, since T/P_10 is in [6.9e3,7.0e3] at 1/100 (C09)")
setf(R, "prefreeze", "COMPUTED (pkg/recompute/final_s_lane.py, pkg/repair/G0-repair-checks.py; the draft's factor-12 values by polymer-norm/delta_scan3.py, synth/verify_core.py, final-check/s_lane.py), on CROSS_READ counts")
setf(R, "falsifier", "delta_1 outside [4.7159e-6,4.7160e-6], the head-free limit outside its bracket, c_fin outside [0.3678794,0.3678795], a ratio outside its bracket, or C_1 NOT_MET")

R = P_ + "C09"
setf(R, "origin", "polymer-norm C09, readout grid repaired, exclusion stated for clusters; values carried to the final constants")
setf(R, "statement", "c_1/2(P) in [2t_2(beta)^4-T, 2t_2(beta)^4+T], T:=(8489/10000)*6alpha*e^{-8theta} minimized over certified (alpha,theta) on the pinned grid theta<=21/4 with the C03 counts (note Proposition 3.28); every cluster other than the one-term cluster (F_P) whose coarse shadow holds the boundary of P has at least 8 plaquettes, attained by the 16 one-cube bumps, since no closed polymer of 5, 6 or 7 plaquettes holds all 8 line links of the boundary of P and a cluster of two or more polymers has at least 4+4 (note Lemma 3.26, Corollary 3.27); the interval is compared with the YM4-03C series P_10(beta)=beta^4/128-beta^6/768+beta^8/1536-467beta^10/2211840")
setf(R, "predicted", "no polymer of 5, 6 or 7 plaquettes holds all of the boundary of P at both positions; P_10 inside the certified interval at beta=1/4000, 1/2000, 1/1000; T/P_10 in [5.2e-4,5.3e-4] at 1/4000 (minimizing i=194), [8.3e-3,8.4e-3] at 1/2000 (i=150), [0.133,0.134] at 1/1000 (i=105), [0.557,0.558] at 1/700 (i=83), [1.032,1.033] at 1/600 (i=73), [6.9e3,7.0e3] at 1/100 (i=0); each minimizing index beats its neighbours by a relative gap of at least 1.9e-5, four times the engine's dyadic resolution 2^-48/alpha_- of at most 4.7e-6; so the leading coarse coupling is resolved to within 0.053 percent at 1/4000 and lost between 1/700 and 1/600, while C07 and C08 still certify H_1 at 1/100: the certificate controls the action there without resolving its leading coefficient")
setf(R, "tag", "CONDITIONAL_G0 (T is G0's readout); the T/P_10 values CONJECTURE on C03; the cluster exclusion DERIVED (note Lemma 3.26, Corollary 3.27) and read by the engine")
setf(R, "low_power", "P_10-2t_2^4=(beta^8/2048)*(1-eta) with eta in [0,4e-7] at the three beta, and T exceeds it by a factor of at least 2.1x10^12, so containment can catch only a gross centering or sign error in G0")
setf(R, "prefreeze", "COMPUTED for T/P_10 and the minimizing i (pkg/recompute/final_s_lane.py over the whole theta grid and c09_neighbours.py; the draft's factor-12 values by polymer-norm/readout.py, judge-cft/c09_grid.py, synth/verify_core.py, final-check/c09.py and pkg/repair/G0-repair-checks.py) and for P_10-2t_2^4 (v2-checks/c09_readout_tail.py); NONE for the exclusion read")

R = P_ + "C10"
setf(R, "statement", "take a scale-k input with no Wilson term, R_k(Y)=s*chi_1/2 of the fine 2x2 loop on each next-coarse plaquette P'', Y its 8 line links (4 at position 0, 4 at position 1), every other R_k=0; it blocks with no integral to R_{k+1}(boundary of P'')=s*chi_1/2(V_P''); the fine norm reads 12*abs(s)*e^{8kappa} (6 next-coarse plaquettes through each line link, sup abs(chi_1/2)=2) and the coarse norm 12*abs(s)*e^{4kappa}; by the slice bound every representation of the output has norm at least 12*abs(s)*e^{4kappa} (note Lemma 4.23, Corollary 4.24), so no valid step bound has c(delta)<e^{-4kappa} at any delta>0 and kappa>=0, in the kappa=0 norm no contraction is possible, and G1's c_fin=e^{-4kappa} is optimal for 0<delta<=0.078733761")
setf(R, "tag", "DERIVED (note Corollary 4.24, for every representation)")

R = P_ + "C10b"
setf(R, "origin", "new in the draft, judge requirement for a G1 falsifier beyond C10; comparisons carried to the final constants and to the slice and per-root bounds")
setf(R, "statement", "at scale k split each next-coarse filling into two 1x2 rectangles along the lower of its two directions and set R_k(Y)=s*chi_1/2(rectangle loop) for each, Y its 6 links (4 line links and the 2 arm links the rectangles share), every other R_k=0; each object alone integrates to a constant, and the pair shares the arm path pi; exactly, to all orders in s, log rho_{k+1}(V)=const+sum_{P''}F(chi_1/2(V_P'')), F(chi)=log c_0(2s*sqrt(2+chi)); input norm delta_in=12*abs(s)*e^{6kappa}; by the slice bound every representation of the output has norm at least 3e^{4kappa}*osc F, which the natural output attains, delta_out=3e^{4kappa}*log c_0(4s) (note Lemma 4.23); the projection bound e^{4kappa}*abs(c_P)/E_abs(chi_1/2) is valid but looser; every root of G1's own representation at a line link is a rectangle with 2 off links and 4 line links, so G1 claims delta_out<=e^{delta}q(2,4)delta_in=e^{delta-4kappa}(e^{2lambda}-1)delta_in (note Proposition 4.15)")
setf(R, "predicted", "E_pi[(chi_b+chi_t)^{2m}]=Cat_m*(2+chi_1/2(V_P''))^m and odd moments 0, for m<=6 at 4 rational coarse configurations; at s=1/2000: delta_in in [0.026890,0.026891], C_k(delta_in) MET (lambda in [0.054871,0.054872]), c_fin(delta_in)=e^{-1}, delta_out in [4.077e-6,4.078e-6], delta_out/delta_in in [1.516e-4,1.517e-4], delta_out/(c_fin*delta_in) in [4.1218e-4,4.1219e-4] (slice slack in [2426.1,2426.2]), per-root bound/delta_out in [289.07,289.08], projection lower bound in [4.00e-7,4.01e-7]; at s=1/4096: delta_in in [0.013129,0.013131], c_fin(delta_in)=e^{-1}, delta_out/delta_in in [7.40e-5,7.41e-5], slice slack in [4968.6,4968.8], per-root bound/delta_out in [274.22,274.23]")
setf(R, "tag", "DERIVED; the c_fin(delta_in) and per-root comparisons CONDITIONAL_G1")
setf(R, "low_power", "G1 is refuted here only if its multi-object bookkeeping is wrong by a factor of about 289 (per root) or 2426 (against c_fin*delta_in)")
setf(R, "prefreeze", "COMPUTED (pkg/recompute/final_s_lane.py, pkg/repair/G1-repair-checks.py; the draft's values by synth/verify_extra.py and final-check/c10b.py); COMPUTED for the moment identity, which derive_checks.py read at one rational configuration before this freeze, so the engine's moment reads count as reproductions")
setf(R, "falsifier", "an exact moment other than Cat_m(2+chi)^m; delta_out or a ratio outside its bracket; delta_out above the per-root bound or above c_fin(delta_in)*delta_in (G1 refuted)")

R = P_ + "C10c"
setf(R, "origin", "new in v2, the final critic's G1 power test; comparisons carried to the final constants and to the slice and per-root bounds")
setf(R, "name", "a single-object channel through off links: the strongest computed G1 test, per-root slack about 4.09")
setf(R, "statement", "at scale k, with rect_b and rect_t the two 1x2 rectangles of C10b in each next-coarse filling, set one object per P'': R_k(Y)=s*chi_1/2(rect_b)*chi_1/2(rect_t), Y the 10 links of the two loops (the 8 line links of the 2x2 boundary and the 2 arm links), every other R_k=0; sup abs(R_k(Y))=4abs(s), attained at U=1, so delta_in=24abs(s)*e^{10kappa}; each arm link lies in exactly one filling (C01), so log rho_{k+1}(V)=const+sum_{P''}f(chi_1/2(V_P'')), f:=log E_pi[e^{sX}], X:=chi_1/2(A*pi)*chi_1/2(pi^{-1}*B) with abs(X)<=4, pi the Haar arm path and AB the 2x2 boundary holonomy, which is V_P'' in the line gauge; leading order: E_pi[X]=chi_1/2(V_P'')/2 (Schur orthogonality: the Haar integral of tr(pi*G_1)tr(pi*G_2) is tr(G_1*G_2^{-1})/2), and sE_pi[X]<=f<=sE_pi[X]+8s^2 (Jensen and Hoeffding's lemma); by the slice bound every representation of the output has norm at least 3e^{4kappa}*osc f, attained by the natural output R_{k+1}(boundary of P'')=f-(max f+min f)/2, delta_out^nat=6e^{4kappa}*osc(f)/2 in 6e*[s-4s^2,s+4s^2] (note Lemma 4.23); every root of G1's own representation at a line link has 2 off links and 8 line links, so G1 claims delta_out<=e^{delta}q(2,8)delta_in=e^{delta-6kappa+2lambda}delta_in (note Proposition 4.15); the projection bound 6e^{4kappa}*abs(c_P)/E_abs(chi_1/2), c_P:=E[f*chi_1/2] in [s/2-4s^2*E_abs(chi_1/2), s/2+4s^2*E_abs(chi_1/2)], is valid but looser")
setf(R, "engine_computes", "with its projector integrator, the exact rationals mu_m(V):=E_pi[X^m] for m=1..6 at 7 rational coarse configurations with distinct chi_1/2(V_P'') and at 4 more under rational coarse gauge transformations, integrating the two arm links one at a time (degree<=2m<=12 per link); mu_m depends on V only through chi_1/2(V_P'') and is a polynomial of degree<=m in it (conjugation invariance and the Clebsch-Gordan expansion of chi_1/2^m, DERIVED), so the 7 values fix it and the 4 more check it; from mu_1..mu_6 the cumulants and the s^1..s^6 Taylor polynomial of f, with the tail beyond s^6 at most (1/2)sum_{m>=7}(16s)^m by the YM4-04A Cauchy argument (abs(X)<=4, so f is analytic with abs(f)<1/2 on abs(s)<=1/16); then osc(f) over chi_1/2 in [-2,2], delta_out^nat, c_P, the projection bound, and the comparisons with the per-root bound and with c_fin(delta_in)*delta_in")
setf(R, "predicted", "mu_1(V)=chi_1/2(V_P'')/2 exactly at all 11 configurations; delta_out^nat/delta_in in (e^{-3/2}/4)*[1-4s,1+4s], e^{-3/2}/4 in [0.05578254,0.05578255]; at s=1/8192: delta_in in [0.0356909,0.0356910], C_k(delta_in) MET (lambda in [0.0733078,0.0733079]), c_fin(delta_in)=e^{-1}, delta_out^nat/delta_in in [0.0557553,0.0558098], delta_out^nat/(c_fin*delta_in) in [0.15155,0.15171] (slice slack in [6.591,6.599]), per-root bound/delta_out^nat in [4.7975,4.8023], projection bound/delta_in in [0.0328285,0.0328860]; at s=1/65536: delta_in in [0.0044613,0.0044614], lambda in [0.0089526,0.0089527], c_fin(delta_in)=e^{-1}, delta_out^nat/delta_in in [0.0557791,0.0557860], delta_out^nat/(c_fin*delta_in) in [0.151623,0.151642] (slice slack in [6.5944,6.5953]), per-root bound/delta_out^nat in [4.0902,4.0908], projection bound/delta_in in [0.0328523,0.0328622]; so G1 is not refuted at either s")
setf(R, "tag", "DERIVED (mu_1, the brackets, the slice bound); the c_fin(delta_in) and per-root comparisons CONDITIONAL_G1")
setf(R, "power", "G1 is refuted here only if its per-root bound underestimates the natural norm, an error by a factor in [4.0902,4.0908] at s=1/65536 ([4.7975,4.8023] at s=1/8192), or if c_fin(delta_in)*delta_in does, a factor in [6.5944,6.5953]; C10b's per-root slack is about 289")
setf(R, "prefreeze", "COMPUTED for e^{-3/2}/4, delta_in, lambda, c_fin(delta_in), the brackets and the slacks (pkg/recompute/final_s_lane.py, pkg/repair/G1-repair-checks.py, v2-checks/c10c_constants.py and c10c_brackets.py); NONE for every mu_m; no SU(2) integral of X was computed before this freeze")
setf(R, "method", "the slice bound, DERIVED in the note (Lemma 4.23): on the slice V^g (every coarse link at 1 except V_l=g) each R(Y) with l not in Y is constant, so sum_{Y containing l} sup abs(R(Y))>=osc_g log rho(V^g)/2, and the 6 coarse plaquettes through l read chi_1/2(g); the per-root bound is the first line of note Proposition 4.15; E_abs(chi_1/2)=8/(3pi) in [0.8488263,0.8488264]; c_fin as in C07")
setf(R, "falsifier", "mu_1 other than chi_1/2(V_P'')/2 at any configuration; a mu_m that is not one polynomial of degree<=m in chi_1/2(V_P'') across the 11 configurations; delta_out^nat/delta_in or a ratio outside its bracket; delta_out^nat above the per-root bound or above c_fin(delta_in)*delta_in (G1 refuted)")

R = P_ + "C11"
setf(R, "origin", "polymer-norm C11; renamed, since under the proved constants the crude chain holds at 1/64")
setf(R, "name", "at 1/64 one crude step and the crude self-map hold")
setf(R, "statement", "at beta_0=1/64 with the crude counts: C_0, C_1(delta_1) and the self-map")
setf(R, "predicted", "C_0 crude MET with delta_1 in [0.0508265,0.0508266]; lambda(delta_1) in [0.1055724,0.1055725]<=1/4, so C_1 MET; c_fin(delta_1)=e^{-1}; delta_2<=1.8699e-2; sum_k delta_k<=8.041e-2; crude self-map MET; the draft's C_1 test 2delta'<=kappa/2 reads 2delta_1*e^{delta_1} in [0.1069532,0.1069533]<=1/8, MET too, so the draft's NOT_MET at 1/64 came from the factor 12; the refined certificate is MET here too (C14)")
delf(R, "predicts_NOT_MET")
delf(R, "role")
setf(R, "tag", "CONDITIONAL_G0_G1: the delta_1 of the C_0 clause is G0's formula, and the C_1 test and c_fin are G1's; arithmetic DERIVED; the fallback 2delta'<=kappa gives the same values")
setf(R, "prefreeze", "COMPUTED (pkg/recompute/final_s_lane.py, pkg/repair/G0-repair-checks.py; the draft's values by polymer-norm/window2.py, synth/verify_core.py, final-check/s_lane.py)")
setf(R, "falsifier", "C_0 or C_1 read NOT_MET at 1/64 with the crude counts; delta_1 outside [0.0508265,0.0508266]; c_fin(delta_1) outside [0.3678794,0.3678795]; or gate G_attack finding an unrepaired gap or a differing constant (UNSUPPORTED)")

R = P_ + "C12"
setf(R, "origin", "polymer-norm C12, head-free value corrected; renamed, since under the proved constants the refined chain holds at 1/50")
setf(R, "name", "at 1/50 the crude certificate fails while the refined chain holds")
setf(R, "statement", "at beta_0=1/50: the crude C_0, the head-free lower limit on delta_1 valid for every count vector N(4..10)>=0, and the refined C_0, C_1 and self-map")
setf(R, "predicted", "C_0 crude NOT_MET (DERIVED, since 1/50>beta_crude); head-free delta_1 in [0.0363229,0.0363230], so every count vector N(4..10)>=0 has delta_1>=0.0363229; this limit no longer forces a NOT_MET, since the draft's NOT_MET came from the factor 12; C_0 refined MET with delta_1 in [0.0363235,0.0363236], lambda(delta_1) in [0.0746422,0.0746423], c_fin(delta_1)=e^{-1}, delta_2<=1.3363e-2, sum_k delta_k<=5.7463e-2, refined self-map MET (CONJECTURE on C03); for a count vector between the C03 head and the crude one nothing is claimed")
setf(R, "predicts_NOT_MET", "C_0 crude at 1/50")
setf(R, "tag", "CONDITIONAL_G0_G1: delta_1 is G0's formula and the C_1 test and c_fin are G1's; arithmetic DERIVED; the refined clauses CONJECTURE on C03")
setf(R, "prefreeze", "COMPUTED (pkg/recompute/final_s_lane.py, pkg/repair/G0-repair-checks.py; the draft's values by referee/check_headfree.py, synth/verify_core.py, final-check/s_lane.py)")
setf(R, "method", "as C07 and C08, at 1/50, with the head-free bound as a lower limit for every count vector N(4..10)>=0")
setf(R, "falsifier", "C_0 crude read MET at 1/50; the head-free delta_1 outside its bracket; for the conjectured clauses, C_0 refined, C_1 or the refined self-map read NOT_MET, or a value outside its bracket")

R = P_ + "C13"
setf(R, "origin", "polymer-norm C13, admissibility test repaired; carried to the final C_k and c_fin")
setf(R, "statement", "delta_crit:=sup{delta: lambda(delta)<=kappa}=sup{delta: C_k(delta) MET}, and c_fin<1 on that whole domain (note Lemma 4.17); beta_ind^crude:=the largest beta_0 on the 10^-5 grid with C_0 crude MET and delta_1<=delta_crit^- (the pinned test; the design-lane surrogate delta_1<=49/1000 reads the edge at 0.01552/0.01553); G1's factor c_fin is read where it leaves e^{-4kappa}")
setf(R, "predicted", "delta_crit in [0.114846768,0.114846769]; c_fin(delta)=e^{-1} for delta<=0.078733761 and c_fin(0.078733762)>e^{-1}; c_fin(1/10) in [0.611173,0.611174] (maximizing f=9); c_fin(11/100) in [0.811310,0.811311] (f=13); c_fin(delta_crit^-) in [0.989898,0.989899]; c_fin(49/1000)=c_fin(1/20)=e^{-1}; MET at 0.01767 (delta_1 in [0.1145675,0.1145676]) and NOT_MET at 0.01768 (delta_1 in [0.1150830,0.1150831]), so beta_ind^crude in [0.01767,0.01768); beta_ind^crude<beta_crude")
setf(R, "predicts_NOT_MET", "the crude self-map at 0.01768 and above")
setf(R, "fallback", "if G1's (1+t)^f step is rejected: delta_crit in [0.111780108,0.111780109] (2delta'<=kappa), factor e^{-1} for delta<=0.077320139, and the crude edge 0.01761/0.01762", after="predicts_NOT_MET")
setf(R, "tag", "CONDITIONAL_G0_G1, arithmetic DERIVED; delta_crit, the c_fin values above 0.078733761 and the edge are TG (fallback above)")
setf(R, "prefreeze", "COMPUTED (pkg/recompute/final_s_lane.py, pkg/repair/G1-repair-checks.py and G1-repair-edges-extra.py; the draft's values by polymer-norm/induction_window.py, referee/check_ind.py, synth/verify_core.py, final-check/edges.py)")
setf(R, "method", "bisection on delta for lambda(delta)=kappa with enclosures on the 10^-9 grid; c_fin by an exact maximum over integer f>=4 with a certified tail cut; C05's procedure with the extra test delta_1<=delta_crit^-, read on both sides: MET by S^+(x^+(alpha_c))<=alpha_c at alpha_c=delta_crit^-/6, NOT_MET by g^-(alpha_c)>0 and g'^+(alpha_c)<0 at alpha_c=delta_crit^+/6, which by convexity puts the least root above alpha_c")
setf(R, "falsifier", "delta_crit outside its bracket; c_fin other than e^{-1} at or below 0.078733761, or a c_fin value outside its bracket; the edge pair read otherwise; beta_ind^crude>=beta_crude")

R = P_ + "C14"
setf(R, "origin", "polymer-norm C14, admissibility test repaired; carried to the final C_k and c_fin")
setf(R, "predicted", "MET at 0.02074 (delta_1 in [0.1088558,0.1088559]) and NOT_MET at 0.02075 (delta_1 in [0.1158911,0.1158912]), the same edge as the head-free limit; head-free delta_1 in [0.1088527,0.1088528] at 0.02074 and in [0.1158861,0.1158862] at 0.02075, so beta_ind<0.02075 for every count vector N(4..10)>=0 (DERIVED arithmetic); at 0.02075 the refined C_0 is still MET (C06), so beta_ind sits one grid step below beta_stop; at beta_0=1/64 the refined self-map is MET with delta_1 in [1.01738e-3,1.01739e-3], c_fin(delta_1)=e^{-1}, delta_2<=3.7428e-4, sum_k delta_k<=1.6095e-3; ordering beta_ind<beta_stop<beta_wall(1/4), 0.02074<0.02075<0.02247; the fallback 2delta'<=kappa gives the same edge")
setf(R, "predicts_NOT_MET", "the self-map at 0.02075 and above for every count vector N(4..10)>=0")
setf(R, "tag", "CONJECTURE on C03 and CONDITIONAL_G0_G1, the head-free clauses DERIVED arithmetic")
setf(R, "prefreeze", "COMPUTED (pkg/recompute/final_s_lane.py, pkg/repair/G1-repair-checks.py and G1-repair-edges-extra.py; the draft's values by referee/check_ind.py, synth/verify_core.py, final-check/edges.py), on CROSS_READ counts")

R = P_ + "C15"
setf(R, "tag", "DERIVED (the C04 wall test above 1/40, note Corollary 3.33; the head-free arithmetic at 1/45); the wall belongs to the 6F_20(n) tail, not to the norm; meaning as a statement about H_1 through G0")

R = P_ + "C16"
setf(R, "origin", "polymer-norm C16, first clause only; values carried to the final constants")
setf(R, "statement", "from C07, delta_m<=c_fin(delta_1)^{m-1}*delta_1 for m>=1, uniformly in N and K; on a final coarse 4^4 torus with 1024 links, osc_V log rho_m<=2*1024*e^{-4kappa}*delta_m/4=(512/e)delta_m (note Lemma 4.21); this is a bound per final torus about the certified class, which runs to the trivial fixed point, and not about UV completeness of the theory")
setf(R, "predicted", "at beta_0=1/100 with the crude constants: delta_20<=c_fin(delta_1)^19*delta_1=e^{-19}delta_1<=3.0940e-11; osc_V log rho_20<=5.828e-9 on the coarse 4^4 torus at spacing 2^20*h_0, within a factor e^{+-5.828e-9} of Haar")
setf(R, "prefreeze", "COMPUTED (pkg/recompute/final_s_lane.py, pkg/repair/G1-repair-checks.py; the draft's values by synth/verify_extra.py)")
setf(R, "falsifier", "the delta_20 bound above 3.0940e-11, the oscillation bound above 5.828e-9, or c_fin(delta_1)>=1")

R = P_ + "C17"
setf(R, "statement", "every input of C_0 and C_k (census, counts N(n), eps_6, KP sums, delta_1, c_fin) reads byte-identical on fine (Z/8)^4 and (Z/12)^4, and the count equality is DERIVED for n<=15 (note Lemma 3.14), so the byte comparison guards against code faults; the YM4-04A global route needs beta<=1/(8N_p): YM4-04A proved it at b=3, and its Cauchy argument (abs(X)<=N_p for the fine plaquette sum X=sum_p(1/2)chi_1/2(U_p), on the disk abs(z)<=1/(4N_p)) does not use the blocking factor, so the same hypothesis stands at b=2")
setf(R, "predicted", "identical receipts on the two lattices; 1/(8N_p)=1/196608 on 8^4, 1/995328 on 12^4, 1/3145728 on 16^4, ->0 as N->infinity; at beta_0=1/100 the global route certifies nothing on any lattice with N_p>=13, while C07's local certificate holds on every fine torus with even side>=8; the replacement holds only for the effective-action norm at beta_0<=0.02074 (C14's edge)")
setf(R, "prefreeze", "CROSS_READ for the counts on both lattices (synth/closed_sets_copy.py); COMPUTED for 1/(8N_p) (derive_checks.py) and for the regime value (pkg/recompute/final_s_lane.py)")

R = P_ + "C19"
setf(R, "origin", "polymer-norm C19, coupling-flow CT16, small-large-field R15; three faults pinned by exact runs in v2; the surrogate and grid-128 values and one planted claim carried to the final constants")
setf(R, "statement", "each planted fault stops the engine on its named check with exit 1: finner_exponent_2 (eps_6 replaced by the L^2 norm)->G_finner_guard, which reads the maximal off-link incidence of the 10-plaquette filling-plus-cube set, 4, and tests sum 1/q<=1, which reads 2>1; a comparison of numbers on that set would not catch it, since there sup abs(z)=(2t_2)^10/64 at leading order lies below the false product; degree_19 (D=19)->C01; missing_tail (S replaced by the head-only polynomial sum_{n=4..10}N(n)x^n with the C03 head: the terms n=11..48 and the n=49 tail removed)->C04, whose guard then reads the refined C_0 MET at 1/40 and at 0.02248 (alpha=2^-22 certifies, with S^+<=1.96e-7 and <=1.28e-7); one_position_support (the norm routine sets #Y to the number of links of Y at position 1, the links that carry V in the line gauge (1,V), in place of all links of Y)->C10, fine norm 12abs(s)e^{4kappa} and ratio 1 in place of e^{-1} at kappa=1/4; global_norm (sum over all Y in place of Y containing l)->C17, 8^4 and 12^4 differ; readout_without_tail (T:=0)->C09 containment, since P_10-2t_2^4=(beta^8/2048)*(1-eta) with eta in [0,4e-7] at the three beta; iteration_cap_400 (at every grid theta the convex search and the exact read are replaced by the iteration alpha_0=0, alpha_{j+1}=s_j:=S^+(up(eps_6^+*e^{2alpha_j+theta})), read MET at the first j with s_j<=alpha_j*(1+10^-40) and NOT_MET when s_j is undefined or above 1/4, or after 400 evaluations of S^+)->C05, MET lost at 0.01902, 0.01903 and 0.01904, so the faulted crude edge reads 0.01901/0.01902; delta_crit_surrogate (delta_1<=49/1000 in place of delta_1<=delta_crit^-)->C13, MET lost at 0.01553-0.01767 (TG; fallback 0.01553-0.01761), so the faulted crude edge reads 0.01552/0.01553; readout_grid_128 (theta cut at i<=128)->C09, T/P_10 in [1.47e-2,1.48e-2] at 1/4000 (minimizing i=128); drop_alias_terms (aliases with n_perp ne 0 dropped)->W01, corner r_1=2 in place of 15/28; longitudinal_read_unflagged->W05; float_literal in any engine file->G_nofloat; planted false claims, read by the same reader from a planted copy of this file: C_0 crude MET at 1/50; C_0 head-free MET at 0.02076; the line-map corner k-independent (r_2=r_1); the averaged corner equal to the line corner")
setf(R, "predicted", "12 of 12 faults stop on their named checks with exit 1; 4 of 4 planted claims read NOT_MET, with the misses at C12, C06, 25823/98640 ne 15/28 and 2 ne 15/28; the unplanted run exits 0 and its receipt is byte-identical across two runs")
setf(R, "tag", "DERIVED for the faulted values, by exact runs; the delta_crit_surrogate edge rests on G0's delta_1 and G1's test (CONDITIONAL_G0_G1) and the readout_grid_128 value on G0's T (CONDITIONAL_G0)")
setf(R, "prefreeze", "COMPUTED (final-check/faults.py, fault_judge.py, fault_dl.py; v2-checks/c19_iteration_cap.py, c19_missing_tail_and_x3.py, c19_one_position.py, c09_readout_tail.py; judge-cft/c09_grid.py; polymer-norm/window2.py; pkg/recompute/final_s_lane.py for the surrogate edge and readout_grid_128); NONE for the engine's exits")

for wid, extra in (("W01", "derive_checks.py for r_1, r_2(pi), A_1, A_2 and A_3"), ("W03", "derive_checks.py for the d=2 closure, the d=3 profile, corners, slopes and increments"),
                   ("W05", "derive_checks.py for the transverse and longitudinal ratios"), ("W07", "derive_checks.py for the aligned ratios")):
    R = P_ + wid
    kv = ROWS[R][1]
    for x in kv:
        if x[0] == "prefreeze":
            x[1] = x[1].rstrip(")") + ", " + extra + ")" if x[1].endswith(")") else x[1] + "; COMPUTED also by " + extra
            break

# ======================= gates =======================
R = "YM4_04C_GATE:G_attack"
setf(R, "criterion", "note sections 3 and 4 derive G0 and G1 in full and end with constants tables against the draft; three second-seat lenses per theorem attacked the two derivation routes before the repair and filed their verdicts (G0: Kotecky-Preiss GAP, counting GAP, assembly GAP, each on the factor 6; G1: tree-graph GAP, channel HOLDS, structure HOLDS; note section 16); the repaired sections carry the proved constants, and this file carries them; the gate stays OPEN until a second seat of the owner's choosing attacks the final sections 3 and 4 as written, G1's (1+t)^f tree-graph step and its root restriction m>=1 included, and files the attack; an unrepaired gap, or a proved constant that differs from the one in this file, makes every row and clause that rests on it read UNSUPPORTED, whatever its arithmetic; a repair or a corrected constant is filed as appended rows after line 41; no engine code before the filing")
setf(R, "rests_on_G0_and_G1", "C07, C08, C11, C12, C13, C14, C16, the replacement clause of C17, the regime clause of the hypothesis row, and the delta_crit_surrogate edge of C19")
setf(R, "rests_on_G0", "the injection clause of C01 (note Lemma 3.9), C09 (T), and the readout_grid_128 value of C19")
setf(R, "rests_on_G1", "the c_fin(delta_in) and per-root comparisons of C10b and C10c, and C13's delta_crit and c_fin values")
setf(R, "rests_on_the_(1+t)^f_step", "delta_crit, C13's c_fin values above 0.078733761 and its crude edge, the crude window of the scope row, and the upper end of C19's surrogate range; each carries its fallback under 2delta'<=kappa", after="rests_on_G1")
setf(R, "rests_on_neither", "C02, C03, C10 (a lower bound on every representation), C18, and the W lane")

R = "YM4_04C_GATE:G_nofloat"
setf(R, "criterion", "every engine and check file passes scripts/no_float_gate.py and the compiled gate; rational enclosures with outward dyadic rounding; derive_checks.py checks its own source for float literals, true division and negative powers before it runs; the scratch scripts of the disclosure row are not engines and are not evidence")

# ======================= ledger =======================
R = "YM4_04C_LEDGER"
setf(R, "DERIVED_relied_on", "YM4-03 Lemma 3, Theorem 4 and Proposition 2; YM4-03C Lemmas A, B, C and its polymer form of e^{beta*a} with t_n=I_n/I_1; YM4-04A global remainder (beta<=1/(8N_p), proved at b=3 by a Cauchy argument that does not use b); note sections 3 and 4: G0 and G1, with Proposition 3.18 (the cluster bounds), Lemmas 3.9-3.11 (the injection, the Fuss-Catalan count, the ratios), Lemma 3.14 (locality and the class rule), Lemma 3.32 (monotonicity in beta_0), Corollary 3.33 (the wall) and Lemma 4.23 (the slice bound)")
setf(R, "REPORTED_relied_on", "Kotecky-Preiss, Commun. Math. Phys. 103 (1986) 491-498 (G1; a cross-reference for G0); Finner, Ann. Probab. 20 (1992) 1893-1901 (G0, C02); the exponential formula for connected graphs, Stanley, Enumerative Combinatorics vol. 2 (1999) Corollary 5.1.6 (G0); Weyl's integration formula, completeness of the characters and Schur orthogonality on SU(2), Brocker and tom Dieck, Representations of Compact Lie Groups (1985) IV.1 (G0, C10c); Hoeffding's lemma, W. Hoeffding, J. Amer. Statist. Assoc. 58 (1963) 13-30 (C10c); Watson's G_3(0), Quart. J. Math. Oxford 10 (1939) 266-276 (W01); the moments of the uniform measure on the 3-sphere (derive_checks.py); cross-references only: Graham, Knuth and Patashnik, Concrete Mathematics, 2nd ed. (1994), Dvoretzky and Motzkin (1947) and Penrose (1967), whose results note section 3 proves")
delf(R, "TO_BE_DERIVED_in_the_freeze_note")
setf(R, "DERIVED_in_the_freeze_note", "G0 and G1 (sections 3 and 4); F_20(n+1)/F_20(n) increasing to mu for all n (Lemma 3.11, L08); the limit A_b/b->G_3(0) (section 10)", after="REPORTED_relied_on")
setf(R, "CONDITIONAL_here", "every row or clause listed under gate G_attack, which stays OPEN for a second seat of the owner's choosing")
setf(R, "OPEN_after_this_step", "the formal second-seat attack of the final sections 3 and 4 (gate G_attack); an averaging map for SU(2); nonlinear small-field bounds at weak coupling; a renormalized large-field bound from rho_{k+1}; the effective-coupling recursion (Delta_beta=(11/(3pi^2))ln2 per halving); the crossover from beta_0 near 0.02; relevant counterterms; a growth bound for Lemma-B-closed sets below mu; W06's whole-zone covering certificate; uniformity over infinitely many weak-coupling steps; YM4-05; YM4-06")

# lambda now names lambda(delta) of G1, so W02's direction index and W06's eigenvalue variable are renamed
import re as _re
for rk, pairs in (("PREDICT:W02", (("n_lambda", "n_rho"), ("p_lambda", "p_rho"))),):
    for x in ROWS[rk][1]:
        for a_, b_ in pairs:
            x[1] = x[1].replace(a_, b_)
for x in ROWS["PREDICT:W06"][1]:
    if x[0] in ("statement", "predicted", "method"):
        x[1] = _re.sub(r"lambda", "y", x[1])
for rk in ("PREDICT:W02", "PREDICT:W06"):
    assert all("lambda" not in x[1] for x in ROWS[rk][1]), rk

# the two keys of the draft that held "=" are renamed, so that every field splits at its first "="
for rk, old, new in (("YM4_04C_HYPOTHESIS", "H_k(kappa,delta_k),k>=1", "H_k(kappa,delta_k),k_at_least_1"),
                     ("YM4_04C_CERTIFICATES", "C_k(delta_k),k>=1", "C_k(delta_k),k_at_least_1")):
    for x in ROWS[rk][1]:
        if x[0] == old:
            x[0] = new
            break
    else:
        raise KeyError(old)

# ======================= the summary row =======================
body_rows = [ROWS[k] for k in ORDER if k != "PREDICTION_SUMMARY"]
lines = []
for kind, kv in body_rows:
    lines.append("|".join([kind] + [f"{k}={norm(k, v)}" for k, v in kv] + ["json=0"]))
n_lines = len(lines) + 1
summary = [
    ("lines", f"{n_lines}"),
    ("rows", "28 PREDICT rows"), ("lane_S", "21 (C01-C19, C10b, C10c)"), ("lane_W", "7 (W01-W07)"), ("gates", "4"),
    ("other_rows", "9 (PREDICTION, HYPOTHESIS, CERTIFICATES, THEOREMS, W_HYPOTHESIS, SCOPE, DISCLOSURE, LEDGER, this SUMMARY)"),
    ("rows_predicting_a_NOT_MET", "13: C04, C05, C06, C10, C12, C13, C14, C15, C19 (its 4 planted false claims: C_0 crude MET at 1/50; C_0 head-free MET at 0.02076; r_2=r_1 for the line map; the averaged corner equal to the line corner), W01, W04 (a reproduction row), W05, W07"),
    ("conditional_on_G0_and_G1", "C07, C08, C11, C12, C13, C14, C16, C17's replacement clause, the hypothesis row's regime clause, C19's delta_crit_surrogate edge"),
    ("conditional_on_G0", "C01's injection clause, C09, C19's readout_grid_128 value"),
    ("conditional_on_G1", "C10b's and C10c's c_fin(delta_in) and per-root comparisons, C13's delta_crit and c_fin values"),
    ("conditional_on_the_(1+t)^f_step", "delta_crit, C13's c_fin values above 0.078733761 and its crude edge, the scope row's crude window, the upper end of C19's surrogate range, each with its fallback"),
    ("meaning_only_through_G0", "C04, C05, C06, C15, C19's iteration_cap_400 and missing_tail reads"),
    ("prefreeze_CROSS_READ", "C01 (census), C03, the C03 heads of C06, C08, C09, C12 and C14, C17 (counts), W04 (float, reproduction), W06 (b)"),
    ("prefreeze_COMPUTED", "C01 (F_20), C02, C04, C05, C06, C07, C08, C09, C10 (norm counts), C10b (values and the moment identity), C10c (constants), C11, C12, C13, C14, C15, C16, C17 (1/(8N_p) and the regime value), C19 (faulted values), W01, W02, W03, W05, W07 (aligned ratios)"),
    ("prefreeze_NONE", "row C18; clauses: C01's A_c(n) count, C09's cluster-exclusion read, C10's holonomy reads, C10c's moment reads, C19's engine exits, W06 (a), W07's random tiles"),
    ("recomputed", "C07, C08, C09, C10b, C10c, C11, C12, C13, C14, C16, C17, C19, and the HYPOTHESIS, CERTIFICATES, THEOREMS, SCOPE, G_attack, LEDGER and SUMMARY rows"),
    ("predictions_confirmed_count", "may include only the prefreeze_NONE row and clauses; every CROSS_READ or COMPUTED value counts as a reproduction"),
    ("pin", f"head -n {n_lines} docs/PREDICTION-YM4-04C-LOCAL-POLYMER-NORM-20261109.hbp piped to sha256sum covers lines 1-{n_lines}, every frozen row including this summary; appended rows start at line {n_lines + 1}"),
    ("frozen_before_engine", "YES once the owner files the freeze commit, which carries note sections 3 and 4, derive_checks.py and the three manifests; gate G_attack stays OPEN at that commit"),
]
lines.append("|".join(["PREDICTION_SUMMARY"] + [f"{k}={norm(k, v)}" for k, v in summary] + ["json=0"]))
assert len(lines) == 41
for ln in lines:
    assert " " not in ln and ln.endswith("|json=0") and ln.isascii(), ln[:80]
    for fld in ln.split("|")[1:]:
        assert "=" in fld and "=" not in fld.split("=", 1)[0] and "=" not in fld.split("=", 1)[1][:1], fld[:60]
with open(OUT, "w") as fh:
    fh.write("\n".join(lines) + "\n")
print(OUT, len(lines), "lines; MANIFEST-ym4c-pkg.sha256", MAN3_SHA, MAN3_LINES)
