"""Bounded independent arithmetic and distribution checks for the sidecar."""

from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import product
import json
from math import prod
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "snapshot/generic-divisor-class-2026-10-26"
spec = importlib.util.spec_from_file_location("reviewed_class_bound", SOURCE / "class_bound.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def exact_tower_bound(e):
    return Fraction((5*e+1)*3**(10*e+2), 100003**(3*e+9)*99225)


def elliptic_add(a, b):
    """Group law on the smooth curve y^2=x^3+2 over F_7."""
    if a is None:
        return b
    if b is None:
        return a
    x, y = a
    z, w = b
    if x == z and (y+w) % 7 == 0:
        return None
    slope = (3*x*x*pow(2*y, -1, 7) if a == b
             else (w-y)*pow(z-x, -1, 7)) % 7
    xx = (slope*slope-x-z) % 7
    return (xx, (slope*(x-xx)-y) % 7)


def main():
    bounds = {}
    for e in (8, 16, 32, 64, 128):
        g, d, n = 5*e+1, 10*e+3, 22*e
        a = (2*g-2)-3*d+n
        assert a == 2*e-9 and 0 < a < g-1
        assert g-a-1 == 3*e+9 and n > 2*d
        assert d-g+1 == 5*e+3 and 2*d-g+1 == 15*e+6
        b = exact_tower_bound(e)
        assert b == module.bad_class_upper(100003, g, a)
        assert b == module.tower_class_certificate(e)["bad_fraction_upper_under_uniform_Pic_d"]
        assert 0 < b < 1
        with localcontext() as ctx:
            ctx.prec = 45
            dec = str(Decimal(b.numerator)/Decimal(b.denominator))
        bounds[str(e)] = {"g": g, "d": d, "n": n, "a": a,
                          "rational_bound": str(b), "decimal_bound": dec}
    assert exact_tower_bound(8) < Fraction(1, 10**128)
    assert 316**2 < 100003 < 317**2
    ratio_cap = Fraction(2*3**10, 100003**3)
    assert ratio_cap < 1
    for e in range(1, 257):
        assert exact_tower_bound(e+1)/exact_tower_bound(e) < ratio_cap

    # Enumerate affine multiplication-by-three maps and every bad subset.
    cases = 0
    groups = [(n,) for n in range(1, 13)] + [(3, 3), (2, 3), (2, 2, 3)]
    for moduli in groups:
        group = list(product(*(range(n) for n in moduli)))
        h = len(group)
        assert h == prod(moduli)
        kernel = sum(all(3*x % n == 0 for x, n in zip(t, moduli)) for t in group)
        for offset in group:
            fibres = Counter(tuple((c-3*x) % n for c, x, n in zip(offset, t, moduli))
                             for t in group)
            assert set(fibres.values()) == {kernel}
            assert len(fibres)*kernel == h
            counts = [fibres[t] for t in group]
            for mask in range(1 << h):
                selected = [i for i in range(h) if mask >> i & 1]
                preimages = sum(counts[i] for i in selected)
                intersection = sum(bool(counts[i]) for i in selected)
                actual = Fraction(preimages, h)
                assert actual == Fraction(kernel*intersection, h)
                assert actual <= module.preimage_fraction_bound(h, kernel, len(selected))
                cases += 1

    points = [None]+[(x, y) for x in range(7) for y in range(7)
                    if (y*y-x*x*x-2) % 7 == 0]
    assert len(points) == 9
    assert all(elliptic_add(elliptic_add(a, a), a) is None for a in points)
    elliptic = {"curve": "y^2=x^3+2 over F_7", "points": points,
                "class_number": 9, "rational_3_torsion": 9,
                "zero_class_bad_fraction_under_tripling": "1",
                "incorrect_bound_without_torsion": "1/9"}

    # A sampler can concentrate on a rare bad class. TV error is additive.
    n = 101
    uniform = [Fraction(1, n)]*n
    point_mass = [Fraction(int(i == 0)) for i in range(n)]
    mixing = Fraction(1, 100)
    biased = [(1-mixing)*u+mixing*v for u, v in zip(uniform, point_mass)]
    tv = sum(abs(u-v) for u, v in zip(uniform, biased))/2
    assert biased[0] == uniform[0]+tv
    assert point_mass[0] == 1 and uniform[0] == Fraction(1, 101)

    for prime, genus, residual in [(5, 1, -1), (7, 1, 0), (100003, 41, -1),
                                   (100003, 41, 0), (100003, 41, 40)]:
        value = module.bad_class_upper(prime, genus, residual)
        assert 0 <= value <= 1
        if residual < 0:
            assert value == 0

    report = {"tower_bounds": bounds, "all_step_ratio_cap": str(ratio_cap),
              "finite_group_bad_subset_cases": cases,
              "elliptic_torsion_countercontrol": elliptic,
              "sampler_countercontrol": {"uniform_bad_fraction": str(uniform[0]),
                                         "biased_bad_fraction": str(biased[0]),
                                         "TV_distance": str(tv), "TV_bound_attained": True,
                                         "point_mass_bad_fraction": "1"},
              "native_generic_divisor_or_matrix_constructed": False,
              "source_tests_passed_separately": 14,
              "source_sha256": {p.name: sha256(p.read_bytes()).hexdigest()
                                for p in sorted(SOURCE.iterdir()) if p.is_file()}}
    (ROOT / "independent_generic_results.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"e8_bound": bounds["8"]["decimal_bound"],
                      "finite_group_cases": cases,
                      "elliptic_torsion_countercontrol": "PASS",
                      "TV_countercontrol": "PASS",
                      "source_sha256": report["source_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
