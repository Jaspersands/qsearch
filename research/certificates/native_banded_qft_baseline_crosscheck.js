"use strict";
// Independent rational root enclosures and Gaussian-integer marginal replay.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js");
const {check, rat, parse, str, add, sub, mul, div, cmp, zero, one} = E;
const ROOT = path.resolve(__dirname, "../..");
const REPORT = path.join(ROOT, "research/classical_baselines/native_banded_qft_baseline.json");
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const same = (a, b, msg) => check(JSON.stringify(a) === JSON.stringify(b), msg);
const abs = a => [a[0] < 0n ? -a[0] : a[0], a[1]];
const neg = a => [-a[0], a[1]];
const max = (a, b) => cmp(a, b) >= 0n ? a : b;
const gadd = (a,b) => [a[0]+b[0], a[1]+b[1]];
const gmul = (a,b) => [a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]];
const gconj = a => [a[0], -a[1]];
const mod = (x,q) => (x%q+q)%q;
const ceilLog2 = x => { check(x > 0n, "positive logarithm"); return (x-1n).toString(2).length - (x === 1n ? 1 : 0); };
function turnMod(t) { return rat(mod(t[0],t[1]),t[1]); }

function* tuples(alphabets, j=0, prefix=[]) {
  if (j === alphabets.length) { yield prefix; return; }
  for (const x of alphabets[j]) yield* tuples(alphabets,j+1,[...prefix,x]);
}

const piCache = new Map(), rootCache = new Map();
function floorDiv(a,b) {return a>=0n ? a/b : -((-a+b-1n)/b);}
const ceilDiv=(a,b)=>-floorDiv(-a,b);
function piInterval(N) {
  if (piCache.has(N)) return piCache.get(N);
  function atan(k) {
    let p=rat(1n,BigInt(k)), sum=zero; const x2=rat(1n,BigInt(k*k));
    for(let j=0;j<N;j++) {sum=add(sum,div(j%2 ? neg(p):p,rat(BigInt(2*j+1))));p=mul(p,x2);}
    const end=add(sum,div(N%2 ? neg(p):p,rat(BigInt(2*N+1))));
    return cmp(sum,end)<0n ? [sum,end]:[end,sum];
  }
  const a=atan(5),b=atan(239);
  const v=[sub(mul(rat(16n),a[0]),mul(rat(4n),b[1])),sub(mul(rat(16n),a[1]),mul(rat(4n),b[0]))];
  piCache.set(N,v);return v;
}

function rootInterval(turn, P) {
  const id=str(turn)+":"+P;
  if(rootCache.has(id)) return rootCache.get(id);
  const N=Math.ceil(P/4)+16;
  check(N<=512,"independent root-check precision cap, not acceptance");
  // Directed fixed-point interval arithmetic keeps all Taylor intermediates
  // short. Every discarded low bit is rounded OUTWARD, not silently omitted.
  const exactPi=piInterval(N), grid=2n**BigInt(P+32);
  const pi=[floorDiv(exactPi[0][0]*grid,exactPi[0][1]),ceilDiv(exactPi[1][0]*grid,exactPi[1][1])];
  const t=cmp(turn,rat(1n,2n))>0n ? sub(turn,one):turn;
  const products=pi.map(p=>2n*t[0]*p);
  const x=[floorDiv(products[0]<products[1]?products[0]:products[1],t[1]),
    ceilDiv(products[0]>products[1]?products[0]:products[1],t[1])];
  const times=(a,b)=>{
    const p=[a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]];
    return [floorDiv(p.reduce((a,b)=>a<b?a:b),grid),ceilDiv(p.reduce((a,b)=>a>b?a:b),grid)];
  };
  const negative=a=>[-a[1],-a[0]];
  const divided=(a,d)=>[floorDiv(a[0],d),ceilDiv(a[1],d)];
  const plus=(a,b)=>[a[0]+b[0],a[1]+b[1]];
  const x2=times(x,x);let c=[grid,grid],s=x,ct=[grid,grid],st=x;
  for(let j=1;j<N;j++) {
    ct=divided(negative(times(ct,x2)),BigInt((2*j-1)*(2*j)));c=plus(c,ct);
    st=divided(negative(times(st,x2)),BigInt((2*j)*(2*j+1)));s=plus(s,st);
  }
  // |argument|<=pi<4, and real sine/cosine derivatives have magnitude<=1.
  let factorial=1n;for(let j=2;j<=2*N;j++)factorial*=BigInt(j);
  const ec=ceilDiv(4n**BigInt(2*N)*grid,factorial);
  const es=ceilDiv(4n**BigInt(2*N+1)*grid,factorial*BigInt(2*N+1));
  const out=[[rat(c[0]-ec,grid),rat(c[1]+ec,grid)],[rat(s[0]-es,grid),rat(s[1]+es,grid)]];
  rootCache.set(id,out);return out;
}

function verifyModel(C) {
  const R=C.model,q=BigInt(R.modulus_q),ph=R.public_digit_phase_tables.map(row=>row.map(BigInt)),M=ph.length;
  check(String(q)===R.modulus_q,"exact canonical modulus string");
  const b=R.twiddle_bandwidth_b, sign=R.second_call_sign, L=R.accuracy_ledger;
  check(M>=1&&b>=1&&b<=M&&[-1,1].includes(sign),"public schedule parameters");
  ph.forEach(row=>check(row.length===3&&row.every(x=>x>=0n&&x<q),"canonical phase table"));
  same(ph.map(row=>row.map(String)),R.public_digit_phase_tables,"exact canonical phase strings");
  const f=L.failure_bits,P=f+ceilLog2(32n*BigInt(M)*3n**BigInt(M)),K=f+ceilLog2(4n*BigInt(M));
  check(L.word_sites_M===M&&L.phase_grid_bits_P===P&&L.random_bits_per_digit_K===K,"linear precision and random bits");
  const eps=rat(4n,2n**BigInt(P)), ne=mul(rat(2n*3n**BigInt(M)*BigInt(M)),eps);
  const phase=mul(rat(2n),ne), grid=rat(2n*BigInt(M),2n**BigInt(K)), total=add(phase,grid);
  same([L.root_complex_error_upper,L.unnormalized_state_2norm_error_upper,
    L.normalized_phase_approximation_TV_upper,L.finite_uniform_grid_TV_upper,L.per_complete_sample_TV_upper],
    [eps,ne,phase,grid,total].map(str),"global accuracy ledger");
  check(cmp(total,rat(1n,2n**BigInt(f)))<=0n&&cmp(mul(rat(BigInt(M)),eps),rat(1n,2n))<=0n,"nonvacuous phase perturbation");
  check(L.ideal_independent_uniform_bits_required===true&&L.rare_prefix_conditional_precision_assumed===false&&
    L.numerical_or_work_cap_is_hardness_evidence===false,"accuracy premises");
  const roots=new Map(),scale=2n**BigInt(P);
  for(const receipt of R.phase_grid) {
    const turn=parse(receipt.turn), nums=receipt.integer_value.map(BigInt);
    check(nums.length===2&&receipt.integer_value.every((x,i)=>String(nums[i])===x),"canonical Gaussian integers");
    check(cmp(turn,zero)>=0n&&cmp(turn,one)<0n&&!roots.has(str(turn)),"canonical unique phase root");
    const intervals=rootInterval(turn,P);
    let err=zero;
    intervals.forEach((v,i)=>{
      const chosen=rat(nums[i],scale);
      err=add(err,max(abs(sub(v[0],chosen)),abs(sub(v[1],chosen))));
    });
    check(cmp(err,eps)<=0n,"independent Machin/Taylor phase error certificate");
    check(cmp(parse(receipt.Arb_complex_l1_error_upper),eps)<=0n&&receipt.enclosure_bits<=R.resource_policy.max_enclosure_bits,
      "declared root enclosure budget");
    roots.set(str(turn),nums);
  }
  const denom=3n**BigInt(b), local=new Map(), masses=new Map();
  const requiredRoots=new Set();
  for(let k=0;k<M;k++)for(let w=0;w<3;w++)for(let t=0;t<3;t++)for(let r=0n;r<denom;r++)
    requiredRoots.add(str(turnMod(add(rat(ph[k][w]+BigInt(sign)*ph[M-1-k][t],q),rat(r,denom)))));
  same([...roots.keys()].sort(),[...requiredRoots].sort(),"all roots prepared before outcome randomness");
  function factor(k,w,x) {
    const id=JSON.stringify([k,w,x]);if(local.has(id))return local.get(id);
    let shift=0n;
    w.forEach((a,j)=>{shift+=BigInt(a-x[j])*3n**BigInt(b-1-j);});
    let out=[0n,0n];
    for(let t=0;t<3;t++) {
      const key=str(turnMod(add(rat(ph[k][w[0]]+BigInt(sign)*ph[M-1-k][t],q),rat(BigInt(t)*shift,denom))));
      check(roots.has(key),"required public root supplied");out=gadd(out,roots.get(key));
    }
    local.set(id,out);return out;
  }
  function mass(prefix) {
    const id=JSON.stringify(prefix);if(masses.has(id))return masses.get(id);
    const alphabets=Array.from({length:M},(_,j)=>{
      const out=[];for(let w=0;w<3;w++)for(let wp=0;wp<3;wp++)
        for(const x of (j<prefix.length?[prefix[j]]:[0,1,2]))out.push([w,wp,x]);return out;
    });
    let states=new Map();for(const s of tuples(alphabets.slice(0,b-1)))states.set(JSON.stringify(s),[1n,0n]);
    for(let k=0;k<M;k++) {
      const next=new Map(),prevLen=Math.min(b-1,M-k);
      for(const win of tuples(alphabets.slice(k,k+b))) {
        const w=win.map(x=>x[0]),wp=win.map(x=>x[1]),x=win.map(x=>x[2]);
        const term=gmul(states.get(JSON.stringify(win.slice(0,prevLen))),gmul(factor(k,w,x),gconj(factor(k,wp,x))));
        const key=JSON.stringify(win.slice(1));next.set(key,gadd(next.get(key)||[0n,0n],term));
      }states=next;
    }
    const result=states.get("[]");check(result[1]===0n&&result[0]>=0n,"real positive joint prefix mass");
    masses.set(id,result[0]);return result[0];
  }
  const z=mass([]);check(z>0n,"normalization of approximate state");
  const calibration=C.small_calibration_only_all_outcome_probabilities;
  if(M<=3) {
    const probs=[];for(const x of tuples(Array.from({length:M},()=>[0,1,2])))probs.push(str(rat(mass(x),z)));
    same(calibration,probs,"all small calibration masses");
    check(cmp(probs.map(parse).reduce(add,zero),one)===0n,"complete calibration normalization");
  } else check(calibration.length===0,"growing control not densely enumerated");
  for(const sample of C.sampling.samples) {
    const digits=sample.site_digits_MSB_first;
    check(digits.length===M&&digits.every(d=>[0,1,2].includes(d)),"sample shape");
    if(M<=3) {
      check(sample.trace.length===M,"complete finite trace");
      let prefix=[];
      sample.trace.forEach((step,k)=>{
        same(step.prefix,prefix,"sample prefix");
        const weights=[0,1,2].map(d=>mass([...prefix,d]));
        same(step.child_weights,weights.map(String),"exact branch masses");
        const parent=mass(prefix);check(weights.reduce((a,b)=>a+b,0n)===parent&&parent>0n,"CDF parent");
        const u=BigInt(step.uniform_grid_integer);check(u>=0n&&u<2n**BigInt(K),"K-bit draw");
        let cumulative=0n,d=0;
        for(;d<3;d++){cumulative+=weights[d];if(u*parent<cumulative*2n**BigInt(K))break;}
        check(step.selected_digit===d&&digits[k]===d,"exact discrete inverse CDF");prefix.push(d);
      });
    } else {
      check(sample.trace.length===0,"compact growing trace");
      check(mass(digits)>0n,"growing sampled outcome has nonzero mass");
    }
  }
  const count=C.sampling.samples.length;
  same(C.sampling.joint_batch_TV_upper_under_IID_bits,str(cmp(mul(rat(BigInt(count)),total),one)>0n?one:mul(rat(BigInt(count)),total)),"batch loss");
  const work=R.observed_work;
  check(work.dense_word_rows_allocated===0&&work.all_outcomes_enumerated_by_sampler===false&&work.hidden_truth_used===false,
    "no dense solver or private truth");
  check(work.root_enclosures_computed===roots.size&&work.peak_boundary_states===27**(b-1)&&
    work.random_bits_consumed===count*M*K,"observed resource counts");
  check(R.intermediate_integer_bits_upper===M*(2*P+8)+2&&
    work.maximum_integer_bits_seen>=z.toString(2).length&&
    work.maximum_integer_bits_seen<=R.intermediate_integer_bits_upper,"charged integer precision bounds");
  check(R.local_factor_cache_entries_upper===M*9**b&&
    R.local_factor_cache_entries<=R.local_factor_cache_entries_upper,"factor cache is not free boundary memory");
  const producerPrefixes=new Map();
  function remember(prefix) {producerPrefixes.set(JSON.stringify(prefix),prefix);}
  remember([]);
  for(const sample of C.sampling.samples) {
    let prefix=[];
    for(const digit of sample.site_digits_MSB_first) {
      [0,1,2].forEach(d=>remember([...prefix,d]));prefix.push(digit);
    }
  }
  if(M<=3)for(const x of tuples(Array.from({length:M},()=>[0,1,2])))remember(x);
  let actualWindows=0;
  for(const prefix of producerPrefixes.values())for(let k=0;k<M;k++) {
    let windows=1;for(let j=k;j<Math.min(M,k+b);j++)windows*=j<prefix.length?9:27;
    actualWindows+=windows;
  }
  check(work.prefix_contractions===producerPrefixes.size&&R.cached_prefix_weights===producerPrefixes.size&&
    work.window_evaluations===actualWindows,"reconstructed actual marginal work, not a hypothetical count");
  check(R.max_prefix_boundary_states_upper===27**(b-1)&&R.prefix_window_evaluations_upper===M*27**b&&
    R.complete_sample_window_evaluations_upper===(3*M+1)*M*27**b,"structural bounds");
  check(work.window_evaluations<=R.resource_policy.max_total_window_evaluations&&
    R.exact_integer_arithmetic_bit_cost_is_not_unit_cost===true&&R.general_quantum_lower_bound_claimed===false&&
    R.hidden_secret_recovery_algorithm_supplied===false&&C.private_truth_or_errors_supplied_to_baseline===false,"cost and scope");
  // Reconstruct all required root arguments independently from public observations.
  const raw=C.original_records,mask=C.public_mask;
  check(raw.length===2*M,"original paired observations");
  check(new Set(raw.map(r=>r.source_id)).size===raw.length&&raw.every(r=>BigInt(r.modulus)===q),"same original bank, not fabricated repeats");
  const digitPairs=[[1,0],[-1,1],[0,-1]];
  const reconstructed=Array.from({length:M},(_,j)=>digitPairs.map(([a,b])=>{
    const r0=raw[2*j],r1=raw[2*j+1];
    let value=BigInt(a*r0.value+b*r1.value);
    mask.forEach((c,i)=>{value+=BigInt(a*r0.label[i]+b*r1.label[i])*BigInt(c);});
    return String(mod(value,q));
  }));
  same(R.public_digit_phase_tables,reconstructed,"same-public-data phase access");
  return {sites:M,bandwidth:b,independent_phase_roots:roots.size};
}

function verify(R) {
  check(R.status==="CERTIFIED_DENSE_FREE_TWO_CALL_BANDED_QFT_CLASSICAL_BASELINE","report status");
  check(R.producer_sha256===hash(path.join(ROOT,"theorems/native_banded_qft_baseline.py"))&&
    R.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_BANDED_QFT_BASELINE.md"))&&
    R.contract_sha256===hash(path.join(ROOT,"research/hypotheses/native_banded_qft_baseline_contract.json")),"current provenance");
  const deps=["native_response_fourier_factorization_audit.py","native_basis_lottery.py","native_full_root_slice.py","ternary_noise_degradation.py"];
  same(Object.keys(R.dependency_sha256).sort(),deps.sort(),"dependencies");
  deps.forEach(f=>check(R.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(R.controls.length===7,"finite and growing controls");
  const controls=R.controls.map(verifyModel);
  check(R.full_cyclic_approximation_profiles.length===5,"full cyclic accuracy profiles");
  for(const L of R.full_cyclic_approximation_profiles){
    const M=L.word_sites_M,f=L.failure_bits,target=64n*BigInt(M)*2n**BigInt(f);
    let b=1,p=3n;while(b<M&&p<target){b++;p*=3n;}
    let omitted=zero;for(let d=b;d<M;d++)omitted=add(omitted,rat(BigInt(M-d),3n**BigInt(d+1)));
    const single=mul(rat(176n,7n),omitted),joint=mul(rat(2n),single);
    const P=f+1+ceilLog2(32n*BigInt(M)*3n**BigInt(M)),K=f+1+ceilLog2(4n*BigInt(M));
    const arithmetic=add(rat(16n*BigInt(M)*3n**BigInt(M),2n**BigInt(P)),rat(2n*BigInt(M),2n**BigInt(K)));
    check(L.selected_bandwidth_b===b&&L.integer_cutoff_threshold_64_M_times2_pow_f===String(target)&&
      L.forward_and_adjoint_QFTs_charged===2,"qutrit truncation cutoff and two transforms");
    same([L.exact_omitted_weight_sum,L.single_QFT_operator_norm_error_upper,L.joint_Born_TV_truncation_upper,
      L.classical_phase_and_grid_TV_upper,L.complete_full_cyclic_sample_TV_upper],
      [omitted,single,joint,arithmetic,add(joint,arithmetic)].map(str),"qutrit CP telescoping and combined TV");
    check(cmp(add(joint,arithmetic),rat(1n,2n**BigInt(f)))<=0n&&L.exact_untruncated_sampler_supplied===false&&
      L.inverse_polynomial_accuracy_gives_logarithmic_bandwidth===true&&
      L.small_work_caps_disprove_this_constructive_bound===false,"approximate not exact and no cap falsification");
  }
  check(R.accepted_speedup_candidate===false&&R.new_active_negative_result_created===false&&
    R.exact_full_bandwidth_polynomial_sampler_claimed===false&&
    R.full_cyclic_inverse_polynomial_accuracy_structural_sampler_bound===true&&
    R.three_or_more_calls_covered===false,"approximate two-call scope, no exact or many-call claims");
  return {verified:true,controls,independent_transcendental_phase_certificates:true,accepted_speedup_candidate:false};
}
module.exports={verify,verifyModel,rootInterval};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(REPORT,"utf8"))),null,2));
