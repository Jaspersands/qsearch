# Predeclared Arithmetic Check

## Question

Can the existing Rees receiver's quadratic diagonal cancellation use a
polynomial-size label bank, without hiding an unbounded root solver?

Audit correction: `nil3_guarded_cyclic_dispatch.square_weights_capped`
ALREADY supplies this for `p = 3 mod 4`. The missing capability is the
`p = 1 mod 4` regime rejected by `required_bezout_arity`, not quadratic
cancellation in its entirety. The new implementation generalizes this
coverage and makes source-bank admission explicit. It does not improve the
known arity bound in the already covered regime.

Implement the published Ivanyos--Santha Proposition 9 construction, not a
new search heuristic. Inputs are public finite-field moment matrices. They
are arithmetic controls, not new oracle-problem candidates.

## Acceptance

- Exact nonzero witnesses on the ORIGINAL equations, including redundant rows.
- At most `(r+1)^2` used prefix columns for observed equation rank `r`.
- Admission requires `(rank_cap+1)^2` preallocated labels. All acquired copies
  are charged even if their output scale is zero. No quantum resampling.
- Exercise both early exits and the four-cell scalar construction.
- Exercise odd small fields and a 127-bit field, ranks 0, 1, 2, 4, 8 and 16.
- Include 127-bit primes in the NEW `p = 1 mod 4` regime, and a 64-bit
  prime with a 32-bit 2-primary component in `p-1`.
- Explicit finite root/scalar budgets; bad roots, malformed inputs and RNG
  exhaustion cannot produce accepted witnesses.
- Compare the arity formulas, not noisy wall-clock quantum speedups.

## Falsifiers / Limits

Any accepted nonzero moment, false nonzero support, uncontrolled field-size
enumeration or missing copy charge rejects the implementation. A successful
replay does not validate the complete HSP reduction, its source, or novelty.
The existing cubic solver still uses an expected-time polynomial-root backend;
this pass must not claim a fully clocked class-three quantum implementation.

Source: https://arxiv.org/html/1503.09016, Proposition 9.
Dependency: the local scalar-cancellation bundle and exact rank-row routine.
Repository integration is deferred while its migration is running.
