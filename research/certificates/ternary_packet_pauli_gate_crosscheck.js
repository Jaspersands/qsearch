"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const report=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../phase_workbench/ternary_packet_pauli_gate.json"),"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},same=(a,b,m)=>check(JSON.stringify(a)===JSON.stringify(b),m),mod=(a,q)=>(a%q+q)%q;
const words=k=>Array.from({length:3**k},(_,i)=>Array.from({length:k},(_,j)=>Math.floor(i/3**(k-j-1))%3));
function gcd(a,b){while(b)[a,b]=[b,a%b];return a<0n?-a:a;}
function frac(a,b){const g=gcd(a,b);a/=g;b/=g;return b===1n?String(a):a+"/"+b;}
function binom(n,k){let v=1n;for(let i=1;i<=k;i++)v=v*BigInt(n-i+1)/BigInt(i);return v;}
function rref(matrix){
  const A=matrix.map(row=>row.map(x=>mod(x,3))),pivots=[];let r=0;
  for(let j=0;j<A[0].length&&r<A.length;j++){
    const k=A.findIndex((row,i)=>i>=r&&row[j]);if(k<0)continue;
    [A[r],A[k]]=[A[k],A[r]];const inverse=A[r][j];A[r]=A[r].map(a=>a*inverse%3);
    for(let i=0;i<A.length;i++)if(i!==r){const f=A[i][j];A[i]=A[i].map((a,k)=>mod(a-f*A[r][k],3));}
    pivots.push(j);r++;
  }
  return{rows:A.slice(0,r),pivots,free:Array.from({length:A[0].length},(_,j)=>j).filter(j=>!pivots.includes(j))};
}
function geometry(low,syndrome){
  const R=rref([low]),h=R.free.length,K=low.length;
  check(syndrome.length===R.pivots.length,"actual measured syndrome shape");
  const assignment=z=>{
    const t=Array(K).fill(0);R.free.forEach((f,j)=>t[f]=z[j]);
    R.pivots.forEach((p,j)=>t[p]=mod(syndrome[j]-R.free.reduce((s,f)=>s+R.rows[j][f]*t[f],0),3));return t;
  };
  const base=assignment(Array(h).fill(0)),D=Array.from({length:K},()=>[]);
  for(let j=0;j<h;j++){const e=Array(h).fill(0);e[j]=1;const t=assignment(e);for(let i=0;i<K;i++)D[i].push(mod(t[i]-base[i],3));}
  return{R,h,K,D,assignment};
}
function rank(rows){return rows.length?rref(rows).pivots.length:0;}
function nativePair(label){
  // Derive q*beta at L3 from pi^2, rather than using reported frequencies.
  let V=[[1n,0n],[0n,1n]],pi=[[-1n,-1n],[1n,-2n]];
  for(let i=0;i<2;i++)V=V.map(row=>pi[0].map((_,j)=>row.reduce((s,a,k)=>s+a*pi[k][j],0n)));
  const den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]),u=9n*(2n*V[1][1]+V[1][0])/den,v=9n*(-2n*V[0][1]-V[0][0])/den;
  const[x,y]=label.map(BigInt);return[Number(mod(u*x+v*y,9n)),Number(mod((u+v)*x-u*y,9n))];
}
function checkProbe(g,p){
  const v=p.logical_translation,w=p.logical_diagonal;
  check(v.length===g.h&&w.length===g.h&&v.some(Boolean)&&[...v,...w].every(a=>Number.isInteger(a)&&a>=0&&a<3),"nontrivial canonical Pauli");
  const physical=g.D.map(row=>mod(row.reduce((s,a,j)=>s+a*v[j],0),3)),S=physical.flatMap((a,i)=>a?[i]:[]),rows=S.map(i=>g.D[i]);
  const b=rank(rows),inSpan=rank([...rows,w])===b;
  same(p.physical_translation,physical,"actual kernel physical translation");same(p.translated_physical_support,S,"actual translated coordinates");
  check(p.restricted_kernel_frame_rank===b&&p.diagonal_in_restricted_row_span===inSpan&&p.conditional_high_lift_squared_overlap_mean===(inSpan?frac(1n,3n**BigInt(b)):"0"),"restricted rank, not Hamming weight, controls exact moment");
  check(p.outside_span_overlap_identically_zero_for_each_high_lift===!inSpan&&p.conditioned_low_frame_and_syndrome===true&&p.nonzero_residual_secret_required===true&&p.probe_choice_low_only_policy_verified_by_this_function===false&&p.general_collective_receiver_or_high_informed_search_excluded===false,"conditional low-defined scope and nonzero-secret exception");
  return{v,w,b,inSpan};
}
const hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../TERNARY_PACKET_PAULI_GATE.md"))).digest("hex");
check(report.derivation_sha256===hash&&report.status==="CORRELATED_PACKET_LOW_DEFINED_PAULI_VISIBILITY_GATE_REVIEW_PENDING","pinned derivation");
for(const k of["candidate_record_accepted","general_receiver_no_go_claimed","quantum_speedup_proved"])check(report[k]===false,"scoped gate, not generic lower bound: "+k);
const schedule=[[[1,1,1],[1,0],[0,0]],[[1,1,0],[1,0],[0,0]],[[1,1,0],[1,0],[0,1]]];
check(report.complete_conditional_censuses.length===3,"complete specified censuses");
let highCount=0,characterPairs=0;
report.complete_conditional_censuses.forEach((c,index)=>{
  const[low,v,w]=schedule[index];same(c.low_first_frequency_rows,low,"conditional source strata");same(c.syndrome,[1],"nonzero observed syndrome");
  same(c.probe.logical_translation,v,"chosen logical translation");same(c.probe.logical_diagonal,w,"chosen logical character");
  c.prototype_native_labels.forEach((row,i)=>{same(nativePair(row[0]),[low[i],2*low[i]%3],"actual native odd chart");check((row[0][0]+row[0][1])%3===low[i],"actual odd residue");});
  const g=geometry(low,c.syndrome),p=checkProbe(g,c.probe),points=words(g.h),hist=[0,0,0],tables=[];let maximum=0;
  same(c.kernel_frame,g.D,"kernel generator reconstructed from actual low matrix");
  for(const high of words(2*g.K)){
    const pairs=low.map((a,i)=>[a+3*high[2*i],2*a%3+3*high[2*i+1]]),phase=[];
    for(const z of points){
      const t=g.assignment(z),target=g.assignment(z.map((a,j)=>(a+v[j])%3));
      const diff=mod(t.reduce((s,a,i)=>s+(target[i]?pairs[i][target[i]-1]:0)-(a?pairs[i][a-1]:0),0),9);
      check(diff%3===0,"true original-root derivative divisibility");
      phase.push(mod(diff/3+w.reduce((s,a,j)=>s+a*z[j],0),3));
    }
    tables.push(phase);for(const a of phase)for(const b of phase)hist[mod(a-b,3)]++;
    const re=phase.reduce((s,a)=>s+Math.cos(2*Math.PI*a/3),0)/phase.length,im=phase.reduce((s,a)=>s+Math.sin(2*Math.PI*a/3),0)/phase.length;
    maximum=Math.max(maximum,Math.hypot(re,im));
  }
  const denominator=tables.length*points.length**2;
  same(c.exact_character_difference_histogram,hist,"complete exact character histogram");
  check(hist[1]===hist[2]&&c.character_average_denominator===denominator&&c.exact_squared_overlap_mean===frac(BigInt(hist[0]-hist[2]),BigInt(denominator))&&c.exact_squared_overlap_mean===(p.inSpan?frac(1n,3n**BigInt(p.b)):"0"),"exact rational moment without fitting");
  check(c.complete_high_lift_assignments===729&&c.logical_words_per_lift===9&&c.all_phase_tables_sha256===crypto.createHash("sha256").update(JSON.stringify(tables)).digest("hex"),"all actual native high-lift phase tables");
  check(Number.isFinite(c.maximum_single_lift_overlap_magnitude)&&Math.abs(maximum-c.maximum_single_lift_overlap_magnitude)<4e-12&&(!p.inSpan?maximum<4e-12:true),"each forbidden character is zero, not just the mean");
  check(c.identical_packet_factory_supplied===false&&c.quantum_speedup_proved===false,"conditional census is not a quantum source factory");
  highCount+=tables.length;characterPairs+=denominator;
});
check(report.complete_small_low_matrix_distance_controls.length===27,"all small low matrices");
let directions=0;
report.complete_small_low_matrix_distance_controls.forEach((c,index)=>{
  const low=words(3)[index],R=rref([low]),g=geometry(low,Array(R.pivots.length).fill(0));
  check(c.odd_level===3,"actual native level");c.native_labels.forEach((row,i)=>same(nativePair(row[0]),[low[i],2*low[i]%3],"native small distance source"));
  same(c.syndrome,Array(R.pivots.length).fill(0),"small distance frame");same(c.RREF_rows,R.rows,"dual code");same(c.kernel_frame,g.D,"primal generator");
  const vv=words(g.h).filter(v=>v.some(Boolean)),physical=vv.map(v=>g.D.map(row=>mod(row.reduce((s,a,j)=>s+a*v[j],0),3))),primal=Math.min(...physical.map(row=>row.filter(Boolean).length));
  const dualWords=words(R.pivots.length).filter(v=>v.some(Boolean)).map(v=>Array.from({length:3},(_,i)=>mod(R.rows.reduce((s,row,j)=>s+v[j]*row[i],0),3))),dual=dualWords.length?Math.min(...dualWords.map(row=>row.filter(Boolean).length)):4;
  const ranks=physical.map(t=>rank(t.flatMap((a,i)=>a?[g.D[i]]:[]))),bound=Math.min(primal,dual-1);
  check(ranks.every(b=>b>=bound)&&c.primal_minimum_distance===primal&&c.dual_minimum_distance_or_K_plus_one===dual&&c.all_nonzero_translation_rank_lower_bound===bound&&c.exact_minimum_translation_rank===Math.min(...ranks)&&c.all_logical_directions_checked===vv.length,"all directions obey dual-distance projection bound");
  check(c.distance_enumeration_is_scalable_algorithm===false,"finite code distances, not a scalable solver");directions+=vv.length;
});
same(report.analytic_population_envelopes.map(c=>c.dimension),[32,64,128,256,1024],"prespecified analytic population schedule");
for(const c of report.analytic_population_envelopes){
  const n=c.dimension,K=2*n,d=n/8,T=n*n;let U=0n;
  for(let j=1;j<d;j++)U+=binom(K,j)*2n**BigInt(j-1);
  const N=3n**BigInt(n),P=3n**BigInt(K),B=3n**BigInt(d-1),primal=frac(U,N),dual=frac((N-1n)*U,P),badNum=U*P+(N-1n)*U*N,badDen=N*P;
  const goodNum=BigInt(T)>B?B:BigInt(T),rawDen=badDen*B,unclippedRaw=badNum*B+goodNum*badDen,rawNum=unclippedRaw>rawDen?rawDen:unclippedRaw;
  check(c.odd_input_count===K&&c.distance_threshold===d&&c.minimum_restricted_rank_on_good_sources===d-1&&c.low_defined_menu_size===T,"constant-rate source and polynomial menu");
  check(c.primal_distance_failure_union_bound===primal&&c.dual_distance_failure_union_bound===dual&&c.combined_bad_low_source_probability_upper===frac(badNum,badDen)&&c.good_source_menu_squared_overlap_mean_upper===frac(goodNum,B)&&c.raw_population_menu_squared_overlap_mean_upper===frac(rawNum,rawDen)&&c.one_Pauli_test_mean_total_variation_to_unbiased_upper_squared===frac(rawNum,4n*rawDen),"exact unconditional source tails and raw menu costs");
  check(c.fresh_B_packet_transcript_TV_upper_squared_before_clipping==="B^2*raw_bound/4"&&c.full_row_rank_conditioning_assumed===false&&c.menu_can_be_selected_from_high_labels_after_low_only_definition===true&&c.implicit_high_informed_exponential_probe_families_covered===false&&c.multiple_noncommuting_measurements_on_same_packet_covered===false&&c.generic_quantum_complexity_lower_bound===false,"one fresh Pauli test per packet, no overbroad transcript claim");
}
console.log(JSON.stringify({status:"independent_packet_pauli_gate_certificates_passed",completeHighLiftAssignments:highCount,exactCharacterPairs:characterPairs,completeLowMatrices:27,nonzeroLogicalDirections:directions,populationEnvelopes:5,generalReceiverNoGo:false}));
