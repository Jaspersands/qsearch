"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),{determinant}=require("./planted_qary_usvp_source_crosscheck.js");
const {check,same,rat,zero,one,add,sub,mul,div,cmp,parse,str}=E;
const ROOT=path.resolve(__dirname,"../.."),FILE=path.join(ROOT,"research/phase_workbench/dcp_carry_congruence_source.json");
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
const I=x=>{check(typeof x==="string"||Number.isSafeInteger(x),"exact integer source data");return typeof x==="string"&&x.startsWith("-0x")?-BigInt(x.slice(1)):BigInt(x);};
const mod=(x,q)=>(x%q+q)%q,abs=x=>x<0n?-x:x;
const matrix=A=>A.map(row=>row.map(I));
const matSame=(a,b,msg)=>same(a.map(row=>row.map(String)),b.map(row=>row.map(String)),msg);
function multiply(A,B){return A.map(row=>B[0].map((_,j)=>row.reduce((v,x,k)=>v+x*B[k][j],0n)));}
function gcd(a,b){a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a;}
function probability(P){
  check(P&&["0x0","0x1"].includes(P.numerator_hex),"explicit exact binary probability");
  const e=I(P.denominator_binary_exponent);check(e>=0n&&e<=1000000n,"UNKNOWN_PROBABILITY_REPLAY_CAP");
  check(P.numerator_hex!=="0x0"||e===0n,"canonical zero probability");
  return rat(BigInt(P.numerator_hex),1n<<e);
}

function lattice(C,expected) {
  const G=matrix(C.generator_rows),H=matrix(C.row_hnf_basis),A=matrix(C.basis_from_generator_coefficients),B=matrix(C.generators_from_basis_coefficients);
  matSame(G,expected,"intended lattice generators");
  matSame(multiply(A,G),H,"basis belongs to original integer lattice");
  matSame(multiply(B,H),G,"all original generators belong to basis lattice");
  const d=H.length;
  check(H.every((row,i)=>row.length===d&&row[i]>0n&&row.slice(0,i).every(x=>x===0n)),"constraint-first upper row HNF");
  const index=abs(determinant(H));
  check(index===I(C.integer_lattice_index)&&C.HNF_rows===G.length&&C.HNF_columns===d&&
    C.internal_transform_cells===G.length**2,"paid exact lattice index and dimensions");
  const bits=G.flat().reduce((v,x)=>Math.max(v,abs(x).toString(2).replace(/^0$/,"").length),0);
  check(bits===C.largest_generator_entry_bits,"integer bit-length accounting");
  return {H,index};
}

function rowCoordinates(target,H) {
  const x=[];
  for(let j=0;j<H.length;j++) {
    let r=rat(target[j]);for(let i=0;i<j;i++)r=sub(r,mul(x[i],rat(H[i][j])));
    x.push(div(r,rat(H[j][j])));
  }
  return x;
}

function affine(L,R,D,J,Q,targets,offsets) {
  matSame(matrix(L.constraint_matrix),R,"native mixed-modulus constraints");
  matSame(matrix(L.output_matrix),J,"physical linear output labels");
  same(L.constraint_moduli.map(x=>String(I(x))),D.map(String),"all constraint periods");
  matSame(matrix(L.component_output_offsets),offsets,"component label offsets");
  check(I(L.input_modulus)===Q&&L.input_width===J[0].length,"native higher-label domain");
  const m=J[0].length,c=R.length,d=J.length;
  let rc={H:[],index:1n};
  if(c) {
    const generators=Array.from({length:m},(_,i)=>R.map(row=>row[i]));
    for(let i=0;i<c;i++)generators.push(Array.from({length:c},(_,j)=>i===j?D[i]:0n));
    rc=lattice(L.constraint_lattice_certificate,generators);
  }else check(L.constraint_lattice_certificate===null,"empty constraint module");
  const joint=Array.from({length:m},(_,i)=>R.map(row=>row[i]).concat(J.map(row=>row[i])));
  for(let i=0;i<c;i++)joint.push(Array.from({length:c+d},(_,j)=>i===j?D[i]:0n));
  for(let i=0;i<d;i++)joint.push(Array.from({length:c+d},(_,j)=>j===c+i?Q:0n));
  const jc=lattice(L.joint_lattice_certificate,joint),A=jc.H.slice(c).map(row=>row.slice(c)),index=abs(determinant(A));
  matSame(A,matrix(L.output_kernel_integer_basis),"correct bottom-right output kernel block");
  const volume=Q**BigInt(d),support=volume/index,totalD=D.reduce((a,b)=>a*b,1n);
  check(jc.index===rc.index*index&&volume%index===0n&&totalD%rc.index===0n&&
    index===I(L.output_kernel_lattice_index)&&support===I(L.output_support_size_per_accepted_component)&&
    totalD/rc.index===I(L.constraint_image_size),"exact image/fiber cardinalities");
  for(let j=0;j<d;j++) {
    const period=A.reduce((g,row)=>gcd(g,row[j]),Q);
    check(Q/period===I(L.output_marginal_support_sizes[j]),"marginal support, not a joint IID assertion");
  }
  check(L.components.length===targets.length,"all independent native components accounted");
  let all=true;
  L.components.forEach((C,l)=>{
    same(C.target.map(x=>String(I(x))),targets[l].map(String),"actual component target");
    const coefficients=rowCoordinates(targets[l],rc.H),possible=coefficients.every(x=>x[1]===1n);
    check(C.acceptance_possible===possible,"integer target consistency");all=all&&possible;
    if(!possible) {
      same(C.nonintegral_constraint_basis_coordinates,coefficients.map(str),"exact nonintegral membership obstruction");return;
    }
    const z=C.particular_higher_label_solution.map(I);
    check(z.length===m&&z.every(x=>x>=0n&&x<Q),"canonical particular higher-label solution");
    R.forEach((row,i)=>check(mod(row.reduce((s,x,k)=>s+x*z[k],0n),D[i])===targets[l][i],"actual congruences satisfied"));
    const y=J.map((row,j)=>mod(row.reduce((s,x,k)=>s+x*z[k],0n)+offsets[l][j],Q));
    same(y.map(String),C.output_coset_representative.map(x=>String(I(x))),"actual affine output coset");
  });
  const per=rat(rc.index,totalD);
  let jointMass=one;for(let l=0;l<targets.length;l++)jointMass=mul(jointMass,per);
  if(!all)jointMass=zero;
  check(cmp(probability(L.acceptance_probability_per_consistent_component),per)===0n&&
    cmp(probability(L.joint_native_acceptance_probability),jointMass)===0n&&L.acceptance_possible===all&&
    L.conditional_output_uniform_on_reported_affine_cosets===all&&
    L.conditional_joint_labels_IID_uniform_mod_Q===(all&&index===1n)&&
    L.particular_solution_is_not_unknown_quantum_state_preparation===true&&L.state_or_higher_label_enumeration_used===false,"conditional source law, not a quantum sampler");
  if(all)check((1n<<I(L.expected_supplied_attempts_IF_fresh_batches_exist.power_of_two))*jointMass[0]===jointMass[1],"native resupply attempts remain paid");
  else check(L.expected_supplied_attempts_IF_fresh_batches_exist===null,"impossible event has no finite resupply cost");
  check(L.resupply_cost_model==="INDEPENDENT_SUPPLIED_BATCH_REJECTION; not a coherent-preparation lower bound","no general quantum resupply lower bound");
  check(L.joint_coordinate_order==="CONSTRAINTS_FIRST_OUTPUTS_LAST_FLINT_ROW_HNF","correct HNF convention");
  return {possible:all,support,mass:jointMass,A};
}

function* combinations(n,h,start=0,prefix=[]) {
  if(!h){yield prefix;return;}
  for(let j=start;j<=n-h;j++)yield* combinations(n,h-1,j+1,prefix.concat(j));
}
function binaryRank(values) {
  const pivots=new Map();let rank=0;
  for(let x of values)while(x) {
    const p=x.toString(2).length-1;
    if(pivots.has(p))x^=pivots.get(p);else{pivots.set(p,x);rank++;break;}
  }
  return rank;
}

function lex(a,b){for(let i=0;i<Math.min(a.length,b.length);i++)if(a[i]!==b[i])return a[i]-b[i];return a.length-b.length;}
const better=(a,b)=>!b||a.length<b.length||(a.length===b.length&&lex(a,b)<0);
function minimumOverlapReference(U,t) {
  const d=U.length,disjoint=U.every((u,i)=>U.slice(i+1).every(v=>(u&v)===0n));
  if(disjoint)return {mixed:[],work:{distinct_nonzero_intersections:d,mixed_intersection_constraints:0,pairwise_intersections_evaluated:d*(d-1)/2}};
  check(d<=12,"UNKNOWN_NONDISJOINT_OVERLAP_REFERENCE_CAP");
  // Independent full-subset reference, not the compiler's pruned recurrence.
  const all=new Map(),mixed=new Map(),subsets=[];
  for(let mask=1;mask<1<<d;mask++) {
    const S=Array.from({length:d},(_,i)=>i).filter(i=>mask&(1<<i));if(S.length>t)continue;
    const e=S.reduce((x,i)=>x&U[i],U[S[0]]);if(!e)continue;
    subsets.push([e,S]);const key=String(e);
    if(better(S,all.get(key)))all.set(key,S);
    if(S.length>=2&&better(S,mixed.get(key)))mixed.set(key,S);
  }
  let work=0;
  for(let j=0;j<d;j++) {
    const prefix=new Map();
    for(const [e,S] of subsets)if(S[S.length-1]<j&&better(S,prefix.get(String(e))))prefix.set(String(e),S);
    work+=Array.from(prefix.values()).filter(S=>S.length<t).length;
  }
  return {mixed:Array.from(mixed,([e,S])=>[BigInt(e),S]).sort((a,b)=>a[1].length-b[1].length||lex(a[1],b[1])),
    work:{distinct_nonzero_intersections:all.size,mixed_intersection_constraints:mixed.size,pairwise_intersections_evaluated:work}};
}

function binomial(n,k){let v=1n;for(let i=1;i<=k;i++)v=v*BigInt(n-k+i)/BigInt(i);return v;}

function native(C) {
  const B=C.low_label_matrix,t=C.phase_exponent,n=B.length,m=B[0].length,U=C.physical_directions_hex.map(BigInt),d=U.length;
  const x=BigInt(C.physical_background_hex),Q=1n<<BigInt(t-1),whole=(1n<<BigInt(m))-1n;
  check(I(C.modulus)===2n*Q&&C.dimension===n&&C.physical_input_width===m&&C.retained_outputs===d&&
    C.selection_model_required==="low-bits-and-initial-syndrome-only"&&C.fresh_native_batches_supplied_by_compiler===false&&
    C.coherent_native_parent_inverse_or_amplification_supplied===false&&
    C.reported_entropy_is_public_label_entropy_not_secret_information===true,"actual phase level, dimensions and source supply");
  check(cmp(probability(C.probability_of_this_fixed_B_under_IID_native_low_bits),rat(1n,1n<<BigInt(n*m)))===0n&&
    C.observed_B_is_not_automatically_a_rejection_filter===true,"fixed-B calibration is not a free postselected native source");
  check(binaryRank(U)===d&&U.every(u=>u>0n&&u<=whole)&&x>=0n&&x<=whole,"independent physical directions and background");
  check(B.every(row=>row.length===m&&row.every(x=>x===0||x===1)),"binary low-label input");
  const signs=Array.from({length:m},(_,i)=>(x>>BigInt(i))&1n?-1n:1n);
  for(const row of B)for(const u of U)check(row.reduce((s,b,i)=>s+b*Number((u>>BigInt(i))&1n),0)%2===0,"parity-kernel directions");
  const R=[],D=[],targets=B.map(()=>[]),monomials=[];let terms=0n,checked=0;
  for(let h=2;h<=Math.min(d,t);h++)terms+=binomial(d,h);
  const overlaps=minimumOverlapReference(U,t);
  same(overlaps.work,C.overlap_closure_work,"compressed intersection work, not exponential monomial enumeration");
  check(terms===I(C.monomial_expansion_terms)&&C.selection_lineage_programmatically_verified===false&&
    C.quantum_product_extraction_circuit_compiled===false&&C.efficient_receiver_supplied===false&&
    C.accepted_speedup_candidate===false&&C.novelty_claim===false,"honest source and selection scope");
  for(const [overlap,subset] of overlaps.mixed) {
    const h=subset.length;checked++;
    const row=signs.map((e,i)=>e*((overlap>>BigInt(i))&1n));
    const sums=B.map(b=>row.reduce((s,e,i)=>s+e*BigInt(b[i]),0n));
    if(sums.some(z=>z%2n!==0n)) {
      check(C.acceptance_possible===false&&C.reason==="LOW_BIT_MIXED_MONOMIAL_OBSTRUCTION"&&
        C.monomials_checked===checked&&cmp(probability(C.joint_native_acceptance_probability),zero)===0n,"real low-bit obstruction");
      return {possible:false,enumerated:false};
    }
    if(h===t||overlap===0n)continue;
    const period=1n<<BigInt(t-h);R.push(row);D.push(period);
    monomials.push({degree:h,subset,overlap_hex:"0x"+overlap.toString(16)});
    sums.forEach((z,l)=>targets[l].push(mod(-z/2n,period)));
  }
  same(monomials,C.higher_label_congruence_monomials,"all higher-degree constraints, not pair parities only");
  check(C.monomials_checked===checked,"actual monomial work");
  const J=U.map(u=>signs.map((e,i)=>e*((u>>BigInt(i))&1n)));
  const offsets=B.map(b=>U.map(u=>mod(signs.reduce((s,e,i)=>s+e*BigInt(b[i])*((u>>BigInt(i))&1n),0n)/2n,Q)));
  const law=affine(C.source_law,R,D,J,Q,targets,offsets);
  check(C.acceptance_possible===law.possible&&cmp(probability(C.joint_native_acceptance_probability),law.mass)===0n&&
    C.all_top_output_bits_jointly_uniform_IF_accepted===law.possible&&
    C.native_law_background_invariant_IF_selection_lineage_holds===true&&
    C.free_postselection_or_fresh_label_oracle_supplied===false,"conditional native acceptance and output scope");
  if(law.possible) {
    check((law.support&(law.support-1n))===0n&&law.support>=(1n<<BigInt(d)),"free top output bits");
    check(C.conditional_output_entropy_bits_IF_accepted===n*(law.support.toString(2).length-1),"joint entropy, not marginal entropy sum");
    check(C.expected_original_phase_registers_IF_independent_fresh_batches.coefficient===m&&
      I(C.expected_original_phase_registers_IF_independent_fresh_batches.power_of_two)===I(C.source_law.expected_supplied_attempts_IF_fresh_batches_exist.power_of_two),"all original phase registers paid per supplied batch");
  }else check(C.conditional_output_entropy_bits_IF_accepted===null,"no conditional law for an impossible event");
  // Symbolic background change: Z'=epsilon Z-xB. Check its targets/offsets.
  R.forEach((row,j)=>B.forEach((b,l)=>{
    let sumB=0n,translation=0n;
    row.forEach((e,i)=>{const included=e!==0n;sumB+=included?BigInt(b[i]):0n;translation+=included&&((x>>BigInt(i))&1n)?BigInt(b[i]):0n;});
    check(mod(targets[l][j]-mod(-sumB/2n,D[j])-translation,D[j])===0n,"background target relabeling identity");
  }));
  U.forEach((u,j)=>B.forEach((b,l)=>{
    let sumB=0n,translation=0n;
    for(let i=0;i<m;i++)if((u>>BigInt(i))&1n){sumB+=BigInt(b[i]);if((x>>BigInt(i))&1n)translation+=BigInt(b[i]);}
    check(mod(offsets[l][j]-sumB/2n+translation,Q)===0n,"background output relabeling identity");
  }));
  return {possible:law.possible,enumerated:false};
}

function verify(R) {
  check(R.producer_sha256===hash(path.join(ROOT,"theorems/dcp_carry_congruence_source.py"))&&
    R.derivation_sha256===hash(path.join(ROOT,"research/DCP_CARRY_CONGRUENCE_SOURCE.md"))&&
    R.contract_sha256===hash(path.join(ROOT,"research/hypotheses/dcp_carry_congruence_source_contract.json")),"current provenance");
  check(R.native_source_controls.length===24,"complete fixed conditional control set");
  R.native_source_controls.forEach(native);
  const large=R.large_exact_not_enumerated_control;native(large);
  check(cmp(probability(large.joint_native_acceptance_probability),rat(1n,1n<<992n))===0n,"fresh output does not remove the 2^-992 acceptance cost");
  const disjoint=R.large_disjoint_compressed_control;native(disjoint);
  check(disjoint.phase_exponent===1024&&disjoint.retained_outputs===64&&disjoint.monomials_checked===0&&
    disjoint.overlap_closure_work.pairwise_intersections_evaluated===2016,"large sparse packet compiled without expanding 2^64 terms");
  check(native(R.parity_passes_but_integer_targets_inconsistent_control).possible===false,"integer inconsistency beyond all binary parity tests");
  check(R.quantum_source_or_receiver_implemented===false&&R.hardness_or_quantum_speedup_demonstrated===false&&
    R.accepted_speedup_candidate===false&&R.new_active_negative_result_created===false&&R.novelty_claim===false,"no quantum circuit, decoder or hardness promotion");
  return {verified:true,conditional_controls:24,large_phase_exponents:[64,1024],integer_target_counterexample:true,quantum_receiver:false};
}
module.exports={verify,native,lattice};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||FILE,"utf8"))),null,2));
