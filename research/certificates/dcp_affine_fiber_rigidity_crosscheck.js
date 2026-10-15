#!/usr/bin/env node
"use strict";

// Original-assignment replay uses Mobius finite differences, independently of
// the Python parity expansion. No floating point is used for label arithmetic.
const fs = require("fs");
const path = require("path");
const {sameProbability} = require("./dcp_adaptive_direction_rank_gate_crosscheck.js");

function need(ok, message) { if (!ok) throw new Error(message); }
function same(a,b) { return JSON.stringify(a) === JSON.stringify(b); }
function parity(x) { let p=0; for (;x;x&=x-1) p^=1; return p; }
function map(rows,x,c) { return rows.reduce((y,r,i)=>y|(parity(r&x)<<i),0)^c; }
function rank(rows,m) {
  const a=rows.slice(); let r=0;
  for(let j=0;j<m;j++) {
    let k=r; while(k<a.length && !(a[k]&(1<<j))) k++;
    if(k===a.length) continue;
    [a[r],a[k]]=[a[k],a[r]];
    for(let i=r+1;i<a.length;i++) if(a[i]&(1<<j)) a[i]^=a[r];
    r++;
  }
  return r;
}
function canonicalHex(h) { need(typeof h==="string" && /^0x[0-9a-f]+$/.test(h),"invalid integer"); return BigInt(h); }
function mod(x,q) { return ((x%q)+q)%q; }
function checkSignature(C) {
  const A=C.public_labels_hex.map(row=>row.map(canonicalHex)), n=A.length, m=A[0].length;
  need(n>0&&m>0&&n<=4096&&m<=4096&&n*m<=2000000,"signature size");
  need(A.every(row=>row.length===m),"rectangular labels");
  const p=Array.from({length:m},(_,i)=>A.reduce((v,row,l)=>v|((row[i]&1n)<<BigInt(l)),0n));
  const zero=[],repeats=[];
  for(let i=0;i<m;i++) {
    if(p[i]===0n) zero.push(i);
    for(let j=0;j<i;j++) if(p[i]===p[j]) repeats.push([j,i]);
  }
  const good=zero.length===0&&repeats.length===0;
  need(C.secret_vector_components===n&&C.original_registers===m,"signature dimensions");
  need(same(C.low_column_signatures_hex,p.map(v=>"0x"+v.toString(16)))&&
       same(C.zero_signature_coordinates,zero)&&same(C.repeated_signature_pairs,repeats),"actual low signatures");
  need(C.nonzero_distinct_signatures===good&&C.global_affine_mod4_automorphism_classification===
       (good?"IDENTITY_ONLY":"UNKNOWN"),"signature gate classification");
  need(C.failure_of_gate_proves_a_nonidentity_automorphism===false&&
       C.all_binary_combinations_of_diagonal_forms_used===true&&
       C.full_label_adaptive_global_affine_selectors_covered===true&&
       C.partial_affine_proposals_excluded===false&&C.adaptive_affine_measurement_trees_excluded===false&&
       C.scalar_DHSP_lower_bound===false,"signature scope");
  // Reconstruct a separating form WITHOUT checking coordinate containment.
  for(let i=0;i<m;i++) for(let j=0;j<m;j++) if(p[i] && p[i]!==p[j]) {
    let u=0n;
    // A bit in output outside input, or two bits with different dot pairs.
    for(let l=0;l<n;l++) if((p[i]&(1n<<BigInt(l))) && !(p[j]&(1n<<BigInt(l)))) {
      u=1n<<BigInt(l); break;
    }
    if(!u) {
      const low=p[i]&-p[i], outside=p[j]&~p[i];
      u=low|(outside&-outside);
    }
    function bitParity(v) { let r=0; for(;v;v&=v-1n) r^=1; return r; }
    need(bitParity(p[i]&u)===1&&bitParity(p[j]&u)===0,"separating diagonal form");
  }
  return {A,p,n,m,good};
}
function delta(A,rows,c,x,q) {
  const y=map(rows,x,c);
  return A.map(row=>mod(row.reduce((v,a,i)=>v+a*BigInt(((y>>i)&1)-((x>>i)&1)),0n),q));
}
function coefficients(A,p,rows,c) {
  const m=rows.length, n=A.length, f0=delta(A,rows,c,0,4n), linear=Array.from({length:n},()=>[]);
  const singleton=Array.from({length:m},(_,j)=>delta(A,rows,c,1<<j,4n));
  for(let l=0;l<n;l++) for(let j=0;j<m;j++) linear[l].push(Number(mod(singleton[j][l]-f0[l],4n)));
  const quadratic=[];
  for(let j=0;j<m;j++) for(let k=j+1;k<m;k++) {
    const f=delta(A,rows,c,(1<<j)|(1<<k),4n);
    quadratic.push(f.map((v,l)=>Number(mod(v-singleton[j][l]-singleton[k][l]+f0[l],4n))));
  }
  const bad=[];
  for(let i=0;i<m;i++) for(let j=0;j<m;j++) if((rows[i]>>j)&1 && p[i] && p[i]!==p[j]) bad.push([i,j]);
  let global=true;
  for(let x=0;x<1<<m;x++) if(delta(A,rows,c,x,4n).some(v=>v!==0n)) global=false;
  const invertible=rank(rows,m)===m;
  return {
    linear_rows_hex:rows.map(r=>"0x"+r.toString(16)),affine_offset_hex:"0x"+c.toString(16),
    constant_mod4:f0.map(Number),linear_mod4_by_component:linear,
    quadratic_mod4_by_lexicographic_input_pair:quadratic,
    linear_map_invertible:invertible,preserves_all_original_assignments_mod4:global,
    is_global_affine_fibre_automorphism:invertible&&global,
    simultaneous_form_forbidden_entries:bad,all_coefficients_are_exact_integers:true,
  };
}
function checkFinite(C) {
  const {A,p,m,good}=checkSignature(C.signature_certificate), t=C.phase_bits;
  need(m<=3&&Number.isSafeInteger(t)&&t>=3&&t<=4096,"finite replay bounds");
  const q=1n<<BigInt(t);
  need(A.every(row=>row.every(a=>a<q)),"canonical full labels");
  const maps=[]; let count=0;
  for(let code=0;code<1<<(m*m);code++) {
    const rows=Array.from({length:m},(_,i)=>(code>>(m*(m-1-i)))&((1<<m)-1));
    if(rank(rows,m)!==m) continue;
    for(let c=0;c<1<<m;c++) {
      count++;
      let global=true;
      for(let x=0;x<1<<m;x++) if(delta(A,rows,c,x,4n).some(v=>v!==0n)) {global=false;break;}
      if(global) {
        const coeff=coefficients(A,p,rows,c);
        need(coeff.simultaneous_form_forbidden_entries.length===0,"form support counterexample");
        maps.push(coeff);
      }
    }
  }
  need(C.complete_affine_bijections_tested===count&&same(C.global_mod4_automorphisms,maps),"complete automorphism census");
  if(good) need(maps.length===1&&maps[0].affine_offset_hex==="0x0"&&
                 same(maps[0].linear_rows_hex,Array.from({length:m},(_,i)=>"0x"+(1<<i).toString(16))),"rigidity counterexample");
  if(C.partial_proposal_control) {
    const P=C.partial_proposal_control, rows=P.coefficients.linear_rows_hex.map(v=>Number(canonicalHex(v))),
      c=Number(canonicalHex(P.coefficients.affine_offset_hex));
    need(rows.length===m&&rows.every(r=>r>=0&&r<1<<m)&&c>=0&&c<1<<m,"proposal range");
    need(same(P.coefficients,coefficients(A,p,rows,c)),"proposal coefficient replay");
    const accepted=[],fixed=[],nonreciprocal=[];
    for(let x=0;x<1<<m;x++) {
      const y=map(rows,x,c);
      if(x===y) {fixed.push("0x"+x.toString(16));continue;}
      if(map(rows,y,c)!==x) {nonreciprocal.push("0x"+x.toString(16));continue;}
      const d=delta(A,rows,c,x,q);
      if(d.every(v=>v%4n===0n)&&d.some(v=>v!==0n)) accepted.push({
        x_hex:"0x"+x.toString(16),partner_hex:"0x"+y.toString(16),
        output_label_hex:d.map(v=>"0x"+(v/4n).toString(16))});
    }
    need(same(P.useful_reciprocal_assignments,accepted)&&same(P.fixed_assignments_hex,fixed)&&
         same(P.nonreciprocal_assignments_hex,nonreciprocal),"original useful pairs");
    sameProbability(P.paid_input_useful_acceptance_probability,BigInt(accepted.length),m,"paid useful mass");
    need(P.complete_assignment_census_is_a_scalable_algorithm===false,"finite census cost scope");
  }
}
function checkNative(R) {
  const n=R.secret_vector_components,m=R.original_registers;
  need(Number.isSafeInteger(n)&&n>0&&n<=4096&&Number.isSafeInteger(m)&&m>0&&m<=1000000,"native sizes");
  const zero=BigInt(m),repeat=BigInt(m)*BigInt(m-1)/2n,total=zero+repeat,den=1n<<BigInt(n),bad=total>den?den:total;
  sameProbability(R.zero_signature_union_upper_bound_uncapped,zero,n,"zero union");
  sameProbability(R.repeated_signature_union_upper_bound_uncapped,repeat,n,"birthday union");
  sameProbability(R.rigidity_gate_failure_probability_upper_bound,bad,n,"failure bound");
  sameProbability(R.identity_only_probability_lower_bound,den-bad,n,"rigidity bound");
  if(m<=1024) {
    let prod=1n;
    if(BigInt(m)>=den) prod=0n;
    else for(let j=1;j<=m;j++) prod*=den-BigInt(j);
    sameProbability(R.exact_signature_gate_probability,prod,n*m,"exact birthday product");
    need(R.exact_probability_omitted_due_to_work_cap===false,"exact probability cap");
  } else need(R.exact_signature_gate_probability===null&&R.exact_probability_omitted_due_to_work_cap===true,"honest exact product omission");
  need(R.bound_vacuous===(bad===den)&&R.native_low_labels==="IID uniform column signatures in F2^n BEFORE postselection"&&
       R.all_full_label_selected_global_affine_bijections_covered===true&&
       R.gate_failure_probability_is_probability_of_nontrivial_automorphism===false&&
       R.postselected_low_label_laws_inherit_native_probability===false&&
       R.partial_affine_acceptance_probability_bounded_here===false&&R.general_quantum_lower_bound===false,"native probability scope");
}
function verify(R) {
  need(R.contract_id==="global_affine_mod4_fibre_signature_rigidity_v1"&&
       R.status==="LOCAL_DERIVATION_EXTERNAL_REVIEW_PENDING"&&R.accepted_speedup_candidate===false&&
       R.novelty_claim===false&&R.external_theorem_review_complete===false&&R.source_quantum_preparations_executed===0,"global admission");
  const fixtures=[
    ["nonzero-antichain",[[1,1,0],[1,0,1],[0,1,1]]],
    ["comparable-BUT-distinct-signatures-partial-success",[[1,0,5],[0,1,1]]],
    ["repeated-low-signatures-useful-swap",[[1,5],[2,2]]],
    ["zero-signature-useful-translation",[[1,4]]],
    ["duplicate-signatures-are-NOT-sufficient",[[1,1],[0,2]]],
    ["one-nonzero-column",[[3]]],
  ];
  need(R.finite_controls.length===fixtures.length,"finite coverage");
  R.finite_controls.forEach((C,i)=>{
    need(C.control_id===fixtures[i][0]&&same(C.signature_certificate.public_labels_hex,
         fixtures[i][1].map(row=>row.map(v=>"0x"+v.toString(16))))&&C.phase_bits===3,"finite source binding");
    checkFinite(C);
  });
  need(R.polynomial_signature_controls.length===3,"polynomial control coverage");
  R.polynomial_signature_controls.forEach((C,i)=>{
    const n=[32,64,128][i];
    need(C.seed===3217+n&&C.sampling==="unfiltered pseudorandom finite control, NOT source theorem"&&
         C.certificate.secret_vector_components===n&&C.certificate.original_registers===3*n,"unfiltered sample scope");
    checkSignature(C.certificate);
  });
  need(R.native_probability_frontiers.length===14,"native frontier coverage");
  R.native_probability_frontiers.forEach((C,i)=>{
    const n=[1,8,32,64,128,256,512][Math.floor(i/2)];
    need(C.secret_vector_components===n&&C.original_registers===3*n+i%2,"native frontier grid");checkNative(C);
  });
  const s=R.scope;
  need(s.relation==="A P(x) = A x mod4 for EVERY original Boolean assignment"&&
       s.map_class==="globally Boolean-affine bijections P(x)=Lx XOR c"&&
       s.higher_descent_moduli_inherit_necessary_mod4_obstruction===true&&
       s.full_public_label_adaptive_choice_of_L_and_c_allowed===true,"scope premise");
  ["one_bit_mod2_descent_covered","partial_proposals_excluded","adaptive_measurement_trees_excluded",
   "nonlinear_pairing_excluded","general_quantum_lower_bound","efficient_coarse_only_pairing_program_supplied",
   "source_joint_noise_or_growing_level_composition_resolved"].forEach(k=>need(s[k]===false,"scope expansion: "+k));
  return {status:"ok",finite_controls:6,polynomial_controls:3,native_frontiers:14,general_quantum_lower_bound:false};
}
module.exports={verify,checkSignature};
if(require.main===module) {
  const file=process.argv[2]||path.resolve(__dirname,"../phase_workbench/dcp_affine_fiber_rigidity.json");
  console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(file,"utf8")))));
}
