"use strict";
// Independent original-label rounding, lineage, source populations and alias replay.
// Value-dependent receipts are explicitly OUTSIDE the compressed-only observation.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,same,rat,parse,str,add,mul,div,cmp,one}=require("./cyclotomic_exact.js");
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/classical_baselines/native_classical_modulus_descent.json");
const mod=(x,q)=>(x%q+q)%q, enc=x=>x<=9007199254740991n&&x>=-9007199254740991n?Number(x):String(x);
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const digest=x=>crypto.createHash("sha256").update(JSON.stringify(canonical(x))).digest("hex");
const min=(a,b)=>cmp(a,b)<=0n?a:b;
function root(q){let r=0;check(q>=3n,"positive ternary modulus");while(q%3n===0n){q/=3n;r++;}check(q===1n,"ternary root");return r;}
function floorDiv(x,d){return (x-mod(x,d))/d;}
const third=x=>floorDiv(x+1n,3n);
function observation(p){return {modulus:p.modulus,labels:p.labels,values:p.values};}
function direction(labels,q){
  const n=labels[0][0].length,k=labels.length;check(k===n+1&&root(q)>=2,"actual complete block");
  const A=Array.from({length:n},(_,i)=>labels.map(([a,c])=>Number(mod(BigInt(a[i])+BigInt(c[i]),3n)))),pivots=[];
  let row=0;
  for(let col=0;col<k&&row<n;col++){
    let p=row;while(p<n&&!A[p][col])p++;if(p===n)continue;
    [A[row],A[p]]=[A[p],A[row]];const s=A[row][col];A[row]=A[row].map(x=>x*s%3);
    for(let i=0;i<n;i++)if(i!==row){const t=A[i][col];A[i]=A[i].map((x,j)=>(x-t*A[row][j]+6)%3);}
    pivots.push(col);row++;
  }
  const f=Array.from({length:k},(_,j)=>j).find(j=>!pivots.includes(j)),v=Array(k).fill(0);v[f]=1;
  pivots.forEach((p,i)=>v[p]=(3-A[i][f])%3);const s=v.find(x=>x);return v.map(x=>x*s%3);
}
function branch(labels,v,q){
  const n=labels[0][0].length;
  check(v.length===labels.length&&v.some(x=>x)&&v.every(x=>Number.isInteger(x)&&x>=0&&x<3),"canonical kernel direction");
  for(let i=0;i<n;i++)check(labels.reduce((s,[a,c],j)=>s+(BigInt(a[i])+BigInt(c[i]))*BigInt(v[j]),0n)%3n===0n,"original low kernel");
  const weights=[1,2].map(z=>v.map(x=>!x?[0,0]:x*z%3===1?[-2,1]:[-1,-1]));
  const reduced=weights.map(row=>Array.from({length:n},(_,i)=>{
    const delta=mod(labels.reduce((s,[a,c],j)=>s+BigInt(row[j][0])*BigInt(a[i])+BigInt(row[j][1])*BigInt(c[i]),0n),q);
    check(delta%3n===0n,"actual original-label divisibility");return enc(delta/3n);
  }));return {weights,reduced};
}
function next(inputs){
  check(inputs.length>0,"nonempty real pair inputs");const q=BigInt(inputs[0].modulus),n=inputs[0].labels[0].length,w=n+1;
  check(root(q)>=2,"remaining root");const ids=inputs.flatMap(p=>p.original_source_ids);
  check(new Set(ids).size===ids.length,"same original ancestors not independent");
  inputs.forEach(p=>check(BigInt(p.modulus)===q&&p.level===inputs[0].level&&p.labels.length===2&&p.labels.every(a=>a.length===n&&a.every(x=>BigInt(x)>=0n&&BigInt(x)<q))&&p.values.length===2&&p.values.every(x=>BigInt(x)>=0n&&BigInt(x)<q),"canonical actual records"));
  const used=Math.floor(inputs.length/w)*w,out=[];
  for(let start=0;start<used;start+=w){
    const parents=inputs.slice(start,start+w),labels=parents.map(p=>p.labels),v=direction(labels,q),{weights,reduced}=branch(labels,v,q);
    const values=weights.map(row=>enc(mod(third(parents.reduce((s,p,j)=>s+BigInt(row[j][0])*BigInt(p.values[0])+BigInt(row[j][1])*BigInt(p.values[1]),0n)),q/3n)));
    out.push({modulus:enc(q/3n),labels:reduced,values,kind:"DESCENDED_CORRELATED_CLASSICAL_PAIR",level:inputs[0].level+1,
      original_source_ids:parents.flatMap(p=>p.original_source_ids),direction:v,branch_weights:weights,parent_record_sha256:parents.map(digest),
      fresh_original_errors_created:false,pair_errors_assumed_independent:false,receipt_hashes_are_excluded_from_compressed_only_receiver:true});
  }
  const cost={input_pairs:inputs.length,output_pairs:out.length,input_modulus:enc(q),output_modulus:enc(q/3n),block_width:w,pairs_used:used,
    unused_original_source_ids:inputs.slice(used).flatMap(p=>p.original_source_ids),original_ancestors_paid_once:ids.length,
    label_preprocessing_arithmetic_order_per_block:"O(n^3) over F3 and O(n^2) log(q)-bit arithmetic",
    quantum_only_unknown_phases_are_an_input:false,retained_parent_values_are_part_of_observation:false};return {out,cost};
}
function guess(g){
  const Q=BigInt(g.original_modulus),d=g.levels,n=g.dimension,t=g.final_pairs,r=root(Q);
  check([d,n,t].every(Number.isSafeInteger)&&d>0&&d<r&&n>0&&t>=0,"scoped information dimensions");
  const q=Q/3n**BigInt(d),alias=rat(1n,3n**BigInt(n*d)),p=2*t-n,scale=rat(q**BigInt(Math.max(0,p)),q**BigInt(Math.max(0,-p)));let b=mul(alias,min(one,scale));
  if(g.true_conditional_pair_max_atom_upper!==null){
    const beta=parse(g.true_conditional_pair_max_atom_upper);check(cmp(beta,rat(1n,q*q))>=0n&&cmp(beta,one)<=0n,"true joint atom premise");
    b=mul(alias,min(one,mul(scale,rat(beta[0]**BigInt(t),beta[1]**BigInt(t)))));
  }
  const short=Math.max(b[0].toString(2).length,b[1].toString(2).length)<=12000;
  check(BigInt(g.remaining_modulus)===q&&g.erased_secret_trits===n*d&&g.alias_only_full_secret_success_upper===str(alias)&&g.full_original_secret_guessing_success_upper===(short?str(b):null)&&g.observation_alphabet_bound_applied===true,"actual quotient erasure/likelihood upper");
  same(g.full_original_secret_guessing_success_upper_power3_without_atom,g.true_conditional_pair_max_atom_upper===null?{base:3,exponent:-n*d+Math.min(0,(r-d)*p)}:null,"symbolic exact large information bound");
  check(g.uniform_original_secret_and_secret_independent_labels_errors_required===true&&g.independent_final_noise_pairs_given_labels_required_for_atom_bound===(g.true_conditional_pair_max_atom_upper!==null),"source and conditional correlation premises");
  check(g.receiver_input==="ONLY final labels/values and secret-independent label-only metadata"&&g.repeated_preparation_from_same_compressed_records_adds_information===false&&g.all_original_data_algorithms_or_quantum_LWE_are_ruled_out===false,"information scope");
  same(g.excluded_inputs,["original or intermediate responses","value-dependent hashes/receipts","truth/noise fixtures","quantum-only source states"],"no parent hash side-channel in receiver");
}
function source(c){
  const q=BigInt(c.original_modulus),s=c.fixed_low_slopes,labels=s.map(b=>[[0],[b]]),v=direction(labels,q),site=v.findIndex(x=>x),counts=new Map(),low=new Map();
  same(v,c.direction,"low-only direction independently replayed");check(c.varied_active_site===site,"actual active site");
  for(let a=0n;a<q;a++)for(let h=0n;h<q/3n;h++){
    const changed=labels.map(([a,c])=>[[...a],[...c]]);changed[site]=[[enc(a)],[enc(mod(BigInt(s[site])-a,3n)+3n*h)]];
    const key=JSON.stringify(branch(changed,v,q).reduced.map(a=>a[0]));counts.set(key,(counts.get(key)||0)+1);
    if(a%3n===0n)low.set(key,(low.get(key)||0)+1);
  }
  check(c.assignments_checked===Number(q*q/3n)&&c.remaining_pair_space===Number(q*q/9n)&&c.conditional_on_slopes_outputs===counts.size&&c.conditional_on_all_low_labels_outputs===low.size,"all original source assignments counted");
  same(c.conditional_on_slopes_multiplicities,[...new Set(counts.values())].sort(),"conditional slopes source fibres");same(c.conditional_on_all_low_labels_multiplicities,[...new Set(low.values())].sort(),"all low labels change source law");
  check(counts.size===Number(q*q/9n)&&low.size===Number(q*q/27n)&&c.all_low_labels_may_be_conditioned_without_changing_the_law===false,"conditional source distinction");return c.assignments_checked;
}
function lift(L,raw,truth){
  const q=BigInt(L.original_modulus),n=L.known_lower_input.length,lower=L.known_lower_input.map(BigInt),rows=raw.flatMap(p=>p.labels),values=raw.flatMap(p=>p.values),ids=raw.flatMap(p=>p.original_source_ids);
  check(L.original_records_read===rows.length&&L.known_lower_correctness_established===false&&L.row_basis_selected_from_labels_only===true&&L.all_rounding_equations_are_conditional_on_original_error_bound===true&&L.complete_original_secret_solver_supplied===false,"conditional original-bank input and cost");
  same(L.known_lower_input,truth.map(x=>enc(mod(BigInt(x),q/3n))),"truth lower prefix ONLY in conditional control");
  const A=Array.from({length:n},(_,i)=>rows.map(a=>Number(BigInt(a[i])%3n))),pivots=[];let rank=0;
  for(let col=0;col<rows.length&&rank<n;col++){
    let p=rank;while(p<n&&!A[p][col])p++;if(p===n)continue;
    [A[rank],A[p]]=[A[p],A[rank]];const s=A[rank][col];A[rank]=A[rank].map(x=>x*s%3);
    for(let i=0;i<n;i++)if(i!==rank){const t=A[i][col];A[i]=A[i].map((x,j)=>(x-t*A[rank][j]+6)%3);}
    pivots.push(col);rank++;
  }
  check(rank===n&&L.rank_mod3===n,"live source full low rank");same(L.label_only_basis_rows,pivots,"basis fixed before values");
  const transcript=rows.map((a,j)=>{
    const residual=mod(BigInt(values[j])-a.reduce((s,x,i)=>s+BigInt(x)*lower[i],0n),q),dist=[0n,1n,2n].map(t=>{
      const x=mod(residual-t*q/3n,q),y=mod(t*q/3n-residual,q);return x<y?x:y;
    });const chosen=dist.reduce((best,x,k)=>x<dist[best]?k:best,0);
    return {source_id:ids[j],corrected_original_response:enc(residual),circular_distances:dist.map(enc),rounded_top_equation:chosen};
  });same(L.rounding_transcript,transcript,"actual original corrected responses/centers");
  const B=pivots.map(j=>[...rows[j].map(x=>Number(BigInt(x)%3n)),transcript[j].rounded_top_equation]);
  for(let col=0;col<n;col++){
    let p=col;while(p<n&&!B[p][col])p++;check(p<n,"unit F3 original basis");[B[col],B[p]]=[B[p],B[col]];
    const scale=B[col][col];B[col]=B[col].map(x=>x*scale%3);
    for(let i=0;i<n;i++)if(i!==col){const s=B[i][col];B[i]=B[i].map((x,j)=>(x-s*B[col][j]+6)%3);}
  }
  const top=B.map(a=>a[n]),consistent=rows.every((a,j)=>Number(a.reduce((s,x,i)=>s+BigInt(x)*BigInt(top[i]),0n)%3n)===transcript[j].rounded_top_equation);
  check(consistent&&L.status==="CONDITIONAL_ORIGINAL_BANK_TOP_DIGIT_LIFT"&&L.rounding_consistency_proves_lower_input_or_noise_promise===false,"consistent conditional answer not a proof of premises");
  same(L.recovered_top_digits,top,"F3 top-digit equations");same(L.recovered_secret,lower.map((a,i)=>enc(a+q/3n*BigInt(top[i]))),"conditional full original lift");
}
function data(c){
  const first=c.histories[0].inputs,truth=c.truth_fixture_only,s=truth.original_secret,errors=truth.original_errors,Q=BigInt(first[0].modulus),n=s.length;
  check(errors.length===2*first.length&&c.original_values_verified===true,"complete calibration originals");
  first.forEach((p,j)=>{check(p.kind==="ORIGINAL_CLASSICAL_PAIR"&&p.level===0&&p.original_source_ids.length===2,"typed real originals");p.values.forEach((y,k)=>check(mod(p.labels[k].reduce((v,a,i)=>v+BigInt(a)*BigInt(s[i]),0n)+BigInt(errors[2*j+k]),Q)===BigInt(y),"actual noisy source values"));});
  let current=first,blocks=0;
  c.histories.forEach(h=>{same(h.inputs,current,"same actual parent bank");const r=next(current);same(h.outputs,r.out,"original labels/rounding/ancestry receipt replay");same(h.cost,r.cost,"all source contraction and preprocessing charged");current=r.out;blocks+=current.length;});
  const remaining=Q/3n**BigInt(c.histories.length),obs=current.map(observation),expectedAliases=[s,s.map(x=>enc(mod(BigInt(x)+remaining,Q))),s.map(x=>enc(mod(BigInt(x)+2n*remaining,Q)))];
  check(c.alias_replays.length===3,"actual quotient aliases");
  c.alias_replays.forEach((a,j)=>{
    same(a.secret_fixture_only,expectedAliases[j],"actual lost-digit secret shift");
    let other=first.map((p,index)=>({...p,values:p.labels.map((row,k)=>enc(mod(row.reduce((v,x,i)=>v+BigInt(x)*BigInt(a.secret_fixture_only[i]),0n)+BigInt(errors[2*index+k]),Q)))}));
    for(let d=0;d<c.histories.length;d++)other=next(other).out;
    check(a.final_observations_equal===(JSON.stringify(other.map(observation))===JSON.stringify(obs))&&a.final_observations_equal===true,"lost original-secret information even with noise");
    check(a.first_parent_receipt_equal===(digest(other[0])===digest(current[0])),"value-dependent receipt is separate information");
  });
  const g=c.full_secret_bound_for_compressed_only_receiver;guess(g);check(g.dimension===n&&BigInt(g.original_modulus)===Q&&g.levels===c.histories.length&&g.final_pairs===current.length,"bound on this actual compressed source");
  lift(c.conditional_original_bank_lift,first,s);
  check(c.conditional_lift_matches_truth===(JSON.stringify(c.conditional_original_bank_lift.recovered_secret)===JSON.stringify(s))&&c.conditional_lift_matches_truth===true&&c.lower_prefix_supplied_from_truth_FOR_CONTROL_ONLY===true,"original bank reopens digit recovery, lower truth is not an algorithm");
  check(c.secret_or_errors_read_by_transformation===false&&c.a_working_secret_decoder_is_supplied===false,"truth not receiver input");return blocks;
}
function noise(c){
  const q=BigInt(c.input_modulus)/3n,v=c.direction.filter(x=>x),law=c.original_error_law.map(([e,p])=>[BigInt(e),parse(p)]),counts=new Map();let assignments=0;
  function visit(j,e,p){
    if(j===2*v.length){
      assignments++;const sums=[0n,0n];v.forEach((x,k)=>{const a=e[2*k],b=e[2*k+1],delta=[b-2n*a,-b-a];sums[0]+=delta[x-1];sums[1]+=delta[2-x];});
      const key=JSON.stringify(sums.map(x=>enc(mod(third(x),q))));counts.set(key,add(counts.get(key)||rat(0n),p));return;
    }law.forEach(([x,t])=>visit(j+1,[...e,x],mul(p,t)));
  }visit(0,[],one);
  const expected=[...counts].map(([e,p])=>({errors:JSON.parse(e),probability:str(p)})).sort((a,b)=>a.errors[0]-b.errors[0]||a.errors[1]-b.errors[1]);
  same(c.law,expected,"joint rounded/modular noise distribution, not independent scalars");
  const largest=[...counts.values()].reduce((a,b)=>cmp(a,b)>=0n?a:b);
  check(c.assignments_evaluated===assignments&&c.pair_max_atom===str(largest)&&c.status==="EXACT_DECLARED_ORIGINAL_ERROR_LAW_PUSHFORWARD"&&c.law_inferred_from_observed_responses===false&&c.scalar_product_law_assumed===false,"declared noise/atom scope");return assignments;
}
function ledger(L){
  const q=BigInt(L.input_modulus),m=BigInt(L.active_sites),V=parse(L.true_input_marginal_second_moment_upper),f=L.independent_original_scalars_required?5n:9n;
  const before=mul(rat(f*m),V),after=add(mul(rat(2n,9n),before),rat(1n,2n));
  check(BigInt(L.output_modulus)===q/3n&&L.pre_rounding_branch_second_moment_upper===str(before)&&L.rounded_output_marginal_second_moment_upper===str(after)&&L.normalized_output_moment_upper===str(div(after,rat(q*q/9n))),"correlated noise moment recurrence");
  check(L.within_pair_covariance_before_rounding_upper_if_original_independent===(L.independent_original_scalars_required?str(mul(rat(2n*m),V)):null)&&L.within_pair_covariance_if_identical_scalar_variance_formula==="m * actual common variance","heteroscedastic original covariance not an IID derived-pair assumption");
  check(L.independent_input_pairs_and_conditional_joint_sign_symmetry_required===true&&L.output_pair_errors_independent===false&&L.moments_infer_maximum_noise_atom===false&&L.upper_bound_growth_is_a_noise_lower_bound_or_no_go===false&&L.source_premises_established_by_API===false,"conditional noise scope");
}
function scaling(c){
  const n=c.dimension,r=c.root_digits,M=c.original_pairs;let q=3n**BigInt(r),V=add(rat(q*q,3n*BigInt(n)**6n),rat(1n,2n));
  const required=BigInt(n+1)**BigInt(r-1);
  check(c.full_depth_levels_to_modulus3===r-1&&c.original_pairs_required_for_one_terminal_pair_under_this_policy===String(required)&&BigInt(c.terminal_pairs_available_under_same_bank_full_depth_policy)===BigInt(M)/required&&c.this_fixed_policy_resource_recurrence_is_a_universal_receiver_lower_bound===false,"full-depth same-bank sample contraction is a policy cost, not a general lower bound");
  c.levels.forEach((row,j)=>{
    const L=row.worst_support_noise_ledger;ledger(L);check(row.level===j+1&&row.remaining_pairs===Math.floor(M/(n+1)**(j+1))&&BigInt(L.input_modulus)===q&&L.active_sites===n+1&&L.true_input_marginal_second_moment_upper===str(V)&&L.independent_original_scalars_required===(j===0),"same data/noise recurrence with IID only on originals");
    q/=3n;V=parse(L.rounded_output_marginal_second_moment_upper);const g=row.compressed_only_full_secret_bound;guess(g);
    check(g.dimension===n&&BigInt(g.original_modulus)===3n**BigInt(r)&&g.levels===j+1&&g.final_pairs===row.remaining_pairs,"information ledger bound to same scaling data");
  });check(c.true_source_moment_and_conditional_pair_independence_established===false&&c.noise_upper_bound_is_a_general_obstruction===false,"conditional scaling not universal negative");
}
function liftLedger(L){
  const n=L.dimension,m=L.original_records,q=BigInt(L.original_modulus),V=parse(L.true_original_second_moment_upper),rank=rat(1n,3n**BigInt(Math.min(64,m-n))),loss=min(one,div(mul(rat(BigInt(36*m)),V),rat(q*q)));
  check(m>=n&&root(q)>=2,"valid original-bank row budget");
  same(L.IID_uniform_original_low_labels_rank_failure_upper_compact,{numerator:"3^n-1",denominator:"2*3^m",n,m},"symbolic exact original-label rank upper");
  check(L.rank_failure_upper_used_in_budget===str(rank)&&L.conditional_rounding_failure_union_upper===str(loss)&&L.conditional_lift_failure_upper_given_correct_lower===str(min(one,add(rank,loss))),"charged conditional original-bank failure budget");
  check(L.known_lower_correctness_is_an_external_premise===true&&L.original_noise_moments_and_label_source_promises_verified===false&&L.returned_consistent_solution_is_a_correctness_certificate===false&&L.original_bank_retention_is_charged_not_forbidden===true,"conditional classical lift is not an unconditional decoder");
}
function verify(p){
  check(p.status==="SOURCE_CORRECT_CLASSICAL_DESCENT_AND_COMPRESSED_ONLY_INFORMATION_AUDIT_REVIEW_PENDING","review-pending status");
  check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_classical_modulus_descent.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_CLASSICAL_MODULUS_DESCENT.md")),"current producer/derivation");
  const deps=["ternary_covariant_noise.py","ternary_measured_lattice_decoder.py","ternary_noise_degradation.py","native_full_root_slice.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"actual dependencies");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(p.source_law_controls.length===9&&p.original_data_controls.length===3&&p.declared_noise_controls.length===3&&p.scaling.length===4&&p.retained_original_bank_conditional_lift_ledgers.length===4,"declared finite scope");
  const populations=p.source_law_controls.map(source),blocks=p.original_data_controls.map(data),noises=p.declared_noise_controls.map(noise);p.scaling.forEach(scaling);
  p.retained_original_bank_conditional_lift_ledgers.forEach(liftLedger);
  check(p.accepted_speedup_candidate===false&&p.new_active_negative_result_created===false,"no candidate or general no-go admitted");
  return {verified:true,original_label_population_assignments:populations.reduce((a,b)=>a+b,0),original_data_descent_blocks:blocks.reduce((a,b)=>a+b,0),declared_joint_noise_assignments:noises.reduce((a,b)=>a+b,0),alias_replays:9,whole_secret_decoder_or_quantum_speedup:false};
}
module.exports={verify,next,direction,branch,guess};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));
