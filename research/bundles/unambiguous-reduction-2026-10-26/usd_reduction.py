"""Scoped unambiguous-decoder transfer bound and bounded signed controls.

These controls evaluate a fixed published measurement, never search circuits.
No classical hardness, uniform output law, or quantum execution is asserted.
"""

from fractions import Fraction
from itertools import combinations, product

import numpy as np


def transfer_bound(decoder_failure_upper, gram_tail_upper=None):
    for value in (decoder_failure_upper, gram_tail_upper):
        if value is not None and type(value) not in (int, Fraction):
            raise ValueError("exact rational analytic bounds required")
        if value is not None and value < 0:
            raise ValueError("bounds must be nonnegative")
    e = Fraction(decoder_failure_upper)
    a = e if gram_tail_upper is None else Fraction(gram_tail_upper)
    return {"ideal_success_lower": max(Fraction(0), (1-e)/(1+a)),
            "expected_trials_upper": 1/(1-e) if e < 1 else None,
            "requires": "coherent error-free-or-failure decoder and full-support Gram bound",
            "proof_status": "WRITTEN_DEDUCTION_NOT_INDEPENDENTLY_REVIEWED",
            "quantum_advantage_established": False}


def repetition_control(length):
    """F3 repetition-code control, at most 81 amplitudes; not a hard family."""
    if type(length) is not int or length not in (1, 2, 3, 4):
        raise ValueError("only fixed lengths 1 through 4; no scalable dense simulation")
    pairs = tuple(combinations(range(3), 2))
    incidence = np.array([[int(c == a)-int(c == b) for c in range(3)]
                         for a, b in pairs], dtype=float)
    cycle = np.array([1., -1., 1.])
    unitary = incidence/np.sqrt(3)+np.outer(cycle, np.ones(3))/3
    if not np.allclose(unitary.T@unitary, np.eye(3), atol=1e-14, rtol=0):
        raise ArithmeticError("signed pair isometry completion is not unitary")
    qft = np.exp(2j*np.pi*np.outer(np.arange(3), np.arange(3))/3)/np.sqrt(3)
    transform, fourier = np.ones((1, 1)), np.ones((1, 1), dtype=complex)
    for _ in range(length):
        transform = np.kron(transform, unitary)
        fourier = np.kron(fourier, qft)
    outcomes = list(product(range(3), repeat=length))
    numerators = np.array([[np.prod([incidence[j, c] for j in outcome])
                            for c in range(3)] for outcome in outcomes], dtype=int)
    good = []
    for outcome in outcomes:
        compatible = set.intersection(*(set(pairs[j]) for j in outcome))
        # Exhaustive 3^2 check of the published linear relaxation, only here.
        relaxed = [(v, w) for v, w in product(range(3), repeat=2)
                   if all((w-sum(pairs[j])*v+np.prod(pairs[j])) % 3 == 0
                          for j in outcome)]
        if compatible and (len(relaxed) == 1) != (len(compatible) == 1):
            raise ArithmeticError("repetition decoder differs from the Schur relaxation")
        good.append(len(compatible) == 1)
    good = np.array(good)
    denominator = 2**length
    gram_numerator = numerators.T@numerators
    good_numerator = numerators[good].T@numerators[good]
    expected_good = denominator-2
    if not np.array_equal(good_numerator, expected_good*np.eye(3, dtype=int)):
        raise ArithmeticError("successful branches are not exactly unambiguous")
    p = Fraction(expected_good, denominator)
    e, a = Fraction(6, denominator), Fraction(2, denominator)
    outputs = []
    for syndrome in range(3):
        fiber = [i for i, word in enumerate(outcomes)
                 if all(word) and sum(word) % 3 == syndrome]
        lam = Fraction(3*len(fiber), denominator)
        if not p:
            outputs.append({"syndrome": syndrome, "gram_eigenvalue": str(lam),
                            "status": "NO_ACCEPTED_DECODER_BRANCH"})
            continue
        character = np.exp(-2j*np.pi*syndrome*np.arange(3)/3)
        post = numerators@character/np.sqrt(denominator*3*float(p))
        post[~good] = 0
        output = fourier@transform.T@post
        target = np.zeros(len(outcomes), dtype=complex)
        target[fiber] = 1/np.sqrt(len(fiber))
        fidelity = float(abs(np.vdot(target, output))**2)
        success = float(np.sum(abs(output[fiber])**2))
        if (abs(np.vdot(output, output)-1) > 1e-12
                or abs(fidelity-float(p/lam)) > 1e-12
                or success+1e-12 < fidelity):
            raise ArithmeticError("direct signed reduction violates overlap identity")
        outputs.append({"syndrome": syndrome, "gram_eigenvalue": str(lam),
                        "proved_target_fidelity": str(p/lam),
                        "direct_target_fidelity": fidelity,
                        "direct_valid_output_probability": success,
                        "status": "BOUNDED_CLASSICAL_STATEVECTOR_CONTROL"})
    return {"length": length, "prime": 3, "code_dimension": 1,
            "amplitudes_enumerated": 3**length,
            "actual_decoder_success": str(p), "decoder_union_bound": str(e),
            "gram_tail": str(a), "old_quantum_failure_expression": str(6*e),
            "gram_numerator": gram_numerator.tolist(),
            "successful_gram_numerator": good_numerator.tolist(),
            "gram_denominator": denominator,
            "refined_success_lower": str(transfer_bound(e, a)["ideal_success_lower"]),
            "syndromes": outputs, "hardness_evidence": False,
            "quantum_execution": False}


def wrong_answer_countercontrol():
    """Exact rational 8-state counterexample to dropping unambiguity."""
    n = 8
    u = [[Fraction(int(i == j)) - (Fraction(1, 2) if i >= 4 and j >= 4 else 0)
          for j in range(n)] for i in range(n)]
    if any(sum(u[r][i]*u[r][j] for r in range(n)) != int(i == j)
           for i in range(n) for j in range(n)):
        raise ArithmeticError("countercontrol is not orthogonal")
    p = sum(u[i][i]**2 for i in range(n))/n
    post = [sum(u[j][i]*u[j][j] for j in range(n)) for i in range(n)]
    fidelity = sum(post)**2/(n*n*p)
    return {"states": n, "gram": "identity", "actual_decoder_success": str(p),
            "actual_target_fidelity": str(fidelity), "false_unambiguous_bound": str(p),
            "unambiguous": False, "hypothesis_is_necessary": fidelity < p}
