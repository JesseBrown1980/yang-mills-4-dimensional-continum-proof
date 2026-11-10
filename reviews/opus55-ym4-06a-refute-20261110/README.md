# Independent refutation of PR #47 (YM4-06A): filed evidence

This folder holds the independent refuter's (opus55) files for YM4-06A, unedited. This README is a separate filing note: the manifest does not list it, and it changes none of the 44 files.

## Provenance

- `original_git_commit=NOT_APPLICABLE`: the refuter generated the 44 files outside Git, in `C:/tmp/opus55/ym4-06a-refute/`.
- **Manifest:** [`REFUTER-MANIFEST.hbp`](REFUTER-MANIFEST.hbp) records each file's original path, byte count and full SHA-256.
  - sha256 `58353d3c172c86b5bd52bc769758dc56ca44fec8c0a224085ed87ea0067bbb15`.
  - Committed alone, before any refuter file, in commit `77062d804865c684eec1dfe57a0b0d271855d895`.
  - The refuter's clone `repo/` and its patched `probe/` copies are excluded.
- **Scope of the manifest:** it fixes an integrity baseline as of its creation (2026-11-10, `built_utc=2026-11-10T13:42:04Z`). The files' earlier creation history is outside what it records.
- **One rename, bytes unchanged:** `aux.hbp` is filed as `aux_output.hbp`, because AUX is a reserved device name on Windows ([`FILED.hbp`](FILED.hbp)).
- **Reproducibility:** the refuter's code and receipts replay with the preserved files unmodified, through wrappers only.
  - [`tests/ym4_06a_verify_refuter_manifest.sh`](../../tests/ym4_06a_verify_refuter_manifest.sh) checks every file's path, byte count and full sha256 against the manifest, and the manifest's own sha256 against the value above.
  - The CI job [`.github/workflows/ym4-06a-global-lock.yml`](../../.github/workflows/ym4-06a-global-lock.yml) reruns `refute_support_lemma.py`, and `refute_s3.py` at budget 7 on 2×2×2, 2×2×3, 2×3×3, 3×3×3 and 3×3×4, against the filed outputs.
