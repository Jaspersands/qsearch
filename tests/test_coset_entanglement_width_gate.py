import os
import tempfile
import unittest
from pathlib import Path

from coset_entanglement_width_gate import (
    build_entanglement_width_gate_report,
    write_entanglement_width_gate_report,
)
from literature_pipeline import extract_literature_records
from research_registry import load_experiment_results, load_negative_results


class EntanglementWidthGateTests(unittest.TestCase):
    def test_multiregister_literature_is_structured(self):
        records = {
            record.id: record
            for record in extract_literature_records()
        }
        record = records["moore-russell-multiregister-2005"]

        self.assertIn("Omega(n log n)", record.no_go_barrier)
        self.assertIn("Entangled multiregister", record.mechanism)
        self.assertIn("associator", record.open_question)

    def test_all_bounded_mechanisms_are_quarantined(self):
        report = build_entanglement_width_gate_report()

        self.assertEqual(
            report.headline_metrics[
                "bounded_mechanism_end_to_end_information_eligible_count"
            ],
            0,
        )
        self.assertEqual(
            report.headline_metrics["maximum_current_joint_register_count"],
            3,
        )
        self.assertTrue(
            all(
                not mechanism.end_to_end_information_eligible
                for mechanism in report.bounded_register_mechanisms
            )
        )

    def test_gate_requires_growing_entanglement_width(self):
        report = build_entanglement_width_gate_report()

        self.assertTrue(
            report.claim_gate["omega_n_log_n_entanglement_width_required"]
        )
        self.assertFalse(
            report.claim_gate["current_growing_width_architecture_exists"]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_entanglement_width_gate_report(
                    output_path=Path("entanglement-width.json")
                )
                results = load_experiment_results()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(
            any(
                result["experiment_id"]
                == "EXP-COSET-ENTANGLEMENT-WIDTH-GATE"
                for result in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-COSET-BOUNDED-COPY-MECHANISM-AS-GI-DECODER"
                for item in negatives
            )
        )


if __name__ == "__main__":
    unittest.main()
