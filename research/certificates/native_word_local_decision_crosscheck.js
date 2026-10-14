"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto"),E=require("./cyclotomic_exact.js");
const {check,same,rat,parse,str,add,sub,mul,div,cmp,one,zero}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/reductions/native_word_local_decision.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex"),key=JSON.stringify;
const mod=(a,q)=>(a%q+q)%q,min=(a,b)=>cmp(a,b)<=0n?a:b;
function cube(q,n){return n?cube(q,n-1).flatMap(w=>Array.from({length:q},(_,a)=>[...w,a])):[[]];}
function blocks(M,k,start=0,p=[]){if(!k)return[p];return Array.from({length:M-start-k+1},(_,j)=>blocks(M,k-1,start+j+1,[...p,start+j])).flat();}
function choose(M,k){let x=1n;for(let j=1;j<=k;j++)x=x*BigInt(M-j+1)/BigInt(j);return x;}
function vocabulary(M,k){let x=0n;for(let j=1;j<=k;j++)x+=choose(M,j)*6n**BigInt(j);return x/2n;}
function scopes(o,yes,no){yes.forEach(k=>check(o[k]===true,"scope "+k));no.forEach(k=>check(o[k]===false,"unsupported claim "+k));}
function expectation(K,phases,rows){const D=phases.length;let x=K.F();rows.forEach((row,i)=>row.forEach(([j,w])=>{x=K.plus(x,K.scale(K.powers[mod(phases[j]-phases[i],K.q)],div(w,rat(BigInt(D)))));}));return x;}
function finite(c){
  const s=c.preparation_contract,f=s.public_family,q=Number(f.modulus),n=f.dimension,M=f.sites,K=E.field(q),D=3**M;
  check(f.cohorts===1&&Number.isSafeInteger(n)&&n>0&&D<=256,"bounded paired source");
  const raw=c.original_records,mask=c.known_mask,truth=c.truth_fixture_only.masked_secret,errors=c.truth_fixture_only.original_errors;
  check(raw.length===2*M&&mask.length===n&&truth.length===n&&errors.length===2*M,"original shape");
  const ids=new Set();raw.forEach((r,j)=>{
    check(r.modulus===q&&r.label.length===n&&typeof r.source_id==="string"&&r.source_id&&!ids.has(r.source_id),"original lineage");ids.add(r.source_id);
    [...r.label,r.value,...mask,...truth].forEach(x=>check(Number.isSafeInteger(x)&&x>=0&&x<q,"canonical original data"));check(Number.isSafeInteger(errors[j]),"exact original error");
    check(mod(r.value+r.label.reduce((a,x,i)=>a+x*mask[i],0)-r.label.reduce((a,x,i)=>a+x*truth[i],0),q)===mod(errors[j],q),"truth source equation");
  });
  const pairs=Array.from({length:M},(_,j)=>[raw[2*j].label,raw[2*j+1].label]);same(f.paired_labels,[pairs],"actual pair labels");
  const W=cube(3,M),index=new Map(W.map((w,i)=>[key(w),i])),values=[],phases=[],ideal=[];
  const localPhases=pairs.map((pair,j)=>{const a=mod(raw[2*j].value+pair[0].reduce((a,x,i)=>a+x*mask[i],0),q),b=mod(raw[2*j+1].value+pair[1].reduce((a,x,i)=>a+x*mask[i],0),q);return[a,mod(b-a,q),mod(-b,q)];});
  const offsets=pairs.map(([a,b])=>[a.map((x,i)=>mod(b[i]-2*x,q)),a.map((x,i)=>mod(-b[i]-x,q))]);
  const rows=W.map(w=>{const beta=w.flatMap(t=>[[1,0],[-1,1],[0,-1]][t]),freq=Array.from({length:n},(_,i)=>mod(beta.reduce((a,b,j)=>a+b*raw[j].label[i],0),q)),phase=mod(w.reduce((a,t,j)=>a+localPhases[j][t],0),q);values.push(freq);phases.push(phase);ideal.push(mod(freq.reduce((a,x,i)=>a+x*truth[i],0),q));return{cohort:0,word:w,frequency:freq,known_phase:phase};});
  same(c.actual_word_rows,rows,"all actual original words");same(s.known_word_phases_by_cohort,[localPhases],"original preparation phases");
  scopes(s,[],["secret_or_errors_supplied_to_preparation","normalized_fibre_oracle_supplied","physical_gate_synthesis_and_precision_supplied"]);
  check(s.original_records_paid_once===2*M&&s.uniform_qutrits===M,"paid original and word counts");
  const R=c.heatbath_reference,H=R.prefix,k=R.support,B=blocks(M,k),locals=cube(3,k);
  check([3,9,27,81].includes(H)&&q%H===0&&k>0&&k<=M,"legal prefix and block size");same(R.complete_words,W,"whole word order");same(R.full_frequency_values,values,"original full frequency values");
  const local=(block,digits)=>Array.from({length:n},(_,i)=>mod(block.reduce((a,j,l)=>a+(digits[l]?offsets[j][digits[l]-1][i]:0),0),H));
  const transitions=W.map(w=>{
    const out=new Map();for(const b of B){const target=key(local(b,b.map(j=>w[j]))),allowed=locals.filter(d=>key(local(b,d))===target),p=rat(1n,BigInt(B.length*allowed.length));
      allowed.forEach(d=>{const v=w.slice();b.forEach((j,l)=>v[j]=d[l]);const i=index.get(key(v));out.set(i,add(out.get(i)||zero,p));});}
    return [...out].sort((a,b)=>a[0]-b[0]);
  });
  same(R.conditional_transition_rows,transitions.map(row=>row.map(([j,w])=>[j,str(w)])),"all exact conditional kernel rows");
  const unseen=new Set(W.map((_,i)=>i)),components=[];while(unseen.size){const seen=new Set([Math.min(...unseen)]),stack=[...seen];while(stack.length){for(const[j]of transitions[stack.pop()])if(!seen.has(j)){seen.add(j);stack.push(j);}}seen.forEach(i=>unseen.delete(i));components.push([...seen].sort((a,b)=>a-b));}
  same(R.connected_components,components,"actual communicating components");
  const ground=Array(D),bounds=[];components.forEach(C=>{
    C.forEach(i=>ground[i]=C.map(j=>[j,rat(1n,BigInt(C.length))]));
    if(C.length>1){let edge=one;C.forEach(i=>transitions[i].forEach(([j,w])=>{if(j!==i)edge=min(edge,w);}));bounds.push(k===M?one:div(mul(rat(2n),edge),rat(BigInt(C.length*(C.length-1)))));}
  });
  const groundP=expectation(K,phases,ground),oneStep=expectation(K,phases,transitions),idealP=expectation(K,ideal,ground);
  same(c.exact_ground_acceptance_polynomial,K.encode(groundP),"exact ground probability");same(c.exact_one_random_block_acceptance_polynomial,K.encode(oneStep),"exact local energy statistic");
  check(c.ground_rank===components.length&&c.full_fibre_span_rank===new Set(values.map(key)).size,"component rank is not automatically fibre rank");
  const trace=transitions.reduce((a,row,i)=>add(a,row.find(([j])=>i===j)[1]),zero);
  check(c.exact_ground_IID_null_acceptance===str(rat(BigInt(components.length),BigInt(D)))&&c.exact_one_random_block_IID_null_acceptance===str(div(trace,rat(BigInt(D)))),"true IID null traces");
  check(c.Hamiltonian_identically_zero===(bounds.length===0)&&c.positive_Hamiltonian_gap_lower===(bounds.length?str(bounds.reduce(min)):null),"absolute nonzero gap versus identity effect");
  const preserves=transitions.every((row,i)=>row.every(([j])=>key(values[i])===key(values[j])));
  check(R.full_native_source_family_stationary_certified===preserves&&c.full_root_source_moment_bound_applicable===preserves,"prefix fidelity cannot grant whole-root source bound");
  let e2=0n;for(let j=0;j<2*M;j+=2){const a=BigInt(errors[j]),b=BigInt(errors[j+1]);e2+=a*a+b*b-a*b;}
  const noise=min(one,rat(80n*e2,3n*BigInt(q*q)));
  check(c.conditional_pathwise_ground_rejection_upper===(preserves?str(noise):null),"truth-only frozen-error bound");
  if(preserves){check(K.eq(idealP,K.unit),"source lies in full-root component span");check(E.sign(K,K.plus(groundP,K.scale(K.unit,sub(noise,one))))>=0,"actual rejection below pathwise bound");}
  const interval=c.classical_first_block_expectation,b=Array.from({length:k},(_,i)=>i),groups=new Map();
  locals.forEach(d=>{const value=key(local(b,d)),phase=mod(d.reduce((a,t,j)=>a+localPhases[b[j]][t],0),q);if(!groups.has(value))groups.set(value,[]);groups.get(value).push(phase);});
  let p=K.F(),pairCount=0;groups.forEach(v=>{pairCount+=v.length*(v.length-1)/2;v.forEach(a=>v.forEach(b=>{p=K.plus(p,K.scale(K.powers[mod(b-a,q)],rat(1n,BigInt(locals.length*v.length))));}));});
  const lo=parse(interval.acceptance_lower),hi=parse(interval.acceptance_upper);check(cmp(lo,hi)<=0n&&cmp(sub(hi,lo),rat(1n,1n<<BigInt(interval.enclosure_bits)))<=0n,"certified local interval width");
  check(E.sign(K,K.plus(p,K.scale(K.unit,rat(-lo[0],lo[1]))))>=0&&E.sign(K,K.plus(K.scale(K.unit,hi),K.scale(p,rat(-1n))))>=0,"classical interval contains exact quantum local statistic");
  same(interval.block,b,"one block only");check(interval.local_words_evaluated===locals.length&&interval.cosine_pair_evaluations===pairCount&&interval.exact_IID_raw_null_acceptance===str(rat(BigInt(groups.size),BigInt(locals.length))),"whole local enumeration and original null cost");
  scopes(interval,["uses_actual_original_values_and_known_mask","null_trace_is_for_fixed_mask_IID_original_values"],["all_blocks_or_whole_words_enumerated","unknown_quantum_only_phases_allowed","ground_space_projection_or_long_time_walk_simulated"]);
  // Enumerate the full six-transition vocabulary, not only observed edges.
  const signatures=[[1,0],[0,1],[-1,0],[-1,1],[0,-1],[1,-1]],directions=[[0,1],[0,2],[1,0],[1,2],[2,0],[2,1]],zeros=[];let count=0;
  for(let j=1;j<=k;j++)for(const b of blocks(M,j))for(const choices of cube(6,j)){
    const coeff=choices.map(x=>signatures[x]);if(coeff[0].find(x=>x)<0)continue;count++;
    const freq=Array.from({length:n},(_,l)=>mod(b.reduce((a,i,t)=>a+coeff[t][0]*offsets[i][0][l]+coeff[t][1]*offsets[i][1][l],0),H));
    if(freq.every(x=>!x)){const a=Array(M).fill(0),c=a.slice();b.forEach((i,t)=>[a[i],c[i]]=directions[choices[t]]);zeros.push({positions:b,coefficients:coeff,first_word:a,second_word:c});}
  }
  const A=c.whole_small_signature_audit;same(A.zero_signatures,zeros,"all exact original collision signatures");check(A.unoriented_signatures_checked===String(count)&&BigInt(count)===vocabulary(M,k)&&A.complete_vocabulary_checked===true&&A.all_small_moves_frozen_certified===(zeros.length===0),"whole small-support audit");
  scopes(c,["null_trace_is_for_fixed_mask_IID_original_values"],["dense_kernel_is_an_efficient_ground_effect","coherent_walk_gate_export_supplied","unknown_phase_measurement_access_granted","new_speedup_claim"]);
  return{words:D,signatures:count};
}
function population(L){
  const n=L.dimension,r=L.root_digits,M=L.original_pairs,k=L.support;[n,r,M,k].forEach(x=>check(Number.isSafeInteger(x)&&x>0,"positive scaling parameter"));check(k<=M,"legal support");
  const v=vocabulary(M,k),G=3n**BigInt(n*r),bits=Math.min(128,Math.max(0,G.toString(2).length-v.toString(2).length-1)),p=rat(1n,1n<<BigInt(bits));
  check(L.unoriented_difference_signatures===String(v)&&L.conservative_probability_budget_bits===bits&&L.probability_any_exact_full_root_local_collision_upper===str(p)&&L.probability_ground_effect_is_identity_lower===str(sub(one,p)),"conservative scaling bound rounded up");
  same(L.exact_uncapped_union_ratio,{numerator:String(v),denominator_base:3,denominator_exponent:n*r},"exact factored ratio without huge decimal allocation");
  check(v*(1n<<BigInt(bits))<=G||bits===0,"no falsely sharpened probability bound");
  check(L.nonunit_offset_chart_determinant===3,"singular chart modulo3");
  scopes(L,["original_paired_labels_IID_uniform_required","label_and_word_adaptive_exact_local_policies_covered","every_signature_has_a_unit_in_original_pair_coefficients"],
    ["independent_offset_frequency_columns_assumed","temporary_syndrome_violations_or_collective_macros_excluded","generic_quantum_decoder_lower_bound_proved"]);
}
function verify(p){
  check(p.status==="PAIRED_WORD_LOCAL_GROUND_TEST_AND_CLASSICAL_ONE_BLOCK_COUNTERPART_REVIEW_PENDING","review pending");
  check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_word_local_decision.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_WORD_LOCAL_DECISION.md")),"current provenance");
  const deps=["native_short_preimage_reduction.py","native_word_frame_access.py","native_full_root_slice.py","native_word_span_decision.py","ternary_native_block_walk.py","ternary_certified_noise_sampler.py","ternary_covariant_noise.py","ternary_measured_lattice_decoder.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"dependency set");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(p.actual_paired_source_controls.length===4&&p.growing_root_local_move_ledgers.length===4,"live coverage");const stats=p.actual_paired_source_controls.map(finite);p.growing_root_local_move_ledgers.forEach(population);
  same(p.actual_paired_source_controls.map(c=>[c.ground_rank,c.full_fibre_span_rank,c.full_root_source_moment_bound_applicable]),[[81,9,true],[13,9,true],[9,9,true],[3,9,false]],"frozen, disconnected, global and false-prefix controls");
  scopes(p,[],["offset_chart_joint_law_is_IID","all_efficient_span_tests_excluded","accepted_speedup_candidate","new_active_negative_result_created"]);
  return{verified:true,exact_transition_rows:stats.reduce((a,x)=>a+x.words,0),complete_original_signatures:stats.reduce((a,x)=>a+x.signatures,0),local_statistics_with_classical_counterpart:4,
    global_ground_effect_or_general_receiver_lower_bound:false};
}
module.exports={verify,finite,population};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));
