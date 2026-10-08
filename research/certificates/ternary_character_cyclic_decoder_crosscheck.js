"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto"),cp=require("child_process");
const sourcePath=path.join(__dirname,"../classical_baselines/ternary_character_sdp_decoder.json"),gapPath=path.join(__dirname,"../classical_baselines/ternary_character_sdp_gap_certificate.json");
const R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../classical_baselines/ternary_character_cyclic_decoder.json"),"utf8"));
const source=JSON.parse(fs.readFileSync(sourcePath,"utf8")),gaps=JSON.parse(fs.readFileSync(gapPath,"utf8"));
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex"),check=(x,m)=>{if(!x)throw Error(m);},key=JSON.stringify;
const same=(a,b,m)=>check(key(a)===key(b),m),near=(a,b,m,t=1e-7)=>check(Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=t,m);
check(R.source_report_sha256===hash(sourcePath)&&R.gap_report_sha256===hash(gapPath)&&R.derivation_sha256===hash(path.join(__dirname,"../TERNARY_CHARACTER_CYCLIC_DECODER.md")),"pinned source/gap/derivation");
check(R.global_realizability_or_population_recovery_proved===false&&R.accepted_candidate_or_speedup===false,"unsupported repair claims");
const mod=(a,q)=>(a%q+q)%q,dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
const order=(d,q)=>q/d.reduce((s,x)=>gcd(s,x),q);
function lex(a,b){for(let i=0;i<a.length;i++)if(a[i]!==b[i])return a[i]-b[i];return 0;}
function differences(nodes,q){const out=new Map();nodes.forEach((a,i)=>nodes.forEach((b,j)=>{const d=a.map((x,k)=>mod(x-b[k],q)),keyD=key(d);if(!out.has(keyD))out.set(keyD,{d,entry:i*nodes.length+j});}));return out;}
function description(nodes,q){
  const diff=differences(nodes,q),visited=new Set(),groups=[];let count=0;
  for(const{d}of diff.values()){
    const m=order(d,q);if(m===1)continue;const units=[];for(let k=1;k<m;k++)if(gcd(k,m)===1)units.push(d.map(x=>mod(k*x,q)));
    units.sort(lex);const v=units[0],id=key(v);if(visited.has(id))continue;visited.add(id);
    const powers=Array.from({length:m},(_,k)=>key(v.map(x=>mod(k*x,q))));
    if(powers.every(p=>diff.has(p))){groups.push({order:m,generator:v,power_entries:powers.map(p=>diff.get(p).entry)});count+=m;}
  }
  groups.sort((a,b)=>a.order-b.order||lex(a.generator,b.generator));
  return{status:"ALL_REPRESENTED_COMPLETE_CYCLIC_GROUPS",groups,constraints:count,distinct_represented_differences:diff.size,all_full_group_cyclic_subgroups_enumerated:false,incomplete_subgroups_silently_completed:false};
}
function rootBounds(m){const c=gaps.certificates.find(c=>c.modulus%m===0);check(c,"independently certified compatible root table");return Array.from({length:m},(_,k)=>c.root_intervals[k*c.modulus/m]);}
const productBound=(a,r,k,lower)=>a*BigInt(r[k+(((a>=0n)===lower)?"_lower":"_upper")]);
function bigGcd(a,b){a=a<0n?-a:a;while(b)[a,b]=[b,a%b];return a;}
function fraction(a,b){const g=bigGcd(a,b);return b/g===1n?String(a/g):a/g+"/"+b/g;}
let exactNegative=0,polygonChecks=0,cyclicChecks=0,entries=0;
for(const a of R.exact_old_witness_audits){
  const c=gaps.certificates.find(c=>c.seed===a.seed);check(c,"old exact point linkage");const D=description(c.nodes,c.modulus);
  same(a.description,D,"independent complete-cycle compilation and actual orders");const K=c.nodes.length,w=c.witness,S=BigInt(w.moment_scale),negatives=[];
  let least=null;
  D.groups.forEach((g,gi)=>{const roots=rootBounds(g.order);for(let t=0;t<g.order;t++){
    let upper=0n;g.power_entries.forEach((entry,k)=>{const i=Math.floor(entry/K),j=entry%K,r=roots[k*t%g.order];upper+=productBound(BigInt(w.matrix_real_integer[i][j]),r,"cos",false)+productBound(BigInt(w.matrix_imag_integer[i][j]),r,"sin",false);});
    const den=S*2n**48n*BigInt(g.order);if(least===null||upper*least[1]<least[0]*den)least=[upper,den];
    if(upper<0n)negatives.push({group_index:gi,sector:t,order:g.order,generator:g.generator,probability_upper_numerator:String(upper),probability_upper_denominator:String(den)});
  }});
  same(a.exact_negative_cyclic_probabilities,negatives,"all exact negative cyclic laws");check(a.negative_laws_certified===negatives.length&&a.negative_cyclic_groups_certified===new Set(negatives.map(x=>x.group_index)).size&&a.least_probability_upper_exact===fraction(...least),"exact cyclic probability upper bounds");
  let minimum=null,checks=0;for(const{d,entry}of differences(c.nodes,c.modulus).values()){
    const m=order(d,c.modulus);if(m===1)continue;const roots=rootBounds(m),i=Math.floor(entry/K),j=entry%K,x=BigInt(w.matrix_real_integer[i][j]),y=-BigInt(w.matrix_imag_integer[i][j]);
    for(let t=0;t<m;t++){const h=mod((m-1)/2-t,m),margin=-S*BigInt(roots[(m-1)/2].cos_upper)+productBound(x,roots[h],"cos",true)+productBound(y,roots[h],"sin",true);minimum=minimum===null||margin<minimum?margin:minimum;checks++;}
  }
  check(minimum>=0n&&a.first_moment_polygons_pass_exactly===true&&a.minimum_polygon_margin_integer===String(minimum)&&a.first_moment_polygon_checks===checks&&a.polygon_margin_denominator===String(S*2n**48n),"EVERY actual-order root polygon passes exactly");
  check(a.full_secret_enumeration_used_to_find_cuts===false&&a.cyclic_positivity_proves_global_realizability===false,"cyclic repair is not global character inference");exactNegative+=negatives.length;polygonChecks+=checks;
}
function score(records,s){const q=records[0].modulus;return records.reduce((v,r)=>{const a=mod(r.outcome[0]-dot(r.first,s),q),b=mod(r.outcome[1]-dot(r.second,s),q);return v+Math.cos(2*Math.PI*a/q)+Math.cos(2*Math.PI*b/q)+Math.cos(2*Math.PI*mod(a-b,q)/q);},0)/records.length;}
function sourceChart(level){
  let V=[[1n,0n],[0n,1n]],pi=[[-1n,-1n],[1n,-2n]];for(let j=0;j<level-1;j++)V=V.map(r=>pi[0].map((_,i)=>r.reduce((s,a,k)=>s+a*pi[k][i],0n)));
  const q=3n**BigInt(Math.ceil(level/2)),den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]),a=q*(2n*V[1][1]+V[1][0]),b=q*(-2n*V[0][1]-V[0][0]);
  check(a%den===0n&&b%den===0n,"new native source chart");const u=a/den,v=b/den;return z=>{const[x,y]=z.map(BigInt);return[Number(mod(u*x+v*y,q)),Number(mod((u+v)*x-u*y,q))];};
}
for(const c of R.controls){
  const original=source.native_controls.find(x=>x.seed===c.seed);check(original,"training cohort source");same(c.old_training_ids,original.decoder.original_ids,"same saved classical training ancestry");
  check(c.reused_classical_training_records_are_not_reused_quantum_inputs===true&&c.old_holdout_used_for_validation===false&&c.population_recovery_proved===false&&c.independent_physical_source_supply_certified_by_seeds===false,"source/training/fresh claim boundary");
  const model=c.model,D=description(model.nodes,c.modulus),K=model.nodes.length;
  same(model.nodes,original.decoder.model.nodes,"unchanged public circuit node set");same(model.cyclic_description,D,"ALL complete cyclic inequalities, not selected violations");
  check(model.cyclic_compilation_reads_truth_or_outcomes===false&&model.cyclic_cost_polynomial_in_q_not_logq===true,"compiler scope and cost");
  const S=c.solver;
  if(c.candidate!==null){
    check(S.status==="SOLVED_NUMERICALLY"&&S.audit.numerically_feasible&&S.audit.exact_PSD_or_optimality_certificate===false,"numerical solver admission only");
    const re=S.matrix_real,im=S.matrix_imag,tol=S.audit.feasibility_tolerance,seen=new Map();let diag=0,herm=0,diff=0,min=Infinity,imag=0;
    for(let i=0;i<K;i++)for(let j=0;j<K;j++){
      check(Number.isFinite(re[i][j])&&Number.isFinite(im[i][j]),"finite saved matrix");if(i===j)diag=Math.max(diag,Math.hypot(re[i][j]-1,im[i][j]));
      herm=Math.max(herm,Math.hypot(re[i][j]-re[j][i],im[i][j]+im[j][i]));const k=key(model.nodes[i].map((a,l)=>mod(a-model.nodes[j][l],c.modulus)));
      if(!seen.has(k))seen.set(k,[re[i][j],im[i][j]]);const v=seen.get(k);diff=Math.max(diff,Math.hypot(re[i][j]-v[0],im[i][j]-v[1]));
    }
    D.groups.forEach(g=>{for(let t=0;t<g.order;t++){let real=0,complex=0;g.power_entries.forEach((entry,k)=>{const i=Math.floor(entry/K),j=entry%K,theta=2*Math.PI*k*t/g.order,C=Math.cos(theta),T=Math.sin(theta);real+=C*re[i][j]+T*im[i][j];complex+=C*im[i][j]-T*re[i][j];});min=Math.min(min,real/g.order);imag=Math.max(imag,Math.abs(complex/g.order));}});
    near(min,S.audit.minimum_complete_cyclic_probability,"every new cyclic probability");near(imag,S.audit.complete_cyclic_imaginary_residual,"cyclic imaginary residue");check(D.constraints===S.audit.complete_cyclic_probabilities_checked&&min>=-tol&&imag<=tol&&Math.max(diag,herm,diff)<=tol,"complete strengthened numerical feasibility");
    // Independently check a numerical PSD slack, not an exact feasibility proof.
    const L=Array.from({length:K},()=>Array.from({length:K},()=>[0,0]));for(let j=0;j<K;j++){
      let v=re[j][j]+2*tol;for(let k=0;k<j;k++)v-=L[j][k][0]**2+L[j][k][1]**2;check(v>0,"numerically shifted PSD check");L[j][j]=[Math.sqrt(v),0];
      for(let i=j+1;i<K;i++){let a=re[i][j],b=im[i][j];for(let k=0;k<j;k++){const[x,y]=L[i][k],[u,z]=L[j][k];a-=x*u+y*z;b-=y*u-x*z;}L[i][j]=[a/L[j][j][0],b/L[j][j][0]];}
    }
    near(score(original.training_records,c.candidate),c.refinement.training_score,"training-selected refined candidate");same(c.candidate,c.refinement.candidate,"candidate frozen by training");cyclicChecks+=D.constraints;entries+=K*K;
  }
  const fresh=c.fresh_source,at=sourceChart(fresh.original_level);check(fresh.seed===c.seed+100&&fresh.original_level===original.original_source_batches[0].original_level&&fresh.records.length===c.new_fresh_native_qutrits&&c.new_fresh_native_qutrits===256,"NEW frozen validation source");
  fresh.original_ring_labels.forEach((z,i)=>{const f=z.map(at);same(fresh.records[i].first,f.map(x=>x[0]),"new first frequency");same(fresh.records[i].second,f.map(x=>x[1]),"new second frequency");});
  near(c.simultaneous_four_method_false_acceptance_upper,4*Math.exp(-2*256/81),"four-method union bound, no independence claim");
  const candidates={cyclic:c.candidate,old_SDP:original.decoder.candidate,classical14:original.decoder.matched_nonSDP_baseline.candidate,classical256:original.decoder.stronger_nonSDP_baseline.candidate};
  for(const[name,v]of Object.entries(c.fresh_verification)){
    same(v.candidate,candidates[name],"frozen method candidate");near(score(fresh.records,v.candidate),v.score,"new fresh raw score");check(v.threshold_passed===(v.score>=.5),"raw threshold");
    check(v.fresh_original_ids.length===256&&new Set(v.fresh_original_ids).size===256&&v.fresh_original_ids.every(x=>x.includes("NEW-fresh")&&!c.old_training_ids.includes(x)),"fresh disjoint ancestor ledger");
    check(v.candidate_selected_before_holdout&&v.distinct_IDs_prove_physical_IID_supply===false&&v.speedup_claim_allowed===false,"verification is not algorithm promotion");
    check(c.calibration_recovery_NOT_decoder_input[name]===(key(v.candidate)===key(original.calibration_secret_NOT_decoder_input)),"truth used only after candidate freezing");
  }
}
// This pins and independently verifies the rational root tables and old source.
cp.execFileSync(process.execPath,[path.join(__dirname,"ternary_character_sdp_gap_certificate_crosscheck.js"),gapPath],{stdio:"pipe"});
console.log(JSON.stringify({status:"PASS",exact_negative_laws:exactNegative,root_polygon_checks_exact:polygonChecks,numerical_cyclic_probabilities_checked:cyclicChecks,numerical_matrix_entries_checked:entries,global_realizability_or_population_recovery_certified:false}));
