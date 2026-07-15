import os
import tempfile
import unittest
from pathlib import Path

from coset_state_workbench import (
    audit_graph_pair,
    cfi_parity_graph_complete,
    cfi_parity_graph_k4,
    spectrum_signature,
    wl_k_signature,
    write_coset_workbench,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results


class CosetStateWorkbenchTests(unittest.TestCase):
    def test_shrikhande_rook_pair_survives_3wl_but_not_4wl(self):
        audit = audit_graph_pair("shrikhande-vs-rook")
        self.assertTrue(audit.pair.known_nonisomorphic)
        self.assertEqual(audit.positive_signal, "partial: higher-k WL baseline distinguishes this pair before any quantum observable is needed")
        self.assertFalse(any(item.distinguishes for item in audit.classical_invariants))
        self.assertFalse(any(item.distinguishes for item in audit.relation_observables))
        self.assertTrue(any(item.name == "wl3_tuple_refinement" for item in audit.classical_invariants))
        self.assertFalse(any(item.k <= 3 and item.distinguishes for item in audit.wl_scaling if item.evaluated))
        self.assertTrue(any(item.k == 4 and item.distinguishes for item in audit.wl_scaling if item.evaluated))

    def test_control_pair_is_classically_distinguished(self):
        audit = audit_graph_pair("cycle-vs-chorded-cycle")
        self.assertTrue(any(item.distinguishes for item in audit.classical_invariants))
        self.assertTrue(any(item.name == "wl3_tuple_refinement" and item.distinguishes for item in audit.classical_invariants))
        self.assertTrue(audit.falsifiers_triggered)

    def test_cfi_parity_pair_survives_low_wl_but_has_exact_certificate(self):
        graph_a = cfi_parity_graph_k4(twisted_edge=None)
        graph_b = cfi_parity_graph_k4(twisted_edge=(0, 1))
        self.assertEqual(graph_a.shape, (28, 28))
        self.assertEqual(spectrum_signature(graph_a), spectrum_signature(graph_b))
        self.assertEqual(wl_k_signature(graph_a, k=3), wl_k_signature(graph_b, k=3))

        audit = audit_graph_pair("cfi-k4-parity-twist")
        self.assertTrue(audit.pair.known_nonisomorphic)
        self.assertTrue(audit.positive_signal.startswith("boundary"))
        self.assertFalse(any(item.distinguishes for item in audit.classical_invariants))
        self.assertFalse(any(item.distinguishes for item in audit.relation_observables))
        self.assertFalse(any(item.evaluated and item.distinguishes for item in audit.wl_scaling))
        self.assertTrue(audit.exact_isomorphism_check.supports_known_status)

    def test_scalable_cfi_pair_records_wl_scaling_boundary(self):
        graph_a = cfi_parity_graph_complete(5, twisted_edge=None)
        graph_b = cfi_parity_graph_complete(5, twisted_edge=(0, 1))
        self.assertEqual(graph_a.shape, (60, 60))
        self.assertEqual(spectrum_signature(graph_a), spectrum_signature(graph_b))

        audit = audit_graph_pair("cfi-k5-parity-twist")
        self.assertEqual(audit.pair.vertex_count, 60)
        self.assertTrue(audit.positive_signal.startswith("boundary"))
        self.assertFalse(any(item.distinguishes for item in audit.classical_invariants))
        self.assertFalse(any(item.distinguishes for item in audit.relation_observables))
        self.assertTrue(any(item.name == "wl3_tuple_refinement" and item.signature_a == "skipped" for item in audit.classical_invariants))
        self.assertTrue(any(item.name == "three_register_tuple_relation_colors" and item.value_a == "skipped" for item in audit.relation_observables))
        self.assertTrue(any(item.k == 3 and not item.evaluated for item in audit.wl_scaling))
        self.assertFalse(audit.exact_isomorphism_check.evaluated)

    def test_coset_workbench_writes_artifact_and_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_coset_workbench(pair_ids=["shrikhande-vs-rook"])
                artifact_exists = Path("research/coset_workbench/nonabelian_hsp_audit.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(len(payload["pair_audits"]), 1)
        self.assertIn("wl_scaling", payload["pair_audits"][0])
        self.assertIn("exact_isomorphism_check", payload["pair_audits"][0])
        self.assertTrue(artifact_exists)
        self.assertTrue(any(result["id"] == "RESULT-COSET-WORKBENCH-LATEST" for result in results))
        self.assertFalse(any(item["id"].startswith("COSET-DEQUANTIZED-") for item in negatives))

    def test_coset_workbench_records_scalable_cfi_metrics(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_coset_workbench(pair_ids=["cfi-k5-parity-twist"])
                results = load_experiment_results()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(payload["pair_audits"][0]["pair"]["vertex_count"], 60)
        record = next(item for item in results if item["id"] == "RESULT-COSET-WORKBENCH-LATEST")
        self.assertEqual(record["metrics"]["scalable_cfi_pair_count"], 1)
        self.assertGreaterEqual(record["metrics"]["skipped_wl_scaling_count"], 1)
        self.assertEqual(record["metrics"]["max_vertex_count"], 60)

    def test_coset_workbench_records_negative_result_for_classically_solved_pair(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_coset_workbench(pair_ids=["cycle-vs-chorded-cycle"])
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(payload["pair_audits"][0]["positive_signal"], "control: classical baseline distinguishes this pair")
        self.assertTrue(any(item["id"].startswith("COSET-DEQUANTIZED-") for item in negatives))


if __name__ == "__main__":
    unittest.main()
