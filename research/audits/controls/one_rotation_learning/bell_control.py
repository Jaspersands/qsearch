"""Exact n=4 cyclotomic Bell-law falsifier; not an asymptotic learner."""
import json
from pathlib import Path
from sage.all import CyclotomicField, QQ

n = 4
size = 1 << n
mask = size-1
K = CyclotomicField(16, "zeta")
zeta = K.gen()
imag = zeta**4
c = (zeta+zeta**-1)/2
s = (zeta-zeta**-1)/(2*imag)
invsqrt2 = (zeta**2+zeta**-2)/2
base = [c**(n-t.bit_count())*s**t.bit_count() for t in range(size)]
psi = [zeta**(-((-1)**t.bit_count()))*base[t] for t in range(size)]
assert sum(a*a.conjugate() for a in psi) == 1

gates = [("H", 0), ("S", 1), ("CX", 1, 2), ("CX", 3, 0)]


def clifford(state, inverse=False):
    a = list(state)
    for gate in reversed(gates) if inverse else gates:
        out = list(a)
        kind, j = gate[:2]
        if kind == "H":
            for t in range(size):
                if not ((t >> j) & 1):
                    u = t ^ (1 << j)
                    out[t], out[u] = (a[t]+a[u])*invsqrt2, (a[t]-a[u])*invsqrt2
        elif kind == "S":
            for t in range(size):
                if (t >> j) & 1:
                    out[t] *= -imag if inverse else imag
        else:
            target = gate[2]
            for t in range(size):
                out[t ^ (((t >> j) & 1) << target)] = a[t]
        a = out
    return a


def pullback(v):
    x, z = v & mask, v >> n
    for gate in reversed(gates):
        kind, j = gate[:2]
        if kind == "H":
            flip = ((x ^ z) >> j) & 1
            x ^= flip << j
            z ^= flip << j
        elif kind == "S":
            z ^= (((x >> j) & 1) ^ 1) << j  # affine transpose offset
        else:
            k = gate[2]
            x ^= ((x >> j) & 1) << k
            z ^= ((z >> k) & 1) << j
    return x | (z << n)


def mu(v):
    x, z = v & mask, v >> n
    if x & z:
        return QQ(0)
    return QQ(1)/2**(n+(x | z).bit_count())


def law(v):
    if (v & mask).bit_count() % 2:
        return mu(v)
    return (mu(v)+mu(v ^ (mask << n)))/2


def bell(a, v):
    x, z = v & mask, v >> n
    amplitude = sum((-1)**((z & t).bit_count())*a[t]*a[t ^ x] for t in range(size))/4
    return QQ(amplitude*amplitude.conjugate())


scrambled = clifford(psi)
law_mass = sum(law(v) for v in range(size*size))
assert law_mass == 1
support = []
for v in range(size*size):
    assert bell(psi, v) == law(v)
    assert bell(scrambled, v) == law(pullback(v))
    x, z = v & mask, v >> n
    q = (x & z).bit_count() % 2
    equations = [q] + [((x >> i)&1)*((x >> j)&1)*(((z >> i)^(z >> j))&1)
                       for i in range(n) for j in range(i+1, n)]
    assert (not any(equations)) == bool(law(v))
    if law(v):
        support.append(v)
assert any(law(v) and not law(v ^ (mask << n)) for v in support)
shift = pullback(0)
columns = [pullback(1 << j) ^ shift for j in range(2*n)]
for v in range(size*size):
    u = shift
    for j in range(2*n):
        if (v >> j) & 1:
            u ^= columns[j]
    assert u == pullback(v)

# Truth used only in this finite identity control, never learner input.
physical_P_psi = clifford([(-1)**t.bit_count()*a for t, a in enumerate(clifford(scrambled, True))])
corrected = [c*a+imag*s*b for a, b in zip(scrambled, physical_P_psi)]
assert corrected == clifford(base)
result = {"n": n, "labels_checked_each_frame": size*size, "support_size": len(support),
          "exact_field": "Q(zeta16)", "law_mass": str(law_mass),
          "nontrivial_affine_clifford_offset": shift,
          "law_and_cubic_cut": True, "physical_pauli_correction": True,
          "naive_translation_period": False,
          "claims": {"full_learner_executed": False, "asymptotic_from_control": False,
                     "quantum_execution": False, "speedup": False}}
Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, separators=(",", ":")))
