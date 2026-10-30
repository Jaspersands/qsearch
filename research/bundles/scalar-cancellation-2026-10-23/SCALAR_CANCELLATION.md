# Constructive Scalar Cancellation For The Bounded-Index Receiver

2026-10-23. A missing classical primitive is now implemented and tested.
This is NOT a new SDE theorem, a quantum receiver, an independent validation
of the proposed Rees algorithm, or evidence of classical hardness.

## Decision

The existing `central-rank-2026-10-23/central_rank.py` composes scalar
diagonal solves on disjoint supports, but previously used an unimplemented
general scalar callback. Its finite higher-degree tests used exhaustive
small-field fixtures. This bundle supplies a real callback for every odd
prime and every reduced degree g dividing p-1. It has a uniform polynomial
arithmetic bound in g and log(p), with explicit randomized abort caps.

It closes that implementation dependency for the bounded-codimension/FPT
controller. It does NOT implement the different, polynomial-in-rank SDE
algorithm needed by the general fixed-class construction. The composer
still consumes (g+1)^r columns at observed equation rank r, subject to its
full preallocated public-rank-cap bank. Do not silently call that polynomial
in an unrestricted r.

The scalar-solvability result and recursive composition are already prior
art: [Ivanyos--Santha, Fact 2 and the paragraph following it](https://arxiv.org/html/1503.09016).
The implementation below uses a different, explicitly capped elementary
randomized route, rather than pretending that the cited deterministic
algorithm has been compiled. No novelty is claimed for its ingredients.

## Exact Contract

Given canonical public coefficients a_0,...,a_g in F_p, output a nonzero
tuple x with sum_i a_i*x_i^g=0. No hidden subspace, secret coefficient,
source amplitude, oracle table, or preselected favorable label is supplied.
Only the degree is factored. No factorization of the unrestricted p-1 is
needed. The prime-field check uses the same FLINT primality routine as the
repository; the arithmetic proof assumes that the modulus is genuinely prime.

If any coefficient is zero, its unit vector is a solution. If g=1, solve
the two-term linear equation. The remaining arguments assume all a_i are
nonzero and g>=2. Every output is verified exactly. Resource-cap failures
return no witness; they never become an all-zero scale vector.

## 1. Small Fields: A Deterministic Sumset Construction

This branch is permitted ONLY when p<=16*g^4. Enumerate the power image

    P = {x^g : x in F_p},  |P| = 1+(p-1)/g,

retaining one root per image value. Fix x_g=1 and find -a_g in

    a_0*P + ... + a_(g-1)*P.

The repeated Cauchy-Davenport inequality gives cardinality at least
min(p, 1+g*(|P|-1))=p. A dynamic program with predecessor witnesses finds
the desired representation; early termination simply sets unused coordinates
to zero. The last coordinate remains one, so nontriviality is automatic.
See the prime-field sumset statement in this
[research paper](https://arxiv.org/abs/1202.1816).

The implementation uses at most g*p*|P| attempted sum transitions, plus
one cached power-image table. Under this branch guard that is polynomial
in g. It is NOT an uncharged O(p) method for unbounded large primes. The
report records each enumerated field element and each attempted transition.

## 2. Large Fields: A Uniformly Successful Curve Trial

For p>16*g^4, use only the first three coefficients and set x_2=1:

    a_0*x^g + a_1*y^g + a_2 = 0.

The projective curve a_0*X^g+a_1*Y^g+a_2*Z^g=0 is smooth: the
coefficients are nonzero and p does not divide g. Its genus is
(g-1)(g-2)/2. Hasse-Weil and at most g points at infinity imply

    N_aff >= p+1-(g-1)*(g-2)*sqrt(p)-g > p/2.

Each x has at most g corresponding y values. Thus a uniform x has a
solution with probability at least 1/(2g), UNIFORMLY in the coefficients.
The standard curve bound and Fermat genus are stated, for example, in
[Moments of Gaussian periods and modified Fermat curves](https://link.springer.com/article/10.1007/s11139-025-01090-x).

One trial draws x, computes v=-(a_0*x^g+a_2)/a_1, and checks whether v
has a g-th root. If so, return (x,y,1,0,...,0). This argument applies to
adversarial coefficient vectors, not just random labels. A fixed seeded
replay is a correctness test, NOT evidence for this probability statement.

## 3. Roots Without An Uncharged Discrete-Log Oracle

Let pi be the prime divisors of g and write p-1=M*Q, where M is the full
pi-smooth part and gcd(Q,g)=1. This decomposition only requires factoring
g and repeatedly dividing p-1 by those small factors.

Draw v uniformly from F_p^*, set eta=v^Q, and accept exactly when
eta^(M/l)!=1 for every l in pi. This produces a generator of the order-M
subgroup with probability product_(l in pi)(1-1/l)>=1/g. Sampling is capped.

For a nonzero g-th power a, split it into its coprime primary components:

    a_M = a^[Q*(Q^-1 mod M)],
    a_Q = a^[M*(M^-1 mod Q)]       (a_Q=1 if Q=1).

Compute L=log_eta(a_M) by ordinary Pohlig-Hellman digit lifting on each
l-primary component, then CRT. Each digit lookup has at most l<=g
entries. The number of digits is O(log p); there is no search over M.
Because a is a g-th power and g divides M, the canonical L is divisible
by g. A root is

    eta^(L/g) * a_Q^(g^-1 mod Q).

The code independently checks each component logarithm, the CRT logarithm,
and the final root. Euler's criterion first rejects genuine nonresidues.
No black-box polynomial factorization/root routine is used. The Q=1 case,
mixed prime factors, and long prime-power digit chains have separate tests.

This is smooth-order discrete logarithm, not a fast algorithm for general
discrete logarithms, and provides no new attack on ECDSA.

## 4. Complete Classical Failure Budget

Suppose the caller declares at most C scalar calls and an abort budget
2^-s. Set b=s+ceil(log2(C+1)). Share ONE root-engine setup across all calls.
Cap its generator search at g*b attempts and each curve solve at 2*g*b.
Then each failure probability is at most 2^-b, and a union bound gives

    Pr[any arithmetic sampling abort] <= (C+1)*2^-b <= 2^-s.

This holds conditionally on every prior public history, under independent
uniform random draws. No independence between scalar coefficient vectors
is required. Small-field and linear branches have zero randomized failure.
The backend enforces C and latches randomized failure; it cannot silently
extend a failed attempt. Python's standard random-source implementation and
FLINT's input primality check are ordinary trusted runtime dependencies,
not a bit-level verified implementation. No wall-clock deadline is asserted.

For the existing composer at public rank cap kappa, use
C=((g+1)^kappa-1)/g (or zero at g=1). Choose s after allocating the total
receiver's failure budget across ALL merge nodes. One merge's 2^-64
default is not a whole large-tree error budget. Classical retries, if used,
operate on the saved public labels before any controlled dilation, with
their additional costs charged; source labels must not be resampled.

## 5. Attempts To Falsify This Construction

- Even-degree signs: over F5, nonzero fourth powers are all one. Four
  terms cannot cancel, and -1 is not a fourth power. The solver correctly
  uses all five inputs. It never imports the odd-degree sign shortcut.
- Hidden field enumeration: the large-prime tests use a 128-bit prime
  congruent to 1 modulo 27720. Degrees 2 through 12 are genuinely
  nonbijective there, and the field-element scan count stays zero.
- Missing higher primary digits: a prime with 2^27 dividing p-1 exercises
  many lifting digits, not just the first residue class.
- Bad randomness: constant unsuccessful draws exhaust the relevant cap
  and return no witness. Uniformity is a stated assumption, not tested
  into existence by deterministic pseudorandom trials.
- Corrupt arithmetic: a deliberately wrong root is rejected by the final
  exact scalar moment. A zero witness is separately rejected.
- False source savings: a rank-one observation with public cap three still
  pays all 125 fourth-power columns. Unused columns are assigned zero
  scales, not refunded or reused as independent targets.
- Characteristic: an initial degree-9/F7 integration fixture was rejected
  by the existing degree<p contract. It was replaced with degree-9/F13;
  the invalid case remains a rejection test.

## Remaining Scientific Blockers

The public-label arithmetic gap is smaller, but none of the following has
been established by this pass: coherent source preparation, the full Rees
quantum receiver, an independently reviewed new HSP theorem, a natural
hard application, or a better-than-classical end-to-end algorithm. The
general fixed-class polynomial-in-rank cancellation path remains separate.
Do not spend another pass enlarging scalar test grids. The next useful
step is independent scrutiny of the whole reduction or an explicit native
application that survives its existing classical attacks.
