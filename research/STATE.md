# Research State

Read this page and `research/TRAPS.md` at the start of every Codex research
pass. `research/GOAL.md` is binding. Search the handoff/priority archives
only for a specific term; never read them whole. Paths below are relative
to `research/`. Rewrite at the end of each pass; detail belongs in notes.

As of 2026-11-10, after the handoff entry
"2026-11-10 Rees dfs2b Queue Finished: E_2(8) Determined (293 Primes), E_2(9) Known to 25000; Paper Pass Applied Locally (AI Only)";
several entries below it are from the same day.

Now (11-09, AI only): SDE F_q extension refereed by two AI referees.
- Proved (AI-refereed): p = 5, S = {0,±1} worst case n²/4 + 3n/2 + 2, deterministic (Theorem B′;
  KOW's q = 5 constant 0.4 -> 0.25). Theorem C: (1−1/p)a²/2 + O(a log a) (κ = 2 every odd p,
  κ = 3 at p ≡ 1 mod 3). Exact (Lemma Q repaired by Lemma N): no two-dependency 2-dim gadget at
  p = 7, 11, 13 (κ = 2); k = 3 at p = 7 also UNSAT. The lrat-check build used on 9 Nov was
  unsound; re-verified with the fixed checker: p = 7 (k = 2, 3) and p = 11. p = 13 is CaDiCaL UNSAT,
  not independently proof-checked (rerun queued; audits/reviews/2026-11-09-lrat-and-audit-fixes.md).
  q = 11, 13 interval S open.
- Next: does every spanning k = 3 label set at p = 5 realize three dimensions (n²/6 + O(n))?
  See audits/reviews/2026-11-08-rees-sde-fq-nest.md §0 and §8. SAT checks use gadget_cnf5.py
  (CaDiCaL + the fixed lrat-check in audits/reviews/2026-11-09-lrat-checker-fix/), not pycosat.

Now (11-10, AI only): square gap still OPEN.
- Proved, refereed: every p = 1 mod kappa with p <= kappa^3-3kappa^2+2kappa is in E_2(kappa).
  This is a twisted Stepanov bound (the pattern is separable); the paper says
  kappa^2-3kappa+3.
- Found: a separable-type certificate that O1, O2 and Chebotarev do not exclude. At kappa=4 its
  pair-signed form certifies from p=137, below 203. With Weil only it is rigorous at about
  T_A^2.
- kappa=5, exact at 56 single primes 181-2311 (validated C kernel): PW_pair < 1 at every tested
  prime 821-2311, PW < 1 at every tested prime 1231-2311; O1 barrier 2628, T_A(5) ~ 1.25e4.
- OSC' made precise (report section 11). The c/p bias is NOT a boundary term (exact
  decomposition; it sits in the complete-sum part). Two forms: per class OSC'(B), and per group
  OSC'_rms(B_L, B_D) (weighted rms over the m <= 6 and one-sided classes <= B_L, over m >= 7
  <= B_D kappa^2/p, plus noise). Conditionally either gives exponent (1/2+o(1))kappa:
  kappa/2 + kappa/(2 ln kappa) + log_kappa max(B_L, sqrt B_D) + O(1). Weights are bounded
  rigorously. OSC' is unproved for every kappa.
- Data: m_0 = 6 at kappa = 4, 5, 6. Group constants at typical primes do not grow with kappa
  (B_L medians 0.33/0.37/0.34, B_D 1.03/0.85/0.34 at kappa = 4/5/6; equal-p factors 0.55-2.3 per
  step; the lambda-law is excluded). kappa=7 at lambda 0.4 and 0.5: B_L 0.22-0.27, B_D < 2.6
  (2-sigma), not spikes. Per-class kappa=6 constants are NOT resolved (the earlier 2.8/3.1 were
  not bounds).
- Live obstruction: spike primes (report section 12). The kappa=6 survey is complete (89 primes,
  lambda 0.2-0.55; section 12.10).
  - Spikes reach B_L 1.88 (1657) and B_D 14.8 (1789), 4x and 18-25x the band medians. 9 of the 29
    primes with lambda <= 0.25 are spikes by some flag.
  - Over all 89 primes, 21 are spikes, and amplitude falls as lambda rises (largest B_D 14.8, 6.6,
    1.4). At lambda ~ 0.5 the debiased PW_pair is below 1 at all 29 primes (28 by the CS upper
    estimate).
  - Pre-registered: H1 (B_D spikes only at p = 1 mod 12) is refuted by 2143; the class shift H2
    held (MW 0.006 and 0.012, stratified 0.0001); no mechanism. symR predicted N1/mu1 at the 74
    later primes with rms log error 0.18: real prediction at lambda <= 0.31, none within the
    lambda ~ 0.5 band (slope rejected).
  - At lambda ~ 0.21, 71-88% of (C1) configurations are 2+2 involution-structured: some iota swaps
    two pairs of S and has two iota-pairs in T. This holds at spikes and at the one typical prime
    measured.
  - Spikes have a large family factor F (2.3-4.4, against 0.3) and large family class values (B_D
    4.3-17.3, against 0.44). The rest of the measure is lifted too.
  - Elementary bound (section 12.12; needs no (N); asymptotic only): with s the 2+2 share and
    G = s/R_2+2, the family can spoil the (1/2+o(1))kappa exponent only if G = kappa^{Omega(kappa)}.
    At kappa = 7-10 it certifies nothing (D addition kappa^{6.8-7.6} vs tolerance 3.4-5.7). Nothing
    bounds G (only cap G <= 1/R_2+2 = kappa^{2.4-5.1} at the thresholds); the counts sit below the
    Weil range; no counterexample family. Measured G: 0.5-2 at kappa=7 (5 primes); kappa=6 capped.
  - kappa=4 in closed form (section 12.13; AI-refereed sketch): #split in {1,3} by eta(r), eta(1-r)
    (r the cross-ratio); G(S) -> (2/3)#split, G(p) = 1 + O(p^-1/2) by Weil (a factor-2 bracket only
    from p ~ 3e6; thresholds ~100-200). Exact G 1.52 -> 1.003 for p 101-32009. At every fixed kappa
    G -> 1, and Weil's range is kappa^{(4+o(1))kappa} (corrects the kappa^{c kappa^2} of 12.12);
    near the thresholds the open question is the clustering of sparse one-variable patterns.
    kappa=5 shape pre-registered, held at 6 primes (G 1.17 at 1451, 0.999 at 100151).
  - F = G*N1/mu1. F over all 29 primes with lambda <= 0.25 (section 12.11) is 0.24-4.41, max
    1789, and tracks N1/mu1 (Spearman 0.98). CORRECTED: the earlier '"F bounded" is "(N)'s B
    bounded at spike primes"' was backwards; spike primes have N1/mu1 1.3-4.5 and do not stress
    (N). The 2+2 share falls with lambda to 0.50 (F1 refuted). Post hoc: share higher at p = 1
    than 7 mod 12 (0.71 vs 0.62); not a claim.
  - At kappa=7 (lambda 0.3 and 0.2) F is 0.5-1.8, inside kappa=6's range, so the 2+2 weight
    falls with R_2+2 = N_inv^2 kappa^4/p^2 up to F. At 23549 (lambda 0.2) it is 0.055 mu1,
    against 0.31-3.5 at kappa=6: a weight depending on lambda alone is rejected (P ~ 1e-7), at
    one prime.
  - kappa=7, p=36037 (lambda 0.31, picked on symR): a spike in B_L against two equal-lambda
    primes. B_L 0.635 (2-sigma >= 0.54) is 2.7x and 2.6x 35099 (0.237) and 34847 (0.245; median
    symR, scored by a rule written before its run, not close), and 2.4-2.9x the lambda 0.4-0.5
    values. About 2.4x the implied band median, against <= 1.46x for unflagged kappa=6 primes
    there. N1/mu1 1.08; B_D has a consistent sign but an unresolved size. Two primes do not give
    the kappa=7 spread.
  - Not carried by the 2+2 family: its 2+2 share is 3.1% (F 1.6), and without those configurations
    B_L is still 0.57 (2.4x 35099). What carries it is unexamined ("not 2+2" is mc_split's flag).
  - 34693, with 36037's symR (rule written first, seed 17): INCONCLUSIVE. Rest B_L 0.386 (2-sigma
    0.374-0.398), between the comparison primes (<= 0.270) and LIFTED's 0.40; prediction failed.
    Four primes at lambda ~ 0.3 sit at three separated levels; symR does not fix B_L; 95% of the
    excess is in (2,2); G 1.05. B_D is noise-level there and at 36037.
  - The exponent needs OSC' at lambda_T = 0.43, 0.18, 0.07, 0.02 for kappa = 7..10, below almost
    everything tested.
- Monte Carlo files from before the 9 Nov 22:20 batching fix overstate weak bins (report 11.3).
- Proved (AI-refereed): C1 configurations exist below pigeonhole (Theorem C; ~kappa^kappa/(2e)).
- Next:
  - the kappa=7 spread at lambda ~ 0.3: the other five primes in sym_rate_k7_lam03.out by
    mc_classes, rules written first (12:24:39), seeds 19-27 (mechanical item 6, RUNNING, done ~16:45);
  - theory: bound rho_rest (the not-2+2 part of OSC') or G near the thresholds (joint factorial
    moments of (b_K, m_K) at lambda ~ 1); neither has a method;
  - a (C1) sampler for kappa=8 at lambda 0.18;
  - (L') for the (2,2) classes;
  - kappa=5 at 2521 and 2621, once the machine is unloaded.
- See audits/reviews/2026-11-09-rees-square-gap-stepanov.md sections 11-12.
Compare its full title with `rg -m1 '^## 20' research/AGENT_HANDOFF.md`.
Other collaborators' Rees afternoon status and owner decisions are retained.

GAUDIN_TWO_CLUSTER_GAP.md gives a CLOSED written native counterfamily:
N=2n,n>=27, excitationM=n, distinct sites eps_Ai=n^-8*i,
eps_Bi=1+n^-8*i, g1/(2n), squared joint separation<=2312n^-5/3.
This refutes a UNIFORM Omega(1/N) floor under polynomial native conditioning.
Finite-spacing fusion pays the large internal coefficients; exact commuting
compression and two-tent min-max give the ALL-FAMILY bound. Exact n64 Sturm
plus the fusion proof gives physical128-site separation²<1/400<1/128.

The two-level BCS critical mechanism/exponent is PRIOR ART; no novelty.
Actual accepted Lutzv3 leaves the general SAME-sector bound open. Neither
its proved coupling limits nor its specific numerical families are refuted.
The strongest comparator is the classical n+1-dimensional fused problem;
N6 optimizer evidence alone was nonfalsification. Two CLOSED reviews checked,
two primary snapshots, three frozen scoped controls. No matching Theta law,
superpolynomial gap, general preparation no-go, separation or execution.
A weaker inverse-polynomial all-path gap could still pay native preparation.

Scoped milestone: audits/controls/gaudin_adversarial_gap/checkpoint.json.
Claude narrow fusion request refusedEMPTY, terminal/reaped/no findings/retry,
estimateUSD0.133568; historical valid n^-16 packet retained. Aggregate79
nonpartial estimatesUSD60.361134/38complete is NOTbalance; two older bills
UNKNOWN. Expiring-credit allocation persists. Independently reselect by
external value; no nearby critical variant, gap curve, filter or backend.

BINARY_FOCK_KERR_SAMPLING.md establishes a reviewed WRITTEN native quantum
count sampler for an explicit passive/number/Kerr circuit with binary Fock
occupations, poly(nativebits,logK,log1epsilon) gates. Every fixed-global-total
input/reference is covered; common grid, coherent degree phases, tail/cutoff
padding and clean-ancilla error are paid. Actual Prakash Cor2.3 already claims
the endpoint: PRIOR ART, no new algorithm or separation.

The decisive classical attack is CLOSED for BUNCHED input and numerical
chi=product(2 reduced Kerr denominators): coherent branch rejection from
multinomial condensates runs in bounded poly(chi,nativebits,logK,log1epsilon)
time. Binary binomial sampling, finite arithmetic and tiny-S coupling are
paid. Polynomialchi is classically matched; arbitrary-Fock and exponentialchi
are NOT. Exact two-photon control refutes an incoherent Fourier mixture by
TV1/2; exact dual-rail CZ gives only known universal-circuit inclusion.

Three CLOSED reviews parent-read, five actual primary PDFs plus NIST remainder
statement, frozen exact Sage control PASS. No full/quantum implementation,
novelty, hardness or separation. Scoped milestone:
 audits/controls/binary_fock_kerr/checkpoint.json. Claude useful binomial review
checked with precision guards; distinct generation refusedEMPTY. Both terminal,
no retry, estimateUSD0.314984. Aggregate78 nonpartialUSD60.227566/38complete
is NOTbalance; two older billsUNKNOWN. Expiring-credit allocation persists.
Independently reselect by external value; no nearby Kerr variant/backend.

Prior GAUDIN_JOINT_CHARGE_TRAVERSAL.md establishes a reviewed CONDITIONAL written
preparation: explicit commuting-charge randomization follows a known product
branch without intermediate Bethe-root/charge advice. With rank-one joint
separationkappa, derivativeL and paid simulation norms, bounded rational
random clocks/finite precision give polynomial BIT/gates in1/epsilon.
Known Boixo eigenpath machinery. Only averaged state preparation, no coherent
arbitrary-input label transform, reflection or fast-forwarding.

Full native Richardson-Gaudin preparation remains UNADMITTED: polynomial
SAME-M joint separation is OPEN, and rational distinctness alone does not
pay coefficient norms. Accepted Lutzv3 actual source also leaves that gap open.
ExactN3 gap1.879457<2 refutes a stronger constant floor; M1 analytically
hasgap>=2/N and is classically easy. Exactly12 prior bulk cases did not falsify1/N;
that is finite evidence only. The subsequent analytic two-cluster family above
REFUTES uniform1/N; no weaker inverse-polynomial lower bound, novelty,
separation or execution is established.
Two CLOSED reviews read, two primary PDFs, both new control scripts read.
Scoped checkpoint: audits/controls/gaudin_charge_tracking/checkpoint.json.

Claude QPE critique truncated with partial text, checked caveats retained;
independent gap request truncatedEMPTY. Both terminal/reaped, no retry.
EstimateUSD1.796010; aggregate76 nonpartialUSD59.912582/37complete is NOT
balance. Two old partial bills remain UNKNOWN. Expiring-credit allocation
persists. Next independently select by external value; this line re-enters
only with a concrete BULK joint-gap derivation/counterexample, not another
filter, mesh, easy-sector or finite-size scan.

Prior INDEFINITE_TERNARY_SPINOR_ADMISSION.md retains its reviewed classical
polynomial-BIT dyadic spinor compilation and ordinary-class-group falsifier.
Full native isometry remains PARKED: common-ambient transport with paid prime
support and local transporter offsets OPEN. No generic local backend queued.

Previous RATIONAL_GAUDIN_PREFIX_ADMISSION.md retains its exact determinant-
deletion and common-dual falsifiers, paid one-site marginal and conditional
classical sampling/sparse-readout comparator. Full Bethe preparation OPEN;
no new norm-boundary variant queued without an ALL-prefix operation.

Previous LOCAL_SATURATION_FINITE_PRECISION.md results remain: finite quotient
E=2L removes exact representative relations; bounded Stoll kernel has shape
t0*k[x]_(<=g-j). Smith precision and two-lambda monic losses are proved.
LOCAL_HALVING_SATURATION.md retains reviewed all-prime polynomial ITERATION.
Native actual-point HALF/labels/conditioning remain OPEN, so complete local
Kummer/global Selmer algorithms are not admitted. No new matrix utility or
model backend is queued.

COMPACT_INTEGRAL_SIMILARITY.md establishes a reviewed WRITTEN bounded-error
quantum polynomial-BIT/gate composition for arbitrary growing binary integer
matrices A,B: NO or polynomial-size compact INTEGER C with BC=CA, detC=+/-1.
Conservative GRH hypothesis retained; source S-unit/PIP does not itself need
GRH. No supplied centralizer, split map, maximal order, units, ideals or witness.
BHJ Cor9.16 is PRIOR ART; this repairs compact-output consumption, not a new
quantum primitive or a separation. Existing dimension2 minimum expanded-output
obstruction remains valid; expanded/short conjugators are outside the contract.

Paid single-matrix quotient, rank-one Steinitz formula, proper conductor and
normalized beta/xi yield compact descent. Local product residues REUSE
COMPACT_RESIDUE_CONDUCTOR_DECISION.md; fractional matrix sums use enlarged
moduli and exact small division. An integral lattice section and Jordan-length
character compute determinant from SMALL covolumes, avoiding generic compact
PIT. Verified unit-list union amplifies completeness; ABORT/false NO are in
eta. Positive structural certificates do not certify unit completeness.

Strongest classical baseline is the SAME BHJ reduction with classical
class/unit/PIP/finite-ring arithmetic. No hardness, novelty, practical cost,
human/formal verification, full implementation or quantum execution claimed.
Two closed reviews, two new primary snapshots plus reused corrected BS2025v2,
and one exact classical control complete. Controls distinguish dyadic/nonunit
and split-prime residues, safe denominator division, and length-weighted
-136 determinant from incorrect578. No old Pell/output-size rerun.

Claude useful residue review (two minor report errors repaired) plus empty
truncated determinant request estimateUSD1.093082; both terminal, no retry.
Aggregate68 nonpartial estimatesUSD51.757902/35 completed reports is NOT
balance; priorpartial timeout billingUNKNOWN. Dedicated expiring credit is
still allocated for useful research. Independently reselect next; no nearby
tuple variant, backend, generic compact-PIT project or agreement audit queued.

FOLDED_CHAIN_COHERENT_TRANSFORM.md establishes a reviewed WRITTEN uniform
quantum circuit for exp(-it H_N), the explicit open folded XXZ Hamiltonian,
on EVERY quantum input (including an external reference), with BIT/gate cost
polynomial in N, binary rational time length, and log(1/epsilon). Bond XOR,
complete 11/10/0 parsing with terminal D, and coherent conserved labels give
an exact direct sum of free paths. No fragment, Bethe-root or state oracle.
Controlled sine transforms preserve sector phases; finite compilation has
clean-input isometry error, with O(epsilon) ancillary leakage allowed.

Known Slater/CT classical algorithms MATCH basis-input quenches and specified
eigenbasis-state additive sparse-observable readouts, including long Pauli
strings and binary long times. No arbitrary-input classical simulation or
separation is inferred. Bulk encoding is prior art; no novelty, practical cost,
human/formal verification, implementation or quantum execution claim.
Source energy-factor discrepancy is resolved by the explicit Pauli definition:
hopping -1/2, one-body energy -cos. Periodic/general XXZ is outside scope.

Two closed reviews, four used primary sources (six retained PDF snapshots),
and one exact Sage run N=2..8 complete. Claude useful bijection proof plus
empty truncated composition request estimate USD1.223514; both terminal,
no retry. Aggregate 66 nonpartial estimates USD50.664820/34 reports is NOT
balance; prior partial timeout billing UNKNOWN. Expiring-credit instruction
persists. Independently reselect; no nearby deformation or backend queued.

QUINTIC_SURFACE_P2_ADMISSION.md establishes a reviewed WRITTEN bounded-error
quantum poly(logp,log1/eta) BIT/gate reduction for exactFULL degree53P2 of
EVERY smooth quinticSURFACE/P3/Fp, nativebinaryinput, FIXEDdegree5. Reused
constructor/induction with verified g31/r62/base45/nodes220, explicitarithmetic
frame/twist/localdata, recomputedQ_5/directcountfallback, degreeguards13578/62,
charzeroNewton, CRT2^54p^53 and restartedfiniteclocks. No GRH/Tate or hidden
torsion/monodromy/cohomology advice; no independent exact-outputcertificate.

Two closedreviews/five newprimarysources/exactclassicalcontrol complete.
KNOWN Deligne/Schnell theorem excludes generic Hodge-compatible abelian
replacement for VERYGENERALcomplex degree>=5 surfaces (primitiveHodge4,44,4).
This is NOT an allFpclassical lowerbound, exclusion ofspecialsurfaces or
novelbarrier. Actualcontrolledreduction retainsp-dependence. No novelty/speedup,
growingdegree, practicalcost, human/formal verification or full/quantumexecution.
ClassicalF7example58points givestrace+8,c1=-8; helperlabelerrorcorrected and
rerunonce, nofullP2 inference. Independentlyreselect; no d6variant/backend/sweep.

One usefulClaude reportestimateUSD0.512620, terminal/no retry. Aggregate64
nonpartial estimatesUSD49.441306/33reports is NOTbalance; priorpartialtimeout
billingUNKNOWN. Expiringcredit instruction remainsactive. Priorquarticwritten
reduction and its viableoldKS classicalcomparator remainrecorded below.

Prior Gaussian channel learner remains a reviewed written result with a full
product-input/Pauli classical data match; see its accounted-for row below.

CSA_MINIMAL_MODULE.md establishes a reviewed WRITTEN quantum polynomial-BIT
construction under explicit GRH for arbitrary growing CSA/field input: Schur
index d, a compact primitive idempotent and minimal left ideal/action. Classical
factoring-paid index, polynomial-size degree-d splitting field, known KM split
map and exact compact Hom/right-identity extraction pay the complete route.
No splitting field, module, local invariant or class/unit advice is supplied.

Positive certificate soundness is independent of GRH under field/CSA promises:
expanded maximal-order/index certificate + exact Amitsur cochain/presentation,
proved rank upper bounds and modular nonzero minors. Transcript-relative
reconstruction only, no input-canonical output or general PIT. Source/core
reviews, eightprimary sources and exact classical control complete. PARI table
index is UNSUPPORTED; specialized cyclic-H index2 passes, no hardness inference.
No novelty/separation, human/formal verification, expanded/integral/short output,
division normal form or full/quantumexecution. Two useful Claude reports cost
an estimatedUSD0.860428. Aggregate54 nonpartial estimatesUSD41.087802/29reports
is NOT balance; prior partial timeout billingUNKNOWN. Independently reselect;
no arithmetic backend or nearby extension queued.

STABILIZER_SPAN_RECONDITIONING.md establishes a reviewed exact separation:
every positive stabilizer frame confined to an explicit K=binom(n,2)+1 span
has condition>=2^n/[K(n+1)], even with arbitrary augmentation/reweighting.
Algebraic tagging forces EXACT rankK and unique minimum-rank span; every
rank-minimizer has squared coefficient cost>=2^n/[4(n+1)], while <=K+n+1
outside-span atoms give cost<=4(n+1). No hidden frame/source advice.

Source/core review and tagging addendum, fiveprimary sources and two exact
CLASSICAL controls complete. Base global fidelity9/[4(n+1)] and polynomial
extent paid; tagging is exponentially close to that easy base. No approximate-
rank hardness, native learning no-go, exponential GLOBALextent, novelty or
quantum execution. Known rank-to-extent2^O(sqrt(k logk)) and copy-only learner
retained; general polynomial-rank learning/optimizedextent remainOPEN.
Two useful Claude reports estimateUSD0.506252; BIT/COPY and zero-robust-radius
overstatements rejected. Aggregate52 nonpartial estimatesUSD40.227374/27reports
is NOT balance; prior partialtimeout billingUNKNOWN. Independently pivot;
no conditioning/projection/learner backend or nearby sweep queued.

REDUCED_NORM_PRESCRIBED_FIELD.md establishes a reviewed WRITTEN quantum
polynomial-BIT reduced-norm SEARCH under explicit GRH for arbitrary growing
CSA/field inputs and expanded a. Paid prescribed degree-n splitting field,
known Amitsur map and REGULAR-module transport give compact x, or exact HMS
sign NO; failures ABORT. Small-atom LS/HNF and checked expanded Phi provide
an exact deterministic classical positive construction certificate.

Three independent reviews/fourprimary sources/exact classical control complete.
Wild/negative local valuations, denominator-adjusted CRT, RIGHT multiplication
and compact modulus clocks paid. Classical HMS decision already known; PARI
norm baseline passed. No novelty/separation, human/formal review,
integral/short/expanded output or full/quantumexecution. Both Claude reports
useful, estimateUSD0.766564; unchecked-rho gap repaired. Aggregate50 nonpartial
estimatesUSD39.721122/25reports is NOT balance; prior partial timeout billing
UNKNOWN. Independently pivot; no adjacent integral/PIP/backend extension.

RELATIVE_NORM_TENSOR_SUPPORT.md establishes a reviewed WRITTEN quantum
polynomial-BIT compact N_L/K solver under EXPLICIT GRH for arbitrary growing
fields, expanded maximal-order bases/tables/embedding and nonrational target.
Relative tensor paired norms plus the reused absolute discriminant bound pay
complete support; full torsion and existing classical LS atom relations pay
the endpoint. No normal closure or hidden class/unit/solution advice.

Full independent review, actual BS/LS interfaces, Simon original pages67/74,
scoped2023 gate-synthesis baseline and exact PARI control complete. Classical
solver succeeds on the control; absoluteNorm1 can hide support above31.
No novelty/separation, integral/short/expanded output, practical scale or
full/quantumexecution. YES verifier exact; NO uses complete-source success.
Claude coordinate report checked, estimateUSD0.312188. Fable support request
terminal ReadTimeout/no report, billing UNKNOWN; no retry/evidence from it.
Independently pivot; no adjacent multinorm/norm backend or sweep queued.

MIXED_GAUSSIAN_PAIR_LEARNING.md establishes a reviewed WRITTEN polynomial-
copy/BIT learner for EVERY exact IID mixture of TWO arbitrary mixed fermionic
Gaussians, knownMajoranas/ordinaryqubitcircuits, no branch/weight/gap advice.
Degree2/4/6 exterior data, random6minor/Pfaffian/Lefschetz inverse, contracted
fourform support and uniformattenuation close reconstruction. Lowrank Schur
map reduces to<=2modecore; spectral parityblocks give DIRECT <=4Gaussian
output. No physicalchannel/CJ/postselection in final algorithm.

Exact/core, actualsource and full numericalcomposition reviews read/accepted;
explicitthresholds,κ^10000 precision/inverse ledger and allfiniteclocks paid.
Classical exact H/J/8Dcross/rank2/Schur/CJcontrol passed; no fulllearner or
quantumexecution. Suppliedcomponent Wick baseline and actual2026 stabilizer-
rank2 prioralgorithm retained. No human/formal review,novelty,separation,
practicalcost,noisy/offmodel,manycomponent or parity-restricted-gate claim.
One Claude attempt truncated at16k withunfinished397-characterprefix,
estimateUSD0.828720; no usableproof/retry/pendingcall. Aggregate47estimates
USD38.642370,22reports is NOTbalance. Independently pivot; no adjacent rank
extension,tomography backend or sweep queued.

WILD_LOCAL_SELMER_ADMISSION.md PARKS general growing-genus two-Selmer
DIMENSION under explicitGRH: arbitrary wild local-image generation and
dyadic regular-model BIT costs remain unpaid. Exact reviewed family
f=(x^(2g-2)-p)(x³-p²), EVERYg>=2/oddp, has image dimension1 while ALL
unramified curve-point traces vanish. Explicit ramified branch divisor
recovers the direction, within degree<=g. No general local/model no-go.

Known unstratified polynomial sampler has raw necessary-event probability
3^-N on a separate O(N)-bit family; no hardness or quantum lower bound.
Six primary sources, focused review and exact classical control complete.
Liu's actual dyadic resolution gives equations/termination; retain its
separate Weierstrass-chain bound v(Delta)/2. No total arbitrary-wild BIT
clock or effective complete divisor source was established. Two Claude
calls EMPTY/max_tokens, estimateUSD2.759310; aggregate46estimates
USD37.813650,22reports is NOTbalance. No findings/retries/pending calls.
No fullalgorithm, novelty/separation, MWrank or quantum execution.
Independently pivot; no resolution backend or adjacent sampling sweep.

CUBIC_COVARIANT_COPY_PROCESSOR.md rejects two uses of the KNOWN six-copy
antiidentity for hidden cubic-frame recovery. One-output channel sends each
Pauli r to r^5, preserves original stabilizers, and with polynomial copies
approaches their mixed code state; CCZ products lose frame intoI/2^n.
Two-Bell retention is EXACTLY ordinary independent Bell samples plus two
known-Pauli-corrected original copies, for arbitrary complex pure input.
Six-copy binary copy-linear covariant maps are only perm/anti-permutations.

Focused independent review, threeprimary sources and one exact complex/CCZ
control complete. GNW prior testing machinery retained; OPI/sparse-root and
actual folded/cycle-DQI screens did not pay a new native endpoint. Claude
useful report estimateUSD0.327524; false C^T C side claim rejected. Aggregate
44estimatesUSD35.054340,22reports is NOTbalance. No pendingcall/retry. No
learner, novelty/separation, native hardness, generalreceiver no-go or quantum
execution. General cubic learner stays PARKED; only these receivers CLOSED.
Independently pivot; no convolution learner/backend or adjacent gap sweep.

GLOBAL_COMPACT_ISOTROPY.md establishes a reviewed WRITTEN bounded-error
quantum polynomial-BIT isotropy decision/COMPACT point under EXPLICIT GRH,
EVERY growing-degree number field and nondegenerate growing-dimension form.
Expanded input pays compatible defining/maximal-order basis/table. One5plane
matches real signatures; local quadratic ideal norms and polynomial weakapprox
reduce5to4; opposite-ideal descent consumes known Amitsur quaternion splitting.

Four scoped reviews read, sevenprimary sources, one exact classical/algebra
control complete. PARI solves rational controls; gauged Q(sqrt6) descent,
discriminant sign and ramifieddyadic generators checked. Published local
formula has fractional-input counterexample; weak density bound does not
pay BIT clock, neither proves general hardness. No human/formal review,
novelty/separation, expanded/short/integral or compact Witt output, GRHremoval,
full/quantum execution. One useful Claude report plus one emptyrefusal cost
estimateUSD0.707116; aggregate43estimatesUSD34.726816,21reports is NOTbalance.
No pendingcall/retry. Independently choose next native mechanism; no backend.

TWO_GAUSSIAN_PAIR_LEARNING.md establishes a reviewed WRITTEN polynomial-copy/
BIT learner for EVERY normalized sum of TWO arbitrary pure EVEN Gaussians,
exact IID copies, knownMajoranas/ordinaryqubitcircuits, no branch/frame/gap/
overlap/minweight advice. Covariance groups, cancellation-uniform merge/
fourmode dichotomy, positive R2 pairing signal with quantified catfallback,
low-nu quarticorientation and charged known MPS tomography recover framephase.

Exact/core/composition/source AI reviews and one eightmode control complete.
R2gap243/6700 saturatescatbound; rotatedcovariance gives rank12 projector;
complex/cancellation and GHZphase controls passed. Earlier overstrongtest
nu>=1/3 failed; theoremnu>=c/3 unchanged. Known sequentialendpoint1002.4632
and phase-aware Pfaffian baseline retained; priority UNKNOWN. No fulllearner/
quantumexecution, classicalseparation, generalrank, noisy/mixedsource or
parity-preserving-only gate claim. Four Claude runs:2useful/2emptyterminal,
estimateUSD5.559080. Aggregate41estimatesUSD34.019700,20reports is notbalance.
Independently select next native mechanism; no rankextension/backend queued.

SPARSE_FOCK_TORUS_FALSIFIER.md rejects quadratic-variance/maximal-torus
completion as a GENERAL polynomial-sparse Fock learner. For Paley n=p3mod4
translate states, r=n branches have distance>=6, variancekernel exactlyu(1)
and nonzero gap>=10/11. ALL degree2/4 Majorana means are passiveU(n)-invariant.
Known Sugita Cartan twirl gives approximate-support success for any
U-independent listL of passiveframes <=L R(n+3)/[4 binom(n,w)(1-epsilon²)²].
Polynomial lists/support budgets therefore fail exponentially on HaarU.

Structural/source/quantifier reviews and exactp11 control complete. Full231
Gram has spectrum0^1,(12/11)^120,(10/11)^110; changedstate overlap43/55
has SAME moments, but degree6 occupation triple changes1/11 to9/275.
No generallearner impossibility/hardness, arbitraryGaussian-frame coverage,
novelty or quantumexecution. Joint/higher/coherent data remain outside scope.
One useful terminal Claude audit estimated USD0.596230; unsupported active-
frame overreach was rejected. Independent arithmetic screen still needs
smallgood cyclotomic specialization; CIT only tests a specified root.
No lowmoment backend, gap sweep or nearby counterfamily solver queued.

TWO_FOCK_GAUSSIAN_LEARNING.md is a reviewed WRITTEN polynomial-copy/BIT
learner for EVERY exact parity-definite G(alpha|x>+beta|y>), shared unknown
even Gaussian G, arbitrary same-parity Fockstrings, known physicalMajoranas.
No minimumweights, frame/inverse or branch advice. For Hammingk>=6,
connectedquartic K=4p(1-p)W(Jactive) has isolated top eigenvectorJactive.
Uniform spectral/polar rounding, old fixed4 compression, dominantGaussian
fallback and fresh two-dimensional phase tomography close the endpoint.

Core and actualsource reviews complete. The fixedparticlecap/pairedmagic
sources do not cover all growing cats; substantial quarticcumulant method
overlap remains, priority UNKNOWN. Exact7mode/6active control verifies
spectrum5^1,1^30,(-1)^35,0^25, phaseblind moments, learned56Givens frame,
phase recovery and k4/k2 countercontrols. No full noisy learner or quantum
execution, general sparsity, unknownMajoranas, novelty or separation.
Classical supplieddescription Pfaffian simulation remains; all inference
processing is classical. Two useful terminal Claude reports estimated
USD1.650348; no retries/pendingcalls/balance inference. Independently select
the next externally valuable mechanism; no adjacent backend is queued.

GENERAL_SPARSE_CONSTANTS_ATTACK.md establishes a reviewed WRITTEN classical
polynomial sparse-BIT algorithm for Alg={e:u^e algebraic/Q} for EVERY charged
growing-degree monic irreducible Q(T)[Y] field, growing s,k and binary sparse
T exponents. Original-basis extended derivatives, implicit coefficient bounds,
large-prime evaluation and FULL congruence/LLL recovery are paid. Alg is NOT
fullRel; the uniform compact-constant operation remains OPEN.

Direct rational specialization in the supplied monic basis can force
exponential expanded bits at EVERYgood point; naiveLC can cancel on all
simple branches. The explicit counterfamily itself is easy (Alg=0), so this
is no hardness or generalmapimpossibility claim. Core/counterfamily review
and exact quartic control passed (41-bit exponent, derivative rank2, Alg5,
nonrationalconstants/sign, badp257 rank1). No fullsolver/quantum execution,
novelty or separation. Two terminal empty Claude calls estimated USD0.900988;
no findings/retries/pendingcall/balance inference. Independently select the
next mechanism; no easyfaceextension or constantbackend is queued.

HIDDEN_CUBIC_PHASE_LEARNING.md: reviewed admission pass PARKED. Exact-copy
unknown-Clifford occurrence2 cubic learning has local factored Bell equations,
but no paid frame extractor. A proved uniform factored-event gap (d3,k5:
2^-72) lets polynomial copies exclude false factored equations. It does NOT
certify full K5 or locate factors. Generic two-factor search with prescribed
nonzero value contains graph4-coloring; NO native-hardness transfer.

Actual known-frame/product-block/supplied-stabilizer sources retain their
access limits. Exact CLASSICAL Bell sampler from suppliedf,C and six-variable
K4 control passed (support925, offset trap, K1=0/K2dim1). No all-n width,
learner, novelty, separation, quantum execution or noisy-source claim.
Two terminal empty Claude max_tokens calls cost an estimated USD2.350002;
no findings/retries/pending call/balance inference. No gap sweep or generic
factor backend queued. Independently select the next native mechanism.

CYCLIC_SUPPORT_MONOMIAL_DESCENT.md is a reviewed WRITTEN bounded-error
quantum polynomial-BIT torus-torsor/descent solver under EXPLICIT GRH.
Input explicitly pays Galois E/Q, maximal order, all automorphisms, arbitrary
integer monomial action and cocycle; return NO or compact x with a_g=x/(g star x).
This does NOT construct a succinct torus's potentially enormous splitting field.

Cyclic decomposition/fixed-field transfer removes outside-S valuations
PRIMITIVELY; discriminant tower/source48 pays polynomial support without
auxiliary fields. Complete compact S-units plus existing LS atom relations
and exact integer solving close the endpoint; torsion included. Positive
verification is deterministic/unconditional and precedes emission. No new
log/equality subsystem. All four reviews and one exact cyclotomic control
complete, with classical Smith witness, torsion14 and260-bit compact output.
Classical S-units and Hilbert90/permutation/conic baselines remain; substantial
Amitsur/cohomology prior overlap, priority UNKNOWN. No novelty/separation,
expanded/integral/short solution, GRH removal or full/quantum execution.
Two terminal Claude calls: one refusal, one useful, estimated USD0.482402.
No retry or balance inference; independently select the next native mechanism.

TENSOR_SQUARE_RATIONAL_NORMS.md is a reviewed WRITTEN bounded-error quantum
polynomial-BIT rational norm solver under EXPLICIT GRH, arbitrary growing
number-field degree, explicit MAXIMAL-order basis/table and rational target.
Return NO or compact x with N(x)=a; no hidden closure, class/unit or solution
advice. Positive compact outputs admit exact classical norm certificates.

Unconditional support lemma uses paired norms from L tensor L and the full
primitive residue-degree kernel. Tensor discriminant D^(2n) and source48
pay a polynomial numerical prime support; no auxiliary fields are computed.
One complete compact S-unit computation in L plus classical gcd-free norm
coordinates/signs/HNF closes the endpoint. Full reviews and one exact degree5
control complete, including matched PARI witness and compact signed output.
Simon prior overlap is substantial; inspected tensor-torus results do not
supply the same support bound. Priority UNKNOWN. Prime-degree/S_n HNP gives
strong existence baselines, not compact witnesses. Claude's smooth-relation
and Chebotarev runtime claims were not accepted as proved algorithms.
Two useful terminal Claude calls estimated USD1.325932; no retry or balance
inference. No novelty/separation, integral/short solver, GRH removal or full/
quantum execution claim. Independently select the next valuable mechanism;
no adjacent norm extension or general backend is queued.

ARBITRARY_PAULI_MAGIC_LEARNING.md is a reviewed WRITTEN polynomial-time
copy learner for every exact C exp(-i*pi*P/8)H^n, arbitrary signed Pauli
including partial/empty support, unknown Clifford. This completes the native
one-extra-T-amid-Cliffords architecture on extensive H magic. Approximate
preparation within epsilon, failure eta; no source inverse or hidden axes.

Core/source/endpoint/integrated reviews complete. Interference deletion gives
canonical active K3 and gamma3>=1/1024 for w>=25. Smallw nonzero atoms pay
uniform global gamma2>=4^-24/48, followed by direct bounded-block tomography;
large blocks use old cubic physical-axis extraction and exact-candidate
verification. Universal gap inverse ~1.35e16: asymptotic, NOT practical.
One exact four-case control catches Y cancellation, six YZZZZ deleted labels,
and affine-point/physical-direction confusion; n4 decoder reused, no search.
Both Claude audits useful, total estimate USD1.432656; corrected minor report
wording, no retries or balance inference. No full/quantum execution, novelty,
classical separation, noisy/angle/two-rotation/MPS/channel claim. No adjacent
implementation; independently choose the next externally valuable mechanism.

ONE_ROTATION_MAGIC_LEARNING.md is a reviewed WRITTEN polynomial-time
copy learner for every n>=4 exact C exp(-i*pi*Z^n/8)|H>^n, unknown Clifford.
Output preparation within trace distance epsilon, failure eta; paid
poly(n,1/epsilon,log1eta), no source inverse/evaluator/hidden axes. Complete
cubic Bell source, uniform Lie/square-zero/degree3 Macaulay extraction and
capped known product learners compose with fresh-copy candidate verification.

Core/source/full error-resource independent reviews complete. n+1 physical
axes suffice; no uniqueness. Clifford-product width n and >0.088 distance
from any nontrivial Clifford PURE product explain existing-source limits,
not hardness. Exact n4 Bell and scrambled Macaulay controls pass with zero
coefficient search; wrong p-period/commutator/inverse-transpose shortcuts fail.
No full learner/quantum execution, novelty, classical separation, general
noisy/MPS extension or hardware claim. Arbitrary Pauli is now covered above. Three Claude calls
estimated USD1.988864: one useful, one empty truncated, one refused; no
retries or invoice/balance inference. No adjacent implementation queued;
independently rank the next native operation.

GOOD_DYADIC_GROWING_SELMER.md is a reviewed WRITTEN bounded-error quantum
polynomial-BIT two-Selmer DIMENSION composition for explicit growing-genus
smooth Z2 hyperelliptic models, odd-Galois branch field factors, and good
odd p<=d. No supplied class/unit/point/local advice. New CLASSICAL local
trace/shallow-formal and nonsaturated O/8 operations pay dyadic generation;
large-p images and existing quantum global arithmetic close the endpoint.

Core/source/global/family/integrated reviews complete; separate sign units,
aggregate complete-basis error and atom norm-height precision repaired.
Odd-cyclic Grunwald/CRT supplies a nonvacuous Q x K x K family for every
odd-prime genus, no efficient input generator promised. Exact duplicate-field
norm simplification reuses K arithmetic; no classical polynomial counterpart
established. One genus3/tangent/dyadic-filtration control passed; no full
Selmer/quantum execution, novelty, separation, arbitrary-curve or MW-rank
claim. Claude coordinates report useful, trace request refused; total estimate
USD0.223688, no retry or invoice/balance inference. No adjacent implementation
queued; choose the next native mechanism by independent external value.

LARGE_PRIME_LOCAL_KUMMER_IMAGE.md is a reviewed WRITTEN CLASSICAL
polynomial-BIT complete delta(J(Qp)) algorithm for monic separable odd
d=2g+1>=3, p>d, growing genus and arbitrary bad reduction. Paid all
small-degree tame fields, bounded exceptional discs and character-functional
span sampling replace field scans/rare sources. Explicit p-integral orders,
finite-ring coordinates and P/S/W precision close BIT costs; actual rank
r-1 certifies every returned basis, capped failures return ABORT.

Independent core, actual full-source/arithmetic and final integrated reviews
complete; Claude coordinate audit repaired stopping/frame/basis details and
prompt/source omissions. One exact generic-span/fractional-child/Cramer
control passed and rejected stronger false assertions. No full algorithm or
quantum execution, novelty, global Selmer, small/wild/dyadic or MW-rank claim.
No larger implementation or adjacent extension queued; independently rank
new native end-to-end mechanisms before the next pass. Four Claude calls
cost an estimated USD6.767224; three ended empty, one useful report. No
invoice/balance inference or retry. Seven-day use-all allocation is durable.

General sparse characteristic-zero small-order specialization remains OPEN:
actual bounded-CIT tests a supplied order, not a polynomial numerical good
order for norm circuits. No classical completion or new quantum receiver
was established by those empty searches.

BOUNDED_DEGREE_CONTRACTION_BASELINE.md is a reviewed WRITTEN source-based
classical exact Boolean contraction composition for explicit constant-arity/
occurrence tables over FIXED Q(zeta8), explicitly charged variables L>=n.
Actual main-source layout/counting and added BIT/space obligations checked.
Time poly(L)*2^{O(n(loglogn)^2/sqrt(logn))}, polynomial space. Explicit
H,T,CNOT ONE amplitude inherits n<=2G and a subexponential G bound.

One exact four-variable supplied-design control passed nine jets and Hermite
recovery with nontrivial measurement kernels and complex algebraic weights;
wrong x-dependent corrections and omitted fixed bits fail. No asymptotic
algorithm, SAT or quantum execution. Independent final reviews complete;
unused-variable output size repaired. Claude completed, estimated USD0.32692.
No whole ETH manuscript/sharper appendix acceptance, novelty, polynomial
simulation, qubit-count bound, sampler, oracle gate or new quantum algorithm.
Compare the MINIMUM applicable classical time bound; space costs differ.
No follow-on simulator/appendix audit queued. New quantum operation must win
independent native-value admission; SU(n) compilation alone and an unresolved
weighted-character hidden-torus receiver did not supply one this pass.

MONOMIAL_KUMMER_SPARSE_RELATIONS.md is a complete reviewed WRITTEN classical
polynomial sparse-BIT full-relation algorithm for irreducible monomial
Kummer fields, growing s,k,charged numerical delta and binary T exponents.
Unimodular constants and noncancelling leading coefficients stay compact;
original-basis derivatives, modular LLL and actual LS pullback are paid.
Both core and combined actual-text/source/resource reviews accepted.

One exact delta6,41-bit exponent control recovered Alg rank5 and full Rel
rank3, retaining order2 sign nonsaturation, compact powers, tied LCs,
derivative/LC false positives and p257 content collapse. No general LS,
theorem-sized or quantum execution. No general-f counterpart, novelty,
separation or poly(logdelta) claim. No API call or follow-on implementation
queued; general growing-degree constants remain unknown. Next selection
must independently rank external value, not extend this result by inertia.

Previous independent comparison found no new paid quantum mechanism.
OSCILLATOR_PAIRING_AND_MECHANISM_TRIAGE.md closes only the proposed nonlinear
escape under an EXACT universal pairing identity: it forces a linear map
(or affine with a global phase), and the public square-permutation case has
an exact polynomial classical optimizer and uniform-shell sampler. Narrow
review accepted; one Sage linear/Toffoli control passed. Rectangular DQI,
other nonlinear constructions and quantum-only access are NOT dequantized.

List-decoded DQI and its random-table normalization are already known/local;
rank-metric DQI is prior art; other independently compared native directions
supplied no new paid decoder. Growing-degree character recovery remains open
with exp(O(d log d)) existing cost, but this pass supplied no factorial-removal
operation. Claude returned terminal refusal with no report, estimated$0.063892;
request/usage retained, no retry. No infrastructure, scan or neighboring
extension queued. Fresh selection must independently rank external value.

SPARSE_CHARZERO_FUNCTION_FIELD_RELATIONS.md is a reviewed WRITTEN bounded-
error quantum polynomial-BIT full relation algorithm for explicit Q(T)[Y]/
monic irreducible f, growing s,k,charged delta and binary sparse T exponents.
Nonzero inputs are promises; no inverse, constant-field, valuations, points
or relation advice. Quantitative Northcott/all-place log geometry pays the
full basis bound; large-prime content and point-norm union bounds pay exact
finite-ring HSP/LLL recovery. Full core/source/resource/actual-text reviews
complete. No arbitrary ideal conversion, novelty, separation or execution.

Decisive classical attack closes ALL degree1 and degree2 inputs of this SAME
sparse-bit model, including growing variables and tuples. Modular derivative
congruences and exact LLL recover Alg; original leading coefficients in Q or
an explicit quadratic field recover the full Rel via actual LS. One norm
resolves quadratic leading cancellation, without Puiseux expansion or huge
basis powers. This supplies classical algorithms, not a new quantum primitive.

One exact N=2^40+1 control passed without T-power expansion. Both square-root
branches give Z(1,1,-1,0); derivative-only/LC-only and small-characteristic
false positives are caught. No HSP/generalLS/full algorithm run. No API call
this pass. General growing-degree classical sparse-bit place computation and
novelty remain UNKNOWN; no reverse char0 DLog equivalence is asserted.
Actual thermal/zeta and native syndrome/Legendre alternatives supplied no
new paid operation in the independent comparison. No neighboring extension
or implementation queued; next pass must independently rank external value.

WRITTEN CONSTRUCTIVE QUANTUM COMPOSITION: full core/resource review accepted.
FUNCTION_FIELD_RELATIONS_RANDOM_SPECIALIZATION.md computes exact relation
lattices over explicit Fp(T)[Y]/monic irreducible f with s,delta,k all growing
and binary-sparse coefficient degrees, in bounded-error polynomial BIT time.
Random large finite specialization, canonical full quotient HSP and exact
short-prefix LLL pay the whole algorithm. No inverse, divisor, constant-field,
source-point or relation advice; no arbitrary ideal-to-field conversion.

The uniform basis bound and simultaneous norm-polynomial collision bound
are proofs, not deductions from finite controls. One exact F5(T) rank2
nonsaturation/collision control and a nilpotent quotient guard passed;
no HSP or full algorithm execution. Claude refused without findings,
estimated$0.047964; no retry. No novelty or separation claim.

Classical counterpart and final actual-text review complete: private random-exponent tests
supply primitive generators from generator-promised DLog without factoring;
residue logs and nilpotent filtration pay full finite-ring relations. With
actual KW1906.10668 Thm1.1, the WHOLE algorithm is already classical
quasipolynomial for fixed p. Do not imply exponential separation there.
The forward reduction and constant-field two-unit special case give randomized
polynomial-time Turing equivalence with finite-field DLog, preserving fixed p.
This is a constructive reduction, not a new quantum primitive or hardness proof.
No implementation or neighboring extension queued; next selection must
compare independent externally valuable mechanisms.

The previous pass completed a constructive CLASSICAL composition:
AFFINE_UNIT_RELATIONS_DIFFERENTIAL_SPECIALIZATION.md computes the full
relation lattice of growing supplied unit/inverse tuples in a PRIME affine
Q-algebra with FIXED variable count, in deterministic polynomial bit time.
Characteristic-zero PRIME Z-domains inherit it by rationalization. Independent
core, source/cost and final actual-text reviews complete. Explicit dlog
module and rational-function size lemmas, finite specialization and original-
unit LS relations avoid fixed-k enumeration and huge power expansion.

Two exact Sage controls passed, including nontrivial Q(sqrt2) constants.
Neither runs general LS or the full algorithm. No complete unit/class/PIP
computation, quantum advantage, novelty, growing-variable, finite-characteristic,
nonreduced/reducible or sparse-binary-exponent claim. The new metabelian
paper's remaining quantum scopes are not dequantized. Claude audit cost
estimate$0.393336; verified source obligations and dispositions are durable.

Independent selection found no new operation from explicit-form Hessian/QFT
under its generic-pencil conditions, supersingular torsion alignment without
an evaluator, or Galois factor-degree sampling. The actual new metabelian
source2610.27250v1 supplied the constructive arithmetic lead. Further work
on positive characteristic must offer a PAID growing-tuple operation and
win an independent value comparison; dlog(x^p)=0 invalidates a naive transfer.
No automatic extension, new subsystem or further control is queued.

The previous pass closed two concrete decoder tests, without a new algorithm.
LEGENDRE_FOURIER_FEATURE_CLASSICAL_MATCH.md is independently actual-text
and Claude proof reviewed. Chosen-BIT additive Fourier means AND public
candidate-syndrome scores have classical poly(m,logp,epsilon^-1) estimators.
This matches robust statistical-query interfaces, not full-label laws or
copy-only sources. A polynomial SQ decoder would remain valuable; none is
known here. The complete true-Q syndrome marginal equals the public mask
marginal for root-freeQ, while ideal moments+independent mask noise is an
INCORRECT full-label law. Oldp5 gives8/3125 versus1/3000 at0; all oddd>=3
irreducible targets also disagree exactly. No controlled-approximation
lower bound follows. True recurrence rows are not mostly correct, but
low-inlier regression and coherent/joint-label decoders remain OPEN.

One Sage reuse of the EXISTING p5 case passed exact counts and six native
classical-estimator populations. No new FFT, parameter sweep, quantum
execution or full-suite claim. Fable constructive call refused without a
report; distinct Opus/high proof audit completed. Estimated pass usage
$0.57356; snapshots and dispositions are durable, not invoice/balance data.

The actual new superlattice paper was obtained from its public mirror.
SUPERLATTICE_CONDITIONAL_RECORD_AUDIT.md and durable source excerpts record
its conditional record+marked-occurrence sampler (success>=1/2), still
exponential in list work/space and explicitly omitting discarded scalar
coins. No polynomial pure-DGS or clean inverse follows. Chosen-line
multivariate interpolation inherits fixed-degree univariate decoding.
Next selection must compare independent native mechanisms; do not write
another nearby Hankel/lattice barrier or implement a wrapper without an
explicit paid operation and an end-to-end role.

Section10 of PRIME_INDEX_FACTORIAL_RESIDUE_NORMALIZATION.md now REMOVES
all physical Gauss-phase calls from the written factorial composition.
Parent proof, independent Claude/Codex core and final actual-text reviews
are complete. Fix zeta and sigma, choose ANY classical algebraic root of
t^ell=A, and evaluate unit modes and algebraic tau_j in that SAME embedding.
Both acquire zeta^(-bj), so their ratio and selected unit exponent are
invariant. The physical isomorphism is proof-only; its branch is not learned.
Quantum factoring and complete compact S-units remain required. This is
not a classical Gauss-phase algorithm or a full classical factorial solver.

A sharp mismatch law keeps the local pi=p/t FIXED: unit embedding b and
numerical target embedding d give k!*r^(d-b). One exact Sage ell5,p11
control gives all5 matched outputs2 and all5 target-only mismatches8;
256-bit numerical mode covariance error<2.8e-77. The known c supplies
validation truth; no L1 sampler, PIP or quantum routine was run. No new
sweep or implementation is queued. The older cubic construction inherits
the same removal at ell3; its original Gauss-based version remains optional.

Independent selection rejected explicit trilinear-form cubic-phase Bell
sampling as a new mechanism: its measured quadratic-derivative law has an
exact O(n³) Gaussian-elimination sampler. No coherent GL-control no-go.
Existing lattice pair-cooling supplied no new paid operation. The actual
new superlattice source audit is now complete at the scope above; its full
144-page algorithm has not been independently verified. Source claims and
the conditional-record deduction must retain that distinction.

PRIME_INDEX_FACTORIAL_RESIDUE_NORMALIZATION.md is now independently
core/source, integrated-resource and final actual-text delta/source reviewed.
For EVERY odd prime ell dividingp-1, the WRITTEN unconditional bounded-error
quantum composition computes((p-1)/ell)! modp in poly(NUMERICAL ell,logp,
log1eta), with no GRH or supplied arithmetic advice. Numerical ell matters;
this is polynomial in binary input size only when ell<=poly(logp).
Uniform fields, complete compact units/class data, generator-height
balancing, phase/residue normalization and whole-output confidence are paid.

Claude audits sharpened compact-DAG exponent accounting and precision,
phase-mode selection and explicit source/access contracts. A genuine
source-packet defect was repaired: PDF page breaks shifted splitlines()
locators and omitted Greither's proof. Actual pp456--457 give C_small=2C
by augmentation; actual p496 cancels the SAME-action correction at every
R-prime above2. Corrected primary excerpts and independent source review
are durable. The existing randomized nonrealL1 estimator refutes the
reviewer's speculative analytic GRH objection. Passing reviews alone are
not the proof: the parent checked these derivations and source statements.

The durable ell5,p11 control passes: alpha2!=alpha but the factorial residue
is2; an unnormalized real unit makes integer Hilbert90 fail. It executed
no PIP or quantum primitive. Classical Tal factorial and class/unit
baselines retain their scopes. No novelty, classical separation, arbitrary
factorial or poly(logell) claim. Next selection must compare independent
externally valuable mechanisms; no nearby extension or implementation
is admitted merely because this composition is now complete.

Owner-authorized Claude integration is complete and used: selected-context
runner, cost preflight, exact snapshots/usage,23 focused tests passed.
Eight paid requests yielded3 completed reports and5 truncated attempts;
usage estimate$8.956502, not an invoice or account balance. The owner
raised the provider limit to$200 after one preflight refusal; resumed use
succeeded. Default to narrow high-effort Claude tasks, keep parent core
reasoning at top effort, and treat every finding as something to verify.
See CLAUDE_RESEARCH_WORKFLOW.md and the note's Section9 dispositions.

Completed constructive cubic-factorial pass:
THIRD_FACTORIAL_CUBIC_CIRCULAR_UNITS.md Sections1--8 has independent
core/source and final actual-text review ACCEPTED. For EVERY binary prime
p1mod3,p>=7, the WRITTEN unconditional bounded-error quantum composition
computes((p-1)/3)! modp in poly(logp,log1eta). Degree3/6 fields, complete
compact S-units, exact SAME-action class Fitting ideal, known Gauss phase
and classical nonreal L1 are paid. No GRH or supplied arithmetic advice.

All2015v2 Thm1.2 controls split character lengths; the scalar regulator
index controls inert/ramified primes. C=Fitt_Z[rho](ClK)U is an exact
submodule identity, not class-module isomorphism. Integer unit Hilbert90
and LOCAL normalized alpha/tau(bar chi) give the canonical factorial.
Binary compact exponents, certified log rounding, leafwise local HNF and
full-output amplification are explicit; no numerical h cost is hidden.

Durable p313 exact controls catch reversed sigma (same index, wrong
lattice), a missing norm sign, and swapped denominator (a local pole).
Correct output72=104! mod313. Degree312 cyclotomic truth is validation
ONLY. Full quantum arithmetic was not executed. Classical comparators
include ERH subexponential class/unit algorithms and the actual Tal
Thm1.1/1.3, Props1.7/4.2/4.3 divisor/fixed-index results. The existing
69-page cached source already contained the broader comparison; no
changed-version inference remains. Exact Jacobi is already classical
at fixed order. No novelty, separation or general-factorial theorem.

This completes a fixed-degree native composition, not the repository's
research goal. Select a new paid growing-parameter mechanism against
independent directions before more arithmetic extensions, sweeps or
implementation. Classical matching remains open here, not hard.

Completed native EDS source pass: ELLIPTIC_DIVISIBILITY_CHARACTER_ADMISSION.md
Sections5--7 and the all-index counterexamples passed independent core
and actual-text review. For every known odd order r>=3, u=(r+1)/2,
f_P(n)=e_P(un modr)*e_P(u)^n, where e_P(m)=chi(2y(mP)) and e_P(0)=0.
One legal even anchor plus one even query reconstructs any full answer;
original integer parity and zero handling are essential. Odd indices
contain NO extra information. No coprimality normalizer is assumed.

On a public prime subgroup, identical sources are exactly kH, where H is
the multiplication stabilizer of public b(m)=chi(2y(mG)). Efficient H
computation is not paid. The y-preserving order3 automorphism on
E/F7:y²=x³+3 proves identical full sources for G=(1,2),3G=(2,2),9G=(4,2),
although the whole group has prime order13 and p3mod4. Generic-j alone
also fails: E/F13:y²=x³+4x+8,j7 has an order5 subgroup whose four nonzero
points all give the same full source. A stronger reviewed rational order7
family gives THREE identical sources for every p3mod8,p>3; excluding43,83
makes j generic. Exact e_P(m)=-(m|7), H={1,2,4}. This is a fixed-r family,
not growing-order or whole-group-prime. The counterexamples are proofs
with exact controls; other finite separation tests imply no asymptotic
identifiability. The simultaneous p3mod4/generic-j/whole-prime-group
promise remains unresolved, not hard.

Actual LauterStange2008 full-value/supplied-point reductions do not solve
this character-only hidden-point input. JaoJetchevVenkatesan2007 already
frames multiplier character reconstruction, with conjectural analytic
separation and unresolved decoding; its algebraic-coordinate theorem has
different outputs. Exhaustive cyclic matching is a legal classical
comparator; stronger exact-source reconstruction remains UNKNOWN.
The source-correct Boolean hidden shift remains valid, but no informative
receiver or efficient decoder is supplied. No degree-free Weil bound,
free stabilizer computation, injectivity, novelty, speedup or execution.
This line is PARKED pending a new paid operation or decisive classical
attack. Compare independent high-upside native mechanisms before more
local separation lemmas, quantum implementation or finite sweeps.

Independent comparison also rejected the specific GI anchor/refinement
and supersingular endpoint-path amplification wrappers: when their
quantum alpha^(-1/2) clock is polynomial, the same classical alpha^(-1)
clock is polynomial. This is not a no-go for other quantum mechanisms.
Actual GI baseline and a current unrestricted-isogeny preprint comparator
were checked with their scopes; neither wrapper is admitted. The next
selection must supply a new paid constructive operation, not another
nearby barrier or search wrapper.

STRUCTURED_EDCP_KLEIN_DUALITY_AUDIT.md Section10 alone has independent
core and actual-text review ACCEPTED; older sections keep their prior
review status. This pass compared distinct lattice, code-equivalence and
sparse-root mechanisms. The selected concrete question was whether coherent
Gaussian pair averaging could remove the public-basis source bottleneck.

Exact law: two paid probability-width-s copies, after measuring u=x-y,
give a widtht=s/sqrt2 Gaussian on L+u/2. Centered output onL has mass
rho_t(L)^2/rho_s(L)^2, order2^-n above smoothing. Actual ADRS Lemma3.4
already gives the classical exact combiner; its squared-coset weights and
multilevel costs must be retained. Z with oddu is the exact counterexample
to treating every branch as centered. Fresh copies do not supply a source
inverse for amplitude amplification.

A constructive all-branch correction uses the PUBLIC Babai residual
of u/2 modL, bounded by R_B=.5sqrt(sum_i||b_i*||^2). Its exact Gaussian
overlap gives trace error<=sqrt(pi R_B^2/(2t^2)+4epsilon) above smoothing.
The review fixed a real wording defect: use translation-equivariant
floor(x+1/2) rounding; merely deterministic ties can break coset invariance.
For tau<=1/4, t>=sqrt(pi)R_B/tau and epsilon<=tau^2/8 suffice. This is
a sufficient regime, not a lower bound outside it.

Measured corrected outputs have EXACT classical averaging/rounding
counterparts. More strongly, direct coordinate-Klein sampling from the
same basis has normalization-tail sum E<=2exp(-a)/(1-exp(-3a)),
a=pi t^2/sum g_i^2, and TV<=exp(4E)-1 forE<=1/4. It already samples
the proved correction regime. No arbitrary coherent measurement is
classically simulated by this statement. Binary-tree iteration also
charges2^k=(s_initial/t_final)^2 input copies and error recurrence
error_(j+1)<=2error_j+tau_j. No BDD/LWE algorithm or separation follows.

No Gaussian implementation or finite sweep was run. The code-orbit Gram
proposal retains its1/n! normalization and has no decoder; computing its
entries by rank is not a coherent dequantization. Sparse-root literature
supplies a q^(1/2+o(1)) trinomial baseline; growing-term hardness is not a
fixed-trinomial or quantum lower bound. Neither alternative was admitted.
Next work needs a distinct explicit native mechanism, not another cooling
wrapper, source-boundary note or finite width experiment.

ODD_GALOIS_CLASS_GROUP_COMPOSITION.md Section6 and its Selmer integration
have independent core and actual-text review ACCEPTED. For explicit
MAXIMAL ORDER input of ANY odd degree n, the WRITTEN unconditional
bounded-error quantum class-invariant composition has clock
poly(b,n!,logD,log1eta). Numerical n! is charged: it is polynomial at EACH
FIXED degree, not uniformly in growing nonnormal degree. The earlier
Galois ODD-degree theorem retains its stronger poly(b,n,logD,log1eta) bound.
No supplied class generators, units, class-membership oracle or constructed
Hilbert class field. No novelty, separation or quantum execution claim.

Actual original Stark1974 Lemma8 p145 gives a quadratic subfield INSIDE K
if a real zero lies within1/(4n!logD) of1. Odd degree excludes that
subfield. A PRINCIPAL exceptional zero may still exist in the wider
Chebotarev region; it is allowed. For logX=A n!log(Dn^n), the exact
derivative of Li(t)-Li(t^beta) gives a constant-fraction dyadic increment.
The same h-independent outside-proper-subgroup count survives endpoint
errors, higher residue degrees and ramification. The existing raw integer,
primality, finite-algebra factorization and padded-slot source then pays
high-probability complete generators; it gives no completeness certificate.
One complete compact S-unit valuation lattice, SNF and canonical-list
majority finish the class-group composition. A is effective but no numeric
sampler setting or practical source implementation is claimed.

ELLIPTIC_TWO_SELMER_COMPOSITION.md is now unconditional for EVERY retained
monic irreducible separable binary cubic f, including non-Galois fields.
Here n!=6, the maximal order is already paid, and the random class primes
have polynomial-bit norms/list size. T=S_bad union S_random replaces the
GRH factor base. The complete compact T-unit/mod2 kernel, small squareclass
representatives and local/real clocks are unchanged. The correct integer
dimension has per-run probability>=2/3-1/20-1/100>1/2 before whole-run
majority. Actual SiksekSmart1997 already gives the polynomial classical
descent reduction; this is composition of published machinery. No MW rank,
points, covering curves, novelty or quantum execution claim.

Previously certified cyclic-cubic C2xC2 and Selmer/dyadic controls are
reused; no new finite test was run for an analytic zero-gap extension.
Strong classical ERH subexponential class/unit computation remains the
comparator. General quadratic/CM/L0 source assumptions and inverse-norm
class coverage remain open. End-of-pass independent comparison admitted
NONE of random-norm factors, imperfect Hankel decoding or Bell full-law
inversion: each lacks a concrete coverage/decoder step. These are open
obligations, not hardness. No implementation or sweep is queued. The next
pass must compare a distinct native mechanism before returning to these
gaps; uniform poly(d,logp) character reconstruction remains a motivated
target but currently has no admitted new operation.

Independent Bell triage is recorded in HIDDEN_FIELD_CHARACTER_ADMISSION.md
Section7: correct joint/conditional amplitudes retain zero-padding terms;
all public bilinear Fourier moments are tiny corrections to p^-rank(R).
No hidden-field decoder or full-law no-go follows, and no sweep is queued.
Next work needs a concrete source/measurement/decoder selected against
independent directions, not more nearby variants or implementation wiring.

The preceding all-packet Hankel falsifier remains reviewed: for every
irreducible degree-d target and2d-1<=m<=p, all consecutive moment windows
have success<=(3/2)d^-d, even on arbitrary weighted/ancilla split-supported
states. Other measurements and imperfect-outcome joint decoding remain
open. OPI anchor-plane scoring is paid, but adaptive higher tails and
first-witness quality remain open; its F8 algebra control is complete.

The preceding ELLIPTIC_TWO_SELMER_COMPOSITION.md local/global reduction
remains core/actual-text reviewed; the current source extension removes
its former class-generator GRH premise for exact dim Sel2(E/Q).
Paid compact T-units, mod2 valuation kernel and local/real clocks are
explicit. Actual SiksekSmart1997 already gives the polynomial classical
descent reduction, so this is composition of published machinery, not a
new mechanism. Existing x³-2 and dyadic-tail controls remain complete;
no MW rank, rational points, covering curves or quantum execution.

UNCONDITIONAL_CLASS_GENERATOR_ADMISSION.md Section5 remains reviewed:
a CLASSICAL factored inverse-norm ideal sampler with TVepsilon and
poly(field input,n,B,log1epsilon) clock at s=1+1/B. Independent Kalai
streams pay the source; numerical B is charged. CLASS COVERAGE is unknown,
so no unconditional complete class-group algorithm. Stronger classical
ERH subexponential class/unit arithmetic remains the comparator.

The preceding L0 results remain intact. Section9 of
FIXED_ORDER_DIRICHLET_L0_RECONSTRUCTION.md gives unconditional CLASSICAL
nonreal L1 approximation, now the preferred analytic step. Dyadic sampling,
periodic tails, effective NONQUADRATIC lower bounds, numerical precision
and confidence are paid; the exact p13 normalization falsifier is complete.
The exact-L0 composition still assumes class-arithmetic GRH. For q2power,
public H gives poly(q,H,logp,log1eta) on h(F+)<=H; all-input
poly(q,h(F+),logp,log1eta) is EXPECTED, with cap U=(2q)^(4q) and strong
h-error amplification. Numerical h is not logh. Fixed-q C(q)*polylogp
remains; no Weber/general polynomial-h/quantum execution claim. Certified
q8,p41 control covers only index1. The odd-minus higher-residue-degree
obstruction and normalized character criterion retain their scoped proofs.

Section9 of QUARTER_FACTORIAL_QUARTIC_ARITHMETIC.md records two narrower
reviewed findings. Relative to ALREADY PAID (Fhalf,Hmod16), the needed
L0 residue mod4 and canonical quarter-factorial are polytime equivalent;
renaming the residue supplies no algorithm. Reducing the integral ODD
Gaussian ideal mod4 yields the unit ideal, but RAW PRESENTATION ENTRIES
may retain information. No general classical lower bound. Actual
Louboutin/Chocian theorem scopes were checked; an independent curve-zeta
proposal was already Kedlaya, so no new subsystem was admitted.

The earlier quarter-factorial composition remains reviewed for p5mod8.
Its preferred two-field version reuses the real block for both Fhalf and
H=h(-4p)mod16 through Kaplan-Williams, with JOINT-pair amplification,
and Matthews's classical quartic Gauss phase. Existing p13/101 controls
catch missing2-factor and wrong conjugation. No quantum execution or
general-prime extension is claimed.

The preceding half-factorial composition remains reviewed: every binary
prime p, polynomial(logp,log1eta) bounded-error quantum time under GRH.
HALF_FACTORIAL_COMPACT_ARITHMETIC.md pays complete compact units, primitive
positive generator, ramified residue and the shared success event. Eight
certified classical controls remain complete. Both compositions use
existing quantum primitives; no separation or novelty is established.

The preceding pass rejected two concrete mechanisms analytically, with
independent actual-note review. An explicit mixed tensor of total order
d<p-1 whose exact finite stabilizer is GL(U)xGL(W) exposes its decomposition
by derivative linear algebra and a two-dimensional commutant. This closes
THAT source proposal for the prior Levi oracle algorithm, not high-degree,
succinct-circuit or opaque inputs. Gaussian Fourier linearization for
public MQ exactly retains alpha times the original solution density;
separated squares give an immediate classical counterexample. See
LEVI_TENSOR_AND_MQ_ADMISSION.md; no new scan or subsystem is queued.

The prior unbalanced-Levi WRITTEN oracle algorithm remains independently
reviewed for r>s>=1,p>=128(r+s), with O(n log1eta) coherent calls and
O(n² log1eta) total evaluations. The stronger WRITTEN classical baseline
uses O((p^(3s/2)+r p^s+n²)log1eta) chosen queries. Both have paid clocks
and exact-on-success certificates; neither full pipeline was executed.
The p3n3 algebra control is complete. The opaque source remains essential;
no externally motivated non-oracle source, novelty or speedup is established.

The preceding independent proposal, composing uniform RSK-preimage
permutations to sample normalized Kronecker coefficients, failed its FIRST
exact test: n4,lambda=mu=22 gives total-variation error1/2 and positive
mass on forbiddenshape31. Independent Sage and parent hand calculations
agree. KRONECKER_RSK_COMPOSITION_TEST.md records the witness and full law.
No general classical-sampling lower bound or quantum claim follows. No
larger scan or implementation is queued; re-rank constructive directions.

The preceding pass establishes an independently derived and actual-text
reviewed WRITTEN classical chosen-query algorithm for every monic squarefree
degree-d Q over explicit K=Fp^r, r>=2, p>=65536(rd)^2. Two translated
prime-subfield norms, decoded by the actual Kopparty theorem, recover Q by
gcd in O(p log1eta) sign queries and polynomial(p,r,d,log1eta) bit time.
Every non-ABORT output is exact; ABORT<=eta. This is polynomial in combined
description/output length when p is polynomially bounded in r,d, not
unrestricted polylogp, binary-degree, passive or phase-copy recovery.
EXTENSION_CHARACTER_NORM_GCD_RECOVERY.md contains the paid construction.
One bounded F49 algebra control completed; it computes norms from hiddenQ
only for diagnosis and does not execute the native decoder. Independent
integral-conjugacy selection was already covered by BHJ Corollary9.16;
the RSK-composition alternative is now falsified as above. No novelty, universal
PRF break, practical security or quantum execution is claimed.

The preceding pass compares a different native weighted-moment receiver
and an independent classical-stream oracle-sketch route. Both were tested
analytically before implementation. WEIGHTED_MOMENT_CHARACTER_ADMISSION.md
passed independent actual-text mathematical review; the parent independently
rederived the calculations and checked the primary source.

For EVERY irreducible degree d=2m-1>=3, direct weighted-moment coefficient
readout has exact conditional probability binom(p,m)/[p^m(p-1)^(m-1)],
already1/(2p) atdegree3. This rejects only that readout, not other uses of
its outcomes. The known fixed-degree native receiver is stronger. No code
or scan is queued. The independent oracle-sketch proposal requires classical
sign labels and O(p Q²/epsilon) samples; phase copies do not supply labels.
Its raw M coordinate-phase updates on|+> have target fidelity at most
min(1,[(d-1)/sqrtp+2M/p]^2), for every realization and on average. This is
only that update model, not a general structured-learning lower bound.
The source's quantum memory advantage remains outside this rejection.

The preceding pass tests the CM elliptic-product classical shortcut for
native cubic Gauss phase. CUBIC_GAUSS_ELLIPTIC_PRODUCT_ADMISSION.md passed
independent actual-text review. Ito already makes the canonical elliptic
factor explicit, but its representative-product alpha remains unpaid.
A full-kernel norm only returns the cube; Tal's arbitrary factorial theorem
retains a sqrt(p/q) term. Four exact finite Sage controls pass, with no
geometric Ito product, elliptic or quantum execution. No classical hardness
or new algorithm follows. Do not build a CM wrapper or larger sweep.

The preceding pass corrects a false universal density-one lattice exclusion
and tests an actual Gaussian preparation proposal.
DCP_HALF_CENTER_DGS_ADMISSION.md Sections1--6 passed independent derivation
and actual-text core review. Correct half-center geometry has ONLY Boolean
closest points when a witness exists; signed parity was dropped by the
legacy exclusion. Exact mean closest-list size is1 on uniform targets,
2-2^-n on uniformly planted targets, not exponential.

A GIVEN-target Gaussian with sigma²<=2pi/log(32n) would return a binary
witness with average probability>7/16 (independentuniformT) or>16/17
(uniformlyplantedT), before TVerror. This is CONDITIONAL on preparation.
The specific conservative zero-centered theta envelope has actual herald
<=(17/16)(8/n)^(n/8); polynomial standard amplitude amplification cannot
pay it. No general DGS lower bound or efficient subset-sum/DCP algorithm.
The legacy note now warns explicitly; one-record preserved quarantine is
queued. Exact n3D8/n2D4 controls and one native n8D256 LLL/GS-nearest-plane/
provedCVP control passed; finite-only. No quantum or Gaussian execution.
The independent CFT rim-hook recursion fails already atlambda21; joint
sampling is not ruled out. No further subsystem or sweep is admitted.

The preceding bounded pass tested a concrete classical OPI Gibbs sampler.
SCALAR_OPI_GIBBS_LINE_TEST.md is actual-text reviewed: for ORIGINAL IID
balanced FULL tables, a fixed positive-temperature field-line heat bath over
a polynomial PUBLIC direction catalog has exponentially small stationary
exit and exponential worst-start mixing (fixed random scan). The weighted
MDS variance pays the exact native/planted change of law. No first-witness
bound, general classical lower bound or rejection of the published adaptive-
basis annealer; no implementation/sweep. Independent surface, arithmetic,
Singer and relative-transduction comparisons admitted no new operation.
Do not continue this mixing restriction or field recognition by inertia.

The preceding candidate has an independently actual-text reviewed
WRITTEN classical baseline for hidden field norm characters: chosen-sign
O(p n log(n/eta)) queries and poly(n,p,log1eta) work, p>=65536n². A public
field from one irreducible sign line plus Frobenius alignment reconstructs
normalized multiplication and the projective norm. No polylog-p classical
or new quantum receiver; the high-p pipeline was not executed.
HIDDEN_FIELD_CHARACTER_ADMISSION.md is authoritative.

The same admission check found a false retained Singer exclusion. Known
Hayashi--Kawachi--Kobayashi bounds give Theta(n) standard mixed coset copies,
not Omega(n²). Subfield elements refute all-nonscalar irreducibility and
the no-parabolic-elements claim; scalar pairs refute the universal classical
collision bound. The dimension-derived gate lower bound is withdrawn.
The old note now warns explicitly; single-record quarantine is queued to
Gemini with its exact hash. No efficient Singer measurement is supplied.
One F81 subfield/intersection control and a native n3p3 Groebner attack
completed; all39 finite candidates recover the same norm and field algebra.

The preceding bounded independent comparison admitted no new operation:
the native Gauss lift still needs unpaid additive-phase access, while
2609.20771v1 Theorem1.2 already supplies classical poly(n,K) PFR under
uniform-sample AND membership access. No new implementation is queued.
This is proposal triage, not a general quantum lower bound or a copy-only
classical simulation. The preceding independent pivot gives an ACTUAL-TEXT reviewed WRITTEN
classical algorithm for every single cycle-count marginal of the character
ROW law chi_lambda(nu)^2/z_nu, for every explicit lambda of n. Exact formal
Slater determinants and binomial inversion run in polynomial bit time.
They compute the SAME pointwise L_lambda=-Elogz used in the published CFT
entropy application, with its logp(n)=O(sqrt(n)) bias plus numerical epsilon.
No joint sampling/entropy, exact Delta S, QCT/column/HSP simulation or
novelty claimed. See CFT_CHARACTER_MARGINAL_BASELINE.md.

Its reviewed hook-count corollary proves -Delta S<=sqrt(2n) H_n logn=o(n)
uniformly over all lambda. This limits extrapolation of the paper's
finite n<=30 linear fits, without contradicting the reported data or
quantum algorithm. Five exact Sage controls match independent character
arithmetic; wrong bosonic scale and unpaid finite window are rejected.

The preceding reviewed WRITTEN algorithm reconstructs every symmetric
determinant det(LA), arbitrary invertible L on Sym_n, n>=3, from fresh exact
GLOBAL padded-character copies. For p>=256[binom(n+3,4)+n+1], copies
O(n^4 log1eta) and poly(n,logp,log1eta) time/space. Its native classical
complete-line/Jordan baseline costs poly(n,p), for p>=65536n², and is not
executed. SYMMETRIC_DETERMINANT_CHARACTER_READOUT.md. The latest source
check finds no bridge from published Legendre MQ, whose diagonal quadrics
are public. No external native application, novelty, separation or
univariate/full-matrix extension is supplied.

The prior independent arithmetic pivot found Tal's September2026 classical
paper already solves exact repeated J_a and modp,p² in poly(q,logp), every
q|p-1,1<=a<q, compatible character/prime. Composite/even/noncoprime cases
are covered; no composite phase opening remains. Planned controls were
cancelled. JACOBI_GROUP_RING_RECOVERY.md retains the reviewed alternative
full-group-ring proof and the stronger prior-art/source boundaries.

The preceding Kloosterman and determinant admission checks found no new
paid receiver. Kloosterman spectral normalization and character-label costs
persist. Direct determinant Fourier labels are O(1/p) from uniform,
requiring Omega(p) measured copies for constant binary advantage. Neither
is a general algorithmic impossibility. No quantum subsystem was built.

The latest independently reviewed WRITTEN composition reconstructs
EVERY affine quadratic F=x^TAx+2b^Tx+c with invertible A, n>=3, from fresh
exact GLOBAL padded-character phase copies, up to one nonzero scalar.
One/two random measured coordinates and paid slice homogenization produce
one shared polynomial-matrix relation; no selected-slice source is supplied.
For p>=256T, T=binom(k+2,2)r(r+1)/2=O(n^2), all resources are polynomial
in n,logp,log1eta. Both parities, arbitrary b,c; no singular-A/n2/noise or
small-prime claim. No novelty, separation or quantum execution claimed.
See AFFINE_QUADRATIC_CHARACTER_SLICE_READOUT.md.

The prior toric point-count pass classically matches Maeda--Yano2608.23929
accuracy on odd-characteristic Newton-nondegenerate explicit bounded Laurent
support; general s>rho degenerate inputs remain UNKNOWN. That source is
explicit, not an unknown-polynomial character oracle. No Pila execution.
See TORIC_POINTCOUNT_ACCURACY_BASELINE.md.

The preceding independently reviewed WRITTEN result reconstructs an
unknown nonsingular quadratic form projectively from GLOBAL pure padded
character copies in poly(n,logp,log1eta), for oddn>=3,p>=16n^2. Fourier
dual-cone sampling and public linear algebra pay the receiver. The oracle
upper bound was already a univariate corollary; the source-only distinction
is explicit. No novelty, separation or quantum execution is claimed.

The earlier independently reviewed univariate quantum reconstruction
bound is UNIFORM exp(O(d logd))*poly(logp,kappa^-1,log1eta), for every monic
SQUAREFREE degree-d polynomial, d>=2, at a polynomial prime threshold.
Fresh native padded Legendre phase copies suffice; ONE fixed corrupted
sign function with rho<1/4 is also covered, kappa=1-4rho. A 2d-1-copy
coefficient receiver supplies one decodable Hankel moment vector. The
factorial degree cost remains. An independently reviewed packing theorem
now bounds this SAME Fourier/Hankel receiver by d^-d even after arbitrary
split-support reweighting/rephasing. This route is independent of the older
quadratic GL2 route. No poly(d) efficiency, quantum execution, novelty
or separation is claimed.

## Now

- **Rees, rest of 11-09 (AI only, pending human review).** (i) Non-unique encodings: HSP for
  arbitrary H still works (normal H was IMS Thm 8); acquiring the chart needs Omega(sqrt p)
  identity tests (2026-11-09-rees-nonunique-encoding-blackbox.md). (ii) Local paper patch,
  passes 6-7: hostile-referee fixes applied; NEW prop:dl-central-scalars (DL automorphisms
  scale the centre only by +-1, char != 2; refereed CORRECT, Groebner check p = 3..11);
  thm:bb-envelope exponent > p no longer conditional on ring-to-field(iii) (Schedule 2 has
  worst-case bounds on every oracle; refereed CORRECT after 4 tightenings)
  (2026-11-09-rees-dl-scalars-schedule2-referee.md). (iii) Mechanical queue: all top items
  DONE except the kappa=5 p <= 2628 table (now osc-k5/summary.out to 2311; 2521, 2621 left).
- **Rees deep checks (11-09, AI only, pending human review).** (i) Hostile referee of the
  integrated core (prep tree): MINOR, no break; Ivanyos-Santha import matches the source; one
  Dixmier-Lister scalar check timed out (UNKNOWN); significance risk at STOC
  (2026-11-09-rees-core-hostile-referee.md). (ii) Black-box exponent p^e, class < p: removable,
  conditional only on Thm is-import, via the Ivanyos-Sanselme-Santha 2012 route (not new);
  5359/5359 subgroups recovered. Owner 9 Nov: claim it; added to the local paper patch as
  cor:black-box-pe (credits ISS 2012; thm:bb-envelope wording left for the integrator)
  (2026-11-09-rees-exponent-pe-blackbox.md). (iii) Native application search 2: none found;
  best survivor (Legendre-masked unipotent symmetry) is constructed
  (2026-11-09-rees-native-application-search-2.md).
- **Rees black-box corollary (11-09, AI only, pending human review; paper NOT edited).**
  Draft audits/reviews/2026-11-08-rees-blackbox-corollary-draft.tex, revised after an
  independent referee (MINOR, no break) and a citation check. Exponent-p black-box p-groups of
  class c < p with unique encoding reduce to Thm main (conditional on Thm is-import; not Las
  Vegas; worst-case queries poly(l)). Finite control: 5 groups, all subgroups recovered.
  Owner decisions open: whether it enters the short paper; referee finding 7 (core uses
  full-version lemmas). Paper pass prepared locally (2026-11-09-rees-paper-pass-prep, gitignored).
- **Repo (11-09).** Only `main` exists, locally and on GitHub. Paper drafts, outreach 04/05,
  third-party texts/PDFs, claude_inputs, >10 MB outputs are gitignored (local only).
- **dfs2b queue FINISHED (11-10, AI only, pending human review).** E_2(8) is DETERMINED: 293
  primes, largest 14281 (1.23 kappa^4.5); all 556 primes = 1 mod 8 up to 20000 decided, none above
  (explicit-contraction sweeps). E_2(9) known only up to 25000: 414 members, largest 24967; 1295
  listed exceptions above 25000 and (9^9/2, T_A(9)] still open. Non-members 21871, 22051, 22303,
  23671, 24841 have witnesses checked by an independent verifier and PARI (530 witness lines, 0
  bad); every plain-mode cross-check INFEASIBLE. Report audits/reviews/2026-11-10-rees-dfs2b-queue-final.md.
  Paper pass APPLIED locally to docs/papers/rees-hsp (core 35 pp., companion 211 pp., clean);
  backup in the gitignored prep folder. The Ivanyos personal-communication sentence is still not in.
- **Rees SDE open directions (11-08, AI only, pending human review).** (i) p = 3, worst-case
  F_3^n subset sum: PROVED deterministic poly time at n²/4 + O(n^{3/2}) vectors (KOW: n²/3);
  proof referee no gap, break attempt no failure, no prior source found; beats KOW's explicit
  bound only for n > 80. (ii) Prime condition: o(a²) whenever p/a -> inf (F = O(a²/min(log a,
  log(p/a)))); an a-independent threshold needs open Q-loc; nothing at bounded p. (iii)
  Near-linear: only promise-problem hardness below ~2a (Legendre PRF); total regime untouched.
  Handoff entry "2026-11-08 Rees SDE Open Directions". (iv) F_q (11-09, AI-refereed): p = 5 at
  n²/4 + 3n/2 + 2 (Theorem B′); (1−1/p)a²/2 + O(a log a) at every odd p (κ = 2); no
  two-dependency gadget at p = 7, 11, 13 (LRAT-verified at p = 7, 11 with the fixed checker; p = 13 CaDiCaL UNSAT,
  not independently proof-checked, 9 Nov checker fix). Handoff entry "2026-11-09 Rees SDE F_q Referees".
- **Rees SDE worst case below a² (11-07, AI only, pending human review): Theorem A.**
  Every bank in F_p^a with D_J(a)+O(Ja) columns, J = ceil(log_kappa a), fixed kappa, is solved
  Las Vegas in poly(a, log p) time at p >= ~72 kappa^2 a^6 J^2: O(a²/log a) columns, versus
  the previous (a+1)(a+2)/2. The new step is the Rado flat (matroid-intersection certificate),
  which removes Q1's heavy stalls. Fable referee: CORRECT; independent reimplementation: no
  break. A piece-scheme barrier (argued) says Theta(a²/log a) is this family's limit. Not
  uniform in p; the paper still says (a+1)(a+2)/2 (owner decision). Handoff entry
  "2026-11-07 Rees SDE Worst Case Below a²".
- **Current Gaudin gap: uniform1/N floor REFUTED, weaker polynomial gap OPEN.**
  Explicit distinct rational two-cluster sites with polynomial conditioning
  have squared joint separation<=2312n^-5/3,N=2n. Reviewed finite-spacing
  fusion and two-tent min-max prove the family, not numerical extrapolation.
  Exact128-site certificate<1/400<1/128. Known BCS critical mechanism; actual
  accepted source leaves general SAME-sector gap open. Two CLOSED reviews;
  no superpolynomial gap, general preparation no-go, novelty or separation.
  Conditional preparation remains viable if a weaker all-path polynomial
  bound can be paid. Independently reselect; no nearby scan/filter/backend.

- **Prior binary-Fock Kerr: prior-art quantum endpoint, restricted classical match.**
  Full native passive/Kerr circuit sampling is a known written quantum
  poly(nativebits,logK,log1epsilon) construction. A reviewed coherent-branch
  classical sampler matches BUNCHED input when numericalchi is polynomial;
  binary binomial/precision/finite clocks are paid. Exact mixture TV1/2 and
  CZ/parity controls separate interference from dequantization. Three CLOSED
  reviews and one frozen exact control; no novelty/separation/execution.
  Independently reselect; no optical backend or nearby low-branch variant.

- **Prior Gaudin traversal: conditional operation paid, native gap OPEN.**
  Known joint-charge randomization removes classical target-label tracking;
  dimension-free error and finite clocks/precision paid. The new two-cluster
  family refutes uniform1/N; a weaker inverse-polynomial gap remains OPEN.
  Two CLOSED reviews. Only averaged initial-label branch preparation under
  explicit gap/resource promises; no full algorithm/separation/execution.
  Re-entry needs a bulk gap inequality/counterexample, not more Zeno plumbing.
- **Prior spinor admission: local dyadic gate paid; full native route PARKED.**
  Classical polynomial-BIT ternary spinor generators via bounded goodBONG
  repairs and Hilbert/filtration linear algebra; no squareclass enumeration.
  Exact same-genus/nonisometric3-neighbor family refutes ordinary-Cl reuse.
  Global ambient/support and local transporter offsets remain OPEN. Two
  closed reviews/two finite controls; no full algorithm or separation.
  Both API calls empty (refusal/truncation), no findings/retries. Independently
  reselect next; only a paid native transport operation reopens this route.
- **Prior Bethe prefix route: direct determinant shortcut FALSIFIED.**
  Valid rational Gaudin eigenstate, exact4/9 prefix-norm discrepancy and no
  single common one-hole dual. Full preparation remains OPEN. Source/core
  reviews CLOSED, exact classical control PASS. A classical ALL-prefix
  oracle would also pay sampling and sparse-observable estimation. One
  Claude repair ended ReadTimeout/EMPTY, no findings/retry, billingUNKNOWN.
  One-site marginal baseline is paid; scoped checkpoint closes the pass.
  Independently select a new operation; no further Bethe variant queued.
- **Prior local saturation: finite quotient and kernel structure proved;
  native finite precision OPEN.** Controlled residuals moduloE=2L allow exact
  finite presentations. Bounded Stoll nullity isg-j+1; Smith-kernel precision
  isN-K, monic normalization can lose2lambda. Prior all-prime polynomial
  iteration bound retained. Complete local/global algorithms unadmitted.
  Closed source/core addendum; one exact new control and precision falsifiers,
  no old reruns. Claude completed Howell/empty certificate, both terminal;
  estimateUSD2.110246, cumulativeUSD57.237428 is NOTbalance. Independently
  reselect next; only a paid finite HALF interface justifies continuing here.
- **Prior compact integral similarity, written composition complete:**
  arbitrary growing binary A,B; NO or compact integer unimodular intertwiner;
  polynomial quantum BIT/gates under conservatively retained GRH. Known BHJ
  algorithm, with paid compact descent, residue, lattice-section and small-
  determinant joins. Two closed reviews and one exact classical control.
  Classical arithmetic baseline unchanged; no novelty/separation/execution.
  Claude estimateUSD1.093082; cumulativeUSD51.757902 is NOT balance.
  Independently select next by external value; no nearby variant/backend.
- **Prior folded-chain coherent evolution, written proof complete:** all
  open-boundary sectors are encoded reversibly from arbitrary quantum input;
  controlled free-path evolution costs poly(N,bitlength(t),log1/epsilon).
  Source/core reviews and one exact classical run close the written contract.
  Specified eigenstate and computational-basis readouts are classically matched
  by determinant sampling and CT estimators. No novelty/separation/execution.
  Keep native hopping -1/2 despite the source energy-formula discrepancy.
  Two Claude calls cost an estimated USD1.223514; empty truncated report gives
  no evidence. Independent next selection; no backend/periodic variant queued.
- **Prior quintic-surface P2, written proof complete:** every smooth
  quintic/Fp fromnativebinaryinput, fixeddegree, bounded-errorpolylogp quantum
  exactP2. Recomputedgeometry/arithmetic/source/CRT/finiteclocks accepted in
  twoclosedreviews. ActualSchnell/Deligne obstruction is KNOWN and concerns
  verygeneralCOMPLEX Hodge-compatible abelianreplacement only. Otherclassical
  algorithms/specialFp cases remainopen; no separation/novelty/execution.
  Fiveprimarysources and exactclassicalcontrol, correctedtrace/coefficient
  labels(+8/-8 for58F7points), no fullP2control. OneClaude report .512620USD;
  aggregate49.441306USD/64estimates is notbalance. Independentlyselect next
  externallyvaluableoperation; no nearbydegreevariant/backend/sweep.
- **Prior quartic P2 reduction, written proof complete:** fourclosedreviews
  pay fixeddegree nativequantum bound. Stronger Clifford-marked/arithmetic
  Kuga–Satake classical route remainsviable/open and was suggestedbyElkies1997.
  Formal spin collision isnot a realizedK3pair; no novelty/speedup/execution.
- **Prior two-Gaussian-channel learner, complete:** reviewed written uniform
  polynomial-use/BIT/gate diamond learner for everyexact two-map mixture.
  Productinput/localPauli measurements match all data; no computational or
  coherence advantage, implementation or practicalcost claim. Fiveclosed
  reviews/sixsources/exactclassical control remain authoritative.
- **Prior arbitrary-CSA minimal module, complete:** reviewed WRITTEN
  quantum polynomial-BIT compact primitive idempotent and minimal ideal/action
  under explicit GRH. Classical factoring-only-oracle index + prescribed
  degree-d field + existing KM split map + compact Hom/affine extraction.
  Exact positive certificate verifies index separately; passing ranks alone
  cannot establish primitivity. Two closed reviews/eightprimary sources/one
  exact classical control; PARI arbitrary-table index unsupported, no hardness.
  Two useful Claude reports estimateUSD0.860428; no live call/retry. No novelty,
  separation, expanded/integral output, normal form or full/quantumexecution.
  Independent next mechanism selection; no arithmetic backend/nearby extension.
- **Prior stabilizer-span/minimum-rank separation, complete:** all-n
  counterfamily covers every positive weighted in-span frame. Algebraic tagging
  forces unique rank-minimal span and exponential coefficient cost; a slightly
  larger outside-span decomposition has polynomial cost. Exact-rank result is
  fragile to approximation; no learner hardness or globalextent lower bound.
  Closed source/core/addendum review, fiveprimary sources/two exact classical
  controls and two useful Claude attacks. No quantumexecution/novelty claim.
  Independent next selection, no conditioning/projection backend or sweep.
- **Prior reduced norm composition, complete:** reviewed WRITTEN quantum
  polynomial-BIT SEARCH under GRH, arbitrary growing explicit CSA/field and
  expanded target. Paid prescribed-field constructor and known split primitive
  feed REGULAR-module RIGHT transport; exact canonical construction certificate
  checks expanded Phi, small-atom LS relations and modular nonzero determinant.
  Three reviews/fourprimary sources/exact PARI/nondivision control complete.
  No novelty/separation, minimal-module, integral/short/expanded or execution
  claim. Two useful Claude reports estimateUSD0.766564; no live call/retry.
  Independently choose next mechanism, no integral/PIP/backend extension.
- **Prior relative norm composition, complete:** reviewed WRITTEN quantum
  polynomial-BIT exact compact N_L/K witness or NO under GRH, arbitrary growing
  explicit fields/maximal orders/embedding and nonrational target. Relative
  tensor support plus FULL torsion/LS relation endpoint paid; no closure.
  Actual sources and prior Simon endpoint retained; PARI control passed.
  No novelty/separation, integral/short/expanded or full/quantumexecution.
  Claude coordinate report checked; support call terminal ReadTimeout/no
  report, billing unknown. No retry or findings from it. Independent
  next selection; no multinorm/norm backend extension.
- **Prior mixed-Gaussian pair learner, complete:** reviewed WRITTEN
  uniform polynomial-copy/BIT learner for ALL exactIID mixtures of two mixed
  Gaussians, knownMajoranas/ordinarygates. No weights/branches/gaps supplied.
  Exterior-square inverse and lowrank Schur-core map with direct<=4Gaussian
  output close every case; allκ thresholds/error/finiteclocks paid. Three
  scoped reviews read, exact classicalcontrol passed; no full/quantumexecution.
  Prior stabilizerrank2 result and suppliedcomponent Wick baseline retained.
  Claude unfinishedprefix estimateUSD0.828720 gives no usableproof; no retry.
  No novelty,separation,offmodel,manycomponent or practicalclaim. Independently
  choose another native mechanism; no rankextension/tomography/CJ backend.
- **Prior wild-local Selmer admission, complete:** general endpoint PARKED;
  missing full local source/model BIT payments. Reviewed all-genus oddp
  counterfamily kills unramified curve-point traces alone, with explicit
  ramified degree<=g witness. Uniform-divisor rare-event example rejects
  that sampler only. Sixprimary sources and focused review, exact CAS control
  complete; source chain-length bound retained within actual scope. Two
  empty terminal Claude calls estimateUSD2.759310, no findings/retries.
  No fullalgorithm or general no-go; independently select another native
  mechanism. No regular-model backend or source-variant sweep queued.
- **Prior cubic covariant-processor pass, complete:** exact one-output
  r->r^5 and two-Bell instrument equivalence reject the specified six-copy
  receivers as new hidden-frame primitives. Copy/gate clock paid; original
  stabilizers unchanged and deep convolution approaches a mixed code state.
  Known GNW operation retained. Focused review, threeprimary sources and
  exact complex/Y/CCZ/cancellation control complete. One useful Claude audit
  USD0.327524; incorrect C^T C remark rejected. No general learner/no-go,
  novelty/separation or quantum execution. Original cubic learner PARKED;
  independently select a different native mechanism, no receiver variants.
- **Prior global compact isotropy pass, complete:** reviewed WRITTEN
  bounded-error quantum polynomial-BIT decision and compact isotropic point
  for all explicit growing-(degree,dimension) inputs, under GRH. Paid one5plane,
  quadratic ideal norms, finite/real approximation and arbitrary-splitting
  descent close the endpoint using known Amitsur splitting. Four reviews,
  sevenprimary sources and one exact classical/algebra control complete.
  Rational/special-field classical baselines retained; novelty UNKNOWN.
  No execution, expanded/short/integral point, compact Witt decomposition or
  GRH removal. Claude useful weakapprox audit plus emptyrefusal estimate
  USD0.707116. Next pass compares independent mechanisms, no adjacent backend.
- **Prior two-Gaussian learning pass, complete:** reviewed WRITTEN uniform
  polynomial-copy/BIT learner for all exact EVEN Gaussianrank<=2 inputs.
  Paid covariancegrouping/quarticpairing/catfallback, explicit errorhierarchy,
  known coherent MPS endpoint and fresh validation close endtoend learning.
  Four independent scoped reviews, sixprimary sources and one exactcontrol;
  no human/formal review, novelty/separation or execution claim. Two useful
  Claude reports plus two emptyterminal calls estimate USD5.559080. Keep the
  actual phase/precision classical baseline and known MPS priorart. Next
  pass compares independent native mechanisms before any extension.
- **Prior sparse-Fock torus falsifier, complete:** exact Paleyr=n family
  has a constant-gap u(1) quadratic stabilizer and passive-invariant complete
  degree2/4 moments. Known Cartan twirl pays the approximate-support bound
  for any U-independent polynomial list of passive completions, rejecting
  this generalization even at constant error. Source/structural/quantifier
  reviews and exact231-dimensional Gram control passed; degree6 data escape.
  General learning and non-passive/higher/joint interfaces remain OPEN.
  Claude useful audit estimate USD0.596230. Independently select the next
  native mechanism; no eigensolver/backend/sweep on this rejected route.
- **Prior two-Fock Gaussian learning pass, complete:** reviewed WRITTEN
  polynomial-copy/BIT learner for every exact sharedGaussian two-Fock
  state with fixed parity, knownMajoranas and arbitrary growing separation.
  Fourthcumulant spectral extraction plus uniform rounding and measured
  relativephase closes the balancedcat case; fixed4 and dominantGaussian
  candidates cover all other weights/separations. Actualsource/core reviews
  and exact7mode control passed. Classical Pfaffian baseline retained; no
  novelty/separation/general sparse/noisy/full or quantum execution claim.
  Two useful Claude reports estimated USD1.650348. Next pass independently
  ranks native problems before proposing any extension or implementation.
- **Prior general sparse algebraic-constant lattice pass, complete:**
  reviewed WRITTEN classical polynomial sparse-BIT Alg recovery for EVERY
  growingdelta native field. Implicit derivative coefficientbounds, full
  finite-congruence lattice and exactLLL prefix preserve fullgeneration.
  FullRel remains open at compactconstantrelations; Alg does not remove
  constants/torsion. Exact counterfamily rejects direct small-expanded-height
  rational specialization and naiveLC, without nativehardness/generalno-go.
  Core/counterfamily review and quarticcontrol closed; badp257 rejects a
  smallcharacteristic shortcut. Two empty terminal Claude calls estimated
  USD0.900988, no findings/retries. No nearby subclass/backend/barrier sweep
  queued; independently select the next externally valuable mechanism.
- **Prior hidden cubic phase admission, complete and PARKED:** copies-only
  unknown-Clifford occurrence2 cubic family has exact <=5-factor Bell
  constraints. Reviewed general factored-event gap2^-72 at d3,k5 pays
  simultaneous exclusion of false FACTORED equations; full K5 need not be
  exact and finding factors/phase frame remains unpaid. Scoped generic
  factor search with P(0)=1 contains graph4-coloring, no native hardness.
  Source/proof/reduction reviews and one classical K4 exact control closed.
  Suppliedf,C Bell sampler is polynomial; no learning/separation or growing
  product-width conclusion from six-qubit control. Two empty terminal
  Claude calls estimated USD2.350002, no evidence or retry. No further
  gap/width sweep or backend admitted; independently select a new mechanism.
- **Prior cyclic-support monomial descent pass, complete:** reviewed
  WRITTEN quantum polynomial-BIT compact torsor-point solver under GRH for
  explicit Galois splitting data and arbitrary integer G-action/cocycle.
  Primitive cyclic support reduction, paid numerical cutoff, complete
  compact S-units, LS full atom relations and integer solving close the
  endpoint. Deterministic positive verification retains all torsion.
  Core/source/coordinate/final reviews and one exact CLASSICAL cyclotomic
  control complete; optional log subsystem replaced by established methods.
  Classical S-unit/Hilbert90/conic baselines and substantial prior overlap
  retained. No novelty/separation, succinct splitting field, expanded or
  integral/short output, GRH removal or full/quantum execution claim.
  Claude estimate USD0.482402, one refusal and one useful report, no retry.
  No adjacent work queued; independently compare externally valuable mechanisms.
- **Prior tensor-square rational norm pass, complete:** reviewed WRITTEN
  quantum polynomial-BIT compact norm solver under GRH for arbitrary growing
  degree and supplied maximal-order table. Paired norm support proof is
  unconditional under its class-support assumption; D^(2n) pays polynomial
  support without computing any auxiliary field or closure. Complete compact
  S-units, gcd-free exact coordinates/sign and HNF close the native endpoint.
  Core/source/resource/final reviews and one exact control complete. Simon
  prior overlap and prime-degree/S_n HNP existence baselines retained;
  no classical witness counterpart established. Two useful Claude calls,
  estimated USD1.325932, with unproved runtime claims explicitly rejected.
  No novelty/separation, integral/short solver, GRH removal or execution
  claim. No adjacent work queued; independently compare new native mechanisms.
- **Prior arbitrary-Pauli learner pass, complete:** reviewed WRITTEN
  quantum-copy polynomial learner for exact unknown-Clifford arbitrary
  signed-Pauli pi/8 rotation on H^n, all supports. Largew interference
  deletion and canonical cubic geometry; smallw paid gap and direct global
  tomography; physical-axis correction and exact verifier on large branch.
  Zero-residual/stabilizer and approximate-output completeness guards fixed.
  Universal gap inverse ~1.35e16; no practical claim. Core/source/endpoint/
  integrated reviews and four-case exact control complete, no full execution.
  Both Claude audits useful, estimated USD1.432656. No novelty/separation or
  generic noisy/angle/MPS/channel extension; no adjacent work queued.
- **Prior one-rotation cubic Bell pass, complete:** reviewed WRITTEN
  polynomial learner for the exact Clifford-hidden full-Z-rotated H-product
  family. Complete cubic source, uniform Lie/square-zero/Macaulay algebra,
  n+1 correcting candidates, capped product learner and fresh-source known
  inverse verification pay approximate output. Source/core/final reviews
  and exact n4 identity/covariance controls complete; no coefficient search.
  Width n and pure-product distance bound are source limits, not hardness.
  Claude total estimate USD1.988864 (one useful, two empty), no retries.
  No full execution, novelty, separation or general noisy/MPS extension.
  No adjacent implementation; independent next native-value selection.
- **Prior good-dyadic growing-Selmer pass, complete:** reviewed WRITTEN
  bounded-error quantum polynomial-BIT DIMENSION for the exact explicit
  good-Z2/odd-Galois-factor/good-small-odd family, growing genus. Paid
  classical trace/shallow-formal local generation and exact nonsaturated
  O/8 coordinates combine with existing quantum global arithmetic. Separate
  sign units, complete-basis error budgets and atom-specific precision paid.
  Unbounded shifted Q x K x K family; strongest duplicate-field simplification
  does not remove complete unit/class2 information. Core/source/global/family/
  integrated reviews and one exact finite control complete. Claude estimate
  USD0.223688 (one useful, one refused), no retry. No execution, novelty,
  separation, arbitrary-curve or MW-rank claim. No adjacent implementation;
  independently rank next native mechanism before another experiment.
- **Prior large-prime local-image pass, complete:** reviewed WRITTEN
  classical polynomial-BIT basis of delta(J(Qp)) for monic odd d>=3,p>d,
  growing genus/arbitrary bad reduction. Paid tame extensions, discwise
  functional sampling, local orders and explicit precision; returned frame
  and rank certificate make every returned output exact, otherwise ABORT.
  Core/source/final review and one exact falsifier control complete. Claude
  coordinate audit useful; total four-call estimate USD6.767224, three empty
  calls with no findings/retry. No global Selmer, small/wild/dyadic, novelty
  or quantum execution. No adjacent implementation queued; independent
  native-value selection next. General small-order sparse specialization
  remains open; actual CIT does not supply the missing order bound.
- **Prior contraction baseline pass, complete:** reviewed source-based
  exact fixed-Q(zeta8) bounded-degree Boolean contraction in subexponential
  variable count and polynomial BIT space, with L>=n explicitly charged.
  Explicit H,T,CNOT one-amplitude reduction gives n<=2G; final actual-text
  source/bit/circuit review complete. One nontrivial-kernel exact control
  passed; Claude completed at estimated USD0.32692. No whole ETH-paper or
  sharper appendix acceptance, polynomial/qubit-count simulator, sampler,
  novelty or new quantum algorithm. Compare minimum applicable time bounds;
  no larger implementation or adjacent audit queued. Select a new paid native
  quantum operation by independent value before proposing another experiment.
- **Prior monomial Kummer pass, complete:** reviewed WRITTEN classical
  polynomial sparse-bit full relations at growing s,k,charged delta. Paid
  unimodular constants, compact leading coefficients, original-basis
  derivative/LLL kernel and LS pullback preserve all torsion. One exact
  delta6 binary-exponent control recovered Alg rank5/Rel rank3, with source
  and nonsaturation guards. No general f, novelty, separation, poly(logdelta),
  general LS/full-algorithm or quantum execution. No API or extension queued.
- **Prior oscillator pass:** exact pairing forces linear/affine structure;
  public square-permutation optimization is classical. Toffoli control and
  narrow review complete. Claude character request refused with no report,
  estimated$0.063892; no retry. Rectangular/nonlinear alternatives stay open.

- **Prior characteristic-zero sparse pass, complete:** reviewed WRITTEN
  quantum polynomial-bit full relations for explicit monic algebraic function
  fields, growing s,k,delta and binary sparse degrees. Full constant-relation
  bit bound and prime/content/source/LLL costs paid. Complete classical
  sparse-bit degree1 and degree2 counterparts; one exact binary-exponent,
  cancellation and bad-characteristic control. No advice, arbitrary ideal
  conversion, novelty, separation, reverse char0 DLog equivalence or execution.
  General classical complexity remains unknown; independent next selection.
- **Prior positive-characteristic sparse pass, complete:** reviewed WRITTEN quantum
  polynomial-bit exact relation lattice for explicit monic irreducible field
  presentations, with growing s,k,delta and binary sparse T exponents. Random
  finite specialization, full-ring HSP and exact LLL prefix are paid. No
  supplied inverse/divisor/constant/point advice or arbitrary ideal conversion.
  Independent classical reduction pays generators and nilpotents, giving a
  whole fixed-p quasipolynomial comparator from actual KW DLog. The native
  problem is randomized-polytime Turing equivalent to finite-field DLog. Exact native
  nonsaturation/collision and nilpotent controls only; no quantum execution,
  novelty or separation. Choose the next direction by independent value.
- **Prior affine-unit pass, complete:** reviewed WRITTEN classical
  polynomial-bit relation lattice for growing supplied unit tuples in
  fixed-variable PRIME affineQalgebras and characteristic-zero PRIME
  Z-domains. dlog plus finite specialization, actual LS source and all
  representation costs paid. Two exact controls; no complete-unit algorithm,
  full execution, quantum advantage or novelty. Next native operation must
  compete against independent directions, not follow by continuity.
- **Prior decoder-interface pass, complete:** chosen-BIT classical
  additive-mean and candidate-syndrome scoring matches; exact root-free
  syndrome/mask equality; full independent-mask law refuted; mostly-correct
  recurrence premise refuted. Complete joint-label decoding remains open.
  A polynomial SQ decoder could solve the native problem classically and
  would be welcome. No receiver implementation or extra sweep queued.
- **Independent next selection required:** full superlattice source has
  been checked; its record posterior is classical/exponential and not a
  clean inverse. Chosen-line multivariate interpolation inherits fixed-d
  cost. No nearby variant is admitted. Start with a distinct explicit paid
  operation, corpus/literature and strongest classical attack.

- **Uniform prime-index factorial, reviewed written composition:** EVERY
  odd primeell dividingp-1, unconditional quantum poly(NUMERICAL ell,logp,
  log1eta) for((p-1)/ell)! modp. Final resource, precision and actual-source
  checks are complete. Section10 removes ALL physical Gauss-phase calls:
  any consistent algebraic embedding suffices. Factoring and compact
  S-units remain quantum. Exact mismatch law k!*r^(d-b) and one ell5,p11
  control; no novelty, separation or quantum execution. The superlattice
  source audit above supplies no new polynomial coherent primitive.
- **Claude research agents integrated:** narrow paid reviews supplement
  parent derivation and primary-source checks; snapshots, costs and
  dispositions are durable. Default high; max exhausted budgets without
  useful final reports in these trials. Owner's provider limit is now$200.
  Latest recorded Opus audit refused without a research report; estimated
  usage$0.063892 for the character request, no retry. The earlier decoder pass used one completed
  Opus audit and one Fable refusal, estimated$0.57356. Refusals supply no
  research findings. These are usage estimates, not balance or invoice data.
- **One-third factorial composition, reviewed:** EVERY binary p1mod3,
  unconditional written quantum poly(logp,log1eta) for((p-1)/3)! modp.
  Complete compact S-units, exact class-module Fitting, known Gauss phase,
  classical L1 and integer Hilbert90/local residue are paid in degree3/6.
  One certified p313 control catches action, norm-sign and denominator
  errors; no quantum execution. Classical fixed-index/divisor comparisons
  checked in actual Tal source. No novelty or separation. Next selection
  must compare growing-parameter native mechanisms independently; no
  arithmetic extension or implementation admitted merely by continuity.
- **EDS character source characterization complete, reviewed:** full
  integer answers are exactly reconstructible from the even-coordinate
  sequence plus one anchor. F7/order13 gives a triple collision at p3mod4;
  F13/j7/order5 gives four and refutes the generic-j-only repair. A reviewed
  infinite p3mod8 family with fixed order7 also refutes the generic-j+p3mod4
  patch; growing-order and whole-prime-group scope is unchanged. Actual
  primary-source scopes checked. No efficient decoder admitted; PARKED
  pending a new paid operation or decisive attack. Compare independent
  native mechanisms before further separation analysis or implementation.
- **Gaussian pair cooling, scoped review complete:** Section10 of
  STRUCTURED_EDCP_KLEIN_DUALITY_AUDIT.md gives the exact shifted branch law,
  a sufficient all-branch Babai correction and its direct classical profile-
  Klein comparison. Use translation-equivariant rounding and charge the
  binary-tree copies/errors. No new lattice source/decoder was admitted;
  no Gaussian sweep or implementation queued. Compare a distinct native
  mechanism before returning to this route.
- **Selection after the constructive checkpoint:** independent comparison
  admitted no operation from random-norm class generation, imperfect
  Hankel decoding or Bell full-law inversion. Do not build these sources
  again or write another barrier note. Compare a distinct native mechanism
  by corpus, primary literature and the strongest classical baseline;
  reopening needs a specific paid operation with an end-to-end role.
- **Elliptic2-Selmer composition and priority audit, reviewed:**
  ELLIPTIC_TWO_SELMER_COMPOSITION.md now gives an UNCONDITIONAL written
  bounded-error quantum polynomial-bit dimension algorithm for ALL retained
  irreducible integral cubics. Reviewed Stark/TZ prime-source replacement
  removes the former GRH premise; compact parity and local clocks remain. Actual SiksekSmart1997 already supplies its polynomial
  classical descent reduction. Two scoped controls complete; no new
  quantum mechanism/subsystem, rank/point claim or quantum execution.
  Select a distinct native question before extending this arithmetic line.
- **Classical inverse-norm ideal sampling, reviewed:** the exact-law
  derivation and finite TV/bit clocks in UNCONDITIONAL_CLASS_GENERATOR_ADMISSION.md
  Section5 are accepted. Independent factored integer streams remove the
  need for Shor or a zeta-residue rejection factor. Class coverage at
  polynomial numerical B remains unknown; no unconditional class algorithm.
  The independently selected elliptic2-Selmer composition is now
  accounted for above. No sampler implementation or scan.
- **Unconditional classical nonreal L1 approximation, reviewed:** dyadic
  importance sampling plus periodic tail and an effective nonquadratic
  lower bound gives relative/log-magnitude/circular-phase accuracy delta
  in poly(q,logp,1/delta,log1rho). Actual-text integration accepted;
  exact p13 weight-omission falsifier complete. Preferred analytic step
  for L0/quarter-factorial; class arithmetic STILL uses GRH. No exact
  classical L0 or polynomial-in-logprecision claim. Numerical h remains
  in the uniform cost, and sampling confidence/freshness are charged.
- **Uniform index-dependent L0, reviewed:** Section8 replaces fixed-field
  precomputation by paid full-unit coordinates W_i=h B^+Log epsilon_i.
  Public H gives poly(q,H,logp,log1eta) clock on h<=H; ALL-input
  poly(q,h,logp,log1eta) is EXPECTED time under GRH. Numerical target
  accuracy still costs poly(h). Explicit cap U, bad-h amplification,
  compact precision/CRT and fresh whole-output repetitions are reviewed.
  No unrestricted all-q polynomial claim, Weber assumption, new code,
  novelty or separation. Existing q8 control covers only index1.
- **Fixed-order exact L0, reviewed explicit-input composition:** for EACH
  FIXED q2power>=4 and odd chi of prime conductor p, WRITTEN
  C(q)*poly(logp,log1eta) bounded-error quantum time under GRH.
  Gaussian-period field construction, complete class module/action,
  non-PID Fitting, exact2-part and fixed-field generator/unit/phase steps
  are paid. Core/source and actual-note reviews accepted. Sole certified
  q8,p41 control has a decisive skip-unit failure; no quantum/short-GRH
  execution, growing-q claim, novelty or classical separation.
  FIXED_ORDER_DIRICHLET_L0_RECONSTRUCTION.md records proof and limits.
- **Arithmetic priority boundary:** no further denominator extension or
  generic subsystem is authorized by the result alone. Compare a concrete
  same-input classical ideal operation against independent native routes.
  Relative quartic residue/sign equivalence does not itself supply an
  algorithm; reduced-ideal mod4 failure does not rule out raw-entry uses.
- **Canonical quarter-factorial, reviewed explicit-input composition:**
  p=5mod8 in binary, polynomial(logp,log1eta) BOUNDED-error quantum time
  under GRH. QUARTER_FACTORIAL_QUARTIC_ARITHMETIC.md pays the degree4
  integral basis, class module/action from one S-unit relation event,
  Gaussian Fitting ideal and character convention. Both L0 coordinates
  odd restore exactly1+i. The already-paid half-factorial supplies the
  signed prime in Matthews's classical Gauss formula; the unconditional randomized L1
  estimate selects the exact Gaussian associate with charged confidence, then interval and
  quadratic class-number identities select G among its two square roots.
  Actual primary sources and independent actual-note reviews accepted.
  Certified p13/p101 controls catch missing2-factor and wrong conjugation;
  no quantum or full canonical-unit-selection execution. No novelty,
  separation or extension to p1mod8/general factorials.
- **Shared real arithmetic removes a quantum call, reviewed:** actual
  Kaplan-Williams1982 Theorem1 supplies Hmod16 as h_R Tr(epsilon³)/2.
  Evaluate compact epsilon³ mod32O and amplify the JOINT (Fhalf,Hmod16)
  pair on the same complete-S-unit event. Only two number fields remain.
  Section8 core, source, uniform formula and actual-note reviews accepted;
  existing certified p13/p101 data give Hmod16=2/14. No new scan.
- **Output-specific classical question remains:** a direct mod8 class-
  number substitution flips the selected root when its lift changes by8;
  it does not pay the sign. The exact unresolved classical target is one
  coordinate of quartic L0 modulo4, not the full class group by necessity.
  Require a concrete paid operation and independent direction comparison
  before more factorial work; no hardness follows from this audit.
- **Independent topology operation rejected:** the proposed direct unitary
  AJL/volume-limit circuit requires the N-dimensional color at root orderN,
  whose quantum dimension is0. It is absent from path labels1,...,N-1.
  This excludes that circuit substitution only; no general topological
  no-go or assertion about current volume-conjecture status is made.
- **Paid canonical half-factorial composition, reviewed:** binary prime p,
  polynomial(logp,log1eta) BOUNDED-error quantum computation under GRH.
  One compact S-unit generator set supplies h and the full integer unit
  kernel on one success event; rational reconstruction/Bezout and exact
  signs normalize epsilon>1, and the existing local residue theorem pays
  nonunit factors. Known Mordell/Chowla congruences, including p3 exception.
  Eight certified classical controls complete; no quantum execution,
  polynomial classical sign certificate, novelty or separation. Accounted
  for as a composition of existing primitives; compare independent routes
  before any fractional-factorial extension.
- **Explicit Levi source and independent MQ mechanism rejected:**
  LEVI_TENSOR_AND_MQ_ADMISSION.md is independently actual-text reviewed.
  For d<p-1 explicit mixed tensors, exact finite Levi invariance yields
  exactly the block End algebra by derivatives; its commutant recovers
  U,W classically. No general source exclusion. The specified Gaussian MQ
  circuit has verified probability alpha times original solution density;
  no general MQ no-go. No implementation or repeat finite tests needed.
- **Constructive unbalanced Levi oracle algorithm, reviewed:** for known
  r>s>=1,p>=128n, ordinary additive matrix QFT exposes uniform kernels in
  U/Wperp with exactly charged good-mixture mass. r fresh copies each
  orientation plus a deterministic transvection certificate recover both
  summands; finite GL source clocks, valid-domain guards and QFT precision
  yield exact-on-success output, ABORT<=eta, polynomial resource costs.
  UNBALANCED_LEVI_COSET_RECOVERY.md passed independent derivation and
  actual-note core review. Known Borel machinery is credited; no novelty.
- **Matched classical baseline and application boundary:** a bounded
  birthday search in rank-one transvection subgroups plus membership
  rejection recovers the same pair in O((p^(3s/2)+r p^s+n²)log1eta)
  evaluations. Parent independently checked this derivation; no optimality
  claim. One p3n3 diagnostic complete, both full pipelines unexecuted.
  Opaque coherent coset access is a supplied promise, not a recovered
  source; explicit idempotent/matrix labels or H generators ease the input.
  No non-oracle application admitted. Balanced/small-p/all-Levi extensions
  require new arguments and must win an independent direction comparison.
- **Independent Kronecker sampler rejected at first exact test:** uniform
  RSK preimages followed by composition have TVerror1/2 at n4,lambda=mu22.
  Forbidden witness2143 composed2413=1324 has shape31; target coefficient
  is0. Sage exact internal product and parent character/product derivation
  agree. Only this sampler is closed. No scan, new subsystem, general
  classical lower bound or hidden-involution reduction. Re-rank native
  constructive mechanisms before continuing representation-theory work.
- **New constructive classical extension-field baseline, reviewed:**
  Given chosen padded signs of EVERY monic squarefree degree-d Q over
  public K=Fp^r, r>=2, p>=65536(rd)^2, two random translated norm lines
  recover Q exactly on success. Kopparty's full polynomial-p decoder is
  charged; O(p log1eta) queries and polynomial(p,r,d,log1eta) work,
  ABORT<=eta, exact gcd-degree certificate. No hidden root labels or norm
  values. Proper-subfield coefficients are covered by random translation.
  EXTENSION_CHARACTER_NORM_GCD_RECOVERY.md passed independent derivation
  and actual-text review. F49 diagnostic completed; full decoder not run.
  Fixed small characteristic/unbounded rd, unrestricted polylogp, repeated
  factors and passive/copy-only sources remain outside this algorithm.
  No implementation queue. Compare independent high-upside operations
  before extending this parameter boundary.
- **New weighted-moment receiver rejected before implementation.** For
  EVERY irreducible Q ofdegree d=2m-1>=3, public weights/Prony encoding and
  coefficient Fourier readout succeed with binom(p,m)/[p^m(p-1)^(m-1)],
  conditional on distinctx. Atdegree3 this is1/(2p), not polylogp success.
  Independent actual-note review accepted exact normalization and erasure.
  This differs from the split-resultant receiver; no claim about other
  uses of these outcomes or arbitrary collective measurements.
- **Independent oracle-sketch route does not remove native access costs.**
  Actual2604.07639v2 D.12/D.13 uses CLASSICAL labels and O(pQ²/epsilon)
  samples for uniform domainp. It supplies no phase-copy inverse. Raw
  coordinate updates require Omega(p) for constant target fidelity when
  p≫d² by the reviewed touched-coordinate/Weil bound. No rejection of
  its quantum space advantage, no all-algorithm lower bound or new code.
  Next question remains a concrete paid receiver polynomial in d,logp;
  compare independent directions before extending either failed operation.
- **Cubic Gauss elliptic shortcut: admission test complete.** Native input is
  explicit primary Eisenstein pi, fixed standard additive character. Ito's
  canonical elliptic product is already explicit; alpha(S_pi), a modular
  representative product, contains the remaining branch. Full-kernel norm
  gives only tau³; exact Jacobi reconstruction and arbitrary factorial cost
  must be distinguished. Tal's fixedq3 factorial call is not polylogp.
  Actual-note review and four finite exact Sage controls complete; no new
  quantum/classical algorithm, hardness, novelty or geometric-product run.
  No implementation queue. Highest-priority question remains a paid native
  character-polynomial receiver polynomial in degree AND logp.
- **Half-center lattice exclusion corrected; direct Gaussian proposal tested:**
  Given native explicit modular subset sum, binary witnesses are exactly
  closest coset points at the Boolean midpoint; no shorter nonbinary points.
  Signed parity changes determinant to2^n D/g. AtD2^n the exact mean count
  is1 under IID coefficients/independentuniformT, and2-2^-n under uniformX
  planting. No small-list finder or efficientCVP follows. The0.9408 source
  theorem also requires an SVPoracle. Legacy note corrected; single-record
  preserved quarantine queued, without withdrawing unrelated lattice work.
- **Gaussian target is useful but its preparation remains unpaid:**
  DCP_HALF_CENTER_DGS_ADMISSION.md passed actual-text core review. Width
  sigma²<=2pi/log(32n) gives source-average binaryprobability>7/16 under
  uniform targets and>16/17 under planted targets, minus samplerTVerror.
  A given-target sampler is required; generating fresh target/witness pairs
  is insufficient. Conservative unshifted-theta rejection has herald
  <=(17/16)(8/n)^(n/8), a specific-normalization failure, not allDGS hardness.
  Exact tiny Sage/fpylll controls completed, no quantum execution or scaling
  claim. Do not build a Gaussian wrapper without a new paid normalization.
- **Fixed-direction OPI Gibbs proposal falsified at its stated mixing gate:**
  Native q=2^t,m=q-1,[m,k] RS with independent uniform halfset tables.
  Fixed beta>0,R in(0,1), polynomial public catalog; exact weighted MDS
  variance and two-symbol affinity give exp(-Omega(m)) stationary exit.
  Fixed random-scan spanning mixtures consequently mix exponentially slowly
  in the worst start, with high probability over the ORIGINAL tables.
  SCALAR_OPI_GIBBS_LINE_TEST.md passed parent actual-text mathematical review.
  This does NOT bound first attainment from uniform/Prange input; the traps
  can already be witnesses. Published updated-basis annealing survives this
  test. No new algorithm, novelty, hardness, quantum run or benchmark.
  Independent candidate checks admitted no new paid operation; keep the
  implementation queue empty and compare fresh mechanisms before more work.
- **Hidden field classical baseline reviewed, quantum admission absent:**
  F(x)=padded chi_p Norm(Lx), arbitrary invertible Fp-linear L, n>=2.
  For p>=65536n², verified full sign lines create a public field and align
  each basis image among n Frobenius choices; O(p n log(n/eta)) queries,
  polynomial(n,p,log1eta) work. Exact-on-success, capped unbiased draws,
  factorization and retry budgets paid. Output normalized field product
  with identityv and norm/Norm(Lv), not unique originalL. No selected-line
  copies, sign-to-Singer oracle, polylog-p classical or quantum circuit.
  HIDDEN_FIELD_CHARACTER_ADMISSION.md. High-p pipeline WRITTEN, not run.
- **Singer barrier corrected from primary proof:** distinct Singer field
  algebras intersect in proper degreee<=n/2. Published PGM error bound
  <=4(N-1)p^(-nk/2), any-POVM average success<=(p^n-1)^k/N, so fixed-error
  standard coset-copy complexity Theta(n). No time bound or general-query
  lower bound. F81 exact subfield/charpoly/intersection control passes;
  native p3n3 Singular solve gives39 equivalent norm/algebra candidates
  from26 signs, finite only. Legacy note corrected; exact-hash registry
  quarantine and test-description scoping remain Gemini mechanical work.
- **Admission comparison, no new subsystem:** the Gauss identity does not
  itself convert native character copies to additive polynomial phases.
  No paid conversion was supplied by the independent mechanism review.
  Separately, actual primary text of 2609.20771v1 Theorem1.2 gives classical
  poly(n,K,log1delta) PFR with uniform samples and membership queries;
  do not pursue that exact task as an unmatched polynomial quantum route.
  No copy-only extension or independent proof audit. The OPI comparison
  found no new contraction beyond the already recorded small-conditioning
  falsifier. No code, tests, new barrier note or claim promotion.
- **Highest-value unresolved question:** can native character-polynomial
  reconstruction admit a paid quantum algorithm polynomial in BOTH degree
  and logp, rather than the remaining factorial degree dependence? Compare
  this published query/time gap with independent high-upside directions
  before continuing. The fixed-degree noisy problem is now covered at the
  written level, and a collective Hankel operation now gives uniform
  exp(O(d logd)) cost with a polynomial field threshold. Do not add nearby
  noise variants or merely relabel slow degree growth. The SAME split-source
  Fourier/Hankel operation is now closed as a polynomial-degree route.
  The symmetric-determinant receiver is now a proved structured case,
  without a source reduction from this native problem. Select a different
  paid source/measurement or an independent native direction; a specific
  operation and first falsifier must pass corpus,
  primary literature and classical baselines before implementation.
- **Coarse CFT entropy now classically matched, pointwise:** explicit
  lambda, row law chi_lambda(nu)^2/z_nu. Exact single-count marginals via
  finite formal Slater determinants; all-n polynomial bit cost. A protected
  O(n) window pays infinite-wedge CCR/Taylor stabilization, finite Laguerre
  mixture and exact binomial inversion. L=-sum P_s(m)log(s^m m!) computed
  to epsilon in poly(n,log1epsilon), same bias logp(n)+epsilon as the
  source's Section5.2 estimator. Actual-text core and separate source
  audits accepted. CFT_CHARACTER_MARGINAL_BASELINE.md. No joint law,
  joint entropy/exact Delta S, column sampling or full QCT simulation.
- **Entropy scale and evidence:** hook multiplicities give E m_s=h_s/s;
  equal hooks form an antichain, hence h_s<=sqrt(2n). Uniform bound
  -Delta S<=sqrt(2n) H_n logn=o(n) rules out asymptotic linear growth of
  the maximum or any average, not the source's finite plots. Five exact
  Sage marginal cases agree with full-row characters; wrong scale/window
  can remain positive/normalized but fail. Finite-only controls; no
  novelty, quantum run, paper-error or optimized classical exponent.
- **Independent comparison did not admit more subsystems:** published
  Legendre MQ is explicit diagonal quadrics and does not provide hidden
  full-Sym copies. In fixed-field complete AG, the effective parity
  selector budget2e-11 is strictly belowg=5e+1; raising it to the RR
  guarantee destroys the retained auxiliary-section rank certificate.
  Jacobian coordinates/halves were already paid classically. No new
  sparse selector or small-r2 promise; no extra AG backend or sweep.
- **Structured growing-degree receiver reviewed and bounded pass complete:**
  EVERY n>=3, arbitrary L on Sym_n, p>=256M, M=binom(n+3,4)+n+1.
  Global exact padded copies; parity Gauss combination has uniform rank1
  Fourier magnitude and squared source error<=4/(p-1). Learn Veronese I2,
  tangents, mixed-product lines and one generic-frame alignment, then the
  trace adjoint. All raw-row errors, PIT/majority and four eta/4 caps paid.
  O(n^4 log1eta) copies; poly(n,logp,log1eta) time/space. Actual-text core
  review accepted. SYMMETRIC_DETERMINANT_CHARACTER_READOUT.md. This does
  not supply a univariate source bridge or supersede the full-matrix
  direct-Fourier rejection. Do not start a determinant-variant program.
- **Native classical and evidence boundary:** same projective circuit
  output via complete sign lines, verified Kopparty decoding, log-det jets,
  trace Jordan multiplication and Newton identities. p>=65536n²;
  O(p[N³+log1eta]) native queries, poly(n,p) work, WRITTEN not executed.
  Actual source threshold epsilon*sqrt(p)/16, both leading signs and
  padded zeros paid; Weil exception includes any nonzero scalar square.
  No polylog classical learner/hardness/separation claimed. n3p5/n4p3
  raw FFT controls and n3p65537 ideal decoder pass; latter exact symbolic
  projective recovery rejects wrong adjoint/inverse controls. No actual
  contaminated-source or quantum run, native external application or
  novelty. Known-column alternative retained only as a non-admitted lemma.
- **Independent arithmetic pivot resolved by stronger current prior art:**
  exact repeated J_a, all q|p-1,1<=a<q, compatible character/prime,
  poly(q,logp) classical recovery including modp,p². Reviewed group-ring
  derivation pays all-character valuations, integral gluing, public norm,
  signed cyclic shift and even-q moment. Actual-source audit of Tal's
  September ECCC TR26-211 confirms the same native classical task via
  known-norm recovery and van Wamelen orientation. Supplied-p,q setup is
  Las Vegas polynomial(q,logp); selecting q from p alone is separate.
  Four controls CANCELLED before implementation. No novelty, paper-error,
  normalized-generator/factorial execution or matched exponent-c claim.
  JACOBI_GROUP_RING_RECOVERY.md. Do not reopen composite phase ambiguity.
- **Affine quadratic COPY receiver reviewed:** every n>=3, invertible A,
  arbitrary b,c and p>=256T. Let k1/2 for odd/even n, r=n-k+1 odd and
  T=binom(k+2,2)r(r+1)/2. Measure z, append public t!=0, homogenize the
  slice and Fourier sample. Shared C(z)=adjH_z/detB has degree2 and Crr1.
  Unique relation/rank escape, public reconstruction, resampled P and
  original-copy candidate verification pay polynomial resources/error.
  Actual-text independent review accepts Sections1--6 and5eta/8 ledger.
- **Slice source and controls paid:** actual/ideal squared distance is
  2(1-sqrt(1-1/p)); rare-event comparison gives26/p raw-row failure from
  ideal13/p, so no free ideal homogeneous source. n3p7 andn4p5 controls
  give ranks17/35, exact projective affine decode,4558 sign identities,
  retained bad slices and charged source change. Singular-B guard is
  ANALYSIS ONLY, not a hidden determinant test. All finite primes below
  threshold; actual noisy-row/coherent receiver not executed.
- **Affine classical/oracle scope:** random translated grids avoid the
  unique possible zero critical point. Fourth centered moments recover
  unknown leading character;220 F11 pairs and one F101 affine case pass.
  Stronger four-template square-root-p line attack independently checked
  as WRITTEN, not implemented: O(n^2sqrt(p)*polylog) native queries,
  extra n for input assembly. BIT/raw-phase quantum polynomial upper
  bound already follows from chosen-line univariate decoding. Classical
  polylog affine sign learning implies ALL shifted-Legendre instances
  via sum x_i^2+s; no hardness or copy-only reduction. Main note and
  audits/reviews/2026-11-06-affine-quadric-classical-scope.md retain scope.
- **Quadratic composition now accounted for:** this is one completed
  constructive slice-lift pass, not a new variant program. Do not extend
  by default to singular forms, noise, n2 or smallerp. General native
  polynomial-degree reconstruction stays highest priority; a new operation
  or independent direction must pass admission before implementation.
- **Kloosterman alternative tested, not admitted:** explicit growing
  odd prime p,a!=0, approximate K_p(a)/sqrt(p). Actual-source audit confirms
  Bruin's sqrt(p) extraction and Childs's already-published walk norm loss.
  Published degree theorem gives [Q(K):Q]=(p-1)/2 for EVERY p>=5,a!=0,
  refuting an elliptic integer-trace transfer, not approximate computation.
  C_a:y^p-y=x+a/x has genus p-1; (x,y)->(rx,ry) identifies C_a,C_(r^2a),
  while the requested character traces differ for r!=+/-1. Unmarked whole
  zeta loses the label even if its cost is ignored. Marked/original-a
  algorithms remain open. One exact p5 pair verifies unequal conjugates,
  genus4 and counts12; full zeta/quantum algorithm not executed. No more
  formal rank2/walk wrappers. KLOOSTERMAN_SPECTRAL_ADMISSION.md.
- **Structured determinant Fourier candidate rejected at admission:**
  unknown L in GL(n^2,Fp), n>=2, global padded character of det(mat(Lx)).
  Exact matrix Gauss sums give TV(P_L,uniform)<=1/(p-1)+p^(-n/2), padding
  included. IID t labels multiply the bound; binary success2/3 needs
  t>=p/15, despite unrestricted classical postprocessing. Independent
  core review accepted the written proof. This is NOT a coherent or
  collective copy lower bound. Full-value determinant equivalence is
  already polynomial under GGKS19's field promises; sign/copy-only
  learning is not thereby solved. Native source application also unpaid.
  No implementation or scan: CHARACTER_DETERMINANT_FOURIER_ADMISSION.md.
- **Independent toric point-count comparison:** explicit canonical Laurent
  inputs, fixed augmented rational rank rho and bounded exponent entries.
  For odd-characteristic Newton-nondegenerate s>rho, the published bound
  |N_g-A_r|<=(v-1)q^((r-1)/2) meets the requested epsilon q^(n+s/2-rho).
  Saturated coordinates, v<=r!(2C)^r, a large-q ambient answer and bounded
  small-q enumeration pay poly(input,logq,1/epsilon) classical time.
  Equality s=rho has an exact fixed-order character algorithm via Pila
  curve counts, with no full DLP/Gauss oracle. Both actual-text independent
  reviews accept the written composition after scope/encoding clarifications.
  General s>rho degenerate inputs remain outside the result.
- **Point-count falsifiers and triage:** p41/43 generic controls certify all
  15 Newton faces and exact errors103/11. Degenerate factored input has
  error1560>840.5 atp41; factorization solves it, so no hardness. p13g4
  checks16 exact Jacobi identities and64tuple pointcount0; Pila itself not
  executed. Native character poly(d,logp) remains the main question after
  independent OPI/HSP comparison; no new operation passed admission.
  TORIC_POINTCOUNT_ACCURACY_BASELINE.md records the proof/source boundaries.
- **Global quadratic-character COPY receiver reviewed:** oddn>=3,
  p>=16n^2, every nonsingular symmetric A. Exact fresh global padded phase
  copies suffice for projective recovery in poly(n,logp,log1eta). Fourier
  mass alpha=(1-p^(-(n-1)))(1-1/p)^2 is uniform on the nonzero dual cone.
  A Witt chart proves5/p wrong-quadratic intersection and uniform feature
  rank escape; D-1 labels succeed>=9/16. Fresh cone validation, capped
  attempts and QFT precision pay all errors/resources. Independent actual-
  text review accepts the theorem. QUADRATIC_CHARACTER_CONE_READOUT.md.
- **Source/classical scope paid:** existing univariate degree2 algorithms
  already give polynomial BIT/raw-phase recovery via O(n^2) affine lines;
  GLOBAL copies cannot supply those line states free (direct costp^(n-1)).
  Native classical line moments give O(n^2p) SIGN queries/O(n^3p) field
  work;84 exact p7 cases pass. A classical poly(n,logp) projective learner
  would solve shifted Legendre with one-query simulation and exactzero
  repair;2058 simulation/36 ratio checks pass. Implication only, no hardness.
- **Cone controls complete:** four prescribed sources, exact field/rank
  algebra plus floating FFT, all belowthreshold. Full cone ranks5,5,5,14;
  omitted zero padding changes the law. p5 I and2I have the same projective
  cone but different zero spikes. At p3,n5 correct and wrong cone validation
  both accept49/81, so no small-prime extension. No coherent circuit run.
  The copy theorem is accounted for; no generic parity/noise sweep.
- **Independent source-priority check:** retrieved November Simon mirror
  has unchanged operational decoder despite rewritten explanation. Direct
  official/mirror byte identity UNKNOWN. October label-information transfer
  remains applicable to inspected operations; no DCP re-entry or simulation.
  See audits/reviews/2026-11-05-simon-november-source-delta.md.
- **Actual Hankel success boundary reviewed:** for every irreducible Q,
  d>=2 and p>=2d-1, ANY normalized state on the same fully split degree2d-1
  coefficient support has correctness <=(d-1)!/(2d-1)!<=d^-d under this
  Fourier/Hankel measurement. A residue fiber cannot contain two distinct
  polynomials sharing d roots; d-subset packing and Cauchy prove the bound.
  This covers arbitrary weights/phases, mixed states and retained ancillas.
  Clean exact mass is sum C_v^2/(N p^d) minus zero-frequency mass. Parent
  exact p5 check gives217/3125, agreeing with saved FFT. The valid algorithm
  upper bound remains; no generic quantum/copy/query lower bound follows.
  See LEGENDRE_HANKEL_SUCCESS_BOUNDARY.md; no more success/weight sweeps.
- **Independent constructive triage:** public coefficient translation
  lacks paid resultant-phase transport. Exact p7 targets with identical
  root signs need opposite shifted phases; parent Sage reproduction passes.
  Extra native queries/interference remain open, not supplied. Independent
  OPI marginal-based unequal reliabilities reduce to equal-list weights
  whenever <=k-1 other rows are conditioned; no new operation admitted.
  No new decoder, benchmark or generic subsystem. Next work must change
  the actual operation or win an independent native-direction comparison.
- **Uniform Hankel receiver reviewed:** for all d>=2, monic squarefreeQ,
  p>=256d^2, clean padded pure copies admit per-attempt correctness
  >=1/(32(2d-1)!). For ONE fixed corrupted F at rho<1/4, require also
  p>=64d^2/(1-4rho)^2 and use bound1/(32*36^(2d-1)*(2d-1)!). One
  Fourier outcome gives a full-rank weighted-trace Hankel matrix and Q;
  Cauchy applies to the Q-specific decoding event. Exact signed-subset
  recurrence pays robustness. Uniform permutation cleanup, shared-seed
  factoring, QFT, verification and caps give the stated total bound and
  polynomial ACTIVE workspace; source cap R(2d-1+K), failure<=9eta/16.
  This removes the old exp(O(d^2 logd)) retry cost and factorial prime
  threshold, but not factorial density. See LEGENDRE_HANKEL_RESULTANT_READOUT.md.
- **Hankel falsifiers completed:** four clean sources and one fixed
  corrupted cubic, original-degree native table baselines first. All
  virtual unit labels decodeQ and nonunit labels in the annihilator are
  singular. Leaving old chi(a)^m uncorrected kills both quadratic overlaps;
  required phase is chi(a)^d. p7 corrupted E5=-2/3. Every finite case has
  wrong projection score1; corrupted table equals another polynomial's.
  All p below threshold. Exact fields/floating FFT only; no full verifier
  or quantum execution. Known Prony and full-VALUE interpolation do not
  supply the native character moments; exact priority remains unclaimed.
- **Fixed corrupted-function decoder reviewed:** for fixedd>=2,
  rho<1/4 and p>=max{512*9^d*d!,64d^2/(1-4rho)^2}, fresh pure copies of
  ONE fixed F withinrho*p of paddedchiQ reconstruct every monic squarefree
  degree-d Q in C_d poly(logp,(1-4rho)^-1,log1eta) gates/copies. An exact
  signed-subset overlap, controlled sampling collision bound and uniform
  rank growth feed statistical public-candidate verification. Explicit
  bounded schedule/precision gives failure<=9eta/16. Independent review
  accepted all steps. No mixed/device/changing-mask/correlated-source or
  growing-degree extension. See LEGENDRE_CORRUPTED_CHARACTER_READOUT.md.
- **Robust-source falsifiers completed:**12 fixed controls, native table
  decoding first,808 proper-subspace checks. p7 mixedcubic with one
  nonrootflip has E3=0 despite IID8/27; two flips reverse its sign. Root
  flips preserve comparison overlap. At p11, X^3+X and X^3+4X^2+3X+8
  have opposite padded tables and identical physical phase states; BIT
  access distinguishes. Parent reproduced exact counterexamples. Ten
  coarse bounds are vacuous; all finitep below threshold. No quantum run.
- **Classical/error-radius comparison:** Kopparty applies to full tables
  below its stated1/8 radius, not automaticallyrho<1/4. Empirical exhaustive
  decoding coversrho<1/4 with polynomial-in-logp BIT queries and p^d
  enumeration; no query separation. Midpoint tables exclude every fixed
  rho>1/4 asymptotically, not an exact finite-radius claim. Classical
  polylog total-time recovery and exact quantum priority remain open.
- **Squarefree padded extension reviewed:** the coefficient receiver now
  reconstructs every monic SQUAREFREE degree-d Q, d>=2 fixed, for every
  prime p>=max{128d!,256d^2}, in C_d poly(logp,log(1/eta)) gates/copies.
  lambda0=+1 copies require no unknown root flags. A virtual product-algebra
  character has U Fourier labels in Q-perp, not all nonzero labels. Exact
  overlap Ngood/sqrt(N0*pU), uniform escape and shared-factor verification
  pay the same bounded receiver with a squarefree candidate filter.
  Independent review accepts proof and resources. No growing-degree,
  small-prime-universal, noisy-quantum, novelty or separation claim. See
  LEGENDRE_SQUAREFREE_RESULTANT_READOUT.md.
- **New decisive source falsifiers:** three p11 factor patterns pass the
  appropriate U-point spectrum and subspace controls. The old all-nonzero-H
  spectrum is false for reducible Q. X(X-1)(X-2) and irreducible
  X^3+4X^2+10X+5 have EXACTLY the same padded table at p11; TRIT distinguishes.
  Distinct irreduciblequadratic squares have identical constant+1 TRIT
  tables (explicit p5). No unqualified finite fallback or repeated-factor
  reconstruction. Exact fields/floating FFT, no quantum execution.
- **Classical source/priority audit:** Kopparty2601.07137 AlgorithmA/Thm3.1
  gives a full-p-query poly(p) decoder with constant-error tolerance; root
  padding costs <=d errors. Its proved degree bound has an extra factor16
  relative to the introduction; use the explicit sufficient constants.
  This does not transfer to IID arbitrary OPI halfsets. A worst-case
  classical irreducible-quadratic decoder would solve ordinary linear
  Legendre hidden shift via one-query simulation and a paid padded-zero
  correction. That is an implication, not hardness. No new polylog classical
  operation was admitted; exact quantum receiver priority remains open.
- **Fixed-degree resultant-hyperplane receiver reviewed:** for each FIXED
  d>=2 and every prime p>=max{d(d-1),16d!,16(2d-1)^2}, native pure copies
  reconstruct every monic irreducible degree-d Q in
  C_d poly(logp,log(1/eta)) gates/copies. Distinct-root folding, a coherent
  public scalar with chi(a)^d and paid clean factorization give a split
  coefficient state. Constant overlap with a VIRTUAL norm-character state
  forces Fourier escape from EVERY proper subspace of Q-perp. Blocks of d
  samples reconstruct Q; fresh-copy projections verify it. Public random
  signatures pay root erasure for all labels simultaneously. Explicit
  seed/sampler caps, error budgets and Kitaev's abelian QFT pay the circuit.
  Independent review accepted the proof and resource ledger. Degree growth,
  small-prime universality, noisy/correlated sources and novelty are excluded.
  See LEGENDRE_RESULTANT_HYPERPLANE_READOUT.md. The older GL2 proof remains
  independently valid; no further GL2 subsystem is needed for this route.
- **Native cubic classical attack reviewed:** for every p>=23, p original
  character queries and O(M(p)logp+p) field work recover every irreducible
  cubic. A central unaliased coefficient window, differential recurrence
  and Wronskian degree contradiction prove full rank. Exact finite controls
  found48 rank-two p13 exceptions and full rank for all p17/19 inputs.
  Fast interpolation is a resource theorem; the finite script uses Lagrange.
  This is exponential in logp, not hardness or a matching polylog algorithm.
- **Resultant finite falsifiers completed:** all10 p5 quadratics and112 p7
  cubics,60/6384 proper-hyperplane checks, exact field algebra plus floating
  FFT. Phase, flat-spectrum and overlap identities pass. Retained injective
  root labels make Fourier output uniform; missing chi(a)^3 kills cubic
  overlap. The p7 escape lower bound is vacuous. No quantum circuit was
  compiled or run. No expanded scan is requested.
- **Growing-prime BIT reconstruction accounted for:**
  QUADRATIC_LEGENDRE_SPHERICAL_READOUT.md gives a reviewed written
  poly(log p,log(1/eta)) composition for every monic irreducible quadratic.
  T=2DC-J, explicit principal fixed vectors, the GL2 QFT's actual GT basis,
  and a two-Gauss-phase adjoint LCU pay the full receiver. Xi's fourth
  Jacobi moment gives trace p^4/8+O(p^(7/2)), with joint ideal success>1/32
  for p>=625, including every projection/LCU flag. No polar inverse or
  conditioning bound is used. Capped preprocessing, exact fresh
  verification and bounded retries give failure<eta. Three independent
  scoped reviews accepted the corrected written composition.
  Label order, inverse-additive PDF bars, entire dual-vector conjugation,
  compatible generators and exact sampler caps are essential. Five exact
  character controls and an all21-column p7 frame control are algebraic
  checks only. No compiled/executed quantum receiver or novelty/separation.
- **Phase-copy source restriction removed:** an independent review accepts
  the finite-domain copy-only corollary. Omitting infinity changes the
  normalized two-copy state by norm<1/16 for p>=625; contraction of the
  reviewed receiver gives ideal joint correctness>1/128. Verification uses
  fresh copies and public known-candidate projections, not classical oracle
  values. Explicit precision/capped retries and a separate small-prime
  copy-only procedure give failure<eta and polynomial gates/copies. An
  uncontrolled raw phase query makes each required copy; no controlled
  unknown unitary or homogeneous lift is assumed. Exact pure tensor-power
  source only. The classical bit-query baseline retains its own model.
- **Critical GL2 source audited:** the explicit hard A_gamma circuit now
  has a separate all-q proof/resource audit, including noncircular
  exceptional-column preparation. Its torus-map isometry independently
  forces target-column orthonormality. One finite source falsifier checks
  all 15 central-trivial columns at q=3,5,7 with 200-bit matrices; omitted
  exceptional correction fails. This is not whole-QFT or device execution.
  No further source/conditioning sweep is needed. Focused classical
  derivative/sparse-power/Mobius triage admitted no new operation and
  establishes no lower bound. Re-rank independent directions before more
  work on this line. See the GL2 source review and its scoped artifact.
- **Native quantum comparator paid:** independently reviewed exact MDS
  second moment gives E chi2<=2^m/q^k and simultaneous relative-count
  failure<=4^m/(delta^2 q^k) for all Boolean acceptance patterns on the
  original IID FULL half-set tables. This supplies ONE good-instance event
  paying known complete-list erasure with success Z/L, Z=1+o(1).
  The attainable asymptotic score is1/2+sqrt(a(1-a)),
  a=min(1/2,1-sqrt(1-R)); at R1/4,0.840625 versus the old unique-radius
  0.830719. For fixed R>3/4, polynomial repetitions find perfect witnesses.
  All-field Johnson decoding, public table circuits, precision and global
  bounded retries are charged. The curve/mechanism are prior art; no
  capacity-decoder transfer, quantum execution, novelty or speedup claim.
  Correlated trace-hyperplane tables explicitly falsify a worst-case
  extension. Historical finite DQI scores remain as executed. See
  SCALAR_OPI_RANDOM_TABLE_LIST_SAMPLER.md and its independent review.
- **Portfolio reason:** interleaved OPI already lacks a paid support-phase
  erasure operation, and Kopparty's structured fibers do not supply it for
  native IID tables. The admitted global-copy quadric receiver instead
  exploits an exact dual-cone law in growing dimension, a different paid
  operation on the established multivariate character-learning problem.
  Its stronger oracle upper bound was already a univariate corollary;
  only the global-copy source distinction is new to this ledger. The
  univariate Hankel packing boundary remains closed, and the November
  Simon mirror supplies no changed decoder. Further work must identify
  external native use or a genuinely different paid source/measurement,
  then win an independent portfolio comparison. Priority remains unclaimed.
  Binary-cubic orbital formulas and the older failed affine/matrix-coset
  operations are not used. No generic subsystem was introduced.
- **Fixed-characteristic Legendre boundary established:** for FIXED oddp,
  q=p^n and n growing, paid reflection fingerprints feed Friedl et al.'s
  known hidden-translation algorithm, time(n+p)^O(p). A public character
  Fourier diagonal gives C/tau+J/q and constant-success width recovery
  without a supplied Gauss phase. Independent review accepted the written
  polynomial-time composition, including zero shift, field arithmetic,
  source injectivity, precision and capped-retry accounting. Raw-phase
  relative-bit compilation also applies. No quantum implementation or
  novelty/separation claim. This does not enlarge a prime-field oracle or
  solve growing-prime q=p. QUADRATIC_LEGENDRE_RECOVERY.md, final section.
- **Earlier Legendre comparators retained:** reflection fingerprints give
  an exact DCP source; Kuperberg plus a constant-success partial-Legendre
  transform gives2^O(sqrt(log p)) time, queries and quantum space. The
  stronger classical chosen-query baseline uses expected O(sqrt(p)polylog p)
  time/queries/memory, with conservative error257/4096. All6 predeclared
  classical keys recovered;164 moment controls and3 p3 exceptions retained.
  Exact p37/43 algebra verified80 fibers,3218 DCP phases, unitarity and both
  Gauss-phase branches. No end-to-end quantum decoder was executed.
- **Legendre source correction:** a public reference eigenstate and two
  controlled swaps compile relative output bits with ONE uncontrolled phase
  query, up to a fixed global phase. All2558 exact Sage p5/7 basis cases
  passed;1248 omitted-swap cases failed. This weakens the quantum access
  requirement without changing the saved classical bit-query baseline.
  Copies alone do not supply the construction; no general copy lower bound.
- **Legendre receiver proposals parked:** affine evaluation followed by two
  character projections has success1/(p-1)^2, costingTheta(p) under generic
  amplification; the GL2 cleanup does not remove that normalization.
  Homogeneous self-duality holds for every balanced projective-line coloring,
  and its direct Fourier output is uniform. The native two-copy B_k polar
  remains unpaid, not impossible; measuring k removes the center phase.
  No generic receiver framework or conditioning sweep. A different explicit
  circuit is required before reopening either tested proposal.
- **Matrix-coset receiver rejected:** for p>=41, polylog public projective
  fingerprints hide H<=GL2 of order p^2-1, with exactly two stabilizers of
  each nonzero vector. One routed original bit query computes each
  homogeneous bit; global bad-list probability<=p^4(3/4)^L. After labels
  are discarded, the additive-Fourier probability of EVERY measured matrix
  depends only on its rank and p, never on the secret. Independent review
  accepted the source, rank counts, exact normalization and H-to-Q
  postprocessing. Retained-label/coherent/collective readouts remain outside
  this falsifier. No new simulation or general HSP framework.
- **AG alternative rechecked:** actual F1019 seed infinitude does not bound
  full rational r2 along the arbitrary quadratic chain; the source is not
  a specified cofinal Frattini tower. Ordinary RR degree g exceeds the
  selector budget by3e+12. No new selector or rank theorem was found in the
  bounded source audit. Existing marked-point obstruction and conditional
  small-rank theorem remain; no backend or finite-rank sweep.
- **AG matrix-only proposal recovered prior work:** the root count FPTAS
  and its explicit conditioning counterexample are already in
  NORM_SAMPLER_CLOCK_FALSIFIER.md. Multibasis/AJT and affine-repair audits
  also cover the proposed direct shortcuts. No new attack, conditional-count
  oracle, theorem or counterexample package was added for this lookup.
- **Scalar OPI question remains live:** can a polynomial-time classical
  algorithm on FULL EXPLICIT random scalar OPI tables match the known DQI
  score? Native family: F_(2^t),m=q-1,degree<k,IID half-sets; no folded-oracle,
  prime-field or compact-predicate transfer. See SCALAR_OPI_NATIVE_PRIORITY.md.
- **Completed restrictions:** the full-row-rank affine-flat forcing
  certificate cannot close a fixed DQI gap. Equal-within-list INTEGER Hasse
  multiplicities cannot meet the strict GS/KV root certificate for k>=3,
  even with adaptive row weights. Unequal symbol weights and accidental
  factors remain outside this statement. Independent reviews accepted both.
- **Completed FFT result:** the specified schedule averaging all future
  coefficients before freezing ignores all but k-1 actual tables at dyadic
  k. Its mean is at best the Prange limit; polynomial independent restarts
  do not close a constant gap. Adaptive feedback is not bounded.
- **Actual experiment stopped:** the freeze-aware max-sum repair ran at
  q16/64/256,k=q/4, two seeds each, against actual Prange32 and rational
  ideal-DQI mean bounds. At q256 it scored155,165 versus Prange171,172 and
  DQI>=203.636. Independent Sage checked all18 native witnesses plus exact
  Hasse/unequal-weight/Cauchy controls. Independent implementation review
  found no invalidating error. This is finite failure, not hardness or an
  asymptotic result. SCALAR_OPI_SOFT_DECODING.md records all limits/artifacts.
- **Algorithm H classical probe completed:** exact full-table Walsh
  restriction uses known weighted-parity elimination, <=kt steps and
  polynomial explicit-input cost. Six unchanged saved cases: q256206/203
  versus Prange171/172 and DQI mean lower203.636. One predeclared q512,
  k128,seed3101 continuation returned396 versus Prange347 and DQI414.037.
  Independent Sage checked all seven native witnesses plus q512 Prange,
  2396 saved parities/gain identities and62 exact section means. Rank-4
  accepted affine images explain much of the finite gain. The next-size
  persistence test failed; stop sweeps, retain the finite classical baseline.
  The reviewed early no-alias lemma does not bound the final score; an
  explicit balanced quadratic table refutes an initial-Walsh ceiling.
  Asymptotic matching and classical hardness remain UNKNOWN. See
  SCALAR_OPI_FOURIER_ELIMINATION.md and its linked artifacts/review.
- **Independent alternative checked:** reciprocal-trace BIT hidden shift
  has a paid Fourier-sign polynomial construction, but generic Boolean
  injectivization+Simon already solves it. The old constant-degree classical
  negative reads FULL prime-field values and does not transfer. F4 really
  has ambiguous shifts; 25 exact autocorrelation controls passed. Park the
  line absent a separate native application. RECIPROCAL_TRACE_SHIFT_SCOPE.md.
- **Earlier quantum portfolio decision:** no new quantum operation was admitted. Jo's list-erasure
  construction is prior machinery. Local-only Goppa pivots retain the large
  syndrome space; AG four-base extraction and one-endomorphism transport
  supplied no new paid step. Keep those routes parked. No new sweep,
  receiver, quotient package, registry promotion, manuscript or outreach.
- **Rees checks (11-01/02, AI sessions only):** the core proof check found
  steps 1-5 of main.tex Theorem main hold under Schedule 1 for every c<p and
  every H, with no gap or counterexample; Schedules 2-3 stay conditional.
  The priority check puts the conjunction at "possibly new": IS Cor 8 is a
  special case (A4 not new), the descent is IS Section 5's (A2 not new as a
  mechanism), and only A1, the graded cover for arbitrary H, may be new.
  All Rees claim gates stay false; human review is still required. Next:
  an A1 priority note from citing-paper full texts. Reports in audits/reviews/.
- **Rees extensions and schedules (11-02, AI sessions only):** Cor fpt-r
  (class not fixed), the ring-to-field torsion recursion and the black-box
  pullback all survive with no counterexample, given unstated but
  elementary steps (IMS error amplification, two stop rules, ker Phi as an
  abelian HSP). A per-grade Schedule 1/2 rule is valid for every p>c and cuts
  class-9 queries to 2^61.5-2^1562 depending on p, but the worst-case
  exponent barely moves (145->143). Small-prime arity: witnesses always exist
  at kappa*a+1, so only efficient FINDING is open; Schedule 2's threshold is
  proved 26-156x lower. Open: a near-observed two-level threshold.
- **Rees full campaign (11-02, twelve AI sessions, REES_FULL_CAMPAIGN.md):**
  no counterexample anywhere. The hidden-codimension bound is restored; the
  prime-power compiler covers every c<p (fix in universal_lazard_words.py);
  the subspace, compilation and filter sections are checked with text gaps;
  the Lean rebuild matches the paper and four new general-class files are
  added outside formal/. A deterministic Schedule 1 solver and an exact
  end-to-end simulator (230/230 recoveries) now exist. A1 is still possibly
  new. No native application (negative result). Candidate manuscript
  main-full-draft.tex awaits owner decisions on conflicts C1-C17; human
  review remains the binding gate.
- **Rees full campaign round 2 (11-02, 18 AI sessions, REES_FULL_CAMPAIGN_2.md):**
  main.tex is now the full paper: 89 pp. with proof appendices A-E,
  building clean, with change log -integration-log.md. New in it: an all-prime
  black-box theorem, a classical query bound Theta(p^{(m-1)/2}), a
  triangular solver, a 2^34 Schedule-3 sampler and the referee P1-P8 fixes.
  Eight Lean modules are promoted into formal/ (403 guards, clean build).
  Also new: a Qiskit circuit for Heis(F_3) and class-four exact simulation
  at Rule W arity. No counterexample. Still open: human review, the
  Schedule 2 square gap, o(a^2) SDE finding, a coherent receiver and a native
  application. Ranked list and next command: REES_FULL_CONTINUATION.md.
- **Rees rounds 3-4 (11-02 night):** Appendix F proves the free-coordinate
  Schedule 3 theorem. Unanchored AI proof checks of Appendices A, B and E and
  of the core found no error, only gaps (most notably the lem:hybrid domain).
  A 25 pp. core paper is at docs/papers/rees-hsp/core/. Threshold-3 is an
  obstruction near kappa^kappa/2. See REES_FULL_CONTINUATION.md.
- **Rees 11-03/04 passes (AI only; main.tex 149 pp., builds clean; log rows
  I137-I189 in audits/reviews/2026-11-02-rees-integration-log.md). State now:**
  - Black box: (H1), (H2), (H3) of prop:tb-count-gates all discharged
    (I150, I172, I174, rechecked I178); normal-form proviso removed by
    lem:tb-howell-rounds (I183); chart-size and Lie-ring checks after a failed
    kernel step (I181, I183). Total time tau_c = max(E_W(c)+1+max(3,beta_c),
    23/2), cases c=1, 2, >=3. AKS cited only at O~(log^{21/2}); whether
    Thm 5.3 is 15/2 NEEDS A HUMAN (then 23/2 -> 17/2).
  - Coherent receiver: prop:coherent-receiver (I173, check applied I175) is an
    EXISTENCE statement via Pippenger-Fischer + Bennett on Schedule 1; not
    implemented; gate coherent_receiver_implemented stays false. Explicit
    T^IS_d = C_1 d^3 M_d b^3 (g_d^2+b^2) in rem:is-runtime (I177), TM layout
    sketched (I179). Coherent witness circuits wired into four backends. lem:qft-mod is already wired (optional backend
    theorems/rees_circuit_qft_wire.py, I157); do not redo it.
  - E_2: exact for kappa<=7. kappa=8: E_2(8) ⊆ [3, 20000] (I187 sweep to
    ceil T_A(8)=117441563 + I189: all 29 former gap primes FEASIBLE; two
    verifiers). Decided up to 11953; 11689 and 11953 ∈ E_2(8) (11953 = 1.03 kappa^4.5,
    found 11-04 ~22:00 by the old sequential scan, which is now finished and
    killed; not yet in the paper). Queues add 12073, 12281, 12289, 12377, 12457, 12809 ∈ E_2(8)
    (12809 = 1.106 kappa^4.5; 30/216 decided at 11-04 23:30, ~12 h to go at this
    rate); kappa=9 adds 15823, 15859.
    kappa=9 T1/P sweep DONE and IN THE PAPER (I223; 2026-11-04-rees-k9-sweep.md
    "Result (2026-11-05)"): every prime p = 1 mod 9 in (20000, 9^9/2] (1791117
    primes) has an explicit two-level contraction checked by two verifiers (bad=0),
    except 1373 listed primes (exceptions_20000_193710244.txt, max 424549; OPEN,
    not shown in E_2(9)); 3098 witnesses have a zero entry, all at p <= 651727.
    9^9/2 < T_A(9), so E_2(9) is still not known exactly.
    dfs2b snapshot in the paper (I223, 11-05 06:49): decided to 13873 (kappa=8) and
    16363 (kappa=9); largest proved members 14281 in E_2(8) (1.23 kappa^4.5) and
    18199 in E_2(9) (0.30 kappa^5). Screens dfs2b_k8hi_2..4, dfs2b_9_14501/_17501
    still running (grep INFEASIBLE small-prime/dfs2b_k8_hi_q*.out and
    dfs2b_k9_1*.out); dfs2b on k9 exceptions 20071, 20089, 20107 running.
    Remaining for exact E_2(8): primes in (13873, 20000].
    11-05 midday: only 8 kappa=8 primes <= 20000 remain undecided (18457 18617 19009
    19273 19457 19681 19801 19961), plus 41 kappa=9 primes in [16741, 19963]. Three
    cloud sessions (dfs2b-cloud-a/b/c, 5.5 h deadline, results only in their final
    messages, nothing committed) run: A = those 7 kappa=8 (not 18457) + kappa=9 >= 18397;
    B = kappa=9 16741-17497; C = kappa=9 exceptions 21313-24373 (48 primes). Re-verify
    every FEASIBLE witness locally (verify_k9.py / dfs2b re-check) before using it.
    Also: dfs2b-xcheck-d/e rerun the 213 kappa=8 members <= 10753 and 211 kappa=9
    members <= 14149 never checked independently, in dfs2b "plain" mode (same tree and
    node counts as unpruned dfs2; nosym/plain are ~10x slower, so the headline members
    14281/18199 are out of reach); dfs2b-cloud-f = kappa=9 exceptions 24391-27271.
  - Overnight 11-04/05 (log I190-I239; main.tex 201 pp., core 27 pp., clean): P6/P8 (I190-191);
    prop:triangular-sde adversarially reviewed TRUE, gaps closed, E_W unchanged so
    not adopted (I192); application-3 negative, survivor S1 = circuit polynomials of
    degree >= p (I193); IS restarts collapse to Omega(kappa) runs for prime-power
    kappa (I194); K7 merge: thm:random-column is now thm:free-coordinate(iv), and
    zero-sum Z1 (finder <=> avg-case binary SIS), A4 (coset-copy proved) folded in
    (I195-I201); Lean class six + kappa=2 contraction + CW receiver policies,
    488 guards (I202); rem:sde-subquadratic, SDE in O(a^2/log a) columns for
    i.i.d. uniform columns, quadratic stays the worst case (I203); K30 exact
    exponents in Z[zeta_p], clause dropped (I204); coset-refinement tower,
    appendix-schedule2 app:s2-tower, square gap NOT closed and arity not
    lowered (I205); rem:sde-block-steered, floor((a+2)^2/4)+[a odd] columns,
    applies to Rees labels via the span; ADOPTED 11-05 (I233) (I206).
    Threshold-7 (audits/reviews/2026-11-05-rees-threshold-7.md, unchecked at
    checked 02:00 in -threshold-7-check.md, no Error, integrated as
    app:s2-chains, I209; 164 pp.): for every kappa >= 4 (incl. prime kappa) a
    CUBIC-arity C(a+3,3) solver at p > Theta_2(kappa) <= 4.05 kappa^2
    (ln kappa)^kappa (kappa >= 16; Theta_2(5)=3781, Theta_2(7)=30823), far below
    T_A; a barrier to O(a^2) from towers; exact no-chain primes kappa = 4..9.
    Alternative option, not a Schedule 2 change. OWNER DECISION: using chains
    or the tower at kappa_d = 4 in the combined rule would change E_W(7..9).
    Referee 13 on overnight text: 4 Errors (tower threshold not polynomial
    for large prime factor of kappa; combined rule has no Schedule 3; Lean rank;
    application-3 class < p) + gaps/imprecisions fixed in main.tex (I207).
    Receiver sims (audits/reviews/2026-11-05-rees-receiver-sims.md, unchecked
    01:30): monolithic exact simulation Heis(F_3) c=2 (all 19 subgroups) and
    n4(F_5) c=3 (7/9); exhaustive n5(F_5) class-four merges (extension to all
    pairs argued); n5(F_7), n6(F_7) class five module by module.
    coherent_receiver_implemented stays false. Check + integration running.
    Schedule 3 zero-sum node (-s3-arity.md, checked -s3-arity-check.md, no
    Error, rem:fc-zero-sum-arity, I210; 166 pp.): polynomial-time average-case
    node at Gamma_0, arity O_c(g^{1+ceil(log2 c)} log(1/tau)), abort <= tau,
    weight-doubling recursion on KMOSW affine reducibility; barriers for merge
    trees, switch recursion, information sets. o(g^2) and f(p)poly(g) still
    open. OWNER DECISION: adopt it as a third Gamma_0 option in (R1).
    SDE worst case (-sde-worst-case.md, checked -sde-worst-case-check.md, no
    Error, rem:sde-worst-case, I211): every kappa a+1 columns solvable (CW,
    already in paper), longest unsolvable length in [2a, kappa a], = 2a at
    kappa=2; general-position banks solved with floor((a+2)^2/4)+a columns,
    no randomness over columns; Rees labels are in general position only at
    p >> C(M,a_d). Arbitrary columns: still (a+1)(a+2)/2 proved; o(a^2)
    conjectured (2520 banks). No table/E_W/143 change.
    Receiver round 2 (-receiver-round2.md, checked -round2-check.md, no Error,
    I212): exact output law of the whole Heis(F_3) circuit, all 19 subgroups;
    checkpoint checks vs h-derived reference states (92 mutants: 72 caught
    every run, 20 provably dead gates, none missed); step (R) product identity
    Lean-checked (standalone module, not in Formal.lean); n6(F_7) class five
    14/14 seeded recoveries. Gate coherent_receiver_implemented stays false.
    Core paper core/main-core.tex (27 pp., clean) synced with I190-I212
    corrections (-core-sync.md, I213).
    Application-4 (-application-4.md, checked -4-check.md, I214): no native
    application; Theorem W proved: S1 is classically easy when the base-p digit
    sum of F is bounded with p > max((nu-1)d, 2d), D <= p (possibly known,
    NEEDS HUMAN VERIFICATION). Residual S1: unbounded p-weight, or D fixed with p
    superpolynomial. speedup/novelty gates stay false.
    Referee 14 (Fable, whole paper, -referee-14-fable.md): major revision, 2E/8G/
    20I/12S; verified and applied (-referee-14-applied.md, I215): E1 chain
    values attributed to the numerical criterion, dates 5 Nov, tower step-1
    sampler gap stated (T_A(q) < p <= T_S(q) not proved), Lean c7 scope kept
    conditional (README lists unbuilt class-seven modules). 170 pp., clean. OWNER DECISION:
    restructure the 167-pp companion (project-log character, 184 \file paths).
    Threshold-8 (-threshold-8.md, checked -8-check.md, app:s2-local, I216):
    square gap NOT closed; proved every p = 1 mod kappa with p <= kappa^2-3kappa+3
    is in E_2(kappa); r-row obstructions silent above ((r-1)kappa^r+2)^2; exact
    E_2(10) to 8191 (non-members 3361 3761 5821), E_2(12) to 10453 (all members);
    Poisson heuristic 1.47-1.57 kappa^((kappa+1)/2) kept as conjecture, not in paper.
    Threshold-9 (-threshold-9.md, checked -9-check.md, rem:app-s2-joint-moments,
    I220): exponent kappa^kappa NOT beaten; conditional on the AI-only central-
    moment bound (threshold-2 Thm 5), p >= 6 kappa^kappa+1 is outside E_2(kappa)
    for kappa >= 729; barrier: bounds valid for every law with Lemma 2's brackets
    cannot certify p <= kappa^kappa/2 (special case of the BGP barrier).
    Lean class seven (-lean-c7.md): BCHClassSeven, BCHClassSevenSubgroups,
    ReesGeneralLawClassSeven build with --wfail, no sorry, 509 guards (471 for
    the paper); lcm of BCH denominators 30240, needs p >= 11. Side finding:
    Sage 10.9 bch_iterator wrong from degree 6. Checked (-lean-c7-check.md, no
    Error), paper + core say class three to seven, c >= 8 outside (I217).
    Lean SDE solvers (-lean-sde-solver.md, formal/Formal/ReesSdeSolver.lean,
    standalone, not yet wired/guarded): computable triangular kappa=2 solver
    (triSolve_spec, (a+1)(a+2)/2 columns), quadSolveZMod_spec (contraction by
    search), linear kappa=1 (linSolve_spec, a+1), exhaustive CW search at
    kappa a+1; running time unproved. Integrate after the c7 check (same table).
    IS restarts, composite kappa (-is-restarts-composite.md, checked -check.md,
    rem:is-runtime, I219): exact worst case rho = nu - min_q v_q((p-1)/kappa) runs
    for the variant, nu+1 tight for the default; no run bound in kappa alone.
    Open: a bound in (kappa_d, g_d).
    Lean SDE solvers + (R) module (-lean-sde-solver-check.md, I218): ReesSdeSolver
    (computable kappa<=2 solvers, CW search) and ReesMergeReduction (step R) now
    imported and guarded; full lake build --wfail OK (3524 jobs); 538 guards
    (500 for the paper table + 38). tab:lean-modules split into 3 parts.
    Schedule 3 witness sampler h>=3 (-s3-witness-h3.md, checked -h3-check.md,
    rem:fc-witness-h3, I221): Theorem H, weight doubling on mu_h u {0}, arity
    degree 1+j*_h (2-3 at the test primes vs Schedule 1's 4-40); depth barrier
    j*_h = log2 p/phi(h)+O(1). With these nodes Schedule 3's classical node work
    is polynomial at fixed c for every p > c, at more queries (query exponent 19
    at c=9; log2 Q 93-151 vs 34-42 on the class-nine profile); no speedup.
    The "answers prop:rc-lower's question" claim was REJECTED (framing error).
    OWNER DECISIONS OD1, OD2: both APPLIED 11-05 (I232, I234).
    Morning 11-05 (I223-I227): k9 sweep to 9^9/2 (I223); Lean ReesS2Local
    (two-row + divisor lemmas, Prop cyclotomic (i),(ii): p <= kappa^2-3kappa+3 =>
    p in E_2(kappa); 552 guards, 514 table; checked faithful, I224); receiver round 3
    (n4(F_5): exact whole-circuit law for gamma_2 and <e1+e2,e3> via two hand-proved
    coset lemmas; other 7 subgroups conditional on 13 label tuples; p=7 sources;
    checked, I225); referee-16 (Fable) on all overnight additions: 0 Error, 0 Gap,
    6 Imprecision, 4 Style, all applied (I226; kappa^kappa/2 barrier now "argued").
    Referee-17 (Fable) on core/main-core.tex: major revision, 0 Error, 2 Gap, 16 I, 4 S;
    20 applied (I227, -referee-17-applied.md; core 28 pp. clean). OWNER DECISIONS (resolved 11-05, see Late morning):
    OD3 restate thm main with an abstract arity A_d and an Ivanyos-Santha corollary
    (or have a human confirm the AI reading of arXiv:1503.09016v2 behind B_d and
    exponent 145) -- ready-to-apply draft, 29 pp. clean, in
    audits/reviews/2026-11-05-rees-od3-draft/ (main-core.tex, od3.diff; companion port
    companion/od3-main.diff, 179 pp. clean; NOT applied);
    OD4 cut the core Outlook to half a page -- draft in
    audits/reviews/2026-11-05-rees-od4-draft/ (od4.diff alone: 26 pp.; od4-on-od3.diff after
    OD3: 27 pp.; both clean; NOT applied). A second AI reading of IS 2015
    (-is2015-second-reading.md) confirms the B_d reading with caveats; page locators added
    to core rem:is-printed (I228). Still needs a human check (IS pp. 3, 7, 8-10).
    Local commit 88eccdd8 on branch rees-full-overnight-2026-11-05 (1632 Rees paths, through
    I227; NOT pushed; unsent outreach drafts in archive/ and big outputs excluded). Live
    dfs2b outputs keep changing after it; I228 and the STATE/handoff edits after it are
    uncommitted.
    Late morning 11-05 (I229-I239; owner decisions of 11-05 applied): OD3 READABLE variant
    (owner wants the main theorem readable): thm:main stays concrete, new rem:main-solver
    says what the proof uses from Schedule 1 (I230); the abstract-solver OD3 draft is NOT
    applied. OD4 shorter Outlook (I231), OD1 (I232), block-steered ADOPTED (I233: fcs-budget
    combined 944.9/555.4/61.5 -> 940.3/533.4/41.4 at 2^31-1/2^61-1/2^127-1; E_W unchanged),
    OD2 ADOPTED (I234: zero-sum node at Gamma_0 and h>=3 sampler at Gamma_F in (R1);
    Schedule 3 classical time polynomial at fixed c, more queries, no speedup).
    Receiver general lemma (left-translation invariance; per-tuple P_coh = P_meas; I229);
    kappa=2 witness circuit proved for every odd p given the arithmetic macros (I236); 5^12
    re-run on the current gate list passes. Square-gap barriers proved (I235;
    prop:app-s2-barrier, prop:app-s2-chebotarev); square gap still OPEN.
    Referee 18 on core: ready to send after fixes; 0E/0G; applied (I237; enumerated thm:main,
    tau for the sample surplus). Companion RESTRUCTURED into paper order with a provenance
    appendix (I238; archive in docs/papers/rees-hsp/archive/main-2026-11-05-before-restructure/);
    counterparts + a real fix in thm:uniform-compilation(iii) eps' = eta^2/(16p) (I239).
    dfs2b: 20071, 20089, 20107 in E_2(9) (1370 of 1373 kappa=9 primes still open); decided to
    16993 (kappa=8) and 16633 (kappa=9). Core 27 pp., companion 201 pp., both clean;
    PDFs in docs/papers/rees-hsp/pdf/. Expert email drafts (unsent):
    docs/papers/rees-hsp/emails/expert-emails-2026-11-05.md. Referee 19 on the restructured
    companion: audits/reviews/2026-11-05-rees-referee-19-companion.md.
    Evening 11-05 (cloud A-G collected, audits/reviews/2026-11-05-rees-cloud-batch-results.md;
    0 conflicts with local): E_2(8) on [3,20000] now EXACT (all 556 p=1 mod 8 decided; 293
    members, largest 14281; 276 witnesses re-verified). E_2(9) <= 20000: 358/372 decided,
    largest member 18793, open 18919..19963 (14 primes); 17317/17389/17443/17497 INFEASIBLE are
    cloud-only (B) until local dfs2b_9_14501 confirms. kappa=9 exceptions: 15 of first 16 are
    members. Plain-mode cross-checks now through 7577 (kappa=8) and 11593 (kappa=9). Cloud
    C/D/E/F still running past the credit window; A's long jobs lost to a container restart.
    G (native application): no natural problem found; shortlist + citation items in the file.
    Paper NOT yet updated with these numbers.
    11-07 18:10: late cloud results saved (audits/reviews/2026-11-07-rees-cloud-late-results.txt):
    C decided kappa=9 exceptions 21313 21493 21529 21601 21673 21727 21799 21817, all INFEASIBLE
    (members; 27 of 29 decided exceptions are members); E plain-mode confirmed 36 more kappa=9
    members 11701..13933 (only 13807, 14149 left); A's node counts equal local ones. Cloud
    sessions A-F archived (stopped). Local queue restarted with the 99 jobs not done anywhere.
    11-07 17:40: the other device is a locked-down Windows work laptop (no compiler), so the
    143-job brief queue runs LOCALLY instead: screen dfs2b_queue_1107 (8 jobs, nice 10),
    audits/reviews/2026-11-07-rees-dfs2b-local-queue/ (queue.txt, run.sh resumable, out/K_P_MODE.out,
    out/ALL_DONE when finished; est. ~3 days). Never kill. Re-run ./run.sh after a reboot.
    11-06 22:51: E_2(9) on [3,20000] now EXACT (local dfs2b_9_17501 DONE): all 372 p=1 mod 9
    decided, 342 members, largest 19963 (0.338*9^5); new witnesses verified. Brief phase 1 dropped.
    11-06 morning: local dfs2b_9_14501 DONE (confirms 17317-17497 in E_2(9)); dfs2b_9_17501 at
    19423; kappa=9 <= 20000 open: 19441 19477 19603 19801 19891 19963. k9sweep workers idle
    (queue of 20 done: 21061, 21169, 21277 members; 19 of 21 decided exceptions are members).
    dfs2b cost ~ p^5.6 (3 h at 21313, ~8 h at 25000, ~1 day at 30000): the 1352 open
    exceptions cannot all be decided this way. Other-device brief (147 jobs: the 4 top
    kappa=9 <= 20000, 58 exceptions <= 25000, 47+38 plain cross-checks):
    audits/reviews/2026-11-06-rees-dfs2b-other-device-brief.md. Owner copies results back.
    Older cloud sessions (20, 11-02..04) harvested 11-05 night, never saved before:
    audits/reviews/2026-11-04-rees-cloud-numeric-harvest.md (16 numeric; 250 witnesses ok,
    0 conflicts; independent solvers indep/hard29/e2k8low re-decide 9473, 9769 (kappa=8),
    17623 (kappa=9) and all 145 primes of (9769,20000], so "single run of the pruned search"
    is out of date there; sweep8 re-covers only to 1.17e8, not T_A(8)=117441563) and
    -cloud-research-harvest.md (5 research reports; ranked citation fixes for main.tex:120,
    760, 1222, 702 etc., NOT applied; SDE-session barrier and zerosum lemma superseded).
    Afternoon 11-05 (I240-I242; companion 203 pp. clean in scratchpad build, pdf/ copy still
    the 201 pp. one; uncommitted): referee 19 applied (I240). Receiver for general (G,H)
    (I241, -receiver-general-gh.md + -check.md): witness circuit proved correct for every
    kappa_d >= 3 with p not in E_2(kappa_d), given the arithmetic macros (exhaustive p <= 127);
    coherent_k3 emits provably correct coherent programs for every class-2/3 instance with
    p <= 2*10^6, poly(log|G|, log p) gates; above 2*10^6 the capped search also refuses some
    valid p. NOT the receiver of thm:main; coherent_receiver_implemented stays FALSE.
    SDE Q1 (I242, -sde-q1.md, -sde-q1-search.md, -sde-q1-check.md): rem:sde-worst-case-q1 in
    appendix-sde-side.tex. Every bank of rank r with >= floor((r+2)^2/4)+3r columns reduces in
    deterministic poly time to a solution or a flag with rounds of <= 3+c blocks; at c <= 2
    back substitution fails w.p. <= 1/2 for kappa=2, p >= max(62000,320r) and kappa=3,
    p >= max(3.75e6,2430r). c is NOT bounded (stalls needing 3 splittings in one round occur
    at a in {7,8}, all resolved by recursion), so arity stays (a+1)(a+2)/2 and Conjecture 5
    stays open. Checker says +r budget suffices (§3.1); not adopted pending one more check.
    Cloud batch (7 sessions, 5.5 h cap, results only in final messages): dfs2b A/B/C/F, plain
    cross-checks D/E (see the dfs2b bullet above), G = native-application literature search
    with citation verification. Collect, re-verify FEASIBLE witnesses locally, then update
    E_2(8)/E_2(9) and the cross-check range. Clean-copy Lean rebuild (lake --no-cache build
    --wfail, commit b117b98e) PASSED: EXIT=0, 3525 jobs, no warning/error/sorry, all 73 Formal
    modules recompiled (Mathlib prebuilt); recorded in the paper (I243).
    NEVER run make_numbers.py (even --check rewrites numbers.tex); see TRAPS 17.
  - Unanchored AI referee passes 5-11 covered every section and appendix on
    11-04 (reports audits/reviews/2026-11-04-rees-referee-{5..11}-*.md, each
    with an "Applied (11-04)" section). No open Error. Citations needing a
    human: AKS Thm 5.3, CEMM sections, Imran-Ivanyos theorem/section
    numbers, Kitaev s.5 Thm 2, Cleve-Watrous 7.1, van de Woestijne s.6/6.1
    (paper vs thesis), IMS Thm 11, ISS s.3, Bene Watts Alg 1-2, Khukhro, Kothari-ODonnell-Wu, 3 Sept-2026 arXiv IDs in references.bib,
    Lidl-Niederreiter 5.41 (grep "NEEDS HUMAN VERIFICATION" in the .tex).
  - Threshold-6 (11-05, AI only, audits/reviews/2026-11-05-rees-threshold-6.md): the square
    gap is NOT closed, but for composite kappa it is BYPASSED by a tower of coset refinements
    (one prime factor at a time). The threshold is p > max(T_A(q)[q>=5], 4kappa^{q+1}, 4q^2kappa^5),
    q the largest prime of kappa, and ((kappa-1)^2+1)^2 for kappa = 2^L. The arity
    (a+1)prod((q_t-1)a+1) has degree 1+Omega(kappa) in a, so this is not O(a^2). Exact: every
    p = 1 mod kappa is covered except a few small primes in E_2 (kappa=7: {29,43,71,113}, pending
    one re-check). Proposed .tex in report §8, not applied. Prime kappa: unchanged.
  - Square gap 11-09 (audits/reviews/2026-11-09-rees-square-gap-stepanov.md): E_2 now proved
    to contain all p <= kappa^3-3kappa^2+2kappa (lower side only). The type certificate escapes
    O1/O2 but is unproved; kappa=5 data: PW_pair < 1 at all tested primes 821-2311, but OSC's
    (H) fails at m=6. OSC' made precise (report section 11): conditionally exponent
    (1/2+o(1))kappa; no boundary term exists (refuted); spike primes are the live obstruction.
    C1 existence proved from ~kappa^kappa/(2e). 11-10 (section 12): the kappa=6 spike survey is
    complete (89 primes); the class rule H1 is refuted, the class shift held. Spikes are large-F 2+2 involution families
    plus a lifted rest. The family can move the exponent only if F*B = kappa^{Omega(kappa)}. At
    kappa=7, 36037 is a B_L spike against two equal-lambda primes (pre-registered), not carried by
    the 2+2 family. Paper not edited.
  - Open math: Schedule 2 square gap (two-level E_2 itself; for prime kappa nothing beats
    kappa^{kappa+1}); poly(kappa) threshold at arity O(a^2); o(a^2) SDE finding now PROVED whenever p/a -> inf, AI-checked, pending human review (Theorem A, audits/reviews/2026-11-07-rees-sde-subquad-A.md; audits/reviews/2026-11-08-rees-sde-uniform-p.md: O(a^2/min(log a, log(p/a))) columns, every bank; bounded p still open; paper not edited, owner decision); F_3 worst case n^2/4 + O(n^{3/2}) (audits/reviews/2026-11-08-rees-sde-p3-nest.md, AI-checked); near-linear total regime open; the nu+1 IS restarts for
    kappa with two distinct primes (prime-power kappa done, I194); kappa=8 on (11897, 20000] (running); kappa=9 above 15787.
  - All claim gates false; local commits 88eccdd8, b117b98e on rees-full-overnight-2026-11-05,
    NOT pushed (public repo; owner OK needed). Ranked list:
    REES_FULL_CONTINUATION.md (its "What full still lacks" list predates
    11-04 evening; this bullet supersedes it where they differ).
- **Retained previous written results:** PERMUTABLE_SYLOW_HSP.md gives the
  reviewed paid solvable-group/permutation HSP upper bound; explicit
  strings/graphs/codes are classically matched. PERMUTABLE_STATE_HSP.md gives
  the reviewed fresh-IID mixed-copy all-prime solvable learner, with paid
  controlled linearR, gaps, torsion preimages and termination. Its proposed
  T-conjugated application fails outside already-solved central cases.
  Prior six group controls, three density controls and 37 regressions remain
  the executed scope; they were not rerun in this pass. AG_SMALL_PARITY_SELECTOR.md
  retains conditional expected-poly search under logarithmic full Pic/2 rank.
- **Next admission criterion:** the BIT growing-prime receiver is now
  accounted for at the written-theorem level; do not keep developing its
  polar decomposition or conditioning. Re-rank independent native questions
  before another major quantum mechanism. A source-boundary extension must
  specify actual preparation and verification; the finite pure-copy case
  is already proved. A classical attack needs a
  new constructive operation. Check corpus, primary texts and exact-model
  baselines before implementation. Missing mechanisms and finite failures
  do not establish hardness.

## Live

| Direction | Where it stands | File |
|---|---|---|
| Joint-charge Gaudin eigenstate preparation | Reviewed CONDITIONAL explicit random-dephasing traversal removes classical q(s)/Bethe-root advice with paid joint gap, derivative and Pauli-time costs. Exact floor2 and now uniform1/N squared gap falsified; two-cluster native upper2312n^-5/3. M1 classically matched; finite controls alone prove no scaling. Weaker polynomial SAME-M all-path gap remains OPEN. No full algorithm, coherence, novelty, separation or execution. | `GAUDIN_JOINT_CHARGE_TRAVERSAL.md` |
| Full wild-local Kummer image by halving saturation | Reviewed all-prime polynomial iteration; new finite quotient E=2L removes exact representative relations, bounded Stoll kernel shape proved, sharp Smith/normalization losses corrected. Actual-point cosets and native polynomial ONE-HALF conditioning remain OPEN; full local/global algorithm unadmitted. Mascot good-reduction/prime-to-p and KM field-operation scopes do not close it. Exact finite controls only; no novelty, hardness, separation or execution. | `LOCAL_HALVING_SATURATION.md`, `LOCAL_SATURATION_FINITE_PRECISION.md` |
| Large-prime growing-genus local Kummer image | Reviewed WRITTEN classical polynomial-BIT complete local basis for monic odd d>=3,p>d, arbitrary bad reduction; paid all degree<=g tame fields, bounded discs, functional-span sampling, local orders and P/S/W precision. Returned frame/rank certificate; ABORT on capped failure. Core/source/final reviews and exact falsifier control. No global/small-prime/dyadic, novelty or quantum execution claim. | `LARGE_PRIME_LOCAL_KUMMER_IMAGE.md` |
| Uniform native character reconstruction | Known exp(O(d logd)) upper bound remains. Irreducible all-packet/consecutive-window success<=(3/2)d^-d. Chosen-BIT additive means and candidate-syndrome scores are classically matched; complete syndrome/mask law is exact but full independent-noise model false. No mostly-correct recurrence premise. A polynomial SQ decoder would still be valuable. Joint labels/coherence remain open; next operation must compete against independent directions, no further boundary sweep. | `LEGENDRE_HANKEL_RESULTANT_READOUT.md`, `LEGENDRE_HANKEL_SUCCESS_BOUNDARY.md`, `LEGENDRE_FOURIER_FEATURE_CLASSICAL_MATCH.md` |
| Classical native Legendre reconstruction and prior-art boundary | Can a new character-only operation match fixed-degree polynomial quantum reconstruction? Quadratic expected sqrt(p), cubic p-query quasilinear arithmetic are upper bounds, not hardness. Exact priority of the coefficient-space receiver remains open; no repeat sweeps. | `LEGENDRE_RESULTANT_HYPERPLANE_READOUT.md`, `QUADRATIC_LEGENDRE_RECOVERY.md` |
| Full-input classical counterpart for scalar OPI | Paid anchor-plane lookahead and every-table moments are reviewed, but no adaptive quality or first-witness guarantee is known. The direction family is already in published basis pivots; no solver or sweep admitted. The fixed-catalog mixing theorem is narrower. The known Johnson quantum comparator remains paid; classical matching is open. | `SCALAR_OPI_NATIVE_PRIORITY.md`, `SCALAR_OPI_RANDOM_TABLE_LIST_SAMPLER.md`, `SCALAR_OPI_ANCHOR_PLANE_ADMISSION.md` |

## Accounted-for parameter boundary

| Direction | Established result and scope | File |
|---|---|---|
| Two-cluster Gaudin joint-gap counterfamily | Reviewed finite-distinct rational sites, spacingn^-8,g1/(2n),N=2n,M=n give squared gap<=2312n^-5/3 by fusion/min-max; exact128-site bound<1/400. Uniform1/N floor refuted, weaker polynomial preparation OPEN. Known critical BCS mechanism; no novelty, superpoly-gap or separation. | `GAUDIN_TWO_CLUSTER_GAP.md` |
| Binary-Fock passive/Kerr circuit sampling | Reviewed WRITTEN full native quantum polynomial(nativebits,logK,log1epsilon) count sampler, known Prakash Cor2.3. Common coherent QHT/cutoff/phases paid. Classical bounded-time sampler matches BUNCHED input with polynomial numerical chi, using coherent rejection and binary-binomial precision; not arbitrary Fock/exponentialchi. Three reviews, five primary PDFs and exact mixture/CZ/parity controls. No novelty/separation, physical exponential-photon preparation or full/quantum execution. | `BINARY_FOCK_KERR_SAMPLING.md` |
| Compact integral similarity, growing binary integer matrices | Reviewed WRITTEN bounded-error quantum poly(native bits,log1eta) compact INTEGER unimodular witness or NO, conservatively under GRH. Known BHJ algorithm; paid compact Steinitz/conductor descent, reused local residues, fractional-sum guard, Z-linear section and Jordan-length/small-covolume determinant test. Verified unit union amplifies completeness. Two reviews and one exact classical control; expanded witness obstruction retained. No tuple extension, generic compact PIT, novelty, separation or quantum execution. | `COMPACT_INTEGRAL_SIMILARITY.md` |
| Open folded-chain coherent evolution | Reviewed WRITTEN arbitrary-input unitary fast-forwarding in poly(N,bitlength(t),log1/epsilon), complete boundary/terminal-word encoding and controlled free-fermion phases. Two reviews; four used sources/six retained PDFs; one exact classical run. Slater/CT methods match specified eigenstate and basis-input additive sparse readouts. Known bulk map; no novelty/separation, practical cost, human/formal verification, implementation or quantum execution. | `FOLDED_CHAIN_COHERENT_TRANSFORM.md` |
| Fixed-degree quintic-surface P2 | Reviewed WRITTEN bounded-error quantum polynomial(logp,log1/eta) BIT/gate exactdegree53P2 for EVERY smoothquintic/P3/Fp, nativeinput. Verifiedgeometry/arithmeticreadout/source/CRT/finiteclocks; twonewreviews/fiveprimarysources/exactclassicalcontrol. KnownSchnell/Deligne excludes verygeneralCOMPLEX Hodge-compatible abelianreplacement, NOT everyFpclassicalalgorithm. No novelty/separation, growingdegree, practicality, human/formal verification or execution. | `QUINTIC_SURFACE_P2_ADMISSION.md` |
| Fixed-degree quartic-surface P2 | Reviewed WRITTEN bounded-error quantum polynomial(logp,log1/eta) BIT/gate reduction for EVERY smoothquartic overFp from nativebinaryinput. Paid unique-divisor charts/arithmetic frame and twist construction, modular induction, exact Fourier/Newton, localLeray/CRT and finiteclocks. Fourreviews/tennewprimaryPDFs/retainedcurve source/webscope/exactclassicalcontrol. Stronger KS classical marking/descent remainsOPEN; Elkies1997 already suggestedthatroute. No novelty/speedup, growingdegree, practicalcost, human/formal verification or full/quantumexecution. | `SURFACE_TORSION_COVER_RECONSTRUCTION.md` |
| Two full Gaussian channels, diamond learning | Reviewed WRITTEN uniform polynomial-use/BIT/gate learner for EVERY exact memoryless two-map mixture, known Majoranas and ordinary qubit gates, no weight/branch/gap advice. Proper reconstruction and deterministic constant-core processor yield explicit CPTP output with full diamond guarantee. ALL data matched by nonadaptive product inputs/Pauli readout and classical processing. Five reviews/sixsources/exact classical control. No novelty, coherence/computational advantage, practicalcost, human/formal review, offmodel/many-map or full/quantumexecution. | `GAUSSIAN_CHANNEL_MIXTURE_ADMISSION.md` |
| General central-simple-algebra minimal module | Reviewed WRITTEN quantum polynomial-BIT compact primitive idempotent and minimal left ideal/action under explicit GRH, arbitrary growing expanded CSA/field inputs. Classical factoring-paid Schur index, degree-index field, known KM split map, compact Hom/right-identity extraction. Exact classical positive certificate; two reviews/eightprimary sources/one exact classical control, scoped PARI table-index unsupported receipt. No novelty/separation, human/formal review, input-canonical/expanded/integral output, division normal form or full/quantumexecution. | `CSA_MINIMAL_MODULE.md` |
| General central-simple-algebra reduced norm SEARCH | Reviewed WRITTEN bounded-error quantum polynomial-BIT compact x with Nrd(x)=a or exact HMS sign NO under explicit GRH; arbitrary growing explicit CSA/field/maximal-order input and expanded target. Prescribed splitting field, known Amitsur splitting and regular RIGHT-module transport; deterministic classical canonical positive certificate. Three reviews/fourprimary sources/exact PARI/nondivision control. No novelty/separation, human/formal review, minimal modules, integral/short/expanded output or full/quantumexecution. | `REDUCED_NORM_PRESCRIBED_FIELD.md` |
| Arbitrary relative norm equations | Reviewed WRITTEN quantum polynomial-BIT compact N_L/K(x)=a solver under explicit GRH, arbitrary growing explicit fields/maximal orders/embedding and expanded target. Relative tensor support with absolute discriminant payment, full torsion and classical LS atom relations. Full review/source audit/exact PARI control complete; extra Claude support attempt timed out/no report, billing unknown. No novelty/separation, integral/short/expanded output or full/quantumexecution. | `RELATIVE_NORM_TENSOR_SUPPORT.md` |
| Mixtures of two arbitrary mixed fermionic Gaussians | Reviewed WRITTEN polynomial-copy/BIT learner for EVERY exactIID two-component mixture, knownMajoranas/ordinaryqubitgates, no weights/gaps/components. Degree2/4/6 exterior inverse plus uniformly regularized lowrank Schur map yields direct <=4knownGaussian output. Explicit numerical ledger, three reviews and exact classical control complete. No full/quantumexecution, novelty, classicalseparation, practicalcost, offmodel/noisy or manycomponent claim. | `MIXED_GAUSSIAN_PAIR_LEARNING.md` |
| General number-field compact isotropy | Reviewed WRITTEN bounded-error quantum polynomial-BIT NO or nonzero compact isotropic point under explicit GRH; arbitrary charged field degree/form dimension, expanded compatible maximal-order input. Single5plane, paid quadratic ideal norms/weakapprox, arbitrary-splitting descent and fresh-prime compact verifier. Known Amitsur splitting reused; four reviews/seven sources/one classical exact control. No novelty/separation, human/formal review, expanded/short/integral point, compact Witt decomposition, GRH removal or full/quantum execution. | `GLOBAL_COMPACT_ISOTROPY.md` |
| Arbitrary even Gaussian-rank-two learning | Reviewed WRITTEN uniform polynomial-copy/BIT learner from exact IID copies, knownMajoranas, no branch/frame/weight/gap/overlap advice. Covariance grouping, cancellation-safe merge/fourmode dichotomy, positive R2 pairing/catfallback, low-nu orientation, known coherent MPS endpoint and fresh validation. Four reviews/sixsources/one exact8mode control. No noisy/generalrank, novelty/separation, human/formal review or full/quantum execution. | `TWO_GAUSSIAN_PAIR_LEARNING.md` |
| Two-Fock Gaussian basis learning | Reviewed WRITTEN polynomial-copy/BIT learner for all exact parity-definite sharedGaussian two-Fock states, known physical Majoranas, no weight/frame advice. Connectedquartic isolated eigenvector, uniform polar rounding, fixed4 fallback, fresh phase/readout validation. Actualsource/core reviews and one exact7mode/6active control. No general sparsity/noise/unknownMajoranas, novelty, separation or quantum execution. | `TWO_FOCK_GAUSSIAN_LEARNING.md` |
| General sparse algebraic-constant lattice | Reviewed WRITTEN classical polynomial sparse-BIT FULL Alg for arbitrary charged growingdelta, s,k,binaryTdegrees; implicit derivativebounds, prime/congruence/LLL fullrecovery. Direct-specialization/naiveLC falsifiers scoped; one quarticcontrol. FullRel constants remain OPEN; no genericmap, novelty, separation or full/quantum execution. | `GENERAL_SPARSE_CONSTANTS_ATTACK.md` |
| Cyclic-support monomial Galois descent | Reviewed WRITTEN quantum polynomial-BIT compact torus-torsor trivialization under GRH, explicitly charged Galois field/group/action/cocycle. Primitive cyclic support; complete S-units; existing LS full atom relations, torsion and integer solving; deterministic positive verifier. Four reviews/one classical finite control. No novelty/separation, succinct splitting-field construction, expanded/integral/short output, GRH removal or full/quantum execution. | `CYCLIC_SUPPORT_MONOMIAL_DESCENT.md` |
| Tensor-square rational norm equations | Reviewed WRITTEN quantum polynomial-BIT compact rational norm solver under explicit GRH, arbitrary growing degree and supplied maximal-order table. Unconditional paired-norm support lemma; tensor discriminant pays polynomial support without auxiliary fields/closure. Complete compact S-units and exact gcd-free/sign/HNF endpoint. Prior support methods and HNP existence baselines retained; one exact control only. No novelty, separation, integral/short output, GRH removal or full/quantum execution. | `TENSOR_SQUARE_RATIONAL_NORMS.md` |
| Arbitrary-Pauli Clifford-hidden magic learning | Reviewed WRITTEN polynomial copy learner for all exact C exp(-i*pi*P/8)H^n, arbitrary signed Pauli/support. Largew deletion/K3 gap and old cubic axes; smallw uniform gap and direct tomography; complete source/error review. Crude structural gap inverse ~1.35e16, not practical. Four finite controls, no full/quantum execution, novelty, separation, noisy/angle/MPS/channel claim. | `ARBITRARY_PAULI_MAGIC_LEARNING.md` |
| One-rotation Clifford-hidden magic-state learning | Reviewed WRITTEN copy-based polynomial learner for every n>=4 exact C exp(-i*pi*Z^n/8) H^n. Cubic Bell gap, uniform Lie/square-zero/degree3 Macaulay axis list, capped product primitive and fresh-copy known-circuit verification; approximate epsilon output, no advice. Width n; exact finite controls only, no full learner/quantum execution, novelty, classical separation or generic noisy/MPS extension. | `ONE_ROTATION_MAGIC_LEARNING.md` |
| Good-dyadic growing-genus two-Selmer dimension | Reviewed WRITTEN bounded-error quantum polynomial-BIT composition for explicit smooth good-Z2 models, odd-Galois branch fields and good odd p<=d. Paid local trace/shallow formal/O8 coordinates, large-p images, global compact arithmetic and aggregate errors. Nonvacuous unbounded Q x K x K family; duplicate-field baseline retained. Exact finite controls only; no execution, novelty, separation, arbitrary curve or MW rank. | `GOOD_DYADIC_GROWING_SELMER.md` |
| Fixed-field bounded-degree contraction baseline | Reviewed WRITTEN source-based exact classical sum-product with explicit L>=n, fixed Q(zeta8), constant arity/occurrence. Subexponential n and polynomial BIT space; explicit H,T,CNOT ONE amplitude inherits n<=2G. Exact supplied-design control only; no whole ETH-paper/sharper appendix, polynomial/qubit-count simulation, sampler, novelty or quantum advantage. | `BOUNDED_DEGREE_CONTRACTION_BASELINE.md` |
| Growing-degree monomial Kummer sparse relations | Reviewed WRITTEN classical polynomial sparse-bit full Rel for irreducible Y^delta-a*T^v, growing s,k,charged delta and binary exponents. Paid monomial constants, compact LC, derivative/LLL and original-small-tuple LS; one exact delta6 torsion/control case. No general f, poly(logdelta), novelty, separation or full execution. | `MONOMIAL_KUMMER_SPARSE_RELATIONS.md` |
| Sparse characteristic-zero function-field relations | Reviewed WRITTEN bounded-error quantum polynomial-bit composition for explicit Q(T)[Y]/monic irreducible f, growing s,k,charged delta and binary sparse T degrees. Full constant-relation bit bound, large-prime content/point-norm union, finite-ring HSP and exact LLL paid. Full CLASSICAL polynomial sparse-bit solvers for degrees1 and2 using derivatives and original leading coefficients; quadratic cancellation uses one norm. One exact binary-exponent control; no advice, arbitrary ideal conversion, novelty, separation or full execution. General classical complexity unknown. | `SPARSE_CHARZERO_FUNCTION_FIELD_RELATIONS.md` |
| Sparse function-field relation lattice | Reviewed WRITTEN bounded-error quantum polynomial-bit algorithm for explicit Fp(T)[Y]/monic irreducible f; growing s,k,charged delta and binary sparse T degrees. Uniform basis bound, finite specialization norm union bound, full-ring HSP and exact nonsaturated LLL prefix paid. Randomized-polytime Turing equivalent to finitefield DLog without integer factoring; whole fixed-p classical quasipolynomial comparator. Exact controls only; no arbitrary ideal conversion, novelty, separation or quantum execution. | `FUNCTION_FIELD_RELATIONS_RANDOM_SPECIALIZATION.md` |
| Growing-tuple affine unit relations | Reviewed WRITTEN deterministic CLASSICAL polynomial-bit composition for PRIME affine Q-algebras at fixed variable count and growing supplied unit/inverse tuples; char0 PRIME Z-domain corollary. dlog/Hermann, explicit generic finite specialization and unrestricted LS relations paid without huge powers. Two exact controls; no complete units/class/PIP, general metabelian, positive-characteristic, novelty or full execution claim. | `AFFINE_UNIT_RELATIONS_DIFFERENTIAL_SPECIALIZATION.md` |
| Classical chosen-sign Fourier feature estimation | Independently reviewed exact unbiased bounded estimator for any fixed F and public shift, polynomial(m,logp,epsilon^-1); adaptive robust SQ and public subspace-score extension. Root-free mask marginal identity; exact full-noise counterexamples; one reused p5 classical control. No full-label simulation, copy-only classical access, decoder or speedup claim. | `LEGENDRE_FOURIER_FEATURE_CLASSICAL_MATCH.md` |
| Prime-index factorial, odd prime ell dividingp-1 | Independently reviewed WRITTEN unconditional bounded-error quantum poly(NUMERICAL ell,logp,log1eta) for every input. Uniform fields, SAME-action Fitting, balanced generator and confidence are paid. Section10 removes physical Gauss-phase calls by consistent-embedding covariance; quantum factoring/S-units remain. Exact mismatch law and ell5,p11 controls; no quantum execution, novelty, separation, arbitrary factorial or poly(logell) claim. | `PRIME_INDEX_FACTORIAL_RESIDUE_NORMALIZATION.md` |
| One-third factorial, binary prime p1mod3 | Independently core/source and actual-text reviewed WRITTEN unconditional bounded-error quantum poly(logp,log1eta), every p>=7. Degree3/6 fields; one complete compact S-unit event, SAME-action class Fitting, known Gauss phase/classical L1, integer Hilbert90 and normalized local residue. Compact precision and final-integer majority paid. Durable p313 orientation/sign/pole controls only; no quantum execution, novelty, separation or general factorial. | `THIRD_FACTORIAL_CUBIC_CIRCULAR_UNITS.md` |
| Odd-degree class groups, explicit maximal order | Reviewed WRITTEN unconditional canonical invariant factors: poly(b,n,logD,log1eta) for Galois odd degree; Section6 gives poly(b,n!,logD,log1eta) for ANY odd degree, polynomial only at FIXED degree. Actual Stark gap controls the permitted principal exceptional term on a larger dyadic interval. Raw classical prime source, full compact S-units/SNF and canonical majority are paid. Prior certified C2xC2 cubic control reused; no general even-degree, CM, novelty, separation or execution claim. | `ODD_GALOIS_CLASS_GROUP_COMPOSITION.md` |
| Scalar OPI exact anchor-plane scoring | Reviewed written O(mq+q²logq) integer scoring after preprocessing, plus field work. Every-table line mean and plane mean/variance are anchor-independent; adaptive tails remain open. Strict ascent gives only local optimality. One F8 exact algebra control; no quality or execution claim for a full search. | `SCALAR_OPI_ANCHOR_PLANE_ADMISSION.md` |
| Elliptic2-Selmer dimension, monic irreducible cubic | Reviewed WRITTEN UNCONDITIONAL bounded-error quantum poly(coefficient bits,log1eta) for EVERY retained cubic, including non-Galois. Fixed-degree Stark/TZ source replaces GRH factor base; maximal order, complete T-unit mod2 kernel, small representatives and local/real clocks are paid. Actual SiksekSmart1997 descent is prior art. Published-machinery composition; two existing controls reused. No MW rank, points, covers, novelty, separation or quantum execution. | `ELLIPTIC_TWO_SELMER_COMPOSITION.md` |
| Classical inverse-norm ideal sampling | Independently core/actual-text reviewed sampler with factorization, TV epsilon, polynomial(field input,n,B,log1epsilon) clock for s=1+1/B. No GRH, quantum factoring or class advice. Normalized class coverage remains UNKNOWN, and the bounded-norm law differs. No implementation, novelty or unconditional class-group claim. | `UNCONDITIONAL_CLASS_GENERATOR_ADMISSION.md` Section5 |
| Nonreal Dirichlet L1, explicit prime-conductor character | Reviewed CLASSICAL randomized additive-epsilon and relative/log-magnitude/circular-phase-delta approximation in poly(q,logp,1/epsilon or1/delta,log1rho), unconditionally. Dyadic importance law, periodic tail, effective nonquadratic lower bound and confidence/bit costs paid. Exact p13 normalization falsifier; no full confidence experiment, exact L0, quadratic-relative or novelty claim. | `FIXED_ORDER_DIRICHLET_L0_RECONSTRUCTION.md` Section9 |
| Exact Dirichlet L0, power-of-two character order | Reviewed WRITTEN under-GRH bounds for p=1+qk, k odd, public root: fixed-q C(q)*poly(logp,log1eta); public-H poly(q,H,logp,log1eta) clock on h(F+)<=H; ALL-q EXPECTED poly(q,h(F+),logp,log1eta). Paid field/class/Fitting and full-unit index-scaled coordinates; exact2-part, compact CRT and phase. Preferred analytic approximation is unconditional classical Monte Carlo; full class arithmetic still uses GRH. Existing q8,p41 control covers index1 only. No general polynomial h bound, Weber claim, novelty, separation or quantum execution. | `FIXED_ORDER_DIRICHLET_L0_RECONSTRUCTION.md` |
| Canonical quarter-factorial, binary prime p5mod8 | Reviewed WRITTEN bounded-error quantum composition under GRH, polynomial(logp,log1eta). Paid quartic class module/action and oriented L0; classical Gauss phase and Hmod16 reuse one real S-unit block, with joint-pair amplification. Two number fields only. Certified p13/101 controls; no quantum execution, novelty, separation or general-prime extension. | `QUARTER_FACTORIAL_QUARTIC_ARITHMETIC.md` |
| Canonical half-factorial, explicit binary prime | Reviewed WRITTEN bounded-error quantum composition under GRH, polynomial(logp,log1eta), using known congruences and one compact S-unit call. Shared class/unit success, primitive positive-unit normalization and ramified residues paid. Eight certified classical controls, no quantum execution or classical separation. | `HALF_FACTORIAL_COMPACT_ARITHMETIC.md` |
| Explicit low-degree mixed-tensor Levi source | Reviewed classical polynomial recovery from the actual dense/sparse tensor, d<p-1 and p>=128n, exact finite stabilizer promise. Lie stabilizer equals block End algebra; commutant yields both summands. No finite/algebraic-stabilizer equivalence assumption or high-degree/opaque-source claim. | `LEVI_TENSOR_AND_MQ_ADMISSION.md` |
| Unbalanced two-block Levi, opaque coset oracle | Reviewed WRITTEN quantum recovery for r>s>=1,p>=128n: O(n log1eta) coherent calls, O(n² log1eta) total evaluations, polynomial(n,logp,labelwidth,log1eta) work, exact-on-success and ABORT<=eta. Strong WRITTEN classical star-collision/membership baseline O((p^(3s/2)+r p^s+n²)log1eta). Finite algebra control complete; full algorithms not run. No balanced/small-p theorem, novelty, classical lower bound or non-oracle application. | `UNBALANCED_LEVI_COSET_RECOVERY.md` |
| Extension-field Legendre chosen-query recovery | Independently reviewed WRITTEN exact-on-success recovery for EVERY monic squarefree degree-d Q over public Fp^r, r>=2, p>=65536(rd)^2. Two decoded translated norms and a gcd; O(p log1eta) queries, polynomial(p,r,d,log1eta) work, ABORT<=eta. Proper-subfield coefficients covered. F49 algebra control complete, native decoder not run. No unrestricted polylogp, passive/copy-only, repeated-factor or fixed-small-characteristic claim. | `EXTENSION_CHARACTER_NORM_GCD_RECOVERY.md` |
| Hidden field norm character, chosen-sign classical baseline | Reviewed WRITTEN O(p n log(n/eta)) query and poly(n,p,log1eta) reconstruction for all invertibleL, n>=2, p>=65536n². Verified line decoding, public field and Frobenius alignment; exact normalized product/norm. No copy-only transfer, high-p execution or polynomial-logp claim. | `HIDDEN_FIELD_CHARACTER_ADMISSION.md` |
| Singer standard-coset copy complexity | Direct reviewed application of published0604174 Thms2.3/2.5 gives Theta(n) copies at fixed error for GL_n(Fp), oddp, asn grows. Old Omega(n²), universal collision and gate-bound arguments withdrawn; no efficient measurement or native sign-to-coset reduction. | `HIDDEN_FIELD_CHARACTER_ADMISSION.md`, `SINGER_CYCLE_TORAL_HSP_OBSTRUCTION_DELIGNE_LUSZTIG_BARRIER.md` |
| Exact repeated Jacobi reconstruction, all conductors | Published September2026 Tal Thm1.5/Section3.1 already gives classical poly(q,logp) exact J_a and residues modp,p² for every q dividing p-1 and1<=a<q, with compatible character/prime. Independent source audit plus reviewed alternate full-group-ring reduction. No LS/GS/factorial execution, novelty or same-runtime-exponent claim. | `JACOBI_GROUP_RING_RECOVERY.md`, `audits/sources/jacobi_classical_eccc_2026_211.pdf` |
| Affine quadratic global-copy reconstruction | Independently reviewed written poly(n,logp,log1eta) projective learner for every n>=3, invertible A, arbitrary b,c and p>=256T=O(n^2). Random measured slices plus paid t!=0 homogenization share one adjugate relation; no chosen-slice access. Original-copy validation and caps paid. Three source controls, separate native moments and reviewed unimplemented sqrt(p) classical baseline. No novelty/separation/quantum execution. | `AFFINE_QUADRATIC_CHARACTER_SLICE_READOUT.md`, `audits/reviews/2026-11-06-affine-quadric-classical-scope.md` |
| Toric point-count accuracy comparison | Written classical poly(input,logq,1/epsilon) comparison for all odd-characteristic Newton-nondegenerate bounded-rank/bounded-entry explicit Laurent inputs. Both the s>rho ambient/weight branch and s=rho exact fixed-order Jacobi/Pila branch independently accepted. Four prescribed exact controls, no Pila/quantum execution. General degenerate s>rho remains UNKNOWN; published quantum theorem remains valid. | `TORIC_POINTCOUNT_ACCURACY_BASELINE.md` |
| Global quadratic-character copy reconstruction | Independently reviewed written poly(n,logp,log1eta) projective reconstruction for nonsingular symmetric A, oddn>=3,p>=16n^2, exact fresh GLOBAL padded copies. Dual-cone Fourier law, uniform rank escape, fresh-label verification and precision paid. Oracle upper bound already a univariate corollary; classical O(n^2p)-query baseline and four below-threshold controls retained. No novelty/separation/execution or even/smallp/noise claim. | `QUADRATIC_CHARACTER_CONE_READOUT.md`, `audits/reviews/2026-11-05-quadric-classical-scope.md` |
| Uniform Hankel character receiver | Independently reviewed written exp(O(d logd))*poly(logp,kappa^-1,log1eta) reconstruction for every monic squarefree degree-d Q, d>=2, with polynomial prime threshold. One 2d-1-copy outcome, public Hankel solve, fixed-corruption recurrence, statistical verification, uniform gates and polynomial active space paid. Five below-threshold algebra controls; no poly(d), novelty, separation or execution claim. | `LEGENDRE_HANKEL_RESULTANT_READOUT.md` |
| Fixed corrupted-character reconstruction | Independently reviewed fixed-degree polynomial quantum decoding for every fixed rho<1/4 and sufficiently largep. ONE corrupted function, fresh pure copies; exact subset overlap, statistical verification and caps paid. No mixed/device noise or growing-degree efficiency. | `LEGENDRE_CORRUPTED_CHARACTER_READOUT.md` |
| Squarefree padded-character reconstruction | Independently reviewed fixed-degree polynomial quantum composition for every squarefree monic Q and sufficiently large prime p; no hidden root flags. Virtual product-algebra support and fresh-copy verification paid. p11 padded collision and repeated-factor impossibility retained. | `LEGENDRE_SQUAREFREE_RESULTANT_READOUT.md` |
| Fixed-degree resultant-hyperplane Legendre reconstruction | Independently reviewed written polynomial-in-logp quantum algorithm for each fixed d>=2 and sufficiently large p. Fresh pure native copies, paid clean coefficient encoding, abelian QFT, uniform rank growth, capped verification. No growing-degree, all-small-prime, execution, novelty or separation claim. | `LEGENDRE_RESULTANT_HYPERPLANE_READOUT.md` |
| Cubic native full-table classical reconstruction | Independently proved p-query O(M(p)logp+p) field-operation recovery for every irreducible cubic p>=23; rank-gap/Wronskian proof. p13 exceptions refute a broader threshold. Not polylog and not classical hardness. | `audits/reviews/2026-11-05-cubic-character-window-review.md` |
| Growing-prime irreducible-quadratic Legendre reconstruction | Independently reviewed written polynomial quantum composition using paid partial spherical transforms and a Gauss-phase adjoint. Fresh pure phase copies suffice; BIT and uncontrolled phase-query corollaries pay every preparation, verification copy and capped retry. No quantum execution, novelty, speedup or classical separation. | `QUADRATIC_LEGENDRE_SPHERICAL_READOUT.md` |
| Native binary random-table Johnson sampler | Reviewed second-moment source certificate pays known complete-list quantum sampling, with high probability over one original IID full-table instance. Polynomial full-input cost and global abort/precision budgets; perfect search for fixed R>3/4. No new mechanism, capacity claim, classical hardness or quantum execution. | `SCALAR_OPI_RANDOM_TABLE_LIST_SAMPLER.md` |
| Quadratic character reconstruction over fixed-characteristic extension fields | Written polynomial-time quantum composition from published hidden translation and paid character transforms, independently reviewed. Fixed oddp,q=p^n,n growing; effective field and Q2 or compiled raw-phase access. No growing-prime transfer, novelty, separation or executed quantum decoder. | `QUADRATIC_LEGENDRE_RECOVERY.md` |

## Parked: reopen only with a new input, theorem or application

| Direction | Why parked | File |
|---|---|---|
| Native indefinite ternary integral isometry | Full growing-number-field decision route UNADMITTED: common ambient/support and local transporter offsets OPEN. Classical polynomial-BIT dyadic stabilizer spinor generators now paid via Beli/Voight; ordinary-Cl shortcut refuted by exact same-genus/nonisometric3-neighbor family. Two closed reviews/two exact component controls. Reopen for an actual native transport/relative obstruction operation, not another local variant; no novelty, hardness, separation or execution. | `INDEFINITE_TERNARY_SPINOR_ADMISSION.md` |
| Rational Gaudin determinant-prefix preparation | Direct on-shell determinant deletion refuted on a valid rational eigenstate; same-prefix single Cauchy dual also impossible. Cauchy amplitudes are paid, ALL-prefix norms are not. Any classical prefix routine also pays Born sampling and sparse readout. Two CLOSED reviews and exact classical control; Claude repair timed out EMPTY, billingUNKNOWN/no retry. No full preparation, hardness, general no-go, novelty or separation. | `RATIONAL_GAUDIN_PREFIX_ADMISSION.md` |
| General growing-genus two-Selmer dimension | Native arbitrary bad/small/wild/dyadic input under explicitGRH not admitted. Existing global arithmetic does not pay complete local image. New halving route has reviewed polynomial iteration for every prime; finite-quotient and bounded-kernel structure now proved, but stable native ONE-HALF remains OPEN (LOCAL_SATURATION_FINITE_PRECISION.md). Reviewed all-genus oddp family has dimension1 but all unramified curve-point traces vanish; ramified branch witness exists. Uniform polynomial source can be exponentially rare. Actual regular-model equations/chain bounds do not yet pay total BIT work or effective divisor lifts. No general no-go, hardness, novelty or execution. | `WILD_LOCAL_SELMER_ADMISSION.md` |
| General sparse-Fock quadratic-torus completion | Reviewed Paleyr=n constant-gap counterfamily has identical complete degree2/4 means for every passive rotation. Known Cartan twirl proves polynomial U-independent lists fail polynomial approximate support with exponentially high probability. No pureGaussian compression even one mode at small constant error. Higher/joint/coherent data and unrestricted Gaussian frames remain open; no generallearning lower bound. | `SPARSE_FOCK_TORUS_FALSIFIER.md` |
| Hidden cubic phase learning admission | Specific six-copy covariant processors additionally rejected in CUBIC_COVARIANT_COPY_PROCESSOR.md; general contract remains PARKED: exact-copy unknown Clifford/occurrence2 cubic family. Reviewed factored-event gap pays false-product exclusion, not full K5 or phase-frame extraction. Supplied-description classical Bell sampler and one width6 control; no native hardness, learner, novelty, separation or quantum execution. | `HIDDEN_CUBIC_PHASE_LEARNING.md` |
| Elliptic divisibility character reconstruction | Reviewed exact full-source normal form reduces all indices to chi(2y(mP)); collision classes are public-reference multiplier-stabilizer cosets. F7/order13, generic-j F13/order5 and an infinite p3mod8/generic-j fixed-order7 family prove all-index ambiguities. No informative receiver or efficient decoder; stronger classical attacks UNKNOWN. Reopen only with a new paid operation or decisive attack, not generic hidden-shift relabeling or a separation sweep. | `ELLIPTIC_DIVISIBILITY_CHARACTER_ADMISSION.md` |
| Coherent Gaussian pair cooling | Section10 independently reviewed: centered branch exponentially rare above smoothing; all-branch Babai correction is approximate and its proved regime is directly classically sampled using the full Gram-Schmidt profile. Binary-tree copies/errors charged. No general coherent-cooling impossibility; reopen only with a paid operation outside this sufficient regime and a native decoder. Older note sections not newly promoted. | `STRUCTURED_EDCP_KLEIN_DUALITY_AUDIT.md` Section10 |
| Reciprocal-trace Boolean hidden shift | Paid spectral construction retained for n>=3, but known injectivization+Simon already supplies polynomial recovery. Full-value classical negative does not transfer; no native application or hardness claim. | `RECIPROCAL_TRACE_SHIFT_SCOPE.md` |
| Affine-projection Legendre decoder and homogeneous Fourier readout | Exact affine herald1/(p-1)^2; homogeneous direct Fourier probabilities uniform for every balanced projective-line coloring. Reopen only for a different paid operation; not a native decoding impossibility. | `QUADRATIC_LEGENDRE_RECOVERY.md` |
| Legendre matrix-coset additive-Fourier receiver | Paid bit-Q2 source, but after discarding oracle labels the full measured matrix law is exactly secret-independent. Reopen only with a different informative paid operation; retained labels and coherent/collective readouts are outside the falsifier. | `QUADRATIC_LEGENDRE_MATRIX_COSETS.md` |
| Scalar-OPI greedy Algorithm H probe | Seven native witnesses verified; q256206/203, q512396 below DQI414.037 on the predeclared continuation. Finite baseline retained. Reopen only for a new constructive operation or source-correct theorem; no asymptotic failure claim or new sweep. | `SCALAR_OPI_FOURIER_ELIMINATION.md` |
| Freeze-aware scalar-OPI FFT repair | Six native cases completed and independently verified; larger tested scores missed DQI. Reopen only with a concrete operation addressing the retained joint correlations, not a larger sweep. | `SCALAR_OPI_SOFT_DECODING.md` |
| Further permutable Bose StateHSP applications | Complete written learner reviewed. T-conjugated noncentral involutions fail permutability; surviving central cases already abelian. Reopen only with a motivated native family passing the source/gap and existing-learner filters. | `PERMUTABLE_STATE_HSP.md` |
| Ordinary permutable-HSP native applications | Written solvable/permutation upper bound retained. Explicit permutation-action strings/graphs/codes are classically matched via public Sylows and Luks. FullUT_D symbolic-polynomial promise forces normalH, already IMS. Reopen only with a distinct motivated native model. | `PERMUTABLE_SYLOW_HSP.md`, `CLASS_THREE_APPLICATION_AUDIT.md` |
| Fixed-field complete-AG full-support syndrome, general campaign | New low-r2 classical SEARCH branch; full tower rank and non-enumerative selector unresolved. Marked-only selection refuted on about half the source. Fresh norm clock exponential. Reopen only with a new mechanism, not source-generation or more parity tables. | `AG_SMALL_PARITY_SELECTOR.md`, `NORM_SAMPLER_CLOCK_FALSIFIER.md` |
| Weak surface IsERP and local attacks | Conditional full-output theorem retained; arbitrary-ell output correction proved. No distinct native payoff after bounded audit. Cayley membership is not K recovery; native geometry remains outside restricted lower bounds. | `SURFACE_THEOREM_PRIORITY_AUDIT.md`, `SURFACE_CAYLEY_MEMBERSHIP.md` |
| Additive full-suborder EndRing | Independently reviewed composition removes specific reference/norm assumptions relative to imported PPAV contracts; same endpoint already published heuristically. Needs new native input payoff, not more dimension128 wiring. | `bundles/additive-source-independent-review-2026-10-26/REVIEW.md`, `bundles/full-suborder-impact-audit-2026-10-26/IMPACT_AND_INPUT.md` |
| Rees nilpotent HSP cover reduction (c<p) | Fixed-class, growing-prime polynomial-time composition. AI proof check (11-01) found steps 1-5 hold under Schedule 1, no gap; AI priority check: A2/A4 partly known via Ivanyos-Santha, A1 possibly new, search thin. 11-02 AI checks: fpt-r, ring-to-field, black-box, codimension, subspace, compilation and filters all survive with closable text gaps; combined Schedule 1/2 rule valid for all p>c; solver and exact simulator built; round 2 made `docs/papers/rees-hsp/main.tex` the full paper with appendices A-E (125 pp. after the 11-04 passes, I152); gaps ranked in `REES_FULL_CONTINUATION.md`. Human review and an A1 priority note still required; all claim gates false. No native application. Single-evaluation pullback is dilation-invariant only when H>=[G,G]. | `REES_HSP_REDUCTION.md`, `audits/reviews/2026-11-01-rees-core-proof-check.md`, `audits/reviews/2026-11-01-rees-priority-check.md` |
| Genus-two shifted-norm selector | Open but bypassed for the reviewed fixed-dimension16 source. Reopen only for a motivated genus-two-only requirement. | `SIEGEL_CAYLEY_REPOLARIZATION.md` |
| Rees applications | None survived; the 11-02 search is a reviewed negative (classical-input channels all classical; shift-and-phase family is Ivanyos-Santha Section 5). Residual: succinct degree>=p objects or opaque labels. | `audits/reviews/2026-10-30-rees-application-selection.md`, `audits/reviews/2026-11-02-rees-application.md` |
| Siegel/symplectic HSP reductions | Source recovered and complete conditional chain audited; no distinct native application currently justifies more receiver work. | `SYMPLECTIC_CHAIN_RING_DIGIT_REDUCTION.md` |
| SDE solver campaign | Stopped. The regular-pivot backend was declined because Boolean enumeration matches it. | `PIVOT_REGULARITY_DECISION.md` |
| Inverse-trace uniform sampling | No useful reduction needs the full law. No more backends. | `INVERSE_TRACE_SAMPLING_DECISION.md` |
| Mersenne reciprocal-trace | Published machinery, no reduction, classical witnesses. | `MERSENNE_TRIAGE_DECISION.md` |
| Quaternion compact-orbit receiver | No polynomial decoder, and Cartesian readout is classically simulable. Re-entry needs a native family with an affordable contraction. | `QUATERNION_ARITHMETIC_RECEIVER.md` |
| Arithmetic orbits (pencils, tensors, PIP) | Known machinery or classical. Needs a native problem whose format grows. | `ARITHMETIC_TENSOR_DIRECTION_AUDIT.md` |
| Goppa quantum access | Needs a quotient map that preserves the characteristic. Held-out readout costs 2^rank postselection. | `GOPPA_LOCAL_QUOTIENT_PRESENTATION.md` |
| Parabolic / Lie-type matrix HSPs | n=3 (SO6/SL4) is prior art. Recovery for n>=4 orthogonal is proposed, with novelty unresolved. The 10-11 negatives are withdrawn. | `PARABOLIC_CUT_LIST_CORRECTION.md` |
| Prior structured DQI/OPI-family decoders (polar Gibbs, MPI, Hermite, chirp) | Each tested decoder met a classical competitor or prior art. MPI is a failed transfer, not hardness. The new scalar TABLE-source classical question above is separate. | `HERMITE_DECODER_PRIOR_ART.md`, `../docs/papers/classical-competitors/` |
| Ternary/F3 syndrome filtering | Two tested corrections were falsified, and Kothari et al. cover fixed positive density. Structured optimized Q is not excluded (review pending). | `TERNARY_SYNDROME_CORRECTION.md` |
| Other DCP sources and sieves | Reserve until a concrete new rule. Retrieved November Simon mirror leaves decoder operations unchanged; official-byte identity UNKNOWN. No re-entry from a revised explanation or date. | `DCP_SIMON_OCTOBER_REVISION_AUDIT.md`, `audits/reviews/2026-11-05-simon-november-source-delta.md` |
| Code equivalence / GI collective observables | No concrete receiver. | `NONABELIAN_BARRIER_SCOPE_AUDIT.md` |
| Symmetry and noisy-phase learning | Scoped learners built on known theorems. | `audits/reviews/2026-10-30-noisy-phase-native-scope.md` |
| Natural dynamics (boson, Fokker-Planck) | Tested readouts matched classically. | `FOKKER_PLANCK_CLASSICAL_BASELINE.md` |

## Closed: do not reopen

Unramified curve-point trace generation as a COMPLETE general local Kummer
source is refuted by the all-genus oddp family in WILD_LOCAL_SELMER_ADMISSION.md.
The specified uniform integral polynomial-divisor sampler also lacks a
polynomial clock on its O(N)-bit clustered family. These are source-specific
closures; ramified divisor/Picard/stratified approaches remain open.

The specific split-support Fourier/Hankel operation is closed as a
polynomial-degree-success route. For every irreducible target and every
2d-1<=m<=p, checking all consecutive2d-moment windows has success at most
(3/2)d^-d, even with arbitrary weights, phases, mixtures or ancillas.
The original m=2d-1 bound remains d^-d. This does not close the general
native problem or imperfect-outcome joint decoding, nor invalidate the
known exp(O(dlogd)) algorithm. See LEGENDRE_HANKEL_SUCCESS_BOUNDARY.md.

| Direction | Killed by | File |
|---|---|---|
| Universal in-span stabilizer reconditioning and cheap exact rank minimizers | REFUTED by an all-n explicit span, arbitrary positive weights/number of rays, and algebraic tagging forcing the unique minimum-rank span. Condition>=2^n/[K(n+1)]; every rank-minimal squared coefficient cost>=2^n/[4(n+1)], yet <=K+n+1 outside atoms have cost<=4(n+1). Reviewed exact proof/classical controls. No approximate-learning hardness, global extent barrier, novelty or quantumexecution; polynomial optimized extent remains open. | `STABILIZER_SPAN_RECONDITIONING.md` |
| Six-copy binary copy-linear covariant cubic-frame processors | One-output r->r^5 preserves signed stabilizers and converges to their mixed code state; two-Bell instrument gives ordinary Bell samples plus Pauli-corrected original copies for every pure complex input. Copy-linear O6 only permutations/anti-permutations. Known machinery, focused reviewed proof and finite control; no general coherent-receiver impossibility, learner, novelty/separation or quantum execution. | `CUBIC_COVARIANT_COPY_PROCESSOR.md` |
| Gaussian Fourier linearization followed by zero-frequency MQ readout | Exact verified success is alpha times original solution density conditional on preparing invertible pencils, with another alpha for a single initial herald. Separated squares are solved immediately classically. Only this circuit/readout is rejected. | `LEVI_TENSOR_AND_MQ_ADMISSION.md` |
| Direct two-copy quadratic Legendre kernel as a unitary or uniform-label herald decoder | Distinct columns have nonzero overlap, even after diagonal removal; the specified uniform-label herald has Theta(p^-2) success. Does not exclude a different measurement or efficient polar transform. | `QUADRATIC_LEGENDRE_RECOVERY.md` |
| Equal-within-list row-weighted GS/KV strict certificate for scalar half-list OPI | Every nonzero interpolant has weighted degree at least total row multiplicity once (q/2)(k-1)>=m. Covers integer Hasse weights and adaptive rows; not unequal symbols or accidental roots. | `SCALAR_OPI_SOFT_DECODING.md` |
| Future-uniform additive-FFT SC schedule at dyadic scalar-OPI rates | Zero-offset cancellation discards all but k-1 real tables; mean at most Prange and no constant-gap rescue by polynomial independent restarts. No adaptive-feedback bound. | `SCALAR_OPI_SOFT_DECODING.md` |
| Straightforward affine-flat forcing certificate matching DQI on IID scalar OPI tables | Random halfsets have O(log t) flat dimension whp, while the full-row-rank prefix certificate needs dimension Omega(t). Does not bound dependent systems, adaptive table use or unforced scores. | `SCALAR_OPI_NATIVE_PRIORITY.md` |
| All-prime copy-only terminal gap for permutable Bose StateHSP | Operation-level odd-prime ISS and binary Imran-Ivanyos erasure, complete torsion preimages and explicit stops pay the written composition. No unknown-source inverse/purification or conjugation-symmetry claim. | `PERMUTABLE_STATE_HSP.md` |
| Solvable ambient restriction beyond nilpotence for ordinary permutable-H HSP | Sylow completeness from HP subgroup order plus p-group solver; public IMS preprocessing pays all solvable inputs (nu=1) and permutation representations. No unrestricted finite opaque scope or novelty claim. | `PERMUTABLE_SYLOW_HSP.md` |
| Class/prime restrictions for ordinary permutable-H HSP in uniquely encoded NILPOTENT groups | Second-center probe reduction plus original-ambient normalizers and paid CRT Sylows; independent automated reviews accepted the written upper bound. No novelty, implementation, new separation or nonnilpotent scope. | `PERMUTABLE_NILPOTENT_HSP.md` |
| Lie-coordinate advice as a necessary premise for permutable HSP with c<p | Public power map plus published normal-HSP/normalizer and paid quantum collection removes that premise. Reviewed written polynomial upper bound with ordinary f and unique encodings, not copy-only/general-class scope or a novelty claim. | `PERMUTABLE_LAZARD_HSP.md` Sections6-7 |
| Superpolynomial sampling separation from fixed-prime regular BPQM success | General classical insertion theorem matches ensemble-average TV->0 for fixed rational mu under the same imported source theorem. Raw sockets; no claim for arbitrary ensembles, growing/succinct alphabets, all-instance sampling or polynomial/practical improvements. | `TERNARY_SEQUENTIAL_SAMPLING.md` |
| Inverse-trace native search | Classical expected-poly search for any target, odd n>=61 (10-30) | `INVERSE_TRACE_GENERAL_SEARCH.md` |
| Complete AG SEARCH with logarithmic full rational Pic/2 rank at fixedq1019 | Exact prime selector plus one-component norm gives expected-poly all-syndrome search under retained paid arithmetic. Fixed rank-bound constant; no uniform-output claim and no proof the infinite tower satisfies the rank promise. | `AG_SMALL_PARITY_SELECTOR.md` |
| Complete AG full-support syndrome, q^2>=44e ONLY | Expected-poly classical solver and exact uniform sampler for every complete AG input with odd q>=1019, e>=8, q^2>=44e. Novelty demoted (10-27). Fixed q with e->infinity is still open. | `bundles/two-component-norm-2026-10-27/`, `bundles/norm-sampling-2026-10-27/` |
| Siegel shortcuts (failed complement, supplied Hom/End) | Wrong polarization for the specific complementary map; strong lattice advice makes the kernel classical. Does NOT exclude the recovered eight-square map. | `WEAK_SIEGEL_CONVERSION_AUDIT.md`, `SIEGEL_ENDOMORPHISM_TRANSPORT_ATTACK.md` |
| Simon DCP decoder (ePrint 2026/1591) | The Lemma 3 step is unsupported, and the October revision is unchanged | `DCP_SIMON_OCTOBER_REVISION_AUDIT.md` |
| Permutation-coset sources (CFI, wreath, bank) | Luks gives poly time, and the wreath is recovered classically | `WREATH_COSET_PERMUTATION_HOLEVO_COLLAPSE.md` |

## Standing owner rules

- `GOAL.md` is binding: Codex does the deep reasoning, and Gemini does
  low-judgment work through `MECHANICAL_FOLLOW_UP_PLAN.md`. No tiny-circuit
  search or toy oracles. Running out of usage is a handoff, not completion.
- No outside contact or submission without explicit owner instruction.
  Everything in `../docs/outreach/` is unsent.
- No registry promotion: `registry/candidates.json` holds 8 unpromoted
  hypotheses, unchanged since 10-09.
- Gemini "Investigations 21-61" are unreviewed (specific records are
  quarantined in `CAMPAIGN_NEGATIVE_CLAIM_AUDIT.md`). Never cite them to
  rule a direction out.

## Where things live

- **Algebra tools:** `TOOLBOX.md`. **Review receipts:** `audits/reviews/`.
  **Classical baselines and certificates:** `classical_baselines/`.
- **Bundles:** the 10-22 to 10-27 working bundles that the handoff cites
  under `~/Developer/qsearch-research-work/<bundle>/` are copied, text only,
  to `bundles/<bundle>/`. See `bundles/README.md`.
- **Tests:**
  `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider -W error <tests>`.
  `../tests/KNOWN_FAILURES.txt` lists the 134 tests that already fail.
- **Location:** the repo is at `~/Developer/qsearch`, moved off the iCloud
  Desktop on 2026-10-31. Records citing `/Users/jaspersands/Desktop/quantum
  algorithm search/...` mean the same path under the repo root.

## Known open issues

- `../docs/papers/rees-hsp/main.tex` was corrected on 10-31 (Claude Code):
  tuple lift, right-action channel, source-faithful SDE bounds, real Lean
  modules; FPT(k), Omega(p^55) and the weak-Schur mixed-state claim
  withdrawn; every section then re-audited by automated referees and
  corrected; key citations checked against the papers. No human review. Record: `audits/reviews/2026-10-31-rees-manuscript-falsifiers.md`
  Section 5. Pre-correction copies are in `archive/`; never send them. No outreach sent.
  The 11-01 proof and priority checks list text fixes (related work at
  main.tex:116, the IS threshold remark at :420, Schedule 2 wording at
  :436-437, and the bibliography year mismatches); none applied. Their
  check scripts live outside the repo; see the mechanical queue entry of
  that date. The 11-02 extension and schedule reports add more ranked
  fixes (IMS amplification at :546, stop rules at :569, the black-box
  ker Phi and small-prime gaps, budgeting B_{kappa_d} not B_d). Since 11-02
  round 2 these are applied in main.tex (integration log I1-I65); the open
  judgement calls are K1-K15 and referee F1/M4 in that log.
  Their scripts are in the repo under audits/reviews/2026-11-02-rees-*/.
- Corpus lookup missed retained source bundles; consult explicit references
  in `SURFACE_SOURCE_RECONCILIATION.md` before declaring a source gap.
- `NEG-CHARACTER-SHIFT-UNIFORM-DECODING-LOWER-BOUND-BARRIER` (10-11) says it
  proves a uniform Omega(p) classical lower bound. Its proof
  (`CHARACTER_SHIFT_UNIFORM_DECODING_LOWER_BOUND.md`, Theorem 4) covers only
  candidate-testing algorithms and assumes Legendre PRF hardness. Treat it
  as conditional, and never cite it as hardness.
