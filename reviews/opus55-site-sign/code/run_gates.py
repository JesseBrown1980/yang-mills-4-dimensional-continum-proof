import importlib.util, sys
target = "C:/tmp/ym4-02c-sign-wt/tests/test_site_sign_4d.py"
data = open(target, "rb").read()
for label, path in (("v3_attack_copy", "C:/tmp/opus55/gate-v3-attack-20261103/gate/no_float_gate.py"), ("ym4_02b_scripts", "C:/tmp/ym4-02b-wt/scripts/no_float_gate.py"), ("gate_v4", "C:/tmp/gate-v4/no_float_gate.py")):
    spec = importlib.util.spec_from_file_location("gate_" + label, path)
    m = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(m)
    try:
        f = m.findings(data, "tests/test_site_sign_4d.py")
    except TypeError:
        f = m.findings(data, "tests/test_site_sign_4d.py", frozenset())
    print("GATE|%s|findings=%d|json=0" % (label, len(f)))
    for x in f[:30]:
        print("GATE_FINDING|%s|%s|json=0" % (label, x))
