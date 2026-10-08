"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const C=require("./cyclotomic_exact.js"),V=require("./native_recovery_capacity_exact.js");
const {check,same,rat:F,add,mul,div,parse}=C;
const B=x=>{check(typeof x==="string"||Number.isSafeInteger(x),"exact integer encoding");return BigInt(x);};
function run(r){
  check(r.status==="NATIVE_FULL_RECOVERY_CAPACITY_AND_TRANSFER_AUDIT_REVIEW_PENDING"&&!r.capacity_pass_proves_scalable_receiver&&!r.general_noisy_quantum_lower_bound&&!r.receiver_supplied&&!r.accepted_speedup_candidate,"capacity and certificate gates, not an algorithm or general no-go");
  check(r.derivation_sha256===crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../NATIVE_RECOVERY_CAPACITY.md"))).digest("hex"),"pinned capacity derivation");
  const specs=[[16,512],[64,512],[64,4096],[16,1024]];check(r.copy_controls.length===specs.length,"all copy profiles");
  r.copy_controls.forEach((p,i)=>V.copy(p,64,3n**BigInt(specs[i][0]),BigInt(specs[i][1])));
  same(r.query_controls.map(p=>p.weighted_phase_exposure),[0,128,1024],"all displayed indexed query budgets");r.query_controls.forEach(p=>V.query(p,64,3n**64n,512n,B(p.weighted_phase_exposure)));
  same(r.Gaussian_joint_profiles.map(p=>[p.dimension,String(B(p.modulus)),p.alpha,p.bank_size]),[[64,String(3n**64n),"1/1048576",512],[64,String(3n**64n),"1/1048576",1024],[64,String(3n**64n),"1/16777216",512]],"original, enlarged-bank and changed-noise profiles");
  for(const p of r.Gaussian_joint_profiles){
    const q=B(p.modulus),M=B(p.bank_size),alpha=parse(p.alpha),moment=add(div(mul(F(q*q),mul(alpha,alpha)),F(3n)),F(1n,2n));
    check(p.source_parameter_guard===((alpha[0]*q)**2n>=4n*BigInt(p.dimension)*alpha[1]**2n)&&!p.source_noise_bound_is_receiver_capacity_certificate&&!p.receiver_supplied&&!p.accepted_speedup_candidate,"source guard separate from full-secret receiver capacity");
    V.copy(p.copy_only_capacity,p.dimension,q,M);V.minimum(p.indexed_minimum_exposure,p.dimension,q,M);V.incompatibility(p.generic_noise_incompatibility,p.dimension,q,M,moment);
  }
  const reference=[];for(let K=0;K<5;K++)for(let W=0;W<5;W++)reference.push([K,W]);
  same(r.exact_reference_ball_controls.map(p=>[p.coordinates,p.radius]),reference,"complete small combinatorial controls, not toy algorithms");r.exact_reference_ball_controls.forEach(p=>V.ball(p,B(p.coordinates),B(p.radius)));
  // Also verify that the LIVE source adapters expose, rather than hide, capacity.
  const copySource=JSON.parse(fs.readFileSync(path.join(__dirname,"../reductions/native_noisy_phase_input.json"),"utf8"));
  copySource.source_profiles.forEach(p=>{check(!p.nonvacuous_noise_bound_is_full_recovery_feasibility,"source profile does not promote a small loss");V.copy(p.full_recovery_capacity,p.dimension,B(p.modulus),B(p.native_inputs));});
  const querySource=JSON.parse(fs.readFileSync(path.join(__dirname,"../reductions/native_noisy_indexed_access.json"),"utf8"));
  querySource.Gaussian_moment_exposure_controls.forEach(p=>{check(p.secret_dimension===64&&!p.nonvacuous_noise_bound_is_full_recovery_feasibility,"indexed source knows secret dimension and required capacity");V.query(p.full_recovery_capacity,p.secret_dimension,B(p.modulus),B(p.fixed_original_bank_size),B(p.weighted_phase_exposure));});
  return {status:"PASS",copy_controls:r.copy_controls.length,query_controls:r.query_controls.length,joint_Gaussian_profiles:r.Gaussian_joint_profiles.length,exact_ball_reference_controls:r.exact_reference_ball_controls.length,live_copy_profiles:copySource.source_profiles.length,live_query_profiles:querySource.Gaussian_moment_exposure_controls.length,global_generic_ledger_incompatibilities:r.Gaussian_joint_profiles.filter(p=>p.generic_noise_incompatibility.global_incompatibility_certified).length,receiver_supplied:false,general_noisy_quantum_lower_bound:false};
}
const input=process.argv[2]||path.join(__dirname,"../reductions/native_recovery_capacity.json");
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(input,"utf8"))),null,2));
