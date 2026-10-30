# Balanced Signed MPI: A Bounded Coherent Compilation Argument

2026-10-23. LOCAL THEORETICAL COMPLETION, INDEPENDENT REVIEW PENDING.
No compiled native quantum circuit, optimizer execution, hardness proof,
novelty determination, or speedup admission. This is not another pilot
ansatz: it addresses the existing candidate's implementation/access gap.

## 1. Same Problem, Not A New Oracle

Keep the public instance from `research/BALANCED_SIGNED_MPI.md`:
F=F_(2^h), N=2^h-1>3, disjoint points t_i,z_j, a primitive g, and

    B_ij = log_g(t_i+z_j) mod N,
    S(x) = mean_i cos(2*pi*((B*x)_i-c_i)/N), x in Z_N^n.

The field presentation, points, g, B, and centers c are public. Both sides
receive the SAME B. The existing rational separation and mean identity
are dependencies, not discoveries of this pass. The signed decoder comes
from [Mazumder--Niroula, Section 6.2/B.2](https://arxiv.org/html/2610.06753);
the repository's balanced-box extension supplies the stronger box/readout
guard. Its algebraic Lean result does not formally verify this compilation.

For E={y in {0,+1,-1}^m : P(y)<=a, Q(y)<=a}, require n>=2a+2.
For rational 0<t<1, let Z be its mass under independent probabilities
(1-t,t/2,t/2). The existing exact mean is

    mu = sqrt(2*t*(1-t))*Pr_(m-1)[P<=a-1,Q<=a]/Z.

The new source and success bounds require certified Z>0 and a positive
inverse-polynomial score margin, not merely a nonzero successful branch.

## 2. Two Preprocessing Models Must Stay Separate

**Explicit B supplied:** check g^(B_ij)=t_i+z_j by binary field
exponentiation in polynomial bit time. Irreducibility of the degree-h
field modulus is also classically testable. A primitive generator is a
standard input promise; if certification is required, its order needs a
factored-order certificate or separately paid construction. Do not claim
that arbitrary factorization of N is automatically free.

The quantum algorithm below uses NO discrete-log subroutine and NO
coherent logarithm table. The decoder only needs g^s, not log_g(s).
Explicit B has mn*h bits up to encoding constants, so reading it is paid.

**Only points supplied:** constructing B may itself require hard discrete
logarithms. If q=2^h is polynomial in the actual instance size, an explicit
table of all q-1 powers gives a fully classical polynomial preprocessing
route; primitive-generator search can also be paid in q. The native
q=8192 case is in this regime. If q is exponentially large and B is absent,
do not advertise a new access-matched advantage by granting B only to the
quantum side. That would be a different problem, possibly using Shor.

## 3. A Bounded Source Instrument

Use two qubits per symbol, with 00=0, 10=+1, 11=-1. A single variable-angle
Ry gate followed by controlled-H prepares the three desired amplitudes.
Controlled-H has an exact constant-size Clifford+T realization, for example
by conjugating controlled-Z with Ry(pi/4) and Ry(-pi/4). Its control-zero
branch is identity. The unused fourth symbol is rejected by validation.

Reversibly compute P,Q and the box-membership bit, using fixed-width
counters. Measure ONLY the membership bit. On acceptance, uncompute both
counters and all predicate workspace. On rejection, discard/reset every
register and use a fresh product preparation. After L attempts abort the
round if none succeeded. Ideal preparation succeeds with probability

    A = 1-(1-Z)^L.

Every successful retry index yields exactly the same normalized pilot;
retaining that index does not reveal y. In contrast, measuring the counts
or leaving them in discarded workspace destroys interference between the
count sectors. In this family it kills the score's nearest-symbol
transitions and makes the ideal mean zero. This is tested explicitly.

Apply the center phase exp(-2*pi*i*c.y/N), then compute z=B^T*y mod N.
Use at most two controlled constant additions/subtractions per matrix
entry. B is fixed circuit data; no qRAM access is assumed.

## 4. A Total Decoder And Its Reversible Use

The following classical program has a polynomial clock on ALL bit strings,
not just on promised syndromes. Invalid inputs return flag=0 and y=0.

1. Reject h-bit syndrome words >=N. Compute g^(z_j) by ordinary binary
   field exponentiation, O(nh) field multiplications, with no table lookup.
2. Interpolate the degree-<n value polynomial and construct the degree-n
   vanishing polynomial at the public evaluation points.
3. Run extended Euclid, padded to at most n degree-decreasing iterations.
   Stop at the numerator degree cap. Check denominator, reduce by gcd,
   normalize, and verify both degree bounds and monicity. Every attempted
   inversion has a checked nonzero branch; invalid branches are total.
4. Evaluate numerator and denominator at every public support point.
   Build the signed root indicator. Check disjoint roots, exact root
   counts, interpolation equations and the ORIGINAL syndrome B^T*y=z.
   A failure yields the fixed invalid output, not an exception or retry.

The existing reference decoder tests the corresponding classical algorithm.
On the licensed box it returns the unique original y. Off that box it is
allowed to return any valid licensed inverse or the invalid flag. It must
not invent a promised preimage or run an unbounded search.

Ordinary naive polynomial arithmetic costs O(n^3+mn+nh) field operations.
Using the conservative O(h^3) bound even for field inversion gives ordinary
Boolean time T=O((n^3+mn+nh)h^3), with explicit arrays and polynomial-sized
coefficients. A conservative oblivious simulation has O(T^2) Boolean gates.
Store its full history, copy its output, and reverse the history to obtain
a clean reversible decoder of O(T^2) gates and workspace. This is a
deliberately loose existence bound, NOT a practical gate estimate. Data-
dependent degree/index operations need explicit scans/multiplexers in a
real compiler; the word-RAM count must not be relabeled a gate count.

Compute D(z) into fresh scratch, XOR its two-bit symbol encoding out of
the ORIGINAL y register, then reverse D to erase its outputs/flag/scratch.
Write w_y for the normalized nonnegative pilot weight and
alpha_y=w_y*exp(-2*pi*i*c.y/N). Thus, on the source support,

    sum_y alpha_y |y>|B^T y>|0> -> |0> sum_y alpha_y |B^T y>|0>.

All invalid branches still extend to a unitary because D is a total
classical function implemented by compute/copy/uncompute. No inverse of
a one-way map is supplied as an oracle, and no measurement of y occurs.

## 5. The Correct Fourier Operation

Apply n copies of Q_N, with convention
Q_N|z> = N^(-1/2) sum_x exp(+2*pi*i*z*x/N)|x>.
The resulting amplitudes are proportional to
sum_y w_y exp(2*pi*i*y.(Bx-c)/N). This fixes the sign convention.

Use an arbitrary-modulus Fourier circuit, NOT a power-of-two QFT on an
embedded h-bit register. Uniform efficient arbitrary-order QFT constructions
are established; [Mosca--Zalka](https://arxiv.org/abs/quant-ph/0301093)
give a construction with efficiently computable gate parameters. Standard
finite-gate synthesis yields polynomial cost in h and log(1/eta) for error
eta. Composite N is allowed; field Gaussian elimination over Z_N is not
part of this operation. No claimed optimized QFT constant is needed here.

Our F16 diagnostic compares Q_15 with the incorrect Q_16 padding, retaining
invalid outputs as ABORT. The distributions disagree even before any
native-size resource question. This is an implementation falsifier, not
an oracle-problem benchmark or a scalable QFT implementation.

## 6. Complete-Instrument Precision, Not Rare-Branch Precision

Let epsilon be the TOTAL variation/half-diamond error budget for ONE
complete bounded round, including source retry records and ABORT.
Allocate operator-norm approximation errors at most

    epsilon/(3 L m) per product-source rotation,
    epsilon/(6 m)   per center-phase gate (at most 2m),
    epsilon/(3 n)   per Q_N.

Counters, finite-field arithmetic and Boolean reversible gates are exact
logical operations. A fault-tolerant physical realization must separately
pay their logical-failure budget; this note does not model hardware noise.
The telescoping channel bound, including measurement and reset, sums to
epsilon. There is NO division by Z and no normalization of an uncontrolled
rare branch. It remains valid if approximation creates a small amplitude
on invalid symbol/syndrome encodings, since the full instrument is total.

For score threshold tau, evaluate each cosine with a certified rational
interval of width <=2 eta. Accept only if the mean LOWER endpoint is >=tau.
Acceptance is always valid, including scores arbitrarily close to tau.
Reject any noncanonical measured assignment as ABORT before scoring.
Every score >=tau+2 eta is accepted. Our executable verifier uses Machin's
identity for pi and alternating Taylor remainders, not a floating cutoff.

If the ideal conditional mean is >=mu0 and tau+2eta<mu0, then

    p_tail >= (mu0-tau-2eta)/(1-tau-2eta),
    p_round >= [1-(1-Z0)^L]*p_tail - epsilon.       (1)

Subtract epsilon AFTER multiplying by preparation success. The larger
expression A*(p_tail-epsilon) would incorrectly apply an unconditional
instrument bound as though it were conditional on successful preparation.

Fresh bounded rounds have conditional success at least p_round. For
k=ceil(1/p_round), (1-p_round)^k<=1/2 by Bernoulli's inequality; k*s rounds
give failure <=2^(-s), including all explicit aborts. No near-threshold
result is silently accepted, and no infinite restart loop is hidden.
This is a verified SEARCH guarantee. It is not total-variation closeness
of the repeated final output law to the ideal sampler at error 2^(-s).
The per-round error need not be divided by the round count for this
success-amplification argument; that would be needed for a different
whole-output-distribution claim.

## 7. Native Certified Envelope

For m=6000,n=420,h=13,a=209,t=13/200, exact multinomial arithmetic and a
rational square-root enclosure re-establish Z>7/10 and mu>342/1000.
Use tau=3/10, eta=1/1000, epsilon=1/1000, L=2. Then (1) is

    p_round >= (91/100)*(20/349)-1/1000 > 1/20.

The conservative planner uses k=20, so 800 rounds and at most 1600 raw
preparations give failure <=2^-40. This is a WORST-CASE cap, not a claim
that an experiment ran 800 times or that typical cost is that large.

Each round has at most 12,000 variable source rotations, 12,000 center
phases, 5,040,000 controlled modular additions/subtractions, 420 genuine
Q_8191 operations and two reversible decoder calls. Data registers alone
occupy 17,460 logical qubits, excluding counters, Fourier ancillas and the
potentially dominant decoder workspace. These are logical operation
counts, NOT Toffoli counts, T counts, physical qubits or wall time.

For a growing family, explicit B, paid rational-t bit length, input h and
inverse-polynomial Z/score margin give a polynomial algorithm through the
construction above. A family whose useful margin vanishes exponentially
does not inherit that conclusion. No additional empirical hardness claim
is established by this compilation argument.

## 8. Self-Attack, Remaining Work And Handoff

- This does not independently prove the balanced-box mean/readout theorem.
  A flaw in that dependency invalidates the success guarantee.
- Reversible compilation is a CONSTRUCTIVE COMPLEXITY argument, not generated
  native gates. The finite instrument reference decoder is an enumerated dictionary,
  used only to test the instrument. It must never replace rational decoding
  in an asymptotic claim.
- A separate dependency replay executes the UNCHANGED rational decoder body
  over F_(2^64) with exponentiation replacing its power-table access and
  explicit B replacing its log-table syndrome check. All 21 licensed
  patterns decode; an outside-box pattern is rejected. Its public fixture
  lies in an easy F16 subfield, whose 15 logs construct B. This establishes
  neither a hard input nor a new decoder; it checks the table-free access
  substitution without materializing a 2^64-entry table. Only the two
  required functions are AST-loaded to avoid unrelated offloaded imports.
- Exact arithmetic tests and the existing finite decoder tests do not
  certify optimality, classical hardness, practical runtime, or novelty.
- Explicit B is paid public data. A points-only large-field variant needs
  a separate access-matched preprocessing comparison.
- The largest scientific gap is still a structural classical optimizer
  or a meaningful independent application/reduction, not state preparation.
  Published FFT/systematic searches already exist; do not rediscover them.

After migration, Gemini can integrate this budget and the invalid-branch
requirements, then compile a genuinely reversible bounded rational decoder
and test its garbage cleanup. Preserve `compiled_quantum_solver=false`
until that is done. Do not relabel the finite dictionary as that compiler.
No registry candidate admission, UI edits, moving-checkout edits, commits,
or restoration of legacy circuit search are part of this pass.
