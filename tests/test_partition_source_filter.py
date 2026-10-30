"""Exact finite kernel controls and independent physical-density checks."""
from fractions import Fraction
from itertools import product
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from theorems.partition_source_filter import (
    nonuniform_layer, reference_partition, repeated_nonuniform_layer, singleton_partition,
)


@pytest.mark.parametrize("n,f,purity,gap,d_size,t_size,h_size,valid", [
    (2, nonuniform_layer, Fraction(5, 27), Fraction(2, 27), 3, 3, 9, True),
    (3, repeated_nonuniform_layer, Fraction(5, 81), Fraction(2, 81), 3, 9, 81, True),
    (3, lambda x: (0, x[1]) if x[2] == 0 else (1, x[0]) if x[2] == 1 else (2, x[0], x[1]),
     Fraction(7, 81), Fraction(1, 27), 9, 9, 27, True),
    (2, singleton_partition, Fraction(65, 81), Fraction(14, 81), 9, 1, 1, False),
    (1, tuple, Fraction(1, 3), None, 1, 3, 9, True),
    (1, lambda x: None, Fraction(1), Fraction(1), 3, 3, 3, True),
])
def test_exact_global_gap_and_full_pauli_group(n, f, purity, gap, d_size, t_size, h_size, valid):
    row = reference_partition(n, f)
    assert row["purity"] == purity
    assert row["minimum_positive_loss"] == gap
    assert len(row["collision_difference_span"]) == d_size
    assert len(row["translation_symmetries"]) == t_size
    assert len(row["pauli_symmetries"]) == h_size
    assert row["stabilizer_diagonal"] is valid
    assert sum(row["fiber_sizes"]) == 3**n
    assert row["purity"] <= Fraction(1, row["quotient_size"])


@pytest.mark.parametrize("f", [nonuniform_layer, singleton_partition])
def test_exact_losses_match_direct_complex_density_matrix(f):
    n, p = 2, 3
    points = list(product(range(p), repeat=n))
    rho = np.array([[f(x) == f(y) for y in points] for x in points], dtype=float)/len(points)
    assert np.linalg.eigvalsh(rho).min() >= -1e-12
    exact = reference_partition(n, f)
    for label, loss in exact["pauli_losses"]:
        x, z = label[:n], label[n:]
        W = np.array([[1]], dtype=complex)
        for a, b in zip(x, z):
            local = np.diag(np.exp(2j*np.pi*b*np.arange(p)/p))@np.roll(np.eye(p), a, axis=0)
            W = np.kron(W, local)
        physical = np.trace(rho@rho-rho@W@rho@W.conj().T).real
        assert physical == pytest.approx(float(loss), abs=1e-12)


def test_equality_not_label_periodicity_is_the_target():
    row = reference_partition(1, tuple)
    # Every nonzero shift changes the label, but the equality relation is unchanged.
    assert tuple((1,)) != tuple((0,))
    assert row["translation_symmetries"] == ((0,), (1,), (2,))
    assert len(row["pauli_symmetries"]) == 9


def test_arbitrary_unhashable_label_encoding_preserves_reference():
    original = reference_partition(2, nonuniform_layer)
    renamed = reference_partition(2, lambda x: ["opaque", list(nonuniform_layer(x))])
    assert renamed == original


def test_coarse_hash_cannot_identify_original_hidden_subgroup():
    def original(x):
        return x[1], x[2]

    def hash_label(y):
        b, c = y
        return c, 0 if c == 0 else b

    coarse = lambda x: hash_label(original(x))
    before, after = reference_partition(3, original), reference_partition(3, coarse)
    assert len(before["collision_difference_span"]) == 3
    assert len(after["collision_difference_span"]) == 9
    assert set(before["collision_difference_span"]) < set(after["collision_difference_span"])
    # The identical coarse source can also arise from the injective oracle x->x.
    assert reference_partition(3, lambda x: coarse(tuple(x))) == after
    assert after["stabilizer_diagonal"]


def test_one_qudit_partition_classification_is_not_purity_only():
    # All five partitions of three inputs, independently listed.
    partitions = ((0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (0, 1, 2))
    rows = [reference_partition(1, lambda x, labels=labels: labels[x[0]]) for labels in partitions]
    assert [r["stabilizer_diagonal"] for r in rows] == [True, False, False, False, True]
    assert all(r["purity"] == Fraction(5, 9) for r in rows[1:4])


def test_affine_fibers_alone_do_not_imply_one_common_stabilizer_basis():
    def f(x):
        if x[1] == x[2] == 0:
            return ("line_x",)
        if x[0] == 0 and x[2] == 1:
            return ("line_y",)
        return ("singleton",)+x
    row = reference_partition(3, f)
    assert row["fiber_sizes"] == [1]*21+[3, 3]
    assert len(row["collision_difference_span"]) == 9
    assert len(row["translation_symmetries"]) == 1
    assert not row["stabilizer_diagonal"]


def test_fresh_hash_averaging_increases_purity_but_erases_subgroup_from_full_H():
    p, points = 3, list(product(range(3), repeat=2))
    sources, groups = [], []
    for coordinate in (0, 1):
        labels = [x[coordinate] for x in points]
        rho = np.array([[a == b for b in labels] for a in labels], dtype=float)/9
        # All eight binary hashes: exact pairwise collision probability 1/2.
        average = np.zeros((9, 9))
        for h in product(range(2), repeat=3):
            average += np.array([[h[a] == h[b] for b in labels] for a in labels])/72
        assert np.allclose(average, rho/2+np.ones((9, 9))/18)
        purity = np.trace(average@average).real
        assert purity == pytest.approx(1/2)
        members, positive = [], []
        for label in product(range(p), repeat=4):
            x, z = label[:2], label[2:]
            W = np.array([[1]], dtype=complex)
            for a, b in zip(x, z):
                W = np.kron(W, np.diag(np.exp(2j*np.pi*b*np.arange(p)/p))
                            @np.roll(np.eye(p), a, axis=0))
            loss = purity-np.trace(average@W@average@W.conj().T).real
            if abs(loss) < 1e-12:
                members.append(label)
            else:
                positive.append(loss)
        assert min(positive) == pytest.approx(1/4)
        groups.append(set(members))
        sources.append(average)
    assert groups[0] == groups[1] == {x+(0, 0) for x in points}
    assert not np.allclose(sources[0], sources[1])


def test_flagged_high_purity_source_keeps_hidden_information_outside_full_group():
    groups = []
    for coordinate in (1, 2):
        def f(x):
            return (x[0], x[coordinate]) if x[0] == 1 else (x[0],)
        row = reference_partition(3, f)
        assert row["stabilizer_diagonal"]
        assert row["purity"] == Fraction(7, 27)
        assert row["minimum_positive_loss"] == Fraction(2, 27)
        expected = {(0, a, b, c, 0, 0) for a, b, c in product(range(3), repeat=3)}
        groups.append(set(row["pauli_symmetries"]))
        assert groups[-1] == expected
    assert groups[0] == groups[1]


def test_reference_domain_cap_is_enforced_before_evaluation():
    with pytest.raises(ValueError):
        reference_partition(4, lambda x: pytest.fail("must not evaluate outside cap"))


def test_cli_runs_actual_classical_attack_and_retains_scope(tmp_path, capsys):
    import qsearch
    args = qsearch.build_parser().parse_args(["phase-copy-baseline", "--partition-source", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    path = tmp_path/"research/classical_baselines/partition_source_filter.json"
    row = json.loads(path.read_text())
    assert row == json.loads(capsys.readouterr().out)
    assert row["status"] == "MATCHED_CLASSICAL_PARTITION_SOURCE_FILTER"
    for case in row["controls"]:
        assert case["generators_match_exact_reference"]
        run = case["classical_run"]
        assert run["status"] == "SUCCESS"
        assert 0 < run["counts"]["queries"] <= run["caps"]["query_bound"]
        assert not run["source_promises_certified"]
    assert not row["promise_violating_control"]["stabilizer_diagonal"]
    assert row["quantum_copies_consumed"] == 0
    assert not row["general_quantum_input_dequantized"]
    assert not row["new_speedup_claim_allowed"]
    root = Path(qsearch.__file__).resolve().parent
    for source, digest in row["source_sha256"].items():
        assert hashlib.sha256((root/source).read_bytes()).hexdigest() == digest
    assert not (tmp_path/"research/registry/candidates.json").exists()


def test_cli_partition_mode_exclusive(tmp_path):
    import qsearch
    with pytest.raises(SystemExit):
        qsearch.build_parser().parse_args([
            "phase-copy-baseline", "--partition-source", "--pauli-symmetry"])
