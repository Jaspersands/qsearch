"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto"),cp=require("child_process");
const R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../classical_baselines/ternary_character_joint_plane.json"),"utf8"));
const parentPath=path.join(__dirname,"../classical_baselines/ternary_character_cyclic_gap_certificate.json"),P=JSON.parse(fs.readFileSync(parentPath,"utf8"));
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex"),check=(x,m)=>{if(!x)throw Error(m);},key=JSON.stringify;
const same=(a,b,m)=>check(key(a)===key(b),m),mod=(a,q)=>(a%q+q)%q;
check(R.status==="EXACT_FINITE_JOINT_PLANE_OBSTRUCTION_REVIEW_PENDING"&&R.source_report_sha256===hash(parentPath)&&R.derivation_sha256===hash(path.join(__dirname,"../TERNARY_CHARACTER_JOINT_PLANE.md")),"pinned exact joint audit ancestry and derivation");
check(R.new_optimizer_or_source_experiment===false&&R.population_or_asymptotic_failure_claim===false&&R.accepted_speedup_candidate===false,"joint finite scope");
same(R.controls.map(c=>c.seed),[93017,93018],"complete fixed native cohorts");
function lex(a,b){for(let k=0;k<a.length;k++)if(a[k]!==b[k])return a[k]-b[k];return 0;}
function compile(nodes,q){
  const D=new Map();nodes.forEach((a,i)=>nodes.forEach((b,j)=>{const d=a.map((x,k)=>mod(x-b[k],q)),id=key(d);if(!D.has(id))D.set(id,{d,entry:i*nodes.length+j});}));
  const zero=Array(nodes[0].length).fill(0),lineMap=new Map();
  for(const{d}of D.values())if(d.some(x=>x!==0)&&d.every(x=>3*x%q===0)){
    const opposite=d.map(x=>mod(-x,q)),first=lex(d,opposite)<0?d:opposite;lineMap.set(key(first),first);
  }
  const lines=Array.from(lineMap.values()).sort(lex),seen=new Set(),planes=[];
  for(let i=0;i<lines.length;i++)for(let j=i+1;j<lines.length;j++){
    const a=lines[i],b=lines[j],vectors=[];for(let x=0;x<3;x++)for(let y=0;y<3;y++)vectors.push(a.map((v,k)=>mod(x*v+y*b[k],q)));
    vectors.sort(lex);const span=key(vectors);if(new Set(vectors.map(key)).size!==9||seen.has(span))continue;seen.add(span);
    if(vectors.every(d=>D.has(key(d)))){
      const first=vectors.find(d=>key(d)!==key(zero)),line=new Set([key(zero),key(first),key(first.map(x=>mod(2*x,q)))]),second=vectors.find(d=>!line.has(key(d))),entries=[];
      for(let x=0;x<3;x++)for(let y=0;y<3;y++)entries.push(D.get(key(first.map((v,k)=>mod(x*v+y*second[k],q)))).entry);
      planes.push({generators:[first,second],group_order:9,power_entries:entries});
    }
  }
  planes.sort((a,b)=>lex(a.generators[0],b.generators[0])||lex(a.generators[1],b.generators[1]));
  return{status:"ALL_REPRESENTED_COMPLETE_ORDER_THREE_PLANES",planes,represented_order_three_lines:lines.length,line_pairs_checked:lines.length*(lines.length-1)/2,distinct_spanned_planes_checked:seen.size,complete_planes:planes.length,incomplete_spanned_planes:seen.size-planes.length,joint_laws_checked:9*planes.length,unrepresented_moments_added:false,full_secret_enumeration_used:false,compilation_reads_truth_outcomes_or_witness:false};
}
function gcd(a,b){a=a<0n?-a:a;while(b)[a,b]=[b,a%b];return a;}
function fraction(a,b){const g=gcd(a,b);return b/g===1n?String(a/g):a/g+"/"+b/g;}
const bound=(a,r,k,lower)=>a*BigInt(r[k+(((a>=0n)===lower)?"_lower":"_upper")]);
let laws=0,negativeCount=0,planes=0;
for(const c of R.controls){
  const parent=P.certificates.find(p=>p.seed===c.seed);check(parent,"exact parent linkage");const D=compile(parent.nodes,parent.modulus),w=parent.witness,K=parent.nodes.length,S=BigInt(w.moment_scale),roots=[0,1,2].map(k=>parent.root_intervals[k*parent.modulus/3]);
  same(c.description,D,"independent full order-three plane compilation");
  check(c.exact_reality_and_normalization===true&&c.all_separate_cyclic_laws_pass_exactly===true&&parent.cyclic_feasibility.all_complete_cyclic_laws_exactly_nonnegative===true&&c.all_joint_laws_or_global_realizability_certified===false,"joint versus line scope");
  const negatives=[];let least=null,leastLower=null;const den=9n*S*2n**48n;
  D.planes.forEach((p,pi)=>{
    const v=p.power_entries.map(e=>[Math.floor(e/K),e%K]);let[i,j]=v[0];check(w.matrix_real_integer[i][j]===w.moment_scale&&w.matrix_imag_integer[i][j]===0,"exact joint normalization");
    for(let x=0;x<3;x++)for(let y=0;y<3;y++){const[i,j]=v[3*x+y],[a,b]=v[3*mod(-x,3)+mod(-y,3)];check(w.matrix_real_integer[i][j]===w.matrix_real_integer[a][b]&&w.matrix_imag_integer[i][j]===-w.matrix_imag_integer[a][b],"exact joint reality");}
    for(let u=0;u<3;u++)for(let vSector=0;vSector<3;vSector++){
      let upper=0n,lower=0n;for(let x=0;x<3;x++)for(let y=0;y<3;y++){
        const[i,j]=v[3*x+y],r=roots[(x*u+y*vSector)%3],a=BigInt(w.matrix_real_integer[i][j]),b=BigInt(w.matrix_imag_integer[i][j]);
        upper+=bound(a,r,"cos",false)+bound(b,r,"sin",false);lower+=bound(a,r,"cos",true)+bound(b,r,"sin",true);
      }
      least=least===null||upper<least?upper:least;leastLower=leastLower===null||lower<leastLower?lower:leastLower;
      if(upper<0n)negatives.push({plane_index:pi,sectors:[u,vSector],generators:p.generators,joint_probability_upper_numerator:String(upper),joint_probability_upper_denominator:String(den)});
    }
  });
  same(c.negative_joint_laws,negatives,"ALL exact negative joint laws and rational bounds");
  check(c.status==="EXACT_JOINT_PLANE_VIOLATIONS"&&c.negative_joint_laws_certified===negatives.length&&negatives.length>0,"exact finite joint obstruction");
  check(c.minimum_joint_probability_upper_exact===fraction(least,den)&&c.minimum_joint_probability_lower_exact===fraction(leastLower,den),"exact extreme bounds");laws+=D.joint_laws_checked;planes+=D.complete_planes;negativeCount+=negatives.length;
}
const native=JSON.parse(fs.readFileSync(path.join(__dirname,"../classical_baselines/ternary_character_sdp_decoder.json"),"utf8"));
same(R.all_joint_cuts_survivors.map(c=>c.seed),[93017,93018],"both exact all-joint-cut survivor cohorts");
let mixedLaws=0,mixedEntries=0;
for(const c of R.all_joint_cuts_survivors){
  const p=P.certificates.find(x=>x.seed===c.seed),original=native.native_controls.find(x=>x.seed===c.seed),w=c.witness,old=p.witness,K=p.nodes.length;
  check(c.status==="EXACT_ALL_JOINT_PLANE_CUTS_CHARACTER_GAP"&&c.all_complete_joint_planes_exactly_nonnegative===true&&c.population_or_asymptotic_failure_claim===false,"all-cut finite negative result");
  check(w.status==="EXACT_CONVEX_PARENT_IDENTITY_MOMENT_POINT"&&w.PSD_certificate_kind==="EXACT_CONVEXITY_FROM_INDEPENDENTLY_CERTIFIED_PARENT"&&w.PSD_certified===true&&w.parent_seed===p.seed&&w.new_numerical_factor_or_solver_used===false,"exact PSD from verified convex parent");
  check(w.identity_weight_numerator===1&&w.identity_weight_denominator===4&&w.moment_scale===4*old.moment_scale,"predeclared one-quarter identity mixture");
  check(w.matrix_real_integer.length===K&&w.matrix_imag_integer.length===K,"complete mixed point");
  for(let i=0;i<K;i++){check(w.matrix_real_integer[i].length===K&&w.matrix_imag_integer[i].length===K,"complete mixed row");for(let j=0;j<K;j++){
    check(Number.isSafeInteger(w.matrix_real_integer[i][j])&&Number.isSafeInteger(w.matrix_imag_integer[i][j]),"exact mixed integers");
    check(w.matrix_real_integer[i][j]===3*old.matrix_real_integer[i][j]+(i===j?old.moment_scale:0)&&w.matrix_imag_integer[i][j]===3*old.matrix_imag_integer[i][j],"EVERY exact convex mixture moment");mixedEntries++;
  }}
  const S=BigInt(w.moment_scale),cyclic=c.cyclic_feasibility,joint=c.joint_feasibility,D=compile(p.nodes,p.modulus);
  same(cyclic.description,p.cyclic_feasibility.description,"same complete cyclic cuts");same(joint.description,D,"ALL joint cuts, not just three violated sectors");
  let minimum=null,location=null,count=0;
  cyclic.description.groups.forEach((g,gi)=>{for(let t=0;t<g.order;t++){
    let lower=0n;g.power_entries.forEach((e,k)=>{const i=Math.floor(e/K),j=e%K,r=p.root_intervals[(k*t%g.order)*p.modulus/g.order];lower+=bound(BigInt(w.matrix_real_integer[i][j]),r,"cos",true)+bound(BigInt(w.matrix_imag_integer[i][j]),r,"sin",true);});
    const den=S*2n**48n*BigInt(g.order);check(lower>=0n,"mixed point satisfies EVERY cyclic law");if(minimum===null||lower*minimum[1]<minimum[0]*den){minimum=[lower,den];location={group_index:gi,sector:t,order:g.order};}count++;
  }});
  check(cyclic.status==="ALL_COMPLETE_CYCLIC_LAWS_EXACTLY_FEASIBLE"&&cyclic.all_complete_cyclic_laws_exactly_nonnegative===true&&cyclic.exact_reality_and_normalization_from_conjugate_powers===true&&cyclic.global_cross_cycle_character_realizability_certified===false,"mixed cyclic scope");
  check(cyclic.minimum_complete_cyclic_probability_lower_exact===fraction(...minimum)&&cyclic.complete_cyclic_probabilities_exact_lower_checked===count,"all mixed cyclic exact bounds");same(cyclic.minimum_lower_location,location,"mixed cyclic minimum location");mixedLaws+=count;
  let leastLower=null,leastUpper=null;count=0;const den=9n*S*2n**48n;
  D.planes.forEach(plane=>{for(let u=0;u<3;u++)for(let v=0;v<3;v++){
    let lower=0n,upper=0n;for(let x=0;x<3;x++)for(let y=0;y<3;y++){
      const e=plane.power_entries[3*x+y],i=Math.floor(e/K),j=e%K,r=p.root_intervals[((x*u+y*v)%3)*p.modulus/3],a=BigInt(w.matrix_real_integer[i][j]),b=BigInt(w.matrix_imag_integer[i][j]);
      lower+=bound(a,r,"cos",true)+bound(b,r,"sin",true);upper+=bound(a,r,"cos",false)+bound(b,r,"sin",false);
    }
    check(lower>=0n,"mixed point satisfies EVERY nine-sector joint law");leastLower=leastLower===null||lower<leastLower?lower:leastLower;leastUpper=leastUpper===null||upper<leastUpper?upper:leastUpper;count++;
  }});
  check(joint.status==="NO_EXACT_JOINT_VIOLATION"&&joint.negative_joint_laws_certified===0&&joint.negative_joint_laws.length===0&&joint.exact_reality_and_normalization===true&&joint.all_separate_cyclic_laws_pass_exactly===true&&joint.all_joint_laws_or_global_realizability_certified===false,"mixed joint audit not global realization");
  check(joint.minimum_joint_probability_lower_exact===fraction(leastLower,den)&&joint.minimum_joint_probability_upper_exact===fraction(leastUpper,den)&&count===D.joint_laws_checked,"all joint exact probability bounds");mixedLaws+=count;
  let objective=0n;original.training_records.forEach((r,k)=>{const[a,b]=p.native_nodes[k];for(const[i,j,e]of[[a,0,r.outcome[0]],[b,0,r.outcome[1]],[a,b,mod(r.outcome[0]-r.outcome[1],p.modulus)]]){
    const x=BigInt(w.matrix_real_integer[i][j]),y=BigInt(w.matrix_imag_integer[i][j]),root=p.root_intervals[e];objective+=bound(x,root,"cos",true)+bound(y,root,"sin",true);
  }});
  const upper=BigInt(p.character_census.global_character_score_upper_numerator)*S,gap=objective-upper;
  check(gap>0n&&c.SDP_feasible_score_lower_numerator===String(objective)&&c.all_character_score_upper_same_scale_numerator===String(upper)&&c.strict_gap_lower_numerator===String(gap)&&c.score_common_denominator===String(S*2n**48n),"exact score gap AFTER every joint plane cut");
  check(c.parent_census_reused_only_under_independently_verified_unchanged_records===true&&c.all_secrets_enumerated_to_construct_mixed_point===false,"parent census bound verified but not used in construction");
}
const parent=JSON.parse(cp.execFileSync(process.execPath,[path.join(__dirname,"ternary_character_cyclic_gap_certificate_crosscheck.js"),parentPath],{encoding:"utf8"}));
check(parent.status==="PASS","independent exact PSD/cyclic/gap parent replay");
console.log(JSON.stringify({status:"PASS",complete_order_three_planes:planes,exact_joint_laws_checked:laws,exact_negative_joint_laws:negativeCount,
  exact_all_joint_cut_gaps:2,exact_mixed_probability_laws_checked:mixedLaws,exact_mixed_moment_entries:mixedEntries,global_character_or_population_inference_certified:false}));
