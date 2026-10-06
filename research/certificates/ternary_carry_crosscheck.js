"use strict";
// Independent native frequency formulas, GF3 elimination and full branch replay.
const fs=require("fs"),path=require("path");
const r=JSON.parse(fs.readFileSync(path.join(__dirname,"../phase_workbench/ternary_carry_packets.json"),"utf8"));
function check(v,m){if(!v)throw Error(m);}
function close(a,b,m){check(Math.abs(a-b)<5e-12,`${m}: ${a} != ${b}`);}
function mod(x,q){return((x%q)+q)%q;}
function same(a,b,m){check(JSON.stringify(a)===JSON.stringify(b),m);}
function tuples(h){return Array.from({length:3**h},(_,i)=>Array.from({length:h},(_,j)=>Math.floor(i/3**(h-j-1))%3));}
function freq(y,j,L){const[a,b]=y;if(j===0)return 0;return L===3 ? mod(j===1 ? a-2*b : -a-b,9) : mod(j===1 ? -a-b : -2*a+b,27);}
function rref(labels){
  const m=labels.length,n=labels[0].length,A=Array.from({length:n},(_,l)=>labels.map(y=>mod(y[l][0]+y[l][1],3))),pivots=[];
  let rank=0;
  for(let j=0;j<m && rank<n;j++){
    const i=A.findIndex((row,i)=>i>=rank && row[j]);if(i<0)continue;
    [A[i],A[rank]]=[A[rank],A[i]];
    A[rank]=A[rank].map(x=>mod(x*A[rank][j],3));
    for(let k=0;k<n;k++)if(k!==rank){const c=A[k][j];A[k]=A[k].map((x,h)=>mod(x-c*A[rank][h],3));}
    pivots.push(j);rank++;
  }
  return {rows:A.slice(0,rank),pivots,free:Array.from({length:m},(_,j)=>j).filter(j=>!pivots.includes(j))};
}
function assignment(c,syndrome,z){
  const v=Array(c.labels.length).fill(0);
  c.free.forEach((f,j)=>v[f]=z[j]);
  c.pivots.forEach((p,i)=>v[p]=mod(syndrome[i]-c.free.reduce((a,f)=>a+c.rows[i][f]*v[f],0),3));return v;
}
function frequencies(labels,j,L){return labels[0].map((_,l)=>mod(labels.reduce((v,y,i)=>v+freq(y[l],j[i],L),0),3**((L+1)/2)));}
function residual(c,syndrome,z,L){
  const q=3**((L+1)/2),base=frequencies(c.labels,assignment(c,syndrome,Array(c.free.length).fill(0)),L);
  return frequencies(c.labels,assignment(c,syndrome,z),L).map((x,l)=>{const d=mod(x-base[l],q);check(d%3===0,"nondivisible native phase");return d/3;});
}
function poly(rows,z){return rows.map(row=>mod(row.coefficients.reduce((v,c)=>v+c.coefficient*z.reduce((a,x,j)=>a*x**c.powers[j],1),0),3));}
function multiply(a,b){return[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];}
let amplitudes=0,branches=0,polynomialValues=0;
for(const a of r.native_controls){
  const L=a.resources.parent_level,labels=a.native_labels,c={...rref(labels),labels},q=3**((L+1)/2),s=a.integer_secret_calibration;
  same(c.rows,a.public_RREF_rows,"independent GF3 RREF");same(c.pivots,a.pivots,"pivot indices");same(c.free,a.free_columns,"kernel width");
  const rank=c.pivots.length,h=c.free.length;
  check(a.all_syndrome_branches.length===3**rank,"postselected native syndrome");
  let total=0;
  for(const b of a.all_syndrome_branches){
    const points=tuples(h),states=[];let probability=0;
    for(const [i,z]of points.entries()){
      const j=assignment(c,b.syndrome,z),f=frequencies(labels,j,L),theta=2*Math.PI*mod(f.reduce((v,x,l)=>v+s[l]*x,0),q)/q;
      const amp=[Math.cos(theta)*3**(-labels.length/2),Math.sin(theta)*3**(-labels.length/2)];
      amp.forEach((x,k)=>close(x,b.full_unnormalized_joint_amplitudes[i][k],"native compiler complex amplitude"));
      const value=residual(c,b.syndrome,z,L);same(value,b.public_residual_frequency_table[i],"actual reduced phase table");
      if(L===3){same(poly(b.classical_cubic_polynomial.component_polynomials,z),value,"cubic interpolation");polynomialValues++;}
      else check(b.classical_cubic_polynomial===null,"higher-depth phase mislabeled cubic");
      states.push(amp);probability+=amp[0]**2+amp[1]**2;amplitudes++;
    }
    close(probability,3**(-rank),"uniform native syndrome");close(probability,b.probability,"charged branch probability");total+=probability;
    let purity=0;
    const width=3**(h-1);
    for(let i=0;i<3;i++)for(let j=0;j<3;j++){
      let inner=[0,0];
      for(let k=0;k<width;k++){
        const v=states[i*width+k],w=states[j*width+k],z=multiply(v,[w[0],-w[1]]);
        inner=[inner[0]+z[0]/probability,inner[1]+z[1]/probability];
      }
      purity+=inner[0]**2+inner[1]**2;
    }
    close(purity,b.first_retained_qutrit_purity,"joint-register entanglement");branches++;
  }
  close(total,1,"complete native instrument");close(a.physical_full_output_norm,1,"producer norm");
  check(!a.constant_fraction_retained_registers_is_a_decoder && !a.resources.outputs_certified_as_IID_PSP_samples,"false throughput promotion");
}
let conditionalValues=0;
for(const a of r.conditional_algebraic_sum_controls){
  const packets=a.three_packet_native_labels.map(labels=>({...rref(labels),labels})),points=tuples(packets[0].free.length);
  for(const[i,z]of points.entries()){
    const values=packets.map((p,j)=>residual(p,a.initial_syndromes[j],z.map((x,k)=>mod(x+a.difference_shifts[j][k],3)),3));
    const value=values[0].map((_,l)=>mod(values.reduce((v,x)=>v+x[l],0),3));
    same(value,a.conditional_algebraic_sum.public_frequency_table[i],"conditional ternary sum");
    same(poly(a.conditional_algebraic_sum.component_polynomials,z),value,"degree-two cancellation");conditionalValues++;
  }
  check(a.conditional_algebraic_sum.component_polynomials.every(p=>p.degree<=2),"uncancelled cubic term");
  check(!a.full_three_packet_quantum_instrument_replayed && !a.conditional_algebraic_sum.native_source_matching_supplied,"conditional algebra promoted to source algorithm");
}
const cost=r.literal_low_matrix_match_ledger;
check(cost.second_and_third_IID_low_matrices_both_match_first_probability.exponent===-2*cost.secret_dimension*cost.native_qutrits_per_batch,"free source matching");
check(cost.probabilities_are_conditioning_costs_not_optimal_matching_lower_bounds && !cost.more_general_public_tensor_alignment_excluded,"literal matching became universal no-go");
const d=r.higher_level_fourth_difference_countercontrol,c=r.native_controls[d.native_control_index];
const b=c.all_syndrome_branches.find(b=>JSON.stringify(b.syndrome)===JSON.stringify(d.syndrome));
const points=tuples(c.free_columns.length),table=new Map(points.map((z,i)=>[z.join(","),b.public_residual_frequency_table[i]]));
const values=Array(c.integer_secret_calibration.length).fill(0);
for(let mask=0;mask<16;mask++){
  const z=d.origin.map((x,j)=>mod(x+d.four_additive_directions.reduce((v,a,k)=>v+((mask>>k)&1)*a[j],0),3));
  const sign=(-1)**Array.from({length:4},(_,k)=>(mask>>k)&1).reduce((a,b)=>a+b,0);
  table.get(z.join(",")).forEach((x,l)=>values[l]+=sign*x);
}
same(values.map(x=>mod(x,9)),d.fourth_difference_by_secret_component,"higher-level degree-transfer falsifier");
check(values.some(x=>mod(x,9)!==0) && !d.fixed_classical_cubic_receiver_transfer_allowed,"unsupported cubic receiver");
check(Object.values(r.claim_gate).every(x=>x===false),"candidate promoted");
console.log(JSON.stringify({status:"independent_replay_passed",complex_amplitudes:amplitudes,complete_native_branches:branches,
  cubic_function_values:polynomialValues,conditional_quadratic_sum_values:conditionalValues,new_algorithm:false}));
