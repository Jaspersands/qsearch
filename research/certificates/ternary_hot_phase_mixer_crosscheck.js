"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,same,rat,zero,one,add,sub,mul,div,str,parse,cmp}=require("./cyclotomic_exact.js");
const root=path.join(__dirname,"../.."),R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(root,"research/phase_workbench/ternary_hot_phase_mixer.json"),"utf8"));
const key=JSON.stringify,mod=(a,q)=>(a%q+q)%q,sum=a=>a.reduce(add,zero),square=a=>mul(a,a),pow=(a,n)=>rat(a[0]**BigInt(n),a[1]**BigInt(n));
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
check(R.derivation_sha256===hash(path.join(root,"research/TERNARY_HOT_PHASE_MIXER.md")),"pinned hot-stage derivation");
for(const flag of["arbitrary_quantum_receiver_lower_bound","efficient_clean_fiber_preparation_supplied","quantum_speedup_proved","candidate_record_accepted","novelty_claim"])check(R[flag]===false,"unsupported hot-stage claim: "+flag);
check(R.multiple_layers_are_not_excluded===true&&R.finite_menu_selection_uses_charged_classical_statevector_enumeration===true,"multiple layers are open; menu scoring is charged enumeration");
function cube(q,n){let out=[[]];for(let i=0;i<n;i++)out=out.flatMap(w=>Array.from({length:q},(_,j)=>[...w,j]));return out;}
function chart(level){let V=[[1n,0n],[0n,1n]],pi=[[-1n,-1n],[1n,-2n]];for(let j=0;j<level-1;j++)V=V.map(row=>pi[0].map((_,i)=>row.reduce((s,a,k)=>s+a*pi[k][i],0n)));const q=3n**BigInt(level/2),den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]),a=q*(2n*V[1][1]+V[1][0]),b=q*(-2n*V[0][1]-V[0][0]);check(a%den===0n&&b%den===0n,"native chart integrality");const u=a/den,v=b/den;return label=>{const[x,y]=label.map(BigInt);return[Number((u*x+v*y)%q+q)%Number(q),Number(((u+v)*x-u*y)%q+q)%Number(q)];};}
const source=R.native_source,n=source.dimension,q=source.modulus,M=source.source_inputs,at=chart(source.native_level),F=source.original_ring_labels.map(row=>{const p=row.map(at);return[p.map(x=>x[0]),p.map(x=>x[1])];});
check(n===2&&q===9&&M===5&&source.native_level===4&&source.seed===89881,"actual prespecified full-root native cohort");same(F,source.native_frequencies,"original ring chart produces full frequencies");
const W=cube(3,M),D=W.length,V=W.map(w=>Array.from({length:n},(_,j)=>mod(w.reduce((a,t,i)=>a+(t===0?0:F[i][t-1][j]),0),q)));
const ca=(a,b)=>[a[0]+b[0],a[1]+b[1]],cm=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],scale=(a,c)=>a.map(v=>v*c),norm=a=>a[0]*a[0]+a[1]*a[1],cis=a=>[Math.cos(a),Math.sin(a)];
const close=(a,b,msg)=>check(Math.abs(a-b)<2e-12,msg);
let amplitudesChecked=0;
function numericReference(ref,words,values,target){
  const width=words[0].length,D=words.length,E=values.map(v=>v.reduce((a,x,j)=>a+Number(x!==target[j]),0)),lookup=new Map(words.map((w,i)=>[key(w),i]));
  same(words,ref.complete_words,"complete actual word reference");same(E,ref.complete_residual_energies,"full-root cost energies");
  let state=words.map(()=>[1/Math.sqrt(D),0]);
  for(const[gamma,beta]of ref.layers){state=state.map((a,i)=>cm(a,cis(-gamma*E[i])));const phase=cis(-beta),off=scale(ca([1,0],scale(phase,-1)),1/3);for(let axis=0;axis<width;axis++){const out=[];words.forEach(word=>{let z=[0,0];for(let j=0;j<3;j++){const previous=word.slice();previous[axis]=j;const gate=j===word[axis]?ca(phase,off):off;z=ca(z,cm(gate,state[lookup.get(key(previous))]));}out.push(z);});state=out;}}
  check(ref.state_amplitudes_numeric.length===D,"whole final amplitude vector");state.forEach((a,i)=>{close(a[0],ref.state_amplitudes_numeric[i][0],"independent actual mixer real amplitude");close(a[1],ref.state_amplitudes_numeric[i][1],"independent actual mixer imaginary amplitude");amplitudesChecked++;});
  const marked=E.map((e,i)=>e===0?i:-1).filter(i=>i>=0),success=marked.reduce((a,i)=>a+norm(state[i]),0),vector=marked.reduce((a,i)=>ca(a,state[i]),[0,0]),coherent=marked.length?norm(vector)/marked.length:0,p=rat(BigInt(marked.length),BigInt(D));
  same(marked,ref.marked_word_indices,"complete target membership");close(state.reduce((a,z)=>a+norm(z),0),1,"unitary normalization");close(success,ref.raw_fiber_membership_probability_numeric,"raw success, not a herald score");close(coherent,ref.normalized_uniform_fiber_overlap_squared_numeric,"coherent uniform-fiber overlap separately audited");
  const grover=mul(p,square(sub(rat(3n),mul(rat(4n),p))));
  check(ref.classical_uniform_word_rejection_probability_exact===str(p)&&ref.Grover_one_marked_reflection_probability_exact===str(grover),"matched classical rejection and existing Grover baselines");
  check(ref.classical_reference_word_enumerations_charged===D&&ref.numeric_reference_is_scalable_compiler_or_exact_roundoff_certificate===false&&ref.fiber_membership_is_not_clean_uniform_fiber_erasure===true,"finite simulation not a clean eraser or compiled optimizer");
}
check(R.one_layer_public_angle_menu.length===16,"complete committed finite angle menu");R.one_layer_public_angle_menu.forEach(ref=>{check(ref.layers.length===1,"one-layer menu only");numericReference(ref,W,V,ref.target_frequency);});
numericReference(R.best_public_finite_menu_trial,W,V,R.best_public_finite_menu_trial.target_frequency);
close(R.best_public_finite_menu_trial.raw_fiber_membership_probability_numeric,Math.max(...R.one_layer_public_angle_menu.map(r=>r.raw_fiber_membership_probability_numeric)),"actual public finite menu winner");
check(R.two_layer_open_scope_control.layers.length===2,"two-layer scope control retained");numericReference(R.two_layer_open_scope_control,W,V,R.two_layer_open_scope_control.target_frequency);
numericReference(R.native_field_root_positive_control,cube(3,1),[[0],[1],[2]],[1]);close(R.native_field_root_positive_control.raw_fiber_membership_probability_numeric,1,"known linear native field-root positive escape");
let labelsChecked=0,targetCases=0;
for(const c of R.exact_native_population_censuses){const q=c.modulus,M=c.source_inputs,D=3**M,W=cube(3,M);let uniform=zero,born=zero,total=0;
  for(const flat of cube(q,2*M)){const V=W.map(w=>mod(w.reduce((s,t,i)=>s+(t===0?0:flat[2*i+t-1]),0),q));for(let y=0;y<q;y++){let a=V.map(v=>rat(v===y?1n:-1n));for(let axis=0;axis<M;axis++){a=W.map(word=>{let value=zero;for(let j=0;j<3;j++){const previous=word.slice();previous[axis]=j;const index=previous.reduce((a,t)=>a*3+t,0),gate=sub(rat(2n,3n),rat(j===word[axis]?1n:0n));value=add(value,mul(gate,a[index]));}return value;});}const marked=V.map((v,i)=>v===y?i:-1).filter(i=>i>=0),p=div(sum(marked.map(i=>square(a[i]))),rat(BigInt(D)));uniform=add(uniform,div(p,rat(BigInt(q))));born=add(born,mul(p,rat(BigInt(marked.length),BigInt(D))));}total++;}
  uniform=div(uniform,rat(BigInt(total)));born=div(born,rat(BigInt(total)));const eta=rat(BigInt(2-q),BigInt(q)),diag=pow(rat(-1n,3n),M),formula=div(add(square(add(eta,mul(sub(one,eta),diag))),mul(sub(one,square(eta)),sub(one,square(diag)))),rat(BigInt(q)));
  check(c.entire_native_label_matrices===total&&c.all_uniform_target_cases===total*q&&c.uniform_target_mean_success_exact===str(uniform)&&c.Born_target_mean_success_exact===str(born)&&cmp(uniform,formula)===0n,"complete native census and exact one-layer moment formula");
  const p=c.one_layer_prediction;check(p.dimension===1&&p.modulus===String(q)&&p.source_inputs===M&&p.phase_mean_exact===str(eta)&&p.mixer_diagonal_exact===str(diag)&&p.uniform_target_population_success_exact===str(formula)&&p.phase_angle==="pi"&&p.mixer_angle==="pi"&&p.target_is_uniform_full_frequency_not_Born_weighted===true,"uniform target differs from native Born weighting");labelsChecked+=total;targetCases+=total*q;
}
function isqrt(a){if(a<2n)return a;let x=1n<<BigInt(Math.ceil(a.toString(2).length/2));for(;;){const y=(x+a/x)/2n;if(y>=x)return x;x=y;}}
function rootUpper(a){const scale=1n<<80n,v=a[0]*a[1]*scale*scale,r=isqrt(v);return rat(r*r===v?r:r+1n,scale*a[1]);}
for(const c of R.five_word_torsion_controls){
  const q=c.modulus,B=Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>Number(i!==j)));let value=0n,quarterReal=0n,quarterImag=0n;
  for(const a of cube(q,4)){const total=a.reduce((s,x)=>s+x,0),marked=a.map(x=>Number(mod(total-x,q)!==0)),nonzero=marked.reduce((a,b)=>a+b,0);value+=nonzero%2?-1n:1n;const phase=mod(marked[2]+marked[3]-marked[0]-marked[1],4);quarterReal+=[1n,0n,-1n,0n][phase];quarterImag+=[0n,1n,0n,-1n][phase];}
  const actual=rat(value,BigInt(q)**4n),eta=rat(BigInt(2-q),BigInt(q)),b=rat(2n,BigInt(q)),predicted=add(pow(eta,4),mul(rat(2n),pow(b,4)));
  same(c.base_original_word,[0,0,0,0],"actual original native base");same(c.other_original_words,B,"four weight-three native words");same(c.pointed_first_row_coefficient_matrix,B,"native J-I coefficient matrix");
  check(c.pointed_matrix_determinant===-3&&c.independent_IID_first_row_assignments_checked===q**4&&c.actual_four_phase_pi_moment_exact===str(actual)&&cmp(actual,predicted)===0n&&c.false_full_independence_prediction_exact===str(pow(eta,4)),"complete native five-word torsion correlation, not independent phases");
  const normA=rat(BigInt(1+(q-1)**2),BigInt(q*q)),normB=rat(2n,BigInt(q*q)),quarter=add(square(normA),mul(rat(2n),square(normB)));
  check(quarterImag===0n&&c.mixed_quarter_phase_imaginary_part_exact==="0"&&c.mixed_quarter_phase_moment_exact===str(quarter)&&cmp(quarter,rat(quarterReal,BigInt(q)**4n))===0n&&c.false_independent_mixed_quarter_phase_prediction_exact===str(square(normA)),"independent genuinely complex mixed-sign path moment");
  const kernel=cube(q,4).filter(v=>v.every((x,j)=>mod(v.reduce((s,a)=>s+a,0)-x,q)===0));same(kernel,[0,1,2].map(k=>Array(4).fill(k*q/3)),"full-root annihilator is precisely three characters, not four IID frequencies");
  check(c.unused_second_native_rows_integrated_out_not_assumed_fixed_in_population===true&&c.kernel_characters_are_uniform_all_four_coordinates_at_multiples_of_q_over_three===true&&c.correlation_is_an_executed_two_layer_advantage===false,"correlation does not by itself supply an interference algorithm");
}
for(const c of R.one_layer_adaptive_scaling_ledgers){const n=c.dimension,q=BigInt(c.modulus),M=c.source_inputs,G=q**BigInt(n),D=3n**BigInt(M),m=BigInt(c.implicit_angle_net_points_per_axis);check((m-1n)**3n<G&&m**3n>=G&&c.implicit_angle_net_points_total===String(m*m),"implicit exact cube-root net cardinality");const error=rat(BigInt(44*(n+M)),7n*m),raw=add(rat(9n*m*m,G),error),uniform=cmp(raw,one)<0n?raw:one,b=add(uniform,rootUpper(mul(rat(G-1n,D),uniform))),born=cmp(b,one)<0n?b:one;
  check(c.native_word_dimension===String(D)&&c.full_frequency_group===String(G)&&c.one_fixed_angle_pair_uniform_population_success_upper===str(G>9n?rat(9n,G):one)&&c.probability_discretization_error_upper===str(error)&&c.best_label_and_target_adaptive_angles_uniform_population_success_upper===str(uniform)&&c.best_label_and_target_adaptive_angles_Born_population_success_upper===str(born),"public continuous angle net and Born-weight correction");
  for(const flag of["net_is_mathematical_certificate_not_executed_optimizer","labels_and_target_may_select_continuous_angles","mixer_form_and_one_layer_template_fixed","multiple_layers_or_label_adaptive_mixer_shapes_are_not_covered"])check(c[flag]===true,"one-layer net scope: "+flag);check(c.arbitrary_quantum_receiver_lower_bound===false,"no generic hot receiver impossibility");
}
console.log(JSON.stringify({status:"PASS",numeric_amplitudes_replayed:amplitudesChecked,entire_IID_label_matrices:labelsChecked,exact_uniform_target_cases:targetCases,multiple_layers_excluded:false}));
