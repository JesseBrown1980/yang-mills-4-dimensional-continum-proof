# The count on the Q8 slice (ℤ/2) × (ℤ/1)

`fixed_slice_mechanism.py` and `RECEIPT.hbp` are this seat's count of the fixed slice, read over all 4,096 configurations. [`tests/test_site_sign_4d.py`](../../tests/test_site_sign_4d.py) reads the same numbers on its own table, in the rows `SITE_SIGN_SIDE_ONE_PAIRS`, `SITE_SIGN_SIDE_ONE_HOLONOMIES` and `SITE_SIGN_SIDE_ONE_WEIGHTS`, MEASURED by that script.

**GPT-6 reproduced the counts independently with its own multiplication:** 4,096 configurations, 2,176 exact inverses, 3,712 same class, 1,024 both central, 0 and 384 negative products. NAMED, as relayed by the operator on November 3, 2026. The run is GPT-6's, and this seat holds it through that relay.

| Count | GPT-6, as relayed | `RECEIPT.hbp` |
|---|---:|---|
| Configurations | 4,096 | `configs=4096` |
| Exact inverses | 2,176 | `p1_is_inverse_of_p0=2176` |
| Same class | 3,712 | `same_class=3712` |
| Both central | 1,024 | `both_central=1024` |
| Negative products | 0 and 384 | `slice_product_negative=0` on w = 3, 2, 1, −1, −2, on 1, 1, 1, −1, −1 and on 3, 2, 1, −1, 2, and `slice_product_negative=384` on 1, −1, 1, 1, 1 |

GPT-6's review of the theorem in [the note](../../docs/NOTE-YM4-02c-SITE-SIGN.md) is preliminary, and the operator asked for its final check.
