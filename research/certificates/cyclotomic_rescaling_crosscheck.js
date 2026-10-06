"use strict";
// Independent closed-form ternary ideal arithmetic and all-branch native replay.
const fs = require("fs"), path = require("path");
const report = JSON.parse(fs.readFileSync(path.join(__dirname, "../phase_workbench/cyclotomic_rescaling_gate.json"), "utf8"));
function check(v, m) { if (!v) throw new Error(m); }
function close(a, b, m) { check(Math.abs(a-b) < 4e-12, `${m}: ${a} != ${b}`); }
function mod(a, n) { return ((a%n)+n)%n; }
function chart(L) {
  const q = 3**Math.floor(L/2);
  return L%2 ? [3*q, 2*q, q] : [q, 0, q];
}
function reduce(v, L) {
  const [h, c, k] = chart(L), carry = Math.floor(v[1]/k);
  return [mod(v[0]-carry*c, h), mod(v[1], k)];
}
function add(u, v, L) { return reduce([u[0]+v[0], u[1]+v[1]], L); }
function mul(u, v, L) { return reduce([u[0]*v[0]-u[1]*v[1], u[0]*v[1]+u[1]*v[0]-u[1]*v[1]], L); }
function residue(y) { return mod(y[0]+y[1], 3); }
function transport(y, a, L) {
  if (a===1) return reduce(y, L);
  let z = [y[0]-y[1], -y[1]];
  for (let j=0;j<L;j++) z=mul(z, [0, -1], L);
  return reduce(z, L);
}
function quotient(y, L) {
  check(residue(y)===0, "actual label is not pi-divisible");
  const a=-2*y[0]+y[1], b=-y[0]-y[1];
  check(a%3===0 && b%3===0, "nonintegral ideal quotient");
  return reduce([a/3,b/3], L-1);
}
function beta(L) {
  let u=2,v=-1;
  for(let j=1;j<L;j++) [u,v]=[-2*u-v,u-v];
  return [u,v,3**L];
}
function pairing(s,y,L) {
  const [a,b]=mul(s,y,L), [u,v,d]=beta(L);
  return mod(a*u+b*v,d)/d;
}
function coefficient(j,L) { return reduce([[0,0],[1,0],[1,1]][j],L); }
function root(j,L) { return reduce([[1,0],[0,1],[-1,-1]][j],L); }
function phase(s,y,j,L) {
  const theta=2*Math.PI*mod(s.reduce((v,x,i)=>v+pairing(x,mul(y[i],coefficient(j,L),L),L),0),1);
  return [Math.cos(theta),Math.sin(theta)];
}
function cmul(u,v) { return [u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0]]; }
function scaled(v,s) { return v.map(x=>x*s); }
function norm(v) { return v[0]**2+v[1]**2; }
function same(u,v,m) { check(JSON.stringify(u)===JSON.stringify(v),m); }
function tuples(r) { return Array.from({length:3**r},(_,v)=>Array.from({length:r},()=>{const a=v%3;v=Math.floor(v/3);return a;})); }
function ring(L) { const [a,,b]=chart(L); return Array.from({length:a*b},(_,v)=>[Math.floor(v/b),v%b]); }
function gcd(a,b) { while(b) [a,b]=[b,a%b]; return a; }

for (const c of report.arithmetic_charts) {
  same(c.column_HNF_diagonal_cross_diagonal,chart(c.level),"ideal HNF");
  check(c.ring_cardinality===String(3**c.level),"wrong quotient cardinality");
  const [u,v,d]=beta(c.level);
  for(const [i,n] of [u,v].entries()) {
    const q=c.trace_pairing_power_basis_row[i];
    check(BigInt(q.numerator)*BigInt(d)===BigInt(q.denominator)*BigInt(n),"exact trace-dual denominator");
  }
}
let amplitudes=0,branches=0,sourcePairs=0;
check(report.physical_gaussian_merge_controls.length===8,"missing native source controls");
for(const c of report.physical_gaussian_merge_controls) {
  const L=c.parent_level,p=c.plan,indices=p.selected_input_indices,r=indices.length,s=c.integer_secret_calibration;
  check(s.every(x=>x[1]===0),"secret is not integer-embedded");
  same(indices,p.full_kernel_weights.flatMap((w,j)=>w ? [j] : []),"selected support");
  for(let k=0;k<p.vector_dimension;k++) {
    check(mod(c.native_input_labels.reduce((a,row,j)=>a+p.full_kernel_weights[j]*residue(row[k]),0),3)===0,"not a Gaussian dependence");
  }
  const selected=indices.map(j=>c.native_input_labels[j]),roots=p.qudit_input_multipliers;
  const labels=selected.map((row,j)=>row.map(y=>transport(y,roots[j],L)));
  for(let j=0;j<r;j++) check(mod(roots[j]**L,3)===p.full_kernel_weights[indices[j]],"illegal native rescaling");
  const joint=new Map();
  for(const old of tuples(r)) {
    let a=[3**(-r/2),0];
    for(let j=0;j<r;j++) a=cmul(a,phase(s,selected[j],old[j],L));
    const after=old.map((x,j)=>mod(roots[j]*x,3));
    const target=[after[0],...after.slice(1).map(x=>mod(x-after[0],3))];
    check(!joint.has(target.join(",")),"compiler not a permutation");
    joint.set(target.join(","),a);
  }
  check(c.all_branches.length===3**(r-1),"unrecorded measured outcomes");
  let total=0;
  for(const b of c.all_branches) {
    const x=[0,...b.difference_outcomes];
    let combined=Array.from({length:p.vector_dimension},()=>[0,0]),offset=Array.from({length:p.vector_dimension},()=>[0,0]);
    for(let j=0;j<r;j++) for(let k=0;k<p.vector_dimension;k++) {
      combined[k]=add(combined[k],mul(root(x[j],L),labels[j][k],L),L);
      offset[k]=add(offset[k],mul(coefficient(x[j],L),labels[j][k],L),L);
    }
    const child=combined.map(y=>quotient(y,L));
    same(child,b.child_label,"known descendant label");
    const theta=2*Math.PI*mod(s.reduce((a,y,k)=>a+pairing(y,offset[k],L),0),1);
    const global=[Math.cos(theta),Math.sin(theta)];
    let probability=0;
    for(let j=0;j<3;j++) {
      const a=joint.get([j,...b.difference_outcomes].join(","));
      const expected=scaled(cmul(global,phase(s,child,j,L-1)),3**(-r/2));
      for(let k=0;k<2;k++) {
        close(a[k],b.unnormalized_qudit_amplitudes[j][k],"physical native amplitude");
        close(a[k],expected[k],"retained global phase and child identity");
      }
      probability+=norm(a); amplitudes++;
    }
    close(probability,3**(1-r),"full-label-independent outcome law");
    close(probability,b.branch_probability,"charged outcome probability");
    total+=probability; branches++;
  }
  close(total,1,"full instrument norm"); close(c.full_output_norm,1,"producer norm");
  check(c.known_SUM_difference_count===r-1 && c.known_qudit_permutation_count===r,"unaccounted gates");
  check(!c.postselection_or_cloning_used && !p.selection_uses_current_higher_label_digits,"source model changed");
}
const conditioned=report.conditioned_exact_source_control;
const high=ring(3).filter(y=>residue(y)===1);
for(let x=0;x<3;x++) {
  const counts=new Map(ring(2).map(y=>[y.join(","),0]));
  for(const y of high) for(const z of high) {
    const child=quotient(add(transport(y,2,3),mul(root(x,3),z,3),3),3).join(",");
    counts.set(child,counts.get(child)+1);sourcePairs++;
  }
  const saved=conditioned.counts_conditioned_on_each_difference_outcome.find(b=>b.difference_outcome===x);
  for(const row of saved.child_label_counts) check(counts.get(row.label.join(","))===row.count && row.count===9,"conditional source posterior not uniform");
}
for(const c of report.level_power_classifications) {
  const values=[...new Set(Array.from({length:c.prime-1},(_,j)=>mod((j+1)**c.level,c.prime)))].sort((a,b)=>a-b);
  same(values,c.native_rescaling_residue_multipliers,"general prime power subgroup");
  check(values.length===(c.prime-1)/gcd(c.level,c.prime-1),"subgroup cardinality");
  check(c.arbitrary_nonzero_Gaussian_coefficients_available===(values.length===c.prime-1),"unjustified Gaussian compiler");
  check(!c.all_quantum_encodings_or_merges_excluded,"scoped gate became universal no-go");
}
const even=report.even_level_countercontrol;
same(transport([1,0],2,2),even.transformed_first_label,"even label transport");
check(residue(add(transport([1,0],2,2),[1,0],2))===2,"even-level falsifier disappeared");
const permutations=new Set();
for(const c of report.all_ternary_index_permutation_even_level_controls) {
  const a=c.affine_multiplier,b=c.affine_offset;
  const y=transport(mul(root(b,2),[1,0],2),a,2);
  same(y,c.transformed_label,"affine label transport");
  check(residue(y)===1 && c.transformed_low_residue===1,"permutation bypassed even-level gate");
  same(c.old_index_as_function_of_new,[0,1,2].map(j=>mod(a*j+b,3)),"wrong permutation");
  permutations.add(c.old_index_as_function_of_new.join(","));
}
check(permutations.size===6,"not all qutrit basis permutations covered");
for(const c of report.ternary_scaling_ledgers) {
  check(c.Gaussian_surjective_stages===c.modulus_log3-1 && c.remaining_subset_zero_sum_stages===c.modulus_log3,"wrong level count");
  check(!c.quasi_polynomial_bottleneck_removed,"false breakthrough promotion");
}
check(Object.values(report.claim_gate).every(v=>v===false),"claim gate promoted");
console.log(JSON.stringify({status:"independent_replay_passed",complex_amplitudes:amplitudes,
  complete_quantum_branches:branches,conditioned_source_pair_outcomes:sourcePairs,
  arithmetic_charts:report.arithmetic_charts.length,power_classifications:report.level_power_classifications.length,new_algorithm:false}));
