"use strict";
// Independent integer polynomial expansion, F3 solve and actual-root original lifting.
// Alphabet-compatible uniqueness does NOT certify a false planted-noise promise.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),M=require("./native_small_multiple_completion_crosscheck.js");
const {check,same,rat,parse,str,add,sub,mul,div,cmp,one}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/classical_baselines/native_small_alphabet_decoder.json");
const mod=(x,q)=>(x%q+q)%q,field=x=>(x%3+3)%3;
const enc=x=>x<=9007199254740991n&&x>=-9007199254740991n?Number(x):String(x);
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const digest=x=>crypto.createHash("sha256").update(JSON.stringify(canonical(x))).digest("hex");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex"),bits=x=>x===0n?0:x.toString(2).length,min=(a,b)=>cmp(a,b)<=0n?a:b;
function integer(x){check((typeof x==="number"&&Number.isSafeInteger(x))||typeof x==="string","exact JSON integer, not bool/float");const b=BigInt(x);check(enc(b)===x,"canonical exact integer transport");return b;}
function root(q){check(q>=3n,"positive original root");let r=0;while(q%3n===0n){r++;q/=3n;}check(q===1n,"full ternary prime power");return r;}
function layout(n,method){
  const out=[];
  if(method==="quadratic"){for(let i=0;i<n;i++)for(let j=i;j<n;j++)out.push(["quadratic",[i,j]]);for(let i=0;i<n;i++)out.push(["u",[i]]);return out;}
  check(method==="cubic","explicit small-alphabet method");
  for(let i=0;i<n;i++)out.push(["u",[i]]);for(let i=0;i<n;i++)out.push(["u2",[i]]);
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)out.push(["uij",[i,j]]);
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j)out.push(["u2j",[i,j]]);
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let k=j+1;k<n;k++)out.push(["uijk",[i,j,k]]);
  for(let i=0;i<n;i++)out.push(["v",[i]]);return out;
}
function equation(a,t,method){
  const L=layout(a.length,method);
  if(method==="quadratic")return [L.map(([kind,ij])=>field(kind==="u"?t*a[ij[0]]:(ij[0]===ij[1]?1:2)*a[ij[0]]*a[ij[1]])),field(1-t*t)];
  // Expand (t-sum a_i*u_i)^3-(t-sum a_i*u_i) over INTEGER polynomials.
  const linear=[[[],t],...a.map((x,i)=>[[i],-x])],P=new Map();
  function term(indices,c){const key=indices.slice().sort((a,b)=>a-b).join(",");P.set(key,(P.get(key)||0)+c);}
  for(const [i,x] of linear)for(const [j,y] of linear)for(const [k,z] of linear)term([...i,...j,...k],x*y*z);
  linear.forEach(([i,c])=>term(i,-c));
  // Canonical trit identity u_i^3 = u_i +3*(u_i^2-u_i), BEFORE division.
  a.forEach((_,i)=>{const key=[i,i,i].join(","),c=P.get(key)||0;P.delete(key);term([i],-2*c);term([i,i],3*c);});
  for(const [key,c] of P){check(c%3===0,"coefficientwise integer carry division");P.set(key,field(c/3));}
  const row=L.map(([kind,ij])=>{
    if(kind==="v")return a[ij[0]]%3;
    const indices=kind==="u2"?[ij[0],ij[0]]:kind==="u2j"?[ij[0],ij[0],ij[1]]:ij;
    return P.get(indices.slice().sort((a,b)=>a-b).join(","))||0;
  });return [row,field(-(P.get("")||0))];
}
function featureVector(u,v,method){return layout(u.length,method).map(([kind,ij])=>{
  if(kind==="v")return v[ij[0]];if(kind==="u")return u[ij[0]];
  if(kind==="u2")return field(u[ij[0]]**2);if(kind==="u2j")return field(u[ij[0]]**2*u[ij[1]]);
  return field(ij.reduce((s,i)=>s*u[i],1));
});}
function solve(rows,rhs,D){
  const A=rows.map((a,i)=>[...a,rhs[i]]),pivots=[];let rank=0;
  for(let col=0;col<D&&rank<A.length;col++){
    let p=rank;while(p<A.length&&!A[p][col])p++;if(p===A.length)continue;
    [A[rank],A[p]]=[A[p],A[rank]];const s=A[rank][col];for(let j=col;j<=D;j++)A[rank][j]=A[rank][j]*s%3;
    for(let i=0;i<A.length;i++)if(i!==rank&&A[i][col]){const t=A[i][col];for(let j=col;j<=D;j++)A[i][j]=field(A[i][j]-t*A[rank][j]);}
    pivots.push(col);rank++;
  }
  if(A.some(row=>row.slice(0,D).every(x=>x===0)&&row[D]))return {status:"inconsistent",rank,solution:null};
  if(rank<D)return {status:"rankless",rank,solution:null};
  const out=Array(D).fill(0);pivots.forEach((j,i)=>out[j]=A[i][D]);return {status:"full",rank,solution:out};
}
function rawCheck(raw){
  check(raw.length>0&&raw.length%2===0&&new Set(raw.map(s=>s.source_id)).size===raw.length,"distinct actual paired originals");
  const q=integer(raw[0].modulus),n=raw[0].label.length;root(q);check(n>0,"positive source dimension");
  raw.forEach(s=>check(integer(s.modulus)===q&&s.label.length===n&&s.label.every(a=>integer(a)>=0n&&integer(a)<q)&&integer(s.value)>=0n&&integer(s.value)<q&&typeof s.source_id==="string"&&s.source_id.length>0,"canonical original records"));
  return {q,n,m:raw.length};
}
function result(raw,R,cap=2000000){
  const {q,n,m}=rawCheck(raw),method=R.method,D=layout(n,method).length,entries=m*(D+1),alphabet=method==="cubic"?[-1,0,1]:[-1,1];
  check((method!=="cubic"||root(q)>=2)&&integer(R.original_modulus)===q&&R.dimension===n&&R.original_records_paid_once===m&&R.feature_dimension===D&&R.logical_augmented_matrix_entries===entries,"same full-root source and whole feature matrix");
  same(R.required_canonical_original_error_alphabet,alphabet,"source alphabet not substituted from Gaussian moments");
  check(R.actual_planted_secret_or_noise_law_certified===false&&R.original_data_without_secret_mask_errors_or_oracle_input===true&&R.new_quantum_algorithm_or_general_Gaussian_solver===false&&R.classical_secret_hypotheses_enumerated===0&&R.matrix_and_original_record_work_are_free===false&&R.matrix_cap_includes_Python_and_FLINT_overhead===false,"source interface and cost scope");
  check(R.row_generation_order===(method==="cubic"?"O(m*n^3)":"O(m*n^2)")&&R.field_elimination_order==="O(m*D^2)"&&R.matrix_storage_order==="O(m*D)"&&R.full_root_lift_arithmetic_order==="O(n^2*m+n^3*log(r+1)+m*n) on O(log(q))-bit operands","charged polynomial field/ring work");
  if(entries>cap){check(R.status==="WHOLE_FEATURE_MATRIX_CAP_EXCEEDED_NOT_NO_SOLUTION"&&R.compiled_rows===0&&R.field_elimination_calls===0&&R.coefficient_rank===null&&R.candidate_secret===null&&R.fixed_instance_alphabet_uniqueness_certified===false,"preflight not a nonexistence claim");return {rows:0,rank:0};}
  const equations=raw.map(s=>equation(s.label.map(a=>Number(integer(a)%BigInt(method==="cubic"?9:3))),Number(integer(s.value)%BigInt(method==="cubic"?9:3)),method)),rows=equations.map(a=>a[0]),rhs=equations.map(a=>a[1]);
  check(R.compiled_rows===m&&R.compiled_system_sha256===digest({basis:layout(n,method),rows,rhs})&&R.original_records_sha256===digest(raw),"independent integer-polynomial coefficients bound to ORIGINAL values");
  const S=solve(rows,rhs,D);
  if(S.status==="inconsistent"){check(R.status==="INCONSISTENT_SMALL_ALPHABET_EQUATIONS"&&R.coefficient_rank===null&&R.field_elimination_calls===1&&R.candidate_secret===null,"corrupted equations fail rather than use truth");return {rows:m,rank:S.rank};}
  if(S.status==="rankless"){check(R.status==="INSUFFICIENT_FEATURE_RANK_NOT_NO_SECRET"&&R.coefficient_rank===S.rank&&R.field_elimination_calls===2&&R.candidate_secret===null,"actual incomplete rank is not guessed");return {rows:m,rank:S.rank};}
  check(R.coefficient_rank===D&&R.field_elimination_calls===1,"actual full coefficient rank");same(R.linearized_solution,S.solution,"independent exact F3 solution");
  const u=method==="cubic"?S.solution.slice(0,n):S.solution.slice(-n),v=method==="cubic"?S.solution.slice(-n):null,expected=featureVector(u,v,method);
  if(JSON.stringify(S.solution)!==JSON.stringify(expected)){
    check(R.status==="INVALID_NONLINEAR_FEATURE_LIFT"&&R.candidate_secret===null&&R.low_secret===null&&R.fixed_instance_alphabet_uniqueness_certified===false,"unique linear field solution can be a nonphysical feature vector");
    return {rows:m,rank:D};
  }
  const prefix=method==="cubic"?9n:3n,lower=method==="cubic"?u.map((a,i)=>a+3*v[i]):u;
  same(R.low_secret,lower,"actual recovered low secret, no truth assignment");check(R.prefix_modulus===Number(prefix)&&R.nonlinear_features_verified===true,"correct prefix/feature scope");
  let candidate;
  if(q===prefix){candidate=lower;same(R.full_root_lift,{applied:false,prefix_modulus:Number(prefix),remaining_modulus:1,root_already_complete:true},"actual root already complete");}
  else{
    // Reuse independently implemented ring Gaussian elimination, not Python's lift.
    const c=q/prefix,w=lower.map(x=>enc(mod(c*BigInt(x),q))),lift=M.complete(raw,c,w),H=R.full_root_lift;
    check(lift.status==="CONDITIONAL_ORIGINAL_BANK_MULTIPLE_COMPLETION","actual unit original-row higher lift");
    same(H,{applied:true,prefix_modulus:Number(prefix),remaining_modulus:enc(c),public_basis_model:lift.public_basis_model,
      rounding_transcript:lift.rounding_transcript.map(t=>({source_id:t.source_id,corrected_original_response:t.corrected_original_response,rounded_higher_equation:t.rounded_missing_quotient_equation})),
      higher_solution:lift.missing_quotient_solution,all_original_higher_equations_consistent:true,new_independent_samples_created:false},"same ORIGINAL high-root responses, unit minor and all equations");
    candidate=lift.candidate_secret;
  }
  const residuals=raw.map(s=>enc(mod(integer(s.value)-s.label.reduce((v,a,i)=>v+integer(a)*BigInt(candidate[i]),0n)+q/2n,q)-q/2n));
  same(R.original_candidate_residuals,residuals,"actual entire-root signed circular residuals");
  check(residuals.every(e=>alphabet.includes(e)),"declared circular alphabet fits ALL originals");
  check(R.status==="UNIQUE_BOUNDED_ALPHABET_COMPATIBLE_FULL_ROOT_SECRET"&&R.fixed_instance_alphabet_uniqueness_certified===true&&R.planted_secret_recovery_requires_the_true_alphabet_promise===true,"fixed-instance alphabet uniqueness, not planted-source certification");
  same(R.candidate_secret,candidate,"actual full-root classical candidate");return {rows:m,rank:D};
}
function rankBudget(L){
  const n=L.dimension,m=L.original_rows,D=layout(n,"cubic").length,s=L.supported_original_noise_residues,p=parse(L.true_noise_probability_floor);
  check(Number.isSafeInteger(n)&&n>0&&Number.isSafeInteger(m)&&m>0,"positive exact source dimensions");
  check([2,3].includes(s.length)&&new Set(s).size===s.length&&s.every(x=>[-1,0,1].includes(x))&&cmp(p,rat(0n))>0n&&cmp(p,rat(1n,BigInt(s.length)))<=0n,"actual two/three residue probability floor");
  const escape=div(mul(rat(s.length===3?2n:1n),p),rat(3n)),capture=sub(one,escape),b=16,power=rat(capture[0]**16n,capture[1]**16n),k=bits(power[1]/power[0])-1,e=2*D-k*Math.floor(m/b);
  let budget=rat(1n,2n**BigInt(Math.min(64,Math.max(0,-e)))),exact=null;
  if(m<=512&&D<=512){exact=min(one,mul(rat(3n**BigInt(D)-1n,2n),rat(capture[0]**BigInt(m),capture[1]**BigInt(m))));budget=min(budget,exact);}
  check(2n**BigInt(k)*power[0]<=power[1]&&power[1]<2n**BigInt(k+1)*power[0],"certified capture-power exponent, not3bits for a1/6 bound");
  check(L.feature_dimension===D&&L.row_escape_probability_lower===str(escape)&&L.hyperplane_capture_probability_upper===str(capture)&&L.capture_power_block===16&&L.capture_power_at_block===(Math.max(bits(power[0]),bits(power[1]))<=12000?str(power):null)&&L.capture_power_negative_log2_floor===k&&L.dyadic_rank_union_exponent===e&&L.exact_rank_union_upper_if_short===(exact?str(exact):null)&&L.rank_failure_upper_used===str(budget),"entire projective-hyperplane source rank union");
  same(L.projective_hyperplanes,{base:3,exponent:D,subtract:1,denominator:2},"all linearized hyperplanes");
  check(L.independent_uniform_original_labels_and_label_independent_noise_required===true&&L.actual_source_promise_or_probability_floor_established===false&&L.finite_matrix_rank_is_not_a_source_IID_certificate===true,"distribution is not inferred from successful data");
}
function control(c){
  const {q,n,m}=rawCheck(c.original_records),T=c.truth_fixture_only,R=c.decoder;
  check(T.original_secret.length===n&&T.original_errors.length===m&&T.original_secret.every(s=>integer(s)>=0n&&integer(s)<q),"canonical complete planted-source fixture");
  c.original_records.forEach((s,j)=>check(mod(s.label.reduce((v,a,i)=>v+integer(a)*integer(T.original_secret[i]),0n)+integer(T.original_errors[j]),q)===integer(s.value),"actual source calibration and frozen errors"));
  const verified=result(c.original_records,R);check(c.matches_truth_fixture===(JSON.stringify(R.candidate_secret)===JSON.stringify(T.original_secret))&&c.secret_or_errors_entered_decoder===false&&c.unbounded_Gaussian_noise_is_represented_by_this_calibration===false,"truth only after actual decoding");
  if(R.method==="cubic"){rankBudget(c.cubic_source_rank_budget);check(c.cubic_source_rank_budget.dimension===n&&c.cubic_source_rank_budget.original_rows===m,"confidence on this actual source");same(c.cubic_source_rank_budget.supported_original_noise_residues,c.declared_calibration_noise_alphabet,"declared actual signed vs mixed model");}
  else check(c.cubic_source_rank_budget===null,"do not invent a cubic rank claim for the faster quadratic path");
  return verified;
}
function tuples(q,n){if(!n)return [[]];return tuples(q,n-1).flatMap(a=>Array.from({length:q},(_,i)=>[...a,i]));}
function grid(G){
  const n=G.dimension,D=layout(n,"cubic").length,count=3**(2*n+1);check(count*D<=1000000,"whole coefficient-grid cap");
  const rows=tuples(3,2*n+1).map(p=>equation(Array.from({length:n},(_,i)=>p[i]+3*p[n+i]),p[p.length-1],"cubic")[0]);
  const S=solve(rows,Array(rows.length).fill(0),D);
  check(G.full_public_parameter_grid_rows===count&&G.feature_dimension===D&&G.coefficient_rank_mod3===S.rank&&S.rank===D&&G.coefficient_grid_sha256===digest(rows)&&G.these_rows_are_not_new_oracle_samples===true,"full structural parameter span, not a sample oracle");return count;
}
function escape(C){
  const u=C.secret_low_fixture_only,s=C.noise_alphabet,rows=[];
  for(let a=0;a<9;a++)for(const e of s)rows.push(equation([a],(a*u+e+18)%9,"cubic")[0]);
  const counts=tuples(3,3).filter(v=>v.some(x=>x)).map(v=>rows.filter(row=>row.reduce((z,a,i)=>z+a*v[i],0)%3).length),minimum=Math.min(...counts);
  const actual=rat(BigInt(minimum),BigInt(rows.length)),lower=s.length===3?rat(2n,3n*BigInt(s.length)):rat(1n,3n*BigInt(s.length));
  check(C.public_label_noise_assignments===rows.length&&C.nonzero_duals_checked===26&&C.minimum_actual_escape_probability===str(actual)&&C.claimed_escape_lower===str(lower)&&cmp(actual,lower)>=0n&&C.secret_enters_receiver===false,"complete actual noise-conditioned scalar dual census");return rows.length*26;
}
function falsifier(c){
  rawCheck(c.original_records);const verified=result(c.original_records,c.decoder,c.max_matrix_entries);
  const q=BigInt(c.original_records[0].modulus),T=c.truth_fixture_only;
  check(T.original_secret.length===c.original_records[0].label.length&&T.original_errors.length===c.original_records.length,"complete actual falsifier fixture");
  c.original_records.forEach((s,j)=>check(mod(s.label.reduce((v,a,i)=>v+BigInt(a)*BigInt(T.original_secret[i]),0n)+BigInt(T.original_errors[j]),q)===BigInt(s.value),"actual falsifier source, including deliberately false alphabet"));
  check(c.matches_planted_truth===(JSON.stringify(c.decoder.candidate_secret)===JSON.stringify(T.original_secret))&&c.false_source_alphabet_promise_may_not_be_repaired_from_truth===true,"planted identity not inferred from compatibility");
  if(c.kind==="wrong_planted_secret_with_unique_alphabet_fit")check(c.decoder.fixed_instance_alphabet_uniqueness_certified===true&&c.matches_planted_truth===false,"wrong compatible secret under a false generative premise preserved");
  return verified;
}
function verify(p){
  check(p.status==="POLYNOMIAL_FULL_ROOT_SMALL_ALPHABET_CLASSICAL_BASELINE_EXTERNAL_REVIEW_PENDING","review-pending bounded-source decoder");
  check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_small_alphabet_decoder.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_SMALL_ALPHABET_DECODER.md")),"current source and derivation");
  const deps=["native_affine_fibre_relaxation.py","native_classical_modulus_descent.py","native_small_multiple_completion.py","native_full_root_slice.py","nil3_state_hsp_descent_receiver.py","ternary_covariant_noise.py","ternary_measured_lattice_decoder.py","ternary_phase_qubit_decoder.py","ternary_noise_degradation.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"actual dependencies");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(p.accepted_speedup_candidate===false&&p.new_active_negative_result_created===false&&p.general_Gaussian_LWE_solver_or_new_quantum_algorithm===false&&p.novelty_claim===false,"no quantum/Gaussian/general novelty claim");
  check(p.original_data_controls.length===4&&p.complete_coefficient_grids.length===3&&p.complete_scalar_escape_controls.length===9&&p.falsifier_controls.length===5&&p.scaling_rank_budgets.length===4,"declared actual-source/negative coverage");
  const records=p.original_data_controls.map(control),grids=p.complete_coefficient_grids.map(grid),duals=p.complete_scalar_escape_controls.map(escape);p.falsifier_controls.forEach(falsifier);p.scaling_rank_budgets.forEach(rankBudget);
  return {verified:true,full_root_original_data_controls:4,original_equations_replayed:records.reduce((s,r)=>s+r.rows,0),complete_structural_grid_rows:grids.reduce((a,b)=>a+b,0),scalar_label_noise_dual_checks:duals.reduce((a,b)=>a+b,0),falsifiers:5,quantum_or_general_Gaussian_solver:false};
}
module.exports={verify,equation,solve,layout,result,rankBudget};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));
