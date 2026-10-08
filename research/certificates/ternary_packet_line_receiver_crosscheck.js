"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../phase_workbench/ternary_packet_line_receiver.json"),"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},key=JSON.stringify,same=(a,b,m)=>check(key(a)===key(b),m),mod=(a,q)=>(a%q+q)%q;
const words=h=>Array.from({length:3**h},(_,i)=>Array.from({length:h},(_,j)=>Math.floor(i/3**(h-j-1))%3));
check(R.derivation_sha256===crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_PACKET_LINE_RECEIVER.md"))).digest("hex"),"pinned line derivation");
check(R.status==="ONE_USE_PACKET_LINE_COMPILED_EXACT_ADMISSION_SCOPED_REVIEW_PENDING"&&R.accepted_speedup_candidate===false&&R.general_receiver_impossibility_claim===false&&R.new_original_source_or_unknown_inverse_granted===false,"compiled line instrument and scoped exact admission only");
function chart(level){
  let V=[[1n,0n],[0n,1n]];const pi=[[-1n,-1n],[1n,-2n]];
  for(let j=0;j<level-1;j++)V=V.map(row=>[0,1].map(i=>row.reduce((s,x,k)=>s+x*pi[k][i],0n)));
  const den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]),a=9n*(2n*V[1][1]+V[1][0]),b=9n*(-2n*V[0][1]-V[0][0]);check(a%den===0n&&b%den===0n,"integral native root9 chart");
  return z=>{const[x,y]=z.map(BigInt),u=a/den,v=b/den;return[Number(mod(u*x+v*y,9n)),Number(mod((u+v)*x-u*y,9n))];};
}
const even=chart(4),odd=chart(3);
function rref(A){
  const w=A[0].length;A=A.map(row=>row.map(x=>mod(x,3)));let r=0;const pivots=[];
  for(let j=0;j<w&&r<A.length;j++){const k=A.findIndex((row,i)=>i>=r&&row[j]);if(k<0)continue;[A[r],A[k]]=[A[k],A[r]];A[r]=A[r].map(x=>x*A[r][j]%3);for(let i=0;i<A.length;i++)if(i!==r){const f=A[i][j];A[i]=A[i].map((x,k)=>mod(x-f*A[r][k],3));}pivots.push(j);r++;}
  return{rows:A.slice(0,r),pivots,free:Array.from({length:w},(_,i)=>i).filter(i=>!pivots.includes(i))};
}
function kernel(columns){const r=rref(columns[0].map((_,j)=>columns.map(v=>v[j]))),v=Array(columns.length).fill(0);v[r.free[0]]=1;r.pivots.forEach((p,j)=>v[p]=mod(-r.rows[j][r.free[0]],3));return v;}
const sum=(v,ids)=>v[0].map((_,j)=>mod(ids.reduce((s,i)=>s+v[i][j],0),3));
function support(v){
  const n=v[0].length,blocks=[],common=[];
  for(let j=0;j<n+1;j++){const ids=Array.from({length:n+1},(_,i)=>j*(n+1)+i),c=kernel(ids.map(i=>v[i])),a=ids.filter((_,i)=>c[i]===1),b=ids.filter((_,i)=>c[i]===2);if(!a.length||!b.length)return a.length?a:b;blocks.push([a,b]);common.push(sum(v,a));}
  const c=kernel(common),a=c.flatMap((x,j)=>x===1?[j]:[]),b=c.flatMap((x,j)=>x===2?[j]:[]);
  return(!a.length||!b.length?(a.length?a:b).flatMap(j=>blocks[j][0]):[...a.flatMap(j=>blocks[j][0]),...a.flatMap(j=>blocks[j][1]),...b.flatMap(j=>blocks[j][0])]).sort((a,b)=>a-b);
}
function model(labels,syndrome){
  const K=labels.length,n=labels[0].length,pairs=labels.map(row=>row.map(odd));
  const C=Array.from({length:n},(_,l)=>pairs.map(row=>row[l][0]%3)),kappa=Array.from({length:n},(_,l)=>pairs.map(row=>mod(row[l][0]+row[l][1],9)/3));check(kappa.flat().every(Number.isInteger),"actual odd frequencies");
  const r=rref(Array.from({length:n},(_,l)=>labels.map(row=>mod(row[l][0]+row[l][1],3)))),h=r.free.length;
  check(syndrome.length===r.pivots.length&&syndrome.every(x=>Number.isInteger(x)&&x>=0&&x<3),"full canonical syndrome");
  const assignment=z=>{const t=Array(K).fill(0);r.free.forEach((f,j)=>t[f]=z[j]);r.pivots.forEach((p,j)=>t[p]=mod(syndrome[j]-r.free.reduce((s,f)=>s+r.rows[j][f]*t[f],0),3));return t;};
  const base=assignment(Array(h).fill(0)),D=Array.from({length:K},(_,i)=>r.free.map((_,j)=>mod(assignment(Array.from({length:h},(_,k)=>Number(j===k)))[i]-base[i],3)));
  const residual=z=>{const t=assignment(z);return C.map((_,l)=>{const d=mod(t.reduce((s,x,i)=>s+(x?pairs[i][l][x-1]:0)-(base[i]?pairs[i][l][base[i]-1]:0),0),9);check(d%3===0,"true ring-root residual divisible3");return d/3;});};
  const maskRows=C.flatMap(row=>r.free.map((_,j)=>row.map((x,i)=>x*D[i][j]%3))),maskRank=rref(maskRows).pivots.length;
  const data={frequency_pairs:pairs,C,kappa,D,base,original_low_syndrome:C.map(row=>mod(row.reduce((s,x,i)=>s+x*base[i],0),3)),coupling_mask_rows:maskRows,coupling_mask_rank:maskRank,only_constant_diagonal_masks_preserve_kernel:maskRank===K-1,coupling_is_a_rank_certificate_not_a_direction_enumerator:true,low_matrix_rank:rref(C).pivots.length,complete_direction_search_or_teleportation_success_claimed:false};
  return{K,n,h,r,data,assignment,residual};
}
let checks=0,admitted=0,branches=0;
function audit(a){
  check(a.status==="COMPLETE_NATIVE_ALL_TRANSLATION_LINE_AUDIT"&&a.odd_level===3&&a.complete_direction_search_is_scalable===false&&a.one_unknown_program_supplied_or_decoder_implemented_by_this_audit===false,"complete bounded line calibration");
  const m=model(a.native_labels,a.syndrome),points=words(m.h);same(a.RREF_rows,m.r.rows,"actual native RREF");same(a.coupling,m.data,"all public coupling/curvature equations");same(a.logical_points,points,"ALL logical words");same(a.actual_residual_table,points.map(m.residual),"ALL actual native residuals");
  same(a.direction_certificates.map(c=>c.logical_direction),points.filter(v=>v.some(Boolean)),"EVERY nonzero direction");let count=0,yes=0;
  for(const c of a.direction_certificates){
    const v=c.logical_direction,d=m.data.D.map(row=>mod(row.reduce((s,x,j)=>s+x*v[j],0),3)),S=d.flatMap((x,i)=>x?[i]:[]);
    const gradient=m.data.C.map(row=>Array.from({length:m.h},(_,j)=>mod(-S.reduce((s,i)=>s+row[i]*m.data.D[i][j],0),3))),constant=m.data.C.map((row,l)=>mod(S.reduce((s,i)=>s+m.data.kappa[l][i]-row[i]*m.data.base[i],0),3));
    same(c.physical_direction,d,"physical direction");same(c.physical_support,S,"full changed-site support");same(c.line_sum_gradient,gradient,"exact whole-packet line-sum gradient");same(c.line_sum_constant,constant,"exact whole-packet line-sum constant");
    const accepts=!constant.some(Boolean)&&!gradient.flat().some(Boolean);check(c.affine_for_every_Bell_shift_and_every_secret===accepts&&c.direction_may_read_all_public_high_labels_and_syndrome===true&&c.direction_selected_before_current_Bell_shift_required===true&&c.known_nonzero_equation_or_uniform_equation_labels_guaranteed===false,"high-informed all-shift admission, no automatic equation quality");
    for(const z of points){const values=[0,1,2].map(j=>m.residual(z.map((x,k)=>mod(x+j*v[k],3))));const actual=Array.from({length:m.n},(_,l)=>mod(values.reduce((s,row)=>s+row[l],0),3)),expected=constant.map((x,l)=>mod(x+gradient[l].reduce((s,y,j)=>s+y*z[j],0),3));same(actual,expected,"exact line identity for EVERY translation");count++;}
    if(accepts){yes++;if(m.data.only_constant_diagonal_masks_preserve_kernel){check(S.length===m.K,"coupled code cannot admit proper support");same(m.data.original_low_syndrome,m.data.kappa.map(row=>mod(row.reduce((s,x)=>s+x,0),3)),"coupled code cannot admit wrong syndrome");}}
  }
  check(a.all_direction_shift_pairs_checked===count&&a.admitted_nonzero_directions===yes,"complete affine admission counts");checks+=count;admitted+=yes;branches++;return m;
}
same(R.actual_source_controls.map(c=>c.seed),[94101,94102],"fixed original-source cohorts");
for(const c of R.actual_source_controls){
  const s=c.source,n=s.dimension,K=s.odd_inputs_acquired,M=K*(n+1)**2,rows=c.original_native_labels.map(row=>row.map(even));
  check(s.original_even_level===4&&s.acquired_original_native_inputs===M&&rows.length===M&&new Set(s.original_source_ids).size===M,"paid original source and distinct ancestry");
  check(s.distinct_ids_certify_physical_independence===false&&s.unknown_preparation_inverse_or_amplification_used===false&&s.untouched_curvature_labels_claimed_fresh_IID===false&&c.selected_pointer_is_population_or_free_source_claimed===false,"no stronger source access");
  const B=rows.map(row=>row.map(([a,b])=>(a+b)%3)),W=(n+1)**2,ss=Array.from({length:K},(_,j)=>support(B.slice(j*W,(j+1)*W)).map(i=>i+j*W));
  same(s.odd_input_original_ancestors,ss.map(S=>S.map(i=>s.original_source_ids[i])),"independent curvature-only support reconstruction");
  const ptr=ss.flatMap(S=>S.slice(1)),anchor=Array(M).fill(0);ptr.forEach((i,j)=>anchor[i]=c.selected_pointer[j]);
  const F=t=>Array.from({length:n},(_,l)=>mod(t.reduce((sum,x,i)=>sum+(x?rows[i][l][x-1]:0),0),9)),base=F(anchor);
  const oddPairs=ss.map(S=>[1,2].map(j=>{const t=[...anchor];S.forEach(i=>t[i]=mod(t[i]+j,3));return F(t).map((x,l)=>mod(x-base[l],9));})).map(pair=>Array.from({length:n},(_,l)=>pair.map(row=>row[l])));
  const prototype=model(c.branches[0].audit.native_labels,c.branches[0].audit.syndrome);same(c.branches.map(b=>b.audit.syndrome),words(prototype.r.pivots.length),"every syndrome at selected pointer");check(c.all_syndromes_at_this_pointer_checked===true&&c.all_original_pointer_outcomes_checked===(ptr.length===0),"not every pointer or a free selected branch");
  for(const b of c.branches){const m=audit(b.audit);same(m.data.frequency_pairs,oddPairs,"actual odd labels from original root9 inputs");const exp=ptr.length+m.r.pivots.length;check(b.raw_source_branch.raw_joint_branch_probability_exponent_base_three===exp&&b.raw_source_branch.raw_joint_branch_probability==="1/"+3n**BigInt(exp),"raw selected pointer/syndrome probability");
    for(const z of words(m.h)){const t=m.assignment(z),original=[...anchor],original0=[...anchor];ss.forEach((S,j)=>S.forEach(i=>{original[i]=mod(original[i]+t[j],3);original0[i]=mod(original0[i]+m.data.base[j],3);}));same(F(original).map((x,l)=>mod(x-F(original0)[l],9)/3),m.residual(z),"actual original-root phase identity");}
  }
}
check(R.countercontrols.length===2,"coupled and decomposable countercontrols retained");for(const c of R.countercontrols){check(c.engineered_not_population_sample===true,"engineered exception not IID experiment");c.branches.forEach(audit);}
function gcd(a,b){a=a<0n?-a:a;while(b)[a,b]=[b,a%b];return a;}
function frac(a,b=1n){const g=gcd(a,b);return[a/g,b/g];}
const add=(a,b)=>frac(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),str=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1],clip=a=>a[0]>=a[1]?[1n,1n]:a;
function gb(n,r){let a=1n,b=1n;for(let i=0;i<r;i++){a*=3n**BigInt(n-i)-1n;b*=3n**BigInt(r-i)-1n;}check(a%b===0n,"integer Gaussian count");return a/b;}
same(R.population_gates.map(x=>x.dimension),[1,4,8,16,32,64],"complete growing population regimes");
for(const x of R.population_gates){
  const n=x.dimension,K=x.odd_inputs,q=3n**BigInt(n);check(K===4*n&&x.original_even_level4_input_cap===K*(n+1)**2,"source regime K=4n");
  const rank=frac(q-1n,2n*3n**BigInt(K)),zero=frac(BigInt(K),q),terms=[];let decomp=frac(0n);
  for(let r=1;r<n;r++){const count=gb(n,r)*3n**BigInt(r*(n-r)),size=3n**BigInt(r)+3n**BigInt(n-r)-1n,term=frac(count*size**BigInt(K),q**BigInt(K));decomp=add(decomp,term);terms.push({projection_rank:r,idempotent_projection_count:String(count),complementary_subspace_union_size:String(size),probability_union_bound:str(term)});}
  same(x.projection_terms,terms,"independent exact idempotent counts and IID column probabilities");const bad=clip(add(add(rank,zero),decomp)),good=frac(1n,q),raw=clip(add(bad,good));
  check(x.rank_failure_upper===str(clip(rank))&&x.zero_column_upper===str(clip(zero))&&x.bad_low_matrix_probability_upper===str(bad)&&x.good_matrix_admissible_syndrome_probability_upper===str(good)&&x.raw_exact_one_use_line_admission_probability_upper===str(raw),"all exact raw population bounds and clipping");
  check(x.original_IID_source_premise_required===true&&x.high_label_informed_direction_search_allowed===true&&x.approximate_or_non_affine_line_receivers_covered===false&&x.multi_program_cubic_cancellation_factory_covered===false&&x.all_native_quantum_receivers_excluded===false,"exact population scope");
}
let bell=0;check(R.physical_receiver_controls.length===3,"all field secrets in physical countercontrol");
for(const c of R.physical_receiver_controls){const m=model(c.native_labels,c.syndrome),points=words(m.h),v=c.direction,s=c.calibration_secret;
  check(c.one_supplied_program_consumed===true&&c.virtual_branches_are_independent_source_programs===false&&c.maximum_physical_residual<4e-12&&Math.abs(c.total_raw_Bell_probability-1)<4e-12,"bounded actual Bell replay");
  same(c.all_Bell_branches.map(b=>[b.Bell_shift,b.Bell_phase]),points.flatMap(a=>points.map(b=>[a,b])),"every Bell branch, none postselected");
  for(const b of c.all_Bell_branches){const q0=m.residual(b.Bell_shift),q1=m.residual(b.Bell_shift.map((x,j)=>mod(x+v[j],3))),label=q1.map((x,l)=>mod(x-q0[l],3)),answer=mod(label.reduce((t,x,l)=>t+x*s[l],0),3);
    same(b.equation_label,label,"exact equation label");check(b.answer===answer&&b.raw_Bell_probability==="1/"+3n**BigInt(2*m.h),"correct deterministic equation and raw Bell cost");b.Fourier_probabilities.forEach((p,j)=>check(Number.isFinite(p)&&Math.abs(p-Number(j===answer))<4e-12,"physical Fourier probabilities"));bell++;
  }
}
let selectorRows=0;
same(R.complete_line_instrument_compilers.map(x=>x.compiler.width),[1,2,3],"complete line compiler regimes");
for(const c of R.complete_line_instrument_compilers){
  const p=c.compiler,h=p.width,v=p.fixed_public_direction,N=3**h,points=words(h);
  check(c.reference_dimension===2&&c.complete_Bell_branches_checked===N*N&&c.maximum_Kraus_amplitude_residual<4e-12&&Math.abs(c.total_raw_probability-1)<4e-12&&c.packet_is_secret_flat_phase_calibration_only===false,"arbitrary reference-entangled Bell tensor replay");
  check(v.length===h&&v.some(Boolean)&&p.chart_columns.length===h&&p.inverse_chart_rows.length===h&&p.chart_columns.every(col=>col.length===h),"complete public invertible chart");same(p.chart_columns[0],v,"line is first chart direction");
  check(p.Kraus_squared_coefficient_denominator===3*N&&p.public_line_shift_probability==="1/3"&&p.public_Bell_phase_probability==="1/"+BigInt(N)&&p.measured_quotient_registers===h-1,"EXACT random/Kraus normalization and measured wires");
  check(p.same_supplied_packet_consumed===true&&p.arbitrary_packet_density_matrix_and_external_reference_covered===true&&p.affine_phase_or_secret_promise_required===false&&p.arbitrary_unknown_teleported_data_or_multiple_lines_covered===false&&p.classical_simulation_of_quantum_packet_claimed===false,"compiler scope beyond affine, not beyond fixed known data");
  same(p.all_shift_supports.map(x=>x.Bell_shift),points,"ALL Bell shifts in exact support certificate");const counts=new Map(points.map(z=>[key(z),0]));
  for(const record of p.all_shift_supports){
    const a=record.Bell_shift,coords=p.inverse_chart_rows.map(row=>mod(row.reduce((s,x,j)=>s+x*a[j],0),3));
    same(a,Array.from({length:h},(_,i)=>mod(p.chart_columns.reduce((s,col,j)=>s+col[i]*coords[j],0),3)),"chart and inverse on EVERY word");
    let wire=[...a];for(const g of p.chart_gates){if(g.gate==="SWAP_F3")[wire[g.first],wire[g.second]]=[wire[g.second],wire[g.first]];else if(g.gate==="SCALE_F3")wire[g.wire]=mod(wire[g.wire]*g.factor,3);else{check(g.gate==="SUM_F3","known native field gate");wire[g.target]=mod(wire[g.target]+g.factor*wire[g.control],3);}}
    same(wire,coords,"actual public gate recipe is inverse chart");check(record.public_random_line_shift===coords[0],"public random shift t");same(record.measured_quotient,coords.slice(1),"actual quotient measured, not full packet");
    const original=[0,1,2].map(j=>a.map((x,i)=>mod(x+j*v[i],3))),base=Array.from({length:h},(_,i)=>mod(p.chart_columns.slice(1).reduce((s,col,j)=>s+col[i]*coords[j+1],0),3)),compiled=[0,1,2].map(j=>base.map((x,i)=>mod(x+(coords[0]+j)*v[i],3)));
    same(record.original_Kraus_input_words,original,"known-line Bell Kraus selector");same(record.compiled_Kraus_input_words,compiled,"direct projection Kraus selector");same(compiled,original,"exact COMPLETE instrument support equality");original.forEach(z=>counts.set(key(z),counts.get(key(z))+1));selectorRows+=3;
  }
  check(Array.from(counts.values()).every(x=>x===3),"Kraus completeness after ALL uniform Bell phases, not postselected equivalence");
}
console.log(JSON.stringify({status:"PASS",exact_direction_shift_pairs_checked:checks,packet_branches:branches,admitted_direction_controls:admitted,physical_Bell_branches_checked:bell,population_regimes:6,exact_line_Kraus_selector_rows_checked:selectorRows,arbitrary_packet_line_instrument_compiled:true,general_quantum_receiver_lower_bound:false}));
