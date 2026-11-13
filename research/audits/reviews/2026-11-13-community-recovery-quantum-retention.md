# Retaining the native community high-energy state

2026-11-13. Independent READ-ONLY audit of the existing compiler, with this
new proof note only. STATE/TRAPS, the closed source repair, ordered trace
review section 8, certificate section 8, completed old compiler sections
5–6, and the new mass lemma were read. No API/network/Git/tests.

**Conclusion.** The detector's accepted branch can be retained at the stated
cost. It produces a density state on the FULL ordered injective-tuple space,
with sufficiently small low-energy mass; it need not be an exact eigenstate
or a globally symmetric vector. Actual compiled inverses, a public overlap
floor, and a capped randomized amplification schedule pay the retention.
Repeated successful calls give IID copies of the SAME state conditional on
the frozen arrays. This note does not prove the remaining tomography or
complete quantum recovery theorem.

## 1. Source contract and matching the energy constants

Fix even p=2d>=4, k>=3, fixed rational q in (0,1/2) away from zero, growing
polylogarithmic ell=p*lambda=o(sqrt(n)), and known effective signal at a
sufficient fixed multiple of the log-free frontier. Put

    L=ceil(log_2 n), t=1/L, M=binom(n,p),
    D=binom(ell,d)binom(n-ell,d), Dbar=n^d ell^d,
    epsilon_M=(1-t)epsilon_*, b=epsilon_M/sqrt(q(1-q)),
    h=t epsilon_*/sqrt(q(1-q)), beta_*=epsilon_*/sqrt(q(1-q)).

Form the already paid TWO-way asymmetric clones once, including any known
attenuation. The actual preparation/controller uses only these fixed arrays
and public parameters. No label, gauge, refreshed graph, QRAM, supplied
projector or preparation oracle is used.

Use the rational unnormalized ordered operator A_ord, with entries Y_M-q
on legal transitions and zero on invalid tuples. Its row degree is d!*D,
so alpha=d!*D bounds its norm on EVERY array. All slot orderings are kept.
`community-native-classical-match.md` LF292–327 proves the trace bound on
this entire ordered space: starting rows (n)_ell, at most d! target lifts
per set transition, and independent-copy symmetrization. It is not merely
a norm bound on the globally symmetric slice.

For a fully computable constant choice, take the certificate's section 8
constants

    c_full=k^(1-(2p+2)d)/(2^d d!),
    c_small=binom(p,d) k^(1-2p-2d)/(p^d (2d)^(d-1)),
    c0=min(1,c_full,c_small), theta_G=c0/8, kappa=c0/32.

For sufficiently large n, that certificate has mean Rayleigh quotient
>=c0*epsilon_M*Dbar/4. The enlarged fixed SNR constant makes its ordered
noise <=c0*epsilon_M*Dbar/16. Since the mean norm is <=epsilon_M*Dbar,
the observed certificate has mass >=kappa at energies
>=theta_G*epsilon_M*Dbar. These follow by the same Rayleigh/norm argument
as the retained certificate, with no unknown quantities supplied.

The classical mass lemma's larger constant need not equal this guide
constant. Set

    c_ret=min(1/(2k^p),theta_G/2), a_ret=c_ret*epsilon_M*D,
    tau_hi=d!*a_ret, tau_lo=3*tau_hi/4, Delta=tau_hi/4.

As d!*D<=Dbar, the existing guide's high band is above tau_hi. Replace c
by c_ret in the mass lemma's explicit large-n and noise conditions: require
d!*D/V>=1/2, r/d!<=c_ret*D/8, and T<=a_ret/8, with its V,r,T definitions.
This only enlarges fixed p,k,q-dependent constants. On that single noise
event, A_ord>=-tau_hi/4. Hence every legal trace-one density sigma with
mass >=1-zeta at energy >=tau_lo, zeta<=1/4, has

    Tr(A_ord sigma)>=tau_hi*(3/4-zeta)>=tau_hi/2,
    Tr(P_L rho_1)>=mu_ret:=c_ret/(8k)>0.               (1)

The tomography/rounding parameters must use mu_ret, not silently retain
the larger classical value 1/(16k^(p+1)). The change is constant in ell,n.

## 2. A known overlap floor on one good frozen instance

Let J be the explicit product of normalized within-p-block permutation
isometries, not a global symmetrizer. Put U=Pi_cf(A^G)^tensor(lambda),
V=Pi_cf(hf)^tensor(lambda), and |g>=JU/||U||.
The retained directional covariance proof uses
s=J*P_hi JV/||P_hi JV||, with ||s||<=1; J*P_hi J need not be a projector.
It gives ||P_hi JU||^2>=kappa*||hf||^(2lambda)/8 except with probability
O_pk(lambda^2/(h^2 M)). Uniformly in labels,

    ||f||^2>=c_f M, c_f=k^(1-2p)/2,

for sufficiently large n, by the full-tensor lower bound minus repeated
indices. Markov gives ||U||^2<=L(2M)^lambda except with probability 1/L.
Thus an explicit public lower floor is

    ||P_hi g||^2>=gamma,
    gamma=(kappa/(8L))*(c_f h^2/2)^lambda.             (2)

Decrease gamma to a positive dyadic lower bound when compiling. It has
O(ell log n) bits at the retained frontier. The good-instance probability
also pays the ordered noise event. The model-TV term is paid ONCE:
O(sqrt(M t^2 beta_*^4)) plus finite-bit source error. At the log-free scale,
the covariance error is O_pk(ell^(d+1)L^2/n^d), and the TV exponent is
O_pk(ell^(2-p)/L^2). These and 1/L tend to zero. No resampling-until-good
procedure is asserted; the algorithm is capped on bad arrays as well.

For every fixed-q array, squared single-edge guide amplitudes lie between
fixed positive constants. Each vertex has sampling mass O_q(p/n), so the
collision test succeeds with probability 1-O_q(ell^2/n)>=1/2. The existing
coherent collision amplification therefore prepares |g> to any required
column error with logarithmic accuracy overhead. Its known table circuit
and actual reverse are charged; no n^ell amplitude vector is constructed.

## 3. Filtering and actual-inverse amplification

An ideal coherent filter accepts energies >=tau_hi with probability
>=1-delta and energies <=tau_lo with probability <=delta. The interval
between them is unconstrained. Repeated constant-success QPE, a coherent
majority flag, and the existing sparse-Hamiltonian simulator implement this
with O((alpha/Delta)*polylog(alpha/Delta,1/delta)) sparse-access calls.
Shift/scale the simulated spectrum inside a proper subinterval of the
phase circle to avoid wraparound. No gap around each eigenvalue is assumed.
Keep ALL QPE/majority work through amplification; it need not uncompute to
zero on the accepted branch. Tracing it afterward may produce a mixed state.

AND the final flag with an EXACT reversible validity test on the output
tuple: every index is <n and all indices are distinct. This kills any
invalid-register leakage caused by compiled-column error. It leaves the
ideal high-band mass unchanged and costs poly(ell,log n) gates. Accordingly
every actual accepted state is exactly supported where the mass lemma acts.

Here is a finite schedule requiring no actual-overlap estimate. Choose
0<eta,zeta<=1/4, nu=gamma/4, and

    B_trials=ceil(8 ln(4/eta)), mu=min(zeta,eta^2/B_trials),
    delta=nu*mu/4096, e_col=sqrt(nu*mu)/64.

Compile ONE actual unitary W consisting of guide preparation, filter and
validity flag, so its zero-input column differs by <=e_col from the ideal
filtered guide column. Split this error between guide preparation and
full-operator simulation/filter compilation. Such accuracy is paid by the
existing compiler. The actual flag-success probability s satisfies s>=nu:
its amplitude is at least sqrt((1-delta)gamma)-e_col>sqrt(nu).
Moreover the actual unnormalized accepted low-band amplitude is at most
sqrt(delta)+e_col=sqrt(nu*mu)/32. Conditional on success its squared
low-band mass is therefore <=mu/1024<=zeta/1024.                (3)
It is also <=eta^2/1024: the normalized high-band projection is a
proof-only reference state within trace distance eta/32 of the retained
state. No such projector is supplied to or implemented by the algorithm.

Use W and its ACTUAL gate-by-gate inverse with the same workspace banks.
The initial-zero and final-flag reflections are exact finite-gate circuits.
For s=sin^2(theta), j Grover iterations have success probability
sin^2((2j+1)theta). Every successful iterate has precisely the SAME normalized
accepted component Pi_flag W|0>/sqrt(s), up to a global phase. Thus errors
are certified for the actual W; no unproved global ideal-dilation hybrid
or independent approximation to W's inverse is invoked.

Let R be a power of two with 4/sqrt(nu)<=R<8/sqrt(nu). In each trial, with
probability 1/2 use j=0; otherwise choose j uniformly in {0,...,R-1}.
For s>=1/4 the first branch succeeds >=1/8. For nu<=s<1/4,

    average_j sin^2((2j+1)theta)
      =1/2-sin(4Rtheta)/(4R sin(2theta))>1/4,

since sin(2theta)>=sqrt(3nu). Hence each trial succeeds >=1/8. After at
most B_trials attempts, output the first accepted state or ABORT; on a
good frozen instance ABORT probability is <=eta/4. All fair-bit choices
are bounded and exact. If the whole spectrum is below tau_lo, the actual
initial flag mass is <=nu*mu/1024 by the same unnormalized column bound.
Using (2j+1)^2<=256/nu, total false-success probability is then
<=B_trials*mu/4<=eta/4; this does not assume the planted success floor.

## 4. Charged cost and repeated accepted copies

Guide-table compilation and each lookup cost O(M*poly(B,ell,precision));
every Hamiltonian lookup scans the frozen table, with no free QRAM.
Here alpha/Delta=4/(c_ret*epsilon_M), polynomial at the frontier. A safe
one-output/ABORT gate bound is

    M*poly(B,ell,P)*(lambda+alpha/Delta)*R*B_trials,
    P=O(B+ell log n+log(1/eta)+log(1/zeta)),             (4)

absorbing the filter and collision-amplification logarithms in the polynomial.
All inverses and reflections are included. Since
gamma^(-1/2)=O_pk(sqrt(L))*h^(-lambda)*exp(O_pk(ell)), this is

    n^(ell/4)*exp(O_pk(ell*(log ell+log log n)))
      *poly(n^p,B,log(1/eta),log(1/zeta)).              (5)

The output is the retained ordered tuple, with filter work discarded only
after success. It has O(ell log n) index qubits. Neither global symmetry,
an exact spectral projector, nor an individual eigenstate is promised.

For T_copies=O(n^6 log n), use the SAME compiled W and frozen arrays in
every call, with fresh initialized qubits and independent internal coins.
Conditional on those arrays, every successful branch outputs exactly the
same density sigma (the work-trace of Pi_flag W|0>/sqrt(s)). Consequently
successful outputs are IID sigma copies, including after conditioning on
all calls succeeding. Set eta=n^(-4)/T_copies; a union bound pays all
computational ABORTs by O(n^-4), and log T_copies only adds O(log n) bits.
The good-source event and source-TV budget are not multiplied by T_copies.

Original-Y validation is joined later by its uniform all-labelings event
and a union bound, not by comparing a joint law of original Y with ideal
independent clones. This note closes retention and its source interface;
the full recovery theorem still requires the separate tomography join.
