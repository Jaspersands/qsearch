# Reciprocal-Trace Hidden Shift: Paid Corollary, Existing Endpoint

31 October 2026. Source-model correction and independently reviewed written
corollary. No novelty, classical hardness, separation, native cryptanalytic
application or quantum implementation. This is a bounded selection audit,
not a new oracle-problem campaign.

## Exact Input And The Prior Negative's Scope

Supply a public irreducible polynomial and basis for F_q, q=2^n. The only
unknown is s. The input oracle is the reversible BIT map
U_s|x,b>=|x,b+Tr(inv0(x+s))>, where inv0(0)=0. Seek s. Public evaluation
of f(x)=Tr(inv0(x)) costs poly(n). Coherent oracle access is an assumption;
neither passive classical samples nor an actual stream cipher supply it
automatically. A full explicit q-entry table has a different input size.

The corpus's trace_kloosterman_x_plus_inv negative does NOT solve this
problem. `../theorems/trace_function_search.py` chooses an odd prime p and
hands its decoder the FULL value z+z^-1 in F_p. Clearing that denominator
gives a quadratic. Here one sees only an F2 trace. Away from z=0, the
analogous equation is

    sum_(j=0)^(n-1) z^(q/2-2^j) + b*z^(q/2) = 0,

with degree q/2 for b=1 and q/2-1 for b=0, and the zero-extension case
must be added separately. If B(z) denotes the displayed sum without its
b term, the exact zero-extended equations are z B(z)=0 for b=0 and
z^(q/2)+B(z)=0 for b=1; both have degree q/2 and q/2 roots.
This degree growth is not a hardness proof or
a lower bound for other algorithms. The old repeated same-direction
finite-difference diagnostic is also vacuous: D_a^2=0 for every Boolean
function on a characteristic-two additive group. Independent source review
confirmed both mismatches. Exhaustive candidate filtering is legal but
costs q times the sample count; O(n) informative bits alone do not pay it.

## Paid Fourier-Phase Construction

Write psi(z)=(-1)^Tr(z) and W(u)=sum_x psi(inv0(x)+ux). The audited
`RECIPROCAL_TRACE_SOURCE_ACCESS.md` gives W(0)=0 and, for u!=0,
W(u)=#E_u(F_q)-q for E_u: v^2+zv=z^3+u. This is the known
[Ahmadi--Granger Lemma2.1 identity](https://arxiv.org/pdf/1104.3882), with
the zero-extended Kloosterman convention. Exact characteristic-two point
counting costs poly(n); the repository's small exhaustive counter is not
that backend.

One U_s query prepares q^-1/2 sum_x psi(inv0(x+s))|x>. The additive Fourier
transform gives amplitudes W(u)psi(us)/q. Compute W(u) exactly, apply its
sign, and uncompute; take arbitrary sign on zeros and handle u=0 without
the singular curve. An inverse transform gives s with probability

    p_s = (sum_u |W(u)|)^2/q^3 >= q/(1+2sqrt(q))^2.

The inequality uses Parseval sum W^2=q^2 and Hasse max|W|<=1+2sqrt(q).
The field trace-pairing conversion and Hadamards implement the additive
Fourier transform. A uniform exact point-count algorithm can be made
reversible with polynomial padded work and clean workspace. Approximate
orders do not suffice to decide the sign. There is no supplied Fourier
oracle, field-sized advice or free postselection in this written argument.
The spectral phase method is established hidden-shift machinery; no new
framework follows from this specialization.

For a!=0, c=a^-1, the exact autocorrelation is

    C(a)=sum_x psi(inv0(x)+inv0(x+a))
        = W(c)-2+2psi(c).

To see this, put x=at and y=1/(t^2+t) off t=0,1. The possible y are
nonzero with Tr(1/y)=0, each with two preimages. Expand their indicator;
the two exceptional t contribute 2psi(c). Thus C(a)<=1+2sqrt(q).
For n>=3 this is strictly less than q, so the shift is identifiable and
every false candidate passes a fresh uniform equality query with
probability at most rho=[1+(1+2sqrt(8))/8]/2<0.916. Independent verification
and O(log(1/epsilon)) candidate repetitions give bounded-error recovery.
At n=2, f(x)=Tr(x): shifts with equal trace are indistinguishable. The
theorem must exclude this case or output its period coset. At n=1 recovery
is elementary.

## The Decisive Existing Quantum Comparator

Point counting is not needed for polynomial-time solvability. The primary
[Gharibı1207.4537, Theorem5 and Simon reduction](https://arxiv.org/pdf/1207.4537)
gives the relevant known injectivization mechanism. Choose t independent
uniform public offsets v_i and h(x)=(f(x+v_i))_i. For fixed x!=y,
Pr[h(x)=h(y)]<=rho^t. Union bound over fewer than q^2/2 pairs gives an
injective h except probability delta with

    t >= (2n log(2)+log(1/delta))/(-log(rho)).

Then H(x,0)=h(x), H(x,1)=h(x+s) is exactly two-to-one, with Simon period
(s,1). O(n+log(1/epsilon)) Simon samples recover it. Each H call costs
O(t) shifted-bit queries and public evaluations; even without controlled
oracle access, compute each bit in scratch, conditionally copy and uncompute.
Total oracle cost is O((n+log(1/epsilon))^2), with polynomial arithmetic.
Independent review accepted this reduction and the finite exception.

The public f model also admits O(n) CLASSICAL queries followed by exhaustive
candidate filtering, by the same agreement bound. Thus black-box lower
bounds in which BOTH f and g are unknown cannot transfer to this source.
No polynomial-time classical decoder is established by this audit.

The exact Sage source-scope control
`classical_baselines/reciprocal_trace_shift_scope.json` checks all 25
nonzero-a autocorrelations for n=2,3,4, the F4 ambiguity, both zero-extended
trace equations, and a separate F17 full-value quadratic recovery. It is
finite calibration, not an asymptotic hardness test or quantum execution.

## Research Decision

The candidate offered poly(n) quantum time versus exhaustive O(2^n poly(n))
classical recovery, but that comparison is not a separation and the quantum
endpoint already follows from Simon. Inverse-trace predicates occur in
other work, yet no independently motivated application with precisely this
shift promise and paid coherent access was established here. Park the line;
do not build a point counter, simulator, benchmark or new receiver. Retain
the useful source-scope correction without weakening the original negative
on its actual prime-field/full-value input. Reopen only for a distinct
native model whose real blocker is removed by the spectral construction.
