"use strict";
// Independent complete dyadic instrument from PUBLIC lattice inputs.
const fs=require("fs"),path=require("path"),crypto=require("crypto"),E=require("./cyclotomic_exact.js");
const {check,rat,str,add,zero}=E,ROOT=path.resolve(__dirname,"../..");
const REPORT=path.join(ROOT,"research/phase_workbench/lattice_cube_dcp_readout.json");
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const same=(a,b,m)=>E.same(canonical(a),canonical(b),m),mod=(x,q)=>(x%q+q)%q;
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
function* tuples(M,n,p=[]){if(!n){yield p;return;}for(let x=0;x<M;x++)yield*tuples(M,n-1,[...p,x]);}
const encode=(a,M)=>a.reduce((s,x,i)=>s+x*(2*M)**i,0);
function polynomial(C,N){const c=C.slice(0,N/2);for(let i=N/2;i<N;i++)c[i-N/2]=E.sub(c[i-N/2],C[i]);while(c.length&&!c[c.length-1][0])c.pop();return c.reverse().map(str);}
function value(P,N){let re=0,im=0;P.slice().reverse().forEach((s,i)=>{const q=E.parse(s),x=Number(q[0])/Number(q[1]);re+=x*Math.cos(2*Math.PI*i/N);im+=x*Math.sin(2*Math.PI*i/N);});return [re,im];}
function resources(R){
  const C=R.clean_evaluator,S=C.public_source,B=S.basis_rows,n=B.length,M=S.box,W=S.cube_width,p=S.prime,m=S.residue_guess,i0=S.coordinate;
  const b=Math.log2(M),k=Math.log2(W),maxima=Array(n).fill(M-1);maxima[i0]=p*(M-1)+m;
  const widths=B.map((_,i)=>{const bound=B.reduce((s,row,j)=>s+Math.abs(row[i])*maxima[j],0)+W;
    const bits=Math.max(BigInt(bound).toString(2).length+1,k+1);return {absolute_point_minus_offset_bound:bound,signed_point_workspace_bits:bits,
      low_remainder_bits_to_uncompute:k,signed_cell_output_bits:bits-k,strict_signed_range_certified:bound<2**(bits-1)};});
  const w=Math.max(...widths.map(x=>x.signed_point_workspace_bits)),ell=n*(b+1),out=widths.reduce((s,x)=>s+x.signed_cell_output_bits,0);
  check(R.position_qubits===ell&&R.zero_padding_qubits===n&&R.phase_modulus===(2*M)**n,"in-place position dimensions");
  check(R.original_position_wires_reused_in_place===true&&R.copied_original_position_garbage_retained===false,"no copied position garbage");
  check(C.compiled_qubits===1+n*b+out+2*w+1&&R.compiled_phase_parent_qubits===C.compiled_qubits+n,"all logical workspace charged");
  same(C.width_certificate.coordinate_width_certificates,widths,"signed point widths");
  check(C.input_qubits===1+n*b&&C.cell_output_qubits===out&&C.shared_arithmetic_workspace_qubits===2*w+1,"source register dimensions");
  let additions=0,instructions=0;
  const term=x=>{x=mod(x,2**w);if(x){additions++;instructions+=2*x.toString(2).split("1").length-1;}};
  for(let i=0;i<n;i++){
    for(let j=0;j<n;j++)for(let h=0;h<b;h++)term((j===i0?p:1)*B[j][i]*2**h);
    term(m*B[i0][i]);term(-S.offsets[i]);
  }
  check(C.constant_additions_including_uncompute===2*additions&&C.logical_instruction_count===2*instructions+out,"actual constant additions and copies charged");
  check(R.logical_QFT_H_gates===ell&&R.logical_QFT_controlled_phase_gates===ell*(ell-1)/2&&R.logical_QFT_swap_gates===Math.floor(ell/2),"full positive QFT resources");
  check(R.public_cell_and_label_measured_colour_qubit_retained===true&&R.hidden_shift_or_preimages_enter_compiler===false&&R.hardware_or_fault_tolerant_QFT_precision_certified===false,"compiled readout scope");
  return S;
}
function instrument(S){
  const B=S.basis_rows,n=B.length,M=S.box,W=S.cube_width,D=2*M**n,N=(2*M)**n;
  check(N<=32&&D*N<=16384,"complete finite reference cap");
  const fibres=new Map();
  for(let t=0;t<2;t++)for(const a of tuples(M,n)){
    const coefficients=a.slice();coefficients[S.coordinate]=S.prime*a[S.coordinate]+t*S.residue_guess;
    const cell=Array.from({length:n},(_,i)=>Math.floor((coefficients.reduce((s,c,j)=>s+c*B[j][i],0)-S.offsets[i])/W));
    const key=cell.join(",");if(!fibres.has(key))fibres.set(key,{cell,points:[]});fibres.get(key).points.push([t,a]);
  }
  const sorted=[...fibres.values()].sort((a,b)=>{for(let i=0;i<n;i++)if(a.cell[i]!==b.cell[i])return a.cell[i]-b.cell[i];return 0;});
  const all=[],labels=Array.from({length:N},()=>Array.from({length:N},()=>zero));
  for(const f of sorted)for(let k=0;k<N;k++){
    const trace=Array.from({length:N},()=>zero),matrix=[];
    for(let t=0;t<2;t++){
      const row=[];
      for(let u=0;u<2;u++){
        const c=Array.from({length:N},()=>zero);
        for(const [colour,a] of f.points)if(colour===t)for(const [other,b] of f.points)if(other===u){
          const exp=mod(k*(encode(a,M)-encode(b,M)),N);c[exp]=add(c[exp],rat(1n,BigInt(D*N)));
        }
        if(t===u)for(let i=0;i<N;i++)trace[i]=add(trace[i],c[i]);
        row.push(polynomial(c,N));
      }
      matrix.push(row);
    }
    for(let i=0;i<N;i++)labels[k][i]=add(labels[k][i],trace[i]);
    all.push({cell:f.cell,label:k,unnormalized_colour_density:matrix,joint_Born_probability:polynomial(trace,N)});
  }
  const probabilities=labels.map(c=>polynomial(c,N)),uniform=probabilities.every(p=>JSON.stringify(p)===JSON.stringify([str(rat(1n,BigInt(N)))]));
  let bad=0,valid=true,common=new Set(),good=0;const colours=[0,0],sizes=new Map();
  for(const f of sorted){const points=f.points;sizes.set(points.length,(sizes.get(points.length)||0)+1);
    if(points.length>2||new Set(points.map(([t])=>t)).size!==points.length)valid=false;
    if(points.length===1){bad++;colours[points[0][0]]++;}
    if(points.length===2&&points[0][0]!==points[1][0]){good++;const a=points.find(([t])=>t===0)[1],b=points.find(([t])=>t===1)[1];common.add(b.map((x,i)=>x-a[i]).join(","));}
  }
  valid=valid&&common.size<=1;
  return {N,D,all,probabilities,uniform,valid,bad,good,colours,sizes,fibres:sorted};
}
function checkControl(C){
  const S=resources(C.compiled_resources),ref=C.exact_Born_reference,X=instrument(S);
  same(ref.all_cell_label_outcomes,X.all,"every exact weighted colour-density entry");
  same(ref.all_label_Born_probabilities,X.probabilities,"complete label Born law");
  check(ref.modulus===X.N&&ref.input_population===X.D&&ref.label_distribution_uniform===X.uniform,"reference dimensions and uniformity not assumed");
  check(ref.preimages_are_private_reference_data_not_emitter_advice===true,"private census access");
  const shape=ref.full_domain_source_shape_audit;
  same(shape.public_source,S,"shape audit binds public source");
  check(shape.complete_original_domain_censused===X.D&&shape.measured_cell_count===X.fibres.length&&shape.valid_two_point_source_on_full_domain===X.valid,"source-shape census");
  same(shape.fibre_size_histogram,[...X.sizes].sort((a,b)=>a[0]-b[0]).map(([s,c])=>({size:s,cells:c,Born_mass:str(rat(BigInt(s*c),BigInt(X.D)))})),"Born cell weights");
  check(shape.bad_register_rate===(X.valid?str(rat(BigInt(X.bad),BigInt(X.D))):null)&&shape.good_two_point_Born_mass===str(rat(BigInt(2*X.good),BigInt(X.D))),"actual bad/good rates");
  same(shape.PRIVATE_AUDIT_ONLY_singleton_colour_counts,X.colours,"balanced singleton census");
  const A=C.compiled_source_sampling_audit,M=A.simulation_metadata,receipts=A.public_receipts,matrices=A.PRIVATE_AUDIT_ONLY_emitted_density_matrices;
  check(receipts.length===24&&M.actual_compiled_source_preparations_charged===24&&M.source_function_evaluations_charged===24&&M.original_receipts_emitted===24,"every source preparation charged");
  check(M.conditioned_snapshot_key_and_count_checks_passed===true&&M.public_Z_frame_snapshot_then_correction_used===true,"conditioned snapshot guard");
  check(M.MPS_truncation_threshold===0&&M.floating_point_density_tolerance===1e-7&&M.numerical_error_is_a_formally_certified_channel_bound===false&&M.hidden_shift_or_preimages_supplied_to_sampler===false&&M.source_shots_independent_given_public_parameters===true,"numerical and actual access model scope");
  check(M.public_source_function_fingerprint===crypto.createHash("sha256").update(JSON.stringify(canonical(S))).digest("hex"),"source provenance fingerprint");
  const table=new Map(X.all.map(r=>[r.cell.join(",")+":"+r.label,r]));let maxError=0;const ids=new Set();
  receipts.forEach(r=>{
    same(Object.keys(r).sort(),["id","modulus","label","measured_cells","original_source_receipts","merge_depth"].sort(),"public receipt has no private phase or clean flag");
    check(!ids.has(r.id)&&r.modulus===X.N&&r.merge_depth===0,"fresh original receipt");ids.add(r.id);
    same(r.original_source_receipts,[r.id],"single original source ancestry");
    const row=table.get(r.measured_cells[0].join(",")+":"+r.label);check(row,"observed source cell/label exists");
    const p=value(row.joint_Born_probability,X.N);check(Math.abs(p[1])<1e-12&&p[0]>1e-7,"nonzero resolved measured branch");
    const density=matrices[r.id];check(density&&density.length===2&&density.every(x=>x.length===2),"private density shape");
    for(let t=0;t<2;t++)for(let u=0;u<2;u++){
      const z=value(row.unnormalized_colour_density[t][u],X.N),actual=density[t][u];
      check(actual.length===2&&actual.every(Number.isFinite),"finite density value");
      const error=Math.hypot(z[0]/p[0]-actual[0],z[1]/p[0]-actual[1]);maxError=Math.max(maxError,error);
    }
  });
  same(Object.keys(matrices).sort(),[...ids].sort(),"no uncharged private states");
  check(maxError<=1e-7&&Math.abs(maxError-A.private_audit_max_conditional_density_error)<1e-10&&A.exact_reference_agrees_for_every_emitted_register===true,"each numerical emitted qubit vs exact instrument");
  const budget=rat(1n,BigInt(Math.log2(X.N))),met=X.valid&&E.cmp(rat(BigInt(X.bad),BigInt(X.D)),budget)<=0n;
  check(A.numerical_f1_bad_register_budget===str(budget)&&A.finite_f1_bad_register_budget_met===met&&A.full_Regev_growing_family_reduction_certified===false,"shape, finite budget and full theorem scope are distinct");
  return X.all.length;
}
function verify(R){
  check(R.status==="PUBLIC_LATTICE_TO_DCP_PHASE_CIRCUIT_AND_OPAQUE_NOISY_REGISTERS_REVIEW_PENDING","review-pending status");
  [["producer_sha256","theorems/lattice_cube_dcp_readout.py"],["derivation_sha256","research/LATTICE_CUBE_DCP_READOUT.md"],["contract_sha256","research/hypotheses/lattice_cube_dcp_readout_contract.json"]].forEach(([k,f])=>check(R[k]===hash(path.join(ROOT,f)),"provenance "+k));
  const deps=["lattice_cube_coset_source.py","lattice_cube_source_circuit.py","lattice_qft_precision.py"];
  same(Object.keys(R.dependency_sha256).sort(),deps,"direct scientific dependencies");deps.forEach(f=>check(R.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(R.actual_lattice_source_controls.length===5,"five actual compiled source controls");
  const outcomes=R.actual_lattice_source_controls.reduce((n,c)=>n+checkControl(c),0);
  resources(R.large_compiled_not_simulated_phase_source);check(R.large_compiled_not_simulated_phase_source.compiled_phase_parent_qubits===127,"large source compiled, not simulated");
  check(R.source_preparations_in_finite_calibration===120,"total actual source preparations");
  ["accepted_speedup_candidate","efficient_noisy_DCP_decoder_supplied","new_active_negative_result_created","novelty_claim"].forEach(k=>check(R[k]===false,"no unproved result "+k));
  return {verified:true,actual_compiled_source_controls:5,exact_cell_label_outcomes:outcomes,charged_source_preparations:120,accepted_speedup_candidate:false};
}
module.exports={verify,instrument,resources};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT,"utf8"))),null,2));
