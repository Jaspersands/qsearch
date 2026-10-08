"use strict";

const fs=require("fs"),path=require("path");
const {check,same,rat,parse,str,cmp,mod,field}=require("./cyclotomic_exact");
const out=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../reductions/native_diagonal_orbit_channel.json"),"utf8"));
const K=field(9),near=(a,b,msg)=>check(Number.isFinite(a)&&Math.abs(a-b)<3e-10,msg);
const zero=()=>K.F(),key=x=>JSON.stringify(x),scale=(x,n,d=1)=>K.scale(x,rat(BigInt(n),BigInt(d)));
function numeric(a){let real=0,imag=0;a.forEach((x,i)=>{const v=Number(x[0])/Number(x[1]);real+=v*Math.cos(2*Math.PI*i/9);imag+=v*Math.sin(2*Math.PI*i/9);});return [real,imag];}
function ring(r){
  const h0=3**Math.ceil(r/2),h1=3**Math.floor(r/2),cross=r%2?2*h1:0;
  const reduce=([a,b])=>[mod(a-cross*Math.floor(b/h1),h0),mod(b,h1)];
  const times=(a,b)=>reduce([a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]-a[1]*b[1]]);
  const roots=[[1,0],[0,1],[-1,-1]],lambdas=[[0,0],[1,0],[1,1]];
  const rotate=(a,t)=>times(a,roots[mod(t,3)]);
  const phase=(a,b)=>{const v=times(a,b);return mod(r===2?3*(-v[0]+v[1]):r===3?v[0]-2*v[1]:v[1],9);};
  const total=(a,b)=>mod(a.reduce((x,v,i)=>x+phase(v,b[i]),0),9);
  const add=(a,b)=>reduce([a[0]+b[0],a[1]+b[1]]);
  const effective=(rows,v)=>rows.reduce((sum,row,i)=>sum.map((x,j)=>add(x,rotate(row[j],v[i]))),rows[0].map(()=>[0,0]));
  return {reduce,times,rotate,phase,total,lambdas,effective};
}
function words(m){if(!m)return [[]];return words(m-1).flatMap(w=>[0,1,2].map(j=>[...w,j]));}
const sourcePhase=(R,rows,s,w)=>mod(rows.reduce((p,a,i)=>p+R.total(s,a.map(x=>R.times(x,R.lambdas[w[i]]))),0),9);
const phaseString=p=>str(rat(BigInt(p),9n));
function controls(R,n){
  const values=[[Array.from({length:n},()=>[0,0]),0]];
  for(let i=0;i<n;i++)for(const b of [[1,0],[0,1]]){const v=Array.from({length:n},()=>[0,0]);v[i]=R.reduce(b);for(let t=0;t<3;t++)values.push([v,t]);}
  for(let t=0;t<3;t++)values.push([Array.from({length:n},()=>R.reduce([2,1])),t]);
  return Array.from(new Map(values.map(g=>[key(g),g])).values());
}
function protocol(R,rows,s,groups,alpha){
  const basis=words(rows.length),D=basis.length,L=groups.length,index=new Map(basis.map((w,i)=>[key(w),i]));
  const actions=groups.map(([b,t])=>basis.map(w=>{const y=w.map(x=>mod(x-t,3));return [index.get(key(y)),mod(rows.reduce((p,a,i)=>p+R.total(a,b.map(x=>R.rotate(x,y[i]))),0),9)];}));
  const act=(v,a,inverse=false)=>{const z=Array.from({length:D},zero);a.forEach(([j,p],i)=>{if(inverse)z[i]=K.times(K.powers[mod(-p,9)],v[j]);else z[j]=K.times(K.powers[p],v[i]);});return z;};
  const psi=basis.map(w=>K.powers[sourcePhase(R,rows,s,w)]);
  let state=actions.map(a=>act(psi,a));
  const history=[];
  for(let round=0;round<3;round++){
    const next=Array.from({length:L},()=>Array.from({length:D},zero));
    for(let g=0;g<L;g++)for(let h=0;h<L;h++){const u=scale(K.powers[mod(g*h+alpha*h,9)],1,3);for(let j=0;j<D;j++)next[g][j]=K.plus(next[g][j],K.times(u,state[h][j]));}
    for(const g of [0,L-1])next[g]=next[g].map(x=>scale(x,-1));
    let mean=Array.from({length:D},zero);
    actions.forEach((a,g)=>{const v=act(next[g],a,true);mean=mean.map((x,j)=>K.plus(x,v[j]));});
    mean=mean.map(x=>scale(x,1,L));
    state=actions.map((a,g)=>act(mean,a).map((x,j)=>K.plus(scale(x,2),scale(next[g][j],-1))));
    const density=state.map(row=>state.map(other=>scale(row.reduce((v,x,j)=>K.plus(v,K.times(x,K.conj(other[j]))),zero()),1,L*D)));
    history.push(density);
  }
  return history;
}
check(out.status==="NATIVE_WORD_ORBIT_PRESERVING_CHANNEL_ONE_COPY_SIMULATION_REVIEW_PENDING","scoped derivation status");
for(const n of ["observed_label_dependent_group_operations_covered","relative_orbit_preparation_and_inverse_covered","preserving_readouts_simulated_with_one_original_native_source_copy"])check(out[n]===true,"source-preserving channel scope");
for(const n of ["simulation_is_valid_for_arbitrary_fixed_frequency_prior","arbitrary_seed_mixing_or_independent_per_copy_group_actions_covered","all_native_quantum_receivers_ruled_out","new_quantum_algorithm_or_speedup_claimed","novelty_claimed"])check(out[n]===false,"do not promote orbit cut to arbitrary-source or receiver bound");
same(out.complete_source_controls.map(c=>[c.native_level,c.native_dimension,c.original_source_copies]),[[2,1,3],[4,1,3],[3,2,3],[4,1,4]],"complete source-control cohort");
let phaseIdentities=0,actionIdentities=0,densityEntries=0;
for(const c of out.complete_source_controls){
  const R=ring(c.native_level),rows=c.labels,s=c.native_secret,m=c.original_source_copies,n=c.native_dimension,offsets=words(m-1).map(v=>[0,...v]),W=offsets.length;
  check(rows.length===m&&rows.every(row=>row.length===n)&&s.length===n,"actual source dimensions");
  check(c.complete_original_word_count===3**m&&c.complete_word_orbit_count===W,"all original words and rotation orbits");
  const groups=controls(R,n);same(c.all_public_group_controls,groups,"public group controls independently reconstructed");
  same(c.complete_orbit_branches.map(b=>b.offset),offsets,"every word orbit, no selected collision class");
  for(const [i,b] of c.complete_orbit_branches.entries()){
    const v=offsets[i],u=R.effective(rows,v),global=sourcePhase(R,rows,s,v);
    same(b.effective_native_frequency,u,"native effective frequency, not an arbitrary label");
    check(b.exact_orbit_weight===str(rat(1n,BigInt(W))),"uniform secret-independent raw orbit weight");
    check(b.exact_secret_dependent_global_phase_mod1_NOT_USED_BY_SIMULATOR===phaseString(global),"source global phase");
    const native=[0,1,2].map(j=>sourcePhase(R,[u],s,[j]));
    const original=[0,1,2].map(j=>sourcePhase(R,rows,s,v.map(x=>mod(x+j,3))));
    same(b.exact_original_word_phases_mod1,original.map(phaseString),"original full-root word phases");
    same(b.exact_effective_qutrit_phases_mod1,native.map(phaseString),"effective native qutrit phases");
    for(let j=0;j<3;j++){check(mod(original[j]-native[j],9)===global,"exact global-phase factorization for every branch");phaseIdentities++;}
    const records=groups.map(([translation,t])=>[0,1,2].map(j=>{
      const w=v.map(x=>mod(x+j-t,3));
      const actual=mod(rows.reduce((p,a,l)=>p+R.total(a,translation.map(x=>R.rotate(x,w[l]))),0),9);
      const expected=R.total(u,translation.map(x=>R.rotate(x,j-t)));
      check(actual===expected,"induced tensor action preserves offsets and equals one-qutrit representation");actionIdentities++;
      return phaseString(actual);
    }));
    same(b.exact_action_phases_by_public_group_and_rotation,records,"every declared exact action phase");
  }
  near(c.maximum_original_vs_orbit_branch_state_error,0,"complete branch-state identity");
  const p=c.actual_label_dependent_group_protocol,alpha=mod(rows.flat().reduce((sum,[a,b])=>sum+a+b,0),9);
  check(p.public_group_control_count===9&&p.unitary_label_phase_index===alpha&&p.rounds===3&&p.all_final_seed_registers_discarded===true,"actual label-dependent group-only protocol");
  const actual=protocol(R,rows,s,groups.slice(0,9),alpha);
  const simulated=Array.from({length:3},()=>Array.from({length:9},()=>Array.from({length:9},zero)));
  for(const b of c.complete_orbit_branches){const density=protocol(R,[b.effective_native_frequency],s,groups.slice(0,9),alpha);for(let t=0;t<3;t++)for(let g=0;g<9;g++)for(let h=0;h<9;h++)simulated[t][g][h]=K.plus(simulated[t][g][h],scale(density[t][g][h],1,W));}
  check(p.full_output_group_density_real_imag_by_round.length===3&&p.original_vs_one_copy_orbit_mixture_density_errors.length===3,"complete protocol density history");
  for(let t=0;t<3;t++){
    near(p.original_vs_one_copy_orbit_mixture_density_errors[t],0,"reported one-copy simulation error");
    check(p.full_output_group_density_real_imag_by_round[t].length===9,"whole group output density");
    for(let g=0;g<9;g++){
      check(p.full_output_group_density_real_imag_by_round[t][g].length===9,"whole density row");
      for(let h=0;h<9;h++){
        check(K.eq(actual[t][g][h],simulated[t][g][h]),"exact whole group channel equals the one-copy orbit mixture");
        const expected=numeric(actual[t][g][h]),record=p.full_output_group_density_real_imag_by_round[t][g][h];
        check(record.length===2,"complex density entry");near(record[0],expected[0],"actual output density real part");near(record[1],expected[1],"actual output density imaginary part");densityEntries++;
      }
    }
  }
  const escape=c.seed_mixing_escape;
  check(escape.source_secret_for_escape_control==="all zero"&&escape.this_measurement_interferes_distinct_word_orbits===true,"explicit allowed escape outside cut");
  near(escape.original_batch_all_plus_measurement_probability,1,"coherent original source, not orbit mixture");
  near(escape.orbit_pinched_batch_all_plus_measurement_probability,1/W,"seed mixing distinguishes pinched source");
  check(escape.exact_pinched_probability===str(rat(1n,BigInt(W))),"raw pinched-source contrast");
  for(const n of ["simulation_global_phase_or_secret_is_an_algorithm_input","simulation_is_a_classical_dequantization","full_depth_receiver_supplied"])check(c[n]===false,"one quantum copy and no secret oracle or decoder");
}
same(out.growing_information_ledgers.map(c=>[c.native_level,c.native_dimension]),[[2,1],[8,8],[32,32],[128,128]],"growing information ledger cohort");
for(const c of out.growing_information_ledgers){
  const r=c.native_level,n=c.native_dimension,m=r*n;
  check(c.original_IID_copies===m&&c.simulating_original_native_source_copies===1&&c.public_auxiliary_rows===m-1,"actual one-copy model simulation ledger");
  same(c.uniform_full_ring_secret_success_upper_bound,{cap:1,numerator:3,denominator:{base:3,exponent:r*n}},"qutrit dimensional success bound, full ring prior");
  same(c.uniform_integer_embedded_secret_success_upper_bound,{cap:1,numerator:3,denominator:{base:3,exponent:Math.ceil(r/2)*n}},"actual integer-embedded secret prior");
  for(const n of ["simulation_requires_full_uniform_IID_frequency_prior","same_initial_public_frequency_record_distribution_preserved","final_readout_must_not_interfere_distinct_word_orbits","joint_original_input_trace_distance_error_adds_to_raw_bound"])check(c[n]===true,"source and readout premises");
  for(const n of ["arbitrary_seed_mixing_or_independent_per_copy_actions_covered","all_native_receivers_ruled_out"])check(c[n]===false,"nonpreserving escape remains available");
}
console.log(JSON.stringify({status:"PASS",exact_original_word_phase_identities:phaseIdentities,exact_induced_action_intertwiners:actionIdentities,exact_full_group_density_entries:densityEntries,one_copy_simulation_scope_preserved:true,seed_mixing_escape_preserved:true}));
