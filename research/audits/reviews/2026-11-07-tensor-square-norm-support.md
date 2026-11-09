# Tensor-square support theorem for rational norm equations

Date: 2026-11-07. Independent mathematical review of the proposed support
reduction. No Git, network, external API, normal-closure construction or
norm-equation implementation was used. Parent owns prior-art and source
audits. This is a support theorem with an explicit class-generation
hypothesis, NOT by itself a paid arbitrary-field quantum norm solver.

## 1. Precise statement and verdict

Let L/Q be ANY number field of degree n, with no normality assumption,
and let a be in Q*. Decompose the finite etale algebra

    L tensor_Q L = product_{j=1}^t E_j.

Retain, for each factor, BOTH embeddings

    iota_{j,1}, iota_{j,2}:L -> E_j

induced by x tensor 1 and 1 tensor x. Isomorphic factors must not be
merged while discarding these maps. The sum of their absolute degrees is
n^2. Since each contains L, there are at most n factors and

    sum_j [E_j:iota_{j,1}(L)] = n.

Let S be a finite set of rational primes containing:

1. every rational prime ramified in L;
2. every prime in the numerator or denominator of a;
3. every rational prime below a chosen class-generating set of prime
   ideals of EACH E_j.

Write S_M for all primes of a field M above S. Then

    a in Norm_{L/Q}(L*)
        iff
    a in Norm_{L/Q}(O_{L,S_L}*).                            (1)

The nontrivial direction of (1) is correct. The proof below handles
unequal residue degrees, fractional divisors, exact signs and ordinary
rather than narrow ideal classes. No counterexample was found to this
precise statement.

The restriction a!=0 is necessary: zero is a norm of zero but cannot be
the norm of an S-unit. The reverse implication in (1) is immediate.

## 2. Paired element norms and paired divisor norms

For b in E_j*, define elements of L by

    u_{j,k}(b)=iota_{j,k}^{-1}(
                  Norm_{E_j/iota_{j,k}(L)}(b)),  k=1,2,
    y_j(b)=u_{j,1}(b)/u_{j,2}(b).

Norm transitivity gives the EXACT rational identities

    Norm_{L/Q}(u_{j,1}(b))=Norm_{E_j/Q}(b)
                         =Norm_{L/Q}(u_{j,2}(b)),
    Norm_{L/Q}(y_j(b))=1.                                  (2)

This is +1, not merely a rational number with zero finite valuations.
Thus negative a and archimedean signs introduce no defect in this step.

Let Div(M) denote the free abelian group of nonzero prime ideals of a
number field M. The relative ideal norm, followed by identification
through iota_{j,k}, defines a homomorphism

    N_{j,k}:Div(E_j) -> Div(L).

Put partial_j=N_{j,1}-N_{j,2}. Norms of principal fractional ideals give

    partial_j(div(b))=div(y_j(b)).                           (3)

For a prime Q of E_j above a prime P of the embedded L, the norm exponent
is the RELATIVE RESIDUE DEGREE f(Q/P). It is not the ramification index.
All primes over a rational prime remain over that same rational prime
under either norm. In particular, S-supported divisors have S-supported
paired boundaries.

## 3. Local tensor decomposition at an unramified prime

Fix p outside S. Then L is unramified at p and

    L tensor Q_p = product_{i=1}^r K_{f_i},

where K_f is the unramified extension of Q_p of degree f and f_i is the
residue degree of the corresponding L-prime P_i. The standard unramified
tensor identity is

    K_f tensor_{Q_p} K_g
       = product_{s=1}^{gcd(f,g)} K_{lcm(f,g)}.              (4)

For example, (4) follows first for finite residue fields by Frobenius
orbits on pairs of embeddings, and then by unique unramified lifting.
This is a proof device; the algorithm need not construct a global normal
closure. It also shows directly that every E_j is unramified at p.

Since (L tensor L) tensor Q_p is simultaneously the product of the
completions of the E_j and the product of all K_{f_i} tensor K_{f_l},
for EVERY pair i,l there is a prime Q in some tensor factor E_j whose two
contractions are P_i and P_l, and whose absolute residue degree is
lcm(f_i,f_l). Consequently, writing g_il=gcd(f_i,f_l),

    partial_j(Q)
        =(f_l/g_il) P_i - (f_i/g_il) P_l.                   (5)

These are the primitive pair syzygies. The multiplicity gcd(f_i,f_l) in
(4) is harmless: any one component supplies (5). Different choices may
lie in different E_j or in different primes of one factor; all factors
are retained. A paired cycle always lies inside one diagonal global
embedding orbit, which is why no missing tensor factor is being assumed.

Equivalently, Frobenius acts on the n embeddings of L with cycle lengths
f_i. Its orbit on a chosen ordered pair from cycles i,l has length
lcm(f_i,f_l), with projection degrees lcm/f_i and lcm/f_l. This recovers
(5) with exactly the same coefficients.

The proof is not extended to ramified p: inertia can change this simple
pair-cycle description. Such primes were deliberately included in S.

## 4. Primitive pair syzygies generate the FULL integer kernel

For any positive integers f_1,...,f_r, define

    K=ker_Z [f_1 ... f_r],
    c_il=(f_l/gcd(f_i,f_l)) e_i
          -(f_i/gcd(f_i,f_l)) e_l,
    M=span_Z{c_il:i<l}.

Then

    M=K.                                                   (6)

Proof. Clearly M is contained in K. Over Q the pair vectors span the
rank-(r-1) kernel, so M has finite index in K (the r=1 case is zero).
Fix ANY rational prime ell and work over R=Z_(ell). Choose i with minimal
ell-adic valuation of f_i. Then f_l/f_i belongs to R for every l, and

    h_l=e_l-(f_l/f_i)e_i,  l!=i,

is an R-basis of K tensor R. This statement does not invert a nonunit
illegally: the relation sum f_l v_l=0 is equivalent, in the domain R, to
v_i+sum_{l!=i}(f_l/f_i)v_l=0 after factoring out the nonzero f_i.
Also f_i/gcd(f_i,f_l) is an ell-adic unit, so

    c_il=-(f_i/gcd(f_i,f_l))*h_l

is a unit multiple of that basis vector. Thus M tensor R=K tensor R for
every ell. A nontrivial finite index would have a prime divisor and
survive that localization, a contradiction. This proves (6), without a
saturation operation or a hypothesis gcd(f_1,...,f_r)=1.

Two useful countercontrols distinguish this argument from false shortcuts:

* Using NONprimitive vectors f_l e_i-f_i e_l fails already for (2,2):
  it gives 2(e_1-e_2) and misses the kernel vector e_1-e_2. The tensor
  residue degree is lcm=2, not the product 4.
* Keeping a SINGLE fixed star globally can also fail. For (2,3,5), the
  pivot-2 star (3,-2,0),(5,0,-2) has index 2 in the kernel and misses
  (-4,1,1). The remaining pair (0,5,-3) repairs it; indeed twice the
  first, minus twice the second, plus the third equals (-4,1,1).
  The minimizing pivot in the proof is allowed to depend on ell.

This is also effective integer linear algebra: there are O(r^2) vectors,
their entries are at most max f_i, and HNF computes their exact lattice.
In the field application r<=n and f_i<=n. The proof's localization over
all primes is not an algorithmic instruction to enumerate primes.

## 5. Exactness away from S and principalization

Restrict divisors to primes outside S. Equations (5)--(6) show exactness
at the middle of

    direct_sum_j Div(E_j outside S)
           --sum partial_j--> Div(L outside S)
           --Norm--> Div(Q outside S).                     (7)

No right-surjectivity is asserted. At p the last map has coefficients
f_i and its image may be gcd(f_i) Z; only its kernel is needed.

Now suppose x in L* has Norm_{L/Q}(x)=a. Let D be the outside-S part of
div(x). Since a is supported on S, for each p outside S its valuations
v_i satisfy sum_i f_i v_i=0. By (7) there are finitely supported fractional
divisors D_j on E_j, supported outside S, such that

    D=sum_j partial_j(D_j).                                (8)

The coefficients can be positive or negative; no effective-divisor claim
is needed. By hypothesis, classes of primes over S generate each ordinary
Cl(E_j). Choose a fractional S-supported divisor A_j with
[A_j]=[D_j]. Thus

    D_j-A_j=div(b_j)

for some b_j in E_j*. By (3), the outside-S divisor of y_j(b_j) is exactly
partial_j(D_j). Define

    x_S=x / product_j y_j(b_j).

Equation (8) implies div(x_S) is supported on S. Equation (2) implies

    Norm_{L/Q}(x_S)=a

as an EXACT signed rational equality. This proves (1).

Ordinary ideal classes suffice: no totally positive principal generator
is requested, and the ratio in (2) preserves the original norm sign for
any choice of b_j. Repeated/isomorphic tensor factors cause no problem
provided their two embeddings remain attached to them.

## 6. What this proof pays, and what it does not

Established:

* total auxiliary absolute degree n^2, with at most n field factors;
* a local primitive-syzygy formula at every unramified p outside S;
* full INTEGER kernel generation, rather than a finite-index sublattice;
* exact support removal by paired norms, including signs and fractions;
* applicability to arbitrary, possibly non-Galois L and to n=1.

The divisors D_j and elements b_j are existential objects built from an
already existing solution x. A solver reducing the task to the norm map
on the finite S-unit group need not first know x, factor its divisor, or
construct these b_j. Conversely, this proof must not be described as an
algorithm that computes those objects without paying that input access.

Outstanding resource/source obligations for a native polynomial solver:

1. Construct the tensor factor fields, their BOTH embeddings and integral
   arithmetic with polynomial bit sizes. The dimension bound alone is
   not a cited factoring or integral-basis theorem.
2. Supply a polynomial-size, polynomial-bit CLASS-GENERATING set for every
   arbitrary E_j, with a proved clock and success event. These fields need
   not be Galois or odd-degree. The current odd-Galois source theorem must
   not be transferred to them. Taking every prime below a numerical
   Minkowski bound would not by itself give a polynomial list.
3. Pay a complete compact S-unit basis of L and the exact rational norm
   membership/reconstruction computation. Handle a=0 separately if the
   eventual API includes it.

No Hasse norm principle was proved or assumed: local solvability need not
imply global solvability. The theorem preserves the EXACT global norm
image inside a sufficiently supported S-unit group; it does not replace
global membership by local tests. It is unrelated to quaternion reduced
norms and supplies no claimed novelty or speedup before the parent's
source and classical-baseline comparison.
