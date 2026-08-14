import math

import numpy as np

from self_dual_wreath_compressed_racah_block_probe import (
    build_compressed_racah_probe_report,
    compile_compressed_racah_block,
    racah_block_from_pair_embeddings,
)
from symmetric_yjm_pair_fiber import pair_intertwiner_embeddings


def test_pairwise_yjm_fiber_compiles_unequal_irreps() -> None:
    embeddings, metrics = pair_intertwiner_embeddings(
        (3, 2),
        (3, 1, 1),
        (3, 1, 1),
    )
    assert embeddings.shape == (2, 5, 6, 6)
    assert metrics.multiplicity == 2
    assert metrics.eigensolve_vector_dimension == 30
    assert metrics.direct_invariant_vector_dimension == 180
    assert metrics.maximum_penalty_residual < 1e-7
    assert metrics.embedding_isometry_residual < 1e-7
    assert metrics.status == "pairwise-yjm-fiber-compiled"


def test_compressed_racah_blocks_match_independent_six_character_law() -> None:
    source = (3, 1, 1)
    left = (3, 2)
    right = (2, 2, 1)
    diagonal = compile_compressed_racah_block(
        "diagonal",
        (source, source, source, source),
        left,
        left,
    )
    off_diagonal = compile_compressed_racah_block(
        "off-diagonal",
        (source, source, source, source),
        left,
        right,
    )
    for record in (diagonal, off_diagonal):
        assert record.finite_likelihood_block_mass_residual is not None
        assert record.finite_likelihood_block_mass_residual < 1e-10
        assert 0 <= record.block_operator_norm_square <= 1 + 1e-10
        assert record.status == "compressed-racah-block-mass-verified"


def test_racah_block_mass_is_multiplicity_gauge_invariant() -> None:
    source = (3, 1, 1)
    intermediate = (3, 2)
    ab_mu, _ = pair_intertwiner_embeddings(source, source, intermediate)
    mu_c_l, _ = pair_intertwiner_embeddings(intermediate, source, source)
    a_nu_l, _ = pair_intertwiner_embeddings(source, intermediate, source)
    rng = np.random.default_rng(19)

    def orthogonal(size: int) -> np.ndarray:
        q, _ = np.linalg.qr(rng.normal(size=(size, size)))
        return q

    original = racah_block_from_pair_embeddings(
        ab_mu,
        mu_c_l,
        ab_mu,
        a_nu_l,
    )
    rotated = racah_block_from_pair_embeddings(
        np.einsum("ij,jabm->iabm", orthogonal(2), ab_mu),
        np.einsum("ij,jmcl->imcl", orthogonal(2), mu_c_l),
        np.einsum("ij,jbcn->ibcn", orthogonal(2), ab_mu),
        np.einsum("ij,janl->ianl", orthogonal(2), a_nu_l),
    )
    assert math.isclose(
        float(np.linalg.norm(original) ** 2),
        float(np.linalg.norm(rotated) ** 2),
        rel_tol=1e-11,
        abs_tol=1e-11,
    )
    assert np.allclose(
        np.linalg.svd(original, compute_uv=False),
        np.linalg.svd(rotated, compute_uv=False),
        rtol=1e-11,
        atol=1e-11,
    )


def test_report_keeps_claim_gate_closed() -> None:
    report = build_compressed_racah_probe_report(scaling_n_values=(6,))
    assert report.headline_metrics["control_failure_count"] == 0
    assert report.headline_metrics["independent_s5_exact_block_control_count"] == 4
    assert report.headline_metrics["maximum_probe_n"] == 6
    assert report.claim_gate["pairwise_yjm_fiber_compiler_verified"] is True
    assert report.claim_gate["full_physical_average_racah_mi_computed"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
