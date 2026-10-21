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

# Subsystem CLI hook: dcp-quantum-amplitude-amplification-grover-reflection-witness-bridge -> theorems.dcp_quantum_amplitude_amplification_grover_reflection_witness_bridge

# Subsystem CLI hook: dcp-fixed-point-pi-over-3-grover-syndrome-amplification-bridge -> theorems.dcp_fixed_point_pi_over_3_grover_syndrome_amplification_bridge

# Subsystem CLI hook: dcp-radix-4-quaternary-qft-butterfly-depth-halving-bridge -> theorems.dcp_radix_4_quaternary_qft_butterfly_depth_halving_bridge

# Subsystem CLI hook: dcp-quantum-chernoff-information-geodesic-exponent-bridge -> theorems.dcp_quantum_chernoff_information_geodesic_exponent_bridge

# Subsystem CLI hook: dcp-pauli-twirling-coherent-carry-to-stochastic-dephasing-bridge -> theorems.dcp_pauli_twirling_coherent_carry_to_stochastic_dephasing_bridge

# Subsystem CLI hook: dcp-reed-muller-boolean-polynomial-degree-cnot-depth-bridge -> theorems.dcp_reed_muller_boolean_polynomial_degree_cnot_depth_bridge

# Subsystem CLI hook: dcp-adaptive-sequential-probability-ratio-test-wald-peeling-bridge -> theorems.dcp_adaptive_sequential_probability_ratio_test_wald_peeling_bridge

# Subsystem CLI hook: dcp-non-clifford-t-count-resource-tradeoff-cnot-vs-qft-bridge -> theorems.dcp_non_clifford_t_count_resource_tradeoff_cnot_vs_qft_bridge

# Subsystem CLI hook: dcp-quantum-slepian-prolate-spheroidal-discrete-window-bridge -> theorems.dcp_quantum_slepian_prolate_spheroidal_discrete_window_bridge

# Subsystem CLI hook: dcp-quantum-fano-holevo-mutual-information-sample-lower-bound-bridge -> theorems.dcp_quantum_fano_holevo_mutual_information_sample_lower_bound_bridge

# Subsystem CLI hook: dcp-non-binary-reed-solomon-vandermonde-qudit-witness-bridge -> theorems.dcp_non_binary_reed_solomon_vandermonde_qudit_witness_bridge

# Subsystem CLI hook: dcp-magic-state-distillation-15-to-1-reed-muller-peeling-cost-bridge -> theorems.dcp_magic_state_distillation_15_to_1_reed_muller_peeling_cost_bridge

# Subsystem CLI hook: dcp-entanglement-assisted-pre-shared-ebit-superdense-phase-bridge -> theorems.dcp_entanglement_assisted_pre_shared_ebit_superdense_phase_bridge

# Subsystem CLI hook: dcp-clifford-cnot-depth-logarithmic-tree-vs-linear-chain-bridge -> theorems.dcp_clifford_cnot_depth_logarithmic_tree_vs_linear_chain_bridge

# Subsystem CLI hook: dcp-prime-field-f-p-berlekamp-massey-linear-recurrence-peeling-bridge -> theorems.dcp_prime_field_f_p_berlekamp_massey_linear_recurrence_peeling_bridge

# Subsystem CLI hook: dcp-master-verification-82-subsystem-comprehensive-ledger-bridge -> theorems.dcp_master_verification_82_subsystem_comprehensive_ledger_bridge

# Subsystem CLI hook: dcp-even-sublattice-parity-blindness-and-rescaling-bridge -> theorems.dcp_even_sublattice_parity_blindness_and_rescaling_bridge

# Subsystem CLI hook: planted-qary-macwilliams-dual-weight-enumerator-bridge -> theorems.planted_qary_macwilliams_dual_weight_enumerator_bridge

# Subsystem CLI hook: native-higher-call-composite-modulus-crt-factorization-audit -> theorems.native_higher_call_composite_modulus_crt_factorization_audit

# Subsystem CLI hook: dcp-multi-packet-product-twirl-sq-dimension-audit -> theorems.dcp_multi_packet_product_twirl_sq_dimension_audit

# Subsystem CLI hook: dcp-coherent-syndrome-uncomputation-reversible-oracle-bridge -> theorems.dcp_coherent_syndrome_uncomputation_reversible_oracle_bridge

# Subsystem CLI hook: dcp-sieve-bucket-collision-birthday-tradeoff-audit -> theorems.dcp_sieve_bucket_collision_birthday_tradeoff_audit

# Subsystem CLI hook: dcp-twisted-convolution-pretty-good-measurement-gram-bridge -> theorems.dcp_twisted_convolution_pretty_good_measurement_gram_bridge

# Subsystem CLI hook: dcp-dyadic-valuation-anchor-invariance-hierarchy-bridge -> theorems.dcp_dyadic_valuation_anchor_invariance_hierarchy_bridge

# Subsystem CLI hook: dcp-bell-conjugate-pair-phase-cancellation-obstruction -> theorems.dcp_bell_conjugate_pair_phase_cancellation_obstruction

# Subsystem CLI hook: dcp-coset-subspace-qft-concentration-and-leakage-bridge -> theorems.dcp_coset_subspace_qft_concentration_and_leakage_bridge

# Subsystem CLI hook: dcp-cyclic-group-qft-dihedral-coset-interference-bridge -> theorems.dcp_cyclic_group_qft_dihedral_coset_interference_bridge

# Subsystem CLI hook: dcp-adaptive-hybrid-classical-quantum-peeling-sample-complexity-bridge -> theorems.dcp_adaptive_hybrid_classical_quantum_peeling_sample_complexity_bridge

# Subsystem CLI hook: dcp-overlapping-cnot-dag-carry-fanout-obstruction -> theorems.dcp_overlapping_cnot_dag_carry_fanout_obstruction

# Subsystem CLI hook: dcp-sine-window-fejer-dirichlet-kernel-cutoff-bridge -> theorems.dcp_sine_window_fejer_dirichlet_kernel_cutoff_bridge

# Subsystem CLI hook: dcp-anchor-conditioned-adaptive-syndrome-routing-bridge -> theorems.dcp_anchor_conditioned_adaptive_syndrome_routing_bridge

# Subsystem CLI hook: dcp-multicopy-schur-weyl-symmetric-projection-bridge -> theorems.dcp_multicopy_schur_weyl_symmetric_projection_bridge

# Subsystem CLI hook: dcp-cascaded-dyadic-adaptive-kernel-weight-pruning-bridge -> theorems.dcp_cascaded_dyadic_adaptive_kernel_weight_pruning_bridge

# Subsystem CLI hook: dcp-multicopy-distinct-header-cyclic-swap-interference-bridge -> theorems.dcp_multicopy_distinct_header_cyclic_swap_interference_bridge

# Subsystem CLI hook: dcp-cnot-conjugated-schur-weyl-clifford-twirl-bridge -> theorems.dcp_cnot_conjugated_schur_weyl_clifford_twirl_bridge

# Subsystem CLI hook: dcp-dihedral-vs-heisenberg-two-copy-commutant-bridge -> theorems.dcp_dihedral_vs_heisenberg_two_copy_commutant_bridge

# Subsystem CLI hook: dcp-noisy-cascaded-dyadic-peeling-sample-complexity-bridge -> theorems.dcp_noisy_cascaded_dyadic_peeling_sample_complexity_bridge

# Subsystem CLI hook: dcp-odd-prime-modulus-cnot-carry-shift-obstruction -> theorems.dcp_odd_prime_modulus_cnot_carry_shift_obstruction

# Subsystem CLI hook: dcp-heisenberg-dyadic-boundary-cocycle-repair-bridge -> theorems.dcp_heisenberg_dyadic_boundary_cocycle_repair_bridge

# Subsystem CLI hook: dcp-correlated-z-fault-syndrome-parity-twirl-bridge -> theorems.dcp_correlated_z_fault_syndrome_parity_twirl_bridge

# Subsystem CLI hook: dcp-multi-target-reusable-syndrome-bank-amortization-bridge -> theorems.dcp_multi_target_reusable_syndrome_bank_amortization_bridge

# Subsystem CLI hook: dcp-tensor-power-k-moment-dihedral-twirl-bridge -> theorems.dcp_tensor_power_k_moment_dihedral_twirl_bridge

# Subsystem CLI hook: dcp-ternary-signed-witness-cnot-routing-bridge -> theorems.dcp_ternary_signed_witness_cnot_routing_bridge

# Subsystem CLI hook: dcp-coherent-syndrome-sign-flip-pauli-frame-bridge -> theorems.dcp_coherent_syndrome_sign_flip_pauli_frame_bridge

# Subsystem CLI hook: dcp-banded-qft-truncation-vs-dyadic-cnot-fidelity-bridge -> theorems.dcp_banded_qft_truncation_vs_dyadic_cnot_fidelity_bridge

# Subsystem CLI hook: dcp-multi-packet-collective-helstrom-product-likelihood-bridge -> theorems.dcp_multi_packet_collective_helstrom_product_likelihood_bridge

# Subsystem CLI hook: dcp-ternary-pgm-gram-eigenvalue-success-bridge -> theorems.dcp_ternary_pgm_gram_eigenvalue_success_bridge

# Subsystem CLI hook: dcp-coherent-fiber-support-erasure-inversion-bridge -> theorems.dcp_coherent_fiber_support_erasure_inversion_bridge

# Subsystem CLI hook: dcp-d-ary-qudit-phase-register-cnot-mod-d-bridge -> theorems.dcp_d_ary_qudit_phase_register_cnot_mod_d_bridge

# Subsystem CLI hook: dcp-sine-vs-box-window-pair-difference-overlap-bridge -> theorems.dcp_sine_vs_box_window_pair_difference_overlap_bridge

# Subsystem CLI hook: dcp-quantum-phase-estimation-kaiser-bessel-chebyshev-dolph-window-bridge -> theorems.dcp_quantum_phase_estimation_kaiser_bessel_chebyshev_dolph_window_bridge

# Subsystem CLI hook: dcp-krawtchouk-polynomial-binary-hamming-scheme-macwilliams-cnot-bridge -> theorems.dcp_krawtchouk_polynomial_binary_hamming_scheme_macwilliams_cnot_bridge

# Subsystem CLI hook: dcp-quantum-fisher-information-matrix-multiparameter-cramer-rao-bridge -> theorems.dcp_quantum_fisher_information_matrix_multiparameter_cramer_rao_bridge

# Subsystem CLI hook: dcp-hidden-shift-bent-function-roetteler-involutory-dual-bridge -> theorems.dcp_hidden_shift_bent_function_roetteler_involutory_dual_bridge

# Subsystem CLI hook: dcp-noisy-quantum-ram-bucket-brigade-routing-fault-scaling-bridge -> theorems.dcp_noisy_quantum_ram_bucket_brigade_routing_fault_scaling_bridge

# Subsystem CLI hook: dcp-modular-hermite-normal-form-determinant-smith-peeling-bridge -> theorems.dcp_modular_hermite_normal_form_determinant_smith_peeling_bridge

# Subsystem CLI hook: dcp-continuous-variable-gkp-modular-grid-stabilizer-peeling-bridge -> theorems.dcp_continuous_variable_gkp_modular_grid_stabilizer_peeling_bridge

# Subsystem CLI hook: dcp-shadow-tomography-classical-shadows-pauli-observable-sample-bridge -> theorems.dcp_shadow_tomography_classical_shadows_pauli_observable_sample_bridge

# Subsystem CLI hook: dcp-quantum-ziv-zakai-bellman-minimax-phase-lower-bound-bridge -> theorems.dcp_quantum_ziv_zakai_bellman_minimax_phase_lower_bound_bridge

# Subsystem CLI hook: dcp-measurement-based-mbqc-cluster-state-cnot-peeling-bridge -> theorems.dcp_measurement_based_mbqc_cluster_state_cnot_peeling_bridge

# Subsystem CLI hook: dcp-quantum-linear-systems-hhl-condition-number-modular-inversion-bridge -> theorems.dcp_quantum_linear_systems_hhl_condition_number_modular_inversion_bridge

# Subsystem CLI hook: dcp-floquet-dynamical-decoupling-carr-purcell-udds-carry-filter-bridge -> theorems.dcp_floquet_dynamical_decoupling_carr_purcell_udds_carry_filter_bridge

# Subsystem CLI hook: dcp-quantum-sanov-theorem-large-deviations-kl-syndrome-hypothesis-bridge -> theorems.dcp_quantum_sanov_theorem_large_deviations_kl_syndrome_hypothesis_bridge

# Subsystem CLI hook: dcp-majorana-fermionic-gaussian-matchgate-parity-peeling-bridge -> theorems.dcp_majorana_fermionic_gaussian_matchgate_parity_peeling_bridge

# Subsystem CLI hook: dcp-quantum-wasserstein-ornstein-uhlenbeck-cooling-dissipative-peeling-bridge -> theorems.dcp_quantum_wasserstein_ornstein_uhlenbeck_cooling_dissipative_peeling_bridge

# Subsystem CLI hook: dcp-galois-ring-gr-4-m-nechaev-kloosterman-hensel-carry-bridge -> theorems.dcp_galois_ring_gr_4_m_nechaev_kloosterman_hensel_carry_bridge

# Subsystem CLI hook: dcp-quantum-network-distributed-teleportation-bell-pair-cnot-peeling-bridge -> theorems.dcp_quantum_network_distributed_teleportation_bell_pair_cnot_peeling_bridge

# Subsystem CLI hook: dcp-centennial-100-subsystem-master-audit-and-completeness-bridge -> theorems.dcp_centennial_100_subsystem_master_audit_and_completeness_bridge

# Subsystem CLI hook: dcp-quantum-renyi-petz-sandwiched-divergence-hypothesis-bridge -> theorems.dcp_quantum_renyi_petz_sandwiched_divergence_hypothesis_bridge

# Subsystem CLI hook: dcp-expander-graph-margulis-ramanujan-ldpc-syndrome-peeling-bridge -> theorems.dcp_expander_graph_margulis_ramanujan_ldpc_syndrome_peeling_bridge

# Subsystem CLI hook: dcp-quantum-kramers-kronig-causal-susceptibility-phase-dispersion-bridge -> theorems.dcp_quantum_kramers_kronig_causal_susceptibility_phase_dispersion_bridge

# Subsystem CLI hook: dcp-representation-theory-schur-weyl-symmetric-subspace-permutation-bridge -> theorems.dcp_representation_theory_schur_weyl_symmetric_subspace_permutation_bridge

# Subsystem CLI hook: dcp-topological-surface-code-lattice-surgery-zz-merge-split-cnot-bridge -> theorems.dcp_topological_surface_code_lattice_surgery_zz_merge_split_cnot_bridge

# Subsystem CLI hook: dcp-bernstein-vazirani-fourier-sampling-vs-nonlinear-bent-walsh-bridge -> theorems.dcp_bernstein_vazirani_fourier_sampling_vs_nonlinear_bent_walsh_bridge
