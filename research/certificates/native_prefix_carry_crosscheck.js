"use strict";
// Exact actual prefix words, compact divided-cube arithmetic and canonical cubics.
// First two digits only; no solver or growing-root coherent sampler is certified.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,same,rat,str}=require("./cyclotomic_exact.js");
const A=require("./native_affine_fibre_crosscheck.js"),H=require("./native_short_preimage_crosscheck.js");
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/native_prefix_carry_lift.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex"),mod=(x,q)=>(x%q+q)%q;
const tuples=(n)=>n?tuples(n-1).flatMap(a=>[0,1,2].map(x=>[...a,x])):[[]];
const trits=a=>a.every(x=>Number.isInteger(x)&&x>=0&&x<3);
function compact(s,u) {
  const n=s.next_digit_equations,out=s.F3_constants.map((c,i)=>BigInt(c)+s.F3_linear_coefficients[i].reduce((v,a,l)=>v+BigInt(a*u[l]),0n)+s.F3_diagonal_quadratic[i].reduce((v,a,l)=>v+BigInt(a*u[l]*u[l]),0n));
  s.pivot_affine_forms.forEach((f,j)=>{
    const b=f.coefficients,L=b.reduce((v,a,l)=>v+BigInt(a*u[l]),0n),numerator=L**3n-b.reduce((v,a,l)=>v+BigInt(a)**3n*BigInt(u[l])**3n,0n);
    check(numerator%3n===0n,"integer divided cube is legitimate");
    const square=b.reduce((v,a,l)=>v+BigInt(a*u[l]*u[l]),0n);
    for(let i=0;i<n;i++){const w=s.F3_pivot_weights[j][i];out[i]+=BigInt(w.square)*L*L+BigInt(w.cube)*(square+numerator/3n);}
  });
  return out.map(x=>Number(mod(x,3n)));
}
function polys(p,u) {return p.map(row=>row.reduce((s,m)=>s+m.coefficient*m.powers.reduce((v,p,l)=>v*u[l]**p,1),0)%3);}
function recompile(s,f,target,offsets) {
  const n=f.dimension,k=s.free_trits,pairs=f.paired_labels[s.cohort],constants=[],linear=[],diagonal=[],weights=s.pivot_affine_forms.map(()=>[]);
  for(let i=0;i<n;i++) {
    let constant=pairs.reduce((v,[a])=>v+BigInt(a[i]),0n)-BigInt(target[i]);const row=Array(k).fill(0n),diag=[];
    s.pivot_affine_forms.forEach((form,j)=>{
      const site=form.site,c=BigInt(form.offset),b=form.coefficients.map(BigInt),a=BigInt(pairs[site][0][i]),w=BigInt(pairs[site][1][i])-2n*a;
      constant+=w*c**3n+3n*a*c*(c-1n);
      for(let l=0;l<k;l++)row[l]+=w*(3n*c*c*b[l]-2n*b[l]**3n)+3n*a*(2n*c-1n)*b[l];
      weights[j].push({square:Number(mod(w*c+a,3n)),cube:Number(mod(w,3n))});
    });
    s.prefix_recipe.free_columns.forEach((site,l)=>{const a=BigInt(pairs[site][0][i]),w=BigInt(pairs[site][1][i])-2n*a;row[l]+=-2n*w-3n*a;diag.push(Number(mod(w+a,3n)));});
    check(constant%3n===0n&&row.every(x=>x%3n===0n),"coefficientwise divisibility after actual prefix constraints");
    constants.push(Number(mod(constant,9n)/3n));linear.push(row.map(x=>Number(mod(x,9n)/3n)));diagonal.push(diag);
  }
  same(s.F3_constants,constants,"actual divided constant coefficients");same(s.F3_linear_coefficients,linear,"actual divided linear coefficients");same(s.F3_diagonal_quadratic,diagonal,"actual free-site diagonal quadratic");same(s.F3_pivot_weights,weights,"actual pivot square/divided-cube weights");
}
function bounded(c) {
  const f=c.public_family,q=BigInt(f.modulus),B=f.cohorts,M=f.sites,n=f.dimension;
  check(q>=9n&&Number.isInteger(n)&&n>0&&Number.isInteger(B)&&B>0&&(B&(B-1))===0&&Number.isInteger(M)&&M>=n,"valid first-carry native shape");
  let root=q;while(root%3n===0n&&root>1n)root/=3n;check(root===1n,"true ternary root");
  check(f.paired_labels.length===B&&f.paired_labels.every(c=>c.length===M&&c.every(p=>p.length===2&&p.every(a=>a.length===n&&a.every(x=>BigInt(x)>=0n&&BigInt(x)<q))))&&f.responses_masks_source_IDs_and_errors_supplied===false,"actual original public pairs only");
  const slopes=b=>Array.from({length:n},(_,i)=>f.paired_labels[b].map(([a,d])=>Number(mod(BigInt(a[i])+BigInt(d[i]),3n))));
  if(c.status==="PREFIX_RANK_UNSUPPORTED_NOT_NO_WORDS") {
    check(Array.from({length:B},(_,b)=>A.rank3(slopes(b))).some(rank=>rank<n)&&c.source_impossibility_or_general_no_go_inferred===false,"unsupported prefix rank is not absence of native words");return {words:0,equations:0,unsupported:1};
  }
  check(c.status==="EXACT_COMPACT_MOD9_CARRY_AND_COMPLETE_PREFIX_WORD_CONTROL"&&c.new_cubic_solver_or_full_root_row_circuit===false,"exact first-carry reference, no solver");
  check(c.target.length===n&&c.target.every(x=>BigInt(x)>=0n&&BigInt(x)<q)&&c.cohort_controls.length===B&&B*3**(M-n)<=4096,"canonical target and complete bounded cohort coverage");
  let checked=0;
  c.cohort_controls.forEach((control,b)=>{
    const s=control.compact_circuit;check(s.cohort===b&&s.free_trits===M-n&&s.next_digit_equations===n&&s.total_degree_upper===3,"actual prefix circuit shape");same(s.public_family,f,"same actual label family");same(s.target,c.target,"same actual target");check(s.prefix_recipe.modulus==="3","only low-prefix F3 coordinates are linear");
    const P=A.recipe(s.prefix_recipe,slopes(b)),offset=Array.from({length:n},(_,i)=>Number(mod(f.paired_labels[b].reduce((v,[a])=>v+BigInt(a[i]),0n),3n))),rhs=c.target.map((x,i)=>Number(mod(BigInt(x)-BigInt(offset[i]),3n))),zero=Array(M-n).fill(0),word0=P.solve(rhs,zero);
    same(s.word_offsets,word0,"actual low-prefix affine word offsets");
    const coefficients=Array.from({length:M-n},(_,l)=>{const u=[...zero];u[l]=1;return P.solve(rhs,u).map((x,i)=>(x-word0[i]+3)%3);});
    const forms=s.prefix_recipe.pivot_columns.map(site=>({site,offset:word0[site],coefficients:coefficients.map(row=>row[site])}));same(s.pivot_affine_forms,forms,"actual dense pivot forms, not fictitious independent variables");
    check(s.dense_divided_cube_forms_upper===n&&s.coefficient_division_by3_is_verified_integer_division===true&&s.matching_mod9_implies_full_root_matching===(q===9n),"actual cubic and carry scope");
    ["expanded_cubic_tensor_materialized","divided_cubes_are_ordinary_rank_one_F3_cubes","source_values_mask_secret_or_errors_supplied","polynomial_cubic_solver_or_uniform_row_sampler_supplied","physical_row_preparation_circuit_executed"].forEach(k=>check(s[k]===false,"compact circuit scope "+k));
    check(s.F3_constants.length===n&&trits(s.F3_constants)&&s.F3_linear_coefficients.length===n&&s.F3_diagonal_quadratic.length===n&&[...s.F3_linear_coefficients,...s.F3_diagonal_quadratic].every(row=>row.length===M-n&&trits(row)),"canonical F3 coefficient arrays");
    recompile(s,f,c.target,word0);
    check(control.canonical_polynomials.length===n,"all n canonical carry equations");
    control.canonical_polynomials.forEach(poly=>{
      const keys=poly.map(m=>JSON.stringify(m.powers));check(new Set(keys).size===keys.length,"unique canonical monomials");same(keys,[...keys].sort(),"canonical polynomial order");
      check(poly.every(m=>m.powers.length===M-n&&trits(m.powers)&&m.powers.reduce((a,b)=>a+b,0)<=3&&[1,2].includes(m.coefficient)),"canonical F3 polynomial is degree at most3, not a fit with hidden high degree");
    });
    const free=tuples(M-n),rows=control.complete_prefix_word_rows;check(rows.length===free.length,"complete prefix word table");
    let mod9Hits=0,fullHits=0;
    free.forEach((u,j)=>{
      const w=P.solve(rhs,u),frequency=H.frequency(f,b,w),actual=frequency.map((x,i)=>mod(BigInt(x)-BigInt(c.target[i]),9n));check(actual.every(x=>x%3n===0n),"actual word matches its low prefix");
      const residual=actual.map(x=>Number(x/3n)),value=compact(s,u);same(value,residual,"compact actual native carry, not a linear substitute");same(polys(control.canonical_polynomials,u),residual,"canonical cubic equals actual native function everywhere");
      const mod9Match=residual.every(x=>x===0),fullMatch=frequency.every((x,i)=>BigInt(x)===BigInt(c.target[i]));mod9Hits+=Number(mod9Match);fullHits+=Number(fullMatch);
      same(rows[j],{free_trits:u,native_word:w,actual_frequency:frequency,next_digit_residual:residual,matches_mod9_target:mod9Match,matches_entire_root_target:fullMatch},"exact actual prefix word and distinct full-root predicate");checked++;
    });
    check(control.mod9_filter_acceptance===str(rat(BigInt(mod9Hits),BigInt(free.length)))&&control.entire_root_filter_acceptance===str(rat(BigInt(fullHits),BigInt(free.length))),"raw conditional-prefix filter laws, zero acceptances retained");
  });
  check(c.complete_prefix_words_checked===checked,"all cohort prefixes charged");return {words:checked,equations:B*n,unsupported:0};
}
function ledger(L) {
  const n=L.dimension,r=L.root_digits,B=L.cohorts,M=L.sites;check([n,r,B,M].every(x=>Number.isSafeInteger(x)&&x>0)&&(B&(B-1))===0&&M>=n,"full prefix shape");
  check(L.free_native_word_trits_per_cohort===M-n,"native prefix entropy, not unrestricted coefficient entropy");
  const mean={base:3,negative_exponent:n*(r-1)};same(L.uniform_higher_target_mean_acceptance,mean,"uniform higher-target mean");same(L.prescribed_target_ensemble_mean_under_uniform_higher_labels,mean,"separate population mean");
  check(L.ordinary_amplification_mean_acceptance_upper==="min(1,(2j+1)^2*3^[-n(r-1)])","scoped ordinary-amplification mean price");
  ["full_prefix_rank_in_each_cohort_required","IID_uniform_higher_original_labels_conditioned_on_low_labels_required_for_prescribed_target_mean","prescribed_target_fixed_conditioned_on_low_labels_before_higher_labels_required","prefix_basis_and_cohort_weights_depend_only_on_low_labels_required"].forEach(k=>check(L[k]===true,"prefix/filter population premise "+k));
  ["uniform_target_mean_is_a_per_dataset_prescribed_target_promise","population_law_established_by_finite_artifact","later_digit_equations_proved_degree3","generic_carry_solvers_excluded","accepted_speedup_candidate"].forEach(k=>check(L[k]===false,"prefix/filter scope "+k));
}
function verify(p) {
  check(p.status==="COMPACT_NATIVE_FIRST_CARRY_EQUATIONS_AND_PREFIX_ROW_REFERENCE_REVIEW_PENDING","review-pending first-carry derivation");
  check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_prefix_carry_lift.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_PREFIX_CARRY_LIFT.md")),"live source and derivation hashes");
  const deps=["native_affine_fibre_relaxation.py","native_known_seed_group_workbench.py","native_short_preimage_reduction.py","known_preparation_coherent_reflection.py","ternary_covariant_noise.py","ternary_measured_lattice_decoder.py","ternary_noise_degradation.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"direct provenance");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(p.bounded_carry_controls.length===5&&p.growing_prefix_filter_ledgers.length===4,"declared live coverage");
  const stats=p.bounded_carry_controls.map(bounded);p.growing_prefix_filter_ledgers.forEach(ledger);
  ["polynomial_cubic_solver_or_full_root_row_circuit","accepted_speedup_candidate","new_active_negative_result_created"].forEach(k=>check(p[k]===false,"report scope "+k));
  return {verified:true,actual_prefix_words:stats.reduce((a,s)=>a+s.words,0),canonical_carry_equations:stats.reduce((a,s)=>a+s.equations,0),unsupported_controls:stats.reduce((a,s)=>a+s.unsupported,0),scaling_ledgers:4,growing_root_solver_supplied:false};
}
module.exports={verify,compact,bounded,ledger,recompile};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));
