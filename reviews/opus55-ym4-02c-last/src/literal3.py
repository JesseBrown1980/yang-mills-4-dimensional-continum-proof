#!/usr/bin/env python3
"""A literal Gram for two more PSD weights of the k=2 family, against the orbit route. Integers only, json=0."""
import sys
sys.path.insert(0, "C:/tmp/opus55/recheck-02c-20261103/last/src")
from literal import *
print(run_q8((0, 3, 0, 0, 1), (1, 1, 4)), flush=True)
print(run_q8((0, 3, 1, 0, 0), (1, 1, 4)), flush=True)
