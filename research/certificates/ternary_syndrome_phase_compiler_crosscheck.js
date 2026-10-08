"use strict";
// Exact native-source, phase and risk checks; no efficient decoder is inferred.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const report=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../phase_workbench/ternary_syndrome_phase_compiler.json"),"utf8"));
function check(x,m){if(!x)throw Error(m);}
const same=(a,b,m)=>check(JSON.stringify(a)===JSON.stringify(b),m),mod=(x,q)=>(x%q+q)%q;
function I(x){check(typeof x==="string"&&/^(0|[1-9][0-9]*)$/.test(x),"canonical nonnegative integer string");return BigInt(x);}
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
function fraction(a,b){a=BigInt(a);b=BigInt(b);check(a>=0n&&b>0n,"nonnegative fraction");const g=gcd(a,b);a/=g;b/=g;return b===1n?String(a):a+"/"+b;}
function pow(a,e,q){let v=1n;while(e){if(e&1n)v=v*a%q;a=a*a%q;e>>=1n;}return v;}
function polynomial(P,f){const q=I(P.modulus);return P.terms.reduce((v,t)=>mod(v+I(t.coefficient)*t.powers.reduce((w,e,k)=>w*pow(f[k],I(e),q)%q,1n),q),0n);}
function derivative(P,f,j){return Number(P.terms.reduce((v,t)=>{const e=I(t.powers[j]);if(!e)return v;return mod(v+I(t.coefficient)*e*t.powers.reduce((w,a,k)=>w*pow(f[k]%3n,I(a)-BigInt(k===j),3n)%3n,1n),3n);},0n));}
function phaseCertificate(c){
  const P=c.program,q=I(P.modulus),Q=q/3n,n=P.dimension,j=c.target_coordinate,S=c.syndrome.map(I);
  check(Number.isSafeInteger(n)&&n>0&&Number.isSafeInteger(j)&&j>=0&&j<n&&S.length===n&&S.every(a=>a<q)&&S[j]<Q,"canonical syndrome and target");
  let power=q;while(power>1n&&power%3n===0n)power/=3n;check(power===1n&&q>=3n,"ternary root");
  const isPolynomial=P.family==="MODULAR_INTEGER_POLYNOMIAL";
  if(isPolynomial)for(const t of P.terms)check(I(t.coefficient)<q&&t.powers.length===n&&t.powers.every(e=>I(e)>=0n),"integer modular polynomial");
  else check(P.family==="TOP_DIGIT_QUADRATIC_NON_POLYNOMIAL"&&q>=9n&&Number.isSafeInteger(P.coordinate)&&P.coordinate>=0&&P.coordinate<n&&[1,2].includes(P.coefficient),"precise nonpolynomial countercontrol");
  const values=[0,1,2].map(h=>{const f=S.slice();f[j]+=Q*BigInt(h);return isPolynomial?polynomial(P,f):Q*BigInt(P.coefficient)*(f[P.coordinate]/Q)**2n%q;});
  const delta=mod(values[1]-values[0],q),linear=delta%Q===0n&&mod(values[2]-values[0]-2n*delta,q)===0n;
  same(c.phase_numerators_on_three_classes,values.map(String),"exact three-class phase values");
  check(c.phase_is_known_trit_translation===linear&&c.known_trit_translation===(linear?Number(delta/Q):null),"known character translation, not arbitrary phases");
  const gradient=isPolynomial?derivative(P,S,j):null;
  check(c.polynomial_derivative_trit===gradient&&c.square_zero_high_increment_theorem_applies===(isPolynomial&&q>=9n)&&c.root_one_or_nonpolynomial_exception_not_overridden===!(isPolynomial&&q>=9n),"Taylor scope");
  if(isPolynomial&&q>=9n)check(linear&&gradient===Number(delta/Q)&&Q*Q%q===0n,"square-zero Taylor identity and gradient");
  return {P,q,Q,S,j,g:linear?Number(delta/Q):null};
}
const hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_SYNDROME_PHASE_COMPILER.md"))).digest("hex");
check(report.derivation_sha256===hash&&report.status==="INITIAL_POLYNOMIAL_FREQUENCY_PHASE_COMPILATION_REVIEW_PENDING","pinned derivation and review status");
for(const k of["quantum_speedup_proved","candidate_record_accepted","novelty_claim","pointwise_secret_success_or_general_measurement_no_go","additional_same_secret_samples_or_query_access_covered","native_source_supply_or_efficient_decoder_created"])check(report[k]===false,"explicit limitation: "+k);
check(report.every_fixed_native_label_matrix_uniform_secret_risk_scope===true,"uniform prior, fixed labels");
const schedule=[[1,2,0],[2,16,0],[3,32,1],[2,64,1]];
check(report.analytic_fiber_certificates.length===4,"analytic schedule");
report.analytic_fiber_certificates.forEach((c,i)=>{const v=phaseCertificate(c),[n,r,j]=schedule[i];check(c.program.dimension===n&&v.q===3n**BigInt(r)&&v.j===j&&v.g!==null,"scalable exact controls");});
const digit=phaseCertificate(report.nonpolynomial_top_digit_countercontrol),root=phaseCertificate(report.root_one_countercontrol);
check(digit.q===81n&&digit.g===null&&root.q===3n&&root.g===null,"exceptions remain exceptions");
const recipe=report.scalable_gradient_recipe;
same([recipe.dimension,recipe.digits,recipe.original_qutrits,recipe.target_coordinate],[2,64,126,1],"scalable recipe geometry");
check(recipe.retained_measurement_register_trits===1&&recipe.low_frequency_scratch_trits===2&&recipe.extra_original_source_copies===0&&recipe.frequency_row_evaluations_per_compute_or_uncompute===126,"minimal one-trit arithmetic cost");
same(recipe.steps,["compute F(x) mod3 reversibly from public frequency rows mod3","evaluate and copy partial_j P(F mod3) into ONE gradient trit","UNCOMPUTE every low-frequency and derivative scratch register","measure ONLY the gradient trit","run the original remaining receiver on the original word registers","add polynomial derivative at the syndrome to the original trit prediction mod3"],"clean compute/copy/uncompute/measure/translate order");
for(const k of["phase_program_parameters_needed_only_mod3","label_dependent_program_coefficients_may_still_depend_on_high_labels","known_arithmetic_polynomial_in_public_input_size","uniform_secret_mean_success_preserved"])check(recipe[k]===true,"recipe invariant: "+k);
for(const k of["full_frequency_or_syndrome_register_required","original_words_or_target_high_trit_measured","frequency_fiber_basis_or_inverse_supplied","pointwise_secret_success_preserved","additional_same_secret_sources_or_query_access_covered","interleaved_noncommuting_phase_operations_covered","hardware_gate_export_implemented"])check(recipe[k]===false,"recipe does not grant: "+k);

function matmul(A,B){return A.map(row=>B[0].map((_,j)=>row.reduce((v,a,k)=>v+a*B[k][j],0n)));}
function chart(r){let V=[[1n,0n],[0n,1n]],B=[[-1n,-1n],[1n,-2n]];for(let i=0;i<2*r-1;i++)V=matmul(V,B);const q=3n**BigInt(r),den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]),u=q*(2n*V[1][1]+V[1][0]),v=q*(-2n*V[0][1]-V[0][0]);check(u%den===0n&&v%den===0n,"integral native ideal chart");return[u/den,v/den];}
function words(M){return Array.from({length:3**M},(_,i)=>Array.from({length:M},(_,j)=>Math.floor(i/3**(M-j-1))%3));}
function counts(indices,hs,ws,phases){return[0,1,2].map(t=>ws.map(z=>{const exponents=indices.map((a,k)=>mod(t*hs[k]+phases[k]-z.reduce((v,b,j)=>v+b*ws[a][j],0),3));const C=[0,0,0];for(const a of exponents)for(const b of exponents)C[mod(a-b,3)]++;check(C[1]===C[2]&&C[0]>=C[1],"real nonnegative cubic Born law");return C[0]-C[1];}));}
let exactProbabilities=0,nativeBranches=0;
check(report.native_receiver_controls.length===2,"complete native controls");
report.native_receiver_controls.forEach((c,index)=>{
  const [n,r,j]=index===0?[1,4,0]:[1,6,0],q=3**r,Q=q/3,M=n*r-2,D=3**M,ws=words(M),[u,v]=chart(r);
  same([c.dimension,c.root_digits,c.modulus,c.target_coordinate],[n,r,q,j],"native control schedule");
  check(c.native_labels.length===M&&c.full_frequency_rows.length===M,"complete original native batch");
  for(let k=0;k<M;k++){check(c.native_labels[k].length===n&&c.full_frequency_rows[k].length===2&&c.full_frequency_rows[k].every(row=>row.length===n),"native label shapes");for(let a=0;a<n;a++){const [l,h]=c.native_labels[k][a];check([l,h,...c.full_frequency_rows[k].map(row=>row[a])].every(z=>Number.isSafeInteger(z)&&z>=0&&z<q),"canonical native full labels");same(c.full_frequency_rows[k].map(row=>row[a]),[Number(mod(u*BigInt(l)+v*BigInt(h),BigInt(q))),Number(mod((u+v)*BigInt(l)-u*BigInt(h),BigInt(q)))],"actual native chart, not an oracle surrogate");}}
  const frequencies=ws.map(w=>Array.from({length:n},(_,a)=>mod(w.reduce((s,d,k)=>s+(d?c.full_frequency_rows[k][d-1][a]:0),0),q)));
  same(c.words,ws,"original lexicographic word basis");same(c.word_frequencies,frequencies,"all public frequency evaluations");
  const groups=new Map();frequencies.forEach((f,i)=>{const S=f.map((a,k)=>k===j?a%Q:a),key=JSON.stringify(S);if(!groups.has(key))groups.set(key,{S,indices:[]});groups.get(key).indices.push(i);});
  const branches=[...groups.values()].sort((a,b)=>a.S[0]-b.S[0]);check(c.occupied_syndrome_branches.length===branches.length,"all occupied Born branches");
  const total=Array.from({length:3},()=>Array(D).fill(0)),baseBranches=[],gradientMass=[0,0,0];
  branches.forEach((b,k)=>{const rec=c.occupied_syndrome_branches[k],v=phaseCertificate(rec.certificate),hs=b.indices.map(a=>Math.floor(frequencies[a][j]/Q)),P=v.P;
    same(rec.certificate.syndrome,b.S.map(String),"canonical occupied nuisance syndrome");check(v.q===BigInt(q)&&v.j===j&&v.g!==null,"compatible polynomial control");
    same(rec.word_indices,b.indices,"complete fiber words");same(rec.high_trits,hs,"all target high trits");check(rec.Born_mass===fraction(b.indices.length,D),"unconditioned original Born mass");
    const phases=b.indices.map(a=>Number(mod(polynomial(P,frequencies[a].map(BigInt))-polynomial(P,b.S.map(BigInt)),BigInt(q))/BigInt(Q)));
    const base=counts(b.indices,hs,ws,hs.map(()=>0)),chirped=counts(b.indices,hs,ws,phases);
    for(let t=0;t<3;t++){same(chirped[t],base[(t+v.g)%3],"independent exact class-law translation");check(base[t].reduce((a,b)=>a+b,0)===b.indices.length*D,"Born normalization with all failure outcomes");for(let o=0;o<D;o++)total[t][o]+=chirped[t][o];}
    baseBranches.push({g:v.g,base});gradientMass[v.g]+=b.indices.length;exactProbabilities+=6*D;nativeBranches++;
  });
  same(c.chirped_output_trit_laws_no_syndrome_reported,total.map(row=>row.map(a=>fraction(a,D*D))),"all exact chirped output probabilities");
  const decoder=ws.map((_,o)=>[0,1,2].reduce((best,t)=>total[t][o]>total[best][o]?t:best,0));same(c.original_chirped_MAP_decoder,decoder,"exact reference decoder with deterministic ties");
  const original=decoder.reduce((s,t,o)=>s+total[t][o],0),compiled=baseBranches.reduce((s,b)=>s+decoder.reduce((v,d,o)=>v+b.base[(d+b.g)%3][o],0),0);
  check(original===compiled&&c.original_chirped_uniform_trit_success===fraction(original,3*D*D)&&c.compiled_unchirped_uniform_trit_success===fraction(compiled,3*D*D),"uniform-secret risk equality, not pointwise equality");
  const counter=c.constant_decision_pointwise_countercontrol;same(counter.original_success_by_trit,["1","0","0"],"constant prediction control");same(counter.compiled_success_by_trit,gradientMass.map(a=>fraction(a,D)),"different pointwise success permitted");check(counter.uniform_mean_success_both==="1/3","same uniform risk in countercontrol");
  same(c.calibration_secrets_only,[[0],[1],[3],[q-1]],"zero, primitive and nonprimitive physical controls");
  for(const k of["actual_full_root_phase_Born_residual","gradient_only_complete_uniform_secret_score_residual","dirty_full_frequency_probability_residual"])check(Number.isFinite(c[k])&&c[k]>=0&&c[k]<3e-11,"physical replay residual: "+k);
  check(c.complete_uniform_secrets_enumerated_for_gradient_calibration===q**n&&c.complete_ensemble_amplitude_cells_calibration_only===q**n*D&&c.classical_word_and_output_enumerations_calibration_only===D,"complete calibration cost, not scalable execution");
  check(c.dirty_full_frequency_scratch_or_measurement_trit_success==="1/3"&&c.efficient_MAP_decoder_or_fiber_transform_supplied===false&&c.uniform_mean_not_pointwise_secret_guarantee===true&&c.speedup_claim_allowed===false,"negative scratch control and no speedup");
});
const p=report.partial_block_frequency_countercontrol,first=report.native_receiver_controls[0];
same(p.words,[[0,0],[1,1],[2,2]],"partial-block native word control");
const total=p.words.map(w=>first.word_frequencies[w[0]*3+w[1]][0]),partial=p.words.map(w=>w[0]?first.full_frequency_rows[0][w[0]-1][0]:0),values=partial.map(a=>41*a*a%81);
same(p.total_frequencies,total,"actual total frequencies");same(p.common_total_nuisance_syndrome,[0],"shared total nuisance fiber");check(total.every(a=>a%27===0),"one total syndrome");same(p.first_block_frequencies,partial,"actual partial frequencies");same(p.partial_quadratic_phase_values,values,"actual partial-block quadratic phase");check((values[1]-values[0])%27!==0&&p.native_control_index===0&&p.known_total_trit_translation_available===false,"partial-block exception is not compiled away");
console.log(JSON.stringify({status:"independent_initial_polynomial_phase_risk_certificates_passed",analyticCertificates:4,nativeBranches,exactProbabilities,physicalReplaysIndependentlyReexecuted:false,phaseExceptions:3,pointwiseGuarantee:false,quantumSpeedupProved:false}));
