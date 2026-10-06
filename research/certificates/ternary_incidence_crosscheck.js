"use strict";
// Independent bounded source replay and public GF3 constraint elimination.
const fs=require("fs"),path=require("path");
const report=JSON.parse(fs.readFileSync(path.join(__dirname,"../phase_workbench/ternary_incidence_decoder.json"),"utf8"));
function check(x,message){if(!x)throw Error(message);}
function mod(x,q=3){return((x%q)+q)%q;}
function dot(a,b,q=3){return mod(a.reduce((v,x,i)=>v+x*b[i],0),q);}
function same(a,b,message){check(JSON.stringify(a)===JSON.stringify(b),message);}
function born(a,c,q,b,o){
  let re=0,im=0;[0,a,c].forEach((f,j)=>{
    const angle=2*Math.PI*(f/q-(b*j*j+o*j)/3);re+=Math.cos(angle);im+=Math.sin(angle);
  });return(re*re+im*im)/9;
}
let branches=0,zeros=0,rowsChecked=0,decoders=0;
// Direct trace chart for L3: C1=u-2v, C2=-u-v mod9.
// Rebuild the measurement permutation without Python's packet/compiler APIs.
const labels=[];for(let u=0;u<9;u++)for(let v=0;v<3;v++)labels.push([u,v]);
const strata=new Map();let amplitudeError=0;
for(const y1 of labels)for(const y2 of labels){
  const ys=[y1,y2],low=ys.map(y=>mod(y[0]+y[1])),pivot=low.findIndex(x=>x!==0),rank=Number(pivot>=0);
  const free=[0,1].filter(i=>i!==pivot);
  for(let outcome=0;outcome<3;outcome++){
    const syndrome=rank?[outcome]:[],complement=rank?[]:[outcome];
    const words=[0,1,2].map(j=>{
      const word=[0,0];word[free[0]]=j;if(!rank)word[free[1]]=outcome;
      if(rank)word[pivot]=mod(low[pivot]*(outcome-low[free[0]]*j));return word;
    });
    const phase=words.map(word=>mod(ys.reduce((v,y,i)=>v+[0,y[0]-2*y[1],-y[0]-y[1]][word[i]],0),9));
    const difference=phase.slice(1).map(x=>mod(x-phase[0],9));check(difference.every(x=>x%3===0),"native divisibility");
    const freq=difference.map(x=>x/3),key=JSON.stringify([low,syndrome,complement]),pair=JSON.stringify(freq);
    if(!strata.has(key))strata.set(key,new Map());const counts=strata.get(key);counts.set(pair,(counts.get(pair)||0)+1);
    words.forEach((_,j)=>{
      const original=2*Math.PI*8*(phase[j]-phase[0])/9,lower=2*Math.PI*2*[0,...freq][j]/3;
      amplitudeError=Math.max(amplitudeError,Math.hypot(Math.cos(original)-Math.cos(lower),Math.sin(original)-Math.sin(lower)));
    });branches++;
  }
}
check(strata.size===27 && branches===2187 && amplitudeError<1e-12,"full source replay");
for(const counts of strata.values())check(counts.size===9 && [...counts.values()].every(x=>x===9),"conditional native uniformity");
check(report.full_native_source_control.all_affine_branches_replayed===branches,"report source count");
for(const c of report.six_unimodular_line_matrices){
  const [j0,j1,j2]=c.physical_digit_permutation,M=[[j1-j0,Number(j1===2)-Number(j0===2)],[j2-j0,Number(j2===2)-Number(j0===2)]];
  same(c.integer_matrix,M,"local matrix");check(Math.abs(M[0][0]*M[1][1]-M[0][1]*M[1][0])===1,"nonunit determinant");
}
function compositions(n,total){
  if(!n)return total?[]:[[]];const out=[];
  for(let a=0;a<=Math.min(2,total);a++)for(const tail of compositions(n-1,total-a))out.push([a,...tail]);return out;
}
function polyAdd(p,e,c){const k=e.join(",");p.set(k,mod((p.get(k)||0)+c));}
function multiply(p,q){
  const out=new Map();for(const [u,a]of p)for(const [v,b]of q){
    const x=u.split(",").map(Number),y=v.split(",").map(Number);
    const e=x.map((a,i)=>{const t=a+y[i];return t<3?t:1+(t-1)%2;});polyAdd(out,e,a*b);
  }return out;
}
function constraint(c,n){
  const zero=Array(n).fill(0),A=new Map(),B=new Map();polyAdd(A,zero,-c.outcome);polyAdd(B,zero,-c.basis);
  for(let j=0;j<n;j++){const unit=zero.map((_,i)=>Number(i===j));polyAdd(A,unit,c.alpha[j]);polyAdd(B,unit,c.beta[j]);}
  const square=multiply(B,B),factor=new Map();for(const [e,x]of square)factor.set(e,mod(-x));polyAdd(factor,zero,1);
  return multiply(factor,A);
}
for(const c of report.final_field_native_decoders){
  const n=c.dimension,basis=[0,1,2,3].flatMap(d=>compositions(n,d)),D=basis.length,rows=new Map(),secret=c.result.secret;
  const features=basis.map(e=>mod(e.reduce((v,a,i)=>v*secret[i]**a,1)));
  same(features,c.result.feature_vector,"secret feature certificate");
  for(const sample of c.public_measurement_records){
    const A=mod(dot(sample.alpha,secret)-sample.outcome),B=mod(dot(sample.beta,secret)-sample.basis);
    check(mod((1-B*B)*A)===0,"observed sample excludes certified secret");
    const p=constraint(sample,n),v=basis.map(e=>p.get(e.join(","))||0);
    for(const [pivot,row]of [...rows].sort((a,b)=>a[0]-b[0])){
      const coefficient=v[pivot];for(let j=0;j<D;j++)v[j]=mod(v[j]-coefficient*row[j]);
    }
    const pivot=v.findIndex(x=>x!==0);if(pivot>=0){const inverse=v[pivot];rows.set(pivot,v.map(x=>mod(x*inverse)));}
    rowsChecked++;
  }
  check(rows.size===D-1 && c.result.rank===D-1 && c.result.status==="FIELD_SECRET_CERTIFIED","public rank certificate");
  check(c.source_batches===c.public_measurement_records.length && c.odd_native_qutrits_consumed===(n+1)*c.source_batches,"source charge");
  check(!c.result.secret_assignments_enumerated && !c.result.complete_parent_secret_recovered,"field result promoted");
  check(c.probability_budget.sufficient_fresh_IID_samples===81*(D-1+4*c.probability_budget.confidence_bits),"budget arithmetic");decoders++;
}
for(const q of [3,9,27]){
  let any=0;const counts=Array(9).fill(0);
  for(let a=0;a<q;a++)for(let c=0;c<q;c++){
    let has=false;for(let b=0;b<3;b++)for(let o=0;o<3;o++){
      const u=mod(a-q/3*(b+o),q),v=mod(c-q/3*(4*b+2*o),q),zero=(u===q/3&&v===2*q/3)||(v===q/3&&u===2*q/3);
      check(zero===(born(a,c,q,b,o)<1e-25),"equilateral support theorem");if(zero){counts[3*b+o]++;has=true;zeros++;}
    }if(has)any++;
  }check(any===9 && counts.every(x=>x===2),"higher-root zero census");
}
const shadow=report.native_low_shadow_countercontrol;
for(let o=0;o<3;o++)check(Math.abs(born(8,8,9,2,o)-shadow.actual_outcome_probabilities[o])<1e-12,"native shadow countercontrol");
check(shadow.actual_outcome_probabilities[1]>.18 && shadow.false_constraint_value_at_true_secret===2 && !shadow.field_shadow_transfer_admitted,"shadow false constraint");
for(const c of report.higher_root_support_exclusion_ledgers){
  const R=3n**BigInt(c.root_digits);check(BigInt(c.phase_modulus)===R,"root ledger");
  function fraction(s){const p=s.split("/").map(BigInt);return[p[0],p[1]||1n];}
  const [a,b]=fraction(c.fixed_MUB_outcome_zero_fraction);check(a*R*R===2n*b,"zero fraction");
  check(!c.positive_likelihood_information_ruled_out && !c.general_classical_or_quantum_decoder_lower_bound,"restricted boundary promoted");
}
check(!report.new_full_depth_algorithm && !report.candidate_accepted && !report.speedup_claim_allowed,"claim promotion");
console.log(JSON.stringify({status:"independent_replay_passed",native_affine_branches:branches,
  conditional_source_strata:strata.size,public_constraint_rows:rowsChecked,field_decoders:decoders,exact_MUB_zeros:zeros,new_full_depth_algorithm:false}));
