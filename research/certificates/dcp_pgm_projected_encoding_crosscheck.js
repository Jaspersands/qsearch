// Independent structured public-unitary execution; not independent proof review.
const assert=require('assert/strict'),fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const report=JSON.parse(fs.readFileSync(path.join(root,'research/classical_baselines/dcp_pgm_projected_encoding.json'),'utf8'));
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
const read=r=>[BigInt('0x'+r.numerator_hex),BigInt('0x'+r.denominator_hex)];
const eq=(a,b)=>assert.equal(a[0]*b[1],b[0]*a[1]);
const digits=(x,n,q)=>Array.from({length:n},()=>{const t=x%q;x=Math.floor(x/q);return t;}).reverse();
const parity=x=>{let p=0;while(x){p^=x&1;x>>=1;}return p;};
const zero=D=>Array.from({length:D},()=>[0,0]);
const mul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];
const norm=a=>a[0]**2+a[1]**2;
const sqrt=x=>{if(x<2n)return x;let a=1n<<BigInt(Math.ceil(x.toString(2).length/2));while(true){const b=(a+x/a)/2n;if(b>=a)return a;a=b;}};
let actualUnknownInputs=0,blockColumns=0;
for(const control of report.physical_controls) {
  const A=control.labels,q=control.modulus,n=A.length,m=A[0].length,G=q**n,N=2**m,D=G*N;
  const sums=Array.from({length:N},(_,xi)=>{
    const x=digits(xi,m,2);return A.map(r=>r.reduce((z,a,i)=>z+a*x[i],0)%q);
  });
  const eta=Array(G).fill(0);for(const t of sums)eta[t.reduce((z,v)=>z*q+v,0)]++;
  assert.deepEqual(eta,control.fiber_counts);
  function phase(s,x,sign) {
    const secret=digits(s,n,q),theta=sign*2*Math.PI*secret.reduce((z,v,j)=>z+v*sums[x][j],0)/q;
    return [Math.cos(theta),Math.sin(theta)];
  }
  function had(v,candidate) {
    const result=zero(D);
    if(candidate)for(let s=0;s<G;s++)for(let z=0;z<G;z++)for(let x=0;x<N;x++) {
      const c=(-1)**parity(s&z)/Math.sqrt(G);
      result[s*N+x][0]+=c*v[z*N+x][0];result[s*N+x][1]+=c*v[z*N+x][1];
    }
    else for(let s=0;s<G;s++)for(let y=0;y<N;y++)for(let x=0;x<N;x++) {
      const c=(-1)**parity(y&x)/Math.sqrt(N);
      result[s*N+y][0]+=c*v[s*N+x][0];result[s*N+y][1]+=c*v[s*N+x][1];
    }
    return result;
  }
  function apply(v,inverse=false) {
    const first=had(v,!inverse);
    const second=first.map((a,i)=>mul(a,phase(Math.floor(i/N),i%N,inverse?1:-1)));
    return had(second,inverse);
  }
  for(let x=0;x<N;x++) {
    const v=zero(D);v[x]=[1,0];const out=apply(v),back=apply(out,true);
    back.forEach((a,i)=>{near(a[0],i===x?1:0);near(a[1],0);});
    for(let s=0;s<G;s++) {
      const e=phase(s,x,-1);near(out[s*N][0],e[0]/Math.sqrt(G*N));near(out[s*N][1],e[1]/Math.sqrt(G*N));
    }
    blockColumns++;
  }
  const S2=eta.reduce((z,v)=>z+v*v,0);
  eq(read(control.raw_herald_exact),[BigInt(S2),BigInt(N*N)]);
  eq(read(control.raw_correct_exact),[1n,BigInt(G)]);
  eq(read(control.raw_conditional_correct_exact),[BigInt(N*N),BigInt(G*S2)]);
  const positive=eta.filter(v=>v>0);
  eq(read(control.supported_singular_value_condition_number_squared),[BigInt(Math.max(...positive)),BigInt(Math.min(...positive))]);
  near(control.ideal_PGM_success,eta.reduce((z,v)=>z+Math.sqrt(v),0)**2/(G*N));
  for(const row of control.physical_controls) {
    const table=[];let totalCorrect=0;
    for(let s=0;s<G;s++) {
      const input=zero(D);for(let x=0;x<N;x++){const a=phase(s,x,1);input[x]=[a[0]/Math.sqrt(N),a[1]/Math.sqrt(N)];}
      let state=apply(input);
      for(let k=0;k<row.physical_reflection_rounds;k++) {
        state=state.map((a,i)=>a.map(v=>v*(i%N===0?1:-1)));
        state=apply(state,true).map((a,i)=>a.map(v=>v*(i<N?1:-1)));
        state=apply(state).map(a=>a.map(v=>-v));
      }
      const probabilities=Array.from({length:G},(_,r)=>norm(state[r*N]));table.push(probabilities);
      const herald=probabilities.reduce((z,v)=>z+v,0),correct=probabilities[s];totalCorrect+=correct/G;
      const stored=row.every_secret_physical_probabilities[s];assert.deepEqual(stored.secret,digits(s,n,q));
      near(herald,stored.herald);near(correct,stored.correct_unconditional);near(1-herald,stored.failed_herald);
      near(state.reduce((z,a)=>z+norm(a),0),1);near(stored.total_physical_norm,1);
      probabilities.forEach((v,r)=>near(v,row.heralded_output_probabilities_by_secret[s][r]));actualUnknownInputs++;
    }
    const sigma=eta.map(v=>Math.sqrt(v/N)),p=sigma.map(v=>Math.sin(row.degree*Math.asin(Math.min(1,v))));
    near(totalCorrect,sigma.reduce((z,v,i)=>z+v*p[i],0)**2/G);
    near(totalCorrect,row.spectral_correct_unconditional);
    near(row.spectral_herald,sigma.reduce((z,v,i)=>z+v*v*p[i]*p[i],0));
    const optimal=Array.from({length:G},(_,r)=>Math.max(...table.map(v=>v[r]))).reduce((z,v)=>z+v,0)/G;
    near(optimal,row.optimal_classical_label_guess_uniform_secret_unconditional);
    assert.ok(optimal<=Math.min(1,Math.PI**2*row.degree**2/(4*G))+1e-9);
  }
}
let completeNativeMatrices=0;
for(const row of report.complete_native_sources) {
  const {n,q,m}=row,G=q**n,N=2**m,M=q**(n*m);let S2=0;
  for(let ai=0;ai<M;ai++) {
    const flat=digits(ai,n*m,q),A=Array.from({length:n},(_,j)=>flat.slice(j*m,(j+1)*m)),eta=Array(G).fill(0);
    for(let xi=0;xi<N;xi++) {
      const x=digits(xi,m,2),t=A.map(r=>r.reduce((z,a,i)=>z+a*x[i],0)%q);
      eta[t.reduce((z,v)=>z*q+v,0)]++;
    }
    S2+=eta.reduce((z,v)=>z+v*v,0);completeNativeMatrices++;
  }
  eq(read(row.exact_mean_raw_herald),[BigInt(S2),BigInt(M*N*N)]);
  eq(read(row.exact_mean_raw_herald),[BigInt(N+G-1),BigInt(N*G)]);
  eq(read(row.exact_pooled_conditional_correct),[BigInt(N),BigInt(N+G-1)]);
  eq(read(row.unconditional_correct),[1n,BigInt(G)]);
}
for(const r of report.native_growing_ledgers) {
  const G=1n<<BigInt(r.dimension*r.modulus_bits),N=1n<<BigInt(r.phase_qubits),d=BigInt(r.degree);
  eq(read(r.native_mean_raw_herald_probability),[N+G-1n,N*G]);
  eq(read(r.native_pooled_correct_probability_given_raw_herald),[N,N+G-1n]);
  eq(read(r.raw_comparison_unconditional_correct_probability),[1n,G]);
  const num=5n*d*d,den=2n*G;
  eq(read(r.odd_bounded_polynomial_correct_probability_upper_bound),num>=den?[1n,1n]:[num,den]);
  assert.equal(r.conservative_correct_probability_dyadic_exponent,(den/num).toString(2).length-1);
  const k=BigInt('0x'+r.minimum_degree_necessary_for_target_success);
  let expect=sqrt(G/5n);if(expect*expect*5n<G)expect++;
  assert.equal(k,expect);assert.equal(r.arbitrary_interleaved_algorithms_or_other_encodings_ruled_out,false);
}
for(const [file,hash] of Object.entries(report.dependency_sha256))
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex'),hash);
assert.ok(Object.values(report.claim_gate).every(v=>v===false));
assert.equal(report.easy_binary_family_countercontrol.direct_correct_probability,1);
assert.equal(report.easy_binary_family_countercontrol.general_hidden_subgroup_hardness_inferred,false);
console.log(JSON.stringify({status:'INDEPENDENT_LANGUAGE_PHYSICAL_CODE_CHECK_NOT_PROOF_REVIEW',
  actualUnknownInputs,blockColumns,completeNativeMatrices,exactGrowingLedgers:report.native_growing_ledgers.length},null,2));
