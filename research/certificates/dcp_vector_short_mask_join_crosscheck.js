#!/usr/bin/env node
"use strict";
// Independent direct vector graphs and exact source/resource arithmetic.
// No packed-key cyclic addition and no producer pass flags are trusted.
const fs=require("fs"),path=require("path");
const {sameProbability,readProbability,normalize}=require("./dcp_adaptive_direction_rank_gate_crosscheck.js");
function need(v,m){if(!v)throw new Error(m);}
function same(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function mod(a,q){return(a%q+q)%q;}
function parity(x){let n=0;for(;x;x&=x-1)n^=1;return n;}
function pop(x){let n=0;for(;x;x&=x-1)n++;return n;}
function choose(n,k){let v=1n;for(let i=1;i<=k;i++)v=v*BigInt(n+1-i)/BigInt(i);return v;}
function hex(v){return"0x"+v.toString(16);}
function checkResource(R){
  const n=R.secret_vector_components,m=R.original_registers,k=R.per_block_weight;
  need(Number.isSafeInteger(n)&&n>0&&n<=512&&Number.isSafeInteger(m)&&m>=2&&m%2===0&&m<=4096&&
       Number.isSafeInteger(k)&&k>=1&&k<=m/2,"resource dimensions");
  const C=R.counts_hex,L=BigInt(C.each_list_length),G=1n<<BigInt(2*n),S=L*L,available=choose(m/2,k);
  need(L>0n&&L<=available,"distinct support lists");
  let g=0;while((1n<<BigInt(g))*G<4n*S)g++;
  const levels=(2n*L-1n).toString(2).length,P=1n<<BigInt(levels),comparators=P*BigInt(levels*(levels+1))/4n;
  const keyBits=2*n+g+1,counterBits=S.toString(2).length,recordBits=keyBits+2+m,stateBits=keyBits+3*counterBits+3*m;
  const expected={each_list_length:L,available_block_supports:available,padded_records:P,
    one_xor_record_evaluations:4n*L,one_xor_comparators:2n*comparators,
    one_xor_scan_steps:2n*P,six_xor_comparators:12n*comparators,
    persistent_workspace_bits:P*BigInt(recordBits)+(P+1n)*BigInt(stateBits)+comparators};
  need(Object.keys(C).length===Object.keys(expected).length,"resource ledger completeness");
  Object.entries(expected).forEach(([key,v])=>need(C[key]===hex(v),"charged join resource: "+key));
  need(R.group==="Z4^n with componentwise modular addition"&&R.group_cardinality_binary_exponent===2*n&&
       R.physical_mask_width===2*k&&R.hash_bits===g&&R.public_seed_bits===g*(m+1)&&
       R.record_bits===recordBits&&R.scan_state_bits===stateBits,"group/hash/register parameters");
  sameProbability(R.mean_degree,S,2*n,"first degree moment");
  sameProbability(R.degree_second_moment,S*S+S*(G-1n),4*n,"second degree moment");
  const lower=normalize((S<<BigInt(2*n+g))-2n*S*(S-1n),4*n+3*g);
  sameProbability(R.native_mean_coarse_coverage_lower_bound,lower.p,lower.e,"mutual isolation bound");
  sameProbability(R.mark_probability,1n,g,"affine mark probability");
  need(R.full_assignment_table_used===false&&R.coherent_RAM_assumed===false&&R.polynomial_time_claimed===false&&
       R.gate_export_implemented===false&&R.time_form==="O(L*log(L)^2*poly(n,m))"&&
       R.space_form==="O(L*poly(n,m)) coherent basis-wire bits","exponential/coherent resource scope");
  return {n,m,k,L,g,S,G,lower};
}
function family(m,k,L){
  const masks=[];for(let u=1;u<1<<(m/2);u++)if(pop(u)===k)masks.push(u);
  const coords=u=>Array.from({length:m/2},(_,i)=>i).filter(i=>u>>i&1);
  masks.sort((u,v)=>{const a=coords(u),b=coords(v);for(let i=0;i<a.length;i++)if(a[i]!==b[i])return a[i]-b[i];return 0;});
  const block=masks.slice(0,Number(L));return block.flatMap(u=>block.map(v=>u|(v<<(m/2))));
}
function marked(x,H,c){return H.reduce((v,h,j)=>v|(parity(h&x)<<j),0)===c;}
function delta(A,x,y){return A.map(row=>mod(row.reduce((v,a,i)=>v+a*(((y>>i)&1)-((x>>i)&1)),0),4));}
function checkProgram(P){
  need(P.kind==="VECTOR_Z4_BALANCED_SORT_JOIN"&&P.descent_bits===2,"program group");
  const C=checkResource(P.resource_ledger),{n,m,k,L,g}=C,A=P.coarse_labels;
  need(n===P.components&&m===P.width&&k===P.per_block_weight&&P.list_length_hex===hex(L)&&m<=8&&
       A.length===n&&A.every(row=>row.length===m&&row.every(a=>Number.isSafeInteger(a)&&a>=0&&a<4)),"finite public coarse source");
  const H=P.hash_rows_hex.map(h=>Number(BigInt(h))),c=Number(BigInt(P.hash_offset_hex));
  need(H.length===g&&H.every(h=>Number.isSafeInteger(h)&&h>=0&&h<1<<m)&&Number.isSafeInteger(c)&&c>=0&&c<1<<g,"unfiltered seed representation");
  need(P.selection_access==="coarse-labels-and-independent-unfiltered-affine-seed"&&
       P.seed_has_been_conditioned_on_success===false&&P.uniform_efficient_program_supplied===false&&
       P.table_lookup_is_a_free_coherent_oracle===false,"program lineage/cost scope");
  return {...C,A,H,c,masks:family(m,k,L)};
}
function checkFinite(F){
  const C=checkProgram(F.program),{A,H,c,m,n,masks}=C,size=1<<m;
  const table=Array.from({length:size},(_,x)=>{
    if(!marked(x,H,c))return null;
    const neighbors=masks.filter(u=>marked(x^u,H,c)&&delta(A,x,x^u).every(v=>v===0)).map(u=>x^u);
    return neighbors.length===1?neighbors[0]:null;
  });
  need(F.all_original_assignments_checked===size&&same(F.diagnostic_proposal_table_NOT_free_oracle,table)&&
       F.source_selection==="unfiltered seeded finite control, NOT a source probability estimate","direct vector proposal graph");
  const K=F.compiler,t=K.phase_bits,q=1n<<BigInt(t),full=K.public_labels_hex.map(row=>row.map(BigInt));
  need(K.descent_bits===2&&same(K.program,F.program)&&full.length===n&&
       full.every((row,l)=>row.length===m&&row.every((a,i)=>a>=0n&&a<q&&Number(a%4n)===A[l][i])),"full higher label binding");
  const accepted=[],pairs=[];
  for(let x=0;x<size;x++){
    const y=table[x];if(y===null||table[y]!==x)continue;
    const d=full.map(row=>mod(row.reduce((v,a,i)=>v+a*BigInt(((y>>i)&1)-((x>>i)&1)),0n),q));
    need(d.every(v=>v%4n===0n),"physical coarse relation");
    if(!d.some(v=>v!==0n))continue;
    accepted.push(x);
    if(x<y)pairs.push({first:x,second:y,descended_label_hex:d.map(v=>hex(v/4n)),physical_Hamming_width:pop(x^y),
      unconditional_pair_probability:{numerator_hex:"0x1",denominator_binary_exponent:m-1}});
  }
  need(same(K.accepted_assignments,accepted)&&same(K.pairs,pairs),"reciprocal useful vector pairs");
  sameProbability(K.useful_descent_probability,BigInt(accepted.length),m,"paid useful acceptance");
  need(K.accepted_XOR_F_calls===6&&K.failed_XOR_F_calls===4&&K.original_unknown_phase_qubits_per_attempt===m&&
       K.compiler_qubits_excluding_F_internal_work===3*m+4&&K.output_qubits_on_accepted_attempt===1&&
       K.pair_list_is_measurement_outcomes_not_parallel_outputs===true&&K.hardware_gate_export_backend_implemented===false&&
       K.secret_or_phase_evaluator_is_program_input===false&&K.same_A_source_resupply_or_inverse_supplied===false&&
       K.fresh_descended_labels_IID_certified===false,"compiler scope");
}
function checkCensus(R,n,m,k,L){
  const C=checkResource(R.resource_ledger),{g}=C,size=1<<m,seedCount=1<<(g*(m+1)),maskFamily=family(m,k,BigInt(L));
  need(R.components===n&&R.width===m&&R.weight===k&&R.list_length===L&&C.n===n&&C.m===m&&C.k===k&&C.L===BigInt(L),"census source coverage");
  const marks=[];
  for(let seed=0;seed<seedCount;seed++){
    const H=Array.from({length:g},(_,j)=>(seed>>(j*m))&(size-1)),c=seed>>(g*m);
    let mark=0;for(let x=0;x<size;x++)if(marked(x,H,c))mark|=1<<x;marks.push(mark);
  }
  let first=0,second=0,matched=0;
  for(let code=0;code<4**(n*m);code++){
    const A=Array.from({length:n},(_,l)=>Array.from({length:m},(_,i)=>(code>>(2*(l*m+i)))&3));
    const graph=Array.from({length:size},(_,x)=>maskFamily.reduce((bits,u)=>delta(A,x,x^u).every(v=>v===0)?bits|(1<<(x^u)):bits,0));
    graph.forEach(adj=>{const d=pop(adj);first+=d;second+=d*d;});
    for(const selected of marks){
      const induced=graph.map(adj=>adj&selected);
      for(let x=0;x<size;x++)if(selected>>x&1){const adj=induced[x];if(adj&&!(adj&(adj-1))&&induced[31-Math.clz32(adj)]===(1<<x))matched++;}
    }
  }
  const total=4**(n*m)*size*seedCount;
  need(R.all_label_seed_assignments_enumerated===total&&R.sum_unmarked_degrees===first&&
       R.sum_squared_unmarked_degrees===second&&R.mutual_unique_marked_assignments===matched,"complete original-label/seed census");
  sameProbability(R.observed_coarse_acceptance_probability,BigInt(matched),Math.log2(total),"observed source mass");
  need(BigInt(matched)*(1n<<BigInt(C.lower.e))>=BigInt(total)*C.lower.p&&
       R.uniform_hash_seed_space_rank_or_success_postselected===false,"census coverage/law scope");
}
function checkFrontier(F,n){
  const C=checkResource(F.resource_ledger),{L,k,lower}=C;
  need(C.n===n&&C.m===4*n&&L===1n<<BigInt(n)&&C.g===2&&k<=n&&F.phase_bits===n+2,"default vector growing grid");
  if(k>1)need(choose(2*n,k-1)<L,"minimum balanced mask weight");
  const nonzero=(1n<<BigInt(n*n))-1n,v=BigInt(n-1),ve=Math.log2(n);
  sameProbability(F.original_visibility,v,ve,"original visibility grid");
  sameProbability(F.uniform_higher_label_nonzero_probability,nonzero,n*n,"charged higher-label zero rejection");
  sameProbability(F.native_mean_useful_probability_lower_bound,lower.p*nonzero,lower.e+n*n,"useful source lower bound");
  sameProbability(F.native_mean_useful_visibility_lower_bound,lower.p*nonzero*v**BigInt(2*k),lower.e+n*n+2*k*ve,"original physical-width signal lower");
  need(F.source_coverage_lower_bound_is_for_each_fixed_A_or_seed===false&&F.favorable_A_or_seed_selection_uncharged===false&&
       F.abstract_noisy_source_wrapper_may_apply_under_its_separate_premises===true&&
       F.classical_partner_search_is_a_classical_secret_decoder===false&&F.exponential_recursive_supply_removed===false,"frontier interpretation");
}
function verify(R){
  need(R.contract_id==="vector_Z4_short_mask_balanced_sorting_join_frontier_v1"&&
       R.status==="LOCAL_DERIVATION_EXTERNAL_REVIEW_PENDING"&&R.accepted_speedup_candidate===false&&R.novelty_claim===false&&
       R.external_theorem_review_complete===false&&R.source_quantum_preparations_executed===0,"global admission");
  need(R.finite_controls.length===6&&R.complete_source_censuses.length===2&&R.native_short_mask_frontiers.length===5,"research coverage");
  need(same(R.finite_controls[0].compiler.public_labels_hex,[["0x1","0x3"],["0x1","0x3"]])&&
       same(R.finite_controls[1].compiler.public_labels_hex,[["0x3","0x1"],["0x0","0x3"]]),"group-packing countercontrols");
  R.finite_controls.forEach(checkFinite);checkCensus(R.complete_source_censuses[0],1,4,1,2);checkCensus(R.complete_source_censuses[1],2,2,1,1);
  R.native_short_mask_frontiers.forEach((F,i)=>checkFrontier(F,[8,16,32,64,128][i]));
  const s=R.scope;
  need(s.relation==="A(y-x)=0 in Z4^n, not one cyclic integer congruence"&&
       s.coarse_only_fresh_higher_label_law_applies_with_fresh_batches===true,"vector source premise");
  ["full_higher_labels_are_program_inputs","sorting_network_gate_export_implemented","coherent_RAM_assumed",
   "polynomial_time_or_coherent_space_claimed","constant_mean_coverage_and_visibility_implies_scalable_decoder",
   "natural_source_noise_or_hardness_certified","improves_known_DCP_time_query_tradeoff"].forEach(k=>need(s[k]===false,"scope expansion: "+k));
  need(same(R.literature,["https://arxiv.org/abs/1207.2307","https://arxiv.org/abs/2206.14408"]),"prior baseline references");
  return{status:"ok",finite_vector_controls:6,complete_source_censuses:2,native_frontiers:5,polynomial_time_claimed:false};
}
module.exports={verify};
if(require.main===module){const file=process.argv[2]||path.resolve(__dirname,"../phase_workbench/dcp_vector_short_mask_join.json");console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(file,"utf8")))));}
