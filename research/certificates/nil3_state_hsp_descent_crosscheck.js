"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {check,same}=require("./cyclotomic_exact.js");
const ROOT=path.resolve(__dirname,"../..");
const DERIVATION=path.join(ROOT,"research/NIL3_STATE_HSP_DESCENT.md");
const PRODUCER=path.join(ROOT,"theorems/nil3_state_hsp_descent_receiver.py");
const REPORT=path.join(ROOT,"research/reductions/nil3_state_hsp_descent_receiver.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const mod=(a,n)=>(a%n+n)%n;
function reduce(v){const b=mod(v[1],3),carry=(v[1]-b)/3;return [mod(v[0]-6*carry,9),b];}
const add=(a,b)=>reduce([a[0]+b[0],a[1]+b[1]]);
const mul=(a,b)=>reduce([a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]-a[1]*b[1]]);
const roots=[[1,0],[0,1],[-1,-1]],lambdas=[[0,0],[1,0],[1,1]];
const exponent=(a,s)=>{const v=mul(a,s);return mod(v[0]-2*v[1],9);};
const row=label=>label.map(a=>{const e=exponent(a,[6,0]);check(e%3===0,"native central order3");return e/3;});
function compose(g,h){const [x,t]=g,[y,u]=h;return [x.map((a,i)=>add(a,mul(y[i],roots[t]))),(t+u)%3];}
function rank3(rows,n){
  const A=rows.map(r=>r.slice());let rank=0;
  for(let j=0;j<n;j++){
    const p=A.findIndex((r,i)=>i>=rank&&mod(r[j],3)!==0);if(p<0)continue;
    [A[rank],A[p]]=[A[p],A[rank]];
    const scale=mod(A[rank][j],3)===1?1:2;A[rank]=A[rank].map(v=>mod(v*scale,3));
    for(let i=0;i<A.length;i++)if(i!==rank){const c=mod(A[i][j],3);A[i]=A[i].map((v,k)=>mod(v-c*A[rank][k],3));}
    rank++;
  }
  return rank;
}
function run(r){
  check(r.status==="NIL3_CONDITIONAL_NATIVE_PHASE_LIFT_NOT_COMPLETE_RECEIVER","no certified complete-receiver status");
  check(!Object.hasOwn(r,"end_to_end_simulation"),"secret-assignment recovery records cannot be restored");
  check(r.derivation_sha256===hash(DERIVATION)&&r.producer_sha256===hash(PRODUCER),"pinned source and derivation");
  const s=r.summary;
  check(s.nil3_state_hsp_solved_in_polynomial_time===false&&s.nil3_copy_complexity_is_O_n4===false&&s.conditional_top_digit_phase_lift_constructed===true&&s.lower_quotient_receiver_supplied===false&&s.tree_dilation_is_a_universal_lower_bound===false&&s.growing_depth_LWE_hardness_proved===false&&s.shor_level_speedup_claimed===false,"conditional component cannot promote absent quotient recovery or universal hardness");
  const ring=r.ring_model_countercontrols;
  check(ring.level===3&&ring.native_cyclotomic_ring_is_F3_truncated_polynomial_ring===false,"correct ring model");
  same(ring.ideal_HNF,[9,6,3],"actual ramified quotient");
  same(ring.native_three_times_one,add([1,0],add([1,0],[1,0])),"three times1 is not0");
  same(ring.incorrect_characteristic_three_result,[0,0],"retracted polynomial-ring result");
  same(ring.native_pi_squared,mul([-1,1],[-1,1]),"actual pi squared");
  const g=[[[8,0]],1],cube=compose(compose(g,g),g);
  same(ring.native_hidden_generator,g,"cyclic hidden subgroup generator");
  same(ring.native_hidden_generator_cube,cube,"native generator really has order3");
  check(ring.incorrect_truncated_polynomial_generator_cube_z_digit===2,"wrong-ring generator had order9");
  check(r.complete_scalar_phase_controls.length===729,"all scalar source combinations");
  let index=0;
  for(let x=0;x<3;x++)for(let y=0;y<3;y++)for(let u=0;u<3;u++)for(let a=0;a<9;a++)for(let b=0;b<3;b++){
    const c=r.complete_scalar_phase_controls[index++],lower=[x,y],label=[a,b],secret=add(reduce(lower),mul([6,0],[u,0]));
    same(c.known_lower,lower,"all lower representatives");same(c.public_label,label,"all original labels");
    check(c.top_digit_fixture_only===u&&c.known_lower_is_an_explicit_input_premise===true&&c.top_secret_used_in_gate_parameters===false,"top digit is a fixture, not a gate parameter");
    const source=lambdas.map(l=>exponent(label,mul(secret,l)));
    const correction=lambdas.map(l=>mod(-exponent(label,mul(lower,l)),9));
    const residual=source.map((v,j)=>mod(v+correction[j],9)),coeff=row([label])[0],k=mod(coeff*u,3);
    same(c.source_phase_exponents_mod9_fixture,source,"actual original-state ninth-root phases");
    same(c.phase_correction_exponents_mod9,correction,"secret-blind known-lower correction");
    same(c.central_character_row,[coeff],"actual central-character coefficient");
    same(c.exact_residual_phase_exponents_mod9,residual,"complete residual phase");
    same(residual,[0,3*k,mod(6*k,9)],"Fourier character, not an assumed residual");
    check(c.expected_top_character_outcome_fixture===k&&c.measurement_probabilities.length===3&&c.measurement_probabilities.every((p,j)=>Number.isFinite(p)&&Math.abs(p-(j===k?1:0))<1e-12),"actual qutrit Fourier numerical conformance");
  }
  check(r.conditional_batch_controls.length===3,"committed conditional vector batches");
  let consumed=0;
  r.conditional_batch_controls.forEach((b,i)=>{
    const n=[2,4,8][i],out=b.result,truth=b.top_truth_fixture_only;
    check(b.dimension===n&&b.lower_quotient_receiver_executed===false&&b.known_lower_fixture.length===n&&truth.length===n&&truth.every(t=>Number.isInteger(t)&&t>=0&&t<3),"lower recovery not claimed from a supplied premise");
    b.known_lower_fixture.forEach(v=>check(v.length===2&&v.every(x=>Number.isInteger(x)&&x>=0&&x<3),"known level2 representatives"));
    check(b.public_labels.length===n+8&&out.available_samples===n+8&&out.consumed_samples>=n&&out.consumed_samples<=n+8&&out.rows.length===out.consumed_samples&&out.measured_outcomes.length===out.consumed_samples,"finite source budget, no free extra samples");
    b.public_labels.forEach(label=>check(label.length===n&&label.every(v=>v.length===2&&Number.isInteger(v[0])&&v[0]>=0&&v[0]<9&&Number.isInteger(v[1])&&v[1]>=0&&v[1]<3),"actual native label chart"));
    check(out.status==="CONDITIONAL_TOP_DIGITS_RECOVERED"&&out.known_lower_premise_verified_here===false&&out.full_secret_receiver_supplied===false,"conditional reconstruction only");
    out.rows.forEach((a,j)=>{same(a,row(b.public_labels[j]),"rows derived from consumed original labels");check(out.measured_outcomes[j]===mod(a.reduce((v,t,k)=>v+t*truth[k],0),3),"actual top-character measurement outcome");});
    check(rank3(out.rows,n)===n,"full-rank reconstruction, no guessing missing digits");
    same(out.recovered_top_digits,truth,"conditional top output");
    consumed+=out.consumed_samples;
  });
  check(r.tree_dilation_ledger.length===20,"complete specified-tree ledger");
  r.tree_dilation_ledger.forEach((c,i)=>{
    const n=[4,8,16,32][Math.floor(i/5)],depth=[2,3,4,8,16][i%5],W=BigInt(n+1)**2n;
    check(c.dimension_n===n&&c.nilpotency_class_r===depth&&c.window_size_W===Number(W),"committed dimensions and depths");
    check(BigInt(c.copies_per_state_in_specified_disjoint_tree)===W**BigInt(depth-2)&&BigInt(c.total_copies_in_specified_disjoint_tree)===BigInt(n*n)*W**BigInt(depth-2),"literal disjoint-tree recurrence, not a lower bound");
    check(c.fixed_depth_polynomial_degree_in_n===2*depth-2&&c.every_fixed_r_is_polynomial_in_n===true&&c.implemented_receiver_or_universal_copy_lower_bound===false,"every fixed depth is polynomial; no blanket growing-depth impossibility");
  });
  return {status:"PASS",native_scalar_phase_controls:729,conditional_vector_batches:3,consumed_samples:consumed,tree_model_records:20,full_receiver_supplied:false};
}
if(require.main===module){console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2]||REPORT,"utf8"))),null,2));}
module.exports={run};
