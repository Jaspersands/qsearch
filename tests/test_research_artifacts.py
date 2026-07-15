import unittest

from literature_radar import build_literature_index
from problem_ontology import build_problem_ontology
from proof_gate import passes_proof_gate, validate_candidate
from research_lab import build_research_audit
from research_registry import seed_candidate_records


class ResearchArtifactTests(unittest.TestCase):
    def test_problem_ontology_has_no_dangling_relations(self):
        ontology = build_problem_ontology()
        node_ids = {node["id"] for node in ontology["nodes"]}
        for relation in ontology["relations"]:
            self.assertIn(relation["source"], node_ids)
            self.assertIn(relation["target"], node_ids)

    def test_literature_index_contains_no_go_and_hidden_shift_tags(self):
        index = build_literature_index(refresh_arxiv=False)
        self.assertIn("no-go", index["tag_index"])
        self.assertIn("hidden-shift", index["tag_index"])
        self.assertGreaterEqual(len(index["seed_papers"]), 10)

    def test_research_audit_ranks_interventions_by_lift(self):
        audit = build_research_audit(agenda=None, root=None)
        lifts = [item["expected_breakthrough_lift"] for item in audit["ranked_improvements"]]
        self.assertEqual(lifts, sorted(lifts, reverse=True))
        self.assertGreater(lifts[0], 9.0)
        self.assertGreaterEqual(len(audit["proof_obligations"]), 10)

    def test_proof_gate_rejects_toy_oracle_candidate(self):
        candidate = {
            "problem_family": "custom oracle on N<=3 examples",
            "classical_baseline": "brute force",
        }
        issues = validate_candidate(candidate)
        self.assertFalse(passes_proof_gate(candidate))
        self.assertGreaterEqual(len(issues), 10)

    def test_proof_gate_accepts_structural_seed_candidate(self):
        candidates, experiments = seed_candidate_records()
        self.assertGreaterEqual(len(candidates), 2)
        self.assertGreaterEqual(len(experiments), 2)
        for candidate in candidates:
            payload = candidate.__dict__
            self.assertEqual(validate_candidate(payload), [])
            self.assertTrue(passes_proof_gate(payload))


if __name__ == "__main__":
    unittest.main()
