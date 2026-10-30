# Five-Agent Constructive Round

30 October 2026. The useful surviving result is classical: a constructive
trace-affine extension of the inverse-trace norm search, with a reviewed
polynomial-success proof and a verified sparse native witness. No quantum
candidate, novelty claim, or Shor-level result is promoted.

## Assignments

| Agent | Focus | Outcome |
| --- | --- | --- |
| Mencius the 2nd | Constructive quaternion commutative slices | Compatible slices reduce to an existing classical CM-order algorithm; finding compatible embeddings remains unresolved. |
| Hume the 2nd | A native use of fast orthogonal-polynomial transforms | Proposed compressed MacWilliams readout loses its signal on an explicit code family; no new quantum mechanism. |
| Newton the 2nd | Genus-zero norm construction and acceptance | Repaired the proposed canonical allocation to uniform allocation and supplied a first/second-moment success proof. |
| Banach the 2nd | Independent attack on Newton's proof | Checked the exact published divisor estimate, MDS count, scalar normalization, avoidance and growing-parameter bounds. |
| Heisenberg the 2nd | Simpler same-input classical attacks and code audit | Corrected the parent's false reciprocal-linear identity and excluded low-degree inverse-polynomial shortcuts; independently checked the live artifact. |

IDs in that order:

```
01a18b23-603c-7832-87cd-3e5c3facf667
01a18b23-6116-7a12-9cfb-be5fdcb29d24
01a18b2a-703a-7b30-bd92-33cf17de7da4
01a18b2d-5bbf-77e3-ae6d-0b779e205af5
01a18b2c-f026-79b0-aa2a-a587243b2223
```

These were focused automated reviews, not human review. The agents were
read-only; the parent integrated the constructive result. The immediately
preceding six-agent round is recorded separately, not counted again here.

## Constructive Result

Read [the complete argument](../../INVERSE_TRACE_GENUS_ZERO_NORM.md).
For b_i=Tr(c*alpha_i+d0), c!=0, the rational curve Y^2+Y=cX+d0 turns
the native search into an exactly checkable norm-factorization trial.
Uniform choices among ALL normalized factor allocations are essential.
An MDS first moment counts valid lifts including all nonvanishing
exclusions. Sawin's d_4 progression bound controls the second moment.
Their combination gives expected-polynomial classical search for every
odd native n>=15, not just existence or a random-polynomial heuristic.

The fixed n17 input uses points 0,...,288, basis-bit-8 targets (33 ones),
K36 and c512. It is outside the older dense support guard. The live
protocol produced a witness after 15 trials in 158.27s. Mathematical
success certificate: at least 1/21853701 per IID trial; no practical
runtime prediction follows from that deliberately conservative bound.
The witness and full polynomial certificate are retained in
`research/classical_baselines/inverse_trace_genus_zero_n17.json`.

Corrections retained: normalized scalar is unique, not a q+1 freedom;
the second moment uses the ORIGINAL squarefree progression, not an
unjustified infinity constraint; deterministic factor allocation is not
covered; zero field elements in python-flint must be compared explicitly
with zero, not tested by scalar truthiness. The latter was caught in the
new Fourier control and fixed before its passing replay.

The general singleton target still requires polynomial AS genus at least
127 at n17, even after arbitrary trace-only polynomial interpolation.
This extends the old rejection-law boundary but is not an algorithmic
hardness claim. The new theorem and that boundary cover different inputs.

## Quaternion Slice Outcome

Mencius supplied a more explicit compatible-embedding reduction. With
R=O_r(I), noncentral b in R, K=F(b), S=R intersect K, choose a in O with
the same characteristic polynomial and solve a*t=t*b for nonzero t.
Compute J=(t^-1 I) intersect K and w=q/nrd(t). A native generator in
this slice forces J*conjugate(J)=w*S. When this identity holds, the
polarized principal-ideal task is the classical CM-order problem treated
by [Lenstra--Silverberg](https://arxiv.org/abs/1706.07373); a solution z
gives t*z. Arbitrary field principality is not this compatible task.

The missing step is a polynomial-size efficiently constructed list of
compatible embeddings, not another field-PIP backend. An explicit
counterexample over Q has O=Z[1,i,j,k], I=O(1+i), q=2. The naive slice
a=b=j,t=1 yields J=2Z[j], with J*conjugate(J)=4Z[j], not 2Z[j], although
I has the promised generator and 2 is a norm in Q(j). Choosing a=k
instead works because (1+i)j=k(1+i). Thus a public convenient subfield
or a right-order identification alone does not supply compatibility.
This is a scoped counterexample, not a lower bound on embedding search.

## Transform Readout Outcome

The fast [Krawtchouk transform](https://arxiv.org/abs/2610.03581) is a
legitimate primitive, but its amplitudes are not weight probabilities.
For a binary code C of length N, let A_w count words of weight w and
a_w=A_w/sqrt(|C|*binom(N,w)). The vector has squared norm p_sym, generally
not one. The unitary maps a(C) to a(C_perp). After normalizing the input,
measurement of t has probability

```
q_t = A_t(C_perp)^2 / (|C_perp|*binom(N,t)*p_sym),
```

not the native undetected-error probability A_t(C_perp)/binom(N,t).
For succinct RM(1,m), N=2^m, the weight distribution is
A_0=A_N=1, A_(N/2)=2N-2. Therefore

```
p_sym = 1/N + (2N-2)^2/(2N*binom(N,N/2)),
Pr[weight-4 error undetected] = 1/(N-3),
q_4 = Theta(N^4*2^(-N)).
```

The native probability has an exact classical count: three distinct
points determine the fourth by XOR. The readout probability is about
7.58e-14 at N64 and 3.09e-69 at N256, even granting free preparation of
the normalized input. Classical sampling of t distinct columns also
gives polynomial additive-error estimates from the native succinct
evaluator. Generic amplitude estimation offers its usual quadratic
improvement without this transform. No transform backend is justified
by the proposed readout; this is not a lower bound on every QOPT use.

## Verification And Next Work

The parent added one certificate module, one focused test file, one
native artifact and the detailed proof note. No production CLI or UI
change, registry promotion, commit or push is part of this round.
See the latest AGENT_HANDOFF entry for final checks and the mechanical
integration contract. Keep uniform sampling, arbitrary targets and a
genuinely useful quantum mechanism explicitly unresolved. Do not turn a
classical elimination of a candidate family into a claimed quantum gain.

Final selected replay: 219 tests passed in 16.34s, including 16 new
controls; two Python compile checks and 12 site JavaScript syntax checks
passed. `qsearch.py validate` returned valid=true/issues=[]. This is not
the full repository suite or a Lean replay. The initial run had 218 passes
and one pre-existing stale proof-hash failure. Replaying the existing
algebraic-audit generator changed ONLY that hash; no assertion was waived.
Heisenberg's joint T,F tampering finding was repaired by adding exact norm
and point-polynomial assertions, then included in the passing replay.

The registry's 13 JSON files retain aggregate SHA256
79c8b3fca6c2bb7c70cca8116b8356bc3dc69734c682feeba16a8bbf1949c0fd.
The new native artifact SHA256 is
e86442023227f76462424022e32fbbb7c2a5702043042690ffeac91e89a67c8b.
Heisenberg verified its field irreducibility, every syndrome/target,
all exact polynomial identities, scalar/degree constraints, and all trial
hashes/allocation choices using separate binary-polynomial arithmetic.
The parent's durable regression independently checks native constraints
and replays polynomial hashes without expensive fresh factorization.
