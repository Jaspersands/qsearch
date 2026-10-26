"""Controls for the standalone five-step guarded cyclic-H dispatcher and 127-bit row compression."""
from fractions import Fraction
import json
import random

import pytest

from theorems.nil3_cocycle_receiver import learn_quotient_line
from theorems.nil3_guarded_cyclic_dispatch import (
    REPORT, NormalWordLieBridge, abelian_bridge, adapted_presentation_exact,
    conic_failure_bound, filiform_class_three_bridge, guarded_cyclic_dispatch,
    independent_columns_exact, normal_word_coset_fixture, square_weights_capped,
)


def heisenberg_bridge(p=11):
    """3D Heisenberg normal words X^a Z^b Y^c with m=2, n=1 (224 cosets/output)."""

    def collect(left, right):
        a, b, c = left
        x, y, z = right
        return (a + x) % p, (b + y - x * c) % p, (c + z) % p

    return NormalWordLieBridge(p, 3, collect)


def test_127bit_prime_row_compression_and_capped_conic_solver():
    p = (1 << 127) - 1
    assert p % 4 == 3
    rng = random.Random(2026102101)
    base = [[rng.randrange(p) for _ in range(4)] for _ in range(2)]
    columns = [
        [(c0 * a + c1 * b) % p for a, b in zip(base[0], base[1])]
        for c0, c1 in [
            (1, 0),
            (0, 1),
            (3, 5),
            (7, 11),
            (0, 0),
            (13, 17),
            (19, 23),
            (29, 31),
            (37, 41),
        ]
    ]
    compressed, rank = independent_columns_exact(columns, p)
    assert rank == 2
    assert len(compressed) == len(columns) == 9
    weights = square_weights_capped(p, columns, rng, conic_attempt_cap=64)
    assert any(weights)
    assert all(
        sum(col[j] * w * w for col, w in zip(columns, weights)) % p == 0
        for j in range(4)
    )
    bound = conic_failure_bound(p, 16)
    assert bound == Fraction(p - 1, 2 * p) ** 16 < Fraction(1, 1 << 16)


def test_conic_exhaustion_and_invalid_parameters_fail_closed():
    p = 11
    cols = [[1], [1], [1], [1]]

    class AlwaysNonSquareY2:
        def randrange(self, modulus):
            # For p=11, x=0 gives y2 = -1 = 10, which is a non-square mod 11.
            return 0

    with pytest.raises(RuntimeError, match="bounded conic sampler exhausted"):
        square_weights_capped(p, cols, AlwaysNonSquareY2(), conic_attempt_cap=4)
    with pytest.raises(ValueError, match="p=3 mod 4"):
        conic_failure_bound(5, 4)
    with pytest.raises(ValueError, match="conic_attempt_cap"):
        square_weights_capped(p, cols, random.Random(0), conic_attempt_cap=0)


def test_unmodified_learn_quotient_line_rejects_or_misclassifies_trivial_h():
    bridge = filiform_class_three_bridge(11)
    group, _, _ = adapted_presentation_exact(bridge)
    trivial_coset = {group.zero: 1.0 + 0j}
    with pytest.raises(ValueError, match="nonzero quotient-line source promise failed"):
        learn_quotient_line(group, lambda: trivial_coset, random.Random(5))


@pytest.mark.parametrize(
    "expected_case,gen_word",
    [
        ("TRIVIAL", (0, 0, 0)),
        ("NORMAL_CYCLIC", (0, 4, 0)),
        ("TRANSVERSE_CYCLIC", (2, 3, 5)),
    ],
)
def test_guarded_dispatch_handles_trivial_normal_and_transverse_on_normal_words(
    expected_case, gen_word
):
    p = 11
    bridge = heisenberg_bridge(p)
    source_rng = random.Random(700 + sum(gen_word))
    dispatch_rng = random.Random(800 + sum(gen_word))
    calls = 0

    def source():
        nonlocal calls
        calls += 1
        rep = tuple(source_rng.randrange(p) for _ in range(bridge.dimension))
        return normal_word_coset_fixture(bridge, gen_word, rep)

    result = guarded_cyclic_dispatch(
        bridge, source, error=Fraction(1, 3), rng=dispatch_rng
    )
    assert result["status"] == "SUCCESS"
    assert result["case"] == expected_case
    assert result["source_copies"] == calls
    expected_subgroup = {bridge.power(gen_word, t) for t in range(p)}
    assert result["learned_subgroup"] == expected_subgroup


def test_guarded_dispatch_routes_abelian_ambient_presentations():
    p = 11
    bridge = abelian_bridge(p, 3)
    for expected_case, gen_word in [
        ("ABELIAN_TRIVIAL", (0, 0, 0)),
        ("ABELIAN_CYCLIC", (1, 4, 8)),
    ]:
        source_rng = random.Random(900 + sum(gen_word))
        dispatch_rng = random.Random(950 + sum(gen_word))
        calls = 0

        def source():
            nonlocal calls
            calls += 1
            rep = tuple(source_rng.randrange(p) for _ in range(3))
            return normal_word_coset_fixture(bridge, gen_word, rep)

        result = guarded_cyclic_dispatch(
            bridge, source, error=Fraction(1, 3), rng=dispatch_rng
        )
        assert result["status"] == "SUCCESS"
        assert result["case"] == expected_case
        assert result["ambient_abelian"]
        assert result["source_copies"] == calls
        assert result["learned_subgroup"] == {bridge.power(gen_word, t) for t in range(p)}


def test_incomplete_rank_is_recorded_as_failure_not_a_fabricated_subgroup():
    p = 11
    # 1. Normal stage on n=2 (filiform class-3) where 1 sample is (0, 0) -> nullity = 2 > 1
    filiform = filiform_class_three_bridge(p)

    class ZeroChoiceRandom(random.Random):
        def choices(self, population, weights=None, *, cum_weights=None, k=1):
            return [population[0]]

    res_norm = guarded_cyclic_dispatch(
        filiform,
        lambda: normal_word_coset_fixture(filiform, filiform.zero, filiform.zero),
        rng=ZeroChoiceRandom(1),
        normal_sample_override=1,
    )
    assert res_norm["status"] == "INCOMPLETE_NORMAL_RANK_FAILURE"
    assert res_norm["generators"] is None

    # 2. Quotient stage on m=2 (heisenberg_bridge) where normal stage passes (n=1, 1 nonzero sample)
    # and quotient stage draws (0, 0) once -> nullity = 2 > 1
    heis = heisenberg_bridge(p)

    class NonzeroThenZeroChoiceRandom(random.Random):
        def __init__(self, seed):
            super().__init__(seed)
            self.calls = 0

        def choices(self, population, weights=None, *, cum_weights=None, k=1):
            self.calls += 1
            # Call 1 is choosing q_obs in sample_normal_intersection_frequency;
            # Call 2 is sample_fourier on N (pick index 1 -> nonzero);
            # Call 3 is sample_fourier on V (pick index 0 -> (0, 0)).
            if self.calls == 2:
                return [population[1]]
            return [population[0]]

    res_quot = guarded_cyclic_dispatch(
        heis,
        lambda: normal_word_coset_fixture(heis, heis.zero, heis.zero),
        rng=NonzeroThenZeroChoiceRandom(2),
        normal_sample_override=1,
        quotient_sample_override=1,
    )
    assert res_quot["status"] == "INCOMPLETE_QUOTIENT_RANK_FAILURE"
    assert res_quot["generators"] is None

    # 3. Abelian d=3 with 1 sample -> nullity >= 2!
    ab = abelian_bridge(p, 3)
    res_ab = guarded_cyclic_dispatch(
        ab,
        lambda: normal_word_coset_fixture(ab, ab.zero, ab.zero),
        rng=random.Random(9012),
        normal_sample_override=1,
    )
    assert res_ab["status"] == "INCOMPLETE_ABELIAN_RANK_FAILURE"
    assert res_ab["generators"] is None


def test_saved_report_verifies_all_cases_and_honest_scope_flags():
    saved = json.loads(REPORT.read_text())
    assert [c["dispatched_case"] for c in saved["cases_executed"]] == [
        "TRIVIAL",
        "NORMAL_CYCLIC",
        "TRANSVERSE_CYCLIC",
        "ABELIAN_TRIVIAL",
        "ABELIAN_CYCLIC",
    ]
    assert all(c["recovered_exact_subgroup"] for c in saved["cases_executed"])
    bridge = filiform_class_three_bridge(saved["prime"])
    for case in saved["cases_executed"][:3]:
        gen = tuple(case["generator_fixture"])
        expected_sub = {bridge.power(gen, t) for t in range(saved["prime"])}
        if case["returned_generators"]:
            ret_gen = tuple(case["returned_generators"][0])
            assert {bridge.power(ret_gen, t) for t in range(saved["prime"])} == expected_sub
        else:
            assert expected_sub == {bridge.zero}
    assert saved["large_prime_127bit_backend_control"]["prime_bits"] == 127
    assert saved["large_prime_127bit_backend_control"]["square_relation_verified"]
    assert saved["full_rank_m_permitted_for_trivial_H"]
    assert saved["incomplete_rank_recorded_as_failure"]
    assert not saved["stops_at_m_minus_one_on_trivial_H"]
    assert not saved["ideal_learned_direction_injected"]
    assert not saved["iss_outer_normalizer_recursion_executed"]
    assert not saved["black_box_presentation_acquisition_executed"]
    assert not saved["general_prime_sde_backend_executed"]
    assert not saved["full_nil3_hsp_claim_admitted"]
    assert not saved["novelty_established"]
