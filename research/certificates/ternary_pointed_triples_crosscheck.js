"use strict";
// Native integer frequency recurrence, direct GF3 elimination and exact covers.
const fs=require("fs"),path=require("path");
const report=JSON.parse(fs.readFileSync(path.join(__dirname,"../phase_workbench/ternary_pointed_triples.json"),"utf8"));
function check(x,message){if(!x)throw Error(message);}
function same(x,y,message){check(JSON.stringify(x)===JSON.stringify(y),message);}
function mod(x,q=3){return((x%q)+q)%q;}
function freq(y,L){
  let [u,v]=L%2?[2,-1]:[-1,1];for(let level=L%2?1:2;level<L;level+=2)[u,v]=[u+v,-u];
  const q=3**Math.ceil(L/2);return[mod(u*y[0]+v*y[1],q),mod((u+v)*y[0]-u*y[1],q)];
}
function native(labels,L){return labels.map(row=>{const pairs=row.map(y=>freq(y,L));return[0,1].map(j=>pairs.map(p=>p[j]));});}
function words(m){return Array.from({length:3**m},(_,i)=>Array.from({length:m},(_,j)=>Math.floor(i/3**(m-j-1))%3));}
function rref(A){
  const B=A.map(row=>row.map(x=>mod(x))),pivots=[];let r=0;
  for(let j=0;j<B[0].length&&r<B.length;j++){
    let k=r;while(k<B.length&&!B[k][j])k++;if(k===B.length)continue;
    [B[r],B[k]]=[B[k],B[r]];const inverse=B[r][j];B[r]=B[r].map(x=>mod(x*inverse));
    for(let i=0;i<B.length;i++)if(i!==r){const c=B[i][j];B[i]=B[i].map((x,k)=>mod(x-c*B[r][k]));}
    pivots.push(j);r++;
  }return{rows:B.slice(0,r),pivots};
}
function pointed(F,x){
  const n=F[0][0].length,m=x.length,D=x.map((a,i)=>Array.from({length:n},(_,l)=>mod((a===2?0:F[i][a][l])-(a===0?0:F[i][a-1][l]))));
  const reduced=rref(Array.from({length:n},(_,l)=>D.map(row=>row[l]))),free=Array.from({length:m},(_,i)=>i).filter(i=>!reduced.pivots.includes(i)),w=Array(m).fill(0);
  w[free[0]]=w[free[1]]=1;reduced.pivots.forEach((p,i)=>w[p]=mod(-reduced.rows[i][free[0]]-reduced.rows[i][free[1]]));
  const p=w.indexOf(1),u=w.map((a,i)=>Number(a===2||(a===1&&i===p))),v=w.map((a,i)=>Number(a===2||(a===1&&i!==p)));
  return{words:[x,x.map((a,i)=>mod(a+u[i])),x.map((a,i)=>mod(a+v[i]))],w,free,pivots:reduced.pivots};
}
function value(F,x,q){return F[0][0].map((_,l)=>mod(x.reduce((s,j,i)=>s+(j?F[i][j-1][l]:0),0),q));}
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
function rational(a,b=1n){const d=gcd(a,b);return[a/d,b/d];}
function parse(s){const t=s.split("/").map(BigInt);return[t[0],t[1]||1n];}
function add(a,b){return rational(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function compare(a,b){const x=a[0]*b[1]-b[0]*a[1];return x<0n?-1:x>0n?1:0;}
function sameFraction(a,b,message){check(compare(a,b)===0,message);}
let anchorTriples=0,coverEdges=0,rationalConstraints=0,rootComponents=0;
for(const c of report.explicit_cover_controls){
  const F=native(c.native_labels,c.native_level),points=words(c.input_qutrits),index=new Map(points.map((x,i)=>[x.join(","),i])),oriented=points.map(x=>pointed(F,x).words.map(w=>index.get(w.join(","))));
  same(oriented,c.pointed_oriented_edges,"pointed native elimination");check(points.length===c.physical_words_enumerated,"hidden source filter");
  const edgeMap=new Map();for(const edge of oriented){
    check(new Set(edge).size===3,"duplicate corner");const values=edge.map(v=>value(F,points[v],3));
    check(F[0][0].every((_,l)=>mod(values.reduce((s,row)=>s+row[l],0))===0),"native component low zero sum");
    const sorted=[...edge].sort((a,b)=>a-b);edgeMap.set(sorted.join(","),sorted);anchorTriples++;
  }
  const degrees=Array(points.length).fill(0);for(const edge of edgeMap.values())edge.forEach(v=>degrees[v]++);
  check(edgeMap.size===c.distinct_three_word_edges && Math.max(...degrees)===c.maximum_incidence_degree,"native cover degrees");
  if(c.endpoint_collision_anchor_ids){const [a,b,y]=c.endpoint_collision_anchor_ids;check(a!==b&&oriented[a][1]===y&&oriented[b][1]===y,"nonunitary pointer witness");}
  if(!c.edge_records)continue;
  const loads=Array.from({length:points.length},()=>[0n,1n]),prices=c.dual_vertex_prices.map(parse);let mass=[0n,1n],dual=[0n,1n];
  prices.forEach(p=>dual=add(dual,p));
  for(const edge of c.edge_records){
    check(edgeMap.has(edge.vertex_ids.join(",")),"edge not in pointed cover");const w=parse(edge.Kraus_weight);check(w[0]>=0n,"negative effect");mass=add(mass,w);
    let price=[0n,1n];edge.vertex_ids.forEach(v=>{loads[v]=add(loads[v],w);price=add(price,prices[v]);});
    check(compare(price,[1n,1n])>=0,"invalid rational dual");rationalConstraints++;
    const full=edge.vertex_ids.map(v=>value(F,points[v],3**(c.native_level/2))),q=3**(c.native_level/2);
    const a=full[1].map((x,l)=>mod(x-full[0][l],q)),b=full[2].map((x,l)=>mod(x-full[0][l],q));
    same(a,edge.relative_first,"full root first frequency");same(b,edge.relative_second,"full root second frequency");
    edge.native_odd_output_labels.forEach((y,l)=>{same(freq(y,c.native_level-1),[a[l],b[l]],"native odd output chart");rootComponents++;});
    coverEdges++;
  }
  loads.forEach(v=>{check(compare(v,[1n,1n])<=0,"invalid primal or missing failure effect");rationalConstraints++;});
  sameFraction(parse(c.exact_implemented_acceptance),rational(3n*mass[0],BigInt(points.length)*mass[1]),"flat source branch mass");
  const upper=rational(3n*dual[0],BigInt(points.length)*dual[1]);sameFraction(parse(c.exact_cover_acceptance_upper),compare(upper,[1n,1n])>0?[1n,1n]:upper,"dual source mass");
  check(!c.uniform_scalable_cover_compiler_supplied && !c.accepted_native_IID_low_source_transfer_proved,"reference LP promoted");
}
for(const c of report.growing_root_pointed_outputs){
  const F=native(c.native_labels,c.even_parent_level),p=pointed(F,c.words[0]);same(c.words,p.words,"deep native pointed witnesses");same(c.kernel_word,p.w,"deep kernel relation");
  const values=c.words.map(w=>value(F,w,c.phase_modulus)),a=values[1].map((x,l)=>mod(x-values[0][l],c.phase_modulus)),b=values[2].map((x,l)=>mod(x-values[0][l],c.phase_modulus));
  same(c.relative_first,a,"deep first");same(c.relative_second,b,"deep second");
  c.native_odd_output_labels.forEach((y,l)=>{same(freq(y,c.odd_output_level),[a[l],b[l]],"deep actual native chart");rootComponents++;});
  check(c.phase_modulus===3**(c.even_parent_level/2)&&!c.pointed_witness_is_a_quantum_receiver,"field replacement or receiver promotion");
}
for(const c of report.uniform_anchor_source_ledgers){
  const m=BigInt(c.even_native_input_width),n=BigInt(c.dimension),pairs=(2n**m-1n)*(2n**m-2n),b=rational(pairs,3n**(2n*n)),e=[1n,3n**n];
  sameFraction(parse(c.uniform_anchor_zero_low_output_probability_upper),compare(b,[1n,1n])>0?[1n,1n]:b,"mask source union bound");
  check(!c.coherent_pointed_cover_compiler_supplied,"pointed source promoted");
}
for(const c of report.conditional_inverse_geometry_ledgers){
  const m=BigInt(c.physical_width),C=m*m*(m-1n)/2n,B=(1n+2n*C)*(1n+4n*C),cap=(36n*B+16n)/17n;
  check(BigInt(c.full_rank_inverse_cases_per_endpoint_upper)===C&&BigInt(c.full_rank_anchored_incidence_degree_second_moment_upper)===B,"inverse case geometry");
  check(BigInt(c.theoretical_degree_truncation_cap)===cap,"degree cap");
  sameFraction(parse(c.native_average_truncated_cover_acceptance_lower),[17n,12n*cap],"source acceptance theorem");
  check(c.requires_complete_coherent_incoming_enumerator&&!c.geometry_bound_is_efficient_quantum_compiler&&!c.one_output_per_n_plus2_stage_closes_full_recursion,"conditional geometry promoted");
}
check(Object.values(report.claim_gate).every(v=>v===false),"new algorithm claim");
console.log(JSON.stringify({status:"independent_replay_passed",native_pointed_anchor_triples:anchorTriples,
  rational_cover_edges:coverEdges,exact_primal_dual_constraints:rationalConstraints,
  native_full_root_components:rootComponents,efficient_coherent_extractor:false}));
