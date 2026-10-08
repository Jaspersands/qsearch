"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const C = require("./cyclotomic_exact.js");
const {check, same, rat: F, add, sub, mul, div, str, parse, cmp, field, sign} = C;
const B = x => { check(typeof x === "string" || Number.isSafeInteger(x), "exact serialized integer"); return BigInt(x); };
const zero = F(0n), one = F(1n), integer = x => F(BigInt(x));
const max = (a,b) => cmp(a,b) >= 0n ? a : b, min = (a,b) => cmp(a,b) <= 0n ? a : b;
const bitLength=x=>x===0n?0:x.toString(2).length;
const mod = (a,q) => (a%q+q)%q, floor = a => a[0]/a[1]-(a[0] < 0n && a[0]%a[1] ? 1n : 0n);
function power(a,n) { let b = one; for (let j=0;j<n;j++) b=mul(b,a); return b; }
function root(q) { let r=q,k=0; check(q>=3n,"positive full root"); while(r%3n===0n){r/=3n;k++;} check(r===1n,"ternary full root");return k; }
const piCache = new Map();
function piBox(bits) {
  if(piCache.has(bits)) return piCache.get(bits);
  const tolerance = F(1n,2n**BigInt(bits+10));
  function atan(d) {
    let total=zero,p=BigInt(d),k=0;
    for(;;) {
      total=add(total,F(k%2?-1n:1n,BigInt(2*k+1)*p)); k++; p*=BigInt(d*d);
      const next=F(k%2?-1n:1n,BigInt(2*k+1)*p), abs=F(next[0]<0n?-next[0]:next[0],next[1]);
      if(cmp(abs,tolerance)<=0n) return [min(total,add(total,next)),max(total,add(total,next))];
    }
  }
  const a=atan(5),b=atan(239), bounds=[sub(mul(integer(16),a[0]),mul(integer(4),b[1])),sub(mul(integer(16),a[1]),mul(integer(4),b[0]))];
  check(cmp(bounds[0],integer(3))>0n&&cmp(bounds[1],integer(4))<0n&&cmp(sub(bounds[1],bounds[0]),mul(integer(20),tolerance))<=0n,"proved rational Machin interval");
  piCache.set(bits,bounds); return bounds;
}
function cosine(q,k,bits) {
  k=mod(k,q);
  if(k===0n)return [one,one];
  if(k===q/3n||k===2n*q/3n)return [F(-1n,2n),F(-1n,2n)];
  if(k>q-k)k=q-k;
  const [lo,hi]=piBox(bits), x=mul(F(k,q),add(lo,hi)), x2=mul(x,x), angleError=mul(F(k,q),sub(hi,lo)), tolerance=F(1n,2n**BigInt(bits+8));
  let term=one,total=one,remainder=integer(8),j=0;
  while(cmp(remainder,tolerance)>0n) {
    j++; term=div(mul(F(-1n),mul(term,x2)),integer((2*j-1)*(2*j))); total=add(total,term);
    remainder=mul(remainder,F(16n,BigInt((2*j+1)*(2*j+2))));
  }
  const error=add(remainder,angleError), result=[max(F(-1n),sub(total,error)),min(one,add(total,error))];
  check(cmp(result[0],result[1])<=0n&&cmp(sub(result[1],result[0]),F(1n,2n**BigInt(bits)))<=0n,"entire exact cosine interval");return result;
}
function acceptance(q,pair,bits) {
  const boxes=[pair[0],pair[1],pair[0]-pair[1]].map(k=>cosine(q,k,bits));
  const sum=side=>boxes.reduce((s,b)=>add(s,b[side]),zero);
  return [max(zero,div(add(integer(3),mul(integer(2),sum(0))),integer(9))),min(one,div(add(integer(3),mul(integer(2),sum(1))),integer(9)))];
}
const failure = (bits,L) => min(one,add(power(F(2n,3n),L),F(BigInt(3*L),2n**BigInt(bits))));
let verifiedCoins=0,verifiedProposals=0;
function verifySampler(q,run,config) {
  const {max_bits:Bcap,max_proposals:L,block_bits:block}=config;
  check(Number.isInteger(Bcap)&&Bcap>0&&Number.isInteger(L)&&L>0&&Number.isInteger(block)&&block>0,"positive explicit sampling caps");
  check(run.trace.length>=1&&run.trace.length<=L&&!run.successful_channel_conditioned_on_no_abort_is_exact&&run.failure_probability_upper===str(failure(Bcap,L)),"aborts charged, not conditional exactness");
  let coins=0,lastDecision;
  run.trace.forEach((proposal,index)=>{
    const pair=proposal.proposal.map(B);check(pair.length===2&&pair.every(x=>x>=0n&&x<q),"whole-root uniform proposal domain");
    let oldBits=0,oldPrefix=0n;
    check(proposal.decisions.length>=1,"nonempty full coin trace");
    proposal.decisions.forEach((step,j)=>{
      check(step.bits===Math.min(Bcap,oldBits+block),"public refinement schedule and cap");
      const prefix=B(step.coin_prefix), width=step.bits-oldBits;
      check(prefix>=0n&&prefix<2n**BigInt(step.bits)&&(prefix>>BigInt(width))===oldPrefix,"consistent nested canonical coin prefixes");
      const [lo,hi]=acceptance(q,pair,step.bits), coinLo=F(prefix,2n**BigInt(step.bits)),coinHi=F(prefix+1n,2n**BigInt(step.bits));
      check(step.acceptance_lower===str(lo)&&step.acceptance_upper===str(hi),"independent complete rational trig enclosure");
      const decision=cmp(coinHi,lo)<=0n?"ACCEPT":cmp(coinLo,hi)>=0n?"REJECT":"REFINE";
      check(step.decision===decision,"exact interval coin decision, no midpoint");
      if(j<proposal.decisions.length-1)check(decision==="REFINE","only unresolved coins refined");
      oldBits=step.bits;oldPrefix=prefix;coins+=width;verifiedCoins++;
    });
    lastDecision=proposal.decisions.at(-1).decision;
    if(index<run.trace.length-1)check(lastDecision==="REJECT","no dropped accept or abort before next proposal");
    verifiedProposals++;
  });
  check(run.coin_bits_read===coins,"exact read coin-bit ledger");
  if(run.noise!==null) {
    check(run.status==="CERTIFIED_DECISIONS_WITH_EXPLICIT_ABORT_BUDGET"&&lastDecision==="ACCEPT","complete sample from accepted last proposal");
    same(run.noise.map(x=>String(B(x))),run.trace.at(-1).proposal.map(x=>String(B(x))),"actual accepted public noise");
  } else if(lastDecision==="REFINE")check(run.status==="UNKNOWN_COIN_PRECISION_CAP"&&run.trace.at(-1).decisions.at(-1).bits===Bcap,"precision cap stays unknown");
  else check(run.status==="UNKNOWN_PROPOSAL_CAP"&&lastDecision==="REJECT"&&run.trace.length===L,"proposal cap stays unknown");
}
function bound(q,M,V,bits=64,L=128) {
  const pair=min(one,div(mul(integer(80),V),F(3n*q*q))),abort=failure(bits,L);
  return {pair,abort,total:min(one,mul(integer(M),add(pair,abort)))};
}
function verifyBound(b,q,M,V,bits=64,L=128) {
  const expected=bound(q,M,V,bits,L);
  check(b.source_integer_second_moment_upper===str(V)&&b.per_record_ideal_noise_TV_upper===str(expected.pair)&&b.per_record_sampler_abort_probability_upper===str(expected.abort)&&b.complete_transcript_success_loss_upper===str(expected.total)&&b.bound_is_nonvacuous===(cmp(expected.total,one)<0n),"exact source/noise/abort TV ledger");
  check(b.input_classical_samples_required===2*M&&b.output_paired_records===M&&b.native_unknown_quantum_states_prepared===0&&!b.input_assumptions_inferred_from_observed_values&&!b.unconditional_hardness_or_speedup&&!b.conditioning_on_sampler_success_erases_loss,"input promises and costs, no quantum source or hardness by schema");
  same(b.assumptions,["same unknown secret","IID uniform full-root labels","independent symmetric source errors","public true second-moment bound","independent ideal random bits","fixed decoder and charged sample count"],"all transfer assumptions explicit");return expected;
}
function verifyRounding(c) {
  const q=B(c.modulus),lo=parse(c.lower),hi=parse(c.upper);root(q);
  const a=floor(add(mul(F(q),lo),F(1n,2n))),b=floor(add(mul(F(q),hi),F(1n,2n)));
  check(cmp(lo,hi)<=0n&&B(c.first_integer)===a&&B(c.last_integer)===b&&!c.midpoint_guess_on_ambiguous_interval,"exact source interval endpoints and rounding");
  if(a===b)check(c.status==="CERTIFIED_UNIQUE_ROUNDING"&&B(c.value)===mod(a,q),"unique rounding including wrapped/negative representatives");
  else check(c.status==="UNKNOWN_ROUNDING_BOUNDARY"&&c.value===null,"ambiguous source stays unknown");
}
function finiteConvolution(q) {
  const K=field(q), plus=K.plus,scale=K.scale,cos=k=>scale(plus(K.powers[C.mod(k,q)],K.powers[C.mod(-k,q)]),F(1n,2n));
  const nu=(u,v)=>scale(plus(K.unit,scale(plus(plus(cos(u),cos(v)),cos(u-v)),F(2n,3n))),F(1n,BigInt(q*q)));
  const phi=scale(plus(K.unit,cos(1)),F(1n,2n)),phi2=K.times(phi,phi),chi=[[-1,F(1n,4n)],[0,F(1n,2n)],[1,F(1n,4n)]];
  let mass=K.F(),TV=K.F();
  for(let u=0;u<q;u++)for(let v=0;v<q;v++) {
    const original=nu(u,v);mass=plus(mass,original);
    let convolved=K.F();for(const [a,p]of chi)for(const[b,r]of chi)convolved=plus(convolved,scale(nu(C.mod(u-a,q),C.mod(v-b,q)),mul(p,r)));
    const actualFormula=scale(plus(K.unit,scale(plus(K.times(phi,plus(cos(u),cos(v))),K.times(phi2,cos(u-v))),F(2n,3n))),F(1n,BigInt(q*q)));
    check(K.eq(convolved,actualFormula),"every exact finite forward-convolution entry");
    const difference=plus(convolved,scale(original,F(-1n))),s=sign(K,difference);
    TV=plus(TV,scale(difference,F(BigInt(s),2n)));
  }
  check(K.eq(mass,K.unit),"finite native noise normalization");
  const limit=K.scale(K.unit,min(one,F(40n,BigInt(3*q*q))));
  check(sign(K,plus(limit,scale(TV,F(-1n))))>=0,"exact finite TV satisfies public moment bound");
  for(let k=0;k<q;k++)check(sign(K,scale(plus(K.unit,cos(k)),F(1n,2n)))>0,"all source Fourier modes nonzero, inverse unique");
  const inverseZeroNumerator=plus(plus(scale(phi2,F(3n)),scale(phi,F(-2n))),scale(K.unit,F(-1n)));
  check(sign(K,phi)>0&&sign(K,plus(K.unit,scale(phi,F(-1n))))>0&&sign(K,inverseZeroNumerator)<0,"unsmoothed inverse kernel negative at native zero, not a forward-convolution obstruction");
  return q*q;
}
function run(r) {
  check(r.status==="CONDITIONAL_CLASSICAL_NOISE_DEGRADATION_REVIEW_PENDING"&&!r.parameter_guards_are_complete_hardness_proof&&!r.native_quantum_input_bridge_or_efficient_receiver&&!r.accepted_speedup_candidate,"conditional source reduction, no speedup");
  check(r.derivation_sha256===crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_NOISE_DEGRADATION.md"))).digest("hex"),"pinned derivation");
  same(r.controls.map(c=>[c.n,c.root_digits,c.count,c.seed]),[2,4,16,80].map(d=>[4,d,16,128000+d]),"precommitted source transform controls");
  let originals=0,outputs=0;
  for(const c of r.controls) {
    const q=3n**BigInt(c.root_digits),d=c.converted,n=c.n,M=c.count;root(q);
    check(!c.calibration_distribution_is_LWE_hardness_source&&!c.underlying_unknown_native_states_simulated_or_prepared,"calibration is not a hardness source or quantum state");
    check(c.source_records.length===2*M&&c.source_errors_diagnostic.length===2*M&&d.records.length===M&&d.sampler_runs.length===M&&d.source_ancestry.length===M&&d.complete_transcript&&d.status==="CONDITIONAL_CLASSICAL_TRANSCRIPT_DEGRADATION","every original included in complete paired transcript");
    check(B(d.modulus)===q&&d.secret_dimension===n&&!d.partial_outputs_can_replace_the_promised_complete_source&&!d.input_labels_chosen_or_mutated&&!d.unknown_secret_input&&d.native_unknown_quantum_states_prepared===0&&!d.hardness_transfer_admitted&&!d.accepted_speedup_candidate,"full-root access and admission scope");
    same(d.sampler_config,{max_bits:64,max_proposals:128,block_bits:8},"costed public precision/proposal caps");verifyBound(d.conditional_bound,q,M,F(1n,2n));
    const mask=d.reduction_side_secret_mask.map(B),s=c.calibration_secret.map(B);
    check(mask.length===n&&s.length===n&&[...mask,...s].every(x=>x>=0n&&x<q),"full-root reduction-side mask and posthoc calibration secret");
    const seen=new Set();
    c.source_records.forEach((record,i)=>{
      check(!seen.has(record.source_id)&&record.source_id===`noise-degradation-${c.seed}-source-${i}`,"distinct original ancestry");seen.add(record.source_id);
      const a=record.label.map(B),e=B(c.source_errors_diagnostic[i]);check(B(record.modulus)===q&&a.length===n&&a.every(x=>x>=0n&&x<q)&&[-1n,0n,1n].includes(e),"public calibration error law and labels");
      const value=mod(a.reduce((v,x,j)=>v+x*s[j],0n)+e,q);check(B(record.value)===value,"posthoc source value check only");
    });
    for(let j=0;j<M;j++) {
      const record=d.records[j],input=[c.source_records[2*j],c.source_records[2*j+1]],noise=d.sampler_runs[j];verifySampler(q,noise,d.sampler_config);
      same(record.first.map(x=>String(B(x))),input[0].label.map(x=>String(B(x))),"first label unchanged");same(record.second.map(x=>String(B(x))),input[1].label.map(x=>String(B(x))),"second label unchanged");
      same(d.source_ancestry[j],input.map(x=>x.source_id),"exact original pairing without reuse");check(B(record.modulus)===q&&record.outcome.length===2,"complete original-root output");
      input.forEach((x,k)=>{const a=x.label.map(B),value=mod(B(x.value)+a.reduce((v,z,i)=>v+z*mask[i],0n)+B(noise.noise[k]),q);check(B(record.outcome[k])===value,"secret-blind public source transform");});
    }
    originals+=2*M;outputs+=M;
  }
  same(r.rounded_Gaussian_source_profiles.map(p=>[p.dimension,String(B(p.modulus)),p.alpha]),[[64,String(3n**16n),"1/1048576"],[64,String(3n**64n),"1/1048576"],[64,"9","1/1048576"],[64,String(3n**16n),"1/2"]],"matching and failing source parameter regimes");
  for(const p of r.rounded_Gaussian_source_profiles) {
    const q=B(p.modulus),alpha=parse(p.alpha),n=p.dimension,M=512,V=add(div(mul(F(q*q),mul(alpha,alpha)),integer(3)),F(1n,2n));root(q);
    const source=cmp(mul(F(q*q),mul(alpha,alpha)),integer(4*n))>=0n,classical=q*q>=2n**BigInt(n);
    check(p.rounded_integer_error_second_moment_upper===str(V)&&p.alpha_q_at_least_2_sqrt_n===source&&p.q_at_least_2_to_n_over_two===classical&&p.published_quantum_worst_case_source_parameter_guard===source&&p.published_classical_worst_case_source_parameter_guard===(source&&classical),"published theorem guard, not prime-only import");
    check(!p.Gaussian_width_is_standard_deviation&&!p.modulus_is_imported_from_prime_only_theorem&&p.source_precision_adapter_implemented&&!p.hardness_transfer_admitted&&p.source_error_law==="continuous D_alpha on torus, rounded only AFTER scaling by q","continuous source law and admission debt");
    const kappa=64,L=2*(kappa+bitLength(BigInt(2*M-1))),coinBits=kappa+bitLength(BigInt(6*M*L-1)),budget=p.sampler_budget,union=min(one,mul(integer(M),failure(coinBits,L)));
    check(budget.failure_bits===kappa&&budget.max_bits===coinBits&&budget.max_proposals===L&&budget.block_bits===8&&budget.M_record_sampler_abort_union_upper===str(union)&&!budget.fixed_precision_is_asymptotically_sufficient&&cmp(union,F(1n,2n**BigInt(kappa)))<=0n,"precision/proposal budgets scale with M and confidence");
    const bits=q.toString(2).length+M.toString(2).length+kappa+3,width=F(1n,2n**BigInt(bits)),per=min(one,mul(mul(integer(2),width),add(F(q),div(one,alpha)))),rounding=min(one,mul(integer(2*M),per));
    const gate=p.source_rounding_loss;
    check(p.source_rounding_precision_bits===bits&&gate.maximum_normalized_observation_interval_width===str(width)&&gate.per_input_rounding_abort_probability_upper===str(per)&&gate.two_M_input_rounding_abort_union_upper===str(rounding)&&gate.source_interval_contains_true_observation_is_assumed_not_inferred&&gate.input_errors_are_continuous_D_alpha_before_rounding,"both input rounding failures charged at explicit precision");
    if(source)check(cmp(rounding,F(1n,2n**BigInt(kappa)))<=0n,"source rounding confidence follows valid alpha-q guard");
    const b=verifyBound(p.conditional_transcript_bound,q,M,V,coinBits,L);check(p.composed_success_loss_upper===str(min(one,add(b.total,rounding))),"composed source/measurement/sampler success transfer");
  }
  r.rounding_controls.forEach(verifyRounding);
  check(r.sampler_failure_controls.length===2,"explicit abort controls");r.sampler_failure_controls.forEach(c=>verifySampler(B(c.modulus),c.result,c));
  same(r.sampler_failure_controls.map(c=>c.result.status),["UNKNOWN_PROPOSAL_CAP","UNKNOWN_COIN_PRECISION_CAP"],"caps are not successful pseudo-transcripts");
  same(r.finite_convolution_controls.map(c=>c.modulus),[3,9],"bounded exact-convolution controls");
  const entries=r.finite_convolution_controls.reduce((s,c)=>{check(c.chi_zero==="1/2"&&c.chi_plus_minus_one_each==="1/4"&&c.source_second_moment==="1/2","specified calibration law");return s+finiteConvolution(c.modulus);},0);
  return {status:"PASS",classical_input_originals:originals,complete_paired_outputs:outputs,verified_proposals:verifiedProposals,exact_lazy_coin_decisions:verifiedCoins,finite_exact_convolution_entries:entries,source_profiles:r.rounded_Gaussian_source_profiles.length,rounding_controls:r.rounding_controls.length,explicit_abort_controls:2,hardness_transfer_admitted:false,quantum_input_bridge:false};
}
if(require.main===module){const report=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../reductions/ternary_noise_degradation.json"),"utf8"));console.log(JSON.stringify(run(report),null,2));}
module.exports={run,cosine,verifySampler};
