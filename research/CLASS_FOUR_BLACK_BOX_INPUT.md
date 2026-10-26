# Class-Four Input Transport Without A Coherent Decoder

2026-10-21. WRITTEN REDUCTION AND TESTED PUBLIC WORD EVALUATORS.
Not an executed quantum preprocessing routine, independently reviewed HSP
theorem, novelty claim or application. The class-four receiver remains a
proposal. This removes a specific supplied-coordinate assumption from its
WRITTEN input reduction, conditional on the remaining receiver proof.

Extension: [CLASS_FOUR_PRIME_POWER_INPUT.md](CLASS_FOUR_PRIME_POWER_INPUT.md)
uses an annihilating p-power instead of p, mixed-order additive relations,
and local order-p extraction. The field-valued construction below remains
the simpler exponent-p case. The extension does not validate the receiver.

## Question And Precise Access Model

Can the supplied Lie table be obtained from an ordinary black-box group
without assuming a free normal-word presentation or coherent logarithm?

Assume a known prime p>4; a promised exponent-p group G of class <=4;
unique n-bit encodings of group elements; an identity encoding; s supplied
group generators; and coherent reversible multiplication. The HSP oracle
f separates left cosets gH and is callable on these encodings. Both types
of oracle call are charged. Multiplication is not the hiding oracle.
The group/exponent/class/encoding promises are not inferred from tests.

The proposal below only needs FORWARD encoding of chosen Lie coordinates
into G. It never coherently decodes an unknown encoded element. A supply
of coset states WITHOUT the hiding oracle would be a different interface.

## 1. Make The Underlying Additive Group Available

Effective inverse BCH is established mathematics, not new here; see
[Cicalo, de Graaf and Vaughan-Lee](https://doi.org/10.1016/j.jalgebra.2011.11.031).
The existing BOUNDED_CLASS_METABELIAN_HSP.md gives the explicit class-four
corrections and a universal rational free-word certificate.

For the convention [a,b]_G=a^-1 b^-1 a b, define

```
w=[g,h]_G, u=[g,w]_G, v=[h,w]_G,
A=[g,u]_G, B=[h,u]_G, C=[h,v]_G.

ADD(g,h) = g h w^(-1/2) u^(-1/12) v^(1/12) A^(-1/24) C^(1/24)
BRACKET(g,h) = w u^(1/2) v^(1/2) A^(1/3) B^(1/4) C^(1/3).
```

They represent exp(log(g)+log(h)) and exp([log(g),log(h)]). A rational
power a/b means ordinary exponent a*b^-1 mod p, computed by repeated
squaring; it is NOT a root or discrete-log oracle. The group elements
need not expose matrix entries or normal-word digits.

NEW `theorems/class_four_group_words.py` evaluates exactly these words
with only multiplication, the identity and p. Its conservative counts in
original multiplications, for ell=p.bit_length(), are

```
power: <=2ell; ADD: <=30ell+21; BRACKET: <=34ell+23;
an additive combination of k elements: <=k*(32ell+21).
```

These are classical word-evaluation counts, not native quantum gate counts.
Straight-line reversible computation, controlled arithmetic and workspace
uncomputation add charged polynomial overhead. A Python callable is not
itself a coherent oracle implementation.

## 2. Group Generators Are Not An Additive Basis

Let a_1,...,a_s be the supplied group generators. Enumerate the right-nested
LIE brackets [a_i,[a_j,...]] of lengths one through four using BRACKET,
not uncorrected group commutators. Keep a list b_1,...,b_t; zero entries
may be dropped. Then t<=s+s^2+s^3+s^4.

The linear span of all these words is a Lie subalgebra: Jacobi rewrites
brackets as linear combinations of right-nested words, and words of
length >4 vanish. Its exponential is a subgroup containing the original
generators, hence is all G. Consequently b_1,...,b_t span the additive
Lie algebra. They need NOT be independent.

This step is essential. In UT5, the four adjacent elementary transvections
generate G, but their logarithms have additive rank four, whereas dim L=10.
The new opaque-encoding control recovers rank ten only after bracket closure.
Using the original generators directly in a purported additive basis would
prepare the wrong source and omit valid group directions.

## 3. Acquire A Basis By Known Abelian HSP

The public function

```
F: F_p^t -> G,     F(c)=ADD_i(b_i^c_i)
```

is a homomorphism onto the ADDITIVE group of L. Uniqueness of the output
encoding makes its fibers exactly the cosets of ker F. Its circuit uses
O(t log p) group operations, plus reversible overhead, and ZERO calls to
the original hiding oracle f.

Apply known abelian HSP to F. This is the kernel-and-quotient method of
[Cheung--Mosca, Algorithm 10](https://arxiv.org/pdf/cs/0101004), specialized
to known exponent p, so ordinary finite-field elimination replaces the
general integer relation bookkeeping. It is a dependency, not a new
group-decomposition algorithm or a classical dequantization.

Given the correct kernel K, compute a complement C to K in F_p^t and encode
its basis vectors using F. The resulting d elements g_1,...,g_d form an
additive basis, where d=t-dim K. The rank d need not be supplied. Check
every proposed kernel generator by F(k)=identity, but do NOT infer kernel
completeness merely because all supplied relations are sound. The quantum
subroutine's bounded-error guarantee remains charged.

We never need the inverse of F on a quantum register. F is many-to-one
before this basis acquisition; calling its value a coordinate permutation
would be false. Likewise, ordinary products b_1^c_1 ... b_t^c_t are NOT
the homomorphism F in a nonabelian group.

## 4. Compute Only The Coordinates Actually Needed

For each pair i<j compute z=BRACKET(g_i,g_j) by public group words.
Define another public additive homomorphism

```
F_z: F_p^(d+1) -> G,
F_z(c,u)=ADD(ADD_i(g_i^c_i),z^u).
```

Its kernel is the line span((-coord(z),1)). Known abelian HSP finds this
line. Require dimension one and a nonzero last coordinate; normalize that
coordinate to one, negate the others, and verify the result by forward
encoding. This obtains every structure constant with at most binom(d,2)
additional abelian-HSP calls. Computing these CLASSICAL coordinates during
setup is not an implementation of a coherent arbitrary-element decoder.

There are at most 1+binom(t,2) kernel-learning calls even on a bad earlier
history. Impose fixed input-size polynomial clocks on every call. Reject
malformed outputs, failed relations, wrong line dimensions or an invalid
resulting bracket table. Check alternation, Jacobi and class <=4 publicly;
these consistency checks do not replace the probabilistic basis guarantee.

For total setup error delta, give each kernel call failure <=delta/Cmax,
where Cmax=1+binom(t,2). One convenient amplification is to repeat a
constant-error kernel algorithm independently and take a majority of its
canonical reduced-row bases. Each map's domain is FIXED, so its correct
kernel has a unique encoding. O(log(Cmax/delta)) repeats suffice, with
inverse-polynomial quantum precision inside each constant-error run.
This keeps the amplification cost logarithmic without relying on rare-
branch renormalization. All clocks also apply after an incorrect earlier
kernel estimate, where a later promised one-dimensional kernel can fail.

At constant base error, a k-dimensional kernel-domain call can use k+2
Fourier samples: the ideal rank failure is at most
1/(p^2*(p-1)), leaving room for approximation. Thus one conservative setup
operation scale, before outer kernel amplification, is

```
O((s^4 + t*(t+2) + d^2*(1+(d+1)*(d+3))) * log p)
```

in group multiplications, plus polynomial Fourier/field/bit work. This
is an asymptotic envelope, not an executed preprocessing benchmark. It
must be ADDED to the receiver cost, not counted as a free presentation.

## 5. Pull Back The Original Hiding Oracle Cleanly

Fix the successfully learned basis and table for the remainder of a run.
Let E:F_p^d->G be its forward additive encoder. Compile

```
|x>|0>|0> -> |x>|E(x)>|0>
          -> |x>|E(x)>|f(E(x))>
          -> |x>|0>|f(E(x))>.
```

The last step reverses the PUBLIC ENCODER while retaining x. It does not
evaluate E^-1 and does not uncompute the hiding label. Trace the hiding
output when preparing mixed coset states. Since E identifies the computed
BCH multiplication with multiplication in G, f o E hides exactly the
transported subgroup. One pulled-back query uses one original f query
plus O(d log p) group operations and reversible overhead.

Subsequent subgroup restrictions, normalizers and quotient sections can
be computed in the acquired Lie coordinates. Their forward maps compose
with E; the original black-box coordinate inverse is still unnecessary.
Encode the final subgroup generators back into G using E.

Amplify the receiver in THIS FIXED coordinate chart. Reacquiring unrelated
bases before each run and taking a literal majority of generator strings
would be invalid: the same H can have different generating sets. Allocate
epsilon/2 to setup and epsilon/2 to the existing fixed-chart receiver's
canonical-output amplification. Setup uses no information about H.

## Scope, Falsifiers And Next Step

Conditional corollary: if the proposed explicit-Lie class-four receiver is
correct, the same ordinary HSP is polynomial-time quantum solvable for the
unique-encoding black-box exponent-p/class<=4 input above, with known p>4.
This does not establish the receiver, general exponents, small primes,
nonunique encodings, a state-only reduction, novelty or a useful application.

This route fails if a required operation needs hidden input, if the bracket
closure does not span, if the encoded function is not additive, if a decoder
is smuggled into oracle cleanup, or if group operations/quantum kernel calls
are left uncharged. Tests specifically reject the generator-span and
ordinary-product substitutions. The prior polynomial-valued hiding-label
classical filter still applies whenever its stronger explicit-label input
promise holds; opaque group encodings do not establish an application gap.

Implemented: public group words, bracket spanning family and forward
combinations, with opaque-token controls through a 127-bit prime. NOT
implemented: quantum kernel acquisition, coherent compilation, full receiver
or independent proof review. Keep the main theorem UNDER REVIEW. The next
high-value task is a whole-proof/application challenge, not another inverse-
BCH fixture or rewriting the existing transcript-induction argument.
