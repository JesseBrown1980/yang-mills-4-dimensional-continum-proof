# nf_scan.py -- token scan of this lane's scripts: float literals, the true-division operator,
# negative powers written as '** -', and imports of float, fractions, decimal or math.
import io
import sys
import tokenize

FILES = ['ilib.py', 'g1lib.py', 'polylib.py', 'n1_constants.py', 'n2_certs.py', 'n3_c09.py', 'n4_g1c.py', 'n5_w03.py', 'n6_extra.py', 'n7_precision_recheck.py',
         't_ilib.py', 'nf_scan.py']
BASE = '/mnt/c/tmp/opus55/ym4-04c-gattack/work/L5-numbers/'
total = 0
for f in FILES:
    src = open(BASE + f, encoding='utf-8').read()
    toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    fl = 0
    td = 0
    npw = 0
    bad_imp = 0
    names = 0
    for i, t in enumerate(toks):
        if t.type == tokenize.NUMBER:
            s = t.string.lower()
            if not s.startswith('0x') and ('.' in s or 'e' in s or 'j' in s):
                fl += 1
        if t.type == tokenize.OP and t.string in ('/', '/='):
            td += 1
        if t.type == tokenize.OP and t.string == '**':
            if i + 1 < len(toks) and toks[i + 1].string == '-':
                npw += 1
        if t.type == tokenize.NAME and t.string in ('float', 'Fraction', 'Decimal'):
            names += 1
        if t.type == tokenize.NAME and t.string in ('fractions', 'decimal', 'math'):
            if i > 0 and toks[i - 1].string in ('import', 'from'):
                bad_imp += 1
    total += fl + td + npw + bad_imp + names
    print('NF|file=' + f + '|float_literals=' + str(fl) + '|true_division_ops=' + str(td) + '|negative_powers=' + str(npw) +
          '|float_names=' + str(names) + '|float_or_fraction_imports=' + str(bad_imp) + '|json=0')
print('NF_END|total=' + str(total) + '|json=0')
