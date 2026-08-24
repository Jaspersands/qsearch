import unittest
from literature_radar import _arxiv_id_from_url

class LiteratureRadarTests(unittest.TestCase):
    def test_arxiv_id_extraction(self):
        self.assertEqual(_arxiv_id_from_url("https://arxiv.org/abs/2301.12345"), "2301.12345")
        self.assertIsNone(_arxiv_id_from_url("not-a-url"))

if __name__ == "__main__":
    unittest.main()
