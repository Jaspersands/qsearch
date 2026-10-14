"use strict";
// Algebra, F3 blocks and event budgets; Arb probability replay is a separate gate.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),M=require("./native_small_multiple_completion_crosscheck.js"),C=require("./native_small_alphabet_decoder_crosscheck.js");
const {check,same,rat,parse,str,add,sub,mul,div,cmp,one,zero}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/classical_baselines/native_gaussian_quotient_completion.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const mod=(a,q)=>(a%q+q)%q,enc=x=>x>=-9007199254740991n&&x<=9007199254740991n?Number(x):String(x);
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const digest=x=>crypto.createHash("sha256").update(JSON.stringify(canonical(x))).digest("hex"),min=(a,b)=>cmp(a,b)<=0n?a:b;
function integer(x){check((typeof x==="number"&&Number.isSafeInteger(x))||typeof x==="string","exact integer transport");const b=BigInt(x);check(enc(b)===x,"canonical integer");return b;}
function flags(o,yes,no){yes.forEach(k=>check(o[k]===true,"required premise "+k));no.forEach(k=>check(o[k]===false,"unsupported claim "+k));}
function control(c){
  const raw=c.original_records,q=integer(raw[0].modulus),n=raw[0].label.length,s=c.truth_fixture_only.original_secret,e=c.truth_fixture_only.original_errors;
  const coef=integer(c.signed_coefficient),model=M.quotient(q,coef,c.supplied_multiple),R=c.alphabet_completion,A=R.adapter,Q=integer(model.remaining_modulus),g=integer(model.nonunit_factor);
  check(raw.length>0&&raw.length%2===0&&new Set(raw.map(x=>x.source_id)).size===raw.length,"actual distinct original pairs");
  same(A.model,model,"unit-part full-root multiple extraction");check(A.status==="ONE_TO_ONE_ORIGINAL_QUOTIENT_RECORDS"&&A.original_records_sha256===digest(raw)&&A.original_records_paid_once===raw.length,"adapter bound to original bank");
  const children=[],receipts=[];raw.forEach((r,i)=>{
    check(integer(r.modulus)===q&&r.label.length===n&&integer(r.value)>=0n&&integer(r.value)<q,"whole source shape");
    const residual=mod(integer(r.value)-r.label.reduce((a,x,j)=>a+integer(x)*integer(model.known_quotient_IF_multiple_is_true[j]),0n),q);
    const child={label:r.label.map(a=>enc(integer(a)%g)),value:enc((residual+Q/2n)/Q%g),modulus:enc(g),source_id:r.source_id};children.push(child);
    receipts.push({source_id:r.source_id,parent_record_sha256:digest(r),corrected_original_response:enc(residual),derived_record:child});
    check(mod(r.label.reduce((a,x,j)=>a+integer(x)*integer(s[j]),0n)+integer(e[i]),q)===integer(r.value),"truth-only original unwrapped noise");
    const h=s.map((x,j)=>(integer(x)-integer(model.known_quotient_IF_multiple_is_true[j]))/Q),derivedNoise=(integer(e[i])+Q/2n>=0n?(integer(e[i])+Q/2n)/Q:-((-integer(e[i])-Q/2n+Q-1n)/Q));
    check(mod(child.label.reduce((a,x,j)=>a+integer(x)*h[j],0n)+derivedNoise,g)===integer(child.value),"derived true-prefix equation at the actual root");
  });
  same(A.derived_records,children,"one-to-one actual derived records");same(A.record_receipts,receipts,"unchanged source IDs and parent hashes");
  flags(A,["parent_source_IDs_preserved"],["new_independent_original_samples_created","multiple_truth_or_Gaussian_law_certified","truth_or_errors_entered_adapter"]);
  if(R.decoder.algorithm==="CERTIFIED_AFFINE_SECRET_COORDINATES_AND_CANONICAL_SUBSTITUTION")require("./native_partial_coordinate_decoder_crosscheck.js").result(children,R.decoder);
  else C.result(children,R.decoder,R.max_matrix_entries);
  const candidate=R.decoder.candidate_secret.map((h,j)=>enc(integer(model.known_quotient_IF_multiple_is_true[j])+Q*integer(h)));
  same(R.candidate_secret,candidate,"actual candidate from derived solver, not truth assignment");check(R.multiple_equation_verified===true&&candidate.every((x,j)=>mod(coef*integer(x),q)===integer(c.supplied_multiple[j])),"original multiple equation");
  const distances=raw.map(r=>{const x=mod(integer(r.value)-r.label.reduce((a,y,j)=>a+integer(y)*integer(candidate[j]),0n),q);return enc(x<q-x?x:q-x);});
  const radius=integer(R.verification_radius);check(4n*radius<q&&distances.every(x=>integer(x)<=radius),"original public radius checked on every value");
  same(R.original_fit,{fits_public_radius:true,radius:enc(radius),original_circular_error_distances:distances,original_records_checked:raw.length,bounded_fit_alone_certifies_truth:false},"original-data verifier, not truth certification");
  check(R.status==="ONE_ALPHABET_COMPATIBLE_ORIGINAL_RADIUS_FIT_SOURCE_PREMISES_REQUIRED"&&c.completion_matches_truth_fixture===(JSON.stringify(s)===JSON.stringify(candidate)),"forward calibration comparison");
  flags(c,["multiple_inputs_generated_from_truth_FOR_CALIBRATION_ONLY"],["calibration_is_an_unbounded_Gaussian_source"]);
  flags(R,[],["multiple_membership_in_planted_orbit_certified","actual_planted_secret_or_noise_law_certified","free_multiple_producer_supplied"]);
  same(c.strict_zero_error_quotient_baseline,M.complete(raw,coef,c.supplied_multiple),"same-input old zero-error comparison");
  return raw.length;
}
function capture(L){
  const d=L.feature_block_dimension,m=integer(L.original_rows),eps=parse(L.row_escape_probability_lower);check(Number.isSafeInteger(d)&&d>0&&m>0n&&cmp(eps,zero)>=0n&&cmp(eps,one)<=0n,"feature/capture parameters");
  const T=eps[0]?(eps[1]+eps[0]-1n)/eps[0]:null,blocks=T?m/T:0n,e=T?BigInt(2*d)-blocks:null,bits=e===null||e>=0n?0n:(-e>64n?64n:-e),budget=rat(1n,1n<<bits);
  check(L.power_block===(T===null?null:enc(T))&&L.block_times_escape===(T===null?null:str(mul(rat(T),eps)))&&L.complete_power_blocks===enc(blocks)&&L.union_power2_exponent===(e===null?null:enc(e))&&L.rank_failure_upper===str(budget),"adaptive reciprocal-Bernoulli block bound");
  if(T)check(cmp(mul(rat(T),eps),one)>=0n,"power block actually gives a half bound");check(L.power_half_bound_uses_reciprocal_Bernoulli_inequality===true,"not a fitted decay exponent");
}
function rank(L){
  const n=L.dimension,D=C.layout(n,"cubic").length,Q=n*(n+1)/2,z=parse(L.zero_probability_lower_IN_truncated_law),t=parse(L.nonzero_probability_lower_IN_truncated_law);
  check(z[0]>=0n&&t[0]>=0n&&cmp(add(z,t),one)<=0n&&L.feature_dimension===D&&L.base_feature_dimension===D-Q&&L.quadratic_feature_dimension===Q,"base/quadratic dimensions and true law floors");
  const B=L.zero_row_base_rank_budget,T=L.nonzero_row_quadratic_rank_budget;capture(B);capture(T);
  check(B.feature_block_dimension===D-Q&&T.feature_block_dimension===Q&&B.original_rows===T.original_rows&&B.row_escape_probability_lower===str(mul(rat(2n,9n),z))&&T.row_escape_probability_lower===str(div(t,rat(3n))),"two-stage source rank events");
  check(L.conditional_rank_failure_upper===str(min(one,add(parse(B.rank_failure_upper),parse(T.rank_failure_upper)))),"base rank plus quadratic rank union");
  flags(L,["secret_translation_used_only_in_rank_proof_not_decoder","fixed_secret_original_uniform_labels_and_independent_noise_required"],["full_rank_established_by_source_promise_not_small_fixtures"]);
}
function cube(q,n){return n?cube(q,n-1).flatMap(w=>Array.from({length:q},(_,a)=>[...w,a])):[[]];}
function grid(G){
  const n=G.dimension,L=C.layout(n,"cubic"),D=L.length,Q=n*(n+1)/2;
  const rows=cube(9,n).map(a=>C.equation(a,0,"cubic")[0]),indices=L.map((a,i)=>[a[0],i]).filter(([k])=>k!=="u2"&&k!=="uij").map(([,i])=>i),base=rows.map(r=>indices.map(i=>r[i]));
  const quad=cube(3,n).map(a=>{const r=[];for(let i=0;i<n;i++)for(let j=i;j<n;j++)r.push(a[i]*a[j]%3);return r;});
  const fullRank=C.solve(rows,rows.map(()=>0),D).rank,baseRank=C.solve(base,base.map(()=>0),D-Q).rank,quadRank=C.solve(quad,quad.map(()=>0),Q).rank;
  same(G,{dimension:n,full_feature_dimension:D,quadratic_dimension:Q,zero_label_grid_rows:9**n,zero_coefficient_rank:fullRank,zero_base_coefficient_rank:baseRank,zero_coefficient_sha256:digest(rows),base_column_indices:indices,quadratic_label_grid_rows:3**n,quadratic_rank:quadRank,quadratic_sha256:digest(quad)},"whole structural grids reconstructed from integer carries");
  check(fullRank===D-Q&&baseRank===D-Q&&quadRank===Q,"zero and nonzero blocks have claimed complete ranks");
}
function separationBig(L){
  const m=integer(L.original_rows);if(m<=9007199254740991n){M.separation(L);return;}
  const q=integer(L.original_modulus),n=L.dimension,R=integer(L.verification_radius),rows=L.valuation_small_ball_certificates,r=rows.length;
  check(q===3n**BigInt(r)&&4n*R<q,"actual full-root source code");let maxE=null;
  rows.forEach((x,d)=>{const H=3n**BigInt(r-d),a=2n*(2n*R/(3n**BigInt(d)))+1n,b=x.exact_probability_power_block,D=H**BigInt(b),N=a**BigInt(b),k=BigInt((D/N).toString(2).length-1),popbits=(3n**BigInt((r-d)*n)-1n).toString(2).length,blocks=m/BigInt(b),e=BigInt(popbits)-k*blocks;
    same(x,{difference_valuation:d,subgroup_order:enc(H),small_ball_numerator:enc(a),small_ball_denominator:enc(H),difference_population_base3_exponent:(r-d)*n,population_upper_ceil_log2:popbits,exact_probability_power_block:b,power_negative_log2_floor:Number(k),complete_power_blocks:enc(blocks),term_upper_power2_exponent:enc(e)},"large-bank exact source-code stratum");
    maxE=maxE===null||e>maxE?e:maxE;});
  const exponent=maxE+BigInt(r>1?BigInt(r-1).toString(2).length:0),bits=exponent>=0n?0n:(-exponent>64n?64n:-exponent);
  check(L.dyadic_union_upper_exponent===enc(exponent)&&L.exact_union_upper_if_short===null&&L.global_code_separation_failure_upper_used===str(rat(1n,1n<<bits)),"big integer source union without floating row counts");
  flags(L,["IID_uniform_original_label_rows_required","separation_event_covers_all_secrets_and_adaptive_candidates"],["candidate_count_union_multiplier_required","fixed_instance_distance_certified"]);
}
function probabilityBox(b){const lo=parse(b.lower),hi=parse(b.upper);check(cmp(lo,zero)>=0n&&cmp(lo,hi)<=0n&&cmp(hi,one)<=0n,"probability enclosure syntax");}
function source(P){
  const n=P.dimension,r=P.root_digits,q=3n**BigInt(r),m=integer(P.original_rows),alpha=parse(P.continuous_D_alpha_width);
  check(n>0&&r>0&&m>0n&&cmp(alpha,zero)>0n&&cmp(alpha,one)<0n,"declared source parameters");
  separationBig(P.original_code_separation_ledger);
  check(integer(P.original_code_separation_ledger.original_modulus)===q&&integer(P.original_code_separation_ledger.original_rows)===m&&P.original_code_separation_ledger.dimension===n,"same original source code event");
  const original=P.original_Gaussian_radius_law;probabilityBox(original);check(original.continuous_Gaussian_width===str(mul(alpha,rat(q)))&&original.integer_error_radius===P.original_code_separation_ledger.verification_radius,"same original Gaussian radius");
  const originalTail=min(one,mul(rat(m),parse(original.upper)));check(P.original_radius_event_failure_upper===str(originalTail),"whole original radius failure");let union=add(originalTail,parse(P.original_code_separation_ledger.global_code_separation_failure_upper_used));
  const seen=new Set();P.valuation_terms.forEach(T=>{const d=T.valuation,G=T.Gaussian_derived_error_law;
    check(Number.isSafeInteger(d)&&d>=2&&d<r&&!seen.has(d),"declared true-prefix valuations");seen.add(d);
    check(G.continuous_Gaussian_width===str(mul(alpha,rat(3n**BigInt(d)))),"exact alpha*g derived Gaussian law");[G.zero,G.each_signed_one,G.outside_triplet].forEach(probabilityBox);
    flags(G,[],["independent_transcendental_certificate_supplied","conditioning_erases_outside_triplet_mass"]);
    const R=T.conditional_rank_ledger;rank(R);check(R.dimension===n&&integer(R.zero_row_base_rank_budget.original_rows)===m&&R.zero_probability_lower_IN_truncated_law===G.zero.lower&&R.nonzero_probability_lower_IN_truncated_law===str(mul(rat(2n),parse(G.each_signed_one.lower))),"unconditional bin floors valid in the scalar-truncated law");
    const tail=min(one,mul(rat(m),parse(G.outside_triplet.upper))),failure=min(one,add(tail,parse(R.conditional_rank_failure_upper)));
    check(T.whole_original_bank_outside_triplet_failure_upper===str(tail)&&T.fixed_valuation_failure_upper===str(failure)&&T.conditioning_on_data_selected_multiple_truth===false,"tail retained before adaptive coverage");union=add(union,failure);
  });union=min(one,union);
  check(P.uniform_local_failure_upper===str(union)&&P.external_true_usable_multiple_coverage_failure_upper===null&&P.recovery_failure_upper_IF_coverage_and_source_laws_hold===null,"no granted coverage or uncharged global events");
  check(P.source_alpha_q_at_least_2_sqrt_n===(cmp(mul(mul(alpha,alpha),rat(q*q)),rat(BigInt(4*n)))>=0n)&&integer(P.logical_matrix_entries_for_each_decoder)===m*BigInt(C.layout(n,"cubic").length+1),"scalar source guard and paid full matrix");
  flags(P,["all_valuations_union_before_external_data_selected_multiple","full_declared_matrix_and_uncapped_multiple_coverage_required","external_coverage_is_for_known_coefficient_and_multiple_pairs"],["source_law_or_multiple_producer_supplied","unit_parts_at_same_valuation_create_independent_source_banks","unknown_coefficient_list_scan_implemented_in_this_module"]);
}
function verify(p){
  check(p.status==="SOURCE_CORRECT_GAUSSIAN_QUOTIENT_COMPLETION_AND_SPLIT_RANK_REVIEW_PENDING","review pending");
  check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_gaussian_quotient_completion.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_GAUSSIAN_QUOTIENT_COMPLETION.md")),"current producer/derivation");
  const deps=["native_small_multiple_completion.py","native_small_alphabet_decoder.py","native_classical_modulus_descent.py","native_full_root_slice.py","native_partial_coordinate_decoder.py","ternary_covariant_noise.py","ternary_noise_degradation.py","ternary_measured_lattice_decoder.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"dependency set");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(p.actual_original_data_controls.length===3&&p.zero_quadratic_structural_grids.length===3&&p.conditional_Gaussian_source_profiles.length===6,"declared coverage");
  const records=p.actual_original_data_controls.map(control);p.zero_quadratic_structural_grids.forEach(grid);p.conditional_Gaussian_source_profiles.forEach(source);
  flags(p,[],["accepted_speedup_candidate","new_active_negative_result_created","Gaussian_LWE_solver_or_new_quantum_algorithm","novelty_claim"]);
  return{verified:true,original_record_adaptations_replayed:records.reduce((a,b)=>a+b,0),structural_grids:3,conditional_source_budgets:6,
    Gaussian_special_function_boxes_recomputed:false,separate_Arb_probability_replay_required:true,multiple_producer_supplied:false};
}
module.exports={verify,control,capture,rank,source};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));
