"use strict";
// Independent exact sign mixing, complete collision censuses and conditional budgets.
// Supplied integers do not prove that a Gaussian sampler or producer exists.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),B=require("./native_basis_lottery_crosscheck.js");
const {check,rat,parse,str,add,sub,mul,div,cmp,one,zero}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/native_source_refresh.json");
const mod=(x,q)=>(x%q+q)%q,enc=x=>x<=9007199254740991n&&x>=-9007199254740991n?Number(x):String(x);
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const same=(a,b,msg)=>E.same(canonical(a),canonical(b),msg),digest=x=>crypto.createHash("sha256").update(JSON.stringify(canonical(x))).digest("hex"),hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const bits=x=>x===0n?0:x.toString(2).length,min=(a,b)=>cmp(a,b)<=0n?a:b,max=(a,b)=>cmp(a,b)>=0n?a:b;
function exact(x){check(typeof x==="number"?Number.isSafeInteger(x):typeof x==="string"&&/^-?(0|[1-9][0-9]*)$/.test(x),"canonical exact integer");const y=BigInt(x);same(enc(y),x,"canonical large integer encoding");return y;}
function root(q){check(q>=3n,"positive ternary root");let d=0;while(q%3n===0n){q/=3n;d++;}check(q===1n,"actual odd prime-power root");return d;}
function label(L){
  const n=L.dimension,d=L.root_digits,m=L.original_rows,k=L.output_rows,eta=parse(L.batch_label_TV_tolerance);
  check([n,d,m,k].every(x=>Number.isSafeInteger(x)&&x>0)&&n*d<=65536&&cmp(eta,zero)>0n&&cmp(eta,one)<0n,"whole label-quality scope");
  const N=3n**BigInt(n*d),F=div(rat(BigInt(k)**2n,4n),mul(eta,eta)),population=bits(N-1n),f=bits(F[0])-(bits(F[1])-1),e=population+f-m,upper=rat(1n,2n**BigInt(Math.min(64,Math.max(0,-e))));
  same(L,{dimension:n,root_digits:d,original_rows:m,output_rows:k,batch_label_TV_tolerance:str(eta),label_population_base3_exponent:n*d,
    nonzero_population_ceil_log2_upper:population,Markov_chi_square_factor:str(F),factor_power2_exponent_upper:f,label_quality_failure_power2_exponent_upper:e,
    label_quality_failure_upper:str(upper),exact_expected_chi_square_IF_small:m<=2048&&n*d<=2048?str(rat(N-1n,2n**BigInt(m))):null,
    expected_chi_square_formula:"(g^n-1)/2^m",IID_uniform_original_label_rows_required:true,sign_difference2_is_a_ring_unit:true,
    one_observed_full_rank_bank_quality_certified:false,rows_from_reused_parent_are_new_original_samples:false},"upward entropy/Markov certificate, not floats or rank assumption");
}
function source(S){
  const n=S.dimension,r=S.original_root_digits,m=S.original_rows,k=S.output_rows,a=parse(S.normalized_original_Gaussian_width),b=parse(S.normalized_target_Gaussian_width),el=parse(S.batch_label_TV_tolerance),en=parse(S.batch_noise_TV_tolerance),dmin=S.minimum_supported_root_digits,dmax=S.maximum_supported_root_digits;
  check(Number.isSafeInteger(r)&&r>0&&dmin>=1&&dmin<=dmax&&dmax<=r&&[a,b,el,en].every(x=>cmp(x,zero)>0n&&cmp(x,one)<0n)&&cmp(add(el,en),one)<0n,"valid widths, TV and complete root scope");
  label(S.maximum_root_label_quality_ledger);const L=S.maximum_root_label_quality_ledger;
  check(L.dimension===n&&L.root_digits===dmax&&L.original_rows===m&&L.output_rows===k&&L.batch_label_TV_tolerance===str(el),"same actual original/target label parameters");
  const D=dmax-dmin+1,lf=min(one,mul(rat(BigInt(D)),parse(L.label_quality_failure_upper))),floor=rat(BigInt(m),2n*3n**BigInt(2*dmin)),H=div(sub(div(mul(mul(en,en),mul(b,b)),rat(4n*BigInt(k))),floor),rat(2n)),energy=div(mul(rat(BigInt(m)),mul(a,a)),rat(6n)),nf=cmp(H,zero)>0n?min(one,div(energy,H)):one;
  const primitive=rat(1n,3n**BigInt(n)),p=S.ideal_target_source_producer_success_lower_EXTERNAL,delta=S.certified_complete_dither_sampler_TV_loss_EXTERNAL;
  [p,delta].forEach(v=>{if(v!==null){const x=parse(v);check(cmp(x,zero)>=0n&&cmp(x,one)<=0n,"valid individual external contract");}});
  let success=null;if(p!==null&&delta!==null){const x=parse(p),y=parse(delta);success=str(max(zero,sub(sub(sub(sub(x,el),en),primitive),y)));}
  same(S,{dimension:n,original_root_digits:r,original_rows:m,output_rows:k,minimum_supported_root_digits:dmin,maximum_supported_root_digits:dmax,
    normalized_original_Gaussian_width:str(a),normalized_target_Gaussian_width:str(b),batch_label_TV_tolerance:str(el),batch_noise_TV_tolerance:str(en),
    target_width_multiplier:str(div(b,a)),maximum_root_label_quality_ledger:L,reachable_fixed_roots_covered:D,all_reachable_label_quality_failure_upper:str(lf),
    normalized_rounding_energy_floor_upper:str(floor),common_continuous_original_energy_threshold:str(H),true_original_continuous_energy_expectation_upper_using_pi_gt3:str(energy),
    common_original_energy_failure_upper:str(nf),all_reachable_source_quality_failure_upper:str(min(one,add(lf,nf))),common_energy_event_is_nonvacuous:cmp(H,zero)>0n&&cmp(nf,one)<0n,
    uniform_to_primitive_masked_secret_TV:str(primitive),ideal_target_source_producer_success_lower_EXTERNAL:p,certified_complete_dither_sampler_TV_loss_EXTERNAL:delta,
    one_refresh_coverage_lower_IF_quality_and_external_contracts_hold:success,original_noise_independence_required_for_energy_Markov_bound:false,
    one_refresh_unconditional_coverage_lower_IF_source_and_external_contracts_hold:success===null?null:str(mul(sub(one,min(one,add(lf,nf))),parse(success))),
    sign_sum_error_and_label_independence_assumed:false,only_true_original_prefixes_covered:true,same_narrow_width_producer_advantage_inherited:false,
    actual_source_law_quality_sampler_or_producer_certified:false,coefficient_ambiguity_or_false_prefix_pruning_resolved:false},"common original energy, all-root label UNION and conditional coverage gate");
}
function canonicalNode(raw,scale0,prefix0){
  const q=exact(raw[0].modulus),scale=BigInt(scale0),n=raw[0].label.length;
  B.complete(raw,1n,Array(n).fill(0),0n);if(scale!==1n)root(scale);
  check(scale>=1n&&scale<q&&q%scale===0n,"nonterminal original cumulative scale");
  const P=prefix0.map(exact),g=q/scale;check(P.length===n&&P.every(x=>x>=0n&&x<scale),"canonical original prefix");
  const node={original_records_sha256:digest(raw),modulus:enc(g),original_scale:enc(scale),known_original_lower_prefix_IF_path_true:P.map(enc)},children=[],receipts=[];
  raw.forEach(r=>{const e=mod(BigInt(r.value)-r.label.reduce((v,a,i)=>v+BigInt(a)*P[i],0n),q),child={label:r.label.map(a=>enc(mod(BigInt(a),g))),value:enc(mod((e+scale/2n)/scale,g)),modulus:enc(g),source_id:r.source_id};children.push(child);receipts.push({source_id:r.source_id,original_record_sha256:digest(r),corrected_original_response:enc(e),derived_record:child});});
  return {canonical_node:node,canonical_node_sha256:digest(node),derived_records:children,record_receipts:receipts,
    original_records_paid_once:raw.length,original_response_rounding_evaluations:raw.length,source_IDs_preserved:true,
    true_prefix_or_noise_law_certified:false,new_original_samples_created:false};
}
function transform(raw,F){
  const q=exact(raw[0].modulus),g=exact(F.modulus),n=raw[0].label.length,m=raw.length,k=F.supplied_sign_rows.length;root(g);
  check(q%g===0n&&k>0,"actual original quotient and complete output batch");B.complete(raw,1n,Array(n).fill(0),0n);
  const scale=q/g,P=F.known_original_lower_prefix_IF_true.map(exact),z=F.supplied_secret_mask.map(exact),T=F.supplied_sign_rows,G=F.supplied_integer_dithers;G.forEach(exact);
  check(Number.isSafeInteger(F.max_entries)&&F.max_entries>0,"whole logical transform cap");
  check(P.length===n&&P.every(x=>x>=0n&&x<scale)&&z.length===n&&z.every(x=>x>=0n&&x<g)&&G.length===k&&T.every(row=>row.length===m&&row.every(t=>t===-1||t===1)),"canonical prefix/mask, signs and external integers");
  const entries=m*n+k*m+k*n,base={original_records_sha256:digest(raw),original_records_paid_once:m,modulus:enc(g),original_scale:enc(scale),known_original_lower_prefix_IF_true:P.map(enc),
    supplied_sign_rows:T,supplied_secret_mask:z.map(enc),supplied_integer_dithers:G,planned_transform_entries:entries,max_entries:F.max_entries,
    derived_original_record_count:0,original_response_rounding_evaluations:0,sign_label_accumulation_terms:0,sign_response_accumulation_terms:0,mask_dot_product_terms:0,
    producer_input:null,original_quotient_receipts:[],output_receipts:[],source_quality_or_true_prefix_established:false,supplied_dithers_certified_Gaussian:false,
    signs_and_mask_certified_IID_uniform:false,fresh_public_randomness_is_a_fresh_original_sample:false,actual_producer_or_quantum_algorithm_supplied:false};
  if(entries>F.max_entries){same(F,{...base,status:"WHOLE_REFRESH_TRANSFORM_CAP_EXCEEDED_NOT_SOURCE_FAILURE"},"no partially executed transform");return;}
  const derived=[],receipts=[];
  raw.forEach(r=>{const e=mod(BigInt(r.value)-r.label.reduce((v,a,i)=>v+BigInt(a)*P[i],0n),q),child={label:r.label.map(a=>enc(mod(BigInt(a),g))),value:enc(mod((e+scale/2n)/scale,g)),modulus:enc(g),source_id:r.source_id};derived.push(child);receipts.push({source_id:r.source_id,original_record_sha256:digest(r),corrected_original_response:enc(e),derived_record:child});});
  const labels=[],values=[],outputs=[];
  T.forEach((sign,j)=>{const a=Array.from({length:n},(_,i)=>mod(derived.reduce((v,r,h)=>v+BigInt(sign[h])*BigInt(r.label[i]),0n),g)),y=mod(derived.reduce((v,r,h)=>v+BigInt(sign[h])*BigInt(r.value),0n),g),shift=mod(a.reduce((v,x,i)=>v+x*z[i],0n),g),value=mod(y+BigInt(G[j])-shift,g);labels.push(a.map(enc));values.push(enc(value));outputs.push({output_index:j,ALL_original_source_IDs:raw.map(r=>r.source_id),signed_parent_response_modulus:enc(y),mask_response_shift:enc(shift),supplied_integer_dither:G[j],output_label:a.map(enc),output_response:enc(value)});});
  same(F,{...base,status:"ACTUAL_SIGN_MASK_TRANSFORM_WITH_UNCERTIFIED_EXTERNAL_DITHERS",derived_original_record_count:m,original_response_rounding_evaluations:m,
    sign_label_accumulation_terms:k*m*n,sign_response_accumulation_terms:k*m,mask_dot_product_terms:k*n,
    producer_input:{modulus:enc(g),labels,responses:values},original_quotient_receipts:receipts,output_receipts:outputs,producer_input_contains_signs_mask_prefix_or_source_metadata:false},"actual original-record sign/mask algebra, all ancestry and work");
}
function census(C){
  const n=C.dimension,d=C.root_digits,m=C.original_rows,q=3**d,N=q**n,banks=N**m,K=2**m;check(banks*K*m*n<=100000,"WHOLE finite matrix/sign census");
  const vector=x=>{const a=[];for(let j=0;j<n;j++){a.unshift(x%q);x=Math.floor(x/q);}return a;},labels=Array.from({length:N},(_,j)=>vector(j));
  let chi=zero,tv=zero,zeroTV=null;const histogram={};
  for(let code=0;code<banks;code++){
    let b=code;const rows=[];for(let j=0;j<m;j++){rows.push(labels[b%N]);b=Math.floor(b/N);}const counts=Array(N).fill(0);
    for(let sign=0;sign<K;sign++){
      const v=Array(n).fill(0);rows.forEach((a,h)=>a.forEach((x,i)=>v[i]+=((sign>>h)&1?1:-1)*x));
      const index=v.reduce((z,x)=>z*q+((x%q+q)%q),0);counts[index]++;
    }
    const c=rat(BigInt(N*counts.reduce((z,x)=>z+x*x,0)-K*K),BigInt(K*K)),t=rat(BigInt(counts.reduce((z,x)=>z+Math.abs(N*x-K),0)),BigInt(2*N*K));
    chi=add(chi,c);tv=add(tv,t);const key=str(t);histogram[key]=(histogram[key]||0)+1;if(code===0)zeroTV=t;
  }
  const meanChi=div(chi,rat(BigInt(banks))),meanTV=div(tv,rat(BigInt(banks))),expected=rat(BigInt(N-1),BigInt(K));
  check(cmp(meanChi,expected)===0n&&cmp(mul(meanTV,meanTV),div(meanChi,rat(4n)))<=0n,"exact collision expectation and Cauchy--Schwarz");
  same(C,{dimension:n,root_digits:d,original_rows:m,original_matrices_checked:banks,sign_rows_per_matrix:K,complete_label_accumulation_terms:banks*K*m*n,
    exact_mean_chi_square:str(meanChi),theoretical_exact_mean_chi_square:str(expected),exact_mean_conditional_label_TV:str(meanTV),zero_matrix_conditional_TV:str(zeroTV),
    conditional_TV_histogram:histogram,all_source_matrices_individually_uniform_claimed:false,finite_census_is_a_new_oracle_problem_or_candidate:false},"all original matrices and sign rows, not a favorable subset");return banks;
}
function verify(P){
  check(P.status==="SOURCE_REFRESH_ALGEBRA_ENTROPY_AND_COMMON_ENERGY_AUDIT_SAMPLER_AND_PRODUCER_MISSING"&&P.producer_sha256===hash(path.join(ROOT,"theorems/native_source_refresh.py"))&&P.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_SOURCE_REFRESH.md")),"current scoped source-refresh audit");
  const deps=["native_basis_lottery.py","native_affine_fibre_relaxation.py","native_classical_modulus_descent.py","native_gaussian_quotient_completion.py","native_small_multiple_completion.py","ternary_covariant_noise.py","ternary_noise_degradation.py","ternary_measured_lattice_decoder.py"];
  same(Object.keys(P.dependency_sha256).sort(),deps.sort(),"direct scientific dependencies");deps.forEach(f=>check(P.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  const C=P.actual_supplied_dither_control,raw=C.original_records,s=C.secret_AND_original_errors_FOR_CALIBRATION_ONLY.secret,e=C.secret_AND_original_errors_FOR_CALIBRATION_ONLY.errors,q=BigInt(raw[0].modulus);
  check(raw.length===5&&s.length===2&&e.length===5&&C.Gaussian_dithers_or_uniform_signs_mask_claimed===false,"non-Gaussian declared calibration scope");
  raw.forEach((r,j)=>check(mod(r.label.reduce((v,a,i)=>v+BigInt(a)*BigInt(s[i]),0n)+BigInt(e[j]),q)===BigInt(r.value),"actual original observations"));transform(raw,C.transform);
  const alias=P.false_prefix_calibration_alias;transform(raw,alias.transform);
  same(alias.transform.known_original_lower_prefix_IF_true,C.transform.known_original_lower_prefix_IF_true.map(x=>(x+1)%C.transform.original_scale),"explicit FALSE original prefix");
  same(alias.transform.producer_input,C.transform.producer_input,"finite rounding alias persists through sign/mask mixing");
  check(alias.same_producer_input===true&&alias.same_input_certifies_true_prefix===false&&alias.finite_alias_is_general_source_or_no_go===false,"same producer input is not a prefix certificate");
  check(P.complete_sign_collision_censuses.length===2&&P.width_and_root_scope_profiles.length===7,"declared census and scaling scope");
  const banks=P.complete_sign_collision_censuses.reduce((z,c)=>z+census(c),0);
  P.width_and_root_scope_profiles.forEach(S=>{if(S.status){let dmin=1,dmax=1;const n=S.dimension;while(3n**BigInt(dmin)<BigInt(n)**7n)dmin++;while(3n**BigInt(dmax+1)<=BigInt(n)**9n&&dmax+1<=n)dmax++;
    same(S,{dimension:n,status:"NO_DECLARED_ROOT_INTERVAL_ABOVE_ROUNDING_FLOOR",required_minimum_root_digits:dmin,available_maximum_root_digits:dmax},"unsupported root interval is not invented");check(dmin>dmax,"actually empty declared interval");}else source(S);});
  check(P.source_refresh_sampler_implemented===false&&P.source_conditioned_producer_amplification_established===false&&P.accepted_speedup_candidate===false&&P.new_active_negative_result_created===false&&P.novelty_claim===false,"no sampler/oracle/algorithm hidden in algebra");
  return {verified:true,complete_original_matrices_censused:banks,actual_sign_label_terms:C.transform.sign_label_accumulation_terms,
    conditional_width_profiles:P.width_and_root_scope_profiles.length,Gaussian_sampler_or_producer_supplied:false};
}
module.exports={verify,label,source,transform,census,canonicalNode};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));
