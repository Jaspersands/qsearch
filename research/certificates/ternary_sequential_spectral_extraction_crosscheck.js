"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,same,rat,zero,one,add,mul,div,str,parse,cmp,mod,field,sign,signCertificate,matrices}=require("./cyclotomic_exact.js");
const root=path.join(__dirname,"../.."),reportPath=process.argv[2]||path.join(root,"research/classical_baselines/ternary_sequential_spectral_extraction.json");
const R=JSON.parse(fs.readFileSync(reportPath,"utf8")),hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
for(const flag of["classical_model_construction_from_native_input_supplied","native_noisy_decoder_supplied","quantum_speedup_proved","candidate_record_accepted","novelty_claim"])check(R[flag]===false,"unsupported research claim: "+flag);
const key=JSON.stringify,dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
check(R.derivation_sha256===hash(path.join(root,"research/TERNARY_SEQUENTIAL_SPECTRAL_EXTRACTION.md")),"pinned derivation");
check(R.source_report==="research/classical_baselines/ternary_character_synchronization.json"&&R.source_report_sha256===hash(path.join(root,R.source_report)),"pinned native source");
const source=JSON.parse(fs.readFileSync(path.join(root,R.source_report),"utf8"));
same(R.commuting_native_label_controls.map(c=>c.source_seed),[89513,89523,89533],"committed source controls");
check(R.noncommuting_native_label_controls.length===2,"both noncommuting orders required");
let trajectories=0,words=0,normBounds=0,dyadicSteps=0;
for(const c of [...R.commuting_native_label_controls,...R.noncommuting_native_label_controls]){
  const records=c.records,q=records[0].modulus,n=records[0].first.length,p=c.supplied_model,v=c.verification,s=c.sampling,K=field(q),M=matrices(K);
  if(c.source_seed){const original=source.native_controls.find(x=>x.seed===c.source_seed);same(records,original.native_records,"same native records, not substituted easy inputs");}
  check(p.access_model==="supplied_classical_matrices_and_state"&&p.calibration_operators_encode_known_support===true&&p.matrices_were_constructed_from_native_noisy_records===false&&p.has_native_quantum_access_to_these_generators===false,"known-support calibration is not native access");
  const order=p.measurement_order;check(order.length===n&&new Set(order).size===n&&order.every(i=>Number.isInteger(i)&&i>=0&&i<n),"complete measurement order");same(order,p.represented_product_order,"same ordered-word premises");same(order,v.measurement_order,"certificate order");
  const dim=p.metric.length;check(dim<=6,"independent exact control dimension cap");
  const G=M.decode(p.metric,dim,dim),psi=M.decode(p.state,dim,1),I=M.identity(dim),U=p.operators.map(A=>M.decode(A,dim,dim));
  check(U.length===n&&M.eq(G,M.star(G)),"one generator per secret coordinate / Hermitian metric");
  check(v.positive_metric_certificate.positive_definite_required===true,"strict metric certificate required");M.LDL(G,v.positive_metric_certificate);
  check(K.eq(M.norm(psi,G),K.unit),"exact normalized state");U.forEach(A=>check(M.eq(M.times(M.times(M.star(A),G),A),G)&&M.eq(M.power(A,q),I),"metric unitarity and full-root finite order"));
  const delta=p.commutator_operator_norm_uppers.map(row=>row.map(parse));
  check(delta.length===n&&delta.every(row=>row.length===n),"whole pairwise norm vocabulary");
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)check(cmp(delta[i][j],delta[j][i])===0n&&delta[i][j][0]>=0n&&(i!==j||delta[i][j][0]===0n),"nonnegative symmetric commutator bounds");
  check(v.commutator_norm_certificates.length===n*(n-1)/2,"all norm certificates retained");
  let pair=0,exactlyCommuting=true;
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
    const cert=v.commutator_norm_certificates[pair++];same(cert.generators,[i,j],"ordered complete pair certificate");check(cert.operator_norm_upper===str(delta[i][j]),"pair bound encoding");
    const C=M.plus(M.times(U[i],U[j]),M.scale(M.times(U[j],U[i]),K.scale(K.unit,rat(-1n))));
    exactlyCommuting=exactlyCommuting&&M.eq(C,M.zeroM(dim,dim));
    const A=M.plus(M.scale(G,K.scale(K.unit,mul(delta[i][j],delta[i][j]))),M.scale(M.times(M.times(M.star(C),G),C),K.scale(K.unit,rat(-1n))));
    M.LDL(A,cert.PSD_bound_certificate);normBounds++;
  }
  const projectors=U.map(A=>{
    const powers=[I];for(let k=1;k<q;k++)powers.push(M.times(powers[k-1],A));
    const family=[];let total=M.zeroM(dim,dim);
    for(let t=0;t<q;t++){
      let P=M.zeroM(dim,dim);powers.forEach((B,k)=>P=M.plus(P,M.scale(B,K.scale(K.powers[mod(-t*k,q)],rat(1n,BigInt(q))))));total=M.plus(total,P);
      if(!M.eq(P,M.zeroM(dim,dim))){check(M.eq(M.times(P,P),P)&&M.eq(M.times(M.star(P),G),M.times(G,P))&&M.eq(M.times(A,P),M.scale(P,K.powers[t])),"exact projector/eigenvalue");family.push([t,P]);}
    }
    check(M.eq(total,I),"complete spectral partition");return family;
  });
  const gcd=(a,b)=>{while(b)[a,b]=[b,a%b];return a;},steps=projectors.map(family=>family.reduce((s,[t])=>gcd(s,t),q)),periods=steps.map(a=>q/a),possible=periods.reduce((s,a)=>s*BigInt(a),1n);
  same(steps,v.eigenlabel_subgroup_steps,"eigenlabel subgroup steps");same(periods,v.generator_exact_periods,"exact minimal generator periods, not just U^q=I");
  check(v.secret_support_size_upper_from_generator_periods===String(possible)&&v.uniform_secret_coverage_upper_from_generator_periods===str(rat(possible,BigInt(q)**BigInt(n)))&&v.all_generators_primitive_q_order===steps.every(a=>a===1),"low-period generators cannot pretend to cover the full secret space");
  const vocabulary=projectors.reduce((s,family)=>s*BigInt(family.length),1n),support=[possible,vocabulary,exactlyCommuting?BigInt(dim):vocabulary].reduce((a,b)=>a<b?a:b);
  same(v.nonzero_projector_counts,projectors.map(family=>family.length),"actual nonzero spectral vocabularies");
  check(v.all_generators_exactly_commute===exactlyCommuting&&v.secret_support_size_upper_from_supplied_model===String(support)&&v.uniform_secret_coverage_upper_from_supplied_model===str(rat(support,BigInt(q)**BigInt(n))),"joint support bound / commuting model has at most R secret atoms");
  const basis=v.difference_basis,inv=basis.modular_unit_difference_inverse,D=basis.basis_record_indices.map(i=>records[i].first.map((a,j)=>mod(a-records[i].second[j],q)));
  check(D.length===n&&inv.length===n&&inv.every(row=>row.length===n)&&basis.rank_mod3===n,"full native difference basis");
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)check(mod(dot(D[i],inv.map(row=>row[j])),q)===Number(i===j),"exact inverse at retained q");
  const h=rat(BigInt(q*q-1),BigInt(4*q));check(v.pinching_constant_exact===str(h),"balanced-power pinching constant");
  const coefficients=f=>inv[0].map((_,i)=>{const a=mod(dot(f,inv.map(row=>row[i])),q);return 2*a<q?a:a-q;});
  const word=b=>order.reduce((A,i)=>M.times(A,M.power(U[i],mod(b[i],q))),I);
  const disturbance=b=>mul(h,order.reduce((sum,i,a)=>add(sum,order.slice(a+1).reduce((z,j)=>add(z,mul(rat(BigInt(Math.abs(b[j]))),delta[i][j])),zero)),zero));
  check(v.native_moment_certificates.length===3*records.length&&p.original_native_moments.length===records.length&&p.representation_error_uppers.length===records.length,"all original moments");
  let totalError=zero,suppliedScore=K.F();const seen=new Map();
  records.forEach((r,j)=>{
    check(r.first.length===n&&r.second.length===n&&r.modulus===q&&r.outcome.length===2,"native record shape");
    const frequencies=[r.first,r.second,r.first.map((x,i)=>mod(x-r.second[i],q))],out=[...r.outcome,mod(r.outcome[0]-r.outcome[1],q)];
    check(p.original_native_moments[j].length===3&&p.representation_error_uppers[j].length===3,"difference observable not dropped");
    frequencies.forEach((f,k)=>{
      const target=K.decode(p.original_native_moments[j][k]),sigma=parse(p.representation_error_uppers[j][k]),b=coefficients(f),expect=M.expect(psi,G,word(b)),cert=v.native_moment_certificates[3*j+k];
      check(sigma[0]>=0n&&sign(K,K.plus(K.unit,K.scale(K.times(target,K.conj(target)),rat(-1n))))>=0,"bounded original moment / nonnegative sigma");
      if(seen.has(key(f)))check(K.eq(seen.get(key(f)),target),"same frequencies have same original moments");seen.set(key(f),target);if(f.every(x=>x===0))check(K.eq(target,K.unit),"zero frequency normalization");
      same(cert.frequency,f,"original frequency retained");same(cert.balanced_basis_coefficients,b,"balanced reconstruction");check(cert.record_index===j&&cert.harmonic_index===k&&K.eq(K.decode(cert.ordered_word_expectation),expect)&&cert.original_representation_error_upper===str(sigma),"original word representation certificate");
      const diff=K.plus(target,K.scale(expect,rat(-1n))),upper=K.plus(K.scale(K.unit,mul(sigma,sigma)),K.scale(K.times(diff,K.conj(diff)),rat(-1n)));
      check(["POSITIVE","ZERO"].includes(signCertificate(K,upper,cert.representation_bound_certificate)),"exact original sigma bound");
      const dist=disturbance(b),err=add(sigma,dist),clipped=cmp(err,rat(2n))>0?rat(2n):err;
      check(cert.sequential_disturbance_upper===str(dist)&&cert.total_original_moment_error_upper===str(clipped),"coefficient-sensitive polynomial moment bound");totalError=add(totalError,clipped);
      const phase=K.times(K.powers[mod(-out[k],q)],target);suppliedScore=K.plus(suppliedScore,K.scale(K.plus(phase,K.conj(phase)),rat(1n,2n)));
    });
  });
  check(v.native_score_expectation_loss_upper===str(totalError)&&s.score_expectation_loss_upper===str(totalError),"complete native score loss");
  const cache=new Map();
  function branches(values,vector,step){
    const id=key(values);if(cache.has(id))return cache.get(id);
    const candidates=projectors[order[step]].map(([t,P])=>[t,M.times(P,vector)]).filter(([,x])=>!M.eq(x,M.zeroM(dim,1)));
    const norm=M.norm(vector,G),weights=candidates.map(([,x])=>M.norm(x,G));
    check(K.eq(weights.reduce(K.plus,K.F()),norm)&&sign(K,norm)>0,"positive complete conditional CDF");
    const result={candidates,weights,norm};cache.set(id,result);return result;
  }
  const nativeScore=secret=>records.reduce((sum,r)=>{const a=mod(r.outcome[0]-dot(r.first,secret),q),b=mod(r.outcome[1]-dot(r.second,secret),q);return[a,b,mod(a-b,q)].reduce((z,e)=>K.plus(z,K.scale(K.plus(K.powers[e],K.powers[mod(-e,q)]),rat(1n,2n))),sum);},K.F());
  let best=null,bestScore=null;
  for(const trajectory of s.dyadic_prefix_trajectories){
    check(trajectory.length===n,"no partially completed trajectory accepted");let vector=psi;const values=Array(n).fill(null),prefix=[];
    trajectory.forEach(([bits,raw,t],step)=>{
      check(Number.isInteger(bits)&&bits>=8&&bits<=128&&bits%8===0&&typeof raw==="string"&&Number.isInteger(t)&&t>=0&&t<q,"bounded exact random prefix encoding");
      const a=BigInt(raw),den=1n<<BigInt(bits);check(a>=0n&&a<den&&String(a)===raw,"dyadic prefix range");
      const {candidates,weights,norm}=branches(prefix,vector,step),lower=K.scale(norm,rat(a,den)),upper=K.scale(norm,rat(a+1n,den));let cumulative=K.F(),selected=null;
      candidates.forEach(([label,x],j)=>{const previous=cumulative;cumulative=K.plus(cumulative,weights[j]);if(label===t){check(sign(K,K.plus(lower,K.scale(previous,rat(-1n))))>=0&&sign(K,K.plus(cumulative,K.scale(upper,rat(-1n))))>=0,"entire dyadic bin is inside the selected exact CDF interval");selected=x;}});
      check(selected!==null,"trajectory outcome has nonzero projector weight");vector=selected;values[order[step]]=t;prefix.push(t);dyadicSteps++;
    });
    const secret=inv.map(row=>mod(dot(row,values),q)),score=nativeScore(secret);
    if(best===null||sign(K,K.plus(score,K.scale(bestScore,rat(-1n))))>0){best=secret;bestScore=score;}trajectories++;
  }
  const ledger=s.ledger,epsilon=parse(ledger.score_sampling_slack),k=ledger.confidence_bits,draws=mul(rat(BigInt(k)),div(add(rat(BigInt(6*records.length)),epsilon),epsilon));
  const required=(draws[0]+draws[1]-1n)/draws[1];check(epsilon[0]>0n&&Number.isInteger(k)&&k>0&&BigInt(s.completed_draws)===required&&s.dyadic_prefix_trajectories.length===s.completed_draws&&ledger.required_fixed_independent_draws===s.completed_draws,"fixed independent-draw budget");
  check(ledger.bound_controls_bad_and_returned_event_not_abort_conditioned_probability===true&&ledger.requires_independent_uniform_random_bits_and_supplied_model_premises===true&&ledger.unknown_sign_or_random_prefix_abort_never_silently_resampled===true,"abort/randomness scope");
  same(best,s.selected_secret,"maximum of every returned trajectory");check(K.eq(bestScore,K.decode(s.selected_score))&&K.eq(suppliedScore,K.decode(s.original_supplied_moment_score)),"exact selected and original scores");
  const threshold=K.plus(suppliedScore,K.scale(K.unit,rat(-add(totalError,epsilon)[0],add(totalError,epsilon)[1])));check(K.eq(threshold,K.decode(s.score_threshold)),"score threshold");
  check(["POSITIVE","ZERO"].includes(signCertificate(K,K.plus(bestScore,K.scale(threshold,rat(-1n))),s.score_margin_certificate))&&s.conditional_rounding_score_certified===true,"posthoc score fact");
  for(const flag of["probabilistic_failure_claim_applies_to_this_seeded_run","unknown_trajectories_silently_discarded","full_secret_grid_enumerated","held_out_native_prediction_verified","native_noisy_recovery_proved","quantum_speedup_proved"])check(s[flag]===false,"unsupported sampling claim: "+flag);
  check(s.randomness_kind==="seeded_calibration"&&v.supplied_model_certified===true&&v.dense_projector_entries_upper===n*q*dim*dim&&v.projector_terms_charged===n*q*q&&v.cyclotomic_field_degree_charged===K.d&&v.input_compact_JSON_bytes===JSON.stringify(p).length,"explicit model access and arithmetic costs");
  for(const flag of["full_secret_grid_enumerated","all_internal_intermediate_bit_costs_certified","classical_model_construction_from_native_input_supplied","native_noisy_recovery_proved","quantum_speedup_proved"])check(v[flag]===false,"unsupported model claim: "+flag);
  if(c.reference){
    const ref=c.reference,expected=q**n;check(expected<=4096&&ref.probabilities.length===expected&&ref.all_balanced_word_probes.length===expected,"complete bounded reference, not subset");
    const probabilities=[];
    for(let index=0;index<expected;index++){
      let raw=index;const values=Array(n).fill(0);for(let i=n-1;i>=0;i--){values[i]=raw%q;raw=Math.floor(raw/q);}let vector=psi;
      order.forEach(i=>{const found=projectors[i].find(([t])=>t===values[i]);vector=found?M.times(found[1],vector):M.zeroM(dim,1);});
      const prob=M.norm(vector,G),item=ref.probabilities[index];same(values,item.root_eigenvalue_tuple,"complete ordered outcome enumeration");check(K.eq(prob,K.decode(item.probability))&&sign(K,prob)>=0,"exact sequential reference probability");probabilities.push([values,prob]);
    }
    check(K.eq(probabilities.reduce((z,[,p])=>K.plus(z,p),K.F()),K.unit),"full reference normalization");
    for(let index=0;index<expected;index++){
      let raw=index;const b=Array(n).fill(0);for(let i=n-1;i>=0;i--){const a=raw%q;b[i]=2*a<q?a:a-q;raw=Math.floor(raw/q);}
      const mean=probabilities.reduce((z,[values,p])=>K.plus(z,K.times(p,K.powers[mod(dot(b,values),q)])),K.F());let X=I;
      order.slice().reverse().forEach(i=>{const Y=M.zeroM(dim,dim);X=projectors[i].reduce((z,[t,P])=>M.plus(z,M.scale(M.times(M.times(P,X),P),K.powers[mod(b[i]*t,q)])),Y);});
      const before=M.expect(psi,G,word(b)),dist=disturbance(b),probe=ref.all_balanced_word_probes[index],diff=K.plus(mean,K.scale(before,rat(-1n)));
      check(K.eq(mean,M.expect(psi,G,X)),"independent exact Heisenberg order law");same(b,probe.balanced_word,"entire balanced word vocabulary");check(K.eq(mean,K.decode(probe.sequential_moment))&&K.eq(before,K.decode(probe.ordered_operator_moment))&&probe.disturbance_upper===str(dist),"reference moment values and polynomial coefficient");
      check(["POSITIVE","ZERO"].includes(signCertificate(K,K.plus(K.scale(K.unit,mul(dist,dist)),K.scale(K.times(diff,K.conj(diff)),rat(-1n))),probe.disturbance_certificate)),"exact disturbance inequality");words++;
    }
  }
}
for(const L of R.polynomial_precision_ledgers){const n=L.generators,q=BigInt(L.modulus),h=rat(q*q-1n,4n*q),worst=mul(h,rat((q-1n)*BigInt(n*(n-1)),4n));check(L.pinching_constant_exact===str(h)&&L.worst_balanced_word_uniform_commutator_coefficient===str(worst)&&L.sufficient_uniform_commutator_bound_at_zero_representation_error===str(div(rat(1n,30n),worst))&&L.native_source_satisfies_premises===false,"conditional polynomial precision ledger");}
for(const flag of["classical_model_construction_from_native_input_supplied","native_noisy_decoder_supplied","quantum_speedup_proved","candidate_record_accepted","novelty_claim"])check(R[flag]===false,"unsupported research claim: "+flag);
console.log(JSON.stringify({status:"PASS",sample_trajectories_checked:trajectories,dyadic_CDF_steps_checked:dyadicSteps,all_balanced_word_probes:words,operator_norm_bounds_checked:normBounds,native_decoder_supplied:false}));
