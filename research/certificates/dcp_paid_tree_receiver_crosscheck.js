"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),S=require("./lattice_sine_window_source_crosscheck.js");
const {check,same,parse,rat,zero,one,add,div,mul,cmp}=E;
const ROOT=path.resolve(__dirname,"../.."),FILE=path.join(ROOT,"research/phase_workbench/dcp_paid_tree_receiver.json");
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
const pop=x=>x.toString(2).split("").filter(x=>x==="1").length;
const key=s=>JSON.stringify(s),normalize=s=>s.slice().sort((a,b)=>a[1]-b[1]);
const eq=(a,b)=>cmp(a,b)===0n;
function power(x,k){let v=one;while(k--)v=mul(v,x);return v;}

function confidenceCounterexample(c) {
  check(c.ell===3&&c.stage===2&&c.label===1&&c.correct_prefix===1&&c.true_stage_bit===0&&c.samples===35,"actual dyadic pi/4 stage");
  const v=parse(c.root_visibility),delta=parse(c.total_failure_budget),ell=rat(3n),m=35;
  const root=parse(c.sqrt_two_rational_lower),p=div(add(one,div(v,root)),rat(2n));
  check(cmp(mul(root,root),rat(2n))<0n&&cmp(root,one)>0n&&
    eq(p,parse(c.positive_spin_probability_upper))&&cmp(p,rat(1n,2n))>0n,"rigorous sqrt(2) and positive-spin enclosure");
  const j=Math.floor((m-1)/2);let choose=1n;
  for(let k=1;k<=j;k++)choose=choose*BigInt(m-j+k)/BigInt(k);
  const term=mul(rat(choose),mul(power(p,j),power(add(one,mul(rat(-1n),p)),m-j)));
  const allowed=div(delta,ell);
  check(eq(term,parse(c.single_binomial_error_term_lower))&&cmp(term,allowed)>0n&&
    c.strict_negative_score_positive_spin_count===j&&eq(allowed,parse(c.allowed_per_stage_error)),"one strictly negative score event already violates the budget");
  const x=div(mul(rat(BigInt(m)),mul(v,v)),rat(2n));let exp=one,t=one;
  for(let k=1;k<=16;k++){t=div(mul(t,x),rat(BigInt(k)));exp=add(exp,t);}
  check(eq(exp,parse(c.exp_m_v_squared_over_two_Taylor_lower))&&cmp(exp,div(mul(rat(2n),ell),delta))>0n,"old quota met by positive-term exponential certificate");
  let bits=0;while(cmp(rat(1n<<BigInt(bits)),div(ell,delta))<0n)bits++;
  const bound=div(rat(BigInt(8*bits)),mul(v,v)),quota=(bound[0]+bound[1]-1n)/bound[1];
  check(BigInt(c.corrected_sufficient_quota)===quota&&c.old_factor_two_quota_is_met===true&&
    c.actual_error_exceeds_claimed_per_stage_budget===true&&c.source_acquisition_or_prefix_learning_is_free===false,"corrected conservative confidence scope");
  check(eq(v,rat(4n,5n))&&c.positive_exponential_Taylor_degree===16&&c.within_inverse_log_bad_register_promise===true&&
    cmp(add(one,mul(rat(-1n),v)),div(one,ell))<=0n,"counterexample is inside the inverse-log noise promise");
}

function fixedForest(P,v) {
  const m=P.labels.length,N=P.modulus,whole=(1<<m)-1,hits=new Map();let assignments=0;
  for(let mask=1;mask<=whole;mask++) {
    const labels=P.labels.filter((_,i)=>mask&(1<<i));let count=0;
    for(let signs=0;signs<2**(labels.length-1);signs++) {
      assignments++;let sum=labels[0];
      for(let i=1;i<labels.length;i++)sum+=((signs>>(i-1))&1?1:-1)*labels[i];
      if((sum%N+N)%N===N/2)count++;
    }
    hits.set(mask,rat(BigInt(count),1n<<BigInt(labels.length-1)));
  }
  function* partitions(mask) {
    if(!mask){yield [];return;}
    const bit=mask&-mask;
    for(let subset=mask;subset;subset=(subset-1)&mask)if(subset&bit) {
      for(const rest of partitions(mask^subset))yield [subset,...rest];
    }
  }
  function score(blocks) {
    let none=one,value=zero;
    for(const mask of blocks.slice().sort((a,b)=>pop(a)-pop(b)||a-b)) {
      value=add(value,mul(mul(none,hits.get(mask)),power(v,pop(mask))));
      none=mul(none,add(one,mul(rat(-1n),hits.get(mask))));
    }
    return value;
  }
  let best=zero,tried=0;
  for(const blocks of partitions(whole)) {tried++;const x=score(blocks);if(cmp(x,best)>0n)best=x;}
  const B=P.fixed_forest_baseline;let mask=0;
  for(const block of B.best_partition_masks){check(block>0&&block<=whole&&(mask&block)===0,"valid fixed forest partition");mask|=block;}
  check(mask===whole&&eq(score(B.best_partition_masks),best)&&eq(parse(B.optimal_target_weighted_visibility),best)&&
    B.complete_set_partitions_evaluated===tried&&B.signed_assignments_evaluated===assignments&&
    B.postmeasurement_selection_among_all_fixed_tree_targets_included===true,"complete matched nonadaptive forest optimum");
  return best;
}

function plan(P) {
  const N=P.modulus,M=P.labels.length,v=parse(P.externally_assumed_root_visibility_lower),whole=(1<<M)-1;
  check(Number.isSafeInteger(N)&&N>=2&&N<=2**20&&(N&(N-1))===0&&M>0&&M<=8,"bounded public receiver input");
  check(cmp(v,zero)>=0n&&cmp(v,one)<=0n,"visibility model promise");
  const table=new Map();
  for(const row of P.Bellman_certificate) {
    const s=row.state;let mask=0;
    same(normalize(s),s,"canonical forest order");
    for(const [k,a] of s) {
      check(Number.isSafeInteger(a)&&a>0&&a<=whole&&(mask&a)===0&&Number.isSafeInteger(k)&&k>=0&&k<N,"disjoint canonical live forest");mask|=a;
    }
    check(mask===whole&&!table.has(key(s)),"complete root ancestry and unique subproblem");
    table.set(key(s),row);
  }
  function child(s,i,j,b) {
    return normalize(s.filter((_,k)=>k!==i&&k!==j).concat([[(s[i][0]+(b===0?1:-1)*s[j][0]+N)%N,s[i][1]|s[j][1]]]));
  }
  const root=normalize(P.labels.map((k,i)=>[k,1<<i])),reached=new Set();let actions=0;
  function verify(s) {
    const id=key(s);if(reached.has(id))return;
    reached.add(id);check(table.has(id),"every Bellman branch must be supplied");
    const row=table.get(id);let best=zero,selected=zero;
    for(const [k,a] of s)if(k===N/2) {
      const bias=power(v,pop(a));if(cmp(bias,best)>0n)best=bias;
    }
    if(row.action[0]==="stop") {
      if(row.action[1]!==null) {
        check(s.some(([k,a])=>a===row.action[1]&&k===N/2),"stopping output is an actual parity target");
        selected=power(v,pop(row.action[1]));
      }
    } else check(row.action[0]==="merge","legal stop/merge policy");
    for(let i=0;i<s.length;i++)for(let j=0;j<s.length;j++)if(i!==j) {
      actions++;
      const plus=child(s,i,j,0),minus=child(s,i,j,1);verify(plus);verify(minus);
      const candidate=div(add(parse(table.get(key(plus)).value),parse(table.get(key(minus)).value)),rat(2n));
      if(cmp(candidate,best)>0n)best=candidate;
      if(row.action[0]==="merge"&&row.action[1]===s[i][1]&&row.action[2]===s[j][1])selected=candidate;
    }
    check(eq(parse(row.value),best)&&eq(selected,best),"Bellman upper optimum AND achievable chosen action");
  }
  verify(root);
  check(reached.size===table.size&&table.size===P.states_visited&&actions===P.ordered_actions_evaluated,"paid complete policy search");
  const value=parse(table.get(key(root)).value);
  check(eq(value,parse(P.optimal_target_weighted_visibility))&&
    eq(div(add(one,value),rat(2n)),parse(P.parity_success_IF_model_and_fair_guess_on_failure)),"unconditional target-weighted visibility, not heralded success");
  check(P.algorithm_is_polynomial_in_log_modulus_and_root_count===false&&P.source_model_is_certified_by_label_table===false,"no inflated complexity/source claim");
  const fixed=fixedForest(P,v);
  check(eq(parse(P.public_feedback_gain_over_best_fixed_forest),add(value,mul(rat(-1n),fixed)))&&cmp(value,fixed)>=0n,"feedback gain against matched baseline");
  return {table,root,child};
}

const cmul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];
function near(a,b) {
  a.forEach((row,i)=>row.forEach((z,j)=>check(Math.abs(z[0]-b[i][j][0])<1e-7&&Math.abs(z[1]-b[i][j][1])<1e-7,"private physical channel replay")));
}
function physical(C) {
  const B=plan(C.public_plan),sampling=C.compiled_source_sampling_audit;
  same(sampling,C.physical_source_certificate.actual_sampling_audit,"one charged source batch, not a substituted state table");
  const shots=S.instrument(C.physical_source_certificate);
  const receipts=new Map(sampling.public_receipts.map(x=>[x.id,x]));
  const states=new Map(Object.entries(sampling.PRIVATE_AUDIT_ONLY_density_matrices));
  const original=sampling.public_receipts.map(x=>x.id),live=new Set(original),N=C.public_plan.modulus;
  same(sampling.public_receipts.map(x=>x.label),C.public_plan.labels,"only emitted public labels enter plan");
  const mask=ids=>ids.reduce((v,id)=>{check(original.includes(id),"real source ancestor");return v|(1<<original.indexOf(id));},0);
  let forest=B.root;
  for(const t of C.actual_execution.transcript) {
    const a=t.left,b=t.right,out=t.output;
    check(a.id!==b.id&&live.has(a.id)&&live.has(b.id)&&!receipts.has(out.id),"two live independent components, no reset");
    same(receipts.get(a.id),a,"bound left receipt");same(receipts.get(b.id),b,"bound right receipt");
    const A=states.get(a.id),D=states.get(b.id),branch=t.actual_branch;
    check(branch===0||branch===1,"one actual computational outcome");
    const block=A.map((row,i)=>row.map((x,j)=>cmul(x,D[i^branch][j^branch])));
    const mass=block[0][0][0]+block[1][1][0];
    check(Math.abs(mass-0.5)<1e-7,"balanced conditional-product branch law");
    const rho=block.map(row=>row.map(z=>z.map(x=>x/mass)));
    check(out.label===(a.label+(branch===0?b.label:-b.label)+N)%N&&out.modulus===N&&out.measured_cells.length===0&&
      out.merge_depth===Math.max(a.merge_depth,b.merge_depth)+1,"physical label/depth, not fictitious new state");
    same(out.original_source_receipts,a.original_source_receipts.concat(b.original_source_receipts),"paid complete leaf lineage");
    const ma=mask(a.original_source_receipts),mb=mask(b.original_source_receipts);
    const action=B.table.get(key(forest)).action;
    same(action,["merge",ma,mb],"executor follows precomputed public policy");
    const i=forest.findIndex(x=>x[1]===ma),j=forest.findIndex(x=>x[1]===mb);
    forest=B.child(forest,i,j,branch);
    live.delete(a.id);live.delete(b.id);live.add(out.id);receipts.set(out.id,out);states.set(out.id,rho);
  }
  const result=C.actual_execution,action=B.table.get(key(forest)).action;
  check(action[0]==="stop"&&result.roots_supplied_and_paid===shots&&result.source_preparations_charged===shots&&
    result.unknown_phase_registers_reprepared_or_cloned===false,"all roots paid, including aborts and unused registers");
  if(result.status==="NO_INFORMATIVE_TARGET_ABORT")check(action[1]===null&&result.parity_bit===null,"honest target failure");
  else {
    const out=result.terminal_public_receipt,rho=states.get(out.id);
    check(live.has(out.id)&&out.label===N/2&&mask(out.original_source_receipts)===action[1]&&
      result.output_original_leaves===out.original_source_receipts.length,"actual selected single target");
    same(receipts.get(out.id),out,"terminal receipt provenance");
    near(rho,result.PRIVATE_AUDIT_ONLY_terminal_density);
    check(result.terminal_measurement.axis==="X"&&result.terminal_measurement.id===out.id&&
      result.parity_bit===result.terminal_measurement.outcome&&[0,1].includes(result.parity_bit)&&result.full_shift_recovered===false,"one physical parity readout only");
  }
  check(C.only_one_parity_bit_targeted===true&&C.full_DCP_algorithm_claimed===false,"not full secret recovery");
  return shots;
}

function verify(R) {
  check(R.producer_sha256===hash(path.join(ROOT,"theorems/dcp_paid_tree_receiver.py"))&&
    R.derivation_sha256===hash(path.join(ROOT,"research/DCP_PAID_TREE_RECEIVER.md"))&&
    R.contract_sha256===hash(path.join(ROOT,"research/hypotheses/dcp_paid_tree_receiver_contract.json")),"current provenance");
  Object.entries(R.dependency_sha256).forEach(([p,h])=>check(hash(path.join(ROOT,"theorems",p))===h,"dependency provenance"));
  R.exact_finite_policy_controls.forEach(plan);
  const shots=R.actual_physical_source_controls.reduce((v,c)=>v+physical(c),0);
  check(shots===24&&shots===R.actual_source_preparations_charged,"actual input supply");
  for(const p of R.raw_label_acquisition_profiles) {
    check(eq(parse(p.stratum_probability),rat(1n<<BigInt(p.stage),1n<<BigInt(p.ell)))&&
      eq(parse(p.expected_original_preparations_without_sieve),rat(BigInt(p.useful_record_quota)*(1n<<BigInt(p.ell)),1n<<BigInt(p.stage)))&&
      p.sieved_acquisition_cost_is_supplied_by_this_bound===false,"raw acquisition is not a free sieve");
  }
  for(const p of R.feedback_template_raw_source_bounds) {
    const N=1n<<BigInt(p.ell),M=BigInt(p.original_roots),raw=rat(M*(M-1n)*(M-2n)*(N-4n),N**3n);
    const bound=cmp(raw,one)>0n?one:raw;
    check(eq(parse(p.probability_any_template_upper),bound)&&p.generated_or_sieved_labels_covered===false,"literal feedback template acquisition paid, no general no-go");
  }
  confidenceCounterexample(R.old_quadrature_confidence_claim_counterexample);
  check(R.finite_policy_optimum_is_general_quantum_optimum===false&&R.efficient_noisy_receiver_supplied===false&&
    R.accepted_speedup_candidate===false&&R.novelty_claim===false,"no broad no-go, solver or novelty promotion");
  check(R.exact_finite_policy_controls.length===5,"all finite policy controls");
  return {verified:true,exact_policy_controls:5,physical_source_controls:4,actual_preparations:shots,accepted_speedup_candidate:false};
}
module.exports={verify,plan,confidenceCounterexample};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||FILE,"utf8"))),null,2));
