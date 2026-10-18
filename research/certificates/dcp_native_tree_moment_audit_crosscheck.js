#!/usr/bin/env node
"use strict";
// Producer: exact Z4 elimination. Checker: independent tree partition counting
// plus direct original-label edge constraints and exact overflow arithmetic.
const fs=require("fs"),path=require("path");
const {sameProbability,readProbability,normalize,add}=require("./dcp_adaptive_direction_rank_gate_crosscheck.js");
function need(v,m){if(!v)throw new Error(m);}
function same(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function pop(x){let n=0;for(;x;x&=x-1)n++;return n;}
function mul(a,b){return normalize(a.p*b.p,a.e+b.e);}
function sub(a,b){const e=Math.max(a.e,b.e);return normalize((a.p<<BigInt(e-a.e))-(b.p<<BigInt(e-b.e)),e);}
function hex(x){return"0x"+x.toString(16);}
function frac(s){const[a,b="1"]=String(s).split("/");const p=BigInt(a),q=BigInt(b);need(q>0n,"rational denominator");return{p,q};}
function checkFraction(s,p,q,m){const a=frac(s);need(a.p*q===p*a.q,m);}
function choose(n,k){let p=1n;for(let j=1;j<=k;j++)p=p*BigInt(n+1-j)/BigInt(j);return p;}
function checkMoment(R){
  const a=R.depth,b=R.chunk_components;
  need(Number.isSafeInteger(a)&&a>=1&&a<=8&&Number.isSafeInteger(b)&&b>=1&&b<=64,"moment dimensions");
  const k=2**a,L=1n<<BigInt(2*b),c=normalize(L-1n,4*b);
  need(R.secret_vector_components===b*(a+1)&&R.leaf_count===k&&R.leaf_list_length_hex===hex(L),"native tree dimensions");
  need(R.internal_weight_moment_recurrence.length===a+1,"recurrence coverage");
  let f={p:1n,e:0};sameProbability(R.internal_weight_moment_recurrence[0],1n,0,"initial moment");
  for(let j=1;j<=a;j++){f=add(mul(f,f),c);sameProbability(R.internal_weight_moment_recurrence[j],f.p,f.e,"native moment recurrence");}
  const M=add(f,normalize(L-1n,2*b));
  sameProbability(R.mean_degree,1n,0,"native mean degree");sameProbability(R.second_degree_moment,M.p,M.e,"native second moment");
  need(R.M_at_most_3_sufficient_size_condition===(L>=2n*BigInt(k-1))&&
       R.M_actually_at_most_3===(M.p<=3n*(1n<<BigInt(M.e)))&&R.leaf_entries_assumed_mutually_IID===false,"moment scope/size gate");
  return{a,b,k,L,n:b*(a+1),M};
}
function checkPatterns(C,a){
  const b=C.chunk_components,k=2**a,L=1n<<BigInt(2*b);
  need(C.depth===a&&b===1&&C.patterns.length===2**k&&C.ranks_are_over_Z4_with_no_even_residual_not_only_F2===true,"complete pattern/rank coverage");
  let total={p:0n,e:0},pairTotal=0n;
  C.patterns.forEach((R,s)=>{
    const ranks=[];let redundancies=0;
    for(let j=1;j<=a+1;j++){
      const size=2**Math.min(j,a);let rank=0;
      for(let start=0;start<k;start+=size){const shared=((s>>start)&((1<<size)-1))===(1<<size)-1;rank+=shared?1:2;if(shared)redundancies++;}
      ranks.push(rank);
    }
    need(R.shared_leaf_mask_hex===hex(BigInt(s))&&same(R.unit_constraint_ranks_by_chunk,ranks)&&
         R.shared_subtree_and_last_root_redundancies===redundancies,"independent Z4 partition rank");
    const pairs=L**BigInt(k)*(L-1n)**BigInt(k-pop(s)),e=2*b*ranks.reduce((s,r)=>s+r,0);
    need(R.ordered_tuple_pair_count_hex===hex(pairs),"native shared-support multiplicity");
    sameProbability(R.joint_survival_probability,1n,e,"joint native survival");
    sameProbability(R.second_moment_term,pairs,e,"weighted native moment term");
    total=add(total,normalize(pairs,e));pairTotal+=pairs;
  });
  need(pairTotal===L**BigInt(2*k),"complete tuple pair population");
  sameProbability(C.observed_second_moment,total.p,total.e,"rank-census moment sum");
  let f={p:1n,e:0};for(let j=0;j<a;j++)f=add(mul(f,f),normalize(L-1n,4*b));
  const expected=add(f,normalize(L-1n,2*b));
  need(total.p===expected.p&&total.e===expected.e,"rank census vs compact moment");
}
function checkOverflow(R,a,b){
  const D=checkMoment(R.moment),{k,L,n,M}=D,unit=1n<<BigInt(M.e),ceilM=(M.p+unit-1n)/unit;
  need(D.a===a&&D.b===b,"overflow parameter grid");
  let g=0;while((1n<<BigInt(g))*unit<4n*(M.p-unit))g++;
  const C=256n*ceilM*BigInt(k)*L,deltaP=BigInt(k-2)*L,deltaQ=C+1n;
  need(R.hash_bits===g&&R.public_affine_seed_bits===g*(4*b*k+1)&&R.intermediate_list_capacity_hex===hex(C)&&
       R.nonroot_internal_nodes===k-2,"mark/cap/source budget");
  sameProbability(R.affine_mark_probability,1n,g,"independent mark probability");
  checkFraction(R.overflow_probability_upper_bound_exact_rational,deltaP,deltaQ,"unconditional overflow union");
  checkFraction(R.M_times_overflow_bound_exact_rational,M.p*deltaP,unit*deltaQ,"degree-correlated Cauchy product");
  need(M.p*deltaP*256n<unit*deltaQ,"justified overflow loss surrogate");
  const original=normalize((unit<<BigInt(g))-2n*(M.p-unit),M.e+3*g),loss=k>2?normalize(1n,2*g+3):{p:0n,e:0},lower=sub(original,loss);
  sameProbability(R.original_mutual_isolation_lower,original.p,original.e,"mutual edge/wedge bound");
  sameProbability(R.overflow_marked_mass_loss_upper_surrogate,loss.p,loss.e,"two-endpoint correlated overflow loss");
  sameProbability(R.coarse_mass_lower_IF_clean_exact_receiver_contract,lower.p,lower.e,"conditional nonoverflow mass");
  sameProbability(R.universal_loose_coarse_lower_IF_receiver_contract,3n,2*g+3,"loose conditional source lower");
  const B=4*b;let w=1;while(choose(B,w)<L)w++;
  need(R.default_leaf_block_width===B&&R.default_original_registers===B*k&&R.default_leaf_support_weight===w&&
       R.default_full_physical_mask_width===k*w,"physical support accounting");
  const e=Math.floor(Math.log2(n)),v={p:(1n<<BigInt(e))-1n,e},vis=normalize(v.p**BigInt(k*w),e*k*w),weighted=mul(lower,vis);
  sameProbability(R.dyadic_original_visibility_lower_promise,v.p,v.e,"dyadic noise lower premise");
  checkFraction(R.ideal_inverse_dimension_visibility_exact_rational,BigInt(n-1),BigInt(n),"inverse-dimension target noise");
  sameProbability(R.conditional_mean_unfiltered_visibility_lower_IF_receiver_contract,weighted.p,weighted.e,"physical-width visibility factor");
  const factors=R.conditional_mean_useful_visibility_lower_factors_IF_receiver_contract;
  need(R.input_phase_bits_for_higher_label_factor===n+2&&factors.length===3&&
       same(factors[2],{one_minus_two_to_negative:n*n}),"paid higher-label factorization");
  sameProbability(factors[0],lower.p,lower.e,"coarse lower factor");sameProbability(factors[1],vis.p,vis.e,"visibility lower factor");
  need(R.naive_nonroot_candidate_cell_upper_bound_hex===hex(BigInt(k-2)*C*C)&&
       R.classical_Wagner_expected_kL_bound_used_as_quantum_gate_count===false&&R.clean_bounded_list_receiver_implemented===false&&
       R.overflow_detection_inspects_affine_mark_seed===false&&R.overflow_independent_of_degree_assumed===false&&
       R.native_mean_is_before_label_or_syndrome_postselection===true&&
       R.source_bound_is_pointwise_in_A_or_hash_seed===false,"receiver/cost/overflow scope");
}
function checkEdges(C,index){
  const A=C.coarse_labels,a=C.depth,b=C.chunk_components,k=2**a,m=A[0].length,n=A.length;
  need(a===2&&b===1&&m===16&&n===3&&A.every(row=>row.length===m&&row.every(v=>Number.isSafeInteger(v)&&v>=0&&v<4))&&
       C.control_id===["unfiltered-seeded-native-edge-control","all-zero-high-degree-countercontrol"][index]&&
       same(C.original_assignments,[0,3,17,121,1024,65535]),"finite original-label control");
  const lists=C.leaf_supports_hex.map(row=>row.map(h=>Number(BigInt(h))));
  need(same(lists,Array.from({length:4},(_,j)=>Array.from({length:4},(_,i)=>1<<(4*j+i)))),"fixed native leaf supports");
  function passes(x,masks){
    for(let level=1;level<=a+1;level++){
      const size=2**Math.min(level,a);
      for(let start=0;start<k;start+=size){
        const u=masks.slice(start,start+size).reduce((v,s)=>v|s,0);
        for(let l=(level-1)*b;l<level*b;l++){
          const sum=A[l].reduce((s,v,i)=>s+((u>>i)&1?v*((x>>i)&1?-1:1):0),0);
          if((sum%4+4)%4!==0)return false;
        }
      }
    }
    return true;
  }
  let accepted=0,checks=0;
  for(const x of C.original_assignments)for(let code=0;code<256;code++){
    const masks=lists.map((row,j)=>row[(code>>(2*j))&3]),u=masks.reduce((v,s)=>v|s,0);
    if(passes(x,masks)){
      need(passes(x^u,masks),"partner negation invariance");accepted++;
      for(const row of A)need(row.reduce((s,v,i)=>s+v*((((x^u)>>i)&1)-((x>>i)&1)),0)%4===0,"full coarse preservation");
    }
    checks++;
  }
  need(C.tuple_tests===checks&&C.accepted_filtered_edges===accepted&&C.counts_are_native_probability_estimates===false,"edge census/scope");
  if(index===1)need(A.every(row=>row.every(v=>v===0))&&accepted===1536,"bad pointwise high-degree control");
}
function verify(R){
  need(R.contract_id==="native_signed_tree_second_moment_and_overflow_contract_v1"&&R.status==="LOCAL_DERIVATION_RECEIVER_NOT_IMPLEMENTED"&&
       R.accepted_speedup_candidate===false&&R.novelty_claim===false&&R.external_theorem_review_complete===false&&R.source_quantum_preparations_executed===0,"global admission");
  need(R.complete_pattern_rank_censuses.length===3&&R.native_edge_invariance_controls.length===2&&R.conditional_overflow_frontiers.length===8,"research coverage");
  R.complete_pattern_rank_censuses.forEach((C,i)=>checkPatterns(C,i+1));R.native_edge_invariance_controls.forEach(checkEdges);
  const grid=[[1,1],[2,1],[3,1],[3,4],[4,8],[4,16],[4,32],[4,64]];
  R.conditional_overflow_frontiers.forEach((F,i)=>checkOverflow(F,...grid[i]));
  ["leaf_entries_assumed_mutually_IID","free_list_oracle_or_QRAM","silent_truncation_inherits_this_contract",
   "overflow_independent_of_degree_assumed","mathematical_graph_bound_is_an_implemented_receiver",
   "polynomial_time_or_growing_depth_decoder_supplied","actual_natural_source_noise_certified"].forEach(k=>need(R.scope[k]===false,"scope expansion: "+k));
  need(R.scope.higher_label_useful_factor_requires_fresh_uniform_lifts===true,"higher-label source premise");
  need(same(R.literature,["https://people.eecs.berkeley.edu/~daw/papers/genbday.html","https://arxiv.org/abs/2410.06856"]),"prior literature scope");
  return{status:"ok",complete_equality_patterns:276,original_tuple_checks:3072,conditional_frontiers:8,coherent_receiver_implemented:false};
}
module.exports={verify};
if(require.main===module){const file=process.argv[2]||path.resolve(__dirname,"../phase_workbench/dcp_native_tree_moment_audit.json");console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(file,"utf8")))));}
