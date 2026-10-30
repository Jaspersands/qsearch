"""Replay exact laws and the existing native input without inventing new inputs."""

import argparse
import hashlib
import json
from pathlib import Path

from exact_control import enumerate_control
from norm_sampling import GlobalNormSampler, NormCompletion, RankWeightedNormSampler, ag_sampling_bounds, systematic_draw
from scope_bounds import encode_fraction

ROOT = Path(__file__).resolve().parent


def make_receipt():
    source = ROOT.parent / "two-component-norm-2026-10-27/receipt.json"
    previous = json.loads(source.read_text())
    for name, expected in previous["source_hashes"].items():
        if hashlib.sha256((ROOT.parent / name).read_bytes()).hexdigest() != expected:
            raise ArithmeticError("native fixture source changed: "+name)
    case = NormCompletion(previous["p"], previous["original_parity"],
                          previous["auxiliary"], previous["annihilator"], 2)
    sampler = GlobalNormSampler(case)
    # Existing public-geometry fixture: d(row B)>=93, deg(8I)=64,
    # and h has full support. Thus every nonzero c restricts A injectively.
    if not all(case.h) or case.r != 32 or case.k != 43 or case.m != 176:
        raise ArithmeticError("native geometric rank-promise fixture changed")
    exact_sampler = RankWeightedNormSampler(case, restriction_rank=32)
    syndromes = [[0]*case.k, [1]*case.k, [(i*i+17*i+3) % case.p for i in range(case.k)]]
    outputs = []
    for j, syndrome in enumerate(syndromes):
        for method in ("norm", "systematic", "rank_weighted_norm"):
            if method == "norm":
                result = sampler.draw(syndrome, seed=27130+j)
            elif method == "systematic":
                result = systematic_draw(case.p, case.B, syndrome, seed=27140+j)
            else:
                result = exact_sampler.draw(syndrome, seed=27160+j)
            if result["status"] != "VERIFIED_NATIVE_WITNESS":
                raise ArithmeticError("fixed control did not finish; no replacement input")
            word = result["word"]
            if not all(word) or any(sum(a*b for a, b in zip(row, word)) % case.p != s
                                   for row, s in zip(previous["original_parity"], syndrome)):
                raise ArithmeticError("raw original relation verification failed")
            outputs.append({"method": method, **result})
    dependencies = [source, ROOT / "replay.py", ROOT / "norm_sampling.py",
                    ROOT / "exact_control.py",
                    ROOT.parent / "two-component-norm-2026-10-27/norm_completion.py",
                    ROOT.parent / "two-component-norm-2026-10-27/scope_bounds.py"]
    return {
        "status": "SCOPED_SAMPLING_THEOREM_AND_EXACT_LAW_CONTROLS",
        "exact_controls": [enumerate_control(1, True), enumerate_control(0, False)],
        "native_dimensions": [case.k, case.m], "p": case.p,
        "native_outputs": outputs, "native_input_already_easy": True,
        "native_fixture_reused_not_newly_generated": True,
        "large_field_ag_bounds": [ag_sampling_bounds(1019, e) for e in (8, 63, 64, 128, 256)],
        "unweighted_norm_native_exact_uniform_claim": False,
        "rank_weighted_native_uniformity_conditional_on_geometric_rank_proof": True,
        "native_restriction_rank_justification": {
            "rowspace_distance_lower": 93, "auxiliary_pole_degree": 64,
            "auxiliary_dimension": 32, "h_full_support_checked": True,
            "distance_and_pole_proofs_reused_not_inferred_from_samples": True},
        "native_matrix_only_adapter_implemented": False,
        "fixed_prime_asymptotic_sampler": False,
        "source_hashes": {str(path.relative_to(ROOT.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in dependencies},
        "verified_native_dependency_hashes": previous["source_hashes"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    receipt = make_receipt()
    encoded = json.dumps(receipt, sort_keys=True, indent=2, default=encode_fraction)+"\n"
    path = ROOT / "receipt.json"
    if arguments.write:
        path.write_text(encoded)
    elif path.read_text() != encoded:
        raise SystemExit("receipt mismatch")
    print(json.dumps({"status": "PASS", "mode": "write" if arguments.write else "check",
                      "native_witnesses": len(receipt["native_outputs"]),
                      "exact_controls": receipt["exact_controls"],
                      "ag_e64_success_lower": float(receipt["large_field_ag_bounds"][2]["trial_success_lower"]),
                      "ag_e64_tv_upper": float(receipt["large_field_ag_bounds"][2]["tv_upper"])},
                     default=encode_fraction))
