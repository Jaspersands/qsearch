"use strict";
// Actual native words, exact cyclotomic effects and integer degree prices.
// This is not an independent proof of the general Markov derivative theorem.
const fs=require("fs"),path=require("path"),crypto=require("crypto"),E=require("./cyclotomic_exact.js");
const {check,rat,parse,str,add,sub,mul,div,cmp,zero,one}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/native_word_spectral_filter_audit.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const same=(a,b,m)=>E.same(canonical(a),canonical(b),m),mod=(a,q)=>(a%q+q)%q;
const min=(a,b)=>cmp(a,b)<=0n?a:b,max=(a,b)=>cmp(a,b)>=0n?a:b;
function* words(q,n,p=[]){if(p.length===n){yield p;return;}for(let t=0;t<q;t++)yield*words(q,n,[...p,t]);}
function binomial(n,k){let x=1n;for(let j=1;j<=k;j++)x=x*BigInt(n-j+1)/BigInt(j);return x;}
function value(C,x){let y=zero;for(let j=C.length-1;j>=0;j--)y=add(mul(y,x),C[j]);return y;}
function coefficients(S){
  const d=S.degree,f=S.family;check(Number.isSafeInteger(d)&&d>=0&&d<=32,"whole finite polynomial cap");
  let C,reason;
  if(f==="GEOMETRIC"&&d>=1){C=[zero,...Array.from({length:d},(_,j)=>rat((j%2===0?1n:-1n)*binomial(d,j+1)))];reason="1-(1-x)^d belongs to [0,1] on [0,1]";}
  else if(f==="CHEBYSHEV_ENDPOINT"&&d>=1){
    let prev=[one],cur=[rat(-1n),rat(2n)];
    for(let j=1;j<d;j++){const next=Array.from({length:cur.length+1},()=>zero);cur.forEach((c,i)=>{next[i]=sub(next[i],mul(rat(2n),c));next[i+1]=add(next[i+1],mul(rat(4n),c));});prev.forEach((c,i)=>next[i]=sub(next[i],c));prev=cur;cur=next;}
    C=cur.map(c=>mul(rat(d%2===0?-1n:1n,2n),c));C[0]=add(C[0],rat(1n,2n));reason="(1-(-1)^d*T_d(2x-1))/2 belongs to [0,1] on [0,1]";
  } else if(f==="NONZERO_KERNEL_BIAS"&&d===1){C=[rat(1n,3n),rat(2n,3n)];reason="1/3+2*x/3 belongs to [0,1] on [0,1]";}
  else if(f==="CONSTANT"&&d===0){C=[rat(1n,3n)];reason="constant 1/3";}
  else throw Error("analytically globally bounded family required");
  same(S.ascending_coefficients,C.map(str),"exact whole polynomial");
  check(S.global_effect_range==="[0,1] on ALL x in [0,1]"&&S.global_range_certificate===reason&&S.polynomial_selected_independently_of_original_values===true&&S.filter_physical_QSVT_implementation_supplied===false,"global range and legal selection, no free circuit");
  return C;
}
function control(C){
  const raw=C.original_records,q=raw[0].modulus,n=raw[0].label.length,M=raw.length/2,mask=C.known_mask,D=3**M;
  check(Number.isSafeInteger(M)&&M>0&&D<=256&&q<=81&&mask.length===n,"finite paired native control");
  const K=E.field(q),ids=new Set();
  raw.forEach(r=>{check(r.modulus===q&&r.label.length===n&&typeof r.source_id==="string"&&r.source_id.length>0&&!ids.has(r.source_id),"original bank IDs and shape");ids.add(r.source_id);[...r.label,r.value,...mask].forEach(x=>check(Number.isSafeInteger(x)&&x>=0&&x<q,"canonical original values"));});
  const rows=[],groups=new Map();
  for(const w of words(3,M)){
    const beta=w.flatMap(t=>[[1,0],[-1,1],[0,-1]][t]);
    const frequency=Array.from({length:n},(_,i)=>mod(beta.reduce((s,b,j)=>s+b*raw[j].label[i],0),q));
    const phase=mod(beta.reduce((s,b,j)=>s+b*(raw[j].value+raw[j].label.reduce((v,a,i)=>v+a*mask[i],0)),0),q);
    rows.push({word:w,frequency,known_phase:phase});const key=JSON.stringify(frequency);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(phase);
  }
  same(C.actual_native_word_rows,rows,"all actual original word/phase rows");
  let collision=zero;groups.forEach(phases=>collision=add(collision,rat(BigInt(phases.length**2),BigInt(D**2))));
  check(C.word_dimension===D&&C.supported_frequency_count===groups.size&&C.collision_probability===str(collision),"actual unbalanced collision mass");
  C.spectral_filter_controls.forEach(F=>{
    const S=F.filter,coeff=coefficients(S),p0=value(coeff,zero);
    let source=K.scale(K.unit,p0),nullMean=p0,ideal=zero;
    groups.forEach(phases=>{
      const p=rat(BigInt(phases.length),BigInt(D)),v=value(coeff,p),weight=div(sub(v,p0),rat(BigInt(D*phases.length)));
      nullMean=add(nullMean,div(sub(v,p0),rat(BigInt(D))));ideal=add(ideal,mul(p,v));
      phases.forEach(a=>phases.forEach(b=>source=K.plus(source,K.scale(K.powers[mod(b-a,q)],weight))));
    });
    const gap=K.plus(source,K.scale(K.unit,mul(rat(-1n),nullMean)));
    const bound=min(one,mul(rat(BigInt(S.degree**2)),add(collision,rat(1n,BigInt(D)))));
    same(F.exact_source_acceptance_root_polynomial,K.encode(source),"exact native spectral effect");
    same(F.exact_source_minus_IID_null_root_polynomial,K.encode(gap),"exact source/null gap");
    check(F.IID_null_acceptance===str(nullMean)&&F.ideal_source_acceptance_IF_codeword===str(ideal)&&F.absolute_source_null_gap_upper===str(bound),"trace, ideal reference and Markov price");
    check(K.eq(source,K.conj(source))&&E.sign(K,source)>=0&&E.sign(K,K.plus(K.unit,K.scale(source,rat(-1n))))>=0,"exact positive effect probability");
    [1n,-1n].forEach(sign=>check(E.sign(K,K.plus(K.scale(K.unit,bound),K.scale(gap,rat(sign))))>=0,"exact source gap within scoped bound"));
    const l1=coeff.reduce((s,c)=>add(s,rat(c[0]<0n?-c[0]:c[0],c[1])),zero),shadow=F.matched_classical_monomial_estimator;
    check(shadow.coefficient_l1_norm===str(l1)&&shadow.maximum_words_per_monomial_shot===S.degree+1&&shadow.coefficient_norm_and_inverse_precision_are_not_free===true&&shadow.polynomial_time_classical_dequantization_established===false,"matched estimator has paid coefficient norm, not universal dequantization");
  });
  check(C.dense_control_is_scalable_circuit===false&&C.IID_label_source_law_established_by_this_fixture===false,"finite source scope");return D;
}
function floorSqrt(N){if(N<2n)return N;let x=1n<<BigInt(Math.ceil(N.toString(2).length/2));while(true){const y=(x+N/x)/2n;if(y>=x)return x;x=y;}}
function ledger(L){
  const n=L.dimension,r=L.root_digits,s=L.word_surplus;[n,r,s].forEach(x=>check(Number.isSafeInteger(x)&&x>0,"positive scalable scope"));check(n*r<=16384,"exact degree bit scope");
  const gamma=parse(L.required_decision_gap),eps=parse(L.uniform_effect_error_each_ensemble),delta=parse(L.preparation_trace_error_each_ensemble);
  check(cmp(gamma,zero)>0n&&cmp(gamma,one)<=0n&&cmp(eps,zero)>=0n&&cmp(eps,one)<=0n&&cmp(delta,zero)>=0n&&cmp(delta,one)<=0n,"implementation budgets");
  const residual=max(zero,sub(sub(gamma,mul(rat(2n),eps)),mul(rat(2n),delta))),factor=add(one,rat(2n,3n**BigInt(s))),squared=div(mul(residual,rat(3n**BigInt(n*r))),factor);
  let d=floorSqrt(squared[0]/squared[1]);if(d*d*squared[1]<squared[0])d++;
  check(L.word_sites===n*r+s&&L.frequency_population_base3_exponent===n*r&&L.residual_exact_filter_gap_required===str(residual)&&BigInt(L.minimum_acceptance_polynomial_degree_under_scoped_model)===d&&L.degree_lower_bound_bit_length===(d?d.toString(2).length:0),"exact conservative ensemble degree certificate");
  same(L.expected_collision_plus_inverse_word_dimension_upper,{coefficient:str(factor),base:3,exponent:-n*r},"symbolic collision bound without astronomical decimal probabilities");
  ["label_only_globally_bounded_raw_Gram_filter_required","IID_full_root_original_labels_and_IID_uniform_null_values_required","arbitrary_original_source_phase_noise_is_allowed_in_upper_bound","mask_may_depend_on_original_values_IF_fibre_constant"].forEach(k=>check(L[k]===true,"required premise "+k));
  ["balanced_fibres_or_per_matrix_uniformity_assumed","coefficients_may_depend_on_original_values","degree_bound_is_a_general_quantum_query_lower_bound","efficient_different_preconditioner_or_noncommuting_measurement_excluded","actual_quantum_decision_algorithm_supplied"].forEach(k=>check(L[k]===false,"scope not generalized "+k));
}
function census(C){
  const n=C.dimension,r=C.root_digits,M=C.word_sites,q=3**r,D=3**M,banks=q**(2*M*n),work=banks*D*M*n;
  check(work<=10000,"complete label/word census cap");let sum=zero;
  for(const A of words(q,2*M*n)){
    const counts=new Map();for(const w of words(3,M)){const f=Array(n).fill(0);w.forEach((t,j)=>{const [a,c]=[[1,0],[-1,1],[0,-1]][t];for(let i=0;i<n;i++)f[i]=mod(f[i]+a*A[2*j*n+i]+c*A[(2*j+1)*n+i],q);});const key=JSON.stringify(f);counts.set(key,(counts.get(key)||0)+1);}counts.forEach(c=>sum=add(sum,rat(BigInt(c*c),BigInt(D*D))));
  }
  const mean=div(sum,rat(BigInt(banks))),expected=add(rat(1n,BigInt(q**n)),div(sub(one,rat(1n,BigInt(q**n))),rat(BigInt(D))));
  check(C.complete_original_label_banks===banks&&C.complete_coordinate_accumulation_terms===work&&C.exact_mean_collision_probability===str(mean)&&C.theoretical_collision_probability===str(expected)&&cmp(mean,expected)===0n&&C.census_is_new_oracle_problem_or_algorithm_candidate===false,"complete exact collision census");
}
function verify(R){
  check(R.status==="RAW_WORD_GRAM_BOUNDED_SPECTRAL_FILTER_DEGREE_AND_ENSEMBLE_SCOPE_AUDIT"&&R.producer_sha256===hash(path.join(ROOT,"theorems/native_word_spectral_filter_audit.py"))&&R.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_WORD_SPECTRAL_FILTER_AUDIT.md")),"current mathematical provenance");
  const deps=["native_basis_lottery.py","native_full_root_slice.py","native_word_span_decision.py","native_small_multiple_completion.py","ternary_measured_lattice_decoder.py","ternary_noise_degradation.py"];
  same(Object.keys(R.dependency_sha256).sort(),deps.sort(),"direct dependencies");deps.forEach(f=>check(R.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(R.actual_native_source_controls.length===4&&R.scaling_degree_ledgers.length===4&&R.complete_label_source_collision_censuses.length===3,"declared complete control scope");
  const total=R.actual_native_source_controls.reduce((s,c)=>s+control(c),0);R.scaling_degree_ledgers.forEach(ledger);R.complete_label_source_collision_censuses.forEach(census);
  control(R.concentrated_labels_countercontrol);check(R.concentrated_labels_countercontrol.collision_probability==="1"&&R.concentrated_labels_countercontrol.spectral_filter_controls[0].IID_null_acceptance==="1/9","not every fixed public matrix is flat");
  same(R.unbounded_rescaling_countercontrol,{balanced_supported_eigenvalue:"1/81",candidate_degree1_polynomial:"81*x",value_at_supported_eigenvalue:"1",value_at_x1:"81",valid_globally_bounded_filter:false,cheap_normalized_block_encoding_supplied:false},"spectral rescaling violates global boundedness");
  same(R.data_dependent_coefficients_countercontrol,{effect:"P_y(x)=1 if ALL original values are0, else0",polynomial_degree:0,fixed_zero_secret_noiseless_calibration_acceptance:"1",IID_uniform_null_acceptance_with4_original_values_mod3:"1/81",original_values_enter_effect_selection:true,label_only_filter_model_applies:false,is_hard_source_or_algorithm_candidate:false},"response-dependent effect is outside null trace model");
  check(R.accepted_speedup_candidate===false&&R.new_active_negative_result_created===false&&R.all_quantum_measurements_or_preconditioners_excluded===false&&R.research_decision==="DO_NOT_TREAT_RAW_FRAME_QSVT_AS_FREE_NORMALIZATION_SEARCH_STRUCTURAL_PRECONDITIONERS_OR_NONCOMMUTING_TESTS","no unproved global exclusion or speedup");
  return {verified:true,actual_native_word_rows:total,exact_spectral_filters:R.actual_native_source_controls.reduce((s,c)=>s+c.spectral_filter_controls.length,0),complete_label_censuses:3,scaling_degree_ledgers:4,general_quantum_lower_bound_claimed:false};
}
module.exports={verify,control,ledger,census,coefficients};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));
