#!/usr/bin/env node
"use strict";

// Independent bounded checker: enumerates dependence witnesses, rather than
// reusing the producer's Gaussian algorithm, then executes elementary gates.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {sameProbability,readProbability,normalize,add,capped}=require("./dcp_adaptive_direction_rank_gate_crosscheck.js");
const {checkSignature}=require("./dcp_affine_fiber_rigidity_crosscheck.js");

function need(v,msg){if(!v)throw new Error(msg);}
function same(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function mod(a,q){return(a%q+q)%q;}
function parity(x){let p=0;for(;x;x&=x-1n)p^=1;return p;}
function hex(a){return "0x"+a.toString(16);}
function pythonCanonical(v){
  if(Array.isArray(v))return "["+v.map(pythonCanonical).join(", ")+"]";
  if(v&&typeof v==="object")return "{"+Object.keys(v).sort().map(k=>JSON.stringify(k)+": "+pythonCanonical(v[k])).join(", ")+"}";
  return JSON.stringify(v);
}
function source(P){
  need(P.kind==="POLYNOMIAL_DISJOINT_PARITY_KERNEL"&&P.descent_bits===2,"program kind");
  const A=P.coarse_labels,n=A.length,m=P.width;
  need(Number.isSafeInteger(n)&&n>=1&&n<=6&&Number.isSafeInteger(m)&&m>=(n+1)**2&&m<=256&&P.components===n,"bounded checker scope");
  need(A.every(row=>row.length===m&&row.every(a=>Number.isSafeInteger(a)&&a>=0&&a<4)),"coarse labels");
  const supports=P.disjoint_supports_hex.map(BigInt);need(supports.length===n+1,"support count");
  let used=0n;
  for(const u of supports){
    need(u>0n&&u<1n<<BigInt(m)&&!(u&used),"disjoint nonzero supports");used|=u;
    for(const row of A)need(row.reduce((s,a,i)=>s+((u>>BigInt(i))&1n? a:0),0)%2===0,"parity kernel");
  }
  // Independently reconstruct the high-pivot RREF kernel convention of the
  // PUBLIC preprocessing; valid supports alone would not prove low-bit lineage.
  const canonical=[];
  for(let j=0;j<n+1;j++){
    const rows=A.map(row=>row.slice(j*(n+1),(j+1)*(n+1)).reduce((v,a,i)=>v|((a&1)<<i),0));
    let used=0;const pivots=[];
    for(let bit=n;bit>=0;bit--){
      let k=used;while(k<n&&!(rows[k]>>bit&1))k++;
      if(k===n)continue;
      [rows[k],rows[used]]=[rows[used],rows[k]];
      for(let i=0;i<n;i++)if(i!==used&&(rows[i]>>bit&1))rows[i]^=rows[used];
      pivots.push(bit);used++;
    }
    let free=0;while(pivots.includes(free))free++;
    let u=1<<free;for(let i=0;i<used;i++)if(rows[i]>>free&1)u|=1<<pivots[i];
    canonical.push(BigInt(u)<<BigInt(j*(n+1)));
  }
  need(same(supports.map(hex),canonical.map(hex)),"actual parity-only canonical preprocessing");
  need(P.selection_access==="coarse-public-labels-only"&&P.uniform_efficient_program_supplied===true&&
       P.support_selection_access==="A-mod2-only-canonical-block-kernel"&&
       P.table_lookup_is_a_free_coherent_oracle===false&&P.full_assignment_lookup_rows===0&&
       P.algorithmic_baseline==="disjoint parity dependencies followed by binary Gaussian dependence"&&
       P.new_sieve_exponent_claimed===false,"program cost/access scope");
  return {A,n,m,supports};
}
function multiply(a,b){return normalize(a.p*b.p,a.e+b.e);}
function rationalDyadic(p,q){
  let a=p,b=q;while(b){const c=a%b;a=b;b=c;}p/=a;q/=a;
  let e=0;while(q>1n&&!(q&1n)){q>>=1n;e++;}need(q===1n,"expected exact dyadic");return normalize(p,e);
}
function checkMean(R){
  const w=R.physical_support_weights,n=w.length-1,v=readProbability(R.visibility),hist=Array.from({length:n+1},()=>new Map()),count=Array(n+1).fill(0);
  need(n>=1&&n<=2,"bounded independent noise census");
  for(let table=0;table<1<<(n*(n+1));table++){
    const cols=Array.from({length:n+1},(_,j)=>(table>>(n*j))&((1<<n)-1));let d=0;
    for(let candidate=1;candidate<1<<(n+1);candidate++){
      let x=0;cols.forEach((c,j)=>{if(candidate>>j&1)x^=c;});if(!x){d=candidate;break;}
    }
    const j=Math.floor(Math.log2(d));let weight=0;
    w.forEach((a,k)=>{if(d>>k&1)weight+=a;});count[j]++;hist[j].set(weight,(hist[j].get(weight)||0)+1);
  }
  const exponent=n*(n+1);let total=normalize(0n,0);
  need(R.first_dependence_law.length===n+1,"dependence law coverage");
  hist.forEach((h,j)=>{
    let value=normalize(0n,0);
    for(const [weight,multiplicity]of h)value=add(value,normalize(BigInt(multiplicity)*v.p**BigInt(weight),v.e*weight));
    total=add(total,normalize(value.p,value.e+exponent));
    const conditional=rationalDyadic(value.p,(1n<<BigInt(value.e))*BigInt(count[j]));
    const D=R.first_dependence_law[j];
    need(D.first_dependent_column_index===j,"dependence position");
    sameProbability(D.probability,BigInt(count[j]),exponent,"first dependency census");
    sameProbability(D.conditional_mean_visibility,conditional.p,conditional.e,"conditional width visibility");
  });
  sameProbability(R.native_mean_unfiltered_visibility,total.p,total.e,"parity-conditioned visibility census");
  need(R.conditioned_on_parity_B_only_not_full_coarse_A===true&&R.support_selection_may_read_second_low_bits===false,"mean conditioning scope");
}
function checkNativeNoise(R){
  const n=R.secret_vector_components,r=Math.floor(n/16),v=readProbability(R.visibility);
  let count=0n,choose=1n;for(let w=1;w<=r;w++){choose=choose*BigInt(n+2-w)/BigInt(w);count+=choose;}
  const b=capped(normalize(BigInt(n+1)*count,n)),a=normalize(v.p**BigInt(r+1),v.e*(r+1));
  const unit=1n<<BigInt(a.e),g=capped(normalize((unit+a.p)**BigInt(n+1)-unit**BigInt(n+1),n+a.e*(n+1)));
  const notB=normalize((1n<<BigInt(b.e))-b.p,b.e),upper=add(b,multiply(notB,g));
  need(R.original_copies===(n+1)**2&&R.low_block_support_cutoff===r,"native noise model parameters");
  sameProbability(R.some_block_has_a_short_nonempty_kernel_vector_probability_upper_bound,b.p,b.e,"short block union");
  sameProbability(R.mean_visibility_given_no_short_block_upper_bound,g.p,g.e,"Gaussian dependency noise upper");
  sameProbability(R.native_mean_unfiltered_visibility_upper_bound,upper.p,upper.e,"native source visibility upper");
  need(R.support_selection_is_parity_only_and_blocks_are_disjoint===true&&
       R.second_low_label_bits_and_original_Z_background_are_averaged===true&&
       R.fixed_full_coarse_matrix_inherits_this_probability_bound===false&&R.arbitrary_partial_or_collective_pairing_covered===false&&
       R.noise_promise==="independent balanced ORIGINAL-register dephasing","native noise scope");
}
function controls(S,x){return S.supports.map(u=>S.A.reduce((v,row,l)=>{
  let sum=0;row.forEach((a,i)=>{if(u>>BigInt(i)&1n)sum+=a*(x>>BigInt(i)&1n?-1:1);});
  need(sum%2===0,"integral signed half sum");
  return v|(BigInt(((sum/2)%2+2)%2)<<BigInt(l));
},0n));}
function dependence(S,x){
  const C=controls(S,x);let chosen=0;
  // Smallest nonzero integer dependence equals the producer's first-prefix
  // Gaussian dependence. Enumeration is checker-only and explicitly capped.
  for(let d=1;d<1<<C.length;d++){
    let sum=0n;C.forEach((v,j)=>{if(d>>j&1)sum^=v;});
    if(sum===0n){chosen=d;break;}
  }
  need(chosen>0,"nonempty dependence");
  return chosen;
}
function partner(S,x){const d=dependence(S,x);return x^S.supports.reduce((u,v,j)=>d>>j&1?u^v:u,0n);}
function execute(word,C){for(const g of C.gates){if(g.slice(1,-1).every(c=>word>>BigInt(c)&1n))word^=1n<<BigInt(g[g.length-1]);}return word;}
function checkCircuit(C,S){
  need(C.kind==="X_CX_CCX_COMPUTE_COPY_UNCOMPUTE"&&C.input_bits===S.m&&
       C.xor_output_bits_including_valid===S.m+1&&C.total_qubits===2*S.m+1+C.zero_work_bits_required,"evaluator registers");
  need(C.unknown_source_inverse_used===false&&C.hardware_transpilation_executed===false&&
       C.cost_order==="O(n*m+n^3+m) elementary reversible gates and work bits","evaluator scope");
  const counts={};
  for(const g of C.gates){
    need(["X","CX","CCX"].includes(g[0])&&g.length==={X:2,CX:3,CCX:4}[g[0]],"elementary gate kind");
    const bits=g.slice(1);need(new Set(bits).size===bits.length&&bits.every(b=>Number.isSafeInteger(b)&&b>=0&&b<C.total_qubits),"distinct gate wires");
    counts[g[0]]=(counts[g[0]]||0)+1;
  }
  need(Object.keys(counts).length===Object.keys(C.gate_counts).length&&
       Object.keys(counts).every(k=>counts[k]===C.gate_counts[k]),"actual gate counts");
  for(let x=0;x<1<<S.m;x++){
    const input=BigInt(x),y=partner(S,input),expected=input|(((1n<<BigInt(S.m))|y)<<BigInt(S.m));
    need(execute(input,C)===expected,"actual XOR-F gates or workspace cleanup");
    const target=(1n<<BigInt(S.m+1))-1n;
    need(execute(input|(target<<BigInt(S.m)),C)===(expected^(target<<BigInt(S.m))),"arbitrary XOR target");
  }
}
function checkFinite(C){
  const S=source(C.program),m=S.m,size=1<<m;
  need(m<=10&&C.original_assignments_exhausted===size,"finite census scope");
  need(C.reversible_XOR_F.program_sha256===crypto.createHash("sha256").update(pythonCanonical(C.program)).digest("hex"),"evaluator/program provenance");
  checkCircuit(C.reversible_XOR_F,S);
  const K=C.compiler,t=K.phase_bits,q=1n<<BigInt(t),A=K.public_labels_hex.map(row=>row.map(BigInt));
  need(A.length===S.n&&A.every((row,l)=>row.length===m&&row.every((a,i)=>a>=0n&&a<q&&Number(a%4n)===S.A[l][i]))&&
       K.descent_bits===2&&same(K.program,C.program),"original source/program binding");
  const accepted=[],pairs=[],hist={};
  for(let x=0;x<size;x++){
    const xx=BigInt(x),yy=partner(S,xx),y=Number(yy);
    need(yy!==xx&&partner(S,yy)===xx&&same(controls(S,xx).map(hex),controls(S,yy).map(hex)),"reciprocity/control invariance");
    let w=0;for(let z=xx^yy;z;z&=z-1n)w++;hist[w]=(hist[w]||0)+1;
    const delta=A.map(row=>mod(row.reduce((s,a,i)=>s+a*BigInt(((y>>i)&1)-((x>>i)&1)),0n),q));
    need(delta.every(v=>v%4n===0n),"global coarse preservation");
    if(!delta.some(v=>v!==0n))continue;
    accepted.push(x);
    if(x<y)pairs.push({first:x,second:y,descended_label_hex:delta.map(v=>hex(v/4n)),
                      physical_Hamming_width:w,unconditional_pair_probability:{numerator_hex:"0x1",denominator_binary_exponent:m-1}});
  }
  need(same(hist,C.physical_direction_width_histogram)&&same(K.accepted_assignments,accepted)&&same(K.pairs,pairs),"original widths/labels/admission");
  sameProbability(C.coarse_admission_probability,1n,0,"coarse admission");
  sameProbability(K.useful_descent_probability,BigInt(accepted.length),m,"useful paid probability");
  need(C.control_columns_invariant_under_partner===true&&K.accepted_XOR_F_calls===6&&K.failed_XOR_F_calls===4&&
       K.original_unknown_phase_qubits_per_attempt===m&&K.compiler_qubits_excluding_F_internal_work===3*m+4&&
       K.output_qubits_on_accepted_attempt===1&&K.pair_list_is_measurement_outcomes_not_parallel_outputs===true&&
       K.hardware_gate_export_backend_implemented===false&&K.secret_or_phase_evaluator_is_program_input===false&&
       K.same_A_source_resupply_or_inverse_supplied===false&&K.fresh_descended_labels_IID_certified===false,"compiler resource scope");
  const F=C.CNOT_Z_feedforward_receiver,pivots=S.supports.map(u=>{
    const v=u&-u;let j=0;while((1n<<BigInt(j))!==v)j++;return j;
  }),mask=pivots.reduce((v,p)=>v|(1<<p),0),first=[];
  S.supports.forEach((u,j)=>{for(let i=0;i<m;i++)if(i!==pivots[j]&&(u>>BigInt(i)&1n))first.push([pivots[j],i]);});
  need(same(F.first_stage_CNOTs,first)&&same(F.logical_pivot_wires,pivots)&&
       same(F.first_measured_Z_wires,Array.from({length:m},(_,i)=>i).filter(i=>!pivots.includes(i))),"actual first CNOT/Z chart");
  function cnots(x,gates){for(const [c,t]of gates)x^=((x>>c)&1)<<t;return x;}
  let index=0;const seen=new Set();
  for(let b=0;b<size;b++)if(!(b&mask)){
    const d=dependence(S,BigInt(b)),j=Math.log2(d&-d),output=pivots[j],second=[];
    pivots.forEach((p,k)=>{if(k!==j&&(d>>k&1))second.push([output,p]);});
    for(let outcome=0;outcome<1<<S.n;outcome++){
      const B=F.branches[index++],other=pivots.filter(p=>p!==output);
      const value=b|other.reduce((v,p,k)=>v|(((outcome>>k)&1)<<p),0);
      const x=cnots(cnots(value,second.slice().reverse()),first.slice().reverse()),
        y=cnots(cnots(value|(1<<output),second.slice().reverse()),first.slice().reverse());
      need(B.first_background_hex===hex(BigInt(b))&&B.second_outcome===outcome&&
           B.classical_dependence_hex===hex(BigInt(d))&&B.output_physical_wire===output&&
           same(B.second_stage_CNOTs,second)&&same(B.oriented_original_endpoints,[x,y])&&
           partner(S,BigInt(x))===BigInt(y),"feedforward original branch lineage");
      const delta=A.map(row=>mod(row.reduce((s,a,i)=>s+a*BigInt(((y>>i)&1)-((x>>i)&1)),0n),q));
      need(delta.every(v=>v%4n===0n)&&same(B.output_label_hex,delta.map(v=>hex(v/4n)))&&
           B.nonzero_label===delta.some(v=>v!==0n)&&B.original_pair_width===(BigInt(x^y).toString(2).split("1").length-1),"feedforward signed output");
      sameProbability(B.unconditional_Born_mass,2n,m,"feedforward Born mass");
      need(!seen.has(x)&&!seen.has(y),"duplicated physical endpoint");seen.add(x);seen.add(y);
    }
  }
  need(index===F.branches.length&&seen.size===size&&F.first_outcome_bits===m-S.n-1&&F.second_outcome_bits===S.n&&
       F.output_phase_qubits_per_actual_attempt===1&&F.classical_feedforward_not_coherent_Gaussian_required===true&&
       F.census_is_an_executed_quantum_experiment===false&&F.actual_attempt_follows_one_branch_not_all_outcomes===true,"feedforward all-outcome scope");
}
function checkFrontier(R){
  const n=R.secret_vector_components,t=R.phase_bits,m=(n+1)**2,s=Math.floor((t-1)/2),den=1n<<BigInt((t-2)*n);
  need(R.original_copies_per_two_bit_output_attempt===m&&R.two_bit_stages_without_overshooting_last_phase_bit===s&&
       R.remaining_phase_bits_after_these_stages===t-2*s&&
       R.ideal_no_zero_filter_original_copies_after_these_stages===(BigInt(m)**BigInt(s)).toString()&&
       R.ideal_no_failure_copies_including_last_one_bit_stage===(BigInt(n+1)**BigInt(t-1)).toString(),"recursive supply");
  sameProbability(R.pure_native_mean_useful_admission,den-1n,(t-2)*n,"native source mean");
  const log=Math.log2(n);
  sameProbability(R.one_over_n2_visibility,BigInt(n*n-1),2*log,"inverse quadratic visibility");
  sameProbability(R.one_over_n2_visibility_worst_width_factor,BigInt(n*n-1)**BigInt(m),2*log*m,"quadratic-noise factor");
  sameProbability(R.one_over_n_visibility_worst_width_factor,BigInt(n-1)**BigInt(m),log*m,"linear-noise lower factor");
  need(R.per_level_failures_and_fresh_batch_supply_must_be_added===true&&
       R.all_levels_source_and_noise_composition_certified===false&&R.new_Kuperberg_or_Regev_exponent===false&&
       R.visibility_factors_are_conservative_lower_bounds_NOT_noise_upper_bounds===true,"frontier scope");
}
function verify(R){
  need(R.contract_id==="coarse_only_disjoint_kernel_nonlinear_involution_v1"&&R.status==="LOCAL_DERIVATION_EXTERNAL_REVIEW_PENDING"&&
       R.accepted_speedup_candidate===false&&R.novelty_claim===false&&R.external_theorem_review_complete===false&&R.source_quantum_preparations_executed===0,"global admission");
  need(R.finite_controls.length===2,"finite coverage");R.finite_controls.forEach(checkFinite);
  need(R.parity_conditioned_noise_means.length===2,"conditional mean coverage");
  R.parity_conditioned_noise_means.forEach((M,i)=>{
    const weights=R.finite_controls[i].program.disjoint_supports_hex.map(u=>BigInt(u).toString(2).split("1").length-1);
    need(same(M.physical_support_weights,weights),"noise/source support binding");
    sameProbability(M.visibility,3n,2,"conditional noise grid");checkMean(M);
  });
  need(R.native_noise_upper_frontiers.length===12,"native noise coverage");
  R.native_noise_upper_frontiers.forEach((C,i)=>{
    const n=[32,64,128,256][Math.floor(i/3)],k=i%3;
    need(C.secret_vector_components===n,"native noise dimension grid");
    sameProbability(C.visibility,k===0?1n:BigInt(k===1?n-1:n*n-1),k===0?2:Math.log2(n)*(k===1?1:2),"native noise visibility grid");
    checkNativeNoise(C);
  });
  const N=R.selected_global_nonaffine_control,S=source(N.program);
  checkSignature(N.signature_certificate);
  need(N.selection==="explicit distinct nonzero signatures, NOT IID"&&S.n===6&&S.m===49&&
       N.nonaffinity_follows_from_global_rigidity_not_probe_statistics===true,"selected control scope");
  // The pointwise signature gate is checked here without loading a mutable
  // unrelated native probability artifact.
  const p=Array.from({length:S.m},(_,i)=>S.A.reduce((v,row,l)=>v|((row[i]&1)<<l),0));
  need(!p.includes(0)&&new Set(p).size===S.m&&N.signature_certificate.nonzero_distinct_signatures===true&&
       same(N.signature_certificate.public_labels_hex,S.A.map(row=>row.map(a=>hex(BigInt(a)))))&&
       same(N.signature_certificate.low_column_signatures_hex,p.map(v=>hex(BigInt(v))))&&
       N.signature_certificate.global_affine_mod4_automorphism_classification==="IDENTITY_ONLY","actual selected rigidity premise");
  need(N.sampled_original_inputs.length===32,"selected probe coverage");
  N.sampled_original_inputs.forEach(P=>{const x=BigInt(P.input_hex),y=partner(S,x);need(x>=0n&&x<(1n<<BigInt(S.m))&&y!==x&&hex(y)===P.partner_hex&&partner(S,y)===x&&
      same(controls(S,x).map(hex),controls(S,y).map(hex)),"large non-table partner probe");});
  need(R.supply_and_noise_frontiers.length===4,"frontier coverage");
  R.supply_and_noise_frontiers.forEach((C,i)=>{need(C.secret_vector_components===[4,8,16,32][i]&&C.phase_bits===C.secret_vector_components,"growing frontier grid");checkFrontier(C);});
  const s=R.scope;
  ["coarse_only_uniform_higher_label_theorem_applies_with_fresh_batches","original_higher_label_transcript_must_be_discarded",
   "elementary_reversible_gate_lists_exported_for_bounded_controls"].forEach(k=>need(s[k]===true,"scope premise: "+k));
  ["uniformity_conditioned_on_old_full_A","pure_zero_label_injection_backend_supplied","arbitrary_correlated_noise_covered",
   "coherent_Gaussian_control_is_free","polynomial_supply_for_growing_phase_bits","matched_classical_hardness_or_speedup_established",
   "improves_known_Gaussian_or_isotropic_asymptotics"].forEach(k=>need(s[k]===false,"scope expansion: "+k));
  return{status:"ok",finite_controls:2,reversible_evaluator_assignments:528,nonlinear_original_width:49,new_sieve_exponent:false};
}
module.exports={verify};
if(require.main===module){const file=process.argv[2]||path.resolve(__dirname,"../phase_workbench/dcp_disjoint_kernel_pairing.json");console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(file,"utf8")))));}
