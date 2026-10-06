"use strict";
// Native Z9 frequencies and finite differences, independent of FLINT/Python.
const fs=require("fs"),path=require("path");
const r=JSON.parse(fs.readFileSync(path.join(__dirname,"../phase_workbench/ternary_schur_tensor.json"),"utf8"));
function check(v,m){if(!v)throw Error(m);}
function mod(x,q=3){return((x%q)+q)%q;}
function close(a,b,m){check(Math.abs(a-b)<5e-12,m);}
function same(a,b,m){check(JSON.stringify(a)===JSON.stringify(b),m);}
function points(q,n){return Array.from({length:q**n},(_,i)=>Array.from({length:n},(_,j)=>Math.floor(i/q**(n-j-1))%q));}
function sum(columns,coefficients){return columns[0].map((_,i)=>mod(columns.reduce((v,c,j)=>v+c[i]*coefficients[j],0)));}
function frequencies(labels,word){return labels[0].map((_,l)=>mod(labels.reduce((v,row,i)=>v+(word[i]===0 ? 0 : word[i]===1 ? row[l][0]-2*row[l][1] : -row[l][0]-row[l][1]),0),9));}
function polynomial(row,point){return mod(row.reduce((v,t)=>v+t.coefficient*t.powers.reduce((a,e,j)=>a*point[j]**e,1),0));}
function matrixRank(columns){
  const a=columns[0].map((_,i)=>columns.map(c=>c[i]));let rank=0;
  for(let j=0;j<columns.length;j++){
    const pivot=a.findIndex((row,i)=>i>=rank && row[j]);if(pivot<0)continue;
    [a[pivot],a[rank]]=[a[rank],a[pivot]];const inverse=a[rank][j]===1 ? 1 : 2;a[rank]=a[rank].map(x=>mod(x*inverse));
    for(let i=0;i<a.length;i++)if(i!==rank){const scalar=a[i][j];a[i]=a[i].map((x,k)=>mod(x-scalar*a[rank][k]));}rank++;
  }return rank;
}
let mixedDifferences=0,sparseEvaluations=0,physicalWords=0,branchAmplitudes=0,sourceAssignments=0;
const c=r.diagonal_zero_false_admission_control,A=c.low_label_rows,V=c.physical_kernel_columns,h=V.length;
same(A,c.native_labels[0].map((_,l)=>c.native_labels.map(row=>mod(row[l][0]+row[l][1]))),"native low-label matrix");
check(matrixRank(V)===h,"dependent kernel chart");
check(V.every(v=>A.every(row=>mod(row.reduce((s,a,i)=>s+a*v[i],0))===0)),"not a native kernel");
const all=points(3,h),zero=Array(h).fill(0),baseF=frequencies(c.native_labels,sum(V,zero));
function residual(z){const values=frequencies(c.native_labels,sum(V,z));return values.map((x,l)=>{const delta=mod(x-baseF[l],9);check(delta%3===0,"non-divisible native phase");return delta/3;});}
for(const z of all){same(c.public_polynomial.component_polynomials.map(row=>polynomial(row,z)),residual(z),"sparse native polynomial");sparseEvaluations++;}
function triple(u,v,w){const p=[u,v,w].map(x=>sum(V,x));return A.map(row=>mod(-row.reduce((s,a,i)=>s+a*p[0][i]*p[1][i]*p[2][i],0)));}
for(const v of all)check(triple(v,v,v).every(x=>x===0),"characteristic-three diagonal constraint");
const basis=Array.from({length:h},(_,j)=>zero.map((_,i)=>Number(i===j)));let nonzero=0;
for(let i=0;i<h;i++)for(let j=i;j<h;j++)for(let k=j;k<h;k++){
  const directions=[basis[i],basis[j],basis[k]],expected=triple(...directions);
  for(const origin of all){
    let delta=Array(A.length).fill(0);
    for(const bits of points(2,3)){
      const z=origin.map((x,l)=>mod(x+bits.reduce((s,b,a)=>s+b*directions[a][l],0))),values=residual(z),sign=(-1)**(3-bits.reduce((s,b)=>s+b,0));
      delta=delta.map((x,l)=>mod(x+sign*values[l]));
    }same(delta,expected,"native mixed third derivative");mixedDifferences++;
  }if(expected.some(Boolean))nonzero++;
}
check(nonzero>0 && c.mixed_admission.all_diagonal_triples_zero && !c.mixed_admission.classical_quadratic_restriction_admitted,"false diagonal admission");
const large=r.polynomial_size_representation_control,largeRows=large.public_polynomial.component_polynomials;
check(!large.public_polynomial.dense_3_to_h_phase_table_built && large.public_polynomial.public_residual_evaluations===152 &&
  large.retained_width===16 && large.dense_phase_table_size_avoided==="43046721","exponential table slipped into public representation");
check(largeRows.every(row=>row.every(t=>t.powers.reduce((a,b)=>a+b,0)<=3)),"noncubic sparse output");
const largeV=large.physical_kernel_columns,largeA=large.low_label_rows;
same(largeA,large.native_labels[0].map((_,l)=>large.native_labels.map(row=>mod(row[l][0]+row[l][1]))),"large native low matrix");
check(matrixRank(largeV)===16 && largeV.every(v=>largeA.every(row=>mod(row.reduce((s,a,i)=>s+a*v[i],0))===0)),"large public kernel chart");
for(let i=0;i<10;i++){
  const z=Array.from({length:16},(_,j)=>mod(j*j+i*j+i)),freq=frequencies(large.native_labels,sum(largeV,z));
  const residual=freq.map(x=>{check(x%3===0,"large native division");return x/3;});
  same(largeRows.map(row=>polynomial(row,z)),residual,"large sparse native polynomial");sparseEvaluations++;
}
for(const c of r.all_outcome_disjoint_block_controls){
  const B=c.completed_logical_frame_columns,h=B.length,k=c.retained_quadratic_qutrits,m=c.native_qutrits_consumed,V=c.physical_kernel_columns;
  check(matrixRank(B)===h && c.restriction_admission.classical_quadratic_restriction_admitted,"noninvertible retained restriction");
  const W=c.restriction_admission.physical_frame_columns;
  check(W.every((v,i)=>W.every((w,j)=>i===j || v.every((x,l)=>!x || !w[l]))),"block supports not disjoint");
  const seen=new Set();let probability=0;
  for(const branch of c.all_initial_and_complement_outcomes){
    const y=branch.measured_initial_and_complement_syndrome.slice(0,c.initial_pivots.length),tail=branch.measured_initial_and_complement_syndrome.slice(c.initial_pivots.length);
    const values=[];
    for(const[outputIndex,z]of points(3,k).entries()){
      const logical=sum(B,[...z,...tail]),physical=Array(m).fill(0);
      c.initial_free_columns.forEach((f,j)=>{physical[f]=logical[j];});
      c.initial_pivots.forEach((p,i)=>{physical[p]=mod(y[i]-c.initial_RREF_rows[i].reduce((v,a,j)=>v+(c.initial_free_columns.includes(j) ? a*physical[j] : 0),0));});
      const wordKey=physical.join(",");check(!seen.has(wordKey),"native word reused");seen.add(wordKey);
      const freq=frequencies(c.native_labels,physical),theta=2*Math.PI*mod(freq.reduce((v,x,j)=>v+x*c.integer_secret_calibration[j],0),9)/9;
      const amplitude=[Math.cos(theta)/Math.sqrt(3**m),Math.sin(theta)/Math.sqrt(3**m)];
      amplitude.forEach((x,j)=>close(x,branch.all_unnormalized_native_amplitudes[outputIndex][j],"full native source amplitude"));
      values.push(freq);branchAmplitudes++;
    }
    same(values[0],branch.public_component_frequency_base_mod9,"branch global phase discarded");
    const residuals=values.map(v=>v.map((x,l)=>{const delta=mod(x-values[0][l],9);check(delta%3===0,"restriction lost phase divisibility");return delta/3;}));
    same(residuals,branch.public_divided_residual_table_mod3,"actual native divided phase");
    for(const[i,z]of points(3,k).entries())same(branch.quadratic_component_polynomials.map(row=>polynomial(row.coefficients,z)),residuals[i],"quadratic restricted phase");
    check(branch.quadratic_component_polynomials.every(row=>row.coefficients.every(t=>t.powers.filter(Boolean).length<=1)),"disjoint outputs entangled by cross term");
    close(branch.probability,3**(-(m-k)),"postselected complement syndrome");probability+=branch.probability;
  }
  check(seen.size===3**m,"missing native words");close(probability,1,"missing branch mass");physicalWords+=seen.size;
  check(k===Math.floor(m/(c.low_label_rows.length+1)) && !c.original_even_source_acquisition_charged &&
    !c.full_secret_top_digit_recovered && !c.generic_quadratic_packet_is_decoder,"conditional primitive exaggerated");
}
for(const c of r.quadratic_source_law_controls){
  const W=c.physical_frame_columns,k=W.length,m=W[0].length;
  const squares=W.map(w=>w.map(x=>mod(x*x))),cross=[];
  for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)cross.push(W[i].map((x,l)=>mod(x*W[j][l])));
  const d=matrixRank([...squares,...cross]),e=cross.length ? matrixRank(cross) : 0;
  check(d===c.square_Schur_rank && e===c.offdiagonal_Schur_rank && c.conditional_diagonal_label_entropy_per_component_trits===d-e,"quadratic source entropy");
  check(c.conditional_linear_label_entropy_per_component_trits===k,"linear source rank");
  const probability=c.all_component_cross_terms_cancel_probability;
  check(c.all_cross_cancellation_targets_consistent && BigInt(probability.numerator)*3n**BigInt(c.secret_components*e)===BigInt(probability.denominator),"uncharged product-state filter");
  check(m===4 && k===2 && c.secret_components===1,"source countercontrol scope");
  const diagonalCounts=new Map();let accepted=0;
  for(const high of points(3,m)){
    function Q(z){const word=sum(W,z),f=mod(word.reduce((a,j,i)=>a+(j===0 ? 0 : j===1 ? 1 : 2+3*high[i]),0),9);check(f%3===0,"source affine division");return f/3;}
    const single=[Q([1,0]),Q([0,1])],double=[Q([2,0]),Q([0,2])],mixed=mod(Q([1,1])-single[0]-single[1]);
    if(mixed===0){const key=single.map((x,j)=>mod(2*x-double[j])).join(",");diagonalCounts.set(key,(diagonalCounts.get(key)||0)+1);accepted++;}
    sourceAssignments++;
  }
  check(accepted===81/3**e && diagonalCounts.size===3**(d-e) && new Set(diagonalCounts.values()).size===1,"native high-source product law");
  check(c.conditional_product_qutrit_labels_IID_uniform===(d-e===k) && !c.cross_filter_physically_executed_here &&
    !c.arbitrary_public_Clifford_or_basis_changes_excluded && !c.correlated_quadratic_outputs_useless,"fixed-frame source became universal no-go");
}
check(Object.values(r.claim_gate).every(x=>x===false),"candidate promoted");
console.log(JSON.stringify({status:"independent_replay_passed",mixed_native_differences:mixedDifferences,
  sparse_polynomial_values:sparseEvaluations,all_native_words:physicalWords,complex_branch_amplitudes:branchAmplitudes,
  exhaustive_native_high_source_assignments:sourceAssignments,new_algorithm:false}));
