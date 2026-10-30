"""Native public maps and separate local controls; no incoming isogeny."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import sys

from native_maps import OrderFiveModel, finite_points
from local_gate import ROOT, orbit_control, pullback_control, split_control

sys.path.insert(0, str(ROOT/"frobenius-order-completion-2026-10-25"))
from completion import lagrangians


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    previous_path = ROOT/"regular-spectrum-kernel-2026-10-25"/"receipt.json"
    previous = json.loads(previous_path.read_text())
    for base, key in ((previous_path.parent, "source_sha256"), (ROOT, "dependency_sha256")):
        for name, expected in previous[key].items():
            if digest(base/name) != expected:
                raise AssertionError(f"frozen predecessor changed: {name}")

    model = OrderFiveModel(19)
    points = finite_points(model)
    if len(points)+1 != 438:
        raise AssertionError("native point count changed")
    for x, y in points:
        divisor = model.from_points([(x, y)])
        if model.gamma(divisor) != model.from_points([(model.zeta*x, y)]):
            raise AssertionError("Mumford map disagrees with actual point pushforward")
        moved = divisor
        for _ in range(5):
            moved = model.gamma(moved)
        if moved != divisor:
            raise AssertionError("native automorphism order check failed")
        if model.frobenius(model.gamma(divisor)) != model.gamma(model.frobenius(divisor), -1):
            raise AssertionError("native Frobenius inversion relation failed")
    rng, two_point_count = random.Random(25), 0
    while two_point_count < 40:
        pair = rng.sample(points, 2)
        if pair[0][0] == pair[1][0]:
            continue
        divisor = model.from_points(pair)
        moved = model.gamma(divisor)
        if moved != model.from_points([(model.zeta*x, y) for x, y in pair]):
            raise AssertionError("degree-two divisor map failed")
        if model.frobenius(moved) != model.gamma(model.frobenius(divisor), -1):
            raise AssertionError("degree-two semidirect relation failed")
        two_point_count += 1
    identity = model.from_points([])
    if model.gamma(identity) != identity or model.frobenius(identity) != identity:
        raise AssertionError("divisor identity changed")

    gamma, frobenius = split_control()
    profiles, source_profiles = Counter(), Counter()
    for index, plane in enumerate(lagrangians(11, cap=2000)):
        orbit = orbit_control(plane, gamma, frobenius, 19, 11)
        profiles[orbit] += 1
        if index % 97 == 0:
            pulled = pullback_control(plane, gamma, frobenius, 19, 11)
            if pulled != tuple(rank-2 for rank in orbit[1:]):
                raise AssertionError("source pullbacks and target orbit growth disagree")
            source_profiles[pulled] += 1
    if profiles != {(2, 4, 4): 1464} or source_profiles != {(2, 2): 16}:
        raise AssertionError("local full-census/control profiles changed")

    sources = ("native_maps.py", "local_gate.py", "test_native_maps.py", "replay.py",
               "ORDER_FIVE_GATE.md", "HANDOFF.md")
    dependencies = {
        "regular-spectrum-kernel-2026-10-25/receipt.json",
        "regular-spectrum-kernel-2026-10-25/REGULAR_SPECTRUM.md",
        "source-pullback-2026-10-23/pullback.py",
        "source-pullback-2026-10-23/SOURCE_PULLBACK_ATTACK.md",
        "kernel-output-2026-10-23/kernel_output.py",
        "frobenius-order-completion-2026-10-25/completion.py",
    }
    record = {
        "status": "PROPOSED_NATIVE_SUBFAMILY_CLASSICAL_ATTACK_REVIEW_PENDING",
        "native_public_map_frontend_executed": True,
        "incoming_geometric_isogeny_constructed": False,
        "native_kernel_recovered": False,
        "geometric_weak_basis_backend_executed": False,
        "geometric_hiding_function_executed": False,
        "hiding_function_queries_required_by_theorem": 0,
        "independent_review_completed": False,
        "quantum_speedup_admitted": False,
        "native_control": {
            "curve": "y^2=x^5-1", "characteristic": 19, "point_field_degree": 2,
            "points_including_infinity": len(points)+1,
            "affine_point_maps_checked": len(points), "degree_two_divisors_checked": two_point_count,
            "identity_checked": True, "field_context": str(model.field), "zeta": str(model.zeta),
            "coefficient_frobenius_inversion_relation_checked": True,
            "incoming_isogeny_present": False,
        },
        "native_model_certificates": [OrderFiveModel(p, 2).certificate(11)
                                      for p in (19, 29, 59, 79, 109, 139, 4294967279)],
        "separate_local_control": {
            "ell": 11, "characteristic_parameter": 19, "lagrangian_census_size": 1464,
            "orbit_profiles": [{"ranks": list(k), "count": v} for k, v in sorted(profiles.items())],
            "prime_square_pullback_profiles": [{"ranks": list(k), "count": v}
                                                for k, v in sorted(source_profiles.items())],
            "known_reference_lagrangians_used": True,
            "native_torsion_basis_constructed": False,
        },
        "frozen_predecessor_sources_checked": len(previous["source_sha256"]),
        "frozen_predecessor_dependencies_checked": len(previous["dependency_sha256"]),
        "source_sha256": {name: digest(root/name) for name in sources},
        "dependency_sha256": {name: digest(ROOT/name) for name in sorted(dependencies)},
    }
    destination = root/"receipt.json"
    destination.write_text(json.dumps(record, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"receipt": str(destination), "sha256": digest(destination),
                      "native_affine_points": len(points), "local_planes": 1464,
                      "native_kernel_recovered": False}, indent=2))


if __name__ == "__main__":
    main()
