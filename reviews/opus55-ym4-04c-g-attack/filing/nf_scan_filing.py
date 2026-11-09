# nf_scan_filing.py -- token scan of the filing scripts: float literals, true division,
# negative powers, float/Fraction/Decimal names and fractions/decimal/math imports.
import io
import tokenize

BASE = '/mnt/c/tmp/opus55/ym4-04c-gattack/work/filing/'
FILES = ['c05_c06_edges.py', 'gen_filing.py', 'nf_scan_filing.py']
total = 0
for f in FILES:
    src = open(BASE + f, encoding='utf-8').read()
    toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    fl = td = npw = bad = nm = 0
    for i, t in enumerate(toks):
        if t.type == tokenize.NUMBER:
            s = t.string.lower()
            if not s.startswith('0x') and ('.' in s or 'e' in s or 'j' in s):
                fl += 1
        if t.type == tokenize.OP and t.string in ('/', '/='):
            td += 1
        if t.type == tokenize.OP and t.string == '**' and i + 1 < len(toks) and toks[i + 1].string == '-':
            npw += 1
        if t.type == tokenize.NAME and t.string in ('float', 'Fraction', 'Decimal'):
            nm += 1
        if t.type == tokenize.NAME and t.string in ('fractions', 'decimal', 'math') and i > 0 and toks[i - 1].string in ('import', 'from'):
            bad += 1
    total += fl + td + npw + bad + nm
    print('NF|file=' + f + '|float_literals=' + str(fl) + '|true_division_ops=' + str(td) + '|negative_powers=' + str(npw)
          + '|float_names=' + str(nm) + '|float_or_fraction_imports=' + str(bad) + '|json=0')
print('NF_END|total=' + str(total) + '|json=0')
