"use strict";

// Exact independent replay of a finite public instrument, not a receiver.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js");
const {primeCertificate} = require("./planted_qary_usvp_source_crosscheck.js");
const {verifyPlan} = require("./lattice_qft_precision_crosscheck.js");
const {check, same, rat, zero, one, add, sub, mul, div, str, parse, cmp} = E;
const ROOT = path.resolve(__dirname, "../..");
const FILE = path.join(ROOT, "research/phase_workbench/lattice_sine_window_source.json");
const hash = p => crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
const abs = x => x < 0n ? -x : x;
const dyadic = x => Number.isSafeInteger(x) && x >= 2 && (BigInt(x) & (BigInt(x)-1n)) === 0n;

function field(R) {
  check(dyadic(R) && R >= 4 && R <= 128, "bounded dyadic reference field");
  const d=R/2, F=()=>Array.from({length:d},()=>zero);
  function monomial(j) {
    j=(j%R+R)%R; const a=F(); a[j%d]=rat(j<d?1n:-1n); return a;
  }
  const plus=(a,b)=>a.map((x,i)=>add(x,b[i]));
  const scale=(a,b)=>a.map(x=>mul(x,b));
  const minus=(a,b)=>plus(a,scale(b,rat(-1n)));
  function times(a,b) {
    const c=F();
    a.forEach((x,i)=>{if(x[0])b.forEach((y,j)=>{
      if(y[0]) c[(i+j)%d]=add(c[(i+j)%d],mul(mul(x,y),rat(i+j<d?1n:-1n)));
    });});
    return c;
  }
  function encode(a) {let k=d;while(k&&!a[k-1][0])k--;return a.slice(0,k).reverse().map(str);}
  function decode(a) {
    check(Array.isArray(a)&&a.length<=d,"complete field polynomial");
    const out=F();a.slice().reverse().forEach((x,i)=>out[i]=parse(x));
    same(encode(out),a,"canonical field encoding");return out;
  }
  function value(a) {
    return a.reduce((v,x,j)=>{
      const t=Number(x[0])/Number(x[1]), angle=2*Math.PI*j/R;
      return [v[0]+t*Math.cos(angle),v[1]+t*Math.sin(angle)];
    },[0,0]);
  }
  return {F,monomial,plus,scale,minus,times,encode,decode,value};
}

function affinity(K,t,F,R) {
  // Independent sine-product convolution, rather than Python's cos difference.
  let a=F.F();
  for(let x=1;x<K;x++)if(x-t>=1&&x-t<K) {
    const u=F.minus(F.monomial(R*x/(2*K)),F.monomial(-R*x/(2*K)));
    const v=F.minus(F.monomial(R*(x-t)/(2*K)),F.monomial(-R*(x-t)/(2*K)));
    a=F.plus(a,F.scale(F.times(u,v),rat(-1n,BigInt(2*K))));
  }
  return a;
}

function canonical(x) {
  if(Array.isArray(x))return x.map(canonical);
  if(x!==null&&typeof x==="object")return Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])]));
  return x;
}
const fingerprint=x=>crypto.createHash("sha256").update(JSON.stringify(canonical(x))).digest("hex");

function packetPlan(p) {
  const w=p.packet_bits, K=p.packet_side;
  check(dyadic(K)&&2**w===K,"packet width");
  const expected={logical_qubits:2*w, clean_AND_work_qubits:w-1, known_flag_qubits:1,
    W_forward_uses:2,W_inverse_uses:1,known_zero_reflections:1,H_gates:3*w+6,
    X_gates:2*w+3,CCX_gates:2*(w-1),CP_gates:3*w+1,P_gates:w+1,logical_instructions:11*w+9};
  Object.entries(expected).forEach(([k,v])=>check(p[k]===v,"packet count "+k));
  check(p.postselection_used===false&&p.known_zero_parent_success_probability==="1"&&
    p.flag_clear_for_arbitrary_input_claimed===false&&p.hardware_synthesis_or_simulator_roundoff_certified===false,"packet scope");
  function atan(k,N) {
    const x=rat(1n,BigInt(k)), x2=mul(x,x);let term=x,sum=zero;
    for(let j=0;j<N;j++) {sum=add(sum,div(mul(term,rat(j%2?-1n:1n)),rat(BigInt(2*j+1))));term=mul(term,x2);}
    const end=add(sum,div(mul(term,rat(N%2?-1n:1n)),rat(BigInt(2*N+1))));
    return cmp(sum,end)<=0n?[sum,end]:[end,sum];
  }
  const a=atan(5,p.Machin_terms), b=atan(239,p.Machin_terms);
  const lo=sub(mul(rat(16n),a[0]),mul(rat(4n),b[1]));
  const hi=sub(mul(rat(16n),a[1]),mul(rat(4n),b[0]));
  check(cmp(lo,parse(p.pi_lower))===0n&&cmp(hi,parse(p.pi_upper))===0n,"independent Machin enclosure");
  const encoded=rat(884279719003555n,281474976710656n);
  check(cmp(encoded,parse(p.encoded_binary64_pi))===0n,"binary64 pi binding");
  const weight=sub(rat(33n,4n),rat(7n,BigInt(K)));
  const e1=sub(encoded,lo),e2=sub(encoded,hi);
  const error=cmp(rat(abs(e1[0]),e1[1]),rat(abs(e2[0]),e2[1]))>=0n?rat(abs(e1[0]),e1[1]):rat(abs(e2[0]),e2[1]);
  check(cmp(parse(p.retained_absolute_pi_weight),weight)===0n&&
    cmp(parse(p.encoded_rotation_operator_error_upper),mul(weight,error))===0n,"packet angle budget");
}

function resources(c) {
  const s=c.public_source,e=c.closed_resources,n=s.basis_rows.length,m=Math.log2(s.box),K=s.packet_side;
  check(dyadic(s.box)&&dyadic(K)&&s.coordinate<n&&s.residue>0&&s.residue<s.prime,"public parameters");
  primeCertificate(s.split_prime_certificate);
  check(s.split_prime_certificate.prime===s.prime,"split prime binding");
  const maxima=s.basis_rows.map((_,j)=>BigInt(s.box-1)*(j===s.coordinate?BigInt(s.prime):1n)+(j===s.coordinate?BigInt(s.residue):0n));
  const bounds=s.basis_rows.map((_,i)=>s.basis_rows.reduce((v,row,j)=>v+abs(BigInt(row[i]))*maxima[j],0n));
  const W=Math.max(...bounds.map(x=>(x+BigInt(K-1)).toString(2).length+1));
  const expectedQubits=1+n*m+n*W+2*W+1+Math.log2(K)+n;
  let additions=0,flips=0;
  for(let i=0;i<n;i++) {
    const values=[];
    s.basis_rows.forEach((row,j)=>{for(let h=0;h<m;h++)values.push(BigInt(row[i])*(j===s.coordinate?BigInt(s.prime):1n)*(1n<<BigInt(h)));});
    values.push(BigInt(s.residue)*BigInt(s.basis_rows[s.coordinate][i]));
    for(let x of values) {
      x=(x%(1n<<BigInt(W))+(1n<<BigInt(W)))%(1n<<BigInt(W));
      if(x) {additions++;flips+=x.toString(2).replace(/0/g,"").length;}
    }
  }
  check(e.total_source_qubits===expectedQubits&&c.compiled_qubits===expectedQubits&&
    e.constant_additions_including_uncompute===2*additions&&e.arithmetic_logical_instructions===4*flips+2*additions+n&&
    c.compiled_parent_instructions===2+n*m+2*n+4*flips+2*additions,"source resource census");
  check(e.arithmetic_width_plan.shared_signed_word_bits===W&&e.position_QFT_qubits===n*(m+1),"signed and cyclic widths");
  packetPlan(e.packet_plan);
  verifyPlan(c.QFT_angle_accounting_plan);
  const packetError=mul(rat(BigInt(n)),parse(e.packet_plan.encoded_rotation_operator_error_upper));
  const parameters=add(packetError,parse(c.QFT_angle_accounting_plan.single_use_encoded_CP_parameter_operator_error_upper));
  const total=add(packetError,parse(c.QFT_angle_accounting_plan.single_use_encoded_QFT_operator_error_upper));
  const totalError=cmp(total,rat(2n))>0n?rat(2n):total;
  check(cmp(parse(c.encoded_packet_parameter_operator_upper_per_parent),packetError)===0n&&
    cmp(parse(c.packet_and_retained_QFT_parameter_operator_upper_per_parent),parameters)===0n&&
    cmp(parse(c.packet_and_QFT_operator_upper_relative_to_ideal_full_QFT),totalError)===0n,"separate angle/truncation budgets");
  check(c.original_position_wires_reused_in_place===true&&c.mixed_colour_inverse_available===false&&
    c.full_parent_inverse_requires_localization_and_label_registers===true&&c.hardware_arithmetic_synthesis_or_roundoff_certified===false,"inverse and precision scope");
}

function inverse(B) {
  const n=B.length,A=B.map((row,i)=>row.map(x=>rat(BigInt(x))).concat(row.map((_,j)=>i===j?one:zero)));
  for(let j=0;j<n;j++) {
    const pivot=A.findIndex((row,i)=>i>=j&&row[j][0]!==0n);
    check(pivot>=j,"full-rank public basis");[A[j],A[pivot]]=[A[pivot],A[j]];
    const t=A[j][j];A[j]=A[j].map(x=>div(x,t));
    for(let i=0;i<n;i++)if(i!==j) {const t=A[i][j];A[i]=A[i].map((x,k)=>sub(x,mul(t,A[j][k])));}
  }
  return A.map(row=>row.slice(n));
}

function privateTemplate(s,ref,F,rows,audit) {
  if(!ref.QFT_is_exact) {
    check(audit.status==="APPROXIMATE_QFT_NOT_AN_EXACT_DCP_TEMPLATE"&&audit.finite_marginal_template_matches===false,"no exact-DCP transfer");
    return;
  }
  const u=audit.PRIVATE_AUDIT_ONLY_vector,Binv=inverse(s.basis_rows),n=u.length,N=s.phase_modulus,R=ref.reference_root;
  const d=u.map((_,j)=>u.reduce((v,x,i)=>add(v,mul(rat(BigInt(x)),Binv[i][j])),zero));
  check(d.every(x=>x[1]===1n),"integer private lattice coordinates");
  same(d.map(x=>Number(x[0])),audit.PRIVATE_AUDIT_ONLY_basis_coefficients,"independent basis solve");
  const h=d.map((x,i)=>Number(i===s.coordinate?(x[0]-BigInt(s.residue))/BigInt(s.prime):x[0]));
  check((d[s.coordinate][0]-BigInt(s.residue))%BigInt(s.prime)===0n,"correct private trial");
  same(h,audit.PRIVATE_AUDIT_ONLY_parent_shift,"parent displacement");
  const J=h.reduce((v,x,i)=>v+x*(2*s.box)**i,0), scalar=(J%N+N)%N;
  check(scalar===audit.PRIVATE_AUDIT_ONLY_cyclic_shift,"cyclic, not tensor, label");
  const overlap=h.reduce((v,x)=>mul(v,rat(BigInt(Math.max(0,s.box-Math.abs(x))),BigInt(s.box))),one);
  let v=u.reduce((v,x)=>F.times(v,affinity(s.packet_side,x,F,R)),F.monomial(0));v=F.scale(v,overlap);
  same(F.encode(v),audit.exact_marginal_visibility,"independent exact visibility");
  check(str(overlap)===audit.box_overlap,"finite box overlap");
  let match=true;
  rows.forEach((row,k)=>{
    const off=F.scale(F.times(v,F.monomial(-R/N*k*J)),rat(1n,BigInt(2*N)));
    const star=off.reduce((v,x,j)=>F.plus(v,F.scale(F.monomial(-j),x)),F.F());
    const diagonal=F.encode(F.scale(F.monomial(0),rat(1n,BigInt(2*N))));
    const expected=[[diagonal,F.encode(off)],[F.encode(star),diagonal]];
    match=match&&JSON.stringify(expected)===JSON.stringify(row.unnormalized_colour_density);
  });
  check(match===audit.finite_marginal_template_matches,"full finite marginal template scope");
  check(audit.status===(match?"FINITE_PRIVATE_TEMPLATE_MATCH":"ALIASES_OR_MODEL_MISMATCH"),"alias falsifier status");
}

function instrument(control) {
  resources(control.compiled_resources);
  const ref=control.exact_reference,s=ref.public_source,n=s.basis_rows.length,M=s.box,K=s.packet_side;
  same(s,control.compiled_resources.public_source,"same public compiled/reference source");
  const R=ref.reference_root,N=(2*M)**n,D=2*M**n,ell=Math.log2(N),F=field(R);
  const positions=[];
  function enumerate(a) {if(a.length===n)positions.push(a);else for(let x=0;x<M;x++)enumerate(a.concat(x));}
  enumerate([]);const parents=[0,1].flatMap(b=>positions.map(a=>[b,a]));
  same(parents,ref.parents,"complete parents, not selected preimages");
  const points=parents.map(([b,a])=>s.basis_rows.map((_,j)=>a.reduce((v,x,i)=>v+(x*(i===s.coordinate?s.prime:1)+(i===s.coordinate?b*s.residue:0))*s.basis_rows[i][j],0)));
  same(points,ref.public_points,"all public lattice points");
  const gram=points.map(x=>points.map(y=>x.reduce((v,t,i)=>F.times(v,affinity(K,t-y[i],F,R)),F.scale(F.monomial(0),rat(1n,BigInt(D))))));
  same(gram.map(row=>row.map(F.encode)),ref.complete_public_Gram,"independent full packet Gram");
  // Replay H/CP gates in descending wire order, then final bit reversal.
  function kernel(k,x) {
    const out=Array.from({length:ell},(_,j)=>(k>>(ell-1-j))&1);
    let p=0;
    for(let j=ell-1;j>=0;j--) {
      p+=R/2*((x>>j)&1)*out[j];
      for(let i=j-1;i>=Math.max(0,j-ref.QFT_cutoff);i--)p+=R/(2**(j-i+1))*out[j]*((x>>i)&1);
    }
    return F.monomial(p);
  }
  const J=a=>a.reduce((v,x,i)=>v+x*(2*M)**i,0);
  let mass=F.F();
  const rows=Array.from({length:N},(_,k)=>{
    const rho=Array.from({length:2},()=>Array.from({length:2},F.F));
    parents.forEach(([b,a],i)=>parents.forEach(([c,z],j)=>{
      const left=kernel(k,J(a)), right=kernel(k,J(z));
      // root conjugation by exact monomial inversion is implemented via coefficients.
      const star=right.reduce((v,x,t)=>F.plus(v,F.scale(F.monomial(-t),x)),F.F());
      rho[b][c]=F.plus(rho[b][c],F.scale(F.times(F.times(gram[i][j],left),star),rat(1n,BigInt(N))));
    }));
    const p=F.plus(rho[0][0],rho[1][1]);mass=F.plus(mass,p);
    return {label:k,joint_label_probability:F.encode(p),unnormalized_colour_density:rho.map(row=>row.map(F.encode))};
  });
  same(rows,ref.all_label_outcomes,"every exact conditioned label density");
  same(F.encode(mass),["1"],"complete instrument probability");
  privateTemplate(s,ref,F,rows,control.private_template_audit);
  const audit=control.actual_sampling_audit,meta=audit.metadata;
  check(meta.public_source_fingerprint===fingerprint(s)&&meta.QFT_cutoff===ref.QFT_cutoff&&
    meta.logical_readout_QFT_is_exact_reference===ref.QFT_is_exact&&
    meta.actual_compiled_source_preparations_charged===audit.public_receipts.length&&
    meta.packet_unitaries_charged===n*audit.public_receipts.length&&meta.W_calls_charged===3*n*audit.public_receipts.length&&
    meta.conditioned_snapshot_keys_and_multiplicities_checked===true&&meta.source_DCP_promise_is_not_inferred_from_samples===true,"physical source accounting");
  for(const receipt of audit.public_receipts) {
    check(receipt.measured_cells.length===0&&receipt.label>=0&&receipt.label<N&&receipt.modulus===N,"labels only, no localization");
    same(receipt.original_source_receipts,[receipt.id],"distinct root ancestry");
    const row=rows[receipt.label],p=F.value(F.decode(row.joint_label_probability))[0];
    const got=audit.PRIVATE_AUDIT_ONLY_density_matrices[receipt.id];
    row.unnormalized_colour_density.forEach((r,i)=>r.forEach((x,j)=>{
      const z=F.value(F.decode(x));
      check(Math.abs(z[0]/p-got[i][j][0])<1e-7&&Math.abs(z[1]/p-got[i][j][1])<1e-7,"sampled conditional density");
    }));
  }
  if(meta.QFT_usage_ledger!==null)check(meta.QFT_usage_ledger.charged_forward_calls===audit.public_receipts.length,"actual cutoff QFT calls paid");
  check(control.private_template_audit.correct_trial_flag_given_to_receiver===false&&
    control.private_template_audit.full_growing_reduction_certified===false,"private audit is not a trial selector");
  return audit.public_receipts.length;
}

function verify(report) {
  check(report.producer_sha256===hash(path.join(ROOT,"theorems/lattice_sine_window_source.py"))&&
    report.derivation_sha256===hash(path.join(ROOT,"research/LATTICE_SINE_WINDOW_SOURCE.md"))&&
    report.contract_sha256===hash(path.join(ROOT,"research/hypotheses/lattice_sine_window_source_contract.json")),"current provenance");
  Object.entries(report.dependency_sha256).forEach(([p,h])=>check(hash(path.join(ROOT,"theorems",p))===h,"dependency provenance"));
  check(report.actual_source_controls.length===4,"complete control set");
  let shots=report.actual_source_controls.reduce((v,c)=>v+instrument(c),0);
  shots+=instrument(report.approximate_instrument_control);
  resources(report.large_compiled_not_simulated);
  check(shots===report.charged_source_preparations&&shots===34,"all actual preparations paid");
  check(report.accepted_speedup_candidate===false&&report.hard_lattice_source_or_efficient_receiver_supplied===false&&
    report.new_active_negative_result_created===false&&report.novelty_claim===false,"no inflated result");
  return {verified:true,exact_controls:4,approximate_controls:1,source_preparations:shots,accepted_speedup_candidate:false};
}
module.exports={verify,field,affinity,instrument,resources};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||FILE,"utf8"))),null,2));
