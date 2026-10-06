// Independent arbitrary-POVM classifier, complete native source and exact ledgers.
// Code crosscheck, not independent mathematical peer review.
const assert=require('assert/strict'),fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const report=JSON.parse(fs.readFileSync(path.join(root,'research/classical_baselines/dcp_native_product_readout_bound.json'),'utf8'));
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-9,`${a} != ${b}`);
const vec=(x,n,q)=>Array.from({length:n},()=>{const t=x%q;x=Math.floor(x/q);return t;});
const read=a=>[BigInt(a.sign)*BigInt(a.numerator_hex),BigInt(a.denominator_hex)];
const eq=(a,b)=>assert.equal(a[0]*b[1],b[0]*a[1]);
let POVMControls=0,nativeMatrices=0,nativeMatrixSecretPairs=0;
for(const row of report.actual_arbitrary_product_POVM_controls) {
  const A=row.labels,q=row.modulus,n=A.length,P=row.local_POVMs_weight_and_Bloch_rows,m=P.length,G=q**n;
  P.forEach(p=>{
    near(p.reduce((s,e)=>s+e[0],0),1);
    for(let k=1;k<4;k++)near(p.reduce((s,e)=>s+e[0]*e[k],0),0);
    p.forEach(e=>{assert.ok(e[0]>0);assert.ok(e.slice(1).reduce((s,x)=>s+x*x,0)<=1+1e-10);});
  });
  const likelihoods=[];let C=0;
  for(let si=0;si<G;si++) {
    const s=vec(si,n,q),theta=Array.from({length:m},(_,i)=>2*Math.PI*A.reduce((z,r,j)=>z+r[i]*s[j],0)/q);
    likelihoods.push(P.map((p,i)=>p.map(e=>e[0]*(1+e[1]*Math.cos(theta[i])+e[2]*Math.sin(theta[i])))));
    C+=theta.reduce((z,t)=>z*(1+Math.cos(t)**2),1)/G;
  }
  const outcomes=P.reduce((s,p)=>s*p.length,1);let success=0,collision=0;
  for(let yi=0;yi<outcomes;yi++) {
    let index=yi;const y=P.map(p=>{const v=index%p.length;index=Math.floor(index/p.length);return v;});
    const base=y.reduce((s,v,i)=>s*P[i][v][0],1);
    const values=likelihoods.map(p=>y.reduce((s,v,i)=>s*p[i][v],1));
    success+=Math.max(...values)/G;collision+=values.reduce((s,v)=>s+v*v/base,0)/G;
  }
  near(C,row.matrix_pointwise_collision_envelope);near(success,row.actual_optimal_decoder_correct_probability);
  near(collision,row.actual_mean_weighted_likelihood_collision);assert.ok(collision<=C+1e-9);
  assert.ok(success<=Math.sqrt(C/G)+1e-9);POVMControls++;
}
for(const row of report.complete_native_source_controls) {
  const n=row.dimension,q=row.modulus,m=row.phase_qubits;let total=0;
  for(let ai=0;ai<q**(n*m);ai++) {
    const a=vec(ai,n*m,q);let C=0;
    for(let si=0;si<q**n;si++) {
      const s=vec(si,n,q);let product=1;
      for(let i=0;i<m;i++) {
        const t=s.reduce((z,v,j)=>z+v*a[j*m+i],0);
        product*=1+Math.cos(2*Math.PI*t/q)**2;
      }
      C+=product/q**n;nativeMatrixSecretPairs++;
    }
    total+=C/q**(n*m);nativeMatrices++;
  }
  near(total,row.actual_native_mean_collision_envelope);
  near(total,(3/2)**m+(2**m-(3/2)**m)/(q/2)**n);
}
let ledgers=0;
for(const row of [...report.native_near_entropy_width_ledgers,report.order_two_exception_ledger]) {
  const n=row.dimension,L=row.modulus_bits,m=row.phase_qubits,G=1n<<BigInt(n*L),Gh=1n<<BigInt(n*(L-1));
  let num=3n**BigInt(m)*(Gh-1n)+4n**BigInt(m),den=(1n<<BigInt(m))*Gh*G;
  if(num>=den){num=1n;den=1n;}
  eq(read(row.source_mean_uniform_secret_correct_probability_squared_upper_bound),[num,den]);
  assert.equal(row.conservative_correct_probability_dyadic_exponent,Math.floor(((den/num).toString(2).length-1)/2));
  assert.equal(row.adaptive_local_or_entangled_measurements_ruled_out,false);ledgers++;
}
const control=report.adaptive_scope_countercontrol;
for(let s=0;s<4;s++) {
  let success=0;
  for(let parity=0;parity<2;parity++)for(let high=0;high<2;high++) {
    const p2=(1+(-1)**parity*Math.cos(Math.PI*s))/2;
    const mean=parity===0?Math.cos(Math.PI*s/2):Math.sin(Math.PI*s/2);
    if(parity+2*high===s)success+=p2*(1+(-1)**high*mean)/2;
  }
  near(success,1);near(success,control.adaptive_every_secret_correct_probabilities[s]);
}
assert.ok(control.nonadaptive_matrix_pointwise_correct_probability_bound<1);
for(const [file,hash] of Object.entries(report.dependency_sha256))
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex'),hash);
assert.equal(report.claim_gate.speedup_claim_allowed,false);
console.log(JSON.stringify({status:'INDEPENDENT_BOUNDED_CODE_CROSSCHECK_NOT_THEOREM_REVIEW',POVMControls,
  nativeMatrices,nativeMatrixSecretPairs,exactLedgers:ledgers,adaptiveFixedSecretCountercontrols:4},null,2));
