import json
import os
import tempfile
import unittest
from pathlib import Path

from blocker_taxonomy import write_blocker_taxonomy
from cfi_parity_solver import write_cfi_parity_solver_report
from cfi_structural_decoder import write_cfi_structural_decoder_report
from code_canonicalization_baseline import write_code_canonicalization_baseline
from code_tuple_profile_baseline import write_code_tuple_profile_baseline
from conjecture_tracker import write_conjecture_report
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment
from mutation_engine import build_mutation_proposals, write_mutation_report
from research_registry import initialize_seed_registry, load_candidates, load_experiments, load_mutation_proposals, validate_registry


class MutationEngineTests(unittest.TestCase):
    def test_blocked_conjectures_generate_mutation_proposals(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-DHS-PHASE-SIEVE")
                run_experiment("EXP-CODE-COSET-RANK")
                write_dequantization_report()
                write_conjecture_report()
                report = write_mutation_report()
                write_conjecture_report()
                second_pass_proposals = build_mutation_proposals()
                proposals = load_mutation_proposals()
                candidates = load_candidates()
                experiments = load_experiments()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        mutation_types = {proposal["mutation_type"] for proposal in proposals}
        self.assertGreaterEqual(report["proposal_count"], 2)
        self.assertIn("dcp-recursive-decoder-certificate", mutation_types)
        self.assertIn("dcp-bad-register-robust-architecture", mutation_types)
        self.assertIn("dcp-random-label-polynomial-decoder", mutation_types)
        self.assertNotIn("query-model-hardened-hidden-shift", mutation_types)
        self.assertNotIn("learnability-resistant-hidden-shift", mutation_types)
        self.assertIn("wl-hard-coset-observable", mutation_types)
        self.assertGreaterEqual(report["accepted_preflight_count"], 1)
        self.assertFalse(any(candidate["id"].startswith("MUT-CAND-DHS-GOWERS-SIEVE") for candidate in candidates))
        self.assertTrue(any(candidate["id"].startswith("MUT-CAND-CODE-COSET-COLLECTIVE") for candidate in candidates))
        self.assertFalse(any(experiment["id"].startswith("EXP-MUT-DHS-GOWERS-SIEVE") for experiment in experiments))
        self.assertTrue(any(experiment["id"].startswith("EXP-MUT-CODE-COSET-COLLECTIVE-CODE-EQUIV") for experiment in experiments))
        dcp_proposal = next(proposal for proposal in proposals if proposal["mutation_type"] == "dcp-recursive-decoder-certificate")
        self.assertFalse(dcp_proposal["proof_gate_eligible"])
        self.assertTrue(dcp_proposal["proof_obligations_to_resolve"])
        robust_proposal = next(
            proposal for proposal in proposals if proposal["mutation_type"] == "dcp-bad-register-robust-architecture"
        )
        self.assertFalse(robust_proposal["proof_gate_eligible"])
        self.assertEqual(robust_proposal["formalization_status"], "proposal-only-unformalized")
        self.assertTrue(any("bad flags" in item for item in robust_proposal["rejection_filters"]))
        self.assertFalse(any("bad flag oracle" in module.lower() for module in robust_proposal["required_modules"]))
        self.assertFalse(any(candidate["id"].endswith("DCP-BAD-REGISTER-ROBUST-ARCHITECTURE") for candidate in candidates))
        random_decoder_proposal = next(
            proposal for proposal in proposals if proposal["mutation_type"] == "dcp-random-label-polynomial-decoder"
        )
        self.assertFalse(random_decoder_proposal["proof_gate_eligible"])
        self.assertTrue(any("length-N FFT" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertTrue(any("random supplied labels" in item for item in random_decoder_proposal["proof_obligations_to_resolve"]))
        self.assertTrue(any("query-access SFT" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertTrue(any("uniform hashed Hadamard" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertTrue(any("polynomial-trace" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertTrue(any("covariant-PGM success formulas" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertIn("normalized subset-sum fiber ranking/unranking and block-encoding search", random_decoder_proposal["required_modules"])
        self.assertTrue(any("signal-only witnesses" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertIn("density-one partial average-case subset-sum solver synthesis", random_decoder_proposal["required_modules"])
        self.assertTrue(any("explicit subset candidate lists" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertTrue(any("weaker partial deterministic" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertIn("modular lattice-embedding mutation with average-case short-vector geometry analysis", random_decoder_proposal["required_modules"])
        self.assertTrue(any("retuning scales" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertTrue(any("LPN/LWE" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertTrue(any("biased or smooth one-score" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertIn("degree-indexed U-statistic resource auditor", random_decoder_proposal["required_modules"])
        self.assertIn(
            "implicit tensor-contraction cost, coefficient-norm, precision, and N-spectrum detector",
            random_decoder_proposal["required_modules"],
        )
        self.assertTrue(any("disjoint fixed-degree" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertTrue(any("all-subsets product U-statistics" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertIn("full-rank many-outcome covariant measurement and compressed-PGM synthesis", random_decoder_proposal["required_modules"])
        self.assertIn("low-bond tensor-train contraction search", random_decoder_proposal["required_modules"])
        self.assertTrue(any("rank-one elementary-symmetric" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertIn("exact cross-component all-order Hoeffding covariance evaluator", random_decoder_proposal["required_modules"])
        self.assertTrue(any("tested cosine, Fejer" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertIn("approximate hashed-residue tensor-network search", random_decoder_proposal["required_modules"])
        self.assertIn("which-path garbage and interference verifier", random_decoder_proposal["required_modules"])
        self.assertIn(
            "target-independent shared-seed and reversible fixed-seed interface checker",
            random_decoder_proposal["required_modules"],
        )
        self.assertIn(
            "paired quantum witness amplitude and workspace-fidelity certificate",
            random_decoder_proposal["required_modules"],
        )
        self.assertTrue(any("solely for nondeterminism" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertTrue(any("inverse-polynomial workspace overlap" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertIn(
            "odd-unit orbit sampler and reduced-basis feature extractor",
            random_decoder_proposal["required_modules"],
        )
        self.assertTrue(any("signed-coordinate randomization" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertTrue(any("odd-unit LLL rescue counts" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertIn(
            "symbolic odd-part residue-orbit invariant and anti-concentration prover",
            random_decoder_proposal["required_modules"],
        )
        self.assertTrue(any("further blind odd-unit" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertTrue(any("which-subset garbage" in item for item in random_decoder_proposal["rejection_filters"]))
        self.assertFalse(any(proposal["source_candidate_id"].startswith("MUT-CAND-") for proposal in second_pass_proposals))
        self.assertTrue(validation["valid"])

    def test_typed_research_mutations_replace_generic_fallback_without_conjectures(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                proposals = build_mutation_proposals()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(proposals)
        typed = [
            proposal
            for proposal in proposals
            if proposal["mutation_type"] == "typed-recoupling-mechanism"
        ]
        self.assertEqual(len(typed), 2)
        self.assertTrue(all(proposal["proof_gate_eligible"] is False for proposal in typed))
        self.assertFalse(any(proposal["mutation_type"] == "blocker-driven-search" for proposal in proposals))

    def test_malformed_proof_debt_report_does_not_block_mutation(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(parents=True, exist_ok=True)
                Path("research/proof_debt_report.json").write_text("")
                report = write_mutation_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertGreaterEqual(report["proposal_count"], 1)
        self.assertTrue(validation["valid"])

    def test_blocker_artifacts_generate_targeted_code_and_cfi_mutations(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_code_canonicalization_baseline(include_code_family_search=False)
                write_code_tuple_profile_baseline(include_code_family_search=False)
                write_cfi_parity_solver_report(base_sizes=[4, 5, 6])
                write_cfi_structural_decoder_report(base_ids=["complete-k5", "mobius-ladder-8"])
                write_dequantization_report()
                write_blocker_taxonomy()
                report = write_mutation_report()
                proposals = load_mutation_proposals()
                candidates = load_candidates()
                experiments = load_experiments()
                canonical_exp = "EXP-MUT-CODE-COSET-COLLECTIVE-CODE-CANONICALIZATION"
                tuple_exp = "EXP-MUT-CODE-COSET-COLLECTIVE-CODE-TUPLE-PROFILE"
                runner_result = run_experiment(canonical_exp)
                tuple_runner_result = run_experiment(tuple_exp)
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        mutation_types = {proposal["mutation_type"] for proposal in proposals}
        self.assertIn("canonicalization-resistant-code-equivalence", mutation_types)
        self.assertIn("cfi-promise-escape-coset", mutation_types)
        self.assertTrue(any(candidate["id"].endswith("CANONICALIZATION-RESISTANT-CODES") for candidate in candidates))
        self.assertTrue(any(candidate["id"].endswith("CFI-PROMISE-ESCAPE") for candidate in candidates))
        self.assertTrue(any(experiment["id"] == canonical_exp for experiment in experiments))
        self.assertTrue(any(experiment["id"] == tuple_exp for experiment in experiments))
        self.assertGreaterEqual(report["accepted_preflight_count"], 2)
        self.assertEqual(runner_result.status, "completed")
        self.assertEqual(tuple_runner_result.status, "completed")
        self.assertTrue(validation["valid"])

    def test_coset_triage_artifact_generates_escape_proposal(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research/coset_workbench").mkdir(parents=True, exist_ok=True)
                Path("research/coset_workbench/coset_frontier_triage.json").write_text(
                    """{
  "headline_metrics": {
    "rejected_pair_count": 4,
    "survivor_pair_count": 0,
    "proof_debt_pair_count": 0
  }
}"""
                )
                proposals = build_mutation_proposals()
            finally:
                os.chdir(old_cwd)

        mutation_types = {proposal["mutation_type"] for proposal in proposals}
        self.assertIn("coset-frontier-triage-escape", mutation_types)
        triage = next(proposal for proposal in proposals if proposal["mutation_type"] == "coset-frontier-triage-escape")
        self.assertIn("coset frontier triage gate", triage["required_modules"])
        self.assertIn("DEQ-COSET-FRONTIER-TRIAGE-REJECTIONS", triage["linked_blockers"])

    def test_exact_reduction_failures_generate_interface_repair_proposals(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                audit_path = Path("research/reductions/interface_audit.json")
                audit_path.parent.mkdir(parents=True, exist_ok=True)
                audit_path.write_text(
                    json.dumps(
                        {
                            "audits": [
                                {
                                    "id": "AUDIT-DHS",
                                    "route_id": "ROUTE-DHS",
                                    "candidate_id": "DHS-GOWERS-SIEVE",
                                    "theorem_contract_id": "THM-REGEV-USVP-TO-DCP-2003",
                                    "target_problem": "candidate-specific-hidden-shift-family",
                                    "checks": [
                                        {"axis": "access-model", "passed": False},
                                        {"axis": "full-family-coverage", "passed": False},
                                    ],
                                },
                                {
                                    "id": "AUDIT-CODE",
                                    "route_id": "ROUTE-CODE",
                                    "candidate_id": "CODE-COSET-COLLECTIVE",
                                    "theorem_contract_id": "CONSTRUCTION-CODE-EQUIVALENCE-TO-NONABELIAN-HSP",
                                    "target_problem": "candidate-collective-observable-family",
                                    "checks": [
                                        {"axis": "access-model", "passed": True},
                                        {"axis": "full-family-coverage", "passed": False},
                                    ],
                                },
                                {
                                    "id": "AUDIT-RECURSIVE",
                                    "route_id": "ROUTE-RECURSIVE",
                                    "candidate_id": "MUT-CAND-DHS-GOWERS-SIEVE-QUERY-MODEL-HARDENED",
                                    "theorem_contract_id": "THM-REGEV-USVP-TO-DCP-2003",
                                    "target_problem": "candidate-specific-hidden-shift-family",
                                    "checks": [{"axis": "access-model", "passed": False}],
                                },
                            ]
                        }
                    )
                )
                proposals = build_mutation_proposals()
                report = write_mutation_report(promote_valid=False)
            finally:
                os.chdir(old_cwd)

        by_type = {proposal["mutation_type"]: proposal for proposal in proposals}
        self.assertIn("reduction-contract-coset-sample-native", by_type)
        self.assertIn("generic-dhsp-family-lift", by_type)
        self.assertIn("full-source-family-lift", by_type)
        sample_native = by_type["reduction-contract-coset-sample-native"]
        self.assertEqual(sample_native["theorem_contract_id"], "THM-REGEV-USVP-TO-DCP-2003")
        self.assertIn("access-model", sample_native["failed_interface_axes"])
        self.assertFalse(sample_native["proof_gate_eligible"])
        self.assertEqual(sample_native["formalization_status"], "proposal-only-unformalized")
        self.assertTrue(sample_native["rejection_filters"])
        self.assertTrue(all("coherent evaluator" not in module.lower() for module in sample_native["required_modules"]))
        self.assertIn("no evaluator oracle", sample_native["new_hypothesis"].lower())
        self.assertFalse(any(proposal["source_candidate_id"].startswith("MUT-CAND-") for proposal in proposals))
        self.assertEqual(report["interface_repair_proposal_count"], 3)
        self.assertEqual(report["proposal_only_count"], 5)
        self.assertEqual(
            len(
                [
                    proposal
                    for proposal in report["proposals"]
                    if proposal["mutation_type"] == "typed-recoupling-mechanism"
                ]
            ),
            2,
        )


if __name__ == "__main__":
    unittest.main()
