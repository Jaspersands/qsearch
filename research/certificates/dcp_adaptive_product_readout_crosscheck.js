// Independent-language bounded arithmetic/instrument checks, not theorem review.
const assert=require('assert/strict'),fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const report=JSON.parse(fs.readFileSync(path.join(root,'research/classical_baselines/dcp_adaptive_product_readout_bound.json'),'utf8'));
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
const read=r=>[BigInt('0x'+r.numerator_hex),BigInt('0x'+r.denominator_hex)];
const eq=(a,b)=>assert.equal(a[0]*b[1],b[0]*a[1]);
const number=r=>{const [a,b]=read(r);return Number(a)/Number(b);};
const vec=(x,n,q)=>Array.from({length:n},()=>{const y=x%q;x=Math.floor(x/q);return y;});
const cmul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];
const cadd=(a,b)=>[a[0]+b[0],a[1]+b[1]];
function weight4(delta) {
  const nz=delta.filter(v=>v!==0);
  if(nz.length && Math.abs(nz.at(-1))===1)return 0;
  return delta.reduce((z,v)=>z*(v===0?6:Math.abs(v)===1?4:1),1);
}
let physicalTrees=0,physicalLeafSecretPairs=0,compiledCoefficients=0;
for(const control of report.actual_instrument_controls) {
  const A=control.labels,q=control.modulus,n=A.length,m=A[0].length,G=q**n;
  const deltas=Array.from({length:5**m},(_,i)=>vec(i,m,5).map(v=>v-2));
  const coeff=new Map(deltas.map(d=>[d.join(','),[0,0]]));
  for(const evaluation of control.evaluations) {
    let success=0,collision=0;const normalization=Array(G).fill(0);
    near(evaluation.leaf_reference_probabilities_and_effects.reduce((z,r)=>z+r.reference_probability,0),1);
    assert.equal(evaluation.tree_leaves,evaluation.leaf_reference_probabilities_and_effects.length);
    for(const leaf of evaluation.leaf_reference_probabilities_and_effects) {
      const Q=leaf.reference_probability,es=leaf.effects;
      assert.equal(es.length,m);near(Q,es.reduce((z,e)=>z*e[0],1));
      for(const e of es) {
        assert.ok(e[0]>0);assert.ok(e.slice(1).reduce((z,x)=>z+x*x,0)<=1+1e-9);
        if(evaluation.refined){near(e[1]**2+e[2]**2,1);near(e[3],0);}
      }
      const values=Array.from({length:G},(_,si)=>{
        const s=vec(si,n,q);let v=1;
        for(let i=0;i<m;i++) {
          const theta=2*Math.PI*A.reduce((z,r,j)=>z+r[i]*s[j],0)/q;
          v*=1+es[i][1]*Math.cos(theta)+es[i][2]*Math.sin(theta);
        }
        normalization[si]+=Q*v;physicalLeafSecretPairs++;return v;
      });
      success+=Q*Math.max(...values)/G;
      collision+=Q*values.reduce((z,v)=>z+v*v,0)/G;
      if(evaluation.refined)for(const d of deltas) {
        let z=[Q,0];
        for(let i=0;i<m;i++) {
          let a=[es[i][1],-es[i][2]];
          if(d[i]<0)a=[a[0],-a[1]];
          if(d[i]===0)a=[1.5,0];
          else if(Math.abs(d[i])===2){a=cmul(a,a);a=[a[0]/4,a[1]/4];}
          z=cmul(z,a);
        }
        coeff.set(d.join(','),cadd(coeff.get(d.join(',')),z));
      }
    }
    normalization.forEach(v=>near(v,1));near(success,evaluation.optimal_classical_record_success);
    near(collision,evaluation.weighted_collision);physicalTrees++;
  }
  let envelope=0,actual=[0,0];
  for(const row of control.refined_fourier_coefficients) {
    const d=row.delta,z=coeff.get(d.join(','));near(z[0],row.real);near(z[1],row.imaginary);
    assert.ok(Math.hypot(...z)<=weight4(d)/4**m+1e-8);
    if(A.every(r=>r.reduce((v,a,i)=>v+a*d[i],0)%q===0)) {
      actual=cadd(actual,z);envelope+=weight4(d)/4**m;
    }
    compiledCoefficients++;
  }
  near(envelope,number(control.fixed_matrix_refined_collision_envelope));near(actual[1],0);
  near(actual[0],control.evaluations[1].weighted_collision);
  assert.ok(control.evaluations[1].optimal_classical_record_success**2<=envelope/G+1e-9);
  assert.ok(control.evaluations[0].weighted_collision<=control.evaluations[1].weighted_collision+1e-9);
  assert.ok(control.evaluations[0].optimal_classical_record_success<=control.evaluations[1].optimal_classical_record_success+1e-9);
}
near(report.actual_instrument_controls[0].evaluations[0].optimal_classical_record_success,1);
let nativeMatrices=0,targetFibers=0;
for(const row of report.complete_source_envelopes) {
  const {n,q,m}=row,G=q**n,M=q**(n*m),N=2**m;
  let weightSum=0,first=0,second=0,pgm=0;
  for(let ai=0;ai<M;ai++) {
    const flat=vec(ai,n*m,q),A=Array.from({length:n},(_,j)=>flat.slice(j*m,(j+1)*m));
    for(let di=0;di<5**m;di++) {
      const d=vec(di,m,5).map(v=>v-2);
      if(A.every(r=>r.reduce((z,a,i)=>z+a*d[i],0)%q===0))weightSum+=weight4(d);
    }
    const eta=Array(G).fill(0);
    for(let xi=0;xi<N;xi++) {
      const x=vec(xi,m,2),t=A.map(r=>r.reduce((z,a,i)=>z+a*x[i],0)%q);
      eta[t.reduce((z,v,j)=>z+v*q**j,0)]++;
    }
    first+=eta.reduce((z,v)=>z+v,0);second+=eta.reduce((z,v)=>z+v*v,0);
    pgm+=eta.reduce((z,v)=>z+Math.sqrt(v),0)**2/(N*G*M);
    targetFibers+=G;nativeMatrices++;
  }
  assert.equal(row.complete_label_matrices,M);
  eq(read(row.exact_mean_collision_envelope),[BigInt(weightSum),BigInt(M*4**m)]);
  eq(read(row.exact_mean_uniform_target_fiber_count),[BigInt(first),BigInt(M*G)]);
  eq(read(row.exact_mean_uniform_target_fiber_second_moment),[BigInt(second),BigInt(M*G)]);
  assert.equal(second*G,M*N*(N+G-1));near(pgm,row.actual_source_mean_collective_PGM_success);
  eq(read(row.collective_PGM_mean_success_lower_bound),[BigInt(N),BigInt(N+G-1)]);
  assert.ok(pgm>=N/(N+G-1)-1e-9);
}
let strictEntropyWidthComparisons=0,vacuousLedgers=0;
for(const r of report.growing_ledgers) {
  const n=r.dimension,L=r.modulus_bits,m=r.phase_qubits;
  const G=1n<<BigInt(n*L),H=1n<<BigInt(n*(L-1)),N=1n<<BigInt(m);
  const three=3n**BigInt(m),four=4n**BigInt(m),eight=8n**BigInt(m);
  const num=5n*G*(three*(H-1n)+four)+H*(eight+4n*three-5n*four);
  const den=5n*N*G*G*H;
  eq(read(r.unclamped_source_mean_success_squared_envelope),[num,den]);
  eq(read(r.source_mean_success_squared_upper_bound),num>=den?[1n,1n]:[num,den]);
  eq(read(r.uniform_target_fiber_mean),[N,G]);
  eq(read(r.uniform_target_fiber_second_moment),[N*(N+G-1n),G*G]);
  eq(read(r.collective_PGM_source_mean_success_lower_bound),[N,N+G-1n]);
  const gap=N*N*den>num*(N+G-1n)**2n;
  assert.equal(r.collective_lower_exceeds_adaptive_upper,gap);
  assert.equal(gap,r.density_surplus===0);if(gap)strictEntropyWidthComparisons++;
  assert.equal(r.bound_is_vacuous,num>=den);if(num>=den)vacuousLedgers++;
  assert.equal(r.label_adaptive_ordering_revisiting_or_quantum_memory_covered,false);
  assert.equal(r.collective_PGM_efficient_implementation_supplied,false);
  assert.equal(r.speedup_claim_allowed,false);
}
for(const [file,hash] of Object.entries(report.dependency_sha256))
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex'),hash);
assert.ok(Object.values(report.claim_gate).every(v=>v===false));
console.log(JSON.stringify({status:'INDEPENDENT_LANGUAGE_CODE_CHECK_NOT_THEOREM_REVIEW',physicalTrees,
  physicalLeafSecretPairs,compiledCoefficients,nativeMatrices,targetFibers,
  exactGrowingLedgers:report.growing_ledgers.length,strictEntropyWidthComparisons,vacuousLedgers},null,2));
