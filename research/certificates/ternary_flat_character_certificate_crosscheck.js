"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto"),cp=require("child_process");
const root=path.join(__dirname,"../.."),R=JSON.parse(fs.readFileSync(process.argv[2]||path.join(root,"research/classical_baselines/ternary_flat_character_certificate.json"),"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},key=JSON.stringify,same=(a,b,m)=>check(key(a)===key(b),m);
const mod=(x,q)=>(x%q+q)%q,dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b)[a,b]=[b,a%b];return a;}
function rat(a,b=1n){if(b<0n){a=-a;b=-b;}check(b!==0n,"rational denominator");const g=gcd(a,b);return[a/g,b/g];}
const zero=rat(0n),one=rat(1n),add=(a,b)=>rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),neg=a=>[-a[0],a[1]],sub=(a,b)=>add(a,neg(b)),mul=(a,b)=>rat(a[0]*b[0],a[1]*b[1]),div=(a,b)=>rat(a[0]*b[1],a[1]*b[0]);
const str=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1],parse=s=>{const p=s.split("/");return rat(BigInt(p[0]),p.length===1?1n:BigInt(p[1]));},cmp=(a,b)=>a[0]*b[1]-b[0]*a[1];
function pow(a,n){let b=one;while(n){if(n%2)b=mul(b,a);n=Math.floor(n/2);if(n)a=mul(a,a);}return b;}
function field(q){
  const d=2*q/3,F=()=>Array.from({length:d},()=>zero),eq=(a,b)=>a.every((x,i)=>cmp(x,b[i])===0n),plus=(a,b)=>a.map((x,i)=>add(x,b[i]));
  function times(a,b){const c=Array.from({length:2*d-1},()=>zero);a.forEach((x,i)=>b.forEach((y,j)=>c[i+j]=add(c[i+j],mul(x,y))));for(let i=c.length-1;i>=d;i--){const x=c[i];c[i-d]=sub(c[i-d],x);c[i-d+d/2]=sub(c[i-d+d/2],x);}return c.slice(0,d);}
  const unit=F();unit[0]=one;const z=F();z[1]=one;const powers=[unit];for(let i=1;i<q;i++)powers.push(times(powers[i-1],z));check(eq(times(powers[q-1],z),unit),"full cyclotomic root order");
  function decode(raw){check(Array.isArray(raw)&&raw.length<=d&&raw.every(x=>typeof x==="string"),"exact canonical cyclotomic encoding");const a=F();raw.slice().reverse().forEach((x,i)=>a[i]=parse(x));same(encode(a),raw,"reduced canonical polynomial");return a;}
  function encode(a){let k=a.length;while(k&&a[k-1][0]===0n)k--;return a.slice(0,k).reverse().map(str);}
  const scale=(a,r)=>a.map(x=>mul(x,r)),conj=a=>a.reduce((v,x,i)=>plus(v,scale(powers[mod(-i,q)],x)),F());
  return{q,d,F,unit,powers,eq,plus,times,decode,encode,scale,conj};
}
function piInterval(N){
  function atan(k){const x=rat(1n,BigInt(k)),x2=mul(x,x);let sum=zero,p=x;for(let j=0;j<N;j++){sum=add(sum,div(j%2?neg(p):p,rat(BigInt(2*j+1))));p=mul(p,x2);}const next=div(N%2?neg(p):p,rat(BigInt(2*N+1))),end=add(sum,next);return cmp(sum,end)<=0?[sum,end]:[end,sum];}
  const a=atan(5),b=atan(239);return[sub(mul(rat(16n),a[0]),mul(rat(4n),b[1])),sub(mul(rat(16n),a[1]),mul(rat(4n),b[0]))];
}
function signCertificate(K,a,c){
  check(K.eq(a,K.conj(a)),"character weight real in specified embedding");
  if(a.slice(1).every(x=>x[0]===0n)){const s=a[0][0]>0n?"POSITIVE":a[0][0]<0n?"NEGATIVE":"ZERO";check(c.status===s&&c.rational_value===str(a[0])&&c.lower===str(a[0])&&c.upper===str(a[0]),"exact rational sign");return s;}
  const N=c.Machin_arctangent_terms,L=c.cosine_Taylor_terms;check(Number.isInteger(N)&&N>=8&&N<=128&&L===N,"bounded rational sign certificate");
  const bounds=piInterval(N),center=div(add(...bounds),rat(2n)),radius=div(sub(bounds[1],bounds[0]),rat(2n));let lo=zero,hi=zero;
  a.forEach((coefficient,k)=>{if(coefficient[0]===0n)return;const x=div(mul(rat(BigInt(2*k)),center),rat(BigInt(K.q))),x2=mul(x,x);let term=one,sum=one;for(let j=1;j<L;j++){term=div(neg(mul(term,x2)),rat(BigInt((2*j-1)*(2*j))));sum=add(sum,term);}let factorial=1n;for(let j=2;j<=2*L;j++)factorial*=BigInt(j);const error=add(div(pow(x,2*L),rat(factorial)),div(mul(rat(BigInt(2*k)),radius),rat(BigInt(K.q)))),left=sub(sum,error),right=add(sum,error);lo=add(lo,mul(coefficient,coefficient[0]>0n?left:right));hi=add(hi,mul(coefficient,coefficient[0]>0n?right:left));});
  check(c.lower===str(lo)&&c.upper===str(hi)&&c.interval_uses_only_exact_rational_arithmetic===true,"recomputed Machin/Taylor sign interval");check((c.status==="POSITIVE"&&lo[0]>0n)||(c.status==="NEGATIVE"&&hi[0]<0n),"strict certified weight sign");return c.status;
}
function chart(level){
  let V=[[1n,0n],[0n,1n]],pi=[[-1n,-1n],[1n,-2n]];for(let j=0;j<level-1;j++)V=V.map(row=>pi[0].map((_,i)=>row.reduce((s,a,k)=>s+a*pi[k][i],0n)));
  const q=3n**BigInt(level/2),den=3n*(V[0][0]*V[1][1]-V[0][1]*V[1][0]),a=q*(2n*V[1][1]+V[1][0]),b=q*(-2n*V[0][1]-V[0][0]);check(a%den===0n&&b%den===0n,"true native chart integral");const u=a/den,v=b/den;return label=>{const[x,y]=label.map(BigInt);return[Number((u*x+v*y)%q+q)%Number(q),Number(((u+v)*x-u*y)%q+q)%Number(q)];};
}
function compile(records,base,b){
  const q=records[0].modulus,n=records[0].first.length,D=records.map(r=>r.first.map((x,i)=>mod(x-r.second[i],q))),I=b.modular_unit_difference_inverse,indices=b.basis_record_indices;
  check(indices.length===n&&new Set(indices).size===n&&b.rank_mod3===n,"full native unit-difference basis");for(let i=0;i<n;i++)for(let j=0;j<n;j++)check(mod(dot(D[indices[i]],I.map(row=>row[j])),q)===Number(i===j),"exact full-root basis inverse");
  const S=[],lookup=new Map(),trace=[];function offset(v){v=v.map(x=>mod(x,q));const k=key(v);if(!lookup.has(k)){lookup.set(k,S.length);S.push(v);}return lookup.get(k);}
  const zero=offset(Array(n).fill(0)),generators=indices.map(i=>offset(D[i]));function add(i,j){const k=offset(S[i].map((x,l)=>x+S[j][l]));trace.push({left_offset:i,right_offset:j,result_offset:k});return k;}
  const powers=new Map();function multiply(i,c){let total=zero,power=i,bit=0;while(c){if(c%2)total=add(total,power);c=Math.floor(c/2);bit++;if(c){const k=key([i,bit]);if(!powers.has(k))powers.set(k,add(power,power));power=powers.get(k);}}return total;}
  const commuting=[];generators.forEach((a,i)=>generators.slice(i+1).forEach(b=>commuting.push({left_generator:a,right_generator:b,sum_offset:add(a,b)})));
  const loops=generators.map(i=>({generator_offset:i,integer_multiplier:q,endpoint_offset:multiply(i,q)})),targets=base.map((v,j)=>{const coefficients=I[0].map((_,i)=>mod(dot(v,I.map(row=>row[i])),q));let total=zero;generators.forEach((i,k)=>{if(coefficients[k])total=add(total,multiply(i,coefficients[k]));});same(S[total],v,"each original native frequency reconstructed");return{base_frequency_index:j,basis_coefficients:coefficients,endpoint_offset:total};});
  const W=[],index=new Map();base.forEach(v=>S.forEach(s=>{const w=v.map((x,i)=>mod(x+s[i],q)),k=key(w);if(!index.has(k)){index.set(k,W.length);W.push(w);}}));
  return{S,W,trace,commuting,loops,targets,generators,baseIndices:base.map(v=>index.get(key(v))),translated:S.map(s=>base.map(v=>index.get(key(v.map((x,i)=>mod(x+s[i],q)))))),D};
}
function det(K,A){
  // This independent control checker bounds minor size; it is not a general
  // replacement for the production exact-field rank/extraction implementation.
  check(A.length<=6,"independent determinant control cap exceeded");if(A.length===0)return K.unit;let sum=K.F();A[0].forEach((x,j)=>{const minor=A.slice(1).map(row=>row.filter((_,i)=>i!==j));sum=K.plus(sum,K.scale(K.times(x,det(K,minor)),rat(j%2?-1n:1n)));});return sum;
}
check(R.derivation_sha256===hash(path.join(root,"research/TERNARY_FLAT_CHARACTER_CERTIFICATE.md")),"pinned exact flat derivation");
let entries=0,atomsChecked=0,nonrational=0;
const controls=[...R.native_controls,R.nonrational_positive_weight_countercontrol];same(R.native_controls.map(c=>c.seed),[89641,89643],"prespecified actual native sources");
for(const c of controls){
  const records=c.records,q=records[0].modulus,K=field(q),layout=c.layout,V=layout.base_frequencies,at=chart(c.original_native_level),frequencies=c.original_ring_labels.map(row=>{const f=row.map(at);return[f.map(x=>x[0]),f.map(x=>x[1])];});
  same(c.original_native_frequencies,frequencies,"original cyclotomic/native chart");records.forEach((r,i)=>{same(r.first,frequencies[i][0],"native first row");same(r.second,frequencies[i][1],"native second row");check(r.modulus===3**(c.original_native_level/2),"actual retained root");});
  const rebuilt=compile(records,V,layout.difference_basis);for(const[a,b]of[["offsets","S"],["extension_frequencies","W"],["addition_trace","trace"],["commutation_sums","commuting"],["basis_q_loops","loops"],["base_targets","targets"],["generator_offsets","generators"],["original_block_indices","baseIndices"],["translated_node_indices","translated"]])same(layout[a],rebuilt[b],"independent complete translate layout: "+a);
  check(rebuilt.loops.every(x=>x.endpoint_offset===0)&&layout.dense_classical_moment_entries===rebuilt.W.length**2&&layout.cyclotomic_field_degree===K.d,"integer orders / actual classical matrix costs");
  const verified=c.verification,atoms=verified.character_atoms,weights=atoms.map(a=>K.decode(a.weight));check(verified.character_distribution_certified===true&&verified.PSD_certified_by_positive_character_reconstruction===true,"positive character certificate status");
  atoms.forEach((a,i)=>{check(signCertificate(K,weights[i],a.positive_weight_certificate)==="POSITIVE","strictly positive support atom");if(a.positive_weight_certificate.interval_uses_only_exact_rational_arithmetic)nonrational++;});check(K.eq(weights.reduce(K.plus,K.F()),K.unit),"normalized exact positive weights");
  const W=rebuilt.W,M=c.extension_moment_matrix,old=c.original_moment_matrix;check(M.length===W.length&&M.every(row=>row.length===W.length)&&old.length===V.length&&old.every(row=>row.length===V.length),"whole original/extension matrix shape");
  W.forEach((u,i)=>W.forEach((v,j)=>{const expected=atoms.reduce((s,a,k)=>K.plus(s,K.times(weights[k],K.powers[mod(dot(u.map((x,l)=>x-v[l]),a.secret),q)])),K.F());check(K.eq(K.decode(M[i][j]),expected),"every supplied entry reconstructed by genuine positive characters");}));
  V.forEach((_,i)=>V.forEach((_,j)=>same(old[i][j],M[rebuilt.baseIndices[i]][rebuilt.baseIndices[j]],"retained original block exact")));
  const independent=verified.independent_base_frequency_indices;check(independent.length===atoms.length&&new Set(independent).size===atoms.length,"complete original base rank minor");const E=independent.map(i=>atoms.map(a=>K.powers[mod(dot(V[i],a.secret),q)]));check(!K.eq(det(K,E),K.F()),"exact nonzero native character evaluation minor proves base rank");
  check(verified.rank_original_exact===atoms.length&&verified.rank_extension_exact===atoms.length&&verified.all_moment_entries_checked===W.length**2&&verified.translation_operators_checked===rebuilt.S.length,"flat rank and complete checks");
  let prefixes=new Set(["[]"]),scans=0;const values=atoms.map(a=>layout.difference_basis.basis_record_indices.map(i=>mod(dot(rebuilt.D[i],a.secret),q)));for(let i=0;i<records[0].first.length;i++){scans+=q*prefixes.size;prefixes=new Set(values.map(v=>key(v.slice(0,i+1))));}check(verified.projector_eigenvalues_scanned===scans&&verified.projector_terms_charged===q*scans&&verified.field_degree_charged===K.d&&verified.full_secret_grid_size===String(BigInt(q)**BigInt(records[0].first.length)),"q eigenvalue scanning costs, not q^n search");
  const rounding=c.harmonic_score_rounding;const score=secret=>records.reduce((s,r)=>{const a=mod(r.outcome[0]-dot(r.first,secret),q),b=mod(r.outcome[1]-dot(r.second,secret),q);return[a,b,mod(a-b,q)].reduce((t,e)=>K.plus(t,K.scale(K.plus(K.powers[e],K.powers[mod(-e,q)]),rat(1n,2n))),s);},K.F());
  const average=atoms.reduce((s,a,i)=>K.plus(s,K.times(weights[i],score(a.secret))),K.F()),selected=score(rounding.selected_secret);check(atoms.some(a=>key(a.secret)===key(rounding.selected_secret))&&K.eq(K.decode(rounding.selected_score),selected)&&K.eq(K.decode(rounding.mixture_score),average),"classical rounding scores exactly recomputed");check(["POSITIVE","ZERO"].includes(signCertificate(K,K.plus(selected,K.scale(average,rat(-1n))),rounding.margin_certificate)),"selected character dominates exact moment score");
  check(rounding.only_extracted_character_candidates_tested===atoms.length&&rounding.native_noisy_recovery_proved===false&&rounding.held_out_native_prediction_verified===false&&rounding.native_log_likelihood_is_this_score===false,"rounding is not noisy recovery/log likelihood");
  const inputBits=M.flat(2).reduce((s,x)=>{const a=parse(x),num=a[0]<0n?-a[0]:a[0];return Math.max(s,num===0n?0:num.toString(2).length,a[1].toString(2).length);},0);
  check(verified.classical_extension_compact_JSON_bytes===JSON.stringify(M).length&&verified.input_max_rational_coefficient_bits===inputBits&&Number.isInteger(verified.retained_coordinate_operator_atom_max_coefficient_bits)&&verified.retained_coordinate_operator_atom_max_coefficient_bits>0,"classical input/retained coefficient costs not free");
  for(const k of["full_secret_grid_enumerated","floating_PSD_or_rank_tolerance_used","classical_completion_algorithm_supplied","all_internal_intermediate_bit_costs_certified","native_noisy_recovery_proved","quantum_speedup_proved"])check(verified[k]===false,"unsupported extraction claim: "+k);
  check(c.known_atoms_used_only_by_calibration_producer===true&&c.supplied_matrix_was_learned_from_noisy_native_records===false&&c.external_IID_native_supply_certified===false,"honest calibration / source access");entries+=W.length**2;atomsChecked+=atoms.length;
}
check(R.native_nonextension_source==="research/classical_baselines/ternary_observable_moment_lift.json"&&R.native_nonextension_source_sha256===hash(path.join(root,R.native_nonextension_source)),"retained native nonextension source pinned");
const source=JSON.parse(fs.readFileSync(path.join(root,R.native_nonextension_source),"utf8")),original=JSON.parse(fs.readFileSync(path.join(root,source.source_report),"utf8"));
const priorCheck=JSON.parse(cp.execFileSync("node",[path.join(__dirname,"ternary_observable_moment_lift_crosscheck.js")],{encoding:"utf8"}));check(priorCheck.status==="PASS","independent retained native nonextension replay");
same(R.native_nonextension_controls.map(c=>c.source_seed),[89513,89523,89533],"all preregistered negative sources retained");
for(const c of R.native_nonextension_controls){const prior=source.native_controls.find(x=>x.source_seed===c.source_seed),lift=original.native_controls.find(x=>x.seed===c.source_seed).adaptive_character_lift,lookup=new Map();lift.nodes.forEach((x,i)=>{if(!lookup.has(key(x.frequency)))lookup.set(key(x.frequency),i);});const selected=[...lookup.values()],classes=prior.partition_witness.class_labels,first=selected.findIndex(i=>classes[i]!==classes[selected[0]]),issue=c.verification.issues[0];check(first>=0&&c.base_node_count===selected.length&&c.exact_original_PSD_rank===prior.partition_witness.matrix_rank_exact,"retained original PSD classes");same(issue.frequency,lift.nodes[selected[first]].frequency,"actual inconsistent native anchor");check(issue.frequency_index===first&&key(issue.anchor_value)==="[]"&&c.saturation_guard_runs_before_extension_construction===true&&c.verification.status==="REJECTED_CHARACTER_DISTRIBUTION_SATURATION"&&c.verification.character_distribution_certified===false,"saturation rejects before caps/completion");same(issue.unit_difference_basis,prior.difference_basis,"same exact unit difference basis");}
check(R.status==="EXACT_NATIVE_FLAT_CERTIFICATE_CONDITIONAL_CLASSICAL_EXTRACTION_REVIEW_PENDING","research status");for(const k of["completion_solver_implemented","approximate_flatness_proved","native_noisy_decoder_supplied","quantum_speedup_proved","candidate_record_accepted"])check(R[k]===false,"unproved research claim: "+k);
console.log(JSON.stringify({status:"PASS",exact_cyclotomic_moment_entries:entries,positive_character_atoms:atomsChecked,nonrational_weight_intervals:nonrational,retained_native_nonextension_falsifiers:R.native_nonextension_controls.length,native_noisy_decoder_supplied:false}));
