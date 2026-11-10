#!/usr/bin/env bash
# Wrapper for YM4-06A review evidence: verifies every filed refuter file against REFUTER-MANIFEST.hbp (path, byte count, full
# sha256), checks the manifest's own sha256 against the value recorded in the PR body (argument 1), and that the folder holds
# nothing the manifest does not list apart from the filing extras. The evidence files are never edited.
# usage: tests/ym4_06a_verify_refuter_manifest.sh MANIFEST_SHA256
set -euo pipefail
d=reviews/opus55-ym4-06a-refute-20261110
m="$d/REFUTER-MANIFEST.hbp"
want="$1"
got=$(sha256sum "$m" | cut -c1-64)
if [ "$got" != "$want" ]; then echo "FAILED|check=manifest_sha256|got=$got|want=$want|json=0"; exit 1; fi
n=0
listed=" REFUTER-MANIFEST.hbp FILED.hbp "
while IFS='|' read -r tag path bytes sha _; do
  [ "$tag" = REFUTER_FILE ] || continue
  p=${path#path=}; b=${bytes#bytes=}; h=${sha#sha256=}
  t="$p"
  # AUX is a reserved device name on Windows; the file is filed under this name with its bytes unchanged (FILED.hbp)
  [ "$p" = aux.hbp ] && t=aux_output.hbp
  f="$d/$t"
  if [ ! -f "$f" ]; then echo "FAILED|check=missing|path=$p|json=0"; exit 1; fi
  if [ "$(wc -c < "$f")" -ne "$b" ]; then echo "FAILED|check=bytes|path=$p|json=0"; exit 1; fi
  if [ "$(sha256sum "$f" | cut -c1-64)" != "$h" ]; then echo "FAILED|check=sha256|path=$p|json=0"; exit 1; fi
  listed="$listed$t "
  n=$((n + 1))
done < "$m"
grep -qx "REFUTER_MANIFEST_END|files=$n|json=0" "$m" || { echo "FAILED|check=manifest_count|files=$n|json=0"; exit 1; }
for f in "$d"/*; do
  b=$(basename "$f")
  case "$listed" in *" $b "*) ;; *) echo "FAILED|check=unlisted|path=$b|json=0"; exit 1 ;; esac
done
echo "REFUTER_MANIFEST_CHECK|manifest_sha256=$got|files=$n|path_bytes_sha256_all_match=1|unlisted=0|json=0"
