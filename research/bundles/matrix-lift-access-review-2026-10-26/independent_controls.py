"""Independent boundary and coordinate-algebra controls; no parent writes."""

from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations_with_replacement
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / "matrix-geometry-lift-2026-10-26"
SOURCES = [PARENT / name for name in ("LIFT.md", "point_lift.py", "test_point_lift.py")]
SOURCES.append(ROOT.parent / "generic-divisor-class-2026-10-26/MATRIX_GEOMETRY.md")
spec = spec_from_file_location("audited_point_lift", PARENT / "point_lift.py")
audited = module_from_spec(spec)
spec.loader.exec_module(audited)


def rref(data, p):
    a = [[x % p for x in row] for row in data]
    if not a:
        return [], []
    pivot_columns = []
    for j in range(len(a[0])):
        index = next((i for i in range(len(pivot_columns), len(a)) if a[i][j]), None)
        if index is None:
            continue
        i = len(pivot_columns)
        a[i], a[index] = a[index], a[i]
        inv = pow(a[i][j], -1, p)
        a[i] = [x * inv % p for x in a[i]]
        for t in range(len(a)):
            if t != i and a[t][j]:
                coefficient = a[t][j]
                a[t] = [(x - coefficient * y) % p for x, y in zip(a[t], a[i])]
        pivot_columns.append(j)
    return a[:len(pivot_columns)], pivot_columns


def kernel(data, p, ncols=None):
    reduced, pivots = rref(data, p)
    ncols = len(data[0]) if data else ncols
    result = []
    for j in range(ncols):
        if j in pivots:
            continue
        row = [0] * ncols
        row[j] = 1
        for i, c in enumerate(pivots):
            row[c] = -reduced[i][j] % p
        result.append(row)
    return result


def products(a, b, p):
    return rref([[(x * y) % p for x, y in zip(u, v)] for u in a for v in b], p)[0]


def quotient(a, b, p):
    return kernel(products(a, kernel(b, p), p), p)


def transpose(a):
    return list(map(list, zip(*a)))


def monomials(n, degree):
    out = []
    for indices in combinations_with_replacement(range(n), degree):
        exp = [0] * n
        for j in indices:
            exp[j] += 1
        out.append(tuple(exp))
    return out


def evaluate(exp, point, p):
    value = 1
    for e, x in zip(exp, point):
        value = value * pow(x, e, p) % p
    return value


def coordinates_in_basis(basis, vector, p):
    augmented = [row + [value] for row, value in zip(transpose(basis), vector)]
    rr, pivots = rref(augmented, p)
    assert pivots == list(range(len(basis)))
    coeffs = [row[-1] for row in rr]
    assert [sum(c * row[j] for c, row in zip(coeffs, basis)) % p
            for j in range(len(vector))] == vector
    return coeffs


def fixture(g, p):
    # y^2 = x^(2g+1) + 2x + 2; the smoothness check includes all roots
    # by polynomial gcd, not just F_p-rational roots.
    from flint import nmod_poly
    f = nmod_poly([2, 2] + [0] * (2*g-1) + [1], p)
    assert f.gcd(f.derivative()).degree() == 0
    points = [(x, y) for x in range(p) for y in range(p)
              if (y*y - x**(2*g+1) - 2*x - 2) % p == 0]
    points.sort(key=lambda point: (point[1] == 0, point))
    d = 2*g+1
    points = points[:2*d+4]
    assert len(points) == 2*d+4
    basis = [[pow(x, i, p) for x, _ in points] for i in range(g+1)]
    basis.append([y for _, y in points])
    return points, basis


def extra_values(points, selected, g, p):
    xp, yp = points[selected]
    assert yp
    out = []
    for i, (x, y) in enumerate(points):
        if i == selected:
            continue
        if x != xp:
            out.append((y + yp) * pow(x - xp, -1, p) % p)
        else:
            assert y == -yp % p
            out.append(-((2*g+1)*pow(xp, 2*g, p)+2) * pow(2*yp, -1, p) % p)
    return out


def boundary_controls():
    checks = []
    for g, p in ((1, 17), (2, 101)):
        points, basis = fixture(g, p)
        k, m = len(basis), len(points)
        for selected in range(m):
            if not points[selected][1]:
                continue
            keep = [i for i in range(m) if i != selected]
            oracle = [[row[i] for i in keep] for row in basis]
            oracle.append(extra_values(points, selected, g, p))
            for scaled in (False, True):
                weights = [pow(3, i+1, p) for i in range(m)] if scaled else [1]*m
                source = [[x*u % p for x, u in zip(row, weights)] for row in basis]
                if scaled:
                    source[0] = [(x+2*y) % p for x, y in zip(source[0], source[1])]
                result = audited.lift_point(source, p, selected)
                target = [[v*weights[j] % p for v, j in zip(row, keep)] for row in oracle]
                got = result["lifted_punctured"]
                assert rref(got, p)[0] == rref(target, p)[0]
                assert got[:k] == [[row[j] for j in keep] for row in source]
                assert [row[selected] for row in result["lifted_projective_points_as_columns"]] == [0]*k+[1]
                assert result["inferred_genus_under_AG_promise"] == g
                assert result["inferred_degree_under_AG_promise"] == 2*g+1
                checks.append({"g": g, "p": p, "m": m, "point": selected, "scaled_and_row_mixed": scaled})
    return checks


def elliptic_add(P, Q, p=17):
    if P is None:
        return Q
    if Q is None:
        return P
    x, y = P
    u, v = Q
    if x == u and (y+v) % p == 0:
        return None
    slope = ((3*x*x+2)*pow(2*y, -1, p) if P == Q
             else (v-y)*pow(u-x, -1, p)) % p
    z = (slope*slope-x-u) % p
    return z, (slope*(x-z)-y) % p


def below_length_counterexample():
    p = 17
    all_points = [(x, y) for x in range(p) for y in range(p)
                  if (y*y-x*x*x-2*x-2) % p == 0]
    rng = random.Random(20261026)
    points = None
    for _ in range(100):
        candidate = rng.sample(all_points, 8)
        total = None
        for point in candidate:
            total = elliptic_add(total, point)
        if total is not None:
            last = (total[0], -total[1] % p)
            if last not in candidate:
                points = candidate + [last]
                break
    assert points is not None
    xp, yp = points[0]
    rest = points[1:]
    V0 = [[1]*8, [x for x, y in rest], [y for x, y in rest]]
    minus = [[(x-xp) % p for x, y in rest], [(y-yp) % p for x, y in rest]]
    square = products(V0, V0, p)
    computed = quotient(minus, square, p)
    actual = V0 + [extra_values(points, 0, 1, p)]
    assert len(rref(actual, p)[0]) == 4
    assert len(rref(computed, p)[0]) == 5
    full = [[1]*9, [x for x, y in points], [y for x, y in points]]
    try:
        audited.lift_point(full, p)
    except ValueError as exc:
        rejection = str(exc)
    else:
        raise AssertionError("m=2d+3 should be outside the helper's contract")
    return {"curve": "y^2=x^3+2x+2 over F_17", "points": points,
            "m": 9, "d": 3, "g": 1, "true_lift_dimension": 4,
            "quotient_dimension": 5, "helper_rejection": rejection}


def algebra_control():
    p = 17
    points, source = fixture(1, p)
    result = audited.lift_point(source, p, 0)
    lifted = result["lifted_punctured"]
    degree2 = monomials(4, 2)
    quadrics = kernel([[evaluate(e, pt, p) for e in degree2]
                      for pt in transpose(lifted)], p)
    assert len(quadrics) == 2
    # Compare with the explicit functions, including points not used by the lift.
    oracle = [row[1:] for row in source] + [extra_values(points, 0, 1, p)]
    extra_coeffs = coordinates_in_basis(oracle, lifted[-1], p)
    assert extra_coeffs[-1]
    xp, yp = points[0]
    all_points = [(x, y) for x in range(p) for y in range(p)
                  if (y*y-x*x*x-2*x-2) % p == 0]
    mapped = []
    for x, y in all_points:
        if (x, y) == (xp, yp):
            pt = [0, 0, 0, 1]
        else:
            z = ((y+yp)*pow(x-xp, -1, p) if x != xp
                 else -(3*xp*xp+2)*pow(2*yp, -1, p)) % p
            pt = [1, x, y, sum(a*b for a, b in zip(extra_coeffs, [1, x, y, z])) % p]
        mapped.append(pt)
    mapped.append([0, 0, 1, extra_coeffs[2]])  # The point at infinity.
    for pt in mapped:
        assert all(sum(c*evaluate(e, pt, p) for c, e in zip(q, degree2)) % p == 0 for q in quadrics)
    # Tangent at P, in the chart X_3=1, must recover the original column.
    jacobian = [[q[degree2.index(tuple(int(t == j)+int(t == 3) for t in range(4)))]
                 for j in range(3)] for q in quadrics]
    tangent = kernel(jacobian, p)
    assert len(tangent) == 1
    assert rref(tangent, p)[0] == rref([[1, xp, yp]], p)[0]
    dimensions = {0: 1, 1: 4}
    for degree in range(2, 8):
        mons = monomials(4, degree)
        index = {e: j for j, e in enumerate(mons)}
        relations = []
        for e in monomials(4, degree-2):
            for q in quadrics:
                row = [0]*len(mons)
                for c, e2 in zip(q, degree2):
                    row[index[tuple(a+b for a, b in zip(e, e2))]] = c
                relations.append(row)
        dimensions[degree] = len(mons)-len(rref(relations, p)[0])
        assert dimensions[degree] == 4*degree
    sample_cubic_rank = len(rref([[evaluate(e, pt, p) for e in monomials(4, 3)]
                                 for pt in transpose(lifted)], p)[0])
    assert sample_cubic_rank < dimensions[3]
    return {"quadrics": quadrics, "monomial_order_degree2": degree2,
            "Hilbert_dimensions_through_7": dimensions,
            "punctured_sample_cubic_rank": sample_cubic_rank,
            "true_cubic_dimension": dimensions[3], "checked_curve_points": len(mapped),
            "tangent_original_column_match": True}


def scope_control():
    # The geometric assertion includes genus zero; the implementation does not.
    source = [[1]*8, list(range(8))]
    try:
        audited.lift_point(source, 17)
    except ValueError as exc:
        return {"g": 0, "d": 1, "m": 8, "rejected": str(exc)}
    raise AssertionError("expected implementation's explicit genus-zero exclusion")


def perfect_pairing_control():
    cases = []
    for p, algebra in ((2, "split_product"), (17, "nonreduced_local")):
        s = 3
        tensor = [[[0]*s for _ in range(s)] for _ in range(s)]
        for i in range(s):
            for j in range(s):
                if algebra == "split_product" and i == j:
                    tensor[i][j][i] = 1
                elif algebra == "nonreduced_local" and i+j < s:
                    tensor[i][j][i+j] = 1
        # Change the three module bases independently; no generator is supplied.
        bases = [[[1, 1, 0], [0, 1, 1], [0, 0, 1]],
                 [[1, 0, 1], [0, 1, 0], [0, 0, 1]],
                 [[1, 1, 1], [0, 1, 1], [0, 0, 1]]]
        transformed = []
        for x in bases[0]:
            transformed.append([])
            for y in bases[1]:
                value = [sum(x[i]*y[j]*tensor[i][j][t]
                             for i in range(s) for j in range(s)) % p for t in range(s)]
                transformed[-1].append(coordinates_in_basis(bases[2], value, p))
        mu = transformed
        constraints = []
        for i in range(s):
            for j in range(s):
                for t in range(s):
                    uv = [0]*(3*s*s)
                    uw = [0]*(3*s*s)
                    for a in range(s):
                        uv[a*s+i] += mu[a][j][t]
                        uv[s*s+a*s+j] -= mu[i][a][t]
                        uw[a*s+i] += mu[a][j][t]
                        uw[2*s*s+t*s+a] -= mu[i][j][a]
                    constraints.extend([uv, uw])
        triples = kernel(constraints, p)
        assert len(triples) == s
        first = [row[:s*s] for row in triples]
        assert len(rref(first, p)[0]) == s
        identity = [int(i == j) for i in range(s) for j in range(s)]
        coordinates_in_basis(first, identity, p)
        for u in first:
            for v in first:
                uv = [sum(u[i*s+a]*v[a*s+j] for a in range(s)) % p
                      for i in range(s) for j in range(s)]
                vu = [sum(v[i*s+a]*u[a*s+j] for a in range(s)) % p
                      for i in range(s) for j in range(s)]
                assert uv == vu
                coordinates_in_basis(first, uv, p)
        cases.append({"p": p, "algebra": algebra, "dimension": s,
                      "recovered_dimension": len(first), "identity_and_closure": True})
    return cases


def main():
    before = {str(path): sha256(path.read_bytes()).hexdigest() for path in SOURCES}
    report = {"boundary_checks": boundary_controls(),
              "below_length_counterexample": below_length_counterexample(),
              "coordinate_algebra": algebra_control(), "scope_control": scope_control(),
              "perfect_pairing_controls": perfect_pairing_control()}
    after = {str(path): sha256(path.read_bytes()).hexdigest() for path in SOURCES}
    assert before == after
    report["audited_source_sha256"] = before
    report["parent_files_unchanged"] = True
    report["status"] = "PASS: finite controls, not an all-input proof or arithmetic backend"
    destination = ROOT / "control_results.json"
    destination.write_text(json.dumps(report, indent=2)+"\n")
    print(report["status"])
    print(f"{len(report['boundary_checks'])} exact equality/scaling controls")
    print(json.dumps({k: v for k, v in report.items() if k != "boundary_checks"}, indent=2))


if __name__ == "__main__":
    main()
