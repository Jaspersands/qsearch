// Independent exact finite algebra/source checks, NOT independent theorem review.
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const root = path.resolve(__dirname, "../..");
const read = name => JSON.parse(fs.readFileSync(path.join(root,name), "utf8"));
const report = read("research/reductions/native_rlwe_quaternion_kernel.json");
const check = (x,message) => { if (!x) throw new Error(message); };
const ints = a => a.map(BigInt);
const eq = (a,b) => a.length===b.length && a.every((v,i)=>v===b[i]);
const mod = (x,q) => (x%q+q)%q;
const abs = x => x<0n ? -x : x;
const add = (a,b) => a.map((v,i)=>v+b[i]);
const neg = a => a.map(v=>-v);
const bar = a => [a[0],...a.slice(1).reverse().map(v=>-v)];
function mul(a,b) {
  check(a.length===b.length,"ring dimensions");
  const d=a.length, c=Array(d).fill(0n);
  for (let i=0;i<d;i++) for (let j=0;j<d;j++) {
    c[(i+j)%d]+=(i+j<d ? 1n : -1n)*a[i]*b[j];
  }
  return c;
}
const norm = a => mul(a,bar(a));
const member = (g,f,m,q) => add(g,neg(mul(m,f))).every(v=>mod(v,q)===0n);
const centered = (a,q) => a.map(v=>mod(v+q/2n,q)-q/2n);
const matrix = a => a.map(ints);
const mm = (a,b) => a.map(row => b[0].map((_,j)=>row.reduce((s,v,k)=>s+v*b[k][j],0n)));
const transpose = a => a[0].map((_,j)=>a.map(row=>row[j]));
const matrixEq = (a,b) => a.length===b.length && a.every((row,i)=>eq(row,b[i]));
function convolution(a) {
  return a.map((_,i)=>a.map((__,j)=>(i>=j ? 1n : -1n)*a[(i-j+a.length)%a.length]));
}
function determinant(input) {
  const a=input.map(row=>[...row]), n=a.length;
  let previous=1n, sign=1n;
  for (let k=0;k<n-1;k++) {
    if (a[k][k]===0n) {
      const j=a.findIndex((row,i)=>i>k && row[k]!==0n);
      if (j<0) return 0n;
      [a[k],a[j]]=[a[j],a[k]];
      sign=-sign;
    }
    const pivot=a[k][k];
    for (let i=k+1;i<n;i++) for (let j=k+1;j<n;j++) {
      const numerator=a[i][j]*pivot-a[i][k]*a[k][j];
      check(numerator%previous===0n,"Bareiss exact division");
      a[i][j]=numerator/previous;
    }
    for (let i=k+1;i<n;i++) a[i][k]=0n;
    previous=pivot;
  }
  return sign*a[n-1][n-1];
}
let encodings=0, finiteRatios=0, nativeRows=0, unitControlVectors=0, hashes=0;
function verifyEncoding(row) {
  const m=ints(row.canonical_native_ratio), d=m.length, q=BigInt(row.modulus);
  const lift=centered(m,q), n=norm(lift), one=Array(d).fill(0n); one[0]=1n;
  const compatible=add(n,one).every(v=>mod(v,q)===0n);
  check(compatible===row.hamilton_original_metric_left_ideal_compatible,"Hamilton source gate");
  check(row.standard_hamilton_action_original_metric_and_square_verified,"missing physical J0 check");
  const positive=row.adaptive_definite_order, rho=ints(positive.parameter_coefficients);
  check(eq(rho,bar(rho)),"real positive parameter");
  check(add(rho,n).every(v=>mod(v,q)===0n),"left-ideal parameter congruence");
  const off=rho.slice(1).reduce((s,v)=>s+abs(v),0n);
  const residue=centered(neg(n),q), energy=residue.reduce((s,v)=>s+v*v,0n);
  check(BigInt(positive.every_positive_congruence_lift_lambda_max_squared_lower_bound)===energy,"all-lifts spectral obstruction");
  check(BigInt(positive.every_positive_congruence_lift_full_metric_condition_number_squared_lower_bound)===energy,"all-lifts full-metric obstruction");
  check(rho.reduce((s,v)=>s+v*v,0n)>=energy,"centered residue minimizes energy");
  const units=positive.norm_one_units, hamilton=eq(rho,one);
  check(units.exact_count===(hamilton ? 4*d : 2*d),"constructed-order norm-one count");
  check(units.cannot_change_R_projective_direction===!hamilton,"norm-one projective scope");
  check(units.fixed_reduced_norm_principal_generators_original_physical_length_invariant && !units.general_units_or_different_reduced_norms_classified,"fixed-norm orbit scope");
  check(rho[0]-off>=1n,"strict positive spectral lower bound");
  check(rho[0]-off===BigInt(positive.exact_spectral_lower_bound),"lower bound");
  check(rho[0]+off===BigInt(positive.exact_spectral_upper_bound),"upper bound");
  const C=convolution(rho);
  check(matrixEq(C,transpose(C)),"self adjoint metric");
  const principal=row.adaptive_known_principal_order, p=ints(principal.parameter_coefficients);
  check(eq(p,add(one.map(v=>q*v),neg(n))),"known principal parameter");
  check(eq(add(n,p),one.map(v=>q*v)),"known generator norm");
  check(principal.zero_parameter_is_degenerate_NOT_quaternion_PIP_input===p.every(v=>v===0n),"degenerate quaternion gate");
  check(principal.nonzero_parameter_defines_a_quaternion_algebra===p.some(v=>v!==0n),"nondegenerate quaternion gate");
  check(positive.principality_promised_or_proved===eq(p,rho),"limited positive principality promise");
  check(BigInt(principal.generator_physical_norm_squared)===lift.reduce((s,v)=>s+v*v,1n),"physical generator norm");
  check(eq(ints(principal.known_generator[0]),lift) && eq(ints(principal.known_generator[1]),one),"known generator supplied");
  check(!principal.PIP_has_an_unknown_generator_to_find && !principal.source_metric_or_shortness_guarantee_supplied,"unearned generator guarantee");
  check(!row.candidate_record_accepted && !row.novelty_claim && !row.speedup_claim_allowed,"claim promotion");
  if (row.finite_algebra_certificate) {
    const certificate=row.finite_algebra_certificate;
    const B=matrix(certificate.graph_kernel_column_basis), J=matrix(certificate.positive_order_left_j);
    const G=matrix(certificate.known_principal_generator_basis);
    const C_m=convolution(lift), C_p=convolution(p);
    const unit=(i,j)=>i===j ? 1n : 0n;
    const expectedB=Array.from({length:2*d},(_,i)=>Array.from({length:2*d},(_,j)=>
      i<d ? (j<d ? q*unit(i,j) : C_m[i][j-d]) : (j<d ? 0n : unit(i-d,j-d))));
    const expectedG=Array.from({length:2*d},(_,i)=>Array.from({length:2*d},(_,j)=>
      i<d ? (j<d ? C_m[i][j] : -C_p[i][j-d]) : (j<d ? unit(i-d,j) : C_m[j-d][i-d])));
    check(matrixEq(B,expectedB) && matrixEq(G,expectedG),"actual complete kernel/generator bases");
    const expectedJ=Array.from({length:2*d},()=>Array(2*d).fill(0n));
    for (let j=0;j<2*d;j++) {
      const e=Array(d).fill(0n); e[j%d]=1n;
      const v=j<d ? [...Array(d).fill(0n),...bar(e)] : [...neg(mul(rho,bar(e))),...Array(d).fill(0n)];
      v.forEach((x,i)=>{ expectedJ[i][j]=x; });
    }
    check(matrixEq(J,expectedJ),"actual left quaternion action");
    const JB=mm(J,B);
    for (const v of transpose(JB)) check(member(v.slice(0,d),v.slice(d),lift,q),"full left closure");
    for (const v of transpose(G)) check(member(v.slice(0,d),v.slice(d),lift,q),"principal basis membership");
    check(abs(determinant(B))===q**BigInt(d) && abs(determinant(G))===q**BigInt(d),"full index, not one contained relation");
    check(BigInt(principal.exact_basis_determinant)===q**BigInt(d),"reported index");
  }
  encodings++;
}
for (const row of report.random_algebra_controls) verifyEncoding(row);
const native=report.same_saved_native_d64_kernel;
verifyEncoding(native);
const original=read("research/certificates/native_rlwe_babai_profile_d64.json");
const originalRatio=ints(original.native_ratio), q=BigInt(original.q), d=originalRatio.length;
const graphRatio=bar(originalRatio).map(v=>mod(v,q));
check(eq(ints(native.canonical_native_ratio),graphRatio),"native ADJOINT convention, not an unrecorded transpose");
check(eq(ints(native.original_saved_ratio),originalRatio),"native ratio provenance");
check(native.graph_ratio_is_original_adjoint && native.coordinate_map_is_exact_signed_isometry,"native coordinate isometry debt");
for (const row of original.reduced_row_basis) {
  const x=ints(row.slice(0,d)), y=ints(row.slice(d));
  check(member(x,neg(y),graphRatio,q),"actual saved native basis row");
  nativeRows++;
}
check(native.saved_native_reduced_basis_rows_checked===nativeRows,"native coverage");
for (const row of report.complete_finite_source_counts) {
  const d=row.d, q=BigInt(row.q), limit=q**BigInt(d);
  let count=0, energySum=0n, energySquareSum=0n;
  for (let k=0n;k<limit;k++) {
    let j=k;
    const a=Array.from({length:d},()=>{ const v=j%q; j/=q; return v; });
    const n=norm(a);
    if (n.every((v,i)=>mod(v+(i===0 ? 1n : 0n),q)===0n)) count++;
    const energy=centered(n,q).reduce((s,v)=>s+v*v,0n);
    energySum+=energy; energySquareSum+=energy*energy;
    finiteRatios++;
  }
  check(count===row.eligible_ratio_count,"complete native source count");
  check(BigInt(row.all_ratio_count)===limit,"full source denominator");
  check(BigInt(count)===(d===2 ? q+1n : q**BigInt(d/2)-1n),"correct CRT regime, including d2 exception");
  check(BigInt(row.native_centered_real_norm_energy_sum)===energySum,"exact native energy first moment");
  check(BigInt(row.native_centered_real_norm_energy_square_sum)===energySquareSum,"exact native energy second moment");
  if (d>=4) {
    const x=q**BigInt(d/2), w=BigInt(d-1), v=BigInt(2*d-3), t=q*q-1n;
    // mu2=t/12; mu4=t*(3q^2-7)/240. Integer cross-products
    // keep the entire source-mixture calculation exact.
    check(energySum*x*12n===limit*(x-1n)*w*t,"uniform-plus-zero mixture mean");
    const momentNumerator=5n*w*w*t*t+v*(3n*t*(3n*q*q-7n)-5n*t*t);
    check(energySquareSum*x*720n===limit*(x-1n)*momentNumerator,"uniform-plus-zero mixture second moment");
  }
}
for (const row of report.growing_native_source_gates) {
  const q=BigInt(row.modulus), x=q**BigInt(row.dimension/2);
  check(q%8n===3n && row.dimension>=4,"CRT assumptions");
  check(BigInt("0x"+row.exact_full_source_probability.numerator_hex)===x-1n,"source numerator");
  check(BigInt("0x"+row.exact_full_source_probability.denominator_hex)===x*x,"source denominator");
  check(BigInt("0x"+row.conditional_on_unit_ratio_probability.denominator_hex)===x-1n,"unit conditioning");
  check(row.full_source_probability_upper_bound_dyadic_exponent===x.toString(2).length-1,"conservative dyadic bound");
  const metric=row.unavoidable_positive_lift_metric_distortion, t=q*q-1n;
  const w=BigInt(row.dimension-1), v=BigInt(2*row.dimension-3);
  const fraction=(f,n,d)=>check(BigInt(f.numerator)*d===n*BigInt(f.denominator),"exact metric fraction");
  fraction(metric.uniform_real_centered_coefficient_energy_mean,w*t,12n);
  fraction(metric.uniform_real_centered_coefficient_energy_variance,v*(3n*t*(3n*q*q-7n)-5n*t*t),720n);
  fraction(metric.lambda_max_and_full_metric_condition_number_squared_threshold,w*t,24n);
  const chebDenominator=5n*w*w*t*t;
  const chebNumerator=chebDenominator-4n*v*(3n*t*(3n*q*q-7n)-5n*t*t);
  const p=metric.source_probability_lower_bound;
  check(BigInt("0x"+p.numerator_hex)*x*chebDenominator===BigInt("0x"+p.denominator_hex)*(x-1n)*(chebNumerator>0n ? chebNumerator : 0n),"exact Chebyshev mixture probability");
  check(metric.all_positive_lifts_covered_not_just_constructed_lift && !metric.different_coordinate_maps_or_all_weighted_algorithms_ruled_out,"metric theorem scope");
  check(!row.speedup_claim_allowed,"source count is not an algorithm");
}
const counter=report.known_long_generator_short_nongenerator_countercontrol;
verifyEncoding(counter.encoding);
check(member(ints(counter.short_relation[0]),ints(counter.short_relation[1]),[128n,0n],257n),"short nongenerator exists");
check(counter.short_physical_norm_squared===5,"short norm");
check(BigInt(counter.every_principal_generator_norm_squared_lower_bound_for_this_d2_order)===128n**2n-2n*257n,"all-generator physical lower bound");
for (const [q,rho,count] of [[7n,[5n,0n],4],[3n,[1n,0n],8]]) {
  let unitCount=0, fixedCount=0;
  for (let a=-2n;a<=2n;a++) for (let b=-2n;b<=2n;b++) {
    for (let c=-2n;c<=2n;c++) for (let e=-2n;e<=2n;e++) {
      const g=[a,b], f=[c,e], nr=add(norm(g),mul(rho,norm(f)));
      if (eq(nr,[1n,0n])) unitCount++;
      if (eq(nr,[q,0n]) && member(g,f,[1n,1n],q)) {
        check(a*a+b*b+c*c+e*e===3n,"fixed-norm generators cannot change physical length in this control");
        fixedCount++;
      }
      unitControlVectors++;
    }
  }
  check(unitCount===count && fixedCount===count,"actual norm-one and fixed-generator control orbits");
}
check(!report.claim_gate.speedup_claim_allowed && !report.claim_gate.independent_review,"report review/advantage debt");
check(!report.claim_gate.all_weighted_quaternion_or_general_quantum_algorithms_ruled_out,"scope overreach");
for (const [name,expected] of Object.entries(report.dependency_sha256)) {
  const actual=crypto.createHash("sha256").update(fs.readFileSync(path.join(root,name))).digest("hex");
  check(actual===expected,`stale dependency: ${name}`); hashes++;
}
console.log(JSON.stringify({status:"BOUNDED_EXACT_CROSSCHECK_PASSED_NOT_INDEPENDENT_REVIEW",encodings,finiteRatios,nativeRows,unitControlVectors,hashes}));
