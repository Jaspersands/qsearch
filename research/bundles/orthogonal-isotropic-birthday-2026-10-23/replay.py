import hashlib
import json
from pathlib import Path

import isotropic_birthday as ib


def main():
    here = Path(__file__).resolve().parent
    runs = []
    for n, p in ((3, 3), (3, 5), (4, 3), (5, 3), (4, 13)):
        hidden = ib.op.eye(2*n)[:n]
        swap = [list(row) for row in ib.op.eye(2*n)]
        swap[0], swap[n] = swap[n], swap[0]
        hidden = ib.op.image(tuple(map(tuple, swap)), hidden, p)
        oracle = ib.op.OpaqueFixtureOracle(hidden, p)
        report = ib.recover(oracle, n, p)
        assert report["candidate"] == hidden
        assert report["actual_queries"] == oracle.calls
        runs.append({"rank": n, "prime": p, "correct_hidden_space": True, **report})
    files = [here / name for name in ("isotropic_birthday.py", "test_isotropic_birthday.py",
                                      "CLASSICAL_ATTACK.md", "replay.py")]
    files += [Path(ib.op.__file__), ib.WORK / "central-rank-2026-10-23/central_rank.py"]
    receipt = {"status": "proposed stronger classical baseline; independent review pending",
               "quantum_executed": False, "natural_source_hardness_established": False,
               "runs": runs,
               "analytical_not_executed_schedules": [ib.query_schedule(n, p) for n, p in ((16, 3), (64, 3), (8, 127))],
               "source_hashes": {str(path.relative_to(ib.WORK)): hashlib.sha256(path.read_bytes()).hexdigest()
                                 for path in files}}
    path = here / "isotropic_birthday_receipt.json"
    path.write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps({"receipt": str(path), "actual_query_counts": [run["actual_queries"] for run in runs]}, indent=2))


if __name__ == "__main__":
    main()
