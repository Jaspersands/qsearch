import json
import os
import tempfile
import unittest
from pathlib import Path

from code_frontier_triage import build_code_frontier_triage, write_code_frontier_triage
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


def write_artifact(path: str, payload: dict) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload))


class CodeFrontierTriageTests(unittest.TestCase):
    def test_qc_canonicalization_controls_discharge_search_proof_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_artifact(
                    "research/code_equivalence/quasi_cyclic_code_search.json",
                    {
                        "records": [
                            {
                                "spec": {"id": "qc-index4-two-circulants"},
                                "status": "qc-tuple-collision-proof-debt",
                                "interpretation": "Search-level proof debt before automorphism checks.",
                            }
                        ]
                    },
                )
                write_artifact(
                    "research/code_equivalence/quasi_cyclic_canonicalization.json",
                    {
                        "records": [
                            {
                                "id": "qc-index4-two-circulants-trial-4-prior-0",
                                "status": "equivalent-under-qc-automorphism-control",
                                "interpretation": "Natural QC automorphism proves this collision is a control.",
                            }
                        ]
                    },
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report.headline_metrics["record_count"], 1)
        row = report.records[0]
        self.assertEqual(row.row_id, "qc-family-qc-index4-two-circulants")
        self.assertEqual(row.final_status, "control-or-no-hard-row-not-positive-evidence")
        self.assertEqual({item.source for item in row.evidence}, {"quasi_cyclic_code_search", "quasi_cyclic_canonicalization"})

    def test_qc_information_set_resolver_discharges_qc_proof_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_artifact(
                    "research/code_equivalence/quasi_cyclic_code_search.json",
                    {
                        "records": [
                            {
                                "spec": {"id": "qc-index5-three-circulants"},
                                "status": "qc-tuple-collision-proof-debt",
                                "interpretation": "Search-level proof debt before generic canonicalization.",
                            }
                        ]
                    },
                )
                write_artifact(
                    "research/code_equivalence/quasi_cyclic_canonicalization.json",
                    {
                        "records": [
                            {
                                "id": "qc-index5-three-circulants-trial-9-prior-0",
                                "status": "qc-automorphism-no-equivalence-proof-debt",
                                "interpretation": "Restricted automorphism non-equivalence is proof debt.",
                            }
                        ]
                    },
                )
                write_artifact(
                    "research/code_equivalence/qc_information_set_resolver.json",
                    {
                        "records": [
                            {
                                "id": "qc-index5-three-circulants-trial-9-prior-0",
                                "source_search_id": "qc-index5-three-circulants",
                                "status": "equivalent-control-under-information-set-canonicalization",
                                "interpretation": "Exact information-set canonicalization resolves the row as a control.",
                            }
                        ]
                    },
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        row = next(record for record in report.records if record.row_id == "qc-family-qc-index5-three-circulants")
        self.assertEqual(row.final_status, "control-or-no-hard-row-not-positive-evidence")
        self.assertIn("qc_information_set_resolver", {item.source for item in row.evidence})

    def test_classical_rejection_dominates_code_proof_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_artifact(
                    "research/code_equivalence/code_structural_invariants.json",
                    {
                        "records": [
                            {
                                "id": "row-a",
                                "status": "rejected-by-structural-code-invariant",
                                "interpretation": "Support splitting separates the row.",
                            }
                        ]
                    },
                )
                write_artifact(
                    "research/code_equivalence/code_information_set_baseline.json",
                    {
                        "records": [
                            {
                                "id": "row-a",
                                "status": "information-set-survivor-proof-debt",
                                "interpretation": "Information sets did not reject this row.",
                            }
                        ]
                    },
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        row = next(record for record in report.records if record.row_id == "row-a")
        self.assertEqual(row.final_status, "rejected-by-classical-code-baseline")
        self.assertEqual(report.headline_metrics["rejected_row_count"], 1)

    def test_cyclic_code_search_controls_are_triaged(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_artifact(
                    "research/code_equivalence/cyclic_code_search.json",
                    {
                        "records": [
                            {
                                "spec": {"id": "cyclic-n15"},
                                "status": "cyclic-collisions-all-dihedral-controls",
                                "interpretation": "All cyclic-code collisions are reciprocal/dihedral controls.",
                            }
                        ]
                    },
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        row = next(record for record in report.records if record.row_id == "cyclic-family-cyclic-n15")
        self.assertEqual(row.row_family, "cyclic-code-family")
        self.assertEqual(row.final_status, "control-or-no-hard-row-not-positive-evidence")

    def test_goppa_code_search_controls_are_triaged(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_artifact(
                    "research/code_equivalence/goppa_code_search.json",
                    {
                        "records": [
                            {
                                "spec": {"id": "goppa-m3-t2"},
                                "status": "goppa-collisions-all-semilinear-controls",
                                "interpretation": "All Goppa-code collisions are semilinear controls.",
                            }
                        ]
                    },
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        row = next(record for record in report.records if record.row_id == "goppa-family-goppa-m3-t2")
        self.assertEqual(row.row_family, "goppa-code-family")
        self.assertEqual(row.final_status, "control-or-no-hard-row-not-positive-evidence")

    def test_schur_filtration_rejection_is_triaged(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_artifact(
                    "research/code_equivalence/code_schur_filtration.json",
                    {
                        "family_records": [
                            {
                                "triage_row_id": "goppa-family-goppa-m4-t2",
                                "row_family": "goppa-code-family",
                                "status": "rejected-by-schur-filtration",
                                "interpretation": "Dual square dimensions separate this row.",
                            }
                        ]
                    },
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        row = next(record for record in report.records if record.row_id == "goppa-family-goppa-m4-t2")
        self.assertEqual(row.final_status, "rejected-by-classical-code-baseline")
        self.assertIn("code_schur_filtration", {item.source for item in row.evidence})

    def test_closure_conductor_rejection_is_triaged(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_artifact(
                    "research/code_equivalence/code_closure_attack.json",
                    {
                        "family_records": [
                            {
                                "triage_row_id": "goppa-family-goppa-m4-t3",
                                "row_family": "goppa-code-family",
                                "status": "rejected-by-t-closure-conductor",
                                "interpretation": "A local closure signature separates this row.",
                            }
                        ]
                    },
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        row = next(record for record in report.records if record.row_id == "goppa-family-goppa-m4-t3")
        self.assertEqual(row.final_status, "rejected-by-classical-code-baseline")
        self.assertIn("code_closure_attack", {item.source for item in row.evidence})

    def test_tanner_code_search_controls_are_triaged(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_artifact(
                    "research/code_equivalence/tanner_code_search.json",
                    {
                        "records": [
                            {
                                "spec": {"id": "tanner-10-5-dv2-dc4"},
                                "status": "tanner-collisions-all-equivalent-controls",
                                "interpretation": "All Tanner collisions are graph/canonicalization controls.",
                            }
                        ]
                    },
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        row = next(record for record in report.records if record.row_id == "tanner-family-tanner-10-5-dv2-dc4")
        self.assertEqual(row.row_family, "tanner-ldpc-family")
        self.assertEqual(row.final_status, "control-or-no-hard-row-not-positive-evidence")

    def test_affine_geometry_code_search_controls_are_triaged(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_artifact(
                    "research/code_equivalence/affine_geometry_code_search.json",
                    {
                        "records": [
                            {
                                "spec": {"id": "ag2-f3-k6"},
                                "status": "affine-geometry-collisions-all-equivalent-controls",
                                "interpretation": "All affine-geometry collisions are AGL controls.",
                            }
                        ]
                    },
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        row = next(record for record in report.records if record.row_id == "ag-family-ag2-f3-k6")
        self.assertEqual(row.row_family, "affine-geometry-code-family")
        self.assertEqual(row.final_status, "control-or-no-hard-row-not-positive-evidence")

    def test_rank_metric_code_search_controls_are_triaged(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_artifact(
                    "research/code_equivalence/rank_metric_code_search.json",
                    {
                        "records": [
                            {
                                "spec": {"id": "gabidulin-m4-n3-k2"},
                                "status": "rank-metric-collisions-all-equivalent-controls",
                                "interpretation": "All binary-expanded rank-metric rows are block controls.",
                            }
                        ]
                    },
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        row = next(record for record in report.records if record.row_id == "rank-metric-family-gabidulin-m4-n3-k2")
        self.assertEqual(row.row_family, "binary-expanded-rank-metric-family")
        self.assertEqual(row.final_status, "control-or-no-hard-row-not-positive-evidence")

    def test_rank_metric_proof_debt_is_not_hidden_by_control_rows(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_artifact(
                    "research/code_equivalence/rank_metric_code_search.json",
                    {
                        "records": [
                            {
                                "spec": {"id": "gabidulin-m4-n3-k2"},
                                "status": "rank-metric-code-search-proof-debt",
                                "interpretation": "Some binary-expanded rank-metric rows survived canonicalization caps.",
                            }
                        ]
                    },
                )
                write_artifact(
                    "research/code_equivalence/code_low_weight_structure.json",
                    {
                        "records": [
                            {
                                "row_id": "rank-metric-family-gabidulin-m4-n3-k2",
                                "row_family": "binary-expanded-rank-metric-family",
                                "status": "low-weight-matroid-equivalent-control",
                                "interpretation": "A different row in the family is a control.",
                            }
                        ]
                    },
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        row = next(record for record in report.records if record.row_id == "rank-metric-family-gabidulin-m4-n3-k2")
        self.assertEqual(row.final_status, "proof-debt-not-positive-evidence")

    def test_exact_incidence_family_control_discharges_rank_metric_proof_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_artifact(
                    "research/code_equivalence/rank_metric_code_search.json",
                    {
                        "records": [
                            {
                                "spec": {"id": "gabidulin-m4-n3-k2"},
                                "status": "rank-metric-code-search-proof-debt",
                                "interpretation": "Generic canonicalization exceeded its assignment cap.",
                            }
                        ]
                    },
                )
                write_artifact(
                    "research/code_equivalence/code_incidence_resolver.json",
                    {
                        "family_records": [
                            {
                                "triage_row_id": "rank-metric-family-gabidulin-m4-n3-k2",
                                "row_family": "binary-expanded-rank-metric-family",
                                "status": "incidence-family-all-equivalent-controls",
                                "interpretation": "Every source proof-debt pair has a verified exact coordinate permutation.",
                            }
                        ]
                    },
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        row = next(record for record in report.records if record.row_id == "rank-metric-family-gabidulin-m4-n3-k2")
        self.assertEqual(row.final_status, "control-or-no-hard-row-not-positive-evidence")
        self.assertIn("code_incidence_resolver", {item.source for item in row.evidence})

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_artifact(
                    "research/code_equivalence/code_structural_invariants.json",
                    {
                        "records": [
                            {
                                "id": "row-a",
                                "status": "rejected-by-structural-code-invariant",
                                "interpretation": "Support splitting separates the row.",
                            }
                        ]
                    },
                )
                payload = write_code_frontier_triage()
                artifact_exists = Path("research/code_equivalence/code_frontier_triage.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["rejected_row_count"], 1)
        self.assertTrue(any(result["artifacts"].get("code_frontier_triage") for result in results))
        self.assertTrue(any(item["id"].startswith("CODE-FRONTIER-TRIAGE-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "code_frontier_triage" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
