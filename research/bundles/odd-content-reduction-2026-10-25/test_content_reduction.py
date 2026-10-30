from pathlib import Path
import sys

import pytest
from sympy import Matrix, eye, zeros

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content_reduction import probe_schedule, recover_content
from controls_content import (
    content_control, ideal_scaling_control, noncyclic_endomorphism_control,
    preserves_smith_doubled,
)
from cyclic_source import affine_query, certificate_queries
from controls_cyclic import local_lines
from kernel_output import alternating_form, mod


@pytest.mark.parametrize("p,e,a", [(3, 1, 0), (3, 2, 0), (3, 2, 1), (3, 3, 1),
                                  (3, 4, 1), (3, 4, 2), (3, 5, 1),
                                  (5, 3, 0), (5, 3, 1), (5, 4, 2)])
def test_public_probes_recover_only_the_scalar_content(p, e, a):
    n, factors = p**e, ((p, e),)
    for vector in ((1, 0), (0, 1), (1, p), (1, p*p), (p, 1), (1, 1)):
        result = content_control(n, factors, {p: (e, a, vector)})
        assert result["content"] == p**a
        assert result["cyclic_residual_degree"] == p**(e-2*a)
        assert not result["direction_recovered"]
        assert not result["native_source_executed"]


def test_two_axes_are_required():
    result = content_control(3**5, ((3, 5),), {3: (5, 1, (1, 3))})
    assert result["components"][0]["thresholds"] == [1, 3]
    assert result["content"] == 3


def test_mixed_primary_scalar_component_and_public_query_legality():
    n, factors = 3**5*5**4, ((3, 5), (5, 4))
    result = content_control(n, factors, {3: (5, 1, (3, 1)), 5: (4, 2, (1, 0))})
    assert result["content"] == 75 and result["cyclic_residual_degree"] == 27
    form = alternating_form(2)
    for record in probe_schedule(n, factors):
        query, p = record["query"], record["key"][0]
        assert mod(query.T*form*query-form, n) == zeros(4)
        other = 5**4 if p == 3 else 3**5
        assert mod(query, other) == eye(4)


def test_pure_scalar_kernel_has_no_line_output():
    result = content_control(225, ((3, 2), (5, 2)),
                             {3: (2, 1, (1, 1)), 5: (2, 1, (1, 2))})
    assert result["content"] == 15 and result["cyclic_residual_degree"] == 1
    assert (15*eye(4)).det() == 225**2


@pytest.mark.parametrize("p,e,a", [(3, 3, 1), (3, 4, 1), (5, 3, 1)])
def test_full_level_certificates_resolve_only_the_residual_direction(p, e, a):
    n, d = p**e, e-2*a
    queries = certificate_queries((1, p), n, ((p, e),))
    for vector in local_lines(p, d):
        accepted = all(preserves_smith_doubled(q, p, e, a, vector) for q in queries)
        assert accepted == ((vector[1]-p*vector[0]) % (p**d) == 0)
    # Higher digits are immaterial, rather than falsely distinguished.
    assert all(preserves_smith_doubled(q, p, e, a, (1, p+p**d)) for q in queries)


def test_affine_lifts_preserve_residual_query_without_a_ring_embedding():
    n, m = 3**5, 3**3
    for a in (1, 2, 5):
        for u in (0, 1, 26):
            full, residual = affine_query(a, u, n), affine_query(a, u, m)
            assert mod(full, m) == residual
            assert int(full.det()) % n == 1


def test_original_ideal_not_merely_cyclic_residual_ideal():
    record = ideal_scaling_control()
    assert record["ideal_index"] == 243**2
    assert record["content"] == 3 and record["residual_degree"] == 27
    assert record["annihilates_original_supplied_kernel"]


def test_genuine_noncyclic_endomorphism_and_original_principal_ideal():
    result = noncyclic_endomorphism_control()
    assert result["content"] == 3 and result["residual_degree"] == 25
    assert result["reconstructed_ideal_equals_principal_left_ideal"]
    assert not result["unknown_kernel_recovered"]


@pytest.mark.parametrize("mutation", ["missing", "nonboolean", "nonmonotone", "parity", "terminal"])
def test_malformed_comparison_records_are_rejected(mutation):
    n, factors = 27, ((3, 3),)
    matches = {r["key"]: r["key"][2] >= 3 for r in probe_schedule(n, factors)}
    if mutation == "missing":
        matches.pop((3, "upper", 0))
    elif mutation == "nonboolean":
        matches[(3, "upper", 0)] = 0
    elif mutation == "nonmonotone":
        matches[(3, "upper", 0)] = True
    elif mutation == "parity":
        matches = {key: key[2] >= 2 for key in matches}
    else:
        matches[(3, "upper", 3)] = False
    with pytest.raises(ValueError):
        recover_content(n, factors, matches)
