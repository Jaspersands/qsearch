"use strict";
// Independent integer source identities, field reconstruction and fiber census.
const fs=require("fs"),path=require("path");
const report=JSON.parse(fs.readFileSync(path.join(__dirname,"../phase_workbench/ternary_least_trit_bootstrap.json"),"utf8"));
function check(x,m){if(!x)throw Error(m);}
const mod=(x,q)=>((x%q)+q)%q;
const bigmod=(x,q)=>((x%q)+q)%q;
const dot=(a,b)=>a.reduce((s,x,j)=>s+BigInt(x)*BigInt(b[j]),0n);
function same(a,b,m){check(JSON.stringify(a)===JSON.stringify(b),m);}
function root(x,q){const t=2*Math.PI*Number(bigmod(x,q))/Number(q);return[Math.cos(t),Math.sin(t)];}
function nativeFrequency(label,L){
  let u=-1n,v=1n;
  for(let j=2;j<L;j+=2)[u,v]=[u+v,-u];
  const q=3n**BigInt(L/2),[a,b]=label.map(BigInt);
  return[Number(bigmod(u*a+v*b,q)),Number(bigmod((u+v)*a-u*b,q))];
}
let transformations=0;
for(const c of report.native_prefix_and_randomization_controls){
  const q=BigInt(c.phase_denominator),scale=3n**BigInt(c.known_prefix_digits),Q=q/scale;
  const sign=BigInt(c.public_random_sign),p=c.permutation,s=c.calibration_secret_only.map(BigInt);
  const prefix=c.assumed_correct_prefix.map(BigInt),shift=c.public_random_shift.map(BigInt);
  check(s.every((x,j)=>x%scale===prefix[j]),"calibration prefix promise");
  const guess=prefix.map((x,j)=>x+scale*shift[j]);
  const target=p.map(j=>bigmod(sign*((s[j]-prefix[j])/scale-shift[j]),Q));
  same(target.map(Number),c.transformed_secret_calibration_only,"randomized secret identity");
  const lower=[c.learner_view.first,c.learner_view.second];
  for(let k=0;k<2;k++){
    const row=[c.original_first,c.original_second][k];
    same(p.map(j=>Number(bigmod(sign*BigInt(row[j]),Q))),lower[k],"native relabeling");
    check(bigmod(-dot(row,guess),q)===BigInt(c.diagonal_phase_numerators[k+1]),"known phase program");
    check(bigmod(dot(row,s)+BigInt(c.diagonal_phase_numerators[k+1]),q)===scale*bigmod(dot(lower[k],target),Q),"exact physical amplitude exponent");
  }
  c.original_native_ring_labels.forEach((label,j)=>same(nativeFrequency(label,c.original_native_even_level),[c.original_first[j],c.original_second[j]],"original native chart"));
  c.lower_native_ring_labels.forEach((label,j)=>same(nativeFrequency(label,c.learner_view.native_even_level),[lower[0][j],lower[1][j]],"lower native chart"));
  check(!c.wrong_prefix_source_promise&&!c.unknown_secret_passed_to_learner,"source claim gates");
  transformations++;
}
for(const c of report.exact_source_uniformity){
  check(BigInt(c.original_frequency_pairs)===BigInt(c.lower_frequency_pairs)*BigInt(c.exact_preimages_per_lower_pair),"uniform lift cardinality");
  check(!c.reducing_measured_covariant_records_gives_this_source,"no measured shadow bridge");
}
same(report.biased_error_countercontrol.symmetrized_error_law,["2/5","3/10","3/10"],"sign-symmetric biased error law");
check(report.primitive_only_countercontrol.uniform_all_secret_success_lower_bound==="4/15","primitive-only gap");
for(const c of report.conditional_reduction_ledgers){
  const[n,d]=c.advantage_assumption.split("/").map(Number),eps=n/d;
  const decisions=c.dimension*c.root_digits,R=c.repetitions_per_coordinate_digit;
  check(9*R*eps*eps/8>=Math.log(2*decisions)+16*Math.log(2),"fresh-call amplification bound");
  check(c.total_fresh_weak_calls===R*decisions&&c.total_fresh_original_native_qutrits===R*decisions*c.native_qutrits_per_weak_call_assumption,"complete sample charge");
  check(!c.weak_learner_implemented&&!c.full_native_recovery_implemented,"conditional not implemented");
}
for(const c of report.arbitrary_collective_least_trit_copy_gates){
  const[a,b]=(c.mean_advantage_squared_upper_bound.includes("/")?c.mean_advantage_squared_upper_bound.split("/"):[c.mean_advantage_squared_upper_bound,"1"]).map(BigInt);
  check(a*(2n*3n**BigInt(c.dimension*c.root_digits))===b*(3n**BigInt(c.native_copies)-1n),"exact full-label copy moment");
  check(c.necessary_copy_gate_passed===(100n*a>=b),"one-tenth advantage copy condition");
}
let wordsChecked=0;
for(const c of report.least_trit_information_only_references){
  const q=3**c.digits,M=c.frequency_pairs.length,D=3**M,fibers=new Map();
  for(let w=0;w<D;w++){
    let v=w;const f=Array(c.dimension).fill(0);
    for(let j=M-1;j>=0;j--){const digit=v%3;v=Math.floor(v/3);if(digit)for(let k=0;k<f.length;k++)f[k]=mod(f[k]+c.frequency_pairs[j][digit-1][k],q);}
    const key=[f[0]%(q/3),...f.slice(1)].join(","),k=Math.floor(f[0]/(q/3));
    if(!fibers.has(key))fibers.set(key,[0,0,0]);fibers.get(key)[k]++;
  }
  check(fibers.size===c.nuisance_fiber_count,"nuisance fiber count");
  for(const f of c.nuisance_fibers)same(fibers.get(f.key.join(",")),f.counts_by_trit_character,"native word/fiber census");
  const success=[...fibers.values()].reduce((s,c)=>s+c.reduce((v,k)=>v+Math.sqrt(k),0)**2,0)/(3*D);
  check(Math.abs(success-c.optimal_uniform_secret_least_trit_success)<1e-12,"trit primal/dual optimum trace");
  check(!c.efficient_fiber_preparation_or_inverse_granted&&!c.native_weak_learner_implemented,"exponential reference gates");
  wordsChecked+=D;
}
function featureBasis(n){
  const powers=[];
  function rec(prefix){if(prefix.length===n){if(prefix.reduce((a,b)=>a+b,0)<=3)powers.push(prefix);return;}for(let k=0;k<3;k++)rec([...prefix,k]);}
  rec([]);powers.sort((a,b)=>a.reduce((x,y)=>x+y,0)-b.reduce((x,y)=>x+y,0)||a.join("").localeCompare(b.join("")));
  return powers;
}
function times(A,B){
  const out=new Map();
  for(const[ak,av]of A)for(const[bk,bv]of B){
    const a=ak.split(",").map(Number),b=bk.split(",").map(Number);
    const key=a.map((x,j)=>{const t=x+b[j];return t<3?t:1+(t-1)%2;}).join(",");
    out.set(key,mod((out.get(key)||0)+av*bv,3));
  }return out;
}
function polynomial(record,n){
  const zero=Array(n).fill(0).join(","),A=new Map([[zero,mod(-record.outcome,3)]]),B=new Map([[zero,mod(-record.basis,3)]]);
  for(let j=0;j<n;j++){const key=Array.from({length:n},(_,k)=>Number(k===j)).join(",");A.set(key,record.alpha[j]);B.set(key,record.beta[j]);}
  const gate=new Map([...times(B,B)].map(([k,v])=>[k,mod(-v,3)]));gate.set(zero,mod((gate.get(zero)||0)+1,3));
  return times(gate,A);
}
function decodeField(records,n){
  const basis=featureBasis(n),D=basis.length,rows=new Map();
  for(const record of records){
    const poly=polynomial(record,n),v=basis.map(p=>poly.get(p.join(","))||0);
    for(const[j,row]of[...rows.entries()].sort((a,b)=>a[0]-b[0])){const x=v[j];for(let k=0;k<D;k++)v[k]=mod(v[k]-x*row[k],3);}
    const pivot=v.findIndex(x=>x);if(pivot<0)continue;
    const inv=v[pivot];for(let k=0;k<D;k++)v[k]=mod(v[k]*inv,3);rows.set(pivot,v);
  }
  check(rows.size===D-1,"independent field constraint rank");
  const free=basis.findIndex((_,j)=>!rows.has(j)),v=Array(D).fill(0);v[free]=1;
  for(const[j,row]of[...rows.entries()].sort((a,b)=>b[0]-a[0]))v[j]=mod(-row.reduce((s,x,k)=>s+x*v[k],0),3);
  check(v[0]!==0,"affine feature normalization");const inv=v[0];for(let k=0;k<D;k++)v[k]=mod(v[k]*inv,3);
  const secret=Array.from({length:n},(_,j)=>v[basis.findIndex(p=>p.every((x,k)=>x===Number(k===j)))]);
  check(basis.every((p,j)=>p.reduce((a,e,k)=>mod(a*secret[k]**e,3),1)===v[j]),"nullvector evaluation certificate");
  return secret;
}
let fieldRecords=0;
for(const c of report.actual_known_prefix_field_closures){
  const q=BigInt(c.original_modulus),scale=q/3n,s=c.calibration_secret_only.map(BigInt),prefix=c.externally_given_correct_prefix.map(BigInt);
  const recovered=decodeField(c.raw_public_records,c.dimension);
  same(recovered,c.recovered_top_trit,"independent public-data final-field decoder");
  same(s.map((x,j)=>Number((x-prefix[j])/scale)),recovered,"conditional top-digit calibration");
  for(const record of c.raw_public_records){
    const rows=[record.original_first,record.original_second],phases=record.phase_numerators.map(BigInt);
    const exponents=rows.map((row,k)=>{check(phases[k]===bigmod(-dot(row,prefix),q),"known-prefix physical phase");return bigmod(dot(row,s)+phases[k],q);});
    const psi=[[1,0],...exponents.map(x=>root(x,q))];
    for(let o=0;o<3;o++){
      let re=0,im=0;
      for(let j=0;j<3;j++){const z=root(BigInt(-record.basis*j*j-o*j),3n);re+=(z[0]*psi[j][0]-z[1]*psi[j][1])/3;im+=(z[0]*psi[j][1]+z[1]*psi[j][0])/3;}
      check(Math.abs(re*re+im*im-record.probabilities[o])<1e-12,"original corrected root MUB Born law");
    }
    const a=Number(bigmod(dot(record.alpha,recovered)-BigInt(record.outcome),3n));
    const b=Number(bigmod(dot(record.beta,recovered)-BigInt(record.basis),3n));
    check(mod((1-b*b)*a,3)===0,"true feasible cubic constraint");
    fieldRecords++;
  }
  check(!c.prefix_discovered_by_this_control&&!c.original_full_secret_discovery&&!c.decoder_received_unknown_secret,"conditional closure claim gates");
}
check(!report.higher_root_weak_learner_implemented&&!report.full_native_secret_search_implemented&&!report.accepted_candidate,"global non-breakthrough gates");
process.stdout.write(JSON.stringify({status:"independent_replay_passed",native_transformations:transformations,
  nuisance_fiber_words:wordsChecked,original_root_field_records:fieldRecords,independent_public_field_decoders:3,higher_root_weak_learner:false})+"\n");
