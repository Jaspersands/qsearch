// Independent exact encoding/calibration checks, NOT independent theorem review.
"use strict";
const fs=require("fs"), path=require("path"), crypto=require("crypto");
const root=path.resolve(__dirname,"../..");
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),"utf8"));
const report=read("research/reductions/native_rlwe_conductor_order.json");
const check=(x,m)=>{if(!x) throw new Error(m);};
const eq=(a,b)=>a.every((v,i)=>v===b[i]);
const mod=(x,q)=>(x%q+q)%q;
const bar=a=>[a[0],...a.slice(1).reverse().map(v=>-v)];
const add=(a,b)=>a.map((v,i)=>v+b[i]);
function mul(a,b) {
  const d=a.length,c=Array(d).fill(0n);
  for(let i=0;i<d;i++) for(let j=0;j<d;j++) c[(i+j)%d]+=(i+j<d?1n:-1n)*a[i]*b[j];
  return c;
}
const norm=a=>mul(a,bar(a));
const gcd=(a,b)=>b===0n?a:gcd(b,a%b);
function det(input) {
  const a=input.map(row=>[...row]),n=a.length;
  let old=1n,sign=1n;
  for(let k=0;k<n-1;k++) {
    if(a[k][k]===0n) {
      const j=a.findIndex((row,i)=>i>k&&row[k]!==0n);
      if(j<0) return 0n;
      [a[k],a[j]]=[a[j],a[k]];sign=-sign;
    }
    const p=a[k][k];
    for(let i=k+1;i<n;i++) for(let j=k+1;j<n;j++) {
      const v=a[i][j]*p-a[i][k]*a[k][j];
      check(v%old===0n,"exact determinant division");a[i][j]=v/old;
    }
    for(let i=k+1;i<n;i++) a[i][k]=0n;
    old=p;
  }
  return sign*a[n-1][n-1];
}
let encodings=0, nativeRows=0, vectors=0, units=0, hashes=0;
function verify(row) {
  const q=BigInt(row.modulus),d=row.dimension;
  const m=row.graph_ratio.map(v=>mod(BigInt(v)+q/2n,q)-q/2n);
  const one=Array(d).fill(0n);one[0]=1n;
  const beta=add(norm(m),one);
  check(eq(beta,row.local_principality.reduced_norm_coefficients.map(BigInt)),"reduced norm");
  const C=Array.from({length:d},(_,i)=>Array.from({length:d},(_,j)=>(i>=j?1n:-1n)*beta[(i-j+d)%d]));
  const index=det(C);
  check(index>=1n&&index===BigInt("0x"+row.local_principality.contained_sublattice_global_index_hex),"full contained-ideal index");
  check(row.local_principality.certificate_at_primes_dividing_q_supplied===(gcd(index,q)===1n),"local unit certificate");
  check(row.ambient_order_saturation.O_0_times_native_graph_equals_O_0===(gcd(index,q)===1n),"ambient saturation loses level data");
  check(row.ambient_order_saturation.every_overorder_containing_O_0_erases_graph_upon_extension===(gcd(index,q)===1n),"overorder saturation scope");
  check(row.ambient_order_saturation.M_dependent_overorder_choice_not_ruled_out,"adaptive order choice is extra data, not ruled out");
  check(row.local_principality.contained_sublattice_equals_full_graph_globally===(index===1n),"local vs global equality");
  const principal=row.graph_ratio.every(v=>BigInt(v)===0n);
  check(row.global_principality.principal_over_THIS_conductor_order===principal,"published-theorem-dependent principal source gate");
  check(BigInt("0x"+row.global_principality.source_uniform_principal_probability.denominator_hex)===q**BigInt(d),"full source denominator");
  check(row.original_physical_metric_preserved_exactly&&row.native_graph_is_fractional_left_ideal,"new encoding scope");
  check(!row.all_quaternion_orders_or_short_element_algorithms_ruled_out&&!row.speedup_claim_allowed,"scope/claim gates");
  // Check both families of native basis columns under left q*j.
  for(let i=0;i<d;i++) {
    const e=Array(d).fill(0n);e[i]=1n;
    for(const [g,f] of [[e.map(v=>q*v),Array(d).fill(0n)],[mul(m,e),e]]) {
      const outg=bar(f).map(v=>-q*v),outf=bar(g).map(v=>q*v);
      check(add(outg,mul(m,outf).map(v=>-v)).every(v=>mod(v,q)===0n),"q*j graph closure");
      check(outg.concat(outf).reduce((s,v)=>s+v*v,0n)===q*q*g.concat(f).reduce((s,v)=>s+v*v,0n),"q*j scaled original metric");
    }
  }
  encodings++;
}
report.finite_controls.forEach(verify);
verify(report.same_saved_native_d64_kernel);
const saved=read("research/certificates/native_rlwe_babai_profile_d64.json");
const ratio=bar(saved.native_ratio.map(BigInt)),q=BigInt(saved.q),d=ratio.length;
check(eq(report.same_saved_native_d64_kernel.graph_ratio.map(BigInt),ratio.map(v=>mod(v,q))),"same native adjoint ratio");
for(const row of saved.reduced_row_basis) {
  const g=row.slice(0,d).map(BigInt),f=row.slice(d).map(v=>-BigInt(v));
  check(add(g,mul(ratio,f).map(v=>-v)).every(v=>mod(v,q)===0n),"native source basis");nativeRows++;
}
for(let k=0;k<3**8;k++) {
  let t=k;
  const x=Array.from({length:8},()=>{const v=BigInt(t%3-1);t=Math.floor(t/3);return v;});
  const g=x.slice(0,4),f=x.slice(4),n=add(norm(g),norm(f));
  check(n[2]===0n&&n[3]===-n[1],"real d4 norm");
  if((n[0]*n[0]-2n*n[1]*n[1])**2n===1n) {
    units++;check(!g.some(v=>v!==0n)||!f.some(v=>v!==0n),"no mixed ambient unit in bounded calibration");
  }
  vectors++;
}
check(vectors===report.bounded_d4_unit_check.coefficient_vectors_checked&&units===report.bounded_d4_unit_check.ambient_units,"exact bounded unit coverage");
check(report.published_dependency.not_Weber_class_number_one_conjecture,"external theorem scope");
check(!report.claim_gate.speedup_claim_allowed&&!report.claim_gate.independent_review,"no independent review/algorithm");
for(const [p,h] of Object.entries(report.dependency_sha256)) {
  check(crypto.createHash("sha256").update(fs.readFileSync(path.join(root,p))).digest("hex")===h,`stale dependency ${p}`);hashes++;
}
console.log(JSON.stringify({status:"EXACT_BOUNDED_CROSSCHECK_NOT_INDEPENDENT_REVIEW",encodings,nativeRows,vectors,units,hashes}));
