"""Replay the public pullback interface, not the imported quantum solver."""

import argparse
import json
from pathlib import Path
import sys

import a3_pullback as a3

sys.path.insert(0, str(Path(__file__).resolve().parent.parent /
                       "orthogonal-exterior-2026-10-27"))
from exterior_controls import all_subspaces

op = a3.op


def receipt():
    p, counts, seen = 3, {}, set()
    spaces = {d: tuple(all_subspaces(4, d, p)) for d in (1, 2, 3)}
    flags = [(v,) for d in (1, 2, 3) for v in spaces[d]]
    flags += [(point, hyperplane) for point in spaces[1] for hyperplane in spaces[3]
              if len(op.basis(point+hyperplane, p)) == 3]
    query = [list(v) for v in op.eye(4)]
    query[0][1] = 1
    phi = a3.exterior_square(query, p)
    for flag in flags:
        hidden = a3.flag_to_singular(flag, p)
        assert hidden not in seen
        seen.add(hidden)
        counts[len(hidden)] = counts.get(len(hidden), 0)+1
        assert a3.supplied_space_to_flag(hidden, p) == flag
        assert a3.flag_to_singular(a3.image_flag(query, flag, p), p) == op.image(phi, hidden, p)
    assert counts == {1: 130, 2: 520, 3: 80}
    interface = []
    for p in (3, 5, 2**127-1):
        for shape in ((1,), (2,), (3,), (1, 3)):
            flag = tuple(op.eye(4)[:d] for d in shape)
            hidden = a3.flag_to_singular(flag, p)
            original = op.OpaqueFixtureOracle(hidden, p)
            pullback = a3.PullbackOracle(original, p)
            origin = pullback(op.eye(4))
            tests = 0
            for i in range(4):
                for j in range(4):
                    if i == j:
                        continue
                    g = [list(v) for v in op.eye(4)]
                    g[i][j] = 1
                    assert (pullback(g) == origin) == (a3.image_flag(g, flag, p) == flag)
                    tests += 1
            assert original.calls == pullback.calls == tests+1
            interface.append({"p": p, "flag_dimensions": shape,
                              "original_queries": original.calls, "pullback_queries": pullback.calls,
                              "hidden_data_used_only_by_fixture": True})
    return {"status": "exact_reduction_controls_only", "p3_flag_counts_by_hidden_rank": counts,
            "one_query_pullback_controls": interface, "imported_solver_executed": False,
            "quantum_algorithm_executed": False, "novel_algorithm_claimed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", type=Path)
    group.add_argument("--check", type=Path)
    args = parser.parse_args()
    data = receipt()
    encoded = json.loads(json.dumps(data))
    if args.write:
        args.write.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    elif json.loads(args.check.read_text(encoding="utf-8")) != encoded:
        raise SystemExit("receipt differs from exact replay")
    print(json.dumps({"verified": True, "flags": sum(data["p3_flag_counts_by_hidden_rank"].values()),
                      "interface_cases": len(data["one_query_pullback_controls"]),
                      "imported_solver_executed": False}))


if __name__ == "__main__":
    main()
