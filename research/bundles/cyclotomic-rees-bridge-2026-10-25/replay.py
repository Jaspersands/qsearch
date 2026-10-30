"""Reproduce the exact bridge falsifiers; no native secret search."""

import argparse
import hashlib
import json
from pathlib import Path
import platform

import flint
from flint import fmpz_mat

from bridge_controls import (CyclotomicRing, evaluate_mod, exact_phase_fidelity,
                             fermat_null_polynomial, newton_dilation,
                             newton_dilation_matrix, parameters)


ROOT = Path(__file__).resolve().parent
FILES = ("bridge_controls.py", "test_bridge_controls.py", "replay.py",
         "CYCLOTOMIC_BRIDGE.md", "HANDOFF.md")
DEPENDENCIES = (
    "rees-formal-core-2026-10-24/REES_RESOURCE_AND_PRIOR_ART.md",
    "rees-independent-review-2026-10-23/source/REES_HSP_REDUCTION.md",
    "rees-class-three-2026-10-24/class_three.py",
    "rees-class-three-2026-10-24/test_class_three.py",
    "rees-class-three-2026-10-24/receipt.json",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report():
    ring = CyclotomicRing(3, 2)
    ideals = [len(ring.ideal(k)) for k in range(ring.L+1)]
    assert ideals == [81, 27, 9, 3, 1]
    null_rows = []
    for p, t in ((2, 2), (2, 5), (3, 2), (3, 3), (5, 2), (7, 2)):
        coefficients = fermat_null_polynomial(p, t)
        zero_count = sum(evaluate_mod(coefficients, s, p**t) == 0 for s in range(p**t))
        assert zero_count == p**t and coefficients[1] and coefficients[p]
        null_rows.append({"p": p, "t": t, "coefficients": coefficients,
                          "all_scalar_evaluations_zero": True,
                          "scalar_evaluations_checked": zero_count})
    dilation = newton_dilation_matrix(4, 4)
    identity = fmpz_mat([[int(i == j) for j in range(4)] for i in range(4)])
    residue = lambda matrix: [[int(matrix[i, j]) % 3 for j in range(4)] for i in range(4)]
    assert residue(dilation) != residue(identity)
    assert residue((dilation-identity)**2) == [[0]*4 for _ in range(4)]
    assert residue(dilation**3) == residue(identity)
    general_unipotent = []
    for p in (2, 3, 5, 7, 11, 13):
        action = newton_dilation_matrix(p, 1+p)
        expected = [[int(i == j)+int(i == 0 and j == p-1)
                     for j in range(p)] for i in range(p)]
        actual = [[int(action[i, j]) % p for j in range(p)] for i in range(p)]
        assert actual == expected
        general_unipotent.append({"p": p, "scale": 1+p, "degree": p,
                                 "identity_plus_E_1_p": True})
    left, right = ring.hidden(0), ring.hidden(3)
    reduce = lambda subgroup: {(tuple(c % 3 for c in x), a) for x, a in subgroup}
    assert left != right and reduce(left) == reduce(right)
    phases = [ring.phase(ring.zeta, s) for s in (0, 3)]
    fidelity = exact_phase_fidelity(*phases)
    assert str(fidelity) == "1/3"
    normalizers = []
    for secret in (0, 1, 3):
        generator = ring.scalar(secret), 1
        actual = set()
        for x in ring.elements():
            for a in range(ring.p):
                g = x, a
                conjugate = ring.group_mul(ring.group_mul(g, generator), ring.group_inverse(g))
                if conjugate == generator:
                    actual.add(g)
        expected = {(ring.add(ring.mul(ring.lam(a), ring.scalar(secret)), z), a)
                    for a in range(ring.p) for z in ring.ideal(ring.L-1)}
        assert actual == expected and len(actual) == 9
        normalizers.append({"secret_for_control_only": secret, "order": len(actual),
                            "group_elements_checked": 243, "formula_matches": True})
    return {
        "scope": "exact falsifiers of naive Rees-to-cyclotomic bridge, not a CCP solver",
        "primary_source": "https://arxiv.org/html/2609.34996v1",
        "runtime": {"python": platform.python_version(), "python_flint": flint.__version__},
        "parameters": [parameters(p, t, n=17) for p, t in
                       ((2, 1), (2, 5), (3, 1), (3, 2), (5, 1), (5, 4), (127, 3))],
        "fermat_null_polynomial_controls": null_rows,
        "native_ring": {"p": 3, "q": 9, "n": 1, "class": 4,
                        "ring_order": 81, "group_order": 243,
                        "ideal_orders": ideals, "pairing_matrix": ring.pairing_matrix()},
        "newton_repair": {"degree_four_scale_two": newton_dilation(4, 2),
                          "scale_four_matrix_mod_three": residue(dilation),
                          "nonzero_nilpotent_part_square": residue((dilation-identity)**2),
                          "dilation_order": 3,
                          "general_unipotent_controls": general_unipotent,
                          "scalar_diagonalization_possible": False},
        "secret_digit_control": {"distinct_original_subgroups": True,
                                 "equal_mod_three_images": True,
                                 "label": list(ring.zeta),
                                 "phase_exponents": [[str(x) for x in row] for row in phases],
                                 "fidelity": str(fidelity)},
        "normalizers": normalizers,
        "not_established": {"native_search_algorithm": True, "polynomial_copy_receiver": True,
                            "classical_hardness": True, "quantum_advantage": True,
                            "LWE_consequence": True, "independent_review": True},
        "source_sha256": {name: digest(ROOT/name) for name in FILES},
        "frozen_dependency_sha256": {name: digest(ROOT.parent/name) for name in DEPENDENCIES},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = json.dumps(report(), indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"Wrote {args.output}: {hashlib.sha256(output.encode()).hexdigest()}")
    else:
        print(output, end="")
