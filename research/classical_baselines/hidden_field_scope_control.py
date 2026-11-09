from sage.all import *
import json, sys, time, subprocess

from pathlib import Path
OUT=str(Path(__file__).with_suffix('.json'))

def field_data(p,n,name='b'):
    F=GF(p); K=GF(p**n,name=name); b=K.gen(); basis=[b**i for i in range(n)]
    V, to_field, from_field=K.vector_space(map=True)
    def coords(x): return vector(F,from_field(K(x)))
    def regular(x): return matrix(F,n,n,lambda i,j:coords(K(x)*basis[j])[i])
    return F,K,b,basis,coords,regular

def algebra_space(F,n,mats):
    return VectorSpace(F,n*n).subspace([vector(F,A.list()) for A in mats])

def part_one():
    start=time.perf_counter(); F,K,b,basis,coords,regular=field_data(3,4)
    a=b**10; E=[regular(x) for x in basis]
    A=regular(a); m=A.minimal_polynomial(); cp=A.charpoly()
    c=b
    S=matrix(F,4,4,lambda i,j:coords(basis[j]+c*basis[j]**9)[i])
    assert S.is_invertible()
    Sinv=S.inverse(); Ep=[S*B*Sinv for B in E]
    W=algebra_space(F,4,E); Wp=algebra_space(F,4,Ep); D=W.intersection(Wp)
    invertible_intersection=sum(matrix(F,4,4,v).is_invertible() for v in D)
    out={'field_modulus':str(K.modulus()),'primitive_c_order':int(c.multiplicative_order()),'a_order':int(a.multiplicative_order()),'regular_generator_charpoly_matches_field':regular(b).charpoly()==K.modulus(),'a':str(a),'a_in_F9':a**9==a,'a_not_in_F3':a**3!=a,
         'a_minimal_polynomial':str(a.minimal_polynomial()),'regular_minimal_polynomial':str(m),
         'minimal_polynomial_degree':int(m.degree()),'regular_characteristic_polynomial':str(cp),
         'characteristic_polynomial_equals_minpoly_squared':cp==m**2,'charpoly_is_irreducible':cp.is_irreducible(),
         'S_determinant':int(S.det()),'S_invertible':S.is_invertible(),
         'field_algebra_dimension':W.dimension(),'conjugated_algebra_dimension':Wp.dimension(),
         'intersection_dimension':D.dimension(),'intersection_algebra_size':3**D.dimension(),
         'intersection_unit_count':int(invertible_intersection),'each_torus_order':3**4-1,
         'seconds':time.perf_counter()-start}
    assert out['primitive_c_order']==80 and out['a_order']==8 and out['regular_generator_charpoly_matches_field']
    assert out['minimal_polynomial_degree']==2 and out['characteristic_polynomial_equals_minpoly_squared']
    assert out['intersection_dimension']==2 and out['intersection_unit_count']==8
    return out

def native_producer(p,n,oracle):
    # No secret transform is an input. Field, regular basis, and all query
    # vectors are public; the callable is the sole access to hidden data.
    start=time.perf_counter(); F,K,b,basis,coords,regular=field_data(p,n)
    R=PolynomialRing(F,[f'l{i}{j}' for i in range(n) for j in range(n)]+['z'],order='degrevlex')
    vs=R.gens(); U=matrix(R,n,n,vs[:n*n]); z=vs[-1]
    Y=PolynomialRing(F,[f'y{i}' for i in range(n)])
    normpoly=sum((Y.gen(k)*matrix(Y,regular(basis[k])) for k in range(n)),zero_matrix(Y,n,n)).det()
    constraints=[]; query_count=0
    for values in cartesian_product([list(F)]*n):
        x=vector(F,values)
        if x.is_zero(): continue
        target=F(oracle(x)); query_count+=1
        yvalues=list(U*x)
        constraints.append(Y.hom(yvalues,R)(normpoly)-target)
    constraints.extend(v**p-v for v in vs)
    constraints.append(z*U.det()-1)
    I=R.ideal(constraints)
    setup=time.perf_counter()-start
    begin=time.perf_counter(); gb=I.groebner_basis(algorithm='libsingular:std')
    gb_seconds=time.perf_counter()-begin
    begin=time.perf_counter(); solutions=R.ideal(gb).variety(ring=F)
    variety_seconds=time.perf_counter()-begin
    candidates=[matrix(F,n,n,[sol[vs[k]] for k in range(n*n)]) for sol in solutions]
    return candidates,{'n':n,'p':p,'public_field_modulus':str(K.modulus()),'query_count':query_count,
       'constraints':len(constraints),'variables':len(vs),'groebner_basis_size':len(gb),
       'solution_count':len(candidates),'setup_seconds':setup,'groebner_seconds':gb_seconds,
       'variety_seconds':variety_seconds,'producer_seconds':time.perf_counter()-start},normpoly

def run_native(n):
    start=time.perf_counter(); p=3; F,K,b,basis,coords,regular=field_data(p,n)
    secret=matrix(F,[[1,1,0],[0,1,1],[1,0,0]]) if n==3 else matrix(F,[[1,1],[1,2]])
    assert secret.is_invertible()
    query_count=[0]
    def oracle(x):
        assert not x.is_zero()
        query_count[0]+=1
        y=secret*x
        return F(sum((y[k]*basis[k] for k in range(n)),K(0)).norm())
    candidates,out,normpoly=native_producer(p,n,oracle)
    Y=normpoly.parent(); yy=vector(Y,Y.gens()); emb=F.hom(Y)
    def transformed_norm(L):
        image=list(matrix(Y,L)*yy)
        return Y.hom(image,Y)(normpoly)
    truepoly=transformed_norm(secret)
    def projective_tuple(poly):
        d=poly.dict(); lead=next(iter(sorted(d,reverse=True))); scale=d[lead]
        return tuple(sorted((tuple(exp),int(coeff/scale)) for exp,coeff in d.items()))
    truth=projective_tuple(truepoly)
    E=[regular(x) for x in basis]
    truth_algebra=algebra_space(F,n,[secret.inverse()*A*secret for A in E])
    norm_ok=[]; algebra_ok=[]; exactnorm_ok=[]
    for L in candidates:
        pol=transformed_norm(L)
        norm_ok.append(projective_tuple(pol)==truth)
        exactnorm_ok.append(pol==truepoly)
        algebra_ok.append(algebra_space(F,n,[L.inverse()*A*L for A in E])==truth_algebra)
    out.update({'observed_oracle_calls':query_count[0], 'all_candidates_invertible':all(L.is_invertible() for L in candidates),
       'same_projective_norm_count':sum(norm_ok),'same_exact_norm_polynomial_count':sum(exactnorm_ok),
       'same_hidden_regular_field_algebra_count':sum(algebra_ok),'secret_present':any(L==secret for L in candidates),
       'total_seconds_with_validation':time.perf_counter()-start,
       'expected_group_count_hypothesis':n*(p**n-1)//(p-1),
       'control_scope':'all nonzero native queries, exact prime-field equations; finite only, no quantum execution'})
    print(json.dumps(out,default=int),flush=True)
    return out

if len(sys.argv)>1 and sys.argv[1]=='--native':
    run_native(int(sys.argv[2]))
else:
    result={'subfield_counterexample':part_one(),'groebner_attempts':[],'native_cap_seconds':30}
    print(json.dumps(result['subfield_counterexample'],default=int),flush=True)
    for n in [3,2]:
        begin=time.perf_counter()
        try:
            child=subprocess.run([sys.executable,__file__,'--native',str(n)],capture_output=True,text=True,timeout=30)
            if child.returncode:
                item={'n':n,'status':'error','seconds':time.perf_counter()-begin,'stdout':child.stdout[-3000:],'stderr':child.stderr[-5000:]}
                result['groebner_attempts'].append(item)
                print(json.dumps(item,default=int),flush=True)
                break
            item=json.loads(child.stdout.strip().splitlines()[-1]); item['status']='completed'; item['cap_wall_seconds']=time.perf_counter()-begin
            result['groebner_attempts'].append(item); print(json.dumps(item,default=int),flush=True); break
        except subprocess.TimeoutExpired:
            item={'n':n,'status':'timeout','seconds':time.perf_counter()-begin,'cap_seconds':30}
            result['groebner_attempts'].append(item); print(json.dumps(item,default=int),flush=True)
            if n==2: break
    with open(OUT,'w') as handle: json.dump(result,handle,indent=2,default=int)
