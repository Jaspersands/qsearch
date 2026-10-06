"use strict";
// Independent source coordinates, suffix DP, reversible ranking and full DFT.
const fs=require("fs"),path=require("path");
const r=JSON.parse(fs.readFileSync(path.join(__dirname,"../phase_workbench/cyclotomic_fiber_receiver.json"),"utf8"));
function check(v,m){if(!v)throw Error(m);}
function close(a,b,m){check(Math.abs(a-b)<5e-12,`${m}: ${a} != ${b}`);}
function mod(x,q){return((x%q)+q)%q;}
function same(a,b,m){check(JSON.stringify(a)===JSON.stringify(b),m);}
function betaRow(L){let u=2,v=-1;for(let j=1;j<L;j++)[u,v]=[-2*u-v,u-v];const d=3**Math.floor(L/2);return[u/d,v/d];}
function coordinates(y,L){const q=3**Math.ceil(L/2),[u,v]=betaRow(L),[a,b]=y;return[mod(u*a+v*b,q),mod((u+v)*a-u*b,q)];}
function tuples(q,n){return Array.from({length:q**n},(_,i)=>Array.from({length:n},(_,j)=>Math.floor(i/q**(n-j-1))%q));}
function key(v){return v.join(",");}
function value(f,w,q){return f[0][0].map((_,l)=>mod(f.reduce((v,row,i)=>v+(w[i] ? row[w[i]-1][l] : 0),0),q));}
function add(a,b,q){return a.map((x,j)=>mod(x+b[j],q));}
function multiply(a,b){return[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];}
function divide(a,b){const norm=b[0]**2+b[1]**2;return[(a[0]*b[0]+a[1]*b[1])/norm,(a[1]*b[0]-a[0]*b[1])/norm];}
function power(z,k){let result=[1,0];for(let i=0;i<k;i++)result=multiply(result,z);return result;}
function determinant(matrix){
  if(matrix.length===1)return BigInt(matrix[0][0]);
  return matrix[0].reduce((v,x,j)=>v+(j%2 ? -1n : 1n)*BigInt(x)*determinant(matrix.slice(1).map(row=>row.filter((_,k)=>k!==j))),0n);
}
function erasure(v){
  if(v.length===1)return v;
  let w=Array(v.length).fill(1/Math.sqrt(v.length));w[0]-=1;
  const norm=Math.sqrt(w.reduce((v,x)=>v+x*x,0));w=w.map(x=>x/norm);
  const inner=v.reduce((a,x,j)=>[a[0]+w[j]*x[0],a[1]+w[j]*x[1]],[0,0]);
  return v.map((x,j)=>[x[0]-2*w[j]*inner[0],x[1]-2*w[j]*inner[1]]);
}
let sourceLabels=0,words=0,complexAmplitudes=0,projectionControls=0,DFTOutcomes=0;
let generalTraceEntries=0,onehotControls=0,binaryBasisAmplitudes=0;
for(const c of r.general_prime_source_and_charged_onehot_controls){
  const p=c.prime,d=p-1,q=p**c.modulus_logp,L=d*c.modulus_logp,M=c.power_basis_frequency_matrix;
  check(q===c.modulus && L===c.native_full_ramification_level,"general source conductor");
  check(M.length===d && M.every(row=>row.length===d && row.every(Number.isSafeInteger)),"integer frequency basis");
  const det=determinant(M);check((det===1n || det===-1n) && det===BigInt(c.integer_matrix_determinant),"non-unimodular general source");
  // Independent complex-embedding trace, not the Python quotient-ring matrices.
  for(let j=1;j<p;j++)for(let l=0;l<d;l++){
    let trace=[0,0];
    for(let k=1;k<p;k++){
      const z=[Math.cos(2*Math.PI*k/p),Math.sin(2*Math.PI*k/p)];let lambda=[0,0];
      for(let a=0;a<j;a++){const term=power(z,a);lambda=[lambda[0]+term[0],lambda[1]+term[1]];}
      const term=divide(multiply(lambda,power(z,l)),power([z[0]-1,z[1]],L-1));
      trace=[trace[0]+q*term[0]/p,trace[1]+q*term[1]/p];
    }
    check(Math.abs(trace[0]-M[j-1][l])<2e-8 && Math.abs(trace[1])<2e-8,"general cyclotomic trace formula");generalTraceEntries++;
  }
  const frequencies=M.map(row=>mod(row.reduce((v,x,j)=>v+x*c.native_ring_label_coefficients[j],0),q));
  same(frequencies,c.independent_supplied_binary_phase_labels,"supplied frequencies/native label mismatch");
  const selected=[0,...Array.from({length:d},(_,j)=>2**j)],failed=Array.from({length:2**d},(_,i)=>i).filter(i=>!selected.includes(i));
  same(selected,c.accepted_binary_word_indices,"one-hot projector not public");same(failed,c.failed_binary_word_indices,"discarded projector failures");
  const supplied=Array.from({length:2**d},(_,word)=>{
    const phase=mod(c.integer_secret_calibration*frequencies.reduce((v,x,j)=>v+((word>>j)&1)*x,0),q),theta=2*Math.PI*phase/q;
    return[Math.cos(theta)/Math.sqrt(2**d),Math.sin(theta)/Math.sqrt(2**d)];
  });
  const success=selected.reduce((v,j)=>v+supplied[j][0]**2+supplied[j][1]**2,0);
  close(success,p/2**d,"charged one-hot acceptance");close(success,c.onehot_projection_probability,"reported one-hot acceptance");
  close(failed.reduce((v,j)=>v+supplied[j][0]**2+supplied[j][1]**2,0),c.failed_projection_probability,"charged one-hot rejection");
  selected.forEach((word,j)=>supplied[word].forEach((x,k)=>close(x/Math.sqrt(success),c.conditional_native_qudit_amplitudes[j][k],"conditional native phase amplitude")));
  const binaryCost=c.expected_binary_samples_per_native_qudit,nativeCost=c.expected_native_qudits_per_binary_sample;
  check(BigInt(binaryCost.numerator)*BigInt(p)===BigInt(binaryCost.denominator)*BigInt(d*2**d),"reverse source overhead hidden");
  check(BigInt(nativeCost.numerator)*2n===BigInt(nativeCost.denominator)*BigInt(p),"forward source overhead hidden");
  check(c.fresh_binary_registers_required===d && c.all_nonzero_native_frequencies_are_IID_uniform_Zq &&
    !c.inverse_from_one_native_qudit_or_cloning_granted && c.constant_overhead_requires_fixed_prime &&
    c.known_reduction_conformance_not_novel_algorithm,"known reduction overstated");
  onehotControls++;binaryBasisAmplitudes+=supplied.length;
}
for(const c of r.source_bijection_controls){
  const L=c.level,q=3**Math.ceil(L/2),a=3**Math.ceil(L/2),b=3**Math.floor(L/2),[u,v]=betaRow(L),seen=new Set();
  same(c.frequency_matrix,[[u,v],[u+v,-u]],"exact trace-coordinate matrix");
  check(-(u*u+u*v+v*v)===c.matrix_determinant,"wrong coordinate determinant");
  for(const y of tuples(a,1).flatMap(([x])=>tuples(b,1).map(([z])=>[x,z]))){
    const pair=coordinates(y,L);check(!seen.has(key(pair)),"source map not bijective");seen.add(key(pair));sourceLabels++;
    if(L%2)check(mod(pair[1]-2*pair[0],3)===0,"odd-level constraint absent");
  }
  check(seen.size===3**L && c.exhaustive_native_label_count===seen.size,"source entropy mismatch");
  if(L%2===0)check(seen.size===q*q && c.even_level_two_frequencies_independently_uniform,"native frequencies not uniform product");
}
for(const c of [...r.native_full_secret_receiver_controls,r.zero_information_countercontrol]){
  const q=c.full_secret_modulus,n=c.integer_secret_calibration.length,m=c.native_qutrits_consumed,N=q**n,D=3**m,zero=Array(n).fill(0);
  const f=c.native_labels.map(row=>{
    const columns=row.map(y=>coordinates(y,c.parent_level));return[0,1].map(j=>columns.map(x=>x[j]));
  });
  same(f,c.public_two_frequency_vectors,"native full-secret frequencies");
  const suffix=Array(m+1);suffix[m]=new Map([[key(zero),1]]);let additions=0;
  for(let i=m-1;i>=0;i--){
    suffix[i]=new Map();
    for(const [t,count]of suffix[i+1])for(let j=0;j<3;j++){
      const target=key(add(t.split(",").map(Number),j ? f[i][j-1] : zero,q));
      suffix[i].set(target,(suffix[i].get(target)||0)+count);additions++;
    }
  }
  same(suffix.map(x=>x.size),c.classical_DP_resources.suffix_layer_support_sizes,"DP layer supports");
  check(additions===c.classical_DP_resources.exact_count_additions,"hidden preprocessing");
  check(suffix.reduce((v,x)=>v+x.size,0)===c.classical_DP_resources.stored_count_entries,"DP memory omitted");
  for(const row of c.public_fiber_counts)check(suffix[0].get(key(row.target))===row.count,"fiber word multiplicity");
  const ranked=new Map([...suffix[0]].map(([t,count])=>[t,Array(count)]));
  function count(i,target,prefix,j){
    const v=j ? f[i][j-1] : zero;
    return suffix[i+1].get(key(target.map((t,l)=>mod(t-prefix[l]-v[l],q))))||0;
  }
  function unrank(target,rank){
    let prefix=zero.slice();const word=[];
    for(let i=0;i<m;i++)for(let j=0;j<3;j++){
      const cardinality=count(i,target,prefix,j);
      if(rank>=cardinality){rank-=cardinality;continue;}
      word.push(j);prefix=add(prefix,j ? f[i][j-1] : zero,q);break;
    }
    check(word.length===m && rank===0,"public inverse rank failed");return word;
  }
  for(const word of tuples(3,m)){
    const t=value(f,word,q);let rank=0,prefix=zero.slice();
    for(let i=0;i<m;i++){
      for(let j=0;j<word[i];j++)rank+=count(i,t,prefix,j);
      prefix=add(prefix,word[i] ? f[i][word[i]-1] : zero,q);
    }
    same(unrank(t,rank),word,"reversible native index erasure");
    const theta=2*Math.PI*mod(t.reduce((v,x,j)=>v+x*c.integer_secret_calibration[j],0),q)/q;
    check(ranked.get(key(t))[rank]===undefined,"rank collision");
    ranked.get(key(t))[rank]=[Math.cos(theta)/Math.sqrt(D),Math.sin(theta)/Math.sqrt(D)];words++;
  }
  const targets=tuples(q,n),erased=new Map();let leakage=0;
  for(const[t,v]of ranked){
    const clean=erasure(v);erased.set(t,clean[0]);
    leakage+=clean.slice(1).reduce((v,x)=>v+x[0]**2+x[1]**2,0);complexAmplitudes+=v.length;
  }
  close(leakage,c.rank_register_leakage_probability,"full known rank-unitary replay");
  const a=targets.map(t=>erased.get(key(t))||[0,0]);
  a.forEach((x,i)=>x.forEach((y,k)=>close(y,c.erased_target_amplitudes[i][k],"erased full-target amplitude")));
  const probabilities=targets.map(k=>{
    const v=a.reduce((v,x,j)=>{
      const theta=-2*Math.PI*mod(targets[j].reduce((v,t,l)=>v+t*k[l],0),q)/q;
      const phase=[Math.cos(theta),Math.sin(theta)],z=multiply(x,phase);return[v[0]+z[0]/Math.sqrt(N),v[1]+z[1]/Math.sqrt(N)];
    },[0,0]);return v[0]**2+v[1]**2;
  });
  probabilities.forEach((p,j)=>close(p,c.all_full_secret_Fourier_outcome_probabilities[j],"full vector Fourier readout"));
  close(probabilities.reduce((v,x)=>v+x,0)+leakage,1,"all outcomes charged");
  const secretIndex=targets.findIndex(t=>key(t)===key(c.integer_secret_calibration));
  close(probabilities[secretIndex],c.actual_full_secret_recovery_probability,"full secret not its low digit");
  const optimum=[...suffix[0].values()].reduce((v,count)=>v+Math.sqrt(count/D),0)**2/N;
  close(optimum,c.optimal_covariant_measurement_probability,"PGM formula");
  close(probabilities[secretIndex],optimum,"reference implements actual PGM");
  check(c.nonzero_rank_outcomes_retained_as_failure && !c.exponential_DP_preprocessing_ignored && !c.higher_secret_digits_discarded,"false efficient receiver promotion");
  for(const p of c.charged_vector_DCP_projection_controls){
    const theta=2*Math.PI*mod(p.binary_phase_label.reduce((v,x,j)=>v+x*c.integer_secret_calibration[j],0),q)/q;
    same(p.known_projector_basis_indices,[0,1],"unknown projection supplied");
    close(p.accepted_probability,2/3,"projection success");close(p.failed_probability,1/3,"dropped projector outcome");
    [[1/Math.sqrt(2),0],[Math.cos(theta)/Math.sqrt(2),Math.sin(theta)/Math.sqrt(2)]].forEach((x,j)=>x.forEach((v,k)=>close(v,p.conditional_binary_amplitudes[j][k],"native DCP bridge phase")));
    check(p.all_projector_outcomes_costed && p.full_integer_secret_retained && !p.arbitrary_Gaussian_DCP_merge_supplied,"DCP projection exaggerated");projectionControls++;
  }
  DFTOutcomes+=N;
}
for(const c of r.growing_parameter_ledgers){
  const exponent=c.vector_dimension*c.modulus_log3,N=3n**BigInt(exponent),D=N*81n,b=c.ideal_source_mean_PGM_success_lower_bound;
  check(c.raw_native_qutrits===exponent+4 && BigInt(c.explicit_DP_worst_case_group_states)===N,"hidden exponential table");
  check(BigInt(b.numerator)*(D+N-1n)===BigInt(b.denominator)*D,"source information bound");
  const entries=c.expected_final_DP_count_entries_lower_bound;
  check(BigInt(entries.numerator)*(D+N-1n)===BigInt(entries.denominator)*N*D,"sparse DP source cost omitted");
  check(!c.source_information_bound_is_new_algorithm && !c.classical_or_quantum_optimal_runtime_lower_bound_claimed,"reference cost became universal hardness");
}
check(Object.values(r.claim_gate).every(x=>x===false),"candidate promoted");
console.log(JSON.stringify({status:"independent_replay_passed",exhaustive_source_labels:sourceLabels,
  general_prime_trace_entries:generalTraceEntries,charged_onehot_controls:onehotControls,binary_product_amplitudes:binaryBasisAmplitudes,
  native_words_ranked_and_unranked:words,complex_native_amplitudes:complexAmplitudes,
  full_secret_Fourier_outcomes:DFTOutcomes,charged_DCP_projectors:projectionControls,new_algorithm:false}));
