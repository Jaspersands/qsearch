"use strict";

// Exact bounded clean channel and domination; baseline MAP replay is numerical.
const fs=require("fs"),path=require("path");
const {check,same,rat,mod,field,sign}=require("./cyclotomic_exact");
const out=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../phase_workbench/native_echo_history_receiver.json"),"utf8"));
const near=(a,b,msg)=>check(Number.isFinite(a)&&Math.abs(a-b)<3e-10,msg);
check(out.status==="NATIVE_MULTIROUND_ECHO_HISTORY_RECEIVER_REVIEW_PENDING","review-pending original-source control");
for(const name of ["new_speedup_claimed","novelty_claimed","candidate_accepted"])check(out[name]===false,"no promotion from finite scores");
for(const name of ["contraction_exponent_is_mediator_width_TIMES_echo_rounds","fast_conditional_likelihood_is_NOT_unknown_secret_inference","one_echo_obstruction_does_NOT_cover_multiple_rounds"])check(out[name]===true,"cost and scope guards");
check(out.cohorts.length===12&&out.exact_checker_control.source_seed===61910,"whole controls");
const control=out.exact_checker_control,K=field(9);
check(control.records.length===10,"complete control policies");
const scale=(a,n,d=1)=>K.scale(a,rat(BigInt(n),BigInt(d))),sub=(a,b)=>K.plus(a,scale(b,-1));
const sum=a=>a.reduce(K.plus,K.F()),square=a=>K.times(a,K.conj(a));
const root=e=>K.powers[mod(e,9)];
const number=a=>a.reduce((v,x,i)=>v+Number(x[0])/Number(x[1])*Math.cos(2*Math.PI*i/9),0);
const words=m=>m?words(m-1).flatMap(w=>[0,1,2].map(j=>[...w,j])):[[]];
const all=words(3),A=words(2),histories=words(3);
function fourier(v,wire){
  return all.map(w=>sum([0,1,2].map(j=>{const x=[...w];x[wire]=j;const index=x.reduce((s,z)=>3*s+z,0);return K.times(root(-3*w[wire]*j),v[index]);})));
}
let exactProbabilities=0,exactWinnerChecks=0,exactDominationChecks=0;
for(const r of control.records){
  const publicSchedule=r.schedule,f=publicSchedule.source,Ks=publicSchedule.round_couplings;
  check(f.modulus===9&&f.mediator_width===1&&f.first_frequencies.length===3&&f.first_frequencies.every(x=>x.length===1),"q9 n1 three-copy control");
  check(Ks.length===3&&Ks.every(x=>x.length===1&&x[0].length===1),"three real rounds");
  same(f.first_frequencies,control.records[0].schedule.source.first_frequencies,"same original first labels");
  same(f.second_frequencies,control.records[0].schedule.source.second_frequencies,"same original second labels");
  const ledger=publicSchedule.recipe;
  check(ledger.original_native_source_copies===3&&ledger.echo_rounds===3&&ledger.mediator_history_count===27,"copies and history exponent");
  check(ledger.frequency_scratch_cleared_before_EVERY_mediator_Fourier===true&&ledger.same_batch_is_evolved_NOT_reprepared===true&&ledger.initial_local_settings_applied_once===true,"physical source and clean scratch");
  check(ledger.has_single_echo_architecture===false&&ledger.A_independence_of_coupling_is_NOT_inferred_from_schedule===true,"no false one-echo gate");
  for(const name of ["unknown_source_preparation_inverse_used","fiber_count_rank_unrank_oracle_used","source_states_reused_or_cloned"])check(ledger[name]===false,"no stronger source oracle");
  const values=i=>[0,f.first_frequencies[i][0],f.second_frequencies[i][0]];
  const eta=i=>[0,...f.local_settings[i]];
  const frequency=w=>w.reduce((v,j,i)=>v+values(i)[j],0);
  const setting=w=>w.reduce((v,j,i)=>v+eta(i)[j],0);
  const P=[];
  for(let s=0;s<9;s++){
    let v=all.map(w=>root(s*frequency(w)-setting(w)));
    for(const matrix of Ks){
      const k=matrix[0][0];
      const chirp=w=>k*(values(0)[w[0]]+values(1)[w[1]])*values(2)[w[2]];
      v=v.map((x,i)=>K.times(root(chirp(all[i])),x));
      v=fourier(fourier(v,0),1);
      v=v.map((x,i)=>K.times(root(-chirp(all[i])),x));
      v=fourier(v,2);
    }
    P.push(v.map(x=>scale(square(x),1,3**12)));
    check(K.eq(sum(P[s]),K.unit),"exact three-round clean normalization");exactProbabilities+=27;
  }
  const winner=r.score.full_secret_MAP_winner_indices_by_outcome;
  check(winner.length===27&&r.score.full_secret_count===9&&r.score.decoder_secret_hypotheses_enumerated===9,"complete exponential decoder reference");
  for(const name of ["efficient_unknown_secret_decoder_supplied","ideal_PGM_circuit_supplied"])check(r.score[name]===false,"no efficient decoder grant");
  let full=K.F();
  winner.forEach((s,j)=>{
    check(Number.isInteger(s)&&s>=0&&s<9,"valid winner");
    for(let t=0;t<9;t++){check(sign(K,sub(P[s][j],P[t][j]))>=0,"exact clean MAP comparison");exactWinnerChecks++;}
    full=K.plus(full,P[s][j]);
  });
  full=scale(full,1,9);
  const tritColumns=[0,1,2].map(t=>all.map((_,j)=>sum(P.filter((_,s)=>s%3===t).map(row=>row[j]))));
  const trit=scale(sum(all.map((_,j)=>tritColumns.map(row=>row[j]).reduce((a,b)=>sign(K,sub(a,b))>=0?a:b))),1,9);
  near(r.score.full_uniform_secret_MAP_success_numeric_reference,number(full),"exact clean full MAP");
  near(r.score.least_trit_MAP_success_numeric_reference,number(trit),"exact clean trit MAP");
  const dirtyA=Array.from({length:9},()=>A.map(()=>K.F()));
  const PB=Array.from({length:9},(_,s)=>[0,1,2].map(b=>number(scale(square(sum([0,1,2].map(y=>root(s*values(2)[y]-eta(2)[y]-3*b*y)))),1,9))));
  let baselineFull=0,baselineTrit=0;
  for(const history of histories){
    const PA=[];
    for(let s=0;s<9;s++){
      const locals=[0,1].map(i=>{
        let v=values(i).map((z,j)=>root(s*z-eta(i)[j]));
        for(let d=0;d<3;d++){
          const delta=Ks[d][0][0]*values(2)[history[d]],before=v;
          v=[0,1,2].map(j=>sum([0,1,2].map(l=>K.times(root(delta*(values(i)[l]-values(i)[j])-3*j*l),before[l]))));
        }
        return v.map(x=>scale(square(x),1,3**4));
      });
      PA.push(A.map(a=>K.times(locals[0][a[0]],locals[1][a[1]])));
      check(K.eq(sum(PA[s]),K.unit),"exact local path normalization");
      PA[s].forEach((p,j)=>dirtyA[s][j]=K.plus(dirtyA[s][j],scale(p,1,27)));
    }
    for(let a=0;a<9;a++)for(let b=0;b<3;b++){
      const column=PA.map((row,s)=>number(row[a])*PB[s][b]/27);
      baselineFull+=Math.max(...column)/9;
      baselineTrit+=Math.max(...[0,1,2].map(t=>column.reduce((v,p,s)=>v+(s%3===t?p:0),0)))/9;
    }
  }
  for(let s=0;s<9;s++)for(let j=0;j<27;j++){
    const dirty=scale(dirtyA[s][Math.floor(j/3)],1,3);
    check(sign(K,sub(scale(dirty,27),P[s][j]))>=0,"exact coherent-history Cauchy domination");exactDominationChecks++;
  }
  const baseline=r.matched_history_LOCC;
  check(baseline.complete_histories_enumerated===27&&baseline.pointwise_coherent_to_dephased_domination_factor===27&&baseline.same_original_native_copies===3,"matched resource accounting");
  check(baseline.single_copy_quantum_gates_only===true&&baseline.classical_simulation_without_unknown_input_states_claimed===false&&baseline.efficient_unknown_secret_decoder_supplied===false,"LOCC not unknown-input classical simulation");
  near(baseline.full_uniform_secret_MAP_success_numeric_reference,baselineFull,"independent numerical MAP on exact baseline laws");
  near(baseline.least_trit_MAP_success_numeric_reference,baselineTrit,"independent numerical trit MAP on exact baseline laws");
  near(r.full_MAP_minus_OWN_LOCC,number(full)-baselineFull,"matched full MAP difference");
  near(r.least_trit_MAP_minus_OWN_LOCC,number(trit)-baselineTrit,"matched trit MAP difference");
}
console.log(JSON.stringify({status:"PASS",exactProbabilities,exactWinnerChecks,exactDominationChecks,baseline_MAP_scores:"numerical replay from exact local path probabilities",scope:"bounded original-source controls, not scaling or an efficient decoder"}));
