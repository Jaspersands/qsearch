"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../phase_workbench/ternary_fourier_information.json"),"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},same=(a,b,m)=>check(JSON.stringify(a)===JSON.stringify(b),m);
const mod=(x,q)=>(x%q+q)%q,dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),key=JSON.stringify;
const words=k=>Array.from({length:3**k},(_,i)=>Array.from({length:k},(_,j)=>Math.floor(i/3**(k-j-1))%3));
function rank(A,width){
  A=A.map(row=>row.map(x=>mod(x,3)));let r=0;
  for(let j=0;j<width&&r<A.length;j++){
    const p=A.findIndex((row,i)=>i>=r&&row[j]);if(p<0)continue;
    [A[r],A[p]]=[A[p],A[r]];A[r]=A[r].map(x=>x*A[r][j]%3);
    for(let i=0;i<A.length;i++)if(i!==r){const c=A[i][j];A[i]=A[i].map((x,k)=>mod(x-c*A[r][k],3));}r++;
  }return r;
}
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
function frac(a,b){const g=gcd(a,b);a/=g;b/=g;return b===1n?String(a):a+"/"+b;}
function energy(e){
  const d=e.width,D=3**d,L=e.directions;check(rank(L,d)===d&&e.physical_frame_rank===d,"injective native frame");
  const features=L.map(row=>row.flatMap((a,i)=>row.slice(i).map(b=>a*b%3))),square=rank(features,d*(d+1)/2);
  check(e.symmetric_square_feature_rank===square&&e.symmetric_square_dimension===d*(d+1)/2&&e.unordered_pair_separation_certified_by_square_span===(square===d*(d+1)/2),"symmetric square rank certificate");
  const code=words(d).map(z=>L.map(row=>dot(row,z)%3)),counts=new Map();
  for(const x of code)for(const y of code){const k=key(x.map((a,i)=>[a,y[i]].sort((a,b)=>a-b)));counts.set(k,(counts.get(k)||0)+1);}
  const E=Array.from(counts.values()).reduce((s,x)=>s+x*x,0);
  check(String(E)===e.ordered_balanced_quadruples&&e.conditional_mean_local_Fourier_collision_nonzero_secret===frac(BigInt(E),BigInt(D)**3n),"independent balanced quadruple energy");
  if(square===d*(d+1)/2)check(E===2*D*D-D&&e.full_square_rank_bound_less_than_one_bit===true,"global unordered-pair separation");
  check(Math.abs(e.entropy_deficit_upper_nats-Math.log(E/(D*D)))<2e-10&&e.physical_IID_source_premise_certified===false,"information entropy deficit / unverified external supply");return E;
}
function info(x,e){
  const G=3n**BigInt(x.components*x.phase_digits),logG=x.components*x.phase_digits*Math.log(3),D=e.program_dimension,c=e.entropy_deficit_upper_nats;
  const zero=Math.exp(-logG),per=c+(Math.log(D)-c)*zero,h=-x.target_mean_full_secret_error*Math.log(x.target_mean_full_secret_error)-(1-x.target_mean_full_secret_error)*Math.log(1-x.target_mean_full_secret_error);
  check(x.secret_count===String(G)&&x.exact_zero_secret_prior_mass===frac(1n,G)&&x.numeric_entropy_and_Fano_values_are_estimates===true,"exact zero-secret mass / numeric estimates");
  check(Math.abs(x.mean_mutual_information_per_output_upper_nats-per)<2e-10&&Math.abs(x.mean_joint_information_upper_nats-x.outputs*per)<2e-10&&Math.abs(x.Fano_required_outputs_lower_real-Math.max(0,((1-x.target_mean_full_secret_error)*logG-h)/per))<2e-8,"entropy subadditivity / Fano accounting");
  for(const k of["label_or_outcome_adaptive_measurement_bases_covered","collective_nonproduct_measurements_covered","computational_cost_of_classical_inference_lower_bounded","source_realization_pointwise_information_bound"])check(x[k]===false,"limited information scope: "+k);
}
const hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_FOURIER_INFORMATION.md"))).digest("hex");
check(R.derivation_sha256===hash&&R.status==="SOURCE_LOCAL_FOURIER_INFORMATION_CEILING_REVIEW_PENDING","pinned derivation");
for(const k of["general_collective_receiver_ruled_out","quantum_speedup_proved","candidate_record_accepted"])check(R[k]===false,"unsupported claim: "+k);
same(R.native_controls.map(c=>c.seed),[89000,89128,89031],"native shape controls");let pairs=0;
for(const c of R.native_controls){
  const keys=new Set();for(const f of c.selected_source_frames){
    check([1,2].includes(f.domain_sign),"one-use sign");for(const row of f.physical_frame_rows)if(row.some(Boolean))keys.add(key(row.map(x=>x*row.find(Boolean)%3)));
  }
  same(Array.from(keys).map(JSON.parse).sort((a,b)=>{for(let i=0;i<a.length;i++)if(a[i]!==b[i])return a[i]-b[i];return 0;}),c.energy.directions,"actual selected physical directions, not fitted output coefficients");
  energy(c.energy);info(c.information_bound,c.energy);pairs+=c.energy.program_dimension**2;
}
const census=R.original_high_chart_census,p=census.original_program,N=9,source=p.source;
const ids=source.original_source_ids,index=new Map(ids.map((x,i)=>[x,i])),supports=source.odd_input_original_ancestors.map(row=>row.map(x=>index.get(x))),counts=new Map(),collisions=[0,0,0];
check(source.original_even_level===4&&source.parent_modulus==="9","true native chart root");
// At level4 the exact integer-frequency matrix is [[0,1],[1,0]].
same(p.original_frequency_pairs,p.original_labels.map(row=>[row.map(label=>mod(label[1],9)),row.map(label=>mod(label[0],9))]),"original ring labels give the native frequency pairs");
check(supports.length===2&&census.records.length===81&&census.virtual_chart_lifts_are_additional_supplied_states===false&&census.finite_chart_proves_physical_IID_source_premise===false,"true original chart / no virtual samples");
const lifts=words(4);census.records.forEach((record,j)=>{
  same(record.original_pivot_alpha_delta_lifts,lifts[j],"complete original alpha/delta chart");const frequencies=p.original_frequency_pairs.map(pair=>pair.map(row=>row.slice()));
  for(let i=0;i<2;i++){const pivot=supports[i][0],h=lifts[j][2*i],k=lifts[j][2*i+1];frequencies[pivot][0][0]=mod(frequencies[pivot][0][0]+3*h,N);frequencies[pivot][1][0]=mod(frequencies[pivot][1][0]+6*h+3*k,N);}
  function original(z){let total=0;for(let i=0;i<ids.length;i++){
    const b=p.original_affine_base[i],t=mod(b+p.original_affine_columns[0][i]*z,3);total+=(t?frequencies[i][t-1][0]:0)-(b?frequencies[i][b-1][0]:0);
  }total=mod(total,N);check(total%3===0,"original residual divides exactly");return total/3;}
  const phase=[0,1,2].map(z=>mod(original(mod(2+z,3))-original(2),3));same(record.actual_phase_values,phase,"true original-source high chart phase after injection");
  const pair=key(phase.slice(1));counts.set(pair,(counts.get(pair)||0)+1);
  for(let s=0;s<3;s++)for(let t=0;t<3;t++){
    let re=0,im=0;phase.forEach((f,z)=>{const angle=2*Math.PI*(s*f-t*z)/3;re+=Math.cos(angle);im+=Math.sin(angle);});const probability=(re*re+im*im)/9;collisions[s]+=probability*probability;
  }
});
check(counts.size===9&&Array.from(counts.values()).every(x=>x===9),"all native output frequency pairs uniformly covered");
for(let s=0;s<3;s++)check(Math.abs(collisions[s]/81-census.mean_Fourier_collision_by_secret[s])<2e-10&&Math.abs(collisions[s]/81-(s?5/9:1))<2e-10,"native fourth moment direct Fourier replay");
for(const x of R.growing_dimension_information_ledgers)info(x,R.native_controls[2].energy);
console.log(JSON.stringify({status:"PASS",ordered_physical_pair_checks:pairs,true_original_chart_words:81,nonzero_secret_collision:"5/9",external_IID_supply_certified:false}));
