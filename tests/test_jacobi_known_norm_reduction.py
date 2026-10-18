"""Known norm is public information, not a generic principal-ideal oracle."""

import hashlib
import itertools
import json
from pathlib import Path

from flint import fmpz_mat
import pytest
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form

import theorems.jacobi_surface_reconstruction as surface
from theorems.jacobi_known_norm_reduction import (
    ARTIFACT, THEOREM, cm_input_certificate, group_ring_input_certificate,
    group_ring_witness, identity, order_description, public_reduction,
    run_controls,
)


def independent_product(a, b, ell):
    # Cyclic convolution followed by Phi_ell reduction, independent of FLINT.
    padded_a, padded_b = tuple(a) + (0,), tuple(b) + (0,)
    cyclic = [sum(padded_a[i] * padded_b[(k - i) % ell] for i in range(ell)) for k in range(ell)]
    return [cyclic[j] - cyclic[-1] for j in range(ell - 1)]


def independent_conjugate(a, ell):
    padded = tuple(a) + (0,)
    rev = [padded[-i % ell] for i in range(ell)]
    return [rev[j] - rev[-1] for j in range(ell - 1)]


@pytest.mark.parametrize("p,ell,abc", [(7, 3, (1, 1, 2)), (11, 5, (1, 1, 1)), (29, 7, (1, 2, 3))])
def test_exact_public_input_replayed_without_its_product_or_matrix_helpers(p, ell, abc):
    source = surface.ReferenceCharacters(p, ell)
    record = public_reduction(source, abc)
    assert source._indices is None and source.reference_summands == 0
    cm, group = record["CM_theorem_input"], record["group_ring_theorem_input"]
    B = Matrix(cm["ideal_basis_rows"])
    assert abs(B.det()) == p ** (ell - 1)
    values = B.tolist()
    products = [independent_product(a, independent_conjugate(b, ell), ell) for a in values for b in values]
    # SymPy uses column HNF, whereas the producer uses row HNF.
    assert hermite_normal_form(Matrix(products).T) == Matrix.eye(ell - 1) * p * p
    T = Matrix([[ell * int(i == j) - 1 for j in range(ell - 1)] for i in range(ell - 1)])
    G = B * T * B.T / (p * p)
    assert G == Matrix(cm["normalized_gram"])
    assert G.det() == ell ** (ell - 2)
    C = Matrix(cm["ring_generator_action_rows"])
    assert C ** ell == Matrix.eye(ell - 1)
    assert C * G * C.T == G
    for row in values:
        for t, e in surface.valuation_profile(abc, ell):
            if e:
                root = source.teichmuller_root(t, e)
                assert sum(c * pow(root, j, p ** e) for j, c in enumerate(row)) % (p ** e) == 0
    R = Matrix(group["ideal_basis_rows"])
    assert abs(R.det()) == p ** ell
    assert R * R.T / (p * p) == Matrix(group["normalized_gram"])
    assert Matrix(group["normalized_gram"]).det() == 1
    for row in R.tolist():
        assert sum(row) % p == 0
        projection = [row[j] - row[-1] for j in range(ell - 1)]
        assert all(x.q == 1 for x in (Matrix([projection]) * B.inv()))
    S = Matrix(group["ring_generator_action_rows"])
    assert (-S) ** ell == -Matrix.eye(ell)
    assert not record["classical_known_norm_recovery_executed"]


def test_order_table_and_involution_are_explicit_theorem_inputs():
    field = surface.Cyclotomic(5)
    order = order_description(field)
    assert order["rank"] == 4
    for i, j in itertools.product(range(4), repeat=2):
        a, b = [int(k == i) for k in range(4)], [int(k == j) for k in range(4)]
        assert order["multiplication_table"][i][j] == independent_product(a, b, 5)
    for j in range(4):
        assert order["conjugation_basis_images"][j] == independent_conjugate([int(k == j) for k in range(4)], 5)
    assert THEOREM["arxiv"] == "1706.07373v3" and not THEOREM["implemented_here"]


def test_all_small_jacobi_witnesses_satisfy_both_ideal_inputs_and_root_selection():
    source = surface.ReferenceCharacters(11, 5)
    for abc in itertools.combinations_with_replacement(range(1, 5), 3):
        if sum(abc) % 5 == 0:
            continue
        record = public_reduction(source, abc)
        value = source.triple(abc)
        B = Matrix(record["CM_theorem_input"]["ideal_basis_rows"])
        assert all(x.q == 1 for x in (Matrix([value]) * B.inv()))
        lifted = group_ring_witness(source, value)
        v = lifted["coefficients"]
        assert sum(v) == 11
        for lag in range(5):
            assert sum(v[j] * v[(j - lag) % 5] for j in range(5)) == (121 if lag == 0 else 0)
        R = Matrix(record["group_ring_theorem_input"]["ideal_basis_rows"])
        assert all(x.q == 1 for x in (Matrix([v]) * R.inv()))
        # The ell cyclic shifts are exactly the remaining root choices at augmentation +p.
        for turn in range(5):
            rotated = v[turn:] + v[:turn]
            projection = tuple(rotated[j] - rotated[-1] for j in range(4))
            assert surface.primary_normalize(source.field, projection, source.p) == value


@pytest.mark.parametrize("norm", [0, -121, 11, 122, 121.0, True])
def test_wrong_or_nonpositive_norm_cannot_be_silently_replaced_by_a_pip_assumption(norm):
    source = surface.ReferenceCharacters(11, 5)
    B, _ = surface.public_ideal_basis(source, (1, 1, 1))
    with pytest.raises(ValueError, match="relative norm|polarization"):
        cm_input_certificate(source.field, B, norm)


def test_matched_index_is_insufficient_without_the_module_action():
    field = surface.Cyclotomic(5)
    # Index 11^4 is right, but this coefficient lattice is not an ideal.
    bad = fmpz_mat([[121, 0, 0, 0], [0, 121, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    with pytest.raises(ValueError, match="closed"):
        cm_input_certificate(field, bad, 121)


def test_incorrect_rank_or_composite_conductor_is_rejected():
    with pytest.raises(ValueError, match="dimension"):
        cm_input_certificate(surface.Cyclotomic(5), identity(3), 121)
    with pytest.raises(ValueError, match="full-rank"):
        cm_input_certificate(surface.Cyclotomic(5), fmpz_mat([[0] * 4 for _ in range(4)]), 121)
    source = surface.ReferenceCharacters(13, 4)
    with pytest.raises(ValueError, match="prime"):
        public_reduction(source, (1, 1, 1))
    with pytest.raises(ValueError, match="prime"):
        group_ring_input_certificate(source, (1, 1, 1))


def test_product_polarization_is_not_itself_an_existence_proof_or_an_ideal_selector():
    source = surface.ReferenceCharacters(11, 5)
    positive = public_reduction(source, (1, 1, 1))
    inverse = public_reduction(source, (4, 4, 4))
    assert not positive["CM_theorem_input"]["input_conditions_alone_prove_a_normalized_generator_exists"]
    assert "Jacobi" in positive["YES_premise"]
    # Both conjugate ideals are valid theorem inputs. Only the positive convention
    # specifies the intended J. Input validity cannot certify arbitrary character labels.
    B = Matrix(inverse["CM_theorem_input"]["ideal_basis_rows"])
    assert any(x.q != 1 for x in Matrix([source.triple((1, 1, 1))]) * B.inv())
    assert positive["CM_theorem_input"]["ideal_basis_rows"] != inverse["CM_theorem_input"]["ideal_basis_rows"]


def test_same_ideal_nonroot_unit_cannot_be_used_as_a_norm_witness():
    source = surface.ReferenceCharacters(11, 5)
    field = source.field
    bad = field.multiply(source.triple((1, 1, 1)), field.add(field.constant(1), field.root(1)))
    with pytest.raises(ValueError, match="norm-normalized"):
        group_ring_witness(source, bad)


def test_large_inputs_require_no_truth_lll_phase_or_full_table(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("not a public theorem-input construction")
    monkeypatch.setattr(surface.ReferenceCharacters, "pair", forbidden)
    monkeypatch.setattr(surface.ReferenceCharacters, "triple", forbidden)
    monkeypatch.setattr(surface.ReferenceCharacters, "indices", property(forbidden))
    monkeypatch.setattr(surface, "classical_lll_attempt", forbidden)
    source = surface.ReferenceCharacters(2 ** 61 - 1, 11, residue_root=54008984094220448)
    report = public_reduction(source, (1, 1, 1))
    assert report["CM_theorem_input"]["ideal_index"] == str(source.p ** 10)
    assert report["group_ring_theorem_input"]["ideal_index"] == str(source.p ** 11)
    assert report["CM_theorem_input"]["basis_max_coefficient_bits"] <= 2 * source.p.bit_length()
    assert report["group_ring_theorem_input"]["basis_max_coefficient_bits"] <= 2 * source.p.bit_length()
    assert source._indices is None and source.reference_summands == 0


def test_live_artifact_is_replayed_with_explicit_nonimplementation_and_scope():
    report = json.loads(ARTIFACT.read_text())
    assert run_controls() == report
    source_file = Path(__file__).resolve().parents[1] / "theorems/jacobi_known_norm_reduction.py"
    assert report["source_sha256"] == hashlib.sha256(source_file.read_bytes()).hexdigest()
    dependency = source_file.with_name("jacobi_surface_reconstruction.py")
    assert report["surface_dependency_sha256"] == hashlib.sha256(dependency.read_bytes()).hexdigest()
    assert len(report["small_controls"]) == 6
    assert len(report["large_public_controls"]) == report["large_distinct_ideal_profiles"] == 51
    assert not report["external_theorem"]["implemented_here"]
    assert not report["accepted_speedup_candidate"] and not report["new_central_negative_registered"]
    assert not report["independent_or_formal_review_completed"]
