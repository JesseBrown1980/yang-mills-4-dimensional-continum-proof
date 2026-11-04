# Tampers with one prediction row at a time, in a scratch copy, and reads whether the test notices, and whether the workflow's hash step would. json=0.
import hashlib, os, re, shutil, subprocess, sys

ROOT = "C:/tmp/opus55/site-sign-attack-20261103"
SRC_TEST = ROOT + "/mut/tests/base_groups_lattices_exhaustive_torus_route_witnesses_side.py"
PRED = "PREDICTION-YM4-02c-SITE-SIGN.hbp"
EARL = "PREDICTION-YM4-02c.hbp"
PINNED = "f73ee43fb6164d2603679cbf01d9814b7fa7ae63574f050d37608be702176929"
pred = open(ROOT + "/repl/docs/" + PRED, "rb").read().decode("utf-8")
earl = open(ROOT + "/repl/docs/" + EARL, "rb").read().decode("utf-8")

# The selectable copy of the unmutated test, built by the harness
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutate
path0 = mutate.build([], "base_for_pred")
text0 = open(path0, encoding="utf-8", newline="\n").read()

CASES = [
    ("p01_patterns_2O", PRED, "group=2O|order=48|inversion_closed_classes=8|patterns=256|homomorphisms_to_{+1,-1}=2|constant_patterns=4", "group=2O|order=48|inversion_closed_classes=8|patterns=256|homomorphisms_to_{+1,-1}=1|constant_patterns=2", "groups"),
    ("p02_side_one_384", PRED, "w_1,-1,1,1,1=negative_on_384", "w_1,-1,1,1,1=negative_on_385", "side_one"),
    ("p03_side_one_corner", PRED, "negative_for_s(-1)=-s(1)=24_of_64", "negative_for_s(-1)=-s(1)=40_of_64", "side_one"),
    ("p04_twist", PRED, "lattice=(Z/2)^3:S=+1:negative_plaquettes=2", "lattice=(Z/2)^3:S=+1:negative_plaquettes=4", "zeros_light"),
    ("p05_su2", PRED, "weight=a_p|lattice=(Z/2)x(Z/2)|exact", "weight=a_p|lattice=(Z/2)x(Z/3)|exact", "su2"),
    ("p06_method", PRED, "lattices=(Z/2)x(Z/2),(Z/2)x(Z/3),(Z/2)^3", "lattices=(Z/2)x(Z/2),(Z/2)x(Z/3)", "summary"),
    ("p07_rule", PRED, "S_constant_iff_the_pattern_is_plus_or_minus_a_homomorphism", "S_constant_iff_the_pattern_is_a_homomorphism", "summary"),
    ("p08_class_pairs", PRED, "class_pairs=320,192,192,320,1024,1024,1024", "class_pairs=320,192,192,320,1024,1024,1023", "side_one"),
    ("p09_earlier_case4", EARL, "case_4=w_3,2,1,-1,2:sign_is_a_homomorphism_0:negative_product_above_0", "case_4=w_3,2,1,-1,2:sign_is_a_homomorphism_0:negative_product_0", "exhaustive"),
    ("p10_limits_gate", PRED, "gate=no_float_gate_draft_with_exponents_proven", "gate=none", "groups"),
    ("p11_limits_integers", PRED, "integers_only=1", "integers_only=0", "groups"),
    ("p12_teeth", PRED, "sabotage=drop_the_cycle:a_cube_with_one_negative_face_is_accepted_and_a_named_check_fails", "sabotage=none", "groups"),
    ("p13_falsifiers", PRED, "a_false_step_in_the_proof", "a_true_step_in_the_proof", "summary"),
    ("p14_first_row", PRED, "written_before_any_control_of_this_file_runs=1", "written_before_any_control_of_this_file_runs=0", "groups"),
    ("p15_zeros_S", PRED, "every_configuration_with_all_plaquettes_central|negative_S=0", "every_configuration_with_all_plaquettes_central|negative_S=1", "zeros_static"),
]

for mid, which, old, new, sel in CASES:
    base = ROOT + "/mut/pred/" + mid
    os.makedirs(base + "/tests", exist_ok=True)
    os.makedirs(base + "/docs", exist_ok=True)
    p, e = pred, earl
    if which == PRED:
        assert p.count(old) == 1, mid
        p = p.replace(old, new)
    else:
        assert e.count(old) == 1, mid
        e = e.replace(old, new)
    open(base + "/docs/" + PRED, "wb").write(p.encode("utf-8"))
    open(base + "/docs/" + EARL, "wb").write(e.encode("utf-8"))
    tp = base + "/tests/t.py"
    open(tp, "w", encoding="utf-8", newline="\n").write(text0)
    lines = p.encode("utf-8").split(b"\n")
    pin_ok = hashlib.sha256(b"\n".join(lines[:15]) + b"\n").hexdigest() == PINNED
    if sel == "zeros_static":
        print("MUTPRED|id=%s|sel=heavy_row_read_by_reading_the_source|hash_step_catches=%d|json=0" % (mid, 1 if pin_ok is False else 0))
        continue
    env = dict(os.environ)
    env["SEL"] = sel
    r = subprocess.run(["python3", "-I", "-X", "utf8", tp], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, creationflags=0x00004000, cwd=base + "/tests", timeout=600)
    out = r.stdout.decode("utf-8", "replace")
    failed = re.findall(r"^FAILED\|check=([^|]*)\|", out, flags=re.M)
    print("MUTPRED|id=%s|file=%s|sel=%s|exit=%d|test_named_failures=%d|first=%s|hash_step_catches=%d|json=0" % (mid, which, sel, r.returncode, len(failed), failed[0] if failed else "none", 1 if pin_ok is False else 0))
    sys.stdout.flush()
print("MUTPRED_DONE|json=0")
