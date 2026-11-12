# Odd-degree Galois class groups without GRH

6 November 2026. WRITTEN composition of published arithmetic and quantum
primitives. Independent source/generator core and actual-note full-
composition reviews accepted. No novelty, separation or quantum
execution claim. Section6 extends the result to every fixed odd degree,
charging numerical n! outside the Galois family, and to all retained
irreducible-cubic Selmer dimensions. The even-degree CM/L0 applications
retain their GRH premise.

## Scientific contract and selection

Input is an explicit integral basis and multiplication table for the
MAXIMAL ORDER O_K of a number field K/Q, promised Galois of odd degree n.
Let D=|disc K| and b be the complete binary input length. The order,
Galois/odd-degree promise and arithmetic representation are explicit;
class generators, units, Hilbert class field and class membership are NOT
supplied. For n=1 the output is trivial; below n>=3.

Primary output is the canonical invariant-factor list of Cl(K), omitting
unit factors. The proposed clock is polynomial(b,n,log D,log(1/eta)), with
failure<=eta. A CLASSICAL randomized source supplies a generating list of
prime ideals with high probability; the existing unconditional compact
S-unit algorithm supplies the complete relation lattice. The intended
advance is removal of class-generator GRH on this native subfamily, not
a new quantum primitive or a proven advantage over all classical methods.

Corpus been-tried and baseline queries preceded the work. Independent
comparison first found the general rational-prime source still unpaid:
a PRINCIPAL exceptional zero can suppress the degree-one prime supply.
Random algebraic-integer norms have a different support law and remain
unresolved. The hidden-norm-character Bell route supplied no constructive
multiplication readout; its linear/bilinear moments are essentially
universal. The odd-Galois route is selected because it actually removes
the generator-source blocker and composes to a specified output.

The strongest retained comparator is classical class/unit arithmetic,
including the rigorous ERH subexponential methods in de Boer--Pellet-Mary--
Wesolowski. A polynomial classical prime-generator source does not compute
its complete unit/relation lattice. No classical lower bound is asserted.
The quantum primitive and the class-group-to-S-unit reduction are already
[Biasse--Song, corrected v2, Theorem1 and Section8.2](https://arxiv.org/abs/2510.02280v2).
Their Algorithm5 uses GRH to enumerate a small-norm generating set. Here
we replace that source by randomized polynomial-BIT primes; their numeric
norms need not be polynomial in log D. Theorem1 charges log norm.

## 1. Excluding only the harmful exceptional factor

Set G0=Gal(K/Q), of odd order. The squaring map on G0 is bijective.
For every nontrivial irreducible character rho, its Frobenius--Schur
indicator is |G0|^-1 sum_g rho(g²)=|G0|^-1 sum_g rho(g)=0.
Thus each nontrivial irreducible representation pairs with a DISTINCT
complex conjugate. By Artin factorization and Brauer MEROMORPHIC
continuation, their orders at a real point beta agree as integers.
Therefore

    ord_beta zeta_K = ord_beta zeta_Q
                     + sum_(conjugate pairs rho) 2 dim(rho) ord_beta L(s,rho).

For 0<beta<1, zeta_Q(beta) is nonzero. Every real zero of zeta_K in that
interval has even multiplicity. No Artin holomorphy conjecture is used.
In particular zeta_K has no SIMPLE exceptional real zero.

Actual supporting source: [Sahu's thesis](https://www.imsc.res.in/xmlui/bitstream/handle/123456789/892/HBNI-TH-256_Dhananjaya_Sahu.pdf?isAllowed=y&sequence=1),
Chapter5, Theorem50 (Heilbronn)
already descends any simple real zero through a Galois extension to an
intermediate extension of degree<=2. Corollary53 records the stronger
odd-order statement. The parent read these statements, not only the
March2026 article abstract. The direct character argument above suffices
for the needed simple-zero exclusion.

This does NOT simply assume that all class-character L-functions lack
exceptional zeros. The next calculation permits a nonprincipal exceptional
class character and shows why it does not suppress subgroup escape.

## 2. Uniform counts outside every proper class subgroup

For ANALYSIS ONLY let M/K be the ordinary Hilbert class field, with
G=Gal(M/K)=Cl(K), h=|G|. Neither M nor h is constructed by the sampler.
Apply actual [Thorner--Zaman, arXiv:1803.02823v3, Theorem1.4](https://arxiv.org/pdf/1803.02823)
with its abelian subgroup equal to G. The fixed field is K and the
conductor parameter is Q=1. The scale is D n^n, NOT disc(M).

For each class g and x>=(D n^n)^c2, the theorem gives

    pi_g(x) = h^-1 [Li(x)-chi(g)Li(x^beta)] [1+e_g(x)],
    |e_g(x)| <= C { exp[-c3 logx/log(D n^n)]
                    + exp[-sqrt(c3 logx/n)] }.

Here either the exceptional term is absent, or chi is a real Hecke
character and beta its simple exceptional zero. The constants c2,c3,C
are absolute and EFFECTIVE. Section1 excludes chi=1, whose L-function
would be zeta_K. Thus any surviving chi is nonprincipal.

For ANY proper subgroup J<G,

    sum_(g outside J) chi(g) is 0 or -|J|.

Indeed sum_G chi=0, while sum_J chi is either0 or|J|. Hence the aggregate
main term outside J is at least (1-|J|/h)Li(x)>=Li(x)/2. Summing the
individual RELATIVE errors introduces no factor h: all individual main
terms are nonnegative, and their sum is at most2Li(x). The total main
term over G is exactly Li(x).

Choose once a sufficiently large effective absolute A, and set

    L = ceil(A log2(D n^n)),       X=2^L.

Increase A to ensure X>=exp(16), endpoint relative errors<=1/1024 at
X and2X, and all elementary inequalities below. This is a computable
absolute constant from the cited theorem, not input-dependent advice.
No numerical value of A is claimed implemented in this pass.

Write Delta=Li(2X)-Li(X)>=X/log(2X). For X this large,
Li(2X)+Li(X)<=12 Delta. Dyadic differencing gives at least
(1/2-24/1024)Delta prime ideals outside J. Prime ideals of residue degree
>=2 and norm<=2X number at most n sqrt(2X). Excluding rational primes
ramified in K removes at most n log2 D more degree-one ideals. Increase
A so their sum is<=Delta/16. Consequently the number of unramified
DEGREE-ONE prime ideals outside J with norm in [X,2X) is at least

    Delta/4 >= X/[4 log(2X)].                                  (1)

The same removal leaves at least Delta/2 total degree-one primes.
Every bound is simultaneous for all J; no subgroup enumeration or
membership oracle is used. The harmless exceptional character need not
be found. A least-prime Linnik existence bound alone would not prove(1).

## 3. A bounded classical generating-list sampler

Let n_pad be the smallest power of two >=n. One RAW trial:

1. Draw L uniform bits and add X, giving ell uniform in [X,2X).
2. Test primality deterministically; reject composites and ell dividing D.
3. Decompose ell O_K into its prime ideals. Use finite-algebra/finite-field
   factorization in the explicit maximal order, not an unverified power-
   basis index assumption. Order the factors canonically and pad to
   n_pad slots. Draw one slot with exactly log2(n_pad) random bits.
4. Retain its prime ideal only if it is real and has residue degree1.

Each eligible prime ideal has exactly the same raw probability
1/(n_pad X). By(1), for every current proper generated subgroup J, one
raw trial escapes J with probability at least

    rho = 1/[16 n(L+1)].                                       (2)

There is no prime-rejection normalization hidden in the clock. Finite
field factorization is classical randomized polynomial time with checked
outputs; use bounded trials and allocate recognized arithmetic failures
at most eta/4 over the whole run. On such a failure return ABORT, rather
than conditioning away a difficult prime. No quantum factoring is used
by this source.

The prime decomposition has a direct paid implementation: for unramified
ell, O_K/ell O_K is an n-dimensional finite etale algebra. A uniform
element separates its n geometric embeddings except with probability
<=n(n-1)/(2ell). Since ell>=X is sufficiently large, this is<1/2.
Verify that 1,a,...,a^(n-1) span the algebra; then its degree-n minimal
polynomial is squarefree. Factor it over F_ell and recover prime ideals
by kernels/HNF; a linear factor T-r gives (ell,a-r). Independent capped
retries and checked finite-field factors fit the stated global error
budget. No factorization of ell-1 or hidden class information is used.

An explicit class-number upper bound suffices. Minkowski gives every class
an integral representative of norm<=2^n sqrt(D). The number of ideals
of norm<=Y is at most Y² zeta_K(2)<=Y² zeta(2)^n<=Y² 2^n. Thus

    h <= U=8^n D,       r=ceil(log2 U).

Every proper subgroup extension increases its order by at least2; at most
r such increases are needed. Perform

    T = ceil[128 n(L+1)(r+log(4/eta))]

raw trials and retain all outputs, deduplicating afterward. The growth
indicators stochastically dominate Bernoulli(rho) until completion. Their
mean lower bound is 8(r+log(4/eta)); Chernoff gives probability<=eta/4
of fewer than r increases. The same argument works for adaptive current
subgroups, since each raw trial uses fresh randomness and(2) holds for
EVERY J. Total source failure is<=eta/2 with the arithmetic budget.

The trial count, output-list size, ideal bit lengths O(poly(n,L,b)), and
arithmetic costs are polynomial in the stated input/confidence sizes.
The algorithm does NOT know whether its returned list is complete and
does NOT return a deterministic completeness certificate. Its success
statement is a proved probability over its own randomness for EVERY
promised input field, not an average over fields.

## 4. Completing the quantum composition

Run the source with fixed failure allowance1/100 to obtain S. On its
complete-generation event, the exact sequence is

    U_S -> Z^S -> Cl(K) -> 0,

where the first arrow is the vector of valuations at S. One complete
compact S-unit basis from Biasse--Song Theorem1 gives the FULL integer
relation lattice. Use the valuation coordinates returned with that basis;
expanding enormous units is unnecessary. Smith normal form of this
integer matrix gives the canonical invariant-factor list of Cl(K).

The S-unit theorem is unconditional and charges n, log D, |S| and the
largest log norm in S; all are paid above. Use its full-basis success
event, not separately successful columns. With the usual bounded-error
primitive success>=2/3, one complete run is correct with probability
at least(99/100)(2/3)>1/2. Cap malformed output dimensions and arithmetic
at the primitive's polynomial clock. Repeat fresh complete runs
O(log(1/eta)) times and take the majority of the CANONICAL integer lists.
Do not majority-vote arbitrary unit or ideal bases.

This yields the stated written bounded-error quantum polynomial-time
composition on explicit maximal orders of odd-degree Galois fields.
It does not supply maximal-order preprocessing from a different input
model, a Galois-promise verifier, class-group action matrices, or a
canonical basis of ideal representatives. It does not remove GRH from
the even-degree CM constructions elsewhere in this repository.

One immediate application reuses an already-paid reduction: in
ELLIPTIC_TWO_SELMER_COMPOSITION.md, if the defining irreducible cubic
field is Galois (equivalently its discriminant is a rational square),
this generating source can replace the GRH small-prime set. Adjoin the
fixed bad-prime set S to the random class generators to form T and use
the same full compact T-unit/mod2 valuation construction. The already
paid cubic maximal-order preprocessing and local/real clocks remain
unchanged. Thus that restricted Selmer-DIMENSION composition is also
unconditional; no rational-rank, point, covering-curve or new descent
claim follows. Section6 subsequently extends this consequence to every
retained cubic input.

## 5. Decisive checks and disposition

The cheapest falsifiers are structural: a principal exceptional factor
would invalidate the source bound; an h factor in the error/threshold
would destroy the clock; using only least-prime existence would leave
acceptance unpaid; ignoring higher residue degrees or power-basis index
primes would change the source; incomplete S-unit relations would not
compute the class group. Each is addressed above under the stated model.

One exact cyclic-cubic classical control completed. For
f=X³-11X²-14X-1, reduction modulo2 is irreducible and its discriminant
is163²=26569; hence its field is cyclic cubic. PARI returned the same
maximal-order discriminant, certified its bnf with bnfcertify=1, and
computed class number4 with invariant factors[2,2]. For theta=X modf,
its prime ideals above5 have the following exact certificates:

| Prime ideal | Class coordinates | Principal square generator |
|---|---|---|
| (5,theta-1) | (1,0) | 1-theta |
| (5,theta+2) | (0,1) | -theta-2 |
| (5,theta-2) | (1,1) | 2theta+1 |

All three norm5, residue-degree1 ideals had zero square class, and the
HNF of each squared ideal equalled the HNF of its displayed generator's
principal ideal EXACTLY. The first two classes generate Cl(K); their
S-unit valuation relation lattice is2Z² and has SNF[2,2]. All three
prime classes sum to zero, as required by their principal product(5).
Thus retaining prime factors is different from retaining only the class
of a factored principal ideal. With four padded slots, each prime class
has probability1/4 conditional on drawing rational prime5.

This certifies the small field/class/ideal bookkeeping, not the theorem's
large effective X, generation confidence, runtime or quantum execution.
The first control reached all square-ideal checks but its final metadata
print used an unsupported cypari2 accessor; the same case was rerun with
PARI's supported .disc member. No instance or scientific rule changed.
No broad scan, class library, registry or manuscript promotion follows.

Priority checking found no matching theorem in the narrow searches; that
is not evidence of novelty. Actual Biasse--Song Section8.2 already gives
the generic reduction for ANY succinct generating prime set. The local
classical-source audit confirms that Rigorous Methods Theorems1.3/12.1
remain ERH and subexponential: paying these generators alone does not pay
its smooth relation collection or unit lattice. The source theorem, nonvanishing fact and
S-unit reduction are all published ingredients. The written composition and its source/clock scopes passed independent
actual-text review. Fields outside the subsequent Section6 scope and the
random-norm
support source remain unresolved.


## 6. Fixed odd degree: allowing a principal exceptional zero

6 November 2026. Independent core and actual-text integration reviews
ACCEPTED; the parent verified the original Stark source statement. This extension removes the Galois restriction at FIXED odd degree.
It retains the explicit MAXIMAL ORDER input and charges numerical n!.
Its externally motivated target is the entire retained irreducible-cubic
Selmer-dimension problem, not a new sampler subsystem. The degree-uniform
odd-Galois result above is unchanged and remains the stronger bound there.

Corpus been-tried lookup for Stark/fixed odd degree/cubic Selmer preceded
the literature check. The baselines lookup identifies classical index
calculus; the stronger rigorous ERH comparator in the scientific contract remains
applicable. Existing certified cubic class-group and Selmer controls are
reused. This change is analytic; no quantum implementation or new finite
sweep would test the exceptional-zero bound. It was selected over the
hidden-field Bell route, whose reviewed low-order moments give no decoder,
because it removes a specific assumption from an end-to-end arithmetic
output. No priority or classical lower bound follows from the bounded
literature search finding no matching quantum Selmer theorem.

### 6.1. Actual source gate

[Stark, Some Effective Cases of the Brauer-Siegel Theorem, Invent.math.23
(1974),135--152, Lemma8, p.145](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0023/PPN356556735_0023.pdf)
states the following for an arbitrary degree-n field K/Q, n>1. A real zero
beta of zeta_K in [1-1/(c1(n) log D),1) implies a quadratic subfield F
INSIDE K with zeta_F(beta)=0. Here c1(n)=4 for a normal field and 4n!
otherwise. The parent read the indexed original page containing Lemma8
and its proof, not merely an abstract. Its proof passes to the normal
closure, uses the discriminant and simple-zero bounds, then descends the
zero to a quadratic subfield of K. Sahu's thesis, Chapter5 Theorem51,
independently gives the same 4n! bound in the more general relative form.
No unverified recent claim about Siegel zeros is used.

For ODD n there is no quadratic subfield of K. Thus any real zero beta
of zeta_K in (0,1) satisfies

    delta := 1-beta > 1/[4 n! log D].                         (6)

This is only a zero-free interval near1. Unlike Section1, it does NOT
assert absence of all simple real zeros or automatically exclude the
principal exceptional term in Thorner--Zaman's wider region. We keep that
term and pay for its suppression by increasing log X. More generally the
same argument applies under an explicit no-quadratic-subfield promise,
but no new even-degree application or promise verifier is claimed here.

### 6.2. The dyadic principal term is large enough

Set, with the same effective absolute constant A enlarged as necessary,

    L = ceil[A n! log2(D n^n)],        X=2^L.

Then (6) implies delta log X >= A/4. Put
F(t)=Li(t)-Li(t^beta). The exact derivative is

    F'(t) = (1-t^(-delta))/log t.

Consequently, for Delta=Li(2X)-Li(X),

    F(2X)-F(X) >= (1-exp(-A/4)) Delta.                       (7)

For a PRINCIPAL exceptional character, the aggregate main term outside
any proper J<Cl(K) is (1-|J|/h)F(t). Choose A>=4 log4; its dyadic
increment is at least3 Delta/8. Endpoint relative errors <=1/1024 cost
at most12 Delta/1024 in this case, since 0<=F(t)<=Li(t). The old uniform
24 Delta/1024 bound also suffices. Removing at most Delta/16 higher-
degree and ramified primes leaves more than Delta/4 eligible degree-one
prime ideals outside J. For a NONPRINCIPAL exceptional character or no
exceptional term, Section2 applies unchanged with the larger X. Thus
in ALL cases the same simultaneous lower bound holds:

    # eligible primes outside J in [X,2X) >= X/[4 log(2X)].  (8)

No class-number-dependent constants, principal-zero detection, subgroup
membership oracle or constructed Hilbert class field enters the source.
A pointwise lower bound on F alone would not justify dyadic subtraction;
the derivative identity is the needed step.

### 6.3. Source and quantum clock

Use exactly Section3's RAW integer/padded-slot source with this new L.
Each eligible prime ideal still has probability1/(n_pad X) per raw trial.
The same rho=1/[16 n(L+1)], U=8^n D, r=ceil(log2 U) and trial count

    T = ceil[128 n(L+1)(r+log(4/eta))]

give a complete generating list except with probability<=eta/2, including
the globally capped finite-field arithmetic failures. All primes rejected
as composite, ramified, high-degree or padded slots are charged. The
finite-etale decomposition proof uses only an explicit maximal order,
not the Galois promise, so it carries over unchanged.

The complete compact S-unit/valuation/SNF construction and fresh canonical
integer-list majority in Section4 therefore have total bounded-error time

    polynomial(b,n!,log D,log(1/eta)).                        (9)

This is unconditional and polynomial for EACH FIXED odd degree. It is
NOT a polynomial(n,log D) theorem for arbitrary nonnormal fields. Neither
a few small primes nor a least-prime existence bound substitutes for(8).
The strong classical unit/relation computation remains unpaid by merely
supplying this classical generator list; no separation is established.

### 6.4. Full retained cubic Selmer consequence

For EVERY monic irreducible separable cubic f in binary, the existing
ELLIPTIC_TWO_SELMER_COMPOSITION.md pays its maximal order after Shor
factorization of disc(f). Here n=3 and n!=6. The random generator list
has polynomial size and O(log D)=O(b)-bit prime norms. Adjoin it to the
fixed bad-prime set S to form T. This replaces the original GRH factor
base for ALL these inputs, including non-Galois cubic fields.

Use the same one complete compact T-unit basis, mod2 valuation kernel,
norm-square rows, small squareclass representatives and paid local/real
filters. Completeness of T is one additional per-run event: run the
source at failure<=1/100 and budget the remaining known arithmetic/quantum
failures so the correct canonical INTEGER dimension has probability>1/2.
Fresh complete-run majority then gives failure<=eta. No class-group
membership test or full class-group output is needed in the descent.

The resulting WRITTEN composition computes dim_F2 Sel2(E/Q) in
unconditional bounded-error quantum polynomial(b,log(1/eta)) time on the
retained input family. It does NOT compute Mordell--Weil rank, rational
points or covering curves, and makes no novelty or execution claim.
Siksek--Smart1997 already supplies the classical polynomial descent
reduction; the change here pays its class-generator premise through
published analytic and quantum arithmetic machinery.

Next hard question: select an independent constructive direction against
an explicit route through the remaining quadratic-field source blocker.
That blocker is not removed by (6), and no nearby sampler variant is
commissioned without a mechanism. The scoped actual-text review of
Section6 and the Selmer replacement is
COMPLETE and accepted these three gates: numerical n! charge, principal-
term dyadic bound, and all-cubic input scope. No controls were rerun.
Next selection begins with the corpus lookup and primary literature for
a concrete operation, not another finite confirmation of this theorem.


End-of-pass independent selection compared three concrete successors and
admitted NONE. Random algebraic-integer norms with Shor factorization and
all prime factors returned have a paid source but no field-uniform
outside-subgroup coverage argument; their correlated law is not the
inverse-norm Euler law. Imperfect Hankel outcomes have no efficient
coefficient-constraint decoder beyond the reviewed rare exact recurrence.
The hidden-field Bell full law has no paid inversion; the low-order moment
and fixed-displacement obstacles remain as scoped in its note. The parent
checked these against the current source/receiver contracts. These are
missing algorithms, not impossibility or hardness results. No new note,
sweep or subsystem was commissioned. Uniform poly(d,logp) native character
reconstruction remains an externally motivated question, but none of the
three supplies its needed operation. Next pass must compare a distinct
native mechanism before returning to these gaps.
