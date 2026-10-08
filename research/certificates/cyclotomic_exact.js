"use strict";

// Independent exact arithmetic for finite certificate replay, not a solver.
const check = (x, message) => { if (!x) throw Error(message); };
const same = (a, b, message) => check(JSON.stringify(a) === JSON.stringify(b), message);
function gcd(a, b) {
  a = a < 0n ? -a : a; b = b < 0n ? -b : b;
  while (b) [a, b] = [b, a % b];
  return a;
}
function rat(a, b = 1n) {
  check(b !== 0n, "zero rational denominator");
  if (b < 0n) { a = -a; b = -b; }
  const g = gcd(a, b);
  return [a / g, b / g];
}
const zero = rat(0n), one = rat(1n);
const add = (a,b) => rat(a[0]*b[1]+b[0]*a[1], a[1]*b[1]);
const neg = a => [-a[0], a[1]], sub = (a,b) => add(a,neg(b));
const mul = (a,b) => rat(a[0]*b[0],a[1]*b[1]), div = (a,b) => rat(a[0]*b[1],a[1]*b[0]);
const str = a => a[1] === 1n ? String(a[0]) : a[0]+"/"+a[1];
const cmp = (a,b) => a[0]*b[1]-b[0]*a[1];
function parse(s) {
  check(typeof s === "string", "exact rational strings required");
  const p = s.split("/"); check(p.length <= 2, "rational syntax");
  const a = rat(BigInt(p[0]), p.length === 1 ? 1n : BigInt(p[1]));
  check(str(a) === s, "canonical rational encoding required"); return a;
}
function pow(a,n) {
  let b = one;
  while (n) { if (n % 2) b = mul(b,a); n = Math.floor(n/2); if (n) a = mul(a,a); }
  return b;
}
const mod = (a,q) => (a%q+q)%q;
function field(q) {
  let r = q;
  check(Number.isSafeInteger(q) && q >= 3 && q <= 81, "bounded checker root");
  while (r % 3 === 0) r /= 3;
  check(r === 1, "full ternary prime-power root required");
  const d = 2*q/3, F = () => Array.from({length:d}, () => zero);
  const eq = (a,b) => a.every((x,i) => cmp(x,b[i]) === 0n);
  const plus = (a,b) => a.map((x,i) => add(x,b[i]));
  function times(a,b) {
    const c = Array.from({length:2*d-1}, () => zero);
    a.forEach((x,i) => { if (x[0]) b.forEach((y,j) => { if (y[0]) c[i+j] = add(c[i+j],mul(x,y)); }); });
    for (let i = c.length-1; i >= d; i--) {
      const x = c[i]; c[i-d] = sub(c[i-d],x); c[i-d+d/2] = sub(c[i-d+d/2],x);
    }
    return c.slice(0,d);
  }
  const unit = F(); unit[0] = one;
  const z = F(); z[1] = one;
  const powers = [unit];
  for (let k = 1; k < q; k++) powers.push(times(powers[k-1],z));
  check(eq(times(powers[q-1],z),unit), "root order identity");
  function encode(a) {
    let k = a.length; while (k && !a[k-1][0]) k--;
    return a.slice(0,k).reverse().map(str);
  }
  function decode(raw) {
    check(Array.isArray(raw) && raw.length <= d, "whole canonical polynomial");
    const a = F(); raw.slice().reverse().forEach((x,i) => a[i] = parse(x));
    same(encode(a),raw,"canonical reduced field coefficients"); return a;
  }
  const scale = (a,b) => a.map(x => mul(x,b));
  const conj = a => a.reduce((s,x,i) => plus(s,scale(powers[mod(-i,q)],x)),F());
  return {q,d,F,unit,powers,eq,plus,times,encode,decode,scale,conj};
}
const piCache = new Map();
function piInterval(N) {
  if (piCache.has(N)) return piCache.get(N);
  function atan(k) {
    const x = rat(1n,BigInt(k)), x2 = mul(x,x); let p = x, sum = zero;
    for (let j = 0; j < N; j++) { sum = add(sum,div(j%2 ? neg(p) : p,rat(BigInt(2*j+1)))); p = mul(p,x2); }
    const end = add(sum,div(N%2 ? neg(p) : p,rat(BigInt(2*N+1))));
    return cmp(sum,end) <= 0n ? [sum,end] : [end,sum];
  }
  const a = atan(5), b = atan(239);
  const result = [sub(mul(rat(16n),a[0]),mul(rat(4n),b[1])),sub(mul(rat(16n),a[1]),mul(rat(4n),b[0]))];
  piCache.set(N,result); return result;
}
const cosineCache = new Map();
function cosineInterval(q,k,N) {
  const id = `${q}:${k}:${N}`;
  if (cosineCache.has(id)) return cosineCache.get(id);
  const bounds = piInterval(N), center = div(add(...bounds),rat(2n)), radius = div(sub(bounds[1],bounds[0]),rat(2n));
  const x = div(mul(rat(BigInt(2*k)),center),rat(BigInt(q))), x2 = mul(x,x);
  let term = one, sum = one;
  for (let j = 1; j < N; j++) { term = div(neg(mul(term,x2)),rat(BigInt((2*j-1)*(2*j)))); sum = add(sum,term); }
  let factorial = 1n; for (let j = 2; j <= 2*N; j++) factorial *= BigInt(j);
  const error = add(div(pow(x,2*N),rat(factorial)),div(mul(rat(BigInt(2*k)),radius),rat(BigInt(q))));
  const result = [sub(sum,error),add(sum,error)]; cosineCache.set(id,result); return result;
}
function interval(K,a,N) {
  let lo = zero, hi = zero;
  a.forEach((x,k) => {
    if (!x[0]) return;
    const [left,right] = cosineInterval(K.q,k,N);
    lo = add(lo,mul(x,x[0] > 0n ? left : right)); hi = add(hi,mul(x,x[0] > 0n ? right : left));
  }); return [lo,hi];
}
const signCache = new Map();
function sign(K,a) {
  const id = K.q+":"+JSON.stringify(K.encode(a));
  if (signCache.has(id)) return signCache.get(id);
  check(K.eq(a,K.conj(a)), "real algebraic scalar required");
  if (a.slice(1).every(x => !x[0])) return a[0][0] > 0n ? 1 : a[0][0] < 0n ? -1 : 0;
  for (let N = 8; N <= 128; N *= 2) {
    const [lo,hi] = interval(K,a,N);
    if (lo[0] > 0n) { signCache.set(id,1); return 1; }
    if (hi[0] < 0n) { signCache.set(id,-1); return -1; }
  } throw Error("unresolved algebraic sign, not acceptance");
}
function signCertificate(K,a,c) {
  check(K.eq(a,K.conj(a)), "real certificate scalar");
  if (a.slice(1).every(x => !x[0])) {
    const s = a[0][0] > 0n ? "POSITIVE" : a[0][0] < 0n ? "NEGATIVE" : "ZERO";
    check(c.status === s && c.rational_value === str(a[0]) && c.lower === str(a[0]) && c.upper === str(a[0]), "rational sign certificate");
    return s;
  }
  const N = c.Machin_arctangent_terms;
  check([8,16,32,64,128].includes(N) && c.cosine_Taylor_terms === N, "bounded sign interval budget");
  const [lo,hi] = interval(K,a,N);
  check(c.lower === str(lo) && c.upper === str(hi) && c.interval_uses_only_exact_rational_arithmetic === true, "independent rational interval");
  check((c.status === "POSITIVE" && lo[0] > 0n) || (c.status === "NEGATIVE" && hi[0] < 0n), "strict interval sign");
  return c.status;
}
function matrices(K) {
  const zeroM = (r,c) => Array.from({length:r},()=>Array.from({length:c},K.F));
  const identity = r => Array.from({length:r},(_,i)=>Array.from({length:r},(_,j)=>i===j?K.unit:K.F()));
  const plus = (A,B) => A.map((row,i)=>row.map((x,j)=>K.plus(x,B[i][j])));
  const scale = (A,x) => A.map(row=>row.map(y=>K.times(x,y)));
  const times = (A,B) => A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>K.plus(s,K.times(x,B[k][j])),K.F())));
  const star = A => A[0].map((_,j)=>A.map(row=>K.conj(row[j])));
  const eq = (A,B) => A.length===B.length && A.every((row,i)=>row.length===B[i].length && row.every((x,j)=>K.eq(x,B[i][j])));
  const decode = (raw,r,c) => { check(raw.length===r&&raw.every(row=>row.length===c),"complete matrix shape"); return raw.map(row=>row.map(K.decode)); };
  function power(A,k) {
    let B = identity(A.length);
    while (k) { if (k%2) B=times(B,A); k=Math.floor(k/2); if(k) A=times(A,A); } return B;
  }
  const expect = (v,G,A) => times(times(times(star(v),G),A),v)[0][0];
  const norm = (v,G) => times(times(star(v),G),v)[0][0];
  function LDL(A,c) {
    const r=A.length,L=decode(c.lower_unit_matrix,r,r),d=c.diagonal.map(K.decode);
    check(d.length===r&&c.pivot_sign_certificates.length===r,"whole LDL dimensions");
    L.forEach((row,i)=>row.forEach((x,j)=>{if(j>=i)check(K.eq(x,i===j?K.unit:K.F()),"unit lower triangular factor");}));
    const D=zeroM(r,r);d.forEach((x,i)=>D[i][i]=x);
    check(eq(times(times(L,D),star(L)),A),"exact LDL factorization reconstructs supplied norm bound");
    let rank=0;
    d.forEach((x,i)=>{const s=signCertificate(K,x,c.pivot_sign_certificates[i]);check(s==="POSITIVE"||(!c.positive_definite_required&&s==="ZERO"),"LDL positivity");if(s==="POSITIVE")rank++;});
    check(rank===c.rank_exact,"certified LDL rank");
  }
  return {zeroM,identity,plus,scale,times,star,eq,decode,power,expect,norm,LDL};
}
module.exports = {check,same,rat,zero,one,add,sub,mul,div,str,parse,cmp,mod,field,sign,signCertificate,matrices};
