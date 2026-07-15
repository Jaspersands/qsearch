import os
import tempfile
import unittest

from literature_pipeline import (
    build_hidden_shift_candidate,
    extract_literature_records,
    hypothesize_from_literature,
    submit_hypothesis,
)
from proof_gate import passes_proof_gate
from research_registry import (
    CandidateRecord,
    load_candidates,
    load_experiments,
    load_rejected_candidates,
    utc_now,
)


class LiteraturePipelineTests(unittest.TestCase):
    def test_literature_extraction_produces_structured_mechanism_records(self):
        records = extract_literature_records(refresh_arxiv=False)
        self.assertGreaterEqual(len(records), 10)
        hidden_shift = [record for record in records if "hidden-shift" in record.tags]
        self.assertTrue(hidden_shift)
        self.assertTrue(hidden_shift[0].mechanism)
        self.assertTrue(hidden_shift[0].problem_family)
        self.assertTrue(hidden_shift[0].reduction)
        self.assertTrue(hidden_shift[0].no_go_barrier)
        self.assertTrue(hidden_shift[0].proof_technique)
        self.assertTrue(hidden_shift[0].open_question)
        self.assertTrue(hidden_shift[0].reusable_abstraction)

    def test_shifted_character_papers_use_specific_complexity_mechanism(self):
        records = extract_literature_records(refresh_arxiv=False)
        shifted = [record for record in records if "shifted-character" in record.tags]

        self.assertGreaterEqual(len(shifted), 3)
        self.assertTrue(all("Gauss" in record.proof_technique for record in shifted))
        self.assertTrue(all("preprocessing" in record.no_go_barrier for record in shifted))
        self.assertTrue(all("reduction" in record.open_question for record in shifted))

    def test_schur_product_papers_extract_classical_code_barriers(self):
        records = extract_literature_records(refresh_arxiv=False)
        schur = [record for record in records if "schur-product" in record.tags]

        self.assertGreaterEqual(len(schur), 2)
        self.assertTrue(all("Schur" in record.mechanism for record in schur))
        self.assertTrue(all("support" in record.open_question for record in schur))
        self.assertTrue(all("polynomial time" in record.no_go_barrier for record in schur))

    def test_hidden_number_records_preserve_random_vs_chosen_access_gap(self):
        records = extract_literature_records(refresh_arxiv=False)
        hidden_number = [record for record in records if "hidden-number" in record.tags]

        self.assertGreaterEqual(len(hidden_number), 2)
        self.assertTrue(all("random-multiplier" in record.problem_family for record in hidden_number))
        self.assertTrue(all("chosen" in record.no_go_barrier for record in hidden_number))
        self.assertTrue(all("one-shot" in record.open_question for record in hidden_number))

    def test_toy_oracle_hypothesis_is_rejected(self):
        now = utc_now()
        toy = CandidateRecord(
            id="TEST-TOY-ORACLE",
            title="Tiny custom oracle secret finder",
            status="hypothesis",
            created_at=now,
            updated_at=now,
            literature_ids=[],
            ontology_node_ids=[],
            problem_family="custom oracle on N<=3 examples",
            input_model="black-box toy oracle",
            classical_baseline="brute force",
            reduction_or_lower_bound="",
            quantum_mechanism="qiskit simulation",
            cost_model="",
            measurement_and_decoding="",
            success_statement="small example appears to work",
            complexity_accounting="",
            no_go_analysis="",
            dequantization_check="",
            falsifiers=[],
        )
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                accepted, issues = submit_hypothesis(toy, [])
            finally:
                os.chdir(old_cwd)
        self.assertFalse(accepted)
        self.assertFalse(passes_proof_gate(toy.__dict__))
        self.assertGreaterEqual(len(issues), 1)

    def test_valid_hidden_shift_hypothesis_is_accepted_by_gate(self):
        records = extract_literature_records(refresh_arxiv=False)
        candidate, experiments = build_hidden_shift_candidate(records)
        self.assertTrue(passes_proof_gate(candidate.__dict__))
        self.assertIn("hidden-shift", candidate.ontology_node_ids)
        self.assertGreaterEqual(len(candidate.literature_ids), 2)
        self.assertGreaterEqual(len(experiments), 1)
        self.assertTrue(all(experiment.falsifiers for experiment in experiments))

    def test_hypothesis_pipeline_records_accepted_and_rejected_candidates(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                result = hypothesize_from_literature(refresh_arxiv=False)

                now = utc_now()
                toy = CandidateRecord(
                    id="TEST-REJECTED-TOY-ORACLE",
                    title="Rejected tiny custom oracle fixture",
                    status="hypothesis",
                    created_at=now,
                    updated_at=now,
                    literature_ids=[],
                    ontology_node_ids=[],
                    problem_family="custom oracle on N<=3 examples",
                    input_model="black-box toy oracle",
                    classical_baseline="brute force",
                    reduction_or_lower_bound="",
                    quantum_mechanism="qiskit simulation",
                    cost_model="",
                    measurement_and_decoding="",
                    success_statement="small example appears to work",
                    complexity_accounting="",
                    no_go_analysis="",
                    dequantization_check="",
                    falsifiers=[],
                )
                accepted, issues = submit_hypothesis(toy, [])

                candidates = load_candidates()
                experiments = load_experiments()
                rejected = load_rejected_candidates()
            finally:
                os.chdir(old_cwd)

        self.assertIn("HYP-LIT-HIDDEN-SHIFT-SIEVE", result.accepted)
        self.assertIn("HYP-LIT-COSET-OBSERVABLES", result.accepted)
        self.assertEqual(result.rejected, [])
        self.assertFalse(accepted)
        self.assertTrue(issues)
        self.assertTrue(any(item["id"] == "HYP-LIT-HIDDEN-SHIFT-SIEVE" for item in candidates))
        self.assertTrue(any(item["candidate_id"] == "HYP-LIT-HIDDEN-SHIFT-SIEVE" for item in experiments))
        rejection = [item for item in rejected if item["id"] == "TEST-REJECTED-TOY-ORACLE"]
        self.assertEqual(len(rejection), 1)
        self.assertGreaterEqual(len(rejection[0]["issues"]), 1)


if __name__ == "__main__":
    unittest.main()
