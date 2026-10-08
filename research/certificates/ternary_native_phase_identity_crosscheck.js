"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const report=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../phase_workbench/ternary_native_phase_identity.json"),"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},same=(a,b,m)=>check(JSON.stringify(a)===JSON.stringify(b),m);
const mod=(x,q)=>(x%q+q)%q,words=k=>Array.from({length:3**k},(_,i)=>Array.from({length:k},(_,j)=>Math.floor(i/3**(k-j-1))%3));
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),key=JSON.stringify;
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
function frac(a,b){const g=gcd(a,b);a/=g;b/=g;return b===1n?String(a):a+"/"+b;}
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
  return out.map(x=>{x=mod(x,N);check(x%3===0,"shared global denominator3");return x/3;});
}
function diff(table,N){return table.map((x,i)=>mod(table[(i+1)%3]-x,N));}
function degreeCertificate(p){
  const R=p.phase_digits+1,N=Number(p.numerator_modulus);let maximum=0;
  function valuation(x){if(!x)return R;let v=0;while(x%3===0){v++;x/=3;}return v;}
  const groups=p.projective_ridge_groups.map(g=>({direction:g.direction,component_certificates:g.component_tables.map(row=>{
    const first=diff(row,N),second=diff(first,N),u=Math.min(...first.map(valuation)),v=Math.min(...second.map(valuation)),degree=Math.max(0,2*(R-u)-1,2*(R-v));maximum=Math.max(maximum,degree);
    return {first_difference_min_valuation:u,second_difference_min_valuation:v,exact_local_additive_degree:degree};
  })}));
  return {group_certificates:groups,certified_global_degree_upper:maximum,upper_bound_is_exact_global_degree:false,tensor_entries_expanded:0,basis:"Delta^(2h+1)=(-3)^h*S^h*Delta; Delta^(2h+2)=(-3)^h*S^h*Delta^2"};
}
function validatePhase(p){
  const d=p.width,n=p.components,r=p.phase_digits,N=3**(r+1),keys=[];
  check(p.phase_modulus===String(3**r)&&p.numerator_modulus===String(N)&&p.exact_shared_denominator===3&&p.additive_degree_bound===2*r+1,"native modulus and proven class bound");
  check(p.high_degree_tensor_expanded===false&&p.unknown_weighted_phase_oracle_supplied===false,"public compact evaluator, no unknown oracle");
  for(const g of p.projective_ridge_groups){
    check(g.direction.length===d&&g.direction.every(x=>Number.isInteger(x)&&[0,1,2].includes(x))&&g.direction.find(Boolean)===1,"canonical projective direction");keys.push(key(g.direction));
    check(g.component_tables.length===n,"all components");
    for(const row of g.component_tables){
      check(row.length===3&&row[0]===0&&row.every(x=>Number.isInteger(x)&&x>=0&&x<N)&&mod(row[2]-2*row[1],3)===0,"normalized native low-linear table");
      let derivative=[...row];for(let k=0;k<2*r+2;k++)derivative=diff(derivative,N);
      check(derivative.every(x=>x===0),"actual local class degree bound");
    }
  }
  check(new Set(keys).size===keys.length&&p.stored_local_frequency_entries===3*n*keys.length,"merged keys and stored scalar cost");
  for(let l=0;l<n;l++)for(let j=0;j<d;j++)check(mod(p.projective_ridge_groups.reduce((s,g)=>s+g.component_tables[l][1]*g.direction[j],0),3)===0,"global divisibility for EVERY word");
}
function stablePythonJson(value){
  if(Array.isArray(value))return "["+value.map(stablePythonJson).join(", ")+"]";
  if(value&&typeof value==="object")return "{"+Object.keys(value).sort().map(k=>JSON.stringify(k)+": "+stablePythonJson(value[k])).join(", ")+"}";
  return JSON.stringify(value);
}
function checkBudget(b,degree,kappa){
  check(b.certified_additive_degree===degree&&b.nonzero_relative_support_lower===frac(1n,2n**BigInt(degree))&&BigInt(b.independent_uniform_tests_required)===BigInt(kappa)*2n**BigInt(degree)&&b.conditional_false_accept_probability_upper===frac(1n,2n**BigInt(kappa)),"inductive support bound and conservative soundness count");
  check(b.dimension_independent===true&&b.fresh_points_after_candidate_commit_required===true,"dimension-free bound needs fresh independent tests");
}
const hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_NATIVE_PHASE_IDENTITY.md"))).digest("hex");
check(report.derivation_sha256===hash&&report.status==="COMPACT_GROWING_DEPTH_PHASE_MERGES_AND_RANDOMIZED_IDENTITIES_REVIEW_PENDING","pinned derivation");
for(const k of["candidate_record_accepted","useful_full_depth_merge_rule_discovered","quantum_speedup_proved"])check(report[k]===false,"no solver/speedup promotion");
same(report.native_controls.map(c=>c.phase_digits),[1,2,3],"whole prespecified depth sweep");
let rootWords=0,injectionBranches=0,explicitWitnesses=0,exactCertificates=0;
for(const c of report.native_controls){
  const r=c.phase_digits,N=3**(r+1),q=3**r,n=2,d=3,ws=words(d),originals=[],values=[],ids=[];let exponent=0;
  check(c.source_programs.length===15&&c.coefficients.length===15,"same full source cohort");
  for(const p of c.source_programs){
    const s=p.source,M=45,chartAt=chart(2*r+2),pairs=p.original_labels.map(row=>{const f=row.map(chartAt);return[f.map(x=>x[0]),f.map(x=>x[1])];});
    check(s.original_even_level===2*r+2&&s.parent_modulus===String(N)&&s.dimension===n&&s.acquired_original_native_inputs===M&&s.original_source_ids.length===M,"actual original depth, dimension and cap");
    same(p.original_frequency_pairs,pairs,"cyclotomic frequency reconstruction");ids.push(...s.original_source_ids);originals.push(pairs);
    check(p.all_source_measurement_outcomes_accepted===true&&p.IID_full_depth_output_label_law_proved===false,"no rare-source/output-law claim");
    const base=p.original_affine_base,columns=p.original_affine_columns;
    check(base.length===M&&columns.length===d&&[base,...columns].every(row=>row.length===M&&row.every(x=>Number.isInteger(x)&&[0,1,2].includes(x))),"full physical original chart");
    const value=z=>Array.from({length:n},(_,l)=>{
      let f=0;for(let i=0;i<M;i++){const t=mod(base[i]+columns.reduce((a,col,j)=>a+col[i]*z[j],0),3),b=base[i];f+=(t?pairs[i][t-1][l]:0)-(b?pairs[i][b-1][l]:0);}
      f=mod(f,N);check(f%3===0,"original residual root division");return f/3;
    });
    validatePhase(p.compact_phase);
    for(const z of ws){same(phaseValue(p.compact_phase,z),value(z),"compact phase equals full original-root map");rootWords++;}
    const localExponent=s.active_original_inputs-d;exponent+=localExponent;
    check(p.raw_source_program_branch_probability===frac(1n,3n**BigInt(localExponent)),"all source measurement masses");values.push(value);
  }
  check(ids.length===675&&new Set(ids).size===675&&c.full_original_input_cap_charged===675&&c.physical_IID_independence_certified_by_ids===false,"all acquired and unused source ancestors charged");
  const selected=c.coefficients.map((x,i)=>x?i:-1).filter(i=>i>=0);same(c.selected_program_indices,selected,"actual consumed programs");
  check(selected.length===4&&c.coefficients.every(x=>Number.isInteger(x)&&[0,1,2].includes(x))&&c.injection_outcomes.length===4,"signed program schema");
  check(c.all_injection_outcomes_accepted===true&&c.each_selected_program_consumed_once===true&&c.unknown_inverse_conjugation_or_cloning_used===false&&c.efficient_search_for_useful_merge_rule_supplied===false&&c.quantum_speedup_proved===false,"correct scope of compact merge");
  check(c.raw_source_program_transcript_probability===frac(1n,3n**BigInt(exponent))&&c.conditional_injection_transcript_probability==="1/531441","source/injection costs kept distinct");
  validatePhase(c.merged_phase);
  const aggregate=new Map();
  for(let k=0;k<selected.length;k++){
    const j=selected[k],sign=c.coefficients[j],m=c.injection_outcomes[k];
    for(const group of c.source_programs[j].compact_phase.projective_ridge_groups){
      const id=key(group.direction),offset=dot(group.direction,m)%3,tables=aggregate.get(id)||Array.from({length:n},()=>[0,0,0]);
      for(let l=0;l<n;l++)for(let t=0;t<3;t++)tables[l][t]=mod(tables[l][t]+group.component_tables[l][(offset+sign*t)%3]-group.component_tables[l][offset],N);
      aggregate.set(id,tables);
    }
  }
  const expectedGroups=[...aggregate].filter(([_,rows])=>rows.some(row=>row.some(Boolean))).map(([direction,component_tables])=>({direction:JSON.parse(direction),component_tables})).sort((a,b)=>key(a.direction).localeCompare(key(b.direction)));
  same(c.merged_phase.projective_ridge_groups,expectedGroups,"exact translated ridge merging without tensor expansion");
  const value=z=>Array.from({length:n},(_,l)=>mod(selected.reduce((s,j,k)=>{
    const m=c.injection_outcomes[k],x=m.map((a,i)=>mod(a+c.coefficients[j]*z[i],3));return s+values[j](x)[l]-values[j](m)[l];
  },0),q));
  const table=ws.map(value);same(c.complete_merged_frequency_table,table,"full-root one-use phase sum");
  for(let i=0;i<ws.length;i++)same(phaseValue(c.merged_phase,ws[i]),table[i],"compact merged evaluator");
  check(c.complete_original_word_checks===405&&c.physical_injection_controls.length===4,"bounded complete source/injection replay");
  for(const replay of c.physical_injection_controls){
    same(replay.full_retained_modulus_secret,[q-1,r>1?q/3+1:2],"full-modulus calibration secret");
    check(replay.all_injection_outcomes===27&&replay.conditional_branch_probability==="1/27"&&replay.reference_dimension===27&&Number.isFinite(replay.arbitrary_reference_entangled_max_error)&&replay.arbitrary_reference_entangled_max_error>=0&&replay.arbitrary_reference_entangled_max_error<4e-12,"all reference-entangled one-use SUM branches, not oracle access");injectionBranches+=27;
  }
  const certificate=degreeCertificate(c.merged_phase);check(certificate.certified_global_degree_upper===2*r,"exact highest native degree cancellation in this control");
  for(const probe of[c.degree_two_probe,c.top_degree_probe]){
    same(probe.degree_certificate,certificate,"independent local valuation degree certificates");checkBudget(probe.budget,2*r,8);
    const commitment=crypto.createHash("sha256").update(stablePythonJson({phase:c.merged_phase,order:probe.tested_derivative_order})).digest("hex");check(probe.phase_commit_sha256===commitment,"candidate/order fixed before points");
    check(probe.exact_identity_proved_by_random_testing===false&&probe.deterministic_seed_is_mathematical_randomness_certificate===false&&probe.soundness_bound_applicable_to_this_run===false&&probe.derivative_cube_vertices_materialized===0,"seeded tests are not probabilistic proof certificates");
    if(probe.status==="EXACT_FACTORED_IDENTITY"){
      check(probe.tested_derivative_order>2*r&&probe.identity_algebraically_certified===true&&probe.evaluations_used===0&&probe.counterexample===null,"exact zero follows from valuation certificate, not samples");exactCertificates++;
    }else{
      check(probe.status==="EXPLICIT_COUNTEREXAMPLE"&&probe.tested_derivative_order===3&&probe.identity_algebraically_certified===false&&probe.evaluations_used>0,"higher-root quadratic transfer falsifier");
      const w=probe.counterexample,k=w.directions.length,out=Array(n).fill(0);
      check(k===3&&w.base.length===d&&w.directions.every(v=>v.length===d),"recorded finite-difference witness");
      for(let bits=0;bits<2**k;bits++){
        const active=Array.from({length:k},(_,i)=>Boolean(bits&(1<<i))),z=w.base.map((a,i)=>mod(a+w.directions.reduce((s,v,j)=>s+(active[j]?v[i]:0),0),3)),sign=(-1)**(k-active.filter(Boolean).length);
        value(z).forEach((x,l)=>out[l]+=sign*x);
      }
      const actual=out.map(x=>mod(x,q));same(w.component_derivative,actual,"exact witness from original-source difference cube");check(actual.some(Boolean),"genuinely nonzero higher-root derivative");explicitWitnesses++;
    }
  }
}
same(report.identity_budgets.map(b=>b.phase_digits),[1,2,4,8,16,32],"complete soundness schedule");
for(const b of report.identity_budgets)checkBudget(b,2*b.phase_digits+1,32);
check(explicitWitnesses===2&&exactCertificates===4,"both correct field-root transfer and growing-depth failure");
console.log(JSON.stringify({status:"independent_compact_native_phase_identity_certificates_passed",originalRootWords:rootWords,oneUseInjectionBranches:injectionBranches,exactValuationCertificates:exactCertificates,quadraticTransferCounterexamples:explicitWitnesses,quantumSpeedup:false}));
