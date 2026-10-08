"use strict";
// Original integer kernels, exact rational primal/Farkas proofs and native MITM.
const fs=require("fs"),path=require("path");
const load=name=>JSON.parse(fs.readFileSync(path.join(__dirname,"../phase_workbench/"+name+".json"),"utf8"));
const source=load("ternary_pair_cell_coverage"), report=load("ternary_prefix_integrality"), catalog=load("ternary_repair_catalog");
const abs=x=>x<0n?-x:x;
function check(x,m){if(!x)throw Error(m);}
function gcd(a,b){a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a;}
function F(a,b=1n){check(b!==0n,"nonzero rational denominator");if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];}
function integer(x){if(typeof x==="number")check(Number.isSafeInteger(x),"lossless integer");return BigInt(x);}
function fraction(x){const [a,b="1"]=String(x).split("/");return F(BigInt(a),BigInt(b));}
const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]), neg=a=>[-a[0],a[1]], sub=(a,b)=>add(a,neg(b));
const mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]), div=(a,b)=>F(a[0]*b[1],a[1]*b[0]);
const eq=(a,b)=>a[0]*b[1]===b[0]*a[1], le=(a,b)=>a[0]*b[1]<=b[0]*a[1];
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0n), mod=(a,q)=>(a%q+q)%q;
const qdot=(a,b)=>a.reduce((s,x,i)=>add(s,mul(x,F(b[i]))),F(0n));
function inverse(a,q){if(q===1n)return 0n;let[r,s,x,y]=[q,mod(a,q),0n,1n];while(s){const k=r/s;[r,s,x,y]=[s,r-k*s,y,x-k*y];}check(r===1n,"unit quotient pivot");return mod(x,q);}
function det(matrix){const a=matrix.map(r=>[...r]),n=a.length;let prev=1n,sign=1n;
  for(let k=0;k<n-1;k++){if(!a[k][k]){const p=a.findIndex((r,i)=>i>k&&r[k]);if(p<0)return 0n;[a[k],a[p]]=[a[p],a[k]];sign=-sign;}
    const pivot=a[k][k];for(let i=k+1;i<n;i++)for(let j=k+1;j<n;j++){const x=pivot*a[i][j]-a[i][k]*a[k][j];check(x%prev===0n,"exact Bareiss division");a[i][j]=x/prev;}
    for(let i=k+1;i<n;i++)a[i][k]=0n;prev=pivot;
  }return sign*a[n-1][n-1];}
const sameSet=(a,b,m)=>check(JSON.stringify(a.map(x=>JSON.stringify(x)).sort())===JSON.stringify(b.map(x=>JSON.stringify(x)).sort()),m);
function word(code,M){const w=[];for(let j=0;j<M;j++){w.push(code%3);code=Math.floor(code/3);}return w;}
function tables(A,Q){const M=A.length/2,L=Math.floor(M/2),N1=3**L,N2=3**(M-L);
  if(Math.max(N1,N2)>200000)return null;
  const left=new Map(),right=[];
  for(let i=0;i<N1;i++){const w=word(i,L),v=mod(w.reduce((s,x,j)=>s+(x?A[2*j+x-1]:0n),0n),Q),key=String(v),bucket=left.get(key)||[];bucket.push(i);left.set(key,bucket);}
  for(let i=0;i<N2;i++){const w=word(i,M-L),v=mod(w.reduce((s,x,j)=>s+(x?A[2*(L+j)+x-1]:0n),0n),Q);right.push([v,i]);}
  return {left,right,L,M,assignments:N1+N2};}
let sourceCases=0,referenceAssignments=0,primalProofs=0,farkasProofs=0,targetsChecked=0,windingsChecked=0,exactGaps=0,decoderTrials=0;
const prepared=new Map();
function prepare(c){if(prepared.has(c.fixture_probe_index))return prepared.get(c.fixture_probe_index);
  const old=source.planted_geometry_probes[c.fixture_probe_index],A=c.labels.map(BigInt),Q=BigInt(c.Q),M=A.length/2,d=2*M;
  check(c.fingerprint===catalog.cases[c.fixture_probe_index].fingerprint,"frozen public geometry identity");
  check(JSON.stringify(c.labels)===JSON.stringify(old.labels)&&c.Q===old.modulus,"original native source labels");
  const saved=old.prepared.bases[0],R=saved.rows.map(r=>r.map(BigInt)),V=saved.directions.map(r=>r.vector.map(BigInt)),N=V.map(v=>dot(v,v));
  const K=R.map(r=>{check(r.length===3*M&&r.every(x=>x%3n===0n),"integer embedded kernel row");const k=[];
    for(let j=0;j<M;j++){check(r[3*j]+r[3*j+1]+r[3*j+2]===0n,"A2 row plane");k.push(-r[3*j+1]/3n,-r[3*j+2]/3n);}check(mod(dot(A,k),Q)===0n,"original kernel membership");return k;});
  const G=A.reduce((g,x)=>gcd(g,x),Q),q=Q/G,pivot=A.findIndex(a=>gcd(a/G,q)===1n),inv=inverse(A[pivot]/G,q);
  check(R.length===d&&abs(det(K))===q,"complete original integer kernel");
  for(let i=0;i<d;i++){const C=dot(R[i],V[i]);check(C>0n&&N[i]>0n,"positive GS orientation");
    check(V[i].reduce((g,x)=>gcd(g,x),0n)===1n,"primitive GS vector");
    for(let j=0;j<M;j++)check(V[i][3*j]+V[i][3*j+1]+V[i][3*j+2]===0n,"GS native plane");
    for(let j=0;j<i;j++)check(dot(R[j],V[i])===0n,"GS earlier-span orthogonality");
    const coeff=V.slice(0,i+1).map((v,j)=>F(dot(R[i],v),N[j]));
    for(let k=0;k<3*M;k++)check(eq(coeff.reduce((s,x,j)=>add(s,mul(x,F(V[j][k]))),F(0n)),F(R[i][k])),"actual current GS prefix-span reconstruction");
  }
  const ref=tables(A,Q);if(ref)referenceAssignments+=ref.assignments;
  const result={A,Q,M,d,R,K,V,N,G,q,pivot,inv,ref,fibers:new Map(),projectors:new Map()};prepared.set(c.fixture_probe_index,result);sourceCases++;return result;
}
function fiber(base,t){const key=String(t);if(base.fibers.has(key))return base.fibers.get(key);if(!base.ref)return null;
  const {left,right,L,M}=base.ref,result=[];
  for(const [value,code]of right)for(const prefix of left.get(String(mod(t-value,base.Q)))||[])result.push([...word(prefix,L),...word(code,M-L)]);
  base.fibers.set(key,result);targetsChecked++;return result;}
function projector(base,b){if(base.projectors.has(b))return base.projectors.get(b);const G=[];
  for(let j=0;j<base.M;j++){let a=F(0n),c=F(0n),r=F(0n);for(let i=0;i<b;i++){a=add(a,F(base.V[i][3*j]**2n,base.N[i]));r=add(r,F(base.V[i][3*j]*base.V[i][3*j+1],base.N[i]));c=add(c,F(base.V[i][3*j+1]**2n,base.N[i]));}G.push([a,r,c]);}
  base.projectors.set(b,G);return G;}
function blockEnergy(gram,r0,r1){const[a,b,c]=gram,D=sub(mul(a,c),mul(b,b));check(a[0]>=0n&&c[0]>=0n&&D[0]>=0n,"PSD projector restriction");
  if(D[0])return div(add(sub(mul(c,mul(r0,r0)),mul(F(2n),mul(b,mul(r0,r1)))),mul(a,mul(r1,r1))),D);
  if(a[0])return eq(mul(a,r1),mul(b,r0))?div(mul(r0,r0),a):null;
  if(c[0])return r0[0]===0n?div(mul(r1,r1),c):null;
  return r0[0]===0n&&r1[0]===0n?F(0n):null;}
function geometry(base,t,saved){const b=saved.unassigned_rows;check(Number.isInteger(b)&&b>0&&b<base.d,"nontrivial prefix, not vacuous root");
  const c=saved.partial_coefficients.map(BigInt),anchor=saved.anchor_coefficients.map(BigInt);check(c.length===base.d&&anchor.length===base.d&&c.slice(0,b).every(x=>x===0n),"canonical partial coefficients");
  check(anchor.slice(b).every((x,i)=>x===c[b+i]),"anchor retains every assigned coefficient");
  const z0=Array(base.d).fill(0n);check(t%base.G===0n,"nonempty integer coset");z0[base.pivot]=mod((t/base.G)*base.inv,base.q);
  const za=z0.map((x,j)=>x+anchor.reduce((s,a,i)=>s+a*base.K[i][j],0n));
  check(za.map(String).join(",")===saved.anchor_native_coordinates.join(","),"exact integer anchor");
  const T=Array.from({length:base.M},(_,j)=>[2n-3n*(z0[2*j]+z0[2*j+1]),-1n+3n*z0[2*j],-1n+3n*z0[2*j+1]]).flat();
  const H=T.map((x,k)=>x-c.slice(b).reduce((s,a,j)=>s+a*base.R[b+j][k],0n)),p=Array(3*base.M).fill(null).map(()=>F(0n));let spent=F(0n);
  for(let i=b;i<base.d;i++){const x=dot(H,base.V[i]),q=F(x,base.N[i]);spent=add(spent,F(x*x,base.N[i]));for(let j=0;j<p.length;j++)p[j]=add(p[j],mul(q,F(base.V[i][j])));}
  check(eq(spent,fraction(saved.assigned_squared_energy)),"exact assigned prefix energy");const remaining=sub(F(BigInt(6*base.M)),spent);check(remaining[0]>=0n,"parent remains in source shell sphere");
  const P=projector(base,b),domains=[];
  for(let j=0;j<base.M;j++){const D=[];for(let digit=0;digit<3;digit++){const energy=blockEnergy(P[j],sub(F(digit===0?2n:-1n),p[3*j]),sub(F(digit===1?2n:-1n),p[3*j+1]));if(energy&&le(energy,remaining))D.push(digit);}check(D.length,"live parent has nonempty necessary domains");domains.push(D);}
  check(JSON.stringify(domains)===JSON.stringify(saved.allowed_digits),"all retained/excluded native digits independently reconstructed");
  const w=base.K.slice(0,b).map(row=>dot(base.A,row)/base.Q),ka=(dot(base.A,za)-t)/base.Q;
  check(w.map(String).join(",")===saved.winding_coefficients.join(",")&&String(ka)===saved.anchor_winding,"original modular winding map");
  const g=w.reduce((a,x)=>gcd(a,x),0n),upper=(base.A.filter((x,i)=>i%2===0).reduce((s,x,j)=>s+(x>base.A[2*j+1]?x:base.A[2*j+1]),0n)-t)/base.Q;
  // Numerator can be negative; the live random-label controls have positive
  // maxima, but use floor division to retain exact general winding semantics.
  const total=base.A.filter((x,i)=>i%2===0).reduce((s,x,j)=>s+(x>base.A[2*j+1]?x:base.A[2*j+1]),0n)-t;
  const maximum=total>=0n?upper:-((-total+base.Q-1n)/base.Q),windings=[];
  for(let k=0n;k<=maximum;k++)if(g?mod(k-ka,g)===0n:k===ka)windings.push(Number(k));
  check(String(g)===saved.winding_gcd&&JSON.stringify(windings)===JSON.stringify(saved.allowed_integral_windings),"complete allowed winding/gcd schedule");
  return {base,t,b,za,H,domains,w,ka,windings};}
function rows(g,winding){const A=[],B=[],E=[],Fv=[];const K=g.base.K.slice(0,g.b);
  for(let j=0;j<g.base.M;j++){const u=K.map(r=>r[2*j]),v=K.map(r=>r[2*j+1]),s=u.map((x,i)=>x+v[i]);
    A.push(u.map(x=>-x),v.map(x=>-x),s);B.push(g.za[2*j],g.za[2*j+1],1n-g.za[2*j]-g.za[2*j+1]);
    const D=g.domains[j];if(!D.includes(0)){E.push(s);Fv.push(1n-g.za[2*j]-g.za[2*j+1]);}if(!D.includes(1)){E.push(u);Fv.push(-g.za[2*j]);}if(!D.includes(2)){E.push(v);Fv.push(-g.za[2*j+1]);}}
  if(winding!==null){E.push(g.w);Fv.push(BigInt(winding)-g.ka);}for(let j=0;j<E.length;j++){A.push(E[j],E[j].map(x=>-x));B.push(Fv[j],-Fv[j]);}return {A,B};}
function primal(g,cert){if(!cert)return false;check(cert.valid,"only exact valid primal records");const y=cert.rational_offsets.map(fraction);check(y.length===g.b,"complete primal prefix offsets");
  const z=g.za.map((a,j)=>add(F(a),y.reduce((s,x,i)=>add(s,mul(x,F(g.base.K[i][j]))),F(0n))));
  z.forEach((x,j)=>check(eq(x,fraction(cert.original_fractional_coordinates[j])),"exact original fractional coordinates"));
  const digits=[];let vertex=true;
  for(let j=0;j<g.base.M;j++){const prob=[sub(F(1n),add(z[2*j],z[2*j+1])),z[2*j],z[2*j+1]];check(prob.every(x=>x[0]>=0n),"exact triangle nonnegativity");
    for(let d=0;d<3;d++)if(!g.domains[j].includes(d))check(prob[d][0]===0n,"forbidden digit retains zero exact mass");
    const d=prob.findIndex(x=>eq(x,F(1n)));if(d<0)vertex=false;digits.push(d);}
  const wind=div(sub(qdot(z,g.base.A),F(g.t)),F(g.base.Q));check(eq(wind,fraction(cert.winding))&&cert.integral_winding===(wind[1]===1n),"exact original modular winding");
  if(cert.required_winding!==null)check(eq(wind,F(BigInt(cert.required_winding))),"required integral winding retained");
  const actual=vertex&&wind[1]===1n?digits:null;
  check(cert.native_simplex_vertex===vertex&&JSON.stringify(cert.actual_native_word)===JSON.stringify(actual),"fractional, wrong-target vertex and native word distinguished");
  primalProofs++;return true;}
function farkas(g,cert){if(!cert)return false;check(cert.valid,"only valid exact dual records");const {A,B}=rows(g,cert.required_winding),y=cert.nonnegative_inequality_multipliers.map(fraction);
  check(y.length===A.length&&y.every(x=>x[0]>=0n),"complete nonnegative Farkas multipliers");
  for(let j=0;j<g.b;j++)check(y.reduce((s,x,i)=>add(s,mul(x,F(A[i][j]))),F(0n))[0]===0n,"exact annihilation of every unassigned column");
  const rhs=qdot(y,B);check(rhs[0]<0n&&eq(rhs,fraction(cert.exact_combined_rhs)),"strict negative right-hand side, no numerical flag trusted");farkasProofs++;return true;}
function model(cert,winding){if(cert)check(cert.required_winding===winding,"certificate must belong to the enclosing model, not another winding branch");}
function truth(g,saved){const actual=fiber(g.base,g.t);if(!actual){check(saved.native_prefix_words===null,"unbudgeted native truth stays unknown");return null;}
  sameSet(actual,saved.whole_target_fiber,"complete original native target fiber");check(actual.length===saved.whole_target_fiber_size,"whole-fiber size");
  const native=actual.filter(w=>{const e=w.flatMap(d=>[d===0?2n:-1n,d===1?2n:-1n,d===2?2n:-1n]),delta=e.map((x,j)=>x-g.H[j]);
    return g.base.V.slice(g.b).every(v=>dot(delta,v)===0n);});sameSet(native,saved.native_prefix_words,"exact native prefix membership, not planted completion");return native;}
for(const c of report.cases){const base=prepare(c);for(const t of c.trials){if(!t.frontier)continue;
  model(t.prefix_primal.certificate,null);model(t.prefix_farkas&&t.prefix_farkas.certificate,null);
  const g=geometry(base,BigInt(t.target),t.frontier),p=primal(g,t.prefix_primal.certificate),d=farkas(g,t.prefix_farkas&&t.prefix_farkas.certificate),native=truth(g,t.native_truth);
  check(!(p&&d),"primal and Farkas cannot both certify the same model");check(d===t.prefix_relaxation_exactly_obstructed,"prefix dual status");
  sameSet(g.windings,t.integral_winding_trials.map(x=>x.winding_branch),"no favorable winding selection");let all=true,has=false;
  for(const r of t.integral_winding_trials){model(r.certificate,r.winding_branch);model(r.farkas&&r.farkas.certificate,r.winding_branch);
    const p=primal(g,r.certificate),d=farkas(g,r.farkas&&r.farkas.certificate);check(!(p&&d),"fixed-winding primal/dual consistency");all=all&&d;has=has||p;windingsChecked++;}
  check(all===t.all_allowed_windings_exactly_obstructed,"entire winding disjunction checked");if((d||all)&&native)check(native.length===0,"no exact obstruction can reject a real native completion");
  if(t.status==="EXACT_WINDING_PREFIX_INTEGRALITY_GAP"){check(native&&native.length===0&&has,"genuine nontrivial fixed-winding integrality gap");exactGaps++;}
}}
const decoderPath=path.join(__dirname,"../phase_workbench/ternary_prefix_lp_decoder.json");
if(fs.existsSync(decoderPath)){const decoder=JSON.parse(fs.readFileSync(decoderPath,"utf8"));for(const c of decoder.cases){const base=prepare(c);for(const t of c.trials){
  check(t.cost.linear_LP_calls<=t.linear_LP_cap&&t.cost.coefficient_nodes<=t.node_budget,"both LP and coefficient caps charged");
  check((t.linear_certificates||[]).length===t.cost.linear_obstruction_prunes,"every runtime linear prune has a retained proof");
  for(const r of t.linear_certificates){model(r.certificate,null);const g=geometry(base,BigInt(t.target),r.frontier);check(farkas(g,r.certificate),"runtime LP cannot prune without an exact proof");}
  const actual=fiber(base,BigInt(t.target));if(t.complete_fiber){check(actual,"independent reference needed for completion claim");sameSet(actual,t.witnesses,"all completed decoder fibers");}
  const unique=new Set(t.witnesses.map(w=>JSON.stringify(w)));check(unique.size===t.witnesses.length,"distinct runtime witnesses");
  for(const w of t.witnesses)check(w.length===base.M&&w.every(x=>Number.isInteger(x)&&x>=0&&x<3)&&mod(w.reduce((s,x,j)=>s+(x?base.A[2*j+x-1]:0n),0n),base.Q)===BigInt(t.target),"verified original native runtime word");
  check(JSON.stringify(t.pair)===JSON.stringify(t.witnesses.length>=2?t.witnesses.slice(0,2):[]),"pair ledger, no duplicate signal");decoderTrials++;
}}}
check(!report.polynomial_pair_finder_proved&&!report.population_obstruction_proved&&!report.novelty_claim,"proof claims remain scoped");
// Independently check the newer discrete audit without using FLINT or SciPy.
let modularTrials=0,modularWords=0,modularFullSupports=0,modularFourierSupports=0;
function parity(x){let p=0;while(x){p^=1;x&=x-1n;}return p;}
function binaryRank(rows){const pivots=new Map();for(const row of rows){let x=row.reduce((s,a,i)=>s|((a&1n)<<BigInt(i)),0n);
  while(x){const j=x.toString(2).length-1;if(pivots.has(j))x^=pivots.get(j);else{pivots.set(j,x);break;}}}return pivots.size;}
function modular(g,t){const s=t.shadow,d=g.base.d,H=s.quotient_annihilator.map(r=>r.map(integer)),r=s.quotient_dimension;
  check(s.field_prime===2&&s.native_coordinate_count===d,"actual binary native-coordinate shadow");
  check(H.length===r&&H.every(h=>h.length===d&&h.every(x=>x===0n||x===1n)),"binary quotient dimensions");
  const baseline=g.domains.map(D=>D[0]);check(JSON.stringify(baseline)===JSON.stringify(s.baseline_word),"actual allowed baseline word");
  const zbase=baseline.flatMap(x=>[x===1?1n:0n,x===2?1n:0n]),binary=[],single=[],full=[],extra=[];
  const code=z=>H.reduce((x,h,i)=>x|(mod(dot(h,z),2n)<<BigInt(i)),0n);
  for(let j=0;j<g.base.M;j++){const D=g.domains[j];if(D.length===1)single.push(j);
    if(D.length===2){binary.push(j);const delta=Array(d).fill(0n);if(D[0])delta[2*j+D[0]-1]-=1n;if(D[1])delta[2*j+D[1]-1]+=1n;extra.push(delta);}
    if(D.length===3){const u=Array(d).fill(0n),v=Array(d).fill(0n);u[2*j]=1n;v[2*j+1]=1n;full.push({block:j,choices:["0",String(code(u)),String(code(v))]});}}
  check(JSON.stringify(binary)===JSON.stringify(s.binary_blocks)&&JSON.stringify(single)===JSON.stringify(s.singleton_blocks),"complete binary/singleton domains");
  check(JSON.stringify(full)===JSON.stringify(s.full_blocks),"original full native triangle syndrome images");
  const K=g.base.K.slice(0,g.b),rankK=binaryRank(K),rank=binaryRank([...K,...extra]);
  check(rankK===s.original_prefix_rank_mod2&&d-rankK===s.original_shadow_dimension&&rank-rankK===s.eliminated_binary_span_rank,"binary elimination ranks");
  check(binaryRank(H)===r&&r===d-rank,"FULL annihilator, not a selected projection");
  for(const h of H)for(const k of [...K,...extra])check(mod(dot(h,k),2n)===0n,"every quotient row annihilates original prefix and binary domains");
  check(code(g.za.map((a,j)=>a-zbase[j]))===integer(s.target_syndrome),"original anchor target syndrome");
  const dp=t.support,size=1n<<BigInt(r),budget=BigInt(dp.cost.preflight_budget);
  check(String(size)===dp.cost.ambient_states,"complete ambient group charged");
  if(size>budget){check(dp.status==="SHADOW_PREFLIGHT_UNKNOWN"&&dp.target_reachable===null&&dp.cost.xor_transitions===0&&dp.support_history.length===0,"no partial table called empty");}
  else{let support=new Set([0]),transitions=0,processed=0;const history=[1];
    for(const block of full){if(BigInt(support.size)===size)break;const choices=new Set(block.choices.map(Number)),next=new Set();transitions+=support.size*choices.size;
      for(const x of support)for(const c of choices)next.add(x^c);support=next;processed++;history.push(support.size);}
    const saturated=BigInt(support.size)===size,reachable=support.has(Number(s.target_syndrome));
    check(dp.target_reachable===reachable&&dp.support_saturated===saturated&&dp.final_support_size===support.size,"exact complete modular support");
    check(dp.cost.xor_transitions===transitions&&dp.cost.blocks_processed===processed&&dp.cost.peak_support_states===support.size&&JSON.stringify(dp.support_history)===JSON.stringify(history),"all support transitions retained");
    check(dp.status===(saturated?"ALL_MOD2_PREFIX_PREDICATES_POWERLESS":reachable?"MOD2_TARGET_REACHABLE_NOT_NATIVE":"MOD2_NATIVE_PREFIX_OBSTRUCTION"),"discrete interpretation");if(saturated)modularFullSupports++;}
  const f=t.fourier;
  if(f.status==="FOURIER_PREFLIGHT_UNKNOWN"){check(size>budget&&f.characters_checked===0&&!f.proves_full_support,"Fourier guard not a proof");}
  else{const histogram=Array(full.length+1).fill(0);for(let h=1n;h<size;h++){let weight=0;for(const b of full)if(parity(h&BigInt(b.choices[1]))||parity(h&BigInt(b.choices[2])))weight++;histogram[weight]++;}
    const denominator=3n**BigInt(full.length),numerator=histogram.reduce((a,n,w)=>a+BigInt(n)*3n**BigInt(full.length-w),0n),lower=denominator>numerator?denominator-numerator:0n;
    check(JSON.stringify(histogram)===JSON.stringify(f.nonzero_character_weight_histogram)&&String(numerator)===f.absolute_nontrivial_mass_numerator&&String(denominator)===f.common_denominator,"exact character weight enumerator");
    check(JSON.stringify([String(lower),String(size*denominator)])===JSON.stringify(f.every_syndrome_probability_lower_bound)&&f.proves_full_support===(numerator<denominator),"exact all-syndrome Fourier lower bound");
    check(f.characters_checked===Number(size-1n)&&f.parity_evaluations===2*full.length*Number(size-1n),"Fourier work charged");if(f.proves_full_support){check(dp.support_saturated,"Fourier proof agrees with complete support");modularFourierSupports++;}}
  const proposal=t.modular_witness,cert=proposal.certificate;
  check(proposal.cost.affine_proposals<=proposal.cost.proposal_budget,"all rejected affine proposals charged");
  if(cert){check(cert.valid&&cert.field_prime===2&&!cert.integer_prefix_membership_proved&&cert.certificate_only_proves_mod2_feasibility,"modular word not promoted to integer completion");
    const w=cert.native_word,a=cert.prefix_coefficients_mod2;check(w.length===g.base.M&&w.every((x,j)=>Number.isInteger(x)&&g.domains[j].includes(x)),"actual domain-valid native word");
    check(a.length===g.b&&a.every(x=>x===0||x===1),"complete binary prefix coefficients");const z=w.flatMap(x=>[x===1?1n:0n,x===2?1n:0n]);
    for(let j=0;j<d;j++)check(mod(z[j]-g.za[j]-a.reduce((v,x,i)=>v+BigInt(x)*K[i][j],0n),2n)===0n,"standalone native modular witness in ORIGINAL prefix");
    const original=mod(dot(z,g.base.A),g.base.Q)===g.t;check(cert.original_target_matches===original,"modular/original target distinction");check(dp.target_reachable!==false,"word agrees with completed support");modularWords++;}
  modularTrials++;
}
const modularPath=path.join(__dirname,"../phase_workbench/ternary_prefix_modular.json");
if(fs.existsSync(modularPath)){const m=JSON.parse(fs.readFileSync(modularPath,"utf8"));
  check(!m.polynomial_pair_finder_proved&&!m.population_obstruction_proved&&!m.novelty_claim,"modular proof claims stay scoped");
  sameSet(m.cases.map(x=>x.fixture_probe_index),report.cases.map(x=>x.fixture_probe_index),"complete matched modular case schedule");
  for(const c of m.cases){const original=report.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index);check(original&&original.fingerprint===c.fingerprint,"actual frozen prefix geometry");const base=prepare(original);
    sameSet(c.trials.map(x=>x.target),original.trials.filter(x=>x.prefix_primal.certificate).map(x=>x.target),"every feasible-prefix target tested, not favorable selection");
    for(const t of c.trials){const old=original.trials.find(x=>x.target===t.target);check(old&&old.prefix_primal.certificate,"new mechanism tested on actually feasible relaxation");
      check(old.status===t.prefix_audit_status&&t.integer_winding_gap===(old.status==="EXACT_WINDING_PREFIX_INTEGRALITY_GAP"),"same source-prefix classification");modular(geometry(base,BigInt(t.target),old.frontier),t);}}
}
let momentPrefixes=0,momentPrimalProofs=0,momentDualProofs=0,momentEliminatedPrefixes=0;
function commonIntegers(values){const q=values.map(fraction),den=q.reduce((d,x)=>d/gcd(d,x[1])*x[1],1n);return {den,values:q.map(x=>x[0]*(den/x[1]))};}
function momentModel(g,winding){const D=g.domains,M=g.base.M,variables=[],index=new Map(),E=[],B=[];
  const key=x=>JSON.stringify(x),variable=x=>{index.set(key(x),variables.length);variables.push(x);};
  for(let j=0;j<M;j++)for(const a of D[j])variable(["p",j,a]);
  for(let i=0;i<M;i++)for(let j=i+1;j<M;j++)for(const a of D[i])for(const b of D[j])variable(["J",i,a,j,b]);
  const joint=(i,a,j,b)=>i<j?["J",i,a,j,b]:["J",j,b,i,a];
  function equation(terms,rhs){const row=new Map();for(const[k,a]of terms){const i=index.get(key(k));check(i!==undefined,"actual native moment variable");row.set(i,(row.get(i)||0n)+a);}for(const[i,a]of row)if(!a)row.delete(i);E.push(row);B.push(rhs);}
  for(let j=0;j<M;j++)equation(D[j].map(a=>[["p",j,a],1n]),1n);
  for(let i=0;i<M;i++)for(let j=i+1;j<M;j++){
    for(const a of D[i])equation([...D[j].map(b=>[joint(i,a,j,b),1n]),[["p",i,a],-1n]],0n);
    for(const b of D[j])equation([...D[i].map(a=>[joint(i,a,j,b),1n]),[["p",j,b],-1n]],0n);}
  const original=[];
  for(let i=g.b;i<g.base.d;i++){const h=g.base.V[i],coeff=Array.from({length:M},(_,j)=>[0n,h[3*j]-h[3*j+1],h[3*j]-h[3*j+2]]);
    const rhs=coeff.reduce((x,c,j)=>x+c[1]*g.za[2*j]+c[2]*g.za[2*j+1],0n);original.push([coeff,rhs]);}
  if(winding!==null)original.push([Array.from({length:M},(_,j)=>[0n,g.base.A[2*j],g.base.A[2*j+1]]),g.t+g.base.Q*BigInt(winding)]);
  for(const[a,rhs]of original){const mean=[];for(let j=0;j<M;j++)for(const d of D[j])mean.push([["p",j,d],a[j][d]]);equation(mean,rhs);
    for(let i=0;i<M;i++)for(const d of D[i]){const terms=[[["p",i,d],a[i][d]-rhs]];
      for(let j=0;j<M;j++)if(j!==i)for(const e of D[j])terms.push([joint(i,d,j,e),a[j][e]]);equation(terms,0n);}}
  return {variables,E,B,sourceEquations:original};}
const momentsPath=path.join(__dirname,"../phase_workbench/ternary_prefix_moments.json");
if(fs.existsSync(momentsPath)){const m=JSON.parse(fs.readFileSync(momentsPath,"utf8"));
  check(!m.polynomial_pair_finder_proved&&!m.population_obstruction_proved&&!m.novelty_claim,"coupled moments not a native solver");
  const scheduled=report.cases.flatMap(c=>c.trials.filter(t=>t.status==="EXACT_WINDING_PREFIX_INTEGRALITY_GAP").map(t=>[c.fixture_probe_index,t.target])).slice(0,m.prefix_budget);
  sameSet(m.cases.flatMap(c=>c.trials.map(t=>[c.fixture_probe_index,t.target])),scheduled,"complete explicit prefix pilot, no favorable selection");
  for(const c of m.cases){const original=report.cases.find(x=>x.fixture_probe_index===c.fixture_probe_index);check(original&&original.fingerprint===c.fingerprint,"same native prefix source");const base=prepare(original);
    for(const t of c.trials){const old=original.trials.find(x=>x.target===t.target),g=geometry(base,BigInt(t.target),old.frontier);
      sameSet(t.all_allowed_windings,g.windings,"full original winding disjunction");sameSet(t.winding_trials.map(x=>x.winding_branch),g.windings,"every coupled winding tested");let all=true,has=false;
      for(const run of t.winding_trials){const model=momentModel(g,run.winding_branch),{E,B,variables}=model;
        check(run.cost.variables===variables.length&&run.cost.equations===E.length&&run.cost.nonzero_entries===E.reduce((n,row)=>n+row.size,0),"full coupled model size retained");
        check(!(run.primal&&run.dual),"no simultaneous primal/dual proof");
        if(run.primal){const c=run.primal;check(c.valid&&c.required_winding===run.winding_branch&&!c.global_native_distribution_proved&&!c.integer_prefix_completion_proved,"coupled continuation is not global native existence");
          const {den,values:x}=commonIntegers(c.moments);check(x.length===variables.length&&x.every(a=>a>=0n),"all native moments nonnegative");
          for(let i=0;i<E.length;i++){let rhs=0n;for(const[j,a]of E[i])rhs+=x[j]*a;check(rhs===B[i]*den,"every original marginal/conditioned source identity exact");}momentPrimalProofs++;has=true;}
        if(run.dual){const c=run.dual;check(c.valid&&c.required_winding===run.winding_branch&&c.proves_no_coupled_moments,"signed equation certificate in correct winding");
          const {den,values:y}=commonIntegers(c.signed_equation_multipliers);check(y.length===E.length,"complete coupled dual equation multipliers");const columns=Array(variables.length).fill(0n);
          for(let i=0;i<E.length;i++)if(y[i])for(const[j,a]of E[i])columns[j]+=y[i]*a;
          check(columns.every(a=>a>=0n)&&columns.length===c.exact_column_coefficients.length&&columns.every((a,j)=>{const q=fraction(c.exact_column_coefficients[j]);return a*q[1]===q[0]*den;}),"all original native moment columns exact nonnegative");
          const rhs=dot(y,B),q=fraction(c.exact_combined_rhs);check(rhs<0n&&rhs*q[1]===q[0]*den,"strict exact contradiction, no floating LP status trusted");momentDualProofs++;}
        all=all&&!!run.dual;
      }
      check(t.prefix_eliminated===all&&t.coupled_moment_survives===has,"complete winding verdict, not one favorable lift");if(all)momentEliminatedPrefixes++;momentPrefixes++;
    }}check(m.prefixes_analyzed===momentPrefixes,"explicit analyzed prefix count");
}
console.log(JSON.stringify({status:"independent_native_prefix_primal_dual_and_truth_checks_passed",sourceCases,referenceAssignments,targetsChecked,
  primalProofs,farkasProofs,windingsChecked,exactWindingGaps:exactGaps,decoderTrials,modularTrials,modularWords,modularFullSupports,modularFourierSupports,
  momentPrefixes,momentPrimalProofs,momentDualProofs,momentEliminatedPrefixes,
  fullEnumerationTreeReplayed:false,populationObstructionProved:false}));
module.exports={check,gcd,abs,F,fraction,eq,det,commonIntegers,sameSet,prepare,geometry,momentModel,report,load};
