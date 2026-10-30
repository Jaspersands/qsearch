# Two-Component Norm Completion: A Scoped Classical Attack

27 October 2026. Scoped independent AI mathematical review completed; see
REVIEW_RESPONSE.md. No quantum
advantage, fixed-prime asymptotic dequantization, or novelty claim.

## Question And Decision

Can a quadratic completion use an auxiliary code of dimension smaller than
the number of parity checks? The one-variable construction cannot: its
linear syndrome map has at most that auxiliary dimension. A two-component
anisotropic norm can, but it loses automatic coordinate nonvanishing.
This note pays that loss with an explicit probability and an executable
rank certificate. It is useful only where those certificates succeed.

The native input remains an explicit full-row-rank B in F_q^(k by m), with
q ODD, an arbitrary syndrome s, and By=s with every y_i nonzero.
The attack additionally CONSTRUCTS or is supplied a public auxiliary matrix
A with r independent rows and h such that

    sum_i B[j,i] h[i] A[u,i] A[v,i] = 0   for all j,u,v.        (1)

These data are verified. A supplied A is not automatically obtainable from
B. The native control uses its already public curve/evaluation construction;
the cost and additional representation are retained. No oracle, hidden
witness, quantum state or full-field truth table is used.

## Algorithm And Exact Certificate

Let T=support(h), set y_i=1 outside T, and subtract those columns from s.
Choose a nonsquare nu. Draw independent uniform offsets a,b in F_q^T and
put, for z,w in F_q^r,

    u = a + A_T^t z,       v = b + A_T^t w,
    y_T = h_T * (u^2 - nu v^2).                              (2)

By (1), the quadratic terms in the syndrome vanish. Define

    M = [2 B_T diag(h*a) A_T^t | -2 nu B_T diag(h*b) A_T^t],
    c = B_T [h*(a^2-nu b^2)].

Solve M(z,w)=s_T-c. Require rank(M)=k, so every original syndrome is
reachable. Compute a particular solution t0 and a basis N for ker(M).
For coordinate i let E_i(z,w)=((A^t z)_i,(A^t w)_i), and define

    rho_i = rank(E_i N),
    p_i = q^(-rho_i) if -(a_i,b_i)-E_i t0 is in image(E_i N),
          0 otherwise.

Under a UNIFORM kernel coefficient vector, p_i is exactly the probability
that both u_i and v_i vanish. Since nu is a nonsquare, those are precisely
the zero outputs in (2). The union bound eta=sum_i p_i therefore certifies
success probability at least 1-eta for this FIXED offset/target pair.
The executable solver admits only eta<=1/2. It samples a capped number of
kernel points and independently verifies the original B,s relation.
An exhausted cap is UNKNOWN, never UNSAT or a hardness certificate.

When all rho_i=2, eta=|T|/q^2 for EVERY syndrome. With q^2>=2|T|,
expected at most two kernel samples suffice. The output law is not claimed
uniform on native witnesses. Particular-solution-only sampling would not
have this probability guarantee; the kernel randomness is essential.

## A Sufficient Offset Theorem

Assume A_i is nonzero for all i in T, and for EVERY nonzero row combination
c in rowspan(B), the columns A_support(h*c) span F_q^r. This is a structural
promise, not something inferred from a few random c tests.

For fixed coefficient lambda!=0, put c=B^t lambda. The two blocks of
M^t lambda are independent uniform vectors in F_q^r: each is the image
of its independent uniform offset under a
surjective linear map. For a fixed coordinate i, the chance that these
blocks lie in the two copies of span(A_i) is q^(2-2r).

If rank(M)<k, this event occurs for some lambda!=0 at every i. If rank(M)=k
but rho_i<2, rowspace(M) meets rowspace(E_i) nontrivially, so the same
event occurs for some lambda!=0. A union bound gives

    Pr[rank(M)<k OR some rho_i<2]
        <= min(1, |T| (q^k-1) q^(2-2r)).                   (3)

Thus when the right side is at most 1/2 and q^2>=2|T|, independent offset
trials followed by kernel sampling give a Las Vegas expected-polynomial
classical solver. A bounded implementation has explicit failure caps.
The field-size inequality ALONE does not guarantee a good offset. One
simple sufficient corollary, under the same structural promises, is
2r>=k+4 together with q^2>=2|T|; otherwise retain bound (3) separately.
All matrix arithmetic and random field sampling cost poly(k,m,log q);
nonsquare acquisition by Euler testing has expected constant trials.
The Python backend, unlike the mathematical statement, supports only
verified odd primes below 2^63 and a supplied verified nonsquare.

For complete AG auxiliary E=ev L(D_A), evaluation is injective on any set
larger than deg(D_A). If V has minimum distance d_V and h has z zero
coordinates, d_V-z>deg(D_A) implies the spanning promise. Base-point
freeness on T must still be checked. This observation does NOT construct
D_A, h, the curve, or a good divisor distribution for free.

## Comparison And Limits

The cancellation idea and auxiliary-code framework are prior art:
[Ragavan--Shutty, Section 6.1, Theorem 6.2](https://arxiv.org/html/2610.00502v1#S6.SS1).
Their displayed construction keeps the second norm component constant,
making every coordinate nonzero automatically and requiring a rank-k map
from r variables. Here both components vary: 2r variables can reach k
when r<k, but the simultaneous-zero cost must be paid. No exhaustive
novelty audit of this elementary variant has been performed.

The basic field-size condition is q=Omega(sqrt(m)), rather than the
earlier generic greedy condition q>k+1 for k=Theta(m). This is NOT a
general matrix solver: (1), the offset/rank tests and source costs remain.
At fixed q=1019 the rank-two bound becomes vacuous as m grows. Higher
auxiliary dimensions do not turn a two-dimensional coordinate marginal
into a higher-rank one. Do not infer a fixed-prime asymptotic solver.

The existing degree-eight AG input is already classically easy by several
other attacks. Running this method on it is an interface control, not a
new dequantization or evidence against the harder intended distribution.
The comparison of r<k only rules out the ONE-VARIABLE method using this
SAME auxiliary A, not all other auxiliary codes or classical algorithms.
This attack does not apply to binary inverse-trace acceptance constraints.

## Falsifiers And Next Scientific Gate

- A nonzero mixed quadratic residual in (1) invalidates linearization.
- A square nu invalidates the equivalence between norm zero and pair zero.
- A deficient syndrome rank invalidates all-syndrome reachability.
- Missing kernel-image membership/rank accounting invalidates eta.
- An actual sample not satisfying original B,s and all nonzeros is a bug.
- Failure to construct A,h from the stated input blocks a native algorithm.
- A fixed-q experiment cannot establish scaling beyond m/q^2<1.

Next work should test whether the SAME fixed-prime input admits a genuinely
constructive way to avoid simultaneous zeros once the union bound fails,
or find a useful native reduction. More small controls or larger primes
will not resolve that question. Do not promote a candidate from this pass.
