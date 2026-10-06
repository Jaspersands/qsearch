"use strict";
// Exact native trace recurrence and explicit cubes, independent of Python.
const fs=require("fs"),path=require("path");
const report=JSON.parse(fs.readFileSync(path.join(__dirname,"../phase_workbench/ternary_phase_depth.json"),"utf8"));
function check(v,m){if(!v)throw Error(m);}
function same(a,b,m){check(JSON.stringify(a)===JSON.stringify(b),m);}
function mod(x,q){return((x%q)+q)%q;}
function points(q,n){return Array.from({length:q**n},(_,i)=>Array.from({length:n},(_,j)=>Math.floor(i/q**(n-j-1))%q));}
function delta(table,v,q){return table.map((x,j)=>mod(table[(j+v)%3]-x,q));}
function beta(L){let u=2,v=-1;for(let i=1;i<L;i++)[u,v]=[-2*u-v,u-v];const denominator=3**Math.floor(L/2);return[u/denominator,v/denominator];}
function local(y,L){const[u,v]=beta(L),q=3**Math.ceil(L/2);return[0,mod(u*y[0]+v*y[1],q),mod((u+v)*y[0]-u*y[1],q)];}
function assign(c,z){
  const word=Array(c.native_labels.length).fill(0);c.free.forEach((f,j)=>{word[f]=z[j];});
  c.pivots.forEach((p,i)=>{word[p]=mod(c.syndrome[i]-c.rows[i].reduce((v,a,j)=>v+(c.free.includes(j) ? a*word[j] : 0),0),3);});return word;
}
let integerIdentities=0,growingDerivatives=0,restrictedValues=0,aliasAmplitudes=0;
for(const c of report.cyclic_operator_identities){
  const d=c.derivative_order;
  for(const basis of points(2,3).filter(x=>x.reduce((a,b)=>a+b,0)===1)){
    let actual=basis.slice();for(let i=0;i<d;i++)actual=actual.map((x,j)=>actual[(j+1)%3]-x);
    let predicted=basis.slice();for(let i=0;i<c.remaining_difference_order;i++)predicted=predicted.map((x,j)=>predicted[(j+1)%3]-x);
    predicted=predicted.map((_,j)=>c.integer_multiplier*predicted[(j+c.cyclic_shift_power)%3]);
    same(actual,predicted,"integer cyclic operator identity");integerIdentities++;
  }
}
for(const c of report.sharp_native_odd_level_controls){
  const L=c.level,q=3**Math.ceil(L/2),R=q/3,columns=[[2,1,0],[2,0,1]],r=(L-1)/2;
  for(const[dirs,expected]of [[c.logical_derivative_directions,c.retained_component_derivative],[c.next_derivative_directions,c.next_derivative]]){
    let total=0;
    for(let i=0;i<3;i++){
      let table=local(c.native_labels[i][0],L);
      for(const v of dirs)table=delta(table,mod(v.reduce((s,x,j)=>s+x*columns[j][i],0),3),q);
      total+=table[0];
    }
    const value=mod(total,q);check(value%3===0,"native derivative division");same([value/3],expected,"growing native phase derivative");growingDerivatives++;
  }
  same(c.retained_component_derivative,[3**(r-1)],"sharp degree witness");same(c.top_weighted_Schur_prediction,c.retained_component_derivative,"highest tensor prediction");
  const cost=c.resources;check(cost.local_modular_subtractions===9*(L+1) && cost.derivative_cube_vertices_not_materialized===String(2**(L+1)) &&
    cost.local_frequency_entries_stored===9 && cost.unknown_weighted_phase_queries===0 && !cost.coherent_unknown_preparation_or_inverse_supplied,"oracle or cube access smuggled in");
}
const transfer=report.cubic_to_fifth_degree_transfer_countercontrol,physicalPoints=points(3,3),W=[0,1,2].map(j=>physicalPoints.map(x=>x[j]));
same(transfer.physical_point_order,physicalPoints,"evaluation-code source ordering");
for(let i=0;i<3;i++)for(let j=i;j<3;j++)for(let k=j;k<3;k++)check(mod(physicalPoints.reduce((s,x,a)=>s+x[2]*W[i][a]*W[j][a]*W[k][a],0),3)===0,"cubic Schur condition");
check(mod(physicalPoints.reduce((s,x)=>s+x[0]**2*x[1]**2*x[2]**2,0),3)===2,"fifth Schur witness");
for(const c of transfer.native_level_controls){
  const L=c.level,q=3**Math.ceil(L/2),model={native_labels:transfer.native_labels,free:c.initial_free_columns,pivots:c.initial_pivots,rows:c.initial_RREF_rows,syndrome:Array(c.initial_pivots.length).fill(0)};
  same(c.physical_frame_columns,W,"changed Schur frame");
  const table=physicalPoints.map(z=>{
    const logical=c.logical_frame_columns[0].map((_,i)=>mod(z.reduce((s,x,j)=>s+x*c.logical_frame_columns[j][i],0),3)),word=assign(model,logical);
    same(word,W[0].map((_,i)=>mod(z.reduce((s,x,j)=>s+x*W[j][i],0),3)),"frame not in actual native kernel");
    const f=mod(word.reduce((s,j,i)=>s+local(transfer.native_labels[i][0],L)[j],0),q);check(f%3===0,"native restricted phase division");return[f/3];
  });
  same(table,c.restricted_native_residual_table,"restricted native table");restrictedValues+=table.length;
  const dirs=[[1,0,0],[1,0,0],[0,1,0],[0,1,0],[0,0,1]];let fifth=0;
  for(const bits of points(2,5)){
    const z=[0,0,0].map((_,j)=>mod(bits.reduce((s,b,i)=>s+b*dirs[i][j],0),3)),index=z[0]*9+z[1]*3+z[2];
    fifth+=(-1)**(5-bits.reduce((s,b)=>s+b,0))*table[index][0];
  }
  same([mod(fifth,q/3)],c.fifth_derivative,"cubic transfer countercontrol");
}
check(!transfer.level3_cubic_admission_transfers_to_level5 && !transfer.full_27_input_quantum_instrument_replayed && !transfer.source_cost_or_secret_decoder_supplied,"countercontrol became algorithm");
for(const c of report.conditional_degree_visibility_ledgers){
  const digits=Math.round(Math.log(Number(c.phase_modulus))/Math.log(3)),degree=c.claimed_additive_degree_upper_bound,k=Math.min(digits,Math.ceil(degree/2));
  check(BigInt(c.phase_modulus)===3n**BigInt(digits) && BigInt(c.maximum_relative_phase_order)===3n**BigInt(k) &&
    BigInt(c.secret_alias_step)===3n**BigInt(k) && c.minimum_additive_degree_needed_for_full_phase_order===2*digits-1,"degree/root-order gate");
  check(c.all_residual_secret_digits_could_be_retained===(k===digits) && !c.degree_bound_itself_certified_by_this_ledger &&
    !c.retained_junk_coherent_syndromes_other_measurements_excluded,"conditional degree bound promoted to universal no-go");
}
for(const c of report.constant_degree_secret_alias_controls){
  const q=3**c.phase_digits,frequencies=[0,q/3,mod(4*q/3,q)];same(c.component_frequency_table,frequencies,"classical quadratic frequency scale");
  for(let j=0;j<3;j++)for(let a=0;a<2;a++){
    const theta=2*Math.PI*mod(c.secret_pair[a]*frequencies[j],q)/q,expected=[Math.cos(theta)/Math.sqrt(3),Math.sin(theta)/Math.sqrt(3)];
    expected.forEach((x,k)=>check(Math.abs(x-c.calibration_phase_amplitudes[a][j][k])<5e-12,"exact high-secret alias amplitude"));aliasAmplitudes++;
  }
  check(c.pure_output_states_identical && c.secret_pair[1]-c.secret_pair[0]===3,"false alias result");
}
const lifted=report.formal_quadratic_vs_additive_degree_countercontrol;
let table=local(lifted.native_ring_label,lifted.original_even_native_level);
for(const expected of lifted.all_repeated_cyclic_derivative_tables){same(table,expected,"integer-lift/additive-degree distinction");table=delta(table,1,9);}
check(lifted.actual_additive_phase_degree===4 && !lifted.classical_quadratic_F3_transfer_admitted,"formal quadratic treated as classical");
check(Object.values(report.claim_gate).every(x=>x===false),"candidate promoted");
console.log(JSON.stringify({status:"independent_replay_passed",integer_operator_columns:integerIdentities,
  growing_native_derivatives:growingDerivatives,restricted_native_phase_values:restrictedValues,
  secret_alias_amplitudes:aliasAmplitudes,new_algorithm:false}));
