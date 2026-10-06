# Binary-Error Decoder Over Growing Two-Power Moduli

LOCAL DERIVATION / REVIEW PENDING. An actual classical decoder is implemented;
no independent theorem review, novelty, native subset-sum finder, general LWE
attack, accepted candidate or quantum speedup is claimed.

## Model And Result

Input A is an IID uniform n-by-m matrix modulo q=2^L, L>=2. Observe
b=A^T*s+e modulo q. The unknown s is arbitrary and e is any fixed Boolean vector,
both independent of A. Errors need not be independently random or uniform.
The SAME deterministic decoder handles every such fixed pair (s,e).

Let d=2n+binomial(n,2). The proposed source theorem gives failure probability
at most min(1,(2^d-1)*(3/4)^m). On its full-feature-rank event, the algorithm
finds the UNIQUE binary-error secret. With m=3d this is a polynomial-sample,
polynomial-input-bit-length algorithm with asymptotically exponential success.
The union bound can be vacuous at small n even when actual trials succeed.

This is an annihilator/linearization classical baseline in the spirit of
[Arora--Ge](https://eccc.weizmann.ac.il/report/2010/066/). The local contribution
is the implemented mod-four source and Hensel audit, not a claim that bounded
error algebraic learning or lifting is new. This does not solve the original
arithmetic witness problem: no bridge from IID Boolean subset sums to this
specific error source has been supplied.

## Mod-Four Decoder

For each column a_i define

    F_i(x)=(a_i*x-b_i)*(a_i*x-b_i+1).

Over Z/(2^L), F_i(x)=0 iff b_i-a_i*x belongs to {0,1}: consecutive factors
have exactly one odd unit, so the even factor must be zero modulo q. This
argument is specific to the two-power ring and consecutive error roots.

Write x=x0+2*x1 modulo4, with Boolean n-vectors x0,x1. Then

    F_i(x)/2 modulo2
      = sum_j [a_ij*(a_ij+1-2*b_i)/2] x0_j
        + sum_j [a_ij modulo2] x1_j
        + sum_(j<k) [a_ij*a_ik modulo2] x0_j*x0_k
        + b_i*(b_i-1)/2.

The numerator is always even. Linearize the d physical features
(x0_j,x1_j,x0_j*x0_k). Solve the binary linear equations by Gaussian elimination.
REQUIRE rank d and consistency; verify every product feature. A rank-deficient
solution is not a certificate and is not promoted by choosing arbitrary free
variables. The actual secret supplies a consistent product assignment on a
promised source. Full rank identifies its mod-four value uniquely.

## Pointwise Native Source Proof

Translate x=s+y modulo4 using actual binary addition, not XOR alone:

    x0 = s0 XOR y0,
    x1 = s1 XOR y1 XOR (s0 AND y0).

The resulting affine transformation of all d features is invertible. Constant
coordinates shift by the secret's feature word. In the translated equations,
b_i-a_i*s=e_i modulo4, and the constant becomes zero.
Writing a_i=B_i+2*H_i, the row has coordinates

    (H_i + B_i*(1-e_i), B_i, (B_ij*B_ik)_(j<k)).

B_i and H_i are fresh independent uniform binary vectors. For ANY fixed e_i,
the first block remains fresh uniform conditional on B_i. Rows are independent
across samples. Their d coordinates are NOT independent: the pair-product
block is constrained.

A nonzero linear functional with a first-block coefficient is fair. Otherwise
it is a nonzero multilinear Boolean polynomial of degree at most two in B_i.
Such a polynomial is nonzero on at least one quarter of inputs: split on a
variable of a highest-degree monomial and induct on the nonzero derivative;
each derivative-nonzero pair contains at least one nonzero function value.
No coordinatewise IID feature assumption or semi-regularity heuristic is used.

Thus every nonzero column-kernel vector annihilates m rows with probability
at most (3/4)^m. Union over 2^d-1 vectors proves the bound for each fixed s,e.
The small-source controls verify the entire n=1,q=4,m=3 law: all 32 fixed
secret/error pairs give full feature rank on exactly 42 of 64 native matrices.
Errors chosen after inspecting A are NOT covered by this probability claim.

## Unique Hensel Lifts

Once s_j modulo2^j is known, j>=2, seek s_(j+1)=s_j+2^j*delta. Modulo2^(j+1),

    F_i(s_(j+1)) = F_i(s_j) + 2^j*(a_i modulo2)*delta.

The derivative factor 2*(a_i*s_j-b_i)+1 is odd; the quadratic update term
vanishes at this precision. Solve

    B*delta = F(s_j)/2^j modulo2.

Feature rank d implies B has rank n (its columns occur in the feature matrix).
Every lift is uniquely determined; the true secret guarantees consistency.
Verify all final residuals belong to {0,1}. On malformed inputs inconsistent
linearization, nonphysical product features or failed lifts fail closed.

Naive binary elimination costs O(m*d^2+L*m*n^2) bit operations, in addition
to polynomial exact integer arithmetic on the L-bit input. Storage is
O(d^2+m*n*L) bits plus polynomial integer workspace. No loop over q, secret
enumeration, root table or field inversion is used.

## Falsifiers And Scope

- A native fixed-secret/fixed-error rank law violating the support bound,
  a missed binary addition carry or a nonunique full-rank lift falsifies this
  proposed theorem. Independent mathematical review remains essential.
- A fast decoder of THIS input distribution says nothing about standard
  Gaussian-error LWE, native phase states or sparse Boolean witnesses.
- Successful growing-q trials do not prove asymptotic success. The source
  proof, not the four seeds, is the asymptotic evidence under review.
- Production claims must separate implemented decoder, proved source,
  quantum reduction, classical comparison and novelty status.

## Reproduction

    python theorems/binary_error_hensel_decoder.py --save
    PYTHONPATH=theorems python -m pytest -q tests/test_binary_error_hensel_decoder.py
    node research/certificates/binary_error_source_crosscheck.js

The report stores hexadecimal native inputs for n=2,4,8,16 and
L=5,17,33,65. All four trials recovered their planted secrets. The Node
crosscheck independently reconstructs them with BigInt arithmetic.
