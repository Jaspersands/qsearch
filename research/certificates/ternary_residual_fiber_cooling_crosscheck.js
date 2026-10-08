"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,same,rat,zero,one,add,sub,mul,div,str,parse,cmp}=require("./cyclotomic_exact.js");
const root=path.join(__dirname,"../.."),R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(root,"research/phase_workbench/ternary_residual_fiber_cooling.json"),"utf8"));
const key=JSON.stringify,eq=(a,b)=>cmp(a,b)===0n,mod=(a,q)=>(a%q+q)%q;
const sum=a=>a.reduce(add,zero),square=a=>mul(a,a),power=(a,n)=>rat(a[0]**BigInt(n),a[1]**BigInt(n)),abs=a=>cmp(a,zero)<0n?sub(zero,a):a;
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
check(R.derivation_sha256===hash(path.join(root,"research/TERNARY_RESIDUAL_FIBER_COOLING.md")),"pinned residual-cooling derivation");
for(const flag of["arbitrary_quantum_or_hot_schedule_lower_bound","efficient_fiber_eraser_supplied","quantum_speedup_proved","candidate_record_accepted","novelty_claim"])check(R[flag]===false,"unsupported residual-cooling claim: "+flag);
check(R.hot_temperature_excursions_are_not_excluded===true,"cold bound does not cover hot excursions");
function cube(q,n){let out=[[]];for(let i=0;i<n;i++)out=out.flatMap(w=>Array.from({length:q},(_,j)=>[...w,j]));return out;}
function combos(n,k){const out=[];function rec(w,start){if(w.length===k){out.push(w);return;}for(let i=start;i<n;i++)rec([...w,i],i+1);}rec([],0);return out;}
function choose(n,k){let a=1n;for(let j=0;j<k;j++)a=a*BigInt(n-j)/BigInt(j+1);return a;}
function isqrt(a){if(a<2n)return a;let x=1n<<BigInt(Math.ceil(a.toString(2).length/2));for(;;){const y=(x+a/x)/2n;if(y>=x)return x;x=y;}}
function rootUpper(a,bits=80){const scale=1n<<BigInt(bits),v=a[0]*a[1]*scale*scale,b=isqrt(v),ceil=b*b===v?b:b+1n;return rat(ceil,scale*a[1]);}
function chart(level){let V=[[1n,0n],[0n,1n]],pi=[[-1n,-1n],[1n,-2n]];for(let j=0;j<level-1;j++)V=V.map(row=>pi[0].map((_,i)=>row.reduce((s,a,k)=>s+a*pi[k][i],0n)));const q=3n**BigInt(level/2),den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]),a=q*(2n*V[1][1]+V[1][0]),b=q*(-2n*V[0][1]-V[0][0]);check(a%den===0n&&b%den===0n,"exact native chart");const u=a/den,v=b/den;return label=>{const[x,y]=label.map(BigInt);return[Number((u*x+v*y)%q+q)%Number(q),Number(((u+v)*x-u*y)%q+q)%Number(q)];};}
const s=R.native_source,n=s.dimension,q=s.modulus,M=s.source_inputs;
check(n===2&&q===9&&M===5&&s.native_level===4&&s.seed===89881,"prespecified actual native cohort");
const at=chart(s.native_level),F=s.original_ring_labels.map(row=>{const pairs=row.map(at);return[pairs.map(p=>p[0]),pairs.map(p=>p[1])];});same(F,s.native_frequencies,"actual full-root chart from original labels");
const W=cube(3,M),D=W.length,V=W.map(w=>Array.from({length:n},(_,j)=>mod(w.reduce((a,t,i)=>a+(t===0?0:F[i][t-1][j]),0),q)));
let rowsChecked=0,classesChecked=0,largestCross=zero;
same(R.exact_parent_controls.map(c=>[c.support,c.attenuation]),[[1,"1/2"],[1,"1/4"]],"cold controls, not an uncharged hot path");
for(const ref of R.exact_parent_controls){
  const k=ref.support,t=parse(ref.attenuation),B=combos(M,k),E=V.map(y=>y.reduce((a,v,j)=>a+Number(v!==ref.target_frequency[j]),0)),marked=E.map((e,i)=>e===0?i:-1).filter(i=>i>=0),set=new Set(marked);
  same(W,ref.complete_words,"whole native word cube");same(E,ref.complete_residual_energies,"actual coordinate residual energies");same(marked,ref.marked_word_indices,"complete target fiber");
  const rows=W.map(()=>new Map());
  B.forEach(block=>{const other=Array.from({length:M},(_,i)=>i).filter(i=>!block.includes(i)),groups=new Map();W.forEach((w,i)=>{const tag=key(other.map(j=>w[j]));if(!groups.has(tag))groups.set(tag,[]);groups.get(tag).push(i);});
    for(const indices of groups.values()){const a=indices.map(i=>power(t,E[i])),Z=sum(a.map(square));check(cmp(Z,zero)>0n,"finite residual temperature avoids zero normalizers");indices.forEach((i,l)=>{rows[i].set(i,add(rows[i].get(i)||zero,rat(1n,BigInt(B.length))));indices.forEach((j,h)=>{const v=div(mul(a[l],a[h]),mul(Z,rat(BigInt(B.length))));rows[i].set(j,sub(rows[i].get(j)||zero,v));});});classesChecked++;}});
  rows.forEach((row,i)=>{same([...row].filter(([,a])=>!eq(a,zero)).sort((a,b)=>a[0]-b[0]).map(([j,a])=>[j,str(a)]),ref.parent_rows[i],"every exact residual parent entry");for(const[j,a]of row)check(eq(a,rows[j].get(i)||zero),"symmetric parent");check(eq(sum([...row].map(([j,a])=>mul(a,power(t,E[j])))),zero),"coherent residual Gibbs null-vector");rowsChecked++;});
  let maxRow=zero,maxCol=zero;for(const i of marked){const v=sum([...rows[i]].filter(([j])=>!set.has(j)).map(([,a])=>abs(a)));if(cmp(v,maxRow)>0n)maxRow=v;}for(let j=0;j<D;j++)if(!set.has(j)){const v=sum(marked.map(i=>abs(rows[i].get(j)||zero)));if(cmp(v,maxCol)>0n)maxCol=v;}
  const cross=mul(maxRow,maxCol);if(cmp(cross,largestCross)>0n)largestCross=cross;
  check(ref.cross_marked_unmarked_max_row_sum_exact===str(maxRow)&&ref.cross_marked_unmarked_max_col_sum_exact===str(maxCol)&&ref.cross_operator_norm_squared_Schur_upper===str(cross),"complete cross-boundary Schur sums");
  const p=div(rat(BigInt(marked.length)),sum(E.map(e=>power(t,2*e))));check(ref.Gibbs_fiber_probability_exact===str(p),"raw Gibbs target probability");
  check(ref.reference_work_upper===String(BigInt(D)*choose(M,k)*3n**BigInt(k))&&ref.reference_is_scalable_preparation===false,"reference costs3^M, not a compiled warm state");
}
const dynamics=R.finite_cold_dynamics,alpha=parse(R.exact_parent_controls[0].Gibbs_fiber_probability_exact),A=rat(2n,5n),raw=square(add(rootUpper(alpha),mul(A,rootUpper(largestCross)))),bound=cmp(raw,one)<0n?raw:one;
check(dynamics.warm_start_attenuation==="1/2"&&dynamics.absolute_parent_action===str(A)&&dynamics.initial_fiber_probability_exact===str(alpha)&&dynamics.cross_operator_norm_squared_upper===str(largestCross)&&dynamics.raw_fiber_success_upper===str(bound),"actual finite cold boundary action ceiling");
check(dynamics.complete_warm_state_granted_not_prepared===true&&dynamics.numeric_control_is_rigorous_roundoff_certificate===false,"given warm state and explicitly numerical dynamics");check(dynamics.raw_fiber_success_numeric>=0&&dynamics.raw_fiber_success_numeric<=Number(bound[0])/Number(bound[1])+1e-10,"numerical evolution obeys exact ceiling");
const byWord=Array.from({length:9},()=>[]),success=[];
for(const flat of cube(3,4)){const values=cube(3,2).map(w=>mod((w[0]===0?0:flat[w[0]-1])+(w[1]===0?0:flat[2+w[1]-1]),3));for(let x=0;x<9;x++){const matches=values.filter(y=>y===values[x]).length,Z=rat(BigInt(matches*4+9-matches),36n),p=rat(BigInt(matches),9n);byWord[x].push(Z);success.push(div(p,Z));}}
const means=byWord.map(a=>div(sum(a),rat(BigInt(a.length)))),variances=byWord.map((a,i)=>div(sum(a.map(v=>square(sub(v,means[i])))),rat(BigInt(a.length))));
same(R.complete_warm_moment_census,{entire_native_label_matrices:81,original_word_targets_per_matrix:9,mean_normalizer_by_fixed_original_word:means.map(str),variance_normalizer_by_fixed_original_word:variances.map(str),source_weighted_mean_warm_fiber_probability_exact:str(div(sum(success),rat(BigInt(success.length))))},"complete original-word target normalizer moments and warm success");
for(const c of R.population_cold_ledgers){
  const w=c.warm_population_moments,b=c.energy_barrier_population,n=w.dimension,q=BigInt(w.modulus),M=w.source_inputs,k=b.maximum_block_support,D=3n**BigInt(M),G=q**BigInt(n),z=rat(1n,4n),mu=power(div(add(one,mul(rat(q-1n),z)),rat(q)),n),mu2=power(div(add(one,mul(rat(q-1n),square(z))),rat(q)),n),mean=add(rat(1n,D),mul(rat(D-1n,D),mu)),variance=mul(rat(D-1n,D*D),sub(mu2,square(mu))),purity=add(rat(1n,G),rat(G-1n,G*D));
  let badZ=div(mul(rat(4n),variance),square(mu));if(cmp(badZ,one)>0n)badZ=one;let a0=add(div(mul(rat(2n),purity),mu),badZ);if(cmp(a0,one)>0n)a0=one;
  check(w.probability_attenuation===str(z)&&w.mean_nonself_weight_exact===str(mu)&&w.second_nonself_weight_exact===str(mu2)&&w.mean_normalizer_exact===str(mean)&&w.normalizer_variance_exact===str(variance)&&w.source_collision_purity_exact_mean===str(purity)&&w.probability_normalizer_below_half_nonself_mean_upper===str(badZ)&&w.source_weighted_warm_fiber_success_upper===str(a0),"pointed-pair IID mean, variance and raw warm mass bound");
  for(const flag of["target_drawn_as_frequency_of_uniform_original_word","distinct_nonself_weights_pairwise_independent_by_pointed_unit_minor","warm_state_preparation_granted_not_implemented"])check(w[flag]===true,"warm law: "+flag);
  let vocabulary=0n;for(let j=1;j<=k;j++)vocabulary+=choose(M,j)*6n**BigInt(j);vocabulary/=2n;const h=Math.floor(n/3),event=mul(rat(vocabulary*2n**BigInt(h)),power(rat(q+1n,2n*q),n)),bad=cmp(event,one)<0n?event:one,sqrtS=rootUpper(rat(3n**BigInt(k)-1n)),coupling=div(sqrtS,rat(2n**BigInt(h+1)));
  check(b.dimension===n&&b.modulus===String(q)&&b.source_inputs===M&&b.difference_signatures===String(vocabulary)&&b.forbidden_residual_weight_at_most===h&&b.minimum_boundary_energy_on_good_labels===h+1&&b.probability_any_small_signature_below_energy_threshold_upper===str(bad)&&b.cross_fiber_parent_operator_norm_upper===str(coupling)&&b.maximum_cold_amplitude_attenuation==="1/2"&&b.sqrt_local_class_minus_one_upper===str(sqrtS)&&b.sqrt_interval_bits===80,"all-signature energy tail and conditional Schur boundary bound");
  check(b.all_labels_and_targets_and_blocks_covered_on_good_event===true&&b.hotter_excursions_are_outside_scope===true,"cold good-event scope");
  const action=parse(c.absolute_integrated_parent_action),sqrtWarm=rootUpper(a0),raw=add(bad,square(add(sqrtWarm,mul(action,coupling)))),result=cmp(raw,one)<0n?raw:one;check(c.warm_fiber_probability_sqrt_upper===str(sqrtWarm)&&c.source_weighted_cold_raw_fiber_success_upper===str(result),"complete bad-label plus cold-action population ceiling");
  for(const flag of["arbitrary_diagonal_controls_covered","uniform_per_instance_absolute_action_cap_required","requires_all_IID_uniform_full_native_frequency_rows","signed_nonmonotone_schedules_with_attenuation_at_most_half_covered","bad_labels_charged_without_conditioned_normalization"])check(c[flag]===true,"cold action scope: "+flag);check(c.arbitrary_quantum_or_hot_schedule_lower_bound===false&&c.efficient_fiber_eraser_supplied===false,"no general receiver impossibility or supplied eraser");
}
console.log(JSON.stringify({status:"PASS",exact_parent_rows:rowsChecked,complete_conditional_classes:classesChecked,entire_IID_label_matrices:81,original_word_target_moment_cases:729,hot_schedule_excluded:false}));
