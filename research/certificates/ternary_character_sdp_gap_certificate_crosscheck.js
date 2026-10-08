"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto"),cp=require("child_process");
const sourcePath=path.join(__dirname,"../classical_baselines/ternary_character_sdp_decoder.json");
const R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../classical_baselines/ternary_character_sdp_gap_certificate.json"),"utf8"));
const source=JSON.parse(fs.readFileSync(sourcePath,"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},key=JSON.stringify,same=(a,b,m)=>check(key(a)===key(b),m);
const mod=(a,q)=>(a%q+q)%q;
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
check(R.source_report_sha256===hash(sourcePath),"pinned original numerical/source report");
check(R.derivation_sha256===hash(path.join(__dirname,"../TERNARY_CHARACTER_SDP_GAP_CERTIFICATE.md")),"pinned exact certificate derivation");
check(R.numerical_solver_status_used_as_proof===false&&R.asymptotic_impossibility_or_speedup_claim===false,"finite primal scope");
function gcd(a,b){a=a<0n?-a:a;while(b)[a,b]=[b,a%b];return a;}
function F(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return[a/g,b/g];}
const fa=(x,y)=>F(x[0]*y[1]+y[0]*x[1],x[1]*y[1]),fn=x=>[-x[0],x[1]],fsub=(x,y)=>fa(x,fn(y)),fm=(x,y)=>F(x[0]*y[0],x[1]*y[1]),fd=(x,y)=>F(x[0]*y[1],x[1]*y[0]);
const fp=(x,k)=>F(x[0]**BigInt(k),x[1]**BigInt(k));
function floor(x){return x[0]/x[1]-(x[0]<0n&&x[0]%x[1]!==0n?1n:0n);}
const ceil=x=>-floor(fn(x));
function factorial(n){let a=1n;for(let j=2;j<=n;j++)a*=BigInt(j);return a;}
function roots(q){
  function atan(d){const x=F(1,d);let a=F(0);for(let k=0;k<40;k++)a=fa(a,fm(F(k%2?-1:1,2*k+1),fp(x,2*k+1)));return[a,fa(a,fd(fp(x,81),F(81)))];}
  const a=atan(5),b=atan(239),lo=fsub(fm(F(16),a[0]),fm(F(4),b[1])),hi=fsub(fm(F(16),a[1]),fm(F(4),b[0])),P=2n**64n;
  const lower=F(floor(fm(lo,F(P))),P),upper=F(ceil(fm(hi,F(P))),P),mid=fd(fa(lower,upper),F(2));
  const rem=fd(fp(F(22,7),41),F(factorial(41))),T=2n**48n,out=[];
  for(let e=0;e<q;e++){
    if(!e){out.push({cos_lower:Number(T),cos_upper:Number(T),sin_lower:0,sin_upper:0});continue;}
    const signed=2*e<=q?e:e-q,angle=fm(mid,F(2*signed,q)),error=fa(fm(fsub(upper,lower),F(Math.abs(signed),q)),rem);
    let cosine=F(0),sine=F(0);for(let k=0;k<21;k++){
      cosine=fa(cosine,fm(F(k%2?-1:1,factorial(2*k)),fp(angle,2*k)));
      sine=fa(sine,fm(F(k%2?-1:1,factorial(2*k+1)),fp(angle,2*k+1)));
    }
    out.push({cos_lower:Number(floor(fm(fsub(cosine,error),F(T)))),cos_upper:Number(ceil(fm(fa(cosine,error),F(T)))),
              sin_lower:Number(floor(fm(fsub(sine,error),F(T)))),sin_upper:Number(ceil(fm(fa(sine,error),F(T))))});
  }return out;
}
function PSD(c){
  const w=c.witness,K=c.nodes.length,S=w.moment_scale,re=w.matrix_real_integer,im=w.matrix_imag_integer,N=2*K,L=w.factor_lower_triangle_integer;
  check(S===2**24&&w.residual_denominator===String(2n**48n)&&w.matrix_dimension===N,"exact dyadic scales / realification");
  check(re.length===K&&im.length===K&&L.length===N,"full exact point/factor sizes");
  const differences=new Map();let entries=0;
  for(let i=0;i<K;i++){check(re[i].length===K&&im[i].length===K,"exact moment row length");for(let j=0;j<K;j++){
    check(Number.isSafeInteger(re[i][j])&&Number.isSafeInteger(im[i][j]),"integer moments");
    check(re[i][j]===re[j][i]&&im[i][j]===-im[j][i],"exact Hermitian point");
    if(i===j)check(re[i][j]===S&&im[i][j]===0,"exact unit diagonal");
    const d=key(c.nodes[i].map((a,k)=>mod(a-c.nodes[j][k],c.modulus))),v=[re[i][j],im[i][j]];
    if(!differences.has(d))differences.set(d,v);same(v,differences.get(d),"EVERY exact difference constraint");entries++;
  }}
  // Bound every dot-product's ABSOLUTE partial sum by Cauchy. All operations
  // below are integers <2^53, so IEEE doubles represent them exactly.
  let maximumNorm=0;L.forEach((row,i)=>{check(row.length===i+1,"complete triangular factor");let norm=0;for(const a of row){check(Number.isSafeInteger(a)&&Math.abs(a)<2**26,"safe exact factor entry");norm+=a*a;check(Number.isSafeInteger(norm),"safe exact row norm");}maximumNorm=Math.max(maximumNorm,norm);});
  check(maximumNorm<2**51,"Cauchy exact-dot-product arithmetic guard");
  const A=(i,j)=>i<K?(j<K?re[i][j]:-im[i][j-K]):(j<K?im[i-K][j]:re[i-K][j-K]);
  const margins=Array(N).fill(0n);for(let i=0;i<N;i++)for(let j=0;j<=i;j++){
    let dot=0;for(let k=0;k<=j;k++)dot+=L[i][k]*L[j][k];check(Number.isSafeInteger(dot),"exact factor dot");
    const entry=A(i,j);check(Number.isSafeInteger(entry*S)&&Math.abs(entry*S)<2**51,"realification exact arithmetic guard");
    const residual=entry*S-dot;check(Number.isSafeInteger(residual),"exact residual integer");
    const v=BigInt(residual);if(i===j)margins[i]+=v;else{const a=v<0n?-v:v;margins[i]-=a;margins[j]-=a;}
  }
  const minimum=margins.reduce((a,b)=>a<b?a:b);check(minimum>=0n&&String(minimum)===w.minimum_integer_diagonal_dominance_margin&&w.PSD_certified===true,"exact residual Gershgorin PSD certificate");
  return entries;
}
function characterCensus(records,bounds){
  const q=records[0].modulus,n=records[0].first.length,M=records.length,G=q**n,B=2**26;
  check(G<=600000&&Number.isSafeInteger(G)&&3*M*2**23<2**53&&3*M*B<2**53,"complete exact census arithmetic/cap");
  // Split each 48-bit interval numerator, so every inner-loop sum is exact.
  const split=v=>{const hi=Math.floor(v/B);return[hi,v-hi*B];},upper=bounds.map(r=>split(r.cos_upper)),lower=bounds.map(r=>split(r.cos_lower));
  const rows=records.flatMap(r=>[r.first,r.second]),ys=records.flatMap(r=>r.outcome),pred=Array(2*M).fill(0),secret=Array(n).fill(0);
  let bestUpper=[-Infinity,0],bestLower=[-Infinity,0],upperWitness,lowerWitness;
  function normalize(hi,lo){const carry=Math.floor(lo/B);return[hi+carry,lo-carry*B];}
  const greater=(a,b)=>a[0]>b[0]||(a[0]===b[0]&&a[1]>b[1]);
  for(let k=0;k<G;k++){
    let uh=0,ul=0,lh=0,ll=0;for(let i=0;i<M;i++){
      const e1=mod(ys[2*i]-pred[2*i],q),e2=mod(ys[2*i+1]-pred[2*i+1],q);
      for(const e of[e1,e2,mod(e1-e2,q)]){uh+=upper[e][0];ul+=upper[e][1];lh+=lower[e][0];ll+=lower[e][1];}
    }
    const u=normalize(uh,ul),l=normalize(lh,ll);if(greater(u,bestUpper)){bestUpper=u;upperWitness=secret.slice();}if(greater(l,bestLower)){bestLower=l;lowerWitness=secret.slice();}
    if(k+1<G){let j=0;while(j<n){secret[j]=(secret[j]+1)%q;for(let t=0;t<rows.length;t++)pred[t]=mod(pred[t]+rows[t][j],q);if(secret[j]!==0)break;j++;}}
  }
  const integer=v=>String(BigInt(v[0])*BigInt(B)+BigInt(v[1]));
  return {status:"ALL_FULL_ROOT_SECRETS_EXACT_INTERVAL_BOUNDED",secrets_checked:G,paired_score_features_checked:3*M*G,
          score_denominator:String(2n**48n),global_character_score_upper_numerator:integer(bestUpper),
          feasible_character_score_lower_numerator:integer(bestLower),upper_witness:upperWitness,lower_witness:lowerWitness,
          exhaustive_verification_used_by_decoder:false,exact_identity_of_unique_optimal_secret_certified:false};
}
let entries=0,secrets=0,features=0,gaps=0;
for(const c of R.certificates){
  check(c.status==="EXACT_FINITE_SDP_CHARACTER_GAP","expected positive exact gap");
  check(c.finite_counterexample_is_population_or_asymptotic_failure===false&&c.certification_uses_truth_or_holdout===false,"counterexample scope");
  const original=source.native_controls.find(x=>x.seed===c.seed);check(original,"original cohort linkage");same(c.nodes,original.decoder.model.nodes,"original compiled moment model");same(c.native_nodes,original.decoder.model.native_nodes,"original score node linkage");
  const interval=roots(c.modulus);same(c.root_intervals,interval,"independent rational Machin/Taylor root intervals");check(c.root_interval_denominator===String(2n**48n),"exact root denominator");
  entries+=PSD(c);const records=original.training_records,w=c.witness;let value=0n;
  records.forEach((r,k)=>{const[a,b]=c.native_nodes[k];for(const[i,j,e]of[[a,0,r.outcome[0]],[b,0,r.outcome[1]],[a,b,mod(r.outcome[0]-r.outcome[1],c.modulus)]]){
    const x=BigInt(w.matrix_real_integer[i][j]),y=BigInt(w.matrix_imag_integer[i][j]),v=interval[e];
    value+=x*BigInt(x>=0n?v.cos_lower:v.cos_upper)+y*BigInt(y>=0n?v.sin_lower:v.sin_upper);
  }});
  const census=characterCensus(records,interval);same(c.character_census,census,"complete independent exact all-secret census");
  const upper=BigInt(census.global_character_score_upper_numerator)*BigInt(w.moment_scale),gap=value-upper;
  check(value===BigInt(c.SDP_feasible_score_lower_numerator)&&upper===BigInt(c.all_character_score_upper_same_scale_numerator)&&gap===BigInt(c.strict_gap_lower_numerator)&&gap>0n,"strict rational feasible-vs-character gap");
  check(c.score_common_denominator===String(2n**72n)&&c.exact_SDP_optimum_or_dual_certificate_required===false,"a feasible primal witness is enough");
  secrets+=census.secrets_checked;features+=census.paired_score_features_checked;gaps++;
}
// Check source charts and circuit compilation too, not just the saved model.
cp.execFileSync(process.execPath,[path.join(__dirname,"ternary_character_sdp_decoder_crosscheck.js"),sourcePath],{stdio:"pipe"});
console.log(JSON.stringify({status:"PASS",exact_finite_gaps:gaps,exact_moment_entries:entries,full_root_secrets_checked:secrets,exact_score_features_checked:features,numerical_eigenvalues_or_solver_status_trusted:false,population_or_asymptotic_impossibility_certified:false}));
