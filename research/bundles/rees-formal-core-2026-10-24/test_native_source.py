from fractions import Fraction
import json

import numpy as np
import pytest

import native_source_controls as c
import verify as base
import verify_group_bridge as bridge
import verify_native_source as native


def diagnostics(names, axiom="propext"):
    return "\n".join(json.dumps({"severity": "information",
                                "data": f"'{name}' depends on axioms: [{axiom}]"}) for name in names)


def test_manifest_matches_all_explicit_native_declarations():
    assert len(native.THEOREMS) == 13
    assert len(native.DECLARATIONS) == len(set(native.DECLARATIONS)) == 19
    assert (native.ROOT/"AuditNativeSource.lean").read_text() == native.expected_audit()
    assert set(base.parse_axioms(diagnostics(native.DECLARATIONS), native.DECLARATIONS)) == set(native.DECLARATIONS)


@pytest.mark.parametrize("missing", ["source_correlation", "pullback_with_reference", "topGroupEquiv",
                                     "top_hidden_image", "acquireTop_source", "native_average_tree", "native_record_tree"])
def test_unchecked_native_obligation_rejected(missing):
    names = [name for name in native.DECLARATIONS if name != native.PREFIX+missing]
    with pytest.raises(ValueError, match="incomplete"):
        base.parse_axioms(diagnostics(names), native.DECLARATIONS)


@pytest.mark.parametrize("axiom", ["sorryAx", "AssumeNativeSource", "AssumeHiddenInverse"])
def test_source_access_cannot_be_added_by_axiom(axiom):
    with pytest.raises(ValueError, match="unapproved axiom"):
        base.parse_axioms(diagnostics(native.DECLARATIONS, axiom), native.DECLARATIONS)


def test_prior_recursive_proof_cannot_be_changed_unnoticed():
    with pytest.raises(ValueError, match="frozen receipt"):
        bridge.validate_base_record({"combined_theorem_count": 166}, {"combined_theorem_count": 167})


def test_scope_does_not_claim_compilation_or_advantage():
    report = native.scope_report()
    assert report["native_to_top_source_channel_formalized"]
    assert report["native_source_to_recursive_record_identity_checked"]
    assert report["native_independent_mixed_coset_sources_required"]
    assert report["public_uniform_address_and_reversible_translation_required"]
    for key in ("source_inverse_required", "hiding_function_oracle_required_by_copy_only_channel",
                "kernel_index_postselection_required", "uniform_coherent_compiler_implemented",
                "correlated_target_bank_supported", "final_fourier_recovery_formalized",
                "formalizes_full_Rees_algorithm", "quantum_execution", "new_algorithm_or_novelty_claim"):
        assert not report[key]


def test_actual_rees_evaluation_maps_are_homomorphisms_and_jointly_injective():
    for a in (1, 2):
        assert all(c.evaluate(c.cover_mul(x, y), a) == c.mul(c.evaluate(x, a), c.evaluate(y, a))
                   for x in c.COVER for y in c.COVER)
    assert len({tuple(c.evaluate(x, a) for a in (1, 2)) for x in c.COVER}) == len(c.COVER)


@pytest.mark.parametrize("family", ["trivial", "nonhomogeneous_line", "full"])
def test_two_native_copies_produce_actual_cover_source(family):
    source = c.native_source(family)
    actual = c.literal_pullback((source, source))
    expected = c.expected_source(family)
    assert np.max(np.abs(actual-expected)) < 1e-14
    assert abs(np.trace(actual)-1) < 1e-14
    assert np.linalg.eigvalsh(actual)[0] > -1e-14


def test_noninjective_map_needs_no_kernel_postselection():
    assert len({c.evaluate(x, 1) for x in c.COVER}) == len(c.GROUP) < len(c.COVER)
    source = c.native_source("nonhomogeneous_line")
    actual = c.literal_pullback((source,), points=(1,))
    assert np.max(np.abs(actual-c.expected_source("nonhomogeneous_line", points=(1,)))) < 1e-14
    assert abs(np.trace(actual)-1) < 1e-14


def test_wrong_translation_side_and_dirty_work_are_falsified():
    report = c.audit()
    assert report["wrong_left_translation_trace_distance"] > .1
    assert report["retained_evaluation_work_trace_distance"] > .1
    assert report["naive_projection_success_one_factor"] == "1/9"
    assert report["naive_projection_success_ten_factors"] == "1/3486784401"
    assert not report["quantum_execution"] and not report["new_algorithm_or_speedup_claim"]


@pytest.mark.parametrize("prime,factors", [(3, 1), (3, 10), (5, 20), (2**127-1, 3)])
def test_naive_projection_cost_scales_exponentially_without_enumeration(prime, factors):
    assert c.postselection_probability(prime, factors) == Fraction(1, prime**(2*factors))


@pytest.mark.parametrize("prime,factors", [(2, 1), (4, 1), (3, 0)])
def test_resource_domain_errors_rejected(prime, factors):
    with pytest.raises(ValueError):
        c.postselection_probability(prime, factors)


def test_missing_independent_target_rejected():
    with pytest.raises(ValueError, match="per evaluation"):
        c.literal_pullback((np.eye(27)/27,))
