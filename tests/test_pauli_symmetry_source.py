"""Purity-gap deduction controls, not execution of a scalable quantum learner."""
from fractions import Fraction
from itertools import product
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from theorems.coisotropic_symmetry import maximal_isotropic_subspace
from theorems.pauli_symmetry_source import (
    PurityGapPlan, collision_estimate, period_candidates,
    reference_translation_profile, symmetry_decision,
)
from theorems.ut5_matrix_phase_alignment import (
    _rank, extend_symplectic_isometry, symplectic_pair,
)
from theorems.prime_clifford_realization import compile_symplectic, symplectic_action


@pytest.mark.parametrize("p,n,R,gap", [
    (3, 2, 8, Fraction(1, 36)), (3, 3, 27, Fraction(1, 10**4)),
    (101, 40, 3, Fraction(1, 20)), (2**127-1, 8, 4, Fraction(1, 100)),
])
def test_complete_clocks_charge_both_quantum_and_classical_copy_stages(p, n, R, gap):
    row = PurityGapPlan(p, n, R, gap).caps()
    assert row["zero_error_probability_lower_bound"] == Fraction(1, R**3)
    assert row["purity_lower_bound"] == Fraction(1, R)
    assert row["total_raw_copy_cap"] == (row["basis_stage_raw_copy_cap"]
                                        + row["period_stage_eigenbasis_measurement_copy_cap"])
    assert row["basis_stage_raw_copy_cap"] == (
        4*row["candidate_count_cap"] + 2*row["quantum_purity_and_overlap_estimate_count"]
        * row["swap_trials_per_estimate"])
    assert row["period_stage_eigenbasis_measurement_copy_cap"] == (
        row["heavy_anchor_sample_count"]+row["period_cover_sample_count"]
        + 2*row["classical_collision_estimate_count_cap"]*row["independent_pairs_per_collision_estimate"])
    assert row["no_good_chart_probability_bound"] <= Fraction(1, 24)
    assert sum(row["failure_budgets"].values()) == row["total_error_upper_bound"] == Fraction(1, 3)
    assert not row["full_quantum_learner_implemented"]
    assert not row["source_promises_certified"]
    assert not row["original_basis_identified"]
    assert not row["period_stage_requires_collective_quantum_measurements"]


def test_resource_clocks_have_no_numeric_prime_factor():
    assert PurityGapPlan(3, 5, 8, Fraction(1, 36)).caps() == (
        PurityGapPlan(2**127-1, 5, 8, Fraction(1, 36)).caps())
    assert PurityGapPlan(3, 5, 8, Fraction(1, 36)).direct_caps() == (
        PurityGapPlan(2**127-1, 5, 8, Fraction(1, 36)).direct_caps())


def test_preferred_direct_route_spans_full_group_without_chart_or_rank_n_stop():
    plan = PurityGapPlan(3, 2, 8, Fraction(1, 36))
    row = plan.direct_caps()
    assert row["symmetry_dimension_upper_bound"] == 4
    assert row["candidate_source_copy_cap"] == 8*row["candidate_count_cap"]
    assert row["verification_source_copy_cap"] == (
        2*(row["candidate_count_cap"]+1)*row["swap_trials_per_estimate"])
    assert row["total_raw_copy_cap"] == (row["candidate_source_copy_cap"]
                                        + row["verification_source_copy_cap"])
    assert row["total_raw_copy_cap"] < plan.caps()["total_raw_copy_cap"]
    assert sum(row["failure_budgets"].values()) == Fraction(1, 3)
    assert not row["random_clifford_chart_required"]
    assert not row["diagonalizing_basis_required"]
    assert not row["classical_eigenlabel_stage_required"]
    assert not row["full_quantum_learner_implemented"]


def test_tighter_gap_and_failure_budget_are_paid():
    base = PurityGapPlan(3, 2, 8, Fraction(1, 36)).caps()
    tight = PurityGapPlan(3, 2, 8, Fraction(1, 72), Fraction(1, 10)).caps()
    assert tight["swap_trials_per_estimate"] > 4*base["swap_trials_per_estimate"]
    assert tight["heavy_anchor_sample_count"] > base["heavy_anchor_sample_count"]
    assert tight["total_error_upper_bound"] == Fraction(1, 10)


def weights2():
    return {(a, b): Fraction((3, 2, 1)[b], 18) for a, b in product(range(3), repeat=2)}


def pauli(p, x, z):
    local = [np.diag(np.exp(2j*np.pi*b*np.arange(p)/p)) @ np.roll(np.eye(p), a, axis=0)
             for a, b in zip(x, z)]
    result = np.array([[1]], dtype=complex)
    for matrix in local:
        result = np.kron(result, matrix)
    return result


def test_full_rank_actual_density_has_noncommuting_symmetry_group_and_exact_gap():
    weights = weights2()
    reference = reference_translation_profile(3, 2, weights)
    assert reference["purity"] == Fraction(7, 54)
    assert reference["periods"] == ((0, 0), (1, 0), (2, 0))
    assert reference["smallest_positive_loss"] == Fraction(1, 36)
    assert reference["four_equal_label_probability"] >= reference["purity_cubed_lower_bound"]
    rho = np.diag([float(w) for w in weights.values()])
    assert np.linalg.matrix_rank(rho) == 9
    members = []
    for label in product(range(3), repeat=4):
        W = pauli(3, label[:2], label[2:])
        loss = np.trace(rho@rho-rho@W@rho@W.conj().T).real
        assert loss == pytest.approx(0 if label[1] == 0 else 1/36)
        if abs(loss) < 1e-12:
            members.append(label)
    assert len(members) == 27
    algebra = maximal_isotropic_subspace(3, 2, members)
    assert (algebra.span_dimension, algebra.radical_dimension, algebra.isotropic_dimension) == (3, 1, 2)
    assert any(symplectic_pair(a, b, 3) for a in members for b in members)
    # Two genuinely different maximal commuting bases diagonalize this rho.
    L0 = ((0, 0, 1, 0), (0, 0, 0, 1))
    L1 = ((1, 0, 0, 0), (0, 0, 0, 1))
    assert _rank(list(L0+L1), 3) == 3
    assert all(a in members for a in L0+L1)


def test_extracted_basis_feeds_existing_public_clifford_compiler():
    H = ((1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    L = maximal_isotropic_subspace(3, 2, H).n_generators
    target = ((0, 0, 1, 0), (0, 0, 0, 1))
    matrix, _ = extend_symplectic_isometry(3, L, target)
    plan = compile_symplectic(3, matrix)
    assert symplectic_action(3, 2, plan.gates) == matrix
    assert [tuple(sum(matrix[i][j]*v[j] for j in range(4)) % 3 for i in range(4))
            for v in L] == list(target)


def test_independent_translation_columns_are_not_a_valid_general_stopping_rule():
    # Both preserve I/3 tensor |+><+|, but their span has no Lagrangian.
    rows = ((1, 0, 0, 0), (0, 1, 1, 0))
    rho = np.kron(np.eye(3)/3, np.ones((3, 3))/3)
    for v in rows:
        W = pauli(3, v[:2], v[2:])
        assert np.allclose(W@rho@W.conj().T, rho)
    assert _rank([list(v[:2]) for v in rows], 3) == 2
    assert symplectic_pair(*rows, 3) != 0
    assert maximal_isotropic_subspace(3, 2, rows).n_generators is None


@pytest.mark.parametrize("t", [Fraction(1, 4), Fraction(1, 100), Fraction(1, 10**6)])
def test_gap_cannot_be_deduced_from_inverse_purity_alone(t):
    weights = {(b,): (1-t)/3+int(b == 0)*t for b in range(3)}
    row = reference_translation_profile(3, 1, weights)
    assert row["purity"] == (1+2*t*t)/3
    assert row["periods"] == ((0,),)
    assert row["smallest_positive_loss"] == t*t
    distance = sum(abs(w-Fraction(1, 3)) for w in weights.values())/2
    assert distance == 2*t/3
    uniform = reference_translation_profile(3, 1, {(b,): Fraction(1, 3) for b in range(3)})
    assert len(uniform["periods"]) == 3
    assert uniform["smallest_positive_loss"] is None


@pytest.mark.parametrize("t", [Fraction(1, 6), Fraction(1, 100), Fraction(1, 10**6)])
def test_gap_can_vanish_with_all_eigenvalues_bounded_away_from_zero(t):
    q = (Fraction(2, 3), Fraction(1, 6), Fraction(1, 6))
    r = (Fraction(1, 3)+t, Fraction(1, 3)-t, Fraction(1, 3))
    weights = {(i, j): r[i]*q[j] for i, j in product(range(3), repeat=2)}
    base = {(i, j): q[j]/3 for i, j in weights}
    profile = reference_translation_profile(3, 2, weights)
    assert min(weights.values()) >= Fraction(1, 36)
    assert profile["purity"] == Fraction(1, 6)+t*t
    assert profile["smallest_positive_loss"] == 3*t*t/2
    assert profile["period_group_order"] == 1
    assert reference_translation_profile(3, 2, base)["period_group_order"] == 3
    assert sum(abs(weights[x]-base[x]) for x in weights)/2 == t
    chi_squared = sum((weights[x]-base[x])**2/base[x] for x in weights)
    assert chi_squared == 6*t*t
    for a, b in product(range(3), repeat=2):
        loss = profile["purity"]-sum(w*weights[((i-a) % 3, (j-b) % 3)]
                                     for (i, j), w in weights.items())
        expected = (0 if not a and not b else 3*t*t/2 if not b
                    else Fraction(1, 12)+t*t/2 if not a
                    else Fraction(1, 12)+5*t*t/4)
        assert loss == expected


def test_small_loss_threshold_does_not_define_a_subgroup():
    weights = {(b,): Fraction(w, 20) for b, w in enumerate((5, 4, 3, 4, 4))}
    purity = sum(w*w for w in weights.values())
    losses = [purity-sum(w*weights[((b-f) % 5,)] for (b,), w in weights.items())
              for f in range(5)]
    assert purity == Fraction(41, 200)
    assert losses[1] == Fraction(1, 200)
    assert losses[2] == Fraction(3, 400) > losses[1]


@pytest.mark.parametrize("weights", [
    {(0,): Fraction(1)},
    {(0,): Fraction(1, 2), (1,): Fraction(1, 2)},
    {(0,): Fraction(1, 2), (1,): Fraction(1, 3), (2,): Fraction(1, 6)},
    {(i,): Fraction(1, 5) for i in range(5)},
])
def test_four_copy_zero_error_bound_uses_purity_not_peak_or_rank(weights):
    row = reference_translation_profile(5, 1, weights)
    assert row["four_equal_label_probability"] >= row["purity"]**3
    assert row["period_group_order"]*row["purity"] <= 1


def test_measured_eigenlabel_kernels_have_no_eigenweight_argument():
    # An exact-frequency finite control; NOT a random IID run or probability test.
    population = [label for label, w in weights2().items() for _ in range(int(18*w))]
    anchor, shifts = period_candidates(3, 2, population, list(weights2()))
    assert anchor == (0, 0)
    assert len(shifts) == 9
    purity = collision_estimate(3, 2, product(population, repeat=2), (0, 0))
    assert purity == Fraction(7, 54)
    accepted = [s for s in shifts if symmetry_decision(
        purity, collision_estimate(3, 2, product(population, repeat=2), s), Fraction(1, 36))]
    assert accepted == [(0, 0), (1, 0), (2, 0)]


def test_estimate_threshold_robust_to_both_errors_and_rejects_boundary():
    gap, purity = Fraction(1, 36), Fraction(7, 54)
    for e1, e2 in product((-gap/8, gap/8), repeat=2):
        assert symmetry_decision(purity+e1, purity+e2, gap)
        assert not symmetry_decision(purity+e1, purity-gap+e2, gap)
    assert not symmetry_decision(purity, purity-gap/2, gap)


@pytest.mark.parametrize("kwargs", [
    {"prime": 2}, {"prime": 9}, {"width": 0}, {"width": True},
    {"inverse_purity": 0}, {"inverse_purity": 1.0},
    {"gap": Fraction(0)}, {"gap": Fraction(2)}, {"gap": 0.1},
    {"error": Fraction(0)}, {"error": Fraction(1)},
])
def test_plan_rejects_invalid_supplied_promises(kwargs):
    arguments = dict(prime=3, width=2, inverse_purity=8, gap=Fraction(1, 36))
    arguments.update(kwargs)
    with pytest.raises(ValueError):
        PurityGapPlan(**arguments)


def test_reference_and_sample_kernels_refuse_malformed_or_unbounded_inputs():
    with pytest.raises(ValueError, match="cap"):
        reference_translation_profile(3, 100, {})
    with pytest.raises(ValueError, match="weights"):
        reference_translation_profile(3, 1, {(0,): Fraction(1, 2)})
    with pytest.raises(ValueError, match="canonical"):
        period_candidates(3, 1, [(3,)], [(0,)])
    with pytest.raises(ValueError, match="anchor"):
        period_candidates(3, 1, [], [(0,)])
    with pytest.raises(ValueError, match="pair"):
        collision_estimate(3, 1, [], (0,))
    with pytest.raises(ValueError, match="means"):
        symmetry_decision(0.5, Fraction(1, 2), Fraction(1, 4))


def test_cli_writes_scoped_source_bound_artifact_without_candidate_promotion(tmp_path, capsys):
    import qsearch
    prior = tmp_path/"research/reductions/peaked_phase_source.json"
    prior.parent.mkdir(parents=True)
    prior.write_text("previous report")
    args = qsearch.build_parser().parse_args(["phase-copy-baseline", "--pauli-symmetry", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    path = prior.with_name("pauli_symmetry_source.json")
    row = json.loads(path.read_text())
    assert row == json.loads(capsys.readouterr().out)
    assert prior.read_text() == "previous report"
    assert row["sample_profile"]["period_group_order"] == 3
    assert row["preferred_direct_caps"]["candidate_source_copy_cap"] > 0
    control = row["finite_skew_bell_control"]
    assert control["maximum_physical_fourier_discrepancy"] < 1e-10
    assert control["physical_probability_mass"] == pytest.approx(1)
    assert control["incorrect_pure_convolution_mass"] == pytest.approx(control["purity_fourth_power"])
    assert control["incorrect_pure_convolution_mass"] < 1/2
    assert not control["physical_quantum_execution"]
    assert row["public_noncommuting_span_control"]["isotropic_dimension"] == 2
    for key in ("quantum_learner_executed", "novelty_established", "speedup_claim_allowed",
                "source_promises_certified", "matched_classical_input_separation_established"):
        assert row[key] is False
    root = Path(qsearch.__file__).resolve().parent
    for source, digest in row["source_sha256"].items():
        assert hashlib.sha256((root/source).read_bytes()).hexdigest() == digest
    assert not (tmp_path/"research/registry/candidates.json").exists()


def test_cli_modes_exclusive_and_read_only_by_default(tmp_path, capsys, monkeypatch):
    import qsearch
    import theorems.pauli_symmetry_source as module
    parser = qsearch.build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["phase-copy-baseline", "--peaked-noise", "--pauli-symmetry"])
    monkeypatch.setattr(module, "report", lambda: {"quantum_learner_executed": False})
    args = parser.parse_args(["phase-copy-baseline", "--pauli-symmetry"])
    args.root = tmp_path
    assert args.func(args) == 0
    assert not list(tmp_path.iterdir())
