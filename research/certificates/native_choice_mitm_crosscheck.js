"use strict";
// Exact ring MITM replay, not a native-source distribution theorem.
const {check,same}=require("./cyclotomic_exact.js");
const mod=(x,q)=>(x%q+q)%q;
const tuples=t=>t?tuples(t-1).flatMap(a=>[0,1,2].map(x=>[...a,x])):[[]];
function replay(choices,target,q,R) {
  q=BigInt(q);const n=target.length,t=choices.length,left=Math.floor(t/2),lc=3n**BigInt(left),rc=3n**BigInt(t-left),cost=R.cost,bits=q.toString(2).length;
  check(q>=3n&&n>0,"valid exact ring target");let root=q;while(root%3n===0n&&root>1n)root/=3n;check(root===1n,"ternary remaining root");
  check(target.every(x=>BigInt(x)>=0n&&BigInt(x)<q)&&choices.every(c=>c.length===3&&c.every(v=>v.length===n&&v.every(x=>BigInt(x)>=0n&&BigInt(x)<q))&&c[0].every(x=>BigInt(x)===0n)),"canonical three-choice ring data");
  check(Number.isSafeInteger(cost.max_evaluations)&&cost.max_evaluations>0&&Number.isSafeInteger(cost.max_entries)&&cost.max_entries>0,"charged search caps");
  same(cost,{left_assignment_bound:String(lc),right_assignment_bound:String(rc),whole_search_assignment_bound:String(lc+rc),left_memory_entry_bound:String(lc),max_evaluations:cost.max_evaluations,max_entries:cost.max_entries,group_modulus:String(q),group_dimension:n,parameters:t,residue_bits:bits,left_payload_bits_upper:String(lc*BigInt(n*bits+2*left)),payload_bound_includes_runtime_object_overhead:false,per_assignment_modular_additions_upper:n*Math.max(left,t-left),search_is_exponential_in_slice_parameters:true,uniform_solution_sampler:false,source_values_mask_secret_or_errors_used:false},"all exact ring work and payload charges");
  if(lc+rc>BigInt(cost.max_evaluations)||lc>BigInt(cost.max_entries)) {
    check(R.parameters===null&&R.assignments_evaluated===0&&R.stored_entries===0&&R.status==="SEARCH_CAP_EXCEEDED_NOT_NO_SOLUTION","capped is not no solution");return null;
  }
  check(lc+rc<=1000000n,"independent checker finite replay cap; not a solver impossibility");
  const sum=(z,offset)=>Array.from({length:n},(_,i)=>mod(z.reduce((a,v,j)=>a+BigInt(choices[offset+j][v][i]),0n),q));
  const table=new Map();let count=0,answer=null;
  for(const z of tuples(left)){const key=sum(z,0).map(String).join(",");if(!table.has(key))table.set(key,z);count++;}
  for(const z of tuples(t-left)){const other=sum(z,left),key=target.map((x,i)=>String(mod(BigInt(x)-other[i],q))).join(",");count++;if(table.has(key)){answer=[...table.get(key),...z];break;}}
  check(R.assignments_evaluated===count&&R.stored_entries===table.size,"actual work and hash table entries");same(R.parameters,answer,"actual first MITM witness or complete restricted failure");
  if(answer)check(sum(answer,0).every((x,i)=>x===BigInt(target[i])),"entire ring target matched");
  return answer;
}
module.exports={replay};
