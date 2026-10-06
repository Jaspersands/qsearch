"use strict";
// Independent native chart, elementary gate replay, exact noise and radix audit.
const fs=require("fs"),path=require("path");
const report=JSON.parse(fs.readFileSync(path.join(__dirname,"../classical_baselines/ternary_covariant_noise.json"),"utf8"));
function check(x,m){if(!x)throw Error(m);}
function same(x,y,m){check(JSON.stringify(x)===JSON.stringify(y),m);}
const mod=(x,q)=>((x%q)+q)%q;
function root(x,q){const a=2*Math.PI*mod(x,q)/q;return[Math.cos(a),Math.sin(a)];}
function multiply(a,b){return[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];}
function probability(q,a,b){const x=root(a,q),y=root(b,q);return((1+x[0]+y[0])**2+(x[1]+y[1])**2)/(3*q*q);}
function freq(label,L){let[u,v]=[-1,1];for(let j=2;j<L;j+=2)[u,v]=[u+v,-u];const q=3**(L/2);return[mod(u*label[0]+v*label[1],q),mod((u+v)*label[0]-u*label[1],q)];}
function digit(i,wire,width){return Math.floor(i/3**(width-wire-1))%3;}
function replay(re,im,width,tape){
  const D=re.length;
  for(const gate of tape){
    const a=new Float64Array(D),b=new Float64Array(D);
    if(gate.gate==="inverse_F3"){
      const stride=3**(width-gate.wire-1);
      for(let i=0;i<D;i++)if(digit(i,gate.wire,width)===0)for(let j=0;j<3;j++)for(let k=0;k<3;k++){
        const p=root(-j*k,3),source=i+k*stride,target=i+j*stride;
        a[target]+=(p[0]*re[source]-p[1]*im[source])/Math.sqrt(3);
        b[target]+=(p[0]*im[source]+p[1]*re[source])/Math.sqrt(3);
      }
    }else{
      const[f,s]=gate.wires;
      for(let i=0;i<D;i++){
        const x=digit(i,f,width),y=digit(i,s,width);let target=i,z=[1,0];
        if(gate.gate==="controlled_phase")z=root(gate.phase_sign*x*y,gate.phase_denominator);
        else if(gate.gate==="swap")target+=(y-x)*3**(width-f-1)+(x-y)*3**(width-s-1);
        else if(gate.gate==="swap_basis20_01"){
          if(x===2&&y===0)target+=-2*3**(width-f-1)+3**(width-s-1);
          if(x===0&&y===1)target+=2*3**(width-f-1)-3**(width-s-1);
        }else throw Error("unknown native gate");
        a[target]=z[0]*re[i]-z[1]*im[i];b[target]=z[0]*im[i]+z[1]*re[i];
      }
    }re=a;im=b;
  }return[re,im];
}
let bornOutcomes=0;
for(const c of report.native_physical_readout_controls){
  const q=c.modulus,pairs=c.native_labels[0].map(y=>freq(y,c.native_level));
  const a=mod(pairs.reduce((s,p,j)=>s+p[0]*c.calibration_secret[j],0),q),d=mod(pairs.reduce((s,p,j)=>s+p[1]*c.calibration_secret[j],0),q);
  const re=new Float64Array(q*q),im=new Float64Array(q*q);re[0]=1/Math.sqrt(3);
  for(const[i,v]of[[q,a],[2*q,d]]){const z=root(v,q);re[i]=z[0]/Math.sqrt(3);im[i]=z[1]/Math.sqrt(3);}
  const[x,y]=replay(re,im,c.gate_recipe.qutrit_registers,c.gate_recipe.gates);let mass=0;
  for(let u=0;u<q;u++)for(let v=0;v<q;v++){
    const i=u*q+v,p=x[i]**2+y[i]**2;
    check(Math.abs(p-probability(q,u-a,v-d))<1e-11,"native gate/Born/noise law");mass+=p;bornOutcomes++;
  }check(Math.abs(mass-1)<1e-11,"native receiver completeness");
}
const points=[[0,0],[1,0],[0,1]],counts=new Map();
for(const a of points)for(const b of points){const key=[a[0]-b[0],a[1]-b[1]].join(",");counts.set(key,(counts.get(key)||0)+1);}
check(counts.size===7&&[...counts.values()].reduce((s,x)=>s+x*x,0)===15,"exact characteristic support/collision5/3");
function character(q,pair){const x=mod(pair[0],q),y=mod(pair[1],q);if(!x&&!y)return[1n,1n];
  return [...counts.keys()].some(k=>{const[a,b]=k.split(",").map(Number);return(a||b)&&mod(a,q)===x&&mod(b,q)===y;})?[1n,3n]:[0n,1n];}
function gcd(a,b){while(b)[a,b]=[b,a%b];return a<0n?-a:a;}
function fraction(a,b=1n){if(b<0n)[a,b]=[-a,-b];const d=gcd(a,b);return[a/d,b/d];}
function parse(s){const v=s.split("/").map(BigInt);return[v[0],v[1]||1n];}
function add(a,b){return fraction(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function times(a,b){return fraction(a[0]*b[0],a[1]*b[1]);}
function turns(a){return fraction(((a[0]%a[1])+a[1])%a[1],a[1]);}
function equal(a,b,m){check(a[0]*b[1]===b[0]*a[1],m);}
for(const c of report.scalar_attack_gates){
  for(let t=0;t<c.modulus;t++){
    const actual=c.weights.reduce((x,p)=>times(x,character(c.modulus,p.map(w=>t*w))),[1n,1n]);
    const g=c.gate;let expected=[0n,1n];
    if(g.classification==="zero_statistic"||(g.classification==="uniform_on_noise_image_subgroup"&&t*g.noise_image_step%c.modulus===0)||t===0)expected=[1n,1n];
    else if(g.classification==="common_unit_scaled_root_directions"&&g.surviving_dual_frequencies.includes(t))expected=parse(g.fourier_bias);
    equal(actual,expected,"complete scalar compression law");
  }
}
// Uniform marginals do not imply a uniform JOINT channel.
let jointCollision=[0n,1n];
for(let u=0;u<9;u++)for(let v=0;v<9;v++){
  const ch=character(9,[u+v,2*u+3*v]);jointCollision=add(jointCollision,times(ch,ch));
  if((u===0)!==(v===0))check(ch[0]===0n,"joint countercontrol marginal");
}equal(jointCollision,[5n,3n],"invertible joint information retained");
const r=report.chosen_access_countercontrol,q=Number(r.modulus),recovered=Array(r.dimension).fill(0);
let radixSamples=0;
r.decisions.forEach((c,i)=>{
  const coordinate=Math.floor(i/r.root_digits),digitIndex=i%r.root_digits,power=3**(r.root_digits-1-digitIndex);
  same(c.chosen_first_frequency,Array.from({length:r.dimension},(_,j)=>j===coordinate?power:0),"no native random label substitution");
  const values=r.first_register_outcomes[i],correction=power*recovered[coordinate];let real=0,imaginary=0;
  values.forEach(b=>{const z=root(b-correction,q);real+=z[0]/values.length;imaginary+=z[1]/values.length;});
  const scores=Array.from({length:3},(_,d)=>{const z=root(-d,3);return real*z[0]-imaginary*z[1];});
  scores.forEach((x,j)=>check(Math.abs(x-c.scores[j])<1e-10,"independent chosen-access score"));
  const value=scores.indexOf(Math.max(...scores));check(value===c.decoded_digit,"independent radix digit");
  recovered[coordinate]+=value*3**digitIndex;radixSamples+=values.length;
});same(recovered,r.decoded_secret,"polynomial chosen-access estimator");check(radixSamples===r.physical_qutrits_consumed,"fresh copy charge");
for(const c of report.chosen_access_ledgers){const q=BigInt(c.modulus),cost=BigInt(c.chosen_qutrits_required)*q**BigInt(c.dimension);
  check(String(cost)===c.expected_native_qutrits_for_rejection_compiling_this_exact_schedule,"exponential native schedule acquisition");}
for(const c of report.native_polynomial_sample_identifiability){
  check(c.native_qutrit_samples===41*(2*c.dimension*c.root_digits+16),"polynomial identifiability sample ledger");
  check(c.all_secret_search_required_by_reference_decoder&&!c.efficient_random_label_candidate_search_supplied,"identifiability is not a decoder");
}
function lowKernel(vectors){
  const n=vectors[0].length,m=vectors.length,A=Array.from({length:n},(_,j)=>vectors.map(v=>mod(v[j],3))),pivots=[];let row=0;
  for(let col=0;col<m&&row<n;col++){
    let k=row;while(k<n&&!A[k][col])k++;if(k===n)continue;[A[row],A[k]]=[A[k],A[row]];
    const inv=A[row][col];A[row]=A[row].map(x=>mod(x*inv,3));
    for(let j=0;j<n;j++)if(j!==row){const c=A[j][col];A[j]=A[j].map((x,l)=>mod(x-c*A[row][l],3));}
    pivots.push(col);row++;
  }const free=Array.from({length:m},(_,j)=>j).find(j=>!pivots.includes(j)),w=Array(m).fill(0);w[free]=1;
  pivots.forEach((p,j)=>w[p]=mod(-A[j][free],3));return w.map(x=>x===2?-1:x);
}
const tree=report.classical_Gaussian_collimation;let layer=tree.original_marginal_records,steps=0;
while(layer[0].modulus>3){
  const next=[];
  for(let start=0;start<layer.length;start+=tree.dimension+1){
    const parents=layer.slice(start,start+tree.dimension+1),q=parents[0].modulus,w=lowKernel(parents.map(p=>p.first)),certificate=tree.steps[steps++];
    same(w,certificate.ledger.signed_weights,"independent integer signed Gaussian relation");
    const a=parents[0].first.map((_,j)=>mod(parents.reduce((s,p,i)=>s+w[i]*p.first[j],0),q));
    check(a.every(x=>x%3===0),"full-root mean divisibility");
    const observed=mod(parents.reduce((s,p,i)=>s+w[i]*p.outcome,0),q),residue=observed%3;
    let bias=[1n,1n],phi=[0n,1n];parents.forEach((p,i)=>{if(w[i]){bias=times(bias,parse(p.bias));phi=add(phi,times([BigInt(w[i]),1n],parse(p.noise_phase_turns)));}});
    phi=turns(add(phi,[-BigInt(residue),BigInt(q)]));
    const origins=parents.flatMap(p=>p.original_record_ids).sort((a,b)=>a-b);check(new Set(origins).size===origins.length,"shared original noise");
    const out=certificate.output;same(out.first,a.map(x=>x/3),"classical quotient label");check(out.outcome===Math.floor(observed/3)&&out.modulus===q/3,"classical quotient observation");
    same(out.original_record_ids,origins,"all original ancestor charges");equal(parse(out.bias),bias,"multiplied visibility");equal(parse(out.noise_phase_turns),phi,"all-residue phase tag");
    next.push(out);
  }layer=next;
}same(layer[0],tree.final_record,"full collimation tree");
// Complete tiny source mean control, including a nonprimitive wrong difference.
for(const trial of[2,3,5]){
  let mean=0;
  for(let a=0;a<9;a++)for(let c=0;c<9;c++)for(let e=0;e<9;e++)for(let f=0;f<9;f++){
    const x=e+a*(2-trial),y=f+c*(2-trial),score=root(x,9)[0]+root(y,9)[0]+root(x-y,9)[0];
    mean+=probability(9,e,f)*score/81;
  }check(Math.abs(mean-(trial===2?1:0))<1e-10,"native held-out score expectation");
}
check(!report.accepted_quantum_algorithm&&!report.random_label_polynomial_secret_decoder&&!report.classical_simulator_of_original_unknown_phase_states,"overstated native recovery");
console.log(JSON.stringify({status:"independent_replay_passed",native_gate_Born_outcomes:bornOutcomes,
  scalar_characters_checked:report.scalar_attack_gates.length*81,chosen_access_records_redecoded:radixSamples,
  Gaussian_collimation_merges:steps,heldout_native_mean_cases:3,native_random_label_decoder:false}));
