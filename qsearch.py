"""Q-Search research-lab CLI.

Commands:
  python qsearch.py audit
  python qsearch.py literature
  python qsearch.py hypothesize
  python qsearch.py hidden-shift
  python qsearch.py dcp-samples
  python qsearch.py dcp-decode
  python qsearch.py dcp-recurrence
  python qsearch.py dcp-schedules
  python qsearch.py dcp-uniform-schedules
  python qsearch.py dcp-bad-registers
  python qsearch.py dcp-contamination
  python qsearch.py dcp-witness-search
  python qsearch.py dcp-clifford-witnesses
  python qsearch.py dcp-clifford-contamination
  python qsearch.py dcp-hadamard-scaling
  python qsearch.py dcp-random-decoder
  python qsearch.py dcp-decoder-frontier
  python qsearch.py dcp-multiscale-aliasing
  python qsearch.py dcp-fourier-bridge
  python qsearch.py dcp-sparse-fourier-audit
  python qsearch.py dcp-iid-hash-audit
  python qsearch.py dcp-biased-linear-audit
  python qsearch.py dcp-multirecord-audit
  python qsearch.py dcp-ustatistic-audit
  python qsearch.py dcp-factorized-contraction
  python qsearch.py dcp-low-rank-contraction
  python qsearch.py dcp-subset-sum-measurement
  python qsearch.py dcp-hashed-fiber-measurement
  python qsearch.py dcp-reference-projection
  python qsearch.py dcp-covariant-pgm
  python qsearch.py dcp-pgm-gram
  python qsearch.py dcp-pgm-qsvt
  python qsearch.py dcp-quenched-occupancy
  python qsearch.py dcp-fiber-erasure-boundary
  python qsearch.py dcp-erasure-inversion
  python qsearch.py dcp-erasure-coherence
  python qsearch.py dcp-erasure-perturbation
  python qsearch.py coset-natural-multicopy-pgm
  python qsearch.py coset-pgm-gain-localization
  python qsearch.py coset-pgm-average-frame
  python qsearch.py coset-character-ratios
  python qsearch.py coset-projector-subpovm
  python qsearch.py code-wreath-projector-subpovm
  python qsearch.py code-wreath-subpovm-moments
  python qsearch.py code-wreath-natural-unequal
  python qsearch.py code-wreath-moment-word-map
  python qsearch.py code-wreath-word-map-mixing
  python qsearch.py dcp-contaminated-pgm
  python qsearch.py dcp-subset-sum-bridge
  python qsearch.py dcp-subset-sum-lattice
  python qsearch.py dcp-subset-sum-two-adic
  python qsearch.py dcp-subset-sum-resource-frontier
  python qsearch.py dcp-subset-sum-carry-anf
  python qsearch.py dcp-subset-sum-synthesize
  python qsearch.py dcp-subset-sum-low-bit-bdd
  python qsearch.py dcp-subset-sum-conditioned-quotient
  python qsearch.py dcp-subset-sum-carry-slice-lattice
  python qsearch.py dcp-carry-high-part
  python qsearch.py dcp-boolean-coset-separation
  python qsearch.py dcp-marker-list-decoder
  python qsearch.py dcp-marker-deviations
  python qsearch.py dcp-marker-all-targets
  python qsearch.py dcp-marker-vulnerable-coordinates
  python qsearch.py dcp-marker-chart-union
  python qsearch.py dcp-marker-target-beam
  python qsearch.py dcp-subset-sum-target-distribution
  python qsearch.py dcp-coherent-matching
  python qsearch.py dcp-quantum-relation-fidelity
  python qsearch.py dcp-quantum-walk-source-audit
  python qsearch.py dcp-symmetric-relation-lift
  python qsearch.py dcp-fiber-transport
  python qsearch.py dcp-fiber-graph
  python qsearch.py dcp-signed-permutation-transport
  python qsearch.py dcp-affine-transport
  python qsearch.py dcp-fiber-balance
  python qsearch.py dcp-partial-relations
  python qsearch.py dcp-target-locality
  python qsearch.py dcp-fiber-entanglement
  python qsearch.py dcp-adaptive-layouts
  python qsearch.py dcp-subset-sum-randomize
  python qsearch.py dcp-odd-unit-geometry
  python qsearch.py dcp-likelihood-search
  python qsearch.py coset-state
  python qsearch.py collective-observables
  python qsearch.py code-family-search
  python qsearch.py tensor-observables
  python qsearch.py gm-switching
  python qsearch.py cfi-scaling
  python qsearch.py cfi-base-search
  python qsearch.py cfi-parity-solver
  python qsearch.py cfi-structural-decoder
  python qsearch.py cfi-irregular-decoder
  python qsearch.py cfi-bipartite-decoder
  python qsearch.py cfi-code-reduction
  python qsearch.py code-hull-projector
  python qsearch.py individualized-wl
  python qsearch.py individualized-tensors
  python qsearch.py coset-triage
  python qsearch.py representation-obstructions
  python qsearch.py weak-fourier
  python qsearch.py coset-distinguishability
  python qsearch.py coset-pgm
  python qsearch.py coset-holevo
  python qsearch.py coset-covariant-frame
  python qsearch.py coset-two-copy-frame
  python qsearch.py coset-two-copy-transitions
  python qsearch.py coset-three-copy-recoupling
  python qsearch.py coset-commutant-gap-scaling
  python qsearch.py coset-commutant-gap-proof
  python qsearch.py coset-racah-control
  python qsearch.py coset-racah-complete-control
  python qsearch.py coset-racah-hierarchical-control
  python qsearch.py coset-racah-gap-scaling
  python qsearch.py coset-racah-sparse-gap
  python qsearch.py coset-racah-trace-conjecture
  python qsearch.py coset-racah-trace-proof
  python qsearch.py coset-racah-second-moment-proof
  python qsearch.py coset-racah-third-moment-proof
  python qsearch.py coset-racah-fourth-moment-proof
  python qsearch.py coset-racah-root-separation-proof
  python qsearch.py coset-racah-coherent-label-proof
  python qsearch.py coset-racah-stable-transition
  python qsearch.py coset-racah-complementary-sectors
  python qsearch.py coset-racah-stable-shape-proof
  python qsearch.py coset-racah-stable-shape-labels
  python qsearch.py coset-racah-stable-shape-traces
  python qsearch.py coset-racah-stable-shape-second-moments
  python qsearch.py coset-racah-stable-shape-cubic-determinant
  python qsearch.py coset-racah-stable-shape-quadratic-gaps
  python qsearch.py coset-racah-stable-shape-cubic-gap
  python qsearch.py coset-racah-stable-shape-coherent-labels
  python qsearch.py coset-racah-stable-first-stage-labels
  python qsearch.py coset-racah-stable-shape-router
  python qsearch.py coset-racah-stable-encoded-tree
  python qsearch.py coset-racah-stable-three-copy-frame
  python qsearch.py coset-recoupling-capabilities
  python qsearch.py coset-recoupling-synthesize
  python qsearch.py code-equivalence
  python qsearch.py code-invariants
  python qsearch.py code-info-sets
  python qsearch.py code-canonicalize
  python qsearch.py code-profile-search
  python qsearch.py code-tuple-profiles
  python qsearch.py code-low-weight
  python qsearch.py code-qc-search
  python qsearch.py code-qc-canonicalize
  python qsearch.py code-qc-info-resolve
  python qsearch.py code-cyclic-search
  python qsearch.py code-bch-search
  python qsearch.py code-goppa-search
  python qsearch.py code-goppa-scaling
  python qsearch.py code-goppa-syzygies
  python qsearch.py code-goppa-projectors
  python qsearch.py code-tanner-search
  python qsearch.py code-rm-search
  python qsearch.py code-rank-metric-search
  python qsearch.py code-incidence-resolve
  python qsearch.py code-self-dual-search
  python qsearch.py code-self-dual-local-obstruction
  python qsearch.py code-self-dual-global-orbit
  python qsearch.py code-self-dual-hsp
  python qsearch.py code-self-dual-rowspace-hsp
  python qsearch.py code-self-dual-automorphisms
  python qsearch.py code-self-dual-high-order
  python qsearch.py code-self-dual-sparsity
  python qsearch.py code-self-dual-wreath
  python qsearch.py code-self-dual-wreath-hecke
  python qsearch.py code-self-dual-wreath-pgm
  python qsearch.py code-self-dual-wreath-carrier
  python qsearch.py code-self-dual-wreath-orbits
  python qsearch.py code-self-dual-wreath-harmonics
  python qsearch.py code-self-dual-wreath-commutant
  python qsearch.py code-self-dual-wreath-frame-blocks
  python qsearch.py code-self-dual-wreath-unequal-blocks
  python qsearch.py code-self-dual-wreath-w3-tuples
  python qsearch.py code-self-dual-wreath-moments
  python qsearch.py code-self-dual-wreath-third-moment
  python qsearch.py code-self-dual-wreath-all-unequal
  python qsearch.py code-self-dual-wreath-commutators
  python qsearch.py code-self-dual-wreath-stable-rank
  python qsearch.py code-self-dual-wreath-typical-portfolio
  python qsearch.py code-self-dual-wreath-recoupling-transfer
  python qsearch.py code-ag-search
  python qsearch.py code-pg-search
  python qsearch.py code-schur-filtration
  python qsearch.py code-closure-attack
  python qsearch.py code-triage
  python qsearch.py dequantize
  python qsearch.py baselines
  python qsearch.py query-lower-bounds
  python qsearch.py learnability
  python qsearch.py fourier-learnability
  python qsearch.py character-shift
  python qsearch.py character-decoders
  python qsearch.py character-query-info
  python qsearch.py character-complexity
  python qsearch.py phase-naturalness
  python qsearch.py trace-functions
  python qsearch.py family-triage
  python qsearch.py run EXPERIMENT_ID
  python qsearch.py run-next
  python qsearch.py trends
  python qsearch.py proofs
  python qsearch.py reductions
  python qsearch.py reduction-contracts
  python qsearch.py proof-queue
  python qsearch.py sweep
  python qsearch.py conjectures
  python qsearch.py mutate
  python qsearch.py quarantine-invalid
  python qsearch.py blockers
  python qsearch.py frontiers
  python qsearch.py query-models
  python qsearch.py dcp-subset-sum-preconditioned-geometry
  python qsearch.py dcp-subset-sum-fourth-moment
  python qsearch.py dcp-subset-sum-smith-moments
  python qsearch.py dcp-subset-sum-smith-transfer
  python qsearch.py dcp-subset-sum-fixed-moments
  python qsearch.py dcp-subset-sum-conditioned-tail
  python qsearch.py dcp-subset-sum-growing-moments
  python qsearch.py dcp-subset-sum-growing-chain
  python qsearch.py dcp-subset-sum-signed-l2
  python qsearch.py dcp-subset-sum-sparse-characters
  python qsearch.py dcp-subset-sum-qtt
  python qsearch.py dcp-subset-sum-embedding-volume
  python qsearch.py dcp-subset-sum-short-relations
  python qsearch.py dcp-subset-sum-carry-relations
  python qsearch.py dcp-subset-sum-marker-coset
  python qsearch.py dcp-subset-sum-affine-cvp
  python qsearch.py dcp-subset-sum-affine-scaling
  python qsearch.py dcp-subset-sum-affine-bdd
  python qsearch.py ingest-papers PATH
  python qsearch.py propose
  python qsearch.py validate
  python qsearch.py list
"""

from __future__ import annotations

import os
import sys

_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
_CORE_DIR = os.path.join(_ROOT_DIR, "core")
_THEOREMS_DIR = os.path.join(_ROOT_DIR, "theorems")

for _p in [_ROOT_DIR, _CORE_DIR, _THEOREMS_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# The monolith imported theorems/coset_typical_modular_gap_bound.py for every command, and
# that module raises this limit. Keep it, without importing the module.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(100_000)

# The subcommands live in qsearch_cli/, one module per research domain. Every name this
# file used to import, and every command_* function, still resolves as qsearch.<name>. It
# is looked up when it is used, so startup no longer loads every theorem module.


def __getattr__(name: str):
    from qsearch_cli.resolve import resolve

    return resolve(name)


def build_parser():
    from qsearch_cli.parser import build_parser as _build_parser

    return _build_parser(description=__doc__, extend=_legacy_extensions)


def main(argv: list[str] | None = None) -> int:
    from qsearch_cli.main import run

    return run(argv, build_parser())


# -----------------------------------------------------------------------------------------
# Old-style additions still work. Put new imports and command_* functions above this
# block, and their add_parser lines inside _legacy_extensions. Running
#     python tools/split_cli/migrate.py sweep --root .
# later moves them into qsearch_cli/. Adding them to qsearch_cli/commands/ directly is
# preferred; see tools/split_cli/README.md.
# -----------------------------------------------------------------------------------------


def _legacy_extensions(subparsers) -> None:
    pass  # legacy-extensions


# Old-style code above may read any name the monolith had (json, Path, validate_registry,
# command_*). Bind exactly the names it reads. With no old-style code this binds nothing.
from qsearch_cli.legacy import bind as _bind_legacy_globals  # noqa: E402

_bind_legacy_globals(globals())


if __name__ == "__main__":
    import qsearch

    raise SystemExit(qsearch.main())

# Subsystem CLI hook: dcp-coherent-multi-representative-amplitude-equalization-bridge -> theorems.dcp_coherent_multi_representative_amplitude_equalization_bridge

# Subsystem CLI hook: dcp-adaptive-bayesian-posterior-phase-alignment-bridge -> theorems.dcp_adaptive_bayesian_posterior_phase_alignment_bridge

# Subsystem CLI hook: dcp-hypergraph-phase-gate-cz-ccz-carry-elimination-bridge -> theorems.dcp_hypergraph_phase_gate_cz_ccz_carry_elimination_bridge

# Subsystem CLI hook: dcp-noisy-syndrome-measurement-readout-bitflip-bridge -> theorems.dcp_noisy_syndrome_measurement_readout_bitflip_bridge

# Subsystem CLI hook: dcp-gaussian-vs-sine-window-lwe-fourier-leakage-bridge -> theorems.dcp_gaussian_vs_sine_window_lwe_fourier_leakage_bridge

# Subsystem CLI hook: dcp-non-abelian-wreath-product-pair-swap-commutant-bridge -> theorems.dcp_non_abelian_wreath_product_pair_swap_commutant_bridge

# Subsystem CLI hook: dcp-modular-inversion-newton-hensel-lifting-quantum-bridge -> theorems.dcp_modular_inversion_newton_hensel_lifting_quantum_bridge

# Subsystem CLI hook: dcp-sparse-parity-with-noise-ldpc-belief-propagation-bridge -> theorems.dcp_sparse_parity_with_noise_ldpc_belief_propagation_bridge

# Subsystem CLI hook: dcp-quantum-phase-estimation-continued-fraction-q-prime-bridge -> theorems.dcp_quantum_phase_estimation_continued_fraction_q_prime_bridge

# Subsystem CLI hook: dcp-multi-secret-block-matrix-simultaneous-peeling-bridge -> theorems.dcp_multi_secret_block_matrix_simultaneous_peeling_bridge

# Subsystem CLI hook: dcp-clifford-stabilizer-magic-monotone-carry-injection-bridge -> theorems.dcp_clifford_stabilizer_magic_monotone_carry_injection_bridge

# Subsystem CLI hook: dcp-post-selected-weak-value-phase-amplification-obstruction -> theorems.dcp_post_selected_weak_value_phase_amplification_obstruction

# Subsystem CLI hook: dcp-cyclotomic-ring-rlwe-circulant-cnot-shift-invariance-bridge -> theorems.dcp_cyclotomic_ring_rlwe_circulant_cnot_shift_invariance_bridge

# Subsystem CLI hook: dcp-quantum-rejection-sampling-lorentzian-vs-cosine-target-bridge -> theorems.dcp_quantum_rejection_sampling_lorentzian_vs_cosine_target_bridge

# Subsystem CLI hook: dcp-bipartite-entanglement-entropy-syndrome-cut-bridge -> theorems.dcp_bipartite_entanglement_entropy_syndrome_cut_bridge

# Subsystem CLI hook: dcp-end-to-end-hybrid-cnot-hensel-feedforward-receiver-bridge -> theorems.dcp_end_to_end_hybrid_cnot_hensel_feedforward_receiver_bridge

# Subsystem CLI hook: dcp-quantum-singular-value-transformation-pgm-chebyshev-bridge -> theorems.dcp_quantum_singular_value_transformation_pgm_chebyshev_bridge

# Subsystem CLI hook: dcp-galois-frobenius-automorphism-prime-power-peeling-bridge -> theorems.dcp_galois_frobenius_automorphism_prime_power_peeling_bridge

# Subsystem CLI hook: dcp-multi-level-richardson-extrapolation-dephasing-mitigation-bridge -> theorems.dcp_multi_level_richardson_extrapolation_dephasing_mitigation_bridge

# Subsystem CLI hook: dcp-quadratic-residue-legendre-gauss-sum-phase-oracle-bridge -> theorems.dcp_quadratic_residue_legendre_gauss_sum_phase_oracle_bridge

# Subsystem CLI hook: dcp-symplectic-clifford-stabilizer-tableau-witness-compiler-bridge -> theorems.dcp_symplectic_clifford_stabilizer_tableau_witness_compiler_bridge

# Subsystem CLI hook: dcp-coherent-cnot-uncomputation-echo-loschmidt-visibility-bridge -> theorems.dcp_coherent_cnot_uncomputation_echo_loschmidt_visibility_bridge

# Subsystem CLI hook: dcp-lattice-gram-schmidt-babai-nearest-plane-vs-rounding-bridge -> theorems.dcp_lattice_gram_schmidt_babai_nearest_plane_vs_rounding_bridge

# Subsystem CLI hook: dcp-composite-crt-coprime-modulus-tensor-factorization-bridge -> theorems.dcp_composite_crt_coprime_modulus_tensor_factorization_bridge

# Subsystem CLI hook: dcp-walsh-hadamard-gold-bent-nonlinear-carry-spectrum-bridge -> theorems.dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_bridge

# Subsystem CLI hook: dcp-multi-antenna-mimo-spatial-diversity-combining-bridge -> theorems.dcp_multi_antenna_mimo_spatial_diversity_combining_bridge

# Subsystem CLI hook: dcp-kitaev-phase-estimation-hadamard-test-bit-by-bit-bridge -> theorems.dcp_kitaev_phase_estimation_hadamard_test_bit_by_bit_bridge

# Subsystem CLI hook: dcp-haar-random-vs-dihedral-2-design-frame-potential-bridge -> theorems.dcp_haar_random_vs_dihedral_2_design_frame_potential_bridge

# Subsystem CLI hook: dcp-quantum-z-error-detection-stabilizer-iceberg-code-bridge -> theorems.dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge

# Subsystem CLI hook: dcp-non-stationary-markov-drift-secret-tracking-kalman-bridge -> theorems.dcp_non_stationary_markov_drift_secret_tracking_kalman_bridge

# Subsystem CLI hook: dcp-short-integer-solution-sis-dual-homomorphic-trapdoor-bridge -> theorems.dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_bridge

# Subsystem CLI hook: dcp-grand-synthesis-50-subsystem-taxonomy-and-frontier-bridge -> theorems.dcp_grand_synthesis_50_subsystem_taxonomy_and_frontier_bridge
