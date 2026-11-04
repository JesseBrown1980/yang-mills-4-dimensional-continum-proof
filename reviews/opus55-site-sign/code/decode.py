import ast, sys, re
SRC = "C:/tmp/opus55/site-sign-attack-20261103/repl/tests/test_site_sign_4d.py"
SOURCE = open(SRC, encoding="utf-8", newline="\n").read()
exec(open("mutants_auto.py", encoding="utf-8").read().split("class LCG:")[0].split("def write(tree, name):")[0].split("SOURCE = open(SRC")[0].replace("os.makedirs", "(lambda *a, **k: None)").split("for name in (")[0])
