"use strict";
// Independent ideal quotients and exact original-root phases, not Python output.
const fs=require("fs"),path=require("path");
const {check,same,rat,zero,one,add,sub,mul,div,str,parse,cmp,mod,field}=require("./cyclotomic_exact.js");
const root=path.resolve(__dirname,"../.."),file=process.argv[2]||path.join(root,"research/reductions/native_normal_character_channel.json");
const R=JSON.parse(fs.readFileSync(file,"utf8"));
const words=n=>n?words(n-1).flatMap(v=>[0,1,2].map(a=>v.concat(a))):[[]];
const near=(a,b,msg)=>check(Number.isFinite(a)&&Math.abs(a-b)<4e-10,msg);
function reduce(v,r) {
  const t=Math.floor(r/2),h0=3**Math.ceil(r/2),h1=3**t,cross=r%2?2*h1:0;
  const carry=Math.floor(v[1]/h1);return [mod(v[0]-carry*cross,h0),mod(v[1],h1)];
}
const times=(v,w,r)=>reduce([v[0]*w[0]-v[1]*w[1],v[0]*w[1]+v[1]*w[0]-v[1]*w[1]],r);
function beta(r) {
  let a=rat(2n,3n),b=rat(-1n,3n);
  for(let j=1;j<r;j++) [a,b]=[div(sub(mul(rat(-2n),a),b),rat(3n)),div(sub(a,b),rat(3n))];
  return [a,b];
}
const mod1=a=>rat((a[0]%a[1]+a[1])%a[1],a[1]);
function phase(w,labels,s,r) {
  const b=beta(r),lambda=[[0,0],[1,0],[1,1]];let f=zero;
  w.forEach((j,i)=>labels[i].forEach((a,l)=>{const v=times(a,times(s[l],lambda[j],r),r);f=add(f,add(mul(b[0],rat(BigInt(v[0]))),mul(b[1],rat(BigInt(v[1])))));}));
  return mod1(f);
}
function character(w,labels,r,c) {
  const roots=[[1,0],[0,1],[-1,-1]],v=labels[0].map(()=>[0,0]);
  w.forEach((j,i)=>labels[i].forEach((a,l)=>{const b=times(a,roots[j],r);v[l]=reduce([v[l][0]+b[0],v[l][1]+b[1]],r);}));
  return v.map(a=>reduce(a,r-c));
}
function evaluate(K,z) {return z.reduce((s,a,j)=>s+Number(a[0])/Number(a[1])*Math.cos(2*Math.PI*j/K.q),0);}
function norm(K,z) {return K.times(K.conj(z),z);}
function channel(C) {
  const r=C.level,c=C.normal_ideal_power,m=C.original_qutrit_copies,n=C.secret_dimension;
  check(Number.isInteger(r)&&r>=2&&r<=8&&Number.isInteger(c)&&c>=1&&c<r&&m>0&&m<=6,"bounded actual normal-character control");
  const labels=C.labels;check(labels.length===m&&labels.every(v=>v.length===n),"actual supplied cohort dimension");
  for(const v of labels)for(const a of v){check(a.length===2&&a.every(Number.isInteger),"integer native coefficients");same(a,reduce(a,r),"canonical full-root native labels");}
  const ws=words(m),D=ws.length,K=field(3**Math.ceil(r/2)),groups=new Map(),diff=[],powers=[];
  same(C.complete_original_words,ws,"ALL original words, no sampled favorable branches");
  ws.forEach((w,i)=>{
    const char=character(w,labels,r,c);same(C.normal_characters[i],char,"actual NORMAL character, not central replacement");
    const key=JSON.stringify(char);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(i);
    const d=mod1(sub(phase(w,labels,C.right_native_secret,r),phase(w,labels,C.left_native_secret,r)));
    same(C.exact_phase_difference_mod1[i],str(d),"exact ORIGINAL-root secret phase difference");
    const e=mul(d,rat(BigInt(K.q)));check(e[1]===1n,"phase root denominator");diff.push(str(d));powers.push(K.powers[Number(e[0])]);
  });
  const claimed=C.complete_character_classes;check(claimed.length===groups.size,"all raw character outcomes retained");
  let probability=zero,trace=0,alias=true;
  const seen=new Set();for(const b of claimed) {
    const key=JSON.stringify(b.character);check(groups.has(key)&&!seen.has(key),"unique true character class");seen.add(key);
    const indices=groups.get(key);same(b.word_indices,indices,"complete measured class support");
    const weight=rat(BigInt(indices.length),BigInt(D));same(b.raw_Born_probability,str(weight),"raw secret-independent Born mass");probability=add(probability,weight);
    const equal=indices.every(i=>diff[i]===diff[indices[0]]);alias=alias&&equal;
    const z=K.scale(indices.reduce((s,i)=>K.plus(s,powers[i]),K.F()),rat(1n,BigInt(indices.length)));
    const squared=norm(K,z);if(equal)check(K.eq(squared,K.unit),"exact sector alias");
    trace+=Number(weight[0])/Number(weight[1])*Math.sqrt(Math.max(0,1-evaluate(K,squared)));
  }
  same(str(probability),"1","complete channel including ALL outcomes");
  same(C.exact_phase_difference_constant_within_each_class,alias,"exact pinching alias predicate");
  if(alias)near(C.complete_measured_normal_channel_trace_distance,0,"complete identical pinched density matrices");
  else near(C.complete_measured_normal_channel_trace_distance,trace,"independent pure-block trace-distance formula");
  const total=K.scale(powers.reduce((s,z)=>K.plus(s,z),K.F()),rat(1n,BigInt(D)));
  near(C.original_and_coherently_retained_character_channel_fidelity,evaluate(K,norm(K,total)),"exact coherent retention preserves input fidelity");
  check(C.normal_character_measurement_outcomes_are_secret_independent===true&&C.coherent_computation_is_isometry_not_fiber_erasure===true&&C.original_word_register_erased_by_coherent_computation===false&&C.unknown_inverse_or_cloning_used===false&&C.full_character_dictionary_is_scalable_compiler===false,"channel and access scope");
}
function ledger(L) {
  const r=L.native_level,n=L.secret_dimension,c=L.normal_ideal_power,d=Math.ceil(r/2),kept=Math.min(d,Math.ceil((c+1)/2));
  check([r,n,c].every(Number.isInteger)&&r>=2&&n>0&&c>0&&c<r,"ideal precision ledger dimensions");
  same(L.ring_secret_alias_ideal,`pi^${c+1} A`,"normal-character channel alias ideal");
  same(L.maximum_integer_secret_trits_retained_per_coordinate,kept,"ACTUAL integer-secret precision, not full-ring count");
  same(L.integer_secret_alias_class,{base:3,exponent:n*(d-kept)},"exact symbolic fibre count");
  same(L.uniform_full_secret_success_upper_after_ONLY_this_measurement_channel,{numerator:1,denominator_base:3,denominator_exponent:n*(d-kept)},"uniform prior success bound");
  check(L.normal_subgroup_is_central===(c===r-1)&&L.all_branches_including_recorded_character_outcome_included===true&&L.bound_applies_to_coherently_retained_character_register===false&&L.bound_applies_to_arbitrary_quantum_receivers===false&&L.additional_untouched_original_inputs_covered===false,"noncentral versus central and coherent escape scope");
}
same(R.status,"NATIVE_NORMAL_CHARACTER_PINCHING_ALIAS_AND_COHERENT_RETENTION_REVIEW_PENDING","local channel status");
check(R.normal_measurement_is_not_central_descent===true,"normal/central distinction");
for(const key of ["multi_output_or_coherent_receiver_ruled_out","coherent_fiber_erasure_compiled","native_full_depth_receiver_supplied","novelty_claimed","Shor_level_result_claimed"])check(R[key]===false,"scope inflation: "+key);
R.complete_channels.forEach(channel);R.growing_precision_ledgers.forEach(ledger);
for(const C of R.complete_public_conjugate_eraser_controls) {
  const h=C.level-C.normal_ideal_power,B=3**(h*C.secret_dimension);
  check(B<=81&&C.complete_Fourier_outcome_count===B&&Number.isInteger(C.reference_dimension)&&C.reference_dimension>0,"complete computed-pointer eraser dimensions");
  same(C.exact_raw_probability_of_every_outcome,str(rat(1n,BigInt(B))),"uniform raw conjugate-basis outcome law");
  // The diagonal byproduct and its PUBLIC inverse multiply to I on every
  // word, hence also on an arbitrary reference-entangled input.
  const F=field(3**Math.ceil(h/2));
  F.powers.forEach(z=>check(F.eq(F.times(z,F.conj(z)),F.unit),"whole known Fourier-byproduct feedforward identity"));
  near(C.maximum_raw_probability_error,0,"all conjugate-basis raw probabilities");near(C.maximum_feedforward_corrected_joint_vector_error,0,"entanglement-preserving known correction");
  check(C.restores_input_including_reference_entanglement===true&&C.erases_original_word_register===false&&C.decodes_secret===false&&C.undoes_already_classically_measured_normal_character===false&&C.unknown_state_inverse_or_preparation_used===false,"positive eraser restores input, NOT a decoder or irreversible-measurement reversal");
}
console.log(JSON.stringify({status:"PASS",complete_channels:R.complete_channels.length,exact_original_word_phases:R.complete_channels.reduce((s,c)=>s+c.complete_original_words.length,0),
  exact_alias_channels:R.complete_channels.filter(c=>c.exact_phase_difference_constant_within_each_class).length,public_conjugate_eraser_controls:R.complete_public_conjugate_eraser_controls.length,coherent_escape_preserved:true,arbitrary_receiver_lower_bound_claimed:false}));
