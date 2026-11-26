# Review 12 adversarial-fixture inventory

The adversarial coarse-field fixture and the floating-point generators stay outside the integer proof repository, following the review 09–11 convention. No no-float exception is introduced. The package `review11-adversarial-fixture.zip` was delivered separately. Its README, SHA256SUMS, generators and JSON results are also in the Claude project "Yang mills" under `reviews/12-*`.

| File | SHA-256 |
|---|---|
| adv_v.npy | 6b82e825a1577225f5434d154385cf006f1730114fe47e93e0f93f97ceffc9c1 |
| adv_Av.npy | 359c688b01a620fd669bc169eb85fcc86890888c9be1007f0423a63609327460 |
| adv_Ustar_30.npy | c347f0efd8d97fc1272cd10bc31c00aaac91a8298d8abe244792b581d022262d |
| adv_Ustar_36.npy | bca1c7b4c7e2fb7267d56ea3559c74fa39a86a1bb9f1fcfef4591906399a7d4d |
| adv_witness_30.json | 1c867128b50b4a9e63007a671e227a4c821d7be7425a7fe8e0e21d6901004568 |
| adv_witness_36.json | 648e0ef155f4879c8255f0f20d9d600472fa984fca637d9a3212965a4e5a0ad5 |
| adv_fixture.json | c984478c42647ca49aa605845967bad1cf0d0059e3b2ea7a9e861506ce0346d7 |
| adv_fixture.py | fad686c5b55e96fcf6c5782eed7dc1c4eb8867119f90d4e82e514f85c219a8bc |
| build_adv_witness.py | 65a0e394ed34ab1142cfc3d2bb8f7df3d2b42f719617ca4e5011d4fbf5880c67 |

**Array conventions** (full detail in the package README):
- Fine side 12, lexicographic site index, link (s, μ).
- Quaternions (w, x, y, z), right exponential coordinates U·exp(x).
- Coarse link index (block index)·4 + μ.
- The U* arrays are in block-tree gauge, with tree links exactly the identity.

Every number is floating point, not a certificate.
