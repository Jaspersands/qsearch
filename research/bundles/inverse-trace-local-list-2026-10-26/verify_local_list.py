"""Replay exact bounded controls and scalable analytic bounds, without search."""

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import platform

import flint

import local_list as m


ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / "inverse-trace-norm-transfer-2026-10-23/receipt.json"
FROZEN = {
    m.DEPENDENCY: "54fe6f9b8e3e3c2169119196cabb095411b37c76335da8d8d83b61de4535e4ce",
    PREVIOUS: "4d31298a0a9a3a7819596df9ba0e65bb113e432575c2f60b05aaa51a1c539763",
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def report():
    for path, expected in FROZEN.items():
        if digest(path) != expected:
            raise ValueError(f"frozen source changed: {path}")
    frozen = json.loads(PREVIOUS.read_text())
    native = frozen["certificate"]
    witness = frozen["same_input_witness"]
    field = m.NATIVE.BinaryField(native["bits"], native["modulus"])
    if not m.NATIVE.verify(field, native["points"], witness["values"], native["K"],
                           native["targets"], (0,)*native["K"]):
        raise ArithmeticError("unchanged native witness no longer verifies")
    finite = []
    for bits, modulus in ((2, 7), (3, 11), (5, 37), (7, 131)):
        c = m.finite_alphabet(bits, modulus)
        q, envelope = m.parameters(bits)
        spectrum = c.spectrum()
        if (len(c.alphabet) != q//2 or c.inverse_walsh[0] != 0
                or any(2*spectrum[b] != -c.inverse_walsh[b] for b in range(1, q))
                or any(abs(w) > envelope for w in c.inverse_walsh[1:])):
            raise ArithmeticError("Fourier identity or Weil envelope failed")
        maxima = max(abs(w) for w in c.inverse_walsh[1:])
        pair = (0, next(b for b in range(1, q) if abs(c.inverse_walsh[b]) == maxima))
        effect = m.pair_optimum_witness(c, *pair)
        attained = m.positive_effect_posterior(c, (effect,), pair)
        if attained != m.Fraction(1, 2)+m.Fraction(maxima, 2*q):
            raise ArithmeticError("pair optimum not attained")
        all_pairs = None
        if bits in (3, 5):
            dimensions = [m.unambiguous_subspace_dimension(c, pair)
                          for pair in combinations(range(q), 2)]
            if any(dimensions):
                raise ArithmeticError("unexpected unambiguous pair outcome")
            all_pairs = {"pairs_checked": len(dimensions), "nonzero_nullspaces": 0}
        noise = m.fourier_readout_probabilities(c)
        if sum(noise) != 1 or noise[0] != m.Fraction(1, 2):
            raise ArithmeticError("Fourier-readout positive control failed")
        finite.append({
            "bits": bits, "q": q, "modulus": modulus,
            "alphabet_size": len(c.alphabet), "characters_enumerated": q*q,
            "analytic_walsh_envelope": envelope, "exact_max_abs_walsh": maxima,
            "best_pair_posterior": str(attained), "attaining_pair": pair,
            "analytic_pair_posterior_bound": str(m.posterior_bound(bits, 2)),
            "all_pairs_rank_control": all_pairs,
            "fourier_readout_correct_probability": str(noise[0]),
        })
    control = m.finite_alphabet(3, 11)
    affine = tuple(a for a in range(8) if control.field.trace(a))
    c = m.finite_alphabet(3, 11, control_alphabet=affine)
    effect = m.pair_optimum_witness(c, 0, 1)
    if m.positive_effect_posterior(c, (effect,), (0, 1)) != 1:
        raise ArithmeticError("affine-halfspace positive control failed")
    scales = [{"bits": bits, "q": 1 << bits, "alphabet_enumerated": False,
               "necessary_error_free_list_size": m.minimum_list_size(bits),
               "necessary_two_thirds_confidence_list_size": m.minimum_list_size(bits, m.Fraction(2, 3)),
               "pair_posterior_upper": str(m.posterior_bound(bits, 2))}
              for bits in (5, 7, 17, 31, 127)]
    sources = [ROOT / name for name in ("local_list.py", "test_local_list.py",
               "verify_local_list.py", "LOCAL_LIST_BARRIER.md", "HANDOFF.md")]
    sources.extend(FROZEN)
    return {
        "status": "DIRECT_SMALL_LIST_TRANSPLANT_EXCLUDED_NOT_GLOBAL_DECODING",
        "proof_status": "WRITTEN_DEDUCTION_WITH_EXACT_CONTROLS_NOT_INDEPENDENTLY_REVIEWED",
        "scope": {"copies_per_symbol": 1, "posterior_prior": "uniform_local",
                  "unambiguous_requirement": "zero_error_for_every_field_label",
                  "global_codeword_measurements_excluded": False,
                  "adaptive_side_information_excluded": False,
                  "native_hardness_established": False, "quantum_advantage_established": False,
                  "new_native_search_executed": False, "quantum_execution": False,
                  "repository_registry_admission": False},
        "native_witness_replay": {
            "source": str(PREVIOUS.relative_to(ROOT.parent)), "sha256": FROZEN[PREVIOUS],
            "bits": native["bits"], "N": native["N"], "K": native["K"],
            "original_points_and_targets_preserved": True, "native_valid": True,
            "new_search_trials": 0, "previously_paid_trials": witness["trials"],
            "previously_paid_field_draws": witness["field_draws"]},
        "finite_controls": finite,
        "positive_countercontrol": {"alphabet": list(affine), "pair": [0, 1],
                                    "posterior": "1", "native_inverse_trace_alphabet": False},
        "analytic_scaling_not_numerical_experiments": scales,
        "primary_sources": ["https://arxiv.org/html/2610.00502v1#S2.SS1",
                            "https://doi.org/10.1016/S0022-314X(02)00011-2"],
        "runtime": {"python": platform.python_version(), "python_flint": flint.__version__},
        "sha256": {str(path.relative_to(ROOT.parent)): digest(path) for path in sources},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = report()
    destination = ROOT / "receipt.json"
    if args.check:
        if json.loads(destination.read_text()) != json.loads(json.dumps(data)):
            raise SystemExit("FAIL: receipt differs from exact replay")
        print(f"PASS: exact replay; {len(data['sha256'])} hashes; SHA256 {digest(destination)}")
    elif args.write:
        destination.write_text(json.dumps(data, indent=2) + "\n")
        print(f"Wrote {destination}; SHA256 {digest(destination)}")
    else:
        print(json.dumps(data, indent=2))
