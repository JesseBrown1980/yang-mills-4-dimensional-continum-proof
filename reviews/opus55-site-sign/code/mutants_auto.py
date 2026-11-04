# A seeded sweep of operator and constant mutations over the test's source tree, outside the two long loops of section_zeros_central.
# Each mutant runs the sections its function feeds, at below-normal priority, and is compared to the unmutated run of those sections. json=0.
import ast, copy, os, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

ROOT = "C:/tmp/opus55/site-sign-attack-20261103"
SRC = ROOT + "/repl/tests/test_site_sign_4d.py"
MUT = ROOT + "/mut/auto/tests"
os.makedirs(MUT, exist_ok=True)
os.makedirs(ROOT + "/mut/auto/docs", exist_ok=True)
for name in ("PREDICTION-YM4-02c-SITE-SIGN.hbp", "PREDICTION-YM4-02c.hbp"):
    open(ROOT + "/mut/auto/docs/" + name, "wb").write(open(ROOT + "/repl/docs/" + name, "rb").read())

SOURCE = open(SRC, encoding="utf-8", newline="\n").read()

TAIL = '''

def _dual_only():
    lat = Lattice(2, 2, 2)
    width, faces = len(lat.links), lat.faces
    dimension, span, in_kernel = flat_cochains(lat)
    cubes = cube_masks(lat)
    colour = dual_two_colouring(lat)
    bipartite = colour is not None
    even_cubes = [mask for x, mask in zip(lat.sites, cubes) if bipartite and colour[x] == 0]
    one_of_each = all(sum(1 for mask in cubes if (mask >> f) & 1) == 2 and sum(1 for mask in even_cubes if (mask >> f) & 1) == 1 for f in range(len(faces)))
    six_faces = all(mask.bit_count() == 6 for mask in cubes)
    link_faces = [sum(1 << f for f, face in enumerate(faces) if l in face) for l in range(width)]
    link_even_in_cubes = all((mask & faces_of_link).bit_count() % 2 == 0 for mask in cubes for faces_of_link in link_faces)
    odd_side = Lattice(2, 2, 3)
    odd_bipartite = dual_two_colouring(odd_side) is not None
    print("DUAL_ONLY|%d|%d|%d|%d|%d|%d|%d|%d|ok=%d" % (dimension, len(span), flag(in_kernel), flag(six_faces), flag(one_of_each), flag(bipartite), flag(link_even_in_cubes), flag(odd_bipartite), check("dual lattice", six_faces and one_of_each and bipartite and link_even_in_cubes and not odd_bipartite and in_kernel and dimension == 10)))


WITNESS_BOUND = 1 << 13
_order = ["groups", "lattices", "exhaustive", "torus_route", "witnesses", "side_one", "second_seat", "su2", "summary"]
_sel = os.environ.get("SEL", ",".join(_order)).split(",")
for _name in _order:
    if _name in _sel:
        globals()["section_" + _name]()
if "zeros_light" in _sel:
    q = group("Q8")
    section, section_ok = q8_section(q)
    print("ZEROS_SECTION|%d|ok=%d" % (flag(section_ok), check("projection of Q8", section_ok)))
    section_zeros_control(q, section)
    section_zeros_twist(q)
if "zeros_dual" in _sel:
    _dual_only()
finish()
'''

ALL_SECTIONS = "lattices,exhaustive,torus_route,witnesses,side_one,second_seat,su2"
SEL_OF = {
    "Ring": "groups,exhaustive", "negate": "groups,exhaustive", "signed": "groups", "doubled_product": "groups,witnesses", "conjugate": "groups,witnesses", "norm": "groups",
    "q8_elements": "groups", "hurwitz_extra": "groups", "octahedral_extra": "groups", "icosahedral_extra": "groups", "Group": "groups,exhaustive,witnesses", "group": "groups", "joined": "groups",
    "section_groups": "groups", "Lattice": ALL_SECTIONS, "lattice_name": "lattices,witnesses", "face_value": ALL_SECTIONS, "parity_of": "torus_route,witnesses", "sign_on": "exhaustive,torus_route,witnesses",
    "values_of_s": "exhaustive,side_one", "lattice_facts": "lattices,second_seat", "section_lattices": "lattices", "Stream": "witnesses,second_seat,su2", "spanning_tree": "exhaustive,torus_route,zeros_light",
    "gauge_moved": "witnesses", "mask_of_weight": "exhaustive,side_one,second_seat", "section_exhaustive": "exhaustive", "section_torus_route": "torus_route", "exact_classes": "witnesses", "direct_s": "witnesses",
    "predicted_constant": "witnesses", "read_witnesses": "witnesses", "section_witnesses": "witnesses,summary", "section_side_one": "side_one", "section_second_seat": "second_seat",
    "f2_kernel": "zeros_light,zeros_dual", "flat_cochains": "zeros_light,zeros_dual", "q8_section": "zeros_light", "cube_masks": "zeros_dual", "dual_two_colouring": "zeros_dual", "section_zeros_control": "zeros_light",
    "section_zeros_twist": "zeros_light", "reduced_quaternion": "su2", "rational_product": "su2", "rational_inverse": "su2", "real_parts": "su2", "plain_real_parts": "su2", "product_of_pairs": "su2", "section_su2": "su2",
    "section_summary": "summary", "imported_modules": "summary", "finish": "summary", "check": "groups", "flag": "groups", "in_row": "exhaustive,side_one,summary", "read_rows": "groups",
}

SWAP = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt, ast.In: ast.NotIn, ast.NotIn: ast.In}
BIN = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.BitXor: ast.BitOr, ast.BitAnd: ast.BitOr, ast.BitOr: ast.BitXor, ast.Mult: ast.Add, ast.RShift: ast.LShift, ast.LShift: ast.RShift, ast.FloorDiv: ast.Mult}


def sites(tree):
    out = []
    for top in tree.body:
        name = getattr(top, "name", None)
        if name not in SEL_OF:
            continue
        for node in ast.walk(top):
            if isinstance(node, ast.Compare) and type(node.ops[0]) in SWAP:
                out.append((name, node, "cmp"))
            elif isinstance(node, ast.BinOp) and type(node.op) in BIN and not isinstance(node.left, (ast.JoinedStr,)) and not (isinstance(node.left, ast.Constant) and isinstance(node.left.value, str)):
                out.append((name, node, "bin"))
            elif isinstance(node, ast.BoolOp):
                out.append((name, node, "bool"))
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
                out.append((name, node, "not"))
            elif isinstance(node, ast.Constant) and type(node.value) is int:
                out.append((name, node, "const"))
    return out


def apply(node, kind):
    if kind == "cmp":
        node.ops[0] = SWAP[type(node.ops[0])]()
        return "comparison swapped"
    if kind == "bin":
        node.op = BIN[type(node.op)]()
        return "operator swapped"
    if kind == "bool":
        node.op = ast.Or() if isinstance(node.op, ast.And) else ast.And()
        return "and/or swapped"
    if kind == "not":
        node.op = ast.Invert() if False else node.op
        node.operand = ast.UnaryOp(op=ast.Not(), operand=node.operand)
        return "not removed"
    if kind == "const":
        node.value = node.value + 1
        return "constant plus one"
    raise ValueError(kind)


def write(tree, name):
    tree.body = [t for t in tree.body if not (isinstance(t, ast.Expr) and isinstance(t.value, ast.Call) and getattr(t.value.func, "id", "") == "main")]
    text = ast.unparse(tree) + "\n" + TAIL
    path = MUT + "/" + name + ".py"
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return path


def run(path, sel, timeout):
    env = dict(os.environ)
    env["SEL"] = sel
    t0 = time.perf_counter_ns()
    try:
        r = subprocess.run(["python3", "-I", "-X", "utf8", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, creationflags=0x00004000, cwd=MUT, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, "", "", timeout * 1000
    return r.returncode, r.stdout.decode("utf-8", "replace").replace("\r\n", "\n"), r.stderr.decode("utf-8", "replace").replace("\r\n", "\n"), (time.perf_counter_ns() - t0) // 10 ** 6


class LCG:
    def __init__(self, s):
        self.s = s

    def below(self, n):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        return (self.s >> 33) % n


tree0 = ast.parse(SOURCE)
all_sites = sites(tree0)
print("AUTO_SITES|total=%d|json=0" % len(all_sites))
per_fn = {}
for i, (name, node, kind) in enumerate(all_sites):
    per_fn.setdefault(name, []).append(i)
print("AUTO_PER_FUNCTION|%s|json=0" % ",".join("%s:%d" % (k, len(v)) for k, v in sorted(per_fn.items())))
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 300
rng = LCG(20261103)
chosen = []
# stratified: a share per function in proportion to its count, at least 2 where it has them
total = len(all_sites)
for name, idx in sorted(per_fn.items()):
    share = max(2, len(idx) * LIMIT // total)
    pool = list(idx)
    for _ in range(min(share, len(pool))):
        chosen.append(pool.pop(rng.below(len(pool))))
print("AUTO_CHOSEN|mutants=%d|json=0" % len(chosen))
sys.stdout.flush()

BASE = {}
lock = threading.Lock()


def baseline(sel):
    with lock:
        if sel in BASE:
            return BASE[sel]
        path = write(ast.parse(SOURCE), "base_" + re.sub(r"\W+", "_", sel)[:50])
        rc, out, err, ms = run(path, sel, 1200)
        BASE[sel] = (rc, out)
        print("AUTO_BASE|sel=%s|exit=%s|ms=%d|lines=%d|json=0" % (sel, rc, ms, out.count("\n")))
        sys.stdout.flush()
        return BASE[sel]


results = {}


def one(i):
    name, node, kind = all_sites[i]
    sel = SEL_OF[name]
    base_rc, base_out = baseline(sel)
    tree = ast.parse(SOURCE)
    s2 = sites(tree)
    desc = apply(s2[i][1], kind)
    line = node.lineno
    source_line = SOURCE.split("\n")[line - 1].strip()[:90].replace("|", "/")
    path = write(tree, "a%04d" % i)
    rc, out, err, ms = run(path, sel, 240)
    if rc is None:
        verdict = "killed_by_timeout"
        failed, changed = [], -1
    else:
        crash = "Traceback" in err
        failed = re.findall(r"^FAILED\|check=([^|]*)\|", out, flags=re.M)
        a, b = base_out.split("\n"), out.split("\n")
        changed = sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))
        verdict = "killed_by_crash" if crash else "killed_by_named_check" if failed else "killed_by_exit" if rc != base_rc else "passes_its_checks_cmp_catches_it" if changed else "SURVIVES_identical_output"
    with lock:
        print("AUTO|site=%d|fn=%s|line=%d|kind=%s|desc=%s|verdict=%s|first=%s|changed=%d|ms=%d|src=%s|json=0" % (i, name, line, kind, desc, verdict, failed[0] if failed else "none", changed, ms, source_line))
        sys.stdout.flush()
    try:
        os.remove(path)
    except OSError:
        pass


with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(one, chosen))
print("AUTO_DONE|json=0")
