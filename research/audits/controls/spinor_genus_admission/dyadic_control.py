"""Finite exact dyadic squareclass controls, not Beli formula implementation.

Sage algebra: /opt/anaconda3/envs/qsearch-cas/bin/python.
"""
import json
from pathlib import Path
from sage.all import GF, NumberField, PolynomialRing, QQ, matrix, prod, vector

S = PolynomialRing(QQ, 'x')
x = S.gen()
F2 = GF(2)
cases = []
specifications = [(x*x-x-1, 1, 2, [3, 1, 0]),
                  (x**3-6*x-2, 3, 1, [4, 3, 3, 2, 2, 1, 0])]
for polynomial, expected_e, expected_f, expected_filtration in specifications:
    K = NumberField(polynomial, 'a')
    a = K.gen()
    primes = K.primes_above(2)
    assert len(primes) == 1
    P = primes[0]
    e, f = int(P.ramification_index()), int(P.residue_class_degree())
    assert (e, f) == (expected_e, expected_f)
    assert K.signature() == (K.degree(), 0)
    pi = K(2) if e == 1 else a
    assert K.ideal(pi).valuation(P) == 1
    lifts = [K(1), a] if f == 2 else [K(1)]
    residue_field = P.residue_field()
    _, _, to_residue_vector = residue_field.vector_space(map=True)
    residue_basis = matrix(F2, [list(to_residue_vector(residue_field(b))) for b in lifts])
    assert residue_basis.rank() == f
    generators, levels = [pi], [0]
    for j in range(1, 2*e+1):
        for lift in lifts:
            generators.append(1+pi**j*lift)
            levels.append(j)
    assert len(generators) == 1+2*e*f
    assert all(K.ideal(g).valuation(P) == 0 for g in generators[1:])
    symbols = matrix(QQ, len(generators), len(generators), lambda i, j:
                     K.hilbert_symbol(generators[i], generators[j], P))
    assert all(s in (-1, 1) for s in symbols.list())
    gram = matrix(F2, symbols.nrows(), symbols.ncols(),
                  [(1-int(s))//2 for s in symbols.list()])
    dimension = e*f+2
    assert gram == gram.transpose() and gram.rank() == dimension
    selected = list(gram.pivots())
    basis_gram = gram.matrix_from_rows_and_columns(selected, selected)
    assert basis_gram.det() == 1
    selected_columns = gram.matrix_from_columns(selected)
    inverse_gram = basis_gram.inverse()
    coordinates = []
    for j in range(len(generators)):
        coordinate = inverse_gram*vector(F2, [gram[i, j] for i in selected])
        assert selected_columns*coordinate == gram.column(j)
        coordinates.append(coordinate)
    coordinate_matrix = matrix(F2, coordinates).transpose()
    assert coordinate_matrix.rank() == dimension
    filtration_ranks = [int(coordinate_matrix.matrix_from_columns(
        [i for i, level in enumerate(levels) if level >= r]).rank())
        for r in range(1, 2*e+2)]
    assert filtration_ranks == expected_filtration
    assert coordinate_matrix.matrix_from_columns(range(1, len(generators))).rank() == dimension-1
    assert coordinate_matrix.column(0) not in coordinate_matrix.matrix_from_columns(
        range(1, len(generators))).column_space()
    norm_row = matrix(F2, [[gram[0, j] for j in selected]])
    assert norm_row.rank() == 1
    norm_kernel = norm_row.right_kernel()
    assert norm_kernel.dimension() == dimension-1
    norm_generators = []
    for coefficient_vector in norm_kernel.basis():
        representative = prod(generators[j]**int(bit) for j, bit in zip(selected, coefficient_vector))
        assert K.hilbert_symbol(pi, representative, P) == 1
        norm_generators.append(str(representative))
    excluded = next(j for j in selected if gram[0, j] == 1)
    assert K.hilbert_symbol(pi, generators[excluded], P) == -1
    cases.append({'polynomial': str(polynomial), 'e': e, 'f': f,
        'local_degree': e*f, 'uniformizer': str(pi), 'residue_lifts': [str(b) for b in lifts],
        'candidate_count': len(generators), 'candidate_generators': [str(g) for g in generators],
        'Hilbert_F2_Gram': [list(map(int, row)) for row in gram.rows()],
        'squareclass_dimension': dimension, 'Hilbert_Gram_rank': int(gram.rank()),
        'selected_basis_indices': list(map(int, selected)), 'selected_pairing_nondegenerate': True,
        'unit_filtration_r_values': list(range(1, 2*e+2)), 'unit_filtration_ranks': filtration_ranks,
        'uniformizer_outside_unit_span': True,
        'quadratic_norm_kernel': {'extension_radicand': str(pi),
            'dimension': int(norm_kernel.dimension()), 'generators': norm_generators,
            'actual_symbol_on_every_kernel_generator': 1,
            'excluded_generator_actual_symbol': -1}})

result = {'status': 'PASS',
    'scope': 'Two finite exact local Hilbert-pairing/filtration controls; no all-degree inference.',
    'cases': cases,
    'claim_gates': {'all_degree_inference_from_controls': False, 'full_spinor_norm_solver': False,
        'Beli_source_formula_implementation': False, 'full_algorithm': False,
        'quantum_execution': False, 'novelty': False, 'speedup': False}}
Path(__file__).with_name('dyadic_result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'cases': [{key: case[key] for key in (
    'polynomial', 'e', 'f', 'candidate_count', 'Hilbert_Gram_rank', 'unit_filtration_ranks',
    'selected_pairing_nondegenerate', 'uniformizer_outside_unit_span')} for case in cases]}, indent=2))
