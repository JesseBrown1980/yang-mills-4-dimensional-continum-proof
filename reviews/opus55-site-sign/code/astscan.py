import ast, sys
src = open("C:/tmp/ym4-02c-sign-wt/tests/test_site_sign_4d.py", encoding="utf-8").read()
tree = ast.parse(src)
floats = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, (float, complex))]
truediv = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div)]
truediv += [n.lineno for n in ast.walk(tree) if isinstance(n, ast.AugAssign) and isinstance(n.op, ast.Div)]
pows = []
for n in ast.walk(tree):
    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Pow):
        pows.append((n.lineno, ast.unparse(n)))
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("pow", "float", "complex", "round", "sum") and n.func.id != "sum":
        pows.append((n.lineno, "CALL " + ast.unparse(n)))
attrs = sorted({ast.unparse(n) for n in ast.walk(tree) if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "math"})
print("AST|float_literals=%s|true_div=%s|math_attrs=%s|json=0" % (floats, truediv, attrs))
for p in pows:
    print("AST_POW|line=%d|%s|json=0" % p)
