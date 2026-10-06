"use strict";
// Direct reduced monomials / independent batch rank and native trace replay.
const fs=require("fs"),path=require("path");
const report=JSON.parse(fs.readFileSync(path.join(__dirname,"../phase_workbench/ternary_schur_closure.json"),"utf8"));
function check(v,m){if(!v)throw Error(m);}
function same(a,b,m){check(JSON.stringify(a)===JSON.stringify(b),m);}
function mod(x,q=3){return((x%q)+q)%q;}
function dot(a,b){return mod(a.reduce((s,x,i)=>s+x*b[i],0));}
function points(n){return Array.from({length:3**n},(_,i)=>Array.from({length:n},(_,j)=>Math.floor(i/3**(n-j-1))%3));}
function rank(rows){
  if(!rows.length)return 0;
  const a=rows.map(x=>x.slice());let r=0;
  for(let j=0;j<a[0].length && r<a.length;j++){
    const p=a.findIndex((row,i)=>i>=r && row[j]);if(p<0)continue;
    [a[r],a[p]]=[a[p],a[r]];const inverse=a[r][j];a[r]=a[r].map(x=>mod(inverse*x));
    for(let i=0;i<a.length;i++)if(i!==r && a[i][j]){const c=a[i][j];a[i]=a[i].map((x,t)=>mod(x-c*a[r][t]));}
    r++;
  }return r;
}
function monomials(W,d){
  return points(W.length).filter(e=>{const degree=e.reduce((a,b)=>a+b,0);return degree>0 && degree<=d && degree%2===d%2;})
    .map(e=>W[0].map((_,i)=>mod(e.reduce((s,x,j)=>s*W[j][i]**x,1))));
}
function triples(W){
  const words=[];for(let i=0;i<W.length;i++)for(let j=i;j<W.length;j++)for(let k=j;k<W.length;k++)words.push(W[0].map((_,a)=>mod(W[i][a]*W[j][a]*W[k][a])));return words;
}
function beta(L){let u=2,v=-1;for(let i=1;i<L;i++)[u,v]=[-2*u-v,u-v];const a=3**Math.floor(L/2);return[u/a,v/a];}
function local(y,L){const [u,v]=beta(L),q=3**Math.ceil(L/2);return[0,mod(u*y[0]+v*y[1],q),mod((u+v)*y[0]-u*y[1],q)];}
let classesChecked=0,monomialWords=0,nativeWitnessComponents=0,refinementWords=0,sourceMatrices=0;
const controls=report.evaluation_code_countercontrol.level_controls.map(c=>[c,report.evaluation_code_countercontrol.native_labels]);
controls.push([report.overlapping_disjoint_refinement_control.restriction,report.overlapping_disjoint_refinement_control.native_labels]);
controls.push([report.growing_width_native_countercontrol.restriction,report.growing_width_native_countercontrol.native_labels]);
for(const[c,labels]of controls){
  const W=c.physical_frame_columns,A=c.native_low_rows,k=W.length,m=W[0].length,L=c.odd_degree,geometry=c.projective_geometry;
  same(A,Array.from({length:labels[0].length},(_,l)=>labels.map(row=>mod(row[l][0]+row[l][1]))),"not the original native low labels");
  check(W.every(w=>A.every(a=>dot(a,w)===0)),"frame outside low kernel");
  const groups=new Map(),zeros=[];
  for(let i=0;i<m;i++){
    const row=W.map(w=>w[i]),sign=row.find(x=>x!==0);if(sign===undefined){zeros.push(i);continue;}
    const rep=row.map(x=>mod(sign*x)),key=JSON.stringify(rep);if(!groups.has(key))groups.set(key,{rep,word:Array(m).fill(0),support:[]});
    groups.get(key).word[i]=sign;groups.get(key).support.push(i);
  }
  same(geometry.zero_row_coordinates,zeros,"zero coordinates");check(geometry.projective_length===groups.size,"projective length");
  const sorted=Array.from(groups.values()).sort((a,b)=>JSON.stringify(a.rep).localeCompare(JSON.stringify(b.rep)));
  sorted.forEach((g,i)=>{same(geometry.classes[i].representative,g.rep,"projective representative");same(geometry.classes[i].signed_block_word,g.word,"signed block");same(geometry.classes[i].support,g.support,"disjoint support");classesChecked++;});
  const blockImages=sorted.map(g=>A.map(a=>dot(a,g.word)));same(c.signed_block_component_images,blockImages,"weighted class sums");
  const stable=blockImages.every(v=>v.every(x=>x===0));check(c.all_odd_powers_admitted===stable,"stable admission");
  const words=k<=3 ? monomials(W,L) : triples(W);monomialWords+=words.length;
  const dimension=rank(words);check(dimension===c.power_dimension,"higher Schur rank");
  check(c.higher_Schur_admission===words.every(w=>A.every(a=>dot(a,w)===0)),"all mixed admission");
  check(c.odd_power_saturated===(dimension===groups.size),"premature saturation");
  if(k>3)check(dimension===groups.size && L>=3,"large-width rank does not justify stable odd extension");
  if(c.odd_power_saturated)check(c.higher_Schur_admission===stable,"stable admission equivalence");
  const witness=c.mixed_failure_witness;
  if(witness){
    const factors=witness.basis_factor_indices;check(factors.length===L,"wrong witness order");
    const word=W[0].map((_,i)=>mod(factors.reduce((s,j)=>s*W[j][i],1)));same(witness.physical_product_word,word,"mixed witness word");
    const values=A.map(a=>dot(a,word));same(witness.weighted_component_values_mod3,values,"weighted witness");check(values.some(x=>x!==0),"zero falsifier");
    const q=3**Math.ceil(L/2),actual=labels[0].map((_,l)=>{
      let total=0;
      for(let i=0;i<m;i++){
        let table=local(labels[i][l],L);
        for(const j of factors){const direction=W[j][i];table=table.map((x,a)=>mod(table[(a+direction)%3]-x,q));}
        total+=table[0];
      }
      const value=mod(total,q);check(value%3===0,"native division");return value/3;
    });
    same(c.native_top_derivative_of_failure_witness,actual,"native exact falsifier");nativeWitnessComponents+=actual.length;
  }else check(c.native_top_derivative_of_failure_witness===null && c.higher_Schur_admission,"missing witness");
  const refinement=c.disjoint_kernel_refinement;check(refinement.certified===stable,"refinement certificate");
  if(stable){
    same(refinement.signed_blocks,sorted.map(g=>g.word),"refinement blocks");check(refinement.dimension===groups.size,"refinement dimension");
    for(let j=0;j<k;j++)same(W[j],W[0].map((_,i)=>mod(sorted.reduce((s,g)=>s+g.rep[j]*g.word[i],0))),"original frame not contained in refinement");refinementWords+=groups.size;
  }
  const probability=c.fixed_frame_reference_probability;
  check(BigInt(probability.unconditional_admission_probability_denominator)===3n**BigInt(A.length*dimension) &&
    BigInt(probability.conditional_on_AW_zero_probability_denominator)===3n**BigInt(A.length*(dimension-k)),"fixed-frame probability");
  check(!c.fixed_frame_probability_applicable_to_this_source_adaptive_kernel_frame && probability.invalid_after_source_adaptive_frame_selection,"adaptive rarity claim");
  check(!c.secret_decoder_or_generic_no_go && c.top_admission_only_not_constant_degree_or_decoder && !c.source_acquisition_or_full_instrument_charged,"decoder promoted");
}
for(const n of [1,2]){
  let kernel=0,power=0;const W=[[2,1,0],[2,0,1]],words=monomials(W,3);
  for(const flat of points(3*n)){
    const A=Array.from({length:n},(_,i)=>flat.slice(3*i,3*i+3));
    kernel+=W.every(w=>A.every(a=>dot(a,w)===0));power+=words.every(w=>A.every(a=>dot(a,w)===0));sourceMatrices++;
  }
  check(power===1 && kernel===3**n,"conditional fixed-frame source mass");
}
check(Object.values(report.claim_gate).every(v=>v===false),"candidate promotion");
console.log(JSON.stringify({status:"independent_replay_passed",projective_classes:classesChecked,
  direct_monomial_words:monomialWords,native_witness_components:nativeWitnessComponents,
  disjoint_refinement_words:refinementWords,exhaustive_low_source_matrices:sourceMatrices,new_algorithm:false}));
