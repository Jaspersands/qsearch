"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,same,rat,zero,one,add,sub,mul,div,str,parse,cmp}=require("./cyclotomic_exact.js");
const root=path.join(__dirname,"../.."),R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(root,"research/phase_workbench/ternary_soft_fiber_cooling.json"),"utf8"));
const key=JSON.stringify,mod=(x,q)=>(x%q+q)%q,eq=(a,b)=>cmp(a,b)===0n;
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
check(R.derivation_sha256===hash(path.join(root,"research/TERNARY_SOFT_FIBER_COOLING.md")),"pinned soft-fiber derivation");
for(const flag of["quantum_hardware_gate_export_supplied","efficient_fiber_eraser_supplied","arbitrary_quantum_receiver_lower_bound","quantum_speedup_proved","candidate_record_accepted","novelty_claim"])check(R[flag]===false,"unsupported cooling claim: "+flag);
function cube(q,n){let a=[[]];for(let i=0;i<n;i++)a=a.flatMap(w=>Array.from({length:q},(_,j)=>[...w,j]));return a;}
function combos(n,k){const a=[];function rec(w,start){if(w.length===k){a.push(w);return;}for(let i=start;i<n;i++)rec([...w,i],i+1);}rec([],0);return a;}
function choose(n,k){let v=1n;for(let j=0;j<k;j++)v=v*BigInt(n-j)/BigInt(j+1);return v;}
function squared(a){return mul(a,a);}
function sum(a){return a.reduce(add,zero);}
function chart(level){let V=[[1n,0n],[0n,1n]],pi=[[-1n,-1n],[1n,-2n]];for(let j=0;j<level-1;j++)V=V.map(row=>pi[0].map((_,i)=>row.reduce((s,a,k)=>s+a*pi[k][i],0n)));const q=3n**BigInt(level/2),den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]),a=q*(2n*V[1][1]+V[1][0]),b=q*(-2n*V[0][1]-V[0][0]);check(a%den===0n&&b%den===0n,"exact original native frequency chart");const u=a/den,v=b/den;return label=>{const[x,y]=label.map(BigInt);return[Number((u*x+v*y)%q+q)%Number(q),Number(((u+v)*x-u*y)%q+q)%Number(q)];};}
const source=R.native_source,n=source.dimension,q=source.modulus,M=source.source_inputs;
check(n===2&&q===9&&M===5&&source.native_level===4&&source.seed===89881&&source.seed_is_population_scaling_evidence===false,"same preregistered native source, not population scaling evidence");
const at=chart(source.native_level),F=source.original_ring_labels.map(row=>{const pairs=row.map(at);return[pairs.map(p=>p[0]),pairs.map(p=>p[1])];});
same(F,source.native_frequencies,"public frequencies derived from original ring labels");
const W=cube(3,M),D=W.length,V=W.map(w=>Array.from({length:n},(_,j)=>mod(w.reduce((s,x,i)=>s+(x===0?0:F[i][x-1][j]),0),q))),counts=new Map();
for(const y of V)counts.set(key(y),(counts.get(key(y))||0)+1);
const purity=rat(BigInt([...counts.values()].reduce((a,c)=>a+c*c,0)),BigInt(D*D));
check(R.source_collision_purity_exact===str(purity),"original Born-weighted collision purity");
let parentRows=0,localClasses=0;
function residual(S,r,t){if(r===0||r===S)return zero;return div(mul(rat(BigInt(r*(S-r))),squared(sub(one,t))),add(rat(BigInt(r)),mul(rat(BigInt(S-r)),squared(t))));}
function reference(ref){
  const k=ref.support,t=parse(ref.attenuation),B=combos(M,k),S=3**k;
  check(eq(t,zero)||cmp(t,zero)>0n&&cmp(t,one)<=0n,"admitted exact attenuation");
  same(W,ref.complete_words,"complete original word cube");same(V,ref.full_frequency_values,"actual full-root frequencies, not a reduced prefix");
  const marked=V.map((y,i)=>key(y)===key(ref.target_frequency)?i:-1).filter(i=>i>=0),markedSet=new Set(marked);
  same(marked,ref.marked_word_indices,"occupied complete target fiber");check(marked.length>0,"nonempty target for cooling");
  const p=rat(BigInt(marked.length),BigInt(D)),rows=W.map(()=>new Map()),blockCertificates=[];let mean=zero;
  B.forEach(block=>{
    const other=Array.from({length:M},(_,i)=>i).filter(i=>!block.includes(i)),groups=new Map();
    W.forEach((w,i)=>{const tag=key(other.map(j=>w[j]));if(!groups.has(tag))groups.set(tag,[]);groups.get(tag).push(i);});
    const classCounts=[];let norm=zero;
    for(const indices of groups.values()){
      const r=indices.filter(i=>markedSet.has(i)).length;
      const a=indices.map(i=>r===0||markedSet.has(i)?one:t),Z=sum(a.map(squared));check(cmp(Z,zero)>0n,"unmarked zero-temperature class retains continuous limit");
      classCounts.push(r);const part=div(residual(S,r,t),rat(BigInt(D)));norm=add(norm,part);
      indices.forEach((i,l)=>{rows[i].set(i,add(rows[i].get(i)||zero,rat(1n,BigInt(B.length))));indices.forEach((j,h)=>{
        const weight=div(mul(a[l],a[h]),mul(Z,rat(BigInt(B.length))));rows[i].set(j,sub(rows[i].get(j)||zero,weight));});});
      check(cmp(residual(S,r,t),rat(BigInt(r*(S-1))))<=0n,"exact local uniform residual bound, including r>1");localClasses++;
    }
    blockCertificates.push({block,conditional_marked_counts:classCounts,H_block_uniform_residual_squared_exact:str(norm)});mean=add(mean,div(norm,rat(BigInt(B.length))));
  });
  same(blockCertificates,ref.local_block_certificates,"every outside class and local residual recomputed");
  rows.forEach((row,i)=>{const encoded=[...row].filter(([,a])=>!eq(a,zero)).sort((a,b)=>a[0]-b[0]).map(([j,a])=>[j,str(a)]);same(encoded,ref.parent_rows[i],"every rational local Gibbs parent entry");for(const[j,a]of row)check(eq(a,rows[j].get(i)||zero),"Hermitian parent");parentRows++;});
  const hu=rows.map(row=>sum([...row.values()])),norm=div(sum(hu.map(squared)),rat(BigInt(D))),upper=mul(p,rat(BigInt(S-1)));
  check(ref.fiber_density===str(p)&&ref.parent_uniform_residual_squared_exact===str(norm)&&ref.mean_local_uniform_residual_squared_exact===str(mean)&&ref.uniform_residual_squared_upper===str(upper)&&cmp(norm,mean)<=0n&&cmp(mean,upper)<=0n,"state-specific exact norm and Jensen bound");
  const g=W.map((_,i)=>markedSet.has(i)?one:t);for(const row of rows)check(eq(sum([...row].map(([j,a])=>mul(a,g[j]))),zero),"coherent Gibbs ground vector retained");
  const Z=add(rat(BigInt(marked.length)),mul(rat(BigInt(D-marked.length)),squared(t)));
  check(ref.coherent_Gibbs_normalizer_squared===str(Z)&&ref.coherent_Gibbs_fiber_probability_exact===str(div(rat(BigInt(marked.length)),Z)),"complete raw Gibbs normalization");
  check(ref.reference_work_upper===String(BigInt(D)*choose(M,k)*BigInt(S))&&ref.reference_enumerates_complete_native_word_cube===true&&ref.reference_is_scalable_compiler===false,"complete exponential reference cost, not free preparation");
}
function action(c,mass,scope){
  check(c.density_or_collision_purity===str(mass)&&c.weighting_scope===scope,"one-target density versus source-weighted purity");
  const k=c.maximum_block_support,S=3n**BigInt(k),r=parse(c.sqrt_local_class_minus_one_upper),bits=c.sqrt_interval_bits,A=parse(c.parent_action),L=parse(c.marked_projector_action),scale=1n<<BigInt(bits);
  check(r[1]>0n&&cmp(r,zero)>=0n&&cmp(squared(r),rat(S-1n))>=0n&&cmp(squared(sub(r,rat(1n,scale))),rat(S-1n))<0n,"tight directed rational square-root upper");
  check(cmp(A,zero)>=0n&&cmp(L,zero)>=0n,"absolute integrated action");
  const raw=mul(mass,squared(add(add(one,mul(A,r)),L))),bound=cmp(raw,one)<0n?raw:one;
  check(c.raw_fiber_success_upper===str(bound),"raw action success ceiling, no conditioned branch");
  for(const flag of["bound_applies_to_temperature_and_block_policies_depending_on_full_labels_and_target","arbitrary_signed_and_nonmonotone_parent_schedules_covered","projection_or_postselection_is_not_free_parent_evolution","starting_state_is_uniform_native_word_superposition"])check(c[flag]===true,"parent action scope: "+flag);
  check(c.arbitrary_quantum_receiver_lower_bound===false,"not an all-receiver lower bound");return bound;
}
same(R.exact_parent_controls.map(c=>[c.support,c.attenuation]),[[1,"1"],[1,"1/3"],[1,"1/27"],[1,"0"],[2,"1/3"]],"fixed finite cooling controls");
R.exact_parent_controls.forEach(reference);
for(const trial of R.finite_dynamics_controls){
  check(trial.numeric_simulation_is_asymptotic_or_rigorous_roundoff_certificate===false,"finite expm is explicitly numerical, not certified asymptotics");
  check(trial.schedule.length===trial.exact_parent_references.length,"every evolution segment has an exact parent");let A=zero,L=zero,k=0;
  trial.schedule.forEach((s,i)=>{const ref=trial.exact_parent_references[i];reference(ref);check(s.support===ref.support&&s.attenuation===ref.attenuation,"correct schedule parent");const d=parse(s.duration),g=parse(s.coefficient||"1"),m=parse(s.marker_coefficient||"0"),abs=a=>cmp(a,zero)<0n?sub(zero,a):a;check(cmp(d,zero)>=0n,"nonnegative time; reversed evolution uses signed coefficient");A=add(A,mul(d,abs(g)));L=add(L,mul(d,abs(m)));k=Math.max(k,s.support);});
  const c=trial.action_certificate;check(c.parent_action===str(A)&&c.marked_projector_action===str(L)&&c.maximum_block_support===k,"all signed/marker action charged");
  const bound=action(c,parse(trial.exact_parent_references[0].fiber_density),"one_target_density");
  const value=Number(bound[0])/Number(bound[1]);check(trial.raw_fiber_success_numeric>=0&&trial.raw_fiber_success_numeric<=value+1e-10,"reported numerical dynamics respect bound");
}
action(R.source_weighted_action_control,purity,"original_source_Born_weighted_collision_purity");
let total=0,mean=zero;
for(const flat of cube(3,4)){const C=[0,0,0];for(const w of cube(3,2))C[mod((w[0]===0?0:flat[w[0]-1])+(w[1]===0?0:flat[2+w[1]-1]),3)]++;mean=add(mean,rat(BigInt(C.reduce((a,c)=>a+c*c,0)),81n));total++;}
mean=div(mean,rat(BigInt(total)));same(R.complete_native_label_population_control,{dimension:1,modulus:3,source_inputs:2,entire_IID_label_matrices_checked:total,mean_collision_purity_exact:str(mean)},"complete native IID label purity census");check(eq(mean,rat(11n,27n)),"exact expected purity at finite census");
for(const row of R.population_scaling_ledgers){const G=BigInt(row.modulus)**BigInt(row.dimension),D=3n**BigInt(row.source_inputs),K=add(rat(1n,G),rat(G-1n,G*D));check(row.native_word_dimension===String(D)&&row.full_frequency_group===String(G)&&row.expected_source_collision_purity_exact===str(K),"all-word pair law, no independent-edge fiction");const upper=action(row.action_bound,K,"original_source_Born_weighted_collision_purity");check(row.source_weighted_fiber_erasure_squared_error_lower===str(sub(one,upper)),"necessary clean erasure error, not a sufficient certificate");for(const flag of["requires_all_IID_uniform_full_native_frequency_rows","target_frequency_drawn_with_original_Born_weight","uniform_per_instance_action_cap_required","uses_no_small_collision_or_gap_premise"])check(row[flag]===true,"population action scope: "+flag);check(row.efficient_fiber_eraser_supplied===false,"no compiler invented");}
const positive=R.global_block_positive_control;check(positive.all_words_enumerated===D&&positive.support===M&&positive.full_table_preparation_is_charged_exponential===true&&positive.positive_control_refutes_general_Hamiltonian_lower_bound===true,"global-block escape has exponential conditional table");
check(positive.target_vector_error_numeric<1e-12&&Math.abs(positive.parent_action_numeric-Math.PI)<1e-14,"numerical bisector positive control");
console.log(JSON.stringify({status:"PASS",exact_parent_rows:parentRows,complete_conditional_classes:localClasses,entire_IID_label_matrices:total,efficient_fiber_eraser_supplied:false}));
