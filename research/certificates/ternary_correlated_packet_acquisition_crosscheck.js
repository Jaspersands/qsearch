"use strict";
// Reconstruct native charts and both actual coordinate permutations independently.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const report = JSON.parse(fs.readFileSync(process.argv[2] || path.join(__dirname, "../phase_workbench/ternary_correlated_packet_acquisition.json"), "utf8"));
const check = (x, message) => { if (!x) throw Error(message); };
const same = (a, b, message) => check(JSON.stringify(a) === JSON.stringify(b), message);
const mod = (a, q) => (a % q + q) % q;
const words = width => Array.from({length: 3**width}, (_, i) => Array.from({length: width}, (_, j) => Math.floor(i/3**(width-j-1))%3));
const fraction = exponent => exponent ? "1/" + String(3n**BigInt(exponent)) : "1";
const mm = (A, B) => A.map(row => B[0].map((_, j) => row.reduce((s, a, k) => s+a*B[k][j], 0n)));

function nativeChart(level) {
  let V = [[1n, 0n], [0n, 1n]];
  const pi = [[-1n, -1n], [1n, -2n]];
  for (let j=0; j<level-1; j++) V = mm(V, pi);
  const q = 3n**BigInt(Math.ceil(level/2));
  const den = 3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]);
  const u = q*(2n*V[1][1]+V[1][0]), v = q*(-2n*V[0][1]-V[0][0]);
  check(u%den === 0n && v%den === 0n, "integral full-root native chart");
  const a = u/den, b = v/den;
  check(-a*a-b*(a+b) === (level%2 ? -3n : -1n), "native chart determinant");
  return {q: Number(q), pair: ([x,y]) => [Number(mod(a*BigInt(x)+b*BigInt(y),q)), Number(mod((a+b)*BigInt(x)-a*BigInt(y),q))]};
}

function rref(A) {
  A = A.map(row => row.map(x => mod(x,3)));
  const pivots = []; let r=0;
  for (let j=0; j<A[0].length && r<A.length; j++) {
    const k = A.findIndex((row,i) => i>=r && row[j]);
    if (k<0) continue;
    [A[r],A[k]] = [A[k],A[r]];
    const inverse = A[r][j]; A[r] = A[r].map(x => x*inverse%3);
    for (let i=0; i<A.length; i++) if (i!==r) {
      const factor = A[i][j]; A[i] = A[i].map((x,k) => mod(x-factor*A[r][k],3));
    }
    pivots.push(j); r++;
  }
  return {rows: A.slice(0,r), pivots, free: Array.from({length:A[0].length},(_,i)=>i).filter(i=>!pivots.includes(i))};
}
function kernel(columns) {
  const R = rref(columns[0].map((_,j)=>columns.map(v=>v[j]))), c = Array(columns.length).fill(0);
  c[R.free[0]]=1; R.pivots.forEach((p,j)=>c[p]=mod(-R.rows[j][R.free[0]],3)); return c;
}
function sum(vectors, indices) {
  return vectors[0].map((_,j)=>mod(indices.reduce((s,i)=>s+vectors[i][j],0),3));
}
function support(vectors) {
  const n=vectors[0].length, inner=[], common=[];
  for (let g=0; g<n+1; g++) {
    const ids=Array.from({length:n+1},(_,j)=>g*(n+1)+j), c=kernel(ids.map(i=>vectors[i]));
    const left=ids.filter((_,j)=>c[j]===1), right=ids.filter((_,j)=>c[j]===2);
    same(sum(vectors,left),sum(vectors,right),"exact support inner relation");
    if (!left.length || !right.length) return left.length ? left : right;
    inner.push([left,right]); common.push(sum(vectors,left));
  }
  const c=kernel(common), left=c.flatMap((a,j)=>a===1?[j]:[]), right=c.flatMap((a,j)=>a===2?[j]:[]);
  same(sum(common,left),sum(common,right),"exact support outer relation");
  if (!left.length || !right.length) return (left.length ? left : right).flatMap(j=>inner[j][0]).sort((a,b)=>a-b);
  return [...left.flatMap(j=>inner[j][0]),...left.flatMap(j=>inner[j][1]),...right.flatMap(j=>inner[j][0])].sort((a,b)=>a-b);
}

function original(c, n, level, K) {
  const labels=c.original_labels, rows=c.original_frequencies, chart=nativeChart(level), q=chart.q, M=K*(n+1)**2;
  check(labels.length===M && rows.length===M,"charge exact original source count");
  for (let i=0; i<M; i++) {
    check(labels[i].length===n && rows[i].length===2 && rows[i].every(row=>row.length===n),"native source shape");
    for (let j=0; j<n; j++) {
      check(labels[i][j].every(x=>Number.isSafeInteger(x)&&x>=0&&x<q),"bounded original native chart");
      same(rows[i].map(row=>row[j]),chart.pair(labels[i][j]),"actual original even native frequencies");
    }
  }
  const B=rows.map(pair=>pair[0].map((a,j)=>(a+pair[1][j])%3)), W=(n+1)**2;
  const supports=Array.from({length:K},(_,k)=>support(B.slice(k*W,(k+1)*W)).map(i=>i+k*W));
  same(c.supports,supports,"reconstruct curvature-only disjoint support selection");
  const active=supports.flat(), unused=Array.from({length:M},(_,i)=>i).filter(i=>!active.includes(i));
  check(new Set(active).size===active.length && supports.every(S=>S.length&&sum(B,S).every(a=>!a)),"true curvature and original ancestry");
  const pointers=supports.flatMap(S=>S.slice(1));
  const F=word=>Array.from({length:n},(_,j)=>mod(word.reduce((s,x,i)=>s+(x?rows[i][x-1][j]:0),0),q));
  function frame(u) {
    check(u.length===pointers.length && u.every(x=>Number.isInteger(x)&&x>=0&&x<3),"canonical inner pointer");
    const anchor=Array(M).fill(0); pointers.forEach((i,j)=>anchor[i]=u[j]);
    const base=F(anchor), oddRows=supports.map(S=>[1,2].map(t=>{
      const w=[...anchor]; S.forEach(i=>w[i]=(w[i]+t)%3); return F(w).map((a,j)=>mod(a-base[j],q));
    }));
    check(oddRows.every(pair=>pair[0].every((a,j)=>mod(pair[1][j]-2*a,3)===0)),"actual odd-source promise");
    return {anchor, oddRows};
  }
  return {n,level,K,M,q,supports,active,unused,pointers,F,frame};
}

function branch(model, b) {
  const {n,q,K,M,supports,pointers,F}=model, {anchor,oddRows}=model.frame(b.pointers), chart=nativeChart(model.level-1);
  check(b.odd_native_labels.length===K,"odd labels from charged original inputs");
  for (let i=0;i<K;i++) for (let j=0;j<n;j++) same(chart.pair(b.odd_native_labels[i][j]),oddRows[i].map(row=>row[j]),"odd chart is exact original relative phase, not a field shadow");
  const low=Array.from({length:n},(_,j)=>b.odd_native_labels.map(row=>mod(row[j][0]+row[j][1],3))), R=rref(low);
  same(b.RREF_rows,R.rows,"independent Gaussian frame"); same(b.pivots,R.pivots,"physical syndrome wires"); same(b.free,R.free,"joint logical wires");
  const rho=R.pivots.length,h=R.free.length;
  check(b.syndrome.length===rho && b.syndrome.every(x=>Number.isInteger(x)&&x>=0&&x<3),"canonical measured syndrome");
  const assignment=z=>{
    const t=Array(K).fill(0); R.free.forEach((f,j)=>t[f]=z[j]);
    R.pivots.forEach((p,j)=>t[p]=mod(b.syndrome[j]-R.free.reduce((s,f)=>s+R.rows[j][f]*t[f],0),3)); return t;
  };
  const lift=z=>{
    const t=assignment(z), x=[...anchor]; supports.forEach((S,j)=>S.forEach(i=>x[i]=(x[i]+t[j])%3)); return x;
  };
  const base=F(lift(Array(h).fill(0))), points=words(h), full=points.map(z=>F(lift(z)));
  const residual=full.map(f=>f.map((a,j)=>{const d=mod(a-base[j],q);check(d%3===0,"original-root divisibility");return d/3;}));
  same(b.logical_residual_frequencies,residual,"all logical residuals from actual original source");
  const resources=b.resources, source=resources;
  check(source.acquired_original_native_inputs===M && source.active_original_inputs===model.active.length && source.untouched_original_inputs===model.unused.length && source.odd_inputs_acquired===K,"full original acquisition charged, inactive wires not consumed");
  check(source.original_source_ids.length===M&&new Set(source.original_source_ids).size===M&&source.original_source_ids.every(x=>typeof x==="string"&&x.length),"source IDs are distinct recorded ancestors");
  same(source.active_original_source_ids,model.active.map(i=>source.original_source_ids[i]),"active lineage");
  same(source.untouched_original_source_ids,model.unused.map(i=>source.original_source_ids[i]),"untouched lineage");
  same(source.odd_input_original_ancestors,supports.map(S=>S.map(i=>source.original_source_ids[i])),"odd source lineage");
  check(resources.retained_joint_logical_qutrits===h && resources.minimum_retained_joint_logical_qutrits===K-n && h>=K-n,"variable-rank joint retention");
  check(resources.measured_inner_pointer_qutrits===pointers.length && resources.measured_outer_syndrome_qutrits===rho,"actual measured wires");
  check(resources.inner_SUM_inverse_gates===pointers.length && resources.outer_SUM_gates===R.rows.reduce((s,row)=>s+R.free.filter(f=>row[f]).length,0),"two actual SUM recipes");
  const exponent=pointers.length+rho;
  check(resources.raw_joint_branch_probability_exponent_base_three===exponent && resources.raw_joint_branch_probability===fraction(exponent),"raw probability charges active measurements only");
  check(resources.retained_phase_modulus===String(q/3) && resources.retained_additive_degree_upper_bound===model.level-1,"growing-depth retained phase");
  for (const k of ["distinct_ids_certify_physical_independence","untouched_curvature_labels_claimed_fresh_IID","upstream_DCP_or_LWE_input_acquisition_implemented_here","unknown_preparation_inverse_or_amplification_used","outputs_certified_as_IID_native_samples","matched_packet_copies_or_unknown_weighted_phase_oracle_supplied","unused_original_registers_measured_or_discarded","highest_parent_secret_digit_retained_in_packet_payload","highest_parent_secret_digit_lost_from_untouched_original_registers","hardware_synthesis_and_aggregate_error_certificate_supplied","efficient_decoder_or_full_depth_speedup_supplied"]) check(resources[k]===false,"ungranted model or promotion: "+k);
  for (const k of ["intermediate_odd_input_acquisition_charged","upstream_conversion_cap_and_joint_error_obligations_remain","all_pointer_and_syndrome_outcomes_accepted","global_branch_phase_dropped_only_after_both_measurements"]) check(resources[k]===true,"required measured-instrument scope: "+k);
  return {R,h,base,full,residual,points,probability:3**(-exponent),lift};
}

const hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_CORRELATED_PACKET_ACQUISITION.md"))).digest("hex");
check(report.derivation_sha256===hash,"pinned derivation");
check(report.status==="ORIGINAL_SOURCE_CORRELATED_PACKET_ACQUISITION_EXACT_DECODER_OPEN_REVIEW_PENDING" && report.candidate_record_accepted===false && report.novel_algorithm_or_quantum_speedup_claimed===false && report.dense_seed_selection_is_population_evidence===false,"acquisition result, not a new algorithm");
const dense=report.dense_original_instrument_control, model=original(dense,1,6,4);
check(model.active.length===5 && dense.complete_active_words_replayed===243 && dense.untouched_word_cube_enumerated===false,"bounded complete active replay, not the untouched cube");
check(dense.source.acquired_original_native_inputs===16 && dense.source.active_original_inputs===5 && dense.source.untouched_original_inputs===11,"complete source accounting");
check(dense.source.distinct_ids_certify_physical_independence===false && dense.source.untouched_curvature_labels_claimed_fresh_IID===false,"no false independent recycling");
same(dense.calibration_secret,[1],"pinned primitive calibration secret");
const groups=new Map(), allTargets=new Set();
for (const digits of words(model.active.length)) {
  const originalWord=Array(model.M).fill(0); model.active.forEach((i,j)=>originalWord[i]=digits[j]);
  const u=model.supports.flatMap(S=>S.slice(1).map(i=>mod(originalWord[i]-originalWord[S[0]],3)));
  const t=model.supports.map(S=>originalWord[S[0]]), key=JSON.stringify(u);
  if (!groups.has(key)) groups.set(key,[]); groups.get(key).push({t,originalWord});
}
let total=0,minPurity=1,maximumError=0,expectedBranches=0;
for (const u of words(model.pointers.length)) {
  const rows=groups.get(JSON.stringify(u)), records=dense.all_measurement_branches.filter(b=>JSON.stringify(b.pointers)===JSON.stringify(u));
  check(records.length>0,"all inner pointers retained");
  const first=branch(model,records[0]), rank=first.R.pivots.length;
  expectedBranches+=3**rank;
  same(records.map(b=>b.syndrome),words(rank),"all outer syndromes retained exactly once");
  for (const b of records) {
    const actual=branch(model,b), {R,h,points,full,base}=actual;
    same(b.base_original_frequency,base,"observed branch global phase from original inputs");
    check(b.raw_branch_probability===fraction(model.pointers.length+rank)&&Math.abs(b.measured_probability-actual.probability)<4e-12,"raw branch probability");
    check(b.unnormalized_active_amplitudes.length===points.length,"entire logical amplitude vector");
    let probability=0;
    points.forEach((z,j)=>{
      const lifted=actual.lift(z), theta=mod(full[j][0]*dense.calibration_secret[0],model.q), scale=3**(-model.active.length/2);
      const expected=[scale*Math.cos(2*Math.PI*theta/model.q),scale*Math.sin(2*Math.PI*theta/model.q)], value=b.unnormalized_active_amplitudes[j];
      check(value.length===2&&value.every(Number.isFinite),"finite amplitude");
      maximumError=Math.max(maximumError,Math.hypot(value[0]-expected[0],value[1]-expected[1]));
      probability+=value[0]**2+value[1]**2;
      const old=rows.find(x=>JSON.stringify(x.originalWord)===JSON.stringify(lifted));
      check(old!==undefined,"lift agrees with independent actual inner SUM permutation");
      same(R.rows.map(row=>mod(row.reduce((s,a,k)=>s+a*old.t[k],0),3)),b.syndrome,"actual outer SUM output");
      same(R.free.map(f=>old.t[f]),z,"actual free-coordinate output");
      const tag=JSON.stringify([u,b.syndrome,z]); check(!allTargets.has(tag),"coordinate permutation injective"); allTargets.add(tag);
    });
    check(Math.abs(probability-actual.probability)<4e-12,"actual Born mass");
    let purity=0;
    if (h>1) {
      const width=3**(h-1), amps=b.unnormalized_active_amplitudes;
      for (let i=0;i<3;i++) for (let j=0;j<3;j++) {
        let re=0,im=0;
        for (let k=0;k<width;k++) {const a=amps[i*width+k],c=amps[j*width+k]; re+=a[0]*c[0]+a[1]*c[1];im+=a[1]*c[0]-a[0]*c[1];}
        purity+=(re*re+im*im)/(probability*probability);
      }
    } else purity=1;
    check(Math.abs(purity-b.first_logical_register_purity)<4e-12,"actual reduced-state purity");
    minPurity=Math.min(minPurity,purity);total+=probability;
  }
}
check(expectedBranches===dense.all_measurement_branches.length&&expectedBranches===9&&allTargets.size===243,"all active source words and branches, no virtual copies");
check(maximumError<4e-12&&Number.isFinite(dense.maximum_amplitude_error)&&dense.maximum_amplitude_error<4e-12&&Math.abs(total-1)<4e-12&&Math.abs(dense.total_raw_probability-total)<4e-12,"complete measured instrument norm and phases");
check(minPurity<0.5&&Math.abs(minPurity-dense.minimum_first_register_purity)<4e-12&&dense.entangled_calibration_is_population_or_speedup_evidence===false,"non-product countercontrol, not quantum advantage");
let publicWords=0;
same(report.public_original_root_controls.map(c=>[c.seed,c.resources.dimension,c.resources.original_even_level,c.resources.odd_inputs_acquired]),[[88402,2,6,5],[88403,3,8,7]],"prespecified larger original-root controls");
for (const c of report.public_original_root_controls) {
  const model=original(c,c.resources.dimension,c.resources.original_even_level,c.resources.odd_inputs_acquired), actual=branch(model,c);
  check(c.whole_original_word_cube_enumerated===false&&c.bounded_logical_words_checked===actual.points.length,"bounded logical controls, no original cube scalability claim");
  publicWords+=actual.points.length;
}
same(report.analytic_retention_ledgers.map(c=>[c.dimension,c.parent_root_digits]),[[2,3],[8,5],[32,7],[128,9]],"analytic retention schedule");
for (const c of report.analytic_retention_ledgers) {
  const n=c.dimension,r=c.parent_root_digits,K=2*n;
  check(c.original_native_input_cap_required===K*(n+1)**2&&c.intermediate_odd_inputs===K&&c.outer_rank_upper_bound===n&&c.retained_joint_logical_registers_lower_bound===n&&c.residual_root_digits===r-1&&c.residual_phase_modulus===String(3**(r-1))&&c.native_additive_degree_upper_bound===2*r-1,"exact one-step supply and growing-depth retention");
  check(c.one_root_step_original_supply_polynomial_in_n_and_K===true&&c.full_depth_cost_obtained_by_repeating_this_ledger===false&&c.joint_outputs_are_fresh_native_samples===false&&c.efficient_secret_decoder_supplied===false,"no false recursion or decoder");
}
console.log(JSON.stringify({status:"independent_original_source_correlated_packet_certificates_passed",completeActiveWords:243,allMeasuredBranches:9,boundedPublicLogicalWords:publicWords,minimumLogicalPurity:minPurity,decoderSupplied:false}));
