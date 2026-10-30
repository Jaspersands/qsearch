"""Exact class-three Rees channel controls, not a quantum implementation.

All arithmetic is over F_7 or Q[zeta_7]. Sparse regular-group-algebra
coefficients represent the full operator, including implicit zero entries.
No project modules, floating phases, source inverses, or hidden-state
simulator are imported. The small-field SDE enumeration is ONLY a control.
"""

from fractions import Fraction as F
from itertools import product
import argparse
import hashlib
import json
from pathlib import Path
from random import Random


P = 7
WEIGHTS = (1, 1, 1, 1, 1, 2, 2, 2, 3, 3)
# Base: x,y,z=[x,y],u=[x,z],v=[y,z]. Cover: tx,...,tv,t2z,t2u,t2v,t3u,t3v.
BASE_BRACKETS = ((0, 1, 2), (0, 2, 3), (1, 2, 4))
COVER_BRACKETS = ((0, 1, 5), (0, 2, 6), (1, 2, 7), (0, 5, 8), (1, 5, 9))
CZERO = (F(0),) * 6
CONE = (F(1),) + (F(0),) * 5


def cadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def cscale(a, s):
    return tuple(x * s for x in a)


def cmul(a, b):
    out = [F(0)] * 7
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[(i + j) % 7] += x * y
    return tuple(out[i] - out[6] for i in range(6))


def root(k):
    k %= P
    return tuple(F(int(i == k)) for i in range(6)) if k < 6 else (F(-1),) * 6


ROOT_PHASE = {root(k): k for k in range(P)}


def unit(n, i):
    return tuple(int(j == i) for j in range(n))


def add(a, b):
    return tuple((x + y) % P for x, y in zip(a, b))


def scale(a, s):
    return tuple(s * x % P for x in a)


def bracket(a, b, table, removed=()):
    out = [0] * len(a)
    for i, j, k in table:
        if k not in removed:
            out[k] += a[i] * b[j] - a[j] * b[i]
    return tuple(x % P for x in out)


def bch(a, b, table=COVER_BRACKETS, removed=()):
    ab = bracket(a, b, table, removed)
    aab = bracket(a, ab, table, removed)
    bba = bracket(b, scale(ab, -1), table, removed)
    inv2, inv12 = pow(2, -1, P), pow(12, -1, P)
    return tuple(0 if i in removed else
                 (x + y + inv2 * z + inv12 * (u + v)) % P
                 for i, (x, y, z, u, v) in enumerate(zip(a, b, ab, aab, bba)))


def evaluate(s, a):
    return (s * a[0] % P, s * a[1] % P,
            (s * a[2] + s**2 * a[5]) % P,
            (s * a[3] + s**2 * a[6] + s**3 * a[8]) % P,
            (s * a[4] + s**2 * a[7] + s**3 * a[9]) % P)


def dilation(s, a):
    if s % P == 0:
        raise ValueError("Zero is not an automorphism; discard that target")
    return tuple(pow(s, w, P) * x % P for w, x in zip(WEIGHTS, a))


def nullspace(rows, width):
    rows = [[v % P for v in row] for row in rows]
    pivots = []
    r = 0
    for col in range(width):
        pivot = next((j for j in range(r, len(rows)) if rows[j][col]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inv = pow(rows[r][col], -1, P)
        rows[r] = [v * inv % P for v in rows[r]]
        for j in range(len(rows)):
            if j != r and rows[j][col]:
                c = rows[j][col]
                rows[j] = [(v - c * w) % P for v, w in zip(rows[j], rows[r])]
        pivots.append(col)
        r += 1
        if r == len(rows):
            break
    basis = []
    for free in sorted(set(range(width)) - set(pivots)):
        v = [0] * width
        v[free] = 1
        for j, col in enumerate(pivots):
            v[col] = -rows[j][free] % P
        basis.append(tuple(v))
    return basis


def span(basis, width):
    return {tuple(sum(c * b[j] for c, b in zip(coeffs, basis)) % P
                  for j in range(width))
            for coeffs in product(range(P), repeat=len(basis))}


def lifted_hidden_basis(points=(1, 2, 3)):
    # The native hidden line is span(x+u), so y=z=v=u-x=0.
    rows = []
    for s in points:
        images = [evaluate(s, unit(10, j)) for j in range(10)]
        rows.extend([tuple(v[k] for v in images) for k in (1, 2, 4)])
        rows.append(tuple((v[3] - v[0]) % P for v in images))
    return nullspace(rows, 10)


def convolution(a, b, mul):
    out = {}
    for g, x in a.items():
        for h, y in b.items():
            k = mul(g, h)
            out[k] = cadd(out.get(k, CZERO), cmul(x, y))
    return {g: x for g, x in out.items() if x != CZERO}


def branch_moments(hidden, center, removed=()):
    """Compute Pi rho Pi, then regular traces; no branch-law substitution."""
    size = P ** (10 - len(removed))
    identity = (0,) * 10
    mul = lambda a, b: bch(a, b, removed=removed)
    rho = {h: cscale(CONE, F(1, size)) for h in hidden}
    moments, masses = {}, {}
    for label in range(P):
        projector = {scale(unit(10, center), z): cscale(root(-label * z), F(1, P))
                     for z in range(P)}
        measured = convolution(convolution(projector, rho, mul), projector, mul)
        mass = cscale(measured.get(identity, CZERO), size)
        assert all(x == 0 for x in mass[1:]) and mass[0] >= 0
        masses[label] = mass[0]
        if mass[0]:
            # Tr(R_a R_g) = |G| if a=g^-1, and zero otherwise.
            values = {scale(g, -1): cscale(value, size / mass[0])
                      for g, value in measured.items()}
            assert all(v in ROOT_PHASE for v in values.values())
            moments[label] = {g: ROOT_PHASE[v] for g, v in values.items()}
        else:
            assert not measured
    assert sum(masses.values()) == 1
    return moments, masses


def witness(labels, degree):
    """Exhaustive fixed-F_7 control, NOT the scalable SDE algorithm."""
    representatives = {}
    for s in range(P):
        representatives.setdefault(pow(s, degree, P), s)
    for powers in product(representatives, repeat=len(labels)):
        if any(powers) and sum(a * b for a, b in zip(labels, powers)) % P == 0:
            return tuple(representatives[t] for t in powers)
    raise ValueError("No nonzero witness of this arity")


def transformed_moments(moments):
    # Table at argument g is the original trace at Delta_s(g).
    return {(label, s): {dilation(pow(s, -1, P), g): phase for g, phase in table.items()}
            for label, table in moments.items() for s in range(1, P)}


def merge(transformed, labels, scales):
    if len(labels) != len(scales) or not any(scales):
        raise ValueError("A nonempty active witness is required")
    tables = [transformed[label, s] for label, s in zip(labels, scales) if s]
    support = set(tables[0]).intersection(*(set(t) for t in tables[1:]))
    return {g: sum(t[g] for t in tables) % P for g in support}


def stage_control(center, hidden, removed=(), exhaustive=True):
    degree = WEIGHTS[center]
    basis = [unit(10, j) for j in range(10) if j not in removed]
    assert all(bracket(unit(10, center), b, COVER_BRACKETS, removed) == (0,) * 10
               for b in basis)
    moments, masses = branch_moments(hidden, center, removed)
    transformed = transformed_moments(moments)
    hz = {bch(h, scale(unit(10, center), z), removed=removed)
          for h in hidden for z in range(P)}
    expected = {g: 0 for g in hz}
    # Check every scale, not only the representatives chosen by the solver.
    assert all(set(table) == hz for table in transformed.values())
    arity = degree + 1
    tuples = product(moments, repeat=arity)
    if not exhaustive:
        tuples = [tuple(sorted(moments)[i % len(moments)] for i in range(arity))]
    records = zero_scales = zero_labels = 0
    for labels in tuples:
        scales = witness(labels, degree)
        assert merge(transformed, labels, scales) == expected
        assert sum(lam * pow(s, degree, P) for lam, s in zip(labels, scales)) % P == 0
        records += 1
        zero_scales += any(s == 0 for s in scales)
        zero_labels += any(label == 0 for label in labels)

    extra_active = 0
    if set(moments) == set(range(P)):
        labels, scales = ((1, 1, 1, 4), (1, 2, 4, 1)) if degree == 3 else (
            (1, 1, 1), (1, 2, 3))
        assert all(scales)
        assert sum(lam * pow(s, degree, P) for lam, s in zip(labels, scales)) % P == 0
        assert merge(transformed, labels, scales) == expected
        extra_active = 1

    quotient_removed = (*removed, center)
    quotient_hidden = {tuple(0 if j == center else v for j, v in enumerate(h))
                       for h in hidden}
    rng = Random(103 + center)
    addresses = [tuple(0 if j in quotient_removed else rng.randrange(P)
                       for j in range(10)) for _ in range(128)]
    pairs = [(a, b) for a, b in zip(addresses, reversed(addresses))]
    pairs.extend((bch(b, h, removed=quotient_removed), b)
                 for b in addresses for h in quotient_hidden)
    entries = 0
    quotient_size = P ** (10 - len(quotient_removed))
    for twist in (0, 1):
        def section(q):
            v = list(q)
            v[center] = twist * (q[0] * q[1] + q[0]**2 + q[3]) % P
            return tuple(v)
        for q, r in pairs:
            g = bch(scale(section(r), -1), section(q), removed=removed)
            actual = F(int(g in expected), quotient_size)
            diff = bch(scale(r, -1), q, removed=quotient_removed)
            target = F(int(diff in quotient_hidden), quotient_size)
            assert actual == target
            entries += 1
    return {
        "removed_coordinate": center,
        "degree": degree,
        "group_dimension": 10 - len(removed),
        "group_order": P ** (10 - len(removed)),
        "hidden_order": len(hidden),
        "positive_labels": len(moments),
        "masses": {str(k): str(v) for k, v in masses.items()},
        "complete_label_tuples_checked": records,
        "witnesses_checked_per_tuple": 1,
        "additional_all_active_witnesses": extra_active,
        "records_with_zero_scale": zero_scales,
        "records_with_zero_label": zero_labels,
        "exact_sparse_moment_entries_per_record": len(expected),
        "unlisted_moments": "exactly zero by sparse coefficient representation",
        "explicit_address_entry_checks": entries,
        "section_controls": 2,
        "source_copies_per_merge": arity,
    }, quotient_hidden


def associative_product(a, b):
    out = {}
    for w, x in a.items():
        for v, y in b.items():
            if len(w + v) <= 3:
                out[w + v] = (out.get(w + v, 0) + x * y) % P
    return {w: x for w, x in out.items() if x}


def associative_sum(*terms):
    out = {}
    for weight, poly in terms:
        for w, x in poly.items():
            out[w] = (out.get(w, 0) + weight * x) % P
    return {w: x for w, x in out.items() if x}


FREE_LIE_WORDS = ({"x": 1}, {"y": 1}, {"xy": 1, "yx": -1},
                  {"xxy": 1, "xyx": -2, "yxx": 1},
                  {"yxy": 2, "yyx": -1, "xyy": -1})


def lie_words(a):
    return associative_sum(*zip(a, FREE_LIE_WORDS))


def associative_exp(a):
    a2 = associative_product(a, a)
    a3 = associative_product(a2, a)
    return associative_sum((1, {"": 1}), (1, a), (pow(2, -1, P), a2),
                           (pow(6, -1, P), a3))


def algebra_controls():
    rng = Random(718)
    base_basis = [unit(5, i) for i in range(5)]
    cover_basis = [unit(10, i) for i in range(10)]
    pairs = list(product(base_basis, repeat=2))
    pairs += [(tuple(rng.randrange(P) for _ in range(5)),
               tuple(rng.randrange(P) for _ in range(5))) for _ in range(256)]
    for a, b in pairs:
        lhs = associative_exp(lie_words(bch(a, b, BASE_BRACKETS)))
        rhs = associative_product(associative_exp(lie_words(a)), associative_exp(lie_words(b)))
        assert lhs == rhs
    evaluation_checks = dilation_checks = jacobi_checks = 0
    for a, b in product(cover_basis, repeat=2):
        for s in range(1, P):
            assert evaluate(s, bracket(a, b, COVER_BRACKETS)) == bracket(
                evaluate(s, a), evaluate(s, b), BASE_BRACKETS)
            evaluation_checks += 1
            assert dilation(s, bracket(a, b, COVER_BRACKETS)) == bracket(
                dilation(s, a), dilation(s, b), COVER_BRACKETS)
            dilation_checks += 1
    for a, b, c in product(cover_basis, repeat=3):
        jacobi = add(add(bracket(a, bracket(b, c, COVER_BRACKETS), COVER_BRACKETS),
                         bracket(b, bracket(c, a, COVER_BRACKETS), COVER_BRACKETS)),
                     bracket(c, bracket(a, b, COVER_BRACKETS), COVER_BRACKETS))
        assert not any(jacobi)
        jacobi_checks += 1
    lifted = lifted_hidden_basis()
    assert lifted == [(1, 0, 0, 1, 0, 0, 0, 0, 0, 0)]
    native_h = {(a, 0, 0, a, 0) for a in range(P)}
    x_plus_u = (1, 0, 0, 1, 0)
    conjugate = bch(bch(base_basis[1], x_plus_u, BASE_BRACKETS),
                    scale(base_basis[1], -1), BASE_BRACKETS)
    assert conjugate not in native_h
    # Every codimension-one ideal contains z,u,v and one nonzero ax+by.
    # Its bracket with z is au+bv, so no such ideal is abelian.
    directions = [(1, a) for a in range(P)] + [(0, 1)]
    for a, b in directions:
        assert any(bracket((a, b, 0, 0, 0), base_basis[2], BASE_BRACKETS))
    return {
        "base_class": 3,
        "base_dimension": 5,
        "cover_dimension": 10,
        "associative_exp_bch_checks": len(pairs),
        "cover_basis_jacobi_checks": jacobi_checks,
        "evaluation_basis_bracket_checks": evaluation_checks,
        "dilation_basis_bracket_checks": dilation_checks,
        "lifted_hidden_basis": lifted,
        "nonnormal_conjugate": conjugate,
        "codimension_one_nonabelian_ideal_controls": len(directions),
        "source_calls_per_lift": 3,
    }


def final_readout(hidden):
    assert all(not any(h[5:]) for h in hidden)
    support = []
    size = P**5
    for freq in product(range(P), repeat=5):
        value = CZERO
        for h in hidden:
            value = cadd(value, root(-sum(k * v for k, v in zip(freq, h))))
        probability = cscale(value, F(1, size))
        assert probability in (CZERO, cscale(CONE, F(len(hidden), size)))
        if probability != CZERO:
            support.append(freq)
    recovered_basis = nullspace(support, 5)
    assert span(recovered_basis, 5) == {h[:5] for h in hidden}
    return {"frequencies_checked": size, "nonzero_frequencies": len(support),
            "each_positive_probability": str(F(len(hidden), size)),
            "total_probability": str(len(support) * F(len(hidden), size)),
            "recovered_basis": recovered_basis,
            "method": "exact distribution and annihilator, not sampled quantum execution"}


def negative_controls(hidden):
    moments, _ = branch_moments(hidden, 9)
    transformed = transformed_moments(moments)
    hz = {bch(h, scale(unit(10, 9), z)) for h in hidden for z in range(P)}
    expected = {g: 0 for g in hz}
    wrong_degree = merge(transformed, (1, 2), (1, 3))
    assert (1 + 2 * 3) % P == 0 and (1 + 2 * 3**3) % P != 0
    assert wrong_degree != expected
    # A proper source lift needs three distinct nonzero evaluation points.
    incomplete_dimension = len(lifted_hidden_basis((1, 2)))
    repeated_dimension = len(lifted_hidden_basis((1, 1, 1)))
    assert incomplete_dimension > 1 and repeated_dimension > 1
    # At the first quotient, coordinate subtraction is still not group division.
    r = unit(10, 1)
    h = (1, 0, 0, 1, 0, 0, 0, 0, 0, 0)
    q = bch(r, h, removed=(9,))
    assert bch(scale(r, -1), q, removed=(9,)) == h
    assert add(q, scale(r, -1)) not in hidden
    assert bch(q, scale(r, -1), removed=(9,)) not in hidden
    # A base grading is not a substitute for the Rees cover on this tilted H.
    native = (1, 0, 0, 1, 0)
    wrong_base_dilation = tuple(pow(2, w, P) * x % P
                               for w, x in zip((1, 1, 2, 3, 3), native))
    assert wrong_base_dilation not in {scale(native, a) for a in range(P)}
    return {"linear_instead_of_cubic_phase": "rejected",
            "too_few_evaluation_points_hidden_dimension": incomplete_dimension,
            "repeated_evaluation_points_hidden_dimension": repeated_dimension,
            "abelian_subtraction_before_grade_one": "rejected",
            "wrong_side_coset_product": "rejected",
            "base_dilation_on_tilted_hidden_subgroup": "rejected",
            "all_zero_witness": "invalid, would have full rather than HZ support"}


def run():
    algebra = algebra_controls()
    hidden = span(lifted_hidden_basis(), 10)
    negative = negative_controls(hidden)
    stages = []
    removed = ()
    leaves = 1
    for center in (9, 8, 7, 6, 5):
        row, hidden = stage_control(center, hidden, removed)
        stages.append(row)
        leaves *= row["source_copies_per_merge"]
        removed = (*removed, center)
    containing = {add(h, scale(unit(10, 9), z)) for h in hidden for z in range(P)}
    containing_row, _ = stage_control(9, containing)
    assert containing_row["positive_labels"] == 1 and containing_row["masses"]["0"] == "1"
    files = ("class_three.py", "test_class_three.py", "CLASS_THREE.md", "HANDOFF.md")
    return {
        "status": "finite exact self-controls; no new independent review",
        "arithmetic": "F_7 and exact rational cyclotomic Q[zeta_7]",
        "quantum_circuit_executed": False,
        "generic_sde_implemented": False,
        "novelty_certified": False,
        "speedup_established_by_this_run": False,
        "algebra": algebra,
        "stages": stages,
        "center_contained_control": containing_row,
        "negative_controls": negative,
        "final_readout": final_readout(hidden),
        "one_terminal_state_resource_ledger": {
            "lifted_source_copies": leaves,
            "original_source_copies": 3 * leaves,
            "caveat": "scalar-flag control schedule, not the general fixed-class cost bound",
        },
        "sha256": {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                   for name in files},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(result)
    else:
        print(result, end="")
