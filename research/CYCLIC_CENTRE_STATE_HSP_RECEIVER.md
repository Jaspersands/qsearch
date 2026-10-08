# A Costed Receiver For Odd-Prime Cyclic-Centre StateHSP

CONSTRUCTIVE LOCAL DERIVATION / REVIEW PENDING. This is a restricted
StateHSP algorithm specification with finite instrument controls, not a
Shor-level algorithm, novelty claim, general central-extension solver,
DHSP solver or new classical-hardness separation. Independent human review
and a broader priority search remain required.

## A Different Constructive Target

[Holt--Subramanian v1](https://arxiv.org/html/2609.38085v1) supplies projective
abelian symmetry learning in Section9, and leaves general central-extension
Bose learning as Conjecture9.28. Problem6.41 uses copies, a controlled linear
representation and an absolute-overlap gap outside the Bose subgroup.
Sections9.1/9.3.2 and the relevant definitions were inspected. The following
restricted reduction and robust overgroup argument are LOCAL, not asserted
paper theorems. Ordinary nil-2 HSP already has an efficient quantum algorithm
[Ivanyos--Sanselme--Santha](https://arxiv.org/abs/0707.1260); this is not a
new classical HSP speedup. Its relevance is an actual measurement/reduction
recipe for supplied arbitrary mixed quantum states.

Let p be an ODD prime, Q=F_p^d and B a PUBLIC bilinear form Q x Q -> F_p.
The supplied group is

    (x,z)*(y,w)=(x+y,z+w+B(x,y)).

The designated central subgroup Z={(0,z)} has order p; the complete centre
may be larger. Every group element has order dividing p. We have IID copies
of ONE unknown rho, and an efficiently controlled known linear action R.
Promise: Tr(R(g)rho)=1 on S, and |Tr(R(g)rho)|<=1-epsilon outside S, with
epsilon>0. Known group arithmetic, p-QFTs, epsilon and B are supplied.
There is no state-preparation inverse, cloning, chosen central character,
reusable unknown-state oracle or full nonabelian QFT assumption.

The resource bound is polynomial in d, p, 1/epsilon and failure bits kappa.
It is polylogarithmic in |G| at FIXED p (or appropriately polynomially
bounded p), NOT at an arbitrary binary-encoded growing prime p. Even p,
general cocycles, large vector centres and higher nilpotency are not covered.

## 1. Measure The Centre And Pay For The Copies

One controlled R(0,z) Fourier measurement on each fresh rho measures a
central character lambda in F_p. Conditional state rho_lambda is in its
eigenspace, where R(0,z)=omega^(lambda*z). Each bucket consists of IID
copies of its conditional state. Selection/stopping reads ONLY these labels,
not an unknown density table or internal measurement outputs.

If Z is not contained in S, then (0,1) is outside S. Writing w_lambda for
the central weights, the original gap implies

    epsilon <= 1-Re sum_lambda w_lambda*omega^lambda
            <= 2*sum_(lambda!=0) w_lambda.

Hence at least one nonzero bucket has weight >=epsilon/(2*(p-1)). This is
not a promise that every bucket is heavy. Gather all buckets under a fixed
input cap; use the FIRST nonzero bucket to reach the required count. If none
reaches the count, take the centre-trivial branch. The error of doing that
when Z is not fixed is bounded below. If Z is fixed, nonzero labels NEVER
appear and the branch is correct.

This SAME-STATE source is not automatically provided by native DCP packets
with varying public phase labels. Do not transfer the recipe to those states
without a new source conversion and its costs.

## 2. Exact Known Linearisation, Without A Conditional Gap Promise

On a nonzero sector lambda define U_lambda(x)=R(x,0) restricted to it.
Its cocycle is omega^(lambda*B(x,y)). The tensor action

    A_lambda(x)=U_lambda(x)^tensor(p)

is a genuine linear representation of Q on that prepared sector tensor
space: its cocycle is raised to p. It is controlled using p KNOWN R calls
and p supplied copies. On the WHOLE unconditioned tensor Hilbert space that
formula need not be a representation; sector preparation is essential.

If x belongs to pi(S), some (x,z) fixes rho. Consequently
U_lambda(x)rho_lambda=omega^(-lambda*z)rho_lambda and A_lambda(x) fixes the
tensor state EXACTLY. Ordinary abelian Fourier sampling therefore returns
characters annihilating pi(S). No phaseless subgroup is substituted for S.

Write phi_lambda(x)=Tr(U_lambda(x)rho_lambda). The full Fourier probability
law is the Fourier transform of phi_lambda(x)^p. For ANY x with
|phi_lambda(x)|<=1-delta,

    Pr[sampled character(x)!=1] >=delta/2.

Indeed Re(phi_lambda(x)^p)<=1-delta, whereas a character has real part>=-1.
After m independent experiments, the intersection T of the character
kernels contains pi(S) with certainty, and with failure <=|Q|exp(-m*delta/2)
EVERY x in T has |phi_lambda(x)|>1-delta. This is a simultaneous pointwise
guarantee, NOT exact conditional symmetry learning or a minimum conditional
gap premise. The classical operation is finite-field nullspace, not scanning Q.

## 3. Approximate Eigenvectors Force An EXACT Abelian Overgroup

Take delta=1/(16*p^2). For x,y in T, purify rho_lambda as |v>. Choose
unit phases a,b maximizing the respective expectation real parts. Then

    ||(U_lambda(x)-a)|v>|| <sqrt(2*delta),
    ||(U_lambda(y)-b)|v>|| <sqrt(2*delta).

Twice the triangle inequality gives

    ||(U_lambda(x)U_lambda(y)-U_lambda(y)U_lambda(x))|v>||
        <4*sqrt(2*delta).

The two products differ by the CENTRAL scalar
omega^(lambda*(B(x,y)-B(y,x))). Thus a nonzero commutator would have modulus
at least 2*sin(pi/p)>=4/p. But its squared upper bound is
32*delta=2/p^2, strictly smaller than16/p^2. Since lambda!=0 is faithful on
C_p, B(x,y)-B(y,x)=0 for every pair in T. The actual group

    L=pi^(-1)(T)

is therefore ABELIAN and contains S. This is not an approximate matrix
commuting-repair oracle. The conclusion concerns a finite group's exact
bilinear commutator and is checked from the recovered basis before use.
If that check fails, return FAILURE, not a repaired subgroup or speedup.

Let V contain a basis of T. The explicit homomorphism

    (t,c) -> (V*t, c+(1/2)*B(V*t,V*t))

identifies F_p^(dim(T)+1) with L. Its proof uses symmetry of B on T and
inverse2 modulo p. It compiles controlled R using PUBLIC field arithmetic.
No hidden secret, normal-core oracle or learned density matrix is needed.

## 4. Recover The Actual Bose Phases On Fresh Original Copies

Apply ordinary abelian Fourier sampling with this chart to FRESH ORIGINAL
rho copies. The original epsilon gap survives restriction to L. Character
kernel intersection recovers the true S, including its central/eigenvalue
phases. Stopping at T would return only an overgroup and lose that data.

If no nonzero bucket reached its quota, instead use Q with section x->(x,0).
On the successful centre-trivial branch, rho is supported on the Z-fixed
subspace. That subspace is R-invariant, so the section is an actual linear
representation THERE. Fourier sampling is legal on the supplied rho, even
though the section need not be a homomorphism on the entire workspace.
Recover pi(S), then lift it together with all of Z. An input-cap exhaustion
in the nontrivial-centre case is a declared failure event, not free retries.

## Explicit Caps And Failure Ledger

Let h=ceil(log2(p)), kappa>=1. A conservative completely integer ledger is

    delta=1/(16*p^2),
    u=ceil(log2(p-1)),
    m=32*p^2*(d*h+kappa+2+u),
    C=p*m                        conditional copies needed in one bucket,
    w_min=epsilon/(2*(p-1)),
    N=ceil((2*C+8*(kappa+2))/w_min),
    M=ceil(2*((d+1)*h+kappa+2)/epsilon).

Under the nontrivial-centre promise, one bucket's count is Bin(N,w) with
N*w>=2*C+8*(kappa+2). Chernoff at half its mean gives quota-failure at most
exp(-N*w/8)<=2^(-kappa-2). There are at most p-1 possible selected sectors.
For EACH selected sector, the pointwise overgroup failure is at most
|Q|2^(-m*delta/2)<=2^(-kappa-2-u). Because selection uses centre labels ONLY,
conditional Fourier samples have the same law. The extra u bits permit a
conservative union over all p-1 possible DATA-SELECTED sectors, rather than
assuming that selection and the mathematical success event are independent.
Final original-copy sampling has error<=2^(-kappa-2). Total<=3*2^(-kappa-2).
All these bounds include the centre-trivial branch and failure-flag events.

Worst-case original copies <=N+M. Central measurements consume N controlled
R calls; tensor experiments consume C more; final readout consumes M.
At most N+C+M controlled R calls. Bucket storage <=(p-1)*C with surplus
discarded; QFT/field arithmetic is polynomial in the charged parameters.
Source accuracy and gate precision are separate: ideal controls do not
certify a noisy implementation. A whole-channel trace-distance bound eta
would add eta to failure; marginal error bounds are insufficient for
correlated sources. Finite simulation enumerates probabilities only for
calibration; the specified quantum protocol does NOT know those tables.

## Falsification And Scope

The controls include all three hidden central lifts for a nonnormal
Heisenberg reflection-like line, BOTH nonzero sectors, pure cross-sector
coherence and mixed sources, and the centre-trivial branch. Another mixed
source has original gap>=2/3 but a selected sector's exact conditional gap
as small as2^-40. Approximate T can retain a direction that is NOT an exact
sector symmetry. It is nevertheless commuting and final original-state
sampling recovers the correct subgroup. This tries to break the main bridge
instead of relying on exact stabilizer test fixtures.

Four further full instruments use genuinely NON-stabilizer real-amplitude
qutrit factors inside two-qudit sector states. All81 characters are replayed
on the actual three-copy/six-qutrit controlled action. The independent checker
reconstructs exact cyclotomic pure-state Kraus vectors, rather than assuming
that a density matrix diagonalizes in the measured basis. Additional tests
execute non-diagonal arbitrary mixed qutrit controls. These are finite
instrument checks, not an asymptotic resource fit or a native factory.

Small regular/coset and direct-sum states are CONTROLS for established group
families, not proposed new oracle problems. Exact group/character checks and
literal small Kraus replay are distinct from asymptotic efficiency. No
classical-state simulation barrier, graph/code reduction or experimental
quantum advantage is inferred.

Likely limits: p-copy linearisation and same-sector acquisition cost grows
polynomially in p, hence exponentially in log(p); large vector centres can
make sector collisions rare; faithful-character commutator detection fails
for noncyclic centres; characteristic2 breaks both the order-p calculation
and half-quadratic chart; genuine DHSP is not a class-two bilinear extension
of this kind. Approximate gaps are handled, but approximation of supplied
copies/actions still needs a separate error theorem. Literature novelty is
unverified, and this restricted family may already follow from other work.

NEXT: review this derivation independently, especially selection-conditioned
sampling and the pointwise approximate-eigenvector argument. Then seek a
multi-centre construction that avoids exponentially rare identical-sector
copies, or a real state-generation reduction into this family. Do NOT claim
that simply extending the calibration dimensions supplies either bridge.

Gemini/Antigravity owns CLI/registry/UI wiring, full production validation
and Git. The hypothesis contract keeps speedup/novelty/candidate claims false.
