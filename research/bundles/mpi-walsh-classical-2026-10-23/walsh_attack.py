"""A bounded, same-instance affine-Walsh classical attack on native MPI."""

import argparse
import ast
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import random
import time

from flint import arb, ctx, fmpz, fq_default_ctx
import numpy as np


REPO = Path('/Users/jaspersands/Desktop/quantum algorithm search')


def load_resident_functions():
    """Load exactly named, unchanged definitions without broad repository imports."""
    namespace = {"lru_cache": lru_cache, "fmpz": fmpz, "fq_default_ctx": fq_default_ctx,
                 "np": np, "math": math}
    paths = {
        REPO/'theorems/explicit_quadratic_opi.py': {"field", "element", "encoded"},
        REPO/'theorems/balanced_signed_mpi.py': {
            "presentation", "points", "walsh", "trace_indices", "log_cauchy_product",
            "fast_public_matvec", "fft_line_search"},
    }
    hashes = {}
    for path, names in paths.items():
        source = path.read_text()
        tree = ast.parse(source, filename=str(path))
        nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
        if {node.name for node in nodes} != names:
            raise RuntimeError("source dependency definitions changed")
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), namespace)
        hashes[str(path)] = hashlib.sha256(source.encode()).hexdigest()
    return namespace, hashes


def dyadic_partition(start, stop):
    if type(start) is not int or type(stop) is not int or not 0 <= start < stop:
        raise ValueError("nonempty nonnegative integer interval required")
    blocks = []
    while start < stop:
        size = 1 << ((stop-start).bit_length()-1) if start == 0 else start & -start
        while size > stop-start:
            size //= 2
        blocks.append((start, size))
        start += size
    return blocks


def walsh_rows(array, modulus):
    array = np.asarray(array)
    if (array.ndim != 2 or array.shape[1] < 1
            or array.shape[1] & (array.shape[1]-1)
            or array.dtype.kind not in 'iu' or type(modulus) is not int
            or not 3 <= modulus <= 65535):
        raise ValueError("integer matrix with power-of-two width and bounded odd modulus required")
    if modulus % 2 == 0:
        raise ValueError("Walsh basis needs a unit power of two modulo the order")
    result = array.astype(np.int64, copy=True) % modulus
    step = 1
    while step < result.shape[1]:
        for start in range(0, result.shape[1], 2*step):
            left = result[:, start:start+step].copy()
            right = result[:, start+step:start+2*step].copy()
            result[:, start:start+step] = (left+right) % modulus
            result[:, start+step:start+2*step] = (left-right) % modulus
        step *= 2
    return result


def block_basis(start, stop, modulus):
    blocks = dyadic_partition(start, stop)
    if (stop-start > 2048 or type(modulus) is not int or modulus < 3 or modulus % 2 == 0):
        raise ValueError("bounded dimension and odd modulus required")
    basis = np.zeros((stop-start, stop-start), dtype=np.int64)
    for offset, size in blocks:
        signs = np.array([[1 if (i&j).bit_count() % 2 == 0 else -1
                           for j in range(size)] for i in range(size)], dtype=np.int64)
        index = offset-start
        basis[index:index+size, index:index+size] = signs
        if not np.array_equal((signs @ signs) % modulus, size*np.eye(size, dtype=np.int64) % modulus):
            raise ArithmeticError("Walsh involution failed")
    return basis, blocks


def exact_translation_control(kernel, offset, size, modulus):
    """Check f_s(t+u)=chi_s(u)f_s(t) on the entire ambient binary group."""
    kernel = np.asarray(kernel, dtype=np.int64)
    q = len(kernel)
    if q < 2 or q & (q-1) or size < 1 or size & (size-1) or offset % size or offset+size > q:
        raise ValueError("complete aligned affine block required")
    inputs = np.arange(q, dtype=np.int64)[:, None] ^ np.arange(offset, offset+size, dtype=np.int64)
    phases = walsh_rows(kernel[inputs], modulus)
    checks = 0
    for bit in range(size.bit_length()-1):
        shift = 1 << bit
        signs = np.array([1 if mode & shift == 0 else -1 for mode in range(size)], dtype=np.int64)
        if not np.array_equal(phases[np.arange(q) ^ shift], (phases*signs) % modulus):
            raise ArithmeticError("affine translation covariance failed")
        checks += q*size
    # A few direct sums independently check transform conventions.
    for mode in sorted({0, 1 if size > 1 else 0, size-1}):
        signs = np.array([1 if (u&mode).bit_count() % 2 == 0 else -1 for u in range(size)])
        if not np.array_equal(phases[:, mode], (kernel[inputs] @ signs) % modulus):
            raise ArithmeticError("direct Walsh sum disagrees")
    return phases, checks


def shortest_scalar_move(phases, modulus):
    """Exact exhaustive one-dimensional minimax phase diagnostic, not a CVP oracle."""
    values = np.unique(np.minimum(phases % modulus, (-phases) % modulus))
    best = None
    for start in range(1, modulus, 512):
        scalars = np.arange(start, min(start+512, modulus), dtype=np.int64)
        residues = scalars[:, None]*values % modulus
        maxima = np.minimum(residues, modulus-residues).max(axis=1)
        index = int(np.argmin(maxima))
        item = (int(maxima[index]), int(scalars[index]))
        if best is None or item < best:
            best = item
    return {"min_max_centered_residue": best[0], "displacement": best[1],
            "phase_fraction_of_full_turn": best[0]/modulus,
            "distinct_frequencies_up_to_sign": len(values),
            "nonzero_scalar_trials": modulus-1}


def certified_score(residual, modulus):
    with ctx.workprec(96):
        score = sum(((2*arb.pi()*int(v)/modulus).cos() for v in residual), arb(0))/len(residual)
        return {"arb_interval_96_bits": str(score),
                "score_at_least_0_3_certified": bool(score > arb(3)/10),
                "score_below_0_3_certified": bool(score < arb(3)/10)}


def run():
    started = time.perf_counter()
    dependency, source_hashes = load_resident_functions()
    artifact_path = REPO/'research/phase_workbench/balanced_signed_mpi.json'
    artifact_bytes = artifact_path.read_bytes()
    artifact_document = json.loads(artifact_bytes)
    artifact = artifact_document['matched_classical_portfolio']
    bits, m, n, seed = 13, 6000, 420, 261006753
    if (artifact['bits'], artifact['length'], artifact['evaluations'], artifact['center_seed']) != (bits, m, n, seed):
        raise RuntimeError("frozen native artifact contract changed")
    order = 2**bits-1
    supports, evaluations = dependency['points'](bits, m, n)
    _, logs, generator = dependency['presentation'](bits)
    field_modulus = list(map(int, dependency['field'](bits).modulus().coeffs()))
    saved_input = artifact_document['native_decoder']
    if (field_modulus != saved_input['field_modulus_coefficients']
            or generator != saved_input['generator_encoding']
            or list(supports) != saved_input['support_points']
            or list(evaluations) != saved_input['evaluation_points']):
        raise RuntimeError("field presentation or native point lists changed")
    logs = np.array(logs, dtype=np.int64)
    B = logs[np.array(supports)[:, None] ^ np.array(evaluations)[None, :]]
    rng = random.Random(seed)
    centers = np.array([rng.randrange(order) for _ in range(m)], dtype=np.int64)
    if hashlib.sha256(centers.tobytes()).hexdigest() != artifact['centers_sha256']:
        raise RuntimeError("center hash changed")
    inherited = np.array(artifact['best_assignment'], dtype=np.int64)
    inherited_score = float(np.cos(2*np.pi*((B@inherited-centers) % order)/order).mean())
    if abs(inherited_score-artifact['best_mean_cosine']) > 1e-12:
        raise RuntimeError("inherited score failed replay")
    basis, blocks = block_basis(m, m+n, order)
    G = (B @ basis) % order
    kernel = logs.copy()
    kernel[0] = 0  # Irrelevant on disjoint support/evaluation rows; defines the full convolution.
    block_records = []
    for offset, size in blocks:
        phases, checks = exact_translation_control(kernel, offset, size, order)
        index = offset-m
        if not np.array_equal(G[:, index:index+size], phases[list(supports)]):
            raise ArithmeticError("native basis product failed independent transform")
        counts = [len(np.unique(np.minimum(G[:, index+j], (-G[:, index+j]) % order)))
                  for j in range(size)]
        if max(counts) > 2**bits//size-1:
            raise ArithmeticError("coset phase bound failed on disjoint rows")
        block_records.append({"offset": offset, "size": size, "exact_covariance_equalities": checks,
                              "distinct_phase_values_up_to_sign_min": min(counts),
                              "distinct_phase_values_up_to_sign_max": max(counts),
                              "coset_bound_on_disjoint_rows": 2**bits//size-1})
    largest_offset, largest_size = max(blocks, key=lambda item: item[1])
    moves = [{"mode": mode, **shortest_scalar_move(G[:, largest_offset-m+mode], order)}
             for mode in (0, 1, 2, 127, 255)]
    print(json.dumps({"stage": "exact_structure_verified", "blocks": block_records,
                      "shortest_scalar_moves": moves}), flush=True)
    runs = []
    for start_name, initial in [('zero', np.zeros(n, dtype=np.int64)), ('inherited_best', inherited)]:
        for basis_name, transform in [('original', None), ('affine_walsh', basis)]:
            before = time.perf_counter()
            result = dependency['fft_line_search'](B, centers, initial, order, basis_inv=transform, sweeps=2)
            assignment = result['assignment']
            direct = (B @ np.array(assignment, dtype=np.int64)) % order
            fast = dependency['fast_public_matvec'](bits, supports, evaluations, assignment)
            if tuple(int(v) for v in direct) != fast:
                raise ArithmeticError("returned assignment failed original fast convolution replay")
            result.update({"basis": basis_name, "start": start_name,
                           "wall_seconds_diagnostic": time.perf_counter()-before,
                           "original_fast_convolution_replay": True,
                           "certified_score": certified_score((direct-centers) % order, order)})
            runs.append(result)
            print(json.dumps({"stage": "run_finished", **{k: result[k] for k in
                  ('basis','start','initial_mean_cosine','final_mean_cosine','strict_improvements','coordinate_scans','wall_seconds_diagnostic')}}), flush=True)
    root = Path(__file__).resolve().parent
    return {"schema": "isolated-mpi-affine-walsh-attack/v1", "date": "2026-10-23",
            "status": "bounded-native-classical-attack; no-hardness-or-speedup-claim",
            "native_input": {"bits": bits, "m": m, "n": n, "order": order,
                             "generator_encoding": generator, "center_seed": seed,
                             "field_modulus_coefficients": field_modulus,
                             "explicit_matrix_sha256": hashlib.sha256(B.tobytes()).hexdigest(),
                             "original_field_and_point_lists_checked": True,
                             "centers_sha256": artifact['centers_sha256']},
            "blocks": block_records, "largest_block_short_move_controls": moves,
            "inherited_best_score": inherited_score, "runs": runs,
            "any_returned_assignment_certified_above_0_3": any(r['certified_score']['score_at_least_0_3_certified'] for r in runs),
            "all_rows_scored": True, "budget_extended_after_results": False,
            "predeclared_sweeps_per_run": 2, "total_wall_seconds_diagnostic": time.perf_counter()-started,
            "source_sha256": {**source_hashes, str(artifact_path): hashlib.sha256(artifact_bytes).hexdigest(),
                              **{name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in
                                 ('EXPERIMENT.md','walsh_attack.py','test_walsh_attack.py')}},
            "scope_limits": ['one frozen native instance', 'greedy line search not a sampler',
                             'no mixing or classical hardness theorem', 'no generic MPI dequantization',
                             'moving repository untouched', 'independent review pending']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    receipt = run()
    args.output.write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({"output": str(args.output.resolve()), "target_hit": receipt['any_returned_assignment_certified_above_0_3']}))
