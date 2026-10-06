# Fixed-Direction Carry Throughput: A Scoped Obstruction

Status: LOCAL DERIVATION / REVIEW PENDING. No independently reviewed theorem,
novelty claim, general quantum lower bound or security conclusion.

## Research Decision

Do NOT pursue constant-fraction, fixed-direction product extraction that
succeeds on every complement-Z outcome of one native parity packet. For
q>=8 and m=3n, the derivation below bounds its output count by 31 except on
an explicitly bounded source event whose probability vanishes exponentially.
This applies even to an unlimited classical search for the best fixed basis.

The q=4 common-isotropic primitive remains correct. It cannot be extrapolated
to growing phase levels. A legal q=8 postselection primitive is also supplied,
but its acceptance rate, source conditioning and repeated consumption must be
charged. Outcome-adaptive direction changes, different preprocessing,
multi-packet interference and decoding correlated states remain open.

The follow-up [native source law](DCP_CARRY_SOURCE_LAW.md) now separates
fixed-label quantum acceptance from native higher-label acceptance, derives
the exact q=8 output entropy/IID condition, and bounds polynomial menus of
low-label-defined overlapping extractors at growing moduli. It does not
close arbitrary higher-label subspace synthesis or adaptive quantum decoding.

This revises, rather than strengthens by assertion, the target in
[the carry-packet interface](DCP_CARRY_PACKET_READOUT.md).

## 1. Exact Operation Class

Let A be the public n-by-m matrix over Z_q, q=2^t>=8, B=A mod2,
C=rowspace(B) and D=ker(B)=C^perp. After the public parity-chart measurement,
the physical assignments lie in x0+D. Pick independent physical directions
u_1,...,u_d in D, using any public label data and the initial syndrome.

Extend these directions to a basis of D and measure the complementary
coordinates in Z. Keep every complement outcome. The SAME directions must
give exact product phase states for every outcome and every secret. No
outcome-dependent change of retained subspace, approximate-error allowance,
secret-dependent correction or other quantum measurement is included.

Because all assignment amplitudes have equal magnitude, every complement
outcome has its uniform probability. Requiring product states on every
background means mixed phase derivatives vanish on every x in x0+D.
Known, secret-independent local phases do not remove this requirement for
every possible secret; compare each basis secret to secret zero.

## 2. One More Derivative Forces The Conductor

For two retained directions u,v, the mixed XOR derivative of Ax is

    A(x+u+v)-A(x+u)-A(x+v)+Ax
        = -2 sum_i (-1)^x_i A_i u_i v_i.

Here + on physical assignments means XOR, while the outside expression is
integer subtraction of public vector labels. Exact product phases require

    sum_i (-1)^x_i A_i u_i v_i = 0 mod(q/2)             (1)

for every x in the affine parity fiber. Replace x by x+w, w in D,
and subtract the two equations. Since q/2 is divisible by four, reduction
modulo four gives

    sum_i B_i u_i v_i w_i = 0 mod2, for every w in D.  (2)

The signs disappear modulo two. With z=u*v, (2) is precisely

    diag(z)D subset D,
    z*C subset C,
    z in Cond(C,C).                                   (3)

The equivalence uses the symmetry of a diagonal matrix under the usual
binary pairing. It is independent of the syndrome and of the chosen chart.
This is a NECESSARY condition, not sufficient at the higher modulus.

The conductor/stabilizer algebra is established coding-theory structure;
see [Randriambololona, Sections 2.11 and 2.42](https://arxiv.org/html/1312.0022v3).
For completeness, a systematic generator [I|R] makes its computation
elementary. Preservation under diag(z) requires z_p=z_f whenever R_pf=1.
Thus masks in the conductor are constant on every component of the
fundamental bipartite graph; isolated/zero coordinates are kept too.

If that graph has one component, Cond(C,C)=span(1). For independent binary
u,v, u*v cannot equal 1: that would force u=v=1. Therefore

    u_i*u_j=0 for every distinct retained basis pair. (4)

The physical supports must be disjoint. This conclusion is about a basis
of retained output factors, not every pair of codewords in their span.

## 3. Native-Source Throughput Certificate

Use unconditional IID uniform A over Z_q^(n by 3n); B is a fair binary
matrix. All label-dependent choices of the fixed basis are included.

The earlier packet audit gives a conservative failure bound for the
connected-conductor event:

    P_conn_fail <= min(1, (3n+2)2^-n + U_n),
    U_n=sum_(a=1..n,b=0..n,(a,b)!=(n,n))
          binom(n-1,a-1)binom(n,b)2^[-a(n-b)-(n-a)b].

This uses a full-rank 2n-column prefix, an independent n-column graph tail,
and the zero-column union bound. The extra even-row event in the inherited
bound is unnecessary here but conservative. No independence of exceptional
events is assumed. U_n=O(n*2^-n), as derived in the earlier audit.

Every fixed nonzero v in F_2^m obeys Pr[Bv=0]=2^-n. Thus, for w=floor(m/32),

    Pr[minweight(D)<=w] <= 2^-n sum_(j=1..w) binom(m,j). (5)

Outside these two exceptional events, every nonzero direction has weight
at least w+1 and the basis supports are disjoint. Consequently

    d <= floor(m/(w+1)) <= 31.                         (6)

The report retains the EXACT sum of the two probability bounds, clipped
at one, using dyadic integer encoding. Early vacuous rows remain visible.
Asymptotically the distance term is exponentially small: the binary entropy
bound and H_2(1/32)<1/4 give at most 2^(-n/4) for m=3n. This loose estimate
is sufficient; no finite sweep substitutes for the source proof.

In particular d/m tends to zero. For this class, keeping every outcome does
not remove the n-sized loss per level. This is NOT a lower bound for general
quantum algorithms, larger batching schedules, approximate extraction,
nonlinear retained coordinates or adaptive outcome-dependent measurement.

## 4. The Postselection Escape Is A Linear System At q=8

For q=8, a fixed subspace can yield product outputs on SOME complement
outcomes. The ledger computes their exact probability conditional on A and
the initial syndrome, without drawing only accepted outcomes.

First, each pair u_i,u_j must satisfy sum B_l u_i u_j=0 for every l.
Otherwise its mixed phase derivative is odd and cannot vanish mod4.
Next, all pair-overlap functionals must annihilate the retained subspace:

    sum_h B_lh u_ih u_jh u_ah=0 for all i!=j,l,a.      (7)

This includes genuine cubic interactions. If it fails, no background can
make the entire retained state product for all secrets.

When (7) holds, put x=x0+Kz and define

    R_(l,i,j) = K^T(B_l*u_i*u_j),
    b_(l,i,j) = (1/2) sum_h (-1)^x0_h A_lh u_ih u_jh mod2.

The sum defining b is even by the first condition. Equation (1), now mod4,
is exactly the binary system

    Rz=b.                                             (8)

R vanishes on retained directions, so these are constraints only on the
uniform complement outcomes. If consistent, success probability is
2^(-rank R); if inconsistent, it is zero. Thus a seemingly high yield d
must be weighed against an inverse-success batch cost 2^(rank R).
Conditioned output labels are NOT automatically IID. Selecting directions
from higher label bits also requires a new source proof.

This law is exact at q=8 only. Cubic and higher weighted carries at larger
moduli need their own ledger. A sample-count improvement at one level is
not an end-to-end decoder or a growing-modulus speedup.

## 5. A Narrow Approximate-Factorization Gate

At q=8, a nonproduct retained branch has squared fidelity at most
`(1+1/sqrt(2))/2` with ANY pure product state, for at least one secret.
Thus merely allowing small uniform per-branch error does not escape the
fixed-direction gate.

Proof: for a basis secret, the branch is a flat phase state i^f(z).
Its polynomial f modulo four has degree at most three, with even cubic
coefficients. If nonproduct, some retained bit j has nonconstant derivative
g(z_other)=f(1,z_other)-f(0,z_other). This derivative has degree at most two,
and all quadratic coefficients are even. Therefore i^g is a diagonal
Clifford applied to |+>^(d-1), a stabilizer state different from |+> up to
global phase. Their overlap magnitude is at most 1/sqrt(2). To see this
without a counting formula, some X stabilizer of |+> has expectation zero
or minus one in the other stabilizer state. Projection to its +1 eigenspace
has norm at most 1/sqrt(2), and that eigenspace contains |+>.

The one-qubit reduced state of bit j has off-diagonal magnitude at most
1/(2sqrt(2)), hence largest eigenvalue at most `(1+1/sqrt(2))/2`.
Fidelity with any fully product pure state is bounded by this eigenvalue.
The trace distance to every such target is therefore at least sin(pi/8).
The two-direction A=(1,1,1) control attains the eigenvalue ceiling.

For every q>=8, choose secret `(q/8)e_l`. Its effective residual phase is
again i^(F_l mod4). Consequently any violation of the conductor condition
has a secret/background witness with this constant gap. The native d<=31
cap also holds for protocols demanding PURE product approximation with
trace error strictly less than sin(pi/8), uniformly over secrets and every
complement branch. This extension remains local and review-pending.

This does NOT close average-over-outcomes error, selected secret distributions,
approximation to correlated states, or arbitrary channels/measurements.
Failure on one background does not by itself lower-bound its source mass.
Mixed-product targets have only the weaker projector-test distance bound
`1-(1+1/sqrt(2))/2`; do not silently reuse the pure-state trace formula.

## 6. Counterexamples And Falsification

The control A=(1,3,1,3,1,3), with physical directions {0,1,2,3} and
{0,1,4,5}, gives product outputs at every background at q=4. At q=8,
background zero still passes; exactly HALF the complement backgrounds fail.
Checking only a zero syndrome/background would therefore certify a false
all-outcome algorithm. The postselection system has rank one.

Other controls retain disjoint zero-sum blocks at q=8,16,256, and a cubic
obstruction that no complement postselection can repair. Passing the
conductor gate alone is not sufficient: even-label overlaps can retain
nonzero mod4 curvature. None of these bounded controls is a new toy problem
or an asymptotic hardness experiment.

Ways to disprove or escape this audit: find an error in the mixed-derivative
or conductor proof; exhibit a native fixed-basis/all-outcome counterexample
to (6); relax exact factorization with quantitatively useful approximate
states; let measured outcomes change the next retained subspace; use joint
packet interference; or decode the correlated state without factorization.
Each escape must retain its own source, state-consumption and success law.

## Coding Literature: A Possible Escape, Not A Contradiction

Pair/triple overlap constraints are familiar from
[Bravyi--Haah triorthogonal distillation](https://arxiv.org/abs/1209.2426).
The September preprint [San-Jose, 2609.08203v1](https://arxiv.org/html/2609.08203v1)
claims explicit asymptotically good binary CSS codes with higher-level
transversal gates, using AG codes and alphabet reduction. It includes
correction-free variants and a constant-overhead T-state protocol. These
claims need separate verification; we do not certify the preprint here.

Its selected codes, known transversal rotations and fixed hierarchy levels
are not native DCP batches with n unknown, randomly weighted phase generators.
To transfer the idea, establish a PUBLIC encoding compatible with those
native weights, a correction independent of the hidden secret, and rates
uniform across t=Theta(log n). Existing-code existence is not that bridge.

The code's known-gate correction cannot simply be replaced by the same
formula with unknown s. Nor can an unknown phase state be treated as a free
deterministic gate oracle. State injection can leave an unknown correction;
all program states, branches and further corrections must be costed. A
source-aware CSS measurement may escape the complement-Z class audited
here, but deserves a new exact operational contract before implementation.

## Next Research Tasks

Highest priority: outcome-adaptive transformations or a correlated-packet
decoder that extracts secret information without manufacturing independent
lower-level samples. Avoid a blind maximal-q=4-isotropy optimization.
For fixed-subspace postselection, seek polynomial construction with small
rank R on native labels; an isolated favorable batch is not source coverage.
Compose success through growing t and compare named sample-only sieves before
claiming improvement. Independently review the local derivation first.

Gemini owns routine production integration, regression and validation.
The standalone theory commands are:

    python theorems/dcp_carry_throughput_gate.py --save
    python -m pytest -q tests/test_dcp_carry_throughput_gate.py
    node research/certificates/dcp_carry_throughput_crosscheck.js

No candidate promotion, production CLI wiring, full-suite pass or commit is
claimed by this research pass.
