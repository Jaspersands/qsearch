"""Exact sequential spectral moment extraction under supplied-model premises.

LOCAL DERIVATION / REVIEW PENDING. This is conditional matrix dequantization,
not construction of a model from native states/records or a new algorithm.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import random

from sympy.polys.matrices import DomainMatrix

from ternary_character_synchronization import _records
from ternary_covariant_noise import CovariantRecord, root_digits, simulated_record
from ternary_cyclic_extractor import random_even_source
from ternary_flat_character_certificate import Cyclotomic, ResourceLimit, positive_weight_certificate
from ternary_observable_moment_lift import difference_basis

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_SEQUENTIAL_SPECTRAL_EXTRACTION.md"
REPORT = ROOT / "research/classical_baselines/ternary_sequential_spectral_extraction.json"
SOURCE = ROOT / "research/classical_baselines/ternary_character_synchronization.json"


class Uncertified(ValueError):
    pass


def _exact(value, name, positive=False):
    if type(value) not in (int, Fraction) or value < 0 or (positive and value == 0):
        raise ValueError(f"{name} requires a nonnegative exact rational" + (" greater than0" if positive else ""))
    return Fraction(value)


def _rational_input(value, name):
    if type(value) is str:
        parsed = Fraction(value)
        if str(parsed) != value:
            raise ValueError(f"{name} requires canonical exact rational encoding")
        value = parsed
    return _exact(value, name)


def pinching_constant(q):
    root_digits(q)
    # Average the shortest signed representatives, not only powers0..q-1.
    return Fraction(q*q-1, 4*q)


def psd_certificate(field, matrix, require_definite=False):
    """Exact LDL/Schur certificate; zero pivots require an entirely zero row."""
    rows = [list(row) for row in matrix.to_list()]
    R = len(rows)
    if matrix.shape != (R, R) or field.conjugate_matrix(matrix).transpose() != matrix:
        raise Uncertified("Hermitian square metric/norm bound required")
    L = [[field.K.one if i == j else field.K.zero for j in range(R)] for i in range(R)]
    diagonal, signs = [], []
    for k in range(R):
        pivot = rows[k][k]
        sign = positive_weight_certificate(field, pivot)
        if sign["status"] == "ZERO":
            if require_definite or any(rows[i][k] != field.K.zero for i in range(k+1, R)):
                raise Uncertified("singular metric or zero PSD pivot with nonzero row")
        elif sign["status"] != "POSITIVE":
            raise Uncertified("negative or unresolved exact PSD pivot")
        else:
            for i in range(k+1, R):
                L[i][k] = rows[i][k]/pivot
            for i in range(k+1, R):
                for j in range(k+1, R):
                    rows[i][j] -= L[i][k]*pivot*field.conjugate(L[j][k])
        diagonal.append(pivot)
        signs.append(sign)
    return {"lower_unit_matrix": field.encode_matrix(field.matrix(L)),
            "diagonal": [field.encode(x) for x in diagonal], "pivot_sign_certificates": signs,
            "positive_definite_required": require_definite,
            "rank_exact": sum(x != field.K.zero for x in diagonal)}


def _matrix(field, raw, rows, columns):
    if len(raw) != rows or any(len(row) != columns for row in raw):
        raise Uncertified("complete supplied matrix/vector shape required")
    return field.matrix([[field.decode(x) for x in row] for row in raw])


def _norm(field, metric, vector):
    return (field.conjugate_matrix(vector).transpose()*metric*vector).to_list()[0][0]


def _expect(field, metric, vector, operator):
    return (field.conjugate_matrix(vector).transpose()*metric*operator*vector).to_list()[0][0]


def _nonnegative(field, value, label):
    sign = positive_weight_certificate(field, value)
    if sign["status"] not in ("POSITIVE", "ZERO"):
        raise Uncertified(f"{label}: negative or unresolved exact sign")
    return sign


def _coefficients(frequency, inverse, q):
    raw = tuple(sum(a*inverse[j][i] for j, a in enumerate(frequency)) % q for i in range(len(frequency)))
    return tuple(x if 2*x < q else x-q for x in raw)


@dataclass(frozen=True)
class Prepared:
    records: tuple
    field: Cyclotomic
    metric: DomainMatrix
    operators: tuple
    state: DomainMatrix
    projectors: tuple
    order: tuple
    inverse_basis: tuple
    moments: tuple
    coefficients: tuple
    moment_error: tuple
    certificate: dict


def prepare_model(records, payload, max_projector_entries=1_000_000):
    records, n, q = _records(records)
    try:
        if type(max_projector_entries) is not int or max_projector_entries < 1:
            raise ValueError("positive whole-projector entry cap required")
        if payload.get("access_model") != "supplied_classical_matrices_and_state":
            raise Uncertified("native state supply does not grant classical matrices/state coordinates")
        order = tuple(payload["measurement_order"])
        if sorted(order) != list(range(n)) or any(type(x) is not int for x in order):
            raise Uncertified("complete committed measurement/product order required")
        if payload["represented_product_order"] != list(order):
            raise Uncertified("original moment representation uses a different product order")
        basis = difference_basis(records)
        if basis["rank_mod3"] < n:
            raise Uncertified("no full native unit-difference basis")
        field = Cyclotomic(q)
        R = len(payload["metric"])
        if R < 1 or q*n*R*R > max_projector_entries:
            raise ResourceLimit("whole spectral projector vocabulary exceeds cap")
        metric = _matrix(field, payload["metric"], R, R)
        metric_cert = psd_certificate(field, metric, require_definite=True)
        state = _matrix(field, payload["state"], R, 1)
        if _norm(field, metric, state) != field.K.one:
            raise Uncertified("supplied state is not exactly normalized in the positive metric")
        if len(payload["operators"]) != n:
            raise Uncertified("one exact q-order operator per original secret coordinate required")
        operators = tuple(_matrix(field, A, R, R) for A in payload["operators"])
        identity = DomainMatrix.eye(R, field.K).to_dense()
        for A in operators:
            if field.conjugate_matrix(A).transpose()*metric*A != metric or A**q != identity:
                raise Uncertified("supplied operator lacks exact metric unitarity or q-periodicity")
        raw_delta = payload["commutator_operator_norm_uppers"]
        if len(raw_delta) != n or any(len(row) != n for row in raw_delta):
            raise Uncertified("complete operator-norm bound matrix required")
        delta = tuple(tuple(_rational_input(x, "operator-norm bound") for x in row) for row in raw_delta)
        if any(delta[i][i] != 0 or delta[i][j] != delta[j][i] for i in range(n) for j in range(n)):
            raise Uncertified("commutator bounds must be symmetric with zero diagonal")
        norm_certs = []
        exactly_commuting = True
        for i in range(n):
            for j in range(i+1, n):
                C = operators[i]*operators[j]-operators[j]*operators[i]
                exactly_commuting = exactly_commuting and C.is_zero_matrix
                bound = metric.scalarmul(field.K.convert(delta[i][j]**2))-field.conjugate_matrix(C).transpose()*metric*C
                norm_certs.append({"generators": (i, j), "operator_norm_upper": str(delta[i][j]),
                                   "PSD_bound_certificate": psd_certificate(field, bound)})
        projectors = []
        for A in operators:
            powers = [identity]
            for _ in range(1, q):
                powers.append(A*powers[-1])
            family = []
            total = DomainMatrix.zeros((R, R), field.K).to_dense()
            for t in range(q):
                P = DomainMatrix.zeros((R, R), field.K).to_dense()
                for k, power in enumerate(powers):
                    P += power.scalarmul(field.powers[-t*k % q]/field.K.convert(q))
                total += P
                if not P.is_zero_matrix:
                    if P*P != P or field.conjugate_matrix(P).transpose()*metric != metric*P:
                        raise Uncertified("spectral projector is not exactly orthogonal in the positive metric")
                    if A*P != P.scalarmul(field.powers[t]):
                        raise Uncertified("spectral projector has wrong full-root eigenvalue")
                    family.append((t, P))
            if total != identity or any(P*Q != DomainMatrix.zeros((R, R), field.K).to_dense()
                                        for t, P in family for u, Q in family if t != u):
                raise Uncertified("spectral family is incomplete or nonorthogonal")
            projectors.append(tuple(family))
        spectral_steps = [math.gcd(q, *(t for t, _ in family)) for family in projectors]
        possible_labels = math.prod(q//step for step in spectral_steps)
        vocabulary_bound = math.prod(len(family) for family in projectors)
        possible_secrets = min(possible_labels, vocabulary_bound, R if exactly_commuting else vocabulary_bound)
        raw_moments, raw_sigma = payload["original_native_moments"], payload["representation_error_uppers"]
        if len(raw_moments) != len(records) or len(raw_sigma) != len(records) or any(len(x) != 3 for x in (*raw_moments, *raw_sigma)):
            raise Uncertified("all original first/second/difference moments and error bounds required")
        moments, coefficients, errors, moment_certs = [], [], [], []
        seen = {}
        h = pinching_constant(q)
        for j, record in enumerate(records):
            frequencies = (record.first, record.second, tuple((a-b) % q for a, b in zip(record.first, record.second)))
            for k, frequency in enumerate(frequencies):
                target = field.decode(raw_moments[j][k])
                if frequency in seen and seen[frequency] != target:
                    raise Uncertified("original equal native frequencies have inconsistent moments")
                if not any(frequency) and target != field.K.one:
                    raise Uncertified("original zero-frequency moment must be exactly1")
                seen[frequency] = target
                _nonnegative(field, field.K.one-target*field.conjugate(target), "original unit moment bound")
                b = _coefficients(frequency, basis["modular_unit_difference_inverse"], q)
                sigma = _rational_input(raw_sigma[j][k], "original representation error")
                word = identity
                for i in order:
                    word = word*(operators[i]**(b[i] % q))
                expected = _expect(field, metric, state, word)
                mismatch = target-expected
                representation_cert = _nonnegative(field, field.K.convert(sigma*sigma)-mismatch*field.conjugate(mismatch), "original representation bound")
                disturbance = h*sum((abs(b[order[c]])*delta[order[a]][order[c]] for a in range(n) for c in range(a+1, n)), Fraction(0))
                error = min(Fraction(2), sigma+disturbance)
                moments.append(target)
                coefficients.append(b)
                errors.append(error)
                moment_certs.append({"record_index": j, "harmonic_index": k, "frequency": frequency,
                                     "balanced_basis_coefficients": b, "ordered_word_expectation": field.encode(expected),
                                     "original_representation_error_upper": str(sigma), "representation_bound_certificate": representation_cert,
                                     "sequential_disturbance_upper": str(disturbance), "total_original_moment_error_upper": str(error)})
        report = {"status": "SUPPLIED_MODEL_CERTIFIED_FOR_CONDITIONAL_SEQUENTIAL_MOMENTS_REVIEW_PENDING",
                  "supplied_model_certified": True, "difference_basis": basis, "measurement_order": order,
                  "positive_metric_certificate": metric_cert, "commutator_norm_certificates": norm_certs,
                  "native_moment_certificates": moment_certs, "pinching_constant_exact": str(h),
                  "native_score_expectation_loss_upper": str(sum(errors)),
                  "projector_terms_charged": n*q*q, "dense_projector_entries_upper": n*q*R*R,
                  "operator_dimension": R, "cyclotomic_field_degree_charged": field.degree,
                  "generator_exact_periods": [q//step for step in spectral_steps],
                  "eigenlabel_subgroup_steps": spectral_steps,
                  "secret_support_size_upper_from_generator_periods": str(possible_labels),
                  "uniform_secret_coverage_upper_from_generator_periods": str(Fraction(possible_labels, q**n)),
                  "all_generators_primitive_q_order": all(step == 1 for step in spectral_steps),
                  "all_generators_exactly_commute": exactly_commuting,
                  "nonzero_projector_counts": [len(family) for family in projectors],
                  "secret_support_size_upper_from_supplied_model": str(possible_secrets),
                  "uniform_secret_coverage_upper_from_supplied_model": str(Fraction(possible_secrets, q**n)),
                  "input_compact_JSON_bytes": len(json.dumps(payload, separators=(",", ":"))),
                  "all_internal_intermediate_bit_costs_certified": False,
                  "full_secret_grid_size": str(q**n), "full_secret_grid_enumerated": False,
                  "classical_model_construction_from_native_input_supplied": False,
                  "native_noisy_recovery_proved": False, "quantum_speedup_proved": False}
        prepared = Prepared(records, field, metric, operators, state, tuple(projectors), order,
                            tuple(tuple(x) for x in basis["modular_unit_difference_inverse"]),
                            tuple(moments), tuple(coefficients), tuple(errors), report)
        return report, prepared
    except (ValueError, KeyError, IndexError, TypeError) as e:
        return {"status": "UNKNOWN_RESOURCE_LIMIT" if isinstance(e, ResourceLimit) else "REJECTED_OR_UNRESOLVED_SUPPLIED_MODEL",
                "issues": [str(e)], "supplied_model_certified": False, "native_noisy_recovery_proved": False}, None


def sequential_draw(model, rng, max_random_bits=128):
    """One dyadic-prefix draw; unknown/capped comparisons ABORT, never redraw."""
    if type(max_random_bits) is not int or max_random_bits < 8:
        raise ValueError("at least8 explicit random-bit budget required")
    field, metric, vector = model.field, model.metric, model.state
    n = len(model.operators)
    values, transcript = [None]*n, []
    for i in model.order:
        norm = _norm(field, metric, vector)
        candidates = []
        for t, P in model.projectors[i]:
            v = P*vector
            if not v.is_zero_matrix:
                candidates.append((t, v))
        weights = [_norm(field, metric, v) for _, v in candidates]
        if sum(weights, field.K.zero) != norm or norm == field.K.zero:
            raise ArithmeticError("sequential conditional probabilities failed exact normalization")
        prefix = bits = 0
        selected = None
        while bits+8 <= max_random_bits and selected is None:
            prefix = (prefix << 8)+rng.getrandbits(8)
            bits += 8
            lower = field.K.convert(Fraction(prefix, 2**bits))*norm
            upper = field.K.convert(Fraction(prefix+1, 2**bits))*norm
            cumulative = field.K.zero
            for (t, v), weight in zip(candidates, weights):
                previous, cumulative = cumulative, cumulative+weight
                left = positive_weight_certificate(field, lower-previous)
                right = positive_weight_certificate(field, cumulative-upper)
                if left["status"] in ("POSITIVE", "ZERO") and right["status"] in ("POSITIVE", "ZERO"):
                    selected = (t, v)
                    break
        if selected is None:
            return {"status": "UNKNOWN_CAPPED_OR_UNRESOLVED_RANDOM_PREFIX", "completed_steps": len(transcript),
                    "discarded_then_redrawn": False, "secret_certified": False}
        t, vector = selected
        values[i] = t
        transcript.append([bits, str(prefix), t])
    secret = tuple(sum(a*b for a, b in zip(row, values)) % field.q for row in model.inverse_basis)
    return {"status": "EXACT_ACCEPTED_SEQUENTIAL_TRAJECTORY", "secret": secret,
            "root_eigenvalue_tuple": values, "dyadic_prefix_transcript": transcript,
            "secret_certified": True, "discarded_then_redrawn": False,
            "accepted_distribution_conditioned_on_no_abort_is_claimed_unbiased": False}


def confidence_ledger(records, epsilon, confidence_bits):
    records, n, q = _records(records)
    epsilon = _exact(epsilon, "native score sampling slack", positive=True)
    if type(confidence_bits) is not int or confidence_bits < 1:
        raise ValueError("positive integer confidence bits required")
    draws = math.ceil(confidence_bits*(6*len(records)+epsilon)/epsilon)
    return {"native_records": len(records), "generators": n, "modulus": str(q),
            "score_sampling_slack": str(epsilon), "confidence_bits": confidence_bits,
            "required_fixed_independent_draws": draws,
            "ideal_independent_sampling_score_failure_upper": f"2^-{confidence_bits}",
            "bound_controls_bad_and_returned_event_not_abort_conditioned_probability": True,
            "requires_independent_uniform_random_bits_and_supplied_model_premises": True,
            "unknown_sign_or_random_prefix_abort_never_silently_resampled": True,
            "fresh_quantum_preparations_required_if_not_classical_coordinates": draws,
            "native_source_model_and_preparation_costs_supplied": False}


def native_score(field, records, secret):
    score = field.K.zero
    for record in records:
        a, c = record.residual(secret)
        for e in (a, c, (a-c) % field.q):
            score += (field.powers[e]+field.powers[-e % field.q])/field.K.convert(2)
    return score


def supplied_moment_score(model):
    field = model.field
    total = field.K.zero
    for j, record in enumerate(model.records):
        y, z = record.outcome
        for k, e in enumerate((y, z, (y-z) % field.q)):
            value = field.powers[-e % field.q]*model.moments[3*j+k]
            total += (value+field.conjugate(value))/field.K.convert(2)
    return total


def run_sampling(model, epsilon, confidence_bits=8, rng=None, max_draws=None):
    ledger = confidence_ledger(model.records, epsilon, confidence_bits)
    K = ledger["required_fixed_independent_draws"]
    if max_draws is not None and (type(max_draws) is not int or max_draws < K):
        return {"status": "UNKNOWN_INSUFFICIENT_FIXED_DRAW_BUDGET", "ledger": ledger,
                "conditional_rounding_score_certified": False}
    seeded = rng is not None
    rng = rng if seeded else random.SystemRandom()
    trajectories, best, best_score = [], None, None
    for _ in range(K):
        draw = sequential_draw(model, rng)
        if not draw["secret_certified"]:
            return {"status": draw["status"], "completed_draws": len(trajectories), "abort": draw,
                    "unknown_trajectories_silently_discarded": False, "conditional_rounding_score_certified": False}
        score = native_score(model.field, model.records, draw["secret"])
        if best is None:
            best, best_score = draw["secret"], score
        else:
            sign = positive_weight_certificate(model.field, score-best_score)
            if sign["status"] not in ("POSITIVE", "ZERO", "NEGATIVE"):
                return {"status": "UNKNOWN_EXACT_SCORE_ORDERING", "conditional_rounding_score_certified": False}
            if sign["status"] == "POSITIVE":
                best, best_score = draw["secret"], score
        trajectories.append(draw["dyadic_prefix_transcript"])
    score = supplied_moment_score(model)
    loss = sum(model.moment_error)
    threshold = score-model.field.K.convert(loss+Fraction(epsilon))
    margin = positive_weight_certificate(model.field, best_score-threshold)
    met = margin["status"] in ("POSITIVE", "ZERO")
    return {"status": "CONDITIONAL_NATIVE_HARMONIC_ROUNDING_VERIFIED" if met else "SAMPLED_SCORE_BELOW_OR_UNRESOLVED_CONDITIONAL_THRESHOLD",
            "ledger": ledger, "completed_draws": K, "dyadic_prefix_trajectories": trajectories,
            "selected_secret": best, "selected_score": model.field.encode(best_score),
            "original_supplied_moment_score": model.field.encode(score),
            "score_expectation_loss_upper": str(loss), "score_threshold": model.field.encode(threshold),
            "score_margin_certificate": margin, "conditional_rounding_score_certified": met,
            "randomness_kind": "seeded_calibration" if seeded else "system_random_assumption",
            "probabilistic_failure_claim_applies_to_this_seeded_run": False,
            "exact_posthoc_score_fact_not_true_secret_recovery": True,
            "unknown_trajectories_silently_discarded": False,
            "full_secret_grid_enumerated": False, "held_out_native_prediction_verified": False,
            "native_noisy_recovery_proved": False, "quantum_speedup_proved": False}


def weighted_pinching(model, i, b, X):
    field = model.field
    out = DomainMatrix.zeros(X.shape, field.K).to_dense()
    for t, P in model.projectors[i]:
        out += (P*X*P).scalarmul(field.powers[b*t % field.q])
    return out


def bounded_reference(model, max_outcomes=4096):
    field, n = model.field, len(model.operators)
    if field.q**n > max_outcomes:
        raise ResourceLimit("complete reference outcome grid exceeds cap; no partial probability certificate")
    probabilities = []
    maps = [dict(x) for x in model.projectors]
    for values in product(range(field.q), repeat=n):
        vector = model.state
        for i in model.order:
            if values[i] not in maps[i]:
                vector = DomainMatrix.zeros(vector.shape, field.K).to_dense()
                break
            vector = maps[i][values[i]]*vector
        p = _norm(field, model.metric, vector)
        if p != field.K.zero:
            _nonnegative(field, p, "reference sequential probability")
        probabilities.append({"root_eigenvalue_tuple": values, "probability": field.encode(p)})
    if sum((field.decode(p["probability"]) for p in probabilities), field.K.zero) != field.K.one:
        raise ArithmeticError("complete sequential reference probabilities do not sum to1")
    probes = []
    h = pinching_constant(field.q)
    # Complete bounded word reference, not a scalable q^n inference routine.
    raw_delta = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for cert in model.certificate["commutator_norm_certificates"]:
        i, j = cert["generators"]
        raw_delta[i][j] = raw_delta[j][i] = Fraction(cert["operator_norm_upper"])
    identity = DomainMatrix.eye(model.metric.shape[0], field.K).to_dense()
    for raw_b in product(range(field.q), repeat=n):
        b = tuple(x if 2*x < field.q else x-field.q for x in raw_b)
        mean = sum((field.decode(p["probability"])*field.powers[sum(x*y for x, y in zip(b, p["root_eigenvalue_tuple"])) % field.q]
                    for p in probabilities), field.K.zero)
        X = identity
        for i in reversed(model.order):
            X = weighted_pinching(model, i, b[i], X)
        heisenberg = _expect(field, model.metric, model.state, X)
        if mean != heisenberg:
            raise ArithmeticError("Heisenberg order does not match exact sequential probabilities")
        word = identity
        for i in model.order:
            word = word*(model.operators[i]**(b[i] % field.q))
        before = _expect(field, model.metric, model.state, word)
        error = h*sum((abs(b[model.order[c]])*raw_delta[model.order[a]][model.order[c]] for a in range(n) for c in range(a+1, n)), Fraction(0))
        difference = mean-before
        sign = _nonnegative(field, field.K.convert(error*error)-difference*field.conjugate(difference), "polynomial moment disturbance bound")
        probes.append({"balanced_word": b, "sequential_moment": field.encode(mean),
                       "ordered_operator_moment": field.encode(before), "disturbance_upper": str(error),
                       "disturbance_certificate": sign})
    return {"probabilities": probabilities, "all_balanced_word_probes": probes,
            "entire_reference_outcomes_checked": len(probabilities), "reference_is_scalable_sampler": False}


def polynomial_precision_ledger(n, q, per_score_record_loss=Fraction(1, 10)):
    root_digits(q)
    if type(n) is not int or n < 2:
        raise ValueError("at least two generators required for the disturbance ledger")
    loss = _exact(per_score_record_loss, "normalized score loss", positive=True)
    h = pinching_constant(q)
    worst = h*Fraction((q-1)*n*(n-1), 4)
    return {"generators": n, "modulus": str(q), "pinching_constant_exact": str(h),
            "worst_balanced_word_uniform_commutator_coefficient": str(worst),
            "sufficient_uniform_commutator_bound_at_zero_representation_error": str(loss/(3*worst)),
            "original_representation_errors_assumed_zero_not_established": True,
            "precision_dependence_is_polynomial_in_n_and_q": True,
            "native_source_satisfies_premises": False, "global_commuting_operator_rounding_claimed": False}


def calibration_payload(records, secret_support, perturb=False, reverse=False):
    records, n, q = _records(records)
    basis = difference_basis(records)
    field, R = Cyclotomic(q), 3
    metric = DomainMatrix.eye(R, field.K).to_dense()
    state = field.matrix([[field.K.convert(Fraction(2, 3))], [field.K.convert(Fraction(1, 3))], [field.K.convert(Fraction(2, 3))]])
    operators = []
    for j in basis["basis_record_indices"]:
        d = tuple((a-b) % q for a, b in zip(records[j].first, records[j].second))
        eigenvalues = [field.powers[sum(a*s for a, s in zip(d, secret)) % q] for secret in secret_support]
        operators.append(field.matrix([[eigenvalues[i] if i == k else field.K.zero for k in range(R)] for i in range(R)]))
    t = Fraction(1, 10000)
    if perturb:
        if n != 2:
            raise ValueError("prespecified noncommuting calibration uses two native coordinates")
        c, s = field.K.convert((1-t*t)/(1+t*t)), field.K.convert(2*t/(1+t*t))
        H = field.matrix([[c, -s*field.z, field.K.zero], [s*field.powers[-1], c, field.K.zero], [field.K.zero, field.K.zero, field.K.one]])
        operators[1] = H*operators[1]*field.conjugate_matrix(H).transpose()
    moments, sigmas = [], []
    weights = (Fraction(4, 9), Fraction(1, 9), Fraction(4, 9))
    for record in records:
        row, bounds = [], []
        for f in (record.first, record.second, tuple((a-b) % q for a, b in zip(record.first, record.second))):
            row.append(field.encode(sum((field.K.convert(w)*field.powers[sum(a*s for a, s in zip(f, secret)) % q]
                                         for secret, w in zip(secret_support, weights)), field.K.zero)))
            b = _coefficients(f, basis["modular_unit_difference_inverse"], q)
            bounds.append(str(4*t*abs(b[1]) if perturb else Fraction(0)))
        moments.append(row)
        sigmas.append(bounds)
    delta = [["0" for _ in range(n)] for _ in range(n)]
    if perturb:
        delta[0][1] = delta[1][0] = str(8*t)
    order = list(reversed(range(n))) if reverse else list(range(n))
    return {"access_model": "supplied_classical_matrices_and_state", "metric": field.encode_matrix(metric),
            "state": field.encode_matrix(state), "operators": [field.encode_matrix(A) for A in operators],
            "measurement_order": order, "represented_product_order": list(order),
            "commutator_operator_norm_uppers": delta, "original_native_moments": moments,
            "representation_error_uppers": sigmas,
            "calibration_operators_encode_known_support": True,
            "matrices_were_constructed_from_native_noisy_records": False,
            "has_native_quantum_access_to_these_generators": False}


def run_controls():
    source = json.loads(SOURCE.read_text())
    controls = []
    for c in source["native_controls"]:
        records = tuple(CovariantRecord(tuple(r["first"]), tuple(r["second"]), tuple(r["outcome"]), r["modulus"])
                        for r in c["native_records"])
        n, q = len(records[0].first), records[0].modulus
        support = ((0,)*n, tuple(c["calibration_secret"]), (q-1,)*n)
        payload = calibration_payload(records, support)
        verified, model = prepare_model(records, payload)
        if model is None:
            raise ArithmeticError(f"known commuting calibration rejected: {verified}")
        sampling = run_sampling(model, Fraction(len(records), 8), rng=random.Random(c["seed"]+91))
        if not sampling["conditional_rounding_score_certified"]:
            raise ArithmeticError("prespecified conditional classical score calibration failed")
        controls.append({"source_seed": c["seed"], "records": [r.public() for r in records],
                         "supplied_model": payload, "verification": verified, "sampling": sampling})
    native = random_even_source(2, 4, 3, 89641)
    support = ((0, 0), (1, 3), (8, 8))
    rng = random.Random(89642)
    records = tuple(simulated_record(a, c, support[1], 9, rng)[0] for a, c in native.frequencies)
    noncommuting = []
    for reverse in (False, True):
        payload = calibration_payload(records, support, perturb=True, reverse=reverse)
        verified, model = prepare_model(records, payload)
        if model is None:
            raise ArithmeticError(f"noncommuting exact-order calibration rejected: {verified}")
        reference = bounded_reference(model)
        sampling = run_sampling(model, Fraction(len(records), 8), rng=random.Random(89661+int(reverse)))
        if not sampling["conditional_rounding_score_certified"]:
            raise ArithmeticError("noncommuting score sampling calibration failed")
        noncommuting.append({"original_native_level": native.level, "original_ring_labels": native.labels,
                            "records": [r.public() for r in records], "supplied_model": payload,
                            "verification": verified, "reference": reference, "sampling": sampling})
    return {"status": "CONDITIONAL_SEQUENTIAL_NATIVE_MOMENT_EXTRACTION_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "source_report": str(SOURCE.relative_to(ROOT)), "source_report_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "commuting_native_label_controls": controls, "noncommuting_native_label_controls": noncommuting,
            "polynomial_precision_ledgers": [polynomial_precision_ledger(n, q) for n, q in ((8, 9), (32, 81), (128, 243))],
            "classical_model_construction_from_native_input_supplied": False,
            "native_noisy_decoder_supplied": False, "quantum_speedup_proved": False,
            "candidate_record_accepted": False, "novelty_claim": False,
            "routine_wiring_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "successful_conditional_sampling_runs": len(report["commuting_native_label_controls"])+len(report["noncommuting_native_label_controls"]),
                      "native_decoder_supplied": False}, indent=2))


if __name__ == "__main__":
    main()
