"use strict";

// Independent Q(zeta_3) replay of actual source/action/projector identities.
const fs = require("fs");
const path = require("path");
const {check, same, rat, str, parse, cmp, mod, field, matrices, mul, sub} = require("./cyclotomic_exact");
const report = JSON.parse(fs.readFileSync(process.argv[2] || path.join(__dirname, "../reductions/native_orbit_source_access.json"), "utf8"));
const K = field(3), M = matrices(K);
const f = x => K.scale(K.unit, x);
const key = g => JSON.stringify(g);
const near = (a,b,msg) => check(Number.isFinite(a) && Math.abs(a-b) < 2e-10, msg);
const rationalReal = a => { check(a.slice(1).every(x => x[0] === 0n), "exact real probability must be rational"); return a[0]; };
const realNumber = a => Number(a[0])/Number(a[1]);
const checkedProbability = (a,s,msg) => { check(cmp(a,parse(s)) === 0n,msg); return realNumber(a); };
const grover = p => mul(p,mul(sub(rat(3n),mul(rat(4n),p)),sub(rat(3n),mul(rat(4n),p))));

function ring(level) {
  check([1,2].includes(level), "bounded exact orbit calibration");
  const h0 = 3, h1 = level === 1 ? 1 : 3, cross = level === 1 ? 2 : 0;
  const reduce = ([a,b]) => { const carry = Math.floor(b/h1); return [mod(a-cross*carry,h0),mod(b,h1)]; };
  const plus = (a,b) => reduce([a[0]+b[0],a[1]+b[1]]);
  const times = (a,b) => reduce([a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]-a[1]*b[1]]);
  const rotate = (a,t) => times(a,[[1,0],[0,1],[-1,-1]][mod(t,3)]);
  const phase = (a,b) => { const [x,y] = times(a,b); return mod(level === 1 ? 2*x-y : -x+y,3); };
  const words = [];
  for (let a=0;a<h0;a++) for (let b=0;b<h1;b++) words.push([a,b]);
  const elements = words.flatMap(b=>[0,1,2].map(t=>[[b],t]));
  const compose = (g,h) => [[plus(g[0][0],rotate(h[0][0],g[1]))],mod(g[1]+h[1],3)];
  const inverse = g => [[reduce(rotate(g[0][0],-g[1]).map(x=>-x))],mod(-g[1],3)];
  const R = (a,g) => {
    const A=M.zeroM(3,3);
    for(let j=0;j<3;j++) { const out=mod(j-g[1],3); A[out][j]=K.powers[phase(a,rotate(g[0][0],out))]; }
    return A;
  };
  return {reduce,plus,times,rotate,phase,words,elements,compose,inverse,R};
}

function projector(G,schema) {
  const N=G.elements.length;
  const P=M.zeroM(N,N);
  if(schema.kind === "one_dimensional") {
    const [u,v]=schema.parameters;
    check([0,1,2].includes(u) && [0,1,2].includes(v),"actual one-dimensional character index");
    check(schema.irrep_dimension === 1,"one-dimensional irrep dimension");
    const phases=G.elements.map(g=>mod(u*(g[0][0][0]+g[0][0][1])+v*g[1],3));
    for(let g=0;g<N;g++) for(let h=0;h<N;h++) P[g][h]=K.scale(K.powers[mod(phases[g]-phases[h],3)],rat(1n,BigInt(N)));
  } else {
    check(schema.kind === "three_dimensional_central" && N===27,"actual Heisenberg central sector");
    const [lam]=schema.parameters;
    check([1,2].includes(lam) && schema.irrep_dimension===3,"nontrivial centre label and dimension");
    const indices=new Map(G.elements.map((g,i)=>[key(g),i]));
    for(let z=0;z<3;z++) {
      const centre=[[G.reduce([-z,z])],0];
      for(let i=0;i<N;i++) {
        const j=indices.get(key(G.compose(G.elements[i],G.inverse(centre))));
        P[j][i]=K.plus(P[j][i],K.scale(K.powers[mod(-lam*z,3)],rat(1n,3n)));
      }
    }
  }
  return P;
}

let exactSourceActions=0, completeFilters=0, exactDensities=0;
check(report.status === "NATIVE_COPY_TO_COSET_SOURCE_AND_RELATIVE_ORACLE_REFLECTION_AUDIT_REVIEW_PENDING","explicit review status");
check(report.complete_native_orbit_controls.length===4,"complete orbit cohort");
same(report.complete_native_orbit_controls.map(c=>[c.native_level,c.native_secret]), [[1,[1,0]],[1,[2,1]],[2,[1,0]],[2,[2,1]]],"declared actual source controls");
for(const c of report.complete_native_orbit_controls) {
  const G=ring(c.native_level), N=G.elements.length, E=G.words.length;
  same(c.all_public_group_elements,G.elements,"all group entries, not a selected submatrix");
  check(c.group_dimension===N && c.input_seed_dimension===3*E && c.seed_native_label_count===E,"source dimensions");
  check(c.inaccessible_environment_dimension_in_mathematical_purification===E,"unavailable purification environment");
  check(c.relative_orbit_isometry_rank===3*E && c.desired_fixed_purification_reflection_rank===1,"whole seed subspace is not fixed purification");
  const indices=new Map(G.elements.map((g,i)=>[key(g),i]));
  const lambdas=[[0,0],[1,0],[1,1]], s=G.reduce(c.native_secret);
  const H=new Set(lambdas.map((l,t)=>key([[G.times(s.map(x=>-x),l)],t])));
  const vectors=G.words.map(a=>lambdas.map(l=>[K.powers[G.phase(a,G.times(s,l))]]));
  const actions=G.words.map(a=>G.elements.map(g=>G.R(a,g)));
  for(let a=0;a<E;a++) {
    for(let g=0;g<N;g++) check(M.eq(M.times(M.star(actions[a][g]),actions[a][g]),M.identity(3)),"exact unitary induced action and orbit isometry");
    for(const generator of [ [[G.reduce([1,0])],0], [[G.reduce([0,1])],0], [[[0,0]],1] ]) {
      const i=indices.get(key(generator));
      for(let j=0;j<N;j++) {
        check(M.eq(M.times(actions[a][i],actions[a][j]),actions[a][indices.get(key(G.compose(generator,G.elements[j])))]),"exact representation composition");
        exactSourceActions++;
      }
    }
  }
  for(let g=0;g<N;g++) {
    let expectation=K.F();
    for(let a=0;a<E;a++) expectation=K.plus(expectation,M.times(M.times(M.star(vectors[a]),actions[a][g]),vectors[a])[0][0]);
    expectation=K.scale(expectation,rat(1n,BigInt(3*E)));
    check(K.eq(expectation,H.has(key(G.elements[g]))?K.unit:K.F()),"original mixed source subgroup indicator, not just absolute-overlap promise");
  }
  check(c.full_group_coset_density_real_imag.length===N,"whole coset density");
  for(let g=0;g<N;g++) {
    check(c.full_group_coset_density_real_imag[g].length===N,"whole coset row");
    for(let h=0;h<N;h++) {
      const x=H.has(key(G.compose(G.inverse(G.elements[h]),G.elements[g])))?1/N:0;
      const entry=c.full_group_coset_density_real_imag[g][h];
      check(entry.length===2,"complex density entry"); near(entry[0],x,"exact coset density real part"); near(entry[1],0,"exact coset density imaginary part"); exactDensities++;
    }
  }
  const filters=c.complete_known_Fourier_label_partition;
  same(filters.map(x=>[x.kind,x.parameters]), [...[0,1,2].flatMap(u=>[0,1,2].map(v=>["one_dimensional",[u,v]])),...(N===27?[["three_dimensional_central",[1]],["three_dimensional_central",[2]]]:[])],"complete irreplabel index list");
  let sum=M.zeroM(N,N), mass=K.F();
  for(const schema of filters) {
    const P=projector(G,schema);
    check(M.eq(P,M.star(P)) && M.eq(M.times(P,P),P),"whole regular-space projector");
    sum=M.plus(sum,P);
    const regularRank=rationalReal(P.reduce((v,row,i)=>K.plus(v,row[i]),K.F()));
    check(realNumber(regularRank)===schema.regular_group_projector_rank,"regular rank");
    let seedRank=K.F(), probability=K.F();
    for(let a=0;a<E;a++) {
      let C=M.zeroM(3,3);
      for(let h=0;h<N;h++) C=M.plus(C,M.scale(actions[a][h],P[0][h]));
      check(M.eq(C,M.star(C)) && M.eq(M.times(C,C),C),"exact seed isotypic compression");
      seedRank=K.plus(seedRank,C.reduce((v,row,i)=>K.plus(v,row[i]),K.F()));
      for(let g=0;g<N;g++) {
        let L=M.zeroM(3,3);
        for(let h=0;h<N;h++) L=M.plus(L,M.scale(actions[a][h],P[g][h]));
        check(M.eq(L,M.times(actions[a][g],C)),"exact orbit/filter intertwining at every group coordinate");
      }
      probability=K.plus(probability,M.times(M.times(M.star(vectors[a]),C),vectors[a])[0][0]);
    }
    probability=K.scale(probability,rat(1n,BigInt(3*E)));
    const p=realNumber(rationalReal(probability));
    check(realNumber(rationalReal(seedRank))===schema.seed_compressed_projector_rank,"seed rank");
    near(schema.actual_initial_label_probability,p,"source-specific label mass");
    near(schema.actual_probability_after_relative_Grover_iteration,p,"commuting reflections preserve exact source mass");
    near(schema.compressed_projector_idempotence_error,0,"reported compression residual");
    near(schema.orbit_projector_commutation_error,0,"reported intertwining residual");
    mass=K.plus(mass,probability); completeFilters++;
  }
  check(M.eq(sum,M.identity(N)) && K.eq(mass,K.unit),"all label projectors and raw probabilities partition completely");
  const p=rat(1n,BigInt(3**c.native_level));
  checkedProbability(p,c.exact_trivial_label_probability,"trivial irrep mass");
  check(c.relative_reflection_iteration_history.length===9,"all iteration histories");
  c.relative_reflection_iteration_history.forEach((h,i)=>{ check(h.iterations===i,"iteration index"); near(h.actual_trivial_label_probability,realNumber(p),"all relative iterations have unchanged mass"); });
  const full=grover(p);
  checkedProbability(full,c.exact_counterfactual_true_probability,"stronger rank-one reflection contrast");
  near(c.counterfactual_true_purification_one_iteration_probability,realNumber(full),"full-reflection contrast probability");
  for(const name of ["relative_preparation_inverse_return_error","trivial_label_compressed_projector_idempotence_error","Fourier_label_orbit_projector_commutation_error"]) near(c[name],0,"actual known inverse/commutation identity");
  const coord=c.noncentral_coordinate_amplification_countercontrol, q=rat(1n,BigInt(N)), after=grover(q);
  check(coord.known_group_coordinate_index===0,"identity coordinate countercontrol");
  checkedProbability(q,coord.exact_initial_probability,"coordinate Born mass");
  checkedProbability(q,coord.compressed_filter_scalar,"coordinate compressed scalar");
  checkedProbability(after,coord.exact_probability_after_one_relative_iteration,"noncentral relative amplification");
  near(coord.actual_probability_after_one_relative_iteration,realNumber(after),"coordinate amplification actual mass");
  near(coord.compressed_projector_idempotence_error,Math.sqrt(3*E)*realNumber(mul(q,sub(rat(1n),q))),"coordinate compression is not projector");
  near(coord.orbit_projector_commutation_error,Math.sqrt(3*E*realNumber(mul(q,sub(rat(1n),q)))),"coordinate filter does not commute with orbit range");
  near(coord.normalized_conditioned_seed_return_error,0,"noncentral success only restores original source");
  for(const name of ["compressed_filter_is_scalar_identity","output_seed_equals_original_unknown_seed"]) check(coord[name]===true,"coordinate success interpretation");
  for(const name of ["group_event_probability_depends_on_secret","secret_decoded"]) check(coord[name]===false,"coordinate amplification is not secret information");
  for(const name of ["one_native_source_copy_used_for_each_orbit_state","known_relative_preparation_and_inverse_executed"]) check(c[name]===true,"source copies and known relative inverse charged");
  for(const name of ["counterfactual_fixed_purification_reflection_is_supplied","simulation_density_or_secret_are_quantum_algorithm_inputs","source_creation_inverse_oracle_of_exact_nilpotent_theorem_supplied","growing_class_algorithm_supplied"]) check(c[name]===false,"unavailable access cannot be promoted");
}
same(report.growing_source_recipes.map(x=>[x.native_level,x.native_dimension]),[[2,1],[8,8],[32,32],[128,128]],"growing source ledger cohort");
for(const r of report.growing_source_recipes) {
  const trits=r.native_level*r.native_dimension+1;
  same(r.group_order,{base:3,exponent:trits},"symbolic group order");
  check(r.group_coordinate_trits===trits && r.known_controlled_R_calls_per_orbit_source===1 && r.relative_inverse_known_controlled_R_calls===1,"costed source recipe");
  for(const name of ["one_original_IID_native_copy_consumed_per_output","forward_and_inverse_relative_preparation_are_known","relative_inverse_returns_unknown_input_not_a_known_blank","original_exact_subgroup_indicator_required_for_uniform_coset_state","fresh_outputs_are_IID_before_conditioning_on_hidden_or_full_label_transcripts"]) check(r[name]===true,"source/model assumptions explicit");
  for(const name of ["controlled_R_phase_arithmetic_depends_on_secret","fixed_purification_preparation_oracle_supplied","unknown_input_or_purification_reflection_supplied","source_noise_and_gate_precision_certificate_supplied","growing_class_solver_supplied"]) check(r[name]===false,"stronger source capabilities are not free");
}
for(const name of ["primary_exact_theorem_requires_fixed_purification_creation_and_inverse","primary_nonexact_Proposition3_does_not_require_creation_inverse","bounded_class_hypothesis_remains_required_by_primary_results"]) check(report[name]===true,"exact/nonexact literature scopes separated");
for(const name of ["relative_reflection_amplifies_central_Fourier_label_filters","all_catalytic_or_noncommuting_receiver_strategies_ruled_out","native_full_depth_receiver_supplied","novelty_claimed","Shor_level_result_claimed"]) check(report[name]===false,"scoped access result, not universal impossibility or speedup");
console.log(JSON.stringify({status:"PASS",complete_orbit_sources:4,exact_action_compositions:exactSourceActions,exact_coset_density_entries:exactDensities,complete_irreplabel_filters:completeFilters,noncentral_amplification_countercontrols:4,full_depth_or_general_no_go_claimed:false}));
