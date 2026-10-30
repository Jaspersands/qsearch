"""Source collision bounds and a deliberately bounded complete-list reference.

No capacity-decoder backend or quantum circuit is implemented here.
"""

from fractions import Fraction
from itertools import product
from math import comb, prod
from pathlib import Path
import sys

from flint import nmod_mat, nmod_poly

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"orbit-residual-decoder-2026-10-24"))
import orbit_decoder as o


def weights(nodes,p):
    B = nmod_poly([1],p)
    for z in nodes:
        B *= nmod_poly([-z,1],p)
    return [pow(int(B.derivative()(z)),-1,p) for z in nodes]


def unfold(g, rows):
    o.canonical(rows,g.width,len(g.nodes),g.p)
    return [[pow(g.width,-1,g.p)*sum(rows[h][i]*pow(a,-h,g.p)*pow(g.root,-ell*h,g.p)
              for h in range(g.width)) % g.p for ell in range(g.width)]
            for i,a in enumerate(g.representatives)]


def complete_reference(g,cap,syndromes,*,scalar_budget=10000,product_budget=100000):
    """Exhaustive finite checker. Refuse a budget, never truncate a list."""
    if g.width != 3:
        raise ValueError("the native cubic geometry is required")
    M,K,p = len(g.nodes),g.row_length,g.p
    o.integer(cap,"cap",0,K-1)
    o.integer(scalar_budget,"scalar budget",1,10**7)
    o.integer(product_budget,"Cartesian budget",1,10**7)
    o.canonical(syndromes,3,K,p)
    k = M-K
    common = {"scope":"EXHAUSTIVE_FINITE_REFERENCE_NOT_CAPACITY_BACKEND",
              "source_support_or_error_supplied":False,"scalar_messages_per_row":p**k,
              "quantum_circuit_executed":False}
    if p**k > scalar_budget:
        return {**common,"status":"UNAVAILABLE_REFERENCE_BUDGET","complete":False}
    H0 = nmod_mat([[pow(z,j,p) for z in g.nodes[:K]] for j in range(K)],p)
    particular = H0.solve(nmod_mat([[syndromes[h][j] for h in range(3)] for j in range(K)],p))
    delta = weights(g.nodes,p)
    lists = []
    for h in range(3):
        y = [int(particular[i,h]) if i<K else 0 for i in range(M)]
        rowlist = []
        for coeff in product(range(p),repeat=k):
            f = nmod_poly(list(coeff),p)
            error = [(y[i]-delta[i]*int(f(z))) % p for i,z in enumerate(g.nodes)]
            if sum(bool(v) for v in error) <= cap:
                rowlist.append(error)
        lists.append(rowlist)
    combos = prod(map(len,lists))
    common.update({"row_list_sizes":list(map(len,lists)),"Cartesian_product_size":combos})
    if combos > product_budget:
        return {**common,"status":"UNAVAILABLE_PRODUCT_BUDGET","complete":False}
    candidates = {}
    for rows in product(*lists):
        support = [i for i in range(M) if any(row[i] for row in rows)]
        if len(support)>cap:
            continue
        error = unfold(g,rows)
        if o.syndrome(g,error) != syndromes:
            raise ArithmeticError("whole-syndrome list replay failed")
        key = tuple(v for row in error for v in row)
        candidates[key] = error
    errors = [candidates[key] for key in sorted(candidates)]
    status = "VERIFIED_UNIQUE" if len(errors)==1 else ("REJECT_AMBIGUOUS" if errors else "REJECT_EMPTY")
    return {**common,"status":status,"complete":True,"errors":errors,
            "list_size":len(errors),"guard_cap":cap}


def collision_bound(p,M,K,C,w=None):
    o.field(p)
    o.integer(M,"blocks",2,8192)
    o.integer(K,"row syndrome length",2,M)
    o.integer(C,"whole cap",0,K-1)
    g = K-C
    if w is None:
        return min(Fraction(1),Fraction(2**M,p**min(3*g,2*g+2)))
    o.integer(w,"source support",0,C)
    total = Fraction(0)
    for c in range(C+1):
        for a in range(1,w+1):
            b = c-w+a
            if not 0<=b<=M-w or c+a<=K:
                continue
            total += Fraction(comb(w,a)*comb(M-w,b),p**min(3*(K-c),2*a))
    return min(Fraction(1),total)


def endpoint_competitor(g,syndromes,excluded_block):
    """Public interpolation witness at cap K, not a source decoder."""
    M,K,p = len(g.nodes),g.row_length,g.p
    if g.width!=3 or K>=M:
        raise ValueError("proper native cubic code required")
    o.canonical(syndromes,3,K,p)
    o.integer(excluded_block,"excluded block",0,M-1)
    support = [i for i in range(M) if i!=excluded_block][:K]
    V = nmod_mat([[pow(g.nodes[i],j,p) for i in support] for j in range(K)],p)
    a = V.solve(nmod_mat([[syndromes[h][j] for h in range(3)] for j in range(K)],p))
    rows = [[0]*M for _ in range(3)]
    for j,i in enumerate(support):
        for h in range(3):
            rows[h][i]=int(a[j,h])
    error = unfold(g,rows)
    if o.syndrome(g,error)!=syndromes or any(error[excluded_block]):
        raise ArithmeticError("endpoint alias failed original syndrome replay")
    return error


def ledger(p=12289,M=4096,K=2621,D=2375):
    o.field(p)
    o.integer(D,"source radius",0,M)
    if (p-1)%3 or 3*M>p-1:
        raise ValueError("original disjoint cubic orbit domain required")
    C = D+1
    epsilon = collision_bound(p,M,K,C)
    tau = o.binomial_tail(M,Fraction(p+1,2*p),D)
    loss = min(Fraction(1),tau+M*(epsilon+o.sqrt_upper(tau)+o.sqrt_upper(epsilon)))
    return {"p":p,"M":M,"K":K,"dimension":3*K,"rate":str(Fraction(K,M)),
            "source_radius":D,"whole_guard_cap":C,"capacity_slack":str(Fraction(K-C,M)),
            "collision_exponent":min(3*(K-C),2*(K-C)+2),
            "collision_upper_dyadic":str(o.upward(epsilon)),
            "source_tail_upper_dyadic":str(o.upward(tau)),
            "ideal_one_attempt_failure_upper_dyadic":str(o.upward(loss)),
            "old_Prony_equations":3*(K-C),"old_full_rank_gate_holds":3*(K-C)>=D,
            "status":"CONDITIONAL_NUMERICAL_LEDGER_NOT_A_FINITE_DECODER_CERTIFICATE",
            "external_capacity_theorem_finite_threshold_instantiated":False,
            "capacity_backend_implemented":False,"quantum_circuit_executed":False,
            "native_polynomial_produced":False,"speedup_or_novelty_established":False}


def annihilator_matrix(g,T):
    """Exact left-annihilator of the ORIGINAL scalar Vandermonde columns."""
    if len(set(T)) != len(T) or any(type(i) is not int or not 0<=i<len(g.nodes) for i in T):
        raise ValueError("distinct public support indices required")
    if len(T)>=g.row_length:
        raise ValueError("competitor support must be below K")
    V = nmod_poly([1],g.p)
    for i in T:
        for node in g.points[i]:
            V *= nmod_poly([-node,1],g.p)
    return nmod_mat([[int(V(node))*pow(node,j,g.p)%g.p for orbit in g.points for node in orbit]
                     for j in range(g.dimension-3*len(T))],g.p)
