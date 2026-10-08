"use strict";
// Independent BigInt replay: triangular integer projections, not Python GS code.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const report = JSON.parse(fs.readFileSync(path.join(__dirname, "../phase_workbench/ternary_repair_catalog.json"), "utf8"));
const source = JSON.parse(fs.readFileSync(path.join(__dirname, "../phase_workbench/ternary_pair_cell_coverage.json"), "utf8"));
function check(x, message) { if (!x) throw Error(message); }
const abs = x => x < 0n ? -x : x;
function gcd(a, b) { a=abs(a); b=abs(b); while(b) [a,b]=[b,a%b]; return a; }
function fraction(s) { const [a,b="1"]=String(s).split("/"); return [BigInt(a),BigInt(b)]; }
function floor(a,b) { check(b>0n,"positive exact denominator"); return a>=0n ? a/b : -((-a+b-1n)/b); }
const mod = (a,q) => (a%q+q)%q;
const dot = (a,b) => a.reduce((s,x,i)=>s+x*b[i],0n);
function inverse(a,q) {
  if(q===1n)return 0n;
  let [r,s,x,y]=[q,mod(a,q),0n,1n];
  while(s) { const k=r/s; [r,s,x,y]=[s,r-k*s,y,x-k*y]; }
  check(r===1n,"quotient pivot unit"); return mod(x,q);
}
function pythonJSON(x) {
  if(Array.isArray(x))return "["+x.map(pythonJSON).join(", ")+"]";
  if(x!==null&&typeof x==="object")return "{"+Object.keys(x).sort().map(k=>JSON.stringify(k)+": "+pythonJSON(x[k])).join(", ")+"}";
  if(typeof x==="number")check(Number.isSafeInteger(x),"safe JSON fingerprint integer");
  return JSON.stringify(x);
}
const same = (a,b,m) => check(JSON.stringify(a)===JSON.stringify(b),m);
function binomial(n,k) { let a=1n; for(let j=1;j<=k;j++)a=a*BigInt(n-j+1)/BigInt(j); return a; }
function compile(saved) {
  return saved.bases.flatMap(basis=> {
    const R=basis.rows.map(r=>r.map(BigInt)), V=basis.directions.map(r=>r.vector.map(BigInt));
    const inner=V.map(v=>R.map(r=>dot(v,r)));
    inner.forEach((row,i)=> {
      check(row[i]>0n&&row.slice(0,i).every(x=>x===0n),"positive triangular GS projections");
      const [a,b]=fraction(basis.directions[i].multiplier);
      check(a*row[i]===b,"projection reciprocal");
    });
    const kernel=R.map(row=>Array.from({length:row.length/3},(_,j)=>[-row[3*j+1]/3n,-row[3*j+2]/3n]).flat());
    return saved.offsets.map(offset=> {
      const off=offset.map(fraction), D=off.reduce((d,[,b])=>d/gcd(d,b)*b,1n);
      const numerator=off.map(([a,b])=>a*(D/b));
      return {R,V,inner,kernel,D,shift:V.map(v=>dot(v,numerator))};
    });
  });
}
let trials=0, decodes=0, rounding=0, pairs=0, confidenceChecks=0, unionNumerator=0n, unionDenominator=1n;
for(const savedCase of report.cases) {
  const original=source.planted_geometry_probes[savedCase.fixture_probe_index], prepared=original.prepared;
  const A=savedCase.labels.map(BigInt), Q=BigInt(savedCase.Q), M=A.length/2;
  same(savedCase.labels,original.labels,"original source labels");
  check(Q===BigInt(original.modulus)&&Q===3n**BigInt(M+1)&&savedCase.root_digits===M+2,"native underfull scale");
  const key={labels:A.map(Number),Q:Number(Q),bases:prepared.bases.map(b=>b.rows.map(r=>r.map(Number))),offsets:prepared.offsets};
  const hash=crypto.createHash("sha256").update(pythonJSON(key)).digest("hex");
  check(hash===savedCase.fingerprint&&hash===savedCase.training.fingerprint,"frozen policy fingerprint");
  check(savedCase.training.training_words===512&&!savedCase.training.trained_from_target_or_unknown_phase,"public training costs/access");
  const charts=compile(prepared), catalogs=savedCase.sparse_live_catalog.map(patterns=>patterns.map(sparse=> {
    const p=Array(2*M).fill(0n), seen=new Set();
    for(const [i,x] of sparse) { check(Number.isInteger(i)&&i>=0&&i<2*M&&!seen.has(i)&&Number.isSafeInteger(x)&&x!==0,"canonical sparse pattern"); p[i]=BigInt(x); seen.add(i); }
    return p;
  }));
  check(catalogs.length===charts.length,"full chart schedule");
  catalogs.forEach((p,i)=> {
    check(p.length<=64&&p.length===savedCase.actual_catalog_sizes[1][i]&&p[0].every(x=>x===0n),"bounded catalog with charged Babai slot");
    check(new Set(p.map(x=>x.join(","))).size===p.length,"unique catalog patterns");
  });
  const G=A.reduce((g,a)=>gcd(g,a),Q), q=Q/G, pivot=A.findIndex(a=>gcd(a/G,q)===1n), inv=inverse(A[pivot]/G,q);
  for(const t of savedCase.uniform_target_trials) {
    const target=BigInt(t.target), found=[], traces=[];
    const cost={candidate_decodes:0,rounding_steps:0,non_shell_candidates:0,duplicate_words:0};
    let status="CATALOG_EXHAUSTED_NOT_UNSAT_PROOF";
    if(target%G)status="DIVISIBILITY_CERTIFIED_EMPTY";
    else {
      const z0=Array(2*M).fill(0n); z0[pivot]=mod((target/G)*inv,q);
      const T=Array.from({length:M},(_,j)=>[2n-3n*(z0[2*j]+z0[2*j+1]),-1n+3n*z0[2*j],-1n+3n*z0[2*j+1]]).flat();
      outer: for(let h=0;h<charts.length;h++) {
        const c=charts[h], initial=c.V.map((v,i)=>c.D*dot(T,v)+c.shift[i]);
        for(let k=0;k<catalogs[h].length;k++) {
          const H=[...initial], coeff=Array(2*M).fill(0n);
          for(let i=2*M-1;i>=0;i--) {
            const denominator=c.D*c.inner[i][i];
            coeff[i]=floor(2n*H[i]+denominator,2n*denominator)+catalogs[h][k][i];
            for(let j=0;j<i;j++)H[j]-=c.D*coeff[i]*c.inner[j][i];
          }
          cost.candidate_decodes++; cost.rounding_steps+=2*M;
          const z=[], word=[];
          for(let j=0;j<M;j++) {
            const a=z0[2*j]+coeff.reduce((s,x,i)=>s+x*c.kernel[i][2*j],0n);
            const b=z0[2*j+1]+coeff.reduce((s,x,i)=>s+x*c.kernel[i][2*j+1],0n);
            if(!((a===0n&&b===0n)||(a===1n&&b===0n)||(a===0n&&b===1n)))break;
            z.push(Number(a),Number(b)); word.push(a===1n?1:b===1n?2:0);
          }
          if(word.length!==M) { cost.non_shell_candidates++; continue; }
          check(mod(word.reduce((s,x,i)=>s+(x?A[2*i+x-1]:0n),0n),Q)===target,"original modular witness");
          if(found.some(w=>JSON.stringify(w)===JSON.stringify(word))) { cost.duplicate_words++; continue; }
          found.push(word); traces.push({chart:h,pattern_index:k,word,integer_coset_coordinates:z,reduced_basis_coefficients:coeff.map(Number),exact_original_norm:String(6*M)});
          if(found.length===2) { status="VERIFIED_CATALOG_PAIR_NO_COVERAGE_THEOREM"; break outer; }
        }
      }
    }
    same(found,t.witnesses,"all actual witnesses incl exhausted paths");
    same(found.length===2?found:[],t.pair,"distinct pair result");
    same(traces,t.accepted_traces,"exact accepted coefficient traces");
    check(status===t.status,"actual target status");
    for(const [k,v] of Object.entries(cost))check(v===t.cost[k],"charged "+k);
    check(t.cost.training_words_per_fresh_label_attempt===512&&t.cost.original_lll_preparations_per_fresh_labels===prepared.bases.length,"fresh-label preparation costs");
    trials++; decodes+=cost.candidate_decodes; rounding+=cost.rounding_steps; pairs+=found.length===2;
  }
  for(const bound of savedCase.collision_confidence) {
    const n=bound.independent_word_pairs, k=bound.successes;
    check(n===256&&k>=0&&k<=n,"disjoint collision trials");
    const [a,b]=fraction(bound.conditional_collision_upper_assuming_IID_words), [u,v]=fraction(bound.per_chart_failure_probability);
    if(k<n) {
      let numerator=0n;
      for(let j=0;j<=k;j++)numerator+=binomial(n,j)*a**BigInt(j)*(b-a)**BigInt(n-j);
      check(numerator*v<=u*b**BigInt(n),"conservative exact binomial endpoint");
    } else check(a===b,"all-success collision endpoint");
    unionNumerator=unionNumerator*v+u*unionDenominator; unionDenominator*=v;
    const g=gcd(unionNumerator,unionDenominator); unionNumerator/=g; unionDenominator/=g;
    confidenceChecks++;
  }
}
check(20n*unionNumerator<=unionDenominator,"Bonferroni failure bound, no independent-chart assumption");
check(!report.polynomial_pair_finder_proved&&!report.novelty_claim&&report.target_adaptive_repairs_excluded_from_catalog_obstruction,"claims remain scoped");
console.log(JSON.stringify({status:"independent_catalog_target_replay_passed",trials,decodes,rounding,pairs,confidenceChecks,
  independentLLLSearch:false,publicPRNGTrainingReplayed:false,exactSmallCensusReplayed:false,populationCoverageProved:false}));
