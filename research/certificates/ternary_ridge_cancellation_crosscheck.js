"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const report=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../phase_workbench/ternary_ridge_cancellation.json"),"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},same=(a,b,m)=>check(JSON.stringify(a)===JSON.stringify(b),m);
const mod=(x,q)=>(x%q+q)%q,words=k=>Array.from({length:3**k},(_,i)=>Array.from({length:k},(_,j)=>Math.floor(i/3**(k-j-1))%3));
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),key=JSON.stringify;
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
function frac(a,b){const g=gcd(a,b);a/=g;b/=g;return b===1n?String(a):a+"/"+b;}
function rref(A,width){
  A=A.map(row=>row.map(x=>mod(x,3)));const pivots=[];let r=0;
  for(let j=0;j<width&&r<A.length;j++){
    const p=A.findIndex((row,i)=>i>=r&&row[j]);if(p<0)continue;
    [A[r],A[p]]=[A[p],A[r]];const inverse=A[r][j];A[r]=A[r].map(x=>x*inverse%3);
    for(let i=0;i<A.length;i++)if(i!==r){const c=A[i][j];A[i]=A[i].map((x,k)=>mod(x-c*A[r][k],3));}pivots.push(j);r++;
  }
  return {rows:A.slice(0,r),pivots,free:Array.from({length:width},(_,i)=>i).filter(i=>!pivots.includes(i))};
}
function chart(level){
  let V=[[1n,0n],[0n,1n]],pi=[[-1n,-1n],[1n,-2n]];
  for(let j=0;j<level-1;j++)V=V.map(row=>pi[0].map((_,i)=>row.reduce((s,a,k)=>s+a*pi[k][i],0n)));
  const q=3n**BigInt(Math.ceil(level/2)),den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]);
  const a=q*(2n*V[1][1]+V[1][0]),b=q*(-2n*V[0][1]-V[0][0]);check(a%den===0n&&b%den===0n,"integral native chart");
  const u=a/den,v=b/den;return label=>{const[x,y]=label.map(BigInt);return[Number(mod(u*x+v*y,q)),Number(mod((u+v)*x-u*y,q))];};
}
function phaseValue(p,z){
  const N=Number(p.numerator_modulus),out=Array(p.components).fill(0);
  for(const g of p.projective_ridge_groups){const t=dot(g.direction,z)%3;g.component_tables.forEach((row,l)=>out[l]+=row[t]);}
  return out.map(x=>{x=mod(x,N);check(x%3===0,"global denominator");return x/3;});
}
function degreeCertificate(p){
  const R=p.phase_digits+1,N=Number(p.numerator_modulus);let maximum=0;
  const diff=row=>row.map((x,i)=>mod(row[(i+1)%3]-x,N));
  function val(x){if(!x)return R;let v=0;while(x%3===0){v++;x/=3;}return v;}
  const groups=p.projective_ridge_groups.map(g=>({direction:g.direction,component_certificates:g.component_tables.map(row=>{
    const a=diff(row),b=diff(a),u=Math.min(...a.map(val)),v=Math.min(...b.map(val)),D=Math.max(0,2*(R-u)-1,2*(R-v));maximum=Math.max(maximum,D);
    return {first_difference_min_valuation:u,second_difference_min_valuation:v,exact_local_additive_degree:D};
  })}));
  return {group_certificates:groups,certified_global_degree_upper:maximum,upper_bound_is_exact_global_degree:false,tensor_entries_expanded:0,basis:"Delta^(2h+1)=(-3)^h*S^h*Delta; Delta^(2h+2)=(-3)^h*S^h*Delta^2"};
}
function checkLedger(c){
  const n=BigInt(c.components),d=BigInt(c.logical_width),P=(3n**d-1n)/2n,B=n*(P-d)+1n,M=(n+d)*(n+1n)**2n;
  check(c.ambient_projective_forms===String(P)&&c.signature_space_dimension_upper===String(B-1n)&&c.guaranteed_cohort_programs===String(B)&&BigInt(c.original_inputs_per_program)===M&&c.full_original_input_cap===String(B*M),"full ambient bound and actual original supply");
  check(c.source_cap_depends_on_phase_depth===false&&c.ambient_width_dependence_exponential===true&&c.polynomial_when_width_O_log_n===true&&c.one_coordinate_stage_is_trivial===(d===1n)&&c.decoder_or_full_depth_speedup_supplied===false,"width exponential, depth-independent source cap, no decoder claim");
}
const hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_RIDGE_CANCELLATION.md"))).digest("hex");
check(report.derivation_sha256===hash&&report.status==="DEPTH_INDEPENDENT_LOW_RIDGE_CANCELLATION_FACTORY_REVIEW_PENDING","pinned derivation");
for(const k of["candidate_record_accepted","full_root_decoder_supplied","quantum_speedup_proved"])check(report[k]===false,"unproved algorithm: "+k);
same(report.native_controls.map(c=>c.seed),[89001,89128,89128,89031],"all prespecified native controls including root loss");
let sourceWords=0,injections=0,sourceLifts=0,exactDrops=0;
for(const c of report.native_controls){
  checkLedger(c.ledger);const n=c.ledger.components,d=c.ledger.logical_width,r=c.merged_phase.phase_digits,q=3**r,N=3*q,B=c.source_programs.length,K=n+d,M=K*(n+1)**2,ws=words(d),ids=[],values=[],pairsList=[],blocksList=[],signatureMaps=[];let exponent=0;
  check(B===Number(c.ledger.guaranteed_cohort_programs)&&c.low_relation.cohort_programs_charged===B,"whole guaranteed cohort");
  for(const p of c.source_programs){
    const s=p.source,at=chart(2*r+2),pairs=p.original_labels.map(row=>{const f=row.map(at);return[f.map(x=>x[0]),f.map(x=>x[1])];});
    check(s.original_even_level===2*r+2&&s.parent_modulus===String(N)&&s.dimension===n&&s.acquired_original_native_inputs===M&&s.odd_inputs_acquired===K,"original native root and dimensions");
    same(p.original_frequency_pairs,pairs,"actual native ring-frequency chart");ids.push(...s.original_source_ids);pairsList.push(pairs);
    check(s.original_source_ids.length===M&&s.distinct_ids_certify_physical_independence===false&&p.IID_full_depth_output_label_law_proved===false,"identity is not physical IID supply");
    const index=new Map(s.original_source_ids.map((id,i)=>[id,i])),blocks=s.odd_input_original_ancestors.map(row=>row.map(id=>index.get(id)));blocksList.push(blocks);
    check(blocks.length===K&&blocks.every((block,j)=>block.length&&block.every(i=>Number.isInteger(i)&&i>=j*(n+1)**2&&i<(j+1)*(n+1)**2)),"fixed independent windows");
    const active=blocks.flat(),base=p.original_affine_base,columns=p.original_affine_columns;
    check(new Set(active).size===active.length&&s.active_original_inputs===active.length&&s.untouched_original_inputs===M-active.length,"active and unused source ledger");
    same(s.active_original_source_ids,active.map(i=>s.original_source_ids[i]),"actual active ancestry");
    check(base.length===M&&columns.length===d&&[base,...columns].every(row=>row.length===M&&row.every(x=>Number.isInteger(x)&&[0,1,2].includes(x))),"canonical original affine map");
    const anchor=Array(M).fill(0),physicalBase=blocks.map(block=>base[block[0]]);
    for(const block of blocks){
      for(const i of block)anchor[i]=mod(base[i]-base[block[0]],3);
      for(let l=0;l<n;l++)check(mod(block.reduce((sum,i)=>sum+pairs[i][0][l]+pairs[i][1][l],0),3)===0,"curvature-only zero support");
    }
    for(let i=0;i<M;i++)if(!active.includes(i))check(base[i]===0&&columns.every(col=>col[i]===0),"untouched original factors excluded, not silently measured");
    const atDigit=(i,t,l)=>t?pairs[i][t-1][l]:0,odd=blocks.map(block=>[1,2].map(t=>Array.from({length:n},(_,l)=>mod(block.reduce((sum,i)=>sum+atDigit(i,mod(anchor[i]+t,3),l)-atDigit(i,anchor[i],l),0),N))));
    const gaussian=rref(Array.from({length:n},(_,l)=>odd.map(pair=>pair[0][l]%3)),K);
    check(gaussian.free.length>=d,"actual retained free width");
    const expectedColumns=Array.from({length:d},(_,j)=>{
      const t=Array(K).fill(0);t[gaussian.free[j]]=1;gaussian.pivots.forEach((pivot,k)=>t[pivot]=mod(-gaussian.rows[k][gaussian.free[j]],3));
      const out=Array(M).fill(0);blocks.forEach((block,k)=>block.forEach(i=>out[i]=t[k]));return out;
    });same(columns,expectedColumns,"low-defined first-d Gaussian source frame");
    const value=(z,replacement=pairs)=>Array.from({length:n},(_,l)=>{
      let total=0;for(let i=0;i<M;i++){const t=mod(base[i]+columns.reduce((sum,col,j)=>sum+col[i]*z[j],0),3),b=base[i];total+=(t?replacement[i][t-1][l]:0)-(b?replacement[i][b-1][l]:0);}
      total=mod(total,N);check(total%3===0,"true original-root residual divisibility");return total/3;
    });values.push(value);
    for(const z of ws){same(phaseValue(p.compact_phase,z),value(z),"compact program equals original frequencies");sourceWords++;}
    const dictionary=new Map();for(const group of p.compact_phase.projective_ridge_groups){
      const coefficients=group.component_tables.map(row=>row[1]%3);
      if(coefficients.some(Boolean))dictionary.set(key(group.direction),coefficients);
      for(const row of group.component_tables)check(row[0]===0&&mod(row[2]-2*row[1],3)===0,"native low linearity");
    }signatureMaps.push(dictionary);
    exponent+=active.length-d;check(p.raw_source_program_branch_probability===frac(1n,3n**BigInt(active.length-d)),"source pointer/syndrome/complement mass");
  }
  check(new Set(ids).size===ids.length&&ids.length===Number(c.ledger.full_original_input_cap)&&c.full_original_input_cap_charged===ids.length,"no reused ancestors or uncharged programs");
  const keys=[...new Set(signatureMaps.flatMap(map=>[...map.keys()]))].sort(),directions=keys.map(JSON.parse),rows=[];
  for(let l=0;l<n;l++)for(const k of keys)rows.push(signatureMaps.map(map=>(map.get(k)||Array(n).fill(0))[l]));
  const A=rref(rows,B),span=keys.length?rref(Array.from({length:d},(_,j)=>directions.map(v=>v[j])),keys.length).pivots.length:0;
  same(c.low_relation.occupied_signature_directions,directions,"only occupied LOW signature keys");
  same(c.low_relation.signature_rows,rows.map((program_coefficients,i)=>({component:Math.floor(i/keys.length),direction:directions[i%keys.length],program_coefficients})),"all actual low relation rows");
  check(c.low_relation.signature_matrix_rank===A.pivots.length&&c.low_relation.occupied_direction_span_rank===span&&c.low_relation.observed_signature_space_dimension_upper===n*(keys.length-span)&&c.low_relation.ambient_signature_space_dimension_upper===c.ledger.signature_space_dimension_upper&&A.pivots.length<=n*(keys.length-span),"present-cohort and ambient kernel dimensions");
  const kernel=A.free.map(f=>{const v=Array(B).fill(0);v[f]=1;A.pivots.forEach((p,i)=>v[p]=mod(-A.rows[i][f],3));return v;});
  check(kernel.length>0,"nonzero low relation exists");let coefficients=kernel[0];for(const v of kernel)if(v.filter(Boolean).length>coefficients.filter(Boolean).length)coefficients=v;
  same(c.coefficients,coefficients,"deterministic low-only maximum-support selector");same(c.low_relation.coefficients,coefficients,"same proof relation");
  check(c.low_relation.reads_only_native_low_signature_residues===true&&c.low_relation.high_frequency_digits_or_measured_injection_words_read_for_selection===false&&c.low_relation.sparse_occupied_bound_guarantees_future_cohorts===false&&c.low_relation.all_ambient_projective_forms_materialized===false,"no high-dependent or future sparse-space premise");
  const selected=coefficients.map((x,j)=>x?j:-1).filter(j=>j>=0);same(c.selected_program_indices,selected,"one-use consumption");
  const aggregate=new Map();
  for(let k=0;k<selected.length;k++){
    const j=selected[k],sign=coefficients[j],m=c.injection_outcomes[k];
    for(const group of c.source_programs[j].compact_phase.projective_ridge_groups){
      const id=key(group.direction),offset=dot(group.direction,m)%3,tables=aggregate.get(id)||Array.from({length:n},()=>[0,0,0]);
      for(let l=0;l<n;l++){
        const row=group.component_tables[l];for(let a=0;a<3;a++)check(mod(row[(a+sign)%3]-row[a],3)===sign*(row[1]%3)%3,"signed signature is independent of EVERY injection offset");
        for(let t=0;t<3;t++)tables[l][t]=mod(tables[l][t]+row[(offset+sign*t)%3]-row[offset],N);
      }aggregate.set(id,tables);
    }
  }
  const expected=[...aggregate].filter(([_,tables])=>tables.some(row=>row.some(Boolean))).map(([direction,component_tables])=>({direction:JSON.parse(direction),component_tables})).sort((a,b)=>key(a.direction).localeCompare(key(b.direction)));
  same(c.merged_phase.projective_ridge_groups,expected,"native signed merge and exact per-group division");
  check(expected.every(g=>g.component_tables.every(row=>row.every(x=>x%3===0)))&&c.per_ridge_denominator_division_admitted===true,"low relation permits individual division only now");
  const value=(z,replacement)=>Array.from({length:n},(_,l)=>mod(selected.reduce((sum,j,k)=>{
    const m=c.injection_outcomes[k],x=m.map((a,i)=>mod(a+coefficients[j]*z[i],3)),pairs=replacement&&replacement.j===j?replacement.pairs:undefined;
    return sum+values[j](x,pairs)[l]-values[j](m,pairs)[l];
  },0),q));
  const table=ws.map(z=>value(z));same(c.complete_frequency_table,table,"complete phase table from original native inputs");
  for(let i=0;i<ws.length;i++)same(phaseValue(c.merged_phase,ws[i]),table[i],"source-accounted compact cancellation");
  const certificate=degreeCertificate(c.merged_phase);same(c.degree_certificate,certificate,"exact local degree certificate");check(certificate.certified_global_degree_upper<=2*r&&c.top_degree_identity.status==="EXACT_FACTORED_IDENTITY"&&c.top_degree_identity.identity_algebraically_certified===true,"depth-independent degree drop, not a randomized claim");exactDrops++;
  const familyGcd=table.flat().reduce((a,b)=>Number(gcd(BigInt(a),BigInt(b))),q);check(c.component_frequency_family_order===String(q/familyGcd),"full component family order, not just a modulus label");
  if(c.unit_frequency_word_witness){const w=c.unit_frequency_word_witness;check(value(w.word)[w.component]===w.frequency&&w.frequency%3!==0,"real full-root unit word witness");}
  check(c.raw_source_program_transcript_probability===frac(1n,3n**BigInt(exponent))&&c.conditional_injection_transcript_probability===frac(1n,3n**BigInt(d*selected.length)),"combined supply and conditional injection masses");
  check(c.conditional_full_phase_order_loss_upper===frac(1n,3n**BigInt(n*d))&&c.physical_source_IID_premise_verified===false&&c.full_phase_order_of_every_branch_guaranteed===false&&c.full_root_secret_identifiability_proved===false&&c.ordinary_field3_readout_or_phase_power_oracle_supplied===false&&c.uniform_linear_coefficient_law_is_mod3_only===true,"conditional ensemble law is not a decoder/phase oracle");
  check(c.physical_injection_controls.length===selected.length&&c.all_injection_outcomes_accepted===true&&c.each_selected_program_consumed_once===true&&c.unknown_inverse_conjugation_or_cloning_used===false,"physical one-use recipe");
  for(const x of c.physical_injection_controls){check(x.all_injection_outcomes===3**d&&x.conditional_branch_probability===frac(1n,3n**BigInt(d))&&Number.isFinite(x.arbitrary_reference_entangled_max_error)&&x.arbitrary_reference_entangled_max_error>=0&&x.arbitrary_reference_entangled_max_error<4e-12,"complete entangled SUM replay");injections+=3**d;}
  const read=c.program_only_lowest_digit_readout,H=q/3,g=3**n,fibers=new Map();let radicalNumerator=0,collisions=0;
  for(let i=0;i<ws.length;i++){const id=key(table[i].map(x=>x%H));if(!fibers.has(id))fibers.set(id,[]);fibers.get(id).push(i);}
  const fiberRecords=[...fibers].sort(([a],[b])=>a.localeCompare(b)).map(([coarse,indices])=>{
    const base=table[indices[0]],counts=new Map();for(const i of indices){const id=key(table[i].map((x,l)=>mod(x-base[l],q)/H));counts.set(id,(counts.get(id)||0)+1);}
    radicalNumerator+=[...counts.values()].reduce((sum,count)=>sum+Math.sqrt(count),0)**2;collisions+=indices.length*(indices.length-1);
    return {coarse_frequency:JSON.parse(coarse),fiber_words:indices.map(i=>ws[i]),fine_label_counts:[...counts].sort(([a],[b])=>a.localeCompare(b)).map(([label,count])=>({label:JSON.parse(label),count}))};
  });
  same(read.coarse_fibers,fiberRecords,"exact partial-secret high-digit twirl fibers");
  check(read.program_dimension===3**d&&read.coarse_modulus===String(H)&&read.secret_digit_outcomes===String(g)&&read.ordered_distinct_coarse_collisions===collisions&&Math.abs(read.ideal_optimal_lowest_digit_success-radicalNumerator/(g*3**d))<4e-12&&read.chance_success===frac(1n,BigInt(g)),"abelian PGM/dual optimum, not whole-secret success");
  check(read.reference_only_not_efficient_measurement_implementation===true&&read.other_live_original_registers_excluded===true&&read.high_secret_twirl_not_tensor_of_independent_per_program_twirls===true,"program-only prior and scope");
  const pop=c.program_only_population_bound,capNum=BigInt(3**d-1),capDen=BigInt(q)**BigInt(n),gBig=BigInt(g),clipped=capNum*gBig>(gBig-1n)*capDen;
  check(pop.mean_optimal_lowest_digit_advantage_upper===(clipped?frac(gBig-1n,gBig):frac(capNum,capDen))&&pop.population_bound_applies_to_each_fixed_instance===false&&pop.same_shared_higher_secret_across_outputs===true&&pop.unused_original_registers_or_additional_outputs_covered===false,"two-point population bound, shared nuisance secret, no global no-go");
  if(c.original_linear_source_census){
    const census=c.original_linear_source_census,j=census.varied_program,kCount=K,lifts=words(K),zero=Array(d).fill(0),baseTable=table;
    check(census.records.length===3**K&&census.complete_original_high_lifts===3**K&&census.retained_phase_digits===r&&census.virtual_lifts_are_additional_quantum_samples===false&&census.finite_census_certifies_physical_IID_premise===false,"virtual original source census");
    const hist=new Map();
    for(let k=0;k<lifts.length;k++){
      const row=census.records[k],replacement=pairsList[j].map(pair=>pair.map(a=>[...a]));same(row.original_pivot_lifts,lifts[k],"every original high lift");
      blocksList[j].forEach((block,i)=>{const pivot=block[0];replacement[pivot][0][0]=mod(replacement[pivot][0][0]+3*lifts[k][i],N);replacement[pivot][1][0]=mod(replacement[pivot][1][0]+6*lifts[k][i],N);});
      const delta=ws.map((z,i)=>value(z,{j,pairs:replacement}).map((x,l)=>mod(x-baseTable[i][l],3))),beta=Array.from({length:d},(_,i)=>{const e=[...zero];e[i]=1;return delta[ws.findIndex(z=>key(z)===key(e))][0];});
      same(row.component_zero_linear_change_mod3,beta,"mod3 beta from true original high frequencies");
      for(let i=0;i<ws.length;i++)same(delta[i],[dot(beta,ws[i])%3,...Array(n-1).fill(0)],"alpha changes only the linear part, not the quadratic part");
      const id=key(beta);hist.set(id,(hist.get(id)||0)+1);sourceLifts++;
    }
    check(hist.size===3**d&&[...hist.values()].every(x=>x===3**(K-d))&&census.linear_change_multiplicity===3**(K-d),"uniform mod3 linear coefficient census");
  }
}
for(const c of report.cohort_ledgers)checkLedger(c);
check(report.native_controls[0].one_coordinate_control_is_trivial===true&&report.native_controls[0].component_frequency_family_order==="1"&&report.native_controls[0].unit_frequency_word_witness===null,"retained negative root-loss control, not filtered away");
console.log(JSON.stringify({status:"independent_depth_independent_ridge_cancellation_certificates_passed",originalRootWords:sourceWords,oneUseInjectionBranches:injections,originalHighLiftControls:sourceLifts,exactDegreeDrops:exactDrops,fullRootDecoder:false}));
