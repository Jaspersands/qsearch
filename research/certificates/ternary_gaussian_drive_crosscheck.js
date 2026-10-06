"use strict";
// Independent GF3 elimination, native chart, graph census and phase replay.
const fs = require("fs"), path = require("path");
const report = JSON.parse(fs.readFileSync(path.join(__dirname, "../phase_workbench/ternary_gaussian_drive.json"), "utf8"));
const check = (x, message) => { if (!x) throw Error(message); };
const same = (a, b, message) => check(JSON.stringify(a) === JSON.stringify(b), message);
const mod = (x, q = 3) => ((x % q) + q) % q;
function words(m, q = 3) {
  return Array.from({length: q**m}, (_, i) => Array.from({length: m}, (_, j) => Math.floor(i/q**(m-j-1))%q));
}
function native(labels, L) {
  let [u, v] = [-1, 1];
  for (let j = 2; j < L; j += 2) [u, v] = [u+v, -u];
  const q = 3**(L/2);
  return labels.map(row => {
    const pairs = row.map(([a,b]) => [mod(u*a+v*b,q), mod((u+v)*a-u*b,q)]);
    return [0,1].map(j => pairs.map(pair => pair[j]));
  });
}
function rref(A) {
  const B = A.map(row => row.map(x => mod(x))), pivots = [];
  let r = 0;
  for (let j = 0; j < B[0].length && r < B.length; j++) {
    let k = r;
    while (k < B.length && !B[k][j]) k++;
    if (k === B.length) continue;
    [B[r], B[k]] = [B[k], B[r]];
    const inverse = B[r][j];
    B[r] = B[r].map(x => mod(x*inverse));
    for (let i = 0; i < B.length; i++) if (i !== r) {
      const c = B[i][j]; B[i] = B[i].map((x,l) => mod(x-c*B[r][l]));
    }
    pivots.push(j); r++;
  }
  return {rows:B, pivots};
}
function table(F,i,j) { return j ? F[i][j-1] : F[i][0].map(() => 0); }
function difference(F,i,x,previous) {
  const a = table(F,i,previous?x:mod(x+1)), b = table(F,i,previous?mod(x-1):x);
  return a.map((v,l) => mod(v-b[l]));
}
function pointed(F,x) {
  const n = F[0][0].length, m = x.length;
  const columns = x.map((v,i) => difference(F,i,v,false));
  const reduced = rref(Array.from({length:n},(_,l) => columns.map(v => v[l])));
  const free = Array.from({length:m},(_,i) => i).filter(i => !reduced.pivots.includes(i)), w = Array(m).fill(0);
  w[free[0]] = w[free[1]] = 1;
  reduced.pivots.forEach((p,i) => w[p] = mod(-reduced.rows[i][free[0]]-reduced.rows[i][free[1]]));
  const p = w.indexOf(1), z = x.map((a,i) => mod(a+Number(w[i]===2 || (w[i]===1 && i!==p))));
  return {p,w,z,free,pivots:reduced.pivots};
}
function capFor(n) { let b=0; while(3**b<n+2)b++; return b; }
function outgoing(F,x,cap) {
  const n=F[0][0].length, a=pointed(F,x);
  if(a.pivots.length!==n)return null;
  const variables=a.pivots.filter(i=>i!==a.p);
  const rank=variables.length?rref(Array.from({length:n},(_,l)=>variables.map(i=>difference(F,i,a.z[i],true)[l]))).pivots.length:0;
  return variables.length-rank>cap?null:a.z;
}
function incoming(F,z,cap) {
  const n=F[0][0].length,m=z.length, found=new Map();
  for(let f=0;f<m;f++)for(let g=f+1;g<m;g++) {
    const free=[f,g],pivots=Array.from({length:m},(_,i)=>i).filter(i=>i!==f&&i!==g);
    for(const p of [...pivots.filter(i=>i<f),f]) {
      const vars=pivots.filter(i=>i!==p),k=vars.length;
      const columns=vars.map(i=>difference(F,i,z[i],true));
      const fixed=free.map(i=>difference(F,i,z[i],i!==p));
      if(pivots.includes(p))fixed.push(difference(F,p,z[p],false));
      const target=Array.from({length:n},(_,l)=>mod(-fixed.reduce((s,v)=>s+v[l],0)));
      const rank=k?rref(Array.from({length:n},(_,l)=>columns.map(v=>v[l]))).pivots.length:0;
      if(k-rank>cap)continue;
      const aug=rref(Array.from({length:n},(_,l)=>[...columns.map(v=>v[l]),target[l]]));
      if(aug.pivots.includes(k))continue;
      const unknownFree=Array.from({length:k},(_,i)=>i).filter(i=>!aug.pivots.includes(i));
      for(const coefficients of words(unknownFree.length)) {
        const c=Array(k).fill(0);
        unknownFree.forEach((j,i)=>c[j]=coefficients[i]);
        aug.pivots.forEach((j,i)=>c[j]=mod(aug.rows[i][k]-unknownFree.reduce((s,l)=>s+aug.rows[i][l]*c[l],0)));
        if(vars.some((j,i)=>j<p&&c[i]===1))continue;
        const w=Array(m).fill(0);w[f]=w[g]=w[p]=1;vars.forEach((j,i)=>w[j]=c[i]);
        const x=z.map((a,i)=>mod(a-Number(w[i]===2||(w[i]===1&&i!==p)))), actual=pointed(F,x);
        if(JSON.stringify(actual.w)!==JSON.stringify(w)||JSON.stringify(actual.free)!==JSON.stringify(free)
          ||JSON.stringify(actual.z)!==JSON.stringify(z))continue;
        found.set(x.join(","),x);
      }
    }
  }
  return [...found.values()].sort((a,b)=>a.join(",").localeCompare(b.join(",")));
}
function rowFromArcs(points, arcs, vertex) {
  const row=new Map(),key=vertex.join(",");
  function increment(word,amount){const k=word.join(",");row.set(k,(row.get(k)||0)+amount);}
  arcs.forEach((z,i)=>{if(!z)return;if(points[i].join(",")===key){increment(z,-1);increment(vertex,1);}
    if(z.join(",")===key){increment(points[i],-1);increment(vertex,1);}});
  return [...row].filter(([,w])=>w).sort().map(([k,w])=>[k.split(",").map(Number),w]);
}
function components(points,arcs) {
  const index=new Map(points.map((x,i)=>[x.join(","),i])),parent=points.map((_,i)=>i);
  function root(i){while(parent[i]!==i)i=parent[i];return i;}
  arcs.forEach((z,i)=>{if(z)parent[root(i)]=root(index.get(z.join(",")));});
  const groups=new Map();points.forEach((x,i)=>{const k=root(i);if(!groups.has(k))groups.set(k,[]);groups.get(k).push(x);});
  return [...groups.values()];
}
function value(F,x,q){return F[0][0].map((_,l)=>mod(x.reduce((s,j,i)=>s+(j?F[i][j-1][l]:0),0),q));}
function countValues(F,points,q){const counts=new Map();points.forEach(x=>{const k=value(F,x,q).join(",");counts.set(k,(counts.get(k)||0)+1);});return[...counts.values()];}
function evolve(rows,re,im,t) {
  const D=re.length,steps=32,dt=t/steps;
  for(let step=0;step<steps;step++) {
    let tr=re.slice(),ti=im.slice();const outR=re.slice(),outI=im.slice();
    for(let k=1;k<=24;k++) {
      const nr=new Float64Array(D),ni=new Float64Array(D);
      rows.forEach((row,j)=>row.forEach(([a,w])=>{nr[j]+=dt*w*ti[a]/k;ni[j]-=dt*w*tr[a]/k;}));
      for(let j=0;j<D;j++){outR[j]+=nr[j];outI[j]+=ni[j];}
      tr=nr;ti=ni;
    }
    re=outR;im=outI;
  }
  return [re,im];
}
let sparseRows=0,nativeComponents=0,readoutSecrets=0;
for(const c of report.native_readout_calibrations) {
  const F=native(c.native_labels,c.native_level),width=c.dimension+2,q=c.modulus,points=words(width),D=points.length;
  const blocks=Array.from({length:c.block_count},(_,b)=>F.slice(b*width,(b+1)*width));
  blocks.forEach((B,b)=>{
    const arcs=points.map(x=>outgoing(B,x,capFor(c.dimension)));
    check(arcs.filter(Boolean).length===c.retained_directed_arcs_per_block[b],"native arc count");
    points.forEach((x,i)=>{same(rowFromArcs(points,arcs,x),c.block_sparse_row_certificates[b*D+i],"complete native sparse row");sparseRows++;});
  });
  const joint=words(c.physical_qutrits),counts=countValues(F,joint,q);
  const pgm=counts.reduce((s,k)=>s+Math.sqrt(k/joint.length),0)**2/c.secret_count;
  check(Math.abs(pgm-c.known_optimal_PGM_reference_full_secret_success)<1e-11,"full native PGM reference");
  const componentBlocks=blocks.map(B=>components(points,points.map(x=>outgoing(B,x,capFor(c.dimension)))));
  let jointGroups=[[]];for(const groups of componentBlocks)jointGroups=jointGroups.flatMap(prefix=>groups.map(group=>[...prefix,group]));
  let ceiling=0;
  for(const groups of jointGroups) {
    let points=[[]];for(const group of groups)points=points.flatMap(prefix=>group.map(word=>[...prefix,...word]));
    ceiling+=countValues(F,points,q).reduce((s,k)=>s+Math.sqrt(k),0)**2/(joint.length*c.secret_count);nativeComponents++;
  }
  check(Math.abs(ceiling-c.exact_component_preserving_optimal_full_secret_success)<1e-11,"component ceiling");
  c.readouts.forEach(r=>check(r.full_secret_ML_success<=ceiling+1e-10,"component-preserving readout exceeds ceiling"));
  if(c.block_count!==1)continue; // Joint dynamics replay is in Python, not claimed checked here.
  const indices=new Map(points.map((x,i)=>[x.join(","),i]));
  const rows=c.block_sparse_row_certificates.map(row=>row.map(([x,w])=>[indices.get(x.join(",")),w]));
  for(const r of c.readouts.filter(r=>r.time===.7)) {
    const maximum=new Float64Array(D),primitiveMaximum=new Float64Array(D);let primitiveCount=0;
    for(const secret of words(c.dimension,q)) {
      const re=new Float64Array(D),im=new Float64Array(D),primitive=secret.some(x=>x%3);
      if(primitive)primitiveCount++;
      points.forEach((word,i)=>{
        const v=value(F,word,q),h=r.dressing==="low_only"?0:mod(((q+1)/2)*v.reduce((s,x)=>s+x*x,0),q);
        const a=2*Math.PI*mod(v.reduce((s,x,l)=>s+x*secret[l],0)-h,q)/q;
        re[i]=Math.cos(a)/Math.sqrt(D);im[i]=Math.sin(a)/Math.sqrt(D);
      });
      const [a,b]=evolve(rows,re,im,r.time);let mass=0;
      for(let i=0;i<D;i++){const p=a[i]**2+b[i]**2;mass+=p;maximum[i]=Math.max(maximum[i],p);if(primitive)primitiveMaximum[i]=Math.max(primitiveMaximum[i],p);}
      check(Math.abs(mass-1)<1e-10,"independent native evolution normalization");readoutSecrets++;
    }
    check(Math.abs(maximum.reduce((s,x)=>s+x,0)/c.secret_count-r.full_secret_ML_success)<1e-10,"independent native ML replay");
    check(Math.abs(primitiveMaximum.reduce((s,x)=>s+x,0)/primitiveCount-r.primitive_secret_ML_success)<1e-10,"independent primitive replay");
  }
}
for(const c of report.implicit_oracle_controls) {
  const F=native(c.native_labels,c.native_level),z=c.vertex, row=new Map(),predecessors=incoming(F,z,c.nullity_cap),target=outgoing(F,z,c.nullity_cap);
  function increment(x,v){const k=x.join(",");row.set(k,(row.get(k)||0)+v);}
  for(const x of predecessors){increment(x,-1);increment(z,1);}
  if(target){increment(target,-1);increment(z,1);}
  same([...row].filter(([,w])=>w).sort().map(([k,w])=>[k.split(",").map(Number),w]),c.sparse_row,"implicit GF3 row without cube enumeration");sparseRows++;
}
const census=new Map(),points=words(3);let squareTotal=0;
for(const entries of words(6)) {
  const F=Array.from({length:3},(_,i)=>[[entries[2*i]],[entries[2*i+1]]]);
  const groups=components(points,points.map(x=>outgoing(F,x,1))),square=groups.reduce((s,C)=>s+C.length**2,0);
  squareTotal+=square;census.set(square,(census.get(square)||0)+1);
}
same(Object.fromEntries([...census].sort((a,b)=>a[0]-b[0])),report.rank_one_component_census.component_size_square_sum_histogram,"complete low-source component census");
check(squareTotal===7357*27,"exact source component mean7357/729");
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
function equalFraction(text,a,b){const d=gcd(a,b);same(text,b/d===1n?String(a/d):`${a/d}/${b/d}`,"exact rational gate");}
for(const c of report.near_entropy_low_blind_gates) {
  const q=BigInt(c.modulus),n=BigInt(c.dimension),M=BigInt(c.charged_qutrits),N=q**n-(q/3n)**n;
  const a=5n**M,b=3n**M*N;
  equalFraction(c.native_average_decoder_success_squared_upper,a>b?1n:a,a>b?1n:b);
  check(!c.high_label_quantum_control_included&&!c.per_fixed_label_lower_bound_or_general_quantum_lower_bound,"low-blind scope");
}
check(!report.accepted_quantum_algorithm&&!report.generic_quantum_no_go,"unjustified algorithm claim");
console.log(JSON.stringify({status:"independent_replay_passed",complete_sparse_rows:sparseRows,
  native_component_references:nativeComponents,native_evolved_secrets:readoutSecrets,
  exact_low_source_census:729,exact_native_census_anchors:19683,efficient_decoder:false}));
