#!/usr/bin/env python3
"""The twelve sabotages and an unknown name, as the workflow lists them, with each exit code, each named check and a search for a traceback. Integers only, json=0."""
import subprocess
import sys

R = r"C:/tmp/opus55/recheck-02c-20261103"
SCRIPT = sys.argv[1] if len(sys.argv) > 1 else R + "/run/t.py"
NAMES = [
    ("no_inverse_on_time_links", "reflection_"), ("wrong_plane", "reflection_"), ("wrong_multiplicity", "l_n_coefficients"),
    ("negative_weight_called_positive", "GRAM_LINK"), ("signed_site_weight_called_positive", "positive_site_weight_control"),
    ("bad_projector", "Tr(A_B_P)"), ("no_inverse_in_gram", "gauge-moved_site_Gram"), ("wrong_plane_in_gram", "gauge-moved_site_Gram"),
    ("dropped_inverse_third_letter", "plaquette_orientation"), ("dropped_inverse_fourth_letter", "plaquette_orientation"),
    ("every_function_one_plane", "every_function_on_L="), ("t4_half_weights_dropped", "every_function_at_T=4"),
]
for name, named in NAMES:
    p = subprocess.run([sys.executable, "-I", "-X", "utf8", SCRIPT, "sabotage=" + name], capture_output=True)
    out = p.stdout.replace(b"\r", b"").decode("utf8")
    failed = [ln.split("check=")[1].split("|")[0] for ln in out.splitlines() if ln.startswith("FAILED|")]
    hit = any(f.startswith(named) for f in failed)
    tb = "Traceback" in out or b"Traceback" in p.stderr
    print("SABOTAGE|name=%s|exit=%d|failed=%d|named_check_hit=%d|traceback=%d|checks=%s|json=0" % (name, p.returncode, len(failed), 1 if hit else 0, 1 if tb else 0, ",".join(failed)))
p = subprocess.run([sys.executable, "-I", "-X", "utf8", SCRIPT, "sabotage=no_such_name"], capture_output=True)
print("SABOTAGE|name=no_such_name|exit=%d|json=0" % p.returncode)
