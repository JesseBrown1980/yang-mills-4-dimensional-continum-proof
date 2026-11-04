# Hand-placed faults, one mathematical fault per mutant. Read at below-normal priority. json=0.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mutate import *

FAST = "groups,lattices,exhaustive,torus_route,witnesses,side_one,second_seat,su2,summary"
ZL = "zeros_light"

MUTANTS = [
    ("m01_hamilton_sign", "one Hamilton sign wrong", [("((0, 1, 1), (1, 0, 1), (2, 3, 1), (3, 2, -1)),", "((0, 1, 1), (1, 0, 1), (2, 3, 1), (3, 2, 1)),")], "groups"),
    ("m02_conjugate", "conjugate leaves k alone", [("return x[0], negate(x[1]), negate(x[2]), negate(x[3])", "return x[0], negate(x[1]), negate(x[2]), x[3]")], "groups"),
    ("m03_ico_odd", "2I built from odd permutations", [("if inversions % 2 == 0:", "if inversions % 2 == 1:")], "groups"),
    ("m04_no_inverse_merge", "classes not merged with their inverses", [("if partner != c and SABOTAGE != \"count_inverted_classes_apart\":", "if False:")], "groups"),
    ("m05_hom_and", "homomorphism test with and instead of xor", [("bits[m[x][y]] == bits[x] ^ bits[y]", "bits[m[x][y]] == bits[x] & bits[y]")], "groups"),
    ("m06_rule_no_minus", "rule without the minus sign", [("self.rule = sorted(self.homomorphisms + [mask ^ self.full for mask in self.homomorphisms])", "self.rule = sorted(self.homomorphisms)")], "groups,exhaustive,side_one,summary"),
    ("m07_rule_flip_bit0", "rule flips only the identity class", [("[mask ^ self.full for mask in self.homomorphisms]", "[mask ^ 1 for mask in self.homomorphisms]")], "groups,exhaustive,side_one,summary"),
    ("m08_index_no_squares", "second count of homs drops the squares", [(" | {m[x][x] for x in range(self.order)})", ")")], "groups"),
    ("m09_epsilon_plus", "epsilon always +1", [("return -1 if (mask >> self.merged_of[self.one]) & 1 else 1", "return 1")], "witnesses"),
    ("m10_constant_ignores_F", "constant at epsilon -1 taken as -1 always", [("return -1 if q.epsilon(mask) < 0 and plaquettes % 2 else 1", "return -1 if q.epsilon(mask) < 0 else 1")], "witnesses"),
    ("m11_constant_plus", "constant taken as +1 always", [("return -1 if q.epsilon(mask) < 0 and plaquettes % 2 else 1", "return 1")], "witnesses"),
    ("m12_third_letter", "plaquette third letter not inverted, in table route", [("return m[m[m[config[a]][config[b]]][inv[config[c]]]][inv[config[d]]]", "return m[m[m[config[a]][config[b]]][config[c]]][inv[config[d]]]")], FAST),
    ("m13_fourth_letter", "plaquette fourth letter not inverted, in table route", [("return m[m[m[config[a]][config[b]]][inv[config[c]]]][inv[config[d]]]", "return m[m[m[config[a]][config[b]]][inv[config[c]]]][config[d]]")], FAST),
    ("m14_shift_back", "lattice shift runs backward", [("y[mu] = (y[mu] + 1) % self.dims[mu]", "y[mu] = (y[mu] - 1) % self.dims[mu]")], FAST),
    ("m15_wrong_link_third", "third link of a face at x instead of x+nu", [("self.link_index[(self.shift(x, nu), mu)], self.link_index[(x, nu)])", "self.link_index[(x, mu)], self.link_index[(x, nu)])")], FAST),
    ("m16_wrong_link_second", "second link of a face at x instead of x+mu", [("self.link_index[(x, mu)], self.link_index[(self.shift(x, mu), nu)],", "self.link_index[(x, mu)], self.link_index[(x, nu)],")], FAST),
    ("m17_both_orders", "plaquettes also listed with mu > nu", [("for mu in range(self.k) for nu in range(mu + 1, self.k)]", "for mu in range(self.k) for nu in range(self.k) if nu != mu]")], FAST),
    ("m18_exclusive_loose", "exclusive-link check ignores the other staples", [("if not any(staple.count(x) == 1 and x not in others for x in staple):", "if not any(staple.count(x) == 1 for x in staple):")], "lattices"),
    ("m19_exclusive_always", "exclusive-link check always true", [("                exclusive = False\n", "                pass\n")], "lattices"),
    ("m20_parity_or", "parity with or", [("            parity ^= 1 << c\n        parities[parity] += 1", "            parity |= 1 << c\n        parities[parity] += 1")], "groups,exhaustive"),
    ("m21_tree_not_a_tree", "gauge-fixing set closes a Polyakov loop on (Z/2)x(Z/2)", [("    tree, frontier = [], [lat.sites[0]]\n", "    if lat.dims == (2, 2):\n        return [lat.link_index[((0, 0), 0)], lat.link_index[((1, 0), 0)], lat.link_index[((0, 0), 1)]]\n    tree, frontier = [], [lat.sites[0]]\n")], "groups,exhaustive,torus_route," + ZL),
    ("m22_tree_short", "one tree link too few", [("                    tree.append(lat.link_index[(x, mu)])\n", "                    tree.append(lat.link_index[(x, mu)]) if len(tree) < 2 else None\n")], "groups,exhaustive,torus_route," + ZL),
    ("m23_stream_shift", "stream reads other bits", [("return (self.state >> 33) % n", "return (self.state >> 20) % n")], "witnesses,second_seat,su2"),
    ("m24_exact_conj_c", "exact recheck forgets the third inverse", [("x = doubled_product(q.ring, x, conjugate(e[config[c]]))", "x = doubled_product(q.ring, x, e[config[c]])")], "witnesses"),
    ("m25_gauge_right", "gauge move forgets the inverse", [("return [m[m[gauge[s]][u]][inv[gauge[r]]] for u, (s, r) in zip(config, lat.ends)]", "return [m[m[gauge[s]][u]][gauge[r]] for u, (s, r) in zip(config, lat.ends)]")], "witnesses"),
    ("m26_torus_degree", "torus route wrong degree scaling", [("* (2 // degree) for chi, degree in zip(characters, degrees)]", "* degree for chi, degree in zip(characters, degrees)]")], "torus_route"),
    ("m27_side_centre", "up-to-centre read as same class", [("up_to_centre += 1 if c0 == c1 or cls[m[q.minus][p1]] == c0 else 0", "up_to_centre += 1 if c0 == c1 else 0")], "side_one"),
    ("m28_side_row_minus", "side row built with the s(1)=-1 value", [("corner_read, len(corner_constant), 1 << 5, at_plus[0], corner_read)", "corner_read, len(corner_constant), 1 << 5, at_minus[0], corner_read)")], "side_one"),
    ("m29_side_literal_true", "the miss hidden: literal always true", [("literal = all(count == 24 for count in at_plus + at_minus)", "literal = True")], "side_one"),
    ("m30_second_seat_w", "second seat weight off the rule", [("    lat = Lattice(2, 1, 2)\n    w = (3, 2, 1, -1, -2)\n", "    lat = Lattice(2, 1, 2)\n    w = (3, 2, 1, -1, 2)\n")], "second_seat"),
    ("m31_su2_real_part", "one sign in the quaternion product real part", [("return reduced_quaternion(a * e - b * f - c * g - d * h,", "return reduced_quaternion(a * e - b * f - c * g + d * h,")], "su2"),
    ("m32_su2_k_part", "one sign in the k part of the product", [("a * h + b * g - c * f + d * e, m * n)", "a * h + b * g + c * f + d * e, m * n)")], "su2"),
    ("m33_su2_inverse", "rational inverse keeps d", [("return p[0], -p[1], -p[2], -p[3], p[4]", "return p[0], -p[1], -p[2], p[3], p[4]")], "su2"),
    ("m34_su2_palette", "palette element off the unit sphere", [("PALETTE = ((1, 2, 2, 0, 3),", "PALETTE = ((1, 2, 2, 1, 3),")], "su2"),
    ("m35_su2_face_order", "SU(2) faces read in another order, both routes", [("x = rational_product(rational_product(PALETTE[config[a]], PALETTE[config[b]]), rational_inverse(PALETTE[config[c]]))", "x = rational_product(rational_product(PALETTE[config[b]], PALETTE[config[a]]), rational_inverse(PALETTE[config[c]]))"),
                                                                                         ("for slot, inverted in ((a, False), (b, False), (c, True), (d, True)):", "for slot, inverted in ((b, False), (a, False), (c, True), (d, True)):")], "su2"),
    ("m36_su2_sign_swap", "positive g filed under -1", [("found.setdefault(1 if value[0] > 0 else -1, (config, value))", "found.setdefault(-1 if value[0] > 0 else 1, (config, value))")], "su2"),
    ("m37_twist_third_axis", "twist uses i on both directions", [("config = [i if mu == 0 and x[0] == 0 else j if mu == 1 and x[1] == 0 else q.one for x, mu in lat.links]", "config = [i if mu == 0 and x[0] == 0 else i if mu == 1 and x[1] == 0 else q.one for x, mu in lat.links]")], ZL),
    ("m38_control_orbit", "control orbit wrong", [("    orbit = q.order ** len(lat.sites[1:])\n    ok = in_kernel", "    orbit = q.order ** len(lat.sites)\n    ok = in_kernel")], ZL),
    ("m39_section_noncentral", "section base i and j swapped with k", [("    k = q.mult[i][j]\n    section = [q.one, i, j, k]\n", "    k = q.mult[i][j]\n    section = [q.one, i, k, j]\n")], ZL),
    ("m40_flat_extra", "flat cochain kernel drops a basis vector", [("    basis = f2_kernel(rows, len(lat.links))\n    span = [0]\n", "    basis = f2_kernel(rows, len(lat.links))[1:]\n    span = [0]\n")], ZL),
    ("m41_row_lookup_loose", "row lookup always true", [("    return flag(any(line.startswith(tag + \"|\") and (\"|\" + field + \"|\") in line for line in rows))", "    return 1")], FAST),
    ("m42_clean_true", "summary clean always true", [("clean = COUNT[\"off_rule_constant\"] == 0 and COUNT[\"on_rule_both\"] == 0 and COUNT[\"central_odd\"] == 0", "clean = True")], FAST),
    ("m43_off_rule_count", "witness rows stop counting off-rule constants", [("    COUNT[\"off_rule_constant\"] += off_rule - both\n", "    pass\n")], FAST),
    ("m44_witness_ok_weak", "witness ok reduced to the exact recheck", [("ok = both == off_rule and on_rule_ok and exact_ok and gauge_ok and len(reduced) == target", "ok = exact_ok")], FAST),
    ("m45_witness_values_weak", "witness both-values test weakened", [("both += 1 if len(values) == 2 else 0", "both += 1")], "witnesses"),
    ("m46_lattices_expect", "(2,1,2) marked as full", [("((2, 1), False), ((1, 1), False), ((2, 1, 2), False))", "((2, 1), False), ((1, 1), False), ((2, 1, 2), True))")], "lattices"),
    ("m47_drop_added_lattice", "the odd-plaquette lattice left out", [("        read_witnesses(q, ADDED_LATTICE, 1000 * (GROUP_NAMES.index(name) + 1) + 9, True)\n", "")], "witnesses,summary"),
    ("m48_epsilon_plus_no_added", "epsilon +1 with the odd lattice left out", [("return -1 if (mask >> self.merged_of[self.one]) & 1 else 1", "return 1"), ("        read_witnesses(q, ADDED_LATTICE, 1000 * (GROUP_NAMES.index(name) + 1) + 9, True)\n", "")], "witnesses,summary"),
    ("m49_group_sizes", "expected class sizes for 2I altered", [("\"2I\": (1, 1, 12, 12, 12, 12, 20, 20, 30)}", "\"2I\": (1, 1, 12, 12, 12, 12, 20, 30, 20)}")], "groups"),
    ("m50_exhaustive_rule_len", "exhaustive equality dropped", [("rule_met and len(constant) == 8)))", "len(constant) == 8)))")], "groups,exhaustive"),
]

only = set(sys.argv[1:])
DONE = {"m01_hamilton_sign","m02_conjugate","m03_ico_odd","m04_no_inverse_merge","m05_hom_and","m06_rule_no_minus","m07_rule_flip_bit0","m08_index_no_squares","m09_epsilon_plus","m10_constant_ignores_F","m11_constant_plus","m12_third_letter","m13_fourth_letter","m14_shift_back"}
for mid, desc, muts, sel in MUTANTS:
    if (only and mid not in only) or mid in DONE:
        continue
    try:
        evaluate(mid, desc, muts, sel)
    except Exception as ex:  # a harness fault is printed, and the run moves on
        print("MUT|id=%s|desc=%s|result=harness_error|error=%s|json=0" % (mid, desc, str(ex)[:160]))
        sys.stdout.flush()
print("MUT_DONE|json=0")
