import json
import os
import tempfile
import unittest
from pathlib import Path

from blocker_taxonomy import write_blocker_taxonomy
from character_query_information import write_character_query_information_report
from code_equivalence_workbench import write_code_equivalence_workbench
from coset_state_workbench import write_coset_workbench
from phase_family_triage import write_phase_family_triage
from dcp_coherent_matching_interface import write_coherent_matching_interface_audit
from dcp_subset_sum_random_self_reduction import write_random_self_reduction_audit
from dcp_odd_unit_orbit_geometry import write_odd_unit_orbit_geometry_audit
from research_frontier_map import build_frontier_map, write_frontier_map
from research_registry import initialize_seed_registry


class ResearchFrontierMapTests(unittest.TestCase):
    def test_frontier_map_prioritizes_nonabelian_boundary_over_dead_phase_reuse(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_coset_workbench(pair_ids=["cfi-k4-parity-twist", "cfi-k5-parity-twist"])
                write_code_equivalence_workbench(pair_ids=["random-8-4-weak-invariant-collision"])
                write_phase_family_triage()
                write_blocker_taxonomy()
                report = build_frontier_map()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report["top_frontier"], "nonabelian-coset-collective-observables")
        frontier_ids = [item["frontier_id"] for item in report["frontiers"]]
        self.assertIn("hidden-shift-phase-family-generation", frontier_ids)
        hidden = next(item for item in report["frontiers"] if item["frontier_id"] == "hidden-shift-phase-family-generation")
        self.assertEqual(hidden["status"], "abandon-current-family-set")

    def test_write_frontier_map_creates_artifact(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                report = write_frontier_map()
                artifact_exists = Path("research/frontier_map.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(report["id"], "FRONTIER-MAP-LATEST")
        self.assertGreater(report["frontier_count"], 0)

    def test_frontier_map_demotes_coset_when_triage_rejects_every_row(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                Path("research/coset_workbench").mkdir(parents=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/blocker_taxonomy.json").write_text(
                    json.dumps(
                        {
                            "classes": [
                                {"blocker_class": "code-equivalence-invariant-collapse", "priority_score": 15000},
                                {"blocker_class": "coset-classical-invariant-collapse", "priority_score": 7200},
                            ]
                        }
                    )
                )
                Path("research/coset_workbench/coset_frontier_triage.json").write_text(
                    json.dumps(
                        {
                            "headline_metrics": {
                                "record_count": 3,
                                "rejected_pair_count": 3,
                                "proof_debt_pair_count": 0,
                                "survivor_pair_count": 0,
                            }
                        }
                    )
                )
                report = build_frontier_map()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report["top_frontier"], "code-equivalence-hard-family-search")
        coset = next(item for item in report["frontiers"] if item["frontier_id"] == "nonabelian-coset-collective-observables")
        self.assertEqual(coset["status"], "no-current-viable-row-set")
        self.assertIn("Do not design measurements", coset["next_experiment"])

    def test_frontier_map_marks_character_query_route_killed(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_character_query_information_report(n_values=[6])
                report = build_frontier_map()
            finally:
                os.chdir(old_cwd)

        character = next(item for item in report["frontiers"] if item["frontier_id"] == "character-shift-decoding-lower-bound")
        self.assertEqual(character["status"], "decoding-time-only-query-route-killed")
        self.assertIn("Character query-information ceiling", character["evidence"])
        self.assertIn("model-preserving reduction", character["next_experiment"])

    def test_frontier_map_targets_density_one_solver_after_source_bridge(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                Path("research/reductions").mkdir(parents=True)
                Path("research/phase_workbench").mkdir(parents=True)
                Path("research/classical_baselines").mkdir(parents=True)
                Path("research/reductions/dcp_subset_sum_bridge.json").write_text(
                    json.dumps(
                        {
                            "headline_metrics": {
                                "primary_source_conditional_dcp_reduction_count": 1,
                                "proved_polynomial_partial_average_subset_sum_solver_count": 0,
                                "source_contract_satisfying_row_count": 0,
                            }
                        }
                    )
                )
                Path("research/phase_workbench/dcp_contaminated_pgm_audit.json").write_text(
                    json.dumps(
                        {
                            "headline_metrics": {
                                "proved_exact_f1_information_robustness_count": 1,
                                "proved_exact_f1_robust_pgm_circuit_count": 0,
                            }
                        }
                    )
                )
                Path("research/classical_baselines/dcp_subset_sum_lattice_search.json").write_text(
                    json.dumps(
                        {
                            "headline_metrics": {
                                "tail_success_row_count": 1,
                                "tail_row_count": 72,
                                "proved_uniform_inverse_polynomial_coverage_count": 0,
                            }
                        }
                    )
                )
                report = build_frontier_map()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report["top_frontier"], "dcp-density-one-subset-sum-partial-solver")
        dcp = next(
            item
            for item in report["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertEqual(dcp["status"], "source-verified-density-one-partial-solver-open")
        self.assertIn("uniform inverse-polynomial", dcp["next_experiment"])

    def test_frontier_map_treats_seeded_interface_as_resolved_but_quantum_fidelity_as_open(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_coherent_matching_interface_audit(
                    n_values=[16], legal_coverage_exponents=[1], write_registry=False
                )
                report = build_frontier_map()
            finally:
                os.chdir(old_cwd)

        dcp = next(
            item for item in report["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("seeded bridges=1/1", dcp["evidence"])
        self.assertIn("shared-seed randomized solvers are now interface-compatible", dcp["why_it_matters"])
        self.assertIn("paired witness workspaces", dcp["next_experiment"])

    def test_frontier_map_tracks_odd_unit_orbit_as_coverage_not_interface_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_random_self_reduction_audit(
                    n_values=[8], register_offsets=[2], attempt_multiplier=1,
                    trials_per_row=1, write_registry=False
                )
                report = build_frontier_map()
            finally:
                os.chdir(old_cwd)

        dcp = next(
            item for item in report["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Random self-reduction", dcp["evidence"])
        self.assertIn("odd-part easy-orbit certificate", dcp["why_it_matters"])
        self.assertIn("symbolic odd-part", dcp["next_experiment"])

    def test_frontier_map_cuts_blind_odd_unit_sweeps_after_geometry_collapse(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_odd_unit_orbit_geometry_audit(
                    n_values=[8, 10], register_offset=2, base_instances_per_size=2,
                    units_multiplier=1, write_registry=False
                )
                report = build_frontier_map()
            finally:
                os.chdir(old_cwd)

        dcp = next(
            item for item in report["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Odd-unit geometry", dcp["evidence"])
        self.assertIn("Stop blind odd-unit sweeps", dcp["next_experiment"])
        self.assertIn("symbolic odd-part", dcp["next_experiment"])


if __name__ == "__main__":
    unittest.main()
