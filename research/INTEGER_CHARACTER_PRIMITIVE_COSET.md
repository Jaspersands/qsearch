# Classical Primitive-Coset Construction

Status: a **deterministic finite classical falsifier**, plus a written
asymptotic reduction to lower-dimensional exact CVP. Not a polynomial-time
classical theorem for the whole family, a quantum result, or a new lattice
algorithm. The asymptotic reduction is pending independent review.

## Scientific Question

Can classical algorithms exploit the harmonic weights in
INTEGER_CHARACTER_RESONANCE.md without reproducing its quantum sampling
distribution? Yes at the native parameters, with a strong exact
certificate rather than a lucky random witness.

The problem remains unchanged: all primes through B except 3,
M=3^k, N=2*3^(k-1), explicit a_p=log_2(p) modulo N, zero centers,
and output a primitive character with

    S/W >= 1/4,
    S = sum Re(exp(2*pi*i*a_p*x/N))/p,
    W = sum 1/p,
    x mod 3 != 0.

The previous random control already found two accepted characters.
This pass asks for a constructive mechanism and a uniform finite
rounding certificate. It does not adjust the target to recover a gap.

## Freeze The Prefix By Weight

Choose the smallest ordered prime prefix P_z with

    H = sum_(p in P_z) 1/p >= (3/4) W.

This rule depends only on the public problem, not on a successful
assignment. For the native m=1024, B=8167 instance it gives **d=42**
primes through z=191 and H/W approximately 0.7523644178.

Aligning these phases is sufficient if the remaining 982 primes are
charged their worst possible contribution. They are NOT discarded,
assumed random, or given favorable centers.

## Enforce Primitivity In The Lattice

Write Q=N/3 and a for the d prefix labels. Consider

    Gamma_0 = Z^d + (a/Q) Z
            = Z^d + (3a/N) Z.

Since a_1=log_2(2)=1, an integer numerator basis for Gamma_0 is

    A = [ a mod Q ; Q e_2 ; ... ; Q e_d ].

To force x=1 modulo 3, solve nearest vector to the rational target
-a/N in Gamma_0, or -a/3 in its integer numerator lattice.
If v is the resulting integer lattice point, put

    x = (1+3v_1) mod N,
    w = a+3v.

Membership gives w_i=a_i*x modulo N, and x mod3=1 exactly. It is not
enough to use an arbitrary short vector or to require merely x!=0:
such a character can have smaller conductor.

More generally, for residue r=1 or2 and integer prefix centers c,
round to (c-r*a)/3, then w=r*a+3v-c. This supports a finite all-center
certificate for the corresponding shifted weighted objective. The
natural L-function application itself still uses zero centers.

The implementation uses FLINT LLL only to propose a basis. It then
checks every row's lattice membership and the full determinant/index.
Existing normalized integer Gram--Schmidt arithmetic supplies exact
pivots; rational-target rounding divides only the target column by3.
Independent tests compare this to a full Fraction/Bareiss implementation.
All native pivots are also checked using separate leading-Gram
determinants, including the complete 42-dimensional index.

## Certify The Whole Objective

For every real u, cos(2*pi*u)>=1-2*pi^2*u^2>=1-20*u^2.
Therefore the complete score is at least

    (2H-W-20*sum_(i<=d) w_i^2/(p_i*N^2))/W.

No tail estimate or probabilistic hypothesis occurs in this bound.

If the reduced numerator basis has Gram--Schmidt vectors b_i^*, Babai
rounding has, for EVERY real target, squared error at most

    R^2 = sum ||b_i^*/Q||^2 / 4.

Each rounding residual lies in [-1/2,1/2] along an orthogonal
Gram--Schmidt direction. This proves the bound without assuming LLL
quality or interpreting a Haar average as a worst-case guarantee.
Since 1/p_i<=1/2, the complete normalized score is uniformly at least

    (2H-W-10R^2)/W.

The code rounds its rational lower bounds downward to 96-bit dyadics
and independently evaluates all 1024 actual character phases with Arb.

## Native Result

One fixed LLL reduction, one primitive residue class, one nearest-plane
call, no random restart, no coefficient search and no parameter sweep.
The existing 1119-bit public labels and threshold1/4 are unchanged.

- Actual complete weighted score: **0.7606472331**.
- Exact conservative score with every omitted prime set to -1:
  **greater than 0.5047288356**.
- All-prefix-target guarantee from the same basis:
  **greater than 0.5047288356**.
- Primitivity is enforced algebraically, not tested until a lucky vector
  happens to pass.
- LLL basis construction: about **0.650 seconds** in this run. Public
  label preprocessing remains charged, and exact certificate/full-score
  verification took about0.093 seconds. These phase times exclude
  input loading/public-label revalidation and are not total runtimes.
- The prior paid 1024-dimensional Babai basis is NOT used.
- The inherited native ideal quantum mean is about0.3040, not a quantum
  maximum or an executed quantum result.

This rules out using the native weighted task as evidence for quantum
advantage. It is stronger than the previous 2/32 random control: success
follows from a target-independent exact basis certificate with
worst-case accounting of all unoptimized primes.

The complete basis, coefficients, point, primitive character, raw prefix
errors, normalized Gram pivots and interval full score are saved in
classical_baselines/integer_character_primitive_coset.json.
The actual prefix squared error is about6.0244e-16; the all-target
R^2 bound is about1.5354e-15.

## An Asymptotic Classical Route

This part uses existing lattice theorems, not the observed LLL quality.
The dual lattice is

    Gamma_0^* = { y in Z^d : a.y = 0 modulo Q }.

Such a relation implies product p_i^(y_i)=1 modulo M/3. For nonzero y,
unique factorization ensures its positive numerator U and denominator V
are unequal integers. Since M/3 divides U-V,

    M/3 <= |U-V| < z^(||y||_1).

Consequently

    lambda_1(Gamma_0^*) > log(M/3)/(sqrt(d)*log z).

[Banaszczyk's transference theorem](https://arxiv.org/abs/1907.09020)
gives mu(Gamma_0)*lambda_1(Gamma_0^*)=O(d). Hence

    mu(Gamma_0) = O(d^(3/2)*log z/log(M/3)).

This controls the affine primitive coset as well as an arbitrary target;
no homogeneous-vector primitivity assumption is needed.

[The prime harmonic asymptotic](https://dlmf.nist.gov/27.11.E8) gives
W=log log B+C+o(1) and H=log log z+C+o(1). Minimality of the prefix
adds at most1/z. Thus

    log z = exp(O(1))*(log B)^(3/4),
    d <= z = exp(O((log B)^(3/4))) = B^o(1).

For the source family, log M=Theta(m log B)=Theta(B) when the least
allowed modulus is used; a larger modulus only helps the covering bound.
Therefore mu(Gamma_0)=B^(-1+o(1)), tending to zero.

An **exact CVP solver**, applied to the affine target above, consequently
finds a primitive output whose first d phases all approach1. Even with
every remaining phase contributing -1, S/W>=1/2-o(1)>1/4 for all
sufficiently large B. This is an actual classical algorithmic route.
The known [Micciancio--Voulgaris algorithm](https://epubs.siam.org/doi/10.1137/100811970)
supplies the bound

    time 2^O(d) * poly(m,log M), space 2^O(d) * poly(m,log M).

This guaranteed bound is **not polynomial in log M**. It does not prove
dequantization, and a stronger polynomial algorithm may still exist.
Exact CVP was NOT executed in the native pass: its much cheaper Babai
certificate happened to suffice. No finite observation proves that this
continues for unbounded B.

## Attempt To Refute The Interpretation

1. **Does looking at42coordinates cheat?** No. Their combined weight is
   selected by a public exact rule, and all other weights are charged at
   -1. This is not the earlier blind-candidate/random-target argument.
2. **Can x be principal or imprimitive?** No, the affine coset fixes its
   residue to1 modulo3. Merely taking a short homogeneous vector would
   not justify this.
3. **Does LLL automatically give the bound?** No. The saved basis is
   checked exactly. Neither its empirical quality nor transference
   provides a polynomial-time LLL guarantee for all lengths.
4. **Does this solve the earlier uniform-weight CVP?** No. Uniform
   weights would require a prefix of linear dimension, and the geometric
   task and objective differ. That benchmark's own classical witnesses
   remain separate.
5. **Does it sample the quantum law or evaluate full L-values?** No.
   It solves the accepted-witness search task; distribution matching is
   unnecessary for that comparison. Full L-values are not computed.
6. **Is the exact-CVP route a new algorithm or hardness result?** No.
   It is a specialization of standard geometry and an existing solver,
   with a superpolynomial guaranteed cost. It narrows the plausible gap.

## Research Decision

The finite resonance application is convincingly classically solved, not
merely vulnerable to a weak random baseline. Its asymptotic search task
still has a written quantum construction versus a superpolynomial
guaranteed classical bound, but no classical hardness or novelty result.
The heavy concentration in small-prime weights is a substantial classical
advantage and must remain part of every comparison.

Do not spend the next main-model pass sweeping prefix quotas, adjusting
thresholds, optimizing constants or adding more benchmark status records.
Preserve the exact witness and the asymptotic reduction. Further work on
this route requires a genuinely useful external computation or a uniform
algorithmic theorem; otherwise prioritize an independent concrete quantum
mechanism.

Verification:21new tests and357connected tests pass in53.90s with runtime
warnings treated as errors. This includes every native leading-Gram
determinant, rational rounding against independent Fraction/Bareiss
controls, primitive-coset membership and full-score replay. Python/site
syntax, site checks and qsearch validation pass. The full repository
suite was not run; no formal-kernel proof is claimed.

Reproduce:

    python theorems/integer_character_primitive_coset.py
    python -m pytest -q tests/test_integer_character_primitive_coset.py
