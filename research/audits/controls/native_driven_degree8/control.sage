# One fixed degree-eight native Hall1 cut-and-join frequency control.
from sage.all import QQ, Integer, Partitions, PolynomialRing, matrix, diagonal_matrix, factorial, sqrt
from collections import Counter
from pathlib import Path
import json
REPO=Path("/Users/jaspersands/Developer/qsearch")
out=REPO/"research/audits/controls/native_driven_degree8/result.json"
D=int(8);basis=[tuple(int(k) for k in mu) for mu in Partitions(D)];index={mu:i for i,mu in enumerate(basis)};n=len(basis)
checks=[]
def check(condition,label):
    assert condition,label
    checks.append(label)
def z(mu):
    ans=QQ(1)
    for k,m in Counter(mu).items():ans*=QQ(k)**m*factorial(m)
    return ans
def target(parts):return tuple(sorted(parts,reverse=True))
def nnz(A):return int(sum(c!=0 for c in A.list()))
def json_scalar(value):
    if isinstance(value,Integer):return int(value)
    raise TypeError("Unexpected JSON scalar "+str(type(value)))
def encode(A):return [[str(A[r,c]) for c in range(A.ncols())] for r in range(A.nrows())]
check(n==22,"degree8_partition_dimension22")
weights=[z(mu) for mu in basis];H=diagonal_matrix(QQ,weights)
for i,w in enumerate(weights):check(w>0,"positive_Hall_weight_"+str(i))
energies=[sum(k*k for k in mu) for mu in basis];N=diagonal_matrix(QQ,energies)
S=matrix(QQ,n,n)
# Native ordered i,j sum, built directly from occupation multiplicities.
for col,mu in enumerate(basis):
    counts=Counter(mu)
    for i in range(1,D):
        for j in range(1,D-i+1):
            k=i+j
            if counts[k]:
                parts=list(mu);parts.remove(k);parts.extend([i,j])
                S[index[target(parts)],col]+=k*counts[k]
            derivative=counts[i]*(counts[j]-(1 if i==j else 0))
            if derivative:
                parts=list(mu);parts.remove(i);parts.remove(j);parts.append(k)
                S[index[target(parts)],col]+=i*j*derivative
check(S.transpose()*H==H*S,"native_S_exact_weighted_self_adjoint")
check(N.transpose()*H==H*N,"native_N_exact_weighted_self_adjoint")
def frequency_filter(m):
    return matrix(QQ,n,n,lambda row,col:S[row,col] if abs(energies[row]-energies[col])==2*m else 0)
# Independent pair operators use actual polynomial derivatives, not occupation code above.
R=PolynomialRing(QQ,names=tuple("p"+str(k) for k in range(1,D+1)));p=R.gens()
monomials=[]
for mu in basis:
    term=R(1)
    for k in mu:term*=p[k-1]
    monomials.append(term)
def pair_polynomial_operator(a,b):
    assert a!=b and a+b<=D
    result=matrix(QQ,n,n)
    for col,f in enumerate(monomials):
        value=2*((a+b)*p[a-1]*p[b-1]*f.derivative(p[a+b-1])+a*b*p[a+b-1]*f.derivative(p[a-1]).derivative(p[b-1]))
        for exponent,c in value.dict().items():
            mu=target([k for k,m in enumerate(exponent,1) for repeat in range(int(m))])
            result[index[mu],col]+=c
    return result
S15=frequency_filter(15);C35=pair_polynomial_operator(3,5)
for a in range(n):
    for b in range(n):check(S15[a,b]==C35[a,b],"positive_full_matrix_entry_"+str((a,b)))
check(nnz(S15)==2,"positive_filter_only_two_nonzero_entries")
check(1+15>D,"other_factor_pair_1_15_excluded_by_degree")
i8=index[(8,)];i35=index[(5,3)]
amp_down=S15[i35,i8]*sqrt(weights[i35]/weights[i8])
amp_up=S15[i8,i35]*sqrt(weights[i8]/weights[i35])
g=2*sqrt(QQ(120))
check((amp_down-g).simplify_full()==0,"normalized_split_coefficient_2sqrt120")
check((amp_up-g).simplify_full()==0,"normalized_merge_coefficient_2sqrt120")
check(S15[i35,i8]==16 and S15[i8,i35]==30,"ordered_pair_raw_coefficients_16_30")
S6=frequency_filter(6);C16=pair_polynomial_operator(1,6);C23=pair_polynomial_operator(2,3)
for a in range(n):
    for b in range(n):check(S6[a,b]==C16[a,b]+C23[a,b],"negative_alias_sum_matrix_entry_"+str((a,b)))
check(S6!=C16,"negative_filter_not_pair_1_6_alone")
check(S6!=C23,"negative_filter_not_pair_2_3_alone")
w1=(index[(6,1,1)],index[(7,1)])
w2=(index[(3,3,2)],index[(5,3)])
check(S6[w1]==14 and C23[w1]==0,"pair_1_6_alias_explicit_witness")
check(S6[w2]==10 and C16[w2]==0,"pair_2_3_alias_explicit_witness")
def admitted_pairs(m):return [[int(i),int(m//i)] for i in range(1,m+1) if m%i==0 and i<=m//i and i+m//i<=D]
check(admitted_pairs(15)==[[3,5]],"admitted_factor_pair_catalog_m15")
check(admitted_pairs(6)==[[1,6],[2,3]],"admitted_factor_pair_catalog_m6")
result={"status":"PASS","scope":"Only degree8 Hall1, m15 positive and m6 alias controls. Exact finite normalization/frequency falsifier, no growingD sweep, addressability theorem or universality claim.","cas":"/opt/anaconda3/envs/qsearch-cas/bin/sage","D":D,"dimension":n,"basis":[list(mu) for mu in basis],"Hall_z_weights":[str(w) for w in weights],"N_energies":[int(e) for e in energies],"native_S_ordering":"sum over ordered positive i,j with i+j<=8; diagonal i=j counted once","frequency_projection":"retain entries with N_row-N_col=+/-2m; no floating Fourier sum","native_S_matrix":encode(S),"native_S_nonzero_entries":nnz(S),"weighted_adjoint_checks":{"S":True,"N":True},"positive_control":{"m":15,"frequency_abs":30,"admitted_unordered_pairs":admitted_pairs(15),"equals_independent_pair_operator":True,"matrix_entries_compared":int(n*n),"filter_nonzero_entries":nnz(S15),"filter_matrix":encode(S15),"independent_pair_matrix":encode(C35),"normalized_two_level_basis":[[8],[5,3]],"raw_two_level_matrix":[["0",str(S15[i8,i35])],[str(S15[i35,i8]),"0"]],"normalized_split_amplitude":str(amp_down),"normalized_merge_amplitude":str(amp_up),"expected_amplitude":"2*sqrt(120)","amplitude_squared":"480","both_amplitudes_match_exactly":True},"negative_control":{"m":6,"frequency_abs":12,"admitted_unordered_pairs":admitted_pairs(6),"filter_equals_sum_of_both_independent_pairs":True,"matrix_entries_compared":int(n*n),"filter_nonzero_entries":nnz(S6),"pair_1_6_nonzero_entries":nnz(C16),"pair_2_3_nonzero_entries":nnz(C23),"differs_from_either_individual_pair":True,"witness_pair_1_6":{"column_partition":[7,1],"row_partition":[6,1,1],"filter_entry":"14","pair_2_3_entry":"0"},"witness_pair_2_3":{"column_partition":[5,3],"row_partition":[3,3,2],"filter_entry":"10","pair_1_6_entry":"0"},"filter_matrix":encode(S6),"pair_1_6_matrix":encode(C16),"pair_2_3_matrix":encode(C23)},"assertions_passed":len(checks),"assertion_labels":checks}
out.write_text(json.dumps(result,indent=2,sort_keys=True,default=json_scalar)+"\n")
print(json.dumps({"status":"PASS","D":D,"dimension":n,"assertions_passed":len(checks),"matrix_entries_compared":int(2*n*n),"native_S_nonzero_entries":nnz(S),"positive_filter_nonzero_entries":nnz(S15),"positive_normalized_coefficient":str(amp_down),"expected_coefficient":"2*sqrt(120)","negative_filter_nonzero_entries":nnz(S6),"negative_pair_1_6_nonzero_entries":nnz(C16),"negative_pair_2_3_nonzero_entries":nnz(C23),"negative_differs_from_both_individual_pairs":True},indent=2))
