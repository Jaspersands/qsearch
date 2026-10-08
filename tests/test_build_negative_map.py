import importlib.util
import json
import math
import tempfile
import unittest
from pathlib import Path

HAS_SKLEARN = importlib.util.find_spec("sklearn") is not None


def synthetic_records():
    goppa = "goppa code syzygy collision hull projector canonical invariant"
    sieve = "dihedral sieve lattice depth nearest plane reflection list"
    records = []
    for i in range(30):
        records.append({"id": f"GOPPA-{i:02d}", "claim": f"Goppa syzygy collision row {i} resists the hull projector.", "reason": f"{goppa} variant {i % 5}"})
        records.append({"id": f"SIEVE-{i:02d}", "claim": f"Dihedral sieve depth {i} keeps nearest plane lists small.", "reason": f"{sieve} variant {i % 5}"})
    return records


@unittest.skipUnless(HAS_SKLEARN, "scikit-learn is needed to build the map")
class NegativeMapTests(unittest.TestCase):
    def test_points_are_normalised_and_topics_separate(self) -> None:
        from tools.build_negative_map import build_map

        result = build_map(synthetic_records(), regions=2)
        points = {p["id"]: p for p in result["points"]}
        self.assertEqual(len(points), 60)
        for p in points.values():
            self.assertTrue(0 <= p["x"] <= 1 and 0 <= p["y"] <= 1)

        def centroid(prefix):
            xs = [p["x"] for k, p in points.items() if k.startswith(prefix)]
            ys = [p["y"] for k, p in points.items() if k.startswith(prefix)]
            return sum(xs) / len(xs), sum(ys) / len(ys)

        (ax, ay), (bx, by) = centroid("GOPPA"), centroid("SIEVE")
        self.assertGreater(math.hypot(ax - bx, ay - by), 0.2)

    def test_regions_have_distinct_labels_and_counts(self) -> None:
        from tools.build_negative_map import build_map

        regions = build_map(synthetic_records(), regions=2)["regions"]
        self.assertEqual(len(regions), 2)
        labels = [r["label"] for r in regions]
        self.assertTrue(all(labels))
        self.assertEqual(len(set(labels)), 2)
        self.assertEqual(sum(r["count"] for r in regions), 60)

    def test_main_writes_the_map_file(self) -> None:
        from tools.build_negative_map import main

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "site" / "data").mkdir(parents=True)
            records = [{"id": r["id"], "claim": r["claim"], "reason": r["reason"]} for r in synthetic_records()]
            (root / "site" / "data" / "negatives.json").write_text(json.dumps({"records": records}))
            self.assertEqual(main(["--root", str(root), "--regions", "2"]), 0)
            written = json.loads((root / "site" / "data" / "negative_map.json").read_text())
            self.assertEqual(len(written["points"]), 60)


if __name__ == "__main__":
    unittest.main()
