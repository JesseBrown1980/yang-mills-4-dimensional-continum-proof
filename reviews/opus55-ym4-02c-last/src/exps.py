import ast, sys
src = open(sys.argv[1], encoding="utf8").read()
t = ast.parse(src)
seen = {}
for n in ast.walk(t):
    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Pow):
        key = ast.unparse(n.right)
        seen.setdefault(key, []).append(n.lineno)
print("POW_EXPONENTS", {k: len(v) for k, v in seen.items()})
for n in ast.walk(t):
    if isinstance(n, ast.FunctionDef) and n.name == "power":
        print(ast.unparse(n)[:300])
