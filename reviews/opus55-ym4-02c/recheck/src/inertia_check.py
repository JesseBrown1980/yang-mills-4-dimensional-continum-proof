#!/usr/bin/env python3
"""Recheck of YM4-02c at c32087a. The builder's inertia_exact, read from the script text, against char-poly inertia (second seat's helper) on seeded integer symmetric matrices, with many zero diagonals so that the congruence branch runs. No row of the script enters that branch. Standard library, integers only, json=0."""
import ast
import sys
sys.path.insert(0, "C:/tmp/opus55/attack-4d-02c-20261103/src")
from exact import charpoly, inertia_from_charpoly

SOURCE = open(r"C:/tmp/opus55/recheck-02c-20261103/run/t.py", encoding="utf8").read()
tree = ast.parse(SOURCE)
func = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "inertia_exact")
namespace = {}
exec(compile(ast.Module(body=[func], type_ignores=[]), "inertia_exact", "exec"), namespace)
inertia_exact = namespace["inertia_exact"]

state = 20261104


def below(n):
    global state
    state = (state * 6364136223846793005 + 1442695040888963407) % (1 << 64)
    return (state >> 33) % n


trials, disagree, branch_ready, crash = 0, 0, 0, 0
first = None
for size in range(1, 9):
    for _ in range(1500):
        style = below(4)
        m = [[0] * size for _ in range(size)]
        for i in range(size):
            for j in range(i, size):
                v = below(7) - 3
                if style == 0 and i == j:
                    v = 0
                if style == 1 and below(3):
                    v = 0
                if style == 2:
                    # low rank: a sum of two signed rank-one terms
                    v = 0
                m[i][j] = m[j][i] = v
        if style == 2:
            a = [below(5) - 2 for _ in range(size)]
            b = [below(5) - 2 for _ in range(size)]
            s = 1 if below(2) else -1
            m = [[a[i] * a[j] + s * b[i] * b[j] for j in range(size)] for i in range(size)]
        trials += 1
        if all(m[i][i] == 0 for i in range(size)) and any(any(r) for r in m):
            branch_ready += 1
        want = inertia_from_charpoly(charpoly(m))
        try:
            pos, neg, rank = inertia_exact(m)
        except AssertionError:
            crash += 1
            if first is None:
                first = ("assert", m)
            continue
        if (pos, neg, rank) != (want[0], want[1], want[0] + want[1]):
            disagree += 1
            if first is None:
                first = ((pos, neg, rank), want, m)
print("INERTIA_EXACT|trials=%d|zero_diagonal_nonzero_matrices=%d|disagree_with_char_poly=%d|assertion_failures=%d|first=%s|json=0" % (trials, branch_ready, disagree, crash, first))
print("INERTIA_EXACT_CONTROLS|[[0,1],[1,0]]=%s|triangle=%s|zero=%s|json=0" % (inertia_exact([[0, 1], [1, 0]]), inertia_exact([[0, 1, 1], [1, 0, 1], [1, 1, 0]]), inertia_exact([[0, 0], [0, 0]])))
