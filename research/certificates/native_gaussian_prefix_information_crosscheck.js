"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,same,rat,parse,str,mul}=require("./cyclotomic_exact.js");
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/classical_baselines/native_gaussian_prefix_information.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
function ledger(L){
  const n=L.dimension,r=L.root_digits,t=L.prefix_digits,m=L.original_values,bits=L.requested_certificate_bits;
  [n,r,t,m,bits].forEach(x=>check(Number.isSafeInteger(x)&&x>0,"positive exact parameters"));check(t<=r,"actual prefix divides root");
  const a=parse(L.continuous_D_alpha_width);check(a[0]>0n,"Gaussian width");
  const ratio=mul(mul(a,a),rat(3n**BigInt(2*(r-t)))),K=3n*ratio[0]/ratio[1],paid=Math.min(bits,Math.max(0,Number(K>BigInt(bits+(8n*BigInt(m)).toString(2).length)?BigInt(bits):K-BigInt((8n*BigInt(m)).toString(2).length))));
  check(L.Gaussian_width_in_prefix_periods_squared===str(ratio)&&BigInt(L.Gaussian_decay_floor)===K,"exact wrapped Gaussian width/decay");
  check(L.conservative_bank_TV_budget_bits===paid&&L.whole_prefix_bank_to_secret_independent_uniform_TV_upper===str(rat(1n,1n<<BigInt(paid))),"conservative probability bound rounds up");
  const transport=x=>(x<0n?-x:x)<=9007199254740991n?Number(x):String(x);
  same(L.uncapped_bank_bound_IF_decay_floor_positive,K?{rational_factor:str(rat(8n*BigInt(m),7n)),base:2,exponent:transport(-K)}:null,"factored exponent, no huge denominator allocation");
  for(const k of["rounded_original_errors_are_IID_continuous_D_alpha_then_round","noise_independent_of_original_labels_required","public_labels_and_noise_independent_of_secret_required_for_recovery_bound","public_labels_can_be_kept_at_the_full_original_modulus","arbitrary_classical_or_quantum_postprocessing_of_prefix_records_covered"])check(L[k]===true,"conditional source/scope "+k);
  for(const k of["source_Gaussian_law_established_by_calibration","original_full_response_values_available_to_this_restricted_algorithm","true_quotient_side_information_or_other_coherent_access_excluded","exact_uniformity_claimed","general_LWE_or_quantum_decoder_lower_bound_proved"])check(L[k]===false,"not a general decoder prohibition "+k);
}
function verify(p){
  check(p.status==="ROUNDED_GAUSSIAN_ORIGINAL_PREFIX_INFORMATION_BOUND_REVIEW_PENDING","review pending");
  check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_gaussian_prefix_information.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_GAUSSIAN_PREFIX_INFORMATION.md")),"current provenance");
  const deps=["native_small_multiple_completion.py","ternary_measured_lattice_decoder.py"];same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"dependency set");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency hash"));
  same(p.original_mod9_profiles.map(x=>[x.dimension,x.root_digits,x.prefix_digits,x.original_values]),[8,32,64,128].map(n=>[n,n,2,2*(n*n+12)]),"declared source profiles");
  p.original_mod9_profiles.forEach(x=>{ledger(x);check(x.continuous_D_alpha_width===str(rat(1n,BigInt(x.dimension)**3n)),"declared actual profile width");});ledger(p.full_original_root_outside_the_cut);
  same(p.correlated_Gaussian_marginal_countercontrol,{prefix_modulus:9,dimension:1,original_labels:[[0],[1]],scalar_observations:["E","E+s"],
    E_can_be_a_single_rounded_Gaussian:true,marginal_Gaussian_laws_suffice_for_bank_bound:false,errors_are_IID:false,original_difference_recovers_secret_prefix_exactly:true,
    event_b2_minus_b1_equals_s_has_shared_error_probability:"1",same_event_has_IID_uniform_null_probability:"1/9",whole_bank_TV_from_IID_null_lower:"8/9",countercontrol_is_a_hard_source_or_speedup_candidate:false},"shared-error countercontrol, not IID original law");
  for(let s=0;s<9;s++){let count=0;for(let a=0;a<9;a++)for(let b=0;b<9;b++)if((b-a+9)%9===s)count++;check(count===9,"exact IID null event count");}
  check(p.full_original_root_outside_the_cut.whole_prefix_bank_to_secret_independent_uniform_TV_upper==="1","full-root access not discarded");
  check(p.accepted_speedup_candidate===false&&p.new_active_negative_result_created===false,"conditional local information bound only");
  return{verified:true,exact_Gaussian_prefix_ledgers:5,general_decoder_lower_bound:false};
}
module.exports={verify,ledger};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));
