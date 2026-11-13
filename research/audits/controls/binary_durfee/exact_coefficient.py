"""One prescribed finite Laurent-coefficient falsifier, n=1..5 only.
Run with /opt/anaconda3/envs/qsearch-cas/bin/python; JSON receipt on stdout.
Parent owns notes. No helper suite is imported/executed.
"""
from sage.all import QQ, PolynomialRing, SymmetricFunctions, Partitions, matrix
import ast
import hashlib
import json
from pathlib import Path
import sys
import time
import traceback

REPO = Path('/Users/jaspersands/Developer/qsearch')
HELPER = REPO / 'research/audits/controls/super_schur/exact_identity.py'
source = HELPER.read_text()
parsed = ast.parse(source, filename=str(HELPER))
selected = [node for node in parsed.body
            if isinstance(node, ast.FunctionDef) and node.name in {'complete', 'schur'}]
assert {node.name for node in selected} == {'complete', 'schur'}
# Execute ONLY these two stable definitions, never imports or old top-level suite.
exec(compile(ast.Module(body=selected, type_ignores=[]), str(HELPER), 'exec'), globals())

SF = SymmetricFunctions(QQ).schur()
started = time.perf_counter()
rings = {}
numerators = {}
references = {}
rows = []
per_n = []
stats = {'numerator_cache_misses': 0, 'numerator_cache_hits': 0,
         'reference_products': 0, 'max_numerator_monomials': 0,
         'max_pruned_dictionary_states': 0, 'denominator_factor_applications': 0,
         'max_geometric_index_observed': 0, 'skipped_nu': 0,
         'numerator_seconds': 0.0, 'coefficient_seconds': 0.0,
         'reference_seconds': 0.0}

def durfee(part):
    return sum(int(part[i]) >= i + 1 for i in range(len(part)))

def ring_data(d, e):
    key = (d, e)
    if key not in rings:
        names = tuple('x' + str(i) for i in range(d)) + tuple('y' + str(i) for i in range(d))
        names += tuple('u' + str(i) for i in range(e)) + tuple('v' + str(i) for i in range(e))
        R = PolynomialRing(QQ, names=names, order='lex')
        z = R.gens()
        x, y = z[:d], z[d:2*d]
        u, v = z[2*d:2*d+e], z[2*d+e:]
        even = [a*b for a in x for b in u] + [a*b for a in y for b in v]
        odd = [a*b for a in x for b in v] + [a*b for a in y for b in u]
        h = complete(even, odd, 5, R)
        delta = R.one()
        for group in (x, y, u, v):
            for i in range(len(group)):
                for j in range(i+1, len(group)):
                    delta *= group[i] - group[j]
        factors = [(i, d+j) for i in range(d) for j in range(d)]
        factors += [(2*d+i, 2*d+e+j) for i in range(e) for j in range(e)]
        even_indices = tuple(range(d)) + tuple(range(2*d, 2*d+e))
        odd_indices = tuple(range(d, 2*d)) + tuple(range(2*d+e, 2*d+2*e))
        rings[key] = (R, h, delta, factors, even_indices, odd_indices)
    return rings[key]

def numerator(d, e, nu):
    key = (d, e, tuple(nu))
    if key in numerators:
        stats['numerator_cache_hits'] += 1
        return numerators[key]
    tic = time.perf_counter()
    R, h, delta, *_ = ring_data(d, e)
    F = schur(nu, h, R) * delta
    data = {tuple(int(a) for a in powers): coefficient
            for powers, coefficient in F.dict().items()}
    numerators[key] = data
    stats['numerator_cache_misses'] += 1
    stats['max_numerator_monomials'] = max(stats['max_numerator_monomials'], len(data))
    stats['numerator_seconds'] += time.perf_counter() - tic
    return data

def frobenius_target(lam, mu, d, e):
    lc, mc = lam.conjugate(), mu.conjugate()
    return tuple(int(lam[i])-i-1 for i in range(d)) + tuple(int(lc[j])-j-1 for j in range(d)) + tuple(int(mu[i])-i-1 for i in range(e)) + tuple(int(mc[j])-j-1 for j in range(e))

def extract(data, target, d, e, n):
    tic = time.perf_counter()
    _, _, _, factors, evens, odds = ring_data(d, e)
    def admissible(powers):
        return all(powers[i] >= target[i] for i in evens) and all(powers[j] <= target[j] for j in odds)
    current = {powers: value for powers, value in data.items() if admissible(powers)}
    stats['max_pruned_dictionary_states'] = max(stats['max_pruned_dictionary_states'], len(current))
    for i, j in factors:
        # Each remaining factor lowers one even exponent and raises one odd exponent.
        # Hence this pruning discards no term which can reach the fixed target.
        nxt = {}
        for powers, value in current.items():
            max_r = min(n, powers[i] - target[i] - 1, target[j] - powers[j])
            if max_r < 0:
                continue
            stats['max_geometric_index_observed'] = max(stats['max_geometric_index_observed'], max_r)
            for rr in range(max_r+1):
                pp = list(powers)
                pp[i] -= rr + 1
                pp[j] += rr
                pp = tuple(pp)
                if admissible(pp):
                    nxt[pp] = nxt.get(pp, 0) + (-value if rr % 2 else value)
        current = {powers: value for powers, value in nxt.items() if value}
        stats['denominator_factor_applications'] += 1
        stats['max_pruned_dictionary_states'] = max(stats['max_pruned_dictionary_states'], len(current))
        if not current:
            break
    ans = current.get(target, QQ.zero())
    stats['coefficient_seconds'] += time.perf_counter() - tic
    return ans

def receipt(status, **extras):
    return {'status': status,
            'scope': 'Finite exact falsifier only: ALL triples of partitions n=1..5, actual Durfee(lambda),Durfee(mu)<=2. No scalable algorithm, asymptotic theorem, Barvinok implementation, or numerical approximation inferred.',
            'repo': str(REPO), 'cas_interpreter': sys.executable,
            'helper_provenance': {'path': str(HELPER), 'sha256': hashlib.sha256(source.encode()).hexdigest(),
                                  'only_definitions_executed': ['complete','schur'], 'old_suite_executed': False},
            'formula': '[x^alpha y^beta u^gamma v^delta] hs_nu(xu,yv|xv,yu) Delta(x)Delta(y)Delta(u)Delta(v)/(prod(x_i+y_j)prod(u_i+v_j)), expanded even-leading',
            'reference': 'SF[lambda].kronecker_product(SF[mu]).coefficient(nu)',
            'geometric_cap': 'r=0..n for each inverse factor, further limited by monotone exponent target bounds',
            'lex_variable_order': 'x,y,u,v', 'exact_arithmetic': 'QQ polynomial coefficients and integer Laurent exponents',
            'tested_triples': len(rows), 'per_n': per_n, 'stats': stats,
            'elapsed_seconds': time.perf_counter()-started, 'rows': rows, **extras}

try:
    for n in range(1,6):
        tic = time.perf_counter()
        parts = list(Partitions(n))
        relevant = [part for part in parts if durfee(part)<=2]
        count = 0
        nonzero = 0
        regimes = {}
        for lam in relevant:
            d = durfee(lam)
            for mu in relevant:
                e = durfee(mu)
                key = (tuple(lam), tuple(mu))
                rt = time.perf_counter()
                references[key] = SF[lam].kronecker_product(SF[mu])
                stats['reference_seconds'] += time.perf_counter() - rt
                stats['reference_products'] += 1
                target = frobenius_target(lam, mu, d, e)
                assert all(a>=0 for a in target)
                for nu in parts:
                    # No nu-Durfee zero shortcut: every triple is evaluated independently.
                    actual = extract(numerator(d,e,nu), target, d,e,n)
                    expected = references[key].coefficient(nu)
                    if actual != expected:
                        failure = {'n':n,'lambda':list(map(int,lam)),'mu':list(map(int,mu)),
                                   'nu':list(map(int,nu)),'d':d,'e':e,'target':list(target),
                                   'actual':str(actual),'expected':str(expected)}
                        print(json.dumps(receipt('COUNTEREXAMPLE', failure=failure),sort_keys=True))
                        sys.exit(1)
                    assert actual.denominator() == 1
                    value = int(actual)
                    rows.append({'n':n,'lambda':list(map(int,lam)),'mu':list(map(int,mu)),
                                 'nu':list(map(int,nu)),'d':d,'e':e,'coefficient':value,
                                 'reference':int(expected),'equal':True})
                    count += 1
                    nonzero += value != 0
                    regime = str(d)+','+str(e)
                    regimes[regime] = regimes.get(regime,0)+1
        assert count == len(relevant)**2 * len(parts)
        row = {'n':n,'partitions':len(parts),'lambda_mu_partitions':len(relevant),
               'triples':count,'nonzero_values':nonzero,'zero_values':count-nonzero,
               'durfee_regime_counts':regimes,'elapsed_seconds':time.perf_counter()-tic}
        per_n.append(row)
        print('finished n='+str(n)+': '+str(count)+' exact triples',file=sys.stderr,flush=True)
    assert len(rows) == 504
    print(json.dumps(receipt('PASS', assertions='504 exact coefficient/reference equalities;504 integral coefficient assertions; exact count receipts for each n', no_counterexample_found=True),sort_keys=True))
except Exception as exc:
    print(json.dumps(receipt('CODE_OR_API_ISSUE', error_type=type(exc).__name__,error=str(exc),traceback=traceback.format_exc()),sort_keys=True))
    sys.exit(2)
