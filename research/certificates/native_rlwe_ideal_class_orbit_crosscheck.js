// Independent finite field/source/transport checks; NOT independent theorem review.
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const root=path.resolve(__dirname,"../..");
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),"utf8"));
const report=read("research/reductions/native_rlwe_ideal_class_orbits.json");
const check=(x,m)=>{if(!x) throw new Error(m);};
const mod=(x,q)=>(x%q+q)%q;
const key=a=>a.map(String).join(",");
const bar=a=>[a[0],...a.slice(1).reverse().map(v=>-v)];
function mul(a,b) {
  const d=a.length,c=Array(d).fill(0n);
  for(let i=0;i<d;i++) for(let j=0;j<d;j++) c[(i+j)%d]+=(i+j<d?1n:-1n)*a[i]*b[j];
  return c;
}
function scalarInverse(a,q) {
  let r=q,s=mod(a,q),u=0n,v=1n;
  while(s!==0n) {
    const k=r/s;[r,s]=[s,r-k*s];[u,v]=[v,u-k*v];
  }
  check(r===1n,"field scalar invertibility");return mod(u,q);
}
function inverse(a,q) {
  const d=a.length;
  const A=Array.from({length:d},(_,i)=>[
    ...Array.from({length:d},(_,j)=>mod((i>=j?1n:-1n)*a[(i-j+d)%d],q)),i===0?1n:0n]);
  for(let k=0;k<d;k++) {
    const j=A.findIndex((row,i)=>i>=k&&row[k]!==0n);
    check(j>=0,"unit multiplication matrix");[A[k],A[j]]=[A[j],A[k]];
    const u=scalarInverse(A[k][k],q);A[k]=A[k].map(v=>mod(v*u,q));
    for(let i=0;i<d;i++) if(i!==k) {
      const c=A[i][k];A[i]=A[i].map((v,t)=>mod(v-c*A[k][t],q));
    }
  }
  const out=A.map(row=>row[d]);
  check(mul(a,out).every((v,i)=>mod(v,q)===(i===0?1n:0n)),"independent matrix inverse");
  return out;
}
function shift(a,e) {
  const d=a.length,out=Array(d).fill(0n);
  a.forEach((v,i)=>{const j=i+e;out[(j%d+d)%d]=(Math.floor(j/d)%2===0?1n:-1n)*v;});
  return out;
}
const rotate=(a,e,q)=>shift(a,e).map(v=>mod(v,q));
function generic(a,q) {
  const n=mul(a,bar(a)).map(v=>mod(v,q));
  return n.some(v=>v!==0n)&&!n.every((v,i)=>v===(i===0?q-1n:0n));
}
function orbit(a,q) {
  check(generic(a,q),"stated generic source");
  const out=new Map(),reflected=inverse(a,q).map(v=>mod(-v,q));
  for(let k=0;k<a.length;k++) for(const start of [a,reflected]) {
    const word=rotate(start,2*k,q);out.set(key(word),word);
  }
  return out;
}
let ratios=0,classes=0,transports=0,hashes=0;
for(const row of report.complete_finite_source_orbits) {
  const q=BigInt(row.q),d=row.d,members=new Map();
  for(let i=0;i<row.q**d;i++) {
    let t=i;
    const a=Array.from({length:d},()=>{const v=BigInt(t%row.q);t=Math.floor(t/row.q);return v;});
    if(generic(a,q)) members.set(key(a),a);ratios++;
  }
  check(members.size===row.generic_ratio_count,"complete source denominator/filter");
  const sizes={};let classCount=0;
  while(members.size) {
    const a=members.values().next().value,group=orbit(a,q);
    for(const p of group.keys()) {check(members.has(p),"source orbit partition");members.delete(p);}
    sizes[group.size]=(sizes[group.size]||0)+1;classCount++;classes++;
  }
  check(classCount===row.exact_native_class_count,"exact class count");
  check(Object.entries(row.orbit_size_histogram).every(([k,v])=>sizes[k]===v)&&Object.keys(sizes).length===Object.keys(row.orbit_size_histogram).length,"exact orbit-size histogram");
  const x=q**BigInt(d/2),G=(x-1n)*(x-2n);
  check(BigInt(row.generic_ratio_count)===G&&BigInt(classCount)===G/BigInt(2*d)+1n,"conditional class-count theorem");
  check(sizes[d]===2,"only two monomial parity orbits");
}
const native=report.same_saved_native_d64_kernel,q=BigInt(native.modulus),m=native.ratio.map(BigInt),d=m.length;
const group=orbit(m,q);
check(group.size===native.orbit_size,"actual native orbit size");
const compare=(a,b)=>{for(let i=0;i<a.length;i++) if(a[i]!==b[i]) return a[i]<b[i]?-1:1;return 0;};
const canonical=[...group.values()].sort(compare)[0];
check(key(canonical)===key(native.canonical_class_label.map(BigInt)),"numeric, not string-sorted, canonical class label");
const digests=[...group.values()].map(a=>crypto.createHash("sha256").update("["+key(a)+"]").digest("hex")).sort();
check(digests.every((v,i)=>v===native.distinct_orbit_ratio_sha256[i]),"all exact orbit hashes");
const count=report.native_source_class_count,x=q**BigInt(d/2),G=(x-1n)*(x-2n);
check(BigInt("0x"+count.generic_ratio_count_hex)===G,"native source mass");
check(BigInt("0x"+count.exact_generic_native_ideal_class_count_hex)===G/BigInt(2*d)+1n,"native class count, not total order class number");
check(count.counts_only_classes_represented_by_THIS_native_family,"class-number scope");
const saved=read("research/certificates/native_rlwe_babai_profile_d64.json");
check(key(bar(saved.native_ratio.map(BigInt)).map(v=>mod(v,q)))===key(m),"same adjoint native kernel");
const k=native.canonicalizing_unit_word.rotation_exponent,reflection=native.canonicalizing_unit_word.kind==="reflection";
for(const row of saved.reduced_row_basis) {
  const g=row.slice(0,d).map(BigInt),f=row.slice(d).map(v=>-BigInt(v));
  const G=reflection?shift(f,k).map(v=>-v):shift(g,k),F=reflection?shift(g,-k):shift(f,-k);
  const predicted=mul(canonical,F);
  check(G.every((v,i)=>mod(v-predicted[i],q)===0n),"canonical unit-word transport of actual native basis row");
  check(G.concat(F).reduce((s,v)=>s+v*v,0n)===g.concat(f).reduce((s,v)=>s+v*v,0n),"exact native physical isometry");transports++;
}
check(native.global_equivalence_within_generic_native_family_decided_classically&&!native.new_short_relation_or_completion_supplied,"classical label is not a short relation");
check(!report.mechanism.general_nonprincipal_short_element_or_transport_algorithms_ruled_out,"nonnative algorithm scope");
check(!report.claim_gate.speedup_claim_allowed&&!report.claim_gate.independent_review,"algorithm/review debt");
for(const [p,h] of Object.entries(report.dependency_sha256)) {
  check(crypto.createHash("sha256").update(fs.readFileSync(path.join(root,p))).digest("hex")===h,`stale dependency ${p}`);hashes++;
}
console.log(JSON.stringify({status:"EXACT_CLASS_SOURCE_TRANSPORT_CROSSCHECK_NOT_INDEPENDENT_REVIEW",ratios,classes,transports,nativeOrbit:group.size,hashes}));
