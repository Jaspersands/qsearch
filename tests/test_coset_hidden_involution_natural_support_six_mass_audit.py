from pathlib import Path

import proof_tracker

from coset_hidden_involution_natural_support_six_mass_audit import (
    repeated_branch_census,
    run_natural_support_six_mass_audit,
    write_natural_support_six_mass_audit,
)


def _audited_multiplicity_report() -> dict:
    specs = [
        ((10, 4), (5, 2), ()),
        ((10, 2, 2), (5, 2), ()),
        ((10, 3, 1), (5, 1, 1), ()),
        ((10, 3, 1), (4, 2, 1), ()),
        ((9, 4, 1), (4, 2, 1), ()),
        ((10, 2, 2), (5,), (2,)),
        ((10, 2, 2), (4, 1), (2,)),
        ((10, 3, 1), (4, 1), (1, 1)),
    ]
    return {
        "controls": [
            {
                "half_degree": 7,
                "symmetric_partition": list(symmetric),
                "hyperoctahedral_partition": list(alpha),
                "negative_hyperoctahedral_partition": list(beta),
                "compressed_twirl_projection_verified": True,
                "minimum_full_copy_algebra_support": 6,
            }
            for symmetric, alpha, beta in specs
        ]
    }


def test_exact_s14_census_normalizes_and_repeated_mass_dominates() -> None:
    denominator, occupied, numerator, repeated = repeated_branch_census(7)
    assert numerator == denominator
    assert denominator == 87178291200
    assert occupied == 3881
    assert len(repeated) == 2414
    repeated_mass = sum(row.natural_mass_numerator for row in repeated) / denominator
    assert abs(repeated_mass - 0.9784377306078695) <= 1e-15


def test_audited_support_six_blocks_have_negligible_natural_mass() -> None:
    report = run_natural_support_six_mass_audit(
        multiplicity_report=_audited_multiplicity_report(),
        high_mass_report={},
        portfolio_report={},
    )
    assert report.audited_rank_branch_count == 8
    assert abs(report.audited_rank_natural_mass_probability - 3.0693008123563677e-5) <= 1e-18
    assert report.audited_fraction_of_repeated_natural_mass < 3.2e-5
    assert report.theorem.audited_support_six_blocks_have_nonnegligible_mass is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_low_ambient_window_is_source_biased_and_targets_high_mass_blocks() -> None:
    report = run_natural_support_six_mass_audit(
        multiplicity_report=_audited_multiplicity_report(),
        high_mass_report={},
        portfolio_report={},
    )
    first = report.feasibility_windows[0]
    assert first.maximum_symmetric_irrep_dimension == 5000
    assert first.repeated_branch_count == 62
    assert first.natural_mass_probability < 0.001
    target = report.highest_mass_untested_branches[0]
    assert target.symmetric_partition == (5, 3, 2, 2, 1, 1)
    assert target.branching_multiplicity == 26
    assert target.natural_mass_probability > 0.008
    assert target.current_compressor_status == "requires-symbolic-or-matrix-free-transfer"


def test_writer_emits_mass_audit_without_registry(tmp_path: Path) -> None:
    output = tmp_path / "natural-support-mass.json"
    payload = write_natural_support_six_mass_audit(
        output,
        write_registry=False,
        multiplicity_report=_audited_multiplicity_report(),
        high_mass_report={},
        portfolio_report={},
    )
    assert output.exists()
    assert payload["status"] == "finite-support-six-controls-have-negligible-natural-mass"
    assert payload["headline_metrics"]["uniform_support_six_generation_theorem_count"] == 0


def test_proof_tracker_records_selection_bias_and_keeps_typical_gap_open(
    tmp_path: Path,
    monkeypatch,
) -> None:
    output = tmp_path / "natural-support-mass.json"
    write_natural_support_six_mass_audit(
        output,
        write_registry=False,
        high_mass_report={},
        portfolio_report={},
        multiplicity_report=_audited_multiplicity_report(),
    )
    monkeypatch.setattr(
        proof_tracker,
        "NATURAL_SUPPORT_SIX_MASS_AUDIT_PATH",
        output,
    )
    lemmas = {
        lemma.id: lemma
        for lemma in proof_tracker._natural_support_six_mass_lemmas(
            "CODE-COSET-COLLECTIVE"
        )
    }
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-NATURAL-SUPPORT-SIX-MASS-CENSUS"
    ].status.startswith("proved-")
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-TYPICAL-SUPPORT-SIX-GAPPED-COMMUTANT"
    ].status == "blocked-high-mass-block-generation-gap-and-coherent-access-open"


def test_source_ranked_high_mass_scan_is_included_but_remains_subpercent() -> None:
    high_mass_report = {
        "half_degree": 7,
        "symmetric_partition": [5, 3, 2, 2, 1, 1],
        "hyperoctahedral_partition": [2, 1],
        "negative_hyperoctahedral_partition": [2, 1, 1],
        "claim_gate": {
            "support_four_full_copy_algebra_numerically_certified": True,
        },
    }
    report = run_natural_support_six_mass_audit(
        multiplicity_report=_audited_multiplicity_report(),
        high_mass_report=high_mass_report,
        portfolio_report={},
    )
    assert report.audited_rank_branch_count == 9
    assert report.source_ranked_audited_branch_count == 1
    assert abs(report.source_ranked_natural_mass_gain - 0.008705357142857143) <= 1e-16
    assert 0.0087 < report.audited_rank_natural_mass_probability < 0.01
    assert report.theorem.audited_support_six_blocks_have_nonnegligible_mass is False
    assert report.status == (
        "source-ranked-support-four-control-raises-coverage-but-remains-subpercent"
    )


def test_source_weighted_portfolio_raises_coverage_without_typical_claim() -> None:
    high_mass_report = {
        "half_degree": 7,
        "symmetric_partition": [5, 3, 2, 2, 1, 1],
        "hyperoctahedral_partition": [2, 1],
        "negative_hyperoctahedral_partition": [2, 1, 1],
        "claim_gate": {
            "support_four_full_copy_algebra_numerically_certified": True,
        },
    }
    portfolio_report = {
        "half_degree": 7,
        "scanned_branches": [
            {
                "symmetric_partition": [5, 3, 2, 2, 1, 1],
                "hyperoctahedral_partition": [2, 1],
                "negative_hyperoctahedral_partition": [3, 1],
                "certified_support_upper_bound": 4,
                "separator_certificate": {
                    "scalar_common_commutant_numerically_certified": True,
                    "direct_commutant_nullity_at_1e8": 1,
                },
            }
        ],
    }
    report = run_natural_support_six_mass_audit(
        multiplicity_report=_audited_multiplicity_report(),
        high_mass_report=high_mass_report,
        portfolio_report=portfolio_report,
    )
    assert report.source_ranked_audited_branch_count == 2
    assert report.audited_rank_natural_mass_probability > 0.017
    assert report.theorem.audited_support_six_blocks_have_nonnegligible_mass is True
    assert report.theorem.uniform_support_six_generation_proved is False
    assert report.status == (
        "source-ranked-controls-cover-visible-but-not-typical-natural-mass"
    )


def test_unknown_branch_and_empty_priority_do_not_inflate_coverage():
    source = _audited_multiplicity_report()
    source["controls"][0]["symmetric_partition"] = [100]
    report = run_natural_support_six_mass_audit(
        multiplicity_report=source, high_mass_report={}, portfolio_report={}, priority_target_count=0,
    )
    assert report.audited_rank_branch_count == 7
    assert report.highest_mass_untested_branches == []
    assert report.headline_metrics["highest_mass_untested_branch_probability"] == 0


def test_visible_coverage_does_not_invalidate_exact_source_census(tmp_path, monkeypatch):
    import json
    path = tmp_path / "mass.json"
    path.write_text(json.dumps({"claim_gate": {
        "exact_joint_source_law_normalized": True,
        "audited_support_six_blocks_have_nonnegligible_mass": True,
    }}))
    monkeypatch.setattr(proof_tracker, "NATURAL_SUPPORT_SIX_MASS_AUDIT_PATH", path)
    lemma = proof_tracker._natural_support_six_mass_lemmas("CODE-COSET-COLLECTIVE")[0]
    assert lemma.status == "proved-exact-finite-source-law-normalization"
