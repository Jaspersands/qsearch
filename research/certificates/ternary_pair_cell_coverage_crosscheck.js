"use strict";
// Independent exact GS-direction geometry, native error moments and word census.
const fs = require("fs"), path = require("path");
const report = JSON.parse(fs.readFileSync(path.join(__dirname, "../phase_workbench/ternary_pair_cell_coverage.json"), "utf8"));
function check(x, m) { if (!x) throw Error(m); }
const abs = x => x < 0n ? -x : x;
function gcd(a, b) { a=abs(a); b=abs(b); while (b) [a,b]=[b,a%b]; return a; }
function F(a, b=1n) { if (b < 0n) { a=-a; b=-b; } const g=gcd(a,b); return [a/g,b/g]; }
function fraction(s) { const p=s.split("/").map(BigInt); return F(p[0],p[1]||1n); }
const add = (a,b) => F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const mul = (a,b) => F(a[0]*b[0],a[1]*b[1]);
const eq = (a,b) => a[0]*b[1] === b[0]*a[1];
const dot = (a,b) => a.reduce((s,x,i)=>s+x*b[i],0n);
const mod = (a,q) => ((a%q)+q)%q;
function floor(a,b) { return a>=0n ? a/b : -((-a+b-1n)/b); }
function det(matrix) {
  const a=matrix.map(r=>[...r]), n=a.length; let prior=1n, sign=1n;
  for(let k=0;k<n-1;k++) {
    if(!a[k][k]) { const p=a.findIndex((r,i)=>i>k&&r[k]); if(p<0)return 0n; [a[k],a[p]]=[a[p],a[k]]; sign=-sign; }
    const pivot=a[k][k];
    for(let i=k+1;i<n;i++)for(let j=k+1;j<n;j++) { const x=pivot*a[i][j]-a[i][k]*a[k][j]; check(x%prior===0n,"integer Bareiss division"); a[i][j]=x/prior; }
    for(let i=k+1;i<n;i++)a[i][k]=0n;
    prior=pivot;
  }
  return sign*a[n-1][n-1];
}
function sameCounts(actual, saved, m) {
  const keys = new Set([...Object.keys(actual),...Object.keys(saved)]);
  for(const k of keys)check((actual[k]||0)===(saved[k]||0),m+" key="+k);
}
function words(M) { let result=[[]]; for(let i=0;i<M;i++)result=result.flatMap(w=>[0,1,2].map(x=>[...w,x])); return result; }
const count = (map,key) => { map[key]=(map[key]||0)+1; };
function binomial(n,k) { let x=1n; for(let i=1;i<=k;i++)x=x*BigInt(n-i+1)/BigInt(i); return x; }
function listSize(d,k,B) { let n=0n; for(let i=0;i<=k;i++)n+=binomial(d,i)*BigInt(2*B)**BigInt(i); return n; }
let basisRows=0, momentRows=0, exactWords=0, probeWords=0, nativeTargets=0;
function prepare(saved,A,Q) {
  const M=A.length/2, G=A.reduce((g,x)=>gcd(g,x),Q), offsets=saved.offsets.map(r=>r.map(fraction)), charts=[];
  for(const basis of saved.bases) {
    const rows=basis.rows.map(r=>r.map(BigInt));
    check(rows.length===2*M,"full original lattice rank");
    for(const R of rows) {
      check(R.length===3*M && R.every(x=>x%3n===0n),"integer 3*A2 embedding");
      const l=[];
      for(let j=0;j<R.length;j+=3) { check(R[j]+R[j+1]+R[j+2]===0n,"A2 block plane"); l.push(-R[j+1]/3n,-R[j+2]/3n); }
      check(mod(dot(A,l),Q)===0n,"original scalar kernel membership");
    }
    check(det(rows.map(a=>rows.map(b=>dot(a,b))))===3n**BigInt(5*M)*(Q/G)**2n,"complete kernel Gram volume");
    const direction=[];
    basis.directions.forEach((r,i)=> {
      const v=r.vector.map(BigInt), C=dot(rows[i],v), norm=dot(v,v);
      check(v.reduce((g,x)=>gcd(g,x),0n)===1n&&C>0n,"primitive GS orientation");
      for(let j=0;j<i;j++)check(dot(v,rows[j])===0n,"GS orthogonality to entire earlier span");
      for(let j=0;j<v.length;j+=3)check(v[j]+v[j+1]+v[j+2]===0n,"native GS block plane");
      check(eq(fraction(r.multiplier),F(1n,C)),"GS projection reciprocal");
      const prefix=[...direction.map(x=>x.v),v];
      for(let k=0;k<v.length;k++) {
        const reconstructed=prefix.reduce((s,u)=>add(s,F(dot(rows[i],u)*u[k],dot(u,u))),F(0n));
        check(eq(reconstructed,F(rows[i][k])),"GS projection lies in the actual current row prefix span");
      }
      const moments=r.unperturbed_uniform_word_moments;
      const second=F(3n*norm,C*C), third=F(9n*v.reduce((s,x)=>s+x**3n,0n),C**3n);
      let block=0n; for(let j=0;j<v.length;j+=3)block+=(v[j]**2n+v[j+1]**2n+v[j+2]**2n)**2n;
      const fourth=F(54n*norm*norm-27n*block,2n*C**4n);
      check(eq(fraction(moments.mean),F(0n))&&eq(fraction(moments.variance),second),"exact source mean/variance");
      check(eq(fraction(moments.centered_third),third)&&eq(fraction(moments.centered_fourth),fourth),"native skew/fourth moments");
      check(eq(fraction(moments.raw_second),second)&&eq(fraction(moments.raw_fourth),fourth),"unperturbed raw moments");
      direction.push({v,C}); momentRows++; basisRows++;
    });
    for(const offset of offsets) {
      charts.push(direction.map(({v,C})=> {
        const off=v.reduce((s,x,j)=>add(s,mul(offset[j],F(x))),F(0n));
        return {digits:Array.from({length:M},(_,j)=>v.slice(3*j,3*j+3).map(x=>3n*x*off[1])),shift:off[0],den:C*off[1]};
      }));
    }
  }
  check(charts.length===saved.number_charts,"public full scheduled charts"); return charts;
}
function errors(word,chart) {
  return chart.map(r=> { const x=floor(2n*(r.shift+word.reduce((s,x,j)=>s+r.digits[j][x],0n))+r.den,2n*r.den);
    check(abs(x)<=BigInt(Number.MAX_SAFE_INTEGER),"exact safe integer rounding result"); return Number(x); });
}
function cost(e,B) { return e.some(x=>Math.abs(x)>B) ? null : e.filter(x=>x).length; }
function best(e,B) { const c=e.map(x=>cost(x,B)).filter(x=>x!==null); return c.length ? Math.min(...c) : null; }
for(const control of report.exact_controls) {
  const A=control.labels.map(BigInt), c=control.census, Q=BigInt(c.modulus), M=A.length/2, D=3**M;
  const charts=prepare(control.prepared,A,Q), truth=new Map(), histogram={1:{},2:{}}, buckets={1:new Map(),2:new Map()};
  for(const w of words(M)) {
    const t=mod(w.reduce((s,x,i)=>s+(x?A[2*i+x-1]:0n),0n),Q).toString(), e=charts.map(chart=>errors(w,chart));
    truth.set(t,(truth.get(t)||0)+1); exactWords++;
    for(const B of [1,2]) {
      const k=best(e,B); count(histogram[B],k===null?"beyond_magnitude":String(k));
      if(k!==null) { const b=buckets[B].get(t)||[]; b.push(k); b.sort((x,y)=>x-y); b.length=Math.min(2,b.length); buckets[B].set(t,b); }
    }
  }
  check(c.words_classified===D&&c.true_pair_targets===[...truth.values()].filter(x=>x>=2).length,"entire original source word/fiber census");
  check(BigInt(c.empty_uniform_targets)===Q-BigInt(truth.size),"all empty targets included"); nativeTargets+=Number(Q);
  for(const layer of c.layers) {
    const B=layer.maximum_repair_magnitude, pairs={};
    for(const b of buckets[B].values())if(b.length===2)count(pairs,String(b[1]));
    sameCounts(histogram[B],layer.minimum_word_repairs_histogram,"native word minimum repairs");
    sameCounts(pairs,layer.minimum_pair_repairs_histogram,"second-distinct-witness minimum repairs");
    for(const depth of layer.depths) {
      const k=depth.repairs;
      const n=Object.entries(histogram[B]).filter(([j])=>j!=="beyond_magnitude"&&Number(j)<=k).reduce((s,[j,v])=>s+v,0);
      const p=Object.entries(pairs).filter(([j])=>Number(j)<=k).reduce((s,[j,v])=>s+v,0);
      check(n===depth.recovered_words&&p===depth.pair_covered_targets&&2*p<=n,"word-to-uniform-target pair counting bound");
      check(eq(fraction(depth.gamma_exact_conditional),F(BigInt(n),BigInt(D))),"conditional word fraction");
      check(eq(fraction(depth.beta_exact_conditional_uniform_targets),F(BigInt(p),Q)),"exact uniform-target coverage");
      check(eq(fraction(depth.word_count_pair_coverage_upper),F(BigInt(n),2n*Q)),"deterministic beta upper");
      const lower=Math.max(0,c.true_pair_targets-(D-n));
      check(eq(fraction(depth.full_truth_minus_missing_words_pair_lower),F(BigInt(lower),Q))&&p>=lower,"missing-word pair coverage lower");
      check(BigInt(depth.scheduled_candidates_all_charts)===BigInt(charts.length)*listSize(2*M,k,B),"all forced-repair list costs");
    }
  }
  if(c.missed_pair_target_certificate) {
    const counter=c.missed_pair_target_certificate, t=BigInt(counter.target);
    const fiber=words(M).filter(w=>mod(w.reduce((s,x,j)=>s+(x?A[2*j+x-1]:0n),0n),Q)===t);
    check(JSON.stringify(fiber)===JSON.stringify(counter.complete_actual_fiber)&&fiber.length>=2,"complete real missed pair fiber");
    const signatures=fiber.map(w=>charts.map(chart=>errors(w,chart)));
    check(JSON.stringify(signatures)===JSON.stringify(counter.per_word_per_chart_rounded_errors),"all missed-fiber error witnesses");
    const costs=signatures.map(e=>best(e,1));
    check(JSON.stringify(costs)===JSON.stringify(counter.minimum_repairs_per_word_magnitude_one),"missed native repair costs");
    check(costs.filter(k=>k!==null&&k<=1).length<2,"deterministic single-repair completeness falsified");
    check(counter.actual_decoder_candidate_cost===charts.length*(1+4*M),"actual failed full scheduled list charged");
  }
}
for(const control of report.planted_geometry_probes) {
  const A=control.labels.map(BigInt), Q=BigInt(control.modulus), charts=prepare(control.prepared,A,Q), p=control.probe, histogram={}, mag={};
  check(!p.uniform_target_pair_coverage_estimated&&p.targets_would_be_planted_size_biased,"planted word probe never relabelled as target benchmark");
  const patterns=charts.map(()=>new Map());
  for(const r of p.word_records) {
    const e=charts.map(chart=>errors(r.word,chart)), k=best(e,1), magnitudes=e.map(v=>Math.max(...v.map(Math.abs)));
    check(k===r.minimum_repairs_magnitude_one,"large-root actual source word error signature");
    check(e.every((v,i)=>v.filter(x=>x).length===r.per_chart_nonzero_counts[i]),"per-chart error count");
    check(magnitudes.every((x,i)=>x===r.per_chart_maximum_magnitudes[i]),"per-chart error magnitude");
    e.forEach((v,i)=>{ const key=v.join(","); patterns[i].set(key,(patterns[i].get(key)||0)+1); });
    count(histogram,k===null?"beyond_magnitude":String(k)); count(mag,String(Math.min(...magnitudes))); probeWords++;
  }
  sameCounts(histogram,p.minimum_repairs_magnitude_one_histogram,"entire planted probe histogram");
  sameCounts(mag,p.minimum_chart_maximum_magnitude_histogram,"entire planted magnitude histogram");
  patterns.forEach((counts,i)=> {
    const s=p.repair_pattern_sample_statistics[i], values=[...counts.values()], pairs=values.reduce((n,c)=>n+c*(c-1)/2,0);
    check(s.chart===i&&s.distinct_observed_patterns===counts.size&&s.largest_observed_pattern_count===Math.max(...values),"conditional observed repair patterns");
    check(s.equal_pattern_sample_pairs===pairs,"empirical pattern collisions");
    check(eq(fraction(s.empirical_pair_collision_rate_not_population_proof),F(BigInt(pairs),BigInt(p.samples*(p.samples-1)/2))),"sample collision fraction not true collision probability");
  });
}
check(!report.polynomial_pair_finder_proved&&!report.uniform_target_population_coverage_proved&&!report.novelty_claim,"speedup/proof claims remain blocked");
console.log(JSON.stringify({status:"independent_native_coverage_replay_passed",basisRows,momentRows,exactWords,probeWords,
  uniformTargetsAccounted:nativeTargets,independentLLLSearch:false,populationCoverageProved:false}));
