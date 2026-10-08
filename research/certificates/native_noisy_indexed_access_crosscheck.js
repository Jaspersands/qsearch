"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const C=require("./cyclotomic_exact.js");
const Capacity=require("./native_recovery_capacity_exact.js");
const {check,same,rat:F,add,sub,mul,div,str,parse,cmp}=C;
const zero=F(0n),one=F(1n),I=x=>F(BigInt(x));
const B=x=>{check(typeof x==="string"||Number.isSafeInteger(x),"exact serialized integer");return BigInt(x);};
const min=(a,b)=>cmp(a,b)<=0n?a:b,max=(a,b)=>cmp(a,b)>=0n?a:b,abs=x=>F(x[0]<0n?-x[0]:x[0],x[1]);
const mod=(a,q)=>(a%q+q)%q,bitlen=x=>x===0n?0:x.toString(2).length,floor=a=>a[0]/a[1]-(a[0]<0n&&a[0]%a[1]?1n:0n);
function root(q){let d=0,r=q;check(q>=3n,"positive root");while(r%3n===0n){r/=3n;d++;}check(r===1n,"full ternary root");return d;}
const canonical=(k,q)=>{k=mod(k,q);return 2n*k<q?k:k-q;};
function isqrt(n){if(n<2n)return n;let x=1n<<BigInt(Math.ceil(bitlen(n)/2));for(;;){const y=(x+n/x)/2n;if(y>=x)return x;x=y;}}
function bounds(b){
  const q=B(b.modulus),M=B(b.fixed_original_bank_size),V=parse(b.source_integer_second_moment_upper),powers=b.canonical_signed_phase_powers.map(B);root(q);
  check(M>=1n&&cmp(V,zero)>=0n&&powers.every(k=>canonical(k,q)===k),"canonical fixed-bank exposure and true moment premise");
  const W=powers.reduce((s,k)=>s+(k<0n?-k:k),0n),T=powers.filter(k=>k!==0n).length,gateBits=T?64+bitlen(BigInt(2*T-1)):64,sqrtBits=W?64+bitlen(4n*W-1n):64,squared=div(mul(F(80n*M),V),F(q*q)),scale=2n**BigInt(sqrtBits),k=isqrt(squared[0]*scale*scale/squared[1]),lo=F(k,scale),hi=cmp(mul(lo,lo),squared)===0n?lo:F(k+1n,scale),noise=min(one,mul(F(W),hi)),gate=min(one,F(BigInt(2*T),2n**BigInt(gateBits))),total=min(one,add(noise,gate));
  check(B(b.independent_classical_originals_required)===2n*M&&B(b.weighted_phase_exposure)===W&&b.nonidentity_phase_call_count===T&&b.local_gate_precision_bits===gateBits&&b.sqrt_interval_bits===sqrtBits,"copies, inverse/power exposure and scalable precision");
  check(b.RMS_operator_error_squared_upper===str(squared)&&b.sqrt_of_RMS_upper_bound_lower_enclosure===str(lo)&&b.sqrt_of_RMS_upper_bound_upper_enclosure===str(hi)&&b.expected_complete_receiver_noise_success_loss_upper===str(noise)&&b.complete_gate_error_upper===str(gate)&&b.complete_pre_rounding_success_loss_upper===str(total)&&b.bound_is_nonvacuous===(cmp(total,one)<0n),"exact operator-norm hybrid budget with fixed shared errors");
  check(b.source_errors_are_fixed_across_reused_calls&&!b.noise_resampled_on_every_call&&!b.ideal_unknown_inverse_supplied_exactly&&b.approximate_ideal_phase_and_inverse_access_conditionally_supported&&!b.chosen_label_oracle_supplied&&!b.independent_quantum_originals_created_by_reuse&&!b.fast_forwarded_power_costs_only_one_unit_of_noise_exposure&&!b.source_law_or_moment_inferred_from_values&&!b.hardware_synthesis_implemented&&!b.efficient_receiver_supplied&&!b.hardness_transfer_admitted,"conditional indexed access, no free powers or new labels");
  same(b.assumptions,["same integer-vector secret","fixed original IID source bank","true public second-moment bound","committed maximum phase exposure","receiver accesses only fixed-bank labels","charged known local gates and caller operation errors"],"all coherent query premises explicit");
}
const piCache=new Map();
function piBox(bits){
  if(piCache.has(bits))return piCache.get(bits);
  function atan(d){const tolerance=F(1n,2n**BigInt(bits+10));let total=zero,p=BigInt(d),j=0;for(;;){total=add(total,F(j%2?-1n:1n,BigInt(2*j+1)*p));j++;p*=BigInt(d*d);const next=F(j%2?-1n:1n,BigInt(2*j+1)*p),end=add(total,next);if(cmp(abs(next),tolerance)<=0n)return [min(total,end),max(total,end)];}}
  const a=atan(5),b=atan(239),result=[sub(mul(I(16),a[0]),mul(I(4),b[1])),sub(mul(I(16),a[1]),mul(I(4),b[0]))];piCache.set(bits,result);return result;
}
function angle(a,q,value,bits){
  const centered=canonical(value,q),p=piBox(bits),x=mul(F(2n*centered,q),p[0]),y=mul(F(2n*centered,q),p[1]),lo=min(x,y),hi=max(x,y),scale=2n**BigInt(bits+2),chosen=F(floor(add(mul(div(add(lo,hi),I(2)),F(scale)),F(1n,2n))),scale),error=max(abs(sub(chosen,lo)),abs(sub(chosen,hi)));
  check(B(a.phase_numerator)===value&&B(a.centered_numerator)===centered&&a.precision_bits===bits&&a.angle_lower===str(lo)&&a.angle_upper===str(hi)&&a.dyadic_radian_angle===str(chosen)&&a.angle_error_upper===str(error)&&a.diagonal_operator_error_upper===str(error)&&!a.angle_description_is_hardware_synthesis,"known powered phase angle, no secret or hardware compiler");
  check(cmp(error,F(1n,2n**BigInt(bits)))<=0n,"charged branch angle error");
}
function recipe(r,samples,mask){
  const q=B(r.modulus),digits=root(q),k=B(r.canonical_phase_power),M=samples.length/2,seen=new Set();
  samples.forEach(s=>{check(!seen.has(s.source_id)&&B(s.modulus)===q,"all original bank samples distinct and same modulus");seen.add(s.source_id);});
  check(canonical(k,q)===k&&r.local_angle_precision_bits===64&&r.branch_count===M&&r.index_bits===bitlen(BigInt(M-1))&&r.comparison_compute_uncompute_pairs_per_query_upper===M&&r.diagonal_branches_per_query_upper===2*M,"explicit polynomial multiplexor, no free bank access");
  check(r.controlled_operation==="sum_i |i><i| tensor diag(1,omega^(k*b_i),omega^(k*d_i)); invalid indices identity"&&r.access_implementation==="explicit sequential reversible index equality controls; no QRAM assumed"&&r.inverse_by_negating_power&&!r.arbitrary_new_frequency_labels_available&&!r.source_moment_claimed_by_this_recipe&&!r.quantum_hardware_executed,"only known noisy bank phase access");
  check(r.receiver_public_bank.length===M&&r.reduction_side_multiplexor_branches.length===M&&r.original_source_ancestry.length===M,"complete fixed bank and branch program");
  let u=-1n,v=1n;for(let j=0;j<(digits-1)%6;j++)[u,v]=[u+v,-u];
  for(let j=0;j<M;j++){
    const input=[samples[2*j],samples[2*j+1]],p=r.receiver_public_bank[j],b=r.reduction_side_multiplexor_branches[j];
    same(Object.keys(p).sort(),["modulus","level","ring_labels","first_frequency","second_frequency","state_handle","access"].sort(),"receiver bank excludes values and mask");
    same(p.first_frequency,input[0].label,"original first label");same(p.second_frequency,input[1].label,"original second label");same(r.original_source_ancestry[j],input.map(s=>s.source_id),"bank reuse does not add original IDs");
    check(B(p.modulus)===q&&p.level===2*digits&&p.access==="fixed-bank index; phase oracle only"&&p.state_handle===`qutrit-${j}`&&b.state_handle===p.state_handle,"fixed indexed native source metadata");
    p.ring_labels.forEach((a,i)=>{const y=a.map(B);check(mod(u*y[0]+v*y[1],q)===B(input[0].label[i])&&mod((u+v)*y[0]-u*y[1],q)===B(input[1].label[i]),"actual native ring-label map");});
    check(b.scaled_known_phase_values.length===2&&b.angle_recipes.length===2,"both diagonal branches");
    input.forEach((s,i)=>{const value=mod(k*(B(s.value)+s.label.reduce((z,x,h)=>z+B(x)*mask[h],0n)),q);check(B(b.scaled_known_phase_values[i])===value,"powered known original value, not unobserved secret");angle(b.angle_recipes[i],q,value,64);});
  }
  return 2*M;
}
function run(r){
  check(r.status==="CONDITIONAL_FIXED_BANK_COHERENT_ACCESS_REVIEW_PENDING"&&r.quantum_hardware_states_executed===0&&!r.ideal_source_inverse_supplied_exactly&&!r.chosen_label_oracle_supplied&&!r.efficient_receiver_supplied&&!r.hardness_transfer_admitted&&!r.accepted_speedup_candidate&&!r.unseen_label_phase_values_or_secret_reconstruction_supplied,"new approximate interface, not exact unknown oracle or algorithm");
  check(r.derivation_sha256===crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../NATIVE_NOISY_INDEXED_ACCESS.md"))).digest("hex"),"pinned mathematical derivation");
  const schedules=[[9n,[1n,-1n,3n]],[3n**80n,Array.from({length:64},(_,i)=>i%2?-1n:1n)],[3n**80n,[2n**60n]],[9n,[0n,1n,-1n]]];
  check(r.bounds.length===4,"all scalar controls");r.bounds.forEach((b,i)=>{check(B(b.modulus)===schedules[i][0]&&b.fixed_original_bank_size===8&&b.source_integer_second_moment_upper==="1/2","precommitted bank noise controls");same(b.canonical_signed_phase_powers.map(x=>String(B(x))),schedules[i][1].map(String),"all canonical powers retained");bounds(b);});
  const originals=r.originals_for_recipe_replay,mask=r.reduction_side_mask_for_recipe_replay.map(B);check(originals.length===6,"complete literal bank");same(mask.map(String),["2","4"],"literal reduction-side mask");
  originals.forEach((s,i)=>{same(s.label,[i%9,(2*i+1)%9],"committed recipe labels, not a statistical source-law proof");check(s.value===(3*i+2)%9&&s.modulus===9&&s.source_id===`indexed-source-${i}`,"literal original values and IDs");});
  same(r.multiplexor_recipes.map(p=>String(B(p.canonical_phase_power))),["1","-1","3","0"],"forward, inverse, power and identity plans");
  const angles=r.multiplexor_recipes.reduce((s,p)=>s+recipe(p,originals,mask),0);
  const V=add(div(mul(F(3n**128n),mul(F(1n,1048576n),F(1n,1048576n))),I(3)),F(1n,2n));
  check(r.Gaussian_moment_exposure_controls.length===3,"all source-exposure regimes");
  r.Gaussian_moment_exposure_controls.forEach((b,i)=>{check(B(b.modulus)===3n**64n&&b.fixed_original_bank_size===512&&b.source_integer_second_moment_upper===str(V),"same Gaussian moment, different weighted exposure");const expected=i<2?Array.from({length:i===0?128:1024},()=>"1"):[String(2n**20n)];same(b.canonical_signed_phase_powers.map(x=>String(B(x))),expected,"bounded repeated calls versus fast-forwarded large power");bounds(b);check(b.secret_dimension===64&&!b.nonvacuous_noise_bound_is_full_recovery_feasibility,"noise validity does not grant secret recovery");Capacity.query(b.full_recovery_capacity,64,B(b.modulus),512n,B(b.weighted_phase_exposure));});
  return {status:"PASS",bound_controls:7,fixed_bank_recipes:r.multiplexor_recipes.length,known_angles:angles,original_bank_records:originals.length,ideal_source_inverse_supplied_exactly:false,chosen_label_oracle_supplied:false,efficient_receiver_supplied:false};
}
const input=process.argv[2]||path.join(__dirname,"../reductions/native_noisy_indexed_access.json");
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(input,"utf8"))),null,2));
