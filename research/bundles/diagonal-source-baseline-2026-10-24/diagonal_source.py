"""Sample-only diagonal-source reduction; no general group solver is implemented.

The sampling stage never receives probabilities or an explicit support list.
Its promise-dependent output is a small colored-set instance for the cited
classical matrix-group algorithm, not a recovered subgroup or quantum result.
"""
from collections import Counter
from fractions import Fraction as F
from math import ceil


def positive_integer(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def probability(value, name):
    if not isinstance(value, (int, F)) or isinstance(value, bool) or not 0 < value <= 1:
        raise ValueError(f"{name} must be an exact rational in (0,1]")
    return F(value)


def sampling_plan(rank_cap, orbit_gap, failure_probability):
    positive_integer(rank_cap, "rank cap")
    delta = probability(orbit_gap, "orbit gap")
    eta = probability(failure_probability, "failure probability")
    e = delta/(16*rank_cap*(rank_cap+1))
    logarithm = (ceil(2*rank_cap/eta)-1).bit_length()
    count = ceil(F(logarithm, 2)/(e*e))
    return {"rank_cap": rank_cap, "orbit_gap": delta, "failure_probability": eta,
            "frequency_error": e, "sample_count": count,
            "logarithm_upper": logarithm,
            "trace_norm_loss_upper": 2*rank_cap*(rank_cap+1)*e,
            "no_minimum_weight_or_weight_separation": True,
            "rank_gap_diagonality_iid_are_unverified_promises": True,
            "ambient_basis_not_enumerated": True,
            "group_backend_executed": False, "quantum_speedup_claim": False}


def coarsen_histogram(counts, rank_cap, frequency_error):
    """Exact interval-chain coarsening, conditional on the frequency event."""
    positive_integer(rank_cap, "rank cap")
    e = probability(frequency_error, "frequency error")
    if not counts or len(counts) > rank_cap:
        raise ValueError("nonempty histogram respecting rank cap required")
    dimension = None
    for point, count in counts.items():
        if not isinstance(point, tuple) or not point or any(type(x) is not int or x < 0 for x in point):
            raise ValueError("labels must be nonempty tuples of nonnegative integers")
        if dimension is None:
            dimension = len(point)
        if len(point) != dimension:
            raise ValueError("label dimensions differ")
        positive_integer(count, "histogram count")
    total = sum(counts.values())
    ordered = sorted((F(count, total), point) for point, count in counts.items())
    clusters = [[(F(0), None)]]  # The zero-frequency component includes unseen labels.
    for entry in ordered:
        if entry[0]-clusters[-1][-1][0] <= 2*e:
            clusters[-1].append(entry)
        else:
            clusters.append([entry])
    rows = []
    for color, cluster in enumerate(clusters[1:]):
        value = cluster[0][0]-e
        for _, point in cluster:
            rows.append({"point": list(point), "color": color, "value": value})
    return {"status": "COARSENED_SET_CONDITIONAL_ON_UNIFORM_FREQUENCY_EVENT",
            "rows": rows, "color_count": len(clusters)-1,
            "discarded_observed_labels": [list(p) for _, p in clusters[0] if p is not None],
            "observed_labels": len(counts), "sample_count": total,
            "frequency_error": e, "rank_cap": rank_cap,
            "trace_norm_loss_upper": 2*rank_cap*(rank_cap+1)*e,
            "group_backend_executed": False}


def sample_source(sampler, *, rank_cap, orbit_gap, failure_probability,
                  dimension, field_prime, sample_budget):
    """Collect IID classical labels with an explicit cap, then form the set.

    Primality and the source promises are input contracts, not inferred from
    observations. A budget shortfall fails before requesting any samples.
    """
    positive_integer(dimension, "dimension")
    positive_integer(field_prime, "field characteristic")
    if field_prime < 2:
        raise ValueError("field characteristic must be at least two")
    positive_integer(sample_budget, "sample budget")
    plan = sampling_plan(rank_cap, orbit_gap, failure_probability)
    if sample_budget < plan["sample_count"]:
        raise ValueError("sample budget is below the proved schedule")
    counts = Counter()
    for _ in range(plan["sample_count"]):
        point = sampler()
        if (not isinstance(point, tuple) or len(point) != dimension
                or any(type(x) is not int or not 0 <= x < field_prime for x in point)):
            raise ValueError("source returned a noncanonical finite-field label")
        counts[point] += 1
        if len(counts) > rank_cap:
            raise ValueError("observed support already contradicts rank cap")
    return {"status": "SAMPLED_COLORED_SET_NOT_SUBGROUP_BACKEND",
            "plan": plan,
            "coarsening": coarsen_histogram(counts, rank_cap, plan["frequency_error"]),
            "histogram": [{"point": list(p), "count": n} for p, n in sorted(counts.items())],
            "quantum_execution": False, "subgroup_recovered": False}


def colored_points(coarsening):
    colors = coarsening["color_count"]
    return tuple(tuple(row["point"])+(1,)+tuple(int(j == row["color"]) for j in range(colors))
                 for row in coarsening["rows"])


def lift_affine(matrix, translation, color_count, field_prime):
    """Homogeneous affine action plus fixed one-hot color coordinates.

    Invertibility, primality, and the generated group's p-group contract are
    not certified here. Individual unipotent generators alone do not certify
    that their generated group is a p-group.
    """
    positive_integer(field_prime, "field characteristic")
    if field_prime < 2 or type(color_count) is not int or color_count < 0:
        raise ValueError("invalid field or color count")
    n = len(translation)
    if n == 0 or len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("square affine matrix and matching translation required")
    if any(type(x) is not int or not 0 <= x < field_prime for row in matrix for x in row):
        raise ValueError("noncanonical matrix entry")
    if any(type(x) is not int or not 0 <= x < field_prime for x in translation):
        raise ValueError("noncanonical translation entry")
    size = n+1+color_count
    result = [[0]*size for _ in range(size)]
    for i in range(n):
        result[i][:n] = matrix[i]
        result[i][n] = translation[i]
    for i in range(n, size):
        result[i][i] = 1
    return tuple(tuple(row) for row in result)


def apply_matrix(matrix, point, field_prime):
    if len(matrix) != len(point) or any(len(row) != len(point) for row in matrix):
        raise ValueError("matrix/point dimensions differ")
    return tuple(sum(a*x for a, x in zip(row, point)) % field_prime for row in matrix)
