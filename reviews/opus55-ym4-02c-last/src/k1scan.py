#!/usr/bin/env python3
"""(Z/1)x(Z/4) with an arbitrary finite group: H(x0,x1) free on the pairs of classes that a plaquette weight reaches, kernel K tensor K. Look for a weight with a zero, c_0 nonzero, some c_rho c_0 < 0, and no negative eigenvalue. Integers only, json=0. usage = k1scan.py"""
import itertools, sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from exact5 import *

def kmat(G, w):
    n = len(G.reps)
    M = G.mul; I = G.inv
    cl = G.cls
    K = [[sum(w[cl[M[M[M[G.reps[x]][v]][I[G.reps[y]]]][I[v]]]] for v in range(G.n)) for y in range(n)] for x in range(n)]
    reach = [[any(w[cl[M[M[M[G.reps[x]][v]][I[G.reps[y]]]][I[v]]]] for v in range(G.n)) for y in range(n)] for x in range(n)]
    return K, reach

def form(G, w):
    K, reach = kmat(G, w)
    n = len(G.reps)
    S = [(x, y) for x in range(n) for y in range(n) if reach[x][y]]
    return S, [[K[a][a2] * K[b][b2] for (a2, b2) in S] for (a, b) in S], K

def spectrum_signs_abelian(G, w, chars):
    return [sum(G.sizes[k] * w[k] * chars[r][k] for k in range(len(G.reps))) for r in range(len(chars))]
