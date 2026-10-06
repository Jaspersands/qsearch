# Structured EDCP: The Actual Small-Secret Target Needs Only One Block

Date: 2026-09-28. LOCAL DERIVATION / REVIEW PENDING.

NATIVE-RING FOLLOW-UP (2026-09-29):
`NATIVE_RLWE_PHASE_DECODER_TARGET.md` removes the scalar Q construction from
a distinct forward source, proves one-block sufficiency via multiplication
rank, and sharpens BOTH prior tails. Its finite q-near-d^4 references and
original-data classical benchmarks are the next priority. The scalar-Q
calculations below remain scoped to their original source.

COMPUTATIONAL-PRIORITY CORRECTION (2026-09-29):
`NATIVE_RLWE_COVARIANT_DECODER_TARGET.md` keeps prior-aware one-block
decoding but also restores a native two-independent-block covariant target
at wider widths. Information sufficiency does not imply that the one-block
prior-aware inverse is easier to implement. The scalar calculation below
does not settle that computational choice.

This changes the research priority, not the status of an algorithm. The
hardness-linked source has a small error-distributed SECRET. Existing
three/four-block certificates solve the stronger uniform-Z_Q discrimination
problem. A single block is already information-sufficient for the actual
prior at the comparison parameters below, even using LOCAL Fourier readout
and exhaustive classical decoding. Efficient decoding remains unresolved.

Do not promote this information calculation into a quantum advantage.
Do not discard the old uniform-secret results: their stated scope is valid,
but their sufficient block counts are not requirements of the reduction.
The main research target should now include prior-aware one-block inversion,
with matched classical attacks on both the readout AND original RLWE data.

## 1. The Prior And The Label Must Stay Together

Use rank n=1, d>=2 a power of two, q>=3 odd, Q=q^d+1 and
E(v)=sum_i q^i*v_i mod Q. The normal-form reduction's scalar secret is
s=E(v), where v is the centered q-ary error polynomial. In the spherical
lane its unwrapped coefficients have probability width

    rho=sqrt((d^(3/4)*log(d))^2+log(d)^2).

The elliptical lane has a correlated prior with a certified second moment,
not independent coefficients. These are the contracts in
`STRUCTURED_EDCP_SOURCE_HARDNESS_AUDIT.md`. The small-secret normal-form
principle is established in Lemma 2.24 of the
[Ring-LWE toolkit](https://sites.cc.gatech.edu/fac/cpeikert/pubs/toolkit.pdf);
the local audit supplies the required coordinate and rounding ledger.

The phase label a is uniform in Z_Q and independent of the ideal secret.
No unit or odd-label conditioning is needed for the information proof below.
If a is a unit and is normalized to one, the new secret is s'=a*s, with

    pi_a(s')=pi(a^(-1)*s'),

NOT the original small coefficient-Gaussian prior. Its known support has
been multiplied by a. Setting a=1 while keeping pi unchanged would solve
a different and usually much less informative problem.

## 2. A Small Secret Difference Cannot Hide In A Small Quotient

Let the actual prior put mass at least 1-delta_s on

    S={v in Z^d: |v_i|<=R_s}, H=|S|=(2*R_s+1)^d,
    2*R_s<=q-1.

Balanced evaluation is injective on S. For distinct v,w in S put
Delta=v-w, g=gcd(Q,E(Delta)), and t=Q/g>1. The evaluation ideal
I_g={f in R:E(f)=0 mod g} has index g. Since Delta belongs to it,
Delta*R is contained in I_g. Irreducibility of X^d+1 makes multiplication
by nonzero Delta nonsingular, so

    g divides |Norm(Delta)|,
    1<=g<=||Delta||_2^d<=(2*R_s*sqrt(d))^d=:G_s.                       (1)

The norm inequality follows from coefficient Parseval and AM-GM over the
d field embeddings. Equivalently G_s=(4*R_s^2*d)^(d/2), an exact integer.
No factorization of Q is needed. This is the same ideal-norm mechanism as
the earlier collision proof, now applied to SECRET differences.

Power-of-two d matters: at d=3,q=17, Delta=(1,-1,1) has evaluation gcd
273, while ||Delta||_2^d=3^(3/2)<6. Its norm is zero in the reducible
quotient. Do not generalize (1) to arbitrary polynomial rings.

## 3. One-Block Classical Information Certificate

Use the exact periodized Gaussian phase source of
`STRUCTURED_EDCP_LOCAL_READOUT_BASELINE.md`, with amplitude width sigma.
Local Fourier data are

    Y_i=a*q^i*E(v)+noise_i mod Q, i=0,...,d-1,

with independent known noise law nu. For two secrets, positivity of the
Fourier Gaussian makes the Bhattacharyya overlap of these classical laws
equal to the corresponding pure-state inner product. Averaging a gives

    E_a BC(P_v^a,P_w^a)=b_t,
    b_t=Pr[E(C)=0 mod t], C_i iid with the periodized amplitude-squared law.

Let s_G=sigma/sqrt(2), beta=(sqrt(d)/s_G)^d and alpha=1+2^(-2d).
The ideal-dual maximum-mass bound, followed by the charged periodization
comparison, gives

    b_t<=alpha*max(1/t,beta)+d*epsilon_wrap
       <=alpha*max(G_s/Q,beta)+d*epsilon_wrap=:B_pair.                 (2)

Cap B_pair at one if needed. One usable wrapping charge is

    B=floor((Q-1)/2)>0,
    T=sigma^2/(pi*B)*exp(-pi*B^2/sigma^2),
    epsilon_wrap=min(1,2*T+T^2).

This compares the periodized coefficient probability to unwrapped
D_(Z,s_G) modulo Q, BEFORE summing over competitors.

Consider classical maximum likelihood restricted to S. For any true v in
S, the event that a competitor w has at least its likelihood has probability
at most BC(P_v^a,P_w^a). A union bound, then average over a, yields

    E_a Pr[ML_S fails | v] <= min(1,(H-1)*B_pair).

Therefore for ANY independent secret prior obeying the box mass premise,

    Pr[ML_S fails] <= min(1,delta_s+(H-1)*B_pair).                       (3)

The Gaussian prior is not replaced by a uniform-box prior: the fixed-secret
bound is simply averaged against the actual prior. Prior-aware MAP is at
least as good as this ML decoder. The decoder still enumerates H secrets;
(3) is not an efficient classical algorithm. The local measurement is
classically sampleable under the retained-source contract, not under every
standalone phase-state access model.

Physical source, truncation, implementation and rounding losses are added
once using their existing joint ledgers. No rare-event conditioning or
independence of the upstream amplified errors is assumed.

### Two Actual Prior Bounds

For iid coefficient width rho>=1, the unwrapped tail outside S is at most

    delta_s<=d*rho/(pi*R_s)*exp(-pi*R_s^2/rho^2).                       (4)

Use theta(rho)>=rho in the Gaussian tail normalization. A certified upper
rho_bar may replace rho on the right, which is increasing in rho.
Centering modulo q only improves the event being bounded.

For an arbitrary correlated centered prior with E||v||^2<=S2,

    delta_s<=S2/R_s^2.                                                 (5)

This weaker Markov bound suffices for the elliptical lane without revealing
its latent shape or falsely assuming coefficient independence.

## 4. Finite References And A Much Narrower Source Frontier

Take q=nextprime(d^12), and sigma=10^7,10^12,10^17 at d=64,256,1024.
For the spherical prior use rho_bar=100,400,1300 and R_s=rho_bar*sqrt(d).
For the elliptical prior use S2 upper references 100000,5000000,194000000
and R_s=ceil(sqrt(1000*S2)), giving delta_s<=0.001.

| Lane | d | R_s | log10 H | log10 main ML-error upper reference | prior-tail upper reference |
|---|---:|---:|---:|---:|---:|
| spherical | 64 | 800 | 205.0810 | -175.4882 | 1.21858e-87 |
| spherical | 256 | 6400 | 1051.4544 | -1673.7590 | 2.67070e-349 |
| spherical | 1024 | 41600 | 5038.2116 | -10674.3874 | 7.70219e-1397 |
| elliptical | 64 | 10000 | 275.2673 | -105.3019 | 0.001 |
| elliptical | 256 | 70711 | 1318.5331 | -1406.6803 | 0.001 |
| elliptical | 1024 | 440455 | 6087.6104 | -9624.9886 | 0.001 |

The main term is (H-1)*alpha*max(G_s/Q,beta). In EVERY row the total
competitor-weighted wrapping term H*d*epsilon_wrap is additionally charged
by a positive 1e-12000, after checking its analytic logarithmic upper bound.
The prior tail and physical source losses, not these tiny main terms,
control the total success guarantee. These 110-digit references are not
outward interval certificates; the source's primality/reduction qualifications
remain unchanged.

Much of the older phase width is unnecessary for this information goal.
The following exact power-of-two widths satisfy

    (H-1)*alpha*max(G_s/Q,(sqrt(2*d)/sigma)^d)<=10^(-8).                (6)

Both branches of (6) were checked by EXACT integer cross multiplication,
using alpha=(2^(2*d)+1)/2^(2*d). The bounds still add the prior tail,
positive wrapping charge, and physical-source ledger.

| Lane | d | narrower sigma | single-block phase-error reference |
|---|---:|---:|---:|
| spherical | 64 | 32768 | 8.63167e-7 |
| spherical | 256 | 524288 | 1.51890e-10 |
| spherical | 1024 | 4194304 | 1.02527e-14 |
| elliptical | 64 | 524288 | 1.45273e-5 |
| elliptical | 256 | 4194304 | 1.19930e-9 |
| elliptical | 1024 | 67108864 | 1.42640e-13 |

The last column recomputes the established forward phase bound with K=4,
M=ceil(d*log q), m=ceil(log d) and
r_mix=2*d*(floor(q^((d+2)/(d*m)))+1). The root floor was evaluated by
integer nth-root arithmetic. Spherical moments use the actual rho;
elliptical moments conservatively use the displayed energy upper bounds.
This column is ONLY phase error, not the full preparation/decision error.
No live source parameters were changed by this theory pass.

Asymptotically, for R_s=d^(c+o(1)), sigma=d^(b+o(1)), q=d^(a+o(1)), the
two sufficient main terms vanish if

    b>c+1/2, a>2*c+1/2.                                                (7)

The spherical box has c=5/4+o(1). Thus this sufficient one-block criterion
is already met for b>7/4 and a>3, far below the
full-uniform-secret width requirement. Logarithmic factors and finite
constants still matter. The narrower source also permits a larger L in
the phase budget sigma*sqrt(L)<=constant, but L*delta_hash, joint preparation
errors, computation and memory must still be charged. This does not supply
unlimited samples or turn an exponential DHSP sieve into a polynomial one.

## 5. The Right Quantum Target, Without A Free Inverse Transform

Define the Gaussian Fourier code by its normalized columns

    Psi_a|v>=|psi_(a*E(v))>, v in S.

The new task is a prior-aware measurement of this ONE block, compared with
classical decoding of its d Fourier coordinates. It need not implement the
full-Z_Q frequency-fiber isometry studied in the earlier multi-block work.

There is a stronger information check if desired. Put D=(4*R_s+1)^d-1.
The sum over all nonzero secret differences bounds every off-diagonal Gram
row. Therefore

    Pr_a[||Psi_a^dagger*Psi_a-I||_op>tau]<=min(1,D*B_pair/tau).         (8)

Use nonnegative Gaussian overlaps or their absolute values, count possible
differences rather than pretending rows are independent, and apply Markov
after the row domination. This describes a near-isometric code on most
labels. It does NOT compile its inverse.

For example, when a prior state sqrt(pi) is coherently available, let

    R|v>=|v>|psi_(a*E(v))>, L|c>=|sqrt(pi)>|c>.

These give a unit-normalization projected encoding

    A=L^dagger*R=Psi_a*diag(sqrt(pi)),
    A*A^dagger=rho_a=sum_v pi(v)|psi_v><psi_v|.

Let an odd bounded degree-m singular-vector polynomial be p. On the true
prior ensemble, its transferred-block success is exactly

    S_m(a)=Tr[rho_a*p(sqrt(rho_a))^2]
          <=min(1,(pi^2/4)*m^2*Tr(rho_a^2)).                            (9)

The Bernstein inequality argument is the same as the existing polar audit.
Since 0<=overlap<=1 and its average is bounded by B_pair,

    E_a Tr(rho_a^2)<=C_pi+(1-C_pi)*B_pair,
    C_pi=sum_v pi(v)^2.                                                (10)

For the spherical Gaussian conditioned on S,

    C_pi=[Z_(R_s)(rho/sqrt(2))/Z_(R_s)(rho)^2]^d
        approximately (sqrt(2)*rho)^(-d).

Explicitly, if t_s<1 bounds one coefficient's prior tail and
e_rho=2*exp(-pi*rho^2/2)/(1-exp(-3*pi*rho^2/2)), use

    C_pi<=[(1+e_rho)/(sqrt(2)*rho*(1-t_s)^2)]^d.

Conservative theta/tail bounds give necessary log10 polynomial degrees for
mean flag success >=0.9 of 67.7666,345.4659,1663.3059 at the three original
wide comparison points. These are for a uniformly capped-degree transform
of THIS encoding. They are not lower bounds on arbitrary structured
prior-aware quantum measurements. Flag success alone is not correct decoding.

A necessary scope countercontrol is the ordinary H-dimensional Fourier
matrix Psi=F_H. It has a fast inverse, although the same projected-access
construction yields A=F_H/sqrt(H), whose degree-one transfer succeeds with
probability 1/H. A structured transform can therefore escape this wrapper;
the required new work is its construction for the actual Gaussian code.

The prior is therefore a better target, but another generic PGM/polar wrapper
is not the missing algorithm. Nonuniform-prior PGM is not automatically
optimal either. A hidden correlated prior does not automatically supply
coherent preparation of its marginal square-root amplitudes.

Finite truncation/preparation must not be charged only per column when
claiming (8) as an operator approximation over all H columns: Frobenius
conversion alone costs sqrt(H) times a uniform column-vector error.
Similarly, additive ensemble error can dominate the exponentially small
purity scale in (9)-(10). Keep these ideal-encoding scope qualifications.

## 6. Identity-Label Countercontrol

For the original small prior and the label ACTUALLY equal to one, the
unwrapped or centrally truncated phase states satisfy

    E_v D(psi_(E(v)),psi_0)
       <=sqrt(pi)*sigma/(q-1)*sqrt(E||v||^2).

Use the exact negacyclic evaluation energy bound from the phase-moment
audit and the coefficient Gaussian variance sigma^2/(4*pi). In the
spherical lane this becomes

    epsilon_identity<=sigma*rho*sqrt(d/2)/(q-1).                       (11)

At the original comparison widths, references are
1.12837e-12,5.06844e-14,2.13596e-15. With ONLY this phase-state ensemble
and its stated prior, optimal recovery is at most max_v pi(v) plus (11).
This is consistent with high average information for UNIFORM random a.

If original classical source records are retained, that last classification
bound does not apply to all their information. Instead the program can be
replaced by a fixed state within the same distance while retaining those
records; any further algorithm on them still needs its own analysis.

Explicit finite prior-pushforward controls confirm the normalization issue.
For q=5,d=2, coefficient box [-1,1]^2 and probability width 1.2, multiplying
the secret by the unit 3 changes its distribution by TV about 0.3343803.
Special rotations, such as multiplication by q, can preserve an isotropic
coefficient prior; arbitrary unit normalization cannot assume that symmetry.

## 7. Checks And Revised Handoff

Executed targeted mathematical controls, not a bulk repository suite:

- 2,992 exact norm/divisibility checks at d=2,4,8 and q=3,5,7,17, plus
  the reducible d=3 countercontrol. Exhaustive coefficients in [-2,2] for
  d=2,4; 100 sampled d=8 vectors with NumPy seed 290926.
- Seven full small-prior discrimination cases at d=2, R_s=1: q=3,5,7
  with sigma=1.4,2.2, and q=17 with sigma=12. All labels and Fourier
  outcomes were summed. Gaussian-prior width is 1.2. The local
  Bhattacharyya/characteristic and label-average/divisor identities agree
  within 6.67e-16 and 5.56e-16 respectively.
- At q=17,sigma=12, uniform-box ML success is 0.977669, Gaussian-prior
  MAP success 0.992303, and prior PGM success 0.994373. These dense small
  references are NOT scalable algorithms or evidence of a major speedup.
  At q=3,sigma=1.4, prior PGM is 0.639712 while classical prior MAP is
  0.669237, explicitly refuting an assumption of PGM optimality.
- 386 Gram row checks and 1,544 source-weighted polar-polynomial controls
  at degrees 1,3,5,9 checked (8)-(10), including singular small Gram
  matrices. Tiny roundoff-negative eigenvalues were clipped only after
  checking they were greater than -1e-12; these are numerical references.
- Six growing box-information references, six EXACT integer width checks,
  three generic prior-polar degree references, three identity-label bounds,
  and 36 finite unit-prior pushforward controls. Gaussian sums in small
  controls use period images -4..4, not certified infinite-sum intervals.
- Four full-Fourier inverse controls at H=4,8,16,32 distinguish a genuinely
  available structured inverse from its poorly normalized projected access.

Gemini implementation priorities:

1. Add a separate small-secret information certificate with explicit prior,
   R_s,delta_s,H,G_s,B_pair, periodization, and physical-source losses. Keep
   it distinct from uniform-secret block counts and from efficient decoding.
2. Preserve a and the original Gaussian prior in one-block benchmarks. Any
   unit normalization MUST push the prior forward. Include the identity-
   label and reducible-ring countercontrols as rejection tests.
3. Benchmark prior-aware weighted CVP/Babai, list decoding and available
   stronger reduction at L=1, using the existing 2d-dimensional graph
   lattice. Include both wide and narrower certified source settings.
   Generate noise scalably, not with a Q-entry table; separate objective
   mismatch, optimization failure, resource limits and information failure.
   Planted secrets are scoring-only; keep the reduction's held-out sample
   out of preparation, decoder tuning and parameter selection.
4. Also benchmark the original retained RLWE instance. The transformed
   readout is not the strongest classical access model available here.
5. Keep the quantum target as an explicitly compiled prior-aware inverse
   Fourier-code measurement. Record absolute encoding scale, actual input
   prior, source-weighted success and classical comparator. Near-orthogonal
   columns or a PGM formula do not discharge that implementation obligation.

Multi-block coherent conditioning remains a possible route, especially for
other priors. It should no longer be treated as a necessary first target
for this hardness-linked source. No candidate, proof or speedup promotion;
no routine wiring, full-suite run, source change or commit in this pass.
