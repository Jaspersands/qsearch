import json
import os
import tempfile
import unittest
from pathlib import Path

from code_equivalence_workbench import hamming_7_4_generator, permute_columns
from experiment_runner import (
    EXPERIMENT_RUN_HISTORY_PATH,
    EXPERIMENT_TRENDS_PATH,
    run_experiment,
    run_next_experiment,
    run_supported_experiments,
    select_next_experiment,
    supported_experiment_ids,
    write_experiment_trends,
)
from mutation_engine import write_mutation_report
from conjecture_tracker import write_conjecture_report
from dequantization_checks import write_dequantization_report
from research_registry import (
    ExperimentRecord,
    initialize_seed_registry,
    load_candidates,
    load_experiment_results,
    load_experiments,
    load_mutation_proposals,
    save_experiments,
    upsert_experiment,
    validate_registry,
)


class ExperimentRunnerTests(unittest.TestCase):
    def test_new_coset_measurement_pipeline_is_supported_and_dispatches(self):
        experiment_ids = {
            "EXP-COSET-NATURAL-MULTICOPY-PGM",
            "EXP-COSET-PGM-GAIN-LOCALIZATION",
            "EXP-COSET-PGM-AVERAGE-FRAME-BLOCK-ENCODING",
            "EXP-COSET-NATURAL-CHARACTER-RATIO-CONCENTRATION",
            "EXP-COSET-COVARIANT-PROJECTOR-SUBPOVM",
            "EXP-CODE-SELF-DUAL-WREATH-PROJECTOR-SUBPOVM",
            "EXP-CODE-SELF-DUAL-WREATH-SUBPOVM-MOMENTS",
            "EXP-CODE-SELF-DUAL-WREATH-NATURAL-UNEQUAL-DOMINANCE",
            "EXP-CODE-SELF-DUAL-WREATH-NATURAL-MOMENT-WORD-MAP",
            "EXP-CODE-SELF-DUAL-WREATH-WORD-MAP-MIXING",
            "EXP-CODE-SELF-DUAL-WREATH-COUPLED-WORD-WALK-GAP",
            "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-CONDITIONED-KERNEL",
            "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-PARTITION-COLLISION",
            "EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-FRAME-PROBE",
            "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-RATIO-CONTRACT",
            "EXP-CODE-SELF-DUAL-WREATH-SHORT-WORD-PROFILE",
            "EXP-CODE-SELF-DUAL-WREATH-MASK-HYPERGRAPH-REDUCTION",
            "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-TWIRL-REDUCTION",
            "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FOURIER-REDUCTION",
            "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT",
        }
        self.assertTrue(
            experiment_ids.issubset(set(supported_experiment_ids()))
        )
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SUBPOVM-MOMENTS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_subpovm_moment_certificate",
            record["artifacts"],
        )
        self.assertEqual(
            record["metrics"][
                "all_sector_growing_order_moment_contraction_count"
            ],
            0,
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coupled_word_walk_gap_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COUPLED-WORD-WALK-GAP"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_coupled_word_walk_gap",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_all_unequal_conditioned_kernel_dispatches_from_clean_registry(
        self,
    ):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-CONDITIONED-KERNEL"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_all_unequal_conditioned_kernel",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_global_partition_collision_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-PARTITION-COLLISION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_global_partition_collision",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_collision_free_frame_probe_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-FRAME-PROBE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_collision_free_frame_probe",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_character_ratio_contract_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-RATIO-CONTRACT"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_character_ratio_contract",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_short_word_profile_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SHORT-WORD-PROFILE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_short_word_profile",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_mask_hypergraph_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-MASK-HYPERGRAPH-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_mask_hypergraph_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_subgroup_twirl_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-TWIRL-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_subgroup_twirl_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_orientation_fourier_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FOURIER-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_orientation_fourier_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_orientation_fusion_moment_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_orientation_fusion_moment",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_pair_core_carrier_factorization_dispatches_from_clean_registry(
        self,
    ):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pair_core_carrier_factorization",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_multistar_degree_obstruction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_multistar_degree_obstruction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_pair_quotient_overlap_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PAIR-QUOTIENT-OVERLAP"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pair_quotient_overlap",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_recursive_pair_generation_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-PAIR-GENERATION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_recursive_pair_generation",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_augmented_common_core_cech_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-COMMON-CORE-CECH"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_augmented_common_core_cech",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_common_core_cech_laplacian_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-CECH-LAPLACIAN"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_common_core_cech_laplacian",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_pair_core_recoupling_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RECOUPLING-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pair_core_recoupling_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_common_core_atomization_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-ATOMIZATION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_common_core_atomization",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_orientation_laplacian_gap_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_orientation_laplacian_gap",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_orientation_common_range_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COMMON-RANGE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_orientation_common_range",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_orientation_triple_range_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-TRIPLE-RANGE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_orientation_triple_range",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_orientation_pair_angles_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-PAIR-ANGLES"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_orientation_pair_angle_spectrum",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_orientation_block_common_core_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-BLOCK-COMMON-CORE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_orientation_block_common_core",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_plancherel_block_obstruction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-OBSTRUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_plancherel_block_obstruction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_spectral_trimmed_subpovm_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-TRIMMED-SUBPOVM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_spectral_trimmed_subpovm",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_spectral_filter_degree_obstruction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-DEGREE-OBSTRUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_spectral_filter_degree_obstruction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_plancherel_block_mass_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-MASS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_plancherel_block_mass",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_orientation_covariant_quotient_obstruction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COVARIANT-QUOTIENT-OBSTRUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_orientation_covariant_quotient_obstruction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_branch_controlled_invariant_filter_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CONTROLLED-INVARIANT-FILTER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_branch_controlled_invariant_filter",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_block_common_core_quotient_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-BLOCK-COMMON-CORE-QUOTIENT"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_block_common_core_quotient",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_paired_block_filter_bypass_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PAIRED-BLOCK-FILTER-BYPASS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_paired_block_filter_bypass",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_local_isotypic_filter_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-LOCAL-ISOTYPIC-FILTER-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_local_isotypic_filter_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_cluster_locality_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-CLUSTER-LOCALITY-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_cluster_locality_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_spectral_filter_query_lower_bound_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-QUERY-LOWER-BOUND"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_spectral_filter_query_lower_bound",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_affine_core_flag_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-CORE-FLAG-THEOREM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_affine_core_flag_theorem",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_affine_node_common_outlier_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-NODE-COMMON-OUTLIER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_affine_node_common_outlier",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_affine_plane_scalar_holonomy_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SCALAR-HOLONOMY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_affine_plane_scalar_holonomy",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_affine_plane_support_pressure_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SUPPORT-PRESSURE-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_affine_plane_support_pressure_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_affine_recoupling_bundle_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-RECOUPLING-BUNDLE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_affine_recoupling_bundle",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_affine_relation_weighted_bulk_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-RELATION-WEIGHTED-BULK"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_affine_relation_weighted_bulk",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_affine_star_channel_gap_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-STAR-CHANNEL-GAP"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_affine_star_channel_gap",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_augmented_h0_dimension_obstruction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-H0-DIMENSION-OBSTRUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_augmented_h0_dimension_obstruction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_canonical_coefficient_affine_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-CANONICAL-COEFFICIENT-AFFINE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_canonical_coefficient_affine",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_cayley_fiber_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-CAYLEY-FIBER-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_cayley_fiber_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_central_support_rank_bridge_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-CENTRAL-SUPPORT-RANK-BRIDGE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_central_support_rank_bridge",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_coherent_fourier_decoder_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COHERENT-FOURIER-DECODER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_coherent_fourier_decoder",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_collision_free_event_transfer_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-EVENT-TRANSFER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_collision_free_event_transfer",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_common_core_polar_bypass_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-POLAR-BYPASS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_common_core_polar_bypass",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_complete_s6_vertex_channel_audit_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-S6-VERTEX-CHANNEL-AUDIT"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_complete_s6_vertex_channel_audit",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_random_fourier_bridge_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                self.assertIn("EXP-DHS-DCP-RANDOM-FOURIER-BRIDGE", supported_experiment_ids())
                result = run_experiment("EXP-DHS-DCP-RANDOM-FOURIER-BRIDGE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_hidden_number_bridge", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_exact_f1_sample_robustness_count"], 1)
        self.assertEqual(record["metrics"]["proved_polynomial_time_decoder_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_sparse_fourier_transfer_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SPARSE-FOURIER-TRANSFER-AUDIT"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_sparse_fourier_transfer_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_polylog_random_example_decoder_count"], 0)
        self.assertEqual(record["metrics"]["proved_general_random_example_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_iid_linear_hash_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-IID-LINEAR-HASH-ESTIMATOR"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_iid_hash_estimator_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_exact_linear_estimator_no_go_count"], 1)
        self.assertEqual(record["metrics"]["proved_nonlinear_decoder_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_biased_linear_margin_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-IID-BIASED-LINEAR-MARGIN"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_biased_linear_margin_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_uniform_margin_linear_no_go_count"], 1)
        self.assertEqual(record["metrics"]["proved_nonlinear_decoder_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_multirecord_hierarchy_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-IID-MULTIRECORD-HIERARCHY"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_multirecord_estimator_hierarchy", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_disjoint_block_multilinear_no_go_count"], 1)
        self.assertEqual(record["metrics"]["proved_overlapping_ustatistic_lower_bound_count"], 0)
        self.assertEqual(record["metrics"]["proved_collective_measurement_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_ustatistic_variance_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-IID-USTATISTIC-VARIANCE"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_ustatistic_variance_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_overlapping_ustatistic_variance_bound_count"], 1)
        self.assertEqual(record["metrics"]["joint_polynomial_explicit_resource_row_count"], 0)
        self.assertEqual(record["metrics"]["proved_implicit_contraction_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_factorized_contraction_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-IID-FACTORIZED-CONTRACTION"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_factorized_contraction_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_rank_one_implicit_contraction_no_go_count"], 1)
        self.assertEqual(record["metrics"]["joint_polynomial_resource_row_count"], 0)
        self.assertEqual(record["metrics"]["proved_polynomial_rank_contraction_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_low_rank_contraction_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-IID-LOW-RANK-CONTRACTION"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_low_rank_contraction_search", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_uniform_low_rank_family_count"], 0)
        self.assertEqual(record["metrics"]["proved_exact_f1_robust_low_rank_decoder_count"], 0)
        self.assertEqual(record["metrics"]["proved_lattice_composition_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_measurement_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-MEASUREMENT-AUDIT"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_measurement_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["qft_uniformity_failure_count"], 0)
        self.assertEqual(record["metrics"]["proved_polynomial_collective_measurement_count"], 0)
        self.assertEqual(record["metrics"]["proved_exact_f1_robust_decoder_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_hashed_fiber_measurement_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-HASHED-FIBER-MEASUREMENT-AUDIT"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_hashed_fiber_measurement_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["mean_identity_failure_count"], 0)
        self.assertEqual(record["metrics"]["proved_polynomial_fiber_symmetrization_count"], 0)
        self.assertEqual(record["metrics"]["proved_exact_f1_robust_decoder_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_likelihood_branch_bound_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-LIKELIHOOD-BRANCH-BOUND"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_likelihood_branch_bound", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_polynomial_branch_bound_count"], 0)
        self.assertEqual(record["metrics"]["proved_nonlinear_decoder_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_two_adic_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-TWO-ADIC-SEARCH"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_two_adic_search", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_uniform_polynomial_two_adic_solver_count"], 0)
        self.assertEqual(record["metrics"]["source_contract_satisfying_row_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_resource_frontier_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-RESOURCE-FRONTIER"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_resource_frontier", record["artifacts"])
        self.assertEqual(record["metrics"]["known_polynomial_time_algorithm_count"], 0)
        self.assertEqual(record["metrics"]["known_regev_contract_satisfying_algorithm_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_carry_anf_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-CARRY-ANF"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_carry_anf", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_polynomial_algebraic_witness_solver_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_solver_synthesis_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-SOLVER-SYNTHESIS"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_solver_synthesis", record["artifacts"])
        self.assertEqual(record["metrics"]["accepted_candidate_count"], 0)
        self.assertGreater(record["metrics"]["proposal_only_survivor_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_low_bit_bdd_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-LOW-BIT-BDD"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_low_bit_bdd", record["artifacts"])
        self.assertGreater(record["metrics"]["polynomial_width_certificate_count"], 0)
        self.assertEqual(record["metrics"]["proved_polynomial_witness_solver_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_conditioned_quotient_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-CONDITIONED-QUOTIENT"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_conditioned_quotient", record["artifacts"])
        self.assertGreater(record["metrics"]["minimum_tail_normalized_shannon_entropy"], 0.0)
        self.assertEqual(record["metrics"]["proved_polynomial_high_bit_decoder_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_carry_slice_lattice_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-CARRY-SLICE-LATTICE"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_carry_slice_lattice", record["artifacts"])
        self.assertEqual(record["metrics"]["invalid_witness_count"], 0)
        self.assertEqual(record["metrics"]["proved_uniform_inverse_polynomial_coverage_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_target_distribution_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-TARGET-DISTRIBUTION"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_target_distribution", record["artifacts"])
        self.assertGreater(record["metrics"]["moment_certificate_count"], 0)
        self.assertEqual(record["metrics"]["proved_polynomial_representation_solver_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_coherent_matching_interface_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-COHERENT-MATCHING-INTERFACE"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_coherent_matching_interface", record["artifacts"])
        self.assertGreater(record["metrics"]["proved_seeded_randomized_solver_bridge_count"], 0)
        self.assertEqual(record["metrics"]["proved_arbitrary_quantum_relation_solver_bridge_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_random_self_reduction_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-RANDOM-SELF-REDUCTION"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_random_self_reduction", record["artifacts"])
        self.assertGreater(record["metrics"]["source_distribution_bijection_certificate_count"], 0)
        self.assertEqual(record["metrics"]["proved_uniform_inverse_polynomial_legal_coverage_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_odd_unit_orbit_geometry_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-ODD-UNIT-ORBIT-GEOMETRY"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_odd_unit_orbit_geometry", record["artifacts"])
        self.assertGreater(record["metrics"]["full_two_adic_invariant_certificate_count"], 0)
        self.assertEqual(record["metrics"]["proved_inverse_polynomial_easy_orbit_measure_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_run_supported_hidden_shift_experiment_writes_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-GOWERS-SPECTRUM")
                records = load_experiment_results()
                validation = validate_registry()
                history_exists = EXPERIMENT_RUN_HISTORY_PATH.exists()
                trends_exists = EXPERIMENT_TRENDS_PATH.exists()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-GOWERS-SPECTRUM" for item in records))
        self.assertTrue(history_exists)
        self.assertTrue(trends_exists)
        self.assertTrue(validation["valid"])

    def test_phase_sieve_experiment_uses_state_sample_native_dcp_backend(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                self.assertIn("EXP-DHS-DCP-SAMPLE-NATIVE-SIEVE", supported_experiment_ids())
                result = run_experiment("EXP-DHS-PHASE-SIEVE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_sample_native_sieve", record["artifacts"])
        self.assertEqual(record["metrics"]["evaluator_query_count"], 0)
        self.assertEqual(record["metrics"]["full_hidden_reflection_decode_count"], 0)
        self.assertGreater(record["metrics"]["postselection_optimism_gap"], 0)
        self.assertTrue(validation["valid"])

    def test_recursive_dcp_decoder_experiment_preserves_claim_gate(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                self.assertIn("EXP-DHS-DCP-RECURSIVE-DECODER", supported_experiment_ids())
                self.assertIn("EXP-DHS-DCP-RECURRENCE-SCALING", supported_experiment_ids())
                result = run_experiment("EXP-DHS-DCP-RECURSIVE-DECODER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_recursive_decoder", record["artifacts"])
        self.assertEqual(record["metrics"]["evaluator_query_count"], 0)
        self.assertEqual(record["metrics"]["proved_full_failure_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_missing_backend_records_blocked_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                upsert_experiment(
                    ExperimentRecord(
                        id="EXP-UNSUPPORTED-DUMMY",
                        candidate_id="CODE-COSET-COLLECTIVE",
                        title="Unsupported dummy experiment",
                        status="planned",
                        hypothesis="This test-only experiment has no runner.",
                        protocol="No executable protocol.",
                        positive_signal="None.",
                        falsifiers=["Missing runner blocks execution."],
                        metrics=["implemented"],
                        dependencies=[],
                        next_actions=["Add a runner before using this experiment."],
                    )
                )
                result = run_experiment("EXP-UNSUPPORTED-DUMMY")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "blocked-missing-runner")
        blocked = [item for item in records if item["experiment_id"] == "EXP-UNSUPPORTED-DUMMY"]
        self.assertEqual(len(blocked), 1)
        self.assertTrue(blocked[0]["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_coset_rank_experiment_uses_code_equivalence_backend(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-COSET-RANK")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-COSET-RANK-CODE-EQUIVALENCE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_equivalence_audit", record["artifacts"])
        self.assertTrue(validation["valid"])

    def test_code_canonicalization_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-CANONICALIZATION-BASELINE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-CANONICALIZATION-BASELINE-CODE-CANONICALIZATION")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_canonicalization_baseline", record["artifacts"])
        self.assertGreater(record["metrics"]["profile_rejection_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_structural_invariants_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-STRUCTURAL-INVARIANTS")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-STRUCTURAL-INVARIANTS-CODE-EQUIVALENCE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_structural_invariants", record["artifacts"])
        self.assertGreater(record["metrics"]["structural_rejection_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_information_set_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-INFORMATION-SET-CANONICALIZATION")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-INFORMATION-SET-CANONICALIZATION-CODE-EQUIVALENCE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_information_set_baseline", record["artifacts"])
        self.assertGreater(record["metrics"]["information_set_rejection_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_family_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-HARD-FAMILY-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-HARD-FAMILY-SEARCH-CODE-FAMILY-SEARCH")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_family_search", record["artifacts"])
        self.assertGreaterEqual(record["metrics"]["collision_found_count"], 1)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_profile_collision_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-PROFILE-COLLISION-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-PROFILE-COLLISION-SEARCH-CODE-PROFILE-COLLISION")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_profile_collision_search", record["artifacts"])
        self.assertGreater(record["metrics"]["profile_collision_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_tuple_profile_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-TUPLE-PROFILE-BASELINE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-TUPLE-PROFILE-BASELINE-CODE-TUPLE-PROFILE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_tuple_profile_baseline", record["artifacts"])
        self.assertGreater(record["metrics"]["tuple_profile_rejection_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_quasi_cyclic_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-QUASI-CYCLIC-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-QUASI-CYCLIC-SEARCH-QUASI-CYCLIC")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("quasi_cyclic_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["search_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_qc_automorphism_canonicalization_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-CODE-QUASI-CYCLIC-SEARCH")
                result = run_experiment("EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION-QC-AUTOMORPHISM")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("quasi_cyclic_canonicalization", record["artifacts"])
        self.assertGreater(record["metrics"]["record_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_qc_information_set_resolver_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                left = hamming_7_4_generator()
                right = permute_columns(left, [2, 0, 6, 1, 5, 3, 4])
                Path("research/code_equivalence").mkdir(parents=True, exist_ok=True)
                Path("research/code_equivalence/quasi_cyclic_code_search.json").write_text(
                    json.dumps(
                        {
                            "records": [
                                {
                                    "spec": {"id": "qc-test-family"},
                                    "collision_audits": [
                                        {
                                            "id": "qc-test-row",
                                            "length": int(left.shape[1]),
                                            "dimension": int(left.shape[0]),
                                            "generator_a": left.tolist(),
                                            "generator_b": right.tolist(),
                                        }
                                    ],
                                }
                            ]
                        }
                    )
                )
                Path("research/code_equivalence/quasi_cyclic_canonicalization.json").write_text(
                    json.dumps({"records": [{"id": "qc-test-row", "status": "qc-automorphism-no-equivalence-proof-debt"}]})
                )
                result = run_experiment("EXP-CODE-QC-INFORMATION-SET-RESOLVER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-QC-INFORMATION-SET-RESOLVER-CODE-INFOSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("qc_information_set_resolver", record["artifacts"])
        self.assertEqual(record["metrics"]["equivalent_control_count"], 1)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cyclic_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-CYCLIC-ALGEBRAIC-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-CYCLIC-ALGEBRAIC-SEARCH-CYCLIC-CODE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cyclic_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["tuple_collision_count"], 0)
        self.assertGreater(record["metrics"]["dihedral_equivalent_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_goppa_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-GOPPA-ALGEBRAIC-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-GOPPA-ALGEBRAIC-SEARCH-GOPPA-CODE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("goppa_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["tuple_collision_count"], 0)
        self.assertGreater(record["metrics"]["semilinear_control_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_tanner_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-TANNER-LDPC-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-TANNER-LDPC-SEARCH-TANNER")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("tanner_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["tuple_collision_count"], 0)
        self.assertGreater(record["metrics"]["equivalent_control_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_rank_metric_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-RANK-METRIC-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-RANK-METRIC-SEARCH-RANK-METRIC")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("rank_metric_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["block_permutation_control_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_exact_code_incidence_resolver_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                target = Path("research/code_equivalence")
                target.mkdir(parents=True, exist_ok=True)
                left = hamming_7_4_generator()
                right = permute_columns(left, [2, 0, 6, 1, 5, 3, 4])
                (target / "rank_metric_code_search.json").write_text(
                    json.dumps(
                        {
                            "records": [
                                {
                                    "spec": {"id": "runner-rank-family"},
                                    "collision_audits": [
                                        {
                                            "id": "runner-rank-row",
                                            "status": "rank-metric-canonicalization-proof-debt",
                                            "generator_a": left.tolist(),
                                            "generator_b": right.tolist(),
                                        }
                                    ],
                                }
                            ]
                        }
                    )
                )
                result = run_experiment("EXP-CODE-INCIDENCE-ISOMORPHISM-RESOLVER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-INCIDENCE-ISOMORPHISM-RESOLVER-INCIDENCE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_incidence_resolver", record["artifacts"])
        self.assertEqual(record["metrics"]["equivalent_control_count"], 1)
        self.assertEqual(record["metrics"]["verified_permutation_count"], 1)
        self.assertTrue(validation["valid"])

    def test_affine_geometry_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-AFFINE-GEOMETRY-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-AFFINE-GEOMETRY-SEARCH-AFFINE-GEOMETRY")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("affine_geometry_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["affine_control_count"], 0)
        self.assertGreater(record["metrics"]["support_affine_profile_collision_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_projective_geometry_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-PROJECTIVE-GEOMETRY-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-PROJECTIVE-GEOMETRY-SEARCH-PROJECTIVE-GEOMETRY")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("projective_geometry_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["projective_control_count"], 0)
        self.assertGreater(record["metrics"]["support_line_profile_collision_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_frontier_triage_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-CODE-COSET-RANK")
                run_experiment("EXP-CODE-STRUCTURAL-INVARIANTS")
                run_experiment("EXP-CODE-INFORMATION-SET-CANONICALIZATION")
                run_experiment("EXP-CODE-CANONICALIZATION-BASELINE")
                run_experiment("EXP-CODE-HARD-FAMILY-SEARCH")
                run_experiment("EXP-CODE-PROFILE-COLLISION-SEARCH")
                run_experiment("EXP-CODE-TUPLE-PROFILE-BASELINE")
                run_experiment("EXP-CODE-QUASI-CYCLIC-SEARCH")
                run_experiment("EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION")
                result = run_experiment("EXP-CODE-FRONTIER-TRIAGE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-FRONTIER-TRIAGE-CODE-FRONTIER")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_frontier_triage", record["artifacts"])
        self.assertGreater(record["metrics"]["record_count"], 0)
        self.assertGreaterEqual(record["metrics"]["proof_debt_row_count"], 1)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_collective_observable_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-COLLECTIVE-OBSERVABLE-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-COLLECTIVE-OBSERVABLE-SEARCH-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("collective_observable_search", record["artifacts"])
        self.assertGreater(record["metrics"]["observable_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_godsil_mckay_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-GM-SWITCHING-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-GM-SWITCHING-SEARCH-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("godsil_mckay_search", record["artifacts"])
        self.assertGreater(record["metrics"]["nonisomorphic_cospectral_count"], 0)
        self.assertEqual(record["metrics"]["nonclassical_candidate_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cfi_scaling_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-CFI-SCALING")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-CFI-SCALING-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cfi_scaling_probe", record["artifacts"])
        self.assertGreater(record["metrics"]["boundary_record_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cfi_base_family_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-CFI-BASE-FAMILY-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-CFI-BASE-FAMILY-SEARCH-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cfi_base_family_search", record["artifacts"])
        self.assertGreater(record["metrics"]["proof_debt_survivor_count"] + record["metrics"]["finite_survivor_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cfi_parity_solver_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-CFI-PARITY-SOLVER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-CFI-PARITY-SOLVER-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cfi_parity_solver", record["artifacts"])
        self.assertGreater(record["metrics"]["dequantized_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cfi_structural_decoder_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-CFI-STRUCTURAL-DECODER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-CFI-STRUCTURAL-DECODER-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cfi_structural_decoder", record["artifacts"])
        self.assertGreater(record["metrics"]["dequantized_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cfi_irregular_structural_decoder_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-CFI-IRREGULAR-STRUCTURAL-DECODER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-CFI-IRREGULAR-STRUCTURAL-DECODER-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cfi_irregular_structural_decoder", record["artifacts"])
        self.assertGreater(record["metrics"]["dequantized_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cfi_bipartite_structural_decoder_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-CFI-BIPARTITE-STRUCTURAL-DECODER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-CFI-BIPARTITE-STRUCTURAL-DECODER-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cfi_bipartite_structural_decoder", record["artifacts"])
        self.assertGreater(record["metrics"]["dequantized_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_individualized_wl_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-INDIVIDUALIZED-WL")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-INDIVIDUALIZED-WL-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("individualized_wl_baseline", record["artifacts"])
        self.assertGreater(record["metrics"]["dequantized_pair_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_individualized_tensor_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-INDIVIDUALIZED-TENSOR-OBSERVABLES")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-INDIVIDUALIZED-TENSOR-OBSERVABLES-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("individualized_tensor_observables", record["artifacts"])
        self.assertGreater(record["metrics"]["record_count"], 0)
        self.assertEqual(record["metrics"]["nonclassical_candidate_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_coset_frontier_triage_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-COSET-COLLECTIVE-OBSERVABLE-SEARCH")
                run_experiment("EXP-CODE-TENSOR-MEASUREMENT")
                run_experiment("EXP-COSET-INDIVIDUALIZED-WL")
                run_experiment("EXP-COSET-INDIVIDUALIZED-TENSOR-OBSERVABLES")
                run_experiment("EXP-COSET-CFI-PARITY-SOLVER")
                result = run_experiment("EXP-COSET-FRONTIER-TRIAGE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-FRONTIER-TRIAGE-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("coset_frontier_triage", record["artifacts"])
        self.assertGreater(record["metrics"]["rejected_pair_count"], 0)
        self.assertEqual(record["metrics"]["nonclassical_candidate_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_representation_obstruction_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-REPRESENTATION-OBSTRUCTIONS")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-REPRESENTATION-OBSTRUCTIONS-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("representation_obstructions", record["artifacts"])
        self.assertGreater(record["metrics"]["no_go_pressure_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_weak_fourier_signal_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-WEAK-FOURIER-SIGNAL")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-WEAK-FOURIER-SIGNAL-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("weak_fourier_signal", record["artifacts"])
        self.assertGreater(record["metrics"]["near_plancherel_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_coset_state_distinguishability_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-COSET-WEAK-FOURIER-SIGNAL")
                result = run_experiment("EXP-COSET-STATE-DISTINGUISHABILITY")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-STATE-DISTINGUISHABILITY-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("coset_state_distinguishability", record["artifacts"])
        self.assertGreater(record["metrics"]["copy_debt_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_coset_pgm_capacity_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-COSET-WEAK-FOURIER-SIGNAL")
                result = run_experiment("EXP-COSET-PGM-CAPACITY")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-PGM-CAPACITY-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("coset_pgm_capacity", record["artifacts"])
        self.assertGreater(record["metrics"]["measurement_proof_debt_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_tensor_measurement_experiment_uses_graphlet_backend(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-TENSOR-MEASUREMENT")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-TENSOR-MEASUREMENT-GRAPHLET-TENSOR")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("graphlet_tensor_observables", record["artifacts"])
        self.assertGreater(record["metrics"]["observable_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_fourier_compressibility_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-FOURIER-COMPRESSIBILITY")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-FOURIER-COMPRESSIBILITY-FOURIER-COMPRESSIBILITY")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("fourier_compressibility_baselines", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_character_shift_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-CHARACTER-SHIFT-BASELINE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-CHARACTER-SHIFT-BASELINE-CHARACTER-SHIFT")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("character_shift_baselines", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_query_lower_bound_probe_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-QUERY-LOWER-BOUND-PROBES")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-QUERY-LOWER-BOUND-PROBES-QUERY-LOWER-BOUNDS")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("hidden_shift_query_lower_bounds", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_character_decoder_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-CHARACTER-DECODER-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-CHARACTER-DECODER-SEARCH-CHARACTER-DECODER")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("character_decoder_search", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_character_lower_bound_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-CHARACTER-LOWER-BOUND")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-CHARACTER-LOWER-BOUND-CHARACTER-LOWER-BOUND")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("character_shift_lower_bound", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_character_query_information_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-CHARACTER-QUERY-INFORMATION")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-CHARACTER-QUERY-INFORMATION-CHARACTER-QUERY-INFORMATION")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("character_query_information", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_character_moment_obstruction_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-CHARACTER-MOMENT-OBSTRUCTION")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-CHARACTER-MOMENT-OBSTRUCTION-CHARACTER-MOMENTS")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("character_moment_obstruction", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_character_complexity_preprocessing_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-CHARACTER-COMPLEXITY-PREPROCESSING")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(
            result.result_id,
            "RESULT-EXP-DHS-CHARACTER-COMPLEXITY-PREPROCESSING-CHARACTER-COMPLEXITY",
        )
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("character_shift_complexity", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_schur_filtration_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-SCHUR-FILTRATION")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-SCHUR-FILTRATION-SCHUR-FILTRATION")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_schur_filtration", record["artifacts"])
        self.assertTrue(validation["valid"])

    def test_code_closure_conductor_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-CLOSURE-CONDUCTOR-ATTACK")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-CLOSURE-CONDUCTOR-ATTACK-CLOSURE-CONDUCTOR")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_closure_attack", record["artifacts"])
        self.assertEqual(record["metrics"]["ambient_recovery_calibration_count"], 1)
        self.assertTrue(validation["valid"])

    def test_phase_naturalness_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-PHASE-NATURALNESS")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-PHASE-NATURALNESS-PHASE-NATURALNESS")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("phase_family_naturalness", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_trace_function_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-TRACE-FUNCTION-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-TRACE-FUNCTION-SEARCH-TRACE-FUNCTION-SEARCH")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("trace_function_search", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_run_all_supported_uses_available_seed_experiments(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                results = run_supported_experiments()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(set(result.experiment_id for result in results).issubset(set(supported_experiment_ids())))
        self.assertGreaterEqual(len(results), 2)

    def test_run_next_selects_supported_experiment_and_writes_trends(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                selection = select_next_experiment()
                selection_after_run, result = run_next_experiment()
                trend_report = write_experiment_trends()
                history_text = Path("research/experiment_run_history.json").read_text()
            finally:
                os.chdir(old_cwd)

        self.assertIn(selection.experiment_id, supported_experiment_ids())
        self.assertEqual(selection_after_run.experiment_id, selection.experiment_id)
        self.assertEqual(result.status, "completed")
        self.assertIn(result.result_id, history_text)
        self.assertGreaterEqual(trend_report["history_count"], 1)
        self.assertTrue(any(item["experiment_id"] == result.experiment_id for item in trend_report["trends"]))

    def test_run_next_uses_frontier_and_blocker_pressure_over_stale_history(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text('{"top_frontier": "code-equivalence-hard-family-search"}')
                Path("research/blocker_taxonomy.json").write_text('{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}')
                selection = select_next_experiment()
            finally:
                os.chdir(old_cwd)

            self.assertEqual(selection.experiment_id, "EXP-CODE-CLOSURE-CONDUCTOR-ATTACK")
        self.assertIn("top frontier", selection.reason)

    def test_run_next_honors_status_specific_wreath_frontier(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text(
                    """{
  "top_frontier": "code-equivalence-hard-family-search",
  "frontiers": [
    {
      "frontier_id": "code-equivalence-hard-family-search",
      "status": "self-dual-wreath-growing-copy-covariant-decoder"
    }
  ]
}"""
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(
            selection.experiment_id,
            "EXP-CODE-SELF-DUAL-WREATH-HECKE-AUDIT",
        )
        self.assertIn("wreath Hecke audit", selection.reason)

    def test_run_next_honors_character_frontier_over_stale_code_blocker(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text('{"top_frontier": "character-shift-decoding-lower-bound"}')
                Path("research/blocker_taxonomy.json").write_text('{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}')
                selection = select_next_experiment()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(selection.experiment_id, "EXP-DHS-CHARACTER-COMPLEXITY-PREPROCESSING")
        self.assertIn("hidden-shift decoding", selection.reason)

    def test_run_next_routes_density_one_frontier_only_to_subset_sum_family(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text(
                    '{"top_frontier": "dcp-density-one-subset-sum-partial-solver"}'
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(
            selection.experiment_id,
            "EXP-DHS-DCP-SUBSET-SUM-EMBEDDING-VOLUME-THEOREM",
        )
        self.assertIn("density-one partial subset-sum", selection.reason)

    def test_run_next_rotates_supported_falsifier_reruns(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text('{"top_frontier": "code-equivalence-hard-family-search"}')
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                save_experiments(
                    [
                        {
                            "id": "EXP-CODE-INFORMATION-SET-CANONICALIZATION",
                            "candidate_id": "CODE-COSET-COLLECTIVE",
                            "title": "Code information-set canonicalization",
                            "status": "active",
                            "hypothesis": "Code equivalence candidates should survive canonicalization attacks.",
                            "protocol": "Run code canonicalization by information sets.",
                            "dependencies": [],
                            "metrics": ["code", "canonicalization"],
                            "falsifiers": ["Classical information-set rejection."],
                        },
                        {
                            "id": "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
                            "candidate_id": "CODE-COSET-COLLECTIVE",
                            "title": "Code quasi-cyclic automorphism canonicalization",
                            "status": "active",
                            "hypothesis": "Quasi-cyclic code families should survive automorphism canonicalization.",
                            "protocol": "Run code automorphism canonicalization.",
                            "dependencies": [],
                            "metrics": ["code", "automorphism", "canonicalization"],
                            "falsifiers": ["Classical automorphism canonicalization rejection."],
                        },
                    ]
                )
                Path("research/experiment_run_history.json").write_text(
                    """[
  {
    "recorded_at": "2026-01-01T00:00:00Z",
    "experiment_id": "EXP-CODE-INFORMATION-SET-CANONICALIZATION",
    "result_id": "RESULT-INFO-1",
    "candidate_id": "CODE-COSET-COLLECTIVE",
    "status": "completed",
    "summary": "falsified",
    "metrics": {},
    "falsifier_count": 1,
    "falsifiers_triggered": ["Classical information-set rejection."]
  },
  {
    "recorded_at": "2026-01-01T00:00:01Z",
    "experiment_id": "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
    "result_id": "RESULT-QC-1",
    "candidate_id": "CODE-COSET-COLLECTIVE",
    "status": "completed",
    "summary": "falsified",
    "metrics": {},
    "falsifier_count": 1,
    "falsifiers_triggered": ["Classical automorphism canonicalization rejection."]
  },
  {
    "recorded_at": "2026-01-01T00:00:02Z",
    "experiment_id": "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
    "result_id": "RESULT-QC-2",
    "candidate_id": "CODE-COSET-COLLECTIVE",
    "status": "completed",
    "summary": "falsified again",
    "metrics": {},
    "falsifier_count": 1,
    "falsifiers_triggered": ["Classical automorphism canonicalization rejection."]
  }
]"""
                )
                selection = select_next_experiment()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(selection.experiment_id, "EXP-CODE-INFORMATION-SET-CANONICALIZATION")
        self.assertIn("rerun rotation penalty=8", selection.reason)

    def test_run_next_avoids_immediate_repeat_when_peer_falsifier_exists(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text('{"top_frontier": "code-equivalence-hard-family-search"}')
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                save_experiments(
                    [
                        {
                            "id": "EXP-CODE-INFORMATION-SET-CANONICALIZATION",
                            "candidate_id": "CODE-COSET-COLLECTIVE",
                            "title": "Code information-set canonicalization",
                            "status": "active",
                            "hypothesis": "Code equivalence candidates should survive canonicalization attacks.",
                            "protocol": "Run code canonicalization by information sets.",
                            "dependencies": [],
                            "metrics": ["code", "canonicalization"],
                            "falsifiers": ["Classical information-set rejection."],
                        },
                        {
                            "id": "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
                            "candidate_id": "CODE-COSET-COLLECTIVE",
                            "title": "Code quasi-cyclic automorphism canonicalization",
                            "status": "active",
                            "hypothesis": "Quasi-cyclic code families should survive automorphism canonicalization.",
                            "protocol": "Run code automorphism canonicalization.",
                            "dependencies": [],
                            "metrics": ["code", "automorphism", "canonicalization"],
                            "falsifiers": ["Classical automorphism canonicalization rejection."],
                        },
                    ]
                )
                Path("research/experiment_run_history.json").write_text(
                    """[
  {
    "recorded_at": "2026-01-01T00:00:00Z",
    "experiment_id": "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
    "result_id": "RESULT-QC-1",
    "candidate_id": "CODE-COSET-COLLECTIVE",
    "status": "completed",
    "summary": "falsified",
    "metrics": {},
    "falsifier_count": 1,
    "falsifiers_triggered": ["Classical automorphism canonicalization rejection."]
  },
  {
    "recorded_at": "2026-01-01T00:00:01Z",
    "experiment_id": "EXP-CODE-INFORMATION-SET-CANONICALIZATION",
    "result_id": "RESULT-INFO-1",
    "candidate_id": "CODE-COSET-COLLECTIVE",
    "status": "completed",
    "summary": "falsified",
    "metrics": {},
    "falsifier_count": 1,
    "falsifiers_triggered": ["Classical information-set rejection."]
  }
]"""
                )
                selection = select_next_experiment()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(selection.experiment_id, "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION")
        self.assertIn("recent-run freshness penalty=30", selection.reason)

    def test_run_next_tolerates_transient_malformed_derived_artifacts(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text("")
                Path("research/blocker_taxonomy.json").write_text("{")
                selection = select_next_experiment()
            finally:
                os.chdir(old_cwd)

        self.assertIn(selection.experiment_id, supported_experiment_ids())
        self.assertNotIn("top frontier", selection.reason)

    def test_state_native_mutation_does_not_create_learnability_experiment(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-DHS-GOWERS-SPECTRUM")
                write_dequantization_report()
                write_conjecture_report()
                write_mutation_report()
                experiment_id = "EXP-MUT-DHS-GOWERS-SIEVE-LEARNABILITY"
                experiment_ids = {item["id"] for item in load_experiments()}
                mutation_types = {item["mutation_type"] for item in load_mutation_proposals()}
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertNotIn(experiment_id, experiment_ids)
        self.assertIn("dcp-recursive-decoder-certificate", mutation_types)
        self.assertNotIn("learnability-resistant-hidden-shift", mutation_types)
        self.assertTrue(validation["valid"])

    def test_code_low_weight_matroid_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-LOW-WEIGHT-MATROID-BASELINE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-LOW-WEIGHT-MATROID-BASELINE-LOW-WEIGHT-MATROID")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_low_weight_structure", record["artifacts"])
        self.assertTrue(validation["valid"])

    def test_state_native_mutation_does_not_create_phase_fourier_experiment(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-DHS-GOWERS-SPECTRUM")
                write_dequantization_report()
                write_conjecture_report()
                write_mutation_report()
                experiment_id = "EXP-MUT-DHS-GOWERS-SIEVE-FOURIER-COMPRESSIBILITY"
                experiment_ids = {item["id"] for item in load_experiments()}
                hidden_mutation_ids = {
                    item["id"]
                    for item in load_candidates()
                    if item["id"].startswith("MUT-CAND-DHS-GOWERS-SIEVE")
                }
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertNotIn(experiment_id, experiment_ids)
        self.assertFalse(hidden_mutation_ids)
        self.assertTrue(validation["valid"])

    def test_wreath_component_defect_gap_bridge_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-GAP-BRIDGE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_defect_gap_bridge",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_component_povm_regular_master_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-REGULAR-MASTER-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_povm_regular_master_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_component_povm_sparse_support_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPARSE-SUPPORT-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_povm_sparse_support_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_covariant_pgm_factorization_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COVARIANT-PGM-FACTORIZATION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_covariant_pgm_factorization",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_coverage_welch_pressure_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COVERAGE-WELCH-PRESSURE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_coverage_welch_pressure",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_cross_dependency_neutrality_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-CROSS-DEPENDENCY-NEUTRALITY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_cross_dependency_neutrality",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_dependency_homology_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-DEPENDENCY-HOMOLOGY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_dependency_homology",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_early_level_overlap_localization_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-EARLY-LEVEL-OVERLAP-LOCALIZATION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_early_level_overlap_localization",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_extended_kronecker_threshold_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-EXTENDED-KRONECKER-THRESHOLD"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_extended_kronecker_threshold",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_final_root_leverage_edge_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-LEVERAGE-EDGE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_final_root_leverage_edge",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_component_defect_rank_mass_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-RANK-MASS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_defect_rank_mass",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_component_effect_algebra_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-EFFECT-ALGEBRA-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_effect_algebra_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_component_povm_spectral_trim_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPECTRAL-TRIM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_povm_spectral_trim",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_final_root_natural_common_span_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-NATURAL-COMMON-SPAN"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_final_root_natural_common_span",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_fixed_family_common_rank_dilution_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-FIXED-FAMILY-COMMON-RANK-DILUTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_fixed_family_common_rank_dilution",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_global_carrier_channel_extractor_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-CARRIER-CHANNEL-EXTRACTOR"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_global_carrier_channel_extractor",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_global_collision_free_mass_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-COLLISION-FREE-MASS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_global_collision_free_mass",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_global_distinct_joint_kernel_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-DISTINCT-JOINT-KERNEL"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_global_distinct_joint_kernel",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_global_partition_collision_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-PARTITION-COLLISION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_global_partition_collision",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_gpe_holonomy_resolver_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-GPE-HOLONOMY-RESOLVER-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_gpe_holonomy_resolver_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_gpe_pair_polar_transport_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-GPE-PAIR-POLAR-TRANSPORT"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_gpe_pair_polar_transport",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_gpe_recursive_node_compiler_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-GPE-RECURSIVE-NODE-COMPILER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_gpe_recursive_node_compiler",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_graded_channel_graph_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-GRADED-CHANNEL-GRAPH-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_graded_channel_graph_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_graded_flat_transport_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-GRADED-FLAT-TRANSPORT-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_graded_flat_transport_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_graded_frobenius_trim_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-GRADED-FROBENIUS-TRIM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_graded_frobenius_trim",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_hamming_stratum_rank_transition_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-HAMMING-STRATUM-RANK-TRANSITION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_hamming_stratum_rank_transition",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_hierarchical_cokernel_resolution_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-COKERNEL-RESOLUTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_hierarchical_cokernel_resolution",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_hierarchical_polar_tree_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-POLAR-TREE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_hierarchical_polar_tree",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_hierarchy_low_carrier_trim_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-LOW-CARRIER-TRIM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_hierarchy_low_carrier_trim",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_hierarchy_pair_common_rank_budget_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-PAIR-COMMON-RANK-BUDGET"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_hierarchy_pair_common_rank_budget",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_internal_closure_graded_rescue_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-INTERNAL-CLOSURE-GRADED-RESCUE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_internal_closure_graded_rescue",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_interplane_gauge_homology_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-INTERPLANE-GAUGE-HOMOLOGY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_interplane_gauge_homology",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_invariant_projector_circuit_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-INVARIANT-PROJECTOR-CIRCUIT"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_invariant_projector_circuit",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_isotypic_dephasing_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ISOTYPIC-DEPHASING-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_isotypic_dephasing_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_leaf_whitening_commutator_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-LEAF-WHITENING-COMMUTATOR-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_leaf_whitening_commutator_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_level_three_flag_audit_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-LEVEL-THREE-FLAG-AUDIT"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_level_three_flag_audit",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_local_pair_transversality_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-LOCAL-PAIR-TRANSVERSALITY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_local_pair_transversality",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_matrix_cayley_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-MATRIX-CAYLEY-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_matrix_cayley_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_matrix_povm_recursive_compiler_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-MATRIX-POVM-RECURSIVE-COMPILER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_matrix_povm_recursive_compiler",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_mixed_covariant_decoder_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-MIXED-COVARIANT-DECODER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_mixed_covariant_decoder",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_common_span_component_universality_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMMON-SPAN-COMPONENT-UNIVERSALITY-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_common_span_component_universality_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_mrs_coherence_escape_criterion_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-MRS-COHERENCE-ESCAPE-CRITERION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_mrs_coherence_escape_criterion",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_mrs_transcript_povm_separation_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-MRS-TRANSCRIPT-POVM-SEPARATION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_mrs_transcript_povm_separation",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_multiscale_polar_schedule_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-MULTISCALE-POLAR-SCHEDULE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_multiscale_polar_schedule",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_native_frame_access_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-NATIVE-FRAME-ACCESS-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_native_frame_access_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_natural_leaf_commutator_mass_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-MASS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_natural_leaf_commutator_mass",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_natural_pair_carrier_law_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-NATURAL-PAIR-CARRIER-LAW"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_natural_pair_carrier_law",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_operator_steiner_bulk_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-OPERATOR-STEINER-BULK-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_operator_steiner_bulk_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_orientation_filter_physical_access_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FILTER-PHYSICAL-ACCESS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_orientation_filter_physical_access",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_orientation_rank_budget_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RANK-BUDGET"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_orientation_rank_budget",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_orientation_retention_theorem_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RETENTION-THEOREM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_orientation_retention_theorem",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_orientation_subspace_filter_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-SUBSPACE-FILTER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_orientation_subspace_filter",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_pair_common_covering_transition_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PAIR-COMMON-COVERING-TRANSITION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pair_common_covering_transition",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_pair_core_rank_concentration_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RANK-CONCENTRATION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pair_core_rank_concentration",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_pair_polar_sampler_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-SAMPLER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pair_polar_sampler",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_pair_polar_transport_network_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-TRANSPORT-NETWORK"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pair_polar_transport_network",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_pair_transport_degree_obstruction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-DEGREE-OBSTRUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pair_transport_degree_obstruction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_pair_transport_native_mass_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-NATIVE-MASS-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pair_transport_native_mass_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_partial_support_child_embedding_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-CHILD-EMBEDDING"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_partial_support_child_embedding",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_partial_support_source_mass_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-SOURCE-MASS-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_partial_support_source_mass_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_boolean_graph_stopping_core_pressure_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-BOOLEAN-GRAPH-STOPPING-CORE-PRESSURE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_boolean_graph_stopping_core_pressure",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_component_aggregate_frame_indeterminacy_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-AGGREGATE-FRAME-INDETERMINACY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_aggregate_frame_indeterminacy",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_component_commutator_collision_free_transfer_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-COLLISION-FREE-TRANSFER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_commutator_collision_free_transfer",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_component_commutator_haar_benchmark_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-HAAR-BENCHMARK"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_commutator_haar_benchmark",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_component_commutator_trace_mass_bridge_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-TRACE-MASS-BRIDGE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_commutator_trace_mass_bridge",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_component_green_ridge_stability_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-GREEN-RIDGE-STABILITY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_green_ridge_stability",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_component_hamming_orbit_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-HAMMING-ORBIT-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_hamming_orbit_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_component_leaf_resolved_green_normal_form_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-RESOLVED-GREEN-NORMAL-FORM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_leaf_resolved_green_normal_form",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_contiguous_all_a_support_pressure_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-ALL-A-SUPPORT-PRESSURE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_contiguous_all_a_support_pressure",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_contiguous_frame_target_factorization_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-FRAME-TARGET-FACTORIZATION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_contiguous_frame_target_factorization",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_exceptional_block_graph_core_pressure_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-EXCEPTIONAL-BLOCK-GRAPH-CORE-PRESSURE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_exceptional_block_graph_core_pressure",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_frame_subword_entropy_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-FRAME-SUBWORD-ENTROPY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_frame_subword_entropy",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_leaf_marked_green_word_normal_form_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-LEAF-MARKED-GREEN-WORD-NORMAL-FORM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_leaf_marked_green_word_normal_form",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_linear_code_support_pressure_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-LINEAR-CODE-SUPPORT-PRESSURE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_linear_code_support_pressure",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_marked_pressure_obstruction_search_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-MARKED-PRESSURE-OBSTRUCTION-SEARCH"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_marked_pressure_obstruction_search",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_marked_relation_topology_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-MARKED-RELATION-TOPOLOGY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_marked_relation_topology",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_mixed_split_target_genus_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-MIXED-SPLIT-TARGET-GENUS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_mixed_split_target_genus",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_natural_leaf_commutator_trace_profile_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-TRACE-PROFILE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_natural_leaf_commutator_trace_profile",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_parity_stopping_core_pressure_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PARITY-STOPPING-CORE-PRESSURE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_parity_stopping_core_pressure",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_periodic_frame_fiber_counterfamily_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-FIBER-COUNTERFAMILY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_periodic_frame_fiber_counterfamily",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_high_codimension_face_word_frontier_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-HIGH-CODIMENSION-FACE-WORD-FRONTIER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_high_codimension_face_word_frontier",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_periodic_frame_rank_collapse_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-RANK-COLLAPSE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_periodic_frame_rank_collapse",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_petz_pgm_obstruction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PETZ-PGM-OBSTRUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_petz_pgm_obstruction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_pgm_quantum_sampling_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PGM-QUANTUM-SAMPLING-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pgm_quantum_sampling_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_pgm_spectral_window_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PGM-SPECTRAL-WINDOW"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pgm_spectral_window",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_pgm_success_theorem_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PGM-SUCCESS-THEOREM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pgm_success_theorem",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_pgm_truncation_robustness_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PGM-TRUNCATION-ROBUSTNESS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pgm_truncation_robustness",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_physical_orientation_interference_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ORIENTATION-INTERFERENCE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_physical_orientation_interference",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_physical_pgm_intertwiner_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-PGM-INTERTWINER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_physical_pgm_intertwiner",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_plancherel_kronecker_positivity_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-KRONECKER-POSITIVITY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_plancherel_kronecker_positivity",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_polar_factor_transfer_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-POLAR-FACTOR-TRANSFER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_polar_factor_transfer",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_postfilter_frame_compression_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-POSTFILTER-FRAME-COMPRESSION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_postfilter_frame_compression",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_random_steiner_gauge_edge_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-RANDOM-STEINER-GAUGE-EDGE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_random_steiner_gauge_edge",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_reciprocal_carrier_accumulation_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-RECIPROCAL-CARRIER-ACCUMULATION-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_reciprocal_carrier_accumulation_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_regular_master_central_support_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-REGULAR-MASTER-CENTRAL-SUPPORT"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_regular_master_central_support",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_relation_cokernel_transfer_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-RELATION-COKERNEL-TRANSFER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_relation_cokernel_transfer",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_relative_effect_intersection_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-EFFECT-INTERSECTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_relative_effect_intersection",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_relative_surface_factorization_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-SURFACE-FACTORIZATION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_relative_surface_factorization",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_residual_frobenius_typicality_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-RESIDUAL-FROBENIUS-TYPICALITY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_residual_frobenius_typicality",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_sector_weight_concentration_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SECTOR-WEIGHT-CONCENTRATION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_sector_weight_concentration",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_shorted_overlap_balance_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SHORTED-OVERLAP-BALANCE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_shorted_overlap_balance",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_sibling_frame_jacobi_surrogate_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JACOBI-SURROGATE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_sibling_frame_jacobi_surrogate",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_sibling_frame_joint_conditioning_surrogate_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-CONDITIONING-SURROGATE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_sibling_frame_joint_conditioning_surrogate",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_sibling_frame_joint_freeness_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-FREENESS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_sibling_frame_joint_freeness",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_sibling_frame_mp_moments_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-MP-MOMENTS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_sibling_frame_mp_moments",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_sibling_word_map_normal_form_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-WORD-MAP-NORMAL-FORM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_sibling_word_map_normal_form",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_signed_steiner_bulk_edge_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-BULK-EDGE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_signed_steiner_bulk_edge",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_signed_steiner_incidence_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-INCIDENCE-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_signed_steiner_incidence_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_signed_steiner_nullity_theorem_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-NULLITY-THEOREM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_signed_steiner_nullity_theorem",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_single_anchor_shorting_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SINGLE-ANCHOR-SHORTING"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_single_anchor_shorting",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_sparse_invariant_dependency_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SPARSE-INVARIANT-DEPENDENCY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_sparse_invariant_dependency",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_star_channel_mass_typicality_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-STAR-CHANNEL-MASS-TYPICALITY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_star_channel_mass_typicality",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_subgroup_pair_angle_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PAIR-ANGLE-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_subgroup_pair_angle_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_subgroup_projection_walk_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PROJECTION-WALK"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_subgroup_projection_walk",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_support_affine_rank_entropy_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-AFFINE-RANK-ENTROPY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_support_affine_rank_entropy",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_support_difference_peeling_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-DIFFERENCE-PEELING-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_support_difference_peeling_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_target_survival_surface_seed_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-TARGET-SURVIVAL-SURFACE-SEED"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_target_survival_surface_seed",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_trace_polynomial_edge_burden_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-TRACE-POLYNOMIAL-EDGE-BURDEN"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_trace_polynomial_edge_burden",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_trace_weighted_pgm_bridge_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-PGM-BRIDGE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_trace_weighted_pgm_bridge",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_trace_weighted_polar_truncation_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-POLAR-TRUNCATION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_trace_weighted_polar_truncation",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_transport_carrier_mass_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-TRANSPORT-CARRIER-MASS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_transport_carrier_mass",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_two_color_return_walk_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-TWO-COLOR-RETURN-WALK"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_two_color_return_walk",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_two_partition_ribbon_surface_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-TWO-PARTITION-RIBBON-SURFACE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_two_partition_ribbon_surface",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_uniform_orientation_rank_concentration_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-UNIFORM-ORIENTATION-RANK-CONCENTRATION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_uniform_orientation_rank_concentration",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_vertex_channel_groupoid_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-VERTEX-CHANNEL-GROUPOID"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_vertex_channel_groupoid",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_vertex_kernel_graded_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-VERTEX-KERNEL-GRADED-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_vertex_kernel_graded_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_vertex_trivialization_criterion_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-VERTEX-TRIVIALIZATION-CRITERION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_vertex_trivialization_criterion",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_weighted_overlap_exclusion_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-WEIGHTED-OVERLAP-EXCLUSION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_weighted_overlap_exclusion",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_repeated_runs_create_append_only_history(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-DHS-GOWERS-SPECTRUM")
                run_experiment("EXP-DHS-GOWERS-SPECTRUM")
                trend_report = write_experiment_trends()
            finally:
                os.chdir(old_cwd)

        trend = next(item for item in trend_report["trends"] if item["experiment_id"] == "EXP-DHS-GOWERS-SPECTRUM")
        self.assertEqual(trend["run_count"], 2)
        self.assertEqual(trend["status_sequence"], ["needs-theory", "needs-theory"])

    def test_wreath_all_unequal_third_moment_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-THIRD-MOMENT"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_all_unequal_third_moment",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_carrier_orbit_growth_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_carrier_orbit_growth",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_character_moments_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-MOMENTS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_character_moments",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_commutant_transfer_audit_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMMUTANT-TRANSFER-AUDIT"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_commutant_transfer_audit",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_complete_w3_tuples_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLES"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_complete_w3_tuple_audit",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_equal_commutator_audit_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-EQUAL-COMMUTATOR-AUDIT"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_equal_commutator_audit",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_harmonic_carrier_schema_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_harmonic_carrier_schema",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_pgm_polar_audit_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PGM-POLAR-AUDIT"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_pgm_polar_audit",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_physical_frame_blocks_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCKS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_physical_frame_blocks",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_spectrum_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SPECTRUM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_spectrum",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_stable_commutator_rank_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-STABLE-COMMUTATOR-RANK"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_stable_commutator_rank",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_subset_carrier_algebra_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SUBSET-CARRIER-ALGEBRA"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_subset_carrier_algebra",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_third_moment_contraction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-THIRD-MOMENT-CONTRACTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_third_moment_contraction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_typical_partition_portfolio_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-PARTITION-PORTFOLIO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_typical_partition_portfolio",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_typical_recoupling_transfer_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-RECOUPLING-TRANSFER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_typical_recoupling_transfer",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_wreath_unequal_frame_blocks_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-UNEQUAL-FRAME-BLOCKS"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_unequal_frame_blocks",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])


    def test_coset_arbitrary_covariant_measurement_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-ARBITRARY-COVARIANT-MEASUREMENT-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_arbitrary_covariant_measurement_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_centralizer_whitening_rank_bound_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-CENTRALIZER-WHITENING-RANK-BOUND"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_centralizer_whitening_rank_bound",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_covariant_measurement_multiplicity_width_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-COVARIANT-MEASUREMENT-MULTIPLICITY-WIDTH-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_covariant_measurement_multiplicity_width_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_covariant_multiplicity_whitening_escape_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-COVARIANT-MULTIPLICITY-WHITENING-ESCAPE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_covariant_multiplicity_whitening_escape",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_gelfand_row_orientation_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-GELFAND-ROW-ORIENTATION-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_gelfand_row_orientation_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_hidden_involution_binary_decision_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-HIDDEN-INVOLUTION-BINARY-DECISION-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_hidden_involution_binary_decision_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_hidden_involution_fourth_moment_threshold_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-HIDDEN-INVOLUTION-FOURTH-MOMENT-THRESHOLD"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_hidden_involution_fourth_moment_threshold",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_hidden_involution_multiplicity_support_obstruction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-SUPPORT-OBSTRUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_hidden_involution_multiplicity_support_obstruction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_hidden_involution_orbit_hull_twirl_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-HIDDEN-INVOLUTION-ORBIT-HULL-TWIRL-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_hidden_involution_orbit_hull_twirl_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_hidden_involution_query_separation_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-HIDDEN-INVOLUTION-QUERY-SEPARATION-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_hidden_involution_query_separation_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_hidden_involution_support_span_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-SPAN-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_hidden_involution_support_span_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])


    def test_coset_hidden_involution_threshold_compiler_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-HIDDEN-INVOLUTION-THRESHOLD-COMPILER-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_hidden_involution_threshold_compiler_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_hyperoctahedral_branching_polar_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-HYPEROCTAHEDRAL-BRANCHING-POLAR-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_hyperoctahedral_branching_polar_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_kronecker_marginal_conservation_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-KRONECKER-MARGINAL-CONSERVATION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_kronecker_marginal_conservation",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_measurement_copy_width_whitening_tradeoff_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-MEASUREMENT-COPY-WIDTH-WHITENING-TRADEOFF"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_measurement_copy_width_whitening_tradeoff",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_multiplicity_whitening_copy_window_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-MULTIPLICITY-WHITENING-COPY-WINDOW"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_multiplicity_whitening_copy_window",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_perfect_matching_spherical_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-PERFECT-MATCHING-SPHERICAL-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_perfect_matching_spherical_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_prefix_polar_holonomy_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-PREFIX-POLAR-HOLONOMY-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_prefix_polar_holonomy_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_prefix_relative_gap_inference_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-PREFIX-RELATIVE-GAP-INFERENCE-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_prefix_relative_gap_inference_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_restriction_principal_angle_polar_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-RESTRICTION-PRINCIPAL-ANGLE-POLAR-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_restriction_principal_angle_polar_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_sector_coherence_degree_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-SECTOR-COHERENCE-DEGREE-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_sector_coherence_degree_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_coset_source_weighted_frame_inversion_tradeoff_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-SOURCE-WEIGHTED-FRAME-INVERSION-TRADEOFF"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_source_weighted_frame_inversion_tradeoff",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])


    def test_coset_whitening_rank_sandwich_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-COSET-WHITENING-RANK-SANDWICH-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "coset_whitening_rank_sandwich_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_adaptive_layout_uniform_entanglement_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-ADAPTIVE-LAYOUT-UNIFORM-ENTANGLEMENT-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_adaptive_layout_uniform_entanglement_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_arbitrary_measurement_witness_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-ARBITRARY-MEASUREMENT-WITNESS-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_arbitrary_measurement_witness_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_canonical_pgm_erasure_equivalence_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-CANONICAL-PGM-ERASURE-EQUIVALENCE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_canonical_pgm_erasure_equivalence",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_covariant_rank_one_measurement_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-COVARIANT-RANK-ONE-MEASUREMENT-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_covariant_rank_one_measurement_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_four_block_ksum_noncollapse_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-FOUR-BLOCK-KSUM-NONCOLLAPSE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_four_block_ksum_noncollapse",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_linear_depth_fiber_walk_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-LINEAR-DEPTH-FIBER-WALK-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_linear_depth_fiber_walk_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_low_bit_candidate_list_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-LOW-BIT-CANDIDATE-LIST-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_low_bit_candidate_list_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_multiplicity_oracle_query_lower_bound_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-MULTIPLICITY-ORACLE-QUERY-LOWER-BOUND"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_multiplicity_oracle_query_lower_bound",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_per_target_stratum_obstruction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-PER-TARGET-STRATUM-OBSTRUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_per_target_stratum_obstruction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_pgm_bootstrap_perturbation_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-PGM-BOOTSTRAP-PERTURBATION-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_pgm_bootstrap_perturbation_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])


    def test_dcp_pgm_garbage_bootstrap_reduction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-PGM-GARBAGE-BOOTSTRAP-REDUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_pgm_garbage_bootstrap_reduction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_polynomial_feature_contraction_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-POLYNOMIAL-FEATURE-CONTRACTION-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_polynomial_feature_contraction_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_source_weighted_inversion_tradeoff_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-SOURCE-WEIGHTED-INVERSION-TRADEOFF"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_source_weighted_inversion_tradeoff",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_cube_section_gap_theorem_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-SUBSET-SUM-CUBE-SECTION-GAP-THEOREM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_subset_sum_cube_section_gap_theorem",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_sparse_character_obstruction_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-SUBSET-SUM-ADAPTIVE-SPARSE-CHARACTER-OBSTRUCTION"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_subset_sum_sparse_character_obstruction",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_uniform_legal_multiplicity_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-UNIFORM-LEGAL-MULTIPLICITY-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_uniform_legal_multiplicity_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_varying_hms_fiber_normal_form_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DHS-DCP-VARYING-HMS-FIBER-NORMAL-FORM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "dcp_varying_hms_fiber_normal_form",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_diagram_hidden_subalgebra_coset_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DIAGRAM-HIDDEN-SUBALGEBRA-COSET-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "diagram_hidden_subalgebra_coset_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_diagram_multiplicity_source_mass_gate_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-DIAGRAM-MULTIPLICITY-SOURCE-MASS-GATE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "diagram_multiplicity_source_mass_gate",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_all_codimension_baba_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-ALL-CODIMENSION-BABA-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_all_codimension_baba_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_class_uniform_commutator_moment_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-CLASS-UNIFORM-COMMUTATOR-MOMENT"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_class_uniform_commutator_moment",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])


    def test_self_dual_wreath_codimension_one_commuting_compression_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-CODIMENSION-ONE-COMMUTING-COMPRESSION-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_codimension_one_commuting_compression_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_codimension_two_universal_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-CODIMENSION-TWO-UNIVERSAL-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_codimension_two_universal_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_commutator_sector_filter_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMMUTATOR-SECTOR-FILTER-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_commutator_sector_filter_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_component_block_coherence_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-BLOCK-COHERENCE-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_block_coherence_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_component_coefficient_projection_normal_form_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COEFFICIENT-PROJECTION-NORMAL-FORM"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_coefficient_projection_normal_form",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_component_noncrossing_lower_bound_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-NONCROSSING-LOWER-BOUND"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_component_noncrossing_lower_bound",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_full_support_pair_budget_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-FULL-SUPPORT-PAIR-BUDGET-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_full_support_pair_budget_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_information_set_universal_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-INFORMATION-SET-UNIVERSAL-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_information_set_universal_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_interleaved_even_parity_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-EVEN-PARITY-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_interleaved_even_parity_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_interleaved_leaf_pressure_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-LEAF-PRESSURE-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_interleaved_leaf_pressure_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_interleaved_product_lift_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-PRODUCT-LIFT-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_interleaved_product_lift_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])


    def test_self_dual_wreath_nonsystematic_incidence_lattice_bound_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-INCIDENCE-LATTICE-BOUND"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_nonsystematic_incidence_lattice_bound",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_nonsystematic_mod_four_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-MOD-FOUR-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_nonsystematic_mod_four_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_nonsystematic_pair_witness_collapse_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-PAIR-WITNESS-COLLAPSE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_nonsystematic_pair_witness_collapse",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_nonsystematic_twisted_star_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-TWISTED-STAR-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_nonsystematic_twisted_star_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_plancherel_target_word_collapse_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-TARGET-WORD-COLLAPSE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_plancherel_target_word_collapse",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_poisson_ridge_word_mixture_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-POISSON-RIDGE-WORD-MIXTURE"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_poisson_ridge_word_mixture",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_same_support_triangle_target_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SAME-SUPPORT-TRIANGLE-TARGET-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_same_support_triangle_target_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_separator_defect_frontier_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SEPARATOR-DEFECT-FRONTIER"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_separator_defect_frontier",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_systematic_stopping_core_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-SYSTEMATIC-STOPPING-CORE-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_systematic_stopping_core_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_self_dual_wreath_translated_parity_commutator_no_go_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-TRANSLATED-PARITY-COMMUTATOR-NO-GO"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_translated_parity_commutator_no_go",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_semidirect_hms_transfer_boundary_dispatches_from_clean_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-SEMIDIRECT-HMS-TRANSFER-BOUNDARY"
                )
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(
            item for item in records if item["id"] == result.result_id
        )
        self.assertIn(
            "semidirect_hms_transfer_boundary",
            record["artifacts"],
        )
        self.assertTrue(validation["valid"], validation["issues"])



if __name__ == "__main__":
    unittest.main()
