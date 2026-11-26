# Review 11 source inventory

The floating-point scripts for review 11 stay outside the integer proof repository, following the review 09 and 10 convention. No no-float exception is introduced. They are kept in the Claude project "Yang mills" under `reviews/11-*`.

| File | SHA-256 |
|---|---|
| 11-d3c_check.py | 35e6aa46e381af023a63c428a9f970ae6011e74a7caa4705db600faf805f69c0 |
| 11-d3d_preview.py | dca2af4426730efb505109c64b1cb89ada4b65d88a5ea65e0d9e7a19a8de1249 |

**Dependencies:**
- review 10's `10-common.py` and `10-ref_adv.py`;
- review 09's `09-bgH.py` and `09-bg_gen.py`;
- `07-vol14d_bloch_crosscheck.py`;
- `HZoff.npy` from `08-d2_xcheck.py`;
- the stationary witness `Ustar_0.03.npy` from `10-stat.py`.

All are listed in the earlier inventories.

**Not committed:** the run logs and `d3d_preview_extra.json`. The review reproduces every iterate of the D3D preview in §3. Every number is floating point, not a certificate.
