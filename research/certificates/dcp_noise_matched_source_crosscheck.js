#!/usr/bin/env node
"use strict";

// Independent regeneration of both finite source levels and the exact channel.
const fs=require("fs"),path=require("path");
function need(v,m){if(!v)throw new Error(m);}
function gcd(a,b){for(;b;){const c=a%b;a=b;b=c;}return a<0n?-a:a;}
function Q(p,q=1n){const g=gcd(p,q);need(q>0n,"positive denominator");return[p/g,q/g];}
function read(v){const [a,b="1"]=String(v).split("/");return Q(BigInt(a),BigInt(b));}
function add(a,b){return Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return Q(a[0]*b[0],a[1]*b[1]);}
function eq(a,b){return a[0]*b[1]===a[1]*b[0];}
function power(a,k){return Q(a[0]**BigInt(k),a[1]**BigInt(k));}
function dyadic(v){need(/^0x[0-9a-f]+$/.test(v.numerator_hex)&&Number.isSafeInteger(v.denominator_binary_exponent)&&v.denominator_binary_exponent>=0&&v.denominator_binary_exponent<=1024,"dyadic schema");return Q(BigInt(v.numerator_hex),1n<<BigInt(v.denominator_binary_exponent));}
function same(a,b,m){need(eq(a,b),m);}
function mod(a,q){return (a%q+q)%q;}
function bits(x){let n=0;for(;x;x&=x-1)n++;return n;}
function pair(row,x){
  const local=(a,b)=>!(a&1)?1:!(b&1)?2:3,u=local(row[0],row[1]),v=local(row[2],row[3])<<2;
  const half=mask=>mod(row.reduce((s,a,i)=>s+((mask>>i)&1?a*((x>>i)&1?-1:1):0),0)/2,2);
  return x^(!half(u)?u:!half(v)?v:u^v);
}
function increment(H,label,e,c=1){const key=`${label},${e}`;H.set(key,(H.get(key)||0)+c);}
function firstCensus(){
  const H=new Map();
  for(let code=0;code<4096;code++){
    const row=Array.from({length:4},(_,i)=>1+4*((code>>(3*i))&7));
    for(let x=0;x<16;x++){
      const y=pair(row,x);if(x>=y)continue;
      const d=row.reduce((s,a,i)=>s+a*(((y>>i)&1)-((x>>i)&1)),0);
      need(d%4===0,"first coarse relation");increment(H,mod(d/4,8),bits(x^y));
    }
  }
  return H;
}
function secondCensus(){
  const H=new Map();
  for(let code=0;code<4096;code++){
    const row=Array.from({length:4},(_,i)=>(code>>(3*i))&7);
    for(let x=0;x<16;x++){
      const y=pair(row,x);if(x>=y)continue;
      const d=row.reduce((s,a,i)=>s+a*(((y>>i)&1)-((x>>i)&1)),0);
      need(d%4===0,"second coarse relation");
      for(let tag=0;tag<16;tag++){
        const e=row.reduce((s,_,i)=>s+(((x^y)>>i)&1?((tag>>i)&1?4:2):0),0);
        increment(H,mod(d/4,2),e,3**(4-bits(tag)));
      }
    }
  }
  return H;
}
function checkRecipe(R,v,modulus){
  const z=Q(1n,BigInt(modulus)),one=Q(1n),half=Q(1n,2n),notV=Q(v[1]-v[0],v[1]);
  same(dyadic(R.visibility),v,"recipe visibility");
  same(dyadic(R.zero_label_coin_probability),z,"paid zero coin");
  same(dyadic(R.keep_paid_nonzero_qubit_probability),Q(BigInt(modulus-1),BigInt(modulus)),"keep probability");
  same(dyadic(R.replacement_plus_probability_including_zero_coin),mul(mul(z,add(one,v)),half),"matched plus block");
  same(dyadic(R.replacement_minus_probability_including_zero_coin),mul(mul(z,notV),half),"matched minus block");
  same(dyadic(R.conditional_Z_flip_probability),mul(notV,half),"noise matching Z coin");
  need(R.paid_qubit_consumed_before_zero_coin===true&&R.public_visibility_record_retained===true&&
       R.unknown_preparation_inverse_used===false&&R.hardware_backend_executed===false,"channel resource scope");
}
function checkLevel(R,H,modulus){
  let total=0,nonzero=0;const tags=new Set();
  for(const [key,c]of H){total+=c;const[l,e]=key.split(",").map(Number);if(l)nonzero+=c;tags.add(e);}
  need(R.output_modulus===modulus&&R.raw_census_total===total,"raw source total");
  same(dyadic(R.base_visibility),Q(3n,4n),"visibility root lineage");
  need(R.joint_label_visibility_rows.length===H.size,"joint law coverage");
  const seen=new Set();
  for(const row of R.joint_label_visibility_rows){
    const key=`${row.label},${row.visibility_exponent}`,count=H.get(key);
    need(count===row.raw_count&&!seen.has(key),"regenerated source multiplicity");seen.add(key);
    for(let l=0;l<modulus;l++)need(H.get(`${l},${row.visibility_exponent}`)===count,"joint label/tag independence");
    same(read(row.target_probability),Q(BigInt(count),BigInt(total)),"target source mass");
    same(read(row.restored_probability),Q(BigInt(count),BigInt(total)),"restored CQ mass");
  }
  need(R.accepted_nonzero_input_rows.length===H.size*(modulus-1)/modulus,"accepted source coverage");
  const acceptedSeen=new Set();let conditionalSum=Q(0n);
  for(const row of R.accepted_nonzero_input_rows){
    const key=`${row.label},${row.visibility_exponent}`,count=H.get(key);
    need(row.label>0&&row.label<modulus&&count&&!acceptedSeen.has(key),"accepted source label");acceptedSeen.add(key);
    const conditional=Q(BigInt(count),BigInt(nonzero));
    same(read(row.conditional_probability),conditional,"charged conditional source");conditionalSum=add(conditionalSum,conditional);
    same(mul(conditional,Q(BigInt(modulus-1),BigInt(modulus))),Q(BigInt(count),BigInt(total)),"nonzero restored channel action");
  }
  same(conditionalSum,Q(1n),"conditional source normalization");
  same(read(R.charged_nonzero_admission_probability),Q(BigInt(modulus-1),BigInt(modulus)),"zero failure cost");
  need(R.replacement_recipes_by_exponent.length===tags.size,"visibility recipe coverage");
  const recipeTags=new Set();for(const row of R.replacement_recipes_by_exponent){
    need(tags.has(row.visibility_exponent)&&!recipeTags.has(row.visibility_exponent),"distinct recipe tag");recipeTags.add(row.visibility_exponent);
    checkRecipe(row.recipe,power(Q(3n,4n),row.visibility_exponent),modulus);
    let injected=Q(0n);for(const input of R.accepted_nonzero_input_rows)if(input.visibility_exponent===row.visibility_exponent)
      injected=add(injected,mul(read(input.conditional_probability),Q(1n,BigInt(modulus))));
    same(injected,Q(BigInt(H.get(`0,${row.visibility_exponent}`)),BigInt(total)),"zero source block restoration");
  }
  need(R.exact_joint_label_visibility_law_restored===true&&R.pure_replacement_matches_noisy_zero_blocks===false&&
       R.original_higher_labels_retained===false&&R.source_theorem_inferred_from_finite_histogram===false,"source law scope");
}
function verify(R){
  need(R.contract_id==="noise_matched_zero_label_conditional_native_source_restoration_v1"&&
       R.status==="CONDITIONAL_LOCAL_DERIVATION_EXTERNAL_REVIEW_PENDING"&&R.accepted_speedup_candidate===false&&R.novelty_claim===false&&
       R.actual_natural_source_noise_certified===false&&R.external_theorem_review_complete===false&&R.source_quantum_preparations_executed===0,"global admission");
  const P=R.assumed_not_inferred_premises;
  need(P.original_noise_model==="independent-balanced-original-phase-depolarization","independent balanced source premise");
  ["public_visibility_independent_of_fresh_higher_labels","pair_selection_reads_only_coarse_labels","original_diagonal_is_flat",
   "original_higher_label_transcript_discarded","fresh_independent_batches_per_attempt",
   "joint_input_state_factors_conditioned_on_fixed_unknown_secret"].forEach(k=>need(P[k]===true,"missing premise: "+k));
  const first=firstCensus();let a=0,b=0;for(const [key,c]of first){if(key.endsWith(",2"))a+=c;else if(key.endsWith(",4"))b+=c;else throw new Error("unexpected first-level tag");}
  need(a===3*b,"regenerated first-level 3:1 tag law");
  need(R.two_level_exact_censuses.length===2,"source level coverage");checkLevel(R.two_level_exact_censuses[0],first,8);checkLevel(R.two_level_exact_censuses[1],secondCensus(),2);
  const C=R.implemented_wrapper_supply;
  need(C.original_qubits_per_first_level_raw_attempt===4&&C.ideal_no_failure_two_level_original_qubits===16&&
       C.these_costs_are_universal_lower_bounds===false&&C.zero_coin_is_drawn_only_after_a_paid_nonzero_output===true,"supply architecture scope");
  same(read(C.first_level_original_qubits_per_restored_output),Q(32n,7n),"first paid supply");
  same(read(C.first_level_outputs_per_second_level_restored_output),Q(8n),"second paid supply");
  same(read(C.original_qubits_per_second_level_restored_output),Q(256n,7n),"composed paid supply");
  const s=R.scope;
  need(s.abstract_balanced_product_source_family_closed_under_this_channel===true&&s.induction_requires_fresh_independent_batches_and_label_visibility_independence===true,"conditional closure premise");
  ["all_joint_natural_lattice_noise_models_covered","correlated_original_faults_covered_by_marginal_visibility",
   "old_full_higher_label_transcript_may_be_retained","exponential_recursive_supply_or_visibility_loss_removed",
   "hardware_reset_or_Z_coin_backend_implemented"].forEach(k=>need(s[k]===false,"scope expansion: "+k));
  return{status:"ok",exact_source_levels:2,actual_natural_source_noise_certified:false};
}
module.exports={verify};
if(require.main===module){const file=process.argv[2]||path.resolve(__dirname,"../phase_workbench/dcp_noise_matched_source.json");console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(file,"utf8")))));}
