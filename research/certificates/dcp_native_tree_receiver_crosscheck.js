// Independent untruncated graph and exact fixed-schedule resource replay.
// Does not certify a low-level gate export or natural-source noise assumptions.
"use strict";
const fs = require("fs"), path = require("path"), assert = require("assert/strict");
const filename = process.argv[2] || path.join(__dirname, "../phase_workbench/dcp_native_tree_receiver.json");
const report = JSON.parse(fs.readFileSync(filename, "utf8"));
const eq = (a,b) => assert.deepEqual(a,b);
const pow2ceil = x => 2**Math.ceil(Math.log2(x));
const comps = p => p*Math.log2(p)*(Math.log2(p)+1)/4;
const parity = x => { let v=0; while(x) {v^=x&1; x>>>=1;} return v; };
const hash = (x,H,c) => H.reduce((v,h,j)=>v+(parity(x&h)<<j),0)^c;
const choose = (n,k) => { let v=1; for(let i=1;i<=k;i++) v=v*(n-i+1)/i; return Math.round(v); };
const gcd = (a,b) => b===0n?a:gcd(b,a%b);
const rat = (a,b=1n) => { const g=gcd(a,b); return [a/g,b/g]; };
const add = (a,b) => rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const mul = (a,b) => rat(a[0]*b[0],a[1]*b[1]);
const dyadic = a => { let d=a[1], e=0; while(d>1n && d%2n===0n) {d/=2n;e++;} eq(d,1n); return {numerator_hex:"0x"+a[0].toString(16),denominator_binary_exponent:e}; };

function costs(P) {
  const a=P.depth,b=P.chunk_components,k=2**a,L=4**b,n=b*(a+1),m=P.width,B=m/k,C=P.capacity;
  assert(Number.isInteger(a)&&a>=1&&a<=3&&b===1&&m<=32); // Saved controls only.
  assert(Number.isInteger(C)&&C>=L);
  let w=1; while(choose(B,w)<L) w++;
  let f=[1n,1n]; const perturb=rat(BigInt(L-1),BigInt(L*L));
  for(let r=0;r<a;r++) f=add(mul(f,f),perturb);
  const M=add(f,rat(BigInt(L-1),BigInt(L))), mm=add(M,[-1n,1n]);
  const recommended=256*Number((M[0]+M[1]-1n)/M[1])*k*L;
  let g=0; while((1n<<BigInt(g))*mm[1]<4n*mm[0])g++;
  const theta=rat(1n,1n<<BigInt(g));
  let lower=add(mul(theta,theta),mul([-2n,1n],mul(mul(mul(theta,theta),theta),mm)));
  if(k>2) lower=add(lower,mul([-1n,8n],mul(theta,theta)));
  let slots=L,levels=[],candidate=0,comparison=0,scans=0,copies=0;
  let workspace=k*L*(1+m+2*n)+(k-1)*Math.max(1,Math.floor(Math.log2(k-1))+1)+(k-2);
  for(let r=1;r<a;r++) {
    const cells=slots**2,padded=pow2ceil(cells),retained=Math.min(C,cells),nodes=k/2**r,cmp=comps(padded);
    levels.push({level:r,nodes,child_slots:slots,candidate_cells:cells,padded_cells:padded,retained_slots:retained,forward_comparators:cmp});
    candidate+=nodes*cells; comparison+=2*nodes*cmp; scans+=2*nodes*padded; copies+=2*nodes*retained;
    workspace+=nodes*((padded+retained)*(1+m+2*n)+(padded+1)*(Math.floor(Math.log2(cells+1))+1)+cmp);
    slots=retained;
  }
  const padded=pow2ceil(2*slots),cmp=comps(padded),key=2*n+g+1;
  const counter=Math.floor(Math.log2(slots**2))+1,record=key+2+m,scan=key+3*counter+3*m;
  const rootWork=padded*record+(padded+1)*scan+cmp;
  workspace+=rootWork; comparison+=2*cmp;scans+=2*padded;
  const metrics={candidate_cell_evaluations:2*candidate,leaf_record_evaluations:2*k*L,
    root_record_evaluations:4*slots,comparators:comparison,list_scan_steps:scans,
    retained_record_copies:copies,overflow_prefix_steps:2*(k-2)};
  const R={depth:a,chunk_components:b,components:n,leaf_count:k,leaf_list_length:L,block_width:B,
    original_registers:m,leaf_support_weight:w,physical_mask_width:k*w,capacity:C,recommended_capacity:recommended,
    hash_bits:g,public_affine_seed_bits:g*(m+1),nonroot_levels:levels,root_child_slots:slots,
    root_join:{padded_records:padded,persistent_workspace_bits:rootWork}};
  for(const [s,v] of Object.entries(metrics))R["one_XOR_F_"+s]=v;
  Object.assign(R,{persistent_workspace_bits:workspace,accepted_six_XOR_F_comparators:6*comparison,
    failed_four_XOR_F_comparators:4*comparison,compiler_live_qubits_excluding_arithmetic_scratch:workspace+3*m+4,
    polynomial_arithmetic_scratch_excluded:true,
    overflow_is_seed_independent:true,moment_overflow_lower_bound_applicable:C>=recommended,
    moment_coarse_lower_bound_IF_source_premises:C>=recommended?dyadic(lower):null,
    coherent_RAM_assumed:false,hardware_gate_export_implemented:false,
    abstract_clean_basis_wire_interpreter_implemented:true,
    time_and_space_form:"O(k*C^2*poly(n,m,log C)); fixed-address histories retained",
    one_output_recursion_supply_removed:false});
  eq(P.resource_ledger,R);eq(P.kind,"NATIVE_Z4_BOUNDED_TREE_SORT_JOIN");eq(P.descent_bits,2);
  eq(P.overflow_policy,"REJECT_WHOLE_ATTEMPT");eq(P.seed_conditioned_on_success,false);
  eq(P.uniform_efficient_program_supplied,false);eq(P.table_lookup_is_a_free_coherent_oracle,false);
  eq(P.selection_access,"coarse-labels-and-independent-unfiltered-affine-seed");
  return {R,metrics};
}

function supports(B,w,L,start) {
  const result=[];
  function go(i,left,mask) {
    if(!left) {result.push(mask);return;}
    for(let j=i;j<=B-left;j++)go(j+1,left-1,mask+2**(start+j));
  }
  go(0,w,0);return result.slice(0,L);
}
function signed(A,x,mask) {
  return A.map(row=>((row.reduce((v,a,i)=>v+((mask&2**i)?a*(1-2*((x>>>i)&1)):0),0)%4)+4)%4);
}
function reference(P,x) {
  const {R}=costs(P),A=P.coarse_labels,H=P.hash_rows_hex.map(Number),c=Number(P.hash_offset_hex);
  eq(A.length,R.components);assert(A.every(row=>row.length===P.width&&row.every(a=>Number.isInteger(a)&&a>=0&&a<4)));
  eq(H.length,R.hash_bits);assert(H.every(h=>Number.isInteger(h)&&h>=0&&h<2**P.width));
  assert(c>=0&&c<2**H.length);
  let current=Array.from({length:R.leaf_count},(_,j)=>supports(R.block_width,R.leaf_support_weight,R.leaf_list_length,j*R.block_width).map(mask=>({mask,sum:signed(A,x,mask)})));
  let overflow=false;
  for(let level=1;level<P.depth;level++) {
    const next=[];
    for(let j=0;j<current.length;j+=2) {
      const records=[];
      for(const u of current[j])for(const v of current[j+1]) {
        const sum=u.sum.map((s,i)=>(s+v.sum[i])%4);
        if(sum.slice((level-1)*P.chunk_components,level*P.chunk_components).every(s=>s===0))records.push({mask:u.mask^v.mask,sum});
      }
      overflow||=records.length>P.capacity;
      next.push(records); // Full untruncated relation, independent of production compaction.
    }
    current=next;
  }
  const neighbors=[];let rootCount=0;
  for(const u of current[0])for(const v of current[1]) {
    if(u.sum.every((s,i)=>(s+v.sum[i])%4===0)) {
      const y=x^u.mask^v.mask;
      if(hash(u.mask^v.mask,H,0)===0)rootCount++;
      if(hash(y,H,c)===0)neighbors.push(y);
    }
  }
  const y=!overflow&&hash(x,H,c)===0&&neighbors.length===1?neighbors[0]:null;
  return {output:y===null?0:2**P.width+y,overflow,neighbors,rootCount};
}
eq(report.contract_id,"native_Z4_bounded_tree_clean_XOR_F_v1");
eq(report.status,"CLEAN_BASIS_PROGRAM_EXTERNAL_REVIEW_PENDING");
for(const flag of ["accepted_speedup_candidate","novelty_claim","external_theorem_review_complete","hardware_gate_export_implemented","selected_controls_are_native_source_probability_estimates"])eq(report[flag],false);
eq(report.source_quantum_preparations_executed,0);eq(report.abstract_clean_basis_wire_interpreter_implemented,true);
eq(report.scope,{whole_attempt_overflow_rejection:true,root_and_nonroot_histories_uncomputed:true,
  independent_uniform_coarse_labels_required_for_native_mean_bound:true,natural_source_noise_or_hardness_certified:false,
  one_output_recursive_supply_removed:false,improves_known_DCP_exponents:false,latent_error_comparison_used:false});
eq(report.finite_controls.length,6);
let checks=0;
for(const control of report.finite_controls) {
  const P=control.program,{R,metrics}=costs(P);
  eq(P.coarse_labels,control.full_labels.map(row=>row.map(a=>a%4)));
  for(const row of control.evaluations) {
    const ref=reference(P,row.assignment);
    eq(row.output,ref.output);eq(row.whole_attempt_overflow,ref.overflow);eq(row.workspace_clean,true);
    eq(row.metrics,metrics);eq(row.persistent_workspace_bits,R.persistent_workspace_bits);
    eq(row.node_overflows.some(Boolean),ref.overflow);
    if(!ref.overflow)eq(row.truncated_root_neighbor_count_not_accepted_on_overflow,ref.rootCount);
    checks++;
  }
  if(control.known_untruncated_edge) {
    const [x,y]=control.known_untruncated_edge,rx=reference(P,x),ry=reference(P,y);
    assert(rx.neighbors.includes(y)&&ry.neighbors.includes(x));eq(rx.overflow,true);eq(ry.overflow,false);
  }
  if(control.known_reciprocal_pair) {
    const [x,y]=control.known_reciprocal_pair;
    eq(reference(P,x).output,2**P.width+y);eq(reference(P,y).output,2**P.width+x);
  }
}
const K=report.six_call_instrument,P=K.program,A=K.public_labels_hex.map(row=>row.map(Number));
costs(P);eq(K.accepted_XOR_F_calls,6);eq(K.failed_XOR_F_calls,4);
eq(K.hardware_gate_export_backend_implemented,false);eq(K.output_qubits_on_accepted_attempt,1);
eq(K.original_unknown_phase_qubits_per_attempt,P.width);eq(K.compiler_qubits_excluding_F_internal_work,3*P.width+4);
eq(P.coarse_labels,A.map(row=>row.map(a=>a%4)));
const accepted=[],pairs=[];
for(let x=0;x<2**P.width;x++) {
  const ref=reference(P,x);if(!ref.output)continue;
  const y=ref.output-2**P.width;if(reference(P,y).output!==2**P.width+x)continue;
  const delta=A.map(row=>((row.reduce((s,a,i)=>s+a*(((y>>>i)&1)-((x>>>i)&1)),0)%8)+8)%8);
  if(delta.every(d=>d%4===0)&&delta.some(Boolean)) {
    accepted.push(x);
    if(x<y)pairs.push({first:x,second:y,descended_label_hex:delta.map(d=>"0x"+(d/4).toString(16)),
      physical_Hamming_width:((x^y).toString(2).match(/1/g)||[]).length,
      unconditional_pair_probability:{numerator_hex:"0x1",denominator_binary_exponent:P.width-1}});
  }
}
eq(K.accepted_assignments,accepted);eq(K.pairs,pairs);assert(pairs.length>0);
eq(K.useful_descent_probability,dyadic(rat(BigInt(accepted.length),1n<<BigInt(P.width))));
console.log(JSON.stringify({status:"ok",native_assignment_checks:checks,reciprocal_physical_pairs:pairs.length,hardware_gate_export_implemented:false}));
