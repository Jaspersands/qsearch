#!/opt/anaconda3/bin/python
"""One exact F49 shifted-norm census; ANALYSIS ONLY, not a native attack.

H_a is calculated directly from the hidden polynomial for this falsifier.
No character decoder, high-prime Kopparty pipeline, or quantum operation
is executed. The standard-library driver invokes one local Sage worker.
"""

from collections import Counter
import itertools
import json
from pathlib import Path
import subprocess
import sys
import time

SAGE_PYTHON = "/opt/anaconda3/envs/qsearch-cas/bin/python"


def run_control():
    from sage.all import GF, PolynomialRing

    started = time.perf_counter()
    p, r = 7, 2
    base = GF(p)
    field = GF(p**r, name="w")
    w = field.gen()
    _, _, from_field = field.vector_space(map=True)
    ring = PolynomialRing(field, "X")
    X = ring.gen()
    base_ring = PolynomialRing(base, "T")
    # Every coordinate is explicit in the public basis (1,w). Lexicographic
    # element order is (constant coefficient, w coefficient).
    elements = [field(c0) + field(c1) * w for c0, c1 in itertools.product(range(p), repeat=r)]

    def coordinates(value):
        return [int(c) for c in from_field(field(value))]

    def quadratic_trit(value, order):
        if not value:
            return 0
        power = value ** ((order - 1) // 2)
        assert power in (1, -1)
        return 1 if power == 1 else -1

    def padded_sign(trit):
        # The phase convention is chi(0)=+1; its Boolean phase bit is 0.
        return trit if trit else 1

    def shifted_norm(poly, shift):
        H = ring.one()
        for i in range(r):
            conjugate = ring([coefficient ** (p**i) for coefficient in poly.list()])
            H *= conjugate(X + shift ** (p**i))
        assert H.degree() == r * poly.degree() and H.is_monic()
        assert all(coefficient**p == coefficient for coefficient in H.list())
        assert all(coordinates(coefficient)[1] == 0 for coefficient in H.list())
        descended = base_ring([base(coordinates(coefficient)[0]) for coefficient in H.list()])
        assert ring(descended) == H
        G = ring(descended)(X - shift)
        assert G % poly == 0
        return descended, G

    Q0 = X**2 + 1
    # ONE deterministic nonbase irreducible quadratic. Its selection order
    # is (c0_constant,c0_w,c1_constant,c1_w) for X^2+c1*X+c0.
    Q1 = None
    choice_tests = 0
    choice_coordinates = None
    for c0 in elements:
        for c1 in elements:
            if coordinates(c0)[1] == 0 and coordinates(c1)[1] == 0:
                continue
            candidate = X**2 + c1 * X + c0
            choice_tests += 1
            if candidate.is_irreducible():
                Q1 = candidate
                choice_coordinates = coordinates(c0) + coordinates(c1)
                break
        if Q1 is not None:
            break
    assert Q1 is not None and Q1.is_irreducible()
    assert Q0.is_squarefree() and Q1.is_squarefree()

    results = []
    for name, poly in (("Q0_base_coefficient_squarefree", Q0), ("Q1_nonbase_irreducible", Q1)):
        case_started = time.perf_counter()
        rows = []
        by_shift = {}
        all_trit_matches = True
        all_padded_sign_matches = True
        all_padded_bit_matches = True
        zero_evaluations = 0
        for shift in elements:
            H, G = shifted_norm(poly, shift)
            triples = []
            for t in range(p):
                left = quadratic_trit(poly(field(t) + shift), p**r)
                right = quadratic_trit(H(base(t)), p)
                left_sign, right_sign = padded_sign(left), padded_sign(right)
                left_bit, right_bit = (1 - left_sign) // 2, (1 - right_sign) // 2
                all_trit_matches &= left == right
                all_padded_sign_matches &= left_sign == right_sign
                all_padded_bit_matches &= left_bit == right_bit
                assert left == right and left_sign == right_sign and left_bit == right_bit
                zero_evaluations += left == 0
                triples.append({"t": t, "trit_K": left, "trit_base": right,
                                "padded_sign_K": left_sign, "padded_sign_base": right_sign,
                                "padded_phase_bit_K": left_bit, "padded_phase_bit_base": right_bit})
            squarefree = H.is_squarefree()
            row = {"shift_coordinates": coordinates(shift), "H_over_base": str(H),
                   "H_squarefree": bool(squarefree), "G_over_extension": str(G),
                   "Q_divides_G": True, "label_checks": triples}
            rows.append(row)
            by_shift[tuple(coordinates(shift))] = (H, G, squarefree)
        if poly == Q0:
            assert ring(by_shift[(0, 0)][0]) == Q0**2
        accepted = [shift for shift in elements if by_shift[tuple(coordinates(shift))][2]]
        degree_counts = Counter()
        exact_recoveries = 0
        witness_pair = None
        # Ordered pairs include equal shifts; no failures are discarded.
        for shift_a, shift_b in itertools.product(accepted, repeat=2):
            Ha, Ga, _ = by_shift[tuple(coordinates(shift_a))]
            Hb, Gb, _ = by_shift[tuple(coordinates(shift_b))]
            gcd_poly = Ga.gcd(Gb).monic()
            assert gcd_poly % poly == 0
            degree_counts[int(gcd_poly.degree())] += 1
            if gcd_poly.degree() == 2:
                assert gcd_poly == poly
                exact_recoveries += 1
                if witness_pair is None:
                    witness_pair = {"a_coordinates": coordinates(shift_a), "b_coordinates": coordinates(shift_b),
                                    "H_a": str(Ha), "H_b": str(Hb), "recovered_gcd": str(gcd_poly)}
        assert witness_pair is not None
        assert sum(degree_counts.values()) == len(accepted)**2
        results.append({
            "name": name, "Q": str(poly), "Q_monic": bool(poly.is_monic()),
            "Q_squarefree": bool(poly.is_squarefree()), "Q_irreducible_over_K": bool(poly.is_irreducible()),
            "shifts_tested": len(elements), "base_points_per_shift": p,
            "trit_identities_checked": len(elements) * p,
            "all_trit_identities": bool(all_trit_matches),
            "all_padded_sign_identities": bool(all_padded_sign_matches),
            "all_padded_bit_identities": bool(all_padded_bit_matches),
            "zero_evaluations_in_census": int(zero_evaluations),
            "H_squarefree_count": len(accepted), "H_nonsquarefree_count": len(elements) - len(accepted),
            "H_zero_shift_equals_Q_squared": bool(ring(by_shift[(0, 0)][0]) == poly**2),
            "ordered_pairs_both_H_squarefree": len(accepted)**2,
            "gcd_degree_histogram": dict(sorted(degree_counts.items())),
            "Q_divides_every_pair_gcd": True,
            "accepted_degree_two_count": exact_recoveries,
            "every_accepted_degree_two_gcd_is_exact_Q": True,
            "one_exact_recovery_pair": witness_pair,
            "shift_rows": rows,
            "seconds": time.perf_counter() - case_started,
        })
    output = {
        "scope": "ANALYSIS ONLY: H_a was computed directly from hidden Q. One tiny exact census, not native attack execution, high-prime line decoding, quantum execution, or asymptotic evidence.",
        "p": p, "r": r, "K_order": p**r, "K_modulus": str(field.modulus()),
        "coordinate_basis": "(1,w), lexicographic coordinate tuples",
        "Q1_selection_order": "lex (c0_constant,c0_w,c1_constant,c1_w) for X^2+c1*X+c0; require a nonbase coefficient and irreducibility",
        "Q1_selected_coefficient_coordinates": choice_coordinates,
        "Q1_irreducibility_tests_before_selection": choice_tests,
        "padding_convention": "chi trit 0 maps to padded sign +1 and Boolean phase bit 0",
        "H_formula": "product_i Q^(p^i)(T+a^(p^i)), coefficient Frobenius only",
        "G_formula": "H_a(X-a)", "results": results,
        "total_worker_seconds": time.perf_counter() - started,
    }
    artifact = Path(__file__).with_suffix(".json")
    artifact.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"artifact": str(artifact), "Q1": str(Q1), "cases": [
        {key: result[key] for key in ("name", "Q", "H_squarefree_count", "H_nonsquarefree_count",
                                     "gcd_degree_histogram", "accepted_degree_two_count", "one_exact_recovery_pair", "seconds")}
        for result in results], "worker_seconds": output["total_worker_seconds"]}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--sage-worker"]:
        run_control()
    elif not sys.argv[1:]:
        subprocess.run([SAGE_PYTHON, str(Path(__file__).resolve()), "--sage-worker"], check=True, timeout=30)
    else:
        raise SystemExit("Usage: extension_norm_gcd_control.py")
