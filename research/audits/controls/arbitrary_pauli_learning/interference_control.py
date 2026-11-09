"""Exact Bell interference and existing decoder falsifiers, not a full learner."""
import json
import sys
from itertools import combinations
from pathlib import Path
from sage.all import CyclotomicField, QQ, GF, matrix

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'one_rotation_learning'))
from macaulay_n4 import decode, bell_pullback, physical_pauli_forward

K = CyclotomicField(16, 'zeta')
zeta = K.gen()
imag = zeta**4
c = (zeta + zeta**-1)/2
s = (zeta - zeta**-1)/(2*imag)
invsqrt2 = (zeta**2 + zeta**-2)/2


def label(word):
    n = len(word)
    return sum((int(a in 'XY') << i) | (int(a in 'YZ') << (n+i))
               for i, a in enumerate(word))


def pauli(a, p, n):
    x, z = p & ((1 << n)-1), p >> n
    out = [K(0)]*len(a)
    for t, value in enumerate(a):
        out[t ^ x] = imag**((x & z).bit_count()) * (-1)**((z & t).bit_count()) * value
    return out


def case(word):
    n = len(word)
    size, mask = 1 << n, (1 << n)-1
    p = label(word)
    px, pz = p & mask, p >> n
    qp = (px & pz).bit_count() % 2
    base = [c**(n-t.bit_count()) * s**t.bit_count() for t in range(size)]
    rotated = [c*a-imag*s*b for a,b in zip(base, pauli(base,p,n))]
    assert sum(a*a.conjugate() for a in rotated) == 1
    corrected = [c*a+imag*s*b for a,b in zip(rotated, pauli(rotated,p,n))]
    assert corrected == base

    def mu(v):
        x, z = v & mask, v >> n
        return QQ(0) if x & z else QQ(1)/2**(n+(x|z).bit_count())

    def ell(v):
        x, z = v & mask, v >> n
        return (qp + (px & z).bit_count() + (pz & x).bit_count()) % 2

    def rho(v):
        return mu(v) if ell(v) else (mu(v)+mu(v ^ p))/2

    def actual(v):
        x, z = v & mask, v >> n
        amplitude = invsqrt2**n * sum((-1)**((z&t).bit_count()) * rotated[t] * rotated[t^x]
                                        for t in range(size))
        return amplitude*amplitude.conjugate()

    values = [actual(v) for v in range(size*size)]
    overlap = [v for v in range(size*size) if mu(v) and mu(v ^ p)]
    assert sum(values) == sum(rho(v) for v in range(size*size)) == 1
    assert sum(values[v] for v in overlap) == sum(rho(v) for v in overlap)
    overlap_mass = sum(mu(v) for v in overlap)
    assert overlap_mass == (QQ(1)/2)**word.count('Y') * (QQ(3)/4)**(word.count('X')+word.count('Z'))
    for v in range(size*size):
        if v not in overlap:
            assert values[v] == rho(v)
        if not rho(v):
            assert not values[v]
        assert bool(rho(v)) == bool((mu(v) or mu(v^p)) and not (((v&mask)&(v>>n)).bit_count()%2))
    support = [v for v,value in enumerate(values) if value]
    mons = [sum(1 << j for j in term) for d in range(3) for term in combinations(range(2*n),d)]
    k2 = len(mons)-matrix(GF(2), [[int(v&m == m) for m in mons] for v in support]).rank()
    output = {'pauli':word, 'labels_checked':size*size, 'support_size':len(support),
              'envelope_support_size':sum(bool(rho(v)) for v in range(size*size)),
              'cancelled_envelope_labels':sum(bool(rho(v)) and not values[v] for v in range(size*size)),
              'overlap_mass':str(overlap_mass), 'k2_dimension':int(k2),
              'outside_overlap_exact':True, 'source_correction_exact':True}
    if word == 'Y':
        assert rotated[0] == rotated[1] == invsqrt2
        assert output['cancelled_envelope_labels'] == 1 and k2 == 2
    if word == 'YZZZ':
        assert output['cancelled_envelope_labels'] == 0 and k2 == 1
        scrambled_support = [v for v in range(256) if values[bell_pullback(v)]]
        axes, detail = decode(scrambled_support,4)
        expected = sorted(physical_pauli_forward(a) for a in [17,32,64,128,p])
        assert axes == expected
        assert physical_pauli_forward(p) in axes
        # The affine Y-plane map fixes Y as a point but sends its direction to Z.
        affine_y = lambda v: ((v & 1) ^ ((v >> 4) & 1) ^ 1) | (v & ~1)
        assert affine_y(17) == 17
        assert affine_y(17) ^ affine_y(0) == 16
        output.update(candidate_axes=axes, true_physical_axis=physical_pauli_forward(p),
                      affine_point_shortcut_rejected=True, **detail)
    if word == 'YZZZI':
        assert k2 == 2 and not output['cancelled_envelope_labels']
    if word == 'YZZZZ':
        assert output['cancelled_envelope_labels'] > 0
    return output


results = [case(word) for word in ['Y','YZZZ','YZZZI','YZZZZ']]
assert 1024*3**25 < 4**25 and 1024*3**24 > 4**24
out = {'scope':'four fixed exact phase/support falsifiers; existing n4 decoder reused',
       'exact_field':'Q(zeta16)', 'cases':results, 'cutoff_integer_inequality':True,
       'claims':{'full_learner_executed':False, 'quantum_execution':False,
                 'asymptotic_from_controls':False, 'speedup':False}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,separators=(',',':')))
