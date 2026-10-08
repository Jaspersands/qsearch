"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const report=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../phase_workbench/ternary_quadratic_program_receiver.json"),"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},same=(a,b,m)=>check(JSON.stringify(a)===JSON.stringify(b),m),mod=(a,q)=>(a%q+q)%q;
const words=k=>Array.from({length:3**k},(_,i)=>Array.from({length:k},(_,j)=>Math.floor(i/3**(k-j-1))%3));
const dot=(a,b)=>a.reduce((s,x,j)=>s+x*b[j],0),key=JSON.stringify;
function gcd(a,b){while(b)[a,b]=[b,a%b];return a<0n?-a:a;}
function frac(a,b){const g=gcd(a,b);a/=g;b/=g;return b===1n?String(a):a+"/"+b;}
function rref(A){
  A=A.map(row=>row.map(x=>mod(x,3)));const pivots=[];let r=0;
  for(let j=0;j<A[0].length&&r<A.length;j++){
    const p=A.findIndex((row,i)=>i>=r&&row[j]);if(p<0)continue;
    [A[r],A[p]]=[A[p],A[r]];const inverse=A[r][j];A[r]=A[r].map(x=>x*inverse%3);
    for(let i=0;i<A.length;i++)if(i!==r){const f=A[i][j];A[i]=A[i].map((x,k)=>mod(x-f*A[r][k],3));}
    pivots.push(j);r++;
  }
  return {rows:A.slice(0,r),pivots,free:Array.from({length:A[0].length},(_,i)=>i).filter(i=>!pivots.includes(i))};
}
const rankColumns=(C,h)=>C.length?rref(Array.from({length:h},(_,i)=>C.map(v=>v[i]))).pivots.length:0;
const combine=(C,t,h)=>Array.from({length:h},(_,i)=>mod(C.reduce((s,v,j)=>s+v[i]*t[j],0),3));
function nativeChart(level){
  let V=[[1n,0n],[0n,1n]],pi=[[-1n,-1n],[1n,-2n]];
  for(let j=0;j<level-1;j++)V=V.map(row=>pi[0].map((_,i)=>row.reduce((s,a,k)=>s+a*pi[k][i],0n)));
  const q=3n**BigInt(Math.ceil(level/2)),den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]);
  const a=q*(2n*V[1][1]+V[1][0]),b=q*(-2n*V[0][1]-V[0][0]);check(a%den===0n&&b%den===0n,"integral native chart");
  const u=a/den,v=b/den;
  return label=>{const[x,y]=label.map(BigInt);return[Number(mod(u*x+v*y,q)),Number(mod((u+v)*x-u*y,q))];};
}
function apply(gates,x){
  x=[...x];for(const gate of gates){
    if(gate.gate==="SWAP_F3"){const i=gate.first,j=gate.second;[x[i],x[j]]=[x[j],x[i]];}
    else if(gate.gate==="SCALE_F3"){check(gate.factor===2,"nonzero field scaling");x[gate.wire]=2*x[gate.wire]%3;}
    else {check(gate.gate==="SUM_F3"&&[1,2].includes(gate.factor)&&gate.target!==gate.control,"known invertible SUM");x[gate.target]=(x[gate.target]+gate.factor*x[gate.control])%3;}
  }return x;
}
const hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_QUADRATIC_PROGRAM_RECEIVER.md"))).digest("hex");
check(report.derivation_sha256===hash&&report.status==="ONE_USE_QUADRATIC_PROGRAM_SECRET_EQUATION_RECEIVER_NATIVE_FACTORY_OPEN_REVIEW_PENDING","pinned derivation");
for(const k of["candidate_record_accepted","unconditional_IID_native_program_factory_supplied","growing_depth_or_full_secret_quantum_speedup_proved"])check(report[k]===false,"conditional receiver, not a random-source breakthrough: "+k);
check(report.native_calibration_controls.length===2,"all prespecified native controls");
let BellBranches=0,rootWords=0,chartBasisWords=0;
report.native_calibration_controls.forEach((c,index)=>{
  const n=index+1,K=27,W=(n+1)**2,M=K*W,grid=words(3),even=nativeChart(4),odd=nativeChart(3),labels=c.original_labels,source=c.original_source;
  check(c.engineered_low_source_seed===88601+index&&labels.length===M&&source.dimension===n&&source.original_even_level===4&&source.acquired_original_native_inputs===M&&source.active_original_inputs===27&&source.untouched_original_inputs===M-27,"engineered source and full original acquisition");
  check(source.original_source_ids.length===M&&new Set(source.original_source_ids).size===M&&source.original_source_ids.every(x=>typeof x==="string"&&x.length),"all original ancestors");
  const active=grid.map((_,i)=>i*W);same(source.active_original_source_ids,active.map(i=>source.original_source_ids[i]),"true active ancestry");
  same(source.odd_input_original_ancestors,active.map(i=>[source.original_source_ids[i]]),"each odd input from its own original curvature-zero pivot");
  same(source.untouched_original_source_ids,source.original_source_ids.filter((_,i)=>!active.includes(i)),"unused originals not measured zero");
  check(c.source_is_IID_population_control===false&&c.IID_original_source_program_factory_proved===false&&c.identical_program_factory_supplied===false&&c.whole_original_or_parent_packet_word_cube_enumerated===false&&c.higher_parent_secret_digits_recovered===false,"no free engineered program factory or whole-cube claim");
  check(source.distinct_ids_certify_physical_independence===false&&source.upstream_DCP_or_LWE_input_acquisition_implemented_here===false,"provenance IDs are not a source theorem");
  const pairs=active.map(i=>Array.from({length:n},(_,l)=>even(labels[i][l])));
  for(let i=0;i<K;i++)for(let l=0;l<n;l++){
    check((pairs[i][l][0]+pairs[i][l][1])%3===0,"first original curvature-zero site; known SDE picks it");
    same(odd(c.odd_native_labels[i][l]),pairs[i][l],"odd rows equal actual original relative phases");
    check((c.odd_native_labels[i][l][0]+c.odd_native_labels[i][l][1])%3===grid[i][l],"actual engineered low native row");
  }
  check(c.inner_pointers.length===0,"single active support has no measured inner complements");
  const low=Array.from({length:n},(_,l)=>grid.map(x=>x[l])),R=rref(low),H=R.free.length;
  check(H===27-n&&c.outer_syndrome.length===n&&c.outer_syndrome.every(x=>x===0),"known Gaussian calibration outcome, not free selection");
  const assignment=z=>{
    const t=Array(K).fill(0);R.free.forEach((f,j)=>t[f]=z[j]);R.pivots.forEach((p,j)=>t[p]=mod(c.outer_syndrome[j]-R.free.reduce((s,f)=>s+R.rows[j][f]*t[f],0),3));return t;
  };
  const frame=Array.from({length:3},(_,j)=>R.free.map(i=>grid[i][j]));same(c.logical_frame,frame,"engineered evaluation-code restriction");
  const physical=frame.map(v=>{const base=assignment(Array(H).fill(0));return assignment(v).map((a,i)=>mod(a-base[i],3));});
  same(physical,Array.from({length:3},(_,j)=>grid.map(x=>x[j])),"real physical directions through original Gaussian pivots");
  for(let i=0;i<3;i++)for(let j=i;j<3;j++)for(let k=j;k<3;k++)for(let l=0;l<n;l++)check(mod(grid.reduce((s,x,a)=>s+x[l]*physical[i][a]*physical[j][a]*physical[k][a],0),3)===0,"every actual mixed cubic derivative vanishes");
  check(c.mixed_cubic_admission.classical_quadratic_restriction_admitted===true&&c.mixed_cubic_admission.mixed_cubic_witnesses.length===0,"true mixed admission, not diagonal-only test");
  const columns=[...frame];for(let j=0;j<H;j++){const e=Array(H).fill(0);e[j]=1;if(rankColumns([...columns,e],H)>columns.length)columns.push(e);}
  same(c.complete_chart_columns,columns,"complete public invertible restriction chart");
  for(let j=0;j<H;j++){const e=Array(H).fill(0);e[j]=1;same(apply(c.chart_gates,columns[j]),e,"actual SWAP/SCALE/SUM recipe on a basis");chartBasisWords++;}
  check(c.restriction_complement.length===H-3&&c.restriction_complement.every(x=>x===0),"measured complement calibration");
  const base=combine(columns.slice(3),c.restriction_complement,H);same(c.restriction_base,base,"native logical base");
  const F=t=>Array.from({length:n},(_,l)=>mod(t.reduce((s,x,i)=>s+(x?pairs[i][l][x-1]:0),0),9)),f0=F(assignment(base));
  const frequency=z=>{
    const x=combine(frame,z,H).map((a,i)=>mod(a+base[i],3));same(apply(c.chart_gates,x),[...z,...c.restriction_complement],"retained actual coordinates and measured complement");
    return F(assignment(x)).map((a,l)=>{const diff=mod(a-f0[l],9);check(diff%3===0,"full original-root divisibility");return diff/3;});
  };
  const table=words(3).map(frequency);same(c.complete_native_program_frequency_table,table,"all actual original-native program phases");rootWords+=27;
  const value=z=>c.component_matrices.map((A,l)=>mod(A.reduce((s,row,i)=>s+z[i]*dot(row,z),0)+dot(c.component_linear[l],z),3));
  check(c.component_matrices.length===n&&c.component_linear.length===n,"known n-parameter quadratic family");
  for(const A of c.component_matrices)check(A.length===3&&A.every(row=>row.length===3&&row.every(x=>Number.isInteger(x)&&x>=0&&x<3))&&A.every((row,i)=>row.every((a,j)=>a===A[j][i])),"canonical symmetric field matrices");
  same(words(3).map(value),table,"public quadratic matrices equal true native frequencies");
  check(c.raw_program_branch_probability===frac(1n,3n**24n)&&c.all_restriction_outcomes_accepted===true&&c.one_unknown_program_copy_supplied===true,"source branch probability charged, one supplied program");
  check(c.original_source_program_and_one_Bell_branch_probability===frac(1n,3n**30n),"combined original source/program/Bell branch mass, not conditional mass promoted");
  const receiver=c.receiver,v=receiver.direction,grad=c.component_matrices.map(A=>A.map(row=>2*dot(row,v)%3)),offset=c.component_linear.map(row=>dot(row,v)%3);
  check(v.length===3&&v.some(Boolean)&&c.component_matrices.every(A=>mod(A.reduce((s,row,i)=>s+v[i]*dot(row,v),0),3)===0),"common isotropic direction before Bell outcome");
  same(receiver.gradient_rows,grad,"public gradient labels");same(receiver.label_offset,offset,"public label affine offset");
  check(receiver.gradient_rank===rref(grad).pivots.length&&receiver.gradient_rank===n&&receiver.uniform_full_secret_label_law_certified===true,"verified full gradient rank");
  for(const k of["one_supplied_program_consumed_per_equation","all_Bell_outcomes_accepted"])check(receiver[k]===true,"one-use all-outcome receiver");check(receiver.identical_program_copies_or_unknown_inverse_used===false,"no matched copies or phase inverse");
  check(c.isotropic_search.method==="bounded-complete-isotropic-calibration"&&c.isotropic_search.scalable_search_claimed===false&&c.isotropic_search.directions_audited===27&&c.isotropic_search.guaranteed_width===(n+1)**3-n,"small calibration is not wide guaranteed construction");
  check(c.isotropic_search.direction_selection_reads_linear_coefficients===false,"matrix-only isotropic policy");
  const p=c.physical_receiver,s=Array.from({length:n},(_,i)=>i+1),hist=new Map(),ws=words(3);
  same(p.calibration_secret,s,"prespecified original integer-secret calibration");same(p.receiver,receiver,"same certified line");
  check(p.all_Bell_branches.length===729&&p.reference_dimension===2&&p.one_program_consumed_per_actual_use===true&&p.virtual_calibration_branches_are_source_copies===false&&p.unknown_gate_inverse_or_Clifford_byproduct_correction_used===false,"complete one-use program instrument, not repeatable oracle");
  let total=0;
  for(let bi=0;bi<27;bi++)for(let ai=0;ai<27;ai++){
    const b=ws[bi],a=ws[ai],row=p.all_Bell_branches[bi*27+ai],label=grad.map((g,l)=>mod(dot(g,a)+offset[l],3)),answer=mod(dot(s,label),3),correction=dot(b,v)%3;
    same(row.Bell_shift,a,"all shifts exactly once");same(row.Bell_phase,b,"all Bell phases exactly once");same(row.public_equation_label,label,"actual equation label");
    check(row.answer===answer&&row.known_phase_correction===correction&&row.raw_Bell_probability==="1/729","all branches charged with correct known Pauli orientation");
    const phase=[0,1,2].map(j=>{
      const x=a.map((u,i)=>mod(u+j*v[i],3)),original=frequency(x);
      return mod(dot(s,original)-j*dot(b,v)+j*correction,3);
    });
    const probabilities=[0,1,2].map(k=>{
      let re=0,im=0;for(let j=0;j<3;j++){const angle=2*Math.PI*mod(phase[j]-j*k,3)/3;re+=Math.cos(angle)/3;im+=Math.sin(angle)/3;}return re*re+im*im;
    });
    check(Math.abs(probabilities[answer]-1)<4e-12&&row.all_Fourier_probabilities.length===3&&row.all_Fourier_probabilities.every((x,j)=>Number.isFinite(x)&&Math.abs(x-probabilities[j])<4e-12),"Bell projection from original-root phases gives exact Fourier equation");
    const k=key(label);hist.set(k,(hist.get(k)||0)+1);total+=1/729;BellBranches++;
  }
  const expected=[...hist].map(([label,count])=>({label:JSON.parse(label),count})).sort((a,b)=>key(a.label).localeCompare(key(b.label)));
  same(p.public_label_histogram,expected,"uniform full field label image");check(hist.size===3**n&&expected.every(row=>row.count===729/3**n),"exact affine-gradient pushforward law");
  check(Math.abs(total-1)<4e-12&&Math.abs(p.total_raw_Bell_probability-1)<4e-12&&Number.isFinite(p.arbitrary_entangled_data_maximum_amplitude_error)&&p.arbitrary_entangled_data_maximum_amplitude_error>=0&&p.arbitrary_entangled_data_maximum_amplitude_error<4e-12,"complete Bell norm and finite entangled-input replay residual");
});
same(report.conditional_sample_ledgers.map(c=>c.dimension),[1,2,8,32,128],"prespecified conditional sample schedule");
for(const c of report.conditional_sample_ledgers){const n=c.dimension,m=n+8;check(c.extra_equations===8&&c.independent_supplied_programs_required===m&&c.field_equation_rank_failure_upper===frac(3n**BigInt(n)-1n,2n*3n**BigInt(m))&&c.conditional_on_each_program_full_gradient_rank_and_fresh_Bell_randomness===true&&c.availability_of_these_programs_proved===false&&c.original_full_modulus_secret_recovery_proved===false,"conditional exact equation recovery, no source factory or full-secret claim");}
const offsets=report.fresh_linear_offset_law_census,hist=new Map();same(offsets.direction,[0,1],"matrix-only zero-quadratic calibration direction");
for(const beta of words(4)){const label=[beta[1],beta[3]],k=key(label);hist.set(k,(hist.get(k)||0)+1);}
const offsetHistogram=[...hist].map(([label,count])=>({label:JSON.parse(label),count})).sort((a,b)=>key(a.label).localeCompare(key(b.label)));
same(offsets.public_label_histogram,offsetHistogram,"complete fresh uniform offset labels despite deficient gradient");
check(offsets.components===2&&offsets.width===2&&offsets.gradient_rank===0&&offsets.complete_independent_linear_offsets===81&&offsets.direction_selection_reads_linear_coefficients===false&&offsets.uniform_labels_require_full_gradient_rank_for_fixed_program===true&&offsets.uniform_labels_from_fresh_uniform_offsets_need_full_gradient_rank===false&&offsets.fresh_uniform_independent_linear_offsets_are_a_source_premise===true&&offsets.unconditional_native_factory_proved_by_this_census===false,"source law differs from fixed-program criterion, no circular factory claim");
console.log(JSON.stringify({status:"independent_native_quadratic_program_receiver_certificates_passed",nativeOriginalRootWords:rootWords,restrictionChartBasisWords:chartBasisWords,allBellBranches:BellBranches,conditionalFullGradientControls:2,unconditionalNativeFactory:false}));
