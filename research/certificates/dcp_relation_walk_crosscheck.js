// Independent signed-swap, weighted-Laplacian and native dictionary checks.
// No uniform collision finder and no independent mathematical review.
const assert=require('assert/strict'),fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const report=JSON.parse(fs.readFileSync(path.join(root,'research/phase_workbench/dcp_relation_walk_stationarity.json'),'utf8'));
const F=(A,q,x)=>A.map(row=>row.reduce((s,a,j)=>s+a*(x>>j&1),0)%q);
const vec=(x,n,q)=>Array.from({length:n},()=>{const t=x%q;x=Math.floor(x/q);return t;});
const eq=(a,b)=>assert.equal(a[0]*b[1],b[0]*a[1]);
const read=a=>[BigInt(a.sign)*BigInt(a.numerator_hex),BigInt(a.denominator_hex)];
const cap=(num,den)=>num>=den?[1n,1n]:[num,den];
let swapWords=0,sourceEvents=0,fixedSecretLaplacians=0,edges=0;
const swap=report.actual_signed_relation_swap,A=swap.labels,q=swap.modulus,delta=swap.signed_relation;
const support=delta.reduce((s,d,j)=>s+Number(d!==0)*2**j,0);
const positive=delta.reduce((s,d,j)=>s+Number(d===1)*2**j,0),negative=support^positive;
swap.full_basis_permutation.forEach((y,x)=>{
  const expected=[positive,negative].includes(x&support)?x^support:x;
  assert.equal(y,expected);assert.equal(swap.full_basis_permutation[y],x);
  assert.deepEqual(F(A,q,x),F(A,q,y));swapWords++;
});
for(const row of report.complete_native_short_relation_source_controls) {
  const m=row.columns,q=row.modulus,relations=[];
  for(let code=0;code<3**m;code++) {
    const d=vec(code,m,3).map(x=>x-1),weight=d.filter(x=>x!==0).length;
    if(weight>0&&weight<=row.support_threshold&&d.find(x=>x!==0)===1)relations.push(d);
  }
  assert.equal(relations.length,row.all_canonical_signed_relations);
  const hits=Array(relations.length).fill(0);let any=0;
  for(let ai=0;ai<q**m;ai++) {
    const a=vec(ai,m,q);let seen=false;
    relations.forEach((d,j)=>{
      const sum=a.reduce((s,x,k)=>s+x*d[k],0);
      if((sum%q+q)%q===0){hits[j]++;seen=true;}sourceEvents++;
    });
    any+=Number(seen);
  }
  hits.forEach(h=>assert.equal(h,q**(m-1)));
  assert.equal(any,row.actual_tables_with_any_short_relation);
}
for(const row of report.actual_nonzero_fiber_Laplacian_controls) {
  const A=row.labels,q=row.modulus,n=A.length,N=2**row.Boolean_width;
  const target=Array.from({length:N},(_,x)=>F(A,q,x));
  let allFiberEdges=0;
  for(let x=0;x<N;x++)for(let y=0;y<x;y++)
    if(target[x].every((t,j)=>t===target[y][j]))allFiberEdges++;
  assert.equal(allFiberEdges,row.explicit_fiber_edges.length);
  const degrees=Array(N).fill(0);
  row.explicit_fiber_edges.forEach(([x,y,w])=>{degrees[x]+=w;degrees[y]+=w;});
  const mean=degrees.reduce((s,x)=>s+x,0)/N,variance=degrees.reduce((s,x)=>s+x*x,0)/N-mean*mean;
  assert.ok(variance>0);
  assert.ok(Math.abs(variance-row.non_Laplacian_adjacency_source_energy_variance)<1e-9);
  assert.equal(row.all_fiber_preserving_Hamiltonians_leave_state_unchanged,false);
  for(let si=0;si<q**n;si++) {
    const s=vec(si,n,q),state=target.map(t=>{
      const angle=2*Math.PI*t.reduce((z,x,j)=>z+x*s[j],0)/q;
      return [Math.cos(angle)/Math.sqrt(N),Math.sin(angle)/Math.sqrt(N)];
    }),result=Array.from({length:N},()=>[0,0]);
    row.explicit_fiber_edges.forEach(([x,y,w])=>{
      assert.ok(w>0);assert.deepEqual(target[x],target[y]);
      const re=w*(state[x][0]-state[y][0]),im=w*(state[x][1]-state[y][1]);
      result[x][0]+=re;result[x][1]+=im;result[y][0]-=re;result[y][1]-=im;
    });
    assert.ok(result.every(([re,im])=>Math.hypot(re,im)<1e-9));fixedSecretLaplacians++;
  }
  edges+=row.explicit_fiber_edges.length;
}
let ledgers=0;
for(const row of report.native_label_adaptive_dictionary_ledgers) {
  const m=BigInt(row.columns),w=row.excluded_relation_support;
  let combination=1n,count=0n;
  for(let k=1;k<=w;k++) {
    combination=combination*(m-BigInt(k)+1n)/BigInt(k);
    count+=combination*(1n<<BigInt(k-1));
  }
  assert.equal(count,BigInt(row.signed_relation_classes_of_support_at_most_threshold));
  const B=row.dimension*row.modulus_bits,G=1n<<BigInt(B);
  eq(read(row.any_short_relation_native_probability_union_upper_bound),cap(count,G));
  eq(read(row.on_no_short_relation_event_uniform_word_dictionary_applicability_upper_bound),
     cap(BigInt(row.listed_relation_count),1n<<BigInt(w)));
  const source=cap(count,G),active=cap(BigInt(row.listed_relation_count),1n<<BigInt(w));
  eq(read(row.unconditional_native_applicability_probability_upper_bound),
     cap(source[0]*active[1]+active[0]*source[1],source[1]*active[1]));
  const exponent=Math.max(0,B-(count-1n).toString(2).length);
  assert.equal(exponent,row.conservative_short_relation_failure_dyadic_exponent);
  assert.equal(row.label_adaptive_choice_of_the_entire_dictionary_allowed,true);
  assert.equal(row.arbitrary_quantum_walks_or_collective_measurements_ruled_out,false);ledgers++;
}
for(const [file,hash] of Object.entries(report.dependency_sha256))
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex'),hash);
assert.equal(report.claim_gate.speedup_claim_allowed,false);
console.log(JSON.stringify({status:'INDEPENDENT_BOUNDED_CODE_CROSSCHECK_NOT_THEOREM_REVIEW',swapWords,sourceEvents,
  fixedSecretLaplacians,explicitFiberEdges:edges,exactNativeDictionaryLedgers:ledgers},null,2));
