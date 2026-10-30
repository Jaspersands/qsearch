"""Bounded exact public-matrix Hasse-jet controls, not asymptotic GIJS claims.

Generator columns are the supplied points, without a row-basis change. Rows
of E are squarefree degree-d monomials; columns are jets at nonheld-out
points. Only the held-out evaluation, not its whole jet, is tested.
"""

from __future__ import annotations

from itertools import combinations, product
from math import comb
from numbers import Integral
import random

import numpy as np

from theorems.code_syzygy_invariants import gf2_bit_rank, gf2_kernel_from_columns


SCOPE = "Finite exact algebraic controls; not validation of asymptotic GIJS or a quantum claim."
RATIONAL_MAX_MONOMIALS = 256
RATIONAL_MAX_ENTRIES = 30_000
TRANSPOSE_MAX_MONOMIALS = 512
TRANSPOSE_MAX_ENTRIES = 100_000


def _integer(value, name, minimum=0):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral):
        raise TypeError(f"{name} must be an integer, not a Boolean or coercible value")
    value = int(value)
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _parameters(degree, multiplicity):
    degree = _integer(degree, "degree", 1)
    multiplicity = _integer(multiplicity, "multiplicity", 1)
    if degree <= multiplicity:
        raise ValueError("require degree > multiplicity >= 1")
    return degree, multiplicity


def reduced_derivative_orders(d, s):
    """Orders retained by the lowbit GF(2) reduction, not an independent basis.

    For order r, the smallest positive t with odd binom(d-r, t) is
    lowbit(d-r). The same-point Hasse identity eliminates r if r+t < s.
    This preserves the span without asserting independence of retained jets.
    This characteristic-two reduction must not be used for rational ranks.
    """
    d, s = _parameters(d, s)
    return [r for r in range(s) if r + ((d - r) & -(d - r)) >= s]


def _binary_rows(generator):
    if not isinstance(generator, (list, tuple, np.ndarray)):
        raise TypeError("generator must be a rectangular list, tuple, or array of binary rows")
    if isinstance(generator, np.ndarray) and generator.ndim != 2:
        raise ValueError("generator must be two-dimensional")
    if len(generator) == 0:
        raise ValueError("generator must have at least one row")
    rows = []
    for row in generator:
        if not isinstance(row, (list, tuple, np.ndarray)):
            raise TypeError("each generator row must be a sequence")
        if isinstance(row, np.ndarray) and row.ndim != 1:
            raise ValueError("each generator row must be one-dimensional")
        values = []
        for bit in row:
            bit = _integer(bit, "generator entry")
            if bit not in (0, 1):
                raise ValueError("generator entries must be exactly 0 or 1")
            values.append(bit)
        if not values or (rows and len(values) != len(rows[0])):
            raise ValueError("generator must have nonempty, equally sized rows")
        rows.append(tuple(values))
    return tuple(rows)


def _mask(indices):
    return sum(1 << i for i in indices)


def _jet_column(monomial_masks, point, derivative):
    value = 0
    for index, monomial in enumerate(monomial_masks):
        if derivative & monomial == derivative:
            remaining = monomial ^ derivative
            if remaining & point == remaining:
                value |= 1 << index
    return value


def _dot(left, right):
    return (left & right).bit_count() & 1


def _span_witness(columns, target, row_count):
    # Track only pivot combinations, avoiding a quadratic list of dependencies.
    pivots = {}
    for index, column in enumerate(columns):
        value, coefficients = column, 1 << index
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (value, coefficients)
                break
            old_value, old_coefficients = pivots[pivot]
            value ^= old_value
            coefficients ^= old_coefficients
    residual, coefficients = target, 0
    for pivot in sorted(pivots, reverse=True):
        if residual >> pivot & 1:
            value, combination = pivots[pivot]
            residual ^= value
            coefficients ^= combination
    if not residual:
        image = 0
        for index, column in enumerate(columns):
            if coefficients >> index & 1:
                image ^= column
        if image != target:
            raise ArithmeticError("span witness verification failed")
        witness = {
            "kind": "span_coefficients",
            "coefficients": [(coefficients >> i) & 1 for i in range(len(columns))],
            "nonzero_indices": [i for i in range(len(columns)) if coefficients >> i & 1],
            "verified": True,
        }
    else:
        # Extend a functional on the nonpivot residual to annihilate every pivot.
        annihilator = 1 << (residual.bit_length() - 1)
        for pivot in sorted(pivots):
            if _dot(pivots[pivot][0], annihilator):
                annihilator ^= 1 << pivot
        if any(_dot(c, annihilator) for c in columns) or _dot(target, annihilator) != 1:
            raise ArithmeticError("annihilator verification failed")
        witness = {
            "kind": "separating_annihilator",
            "annihilator": [(annihilator >> i) & 1 for i in range(row_count)],
            "packed_annihilator": annihilator,
            "training_pairings_zero": True,
            "target_pairing": 1,
            "verified": True,
        }
    return len(pivots), int(bool(residual)), witness


def _transpose_check(columns, target, row_count, rank, delta, entries):
    if row_count > TRANSPOSE_MAX_MONOMIALS or entries > TRANSPOSE_MAX_ENTRIES:
        return {"status": "skipped_cap", "reason": "independent transpose-kernel cross-check cap"}
    transpose_columns = tuple(
        sum(((column >> row) & 1) << col for col, column in enumerate(columns))
        for row in range(row_count)
    )
    transpose_rank, kernel = gf2_kernel_from_columns(transpose_columns)
    heldout_image_rank = int(any(_dot(target, h) for h in kernel))
    if (transpose_rank != rank or len(kernel) != row_count - rank
            or heldout_image_rank != delta
            or any(_dot(column, h) for h in kernel for column in columns)):
        raise ArithmeticError("transpose-kernel duality cross-check failed")
    return {
        "status": "checked",
        "rank": transpose_rank,
        "annihilator_dimension": len(kernel),
        "heldout_image_rank": heldout_image_rank,
        "membership_matches": True,
    }


def _rational_ranks(columns, target, row_count):
    from sympy import Matrix
    from sympy.polys.domains import QQ
    from sympy.polys.matrices import DomainMatrix

    matrix = Matrix(row_count, len(columns), lambda i, j: (columns[j] >> i) & 1)
    augmented = matrix.row_join(Matrix([(target >> i) & 1 for i in range(row_count)]))
    rank = int(DomainMatrix.from_Matrix(matrix).convert_to(QQ).rank())
    augmented_rank = int(DomainMatrix.from_Matrix(augmented).convert_to(QQ).rank())
    return {
        "requested": True,
        "operator": "full_hasse",
        "field": "Q; identical ranks over R and C for this integer matrix",
        "exact": True,
        "rank": rank,
        "augmented_rank": augmented_rank,
        "delta": augmented_rank - rank,
        "member": augmented_rank == rank,
    }


def analyze(generator, degree, multiplicity, holdout, *, rational=False,
            max_monomials=4096, max_entries=1000000, reduced=False):
    """Return a JSON-serializable exact held-out evaluation membership audit.

    No file writes, hidden support, row reduction of the supplied points, or
    numerical singular-value thresholds are used. Caps count E plus its one
    target column and are checked before monomial/derivative expansion.
    Rank-deficient public generators are allowed and explicitly reported.
    """
    degree, multiplicity = _parameters(degree, multiplicity)
    holdout = _integer(holdout, "holdout")
    max_monomials = _integer(max_monomials, "max_monomials", 1)
    max_entries = _integer(max_entries, "max_entries", 1)
    if type(rational) is not bool or type(reduced) is not bool:
        raise TypeError("rational and reduced must be Booleans")
    if rational and reduced:
        raise ValueError("rational ranks require the full operator; reduced jets are GF(2)-only")
    rows = _binary_rows(generator)
    k, n = len(rows), len(rows[0])
    if degree > k:
        raise ValueError("degree must not exceed the number of generator rows")
    if holdout >= n:
        raise ValueError("holdout point index is out of range")
    monomial_count = comb(k, degree)
    if monomial_count > max_monomials:
        raise ValueError(f"monomial cap exceeded: {monomial_count} > {max_monomials}")
    orders = reduced_derivative_orders(degree, multiplicity) if reduced else list(range(multiplicity))
    jets_per_point = sum(comb(k, order) for order in orders)
    full_jets_per_point = sum(comb(k, order) for order in range(multiplicity))
    column_count = (n - 1) * jets_per_point
    entries = monomial_count * (column_count + 1)
    if entries > max_entries:
        raise ValueError(f"entry cap exceeded (E plus target): {entries} > {max_entries}")
    if rational and (monomial_count > RATIONAL_MAX_MONOMIALS or entries > RATIONAL_MAX_ENTRIES):
        raise ValueError("exact rational cap exceeded: at most 256 monomials and 30000 entries")

    monomials = list(combinations(range(k), degree))
    monomial_masks = [_mask(monomial) for monomial in monomials]
    points = [sum(rows[i][j] << i for i in range(k)) for j in range(n)]
    columns, labels = [], []
    for point_index, point in enumerate(points):
        if point_index == holdout:
            continue
        for order in orders:
            for derivative in combinations(range(k), order):
                labels.append({"point": point_index, "derivative": list(derivative)})
                columns.append(_jet_column(monomial_masks, point, _mask(derivative)))
    target = _jet_column(monomial_masks, points[holdout], 0)
    rank, delta, witness = _span_witness(columns, target, monomial_count)
    if rank != gf2_bit_rank(columns) or rank + delta != gf2_bit_rank((*columns, target)):
        raise ArithmeticError("packed rank cross-check failed")
    generator_rank = gf2_bit_rank(points)
    rational_result = _rational_ranks(columns, target, monomial_count) if rational else {"requested": False}
    return {
        "scope": SCOPE,
        "asymptotic_gijs_validated": False,
        "quantum_claim": False,
        "speedup_claim_allowed": False,
        "accepted_candidate": False,
        "generator": {
            "rows": k, "columns": n, "rank_gf2": generator_rank,
            "full_row_rank": generator_rank == k, "basis_changed": False,
        },
        "degree": degree,
        "multiplicity": multiplicity,
        "holdout": holdout,
        "operator": "reduced_hasse_gf2" if reduced else "full_hasse",
        "derivative_orders": orders,
        "test_operator": "evaluation_only",
        "monomials": [list(monomial) for monomial in monomials],
        "training_columns": labels,
        "packed_training_columns": columns,
        "packed_target": target,
        "dimensions": {
            "monomials": monomial_count, "training_columns": column_count,
            "jets_per_point": jets_per_point, "full_jets_per_point": full_jets_per_point,
            "heldout_points_in_training": 0, "omitted_full_heldout_jets": full_jets_per_point,
            "entries_including_target": entries,
        },
        "gf2": {
            "rank": rank, "augmented_rank": rank + delta, "delta": delta,
            "member": delta == 0, "saturated": rank == monomial_count,
            "target_zero": target == 0, "witness": witness,
        },
        "transpose_crosscheck": _transpose_check(columns, target, monomial_count, rank, delta, entries),
        "rational": rational_result,
        "field_membership_disagrees": (rational_result["member"] != (delta == 0)) if rational else None,
    }


def _rows_from_points(points):
    return [list(row) for row in zip(*points)]


def report():
    """Deterministic bounded controls; returns data without writing any artifacts."""
    controls = []

    def add(name, rows, d, s, holdout, *, rational=False, metadata=None):
        full = analyze(rows, d, s, holdout, rational=rational)
        reduced = analyze(rows, d, s, holdout, reduced=True)
        if (full["gf2"]["rank"], full["gf2"]["delta"]) != (reduced["gf2"]["rank"], reduced["gf2"]["delta"]):
            raise ArithmeticError("full/reduced control disagrees")
        controls.append({
            "id": name, "public_generator": rows, "metadata": metadata or {},
            "full": full, "reduced": reduced, "full_reduced_gf2_agree": True,
        })

    add("separating_evaluation", _rows_from_points([(1, 0, 0), (0, 1, 0), (1, 1, 1)]), 3, 2, 2)
    add("zero_target", _rows_from_points([(1, 0, 0), (0, 1, 0), (0, 0, 1)]), 3, 2, 2)
    add("nonsaturated_duplicate", _rows_from_points([(1, 1, 1, 0), (1, 0, 0, 0), (1, 1, 1, 0)]), 3, 1, 2)
    add("saturated_evaluation_space", _rows_from_points([(1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]), 2, 1, 3)

    points = [tuple(int(i == j) for i in range(6)) for j in range(6)]
    points += [(0, 0, 1, 1, 1, 0), (1, 1, 0, 0, 1, 0), (1, 1, 1, 1, 0, 0)]
    add("binary_membership_not_complex_membership", _rows_from_points(points), 3, 2, 8,
        rational=True, metadata={"goppa_instance": False, "general_no_go": False,
                                 "purpose": "Exact characteristic-change counterexample with d > s."})

    from theorems.goppa_code_search import GF2m, goppa_generator, rootless_on_full_support

    field = GF2m(4)
    coefficients = next(c for c in product(range(field.size), repeat=2) if rootless_on_full_support(field, c))
    goppa = goppa_generator(field, coefficients).tolist()
    add("binary_goppa_t2", goppa, 3, 2, len(goppa[0]) - 1,
        metadata={"goppa_instance": True, "field_degree": 4, "goppa_degree": 2,
                  "rootless_quadratic_is_irreducible": True,
                  "interpolation_lhs": 2 * (len(goppa[0]) - 1),
                  "interpolation_rhs": 3 * (len(goppa[0]) - 5),
                  "sufficient_interpolation_holds": 2 * (len(goppa[0]) - 1) > 3 * (len(goppa[0]) - 5),
                  "observer_input": "public generator only"})
    k, n = len(goppa), len(goppa[0])
    rng = random.Random(1630)
    for _ in range(100):
        random_rows = [[rng.randrange(2) for _ in range(n)] for _ in range(k)]
        if gf2_bit_rank(_mask(i for i in range(k) if random_rows[i][j]) for j in range(n)) == k:
            break
    else:
        raise ArithmeticError("bounded matched full-rank random sampling failed")
    add("matched_random_public_matrix", random_rows, 3, 2, n - 1,
        metadata={"goppa_instance": False, "seed": 1630, "matched_shape_and_rank": True})
    return {"scope": SCOPE, "asymptotic_gijs_validated": False, "quantum_claim": False,
            "speedup_claim_allowed": False, "accepted_candidate": False,
            "controls": controls}
