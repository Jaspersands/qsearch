"""Exact local ordered-rectangle support-map falsifier: only r=2,3,4.
Run with /opt/anaconda3/envs/qsearch-cas/bin/python; JSON receipt on stdout.
Orbit coordinates are invariant per-point coefficients, NEVER orbit sums.
"""
from sage.all import ZZ, matrix, vector, gcd, lcm
from itertools import product
from collections import Counter
import json
import sys
import time
import traceback

START = time.perf_counter()

def diagonal_orbits(points, r):
    remaining = set(points)
    ans = []
    while remaining:
        start = min(remaining)
        orb = []
        point = start
        while point not in orb:
            orb.append(point)
            point = tuple((i+1) % r for i in point)
        assert point == start
        remaining.difference_update(orb)
        ans.append(tuple(orb))
    return ans

def integral_matrix(M):
    assert all(x.denominator() == 1 for x in M.list())
    return matrix(ZZ, M)

def run_case(r):
    tic = time.perf_counter()
    Z = diagonal_orbits(product(range(r), repeat=2), r)
    rectangles = diagonal_orbits(product(range(r), repeat=4), r)
    # X and Y each have ONE Frobenius orbit of length r. Each Z orbit has
    # length r, so both norm weights |Z|/r equal1 (per-point convention).
    A = matrix(ZZ, [[len(orb)//r for orb in Z], [len(orb)//r for orb in Z]])
    columns = []
    for rectangle_orbit in rectangles:
        point_counts = Counter()
        for x0, x1, y0, y1 in rectangle_orbit:
            point_counts[(x0,y0)] += 1
            point_counts[(x0,y1)] -= 1
            point_counts[(x1,y0)] -= 1
            point_counts[(x1,y1)] += 1
        col = []
        for orb in Z:
            values = {point_counts[point] for point in orb}
            assert len(values) == 1
            col.append(values.pop())  # common PER-POINT coefficient
        columns.append(tuple(col))
    B = matrix(ZZ, len(Z), len(columns), lambda i,j:columns[j][i])
    AB = A*B
    assert AB.is_zero()
    K = A.right_kernel_matrix()  # rows: Sage integer kernel basis
    assert K.base_ring() is ZZ and (A*K.transpose()).is_zero()
    DK, UK, VK = K.smith_form()
    assert UK*K*VK == DK
    kernel_invariants = [abs(int(DK[i,i])) for i in range(K.nrows())]
    assert all(a == 1 for a in kernel_invariants)
    assert K.nrows() == A.ncols()-A.rank()
    # Primitive full-rank sublattice of the rational kernel = saturated kernel.
    C = integral_matrix(K.transpose().change_ring(ZZ.fraction_field()).solve_right(B))
    assert K.transpose()*C == B
    D, U, V = C.smith_form()
    assert U*C*V == D
    assert abs(U.det()) == 1 and abs(V.det()) == 1
    rank_B = C.rank()
    diagonal = [abs(int(D[i,i])) for i in range(rank_B)]
    torsion = [a for a in diagonal if a>1]
    free_rank = K.nrows()-rank_B
    w = vector(ZZ, [1,-1]+[0]*(r-2))
    assert A*w == 0 and gcd(list(w)) == 1
    z = K.transpose().change_ring(ZZ.fraction_field()).solve_right(w)
    assert all(c.denominator()==1 for c in z)
    z = vector(ZZ,z)
    uz = U*z
    residue = [int(uz[i] % diagonal[i]) for i in range(rank_B)]
    tail = [int(uz[i]) for i in range(rank_B,K.nrows())]
    missing = any(residue) or any(tail)
    assert missing
    assert free_rank == 0
    order = lcm([ZZ(diagonal[i])//gcd(ZZ(diagonal[i]),uz[i]) for i in range(rank_B)])
    # Construct a concrete integral rectangle combination giving order*w.
    scaled = U*(order*z)
    y = vector(ZZ, C.ncols())
    for i in range(rank_B):
        assert scaled[i] % D[i,i] == 0
        y[i] = scaled[i]//D[i,i]
    coeff = V*y
    assert B*coeff == order*w
    # Index and exact finite quotient independently agree with Smith product.
    index = ZZ.one()
    for a in diagonal:index *= a
    result = {
        'r':r,'X_cycle_type':[r],'Y_cycle_type':[r],
        'Z_orbit_count':len(Z),'Z_orbit_sizes':[len(orb) for orb in Z],
        'Z_orbit_representatives':[list(orb[0]) for orb in Z],
        'ordered_rectangle_orbits':len(rectangles),
        'rectangle_orbit_sizes':sorted(set(len(orb) for orb in rectangles)),
        'A':[[int(a) for a in row] for row in A.rows()],
        'B_shape':[B.nrows(),B.ncols()],
        'B_distinct_columns_with_multiplicity':[{'column':list(col),'multiplicity':count}
            for col,count in sorted(Counter(columns).items())],
        'AB_exactly_zero':True,'rank_A':int(A.rank()),'rank_B':int(rank_B),
        'saturated_kernel_basis_rows':[[int(a) for a in row] for row in K.rows()],
        'kernel_basis_smith_invariants':kernel_invariants,
        'B_coordinates_in_kernel_smith_diagonal':diagonal,
        'smith_identity_exact':True,'smith_transformations_unimodular':True,
        'cokernel_free_rank':int(free_rank),'cokernel_torsion_invariants':torsion,
        'index_of_image_in_kernel':int(index),'image_equals_integer_kernel':False,
        'missing_primitive_vector':[int(a) for a in w],
        'missing_vector_kernel_coordinates':[int(a) for a in z],
        'missing_vector_smith_residue':residue,'missing_vector_exact_order_in_cokernel':int(order),
        'multiple_witness_nonzero_rectangle_coefficients':[{
            'column_index':i,'orbit_representative':list(rectangles[i][0]),'coefficient':int(coeff[i])}
            for i in range(len(coeff)) if coeff[i]],
        'multiple_witness_identity':'B*listed_coefficients = cokernel_order*missing_primitive_vector',
        'elapsed_seconds':time.perf_counter()-tic}
    return result

rows=[]
try:
    for r in [2,3,4]:
        row=run_case(r)
        rows.append(row)
        print('r='+str(r)+': AB=0, cokernel='+str(row['cokernel_torsion_invariants'])+
              ', missing primitive '+str(row['missing_primitive_vector']),file=sys.stderr,flush=True)
    print(json.dumps({'status':'INTEGRAL_GENERATION_REFUTED','scope':'Only equal single-cycle local types r=2,3,4, per-point orbit coordinates and diagonal Frobenius ordered-rectangle transfers. Refutes the proposed integral support map, not norm-problem solvability, hardness, or every polynomial algorithm.',
                      'cases':rows,'mixed_cycle_types_tested':0,
                      'mixed_types_reason':'Already decisive failure at first prescribed type; no mixed scan needed.',
                      'cas_interpreter':sys.executable,'elapsed_seconds':time.perf_counter()-START},sort_keys=True))
except Exception as exc:
    print(json.dumps({'status':'CODE_OR_API_ISSUE','completed_cases':rows,'error_type':type(exc).__name__,'error':str(exc),'traceback':traceback.format_exc()},sort_keys=True))
    sys.exit(2)
