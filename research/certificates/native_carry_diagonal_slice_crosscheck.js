"use strict";
// Exact original-label carry, disjoint kernel restriction and paid MITM replay.
// The degree3 grid proves functional agreement only with the cubic degree contract;
// it does not count solutions or certify a full coherent row or a growing-root solver.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,same,rat,str,add,sub,mul,div,cmp,one}=require("./cyclotomic_exact.js");
const C=require("./native_prefix_carry_crosscheck.js"),A=require("./native_affine_fibre_crosscheck.js"),H=require("./native_short_preimage_crosscheck.js");
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/classical_baselines/native_carry_diagonal_slice.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex"),mod=(x,q)=>(x%q+q)%q;
const tuples=t=>t?tuples(t-1).flatMap(v=>[0,1,2].map(x=>[...v,x])):[[]];
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const digest=x=>crypto.createHash("sha256").update(JSON.stringify(canonical(x))).digest("hex");
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0)%3;
function grid(t) {
  const points=[Array(t).fill(0)];
  for(let i=0;i<t;i++)for(const a of [1,2]){const v=Array(t).fill(0);v[i]=a;points.push(v);}
  for(let i=0;i<t;i++)for(let j=i+1;j<t;j++)for(const [a,b] of [[1,1],[1,2],[2,1]]){const v=Array(t).fill(0);v[i]=a;v[j]=b;points.push(v);}
  for(let i=0;i<t;i++)for(let j=i+1;j<t;j++)for(let h=j+1;h<t;h++){const v=Array(t).fill(0);v[i]=v[j]=v[h]=1;points.push(v);}
  return points.sort((a,b)=>{for(let i=0;i<t;i++)if(a[i]!==b[i])return a[i]-b[i];return 0;});
}
function publicCircuit(s) {
  const f=s.public_family,q=BigInt(f.modulus),n=f.dimension,M=f.sites,k=M-n,b=s.cohort;
  check(q>=9n&&Number.isSafeInteger(n)&&n>0&&Number.isSafeInteger(M)&&M>=n&&Number.isSafeInteger(f.cohorts)&&f.cohorts>0&&(BigInt(f.cohorts)&(BigInt(f.cohorts)-1n))===0n&&Number.isSafeInteger(b)&&b>=0&&b<f.cohorts&&s.free_trits===k&&s.next_digit_equations===n,"actual native carry shape");
  let root=q;while(root%3n===0n&&root>1n)root/=3n;check(root===1n,"true higher ternary root");
  check(f.paired_labels.length===f.cohorts&&f.paired_labels.every(c=>c.length===M&&c.every(p=>p.length===2&&p.every(a=>a.length===n&&a.every(x=>BigInt(x)>=0n&&BigInt(x)<q))))&&f.responses_masks_source_IDs_and_errors_supplied===false,"canonical actual public label pairs");
  check(s.target.length===n&&s.target.every(x=>BigInt(x)>=0n&&BigInt(x)<q),"canonical prescribed target");
  const slopes=Array.from({length:n},(_,i)=>f.paired_labels[b].map(([a,c])=>Number(mod(BigInt(a[i])+BigInt(c[i]),3n))));
  check(s.prefix_recipe.modulus==="3","only low labels are treated as a field");const P=A.recipe(s.prefix_recipe,slopes);
  const offset=Array.from({length:n},(_,i)=>Number(mod(f.paired_labels[b].reduce((v,[a])=>v+BigInt(a[i]),0n),3n))),rhs=s.target.map((x,i)=>Number(mod(BigInt(x)-BigInt(offset[i]),3n))),zero=Array(k).fill(0),word0=P.solve(rhs,zero);
  same(s.word_offsets,word0,"actual affine word offsets");
  const columns=Array.from({length:k},(_,i)=>{const u=[...zero];u[i]=1;return P.solve(rhs,u).map((x,j)=>(x-word0[j]+3)%3);});
  same(s.pivot_affine_forms,s.prefix_recipe.pivot_columns.map(site=>({site,offset:word0[site],coefficients:columns.map(v=>v[site])})),"actual dense affine forms");
  C.recompile(s,f,s.target,word0);
  check(s.total_degree_upper===3&&s.coefficient_division_by3_is_verified_integer_division===true&&s.matching_mod9_implies_full_root_matching===(q===9n),"correct first-carry degree and scope");
  ["expanded_cubic_tensor_materialized","divided_cubes_are_ordinary_rank_one_F3_cubes","source_values_mask_secret_or_errors_supplied","polynomial_cubic_solver_or_uniform_row_sampler_supplied","physical_row_preparation_circuit_executed"].forEach(key=>check(s[key]===false,"raw carry scope "+key));
  return {P,rhs,n,M,k,q};
}
function normalization(s,N) {
  check(N.raw_carry_sha256===digest(s),"bind actual raw carry");const X=s.prefix_recipe.pivot_minor_inverse,n=s.next_digit_equations;
  same(N.output_inverse,X,"actual invertible output minor");
  const apply=rows=>X.map(row=>rows[0].map((_,j)=>dot(row,rows.map(v=>v[j]))));
  const weights=s.F3_pivot_weights.map(w=>X.map(row=>({square:dot(row,w.map(x=>x.square)),cube:dot(row,w.map(x=>x.cube))})));
  same(N.F3_constants,apply(s.F3_constants.map(c=>[c])).map(row=>row[0]),"normalized constants");same(N.F3_linear_coefficients,apply(s.F3_linear_coefficients),"normalized linear part");same(N.F3_diagonal_quadratic,apply(s.F3_diagonal_quadratic),"normalized diagonal part");same(N.F3_pivot_weights,weights,"one actual divided cube per output");
  same(weights.map((w,j)=>w.map((x,i)=>x.cube)),Array.from({length:n},(_,j)=>Array.from({length:n},(_,i)=>Number(i===j))),"actual identity cube coefficient matrix");
  check(N.zero_set_is_preserved===true&&N.one_divided_cube_per_equation===true&&N.output_is_literal_native_digit_residual===false&&N.quadratic_terms_or_free_variables_are_independent===false&&N.uniform_fibre_sampler_or_solver_supplied_by_output_normalization===false,"output change is not solving");
  return {...s,F3_constants:N.F3_constants,F3_linear_coefficients:N.F3_linear_coefficients,F3_diagonal_quadratic:N.F3_diagonal_quadratic,F3_pivot_weights:N.F3_pivot_weights};
}
function divided(b,v) {
  const L=b.reduce((s,a,i)=>s+BigInt(a*v[i]),0n),numer=L**3n-b.reduce((s,a,i)=>s+BigInt(a)**3n*BigInt(v[i])**3n,0n);
  check(numer%3n===0n,"integer divided-cube quotient");return Number(mod(numer/3n,3n));
}
function restriction(s,N,S) {
  const n=s.next_digit_equations,k=s.free_trits,t=S.parameters,B=s.pivot_affine_forms.map(f=>f.coefficients);
  check(S.normalized_carry_sha256===digest(N)&&S.free_prefix_trits===k&&S.directions.length===t&&S.blocks.length===t&&t>=Math.floor(k/(n+1)),"actual restricted coordinate count");
  const occupied=new Set();S.directions.forEach((v,j)=>{
    check(v.length===k&&v.every(x=>Number.isInteger(x)&&x>=0&&x<3)&&v.some(x=>x)&&B.every(b=>dot(b,v)===0),"actual nonzero kernel direction");
    const support=v.map((x,i)=>x?i:-1).filter(i=>i>=0),block=S.blocks[j];check(v[support[0]]===1&&block.start>=0&&block.end<=k&&block.start<block.end&&block.end-block.start<=n+1&&support.every(i=>i>=block.start&&i<block.end&&!occupied.has(i)),"disjoint canonical block support");support.forEach(i=>occupied.add(i));
    check(block.nullity===block.end-block.start-A.rank3(B.map(row=>row.slice(block.start,block.end)))&&block.nullity>0,"actual F3 block nullity");
  });
  const L=N.F3_linear_coefficients.map((row,i)=>S.directions.map(v=>(dot(row,v)+divided(B[i],v))%3)),Q=N.F3_diagonal_quadratic.map((row,i)=>S.directions.map(v=>row.reduce((a,x,l)=>a+(x+B[i][l])*v[l]*v[l],0)%3));
  same(S.F3_constants,N.F3_constants,"same normalized constant term");same(S.F3_linear_columns,L,"restricted divided cubes really become linear");same(S.F3_quadratic_columns,Q,"actual diagonal quadratic coefficients");same(S.uniform_prefix_projection_acceptance,{base:3,negative_exponent:k-t},"lost full-prefix mass charged");
  check(S.support_disjointness_and_kernel_verified===true&&S.restricted_system_is_diagonal_quadratic_plus_linear===true&&S.full_prefix_zero_set_preserved===false&&S.full_coherent_fibre_or_full_root_helper_supplied===false&&S.slice_choice_uses_higher_labels===false,"restricted rows are not full coherent fibres");
  check(S.selection_policy==="LOW_SLOPE_DISJOINT_BLOCK_FIRST_NULLSPACE_VECTOR"&&S.selection_provenance_inferred_from_kernel_validity===false,"low-only selection is a program obligation, not mere kernel membership");
  const expected=[],blocks=[];
  for(let start=0;start<k;start+=n+1){
    const end=Math.min(k,start+n+1),R=B.map(row=>row.slice(start,end));let rank=0;const pivots=[];
    for(let j=0;j<end-start&&rank<n;j++){
      let p=rank;while(p<n&&!R[p][j])p++;if(p===n)continue;
      [R[p],R[rank]]=[R[rank],R[p]];const inverse=R[rank][j]===1?1:2;R[rank]=R[rank].map(x=>x*inverse%3);
      for(let h=0;h<n;h++)if(h!==rank){const a=R[h][j];R[h]=R[h].map((x,l)=>(x-a*R[rank][l]+6)%3);}pivots.push(j);rank++;
    }
    const f=Array.from({length:end-start},(_,i)=>i).find(i=>!pivots.includes(i));if(f===undefined)continue;
    const v=Array(k).fill(0);v[start+f]=1;pivots.forEach((p,i)=>v[start+p]=(3-R[i][f])%3);
    const scale=v.find(x=>x)===1?1:2;expected.push(v.map(x=>x*scale%3));blocks.push({start,end,nullity:end-start-rank});
  }
  same(S.directions,expected,"replayed low-label-only direction selection");same(S.blocks,blocks,"replayed low-only block schedule");
}
const inject=(S,z)=>Array.from({length:S.free_prefix_trits},(_,l)=>S.directions.reduce((v,a,j)=>v+a[l]*z[j],0)%3);
const evaluate=(S,z)=>S.F3_constants.map((c,i)=>(c+z.reduce((v,x,j)=>v+S.F3_linear_columns[i][j]*x+S.F3_quadratic_columns[i][j]*x*x,0))%3);
function moment(L) {
  const n=L.equations,k=L.prefix_free_trits,t=L.slice_parameters,B=L.cohorts;check([n,k,t,B].every(Number.isSafeInteger)&&n>0&&k>=0&&t>=0&&t<=k&&B>0,"valid moment dimensions");
  const mu=rat(3n**BigInt(t),3n**BigInt(n)),variance=mul(mu,sub(one,rat(1n,3n**BigInt(n)))),lower=div(mu,add(mu,sub(one,rat(1n,3n**BigInt(n)))));
  check(L.single_slice_mean_solution_count===str(mu)&&L.single_slice_solution_count_variance===str(variance)&&L.single_slice_solution_existence_probability_lower===str(lower)&&L.single_slice_solution_existence_probability_upper===str(cmp(mu,one)<0n?mu:one),"exact pairwise-independent first/second moment and existence bounds");
  same(L.full_prefix_no_solution_probability_upper_compact,{numerator_base:3,numerator_exponent:n,numerator_subtract:1,denominator_base:3,denominator_exponent:k,denominator_multiplier:B,clipped_at_one:true},"scoped whole-prefix moment bound");
  ["IID_uniform_first_higher_labels_conditioned_on_low_labels_required","full_low_prefix_rank_in_each_cohort_required","target_basis_and_slice_fixed_before_higher_labels_required"].forEach(key=>check(L[key]===true,"moment population premise "+key));
  ["population_premises_established_by_artifact","repeated_slices_on_same_data_are_independent","existence_bound_constructs_witness_or_coherent_sampler","later_carry_or_full_root_decoder_established","accepted_speedup_candidate"].forEach(key=>check(L[key]===false,"moment scope "+key));
}
function solver(s,S,R,P,rhs) {
  const n=s.next_digit_equations,t=S.parameters,left=Math.floor(t/2),lc=3**left,rc=3**(t-left),cost=R.cost;
  same(cost,{left_assignment_bound:String(lc),right_assignment_bound:String(rc),whole_search_assignment_bound:String(lc+rc),left_memory_entry_bound:String(lc),max_evaluations:cost.max_evaluations,max_entries:cost.max_entries,group_modulus:"3",group_dimension:n,parameters:t,residue_bits:2,left_payload_bits_upper:String(lc*(2*n+2*left)),payload_bound_includes_runtime_object_overhead:false,per_assignment_modular_additions_upper:n*Math.max(left,t-left),search_is_exponential_in_slice_parameters:true,uniform_solution_sampler:false,source_values_mask_secret_or_errors_used:false},"all MITM costs and scope");
  check(Number.isSafeInteger(cost.max_evaluations)&&cost.max_evaluations>0&&Number.isSafeInteger(cost.max_entries)&&cost.max_entries>0,"valid paid caps");
  if(lc+rc>cost.max_evaluations||lc>cost.max_entries){check(R.status==="SEARCH_CAP_EXCEEDED_NOT_NO_SOLUTION"&&R.parameters===null&&R.assignments_evaluated===0&&R.stored_entries===0,"preflight is not no solution");return;}
  const contribution=(z,offset)=>Array.from({length:n},(_,i)=>z.reduce((a,x,j)=>a+S.F3_linear_columns[i][offset+j]*x+S.F3_quadratic_columns[i][offset+j]*x*x,0)%3),table=new Map();let count=0,answer=null;
  tuples(left).forEach(z=>{const key=JSON.stringify(contribution(z,0));if(!table.has(key))table.set(key,z);count++;});
  for(const z of tuples(t-left)){const sum=contribution(z,left),needed=S.F3_constants.map((c,i)=>(-c-sum[i]+6)%3),key=JSON.stringify(needed);count++;if(table.has(key)){answer=[...table.get(key),...z];break;}}
  check(R.assignments_evaluated===count&&R.stored_entries===table.size,"actual assignments and peak hash entries charged");
  if(answer===null){check(R.status==="COMPLETE_SEARCH_NO_SOLUTION_ON_THIS_SLICE"&&R.parameters===null&&R.absence_of_full_prefix_or_root_solutions_inferred===false,"complete restricted failure is not general failure");return;}
  const free=inject(S,answer),word=P.solve(rhs,free),frequency=H.frequency(s.public_family,s.cohort,word),full=frequency.every((x,i)=>BigInt(x)===BigInt(s.target[i]));
  same(R.parameters,answer,"actual paid MITM collision");same(R.free_trits,free,"actual public injection");same(R.native_word,word,"actual native word, not only a polynomial root");same(R.actual_frequency,frequency,"actual full-root frequency");check(R.status==="VERIFIED_CLASSICAL_FIRST_CARRY_WITNESS"&&R.whole_root_target_matched===full&&frequency.every((x,i)=>mod(BigInt(x)-BigInt(s.target[i]),9n)===0n),"first carry only unless actual full frequency matches");
}
function control(c) {
  const s=c.raw_carry,{P,rhs,n,k}=publicCircuit(s),N=c.output_normalization,S=c.diagonal_slice,norm=normalization(s,N);restriction(s,N,S);
  const points=c.slice_exhaustively_enumerated?tuples(S.parameters):grid(S.parameters);
  check(c.degree3_unisolvent_grid_used===!c.slice_exhaustively_enumerated&&c.solution_count===(c.slice_exhaustively_enumerated?c.slice_check_rows.filter(r=>r.is_mod9_solution).length:null),"grid is not an exhaustive solution count");
  check(points.length===c.slice_check_rows.length,"complete declared grid");let hits=0;
  points.forEach((z,j)=>{
    const free=inject(S,z),reduced=evaluate(S,z),raw=C.compact(s,free),normalized=C.compact(norm,free);same(reduced,normalized,"degree-reduced formula agrees on coefficient-separating grid");same(normalized,N.output_inverse.map(row=>dot(row,raw)),"invertible output transform");
    const word=P.solve(rhs,free),frequency=H.frequency(s.public_family,s.cohort,word),residual=frequency.map((x,i)=>mod(BigInt(x)-BigInt(s.target[i]),9n));check(residual.every(x=>x%3n===0n),"actual low prefix");same(raw,residual.map(x=>Number(x/3n)),"original-frequency first carry");
    const yes=reduced.every(x=>x===0);hits+=Number(yes);same(c.slice_check_rows[j],{parameters:z,free_trits:free,normalized_carry:normalized,is_mod9_solution:yes},"exact declared native slice point");
  });
  check(c.diagnostic_points_are_a_uniform_solution_sampler===false&&c.full_prefix_enumerated===false&&c.new_quantum_algorithm_or_full_root_helper===false,"slice verification is not an algorithm claim");
  solver(s,S,c.solver,P,rhs);moment(c.conditional_population_ledger);check(c.conditional_population_ledger.equations===n&&c.conditional_population_ledger.prefix_free_trits===k&&c.conditional_population_ledger.slice_parameters===S.parameters,"same population dimensions");return points.length;
}
function verify(p) {
  check(p.status==="CONSTRUCTIVE_CLASSICAL_NATIVE_FIRST_CARRY_DIAGONAL_SLICE_REVIEW_PENDING","review-pending actual classical baseline");
  check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_carry_diagonal_slice.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_CARRY_DIAGONAL_SLICE.md")),"live source/derivation provenance");
  const deps=["native_prefix_carry_lift.py","native_affine_fibre_relaxation.py","native_known_seed_group_workbench.py","native_short_preimage_reduction.py","native_choice_mitm.py","ternary_measured_lattice_decoder.py","ternary_noise_degradation.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"direct provenance");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(p.actual_native_slice_controls.length===4&&p.growing_slice_population_ledgers.length===4,"declared coverage");const points=p.actual_native_slice_controls.map(control);p.growing_slice_population_ledgers.forEach(moment);
  ["accepted_speedup_candidate","new_active_negative_result_created","growing_root_classical_preimage_solver_or_uniform_coherent_row_sampler"].forEach(key=>check(p[key]===false,"report scope "+key));
  return {verified:true,exact_slice_grid_points:points.reduce((a,b)=>a+b,0),paid_MITM_controls:4,scaling_ledgers:4,full_root_or_coherent_row_solver_supplied:false};
}
module.exports={verify,publicCircuit,normalization,restriction,moment,control};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));
