
# ---- extension: beta^13, adding the F=14 closed sets, and a brute force for spin-1 extras on F<=14 closed sets
path14 = "classes_d4_F14.txt"
table14, keep14 = analyse(4, path14)
for key, n in sorted(table14.items()):
    if key[0] == 14:
        print("SHAPE|d=4|F=%d|spans=%d|chi=%d|maxcover=%d|E_prod_a=%s|per_site=%d|json=0" % (key[0], key[1], key[2], key[3], txt(key[4]), n))
new14 = (0, 1)
for key, n in table14.items():
    if key[0] == 14:
        new14 = qa(new14, qm(qm(key[4], (4 ** 14, 1)), (n, 1)))
print("F14|total_coefficient_of_u14=%s|json=0" % txt(new14))


def faces_touching(D, k):
    # faces not in k with all four links on k's cover
    cover = link_set(k)
    cand = set()
    for (x, m) in cover:
        for n in range(D):
            if n == m:
                continue
            a, b = (m, n) if m < n else (n, m)
            cand.add((x, a, b))
            y = list(x)
            y[n] -= 1
            cand.add((tuple(y), a, b))
    out = []
    for f in cand:
        if f in k:
            continue
        x, mu, nu = f
        ls = ((x, mu), (plus(x, mu), nu), (plus(x, nu), mu), (x, nu))
        if all(l in cover for l in ls):
            out.append(f)
    return out


extras = {}
for k, key in keep14:
    ex = faces_touching(4, k)
    extras[(key[0], key[1], key[3], len(ex))] = extras.get((key[0], key[1], key[3], len(ex)), 0) + 1
print("SPIN1_SLOTS|by(F,spans,maxcover,slots)=%s|json=0" % dict(sorted(extras.items())))

series14 = list(series4)
u14 = spow(u, 14)
series14 = [qa(a, qm(new14, b)) for a, b in zip(series14, u14)]
plaq14 = [qm(x, (1, 6)) for x in sder(series14)]
want13 = PUBLISHED_P[13]
print("COMPARE_TABLE1|n=13|<a>_coefficient=%s|-a_n_from_table=%d/%d|match=%d|json=0" % (txt(plaq14[13]), -want13[0], want13[1], 1 if plaq14[13] == (-want13[0], want13[1]) else 0))
residual = qs(qm((-want13[0], want13[1]), (6, 14)), series14[14])
print("BETA14_RESIDUAL|published_minus_assembled_in_logZ_per_site=%s|in_units_of_beta14_over_4^14=%s|json=0" % (txt(residual), txt(qm(residual, (4 ** 14, 1)))))
print("STRETCH13_DONE|json=0")
