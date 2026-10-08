"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const report=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../phase_workbench/ternary_cubic_program_factory.json"),"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},same=(a,b,m)=>check(JSON.stringify(a)===JSON.stringify(b),m);
const mod=(a,q)=>(a%q+q)%q,words=k=>Array.from({length:3**k},(_,i)=>Array.from({length:k},(_,j)=>Math.floor(i/3**(k-j-1))%3));
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),key=JSON.stringify;
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
function frac(a,b){const g=gcd(a,b);a/=g;b/=g;return b===1n?String(a):a+"/"+b;}
function chart(level){
  let V=[[1n,0n],[0n,1n]],pi=[[-1n,-1n],[1n,-2n]];
  for(let j=0;j<level-1;j++)V=V.map(row=>pi[0].map((_,i)=>row.reduce((s,a,k)=>s+a*pi[k][i],0n)));
  const q=3n**BigInt(Math.ceil(level/2)),den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]);
  const a=q*(2n*V[1][1]+V[1][0]),b=q*(-2n*V[0][1]-V[0][0]);
  check(a%den===0n&&b%den===0n,"integral chart");const u=a/den,v=b/den;
  return label=>{const[x,y]=label.map(BigInt);return[Number(mod(u*x+v*y,q)),Number(mod((u+v)*x-u*y,q))];};
}
function rref(A){
  A=A.map(row=>row.map(x=>mod(x,3)));const pivots=[];let r=0;
  for(let j=0;j<A[0].length&&r<A.length;j++){
    const p=A.findIndex((row,i)=>i>=r&&row[j]);if(p<0)continue;
    [A[r],A[p]]=[A[p],A[r]];A[r]=A[r].map(x=>x*A[r][j]%3);
    for(let i=0;i<A.length;i++)if(i!==r){const c=A[i][j];A[i]=A[i].map((x,k)=>mod(x-c*A[r][k],3));}
    pivots.push(j);r++;
  }
  return {rows:A.slice(0,r),pivots,free:Array.from({length:A[0].length},(_,i)=>i).filter(i=>!pivots.includes(i))};
}
function interpolate(table,d){
  const ws=words(d),index=new Map(ws.map((w,i)=>[key(w),i])),I=[[1,0,0],[0,2,1],[2,2,2]];let out=table.map(row=>[...row]);
  for(let axis=0;axis<d;axis++){
    const next=out.map(row=>[...row]);
    for(const w of ws)for(let l=0;l<table[0].length;l++){
      const value=[0,1,2].reduce((s,x)=>{const p=[...w];p[axis]=x;return s+I[w[axis]][x]*out[index.get(key(p))][l];},0);
      next[index.get(key(w))][l]=mod(value,3);
    }out=next;
  }return out;
}
function poly(p,z){return p.component_polynomials.map(row=>mod(row.reduce((s,t)=>s+t.coefficient*t.powers.reduce((a,e,i)=>a*z[i]**e,1),0),3));}
const even=chart(4),hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_CUBIC_PROGRAM_FACTORY.md"))).digest("hex");
check(report.derivation_sha256===hash&&report.status==="UNMATCHED_NATIVE_CUBIC_PROGRAM_FACTORY_FIXED_ROOT_REVIEW_PENDING","pinned scope");
check(report.candidate_record_accepted===false&&report.growing_depth_speedup_proved===false,"no breakthrough claim");
same(report.native_controls.map(c=>c.seed),[88705,88707,88708],"all prespecified nontrivial controls");
let rootWords=0,injections=0,Bells=0,sourceLifts=0;
for(const c of report.native_controls){
  const n=c.calibration_secret.length,d=c.programs[0].retained_width,ws=words(d),R=n*((d+2)*(d+1)*d/6-d),ids=[],values=[],supports=[];
  check(c.programs.length===R+1&&c.cohort_programs_charged===R+1&&c.cubic_feature_dimension===R&&c.guaranteed_cohort_size===R+1,"entire cohort charged");
  let sourceExponent=0,originals=0;
  for(const p of c.programs){
    const s=p.source,K=d+n,W=(n+1)**2,M=K*W;
    check(s.original_even_level===4&&s.dimension===n&&s.acquired_original_native_inputs===M&&p.original_labels.length===M&&s.odd_inputs_acquired===K,"actual original source cap");
    check(p.retained_width===d&&p.frame_policy==="first-d-free-Gaussian-coordinates-low-only"&&p.all_source_measurement_outcomes_accepted===true&&p.upstream_input_supply_and_hardware_error_proved===false,"source policy and unresolved supply");
    check(s.distinct_ids_certify_physical_independence===false&&s.original_source_ids.length===M,"IDs not an IID certificate");ids.push(...s.original_source_ids);originals+=M;
    const pairs=p.original_labels.map(row=>{const f=row.map(even);return[Array.from({length:n},(_,l)=>f[l][0]),Array.from({length:n},(_,l)=>f[l][1])];});
    same(p.original_frequency_pairs,pairs,"native ring frequency reconstruction");
    const idIndex=new Map(s.original_source_ids.map((id,i)=>[id,i])),blocks=s.odd_input_original_ancestors.map(row=>row.map(id=>idIndex.get(id)));
    check(blocks.length===K&&blocks.every((b,j)=>b.length&&b.every(i=>Number.isInteger(i)&&i>=j*W&&i<(j+1)*W)),"disjoint fixed windows");
    const active=blocks.flat();same(s.active_original_source_ids,active.map(i=>s.original_source_ids[i]),"active ancestry");
    check(new Set(active).size===active.length&&s.active_original_inputs===active.length&&s.untouched_original_inputs===M-active.length,"untouched inputs");
    same(s.untouched_original_source_ids,s.original_source_ids.filter((_,i)=>!active.includes(i)),"unused original ancestors");
    const anchor=Array(M).fill(0);let pointer=0;
    for(const block of blocks){
      for(let l=0;l<n;l++)check(mod(block.reduce((a,i)=>a+pairs[i][0][l]+pairs[i][1][l],0),3)===0,"curvature zero support");
      for(const i of block.slice(1))anchor[i]=p.inner_pointers[pointer++];
    }check(pointer===p.inner_pointers.length,"all measured pointer digits");
    const at=(i,t,l)=>t?pairs[i][t-1][l]:0;
    const odd=blocks.map(block=>[1,2].map(t=>Array.from({length:n},(_,l)=>mod(block.reduce((a,i)=>a+at(i,mod(anchor[i]+t,3),l)-at(i,anchor[i],l),0),9))));
    const low=Array.from({length:n},(_,l)=>odd.map(pair=>pair[0][l]%3)),G=rref(low),H=G.free.length;
    check(H>=d&&p.restriction_complement.length===H-d&&p.outer_syndrome.length===G.pivots.length,"actual Gaussian retention");
    const assignment=z=>{const t=Array(K).fill(0);G.free.forEach((f,j)=>t[f]=z[j]);G.pivots.forEach((f,j)=>t[f]=mod(p.outer_syndrome[j]-dot(G.rows[j],t),3));return t;};
    const lift=z=>{const t=assignment([...z,...p.restriction_complement]),x=[...anchor];blocks.forEach((b,j)=>b.forEach(i=>x[i]=mod(x[i]+t[j],3)));return x;};
    const base=lift(Array(d).fill(0)),columns=Array.from({length:d},(_,j)=>lift(Array.from({length:d},(_,i)=>Number(i===j))).map((x,i)=>mod(x-base[i],3)));
    same(p.original_affine_base,base,"original branch base");same(p.original_affine_columns,columns,"low-defined physical free frame");
    const value=(z,replacement=pairs)=>Array.from({length:n},(_,l)=>{
      let difference=0;
      for(let i=0;i<M;i++){const t=mod(base[i]+columns.reduce((a,col,j)=>a+col[i]*z[j],0),3),b=base[i];difference+=(t?replacement[i][t-1][l]:0)-(b?replacement[i][b-1][l]:0);}
      difference=mod(difference,9);check(difference%3===0,"actual original root divisibility");return difference/3;
    });
    const table=ws.map(z=>value(z)),coeff=interpolate(table,d);
    for(let i=0;i<ws.length;i++)same(poly(p,ws[i]),table[i],"public polynomial equals original phases");
    check(coeff.every((row,i)=>dot(ws[i],Array(d).fill(1))<=3||row.every(x=>x===0)),"ordinary cubic degree bound");
    for(let i=0;i<d;i++)for(let j=i;j<d;j++)for(let k=j;k<d;k++)if(i!==k){
      const powers=Array(d).fill(0);powers[i]++;powers[j]++;powers[k]++;
      const wi=ws.findIndex(w=>key(w)===key(powers)),factor=i===j||j===k?2:1;
      for(let l=0;l<n;l++){
        const lowTop=mod(-factor*blocks.reduce((sum,b,h)=>sum+low[l][h]*columns[i][b[0]]*columns[j][b[0]]*columns[k][b[0]],0),3);
        check(coeff[wi][l]===lowTop,"cubic signature depends only on true native low rows and frame");
      }
    }
    sourceExponent+=active.length-d;check(p.raw_program_branch_probability===frac(1n,3n**BigInt(active.length-d)),"all original measured wires charged");
    check(p.public_residual_evaluations_for_polynomial===2*d+d*(d-1)/2,"polynomial public evaluation count");
    values.push({value,pairs,blocks,coeff});supports.push(blocks);rootWords+=ws.length;
  }
  check(new Set(ids).size===ids.length&&ids.every(x=>typeof x==="string"&&x.length),"globally disjoint original ancestry");
  const coefficients=c.coefficients,selected=coefficients.map((x,i)=>x?i:-1).filter(i=>i>=0);
  check(coefficients.length===values.length&&coefficients.every(x=>Number.isInteger(x)&&[0,1,2].includes(x))&&selected.length>=2&&coefficients.includes(2),"nontrivial signed field relation");
  same(c.selected_program_indices,selected,"consumed programs");
  for(let i=0;i<ws.length;i++)if(ws[i].reduce((a,b)=>a+b,0)===3)for(let l=0;l<n;l++)check(mod(dot(coefficients,values.map(v=>v.coeff[i][l])),3)===0,"actual cubic top cancellation");
  for(const j of selected)for(const m of ws){
    const shifted=interpolate(ws.map(z=>values[j].value(m.map((a,i)=>mod(a+coefficients[j]*z[i],3)))),d);
    for(let wi=0;wi<ws.length;wi++)if(ws[wi].reduce((a,b)=>a+b,0)===3)for(let l=0;l<n;l++)
      check(shifted[wi][l]===mod(coefficients[j]*values[j].coeff[wi][l],3),"top cancellation survives EVERY injection shift with domain signs");
  }
  check(c.selection_reads_high_linear_or_quadratic_coefficients===false&&c.unselected_programs_claimed_fresh_IID===false&&c.physical_IID_independence_proved_by_ancestry_ids===false,"low-only relation/source qualifications");
  same(c.injection_gates,selected.map(j=>({gate:"SUM_F3",control:"data",target_program:j,factor:mod(-coefficients[j],3)})),"signed domain SUM consumes one program");
  check(c.all_injection_outcomes_accepted===true&&c.each_selected_program_consumed_once===true&&c.cloning_conjugate_program_or_unknown_inverse_used===false,"physical one-use contract");
  check(c.original_native_inputs_charged===originals&&c.original_source_measurement_branch_probability===frac(1n,3n**BigInt(sourceExponent))&&c.conditional_one_injection_transcript_probability===frac(1n,3n**BigInt(d*selected.length))&&c.raw_source_and_injection_transcript_probability===frac(1n,3n**BigInt(sourceExponent+d*selected.length)),"combined source and injection branch ledger");
  const summed=(z,replacement)=>Array.from({length:n},(_,l)=>mod(selected.reduce((a,j,k)=>{
    const m=c.injection_outcomes[k],x=m.map((t,i)=>mod(t+coefficients[j]*z[i],3));
    return a+values[j].value(x,replacement&&replacement.j===j?replacement.pairs:undefined)[l]-values[j].value(m,replacement&&replacement.j===j?replacement.pairs:undefined)[l];
  },0),3));
  const table=ws.map(z=>summed(z));same(c.complete_factory_frequency_table,table,"quadratic Choi from actual original roots");
  for(let zi=0;zi<ws.length;zi++){
    const z=ws[zi],quadratic=c.component_matrices.map((A,l)=>mod(A.reduce((a,row,i)=>a+z[i]*dot(row,z),0)+dot(c.component_linear[l],z),3));
    same(quadratic,table[zi],"recomputed quadratic matrices and offsets");
  }
  const B=c.complete_injection_tensor_branches;check(B===selected.length*3**d&&Number.isFinite(c.arbitrary_reference_entangled_injection_max_error)&&c.arbitrary_reference_entangled_injection_max_error>=0&&c.arbitrary_reference_entangled_injection_max_error<4e-12,"bounded actual entangled injection replay");injections+=B;
  check(c.complete_original_root_words===(R+1)*3**d&&c.source_theorem_review_status==="LOCAL_DERIVATION_REVIEW_PENDING"&&c.growing_depth_speedup_proved===false,"finite calibration and scoped theorem");
  if(c.bounded_receiver_admitted){
    const receiver=c.physical_receiver,v=receiver.receiver.direction;
    check(v.some(Boolean)&&c.component_matrices.every(A=>mod(A.reduce((a,row,i)=>a+v[i]*dot(row,v),0),3)===0)&&c.isotropic_search.direction_selection_reads_linear_coefficients===false,"matrix-only common isotope");
    check(receiver.all_Bell_branches.length===3**(2*d),"all Bell outcomes");
    for(let bi=0;bi<ws.length;bi++)for(let ai=0;ai<ws.length;ai++){
      const a=ws[ai],b=ws[bi],row=receiver.all_Bell_branches[bi*ws.length+ai],label=c.component_matrices.map((M,l)=>mod(dot(c.component_linear[l],v)+2*M.reduce((x,r,i)=>x+a[i]*dot(r,v),0),3)),answer=mod(dot(c.calibration_secret,label),3);
      same(row.Bell_shift,a,"Bell shift");same(row.Bell_phase,b,"Bell phase");same(row.public_equation_label,label,"source equation label");
      check(row.answer===answer&&row.raw_Bell_probability===frac(1n,3n**BigInt(2*d)),"exact equation and Bell mass");
      const line=[0,1,2].map(j=>mod(dot(c.calibration_secret,summed(a.map((x,i)=>mod(x+j*v[i],3)))),3));
      check(mod(line[1]-line[0],3)===answer&&mod(line[2]-line[0],3)===2*answer%3,"actual source phase affine on isotope");
      check(row.all_Fourier_probabilities.every((x,i)=>Number.isFinite(x)&&Math.abs(x-Number(i===answer))<4e-12),"exact Fourier equation replay");Bells++;
    }
  }
  if(c.original_linear_source_census){
    const census=c.original_linear_source_census,j=census.varied_program_index,K=d+n,index=new Map(ws.map((w,i)=>[key(w),i])),hist=new Map();
    check(census.source_lifts.length===3**K&&census.complete_original_pivot_lifts===3**K&&census.virtual_lifts_are_additional_physical_samples===false&&census.physical_IID_source_premise_certified===false,"virtual conditional source census");
    const lifts=words(K);
    for(let k=0;k<lifts.length;k++){
      const row=census.source_lifts[k],replacement=values[j].pairs.map(pair=>pair.map(x=>[...x]));same(row.original_pivot_linear_lifts,lifts[k],"every original pivot alpha lift");
      supports[j].forEach((block,i)=>{const p=block[0];replacement[p][0][0]=mod(replacement[p][0][0]+3*lifts[k][i],9);replacement[p][1][0]=mod(replacement[p][1][0]+6*lifts[k][i],9);});
      const coefficients=interpolate(ws.map(z=>summed(z,{j,pairs:replacement})),d),beta=Array.from({length:d},(_,i)=>coefficients[index.get(key(Array.from({length:d},(_,k)=>Number(k===i))))][0]);
      same(row.component_zero_linear,beta,"source-law beta from true original frequencies");
      for(let wi=0;wi<ws.length;wi++)if(ws[wi].reduce((a,b)=>a+b,0)===2)same(coefficients[wi],interpolate(table,d)[wi],"alpha leaves quadratic matrices unchanged");
      const kbeta=key(beta);hist.set(kbeta,(hist.get(kbeta)||0)+1);sourceLifts++;
    }
    check(hist.size===3**d&&[...hist.values()].every(x=>x===3**(K-d))&&census.linear_vector_multiplicity===3**(K-d)&&census.quadratic_matrices_unchanged===true,"uniform full beta image without rank premise");
  }
}
const census=report.source_chart_census;check(census.complete_conditioned_original_frequency_pairs_checked===243&&census.conditioned_pivot_controls.length===9&&census.IID_input_premise_certified_by_finite_census===false,"pivot chart census, not IID certification");
for(let curvature=0;curvature<3;curvature++)for(let pointer=0;pointer<3;pointer++){
  const actual=[];
  for(let a=0;a<9;a++)for(let c=0;c<9;c++)if((a+c)%3===curvature){
    const phase=[0,0,mod(-curvature,3)],A=mod(a+phase[(pointer+1)%3]-phase[pointer],9),C=mod(c+phase[(pointer+2)%3]-phase[pointer],9),ell=A%3;
    actual.push([ell,(A-ell)/3,mod(C-2*A,9)/3]);
  }
  actual.sort((a,b)=>key(a).localeCompare(key(b)));same(actual,words(3),"actual conditioned even pivot to odd high chart bijection");
  const row=census.conditioned_pivot_controls[curvature*3+pointer];same(row.odd_chart_words,actual,"all chart words");check(row.curvature===curvature&&row.pointer===pointer&&row.multiplicity===1,"all pointer/curvature controls");
}
same(report.cost_ledgers.map(c=>c.dimension),[1,2,8,32],"cost schedule");
for(const c of report.cost_ledgers){
  const n=BigInt(c.dimension),d=(n+1n)**3n-n,R=n*((d+2n)*(d+1n)*d/6n-d),originals=(R+1n)*(d+n)*(n+1n)**2n;
  check(BigInt(c.guaranteed_isotropic_width)===d&&BigInt(c.cubic_features)===R&&BigInt(c.cohort_program_cap)===R+1n&&c.original_native_input_cap_per_equation===String(originals)&&c.original_native_input_cap_for_n_plus_8_equations===String((n+8n)*originals)&&c.asymptotic_input_cap_degree_in_n===15,"exact polynomial field-root input caps");
  check(c.dense_relation_matrix_field_entries===String(R*(R+1n))&&c.dense_relation_elimination_field_operation_scale===String(R*R*(R+1n))&&c.asymptotic_dense_relation_memory_degree_in_n===20&&c.asymptotic_dense_relation_elimination_degree_in_n===30&&c.field_operation_scale_is_tight_gate_count===false,"dense public linear algebra is expensive and charged symbolically");
  check(c.fixed_root_original_input_cap_polynomial===true&&c.known_fixed_root_sieves_already_polynomial===true&&c.growing_depth_tensor_or_copy_cost_polynomial===false&&c.full_modulus_recovery_or_cryptographic_reduction_supplied===false,"no fixed-root to full-depth promotion");
}
console.log(JSON.stringify({status:"independent_unmatched_native_cubic_factory_certificates_passed",originalRootWords:rootWords,oneUseInjectionBranches:injections,BellBranches:Bells,originalHighLiftControls:sourceLifts,growingDepthSpeedup:false}));
