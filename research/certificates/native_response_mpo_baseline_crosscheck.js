"use strict";
// Independent rounded dense kernels, product-width controls and paid ledgers.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),R0=require("./native_banded_qft_baseline_crosscheck.js");
const {check,rat,parse,str,add,sub,mul,cmp,zero,one}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/classical_baselines/native_response_mpo_baseline.json");
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
const sorted=x=>Array.isArray(x)?x.map(sorted):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,sorted(x[k])])):x;
const same=(a,b,msg)=>check(JSON.stringify(sorted(a))===JSON.stringify(sorted(b)),msg);
function I(s){check(typeof s==="string"||Number.isSafeInteger(s),"exact integer encoding");
  return typeof s==="string"&&s.startsWith("-0x")?-BigInt(s.slice(1)):BigInt(s);}
const abs=x=>x<0n?-x:x,ar=a=>[abs(a[0]),a[1]],max=(a,b)=>cmp(a,b)>0n?a:b;
const gadd=(a,b)=>[a[0]+b[0],a[1]+b[1]],gmul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],conj=a=>[a[0],-a[1]];
const norm=a=>a[0]*a[0]+a[1]*a[1],mod=(a,q)=>(a%q+q)%q;
const cLog=x=>x===1n?0:(x-1n).toString(2).length;
const jsonInt=x=>abs(x)>9007199254740991n?String(x):Number(x);
const encoded=x=>abs(x).toString(2).length<=4096?String(x):(x<0n?"-":"")+"0x"+abs(x).toString(16);
const gsame=(a,b,msg)=>check(a.length===b.length&&a.every((x,i)=>I(x)===b[i]),msg);
function* words(n,p=[]){if(!n){yield p;return;}for(let x=0;x<3;x++)yield* words(n-1,[...p,x]);}
const idx=w=>w.reduce((a,x)=>3*a+x,0);

function ledger(M,b,steps,f,full){
  const S=steps.length,Q=steps.filter(s=>s[0]==="fourier").length;
  let target=null;if(full){target=64n*BigInt(Math.max(1,Q)*M)*2n**BigInt(f);b=1;let p=3n;while(b<M&&p<target){b++;p*=3n;}}
  const P=f+cLog(128n*BigInt(S*M)*3n**BigInt(M)),K=f+cLog(8n*BigInt(M));
  const eps=rat(4n,2n**BigInt(P)),eta=mul(rat(2n*3n**BigInt(M)*BigInt(M)),eps),error=mul(rat(BigInt(2*S)),eta);
  const phase=mul(rat(2n),error),grid=rat(BigInt(2*M),2n**BigInt(K));let omitted=zero;
  if(full)for(let d=b;d<M;d++)omitted=add(omitted,rat(BigInt(M-d),3n**BigInt(d+1)));
  const trunc=mul(rat(BigInt(Q)*176n,7n),omitted),total=add(add(phase,grid),trunc);
  check(cmp(total,rat(1n,2n**BigInt(f)))<=0n&&cmp(mul(rat(BigInt(S)),eta),rat(1n,2n))<=0n,"nonvacuous operator/normalization budget");
  return {word_sites_M:M,operations_S:S,Fourier_calls_Q:Q,requested_accuracy_bits_f:f,target_full_cyclic:full,
    selected_bandwidth_b:b,full_cyclic_cutoff_threshold:target===null?null:String(target),phase_grid_bits_P:P,random_bits_per_digit_K:K,
    root_error_upper:str(eps),per_operation_operator_error_upper:str(eta),unnormalized_state_error_upper:str(error),
    normalized_phase_TV_upper:str(phase),random_grid_TV_upper:str(grid),all_QFT_truncations_TV_upper:str(trunc),
    per_sample_TV_upper_under_IID_bits:str(total),MPO_bond_upper:jsonInt(3n**BigInt(b-1)),MPS_bond_upper:jsonInt(3n**BigInt(Q*(b-1))),
    intermediate_integer_bits_upper:2*M*S*(P+4)+4*(M+1)*Q*(b-1)+4*M+4,
    polynomial_structural_simulation_requires_fixed_Q:true,polynomial_Q_or_exponential_accuracy_is_not_covered:true,
    rare_prefix_precision_or_free_normalization_assumed:false};
}

function verifyControl(C){
  const R=C.model,q=I(R.modulus_q),ph=R.public_digit_phase_tables.map(row=>row.map(I)),M=ph.length,steps=R.schedule;
  check(q>=2n&&M>=1&&ph.every(row=>row.length===3&&row.every(x=>x>=0n&&x<q)),"canonical public phases");
  check(steps.length>=1&&steps.every(s=>s.length===2&&["phase","fourier"].includes(s[0])&&[-1,1].includes(s[1])),"fixed signed schedule");
  const L=R.accuracy_and_width_ledger;
  same(L,ledger(M,L.selected_bandwidth_b,steps,L.requested_accuracy_bits_f,L.target_full_cyclic),"global error/call/width ledger");
  const b=L.selected_bandwidth_b,P=L.phase_grid_bits_P,K=L.random_bits_per_digit_K,scale=2n**BigInt(P),roots=new Map();
  const eps=parse(L.root_error_upper);
  for(const receipt of R.phase_grid){
    const t=parse(receipt.turn),z=receipt.integer_value.map(I);check(z.length===2&&cmp(t,zero)>=0n&&cmp(t,one)<0n&&!roots.has(str(t)),"unique phase grid");
    const intervals=R0.rootInterval(t,P);let err=zero;
    intervals.forEach((bounds,i)=>{const value=rat(z[i],scale);
      err=add(err,max(ar(sub(bounds[0],value)),ar(sub(bounds[1],value))));});
    check(cmp(err,eps)<=0n&&cmp(parse(receipt.Arb_complex_l1_error_upper),eps)<=0n&&
      receipt.enclosure_bits<=R.resource_policy.max_enclosure_bits,"independent root error and declared cap");
    roots.set(str(t),z);
  }
  const root=t=>{t=rat(mod(t[0],t[1]),t[1]);check(roots.has(str(t)),"root missing");return roots.get(str(t));};
  const expected=new Set();const denom=3n**BigInt(b);
  for(let r=0n;r<denom;r++)expected.add(str(rat(r,denom)));
  for(const [kind,s] of steps)if(kind==="phase")for(const row of ph)for(const x of row)expected.add(str(rat(mod(BigInt(s)*x,q),q)));
  same([...roots.keys()].sort(),[...expected].sort(),"roots precompiled before output randomness");
  let bonds=Array(M+1).fill(1),profiles=[],entries=[],blocks=0,compiler=0;
  for(const [kind,s] of steps){
    if(kind==="phase")compiler+=12*bonds.slice(0,M).reduce((sum,L,j)=>sum+L*bonds[j+1],0);
    else {
      if(s===-1)bonds.reverse();
      for(let j=0;j<M;j++){const DL=3**Math.min(b-1,j);blocks+=9*DL;compiler+=36*DL*bonds[j]*bonds[j+1];}
      for(let j=1;j<M;j++)bonds[j]*=3**Math.min(b-1,j);
      if(s===1)bonds.reverse();
    }
    profiles.push([...bonds]);entries.push(6*bonds.slice(0,M).reduce((sum,L,j)=>sum+L*bonds[j+1],0));
  }
  same(R.bond_profiles,profiles,"actual preflight bond growth including reversed ordering");same(R.planned_tensor_entries,entries,"tensor entry charging");
  const envEntries=2*bonds.reduce((s,x)=>s+x*x,0);
  check(R.planned_environment_entries===envEntries&&envEntries<=R.resource_policy.max_environment_entries,"separate environment storage");
  const W=R.observed_work,count=C.sampling.samples.length;
  const envTerms=12*bonds.slice(0,M).reduce((s,l,j)=>s+l*bonds[j+1]**2+l*l*bonds[j+1],0);
  const sampleTerms=12*bonds.slice(0,M).reduce((s,l,j)=>s+l*bonds[j+1]+bonds[j+1]**2+bonds[j+1],0);
  check(W.complex_matrix_products===6*M+9*M*count&&W.underlying_FLINT_integer_matrix_products===4*W.complex_matrix_products&&
    W.readout_integer_scalar_multiply_terms_upper===envTerms+count*sampleTerms&&W.compiler_integer_scalar_multiply_terms_upper===compiler&&
    W.MPO_block_accumulations===blocks&&W.digit_reversals===L.Fourier_calls_Q,"matrix/block/reversal work replay");
  check(W.compiled_tensor_entries_peak===Math.max(...entries)&&W.random_bits_consumed===count*M*K&&
    W.maximum_integer_bits_seen>=2*M*steps.length*P-1&&W.maximum_integer_bits_seen<=L.intermediate_integer_bits_upper,"precision and random-bit cost");
  check(W.complex_matrix_products<=R.resource_policy.max_readout_complex_matrix_products&&
    W.dense_word_table_or_state_allocated_by_sampler===false&&W.SVD_or_bond_truncation_used===false&&W.private_secret_or_errors_used===false&&
    R.normalization_is_exact_integer_not_postselection===true&&R.unknown_coset_copy_access_is_not_public_phase_access===true&&
    R.peak_process_memory_or_runtime_is_not_certified===true&&R.secret_recovery_or_new_quantum_speedup_claimed===false,"scope and paid operations");
  const raw=C.original_records,mask=C.public_mask,pairs=[[1n,0n],[-1n,1n],[0n,-1n]];
  check(raw.length===2*M&&new Set(raw.map(r=>r.source_id)).size===2*M&&raw.every(r=>I(r.modulus)===q),"same original bank");
  const phases=Array.from({length:M},(_,j)=>pairs.map(([a,b])=>{
    const r0=raw[2*j],r1=raw[2*j+1];let x=a*I(r0.value)+b*I(r1.value);
    mask.forEach((z,k)=>{x+=(a*I(r0.label[k])+b*I(r1.label[k]))*I(z);});return String(mod(x,q));
  }));same(R.public_digit_phase_tables,phases,"public-data phase mechanism, no private errors");

  let vector=null,localVectors=null;
  if(M<=3){
    const all=[...words(M)],D=all.length;
    const kernel=all.map(a=>all.map(w=>{
      let z=[1n,0n];for(let j=0;j<M;j++){
        let t=rat(BigInt(a[j]*w[j]),3n);
        for(let d=1;d<=Math.min(b-1,j);d++)t=add(t,rat(BigInt(a[j-d]*w[j]),3n**BigInt(d+1)));
        z=gmul(z,root(t));
      }return z;
    }));
    vector=all.map(()=>[1n,0n]);
    for(const [kind,s] of steps){
      if(kind==="phase")vector=vector.map((z,i)=>all[i].reduce((a,x,j)=>gmul(a,root(rat(BigInt(s)*ph[j][x],q))),z));
      else if(s===1){const output=all.map(()=>[0n,0n]);for(let a=0;a<D;a++){
        output[idx([...all[a]].reverse())]=kernel[a].reduce((z,c,w)=>gadd(z,gmul(c,vector[w])),[0n,0n]);}vector=output;}
      else vector=all.map((_,w)=>all.reduce((z,a,j)=>gadd(z,gmul(conj(kernel[j][w]),vector[idx([...a].reverse())])),[0n,0n]));
    }
    check(C.small_calibration_integer_statevector.length===D,"complete small calibration");
    C.small_calibration_integer_statevector.forEach((z,i)=>gsame(z,vector[i],"independent rounded dense operator state"));
  }else check(C.small_calibration_integer_statevector.length===0,"no growing dense state");
  if(Math.max(...bonds)===1){
    check(b===1,"product width calibration");localVectors=ph.map(()=>[[1n,0n],[1n,0n],[1n,0n]]);
    const F=Array.from({length:3},(_,a)=>Array.from({length:3},(_,w)=>root(rat(BigInt(a*w),3n))));
    for(const [kind,s] of steps){
      if(kind==="phase")localVectors=localVectors.map((v,j)=>v.map((z,x)=>gmul(z,root(rat(BigInt(s)*ph[j][x],q)))));
      else {
        if(s===-1)localVectors.reverse();
        localVectors=localVectors.map(v=>Array.from({length:3},(_,a)=>v.reduce((z,c,w)=>gadd(z,gmul(s===1?F[a][w]:conj(F[w][a]),c)),[0n,0n])));
        if(s===1)localVectors.reverse();
      }
    }
    check(C.product_width_calibration_site_vectors.length===M,"complete product-width calibration");
    C.product_width_calibration_site_vectors.forEach((site,j)=>site.forEach((z,x)=>gsame(z,localVectors[j][x],"independent product-state kernel")));
  }else check(C.product_width_calibration_site_vectors.length===0,"no unjustified product factorization");
  for(const sample of C.sampling.samples){
    const digits=sample.site_digits_MSB_first,draws=sample.uniform_grid_draws;
    check(digits.length===M&&draws.length===M&&digits.every(x=>[0,1,2].includes(x)),"sample/bit-draw shape");
    let prefix=[];
    for(let j=0;j<M;j++){
      const u=I(draws[j]);check(u>=0n&&u<2n**BigInt(K),"canonical K-bit uniform draw");
      let masses=null;
      if(vector){masses=[0n,0n,0n];[...words(M)].forEach((w,i)=>{
        if(prefix.every((x,k)=>w[k]===x))masses[w[j]]+=norm(vector[i]);});
        const trace=sample.trace[j];same(trace.prefix,prefix,"exact small prefix");
        trace.child_weights.forEach((x,i)=>check(I(x)===masses[i],"dense prefix marginal"));
        check(I(trace.uniform_grid_integer)===u&&trace.selected_digit===digits[j],"trace draw and selection");
      }else if(localVectors)masses=localVectors[j].map(norm);
      if(masses){const total=masses.reduce((a,b)=>a+b,0n);check(total>0n,"nonzero parent");let cumulative=0n,d=0;
        for(;d<3;d++){cumulative+=masses[d];if(u*total<cumulative*2n**BigInt(K))break;}
        check(d===digits[j],"independent exact sampling choice");}
      prefix.push(digits[j]);
    }
    if(M<=3)check(sample.trace.length===M,"complete small trace");else check(sample.trace.length===0,"growing trace compact");
  }
  const total=mul(rat(BigInt(count)),parse(L.per_sample_TV_upper_under_IID_bits));
  check(C.sampling.batch_TV_upper_under_IID_bits===str(cmp(total,one)>0n?one:total)&&
    C.sampling.injected_PRNG_is_a_formal_IID_certificate===false&&C.growing_nonproduct_outcomes_independently_recomputed===false,"sampling premises and scope");
  return {sites:M,Fourier_calls:L.Fourier_calls_Q,max_stored_bond:Math.max(...profiles.flat()),
    outcome_replay:vector?"DENSE_CALIBRATION":localVectors?"EXACT_PRODUCT_CALIBRATION":"NOT_RECOMPUTED"};
}

function verify(R){
  check(R.status==="PUBLIC_PHASE_FIXED_LAYER_MPO_CLASSICAL_SAMPLING_BASELINE"&&
    R.producer_sha256===hash(path.join(ROOT,"theorems/native_response_mpo_baseline.py"))&&
    R.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_RESPONSE_MPO_BASELINE.md"))&&
    R.contract_sha256===hash(path.join(ROOT,"research/hypotheses/native_response_mpo_baseline_contract.json")),"current provenance");
  const deps=["native_banded_qft_baseline.py","native_response_fourier_factorization_audit.py","native_full_root_slice.py",
    "native_basis_lottery.py","ternary_noise_degradation.py","ternary_measured_lattice_decoder.py"];
  same(Object.keys(R.dependency_sha256).sort(),deps.sort(),"direct scientific dependencies");
  deps.forEach(p=>check(R.dependency_sha256[p]===hash(path.join(ROOT,"theorems",p)),"dependency "+p));
  check(R.controls.length===5,"finite and growing controls");const controls=R.controls.map(verifyControl);
  const steps=R.controls[0].model.schedule;
  check(R.full_cyclic_fixed_layer_profiles.length===3,"symbolic full-cyclic profiles");
  R.full_cyclic_fixed_layer_profiles.forEach(L=>same(L,ledger(L.word_sites_M,1,steps,L.requested_accuracy_bits_f,true),"every Fourier truncation paid"));
  check(R.fixed_Q_inverse_polynomial_accuracy_has_polynomial_structural_bound===true&&R.arbitrary_polynomial_depth_simulation_claimed===false&&
    R.unknown_phase_copy_simulation_claimed===false&&R.accepted_speedup_candidate===false&&R.new_active_negative_result_created===false,"bounded research decision");
  return {verified:true,controls,accepted_speedup_candidate:false};
}
module.exports={verify,verifyControl,ledger};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(REPORT,"utf8"))),null,2));
