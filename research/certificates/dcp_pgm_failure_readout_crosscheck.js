// Independent all-record circuit execution and rational source ledgers, not review.
const assert=require('assert/strict'),fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const report=JSON.parse(fs.readFileSync(path.join(root,'research/classical_baselines/dcp_pgm_failure_readout.json'),'utf8'));
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
const mul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];
const norm=a=>a[0]**2+a[1]**2;
const digits=(x,n,q)=>Array.from({length:n},()=>{const v=x%q;x=Math.floor(x/q);return v;}).reverse();
const parity=x=>{let p=0;while(x){p^=x&1;x>>=1;}return p;};
const zero=D=>Array.from({length:D},()=>[0,0]);
const read=r=>[BigInt('0x'+r.numerator_hex),BigInt('0x'+r.denominator_hex)];
const eq=(a,b)=>assert.equal(a[0]*b[1],b[0]*a[1]);
const number=r=>{const [a,b]=read(r);return Number(a)/Number(b);};
const add=(a,b)=>[a[0]*b[1]+b[0]*a[1],a[1]*b[1]];
const clamp=a=>a[0]>=a[1]?[1n,1n]:a;
const scale=(a,c)=>[a[0]*c,a[1]];
const rootDyadic=a=>a[0]===0n?{value:[0n,1n],exponent:null}:a[0]>=a[1]?{value:[1n,1n],exponent:0}:(()=>{
  const e=Math.floor(((a[1]/a[0]).toString(2).length-1)/2);return {value:[1n,1n<<BigInt(e)],exponent:e};})();// Exact conservative floor-log rounding.
const C=(r,i=0)=>[r,i],I=[[C(1),C(0)],[C(0),C(1)]];
const gates={I,'-I':I.map(r=>r.map(a=>a.map(v=>-v))),X:[[C(0),C(1)],[C(1),C(0)]],
  Z:[[C(1),C(0)],[C(0),C(-1)]],H:[[C(1/Math.sqrt(2)),C(1/Math.sqrt(2))],[C(1/Math.sqrt(2)),C(-1/Math.sqrt(2))]],
  S:[[C(1),C(0)],[C(0),C(0,1)]],T:[[C(1),C(0)],[C(0),C(Math.SQRT1_2,Math.SQRT1_2)]]};
let pureExecutions=0,completeRecordCells=0,rawLocalProbabilities=0;
for(const control of report.physical_processor_controls) {
  const A=control.labels,q=control.modulus,n=A.length,m=A[0].length,G=q**n,N=2**m,D=G*N;
  const sums=Array.from({length:N},(_,xi)=>{const x=digits(xi,m,2);return A.map(r=>r.reduce((z,a,i)=>z+a*x[i],0)%q);});
  const eta=Array(G).fill(0);for(const t of sums)eta[t.reduce((z,v)=>z*q+v,0)]++;
  assert.deepEqual(eta,control.fiber_counts);eq(read(control.clean_herald_exact),[BigInt(eta.reduce((z,v)=>z+v*v,0)),BigInt(N*N)]);
  const kicks=control.program.filter(op=>op.kind==='Q').length;assert.equal(kicks,control.output_projector_kicks);
  const weights=control.fault_law.map(r=>number(r.weight));near(weights.reduce((z,v)=>z+v,0),1);
  function phase(s,x,sign) {
    const secret=digits(s,n,q),theta=sign*2*Math.PI*secret.reduce((z,v,j)=>z+v*sums[x][j],0)/q;
    return C(Math.cos(theta),Math.sin(theta));
  }
  function had(v,candidate) {
    const out=zero(2*D);
    if(candidate)for(let s=0;s<G;s++)for(let z=0;z<G;z++)for(let x=0;x<N;x++)for(let a=0;a<2;a++) {
      const c=(-1)**parity(s&z)/Math.sqrt(G),i=2*(s*N+x)+a,j=2*(z*N+x)+a;
      out[i][0]+=c*v[j][0];out[i][1]+=c*v[j][1];
    }
    else for(let s=0;s<G;s++)for(let y=0;y<N;y++)for(let x=0;x<N;x++)for(let a=0;a<2;a++) {
      const c=(-1)**parity(y&x)/Math.sqrt(N),i=2*(s*N+y)+a,j=2*(s*N+x)+a;
      out[i][0]+=c*v[j][0];out[i][1]+=c*v[j][1];
    }
    return out;
  }
  function U(v,inverse=false) {
    const first=had(v,!inverse),second=first.map((a,i)=>mul(a,phase(Math.floor(i/(2*N)),Math.floor(i/2)%N,inverse?1:-1)));
    return had(second,inverse);
  }
  function auxiliary(v,gate) {
    const out=zero(2*D),matrix=gates[gate];assert.ok(matrix);
    for(let r=0;r<D;r++)for(let a=0;a<2;a++)for(let b=0;b<2;b++) {
      const z=mul(matrix[a][b],v[2*r+b]);out[2*r+a][0]+=z[0];out[2*r+a][1]+=z[1];
    }
    return out;
  }
  const table=[],baseline=[];
  for(let si=0;si<G;si++) {
    const s=digits(si,n,q),total=Array(2*D).fill(0),reference=Array(2*D).fill(0);
    for(let zi=0;zi<control.fault_law.length;zi++) {
      const {mask}=control.fault_law[zi],input=zero(2*D);
      for(let x=0;x<N;x++) {
        const sign=(-1)**digits(x,m,2).reduce((z,v,i)=>z+v*mask[i],0),p=phase(si,x,1);
        input[2*x]=p.map(v=>v*sign/Math.sqrt(N));
      }
      let state=U(input),ideal=state.map(a=>[...a]);
      const herald=state.reduce((z,a,i)=>z+(Math.floor(i/2)%N===0?norm(a):0),0);
      assert.ok(herald<=number(control.clean_herald_exact)+1e-9);
      for(let ri=0;ri<G;ri++)for(let y=0;y<N;y++) {
        const trial=digits(ri,n,q),bits=digits(y,m,2);let probability=1/G;
        for(let i=0;i<m;i++) {
          const theta=2*Math.PI*A.reduce((z,r,j)=>z+r[i]*(s[j]-trial[j]),0)/q;
          probability*=(1+(-1)**(bits[i]^mask[i])*Math.cos(theta))/2;
        }
        near(probability,norm(state[2*(ri*N+y)]));rawLocalProbabilities++;
      }
      for(const op of control.program) {
        if(op.kind==='aux'){state=auxiliary(state,op.gate);ideal=auxiliary(ideal,op.gate);continue;}
        let projected;
        if(op.kind==='P'){projected=U(U(state,true).map((a,i)=>i<2*N?a:C(0)));}
        else {assert.equal(op.kind,'Q');projected=state.map((a,i)=>Math.floor(i/2)%N===0?a:C(0));}
        const other=state.map((a,i)=>C(a[0]-projected[i][0],a[1]-projected[i][1]));
        const on=auxiliary(projected,op.on),off=auxiliary(other,op.off);
        state=on.map((a,i)=>C(a[0]+off[i][0],a[1]+off[i][1]));
        ideal=auxiliary(ideal,op.kind==='P'?op.on:op.off);
      }
      near(state.reduce((z,a)=>z+norm(a),0),1);near(ideal.reduce((z,a)=>z+norm(a),0),1);
      const distance=Math.sqrt(state.reduce((z,a,i)=>z+(a[0]-ideal[i][0])**2+(a[1]-ideal[i][1])**2,0));
      const tv=state.reduce((z,a,i)=>z+Math.abs(norm(a)-norm(ideal[i])),0)/2;
      const physical=control.physical_controls[si*control.fault_law.length+zi];
      assert.deepEqual(physical.secret,s);assert.deepEqual(physical.mask,mask);near(number(physical.weight),weights[zi]);
      near(distance,physical.state_distance);near(tv,physical.full_record_total_variation);near(herald,physical.raw_herald);
      near(physical.hybrid_state_distance_bound,2*kicks*Math.sqrt(herald));assert.ok(distance<=physical.hybrid_state_distance_bound+1e-8);
      let overlap=C(0);state.forEach((a,i)=>{const z=mul(C(ideal[i][0],-ideal[i][1]),a);overlap[0]+=z[0];overlap[1]+=z[1];});
      const length=Math.hypot(...overlap),factor=length?C(overlap[0]/length,-overlap[1]/length):C(1);
      const aligned=Math.sqrt(state.reduce((z,a,i)=>{const b=mul(a,factor);return z+(b[0]-ideal[i][0])**2+(b[1]-ideal[i][1])**2;},0));
      const trace=aligned*Math.sqrt(Math.max(0,1-aligned**2/4));near(trace,physical.pure_trace_distance);assert.ok(tv<=trace+1e-8);
      state.forEach((a,i)=>{total[i]+=weights[zi]*norm(a);reference[i]+=weights[zi]*norm(ideal[i]);});pureExecutions++;
    }
    total.forEach((v,i)=>{near(v,control.full_probabilities_by_secret[si][i]);near(reference[i],control.reference_probabilities_by_secret[si][i]);completeRecordCells++;});
    near(total.reduce((z,v)=>z+v,0),1);table.push(total);baseline.push(reference);
  }
  const optimal=records=>Array.from({length:2*D},(_,i)=>Math.max(...records.map(r=>r[i]))).reduce((z,v)=>z+v,0)/G;
  near(optimal(table),control.optimal_all_record_uniform_secret_success);near(optimal(baseline),control.matched_random_trial_product_readout_success);
  const tv=table.reduce((z,r,s)=>z+r.reduce((v,a,i)=>v+Math.abs(a-baseline[s][i]),0)/(2*G),0);
  near(tv,control.mean_full_record_total_variation);assert.ok(Math.abs(optimal(table)-optimal(baseline))<=tv+1e-9);
}
let exactLedgers=0;
for(const r of [...report.native_growing_ledgers,report.precision_floor_counterledger]) {
  const n=r.dimension,L=r.modulus_bits,m=r.phase_qubits,k=BigInt(r.maximum_output_projector_kicks);
  const G=1n<<BigInt(n*L),H=1n<<BigInt(n*(L-1)),N=1n<<BigInt(m);
  const B=clamp([3n**BigInt(m)*(H-1n)+4n**BigInt(m),N*G*H]),h=[N+G-1n,N*G],gain=scale(h,4n*k*k);
  eq(read(r.baseline_native_mean_success_squared_bound),B);eq(read(r.native_mean_clean_herald),h);
  eq(read(r.native_mean_trace_distance_gain_squared_bound),gain);
  const b=rootDyadic(B),g=rootDyadic(gain),ideal=clamp(add(b.value,g.value));
  eq(read(r.baseline_mean_success_dyadic_upper),b.value);eq(read(r.trace_gain_dyadic_upper),g.value);
  assert.equal(r.baseline_dyadic_exponent,b.exponent);assert.equal(r.gain_dyadic_exponent,g.exponent);
  eq(read(r.ideal_all_record_native_mean_success_upper),ideal);
  const upper=clamp(add(ideal,read(r.assumed_total_composed_output_trace_error_budget)));
  eq(read(r.all_record_native_mean_success_conservative_upper),upper);
  eq(read(r.common_mean_squared_success_bound),clamp(add(scale(B,2n),scale(h,8n*k*k))));
  assert.equal(r.conservative_all_record_success_dyadic_exponent,(upper[1]/upper[0]).toString(2).length-1);
  assert.equal(r.common_squared_bound_is_for_ideal_operations,true);
  assert.equal(r.arbitrary_terminal_collective_measurements_or_signal_interleavings_covered,false);exactLedgers++;
}
for(const [file,hash] of Object.entries(report.dependency_sha256))
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex'),hash);
for(const key of ['independent_review','candidate_record_accepted','novelty_claim','speedup_claim_allowed','general_collective_or_QSVT_impossibility'])assert.equal(report.claim_gate[key],false);
console.log(JSON.stringify({status:'INDEPENDENT_ALL_RECORD_CODE_CROSSCHECK_NOT_PROOF_REVIEW',
  processorControls:report.physical_processor_controls.length,pureExecutions,completeRecordCells,rawLocalProbabilities,exactLedgers},null,2));
