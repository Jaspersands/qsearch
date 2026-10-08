"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../classical_baselines/ternary_character_synchronization.json"),"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},same=(a,b,m)=>check(JSON.stringify(a)===JSON.stringify(b),m);
const mod=(x,q)=>(x%q+q)%q,dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),key=JSON.stringify;
const directions=[[1,0],[-1,0],[0,1],[0,-1],[1,-1],[-1,1]];
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
function frac(a,b){const g=gcd(a,b);a/=g;b/=g;return b===1n?String(a):a+"/"+b;}
function chart(level){
  let V=[[1n,0n],[0n,1n]],pi=[[-1n,-1n],[1n,-2n]];
  for(let j=0;j<level-1;j++)V=V.map(row=>pi[0].map((_,i)=>row.reduce((s,a,k)=>s+a*pi[k][i],0n)));
  const q=3n**BigInt(Math.ceil(level/2)),den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]);
  const a=q*(2n*V[1][1]+V[1][0]),b=q*(-2n*V[0][1]-V[0][0]);check(a%den===0n&&b%den===0n,"exact native frequency chart");
  const u=a/den,v=b/den;return label=>{const[x,y]=label.map(BigInt);return[Number(mod(u*x+v*y,q)),Number(mod((u+v)*x-u*y,q))];};
}
function ledger(x){
  const n=BigInt(x.components),r=BigInt(x.root_digits),m=BigInt(x.original_native_qutrits),q=3n**r,K=6n*m+1n,C=K*K,P=C*(C-1n)/2n,g=r===1n?1n:3n;
  check(x.modulus===String(q)&&BigInt(x.fixed_vocabulary_nodes)===K&&BigInt(x.complete_moment_constraint_entries)===C,"original native supply / full constraint count");
  const minfrac=(a,b)=>frac(a>b?b:a,b);
  check(x.fixed_A2_template_any_accidental_resonance_probability_upper===minfrac(P*g**n,q**n)&&x.generic_fixed_polynomial_vocabulary_resonance_upper===minfrac(P,3n**n),"fixed-template source probability bounds");
  check(x.any_shared_character_perfectly_fits_noise_probability_upper===minfrac(q**n*3n**m,q**(2n*m)),"paired-noise perfect character union bound");
  const rankN=3n**n-1n,rankD=2n*3n**(2n*m);check(x.unit_basis_rank_failure_probability_upper===minfrac(rankN,rankD),"unit-basis rank failure from projective kernel union");
  const bound=s=>{const a=s.split("/");return [BigInt(a[0]),a.length===1?1n:BigInt(a[1])];},terms=[x.fixed_A2_template_any_accidental_resonance_probability_upper,x.any_shared_character_perfectly_fits_noise_probability_upper,x.unit_basis_rank_failure_probability_upper].map(bound);
  let a=1n,b=1n;for(const[c,d]of terms){a=a*d-c*b;b*=d;}check(x.local_fake_and_global_rejection_and_unit_basis_probability_lower===frac(a>0n?a:0n,b),"joint source event lower bound without independence assertion");
  for(const k of["same_result_for_label_adaptive_syzygy_templates","source_distribution_bound_is_pointwise_certificate","quantum_or_all_classical_decoder_lower_bound"])check(x[k]===false,"source bound scope: "+k);
}
function sync(records,w){
  const q=records[0].modulus,n=records[0].first.length,L=2*records.length,nodes=[{formal_coefficients:Array(L).fill(0),frequency:Array(n).fill(0),phase_exponent:0}];
  records.forEach((r,j)=>directions.forEach(([a,c])=>{const f=Array(L).fill(0);f[2*j]=mod(a,q);f[2*j+1]=mod(c,q);nodes.push({formal_coefficients:f,frequency:r.first.map((x,i)=>mod(a*x+c*r.second[i],q)),phase_exponent:mod(a*r.outcome[0]+c*r.outcome[1],q)});}));
  same(w.nodes,nodes,"fixed native formal vocabulary and counterfeit phases");const seen=new Map(),resonances=[],violations=[];
  nodes.forEach((u,i)=>nodes.forEach((v,j)=>{const f=u.frequency.map((x,k)=>mod(x-v.frequency[k],q)),a=u.formal_coefficients.map((x,k)=>mod(x-v.formal_coefficients[k],q)),h=mod(u.phase_exponent-v.phase_exponent,q),k=key(f);
    if(!seen.has(k))seen.set(k,[a,h,i,j]);const old=seen.get(k);
    if(key(a)!==key(old[0]))resonances.push({first_pair:[old[2],old[3]],second_pair:[i,j],frequency:f,formal_residual:a.map((x,k)=>mod(x-old[0][k],q))});
    if(h!==old[1])violations.push({first_pair:[old[2],old[3]],second_pair:[i,j],frequency:f,nonzero_phase_residual:mod(h-old[1],q)});
  }));
  check(w.all_moment_entries_checked===nodes.length**2&&w.moment_matrix_dimension===nodes.length,"complete difference audit");
  check(w.accidental_difference_resonance_count===resonances.length&&w.violated_difference_constraint_count===violations.length&&w.rank_one_witness_is_valid_for_the_relaxation===(violations.length===0)&&w.no_accidental_formal_difference_resonances===(resonances.length===0),"exact local relaxation feasibility");
  same(w.resonance_witnesses,resonances.slice(0,8),"resonance witnesses");same(w.constraint_violation_witnesses,violations.slice(0,8),"phase violations");
  check(w.matrix_rank_exactly_one&&w.diagonal_entries_exactly_one&&w.phase_variables_are_exact_qth_roots&&w.perfect_local_paired_phase_score===3*records.length&&w.perfect_local_phase_fit_proves_shared_secret===false,"rank-one Gram certificate is not a character");return nodes.length**2;
}
function validator(records,v){
  const q=records[0].modulus,n=records[0].first.length,A=records.flatMap(r=>[r.first,r.second]),y=records.flatMap(r=>r.outcome),basis=v.unit_basis_frequency_rows,I=v.modular_unit_basis_inverse;
  check(basis.length===n&&new Set(basis).size===n&&v.rank_mod3===n,"complete unit row basis");
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)check(mod(A[basis[i]].reduce((s,x,k)=>s+x*I[k][j],0),q)===Number(i===j),"composite-ring inverse checked without field assumption");
  const trial=I.map(row=>mod(dot(row,basis.map(i=>y[i])),q));same(v.basis_interpolated_secret_trial,trial,"public interpolated phases, no hidden secret");
  const relations=A.map((row,j)=>{const coefficients=Array.from({length:n},(_,k)=>mod(row.reduce((s,x,i)=>s+x*I[i][k],0),q)),weights=Array(A.length).fill(0);weights[j]=1;basis.forEach((i,k)=>weights[i]=mod(weights[i]-coefficients[k],q));
    for(let k=0;k<n;k++)check(mod(weights.reduce((s,x,i)=>s+x*A[i][k],0),q)===0,"exact original-frequency syzygy");
    return{target_frequency_row:j,basis_coefficients:coefficients,native_frequency_relation_weights:weights,outcome_phase_residual:mod(dot(weights,y),q)};
  });same(v.all_native_group_relations,relations,"all public modular relation constraints");const first=relations.find(x=>x.outcome_phase_residual)||null;
  same(v.first_nonzero_character_relation,first,"retained character falsifier");check(v.full_group_character_fit_certified===(first===null)&&v.status===(first?"RANK_ONE_PHASE_FIT_NOT_A_CHARACTER":"EXACT_CHARACTER_FIT"),"complete character fit status");
  check(v.truth_or_hidden_secret_used===false&&v.character_validator_is_a_noisy_secret_decoder===false,"validation is not noisy recovery");return{A,y,basis,relations,q,n};
}
function adaptive(data,c){
  const{A,y,basis,relations,q,n}=data,L=A.length,nodes=[],indices=new Map(),stencils=[],conjugated=new Set();
  function node(raw){const f=raw.map(x=>mod(x,q)),k=key(f);if(!indices.has(k)){indices.set(k,nodes.length);nodes.push({formal_coefficients:f,frequency:Array.from({length:n},(_,j)=>mod(f.reduce((s,x,i)=>s+x*A[i][j],0),q)),fake_observed_phase_exponent:mod(dot(f,y),q)});}return indices.get(k);}
  const zero=node(Array(L).fill(0)),native=A.map((_,j)=>node(Array.from({length:L},(_,i)=>Number(i===j))));
  function negative(i){const j=node(nodes[i].formal_coefficients.map(x=>-x));if(!conjugated.has(i)){stencils.push({kind:"conjugation",left_entry:[i,zero],right_entry:[zero,j]});conjugated.add(i);}return j;}
  function add(i,j){const k=node(nodes[i].formal_coefficients.map((x,l)=>x+nodes[j].formal_coefficients[l]));const neg=negative(j);stencils.push({kind:"addition",left_entry:[k,zero],right_entry:[i,neg]});return k;}
  const powers=new Map();function multiply(i,c){let total=zero,power=i,bit=0;while(c){if(c%2)total=add(total,power);c=Math.floor(c/2);bit++;if(c){const k=key([i,bit]);if(!powers.has(k))powers.set(k,add(power,power));power=powers.get(k);}}return total;}
  const loops=basis.map(i=>({basis_frequency_row:i,integer_multiplier:q,endpoint:multiply(native[i],q)})),targets=[];
  for(const r of relations){let total=zero;basis.forEach((i,k)=>{if(r.basis_coefficients[k])total=add(total,multiply(native[i],r.basis_coefficients[k]));});const target=native[r.target_frequency_row];stencils.push({kind:"native_target",left_entry:[total,zero],right_entry:[target,zero]});targets.push({frequency_row:r.target_frequency_row,computed_node:total,native_node:target});}
  same(c.nodes,nodes,"independently recompiled polynomial adaptive circuit nodes");same(c.linear_moment_stencils,stencils,"all addition/conjugation/target constraints including q-loops");same(c.basis_q_loops,loops,"integer q-power loops really compiled");same(c.native_target_maps,targets,"complete native targets");
  const failures=[];stencils.forEach((s,j)=>{const difference=p=>nodes[p[0]].frequency.map((x,k)=>mod(x-nodes[p[1]].frequency[k],q)),phase=p=>mod(nodes[p[0]].fake_observed_phase_exponent-nodes[p[1]].fake_observed_phase_exponent,q);
    same(difference(s.left_entry),difference(s.right_entry),"every moment stencil is native-valid");const r=mod(phase(s.left_entry)-phase(s.right_entry),q);if(r)failures.push({stencil_index:j,kind:s.kind,phase_residual:r});});
  same(c.fake_perfect_local_fit_violated_stencils,failures,"adaptive lift really rejects counterfeit perfect fit");
  const certs=relations.filter(r=>r.outcome_phase_residual).map(r=>{const norm=1+r.basis_coefficients.reduce((s,x)=>s+x*x,0);return{target_frequency_row:r.target_frequency_row,nonzero_modular_phase_residual:r.outcome_phase_residual,one_plus_basis_coefficient_squared_norm:norm,any_feasible_PSD_objective_gap_lower:frac(8n,BigInt(q*q*norm))};});
  same(c.all_rank_PSD_near_perfect_gap_certificates,certs,"all-rank rational objective gap certificates");const best=certs.length?certs.reduce((a,b)=>a.one_plus_basis_coefficient_squared_norm<b.one_plus_basis_coefficient_squared_norm?a:b):null;
  check(c.any_feasible_PSD_objective_gap_lower===(best?best.any_feasible_PSD_objective_gap_lower:"0")&&c.gap_is_to_impossible_perfect_score_not_true_secret_score===true,"gap scope and strongest bound");
  check(c.matrix_dimension===nodes.length&&c.dense_PSD_complex_entries===nodes.length**2&&c.selected_linear_moment_constraint_count===stencils.length&&c.every_rank_one_feasible_point_is_a_shared_group_character===true,"polynomial rank-one-sound circuit dimensions");
  for(const k of["convex_relaxation_tightness_proved","rank_one_optimum_or_efficient_decoder_supplied","PSD_rank_greater_than_one_certifies_a_distribution_over_characters","floating_approximate_rank_one_rounding_certified"])check(c[k]===false,"unproved convex decoder claim: "+k);
  return stencils.length;
}
const hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_CHARACTER_SYNCHRONIZATION.md"))).digest("hex");
check(R.derivation_sha256===hash&&R.status==="NATIVE_RANK_ONE_SYNCHRONIZATION_NOT_A_CHARACTER_REVIEW_PENDING","pinned derivation");
for(const k of["label_adaptive_lifts_or_all_spectral_methods_ruled_out","efficient_noisy_secret_decoder_supplied","quantum_speedup_proved","candidate_record_accepted"])check(R[k]===false,"unproved algorithm claim: "+k);
same(R.native_controls.map(c=>c.seed),[89513,89523,89533],"prespecified original native controls");let entries=0,relations=0,stencils=0;
for(const c of R.native_controls){
  ledger(c.ledger);const records=c.native_records,q=Number(c.ledger.modulus),at=chart(c.original_even_native_level),frequencies=c.original_ring_labels.map(row=>{const f=row.map(at);return[f.map(x=>x[0]),f.map(x=>x[1])];});
  same(c.original_native_frequencies,frequencies,"original cyclotomic ring-frequency chart");records.forEach((r,i)=>{same(r.first,frequencies[i][0],"actual original first frequency");same(r.second,frequencies[i][1],"actual original second frequency");check(r.modulus===q,"actual retained full root");});
  check(records.length===c.ledger.original_native_qutrits&&new Set(c.original_ancestry_ids).size===records.length&&c.source_law_physically_certified===false,"original qutrit ledger / no external IID certificate");
  entries+=sync(records,c.witness);const data=validator(records,c.validator);relations+=data.relations.length;stencils+=adaptive(data,c.adaptive_character_lift);
  const honest=records.map(r=>({...r,outcome:[mod(dot(r.first,c.calibration_secret),q),mod(dot(r.second,c.calibration_secret),q)]}));validator(honest,c.honest_character_countercontrol);same(c.honest_character_countercontrol.basis_interpolated_secret_trial,c.calibration_secret,"honest source character positive countercontrol");
}
entries+=sync(R.label_resonance_countercontrol.records,R.label_resonance_countercontrol.witness);check(R.label_resonance_countercontrol.witness.violated_difference_constraint_count>0,"label-resonance scope countercontrol");
for(const x of R.growing_native_ledgers)ledger(x);
console.log(JSON.stringify({status:"PASS",exact_moment_entries:entries,public_native_syzygies:relations,recompiled_adaptive_moment_stencils:stencils,external_IID_supply_certified:false,noisy_decoder_supplied:false}));
