"use strict";
// Standalone BigInt proof controls; no quantum-source or candidate is supplied.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const report=JSON.parse(fs.readFileSync(path.join(__dirname,"../phase_workbench/ternary_proper_marginal_gap.json"),"utf8"));
const derivation=fs.readFileSync(path.join(__dirname,"../NATIVE_PROPER_MARGINAL_GAP_DERIVATION.md"));
function check(x,message){if(!x)throw Error(message);}
const abs=x=>x<0n?-x:x;
function gcd(a,b){a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a;}
function F(a,b=1n){check(b!==0n,"nonzero exact denominator");if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];}
function q(s){check(typeof s==="string","canonical exact string required");const p=s.split("/");check(p.length<=2,"exact rational syntax");const x=F(BigInt(p[0]),p.length===2?BigInt(p[1]):1n);check(s===(x[1]===1n?String(x[0]):x[0]+"/"+x[1]),"canonical rational, never decimal/alias");return x;}
const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]),eq=(a,b)=>a[0]*b[1]===b[0]*a[1];
const same=(a,b,message)=>check(JSON.stringify(a)===JSON.stringify(b),message),bits=x=>x===0n?0:abs(x).toString(2).length;
const cache=new Map();
function bin(n,h){check(Number.isSafeInteger(n)&&n>=0&&Number.isSafeInteger(h),"exact native binomial coordinates");if(h<0||h>n)return 0n;h=Math.min(h,n-h);const key=n+","+h;if(cache.has(key))return cache.get(key);let v=1n;for(let i=1;i<=h;i++)v=v*BigInt(n-h+i)/BigInt(i);cache.set(key,v);return v;}
function word(N,k,h){return F(bin(N-k,N/2-h),bin(N,N/2));}
function common(xs){const values=xs.map(q),den=values.reduce((d,x)=>d/gcd(d,x[1])*x[1],1n);return {den,values:values.map(x=>x[0]*(den/x[1]))};}
function LDL(M,record){check(record.status==="EXACT_PSD_MOMENT_MATRIX"&&record.matrix_dimension===M&&record.negative===null,"PSD proof kind/dimension");const c=record.ldl;
  check(c&&c.lower.length===M&&c.lower.every(row=>row.length===M)&&c.diagonal.length===M,"complete exact sign-matrix LDL");
  const l=common(c.lower.flat()),d=common(c.diagonal),L=Array.from({length:M},(_,i)=>l.values.slice(i*M,(i+1)*M));
  check(d.values.every(x=>x>=0n)&&L.every((row,i)=>row[i]===l.den&&row.slice(i+1).every(x=>x===0n)),"unit lower factor and nonnegative singular-aware diagonal");
  const D=l.den*l.den*d.den,Q=BigInt(M-1);
  for(let i=0;i<M;i++)for(let j=0;j<M;j++){let value=0n;for(let k=0;k<=Math.min(i,j);k++)value+=L[i][k]*d.values[k]*L[j][k];check(value*Q===(i===j?Q:-1n)*D,"EVERY exact original sign-matrix factor entry");}
}
check(crypto.createHash("sha256").update(derivation).digest("hex")===report.derivation_sha256,"derivation hash-pinned");
check(report.candidate_record_accepted===false&&report.novelty_claim===false&&report.source_population_gap_proved===false&&report.quantum_speedup_proved===false,"controls cannot become algorithm/source claims");
same(report.odd_sizes,[5,7,15,31,63],"explicit odd control schedule");same(report.even_sizes,[4,6,16,32,64],"explicit honest even schedule");
same(report.cases.map(c=>c.M),[...report.odd_sizes,...report.even_sizes],"all controls, no favorable omission");
let classRecords=0,projectiveIdentities=0,normalizations=0,LDLControls=0,oddGaps=0,evenGlobalLaws=0,indicatorEntries=0;
for(const c of report.cases){const M=c.M,Q=BigInt(M-1),odd=M%2===1,max=odd?M-1:M;
  check(Number.isSafeInteger(M)&&M>=4&&c.maximum_marginal_size===max,"strict odd-proper/even-global scope");
  check(c.status===(odd?"EXACT_ODD_PROPER_MARGINAL_PSD_GLOBAL_GAP":"EXACT_EVEN_HONEST_GLOBAL_CONTROL")&&c.is_source_instance===false&&c.is_algorithm_candidate===false&&c.quantum_speedup_proved===false&&c.population_obstruction_proved===false&&c.global_nonrealizability_proved===odd,"mathematical type/claim gates");
  check(c.compressed_probability_semantics==="PER_WORD_AND_MULTIPLICITY_WEIGHTED_CLASS_MASS_DISTINCT","word probabilities and class masses are different types");
  const parts=odd?[[M-1,F(BigInt(M-2),2n*Q)],[M+1,F(BigInt(M),2n*Q)]]:[[M,F(1n)]];
  check(c.components.length===parts.length,"complete balanced mixture");
  parts.forEach(([N,w],i)=>{const p=c.components[i];check(p.population_size===N&&N%2===0&&eq(q(p.mixture_weight),w)&&p.balanced_word_count===String(bin(N,N/2)),"exact genuine balanced populations and nonnegative mixture weights");});
  const probability=(k,h)=>parts.reduce((s,[N,w])=>add(s,mul(w,word(N,k,h))),F(0n));
  check(c.marginal_rows.length===max+1,"every proper/full size retained");let counts=0,projections=0,numBits=0,denBits=0;
  c.marginal_rows.forEach((row,k)=>{
    check(row.k===k&&Number.isSafeInteger(row.k)&&row.classes.length===k+1,"complete ordered k/h schedule");let total=F(0n);
    row.classes.forEach((a,h)=>{const p=q(a.particular_word_probability),mass=q(a.Hamming_class_mass),multiplicity=bin(k,h);
      check(a.h===h&&Number.isSafeInteger(a.h)&&a.word_multiplicity===String(multiplicity)&&p[0]>=0n&&eq(p,probability(k,h))&&eq(mass,mul(F(multiplicity),p)),"EVERY exact binomial native word probability/class mass");total=add(total,mass);
      if(k<max){const next=c.marginal_rows[k+1].classes;check(eq(p,add(q(next[h].particular_word_probability),q(next[h+1].particular_word_probability))),"EVERY projective marginal identity");projections++;}
      numBits=Math.max(numBits,bits(p[0]));denBits=Math.max(denBits,bits(p[1]));counts++;
    });check(eq(total,F(1n))&&eq(q(row.exact_normalization),F(1n)),"entire normalized positive marginal law");normalizations++;
  });
  check(eq(q(c.sign_mean),F(0n))&&eq(q(c.off_diagonal_sign_correlation),F(-1n,Q)),"native mean/pair moments");
  const p1=c.marginal_rows[1].classes,p2=c.marginal_rows[2].classes;
  check(eq(q(p1[0].particular_word_probability),F(1n,2n))&&eq(q(p1[1].particular_word_probability),F(1n,2n)),"unbiased single native events");
  check(eq(add(add(q(p2[0].particular_word_probability),q(p2[2].particular_word_probability)),mul(F(-2n),q(p2[1].particular_word_probability))),F(-1n,Q)),"proper pair marginals give stated sign correlation");
  const t=c.PSD_sum_of_squares_template;check(eq(q(t.sign_diagonal),F(1n))&&eq(q(t.sign_off_diagonal),F(-1n,Q))&&eq(q(t.edge_square_weight),F(1n,Q))&&t.edge_square_count===M*(M-1)/2,"positive all-edge square template");
  check(eq(q(t.constant_moment),F(1n))&&eq(q(t.constant_sign_means),F(0n))&&eq(q(t.indicator_constant_coefficient),F(1n,2n)),"constant/sign PSD extension and indicator mean");
  same(t.indicator_sign_coefficients,["-1/2","1/2"],"actual binary one-hot congruence");
  const signs=t.indicator_sign_coefficients.map(q),samePair=F(BigInt(M-2),4n*Q),oppositePair=F(BigInt(M),4n*Q);
  check(eq(q(t.cross_block_same_indicator_probability),samePair)&&eq(q(t.cross_block_opposite_indicator_probability),oppositePair)&&eq(q(t.same_block_indicator_diagonal),F(1n,2n))&&eq(q(t.same_block_distinct_indicator_product),F(0n)),"complete native one-hot pair table");
  for(let i=0;i<M;i++)for(let j=0;j<M;j++)for(let s=0;s<2;s++)for(let u=0;u<2;u++){
    const R=i===j?F(1n):F(-1n,Q),v=add(F(1n,4n),mul(mul(signs[s],signs[u]),R)),expected=i===j?(s===u?F(1n,2n):F(0n)):(s===u?samePair:oppositePair);check(eq(v,expected),"EVERY original native indicator congruence entry");indicatorEntries++;
  }
  LDL(M,c.exact_sign_LDL_control);LDLControls++;
  const g=c.global_record;
  if(odd){check(g.status==="EXACT_GLOBAL_NATIVE_NONREALIZABILITY"&&g.is_global_probability_distribution===false&&g.all_proper_marginals_projectively_consistent===true,"odd proper laws not falsely globalized");
    const p=g.parity_certificate,K=(BigInt(M)*BigInt(M)-1n)/8n,A=-Q/2n;check(p.integer_constant===String(K)&&p.single_indicator_coefficient===String(A)&&p.pair_indicator_coefficient==="1"&&p.all_native_hamming_weight_values.length===M+1,"complete primitive odd-native parity cut");
    for(let h=0;h<=M;h++){const H=BigInt(h),value=K+A*H+H*(H-1n)/2n,spin=2n*H-BigInt(M);check(value>=0n&&8n*value===spin*spin-1n&&p.all_native_hamming_weight_values[h]===String(value),"EVERY odd native Hamming weight satisfies integrality inequality");}
    const value=add(add(F(K),mul(F(A*BigInt(M)),F(1n,2n))),mul(F(BigInt(M*(M-1)/2)),q(p2[2].particular_word_probability)));
    check(eq(value,F(-1n,8n))&&eq(q(p.exact_pair_moment_value),value)&&p.minimum_native_total_spin_squared==="1"&&p.exact_moment_total_spin_squared==="0"&&p.proves_no_global_native_distribution===true&&p.source_hardness_or_quantum_lower_bound_proved===false,"strict global-native gap, not hardness");oddGaps++;
  }else{
    check(g.status==="EXACT_HONEST_GLOBAL_BALANCED_DISTRIBUTION"&&g.balanced_positive_count===M/2&&g.number_of_global_support_words===String(bin(M,M/2))&&eq(q(g.particular_support_word_probability),F(1n,bin(M,M/2)))&&g.is_global_probability_distribution===true&&g.odd_parity_inequality_applicable===false&&g.balanced_word_countervalue_for_invalid_odd_inequality==="-1/8","genuine even global law excludes transplanting odd inequality");
    const full=c.marginal_rows[M].classes;check(full.every(a=>eq(q(a.Hamming_class_mass),F(a.h===M/2?1n:0n))),"honest global balance support, not hidden proper-only promise");evenGlobalLaws++;
  }
  const cost=c.cost;check(cost.class_records_preflight===counts&&cost.class_records_checked===counts&&counts<=cost.class_record_budget&&cost.sign_matrix_cells_preflight===M*M&&M*M<=cost.sign_matrix_cell_budget&&cost.normalizations_checked===max+1&&cost.projective_identities_checked===projections&&cost.maximum_probability_numerator_bits===numBits&&cost.maximum_probability_denominator_bits===denBits&&cost.native_words_enumerated===0&&cost.LP_calls===0&&cost.edge_squares_checked===M*(M-1)/2&&cost.indicator_pair_entries_checked===4*M*M&&cost.constant_indicator_entries_checked===2*M+1,"whole compressed cost/bit ledger");classRecords+=counts;projectiveIdentities+=projections;
}
console.log(JSON.stringify({status:"independent_native_proper_marginal_PSD_and_parity_controls_passed",oddGaps,evenGlobalLaws,classRecords,projectiveIdentities,normalizations,LDLControls,indicatorEntries,nativeWordsEnumerated:0,quantumSpeedupProved:false,sourceHardnessProved:false}));
