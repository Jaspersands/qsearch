"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const C = require("./cyclotomic_exact.js");
const Capacity = require("./native_recovery_capacity_exact.js");
const {check,same,rat:F,add,sub,mul,div,str,parse,cmp,field} = C;
const zero=F(0n),one=F(1n),I=x=>F(BigInt(x));
const B=x=>{check(typeof x==="string"||Number.isSafeInteger(x),"exact serialized integer");return BigInt(x);};
const abs=x=>F(x[0]<0n?-x[0]:x[0],x[1]);
const min=(a,b)=>cmp(a,b)<=0n?a:b,max=(a,b)=>cmp(a,b)>=0n?a:b;
const mod=(a,q)=>(a%q+q)%q,bitlen=x=>x===0n?0:x.toString(2).length;
const floor=a=>a[0]/a[1]-(a[0]<0n&&a[0]%a[1]?1n:0n);
function root(q){let r=q,k=0;check(q>=3n,"positive root");while(r%3n===0n){r/=3n;k++;}check(r===1n,"full ternary root");return k;}
function matrixPower(A,k){let out=[[1n,0n],[0n,1n]];while(k--){out=out.map(row=>A[0].map((_,j)=>row.reduce((s,x,i)=>s+x*A[i][j],0n)));}return out;}
function frequencyMatrix(r){
  const Z=[[0n,-1n],[1n,-1n]],P=[[-1n,-1n],[1n,-2n]],T=[[1n,-1n],[1n,0n]];
  same(matrixPower(P,2).map(row=>row.map(String)),Z.map(row=>row.map(x=>String(-3n*x))),"ramification identity P^2=-3Z");
  same(matrixPower(T,3).map(row=>row.map(String)),[["-1","0"],["0","-1"]],"frequency recurrence cubic identity");
  // Independent powering of the unit recurrence, not a copied six-row table.
  const U=matrixPower(T,(r-1)%6),u=-U[0][0]+U[1][0],v=-U[0][1]+U[1][1];
  check(u*u+u*v+v*v===1n,"unit norm and determinant at every r");
  return [[u,v],[u+v,-u]];
}
const piCache=new Map();
function piBox(bits){
  if(piCache.has(bits))return piCache.get(bits);
  const tolerance=F(1n,2n**BigInt(bits+10));
  function atan(d){let p=BigInt(d),total=zero,k=0;for(;;){
    total=add(total,F(k%2?-1n:1n,BigInt(2*k+1)*p));k++;p*=BigInt(d*d);
    const next=F(k%2?-1n:1n,BigInt(2*k+1)*p),end=add(total,next);
    if(cmp(abs(next),tolerance)<=0n)return [min(total,end),max(total,end)];
  }}
  const a=atan(5),b=atan(239),box=[sub(mul(I(16),a[0]),mul(I(4),b[1])),sub(mul(I(16),a[1]),mul(I(4),b[0]))];
  check(cmp(box[0],I(3))>0n&&cmp(box[1],I(4))<0n&&cmp(sub(box[1],box[0]),mul(I(20),tolerance))<=0n,"Machin interval remainder");
  piCache.set(bits,box);return box;
}
function verifyAngle(a,q,value,bits){
  const k=value*2n<q?value:value-q,p=piBox(bits),x=mul(F(2n*k,q),p[0]),y=mul(F(2n*k,q),p[1]),lo=min(x,y),hi=max(x,y);
  const scale=2n**BigInt(bits+2),mid=div(add(lo,hi),I(2)),angle=F(floor(add(mul(mid,F(scale)),F(1n,2n))),scale);
  const error=max(abs(sub(angle,lo)),abs(sub(angle,hi)));
  check(B(a.phase_numerator)===value&&B(a.centered_numerator)===k&&a.precision_bits===bits,"known phase and exact centered numerator");
  check(a.angle_lower===str(lo)&&a.angle_upper===str(hi)&&a.dyadic_radian_angle===str(angle)&&a.angle_error_upper===str(error)&&a.diagonal_operator_error_upper===str(error),"complete rational angle compiler replay");
  check(cmp(error,F(1n,2n**BigInt(bits)))<=0n&&!a.angle_description_is_hardware_synthesis,"angle error charged, no hardware claim");
}
function verifyBound(b,q,M,V,kappa=64){
  const bits=kappa+bitlen(2n*M-1n),unit=F(1n,2n**BigInt(bits)),per=min(one,div(mul(I(20),V),F(q*q))),gate=min(one,mul(F(2n*M),unit));
  const total=min(one,add(mul(F(M),per),gate)),g=b.gate_budget;
  check(b.source_integer_second_moment_upper===str(V)&&b.per_state_averaged_trace_distance_upper===str(per)&&b.M_state_success_loss_before_source_rounding_upper===str(total)&&b.bound_is_nonvacuous===(cmp(total,one)<0n),"averaged input noise and ALL preparation losses");
  check(g.failure_bits===kappa&&g.local_gate_precision_bits===bits&&g.F3_operator_error_promise_upper===str(unit)&&g.known_diagonal_operator_error_budget_upper===str(unit)&&g.per_state_preparation_trace_error_upper===str(min(one,mul(I(2),unit)))&&g.M_state_preparation_trace_error_upper===str(gate)&&!g.universal_gate_synthesis_implemented,"scalable precision and synthesis debt");
  check(cmp(gate,F(1n,2n**BigInt(kappa)))<=0n&&B(b.input_classical_originals_required)===2n*M&&B(b.independent_native_qutrits_supplied_in_gate_model)===M,"original and confidence budgets");
  check(!b.promises_inferred_from_sample_values&&!b.individual_pure_realization_has_this_noise_bound&&!b.postselection_erases_global_error&&!b.ideal_source_inverse_supplied&&!b.efficient_receiver_supplied&&!b.hardness_transfer_admitted,"no unsupported source access or solver admission");
  same(b.assumptions,["same unknown integer-vector secret","IID uniform full-root labels","independent symmetric source errors","true public second-moment bound","independent original pair per state","copy-only receiver","F3 implementation satisfies charged operator error"],"explicit transfer premises");
  return {total,bits};
}
function integerSqrt(n){check(n>=0n,"positive sqrt argument");if(n<2n)return n;let x=1n<<BigInt(Math.ceil(bitlen(n)/2));for(;;){const y=(x+n/x)/2n;if(y>=x)return x;x=y;}}
function verifyTrace(c){
  const phi=parse(c.phi),bits=c.bits,x=add(one,phi),v=add(mul(x,x),I(8)),scale=2n**BigInt(bits),k=integerSqrt(v[0]*scale*scale/v[1]),lo=F(k,scale),hi=cmp(mul(lo,lo),v)===0n?lo:F(k+1n,scale),delta=sub(one,phi);
  check(cmp(phi,I(-1))>=0n&&cmp(phi,one)<=0n&&bits===64,"symmetric characteristic scope");
  // The two-dimensional characteristic equation and remaining eigenvalue.
  const t=div(sub(phi,one),I(3)),r=div(sub(mul(phi,phi),one),I(3));
  check(cmp(r,zero)<=0n&&cmp(mul(t,t),zero)>=0n,"antisymmetric eigenvalue nonnegative");
  check(cmp(mul(sub(I(6),x),sub(I(6),x)),v)>=0n&&cmp(sub(I(6),x),zero)>=0n,"sqrt(x^2+8)<=6-x on x in[0,2]");
  check(c.trace_distance_lower===str(div(mul(delta,add(x,lo)),I(6)))&&c.trace_distance_upper===str(div(mul(delta,add(x,hi)),I(6)))&&c.one_minus_phi_upper===str(delta),"exact root interval and trace-distance formula");
}
function density(c){
  const q=Number(B(c.modulus)),K=field(q),phases=(e,f)=>[0,e,f],chi=[[-1,F(1n,4n)],[0,F(1n,2n)],[1,F(1n,4n)]],cos=k=>K.scale(K.plus(K.powers[C.mod(k,q)],K.powers[C.mod(-k,q)]),F(1n,2n));
  same(c.error_law,[[ -1,"1/4"],[0,"1/2"],[1,"1/4"]],"exact independent calibration source law");
  const phi=K.scale(K.plus(K.unit,cos(1)),F(1n,2n)),phi2=K.times(phi,phi);
  check(K.eq(K.decode(c.characteristic_phi_exact),phi),"actual source characteristic");
  const actual=Array.from({length:3},()=>Array.from({length:3},K.F));
  for(const[e,p]of chi)for(const[f,w]of chi){const a=phases(e,f);for(let i=0;i<3;i++)for(let j=0;j<3;j++)actual[i][j]=K.plus(actual[i][j],K.scale(K.powers[C.mod(a[i]-a[j],q)],div(mul(p,w),I(3))));}
  for(let i=0;i<3;i++)for(let j=0;j<3;j++){
    const wanted=K.scale(i===j?K.unit:(i===0||j===0?phi:phi2),F(1n,3n));
    check(K.eq(actual[i][j],wanted)&&K.eq(actual[i][j],K.decode(c.averaged_phase_frame_density_exact[i][j])),"exact finite averaged density, including phi^2 branch");
  }
  check(c.moment_trace_distance_upper===str(min(one,F(10n,BigInt(q*q))))&&!c.numeric_diagnostic_is_certificate&&!c.calibration_is_LWE_hardness_source,"moment guard and calibration scope");
  return 9;
}
function run(report){
  check(report.status==="CONDITIONAL_COPY_ONLY_NOISY_PHASE_INPUT_REVIEW_PENDING"&&!report.hardness_transfer_admitted&&!report.accepted_speedup_candidate&&!report.efficient_native_receiver_supplied&&!report.ideal_unknown_source_inverse_supplied&&!report.arbitrary_full_ring_secrets_covered&&!report.odd_levels_covered&&report.polynomial_input_recipe_not_polynomial_decoder&&report.quantum_hardware_states_executed===0,"review-pending copy-only even source, no decoder or hardware execution");
  check(report.derivation_sha256===crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../NATIVE_NOISY_PHASE_INPUT.md"))).digest("hex"),"pinned mathematical derivation");
  check(report.gate_model==="known qutrit F3 and two diagonal phases with charged operator error","honest selected gate model");
  same(report.controls.map(c=>[c.dimension,c.root_digits,c.native_inputs,c.seed]),[1,2,16,80,300].map(r=>[4,r,8,130000+r]),"precommitted scalable original-source controls");
  let originals=0,recipes=0,angles=0;
  for(const c of report.controls){
    const q=3n**BigInt(c.root_digits),n=c.dimension,M=c.native_inputs,b=c.batch,s=c.calibration_secret.map(B),mask=b.reduction_side_mask.map(B),A=frequencyMatrix(c.root_digits),seen=new Set();root(q);
    check(!c.calibration_is_LWE_hardness_source&&b.status==="CONDITIONAL_COPY_ONLY_GATE_RECIPE_NOT_HARDWARE_EXECUTION"&&b.quantum_hardware_states_executed===0&&!b.efficient_receiver_supplied&&!b.ideal_unknown_state_inverse_supplied&&!b.accepted_speedup_candidate,"calibration and hardware/receiver scope");
    check(c.source_records.length===2*M&&c.source_error_diagnostics.length===2*M&&b.receiver_inputs.length===M&&b.reduction_side_recipes.length===M&&b.source_ancestry.length===M,"complete originals and native recipe batches");
    check(s.length===n&&mask.length===n&&[...s,...mask].every(x=>x>=0n&&x<q),"canonical reduction-side mask and posthoc calibration secret");
    const budget=verifyBound(b.bound,q,BigInt(M),F(1n,2n));
    c.source_records.forEach((a,i)=>{
      check(a.source_id===`noisy-phase-${c.seed}-source-${i}`&&!seen.has(a.source_id),"unique original IDs, not IID inference");seen.add(a.source_id);
      const label=a.label.map(B),e=B(c.source_error_diagnostics[i]);check(B(a.modulus)===q&&label.length===n&&label.every(x=>x>=0n&&x<q)&&[-1n,0n,1n].includes(e),"canonical original source labels");
      check(B(a.value)===mod(label.reduce((v,x,j)=>v+x*s[j],0n)+e,q),"posthoc calibration source, not preparation input");
    });
    for(let j=0;j<M;j++){
      const receiver=b.receiver_inputs[j],recipe=b.reduction_side_recipes[j],pair=[c.source_records[2*j],c.source_records[2*j+1]];
      same(Object.keys(receiver).sort(),["modulus","level","ring_labels","first_frequency","second_frequency","state_handle","access"].sort(),"receiver receives NO noisy values, mask or preparation inverse");
      check(B(receiver.modulus)===q&&receiver.level===2*c.root_digits&&receiver.state_handle===`qutrit-${j}`&&recipe.state_handle===receiver.state_handle&&receiver.access==="one supplied qutrit, copy-only","native state handle and access");
      same(receiver.first_frequency,pair[0].label,"original first frequency");same(receiver.second_frequency,pair[1].label,"original second frequency");same(b.source_ancestry[j],pair.map(x=>x.source_id),"disjoint original pairing");
      check(receiver.ring_labels.length===n,"native ring vector length");
      receiver.ring_labels.forEach((label,i)=>{const y=label.map(B),a=B(pair[0].label[i]),d=B(pair[1].label[i]);check(y.length===2&&y.every(x=>x>=0n&&x<q)&&mod(A[0][0]*y[0]+A[0][1]*y[1],q)===a&&mod(A[1][0]*y[0]+A[1][1]*y[1],q)===d,"actual invertible native label compiler at arbitrary q");});
      check(recipe.initialize==="|0>"&&!recipe.secret_or_errors_as_preparation_inputs&&!recipe.hardware_synthesized&&recipe.F3_operator_error_promise_upper===b.bound.gate_budget.F3_operator_error_promise_upper,"known local gate recipe, no secret/hardware claim");
      same(recipe.gate_order,["F3","diag(1,exp(i*angle_b),exp(i*angle_d))"],"actual preparation order");check(recipe.angles.length===2&&recipe.known_phase_values.length===2,"complete diagonal branches");
      pair.forEach((a,k)=>{const value=mod(B(a.value)+a.label.reduce((v,x,i)=>v+B(x)*mask[i],0n),q);check(B(recipe.known_phase_values[k])===value,"only public noisy values and reduction-side mask enter phase preparation");verifyAngle(recipe.angles[k],q,value,budget.bits);angles++;});
      recipes++;
    }
    originals+=2*M;
  }
  same(report.exact_density_controls.map(c=>Number(B(c.modulus))),[3,9,27,81],"precommitted exact density regimes");
  const densityEntries=report.exact_density_controls.reduce((s,c)=>s+density(c),0);
  same(report.rational_trace_controls.map(c=>c.phi),["-1","-1/2","0","1/4","1/2","999/1000","1"],"all trace regimes including endpoints");report.rational_trace_controls.forEach(verifyTrace);
  same(report.source_profiles.map(p=>[p.dimension,String(B(p.modulus)),p.alpha,p.native_inputs]),[[64,String(3n**16n),"1/1048576",512],[64,String(3n**64n),"1/1048576",512],[64,"9","1/1048576",512],[64,String(3n**16n),"1/2",512]],"valid quantum/classical source and vacuous controls");
  for(const p of report.source_profiles){
    const q=B(p.modulus),M=B(p.native_inputs),alpha=parse(p.alpha),V=add(div(mul(F(q*q),mul(alpha,alpha)),I(3)),F(1n,2n)),source=cmp(mul(F(q*q),mul(alpha,alpha)),I(4*p.dimension))>=0n,classical=q*q>=2n**BigInt(p.dimension);root(q);
    check(!p.nonvacuous_noise_bound_is_full_recovery_feasibility,"source approximation is not recovery capacity");Capacity.copy(p.full_recovery_capacity,p.dimension,q,M);
    check(p.source_theorem==="Brakerski et al.2013 Theorem2.16 (search LWE)"&&p.source_url==="https://arxiv.org/html/1306.0281"&&p.source_error_law==="continuous D_alpha on torus, scaled then nearest-integer rounded"&&!p.Gaussian_width_is_standard_deviation,"precise published source and Gaussian convention");
    check(p.published_quantum_worst_case_source_parameter_guard===source&&p.published_classical_worst_case_source_parameter_guard===(source&&classical)&&!p.hardness_transfer_admitted&&!p.general_full_ring_secret_covered,"source theorem guard does not admit composed hardness");
    const b=verifyBound(p.conditional_quantum_input_bound,q,M,V),bits=bitlen(q)+bitlen(M)+64+3,h=F(1n,2n**BigInt(bits)),per=min(one,mul(mul(I(2),h),add(F(q),div(one,alpha)))),rounding=min(one,mul(F(2n*M),per)),g=p.source_rounding_loss;
    check(p.source_rounding_precision_bits===bits&&g.maximum_normalized_observation_interval_width===str(h)&&g.per_input_rounding_abort_probability_upper===str(per)&&g.two_M_input_rounding_abort_union_upper===str(rounding)&&g.source_interval_contains_true_observation_is_assumed_not_inferred&&g.input_errors_are_continuous_D_alpha_before_rounding,"containing-interval oracle promise and both input failures charged");
    if(source)check(cmp(rounding,F(1n,2n**64n))<=0n,"rounding precision scalable confidence");
    check(p.composed_success_loss_upper===str(min(one,add(b.total,rounding))),"state-noise plus gate plus source-rounding success transfer");
    same(p.remaining_debt,["external composition and novelty review","source oracle supplies containing intervals at charged precision","uniform secret mask and independent source law promises","efficient copy-only native receiver with explicit M and success","F3/phase compilation in the selected physical gate model"],"all open reduction obligations retained");
  }
  const c=report.shared_pair_countercontrol,K=field(3),chi=[[-1,F(1n,4n)],[0,F(1n,2n)],[1,F(1n,4n)]];
  const phi=k=>chi.reduce((s,[e,p])=>K.plus(s,K.scale(K.powers[C.mod(k*e,3)],p)),K.F()),p1=phi(1),p2=phi(2),reused=K.scale(p2,F(1n,9n)),independent=K.scale(K.times(p1,p1),F(1n,9n));
  check(c.modulus===3&&!c.same_pair_yields_IID_originals&&K.eq(p1,K.scale(K.unit,parse(c.phi_one)))&&K.eq(p2,K.scale(K.unit,parse(c.phi_two)))&&K.eq(reused,K.scale(K.unit,parse(c.reused_coherence_entry)))&&K.eq(independent,K.scale(K.unit,parse(c.independent_coherence_entry)))&&K.eq(K.plus(reused,K.scale(independent,I(-1))),K.scale(K.unit,parse(c.entry_difference)))&&c.entry_difference==="1/48","exact shared-error two-copy failure, not IID originals");
  return {status:"PASS",classical_originals:originals,native_gate_recipes:recipes,certified_known_angles:angles,exact_density_entries:densityEntries,rational_trace_controls:report.rational_trace_controls.length,Gaussian_source_profiles:report.source_profiles.length,shared_pair_countercontrols:1,hardware_states_executed:0,efficient_receiver_supplied:false,hardness_transfer_admitted:false};
}
const input=process.argv[2]||path.join(__dirname,"../reductions/native_noisy_phase_input.json");
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(input,"utf8"))),null,2));
