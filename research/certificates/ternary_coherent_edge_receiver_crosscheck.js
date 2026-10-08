"use strict";
// Exact population/kernel checks plus independent finite native unitary replay.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const report = JSON.parse(fs.readFileSync(process.argv[2] || path.join(__dirname, "../phase_workbench/ternary_coherent_edge_receiver.json"), "utf8"));
function check(ok, msg) { if (!ok) throw Error(msg); }
const abs = x => x < 0n ? -x : x;
function gcd(a,b) { a=abs(a); b=abs(b); while(b) [a,b]=[b,a%b]; return a; }
function F(a,b=1n) { check(b!==0n,"nonzero denominator"); if(b<0n){a=-a;b=-b;} const g=gcd(a,b);return [a/g,b/g]; }
const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]), neg=a=>[-a[0],a[1]],
  sub=(a,b)=>add(a,neg(b)), mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]), div=(a,b)=>F(a[0]*b[1],a[1]*b[0]),
  eq=(a,b)=>a[0]*b[1]===b[0]*a[1], le=(a,b)=>a[0]*b[1]<=b[0]*a[1], sq=a=>mul(a,a);
function Q(s) { check(typeof s==="string","canonical rational string"); const t=s.split("/");check(t.length<=2,"rational grammar"); const f=F(BigInt(t[0]),t.length===2?BigInt(t[1]):1n);check(s===(f[1]===1n?String(f[0]):f[0]+"/"+f[1]),"canonical rational value");return f; }
function I(x) { if(typeof x==="bigint"){check(x>=0n,"nonnegative internal integer");return x;}if(typeof x==="number"){check(Number.isSafeInteger(x),"unsafe JSON integer");return BigInt(x);}check(typeof x==="string"&&/^(0|[1-9][0-9]*)$/.test(x),"canonical large integer");return BigInt(x); }
const N=(x,msg)=>{check(Number.isSafeInteger(x),msg);return x;}, close=(a,b,msg)=>check(Number.isFinite(a)&&Math.abs(a-b)<3e-11,msg);
const mod=(a,q)=>(a%q+q)%q;
function params(P) { P=I(P);check(P>=2n&&(P&(P-1n))===0n,"public power-two index");const bits=P.toString(2).length-1,h=Math.ceil(bits/2),p=F(1n,1n<<BigInt(h));return {P,bits,h,p,rho:sub(F(1n),p)}; }
function kernel(q,r,P) {
  const s=params(P);q=I(q);r=I(r);check(q>=0n&&q<=s.P&&r>=0n&&r<=s.P,"degree range");if(!q||!r)return F(0n);
  const x=F(q,s.P),y=F(r,s.P),a=sq(s.p),b=add(a,mul(mul(F(4n),s.rho),sub(add(x,y),mul(F(2n),mul(x,y)))));
  const den=sub(sq(b),mul(F(64n),mul(sq(s.rho),mul(mul(x,y),mul(sub(F(1n),x),sub(F(1n),y))))));
  const positiveDen=add(add(sq(a),mul(F(8n),mul(mul(a,s.rho),add(mul(x,sub(F(1n),y)),mul(y,sub(F(1n),x)))))),mul(F(16n),mul(sq(s.rho),sq(sub(x,y)))));
  check(eq(den,positiveDen),"complete nonnegative denominator identity");
  check(den[0]>0n,"strict exact kernel denominator");
  return div(mul(div(a,F(s.P)),sub(add(a,mul(F(8n),s.rho)),mul(F(4n),mul(s.rho,add(x,y))))),den);
}
function schedule(c,P,tailBits=16) {
  const s=params(P),T=BigInt(tailBits)*(1n<<BigInt(s.h));
  check(I(c.padded_supports)===s.P&&c.index_bits===s.bits&&c.coin_bits===s.h,"charged schedule dimensions");
  check(eq(Q(c.stop_probability),s.p)&&eq(Q(c.rho),s.rho)&&I(c.cutoff)===T,"shared geometric stop and cutoff");
  check(eq(Q(c.tail_probability_upper),F(1n,1n<<BigInt(tailBits)))&&eq(Q(c.singleton_kernel),kernel(1,1,P)),"exact clipping and singleton kernel");
  check(eq(Q(c.mean_iterations_untruncated),div(s.rho,s.p))&&I(c.mean_reversible_predicate_calls_upper)===(2n<<BigInt(s.h))-1n&&I(c.maximum_reversible_predicate_calls)===2n*T-1n,"exponential mean/worst predicate and coin cost");
  check(c.randomization_shared_across_entire_source===true,"shared time not endpoint-specific");
}
const derivation=fs.readFileSync(path.join(__dirname,"../TERNARY_COHERENT_EDGE_RECEIVER.md"));
check(crypto.createHash("sha256").update(derivation).digest("hex")===report.derivation_sha256,"derivation pinned");
check(report.status==="NATIVE_FULL_LABEL_RECEIVER_WITH_EXPONENTIAL_CHARGED_SEARCH"&&report.kernel_source==="core/dcp_coherent_edge_sampling.py","receiver and kernel scope");
for(const k of ["novelty_claim","candidate_record_accepted","classical_witness_finder_needed_by_this_receiver","polynomial_time_weak_learner_implemented","quantum_speedup_proved","full_secret_decoder_implemented","no_go_for_other_receivers"])check(report[k]===false,"false claim gate: "+k);
check(report.local_derivation_review_pending===true,"not independently reviewed theorem");
const populationSchedule=[[1,5],[2,3],[1,16],[2,16],[1,64]];
check(report.population_certificates.length===populationSchedule.length,"complete scaling schedule");
for(let i=0;i<populationSchedule.length;i++){
  const c=report.population_certificates[i],[n,r]=populationSchedule[i],M=n*r-2,D=3n**BigInt(M),G=9n*D,A=D-1n;
  const P=1n<<BigInt((A-1n).toString(2).length),lambda=F(2n*A,G),second=add(sq(lambda),mul(lambda,sub(F(1n),F(2n,G)))),mass=sub(lambda,mul(F(1n,4n),second));
  check(c.dimension===n&&c.root_digits===r&&c.source_qutrits===M&&I(c.native_words)===D&&I(c.full_frequency_group)===G&&I(c.valid_offsets)===A,"native source and density");schedule(c.schedule,P);
  for(const [key,value] of [["useful_edge_probability",F(2n,G)],["mean_degree",lambda],["second_degree_moment",second],["bounded_degree_oriented_mass_lower",mass],["universal_mass_lower",F(5n,36n)],["kernel_lower",F(1n,4225n)],["universal_infinite_interference_lower",F(1n,30420n)],["raw_trit_advantage_after_charged_abort_lower",div(sub(F(1n,30420n),F(1n,65536n)),F(3n))]])check(eq(Q(c[key]),value),"exact population value: "+key);
  check(le(F(1n,5n),lambda)&&le(lambda,F(2n,9n))&&le(F(5n,36n),mass)&&P>=16n,"bounded-degree proof prerequisites");
  check(c.degree_cap_for_proof_only===8&&c.positive_advantage_certified===true,"analysis-only degree cap");
  for(const k of ["full_table_access_required","classical_pair_finder_required","degree_counting_required","bounded_degree_vertices_selected","unknown_source_reflection_required","polynomial_runtime_proved","new_quantum_speedup_proved","cyclic_DHSP_vector_source_acquisition_supplied","hardware_gate_export_implemented","large_source_execution"])check(c[k]===false,"population scope: "+k);
  check(c.uniform_public_index_reflection_only===true&&c.label_law==="ALL_IID_UNIFORM_NATIVE_FULL_FREQUENCY_ROWS"&&c.secret_scope==="EVERY_FIXED_SECRET_AVERAGED_OVER_LABELS_AND_SHARED_PUBLIC_TIME"&&c.query_model==="EXPLICIT_REVERSIBLE_FULL_PUBLIC_LABEL_ARITHMETIC","legal source/access model");
}
function digits(x,w){const a=[];for(let i=0;i<w;i++){a.push(x%3);x=Math.floor(x/3);}return a;}
const rank=a=>a.reduce((s,x,i)=>s+x*3**i,0), minus=d=>d.map(x=>mod(-x,3)), plus=(x,d)=>x.map((a,i)=>mod(a+d[i],3));
function orient(x,d){const e=Number(d.find(a=>a)!==1);return [e?plus(x,d):x,e?minus(d):d,e];}
check(report.native_unit_minor_controls.length===504,"every ordered pointed native triple");let pointed=0;
for(let base=0;base<9;base++)for(let first=0;first<9;first++)for(let second=0;second<9;second++)if(new Set([base,first,second]).size===3){
  const c=report.native_unit_minor_controls[pointed++],words=[base,first,second].map(x=>digits(x,2));
  for(const [k,w] of [["base",words[0]],["first",words[1]],["second",words[2]]])check(JSON.stringify(c[k])===JSON.stringify(w),"pointed complete schedule");
  const rows=words.slice(1).map(w=>[0,1].flatMap(i=>[1,2].map(d=>Number(w[i]===d)-Number(words[0][i]===d))));
  check(JSON.stringify(c.rows)===JSON.stringify(rows)&&c.columns.length===2,"original simplex difference rows");
  const [a,b]=c.columns;check(Number.isSafeInteger(a)&&Number.isSafeInteger(b)&&0<=a&&a<b&&b<4,"unit minor columns");
  const det=rows[0][a]*rows[1][b]-rows[0][b]*rows[1][a];check(Math.abs(det)===1&&det===c.integer_determinant,"composite-ring unit minor");
}
let censusFirst=0,censusSecond=0,censusSingletons=0;
for(let a=0;a<27;a++)for(let c=0;c<27;c++){const v=[0,a,c];for(let x=0;x<3;x++){let degree=0;for(let d=1;d<=2;d++)degree+=Number([9,18].includes(mod(v[(x+d)%3]-v[x],27)));censusFirst+=degree;censusSecond+=degree*degree;censusSingletons+=Number(v.filter(z=>z===v[x]).length===1);}}
const census=report.whole_source_degree_census;
check(census.dimension===1&&census.root_digits===3&&census.source_qutrits===1&&census.complete_native_label_pairs===729&&census.complete_label_word_assignments===2187&&eq(Q(census.mean_degree),F(BigInt(censusFirst),2187n))&&eq(Q(census.second_degree_moment),F(BigInt(censusSecond),2187n))&&census.constant_advantage_large_root_bound_applied_here===false&&census.full_root_homomorphism_label_pairs===3,"whole native label degree/character census, no filtering");
check(census.singleton_native_word_assignments===censusSingletons,"complete source-weighted singleton census");
check(report.source_class_trimming_bounds.length===populationSchedule.length,"all normalization-trimming scaling controls");
report.source_class_trimming_bounds.forEach((c,i)=>{const [n,r]=populationSchedule[i],D=3n**BigInt(n*r-2),G=9n*D,threshold=F(1n,BigInt((n*r)**2)),K=(D*threshold[0]+threshold[1]-1n)/threshold[1],excess=F(D-1n,G),mass=K<=1n?F(1n):div(excess,F(K-1n));check(c.dimension===n&&c.root_digits===r&&I(c.native_words)===D&&I(c.full_frequency_group)===G&&eq(Q(c.squared_singular_threshold),threshold)&&I(c.minimum_retained_class_size)===K,"exact native trimming threshold not supplied mass");for(const [k,v]of [["exact_mean_source_weighted_excess_class_size",excess],["mean_singleton_source_mass_lower",sub(F(1n),excess)],["mean_retained_source_mass_upper",mass],["raw_trit_advantage_upper_if_discarded_outputs_guessed_uniform",mul(F(2n,3n),mass)]])check(eq(Q(c[k]),v),"source-weighted trimming inequality: "+k);check(c.scope==="GLOBAL_PUBLIC_FOURIER_ERASURE_CLASSES_WITH_c_OVER_D_ABOVE_THRESHOLD"&&c.source_law==="ALL_IID_NATIVE_LABELS_AND_UNIFORM_ORIGINAL_WORD_WEIGHT","native weighted class scope");for(const k of ["large_classes_assumed_physically_filterable","conditioned_success_renormalization_granted","lower_bound_against_other_normalizations_or_quantum_receivers"])check(c[k]===false,"trimming not generic receiver no-go: "+k);});
check(report.short_Grover_template_bounds.length===populationSchedule.length,"all restricted time-cap controls");report.short_Grover_template_bounds.forEach((c,i)=>{const [n,r]=populationSchedule[i],D=3n**BigInt(n*r-2),A=D-1n,P=1n<<BigInt((A-1n).toString(2).length),lambda=F(2n*A,9n*D),T=BigInt((n*r)**2),raw=div(mul(lambda,F((2n*T+1n)**2n)),F(3n*P)),bound=le(raw,F(2n,3n))?raw:F(2n,3n);check(c.dimension===n&&c.root_digits===r&&I(c.maximum_iterations)===T&&I(c.padded_offset_domain)===P&&eq(Q(c.native_mean_degree),lambda)&&eq(Q(c.raw_trit_advantage_upper),bound),"exact raw template cap, no short-time constant signal");check(c.scope==="UNCHANGED_CLEAN_PUBLIC_INDEX_GROVER_EDGE_TEMPLATE_WITH_HARD_TIME_CAP"&&c.label_dependent_shared_time_within_cap_allowed===true&&c.failure_and_all_IID_source_labels_charged===true&&c.rules_out_general_quantum_measurements_or_modified_oracles===false,"not a general query/quantum lower bound");});
let kernels=0;
check(report.kernel_checks.length===3,"complete kernel schedule");
report.kernel_checks.forEach((c,i)=>{const P=[8,32,128][i],cap=Math.min(8,P/2);check(c.padded===P&&c.all_positive_degree_pairs===P*P&&c.cap===cap&&eq(Q(c.lower_bound),F(1n,BigInt((1+8*cap)**2))),"kernel schedule");let min=null,bounded=null;
  for(let a=1;a<=P;a++)for(let b=1;b<=P;b++){const v=kernel(a,b,P);check(v[0]>0n,"every exact positive kernel entry");if(!min||le(v,min))min=v;if(a<=cap&&b<=cap&&(!bounded||le(v,bounded)))bounded=v;kernels++;}
  check(eq(min,Q(c.minimum_exact_kernel))&&eq(bounded,Q(c.bounded_minimum_exact_kernel))&&le(Q(c.lower_bound),bounded),"complete kernel minima and lower bound");});
function matrixMultiply(A,B){return A.map(row=>B[0].map((_,j)=>row.reduce((s,a,k)=>s+a*B[k][j],0n)));}
function nativeChart(r){let V=[[1n,0n],[0n,1n]],B=[[-1n,-1n],[1n,-2n]];for(let i=0;i<2*r-1;i++)V=matrixMultiply(V,B);const det=V[0][0]*V[1][1]-V[0][1]*V[1][0],q=3n**BigInt(r),den=3n*det,un=q*(2n*V[1][1]+V[1][0]),vn=q*(-2n*V[0][1]-V[0][0]);check(un%den===0n&&vn%den===0n,"native integer frequency chart");return [Number(un/den),Number(vn/den)];}
function makeGraph(c){const n=c.dimension,r=c.root_digits,M=n*r-2,D=3**M,P=2**Math.ceil(Math.log2(D-1)),q=3**r,Q=q/3,[u,v]=nativeChart(r);check(D*P<=30000,"bounded complete replay");
  check(c.native_labels.length===M&&c.full_frequencies.length===M,"all native source rows");
  for(let i=0;i<M;i++){check(c.native_labels[i].length===n&&c.full_frequencies[i].length===2&&c.full_frequencies[i].every(row=>row.length===n),"native dimension");for(let j=0;j<n;j++){const [a,b]=c.native_labels[i][j];check(Number.isSafeInteger(a)&&Number.isSafeInteger(b)&&a>=0&&a<q&&b>=0&&b<q,"canonical original ring label");check(c.full_frequencies[i][0][j]===mod(u*a+v*b,q)&&c.full_frequencies[i][1][j]===mod((u+v)*a-u*b,q),"frequency chart, not arbitrary table oracle");}}
  const words=Array.from({length:D},(_,x)=>digits(x,M)),values=words.map(w=>Array.from({length:n},(_,j)=>mod(w.reduce((s,d,i)=>s+(d?c.full_frequencies[i][d-1][j]:0),0),q)));
  const delta=(x,y)=>{const a=values[x].map((f,j)=>mod(values[y][j]-f,q));return a.every((f,j)=>j===c.coordinate||f===0)&&[Q,2*Q].includes(a[c.coordinate])?a[c.coordinate]/Q:0;};
  const edges=[],degrees=Array(D).fill(0);for(let x=0;x<D;x++)for(let i=0;i<D-1;i++){const d=digits(i+1,M),y=rank(plus(words[x],d));if(delta(x,y)){edges.push([x,i,y,rank(minus(d))-1]);degrees[x]++;}}
  return {n,r,M,D,P,q,words,values,delta,edges,degrees};
}
const cmul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],phase=x=>[Math.cos(x),Math.sin(x)],norm=a=>a[0]*a[0]+a[1]*a[1];
function initial(g){return Array.from({length:g.D},()=>Array(g.P).fill(1/Math.sqrt(g.P)));}
function iterate(g,state){for(const [x,i]of g.edges)state[x][i]*=-1;for(const row of state){const mean=row.reduce((a,b)=>a+b,0)/g.P;for(let i=0;i<g.P;i++)row[i]=2*mean-row[i];}}
function score(g,row){const t=N(row.iterations,"bounded iteration"),secret=row.calibration_secret_only;check(secret.length===g.n&&secret.every(x=>Number.isSafeInteger(x)&&x>=0&&x<g.q),"all-secret calibration scope");const state=initial(g);for(let k=0;k<t;k++)iterate(g,state);let G=0,herald=0;const groups=new Map();
  for(const [x,i,y,j] of g.edges){G+=state[x][i]*state[y][j]/g.D;herald+=state[x][i]**2/g.D;const [w,d,e]=orient(g.words[x],digits(i+1,g.M)),rep=rank(w),ci=rank(d)-1,key=[rep,ci,row.retained_endpoint_specific_tag_countercontrol?i:"clean"].join(":");if(!groups.has(key))groups.set(key,{rep,ci,amplitudes:[[0,0],[0,0]]});const a=phase(2*Math.PI*mod(g.values[x].reduce((s,f,j)=>s+f*secret[j],0),g.q)/g.q),b=groups.get(key).amplitudes[e],scale=state[x][i]/Math.sqrt(g.D);b[0]+=a[0]*scale;b[1]+=a[1]*scale;}
  let correct=(1-herald)/3,total=1-herald;for(const {rep,ci,amplitudes} of groups.values()){const y=rank(plus(g.words[rep],digits(ci+1,g.M))),target=g.delta(rep,y)*mod(secret[g.coordinate],3)%3;for(let k=0;k<3;k++){const z=cmul(amplitudes[1],phase(-2*Math.PI*k/3)),prob=norm([amplitudes[0][0]+z[0],amplitudes[0][1]+z[1]])/3;total+=prob;if(k===target)correct+=prob;}}
  close(row.heralded_probability,herald,"actual herald probability");close(row.oriented_interference,G,"unequal-degree interference");close(row.raw_correct_probability,correct,"actual raw trine Born score");close(row.predicted_raw_correct_probability,row.retained_endpoint_specific_tag_countercontrol?1/3:(1+G)/3,"unconditioned prediction, dirty tags included");close(total,1,"all trine outcomes and failures normalized");
  check(row.conditional_normalization_used===false&&row.unknown_secret_used_to_select_edges===false&&row.source_dense_cells===g.D*g.P&&row.dense_calibration_not_scalable_storage===true,"source/cost scope");for(const k of ["Born_score_residual","probability_normalization_residual","Grover_row_norm_residual","marked_amplitude_residual"])check(Number.isFinite(row[k])&&row[k]>=0&&row[k]<3e-11,"generator residual plus independent replay");return Math.abs(correct-row.predicted_raw_correct_probability);
}
function averaged(g,c){let infinite=F(0n);for(const [x,,y]of g.edges)infinite=add(infinite,div(kernel(g.degrees[x],g.degrees[y],g.P),F(BigInt(g.D))));check(eq(infinite,Q(c.infinite_interference_exact))&&infinite[0]>=0n,"exact native shared interference");check(JSON.stringify(c.degrees)===JSON.stringify(g.degrees)&&c.oriented_edges===g.edges.length,"all degrees not estimated");const s=params(g.P),p=Number(s.p[0])/Number(s.p[1]),rho=1-p,T=16*2**s.h,state=initial(g);let prob=p,finite=0;for(let t=0;t<T;t++){let G=0;for(const [x,i,y,j]of g.edges)G+=state[x][i]*state[y][j]/g.D;finite+=prob*G;iterate(g,state);prob*=rho;}
  const tail=rho**T;close(c.truncated_interference,finite,"actual clipped shared evolution");close(c.truncated_raw_trit_advantage,finite/3,"raw geometric advantage");close(c.actual_abort_probability,tail,"charged abort");check(eq(Q(c.certified_tail_upper),F(1n,65536n))&&c.per_label_constant_advantage_claimed===false&&c.shared_time_across_source===true&&c.no_edge_labels_retained_in_source_population_estimate===true,"clipping/population scope");close(c.tail_error,Math.abs(finite-Number(infinite[0])/Number(infinite[1])),"tail residual");check(c.tail_error<=tail+3e-11&&tail<=1/65536,"tail loss bound");}
function fiberAccess(g,c){
  check(c.status==="EXACT_NATIVE_TRIPARTITE_GEOMETRY_NOT_AN_EFFICIENT_COMPILER","fiber representation not efficient compiler");
  const fibers=new Map(),Q0=g.q/3;for(let x=0;x<g.D;x++){const value=g.values[x],syndrome=value.map((f,j)=>j===g.coordinate?f%Q0:f),key=JSON.stringify(syndrome);if(!fibers.has(key))fibers.set(key,[[],[],[]]);fibers.get(key)[Math.floor(value[g.coordinate]/Q0)].push(x);}
  check(c.complete_nuisance_fibers.length===fibers.size&&c.words_enumerated===g.D&&c.native_uniform_source_words_partitioned===g.D,"complete native class partition");
  const seen=new Set();let collisions=0,edges=0,optimum=0;
  for(const b of c.complete_nuisance_fibers){const key=JSON.stringify(b.nuisance_syndrome),groups=fibers.get(key);check(groups&&!seen.has(key),"unique original nuisance fiber");seen.add(key);
    const counts=groups.map(a=>a.length),C=counts.reduce((a,b)=>a+b,0),[a,d,e]=counts,degrees=counts.map(v=>C-v),oriented=C*C-counts.reduce((s,v)=>s+v*v,0),poly=["1","0",String(-(a*d+a*e+d*e)),String(-2*a*d*e)],rank=a*d*e?3:counts.filter(v=>v>0).length===2?2:0;
    for(const [field,value]of [["class_counts",counts],["word_ranks_by_high_trit",groups],["class_degrees",degrees],["compressed_adjacency_characteristic",poly]])check(JSON.stringify(b[field])===JSON.stringify(value),"exact native class/degree/spectral data: "+field);
    check(b.compressed_adjacency_rank===rank&&b.oriented_edges===oriented&&b.exact_class_incidence_factorization_checked===true&&b.uniform_class_erasure_singular_values_squared.length===3,"tripartite rank and exact factorization");
    for(let h=0;h<3;h++){check(eq(Q(b.uniform_class_erasure_singular_values_squared[h]),F(BigInt(counts[h]),BigInt(g.D))),"actual native erasure singular value");for(const x of groups[h])check(g.degrees[x]===degrees[h],"degree equals class complement count");}
    const contribution=counts.reduce((s,v)=>s+Math.sqrt(v),0)**2/(3*g.D);close(b.ideal_uniform_class_trine_raw_contribution,contribution,"ideal reference not granted access");optimum+=contribution;collisions+=counts.reduce((s,v)=>s+v*v,0);edges+=oriented;
  }
  check(edges===g.edges.length&&c.exact_full_frequency_collision_count===collisions&&eq(Q(c.raw_public_Fourier_erasure_success),F(BigInt(collisions),BigInt(g.D*g.D))),"exact source erasure success, no free renormalization");
  check(eq(Q(c.mean_erasure_success_over_all_IID_labels),add(F(1n,BigInt(g.D)),F(BigInt(g.D-1),BigInt(g.D)*BigInt(g.q)**BigInt(g.n))))&&eq(Q(c.singleton_class_singular_value_squared),F(1n,BigInt(g.D))),"exponential source/access normalization");close(c.ideal_class_compressed_raw_trit_success,optimum,"class compression agrees with information-only optimum");
  check(c.compressed_adjacency_reconstruction_residual>=0&&c.compressed_adjacency_reconstruction_residual<3e-11,"finite compressed adjacency residual");
  for(const k of ["class_counts_or_uniform_basis_given_to_receiver","erasure_success_renormalization_free","coherent_uniform_class_inverse_preparation_implemented","generic_quantum_lower_bound_proved","quantum_speedup_proved"])check(c[k]===false,"no hidden class compiler or generic lower bound: "+k);
}
function translationAccess(c){
  const n=N(c.dimension,"native dimension"),r=N(c.root_digits,"native root"),M=n*r-2,q=3n**BigInt(r),t=c.translation_control,[u,v]=nativeChart(r),modQ=x=>(x%q+q)%q;
  check(c.native_labels.length===M&&c.full_frequencies.length===M&&t.native_rows.length===M&&t.status==="FULL_ROOT_NATIVE_TRANSLATION_CHARACTER_SCOPE_CONTROL","complete full-root translation schema");
  const equal=(A,B)=>JSON.stringify(A.map(row=>row.map(String)))===JSON.stringify(B.map(row=>row.map(String)));let first=null;
  for(let i=0;i<M;i++){
    check(c.native_labels[i].length===n&&c.full_frequencies[i].length===2&&c.full_frequencies[i].every(row=>row.length===n),"complete scalable native frequency rows");
    const a=c.full_frequencies[i][0].map(I),b=c.full_frequencies[i][1].map(I);
    for(let j=0;j<n;j++){const label=c.native_labels[i][j].map(I);check(label.length===2&&label.every(x=>x<q)&&a[j]<q&&b[j]<q,"canonical large native labels");check(a[j]===modQ(BigInt(u)*label[0]+BigInt(v)*label[1])&&b[j]===modQ(BigInt(u+v)*label[0]-BigInt(u)*label[1]),"exact full-root native chart not modulo-three substitute");}
    const rows=[a,b.map((x,j)=>modQ(x-a[j])),b.map(x=>modQ(-x))],linear=equal([rows[0]],[rows[1]])&&equal([rows[0]],[rows[2]]),record=t.native_rows[i];
    check(record.source_wire===i&&record.three_cycle_increment_rows.length===3&&equal(record.three_cycle_increment_rows.map(row=>row.map(I)),rows)&&record.full_modulus_cycle_is_linear===linear,"ALL exact native increment rows including wraparound");
    if(!linear&&first===null){const coordinate=Array.from({length:n},(_,j)=>j).find(j=>new Set(rows.map(row=>String(row[j]))).size>1);first={i,coordinate,rows};}
  }
  check(t.native_F_is_group_homomorphism===(first===null)&&t.all_secret_phase_states_are_F3_word_characters===(first===null)&&t.necessary_and_sufficient_per_wire==="c=2*a modq AND 3*a=0 modq","character theorem scope");
  if(first){const f=t.first_exact_cycle_disagreement;check(f&&f.source_wire===first.i&&f.frequency_coordinate===first.coordinate&&f.actual_full_frequency_increment_rows.length===3&&equal(f.actual_full_frequency_increment_rows.map(row=>row.map(I)),first.rows),"first genuine full-root disagreement");check(JSON.stringify(f.base_words)===JSON.stringify([0,1,2].map(d=>Array.from({length:M},(_,i)=>i===first.i?d:0)))&&JSON.stringify(f.same_native_unit_offset)===JSON.stringify(Array.from({length:M},(_,i)=>Number(i===first.i))),"actual canonical native witness words/unit offset");}else check(t.first_exact_cycle_disagreement===null,"no invented character obstruction");
  check(t.IID_probability_of_exact_homomorphism.base===3&&t.IID_probability_of_exact_homomorphism.negative_exponent===n*M*(2*r-1)&&t.full_root_not_modulo_three_checked===true&&t.dense_native_words_enumerated===0,"exact IID character probability and scalable arithmetic");
  for(const k of ["rules_out_general_structure_aware_Fourier_transforms","native_informative_graph_invariance_inferred_from_nonhomomorphism","quantum_algorithm_no_go_proved"])check(t[k]===false,"not a generic transform no-go: "+k);
}
function erasureAccess(g,e,f){
  const secret=e.calibration_secret_only;check(secret.length===g.n&&secret.every(s=>Number.isSafeInteger(s)&&s>=0&&s<g.q),"erasure all-secret calibration scope");
  const output=new Map();for(const value of g.values){const key=JSON.stringify(value),angle=2*Math.PI*mod(value.reduce((a,b,j)=>a+b*secret[j],0),g.q)/g.q,a=phase(angle);if(!output.has(key))output.set(key,[0,0]);const v=output.get(key);v[0]+=a[0]/g.D;v[1]+=a[1]/g.D;}
  const actual=[...output.values()].reduce((s,v)=>s+norm(v),0),exact=Q(f.raw_public_Fourier_erasure_success);
  check(eq(Q(e.predicted_raw_erasure_success_exact),exact),"erasure exact success tied to actual source collision counts");close(e.actual_raw_erasure_success,actual,"independent physical uniform-projection Kraus output");close(e.charged_rejection_probability,1-actual,"all original-source rejection charged");
  check(e.full_label_output_amplitude_residual>=0&&e.full_label_output_amplitude_residual<3e-11&&e.whole_unitary_norm_residual>=0&&e.whole_unitary_norm_residual<3e-11&&e.dense_diagnostic_cells===g.D*g.q**g.n&&e.source_registers_measured_only_after_F_evaluation===true,"full native Fourier replay and cost");
  for(const k of ["output_success_renormalized","unknown_source_inverse_used","uniform_class_inverse_preparation_implemented"])check(e[k]===false,"no hidden coherent erasure: "+k);
}
const cases=[[1,5,98301,0],[1,5,98302,0],[1,5,98303,0],[2,3,98304,0],[2,3,98304,1]];check(report.prespecified_native_physical_cases.length===cases.length,"all prespecified sources retained");let physical=0,zeroEdgeCases=0,maxBornResidual=0;
report.prespecified_native_physical_cases.forEach((c,i)=>{check(JSON.stringify([c.dimension,c.root_digits,c.seed,c.coordinate])===JSON.stringify(cases[i])&&c.all_prespecified_labels_retained===true,"no favorable source selection");const g=makeGraph(c);g.coordinate=c.coordinate;if(!g.edges.length)zeroEdgeCases++;check(c.physical_controls.length===15,"complete time/secret schedule");let index=0;for(const t of [0,1,2,5,11])for(const secret of [Array(g.n).fill(0),Array.from({length:g.n},(_,j)=>3*(j+1)%g.q),Array.from({length:g.n},(_,j)=>(g.q-1-j)%g.q)]){const row=c.physical_controls[index++];check(row.iterations===t&&JSON.stringify(row.calibration_secret_only)===JSON.stringify(secret)&&row.retained_endpoint_specific_tag_countercontrol===false,"all secret types/time controls");maxBornResidual=Math.max(maxBornResidual,score(g,row));physical++;}check(c.dirty_scratch_control.retained_endpoint_specific_tag_countercontrol===true,"dirty scratch falsifier retained");score(g,c.dirty_scratch_control);averaged(g,c.geometric_control);fiberAccess(g,c.fiber_structure_control);});
const cancellation=report.fixed_time_cancellation_control;check(cancellation.scope==="SELECTED_NATIVE_BOUNDARY_CALIBRATION_NOT_POPULATION_PERFORMANCE","small-root cancellation scope");const special=makeGraph({dimension:1,root_digits:3,coordinate:0,native_labels:cancellation.native_labels,full_frequencies:cancellation.full_frequencies});special.coordinate=0;score(special,cancellation.physical_control);close(cancellation.physical_control.oriented_interference,-2/3,"actual native negative fixed-time signal");close(cancellation.physical_control.raw_correct_probability,1/9,"fixed-time below chance");averaged(special,cancellation.geometric_control);fiberAccess(special,cancellation.fiber_structure_control);
report.prespecified_native_physical_cases.forEach(translationAccess);
report.prespecified_native_physical_cases.forEach(c=>{const g=makeGraph(c);g.coordinate=c.coordinate;erasureAccess(g,c.erasure_physical_control,c.fiber_structure_control);});
erasureAccess(special,cancellation.erasure_physical_control,cancellation.fiber_structure_control);
const translations=[[1,16,98401],[2,16,98402],[1,64,98403]];check(report.scalable_native_translation_controls.length===3,"all scalable arithmetic cases");report.scalable_native_translation_controls.forEach((c,i)=>{check(JSON.stringify([c.dimension,c.root_digits,c.seed])===JSON.stringify(translations[i])&&c.dense_native_words_enumerated===0,"scalable native controls not dense execution");translationAccess(c);});
console.log(JSON.stringify({status:"independent_native_coherent_receiver_controls_passed",populationCertificates:5,pointedUnitMinors:pointed,kernelEntries:kernels,wholeSourceLabelPairs:729,physicalControls:physical,zeroEdgeCases,maxBornResidual,negativeFixedTimeControl:true,translationControls:8,erasureControls:6,exponentialTime:true,quantumSpeedupProved:false}));
