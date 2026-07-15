import json
import tempfile
import unittest
from pathlib import Path

from paper_ingestion import build_no_go_index, extract_citation_keys, extract_paper_record, write_paper_ingestion


class PaperIngestionTests(unittest.TestCase):
    def test_latex_paper_extraction_finds_mechanism_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hidden_shift_note.tex"
            path.write_text(
                r"""
                \title{A Hidden Shift Phase State Note}
                We study the hidden shift problem and the dihedral hidden subgroup problem.
                The main theorem gives a reduction from structured hidden shift to dihedral HSP.
                A no-go barrier is that full-table dequantization can recover the shift.
                The proof uses Fourier analysis and a phase state primitive.
                Open problem: prove a lower bound for random sample access.
                \begin{theorem}\label{thm:classical-reconstruction}
                Any full-table access model admits a classical reconstruction attack.
                \end{theorem}
                We cite prior work \cite{kuperberg2003,regev2003} and arXiv:2305.01707.
                """
            )
            record = extract_paper_record(path)

        self.assertIsNotNone(record)
        assert record is not None
        self.assertIn("hidden shift", record.problem_family.lower())
        self.assertIn("phase", record.mechanism.lower())
        self.assertIn("reduction", record.reduction.lower())
        self.assertIn("barrier", record.no_go_barrier.lower())
        self.assertIn("proof", record.proof_technique.lower())
        self.assertIn("open problem", record.open_question.lower())
        self.assertTrue(record.theorem_like_statements)
        theorem = next(item for item in record.theorem_like_statements if item.kind == "theorem")
        self.assertEqual(theorem.label, "thm:classical-reconstruction")
        self.assertEqual(theorem.extraction_confidence, "high")
        self.assertIn("\\begin{theorem}", theorem.source_locator)
        self.assertEqual(record.source_format, "tex")
        self.assertIn("kuperberg2003", record.citation_keys)
        self.assertIn("arxiv:2305.01707", record.citation_keys)
        index = build_no_go_index([record])
        self.assertTrue(any(item.barrier_type == "classical-dequantization" for item in index))

    def test_write_paper_ingestion_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "paper.md").write_text("# Quantum Walk Span Program\nA span program framework gives a quantum walk algorithm.")
            records = write_paper_ingestion([root], output_path=root / "out.json", no_go_index_path=root / "nogos.json")

        self.assertEqual(len(records), 1)
        self.assertIn("quantum walk", records[0]["mechanism"].lower())

    def test_citation_key_extraction(self):
        keys = extract_citation_keys(r"See \citep{a,b} and arXiv:2401.12345v2 plus quant-ph/0302112.")
        self.assertEqual(keys, ["a", "arxiv:2401.12345v2", "arxiv:quant-ph/0302112", "b"])

    def test_write_paper_ingestion_writes_no_go_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paper = root / "nogos.tex"
            paper.write_text(
                r"""
                \title{No-Go Note}
                Strong Fourier sampling over the symmetric group has a no-go barrier for graph isomorphism.
                \begin{lemma}
                This lower bound blocks single-register nonabelian Fourier sampling.
                \end{lemma}
                """
            )
            no_go_path = root / "nogos.json"
            records = write_paper_ingestion([paper], output_path=root / "out.json", no_go_index_path=no_go_path)
            no_go_records = json.loads(no_go_path.read_text())

        self.assertEqual(len(records), 1)
        self.assertTrue(no_go_records)
        self.assertTrue(any(item["barrier_type"] == "nonabelian-fourier-sampling" for item in no_go_records))

    def test_random_access_fourier_limit_is_preserved_as_no_go_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "random_access_sft.tex"
            path.write_text(
                r"""
                \title{Significant Fourier Coefficients Under Random Access}
                We distinguish the query access model from a random access model.
                A significant Fourier coefficient algorithm using random noisy samples
                would solve Learning Parity with Noise and hidden number problems.
                We therefore do not expect query-access significant Fourier algorithms
                to transfer to the random access model.
                \begin{theorem}\label{thm:sft-query}
                Query access permits recovery of every significant Fourier coefficient.
                \end{theorem}
                Open problem: characterize random-sample access without chosen queries.
                """
            )
            record = extract_paper_record(path)

        self.assertIsNotNone(record)
        assert record is not None
        self.assertIn("significant Fourier coefficient learning", record.mechanism)
        self.assertIn("random-sample Fourier access separation", record.mechanism)
        self.assertIn("random-access noisy Fourier learning", record.problem_family)
        self.assertIn("do not expect", record.no_go_barrier.lower())
        self.assertIn("random access", record.reusable_abstraction.lower())
        self.assertTrue(any(item.label == "thm:sft-query" for item in record.theorem_like_statements))
        no_go_index = build_no_go_index([record])
        self.assertTrue(any(item.barrier_type == "random-access-fourier-separation" for item in no_go_index))

    def test_multifile_tex_expansion_preserves_sparse_fourier_access_requirements(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            main = root / "main.tex"
            main.write_text(
                r"""
                \title{Sparse Fourier Access Audit}
                \input{methods}
                """
            )
            (root / "methods.tex").write_text(
                r"""
                We give a Sparse Fourier Transform using HashToBins.
                The locator samples pairs randomly but in a correlated fashion.
                The proof uses hashing and filtered shifted measurements.
                """
            )
            record = extract_paper_record(main)

        self.assertIsNotNone(record)
        assert record is not None
        self.assertIn("hash-based sparse Fourier localization", record.mechanism)
        self.assertIn("filtered hash-to-bins Fourier measurements", record.mechanism)
        self.assertIn("correlated sample-pair localization", record.mechanism)
        self.assertIn("structured-query sparse Fourier recovery", record.problem_family)
        self.assertIn("hashing", record.proof_technique.lower())
        self.assertIn("hashtobins", record.reusable_abstraction.lower())


if __name__ == "__main__":
    unittest.main()
