"""Reproduce exact decoded-output controls and actual finite-product runs."""

from fractions import Fraction as Q
from pathlib import Path
from random import Random
import hashlib
import json
import sys

from decoded_controls import accepted_trial_law, exact_importance_moments, observable_mean, output_law
from decoded_transfer import DecodedSampler, PauliEstimator, d, old
from transfer_access import TransferAccess
from tree_sampler import Decomposition


ROOT = Path(__file__).resolve().parent


def small_case(paulis, decoder_kind):
    couplings = [Q((-1)**i, i+1) for i in range(len(paulis))]
    model = d.Physical.create(2, paulis, couplings, Q(1, 2))
    m = model.pilot.m
    dec = Decomposition(m, model.pilot.edges, [set(range(m))], [], independence_bound=m)
    access = TransferAccess(dec, couplings, [(Q(1, 3), Q(1, 7)), (Q(-1, 5), Q(2, 9))])
    table = {model.label(y): y for y in reversed(range(1 << m))}
    if decoder_kind == "zero":
        decoder = lambda syndrome: 0
    elif decoder_kind == "imaginary-phase-control":
        grouped = {model.label(y): y for y in (1, 7)}
        decoder = lambda syndrome: grouped.get(syndrome, 0)
    else:
        decoder = lambda syndrome: table.get(syndrome, 0)
    sampler = DecodedSampler(model, decoder, access)
    accepted, target = accepted_trial_law(sampler), output_law(model, decoder, access.parameters)
    bound = sampler.plan["fiber_bound"]
    assert sum(accepted.values()) == Q(1, bound)
    assert {e: p*bound for e, p in accepted.items() if p} == {e: p for e, p in target.items() if p}
    observations = []
    for observable in ((1, 0, 0), (0, 1, 0), (2, 3, 1)):
        estimator = PauliEstimator(model, decoder, access, observable)
        mean, second = exact_importance_moments(estimator)
        assert mean == observable_mean(model, decoder, access.parameters, observable)
        assert second <= 1
        observations.append({"observable": observable, "exact_mean": mean, "exact_second_moment": second})
    return {"paulis": paulis, "couplings": couplings, "parameters": [[str(u.x), str(u.y)] for u in access.parameters],
            "decoder_kind": decoder_kind, "plan": sampler.plan,
            "nonzero_target_events": sum(bool(p) for p in target.values()),
            "exact_trial_success": sum(accepted.values()), "observations": observations,
            "all_output_events_match": True}


def live_case():
    model, decoder = old.large_fixture(24)
    n, radius = model.n, 4
    bags = [set(range(i, i+radius+1)) for i in range(n-radius)]+[{0, n}]
    links = [(i, i+1) for i in range(n-radius-1)]+[(0, len(bags)-1)]
    decomposition = Decomposition(model.pilot.m, model.pilot.edges, bags, links, independence_bound=1)
    access = TransferAccess(decomposition, model.pilot.couplings, [(Q(1, 5), Q(1, 7)), Q(-1, 9)])
    sampler = DecodedSampler(model, decoder, access, delta=Q(1, 64))
    outputs = [sampler.sample(Random(seed)) for seed in (37, 41, 43, 47)]
    assert all(o["status"] == "sample" for o in outputs)
    estimator = PauliEstimator(model, decoder, access, (1, 0, 0))
    draws = [estimator.draw(Random(seed)) for seed in range(4)]
    return {"physical_qubits": n, "pilot_generators": access.m,
            "finite_transfer_factors": len(access.parameters), "sampler_plan": sampler.plan,
            "transfer_resources": access.resources, "samples": outputs,
            "pauli_draws_diagnostic_only": draws, "pauli_estimate_certified": False,
            "dense_state_used": False, "full_thermal_sampler_executed": False}


def certified_small_estimate():
    model = d.Physical.create(1, [(0, 1, 0)], [1], Q(1, 2))
    access = TransferAccess(Decomposition(1, [], [{0}], [], independence_bound=1), [1], [Q(1, 3)])
    decoder = lambda syndrome: syndrome >> 1
    estimator = PauliEstimator(model, decoder, access, (0, 1, 0))
    result = estimator.estimate(Random(179), epsilon=Q(1, 4), delta=Q(1, 16), max_draws=3000)
    exact, second = exact_importance_moments(estimator)
    return {"result": result, "exact_mean": exact, "exact_second_moment": second,
            "observed_error": abs(result["estimate"]-exact),
            "scope": "finite-pilot implementation control, not a new algorithm candidate"}


def build():
    sources = ("transfer_access.py", "decoded_transfer.py", "decoded_controls.py",
               "test_decoded_transfer.py", "replay.py", "EXACT_DECODED_OUTPUT.md")
    context = ("hdqi-ecf-tree-sampler-2026-10-25/tree_sampler.py",
               "hdqi-ecf-tree-sampler-2026-10-25/tree_controls.py",
               "hdqi-ecf-tree-sampler-2026-10-25/ECF_TREE_SAMPLING.md",
               "hdqi-output-sampling-2026-10-24/output_sampling.py",
               "hdqi-decoded-observables-2026-10-24/decoded_observables.py",
               "central-rank-2026-10-23/central_rank.py")
    result = {"schema": "exact-transfer-decoded-output-v1",
              "source_sha256": {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sources},
              "context_sha256": {f: hashlib.sha256((ROOT.parent/f).read_bytes()).hexdigest() for f in context},
              "claim_status": "local unreviewed exact finite-pilot output theorem and implementation",
              "independent_review_completed": False, "quantum_advantage_claim": False,
              "general_high_rank_output_sampling_solved": False,
              "full_thermal_sampler_executed": False, "small_controls": []}
    cases = [(((1, 0, 0), (0, 1, 0), (1, 1, 1)), "section"),
             (((1, 0, 0), (1, 0, 0), (0, 1, 0)), "section"),
             (((0, 1, 0), (0, 2, 0), (0, 3, 0)), "zero"),
             (((1, 0, 0), (0, 3, 0), (2, 0, 0)), "imaginary-phase-control")]
    for paulis, kind in cases:
        control = small_case(paulis, kind)
        result["small_controls"].append(control)
        print(kind, "full law matches; success", control["exact_trial_success"], flush=True)
    result["live_physical_output"] = live_case()
    live = result["live_physical_output"]
    print("physical", live["physical_qubits"], "pilot", live["pilot_generators"], "fiber rank",
          live["sampler_plan"]["fiber_rank"], "sample trials", [o["trials"] for o in live["samples"]], flush=True)
    result["certified_estimator_control"] = certified_small_estimate()
    control = result["certified_estimator_control"]
    print("estimator control", control["result"]["pilot_samples"], "draws; error", control["observed_error"], flush=True)
    return json.loads(json.dumps(result, default=str))


def main():
    if sys.argv[1:] not in (["write"], ["check"]):
        raise SystemExit("usage: replay.py write|check")
    result = build()
    destination = ROOT/"receipt.json"
    if sys.argv[1] == "write":
        destination.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    elif result != json.loads(destination.read_text()):
        raise SystemExit("receipt mismatch")
    print(sys.argv[1], "PASS; receipt sha256", hashlib.sha256(destination.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
