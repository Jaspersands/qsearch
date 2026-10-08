"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto"),cp=require("child_process");
const root=path.join(__dirname,"../.."),reportPath=process.argv[2]||path.join(root,"research/classical_baselines/ternary_observable_moment_lift.json");
const R=JSON.parse(fs.readFileSync(reportPath,"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},key=JSON.stringify;
const same=(a,b,m)=>check(key(a)===key(b),m),mod=(x,q)=>(x%q+q)%q,dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
function frac(a,b){const g=gcd(a,b);a/=g;b/=g;return b===1n?String(a):a+"/"+b;}
check(R.derivation_sha256===hash(path.join(root,"research/TERNARY_OBSERVABLE_MOMENT_LIFT.md")),"pinned observable derivation");
check(R.source_report==="research/classical_baselines/ternary_character_synchronization.json","known source path");
const basePath=path.join(root,R.source_report),base=JSON.parse(fs.readFileSync(basePath,"utf8"));
check(R.source_report_sha256===hash(basePath),"pinned original native source report");
const sourceCheck=JSON.parse(cp.execFileSync("node",[path.join(__dirname,"ternary_character_synchronization_crosscheck.js"),basePath],{encoding:"utf8"}));
check(sourceCheck.status==="PASS"&&sourceCheck.external_IID_supply_certified===false,"independent original cyclotomic/native audit");
function basis(records,b){
  const q=records[0].modulus,n=records[0].first.length,D=records.map(r=>r.first.map((a,j)=>mod(a-r.second[j],q))),I=b.modular_unit_difference_inverse,indices=b.basis_record_indices;
  check(b.status==="FULL_UNIT_DIFFERENCE_BASIS"&&b.rank_mod3===n&&indices.length===n&&new Set(indices).size===n,"full difference basis");
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)check(mod(dot(D[indices[i]],I.map(row=>row[j])),q)===Number(i===j),"exact full-root difference inverse");
  return{q,n,D,I,indices,A:records.flatMap(r=>[r.first,r.second]),y:records.flatMap(r=>r.outcome)};
}
function closure(lift,q){
  const nodes=lift.nodes,seen=new Map(),stencils=[...lift.linear_moment_stencils];
  const difference=p=>nodes[p[0]].frequency.map((x,j)=>mod(x-nodes[p[1]].frequency[j],q));
  for(const s of stencils)same(difference(s.left_entry),difference(s.right_entry),"native-valid selected stencil");
  nodes.forEach((u,i)=>nodes.forEach((v,j)=>{const k=key(difference([i,j]));if(seen.has(k))stencils.push({kind:"full_translation",left_entry:seen.get(k),right_entry:[i,j]});else seen.set(k,[i,j]);}));
  return{stencils,stats:{all_moment_entries_checked:nodes.length**2,distinct_frequency_differences:seen.size,full_translation_equalities:nodes.length**2-seen.size}};
}
function partition(lift,q,pairs,w){
  const C=closure(lift,q),p=lift.nodes.map((_,i)=>i);
  function find(i){while(p[i]!==i){p[i]=p[p[i]];i=p[i];}return i;}
  function join(a,b){a=find(a);b=find(b);if(a===b)return false;p[Math.max(a,b)]=Math.min(a,b);return true;}
  pairs.forEach(([i,j])=>join(i,j));let changed=true,passes=0;
  while(changed){changed=false;passes++;for(const s of C.stencils){const[a,b]=s.left_entry,[c,d]=s.right_entry;if(find(a)===find(b))changed=join(c,d)||changed;if(find(c)===find(d))changed=join(a,b)||changed;}}
  const labels=p.map((_,i)=>find(i));same(w.class_labels,labels,"independently saturated orthogonal classes");
  for(const s of C.stencils){const[a,b]=s.left_entry,[c,d]=s.right_entry;check((labels[a]===labels[b])===(labels[c]===labels[d]),"every full/selected equality exact");}
  check(w.matrix_rank_exact===new Set(labels).size&&w.closure_passes===passes&&w.all_diagonal_entries_one===true&&w.all_selected_and_full_translation_constraints_satisfied===true,"exact orthogonal Gram certificate");
  for(const k in C.stats)check(w[k]===C.stats[k],"whole moment closure: "+k);
  return{labels,entries:lift.nodes.length**2};
}
function compile(original,records,b){
  const{q,n,A,y,I,indices}=basis(records,b),L=A.length,nodes=JSON.parse(key(original.nodes)),stencils=JSON.parse(key(original.linear_moment_stencils)),lookup=new Map(nodes.map((x,i)=>[key(x.formal_coefficients),i]));
  const conjugated=new Set(stencils.filter(s=>s.kind==="conjugation").map(s=>s.left_entry[0])),powers=new Map(),native=original.native_target_maps.map(x=>x.native_node);
  function node(raw){const f=raw.map(x=>mod(x,q)),k=key(f);if(!lookup.has(k)){lookup.set(k,nodes.length);nodes.push({formal_coefficients:f,frequency:Array.from({length:n},(_,j)=>mod(dot(f,A.map(row=>row[j])),q)),fake_observed_phase_exponent:mod(dot(f,y),q)});}return lookup.get(k);}
  function negative(i){const j=node(nodes[i].formal_coefficients.map(x=>-x));if(!conjugated.has(i)){stencils.push({kind:"conjugation",left_entry:[i,0],right_entry:[0,j]});conjugated.add(i);}return j;}
  function add(i,j){const k=node(nodes[i].formal_coefficients.map((x,l)=>x+nodes[j].formal_coefficients[l])),neg=negative(j);stencils.push({kind:"addition",left_entry:[k,0],right_entry:[i,neg]});return k;}
  function multiply(i,c){if(c<0){i=negative(i);c=-c;}let total=0,power=i,bit=0;while(c){if(c%2)total=add(total,power);c=Math.floor(c/2);bit++;if(c){const k=key([i,bit]);if(!powers.has(k))powers.set(k,add(power,power));power=powers.get(k);}}return total;}
  const differences=records.map((_,i)=>{const f=Array(L).fill(0);f[2*i]=1;f[2*i+1]=-1;const d=node(f);stencils.push({kind:"pair_difference_anchor",left_entry:[d,0],right_entry:[native[2*i],native[2*i+1]]});return d;});
  const loops=indices.map(i=>({basis_record_index:i,integer_multiplier:q,endpoint:multiply(differences[i],q)}));
  const targets=A.map((row,j)=>{const canonical=I[0].map((_,k)=>mod(dot(row,I.map(r=>r[k])),q)),balanced=canonical.map(c=>2*c<q?c:c-q);let total=0;indices.forEach((i,k)=>{if(balanced[k])total=add(total,multiply(differences[i],balanced[k]));});stencils.push({kind:"observable_native_target",left_entry:[total,0],right_entry:[native[j],0]});return{frequency_row:j,computed_node:total,native_node:native[j],canonical_basis_coefficients:canonical,balanced_basis_coefficients:balanced};});
  return{nodes,linear_moment_stencils:stencils,native_target_maps:original.native_target_maps,loops,targets,differences};
}
same(R.native_controls.map(c=>c.source_seed),[89513,89523,89533],"prespecified real native cohorts");
let oldEntries=0,newEntries=0,compiled=0;
for(const c of R.native_controls){
  const source=base.native_controls.find(x=>x.seed===c.source_seed);check(source,"original source retained");same(c.records,source.native_records,"actual native outcomes and full labels");
  const data=basis(c.records,c.difference_basis),original=source.adaptive_character_lift,native=original.native_target_maps.map(x=>x.native_node),pairs=c.records.map((_,i)=>[native[2*i],native[2*i+1]]);
  same(c.original_native_nodes,native,"complete original native node list");same(c.saturated_native_pairs,pairs,"all native pair equalities");
  const old=partition(original,data.q,pairs,c.partition_witness);oldEntries+=old.entries;
  const anchors=native.map(i=>Number(old.labels[i]===old.labels[0]));same(c.original_native_anchor_moments,anchors,"exact zero anchors");check(anchors.every(x=>x===0)&&c.noncharacter_mixture_falsifier_certified===true,"unit-basis character-mixture contradiction");
  const repair=c.observable_refinement; same(repair.difference_basis,c.difference_basis,"same observable unit basis");const rebuilt=compile(original,c.records,c.difference_basis);
  for(const k of["nodes","linear_moment_stencils","native_target_maps"])same(repair[k],rebuilt[k],"independent observable circuit: "+k);
  same(repair.observable_basis_q_loops,rebuilt.loops,"actual q-loops");check(rebuilt.loops.every(x=>x.endpoint===0),"q-loops close exactly");
  same(repair.observable_native_target_maps,rebuilt.targets,"every native row reconstructed");same(repair.pair_difference_nodes,rebuilt.differences,"measured pair anchors");
  const C=rebuilt.targets.reduce((s,t)=>s+t.balanced_basis_coefficients.reduce((a,x)=>a+x*x,0),0),m=c.records.length,q=data.q;
  check(repair.sum_native_balanced_coefficient_squared_norms===C&&repair.native_anchor_total_deficit_upper_per_basis_pair_deficit===C,"all-rank Gram error coefficient");
  const den=BigInt(Math.max(m*q*q,1+C)),w=frac(1n,den),opt=frac(BigInt(m)*den-2n*BigInt(m),den),gap=frac(2n*BigInt(m),den);
  check(repair.weighted_separating_score_anchor_weight===w&&repair.weighted_diagnostic_repaired_all_rank_optimum===opt&&repair.weighted_diagnostic_integrality_gap_before_repair===gap,"rational separating score and all-rank repair");
  const betas=rebuilt.targets.map(t=>6*t.balanced_basis_coefficients.reduce((s,x)=>s+Math.abs(x),0)+1),E=betas.reduce((s,x)=>s+x*x,0);
  same(repair.per_native_target_stencil_residual_error_constants,betas,"conjugation/addition/target residual propagation");
  check(repair.sum_stencil_residual_error_constant_squares===E&&repair.weighted_objective_excess_upper_per_max_complex_stencil_residual===frac(BigInt(E),den-BigInt(C))&&repair.max_stencil_residual_for_half_diagnostic_gap===frac(BigInt(m)*(den-BigInt(C)),den*BigInt(E))&&repair.residual_bound_requires_exact_PSD_and_unit_diagonal===true,"conditional rational numerical precision gate");
  const diag=c.weighted_diagnostic;check(diag.pair_weight==="1"&&diag.native_anchor_penalty===w&&diag.partition_PSD_score===String(m)&&diag.true_character_maximum===opt&&diag.exact_integrality_gap===gap&&diag.maximum_requires_no_secret_enumeration===true&&diag.is_native_noisy_likelihood_objective===false,"diagnostic is not native noisy likelihood");same(diag.true_maximum_attained_at_secret,Array(data.n).fill(0),"zero character attains exact optimum");
  const closed=closure(repair,q);same(repair.complete_moment_closure,closed.stats,"complete refined moment counts");
  check(repair.matrix_dimension===rebuilt.nodes.length&&repair.dense_PSD_complex_entries===rebuilt.nodes.length**2,"polynomial dense matrix charged");
  const next=partition(repair,q,pairs,c.saturated_repaired_partition);newEntries+=next.entries;check(native.every(i=>next.labels[i]===next.labels[0]),"repair forces every saturated native anchor at all ranks");
  check(repair.observable_saturation_bound_certified===true&&repair.every_exact_saturated_basis_pair_forces_shared_character_native_anchors===true&&repair.all_rank_repair_applies_to_weighted_diagnostic_not_native_noisy_likelihood===true&&repair.noisy_recovery_or_general_convex_tightness_proved===false,"repair scope");
  check(c.hidden_secret_or_outcomes_used_to_select_falsifier_or_circuit===false&&c.external_original_source_supply_physically_certified===false&&c.pointwise_representation_failure_is_random_source_decoder_failure===false,"access and source scope");compiled+=rebuilt.linear_moment_stencils.length;
}
check(R.status==="NATIVE_FULL_MOMENT_FALSIFIER_AND_OBSERVABLE_REPAIR_REVIEW_PENDING"&&R.general_sparse_Bochner_convex_hull_equality_falsified_on_retained_sources===true&&R.weighted_diagnostic_repaired_at_every_PSD_rank===true,"honest research status");
for(const k of["full_group_or_secret_enumeration_used","native_noisy_likelihood_tightness_or_decoder_proved","quantum_speedup_proved","candidate_record_accepted"])check(R[k]===false,"unsupported research claim: "+k);
console.log(JSON.stringify({status:"PASS",original_full_moment_entries:oldEntries,repaired_full_moment_entries:newEntries,recompiled_observable_stencils:compiled,native_noisy_decoder_supplied:false,external_IID_supply_certified:false}));
