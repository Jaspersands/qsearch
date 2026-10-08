"use strict";
// Independent F3 and exact Q(zeta_3) replay; no Python or supplied simulators.
const fs=require("fs"), path=require("path"), crypto=require("crypto");
const {check,same,rat,zero,one,add,sub,mul,div,str,parse,cmp,mod,field}=require("./cyclotomic_exact.js");
const rootDir=path.resolve(__dirname,"../.."), K=field(3);
const source=process.argv[2]||path.join(rootDir,"research/reductions/vector_centre_state_hsp_receiver.json");
const R=JSON.parse(fs.readFileSync(source,"utf8"));
const omega=n=>K.powers[mod(n,3)];
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
const number=a=>Number(a[0])/Number(a[1]);
const near=(a,b,msg)=>check(Number.isFinite(a)&&Math.abs(a-b)<3e-10,msg);
const asRat=z=>{check(cmp(z[1],zero)===0n,"exact physical probability is rational");return z[0];};
const words=n=>n?words(n-1).flatMap(v=>[0,1,2].map(a=>v.concat(a))):[[]];
function word(v,n) {check(Array.isArray(v)&&v.length===n&&v.every(a=>Number.isInteger(a)&&a>=0&&a<3),"canonical F3 word");return v;}
const sum=(frame,c,n)=>Array.from({length:n},(_,j)=>mod(frame.reduce((s,v,i)=>s+v[j]*c[i],0),3));
function reduced(rows,n) {
  const A=rows.map(v=>word(v,n).slice()), piv=[];let r=0;
  for(let j=0;j<n&&r<A.length;j++) {
    const i=A.findIndex((v,i)=>i>=r&&v[j]);if(i<0)continue;
    [A[r],A[i]]=[A[i],A[r]];const inv=A[r][j]===1?1:2;
    A[r]=A[r].map(a=>a*inv%3);
    for(let i=0;i<A.length;i++)if(i!==r){const c=A[i][j];A[i]=A[i].map((a,k)=>mod(a-c*A[r][k],3));}
    piv.push(j);r++;
  }
  return [A.slice(0,r),piv];
}
const rank=(A,n)=>reduced(A,n)[1].length;
const member=(A,v)=>rank(A.concat([v]),v.length)===rank(A,v.length);
function kernel(A,n) {
  const [rows,piv]=reduced(A,n);
  return Array.from({length:n},(_,j)=>j).filter(j=>!piv.includes(j)).map(j=>{
    const v=Array(n).fill(0);v[j]=1;piv.forEach((q,i)=>v[q]=mod(-rows[i][j],3));return v;
  });
}
function sameSpan(A,B,n,msg) {check(rank(A,n)===rank(B,n)&&A.every(v=>member(B,v)),msg);}
function ledger(L) {
  const d=L.quotient_dimension,k=L.centre_dimension,b=L.failure_bits,e=parse(L.original_gap_lower);
  check([d,k,b].every(a=>Number.isInteger(a)&&a>0)&&cmp(e,zero)>0n&&cmp(e,one)<=0n,"positive exact ledger parameters");
  const W=BigInt((k+1)**2),H=32n*W*BigInt(4*d+b+2),ceil=a=>(a[0]+a[1]-1n)/a[1];
  const N=ceil(div(rat(2n*(2n*(W+H)+8n*BigInt(2*k+b+2))),e));
  const M=ceil(div(rat(2n*BigInt(2*(d+k)+b+2)),e));
  const expected={zero_sum_window:Number(W),conditional_modulus_defect_threshold:"1/16",purified_commutator_squared_upper:"2",
    nontrivial_ternary_root_squared_distance_exact:"3",required_included_witnesses_per_unfixed_central_element:Number(H),
    original_central_measurement_count:Number(N),fresh_original_final_copy_count:Number(M),total_original_copy_cap:Number(N+M),
    known_controlled_R_call_cap:Number(2n*N+M),conditional_quantum_register_buffer_cap:Number(W),leftover_registers_strictly_less_than:Number(W)};
  for(const [key,v]of Object.entries(expected))same(L[key],v,"exact resource ledger: "+key);
  const eta=rat(1n,2n**BigInt(b+2));
  for(const key of ["central_count_failure_upper","all_pair_overgroup_failure_upper","final_decoder_failure_upper"])same(L[key],str(eta),"component failure bound");
  same(L.total_ideal_failure_upper,str(mul(rat(3n),eta)),"total failure bound");
  check(cmp(mul(rat(N),div(e,rat(2n))),rat(2n*(W+H)+8n*BigInt(2*k+b+2)))>=0n,"central witness count quota");
  check(H>=32n*W*BigInt(4*d+b+2),"all ordered-pair union, not chosen basis only");
  check(L.same_central_sector_collision_required===false&&L.minimum_conditional_gap_assumed===false&&L.original_IID_same_state_source_required===true&&L.unknown_state_inverse_or_cloning_used===false&&L.approximate_input_or_action_error_certified===false,"source and ideal precision scope");
}
function coverage(C,full=false) {
  const k=C.centre_dimension,W=(k+1)**2,N=C.original_inputs;
  check(Number.isInteger(N)&&N>=0&&C.zero_sum_window===W,"coverage dimension");
  const tail=C.leftover_original_indices;
  check(tail.length<W&&new Set(tail).size===tail.length&&tail.every(i=>Number.isInteger(i)&&i>=0&&i<N),"bounded unique leftover tail");
  check(C.leftover_characters.length===tail.length,"all leftover labels accounted");C.leftover_characters.forEach(v=>word(v,k));
  check(C.included_original_inputs+tail.length===N&&C.maximum_live_conditional_registers<=W&&C.maximum_live_conditional_registers<=N,"original-input coverage and memory");
  check(C.block_count<=C.included_original_inputs&&C.included_original_inputs<=W*C.block_count&&C.Gaussian_kernel_calls<=C.block_count*(k+2),"bounded supports and kernel calls");
  check(C.support_selection_reads_internal_measurement_outcomes===false&&C.retained_characters_claimed_IID===false&&C.distinct_indices_certify_physical_IID_copies===false,"conditioning scope");
  if(!full){check(C.complete_blocks_retained===false&&C.blocks===null,"summary is NOT a replayable full block transcript");return;}
  check(C.complete_blocks_retained===true&&C.complete_original_characters.length===N,"coverage-only full transcript");
  const labels=C.complete_original_characters;labels.forEach(v=>word(v,k));
  const live=new Map(), hash=crypto.createHash("sha256");let j=0,used=0;
  for(let i=0;i<N;i++) {
    live.set(i,labels[i]);
    if(live.size<W)continue;
    const b=C.blocks[j++];check(!!b&&b.original_indices.length>0&&b.original_indices.length<=W,"one nonempty bounded block per full window");
    check(new Set(b.original_indices).size===b.original_indices.length&&b.central_characters.length===b.original_indices.length,"no conditional input reused inside block");
    b.original_indices.forEach((id,t)=>{check(live.has(id),"selected original register is actually live");same(b.central_characters[t],live.get(id),"central label attached to actual input");live.delete(id);});
    const z=Array.from({length:k},(_,q)=>mod(b.central_characters.reduce((s,v)=>s+v[q],0),3));
    check(z.every(a=>a===0),"FULL vector cocycle sum cancels");same(b.exact_sum,z,"exact vector sum record");
    check(b.copies_consumed===b.original_indices.length&&b.same_sector_copies_assumed===false,"paid heterogeneous copies");
    hash.update(JSON.stringify(b)+"\n");used+=b.copies_consumed;
  }
  same([...live.keys()],tail,"complete discarded tail");same([...live.values()],C.leftover_characters,"tail label identities");
  check(j===C.blocks.length&&j===C.block_count&&used===C.included_original_inputs,"complete block ledger");
  same(hash.digest("hex"),C.complete_selected_block_stream_sha256,"complete block stream digest");
  const buckets=new Map();labels.forEach(v=>{const s=JSON.stringify(v);buckets.set(s,(buckets.get(s)||0)+1);});
  check(buckets.size===C.distinct_label_count&&Math.max(...buckets.values())===C.largest_identical_sector_bucket,"no invented identical-sector population");
  check(C.full_confidence_copy_ledger_met_by_this_pool===false&&C.large_pool_is_a_coverage_control_not_an_algorithm_scaling_claim===true,"coverage control is NOT full confidence algorithm scaling");
}
function vectorInstrument(c) {
  const labels=c.central_characters,r=labels.length,k=labels[0].length;
  labels.forEach(v=>word(v,k));check(r>0&&r<=3&&Array.from({length:k},(_,j)=>labels.reduce((s,v)=>s+v[j],0)%3).every(a=>!a),"heterogeneous vector-zero-sum instrument");
  const coeff=c.input_integer_amplitudes,phase=c.input_root_phase_exponents;
  check(coeff.length===r&&phase.length===r,"actual exact source vectors");
  let D=1n;coeff.forEach((v,i)=>{check(v.length===9&&v.every(Number.isInteger),"integer nonstabilizer coefficients");word(phase[i],9);const n=v.reduce((s,a)=>s+BigInt(a)**2n,0n);check(n>0n,"nonzero conditional vector");D*=n;near(c.input_amplitude_squared_norms[i],Number(n),"input norm");
    v.forEach((a,j)=>{const p=phase[i][j],z=c.input_amplitudes_real_imag[i][j];near(z[0],a*(p?-.5:1),"source real amplitude");near(z[1],a*(p===1?Math.sqrt(3)/2:p===2?-Math.sqrt(3)/2:0),"source imaginary amplitude");});});
  const inputs=words(2*r),points=words(2);same(c.full_character_words,points,"all block characters");
  for(let iy=0;iy<9;iy++) {
    const y=points[iy],out=Array.from({length:9**r},()=>K.F());
    for(const t of inputs) {
      let amp=1n,p=0;for(let i=0;i<r;i++){const u=3*t[2*i]+t[2*i+1];amp*=BigInt(coeff[i][u]);p+=phase[i][u];}if(!amp)continue;
      for(const [a,b]of points) {
        let q=p-dot(y,[a,b]),index=0;
        for(let i=0;i<r;i++){q+=labels[i][0]*b*t[2*i]+b*t[2*i+1];index=index*9+3*((t[2*i]+a)%3)+t[2*i+1];}
        out[index]=K.plus(out[index],K.scale(omega(q),rat(amp)));
      }
    }
    const norm=out.reduce((s,z)=>add(s,asRat(K.times(K.conj(z),z))),zero),p=div(norm,rat(81n*D));
    near(c.literal_Kraus_probabilities[iy],number(p),"independent exact heterogeneous Kraus branch");near(c.character_law_probabilities[iy],number(p),"exact block Fourier law");
  }
  check(c.actual_conditional_copies_consumed===r&&c.known_controlled_R_calls===r&&c.physical_qutrits===2*r&&c.all_outcomes_retained===true&&c.identical_conditional_state_promise_used===false&&c.full_unprepared_workspace_action_claimed_linear===false,"whole block scope");
}
const comm=(x,y,k)=>[mod(x[1]*y[0]-y[1]*x[0],3),...Array(k-1).fill(0)];
function section(c,t,k) {
  const s=c.quotient_frame.length,x=sum(c.quotient_frame,t.slice(0,s),2),z=sum(c.central_complement,t.slice(s),k);
  z[0]=mod(z[0]+2*x[1]*x[0],3);return [x,z];
}
function sourceVector(lam,r) {
  const j=mod(-dot(lam,r.calibration_tau_b),3),coeff=Array(9).fill(0),phase=Array(9).fill(0);
  for(let t=0;t<3;t++)if(r.source_kind==="nonabelian-preimage"||t===0){coeff[3*t+j]=1;phase[3*t+j]=mod(dot(lam,r.calibration_tau_a)*t,3);}
  return [coeff,phase];
}
function finalInstrument(r) {
  const c=r.quotient_chart,k=r.ledger.centre_dimension,points=words(c.dimension),gamma=parse(r.spectrum_uniform_mixture_weight);
  const labels=words(k).filter(v=>r.fixed_central_axes.every(j=>!v[j])),f=r.literal_final_original_instrument;
  same(f.full_character_words,points,"all final original-state characters");
  points.forEach((y,iy)=>{
    let probability=zero;
    for(const lam of labels) {
      const [coeff,ph]=sourceVector(lam,r),D=BigInt(coeff.reduce((s,a)=>s+a*a,0)),out=Array.from({length:9},()=>K.F());
      for(const t of points) {
        const [[a,b],z]=section(c,t,k);
        for(let u=0;u<9;u++)if(coeff[u]) {
          const i=Math.floor(u/3),j=u%3,index=3*((i+a)%3)+j;
          out[index]=K.plus(out[index],omega(ph[u]+dot(lam,z)+lam[0]*b*i+b*j-dot(y,t)));
        }
      }
      const norm=out.reduce((s,z)=>add(s,asRat(K.times(K.conj(z),z))),zero);
      let weight=div(gamma,rat(BigInt(labels.length)));if(lam.every(a=>!a))weight=add(weight,sub(one,gamma));
      probability=add(probability,mul(weight,div(norm,rat(BigInt(points.length)**2n*D))));
    }
    same(f.exact_mixture_probabilities[iy],str(probability),"exact ORIGINAL mixed-source law");
    near(f.literal_Kraus_probabilities[iy],number(probability),"literal final original-state Kraus branch");near(f.original_moment_Fourier_probabilities[iy],number(probability),"final original Fourier law");
    let closed=zero;
    if(member(r.final_law_active_uniform_character_frame,y))closed=div(gamma,rat(3n**BigInt(r.final_law_active_uniform_character_frame.length)));
    if(member(r.final_law_inactive_uniform_character_frame,y))closed=add(closed,div(sub(one,gamma),rat(3n**BigInt(r.final_law_inactive_uniform_character_frame.length))));
    same(str(closed),str(probability),"executed sampler's mixture law equals physical instrument");
  });
  check(f.uses_fresh_original_copies_not_selected_conditional_states===true&&f.all_outcomes_retained===true&&f.large_density_table_is_algorithm_input===false,"final source access");
}
function baseline(r) {
  const B=r.basis_readout_baseline,k=r.ledger.centre_dimension,A=B.central_label_rows;
  check(B.status==="SOURCE_SPECIFIC_BASIS_READOUT_RECOVERED"&&A.length===B.alternative_fresh_copy_count&&A.length===r.ledger.fresh_original_final_copy_count,"actual alternative baseline copies");
  A.forEach((lam,i)=>{word(lam,k);same(B.clock_computational_basis_outcomes[i],mod(-dot(lam,r.calibration_tau_b),3),"actual clock readout");
    same(mod(dot(lam,B.recovered_tau_b_mod_fixed_centre),3),mod(dot(lam,r.calibration_tau_b),3),"baseline recovered clock equations");
    if(r.source_kind==="nonabelian-preimage"){same(B.first_qutrit_Fourier_basis_indices[i],mod(dot(lam,r.calibration_tau_a),3),"actual first-register Fourier basis index");same(mod(dot(lam,B.recovered_tau_a_mod_fixed_centre),3),mod(dot(lam,r.calibration_tau_a),3),"baseline recovered first-register equations");}});
  same(B.learned_fixed_centre_basis,kernel(A,k),"baseline learns its own centre, no granted label span");
  sameSpan(B.learned_fixed_centre_basis,r.learned_fixed_centre_basis,k,"baseline obtains true fixed centre");
  check(B.uses_known_single_register_basis_measurements===true&&B.classical_sample_access_to_unknown_quantum_state_assumed_free===false&&B.copies_shared_with_collective_receiver===false&&B.baseline_establishes_general_StateHSP_classical_algorithm===false,"baseline is source-specific, not free classical unknown-state access");
}
function receiver(r) {
  ledger(r.ledger);coverage(r.coverage);const L=r.ledger,k=L.centre_dimension,c=r.quotient_chart;
  check(L.quotient_dimension===2&&r.coverage.original_inputs===L.original_central_measurement_count,"complete reference receiver source budget");
  same(r.learned_fixed_centre_basis,kernel(r.central_character_span_basis,k),"ALL centre labels including leftovers determine fixed centre");
  const actualZ=r.fixed_central_axes.map(j=>Array.from({length:k},(_,i)=>Number(i===j)));
  sameSpan(r.learned_fixed_centre_basis,actualZ,k,"actual calibration fixed centre recovered");
  const observed=r.block_character_histogram.map(b=>{word(b.character,2);check(Number.isInteger(b.count)&&b.count>0,"positive block count");check(b.character[1]===0&&(r.source_kind==="nonnormal-line"||b.character[0]===0),"actual block-law support");return b.character;});
  check(r.block_character_histogram.reduce((s,b)=>s+b.count,0)===r.coverage.block_count,"all block measurements paid");
  same(c.quotient_frame,kernel(observed,2),"measured quotient overgroup");sameSpan(r.block_character_span_basis,observed,2,"compressed block span");
  same(c.central_fixed_frame,r.learned_fixed_centre_basis,"quotient uses learned centre");
  check(rank(c.central_fixed_frame.concat(c.central_complement),k)===k&&c.central_fixed_frame.length+c.central_complement.length===k,"genuine central quotient complement");
  check(c.dimension===c.quotient_frame.length+c.central_complement.length,"chart dimension");
  const wholeAbelian=c.quotient_frame.every(x=>c.quotient_frame.every(y=>comm(x,y,k).every(a=>!a)));
  check(c.full_preimage_group_is_abelian===wholeAbelian&&c.section_homomorphism_only_mod_fixed_centre===!wholeAbelian&&c.quotient_action_requires_original_fixed_centre_support===true&&c.general_section_linear_on_full_workspace_claimed===false,"abelian QUOTIENT, not assumed abelian whole group");
  for(const x of c.quotient_frame)for(const y of c.quotient_frame)check(member(c.central_fixed_frame,comm(x,y,k)),"commutators lie in actual fixed centre");
  const pts=words(c.dimension);
  for(const t of pts)for(const u of pts){const [x,z]=section(c,t,k),[y,w]=section(c,u,k),[v,a]=section(c,t.map((s,i)=>(s+u[i])%3),k);
    same(v,x.map((s,i)=>(s+y[i])%3),"chart quotient addition");const error=z.map((s,i)=>mod(s+w[i]+(i===0?x[1]*y[0]:0)-a[i],3));check(member(c.central_fixed_frame,error),"half-quadratic chart is homomorphic MOD fixed centre");}
  const finalRows=r.final_character_histogram.map(b=>{word(b.character,c.dimension);check(Number.isInteger(b.count)&&b.count>0,"fresh final measurement count");check(member(r.final_law_active_uniform_character_frame,b.character)||member(r.final_law_inactive_uniform_character_frame,b.character),"final observed character has a legal source law");return b.character;});
  check(r.final_character_histogram.reduce((s,b)=>s+b.count,0)===L.fresh_original_final_copy_count,"all final original copies paid");
  sameSpan(r.final_character_span_basis,finalRows,c.dimension,"actual compressed final character span");same(r.final_kernel_basis,kernel(r.final_character_span_basis,c.dimension),"actual final subgroup kernel");
  sameSpan(r.final_kernel_basis,kernel(r.final_law_active_uniform_character_frame,c.dimension),c.dimension,"complete subgroup rather than phase-losing projection");
  const generators=r.final_kernel_basis.map(v=>section(c,v,k)).concat(c.central_fixed_frame.map(z=>[[0,0],z]));
  same(r.lifted_subgroup_generators,generators,"lift includes fixed central generators");
  for(const [x,z]of generators){if(r.source_kind==="nonnormal-line")check(x[0]===0,"nonnormal subgroup quotient");const residual=z.map((a,j)=>mod(a-r.calibration_tau_a[j]*x[0]-r.calibration_tau_b[j]*x[1],3));check(member(actualZ,residual),"lift retains true central eigenvalue phases");}
  check(generators.length===actualZ.length+(r.source_kind==="nonnormal-line"?1:2),"full true subgroup dimension");
  check(r.actual_original_copies_consumed===L.total_original_copy_cap&&r.actual_known_controlled_R_calls===L.original_central_measurement_count+r.coverage.included_original_inputs+L.fresh_original_final_copy_count&&r.actual_known_controlled_R_calls<=L.known_controlled_R_call_cap,"exact actual resource accounting");
  check(r.status==="FULL_BUDGET_REFERENCE_RECOVERED"&&r.uniform_control_flow_uses_hidden_source_parameters===false&&r.source_IID_and_known_R_contract_verified_from_outcomes_alone===false&&r.quantum_advantage_inferred_from_calibration===false,"reference, NOT physical or speedup certification");
  finalInstrument(r);baseline(r);
}
for(const [file,key]of [["research/VECTOR_CENTRE_STATE_HSP_TARGET.md","derivation_sha256"],["theorems/vector_centre_state_hsp_receiver.py","producer_sha256"]])same(R[key],crypto.createHash("sha256").update(fs.readFileSync(path.join(rootDir,file))).digest("hex"),"current source/derivation digest");
check(R.status==="VECTOR_CENTRE_HETEROGENEOUS_STATE_HSP_RECEIVER_REVIEW_PENDING"&&R.uniform_quantum_recipe_specified===true,"local restricted construction status");
for(const key of ["all_central_extensions_or_higher_nilpotency_solved","new_classical_HSP_speedup_claimed","candidate_record_accepted","novelty_claimed","Shor_level_result_claimed","native_DHSP_or_CCP_receiver_compiled"])check(R[key]===false,"scope inflation: "+key);
R.growing_integer_resource_ledgers.forEach(ledger);
coverage(R.large_distinct_sector_coverage_control,true);
R.exact_two_qutrit_heterogeneous_instruments.forEach(vectorInstrument);
R.full_budget_reference_receivers.forEach(receiver);
console.log(JSON.stringify({status:"PASS",exact_heterogeneous_two_qutrit_branches:9*R.exact_two_qutrit_heterogeneous_instruments.length,
  full_budget_reference_receivers:R.full_budget_reference_receivers.length,exact_final_original_branches:R.full_budget_reference_receivers.reduce((s,r)=>s+r.literal_final_original_instrument.full_character_words.length,0),
  complete_coverage_original_labels:R.large_distinct_sector_coverage_control.original_inputs,full_budget_block_transcripts_replayed:false,
  basis_readout_baselines:R.full_budget_reference_receivers.length,novelty_or_Shor_level_claimed:false}));
