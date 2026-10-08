"use strict";

// Independent positive-factor and word-pair character-kernel replay.
const fs=require("fs"),path=require("path");
const {check,same,rat,parse,str,add,mul,div,cmp,mod,field}=require("./cyclotomic_exact");
const out=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../classical_baselines/native_label_access_gate.json"),"utf8"));
check(out.status==="NATIVE_COLLECTIVE_PREFIX_LABEL_ACCESS_WEAK_TRIT_GATE_REVIEW_PENDING","review-pending scoped access result");
for(const name of ["unread_digit_residue_covariance_blocks_are_kept","arbitrary_collective_measurements_WITH_LOW_PREFIX_control_covered","full_frequency_classical_decoding_is_allowed"])check(out[name]===true,"actual scope");
for(const name of ["full_label_quantum_measurements_or_all_polynomial_copies_ruled_out","new_speedup_claimed","novelty_claimed","candidate_accepted"])check(out[name]===false,"no unrestricted lower bound or algorithm");
const pow=(a,n)=>a**BigInt(n),vectors=(q,n)=>n?vectors(q,n-1).flatMap(v=>Array.from({length:q},(_,j)=>[...v,j])):[[]];
same(out.single_site_fourth_moment_SOS,{factor:"5/3",gap_monomials:["a^2","b^2","c^2","ab","ac","bc"],gap_coefficients:["2/3","2/3","2/3","-2/3","-2/3","-2/3"],positive_squared_terms:[["a","b"],["a","c"],["b","c"]].map(difference=>({weight:"1/3",difference}))},"sharp one-site fourth-moment SOS");
const sos=out.single_site_fourth_moment_SOS,polynomial=new Map(sos.gap_monomials.map(x=>[x,rat(0n)]));
for(const term of sos.positive_squared_terms){
  const [a,b]=term.difference,w=parse(term.weight);
  polynomial.set(a+"^2",add(polynomial.get(a+"^2"),w));polynomial.set(b+"^2",add(polynomial.get(b+"^2"),w));polynomial.set(a+b,add(polynomial.get(a+b),mul(rat(-2n),w)));
}
same([...polynomial.values()].map(str),sos.gap_coefficients,"exact positive-square reconstruction");
let effectCount=0,gramEntries=0,entangledFactors=0,higherRankEffects=0;
check(out.exact_collective_POVM_controls.length===9,"all collective and adaptive controls");
for(const c of out.exact_collective_POVM_controls){
  const q=c.modulus,n=c.dimension,ell=c.quantum_low_label_digits,b=3**ell,Q=q/b,K=field(q),D=9;
  check(c.original_native_copies===2&&Number.isInteger(Q)&&Q>=3,"original two-copy source, nontrivial unread modulus");
  for(const rows of [c.fixed_first_low_rows,c.fixed_second_low_rows])check(rows.length===2&&rows.every(row=>row.length===n&&row.every(x=>Number.isInteger(x)&&x>=0&&x<b)),"canonical prefix rows, not full labels disguised as low labels");
  const E=c.effects.map(e=>{check(e.length===D&&e.every(row=>row.length===D),"whole effect dimensions");return e.map(row=>row.map(K.decode));});
  check(E.length===c.positive_effect_factors.length,"one factor list per effect");
  const zeroMatrix=()=>Array.from({length:D},()=>Array.from({length:D},K.F));
  const total=zeroMatrix();
  for(let y=0;y<E.length;y++){
    const actual=zeroMatrix(),terms=c.positive_effect_factors[y];
    if(terms.length>1)higherRankEffects++;
    for(const term of terms){
      const weight=parse(term.positive_weight),v=term.vector.map(K.decode);
      check(weight[0]>0n&&v.length===D,"positive rank-one Gram factor");
      for(let i=0;i<D;i++)for(let j=0;j<D;j++)actual[i][j]=K.plus(actual[i][j],K.scale(K.times(v[i],K.conj(v[j])),weight));
      let entangled=false;
      for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)for(let a=0;a<3;a++)for(let z=a+1;z<3;z++){
        const minor=K.plus(K.times(v[3*i+a],v[3*j+z]),K.scale(K.times(v[3*i+z],v[3*j+a]),rat(-1n)));
        if(!K.eq(minor,K.F()))entangled=true;
      }
      if(entangled)entangledFactors++;
    }
    for(let i=0;i<D;i++)for(let j=0;j<D;j++){
      check(K.eq(actual[i][j],E[y][i][j]),"positive factors reconstruct effect");
      check(K.eq(E[y][i][j],K.conj(E[y][j][i])),"exact Hermiticity");
      total[i][j]=K.plus(total[i][j],E[y][i][j]);
    }
    effectCount++;
  }
  for(let i=0;i<D;i++)for(let j=0;j<D;j++)check(K.eq(total[i][j],i===j?K.unit:K.F()),"exact POVM completeness");
  const masses=c.reference_outcome_masses_exact.map(parse);
  check(masses.length===E.length,"every positive reference mass");
  E.forEach((e,y)=>{
    check(masses[y][0]>0n,"positive outcome mass");
    const trace=e.reduce((v,row,i)=>K.plus(v,row[i]),K.F());
    check(K.eq(K.scale(trace,rat(1n,9n)),K.scale(K.unit,masses[y])),"trace reference, not uniform output assumption");
  });
  const words=vectors(3,2),simplex=[[0,0],[1,0],[0,1]],patterns=new Map();
  const lowValue=r=>Array.from({length:n},(_,l)=>r.reduce((s,z,i)=>s+z*(i%2?c.fixed_second_low_rows:c.fixed_first_low_rows)[Math.floor(i/2)][l],0));
  const coefficients=E.map(e=>{
    const row=new Map();
    for(let i=0;i<D;i++)for(let j=0;j<D;j++)if(i!==j&&!K.eq(e[j][i],K.F())){
      const r=words[i].flatMap((z,a)=>simplex[z].map((v,h)=>v-simplex[words[j][a]][h])),key=JSON.stringify(r);
      if(!patterns.has(key))patterns.set(key,{r,low:lowValue(r)});
      row.set(key,K.plus(row.get(key)||K.F(),K.scale(e[j][i],rat(1n,9n))));
    }
    return row;
  });
  const kernel=[];
  for(const [left,a] of patterns)for(const [right,d] of patterns){
    let value=K.F();
    coefficients.forEach((row,y)=>value=K.plus(value,K.scale(K.times(row.get(left)||K.F(),K.conj(row.get(right)||K.F())),div(rat(1n),masses[y]))));
    if(!K.eq(value,K.F()))kernel.push({a,d,value});
  }
  const all=vectors(q,n),retained=all.filter(s=>s.some(x=>x%Q));
  same(c.ALL_nonzero_high_residue_secrets,retained,"no uncharged secret selection");
  check(c.high_kernel_secret_count===b**n&&c.high_residue_sign_block_size_upper===2*b**n&&c.kernel_secret_removal_is_charged_in_gate_NOT_postselection===true,"kernel mass and residue/sign blocks");
  check(c.full_nonkernel_centered_Gram_exact_rationals.length===retained.length,"complete Gram rows");
  let largest=rat(0n);
  retained.forEach((s,i)=>{
    const stored=c.full_nonkernel_centered_Gram_exact_rationals[i];check(stored.length===retained.length,"complete Gram columns");
    let rowSum=rat(0n);
    retained.forEach((t,j)=>{
      let value=K.F();
      for(const term of kernel){
        if(!term.a.r.every((z,h)=>s.every((x,l)=>mod(x*z-t[l]*term.d.r[h],Q)===0)))continue;
        const exponent=s.reduce((v,x,l)=>v+x*term.a.low[l]-t[l]*term.d.low[l],0);
        value=K.plus(value,K.times(term.value,K.powers[mod(exponent,q)]));
      }
      const rational=parse(stored[j]);
      check(K.eq(value,K.scale(K.unit,rational)),"independent direct word-pair character Gram");
      const related=s.every((x,l)=>mod(x-t[l],Q)===0)||s.every((x,l)=>mod(x+t[l],Q)===0);
      if(!related)check(rational[0]===0n,"no cross-residue covariance");
      if(i===j)check(cmp(rational,rat(16n,9n))<=0n,"sharp tensor L4 diagonal bound");
      rowSum=add(rowSum,rat(rational[0]<0n?-rational[0]:rational[0],rational[1]));gramEntries++;
    });
    if(cmp(rowSum,largest)>0n)largest=rowSum;
  });
  const universal=rat(BigInt(32*b**n),9n);
  check(str(largest)===c.maximum_absolute_Gram_row_sum_exact&&str(universal)===c.universal_nonkernel_operator_bound_exact&&cmp(largest,universal)<=0n,"exact finite Gershgorin bound");
  check(c.conditional_high_lift_census_size===Q**(4*n),"complete population size");
  if(c.conditional_high_lift_census_performed)check(Number.isFinite(c.full_conditional_Born_Gram_error)&&c.full_conditional_Born_Gram_error<3e-11&&c.decoded_using_all_full_labels_and_exponential_secret_enumeration===true,"numeric census and full-label decoder disclosure");
}
check(entangledFactors>0&&higherRankEffects>0,"genuine collective and higher-rank controls");
for(const c of out.scaling_ledgers){
  const n=c.dimension,r=c.root_digits,M=c.charged_native_copies,ell=c.quantum_low_label_digits,V=n*(r-ell);
  check(n>0&&r>ell&&ell>=0&&M>=0,"proper prefix-only access scope");
  same(c.least_trit_advantage_upper,{cap:"2/3",nonkernel_squared:{numerator:{positive_base:5,negative_base:3,exponent:M},denominator:{base:3,exponent:M+V}},kernel_term:{numerator:{base:3,exponent:M,subtract:1},denominator:{base:3,exponent:M+V}}},"factored exact weak-target bound");
  same(c.nonzero_residue_covariance_block_size,{coefficient:2,base:3,exponent:n*ell},"alias block size");
  same(c.kernel_secret_prior_mass,{base:3,exponent:-V},"charged kernel mass");
  const eps=parse(c.desired_advantage_exact),den=pow(3n,M+V),variance=pow(5n,M)-pow(3n,M),rare=pow(3n,M)-1n,gap=eps[0]*den-eps[1]*rare;
  check(c.necessary_copy_access_gate_passed===(gap<=0n||variance*eps[1]*eps[1]*den>=gap*gap),"exact requested-advantage screening, no float gate");
  for(const k of ["arbitrary_collective_POVMs_and_outcome_feedback_covered","unlimited_full_label_FINAL_classical_decoding_covered","numerical_underflow_is_NOT_an_exact_zero_bound"])check(c[k]===true,"correct broad collective and narrow label scope");
  for(const k of ["higher_label_digits_in_quantum_control_covered","filtered_full_label_or_nonIID_source_covered","all_polynomial_copy_receivers_ruled_out","speedup_or_candidate_acceptance_allowed"])check(c[k]===false,"explicit escapes and no admission");
}
for(const c of out.full_label_information_only_escapes){
  const q=c.modulus,M=c.original_native_copies;
  check(q===3**c.root_digits&&M===c.root_digits&&c.cube_words_enumerated===3**M,"actual original-source cube cost");
  const counts=new Map();
  for(const w of vectors(3,M)){
    const y=mod(w.reduce((s,j,i)=>s+(j?(j===1?c.first_frequencies:c.second_frequencies)[i][0]:0),0),q);
    counts.set(y,(counts.get(y)||0)+1);
  }
  same(c.fiber_counts,[...counts].sort((a,b)=>a[0]-b[0]),"original native frequency multiplicities");
  const sums=new Map();for(const [y,count] of counts)sums.set(y%(q/3),(sums.get(y%(q/3))||0)+Math.sqrt(count));
  const trit=[...sums.values()].reduce((s,x)=>s+x*x,0)/(3*3**M);
  check(Math.abs(trit-c.dense_FULL_label_PGM_least_trit_success_information_only)<3e-12,"information-only PGM class law");
  check(c.conditional_cohort_is_NOT_a_population_bound_violation===true&&c.efficient_PGM_compiler_or_fiber_oracle_supplied===false&&c.new_algorithm_or_speedup_claimed===false,"no decoder or population violation from full-label PGM reference");
}
console.log(JSON.stringify({status:"PASS",effectCount,gramEntries,entangledFactors,higherRankEffects,scope:"finite PSD/completeness/character and ledger checks; theorem requires external review"}));
