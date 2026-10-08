"use strict";

const fs=require("fs"),path=require("path");
const {check,same,rat,sub,mul,str,mod,field}=require("./cyclotomic_exact");
const out=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../classical_baselines/native_echo_shifted_probe_gate.json"),"utf8"));
check(out.status==="NATIVE_ONE_ECHO_SHIFTED_PROBE_WEAK_TRIT_GATE_REVIEW_PENDING","local derivation review pending");
for(const k of ["full_A_frequency_inverse_calibration_is_covered","large_copy_surplus_or_wide_mediators_ruled_out","general_native_weak_learner_ruled_out","novelty_claimed"])check(out[k]===false,"explicit scope escapes");
const vectors=(q,n)=>n?vectors(q,n-1).flatMap(v=>Array.from({length:q},(_,j)=>[...v,j])):[[]];
const basis=[[0,0],[1,0],[0,1]],quartets=vectors(3,4);
same(out.complete_single_copy_character_quartets.map(c=>c.indices),quartets,"complete81 source character quartets");
const difference=(x,y)=>x.map((z,i)=>z-y[i]);
const det=(a,b)=>a[0]*b[1]-a[1]*b[0];
for(const [i,c] of out.complete_single_copy_character_quartets.entries()){
  const [j,k,l,h]=quartets[i],r=difference(basis[j],basis[k]),p=difference(basis[l],basis[h]);
  let name;
  if(mod(k-j+l-h,3))name="cancelled_by_measured_word_Fourier_character";
  else if(r.every(x=>!x)&&p.every(x=>!x))name="secret_independent_diagonal_background";
  else if(r.every((x,a)=>x===p[a]))name="equal_secrets_only_same_ordered_simplex_root";
  else{
    name="only_the_two_public_shift_exceptions";
    const d=det(r,p),ca=difference(basis[j],basis[l]),cb=difference(basis[k],basis[h]);
    // Independently solve the two coefficient systems by Cramer's rule.
    const columns=[ca,cb.map(x=>-x)],s=columns.map(x=>-det(x,p)/d),t=columns.map(x=>det(r,x)/d);
    check(Math.abs(d)===1&&c.unit_root_determinant===d,"unit elimination over every ternary modulus");
    same(c.exceptional_first_secret_coefficients,s,"first exceptional secret");
    same(c.exceptional_second_secret_coefficients,t,"second exceptional secret");
  }
  check(c.class===name,"independent quartet class");
}
const power=(a,n)=>{let b=rat(1n);for(let i=0;i<n;i++)b=mul(b,a);return b;};
let gramEntries=0;
same(out.exact_centered_Gram_controls.map(c=>[c.modulus,c.left_public_shift,c.right_public_shift,c.A_source_copies]),[[9,[2],[7],1],[9,[2],[7],3],[9,[2],[2],3],[3,[1,0],[2,1],2],[27,[5],[18],2]],"complete Gram controls");
for(const c of out.exact_centered_Gram_controls){
  const q=c.modulus,left=c.left_public_shift,right=c.right_public_shift,n=c.secret_dimension,m=c.A_source_copies;
  const exceptions=[...new Map([left,right].map(v=>{const a=v.map(x=>mod(-x,q));return [JSON.stringify(a),a];})).values()].sort((a,b)=>{for(let i=0;i<a.length;i++)if(a[i]!==b[i])return a[i]-b[i];return 0;});
  const good=vectors(q,n).filter(s=>!exceptions.some(e=>s.every((x,i)=>x===e[i])));
  same(c.all_nonexceptional_secrets,good,"no unreported secret removal");
  same(c.exceptional_secrets,exceptions,"exact two public exceptions");
  const equal=left.every((x,i)=>x===right[i]),background=power(rat(1n,equal?1n:3n),m);
  check(c.secret_independent_background_squared_norm===str(background),"background squared norm");
  check(c.full_centered_probe_Gram_exact_rationals.length===good.length,"whole Gram rows");
  good.forEach((s,i)=>{
    check(c.full_centered_probe_Gram_exact_rationals[i].length===good.length,"whole Gram columns");
    good.forEach((t,h)=>{
      const count=quartets.filter(([j,k,l,z])=>!mod(k-j+l-z,3)&&s.every((v,a)=>[0,1].every(b=>!mod((v+left[a])*basis[j][b]-(v+right[a])*basis[k][b]-(t[a]+left[a])*basis[l][b]+(t[a]+right[a])*basis[z][b],q)))).length;
      const value=sub(power(rat(BigInt(count),9n),m),background);
      check(c.full_centered_probe_Gram_exact_rationals[i][h]===str(value),"independently replayed rational tensor Gram");
      const expected=i!==h?rat(0n):equal?sub(power(rat(5n,3n),m),rat(1n)):sub(rat(1n),power(rat(1n,3n),m));
      check(str(value)===str(expected),"claimed diagonal/orthogonality");gramEntries++;
    });
  });
}
for(const c of out.growing_weak_trit_ledgers){
  const N=c.secret_dimension*c.root_digits,w=c.mediator_width,M=c.original_source_copies,L=c.precommitted_A_independent_policy_count,W=3**w;
  check(c.mediator_basis_size===W&&c.A_source_copies===M-w&&c.original_even_native_level===2*c.root_digits,"actual source accounting");
  same(c.least_trit_mean_advantage_upper_bound,{cap:"2/3",rare_background_and_public_guess_mass:{numerator:W*(W-1)+L*W,denominator:{base:3,exponent:N}},centered_probe_term:{coefficient_squared:L*W*W,Gram_variance_bound:{base:"5/3",exponent:M-w,subtract:1},denominator:{coefficient:2,base:3,exponent:N},outer_operation:"square_root"}},"weak-target bound, not full-secret dimension bound");
  same(c.directed_rational_majorant,{cap:"2/3",rare_term_numerator:W*(W-1)+L*W,rare_term_denominator:{base:3,exponent:N},decay_term_coefficient:L*W,surplus_factor:{base:"5/3",exponent:Math.ceil(Math.max(M-N,0)/2)},exponential_decay:{base:"3/4",exponent:N}},"directed rational decay envelope");
  check(c.fixed_menu_selection_using_full_A_labels_covered===true&&c.public_couplings_may_use_full_B_labels===true&&c.classical_unknown_secret_postprocessing_unlimited_in_bound===true,"selection and inference scope");
  for(const k of ["coupling_values_depending_on_full_A_labels_OUTSIDE_fixed_menu_covered","wide_mediator_or_large_copy_surplus_ruled_out","multiple_interleaved_echo_rounds_ruled_out","arbitrary_orbit_coupling_receivers_ruled_out"])check(c[k]===false,"scope guards");
}
let adaptiveEscapeRecords=0;
const escapes=[out.full_A_inverse_calibration_countercontrol,...out.growing_root_inverse_calibration_countercontrols];
same(escapes.map(c=>c.modulus),[9,27,81],"all growing-root countercontrols");
for(const escape of escapes){
const q=escape.modulus,K=field(q);
check(escape.A_source_copies===1&&escape.left_shift===0&&escape.complete_IID_label_outcome_records===3*q*q,"complete original calibrated countercontrol");
same(escape.two_nonexceptional_secrets,[q/3,2*q/3],"nonexceptional pair");
check(escape.rank_failures_retained===true&&escape.source_labels_rejected===false&&escape.A_independent_orthogonality_extension_is_false===true&&escape.positive_receiver_or_decoder_follows===false,"escape, not a positive algorithm");
check(escape.right_shift_rule===`inverse(a) modulo${q} if a is a unit, otherwise0`,"full A inverse-label policy");
const coefficients=Array(q).fill(0);
const unitCoefficients=Array(q).fill(0),nonunitCoefficients=Array(q).fill(0);
for(let a=0;a<q;a++)for(let c=0;c<q;c++)for(let z=0;z<3;z++){
  const d=a%3?Array.from({length:q},(_,j)=>j).find(j=>mod(a*j,q)===1):0,values=[0,a,c];
  const Z=[q/3,2*q/3].map(s=>{
    check(s!==mod(-d,q),"no adaptive exception omitted");
    const counts=Array(q).fill(0);
    for(let j=0;j<3;j++)for(let k=0;k<3;k++)counts[mod(s*values[j]-(s+d)*values[k]-(q/3)*z*(j-k),q)]++;
    for(const v of values)counts[mod(-d*v,q)]--;
    return counts;
  });
  for(let i=0;i<q;i++)if(Z[0][i])for(let j=0;j<q;j++)if(Z[1][j]){
    const index=mod(i-j,q),v=Z[0][i]*Z[1][j];coefficients[index]+=v;(a%3?unitCoefficients:nonunitCoefficients)[index]+=v;
  }
}
same(escape.root_off_diagonal_numerator_coefficients_ascending,coefficients,"exact full-label root histogram");
const inner=coefficients.reduce((v,count,i)=>K.plus(v,K.scale(K.powers[i],rat(BigInt(count),BigInt(27*q*q)))),K.F());
check(K.eq(inner,K.scale(K.unit,rat(4n,27n)))&&escape.exact_nonzero_centered_Gram_entry==="4/27","exact nonorthogonality forbids a general calibrated cut");
for(const [histogram,denominator,value,name] of [[unitCoefficients,18*q*q,rat(-1n,9n),"conditional_unit_A_Gram_entry"],[nonunitCoefficients,9*q*q,rat(2n,3n),"conditional_nonunit_A_zero_fallback_Gram_entry"]]){
  const conditional=histogram.reduce((v,count,i)=>K.plus(v,K.scale(K.powers[i],rat(BigInt(count),BigInt(denominator)))),K.F());
  check(K.eq(conditional,K.scale(K.unit,value))&&escape[name]===str(value),"exact conditional source partition");
}
adaptiveEscapeRecords+=3*q*q;
}
same(out.growing_root_adaptive_escape_derivation,{root_digits_minimum:2,conditional_unit_A_Gram_entry:"-1/9",conditional_nonunit_A_zero_fallback_Gram_entry:"2/3",unit_A_probability:"2/3",nonunit_A_probability:"1/3",unconditional_Gram_entry:"4/27",external_derivation_review_pending:true},"review-pending growing-root derivation ledger");
console.log(JSON.stringify({status:"PASS",characterQuartets:81,gramEntries,adaptiveEscapeRecords,scope:"finite exact identities; asymptotic argument requires mathematical review"}));
