"use strict";
// Exact prime certificates, independent modular elimination and public attacks.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/planted_qary_usvp_source.json");
const check=(x,msg)=>{if(!x)throw Error(msg);};
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?
  Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const I=x=>{
  check((typeof x==="number"&&Number.isSafeInteger(x))||
    (typeof x==="string"&&String(BigInt(x))===x),"exact canonical integer required");return BigInt(x);
};
const mod=(a,q)=>(a%q+q)%q;
const abs=a=>a<0n?-a:a;
function gcd(a,b){a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a;}
function power(a,n,q){let r=1n;a=mod(a,q);while(n){if(n%2n)r=r*a%q;n/=2n;if(n)a=a*a%q;}return r;}
function sqrt(x){check(x>=0n,"nonnegative square root");if(x<2n)return x;
  let y=1n<<BigInt(Math.ceil(x.toString(2).length/2));while(true){const z=(y+x/y)/2n;if(z>=y)return y;y=z;}}
const rows=A=>A.map(row=>row.map(I));
const vectorSame=(a,b,msg)=>check(a.length===b.length&&a.every((x,i)=>I(x)===b[i]),msg);
function matrixSame(a,b,msg){check(a.length===b.length,msg);a.forEach((r,i)=>vectorSame(r,b[i],msg));}
const norm=v=>v.reduce((s,x)=>s+x*x,0n);
const sign=v=>v.find(x=>x!==0n)<0n?v.map(x=>-x):v;
const lex=(a,b)=>{for(let i=0;i<a.length;i++)if(a[i]!==b[i])return a[i]<b[i]?-1:1;return 0;};

function primeCertificate(C){
  const q=I(C.prime),a=I(C.witness);
  check(C.method==="LUCAS_FULL_N_MINUS_ONE_ORDER_CERTIFICATE","Lucas certificate");
  if(q===2n){check(a===1n&&C.factors.length===0,"base prime");return q;}
  check(q>2n&&a>1n&&a<q,"prime and order witness");
  let total=1n;const seen=new Set();
  for(const F of C.factors){const p=I(F.prime),e=I(F.exponent);
    check(p>=2n&&p<q&&e>=1n&&!seen.has(String(p)),"proper distinct prime factors");
    seen.add(String(p));check(primeCertificate(F.certificate)===p,"recursive factor proof");total*=p**e;
    check(gcd(power(a,(q-1n)/p,q)-1n,q)===1n,"full prime factor order");
  }
  check(total===q-1n&&power(a,q-1n,q)===1n,"complete q-1 and Fermat order");return q;
}

function rref(A,q){
  const B=A.map(r=>r.slice()),m=B.length,n=B[0].length,pivots=[];let rank=0;
  for(let c=0;c<n&&rank<m;c++){
    let p=rank;while(p<m&&B[p][c]===0n)p++;if(p===m)continue;
    [B[p],B[rank]]=[B[rank],B[p]];const inv=power(B[rank][c],q-2n,q);
    B[rank]=B[rank].map(x=>x*inv%q);
    for(let i=0;i<m;i++)if(i!==rank&&B[i][c]!==0n){const t=B[i][c];B[i]=B[i].map((x,j)=>mod(x-t*B[rank][j],q));}
    pivots.push(c);rank++;
  }return {matrix:B,rank,pivots};
}

function determinant(A){
  const B=A.map(r=>r.slice()),n=B.length;let previous=1n,sgn=1n;
  for(let k=0;k<n-1;k++){
    let p=k;while(p<n&&B[p][k]===0n)p++;if(p===n)return 0n;
    if(p!==k){[B[p],B[k]]=[B[k],B[p]];sgn=-sgn;}const pivot=B[k][k];
    for(let i=k+1;i<n;i++){
      for(let j=k+1;j<n;j++){const numerator=B[i][j]*pivot-B[i][k]*B[k][j];
        check(numerator%previous===0n,"fraction-free exact determinant division");B[i][j]=numerator/previous;}
      B[i][k]=0n;
    }previous=pivot;
  }return sgn*B[n-1][n-1];
}

function* vectors(alphabet,n,prefix=[]){if(!n){yield prefix;return;}for(const x of alphabet)yield* vectors(alphabet,n-1,[...prefix,x]);}

function verifyControl(C){
  const P=C.public_problem,q=I(P.prime),n=P.dimension,m=P.constraint_rows,H=rows(P.H);
  check(q>=3n&&primeCertificate(P.prime_certificate)===q&&m>=1&&m<n-1&&n<=128,"certified field and source shape");
  check(H.length===m&&H.every(row=>row.length===n&&row.every(x=>x>=0n&&x<q)),"canonical H");
  const payload={...P};delete payload.public_problem_sha256;
  check(P.public_problem_sha256===crypto.createHash("sha256").update(JSON.stringify(canonical(payload))).digest("hex"),"public input digest");
  check(P.solver_input_contains_plant_seed_or_solution===false&&
    Object.keys(P).every(k=>k==="solver_input_contains_plant_seed_or_solution"||(!k.includes("seed")&&!k.includes("plant"))),"no private input advice");
  const R=rref(H,q);check(R.rank===m,"full public row rank");
  matrixSame(P.public_modular_rref,R.matrix,"independent public RREF");
  check(JSON.stringify(P.pivot_columns)===JSON.stringify(R.pivots),"pivot order");
  const free=Array.from({length:n},(_,i)=>i).filter(i=>!R.pivots.includes(i));
  check(JSON.stringify(P.free_columns)===JSON.stringify(free),"free columns");
  const B=[];
  for(const p of R.pivots){const row=Array(n).fill(0n);row[p]=q;B.push(row);}
  for(const f of free){const row=Array(n).fill(0n);row[f]=1n;R.pivots.forEach((p,i)=>{
    let c=R.matrix[i][f];if(c>q/2n)c-=q;row[p]=-c;});B.push(row);}
  matrixSame(P.row_basis,B,"full modular kernel basis, not a hidden sublattice");
  check(I(P.lattice_index.prime)===q&&P.lattice_index.exponent===m,"index from block-triangular basis and surjective H");
  const member=v=>v.length===n&&H.every(row=>mod(row.reduce((s,a,i)=>s+a*v[i],0n),q)===0n);
  check(B.every(member),"every basis row is a kernel member");

  const G=C.PRIVATE_AUDIT_ONLY_generation,u=G.plant.map(I),L=C.distributional_uniqueness_ledger;
  check(u.length===n&&u.every(x=>[-1n,0n,1n].includes(x))&&u.some(x=>x!==0n)&&member(u),"private primitive plant");
  const support=Number(norm(u));check(support>=Math.ceil(n/3),"dense family prior");
  const attempts=G.attempted_matrices;
  check(attempts.length===L.actual_rank_sampling_attempts&&attempts.length<=L.rank_attempt_cap,"rank attempts charged");
  attempts.forEach((A,i)=>{
    const a=rows(A.H);check(a.length===m&&a.every(row=>row.length===n&&row.every(x=>x>=0n&&x<q)&&
      mod(row.reduce((s,x,j)=>s+x*u[j],0n),q)===0n),"every attempted row is orthogonal");
    const rank=rref(a,q).rank;check(rank===A.rank&&A.accepted_full_row_rank===(rank===m),"attempt rank replay");
    check(i===attempts.length-1?rank===m:rank<m,"first full-rank matrix accepted, no attack filtering");
  });matrixSame(attempts[attempts.length-1].H,H,"accepted public matrix binding");
  check(L.generator_rejects_on_classical_attack_or_uniqueness_outcome===false,"no selection on attack results");
  const radius=I(L.radius),gap=I(L.promised_relative_gap);
  check(L.dimension===n&&L.constraint_rows===m&&I(L.prime)===q&&L.PRIVATE_AUDIT_ONLY_plant_support===support,"uniqueness ledger binding");
  const exactR=sqrt(gap*gap*BigInt(support));check(radius===exactR+(exactR*exactR<gap*gap*BigInt(support)?1n:0n),"exact G times plant norm ceiling");
  const count=L.integer_ball_count_bound;let c=sqrt(radius*radius/BigInt(n));if(BigInt(n)*c*c<radius*radius)c++;
  const box=2n*radius+1n,ball=5n*c+3n,base=box<ball?box:ball;
  check(I(count.containing_box_side)===box&&I(count.Gaussian_volume_side_upper)===ball&&
    I(count.ceil_radius_over_sqrt_dimension)===c&&I(count.selected_count_base)===base&&count.selected_count_exponent===n,"integer volume/box bound");
  const rank=L.rank_conditioning;
  check(I(rank.prime)===q&&rank.orthogonal_space_dimension===n-1&&
    JSON.stringify(rank.failure_exponents)===JSON.stringify(Array.from({length:m},(_,i)=>n-1-i))&&
    rank.uniform_certified_rank_probability_lower==="5/6"&&rank.exact_full_rank_probability==="PRODUCT(1-q^(-exponent))","rank conditioning, not IID afterward");
  const F=L.conditional_failure_bound_factors;
  check(F.numerator_multiplier===6&&F.denominator_multiplier===5&&I(F.count_base)===base&&
    F.count_exponent===n&&I(F.prime)===q&&F.prime_exponent===m,"conditional union bound factors");
  const valid=2n*radius<q&&radius*radius>=gap*gap*BigInt(support);
  check(L.radius_strictly_below_q_over2===(2n*radius<q)&&L.radius_covers_gap_times_plant_norm===true&&
    L.status===(valid?"DISTRIBUTIONAL_UNIQUENESS_BOUND":"UNKNOWN_UNIQUENESS_SCOPE"),"centred-lift scope");
  const numerator=6n*base**BigInt(n),denominator=5n*q**BigInt(m);
  if(valid){const k=I(L.conditional_failure_upper_dyadic.negative_exponent);
    check(L.conditional_failure_upper_dyadic.base===2&&k>=0n,"dyadic encoding");
    if(numerator<=denominator)check(numerator*2n**k<=denominator&&numerator*2n**(k+1n)>denominator,"maximal exact dyadic failure exponent");
    else check(k===0n,"vacuous bound clamps at one");
  }else check(L.conditional_failure_upper_dyadic===null,"invalid scope not certified");
  check(L.bound_is_nonvacuous===(valid&&numerator<denominator)&&L.individual_instance_uniqueness_certified===false&&
    L.computational_hardness_proved===false&&L.rank_conditioned_rows_assumed_IID_unconditioned===false&&
    L.probability_bound_assumes_ideal_independent_uniform_rows===true&&L.seeded_PRNG_fixture_is_not_a_formal_IID_sampler===true,"source probability is not instance hardness");
  check(L.rank_sampling_abort_probability_upper.base===6&&L.rank_sampling_abort_probability_upper.negative_exponent===L.rank_attempt_cap,"rank abort separate");
  const choice=L.prime_selection;check(I(choice.selected_prime)===q&&choice.chosen_before_classical_attack_outcomes===true,"prime selection not attack filtering");
  if(!choice.explicit_prime_supplied){const f=I(choice.failure_bits_target),lower=I(choice.integer_prime_lower_bound);
    const target=(numerator*2n**f+4n)/5n;
    check(lower>=3n&&lower>=2n*radius+1n&&lower**BigInt(m)>=target&&q>=lower&&denominator>=numerator*2n**f,"selected prime meets failure target");
    check(lower===3n||lower===2n*radius+1n||(lower-1n)**BigInt(m)<target,"integer lower threshold, not floating estimate");
  }

  const attacks=C.public_classical_attacks, sparse=attacks.sparse_columns;
  let sparseV=null,checked=0;const seen=new Map();
  for(let j=0;j<n&&!sparseV;j++){
    const col=H.map(row=>row[j]);checked+=m;
    if(col.every(x=>x===0n)){sparseV=Array.from({length:n},(_,i)=>i===j?1n:0n);break;}
    for(const z of [1n,-1n]){const key=col.map(x=>mod(z*x,q)).join(",");
      if(seen.has(key)){sparseV=Array(n).fill(0n);sparseV[seen.get(key)]=1n;sparseV[j]=-z;sparseV=sign(sparseV);break;}}
    seen.set(col.join(","),j);
  }
  check(sparse.modular_entries_processed===checked,"sparse attack input work");
  if(sparseV){vectorSame(sparse.vector,sparseV,"sparse public output");check(I(sparse.squared_norm)===norm(sparseV),"sparse norm");}
  else check(sparse.vector===null&&sparse.absence_proves_hardness===false,"sparse absence is not hardness");

  const A=attacks.public_LLL,T=rows(A.unimodular_row_transform),reduced=rows(A.reduced_row_basis);
  check(T.length===n&&T.every(row=>row.length===n)&&reduced.length===n&&reduced.every(row=>row.length===n),"LLL transform dimensions");
  const columns=Array.from({length:n},(_,j)=>B.map((row,k)=>[k,row[j]]).filter(x=>x[1]!==0n));
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)check(columns[j].reduce((s,[k,x])=>s+T[i][k]*x,0n)===reduced[i][j],"T B equals reduced public basis");
  check(abs(determinant(T))===1n&&reduced.every(member),"unimodular full-lattice transform");
  let shortest=reduced[0];for(const row of reduced)if(norm(row)<norm(shortest)||(norm(row)===norm(shortest)&&lex(row,shortest)<0))shortest=row;
  vectorSame(A.vector,sign(shortest),"minimum returned LLL row");check(I(A.squared_norm)===norm(shortest),"LLL norm");
  check(A.input_basis_rows===n&&A.input_basis_entries===n*n&&A.plant_or_private_seed_used===false&&
    A.empirical_quality_is_a_general_LLL_guarantee===false&&Number.isFinite(A.elapsed_seconds)&&A.elapsed_seconds>=0,"empirical attack scope");
  const quality=A.delta_squared_power_factors;
  check(I(quality.row_squared_norm)===norm(shortest)&&quality.norm_exponent===n&&I(quality.determinant_prime)===q&&quality.determinant_exponent===2*m,"quality factors");

  const M=attacks.complete_ternary_MITM,split=Math.floor(n/2),states=3n**BigInt(split)+3n**BigInt(n-split);
  if(M.status==="UNKNOWN_COMPLETE_MITM_CAP")check(I(M.required_complete_half_states)===states&&states>I(M.max_states)&&
    M.vector===null&&M.cap_failure_proves_hardness===false,"MITM cap not absence");
  else {
    check(n<=16,"complete checker MITM cap");const left=new Map();
    const syn=(v,start,z)=>H.map(row=>mod(v.reduce((s,x,i)=>s+x*row[start+i],0n)*z,q)).join(",");
    for(const v of vectors([-1n,0n,1n],split)){const key=syn(v,0,1n),bucket=left.get(key)||[];
      bucket.push(v);bucket.sort((a,b)=>norm(a)===norm(b)?lex(a,b):norm(a)<norm(b)?-1:1);left.set(key,bucket.slice(0,2));}
    let best=null;
    for(const v of vectors([-1n,0n,1n],n-split))for(const u of left.get(syn(v,split,-1n))||[]){
      const c=sign([...u,...v]);if(c.every(x=>x===0n))continue;
      if(!best||norm(c)<norm(best)||(norm(c)===norm(best)&&lex(c,best)<0))best=c;}
    check(I(M.complete_half_states_processed)===states&&M.maximum_retained_vectors_per_syndrome===2,"complete MITM accounting");
    check(I(M.modular_dot_product_terms)===BigInt(m)*(BigInt(split)*3n**BigInt(split)+BigInt(n-split)*3n**BigInt(n-split)),"MITM dot-product work");
    if(best){vectorSame(M.vector,best,"minimum complete ternary vector");check(I(M.squared_norm)===norm(best),"MITM norm");}
    else check(M.vector===null,"no ternary output only after complete search");
    check(M.plant_or_private_seed_used===false&&M.failure_proves_hardness===false,"family-prior attack not generic hardness");
  }
  const outcomes=C.matched_attack_calibration.PRIVATE_AUDIT_ONLY_attack_calibrations,plant=sign(u),pivot=plant.findIndex(x=>x!==0n);
  let recovered=false;
  for(const outcome of outcomes){let v=attacks[outcome.attack].vector;
    if(v!==null){v=v.map(I);check(member(v)&&v.some(x=>x!==0n),"valid nonzero attack output");
      const d=v.reduce(gcd,0n),primitive=v.map(x=>x/d);if(member(primitive))v=primitive;
      vectorSame(outcome.public_membership_checked_normalized_vector,v,"public-checked primitive normalization");
    }else check(outcome.public_membership_checked_normalized_vector===null,"no invented output");
    const success=v!==null&&lex(sign(v),plant)===0;
    const nonparallel=v!==null&&v.some((x,i)=>x!==v[pivot]*plant[pivot]*plant[i]);
    check(outcome.planted_direction_recovered_up_to_sign===success&&
      outcome.private_uniqueness_event_falsified_for_this_instance===(nonparallel&&norm(v)<=radius*radius),"matched private calibration");recovered||=success;
  }
  const calibration=C.matched_attack_calibration;
  check(calibration.tested_instance_classically_recovers_planted_direction===recovered&&
    calibration.research_decision===(recovered?"FINITE_REGIME_CLASSICALLY_RECOVERED_NO_QUANTUM_SIGNAL":"UNRESOLVED_IMPLEMENTED_ATTACKS_NOT_HARDNESS")&&
    calibration.full_unique_SVP_or_all_classical_algorithms_ruled_out===false,"finite negative scope");
  const census=C.complete_radius_audit,boxStates=(2n*radius+1n)**BigInt(n);
  if(census.status==="UNKNOWN_COMPLETE_RADIUS_CAP")check(I(census.required_box_states)===boxStates&&
    census.individual_uniqueness_certified===false&&census.truncated_search_certifies_absence===false,"radius cap not a certificate");
  else {
    check(boxStates<=200000n,"complete radius checker cap");let checked=0;const bad=[],alphabet=[];
    for(let x=-radius;x<=radius;x++)alphabet.push(x);
    for(const v of vectors(alphabet,n)){if(norm(v)>radius*radius)continue;checked++;
      if(member(v)&&v.some((x,i)=>x!==v[pivot]*plant[pivot]*plant[i]))bad.push(v);}
    check(I(census.complete_box_states)===boxStates&&census.sphere_points_checked===checked,"complete sphere census");
    matrixSame(census.PRIVATE_AUDIT_ONLY_nonparallel_kernel_vectors,bad,"every nonparallel member retained");
    check(census.individual_uniqueness_certified===(bad.length===0)&&census.growing_family_hardness_or_quantum_advantage_certified===false,"instance census not hardness");
  }
  check(C.BKZ_status==="NOT_RUN_DEPENDENCY_FPYLLL_UNAVAILABLE"&&C.MILP_and_general_SIS_search_status==="NOT_IMPLEMENTED_NOT_A_NEGATIVE_RESULT"&&
    C.quantum_source_or_receiver_has_been_benchmarked===false,"missing algorithms not failures");
  return {dimension:n,prime_bits:q.toString(2).length,classically_recovered:recovered};
}

function verify(R){
  check(R.status==="PLANTED_QARY_USVP_PUBLIC_SOURCE_AND_CLASSICAL_FALSIFICATION_REVIEW_PENDING","status");
  check(R.producer_sha256===hash(path.join(ROOT,"theorems/planted_qary_usvp_source.py"))&&
    R.derivation_sha256===hash(path.join(ROOT,"research/PLANTED_QARY_USVP_SOURCE.md"))&&
    R.contract_sha256===hash(path.join(ROOT,"research/hypotheses/planted_qary_usvp_source_contract.json")),"current provenance");
  check(R.source_controls.length===8,"complete finite scaling sweep");const controls=R.source_controls.map(verifyControl);
  check(R.accepted_speedup_candidate===false&&R.source_distribution_is_proved_computationally_hard===false&&
    R.new_active_negative_result_created===false&&R.novelty_claim===false,"no inflated result");
  return {verified:true,source_controls:controls.length,controls,accepted_speedup_candidate:false};
}
module.exports={verify,primeCertificate,rref,determinant};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(REPORT,"utf8"))),null,2));
