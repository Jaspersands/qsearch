"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),Q=require("./planted_qary_usvp_source_crosscheck.js");
const {check,same,rat,parse,cmp,add}=E;
const ROOT=path.resolve(__dirname,"../.."),FILE=path.join(ROOT,"research/classical_baselines/lattice_localization_gap_frontier.json");
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
const I=x=>{check(typeof x==="string"||Number.isSafeInteger(x),"exact public integer");return BigInt(x);};
const mod=(x,q)=>(x%q+q)%q,abs=x=>x<0n?-x:x;
const norm=v=>v.reduce((s,x)=>s+x*x,0n);
const orient=v=>v.find(x=>x!==0n)<0n?v.map(x=>-x):v;

function schedule(p) {
  const n=p.dimension,m=p.constraint_count,r=n-m;
  const B=r===1?0:r===2?1:Math.floor((r-1)/2),L=r-1+m*B;
  let M=2,ell,epsilon;
  while(true) {
    ell=n*(Math.log2(M)+1);epsilon=p.noise_mode==="constant"?rat(1n,8n):rat(1n,BigInt(ell));
    if(cmp(rat(BigInt(L),BigInt(M)),rat(epsilon[0],2n*epsilon[1]))<=0n)break;
    M*=2;
  }
  check(p.parent_side===M&&p.position_wires===ell&&p.public_parent_shift_L1_upper===L&&
    cmp(parse(p.epsilon),epsilon)===0n,"public dimension-only schedule");
  const boundary=rat(BigInt(L),BigInt(M));
  check(cmp(boundary,parse(p.boundary_loss_upper))===0n,"box-boundary budget");
  for(const name of ["cube","sine"]) {
    let side=2;
    const loss=x=>name==="cube"?rat(BigInt(n),BigInt(x)):rat(BigInt(242*n),49n*BigInt(x)**2n);
    while(cmp(loss(side),rat(epsilon[0],2n*epsilon[1]))>0n)side*=2;
    const x=p[name];
    check(x.side===side&&x.sufficient_relative_gap===side&&x.split_prime-1>side,"minimal dyadic localization/gap bound");
    check(cmp(parse(x.localization_loss_upper),loss(side))===0n&&
      cmp(parse(x.total_loss_upper_IF_geometry_holds),add(boundary,loss(side)))===0n&&
      cmp(parse(x.total_loss_upper_IF_geometry_holds),epsilon)<=0n,"matched total noise budget");
    check(Number.isSafeInteger(x.split_prime)&&x.split_prime<1e10,"bounded schedule prime check");
    for(let d=2;d*d<=x.split_prime;d++)check(x.split_prime%d!==0,"splitting modulus must be prime");
  }
  check(p.first_free_basis_coordinate===m&&p.residue===1&&p.coordinate_trials_required_under_dense_ternary_promise===1&&
    p.private_hitting_coordinate_selector_used===false&&p.sparse_ternary_supports_covered_by_this_one_trial_plan===false&&
    p.individual_instance_gap_certified===false&&p.efficient_robust_receiver_supplied===false&&p.quantum_advantage_claimed===false,"public trial and promise scope");
  check(p.constant_noise_satisfies_inverse_log_budget===(cmp(epsilon,rat(1n,BigInt(ell)))<=0n),"no constant-noise promise transfer");
}

function control(c) {
  schedule(c.public_schedule);
  const P=c.public_problem,q=I(P.prime),n=P.dimension,m=P.constraint_rows;
  check(Q.primeCertificate(P.prime_certificate)===q,"exact field prime");
  const H=P.H.map(row=>row.map(I)),B=P.row_basis.map(row=>row.map(I));
  const R=Q.rref(H,q);check(R.rank===m,"full row rank");
  same(R.matrix.map(row=>row.map(String)),P.public_modular_rref.map(row=>row.map(x=>String(I(x)))),"public modular RREF");
  same(R.pivots,P.pivot_columns,"pivot columns");
  const free=Array.from({length:n},(_,j)=>j).filter(j=>!R.pivots.includes(j));
  const expected=R.pivots.map(j=>Array.from({length:n},(_,k)=>k===j?q:0n));
  for(const j of free) {
    const row=Array(n).fill(0n);row[j]=1n;
    R.pivots.forEach((p,i)=>row[p]=-(R.matrix[i][j]>q/2n?R.matrix[i][j]-q:R.matrix[i][j]));expected.push(row);
  }
  same(B.map(row=>row.map(String)),expected.map(row=>row.map(String)),"canonical public integer kernel basis");
  check(abs(Q.determinant(B))===q**BigInt(m),"full public kernel index");
  const attack=c.public_attacks.LLL,T=attack.unimodular_row_transform.map(row=>row.map(I)),A=attack.reduced_row_basis.map(row=>row.map(I));
  check(abs(Q.determinant(T))===1n,"LLL transformation unimodular");
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)check(T[i].reduce((s,x,k)=>s+x*B[k][j],0n)===A[i][j],"public LLL reduction certificate");
  const v=attack.vector.map(I),plant=c.PRIVATE_AUDIT_ONLY_planted_vector.map(I);
  check(H.every(row=>mod(row.reduce((s,x,j)=>s+x*v[j],0n),q)===0n),"attack output in public kernel");
  check(norm(v)===I(attack.squared_norm)&&norm(v)===BigInt(n)&&plant.every(x=>abs(x)===1n),"dense ternary output and plant calibration");
  same(orient(v).map(String),orient(plant).map(String),"private recovery checked AFTER public attack");
  check(attack.plant_or_private_seed_used===false&&P.solver_input_contains_plant_seed_or_solution===false&&
    c.generator_rejects_on_classical_attack_or_uniqueness_outcome===false,"no private attack input or filtering");
  check(c.finite_classical_falsifier.classical_recovery_of_plant_verified===true&&
    c.finite_classical_falsifier.all_lower_gap_lattices_dequantized===false&&
    c.finite_classical_falsifier.public_problem_sha256===P.public_problem_sha256&&
    c.receiver_or_quantum_speedup_demonstrated===false,"finite falsifier is not global dequantization");
}

function verify(R) {
  check(R.producer_sha256===hash(path.join(ROOT,"theorems/lattice_localization_gap_frontier.py"))&&
    R.derivation_sha256===hash(path.join(ROOT,"research/LATTICE_LOCALIZATION_GAP_FRONTIER.md")),"current provenance");
  Object.entries(R.dependency_sha256).forEach(([p,h])=>check(hash(path.join(ROOT,"theorems",p))===h,"dependency provenance"));
  R.public_scaling_schedules.forEach(schedule);R.actual_public_attack_controls.forEach(control);
  check(R.actual_public_attack_controls.length===8&&R.controls_tested===8&&R.classically_recovered_controls===8&&
    R.source_samples_or_quantum_solver_calls_performed===0&&R.all_lattice_hardness_or_robust_decoding_resolved===false&&
    R.accepted_speedup_candidate===false&&R.novelty_claim===false,"honest executed scope");
  return {verified:true,public_schedules:12,public_attack_controls:8,classical_recoveries:8,accepted_speedup_candidate:false};
}
module.exports={verify,schedule};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||FILE,"utf8"))),null,2));
