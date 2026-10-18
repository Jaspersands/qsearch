from fractions import Fraction
import json
import subprocess
import sys

import pytest

from theorems.dcp_adaptive_direction_rank_gate import decode_dyadic
from theorems.dcp_native_tree_variance_cap import (
    REPORT, build_report, cap_certificate, dependent_leaf_census, partial_pattern_census,
)


@pytest.mark.parametrize("depth", [1,2,3])
def test_partial_native_rank_patterns_agree_with_centered_list_moments(depth):
    C = partial_pattern_census(depth, 1)
    assert C["equality_patterns"] == 1 << (1 << depth)
    value = decode_dyadic(C["complete_partial_list_second_moment"])
    assert value > 16
    if depth == 1:
        assert value == 19 and decode_dyadic(C["complete_partial_list_variance"]) == 3


def test_non_iid_overlapping_support_census_preserves_exact_two_wise_moments():
    C = dependent_leaf_census()
    assert C["all_native_label_assignments"] == 65536
    assert C["leaf_entries_jointly_IID"] is False
    assert C["three_support_parity_constraint_always_zero"] is True
    assert C["partial_list_mean"] == "4" and C["partial_list_variance"] == "3"


@pytest.mark.parametrize("depth,chunk", [(1,1),(2,1),(3,1),(4,4),(4,8),(4,16),(4,32),(4,64)])
def test_exact_centered_cap_respects_overflow_incident_edge_loss(depth, chunk):
    C = cap_certificate(depth, chunk)
    S = decode_dyadic(C["sum_nonroot_full_list_variances"])
    M = decode_dyadic(C["root_graph_second_moment"])
    cap = int(C["centered_capacity_hex"], 16)
    L = int(C["leaf_list_length_hex"], 16)
    delta = Fraction(C["overflow_probability_upper_exact_rational"])
    assert cap >= L
    assert delta == S/(cap+1-L)**2
    assert M*delta <= Fraction(1,256)
    assert int(C["old_Markov_capacity_hex"], 16) > cap
    assert C["nodes_or_degree_and_overflow_assumed_independent"] is False
    assert C["existing_receiver_default_capacity_updated"] is False
    assert C["applies_to_silently_truncated_accepted_lists"] is False


def test_no_nonroot_nodes_requires_no_overflow_allowance():
    C = cap_certificate(1, 1)
    assert C["partial_list_variance_by_level"] == []
    assert C["centered_capacity_hex"] == "0x4"
    assert Fraction(C["overflow_probability_upper_exact_rational"]) == 0
    assert decode_dyadic(C["marked_overflow_loss_upper"]) == 0


def test_two_level_exact_nonroot_variance_and_integer_threshold():
    C = cap_certificate(2, 1)
    assert decode_dyadic(C["sum_nonroot_full_list_variances"]) == 6
    assert int(C["centered_capacity_hex"], 16) == 71
    assert int(C["integer_deviation_threshold_hex"], 16) == 68
    assert Fraction(C["capacity_reduction_factor_exact_rational"]) == Fraction(12288,71)


def test_second_partial_level_from_native_first_level_census_not_degree_moment():
    # Conditional second-moment identity with independent disjoint children.
    first_second = Fraction(dependent_leaf_census()["partial_list_second_moment"])
    next_second = first_second**2 / 16 + 3
    next_variance = next_second-16
    assert next_second == Fraction(409,16)
    assert next_variance == Fraction(153,16)
    C = cap_certificate(3,1)
    assert decode_dyadic(C["sum_nonroot_full_list_variances"]) == 4*3 + 2*next_variance == Fraction(249,8)


def test_geometric_variance_bound_when_list_size_dominates_tree():
    for a,b in ((2,2),(3,2),(4,3),(4,8)):
        C = cap_certificate(a,b)
        k,L = C["leaf_count"], int(C["leaf_list_length_hex"],16)
        S = decode_dyadic(C["sum_nonroot_full_list_variances"])
        assert L >= 2*(k-1)
        assert S < 2*(a-1)*k*L


def test_live_artifact_matches_and_cli_is_readonly():
    assert json.loads(REPORT.read_text()) == json.loads(json.dumps(build_report()))
    before = REPORT.read_bytes()
    result = subprocess.run([sys.executable,"qsearch.py","dcp-native-tree-variance-cap","--no-write"],capture_output=True,text=True)
    assert result.returncode == 0,result.stderr
    assert REPORT.read_bytes() == before
