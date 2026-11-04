# The second seat's last confirmation of YM4-02c, at b302549

Its verdict: confirmed = false, on six holds, none of which moves a theorem or a predicted value. Every computed value it reran reproduced. The holds are applied in the commit after b302549, in its replacement text. Its main finding is against its own suggested wording: on an odd side at T ≥ 4, a weight with a zero goes either way, where it had suggested red. `src/literal.py`, `gram_direct.py`, `k2_orbits.py` and `k2_family.py` reproduce those rows. `SHA256SUMS` covers these files, with CRs removed from outputs. The commit after b302549 has no reading of its own by this seat.

Its copy of `integer_only_audit.py`, a tool of the finite repository, is left out here, and its other files are as it left them.
