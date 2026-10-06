// Independent BigInt verifier; arithmetic agreement is NOT independent proof review.
"use strict";
const fs = require("fs");
const path = require("path");
const assert = require("assert");
const file = process.argv[2] || path.join(__dirname, "native_rlwe_primal_babai_d64_seed290960.json");
const saved = JSON.parse(fs.readFileSync(file, "utf8"));
const abs = x => x < 0n ? -x : x;
function gcd(a, b) { a=abs(a); b=abs(b); while(b) [a,b]=[b,a%b]; return a; }
function rational(n, d=1n) {
  if(d < 0n) {n=-n; d=-d;} assert(d > 0n);
  const g=gcd(n,d); return [n/g,d/g];
}
const add = (a,b) => rational(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const neg = a => [-a[0],a[1]];
const sub = (a,b) => add(a,neg(b));
const mul = (a,b) => rational(a[0]*b[0],a[1]*b[1]);
const div = (a,b) => rational(a[0]*b[1],a[1]*b[0]);
const frac = record => rational(BigInt(record.numerator_hex),BigInt(record.denominator_hex));
const le = (a,b) => a[0]*b[1] <= b[0]*a[1];
function integer(x) { assert(Number.isSafeInteger(x)); return BigInt(x); }
const d=saved.d, n=2*d, q=integer(saved.q), l=frac(saved.log_dimension_upper);
assert(d===64 && saved.status==="LOCAL_DERIVATION_REVIEW_PENDING");
for(const flag of ["quantum_algorithm", "asymptotic_attack_proved", "independent_review",
                   "source_distribution_samples", "source_transfer_losses_paid", "held_out_verification_run"])
  assert.strictEqual(saved[flag],false);
assert(163n**25n > 2n**36n * 60n**25n);
assert(163n**l[0] > BigInt(d)**l[1] * 60n**l[0]);
// Prime/residue-degree guard for the actual source row, not an imported label assumption.
for(let p=3n; p*p<=q; p+=2n) assert(q%p!==0n);
let z=q%BigInt(2*d), order=1;
while(z!==1n) {z=z*q%BigInt(2*d); ++order; assert(order<=2*d);}
assert.strictEqual(order,d/2);
const label=saved.label.map(integer);
const centered=label.map(x=>(x+q/2n)%q-q/2n);
const C=Array.from({length:d},(_,i)=>Array.from({length:d},(_,j)=>
  (i<j ? -1n:1n)*centered[(i-j+d)%d]));
const native=saved.native_row_basis.map(row=>row.map(integer));
for(let i=0;i<n;i++) for(let j=0;j<n;j++) {
  const expected=i<d ? (j<d ? BigInt(i===j):C[j-d][i]) :
    (j<d ? 0n:q*BigInt(i-d===j-d));
  assert.strictEqual(native[i][j],expected);
}
const rows=saved.reduced_row_basis.map(row=>row.map(integer));
const U=saved.unimodular_transform.map(row=>row.map(integer));
for(let i=0;i<n;i++) for(let j=0;j<n;j++) {
  let sum=0n; for(let k=0;k<n;k++) sum+=U[i][k]*native[k][j];
  assert.strictEqual(sum,rows[i][j]);
}
for(const row of rows) for(let i=0;i<d;i++) {
  let x=row[d+i]; for(let j=0;j<d;j++) x-=C[i][j]*row[j];
  assert.strictEqual(x%q,0n);
}
const dot=(a,b)=>a.reduce((sum,x,i)=>sum+x*b[i],0n);
let gram=rows.map(a=>rows.map(b=>dot(a,b)));
let previous=1n;
const gs=[], mu=Array.from({length:n},()=>Array.from({length:n},()=>[0n,1n]));
for(let k=0;k<n;k++) {
  const pivot=gram[k][k]; assert(pivot>0n);
  assert.strictEqual(pivot,BigInt(saved.leading_gram_determinants_hex[k]));
  gs.push(rational(pivot,previous));
  for(let j=k+1;j<n;j++) mu[j][k]=rational(gram[k][j],pivot);
  for(let i=k+1;i<n;i++) for(let j=i;j<n;j++) {
    const numerator=pivot*gram[i][j]-gram[i][k]*gram[k][j];
    assert.strictEqual(numerator%previous,0n);
    gram[i][j]=gram[j][i]=numerator/previous;
  }
  previous=pivot;
}
assert.strictEqual(previous,q**BigInt(2*d)); // Membership + exact volume gives index one.
function tail(h, record) {
  let sum=[0n,1n];
  gs.forEach((x,i)=> {
    const ratio=div(mul([27n,25n],x),h), exponent=ratio[0]/ratio[1];
    assert.strictEqual(exponent,BigInt(record.dyadic_exponents[i]));
    const effective=exponent>4096n ? 4096n:exponent;
    sum=add(sum,rational(2n,2n**effective));
  });
  assert.deepStrictEqual(sum,frac(record.uncapped_union_upper));
  const capped=le(sum,[1n,1n]) ? sum:[1n,1n];
  assert.deepStrictEqual(capped,frac(record.failure_upper));
  assert.strictEqual(record.union_exponent_cap,4096);
  return capped;
}
const sphere=saved.certificate.spherical, ell=saved.certificate.elliptical;
const l2=mul(l,l);
assert.deepStrictEqual(frac(sphere.width_squared_upper),mul([513n,1n],l2));
const h=add(l2,mul(mul([32n,1n],l2),add(l2,[2n,1n])));
assert.deepStrictEqual(h,frac(ell.width_squared_upper));
const sphereFailure=tail(frac(sphere.width_squared_upper),sphere), ellFailure=tail(h,ell);
assert.strictEqual(ell.latent_radius_squared,2);
assert.strictEqual(ell.shape_dyadic_exponent,17);
assert.deepStrictEqual(frac(ell.shape_failure_upper),[1n,4096n]);
const total=add(ellFailure,[1n,4096n]);
assert.deepStrictEqual(total,frac(ell.shape_conditioned_total_upper));
const mix=ell.unconditional_mixture, base=add(l2,mul([32n,1n],mul(l2,l2)));
assert.deepStrictEqual(base,frac(mix.base_width_squared_upper));
assert.strictEqual(mix.secret_error_independent_only_conditionally_on_shape,true);
assert.strictEqual(mix.hidden_shape_given_to_decoder,false);
function isqrt(x) {
  let a=0n,b=x+1n;
  while(b-a>1n) {const m=(a+b)/2n; if(m*m<=x) a=m; else b=m;}
  return a;
}
let mixTotal=[0n,1n];
for(let i=0;i<n;i++) {
  const record=mix.directions[i], radius=rational(isqrt(gs[i][0]/gs[i][1]),2n);
  assert.deepStrictEqual(radius,frac(record.radius_lower));
  let v=div(mul([6n,1n],radius),base), alpha=div(mul(mul([BigInt(d),1n],l2),mul(v,v)),[144n,1n]);
  while(!le(alpha,[1n,2n])) {v=div(v,[2n,1n]); alpha=div(alpha,[4n,1n]);}
  assert.deepStrictEqual(v,frac(record.chernoff_parameter));
  assert.deepStrictEqual(alpha,frac(record.mixture_denominator_loss));
  const exponentR=mul([36n,25n],sub(mul(v,radius),div(mul(base,mul(v,v)),[12n,1n])));
  const exponent=exponentR[0]/exponentR[1];
  assert.strictEqual(exponent,BigInt(record.dyadic_exponent));
  let bound=div(rational(2n,2n**(exponent>4096n ? 4096n:exponent)),sub([1n,1n],alpha));
  if(!le(bound,[1n,1n])) bound=[1n,1n];
  assert.deepStrictEqual(bound,frac(record.tail_upper));
  mixTotal=add(mixTotal,bound);
}
assert.deepStrictEqual(mixTotal,frac(mix.uncapped_union_upper));
const mixBound=le(mixTotal,[1n,1n]) ? mixTotal:[1n,1n];
assert.deepStrictEqual(mixBound,frac(mix.failure_upper));
const finalEll=le(total,mixBound) ? total:mixBound;
assert.deepStrictEqual(finalEll,frac(ell.total_failure_upper));
assert(le(sphereFailure,[1n,1n]) && le(finalEll,[1n,1n]));
function floor(a) {
  let k=a[0]/a[1]; if(a[0]<0n && a[0]%a[1]) --k; return k;
}
function decode(b) {
  const target=Array(d).fill(0n).concat(b.map(integer).map(x=>(x+q/2n)%q-q/2n));
  const inner=[];
  for(let i=0;i<n;i++) {
    let x=[dot(rows[i],target),1n];
    for(let j=0;j<i;j++) x=sub(x,mul(mu[i][j],inner[j]));
    inner.push(x);
  }
  const coordinates=inner.map((x,i)=>div(x,gs[i])), coefficients=Array(n).fill(0n);
  for(let i=n-1;i>=0;i--) {
    const z=floor(add(coordinates[i],[1n,2n])); coefficients[i]=z;
    for(let j=0;j<i;j++) coordinates[j]=sub(coordinates[j],mul([z,1n],mu[i][j]));
  }
  return Array.from({length:d},(_,j)=>rows.reduce((sum,row,i)=>sum+coefficients[i]*row[j],0n));
}
let controlCoordinates=0;
for(const control of saved.controls) {
  const secret=control.secret.map(integer), error=control.error.map(integer), b=control.b.map(integer);
  for(let i=0;i<d;i++) {
    let sum=error[i]; for(let j=0;j<d;j++) sum+=C[i][j]*secret[j];
    assert.strictEqual((sum-b[i])%q,0n);
  }
  const answer=decode(control.b);
  assert.deepStrictEqual(answer,control.decoded_secret.map(integer));
  assert.strictEqual(control.correct,answer.every((x,i)=>x===secret[i]));
  controlCoordinates+=d;
}
console.log(JSON.stringify({status:"ARITHMETIC_CROSSCHECK_ONLY", basisEntries:n*n,
  gramPivots:n, sourceLedgers:2, controlCoordinates, independentProofReview:false}));
