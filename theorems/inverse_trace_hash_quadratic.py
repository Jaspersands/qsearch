"""Exact degree-two row-span diagnostic on a supplied native hash cell.

Only a verified combination equal to 1 certifies emptiness. A dual certificate
certifies feasibility only for formal monomials, not native SAT, a witness,
a cell count, a degree bound, or hardness evidence.
No field enumeration, polynomial multiplication closure, or Groebner engine.
"""

from collections.abc import Sequence
import hashlib
from pathlib import Path
from time import perf_counter
import json

from theorems.balanced_codeword_filter import integer, trace_mask
from theorems.explicit_quadratic_opi import element, encoded
from theorems.inverse_trace_algebraic_audit import compiled_relations
from theorems.inverse_trace_quadratic_closure import set_bits
from theorems.inverse_trace_smt import validate_instance, vandermonde_eliminate_residual
from theorems.parity_block_usd_prange import affine_system


IDENTITIES = ("x2_y_plus_x", "x_y2_plus_y", "x4_y_plus_x3",
              "x_y4_plus_y3", "x2_y2_plus_xy")
SOURCE_FILES = ("inverse_trace_hash_quadratic.py", "inverse_trace_algebraic_audit.py",
                "inverse_trace_quadratic_closure.py", "inverse_trace_smt.py",
                "parity_block_usd_prange.py", "balanced_codeword_filter.py",
                "explicit_quadratic_opi.py")


class _Cap(Exception):
    pass


def _json_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def _ordered(values, name):
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise ValueError(f"{name} must be an ordered sequence")
    return tuple(values)


def _inputs(instance, indices, target_syndrome, hash_rows, hash_rhs):
    bits, points, targets, checks = validate_instance(instance)
    indices = _ordered(indices, "residual indices")
    integer(len(indices), checks, len(points), "residual coordinate count")
    for i in indices:
        integer(i, 0, len(points)-1, "residual index")
    if len(set(indices)) != len(indices):
        raise ValueError("distinct residual indices required")
    h = _ordered(target_syndrome, "target syndrome")
    if len(h) != checks:
        raise ValueError("target syndrome must have exactly K field elements")
    for value in h:
        integer(value, 0, (1 << bits)-1, "syndrome field element")
    width = (bits-1)*(len(indices)-checks)
    rows = _ordered(hash_rows, "hash rows")
    for row in rows:
        integer(row, 0, (1 << width)-1, "hash row")
    integer(hash_rhs, 0, (1 << len(rows))-1, "hash rhs")
    public = {"bits": bits, "points": list(points), "targets": list(targets), "checks": checks,
              "field_modulus_coefficients": list(instance["field_modulus_coefficients"])}
    data = {"instance": public, "residual_indices": list(indices), "residual_syndrome": list(h),
            "hash_rows": list(rows), "hash_rhs": hash_rhs}
    return {**data, "B": width, "instance_sha256": _json_hash(public), "cell_sha256": _json_hash(data)}


def _hash_affine(data):
    width = data["B"]
    system = affine_system([(a, (data["hash_rhs"] >> j) & 1)
                            for j, a in enumerate(data["hash_rows"])], max(1, width))
    if width == 0:
        system = {**system, "rref": [row[1:] for row in system["rref"]], "pivots": [], "free": []}
    return {**system, "rref": [list(row) for row in system["rref"]],
            "pivots": list(system["pivots"]), "free": list(system["free"])}


def _tick(deadline, stage):
    if perf_counter() >= deadline:
        raise _Cap("timeout_" + stage)


def _affine_product(a, b, variables):
    """Boolean affine product: diagonal z_i*z_i reduces to z_i."""
    left, right = a >> 1, b >> 1
    linear = (right if a & 1 else 0) ^ (left if b & 1 else 0) ^ (left & right)
    result = (a & b & 1) | (linear << 1)
    for i in set_bits(left | right):
        upper = ((right if (left >> i) & 1 else 0) ^
                 (left if (right >> i) & 1 else 0)) >> (i+1)
        start = 1 + variables + i*(2*variables-i-1)//2
        result ^= upper << start
    return result


def _build_maps(data, system, tick):
    bits, checks = data["instance"]["bits"], data["instance"]["checks"]
    indices, points, targets = data["residual_indices"], data["instance"]["points"], data["instance"]["targets"]
    tick("affine_setup")
    pivots, free, constants, coefficients = vandermonde_eliminate_residual(
        bits, points, indices, data["residual_syndrome"], checks)
    tick("affine_setup")
    mask = trace_mask(bits, 1)
    c = mask & -mask
    positions = [j for j in range(bits) if 1 << j != c]
    basis = [(1 << j) ^ (c if (mask >> j) & 1 else 0) for j in positions]
    order, x_free = [], []
    for i in free:
        x_free.append([1 << (len(order)+j+1) for j in range(bits)])
        order.extend({"kind": "x_free", "coordinate": i, "bit": j} for j in range(bits))
    u = [0]*data["B"]
    for j in system["free"]:
        u[j] = 1 << (len(order)+1)
        order.append({"kind": "u_free", "u_bit": j})
    for row in system["rref"]:
        if any(row[:-1]):
            pivot = next(j for j, value in enumerate(row[:-1]) if value)
            u[pivot] = row[-1]
            for j in system["free"]:
                if row[j]:
                    u[pivot] ^= u[j]
    y_piv = []
    for i in pivots:
        tick("affine_setup")
        local = [1 << (len(order)+j+1) for j in range(bits-1)]
        order.extend({"kind": "y_pivot", "coordinate": i, "basis_index": j} for j in range(bits-1))
        y_piv.append(_trace_affine(bits, targets[i], c, basis, local))
    y_free = [_trace_affine(bits, targets[i], c, basis, u[s*(bits-1):(s+1)*(bits-1)])
              for s, i in enumerate(free)]
    x_piv = []
    for constant, row in zip(constants, coefficients):
        tick("affine_setup")
        word = [(constant >> j) & 1 for j in range(bits)]
        for a, x in zip(row, x_free):
            coefficient = element(bits, a)
            for j, expr in enumerate(x):
                product = encoded(coefficient*element(bits, 1 << j))
                for k in set_bits(product):
                    word[k] ^= expr
        x_piv.append(word)
    return {"x": x_piv+x_free, "y": y_piv+y_free, "u": u, "variable_order": order,
            "trace_mask": mask, "trace_one": c, "trace_kernel_basis": basis,
            "trace_free_bit_positions": positions, "pivot_indices": list(pivots), "free_indices": list(free),
            "pivot_constants": list(constants), "pivot_coefficients": [list(row) for row in coefficients]}


def _trace_affine(bits, target, c, basis, coordinates):
    result = [(target*c >> j) & 1 for j in range(bits)]
    for vector, expr in zip(basis, coordinates):
        for j in set_bits(vector):
            result[j] ^= expr
    return result


def _maps_receipt(model):
    return {**{key: value for key, value in model.items() if key not in ("x", "y", "u")},
            "x_bits_hex": [[hex(a) for a in word] for word in model["x"]],
            "y_bits_hex": [[hex(a) for a in word] for word in model["y"]],
            "u_bits_hex": [hex(a) for a in model["u"]],
            "affine_encoding": "bit 0 constant; bit j+1 is variable j"}


def _quadratic_rows(data, model, strengthen, tick):
    bits = data["instance"]["bits"]
    variables = len(model["variable_order"])
    tick("compilation")
    polynomials = list(zip(IDENTITIES, compiled_relations(bits)))
    tick("compilation")
    if strengthen:
        xy = {0: 1}
        for i in range(bits):
            tick("compilation")
            for j in range(bits):
                xy[(1 << i) | (1 << (bits+j))] = encoded(element(bits, 1 << i)*element(bits, 1 << j))
        polynomials.append(("xy_plus_one", xy))
    for index, x, y in zip(data["residual_indices"], model["x"], model["y"]):
        local, cache = x+y, {0: 1}
        cache.update({1 << j: a for j, a in enumerate(local)})
        for identity, polynomial in polynomials:
            if identity == "xy_plus_one" and data["instance"]["targets"][index] == 0:
                continue
            tick("compilation")
            components = [0]*bits
            for counter, (monomial, coefficient) in enumerate(polynomial.items()):
                if counter % 32 == 0:
                    tick("compilation")
                if monomial not in cache:
                    i, j = tuple(set_bits(monomial))
                    cache[monomial] = _affine_product(local[i], local[j], variables)
                for component in set_bits(coefficient):
                    components[component] ^= cache[monomial]
            for component, row in enumerate(components):
                yield {"coordinate": index, "identity": identity, "component": component}, row


def _raw_hash_rows(data):
    for j, row in enumerate(data["hash_rows"]):
        yield {"hash_row": j}, (row << 1) | ((data["hash_rhs"] >> j) & 1)


def _insert(row, index, basis, metrics, tick):
    combination = 1 << index
    while row:
        pivot = row.bit_length()-1
        if pivot not in basis:
            basis[pivot] = (row, combination)
            return
        previous, proof = basis[pivot]
        row ^= previous
        combination ^= proof
        metrics["elimination_xors"] += 1
        if metrics["elimination_xors"] % 32 == 0 and row not in (0, 1):
            tick("elimination")


def _row_digest(columns):
    digest = hashlib.sha256()
    digest.update(f"columns={columns};little_endian_fixed_width;".encode())
    return digest


def verify_certificate(report, certificate=None):
    """Rebuild source rows and replay XOR; do not trust the elimination basis.

    Replay is deliberately not truncated by the diagnostic timeout. Its full
    cost is charged by analyze_cell; this is not hard-preemptible execution.
    """
    try:
        cert = report["certificate"] if certificate is None else certificate
        if not isinstance(cert, dict):
            return False
        data = _inputs(report["instance"], report["residual_indices"], report["residual_syndrome"],
                       report["hash_rows"], report["hash_rhs"])
        if (cert["cell_sha256"] != data["cell_sha256"] or report["cell_sha256"] != data["cell_sha256"]
                or report["instance_sha256"] != data["instance_sha256"] or cert["xor_hex"] != "0x1"):
            return False
        indices = cert["row_indices"]
        if (not isinstance(indices, list) or not indices or any(type(i) is not int or i < 0 for i in indices)
                or indices != sorted(set(indices))):
            return False
        columns, count = report["row_span_columns"], report["compiled_row_count"]
        integer(count, 1, 100_000, "compiled row count")
        if indices[-1] >= count:
            return False
        if cert["kind"] == "raw_hash_affine":
            if columns != data["B"]+1 or count > len(data["hash_rows"]):
                return False
            rows = iter(_raw_hash_rows(data))
        elif cert["kind"] == "quadratic_row_span":
            strengthen = report["strengthen_target_one"]
            if type(strengthen) is not bool:
                return False
            system = _hash_affine(data)
            if not system["consistent"]:
                return False
            n, k, m = data["instance"]["bits"], data["instance"]["checks"], len(data["residual_indices"])
            variables = n*(m-k)+data["B"]-system["rank"]+k*(n-1)
            expected_columns = 1+variables+variables*(variables-1)//2
            integer(report["max_monomials"], 1, 1_000_000, "monomial cap")
            if columns != expected_columns or columns > report["max_monomials"]:
                return False
            model = _build_maps(data, system, lambda stage: None)
            if _maps_receipt(model) != report["affine_maps"]:
                return False
            rows = iter(_quadratic_rows(data, model, strengthen, lambda stage: None))
        else:
            return False
        digest, selected, identifiers, total = _row_digest(columns), set(indices), [], 0
        for j in range(count):
            identifier, row = next(rows)
            identifiers.append(identifier)
            digest.update(row.to_bytes((columns+7)//8, "little"))
            if j in selected:
                total ^= row
        return (total == 1 and digest.hexdigest() == report["rows_sha256"]
                and _json_hash(identifiers) == _json_hash(report["row_ids"])
                and _json_hash([identifiers[j] for j in indices]) == _json_hash(cert["row_ids"]))
    except (KeyError, ValueError, TypeError, IndexError, AttributeError, StopIteration, OverflowError):
        return False


def verify_relaxation_certificate(report, certificate=None):
    """Replay ALL expected rows against a formal monomial assignment w.

    Require w[0]=1 and row.w=0 throughout. Pair coordinates need not equal
    products of linear coordinates; this is not a native assignment. No rank
    or triangular basis is trusted. Replay is not deadline-truncated.
    """
    try:
        cert = report["relaxation_certificate"] if certificate is None else certificate
        if (not isinstance(cert, dict) or cert["kind"] != "quadratic_dual_relaxation"
                or cert["formal_monomial_assignment_only"] is not True
                or report["row_span_kind"] != "quadratic_row_span"
                or report["row_span_complete"] is not True
                or report["stop_reason"] != "all_rows_processed"):
            return False
        data = _inputs(report["instance"], report["residual_indices"], report["residual_syndrome"],
                       report["hash_rows"], report["hash_rhs"])
        if (cert["cell_sha256"] != data["cell_sha256"] or report["cell_sha256"] != data["cell_sha256"]
                or report["instance_sha256"] != data["instance_sha256"]):
            return False
        strengthen = report["strengthen_target_one"]
        if type(strengthen) is not bool:
            return False
        system = _hash_affine(data)
        if not system["consistent"]:
            return False
        n, k, m = data["instance"]["bits"], data["instance"]["checks"], len(data["residual_indices"])
        variables = n*(m-k)+data["B"]-system["rank"]+k*(n-1)
        columns = 1+variables+variables*(variables-1)//2
        expected = n*(5*m + (sum(data["instance"]["targets"][i] for i in data["residual_indices"])
                            if strengthen else 0))
        integer(report["max_monomials"], 1, 1_000_000, "monomial cap")
        integer(report["max_rows"], 1, 100_000, "row cap")
        if columns > report["max_monomials"] or expected > report["max_rows"]:
            return False
        counts = [report[key] for key in ("expected_row_count", "compiled_row_count",
                  "processed_row_count", "polynomial_rows_raw", "polynomial_rows_processed")]
        counts.append(cert["row_count"])
        widths = [report["row_span_columns"], report["monomial_columns"], cert["width"]]
        if (any(type(count) is not int or count != expected for count in counts)
                or any(type(width) is not int or width != columns for width in widths)):
            return False
        text = cert["w_hex"]
        if type(text) is not str or len(text) > 2+(columns+3)//4:
            return False
        w = int(text, 16)
        if w < 0 or w.bit_length() > columns or not w & 1 or hex(w) != text:
            return False
        model = _build_maps(data, system, lambda stage: None)
        if _maps_receipt(model) != report["affine_maps"]:
            return False
        digest, identifiers = _row_digest(columns), []
        for identifier, row in _quadratic_rows(data, model, strengthen, lambda stage: None):
            if len(identifiers) >= expected or (row & w).bit_count() & 1:
                return False
            identifiers.append(identifier)
            digest.update(row.to_bytes((columns+7)//8, "little"))
        return (len(identifiers) == expected and digest.hexdigest() == report["rows_sha256"]
                and _json_hash(identifiers) == _json_hash(report["row_ids"]))
    except (KeyError, ValueError, TypeError, IndexError, AttributeError, OverflowError):
        return False


def analyze_cell(instance, indices, target_syndrome, hash_rows, hash_rhs, *,
                 timeout_ms=30_000, max_monomials=300_000, max_rows=10_000,
                 strengthen_target_one=True):
    """Test whether 1 lies in the substituted degree-two Boolean row span.

    Variables are n*r raw x_free bits, B-rank(M) accepted-root hash-kernel
    bits, and K*(n-1) pivot trace coordinates, in that order. Hash coordinates
    use the same lowest-trace-pivot, ascending-basis, coordinate-major encoding
    as enumerate_cell. Full row rank gives n*m variables when k=B-K.

    All five compiled field identities are retained, including zero rows.
    Optional xy+1 is added only at target-one coordinates. Polynomial columns
    are constant, linear variables, then pairs (i,j), i<j in lexicographic order.
    Rows are fingerprinted, not serialized as a potentially huge dense matrix.
    Certificates retain original coordinate/identity/component IDs and are
    independently replayed from the saved input by verify_certificate.
    A fully processed span without 1 receives a separately replayed dual
    relaxation certificate: a formal monomial vector w with w[0]=1 and every
    source row orthogonal to w. It does not assign consistent native products.

    timeout_ms starts at entry. Setup calls and individual operations cannot
    be preempted; cooperative checks occur during map/row construction and
    elimination. Certificate replay may exceed the deadline. UNKNOWN_CAP means
    incomplete work unless a verified unit certificate already proves emptiness.
    max_rows bounds compiled rows; row_rank is for the fully processed prefix.
    """
    start = perf_counter()
    integer(timeout_ms, 1, 600_000, "cooperative timeout milliseconds")
    integer(max_monomials, 1, 1_000_000, "monomial column cap")
    integer(max_rows, 1, 100_000, "polynomial row cap")
    if type(strengthen_target_one) is not bool:
        raise ValueError("strengthen_target_one must be a boolean")
    deadline = start+timeout_ms/1000
    tick = lambda stage: _tick(deadline, stage)
    data = _inputs(instance, indices, target_syndrome, hash_rows, hash_rhs)
    system = _hash_affine(data)
    n, k, m = data["instance"]["bits"], data["instance"]["checks"], len(data["residual_indices"])
    variables = n*(m-k)+data["B"]-system["rank"]+k*(n-1)
    monomials = 1+variables+variables*(variables-1)//2
    raw_count = n*(5*m + (sum(data["instance"]["targets"][i] for i in data["residual_indices"])
                          if strengthen_target_one else 0))
    affine = not system["consistent"]
    columns = data["B"]+1 if affine else monomials
    expected = len(data["hash_rows"]) if affine else raw_count
    source = Path(__file__).resolve().parent
    fingerprints = {name: hashlib.sha256((source/name).read_bytes()).hexdigest() for name in SOURCE_FILES}
    report = {**data, "status": "UNKNOWN_CAP", "stop_reason": None,
              "native_cell_empty_certified": False, "certificate": None, "certificate_verified": False,
              "relaxation_certificate": None, "quadratic_relaxation_feasible_certified": False,
              "hash_rank": system["rank"], "hash_consistent": system["consistent"], "hash_system": system,
              "variable_count": variables, "monomial_columns": monomials, "affine_maps": None,
              "row_span_kind": "raw_hash_affine" if affine else "quadratic_row_span",
              "row_span_columns": columns, "expected_row_count": expected,
              "polynomial_rows_raw": raw_count, "polynomial_rows_processed": 0,
              "compiled_row_count": 0, "processed_row_count": 0, "nonzero_row_count": 0,
              "row_rank": 0, "row_span_complete": False, "unit_in_row_span": None,
              "row_ids": [], "rows_sha256": None, "elimination_xors": 0,
              "timeout_ms": timeout_ms, "max_monomials": max_monomials, "max_rows": max_rows,
              "strengthen_target_one": strengthen_target_one,
              "source_sha256": fingerprints[SOURCE_FILES[0]], "source_fingerprints": fingerprints,
              "source_fingerprint_scope": "disk_sources_during_setup_not_loaded_bytecode_attestation",
              "setup_seconds": 0.0, "compilation_seconds": 0.0, "elimination_seconds": 0.0,
              "verification_seconds": 0.0, "total_seconds": 0.0,
              "relaxation_construction_seconds": 0.0, "relaxation_verification_seconds": 0.0,
              "field_enumerated": False, "groebner_basis_computed": False,
              "degree_growth_performed": False, "hardness_evidence": False,
              "polynomial_enumeration_established": False, "uniform_sampler": False,
              "whole_workflow_wall_clock_cap_enforced": False}
    basis, digest, setup_finished = {}, _row_digest(columns), False
    try:
        tick("setup")
        if not affine and monomials > max_monomials:
            raise _Cap("monomial_column_cap")
        if affine:
            rows = iter(_raw_hash_rows(data))
        else:
            model = _build_maps(data, system, tick)
            report["affine_maps"] = _maps_receipt(model)
            rows = iter(_quadratic_rows(data, model, strengthen_target_one, tick))
        report["setup_seconds"] = perf_counter()-start
        setup_finished = True
        while report["compiled_row_count"] < expected:
            if report["compiled_row_count"] >= max_rows:
                raise _Cap("row_cap")
            phase = perf_counter()
            try:
                tick("compilation")
                identifier, row = next(rows)
                digest.update(row.to_bytes((columns+7)//8, "little"))
            finally:
                report["compilation_seconds"] += perf_counter()-phase
            index = report["compiled_row_count"]
            report["compiled_row_count"] += 1
            report["row_ids"].append(identifier)
            report["nonzero_row_count"] += int(bool(row))
            phase = perf_counter()
            try:
                tick("elimination")
                _insert(row, index, basis, report, tick)
            finally:
                report["elimination_seconds"] += perf_counter()-phase
            report["processed_row_count"] += 1
        report["row_span_complete"] = True
        report["stop_reason"] = "all_rows_processed"
    except _Cap as cap:
        report["stop_reason"] = str(cap)
    report["row_rank"] = len(basis)
    report["rows_sha256"] = digest.hexdigest()
    report["polynomial_rows_processed"] = 0 if affine else report["processed_row_count"]
    if not setup_finished:
        report["setup_seconds"] = perf_counter()-start
    if 0 in basis:
        selected = list(set_bits(basis[0][1]))
        report["certificate"] = {"kind": report["row_span_kind"], "cell_sha256": data["cell_sha256"],
                                 "row_indices": selected, "row_ids": [report["row_ids"][j] for j in selected],
                                 "xor_hex": "0x1"}
        phase = perf_counter()
        verified = verify_certificate(report)
        report["verification_seconds"] = perf_counter()-phase
        if not verified:
            raise ArithmeticError("row-combination certificate failed independent replay")
        report.update(status="CERTIFIED_AFFINE_CONTRADICTION" if affine else "CERTIFIED_QUADRATIC_CONTRADICTION",
                      native_cell_empty_certified=True, certificate_verified=True, unit_in_row_span=True)
    elif report["row_span_complete"]:
        if affine:
            raise ArithmeticError("inconsistent raw hash lacked a replayable contradiction")
        phase = perf_counter()
        w = 1
        # Each row's highest bit is its pivot. Ascending pivots fix only later
        # coordinates, leaving every already satisfied triangular row intact.
        for pivot in sorted(basis):
            if (basis[pivot][0] & w).bit_count() & 1:
                w |= 1 << pivot
        report["relaxation_certificate"] = {
            "kind": "quadratic_dual_relaxation", "cell_sha256": data["cell_sha256"],
            "width": columns, "row_count": expected, "w_hex": hex(w),
            "formal_monomial_assignment_only": True}
        report["relaxation_construction_seconds"] = perf_counter()-phase
        phase = perf_counter()
        verified = verify_relaxation_certificate(report)
        report["relaxation_verification_seconds"] = perf_counter()-phase
        report["verification_seconds"] += report["relaxation_verification_seconds"]
        if not verified:
            raise ArithmeticError("dual relaxation certificate failed full independent replay")
        report.update(status="INCONCLUSIVE_QUADRATIC_RELAXATION", unit_in_row_span=False,
                      quadratic_relaxation_feasible_certified=True)
    report["total_seconds"] = perf_counter()-start
    return report
