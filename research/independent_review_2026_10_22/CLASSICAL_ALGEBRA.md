# Native algebraic attack audit

Labels below distinguish exact reductions from algorithms and conjectures.
The input remains the supplied field, distinct points, and arbitrary target
bits at N=n², K=floor(N/8). No witness or oracle is added.

## Exact rational parametrization; unresolved coupled reconstruction

**Proved deduction.** Choose c with Tr(c)=1 by binary linear algebra. For
each target b, the map

    t -> inv0(t²+t+b*c)

is exactly two-to-one onto the accepted root set. This follows because
t²+t has kernel {0,1} and image the trace-zero hyperplane; inv0 is a
permutation. It handles zero correctly when b=0. Independently sampling
t therefore produces precisely the usual accepted-root proposal.

Substituting these rational expressions into Hx=0 does not decouple the
K checks. On the stratum with no zero denominators, clearing denominators
produces equations of total degree at most 2(N-1). An equivalence for every
witness must also handle legal zero branches; for finding one witness,
CONIC_REFORMULATION.md now justifies restricting to the nonzero stratum
at sufficiently large native n. This is an exact reformulation, not a
polynomial solver. Calling the t_i free parameters before imposing H is
the missing step in a putative dequantization.

There is also an exact polynomial reconstruction formulation. Put
P(X)=product_i(X-alpha_i). Every native codeword is

    x_i=F(alpha_i)/P'(alpha_i),  deg F < N-K.

On the nonzero-coordinate stratum, seek F and Z satisfying

    F*(Z²+Z+c*E_b) = P' mod P,

where E_b(alpha_i)=b_i. Here Z is a residue class modulo P, not a
low-degree rational function supplied for free. The congruence follows
coordinatewise from the Artin–Schreier image identity. It retains the
fixed-numerator inverse reconstruction problem. Merely running ordinary
rational interpolation with both numerator and denominator free changes
the problem. Zero coordinates require separate totalized-inverse equations.

**Strongest falsifier / next step:** a bounded algorithm solving this
fixed-numerator congruence for every input at the stated degree bound would
be a genuine native classical attack. A degree count or the abundance of
solutions does not supply that algorithm.

## A concrete failure of the minimum-support scaling shortcut

**Proved counterexample, found by a bounded exact control.** For a support
S of size K+1, let P_S=product_(a in S)(X-a). The supported minimum-weight
codewords have x_a=t/P_S'(a), t nonzero. To make all supported trace bits
one, lambda=1/t must solve

    Tr(lambda*P_S'(a))=1 for all a in S.

Odd field degree does not guarantee consistency. In F_32 represented by
z^5+z²+1, take S=(0,1,z,z+1,z²), encoded as integers (0,1,2,3,4).
The derivative values, in that order, are (24,30,20,18,10).
The first, fourth and fifth XOR to zero: 24+18+10=0. Their three required
trace equations would sum to 0=1. No scaling works. The second, third and
fifth give another odd dependency. This is an algebraic contradiction,
not a failure to find a scaling experimentally.

The small-field search checked 56 supports of size three in F_8 without
a counterexample; extrapolating that success to odd fields would have been
wrong. The F_32 example falsifies the proposed shortcut only. Its K=4,
length-five shortened block is not itself an asymptotic native instance,
and it does not defeat the quantum construction or all adaptive supports.

## Several affine denominator parameters do not remove pole rigidity

**Proved deduction.** Consider a fixed family

    x_i(U)=inv0(a_i*L_g(i)(U)),

where U ranges over F_q^r, a_i is nonzero, and the nonconstant affine
linear forms L_g are distinct up to proportionality (absorbed into a_i).
Allow additional coordinates that are fixed constants. Suppose Hx(U)=0
is a rational identity away from the pole hyperplanes. Then, for each g,
the vector supported on its coordinate group, with entries a_i^(-1),
is itself in C. The fixed constant-coordinate vector is also in C.

Proof: the parity identity has the form c+sum_g v_g/L_g=0. Multiply by
product_g L_g and reduce modulo L_g. The quotient polynomial ring is a
domain and the other forms remain nonzero, forcing v_g=0. Do this for
every g, then c=0. Each nonempty group therefore has at least K+1 entries,
by the minimum distance of C. Totalizing a pole to zero preserves parity,
because it removes a whole supported codeword.

Within a group the target bits are Tr(a_i*L_g(U)), a binary linear image
of one field element. Thus the number of target patterns achieved by this
fixed family is at most

    2^[n*floor(N/(K+1))],

regardless of how many formal parameters r were introduced. Fixed
coordinates contribute a fixed pattern only. This bound is far below 2^N
in the asymptotic native regime. It extends the one-parameter residue
argument to any number of affine denominator parameters.

This is not relying on a gratuitous formal-identity assumption when a
family is claimed to preserve parity for *every* unrestricted field
parameter: if q>2N, a nonzero cleared numerator of degree at most G would
have at most G*q^(r-1) zeros, while the complement of G pole hyperplanes
has at least q^r-G*q^(r-1) points. Hence that all-parameter claim forces
the same identity. A parameter domain restricted after examining b need
not satisfy this counting premise.

**Self-attack / boundary:** the family coefficients may be selected
adaptively from b, numerator polynomials may be nonconstant, or parity may
hold only on a specially solved parameter locus. None is ruled out by
this theorem. In particular, choosing a target-specific supported
codeword as a residue is already a nonlinear native search task; it
cannot be called a free parametrization. The next meaningful attack must
solve that adaptive choice, rather than count the nominal parameters.

## Accepted flats: what is verified and what is still missing

**Experimental observation, independently verified:** the resident n=17
and n=31 accepted-flat receipts contain actual native solutions. The
separate extended-Euclidean field verifier checks irreducibility, all K
field syndromes and all N trace bits; see checkpoint_verification.json.
It verifies the witnesses, not the construction runtime or all targets.

**Conditional attack:** if accepted affine sets a_i+V_i can be constructed
in polynomial time and the binary map

    product_i V_i -> F_q^K, (v_i) -> sum_i H_i*v_i

has full row rank, solve the affine syndrome equation by binary Gaussian
elimination. The local acceptance certificates and this actual rank are
both necessary. The dimension prerequisite is sum dim(V_i)>=nK; it is
not a sufficient rank theorem.

The reviewed construction enumerates local flats with 2^d points and
solves linear trace conditions on a scale parameter. Its certified regime
gives d of logarithmic order in n. This is useful at the verified finite
sizes, but N*d eventually falls below nK for fixed K/N=1/8. This failure
of a dimension prerequisite is specific to that family; it is no lower
bound against larger flats, adaptive families, or nonlinear proposals.

The classification of affine spaces whose *whole inverse image is affine*
does not classify flats on which just Tr(inv0(x)) is constant. Confusing
those properties would incorrectly exclude possible attacks. See the
[primary inverse-image classification](https://arxiv.org/abs/2206.14980).

Further literature checks do not close this gap. [Ostafe, Section 8](https://arxiv.org/html/1410.1252v2) explicitly leaves the analogous
small-affine-space exponential-sum result for the inverse function outside
its polynomial theorem. This establishes the scope of that paper, not a
claim that the question is still open in all current literature. Also,
[Carlet's inverse-sum identity](https://link.springer.com/article/10.1007/s10623-024-01531-6) gives
sum_(v in V) 1/(a+v)=L'_V/L_V(a)!=0 for a outside V. Its trace can be zero;
it does not prohibit a scalar inverse-trace constant flat. Zero-sum
subspace counts likewise address one field sum, not all pointwise bits.

A narrow countercontrol checked all 155 three-dimensional binary linear
subspaces of F_32 and their four affine cosets, with modulus X^5+X^2+1.
None was constant for either inverse-trace bit; the receipt is
affine_flat_countercontrol.json. This falsifies a proposed universal
half-dimension-plus-rounding flat rule already at n=5. It establishes
nothing about maximum dimension at n=17,31,61 or an asymptotic O(log n)
upper bound. In particular, failure of the generic flat construction is
not evidence that all larger, specially chosen flats are absent.

**Next decisive obligation:** construct accepted flats with enough total
dimension and prove the needed global rank for arbitrary given points,
or give an adaptive nonlinear reconstruction that avoids this requirement.

**Subsequent resolution on substantial subfamilies:**
SUBFIELD_EXTENSION_ATTACK.md supplies exactly that missing rank argument
when n is even and there are at least 2K zero targets, or when 3 divides n
and there are at least 3K zeros. It uses the original arbitrary points and
bits. The remaining obligation here concerns prime degrees and targets
outside those guarantees; the earlier logarithmic-flat limitation must
not be reported as excluding these new algorithms.

## Coding and algebraic relaxations do not yet settle the problem

**Proved local checks:** the exact totalized inverse graph is described by
x²y=x and xy²=y over F_q, together with Tr(y)=b. If x=0 these force y=0;
if x is nonzero the first forces y=1/x. Each equation is quadratic over
the binary coordinates. The equation xy=1 alone discards legal zeros.

The repository's degree-two closure argument was reconstructed: two native
codewords supported on K+1 coordinates and meeting only at one coordinate
give a local covariance correction. Such supports exist when N>=2K+1.
This explains why that formal degree-two relaxation cannot constrain the
projected x variables beyond Hx=0. It does not prove that higher-degree
algebraic algorithms are expensive.

A field-degree comparison alone is also insufficient: the number of
Boolean unknowns greatly exceeds the N final trace constraints, but an
explicit inverse map or a proven algorithm for this structured system is
still needed. Generic statements about underdetermined equations, finite
successes, and random-oracle hardness do not fill that gap.
