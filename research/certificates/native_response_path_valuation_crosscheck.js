"use strict";
// Independent multinomial census and full weighted Born-law replay.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js");
const {check, rat, str, add, zero, one} = E;
const ROOT = path.resolve(__dirname, "../..");
const REPORT = path.join(ROOT, "research/reductions/native_response_path_valuation.json");
const canonical = x => Array.isArray(x) ? x.map(canonical) : x && typeof x === "object" ? Object.fromEntries(Object.keys(x).sort().map(k => [k, canonical(x[k])])) : x;
const same = (a, b, msg) => E.same(canonical(a), canonical(b), msg);
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const mod = (x, q) => (x % q + q) % q;
const digits = [[1, 0], [-1, 1], [0, -1]];
const jsonInt = x => x >= -9007199254740991n && x <= 9007199254740991n ? Number(x) : String(x);
function tuples(q, n) {
  if (!n) return [[]];
  return Array.from({length:q}, (_, i) => tuples(q,n-1).map(t => [i,...t])).flat();
}
function factorial(k) { let x=1n; for(let i=2;i<=k;i++)x*=BigInt(i); return x; }
function gcd(a,b) { a=a<0n?-a:a; b=b<0n?-b:b; while(b)[a,b]=[b,a%b]; return a; }

function collisionProfile(n,d,M,k) {
  [n,d,M,k].forEach(x=>check(Number.isSafeInteger(x)&&x>0,"positive census dimensions"));
  check(d<=32 && n*d<=1024 && k<=32 && 2*k*M<=4096,"exact ledger cap");
  // Producer uses forward convolution. Replay uses occupancy multinomials.
  const sums=[], fac=factorial(k);
  for(let a=0;a<=k;a++)for(let b=0;b<=k-a;b++) {
    const c=k-a-b;
    sums.push([a-b,b-c,fac/(factorial(a)*factorial(b)*factorial(c))]);
  }
  const q=3n**BigInt(d), local=Array(d+1).fill(0n);
  let integerZero=0n;
  for(const [x,y,a] of sums)for(const [u,v,b] of sums) {
    let g=gcd(gcd(q,BigInt(x-u)),BigInt(y-v)), h=0;
    while(g>1n){g/=3n;h++;}
    local[h]+=a*b;
    if(x===u&&y===v)integerZero+=a*b;
  }
  const totalLocal=3n**BigInt(2*k), total=totalLocal**BigInt(M);
  const survival=local.map((_,h)=>local.slice(h).reduce((a,b)=>a+b,0n));
  let mean=zero;
  const strata=local.map((c,h)=>{
    const count=survival[h]**BigInt(M)-(h<d?survival[h+1]**BigInt(M):0n);
    const p=rat(1n,3n**BigInt((d-h)*n)), contribution=E.mul(rat(count,total),p);
    mean=add(mean,contribution);
    return {valuation:h,local_count:jsonInt(c),all_sites_path_pair_count:jsonInt(count),
      IID_label_collision_probability:str(p),collision_density_contribution:str(contribution)};
  });
  return {dimension:n,root_digits:d,modulus:jsonInt(q),word_sites:M,positive_response_calls:k,
    compressed_integer_sum_count:sums.length,local_ordered_path_pairs:jsonInt(totalLocal),
    total_ordered_path_pairs:jsonInt(total),local_zero_over_integers_count:jsonInt(integerZero),
    ideal_strata:strata,exact_IID_expected_collision_density:str(mean),
    nonzero_coefficients_assumed_units:false,local_nonzero_modq_nonunit_count:jsonInt(local.slice(1,d).reduce((a,b)=>a+b,0n)),
    collision_density_is_arbitrary_mixer_acceptance:false,
    IID_uniform_original_labels_required:true,quantum_query_lower_bound_supplied:false};
}

function poly(coefficients,q) {
  const K=E.field(q); let a=K.F();
  coefficients.forEach((c,i)=>a=K.plus(a,K.scale(K.powers[i],c)));
  return K.encode(a);
}
function probability(hist,root,denom) {
  const c=Array.from({length:root},()=>zero);
  for(const [a,x] of hist)for(const [b,y] of hist) {
    const idx=mod(a-b,root); c[idx]=add(c[idx],rat(BigInt(x*y),BigInt(denom)));
  }
  return c;
}
function bump(hist,key){hist.set(key,(hist.get(key)||0)+1);}
function complexReadout(rows,q,D) {
  const phases=rows.map(r=>2*Math.PI*r.known_phase/q);
  return Array.from({length:D},(_,x)=>{
    let re=0,im=0;
    for(let w=0;w<D;w++)for(let v=0;v<D;v++) {
      const angle=phases[w]+phases[v]+2*Math.PI*v*(w-x)/D;
      re+=Math.cos(angle);im+=Math.sin(angle);
    }
    return (re*re+im*im)/(D**3);
  });
}
function normalizedReadout(readout,root) {
  const K=E.field(root);let total=K.F();
  for(const p of readout) {
    const a=K.decode(p);check(K.eq(a,K.conj(a)),"real probability");
    check(E.sign(K,a)>=0,"nonnegative exact probability");
    total=K.plus(total,a);
  }
  check(K.eq(total,K.unit),"all-outcome Born normalization");
}
function checkControl(C) {
  const A=C.actual_public_data_readout, raw=C.original_records;
  const q=A.modulus,n=raw[0].label.length,M=raw.length/2,D=3**M,root=Math.max(q,D);
  check(Number.isInteger(M)&&M>0&&D<=9&&q<=27&&q**n<=27,"complete measured control cap");
  const mask=A.public_mask,ids=new Set();
  check(mask.length===n,"full public mask");
  raw.forEach(r=>{
    check(r.modulus===q&&r.label.length===n&&!ids.has(r.source_id)&&typeof r.source_id==="string","consistent original receipts");
    ids.add(r.source_id);
    [...r.label,r.value,...mask].forEach(x=>check(Number.isInteger(x)&&x>=0&&x<q,"canonical original values"));
  });
  const rows=tuples(3,M).map(word=>{
    const beta=word.flatMap(t=>digits[t]);
    const f=Array.from({length:n},(_,i)=>mod(beta.reduce((s,b,j)=>s+b*raw[j].label[i],0),q));
    const phase=mod(beta.reduce((s,b,j)=>s+b*raw[j].value,0)+f.reduce((s,a,i)=>s+a*mask[i],0),q);
    return {word,frequency:f,known_phase:phase};
  });
  same(A.actual_word_rows,rows,"actual public-data words");
  const readout=Array.from({length:D},(_,x)=>{
    const hist=new Map();
    rows.forEach((rw,w)=>rows.forEach((rv,v)=>bump(hist,mod((root/q)*(rw.known_phase+rv.known_phase)+(root/D)*v*(w-x),root))));
    return poly(probability(hist,root,D**3),root);
  });
  same(A.exact_all_outcome_probabilities,readout,"full two-call weighted Born law");
  normalizedReadout(readout,root);
  const numerical=complexReadout(rows,q,D);
  check(A.classical_same_data_FFT_probabilities.length===D,"complete FFT baseline");
  numerical.forEach((p,i)=>check(Number.isFinite(A.classical_same_data_FFT_probabilities[i])&&Math.abs(p-A.classical_same_data_FFT_probabilities[i])<1e-12,"numerical same-data baseline"));
  same({...A,classical_same_data_FFT_probabilities:[]},{modulus:q,word_dimension:D,root_order:root,
    public_mask:mask,actual_word_rows:rows,schedule:"F_D_DAGGER D_y F_D D_y |PLUS_D>",
    exact_all_outcome_probabilities:readout,classical_same_data_FFT_probabilities:[],public_response_phase_calls:2,
    classical_FFT_amplitudes_stored:D,classical_FFT_cost_is_polynomial_in_sites:false,
    hardware_circuit_compiled:false,unknown_phase_oracle_or_truth_used:false,normalized_fibre_oracle_used:false},"unitary access and charged classical scope");
  const errors=C.calibration_only.original_errors, secret=C.calibration_only.masked_secret;
  check(errors.length===raw.length&&secret.length===n,"calibration shape");
  const ephase=rows.map(r=>mod(r.word.reduce((s,t,j)=>s+digits[t][0]*errors[2*j]+digits[t][1]*errors[2*j+1],0),q));
  rows.forEach((r,w)=>check(mod(r.frequency.reduce((s,a,i)=>s+a*secret[i],0)+ephase[w],q)===r.known_phase,"calibration matches actual public response"));
  const secrets=tuples(q,n), mean=[],pinched=[];
  for(let x=0;x<D;x++) {
    let sweep=Array.from({length:root},()=>zero);
    for(const s of secrets) {
      const hist=new Map();
      rows.forEach((rw,w)=>rows.forEach((rv,v)=>{
        const phase=rw.frequency.reduce((a,t,i)=>a+(t+rv.frequency[i])*s[i],0)+ephase[w]+ephase[v];
        bump(hist,mod((root/q)*phase+(root/D)*v*(w-x),root));
      }));
      const p=probability(hist,root,D**3*secrets.length);sweep=sweep.map((a,i)=>add(a,p[i]));
    }
    const groups=new Map();
    rows.forEach((rw,w)=>rows.forEach((rv,v)=>{
      const key=rw.frequency.map((a,i)=>mod(a+rv.frequency[i],q)).join(",");
      if(!groups.has(key))groups.set(key,new Map());
      bump(groups.get(key),mod((root/q)*(ephase[w]+ephase[v])+(root/D)*v*(w-x),root));
    }));
    let p=Array.from({length:root},()=>zero);
    for(const hist of groups.values()) {const t=probability(hist,root,D**3);p=p.map((a,i)=>add(a,t[i]));}
    mean.push(poly(sweep,root));pinched.push(poly(p,root));
  }
  same(mean,pinched,"independent weighted pinching vs secret census");
  same(C.uniform_secret_mean_all_outcomes,mean,"complete secret mean readout");
  same(C.weighted_additive_pinching_all_outcomes,pinched,"weighted additive readout");
  normalizedReadout(mean,root);
  check(C.secret_population===secrets.length&&C.all_outcomes_retained===true&&C.weights_from_actual_unitary===true&&C.raw_collision_count_used_as_quantum_probability===false&&C.efficient_secret_decoder_supplied===false,"control scope");
}
function verify(R) {
  check(R.status==="HIGHER_RESPONSE_PATH_IDEALS_AND_WEIGHTED_UNITARY_READOUT_REVIEW_PENDING","review-pending status");
  [["producer_sha256","theorems/native_response_path_valuation.py"],["derivation_sha256","research/NATIVE_RESPONSE_PATH_VALUATION.md"],["contract_sha256","research/hypotheses/native_response_path_valuation_contract.json"]].forEach(([k,f])=>check(R[k]===hash(path.join(ROOT,f)),"provenance "+k));
  const deps=["native_basis_lottery.py","native_full_root_slice.py","native_word_span_decision.py","ternary_measured_lattice_decoder.py"];
  same(Object.keys(R.dependency_sha256).sort(),deps.sort(),"direct dependencies");
  deps.forEach(f=>check(R.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(R.IID_path_collision_profiles.length===11,"declared profile count");
  R.IID_path_collision_profiles.forEach(C=>same(C,collisionProfile(C.dimension,C.root_digits,C.word_sites,C.positive_response_calls),"multinomial ideal law"));
  same(R.false_unit_assumption_counterexample,{modulus:9,coefficient_difference:[3,0],actual_collision_probability:"1/3",false_uniform_prediction:"1/9",two_call_M1_exact_mean:"25/81",old_two_call_M1_prediction:"67/243"},"false-unit counterexample");
  check(R.weighted_unitary_interleaving_controls.length===3,"declared weighted controls");
  R.weighted_unitary_interleaving_controls.forEach(checkControl);
  ["accepted_speedup_candidate","new_active_negative_result_created","general_quantum_lower_bound","novelty_claim"].forEach(k=>check(R[k]===false,"honesty "+k));
  check(R.research_decision==="SEARCH_WEIGHTED_UNITARY_PATHS_NOT_UNWEIGHTED_COLLISION_COUNTS","research decision");
  return {verified:true,collision_profiles:11,weighted_unitary_controls:3,all_outcomes_retained:true,accepted_speedup_candidate:false};
}
module.exports={verify,collisionProfile,checkControl};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT,"utf8"))),null,2));
