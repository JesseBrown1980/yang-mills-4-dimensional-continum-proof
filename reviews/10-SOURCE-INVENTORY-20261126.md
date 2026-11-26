# Review 10 source inventory

The floating-point scripts for review 10 stay outside the integer proof repository, following the review 09 convention. No no-float exception is introduced. They are kept in the Claude project "Yang mills" under `reviews/10-*`.

| File | SHA-256 |
|---|---|
| 10-common.py | 4c965c13e06b1cf6c6dca85ea0da9eb9575bc867d2bfd430c644e0d27646505d |
| 10-ref_adv.py | f6aab33a47e1f647456cc405c1694575c98d7d04dc3f9df950c723b9fc2d044d |
| 10-ref_bianchi.py | 78e319e6d9eff03ebed120b12f127752fdac61eef22f336b5a3401955e118cec |
| 10-stat.py | 4801367822e478350dbdc5c877e5cecbe3943105791be86a008f993742051f47 |
| 10-witness_kappa.py | 2e536f792d4d1c64175723b0d6a9aa0d94e676ff401430b6f81533b978257bf0 |

**Dependencies:** the review 09 modules `09-bgH.py` and `09-bg_gen.py` (hashes in `09-SOURCE-INVENTORY-20261126.md`), `07-vol14d_bloch_crosscheck.py`, and `HZoff.npy` from `08-d2_xcheck.py`.

**Not committed:** the raw run results (project file `reviews/10-results.json`) and the stationary witness `Ustar_0.03.npy`. Every number in the review comes from those runs and is floating point, not a certificate.

Review 09's scope line has been corrected from "eight" to "ten" backgrounds, as the review 09 inventory noted.
