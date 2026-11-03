# YM4-02c independent Q8 link-reflection Gram check

Source: prediction commit 0e9bcff7d0da84d90dfc8dc77579c5fb9350ac95.

The checker enumerates all 8^7=2,097,152 gauge-fixed Q8 link assignments on the 3x2 periodic lattice. It fixes 5 spanning-tree links to identity, leaves 7 links independent, computes all six oriented plaquettes, multiplies the class-function weights from the prediction, and integrates chi_2(W_t=0)*chi_2(W_t=1). Every assignment is weighted by 1/8^7. The 2D 3x2 reflection relates the two spatial Wilson lines. Results are exact integer sums and rational divisions; no floats.

The implementation uses a quaternion multiplication table derived independently; it checks all group associativity identities and inverses. No repository checker or character-sum shortcut is called.

Run: g++ -O3 -std=c++17 -Wall -Wextra -Werror q8_gram_independent.cpp -o q8check && ./q8check

Scope: exact finite-Q8 negative control only. It does not prove continuous SU2 reflection positivity, the 4D transfer identity, or a continuum mass gap.
