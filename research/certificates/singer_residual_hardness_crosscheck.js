// Independent polynomial-field arithmetic, classical witness replay, and DFTs.
"use strict";
const fs=require("fs"),path=require("path"),assert=require("assert/strict");
const report=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../classical_baselines/singer_residual_hardness.json"),"utf8"));
const close=(a,b)=>assert(Math.abs(a-b)<2e-10,`${a} != ${b}`);
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
class Q {
  constructor(n,d=1n){n=BigInt(n);d=BigInt(d);assert(d>0n);const g=gcd(n<0n?-n:n,d);this.n=n/g;this.d=d/g;}
  add(b){return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}
  mul(b){return new Q(this.n*b.n,this.d*b.d);}
  div(b){return new Q(this.n*b.d,this.d*b.n);}
  eq(b){return this.n===b.n&&this.d===b.d;}
  le(b){return this.n*b.d<=b.n*this.d;}
}
const q=n=>new Q(n),read=x=>new Q(x.numerator,x.denominator),one=q(1),eq=(a,b)=>assert(a.eq(b));
function integerSqrt(n){if(n<2n)return n;let x=1n<<BigInt(Math.ceil(n.toString(2).length/2));while(true){const y=(x+n/x)>>1n;if(y>=x)return x;x=y;}}
function sqrtUpper(x,bits){const a=x.n<<BigInt(2*bits);let root=integerSqrt(a/x.d);if(root*root*x.d<a)root++;return new Q(root,1n<<BigInt(bits));}
const minOne=x=>x.le(one)?x:one;
function field(row){
  const p=row.base_prime,m=row.extension_degree,f=row.modulus_coefficients;
  const mod=x=>(x%p+p)%p,zero=()=>Array(m).fill(0),oneF=()=>[1,...Array(m-1).fill(0)];
  assert.equal(f.length,m+1);assert.equal(f[m],1);
  function mul(a,b){
    const c=Array(2*m-1).fill(0);
    for(let i=0;i<m;i++)for(let j=0;j<m;j++)c[i+j]=mod(c[i+j]+a[i]*b[j]);
    for(let k=2*m-2;k>=m;k--)for(let j=0;j<m;j++)c[k-m+j]=mod(c[k-m+j]-c[k]*f[j]);
    return c.slice(0,m);
  }
  function pow(a,e){e=BigInt(e);let out=oneF();while(e){if(e&1n)out=mul(out,a);a=mul(a,a);e>>=1n;}return out;}
  function directTrace(a){let out=zero(),x=a;for(let j=0;j<m;j++){out=out.map((v,i)=>mod(v+x[i]));x=pow(x,p);}assert(out.slice(1).every(v=>v===0));return out[0];}
  const basis=Array.from({length:m},(_,j)=>zero().map((_,k)=>Number(j===k))),functional=basis.map(directTrace);
  const trace=a=>a.reduce((z,v,j)=>mod(z+v*functional[j]),0);
  return {p,m,mul,pow,one:oneF(),basis,trace,directTrace};
}
function rank(rows,p){
  if(!rows.length)return 0;const A=rows.map(r=>r.slice());let rank=0;
  for(let col=0;col<A[0].length&&rank<A.length;col++){
    const pivot=A.findIndex((row,i)=>i>=rank&&row[col]!==0);if(pivot<0)continue;
    [A[rank],A[pivot]]=[A[pivot],A[rank]];
    let inverse=1;while(inverse*A[rank][col]%p!==1)inverse++;
    A[rank]=A[rank].map(v=>v*inverse%p);
    for(let i=0;i<A.length;i++)if(i!==rank){const c=A[i][col];A[i]=A[i].map((v,j)=>(v-c*A[rank][j]%p+p)%p);}
    rank++;
  }
  return rank;
}
let sourceQueries=0,traceMatrixEntries=0,primitiveCertificates=0,residualWitnesses=0;
for(const r of report.classical_geometry_controls){
  const F=field(r),p=F.p,m=F.m,alpha=r.primitive_element_coefficients,M=BigInt(p)**BigInt(m)-1n;
  let product=1n;
  for(const [prime,exponent] of Object.entries(r.multiplicative_order_factorization)){
    const z=BigInt(prime);assert(z<=100000000n);
    for(let d=2n;d*d<=z;d++)assert.notEqual(z%d,0n);
    product*=z**BigInt(exponent);assert.notDeepEqual(F.pow(alpha,M/z),F.one);
  }
  assert.equal(product,M);assert.deepEqual(F.pow(alpha,M),F.one);primitiveCertificates++;
  const beta=F.pow(alpha,r.hidden_shift_calibration),normal=r.recovered_normal_coefficients;
  for(const record of r.queries){
    const point=F.pow(alpha,record.exponent),value=F.trace(F.mul(beta,point));
    assert.equal(record.oracle_output,Number(value===0));sourceQueries++;
  }
  assert.equal(r.oracle_evaluations,r.queries.length);
  if(p===2){
    assert.deepEqual(normal,beta);assert.equal(r.oracle_evaluations,m);
    r.trace_system.forEach((row,i)=>row.forEach((value,j)=>{
      assert.equal(value,F.trace(F.mul(F.pow(alpha,i),F.basis[j])));traceMatrixEntries++;
    }));
  }else{
    assert.equal(rank(r.trace_constraint_matrix,p),m-1);
    r.independent_positive_points.forEach((x,i)=>{
      const point=F.pow(alpha,x.exponent);assert.deepEqual(point,x.point_coefficients);
      r.trace_constraint_matrix[i].forEach((value,j)=>{assert.equal(value,F.trace(F.mul(point,F.basis[j])));traceMatrixEntries++;});
      assert.equal(F.trace(F.mul(normal,point)),0);
    });
  }
  const target=F.pow(normal,p-1),generator=F.pow(alpha,p-1);
  assert.deepEqual(target,r.residual_target_coefficients);assert.deepEqual(generator,r.residual_generator_coefficients);
  assert.deepEqual(target,F.pow(generator,r.hidden_shift_calibration));residualWitnesses++;
  const v=M/BigInt(p-1),law=r.query_law;let expected=q(0);
  law.rank_progress_probabilities.forEach((value,i)=>{
    const prob=new Q(BigInt(p)**BigInt(m-1)-BigInt(p)**BigInt(i),M);eq(prob,read(value));expected=expected.add(one.div(prob));
  });
  eq(expected,read(law.expected_classical_membership_queries));
  eq(q(p*(m-1)).add(new Q(p*p,(p-1)**2)),read(law.strict_expected_query_upper));
  assert.equal(v.toString(),r.projective_group_order);
  assert(!r.inverse_or_discrete_log_called_by_decoder&&!r.polynomial_time_classical_full_recovery_claim);
}
let exactLedgers=0;
for(const r of report.growing_base_field_ledgers){
  const base=1n<<BigInt(r.base_field_bits),v=base*base+base+1n,k=base+1n,lam=1n;
  const g=r.query_gate,i=r.injectivization,c=r.reconstruction,bits=g.dyadic_square_root_precision_bits;
  assert.equal(g.hypotheses,v.toString());assert.equal(g.marked_points,k.toString());
  const root=sqrtUpper(new Q(1,v),bits).add(q(2*g.queries).mul(sqrtUpper(new Q(k,v),bits)));
  eq(minOne(root.mul(root)),read(g.average_shift_recovery_success_upper));
  const density=new Q(k,v),influence=new Q(2n*(k-lam),v);
  eq(density,read(i.membership_density));eq(influence,read(i.exact_nonzero_shift_influence));
  assert.equal(i.necessary_boolean_offsets_for_any_injective_tuple,base.toString());
  const threshold=BigInt(2*v.toString(2).length+6);
  assert.equal(i.sufficient_random_offsets_for_failure_at_most_one_over_64,((threshold*influence.d+influence.n-1n)/influence.n).toString());
  const expected=new Q(base**3n-1n,base**2n-1n).add(new Q(base**3n-1n,base**2n-base));
  eq(expected,read(c.expected_classical_membership_queries));
  assert(!g.white_box_normal_or_trace_value_oracle_covered&&!g.general_full_oracle_DHSP_lower_bound);exactLedgers++;
}
const add=(a,b)=>[a[0]+b[0],a[1]+b[1]],mul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],scale=(a,b)=>[a[0]*b,a[1]*b];
const abs2=a=>a[0]*a[0]+a[1]*a[1];
function popcount(x){let r=0;while(x){r+=x&1;x>>>=1;}return r;}
function dft(vector,group,inverse=false){
  const n=vector.length;
  return vector.map((_,k)=>vector.reduce((z,a,x)=>{
    const phase=group==="boolean"?[(-1)**popcount(x&k),0]:[Math.cos(2*Math.PI*k*x/n),Math.sin((inverse?-1:1)*2*Math.PI*k*x/n)];
    return add(z,scale(mul(phase,a),1/Math.sqrt(n)));
  },[0,0]));
}
let spectralProbabilities=0;
for(const r of report.spectral_normalization_controls){
  const values=r.membership_values,v=values.length,s=r.hidden_shift_calibration,k=values.reduce((a,b)=>a+b,0);
  const index=(x,delta)=>r.group==="boolean"?x^delta:(x-delta+v)%v;
  for(let delta=1;delta<v;delta++)assert.equal(values.reduce((z,a,x)=>z+a*values[index(x,delta)],0),r.difference_parameter);
  const root=Math.sqrt(k-r.difference_parameter),sums=dft(values.map(a=>[a,0]),r.group).map(a=>scale(a,Math.sqrt(v)));
  const input=values.map((_,x)=>[(-1)**values[index(x,s)]/Math.sqrt(v),0]),hat=dft(input,r.group);
  for(const branch of r.zero_character_controls){
    const corrected=hat.map((a,j)=>mul(a,j===0?[branch.trivial_character_phase,0]:[sums[j][0]/root,-sums[j][1]/root]));
    const out=dft(corrected,r.group,true),probabilities=out.map(abs2);
    probabilities.forEach((p,x)=>{close(p,branch.final_probabilities[x]);spectralProbabilities++;});
    close(probabilities.reduce((a,b)=>a+b,0),1);close(probabilities[s],branch.complete_normalized_target_formula);
  }
  eq(new Q(4*(k-r.difference_parameter),v),read(r.leading_fourier_target_term_NOT_probability));
  assert(r.phase_correction_tables_only_for_calibration&&!r.efficient_coherent_phase_recipe_proved_by_this_module);
}
assert(Object.values(report.claim_gate).every(x=>x===false));
console.log(JSON.stringify({sourceQueries,traceMatrixEntries,primitiveCertificates,residualWitnesses,exactLedgers,spectralProbabilities,independentTheoremReview:false,newAlgorithmClaim:false}));
