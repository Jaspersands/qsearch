import json
import os
import tempfile
import unittest
from pathlib import Path

from candidate_quarantine import quarantine_exact_access_invalid_mutations
from research_registry import (
    initialize_seed_registry,
    load_candidates,
    load_experiment_results,
    load_experiments,
    load_negative_results,
    load_rejected_candidates,
    save_candidates,
    save_experiment_results,
    save_experiments,
    validate_registry,
)


class CandidateQuarantineTests(unittest.TestCase):
    def test_exact_access_invalid_mutation_is_moved_out_of_accepted_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                candidates = load_candidates()
                invalid = dict(next(item for item in candidates if item["id"] == "DHS-GOWERS-SIEVE"))
                invalid["id"] = "MUT-CAND-INVALID-EVALUATOR"
                invalid["title"] = "Invalid evaluator mutation"
                invalid["input_model"] = "Coherent oracle and structured evaluator access not supplied by DCP states."
                invalid["experiment_ids"] = ["EXP-MUT-INVALID-EVALUATOR"]
                save_candidates(candidates + [invalid])
                experiments = load_experiments()
                experiments.append(
                    {
                        "id": "EXP-MUT-INVALID-EVALUATOR",
                        "candidate_id": invalid["id"],
                        "title": "Invalid experiment",
                        "status": "planned",
                        "hypothesis": "The invalid access model works.",
                        "protocol": "Use an unavailable evaluator.",
                        "positive_signal": "None.",
                        "falsifiers": ["Exact access audit fails."],
                        "metrics": ["access"],
                        "dependencies": [],
                        "next_actions": ["Quarantine."],
                    }
                )
                save_experiments(experiments)
                save_experiment_results(
                    [
                        {
                            "id": "RESULT-MUT-INVALID",
                            "experiment_id": "EXP-MUT-INVALID-EVALUATOR",
                            "candidate_id": invalid["id"],
                            "created_at": "2026-01-01T00:00:00+00:00",
                            "status": "completed",
                            "summary": "Invalid.",
                            "metrics": {},
                            "falsifiers_triggered": ["Access mismatch."],
                            "artifacts": {},
                        }
                    ]
                )
                audit_path = Path("research/reductions/interface_audit.json")
                audit_path.parent.mkdir(parents=True, exist_ok=True)
                audit_path.write_text(
                    json.dumps(
                        {
                            "audits": [
                                {
                                    "id": "AUDIT-MUT-INVALID",
                                    "route_id": "ROUTE-MUT-INVALID",
                                    "candidate_id": invalid["id"],
                                    "theorem_contract_id": "THM-REGEV-USVP-TO-DCP-2003",
                                    "checks": [
                                        {
                                            "axis": "access-model",
                                            "passed": False,
                                            "burden": "Remove coherent evaluator access.",
                                        }
                                    ],
                                }
                            ]
                        }
                    )
                )

                report = quarantine_exact_access_invalid_mutations()
                remaining_candidate_ids = {item["id"] for item in load_candidates()}
                remaining_experiment_ids = {item["id"] for item in load_experiments()}
                remaining_result_ids = {item["id"] for item in load_experiment_results()}
                rejected_ids = {item["id"] for item in load_rejected_candidates()}
                negative_ids = {item["id"] for item in load_negative_results()}
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report["quarantined_candidate_count"], 1)
        self.assertNotIn(invalid["id"], remaining_candidate_ids)
        self.assertIn("DHS-GOWERS-SIEVE", remaining_candidate_ids)
        self.assertNotIn("EXP-MUT-INVALID-EVALUATOR", remaining_experiment_ids)
        self.assertNotIn("RESULT-MUT-INVALID", remaining_result_ids)
        self.assertIn(invalid["id"], rejected_ids)
        self.assertIn(f"NEG-QUARANTINE-{invalid['id']}", negative_ids)
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
