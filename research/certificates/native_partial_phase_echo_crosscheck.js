"use strict";

// Bounded original-source control, not an efficient decoder or scaling proof.
const fs=require("fs"),path=require("path");
const {check,same,rat,mod,field,sign}=require("./cyclotomic_exact");
const out=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../phase_workbench/native_partial_phase_echo.json"),"utf8"));
const near=(a,b,msg)=>check(Number.isFinite(a)&&Math.abs(a-b)<2e-10,msg);
check(out.status==="NATIVE_PARTIAL_FREQUENCY_PHASE_ECHO_CONSTRUCTIVE_RECEIVER_REVIEW_PENDING","review-pending receiver status");
for(const k of ["polynomial_secret_search_follows_from_fast_likelihood","source_creation_inverse_or_fiber_oracle_supplied","new_algorithmic_speedup_claimed","novelty_claimed"])check(out[k]===false,"no oracle, efficient search or speedup grant");
check(out.cohort_controls.length===12,"complete numeric cohort list");
const control=out.exact_checker_control;
check(control.source_seed===58122&&control.receiver_records.length===8,"fixed complete exact control");
same(control.receiver_records.map(r=>[r.basis_policy,r.receiver_policy]),["fixed","phase_randomized"].flatMap(b=>["product","positive_echo","negative_echo","A_preconditioned_echo"].map(p=>[b,p])),"all predeclared policies");
const K=field(9),scale=(a,n,d=1)=>K.scale(a,rat(BigInt(n),BigInt(d)));
const sub=(a,b)=>K.plus(a,scale(b,-1));
const number=a=>a.reduce((s,x,i)=>s+Number(x[0])/Number(x[1])*Math.cos(2*Math.PI*i/9),0);
const square=a=>K.times(a,K.conj(a));
function words(m){return m?words(m-1).flatMap(w=>[0,1,2].map(j=>[...w,j])):[[]];}
function rootSum(exponents){const counts=Array(9).fill(0);for(const e of exponents)counts[mod(e,9)]++;return counts.reduce((a,c,i)=>K.plus(a,scale(K.powers[i],c)),K.F());}
const max=column=>column.reduce((best,p)=>sign(K,sub(p,best))>0?p:best,K.F());
const sum=a=>a.reduce(K.plus,K.F());
function score(P){return scale(sum(P[0].map((_,j)=>max(P.map(row=>row[j])))),1,9);}
function tritScore(P){return score([0,1,2].map(t=>P[0].map((_,j)=>sum(P.filter((_,s)=>s%3===t).map(row=>row[j])))));}
let exactProbabilities=0,exactWinnerChecks=0,dominationChecks=0;
for(const r of control.receiver_records){
  const f=r.family;
  check(f.modulus===9&&f.mediator_width===1&&f.first_frequencies.length===3,"actual q9 dimension1 three-copy source");
  check(f.first_frequencies.every(a=>a.length===1)&&f.second_frequencies.every(a=>a.length===1),"source dimension");
  same(f.first_frequencies,control.receiver_records[0].family.first_frequencies,"same original source rows for every policy");
  same(f.second_frequencies,control.receiver_records[0].family.second_frequencies,"same original second rows");
  check(r.score.full_secret_count===9&&r.score.complete_word_outcomes===27&&r.score.decoder_secret_hypotheses_enumerated===9,"complete prior, outcomes and charged MAP enumeration");
  check(r.score.efficient_unknown_secret_decoder_supplied===false&&r.score.ideal_PGM_circuit_supplied===false,"MAP/PGM references are not algorithms");
  const recipe=r.resource_recipe;
  check(recipe.original_native_source_copies===3&&recipe.full_frequency_scratch_cleared_BEFORE_mediator_Fourier===true,"actual original copies and clean scratch");
  for(const k of ["unknown_source_preparation_inverse_used","fiber_count_rank_unrank_oracle_used","source_states_reused_or_cloned"])check(recipe[k]===false,"no hidden resource");
  const coupling=f.public_coupling[0][0],eta=f.local_settings;
  const frequency=(w,start=0)=>mod(w.reduce((s,j,i)=>s+(j? (j===1?f.first_frequencies:f.second_frequencies)[i+start][0]:0),0),9);
  const setting=(w,start=0)=>w.reduce((s,j,i)=>s+(j?eta[i+start][j-1]:0),0);
  const A=words(2),B=words(1),all=words(3);
  const local=(s,w,start)=>square(scale(rootSum(words(w.length).map(x=>s*frequency(x,start)-setting(x,start)-3*x.reduce((t,j,i)=>t+j*w[i],0))),1,3**w.length));
  const P=[],dirty=[],wordDirty=[],localP=[];
  const classes=new Map();for(const y of B){const z=frequency(y,2);if(!classes.has(z))classes.set(z,[]);classes.get(z).push(y);}
  for(let s=0;s<9;s++){
    P.push(all.map(o=>{
      const a=o.slice(0,2),b=o.slice(2);
      const amp=scale(rootSum(all.map(w=>{
        const x=w.slice(0,2),y=w.slice(2),fa=frequency(x),fb=frequency(y,2);
        return s*(fa+fb)-setting(w)+coupling*(fa-frequency(a))*fb-3*o.reduce((t,j,i)=>t+j*w[i],0);
      })),1,27);
      exactProbabilities++;return square(amp);
    }));
    check(K.eq(sum(P[s]),K.unit),"exact clean source normalization");
    dirty.push(all.map(o=>{
      const a=o.slice(0,2),b=o.slice(2);
      return sum([...classes].map(([z,ys])=>K.times(local(mod(s+coupling*z,9),a,0),square(scale(rootSum(ys.map(y=>-setting(y,2)-3*b[0]*y[0])),1,3)))));
    }));
    wordDirty.push(all.map(o=>scale(sum(B.map(y=>local(mod(s+coupling*frequency(y,2),9),o.slice(0,2),0))),1,9)));
    localP.push(B.flatMap(y=>all.map(o=>scale(K.times(local(mod(s+coupling*frequency(y,2),9),o.slice(0,2),0),local(s,o.slice(2),2)),1,3))));
    check(K.eq(sum(dirty[s]),K.unit)&&K.eq(sum(wordDirty[s]),K.unit)&&K.eq(sum(localP[s]),K.unit),"exact baseline normalization");
    for(let j=0;j<27;j++){check(sign(K,sub(scale(dirty[s][j],classes.size),P[s][j]))>=0,"frequency-class pointwise domination");dominationChecks++;}
  }
  r.score.full_secret_MAP_winner_indices_by_outcome.forEach((winner,j)=>{
    check(Number.isInteger(winner)&&winner>=0&&winner<9,"valid MAP winner");
    for(let s=0;s<9;s++){check(sign(K,sub(P[winner][j],P[s][j]))>=0,"exact MAP optimality");exactWinnerChecks++;}
  });
  near(r.score.full_uniform_secret_MAP_success_numeric_reference,number(score(P)),"independent exact clean full MAP");
  near(r.score.least_trit_MAP_success_numeric_reference,number(tritScore(P)),"independent exact clean least trit MAP");
  const baseline=r.matched_randomized_local_baseline;
  check(baseline.distinct_B_frequency_classes===classes.size&&baseline.pointwise_clean_to_dirty_F_B_likelihood_domination_factor===classes.size,"frequency classes not word tags");
  check(baseline.only_single_copy_quantum_gates_used===true&&baseline.classical_dequantization_of_clean_echo_claimed===false,"LOCC baseline, not clean echo dequantization");
  near(baseline.full_uniform_secret_MAP_success_numeric_reference,number(score(localP)),"exact same-copy randomized LOCC full MAP");
  near(baseline.least_trit_MAP_success_numeric_reference,number(tritScore(localP)),"exact same-copy randomized LOCC trit MAP");
  near(baseline.dirty_echo_with_unerased_F_B_scratch_MAP_success,number(score(dirty)),"exact dirty frequency-scratch MAP");
  near(baseline.dirty_echo_with_a_full_B_WORD_tag_MAP_success,number(score(wordDirty)),"exact full-word tag MAP");
  near(r.full_secret_echo_minus_OWN_matched_LOCC,number(sub(score(P),score(localP))),"same-policy full-secret difference");
  near(r.least_trit_echo_minus_OWN_matched_LOCC,number(sub(tritScore(P),tritScore(localP))),"same-policy least-trit difference");
}
console.log(JSON.stringify({status:"PASS",exactProbabilities,exactWinnerChecks,dominationChecks,scope:"bounded q9 complete control; no general decoder or scaling certification"}));
