"use strict";
// Independent original-digit MITM fiber checks and integer dual certificates.
const fs=require("fs"), path=require("path");
const load=name=>JSON.parse(fs.readFileSync(path.join(__dirname,"../phase_workbench/"+name+".json"),"utf8"));
const source=load("ternary_pair_cell_coverage"), report=load("ternary_adaptive_shell");
const dualPath=path.join(__dirname,"../phase_workbench/ternary_native_dual_separation.json");
const dual=fs.existsSync(dualPath)?JSON.parse(fs.readFileSync(dualPath,"utf8")):null;
function check(x,m) { if(!x)throw Error(m); }
const abs=x=>x<0n?-x:x;
function gcd(a,b) { a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a; }
const mod=(a,q)=>(a%q+q)%q;
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0n);
function integer(x) { if(typeof x==="number")check(Number.isSafeInteger(x),"lossless integer certificate");return BigInt(x); }
function inverse(a,q) { if(q===1n)return 0n;let [r,s,x,y]=[q,a,0n,1n];while(s){const k=r/s;[r,s,x,y]=[s,r-k*s,y,x-k*y];}check(r===1n,"unit inverse");return mod(x,q); }
function enumerate(A,Q) {
  const M=A.length/2, N=3**M, result=[];
  for(let k=0;k<N;k++) {
    let number=k, value=0n;const word=[];
    for(let j=0;j<M;j++){const x=number%3;number=Math.floor(number/3);word.push(x);if(x)value+=A[2*j+x-1];}
    result.push({word,value:mod(value,Q)});
  }
  return result;
}
let referenceAssignments=0, trials=0, completeFibers=0, acceptedWords=0, separators=0, skippedReferenceCases=0;
function prepare(c) {
  const original=source.planted_geometry_probes[c.fixture_probe_index];
  check(JSON.stringify(c.labels)===JSON.stringify(original.labels)&&c.Q===original.modulus,"frozen native source");
  const A=c.labels.map(BigInt), Q=BigInt(c.Q), M=A.length/2, basis=original.prepared.bases[0];
  const rows=basis.rows.map(r=>r.map(BigInt));
  check(rows.length===2*M&&rows.every(row=>row.length===3*M&&row.every(x=>x%3n===0n)),"full integer embedded row shape");
  for(const row of rows)for(let j=0;j<M;j++)check(row[3*j]+row[3*j+1]+row[3*j+2]===0n,"original A2 row plane");
  const G=A.reduce((g,a)=>gcd(g,a),Q), q=Q/G, pivot=A.findIndex(a=>gcd(a/G,q)===1n), inv=inverse(A[pivot]/G,q);
  let reference=null;
  if(3**Math.ceil(M/2)<=10000) {
    const middle=Math.floor(M/2), left=enumerate(A.slice(0,2*middle),Q), right=enumerate(A.slice(2*middle),Q), map=new Map();
    for(const w of left){const key=String(w.value), bucket=map.get(key)||[];bucket.push(w.word);map.set(key,bucket);}
    referenceAssignments+=left.length+right.length;reference={map,right};
  } else skippedReferenceCases++;
  return {A,Q,M,rows,G,q,pivot,inv,reference};
}
function validateTrial(c,t,geometry) {
  const {A,Q,M,rows,G,q,pivot,inv,reference}=geometry, target=BigInt(t.target);
  const z0=Array(2*M).fill(0n);z0[pivot]=mod((target/G)*inv,q);
  const T=Array.from({length:M},(_,j)=>[2n-3n*(z0[2*j]+z0[2*j+1]),-1n+3n*z0[2*j],-1n+3n*z0[2*j+1]]).flat();
  const words=t.witnesses, set=new Set(words.map(w=>JSON.stringify(w)));
  check(set.size===words.length,"distinct actual words");
  check(JSON.stringify(t.traces.map(trace=>trace.word))===JSON.stringify(words),"trace/witness identity");
  check(JSON.stringify(t.pair)===JSON.stringify(words.length>=2?words.slice(0,2):[]),"pair/witness identity");
  check(t.cost.coefficient_nodes<=t.node_budget&&t.cost.coefficient_nodes===t.cost.nodes_by_row.reduce((a,b)=>a+b,0),"all coefficient nodes charged");
  check(t.cost.training_words===0&&t.cost.original_lll_preparations_per_fresh_labels===2,"native access/preparation accounting");
  check(!t.status.startsWith("NODE_CAP")||!t.complete_fiber,"caps cannot certify complete/empty fibers");
  for(const trace of t.traces) {
    const coeff=trace.reduced_basis_coefficients.map(integer), z=[];
    for(let j=0;j<M;j++) {
      z.push(z0[2*j]-coeff.reduce((s,x,i)=>s+x*rows[i][3*j+1]/3n,0n));
      z.push(z0[2*j+1]-coeff.reduce((s,x,i)=>s+x*rows[i][3*j+2]/3n,0n));
    }
    check(z.map(String).join(",")===trace.integer_coset_coordinates.map(String).join(","),"integer coset trace");
    const word=z.filter((x,i)=>i%2===0).map((a,j)=>a===1n&&z[2*j+1]===0n?1:a===0n&&z[2*j+1]===1n?2:a===0n&&z[2*j+1]===0n?0:-1);
    check(!word.includes(-1)&&JSON.stringify(word)===JSON.stringify(trace.word),"original native one-hot shell");
    check(mod(word.reduce((s,x,j)=>s+(x?A[2*j+x-1]:0n),0n),Q)===target,"original modular target");
    check(trace.exact_original_norm===String(6*M),"native shell norm");acceptedWords++;
  }
  check(t.traces.length===words.length&&Boolean(t.pair.length)===(words.length>=2),"pair versus witness ledger");
  if(reference) {
    const actual=[];
    for(const w of reference.right)for(const prefix of reference.map.get(String(mod(target-w.value,Q)))||[])actual.push([...prefix,...w.word]);
    if(t.complete_fiber) {
      check(actual.length===words.length&&actual.every(w=>set.has(JSON.stringify(w))),"complete real fiber independently checked by MITM");completeFibers++;
    }
  } else check(!t.complete_fiber,"unaccounted complete fiber needs an independent reference");
  for(const cert of t.dual_certificates||[]) {
    const h=cert.integer_direction.map(BigInt), coeff=cert.partial_coefficients.map(integer), bottom=cert.unassigned_row_count;
    check(h.length===3*M&&coeff.length===2*M&&Number.isInteger(bottom)&&bottom>=0&&bottom<=2*M,"integer separator shape");
    for(let j=0;j<M;j++)check(h[3*j]+h[3*j+1]+h[3*j+2]===0n,"dual native planes");
    for(const row of rows.slice(0,bottom))check(dot(h,row)===0n,"dual annihilates every unassigned row");
    const H=T.map((x,k)=>x-coeff.slice(bottom).reduce((s,a,j)=>s+a*rows[bottom+j][k],0n));
    const lhs=dot(H,h);let rhs=0n;
    for(let j=0;j<M;j++)rhs+=3n*h.slice(3*j,3*j+3).reduce((a,b)=>a>b?a:b);
    check(lhs>rhs&&String(lhs)===cert.exact_branch_inner&&String(rhs)===cert.exact_native_support&&String(lhs-rhs)===cert.strict_margin,"strict exact joint-prefix separator");separators++;
  }
  check((t.dual_certificates||[]).length===(t.cost.dual_separator_prunes||0),"all strict separator prunes recorded");
  if(t.dual_search_cap!==undefined)check(t.cost.dual_search_calls<=t.dual_search_cap,"charged separator search cap");
  trials++;
}
for(const c of report.cases){const geometry=prepare(c);for(const t of c.trials)validateTrial(c,t,geometry);}
if(dual)for(const c of dual.cases){const geometry=prepare(c);for(const t of c.trials)validateTrial(c,t,geometry);}
check(!report.polynomial_pair_finder_proved&&!report.population_coverage_proved&&!report.novelty_claim,"no speedup promotion");
console.log(JSON.stringify({status:"independent_native_fiber_and_dual_certificate_checks_passed",trials,completeFibers,acceptedWords,separators,
  referenceAssignments,skippedReferenceCases,fullEnumerationTreeReplayed:false,sourcePopulationGuarantee:false}));
