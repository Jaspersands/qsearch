"""Unit tests for theorems/lattice_product_phase_source.py."""
from __future__ import annotations

import pytest

from theorems.lattice_sine_window_source import SineWindowSource
from theorems.lattice_product_phase_source import (
    GROUP,
    audit_product_batch,
    compile_product_source,
    decode_parent_shift,
    exact_product_reference,
    group_resource_comparison,
    public_source,
    simulate_product_batch,
)


def test_public_source_and_resource_record():
    source = SineWindowSource(((1,),), 7, 1, 0, 2, 4)
    pub = public_source(source)
    assert pub["phase_group"] == GROUP
    assert pub["rank"] == 1
    assert pub["coordinate_modulus"] == 4
    assert pub["scalar_cyclic_DCP_contract_granted"] is False

    compiled = compile_product_source(source)
    rec = compiled.resource_record()
    assert rec["coordinate_QFT_count_per_parent"] == 1
    assert rec["source_position_wires_reused_in_place"] is True
    assert rec["mixed_colour_inverse_or_correct_trial_flag_available"] is False


def test_exact_product_reference_and_batch_audit():
    source = SineWindowSource(((1,),), 7, 1, 0, 2, 4)
    compiled = compile_product_source(source)
    ref = exact_product_reference(source)
    assert ref["QFT_group"] == GROUP
    assert len(ref["all_label_outcomes"]) == 4

    batch = simulate_product_batch(compiled, 2, 191510, "test-product-source")
    audit = audit_product_batch(source, ref, batch)
    assert audit["all_emitted_product_densities_agree"] is True
    assert audit["speedup_or_hardware_certificate"] is False


def test_decode_parent_shift_and_group_resource_comparison():
    source = SineWindowSource(((17, 0), (16, 1)), 7, 1, 0, 2, 4)
    decoded = decode_parent_shift(source, (1, 3))
    assert decoded["balanced_parent_shift"] == (1, -1)
    assert decoded["correct_vector_or_shortest_vector_certified"] is False

    with pytest.raises(ValueError):
        decode_parent_shift(source, (1, 4))

    comp = group_resource_comparison(8, 32)
    assert comp["original_rank"] == 8
    assert comp["product_has_smaller_group_entropy_than_unlifted_cyclic_source"] is False
    assert comp["group_isomorphism_or_equal_decoder_difficulty_claimed"] is False
