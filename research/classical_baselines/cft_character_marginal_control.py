"""Finite controls for CFT_CHARACTER_MARGINAL_BASELINE.md; Sage required."""
from sage.all import QQ, ZZ, matrix, identity_matrix, zero_matrix, factorial, binomial, SymmetricFunctions, Partition, Partitions
from time import perf_counter
import json

# Producer uses only public lambda and s. Exact formal Jacobi identity is
# used to compute the truncated determinant without expanding its full degree.
def determinant_series_from_public_partition(lam,s,window=None):
    n=sum(lam); M=n//s; K=2*M; F=n+2*M*s+1 if window is None else window; dim=2*F
    J=zero_matrix(ZZ,dim,dim)
    for j in range(-F,F-s):
        J[j+s+F,j+F]=1
        J[j+F,j+s+F]=-1
    occupied=[(lam[i-1] if i<=len(lam) else 0)-i for i in range(1,F+1)]
    idx=[j+F for j in occupied]
    A=[]; power=identity_matrix(ZZ,dim)
    for k in range(K+1):
        A.append(matrix(QQ,power.matrix_from_rows_and_columns(idx,idx))/factorial(k))
        if k<K: power=power*J
    # D=A^-1 mod u^(K+1), computed coefficient by coefficient.
    D=[identity_matrix(QQ,F)]
    for k in range(1,K):
        D.append(-sum((A[i]*D[k-i] for i in range(1,k+1)),zero_matrix(QQ,F,F)))
    # h=C'/C=trace(A^-1 A'), then C'=hC.
    h=[]
    for k in range(K):
        h.append(sum((D[i]*A[k-i+1]).trace()*(k-i+1) for i in range(k+1)))
    C=[QQ(1)]
    for k in range(1,K+1):
        C.append(sum(h[j-1]*C[k-j] for j in range(1,k+1))/k)
    return C,{'n':n,'s':s,'M':M,'F':F,'one_particle_dimension':dim,'occupied_minor_dimension':F,'truncation_degree':K}

def invert_marginal(C,s,scale=None):
    M=(len(C)-1)//2
    # Correct displacement uses scale=s; scale=1 is the requested wrong control.
    if scale is None: scale=s
    r=[sum(C[2*(k-j)]*QQ(scale)**j/(QQ(2)**j*factorial(j)) for j in range(k+1)) for k in range(M+1)]
    B=[(-1)**k*factorial(k)*r[k]/QQ(s)**k for k in range(M+1)]
    P=[sum((-1)**(k-m)*binomial(k,m)*B[k] for k in range(m,M+1)) for m in range(M+1)]
    return B,P

def validation_full_row(lam,s):
    n=sum(lam); M=n//s
    S=SymmetricFunctions(QQ); schur=S.s()(Partition(lam)); p=S.p()
    result=[QQ(0)]*(M+1); rows=[]; norm=QQ(0)
    for nu in Partitions(n):
        char=schur.scalar(p(nu))
        counts=nu.to_exp()
        z=ZZ(1)
        for size,m in enumerate(counts,start=1): z*=ZZ(size)**m*factorial(m)
        weight=char**2/z
        norm+=weight
        multiplicity=counts[s-1] if s<=len(counts) else 0
        result[multiplicity]+=weight
        rows.append({'nu':list(nu),'character':str(char),'z':str(z),'weight':str(weight)})
    return result,norm,rows

results=[]
for lam,s in [([2],1),([2,1],1),([3,2,1],1),([3,2,1],2),([2,2],2)]:
    begin=perf_counter(); C,meta=determinant_series_from_public_partition(lam,s)
    producer_seconds=perf_counter()-begin
    B,P=invert_marginal(C,s)
    begin=perf_counter(); expected,norm,rows=validation_full_row(lam,s)
    validation_seconds=perf_counter()-begin
    result={**meta,'lambda':lam,'C_coefficients':[str(x) for x in C],
            'binomial_moments':[str(x) for x in B],
            'computed_marginal':[str(x) for x in P],
            'full_row_marginal':[str(x) for x in expected],
            'sum_computed':str(sum(P)), 'sum_full_row':str(norm),
            'all_nonnegative':all(x>=0 for x in P), 'all_exact_equal':P==expected,
            'odd_C_coefficients_zero':all(C[k]==0 for k in range(1,len(C),2)),
            'producer_seconds':producer_seconds,'validation_seconds':validation_seconds}
    if s==2:
        _,wrong=invert_marginal(C,s,scale=1)
        result['wrong_scale_marginal']=[str(x) for x in wrong]
        result['wrong_scale_rejected']=wrong!=expected
        result['wrong_scale_nonnegative']=all(x>=0 for x in wrong)
        result['wrong_scale_total']=str(sum(wrong))
    assert result['all_nonnegative'] and result['all_exact_equal'] and sum(P)==1 and norm==1
    if s==2: assert result['wrong_scale_rejected']
    if lam==[2] and s==1:
        short,_=determinant_series_from_public_partition(lam,s,window=sum(lam))
        _,short_P=invert_marginal(short,s)
        result['unpaid_small_window_marginal']=[str(x) for x in short_P]
        result['unpaid_small_window_rejected']=short_P!=expected
        assert result['unpaid_small_window_rejected']
    results.append(result)
    print(json.dumps(result,sort_keys=True),flush=True)
from pathlib import Path
with Path(__file__).with_suffix('.json').open('w') as handle:
    json.dump({'scope':'Five exact finite classical marginal controls, not joint sampling or quantum execution', 'method':'exact QQ formal Jacobi determinant recurrence; producer uses no partitions/characters','results':results},handle,indent=2)
