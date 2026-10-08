"use strict";
// The imported checker first replays the source geometry and all base proofs.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,gcd,abs,F,fraction,commonIntegers,sameSet,prepare,geometry,momentModel,report,load}=require("./ternary_prefix_integrality_crosscheck.js");
const momentBytes=fs.readFileSync(path.join(__dirname,"../phase_workbench/ternary_prefix_moments.json"));
const moments=JSON.parse(momentBytes),psd=load("ternary_moment_psd");
check(crypto.createHash("sha256").update(momentBytes).digest("hex")===psd.source_moment_report_sha256,"source exact moments are hash-pinned");
check(!psd.polynomial_pair_finder_proved&&!psd.population_obstruction_proved&&!psd.novelty_claim,"PSD audit claims remain scoped");
let prefixes=0,activeWindings=0,negativeForms=0,positiveFactorizations=0,cuts=0,newDualProofs=0,newPrimalProofs=0;
const fractionEq=(a,den,value)=>{const q=fraction(value);return a*q[1]===q[0]*den;};
function primal(model,cert,winding){check(cert&&cert.valid&&cert.required_winding===winding,"exact primal in current cut/winding model");
  check(!cert.global_native_distribution_proved&&!cert.integer_prefix_completion_proved,"moments not native realizability");
  const {den,values:x}=commonIntegers(cert.moments);check(x.length===model.variables.length&&x.every(a=>a>=0n),"every original moment AND cut slack nonnegative");
  for(let i=0;i<model.E.length;i++){let rhs=0n;for(const[j,a]of model.E[i])rhs+=x[j]*a;check(rhs===model.B[i]*den,"every source/condition/marginal/PSD-cut row exact");}
  return {den,x};}
function dual(model,cert,winding){check(cert&&cert.valid&&cert.required_winding===winding&&cert.proves_no_coupled_moments,"valid signed dual in complete PSD-cut model");
  const {den,values:y}=commonIntegers(cert.signed_equation_multipliers);check(y.length===model.E.length,"complete original AND PSD-cut equation multipliers");
  const columns=Array(model.variables.length).fill(0n);let rhs=0n;
  for(let i=0;i<model.E.length;i++){rhs+=y[i]*model.B[i];if(y[i])for(const[j,a]of model.E[i])columns[j]+=y[i]*a;}
  check(columns.every(a=>a>=0n)&&columns.length===cert.exact_column_coefficients.length&&columns.every((a,j)=>fractionEq(a,den,cert.exact_column_coefficients[j])),"all moment/slack columns exactly nonnegative");
  check(rhs<0n&&fractionEq(rhs,den,cert.exact_combined_rhs),"exact strict contradiction for all points satisfying valid cuts");}
function matrix(model,p){const indicators=model.variables.map((key,i)=>[key,i]).filter(([key])=>key[0]==="p"),n=indicators.length+1;
  const index=new Map(model.variables.map((key,i)=>[JSON.stringify(key),i])),A=Array.from({length:n},()=>Array(n).fill(0n));A[0][0]=p.den;
  for(let i=1;i<n;i++){const [key,k]=indicators[i-1];A[0][i]=A[i][0]=A[i][i]=p.x[k];
    for(let j=1;j<i;j++){const other=indicators[j-1][0];if(key[1]===other[1])continue;const[a,b]=key[1]<other[1]?[key,other]:[other,key];
      const k=index.get(JSON.stringify(["J",a[1],a[2],b[1],b[2]]));check(k!==undefined,"complete native cross-block moment");A[i][j]=A[j][i]=p.x[k];}}
  return {A,den:p.den,indicators:indicators.map(([key])=>key)};}
function positivity(M,proof){const n=M.A.length;check(proof.matrix_dimension===n,"original indicator-matrix size");
  if(proof.negative){check(!proof.ldl&&proof.status==="EXACT_INDEFINITE_MOMENT_MATRIX"&&proof.negative.valid,"negative point certificate not PSD proof");
    const {den,values:v}=commonIntegers(proof.negative.vector);check(v.length===n,"negative vector covers all ORIGINAL indicators");let value=0n;
    for(let i=0;i<n;i++)for(let j=0;j<n;j++)value+=v[i]*M.A[i][j]*v[j];
    check(value<0n&&fractionEq(value,M.den*den*den,proof.negative.quadratic_value),"strict negative quadratic form independently replayed");negativeForms++;return false;}
  const c=proof.ldl;check(c&&c.valid&&c.proves_psd&&proof.status==="EXACT_PSD_MOMENT_MATRIX","full positive factorization required");
  check(c.lower.length===n&&c.lower.every(row=>row.length===n)&&c.diagonal.length===n,"complete LDL dimensions");
  const l=commonIntegers(c.lower.flat()),d=commonIntegers(c.diagonal),L=Array.from({length:n},(_,i)=>l.values.slice(i*n,(i+1)*n));
  check(d.values.every(x=>x>=0n)&&L.every((row,i)=>row[i]===l.den&&row.slice(i+1).every(x=>x===0n)),"unit lower factor and NONNEGATIVE zero-aware diagonal");
  const denominator=l.den*l.den*d.den;
  for(let i=0;i<n;i++)for(let j=0;j<n;j++){let value=0n;for(let k=0;k<=Math.min(i,j);k++)value+=L[i][k]*d.values[k]*L[j][k];
    check(value*M.den===M.A[i][j]*denominator,"complete exact original LDL matrix reconstruction");}positiveFactorizations++;return true;}
function appendCut(model,M,record,vector){check(JSON.stringify(record.vector)===JSON.stringify(vector),"applied cut is the certified negative direction");
  const v=vector.map(fraction),byKey=new Map(M.indicators.map((key,i)=>[JSON.stringify(key),v[i+1]]));
  const mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]),add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),twice=a=>mul(F(2n),a);
  const coefficients=model.variables.map(key=>{if(key[0]==="p"){const a=byKey.get(JSON.stringify(key));return add(twice(mul(v[0],a)),mul(a,a));}
    if(key[0]==="J")return twice(mul(byKey.get(JSON.stringify(["p",key[1],key[2]])),byKey.get(JSON.stringify(["p",key[3],key[4]]))));return F(0n);});
  const constant=mul(v[0],v[0]),all=[...coefficients,constant],den=all.reduce((d,q)=>d/gcd(d,q[1])*q[1],1n),integers=all.map(q=>q[0]*(den/q[1]));
  const divisor=integers.reduce((g,x)=>gcd(g,x),0n);check(divisor>0n,"nontrivial nonnegative-square cut");const normalized=integers.map(x=>x/divisor),c=normalized.pop(),N=model.variables.length;
  check(record.clearing_denominator===String(den)&&record.primitive_divisor===String(divisor)&&record.integer_constant===String(c)&&record.slack_variable===N,"exact cut normalization and nonnegative slack");
  check(JSON.stringify(record.integer_coefficients)===JSON.stringify(normalized.map(String)),"every original and prior-slack cut coefficient reconstructed");
  const bits=[...normalized,c].reduce((b,x)=>Math.max(b,x===0n?0:abs(x).toString(2).length),0);check(bits===record.maximum_integer_coefficient_bits,"cut coefficient bit size retained");
  const row=new Map();normalized.forEach((x,i)=>{if(x)row.set(i,x);});row.set(N,-1n);model.E.push(row);model.B.push(-c);model.variables.push(["PSD_SLACK",model.variables.filter(key=>key[0]==="PSD_SLACK").length]);cuts++;}
const expected=moments.cases.flatMap(c=>c.trials.filter(t=>t.coupled_moment_survives).map(t=>[c.fixture_probe_index,t.target]));
sameSet(psd.cases.flatMap(c=>c.trials.map(t=>[c.fixture_probe_index,t.target])),expected,"all previously surviving prefixes tested");
for(const c of psd.cases){const pc=report.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index),mc=moments.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index);
  check(pc&&mc&&c.fingerprint===pc.fingerprint,"actual native geometry identity");const base=prepare(pc);
  for(const t of c.trials){const old=mc.trials.find(x=>x.target===t.target),pt=pc.trials.find(x=>x.target===t.target),g=geometry(base,BigInt(t.target),pt.frontier);
    sameSet(t.all_allowed_windings,g.windings,"all original integral windings retained");sameSet(t.winding_trials.map(x=>x.winding_branch),g.windings,"complete PSD-pilot winding schedule");
    let eliminated=true,survives=false;
    for(const run of t.winding_trials){const original=old.winding_trials.find(x=>x.winding_branch===run.winding_branch);check(run.required_winding===run.winding_branch,"same winding model");
      if(!original.primal){check(run.steps.length===0&&run.cuts_added===0&&run.LP_calls===0,"unexamined branches not silently optimized");
        check(run.status===(original.dual?"REUSED_EXACT_MOMENT_OBSTRUCTION":"CARRIED_BASE_WINDING_UNKNOWN"),"base proof/unknown reused faithfully");eliminated=eliminated&&!!original.dual;continue;}
      activeWindings++;check(run.cut_budget===psd.cut_budget&&run.cuts_added<=run.cut_budget&&!run.integer_prefix_completion_proved,"bounded cuts are not integer recovery");
      const model=momentModel(g,run.winding_branch);let applied=0,LPcalls=0,terminal="";
      for(let i=0;i<run.steps.length;i++){const step=run.steps[i],analysis=step.analysis;LPcalls+=analysis.cost.LP_calls;
        check(!(analysis.primal&&analysis.dual),"primal/dual exclusivity");let cert=analysis.primal;
        if(i===0){check(analysis.primal_from_source_report===true&&analysis.primal===null&&analysis.cost.LP_calls===0,"only initial source proof can be reused");cert=original.primal;}
        else{check(!analysis.primal_from_source_report,"later points require their OWN exact certificates");check(analysis.cost.variables===model.variables.length&&analysis.cost.equations===model.E.length,"re-solved complete strengthened model");}
        if(analysis.dual){check(!step.positivity&&!step.added_cut,"dual conclusion after all retained valid cuts");dual(model,analysis.dual,run.winding_branch);newDualProofs++;terminal="EXACT_VALID_PSD_CUT_OBSTRUCTION";}
        else if(cert){const point=primal(model,cert,run.winding_branch);if(i)newPrimalProofs++;check(step.positivity,"exact positivity decision required");const M=matrix(model,point),positive=positivity(M,step.positivity);
          if(positive){check(!step.added_cut,"PSD point not cut off");terminal="EXACT_PSD_CONTINUATION_NOT_NATIVE";}
          else if(step.added_cut){check(applied<run.cut_budget,"no extra cut beyond explicit cap");appendCut(model,M,step.added_cut,step.positivity.negative.vector);applied++;}
          else{check(applied===run.cut_budget,"only explicit cap can stop on an indefinite point");terminal="PSD_CUT_CAP_UNKNOWN";}}
        else{check(!step.positivity&&!step.added_cut,"unknown cannot carry a fake positivity/infeasibility conclusion");terminal="PSD_CUT_RECONSTRUCTION_UNKNOWN";}
        if(terminal)check(i===run.steps.length-1,"no steps after terminal proof or cap");
      }
      check(run.steps.length===applied+1&&run.cuts_added===applied&&run.LP_calls===LPcalls&&terminal===run.status,"complete re-solve/certificate ledger");
      eliminated=eliminated&&terminal==="EXACT_VALID_PSD_CUT_OBSTRUCTION";survives=survives||terminal==="EXACT_PSD_CONTINUATION_NOT_NATIVE";
    }
    check(t.prefix_eliminated===eliminated&&t.psd_continuation_survives===survives,"entire winding verdict, not a point refutation");prefixes++;
  }}
console.log(JSON.stringify({status:"independent_native_moment_positivity_and_valid_cut_checks_passed",prefixes,activeWindings,
  negativeForms,positiveFactorizations,cuts,newDualProofs,newPrimalProofs,populationObstructionProved:false}));
module.exports={primal,matrix,positivity,appendCut,dual,psd,moments,momentBytes};
